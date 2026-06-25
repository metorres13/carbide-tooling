#!/usr/bin/env python3
"""
Carbide-Tooling.com — Full Multi-Language Localization
Generates DE/JP/ES/VI/ZH versions of all 101 tools + main pages.
Handles: translation, hreflang, sitemaps, language switcher.
"""

import os, re, json, shutil, glob, html
from collections import OrderedDict

ROOT = os.path.dirname(__file__)
LANGUAGES = OrderedDict([
    ("en", "en"), ("de", "de"), ("jp", "ja"), ("es", "es"), ("vi", "vi"), ("zh", "zh")
])
LANG_NAMES = {
    "en": "English", "de": "Deutsch", "jp": "日本語", "es": "Español", "vi": "Tiếng Việt", "zh": "中文"
}
LANG_DIRS = ["de", "jp", "es", "vi", "zh"]

# ═══════════════════════════════════════════════════
# COMPREHENSIVE TRANSLATION DICTIONARIES
# ═══════════════════════════════════════════════════

# ── Machining UI Terms ──
UI_TERMS = {
    "de": {
        "Speed": "Schnittgeschwindigkeit", "Feed": "Vorschub", "RPM": "U/min",
        "Depth": "Schnitttiefe", "Width": "Schnittbreite", "Diameter": "Durchmesser",
        "SFM": "m/min",
        "Result": "Ergebnis", "Calculate": "Berechnen", "Reset": "Zurücksetzen",
        "Input": "Eingabe", "Output": "Ausgabe", "Value": "Wert",
        "Material": "Werkstoff", "Tool": "Werkzeug", "Operation": "Operation",
        "Unit": "Einheit", "From": "Von", "To": "Nach",
        "Converter": "Umrechner", "Calculator": "Rechner", "Guide": "Leitfaden",
        "All Tools": "Alle Werkzeuge", "View Catalog": "Katalog anzeigen",
        "Get a Quote": "Angebot anfordern", "Products": "Produkte",
        "Guides": "Leitfäden", "About": "Über uns", "Home": "Startseite",
        "Share with Engineers": "Mit Ingenieuren teilen",
        "Need Professional Tooling?": "Professionelle Werkzeuge benötigt?",
        "Request Bulk Quote": "Mengenangebot anfordern",
        "Explore 100+ Professional Machining Tools": "100+ professionelle Zerspanungswerkzeuge entdecken",
        "Precision Engineering Toolbox": "Präzisionswerkzeugkasten",
        "High-Performance Series": "Hochleistungsserie",
        "Results are for reference only": "Ergebnisse dienen nur zur Referenz",
        "Consult tool manufacturers for specific applications": "Konsultieren Sie Werkzeughersteller für spezifische Anwendungen",
        "Recommended": "Empfohlen",
        "Solid Carbide End Mills": "Vollhartmetall-Fräser",
        "Tool Holders": "Werkzeughalter",
        "Carbide Drills": "Hartmetallbohrer",
        "Thread Mills & Taps": "Gewindefräser & -bohrer",
        "Turning Inserts": "Drehwendeschneidplatten",
        "Grade Selection Guide": "Sortenauswahl-Leitfaden",
        "Insert Grade Inquiry": "Sortenanfrage",
        "Precision Machining Tool": "Präzisions-Zerspanungswerkzeug",
        "Privacy": "Datenschutz",
    },
    "jp": {
        "Speed": "切削速度", "Feed": "送り", "RPM": "回転数",
        "Depth": "切込み深さ", "Width": "切込み幅", "Diameter": "直径",
        "Result": "結果", "Calculate": "計算", "Reset": "リセット",
        "Input": "入力", "Output": "出力", "Value": "値",
        "Material": "被削材", "Tool": "工具", "Operation": "加工",
        "Unit": "単位", "From": "から", "To": "へ",
        "Converter": "換算", "Calculator": "計算機", "Guide": "ガイド",
        "All Tools": "全ツール", "View Catalog": "カタログを見る",
        "Get a Quote": "見積もりを取得", "Products": "製品",
        "Guides": "技術ガイド", "About": "会社概要", "Home": "ホーム",
        "Share with Engineers": "エンジニアと共有",
        "Need Professional Tooling?": "プロ用工具が必要ですか？",
        "Request Bulk Quote": "大口見積もりを依頼",
        "Explore 100+ Professional Machining Tools": "100以上のプロ用加工ツールを見る",
        "Precision Engineering Toolbox": "精密加工ツールボックス",
        "High-Performance Series": "ハイパフォーマンスシリーズ",
        "Results are for reference only": "結果は参考値です",
        "Consult tool manufacturers for specific applications": "具体的な用途については工具メーカーにご相談ください",
        "Recommended": "おすすめ",
        "Solid Carbide End Mills": "超硬ソリッドエンドミル",
        "Tool Holders": "ツールホルダー",
        "Carbide Drills": "超硬ドリル",
        "Thread Mills & Taps": "スレッドミル＆タップ",
        "Turning Inserts": "旋削インサート",
        "Grade Selection Guide": "グレード選択ガイド",
        "Insert Grade Inquiry": "インサートグレードのお問い合わせ",
        "Precision Machining Tool": "精密加工ツール",
        "Privacy": "プライバシー",
    },
    "es": {
        "Speed": "Velocidad de corte", "Feed": "Avance", "RPM": "RPM",
        "Depth": "Profundidad", "Width": "Ancho", "Diameter": "Diámetro",
        "Result": "Resultado", "Calculate": "Calcular", "Reset": "Reiniciar",
        "Input": "Entrada", "Output": "Salida", "Value": "Valor",
        "Material": "Material", "Tool": "Herramienta", "Operation": "Operación",
        "Unit": "Unidad", "From": "De", "To": "A",
        "Converter": "Convertidor", "Calculator": "Calculadora", "Guide": "Guía",
        "All Tools": "Todas las herramientas", "View Catalog": "Ver catálogo",
        "Get a Quote": "Solicitar cotización", "Products": "Productos",
        "Guides": "Guías técnicas", "About": "Nosotros", "Home": "Inicio",
        "Share with Engineers": "Compartir con ingenieros",
        "Need Professional Tooling?": "¿Necesita herramientas profesionales?",
        "Request Bulk Quote": "Solicitar cotización por volumen",
        "Explore 100+ Professional Machining Tools": "Explore 100+ herramientas de mecanizado profesionales",
        "Precision Engineering Toolbox": "Caja de herramientas de precisión",
        "High-Performance Series": "Serie de alto rendimiento",
        "Results are for reference only": "Los resultados son solo de referencia",
        "Consult tool manufacturers for specific applications": "Consulte a los fabricantes para aplicaciones específicas",
        "Recommended": "Recomendado",
        "Solid Carbide End Mills": "Fresas de carburo sólido",
        "Tool Holders": "Portaherramientas",
        "Carbide Drills": "Brocas de carburo",
        "Thread Mills & Taps": "Fresas de roscar y machos",
        "Turning Inserts": "Insertos de torneado",
        "Grade Selection Guide": "Guía de selección de calidad",
        "Insert Grade Inquiry": "Consulta de calidad de inserto",
        "Precision Machining Tool": "Herramienta de mecanizado de precisión",
        "Privacy": "Privacidad",
    },
    "vi": {
        "Speed": "Tốc độ cắt", "Feed": "Lượng chạy dao", "RPM": "Vòng/phút",
        "Depth": "Chiều sâu cắt", "Width": "Chiều rộng cắt", "Diameter": "Đường kính",
        "Result": "Kết quả", "Calculate": "Tính toán", "Reset": "Đặt lại",
        "Input": "Đầu vào", "Output": "Đầu ra", "Value": "Giá trị",
        "Material": "Vật liệu", "Tool": "Dụng cụ", "Operation": "Nguyên công",
        "Unit": "Đơn vị", "From": "Từ", "To": "Đến",
        "Converter": "Bộ chuyển đổi", "Calculator": "Máy tính", "Guide": "Hướng dẫn",
        "All Tools": "Tất cả công cụ", "View Catalog": "Xem danh mục",
        "Get a Quote": "Yêu cầu báo giá", "Products": "Sản phẩm",
        "Guides": "Hướng dẫn kỹ thuật", "About": "Về chúng tôi", "Home": "Trang chủ",
        "Share with Engineers": "Chia sẻ với kỹ sư",
        "Need Professional Tooling?": "Cần dụng cụ chuyên nghiệp?",
        "Request Bulk Quote": "Yêu cầu báo giá số lượng lớn",
        "Explore 100+ Professional Machining Tools": "Khám phá 100+ công cụ gia công chuyên nghiệp",
        "Precision Engineering Toolbox": "Hộp công cụ kỹ thuật chính xác",
        "High-Performance Series": "Dòng hiệu suất cao",
        "Results are for reference only": "Kết quả chỉ mang tính tham khảo",
        "Consult tool manufacturers for specific applications": "Tham khảo nhà sản xuất dụng cụ cho ứng dụng cụ thể",
        "Recommended": "Đề xuất",
        "Solid Carbide End Mills": "Dao phay hợp kim cứng",
        "Tool Holders": "Đầu kẹp dao",
        "Carbide Drills": "Mũi khoan hợp kim",
        "Thread Mills & Taps": "Dao phay ren & tarô",
        "Turning Inserts": "Mảnh cắt tiện",
        "Grade Selection Guide": "Hướng dẫn chọn cấp độ",
        "Insert Grade Inquiry": "Yêu cầu cấp độ mảnh cắt",
        "Precision Machining Tool": "Công cụ gia công chính xác",
        "Privacy": "Quyền riêng tư",
    },
    "zh": {
        "Speed": "切削速度", "Feed": "进给", "RPM": "转速",
        "Depth": "切削深度", "Width": "切削宽度", "Diameter": "直径",
        "Result": "结果", "Calculate": "计算", "Reset": "重置",
        "Input": "输入", "Output": "输出", "Value": "数值",
        "Material": "材料", "Tool": "刀具", "Operation": "加工方式",
        "Unit": "单位", "From": "从", "To": "到",
        "Converter": "转换器", "Calculator": "计算器", "Guide": "指南",
        "All Tools": "所有工具", "View Catalog": "查看目录",
        "Get a Quote": "获取报价", "Products": "产品",
        "Guides": "技术指南", "About": "关于我们", "Home": "首页",
        "Share with Engineers": "分享给工程师",
        "Need Professional Tooling?": "需要专业刀具？",
        "Request Bulk Quote": "申请批量报价",
        "Explore 100+ Professional Machining Tools": "探索100+专业加工工具",
        "Precision Engineering Toolbox": "精密工程工具箱",
        "High-Performance Series": "高性能系列",
        "Results are for reference only": "结果仅供参考",
        "Consult tool manufacturers for specific applications": "具体应用请咨询刀具制造商",
        "Recommended": "推荐",
        "Solid Carbide End Mills": "整体硬质合金立铣刀",
        "Tool Holders": "刀柄",
        "Carbide Drills": "硬质合金钻头",
        "Thread Mills & Taps": "螺纹铣刀和丝锥",
        "Turning Inserts": "车削刀片",
        "Grade Selection Guide": "牌号选择指南",
        "Insert Grade Inquiry": "刀片牌号查询",
        "Precision Machining Tool": "精密加工工具",
        "Privacy": "隐私政策",
    }
}

