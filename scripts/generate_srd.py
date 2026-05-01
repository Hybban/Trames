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
    """Lit chaque fichier MD et le convertit en HTML."""
    md_files = sorted(glob.glob(os.path.join(directory, "*.md")))
    full_html = ""
    
    for filename in md_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        html_segment = markdown2.markdown(content, extras=['tables', 'fenced-code-blocks', 'header-ids'])
        full_html += f"\n{html_segment}\n"
            
    return full_html

def embed_images_in_html(html_content, base_dir):
    def replacer(match):
        img_src = match.group(1)
        if img_src.startswith('http') or img_src.startswith('data:'):
            return match.group(0)
        img_path = os.path.normpath(os.path.join(base_dir, img_src))
        if os.path.exists(img_path):
            with open(img_path, 'rb') as img_file:
                encoded = base64.b64encode(img_file.read()).decode('utf-8')
            ext = os.path.splitext(img_path)[1].lower()
            mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
            if ext == '.svg': mime = 'image/svg+xml'
            elif ext == '.gif': mime = 'image/gif'
            return f'src="data:{mime};base64,{encoded}"'
        print(f"Image introuvable : {img_path}")
        return match.group(0)
    return re.sub(r'src=["\'](.*?)["\']', replacer, html_content)

def generate_pdf(playwright, html_body, theme_name, output_file, lang, cover_title, cover_subtitle, source_dir):
    """Génère un PDF à partir du contenu HTML et du thème spécifié utilisant Playwright."""
    html_body = embed_images_in_html(html_body, source_dir)
    
    # Lecture des CSS pour injection directe
    with open(os.path.join(STYLE_DIR, "base.css"), 'r', encoding='utf-8') as f:
        base_css = f.read()
    with open(os.path.join(STYLE_DIR, f"theme_{theme_name}.css"), 'r', encoding='utf-8') as f:
        theme_css = f.read()

    srd_text = "Document de Référence (SRD)" if lang == "fr" else "System Reference Document (SRD)"

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
            <p class="cover-subtitle">{srd_text}</p>
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

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    configs = [
        {"lang": "fr", "dir": "Sources_fr", "title": "Trames", "subtitle": "Tisser les fils du Destin"},
        {"lang": "en", "dir": "Sources_en", "title": "Threads", "subtitle": "Weaving the Threads of Fate"}
    ]
    
    with sync_playwright() as playwright:
        for config in configs:
            source_dir = config["dir"]
            if not os.path.exists(source_dir):
                print(f"Dossier introuvable : {source_dir}, génération ignorée pour {config['lang']}.")
                continue
                
            html_body = aggregate_html(source_dir)
            
            # 1. Version Noir
            generate_pdf(playwright, html_body, "noir", os.path.join(OUTPUT_DIR, f"{config['title']}_SRD_Noir_{config['lang'].upper()}.pdf"), config["lang"], config["title"], config["subtitle"], source_dir)
            
            # 2. Version Print
            generate_pdf(playwright, html_body, "print", os.path.join(OUTPUT_DIR, f"{config['title']}_SRD_Print_{config['lang'].upper()}.pdf"), config["lang"], config["title"], config["subtitle"], source_dir)
    
    print("\nSuccès ! Vos PDFs sont disponibles dans le dossier 'Générations'.")

if __name__ == "__main__":
    main()
