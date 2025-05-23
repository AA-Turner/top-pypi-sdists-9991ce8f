""" JobManagerHandler is the implementation of the JobManager service
    in the DISET framework

    The following methods are available in the Service interface

    submitJob()
    rescheduleJob()
    deleteJob()
    killJob()

"""
from DIRAC import S_ERROR, S_OK
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Core.DISET.MessageClient import MessageClient
from DIRAC.Core.DISET.RequestHandler import RequestHandler
from DIRAC.Core.Utilities.ClassAd.ClassAdLight import ClassAd
from DIRAC.Core.Utilities.DErrno import EWMSJDL, EWMSSUBM
from DIRAC.Core.Utilities.JEncode import strToIntDict
from DIRAC.Core.Utilities.ObjectLoader import ObjectLoader
from DIRAC.FrameworkSystem.Client.ProxyManagerClient import gProxyManager
from DIRAC.StorageManagementSystem.Client.StorageManagerClient import StorageManagerClient
from DIRAC.WorkloadManagementSystem.Client.JobStatus import filterJobStateTransition
from DIRAC.WorkloadManagementSystem.Client import JobStatus
from DIRAC.WorkloadManagementSystem.Service.JobPolicy import (
    RIGHT_DELETE,
    RIGHT_KILL,
    RIGHT_RESCHEDULE,
    RIGHT_RESET,
    RIGHT_SUBMIT,
    JobPolicy,
)
from DIRAC.WorkloadManagementSystem.Utilities.ParametricJob import generateParametricJobs, getParameterVectorLength

MAX_PARAMETRIC_JOBS = 20


