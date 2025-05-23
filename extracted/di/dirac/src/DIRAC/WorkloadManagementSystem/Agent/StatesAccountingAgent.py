"""  StatesAccountingAgent sends periodically numbers of jobs and pilots in various states for various
     sites to the Monitoring system to create historical plots.

.. literalinclude:: ../ConfigTemplate.cfg
  :start-after: ##BEGIN StatesAccountingAgent
  :end-before: ##END
  :dedent: 2
  :caption: StatesAccountingAgent options
"""
import datetime

from DIRAC import S_ERROR, S_OK
from DIRAC.AccountingSystem.Client.DataStoreClient import DataStoreClient
from DIRAC.AccountingSystem.Client.Types.WMSHistory import WMSHistory
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.Core.Utilities import TimeUtilities
from DIRAC.MonitoringSystem.Client.MonitoringReporter import MonitoringReporter
from DIRAC.WorkloadManagementSystem.DB.JobDB import JobDB
from DIRAC.WorkloadManagementSystem.DB.PilotAgentsDB import PilotAgentsDB


class StatesAccountingAgent(AgentModule):
    """Agent that every 15 minutes will report
    to the AccountingDB (MySQL) or the Monitoring DB (ElasticSearch), or both,
    a snapshot of the JobDB.
    Also sends a snapshot of PilotAgentsDB to Monitoring.
    """

    # WMSHistory fields
    __summaryKeyFieldsMapping = [
        "Status",
        "Site",
        "User",
        "UserGroup",
        "JobGroup",
        "JobType",
        "ApplicationStatus",
        "MinorStatus",
    ]
    __summaryDefinedFields = [("ApplicationStatus", "unset"), ("MinorStatus", "unset")]
    __summaryValueFieldsMapping = ["Jobs", "Reschedules"]
    __renameFieldsMapping = {"JobType": "JobSplitType"}

    # PilotsHistory fields
    __pilotsMapping = ["TaskQueueID", "GridSite", "GridType", "Status", "NumOfPilots"]

    def initialize(self):
        """Standard initialization"""
        # This agent will always loop every 15 minutes
        self.am_setOption("PollingTime", 900)

        # Check whether to send to Monitoring or Accounting or both
        self.jobMonitoringOption = Operations().getMonitoringBackends(monitoringType="WMSHistory")
        self.pilotMonitoringOption = Operations().getMonitoringBackends(monitoringType="PilotsHistory")
        messageQueue = self.am_getOption("MessageQueue", "dirac.wmshistory")
        self.datastores = {}  # For storing the clients to Accounting and Monitoring

        if "Accounting" in self.jobMonitoringOption:
            self.datastores["Accounting"] = DataStoreClient(retryGraceTime=900)
        if "Monitoring" in self.jobMonitoringOption:
            self.datastores["Monitoring"] = MonitoringReporter(
                monitoringType="WMSHistory", failoverQueueName=messageQueue
            )
        if "Monitoring" in self.pilotMonitoringOption:
            self.pilotReporter = MonitoringReporter(monitoringType="PilotsHistory", failoverQueueName=messageQueue)

        self.__jobDBFields = []
        for field in self.__summaryKeyFieldsMapping:
            if field == "User":
                field = "Owner"
            elif field == "UserGroup":
                field = "OwnerGroup"
            self.__jobDBFields.append(field)
        return S_OK()

    def execute(self):
        """Main execution method"""

        # on the first iteration of the agent, do nothing in order to avoid double committing after a restart
        if self.am_getModuleParam("cyclesDone") == 0:
            self.log.notice("Skipping the first iteration of the agent")
            return S_OK()

        # PilotsHistory to Monitoring
        if "Monitoring" in self.pilotMonitoringOption:
            self.log.info("Committing PilotsHistory to Monitoring")

            # TODO: remove this comment from v9.0
            self.log.notice("Notice: 'TaskQueueID' will be removed from the pilotAgentsDB in v9.0.")

            result = PilotAgentsDB().getSummarySnapshot()
            now = datetime.datetime.utcnow()
            if not result["OK"]:
                self.log.error(
                    "Can't get the PilotAgentsDB summary",
                    f"{result['Message']}: won't commit PilotsHistory at this cycle",
                )

            values = result["Value"][1]
            for record in values:
                rD = {}
                for iP, _ in enumerate(self.__pilotsMapping):
                    rD[self.__pilotsMapping[iP]] = record[iP]
                rD["timestamp"] = int(TimeUtilities.toEpochMilliSeconds(now))
                self.pilotReporter.addRecord(rD)

            self.log.info("Committing to Monitoring...")
            result = self.pilotReporter.commit()
            if not result["OK"]:
                self.log.error("Could not commit to Monitoring", result["Message"])
            self.log.verbose("Done committing PilotsHistory to Monitoring")

        # WMSHistory to Monitoring or Accounting
        self.log.info(f"Committing WMSHistory to {'and '.join(self.jobMonitoringOption)} backend")
        result = JobDB().getSummarySnapshot(self.__jobDBFields)
        now = datetime.datetime.utcnow()
        if not result["OK"]:
            self.log.error("Can't get the JobDB summary", f"{result['Message']}: won't commit WMSHistory at this cycle")
            return S_ERROR()

        values = result["Value"][1]

        self.log.info("Start sending WMSHistory records")
        for record in values:
            record = record[1:]
            rD = {}
            for fV in self.__summaryDefinedFields:
                rD[fV[0]] = fV[1]
            for iP, _ in enumerate(self.__summaryKeyFieldsMapping):
                fieldName = self.__summaryKeyFieldsMapping[iP]
                rD[self.__renameFieldsMapping.get(fieldName, fieldName)] = record[iP]
            record = record[len(self.__summaryKeyFieldsMapping) :]
            for iP, _ in enumerate(self.__summaryValueFieldsMapping):
                rD[self.__summaryValueFieldsMapping[iP]] = int(record[iP])

            for backend in self.datastores:
                if backend.lower() == "monitoring":
                    rD["timestamp"] = int(TimeUtilities.toEpochMilliSeconds(now))
                    self.datastores["Monitoring"].addRecord(rD)

                elif backend.lower() == "accounting":
                    acWMS = WMSHistory()
                    acWMS.setStartTime(now)
                    acWMS.setEndTime(now)
                    acWMS.setValuesFromDict(rD)
                    retVal = acWMS.checkValues()
                    if not retVal["OK"]:
                        self.log.error("Invalid WMSHistory accounting record ", f"{retVal['Message']} -> {rD}")
                    else:
                        self.datastores["Accounting"].addRegister(acWMS)

        for backend, datastore in self.datastores.items():
            self.log.info(f"Committing WMSHistory records to {backend} backend")
            result = datastore.commit()
            if not result["OK"]:
                self.log.error(f"Couldn't commit WMSHistory to {backend}", result["Message"])
                return S_ERROR()
            self.log.verbose(f"Done committing WMSHistory to {backend} backend")

        return S_OK()
