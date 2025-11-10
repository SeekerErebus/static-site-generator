import os, helpers
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
    
def generate_page(from_path: Path, template_path: Path, dest_path: Path):
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
    final_html = template.replace('{{ Title }}', title).replace('{{ Content }}', html)
    helpers.file_write(dest_path, final_html)

    