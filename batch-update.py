#!/usr/bin/env python3
"""carbide-tooling.com: 补产品页 + GA注入"""
import json
from pathlib import Path

BASE = Path(__file__).parent
GA_ID = ""
SITE = "https://carbide-tooling.com"

NAV = '''
<nav><div class="container nav-inner"><div class="logo"><span>◆</span> Carbide Tooling</div><div><a href="/">Home</a><a href="/products/">Products</a><a href="/guides/">Guides</a><a href="/about.html">About</a><a href="/quote.html">Quote</a></div></div></nav>'''

FOOT = '<footer><div class="container"><p>© 2026 Carbide Tooling</p></div></footer>'

STYLE = '''
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,"SF Pro Display","Helvetica Neue",Arial,sans-serif;background:#fff;color:#1d1d1f;line-height:1.6}
.container{max-width:980px;margin:0 auto;padding:0 22px}
nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.92);backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid #f0f0f0}
.nav-inner{display:flex;align-items:center;justify-content:space-between;height:48px;font-size:12px}
nav a{color:#1d1d1f;text-decoration:none;margin-left:28px;transition:color .2s}
nav a:hover{color:#06c}.logo{font-size:14px;font-weight:600}.logo span{color:#06c}
.bc{font-size:12px;color:#86868b;padding-top:24px;margin-bottom:8px}
.bc a{color:#06c;text-decoration:none}
h1{font-size:36px;font-weight:700;letter-spacing:-0.5px;margin-bottom:16px}
.layout{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-bottom:60px}
.layout img{width:100%;border-radius:18px;background:#f5f5f7}
h2{font-size:20px;font-weight:600;margin:32px 0 12px}p{font-size:15px;color:#333;margin-bottom:12px}
ul{padding-left:20px;margin-bottom:16px}li{font-size:14px;color:#444;margin-bottom:6px}
.specs{width:100%;border-collapse:collapse;font-size:13px;margin:16px 0}
.specs th{background:#f5f5f7;padding:10px 12px;text-align:left;font-weight:600}
.specs td{padding:10px 12px;border-bottom:1px solid #f0f0f0}
.cta-box{background:#f5f5f7;border-radius:18px;padding:32px;text-align:center;margin:40px 0}
.cta-box h3{font-size:20px;margin-bottom:8px}.cta-box p{font-size:14px;color:#666;margin-bottom:20px}
.btn{display:inline-block;background:#1d1d1f;color:#fff;padding:10px 24px;border-radius:24px;font-size:14px;text-decoration:none}
footer{margin-top:60px;padding:32px 0;border-top:1px solid #f0f0f0;text-align:center;font-size:12px;color:#86868b}
@media(max-width:768px){.layout{grid-template-columns:1fr}}
</style>'''

PRODUCTS = [
    {
        "slug":"drills", "img":"drills.jpg",
        "title":"Carbide Drills — Solid & Indexable",
        "desc":"Source solid carbide and indexable drills from China. Up to 20xD, coated and uncoated. Factory-direct pricing for production shops.",
        "intro":"Solid carbide and indexable drills for general and deep-hole drilling. Available with internal coolant, various point geometries, and coatings for steel, stainless, aluminum, and superalloys.",
        "pricing":"$2.00-15.00",
        "specs":[
            ("Type","Diameter","Depth","Coating","Material","Price"),
            ("Solid Carbide","1-12mm","3xD to 8xD","AlTiN / Uncoated","Steel ≤45 HRC","$2.00-8.00"),
            ("Solid Carbide","3-12mm","5xD to 12xD","TiSiN / AlCrN","Hardened ≤55 HRC","$5.00-12.00"),
            ("Solid Carbide","1-10mm","3xD to 8xD","DLC / Uncoated","Aluminum","$3.00-6.00"),
            ("Indexable","12-40mm","2xD to 5xD","CVD / AlTiN","Steel / Cast Iron","$6.00-15.00"),
        ],
        "points":["Solid carbide micro drills down to 0.5mm","Internal coolant holes up to 20xD depth","Indexable drills with interchangeable heads","Step drills, spot drills, center drills available","Custom geometries for special applications"]
    },
    {
        "slug":"tool-holders", "img":"holders.jpg",
        "title":"Tool Holders — BT, HSK, SK Collet Chucks",
        "desc":"Source BT40, BT30, HSK, and SK tool holders from Chinese manufacturers. Collet chucks, end mill holders, ER collets, tapping holders.",
        "intro":"Complete range of CNC tool holders for milling and drilling. All common tapers and clamping systems available. Precision balanced options for high-speed machining.",
        "pricing":"$8.00-45.00",
        "specs":[
            ("Type","Taper","Clamping","Balance","Material","Price"),
            ("Collet Chuck","BT40 / BT30","ER16-ER40","G6.3","Alloy Steel","$12.00-28.00"),
            ("End Mill Holder","BT40 / HSK","Side lock / Weldon","G6.3","Alloy Steel","$10.00-22.00"),
            ("ER Collet","BT40 / SK","ER11-ER40","G2.5","Spring Steel","$3.00-8.00"),
            ("Tapping Holder","BT40 / BT30","ER / Synchro","G6.3","Alloy Steel","$18.00-45.00"),
            ("HSK Holder","HSK63A / HSK100","ER / Collet","G2.5","Alloy Steel","$25.00-60.00"),
        ],
        "points":["BT40, BT30, HSK63A, HSK100, SK40, SK50 available","Runout within 5µm for precision holders","Heat shrink holders for high-speed applications","Milling chucks for heavy roughing","Custom tapers and special lengths on request"]
    },
]

