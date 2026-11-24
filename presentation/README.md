# Soutenance

Le PowerPoint comporte 44 diapositives et 18 GIF intégrés. En mode Diaporama, laisser dérouler le GIF puis avancer d’une diapositive. Les notes indiquent les états à commenter. Les visualisations scientifiques viennent de `results/figures/`. Les captures proviennent du test local Chrome.

Le dossier contient les sources éditables `build.mjs`, `slides.json` et `QUESTIONS.md`. Le PDF statique montre la dernière image de chaque animation. Prévoir environ cinq minutes par orateur, hors démonstration libre et questions.

Pour une version courte, s’appuyer sur le PDF statique ou ne commenter que l’état final, résumer les sept études avec le tableau comparatif et montrer la décision exacte puis le rétablissement. Pour la démo, ouvrir la fenêtre de 200 positions, avancer un événement, puis un lot. Démarrer et mettre en pause pour montrer la cadence. Forcer un incident et avancer par lots jusqu’à l’alerte. Revenir à la normale et avancer jusqu’au retour. Exporter le CSV.

### Recompiler

Depuis la racine, installer les dépendances du projet, Pillow et ReportLab. Le générateur des GIF utilise DejaVu Sans. La source des diapositives nécessite Node et le module `@oai/artifact-tool` fourni par le runtime Codex. Copier `presentation/build.mjs` dans un répertoire de travail qui résout ce module, puis exécuter Node depuis la racine du dépôt en lui donnant le chemin du PPTX temporaire d’affiches.

```bash
python -m presentation.animations.generate
node /chemin/build.mjs /chemin/posters.pptx
python -m presentation.embed_gifs /chemin/posters.pptx
libreoffice --headless --convert-to pdf --outdir /chemin /chemin/posters.pptx
python -m evaluation.academic_pdfs
```

Renommer le PDF d’affiches en `Data_Stream_Mining_Final_Statique.pdf`. Pour une révision des textes ou des figures, réutiliser les GIF et affiches du dépôt. Le commutateur `--browser` du module d’incorporation vérifie aussi la lecture des GIF extraits avec Playwright et Chrome. Sans le module Codex, ouvrir et modifier le PPTX livré dans un éditeur compatible, ou présenter le PDF statique. Voir [le détail de la validation](ANIMATION_VALIDATION.md).
