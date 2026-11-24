# Études récentes : méthode, preuve et usages

La [notice bibliographique](BIBLIOGRAPHY_VERIFICATION.md) identifie les versions. Les exemples ci-dessous sont didactiques. Les méthodes avancées sont étudiées dans la revue et les résultats du projet proviennent des implémentations locales.

## 1. Tirages pondérés parallèles

Hübschle-Schneider et Sanders traitent les situations où un tirage pondéré séquentiel devient le coût dominant. Ils distinguent tirage unique, avec et sans remise, permutation, Poisson et réservoir par lots. Les tables alias et leurs constructions parallèles permettent de répartir préparation et requêtes. L’analyse dépend du modèle PRAM ou à messages, de la règle de tirage et du nombre de processeurs. Le tableau 1 donne les coûts distincts de construction et requête. Les expériences de la version ACM incluent des constructions de table alias en mémoire partagée. La portabilité des accélérations dépend du matériel et des poids.

Exemple : répartir des latences pondérées sur deux processeurs, construire les structures des lots, puis produire un tirage selon la distribution cible. Notre A-Res utilise un tas et une seule source. Cette comparaison motive la distinction entre règle d’inclusion et stratégie d’exécution.

## 2. Sliding sketches

Gou et al. traitent l’expiration dans des sketches historiques. Leur framework emploie des zones temporelles, adaptées à des requêtes telles que fréquence, heavy hitters et heavy changes. L’analyse de précision et les expériences du manuscrit sont spécifiques aux sketches et aux requêtes adaptés. Le texte présente des comparaisons à budget mémoire donné. Son intérêt vient de la réutilisation d’une structure existante, avec un surcoût de gestion temporelle.

Exemple : ajouter les paquets fréquents d’une période, faire avancer la frontière, puis compter les paquets de la dernière période uniquement. Notre DGIM calcule un agrégat binaire et les maxima pondérés visent des quantiles. Les garanties respectives ne s’échangent pas.

## 3. Évaluation de quantiles

Fernando, Bindra et Daudjee comparent KLL, Moments, DDSketch, UDDSketch et ReqSketch pour choisir un sketch selon l’erreur, la mémoire, les mises à jour et les caractéristiques des données. Les expériences de la section 4 comprennent des données synthétiques et réelles. La section 4.5.3 discute notamment un écart de quantile de Moments sur des données réelles. Une difficulté méthodologique est de comparer les budgets et les métriques d’erreur, en particulier pour les queues.

Exemple : construire deux flux ayant la même médiane mais des queues différentes, puis comparer erreur de rang et écart numérique au P99. Notre protocole adopte cette séparation sans reproduire leurs cinq implémentations.

## 4. Réservoir de jointures

Dai, Hu et Yi visent un échantillon uniforme des résultats d’une jointure qui peut croître plus vite que ses entrées. Ils combinent réservoir à prédicat et index dynamique. Le papier analyse le coût presque linéaire dans son cadre et compare des requêtes sur graphes et données relationnelles. L’index constitue un coût supplémentaire, justifié par la structure de la jointure.

Exemple : lorsqu’une commande arrive, déterminer ses correspondances client, alimenter la sélection via l’index et garder un échantillon du résultat. Notre unité d’échantillonnage est une mesure de latence.

## 5. GK et Khanna–Greenwald

Gribelyuk, Sawettamalya, Wu et Yu simplifient la structure du sketch de quantiles déterministe sur univers totalement ordonné. Ils associent des idées de GK et d’une compression inspirée de la preuve de borne inférieure. Le résultat annoncé par ACM est au plus (2+o(1))ε⁻¹ log(εn) éléments dans son régime asymptotique. Le travail est principalement une preuve. Son intérêt est un contrôle d’espace formel dans le modèle de comparaison.

Exemple : suivre un P99 sur un comparateur de mesures, regrouper des rangs puis demander un quantile avec tolérance additive. Notre passe sur tuples est plus simple à démontrer au tableau et son espace général reste non établi.

## 6. Univers entier

Gupta, Singhal et Wu demandent si l’espace optimal par comparaisons demeure une limite quand les valeurs sont des entiers d’un univers borné. La réponse est négative dans leur modèle, avec une structure déterministe en O(1/ε) mots. Les opérations sur l’univers numérique sont essentielles. Il s’agit d’un résultat théorique et non d’un banc de latences.

Exemple : encoder des délais entiers en microsecondes dans un domaine connu, organiser les intervalles de valeurs et interroger le rang. Les flottants comparés dans notre prototype ne donnent pas accès à son théorème.

## 7. Inférence conditionnelle

Xie, Yan, Jiang et Kong traitent les données qui arrivent par lots sans conserver les anciennes lignes. La perte quantile non lisse est approchée par lissage. La mise à jour en ligne réutilise des résumés et corrige l’erreur liée à l’actualisation. L’article éditeur documente des simulations et deux applications, demande de vélos à Séoul et fonds indiciels. L’inférence exige des hypothèses statistiques et des covariables. Les chiffres détaillés de ces expériences restent à relever dans les tableaux de l’article.

Exemple : associer à chaque latence la charge du serveur, ajuster un P99 conditionnel, puis le mettre à jour avec un nouveau lot. Notre P99 est descriptif et le seuil est opérationnel.
