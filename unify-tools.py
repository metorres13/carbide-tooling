#!/usr/bin/env python3
"""
Carbide-Tooling.com — Apple UI Unification & B2B Conversion Loop
Applies to all 101 tool pages under /tools/<name>/

CRITICAL: Preserves all existing content (SEO, FAQ, Toolbox, calculator JS).
Only adds new sections and upgrades existing ones.
"""

import os, re, json, random, html

ROOT = os.path.dirname(__file__)
TOOLS_DIR = os.path.join(ROOT, "tools")
CSS_HREF = "/css/tool-style.css"

FAVICON_SVG = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%230066cc'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-size='18' font-weight='800' fill='%23fff'%3E◆%3C/text%3E%3C/svg%3E"


# ── Tool name mapping ──
FRIENDLY = {
    "aluminum-alloy-table": "Aluminum Alloy Table",
    "aql-sampling-calculator": "AQL Sampling Calculator",
    "arc-r-to-ij-converter": "Arc R to IJ Converter",
    "automation-vs-manual-calculator": "Automation vs Manual",
    "ball-nose-effective-diameter": "Ball Nose Effective Diameter",
    "batch-cost-calculator": "Batch Cost Calculator",
    "blind-hole-tapping-calculator": "Blind Hole Tapping Calculator",
    "bolt-circle-calculator": "Bolt Circle Calculator",
    "brass-machining-parameters": "Brass Machining Parameters",
    "bulk-discount-calculator": "Bulk Discount Calculator",
    "carbide-grade-cross-ref-2": "Carbide Grade Cross Reference",
    "cast-iron-machining": "Cast Iron Machining Calculator",
    "chamfer-calculator": "Chamfer Calculator",
    "chip-load": "Chip Load Calculator",
    "cnc-roi-calculator": "CNC ROI Calculator",
    "coating-selector": "Coating Selector",
    "coolant-concentration": "Coolant Concentration Calculator",
    "coolant-lifecycle-cost": "Coolant Lifecycle Cost",
    "coord-rotation-calculator": "Coordinate Rotation Calculator",
    "cost-per-part-calculator": "Cost Per Part Calculator",
    "countersink-depth-calculator": "Countersink Depth Calculator",
    "cycle-time-calculator": "Cycle Time Calculator",
    "dia-circ-calculator": "Diameter & Circumference Calculator",
    "die-steel-thermal-conductivity": "Die Steel Thermal Conductivity",
    "dovetail-calculator": "Dovetail Calculator",
    "drill-point-length-calculator": "Drill Point Length Calculator",
    "engineering-interest-calculator": "Engineering Interest Calculator",
    "feed-converter": "Feed Converter",
    "feed-rate-override-calculator": "Feed Rate Override Calculator",
    "flatness-calculator": "Flatness Calculator",
    "force-calculator": "Force Calculator",
    "form-tap-drill-calculator": "Form Tap Drill Calculator",
    "gcode-reference": "G-Code Reference",
    "gdt-symbols-reference": "GD&T Symbols Reference",
    "gear-parameter-calculator": "Gear Parameter Calculator",
    "grade-reference": "Grade Reference",
    "graphite-machining": "Graphite Machining Calculator",
    "gun-drill-calculator": "Gun Drill Calculator",
    "hardness-converter": "Hardness Converter",
    "heat-expansion-calculator": "Heat Expansion Calculator",
    "helical-interpolation-calculator": "Helical Interpolation Calculator",
    "horsepower-calculator": "Horsepower Calculator",
    "inventory-turnover-calculator": "Inventory Turnover Calculator",
    "iso-fit-calculator": "ISO Fit Calculator",
    "keyway-depth-calculator": "Keyway Depth Calculator",
    "machinability-rating": "Machinability Rating",
    "machine-power-calculator": "Machine Power Calculator",
    "mcode-reference": "M-Code Reference",
    "metal-cost-calculator": "Metal Cost Calculator",
    "metal-weight-calculator": "Metal Weight Calculator",
    "metric-imperial-thread-converter": "Metric/Imperial Thread Converter",
    "micron-inch-converter": "Micron to Inch Converter",
    "mrr-calculator": "MRR Calculator",
    "nose-radius-compensation": "Nose Radius Compensation",
    "npt-pipe-thread-calculator": "NPT Pipe Thread Calculator",
    "peck-drilling-calculator": "Peck Drilling Calculator",
    "percentage-of-thread-calculator": "Thread Percentage Calculator",
    "plastic-machining": "Plastic Machining Guide",
    "polar-rect-converter": "Polar to Rectangular Converter",
    "pomodoro-timer": "Pomodoro Timer",
    "pressure-converter": "Pressure Converter",
    "production-efficiency-calculator": "Production Efficiency Calculator",
    "pythagorean-calculator": "Pythagorean Calculator",
    "ramping-angle-calculator": "Ramping Angle Calculator",
    "reaming-allowance-calculator": "Reaming Allowance Calculator",
    "round-bar-weight": "Round Bar Weight Calculator",
    "scrap-value-calculator": "Scrap Value Calculator",
    "sfm-m-min-converter": "SFM to m/min Converter",
    "shipping-duty-estimator": "Shipping Duty Estimator",
    "sine-bar-calculator": "Sine Bar Calculator",
    "slot-milling-calculator": "Slot Milling Calculator",
    "speed-feed": "Speed & Feed Calculator",
    "stainless-properties": "Stainless Steel Properties",
    "step-drill-design-calculator": "Step Drill Design Calculator",
    "step-milling-calculator": "Step Milling Calculator",
    "superalloy-tool-life": "Superalloy Tool Life Estimator",
    "surface-roughness-calculator": "Surface Roughness Calculator",
    "surface-speed": "Surface Speed (SFM) Calculator",
    "tangent-point-calculator": "Tangent Point Calculator",
    "tap-drill-size-calculator": "Tap Drill Size Calculator",
    "taper-calculator": "Taper Calculator",
    "tapping-feed-rate-calculator": "Tapping Feed Rate Calculator",
    "temp-converter": "Temperature Converter",
    "tensile-strength-converter": "Tensile Strength Converter",
    "thread-depth-torque-calculator": "Thread Depth & Torque Calculator",
    "thread-lead-angle-calculator": "Thread Lead Angle Calculator",
    "thread-pitch-diameter-calculator": "Thread Pitch Diameter Calculator",
    "threading-pass-calculator": "Threading Pass Calculator",
    "titanium-machining-guide": "Titanium Machining Guide",
    "tool-change-time-analyzer": "Tool Change Time Analyzer",
    "tool-life-economics": "Tool Life Economics",
    "tool-runout-calculator": "Tool Runout Calculator",
    "tool-steel-heat-treat": "Tool Steel Heat Treat Calculator",
    "tool-wear-cost-calculator": "Tool Wear Cost Calculator",
    "toolbox-organizer": "Toolbox Organizer",
    "torque-unit-converter": "Torque Unit Converter",
    "trochoidal-milling-calculator": "Trochoidal Milling Calculator",
    "tube-weight-calculator": "Tube Weight Calculator",
    "ultimate-unit-converter": "Ultimate Unit Converter",
    "wall-thickness-calculator": "Wall Thickness Calculator",
    "weight-shipping-calculator": "Weight & Shipping Calculator",
}


