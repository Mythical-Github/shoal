from typing import Callable, Any, Tuple

from textual import on
from textual.widget import Widget
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Vertical
from textual.widgets import Header, Static, TextArea, DirectoryTree

from shoal.data_structures import SelectionFilter
from shoal.general.file_io import get_all_drive_letter_paths, get_drive_name
from shoal.base_widgets.base_widgets import BaseButton, BaseHorizontalBox


class SelectionScreen(Screen):
    def __init__(
        self,
        starting_directory: str,
        extensions: list[str],
        selection_filter: SelectionFilter,
        confirm_function: Callable[[str, *Tuple[Any, ...]], Any],
        cancel_function: Callable[[str, *Tuple[Any, ...]], Any],
        widgets_to_refresh_on_screen_pop: list[Widget]
        
    ):
        super().__init__()
        self.starting_directory = starting_directory
        self.extensions = extensions
        self.selection_filter = selection_filter
        self.confirm_function = confirm_function
        self.cancel_function = cancel_function
        self.confirm_function = confirm_function
        self.widgets_to_refresh_on_screen_pop = widgets_to_refresh_on_screen_pop

    def compose(self) -> ComposeResult:
        self.header = Header()
        self.vertical_scroll = Vertical()
        self.picker = Picker(
            starting_directory=self.starting_directory,
            extensions=[],
            selection_filter=self.selection_filter,
            cancel_function=self.cancel_function,
            confirm_function=self.confirm_function,
            widgets_to_refresh_on_screen_pop=self.widgets_to_refresh_on_screen_pop
        )
        with self.vertical_scroll:
            yield self.header
            yield self.picker

    def on_mount(self):
        self.styles.border = ("solid", "grey")
        self.vertical_scroll.height = '100%'


class CurrentDirectoryBar(Static):
    def __init__(
        self,
        starting_directory: str
    ):
        super().__init__()
        self.starting_directory = starting_directory


    def compose(self) -> ComposeResult:
        self.text_area = TextArea(text=str(self.parent.selected_path))
        self.vertical = Vertical()
        with self.vertical:
            yield self.text_area

    def on_mount(self):
        self.vertical.styles.height = 'auto'
        self.styles.height = 'auto'
        self.styles.margin = (1, 0, 0, 0)
        self.text_area.styles.height = 'auto'
        self.text_area.styles.border = ("solid", "grey")
        self.text_area.border_title = "Current Selection"


class CancelButton(Static):
    def __init__(
        self,
        cancel_function
    ):
        super().__init__()
        self.cancel_function = cancel_function

    def compose(self) -> ComposeResult:
        self.cancel_button = BaseButton(button_text='Cancel', button_width='1fr')
        yield self.cancel_button

    def on_mount(self):
        self.cancel_button.styles.width = '1fr'
        self.styles.width = '1fr'
        self.styles.height = 'auto'

    def on_button_pressed(self) -> None:
        simulate_cancel_button_pressed(self.cancel_function)
        post_cancel_button_pressed()


class ConfirmButton(Static):
    def __init__(
        self,
        confirm_function,
        widgets_to_refresh
    ):
        super().__init__()
        self.confirm_function = confirm_function
        self.widgets_to_refresh = widgets_to_refresh

    def compose(self) -> ComposeResult:
        self.confirm_button = BaseButton(button_text='Confirm', button_width='1fr')
        yield self.confirm_button

    def on_mount(self):
        self.confirm_button.styles.width = '1fr'
        self.styles.width = '1fr'
        self.styles.height = 'auto'

    def on_button_pressed(self) -> None:
        simulate_confirm_button_pressed(self.confirm_function)
        post_confirm_button_pressed(widgets_to_refresh=self.widgets_to_refresh)


last_path = ''
def get_current_selected_path() -> str:
    global last_path
    return last_path


def post_cancel_button_pressed():
    from shoal.main_app import app
    app.pop_screen()


def post_confirm_button_pressed(widgets_to_refresh: list[Widget]):
    from shoal.main_app import app
    for widget in widgets_to_refresh:
        widget.refresh(recompose=True)
    app.pop_screen()


