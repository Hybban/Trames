import os
import glob
import markdown2
import base64
import re
from playwright.sync_api import sync_playwright

# Configuration
OUTPUT_DIR = "Générations"
STYLE_DIR = "pdf_styles"

def aggregate_html(directory):
    """Lit chaque fichier MD d'un dossier (trié par nom) et le convertit en HTML."""
    md_files = sorted(glob.glob(os.path.join(directory, "*.md")))
    full_html = ""
    
    for filename in md_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert [IMG](...) (without exclamation mark) to standard markdown image ![IMG](...)
        content = re.sub(r'(?<!\!)\[IMG\]\((.*?)\)', r'![IMG](\1)', content, flags=re.IGNORECASE)
        
        # Replace --pb-- tag with a page break div before markdown conversion
        content = content.replace('--pb--', '<div class="page-break"></div>')
            
        html_segment = markdown2.markdown(content, extras=['tables', 'fenced-code-blocks', 'header-ids'])
        full_html += f"\n{html_segment}\n"
            
    return full_html

def embed_images_in_html(html_content, base_dir):
    """Recherche les balises images et encode les fichiers locaux en Base64."""
    def replacer(match):
        img_src = match.group(1)
        if img_src.startswith('http') or img_src.startswith('data:'):
            return match.group(0)
        
        # Normalize and strip leading slashes to prevent join from breaking
        clean_src = img_src.lstrip('/\\')
        
        # 1. Try to resolve relative to source_dir (base_dir)
        img_path = os.path.normpath(os.path.join(base_dir, clean_src))
        
        # 2. Fallback to project root directory
        if not os.path.exists(img_path):
            img_path = os.path.normpath(os.path.join(os.getcwd(), clean_src))
            
        if os.path.exists(img_path):
            with open(img_path, 'rb') as img_file:
                encoded = base64.b64encode(img_file.read()).decode('utf-8')
            ext = os.path.splitext(img_path)[1].lower()
            mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
            if ext == '.svg': mime = 'image/svg+xml'
            elif ext == '.gif': mime = 'image/gif'
            return f'src="data:{mime};base64,{encoded}"'
        print(f"Image introuvable : {img_path} (source: {img_src})")
        return match.group(0)
    return re.sub(r'src=["\'](.*?)["\']', replacer, html_content)

def generate_pdf(playwright, html_body, output_file, lang, cover_title, cover_subtitle, source_dir, theme_css_path, footer_text, cover_logo_path=None, document_type_text=None):
    """Génère un PDF à partir du contenu HTML et du thème spécifié utilisant Playwright."""
    html_body = embed_images_in_html(html_body, source_dir)
    
    # Transform h3-h6 into divs so only h1 and h2 are picked up by the PDF outline (bookmarks)
    for i in range(3, 7):
        html_body = re.sub(rf'<h{i}\b([^>]*)>', rf'<div class="h{i}"\1>', html_body)
        html_body = re.sub(rf'</h{i}>', '</div>', html_body)
    
    # Lecture des CSS pour injection directe
    with open(os.path.join(STYLE_DIR, "base.css"), 'r', encoding='utf-8') as f:
        base_css = f.read()
    with open(theme_css_path, 'r', encoding='utf-8') as f:
        theme_css = f.read()

    # Remplacement du footer personnalisé
    base_css = base_css.replace("FOOTER_TEXT_PLACEHOLDER", footer_text)

    # Texte de couverture de référence
    if document_type_text is None:
        document_type_text = "Livre de base" if lang == "fr" else "Core Rulebook"
    
    # Rendu du logo de couverture s'il existe
    logo_html = ""
    if cover_logo_path and os.path.exists(cover_logo_path):
        with open(cover_logo_path, 'rb') as img_file:
            encoded_logo = base64.b64encode(img_file.read()).decode('utf-8')
        ext = os.path.splitext(cover_logo_path)[1].lower()
        mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
        if ext == '.svg': mime = 'image/svg+xml'
        elif ext == '.gif': mime = 'image/gif'
        logo_html = f'<img src="data:{mime};base64,{encoded_logo}" class="cover-logo" alt="Logo">'

    # Template HTML complet
    full_html = f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <style>
            {base_css}
            {theme_css}
        </style>
    </head>
    <body>
        <div class="cover-page">
            <h1 class="cover-title">{cover_title}</h1>
            <p class="cover-subtitle">{cover_subtitle}</p>
            <p class="cover-subtitle">{document_type_text}</p>
            {logo_html}
        </div>
        <div class="content">
            {html_body}
        </div>
    </body>
    </html>
    """
    
    # Lancement du navigateur et génération
    browser = playwright.chromium.launch()
    page = browser.new_page()
    
    # On définit le contenu HTML
    page.set_content(full_html)
    
    # On attend que les polices (Google Fonts) soient chargées si possible
    page.wait_for_load_state("networkidle")

    print(f"Génération de {output_file}...")
    try:
        page.pdf(
            path=output_file,
            format="A5",
            print_background=True,
            outline=True,
            tagged=True,
            margin={
                "top": "0px", # Marges déjà gérées dans le CSS @page
                "bottom": "0px",
                "left": "0px",
                "right": "0px"
            }
        )
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier {output_file} : {e}")
        print("Astuce : Le fichier est peut-être ouvert dans un autre programme (ex: lecteur PDF). Fermez-le et réessayez.")
    finally:
        browser.close()
