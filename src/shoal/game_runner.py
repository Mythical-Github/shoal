import os
import subprocess

from shoal import data_structures
from shoal.general.file_io import add_line_to_config
from shoal.logger import print_to_log_window
from shoal.game_clients import (
    get_plutonium_appdata_dir,
    get_plutonium_bootstrapper,
    get_plutonium_modern_warfare_iii_config_path,
    get_current_client,
    get_t7x_client
)
from shoal.settings import (
    get_current_selected_game,
    get_current_username,
    get_currently_selected_game_mode,
    get_game_directory,
    get_game_specific_args,
    get_global_args,
    get_alterware_launcher_path,
    get_use_staging
)

def get_game_launch_arg() -> str:
    current_game_mode = get_currently_selected_game_mode()
    current_selected_game = get_current_selected_game()

    game_info_entry = next((game for game in data_structures.games_info if game.game == current_selected_game), None)
    if not game_info_entry:
        raise ValueError(f"No game entry found for: {current_selected_game.value}")

    game_mode_entry = next((mode for mode in game_info_entry.game_modes if mode.game_mode == current_game_mode), None)
    if not game_mode_entry:
        raise ValueError(f"No game mode entry found for: {current_game_mode.value}")

    return game_mode_entry.arg



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


def run_alterware_t7_client():
    command = f'"{get_t7x_client()}"'
    args = []
    command = f'{command} -launch'
    for arg in args:
        command = f'{command} {arg}'
    for arg in get_game_specific_args():
        command = f'{command} {arg}'
    for arg in get_global_args():
        command = f'{command} {arg}'
    print_to_log_window(command)
    subprocess.Popen(
        command,
        cwd = get_game_directory(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )
    


def run_alterware_game():
    current_selected_game = get_current_selected_game()
    if current_selected_game == data_structures.Games.CALL_OF_DUTY_BLACK_OPS_III:
        run_alterware_t7_client()
        return
    main_exe = get_alterware_launcher_path()
    args = [
        get_game_launch_arg(),
        '--bonus',
        '--skip-redist',
        '--path',
        f'"{get_game_directory()}"'
    ]
    if get_use_staging():
        args.append('--prerelease')
    if get_currently_selected_game_mode() == data_structures.GameModes.SINGLE_PLAYER:
        args_string = '-singleplayer'
    else:
        args_string = '-multiplayer'
    global_args = get_global_args() or []
    game_specific_args = get_game_specific_args() or []
    
    combined_args = global_args + game_specific_args
    for arg in combined_args:
        args_string = f'{args_string} {arg}'
    args.append(f'--pass "{args_string.strip()}"')
    command = f'"{main_exe}"'
    for arg in args:
        command = f'{command} {arg}'
    print_to_log_window(command)
    subprocess.Popen(
        command,
        cwd=os.path.dirname(get_alterware_launcher_path()),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )


def run_game():
    if get_game_directory() == '':
        print_to_log_window(f'You must provide the game directory, before running the game')
        return
    if get_current_client() == data_structures.GameClients.ALTERWARE:
        run_alterware_game()
    elif get_game_launch_arg() == 'iw5mp':
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
