from shoal.logger import print_to_log_window
from shoal.base_widgets import text_input_screen
from shoal.settings import add_global_arg, get_global_args


class GlobalArgsScreen(text_input_screen.TextInputScreen):
    def __init__(self, widget_to_refresh=None):
        super().__init__(
            cancel_function=self.cancel,
            confirm_function=self.confirm,
            input_name="global argument",
            widget_to_refresh=widget_to_refresh
        )
        self.widget_to_refresh = widget_to_refresh

    def cancel(self, text_input):
        print_to_log_window('Cancelling adding of a new global argument')

    def confirm(self, text_input):
        text_value = text_input.value

        if not text_input or text_value.strip() == '':
            print_to_log_window('You cannot add a blank argument')
        elif text_value in get_global_args():
            print_to_log_window('You cannot add a global argument that already exists')
        else:
            add_global_arg(text_value)
            print_to_log_window(f'Added the following global argument "{text_value}"')

        text_input.value = ''
