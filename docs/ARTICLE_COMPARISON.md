# Comparaison des problèmes scientifiques

## A. Fonctions couvertes

| Étude | Problème et approche | Uniforme | Pondéré | Fenêtre | Quantile | Inférence | Lien |
|---|---|---|---|---|---|---|---|
| Hübschle-Schneider–Sanders | Lots, tables alias et sélection parallèle | Cas poids égaux | Oui | Lots, sans expiration glissante générale | — | — | A-Res |
| Gou et al. | Expiration par zones | — | — | Oui | — | — | DGIM |
| Fernando et al. | Comparaison de cinq sketches | Selon sketch | — | — | Oui | — | Méthodologie |
| Dai–Hu–Yi | Index de jointure et réservoir à prédicat | Oui | — | — | — | — | R |
| Gribelyuk et al. | Sketch déterministe comparatif | — | — | — | Oui | — | Espace GK |
| Gupta–Singhal–Wu | Univers entier borné | — | — | — | Oui | — | Modèle de calcul |
| Xie et al. | Mise à jour de régression lissée | — | — | Lots historiques résumés | Conditionnel | Oui | Distinction des cibles |

## B. Modèles, garanties et limites

| Étude | Données et cible | Garantie ou métrique | Temps et espace | Rapport à notre démo |
|---|---|---|---|---|
| Hübschle-Schneider–Sanders | Lots pondérés, plusieurs règles avec/sans remise | Loi de tirage | Dépend de la règle, du modèle parallèle et de la taille du lot, tableau 1 | A-Res séquentiel sur un événement à la fois |
| Gou et al. | Fenêtre et fréquences | Erreur d’estimation, mesures sur sketches adaptés | Surcoût temporel et mémoire propre au sketch | Expiration de DGIM, agrégat binaire |
| Fernando et al. | Flux et quantiles descriptifs | Erreurs de quantile, débit, mémoire | Mesures expérimentales par méthode | Séparer rang, valeur et coût |
| Dai–Hu–Yi | Jointures de tuples en flux | Uniformité sur résultats | Temps presque linéaire sous hypothèses de jointure et index | Échantillonnage uniforme sans jointure dans le projet |
| Gribelyuk et al. | Ordre total, rang descriptif | Additive déterministe | Au plus (2+o(1))ε⁻¹ log(εn) éléments dans le régime de l’article | Théorème utile comme repère, indépendant de notre passe simplifiée |
| Gupta–Singhal–Wu | Univers entier borné, rang descriptif | Additive déterministe | O(1/ε) mots dans le modèle de l’article | Le modèle Python sur flottants n’en hérite pas |
| Xie et al. | Lots avec covariables, régression quantile | Inférence et simulation | Résumé des lots, coût dépend du modèle | Un P99 descriptif s’interprète autrement qu’un P99 conditionnel |

Le temps d’une jointure, l’erreur en rang et la couverture d’un intervalle statistique évaluent des tâches distinctes. Les utiliser comme classement global induirait une comparaison trompeuse. Les [analyses détaillées](ARTICLE_ANALYSIS_DETAILED.md) précisent les exemples et les limites de chaque rapprochement. Les sept méthodes avancées sont étudiées, et le projet implémente uniquement les algorithmes classiques et sa méthode par blocs.
