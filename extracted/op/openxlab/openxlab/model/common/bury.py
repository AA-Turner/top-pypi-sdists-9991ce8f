import sys
import time

from openxlab.model.clients.openapi_client import OpenapiClient
from openxlab.model.common.constants import endpoint
from openxlab.xlab.handler.user_token import get_token
from openxlab.model.common.thread_pool import bury_thread_pool


def bury_data_upload_task(_event_name_: str, client: OpenapiClient):
    payload = {'serviceName': 'model-center', 'eventName': _event_name_,
               'eventTimestamp': int(round(time.time() * 1000)),
               'operatorUid': get_user_id(), 'operatedObjId': _event_name_}
    try:
        client.bury_data_upload(payload)
    except ValueError:
        pass


def bury_data(event_name=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            _event_name_ = event_name
            if _event_name_ is None:
                _event_name_ = get_full_event_name(func.__name__)
            else:
                _event_name_ = get_full_event_name(_event_name_)
            client = OpenapiClient(endpoint)
            bury_thread_pool.submit_task(bury_data_upload_task, _event_name_, client)
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def get_full_event_name(method_name) -> str:
    """
    Judging whether it is the sdk calling method according to the system parameters
    """
    if len(sys.argv) > 1:
        return f"py_client_{method_name}_cli"
    else:
        return f"py_client_{method_name}_sdk"


def get_user_id() -> str:
    try:
        token = get_token()
        if token is not None:
            return token.sso_uid
        else:
            return 'anonymous'
    except ValueError:
        return 'anonymous'
