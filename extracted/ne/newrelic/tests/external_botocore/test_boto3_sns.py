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

import boto3
import pytest
from moto import mock_aws
from testing_support.fixtures import dt_enabled
from testing_support.validators.validate_span_events import validate_span_events
from testing_support.validators.validate_transaction_metrics import validate_transaction_metrics
from testing_support.validators.validate_tt_segment_params import validate_tt_segment_params

from newrelic.api.background_task import background_task
from newrelic.common.package_version_utils import get_package_version_tuple

MOTO_VERSION = get_package_version_tuple("moto")
AWS_ACCESS_KEY_ID = "AAAAAAAAAAAACCESSKEY"
AWS_SECRET_ACCESS_KEY = "AAAAAASECRETKEY"
AWS_REGION_NAME = "us-east-1"
SNS_URL = "sns-us-east-1.amazonaws.com"
TOPIC = "arn:aws:sns:us-east-1:123456789012:some-topic"
sns_metrics = [(f"MessageBroker/SNS/Topic/Produce/Named/{TOPIC}", 1)]
sns_metrics_phone = [("MessageBroker/SNS/Topic/Produce/Named/PhoneNumber", 1)]


@dt_enabled
@validate_span_events(expected_agents=("aws.requestId",), count=2)
@validate_span_events(exact_agents={"aws.operation": "CreateTopic"}, count=1)
@validate_span_events(exact_agents={"aws.operation": "Publish"}, count=1)
@validate_tt_segment_params(present_params=("aws.requestId",))
@pytest.mark.parametrize("topic_argument", ("TopicArn", "TargetArn"))
@validate_transaction_metrics(
    "test_boto3_sns:test_publish_to_sns_topic",
    scoped_metrics=sns_metrics,
    rollup_metrics=sns_metrics,
    background_task=True,
)
@background_task()
@mock_aws
def test_publish_to_sns_topic(topic_argument):
    conn = boto3.client(
        "sns",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME,
    )

    topic_arn = conn.create_topic(Name="some-topic")["TopicArn"]

    kwargs = {topic_argument: topic_arn}
    published_message = conn.publish(Message="my msg", **kwargs)
    assert "MessageId" in published_message


@dt_enabled
@validate_span_events(expected_agents=("aws.requestId",), count=3)
@validate_span_events(exact_agents={"aws.operation": "CreateTopic"}, count=1)
@validate_span_events(exact_agents={"aws.operation": "Subscribe"}, count=1)
@validate_span_events(exact_agents={"aws.operation": "Publish"}, count=1)
@validate_tt_segment_params(present_params=("aws.requestId",))
@validate_transaction_metrics(
    "test_boto3_sns:test_publish_to_sns_phone",
    scoped_metrics=sns_metrics_phone,
    rollup_metrics=sns_metrics_phone,
    background_task=True,
)
@background_task()
@mock_aws
def test_publish_to_sns_phone():
    conn = boto3.client(
        "sns",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME,
    )

    topic_arn = conn.create_topic(Name="some-topic")["TopicArn"]
    conn.subscribe(TopicArn=topic_arn, Protocol="sms", Endpoint="5555555555")

    published_message = conn.publish(PhoneNumber="5555555555", Message="my msg")
    assert "MessageId" in published_message
