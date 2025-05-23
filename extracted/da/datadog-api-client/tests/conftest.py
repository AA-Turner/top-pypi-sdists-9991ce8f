# coding=utf-8
"""Define basic fixtures."""

import os
import hashlib

RECORD = os.getenv("RECORD", "false").lower()
SLEEP_AFTER_REQUEST = int(os.getenv("SLEEP_AFTER_REQUEST", "0"))

# First patch urllib
tracer = None
try:
    from ddtrace import patch, tracer

    patch(urllib3=True)

    from pytest import hookimpl

    @hookimpl(hookwrapper=True)
    def pytest_terminal_summary(terminalreporter, exitstatus, config):
        yield  # do normal output

        ci_pipeline_id = os.getenv("GITHUB_RUN_ID", None)
        dd_service = os.getenv("DD_SERVICE", None)
        if ci_pipeline_id and dd_service:
            terminalreporter.ensure_newline()
            terminalreporter.section("test reports", purple=True, bold=True)
            terminalreporter.line(
                "* View test APM traces and detailed time reports on Datadog (can take a few minutes to become available):"
            )
            terminalreporter.line(
                "* https://app.datadoghq.com/ci/test-runs?query="
                "%40test.service%3A{}%20%40ci.pipeline.id%3A{}&index=citest".format(dd_service, ci_pipeline_id)
            )

except ImportError:
    if os.getenv("CI", "false") == "true" and RECORD == "none":
        raise

import importlib
import functools
import json
import logging
import pathlib
import re
import time
import warnings
from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta
from jinja2 import Template, Environment, meta
from pytest_bdd import given, parsers, then, when

from datadog_api_client import exceptions
from datadog_api_client.api_client import ApiClient
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import OpenApiModel, file_type, data_to_dict

logging.basicConfig()

with (pathlib.Path(__file__).parent.parent / ".generator" / "src" / "generator" / "replacement.json").open() as f:
    EDGE_CASES = json.load(f)

PATTERN_ALPHANUM = re.compile(r"[^A-Za-z0-9]+")
PATTERN_DOUBLE_UNDERSCORE = re.compile(r"__+")
PATTERN_LEADING_ALPHA = re.compile(r"(.)([A-Z][a-z]+)")
PATTERN_FOLLOWING_ALPHA = re.compile(r"([a-z0-9])([A-Z])")
PATTERN_WHITESPACE = re.compile(r"\W")
PATTERN_INDEX = re.compile(r"\[([0-9]*)\]")


def sleep_after_request(f):
    """Sleep after each request."""
    if RECORD == "false" or SLEEP_AFTER_REQUEST <= 0:
        return f

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        time.sleep(SLEEP_AFTER_REQUEST)
        return result

    return wrapper


def escape_reserved_keyword(word):
    """Escape reserved language keywords like openapi generator does it.

    :param word: Word to escape
    :return: The escaped word if it was a reserved keyword, the word unchanged otherwise
    """
    reserved_keywords = ["from"]
    if word in reserved_keywords:
        return f"_{word}"
    return word


def pytest_bdd_after_scenario(request, feature, scenario):
    try:
        ctx = request.getfixturevalue("context")
    except Exception:
        return
    for undo in reversed(ctx["undo_operations"]):
        undo()


def pytest_bdd_apply_tag(tag, function):
    """Register tags as custom markers and skip test for '@skip' ones."""
    skip_tags = {"skip", "skip-python"}
    if RECORD != "none":
        # ignore integration-only scenarios if the recording is enabled
        skip_tags.add("integration-only")
    if RECORD != "false":
        skip_tags.add("replay-only")

    if tag in skip_tags:
        marker = pytest.mark.skip(reason=f"skipped because of '{tag} in {skip_tags}")
        marker(function)
    return True


def snake_case(value):
    for token, replacement in EDGE_CASES.items():
        value = value.replace(token, replacement)
    s1 = PATTERN_LEADING_ALPHA.sub(r"\1_\2", value)
    s1 = PATTERN_FOLLOWING_ALPHA.sub(r"\1_\2", s1).lower()
    s1 = PATTERN_WHITESPACE.sub("_", s1)
    s1 = s1.rstrip("_")
    return PATTERN_DOUBLE_UNDERSCORE.sub("_", s1)


