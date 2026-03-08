from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    telegram_allowed_user_ids: tuple[int, ...] = ()
    telegram_topic_keywords: tuple[str, ...] = ()


def _parse_user_ids(raw: str | None) -> tuple[int, ...]:
    if not raw:
        return ()
    ids: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if part:
            ids.append(int(part))
    return tuple(ids)


def _parse_keywords(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return ()
    return tuple(k.strip().lower() for k in raw.split(",") if k.strip())


def load_settings() -> Settings:
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Missing required environment variable: TELEGRAM_BOT_TOKEN")

    return Settings(
        telegram_bot_token=token,
        telegram_allowed_user_ids=_parse_user_ids(
            os.getenv("TELEGRAM_ALLOWED_USER_IDS")
        ),
        telegram_topic_keywords=_parse_keywords(
            os.getenv("TELEGRAM_TOPIC_KEYWORDS")
        ),
    )
