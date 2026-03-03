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

    # Anthropic model code commented out below:
    # body = json.dumps({
    #     "anthropic_version": "bedrock-2023-05-31",
    #     "max_tokens": 300,
    #     "messages": [
    #         {"role": "user", "content": prompt}
    #     ]
    # })
    # response = bedrock.invoke_model(
    #     modelId="anthropic.claude-3-sonnet-20240229-v1:0",
    #     body=body
    # )
    # result = json.loads(response["body"].read())
    # return result["content"][0]["text"]

    # Use AWS Titan Text (nova2) model instead
    body = json.dumps({
        "inputText": prompt,
        "maxTokens": 300,
        "temperature": 0.7,
        "topP": 0.9
    })
    response = bedrock.invoke_model(
        modelId="amazon.nova-2-lite-v1:0",
        body=body
    )
    result = json.loads(response["body"].read())
    return result["results"][0]["outputText"]