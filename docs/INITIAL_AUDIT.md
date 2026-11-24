# Audit initial

Branche main, commit `60bbda1`, arbre propre. Origine SSH `naseroz/dtata-stream-mining`.
Python 3.13.9, pytest 9.2.0, SciPy 1.16.3, Matplotlib 3.10.6, Streamlit 1.51.0.
Sources : `test_projet4.py` (quatre algorithmes), `demo.py` (trois points d'entrée et deuxième GK),
`tests.py` (quatre tests), `Note.txt` (notes d'équipe), deux fichiers bytecode suivis.

| Exigence | Résultat initial et correction |
|---|---|
| R / T1 | P0 : graines globales, k non validé. Garder Algorithm R, isoler le RNG. |
| A-Res / T2 | P0 : clés instables aux poids extrêmes, recherche O(k), pas de validation. Tas et transformation monotone. |
| DGIM / T3–T4 | P0 : N=1 avec [1] renvoie 0. Pas de contrôle des invariants. Corriger le singleton et vérifier chaque insertion. |
| GK / T5 | P0 : données 1 à 100, ε=.001, médiane 52 au lieu du rang 50. Compression espacée de 1000 événements et bornes incorrectes. |
| Quantiles récents et alerte | P0 : deuxième GK sans compression dans la démo, alerte historique sans récupération. Construire une fenêtre approchée indépendante. |
| Expériences et figures | P1 : aucun pipeline. Exporter mesures et figures reproductibles. |
| Interface et documentation | P2 : aucune interface, aucun README ni rapport. Consolider les entrées et documenter. |
| Extensions | P3 : KLL, t-digest et échantillonnage à récence non prioritaires. |

`python -m pytest -q` : zéro collecte. `python -m pytest -q tests.py` : 4 réussites.
`python demo.py` : succès, alerte à t=1000, exemple DGIM exact 100 / estimé 109.
Le P99 de la démo varie entre exécutions en l'absence de graine locale contrôlée.
