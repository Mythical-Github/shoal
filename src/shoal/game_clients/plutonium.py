import os
import subprocess

from shoal.settings import get_use_staging, SCRIPT_DIR
from shoal.general.file_io import download_file, unzip_file
from shoal.base_widgets import setup_screen
from shoal import game_runner


def get_plutonium_appdata_dir() -> str:
    if get_use_staging():
        pluto_appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium-staging')
    else:
        pluto_appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium')
    return pluto_appdata_path


def get_plutonium_bootstrapper() -> str:
    return os.path.normpath(f'{get_plutonium_appdata_dir()}/bin/plutonium-bootstrapper-win32.exe')


def get_plutonium_modern_warfare_iii_config_path_suffix() -> str:
    return 'storage/iw5/players/config_mp.cfg'


def get_plutonium_modern_warfare_iii_config_path() -> str:
    return os.path.normpath(f'{get_plutonium_appdata_dir()}/{get_plutonium_modern_warfare_iii_config_path_suffix()}')


def get_plutonium_forums_link() -> str:
    return 'https://forum.plutonium.pw/'


def get_plutonium_docs_link() -> str:
    return 'https://plutonium.pw/docs/'


def get_plutonium_github_link() -> str:
    return 'https://github.com/plutoniummod'


def install_plutonium_normal_branch():
    plutonium_updater = get_plutonium_updater()
    os.makedirs(get_plutonium_appdata_dir(), exist_ok=True)
    command = f'"{plutonium_updater}"'
    args = [
        f'--directory "{get_plutonium_appdata_dir()}"',
        '--launcher'
    ]
    for arg in args:
        command = f'{command} {arg}'
    from shoal.logger import print_to_log_window
    print_to_log_window(command)
    subprocess.run(
        command,
        cwd=os.path.dirname(get_plutonium_updater()),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )


# finish
def install_plutonium_staging_branch():
    plutonium_updater = get_plutonium_updater()
    os.makedirs(get_plutonium_appdata_dir(), exist_ok=True)
    command = f'"{plutonium_updater}"'
    args = [
        f'--directory "{get_plutonium_appdata_dir()}"',
        '--launcher',
        '--cdn-url',
        f'"https://cdn.plutonium.pw/updater/staging/info.json"'
    ]
    for arg in args:
        command = f'{command} {arg}'
    from shoal.logger import print_to_log_window
    print_to_log_window(command)
    subprocess.run(
        command,
        cwd=os.path.dirname(get_plutonium_updater()),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )


def get_plutonium_updater() -> str:
    # if not get_is_plutonium_updater_installed():
    #     push_install_plutonium_updater_screen()
    return get_plutonium_updater_path()


def get_plutonium_updater_path() -> str:
    return os.path.normpath(f'{SCRIPT_DIR}/assets/plutonium_updater/plutonium-updater.exe')


def get_is_plutonium_updater_installed() -> bool:
    return os.path.isfile(get_plutonium_updater_path())


def download_plutonium_updater():
    plutonium_updater_path = get_plutonium_updater_path()
    plutonium_updater_zip = os.path.normpath(f'{os.path.dirname(plutonium_updater_path)}/plutonium_updater.zip')
    download_file(get_plutonium_updater_url(), plutonium_updater_zip)
    from shoal.logger import print_to_log_window
    print_to_log_window(f'Plutonium Updater Repo Link: "https://github.com/mxve/plutonium-updater.rs"')
    print_to_log_window(f'Plutonium Updater License: "https://github.com/mxve/plutonium-updater.rs/blob/master/LICENSE"')


def unzip_plutonium_updater():
    plutonium_updater_path = get_plutonium_updater_path()
    plutonium_updater_zip = os.path.normpath(f'{os.path.dirname(plutonium_updater_path)}/plutonium_updater.zip')
    unzip_file(plutonium_updater_zip, os.path.dirname(plutonium_updater_zip))


def cleanup_after_plutonium_updater_install():
    plutonium_updater_path = get_plutonium_updater_path()
    plutonium_updater_zip = os.path.normpath(f'{os.path.dirname(plutonium_updater_path)}/plutonium_updater.zip')
    os.remove(plutonium_updater_zip)


def get_plutonium_updater_github_page() -> str:
    return 'https://github.com/mxve/plutonium-updater.rs'


def get_plutonium_updater_url():
    return 'https://github.com/mxve/plutonium-updater.rs/releases/latest/download/plutonium-updater-x86_64-pc-windows-msvc.zip'


def push_install_plutonium_screen():
    from shoal.main_app import app
    install_function = None
    install_text = None
    if get_use_staging():
        install_function = install_plutonium_staging_branch
        install_text = 'Installing the Plutonium Client Staging Branch...'
    else:
        install_function = install_plutonium_normal_branch
        install_text = 'Installing the Plutonium Client...'
    if not os.path.isfile(get_plutonium_bootstrapper()):
        steps = {
            'Downloading Plutonium Updater...': download_plutonium_updater,
            'Unzipping Plutonium Updater...': unzip_plutonium_updater,
            'Cleaning up leftover files...': cleanup_after_plutonium_updater_install,
            install_text: install_function
        }
        download_nzp_screen = setup_screen.SetupScreen(
                step_text_to_step_functions=steps,
                finished_all_steps_function=game_runner.run_game,
                widgets_to_refresh_on_screen_pop=[],
                screen_label_text="Plutonium Setup:"
            )
        app.push_screen(download_nzp_screen)
    else:
        game_runner.run_game()


# def push_install_plutonium_updater_screen():
#     from shoal.main_app import app
#     if not os.path.isfile(get_plutonium_updater_path()):
#         steps = {
#             'Downloading Plutonium Updater...': download_plutonium_updater,
#             'Unzipping Plutonium Updater...': unzip_plutonium_updater,
#             'Cleaning up leftover files...': cleanup_after_plutonium_updater_install,
#         }
#         download_nzp_screen = setup_screen.SetupScreen(
#                 step_text_to_step_functions=steps,
#                 finished_all_steps_function=game_runner.run_game,
#                 widgets_to_refresh_on_screen_pop=[],
#                 screen_label_text="Plutonium Updater Setup:"
#             )
#         app.push_screen(download_nzp_screen)
#     else:
#         game_runner.run_game()
