import os, re, html

SITE = '/Users/nicky/ZCodeProject/carbide-site'

# Read the index.html to extract nav, footer
with open(os.path.join(SITE, 'index.html'), 'r') as f:
    idx = f.read()

# Extract nav section (from <nav to </nav>)
nav_m = re.search(r'<nav>.*?</nav>', idx, re.DOTALL)
NAV = nav_m.group(0) if nav_m else ''

# Extract footer section (from <footer to </footer>)
ft_m = re.search(r'<footer>.*?</footer>', idx, re.DOTALL)
FOOTER = ft_m.group(0) if ft_m else ''

def convert(filepath):
    rel = os.path.relpath(filepath, SITE)
    print(f"  {rel}")
    
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    
    # Extract title, description
    t_m = re.search(r'<title>(.*?)</title>', text, re.DOTALL)
    d_m = re.search(r'<meta name="description"[^>]*content="([^"]*)"', text)
    c_m = re.search(r'<link rel="canonical"[^>]*href="([^"]*)"', text)
    
    title = t_m.group(1).strip() if t_m else 'Carbide Tooling'
    desc = d_m.group(1) if d_m else ''
    canonical = c_m.group(1) if c_m else f'https://carbide-tooling.com/{rel}'
    
    # Extract body content (exclude old nav and footer)
    body = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.DOTALL)
    body = re.sub(r'<footer[^>]*>.*?</footer>', '', body, flags=re.DOTALL)
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r'.*?<body[^>]*>', '', body, flags=re.DOTALL)
    body = re.sub(r'</body>.*', '', body, flags=re.DOTALL)
    body = body.strip()
    
    # Clean old styles
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<link[^>]*rel="?stylesheet"?[^>]*>', '', body, flags=re.DOTALL)
    # Remove meta/links in body
    body = re.sub(r'<meta[^>]*>', '', body)
    body = re.sub(r'<link[^>]*>', '', body)
    
    # Remove old JSON-LD
    body = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    
    # Wrap body in content div
    depth = rel.count('/')
    prefix = '../' * depth if depth > 0 else './'
    
    # Fix paths
    body = body.replace('src="images/', f'src="{prefix}images/')
    body = body.replace('href="images/', f'href="{prefix}images/')
    body = body.replace('href="products/', f'href="{prefix}products/')
    body = body.replace('href="guides/', f'href="{prefix}guides/')
    
    # Fix nav paths for subpages
    nav_fixed = NAV
    nav_fixed = nav_fixed.replace('href="/', f'href="{prefix}')
    nav_fixed = nav_fixed.replace('src="/', f'src="{prefix}')
    # But external URLs should remain absolute
    nav_fixed = nav_fixed.replace(f'href="{prefix}https://', 'href="https://')
    nav_fixed = nav_fixed.replace(f'src="{prefix}https://', 'src="https://')
    # Fix the href="/ to point to root for nav items
    nav_fixed = nav_fixed.replace(f'href="{prefix}"', 'href="/"')
    # Actually this is getting complex. Let me use a smarter approach:
    # For nav items that should point to root, they need ../ prepended
    # Simple approach: in subpages, root-relative paths need ../
    if depth > 0:
        nav_fixed = NAV.replace('href="/', f'href="{depth > 0 and "../" * depth or "./"}')
        nav_fixed = nav_fixed.replace(f'href="{"../" * depth}https://', 'href="https://')
        nav_fixed = nav_fixed.replace(f'href="{"../" * depth}//', 'href="//')
    else:
        nav_fixed = NAV
    
    # Fixed: use a simpler approach
    nav_fixed = NAV
    if depth > 0:
        nav_fixed = nav_fixed.replace('href="/products/', f'href="{prefix}products/')
        nav_fixed = nav_fixed.replace('href="/guides/', f'href="{prefix}guides/')
        nav_fixed = nav_fixed.replace('href="/about.html', f'href="{prefix}about.html')
        nav_fixed = nav_fixed.replace('href="/quote.html', f'href="{prefix}quote.html')
        nav_fixed = nav_fixed.replace('href="/"', f'href="{prefix}index.html')
        # Don't replace external URLs
        nav_fixed = nav_fixed.replace('href="https://', '##EXTHREF##')
        nav_fixed = nav_fixed.replace(f'href="{prefix}https://', 'href="https://')
        nav_fixed = nav_fixed.replace('##EXTHREF##', 'href="https://')
    
    # Fix footer paths too
    footer_fixed = FOOTER
    if depth > 0:
        footer_fixed = footer_fixed.replace('href="/products/', f'href="{prefix}products/')
        footer_fixed = footer_fixed.replace('href="/guides/', f'href="{prefix}guides/')
        footer_fixed = footer_fixed.replace('href="/about.html', f'href="{prefix}about.html')
        footer_fixed = footer_fixed.replace('href="/quote.html', f'href="{prefix}quote.html')
        footer_fixed = footer_fixed.replace('href="/"', f'href="{prefix}index.html')
        footer_fixed = footer_fixed.replace('src="/images/', f'src="{prefix}images/')
        # External URLs
        footer_fixed = footer_fixed.replace('href="https://', '##EXTHREF##')
        footer_fixed = footer_fixed.replace(f'href="{prefix}https://', 'href="https://')
        footer_fixed = footer_fixed.replace('##EXTHREF##', 'href="https://')
    
    # Build page
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{html.escape(canonical)}">
<meta name="robots" content="index, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700;14..32,800;14..32,900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Inter',-apple-system,'SF Pro Display','Helvetica Neue',Arial,sans-serif;background:#fff;color:#1d1d1f;line-height:1.6;-webkit-font-smoothing:antialiased}}
.container{{max-width:700px;margin:0 auto;padding:0 24px}}
h1{{font-size:40px;font-weight:800;letter-spacing:-.8px;padding-top:80px;margin-bottom:8px}}
.sub{{font-size:18px;color:#86868b;margin-bottom:40px;line-height:1.7}}
p{{font-size:15px;color:#333;margin-bottom:18px;line-height:1.8}}
h2{{font-size:22px;font-weight:700;margin:44px 0 10px;letter-spacing:-.3px}}
h3{{font-size:16px;font-weight:600;margin:28px 0 8px}}
ul,ol{{padding-left:20px;margin-bottom:18px}}
li{{font-size:14px;color:#444;margin-bottom:5px;line-height:1.7}}
a{{color:#0066cc;text-decoration:none}}
a:hover{{text-decoration:underline}}
.breadcrumb{{font-size:12px;color:#86868b;padding-top:20px;margin-bottom:8px}}
.breadcrumb a{{color:#0066cc}}
code{{background:#f5f5f7;padding:1px 6px;border-radius:4px;font-size:13px}}
@media(max-width:768px){{h1{{font-size:28px;padding-top:48px}}}}
</style>
</head>
<body>

{nav_fixed}

<main>
<div class="container" style="min-height:60vh">
{body}
</div>
</main>

{footer_fixed}

</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f"    ✅ {rel}")

def main():
    print("🔄 Converting sub-pages to Apple-industrial style...\n")
    for root, dirs, files in os.walk(SITE):
        for f in files:
            if f.endswith('.html') and f != 'index.html':
                convert(os.path.join(root, f))
    print("\n✅ Done! All sub-pages converted.")

if __name__ == '__main__':
    main()
