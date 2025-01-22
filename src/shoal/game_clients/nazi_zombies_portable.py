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


def installing_nzp_step_one():
    from shoal.general.file_io import download_file
    output_dir = os.path.normpath(os.path.dirname(get_nazi_zombie_portable_executable_path()))
    output_zip = os.path.normpath(os.path.join(output_dir, 'nazi_zombies_portable.zip'))
    os.makedirs(output_dir, exist_ok=True)
    download_file(get_nazi_zombie_portable_download_link(), output_zip)


def installing_nzp_step_two():
    from shoal.general.file_io import unzip_file
    output_dir = os.path.normpath(os.path.dirname(get_nazi_zombie_portable_executable_path()))
    output_zip = os.path.normpath(os.path.join(output_dir, 'nazi_zombies_portable.zip'))
    unzip_file(output_zip, os.path.dirname(output_zip))


def installing_nzp_step_three():
    from shoal.settings import set_game_directory
    output_dir = os.path.normpath(os.path.dirname(get_nazi_zombie_portable_executable_path()))
    output_zip = os.path.normpath(os.path.join(output_dir, 'nazi_zombies_portable.zip'))
    set_game_directory(os.path.dirname(get_nazi_zombie_portable_executable_path()))
    os.remove(output_zip)


def download_nazi_zombie_portable():
    installing_nzp_step_one()
    installing_nzp_step_two()
    installing_nzp_step_three()


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


def get_nzp_user_config_path() -> str:
    return os.path.normpath(os.path.join(get_game_directory(), 'nzp', 'user_settings.cfg'))


def push_install_nazi_zombies_portable_screen() -> str:
    from shoal.base_widgets import setup_screen
    from shoal.main_app import app
    from shoal import game_runner
    if not os.path.isfile(get_nazi_zombie_portable_executable_path()):
        steps = {
                    "Downloading Nazi Zombies: Portable...": installing_nzp_step_one,
                    "Unzipping Nazi Zombies: Portable...": installing_nzp_step_two,
                    "Cleaning up Nazi Zombies: Portable Installation...": installing_nzp_step_three,
                }
        download_nzp_screen = setup_screen.SetupScreen(
                step_text_to_step_functions=steps,
                finished_all_steps_function=game_runner.run_game,
                widgets_to_refresh_on_screen_pop=[],
                screen_label_text="Nazi Zombies: Portable Setup:"
            )
        app.push_screen(download_nzp_screen)
    else:
        game_runner.run_game()
