#!/usr/bin/env python3
"""
Fixup script for localization issues:
1. Fix duplicate lang attributes
2. Translate FAQ titles
3. Translate common phrases properly
4. Generate multilingual sitemaps
5. Create language switcher in footer
6. Add hreflang to remaining pages
"""

import os, re, glob

ROOT = os.path.dirname(__file__)
LANG_DIRS = ["de", "jp", "es", "vi", "zh"]

# ── More translation mappings ──
EXTRA_TRANSLATIONS = {
    "de": {
        "Frequently Asked Questions": "Häufig gestellte Fragen",
        "FAQ": "FAQ",
        "Calculator": "Rechner",
        "Input": "Eingabe",
        "Output": "Ausgabe", 
        "Result": "Ergebnis",
        "Calculate": "Berechnen",
        "Reset": "Zurücksetzen",
        "All Tools": "Alle Werkzeuge",
        "Speed & Feed": "Schnittgeschwindigkeit & Vorschub",
        "Chip Load": "Spanbelastung",
        "Surface Speed": "Schnittgeschwindigkeit",
        "Home": "Startseite",
        "Products": "Produkte",
        "About": "Über uns",
        "Guides": "Leitfäden",
        "Get a Quote": "Angebot anfordern",
        "Privacy": "Datenschutz",
        "Carbide Tooling": "Carbide Tooling",
        "Results are for reference only": "Ergebnisse dienen nur zur Referenz",
        "Consult tool manufacturers for specific applications": "Konsultieren Sie Werkzeughersteller für spezifische Anwendungen",
        "RPM": "U/min", "SFM": "m/min",
    },
    "jp": {
        "Frequently Asked Questions": "よくある質問",
        "FAQ": "FAQ",
        "Calculator": "計算機",
        "Input": "入力",
        "Output": "出力",
        "Result": "結果",
        "Calculate": "計算",
        "Reset": "リセット",
        "All Tools": "全ツール",
        "Speed & Feed": "切削速度と送り",
        "Home": "ホーム",
        "Products": "製品",
        "About": "会社概要",
        "Guides": "ガイド",
        "Get a Quote": "見積もり",
        "Privacy": "プライバシー",
        "Carbide Tooling": "Carbide Tooling",
        "Results are for reference only": "結果は参考値です",
        "Consult tool manufacturers for specific applications": "具体的な用途については工具メーカーにご相談ください",
        "RPM": "rpm", "SFM": "m/min",
    },
    "es": {
        "Frequently Asked Questions": "Preguntas frecuentes",
        "FAQ": "FAQ",
        "Calculator": "Calculadora",
        "Input": "Entrada",
        "Output": "Salida",
        "Result": "Resultado",
        "Calculate": "Calcular",
        "Reset": "Reiniciar",
        "All Tools": "Todas las herramientas",
        "Speed & Feed": "Velocidad y avance",
        "Home": "Inicio",
        "Products": "Productos",
        "About": "Nosotros",
        "Guides": "Guías",
        "Get a Quote": "Cotizar",
        "Privacy": "Privacidad",
        "Carbide Tooling": "Carbide Tooling",
        "Results are for reference only": "Los resultados son solo de referencia",
        "Consult tool manufacturers for specific applications": "Consulte a los fabricantes para aplicaciones específicas",
        "RPM": "RPM", "SFM": "m/min",
    },
    "vi": {
        "Frequently Asked Questions": "Câu hỏi thường gặp",
        "FAQ": "FAQ",
        "Calculator": "Máy tính",
        "Input": "Đầu vào",
        "Output": "Đầu ra",
        "Result": "Kết quả",
        "Calculate": "Tính",
        "Reset": "Đặt lại",
        "All Tools": "Tất cả công cụ",
        "Speed & Feed": "Tốc độ & lượng chạy dao",
        "Home": "Trang chủ",
        "Products": "Sản phẩm",
        "About": "Về chúng tôi",
        "Guides": "Hướng dẫn",
        "Get a Quote": "Báo giá",
        "Privacy": "Quyền riêng tư",
        "Carbide Tooling": "Carbide Tooling",
        "Results are for reference only": "Kết quả chỉ mang tính tham khảo",
        "Consult tool manufacturers for specific applications": "Tham khảo nhà sản xuất dụng cụ",
        "RPM": "v/ph", "SFM": "m/phút",
    },
    "zh": {
        "Frequently Asked Questions": "常见问题解答",
        "FAQ": "常见问题",
        "Calculator": "计算器",
        "Input": "输入",
        "Output": "输出",
        "Result": "结果",
        "Calculate": "计算",
        "Reset": "重置",
        "All Tools": "所有工具",
        "Speed & Feed": "速度与进给",
        "Home": "首页",
        "Products": "产品",
        "About": "关于我们",
        "Guides": "指南",
        "Get a Quote": "获取报价",
        "Privacy": "隐私政策",
        "Carbide Tooling": "Carbide Tooling",
        "Results are for reference only": "结果仅供参考",
        "Consult tool manufacturers for specific applications": "具体应用请咨询刀具制造商",
        "RPM": "转/分", "SFM": "米/分",
    }
}


