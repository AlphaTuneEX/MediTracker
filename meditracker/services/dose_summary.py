from datetime import datetime, timedelta
from collections import defaultdict

def get_daily_dose_summary(session, date):
    from meditracker.models.event import MedicationEvent # type: ignore

    start = datetime.combine(date, datetime.min.time())
    end = start + timedelta(days=1)

    events = (
        session.query(MedicationEvent)
        .filter(
            MedicationEvent.time >= start,
            MedicationEvent.time < end
        )
        .all()
    )

    summary = defaultdict(int)
    details = {}

    for event in events:
        treatment = event.treatment
        drug = treatment.drug
        ingredient = drug.ingredient
        dose = (drug.dose * event.amount)
        summary[ingredient.name] += dose
        details[ingredient.name] = {
            "maximum" : ingredient.maximum_dose,
            "unit" : ingredient.unit
        }

    result = {}

    for name, total in summary.items():
        maximum = details[name]["maximum"]
        percent = round(total / maximum * 100, 1)

        if total > maximum:
            status = "Overdose"

        elif percent >= 85:
            status = "Danger"

        else:
            status = "Normal"

        result[name] = {
            "current" : total,
            "maximum" : maximum,
            "percent" : percent,
            "unit" : details[name]["unit"],
            "status" : status
        }
        
    return result