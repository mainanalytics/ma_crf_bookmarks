import os
from typing import TYPE_CHECKING

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedLayout,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ma_pytemp.gui.default_elements.default_style_values import (
    DefaultBorder,
    DefaultColors,
)
from ma_pytemp.gui.msg_box import DefaultMsgBox
from ma_pytemp.logic.demo_logic import MainLogic

if TYPE_CHECKING:
    from ma_pytemp.app.base_app import BaseApp


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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        icon_size = QSize(35, 35)
        btn_heigth = 60
        btn_width = 60
        label_width = 150

        # dir part
        dir_box = QGroupBox()
        dir_layout = QVBoxLayout(dir_box)
        layout.addWidget(dir_box)

        dir_box_label = QLabel("Select Demo Folder")
        dir_box_label.setObjectName("box_label")
        dir_layout.addWidget(dir_box_label)

        analysis_dir = QLabel("Demo Directory")
        analysis_dir.setFixedWidth(label_width)
        self.demo_dir_input_box = QLineEdit()
        self.demo_dir_input_box.setPlaceholderText("...")
        self.demo_dir_input_box.setReadOnly(True)
        self.demo_dir_input_box.setStyleSheet(
            "QLineEdit[readOnly='true'] { background-color: #E0E0E0; }"
        )

        # analyis dir button
        btn_browse = QPushButton()
        btn_browse.setObjectName("btn_browse")
        btn_browse.setFixedHeight(btn_heigth)
        btn_browse.setFixedWidth(btn_width)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        btn_browse.setIcon(icon)
        btn_browse.setIconSize(icon_size)
        btn_browse.clicked.connect(self.btn_browse_clicked)

        directory_layout = QHBoxLayout()
        directory_layout.addWidget(analysis_dir)
        directory_layout.addWidget(self.demo_dir_input_box)
        directory_layout.addWidget(btn_browse)
        dir_layout.addLayout(directory_layout)
        dir_layout.addStretch(1)

        # logic part
        logic_box = QGroupBox()
        logic_layout = QVBoxLayout(logic_box)
        layout.addWidget(logic_box)
        # logic_layout.addStretch(1)

        logic_box_label = QLabel("Computation heavy logic")
        logic_box_label.setObjectName("box_label")
        logic_layout.addWidget(logic_box_label)

        self.result_label = QLabel("Prime factors:")
        self.result_label.setFixedWidth(label_width)
        self.demo_logic_input_box = QLineEdit()
        self.demo_logic_input_box.setPlaceholderText("input")

        # logic button
        self.btn_stack = QStackedLayout()
        self.btn_container = QWidget()
        self.btn_container.setLayout(self.btn_stack)

        self.btn_start_logic = QToolButton()
        self.btn_start_logic.setObjectName("btn_logic")
        font = QFont()
        font.setPointSize(12)
        self.btn_start_logic.setFont(font)

        self.btn_start_logic.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_start_logic.setFixedHeight(btn_heigth)
        self.btn_start_logic.setFixedWidth(btn_width)
        self.btn_start_logic.setIconSize(icon_size)
        self.btn_start_logic.setText("Start")
        logic_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        self.btn_start_logic.setIcon(logic_icon)
        self.btn_start_logic.clicked.connect(self.btn_start_clicked)

        # abort button
        self.btn_abort_logic = QToolButton()
        self.btn_abort_logic.setObjectName("btn_logic")
        font = QFont()
        font.setPointSize(12)
        self.btn_abort_logic.setFont(font)

        self.btn_abort_logic.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_abort_logic.setFixedHeight(btn_heigth)
        self.btn_abort_logic.setFixedWidth(btn_width)
        self.btn_abort_logic.setIconSize(icon_size)
        self.btn_abort_logic.setText("Abort")
        abort_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserStop)
        self.btn_abort_logic.setIcon(abort_icon)
        self.btn_abort_logic.clicked.connect(self.base_app.abort_thread)

        self.btn_stack.setCurrentIndex(0)
        self.btn_stack.addWidget(self.btn_start_logic)
        self.btn_stack.addWidget(self.btn_abort_logic)

        # add al logic widgets
        logic_level2_layout = QHBoxLayout()
        logic_level2_layout.addWidget(self.result_label)
        logic_level2_layout.addWidget(self.demo_logic_input_box)
        logic_level2_layout.addWidget(self.btn_container, alignment=Qt.AlignRight)

        logic_layout.addLayout(logic_level2_layout)
        logic_layout.addStretch(1)

        self.set_style()

    def btn_browse_clicked(self):
        folder = QFileDialog.getExistingDirectory(parent=self, caption="Select Demo Folder")

        folder = os.path.normpath(folder)
        self.demo_dir_input_box.setText(folder)

    def btn_start_clicked(self):
        try:
            input_value = int(self.demo_logic_input_box.text())
        except Exception as _:
            msg_box: DefaultMsgBox = DefaultMsgBox(
                parent_window=self,
                title="Input Missing",
                msg="Please provide numeric input",
                btn_type="ok",
            )
            msg_box.exec()
            return

        self.btn_stack.setCurrentIndex(1)

        if self.logger:
            self.logger.info("SYS  | Start logic, with input %s.", str(input_value))

        logic = MainLogic()

        self.base_app.main_window.status_bar_handler.start_spinner(
            txt="Logic running", freq=300, timeout=None, spinner_symbols=["⟳", "⟲"]
        )

        # run logic
        self.base_app.run_thread(
            func=lambda: logic.start_logic(input_value=input_value),
            on_return=self.on_finished,
        )

    def on_finished(self, result):
        self.btn_stack.setCurrentIndex(0)

        if self.logger:
            self.logger.info("SYS  | Finished logic. Result: %s.", result)

        self.demo_logic_input_box.setText(f"{result}")
        self.base_app.main_window.status_bar_handler.end_spinner()
        self.base_app.main_window.status_bar_handler.update_status_bar("Logic finished", 5000)
        msg_box_ok: DefaultMsgBox = DefaultMsgBox(
            parent_window=self, title="Logic", msg="Computation finished.", btn_type="ok"
        )
        msg_box_ok.exec()

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
                                background-color: {DefaultColors.light_grey.value};
                                border: none;
                                border-radius: {DefaultBorder.radius.value}px;
                                font-weight: normal;
                                font-style: normal;
                            }}
                            QToolButton:hover{{
                                background-color: {DefaultColors.dark_blue.value};
                            }}
                            QPushButton#btn_browse{{
                                background-color: {DefaultColors.light_grey.value};
                                border: none;
                                border-radius: {DefaultBorder.radius.value}px;
                                font-size: 15px;
                                font-weight: normal;
                                font-style: normal;
                            }}
                            QPushButton#btn_browse:hover{{
                                background-color: {DefaultColors.dark_blue.value};
                            }}
                            """)
