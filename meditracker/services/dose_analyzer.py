from datetime import date, datetime

from ..models.event import MedicationEvent

def analyze_daily_dose(session):
    today = date.today()

    events = (
        session.query(MedicationEvent)
        .filter(
            MedicationEvent.time >= datetime.combine(
                today,
                datetime.min.time()
            )
        )
        .all()
    )

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

        result[name]["dose"] += dose

    for name, item in result.items():
        item["percent"] = round(item["dose"] / item["maximum"] * 100, 1)

        if item["dose"] > item["maximum"]:
            item["status"] = "过量"
#           item["status"] = "+ 升天 +"

        elif item["percent"] >= 85:
            item["status"] = "危险"

        else:
            item["status"] = "正常"

    return result