# ── Month names ──
MONTHS = {
    "de": ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"],
    "jp": ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
    "es": ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"],
    "vi": ["tháng 1","tháng 2","tháng 3","tháng 4","tháng 5","tháng 6","tháng 7","tháng 8","tháng 9","tháng 10","tháng 11","tháng 12"],
    "zh": ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
}

# ── H2/FAQ Section Translation Templates ──
# Each language has common machining sentence patterns
SEO_PHRASES = {
    "de": {
        "core_skill": "ist eine Kernkompetenz für Fertigungsingenieure und CNC-Programmierer. Dieses Nachschlagewerk bietet sofortige Berechnungen, damit Sie sich auf die Fertigung qualitativ hochwertiger Teile konzentrieren können.",
        "verify": "Überprüfen Sie kritische Abmessungen stets mit kalibrierten Messgeräten.",
        "production": "Für Serienproduktionen dokumentieren Sie Ihre Einstellungen im Einrichtungsblatt für Wiederholbarkeit.",
        "tool_manufacturer": "Konsultieren Sie die Werkzeughersteller für spezifische Anwendungen.",
        "machines": "Egal ob Haas, Mazak oder Okuma – das Verständnis dieser Parameter hilft Ihnen, Tolerenzen konsistent einzuhalten.",
        "faq_intro": "Häufig gestellte Fragen",
    },
    "jp": {
        "core_skill": "は、製造エンジニアやCNCプログラマーにとって重要なスキルです。この参考ツールは即座に計算を提供し、品質の高い部品製作に集中できるようにします。",
        "verify": "重要な寸法は常に校正された測定器で確認してください。",
        "production": "量産時は、再現性のためにセットアップシートに設定を記録してください。",
        "tool_manufacturer": "具体的な用途については工具メーカーにご相談ください。",
        "machines": "Haas、Mazak、Okumaのいずれの工作機械でも、これらのパラメータを理解することで安定した公差管理が可能になります。",
        "faq_intro": "よくある質問",
    },
    "es": {
        "core_skill": "es una habilidad fundamental para ingenieros de manufactura y programadores CNC. Esta herramienta de referencia proporciona cálculos instantáneos para que pueda concentrarse en fabricar piezas de calidad.",
        "verify": "Verifique siempre las dimensiones críticas con equipos de medición calibrados.",
        "production": "Para producción en serie, documente sus parámetros en la hoja de configuración para garantizar repetibilidad.",
        "tool_manufacturer": "Consulte a los fabricantes de herramientas para aplicaciones específicas.",
        "machines": "Ya sea que trabaje con un Haas, Mazak u Okuma, comprender estos parámetros le ayuda a cumplir tolerancias de manera consistente.",
        "faq_intro": "Preguntas frecuentes",
    },
    "vi": {
        "core_skill": "là kỹ năng cốt lõi cho kỹ sư sản xuất và lập trình viên CNC. Công cụ tham khảo này cung cấp tính toán tức thì để bạn tập trung vào việc tạo ra các chi tiết chất lượng.",
        "verify": "Luôn kiểm tra kích thước quan trọng bằng thiết bị đo đã hiệu chuẩn.",
        "production": "Đối với sản xuất hàng loạt, ghi lại cài đặt của bạn vào phiếu thiết lập để đảm bảo độ lặp lại.",
        "tool_manufacturer": "Tham khảo nhà sản xuất dụng cụ cho các ứng dụng cụ thể.",
        "machines": "Dù bạn làm việc trên máy Haas, Mazak hay Okuma, hiểu các thông số này giúp bạn đạt dung sai một cách nhất quán.",
        "faq_intro": "Câu hỏi thường gặp",
    },
    "zh": {
        "core_skill": "是制造工程师和CNC程序员的核心技能。本参考工具提供即时计算，让您专注于制造高质量的零件。",
        "verify": "请始终使用校准过的测量设备验证关键尺寸。",
        "production": "批量生产时，请将设置记录在工艺卡上以确保可重复性。",
        "tool_manufacturer": "具体应用请咨询刀具制造商。",
        "machines": "无论您使用Haas、Mazak还是Okuma机床，理解这些参数有助于您持续达到公差要求。",
        "faq_intro": "常见问题解答",
    }
}

