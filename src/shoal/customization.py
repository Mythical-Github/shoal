import os
import sys

import pywinctl
from textual.app import App


def set_terminal_size(app: object, x: int, y: int):
    all_windows = pywinctl.getAllWindows()

    windows = [win for win in all_windows if win.title == app.TITLE]

    for window in windows:
        try:
            window.resize(x, y)
        except Exception as e:
            print(f"Error resizing window {window.title}: {e}")


def set_window_title(window_title: str):
    sys.stdout.write(f"\033]0;{window_title}\007")
    sys.stdout.flush()


def enable_vt100():
    """Enable VT100 escape codes in the Windows Command Prompt."""
    # Check if VT100 is already enabled
    query_command = 'reg query HKCU\\Console /v VirtualTerminalLevel 2>nul'
    result = os.popen(query_command).read()
    if "0x1" not in result:
        os.system('reg add HKCU\\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul')
