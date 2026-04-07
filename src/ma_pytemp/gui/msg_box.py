from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
)

from ma_pytemp.gui.default_elements.default_style_values import (
    DefaultBorder,
    DefaultColors,
    DefaultFont,
)


class DefaultMsgBox(QMessageBox):
    """Default message box for pop up massages"""

    def __init__(self, parent_window: QWidget, title: str, msg: str, btn_type: str):
        """

        Args:
            parent_window (QWidget):
            title (str): The title text of the box
            msg (str): The body text of the box
            btn_type (str): Can be in ["OK", "yn_btn"], handles what type of buttons the box has
            btn_status (str, optional): Can be in ["INFO", "ERROR", "WARNING", "OK"],
                                        handles the displayed icon
        """
        super().__init__()

        self.compile_window: QWidget = parent_window
        self.setWindowTitle(title)
        self.setText(msg)

        # This removes the (X) close button from the title bar
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        if btn_type == "yn_btn":
            self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.setDefaultButton(QMessageBox.No)  # Highlights 'No' for Enter key

        if btn_type == "ok":
            self.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.setIcon(QMessageBox.Icon.Information)

        self.set_style()

    def set_style(self):
        self.setStyleSheet(f"""
                    QMessageBox {{
                        background-color: {DefaultColors.light_grey.value};
                        color: {DefaultColors.pure_black.value};
                        font-family: {DefaultFont.family.value};
                        font-size: {DefaultFont.size.value - 5}px;
                        font-weight: normal;
                        font-style: normal;
                     }}
                    QPushButton {{
                        background-color: {DefaultColors.dark_grey.value};
                        color: white;
                        padding: 5px 15px;
                        border-radius: {DefaultBorder.radius.value}px;
                     }}
                    QPushButton:hover {{
                        background-color: {DefaultColors.dark_blue.value};
                    }}
                """)
