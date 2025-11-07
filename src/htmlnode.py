from __future__ import annotations


class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.__dict__ == other.__dict__
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ''
        result_string = f''
        for key in self.props:
            result_string += f' {key}="{self.props[key]}"'
        return result_string

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict | None = None):
        super().__init__(tag=tag, value=value, props=props)
    def to_html(self):
        if self.value is None:
            raise ValueError("Value is required")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict | None = None):
        super().__init__(tag=tag, children=children, props=props)
    def __eq__(self, other: object) -> bool:
        return super().__eq__(other)
    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required")
        if self.children is None:
            raise ValueError("No children")
        output_string = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            output_string += child.to_html()
        output_string += f'</{self.tag}>'
        return output_string