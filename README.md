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

### 📝 Modifications récentes et impacts (Session en cours)
- **Génération automatique d'une Table des matières (TOC) interactive** :
  - **Algorithme double-passe robuste** : Le moteur de rendu `pdf_generator_core.py` effectue désormais un premier rendu temporaire (brouillon) pour analyser la pagination réelle des titres `h1` via `PyMuPDF`, puis injecte une table des matières rigoureusement paginée lors de la seconde passe.
  - **Esthétique premium adaptative** : Ajout d'une mise en page raffinée avec pointillés extensibles (dot leaders) reliant chaque chapitre à sa page. La table des matières hérite dynamiquement de la charte graphique et des couleurs du thème actif (Noir, Print, ou thèmes spécifiques des suppléments).
  - **Multilingue et interactive** : Titrage dynamique en français (`Table des matières`) ou anglais (`Table of Contents`), avec des hyperliens PDF internes cliquables facilitant la navigation.
- **Mise à jour complète des terminologies de Blessures et du Fuseau** :
  - **Feuilles de personnages HTML (vierges & exemples / avec ou sans fond)** : 
    - Mise à jour de `trames_fiches_vierges.html` et `trames_fiches_personnages.html` avec les nouveaux termes (**Le Fuseau des Moires**, **La Réserve du Fuseau**, **État de Santé**, **Blessures Légères/Graves/Mortelles**), et nettoyage structurel complet (retrait des sections obsolètes *Trame Brûlée* et *Notes* sur les fiches vierges).
    - Création des fiches alternatives **sans couleur de fond** (`trames_fiches_vierges_print.html` et `trames_fiches_personnages_print.html`) dotées de bordures élégantes, idéales pour l'impression domestique afin d'économiser l'encre des joueuses.
    - Compilation automatisée par Playwright de l'ensemble des 4 versions en PDF A4 vectoriel haute fidélité.
  - **Système de Blessures** : Remplacement de "Fil Effiloché" par **Blessure Légère**, "Fil Tendu" par **Blessure Grave**, "Fil à la Limite" par **Blessure Mortelle**, et de "Solidité du Fil" par **État de Santé** (avec correction des accords de genre féminin et pluriels associés) dans tous les fichiers sources Markdown et aides de jeu.
  - **Réserve du Fuseau** : Remplacement dramatique de "Le Métier des Moires" par **Le Fuseau des Moires**, "La Réserve du Métier" par **La Réserve du Fuseau**, et de "point du métier" / "jeton du Métier" par **point du fuseau** / **jeton du Fuseau**.
  - **Le Fuseau** : Remplacement de "Le Métier à Tisser" par simplement **Le Fuseau** pour éviter l'anachronisme avec les métaphores de la fileuse.
