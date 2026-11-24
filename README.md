# Projet 4 · Échantillonnage et fenêtres glissantes

ISTIC, Master D3S · Nasr elhak Khemiri, Wajdi Zayoud, Youssif Cherni.

Le projet maintient des échantillons d’un flux de taille inconnue et estime le nombre d’événements lents ainsi que les quantiles de latence. Les quatre algorithmes sont écrits en Python. Les exemples utilisent des données synthétiques reproductibles.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
python demo.py --seed 42 --events 1200
python -m evaluation.benchmark --profile quick --output results/quick
python -m evaluation.benchmark --profile full
python -m streamlit run dashboard/app.py --server.address 127.0.0.1
```

- `algorithms/` contient Algorithm R, A-Res, DGIM, GK historique et les quantiles récents par blocs.
- `streaming/` gère les distributions synthétiques, les mises à jour et les alertes.
- `evaluation/`, `tests/` et `results/` contiennent le protocole, les tests et les preuves exportées.
- `dashboard/` fournit une vue locale interactive. `demo.py` exécute le même moteur en ligne de commande.
- `docs/` contient l’audit, les exercices, le rapport et la préparation de la soutenance.

La démo de référence signale l’incident à l’événement 403 et montre le rétablissement à 998. Le P99 historique reste élevé après l’incident, tandis que le P99 récent diminue. Le profil complet produit 14 figures et 6 758 lignes de mesures. Le test T1 donne p = 0,6422.

Voir [garanties](docs/MATHEMATICAL_GUARANTEES.md), [protocole](docs/EXPERIMENTAL_PROTOCOL.md), [résultats](docs/SCIENTIFIC_RESULTS.md), [revue scientifique](docs/STATE_OF_THE_ART_FINAL.md), [validation V3](docs/FINAL_VALIDATION_V3.md) et [guide de démonstration](docs/DEMONSTRATION_GUIDE.md).

Les études complémentaires `python -m evaluation.final_study` et `python -m evaluation.sensitivity` portent la collection à 21 figures. Le [rapport final](docs/report/rapport-projet4-final.pdf) se reproduit ensuite avec `python -m evaluation.article` ([prérequis LaTeX](docs/report/README.md)). Les scripts et exercices PDF sont produits par `python -m evaluation.academic_pdfs` avec ReportLab.

Voir les [supports de soutenance](presentation/README.md), le [journal de navigateur](results/browser_validation/report.json) et la [grille de conformité](docs/REQUIREMENTS_TRACEABILITY.md).
