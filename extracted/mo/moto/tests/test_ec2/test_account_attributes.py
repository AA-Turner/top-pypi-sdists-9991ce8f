import boto3

from moto import mock_aws


@mock_aws
def test_describe_account_attributes():
    conn = boto3.client("ec2", region_name="us-east-1")
    response = conn.describe_account_attributes()
    expected_attribute_values = [
        {
            "AttributeValues": [{"AttributeValue": "5"}],
            "AttributeName": "vpc-max-security-groups-per-interface",
        },
        {
            "AttributeValues": [{"AttributeValue": "20"}],
            "AttributeName": "max-instances",
        },
        {
            "AttributeValues": [{"AttributeValue": "EC2"}, {"AttributeValue": "VPC"}],
            "AttributeName": "supported-platforms",
        },
        {
            "AttributeValues": [{"AttributeValue": "none"}],
            "AttributeName": "default-vpc",
        },
        {
            "AttributeValues": [{"AttributeValue": "5"}],
            "AttributeName": "max-elastic-ips",
        },
        {
            "AttributeValues": [{"AttributeValue": "5"}],
            "AttributeName": "vpc-max-elastic-ips",
        },
    ]
    assert response["AccountAttributes"] == expected_attribute_values
