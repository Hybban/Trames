import os
import sys
from playwright.sync_api import sync_playwright

# S'assurer que le dossier des scripts est dans le chemin d'importation
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pdf_generator_core

OUTPUT_DIR = "Générations"
STYLE_DIR = "pdf_styles"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    configs = [
        {
            "lang": "fr", 
            "dir": "Sources_fr", 
            "title": "Trames", 
            "subtitle": "Tisser les fils du Destin",
            "footer": "Trames - Livre de base"
        },
        {
            "lang": "en", 
            "dir": "Sources_en", 
            "title": "Threads", 
            "subtitle": "Weaving the Threads of Fate",
            "footer": "Threads - Core Rulebook"
        }
    ]
    
    with sync_playwright() as playwright:
        for config in configs:
            source_dir = config["dir"]
            if not os.path.exists(source_dir):
                print(f"Dossier introuvable : {source_dir}, génération ignorée pour {config['lang']}.")
                continue
                
            html_body = pdf_generator_core.aggregate_html(source_dir)
            
            lang_output_dir = os.path.join(OUTPUT_DIR, config["lang"])
            if not os.path.exists(lang_output_dir):
                os.makedirs(lang_output_dir)
                
            # Thèmes par défaut
            default_noir_css = os.path.join(STYLE_DIR, "theme_noir.css")
            default_print_css = os.path.join(STYLE_DIR, "theme_print.css")
            main_logo_path = os.path.join("Images", "Trames", f"Logo_Trames_{config['lang']}.png")

            suffix = "Livre_de_base" if config["lang"] == "fr" else "Core_Rulebook"

            # 1. Version Noir
            pdf_generator_core.generate_pdf(
                playwright=playwright,
                html_body=html_body,
                output_file=os.path.join(lang_output_dir, f"{config['title']}_{suffix}_Noir_{config['lang'].upper()}.pdf"),
                lang=config["lang"],
                cover_title=config["title"],
                cover_subtitle=config["subtitle"],
                source_dir=source_dir,
                theme_css_path=default_noir_css,
                footer_text=config["footer"],
                cover_logo_path=main_logo_path
            )
            
            # 2. Version Print
            pdf_generator_core.generate_pdf(
                playwright=playwright,
                html_body=html_body,
                output_file=os.path.join(lang_output_dir, f"{config['title']}_{suffix}_Print_{config['lang'].upper()}.pdf"),
                lang=config["lang"],
                cover_title=config["title"],
                cover_subtitle=config["subtitle"],
                source_dir=source_dir,
                theme_css_path=default_print_css,
                footer_text=config["footer"],
                cover_logo_path=main_logo_path
            )
            
    print("\nSuccès ! Vos PDFs du Livre de base sont disponibles dans le dossier 'Générations'.")

if __name__ == "__main__":
    main()
