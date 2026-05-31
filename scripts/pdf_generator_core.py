import os
import glob
import markdown2
import base64
import re
import io
from PIL import Image
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
        
        # Convert [URL="text"][url] or [URL=text][url] to standard markdown link [text](url)
        content = re.sub(r'\[URL=["\'](.*?)["\']\]\[(https?://.*?)\]', r'[\1](\2)', content, flags=re.IGNORECASE)
        content = re.sub(r'\[URL=([^"\'].*?)\]\[(https?://.*?)\]', r'[\1](\2)', content, flags=re.IGNORECASE)
        # Fallback for old format [URL][url] -> [URL](url)
        content = re.sub(r'\[URL\]\[(https?://.*?)\]', r'[URL](\1)', content, flags=re.IGNORECASE)
        
        # Replace --pb-- tag (with optional spaces) with a page break div before markdown conversion
        content = re.sub(r'--\s*pb\s*--', '<div class="page-break"></div>', content)
            
        html_segment = markdown2.markdown(content, extras=['tables', 'fenced-code-blocks', 'header-ids'])
        full_html += f"\n{html_segment}\n"
            
    return full_html

def embed_images_in_html(html_content, base_dir):
    """Recherche les balises images, les compresse en WebP en mémoire, et les encode en Base64."""
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
            ext = os.path.splitext(img_path)[1].lower()
            if ext == '.svg':
                with open(img_path, 'rb') as img_file:
                    encoded = base64.b64encode(img_file.read()).decode('utf-8')
                return f'src="data:image/svg+xml;base64,{encoded}"'
            
            try:
                with Image.open(img_path) as img:
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        img = img.convert('RGB')
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG', quality=70)
                    encoded = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
                return f'src="data:image/jpeg;base64,{encoded}"'
            except Exception as compress_err:
                print(f"Échec de la compression WebP pour {img_path} : {compress_err}. Utilisation brute.")
                with open(img_path, 'rb') as img_file:
                    encoded = base64.b64encode(img_file.read()).decode('utf-8')
                mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
                if ext == '.gif': mime = 'image/gif'
                return f'src="data:{mime};base64,{encoded}"'
                
        print(f"Image introuvable : {img_path} (source: {img_src})")
        return match.group(0)
    return re.sub(r'src=["\'](.*?)["\']', replacer, html_content)

