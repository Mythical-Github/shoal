from shoal.logger import print_to_log_window
from shoal.base_widgets import text_input_screen
from shoal.settings import get_usernames, set_username


class UsernameScreen(text_input_screen.TextInputScreen):
    def __init__(self, widget_to_refresh=None):
        super().__init__(
            cancel_function=self.simulate_cancel_username_button_pressed,
            confirm_function=self.simulate_confirm_username_button_pressed,
            input_name="username",
            widget_to_refresh=widget_to_refresh
        )
        self.widget_to_refresh = widget_to_refresh

    def simulate_cancel_username_button_pressed(self, text_input):
        print_to_log_window('Cancelling adding of a new username')

    def simulate_confirm_username_button_pressed(self, text_input):
        text_value = text_input.value

        if not text_value or text_value.strip() == '':
            print_to_log_window('You cannot add a blank username')
        elif text_value in get_usernames():
            print_to_log_window('You cannot add a username that already exists')
        else:
            print_to_log_window(f'Added the following username to the username list "{text_value}"')
            set_username(text_value)
