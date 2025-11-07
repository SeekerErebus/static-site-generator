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
    def __repr__(self) -> str:
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props=\'{self.props_to_html()}\')'
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ''
        result_string = f''
        for k,v in self.props:
            result_string += f' {k}={v}'
        return result_string