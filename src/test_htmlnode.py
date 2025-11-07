import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag='p', value='I Love My Life')
        node2 = HTMLNode(tag='p', value='I Love My Life')
        self.assertEqual(node, node2)
    def test_ne(self):
        node = HTMLNode(tag='h1',value='I Love My Life')
        node2 = HTMLNode(tag='p', value='I Love My Life')
        self.assertNotEqual(node, node2)
    def test_repl(self):
        node = HTMLNode(tag='h1',value='I Love My Life')
        test_string = "HTMLNode(tag=h1, value=I Love My Life, children=None, props='')"
        self.assertEqual(f'{node}', test_string)