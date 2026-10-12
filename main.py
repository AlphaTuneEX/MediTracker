from datetime import datetime
# Meditracker
from meditracker.database import Base, engine, Session
from meditracker.debug_function import ECHO
# Meditracker.models
from meditracker.models.ingredient import Ingredient
from meditracker.models.drug import Drug
from meditracker.models.treatment import Treatment
from meditracker.models.event import MedicationEvent
# Applications
import os
import sys
from PySide6.QtWidgets import QApplication
from meditracker.gui.main_window import MainWindow

Base.metadata.create_all(engine)
ECHO("数据库已创建")

app = QApplication(sys.argv)
window = MainWindow()
ECHO("窗口尝试创建")

window.show()
ECHO("窗口尝试显示")

sys.exit(app.exec())