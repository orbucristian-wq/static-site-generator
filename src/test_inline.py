import unittest
from inline import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
                    split_nodes_image, split_nodes_link, text_to_textnodes)
from textnode import TextNode, TextType


class TestInline(unittest.TestCase):
    def test_delimiters(self):
        for delimiter, kind in [('**', TextType.BOLD), ('_', TextType.ITALIC), ('`', TextType.CODE)]:
            with self.subTest(delimiter=delimiter):
                self.assertEqual(split_nodes_delimiter([TextNode(f'a {delimiter}b{delimiter} c', TextType.TEXT)], delimiter, kind),
                                 [TextNode('a ', TextType.TEXT), TextNode('b', kind), TextNode(' c', TextType.TEXT)])

    def test_unclosed(self):
        with self.assertRaisesRegex(ValueError, 'Unclosed'):
            split_nodes_delimiter([TextNode('a **b', TextType.TEXT)], '**', TextType.BOLD)

    def test_preserve_nontext(self):
        node = TextNode('**literal**', TextType.CODE)
        self.assertEqual(split_nodes_delimiter([node], '**', TextType.BOLD), [node])
        self.assertEqual(split_nodes_image([node]), [node])
        self.assertEqual(split_nodes_link([node]), [node])

    def test_extract(self):
        text = '![first](/one.png) [site](https://a.test) ![second](/two.png)'
        self.assertEqual(extract_markdown_images(text), [('first', '/one.png'), ('second', '/two.png')])
        self.assertEqual(extract_markdown_links(text), [('site', 'https://a.test')])
        self.assertEqual(extract_markdown_images('none'), [])

    def test_repeated_adjacent_references(self):
        for split, kind, syntax in [(split_nodes_image, TextType.IMAGE, '![a](/a)'), (split_nodes_link, TextType.LINK, '[a](/a)')]:
            self.assertEqual(split([TextNode(syntax * 2, TextType.TEXT)]), [TextNode('a', kind, '/a')] * 2)

    def test_reference_surrounding_text(self):
        self.assertEqual(split_nodes_image([TextNode('before ![](/x) after', TextType.TEXT)]),
                         [TextNode('before ', TextType.TEXT), TextNode('', TextType.IMAGE, '/x'), TextNode(' after', TextType.TEXT)])

    def test_plain_empty(self):
        self.assertEqual(text_to_textnodes('hello'), [TextNode('hello', TextType.TEXT)])
        self.assertEqual(text_to_textnodes(''), [])

    def test_full_inline(self):
        nodes = text_to_textnodes('This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)')
        self.assertEqual([n.text_type for n in nodes], [TextType.TEXT, TextType.BOLD, TextType.TEXT, TextType.ITALIC, TextType.TEXT, TextType.CODE, TextType.TEXT, TextType.IMAGE, TextType.TEXT, TextType.LINK])
        self.assertEqual(nodes[-1].url, 'https://boot.dev')

    def test_code_and_url_underscores(self):
        self.assertEqual(text_to_textnodes('`a_b **c**` [ref](/some_path)'), [TextNode('a_b **c**', TextType.CODE), TextNode(' ', TextType.TEXT), TextNode('ref', TextType.LINK, '/some_path')])
