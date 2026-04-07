import logging
import os
from datetime import datetime

from ma_pytemp.utils.config import ConfigModel


class NoNewlineFilter(logging.Filter):
    """
    Class for a custom filter functionality
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Folter that removes newlines from string. Handles newlines and carriage returns

        Parameters
        ----------
        record : logging.LogRecord

        Returns
        -------
        bool:
        """
        if isinstance(record.msg, str):
            record.msg = record.msg.replace("\n", " ").replace("\r", "")
        return True


def create_log(config: ConfigModel, name: str = "base_logger") -> tuple[logging.Logger, str]:
    """
    Creates a template logger. Log file is created under given folder. Name consists of logger name
    and date of creation.

    Parameters
    ----------
    config : ConfigModel
        Expect the LoggerConfig enabled
    name : str, optional
        logger name, by default "base_logger"

    Returns
    -------
    logging.Logger

    log_path
        path to the log file
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    log_folder = os.path.normpath(config.logging.folder)
    os.makedirs(log_folder, exist_ok=True)

    daytime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = log_folder + "/" + name + "_" + daytime_str + ".log"

    logging.basicConfig(
        filename=log_path,
        filemode="w",  # 'w' = überschreibt, 'a' = anhängen
        encoding="utf-8",
        level=logging.INFO,
    )
    logging.addLevelName(logging.WARNING, "WARN")  # rename output from WARNING to WARN
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")
    )
    fh.addFilter(NoNewlineFilter())
    logger.addHandler(fh)

    return logger, log_path
