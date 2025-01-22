import os

from shoal import data_structures
from shoal.general.file_io import download_file
from shoal.settings import get_current_selected_game, get_currently_selected_game_mode, get_game_directory


def get_alterware_forums_link() -> str:
    return 'https://forum.alterware.dev/'


def get_alterware_docs_link() -> str:
    return 'https://forum.alterware.dev/docs/'


def get_latest_alterware_launcher_url() -> str:
    return 'https://github.com/mxve/alterware-launcher/releases/latest/download/alterware-launcher.exe'

    
def get_current_config_path_for_alterware_games() -> str:
    if get_current_selected_game() == data_structures.Games.CALL_OF_DUTY_BLACK_OPS_III:
        return os.path.join(f'{get_game_directory()}/t7x/players/user/config.cfg')
    else:
        current_game_mode = get_currently_selected_game_mode()
        if current_game_mode == data_structures.GameModes.SINGLE_PLAYER:
            config_path = os.path.normpath(f'{get_game_directory()}/players2/config.cfg')
        else:
            config_path = os.path.normpath(f'{get_game_directory()}/players2/config_mp.cfg')
        return config_path
    

def get_t7x_download_url() -> str:
    return 'https://master.bo3.eu/t7x/t7x.exe'


def actually_download_t7x():
    t7x_path = get_t7x_client_path()
    if not os.path.isfile(t7x_path):
        download_file(get_t7x_download_url(), t7x_path)


def download_t7x_client():
    t7x_path = get_t7x_client_path()
    if not os.path.isfile(t7x_path):
        download_file(get_t7x_download_url(), t7x_path)


def get_t7x_client_path() -> str:
    return os.path.normpath(f'{get_game_directory()}/t7x.exe')


def get_t7x_client() -> str:
    t7x_path = get_t7x_client_path()
    if not os.path.isfile(t7x_path):
        download_t7x_client()
    return t7x_path


def get_t7x_user_config_path() -> str:
    return os.path.normpath(os.path.join(get_game_directory(), 't7x', 'players', 'user', 'config.cfg'))


def get_alterware_github_link() -> str:
    # technically the launcher url and not the org, but this is what most people would want
    return 'https://github.com/mxve/alterware-launcher'


def push_install_alterware_launcher_screen():
    from shoal.main_app import app
    from shoal.settings import SCRIPT_DIR, get_alterware_launcher_path
    from shoal.base_widgets import setup_screen
    from shoal import game_runner
    if not os.path.isfile(os.path.normpath(f'{SCRIPT_DIR}/assets/alterware_launcher/alterware-launcher.exe')):
        download_alterware_screen = setup_screen.SetupScreen(
                step_text_to_step_functions={"Downloading Alterware Client...": get_alterware_launcher_path},
                finished_all_steps_function=game_runner.run_game,
                widgets_to_refresh_on_screen_pop=[],
                screen_label_text="Alterware Client Setup:"
            )
        app.push_screen(download_alterware_screen)
    else:
        game_runner.run_game()


def push_install_t7x_screen():
    from shoal import game_runner
    from shoal.main_app import app
    from shoal.base_widgets import setup_screen
    from shoal.game_clients.alterware import download_t7x_client, get_t7x_client_path
    if not os.path.isfile(get_t7x_client_path()):
        download_t7x_screen = setup_screen.SetupScreen(
                step_text_to_step_functions={"Downloading T7X Client...": download_t7x_client},
                finished_all_steps_function=game_runner.run_game,
                widgets_to_refresh_on_screen_pop=[],
                screen_label_text="Alterware T7X Client Setup:"
            )
        app.push_screen(download_t7x_screen)
    else:
        game_runner.run_game()
