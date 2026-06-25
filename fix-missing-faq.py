#!/usr/bin/env python3
"""Regenerate basic SEO content for 34 tools that lost their FAQ in the first unify run"""
import os, re

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")

TOOLS = [
    "aql-sampling-calculator", "arc-r-to-ij-converter", "automation-vs-manual-calculator",
    "batch-cost-calculator", "bolt-circle-calculator", "bulk-discount-calculator",
    "cnc-roi-calculator", "coolant-lifecycle-cost", "coord-rotation-calculator",
    "cost-per-part-calculator", "engineering-interest-calculator", "feed-converter",
    "flatness-calculator", "gcode-reference", "inventory-turnover-calculator",
    "iso-fit-calculator", "machine-power-calculator", "mcode-reference",
    "micron-inch-converter", "polar-rect-converter", "pomodoro-timer",
    "pressure-converter", "production-efficiency-calculator", "scrap-value-calculator",
    "sfm-m-min-converter", "shipping-duty-estimator", "temp-converter",
    "tool-change-time-analyzer", "tool-life-economics", "tool-wear-cost-calculator",
    "toolbox-organizer", "torque-unit-converter", "ultimate-unit-converter",
    "weight-shipping-calculator"
]

H2_TEMPLATES = {
    "calculator": [
        ("How the {tool} Works", "The {tool} provides instant, accurate results for CNC machining professionals. Whether you're programming a Haas, Mazak, or Okuma, having the right reference data helps you make better decisions on the shop floor. This tool eliminates guesswork and reduces setup time."),
        ("Practical Applications in CNC Machining", "In daily shop operations, the {tool} serves as a quick reference for machinists, programmers, and manufacturing engineers. Use it during setup, programming, or quality inspection to verify your parameters and ensure consistent results across production runs."),
        ("Best Practices for Accurate Results", "For best results with the {tool}, always verify your input values against known material specifications and machine capabilities. Document your settings in the setup sheet for repeatability. When in doubt, consult tool manufacturer recommendations for optimal performance."),
    ],
}

def friendly_name(name):
    return name.replace("-", " ").title().replace("Cnc", "CNC").replace("Sfm", "SFM").replace("Gcode", "G-Code").replace("Mcode", "M-Code")

def generate_seo(tool_name):
    friendly = friendly_name(tool_name)
    h2s = H2_TEMPLATES["calculator"]
    
    html = '\n<section class="seo-content">\n<div class="container">\n'
    for i, (title, para) in enumerate(h2s):
        html += f'<h2>{title.format(tool=friendly)}</h2>\n<p>{para.format(tool=friendly)}</p>\n'
    
    html += '''<h2>Frequently Asked Questions</h2>
<p><strong>How accurate is this tool?</strong> Results are based on standard engineering formulas and are provided for reference. Always verify critical dimensions with calibrated measurement equipment before production.</p>
<p><strong>Can I use these results for all materials?</strong> The calculations apply to standard materials. For specialized alloys or non-standard conditions, consult the tool manufacturer for specific recommendations.</p>
<p><strong>How do I improve my machining process with this data?</strong> Use this reference data as a starting point and adjust based on your specific machine, tooling, and material combination. Document successful settings for future reference.</p>'''
    
    html += '\n</div>\n</section>\n'
    return html


def main():
    success = 0
    for tool_name in TOOLS:
        fpath = os.path.join(TOOLS_DIR, tool_name, "index.html")
        if not os.path.isfile(fpath):
            print(f"  SKIP {tool_name}: file not found")
            continue
        
        with open(fpath) as f:
            content = f.read()
        
        if "Frequently Asked Questions" in content:
            print(f"  SKIP {tool_name}: already has FAQ")
            continue
        
        seo_html = generate_seo(tool_name)
        
        # Insert before <section class="more-tools"> or before </body>
        if '<section class="more-tools">' in content:
            content = content.replace('<section class="more-tools">', seo_html + '\n<section class="more-tools">', 1)
        elif '</body>' in content:
            content = content.replace('</body>', seo_html + '\n</body>', 1)
        else:
            print(f"  ERROR {tool_name}: no insertion point found")
            continue
        
        with open(fpath, "w") as f:
            f.write(content)
        
        success += 1
        print(f"  ✅ {tool_name}")
    
    print(f"\nFixed {success} tools")


if __name__ == "__main__":
    main()
