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

    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": prompt}
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 300,
            "temperature": 0.7
        }
    }

    response = bedrock.invoke_model(
        modelId="amazon.nova-2-lite-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    # Extract text safely
    output_text = result["output"]["message"]["content"][0]["text"]
    return output_text