class JobManagerHandlerMixin:
    """RequestHandler implementation of the JobManager"""

    @classmethod
    def initializeHandler(cls, serviceInfoDict):
        """Initialization of DB objects and OptimizationMind"""
        try:
            result = ObjectLoader().loadObject("WorkloadManagementSystem.DB.JobDB", "JobDB")
            if not result["OK"]:
                return result
            cls.jobDB = result["Value"](parentLogger=cls.log)

            result = ObjectLoader().loadObject("WorkloadManagementSystem.DB.JobLoggingDB", "JobLoggingDB")
            if not result["OK"]:
                return result
            cls.jobLoggingDB = result["Value"](parentLogger=cls.log)

            result = ObjectLoader().loadObject("WorkloadManagementSystem.DB.TaskQueueDB", "TaskQueueDB")
            if not result["OK"]:
                return result
            cls.taskQueueDB = result["Value"](parentLogger=cls.log)

            result = ObjectLoader().loadObject("WorkloadManagementSystem.DB.PilotAgentsDB", "PilotAgentsDB")
            if not result["OK"]:
                return result
            cls.pilotAgentsDB = result["Value"](parentLogger=cls.log)

        except RuntimeError as excp:
            return S_ERROR(f"Can't connect to DB: {excp!r}")

        cls.pilotsLoggingDB = None
        enablePilotsLogging = Operations().getValue("/Services/JobMonitoring/usePilotsLoggingFlag", False)
        if enablePilotsLogging:
            try:
                result = ObjectLoader().loadObject("WorkloadManagementSystem.DB.PilotsLoggingDB", "PilotsLoggingDB")
                if not result["OK"]:
                    return result
                cls.pilotsLoggingDB = result["Value"](parentLogger=cls.log)
            except RuntimeError as excp:
                return S_ERROR(f"Can't connect to DB: {excp!r}")

        cls.msgClient = MessageClient("WorkloadManagement/OptimizationMind")
        result = cls.msgClient.connect(JobManager=True)
        if not result["OK"]:
            cls.log.warn("Cannot connect to OptimizationMind!", result["Message"])
        return S_OK()

    def initializeRequest(self):
        credDict = self.getRemoteCredentials()
        self.ownerDN = credDict["DN"]
        self.ownerGroup = credDict["group"]
        self.userProperties = credDict["properties"]
        self.owner = credDict["username"]
        self.peerUsesLimitedProxy = credDict["isLimitedProxy"]
        self.maxParametricJobs = self.srv_getCSOption("MaxParametricJobs", MAX_PARAMETRIC_JOBS)
        self.jobPolicy = JobPolicy(self.ownerDN, self.ownerGroup, self.userProperties)
        self.jobPolicy.jobDB = self.jobDB
        return S_OK()

    def __sendJobsToOptimizationMind(self, jids):
        if not self.msgClient.connected:
            result = self.msgClient.connect(JobManager=True)
            if not result["OK"]:
                self.log.warn("Cannot connect to OptimizationMind!", result["Message"])
                return

        result = self.msgClient.createMessage("OptimizeJobs")
        if not result["OK"]:
            self.log.error("Cannot create Optimize message", result["Message"])
            return
        msgObj = result["Value"]
        msgObj.jids = list(sorted(jids))
        result = self.msgClient.sendMessage(msgObj)
        if not result["OK"]:
            self.log.error("Cannot send Optimize message", result["Message"])
            return
        self.log.info("Optimize msg sent", f"for {len(jids)} jobs")

    ###########################################################################
    types_getMaxParametricJobs = []

    def export_getMaxParametricJobs(self):
        """Get the maximum number of parametric jobs

        :return: S_OK()/S_ERROR()
        """
        return S_OK(self.maxParametricJobs)

    types_submitJob = [str]

    def export_submitJob(self, jobDesc):
        """Submit a job to DIRAC WMS.
        The job can be a single job, or a parametric job.
        If it is a parametric job, then the parameters will need to be unpacked.

        :param str jobDesc: job description JDL (of a single or parametric job)
        :return: S_OK/S_ERROR, a list of newly created job IDs in case of S_OK.
        """

        if self.peerUsesLimitedProxy:
            return S_ERROR(EWMSSUBM, "Can't submit using a limited proxy")

        # Check job submission permission
        result = self.jobPolicy.getJobPolicy()
        if not result["OK"]:
            return S_ERROR(EWMSSUBM, "Failed to get job policies")
        policyDict = result["Value"]
        if not policyDict[RIGHT_SUBMIT]:
            return S_ERROR(EWMSSUBM, "Job submission not authorized")

        # jobDesc is JDL for now
        jobDesc = jobDesc.strip()
        if jobDesc[0] != "[":
            jobDesc = f"[{jobDesc}"
        if jobDesc[-1] != "]":
            jobDesc = f"{jobDesc}]"

        # Check if the job is a parametric one
        jobClassAd = ClassAd(jobDesc)
        result = getParameterVectorLength(jobClassAd)
        if not result["OK"]:
            self.log.error("Issue with getParameterVectorLength", result["Message"])
            return result
        nJobs = result["Value"]
        parametricJob = False
        if nJobs is not None and nJobs > 0:
            # if we are here, then jobDesc was the description of a parametric job. So we start unpacking
            parametricJob = True
            if nJobs > self.maxParametricJobs:
                self.log.error(
                    "Maximum of parametric jobs exceeded:",
                    "limit %d smaller than number of jobs %d" % (self.maxParametricJobs, nJobs),
                )
                return S_ERROR(EWMSJDL, "Number of parametric jobs exceeds the limit of %d" % self.maxParametricJobs)
            result = generateParametricJobs(jobClassAd)
            if not result["OK"]:
                return result
            jobDescList = result["Value"]
        else:
            # if we are here, then jobDesc was the description of a single job.
            jobDescList = [jobDesc]

        jobIDList = []
        statusList = []
        minorStatusList = []
        timeStampList = []

        if parametricJob:
            initialStatus = JobStatus.SUBMITTING
            initialMinorStatus = "Bulk transaction confirmation"
        else:
            initialStatus = JobStatus.RECEIVED
            initialMinorStatus = "Job accepted"

        for jobDescription in jobDescList:  # jobDescList because there might be a list generated by a parametric job
            result = self.jobDB.insertNewJobIntoDB(
                jobDescription,
                self.owner,
                self.ownerDN,
                self.ownerGroup,
                self.diracSetup,
                initialStatus=initialStatus,
                initialMinorStatus=initialMinorStatus,
            )
            if not result["OK"]:
                return result

            jobID = result["JobID"]
            self.log.info(f"Job added to the JobDB", f"{jobID} for {self.ownerDN}/{self.ownerGroup}")

            jobIDList.append(jobID)
            statusList.append(result["Status"])
            minorStatusList.append(result["MinorStatus"])
            timeStampList.append(result["TimeStamp"])

        # insert records in logging DB

        # For parametric jobs I can insert logging records in a bulk
        if parametricJob and len(set(jobIDList)) == len(jobIDList):
            result = self.jobLoggingDB.addLoggingRecord(
                jobIDList, statusList, minorStatusList, date=timeStampList, source="JobManager"
            )
        else:
            for jobID, status, minorStatus, timeStamp in zip(jobIDList, statusList, minorStatusList, timeStampList):
                result = self.jobLoggingDB.addLoggingRecord(
                    jobID, status, minorStatus, date=timeStamp, source="JobManager"
                )

        # Set persistency flag
        retVal = gProxyManager.getUserPersistence(self.ownerDN, self.ownerGroup)
        if "Value" not in retVal or not retVal["Value"]:
            gProxyManager.setPersistency(self.ownerDN, self.ownerGroup, True)

        if parametricJob:
            result = S_OK(jobIDList)
        else:
            result = S_OK(jobIDList[0])

        result["JobID"] = result["Value"]
        result["requireProxyUpload"] = self.__checkIfProxyUploadIsRequired()
        # Ensure non-parametric jobs (i.e. non-bulk) get sent to optimizer immediately
        if not parametricJob:
            self.__sendJobsToOptimizationMind(jobIDList)
        return result

    ###########################################################################
    types_confirmBulkSubmission = [list]

    def export_confirmBulkSubmission(self, jobIDs):
        """Confirm the possibility to proceed with processing of the jobs specified
        by the jobIDList

        :param list jobIDs: list of job IDs

        :return: S_OK(list)/S_ERROR() -- confirmed job IDs
        """
        jobList = self.__getJobList(jobIDs)
        if not jobList:
            self.log.error("Issue with __getJobList", f": invalid job specification {str(jobIDs)}")
            return S_ERROR(EWMSSUBM, "Invalid job specification: " + str(jobIDs))

        validJobList, _invalidJobList, _nonauthJobList, _ownerJobList = self.jobPolicy.evaluateJobRights(
            jobList, RIGHT_SUBMIT
        )

        # Check that all the requested jobs are eligible
        if set(jobList) != set(validJobList):
            return S_ERROR(EWMSSUBM, "Requested jobs for bulk transaction are not valid")

        result = self.jobDB.getJobsAttributes(jobList, ["Status", "MinorStatus"])
        if not result["OK"]:
            return S_ERROR(EWMSSUBM, "Requested jobs for bulk transaction are not valid")
        js_dict = strToIntDict(result["Value"])

        # Check if the jobs are already activated
        jobEnabledList = [
            jobID
            for jobID in jobList
            if js_dict[jobID]["Status"]
            in [JobStatus.RECEIVED, JobStatus.CHECKING, JobStatus.WAITING, JobStatus.MATCHED, JobStatus.RUNNING]
        ]
        if set(jobEnabledList) == set(jobList):
            return S_OK(jobList)

        # Check that requested job are in Submitting status
        jobUpdateStatusList = list(jobID for jobID in jobList if js_dict[jobID]["Status"] == JobStatus.SUBMITTING)
        if set(jobUpdateStatusList) != set(jobList):
            return S_ERROR(EWMSSUBM, "Requested jobs for bulk transaction are not valid")

        # Update status of all the requested jobs in one transaction
        result = self.jobDB.setJobAttributes(
            jobUpdateStatusList, ["Status", "MinorStatus"], [JobStatus.RECEIVED, "Job accepted"]
        )

        if not result["OK"]:
            return result

        self.__sendJobsToOptimizationMind(jobUpdateStatusList)
        return S_OK(jobUpdateStatusList)

    ###########################################################################
    def __checkIfProxyUploadIsRequired(self):
        """Check if an upload is required

        :return: bool
        """
        result = gProxyManager.userHasProxy(self.ownerDN, self.ownerGroup, validSeconds=18000)
        if not result["OK"]:
            self.log.error("Can't check if the user has proxy uploaded", result["Message"])
            return True
        # Check if an upload is required
        return not result["Value"]

    ###########################################################################

    @staticmethod
    def __getJobList(jobInput):
        """Evaluate the jobInput into a list of ints

        :param jobInput: one or more job IDs in int or str form
        :type jobInput: str or int or list
        :return : a list of int job IDs
        """

        if not jobInput:
            return []

        if isinstance(jobInput, int):
            return [jobInput]
        if isinstance(jobInput, str):
            try:
                ijob = int(jobInput)
                return [ijob]
            except ValueError:
                return []
        if isinstance(jobInput, list):
            try:
                ljob = [int(x) for x in jobInput]
                return ljob
            except ValueError:
                return []

        return []

    ###########################################################################
    types_rescheduleJob = []

    def export_rescheduleJob(self, jobIDs):
        """Reschedule a single job. If the optional proxy parameter is given
        it will be used to refresh the proxy in the Proxy Repository

        :param list jobIDs: list of job IDs

        :return: S_OK()/S_ERROR() -- confirmed job IDs
        """

        jobList = self.__getJobList(jobIDs)
        if not jobList:
            return S_ERROR("Invalid job specification: " + str(jobIDs))

        validJobList, invalidJobList, nonauthJobList, ownerJobList = self.jobPolicy.evaluateJobRights(
            jobList, RIGHT_RESCHEDULE
        )
        for jobID in validJobList:
            self.taskQueueDB.deleteJob(jobID)
            result = self.jobDB.rescheduleJob(jobID)
            self.log.debug(str(result))
            if not result["OK"]:
                return result
            self.jobLoggingDB.addLoggingRecord(
                result["JobID"],
                status=result["Status"],
                minorStatus=result["MinorStatus"],
                applicationStatus="Unknown",
                source="JobManager",
            )

        if invalidJobList or nonauthJobList:
            result = S_ERROR("Some jobs failed reschedule")
            if invalidJobList:
                result["InvalidJobIDs"] = invalidJobList
            if nonauthJobList:
                result["NonauthorizedJobIDs"] = nonauthJobList
            return result

        result = S_OK(validJobList)
        result["requireProxyUpload"] = len(ownerJobList) > 0 and self.__checkIfProxyUploadIsRequired()
        self.__sendJobsToOptimizationMind(validJobList)
        return result

    types_removeJob = []

    def export_removeJob(self, jobIDs):
        """
        Completely remove a list of jobs, also from TaskQueueDB,
        and including its JobLogging info.
        Only authorized users are allowed to remove jobs.

        :param list jobIDs: list of job IDs
        :return: S_OK()/S_ERROR() -- confirmed job IDs
        """

        jobList = self.__getJobList(jobIDs)
        if not jobList:
            return S_ERROR("Invalid job specification: " + str(jobIDs))

        validJobList, invalidJobList, nonauthJobList, _ = self.jobPolicy.evaluateJobRights(jobList, RIGHT_DELETE)
        count = 0
        error_count = 0

        if validJobList:
            self.log.verbose("Removing jobs", f"(n={len(validJobList)})")
            if not (result := self.jobDB.removeJobFromDB(validJobList))["OK"]:
                self.log.error("Failed to remove jobs from JobDB", f"(n={len(validJobList)})")
            else:
                self.log.info("Removed jobs from JobDB", f"(n={len(validJobList)})")

            for jobID in validJobList:
                resultTQ = self.taskQueueDB.deleteJob(jobID)
                if not resultTQ["OK"]:
                    self.log.warn("Failed to remove job from TaskQueueDB", "(%d): %s" % (jobID, resultTQ["Message"]))
                    error_count += 1
                else:
                    count += 1

            if not (result := self.jobLoggingDB.deleteJob(validJobList))["OK"]:
                self.log.error("Failed to remove jobs from JobLoggingDB", f"(n={len(validJobList)})")
            else:
                self.log.info("Removed jobs from JobLoggingDB", f"(n={len(validJobList)})")

            if count > 0 or error_count > 0:
                self.log.info("Removed jobs from DB", "(%d jobs with %d errors)" % (count, error_count))

        if invalidJobList or nonauthJobList:
            self.log.error(
                "Jobs can not be removed",
                f": {len(invalidJobList)} invalid and {len(nonauthJobList)} in nonauthJobList",
            )
            errMsg = "Some jobs failed removal"
            res = S_ERROR()
            if invalidJobList:
                self.log.debug(f"Invalid jobs: {','.join(str(ij) for ij in invalidJobList)}")
                res["InvalidJobIDs"] = invalidJobList
                errMsg += ": invalid jobs"
            if nonauthJobList:
                self.log.debug(f"nonauthJobList jobs: {','.join(str(nj) for nj in nonauthJobList)}")
                res["NonauthorizedJobIDs"] = nonauthJobList
                errMsg += ": non-authorized jobs"
            res["Message"] = errMsg
            return res

        return S_OK(validJobList)

    def __deleteJob(self, jobID, force=False):
        """Set the job status to "Deleted"
        and remove the pilot that ran and its logging info if the pilot is finished.

        :param int jobID: job ID
        :return: S_OK()/S_ERROR()
        """
        result = self.jobDB.setJobStatus(jobID, JobStatus.DELETED, "Checking accounting", force=force)
        if not result["OK"]:
            return result

        result = self.taskQueueDB.deleteJob(jobID)
        if not result["OK"]:
            self.log.warn("Failed to delete job from the TaskQueue")

        # if it was the last job for the pilot, clear PilotsLogging about it
        result = self.pilotAgentsDB.getPilotsForJobID(jobID)
        if not result["OK"]:
            self.log.error("Failed to get Pilots for JobID", result["Message"])
            return result
        for pilot in result["Value"]:
            res = self.pilotAgentsDB.getJobsForPilot(pilot)
            if not res["OK"]:
                self.log.error("Failed to get jobs for pilot", res["Message"])
                return res
            if not res["Value"]:  # if list of jobs for pilot is empty, delete pilot and pilotslogging
                result = self.pilotAgentsDB.getPilotInfo(pilotID=pilot)
                if not result["OK"]:
                    self.log.error("Failed to get pilot info", result["Message"])
                    return result
                pilotRef = result[0]["PilotJobReference"]
                ret = self.pilotAgentsDB.deletePilot(pilot)
                if not ret["OK"]:
                    self.log.error("Failed to delete pilot from PilotAgentsDB", ret["Message"])
                    return ret
                if self.pilotsLoggingDB:
                    ret = self.pilotsLoggingDB.deletePilotsLogging(pilotRef)
                    if not ret["OK"]:
                        self.log.error("Failed to delete pilot logging from PilotAgentsDB", ret["Message"])
                        return ret

        return S_OK()

    def __killJob(self, jobID, sendKillCommand=True, force=False):
        """Kill one job

        :param int jobID: job ID
        :param bool sendKillCommand: send kill command

        :return: S_OK()/S_ERROR()
        """
        if sendKillCommand:
            if not (result := self.jobDB.setJobCommand(jobID, "Kill"))["OK"]:
                return result

        self.log.info("Job marked for termination", jobID)
        if not (result := self.jobDB.setJobStatus(jobID, JobStatus.KILLED, "Marked for termination", force=force))[
            "OK"
        ]:
            self.log.warn("Failed to set job Killed status", result["Message"])
        if not (result := self.taskQueueDB.deleteJob(jobID))["OK"]:
            self.log.warn("Failed to delete job from the TaskQueue", result["Message"])

        return S_OK()

    def _kill_delete_jobs(self, jobIDList, right, force=False):
        """Kill (== set the status to "KILLED") or delete (== set the status to "DELETED") jobs as necessary

        :param list jobIDList: job IDs
        :param str right: RIGHT_KILL or RIGHT_DELETE

        :return: S_OK()/S_ERROR()
        """
        jobList = self.__getJobList(jobIDList)
        if not jobList:
            self.log.warn("No jobs specified")
            return S_OK([])

        validJobList, invalidJobList, nonauthJobList, ownerJobList = self.jobPolicy.evaluateJobRights(jobList, right)

        badIDs = []

        killJobList = []
        deleteJobList = []
        if validJobList:
            # Get the jobs allowed to transition to the Killed state
            filterRes = filterJobStateTransition(validJobList, JobStatus.KILLED)
            if not filterRes["OK"]:
                return filterRes
            killJobList.extend(filterRes["Value"])

            if not right == RIGHT_KILL:
                # Get the jobs allowed to transition to the Deleted state
                filterRes = filterJobStateTransition(validJobList, JobStatus.DELETED)
                if not filterRes["OK"]:
                    return filterRes
                deleteJobList.extend(filterRes["Value"])

            # Look for jobs that are in the Staging state to send kill signal to the stager
            result = self.jobDB.getJobsAttributes(killJobList, ["Status"])
            if not result["OK"]:
                return result
            stagingJobList = [jobID for jobID, sDict in result["Value"].items() if sDict["Status"] == JobStatus.STAGING]

            for jobID in killJobList:
                result = self.__killJob(jobID, force=force)
                if not result["OK"]:
                    badIDs.append(jobID)

            for jobID in deleteJobList:
                result = self.__deleteJob(jobID, force=force)
                if not result["OK"]:
                    badIDs.append(jobID)

            if stagingJobList:
                stagerClient = StorageManagerClient()
                self.log.info("Going to send killing signal to stager as well!")
                result = stagerClient.killTasksBySourceTaskID(stagingJobList)
                if not result["OK"]:
                    self.log.warn("Failed to kill some Stager tasks", result["Message"])

        if nonauthJobList or badIDs:
            result = S_ERROR("Some jobs failed deletion")
            if nonauthJobList:
                self.log.warn("Non-authorized JobIDs won't be deleted", str(nonauthJobList))
                result["NonauthorizedJobIDs"] = nonauthJobList
            if badIDs:
                self.log.warn("JobIDs failed to be deleted", str(badIDs))
                result["FailedJobIDs"] = badIDs
            return result

        jobsList = killJobList if right == RIGHT_KILL else deleteJobList
        result = S_OK(jobsList)
        result["requireProxyUpload"] = len(ownerJobList) > 0 and self.__checkIfProxyUploadIsRequired()

        if invalidJobList:
            result["InvalidJobIDs"] = invalidJobList

        return result

    ###########################################################################
    types_deleteJob = []

    def export_deleteJob(self, jobIDs, force=False):
        """Delete jobs specified in the jobIDs list

        :param list jobIDs: list of job IDs

        :return: S_OK/S_ERROR
        """

        return self._kill_delete_jobs(jobIDs, RIGHT_DELETE, force=force)

    ###########################################################################
    types_killJob = []

    def export_killJob(self, jobIDs, force=False):
        """Kill jobs specified in the jobIDs list

        :param list jobIDs: list of job IDs

        :return: S_OK/S_ERROR
        """

        return self._kill_delete_jobs(jobIDs, RIGHT_KILL, force=force)

    ###########################################################################
    types_resetJob = []

    def export_resetJob(self, jobIDs):
        """Reset jobs specified in the jobIDs list

        :param list jobIDs: list of job IDs

        :return: S_OK/S_ERROR
        """

        jobList = self.__getJobList(jobIDs)
        if not jobList:
            return S_ERROR("Invalid job specification: " + str(jobIDs))

        validJobList, invalidJobList, nonauthJobList, ownerJobList = self.jobPolicy.evaluateJobRights(
            jobList, RIGHT_RESET
        )

        badIDs = []
        good_ids = []
        for jobID in validJobList:
            result = self.jobDB.setJobAttribute(jobID, "RescheduleCounter", -1)
            if not result["OK"]:
                badIDs.append(jobID)
            else:
                self.taskQueueDB.deleteJob(jobID)
                # gJobDB.deleteJobFromQueue(jobID)
                result = self.jobDB.rescheduleJob(jobID)
                if not result["OK"]:
                    badIDs.append(jobID)
                else:
                    good_ids.append(jobID)
                self.jobLoggingDB.addLoggingRecord(
                    result["JobID"],
                    status=result["Status"],
                    minorStatus=result["MinorStatus"],
                    applicationStatus="Unknown",
                    source="JobManager",
                )

        self.__sendJobsToOptimizationMind(good_ids)
        if invalidJobList or nonauthJobList or badIDs:
            result = S_ERROR("Some jobs failed resetting")
            if invalidJobList:
                result["InvalidJobIDs"] = invalidJobList
            if nonauthJobList:
                result["NonauthorizedJobIDs"] = nonauthJobList
            if badIDs:
                result["FailedJobIDs"] = badIDs
            return result

        result = S_OK()
        result["requireProxyUpload"] = len(ownerJobList) > 0 and self.__checkIfProxyUploadIsRequired()
        return result


class JobManagerHandler(JobManagerHandlerMixin, RequestHandler):
    def initialize(self):
        self.diracSetup = self.serviceInfoDict["clientSetup"]
        return self.initializeRequest()
