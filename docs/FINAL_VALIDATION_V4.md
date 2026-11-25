# Validation finale du projet 4 · V4

Validation du 25 novembre 2026 pour `v1.0.0`, sur `codex/project4-release-v1.0.0`. Référence GitHub `3e79273` (V3), reprise de la V4 locale `9c3d7ca`. Les essais ont été rejoués sous Linux x86-64 avec Python 3.13.9 dans un nouvel environnement virtuel isolé. L’installation des deux fichiers de dépendances et `pip check` réussissent. Les versions du benchmark figurent dans [environment.json](../results/environment.json).

## Vérification et corrections

| Exécution | Résultat |
|---|---|
| V3 intacte dans l’environnement isolé | 86 réussites, 1 échec de chemin dans AppTest avec Streamlit 1.67.0 |
| V3 intacte avec Streamlit 1.51.0 | 87 réussites |
| V4, `python -m pytest -v` | 92 réussites en 7,18 s, dont 5 tests ajoutés depuis V3 |
| Démonstration CLI | Alerte à 403 et rétablissement à 998 |
| Benchmark rapide et complet | 2 710 et 6 758 lignes, zéro dépassement DGIM/GK dans chacun |
| Étude finale et sensibilité | 6 000 requêtes récentes, erreur maximale de 6 rangs et zéro dépassement, 12 configurations N/ε |
| Études appariées | 1 200 états comparés, 30 lignes de scores d’alerte |
| Chrome et Playwright | Intervalles de 0,6 et 2 s, pause, réinitialisation, avancement manuel, changement de paramètres, deux modes mémoire et téléchargement sans avancement, 500 lignes et zéro erreur console |
| PDF et PPTX | Huit pages inspectées et 12 DOI cliquables. 44 diapositives et 44 notes, 18 GIF identiques en octets à V4 et 99 images d’animation, titres des sept articles et résultats T1–T5 visibles en diapositive 35. Lecture des GIF extraits dans Chrome et ouverture du PPTX dans LibreOffice Impress |

Le test AppTest utilise désormais le chemin absolu construit à partir de son fichier. Aucune assertion V3 n’a été retirée. Les nouvelles propriétés couvrent entre autres la masse des rangs et les paires survivantes de GK, le modulo et les sous-fenêtres de DGIM, ainsi que les doublons, le démarrage et le bloc frontière des quantiles récents. Les journaux [V3](../results/pytest_baseline_v4.txt), [V4](../results/pytest_results.txt) et [Chrome](../results/browser_validation/report.json) contiennent les sorties observées.

## Garanties

- GK historique garde sa garantie de rang en εn avec les conventions discrètes. Le seuil de fusion est calculé exactement pour l’ε représenté en machine. La passe de droite à gauche protège les extrêmes, préserve la masse des gaps et interdit les paires encore fusionnables hors du minimum à la fin du balayage. Le comptage des paires anciennes, des tuples jeunes et des insertions entre deux balayages donne O(min(n, √(n/ε))) tuples. L’analyse suppose un ε fixe pendant le flux et un ordre stable des ex æquo. Elle compte des tuples et inclut le tampon à un facteur constant près. Les compteurs Python peuvent croître en taille avec log n. La borne logarithmique du GK classique reste hors de la garantie de cette variante.
- Pour la fenêtre récente, le budget de rang est u + C(S − 1), avec u valeurs périmées encore représentées, C blocs fermés et S le nombre maximal de valeurs par groupe. Le nombre d’entrées est au plus B − 1 + (⌈N/B⌉ + 1)⌈B/S⌉, avec B = ⌊√N⌋. Le tableau de bord affiche u et le budget courant. La FIFO exacte peut être désactivée.
- DGIM conserve sa borne relative de 50 % sur la fenêtre complète. Le benchmark a observé au maximum 33,33 % sur les cas échantillonnés.

Les démonstrations figurent dans [Fondements et garanties](MATHEMATICAL_GUARANTEES.md).

## Quantiles récents groupés

La requête P50/P95/P99 trie les représentants une fois et partage le parcours cumulatif. Les requêtes V3 et V4 utilisent les mêmes traces et configurations. Le tableau indique la médiane de cinq répétitions alternées. Le coût de mise à jour seule est commun aux deux chemins. Le débit mesure le moniteur complet avec ses requêtes. Le pic est l’allocation supplémentaire de la requête, mesurée avec `tracemalloc`. L’état persistant de la fenêtre ne change pas dans cette comparaison.

| N, ε | Mise à jour (ns) | Requête V3 → V4 (µs) | Débit V3 → V4 (év/s) | Pic V3 → V4 (octets) |
|---|---:|---:|---:|---:|
| 200, 0,01 | 276 | 57,4 → 25,6 | 13 770 → 25 975 | 4 120 → 3 656 |
| 1 000, 0,05 | 243 | 157,8 → 70,1 | 5 563 → 11 925 | 11 728 → 11 360 |
| 5 000, 0,05 | 234 | 489,1 → 205,8 | 1 873 → 4 389 | 27 960 → 27 592 |

À N=1 000 et ε=0,05, le gain local est de 2,25× contre 2,17× lors de la précédente exécution V4. Les chronométrages dépendent de la charge de la machine.

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

La [grille](REQUIREMENTS_TRACEABILITY.md) compte **25 PASS sur les 25 exigences obligatoires transmises** et **46 PASS, 1 PARTIAL et 1 OPTIONAL** dans la grille interne. R32 reste partiel. Le texte intégral de Gribelyuk a été retrouvé et la preuve a été contrôlée. Pour Xie, la [revue détaillée](ARTICLE_ANALYSIS_DETAILED.md) s’appuie sur le résumé primaire. Les latences et les incidents sont synthétiques. Les scripts donnent un minutage estimé de 4 min 54 s, 4 min 42 s et 4 min 47 s à partir du texte, des GIF et de la démonstration guidée. La lecture dans Microsoft PowerPoint et les durées mesurées avec les orateurs restent à vérifier.

Le commit de release descend de la V3 sur `main` et de la V4 validée. Les 92 tests réussissent aussi dans un clone local indépendant et après extraction du ZIP. Les fichiers extraits correspondent au commit. Les blobs du rapport (`ffe3ed27d9d7f44ce950361d388fbd4e67fd0acd`) et du PPTX (`433e6a4a739b1d68ad1f793cff05bdd3990823a1`) correspondent entre le commit, les fichiers locaux et le clone indépendant.

La branche et le tag annoté `v1.0.0` sont préparés localement. Le clone GitHub de la V4, la CI hébergée et la comparaison des blobs GitHub sont conditionnés à la publication. Le workflow GitHub Actions définit Python 3.11 et 3.13, les tests, le CLI et le profil rapide.

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
