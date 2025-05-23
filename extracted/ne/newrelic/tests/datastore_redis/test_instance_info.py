# Copyright 2010 New Relic, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import redis

from newrelic.common.package_version_utils import get_package_version_tuple
from newrelic.hooks.datastore_redis import _conn_attrs_to_dict, _instance_info

REDIS_PY_VERSION = get_package_version_tuple("redis")

# Call to `get_connection` function with the usage of the command
# name as an input argument has been deprecated since v5.3.0.
_select_command_as_arg = [
    (pytest.param(None, marks=pytest.mark.skipif(REDIS_PY_VERSION < (5, 3), reason="Deprecated after v5.3"))),
    (pytest.param("SELECT", marks=pytest.mark.skipif(REDIS_PY_VERSION >= (5, 3), reason="Needed until v5.3"))),
]

_instance_info_tests = [
    ((), {}, ("localhost", "6379", "0")),
    ((), {"host": None}, ("localhost", "6379", "0")),
    ((), {"host": ""}, ("localhost", "6379", "0")),
    ((), {"db": None}, ("localhost", "6379", "0")),
    ((), {"db": ""}, ("localhost", "6379", "0")),
    ((), {"host": "127.0.0.1", "port": 1234, "db": 2}, ("127.0.0.1", "1234", "2")),
    (("127.0.0.1", 1234, 2), {}, ("127.0.0.1", "1234", "2")),
]


class DisabledConnection(redis.Connection):
    @staticmethod
    def connect(*args, **kwargs):
        pass


class DisabledUnixConnection(redis.UnixDomainSocketConnection, DisabledConnection):
    pass


class DisabledSSLConnection(redis.SSLConnection, DisabledConnection):
    pass


@pytest.mark.parametrize("args,kwargs,expected", _instance_info_tests)
def test_redis_client_instance_info(args, kwargs, expected):
    r = redis.Redis(*args, **kwargs)
    conn_kwargs = r.connection_pool.connection_kwargs
    assert _instance_info(conn_kwargs) == expected


@pytest.mark.parametrize("args,kwargs,expected", _instance_info_tests)
def test_strict_redis_client_instance_info(args, kwargs, expected):
    r = redis.StrictRedis(*args, **kwargs)
    conn_kwargs = r.connection_pool.connection_kwargs
    assert _instance_info(conn_kwargs) == expected


@pytest.mark.parametrize("args,kwargs,expected", _instance_info_tests)
def test_redis_connection_instance_info(args, kwargs, expected):
    r = redis.Redis(*args, **kwargs)
    r.connection_pool.connection_class = DisabledConnection
    connection = r.connection_pool.get_connection("SELECT")
    try:
        conn_kwargs = _conn_attrs_to_dict(connection)
        assert _instance_info(conn_kwargs) == expected
    finally:
        r.connection_pool.release(connection)


@pytest.mark.parametrize("command_name", _select_command_as_arg)
@pytest.mark.parametrize("args,kwargs,expected", _instance_info_tests)
def test_strict_redis_connection_instance_info(args, kwargs, expected, command_name):
    r = redis.StrictRedis(*args, **kwargs)
    r.connection_pool.connection_class = DisabledConnection
    connection = r.connection_pool.get_connection(command_name)
    try:
        conn_kwargs = _conn_attrs_to_dict(connection)
        assert _instance_info(conn_kwargs) == expected
    finally:
        r.connection_pool.release(connection)


