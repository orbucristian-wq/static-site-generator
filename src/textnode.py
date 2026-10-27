from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (self.text, self.text_type, self.url) == (other.text, other.text_type, other.url)

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'


def text_node_to_html_node(text_node):
    tags = {TextType.TEXT: None, TextType.BOLD: 'b', TextType.ITALIC: 'i', TextType.CODE: 'code'}
    if text_node.text_type in tags:
        return LeafNode(tags[text_node.text_type], text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
    raise ValueError(f'Unsupported text type: {text_node.text_type}')