def glom(value, path):
    from glom import glom as g

    # replace foo[index].bar by foo.index.bar
    path = PATTERN_INDEX.sub(r".\1", path)
    if not isinstance(value, dict):
        path = ".".join(snake_case(p) for p in path.split("."))

    # Support top level array indexing
    path = re.sub(r"^[.]+", "", path)

    return g(value, path) if path else value


def _get_prefix(request):
    test_class = request.cls
    if test_class:
        main = "{}.{}".format(test_class.__name__, request.node.name)
    else:
        base_name = request.node.__scenario_report__.scenario.name
        main = PATTERN_ALPHANUM.sub("_", base_name)[:100]
    prefix = "Test-Python" if _disable_recording() else "Test"
    return f"{prefix}-{main}"


@pytest.fixture
def unique(request, freezed_time):
    prefix = _get_prefix(request)
    return f"{prefix}-{int(freezed_time.timestamp())}"


def relative_time(freezed_time, iso, is_iso_with_timezone_indicator):
    time_re = re.compile(r"now( *([+-]) *(\d+)([smhdMy]))?")

    def func(arg):
        ret = freezed_time
        m = time_re.match(arg)
        if m:
            if m.group(1):
                sign = m.group(2)
                num = int(sign + m.group(3))
                unit = m.group(4)
                if unit == "s":
                    ret += relativedelta(seconds=num)
                elif unit == "m":
                    ret += relativedelta(minutes=num)
                elif unit == "h":
                    ret += relativedelta(hours=num)
                elif unit == "d":
                    ret += relativedelta(days=num)
                elif unit == "M":
                    ret += relativedelta(months=num)
                elif unit == "y":
                    ret += relativedelta(years=num)
            if iso:
                if is_iso_with_timezone_indicator:
                    # Return ISO 8601 formatted string with Z timezone indicator
                    # Example: 2025-04-17T03:17:07.923Z
                    from datetime import timezone

                    return ret.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
                else:
                    return ret.replace(tzinfo=None)  # return datetime object and not string
                    # NOTE this is not a full ISO 8601 format, but it's enough for our needs
                    # return ret.strftime('%Y-%m-%dT%H:%M:%S') + ret.strftime('.%f')[:4] + 'Z'

            return int(ret.timestamp())
        return ""

    return func


def generate_uuid(freezed_time):
    freezed_time_string = str(freezed_time.timestamp())
    return freezed_time_string[:8] + "-0000-0000-0000-" + freezed_time_string[:10] + "00"


@pytest.fixture
def context(vcr, unique, freezed_time):
    """
    Return a mapping with all defined fixtures, all objects created by `given` steps,
    and the undo operations to perform after a test scenario.
    """
    unique_hash = hashlib.sha256(unique.encode("utf-8")).hexdigest()[:16]

    # Dirty fix as on_call cassette and API use the `Z` format instead of `+00:00`
    is_iso_with_timezone_indicator = "on_call" in unique

    ctx = {
        "undo_operations": [],
        "unique": unique,
        "unique_lower": unique.lower(),
        "unique_upper": unique.upper(),
        "unique_alnum": PATTERN_ALPHANUM.sub("", unique),
        "unique_lower_alnum": PATTERN_ALPHANUM.sub("", unique).lower(),
        "unique_upper_alnum": PATTERN_ALPHANUM.sub("", unique).upper(),
        "unique_hash": unique_hash,
        "timestamp": relative_time(freezed_time, False, False),
        "timeISO": relative_time(freezed_time, True, is_iso_with_timezone_indicator),
        "uuid": generate_uuid(freezed_time),
    }

    yield ctx


@pytest.fixture(scope="session")
def record_mode(request):
    """Manage compatibility with DD client libraries."""
    return {"false": "none", "true": "rewrite", "none": "new_episodes"}[RECORD]


def _disable_recording():
    """Disable VCR.py integration."""
    return RECORD == "none"


@pytest.fixture(scope="session")
def disable_recording(request):
    """Disable VCR.py integration. This overrides a pytest-recording fixture."""
    return _disable_recording()


