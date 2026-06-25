#!/usr/bin/env python3
"""Generate sitemap.xml for carbide-tooling.com"""
import os, datetime

SITE = "https://carbide-tooling.com"
ROOT = os.path.dirname(__file__)
DATE = datetime.date.today().isoformat()

def priority(path):
    if path == "" or path == "/":
        return "1.0"
    if path.startswith("/tools/"):
        return "0.8"
    if path.startswith("/products/") or path.startswith("/guides/"):
        return "0.6"
    return "0.5"

def changefreq(path):
    if path == "" or path == "/":
        return "weekly"
    if path.startswith("/tools/"):
        return "monthly"
    return "monthly"

pages = [
    ("", DATE, "weekly", "1.0"),
    ("tools/", DATE, "weekly", "0.9"),
    ("about.html", DATE, "monthly", "0.5"),
    ("quote.html", DATE, "monthly", "0.6"),
]

# Products
product_files = [f for f in os.listdir(os.path.join(ROOT, "products")) if f.endswith(".html")]
for pf in sorted(product_files):
    pages.append((f"products/{pf}", DATE, "monthly", "0.6"))

# Guides
guide_files = [f for f in os.listdir(os.path.join(ROOT, "guides")) if f.endswith(".html")]
for gf in sorted(guide_files):
    pages.append((f"guides/{gf}", DATE, "monthly", "0.6"))

# Tools
tool_dirs = sorted(d for d in os.listdir(os.path.join(ROOT, "tools")) 
                   if os.path.isdir(os.path.join(ROOT, "tools", d)))
for td in tool_dirs:
    pages.append((f"tools/{td}/", DATE, "monthly", "0.8"))

xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for path, lastmod, freq, prio in pages:
    xml += "  <url>\n"
    xml += f'    <loc>{SITE}/{path}</loc>\n'
    xml += f'    <lastmod>{lastmod}</lastmod>\n'
    xml += f'    <changefreq>{freq}</changefreq>\n'
    xml += f'    <priority>{prio}</priority>\n'
    xml += "  </url>\n"

xml += '</urlset>\n'

with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write(xml)

print(f"Generated sitemap with {len(pages)} URLs")
