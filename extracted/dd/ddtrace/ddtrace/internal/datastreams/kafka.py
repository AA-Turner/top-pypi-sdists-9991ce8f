import time

from confluent_kafka import TopicPartition

from ddtrace import config
from ddtrace.internal import core
from ddtrace.internal.datastreams.processor import DsmPathwayCodec
from ddtrace.internal.datastreams.utils import _calculate_byte_size
from ddtrace.internal.logger import get_logger
from ddtrace.internal.utils import ArgumentError
from ddtrace.internal.utils import get_argument_value
from ddtrace.internal.utils import set_argument_value


INT_TYPES = (int,)
MESSAGE_ARG_POSITION = 1
KEY_ARG_POSITION = 2
KEY_KWARG_NAME = "key"

disable_header_injection = False

log = get_logger(__name__)


def dsm_kafka_message_produce(instance, args, kwargs, is_serializing, span):
    from . import data_streams_processor as processor

    topic = core.get_item("kafka_topic")
    cluster_id = core.get_item("kafka_cluster_id")
    message = get_argument_value(args, kwargs, MESSAGE_ARG_POSITION, "value", optional=True)
    key = get_argument_value(args, kwargs, KEY_ARG_POSITION, KEY_KWARG_NAME, optional=True)
    headers = kwargs.get("headers", {})

    payload_size = 0
    payload_size += _calculate_byte_size(message)
    payload_size += _calculate_byte_size(key)
    payload_size += _calculate_byte_size(headers)

    edge_tags = ["direction:out", "topic:" + topic, "type:kafka"]
    if cluster_id:
        edge_tags.append("kafka_cluster_id:" + str(cluster_id))

    ctx = processor().set_checkpoint(edge_tags, payload_size=payload_size, span=span)
    if not disable_header_injection:
        DsmPathwayCodec.encode(ctx, headers)
        kwargs["headers"] = headers

    on_delivery_kwarg = "on_delivery"
    on_delivery_arg = 5
    on_delivery = None
    try:
        on_delivery = get_argument_value(args, kwargs, on_delivery_arg, on_delivery_kwarg)
    except ArgumentError:
        if not is_serializing:
            on_delivery_kwarg = "callback"
            on_delivery_arg = 4
            on_delivery = get_argument_value(args, kwargs, on_delivery_arg, on_delivery_kwarg, optional=True)

    def wrapped_callback(err, msg):
        global disable_header_injection
        if err is None:
            reported_offset = msg.offset() if isinstance(msg.offset(), INT_TYPES) else -1
            processor().track_kafka_produce(msg.topic(), msg.partition(), reported_offset, time.time())
        elif err.code() == -1 and not disable_header_injection:
            disable_header_injection = True
            log.error(
                "Kafka Broker responded with UNKNOWN_SERVER_ERROR (-1). Please look at broker logs for more "
                "information. Tracer message header injection for Kafka is disabled."
            )
        if on_delivery is not None:
            on_delivery(err, msg)

    try:
        args, kwargs = set_argument_value(args, kwargs, on_delivery_arg, on_delivery_kwarg, wrapped_callback)
    except ArgumentError:
        # we set the callback even if it's not set by the client, to track produce calls correctly.
        kwargs[on_delivery_kwarg] = wrapped_callback


def dsm_kafka_message_consume(instance, message, span):
    from . import data_streams_processor as processor

    headers = {header[0]: header[1] for header in (message.headers() or [])}
    topic = core.get_item("kafka_topic")
    cluster_id = core.get_item("kafka_cluster_id")
    group = instance._group_id

    payload_size = 0
    if hasattr(message, "len"):
        # message.len() is only supported for some versions of confluent_kafka
        payload_size += message.len()
    else:
        payload_size += _calculate_byte_size(message.value())

    payload_size += _calculate_byte_size(message.key())
    payload_size += _calculate_byte_size(headers)

    ctx = DsmPathwayCodec.decode(headers, processor())

    edge_tags = ["direction:in", "group:" + group, "topic:" + topic, "type:kafka"]
    if cluster_id:
        edge_tags.append("kafka_cluster_id:" + str(cluster_id))

    ctx.set_checkpoint(
        edge_tags,
        payload_size=payload_size,
        span=span,
    )

    if instance._auto_commit:
        # it's not exactly true, but if auto commit is enabled, we consider that a message is acknowledged
        # when it's read. We add one because the commit offset is the next message to read.
        reported_offset = (message.offset() + 1) if isinstance(message.offset(), INT_TYPES) else -1
        processor().track_kafka_commit(
            instance._group_id, message.topic(), message.partition(), reported_offset, time.time()
        )


def dsm_kafka_message_commit(instance, args, kwargs):
    from . import data_streams_processor as processor

    message = get_argument_value(args, kwargs, 0, "message", optional=True)

    offsets = []
    if message is not None:
        # the commit offset is the next message to read. So last message read + 1
        reported_offset = message.offset() + 1 if isinstance(message.offset(), INT_TYPES) else -1
        offsets = [TopicPartition(message.topic(), message.partition(), reported_offset)]
    else:
        offsets = get_argument_value(args, kwargs, 1, "offsets", True) or []

    for offset in offsets:
        reported_offset = offset.offset if isinstance(offset.offset, INT_TYPES) else -1
        processor().track_kafka_commit(instance._group_id, offset.topic, offset.partition, reported_offset, time.time())


if config._data_streams_enabled:
    core.on("kafka.produce.start", dsm_kafka_message_produce)
    core.on("kafka.consume.start", dsm_kafka_message_consume)
    core.on("kafka.commit.start", dsm_kafka_message_commit)
