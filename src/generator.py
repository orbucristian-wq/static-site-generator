from pathlib import Path
import shutil
from blocks import markdown_to_html_node


def copy_static(source, destination):
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve() or source.resolve() in destination.resolve().parents or destination.resolve() in source.resolve().parents:
        raise ValueError('Destination must be outside the source directory')
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    _copy_recursive(source, destination)


def _copy_recursive(source, destination):
    for entry in sorted(source.iterdir()):
        target = destination / entry.name
        if entry.is_dir():
            target.mkdir()
            _copy_recursive(entry, target)
        else:
            print(f'Copying {entry} -> {target}')
            shutil.copy2(entry, target)


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith('# ') and line[2:].strip():
            return line[2:].strip()
    raise ValueError('Markdown document requires an h1 heading')


def generate_page(from_path, template_path, dest_path, basepath='/'):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    markdown = Path(from_path).read_text(encoding='utf-8')
    template = Path(template_path).read_text(encoding='utf-8')
    content = markdown_to_html_node(markdown).to_html()
    page = template.replace('{{ Title }}', extract_title(markdown)).replace('{{ Content }}', content)
    basepath = '/' + basepath.strip('/') + '/' if basepath.strip('/') else '/'
    page = page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    destination = Path(dest_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page, encoding='utf-8')


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath='/'):
    source, destination = Path(dir_path_content), Path(dest_dir_path)
    for entry in sorted(source.iterdir()):
        if entry.is_dir():
            generate_pages_recursive(entry, template_path, destination / entry.name, basepath)
        elif entry.suffix == '.md':
            generate_page(entry, template_path, destination / entry.with_suffix('.html').name, basepath)