@pytest.fixture
def vcr_config():
    config = dict(
        filter_headers=(
            "DD-API-KEY",
            "DD-APPLICATION-KEY",
            "User-Agent",
            "Accept-Encoding",
        ),
        match_on=[
            "method",
            "scheme",
            "host",
            "port",
            "path",
            "query",
            "body",
            "headers",
        ],
    )
    if tracer:
        from urllib.parse import urlparse

        if hasattr(tracer._writer, "agent_url"):
            config["ignore_hosts"] = [urlparse(tracer._writer.agent_url).hostname]
        else:
            config["ignore_hosts"] = [urlparse(tracer._writer.intake_url).hostname]

    return config


@pytest.fixture
def default_cassette_name(default_cassette_name):
    return PATTERN_DOUBLE_UNDERSCORE.sub("_", default_cassette_name)


@pytest.fixture
def freezed_time(default_cassette_name, record_mode, vcr):
    from dateutil import parser

    if record_mode in {"new_episodes", "rewrite"}:
        tzinfo = datetime.now().astimezone().tzinfo
        freeze_at = datetime.now().replace(tzinfo=tzinfo).isoformat()
        if record_mode == "rewrite":
            pathlib.Path(vcr._path).parent.mkdir(parents=True, exist_ok=True)
            with pathlib.Path(vcr._path).with_suffix(".frozen").open("w+") as f:
                f.write(freeze_at)
    else:
        freeze_file = pathlib.Path(vcr._path).with_suffix(".frozen")
        if not freeze_file.exists():
            msg = (
                "Time file '{}' not found: create one setting `RECORD=true` or " "ignore it using `RECORD=none`".format(
                    freeze_file
                )
            )
            raise RuntimeError(msg)
        with freeze_file.open("r") as f:
            freeze_at = f.readline().strip()

        if not pathlib.Path(vcr._path).exists():
            msg = (
                "Cassette '{}' not found: create one setting `RECORD=true` or " "ignore it using `RECORD=none`".format(
                    vcr._path
                )
            )
            raise RuntimeError(msg)

    return parser.isoparse(freeze_at)


def pytest_recording_configure(config, vcr):
    from vcr import matchers
    from vcr.util import read_body

    is_text_json = matchers._header_checker("text/json")
    transformer = matchers._transform_json

    def body(r1, r2):
        if is_text_json(r1.headers) and is_text_json(r2.headers):
            assert transformer(read_body(r1)) == transformer(read_body(r2))
        else:
            matchers.body(r1, r2)

    vcr.matchers["body"] = body


@given('a valid "apiKeyAuth" key in the system')
def a_valid_api_key(configuration):
    """a valid API key."""
    configuration.api_key["apiKeyAuth"] = os.getenv("DD_TEST_CLIENT_API_KEY", "fake")


@given('a valid "appKeyAuth" key in the system')
def a_valid_application_key(configuration):
    """a valid Application key."""
    configuration.api_key["appKeyAuth"] = os.getenv("DD_TEST_CLIENT_APP_KEY", "fake")


@pytest.fixture(scope="module")
def package_name(api_version):
    return "datadog_api_client." + api_version


@pytest.fixture(scope="module")
def undo_operations():
    result = {}
    for f in pathlib.Path(os.path.dirname(__file__)).rglob("undo.json"):
        version = f.parent.parent.name
        with f.open() as fp:
            data = json.load(fp)
            result[version] = {}
            for operation_id, settings in data.items():
                undo_settings = settings.get("undo")
                undo_settings["base_tag"] = settings.get("tag")
                result[version][snake_case(operation_id)] = undo_settings

    return result


def build_configuration():
    c = Configuration(return_http_data_only=False, spec_property_naming=True)
    c.connection_pool_maxsize = 0
    c.debug = debug = os.getenv("DEBUG") in {"true", "1", "yes", "on"}
    c.enable_retry = True
    if debug:  # enable vcr logs for DEBUG=true
        vcr_log = logging.getLogger("vcr")
        vcr_log.setLevel(logging.INFO)
    if "DD_TEST_SITE" in os.environ:
        c.server_index = 2
        c.server_variables["site"] = os.environ["DD_TEST_SITE"]
    return c


@pytest.fixture
def configuration():
    return build_configuration()


@pytest.fixture
def client(configuration):
    with ApiClient(configuration) as api_client:
        yield api_client