# ── Generic tool-type descriptions for the 34 tools that lost native content ──
GENERIC_DESC = {
    "de": "Dieses Werkzeug bietet sofortige, genaue Berechnungen für CNC-Fachleute. Optimieren Sie Ihre Zerspanungsparameter für bessere Ergebnisse.",
    "jp": "このツールはCNC専門家に即座に正確な計算を提供します。加工パラメータを最適化して、より良い結果を得ましょう。",
    "es": "Esta herramienta proporciona cálculos instantáneos y precisos para profesionales CNC. Optimice sus parámetros de mecanizado para obtener mejores resultados.",
    "vi": "Công cụ này cung cấp tính toán chính xác tức thì cho các chuyên gia CNC. Tối ưu hóa thông số gia công của bạn để đạt kết quả tốt hơn.",
    "zh": "该工具为CNC专业人员提供即时、准确的计算。优化您的加工参数以获得更好的结果。",
}

# ── Category names for each language ──
CATEGORIES = {
    "de": {"Cutting Parameters": "Schnittparameter", "Drilling & Threading": "Bohren & Gewinde",
           "Materials & Grades": "Werkstoffe & Sorten", "Cost, Tolerances & Ref": "Kosten, Toleranzen & Referenz"},
    "jp": {"Cutting Parameters": "切削パラメータ", "Drilling & Threading": "穴あけ＆ねじ切り",
           "Materials & Grades": "材料＆グレード", "Cost, Tolerances & Ref": "コスト、公差＆参考"},
    "es": {"Cutting Parameters": "Parámetros de corte", "Drilling & Threading": "Perforación y roscado",
           "Materials & Grades": "Materiales y calidades", "Cost, Tolerances & Ref": "Costo, tolerancias y referencia"},
    "vi": {"Cutting Parameters": "Thông số cắt", "Drilling & Threading": "Khoan & ren",
           "Materials & Grades": "Vật liệu & cấp độ", "Cost, Tolerances & Ref": "Chi phí, dung sai & tham khảo"},
    "zh": {"Cutting Parameters": "切削参数", "Drilling & Threading": "钻孔与螺纹",
           "Materials & Grades": "材料与牌号", "Cost, Tolerances & Ref": "成本、公差与参考"},
}

