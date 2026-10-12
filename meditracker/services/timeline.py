from datetime import datetime, timedelta


def get_day_range(date):
    start = datetime.combine(date, datetime.min.time())
    return start, start + timedelta(days=1)


def get_timeline(session, date):
    from meditracker.models.event import MedicationEvent  # type: ignore

    start, end = get_day_range(date)
    events = (
        session.query(MedicationEvent)
        .filter(MedicationEvent.time >= start, MedicationEvent.time < end)
        .order_by(MedicationEvent.time)
        .all()
    )
    timeline = []
    for event in events:
        treatment = event.treatment
        drug = treatment.drug
        ingredient = drug.ingredient
        hour = event.time.hour + event.time.minute / 60
        timeline.append({
            "id": event.id,
            "timestamp": event.time,
            "time": event.time,
            # 保留完整精度；GUI 负责按小时比例定位，不能提前舍入。
            "hour": hour,
            "type": "medication",
            "drug": drug.name,
            "ingredient": ingredient.name,
            "dose": drug.dose * event.amount,
            "unit": drug.unit,
            "note": event.note,
        })
    return timeline


def get_hour_timeline(timeline, hour):
    return [event for event in timeline if event["time"].hour == hour]
