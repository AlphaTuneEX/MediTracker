from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QProgressBar, QVBoxLayout, QWidget


class SummaryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        outer = QHBoxLayout(self)
        outer.setContentsMargins(20, 18, 20, 18)
        outer.setSpacing(12)
        self.count_value = self._metric(outer, "服药次数", "0")
        self.last_value = self._metric(outer, "最近服药", "—")

        dose_card = QFrame(objectName="card")
        dose_layout = QVBoxLayout(dose_card)
        dose_layout.setContentsMargins(16, 10, 16, 10)
        dose_layout.setSpacing(5)
        self.dose_title = QLabel("剂量概览", objectName="label")
        self.dose_value = QLabel("暂无记录", objectName="doseValue")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        dose_layout.addWidget(self.dose_title)
        dose_layout.addWidget(self.dose_value)
        dose_layout.addWidget(self.progress)
        outer.addWidget(dose_card, 2)
        self.setStyleSheet("""
            SummaryWidget { background: #659287; }
            QFrame#card { background: rgba(255,255,255,18); border: 1px solid rgba(230,242,221,120); border-radius: 10px; }
            QLabel#label { color: #D8EADF; font-size: 11px; }
            QLabel#value { color: white; font-size: 24px; font-weight: 600; }
            QLabel#doseValue { color: white; font-size: 14px; font-weight: 500; }
            QProgressBar { background: rgba(230,242,221,45); border: none; border-radius: 4px; max-height: 8px; }
            QProgressBar::chunk { background: #20D6B1; border-radius: 4px; }
        """)

    def _metric(self, layout, title, value):
        card = QFrame(objectName="card")
        box = QVBoxLayout(card)
        box.setContentsMargins(16, 10, 16, 10)
        label = QLabel(title, objectName="label")
        output = QLabel(value, objectName="value")
        box.addWidget(label)
        box.addWidget(output, 1, Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(card, 1)
        return output

    def set_summary(self, summary, doses, selected_date=None):
        self.count_value.setText(str(summary.get("count", 0)))
        last = summary.get("last_time")
        self.last_value.setText(last.strftime("%H:%M") if last else "—")
        if not doses:
            self.dose_value.setText("暂无记录")
            self.progress.setValue(0)
            self.progress.setStyleSheet("")
            return
        name, data = max(doses.items(), key=lambda item: item[1].get("percent", 0))
        percent = float(data.get("percent", 0))
        self.dose_value.setText(f"{name}  {data['current']:g} / {data['maximum']:g} {data['unit']}  ·  {percent:g}%")
        self.progress.setValue(min(100, round(percent)))
        color = "#FF6B6B" if percent > 100 else "#FFD54A" if percent >= 85 else "#20D6B1"
        self.progress.setStyleSheet(f"QProgressBar::chunk {{ background: {color}; border-radius: 4px; }}")
