# Traçabilité du projet 4

## Cahier des charges enseignant

Les 25 exigences ci-dessous sont celles de la liste obligatoire transmise avec la demande de version finale. Les références R renvoient à la grille interne.

| Nº | Exigence obligatoire | Preuve | Statut |
|---|---|---|---|
| E01 | Algorithm R implémenté directement | R1, `Reservoir.add`, méthode R en une passe | PASS |
| E02 | Preuve d’inclusion k/n | R10, admission et produit de survie | PASS |
| E03 | A-Res implémenté directement | R2, `WeightedReservoir.add`, tas et priorités | PASS |
| E04 | Clé U^(1/w) et loi pondérée correcte | R11, ordre équivalent des clés logarithmiques et course exponentielle sans remise | PASS |
| E05 | Landmark, tumbling, glissante et décroissance | R6–R9, définitions, exemples et diapositives 8–11 | PASS |
| E06 | DGIM implémenté directement | R3, groupes, fusions et expiration dans `algorithms/dgim.py` | PASS |
| E07 | Erreur relative maximale DGIM de 50 % | R12, preuve du groupe frontière et comparaison à l’oracle | PASS |
| E08 | Représentation DGIM compacte en O(log² N) bits | R12, O(log N) groupes et O(log N) bits par groupe dans le modèle compact | PASS |
| E09 | GK implémenté directement | R4, insertion, compression et requête dans `algorithms/quantiles.py` | PASS |
| E10 | Garantie de rang GK et conventions discrètes | R13, cible qn, rang admissible le plus proche au démarrage, ex æquo et extrêmes | PASS |
| E11 | Interfaces publiques requises préservées | R5, réexports historiques, signatures et tests de compatibilité | PASS |
| E12 | T1, n=100, k=10, 10 000 tirages | R14, `uniform_trial`, χ²=93,316 et p=0,642188 | PASS |
| E13 | T2, inclusions pondérées | R15, essais pour k=1, 2 et comparaison indépendante pour k plus grand | PASS |
| E14 | T3, comparaison au compteur exact à chaque insertion | R16, oracle FIFO des tests exhaustifs et adverses | PASS |
| E15 | T4, invariants et croissance logarithmique | R17, tailles, ordre, modulo, au plus 2·bit_length(N) groupes | PASS |
| E16 | T5, garanties de rang | R18, cinq ε, huit quantiles intérieurs, extrêmes, répétitions et ordre adverse | PASS |
| E17 | Médiane et P99 exacts et approchés | R20–R21, figures 06 et 07, CSV et oracle | PASS |
| E18 | Plusieurs tailles de fenêtre | R19 et R44, cinq N du profil complet et étude jusqu’à N=50 000 | PASS |
| E19 | Flux uniformes, gaussiens et changeants | R22–R24, générateurs et essais | PASS |
| E20 | Application concrète de surveillance des latences | R25, démonstration CLI et Streamlit rejoués | PASS |
| E21 | Alerte de seuil | R26, alerte à 403 et retour à 998 dans le scénario de référence | PASS |
| E22 | Exemples manuels pour les quatre algorithmes | R29, exercices corrigés et animations associées | PASS |
| E23 | Résultats statistiques | R14–R15 et résultats CSV/JSON exportés | PASS |
| E24 | Figures comparant erreur et garantie | R28, figures 04, 05 et 08 | PASS |
| E25 | Rapport scientifique de six à huit pages | R31, rendu LaTeX de huit pages inspecté | PASS |

**Bilan enseignant · 25 PASS sur 25 exigences obligatoires transmises.**

## Grille interne et extensions V4