_instance_info_from_url_tests = [
    (("redis://localhost:1234/",), {}, ("localhost", "1234", "0")),
    (("redis://localhost:1234",), {}, ("localhost", "1234", "0")),
    (("redis://user:password@localhost:6379",), {}, ("localhost", "6379", "0")),
    (("redis://localhost:6379/2",), {}, ("localhost", "6379", "2")),
    (("redis://localhost:6379",), {"db": 2}, ("localhost", "6379", "2")),
    (("redis://@127.0.0.1:6379",), {}, ("127.0.0.1", "6379", "0")),
    (("redis://:1234/",), {}, ("localhost", "1234", "0")),
    (("redis://@:1234/",), {}, ("localhost", "1234", "0")),
    (("redis://localhost:1234/garbage",), {}, ("localhost", "1234", "0")),
    (("redis://localhost:6379/2/",), {}, ("localhost", "6379", "2")),
    (("redis://localhost:6379",), {"host": "someotherhost"}, ("localhost", "6379", "0")),
    (("redis://localhost:6379/2",), {"db": 3}, ("localhost", "6379", "2")),
    (("redis://localhost:6379/2/?db=111",), {}, ("localhost", "6379", "111")),
    (("redis://localhost:6379?db=2",), {}, ("localhost", "6379", "2")),
    (("redis://localhost:6379/2?db=111",), {}, ("localhost", "6379", "111")),
    (("unix:///path/to/socket.sock",), {}, ("localhost", "/path/to/socket.sock", "0")),
    (("unix:///path/to/socket.sock?db=2",), {}, ("localhost", "/path/to/socket.sock", "2")),
    (("unix:///path/to/socket.sock",), {"db": 2}, ("localhost", "/path/to/socket.sock", "2")),
]


@pytest.mark.parametrize("args,kwargs,expected", _instance_info_from_url_tests)
def test_redis_client_from_url(args, kwargs, expected):
    r = redis.Redis.from_url(*args, **kwargs)
    conn_kwargs = r.connection_pool.connection_kwargs
    assert _instance_info(conn_kwargs) == expected


@pytest.mark.parametrize("args,kwargs,expected", _instance_info_from_url_tests)
def test_strict_redis_client_from_url(args, kwargs, expected):
    r = redis.StrictRedis.from_url(*args, **kwargs)
    conn_kwargs = r.connection_pool.connection_kwargs
    assert _instance_info(conn_kwargs) == expected


@pytest.mark.parametrize("command_name", _select_command_as_arg)
@pytest.mark.parametrize("args,kwargs,expected", _instance_info_from_url_tests)
def test_redis_connection_from_url(args, kwargs, expected, command_name):
    r = redis.Redis.from_url(*args, **kwargs)
    if r.connection_pool.connection_class is redis.Connection:
        r.connection_pool.connection_class = DisabledConnection
    elif r.connection_pool.connection_class is redis.UnixDomainSocketConnection:
        r.connection_pool.connection_class = DisabledUnixConnection
    elif r.connection_pool.connection_class is redis.SSLConnection:
        r.connection_pool.connection_class = DisabledSSLConnection
    else:
        raise AssertionError(r.connection_pool.connection_class)
    connection = r.connection_pool.get_connection(command_name)
    try:
        conn_kwargs = _conn_attrs_to_dict(connection)
        assert _instance_info(conn_kwargs) == expected
    finally:
        r.connection_pool.release(connection)


@pytest.mark.parametrize("command_name", _select_command_as_arg)
@pytest.mark.parametrize("args,kwargs,expected", _instance_info_from_url_tests)
def test_strict_redis_connection_from_url(args, kwargs, expected, command_name):
    r = redis.StrictRedis.from_url(*args, **kwargs)
    if r.connection_pool.connection_class is redis.Connection:
        r.connection_pool.connection_class = DisabledConnection
    elif r.connection_pool.connection_class is redis.UnixDomainSocketConnection:
        r.connection_pool.connection_class = DisabledUnixConnection
    elif r.connection_pool.connection_class is redis.SSLConnection:
        r.connection_pool.connection_class = DisabledSSLConnection
    else:
        raise AssertionError(r.connection_pool.connection_class)
    connection = r.connection_pool.get_connection(command_name)
    try:
        conn_kwargs = _conn_attrs_to_dict(connection)
        assert _instance_info(conn_kwargs) == expected
    finally:
        r.connection_pool.release(connection)
