from __future__ import annotations

import asyncio
import json
import logging

from app.models import TelegramEvent
from app.telegram_send import TelegramSender

logger = logging.getLogger(__name__)


class DownstreamProcessor:
    """Replace this class with your own downstream actions."""

    def __init__(self, bot_token: str | None = None) -> None:
        self.sender = TelegramSender(bot_token) if bot_token else None

    async def handle_event(self, event: TelegramEvent) -> None:
        payload = {
            "message_id": event.message_id,
            "type": event.event_type,
            "chat_id": event.chat_id,
            "user_id": event.user_id,
            "username": event.username,
            "first_name": event.first_name,
            "text": event.content,
            "created_at": event.created_at_iso,
        }
        logger.info("DOWNSTREAM_EVENT %s", json.dumps(payload, ensure_ascii=False))

        # -----------------------------------------------------------
        # Example: reply to the user
        # -----------------------------------------------------------
        if self.sender:
            reply_text = f"Echo: {event.content}"
            await self.sender.send_message(event.chat_id, reply_text)

        # -----------------------------------------------------------
        # Replace this section with your real downstream logic:
        #   - Call an API
        #   - Write to a database
        #   - Publish to Kafka / Redis / SQS
        #   - Trigger an alert or automated action
        # -----------------------------------------------------------
        await asyncio.sleep(0)
