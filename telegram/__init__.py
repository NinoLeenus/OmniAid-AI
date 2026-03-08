from __future__ import annotations

from telegram import Bot


class TelegramSender:
    """Helper to send messages back to users."""

    def __init__(self, bot_token: str) -> None:
        self.bot = Bot(token=bot_token)

    async def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: str = "Markdown",
    ) -> None:
        """Send a text message to a chat/user."""
        await self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
        )

    async def send_photo(
        self,
        chat_id: int,
        photo: str,
        caption: str | None = None,
    ) -> None:
        """Send a photo to a chat/user (URL or file_id)."""
        await self.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
        )

    async def send_document(
        self,
        chat_id: int,
        document: str,
        caption: str | None = None,
    ) -> None:
        """Send a document to a chat/user (URL or file_id)."""
        await self.bot.send_document(
            chat_id=chat_id,
            document=document,
            caption=caption,
        )
