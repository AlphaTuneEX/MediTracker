from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCalendarWidget, QDialog, QLabel, QMainWindow, QVBoxLayout, QWidget

from meditracker.database import Session
from meditracker.services.dose_summary import get_daily_dose_summary
from meditracker.services.summary import get_daily_summary
from meditracker.services.timeline import get_timeline

from .date_slider import DateSlider
from .summary_widget import SummaryWidget
from .timeline_widget import TimelineWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MediTracker")
        self.resize(1180, 840)
        self.setMinimumSize(900, 680)
        self._session = Session()
        self._build_ui()
        self.load_date(date.today())

    def _build_ui(self):
        root = QWidget(objectName="root")
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("M · E · D · I · T · R · A · C · K · E · R", objectName="title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(50)
        layout.addWidget(title)

        self.timeline = TimelineWidget()
        layout.addWidget(self.timeline, 1)

        self.date_slider = DateSlider()
        self.date_slider.setFixedHeight(122)
        self.date_slider.date_changed.connect(self.load_date)
        self.date_slider.today_requested.connect(self.go_to_today)
        self.date_slider.calendar_requested.connect(self.open_calendar)
        layout.addWidget(self.date_slider)

        self.summary = SummaryWidget()
        self.summary.setFixedHeight(150)
        layout.addWidget(self.summary)

        self.setStyleSheet("""
            QWidget#root { background: #88BDA4; }
            QLabel#title {
                background: #659287; color: white; font-size: 27px;
                font-weight: 600; letter-spacing: 4px;
            }
        """)

    def load_date(self, selected_date):
        try:
            timeline = get_timeline(self._session, selected_date)
            summary = get_daily_summary(timeline)
            doses = get_daily_dose_summary(self._session, selected_date)
        except Exception as exc:
            self._session.rollback()
            timeline, summary, doses = [], {"count": 0, "last_time": None, "ingredients": {}}, {}
            self.statusBar().showMessage(f"读取数据失败：{exc}", 6000)
        self.timeline.set_timeline(timeline, selected_date)
        self.summary.set_summary(summary, doses, selected_date)

    def go_to_today(self):
        self.date_slider.set_date(date.today())

    def open_calendar(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("选择日期")
        calendar = QCalendarWidget(dialog)
        calendar.setSelectedDate(self.date_slider.current_date)
        box = QVBoxLayout(dialog)
        box.addWidget(calendar)
        calendar.activated.connect(dialog.accept)
        if dialog.exec():
            self.date_slider.set_date(calendar.selectedDate().toPython())

    def closeEvent(self, event):
        self._session.close()
        super().closeEvent(event)
