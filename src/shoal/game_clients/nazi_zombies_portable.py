import os
import platform

from shoal.settings import get_game_directory


def get_nazi_zombie_portable_docs():
    return 'https://docs.nzp.gay/landing/#nazi-zombies-portable-documentation'


def get_nazi_zombie_portable_download_link():
    if platform.system() == "Windows":
        return get_nazi_zombie_portable_windows_download_link()
    else:
        return get_nazi_zombie_portable_linux_download_link()


def get_nazi_zombie_portable_linux_download_link():
    return 'https://github.com/nzp-team/nzportable/releases/download/nightly/nzportable-linux64.zip'


def get_nazi_zombie_portable_windows_download_link():
    return 'https://github.com/nzp-team/nzportable/releases/download/nightly/nzportable-win64.zip'


def get_nazi_zombie_portable_forums_link():
    # the below is technically their discord link
    return 'https://discord.com/invite/Avt2VS5kQM'


def get_nazi_zombie_portable_github_link():
    return 'https://github.com/nzp-team/nzportable'


def download_nazi_zombie_portable():
    from shoal.general.file_io import download_file, unzip_file
    output_dir = os.path.normpath(os.path.dirname(get_nazi_zombie_portable_executable_path()))
    output_zip = os.path.normpath(os.path.join(output_dir, 'nazi_zombies_portable.zip'))
    os.makedirs(output_dir, exist_ok=True)
    download_file(get_nazi_zombie_portable_download_link(), output_zip)
    unzip_file(output_zip, os.path.dirname(output_zip))
    os.remove(output_zip)


def ensure_nazi_zombie_portable_is_installed():
    exec_path = get_nazi_zombie_portable_executable_path()
    if not os.path.isfile(exec_path):
        download_nazi_zombie_portable()
        from shoal.settings import set_game_directory
        set_game_directory(os.path.dirname(get_nazi_zombie_portable_executable_path()))
    return exec_path


def get_nazi_zombie_portable_executable_path():
    from shoal.settings import SCRIPT_DIR
    base_path = f'{SCRIPT_DIR}/assets/nazi_zombies_portable'
    if platform.system() == "Windows":
        return os.path.normpath(os.path.join(base_path, 'nzportable-sdl64.exe'))
    else:
        return os.path.normpath(os.path.join(base_path, 'nzportable64-sdl'))


def get_user_config_path() -> str:
    return os.path.normpath(os.path.join(get_game_directory(), 'nzp', 'user_settings.cfg'))
