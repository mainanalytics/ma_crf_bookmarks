import logging

import pytest
from pytest_html import extras


from ma_pytemp.logic.demo_logic import MainLogic


def test_main_logic():
    """
    Demo test, create functions like this to test all functionalities
    """
    logic = MainLogic()
    result = logic.start_logic(input_value=20)

    logging.info("Starting test for prime factorization: %s", str(20))

    assert result == " 2 ,2 ,5"

    logging.info("Test finished")
