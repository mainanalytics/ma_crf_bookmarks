import os
import sys


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller. Checks if a one-file
    compilation is run. If this is true it searches the resource by runtime in the unpacked
    temporary folder.

    Parameters
    -------
    relative_path : str
        relative path to the resource (same like in a script run)

    Returns
    -------
    str:
        path to ressource dependent of the current enviroment

    """
    if os.path.exists("_internal"):
        return os.path.join("_internal", relative_path)
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
