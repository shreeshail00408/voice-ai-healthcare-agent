from typing import Optional, Dict, Any
import logging
import datetime

logger = logging.getLogger("scheduler_tools")

# In-memory fallback store for development when DB isn't available
_in_memory_appts = {}
_next_appt_id = 1


def _parse_datetime(dt_str: str) -> datetime.datetime:
    # naive parser for example purposes
    return datetime.datetime.fromisoformat(dt_str)


def _use_db():
    try:
        from ..database import db_session, models  # type: ignore
        return True
    except Exception:
        return False


def check_availability(doctor_id: int, datetime_str: str) -> bool:
    dt = _parse_datetime(datetime_str)
    if dt < datetime.datetime.now():
        return False

    if _use_db():
        from ..database import db_session, models  # type: ignore
        with db_session.get_session() as s:
            appts = s.query(models.Appointment).filter(
                models.Appointment.doctor_id == doctor_id,
                models.Appointment.datetime == dt,
                models.Appointment.status == 'scheduled'
            ).all()
            return len(appts) == 0

    # fallback: check in-memory store
    for appt in _in_memory_appts.values():
        if appt['doctor_id'] == doctor_id and appt['datetime'] == dt and appt['status'] == 'scheduled':
            return False
    return True


def book_appointment(patient_id: int, doctor_id: int, datetime_str: str) -> Dict[str, Any]:
    global _next_appt_id
    dt = _parse_datetime(datetime_str)
    if not check_availability(doctor_id, datetime_str):
        raise Exception("Slot unavailable")

    if _use_db():
        from ..database import db_session, models  # type: ignore
        with db_session.get_session() as s:
            appt = models.Appointment(patient_id=patient_id, doctor_id=doctor_id, datetime=dt, status='scheduled')
            s.add(appt)
            s.commit()
            s.refresh(appt)
            logger.info(f"Booked appointment id={appt.id}")
            return {"id": appt.id, "datetime": appt.datetime.isoformat()}

    # in-memory booking
    appt_id = _next_appt_id
    _next_appt_id += 1
    _in_memory_appts[appt_id] = {
        'id': appt_id,
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'datetime': dt,
        'status': 'scheduled'
    }
    logger.info(f"(in-memory) Booked appointment id={appt_id}")
    return {"id": appt_id, "datetime": dt.isoformat()}


def cancel_appointment(appointment_id: int) -> bool:
    if _use_db():
        from ..database import db_session, models  # type: ignore
        with db_session.get_session() as s:
            appt = s.query(models.Appointment).get(appointment_id)
            if not appt:
                return False
            appt.status = 'cancelled'
            s.commit()
            return True

    appt = _in_memory_appts.get(appointment_id)
    if not appt:
        return False
    appt['status'] = 'cancelled'
    return True


def reschedule_appointment(appointment_id: int, new_datetime: str) -> Dict[str, Any]:
    ndt = _parse_datetime(new_datetime)
    if _use_db():
        from ..database import db_session, models  # type: ignore
        with db_session.get_session() as s:
            appt = s.query(models.Appointment).get(appointment_id)
            if not appt:
                raise Exception("Appointment not found")
            if not check_availability(appt.doctor_id, new_datetime):
                raise Exception("New slot unavailable")
            appt.datetime = ndt
            s.commit()
            s.refresh(appt)
            return {"id": appt.id, "datetime": appt.datetime.isoformat()}

    appt = _in_memory_appts.get(appointment_id)
    if not appt:
        raise Exception("Appointment not found")
    if not check_availability(appt['doctor_id'], new_datetime):
        raise Exception("New slot unavailable")
    appt['datetime'] = ndt
    return {"id": appt['id'], "datetime": ndt.isoformat()}
