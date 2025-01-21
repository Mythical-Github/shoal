import os
import subprocess

from shoal import data_structures
from shoal.game_clients.aurora import get_h1_mod_exec_path
from shoal.general.file_io import add_line_to_config, remove_lines_from_config_that_start_with_substring
from shoal.logger import print_to_log_window
from shoal.game_clients.plutonium import (
    get_plutonium_appdata_dir,
    get_plutonium_bootstrapper,
    get_plutonium_modern_warfare_iii_config_path
)
from shoal.game_clients.nazi_zombies_portable import get_nazi_zombie_portable_executable_path, get_nzp_user_config_path
from shoal.game_clients.game_clients import get_current_client, get_current_client_docs_link
from shoal.game_clients.alterware import get_t7x_client, get_t7x_user_config_path
from shoal.settings import (
    get_current_selected_game,
    get_current_username,
    get_currently_selected_game_mode,
    get_game_directory,
    get_game_specific_args,
    get_global_args,
    get_alterware_launcher_path,
    get_use_staging,
    get_global_args
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
        add_line_to_config(get_t7x_user_config_path(), arg)
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


def run_nazi_zombies_portable():
    user_config_path = get_nzp_user_config_path()
    if os.path.isfile(user_config_path):
        remove_lines_from_config_that_start_with_substring(user_config_path, 'name ')
        add_line_to_config(user_config_path, f'name "{get_current_username()}"')
    for arg in get_game_specific_args():
        add_line_to_config(user_config_path, arg)

    command = get_nazi_zombie_portable_executable_path()
    for arg in get_global_args():
        command = f'{command} {arg}'
    subprocess.Popen(
        command,
        cwd=os.path.dirname(get_nazi_zombie_portable_executable_path()),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )


def testing_branch_warning():
    invalid_warning_part_one = 'You have Testing branch enabled for an invalid game'
    invalid_warning_part_two = 'The game will be launched with the Default branch'
    print_to_log_window(invalid_warning_part_one)
    print_to_log_window(invalid_warning_part_two)


def testing_branch_warning_check():
    if get_use_staging():
        if get_current_selected_game() in {
            data_structures.Games.CALL_OF_DUTY_NAZI_ZOMBIES_PORTABLE, 
            data_structures.Games.CALL_OF_DUTY_BLACK_OPS_III,
            data_structures.Games.CALL_OF_DUTY_MODERN_WARFARE_REMASTERED_2017
        }:
            testing_branch_warning()


def no_user_config_exists_warning():
    no_user_config_warning_part_one = 'There is no config yet generated for this client, game, and/or game mode'
    no_user_config_warning_part_two = 'Arg passing and username setting may not work function'
    no_user_config_warning_part_three = 'until next launch/after in game configuration generates a config'
    print_to_log_window(no_user_config_warning_part_one)
    print_to_log_window(no_user_config_warning_part_two)
    print_to_log_window(no_user_config_warning_part_three)


def no_user_config_exists_check():
    current_game = get_current_selected_game
    current_game_mode = get_currently_selected_game_mode
    if current_game == data_structures.Games.CALL_OF_DUTY_BLACK_OPS_III:
        from shoal.game_clients.alterware import get_t7x_user_config_path
        if not os.path.isfile(get_t7x_user_config_path()):
            no_user_config_exists_warning()
    if current_game == data_structures.Games.CALL_OF_DUTY_NAZI_ZOMBIES_PORTABLE:
        from shoal.game_clients.nazi_zombies_portable import get_nzp_user_config_path
        if not os.path.isfile(get_nzp_user_config_path()):
            no_user_config_exists_warning()
    if current_game == data_structures.Games.CALL_OF_DUTY_MODERN_WARFARE_III_2011:
        if current_game_mode == data_structures.GameModes.MULTIPLAYER:
            from shoal.game_clients.plutonium import get_plutonium_modern_warfare_iii_config_path
            if not os.path.isfile(get_plutonium_modern_warfare_iii_config_path()):
                no_user_config_exists_warning()


def client_info_message():
    print_to_log_window(f'Launch Information:')
    print_to_log_window(f'Game: "{get_current_selected_game().value}"')
    print_to_log_window(f'Game Mode: "{get_currently_selected_game_mode().value}"')
    print_to_log_window(f'Client/Project: "{get_current_client().value}"')
    print_to_log_window(f'Client/Project Website: "{get_current_client_docs_link()}"')


def run_mw_remastered_2017():
    command = get_h1_mod_exec_path()
    if get_currently_selected_game_mode() == data_structures.GameModes.SINGLE_PLAYER:
        command = f'{command} -singleplayer'
    else:
        command = f'{command} -multiplayer'
    for arg in get_global_args():
        command = f'{command} {arg}'
    for arg in get_game_specific_args():
        command = f'{command} {arg}'
    print_to_log_window(command)
    subprocess.Popen(
        command,
        cwd=os.path.dirname(get_h1_mod_exec_path()),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )


# def run_mw_remastered_2017():
#     command = get_h1_mod_exec_path()
#     for arg in get_global_args():
#         command = f'{command} {arg}'
#     if get_currently_selected_game_mode() == data_structures.GameModes.SINGLE_PLAYER:
#         command = f'{command} -singleplayer'
#     else:
#         command = f'{command} -multiplayer'
#     combined_string = ''
#     for arg in get_game_specific_args():
#         combined_string = f'{combined_string} {arg}'
#     command = f'{command} --pass "{combined_string.strip()}"'
#     print_to_log_window(command)
#     subprocess.Popen(
#         command,
#         cwd=os.path.dirname(get_h1_mod_exec_path()),
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#         stdin=subprocess.DEVNULL
#     )


def run_game():
    client_info_message()
    testing_branch_warning_check()
    no_user_config_exists_check()
    game_directory = get_game_directory()
    current_client = get_current_client()
    current_game = get_current_selected_game()
    # current_game_mode = get_currently_selected_game_mode()
    current_username = get_current_username()
    plutonium_appdata_dir = get_plutonium_appdata_dir()
    plutonium_bootstrapper = get_plutonium_bootstrapper()
    game_launch_arg = get_game_launch_arg()

    if game_directory == '':
        print_to_log_window(f'You must provide the game directory, before running the game')
        return
    if current_game == data_structures.Games.CALL_OF_DUTY_MODERN_WARFARE_REMASTERED_2017:
        run_mw_remastered_2017()
        return
    if current_game == data_structures.Games.CALL_OF_DUTY_NAZI_ZOMBIES_PORTABLE:
        run_nazi_zombies_portable()
        return
    if current_client == data_structures.GameClients.ALTERWARE:
        run_alterware_game()
    elif game_launch_arg == 'iw5mp':
        run_game_mw3()
    else:
        exe = f'"{plutonium_bootstrapper}"'
        exe = f'{exe} "{game_launch_arg}"'
        exe = f'{exe} "{game_directory}"'
        exe = f'{exe} +name'
        exe = f'{exe} {current_username}'
        exe = f'{exe} -lan'

        args = []
        for arg in args:
            exe = f'{exe} {arg}'
        for arg in get_game_specific_args():
            exe = f'{exe} {arg}'
        for arg in get_global_args():
            exe = f'{exe} {arg}'
        print_to_log_window(exe)
        os.chdir(plutonium_appdata_dir)
        if not os.path.isdir(game_directory):
            print_to_log_window(f'The following game directory is not valid "{game_directory}"')
        elif not os.path.isfile(plutonium_bootstrapper):
            print_to_log_window(f'The following file path is not valid "{plutonium_bootstrapper}"')
        else:
            subprocess.Popen(
                exe,
                cwd=plutonium_appdata_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            )
