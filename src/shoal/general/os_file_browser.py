import os
import subprocess

from shoal.logger import print_to_log_window


def open_directory_in_file_browser(directory_path: str):
    if os.path.isdir(directory_path):
        program = "explorer"
        subprocess.run(
            [program, directory_path],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
        print_to_log_window(f'Opening the following directory in the file browser: "{directory_path}"')
    else:
        print_to_log_window(f'The specified path is not a directory: "{directory_path}"')
