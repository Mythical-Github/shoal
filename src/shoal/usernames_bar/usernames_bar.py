from textual.app import ComposeResult
from textual.widgets import Select, Static

from shoal.base_widgets.base_widgets import (
    BaseButton,
    BaseHorizontalBox,
    BaseLabel
)
from shoal.logger import print_to_log_window
from shoal.settings import get_current_username, get_usernames


class AddUserButton(Static):
    def compose(self) -> ComposeResult:
        self.add_button = BaseButton(button_text="+", button_width="auto")
        yield self.add_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.add_button.styles.height = "auto"
        self.add_button.styles.text_align = "center"
        self.add_button.styles.align = ("center", "middle")
        self.add_button.styles.content_align = ("center", "middle")

    def on_button_pressed(self) -> None:
        from shoal.main_app import app
        from shoal.usernames_bar import usernames_screen
        app.push_screen(usernames_screen.UsernameScreen(widget_to_refresh=self.parent.parent))


class RemoveUserButton(Static):
    def compose(self) -> ComposeResult:
        self.add_button = BaseButton(button_text="-", button_width="auto")
        yield self.add_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.add_button.styles.height = "auto"
        self.add_button.styles.text_align = "center"
        self.add_button.styles.align = ("center", "middle")
        self.add_button.styles.content_align = ("center", "middle")

    def on_button_pressed(self) -> None:
        from shoal.settings import remove_username
        username_bar = self.parent.parent
        username = username_bar.options[username_bar.usernames_combo_box.value][0]

        print_to_log_window(f'Attempting to remove the following username: "{username}"')
        remove_username(username)
        username_bar.refresh(recompose=True)


class UsernameBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BaseHorizontalBox(padding=(1, 0, 0, 0), width="100%")
        self.user_label = BaseLabel(label_text="User:", label_height="auto")
        self.options = []
        for index, username in enumerate(get_usernames()):
            self.options.append((username, index))

        main_value = None
        current_username = get_current_username()

        for entry in self.options:
            if entry[0] == current_username:
                main_value = entry[1]
                break
            else:
                error_message = 'The currently selected game is invalid.'
                RuntimeWarning(error_message)

        self.usernames_combo_box: Select[int] = Select(options=self.options, allow_blank=False, value=main_value)
        self.add_button = AddUserButton()
        self.remove_button = RemoveUserButton()
        with self.horizontal_box:
            yield self.user_label
            yield self.usernames_combo_box
            yield self.remove_button
            yield self.add_button
        yield self.horizontal_box


    def on_mount(self):
        self.add_button.styles.height = "100%"
        self.remove_button.styles.height = "100%"
