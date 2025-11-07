from __future__ import annotations
from typing import Callable
from blocks_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
from htmlnode import LeafNode, ParentNode


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    full_node = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                t1 = block.replace('\n', ' ')
                t2 = text_to_leaves(t1)
                html = ParentNode('p', t2) # pyright: ignore[reportArgumentType]
            case BlockType.HEADING:
                level = len(block) - len(block.lstrip('#'))
                t1 = block.lstrip('#')
                t2 = t1.lstrip()
                t3 = text_to_leaves(t2)
                html = ParentNode(f'h{level}', t3) # pyright: ignore[reportArgumentType]
            case BlockType.CODE:
                t1 = block.lstrip('```').rstrip('```')
                t2 = t1.lstrip('\n').rstrip('\n')
                code_block = TextNode(t2, TextType.CODE)
                t3 = text_node_to_html_node(code_block)
                html = ParentNode('pre', [t3]) # pyright: ignore[reportArgumentType]
            case BlockType.QUOTE:
                t1 = _start_strip(block, lambda i: '> ')
                t2 = text_to_leaves(t1)
                html = ParentNode('blockquote', t2) # pyright: ignore[reportArgumentType]
            case BlockType.UNORDERED_LIST:
                t1 = _start_strip(block, lambda i: '- ')
                lines = t1.splitlines()
                processed_list = []
                for line in lines:
                    leaves = text_to_leaves(line)
                    processed_list.append(ParentNode('li', leaves)) # pyright: ignore[reportArgumentType]
                html = ParentNode('ul', processed_list)
            case BlockType.ORDERED_LIST:
                t1 = _start_strip(block, lambda i: f'{i + 1}. ')
                lines = t1.splitlines()
                processed_list = []
                for line in lines:
                    leaves = text_to_leaves(line)
                    processed_list.append(ParentNode('li', leaves)) # pyright: ignore[reportArgumentType]
                html = ParentNode('ol', processed_list)
            case _:
                raise Exception("Somehow the function that always returns a usable blocktype didn't return a useable one.")
        full_node.append(html)
    return ParentNode('div', full_node)

def text_to_leaves(block: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(block)
    leaf_nodes = list(map(text_node_to_html_node, text_nodes))
    return leaf_nodes

def _start_strip(block: str, substr_gen: Callable) -> str:
    # for Fixed substr: substr_gen = lambda i: substr
    # for ordered list: substr_gen = lambda i: f'{i+1}. '
    lines = block.splitlines(keepends=True)
    adjusted = [line.lstrip(substr_gen(i)) for i, line in enumerate(lines)]
    return ''.join(adjusted)