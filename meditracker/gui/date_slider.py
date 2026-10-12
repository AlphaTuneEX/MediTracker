from datetime import date, timedelta

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget


WEEKDAYS = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


class DateCard(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = date.today()
        self.selected = False
        self.is_today = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumWidth(76)
        self.setMinimumHeight(108)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        card = QRectF(3, 17, self.width() - 6, self.height() - 20)
        if self.selected:
            painter.setBrush(QColor("#659287"))
            painter.setPen(QPen(QColor("#E6F2DD"), 2))
        else:
            painter.setBrush(QColor(101, 146, 135, 70))
            painter.setPen(QPen(QColor(230, 242, 221, 80), 1))
        painter.drawRoundedRect(card, 9, 9)

        if self.is_today:
            painter.setPen(QColor("#18312B"))
            painter.setFont(QFont("Microsoft YaHei UI", 8, QFont.Weight.DemiBold))
            painter.drawText(QRectF(0, 0, self.width(), 16), Qt.AlignmentFlag.AlignCenter, "今天")

        ink = QColor("#FFFFFF") if self.selected else QColor("#E6F2DD")
        painter.setPen(ink)
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        painter.drawText(QRectF(0, 23, self.width(), 17), Qt.AlignmentFlag.AlignCenter, MONTHS[self.value.month - 1])
        painter.setFont(QFont("Georgia", 24, QFont.Weight.Bold))
        painter.drawText(QRectF(0, 36, self.width(), 36), Qt.AlignmentFlag.AlignCenter, f"{self.value.day:02d}")
        painter.setFont(QFont("Microsoft YaHei UI", 8, QFont.Weight.Medium))
        painter.drawText(QRectF(0, self.height() - 25, self.width(), 18), Qt.AlignmentFlag.AlignCenter,
                         WEEKDAYS[self.value.weekday()])


class DateSlider(QWidget):
    date_changed = Signal(date)
    today_requested = Signal()
    calendar_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_date = date.today()
        self._cards = []
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 4, 16, 6)
        layout.setSpacing(7)
        self.today_button = QPushButton("今天")
        self.today_button.setObjectName("shortcut")
        self.today_button.setFixedWidth(50)
        self.today_button.clicked.connect(self.today_requested)
        layout.addWidget(self.today_button)
        for offset in range(-5, 6):
            card = DateCard()
            card.clicked.connect(lambda checked=False, value=offset: self.set_date(
                self.current_date + timedelta(days=value)))
            layout.addWidget(card, 1)
            self._cards.append(card)
        self.calendar_button = QPushButton("日历")
        self.calendar_button.setObjectName("shortcut")
        self.calendar_button.setFixedWidth(50)
        self.calendar_button.clicked.connect(self.calendar_requested)
        layout.addWidget(self.calendar_button)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setStyleSheet("""
            DateSlider { background: #6AAD9D; }
            QPushButton#shortcut { color: #E6F2DD; background: #659287;
                border: 1px solid rgba(230,242,221,170); border-radius: 8px;
                min-height: 42px; font-weight: 600; }
            QPushButton#shortcut:hover { border-color: #E6F2DD; background: #587F76; }
        """)
        self._refresh()

    def set_date(self, value, emit=True):
        changed = value != self.current_date
        self.current_date = value
        self._refresh()
        if emit and changed:
            self.date_changed.emit(value)

    def previous_day(self):
        self.set_date(self.current_date - timedelta(days=1))

    def next_day(self):
        self.set_date(self.current_date + timedelta(days=1))

    def _refresh(self):
        today = date.today()
        for offset, card in zip(range(-5, 6), self._cards):
            card.value = self.current_date + timedelta(days=offset)
            card.selected = offset == 0
            card.is_today = card.value == today
            card.update()

    def wheelEvent(self, event):
        self.previous_day() if event.angleDelta().y() > 0 else self.next_day()
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.previous_day()
        elif event.key() == Qt.Key.Key_Right:
            self.next_day()
        else:
            super().keyPressEvent(event)
