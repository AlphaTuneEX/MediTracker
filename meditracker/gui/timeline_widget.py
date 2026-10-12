from datetime import date, datetime

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPolygonF
from PySide6.QtWidgets import QWidget


class TimelineWidget(QWidget):
    BG = QColor("#88BDA4")
    INK = QColor("#E6F2DD")
    TRACK = QColor("#659287")
    ACCENT = QColor("#20D6B1")
    WARNING = QColor("#FFD54A")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(350)
        self._timeline = []
        self._date = date.today()
        self._selected_hour = datetime.now().hour
        now = datetime.now()
        self._selected_time = float(now.hour)
        self._dragging_selector = False
        self._clock = QTimer(self)
        self._clock.timeout.connect(self.update)
        self._clock.start(1000)

    def set_timeline(self, timeline, selected_date=None):
        self._timeline = timeline or []
        if selected_date:
            self._date = selected_date
        if self._timeline:
            self._selected_hour = self._timeline[-1]["time"].hour
            value = self._timeline[-1]["time"]
            self._selected_time = float(value.hour)
        elif self._date == date.today():
            now = datetime.now()
            self._selected_hour = now.hour
            self._selected_time = float(now.hour)
        self.update()

    def _main_rect(self):
        return QRectF(88, 112, max(100, self.width() - 176), 36)

    def _x_for_hour(self, hour):
        rect = self._main_rect()
        return rect.left() + rect.width() * hour / 24.0

    @staticmethod
    def _event_hour(item):
        value = item["time"]
        return value.hour + value.minute / 60.0 + value.second / 3600.0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), self.BG)
        self._paint_main_axis(painter)
        self._paint_hour_detail(painter)

    def _paint_main_axis(self, painter):
        rect = self._main_rect()
        y = rect.center().y()
        current = datetime.now()
        selected_time = self._selected_time

        painter.setPen(self.INK)
        painter.setFont(QFont("Segoe UI", 30, QFont.Weight.DemiBold))
        painter.drawText(QRectF(0, 12, self.width(), 44), Qt.AlignmentFlag.AlignCenter, current.strftime("%H:%M"))

        painter.setPen(QPen(self.TRACK, 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))
        # 过去日期为完整进度；今天走到当前时刻；未来日期保持空轨道。
        if self._date < date.today():
            painter.setPen(QPen(self.ACCENT, 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))
        elif self._date == date.today():
            day_progress = current.hour + current.minute / 60 + current.second / 3600
            painter.setPen(QPen(self.ACCENT, 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawLine(QPointF(rect.left(), y), QPointF(self._x_for_hour(day_progress), y))

            # 当前时刻：箭头尖端精确指向进度条上的实际位置。
            now_x = self._x_for_hour(day_progress)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#D93624"))
            painter.drawPolygon(QPolygonF([
                QPointF(now_x - 4, y - 22),
                QPointF(now_x + 4, y - 22),
                QPointF(now_x, y - 12),
            ]))

        for hour in range(25):
            x = self._x_for_hour(hour)
            radius = 6 if hour % 2 == 0 else 3
            painter.setBrush(self.INK)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(x, y), radius, radius)

            # 每个整点都显示，交错放置避免相邻文字重叠。
            painter.setPen(self.INK)
            painter.setFont(QFont("Segoe UI", 8, QFont.Weight.Medium))
            label_y = y - 37 if hour % 2 == 0 else y + 13
            painter.drawText(QRectF(x - 23, label_y, 46, 18), Qt.AlignmentFlag.AlignCenter,
                             f"{hour:02d}:00")

        # 选择框代表 [整点, 下一整点) 的小时区间，中心位于两个节点之间。
        selector_left = self._x_for_hour(selected_time)
        selector_right = self._x_for_hour(selected_time + 1.0)
        painter.setPen(QPen(self.WARNING, 2))
        painter.setBrush(QColor(255, 213, 74, 35))
        # 两条竖边严格落在相邻整点的 x 坐标，中心与轨道共用同一个 y。
        painter.drawRoundedRect(QRectF(selector_left, y - 15,
                                       selector_right - selector_left, 30), 5, 5)

        for item in self._timeline:
            # 24 小时轴上相邻分钟距离很小；用精确指针和时间文字避免与整点圆点混淆。
            x = self._x_for_hour(self._event_hour(item))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self.WARNING)
            painter.drawPolygon(QPolygonF([
                QPointF(x - 5, y - 18),
                QPointF(x + 5, y - 18),
                QPointF(x, y - 5),
            ]))
            event_text = item["time"].strftime("%H:%M")
            text_x = min(rect.right() - 48, max(rect.left(), x - 24))
            painter.setPen(QColor("#FFE37A"))
            painter.setFont(QFont("Segoe UI", 8, QFont.Weight.DemiBold))
            painter.drawText(QRectF(text_x, y - 38, 48, 16), Qt.AlignmentFlag.AlignCenter, event_text)

    def _paint_hour_detail(self, painter):
        left, top = 72, 184
        width, height = max(260, self.width() - 144), max(132, self.height() - top - 26)
        card = QRectF(left, top, width, height)
        painter.setPen(QPen(QColor(230, 242, 221, 105), 1))
        painter.setBrush(QColor(101, 146, 135, 75))
        painter.drawRoundedRect(card, 12, 12)

        painter.setPen(self.INK)
        painter.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        painter.drawText(QRectF(left + 18, top + 12, 180, 24), Qt.AlignmentFlag.AlignLeft,
                         f"{self._selected_hour:02d}:00 — {(self._selected_hour + 1):02d}:00")

        axis_left, axis_right, axis_y = left + 28, left + width - 28, top + 64
        painter.setPen(QPen(QColor("#B8D9CA"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(QPointF(axis_left, axis_y), QPointF(axis_right, axis_y))
        for minute in range(0, 61, 5):
            x = axis_left + (axis_right - axis_left) * minute / 60
            radius = 5 if minute % 15 == 0 else 2.5
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self.INK)
            painter.drawEllipse(QPointF(x, axis_y), radius, radius)
            if minute % 15 == 0:
                painter.setPen(QColor("#E6F2DD"))
                painter.setFont(QFont("Segoe UI", 8))
                label_hour = self._selected_hour + minute // 60
                label_minute = minute % 60
                painter.drawText(QRectF(x - 31, axis_y + 10, 62, 18), Qt.AlignmentFlag.AlignCenter,
                                 f"{label_hour:02d}:{label_minute:02d}")

        hour_events = [item for item in self._timeline if item["time"].hour == self._selected_hour]
        for index, item in enumerate(hour_events[:3]):
            minute = item["time"].minute + item["time"].second / 60.0
            x = axis_left + (axis_right - axis_left) * minute / 60
            painter.setPen(QPen(self.WARNING, 1.5))
            painter.drawLine(QPointF(x, axis_y - 2), QPointF(x, axis_y - 10))
            painter.setPen(QPen(QColor("#FFFFFF"), 1.5))
            painter.setBrush(self.WARNING)
            painter.drawEllipse(QPointF(x, axis_y - 13), 5.5, 5.5)
            label = f"{item['time']:%H:%M}  {item['drug']}  {item['dose']:g}{item['unit']}"
            painter.setPen(Qt.GlobalColor.white)
            painter.setFont(QFont("Segoe UI", 10))
            painter.drawText(QRectF(left + 22, top + 102 + index * 22, width - 44, 20), label)
        if not hour_events:
            painter.setPen(QColor(230, 242, 221, 150))
            painter.setFont(QFont("Segoe UI", 10))
            painter.drawText(QRectF(left, top + 102, width, 24), Qt.AlignmentFlag.AlignCenter, "这一小时没有服药记录")

    def _select_from_x(self, x):
        rect = self._main_rect()
        ratio = min(1.0, max(0.0, (x - rect.left()) / rect.width()))
        selected_hour = min(23, max(0, int(ratio * 24)))
        if selected_hour != self._selected_hour:
            self._selected_time = float(selected_hour)
            self._selected_hour = selected_hour
            self.update()

    def mousePressEvent(self, event):
        rect = self._main_rect()
        if event.button() == Qt.MouseButton.LeftButton and rect.adjusted(0, -22, 0, 22).contains(event.position()):
            self._dragging_selector = True
            self._select_from_x(event.position().x())
            self.grabMouse()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging_selector:
            self._select_from_x(event.position().x())
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._dragging_selector and event.button() == Qt.MouseButton.LeftButton:
            self._select_from_x(event.position().x())
            self._dragging_selector = False
            self.releaseMouse()
            event.accept()
            return
        super().mouseReleaseEvent(event)
