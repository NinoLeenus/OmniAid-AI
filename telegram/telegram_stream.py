from __future__ import annotations

import asyncio
import logging
from contextlib import suppress

from app.config import load_settings
from app.downstream import DownstreamProcessor
from app.models import TelegramEvent
from app.telegram_stream import TelegramBotStreamer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("telegram_app")


async def worker(
    queue: asyncio.Queue[TelegramEvent],
    processor: DownstreamProcessor,
    worker_id: int,
) -> None:
    while True:
        event = await queue.get()
        try:
            await processor.handle_event(event)
            logger.info(
                "worker=%s processed msg=%s type=%s from=%s",
                worker_id,
                event.message_id,
                event.event_type,
                event.username or event.user_id,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "worker=%s failed msg=%s err=%s", worker_id, event.message_id, exc
            )
        finally:
            queue.task_done()


async def main() -> None:
    settings = load_settings()

    queue: asyncio.Queue[TelegramEvent] = asyncio.Queue(maxsize=1000)
    processor = DownstreamProcessor(bot_token=settings.telegram_bot_token)
    streamer = TelegramBotStreamer(settings, queue)

    workers = [
        asyncio.create_task(worker(queue, processor, i), name=f"worker-{i}")
        for i in range(1, 4)
    ]

    logger.info("Service started — send a message to your bot!")
    try:
        await streamer.run()
    finally:
        for w in workers:
            w.cancel()
        with suppress(asyncio.CancelledError):
            await asyncio.gather(*workers)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
