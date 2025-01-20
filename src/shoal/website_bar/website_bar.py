from textual import work
from textual.app import ComposeResult
from textual.widgets import Static

from shoal.base_widgets.base_widgets import (
    BaseButton,
    BaseHorizontalBox
)
from shoal.general.os_web_browser import open_website
from shoal.game_clients.game_clients import (
    get_current_client_docs_link, 
    get_current_client_forum_link,
    get_current_client_github_link
)


class DocsButton(Static):
    def compose(self) -> ComposeResult:
        self.docs_button = BaseButton(button_text="Docs", button_width="100%")
        yield self.docs_button
    def on_button_pressed(self) -> None:
        url = get_current_client_docs_link()
        open_website(url)

    def on_mount(self):
        self.styles.width = "1fr"


class ForumsButton(Static):
    def compose(self) -> ComposeResult:
        self.forums_button = BaseButton(button_text="Forums", button_width="100%")
        yield self.forums_button
    def on_button_pressed(self) -> None:
        url = get_current_client_forum_link()
        open_website(url)

    def on_mount(self):
        self.styles.width = "1fr"


class GithubButton(Static):
    def compose(self) -> ComposeResult:
        self.github_button = BaseButton(button_text="Github", button_width="100%")
        yield self.github_button
    def on_button_pressed(self) -> None:
        open_website(get_current_client_github_link())

    def on_mount(self):
        self.styles.width = "1fr"


def print_test_two():
    from shoal.logger import print_to_log_window
    print_to_log_window('test finished')


def print_test():
    from shoal.logger import print_to_log_window
    from time import sleep
    sleep(.1)
    print_to_log_window('testing')


class TestingButton(Static):
    def compose(self) -> ComposeResult:
        self.github_button = BaseButton(button_text="Testing", button_width="100%")
        yield self.github_button

    def on_button_pressed(self) -> None:
        from shoal.base_widgets import setup_screen
        from shoal.main_app import app
        self.steps_to_functions = {
            "test": print_test,
            "test1": print_test,
            "test2": print_test,
            "test3": print_test,
            "test4": print_test,
            "test5": print_test
        }

        self.final_function = print_test_two
        self.widgets_to_refresh_on_pop = []
        self.setup_screen = setup_screen.SetupScreen(
            step_text_to_step_functions=self.steps_to_functions,
            finished_all_steps_function=self.final_function,
            widgets_to_refresh_on_screen_pop=self.widgets_to_refresh_on_pop
        )
        app.push_screen(self.setup_screen)

    def on_mount(self):
        self.styles.width = "1fr"


class WebsiteBar(Static):
    def compose(self) -> ComposeResult:
        with BaseHorizontalBox(padding=(0)):
            yield DocsButton()
            yield GithubButton()
            yield ForumsButton()
            yield TestingButton()
