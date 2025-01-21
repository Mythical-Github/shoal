from textual import on
from textual.app import ComposeResult
from textual.widgets import Select, Static

from shoal import data_structures
from shoal.base_widgets.base_widgets import (
    BaseHorizontalBox,
    BaseLabel
)
from shoal.logger import print_to_log_window
from shoal.game_clients.game_clients import get_game_mode_options
from shoal.settings import (
    get_current_selected_game,
    get_currently_selected_game_mode,
    set_currently_selected_game_mode
)


class GameModeSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BaseHorizontalBox()
        self.game_mode_label = BaseLabel("Game Mode:")

        self.options = get_game_mode_options()

        main_value = None
        current_game = get_currently_selected_game_mode().value

        for entry in self.options:
            if entry[0] == current_game:
                main_value = entry[1]
                break
            else:
                error_message = 'The currently selected game is invalid.'
                RuntimeWarning(error_message)

        self.my_select: Select[int] = Select(self.options, allow_blank=False, value=main_value)
        with self.horizontal_box:
            yield self.game_mode_label
            yield self.my_select


    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        if get_currently_selected_game_mode() != data_structures.get_enum_from_val(data_structures.GameModes, self.options[event.value][0]):
            set_currently_selected_game_mode(data_structures.get_enum_from_val(data_structures.GameModes, self.options[event.value][0]))
            print_to_log_window(f'Changed selected game mode for "{get_current_selected_game().value}" to "{get_currently_selected_game_mode().value}"')


    def on_mount(self):
        self.my_select.styles.content_align = ("center", "middle")
        self.my_select.styles.align = ("center", "middle")
        self.my_select.styles.height = "auto"
