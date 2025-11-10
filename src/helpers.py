import os

def get_os_directories() -> tuple[str, str, str]:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(root_dir, 'static')
    public_dir = os.path.join(root_dir, 'public')
    return (root_dir, static_dir, public_dir)