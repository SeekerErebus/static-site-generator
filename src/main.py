import sys, argparse, helpers
from copy_static import copy_static
from process_markdown import build_site


def main():
    if len(sys.argv) >= 2:
        baseline = sys.argv[1]
    else:
        baseline = '/'
    try:
        public_dir = helpers.get_relative_path('docs')
        content_dir = helpers.get_relative_path('content')
        static_dir = helpers.get_relative_path('static')
        template = helpers.ROOT_DIR / 'template.html'

        helpers.remove_directory(public_dir)
        copy_static(static_dir, public_dir)
        build_site(content_dir, template, public_dir, baseline)

    except Exception as e:
        print(f'Something went wrong, error: {e}')
    

if __name__ == "__main__":
    main()