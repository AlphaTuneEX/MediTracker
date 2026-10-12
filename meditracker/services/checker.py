from datetime import datetime, timedelta, date

def check_interval(session, treatment, current_time = None):
    from meditracker.models.event import MedicationEvent # type: ignore

    if current_time is None:
        current_time = datetime.now()

    last_event = (
        session.query(MedicationEvent)
        .filter(
            MedicationEvent.treatment_id == treatment.id
        )
        .order_by(
            MedicationEvent.time.desc()
        )
        .first()
    )

    if last_event is None:
        return{
            "allowed" : True,
            "last_time" : None,
            "elapsed_hours" : None,
            "required_hours" : treatment.interval_hours
        }

    elapsed = (current_time - last_event.time).total_seconds() / 3600

    return {
        "allowed" : elapsed >= treatment.interval_hours,
        "last_time" : last_event.time,
        "elapsed_hours" : round(elapsed, 2),
        "required_hours" : treatment.interval_hours
    }

def check_event_interval(session, treatment, event_time):
    from meditracker.models.event import MedicationEvent # type: ignore

    events = (
        session.query(MedicationEvent)
        .filter(
            MedicationEvent.treatment_id == treatment.id
        )
        .order_by(
            MedicationEvent.time
        )
        .all()
    )

    warnings = []

    for event in events:
        diff = abs(
            (event_time - event.time).total_seconds() / 3600
        )

        if diff < treatment.interval_hours:
            warnings.append(
                {
                    "time" : event.time,
                    "interval" : round(diff, 2)
                }
            )

    return {
        "allowed" : len(warnings) == 0,
        "warnings" : warnings
    }

def check_daily_dose(session, treatment, date):
    from meditracker.models.event import MedicationEvent # type: ignore

    events = (
        session.query(MedicationEvent)
        .filter(
            MedicationEvent.treatment_id == treatment.id,
            MedicationEvent.time >= date,
            MedicationEvent.time < date + timedelta(days = 1)
        )
        .all()
    )

    total = 0

    for event in events:
        total += (treatment.drug.dose * event.amount)

    ingredient = (treatment.drug.ingredient)

    return {
        "ingredient" : ingredient.name,
        "dose" : total,
        "maximum" : ingredient.maximum_dose,
        "percent" : round(total / ingredient.maximum_dose * 100, 1),
        "allowed" : total <= ingredient.maximum_dose
    }