import re
from textnode import TextNode, TextType

IMAGE_PATTERN = r'!\[([^\[\]]*)\]\(([^()]*)\)'
LINK_PATTERN = r'(?<!!)\[([^\[\]]*)\]\(([^()]*)\)'


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f'Unclosed Markdown delimiter: {delimiter}')
        for i, part in enumerate(parts):
            if part:
                result.append(TextNode(part, text_type if i % 2 else TextType.TEXT))
    return result


def extract_markdown_images(text):
    return re.findall(IMAGE_PATTERN, text)


def extract_markdown_links(text):
    return re.findall(LINK_PATTERN, text)


def _split_nodes_reference(old_nodes, pattern, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        position = 0
        for match in re.finditer(pattern, node.text):
            if match.start() > position:
                result.append(TextNode(node.text[position:match.start()], TextType.TEXT))
            result.append(TextNode(match.group(1), text_type, match.group(2)))
            position = match.end()
        if position < len(node.text):
            result.append(TextNode(node.text[position:], TextType.TEXT))
    return result


def split_nodes_image(old_nodes):
    return _split_nodes_reference(old_nodes, IMAGE_PATTERN, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return _split_nodes_reference(old_nodes, LINK_PATTERN, TextType.LINK)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    # Protect code and reference URLs before parsing formatting delimiters.
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    return split_nodes_delimiter(nodes, '_', TextType.ITALIC)
