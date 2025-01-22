import os

from shoal.general.file_io import download_file
from shoal.settings import get_game_directory


def get_github_link() -> str:
    return 'https://github.com/auroramod'


def get_community_link() -> str:
    return 'https://discord.com/invite/RzzXu5EVnh'


def get_docs_link() -> str:
    return 'https://docs.auroramod.dev/'


def get_h1_mod_exec_path() -> str:
    return os.path.normpath(f'{get_game_directory()}/h1-mod.exe')


def does_h1_mod_exec_exist() -> bool:
    return os.path.isfile(get_h1_mod_exec_path())


def download_h1_mod():
    if not does_h1_mod_exec_exist():
        download_file(get_h1_mod_download_url(), get_h1_mod_exec_path())


def get_h1_mod_download_url() -> str:
    return 'https://github.com/auroramod/h1-mod/releases/latest/download/h1-mod.exe'


def get_h1_mod_user_config_path() -> str:
    return os.path.normpath(f'{get_game_directory()}/players2/config.cfg')


def get_iw7_mod_exec_path() -> str:
    return


def does_iw7_mod_exec_exist() -> bool:
    return


def download_iw7_mod():
    return


def get_iw7_mod_download_url() -> str:
    return


def get_iw7_mod_user_config_path() -> str:
    return


def push_install_h1_screen():
    from shoal.base_widgets import setup_screen
    from shoal import game_runner
    from shoal.main_app import app
    if not os.path.isfile(get_h1_mod_exec_path()):
        download_h1_mod_screen = setup_screen.SetupScreen(
                step_text_to_step_functions={"Downloading Aurora's H1-Mod...": download_h1_mod},
                finished_all_steps_function=game_runner.run_game,
                widgets_to_refresh_on_screen_pop=[],
                screen_label_text="Aurora's H1-Mod Setup:"
            )
        app.push_screen(download_h1_mod_screen)
    else:
        game_runner.run_game()