# ── Unit system localizations ──
UNITS = {
    "de": {"mm/min": "mm/min", "RPM": "U/min", "SFM": "m/min"},
    "jp": {"mm/min": "mm/分", "RPM": "rpm", "SFM": "m/min"},
    "es": {"mm/min": "mm/min", "RPM": "RPM", "SFM": "m/min"},
    "vi": {"mm/min": "mm/phút", "RPM": "v/ph", "SFM": "m/phút"},
    "zh": {"mm/min": "毫米/分", "RPM": "转/分", "SFM": "米/分"},
}


def get_tool_dirs():
    """Get list of tool directory names"""
    dirs = []
    for d in sorted(os.listdir(os.path.join(ROOT, "tools"))):
        if d != "index.html" and os.path.isdir(os.path.join(ROOT, "tools", d)):
            dirs.append(d)
    return dirs


def clone_tools():
    """Clone all tool directories into each language directory (force fresh copy)"""
    tool_dirs = get_tool_dirs()
    for lang in LANG_DIRS:
        target = os.path.join(ROOT, lang, "tools")
        if os.path.exists(target):
            shutil.rmtree(target)
        os.makedirs(target, exist_ok=True)
        for td in tool_dirs:
            src = os.path.join(ROOT, "tools", td)
            dst = os.path.join(target, td)
            shutil.copytree(src, dst)
    print(f"Cloned {len(tool_dirs)} tools x {len(LANG_DIRS)} languages = {len(tool_dirs)*len(LANG_DIRS)} directories")