| ID | Exigence | Implémentation ou chapitre | Validation ou preuve | Statut |
|---|---|---|---|---|
| R1 | Algorithm R | algorithms/sampling.py | T1 + preuve d’inclusion | PASS |
| R2 | A-Res | algorithms/sampling.py | T2, poids extrêmes | PASS |
| R3 | DGIM | algorithms/dgim.py | T3–T4 | PASS |
| R4 | GK | algorithms/quantiles.py | T5, compression par invariants | PASS |
| R5 | Interfaces publiques | test_projet4.py | compatibilité et ancienne suite | PASS |
| R6 | Landmark | MATHEMATICAL_GUARANTEES.md | explication et exemple | PASS |
| R7 | Tumbling | MATHEMATICAL_GUARANTEES.md | explication et exemple | PASS |
| R8 | Glissante | MATHEMATICAL_GUARANTEES.md | explication et exemple | PASS |
| R9 | Décroissance exponentielle | MATHEMATICAL_GUARANTEES.md | définition et formule | PASS |
| R10 | Preuve R | MATHEMATICAL_GUARANTEES.md | remplissage et survie | PASS |
| R11 | Explication A-Res | MATHEMATICAL_GUARANTEES.md | course exponentielle | PASS |
| R12 | Garantie DGIM | MATHEMATICAL_GUARANTEES.md | preuve, T3–T4 | PASS |
| R13 | Garantie de rang GK | MATHEMATICAL_GUARANTEES.md | preuve et convention discrète | PASS |
| R14 | T1 | tests/test_project.py | statistical_results.json | PASS |
| R15 | T2 | tests/test_project.py | statistical_results.json | PASS |
| R16 | T3 | tests/test_project.py | oracle à chaque insertion | PASS |
| R17 | T4 | tests/test_project.py | invariants et modulo | PASS |
| R18 | T5 | tests/test_project.py | huit q et cinq ε | PASS |
| R19 | Tailles DGIM | evaluation/benchmark.py | N jusqu’à 10 000 | PASS |
| R20 | Médiane | evaluation/benchmark.py | figure 06 | PASS |
| R21 | P99 | evaluation/benchmark.py | figure 07 | PASS |
| R22 | Uniforme | streaming/generators.py | T5 et benchmark | PASS |
| R23 | Gaussienne | streaming/generators.py | T5 et benchmark | PASS |
| R24 | Dérive | streaming/generators.py | alerte, figure 12 | PASS |
| R25 | Surveillance | dashboard/app.py, demo.py | test Streamlit et CLI | PASS |
| R26 | Alertes | streaming/engine.py | transitions, figure 13 | PASS |
| R27 | Quantiles récents | algorithms/quantiles.py | borne d’insertion, figure 14 | PASS |
| R28 | Figures des bornes | evaluation/plotting.py | figures 04, 05, 08 | PASS |
| R29 | Exercices | MANUAL_EXERCISES.md | quatre traces canoniques et un exemple de blocs | PASS |
| R30 | Reproductibilité | README.md | tests, CLI et deux profils exécutés | PASS |
| R31 | Rapport et preuves | report/main.tex | 8 pages compilées et inspectées, 12 annotations DOI vérifiées | PASS |
| R32 | État de l’art récent détaillé | ARTICLE_ANALYSIS_DETAILED.md | six textes intégraux et résumé de Xie vérifiés, texte intégral de Xie et certains artefacts non confirmés | PARTIAL |
| R33 | Jeu de données réel | datasets/README.md | scénario synthétique autorisé | OPTIONAL |
| R34 | Contrôles Streamlit | evaluation/browser.py | Chrome, journal JSON et CSV téléchargé | PASS |
| R35 | Corpus récent vérifié | BIBLIOGRAPHY_VERIFICATION.md | sept DOI et bibliographie éditable | PASS |
| R36 | Comparatif et Knowledge Management | ARTICLE_COMPARISON.md, présentation | deux tables et diapositive 6 | PASS |
| R37 | Architecture et captures réelles | report/main.tex, presentation/screenshots/ | diagramme logiciel dans l’article et la slide 28, captures Chrome | PASS |
| R38 | Présentation en six parties avec médias animés | presentation/ | 44 diapositives, titres des sept articles, résultats T1–T5 sur la diapo 35, 18 GIF et 99 images, lecture des GIF extraits sous Chrome, ouverture dans Impress | PASS |
| R39 | Scripts synchronisés et trois orateurs | presentation/slides.json | notes PowerPoint et quatre PDF générés depuis la même source, minutage basé sur le texte et les médias | PASS |
| R40 | Questions de soutenance | presentation/QUESTIONS.md | 59 réponses et PDF | PASS |
| R41 | Rang et mémoire de la fenêtre récente | MATHEMATICAL_GUARANTEES.md | inégalités de CDF, tests et courbes | PASS |
| R42 | Borne d’espace de GK simplifié | algorithms/quantiles.py, MATHEMATICAL_GUARANTEES.md | preuve de O(min(n, √(n/ε))) tuples pour cette passe, essais adverses | PASS |
| R43 | Alertes exactes et approchées | evaluation/final_study.py | matrices et délais sur cinq scénarios | PASS |
| R44 | Fenêtres de taille croissante et temps | evaluation/final_study.py | CSV jusqu’à N=50 000, trois répétitions et pic de requête séparé | PASS |
| R45 | Sensibilité N et epsilon sur trace commune | evaluation/sensitivity.py | douze configurations, matrice de confusion et délais publiés | PASS |
| R46 | Quantiles récents groupés | algorithms/quantiles.py, evaluation/query_benchmark.py | identité sur 1 200 états et mesures appariées | PASS |
| R47 | Propriétés génératives | tests/test_properties_v4.py | oracles de rang, de comptage et de fenêtre, bords et doublons | PASS |
| R48 | Deux stratégies d’alerte | evaluation/alert_comparison.py | 30 comparaisons, confusion et délais par épisode | PASS |

La grille interne compte 46 PASS, 1 PARTIAL et 1 OPTIONAL. R42 valide la borne prouvée pour la variante du dépôt.

| Contrôle de publication | État | Preuve ou dépendance |
|---|---|---|
| Lecture du diaporama dans Microsoft PowerPoint | NOT TESTED | Chrome a lu les GIF extraits et Impress a ouvert le PPTX |
| Chronométrage par les trois orateurs | NOT TESTED | Scripts équilibrés à partir du texte et des durées d’animation, répétition en personne à venir |
| Publication, CI hébergée et clone GitHub de la V4 | BLOCKED | Autorisation de publier requise. Le clone local et l’extraction du ZIP permettent la vérification avant fusion |
