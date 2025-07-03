import boto3
import os
import pytest
from moto import mock_dynamodb
from amplify.backend.function.userHandler.src.index import set_user

TABLE_NAME = "userTable"
REGION = "eu-west-1"

@pytest.fixture
def fake_user_table():
    with mock_dynamodb():
        os.environ["STORAGE_USERTABLE_NAME"] = TABLE_NAME
        os.environ["REGION"] = REGION

        dynamodb = boto3.resource("dynamodb", region_name=REGION)
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "userId", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "userId", "AttributeType": "S"}
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        )
        table.wait_until_exists()

        yield table


def test_set_user_success(fake_user_table):
    user_data = {
        "userId": "u001",
        "name": "Alice",
        "email": "alice@example.com"
    }

    result = set_user(user_data)

    assert result["message"] == "User saved"
    assert result["user"]["userId"] == "u001"

    response = fake_user_table.get_item(Key={"userId": "u001"})
    item = response.get("Item")
    assert item["email"] == "alice@example.com"
