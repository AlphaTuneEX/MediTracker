from datetime import datetime

from meditracker.services.checker import check_daily_dose, check_interval, check_event_interval # type: ignore

def add_medication_event(
        session,
        treatment,
        amount = 1,
        note = None,
        time = None,
        force = False
):

    from meditracker.models.event import MedicationEvent # type: ignore

    if time is None:
        time = datetime.now()

    warnings = []

    interval_result = check_event_interval(session, treatment, time)
    if not interval_result["allowed"]:
        warnings.append(
            f"服用药物间隔不足，必须等待 {treatment.interval_hours} 小时"
        )

    dose_result = check_daily_dose(session, treatment, time.date())
    next_dose = (treatment.drug.dose * amount)
    if (dose_result["dose"] + next_dose > dose_result["maximum"]):
        warnings.append(
            f"超过最大剂量 {dose_result['dose']} / {dose_result['maximum']}{treatment.drug.unit}"
        )

    if warnings and not force:
        return {
            "success" : False,
            "warnings" : warnings
        }

    event = MedicationEvent(
        time = time,
        treatment_id = treatment.id,
        amount = amount,
        note = note
    )

    session.add(event)
    session.commit()

    return {
        "success" : True,
        "event" : event,
        "warnings" : warnings
    }