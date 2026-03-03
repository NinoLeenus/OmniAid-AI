import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="ap-southeast-2")

INFERENCE_PROFILE_ARN = "arn:aws:bedrock:ap-southeast-2:153876892719:inference-profile/nova2-lite-profile"

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
            "max_new_tokens": 300,
            "temperature": 0.5
        }
    }

    response = bedrock.invoke_model(
        modelId=INFERENCE_PROFILE_ARN,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    return result["output"]["message"]["content"][0]["text"]