def _api_name(value):
    value = re.sub(r"[^a-zA-Z0-9]", "", value)
    return value + "Api"


@given(parsers.parse('an instance of "{name}" API'))
def api(context, package_name, client, name):
    """Return an API instance."""
    module_name = snake_case(name)
    package = importlib.import_module(f"{package_name}.api.{module_name}_api")
    context["api"] = {
        "api": getattr(package, _api_name(name))(client),
        "package": package_name,
        "calls": [],
    }


@given(parsers.parse('operation "{name}" enabled'))
def operation_enabled(client, name):
    """Enable the unstable operation specific in the clause."""
    client.configuration.unstable_operations[snake_case(name)] = True


@given(parsers.parse('new "{name}" request'))
def api_request(configuration, context, name):
    """Call an endpoint."""
    api = context["api"]
    context["api_request"] = {
        "api": api["api"],
        "request": getattr(api["api"], snake_case(name)),
        "args": [],
        "kwargs": {},
        "response": (None, None, None),
    }


@given(parsers.parse("body with value {data}"))
def request_body(context, data):
    """Set request body."""
    tpl = Template(data).render(**context)
    context["api_request"]["kwargs"]["body"] = tpl


@given(parsers.parse('body from file "{path}"'))
def request_body_from_file(context, path, package_name):
    """Set request body."""
    version = package_name.split(".")[-1]
    with open(os.path.join(os.path.dirname(__file__), version, "features", path)) as f:
        data = f.read()
    tpl = Template(data).render(**context)
    context["api_request"]["kwargs"]["body"] = tpl


@given(parsers.parse('request contains "{name}" parameter from "{path}"'))
def request_parameter(context, name, path):
    """Set request parameter."""
    context["api_request"]["kwargs"][escape_reserved_keyword(snake_case(name))] = json.dumps(glom(context, path))


@given(parsers.parse('request contains "{name}" parameter with value {value}'))
def request_parameter_with_value(context, name, value):
    """Set request parameter."""
    tpl = Template(value).render(**context)
    context["api_request"]["kwargs"][escape_reserved_keyword(snake_case(name))] = tpl


def assert_no_unparsed(data):
    if isinstance(data, list):
        for item in data:
            assert_no_unparsed(item)
    elif isinstance(data, dict):
        for item in data.values():
            assert_no_unparsed(item)
    elif isinstance(data, OpenApiModel):
        assert not data._unparsed
        for attr in data._data_store.values():
            assert_no_unparsed(attr)


def build_given(version, operation):
    @sleep_after_request
    def wrapper(context, undo):
        name = operation["tag"].replace(" ", "")
        module_name = snake_case(operation["tag"])
        operation_name = snake_case(operation["operationId"])
        package_name = f"datadog_api_client.{version}"

        # make sure we have a fresh instance of API client and configuration
        configuration = build_configuration()
        configuration.api_key["apiKeyAuth"] = os.getenv("DD_TEST_CLIENT_API_KEY", "fake")
        configuration.api_key["appKeyAuth"] = os.getenv("DD_TEST_CLIENT_APP_KEY", "fake")
        configuration.check_input_type = False
        configuration.return_http_data_only = True

        # enable unstable operation
        if operation_name in configuration.unstable_operations:
            configuration.unstable_operations[operation_name] = True

        package = importlib.import_module(f"{package_name}.api.{module_name}_api")
        with ApiClient(configuration) as client:
            api = getattr(package, _api_name(name))(client)
            operation_method = getattr(api, operation_name)
            params_map = getattr(api, f"_{operation_name}_endpoint").params_map

            # perform operation
            def build_param(p):
                openapi_types = params_map[p["name"]]["openapi_types"]
                if "value" in p:
                    if openapi_types == (file_type,):
                        filepath = os.path.join(
                            os.path.dirname(__file__),
                            version,
                            "features",
                            json.loads(Template(p["value"]).render(**context)),
                        )
                        return open(filepath)
                    return json.loads(Template(p["value"]).render(**context))
                if "source" in p:
                    return glom(context, p["source"])

            kwargs = {
                escape_reserved_keyword(snake_case(p["name"])): build_param(p) for p in operation.get("parameters", [])
            }
            result = operation_method(**kwargs)
            request_body = kwargs.get("body", "")

            # register undo method
            def undo_operation():
                return undo(api, version, operation_name, result, request_body, client=client)

            if tracer:
                undo_operation = tracer.wrap(name="undo", resource=operation["step"])(undo_operation)

            context["undo_operations"].append(undo_operation)

            # optional re-shaping
            if "source" in operation:
                result = glom(result, operation["source"])

            # store response in fixtures
            result_body_json = data_to_dict(result)
            context[operation["key"]] = result_body_json

    return wrapper


