from datetime import datetime, date

from ..models.event import MedicationEvent

def today_events(session):
    today = date.today()

    events = (
        session.query(
            MedicationEvent
        )
        .filter(
            MedicationEvent.time >= datetime.combine(
                today,
                datetime.min.time()
            )
        )
    .all()
    )

    return events

def cal_daily_dose(session):
    events = today_events(session)
    result = {}

    for event in events:
        drug = event.treatment.drug
        ingredient = drug.ingredient
        dose = (drug.dose * event.amount)
        name = ingredient.name

        if name not in result:
            result[name] = {
                "dose" : 0,
                "maximum" : ingredient.maximum_dose,
                "unit" : ingredient.unit
            }

        result [name]["dose"] += dose

    for name in result:
        item = result[name]
        item["percent"] = round(item["dose"] / item["maximum"] * 100, 1)

    return result