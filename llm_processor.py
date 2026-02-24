from transformers import pipeline
from prompts import CLASSIFY_PROMPT

classifier = pipeline("text2text-generation", model="google/flan-t5-small")

def analyze_message(message):
    prompt = CLASSIFY_PROMPT.format(message=message)

    result = classifier(prompt, max_length=256)[0]["generated_text"]

    print(result)
    return result