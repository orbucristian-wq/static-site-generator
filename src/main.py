from pathlib import Path
import sys
from generator import copy_static, generate_pages_recursive


ROOT = Path(__file__).resolve().parent.parent


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
    output = ROOT / 'docs'
    copy_static(ROOT / 'static', output)
    generate_pages_recursive(ROOT / 'content', ROOT / 'template.html', output, basepath)


if __name__ == '__main__':
    main()