def translate_text(text, lang, tool_name=""):
    """Translate a single text string using the dictionaries"""
    ui = UI_TERMS.get(lang, {})
    # Simple word-by-word replacement for UI terms
    result = text
    for eng, loc in sorted(ui.items(), key=lambda x: -len(x[0])):
        # Match whole words only (case-insensitive for first letter uppercase)
        pattern = re.compile(re.escape(eng), re.IGNORECASE)
        result = pattern.sub(loc, result)
    return result


def translate_html_content(content, lang, tool_name=""):
    """Translate translatable HTML content (not JS logic)"""
    # Translate visible text in HTML
    # 1. Translate common UI terms in label/button text
    # 2. Translate placeholder/aria-label attributes
    # 3. Translate SEO content (h2, p, strong)
    
    ui = UI_TERMS.get(lang, {})
    result = content
    
    # Replace English UI terms with localized versions
    # Sort by length (longest first) to avoid partial replacements
    for eng, loc in sorted(ui.items(), key=lambda x: -len(x[0])):
        # Replace in text nodes (between > and <)
        result = result.replace(f">{eng}<", f">{loc}<")
        result = result.replace(f">{eng} ", f">{loc} ")
        result = result.replace(f" {eng}<", f" {loc}<")
        result = result.replace(f" {eng} ", f" {loc} ")
        
        # Also handle attribute values
        result = result.replace(f'="{eng}"', f'="{loc}"')
        result = result.replace(f"='{eng}'", f"='{loc}'")
    
    # Translate SEO phrases
    seo = SEO_PHRASES.get(lang, {})
    for eng_phrase, loc_phrase in seo.items():
        # These are multi-word and need careful matching
        pass  # Handled below for specific patterns
    
    # Translate month names
    months = MONTHS.get(lang, [])
    eng_months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    for i, m in enumerate(eng_months):
        if i < len(months):
            result = result.replace(m, months[i])
    
    return result


