# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TRAMES is a French tabletop RPG system with a bilingual (French/English) source content pipeline that generates styled PDFs via Python + Playwright. The project compiles Markdown source files into multi-theme A5 PDFs using a CSS-driven styling system.

## Setup

```bash
pip install -r scripts/requirements.txt
playwright install chromium
```

## Build Commands

```bash
# Generate a single book
python scripts/generate_base.py          # Core rulebook (FR + EN)
python scripts/generate_solo.py          # Solo play supplement
python scripts/generate_trames_d_ombres.py       # Urban fantasy setting
python scripts/generate_trames_d_ombres_solo.py  # Shadow threads solo variant

# Generate all books at once
python scripts/generate_all.py

# Fix blockquote formatting in source files
python scripts/fix_encadres.py
```

**Note:** Close any open PDFs in readers before generating — Playwright will fail with a permission error if the output file is locked.

## Architecture

### Content → PDF Pipeline

1. **Source files** (`Sources_fr/` or `Sources_en/`): Markdown files numbered sequentially (e.g., `01_creation_de_perso.md`). Each starts with a `# H1` title that becomes the chapter cover.
2. **`pdf_generator_core.py`**: Core library that aggregates markdown files into a single HTML document, embeds images as Base64, applies CSS themes, and renders to PDF via Playwright/Chromium.
3. **Generator scripts** (`generate_*.py`): Each calls `pdf_generator_core.py` with a specific source directory, output path, and CSS theme list. Generators define which supplement folders to include and which images/logos to embed.
4. **Output** (`Générations/fr/` and `Générations/en/`): Two PDF variants per book — `Noir` (dark theme) and `Print` (light theme). This directory is gitignored.

### Styling System

- **`pdf_styles/base.css`**: Shared global styles — A5 format (1.3 cm margins), Google Fonts (Outfit headers, Inter body), CSS columns, table styles, CSS variables for colors.
- **`pdf_styles/theme_noir.css`** and **`theme_print.css`**: Override color variables for the two base themes.
- **`Suppléments/`** subdirectories contain supplement-specific CSS overrides (green for solo, gray/turquoise for Trames d'ombres, carmine for the combined solo variant).

### Source File Conventions

- `Sources_fr/` and `Sources_en/` mirror each other exactly — changes in one require parallel updates in the other.
- Supplement chapters live in subfolders inside the source directories (e.g., `Sources_fr/Mode_solo/`).
- When a file in French is modified in `Sources_fr/`, update the translation of the corresponding file in `Sources_en/` in the same commit.

## Markdown Authoring Rules

These rules affect rendering — violating them causes layout or parsing bugs:

- **Lists**: Always precede with a blank line, or `markdown2` merges them into the preceding paragraph.
- **Page breaks**: Insert `--pb--` on its own line (surrounded by blank lines) — processed by `pdf_generator_core.py` into a CSS page-break element.
- **Images**: `![Alt](Images/Trames/file.png)` (standard) or `[IMG](Images/Trames/file.png)` (shorthand processed by core). Paths are relative to project root.
- **Boxed content (encadrés)**: Use `> **Titre:** Contenu` blockquote syntax. The `fix_encadres.py` script converts older `**Encadré**` patterns to this format.
- **Single-column content**: Insert `--pb--` before content that must not be split across CSS columns.

## Writing Conventions

- Real people at the table (players, GM) → feminine forms: *la joueuse*, *la MJ*.
- Fictional characters in the game world → masculine forms: *le héros*, *le personnage*.
