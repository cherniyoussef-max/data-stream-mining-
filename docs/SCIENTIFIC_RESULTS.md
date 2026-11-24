# Surveillance de latences par résumés de flux

## Résumé

Un flux rapide et de longueur inconnue impose de choisir les observations à conserver. Nous implantons quatre méthodes classiques et une approximation des quantiles récents par blocs. Nous les évaluons avec des références exactes et une application locale de surveillance. Le profil complet fournit 6 758 lignes de mesures. Aucun dépassement n’y est observé pour les bornes DGIM et GK. Le scénario synthétique déclenche une alerte à 403 et montre le rétablissement à 998. Les preuves de rang et de comptage sont documentées indépendamment des tests.

## Problème et fondements

Nous cherchons à concilier mémoire, précision et capacité de réaction. Algorithm R conserve un échantillon uniforme de positions. A-Res favorise les latences fortes. DGIM suit les dépassements d’un seuil sur les N derniers événements. GK estime les quantiles historiques. Les résumés par blocs répondent à la question opérationnelle des quantiles récents. Les fenêtres landmark, tumbling, glissantes et à décroissance exponentielle sont détaillées dans [les fondements](MATHEMATICAL_GUARANTEES.md).

## Travaux connexes

Vitter, Efraimidis–Spirakis, Datar et al., Greenwald–Khanna et Arasu–Manku donnent les méthodes fondatrices. Les travaux récents examinent le parallélisme, les jointures, l’expiration et les compromis entre exactitude et ressources. Voir [la bibliographie et le tableau comparatif](STATE_OF_THE_ART.md). Notre objectif est pédagogique et expérimental. Les résultats numériques ci-dessous proviennent de ce dépôt.

## Architecture et protocole

Un événement met à jour le moteur partagé entre CLI et Streamlit. Les tests et benchmarks interrogent les mêmes classes. Le mode avec oracles conserve une FIFO de N éléments pour les quantiles et le comptage exacts. Le benchmark chronomètre les mises à jour et les requêtes hors entrée et références. Les mesures mémoire sont séparées. Le profil complet utilise les graines 42, 204 et 313.

## Résultats mesurés

| Mesure | Valeur |
|---|---:|
| T1, Pearson, 10 000 tirages | χ²=93,316 ; p=0,6422 ; p ajustée=0,3808 |
| T2, poids 1,2,4 et k=1 | 13,88 %, 28,97 %, 57,15 % |
| T2, mêmes poids et k=2 | 38,74 %, 71,79 %, 89,47 % |
| DGIM, erreur relative maximale échantillonnée | 33,33 % pour une borne de 50 % |
| GK, fraction maximale d’erreur de rang | 5,00 % à ε=0,05 |
| Violations des bornes dans le benchmark | 0 |
| Pic tracemalloc FIFO / blocs à N=10 000 | environ 327 / 192 ko |
| Résumé par blocs / FIFO à la fin de la mesure | 2 000 / 10 000 entrées |

Les 14 figures couvrent les inclusions (01–02), l’exactitude et la mémoire DGIM (03–05), les quantiles et leur rang (06–09), le pic mémoire et le débit (10–11), puis le scénario, l’alerte et la dérive (12–14). Les écarts de valeur ne sont pas directement bornés par l’erreur de rang, en particulier dans les queues ou quand la distribution se déplace.

## Scénario et discussion

Le profil complet exporte 6 012 observations DGIM à densité 0,7. Erreur relative moyenne 12,30 %, médiane 12,73 %, 95e centile 24,06 %. Les 648 requêtes GK atteignent au plus 100 % de leur budget de rang (5 000 rangs sur 100 000 à ε=0,05). En millisecondes, l’erreur absolue médiane est 0,120 pour P50 et 0,646 pour P99. Les maxima respectifs sont 2,110 et 14,650. Le contrôle des clés algorithme, graine, fenêtre, n, k, ε, q et distribution ne trouve aucun doublon. Les colonnes numériques de temps, de rang et d’état contrôlées sont finies.

L’[étude complémentaire](../results/final_study.json) balaie six tailles de fenêtre, quatre précisions des blocs, neuf ordres pour GK et cinq scénarios d’alerte. Le scénario isolé montre 4 alertes supplémentaires par rapport au seuil exact et 53 par rapport à l’étiquette d’incident. Le cas sous le seuil ne déclenche aucune alerte. Sur les 6 000 requêtes P99 récentes, l’écart maximal est six rangs et aucun dépassement n’est observé.

L’incident commence à 401 et la récupération du générateur à 801. L’alerte arrive deux événements après le début, et le rétablissement 197 événements après le retour du générateur. Ce délai correspond à l’expiration des mesures élevées dans une fenêtre de 200 positions. Au rétablissement le P99 historique est de 182,51 ms et le P99 récent de 48,21 ms. Les seuils 80 ms et 110 ms s’appliquent respectivement à la médiane et au P99.

La p-valeur de Pearson indique une non-rejection pour les graines déclarées. La garantie de DGIM découle des invariants, ainsi que la précision de rang historique de GK. La compression choisie simplifie GK. Le théorème d’espace de sa version originale demanderait sa stratégie de compression prouvée. Les blocs récents ont une borne propre qui tient compte de la frontière et la FIFO d’évaluation a un coût linéaire. Le jeu de données est entièrement synthétique et la charge n’est pas distribuée. L’effet d’une hystérésis et l’évaluation sur une trace réseau réelle sont des pistes ultérieures.

## Conclusion

L’application sépare les questions historiques et opérationnelles. La reprise du trafic récent alors que le P99 historique reste élevé rend cette différence observable pendant la soutenance.
