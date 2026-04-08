import logging
import os
import tempfile

import pymupdf
from expected_values import ExpectedValues

from ma_crf_bookmarks.logic.bookmark_logic import MainLogic


def test_main_logic():
    """
    Demo test, create functions like this to test all functionalities
    """
    logic = MainLogic()

    crf_path = "input/acrf_raw.pdf"
    sds_path = "input/sds_cdisc.xlsx"
    temp_folder = tempfile.gettempdir()
    new_crf_path = os.path.join(temp_folder, "acrf_bookmarks.pdf")

    logging.info("SYS  | Input CRF:\t\t %s", crf_path)
    logging.info("SYS  | Input SDS:\t\t %s", sds_path)
    logging.info("SYS  | Output CRF:\t %s", new_crf_path)

    _ = logic.start_logic(crf_path=crf_path, sds_path=sds_path, output_path=new_crf_path)

    # read in created aCRF
    crf_doc = pymupdf.open(new_crf_path)
    toc_input = crf_doc.get_toc(simple=True)

    expected_vaules = ExpectedValues()
    toc_expected = expected_vaules.toc_expected

    assert toc_input == toc_expected

    logging.info("Test finished")
