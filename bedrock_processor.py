import boto3
import json
import re

bedrock = boto3.client("bedrock-runtime", region_name="ap-southeast-2")

INFERENCE_PROFILE_ARN = "arn:aws:bedrock:ap-southeast-2:153876892719:application-inference-profile/ozr3df6ffkl7"


def analyze_message(message, context):

    prompt = f"""
    You are an NGO volunteer assistant helping support people who report incidents.

    Your goal is to summarize the situation and provide a helpful, compassionate response.

    Guidelines for the Response:
    - Be empathetic and supportive.
    - Provide practical next steps the person can take.
    - Do NOT say "I cannot give legal advice".
    - Do NOT mention legal disclaimers.
    - Avoid AI-like language.
    - Keep the tone human and supportive.
    - End the response by reassuring the person that the team will review the report and be in touch.

    Return STRICTLY in this format:

    Case Type: <type>
    Urgency: <High/Medium/Low>
    Summary: <1-2 sentence summary>
    Response: <empathetic response with practical next steps and reassurance>

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