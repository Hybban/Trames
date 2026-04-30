---
name: ttrpg-writer
description: Assists TTRPG writers in extracting information from source documents (txt, docx, pdf), organizing lore and mechanics, and structuring manuscripts according to professional TTRPG publishing best practices. Use when Claude is asked to help write, lay out, summarize, or edit a Tabletop RPG rulebook, campaign, or setting document.
---

# TTRPG Writer Assistant

This skill equips Claude to assist Tabletop RPG (TTRPG) authors in analyzing their raw notes (PDFs, DOCX, TXT) and turning them into professionally structured and formatted manuscripts.

## Workflow

1.  **Understand the Source Material**: 
    If the user points to unstructured files (like PDFs or Word docs) containing game lore or mechanics, use `python scripts/extract_docs.py <path_to_file>` to read the textual contents if you cannot read them directly with your built-in tools.

2.  **Separate "Fluff" from "Crunch"**:
    Always help the author structure their content by distinctly isolating narrative/lore ("Fluff") from mechanical rules and stats ("Crunch"). Never bury a complex mechanic within a long narrative paragraph.

3.  **Apply Professional Publishing Rules**:
    When drafting or restructuring sections, follow the best practices defined in [references/design_rules.md](references/design_rules.md).

4.  **Use Ergonomic Layouts**:
    When asked to provide a layout or a draft for a page, use the structure and visual elements provided in [assets/jdr_template.md](assets/jdr_template.md). Help the user prioritize readability, clear signposting, and accessibility (e.g., contrasting call-out boxes, bullet points, avoiding walls of text).

5.  **Review & Polish**:
    If asked to review existing text, look for the "Lawyer's Fallacy" (too many words masking the rule), ensure the K.I.S.S. (Keep It Simple, Stupid) principle is respected, and verify that important rules have clear, concrete examples.
