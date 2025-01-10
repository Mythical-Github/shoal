import sys

import pygetwindow
from textual.app import App


def set_terminal_size(app: App, x: int, y: int):
    all_windows = pygetwindow.getAllWindows()

    # make this an equality check and not a substring check later
    windows = [win for win in all_windows if app.TITLE in win.title]

    for window in windows:
        try:
            window.resizeTo(x, y)
        except Exception as e:
            e


def set_window_title(window_title: str):
    sys.stdout.write(f"\033]0;{window_title}\007")
    sys.stdout.flush()