for f in pathlib.Path(os.path.dirname(__file__)).rglob("given.json"):
    version = f.parent.parent.name
    with f.open() as fp:
        for settings in json.load(fp):
            given(settings["step"])(build_given(version, settings))


def extract_parameters(kwargs, data, parameter):
    if "source" in parameter:
        kwargs[parameter["name"]] = glom(data, parameter["source"])
    elif "template" in parameter:
        variables = meta.find_undeclared_variables(Environment().parse(parameter["template"]))
        ctx = {}
        for var in variables:
            ctx[var] = glom(data, var)
        kwargs[parameter["name"]] = json.loads(Template(parameter["template"]).render(**ctx))


@pytest.fixture
def undo(package_name, undo_operations, client):
    """Clean after operation."""

    def cleanup(api, version, operation_id, response, request, client=client):
        operation = undo_operations.get(version, {}).get(operation_id)
        if operation_id is None:
            raise NotImplementedError((version, operation_id))

        if operation["type"] is None:
            raise NotImplementedError((version, operation_id))

        if operation["type"] != "unsafe":
            return

        # If Undo tag is not the same as the the operation tag.
        # For example, Service Accounts use the DisableUser operation to undo, which is part of Users.
        if "tag" in operation and operation["base_tag"] != operation["tag"]:
            undo_tag = operation["tag"]
            undo_name = undo_tag.replace(" ", "")
            undo_module_name = snake_case(undo_tag)
            undo_package = importlib.import_module(f"{package_name}.api.{undo_module_name}_api")
            api = getattr(undo_package, _api_name(undo_name))(client)

        operation_name = snake_case(operation["operationId"])
        method = getattr(api, operation_name)
        kwargs = {}
        parameters = operation.get("parameters", [])
        for parameter in parameters:
            if "origin" not in parameter or parameter["origin"] == "response":
                extract_parameters(kwargs, response, parameter)
            elif parameter["origin"] == "request":
                extract_parameters(kwargs, request, parameter)
        if operation_name in client.configuration.unstable_operations:
            client.configuration.unstable_operations[operation_name] = True

        try:
            method(**kwargs)
        except exceptions.ApiException as e:
            warnings.warn(f"failed undo: {e}")

    yield cleanup


@when("the request is sent")
def execute_request(undo, context, client, api_version, request):
    """Execute the prepared request."""
    api_request = context["api_request"]

    params_map = getattr(api_request["api"], f'_{api_request["request"].__name__}_endpoint').params_map
    for k, v in api_request["kwargs"].items():
        openapi_types = params_map[k]["openapi_types"]
        if openapi_types == (file_type,):
            filepath = os.path.join(os.path.dirname(__file__), api_version, "features", json.loads(v))
            # We let the GC collects it, this shouldn't be an issue
            api_request["kwargs"][k] = open(filepath)
        else:
            api_request["kwargs"][k] = client.deserialize(v, openapi_types, True)

    try:
        response = api_request["request"](*api_request["args"], **api_request["kwargs"])
        # Reserialise the response body to JSON to facilitate test assertions
        response_body_json = data_to_dict(response[0])
        api_request["response"] = [response_body_json, response[1], response[2]]
    except exceptions.ApiException as e:
        # If we have an exception, make a stub response object to use for assertions
        # Instead of finding the response class of the method, we use the fact that all
        # responses returned have an ordered response of body|status|headers
        api_request["response"] = [e.body, e.status, e.headers]
        return

    if "skip-validation" not in request.node.__scenario_report__.scenario.tags:
        assert_no_unparsed(response[0])

    api = api_request["api"]
    operation_id = api_request["request"].__name__
    response = api_request["response"][0]
    request_body = api_request.get("kwargs", {}).get("body", "")

    def undo_operation():
        return undo(api, api_version, operation_id, response, request_body)

    if tracer:
        undo_operation = tracer.wrap(name="undo", resource="execute request")(undo_operation)

    context["undo_operations"].append(undo_operation)


