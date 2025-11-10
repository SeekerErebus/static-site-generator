import os, helpers
from copy_static import copy_static
from process_markdown import generate_page


def main():
    try:
        public_dir = helpers.get_relative_path('public')
        content_dir = helpers.get_relative_path('content')
        c_index = content_dir / 'index.md'
        p_index = public_dir / 'index.html'
        template = helpers.ROOT_DIR / 'template.html'

        helpers.remove_directory(public_dir)
        copy_static()
        generate_page(c_index, template, p_index)

    except Exception as e:
        print(f'Something went wrong, error: {e}')
    

if __name__ == "__main__":
    main()