from textual import work
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Vertical
from textual.widgets import Header, Static, Label, ProgressBar


class TaskText(Static):
    def __init__(
        self
    ):
        super().__init__()

    def compose(self) -> ComposeResult:
        self.task_text = Label('Default Text')
        yield self.task_text

    def on_mount(self):
        self.styles.align = ('center', 'middle')
        self.styles.content_align = ('center', 'middle')
        self.styles.text_align = ('center')


class SetupScreenProgressBar(Static):    
    def __init__(
        self,
        step_text_to_step_functions,
        finished_all_steps_function,
        widgets_to_refresh_on_screen_pop
    ):
        super().__init__()
        self.step_text_to_step_functions = step_text_to_step_functions
        self.finished_all_steps_function = finished_all_steps_function
        self.widgets_to_refresh_on_screen_pop = widgets_to_refresh_on_screen_pop

    def compose(self) -> ComposeResult:
        self.progress_bar = ProgressBar(len(self.step_text_to_step_functions), show_eta=False)
        yield self.progress_bar

    def on_mount(self):
        self.progress_bar.styles.align = ('center', 'middle')
        self.progress_bar.styles.content_align = ('center', 'middle')
        self.styles.width = '100%'
        self.progress_bar.styles.width = '100%'
    

    def update_label(self, new_text: str):
        self.parent.parent.task_text.task_text.update(content=new_text)


    def update_progress_bar(self):
        self.progress_bar.advance(1)


    @work(thread=True)
    def run_steps(self):
        for step_text, step_function in self.step_text_to_step_functions.items():
            self.update_label(step_text)
            step_function()
            self.update_progress_bar()

        for widget in self.widgets_to_refresh_on_screen_pop:
            widget.refresh(recompose=True)
        
        from shoal.main_app import app
        app.call_from_thread(app.pop_screen)

        self.finished_all_steps_function()


class SetupScreenMainLayout(Static):
    def __init__(
        self,
        step_text_to_step_functions,
        finished_all_steps_function,
        widgets_to_refresh_on_screen_pop,
        screen_label_text
    ):
        super().__init__()
        self.step_text_to_step_functions = step_text_to_step_functions
        self.finished_all_steps_function = finished_all_steps_function
        self.widgets_to_refresh_on_screen_pop = widgets_to_refresh_on_screen_pop
        self.screen_label_text = screen_label_text

    def compose(self) -> ComposeResult:
        self.vertical = Vertical()
        self.screen_label = Label(self.screen_label_text)
        self.task_text = TaskText()
        self.progress_bar = SetupScreenProgressBar(
            self.step_text_to_step_functions,
            self.finished_all_steps_function,
            self.widgets_to_refresh_on_screen_pop
        )
        with self.vertical:
            yield self.screen_label
            yield self.task_text
            yield self.progress_bar

    def on_mount(self):
        self.screen_label.styles.text_style = "bold"
        self.screen_label.styles.width = '100%'
        self.screen_label.styles.align = ('center', 'middle')
        self.screen_label.styles.content_align = ('center', 'middle')
        self.screen_label.styles.padding = 1
        self.vertical.styles.border = ("solid", "grey")
        self.vertical.styles.height = 'auto'
        self.styles.width = '100%'
        self.task_text.styles.width = '100%'
        self.task_text.styles.padding = 1
        self.progress_bar.styles.width = '100%'
        self.progress_bar.styles.padding = (0, 0, 1, 0)
        self.progress_bar.styles.align = ('center', 'middle')
        self.progress_bar.styles.content_align = ('center', 'middle')
        self.vertical.styles.width = '100%'
        self.vertical.styles.align = ('center', 'middle')
        self.vertical.styles.content_align = ('center', 'middle')


class SetupScreen(Screen):
    def __init__(
        self,
        step_text_to_step_functions,
        finished_all_steps_function,
        widgets_to_refresh_on_screen_pop,
        screen_label_text
    ):
        super().__init__()
        self.step_text_to_step_functions = step_text_to_step_functions
        self.finished_all_steps_function = finished_all_steps_function
        self.widgets_to_refresh_on_screen_pop = widgets_to_refresh_on_screen_pop
        self.screen_label_text = screen_label_text

    def compose(self) -> ComposeResult:
        self.header = Header()
        self.text_input_main_layout = SetupScreenMainLayout(
            self.step_text_to_step_functions,
            self.finished_all_steps_function,
            self.widgets_to_refresh_on_screen_pop,
            self.screen_label_text
        )
        self.vertical_scroll = VerticalScroll()
        with self.vertical_scroll:
            yield self.header
            yield self.text_input_main_layout
        yield self.vertical_scroll

    def on_mount(self):
        self.vertical_scroll.styles.margin = 0
        self.vertical_scroll.styles.padding = 0
        self.vertical_scroll.styles.border = ("solid", "grey")
        self.vertical_scroll.styles.align = ('center', 'middle')
        self.text_input_main_layout.progress_bar.run_steps()
