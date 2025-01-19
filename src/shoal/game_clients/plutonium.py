import os

from shoal.settings import get_use_staging


def get_plutonium_appdata_dir() -> str:
    if get_use_staging():
        pluto_appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium-staging')
    else:
        pluto_appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Plutonium')
    return pluto_appdata_path


def get_plutonium_bootstrapper() -> str:
    return os.path.normpath(f'{get_plutonium_appdata_dir()}/bin/plutonium-bootstrapper-win32.exe')


def get_plutonium_modern_warfare_iii_config_path_suffix() -> str:
    return 'storage/iw5/players/config_mp.cfg'


def get_plutonium_modern_warfare_iii_config_path() -> str:
    return os.path.normpath(f'{get_plutonium_appdata_dir()}/{get_plutonium_modern_warfare_iii_config_path_suffix()}')


def get_plutonium_forums_link() -> str:
    return 'https://forum.plutonium.pw/'


def get_plutonium_docs_link() -> str:
    return 'https://plutonium.pw/docs/'


def get_plutonium_github_link() -> str:
    return 'https://github.com/plutoniummod'
