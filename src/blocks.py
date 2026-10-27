from enum import Enum
import re
from htmlnode import ParentNode, LeafNode
from inline import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split('\n\n') if block.strip()]


def block_to_block_type(block):
    lines = block.split('\n')
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f'{i}. ') for i, line in enumerate(lines, 1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        kind = block_to_block_type(block)
        lines = block.split('\n')
        if kind == BlockType.CODE:
            node = ParentNode('pre', [LeafNode('code', block[4:-3])])
        elif kind == BlockType.HEADING:
            hashes, text = block.split(' ', 1)
            node = ParentNode(f'h{len(hashes)}', text_to_children(text))
        elif kind == BlockType.QUOTE:
            text = ' '.join(line[1:].strip() for line in lines)
            node = ParentNode('blockquote', text_to_children(text))
        elif kind in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
            items = [line[2:] if kind == BlockType.UNORDERED_LIST else line.split('. ', 1)[1] for line in lines]
            node = ParentNode('ul' if kind == BlockType.UNORDERED_LIST else 'ol',
                              [ParentNode('li', text_to_children(item)) for item in items])
        else:
            node = ParentNode('p', text_to_children(' '.join(lines)))
        children.append(node)
    return ParentNode('div', children)
