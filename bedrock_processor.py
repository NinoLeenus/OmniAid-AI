import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="ap-southeast-2")

INFERENCE_PROFILE_ARN = "arn:aws:bedrock:ap-southeast-2:153876892719:application-inference-profile/ozr3df6ffkl7"


def analyze_message(message, context):

    prompt = f"""
You are an NGO volunteer assistant. Provide empathetic support and helpful suggestions without giving legal advice.

Context:
{context}

Message:
{message}

Return STRICTLY in this format:

Case Type: <type>
Urgency: <High/Medium/Low>
Summary: <summary>
Response: <response>
"""

    body = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
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

    result_text = result["output"]["message"]["content"][0]["text"]

    # Default values to prevent KeyError
    data = {
        "case_type": "Unknown",
        "urgency": "Unknown",
        "summary": "Not generated",
        "response": "Not generated"
    }

    lines = result_text.split("\n")

    for line in lines:
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()

        if "case type" in key:
            data["case_type"] = value

        elif "urgency" in key:
            data["urgency"] = value

        elif "summary" in key:
            data["summary"] = value

        elif "response" in key:
            data["response"] = value

    return data