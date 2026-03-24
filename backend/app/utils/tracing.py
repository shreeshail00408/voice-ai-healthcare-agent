import logging
from typing import Dict, Any

logger = logging.getLogger("tracing")


def log_traces(session_id: str, traces: Dict[str, Any]):
    logger.info(f"[trace] session={session_id} traces={traces}")
