#!/usr/bin/env python3
"""carbide-tooling.com SEO 注入 + sitemap + robots + 第一篇指南内容"""
import os, json
from pathlib import Path

BASE = Path(__file__).parent
SITE = "https://carbide-tooling.com"
GA_ID = ""  # 填入 GA ID 后可启用

PAGES = [
    {"file":"index.html","url":SITE+"/","prio":"1.0","title":"Carbide Tooling — Precision Cutting Tools Sourcing"},
    {"file":"about.html","url":SITE+"/about.html","prio":"0.5","title":"About — Carbide Tooling"},
    {"file":"quote.html","url":SITE+"/quote.html","prio":"0.7","title":"Get a Quote — Carbide Tooling"},
    {"file":"guides/index.html","url":SITE+"/guides/","prio":"0.8","title":"Technical Guides — Carbide Tooling"},
]

# 1. robots.txt
robots = "User-agent: *\nAllow: /\n\nSitemap: " + SITE + "/sitemap.xml\n"
(BASE / "robots.txt").write_text(robots, encoding="utf-8")
print("✅ robots.txt")

# 2. sitemap.xml
xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p in PAGES:
    xml += f'  <url><loc>{p["url"]}</loc><priority>{p["prio"]}</priority></url>\n'
xml += '</urlset>\n'
(BASE / "sitemap.xml").write_text(xml, encoding="utf-8")
print("✅ sitemap.xml")

# 3. 每页注入 canonical + JSON-LD + GA
for p in PAGES:
    fpath = BASE / p["file"]
    content = fpath.read_text(encoding="utf-8")
    changes = []

    # canonical (在 </title> 后)
    if 'rel="canonical"' not in content:
        content = content.replace("</title>", f'</title>\n<link rel="canonical" href="{p["url"]}">')
        changes.append("canonical")

    # JSON-LD
    if 'ld+json' not in content:
        ld = [
            {"@context":"https://schema.org","@type":"Organization","name":"Carbide Tooling","url":SITE},
            {"@context":"https://schema.org","@type":"WebSite","name":"Carbide Tooling","url":SITE,
             "potentialAction":{"@type":"SearchAction","target":SITE+"/?q={search}","query-input":"required name=search"}}
        ]
        if p["file"] != "index.html":
            ld.append({"@context":"https://schema.org","@type":"Article",
                       "headline":p["title"],"url":p["url"],"mainEntityOfPage":p["url"]})
        ld_html = '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>'
        content = content.replace("</head>", f"  {ld_html}\n</head>")
        changes.append("JSON-LD")

    # GA
    if GA_ID and f"gtag/js?id={GA_ID}" not in content:
        ga = f"""  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>"""
        content = content.replace("</head>", f"{ga}\n</head>")
        changes.append("GA")
    elif not GA_ID and "GOOGLE ANALYTICS" not in content:
        content = content.replace("</head>", "  <!-- GOOGLE ANALYTICS ID: 填入 GA ID 后启用 -->\n</head>")

    fpath.write_text(content, encoding="utf-8")
    print(f"✅ {p['file']}: {' + '.join(changes) if changes else '无改动'}")