def fix_lang_attr(filepath):
    """Fix duplicate lang attributes"""
    with open(filepath) as f: content = f.read()
    # Remove the old lang="en" if present when adding new lang
    content = re.sub(r'<html\s+lang="([a-z]+)"\s+lang="([a-z]+)"', r'<html lang="\1"', content)
    content = re.sub(r'<html\s+lang="en"\s+lang="', r'<html lang="', content)
    with open(filepath, "w") as f: f.write(content)


def fixup_tool(filepath, lang):
    """Fix translation issues in a tool file"""
    with open(filepath) as f: content = f.read()
    orig = content
    
    # Fix html lang attribute
    content = re.sub(r'<html\s+lang="en"', '<html', content)
    lang_map = {"de": "de", "jp": "ja", "es": "es", "vi": "vi", "zh": "zh"}
    if f'lang="{lang_map[lang]}"' not in content:
        content = content.replace("<html", f'<html lang="{lang_map[lang]}"')
    
    # Remove duplicate lang attributes
    content = re.sub(r'lang="([a-z]+)"\s+lang="([a-z]+)"', r'lang="\1"', content)
    
    # Apply extra translations
    extra = EXTRA_TRANSLATIONS.get(lang, {})
    for eng, loc in sorted(extra.items(), key=lambda x: -len(x[0])):
        content = content.replace(eng, loc)
    
    # Fix doubled "Carbide Tooling Carbide Tooling"
    content = re.sub(r'Carbide Tooling\s+Carbide Tooling', 'Carbide Tooling', content)
    
    if content != orig:
        with open(filepath, "w") as f: f.write(content)
        return True
    return False


def add_language_switcher(filepath, lang, tool_name=""):
    """Add language switcher to the footer of tool pages"""
    with open(filepath) as f: content = f.read()
    
    # Build language switcher HTML
    lang_codes = {"de": "DE", "jp": "JP", "es": "ES", "vi": "VI", "zh": "中", "en": "EN"}
    lang_full = {"de": "Deutsch", "jp": "日本語", "es": "Español", "vi": "Tiếng Việt", "zh": "中文", "en": "English"}
    
    # Only add to tool pages (with footer)
    if '</footer>' not in content:
        return False
    
    # Build switcher
    current_lang = lang if lang != "en" else "en"
    base_url = f"https://carbide-tooling.com"
    
    switcher_html = '\n<div class="lang-switcher">\n  <span class="lang-label">🌐</span>\n'
    for lc in ["en", "de", "jp", "es", "vi", "zh"]:
        active = " active" if lc == current_lang else ""
        if lc == "en":
            href = f"{base_url}/tools/{tool_name}/" if tool_name else f"{base_url}/"
        else:
            href = f"{base_url}/{lc}/tools/{tool_name}/" if tool_name else f"{base_url}/{lc}/"
        label = lang_codes.get(lc, lc)
        switcher_html += f'  <a href="{href}" class="lang-link{active}">{label}</a>\n'
    switcher_html += '</div>\n'
    
    # Check if already has lang-switcher HTML element
    if 'class="lang-link"' in content or 'class="lang-switcher"' in content:
        return False
    
    # Insert before </footer>
    content = content.replace('</footer>', switcher_html + '</footer>')
    
    # Add CSS for language switcher if not present
    lang_css = '.lang-switcher{display:flex;align-items:center;justify-content:center;gap:6px;padding:8px 0;margin:8px 0;border-top:1px solid #e8e8ed;font-size:11px}.lang-switcher .lang-label{font-size:13px;margin-right:4px}.lang-switcher .lang-link{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:#fff;border:1px solid #e8e8ed;color:#86868b;text-decoration:none;font-size:10px;font-weight:600;transition:all .15s}.lang-switcher .lang-link:hover{background:#0066cc;color:#fff;border-color:#0066cc}.lang-switcher .lang-link.active{background:#0066cc;color:#fff;border-color:#0066cc}'
    if lang_css not in content:
        content = content.replace('</style>', lang_css + '\n</style>')
    
    with open(filepath, "w") as f: f.write(content)
    return True


