from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import time
import logging
from .stt import StreamingSTT
from .tts import StreamingTTS
from .language import detect_language
from .agent.agent import ConversationAgent

router = APIRouter()
logger = logging.getLogger("websocket")


@router.websocket("/ws/voice")
async def voice_ws(ws: WebSocket):
    await ws.accept()
    stt = StreamingSTT()
    tts = StreamingTTS()
    agent = ConversationAgent()

    try:
        while True:
            msg = await ws.receive_bytes()
            start_stt = time.time()
            text = await stt.transcribe_chunk(msg)
            stt_latency = (time.time() - start_stt) * 1000
            logger.info(f"STT latency: {stt_latency:.1f}ms")

            start_ld = time.time()
            lang = detect_language(text)
            ld_latency = (time.time() - start_ld) * 1000
            logger.info(f"Language detection latency: {ld_latency:.1f}ms, lang={lang}")

            start_llm = time.time()
            response, traces = await agent.handle_turn(text, lang)
            llm_latency = (time.time() - start_llm) * 1000
            logger.info(f"Agent (LLM+tools) latency: {llm_latency:.1f}ms")
            logger.info(f"Reasoning traces: {traces}")

            start_tts = time.time()
            # get audio bytes stream from TTS in preferred lang
            audio_chunks = tts.synthesize_stream(response, lang)
            tts_latency = (time.time() - start_tts) * 1000
            logger.info(f"TTS generation latency: {tts_latency:.1f}ms")

            # stream audio back
            for chunk in audio_chunks:
                await ws.send_bytes(chunk)

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
