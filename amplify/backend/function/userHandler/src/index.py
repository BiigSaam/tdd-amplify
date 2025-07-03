import json
import os
import boto3

region = os.environ.get("REGION", "eu-west-1")
table_name = os.environ.get("STORAGE_USERTABLE_NAME", "userTable")

dynamodb = boto3.resource("dynamodb", region_name=region)
table = dynamodb.Table(table_name)

def set_user(user: dict) -> dict:
    try:
        table.put_item(Item=user)
        return {"message": "User saved", "user": user}
    except Exception as e:
        return {"error": str(e)}

def handler(event, context):
    user = event.get("user")
    if not user or "userId" not in user:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing userId"})
        }
    return {
        "statusCode": 200,
        "body": json.dumps(set_user(user))
    }
