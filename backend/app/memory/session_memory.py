from typing import Any, Dict
import redis
import os
import json

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
_r = redis.from_url(REDIS_URL)


class SessionMemory:
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl = ttl_seconds

    def set(self, session_id: str, data: Dict[str, Any]):
        _r.setex(session_id, self.ttl, json.dumps(data))

    def get(self, session_id: str) -> Dict[str, Any]:
        v = _r.get(session_id)
        if not v:
            return {}
        return json.loads(v)

    def delete(self, session_id: str):
        _r.delete(session_id)
