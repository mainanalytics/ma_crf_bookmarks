# conftest.py
import logging
import os

import pytest
from datetime import datetime


# Fixture to access logger in tests
@pytest.fixture(scope="session")
def logger():
    logger = logging.getLogger("test_logger")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def pytest_configure(config):
    """Configuration for pytest-html
    Used to set a dynamic validation report name

    Args:
        config (_type_): handled by pytest
    """
    config.option.log_cli = True
    config.option.log_cli_level = "INFO"
    config.option.log_cli_format = "%(asctime)s [%(levelname)s] %(message)s"
    config.option.log_cli_date_format = "%H:%M:%S"

    if not config.option.htmlpath:
        os.makedirs("validation_report", exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        config.option.htmlpath = f"validation_report/qc_{now}.html"
