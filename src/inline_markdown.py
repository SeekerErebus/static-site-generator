from __future__ import annotations
import re
from typing import Callable
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        mark_count = node.text.count(delimiter)
        if mark_count % 2 != 0:
            raise ValueError("Unbalanced delimiter in markdown.")
        parts = node.text.split(delimiter)
        prepped_nodes = []
        for i in range(len(parts)):
            part = parts[i]
            if part == '':
                continue
            if i % 2 == 0:
                new_text_node = TextNode(part, TextType.TEXT)
            else:
                new_text_node = TextNode(text=part, text_type=text_type)
            prepped_nodes.append(new_text_node)
        new_nodes.extend(prepped_nodes)
    
    return new_nodes

def _split_nodes_helper(
    old_nodes: list[TextNode],
    pattern: str,
    node_factory: Callable[[re.Match], TextNode]
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = list(re.finditer(pattern, node.text))
        if not matches:
            new_nodes.append(node)
            continue
        pos = 0
        for match in matches:
            start, end = match.start(), match.end()
            if start > pos:
                text_before = node.text[pos:start]
                new_nodes.append(TextNode(text=text_before, text_type=TextType.TEXT))
            special_node = node_factory(match)
            new_nodes.append(special_node)
            pos = end
        if pos < len(node.text):
            text_after = node.text[pos:]
            new_nodes.append(TextNode(text_after, text_type=TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    def image_factory(match: re.Match) -> TextNode:
        alt = match.group(1).strip()
        url = match.group(2).strip()
        return TextNode(alt, TextType.IMAGE, url)
    return _split_nodes_helper(old_nodes, pattern, image_factory)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    def link_factory(match: re.Match) -> TextNode:
        label = match.group(1).strip()
        url = match.group(2).strip()
        return TextNode(label, TextType.LINK, url)
    return _split_nodes_helper(old_nodes, pattern, link_factory)

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_image([node])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)