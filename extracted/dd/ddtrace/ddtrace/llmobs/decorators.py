from functools import wraps
from inspect import isasyncgenfunction
from inspect import iscoroutinefunction
from inspect import isgeneratorfunction
from inspect import signature
import sys
from typing import Callable
from typing import Optional

from ddtrace.internal.logger import get_logger
from ddtrace.llmobs import LLMObs
from ddtrace.llmobs._constants import OUTPUT_VALUE
from ddtrace.llmobs._constants import SPAN_START_WHILE_DISABLED_WARNING


log = get_logger(__name__)


def _get_llmobs_span_options(name, model_name, func):
    traced_model_name = model_name
    if traced_model_name is None:
        traced_model_name = "custom"

    span_name = name
    if span_name is None:
        span_name = func.__name__

    return traced_model_name, span_name


async def yield_from_async_gen(func, span, args, kwargs):
    try:
        gen = func(*args, **kwargs)
        next_val = await gen.asend(None)
        while True:
            try:
                i = yield next_val
                next_val = await gen.asend(i)
            except GeneratorExit:
                await gen.aclose()
                break
            except StopAsyncIteration as e:
                await gen.athrow(e)
                break
            except Exception as e:
                await gen.athrow(e)
                raise
    except (StopAsyncIteration, GeneratorExit):
        raise
    except Exception:
        span.set_exc_info(*sys.exc_info())
        raise
    finally:
        span.finish()


def _model_decorator(operation_kind):
    def decorator(
        original_func: Optional[Callable] = None,
        model_name: Optional[str] = None,
        model_provider: Optional[str] = None,
        name: Optional[str] = None,
        session_id: Optional[str] = None,
        ml_app: Optional[str] = None,
    ):
        def inner(func):
            if iscoroutinefunction(func) or isasyncgenfunction(func):

                @wraps(func)
                def generator_wrapper(*args, **kwargs):
                    if not LLMObs.enabled:
                        log.warning(SPAN_START_WHILE_DISABLED_WARNING)
                        return func(*args, **kwargs)
                    traced_model_name, span_name = _get_llmobs_span_options(name, model_name, func)
                    traced_operation = getattr(LLMObs, operation_kind, LLMObs.llm)
                    span = traced_operation(
                        model_name=traced_model_name,
                        model_provider=model_provider,
                        name=span_name,
                        session_id=session_id,
                        ml_app=ml_app,
                        _decorator=True,
                    )
                    return yield_from_async_gen(func, span, args, kwargs)

                @wraps(func)
                async def wrapper(*args, **kwargs):
                    if not LLMObs.enabled:
                        log.warning(SPAN_START_WHILE_DISABLED_WARNING)
                        return await func(*args, **kwargs)
                    traced_model_name, span_name = _get_llmobs_span_options(name, model_name, func)
                    traced_operation = getattr(LLMObs, operation_kind, LLMObs.llm)
                    with traced_operation(
                        model_name=traced_model_name,
                        model_provider=model_provider,
                        name=span_name,
                        session_id=session_id,
                        ml_app=ml_app,
                        _decorator=True,
                    ):
                        return await func(*args, **kwargs)

            else:

                @wraps(func)
                def generator_wrapper(*args, **kwargs):
                    if not LLMObs.enabled:
                        log.warning(SPAN_START_WHILE_DISABLED_WARNING)
                        yield from func(*args, **kwargs)
                    else:
                        traced_model_name, span_name = _get_llmobs_span_options(name, model_name, func)
                        traced_operation = getattr(LLMObs, operation_kind, LLMObs.llm)
                        span = traced_operation(
                            model_name=traced_model_name,
                            model_provider=model_provider,
                            name=span_name,
                            session_id=session_id,
                            ml_app=ml_app,
                            _decorator=True,
                        )
                        try:
                            yield from func(*args, **kwargs)
                        except (StopIteration, GeneratorExit):
                            raise
                        except Exception:
                            span.set_exc_info(*sys.exc_info())
                            raise
                        finally:
                            span.finish()

                @wraps(func)
                def wrapper(*args, **kwargs):
                    if not LLMObs.enabled:
                        log.warning(SPAN_START_WHILE_DISABLED_WARNING)
                        return func(*args, **kwargs)
                    traced_model_name, span_name = _get_llmobs_span_options(name, model_name, func)
                    traced_operation = getattr(LLMObs, operation_kind, LLMObs.llm)
                    with traced_operation(
                        model_name=traced_model_name,
                        model_provider=model_provider,
                        name=span_name,
                        session_id=session_id,
                        ml_app=ml_app,
                        _decorator=True,
                    ):
                        return func(*args, **kwargs)

            return generator_wrapper if (isgeneratorfunction(func) or isasyncgenfunction(func)) else wrapper

        if original_func and callable(original_func):
            return inner(original_func)
        return inner

    return decorator


