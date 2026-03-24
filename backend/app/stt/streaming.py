from typing import Any
import asyncio
import logging

logger = logging.getLogger("stt")


class StreamingSTT:
    def __init__(self):
        pass

    async def transcribe_chunk(self, audio_bytes: bytes) -> str:
        # Placeholder: in production, forward bytes to a streaming STT provider
        await asyncio.sleep(0.02)  # simulate small processing
        logger.debug("Received audio chunk for STT")
        return "Book appointment tomorrow 10am"
