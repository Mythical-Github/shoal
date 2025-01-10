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


def download_file(url: str, destination: str):
    try:
        print(f"Downloading from {url} to {destination}...")
        urlretrieve(url, destination)
        print("Download completed.")
    except Exception as e:
        print(f"Failed to download file: {e}")
        raise
