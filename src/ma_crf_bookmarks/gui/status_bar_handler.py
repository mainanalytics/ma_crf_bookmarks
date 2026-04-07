from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import QTimer

if TYPE_CHECKING:
    from ma_crf_bookmarks.main import MainWindow


class StatusBarHandler:
    """Class to handle more fancy status massages in the main window"""

    def __init__(self, main_window: "MainWindow"):
        self.main_window = main_window
        self.index = 0
        self.timer = QTimer()

    def start_spinner(
        self,
        txt: str,
        spinner_symbols: Optional[list[str]] = None,
        freq: Optional[int] = 300,
        timeout: Optional[int] = None,
    ):
        """Spinner is used to change the text based on a given frequency. Fancy e.g. to simulate
        a running, or loading task. Thie spinner timer runs in its own thread.
        "⏳", "⌛", "🔄","🔃"

        """
        if spinner_symbols is None:
            spinner_symbols = ["⟳", "⟲"]

        self.index = 0
        self.timer.timeout.connect(
            lambda: self._update_spinner(txt=txt, timeout=timeout, spinner=spinner_symbols)
        )
        self.timer.start(freq)  # update every 300 ms

    def _update_spinner(self, txt: str, timeout: int, spinner: list[str]):
        spinner = spinner * 666 + ["666"]
        symbol = spinner[self.index]
        self.update_status_bar(txt + " " + symbol, timeout)
        self.index = (self.index + 1) % len(spinner)

    def end_spinner(self):
        self.timer.stop()

    def update_status_bar(self, txt: str, timeout: int = None):
        self.main_window.update_status_bar(txt=txt, timeout=timeout)
