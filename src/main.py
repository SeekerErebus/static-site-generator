import os, helpers
from copy_static import copy_static
from process_markdown import build_site


def main():
    try:
        public_dir = helpers.get_relative_path('public')
        content_dir = helpers.get_relative_path('content')
        template = helpers.ROOT_DIR / 'template.html'

        helpers.remove_directory(public_dir)
        copy_static()
        build_site(content_dir, template, public_dir)

    except Exception as e:
        print(f'Something went wrong, error: {e}')
    

if __name__ == "__main__":
    main()