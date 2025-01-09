from textual.app import ComposeResult
from textual.widgets import Select, Static

from shoal.base_widgets.base_widgets import (
    BaseButton,
    BaseHorizontalBox,
    BaseLabel,
)
from shoal.logger import print_to_log_window
from shoal.settings import get_game_specific_args


class AddGameArgButton(Static):
    def compose(self) -> ComposeResult:
        self.add_game_arg_button = BaseButton(button_text="+", button_width="auto")
        yield self.add_game_arg_button

    def on_mount(self):
        self.styles.width = 'auto'

    def on_button_pressed(self) -> None:
        from shoal.main_app import app
        from shoal.game_specific_game_args import game_args_screen
        app.push_screen(game_args_screen.GameArgsScreen(widget_to_refresh=self.parent.parent))


class RemoveGameArgButton(Static):
    def compose(self) -> ComposeResult:
        self.remove_button = BaseButton(button_text="-", button_width="auto")
        yield self.remove_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.remove_button.styles.height = "auto"
        self.remove_button.styles.text_align = "center"
        self.remove_button.styles.align = ("center", "middle")
        self.remove_button.styles.content_align = ("center", "middle")

    def on_button_pressed(self) -> None:
        from shoal.main_app import app
        from shoal.settings import remove_game_specific_arg

        options = app.game_args_section.options

        if not len(options) > 0:
            print_to_log_window('You cannot remove a non-existent argument')
            return

        game_arg = options[app.game_args_section.combo_box.value][0]

        print_to_log_window(f'Attempting to remove the following game specific argument: "{game_arg}"')
        remove_game_specific_arg(game_arg)
        app.game_args_section.refresh(recompose=True)


def allow_game_args_blank() -> bool:
    return len(get_game_specific_args()) == 0


class GameSpecificArgsSection(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BaseHorizontalBox()

        self.options = []

        for arg_index, arg in enumerate(get_game_specific_args()):
            self.options.append((arg, arg_index))

        self.combo_box: Select[int] = Select(self.options, allow_blank=allow_game_args_blank(), prompt='None')

        self.game_args_label = BaseLabel(label_text="Game Args:", label_height="auto")

        self.add_button = AddGameArgButton()

        self.remove_button = RemoveGameArgButton()

        with self.horizontal_box:
            yield self.game_args_label
            yield self.combo_box
            yield self.remove_button
            yield self.add_button
        yield self.horizontal_box

    def on_mount(self):
        self.game_args_label.styles.height = "auto"
