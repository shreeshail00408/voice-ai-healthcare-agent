from typing import Iterable
import time
import logging

logger = logging.getLogger("tts")


class StreamingTTS:
    def __init__(self):
        pass

    def synthesize_stream(self, text: str, lang: str) -> Iterable[bytes]:
        # Placeholder: replace with actual TTS streaming API
        logger.debug(f"Synthesizing TTS for lang={lang}, text={text}")
        # simulate three audio chunks
        for i in range(3):
            time.sleep(0.01)
            yield f"AUDIO-CHUNK-{i}".encode('utf-8')
