import threading
import time

from shoal import game_runner
from shoal.customization import set_window_title
from shoal.auto_run_game_bar.auto_run_game_bar import get_spinbox
from shoal.settings import (
    get_auto_run_game,
    get_auto_run_game_delay,
    get_current_preferred_theme,
    get_title_for_app,
    set_auto_run_game_delay,
    set_current_preferred_theme,
)

has_initially_set_theme = False
has_auto_run_game = False
check_condition_thread = None
stop_thread_event = threading.Event()

time_passed = 0.0
last_run_time = 0.0
TOLERANCE = 0.1
MAX_RUN_INTERVAL = 1.0


def get_currently_selected_theme() -> str:
    global app_instance

    if app_instance is not None:

        return app_instance.theme
    else:
        return "No App Instance Found"


def check_theme():
    if app_instance:
        global has_initially_set_theme
        if has_initially_set_theme:
            current_theme = get_currently_selected_theme()
            if get_current_preferred_theme() != current_theme:
                set_current_preferred_theme(current_theme)


def action_on_condition():
    if get_auto_run_game():
        game_runner.run_game()
        global has_auto_run_game
        has_auto_run_game = True


def periodic_check():
    global time_passed, last_run_time
    while not stop_thread_event.is_set():
        set_window_title(get_title_for_app())
        check_theme()
        spin_box = get_spinbox()
        if spin_box != None:
            if float(spin_box.value) != get_auto_run_game_delay():
                from shoal.logger import print_to_log_window
                spin_box_message = f'The Auto Run Game Delay has been set to "{spin_box.value}" Seconds'
                print_to_log_window(spin_box_message)
                set_auto_run_game_delay(spin_box.value)

        delay = get_auto_run_game_delay()
        if (time_passed - delay) > TOLERANCE:
            global has_auto_run_game
            if not has_auto_run_game:
                current_time = time.time()
                if current_time - last_run_time >= MAX_RUN_INTERVAL:
                    action_on_condition()
                    last_run_time = current_time
        time.sleep(0.1)
        if get_auto_run_game():
            time_passed = time_passed + 0.1

app_instance = None
def start_periodic_check_thread(app):
    global app_instance
    app_instance = app
    global check_condition_thread, stop_thread_event

    stop_thread_event.clear()
    check_condition_thread = threading.Thread(target=periodic_check, daemon=True)
    check_condition_thread.start()


def stop_periodic_check_thread():
    global stop_thread_event
    stop_thread_event.set()
    if check_condition_thread:
        check_condition_thread.join()
