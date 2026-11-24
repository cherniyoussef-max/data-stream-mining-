# Traçabilité du projet 4

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
| R31 | Rapport et preuves | report/main.tex | 8 pages compilées Tectonic, métadonnées et citations contrôlées | PASS |
| R32 | État de l’art récent détaillé | ARTICLE_ANALYSIS_DETAILED.md | sept études et deux tables, certains tableaux d’origine et dépôts restent non vérifiés | PARTIAL |
| R33 | Jeu de données réel | datasets/README.md | scénario synthétique autorisé | OPTIONAL |
| R34 | Contrôles Streamlit | evaluation/browser.py | Chrome, journal JSON et CSV téléchargé | PASS |
| R35 | Corpus récent vérifié | BIBLIOGRAPHY_VERIFICATION.md | sept DOI et bibliographie éditable | PASS |
| R36 | Comparatif et Knowledge Management | ARTICLE_COMPARISON.md, présentation | deux tables et diapositive 6 | PASS |
| R37 | Architecture et captures réelles | report/main.tex, presentation/screenshots/ | diagramme logiciel dans l’article et la slide 28, captures Chrome | PASS |
| R38 | Présentation en six parties avec médias animés | presentation/ | 44 diapositives, 18 GIF incorporés, 99 images distinctes, lecture des GIF extraits sous Chrome, ouverture du fichier dans Impress | PASS |
| R39 | Scripts synchronisés et trois orateurs | presentation/slides.json | notes PowerPoint, quatre PDF, numérotation commune | PASS |
| R40 | Questions de soutenance | presentation/QUESTIONS.md | 57 réponses et PDF | PASS |
| R41 | Rang et mémoire de la fenêtre récente | MATHEMATICAL_GUARANTEES.md | inégalités de CDF, tests et courbes | PASS |
| R42 | Borne d’espace de GK simplifié | algorithms/quantiles.py | rang prouvé, croissance mesurée, théorème d’espace absent pour la variante | PARTIAL |
| R43 | Alertes exactes et approchées | evaluation/final_study.py | matrices et délais sur cinq scénarios | PASS |
| R44 | Fenêtres de taille croissante et temps | evaluation/final_study.py | CSV jusqu’à N=50 000, trois répétitions et pic de requête séparé | PASS |
| R45 | Sensibilité N et epsilon sur trace commune | evaluation/sensitivity.py | douze configurations, matrice de confusion et délais publiés | PASS |

Sur les 44 lignes non optionnelles, 42 PASS et 2 PARTIAL, soit 95,5 % de couverture stricte de cette grille interne. Le choix C autorisé conserve la variante GK et laisse sa borne d’espace générale ouverte. Le contrôle de lecture se limite aux GIF extraits dans Chrome et à l’ouverture du fichier dans Impress.