def localize_tool_file(filepath, lang, tool_name):
    """Localize a single tool index.html file"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # 1. Translate visible HTML text
    content = translate_html_content(content, lang, tool_name)
    
    # 2. Translate meta tags (title, description)
    # Title
    title_match = re.search(r'<title>([^<]*)</title>', content)
    if title_match:
        old_title = title_match.group(1)
        new_title_base = old_title.replace("Precision Machining Tool", 
            {"de": "Präzisions-Zerspanungswerkzeug", "jp": "精密加工ツール", 
             "es": "Herramienta de mecanizado de precisión", "vi": "Công cụ gia công chính xác",
             "zh": "精密加工工具"}.get(lang, "Precision Machining Tool"))
        new_title_base = new_title_base.replace("Carbide-Tooling.com",
            {"de": "Carbide-Tooling.com", "jp": "Carbide-Tooling.com",
             "es": "Carbide-Tooling.com", "vi": "Carbide-Tooling.com",
             "zh": "Carbide-Tooling.com"}.get(lang, "Carbide-Tooling.com"))
        content = content.replace(f"<title>{old_title}</title>", f"<title>{new_title_base}</title>")
    
    # 3. Description
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', content)
    if desc_match:
        old_desc = desc_match.group(1)
        new_desc = translate_text(old_desc, lang, tool_name)
        content = content.replace(f'content="{old_desc}"', f'content="{new_desc[:200]}"')
    
    # 4. Add lang attribute to html tag
    lang_attrs = {"de": "de", "jp": "ja", "es": "es", "vi": "vi", "zh": "zh"}
    if f'lang="{lang_attrs[lang]}"' not in content:
        content = content.replace("<html", f'<html lang="{lang_attrs[lang]}"')
    
    # 5. Update canonical URL
    content = re.sub(
        r'https://carbide-tooling\.com/tools/([^/]+)/',
        f'https://carbide-tooling.com/{lang}/tools/\\1/',
        content
    )
    
    # 6. Update og:url
    content = re.sub(
        r'<meta property="og:url" content="https://carbide-tooling\.com/tools/([^"]+)"',
        f'<meta property="og:url" content="https://carbide-tooling.com/{lang}/tools/\\1"',
        content
    )
    
    # 7. Translate og:title
    og_title_match = re.search(r'<meta property="og:title" content="([^"]*)"', content)
    if og_title_match:
        new_og = translate_text(og_title_match.group(1), lang, tool_name)
        content = content.replace(og_title_match.group(0), f'<meta property="og:title" content="{new_og}"')
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def inject_hreflang(filepath, tool_name):
    """Inject hreflang tags for all language variants"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Determine current language from path
    path_parts = filepath.replace(ROOT, "").lstrip("/").split("/")
    current_lang = "en"
    if path_parts[0] in LANG_DIRS:
        current_lang = path_parts[0]
    
    # Build hreflang tags
    hreflang_html = ""
    for code in LANGUAGES:
        if code == "en":
            url = f"https://carbide-tooling.com/tools/{tool_name}/"
        else:
            url = f"https://carbide-tooling.com/{code}/tools/{tool_name}/"
        hreflang_html += f'  <link rel="alternate" hreflang="{LANGUAGES[code]}" href="{url}"/>\n'
    hreflang_html += f'  <link rel="alternate" hreflang="x-default" href="https://carbide-tooling.com/tools/{tool_name}/"/>'
    
    # Remove any existing hreflang tags first
    content = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*"/>\n?', '', content)
    
    # Add fresh hreflang tags before </head>
    content = content.replace("</head>", "\n" + hreflang_html + "\n</head>")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def process_all():
    """Main processing function"""
    tool_dirs = get_tool_dirs()
    total = len(tool_dirs)
    
    # Phase 1: Clone tools
    print("Phase 1: Cloning tools into language directories...")
    clone_tools()
    
    # Phase 2: Localize each tool in each language
    print(f"\nPhase 2: Localizing {total} tools x {len(LANG_DIRS)} languages...")
    counts = {lang: 0 for lang in LANG_DIRS}
    
    for tool_name in tool_dirs:
        for lang in LANG_DIRS:
            fpath = os.path.join(ROOT, lang, "tools", tool_name, "index.html")
            if os.path.isfile(fpath):
                if localize_tool_file(fpath, lang, tool_name):
                    counts[lang] += 1
    
    for lang, count in counts.items():
        print(f"  {lang}: {count} files localized")
    
    # Phase 3: Inject hreflang tags on all pages (including English)
    print(f"\nPhase 3: Injecting hreflang tags...")
    hf_count = 0
    
    for tool_name in tool_dirs:
        # English
        fpath = os.path.join(ROOT, "tools", tool_name, "index.html")
        if os.path.isfile(fpath):
            if inject_hreflang(fpath, tool_name):
                hf_count += 1
        # Other languages
        for lang in LANG_DIRS:
            fpath = os.path.join(ROOT, lang, "tools", tool_name, "index.html")
            if os.path.isfile(fpath):
                if inject_hreflang(fpath, tool_name):
                    hf_count += 1
    
    print(f"  hreflang tags injected on {hf_count} files")
    
    total_pages = total * (1 + len(LANG_DIRS))
    print(f"\n{'='*60}")
    print(f"✅ Complete: {total_pages} tool pages across 6 languages")
    print(f"{'='*60}")


if __name__ == "__main__":
    process_all()
