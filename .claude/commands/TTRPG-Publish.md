You are helping publish books for the TRAMES tabletop RPG project. This project compiles Markdown source files into styled A5 PDFs (Noir and Print themes) using Python + Playwright.

## Your task

The user wants to publish: $ARGUMENTS

If no argument is given, ask which book(s) to publish. The options are:
- `srd` — Core rulebook (French + English)
- `solo` — Solo play supplement
- `ombres` — Trames d'ombres (urban fantasy setting)
- `ombres-solo` — Trames d'ombres solo variant
- `all` — All books at once

## Step 1 — Pre-flight checks

Before generating any PDF:

1. **Remind the user to close any open PDFs** in their PDF reader. Playwright will throw a permission error if the output file is locked.
2. **Check for unsynced bilingual files**: if recent changes were made in `Sources_fr/`, verify the corresponding files in `Sources_en/` were also updated (and vice versa). Warn the user if you find a mismatch in modification dates or content.

## Step 2 — Validate source Markdown

Scan the relevant source files (in `Sources_fr/` and/or `Sources_en/`) for common authoring mistakes that break rendering:

- **Lists not preceded by a blank line** — `markdown2` will merge them into the preceding paragraph.
- **`--pb--` not surrounded by blank lines** — page break won't be recognised by `pdf_generator_core.py`.
- **Image paths not relative to project root** — images will be missing from the PDF.
- **Old-style boxed content** using `**Encadré**` instead of `> **Titre:** Contenu` blockquote syntax — suggest running `python scripts/fix_encadres.py` to fix these automatically.
- **Writing convention violations**:
  - Real people at the table (players, GM) must use feminine forms: *la joueuse*, *la MJ*, *les joueuses*.
  - Fictional characters in the game world must use masculine forms: *le héros*, *le personnage*.
  - Flag any inconsistencies you find and suggest corrections.

Report all issues found before proceeding. If there are critical issues (broken paths, malformed page breaks), ask the user to fix them first.

## Step 3 — Generate the PDF(s)

Run the appropriate command(s):

| Book | Command |
|------|---------|
| `srd` | `python scripts/generate_srd.py` |
| `solo` | `python scripts/generate_solo.py` |
| `ombres` | `python scripts/generate_trames_d_ombres.py` |
| `ombres-solo` | `python scripts/generate_trames_d_ombres_solo.py` |
| `all` | `python scripts/generate_all.py` |

Show the command output to the user. If the generation fails, diagnose the error:
- **Permission error on output file** → PDF is open in a reader; ask the user to close it.
- **Missing image / Base64 error** → Image path is wrong; check `Images/Trames/` directory.
- **Playwright / Chromium not found** → Run `playwright install chromium`.
- **Import error** → Run `pip install -r scripts/requirements.txt`.

## Step 4 — Report

On success, tell the user:
- Which PDFs were generated and where they are (`Générations/fr/` and/or `Générations/en/`).
- The two variants produced (Noir and Print).
- Any non-critical warnings found during validation that still need attention.
