import os
import shutil
import helpers


def copy_static():
    root_dir, static_dir, public_dir = helpers.get_os_directories()

    if not os.path.exists(static_dir):
        raise FileNotFoundError("There is no static directory.")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir, exist_ok=True)
    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)