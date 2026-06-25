#!/usr/bin/env python3
"""
carbide-tooling.com 优化: 删黑帽隐藏词块 + 补 schema/favicon/og + 重生成sitemap
执行: python3 optimize-carbide.py [--check]
"""
import os, re, json, glob, sys
from html import escape

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://carbide-tooling.com"
TODAY = "2026-06-23"
FAVICON = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22><rect width=%2232%22 height=%2232%22 rx=%227%22 fill=%22%2306c%22/><text x=%2216%22 y=%2223%22 font-size=%2218%22 text-anchor=%22middle%22 fill=%22white%22>◆</text></svg>">'

# 产品/指南页元数据 (name, category, url_path, type)
PAGES_META = {
    "products/end-mills.html":        ("Carbide End Mills", "End Mills", "product"),
    "products/turning-inserts.html":  ("Turning Inserts", "Turning Inserts", "product"),
    "products/drills.html":           ("Carbide Drills", "Drills", "product"),
    "products/tool-holders.html":     ("Tool Holders", "Tool Holders", "product"),
    "products/boring-tools.html":     ("Boring & Reaming Tools", "Boring Tools", "product"),
    "products/threading-tools.html":  ("Threading Tools", "Threading Tools", "product"),
    "guides/end-mill-geometry.html":  ("End Mill Geometry Guide", "Guides", "article"),
    "guides/carbide-grades.html":     ("Carbide Grades Explained", "Guides", "article"),
    "guides/coating-comparison.html": ("Coating Comparison", "Guides", "article"),
    "guides/sourcing-from-china.html":("Sourcing Cutting Tools from China", "Guides", "article"),
}

PRODUCT_FAQ = [
    ("What is the MOQ?", "MOQ starts from 10 pcs for standard sizes. Custom geometries may require higher MOQ."),
    ("What is the lead time?", "Typically 7-21 days depending on quantity, complexity, and coating requirements."),
    ("Can I get samples before ordering?", "Yes. We arrange samples for evaluation before bulk production. Contact us with your specs."),
    ("What coatings are available?", "AlTiN, TiSiN, TiAlN, TiCN, DLC, and uncoated. Coating is selected based on your material and operation."),
]

def get_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    return m.group(1).strip() if m else ""

def get_desc(html):
    m = re.search(r'<meta name="description" content="([^"]*)"', html, re.S)
    return m.group(1).strip() if m else ""

def get_meta(html, name):
    m = re.search(r'<meta\s+(?:name|property)=["\']' + re.escape(name) + r'["\']\s+content=["\'](.*?)["\']', html, re.S)
    return m.group(1).strip() if m else None

def set_meta(html, name, content):
    pat = re.compile(r'(<meta\s+(?:name|property)=["\']' + re.escape(name) + r'["\']\s+content=["\'])[^"\']*(["\'])', re.S)
    if pat.search(html):
        return pat.sub(lambda m: m.group(1) + content + m.group(2), html)
    return None

def build_product_schema(name, desc, url):
    obj = {
        "@context": "https://schema.org", "@type": "Product",
        "name": name, "description": desc,
        "url": url,
        "brand": {"@type": "Brand", "name": "Carbide Tooling"},
        "category": "CNC Cutting Tools",
        "manufacturer": {"@type": "Organization", "name": "Carbide Tooling"},
    }
    return obj

def build_article_schema(title, desc, url):
    return {
        "@context": "https://schema.org", "@type": "Article",
        "headline": title, "description": desc,
        "url": url, "mainEntityOfPage": url,
        "datePublished": TODAY, "dateModified": TODAY,
        "publisher": {"@type": "Organization", "name": "Carbide Tooling"},
    }

def build_breadcrumb(items):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": n, "item": u}
            for i, (n, u) in enumerate(items)
        ],
    }

def build_faq(pairs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }

def inject_jsonld(html, new_objs):
    """注入对象到已有 JSON-LD 数组；无 JSON-LD 则在 </head> 前新建"""
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', html, re.S)
    if m:
        try:
            data = json.loads(m.group(2))
        except Exception:
            data = []
        types = [o.get("@type") for o in data]
        for obj in new_objs:
            if obj["@type"] not in types:
                data.append(obj)
        block = m.group(1) + "\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n  " + m.group(3)
        return html[:m.start()] + block + html[m.end():], "jsonld"
    else:
        block = '\n  <script type="application/ld+json">\n' + json.dumps(new_objs, ensure_ascii=False, indent=2) + '\n  </script>\n'
        html = html.replace("</head>", block + "</head>", 1)
        return html, "jsonld-new"

