from collections import defaultdict
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import cast

from ddtrace.debugging._probe.model import Probe
from ddtrace.debugging._probe.model import ProbeLocationMixin
from ddtrace.debugging._probe.status import ProbeStatusLogger
from ddtrace.internal import forksafe
from ddtrace.internal.logger import get_logger


logger = get_logger(__name__)


class ProbeRegistryEntry(object):
    __slots__ = (
        "probe",
        "installed",
        "emitting",
        "error_type",
        "message",
    )

    def __init__(self, probe: Probe) -> None:
        self.probe = probe
        self.installed = False
        self.emitting = False
        self.error_type: Optional[str] = None
        self.message: Optional[str] = None

    def set_installed(self) -> None:
        self.installed = True

    def set_emitting(self) -> None:
        self.emitting = True

    def set_error(self, error_type: str, message: str) -> None:
        self.error_type = error_type
        self.message = message

    def update(self, probe: Probe) -> None:
        self.probe.update(probe)


def _get_probe_location(probe: Probe) -> Optional[str]:
    if isinstance(probe, ProbeLocationMixin):
        return probe.location()[0]
    else:
        raise ValueError("Unsupported probe type: {}".format(type(probe)))


class ProbeRegistry(dict):
    """Keep track of all the registered probes.

    New probes are also registered as pending, on a location basis, until they
    are processed (e.g. installed, generally by some import hook). Pending
    probes can be retrieved with the ``get_pending`` method.
    """

    def __init__(self, status_logger: ProbeStatusLogger, *args: Any, **kwargs: Any) -> None:
        """Initialize the probe registry."""
        super().__init__(*args, **kwargs)
        self.logger = status_logger

        # Used to keep track of probes pending installation
        self._pending: Dict[str, List[Probe]] = defaultdict(list)

        self._lock = forksafe.RLock()

    def register(self, *probes: Probe) -> None:
        """Register a probe."""
        with self._lock:
            for probe in probes:
                if probe in self:
                    # Already registered.
                    continue

                self[probe.probe_id] = ProbeRegistryEntry(probe)

                location = _get_probe_location(probe)
                if location is None:
                    self.set_error(
                        probe,
                        "UnresolvedLocation",
                        "Unable to resolve location information for probe {}".format(probe.probe_id),
                    )
                    continue

                self._pending[location].append(probe)

                self.logger.received(probe)

    def update(self, probe):
        with self._lock:
            if probe not in self:
                logger.error("Attempted to update unregistered probe %s", probe.probe_id)
                return

            self[probe.probe_id].update(probe)

            self.log_probe_status(probe)

    def set_installed(self, probe: Probe) -> None:
        """Set the installed flag for a probe."""
        with self._lock:
            self[probe.probe_id].set_installed()

            # No longer pending
            self._remove_pending(probe)

            self.logger.installed(probe)

    def set_emitting(self, probe: Probe) -> None:
        """Set the emitting flag for a probe."""
        with self._lock:
            try:
                entry = cast(ProbeRegistryEntry, self[probe.probe_id])
            except KeyError:
                # The probe has likely been removed by remote config but the
                # instrumentation has raced that thread from another thread.
                # Since we can't get an entry from the registry for it we don't
                # log the emitting state.
                logger.debug("Probe %s no longer registered emitted data", probe.probe_id)
                return

            if not entry.emitting:
                entry.set_emitting()
                self.logger.emitting(probe)

    def set_error(self, probe: Probe, error_type: str, message: str) -> None:
        """Set the error message for a probe."""
        with self._lock:
            self[probe.probe_id].set_error(error_type, message)
            self.logger.error(probe, (error_type, message))

    def _log_probe_status_unlocked(self, entry: ProbeRegistryEntry) -> None:
        if entry.emitting:
            self.logger.emitting(entry.probe)
        elif entry.installed:
            self.logger.installed(entry.probe)
        elif entry.error_type:
            assert entry.message is not None, entry  # nosec
            self.logger.error(entry.probe, error=(entry.error_type, entry.message))
        else:
            self.logger.received(entry.probe)

    def log_probe_status(self, probe: Probe) -> None:
        """Log the status of a probe using the status logger."""
        with self._lock:
            self._log_probe_status_unlocked(self[probe.probe_id])

    def log_probes_status(self) -> None:
        """Log the status of all the probes using the status logger."""
        with self._lock:
            for entry in self.values():
                self._log_probe_status_unlocked(entry)

    def _remove_pending(self, probe: Probe) -> None:
        if (location := _get_probe_location(probe)) is None:
            # If the probe has no location information, then it cannot be
            # pending.
            return

        pending_probes = self._pending[location]
        try:
            # DEV: Note that this is O(n), which is fine with a conservative
            # number of probes.
            pending_probes.remove(probe)
        except ValueError:
            # The probe wasn't pending
            pass
        if not pending_probes:
            del self._pending[location]

    def has_probes(self, location: str) -> bool:
        for entry in self.values():
            if _get_probe_location(entry.probe) == location:
                return True
        return False

    def unregister(self, *probes: Probe) -> List[Probe]:
        """Unregister a collection of probes.

        This also ensures that any pending probes are removed if they haven't
        been processed yet.
        """
        unregistered_probes = []
        with self._lock:
            for probe in probes:
                try:
                    entry = self.pop(probe.probe_id)
                except KeyError:
                    # We don't seem to have the probe
                    logger.warning("Tried to unregister unregistered probe %s", probe.probe_id)
                else:
                    probe = entry.probe
                    self._remove_pending(probe)
                    unregistered_probes.append(probe)
        return unregistered_probes

    def get_pending(self, location: str) -> List[Probe]:
        """Get the currently pending probes by location."""
        return self._pending[location]

    def __contains__(self, probe: object) -> bool:
        """Check if a probe is in the registry."""
        assert isinstance(probe, Probe), probe  # nosec

        with self._lock:
            return super().__contains__(probe.probe_id)
