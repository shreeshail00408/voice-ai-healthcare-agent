from celery import Celery
import os

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app = Celery('workers', broker=REDIS_URL, backend=REDIS_URL)


@app.task
def send_reminder(appointment_id: int):
    # lookup appointment and patient, then initiate call or SMS
    print(f"[Celery] Sending reminder for appointment {appointment_id}")
    return True
