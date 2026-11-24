# Questions et réponses de soutenance

## Fondements et échantillonnage

1. **Pourquoi traiter les données en flux ?** Leur volume et leur longueur inconnue rendent le stockage intégral impraticable.
2. **Quel lien avec le Knowledge Management ?** Des mesures brutes deviennent des indicateurs interprétables et des décisions traçables.
3. **Qu’est-ce qu’une fenêtre landmark ?** Elle commence à un repère fixe et s’allonge.
4. **Une fenêtre tumbling ?** Ce sont des blocs disjoints, chacun avec son propre bilan.
5. **Une fenêtre glissante ?** Elle contient ici les N dernières positions et expire à chaque arrivée.
6. **Pourquoi utiliser une décroissance ?** Elle privilégie les observations récentes progressivement.
7. **Que signifie représentatif dans R ?** Chaque sous-ensemble de k positions a la même probabilité.
8. **Pourquoi k/n ?** L’admission k/i suivie de la survie i/n donne k/n. Pour le remplissage, la survie vaut directement k/n.
9. **Et si n est inférieur à k ?** Toutes les positions sont retenues.
10. **Pourquoi échantillonner les positions ?** Deux valeurs égales peuvent provenir d’événements distincts.
11. **Pourquoi pondérer ?** Les latences élevées deviennent plus fréquentes dans l’échantillon exploratoire.
12. **Pourquoi la clé U puissance 1/w ?** Elle équivaut à classer une course exponentielle de taux w.
13. **Pourquoi un tas minimum ?** La plus faible priorité retenue est disponible immédiatement pour une comparaison.
14. **La sélection est-elle k fois w/somme ?** La formule w/somme vaut pour k=1. À k>1, le choix sans remise change les poids restants.
15. **Pourquoi travailler en logarithmes ?** On compare le même ordre sans élever une valeur proche de 1 à une puissance extrême.

## DGIM, GK et blocs

16. **Que représente un bucket DGIM ?** Plusieurs bits 1 consécutifs dans l’ordre des 1, éventuellement séparés par des zéros.
17. **Pourquoi les puissances de deux ?** Deux tailles égales fusionnent et doublent.
18. **Pourquoi les deux plus anciens ?** On garde la séparation temporelle la plus fine près de l’arrivée.
19. **Pourquoi au plus deux par taille ?** Le troisième déclenche une fusion, qui peut se propager.
20. **Que représente le timestamp ?** La fin du bucket, donc le 1 le plus récent représenté.
21. **Quand expire un bucket ?** À l’âge N. Son dernier 1 vient de sortir.
22. **Pourquoi modulo N+1 ?** Un bucket expire à l’âge N avant la réutilisation du même résidu.
23. **Quel bucket est approximé ?** Le plus ancien actif. Un singleton est compté exactement.
24. **D’où vient la borne 50 % ?** Pour un bucket s≥2, au moins s−1 bits plus récents limitent l’erreur relative de la demi-contribution.
25. **Pourquoi O(log² N) bits ?** Il y a O(log N) tailles et chaque taille ou timestamp demande O(log N) bits dans un codage compact.
26. **Que signifient g et delta ?** Le premier contribue au rang minimal cumulé. Le second borne l’intervalle jusqu’au rang maximal.
27. **Pourquoi compresser GK ?** Les voisins dont la fusion préserve l’invariant peuvent partager un représentant.
28. **Pourquoi garder les extrêmes ?** Ils répondent exactement aux requêtes q=0 et q=1.
29. **Qu’est-ce qu’un quantile de doublons ?** Une même valeur couvre un intervalle de rangs possibles.
30. **Que faire avec n très petit ?** Prendre le rang valide le plus proche si l’intervalle demandé ne contient aucun rang entier.
31. **Quelle borne d’espace a votre variante GK ?** O(min(n, √(n/ε))) tuples. Les paires anciennes consomment une part du cumul des rangs. Les tuples récents sont bornés par le nombre d’insertions. La borne classique logarithmique est plus serrée.
32. **Pourquoi deux P99 ?** L’historique résume toutes les latences. Le récent suit les N dernières positions.
33. **Comment fermer un bloc récent ?** Trier, regrouper des rangs voisins, conserver leur maximum et leur effectif.
34. **Pourquoi peut-il rester du périmé ?** Un bloc à cheval sur la frontière est retiré seulement à son expiration complète.
35. **Un quantile peut-il être absent de la fenêtre ?** Oui. C’est alors un seuil dont on mesure la CDF stricte et large.
36. **Pourquoi une borne en deux termes ?** Un terme mesure les points périmés et l’autre la perte de résolution de chaque bloc.
37. **Pourquoi B proche de √N ?** Il équilibre la taille brute du bloc courant avec le nombre de blocs.
38. **Est-ce toujours plus léger que FIFO ?** Non. À faible ε ou petit N, les maxima pondérés peuvent conserver presque autant d’entrées avec plus de métadonnées.

