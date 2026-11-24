# Fiches détaillées des sept articles

Les résultats publiés ci-dessous sont distingués des mesures locales. Les exemples sont illustratifs. Les codes d’articles ne sont pas requis pour exécuter le dépôt. Aucun résultat empirique des articles n’a été répliqué.

## 1 · Hübschle-Schneider et Sanders — ACM TOMS 48(3), 2022

**Contexte et objectif.** Un échantillon pondéré peut être coûteux à préparer lorsque le jeu et l’échantillon sont grands. Les auteurs visent des structures parallèles qui respectent la loi demandée, là où de nombreuses méthodes antérieures sont séquentielles.

**Méthode et modèle.** L’article distingue tirage unique, avec et sans remise, permutations, Poisson et réservoirs par lots. Les tables alias servent aux tirages catégoriels, tandis que des structures et sélections distinctes traitent les autres lois. Les analyses PRAM et passage de messages ne sont pas interchangeables.

**Résultat et évaluation.** Le tableau 1 sépare le travail de construction, le travail de requête et la latence selon la règle. Le manuscrit comprend des comparaisons de constructions alias en mémoire partagée. La structure du travail et les coûts mesurés dépendent de la configuration et de la distribution des poids. Aucun facteur global de vitesse n’est transféré au prototype.

**Exemple.** Répartir des événements de masses 1,2 sur une unité et 6,3 sur une autre. Construire les structures locales. Choisir l’unité et l’événement suivant la loi ciblée. Le GIF A1 illustre la répartition, sans exécuter le papier.