def generate_sitemaps():
    """Generate multilingual sitemaps"""
    tool_dirs = sorted(d for d in os.listdir(os.path.join(ROOT, "tools")) 
                      if d != "index.html" and os.path.isdir(os.path.join(ROOT, "tools", d)))
    
    # Generate separate sitemap for each language
    for lang_code, hreflang_code in [("en","en"), ("de","de"), ("jp","ja"), ("es","es"), ("vi","vi"), ("zh","zh")]:
        urls = []
        
        # Main pages
        if lang_code == "en":
            urls.append(("https://carbide-tooling.com/", "1.0"))
            urls.append(("https://carbide-tooling.com/tools/", "0.9"))
            urls.append(("https://carbide-tooling.com/about.html", "0.5"))
            urls.append(("https://carbide-tooling.com/quote.html", "0.6"))
            for pf in sorted(os.listdir(os.path.join(ROOT, "products"))):
                if pf.endswith(".html"):
                    urls.append((f"https://carbide-tooling.com/products/{pf}", "0.6"))
            for gf in sorted(os.listdir(os.path.join(ROOT, "guides"))):
                if gf.endswith(".html"):
                    urls.append((f"https://carbide-tooling.com/guides/{gf}", "0.6"))
            for td in tool_dirs:
                urls.append((f"https://carbide-tooling.com/tools/{td}/", "0.8"))
        else:
            prefix = f"https://carbide-tooling.com/{lang_code}"
            urls.append((f"{prefix}/", "0.9"))
            urls.append((f"{prefix}/tools/", "0.8"))
            urls.append((f"{prefix}/about.html", "0.5"))
            urls.append((f"{prefix}/quote.html", "0.6"))
            for td in tool_dirs:
                urls.append((f"{prefix}/tools/{td}/", "0.8"))
        
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        xml += '  xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        
        for url, prio in urls:
            xml += "  <url>\n"
            xml += f'    <loc>{url}</loc>\n'
            xml += f'    <priority>{prio}</priority>\n'
            # Add xhtml:link for hreflang
            for lc, hf in [("en","en"), ("de","de"), ("jp","ja"), ("es","es"), ("vi","vi"), ("zh","zh")]:
                if lc == "en":
                    alt_url = url.replace(f"/{lang_code}/", "/").replace("https://carbide-tooling.com//", "https://carbide-tooling.com/")
                    if f"/{lang_code}/" not in url and lang_code != "en":
                        alt_url = url
                else:
                    if lang_code == "en":
                        alt_url = url.replace("https://carbide-tooling.com/", f"https://carbide-tooling.com/{lc}/")
                    else:
                        alt_url = url.replace(f"/{lang_code}/", f"/{lc}/")
                xml += f'    <xhtml:link rel="alternate" hreflang="{hf}" href="{alt_url}"/>\n'
            xml += "  </url>\n"
        
        xml += '</urlset>\n'
        
        fname = f"sitemap-{lang_code}.xml" if lang_code != "en" else "sitemap.xml"
        with open(os.path.join(ROOT, fname), "w") as f:
            f.write(xml)
        print(f"  Generated {fname} ({len(urls)} URLs)")
    
    # Generate sitemap index
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for lang_code in ["en", "de", "jp", "es", "vi", "zh"]:
        fname = f"sitemap-{lang_code}.xml" if lang_code != "en" else "sitemap.xml"
        xml += f'  <sitemap>\n    <loc>https://carbide-tooling.com/{fname}</loc>\n  </sitemap>\n'
    xml += '</sitemapindex>\n'
    with open(os.path.join(ROOT, "sitemap-index.xml"), "w") as f:
        f.write(xml)
    print("  Generated sitemap-index.xml")


