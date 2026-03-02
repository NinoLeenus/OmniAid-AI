import boto3
import json

s3 = boto3.client("s3", region_name="ap-southeast-2")
BUCKET = "omniaid-raw-messages"

def store_raw_message(msg):
    key = f"messages/{msg['id']}.json"
    s3.put_object(Bucket=BUCKET, Key=key, Body=json.dumps(msg))