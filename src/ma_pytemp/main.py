import logging
import traceback

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCloseEvent, QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

from ma_pytemp.app.base_app import MainApp
from ma_pytemp.gui.body_widget import BodyWidget
from ma_pytemp.gui.default_elements.default_style_values import (
    DefaultColors,
    DefaultFont,
)
from ma_pytemp.gui.header_widget import HeaderWidget
from ma_pytemp.gui.logo_painter import scale_icon
from ma_pytemp.gui.status_bar_handler import StatusBarHandler
from ma_pytemp.utils.config import ConfigModel, load_config
from ma_pytemp.utils.hide_termina import hide_terminal
from ma_pytemp.utils.logger import create_log
from ma_pytemp.utils.resource_paths import resource_path
from ma_pytemp.utils.user import User


class MainWindow(QMainWindow):
    """
    Application main window
    """

    def __init__(
        self, config: ConfigModel, user: User, logger: logging.Logger, version: str, root_dir: str
    ):
        super().__init__()

        self.logger = logger
        self.config = config
        self.user = user
        self.version = version
        self.root_dir = root_dir

        self.setWindowTitle("GBS Template Advanced")
        self.setObjectName("mainWindow")
        self.setMinimumSize(QSize(config.userInterface.min_width, config.userInterface.min_height))
        self.set_style()

        # statusbar
        self.status_bar = self.create_status_bar()
        self.status_bar_handler = StatusBarHandler(self)

        # create widgets
        self.main_widget, self.main_layout = self.create_main_widget()

        self.header_widget = HeaderWidget(self)
        self.body_widget = BodyWidget(self)
        self.main_layout.addWidget(self.header_widget, alignment=Qt.AlignTop)
        self.main_layout.addWidget(self.body_widget, alignment=Qt.AlignTop)

        self.main_app = MainApp(self, self.config, self.user, self.logger, self.root_dir)
        self.main_layout.addWidget(self.main_app.app_window, alignment=Qt.AlignTop)

        if self.config.userInterface.hide_terminal:
            hide_terminal()

    def create_main_widget(self) -> tuple[QWidget, QVBoxLayout]:
        """Create midgets for the main window

        Returns:
            tuple[QWidget, QVBoxLayout]:
        """
        # create logo behind everything
        self.pixmap = QPixmap(resource_path("images/mainanalytics_Logo.png"))
        self.pixmap.setDevicePixelRatio(self.devicePixelRatioF())
        self.margin: int = 10  # distance from window edges
        self.scale_ratio: int = 0.2  # change size here (40%)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        # main_layout.addStretch()      # remove stretch
        main_layout.setAlignment(Qt.AlignTop)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        return main_widget, main_layout

    def create_status_bar(self):
        """Create status bar for the main window. This is the black box at the bottom"""
        status_bar = self.statusBar()
        status_bar.setStyleSheet(
            f"""
            background-color: {DefaultColors.dark_grey.value};
            color: {DefaultColors.light_grey.value};
            font-size: 15px;
            font-family: {DefaultFont.family.value};
            border-radius: 0px;
            border: none;
            """
        )
        status_bar.setFixedHeight(25)
        status_bar.showMessage("System Ready", 5000)  # Shows for 5 seconds
        user_label = QLabel(f"User: {self.user.user_id} | v{self.version}")
        user_label.setStyleSheet(f"""
                                 padding-right: 10px;
                                 color: {DefaultColors.light_grey.value};
                                 font-size: 15px;
                                 font-family: {DefaultFont.family.value};
                                 border-radius: 0px;
                                 border: none;
                                 """)
        status_bar.addPermanentWidget(user_label)
        return status_bar

    def set_style(self):
        """Style sheet for the main window"""
        self.setStyleSheet(f"""

            QWidget#mainWindow {{
                    background-color: {DefaultColors.light_grey.value};
                    color: {DefaultColors.pure_black.value};
                    font-family: {DefaultFont.family.value};
                    font-size: {DefaultFont.size.value}px;
                    font-weight: normal;
                    font-style: normal;
                    padding: 0px;
                    border-radius: none;
                    border: none;
                }}
            """)

    def paintEvent(self, event):
        """Creates the mainanalytics logo in the background"""
        super().paintEvent(event)
        scale_icon(self)

    def update_status_bar(self, txt: str, timeout: int = None):
        """Set status bar massage

        Args:
            txt (str): message to be displayed in the statusbar
            timeout (int, optional): Time in seconds to display the massage
        """
        if timeout:
            self.status_bar.showMessage(txt, timeout)
        else:
            self.status_bar.showMessage(txt)

    def closeEvent(self, event: QCloseEvent):
        """Called by colsing the application"""

        if self.logger:
            self.logger.info("SYS  | Tool closed.")

        event.accept()  # allow closing


class Main:
    """
    Main class. Creats GUI and calls logic
    """

    def __init__(self):
        """
        Initialise main object. Creats tk inter instance, and log
        """

        root_dir = "."
        version: str = "1.0.0"

        config, path = load_config(path="config/template-config.yml")
        if config.logging.active:
            self.logger, self.log_path = create_log(config)
            self.logger.info("SYS  | Used config file: %s.", path)
        else:
            self.logger = None

        user: User = User(config, root_dir, self.logger)

        # load gui basics
        self.app = QApplication()

        # set icon
        self.app.setWindowIcon(QIcon(resource_path("ma.ico")))

        self.mainwindow = MainWindow(
            config=config, user=user, logger=self.logger, version=version, root_dir=root_dir
        )

    def main(self):
        """
        Starting GUI and logic
        """
        if self.logger:
            self.logger.info("SYS  | Started ma-pytemp demo.")

        self.mainwindow.show()
        self.app.exec()


if __name__ == "__main__":
    try:
        main = Main()
        main.main()

    except Exception as e:
        print(e)
        traceback.print_exc()
        # time.sleep(30)  # sleep a short while to make the error readable
