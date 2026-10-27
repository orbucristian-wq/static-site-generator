import unittest
from blocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestBlocks(unittest.TestCase):
    def test_split(self):
        self.assertEqual(markdown_to_blocks('\n\n # title\n\n\nparagraph\nnext\n\n- one\n- two\n'), ['# title', 'paragraph\nnext', '- one\n- two'])
        self.assertEqual(markdown_to_blocks(' \n\n'), [])

    def test_block_types(self):
        cases = [('# title', BlockType.HEADING), ('###### title', BlockType.HEADING),
                 ('####### title', BlockType.PARAGRAPH), ('#no space', BlockType.PARAGRAPH),
                 ('```\nx\n```', BlockType.CODE), ('```x```', BlockType.PARAGRAPH),
                 ('>one\n> two', BlockType.QUOTE), ('>one\ntwo', BlockType.PARAGRAPH),
                 ('- one\n- two', BlockType.UNORDERED_LIST), ('-one', BlockType.PARAGRAPH),
                 ('1. one\n2. two', BlockType.ORDERED_LIST), ('1. one\n3. three', BlockType.PARAGRAPH),
                 ('2. two', BlockType.PARAGRAPH)]
        for text, kind in cases:
            with self.subTest(text=text):
                self.assertEqual(block_to_block_type(text), kind)

    def test_paragraphs(self):
        self.assertEqual(markdown_to_html_node('This is **bolded** paragraph\ntext in a p\ntag here\n\nThis is another paragraph with _italic_ text and `code` here').to_html(),
                         '<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>')

    def test_code_literal(self):
        self.assertEqual(markdown_to_html_node('```\nThis _should_ remain\n**same**\n```').to_html(), '<div><pre><code>This _should_ remain\n**same**\n</code></pre></div>')

    def test_headings(self):
        for level in range(1, 7):
            self.assertEqual(markdown_to_html_node('#' * level + ' Hello **world**').to_html(), f'<div><h{level}>Hello <b>world</b></h{level}></div>')

    def test_quote(self):
        self.assertEqual(markdown_to_html_node('>hello\n> **world**').to_html(), '<div><blockquote>hello <b>world</b></blockquote></div>')

    def test_lists(self):
        self.assertEqual(markdown_to_html_node('- one\n- _two_').to_html(), '<div><ul><li>one</li><li><i>two</i></li></ul></div>')
        self.assertEqual(markdown_to_html_node('1. one\n2. `two`').to_html(), '<div><ol><li>one</li><li><code>two</code></li></ol></div>')

    def test_empty(self):
        self.assertEqual(markdown_to_html_node('').to_html(), '<div></div>')
