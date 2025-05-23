import functools
import math
import operator
import string
import sys
from typing import Any

import hypothesis
import hypothesis.stateful
import hypothesis.strategies as st
import pytest
import redis
from hypothesis.stateful import rule, initialize, precondition
from hypothesis.strategies import SearchStrategy

import fakeredis
from ._server_info import redis_ver, floats_kwargs, server_type

self_strategy = st.runner()


@st.composite
def sample_attr(draw, name):
    """Strategy for sampling a specific attribute from a state machine"""
    machine = draw(self_strategy)
    values = getattr(machine, name)
    position = draw(st.integers(min_value=0, max_value=len(values) - 1))
    return values[position]


keys = sample_attr("keys")
fields = sample_attr("fields")
values = sample_attr("values")
scores = sample_attr("scores")

eng_text = st.builds(lambda x: x.encode(), st.text(alphabet=string.ascii_letters, min_size=1))
ints = st.integers(min_value=-2_147_483_648, max_value=2_147_483_647)
int_as_bytes = st.builds(lambda x: str(default_normalize(x)).encode(), ints)
floats = st.floats(width=32, **floats_kwargs)
float_as_bytes = st.builds(lambda x: repr(default_normalize(x)).encode(), floats)
counts = st.integers(min_value=-3, max_value=3) | ints
# Redis has an integer overflow bug in swapdb, so we confine the numbers to
# a limited range (https://github.com/antirez/redis/issues/5737).
dbnums = st.integers(min_value=0, max_value=3) | st.integers(min_value=-1000, max_value=1000)
# The filter is to work around https://github.com/antirez/redis/issues/5632
patterns = st.text(alphabet=st.sampled_from("[]^$*.?-azAZ\\\r\n\t")) | st.binary().filter(lambda x: b"\0" not in x)
string_tests = st.sampled_from([b"+", b"-"]) | st.builds(operator.add, st.sampled_from([b"(", b"["]), fields)
# Redis has integer overflow bugs in time computations, which is why we set a maximum.
expires_seconds = st.integers(min_value=5, max_value=1_000)
expires_ms = st.integers(min_value=5_000, max_value=50_000)


class WrappedException:
    """Wraps an exception for comparison."""

    def __init__(self, exc):
        self.wrapped = exc

    def __str__(self):
        return str(self.wrapped)

    def __repr__(self):
        return "WrappedException({!r})".format(self.wrapped)

    def __eq__(self, other):
        if not isinstance(other, WrappedException):
            return NotImplemented
        if type(self.wrapped) != type(other.wrapped):  # noqa: E721
            return False
        return True
        # return self.wrapped.args == other.wrapped.args

    def __ne__(self, other):
        if not isinstance(other, WrappedException):
            return NotImplemented
        return not self == other


def wrap_exceptions(obj):
    if isinstance(obj, list):
        return [wrap_exceptions(item) for item in obj]
    elif isinstance(obj, Exception):
        return WrappedException(obj)
    else:
        return obj


def sort_list(lst):
    if isinstance(lst, list):
        return sorted(lst)
    else:
        return lst


def normalize_if_number(x):
    if isinstance(x, list):
        return [normalize_if_number(item) for item in x]
    try:
        res = float(x)
        return x if math.isnan(res) else res
    except ValueError:
        return x


def flatten(args):
    if isinstance(args, (list, tuple)):
        for arg in args:
            yield from flatten(arg)
    elif args is not None:
        yield args


def default_normalize(x: Any) -> Any:
    if redis_ver >= (7,) and (isinstance(x, float) or isinstance(x, int)):
        return 0 + x

    return x


def optional(arg: Any) -> st.SearchStrategy:
    return st.none() | st.just(arg)


def zero_or_more(*args: Any):
    return [optional(arg) for arg in args]


class Command:
    def __init__(self, *args):
        args = list(flatten(args))
        args = [default_normalize(x) for x in args]
        self.args = tuple(args)

    def __repr__(self):
        parts = [repr(arg) for arg in self.args]
        return "Command({})".format(", ".join(parts))

    @staticmethod
    def encode(arg):
        encoder = redis.connection.Encoder("utf-8", "replace", False)
        return encoder.encode(arg)

    @property
    def normalize(self):
        command = self.encode(self.args[0]).lower() if self.args else None
        # Functions that return a list in arbitrary order
        unordered = {
            b"keys",
            b"sort",
            b"hgetall",
            b"hkeys",
            b"hvals",
            b"sdiff",
            b"sinter",
            b"sunion",
            b"smembers",
            b"hexpire",
        }
        if command in unordered:
            return sort_list
        else:
            return normalize_if_number

    @property
    def testable(self):
        """Whether this command is suitable for a test.

        The fuzzer can create commands with behaviour that is
        non-deterministic, not supported, or which hits redis bugs.
        """
        N = len(self.args)
        if N == 0:
            return False
        command = self.encode(self.args[0]).lower()
        if not command.split():
            return False
        if command == b"keys" and N == 2 and self.args[1] != b"*":
            return False
        # Redis will ignore a NULL character in some commands but not others,
        # e.g., it recognizes EXEC\0 but not MULTI\00.
        # Rather than try to reproduce this quirky behavior, just skip these tests.
        if b"\0" in command:
            return False
        return True


def commands(*args, **kwargs):
    return st.builds(functools.partial(Command, **kwargs), *args)


