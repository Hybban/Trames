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
            "dir": "Sources_fr/Suppléments/Trames d'ombres Solo", 
            "title": "Trames d'ombres Solo", 
            "subtitle": "Tisser les fils du Destin",
            "style_dir_name": "Trames d'ombres Solo",
            "footer": "Trames - Trames d'ombres Solo",
            "document_type_text": "Supplément Solo"
        },
        {
            "lang": "en", 
            "dir": "Sources_en/Suppléments/Shadow Threads Solo", 
            "title": "Shadow Threads Solo", 
            "subtitle": "Weaving the Threads of Fate",
            "style_dir_name": "Trames d'ombres Solo", # English uses the French style directory
            "footer": "Threads - Shadow Threads Solo",
            "document_type_text": "Solo Supplement"
        }
    ]
    
    with sync_playwright() as playwright:
        for config in configs:
            source_dir = config["dir"]
            if not os.path.exists(source_dir):
                print(f"Dossier introuvable : {source_dir}, génération ignorée pour {config['lang']}.")
                continue
                
            html_body = pdf_generator_core.aggregate_html(source_dir)
            
            lang_output_dir = os.path.join(OUTPUT_DIR, config["lang"], config["title"])
            if not os.path.exists(lang_output_dir):
                os.makedirs(lang_output_dir)
                
            # Thèmes personnalisés et par défaut en fallback
            default_noir_css = os.path.join(STYLE_DIR, "theme_noir.css")
            default_print_css = os.path.join(STYLE_DIR, "theme_print.css")
            
            custom_noir_css = os.path.join(STYLE_DIR, "Suppléments", config["style_dir_name"], "theme_noir.css")
            custom_print_css = os.path.join(STYLE_DIR, "Suppléments", config["style_dir_name"], "theme_print.css")
            
            final_noir_css = custom_noir_css if os.path.exists(custom_noir_css) else default_noir_css
            final_print_css = custom_print_css if os.path.exists(custom_print_css) else default_print_css
 
            # 1. Version Noir
            pdf_generator_core.generate_pdf(
                playwright=playwright,
                html_body=html_body,
                output_file=os.path.join(lang_output_dir, f"{config['title']}_Noir_{config['lang'].upper()}.pdf"),
                lang=config["lang"],
                cover_title=config["title"],
                cover_subtitle=config["subtitle"],
                source_dir=source_dir,
                theme_css_path=final_noir_css,
                footer_text=config["footer"],
                document_type_text=config["document_type_text"]
            )
            
            # 2. Version Print
            pdf_generator_core.generate_pdf(
                playwright=playwright,
                html_body=html_body,
                output_file=os.path.join(lang_output_dir, f"{config['title']}_Print_{config['lang'].upper()}.pdf"),
                lang=config["lang"],
                cover_title=config["title"],
                cover_subtitle=config["subtitle"],
                source_dir=source_dir,
                theme_css_path=final_print_css,
                footer_text=config["footer"],
                document_type_text=config["document_type_text"]
            )
            
    print("\nSuccès ! Vos PDFs Trames d'ombres Solo sont disponibles dans le dossier 'Générations'.")

if __name__ == "__main__":
    main()
