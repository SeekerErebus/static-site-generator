import re
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, HTMLNode


def main():
    txtnode = TextNode('this is some bold text', TextType.BOLD)
    print(txtnode)
    

if __name__ == "__main__":
    main()