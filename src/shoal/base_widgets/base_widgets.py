from textual.containers import Horizontal
from textual.widgets import Button, Label


class BaseButton(Button):
    def __init__(
        self,
        button_text: str = "default_text",
        button_width: str = "auto",
        button_margin: int = 0,
        button_min_width: int = 1,
        button_min_height: int = 1,
        button_border: str = "none",
        button_padding: int = 0,
    ):
        super().__init__()
        self.label = button_text
        self.button_width = button_width
        self.button_margin = button_margin
        self.button_min_width = button_min_width
        self.button_min_height = button_min_height
        self.button_border = button_border
        self.button_padding = button_padding

    def on_mount(self):
        self.styles.width = self.button_width
        self.styles.margin = self.button_margin
        self.styles.min_width = self.button_min_width
        self.styles.border = self.button_border
        self.styles.padding = self.button_padding
        self.styles.min_height = self.button_min_height
        self.styles.border = ("solid", "grey")


class BaseLabel(Label):
    def __init__(
        self,
        label_text: str = "default label text",
        label_border: list = ("solid", "grey"),
        label_padding: tuple = (0, 0, 0, 0),
        label_margin: tuple = (0, 0, 0, 0),
        label_height: any = "auto",
        label_min_height: any = 1,
        label_max_height: any = "100%",
        label_width: any = "auto",
        label_min_width: any = 1,
        label_max_width: any = "100%",
        label_content_align: list = ("center", "middle"),
    ):
        super().__init__(label_text)
        self.label_border = label_border
        self.label_padding = label_padding
        self.label_margin = label_margin
        self.label_height = label_height
        self.label_min_height = label_min_height
        self.label_max_height = label_max_height
        self.label_width = label_width
        self.label_min_width = label_min_width
        self.label_max_width = label_max_width
        self.label_content_align = label_content_align

    def on_mount(self):
        self.styles.border = self.label_border
        self.styles.padding = self.label_padding
        self.styles.margin = self.label_margin
        self.styles.height = self.label_height
        self.styles.min_height = self.label_min_height
        self.styles.max_height = self.label_max_height
        self.styles.width = self.label_width
        self.styles.min_width = self.label_min_width
        self.styles.max_width = self.label_max_width
        self.styles.content_align = self.label_content_align


class BaseHorizontalBox(Horizontal):
    def __init__(
        self,
        content_align: list = ("center", "middle"),
        padding: list = (1, 0, 0, 0),
        margin: list = (0, 0, 0, 0),
        border: tuple = ("none", "black"),
        height: str = "auto",
        width: str = "100%",
        max_width: str = '100%'
    ):
        super().__init__()
        self.content_align = content_align
        self.padding = padding
        self.margin = margin
        self.border = border
        self.height = height
        self.width = width
        self.max_width = max_width

    def on_mount(self):
        self.styles.content_align = self.content_align
        self.styles.padding = self.padding
        self.styles.margin = self.margin
        self.styles.border = self.border
        self.styles.height = self.height
        self.styles.width = self.width
        self.styles.max_width = self.max_width
