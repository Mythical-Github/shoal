import webbrowser

from shoal.logger import print_to_log_window


def open_website(url: str):
    print_to_log_window(f"Opening website url: {url}")
    try:
        webbrowser.open(url, new=2)
    except RuntimeError as error_message:
        print_to_log_window(f"An error occurred: {error_message!s}")
