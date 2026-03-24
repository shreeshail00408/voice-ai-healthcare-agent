Backend FastAPI app for Voice AI Agent.

Structure:
- `app/main.py` - FastAPI application
- `app/websocket.py` - WebSocket voice gateway endpoint
- `app/agent` - Conversation agent and tool invocations
- `app/tools` - Scheduler tools
- `app/memory` - Redis session memory
- `app/stt`, `app/tts` - STT/TTS provider stubs

Run locally:

1. Set environment variables from `.env.example`
2. Start Postgres and Redis (see infra/docker-compose.yml)
3. Install deps: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --reload --port 8000`