def create_lang_homepages():
    """Create minimal language-specific homepages"""
    for lang in LANG_DIRS:
        lang_name = {"de": "Deutsch", "jp": "日本語", "es": "Español", "vi": "Tiếng Việt", "zh": "中文"}[lang]
        
        html = f'''<!DOCTYPE html><html lang="{lang}">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Carbide Tooling — {lang_name}</title>
<meta name="description" content="Carbide Tooling — CNC Zerspanungswerkzeuge in Präzisionsqualität."/>
<link rel="canonical" href="https://carbide-tooling.com/{lang}/"/>
<link rel="stylesheet" href="/css/tool-style.css"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700;14..32,800;14..32,900&display=swap" rel="stylesheet"/>
<meta name="theme-color" content="#0066cc"/>
<link rel="alternate" hreflang="en" href="https://carbide-tooling.com/"/>
<link rel="alternate" hreflang="de" href="https://carbide-tooling.com/de/"/>
<link rel="alternate" hreflang="ja" href="https://carbide-tooling.com/jp/"/>
<link rel="alternate" hreflang="es" href="https://carbide-tooling.com/es/"/>
<link rel="alternate" hreflang="vi" href="https://carbide-tooling.com/vi/"/>
<link rel="alternate" hreflang="zh" href="https://carbide-tooling.com/zh/"/>
<style>body{{font-family:'Inter',sans-serif;padding:40px 24px;text-align:center}}h1{{font-size:28px;font-weight:800}}nav{{height:44px;background:rgba(255,255,255,.96);backdrop-filter:blur(24px);border-bottom:1px solid rgba(0,0,0,.06);display:flex;align-items:center;justify-content:center;gap:20px;position:sticky;top:0;z-index:100;margin:-40px -24px 32px;padding:0 24px}}nav a{{font-size:12px;color:#1d1d1f;text-decoration:none;font-weight:500}}nav a:hover{{color:#0066cc}}.tools{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;max-width:800px;margin:24px auto;text-align:left}}a{{color:#0066cc;text-decoration:none;font-size:13px;padding:6px 10px;border-radius:8px;background:#f5f5f7;display:block}}a:hover{{background:#e8f0fe}}.lang-bar{{display:flex;justify-content:center;gap:8px;margin:20px 0}}.lang-bar a{{display:inline-flex;width:32px;height:32px;border-radius:50%;align-items:center;justify-content:center;font-size:11px;font-weight:600;padding:0}}.lang-bar a.active{{background:#0066cc;color:#fff}}footer{{margin-top:40px;font-size:11px;color:#86868b}}
</style></head><body>
<nav><a href="/{lang}/">Home</a><a href="/{lang}/tools/">Werkzeuge</a><a href="/products/">Produkte</a><a href="/about.html">Über uns</a><a href="/quote.html" style="background:#0066cc;color:#fff;padding:6px 16px;border-radius:20px">Angebot</a></nav>
<h1>Carbide Tooling — <span style="color:#0066cc">{lang_name}</span></h1>
<p style="color:#86868b;max-width:500px;margin:8px auto 24px">Präzisions-Zerspanungswerkzeuge und kostenlose CNC-Rechner.</p>
<div class="lang-bar"><a href="/">EN</a><a href="/de/" class="active">DE</a><a href="/jp/">JP</a><a href="/es/">ES</a><a href="/vi/">VI</a><a href="/zh/">中</a></div>
<div class="tools">'''
        
        # List tools
        tool_dirs = sorted(d for d in os.listdir(os.path.join(ROOT, "tools")) 
                          if d != "index.html" and os.path.isdir(os.path.join(ROOT, "tools", d)))
        for td in tool_dirs[:50]:
            name = td.replace("-", " ").title()
            html += f'<a href="/{lang}/tools/{td}/">{name}</a>\n'
        
        html += '''</div>
<footer><p style="font-size:11px;color:#86868b">© 2026 Carbide Tooling</p></footer>
</body></html>'''
        
        fpath = os.path.join(ROOT, lang, "index.html")
        with open(fpath, "w") as f:
            f.write(html)
        print(f"  Created {lang}/index.html")


def main():
    print("=== Fixup Phase 1: Fix lang attributes & translations ===")
    count = 0
    for lang in LANG_DIRS:
        tools_dir = os.path.join(ROOT, lang, "tools")
        for td in os.listdir(tools_dir):
            if td == "index.html": continue
            fpath = os.path.join(tools_dir, td, "index.html")
            if os.path.isfile(fpath):
                if fixup_tool(fpath, lang):
                    count += 1
    print(f"  Fixed {count} files")
    
    print("\n=== Fixup Phase 2: Add language switcher ===")
    count = 0
    for lang in LANG_DIRS:
        tools_dir = os.path.join(ROOT, lang, "tools")
        for td in os.listdir(tools_dir):
            if td == "index.html": continue
            fpath = os.path.join(tools_dir, td, "index.html")
            if os.path.isfile(fpath):
                if add_language_switcher(fpath, lang, td):
                    count += 1
    # Also add to English tools
    for td in os.listdir(os.path.join(ROOT, "tools")):
        if td == "index.html": continue
        fpath = os.path.join(ROOT, "tools", td, "index.html")
        if os.path.isfile(fpath):
            if add_language_switcher(fpath, "en", td):
                count += 1
    print(f"  Language switcher added to {count} files")
    
    print("\n=== Fixup Phase 3: Generate multilingual sitemaps ===")
    generate_sitemaps()
    
    print("\n=== Fixup Phase 4: Create language homepages ===")
    create_lang_homepages()
    
    print("\n✅ Fixup complete!")


if __name__ == "__main__":
    main()
