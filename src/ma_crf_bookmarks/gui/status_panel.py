from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class StatusPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(800)
        self.setStyleSheet("background-color: #3a3a3a; color: white;")

        right_layout = QVBoxLayout(self)
        right_layout.addWidget(QLabel("Selection Panel"))
        right_layout.addWidget(QLabel("Declare Analysis"))
        right_layout.addWidget(QLabel("Activity Log"))
        right_layout.addStretch()

        self.setVisible(True)

    def toggle(self):
        self.setVisible(not self.isVisible())
