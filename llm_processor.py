import requests

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

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
    