## Expériences, alertes et limites

39. **Que mesure T1 ?** L’écart entre les fréquences d’inclusion et leur espérance de 1 000.
40. **Pourquoi ajuster Pearson ?** Deux inclusions dans un même réservoir de taille fixe sont dépendantes.
41. **Une grande p-valeur prouve-t-elle l’uniformité ?** Non. Elle indique seulement qu’on ne rejette pas le modèle avec ce test.
42. **Pourquoi fixer les graines ?** Pour rejouer les mêmes tirages et distributions sans choisir un résultat favorable.
43. **Les tests démontrent-ils les garanties ?** Les preuves expliquent les garanties. Les tests cherchent des écarts entre code et modèle.
44. **Comment séparer temps et mémoire ?** Le chronomètre tourne hors tracemalloc. La mémoire de requête est mesurée séparément.
45. **Pourquoi les octets varient-ils ?** Objets, allocation et version du runtime influencent les pics.
46. **Pourquoi une petite erreur en rang peut changer le seuil ?** Deux rangs voisins peuvent avoir des latences très éloignées.
47. **Pourquoi attendre avant d’alerter ?** Le moteur attend min(20,N) valeurs pour stabiliser le démarrage.
48. **Que représente un faux positif contre l’incident ?** Une alerte alors que l’étiquette du générateur est inactive, y compris pendant la vidange de la fenêtre.
49. **Pourquoi deux matrices de confusion ?** Une mesure l’accord avec la règle exacte. L’autre mesure la concordance avec l’incident simulé.
50. **Pourquoi le P99 réagit-il aux valeurs isolées ?** Sur un petit N, le rang 99 % peut désigner le maximum.
51. **Pourquoi des données synthétiques ?** Elles permettent de contrôler le début, la durée et la fin d’un incident.
52. **Pourquoi Python et Streamlit ?** Les structures sont lisibles, et le même moteur alimente le terminal et le navigateur.
53. **Avez-vous utilisé Kafka ?** Non. La simulation locale suffit à la question étudiée.
54. **Avez-vous implémenté les sept articles ?** Les articles situent les méthodes. Les quatre algorithmes historiques et les blocs constituent le code testé.
55. **Quel est votre apport ?** Audit, implémentation, tests, étude comparative et démonstration reproductible.
56. **Que mesurer ensuite ?** La stabilité des politiques d’alerte sur une trace réelle annotée et l’effet d’une compression conforme au GK classique.
57. **Comment reproduire le projet ?** Installer les dépendances, lancer pytest, les deux modules d’expérience et le tableau de bord selon le README.
58. **Pourquoi regrouper P50, P95 et P99 ?** Les trois cibles portent sur les mêmes représentants. Un seul tri et un seul parcours cumulatif suffit pour obtenir les trois résultats.
59. **En quoi la persistance change-t-elle l’alerte ?** Elle exige trois décisions concordantes et une proportion minimale de points lents à court terme. Elle filtre les pics isolés, au prix de ne pas les détecter.