def _llmobs_decorator(operation_kind):
    def decorator(
        original_func: Optional[Callable] = None,
        name: Optional[str] = None,
        session_id: Optional[str] = None,
        ml_app: Optional[str] = None,
        _automatic_io_annotation: bool = True,
    ):
        def inner(func):
            if iscoroutinefunction(func) or isasyncgenfunction(func):

                @wraps(func)
                def generator_wrapper(*args, **kwargs):
                    if not LLMObs.enabled:
                        log.warning(SPAN_START_WHILE_DISABLED_WARNING)
                        return func(*args, **kwargs)
                    _, span_name = _get_llmobs_span_options(name, None, func)
                    traced_operation = getattr(LLMObs, operation_kind, LLMObs.workflow)
                    span = traced_operation(name=span_name, session_id=session_id, ml_app=ml_app, _decorator=True)
                    func_signature = signature(func)
                    bound_args = func_signature.bind_partial(*args, **kwargs)
                    if _automatic_io_annotation and bound_args.arguments:
                        LLMObs.annotate(span=span, input_data=dict(bound_args.arguments))
                    return yield_from_async_gen(func, span, args, kwargs)

                @wraps(func)
                async def wrapper(*args, **kwargs):
                    if not LLMObs.enabled:
                        log.warning(SPAN_START_WHILE_DISABLED_WARNING)
                        return await func(*args, **kwargs)
                    _, span_name = _get_llmobs_span_options(name, None, func)
                    traced_operation = getattr(LLMObs, operation_kind, LLMObs.workflow)
                    with traced_operation(
                        name=span_name, session_id=session_id, ml_app=ml_app, _decorator=True
                    ) as span:
                        func_signature = signature(func)
                        bound_args = func_signature.bind_partial(*args, **kwargs)
                        if _automatic_io_annotation and bound_args.arguments:
                            LLMObs.annotate(span=span, input_data=dict(bound_args.arguments))
                        resp = await func(*args, **kwargs)
                        if (
                            _automatic_io_annotation
                            and resp
                            and operation_kind != "retrieval"
                            and span._get_ctx_item(OUTPUT_VALUE) is None
                        ):
                            LLMObs.annotate(span=span, output_data=resp)
                        return resp

            else:

                @wraps(func)
                def generator_wrapper(*args, **kwargs):
                    if not LLMObs.enabled:
                        log.warning(SPAN_START_WHILE_DISABLED_WARNING)
                        yield from func(*args, **kwargs)
                    else:
                        _, span_name = _get_llmobs_span_options(name, None, func)
                        traced_operation = getattr(LLMObs, operation_kind, LLMObs.workflow)
                        span = traced_operation(name=span_name, session_id=session_id, ml_app=ml_app, _decorator=True)
                        func_signature = signature(func)
                        bound_args = func_signature.bind_partial(*args, **kwargs)
                        if _automatic_io_annotation and bound_args.arguments:
                            LLMObs.annotate(span=span, input_data=dict(bound_args.arguments))
                        try:
                            yield from func(*args, **kwargs)
                        except (StopIteration, GeneratorExit):
                            raise
                        except Exception:
                            span.set_exc_info(*sys.exc_info())
                            raise
                        finally:
                            if span:
                                span.finish()

                @wraps(func)
                def wrapper(*args, **kwargs):
                    if not LLMObs.enabled:
                        log.warning(SPAN_START_WHILE_DISABLED_WARNING)
                        return func(*args, **kwargs)
                    _, span_name = _get_llmobs_span_options(name, None, func)
                    traced_operation = getattr(LLMObs, operation_kind, LLMObs.workflow)
                    with traced_operation(
                        name=span_name, session_id=session_id, ml_app=ml_app, _decorator=True
                    ) as span:
                        func_signature = signature(func)
                        bound_args = func_signature.bind_partial(*args, **kwargs)
                        if _automatic_io_annotation and bound_args.arguments:
                            LLMObs.annotate(span=span, input_data=dict(bound_args.arguments))
                        resp = func(*args, **kwargs)
                        if (
                            _automatic_io_annotation
                            and resp
                            and operation_kind != "retrieval"
                            and span._get_ctx_item(OUTPUT_VALUE) is None
                        ):
                            LLMObs.annotate(span=span, output_data=resp)
                        return resp

            return generator_wrapper if (isgeneratorfunction(func) or isasyncgenfunction(func)) else wrapper

        if original_func and callable(original_func):
            return inner(original_func)
        return inner

    return decorator


llm = _model_decorator("llm")
embedding = _model_decorator("embedding")
workflow = _llmobs_decorator("workflow")
task = _llmobs_decorator("task")
tool = _llmobs_decorator("tool")
retrieval = _llmobs_decorator("retrieval")
agent = _llmobs_decorator("agent")
