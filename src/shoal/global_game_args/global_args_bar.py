from textual.app import ComposeResult
from textual.widgets import Select, Static

from shoal.general.file_io import remove_line_from_config
from shoal import data_structures
from shoal.base_widgets.base_widgets import (
    BaseButton,
    BaseHorizontalBox,
    BaseLabel,
)
from shoal.logger import print_to_log_window
from shoal.game_clients.plutonium import get_plutonium_modern_warfare_iii_config_path
from shoal.settings import (
    get_current_selected_game,
    get_global_args
)


class AddGlobalArgButton(Static):
    def compose(self) -> ComposeResult:
        self.add_global_arg_button = BaseButton(button_text="+", button_width="auto")
        yield self.add_global_arg_button

    def on_mount(self):
        self.styles.width = 'auto'

    def on_button_pressed(self) -> None:
        from shoal.main_app import app
        from shoal.global_game_args import global_args_screen
        app.push_screen(global_args_screen.GlobalArgsScreen(widget_to_refresh=self.parent.parent))


def allow_global_args_blank() -> bool:
    if len(get_global_args()) == 0:
        return True
    else:
        return False


class RemoveGlobalArgButton(Static):
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
        from shoal.settings import remove_global_arg

        options = app.global_args_section.options

        if not len(options) > 0:
            print_to_log_window('You cannot remove a non-existent argument')
            return
        global_arg = options[app.global_args_section.combo_box.value][0]
        print_to_log_window(f'Attempting to remove the following global argument: "{global_arg}"')


        remove_global_arg(global_arg)
        if get_current_selected_game().value == data_structures.Games.CALL_OF_DUTY_MODERN_WARFARE_III_2011.value:
            remove_line_from_config(get_plutonium_modern_warfare_iii_config_path(), global_arg)
        app.global_args_section.refresh(recompose=True)


class GlobalArgsSection(Static):
    def compose(self) -> ComposeResult:

        self.options = []

        for arg_index, arg in enumerate(get_global_args()):
            self.options.append((arg, arg_index))


        self.combo_box: Select[int] = Select(self.options, allow_blank=allow_global_args_blank(), prompt='None')

        self.add_button = AddGlobalArgButton()

        self.remove_button = RemoveGlobalArgButton()

        with BaseHorizontalBox():
            yield BaseLabel(label_text="Global Game Args:", label_height="auto")
            yield self.combo_box
            yield self.remove_button
            yield self.add_button
