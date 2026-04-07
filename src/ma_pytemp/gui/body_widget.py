from typing import TYPE_CHECKING

from PySide6.QtWidgets import QHBoxLayout, QWidget

from ma_pytemp.gui.default_elements.default_button import DefaultButton
from ma_pytemp.gui.default_elements.default_label import DefaultLabel

if TYPE_CHECKING:
    from ma_pytemp.main import MainWindow


class BodyWidget(QWidget):
    def __init__(self, main_window: "MainWindow"):
        super().__init__()

        self.main_window: MainWindow = main_window

        self.setObjectName("bodyWidget")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.counter = 0

        self.default_label = DefaultLabel(
            txt=f"Button clicked\n{self.counter}", fixed_size=[150, 150]
        )
        layout.addWidget(self.default_label)

        demo_button = DefaultButton(txt="Click me", fixed_size=[150, 150])
        demo_button.clicked.connect(self.on_button_clicked)
        layout.addWidget(demo_button)

    def on_button_clicked(self):
        self.counter += 1
        self.main_window.update_status_bar("Button clicked", 5000)  # Shows for 5 seconds
        self.default_label.setText(f"Button clicked\n{self.counter}")
