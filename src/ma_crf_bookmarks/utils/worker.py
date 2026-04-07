from PySide6.QtCore import QObject, Signal


class Worker(QObject):
    """Class for handling multi-threading"""

    finished = Signal(object)  # signal to emit result

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._is_running = False  # flag to control abortion

    def run(self):
        self._is_running = True  # flag to control abortion
        result = self.func(*self.args, **self.kwargs)
        self.finished.emit(result)

    def abort(self):
        self._is_running = False  # set flag to request stop
        self.finished.emit("Logic aborted")