def process_file(path, dry=False):
    rel = os.path.relpath(path, BASE)
    html = open(path, encoding="utf-8").read()
    acts = []

    # 1. 删除 SEO-KEYWORDS 隐藏块
    new, n = re.subn(r'\s*<!-- SEO-KEYWORDS -->.*?<!-- END SEO-KEYWORDS -->', '', html, flags=re.S)
    if n:
        html = new; acts.append(f"del-kw({n})")

    # 2. favicon (无则加在 canonical 后)
    if 'rel="icon"' not in html and 'rel="shortcut icon"' not in html:
        html = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1\n' + FAVICON, html, count=1)
        acts.append("favicon")

    # 3. og:image 修正: 本地无 og-image.jpg, 改用 /images/hero.jpg
    og_img = get_meta(html, "og:image")
    if og_img and "og-image.jpg" in og_img:
        html = set_meta(html, "og:image", SITE + "/images/hero.jpg") or html
        acts.append("ogimg")
    elif not og_img:
        ins = f'\n<meta property="og:image" content="{SITE}/images/hero.jpg">'
        html = re.sub(r'(<meta name="robots"[^>]*>)', r'\1' + ins, html, count=1)
        acts.append("ogimg+")

    # 4. og:title / og:description / og:type 补全
    title = get_title(html); desc = get_desc(html)
    for prop, val in [("og:title", title), ("og:description", desc), ("og:type", "website")]:
        cur = get_meta(html, prop)
        if not cur:
            ins = f'\n<meta property="{prop}" content="{val}">'
            # 插到 og:image 后
            html = re.sub(r'(<meta property="og:image"[^>]*>)', r'\1' + ins, html, count=1)
            acts.append("og+" + prop)

    # 5. schema 注入 (产品/指南详情页)
    if rel in PAGES_META:
        name, cat, ptype = PAGES_META[rel]
        url = SITE + "/" + rel
        bc = build_breadcrumb([("Home", SITE + "/"), (cat, SITE + "/products/" if ptype == "product" else SITE + "/guides/"), (name, url)])
        if ptype == "product":
            objs = [build_product_schema(name, desc, url), bc, build_faq(PRODUCT_FAQ)]
        else:
            objs = [build_article_schema(title, desc, url), bc]
        html, st = inject_jsonld(html, objs)
        acts.append(st)

    # 6. 列表/其他页补 BreadcrumbList (index/products-index/guides-index)
    if rel in ("index.html", "products/index.html", "guides/index.html"):
        url = SITE + ("/" if rel == "index.html" else "/" + rel.replace("index.html", ""))
        bc = build_breadcrumb([("Home", SITE + "/")])
        html, st = inject_jsonld(html, [bc])
        acts.append(st)

    if not dry and acts:
        open(path, "w", encoding="utf-8").write(html)
    return rel, ",".join(acts) if acts else "skip"

def regen_sitemap():
    entries = [
        (SITE + "/", 1.0, "daily"),
        (SITE + "/products/", 0.9, "weekly"),
        (SITE + "/products/end-mills.html", 0.8, "weekly"),
        (SITE + "/products/turning-inserts.html", 0.8, "weekly"),
        (SITE + "/products/drills.html", 0.8, "weekly"),
        (SITE + "/products/tool-holders.html", 0.8, "weekly"),
        (SITE + "/products/boring-tools.html", 0.8, "weekly"),
        (SITE + "/products/threading-tools.html", 0.8, "weekly"),
        (SITE + "/guides/", 0.8, "monthly"),
        (SITE + "/guides/end-mill-geometry.html", 0.8, "monthly"),
        (SITE + "/guides/carbide-grades.html", 0.8, "monthly"),
        (SITE + "/guides/coating-comparison.html", 0.8, "monthly"),
        (SITE + "/guides/sourcing-from-china.html", 0.8, "monthly"),
        (SITE + "/about.html", 0.5, "monthly"),
        (SITE + "/quote.html", 0.7, "monthly"),
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, pri, freq in entries:
        lines.append(f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>')
    lines.append('</urlset>')
    open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return len(entries)

def main():
    dry = "--check" in sys.argv
    if dry: print("=== CHECK 模式 ===")
    files = sorted(glob.glob(os.path.join(BASE, "*.html")) +
                   glob.glob(os.path.join(BASE, "products/*.html")) +
                   glob.glob(os.path.join(BASE, "guides/*.html")))
    print(f"共 {len(files)} 页\n")
    for f in files:
        rel, acts = process_file(f, dry=dry)
        print(f"  {rel:40s} {acts}")
    if not dry:
        n = regen_sitemap()
        print(f"\nsitemap.xml 重生成: {n} 条 URL (含 lastmod/changefreq)")

if __name__ == "__main__":
    main()
