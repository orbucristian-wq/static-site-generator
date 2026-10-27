import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_properties(self):
        self.assertEqual(HTMLNode(props={'href': '/a', 'target': '_blank'}).props_to_html(), ' href="/a" target="_blank"')

    def test_empty_properties(self):
        self.assertEqual(HTMLNode().props_to_html(), '')
        self.assertEqual(HTMLNode(props={}).props_to_html(), '')

    def test_abstract(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

    def test_leaf(self):
        self.assertEqual(LeafNode('p', 'Hello').to_html(), '<p>Hello</p>')
        self.assertEqual(LeafNode(None, 'raw').to_html(), 'raw')
        self.assertEqual(LeafNode('span', '').to_html(), '<span></span>')
        with self.assertRaises(ValueError):
            LeafNode('p', None).to_html()

    def test_recursive_parent(self):
        tree = ParentNode('div', [ParentNode('span', [LeafNode('b', 'child')]), LeafNode(None, '!')], {'id': 'root'})
        self.assertEqual(tree.to_html(), '<div id="root"><span><b>child</b></span>!</div>')

    def test_parent_missing_fields(self):
        for node in [ParentNode(None, []), ParentNode('div', None)]:
            with self.assertRaises(ValueError):
                node.to_html()
        self.assertEqual(ParentNode('div', []).to_html(), '<div></div>')
