from datetime import datetime, timedelta
from typing import Optional


def suggest_nearest_slot(requested: datetime, window_minutes: int = 60, interval_minutes: int = 60) -> Optional[datetime]:
    # naive linear search for next available slot
    candidate = requested + timedelta(minutes=interval_minutes)
    end = requested + timedelta(minutes=window_minutes)
    while candidate <= end:
        # in real impl, check DB for conflicts
        # here we assume next slot is available
        return candidate
    return None
