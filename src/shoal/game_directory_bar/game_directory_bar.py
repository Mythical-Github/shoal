from textual.app import ComposeResult
from textual.widgets import Static

from shoal.base_widgets.base_widgets import (
    BaseButton,
    BaseHorizontalBox,
    BaseLabel
)

from shoal.settings import get_game_directory


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
        from shoal.game_directory_bar import game_directory_screen
        app.push_screen(game_directory_screen.GameDirectoryScreen(widget_to_refresh=self.parent.parent))


class GameDirectoryBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BaseHorizontalBox()
        with self.horizontal_box:
            self.game_dir_label = BaseLabel("Game Directory:")
            self.game_dir_location_label = BaseLabel(
                get_game_directory(),
                label_width='1fr',
                label_content_align=('left', 'top'),
                label_height='auto'
            )
            self.select_dir_button = SelectGameDirectoryButton()
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
