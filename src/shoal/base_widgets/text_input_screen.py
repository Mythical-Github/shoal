from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header, Input, Static

from shoal.base_widgets.base_widgets import (
    BaseButton,
    BaseHorizontalBox,
    BaseLabel,
)


class ConfirmButton(Static):
    def __init__(
        self,
        confirm_function
    ):
        super().__init__()
        self.confirm_function = confirm_function
    def compose(self) -> ComposeResult:
        self.confirm_button = BaseButton(button_text='Confirm')
        yield self.confirm_button

    def on_mount(self):
        self.confirm_button.styles.width = 'auto'
        self.styles.width = 'auto'
        self.styles.height = 'auto'

    def on_button_pressed(self) -> None:
        simulate_confirm_button_pressed(self.confirm_function)
        post_confirm_button_pressed()


main_text_input = None
def get_screen_text_input():
    global main_text_input
    return main_text_input


global_widget_to_refresh = None
def get_widget_to_refresh():
    global global_widget_to_refresh
    return global_widget_to_refresh


def post_cancel_button_pressed():
    from shoal.main_app import app
    get_screen_text_input().value = ''
    app.pop_screen()


def post_confirm_button_pressed():
    from shoal.main_app import app
    get_screen_text_input().value = ''
    get_widget_to_refresh().refresh(recompose=True)
    app.pop_screen()


def simulate_cancel_button_pressed(function):
    function(get_screen_text_input())


def simulate_confirm_button_pressed(function):
    function(get_screen_text_input())



class CancelButton(Static):
    def __init__(
        self,
        cancel_function
    ):
        super().__init__()
        self.cancel_function = cancel_function
    def compose(self) -> ComposeResult:
        self.cancel_button = BaseButton(button_text='Cancel')
        yield self.cancel_button

    def on_mount(self):
        self.styles.width = 'auto'
        self.styles.height = 'auto'
        self.cancel_button.styles.width = 'auto'

    def on_button_pressed(self) -> None:
        simulate_cancel_button_pressed(self.cancel_function)
        post_cancel_button_pressed()


class TextInputScreenInput(Input):
    def __init__(
        self,
        confirm_function
    ):
        super().__init__()
        self.confirm_function = confirm_function
    @on(Input.Submitted)
    def on_input_changed(self):
        simulate_confirm_button_pressed(self.confirm_function)
        post_confirm_button_pressed()

main_layout = None
def get_main_layout():
    global main_layout
    return main_layout


class TextInputMainLayout(Static):
    def __init__(
        self,
        cancel_function,
        confirm_function,
        input_name,
        widget_to_refresh
    ):
        super().__init__()
        self.cancel_function = cancel_function
        self.confirm_function = confirm_function
        self.input_name = input_name
        self.widget_to_refresh = widget_to_refresh
    BINDINGS = [
        ("escape", "cancel", "Simulates hitting the cancel button")
    ]
    def compose(self) -> ComposeResult:
        self.label = BaseLabel(
            label_text=f'Input the {self.input_name}',
            label_border=('hidden', 'grey'),
            label_padding=(0, 0, 1, 0)
        )
        self.text_input = TextInputScreenInput(self.confirm_function)
        self.vertical_scrollbox = VerticalScroll()
        self.horizontal_bar = BaseHorizontalBox(padding=0)
        self.cancel_button = CancelButton(self.cancel_function)
        self.confirm_button = ConfirmButton(self.confirm_function)
        with self.vertical_scrollbox:
            yield self.label
            with self.horizontal_bar:
                yield self.text_input
                yield self.cancel_button
                yield self.confirm_button
            yield self.horizontal_bar
        yield self.vertical_scrollbox

        global main_text_input
        main_text_input = self.text_input
        global global_widget_to_refresh
        global_widget_to_refresh = self.widget_to_refresh

    def on_mount(self):
        self.label.styles.width = '100%'
        self.horizontal_bar.styles.align = ('center', 'middle')
        self.vertical_scrollbox.styles.align = ('center', 'middle')
        self.vertical_scrollbox.styles.content_align = ('center', 'middle')
        self.text_input.styles.width = '1fr'
        self.horizontal_bar.styles.border = ('solid', 'grey')

        global main_text_input
        main_text_input = self.text_input
        global global_widget_to_refresh
        global_widget_to_refresh = self.widget_to_refresh

    def action_cancel(self):
        simulate_cancel_button_pressed(self.cancel_function)
        post_cancel_button_pressed()


class TextInputScreen(Screen):
    def __init__(
        self,
        cancel_function,
        confirm_function,
        input_name,
        widget_to_refresh
    ):
        super().__init__()
        self.cancel_function = cancel_function
        self.confirm_function = confirm_function
        self.input_name = input_name
        self.widget_to_refresh = widget_to_refresh

    def compose(self) -> ComposeResult:
        self.header = Header()
        self.text_input_main_layout = TextInputMainLayout(self.cancel_function, self.confirm_function, self.input_name, self.widget_to_refresh)
        self.vertical_scroll = VerticalScroll()
        with self.vertical_scroll:
            yield self.header
            yield self.text_input_main_layout
        yield self.vertical_scroll
        global main_layout
        main_layout = self.text_input_main_layout

    def on_mount(self):
        self.vertical_scroll.styles.margin = 0
        self.vertical_scroll.styles.padding = 0
        self.vertical_scroll.styles.border = ("solid", "grey")
        self.vertical_scroll.styles.align = ('center', 'middle')

    def _on_screen_resume(self):
        self.screen.set_focus(self.text_input_main_layout.text_input)
        return super()._on_screen_resume()
