# TRAMES - Outils de Documentation

Ce projet contient les sources Markdown et les outils de génération pour créer des pdf à partir de ces sources.

## 🖋️ Philosophie de rédaction : Féminisation
Le projet suit une règle stricte de féminisation des termes techniques :
- **Personnes réelles (autour de la table)** : On utilise le féminin systématique (**la joueuse**, **la MJ**).
- **Fiction (personnages)** : Les personnages sont désignés comme des **héros** (masculin neutre pour la fiction).
- **Accords** : Veiller à ce que les adjectifs et déterminants suivent cette règle (ex: "la joueuse est épuisée").

## Gestion du projet
- Quand on ajoute un nouveau supplément, il faut ajouter le sous-dossier correspondant dans le dossier `Sources_fr/Suppléments` et `Sources_en/Suppléments`.
- Quand des modifications ont été validées, il faut noter les impacts dans le fichier README.md.

## 📂 Structure du Projet

```
Trames/
├── Sources_fr/                          # Sources françaises (SRD)
│   ├── 01_Introduction_et_Creation.md
│   ├── 02_Mecanique_de_Resolution.md
│   ├── 03_Sante_et_Blessures.md
│   ├── 04_Manoeuvres_et_Obstacles.md
│   ├── 05_Evolution_du_Personnage.md
│   ├── 99_fiche_de_personnage.md
│   └── Suppléments/
│       ├── Mode solo/                   # Le Fil Solitaire (6 chapitres)
│       ├── Trames d'ombres/             # Supplément d'univers urban fantasy
│       │   ├── 01-Trames_d'Ombres-setting.md
│       │   ├── theme_noir.css           # Thème CSS custom
│       │   └── theme_print.css
│       └── Trames d'ombres Solo/        # Solo pour Trames d'ombres
│
├── Sources_en/                          # Sources anglaises (SRD)
│   ├── 01_Introduction_and_Creation.md
│   ├── 02_Resolution_Mechanic.md
│   ├── 03_Health_and_Wounds.md
│   ├── 04_Maneuvers_and_Obstacles.md
│   ├── 05_Character_Advancement.md
│   ├── 99_character_sheet.md
│   └── Suppléments/
│       ├── Solo Mode/                   # The Solitary Thread (6 chapters)
│       ├── Shadow Threads/              # Shadow Threads setting (EN)
│       │   ├── 01–06 (6 chapitres .md)
│       │   ├── theme_noir.css
│       │   └── theme_print.css
│       └── Shadow Threads Solo/         # Solo for Shadow Threads
│
├── pdf_styles/                          # Styles CSS globaux
│   ├── base.css
│   ├── theme_noir.css
│   └── theme_print.css
│
├── scripts/                             # Outils d'automatisation
│   ├── generate_srd.py                  # Générateur principal de PDFs
│   ├── fix_encadres.py                  # Formateur d'encadrés Markdown
│   └── requirements.txt
│
└── Générations/                         # Sortie (PDFs générés)
    ├── fr/
    │   ├── Trames_SRD_Noir_FR.pdf
    │   ├── Trames_SRD_Print_FR.pdf
    │   ├── Mode solo/
    │   ├── Trames d'ombres/
    │   └── Trames d'ombres Solo/
    └── en/
        ├── Threads_SRD_Noir_EN.pdf
        ├── Threads_SRD_Print_EN.pdf
        ├── Solo Mode/
        ├── Shadow Threads/
        └── Shadow Threads Solo/
```

## 🛠️ Outils techniques
Le rendu est géré par **Playwright (Chromium)** pour garantir un support parfait du CSS3 (colonnes, fonds perdus, polices Google Fonts).

### Dépendances
- Python 3.x
- `playwright`, `markdown2`

### Commandes de génération
Avant la première utilisation :
```bash
pip install -r scripts/requirements.txt
playwright install chromium
```

Pour générer le **Manuel Complet** (dans toutes les langues disponibles) :
```bash
python scripts/generate_srd.py
```

## Traductions
Quand les fichiers du répertoire `Sources_fr` sont mis à jour, il faut mettre à jour les fichiers du répertoire `Sources_en`.

## 🎨 Standards Visuels
- **Format** : Les PDFs sont générés au format **A5** avec des marges de 1,5 cm pour une lecture optimale et un rendu adapté aux manuels de jeu de rôle.
- **Colonnes** : Mise en page sur une seule colonne, justifiée pour le texte `p`, alignée à gauche pour les titres et le gras. 
- **Sauts de page** : Automatiques avant chaque `h1` (sauf le premier du document).
- **Encadrés** : Utiliser la syntaxe blockquote `> **Titre :** Contenu`. Vous pouvez également utiliser le préfixe `**Encadré** ` puis exécuter le script `python scripts/fix_encadres.py` pour formater automatiquement le bloc. Ils sont stylisés aux couleurs du jeu (bordure or).
- **Thèmes (Bleu et Or)** : Le design abandonne l'ancien rouge pour un thème Bleu et Or. Il est décliné en version Print/Base (fond blanc, bleu nuit profond) et Noir (fond anthracite "full bleed", bleu ciel et or vif).
- **Thèmes des suppléments (Gris et Turquoise)** : Le design abandonne l'ancien rouge pour un thème Gris et Turquoise. Il est décliné en version Print/Base (fond blanc, gris foncé) et Noir (fond anthracite "full bleed", gris foncé et turquoise vif).

## ⚠️ Notes de formatage Markdown
- **Listes** : Toujours laisser une **ligne vide** avant de commencer une liste (`*` ou `-`), sinon le rendu sera fusionné dans le paragraphe précédent.
- **Titres** : Commencer chaque fichier par un titre de niveau 1 (`#`) pour la page de garde automatique.
- **Sauts de page manuels** : Insérer le tag `--pb--` seul sur une ligne (entouré de lignes vides) pour forcer un saut de page dans le PDF généré.

## 🔧 Dépannage
- **PermissionError lors de la génération** : Si le script affiche une erreur mentionnant que la permission est refusée pour un fichier PDF, c'est généralement parce que vous avez laissé le PDF ouvert dans votre lecteur (Acrobat, navigateur, etc.). Fermez-le simplement et relancez le script.

## 💾 Gestion de Versions (Git)
Le projet est versionné avec Git. Le fichier `.gitignore` est configuré pour exclure automatiquement les PDFs du dossier `Générations` ainsi que les fichiers temporaires Python. 

Pour lier votre dépôt local à GitHub :
```bash
git branch -M main
git remote add origin https://github.com/votre-pseudo/TRAMES-RPG.git
git push -u origin main
```

---
*Projet maintenu avec l'aide d'Antigravity.*
