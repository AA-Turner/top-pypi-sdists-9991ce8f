import asyncio

import pytest

from ddtrace.constants import ERROR_MSG


@pytest.mark.asyncio
def test_trace_coroutine(test_spans):
    # it should use the task context when invoked in a coroutine
    with test_spans.tracer.start_span("coroutine"):
        pass

    traces = test_spans.pop_traces()

    assert len(traces) == 1
    assert len(traces[0]) == 1
    assert traces[0][0].name == "coroutine"


@pytest.mark.asyncio
async def test_trace_multiple_coroutines(ot_tracer, test_spans):
    # if multiple coroutines have nested tracing, they must belong
    # to the same trace

    async def coro():
        # another traced coroutine
        with ot_tracer.start_active_span("coroutine_2"):
            return 42

    with ot_tracer.start_active_span("coroutine_1"):
        value = await coro()

    # the coroutine has been called correctly
    assert value == 42
    # a single trace has been properly reported
    traces = test_spans.pop_traces()
    assert len(traces) == 1
    assert len(traces[0]) == 2
    assert traces[0][0].name == "coroutine_1"
    assert traces[0][1].name == "coroutine_2"
    # the parenting is correct
    assert traces[0][0] == traces[0][1]._parent
    assert traces[0][0].trace_id == traces[0][1].trace_id


@pytest.mark.asyncio
async def test_exception(ot_tracer, test_spans):
    async def f1():
        with ot_tracer.start_span("f1"):
            raise Exception("f1 error")

    with pytest.raises(Exception, match="f1 error"):
        await f1()

    traces = test_spans.pop_traces()
    assert len(traces) == 1
    spans = traces[0]
    assert len(spans) == 1
    span = spans[0]
    assert span.error == 1
    assert span.get_tag(ERROR_MSG) == "f1 error"
    assert "Exception: f1 error" in span.get_tag("error.stack")


@pytest.mark.asyncio
async def test_trace_multiple_calls(ot_tracer, test_spans):
    # create multiple futures so that we expect multiple
    # traces instead of a single one (helper not used)
    async def coro():
        # another traced coroutine
        with ot_tracer.start_span("coroutine"):
            await asyncio.sleep(0.01)

    futures = [asyncio.ensure_future(coro()) for x in range(10)]
    for future in futures:
        await future

    traces = test_spans.pop_traces()

    assert len(traces) == 10
    assert len(traces[0]) == 1
    assert traces[0][0].name == "coroutine"


@pytest.mark.asyncio
async def test_trace_multiple_coroutines_ot_dd(ot_tracer):
    """
    Ensure we can trace from opentracer to ddtracer across asyncio
    context switches.
    """

    # if multiple coroutines have nested tracing, they must belong
    # to the same trace
    async def coro():
        # another traced coroutine
        with ot_tracer._dd_tracer.trace("coroutine_2"):
            return 42

    with ot_tracer.start_active_span("coroutine_1"):
        value = await coro()

    # the coroutine has been called correctly
    assert value == 42
    # a single trace has been properly reported
    traces = ot_tracer._dd_tracer.pop_traces()
    assert len(traces) == 1
    assert len(traces[0]) == 2
    assert traces[0][0].name == "coroutine_1"
    assert traces[0][1].name == "coroutine_2"
    # the parenting is correct
    assert traces[0][0] == traces[0][1]._parent
    assert traces[0][0].trace_id == traces[0][1].trace_id


@pytest.mark.asyncio
async def test_trace_multiple_coroutines_dd_ot(ot_tracer):
    """
    Ensure we can trace from ddtracer to opentracer across asyncio
    context switches.
    """

    # if multiple coroutines have nested tracing, they must belong
    # to the same trace
    async def coro():
        # another traced coroutine
        with ot_tracer.start_span("coroutine_2"):
            return 42

    with ot_tracer._dd_tracer.trace("coroutine_1"):
        value = await coro()

    # the coroutine has been called correctly
    assert value == 42
    # a single trace has been properly reported
    traces = ot_tracer._dd_tracer.pop_traces()
    assert len(traces) == 1
    assert len(traces[0]) == 2
    assert traces[0][0].name == "coroutine_1"
    assert traces[0][1].name == "coroutine_2"
    # the parenting is correct
    assert traces[0][0] == traces[0][1]._parent
    assert traces[0][0].trace_id == traces[0][1].trace_id
