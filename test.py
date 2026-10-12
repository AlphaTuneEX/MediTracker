from meditracker.database import Session
from meditracker.services.analyzer import today_events, cal_daily_dose
from meditracker.services.dose_analyzer import analyze_daily_dose
from meditracker.services.interval_analyzer import check_interval
from meditracker.services.summary import get_daily_summary
from meditracker.services.event_manager import add_medication_event
from meditracker.services.timeline import get_timeline
from meditracker.services.checker import check_daily_dose, check_interval
from meditracker.services.dose_summary import get_daily_dose_summary
from meditracker.models.treatment import Treatment
from meditracker.models.ingredient import Ingredient
from meditracker.models.drug import Drug

from meditracker.debug_function import ECHO

from datetime import date, datetime

session = Session()

ingredient = (
    session.query(Ingredient)
    .filter_by(name="阿莫西林")
    .first()
)

if ingredient is None:
    ingredient = Ingredient(
        name="阿莫西林",
        category="抗生素",
        maximum_dose=3000,
        unit="mg"
    )

    session.add(ingredient)
    session.commit()

drug_test = (
    session.query(Drug)
    .filter_by(name="Amoxi 1000 - 1 A Pharma")
    .first()
)

if drug_test is None:

    drug_test = Drug(
        name="Amoxi 1000 - 1 A Pharma",
        ingredient_id=ingredient.id,
        dose=1000,
        unit="mg"
    )

    session.add(drug_test)
    session.commit()

treatment = (
    session.query(Treatment)
    .filter_by(name="啥比智齿")
    .first()
)

if treatment is None:

    treatment = Treatment(
        name="啥比智齿",
        drug_id=drug_test.id,
        interval_hours=8,
        start_date=date.today()
    )

    session.add(treatment)
    session.commit()

result = add_medication_event(
    session,
    treatment,
    amount=1,
    note="补充记录",
    time=datetime.now()
)

ECHO(result)

result1 = check_interval(session, treatment)
ECHO(result1)

result2 = check_daily_dose(session, treatment, date.today())
ECHO(result2)

summary = get_daily_dose_summary(session, date.today())
ECHO(summary)

timeline = get_timeline(
    session,
    date.today()
)

data = get_timeline(
    session,
    date.today()
)

for e in data:
    ECHO(e)

for item in timeline:
    ECHO(item)