def friendly_name(name):
    return FRIENDLY.get(name, name.replace("-", " ").title())


def tool_category(name):
    milling = r'mill|speed|feed|chip|surface|roughness|trochoidal|slot|step|ball|helical|runout|mr|horsepower|force|cycle|nose|ramp'
    drilling = r'tap|drill|thread|countersink|ream|gun|npt|pitch|lead|form'
    grade = r'grade|hardness|machinability|coating|tensile|stainless|titanium|aluminum|cast|plastic|graphite|brass|superalloy|steel'
    turning = r'lathe|turn'
    if re.search(turning, name, re.I): return "turning"
    if re.search(milling, name, re.I): return "milling"
    if re.search(drilling, name, re.I): return "drilling"
    if re.search(grade, name, re.I): return "grade"
    return "general"


def product_anchors_html(name):
    cat = tool_category(name)
    links = {
        "milling": [("/products/end-mills.html", "Solid Carbide End Mills"), ("/products/tool-holders.html", "Tool Holders")],
        "drilling": [("/products/drills.html", "Carbide Drills"), ("/products/threading-tools.html", "Thread Mills & Taps")],
        "turning": [("/products/turning-inserts.html", "Turning Inserts"), ("/products/tool-holders.html", "Tool Holders")],
        "grade": [("/products/carbide-grades.html", "Grade Selection Guide"), ("/guides/insert-grade-selection.html", "Insert Grade Inquiry")],
        "general": [("/products/end-mills.html", "Solid Carbide End Mills"), ("/products/turning-inserts.html", "Turning Inserts")],
    }
    items = links.get(cat, links["general"])
    parts = ['<span>🔗 Recommended:</span>']
    for href, label in items:
        parts.append(f'<a href="{href}">{label}</a>')
    return ''.join(parts)