@when("the request with pagination is sent")
def execute_request_with_pagination(undo, context, client, api_version):
    """Execute the prepared paginated request."""
    api_request = context["api_request"]

    params_map = getattr(api_request["api"], f'_{api_request["request"].__name__}_endpoint').params_map
    for k, v in api_request["kwargs"].items():
        api_request["kwargs"][k] = client.deserialize(v, params_map[k]["openapi_types"], True)

    kwargs = api_request["kwargs"]
    client.configuration.return_http_data_only = True
    method = getattr(api_request["api"], f"{api_request['request'].__name__}_with_pagination")
    try:
        response = list(method(*api_request["args"], **kwargs))
        # Reserialise the response body to JSON to facilitate test assertions
        response_body_json = data_to_dict(response)
        api_request["response"] = [response_body_json, 200, None]
    except exceptions.ApiException as e:
        # If we have an exception, make a stub response object to use for assertions
        # Instead of finding the response class of the method, we use the fact that all
        # responses returned have an ordered response of body|status|headers
        api_request["response"] = [e.body, e.status, e.headers]
    finally:
        client.configuration.return_http_data_only = False


@then(parsers.parse("the response status is {status:d} {description}"))
def the_status_is(context, status, description):
    """Check the status."""
    assert status == context["api_request"]["response"][1]


@then(parsers.parse('the response "{response_path}" is equal to {value}'))
def expect_equal(context, response_path, value):
    response_value = glom(context["api_request"]["response"][0], response_path)
    test_value = json.loads(Template(value).render(**context))
    assert test_value == response_value


@then(parsers.parse('the response "{response_path}" has the same value as "{fixture_path}"'))
def expect_equal_value(context, response_path, fixture_path):
    fixture_value = glom(context, fixture_path)
    response_value = glom(context["api_request"]["response"][0], response_path)
    assert fixture_value == response_value


@then(parsers.parse('the response "{response_path}" has length {fixture_length:d}'))
def expect_equal_length(context, response_path, fixture_length):
    response_value = glom(context["api_request"]["response"][0], response_path)
    assert fixture_length == len(response_value)


@then(parsers.parse("the response has {fixture_length:d} items"))
def expect_equal_response_items(context, fixture_length):
    response = context["api_request"]["response"][0]
    assert fixture_length == len(response)


@then(parsers.parse('the response "{response_path}" is false'))
def expect_false(context, response_path):
    response_value = glom(context["api_request"]["response"][0], response_path)
    assert not response_value


@then(parsers.parse('the response "{response_path}" has field "{field}"'))
def expect_response_has_field(context, response_path, field):
    """Check that a response path has field."""
    response_value = glom(context["api_request"]["response"][0], response_path)
    assert field in response_value


@then(parsers.parse('the response "{response_path}" does not have field "{field}"'))
def expect_response_does_not_have_field(context, response_path, field):
    """Check that a response path does not have field."""
    response_value = glom(context["api_request"]["response"][0], response_path)
    assert field not in response_value


@then(parsers.parse('the response "{response_path}" has item with field "{key_path}" with value {value}'))
def expect_array_contains_object(context, response_path, key_path, value):
    from glom.core import PathAccessError

    response_value = glom(context["api_request"]["response"][0], response_path)
    test_value = json.loads(Template(value).render(**context))
    for response_item in response_value:
        try:
            response_item_value = glom(response_item, key_path)
            if response_item_value == test_value:
                return
        except PathAccessError:
            pass
    raise AssertionError(f'could not find key value pair in object array: "{key_path}": "{test_value}"')


@then(parsers.parse('the response "{response_path}" array contains value {value}'))
def expect_array_contains_object(context, response_path, value):
    response_value = glom(context["api_request"]["response"][0], response_path)
    test_value = json.loads(Template(value).render(**context))
    for response_item in response_value:
        if response_item == test_value:
            return
    raise AssertionError(f"could not find value in array: {test_value}")