def generate_pdf(playwright, html_body, output_file, lang, cover_title, cover_subtitle, source_dir, theme_css_path, footer_text, cover_logo_path=None, document_type_text=None, add_toc=True):
    """Génère un PDF à partir du contenu HTML et du thème spécifié utilisant Playwright."""
    # Embed images
    html_body = embed_images_in_html(html_body, source_dir)
    
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
        ext = os.path.splitext(cover_logo_path)[1].lower()
        if ext == '.svg':
            with open(cover_logo_path, 'rb') as img_file:
                encoded_logo = base64.b64encode(img_file.read()).decode('utf-8')
            logo_html = f'<img src="data:image/svg+xml;base64,{encoded_logo}" class="cover-logo" alt="Logo">'
        else:
            try:
                with Image.open(cover_logo_path) as img:
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        img = img.convert('RGB')
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG', quality=70)
                    encoded_logo = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
                logo_html = f'<img src="data:image/jpeg;base64,{encoded_logo}" class="cover-logo" alt="Logo">'
            except Exception as compress_err:
                print(f"Échec de la compression du logo : {compress_err}")
                with open(cover_logo_path, 'rb') as img_file:
                    encoded_logo = base64.b64encode(img_file.read()).decode('utf-8')
                mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
                if ext == '.gif': mime = 'image/gif'
                logo_html = f'<img src="data:{mime};base64,{encoded_logo}" class="cover-logo" alt="Logo">'

    # Extraction des chapitres H1 pour la Table des Matières
    h1_pattern = re.compile(r'<h1\s+id="([^"]+)"[^>]*>(.*?)</h1>', re.IGNORECASE)
    h1_headers = []
    for match in h1_pattern.finditer(html_body):
        h1_id = match.group(1)
        h1_text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        h1_headers.append({"id": h1_id, "text": h1_text})

    has_h1s = len(h1_headers) >= 1
    generate_toc = add_toc and has_h1s

    # Lancement du navigateur
    browser = playwright.chromium.launch()
    page = browser.new_page()

    final_html_body = html_body

    if generate_toc:
        # --- PASSE 1 : Génération d'un brouillon pour extraire la pagination ---
        toc_placeholder = '<div class="table-of-contents" style="visibility: hidden; break-after: page; min-height: 100vh;"></div>'
        draft_html_body = toc_placeholder + html_body
        
        draft_full_html = f"""
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
                {draft_html_body}
            </div>
        </body>
        </html>
        """
        
        draft_pdf_path = output_file + ".draft"
        page.set_content(draft_full_html)
        page.wait_for_load_state("networkidle")
        
        try:
            page.pdf(
                path=draft_pdf_path,
                format="A5",
                print_background=True,
                outline=True,
                tagged=True,
                margin={"top": "0px", "bottom": "0px", "left": "0px", "right": "0px"}
            )
            
            # Lecture des numéros de page depuis les signets du PDF brouillon
            import fitz
            doc = fitz.open(draft_pdf_path)
            pdf_toc = doc.get_toc()
            doc.close()
            
            # Filtrer les signets H1 (niveau 1)
            pdf_h1s = [entry for entry in pdf_toc if entry[0] == 1]
            # Ignorer le titre de couverture sur la page 1 si présent
            if pdf_h1s and pdf_h1s[0][2] == 1:
                pdf_h1s = pdf_h1s[1:]
                
            # Associer les numéros de page par ordre d'apparition
            for i, h1 in enumerate(h1_headers):
                if i < len(pdf_h1s):
                    h1["page"] = pdf_h1s[i][2]
                else:
                    h1["page"] = "?"
        except Exception as draft_err:
            print(f"  -> Avertissement : Échec de l'extraction de la pagination pour la table des matières : {draft_err}")
            for h1 in h1_headers:
                h1["page"] = "?"
        finally:
            if os.path.exists(draft_pdf_path):
                try:
                    os.remove(draft_pdf_path)
                except Exception:
                    pass
                    
        # Construction de la TOC stylisée
        toc_title = "Table des matières" if lang == "fr" else "Table of Contents"
        entries_html = ""
        for h1 in h1_headers:
            entries_html += f"""
            <div class="toc-item">
                <a href="#{h1['id']}" class="toc-link">
                    <span class="toc-text">{h1['text']}</span>
                    <span class="toc-dots"></span>
                    <span class="toc-page">{h1['page']}</span>
                </a>
            </div>
            """
            
        toc_html = f"""
        <div class="table-of-contents">
            <div class="toc-title">{toc_title}</div>
            <div class="toc-divider"></div>
            <div class="toc-items">
                {entries_html}
            </div>
        </div>
        """
        final_html_body = toc_html + html_body

    # --- PASSE 2 : Génération finale du PDF ---
    toc_css = """
            /* Styles de la Table des Matières */
            .table-of-contents {
                break-after: page;
                page-break-after: always;
                padding-top: 0.5cm;
                display: flex;
                flex-direction: column;
            }
            .toc-title {
                font-family: 'Century Gothic', Futura, sans-serif;
                font-size: 20pt;
                color: var(--accent-color);
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: bold;
                margin-bottom: 0.1cm;
            }
            .toc-divider {
                height: 4px;
                background-color: var(--accent-color);
                margin-bottom: 0.8cm;
                width: 100%;
            }
            .toc-items {
                display: flex;
                flex-direction: column;
                gap: 0.35cm;
            }
            .toc-item {
                break-inside: avoid;
            }
            .toc-link {
                display: flex;
                align-items: baseline;
                text-decoration: none !important;
                color: var(--text-color) !important;
                font-family: 'Century Gothic', Futura, sans-serif;
                font-size: 10.5pt;
            }
            .toc-link:hover {
                opacity: 0.85;
            }
            .toc-text {
                font-weight: bold;
                color: var(--accent-color);
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .toc-dots {
                flex-grow: 1;
                border-bottom: 2px dotted var(--muted-text);
                margin: 0 0.2cm;
                position: relative;
                top: -4px;
            }
            .toc-page {
                font-weight: bold;
                color: var(--accent-color);
                font-size: 11pt;
                text-align: right;
                min-width: 0.5cm;
            }
    """ if generate_toc else ""

    full_html = f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <style>
            {base_css}
            {theme_css}
            {toc_css}
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
            {final_html_body}
        </div>
    </body>
    </html>
    """
    
    # On définit le contenu HTML final
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
        
        # Compression post-génération avec PyMuPDF si installé
        temp_output = None
        try:
            import fitz
            temp_output = output_file + ".tmp"
            doc = fitz.open(output_file)
            doc.save(temp_output, garbage=3, deflate=True)
            doc.close()
            os.replace(temp_output, output_file)
            print("  -> Taille du PDF optimisée avec PyMuPDF.")
        except ImportError:
            pass
        except Exception as compression_error:
            print(f"  -> Avertissement : Échec de l'optimisation PyMuPDF : {compression_error}")
            if temp_output and os.path.exists(temp_output):
                os.remove(temp_output)
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier {output_file} : {e}")
        print("Astuce : Le fichier est peut-être ouvert dans un autre programme (ex: lecteur PDF). Fermez-le et réessayez.")
    finally:
        browser.close()
