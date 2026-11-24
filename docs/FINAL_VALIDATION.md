# Validation finale

Ce journal décrit la livraison précédente. Pour les preuves et verdicts actuels, voir [Validation V3](FINAL_VALIDATION_V3.md).

## État initial et changements

L’[audit initial](INITIAL_AUDIT.md) reproduit l’absence de collecte automatique, le comptage DGIM d’un singleton à zéro et un dépassement de rang GK. Les quatre anciens tests passaient lorsqu’on désignait leur fichier. Les implémentations sont maintenant dans `algorithms/`. L’ancien module est un point d’import compatible. Le deuxième GK et les démos redondantes ont été remplacés par un CLI partagé avec le tableau de bord. Les caches compilés ont été retirés de l’index du dépôt.

## Tests

`python -m pytest -v` : 87 collectés, 87 réussis, zéro échec et zéro test ignoré. Les avertissements proviennent de plugins préinstallés. Le [journal](../results/pytest_results.txt) contient les identifiants des tests. T1 : Pearson 93,316, p=0,642188 et p ajustée=0,380806. T2 : comptes 1388/2897/5715 (k=1) et 3874/7179/8947 (k=2) sur 10 000 tirages par configuration. Des essais k=3 couvrent cinq poids égaux puis cinq poids distincts. T3 et T4 : zéro violation des assertions après insertion dans les cas testés. T5 : zéro violation sur les grilles testées, y compris les cibles proches de zéro lorsque l’intervalle brut contient un rang.

## Expériences

Les deux profils ont été exécutés. Rapide : 2 710 lignes. Complet : 6 758 lignes, graines 42, 204, 313. Erreur DGIM échantillonnée maximale 33,33 %. Erreur GK normalisée maximale 5 % avec ε=0,05. Zéro dépassement dans les mesures exportées. À N=10 000, le protocole historique mesure 2 000 entrées contre 10 000 et 191 752 contre 327 080 octets de pic, soit 80 % d’entrées et 41,37 % de pic en moins. Le nouveau protocole chronomètre trois répétitions et mesure la mémoire de requête séparément. Il balaie N de 100 à 50 000. À N=10 000 et ε=0,05, il mesure 82 940 octets pour les blocs et 321 872 pour la FIFO. Ces mesures d’allocation correspondent à des protocoles distincts. Les 19 figures et les mesures détaillées sont dans `results/`.

La croissance de GK est mesurée sur neuf distributions, cinq ε et jusqu’à 100 000 événements. L’expérience ne fournit pas un théorème d’espace. Pour les quantiles récents, sur 6 000 observations le plus grand écart P99 mesuré est de six rangs avec zéro violation de la borne des blocs. Comparer les décisions approchées à la règle exacte donne 1 200 accords sur 1 200 dans le scénario de référence. Contre les étiquettes d’incident : 398 VP, 603 VN, 197 FP, 2 FN et F1=0,80. Le délai de détection est deux événements et le rétablissement intervient 197 événements après la fin de l’incident. Les autres configurations sont dans [l’étude](../results/final_study.json).

## Application

CLI exécuté avec le scénario par défaut, alerte à 403 et rétablissement à 998. AppTest et Chrome ont exercé les commandes de simulation. En Chrome, deux cycles démarrage/pause ont progressé au rythme attendu et le compteur est resté fixe pendant 1,4 s de pause. Le CSV de 500 lignes a été téléchargé et comparé au compteur et au P99 affichés. Le test a parcouru les onglets et changé N en réinitialisant l’état. Le [journal navigateur](../results/browser_validation/report.json) et les captures documentent cette exécution sans erreur console. Les essais intermédiaires avaient rencontré un crash Chrome et une erreur de chargement CSS sur un disque saturé. Le test final a réussi avec un profil temporaire en mémoire et un minuteur désactivé en pause.

## Verdict

| Domaine | Verdict |
|---|---|
| Interfaces et T1–T5 | Vérifiés |
| Exactitude mathématique | Garanties de comptage et de rang documentées, résultats empiriques distincts |
| Reproductibilité | Rapide, complet, CLI, tests et rapport exécutés |
| Démonstration pratique | CLI, AppTest et Chrome validés |
| Dossier académique | Rapport, slides, captures, scripts, exercices et 57 réponses livrés. Analyse numérique des publications partielle |

Le GK simplifié ne revendique pas la borne d’espace de la compression originale. Les blocs récents ont une erreur de frontière et une borne différente. Les sources sont synthétiques et l’oracle optionnel prend O(N) mémoire. Les octets du benchmark mémoire ne couvrent ni les requêtes ni toute la session Streamlit.

Le diaporama contient 41 pages 16:9 et des notes éditables. Impress l’a exporté en PDF statique. Les séquences utilisent des diapositives successives, contrôlées par l’orateur. Microsoft PowerPoint n’a pas été utilisé pour la validation. LaTeX était indisponible et le rapport de huit pages a été compilé avec ReportLab. Les scripts sont construits depuis les mêmes numéros de diapositives que les notes. Les analyses papier restent plus courtes qu’une relecture chiffrée exhaustive de leurs tableaux. La matrice distingue ces limites de la validation du prototype.
