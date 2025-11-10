import shutil
from pathlib import Path

def find_project_root(marker: str = ".git") -> Path:
    """Climb until we find a root marker. Fast (>0.1 ms) and never breaks on refactors."""
    path = Path(__file__).resolve()
    for parent in [path, *path.parents]:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"Project root not found – no {marker!r} in any parent")

ROOT_DIR = find_project_root()

def get_relative_path(rel_path: str | Path) -> Path:
    return ROOT_DIR / rel_path

def remove_directory(file_path: Path) -> bool:
    if file_path.exists():
        shutil.rmtree(file_path)
        return True
    return False

def file_read(file_path: str | Path) -> str:
    """
    Reads the content from a file with the specified file_path.
    
    Args:
    file_path (str or Path): The path of the file to read from.
    
    Returns:
    str: The content of the file, or empty string if unsuccessful.
    """
    path = Path(file_path)
    try:
        with path.open('r') as file:
            content = file.read()
        return content
    except IOError as e:
        print(f"Error reading file: {e}")
        return ""

from pathlib import Path

def file_write(filename: str | Path, content):
    """
    Writes the given content to a file with the specified filename.
    
    Args:
    filename (str or Path): The path of the file to write to.
    content (str): The content to write to the file.
    
    Returns:
    bool: True if successful, False otherwise.
    """
    path = Path(filename) if isinstance(filename, str) else filename
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as file:
            file.write(content)
        return True
    except IOError as e:
        print(f"Error writing to file: {e}")
        return False