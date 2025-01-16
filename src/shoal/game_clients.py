import os

from shoal import data_structures
from shoal.general.file_io import download_file
from shoal.settings import get_current_selected_game, get_use_staging, get_currently_selected_game_mode, get_game_directory


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

def get_game_mode_options() -> list[tuple[str, int]]:
    current_game = get_current_selected_game()

    for game in data_structures.games_info:
        if game.game == current_game:
            return [(mode.game_mode.value, idx) for idx, mode in enumerate(game.game_modes)]

    return []


def get_game_selector_options() -> list[tuple[str, int]]:
    enum_strings = data_structures.get_enum_strings_from_enum(data_structures.Games)
    data = []
    for index, enum_string in enumerate(enum_strings):
        data.append((enum_string, index))
    return data


def get_current_client() -> data_structures.GameClients:
    current_game = get_current_selected_game()
    current_game_mode = get_currently_selected_game_mode()
    client = None
    if current_game == data_structures.Games.CALL_OF_DUTY_GHOSTS:
        client = data_structures.GameClients.ALTERWARE
    elif current_game == data_structures.Games.CALL_OF_DUTY_ADVANCED_WARFARE:
        client = data_structures.GameClients.ALTERWARE
    elif current_game == data_structures.Games.CALL_OF_DUTY_MODERN_WARFARE_II:
        client = data_structures.GameClients.ALTERWARE
    elif current_game == data_structures.Games.CALL_OF_DUTY_BLACK_OPS_III:
        client = data_structures.GameClients.ALTERWARE
    elif current_game == data_structures.Games.CALL_OF_DUTY_MODERN_WARFARE_III:
        if current_game_mode == data_structures.GameModes.SINGLE_PLAYER:
            client = data_structures.GameClients.ALTERWARE
        else:
            client = data_structures.GameClients.PLUTONIUM
    else:
        client = data_structures.GameClients.PLUTONIUM
    return client


def get_plutonium_forums_link() -> str:
    return 'https://forum.plutonium.pw/'


def get_alterware_forums_link() -> str:
    return 'https://forum.alterware.dev/'


def get_plutonium_docs_link() -> str:
    return 'https://plutonium.pw/docs/'


def get_alterware_docs_link() -> str:
    return 'https://forum.alterware.dev/docs/'


def get_current_client_docs_link() -> str:
    if get_current_client() == data_structures.GameClients.ALTERWARE:
        return get_alterware_docs_link()
    else:
        return get_plutonium_docs_link()


def get_current_client_forum_link() -> str:
    if get_current_client() == data_structures.GameClients.ALTERWARE:
        return get_alterware_forums_link()
    else:
        return get_plutonium_forums_link()


def get_latest_alterware_launcher_url() -> str:
    return 'https://github.com/mxve/alterware-launcher/releases/latest/download/alterware-launcher.exe'


def get_current_config_path_for_alterware_games() -> str:
    current_game_mode = get_currently_selected_game_mode()
    if current_game_mode == data_structures.GameModes.SINGLE_PLAYER:
        config_path = os.path.normpath(f'{get_game_directory()}/players2/config.cfg')
    else:
        config_path = os.path.normpath(f'{get_game_directory()}/players2/config_mp.cfg')
    return config_path
    

def get_t7x_download_url() -> str:
    return 'https://master.bo3.eu/t7x/t7x.exe'


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
