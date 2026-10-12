from datetime import datetime

from ..models.event import MedicationEvent

def check_interval(session, treatment_id):
    last_event = (
        session.query(MedicationEvent)
        .filter(
            MedicationEvent.treatment_id == treatment_id
        )
        .order_by(
            MedicationEvent.time.desc()
        )
        .first()
    )

    if not last_event:
        return None

    treatment = last_event.treatment

    now = datetime.now()
    elapsed = (now - last_event.time)
    elapsed_hours = (elapsed.total_seconds() / 3600)

    required = treatment.interval_hours

    return {
        "last_time" : last_event.time,
        "elapsed_hours" : round(elapsed_hours, 1),
        "required_hours" : required,
        "can_take" : (elapsed_hours >= required)
    }   