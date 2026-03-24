# Voice AI Agent — Project Skeleton

This workspace contains a modular, production-oriented skeleton for a real-time multilingual voice AI agent. It includes:

- FastAPI backend with WebSocket voice gateway
- Conversation agent with tool-calling pattern
- Redis session memory and Postgres persistent storage schemas
- STT/TTS provider stubs for streaming integration
- Celery worker for outbound reminders
- Frontend Next.js demo page that streams audio via WebSocket
- Docker Compose to run Postgres and Redis

Next steps:
- Replace STT/TTS stubs with streaming provider SDKs (Deepgram/Whisper/Google for STT; ElevenLabs/Azure for TTS)
- Integrate OpenAI/Llama via LangChain in `app/agent` for richer NLU/dialogue
- Harden scheduler logic with transaction isolation and optimistic locking
- Add authentication, RBAC, and rate-limiting
