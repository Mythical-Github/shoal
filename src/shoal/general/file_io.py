import os
import ctypes
import zipfile
from urllib.request import urlretrieve


def get_all_lines_in_config(config_path: str) -> list[str]:
    with open(config_path, encoding='utf-8') as file:
        return file.readlines()


def set_all_lines_in_config(config_path: str, lines: list[str]):
    with open(config_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def add_line_to_config(config_path: str, line: str):
    if not does_config_have_line(config_path, line):
        with open(config_path, 'a', encoding='utf-8') as file:
            file.write(line + '\n')


def remove_line_from_config(config_path: str, line: str):
    lines = get_all_lines_in_config(config_path)
    with open(config_path, 'w', encoding='utf-8') as file:
        file.writelines(l for l in lines if l.rstrip('\n') != line)


def does_config_have_line(config_path: str, line: str) -> bool:
    return line + '\n' in get_all_lines_in_config(config_path)


def remove_lines_from_config_that_start_with_substring(config_path: str, substring: str):
    new_lines = []
    for line in get_all_lines_in_config(config_path):
        if not line.startswith(substring):
            new_lines.append(line)
    set_all_lines_in_config(config_path, new_lines)


def remove_lines_from_config_that_end_with_substring(config_path: str, substring: str):
    new_lines = []
    for line in get_all_lines_in_config(config_path):
        if not line.endswith(substring):
            new_lines.append(line)
    set_all_lines_in_config(config_path, new_lines)


def remove_lines_from_config_that_contain_substring(config_path: str, substring: str):
    new_lines = []
    for line in get_all_lines_in_config(config_path):
        if not line in (substring):
            new_lines.append(line)
    set_all_lines_in_config(config_path, new_lines)


def download_file(url: str, destination: str):
    try:
        print(f"Downloading from {url} to {destination}...")
        urlretrieve(url, destination)
        print("Download completed.")
    except Exception as e:
        print(f"Failed to download file: {e}")
        raise


def get_all_drive_letter_paths() -> list[str]:
    drive_letters = []
    for drive in range(0, 26):
        drive_letter = f"{chr(drive + ord('A'))}:\\"
        if os.path.exists(drive_letter):
            drive_letters.append(drive_letter)
    return drive_letters


def get_drive_name(drive_letter: str) -> str:
    # below is ai genned, but tested on windows
    """
    Returns the volume label of the specified drive letter using ctypes.
    
    Args:
        drive_letter (str): The drive letter (e.g., 'C:', 'D:')
    
    Returns:
        str: The volume label of the drive or 'No Name' if not found.
    """
    if not drive_letter.endswith(":"):
        drive_letter += ":"
    drive_letter += "\\"

    # Create a buffer for the volume name
    volume_name_buffer = ctypes.create_unicode_buffer(261)  # Max path length

    # Call the Windows API function
    result = ctypes.windll.kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(drive_letter),  # Drive path
        volume_name_buffer,             # Buffer to store volume name
        ctypes.sizeof(volume_name_buffer),  # Size of the buffer
        None,                           # Serial number (unused)
        None,                           # Max component length (unused)
        None,                           # File system flags (unused)
        None,                           # File system name buffer (unused)
        0                               # File system name buffer size (unused)
    )

    # Check if the function succeeded
    if result:
        return volume_name_buffer.value or "No Name"
    else:
        return "Unknown"


def unzip_file(zip_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
