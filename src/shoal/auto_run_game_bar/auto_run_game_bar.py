from textual import on
from textual_spinbox import SpinBox
from textual.app import ComposeResult
from textual.widgets import Checkbox, Static

from shoal.base_widgets.base_widgets import (
    BaseHorizontalBox,
    BaseLabel
)
from shoal.logger import print_to_log_window
from shoal.settings import (
    get_auto_run_game,
    get_auto_run_game_delay,
    get_use_staging,
    set_auto_run_game,
    set_use_staging
)


def generate_spinbox_numbers():
    current = 0.1
    max_num = 999
    while current <= (max_num):
        yield round(current, 1)
        current += 0.1


class AutoRunGameCheckBox(Static):
    def compose(self) -> ComposeResult:
        self.checkbox = Checkbox(value=get_auto_run_game())
        yield self.checkbox

    def on_mount(self):
        self.styles.width = 'auto'

    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        set_auto_run_game(event.value)
        check_box_changed_message = f'Auto Run Game changed to "{event.value}"'
        print_to_log_window(check_box_changed_message)


class StagingCheckBox(Static):
    def compose(self) -> ComposeResult:
        self.checkbox = Checkbox(value=get_use_staging())
        yield self.checkbox

    def on_mount(self):
        self.styles.width = 'auto'


    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        set_use_staging(event.value)
        check_box_changed_message = f'Use Testing Branch changed to "{event.value}"'
        print_to_log_window(check_box_changed_message)

delay_spinbox = None
def get_spinbox():
    global delay_spinbox
    return delay_spinbox


class GameAutoExecuteBar(Static):
    def compose(self) -> ComposeResult:
        self.horizontal_box = BaseHorizontalBox(width="100%")
        with self.horizontal_box:
            self.auto_execute_label = BaseLabel(
                "Auto Run Game:",
                label_content_align=("left", "middle"),
                label_width="auto"
            )
            self.auto_execute_checkbox = AutoRunGameCheckBox()
            self.auto_execute_delay_label = BaseLabel(
                "Delay:",
                label_content_align=("left", "middle"),
                label_width="auto"
            )
            self.auto_execute_delay_spin_box = SpinBox(iter_val=list(generate_spinbox_numbers()), init_val=get_auto_run_game_delay())
            self.staging_label = BaseLabel(
                "Testing Branch:",
                label_content_align=("left", "middle"),
                label_width="auto"
            )
            self.staging_checkbox = StagingCheckBox()
            yield self.staging_label
            yield self.staging_checkbox
            yield self.auto_execute_label
            yield self.auto_execute_checkbox
            yield self.auto_execute_delay_label
            yield self.auto_execute_delay_spin_box

    def on_mount(self):
        self.auto_execute_delay_spin_box.styles.width = "1fr"
        self.auto_execute_checkbox.styles.width = 'auto'
        self.auto_execute_checkbox.styles.content_align = ("center", "middle")
        self.staging_checkbox.styles.width = 'auto'
        global delay_spinbox
        delay_spinbox = self.auto_execute_delay_spin_box
