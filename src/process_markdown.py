import os, shutil, helpers
from pathlib import Path
from markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    """
    Extracts the title from markdown that starts with an H1 header.
    
    Raises ValueError if the markdown does not start with '# '.
    
    Args:
        markdown (str): The markdown string.
    
    Returns:
        str: The title text.
    """
    if not markdown.startswith('# '):
        raise ValueError("Markdown does not start with an H1 header")
    
    # Find the position of the first newline after the header
    newline_pos = markdown.find('\n', 2)
    if newline_pos == -1:
        # No newline, entire rest is title
        title = markdown[2:].strip()
    else:
        # Title ends at newline
        title = markdown[2:newline_pos].strip()
    
    return title
    
def generate_page(from_path: Path, template_path: Path, dest_path: Path, baseline: str) -> None:
    """
    Converts a markdown file into the content of an html file and writes it to disk.

    Args:
    from_path (Path): The markdown file source.
    template_path (Path): The html file that serves as the template.
    dest_path (Path): The target destination file.
    baseline (str): The reference root for page links.
    """
    detail_message = f"Generating page from {str(from_path)} to {str(dest_path)} using {str(template_path)}"
    print(detail_message)

    if not from_path.exists():
        raise FileNotFoundError(f"source {from_path} doesn't exist")
    if not template_path.exists():
        raise FileNotFoundError(f"template {template_path} doesn't exist")
    markdown = helpers.file_read(from_path)
    template = helpers.file_read(template_path)
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    t1 = template.replace('{{ Title }}', title).replace('{{ Content }}', html)
    final_html = t1.replace('href="/', f'href="{baseline}').replace('src="/', f'src="{baseline}')
    helpers.file_write(dest_path, final_html)

def build_site(content_dir: Path, template_path: Path, public_dir: Path, baseline: str) -> None:
    """
    Recursively builds the static site by mirroring the structure of content_dir into public_dir.
    Non-Markdown files are copied directly, while Markdown files (.md) are converted to HTML
    using the provided template and the generate_page function.

    Args:
        content_dir (Path): The source directory containing Markdown and other files.
        template_path (Path): The HTML template path used for Markdown conversion.
        public_dir (Path): The destination directory for the generated site.
        baseline (str): The reference root, passthrough.
    """
    for root, dirs, files in os.walk(content_dir):
        # Compute relative path and create corresponding directory in public_dir
        rel_root = Path(root).relative_to(content_dir)
        out_root = public_dir / rel_root
        out_root.mkdir(parents=True, exist_ok=True)

        # Process each file
        for file in files:
            from_path = Path(root) / file
            rel_file = rel_root / file
            dest_file = public_dir / rel_file

            if file.endswith('.md'):
                # Convert Markdown to HTML
                dest_path = dest_file.with_suffix('.html')
                generate_page(from_path, template_path, dest_path, baseline)
#            else:
#                # Copy non-Markdown files
#                shutil.copy2(from_path, dest_file)