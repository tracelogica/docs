import subprocess
import sys
import unittest
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).parents[1]
SITE = ROOT / "site"


class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = set(); self.links = []; self.images = []; self.landmarks = set(); self.has_lang = False; self.has_title = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html": self.has_lang = bool(attrs.get("lang"))
        if tag == "title": self.has_title = True
        if tag in {"main", "nav", "header"}: self.landmarks.add(tag)
        if attrs.get("id"): self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"): self.links.append(attrs["href"])
        if tag == "img": self.images.append(attrs)


class SiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "site.py", "build"], cwd=ROOT, check=True)

    def test_pages_are_accessible_and_linked(self):
        pages = list(SITE.glob("*.html")); self.assertGreaterEqual(len(pages), 10)
        for page in pages:
            parser = Inspector(); parser.feed(page.read_text())
            self.assertTrue(parser.has_lang and parser.has_title, page)
            self.assertEqual(parser.landmarks, {"main", "nav", "header"}, page)
            self.assertTrue(all("alt" in image for image in parser.images), page)
            for href in parser.links:
                parsed = urlsplit(href)
                if parsed.scheme or href.startswith(("mailto:", "https://", "http://")): continue
                target = page if not parsed.path else SITE / parsed.path
                self.assertTrue(target.exists(), f"{page.name}: broken link {href}")
                if parsed.fragment:
                    linked = Inspector(); linked.feed(target.read_text())
                    self.assertIn(parsed.fragment, linked.ids, f"{page.name}: broken anchor {href}")

    def test_source_content_is_rendered(self):
        rendered = (SITE / "api-quickstart.html").read_text()
        self.assertIn("POST /api/v1/checkpoints", rendered)
        self.assertIn("<table>", rendered)
        self.assertNotIn("docs/api-quickstart.md", rendered)

    def test_multiline_list_items_stay_inside_the_list(self):
        rendered = (SITE / "overview.html").read_text()
        self.assertIn("<li>Security teams evaluating the boundary between a source application and a separate signing authority.</li>", rendered)
        for page in SITE.glob("*.html"):
            self.assertIsNone(re.search(r"</(?:ul|ol)>\s*<p>[a-z]", page.read_text()), page)

    def test_mobile_navigation_is_progressively_enhanced(self):
        css = (SITE / "assets/site.css").read_text()
        html = (SITE / "index.html").read_text()
        self.assertIn(".js .sidebar{display:none", css)
        self.assertNotRegex(css, r"(?<!\.js )\.sidebar\{display:none")
        self.assertIn("document.documentElement.classList.add('js')", html)


if __name__ == "__main__": unittest.main()
