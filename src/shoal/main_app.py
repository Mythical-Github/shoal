from textual.widgets import Header
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll

from shoal import auto_run_thread, logger
from shoal.website_bar.website_bar import WebsiteBar
from shoal.game_selector.game_selector import GameSelector
from shoal.game_buttons_bar.game_buttons_bar import GameButtonsBar
from shoal.global_game_args.global_args_bar import GlobalArgsSection
from shoal.game_directory_bar.game_directory_bar import GameDirectoryBar
from shoal.game_mode_selector.game_mode_selector import GameModeSelector
from shoal.auto_run_game_bar.auto_run_game_bar import GameAutoExecuteBar
from shoal.usernames_bar.usernames_bar import UsernameBar
from shoal.game_specific_game_args.game_specific_args_bar import GameSpecificArgsSection
from shoal.customization import set_terminal_size, set_window_title, enable_vt100
from shoal.settings import get_current_preferred_theme, get_title_for_app


class Shoal(App):
    TITLE = get_title_for_app()
    def compose(self) -> ComposeResult:
        self.main_vertical_scroll_box_zero = VerticalScroll()
        self.game_selector = GameSelector()
        self.game_mode_selector = GameModeSelector()
        self.game_dir_select = GameDirectoryBar()
        self.username_bar = UsernameBar()
        self.global_args_section = GlobalArgsSection()
        self.game_args_section = GameSpecificArgsSection()
        self.game_buttons_bar = GameButtonsBar()
        self.website_bar = WebsiteBar()
        self.auto_run_game_bar = GameAutoExecuteBar()
        with self.main_vertical_scroll_box_zero:
            yield Header()
            yield self.game_selector
            yield self.game_mode_selector
            yield self.game_dir_select
            yield self.username_bar
            yield self.global_args_section
            yield self.game_args_section
            yield self.auto_run_game_bar
            yield self.game_buttons_bar
            yield self.website_bar
            yield logger.logger

    def on_mount(self):
        self.main_vertical_scroll_box_zero.styles.margin = 0
        self.main_vertical_scroll_box_zero.styles.padding = 0
        self.main_vertical_scroll_box_zero.styles.border = ("solid", "grey")
        self.theme = get_current_preferred_theme()
        auto_run_thread.has_initially_set_theme = True


def configure_app():
    set_window_title(get_title_for_app())
    enable_vt100()
    # 52x60 columns/rows in terminal
    set_terminal_size(app, 420, 680)


def run_main_app():
    configure_app()
    auto_run_thread.start_periodic_check_thread(app)
    app.run()


app = Shoal()
