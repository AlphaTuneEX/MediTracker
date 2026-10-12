from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout

class OverviewPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("今日概览")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)