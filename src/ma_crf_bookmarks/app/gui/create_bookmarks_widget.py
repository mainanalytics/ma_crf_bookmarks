import os
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStyle,
    QVBoxLayout,
)

from ma_crf_bookmarks.gui.default_elements.default_style_values import (
    DefaultBorder,
    DefaultColors,
    DefaultFont,
)

if TYPE_CHECKING:
    from ma_crf_bookmarks.app.base_app import MainAppWindow


class CreateBookmarksWidget(QGroupBox):
    def __init__(
        self,
        parent_widget: "MainAppWindow",
        group_txt: str,
        label_txt: str,
        placeholder_txt: str,
        object_name: str,
        default_dir: str,
        label_width: int,
        btn_heigth: int,
        btn_width: int,
        icon_size: int,
        read_only: bool = False,
    ):
        super().__init__()

        self.parent_widget: MainAppWindow = parent_widget
        self.default_dir = default_dir

        self.setTitle(group_txt)
        self.setObjectName(object_name)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        label = QLabel(label_txt)
        label.setFixedWidth(label_width)

        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText(placeholder_txt)
        if read_only:
            self.text_box.setReadOnly(True)
        self.text_box.setFixedHeight(35)

        # analyis dir button
        btn = QPushButton()

        btn.setFixedHeight(btn_heigth)
        btn.setFixedWidth(btn_width)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogEnd)
        btn.setIcon(icon)
        btn.setIconSize(icon_size)

        btn.clicked.connect(self.select_output)

        select_layout = QHBoxLayout()
        select_layout.addWidget(label, alignment=Qt.AlignLeft)
        select_layout.addWidget(self.text_box)
        select_layout.addWidget(btn, alignment=Qt.AlignRight)

        select_layout.setSpacing(15)

        layout.addLayout(select_layout)

        self.set_style()

    def select_output(self):
        if self.parent_widget.crf_path:
            crf_dir = os.path.dirname(self.parent_widget.crf_path)
            base_name = ".".join(os.path.basename(self.parent_widget.crf_path).split(".")[:-1])
            print(base_name)
            file_name = os.path.join(crf_dir, base_name + "_bookmarks.pdf")
        else:
            file_name = os.path.join(self.default_dir, "crf_bookmarks.pdf")

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", file_name, "PDF Files (*.pdf);"
        )

        if file_path:
            self.text_box.setText(file_path)

    def set_style(self):
        self.setStyleSheet(f"""
                           QLabel{{
                                color: {DefaultColors.pure_black.value};
                                font-size: 18px;
                                font-weight: normal;
                                font-style: normal;
                                font-family: {DefaultFont.family.value};
                            }}
                            QGroupBox{{
                                color: {DefaultColors.pure_black.value};
                                font-size: 20px;
                                font-weight: bold;
                                font-style: normal;
                                font-family: {DefaultFont.family.value};
                                padding: {DefaultBorder.padding.value}px;
                                border-radius: {DefaultBorder.radius.value}px;
                                border:2px solid black;
                                margin-top: 10px;
                            }}
                            QGroupBox::title{{
                                subcontrol-origin: margin;
                                subcontrol-position: top left;
                                padding: 0 0px;
                                left: 15px;
                                top: -0px;
                            }}
                            QPushButton{{
                                background-color: {DefaultColors.light_grey.value};
                                border: none;
                                border-radius: {DefaultBorder.radius.value}px;
                                font-size: 15px;
                                font-weight: normal;
                                font-style: normal;
                            }}
                            QPushButton:hover{{
                                background-color: {DefaultColors.dark_blue.value};
                            }}
                            QLineEdit{{
                                background-color: {DefaultColors.light_grey.value};
                                color: {DefaultColors.pure_black.value};
                                font-size: 15px;
                                font-weight: normal;
                                font-style: normal;
                                font-family: {DefaultFont.family.value};
                            }}
                            """)
