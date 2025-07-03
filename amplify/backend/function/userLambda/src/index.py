import json
import os
import boto3

# Initialisation du client DynamoDB
region = os.environ.get("REGION")
dynamodb = boto3.resource("dynamodb", region_name=region)
table_name = os.environ.get("STORAGE_USERTABLE_NAME", "userTable")
table = dynamodb.Table(table_name)


def get_user(user_id: str) -> dict | None:
    try:
        response = table.get_item(Key={"userId": user_id})
        return response.get("Item")
    except Exception as e:
        print(f"[ERROR] get_user() failed: {e}")
        return None


def handler(event, context):
    print("received event:", event)

    user_id = event.get("userId")
    if not user_id:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({"error": "Missing userId"})
        }

    user = get_user(user_id)
    if not user:
        return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({"error": "User not found"})
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps(user)
    }
