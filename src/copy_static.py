import os
import shutil
import helpers
from pathlib import Path


def copy_static(static_dir: Path, public_dir: Path):
    if not static_dir.exists():
        raise FileNotFoundError("There is no static directory.")
    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)