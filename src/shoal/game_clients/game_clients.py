from shoal import data_structures
from shoal.settings import get_current_selected_game, get_currently_selected_game_mode
from shoal.game_clients.alterware import (
    get_alterware_docs_link, 
    get_alterware_forums_link, 
    get_alterware_github_link
)
from shoal.game_clients.plutonium import (
    get_plutonium_docs_link, 
    get_plutonium_forums_link, 
    get_plutonium_github_link
)
from shoal.game_clients.nazi_zombies_portable import (
    get_nazi_zombie_portable_docs, 
    get_nazi_zombie_portable_forums_link, 
    get_nazi_zombie_portable_github_link
)


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
    elif current_game ==  data_structures.Games.CALL_OF_DUTY_NAZI_ZOMBIES_PORTABLE:
        client = data_structures.GameClients.NAZI_ZOMBIES_PORTABLE
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


def get_current_client_docs_link() -> str:
    if get_current_client() == data_structures.GameClients.ALTERWARE:
        return get_alterware_docs_link()
    elif get_current_selected_game() == data_structures.Games.CALL_OF_DUTY_NAZI_ZOMBIES_PORTABLE:
        return get_nazi_zombie_portable_docs()
    else:
        return get_plutonium_docs_link()


def get_current_client_forum_link() -> str:
    if get_current_client() == data_structures.GameClients.ALTERWARE:
        return get_alterware_forums_link()
    elif get_current_selected_game() == data_structures.Games.CALL_OF_DUTY_NAZI_ZOMBIES_PORTABLE:
        return get_nazi_zombie_portable_forums_link()
    else:
        return get_plutonium_forums_link()


def get_current_client_github_link() -> str:
    link = None
    current_client = get_current_client()
    if current_client ==  data_structures.GameClients.PLUTONIUM:
        link = get_plutonium_github_link()
    elif current_client == data_structures.GameClients.ALTERWARE:
        link = get_alterware_github_link()
    else:
        link = get_nazi_zombie_portable_github_link()
    return link
