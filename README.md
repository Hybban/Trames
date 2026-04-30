# TRAMES - Outils de Documentation

Ce projet contient les sources Markdown et les outils de génération pour créer un pdf à partir de ces sources.

## 🖋️ Philosophie de rédaction : Féminisation
Le projet suit une règle stricte de féminisation des termes techniques :
- **Personnes réelles (autour de la table)** : On utilise le féminin systématique (**la joueuse**, **la MJ**).
- **Fiction (personnages)** : Les personnages sont désignés comme des **héros** (masculin neutre pour la fiction).
- **Accords** : Veiller à ce que les adjectifs et déterminants suivent cette règle (ex: "la joueuse est épuisée").

## 📂 Structure du Projet
- `/Sources` : Les chapitres de base du système (générés sous forme de manuel complet).
- `/img` : Images et illustrations à intégrer aux documents.
- `/pdf_styles` : Les feuilles de style CSS (`base.css`, `theme_noir.css`, `theme_print.css`).
- `/scripts` : Outils d'automatisation Python.
- `/Générations` : Dossier de sortie des PDFs.

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

Pour générer le **Manuel Complet** :
```bash
python scripts/generate_srd.py
```

## 🎨 Standards Visuels
- **Format** : Les PDFs sont générés au format **A5** avec des marges de 1,5 cm pour une lecture optimale et un rendu adapté aux manuels de jeu de rôle.
- **Colonnes** : Mise en page sur deux colonnes (justifiée pour le texte `p`, alignée à gauche pour les titres et le gras). **Exception :** Les fichiers préfixés par `99_` (ex: `99_fiche_de_personnage.md`) sont automatiquement générés sur une seule colonne pleine largeur.
- **Sauts de page** : Automatiques avant chaque `h1` (sauf le premier du document) et avant chaque section en colonne unique (fichiers `99_`).
- **Encadrés** : Utiliser la syntaxe blockquote `> **Titre :** Contenu`. Vous pouvez également utiliser le préfixe `**Encadré** ` puis exécuter le script `python scripts/fix_encadres.py` pour formater automatiquement le bloc. Ils sont stylisés aux couleurs du jeu (bordure or).
- **Thèmes (Bleu et Or)** : Le design abandonne l'ancien rouge pour un thème Bleu et Or. Il est décliné en version Print/Base (fond blanc, bleu nuit profond) et Noir (fond anthracite "full bleed", bleu ciel et or vif).

## ⚠️ Notes de formatage Markdown
- **Listes** : Toujours laisser une **ligne vide** avant de commencer une liste (`*` ou `-`), sinon le rendu sera fusionné dans le paragraphe précédent.
- **Titres** : Commencer chaque fichier par un titre de niveau 1 (`#`) pour la page de garde automatique.
- **Images** : Utilisez la syntaxe Markdown classique (ex: `![Description](../img/image.jpg)`). Lors de la compilation, les scripts s'occupent d'embarquer (Base64) ces images directement dans le HTML. De plus, le style CSS contraint toujours l'image à la largeur de sa colonne afin d'éviter qu'elle ne soit coupée.

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
