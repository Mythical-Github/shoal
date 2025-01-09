from textual.widgets import RichLog, Static


class LauncherLog(Static):
    def compose(self):
        self.rich_log = RichLog(wrap=True)
        yield self.rich_log

    def on_mount(self):
        self.rich_log.styles.margin = (1, 0, 0, 0)
        self.rich_log.styles.border = ("solid", "grey")
        self.rich_log.border_title = "Logging"
        self.rich_log.styles.width = "100%"
        self.rich_log.styles.scrollbar_size_horizontal = 0
        self.styles.height = "1fr"
        self.styles.min_height = 6
        self.styles.width = '100%'


logger = LauncherLog()


def print_to_log_window(message: str):
    logger.rich_log.write(message)
