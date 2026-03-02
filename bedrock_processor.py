import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="ap-southeast-2")

def analyze_message(message, context):
    prompt = f"""
You are an NGO volunteer assistant.

Context:
{context}

Message:
{message}

Return in this format:
Case Type:
Urgency (High/Medium/Low):
Summary:
Draft Response (empathetic, no legal advice):
"""

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=body
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]