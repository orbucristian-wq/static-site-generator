from pathlib import Path
import tempfile
import unittest
from generator import copy_static, extract_title, generate_page, generate_pages_recursive


class TestGenerator(unittest.TestCase):
    def test_title(self):
        self.assertEqual(extract_title('## ignored\n#  Hello  \ntext'), 'Hello')
        for markdown in ['## only', '', '# ']:
            with self.assertRaises(ValueError):
                extract_title(markdown)

    def test_recursive_copy_cleans_stale_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, dest = root / 'static', root / 'output'
            (source / 'nested/deep').mkdir(parents=True)
            (source / 'nested/deep/file.bin').write_bytes(b'\x00\xffhello')
            dest.mkdir()
            (dest / 'stale').write_text('old')
            copy_static(source, dest)
            self.assertFalse((dest / 'stale').exists())
            self.assertEqual((dest / 'nested/deep/file.bin').read_bytes(), b'\x00\xffhello')

    def test_copy_rejects_source_overlap(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            for dest in [source, source / 'nested', source.parent]:
                with self.assertRaises(ValueError):
                    copy_static(source, dest)

    def test_generate_recursive_and_basepath(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content, output = root / 'content', root / 'output'
            (content / 'blog/deep').mkdir(parents=True)
            (content / 'index.md').write_text('# Home\n\n[Post](/blog/deep/)\n\n![alt](/img.png)')
            (content / 'blog/deep/index.md').write_text('# Nested\n\n[External](https://example.com)')
            (content / 'ignored.txt').write_text('ignored')
            template = root / 'template.html'
            template.write_text('<title>{{ Title }}</title><link href="/index.css">{{ Content }}')
            generate_pages_recursive(content, template, output, '/project/')
            home = (output / 'index.html').read_text()
            self.assertIn('<title>Home</title>', home)
            self.assertIn('href="/project/blog/deep/"', home)
            self.assertIn('src="/project/img.png"', home)
            self.assertIn('href="/project/index.css"', home)
            self.assertNotIn('{{ ', home)
            nested = (output / 'blog/deep/index.html').read_text()
            self.assertIn('href="https://example.com"', nested)
            self.assertFalse((output / 'ignored.html').exists())

    def test_local_root_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'page.md').write_text('# Home\n\n[Back](/)')
            (root / 'template').write_text('{{ Content }}')
            generate_page(root / 'page.md', root / 'template', root / 'index.html')
            self.assertIn('href="/"', (root / 'index.html').read_text())