- **Harmonisation et nomenclature de la manœuvre "Nouer un Fil"** :
  - Renommage de l'ancienne formulation "Tisser un nouveau Fil" par **"Nouer un Fil"** dans les exemples de jeu (`03_Les_scènes.md`) et dans les fiches récapitulatives (`99_recapitulatifs.md`).
  - Alignement complet des conséquences mécaniques de "Nouer un Fil" (création de plans, liens, alliances ou solutions avec réussites totale 9-12, partielle avec coût 5-8 et échec 1-4) au lieu de l'explication obsolète liée à la dépense d'une ressource.
  - Remplacement dans l'exemple de Jaxx de "Tisser un nouveau Fil" par **Tendre le Fil** (manœuvre défensive cohérente avec la stabilisation du panneau face à une menace d'implosion).
  - Validation automatique par recherche de sécurité (0 occurrence résiduelle de l'ancienne formulation).
- **Prise en charge de la balise URL dynamique cliquable** :
  - Support dans le moteur de rendu `pdf_generator_core.py` du format de balise `[URL="texte à afficher dans le pdf"][lien url complet]` (avec ou sans guillemets optionnels) pour l'intégration de liens hypertextes actifs et cliquables lors de la génération PDF par Playwright.
  - Stylisation des hyperliens (`a`) dans `base.css` utilisant le bleu ardoise du thème (`--accent-color`) et le souligné d'hyperlien classique.
  - Mise en application dans `00_Introduction.md` pour un lien cliquable renvoyant vers l'article sur la sécurité émotionnelle.
- **Restauration et perfectionnement des signets/bookmarks PDF** :
  - Modification de `pdf_generator_core.py` pour supprimer la conversion des titres `h3` à `h6` en balises `div`, permettant à Playwright/Chromium d'inclure la totalité des titres dans l'outline (sommaire interactif) des PDFs générés.
- **Réorganisation des chapitres de règles** :
  - Le Chapitre II (`02_Mecanique_de_Resolution.md`) regroupe désormais la mécanique de base, les **Manœuvres Fondamentales** (*Tendre le Fil*, *Lire la Trame*, *Couper le Fil*, *Nouer un Fil*) et les **Actions Collectives** (structure, lancer commun et table des conséquences) pour une référence facilitée côté joueurs.
  - Le Chapitre V (`05_Outils_de_la_meneuse.md`) est exclusivement centré sur la Meneuse de jeu et s'enrichit de deux nouvelles sections majeures : **La Question Ouverte** (II.5 déplacé ici pour plus de cohérence), **Conseils de Cadrage** (découpage de scènes, sécurité émotionnelle à la table) et **Préparer et Développer un Scénario**.
- **Nettoyage typographique complet (Tirets cadratifs)** : Retrait de l'ensemble des tirets cadratifs (`—`) dans tous les fichiers Markdown sources français au profit d'une ponctuation sémantique plus fluide et rigoureuse (virgules doubles pour les incises, deux-points et points-virgules).
- **Optimisation Extrême de la taille des PDFs (JPEG + tagged=True + PyMuPDF)** :
  - **Images & Logos** : Remplacement de la compression WebP par une compression **JPEG (qualité 70)** avec conversion automatique RVB pour toutes les images opaques. Cela permet au moteur de rendu Chromium d'injecter nativement les images dans le PDF (`/Filter /DCTDecode`) sans devoir les décompresser en bitmaps bruts stockés sous format PNG/FlateDecode lourd. Le poids des 7 illustrations du livre anglais dans le PDF est réduit de **92%** (passant de 2 045 Ko à seulement 160 Ko).
  - **Structure & Accessibilité** : Activation de l'accessibilité (`tagged=True`), assurant la bonne capture des outlines/bookmarks par Playwright et PyMuPDF tout en optimisant la structure.
  - **Polices & Nettoyage final** : Utilisation des polices système élégantes (Century Gothic, Garamond) et traitement par `pymupdf` (`fitz`) pour fusionner les ressources dupliquées. Les livres de base descendent ainsi à seulement **0.63 Mo / 649 Ko** (FR) et **0.70 Mo / 714 Ko** (EN) !
- **Retrait complet de la mention "SRD"** : Remplacement par "Livre de base" (fr) et "Core Rulebook" (en) dans l'ensemble des sources Markdown, documentations et scripts.
- **Renommage du script principal** : Le script de génération du livre de base `generate_srd.py` a été renommé en `generate_base.py`.
- **Nouveaux noms de PDFs générés** : Les PDFs générés pour le Livre de base s'appellent désormais `Trames_Livre_de_base_[Theme]_FR.pdf` (FR) et `Threads_Core_Rulebook_[Theme]_EN.pdf` (EN).
- **Amélioration visuelle des couvertures** :
  - Centrage horizontal automatique de tous les titres de couverture (notamment ceux sur plusieurs lignes tels que `Trames d'ombres` et `Trames d'ombres Solo`) via l'ajout de `text-align: center` dans `base.css`.
  - Affichage précis du type de document sur la couverture des suppléments ("Supplément Solo", "Supplément d'univers") plutôt que "Livre de base".
- **Renommage et alignement de la gamme Solo** : Les titres du Mode Solo ont été harmonisés en `"Trames Mode solo"` (FR) et `"Threads Solo Mode"` (EN) sur les couvertures et dans l'arborescence de génération.

## 📂 Structure du Projet

```
Trames/
├── Sources_fr/                          # Sources françaises (Livre de base)
│   ├── 00_Introduction.md
│   ├── 01_Creation.md
│   ├── 02_Mecanique_de_Resolution.md
│   ├── 03_Les_scènes.md
│   ├── 04_Sante_et_Blessures.md
│   ├── 05_Outils_de_la_meneuse.md
│   ├── 06_Evolution_du_Personnage.md
│   ├── 90_creation_groupe_fil_de_lin.md
│   ├── 91_creation_groupe_fil_de_laine.md
│   ├── 92_creation_groupe_fil_de_soie.md
│   ├── 99_recapitulatifs.md
│   └── Suppléments/
│       ├── La Ville des Fils Perdus/     # Supplément d'univers historique/mystère (A City of Severed Thread)
│       ├── Mode solo/                   # Le Fil Solitaire (6 chapitres)
│       ├── Trames d'ombres/             # Supplément d'univers urban fantasy
│       │   └── 01-Trames_d'Ombres-setting.md
│       └── Trames d'ombres Solo/        # Solo pour Trames d'ombres
│
├── Sources_en/                          # Sources anglaises (Livre de base)
│   ├── 00_Introduction.md
│   ├── 01_Creation.md
│   ├── 02_Resolution_Mechanic.md
│   ├── 03_Health_and_Wounds.md
│   ├── 04_Maneuvers_and_Obstacles.md
│   ├── 05_Character_Advancement.md
│   ├── 99_character_sheet.md
│   └── Suppléments/
│       ├── Solo Mode/                   # The Solitary Thread (6 chapters)
│       ├── Shadow Threads/              # Shadow Threads setting (EN)
│       │   └── 01–06 (6 chapitres .md)
│       └── Shadow Threads Solo/         # Solo for Shadow Threads
│
├── pdf_styles/                          # Styles CSS
│   ├── base.css                         # Style global partagé
│   ├── theme_noir.css                   # Thème de base (Noir)
│   ├── theme_print.css                  # Thème de base (Print)
│   └── Suppléments/                     # Thèmes des suppléments
│       ├── La Ville des Fils Perdus/
│       ├── Mode solo/
│       ├── Trames d'ombres/
│       └── Trames d'ombres Solo/
│
├── scripts/                             # Outils d'automatisation
│   ├── generate_base.py                  # Générateur principal de PDFs
│   ├── fix_encadres.py                  # Formateur d'encadrés Markdown
│   └── requirements.txt
│
└── Générations/                         # Sortie (PDFs générés)
    ├── fr/
    │   ├── Trames_Livre_de_base_Noir_FR.pdf
    │   ├── Trames_Livre_de_base_Print_FR.pdf
    │   ├── La Ville des Fils Perdus/
    │   ├── Trames Mode solo/
    │   ├── Trames d'ombres/
    │   └── Trames d'ombres Solo/
    └── en/
        ├── Threads_Core_Rulebook_Noir_EN.pdf
        ├── Threads_Core_Rulebook_Print_EN.pdf
        ├── Threads Solo Mode/
        ├── Shadow Threads/
        └── Shadow Threads Solo/
```

## 🛠️ Outils techniques
Le rendu est géré par **Playwright (Chromium)** pour garantir un support parfait du CSS3 (colonnes, fonds perdus, polices Google Fonts).

### Dépendances
- Python 3.x
- `playwright`, `markdown2`, `pymupdf`

### Commandes de génération
Avant la première utilisation :
```bash
pip install -r scripts/requirements.txt
playwright install chromium
```

Pour générer les ouvrages individuellement (dans toutes les langues disponibles) :
- **Livre de base** :
```bash
python scripts/generate_base.py
```
- **Mode Solo** :
```bash
python scripts/generate_solo.py
```
- **Trames d'ombres** :
```bash
python scripts/generate_trames_d_ombres.py
```
- **Trames d'ombres Solo** :
```bash
python scripts/generate_trames_d_ombres_solo.py
```
- **La Ville des Fils Perdus** :
```bash
python scripts/generate_la_ville_des_fils_perdus.py
```

Pour générer **tous les ouvrages** d'un coup :
```bash
python scripts/generate_all.py
```

## Traductions
Quand les fichiers du répertoire `Sources_fr` sont modifiés, il faut mettre à jour les fichiers du répertoire `Sources_en`.

## 🎨 Standards Visuels
- **Format** : Les PDFs sont générés au format **A5** avec des marges de 1,5 cm pour une lecture optimale et un rendu adapté aux manuels de jeu de rôle.
- **Colonnes** : Mise en page sur une seule colonne, justifiée pour le texte `p`, alignée à gauche pour les titres et le gras. 
- **Sauts de page** : Automatiques avant chaque `h1` (sauf le premier du document).
- **Encadrés** : Utiliser la syntaxe blockquote `> **Titre :** Contenu`. Vous pouvez également utiliser le préfixe `**Encadré** ` puis exécuter le script `python scripts/fix_encadres.py` pour formater automatiquement le bloc. Ils sont stylisés aux couleurs du jeu (bordure or).
- **Thèmes (Bleu et Or)** : Le design abandonne l'ancien rouge pour un thème Bleu et Or. Il est décliné en version Print/Base (fond blanc, bleu nuit profond) et Noir (fond anthracite "full bleed", bleu ciel et or vif).
- **Thèmes des suppléments** : Les suppléments possèdent des thèmes personnalisés. *Trames d'ombres* utilise un thème **Gris et Turquoise**, le *Mode solo* (Le Fil Solitaire) utilise un thème **Vert**, *Trames d'ombres Solo* un thème **Carmin**, et *La Ville des Fils Perdus* un thème **Laiton et Anthracite / Parchemin et Bronze**. Ils sont tous déclinés en version Print/Base et Noir.

## ⚠️ Notes de formatage Markdown
- **Listes** : Toujours laisser une **ligne vide** avant de commencer une liste (`*` ou `-`), sinon le rendu sera fusionné dans le paragraphe précédent.
- **Titres** : Commencer chaque fichier par un titre de niveau 1 (`#`) pour la page de garde automatique.
- **Sauts de page manuels** : Insérer le tag `--pb--` seul sur une ligne (entouré de lignes vides) pour forcer un saut de page dans le PDF généré.
- **Images** : Pour intégrer une illustration dans le texte, utilisez la syntaxe Markdown standard `![Nom](Images/Trames/Image.png)` ou le raccourci `[IMG](Images/Trames/Image.png)`. Les images du dossier `Images/Trames/` seront encodées en Base64 et intégrées automatiquement au PDF généré sans erreur de chemin.

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
