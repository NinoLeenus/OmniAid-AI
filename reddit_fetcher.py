# import praw
import os
from dotenv import load_dotenv
from mock_messages import mock_messages

load_dotenv()

# ============================
# TEMP: Comment Reddit client
# ============================

# reddit = praw.Reddit(
#     client_id=os.getenv("REDDIT_CLIENT_ID"),
#     client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
#     user_agent="OmniAidAI"
# )

def fetch_messages(limit=5):
    # ============================
    # TEMP: Use mock messages
    # ============================
    return mock_messages[:limit]

    # ============================
    # Original Reddit logic (disabled)
    # ============================
    # messages = []
    # for msg in reddit.inbox.unread(limit=limit):
    #     messages.append({
    #         "id": msg.id,
    #         "author": str(msg.author),
    #         "body": msg.body
    #     })
    # return messages