import boto3
import pytest
from moto import mock_dynamodb
from index import set_user  # <-- adapte si ton fichier a un autre nom

TABLE_NAME = "userTable-dev"

@pytest.fixture
def dynamodb_table():
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "userId", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "userId", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        )

        table.wait_until_exists()
        yield table

def test_set_user_success(monkeypatch, dynamodb_table):
    monkeypatch.setenv("STORAGE_USERTABLE_NAME", TABLE_NAME)
    monkeypatch.setenv("REGION", "eu-west-1")

    user = {
        "userId": "u001",
        "name": "Alice",
        "email": "alice@example.com"
    }

    result = set_user(user)

    assert result["message"] == "User saved"
    assert result["user"] == user

    item = dynamodb_table.get_item(Key={"userId": "u001"})["Item"]
    assert item["name"] == "Alice"
    assert item["email"] == "alice@example.com"
