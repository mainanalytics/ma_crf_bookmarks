from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget

from ma_crf_bookmarks.gui.default_elements.default_label import DefaultLabel
from ma_crf_bookmarks.gui.default_elements.default_style_values import DefaultBorder, DefaultColors

if TYPE_CHECKING:
    from ma_crf_bookmarks.main import MainWindow


class HeaderWidget(QWidget):
    def __init__(self, main_window: "MainWindow"):
        super().__init__()

        self.main_window: MainWindow = main_window

        self.setObjectName("headerWidget")
        self.setFixedHeight(80)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addStretch()

        frame = QFrame()
        frame.setObjectName("headerFrame")
        frame_layout = QHBoxLayout(frame)
        frame_layout.setSpacing(10)
        # frame_layout.addStretch()

        # Icon
        # self.icon_label = QLabel()
        # icon = self.style().standardIcon(QStyle.SP_MediaPlay,)
        # icon = QIcon(resource_path("images/Python-logo-notext.svg.png"))  # path to your icon
        # self.icon_label.setPixmap(icon.pixmap(40, 40))
        # frame_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

        # Text
        self.text_label = DefaultLabel("CRF Bookmark Tool")
        self.text_label.setObjectName("headerLabel")

        frame_layout.addWidget(self.text_label, alignment=Qt.AlignCenter)

        layout.addWidget(frame, alignment=Qt.AlignCenter)

        self.set_style()

    def set_style(self):
        self.setStyleSheet(f"""
                            QWidget#headerFrame{{
                                background-color: {DefaultColors.background.value};
                                color: {DefaultColors.pure_black.value};
                                font-size: 20px;
                                font-weight: bold;
                                font-style: normal;
                                padding: {DefaultBorder.padding.value}px;
                                border-radius: {DefaultBorder.radius.value}px;
                                border: none;
                            }}
                            QWidget#headerLabel{{
                                background-color: {DefaultColors.background.value};
                                color: {DefaultColors.pure_black.value};
                                font-size: 30px;
                                font-weight: bold;
                                font-style: normal;
                                padding: {DefaultBorder.padding.value}px;
                                border-radius: {DefaultBorder.radius.value}px;
                                border: none;
                            }}
                            """)
