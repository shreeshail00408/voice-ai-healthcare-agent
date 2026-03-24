from typing import Tuple, Dict, Any
import logging
import time
from ..memory.session_memory import SessionMemory

logger = logging.getLogger("agent")


class ConversationAgent:
    def __init__(self):
        self.memory = SessionMemory()

    async def handle_turn(self, text: str, lang: str) -> Tuple[str, Dict[str, Any]]:
        # Minimal intent recognition stub
        start = time.time()
        traces = {"steps": []}

        # simple intent rules (placeholder)
        if "book" in text.lower() or "appointment" in text.lower():
            traces["steps"].append("intent_detected:book_appointment")
            # parse placeholders
            # call check availability tool
            traces["steps"].append("tool:check_availability -> calling")
            t0 = time.time()
            # lazy import to avoid heavy DB imports at module import time
            from ..tools import scheduler_tools
            avail = scheduler_tools.check_availability(doctor_id=1, datetime="2026-01-01T10:00:00")
            traces["tool_check_availability_ms"] = int((time.time() - t0) * 1000)

            if avail:
                traces["steps"].append("tool:book_appointment -> calling")
                t1 = time.time()
                appt = scheduler_tools.book_appointment(patient_id=1, doctor_id=1, datetime="2026-01-01T10:00:00")
                traces["tool_book_appointment_ms"] = int((time.time() - t1) * 1000)
                response = "Booked appointment on 2026-01-01 10:00"
            else:
                response = "Doctor unavailable at requested time. Suggest 11:00. Confirm?"
        else:
            traces["steps"].append("intent_detected:unknown")
            response = "I didn't understand. Do you want to book, reschedule, or cancel an appointment?"

        total_ms = int((time.time() - start) * 1000)
        traces["total_handler_ms"] = total_ms

        logger.info(f"Agent response: {response}")
        logger.debug(f"Traces: {traces}")
        return response, traces
