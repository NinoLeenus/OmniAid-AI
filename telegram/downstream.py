from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal


EventType = Literal["text", "photo", "document", "voice", "video", "sticker", "command", "other"]


@dataclass(frozen=True)
class TelegramEvent:
    message_id: int
    event_type: EventType
    chat_id: int
    user_id: int | None
    username: str | None
    first_name: str | None
    text: str | None
    caption: str | None
    date: float

    @property
    def created_at_iso(self) -> str:
        return datetime.fromtimestamp(self.date, tz=timezone.utc).isoformat()

    @property
    def content(self) -> str:
        """Return the best available text content."""
        return self.text or self.caption or ""