# 4. 第一篇指南内容
guide_html = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>End Mill Geometry Guide — Carbide Tooling</title>
<meta name="description" content="Complete guide to end mill geometry: flute count, helix angle, corner radius, coatings, and how each affects cutting performance.">
<link rel="canonical" href="https://carbide-tooling.com/guides/end-mill-geometry.html">
<meta name="robots" content="index, follow">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,"SF Pro Display","Helvetica Neue",Arial,sans-serif;background:#fff;color:#1d1d1f;line-height:1.7;-webkit-font-smoothing:antialiased}
.container{max-width:700px;margin:0 auto;padding:0 22px}
nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.92);backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid #f0f0f0}
.nav-inner{display:flex;align-items:center;justify-content:space-between;height:48px;font-size:12px}
nav a{color:#1d1d1f;text-decoration:none;margin-left:28px;transition:color .2s}
nav a:hover{color:#06c}.logo{font-size:14px;font-weight:600}.logo span{color:#06c}
h1{font-size:36px;font-weight:700;letter-spacing:-0.5px;padding-top:80px;margin-bottom:16px;line-height:1.2}
.sub{font-size:14px;color:#86868b;margin-bottom:40px}
h2{font-size:24px;font-weight:600;margin:48px 0 12px;letter-spacing:-0.3px}
h3{font-size:18px;font-weight:600;margin:32px 0 8px}
p{font-size:16px;color:#333;margin-bottom:16px;line-height:1.7}
ul{padding-left:24px;margin-bottom:16px}
li{font-size:15px;color:#333;margin-bottom:6px}
.tip{background:#f5f5f7;border-radius:12px;padding:20px 24px;margin:24px 0;font-size:14px;color:#333}
footer{margin-top:80px;padding:32px 0;border-top:1px solid #f0f0f0;text-align:center;font-size:12px;color:#86868b}
@media(max-width:768px){h1{font-size:28px;padding-top:48px}}
</style>
</head>
<body>
<nav><div class="container nav-inner"><div class="logo"><span>◆</span> Carbide Tooling</div><div><a href="/">Home</a><a href="/guides/">Guides</a><a href="/about.html">About</a><a href="/quote.html">Quote</a></div></div></nav>
<div class="container">
<h1>End Mill Geometry Guide</h1>
<p class="sub">How flute count, helix angle, corner radius, and coating affect your machining results.</p>

<p>Choosing the right end mill geometry is one of the most impactful decisions you can make for both tool life and surface finish. This guide breaks down every variable so you can make informed choices.</p>

<h2>Flute Count</h2>
<p>Flute count determines chip evacuation, rigidity, and finish. More flutes = stronger core but less chip room.</p>
<ul>
<li><strong>2-flute:</strong> Best for aluminum and non-ferrous materials. Large gullets for chip evacuation. Ideal for slotting and plunging.</li>
<li><strong>3-flute:</strong> A compromise between 2 and 4. Good for aluminum with better finish than 2-flute. Less common but useful.</li>
<li><strong>4-flute:</strong> The most versatile. Strong core, good finish. Best for steel, stainless steel, and general-purpose milling.</li>
<li><strong>5/6-flute:</strong> High-performance for finishing. Excellent surface finish, but poor chip evacuation — never use for slotting.</li>
</ul>

<div class="tip"><strong>Rule of thumb:</strong> For aluminum use 2-3 flutes. For steel use 4 flutes. For finishing use 5-6 flutes. For titanium use variable helix.</div>

<h2>Helix Angle</h2>
<p>Helix angle affects cutting action, chip evacuation, and axial forces.</p>
<ul>
<li><strong>30° (Standard):</strong> Most common. Good balance of cutting action and tool strength. General-purpose.</li>
<li><strong>35-40° (High Helix):</strong> Smoother cutting action, better chip evacuation. Ideal for aluminum and non-ferrous. Higher axial load.</li>
<li><strong>45°+ (Ultra High Helix):</strong> Very aggressive cut, excellent for finishing. Weak core — not for heavy roughing.</li>
<li><strong>Variable Helix:</strong> Designed to reduce chatter and harmonics. Essential for hard metals and long-reach applications.</li>
</ul>

<h2>Corner Radius</h2>
<p>Also called corner chamfer or bull nose. The radius at the cutting edge where the bottom meets the side.</p>
<ul>
<li><strong>Sharp corner (0R):</strong> Maximum versatility — can cut square shoulders. Weakest point — chips easily.</li>
<li><strong>Small radius (0.5-2mm):</strong> Reinforces the cutting edge. Reduces chipping. Better tool life. Slightly higher cutting forces.</li>
<li><strong>Large radius (3mm+):</strong> Heavy roughing. Distributes cutting forces. Not suitable for sharp internal corners.</li>
</ul>

<h2>Coatings</h2>
<p>Coatings extend tool life by reducing heat and friction. Here are the most common types.</p>
<ul>
<li><strong>AlTiN (Aluminum Titanium Nitride):</strong> The most popular general-purpose coating. Good heat resistance (up to 800°C). Works well on steel and stainless.</li>
<li><strong>TiSiN (Titanium Silicon Nitride):</strong> Higher hardness than AlTiN. Excellent for hardened materials (HRC 45+). Good for dry machining.</li>
<li><strong>TiAlN (Titanium Aluminum Nitride):</strong> Similar to AlTiN but slightly lower aluminum content. Good for moderate temperatures.</li>
<li><strong>Uncoated:</strong> For aluminum and non-ferrous (coatings can cause built-up edge). Lower cost but shorter tool life.</li>
</ul>

<h2>Selecting the Right Tool</h2>
<p>Follow this decision flow when choosing an end mill for a new job:</p>
<ul>
<li><strong>Material:</strong> Determine workpiece material and hardness.</li>
<li><strong>Operation:</strong> Roughing, finishing, or both?</li>
<li><strong>Machine:</strong> Rigidity, spindle speed, and coolant capability.</li>
<li><strong>Geometry:</strong> Based on the tables above, select flute count, helix, and radius.</li>
<li><strong>Coating:</strong> Based on material and temperature.</li>
<li><strong>Supplier:</strong> We can help connect you with appropriate Chinese manufacturers.</li>
</ul>

<div class="tip"><strong>Need help selecting?</strong> Tell us your material, operation, and machine specs. We'll recommend the right tool geometry and connect you with a suitable factory. <a href="/quote.html" style="color:#06c;">Get a quote →</a></div>
</div>
<footer><div class="container"><p>© 2026 Carbide Tooling</p></div></footer>
</body>
</html>"""

guide_path = BASE / "guides" / "end-mill-geometry.html"
guide_path.write_text(guide_html, encoding="utf-8")
print("✅ 第一篇指南: end-mill-geometry.html")

# 更新 sitemap 加入新页面
PAGES.append({"file":"guides/end-mill-geometry.html","url":SITE+"/guides/end-mill-geometry.html","prio":"0.8","title":"End Mill Geometry Guide"})
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p in PAGES:
    xml += f'  <url><loc>{p["url"]}</loc><priority>{p["prio"]}</priority></url>\n'
xml += '</urlset>\n'
(BASE / "sitemap.xml").write_text(xml, encoding="utf-8")
print("✅ sitemap.xml 已更新")

print("\n=== 完毕 ===")
