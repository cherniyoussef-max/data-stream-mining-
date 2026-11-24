# Rapport scientifique

La source éditable est `main.tex`. Le document est composé en LaTeX avec Tectonic, la police Liberation Serif et une bibliographie BibTeX de 12 notices. Les graphiques proviennent de `results/figures/`, et la capture de Chrome de `presentation/screenshots/`. Pour rejouer depuis la racine, disposer de Tectonic et de `pdfinfo` (Poppler). Au premier lancement, Tectonic peut télécharger son bundle de paquets.

```bash
python -m evaluation.benchmark --profile full
python -m evaluation.final_study
python -m evaluation.sensitivity
python -m evaluation.alert_comparison
python -m evaluation.query_benchmark
python -m evaluation.article
```

Les mesures insérées dans le texte sont extraites des CSV et JSON dans `measurements.tex`. Le script contrôle le budget de six à huit pages avant de remplacer le PDF.
