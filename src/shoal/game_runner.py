import os
import subprocess

from shoal import data_structures
from shoal.general.file_io import add_line_to_config
from shoal.logger import print_to_log_window
from shoal.game_clients import (
    get_plutonium_appdata_dir,
    get_plutonium_bootstrapper,
    get_plutonium_modern_warfare_iii_config_path,
)
from shoal.settings import (
    get_current_selected_game,
    get_current_username,
    get_currently_selected_game_mode,
    get_game_directory,
    get_game_specific_args,
    get_global_args,
)

def get_game_launch_arg() -> str:
    current_game_mode = get_currently_selected_game_mode()
    current_selected_game = get_current_selected_game()

    game_info_entry = None
    for game_entry in data_structures.games_info.game_entries:
        if game_entry.game == current_selected_game:
            game_info_entry == game_entry
            break
    game_mode_arg = None
    for game_mode_entry in game_info_entry.game_modes:
        if game_mode_entry.game_mode == current_game_mode:
            game_mode_arg = game_mode_entry.arg
            break
    return game_mode_arg


def run_game_mw3():
    exe = f'"{get_plutonium_bootstrapper()}"'
    exe = f'{exe} "{get_game_launch_arg()}"'
    exe = f'{exe} "{get_game_directory()}"'
    exe = f'{exe} +name'
    exe = f'{exe} {get_current_username()}'
    exe = f'{exe} -lan'

    for arg in get_global_args():
        add_line_to_config(get_plutonium_modern_warfare_iii_config_path(), arg)

    for arg in get_game_specific_args():
        add_line_to_config(get_plutonium_modern_warfare_iii_config_path(), arg)

    print_to_log_window(exe)
    os.chdir(get_plutonium_appdata_dir())
    if not os.path.isdir(get_game_directory()):
        print_to_log_window(f'The following game directory is not valid "{get_game_directory()}"')
    elif not os.path.isfile(get_plutonium_bootstrapper()):
        print_to_log_window(f'The following file path is not valid "{get_plutonium_bootstrapper()}"')
    else:
        subprocess.Popen(
            exe,
            cwd=get_plutonium_appdata_dir(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )

# patch this
def run_game():
    if get_game_launch_arg() == 'iw5mp':
        run_game_mw3()
    else:
        exe = f'"{get_plutonium_bootstrapper()}"'
        exe = f'{exe} "{get_game_launch_arg()}"'
        exe = f'{exe} "{get_game_directory()}"'
        exe = f'{exe} +name'
        exe = f'{exe} {get_current_username()}'
        exe = f'{exe} -lan'

        args = []
        for arg in args:
            exe = f'{exe} {arg}'
        for arg in get_game_specific_args():
            exe = f'{exe} {arg}'
        for arg in get_global_args():
            exe = f'{exe} {arg}'

        print_to_log_window(exe)
        os.chdir(get_plutonium_appdata_dir())
        if not os.path.isdir(get_game_directory()):
            print_to_log_window(f'The following game directory is not valid "{get_game_directory()}"')
        elif not os.path.isfile(get_plutonium_bootstrapper()):
            print_to_log_window(f'The following file path is not valid "{get_plutonium_bootstrapper()}"')
        else:
            subprocess.Popen(
                exe,
                cwd=get_plutonium_appdata_dir(),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            )