for prod in PRODUCTS:
    bc = f'<div class="bc"><a href="/">Home</a> › <a href="/products/">Products</a> › {prod["title"].split("—")[0].strip()}</div>'
    specs_html = '<table class="specs"><tr>'
    for h in prod["specs"][0]:
        specs_html += f'<th>{h}</th>'
    specs_html += '</tr>'
    for row in prod["specs"][1:]:
        specs_html += '<tr>'
        for cell in row:
            specs_html += f'<td>{cell}</td>'
        specs_html += '</tr>'
    specs_html += '</table>'

    ul_html = '<ul>'
    for pt in prod["points"]:
        ul_html += f'<li>{pt}</li>'
    ul_html += '</ul>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{prod["title"]} | Carbide Tooling</title>
<meta name="description" content="{prod["desc"]}">
<link rel="canonical" href="{SITE}/products/{prod["slug"]}.html">
<meta name="robots" content="index, follow">
{STYLE}
</head>
<body>
{NAV}
<div class="container">
{bc}
<div class="layout">
  <img src="/images/{prod["img"]}" alt="{prod["title"]}" loading="lazy">
  <div>
    <h1>{prod["title"]}</h1>
    <p>{prod["intro"]}</p>
    <p><strong>Price range (FOB):</strong> {prod["pricing"]}</p>
    <p><strong>Typical lead time:</strong> 7-21 days</p>
    <p><strong>MOQ:</strong> From 10 pcs</p>
    <a href="/quote.html" class="btn" style="margin-top:12px;">Get a Quote →</a>
  </div>
</div>
<h2>Standard Specifications</h2>
{specs_html}
<h2>Available Options</h2>
{ul_html}
<div class="cta-box">
  <h3>Need a quote or sample?</h3>
  <p>Tell us what you need — type, size, quantity, and target price. We'll connect you with the right factory.</p>
  <a href="/quote.html" class="btn">Submit Requirements →</a>
</div>
</div>
{FOOT}
</body>
</html>'''
    (BASE / f"products/{prod['slug']}.html").write_text(html, encoding="utf-8")
    print(f"✅ products/{prod['slug']}.html")

# GA注入到所有页面
for f in list(BASE.rglob("*.html")):
    c = f.read_text(encoding="utf-8")
    if GA_ID and f'gtag/js?id={GA_ID}' not in c:
        ga = f'  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag(\'js\',new Date());gtag(\'config\',\'{GA_ID}\');</script>'
        c = c.replace('</head>', f'{ga}\n</head>')
        f.write_text(c, encoding="utf-8")
        print(f"  GA: {f.name}")

# 更新sitemap
pages = [
    "index.html","products/index.html","products/end-mills.html","products/turning-inserts.html",
    "products/drills.html","products/tool-holders.html",
    "guides/index.html","guides/end-mill-geometry.html","guides/carbide-grades.html",
    "guides/coating-comparison.html","about.html","quote.html"
]
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p in pages:
    name = p.replace("index.html","").replace(".html","")
    url = f"{SITE}/{name}" if name else SITE
    pr = {"index":1.0,"products/":0.9,"end-mills":0.8,"turning-inserts":0.8,"drills":0.8,"tool-holders":0.8,"about":0.5,"quote":0.7}
    prio = "0.7"
    for k,v in pr.items():
        if k in p: prio=v; break
    xml += f'  <url><loc>{url}</loc><priority>{prio}</priority></url>\n'
xml += '</urlset>\n'
Path(BASE / "sitemap.xml").write_text(xml, encoding="utf-8")
print("✅ sitemap.xml 更新")

print("\n=== CNC站完毕 ===")
