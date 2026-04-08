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


class SelectFileWidget(QGroupBox):
    def __init__(
        self,
        parent_widget: "MainAppWindow",
        group_txt: str,
        label_txt: str,
        placeholder_txt: str,
        object_name: str,
        default_dir: str,
        file_format: str,
        label_width: int,
        btn_heigth: int,
        btn_width: int,
        icon_size: int,
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
        self.text_box.setReadOnly(True)
        self.text_box.setFixedHeight(35)

        # analyis dir button
        btn = QPushButton()

        btn.setFixedHeight(btn_heigth)
        btn.setFixedWidth(btn_width)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogStart)
        btn.setIcon(icon)
        btn.setIconSize(icon_size)
        if file_format == "pdf":
            btn.clicked.connect(self.open_file_dialog_pdf)
        if file_format == "xlsx":
            btn.clicked.connect(self.open_file_dialog_xlsx)

        select_layout = QHBoxLayout()
        select_layout.addWidget(label, alignment=Qt.AlignLeft)
        select_layout.addWidget(self.text_box)
        select_layout.addWidget(btn, alignment=Qt.AlignRight)

        select_layout.setSpacing(15)

        layout.addLayout(select_layout)

        self.set_style()

    def open_file_dialog_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CRF file", self.default_dir, "PDF Files (*.pdf);"
        )

        if file_path:
            self.parent_widget.crf_path = os.path.normpath(file_path)
            self.text_box.setText(file_path)
        if (
            self.parent_widget.select_output_widget.valid_output()
            and self.parent_widget.crf_path
            and self.parent_widget.sds_path
        ):
            self.parent_widget.start_btn.setEnabled(True)

    def open_file_dialog_xlsx(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select SDS file", self.default_dir, "Excel Files (*.xlsx);"
        )
        if file_path:
            self.parent_widget.sds_path = os.path.normpath(file_path)
            self.text_box.setText(file_path)
        if (
            self.parent_widget.select_output_widget.valid_output()
            and self.parent_widget.crf_path
            and self.parent_widget.sds_path
        ):
            self.parent_widget.start_btn.setEnabled(True)

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
                            QLineEdit[readOnly='true'] {{
                                background-color: {DefaultColors.light_grey.value};
                                color: {DefaultColors.pure_black.value};
                                font-size: 15px;
                                font-weight: normal;
                                font-style: normal;
                                font-family: {DefaultFont.family.value};
                            }}
                            """)
