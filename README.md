# Static Site Generator

A Python static site generator built for Boot.dev's **Build a Static Site Generator** course. It converts Markdown into HTML using text nodes, recursive HTML trees, and a page template. Python's standard library is the only dependency.

## Run locally

```sh
./main.sh
```

Open http://localhost:8888. Stop the server with Ctrl+C.

## Test

```sh
./test.sh
```

## Build for GitHub Pages

```sh
./build.sh
```

The generated site is in `docs/`, with `/static-site-generator/` as its base path. GitHub Pages serves `docs/` from the `main` branch.

## Content

- `content/`: Markdown pages; nested directories retain their structure.
- `static/`: CSS and images copied into each build.
- `template.html`: HTML document with title and content placeholders.
- `src/`: Node models, inline and block parsers, page generation, and tests.

Supported Markdown: headings, paragraphs, bold, italic, inline code, fenced code blocks, links, images, blockquotes, ordered and unordered lists. Nested inline formatting is outside the course's scope.

The Tolkien example content and images are supplied by the Boot.dev course.
