import boto3
import os

# # Get AWS credentials and region from environment variables
# aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
# aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
# aws_region = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")

# dynamodb = boto3.resource(
#     "dynamodb",
#     region_name=aws_region,
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key
# )
# table = dynamodb.Table("processed_messages")

import boto3

dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-2")
table = dynamodb.Table("OmniAidMessages")

def is_processed(message_id):
    response = table.get_item(Key={"message_id": message_id})
    return "Item" in response

def mark_processed(message_id):
    table.put_item(Item={"message_id": message_id})