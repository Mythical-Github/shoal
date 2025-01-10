from shoal.logger import print_to_log_window
from shoal.base_widgets import text_input_screen
from shoal.settings import add_game_specific_arg, get_game_specific_args


class GameArgsScreen(text_input_screen.TextInputScreen):
    def __init__(self, widget_to_refresh=None):
        super().__init__(
            cancel_function=self.cancel,
            confirm_function=self.confirm,
            input_name="game argument",
            widget_to_refresh=widget_to_refresh
        )
        self.widget_to_refresh = widget_to_refresh

    def cancel(self, text_input):
        print_to_log_window('Cancelling adding of a game argument')

    def confirm(self, text_input):
        text_value = text_input.value.strip()
        if not text_input or text_value.strip() == '':
            print_to_log_window('You cannot add a blank argument')
        elif text_value in get_game_specific_args():
            print_to_log_window('You cannot add a game argument that already exists')
        else:
            add_game_specific_arg(text_value)
            print_to_log_window(f'Added the following game argument "{text_value}"')
