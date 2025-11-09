import os
import shutil


def copy_static():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(root_dir, 'static')
    public_dir = os.path.join(root_dir, 'public')

    if not os.path.exists(static_dir):
        raise FileNotFoundError("There is no static directory.")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir, exist_ok=True)
    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)