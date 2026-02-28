import boto3

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
table = dynamodb.Table("processed_messages")

def is_processed(message_id):
    response = table.get_item(Key={"message_id": message_id})
    return "Item" in response

def mark_processed(message_id):
    table.put_item(Item={"message_id": message_id})