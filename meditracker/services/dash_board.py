from datetime import datetime

from .dose_analyzer import analyze_daily_dose
from .interval_analyzer import check_interval

from ..models.event import MedicationEvent

from ..debug_function import ECHO

def get_dash_board(session, treatment_id):
    dose = analyze_daily_dose(session)
    interval = check_interval(session, treatment_id)
    events = get_today_events(session)

    return {
        "current_time" : datetime.now(),
        "dose" : dose,
        "interval" : interval,
        "events" : events
    }

def get_today_events(session):

    events = (
        session.query(MedicationEvent)
        .order_by(MedicationEvent.time)
        .all()
    )

    result = []

    for event in events:
        result.append(
            {
                "time": event.time,
                "drug": event.treatment.drug.name,
                "amount": event.amount,
                "note": event.note
            }
        )

    return result