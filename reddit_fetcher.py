import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="OmniAidAI"
)

def fetch_messages(limit=5):
    messages = []
    for msg in reddit.inbox.unread(limit=limit):
        messages.append({
            "id": msg.id,
            "author": str(msg.author),
            "body": msg.body
        })
    return messages