#!/usr/bin/env python3
"""Read-only crawler checks against a running build or deployed candidate.

Checks the actual HTML a non-JavaScript crawler receives, including the dynamic
offer page, and every advertised image's bytes. No forms or APIs are submitted.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import struct
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://survivingthesingularity.com"


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.values = {}

    def add(self, key, value):
        self.values.setdefault(key, []).append(value)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head":
            self.in_head = True
        if not self.in_head:
            return
        if tag == "title":
            self.add("title", "present")
        elif tag == "meta":
            self.add(attrs.get("property", attrs.get("name", "")), attrs.get("content", ""))
        elif tag == "link" and attrs.get("rel") == "canonical":
            self.add("canonical", attrs.get("href", ""))

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False


def check(origin):
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, request, fp, code, msg, headers, newurl):
            raise AssertionError(f"Unexpected redirect from reviewed route: {request.full_url}")

    # A local Worker check must stay local even on proxy-configured runners.
    handlers = [NoRedirect()]
    if urllib.parse.urlsplit(origin).hostname in {"localhost", "127.0.0.1", "::1"}:
        handlers.append(urllib.request.ProxyHandler({}))
    opener = urllib.request.build_opener(*handlers)

    def get(path):
        request = urllib.request.Request(origin + path, headers={"User-Agent": "Twitterbot/1.0"})
        with opener.open(request, timeout=20) as response:
            assert response.status == 200, f"{path}: HTTP {response.status}"
            return response.read(), response.headers.get("Content-Type", "")

    sitemap = (ROOT / "static/sitemap.xml").read_bytes()
    served_sitemap, _ = get("/sitemap.xml")
    assert served_sitemap == sitemap, "Published sitemap differs from the reviewed release"
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [item.text for item in ET.fromstring(sitemap).findall("s:url/s:loc", namespace)]
    fields = ["title", "description", "canonical", "og:title", "og:description", "og:url", "og:type",
              "og:image", "og:image:alt", "twitter:card", "twitter:title", "twitter:description", "twitter:image"]
    images = {}
    pages = []
    for url in urls:
        path = urllib.parse.urlsplit(url).path
        # Campaign query parameters must not contaminate canonical/share tags.
        blob, content_type = get(path + "?utm_source=launch-validation&utm_medium=social&utm_campaign=book_release")
        assert "text/html" in content_type, f"{path}: not HTML ({content_type})"
        head = Head()
        head.feed(blob.decode("utf-8"))
        values = head.values
        for field in fields:
            found = values.get(field, [])
            assert len(found) == 1 and found[0].strip(), f"{path}: expected one nonempty {field}, got {found}"
        assert values["canonical"] == [url], f"{path}: canonical mismatch"
        assert values["og:url"] == [url], f"{path}: share URL mismatch"
        assert values["twitter:card"] == ["summary_large_image"], f"{path}: wrong Twitter card"
        assert values["twitter:image"] == values["og:image"], f"{path}: conflicting preview images"
        assert not any("noindex" in robots.lower() for robots in values.get("robots", [])), f"{path}: noindex route in sitemap"
        image_url = urllib.parse.urlsplit(values["og:image"][0])
        assert image_url.scheme == "https" and image_url.netloc == urllib.parse.urlsplit(SITE).netloc, f"{path}: preview must use an absolute first-party HTTPS image"
        image_path = image_url.path + ("?" + image_url.query if image_url.query else "")
        if image_path not in images:
            image, image_type = get(image_path)
            assert image_type.split(";", 1)[0] == "image/png", f"{image_path}: wrong MIME type {image_type}"
            assert image.startswith(b"\x89PNG\r\n\x1a\n") and image[12:16] == b"IHDR", f"{image_path}: not a PNG"
            width, height = struct.unpack(">II", image[16:24])
            assert width >= 1200 and height >= 630 and 1.8 < width / height < 2.0, f"{image_path}: wrong card size {width}x{height}"
            assert len(image) < 5_000_000, f"{image_path}: image exceeds social-card size budget"
            expected = ROOT / "static" / image_url.path.lstrip("/")
            assert expected.read_bytes() == image, f"{image_path}: served image differs from reviewed release"
            images[image_path] = {"width": width, "height": height, "bytes": len(image), "sha256": hashlib.sha256(image).hexdigest()}
        for dimension in ["width", "height"]:
            assert values.get("og:image:" + dimension) == [str(images[image_path][dimension])], f"{path}: declared image {dimension} differs from actual PNG"
        pages.append({"path": path, "title": values["og:title"][0], "image": values["og:image"][0]})
    return {"origin": origin, "pages": pages, "images": images}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origin", required=True, help="Running candidate origin, e.g. http://127.0.0.1:8788")
    parser.add_argument("--report", type=Path, help="Optional JSON evidence path")
    args = parser.parse_args()
    result = check(args.origin.rstrip("/"))
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Social crawler checks: {len(result['pages'])} canonical pages and {len(result['images'])} PNG previews passed without JavaScript.")
    print("Scope: actual HTTP HTML, campaign-query canonicalization and served image bytes. Platform cache refresh and real social-app previews remain deployment checks.")
