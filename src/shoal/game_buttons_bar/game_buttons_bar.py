import os

from textual.widgets import Static
from textual.app import ComposeResult

from shoal.game_clients.aurora import get_h1_mod_exec_path, push_install_h1_screen
from shoal.game_clients.alterware import get_t7x_client_path, push_install_alterware_launcher_screen, push_install_t7x_screen
from shoal.data_structures import GameClients, Games
from shoal.game_clients.plutonium import (
    get_plutonium_appdata_dir, 
    push_install_plutonium_screen
)
from shoal.game_clients.game_clients import get_current_client, get_current_selected_game
from shoal.game_clients.nazi_zombies_portable import get_nazi_zombie_portable_executable_path, push_install_nazi_zombies_portable_screen
from shoal import game_runner
from shoal.settings import get_game_directory, get_alterware_launcher_path
from shoal.base_widgets.base_widgets import BaseButton, BaseHorizontalBox
from shoal.general.os_file_browser import open_directory_in_file_browser


class ClientFilesButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BaseButton(button_text="Client Directory", button_width="100%")
        yield self.button

    def on_button_pressed(self) -> None:
        current_game = get_current_selected_game()
        if current_game == Games.CALL_OF_DUTY_NAZI_ZOMBIES_PORTABLE:
            open_directory_in_file_browser(os.path.dirname(get_nazi_zombie_portable_executable_path()))
        elif get_current_client() == GameClients.ALTERWARE:
            if current_game == Games.CALL_OF_DUTY_BLACK_OPS_III:
                open_directory_in_file_browser(os.path.dirname(get_t7x_client_path()))
            else:
                open_directory_in_file_browser(os.path.dirname(get_alterware_launcher_path()))
        elif get_current_client() == GameClients.AURORA:
            open_directory_in_file_browser(os.path.dirname(get_h1_mod_exec_path()))
        else:
            open_directory_in_file_browser(get_plutonium_appdata_dir())


    def on_mount(self):
        self.styles.width = "1fr"


class GameDirectoryButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BaseButton(button_text="Game Directory", button_width="100%")
        yield self.button

    def on_button_pressed(self) -> None:
        game_dir = get_game_directory()
        open_directory_in_file_browser(game_dir)

    def on_mount(self):
        self.styles.width = "1fr"


def installation_check_then_run_game():
        if get_current_selected_game() == Games.CALL_OF_DUTY_BLACK_OPS_III:
            push_install_t7x_screen()
        elif get_current_selected_game() == Games.CALL_OF_DUTY_NAZI_ZOMBIES_PORTABLE:
            push_install_nazi_zombies_portable_screen()
        elif get_current_client() == GameClients.ALTERWARE:
            push_install_alterware_launcher_screen()
        elif get_current_client() == GameClients.AURORA:
            push_install_h1_screen()
        elif get_current_client() == GameClients.PLUTONIUM:
            push_install_plutonium_screen()
        else:
            game_runner.run_game()


class RunGameButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BaseButton(button_text='Run Game', button_width='100%')
        yield self.button

    def on_button_pressed(self) -> None:
        installation_check_then_run_game()

    def on_mount(self):
        self.styles.width = "1fr"


class GameButtonsBar(Static):
    def compose(self) -> ComposeResult:
        with BaseHorizontalBox():
            yield ClientFilesButton()
            yield GameDirectoryButton()
            yield RunGameButton()