def simulate_cancel_button_pressed(function):
    function(get_current_selected_path())


def simulate_confirm_button_pressed(function):
    function(get_current_selected_path())


class CancelConfirmHorizontalBar(Static):
    def __init__(
        self,
        confirm_function: Callable[[str, *Tuple[Any, ...]], Any],
        cancel_function: Callable[[str, *Tuple[Any, ...]], Any],
        widgets_to_refresh
    ):
        super().__init__()

        self.cancel_function = cancel_function
        self.confirm_function = confirm_function
        self.widgets_to_refresh = widgets_to_refresh

    def compose(self) -> ComposeResult:
        self.horizontal_box = BaseHorizontalBox(padding=0)
        self.confirm_button = ConfirmButton(self.confirm_function, widgets_to_refresh=self.widgets_to_refresh)
        self.cancel_button = CancelButton(self.cancel_function)
        with self.horizontal_box:
            yield self.cancel_button
            yield self.confirm_button
        yield self.horizontal_box

    def on_mount(self):
        self.horizontal_box.styles.height = 'auto'
        # self.styles.margin = (0, 1, 0, 1)


class Picker(Static):
    def __init__(
        self,
        starting_directory: str,
        extensions: list[str],
        selection_filter: SelectionFilter,
        confirm_function: Callable[[str, *Tuple[Any, ...]], Any],
        cancel_function: Callable[[str, *Tuple[Any, ...]], Any],
        widgets_to_refresh_on_screen_pop: list[Widget]
    ):
        super().__init__()
        self.starting_directory = starting_directory
        self.extensions = extensions
        self.selection_filter = selection_filter
        self.confirm_function = confirm_function
        self.cancel_function = cancel_function
        self.confirm_function = confirm_function
        self.widgets_to_refresh_on_screen_pop = widgets_to_refresh_on_screen_pop
        self.selected_path = ''

    def compose(self) -> ComposeResult:
        self.vertical_box = VerticalScroll()
        self.current_directory_bar = CurrentDirectoryBar(starting_directory=self.starting_directory)
        self.dir_tree_widgets_to_drive_paths = {}
        for drive_letter in get_all_drive_letter_paths():
            directory_tree = DirectoryTree(path=drive_letter)
            self.dir_tree_widgets_to_drive_paths[directory_tree] = drive_letter


        self.cancel_confirm_horizontal_bar = CancelConfirmHorizontalBar(
            cancel_function=self.cancel_function, 
            confirm_function=self.confirm_function,
            widgets_to_refresh=self.widgets_to_refresh_on_screen_pop
        )
        yield self.current_directory_bar
        with self.vertical_box:
            for dir_tree_widget in self.dir_tree_widgets_to_drive_paths.keys():
                yield dir_tree_widget
        yield self.cancel_confirm_horizontal_bar
    
    def on_mount(self):
        self.vertical_box.styles.height = '1fr'
        self.vertical_box.styles.border = ('solid', 'grey')
        for dir_tree_widget in self.dir_tree_widgets_to_drive_paths.keys():
            dir_tree_widget.styles.border = ('solid', 'grey')
            dir_tree_widget.styles.height = 'auto'
            drive_letter = self.dir_tree_widgets_to_drive_paths[dir_tree_widget][:-1]
            drive_name = get_drive_name(drive_letter)
            dir_tree_widget.border_title = f'{drive_name} ({drive_letter})'

    @on(DirectoryTree.DirectorySelected)
    def directory_selected(self, event: DirectoryTree.DirectorySelected):
        self.selected_path = str(event.path)
        self.current_directory_bar.text_area.text = self.selected_path
        global last_path
        last_path = self.selected_path

    @on(DirectoryTree.FileSelected)
    def file_selected(self, event: DirectoryTree.FileSelected):
        self.selected_path = str(event.path)
        self.current_directory_bar.text_area.text = self.selected_path
        global last_path
        last_path = self.selected_path
