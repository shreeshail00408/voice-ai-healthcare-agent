import pytest
from app.tools import scheduler_tools
import datetime


def test_check_availability_past():
    past = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
    assert not scheduler_tools.check_availability(doctor_id=1, datetime=past)


def test_check_availability_future():
    future = (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
    # With empty DB this should be True
    assert scheduler_tools.check_availability(doctor_id=1, datetime=future)
