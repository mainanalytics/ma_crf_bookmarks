import ctypes


def hide_terminal():
    """Pyside6 applications are opening a terminal by default. Call this function to close
    the terminal. Only for windows
    """
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)  # 0 = SW_HIDE
        ctypes.windll.kernel32.CloseHandle(whnd)
