from datetime import datetime, date

from meditracker.database import Session
from meditracker.debug_function import ECHO
from meditracker.models.ingredient import Ingredient
from meditracker.models.drug import Drug
from meditracker.models.treatment import Treatment
from meditracker.models.event import MedicationEvent

session = Session()

# 成分录入
amoxicillin = Ingredient(
    name = "阿莫西林",
    category = "抗生素",
    maximum_dose = 3000,
    unit = "mg"
)

ibuprofen = Ingredient(
    name = "布洛芬",
    category = "止痛药",
    maximum_dose = 1200,
    unit = "mg"
)

session.add(amoxicillin)
session.add(ibuprofen)
session.commit()

# 药品录入
amoxi = Drug(
    name = "Amoxi 1000 - 1 A Pharma",
    ingredient = amoxicillin,
    dose = 1000,
    unit = "mg"
)

ibuflam = Drug(
    name = "Ibuflam akut",
    ingredient = ibuprofen,
    dose = 400,
    unit = "mg"
)

session.add(amoxi)
session.add(ibuflam)
session.commit()

# 治疗录入
treatment = Treatment(
    name = "牙齿感染治疗",
    drug = amoxi,
    interval_hours = 8,
    start_date = date.today()
)

session.add(treatment)
session.commit()

# 服药记录测试
event = MedicationEvent(
    time = datetime.now(),
    treatment = treatment,
    amount = 1,
    note = "Test"
)

session.add(event)
session.commit()

ECHO("测试数据录入成功")