def extract_faq_qas(html_content):
    """Extract FAQ Q&A pairs from existing content"""
    faqs = []
    m = re.search(r'<h2>Frequently Asked Questions</h2>(.*?)(?:</section>|<h2>|$)', html_content, re.DOTALL)
    if m:
        section = m.group(1)
        pairs = re.findall(r'<strong>(.*?)</strong>\s*(.*?)(?=<strong>|$)', section, re.DOTALL)
        for q, a in pairs:
            q = re.sub(r'<[^>]+>', '', q).strip()
            a = re.sub(r'<[^>]+>', '', a).strip()
            if q and a and len(q) > 5 and len(a) > 10:
                faqs.append((q, a))
    return faqs


def extract_desc(html_content):
    m = re.search(r'<meta name="description" content="([^"]*)"', html_content)
    return m.group(1) if m else ""


def generate_json_ld(tool_name, friendly_name, desc, faq_qas):
    url = f"https://carbide-tooling.com/tools/{tool_name}/"
    faq_items = []
    for q, a in faq_qas[:5]:
        faq_items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "SoftwareApplication", "name": friendly_name, "url": url,
             "applicationCategory": "EngineeringApplication", "operatingSystem": "Web",
             "description": desc or f"{friendly_name} for CNC machining",
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
            {"@type": "WebPage", "url": url, "name": friendly_name, "description": desc or f"{friendly_name} for CNC machining",
             "isPartOf": {"@type": "WebSite", "url": "https://carbide-tooling.com/"}}
        ]
    }
    if faq_items:
        schema["@graph"].append({"@type": "FAQPage", "mainEntity": faq_items})
    return json.dumps(schema, ensure_ascii=False, indent=2)


