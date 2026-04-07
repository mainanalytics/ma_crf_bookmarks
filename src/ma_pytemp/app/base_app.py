import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Optional

from PySide6.QtCore import QThread

from ma_pytemp.app.main_app_window import MainAppWindow
from ma_pytemp.utils.config import ConfigModel
from ma_pytemp.utils.user import User
from ma_pytemp.utils.worker import Worker

if TYPE_CHECKING:
    from ma_pytemp.main import MainWindow


class APP_STATUS(Enum):
    CLOSED = 0
    INITIALIZED = 1
    RUNNING = 2
    FINISHED = 3
    ERROR = 4


class BaseApp:
    """
    Interface definition for real functional logic. Mainly used to handle threading and references.
    Only change something here if it's really necessary
    """

    def __init__(
        self,
        name: str,
        main_window: "MainWindow",
        config: ConfigModel,
        user: User,
        logger: logging.Logger,
        root_dir: str,
        descripion: Optional[str] = "",
        status: APP_STATUS = APP_STATUS.INITIALIZED,
    ):
        self.config: ConfigModel = config
        self.user: User = user
        self.root_dir: str = root_dir
        self.logger: logging.Logger = logger
        self.name: str = name
        self.description: str = descripion
        self.status: APP_STATUS = status

        self.thread_counter = 0
        self.thread: QThread = None
        self.thread_list: list[QThread] = []
        self.worker: Worker = None
        self.worker_list: list[Worker] = []

        self.main_window: MainWindow = main_window
        if self.main_window:
            self.main_window.setObjectName(self.name)

    def get_status(self) -> APP_STATUS:
        return self.status

    def is_running(self) -> bool:
        return self.status == APP_STATUS.RUNNING

    def set_status(self, status: APP_STATUS):
        self.status = status

    def run_thread(self, func: Callable[[], str], on_return: Callable[[str], Any]):
        """
        To run a computation heavy background task always call this function, like:
            self.app_base.run_thread(func=lambda: self.logic.demo_start_logic(3, 5),
                                     on_return=self.on_finished)
        in your specific app. The on_return function exepts only one.
        Sets the app status to APP_STATUS.RUNNING during execution and to
        APP_STATUS.FINISHED after execution

        Parameters
        ----------
        func : Callable
            callable function, does not exept input parameters, use lambda expressen
            provides return value via str signal.

        on_return : Callable
            function that exepts a return string via signal from the called func.
            Return values does not matter

        """
        self.status = APP_STATUS.RUNNING

        # Create thread and worker
        self.thread_counter += 1
        if self.thread:
            # print("append")
            self.thread_list.append(self.thread)
            self.worker_list.append(self.worker)

        self.thread: QThread = QThread()
        self.thread.setObjectName(f"Thread_{self.thread_counter}")
        self.worker: Worker = Worker(func)

        # Move worker to the thread
        self.worker.moveToThread(self.thread)

        # When thread starts, run the worker's run method
        self.thread.started.connect(self.worker.run)

        # Connect worker finished signal to GUI update
        self.worker.finished.connect(self.thread.quit)  # stop thread when done
        self.worker.finished.connect(lambda: self.set_status(APP_STATUS.FINISHED))
        self.worker.finished.connect(on_return)

        # Optional: delete later to free memory
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # Start the thread (non-blocking)
        self.thread.start()

    def abort_thread(self, wait_till_kill=2000):
        # print("1", datetime.now(), self.thread.isRunning())
        self.worker.abort()

        self.thread.requestInterruption()

        # wait up to 2 seconds for it to finish
        if not self.thread.wait(wait_till_kill):
            # print("2", datetime.now(), self.thread.isRunning())
            self.thread.terminate()
        # print("3", datetime.now(), self.thread.isRunning())

        if self.logger:
            self.logger.info("SYS  | Aborted logic.")

        self.set_status(APP_STATUS.FINISHED)

        self.worker = None


class MainApp(BaseApp):
    """One specific instance of a logic module. Best approach is not to change it."""

    def __init__(
        self,
        main_window: "MainWindow",
        config: ConfigModel,
        user: User,
        logger: logging.Logger,
        root_dir: str,
    ):
        super().__init__(
            name="MainApp",
            main_window=main_window,
            config=config,
            user=user,
            logger=logger,
            root_dir=root_dir,
            descripion="Main logic of the template",
        )
        self.app_window: MainAppWindow = MainAppWindow(base_app=self)
