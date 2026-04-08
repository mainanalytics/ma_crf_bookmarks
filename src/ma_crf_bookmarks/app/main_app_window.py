import os
import traceback
from typing import TYPE_CHECKING

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ma_crf_bookmarks.app.gui.output_file_widget import OutputFileWidget
from ma_crf_bookmarks.app.gui.select_file_widget import SelectFileWidget
from ma_crf_bookmarks.gui.default_elements.default_style_values import (
    DefaultBorder,
    DefaultColors,
)
from ma_crf_bookmarks.gui.msg_box import DefaultMsgBox
from ma_crf_bookmarks.logic.bookmark_logic import MainLogic

if TYPE_CHECKING:
    from ma_crf_bookmarks.app.base_app import BaseApp


class MainAppWindow(QWidget):
    """Demo class to showcase where main logic should be stored. Reuse this code"""

    def __init__(self, base_app: "BaseApp"):
        """
        Main menue

        Parameters
        ----------
        base_app : BaseApp
            handles all communication to main app
        """
        super().__init__()

        self.base_app: BaseApp = base_app
        self.config = base_app.config
        self.logger = base_app.logger

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        icon_size = QSize(50, 50)
        btn_heigth = 85
        btn_width = 85
        label_width = 90
        default_dir = os.path.normpath(self.config.bookmark.default_dir)

        self.sds_path: str = None
        self.crf_path: str = None
        self.output_path: str = None

        # select part
        self.select_crf_widget = SelectFileWidget(
            parent_widget=self,
            group_txt="CRF",
            label_txt="select CRF:",
            placeholder_txt="...",
            object_name="select_CRF",
            default_dir=default_dir,
            file_format="pdf",
            label_width=label_width,
            btn_heigth=btn_heigth,
            btn_width=btn_width,
            icon_size=icon_size,
        )
        layout.addWidget(self.select_crf_widget)

        self.select_sds_widget = SelectFileWidget(
            parent_widget=self,
            group_txt="Study Definition Spec (SDS)",
            label_txt="select SDS",
            placeholder_txt="...",
            object_name="select_SDS",
            default_dir=default_dir,
            file_format="xlsx",
            label_width=label_width,
            btn_heigth=btn_heigth,
            btn_width=btn_width,
            icon_size=icon_size,
        )
        layout.addWidget(self.select_sds_widget)

        self.select_output_widget = OutputFileWidget(
            parent_widget=self,
            group_txt="Output CRF",
            label_txt="output",
            placeholder_txt="...",
            object_name="select_output",
            default_dir=default_dir,
            label_width=label_width,
            btn_heigth=btn_heigth,
            btn_width=btn_width,
            icon_size=icon_size,
        )
        layout.addWidget(self.select_output_widget)

        # Create aCRF btn
        self.start_btn = QToolButton()
        self.start_btn.setObjectName("start_btn")
        font = QFont("Calibri", 20)
        font.setBold(True)
        font.setPointSize(18)
        self.start_btn.setFont(font)

        self.start_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.start_btn.setFixedHeight(btn_heigth + 40)
        self.start_btn.setFixedWidth(btn_width + 40)
        self.start_btn.setIconSize(QSize(70, 70))
        self.start_btn.setText("Create\nBookmarks")
        logic_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        self.start_btn.setIcon(logic_icon)
        self.start_btn.clicked.connect(self.btn_start_clicked)
        self.start_btn.setEnabled(False)

        # set spacing between button and select
        layout.setSpacing(30)
        layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)

        self.set_style()

    def btn_start_clicked(self):
        self.start_btn.setEnabled(False)

        if not self.select_output_widget.valid_output():
            msg_box: DefaultMsgBox = DefaultMsgBox(
                parent_window=self,
                title="Invalid Outputfile",
                msg="Please enter valid output file",
                btn_type="ok",
            )
            msg_box.exec()
            return

        self.output_path = os.path.normpath(self.select_output_widget.text_box.text())
        if self.logger:
            self.logger.info("SYS  | Input CRF:\t\t %s", self.crf_path)
            self.logger.info("SYS  | Input SDS:\t\t %s", self.sds_path)
            self.logger.info("SYS  | Output CRF:\t %s", self.output_path)
            self.logger.info("SYS  | Start creating bookmarks")

        logic = MainLogic()

        self.base_app.main_window.status_bar_handler.start_spinner(
            txt="Creating bookmarks", freq=300, timeout=None, spinner_symbols=["⟳", "⟲"]
        )

        try:
            self.base_app.run_thread(
                func=lambda: logic.start_logic(
                    crf_path=self.crf_path, sds_path=self.sds_path, output_path=self.output_path
                ),
                on_return=self.on_finished,
            )
        except Exception as e:
            msg_box: DefaultMsgBox = DefaultMsgBox(
                parent_window=self,
                title="Error",
                msg=str(e),
                btn_type="ok",
            )
            msg_box.exec()
            self.logger(traceback.print_exc())

    def on_finished(self, result):
        _ = result
        if self.logger:
            self.logger.info("SYS  | Created bookmarks.")

        self.base_app.main_window.status_bar_handler.end_spinner()
        self.base_app.main_window.status_bar_handler.update_status_bar("Bookmarks finished", 5000)

        msg_box_ok: DefaultMsgBox = DefaultMsgBox(
            parent_window=self,
            title="Finished",
            msg=f"CRF created:\n{self.output_path}",
            btn_type="ok",
        )
        msg_box_ok.exec()
        self.start_btn.setEnabled(True)

    def set_style(self):
        self.setStyleSheet(f""" QLabel{{
                                color: {DefaultColors.pure_black.value};
                                font-size: 15px;
                                font-weight: normal;
                                font-style: normal;
                                padding: {DefaultBorder.padding.value}px;
                                border-radius: {DefaultBorder.radius.value}px;
                                border: none;
                            }}
                            QLabel#box_label{{
                                color: {DefaultColors.pure_black.value};
                                font-size: 15px;
                                font-weight: bold;
                                font-style: normal;
                                padding: {DefaultBorder.padding.value}px;
                                border-radius: {DefaultBorder.radius.value}px;
                                border: none;
                            }}
                            QToolButton{{
                                background-color: {DefaultColors.background.value};
                                border: none;
                                border-radius: {DefaultBorder.radius.value}px;
                            }}
                            QToolButton:hover{{
                                background-color: {DefaultColors.dark_blue.value};
                            }}
                            """)
