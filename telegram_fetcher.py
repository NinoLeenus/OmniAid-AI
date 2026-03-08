import json
import os
from pathlib import Path
from typing import Any
from urllib import error, request

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

OFFSET_FILE = Path("data/telegram_offset.txt")


def _bot_token() -> str:
    return os.getenv("TELEGRAM_BOT_TOKEN", "").strip()


def _allowed_user_ids_raw() -> str:
    return os.getenv("TELEGRAM_ALLOWED_USER_IDS", "").strip()


def _topic_keywords_raw() -> str:
    return os.getenv("TELEGRAM_TOPIC_KEYWORDS", "").strip()


def _base_url() -> str:
    token = _bot_token()
    if not token:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable")
    return f"https://api.telegram.org/bot{token}"


def _api_call(method: str, payload: dict[str, Any]) -> dict[str, Any]:
    url = f"{_base_url()}/{method}"
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            parsed = json.loads(body)
    except error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Telegram API HTTP error {exc.code}: {err_body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Telegram API connection error: {exc.reason}") from exc

    if not parsed.get("ok", False):
        raise RuntimeError(f"Telegram API error for {method}: {parsed}")

    return parsed


def _parse_allowed_user_ids() -> set[int]:
    raw = _allowed_user_ids_raw()
    if not raw:
        return set()
    user_ids: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        user_ids.add(int(part))
    return user_ids


def _parse_keywords() -> tuple[str, ...]:
    raw = _topic_keywords_raw()
    if not raw:
        return ()
    return tuple(k.strip().lower() for k in raw.split(",") if k.strip())


def _read_offset() -> int | None:
    if not OFFSET_FILE.exists():
        return None
    raw = OFFSET_FILE.read_text(encoding="utf-8").strip()
    if not raw:
        return None
    return int(raw)


def _write_offset(update_id: int) -> None:
    OFFSET_FILE.parent.mkdir(parents=True, exist_ok=True)
    OFFSET_FILE.write_text(str(update_id), encoding="utf-8")


def fetch_messages(limit: int = 20) -> list[dict[str, Any]]:
    allowed_user_ids = _parse_allowed_user_ids()
    topic_keywords = _parse_keywords()

    offset = _read_offset()
    payload: dict[str, Any] = {
        "limit": max(1, min(limit, 100)),
        "timeout": 0,
        "allowed_updates": ["message"],
    }
    if offset is not None:
        payload["offset"] = offset + 1

    updates = _api_call("getUpdates", payload).get("result", [])
    messages: list[dict[str, Any]] = []
    max_update_id = offset

    for upd in updates:
        update_id = upd.get("update_id")
        if isinstance(update_id, int):
            max_update_id = update_id if max_update_id is None else max(max_update_id, update_id)

        msg = upd.get("message")
        if not msg:
            continue

        from_user = msg.get("from", {})
        user_id = from_user.get("id")
        if allowed_user_ids and user_id not in allowed_user_ids:
            continue

        text = (msg.get("text") or msg.get("caption") or "").strip()
        if not text:
            continue

        if topic_keywords and not any(k in text.lower() for k in topic_keywords):
            continue

        chat = msg.get("chat", {})
        chat_id = chat.get("id")
        message_id = msg.get("message_id")
        if chat_id is None or message_id is None:
            continue

        author = from_user.get("username") or from_user.get("first_name") or "Unknown"
        unified_id = f"tg:{chat_id}:{message_id}"

        messages.append(
            {
                "id": unified_id,
                "author": author,
                "body": text,
                "chat_id": chat_id,
                "message_id": message_id,
                "user_id": user_id,
            }
        )

    if isinstance(max_update_id, int):
        _write_offset(max_update_id)

    return messages


def send_approved_reply(msg: dict[str, Any], summary: str, response: str) -> None:
    summary = (summary or "").strip()
    response = (response or "").strip()
    reply_text = (
        "Thank you for your message.\n\n"
        f"Summary:\n{summary}\n\n"
        f"Response:\n{response}"
    ).strip()

    payload = {
        "chat_id": msg["chat_id"],
        "text": reply_text,
        "reply_to_message_id": msg["message_id"],
        "allow_sending_without_reply": True,
    }
    _api_call("sendMessage", payload)
