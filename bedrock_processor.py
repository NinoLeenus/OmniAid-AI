import boto3
import json
import re

bedrock = boto3.client("bedrock-runtime", region_name="ap-southeast-2")

INFERENCE_PROFILE_ARN = "arn:aws:bedrock:ap-southeast-2:153876892719:application-inference-profile/ozr3df6ffkl7"


def analyze_message(message, context):

    prompt = f"""
You are an NGO volunteer assistant helping support people who report incidents.

Your task is to analyze the message and provide a short ticket summary and a compassionate response.

IMPORTANT RULES:
- Be empathetic and human
- Do NOT provide legal advice
- Do NOT include reasoning or explanations
- Do NOT include headings other than the ones specified
- Do NOT include "Draft Response"
- The response should sound like a caring volunteer

Return STRICTLY in this format:

Case Type: <type>
Urgency: <High/Medium/Low>
Summary: <1-2 sentence summary>
Response: <empathetic human response>

Context:
{context}

Message:
{message}
"""

    body = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 400,
            "temperature": 0.4
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

    # Default safe values
    data = {
        "case_type": "Unknown",
        "urgency": "Medium",
        "summary": "",
        "response": ""
    }

    # Regex extraction (supports multiline responses)
    case_type = re.search(r"Case Type:\s*(.*)", result_text)
    urgency = re.search(r"Urgency:\s*(.*)", result_text)
    summary = re.search(r"Summary:\s*(.*)", result_text)
    response_match = re.search(r"Response:\s*(.*)", result_text, re.DOTALL)

    if case_type:
        data["case_type"] = case_type.group(1).strip()

    if urgency:
        data["urgency"] = urgency.group(1).strip()

    if summary:
        data["summary"] = summary.group(1).strip()

    if response_match:
        data["response"] = response_match.group(1).strip()

    return data