def process_tool(tool_name):
    fpath = os.path.join(TOOLS_DIR, tool_name, "index.html")
    if not os.path.isfile(fpath):
        return False, "File not found"
    
    with open(fpath, "r") as f:
        content = f.read()
    
    friendly = friendly_name(tool_name)
    desc = extract_desc(content)
    faqs = extract_faq_qas(content)
    json_ld = generate_json_ld(tool_name, friendly, desc, faqs)
    url_path = f"https://carbide-tooling.com/tools/{tool_name}/"
    
    # ═══════════════════════════════════════
    # 1. HEAD: Inject CSS, OG, favicon, theme-color, JSON-LD, update title
    # ═══════════════════════════════════════
    
    head_additions = f"""
<link rel="stylesheet" href="{CSS_HREF}"/>
<meta name="theme-color" content="#0066cc"/>
<link rel="icon" type="image/svg+xml" href="{FAVICON_SVG}"/>
<meta property="og:title" content="{friendly} | Precision Machining Tool"/>
<meta property="og:description" content="{html.escape(desc[:150])}"/>
<meta property="og:url" content="{url_path}"/>
<meta property="og:type" content="website"/>
<meta property="og:locale" content="en_US"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="{friendly} | Precision Machining Tool"/>
<script type="application/ld+json">
{json_ld}
</script>"""
    
    content = content.replace("</head>", head_additions + "\n</head>", 1)
    
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        new_title = f"{friendly} | Precision Machining Tool | Carbide-Tooling.com"
        content = content.replace(title_match.group(0), f"<title>{new_title}</title>", 1)
    
    # ═══════════════════════════════════════
    # 2. EXTRACT and REMOVE SEO section from inside footer (if present)
    # ═══════════════════════════════════════
    
    seo_html = ""
    seo_section_match = re.search(r'<section class="seo">.*?</section>', content, re.DOTALL)
    if seo_section_match:
        seo_html = seo_section_match.group(0)
        # Remove SEO section from wherever it is (likely inside footer)
        content = content.replace(seo_html, "", 1)
    
    # Also extract the toolbox div (the Precision Engineering Toolbox)
    toolbox_html = ""
    toolbox_match = re.search(r'<div style="padding:24px 0;margin:32px 0;border-top:1px solid #e8e8ed;border-bottom:1px solid #e8e8ed">.*?</div>', content, re.DOTALL)
    if not toolbox_match:
        toolbox_match = re.search(r'<div[^>]*class="[^"]*toolbox[^"]*"[^>]*>.*?</div>', content, re.DOTALL)
    if toolbox_match:
        toolbox_html = toolbox_match.group(0)
        content = content.replace(toolbox_html, "", 1)
    
    # Also extract the B2B line (High-Performance Series) if it's separate
    b2b_line = ""
    b2b_match = re.search(r'<p[^>]*style="[^"]*text-align:center[^"]*"[^>]*>⚡ Calculated for Carbide-Tooling\.com High-Performance Series.*?</p>', content, re.DOTALL)
    if b2b_match:
        b2b_line = b2b_match.group(0)
        content = content.replace(b2b_line, "", 1)
    
    # Also extract the "All Tools" link that's before the toolbox
    all_tools_match = re.search(r'<p style="margin-bottom:4px"><a href="/tools/" style="color:#0066cc">All Tools</a></p>\s*<p style="font-size:11px;margin-bottom:6px">[^<]*</p>\s*<p style="font-size:11px">[^<]*</p>', content, re.DOTALL)
    
    # ═══════════════════════════════════════
    # 3. Extract and upgrade the footer
    # ═══════════════════════════════════════
    
    footer_match = re.search(r'<footer.*?</footer>', content, re.DOTALL)
    if footer_match:
        old_footer = footer_match.group(0)
        
        # Extract copyright text from old footer
        cr_match = re.search(r'© 2026 Carbide Tooling', old_footer)
        copyright_text = cr_match.group(0) if cr_match else '© 2026 Carbide Tooling'
        
        new_footer = f"""<footer class="tool-footer">
<div class="container">
  <div class="footer-links">
    <a href="/">Home</a>
    <a href="/tools/">All Tools</a>
    <a href="/products/">Products</a>
    <a href="/guides/">Guides</a>
    <a href="/about.html">About</a>
    <a href="/quote.html">Get a Quote</a>
    <a href="/privacy.html">Privacy</a>
  </div>
  <div class="footer-social">
    <a href="https://www.linkedin.com/company/carbide-tooling" target="_blank" rel="noopener" aria-label="LinkedIn">in</a>
    <a href="https://twitter.com/carbidetooling" target="_blank" rel="noopener" aria-label="X (Twitter)">𝕏</a>
    <a href="mailto:sales@carbide-tooling.com" aria-label="Email">✉</a>
  </div>
  <p style="margin-bottom:4px"><a href="/tools/" style="color:#0066cc">All Tools</a></p>
  <p style="font-size:11px;margin-bottom:6px">Results are for reference only. Consult tool manufacturers for specific applications.</p>
  <p style="font-size:11px">{copyright_text}</p>
</div>
</footer>"""
        
        content = content.replace(old_footer, new_footer, 1)
    
    # ═══════════════════════════════════════
    # 4. Inject new sections in order before </body>
    #    Order: SEO content (preserved) → B2B line → Toolbox → B2B card → Product links → More tools → Share bar
    # ═══════════════════════════════════════
    
    # Build new content blocks
    new_b2b_card = """
<aside class="b2b-card">
  <div class="b2b-icon">📦</div>
  <div class="b2b-body">
    <h3>Need Professional Tooling?</h3>
    <p>Get factory-direct pricing, engineered carbide grades, and responsive technical support — all from one source.</p>
  </div>
  <a href="/quote.html" class="b2b-btn">Request Bulk Quote →</a>
</aside>"""
    
    new_product_anchors = f"""<div class="product-links">{product_anchors_html(tool_name)}</div>"""
    
    new_share_bar = f"""<div class="share-bar">
  <span class="share-label">↗ Share with Engineers</span>
  <a href="https://www.linkedin.com/shareArticle?mini=true&url={url_path}" target="_blank" rel="noopener">LinkedIn</a>
  <a href="https://twitter.com/intent/tweet?url={url_path}&text={friendly}" target="_blank" rel="noopener">𝕏</a>
  <a href="mailto:subject={friendly}&body=Check this out: {url_path}">Email</a>
</div>"""
    
    # More tools: 8 random from different categories
    all_tools_list = [d for d in sorted(os.listdir(TOOLS_DIR)) if d != "index.html" and os.path.isdir(os.path.join(TOOLS_DIR, d))]
    candidates = [t for t in all_tools_list if t != tool_name]
    random.shuffle(candidates)
    selected = candidates[:8]
    more_links = ""
    for t in selected:
        fn = friendly_name(t)
        more_links += f'<a href="/tools/{t}/">{fn}</a>\n'
    
    new_more_tools = f"""<section class="more-tools">
  <h3>🔧 Explore 100+ Professional Machining Tools</h3>
  <div class="tool-grid">
{more_links}
  </div>
</section>"""
    
    # Assemble the post-calculator content block
    post_content = ""
    
    # Wrap preserved SEO in modern wrapper if it existed
    if seo_html:
        # Replace old class with new
        seo_updated = seo_html.replace('class="seo"', 'class="seo-content"')
        post_content += seo_updated + "\n"
    
    # Add preserved B2B line if it existed (before toolbox)
    if b2b_line:
        post_content += b2b_line + "\n"
    
    # Add preserved toolbox if existed
    if toolbox_html:
        # Wrap in a modern class
        toolbox_updated = toolbox_html.replace(
            'style="padding:24px 0;margin:32px 0;border-top:1px solid #e8e8ed;border-bottom:1px solid #e8e8ed"',
            'class="toolbox-widget"'
        )
        post_content += toolbox_updated + "\n"
    else:
        # Add a minimal toolbox if none existed
        post_content += """<div class="toolbox-widget"><h3>🔧 Precision Engineering Toolbox</h3><div class="toolbox-links">
<a href="/tools/speed-feed/">Speed & Feed</a>
<a href="/tools/hardness-converter/">Hardness Converter</a>
<a href="/tools/tap-drill-size-calculator/">Tap Drill Size</a>
<a href="/tools/mrr-calculator/">MRR Calculator</a>
<a href="/tools/feed-converter/">Feed Converter</a>
<a href="/tools/surface-roughness-calculator/">Surface Roughness</a>
<a href="/tools/titanium-machining-guide/">Titanium Guide</a>
<a href="/tools/carbide-grade-cross-ref-2/">Grade Cross Ref</a>
<a href="/tools/cost-per-part-calculator/">Cost Per Part</a>
<a href="/tools/torque-unit-converter/">Torque Converter</a>
</div></div>\n"""
    
    # Add B2B card
    post_content += new_b2b_card + "\n"
    
    # Add product anchors
    post_content += new_product_anchors + "\n"
    
    # Add more tools
    post_content += new_more_tools + "\n"
    
    # Add share bar
    post_content += new_share_bar + "\n"
    
    # Insert post_content before </body>
    content = content.replace("</body>", post_content + "\n</body>", 1)
    
    # ═══════════════════════════════════════
    # 5. Clean up double blank lines
    # ═══════════════════════════════════════
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    with open(fpath, "w") as f:
        f.write(content)
    
    return True, "OK"


def main():
    all_tools = sorted(d for d in os.listdir(TOOLS_DIR) if d != "index.html" and os.path.isdir(os.path.join(TOOLS_DIR, d)))
    print(f"Found {len(all_tools)} tool directories\n")
    
    success = 0
    errors = []
    
    for tool_name in all_tools:
        ok, msg = process_tool(tool_name)
        if ok:
            success += 1
            print(f"  ✅ {tool_name}")
        else:
            errors.append((tool_name, msg))
            print(f"  ❌ {tool_name}: {msg}")
    
    print(f"\n{'='*50}")
    print(f"Results: {success} updated, {len(errors)} errors")
    if errors:
        for name, err in errors:
            print(f"  {name}: {err}")
    return 0


if __name__ == "__main__":
    main()
