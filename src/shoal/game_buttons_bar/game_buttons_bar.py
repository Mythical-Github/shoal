import os

from textual.widgets import Static
from textual.app import ComposeResult

from shoal.data_structures import GameClients
from shoal.game_clients import get_plutonium_appdata_dir, get_current_client
from shoal import game_runner
from shoal.settings import get_game_directory, get_alterware_launcher_path
from shoal.base_widgets.base_widgets import BaseButton, BaseHorizontalBox
from shoal.general.os_file_browser import open_directory_in_file_browser


class ClientFilesButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BaseButton(button_text="Client Directory", button_width="100%")
        yield self.button

    def on_button_pressed(self) -> None:
        if get_current_client() == GameClients.ALTERWARE:
            open_directory_in_file_browser(os.path.dirname(get_alterware_launcher_path()))
        else:
            open_directory_in_file_browser(get_plutonium_appdata_dir())


    def on_mount(self):
        self.styles.width = "33%"


class GameDirectoryButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BaseButton(button_text="Game Directory", button_width="100%")
        yield self.button

    def on_button_pressed(self) -> None:
        game_dir = get_game_directory()
        open_directory_in_file_browser(game_dir)

    def on_mount(self):
        self.styles.width = "33%"


class RunGameButton(Static):
    def compose(self) -> ComposeResult:
        self.button = BaseButton(button_text='Run Game', button_width='100%')
        yield self.button

    def on_button_pressed(self) -> None:
        game_runner.run_game()

    def on_mount(self):
        self.styles.width = "33%"


class GameButtonsBar(Static):
    def compose(self) -> ComposeResult:
        with BaseHorizontalBox():
            yield ClientFilesButton()
            yield GameDirectoryButton()
            yield RunGameButton()