**Bilan.** La distinction entre loi de tirage et exécution est l’apport le plus utile. Le projet utilise A-Res séquentiel. [Article](https://doi.org/10.1145/3549934) · [Manuscrit auteur](https://arxiv.org/abs/1903.00227).

## 2 · Gou et al. — IEEE TKDE, 2023

**Contexte et objectif.** De nombreux sketches agrègent tout l’historique, alors que l’opérateur veut des fréquences ou des éléments dominants sur une période récente. Le cadre sépare logique approximative et gestion du temps.

**Méthode et modèle.** Les champs des buckets représentent des zones temporelles. Le déplacement d’un pointeur de balayage retire progressivement l’information ancienne. Le manuscrit discute modèles par comptage ou par temps, fonctions de hachage et optimisation des accès. Le cadre est évalué après adaptation à plusieurs problèmes, pas comme estimateur universel.

**Évaluation.** La §8.1 utilise CAIDA 2016, Web Page, Zipf synthétique de 32 millions d’éléments et StackOverflow. Le dernier sert au cas temporel. Les auteurs déclarent une implémentation C++ ouverte dans la référence [15]. Ils échantillonnent les métriques chaque dixième de fenêtre et font des comparaisons de structures adaptées et de références propres à chaque problème (§8). La part du gain due au modèle et au type d’agrégat n’est pas extrapolée.

**Exemple.** Mettre à jour la zone 2 avec un paquet, décaler l’horizon, puis expirer la zone 1. Le GIF A2 montre les champs temporels. Notre DGIM conserve des groupes de bits 1 et la méthode par blocs vise le rang.

**Bilan.** Les structures historiques peuvent être adaptées, au prix de métadonnées d’expiration. [Manuscrit accepté](https://skyelves.github.io/files/TKDE22-A_Sketch_Framework_for_Approximate_Data_Stream_Processing_in_Sliding_Windows.pdf).

## 3 · Fernando, Bindra et Daudjee — EDBT, 2023

**Contexte et objectif.** Plusieurs sketches proposent des compromis que les garanties seules ne suffisent pas à départager pour une charge. L’objectif est un protocole commun d’observation des coûts et de l’erreur.

**Méthode et évaluation.** KLL, Moments, DDSketch, UDDSketch et ReqSketch reçoivent les jeux Pareto, Uniforme, NYT et Power. La section 4 sépare métriques et paramètres. La figure 6b indique une erreur relative moyenne inférieure à 1 % sur l’expérience uniforme pour les cinq méthodes étudiées (§4.5.2). La figure 6a et la §4.5.1 décrivent une dégradation de KLL au P99 sur la queue Pareto considérée. La §4.5.3 discute l’effet des répétitions sur NYT.

**Exemple.** Alimenter chaque sketch avec le même jeu, puis isoler le résultat uniforme. Le GIF A3 donne la condition et le résultat de la figure 6b. La comparaison s’interprète dans l’unité d’erreur publiée. Notre rapport ne confond pas cette erreur avec l’erreur additive de rang.

**Bilan.** Évaluation empirique multifactorielle, sans hiérarchie générale pour tous les flux. [Actes et figures](https://openproceedings.org/2023/conf/edbt/paper-9.pdf).

## 4 · Dai, Hu et Yi — PACMMOD/SIGMOD, 2024

**Contexte et objectif.** Une jointure peut avoir une sortie beaucoup plus grande que ses entrées. Tirer uniformément en matérialisant la sortie nuit au traitement en flux. Le travail vise à éviter cette matérialisation.

**Méthode et preuve.** Un réservoir à prédicat contourne les candidats inadmissibles. Un index dynamique sur la structure de jointure permet d’identifier et de compter des candidats, avec regroupements et bornes spécifiques (sections sur l’index et l’échantillonnage). Les garanties de temps presque linéaire sont propres au cadre de jointures traité.

**Évaluation et limites.** La section expérimentale utilise notamment 508 837 arêtes Epinions de SNAP, réordonnées séparément pour simuler les relations de graphes, et des données relationnelles. Le volume de candidats et la forme de jointure influencent le coût. L’index peut devenir une part importante de l’état.

**Exemple.** Ajouter une commande, chercher le client correspondant dans l’index, puis produire un candidat admissible au réservoir. Le GIF A4 est illustratif. Notre réservoir se limite aux lectures d’une source.

**Bilan.** Même notion d’uniformité, population différente. [Manuscrit auteur et expériences](https://arxiv.org/html/2404.03194v2).

## 5 · Gribelyuk, Sawettamalya, Wu et Yu — PACMMOD/PODS, 2024

**Contexte et objectif.** GK avait une borne d’espace optimale à l’ordre de grandeur dans le modèle de comparaison, avec une analyse délicate. Les auteurs demandent une construction déterministe plus simple, sans perdre l’ordre de grandeur optimal.

**Méthode et garantie.** Le sketch combine le paradigme de GK et des idées issues de l’analyse de Khanna–Greenwald. La portée est l’erreur additive en rang sur univers totalement ordonné. L’énoncé publié borne l’état asymptotiquement par `(2+o(1)) ε⁻¹ log(εn)` éléments. C’est une preuve théorique, pas une performance mesurée sur des latences.

**Exemple.** Visualiser trois rangs, une marge additive puis un représentant. Le GIF A5 représente l’idée de compression et l’unité de la borne, sans simuler la construction exacte ni prétendre que tout regroupement préserve la garantie.

**Bilan.** L’apport est la preuve d’espace pour une stratégie précise. La compression simplifiée du projet garde la preuve de rang et une évaluation de mémoire. [ACM, article 109](https://doi.org/10.1145/3651610).

## 6 · Gupta, Singhal et Wu — FOCS, 2024

**Contexte et objectif.** Les limites du modèle de comparaison ne répondent pas à la question de l’espace lorsqu’on peut manipuler directement les représentations des valeurs.

**Méthode et garantie.** Les auteurs exploitent un univers entier fini pour obtenir une estimation déterministe avec `O(1/ε)` mots dans leur modèle. Comparer les coûts en éléments et en mots exige de préciser les opérations et la taille du mot. Le cadre n’assimile pas un univers continu à des entiers par hypothèse gratuite.

**Exemple.** Des valeurs 0 à 7 peuvent être découpées selon des intervalles numériques. Le GIF A6 illustre cette propriété. Une discrétisation de mesures réelles devrait compter séparément son erreur de valeur.

**Bilan.** Le travail débloque une borne théorique dans un modèle plus riche. Le résultat n’est pas une borne pour notre GK. [Version auteur](https://arxiv.org/abs/2404.03847).

## 7 · Xie, Yan, Jiang et Kong — Journal of Econometrics, 2025

**Contexte et objectif.** L’inférence sur une régression quantile en flux se heurte à une perte non lisse et au coût de conserver toutes les lignes historiques.

**Méthode et évaluation.** Les auteurs lissent la perte, réutilisent des résumés de lots et corrigent une partie de l’erreur de mise à jour. La notice Elsevier et le programme de présentation des auteurs attestent simulations et applications sur les trajets de vélos à Séoul et les fonds indiciels. Le détail chiffré des tableaux d’inférence n’est pas repris, faute de vérification intégrale de ces tableaux.

**Exemple.** Suivre le P99 de latence selon la charge, mettre à jour les résumés lors d’une arrivée par lot et interroger deux niveaux de charge. Le GIF A7 est un schéma, sans données causales. Le projet estime un P99 marginal et n’infère pas de régression.

**Bilan.** L’étude élargit la cible scientifique à l’incertitude d’un quantile conditionnel avec covariables. [Notice et résumé éditeur](https://www.sciencedirect.com/science/article/pii/S0304407624002756).
