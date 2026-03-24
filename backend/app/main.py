from fastapi import FastAPI
from .websocket import router as websocket_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Voice AI Agent")

app.include_router(websocket_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