# # TODO: all expiry-related commands
common_commands = (
    commands(st.sampled_from(["del", "persist", "type", "unlink"]), keys)
    | commands(st.just("exists"), st.lists(keys))
    | commands(st.just("keys"), st.just("*"))
    # Disabled for now due to redis giving wrong answers
    # (https://github.com/antirez/redis/issues/5632)
    # | commands(st.just('keys'), patterns)
    | commands(st.just("move"), keys, dbnums)
    | commands(st.sampled_from(["rename", "renamenx"]), keys, keys)
    # TODO: find a better solution to sort instability than throwing
    #  away the sort entirely with normalize. This also prevents us
    #  using LIMIT.
    | commands(st.just("sort"), keys, *zero_or_more("asc", "desc", "alpha"))
)


@hypothesis.settings(max_examples=1000)
class CommonMachine(hypothesis.stateful.RuleBasedStateMachine):
    create_command_strategy = st.nothing()

    def __init__(self):
        super().__init__()
        try:
            self.real = redis.StrictRedis("localhost", port=6390, db=2)
            self.real.ping()
        except redis.ConnectionError:
            pytest.skip("redis is not running")
        if self.real.info("server").get("arch_bits") != 64:
            self.real.connection_pool.disconnect()
            pytest.skip("redis server is not 64-bit")
        self.fake = fakeredis.FakeStrictRedis(server=fakeredis.FakeServer(version=redis_ver), port=6390, db=2)
        # Disable the response parsing so that we can check the raw values returned
        self.fake.response_callbacks.clear()
        self.real.response_callbacks.clear()
        self.transaction_normalize = []
        self.keys = []
        self.fields = []
        self.values = []
        self.scores = []
        self.initialized_data = False
        try:
            self.real.execute_command("discard")
        except redis.ResponseError:
            pass
        self.real.flushall()

    def teardown(self):
        self.real.connection_pool.disconnect()
        self.fake.connection_pool.disconnect()
        super().teardown()

    @staticmethod
    def _evaluate(client, command):
        try:
            result = client.execute_command(*command.args)
            if result != "QUEUED":
                result = command.normalize(result)
            exc = None
        except Exception as e:
            result = exc = e
        return wrap_exceptions(result), exc

    def _compare(self, command):
        fake_result, fake_exc = self._evaluate(self.fake, command)
        real_result, real_exc = self._evaluate(self.real, command)

        if fake_exc is not None and real_exc is None:
            print(f"{fake_exc} raised on only on fake when running {command}", file=sys.stderr)
            raise fake_exc
        elif real_exc is not None and fake_exc is None:
            assert real_exc == fake_exc, f"Expected exception `{real_exc}` not raised when running {command}"
        elif real_exc is None and isinstance(real_result, list) and command.args and command.args[0].lower() == "exec":
            assert fake_result is not None
            # Transactions need to use the normalize functions of the
            # component commands.
            assert len(self.transaction_normalize) == len(real_result)
            assert len(self.transaction_normalize) == len(fake_result)
            for n, r, f in zip(self.transaction_normalize, real_result, fake_result):
                assert n(f) == n(r)
            self.transaction_normalize = []
        elif isinstance(fake_result, list):
            assert len(fake_result) == len(real_result), (
                f"Discrepancy when running command {command}, fake({fake_result}) != real({real_result})",
            )
            for i in range(len(fake_result)):
                assert fake_result[i] == real_result[i] or (
                    type(fake_result[i]) is float and fake_result[i] == pytest.approx(real_result[i])
                ), f"Discrepancy when running command {command}, fake({fake_result}) != real({real_result})"

        else:
            assert fake_result == real_result or (
                type(fake_result) is float and fake_result == pytest.approx(real_result)
            ), f"Discrepancy when running command {command}, fake({fake_result}) != real({real_result})"
            if real_result == b"QUEUED":
                # Since redis removes the distinction between simple strings and
                # bulk strings, this might not actually indicate that we're in a
                # transaction. But it is extremely unlikely that hypothesis will
                # find such examples.
                self.transaction_normalize.append(command.normalize)
        if len(command.args) == 1 and Command.encode(command.args[0]).lower() in (b"discard", b"exec"):
            self.transaction_normalize = []

    @initialize(
        attrs=st.fixed_dictionaries(
            dict(
                keys=st.lists(eng_text, min_size=2, max_size=5, unique=True),
                fields=st.lists(eng_text, min_size=2, max_size=5, unique=True),
                values=st.lists(eng_text | int_as_bytes | float_as_bytes, min_size=2, max_size=5, unique=True),
                scores=st.lists(floats, min_size=2, max_size=5, unique=True),
            )
        )
    )
    def init_attrs(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)

    # hypothesis doesn't allow ordering of @initialize, so we have to put
    # preconditions on rules to ensure we call init_data exactly once and
    # after init_attrs.
    @precondition(lambda self: not self.initialized_data)
    @rule(commands=self_strategy.flatmap(lambda self: st.lists(self.create_command_strategy)))
    def init_data(self, commands):
        for command in commands:
            self._compare(command)
        self.initialized_data = True

    @precondition(lambda self: self.initialized_data)
    @rule(command=self_strategy.flatmap(lambda self: self.command_strategy))
    def one_command(self, command):
        self._compare(command)


class BaseTest:
    """Base class for test classes."""

    command_strategy: SearchStrategy
    create_command_strategy = st.nothing()
    command_strategy_redis7 = st.nothing()
    command_strategy_redis_only = st.nothing()

    @pytest.mark.slow
    def test(self):
        class Machine(CommonMachine):
            create_command_strategy = self.create_command_strategy
            command_strategy = self.command_strategy
            if server_type == "redis":
                command_strategy = command_strategy | self.command_strategy_redis_only
            if server_type == "redis" and redis_ver >= (7,):
                command_strategy = command_strategy | self.command_strategy_redis7

        # hypothesis.settings.register_profile("debug", max_examples=10, verbosity=hypothesis.Verbosity.debug)
        # hypothesis.settings.load_profile("debug")
        hypothesis.stateful.run_state_machine_as_test(Machine)
