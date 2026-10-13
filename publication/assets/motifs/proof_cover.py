"""Render the separate original cover illustration at its 4.8-inch print width."""

from pathlib import Path
import json
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
html = '''<!doctype html><html lang="en"><meta charset="utf-8"><title>Cover illustration proof</title>
<style>@page{size:8.5in 11in;margin:.6in}body{margin:0;background:white;color:#202c28;font:12px Georgia,serif}h1{font-size:20px;font-weight:normal}figure{margin:0 0 20px;break-inside:avoid}img{width:4.8in;height:3.4in;display:block}figcaption{margin-top:5px;font-size:10px}@media screen{body{padding:24px;width:620px}}</style>
<h1>A harvest tended</h1><p>Original cover illustration, reproduced 4.8 inches wide. Artwork has a transparent background.</p>
<figure><img src="cover-harvest.svg"><figcaption>Ink and olive on white</figcaption></figure>
<figure><img src="monochrome/cover-harvest.svg"><figcaption>Black-only production alternative</figcaption></figure>
</html>'''
(BASE / "cover-print-proof.html").write_text(html)
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width":720,"height":1100},device_scale_factor=1.5)
    page.goto((BASE / "cover-print-proof.html").as_uri(),wait_until="networkidle")
    assert page.locator("img").evaluate_all("a=>a.length===2&&a.every(x=>x.complete&&x.naturalWidth===480)")
    page.screenshot(path=str(BASE / "cover-print-proof.png"),full_page=True)
    page.pdf(path=str(BASE / "cover-print-proof.pdf"),prefer_css_page_size=True,print_background=True)
    page.set_viewport_size({"width":960,"height":680})
    page.goto((BASE / "cover-harvest.svg").as_uri())
    box=page.locator("svg>g").evaluate("g=>{const b=g.getBBox();return {x:b.x,y:b.y,width:b.width,height:b.height}}")
    assert box["x"]>=25 and box["y"]>=25 and box["x"]+box["width"]<=455 and box["y"]+box["height"]<=326
    page.locator("svg").evaluate('(e)=>{e.style.width="960px";e.style.height="680px";e.style.background="#f4f0e5";}')
    page.screenshot(path=str(BASE / "cover-harvest-proof.png"))
    browser.close()
(BASE / "cover-proof-results.json").write_text(json.dumps({"file":"cover-harvest.svg","print_width_inches":4.8,"geometry_bounds":box,"line_weights_points_at_print_width":{"main":1.296,"fine":0.432}},indent=2)+"\n")
print("Rendered cover art in two palettes at 4.8 inches and verified geometry bounds.")
