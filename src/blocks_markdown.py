from __future__ import annotations
import re
from enum import Enum


def markdown_to_blocks(markdown: str) -> list[str]:
    if not markdown:
        return []
    
    lines = markdown.splitlines()
    blocks = []
    current_block = []
    
    for line in lines:
        if line.strip() == '':
            if current_block:
                block = '\n'.join(current_block).strip()
                if block:
                    blocks.append(block)
                current_block = []
        else:
            current_block.append(line)
    
    if current_block:
        block = '\n'.join(current_block).strip()
        if block:
            blocks.append(block)
    
    return blocks

def block_to_block_type(markdown_block: str) -> BlockType:
    if not markdown_block:
        return BlockType.PARAGRAPH
    lines = markdown_block.splitlines()
    if len(lines) == 1 and re.match(r'^#{1,6}\s', lines[0]):
        return BlockType.HEADING
    if len(lines) > 0 and lines[0].startswith('```') and lines[-1].endswith('```'):
        return BlockType.CODE
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    if all(re.match(rf'^{i+1}\.\ ', lines[i]) for i in range(len(lines))):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'