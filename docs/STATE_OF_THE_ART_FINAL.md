# Revue comparative ciblée des méthodes de flux

Le corpus récent couvre 2022–2025, période choisie pour les travaux sur le passage à l’échelle, l’expiration, les biais d’évaluation des quantiles et les nouvelles bornes d’espace. Cinq articles fondateurs établissent les définitions et les algorithmes historiques. Une technique a été retenue si sa cible, son modèle et son apport sont pertinents pour le projet et traçables à une source primaire. Les publications sans lien direct avec la sélection, l’expiration ou l’estimation de queue sont exclues. Nous avons vérifié des actes, DOI, ACM, le manuscrit IEEE, Elsevier, des manuscrits auteurs et des notices institutionnelles. Cette sélection constitue une revue ciblée, sans protocole systématique.

| Famille | Ce que montrent les travaux | Intérêt pour le projet |
|---|---|---|
| Pondération et jointures | La loi de sélection, la population cible et l’exécution parallèle sont trois questions distinctes. | A-Res cible des positions pondérées, sur un seul flux sans jointure. |
| Expiration | Les estimations sur fenêtres existent depuis les travaux de Datar et d’Arasu–Manku. Gou et al. adaptent plusieurs sketches par zones temporelles. | DGIM et les blocs utilisent l’expiration, avec deux garanties séparées. |
| Quantiles descriptifs | L’erreur de valeur dépend de la distribution et de la métrique. Les bornes d’espace dépendent des opérations permises sur les valeurs. | Nous publions erreurs de rang et en ms, et distinguons la variante Python du GK original. |
| Quantiles conditionnels | Les résumés de lots peuvent actualiser une estimation conditionnée par des covariables. | Extension scientifique distincte du P99 marginal du tableau de bord. |

Le rapport inclut une section dédiée aux sept articles et une comparaison directement dans le PDF. Les [fiches détaillées](ARTICLE_ANALYSIS_DETAILED.md), la [notice des 12 références](BIBLIOGRAPHY_VERIFICATION.md) et les [deux tables comparatives](ARTICLE_COMPARISON.md) sont des pièces complémentaires.
