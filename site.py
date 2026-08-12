#!/usr/bin/env python3
"""Build and serve the TraceLogica documentation with no external dependencies."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import shutil
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).parent.resolve()
OUTPUT = ROOT / "site"
PAGES = [
    ("README.md", "index.html", "Documentation home"),
    ("docs/overview.md", "overview.html", "Product overview"),
    ("docs/api-quickstart.md", "api-quickstart.html", "API quickstart"),
    ("docs/concepts.md", "concepts.html", "Core concepts"),
    ("docs/architecture.md", "architecture.html", "Architecture"),
    ("docs/proof-verification.md", "proof-verification.html", "Verification"),
    ("docs/security.md", "security.html", "Security"),
    ("docs/status.md", "status.html", "Status"),
    ("docs/otlp-ingestion.md", "otlp-ingestion.html", "OTLP scope"),
    ("docs/glossary.md", "glossary.html", "Glossary"),
    ("CONTRIBUTING.md", "contributing.html", "Contributing"),
    ("SECURITY.md", "security-policy.html", "Security policy"),
]
ROUTES = {source: target for source, target, _ in PAGES}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def rewrite_link(href: str, source: str) -> str:
    parsed = urlsplit(href)
    if parsed.scheme or href.startswith(("#", "/")):
        return href
    resolved = (Path(source).parent / parsed.path).as_posix()
    normalized = str(Path(resolved))
    target = ROUTES.get(normalized)
    if not target:
        return href
    return target + (("#" + parsed.fragment) if parsed.fragment else "")


def inline(value: str, source: str) -> str:
    tokens: list[str] = []

    def stash(fragment: str) -> str:
        tokens.append(fragment)
        return f"\x00{len(tokens) - 1}\x00"

    value = re.sub(r"`([^`]+)`", lambda m: stash(f"<code>{html.escape(m.group(1))}</code>"), value)
    value = re.sub(
        r"!\[([^]]*)\]\(([^)]+)\)",
        lambda m: stash(f'<img src="{html.escape(rewrite_link(m.group(2), source), quote=True)}" alt="{html.escape(m.group(1), quote=True)}" loading="lazy">'),
        value,
    )
    value = re.sub(
        r"\[([^]]+)\]\(([^)]+)\)",
        lambda m: stash(f'<a href="{html.escape(rewrite_link(m.group(2), source), quote=True)}">{html.escape(m.group(1))}</a>'),
        value,
    )
    value = html.escape(value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    for index, token in enumerate(tokens):
        value = value.replace(f"\x00{index}\x00", token)
    return value


def markdown(source: str) -> tuple[str, str, list[tuple[str, str]]]:
    lines = (ROOT / source).read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    headings: list[tuple[str, str]] = []
    paragraph: list[str] = []
    list_type: str | None = None
    list_item: list[str] = []
    code: list[str] | None = None
    language = ""
    quote: list[str] = []
    i = 0

    def flush_paragraph() -> None:
        if paragraph:
            out.append(f"<p>{inline(' '.join(part.strip() for part in paragraph), source)}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_type
        flush_list_item()
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    def flush_list_item() -> None:
        if list_item:
            out.append(f"<li>{inline(' '.join(part.strip() for part in list_item), source)}</li>")
            list_item.clear()

    def flush_quote() -> None:
        if quote:
            out.append(f"<blockquote><p>{inline(' '.join(quote), source)}</p></blockquote>")
            quote.clear()

    while i < len(lines):
        line = lines[i]
        if code is not None:
            if line.startswith("```"):
                escaped = html.escape("\n".join(code))
                label = html.escape(language or "text")
                out.append(f'<div class="code-block"><div class="code-label">{label}</div><pre><code class="language-{label}">{escaped}</code></pre></div>')
                code = None
            else:
                code.append(line)
            i += 1
            continue
        if line.startswith("```"):
            flush_paragraph(); close_list(); flush_quote()
            code, language = [], line[3:].strip()
        elif re.match(r"^#{1,6} ", line):
            flush_paragraph(); close_list(); flush_quote()
            level = len(line) - len(line.lstrip("#"))
            text = line[level + 1:]
            anchor = slugify(text)
            if level > 1:
                headings.append((anchor, text))
            out.append(f'<h{level} id="{anchor}">{inline(text, source)}<a class="heading-anchor" href="#{anchor}" aria-label="Link to {html.escape(text, quote=True)}">#</a></h{level}>')
        elif line.startswith("> "):
            flush_paragraph(); close_list(); quote.append(line[2:].strip())
        elif (match := re.match(r"^(- |\d+\. )(.*)", line)):
            flush_paragraph(); flush_quote()
            kind = "ul" if match.group(1) == "- " else "ol"
            if list_type != kind:
                close_list(); list_type = kind; out.append(f"<{kind}>")
            else:
                flush_list_item()
            list_item.append(match.group(2))
        elif line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|(?:\s*:?-+:?\s*\|)+$", lines[i + 1]):
            flush_paragraph(); close_list(); flush_quote()
            headers = [x.strip() for x in line.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([x.strip() for x in lines[i].strip("|").split("|")]); i += 1
            out.append('<div class="table-wrap"><table><thead><tr>' + ''.join(f"<th scope=\"col\">{inline(x, source)}</th>" for x in headers) + "</tr></thead><tbody>")
            out.extend("<tr>" + ''.join(f"<td>{inline(x, source)}</td>" for x in row) + "</tr>" for row in rows)
            out.append("</tbody></table></div>")
            continue
        elif not line.strip():
            flush_paragraph(); close_list(); flush_quote()
        elif list_type:
            # CommonMark permits continuation text on following indented or
            # lazily continued lines. Keep it inside the active list item.
            list_item.append(line)
        else:
            close_list(); flush_quote(); paragraph.append(line)
        i += 1
    flush_paragraph(); close_list(); flush_quote()
    title = next((text for anchor, text in [(slugify(lines[0][2:]), lines[0][2:])] if lines and lines[0].startswith("# ")), "TraceLogica")
    return title, "\n".join(out), headings


def template(title: str, body: str, headings: list[tuple[str, str]], current: str) -> str:
    nav = "".join(f'<a href="{target}"' + (' aria-current="page"' if target == current else '') + f'>{html.escape(label)}</a>' for _, target, label in PAGES[:10])
    toc = "".join(f'<a href="#{anchor}">{html.escape(label)}</a>' for anchor, label in headings)
    return f'''<!doctype html>
<html lang="en" data-theme="auto">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="TraceLogica signed checkpoint authority documentation.">
  <title>{html.escape(title)} · TraceLogica docs</title>
  <link rel="icon" href="assets/brand/tracelogica-github-blue.png"><script>document.documentElement.classList.add('js')</script><link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip-link" href="#content">Skip to content</a>
<div class="release-banner" role="status"><span>Pre-release</span> Signed-checkpoint MVP · Checkpoint authority not yet deployed · Interfaces may change</div>
<header class="topbar">
  <a class="brand" href="index.html" aria-label="TraceLogica documentation home"><img src="assets/brand/tracelogica-github-blue.png" alt=""><strong>TraceLogica</strong><span>Docs</span></a>
  <div class="header-actions"><a href="https://github.com/tracelogica/docs">GitHub</a><a href="status.html">Project status</a><button id="theme-toggle" type="button" aria-label="Switch color theme"><span aria-hidden="true">◐</span></button><button id="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span aria-hidden="true">☰</span><span class="sr-only">Open navigation</span></button></div>
</header>
<div class="layout">
  <nav id="site-nav" class="sidebar" aria-label="Documentation"><div class="nav-label">Documentation</div>{nav}<div class="nav-label secondary">Project</div><a href="contributing.html">Contributing</a><a href="https://github.com/tracelogica/docs">GitHub repository</a><a href="security-policy.html">Security policy</a></nav>
  <main id="content" tabindex="-1"><article>{body}<footer><span>TraceLogica documentation</span><span>Signed checkpoints, independently verifiable.</span></footer></article></main>
  <aside class="toc" aria-label="On this page"><div class="nav-label">On this page</div>{toc or '<a href="#content">Overview</a>'}</aside>
</div><script src="assets/site.js"></script></body></html>'''


def build() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    (OUTPUT / "assets").mkdir(parents=True)
    shutil.copytree(ROOT / "assets" / "brand", OUTPUT / "assets" / "brand")
    shutil.copy2(ROOT / "web" / "site.css", OUTPUT / "assets" / "site.css")
    shutil.copy2(ROOT / "web" / "site.js", OUTPUT / "assets" / "site.js")
    for source, target, _ in PAGES:
        title, body, headings = markdown(source)
        (OUTPUT / target).write_text(template(title, body, headings, target), encoding="utf-8")
    digest = hashlib.sha256("".join((ROOT / p).read_text() for p, _, _ in PAGES).encode()).hexdigest()[:12]
    print(f"Built {len(PAGES)} pages in {OUTPUT} (content {digest})")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "serve"), nargs="?", default="build")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    build()
    if args.command == "serve":
        handler = lambda *a, **kw: SimpleHTTPRequestHandler(*a, directory=str(OUTPUT), **kw)
        print(f"Serving http://127.0.0.1:{args.port}")
        ThreadingHTTPServer(("127.0.0.1", args.port), handler).serve_forever()


if __name__ == "__main__":
    main()
