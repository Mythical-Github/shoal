import os

from textual.widgets import Static
from textual.app import ComposeResult

from shoal.game_clients.aurora import get_h1_mod_exec_path
from shoal.game_clients.alterware import get_t7x_client_path
from shoal.data_structures import GameClients, Games
from shoal.game_clients.plutonium import get_plutonium_appdata_dir
from shoal.game_clients.game_clients import get_current_client, get_current_selected_game
from shoal.game_clients.nazi_zombies_portable import get_nazi_zombie_portable_executable_path
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
        from shoal.main_app import app
        from shoal.base_widgets import setup_screen
        from shoal.game_clients.alterware import download_t7x_client, get_t7x_client_path
        from shoal.game_clients.nazi_zombies_portable import (
            get_nazi_zombie_portable_executable_path,
            installing_nzp_step_one,
            installing_nzp_step_two,
            installing_nzp_step_three
        )
        if get_current_selected_game() == Games.CALL_OF_DUTY_BLACK_OPS_III:
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
        elif get_current_selected_game() == Games.CALL_OF_DUTY_NAZI_ZOMBIES_PORTABLE:
            if not os.path.isfile(get_nazi_zombie_portable_executable_path()):
                self.steps = {
                            "Downloading Nazi Zombies Portable...": installing_nzp_step_one,
                            "Unzipping Nazi Zombies Portable...": installing_nzp_step_two,
                            "Cleaning up Nazi Zombies Portable Installation...": installing_nzp_step_three,
                        }
                download_nzp_screen = setup_screen.SetupScreen(
                        step_text_to_step_functions=self.steps,
                        finished_all_steps_function=game_runner.run_game,
                        widgets_to_refresh_on_screen_pop=[],
                        screen_label_text="Nazi Zombies Portable Setup:"
                    )
                app.push_screen(download_nzp_screen)
            else:
                game_runner.run_game()
        elif get_current_client() == GameClients.ALTERWARE:
            from shoal.settings import SCRIPT_DIR
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
        elif get_current_client() == GameClients.AURORA:
            from shoal.game_clients.aurora import get_h1_mod_exec_path, download_h1_mod
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
        else:
            game_runner.run_game()

    def on_mount(self):
        self.styles.width = "33%"


class GameButtonsBar(Static):
    def compose(self) -> ComposeResult:
        with BaseHorizontalBox():
            yield ClientFilesButton()
            yield GameDirectoryButton()
            yield RunGameButton()
