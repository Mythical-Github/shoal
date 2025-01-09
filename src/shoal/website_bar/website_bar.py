from textual.app import ComposeResult
from textual.widgets import Static

from shoal.base_widgets.base_widgets import (
    BaseButton,
    BaseHorizontalBox
)
from shoal.general.os_web_browser import open_website
from shoal.game_clients import get_current_client_docs_link, get_current_client_forum_link


class DocsButton(Static):
    def compose(self) -> ComposeResult:
        self.docs_button = BaseButton(button_text="Docs", button_width="100%")
        yield self.docs_button
    def on_button_pressed(self) -> None:
        url = get_current_client_docs_link()
        open_website(url)

    def on_mount(self):
        self.styles.width = "33%"


class ForumsButton(Static):
    def compose(self) -> ComposeResult:
        self.forums_button = BaseButton(button_text="Forums", button_width="100%")
        yield self.forums_button
    def on_button_pressed(self) -> None:
        url = get_current_client_forum_link()
        open_website(url)

    def on_mount(self):
        self.styles.width = "33%"


class GithubButton(Static):
    def compose(self) -> ComposeResult:
        self.github_button = BaseButton(button_text="Github", button_width="100%")
        yield self.github_button
    def on_button_pressed(self) -> None:
        url = "https://github.com/Mythical-Github/shoal"
        open_website(url)

    def on_mount(self):
        self.styles.width = "33%"


class WebsiteBar(Static):
    def compose(self) -> ComposeResult:
        with BaseHorizontalBox(padding=(0)):
            yield DocsButton()
            yield GithubButton()
            yield ForumsButton()
