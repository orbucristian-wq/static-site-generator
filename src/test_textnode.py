import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_equal_defaults(self):
        self.assertEqual(TextNode('hello', TextType.TEXT), TextNode('hello', TextType.TEXT))

    def test_different_properties(self):
        original = TextNode('hello', TextType.LINK, '/a')
        for node in [TextNode('bye', TextType.LINK, '/a'), TextNode('hello', TextType.TEXT, '/a'), TextNode('hello', TextType.LINK, '/b'), TextNode('hello', TextType.LINK)]:
            with self.subTest(node=node):
                self.assertNotEqual(original, node)

    def test_repr(self):
        self.assertEqual(repr(TextNode('x', TextType.BOLD)), 'TextNode(x, bold, None)')

    def test_conversions(self):
        for kind, tag in [(TextType.TEXT, None), (TextType.BOLD, 'b'), (TextType.ITALIC, 'i'), (TextType.CODE, 'code')]:
            node = text_node_to_html_node(TextNode('hi', kind))
            self.assertEqual((node.tag, node.value), (tag, 'hi'))
        self.assertEqual(text_node_to_html_node(TextNode('go', TextType.LINK, '/')).to_html(), '<a href="/">go</a>')
        image = text_node_to_html_node(TextNode('alt', TextType.IMAGE, '/a.png'))
        self.assertEqual(image.props, {'src': '/a.png', 'alt': 'alt'})
        self.assertEqual(image.value, '')

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode('x', 'invalid'))
