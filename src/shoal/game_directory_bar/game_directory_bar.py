import os

from textual.widgets import Static
from textual.app import ComposeResult

from shoal.base_widgets.base_widgets import (
    BaseButton,
    BaseHorizontalBox,
    BaseLabel
)
from shoal.logger import print_to_log_window
from shoal.data_structures import SelectionFilter
from shoal.game_directory_bar import game_directory_screen
from shoal.settings import get_game_directory, set_game_directory, get_current_selected_game


def cancel_was_hit(selected_path: str):
    print_to_log_window('Cancelling selection')


def confirm_was_hit(selected_path: str):
    print_to_log_window('The confirm button was pressed')
    dir_path = selected_path

    if not os.path.isdir(dir_path) or dir_path == '.':
        is_not_a_dir_message = f'The following provided directory is invalid: "{dir_path}"'
        print_to_log_window(is_not_a_dir_message)
    else:
        is_a_dir_message = f'The following provided directory: "{dir_path}" was set for the following game: "{get_current_selected_game().value}"'
        set_game_directory(dir_path)
        print_to_log_window(is_a_dir_message)



class SelectGameDirectoryButton(Static):
    def compose(self) -> ComposeResult:
        self.select_game_directory_button = BaseButton(
                button_text="··",
                button_width='6',
                button_border=("none", "black")
            )
        yield self.select_game_directory_button

    def on_mount(self):
        self.styles.width = '6'
        self.select_game_directory_button.styles.padding = 0
        self.select_game_directory_button.styles.margin = 0


    def on_button_pressed(self) -> None:
        from shoal.main_app import app
        app.push_screen(game_directory_screen.SelectionScreen(
            starting_directory='',
            extensions=[],
            selection_filter=SelectionFilter.DIRECTORY,
            cancel_function=cancel_was_hit, 
            confirm_function=confirm_was_hit,
            widgets_to_refresh_on_screen_pop=[app.game_dir_select]
            )
        )


class GameDirectoryBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BaseHorizontalBox()
        self.game_dir_label = BaseLabel("Game Directory:")
        self.game_dir_location_label = BaseLabel(
            get_game_directory(),
            label_width='1fr',
            label_content_align=('left', 'top'),
            label_height='auto'
        )
        self.select_dir_button = SelectGameDirectoryButton()
        with self.horizontal_box:
            yield self.game_dir_label
            yield self.game_dir_location_label
            yield self.select_dir_button

    def on_mount(self):
        self.styles.width = '100%'
        self.styles.height = 'auto'
        self.styles.padding = 0
        self.styles.margin = 0
        self.select_dir_button.styles.text_align = "center"
        self.select_dir_button.styles.align = ("center", "middle")
        self.select_dir_button.styles.content_align = ("center", "middle")
        self.select_dir_button.styles.height = "auto"
