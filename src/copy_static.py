import os
import shutil
import helpers


def copy_static():
    static_dir = helpers.get_relative_path('static')
    public_dir = helpers.get_relative_path('public')

    if not static_dir.exists():
        raise FileNotFoundError("There is no static directory.")
    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)