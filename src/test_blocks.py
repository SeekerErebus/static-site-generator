import unittest
from blocks_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_blocktype_header(self):
        md = '### Header 3'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)
    def test_blocktype_ordered_list(self):
        md = """1. The first thing
2. The second thing
3. The third thing"""
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ORDERED_LIST)
