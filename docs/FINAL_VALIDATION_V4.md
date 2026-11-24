# Validation finale du projet 4 · V4

Base `3e79273`, branche locale `codex/project4-final-v4`. Essais réalisés sous Linux x86-64 avec Python 3.13.9, dans un environnement virtuel isolé. Les versions du benchmark figurent dans [environment.json](../results/environment.json).

## Vérification et corrections

| Exécution | Résultat |
|---|---|
| V3 intacte dans l’environnement isolé | 86 réussites, 1 échec de chemin dans AppTest avec Streamlit 1.67.0 |
| V3 intacte avec Streamlit 1.51.0 | 87 réussites |
| V4, `python -m pytest -v` | 92 réussites, dont 5 nouveaux tests |
| Démonstration CLI | Alerte à 403 et rétablissement à 998 |
| Benchmark rapide et complet | 2 710 et 6 758 lignes, zéro dépassement DGIM/GK dans chacun |
| Étude finale et sensibilité | 6 000 requêtes récentes, erreur maximale de 6 rangs et zéro dépassement, 12 configurations N/ε |
| Études appariées | 1 200 états comparés, 30 lignes de scores d’alerte |
| Chrome et Playwright | Cadence, pause, reset, changement des paramètres, deux modes mémoire, contrôles manuels bloqués pendant la lecture et téléchargement sans avancement, 500 lignes et zéro erreur console |
| PDF et PPTX | Article de 8 pages, 44 diapositives et 44 notes, 18 GIF identiques à V3 et 99 images d’animation. Lecture des GIF extraits dans Chrome et ouverture du PPTX dans LibreOffice Impress |

Le test AppTest utilise désormais le chemin absolu construit à partir de son fichier. Aucune assertion V3 n’a été retirée. Les nouvelles propriétés couvrent entre autres la masse des rangs et les paires survivantes de GK, le modulo et les sous-fenêtres de DGIM, ainsi que les doublons, le démarrage et le bloc frontière des quantiles récents. Les journaux [V3](../results/pytest_baseline_v4.txt), [V4](../results/pytest_results.txt) et [Chrome](../results/browser_validation/report.json) contiennent les sorties observées.

## Garanties

- GK historique garde sa garantie de rang en εn avec la convention discrète aux extrémités. Le seuil de fusion est calculé exactement pour l’ε représenté en machine. La passe existante utilise O(min(n, √(n/ε))) tuples. La preuve compte les gaps des paires anciennes et le nombre de nouvelles insertions. La borne logarithmique du GK classique reste hors de la garantie de cette variante.
- Pour la fenêtre récente, le budget de rang est u + C(S − 1), avec u valeurs périmées encore représentées, C blocs fermés et S le nombre maximal de valeurs par groupe. Le nombre d’entrées est au plus B − 1 + (⌈N/B⌉ + 1)⌈B/S⌉, avec B = ⌊√N⌋. Le tableau de bord affiche u et le budget courant. La FIFO exacte peut être désactivée.
- DGIM conserve sa borne relative de 50 % sur la fenêtre complète. Le benchmark a observé au maximum 33,33 % sur les cas échantillonnés.

Les démonstrations figurent dans [Fondements et garanties](MATHEMATICAL_GUARANTEES.md).

## Quantiles récents groupés

La requête P50/P95/P99 trie les représentants une fois et partage le parcours cumulatif. Les requêtes V3 et V4 utilisent les mêmes traces et configurations. Le tableau indique la médiane de cinq répétitions alternées. Le coût de mise à jour seule est commun aux deux chemins. Le débit mesure le moniteur complet avec ses requêtes. Le pic est l’allocation supplémentaire de la requête, mesurée avec `tracemalloc`. L’état persistant de la fenêtre ne change pas dans cette comparaison.

| N, ε | Mise à jour (ns) | Requête V3 → V4 (µs) | Débit V3 → V4 (év/s) | Pic V3 → V4 (octets) |
|---|---:|---:|---:|---:|
| 200, 0,01 | 281 | 62,0 → 27,4 | 13 086 → 24 738 | 4 120 → 3 656 |
| 1 000, 0,05 | 272 | 161,6 → 74,4 | 5 243 → 11 560 | 11 728 → 11 360 |
| 5 000, 0,05 | 240 | 495,6 → 210,9 | 1 893 → 4 386 | 27 960 → 27 592 |

[Mesures et répétitions brutes](../results/query_benchmark.json)

## Alertes

La règle facultative utilise les seuils de médiane et de P99 de la référence. Elle exige aussi au moins 15 % d’événements estimés au-dessus de 90 ms sur les 50 dernières positions au maximum et trois décisions concordantes. Même scénario et même graine pour chaque paire. Le tableau présente le F1 moyen face aux incidents annotés pour les graines 42, 204 et 313.

| Scénario | Seuil initial | Persistance |
|---|---:|---:|
| Référence | 0,800 | 0,935 |
| Graduel | 0,785 | 0,848 |
| Répété | 0,345 | 0,791 |
| Isolé | 0,036 | 0,000 |
| Sous le seuil | 0,000 | 0,000 |

À la graine 42, les faux positifs du scénario répété passent de 845 à 88, et les faux négatifs de 6 à 22. Sur le scénario de référence, le délai de détection passe de 2 à 11 événements et celui de rétablissement de 197 à 43. La référence par seuil exact indique à quel point l’approximation reproduit une règle, tandis que les étiquettes mesurent sa capacité à détecter les incidents. L’accord de la règle initiale avec son seuil exact va de 99,67 % à 100 % à la graine 42. Les deux politiques échouent sous le seuil, et la persistance rate le pic isolé.

[Précision, rappel, confusion par graine](../results/alert_comparison.csv) · [Délais par épisode](../results/alert_episode_delays.csv) · [Figure](../results/figures/22_alertes_strategies.png)

## Portée et traçabilité

La [grille](REQUIREMENTS_TRACEABILITY.md) compte **46 PASS, 1 PARTIAL et 1 OPTIONAL**. R32 reste partiel. Les notices primaires de Gribelyuk et de Xie ont été contrôlées, et les détails qui nécessitent les textes intégraux ou des artefacts non accessibles restent signalés dans la [revue détaillée](ARTICLE_ANALYSIS_DETAILED.md). Les latences et les incidents sont synthétiques. La variante GK existante a été conservée et la comparaison avec une autre implémentation fidèle à l’algorithme original reste ouverte. La lecture dans Microsoft PowerPoint et la CI hébergée sont à vérifier. Le workflow GitHub Actions définit Python 3.11 et 3.13, les tests, le CLI et le profil rapide.

## Reproduction

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt -r requirements-academic.txt
python -m pytest -v
python demo.py
python -m evaluation.benchmark --profile quick
python -m evaluation.benchmark --profile full
python -m evaluation.final_study
python -m evaluation.sensitivity
python -m evaluation.alert_comparison
python -m evaluation.query_benchmark
python -m evaluation.article
python -m evaluation.academic_pdfs
```

Voir le [README](../README.md) pour lancer la validation du navigateur et les [instructions de soutenance](../presentation/README.md) pour la reconstruction du PPTX.
