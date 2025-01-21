from textual import on
from textual.app import ComposeResult
from textual.widgets import Select, Static

from shoal import data_structures
from shoal.base_widgets.base_widgets import (
    BaseHorizontalBox,
    BaseLabel
)
from shoal.logger import print_to_log_window
from shoal.game_clients.game_clients import get_game_selector_options

from shoal.settings import (
    get_current_selected_game,
    set_current_selected_game
)


class GameSelector(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BaseHorizontalBox()
        self.game_mode_label = BaseLabel("Game:")
        
        self.options = get_game_selector_options()
        
        main_value = None
        current_game = get_current_selected_game().value
        
        for entry in self.options:
            if entry[0] == current_game:
                main_value = entry[1]
                break
        else:
            error_message = f'The currently selected game is invalid. {current_game}'
            raise ValueError(error_message)
        
        self.my_select: Select[int] = Select(self.options, allow_blank=False, value=main_value)
        
        with self.horizontal_box:
            yield self.game_mode_label
            yield self.my_select


    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        from shoal.main_app import app

        set_current_selected_game(data_structures.get_enum_from_val(data_structures.Games, self.options[event.value][0]))
        app.game_mode_selector.refresh(recompose=True)
        app.game_dir_select.refresh(recompose=True)
        app.game_args_section.refresh(recompose=True)
        print_to_log_window(f'Loaded settings for "{get_current_selected_game().value}"')
            

    def on_mount(self):
        self.my_select.styles.content_align = ("center", "middle")
        self.my_select.styles.align = ("center", "middle")
        self.my_select.styles.height = "auto"
