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

Return in this format:
Case Type:
Urgency (High/Medium/Low):
Summary:
Response:
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

    result_text = result["output"]["message"]["content"][0]["text"]

    # Parse the result
    lines = result_text.strip().split('\n')
    data = {}
    current_key = None
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if key == 'Case Type':
                data['case_type'] = value
                current_key = 'case_type'
            elif key.startswith('Urgency'):
                data['urgency'] = value
                current_key = 'urgency'
            elif key == 'Summary':
                data['summary'] = value
                current_key = 'summary'
            elif key == 'Response':
                data['response'] = value
                current_key = 'response'
        else:
            if current_key and line.strip():
                data[current_key] += ' ' + line.strip()

    return data