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

Classify and respond in this format:

Case Type:
Urgency (High/Medium/Low):
Summary:
Draft Response (empathetic, no legal advice):
"""

    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 300,
            "temperature": 0.7,
            "topP": 0.9
        }
    }

    response = bedrock.invoke_model(
        modelId="amazon.titan-text-lite-v1",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    return result["results"][0]["outputText"]