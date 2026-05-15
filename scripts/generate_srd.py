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
        # Replace --pb-- tag with a page break div before markdown conversion
        content = content.replace('--pb--', '<div class="page-break"></div>')
            
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

def generate_pdf(playwright, html_body, output_file, lang, cover_title, cover_subtitle, source_dir, theme_css_path, cover_logo_path=None):
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

    footer_text = "Trames - SRD" if lang == "fr" else "Threads - SRD"
    base_css = base_css.replace("FOOTER_TEXT_PLACEHOLDER", footer_text)

    srd_text = "Document de Référence (SRD)" if lang == "fr" else "System Reference Document (SRD)"
    
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
            <p class="cover-subtitle">{srd_text}</p>
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

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    configs = [
        {"lang": "fr", "dir": "Sources_fr", "title": "Trames", "subtitle": "Tisser les fils du Destin"},
        {"lang": "en", "dir": "Sources_en", "title": "Threads", "subtitle": "Weaving the Threads of Fate"}
    ]
    
    # Mapping for English supplement names to their French style directories
    supp_style_map = {
        "Solo Mode": "Mode solo",
        "Shadow Threads": "Trames d'ombres",
        "Shadow Threads Solo": "Trames d'ombres Solo"
    }
    
    with sync_playwright() as playwright:
        for config in configs:
            source_dir = config["dir"]
            if not os.path.exists(source_dir):
                print(f"Dossier introuvable : {source_dir}, génération ignorée pour {config['lang']}.")
                continue
                
            html_body = aggregate_html(source_dir)
            
            lang_output_dir = os.path.join(OUTPUT_DIR, config["lang"])
            if not os.path.exists(lang_output_dir):
                os.makedirs(lang_output_dir)
                
            # Paths to default themes
            default_noir_css = os.path.join(STYLE_DIR, "theme_noir.css")
            default_print_css = os.path.join(STYLE_DIR, "theme_print.css")
            main_logo_path = os.path.join("Images", "Trames", f"Logo_Trames_{config['lang']}.png")

            # 1. Version Noir
            generate_pdf(playwright, html_body, os.path.join(lang_output_dir, f"{config['title']}_SRD_Noir_{config['lang'].upper()}.pdf"), config["lang"], config["title"], config["subtitle"], source_dir, default_noir_css, cover_logo_path=main_logo_path)
            
            # 2. Version Print
            generate_pdf(playwright, html_body, os.path.join(lang_output_dir, f"{config['title']}_SRD_Print_{config['lang'].upper()}.pdf"), config["lang"], config["title"], config["subtitle"], source_dir, default_print_css, cover_logo_path=main_logo_path)
            
            # --- Supplements Generation ---
            supplements_dir = os.path.join(source_dir, "Suppléments")
            if os.path.exists(supplements_dir):
                for supp_name in os.listdir(supplements_dir):
                    supp_path = os.path.join(supplements_dir, supp_name)
                    if os.path.isdir(supp_path):
                        supp_html_body = aggregate_html(supp_path)
                        
                        # Retrieve the proper style directory name
                        style_folder_name = supp_style_map.get(supp_name, supp_name)
                        
                        # Check for custom themes in pdf_styles/Suppléments/ directory
                        supp_noir_css = os.path.join(STYLE_DIR, "Suppléments", style_folder_name, "theme_noir.css")
                        supp_print_css = os.path.join(STYLE_DIR, "Suppléments", style_folder_name, "theme_print.css")
                        
                        final_noir_css = supp_noir_css if os.path.exists(supp_noir_css) else default_noir_css
                        final_print_css = supp_print_css if os.path.exists(supp_print_css) else default_print_css
                        
                        supp_output_dir = os.path.join(lang_output_dir, supp_name)
                        if not os.path.exists(supp_output_dir):
                            os.makedirs(supp_output_dir)

                        print(f"Génération du supplément : {supp_name} ({config['lang']})")
                        generate_pdf(
                            playwright, 
                            supp_html_body, 
                            os.path.join(supp_output_dir, f"{supp_name}_Noir_{config['lang'].upper()}.pdf"), 
                            config["lang"], 
                            supp_name, 
                            config["subtitle"], 
                            supp_path, 
                            final_noir_css
                        )
                        
                        generate_pdf(
                            playwright, 
                            supp_html_body, 
                            os.path.join(supp_output_dir, f"{supp_name}_Print_{config['lang'].upper()}.pdf"), 
                            config["lang"], 
                            supp_name, 
                            config["subtitle"], 
                            supp_path, 
                            final_print_css
                        )
    
    print("\nSuccès ! Vos PDFs sont disponibles dans le dossier 'Générations'.")

if __name__ == "__main__":
    main()
