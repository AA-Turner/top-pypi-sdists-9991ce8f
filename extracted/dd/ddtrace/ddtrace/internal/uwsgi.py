from __future__ import absolute_import

from typing import Callable
from typing import Optional


class uWSGIConfigError(Exception):
    """uWSGI configuration error.

    This is raised when uwsgi configuration is incompatible with the library.
    """


class uWSGIMasterProcess(Exception):
    """The process is uWSGI master process."""


def check_uwsgi(worker_callback: Optional[Callable] = None, atexit: Optional[Callable] = None) -> None:
    """Check whetever uwsgi is running and what needs to be done.

    :param worker_callback: Callback function to call in uWSGI worker processes.
    """
    try:
        import uwsgi
    except ImportError:
        return

    if not hasattr(uwsgi, "opt"):
        msg = "Unable to access uwsgi options. Please make sure that the --import=ddtrace.auto option is set"
        raise uWSGIConfigError(msg)

    if not (uwsgi.opt.get("enable-threads") or int(uwsgi.opt.get("threads") or 0)):
        msg = "enable-threads option must be set to true, or a positive number of threads must be set"
        raise uWSGIConfigError(msg)

    # If uwsgi has more than one process, it is running in prefork operational mode: uwsgi is going to fork multiple
    # sub-processes.
    # If lazy-app is enabled, then the app is loaded in each subprocess independently. This is fine.
    # If it's not enabled, then the app will be loaded in the master process, and uwsgi will `fork()` abruptly,
    # bypassing Python sanity checks. We need to handle this case properly.
    # The proper way to handle that is to allow to register a callback function to run in the subprocess at their
    # startup, and warn the caller that this is the master process and that (probably) nothing should be done.
    if uwsgi.numproc > 1 and not uwsgi.opt.get("lazy-apps") and uwsgi.worker_id() == 0:
        if not uwsgi.opt.get("master"):
            # Having multiple workers without the master process is not supported:
            # the postfork hooks are not available, so there's no way to start a different profiler in each
            # worker
            raise uWSGIConfigError("master option must be enabled when multiple processes are used")

        # Register the function to be called in child process at startup
        if worker_callback is not None:
            try:
                import uwsgidecorators
            except ImportError:
                raise uWSGIConfigError("Running under uwsgi but uwsgidecorators cannot be imported")
            uwsgidecorators.postfork(worker_callback)

        if atexit is not None:
            original_atexit = getattr(uwsgi, "atexit", None)

            def _atexit():
                try:
                    atexit()
                except Exception:
                    pass

                if original_atexit is not None:
                    original_atexit()

            uwsgi.atexit = _atexit

        raise uWSGIMasterProcess()
