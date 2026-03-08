from telegram_fetcher import fetch_messages

def ingest_data():
    messages = fetch_messages()
    return messages