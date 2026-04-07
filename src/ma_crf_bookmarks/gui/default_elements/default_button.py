from typing import Optional

from PySide6.QtWidgets import QPushButton

from ma_crf_bookmarks.gui.default_elements.default_style_values import (
    DefaultBorder,
    DefaultColors,
    DefaultFont,
)


class DefaultButton(QPushButton):
    def __init__(self, txt: str, fixed_size: Optional[list[int]] = None):
        super().__init__()

        self.setText(txt)
        if fixed_size:
            self.setFixedSize(fixed_size[0], fixed_size[1])

        self.setObjectName("defaultButton")

        self.set_style()

    def set_style(self):
        self.setStyleSheet(f"""
                            QWidget#defaultButton{{
                                background-color: {DefaultColors.dark_grey.value};
                                color: {DefaultColors.light_grey.value};
                                font-family: {DefaultFont.family.value};
                                font-size: {DefaultFont.size.value}px;
                                font-weight: bold;
                                font-style: normal;
                                padding: {DefaultBorder.padding.value}px;
                                border-radius: {DefaultBorder.radius.value}px;
                                border: none;
                            }}
                            QWidget#defaultButton:hover {{
                                background-color: {DefaultColors.dark_blue.value};
                                color: {DefaultColors.light_blue.value};
                            }}""")
