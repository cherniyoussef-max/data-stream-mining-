# Fondements et garanties

## Fenêtres

- **Landmark** : tout conserver conceptuellement depuis un repère fixe, par exemple le début de la journée.
- **Tumbling** : blocs disjoints de taille fixe, comme un bilan distinct par minute.
- **Glissante** : les N derniers événements, avec expiration à chaque insertion.
- **Décroissance exponentielle** : poids d’un événement d’âge a égal à exp(−λa), donc influence ancienne progressivement réduite.

## Algorithm R

À l’instant j > k, une position présente est remplacée avec probabilité 1/j, car un seul des j choix la vise. Pour i > k, admission k/i, puis survie produit de j=i+1 à n de (j−1)/j = i/n, donc inclusion k/n. Pour i ≤ k, admission certaine, puis survie de k+1 à n égale à k/n. Quand n < k toutes les positions sont présentes. Le choix symétrique assure aussi l’uniformité des sous-ensembles : un sous-ensemble cible de taille k sans le nouvel item survit avec probabilité (n−k)/n. Pour un sous-ensemble qui contient le nouvel item, chacun des n−k anciens sous-ensembles candidats conduit au résultat avec probabilité 1/n. Dans les deux cas, le produit avec 1/C(n−1,k) vaut 1/C(n,k).

## A-Res

Pour U uniforme sur ]0,1[, la clé U^(1/w) équivaut à privilégier le plus petit temps T=−log(U)/w. T est exponentiel de taux w. La priorité stockée −log(T)=log(w)−log(−log(U)) évite le débordement d’une division pour les poids extrêmes. L’indice d’arrivée départage les égalités en machine. La course exponentielle donne P(premier=i)=wᵢ/Σw et, par absence de mémoire, le prochain choix est proportionnel aux poids restants. Pour k>1, les probabilités marginales d’inclusion s’obtiennent en sommant les ordres possibles. R utilise O(k) places, avec O(1) par insertion. A-Res utilise O(k) places, O(log k) au pire pour un remplacement et O(1) en cas de rejet.

## DGIM

Bucket de taille s, horodaté par son 1 le plus récent. La fusion des deux plus anciens parmi trois se propage vers les tailles supérieures. Un seul bucket peut chevaucher la frontière. S’il est vivant, sa contribution c satisfait 1 ≤ c ≤ s. Pour s=1 elle est exacte. Pour s≥2, la fusion garantit au moins un bucket de chacune des tailles 1,2,…,s/2 plus récent à la création. Leurs s−1 événements restent dans la fenêtre tant que le dernier 1 du bucket ancien est vivant, même si les buckets récents fusionnent ensuite. Si F compte tous les 1 plus récents, F≥s−1. La surestimation est au plus s/2−1 ≤ (F+1)/2, et la sous-estimation maximale relative se produit à c=s et vaut s/[2(F+s)] ≤ 1/2.

Horloge modulo N+1. À l’instant d’expiration, âge N avant réutilisation du même résidu. Les timestamps des buckets sont distincts, donc au plus un expire par mise à jour. Toute taille s active vérifie s≤N, puisque s−1 1 plus récents sont présents, en plus du 1 de fin. Au plus deux buckets par puissance de deux donnent 2·bit_length(N) entrées. Taille et horodatage codables en O(log N) bits, donc O(log² N) bits dans le modèle compact. En Python les objets et listes ont une surcharge supplémentaire et les opérations de fusion peuvent déplacer des éléments.

## GK historique

Pour chaque tuple (v,g,Δ), le rang minimal r est la somme préfixe des g, et le maximal est r+Δ. Un nouveau point intérieur augmente la somme des g de 1. Le g+Δ du successeur borne la largeur du trou qui précède ce successeur, donc Δ = max(0,⌊2εn⌋−1) couvre le trou. Une extrémité est exacte à l’insertion. Fusionner un tuple dans son successeur préserve les bornes de ce dernier et augmente son g, sous la condition g₁+g₂+Δ₂≤⌊2εn⌋. Sans compression et au début, les gaps unitaires donnent des rangs exacts.

Pour 0<q<1, poser t=qn sans décalage. Quand εn≥1/2, on cherche le premier tuple de borne haute supérieure à t+εn et on renvoie son prédécesseur. Celui-ci a une borne haute ≤t+εn. Puisque la borne haute du successeur dépasse t+εn et que son g+Δ≤2εn, la borne basse du prédécesseur dépasse t−εn. Si aucun tuple ne dépasse le seuil, le maximum est admissible. Si le minimum dépasse le seuil, aucun rang admissible n’existe et le minimum est rendu. Quand εn<1/2, la représentation est exacte et le rang entier valide le plus proche est utilisé (égalité départagée vers l’entier pair). Pour q=0 et q=1 on impose les extrémités exactes. Avec des répétitions, une valeur occupe tous les rangs de #strictement-inférieurs+1 à #inférieurs-ou-égaux. Un ordre stable entre ex aequo permet de raisonner sur les occurrences. La variante conserve les invariants de rang de GK avec balayage simplifié. L’espace du GK original est O((1/ε)log(εn)) entrées quand εn est suffisamment grand et O(n) au démarrage. Ce théorème dépend d’une autre stratégie de compression.

### Espace de la compression GK utilisée

Cette preuve concerne le balayage de notre variante, en **nombre de tuples**, pour ε fixé. Elle établit une borne sous-linéaire moins serrée que celle de GK classique. Le code calcule $K_t=\lfloor 2\varepsilon t\rfloor$ avec des entiers à partir de la valeur rationnelle exacte du flottant ε.

1. Juste après une compression à l’instant $t$, pour toute paire adjacente de survivants $(i,j)$ dont le prédécesseur $i$ n’est pas le minimum, $g_i+g_j+\Delta_j>K_t$. Sinon le balayage aurait fusionné $i$ dans $j$. Le balayage va de droite à gauche. Une fusion ultérieure depuis la gauche peut augmenter $g_i$ et préserve l’inégalité. La somme des $g$ vaut $t$.
2. Pour un survivant $j$ inséré au temps $s_j$, son $\Delta_j$ ne change jamais et vérifie $\Delta_j\le 2\varepsilon s_j$, y compris pour les extrêmes où il vaut zéro. Fixons un âge entier $a\ge1/\varepsilon$. Pour un successeur d’âge au moins $a$, $K_t-\Delta_j\ge 2\varepsilon a-1\ge\varepsilon a$. Hors les deux premiers tuples, chaque tel successeur définit une paire dont la somme des $g$ est donc supérieure à $\varepsilon a$.
3. Chaque $g$ se trouve dans au plus deux paires adjacentes. Les vieux successeurs ainsi comptés sont donc au plus $2t/(\varepsilon a)$. Les tuples plus jeunes sont au plus $a$, car une insertion crée un seul tuple. La taille juste après compression est bornée par $2+a+2t/(\varepsilon a)$.
4. Si $t\ge1/\varepsilon$, prendre $a=\lceil\sqrt{t/\varepsilon}\rceil$ donne $O(\sqrt{t/\varepsilon})$. La période $p$ utilisée par le code est $\Theta(1/\varepsilon)$ pour $0<\varepsilon<1/2$. Le premier balayage arrive au premier multiple de $p$ pour lequel $K_t\ge2$, donc au plus $p-1$ insertions après $\lceil1/\varepsilon\rceil$. Ensuite, il y a au plus $p-1$ insertions depuis le dernier balayage. Dès $n\ge1/\varepsilon$, $\sqrt{n/\varepsilon}\ge1/\varepsilon$ absorbe cette contribution, y compris avant le premier balayage. Pour $n<1/\varepsilon$, la borne triviale $n$ suffit. On obtient $O(\min(n,\sqrt{n/\varepsilon}))$ tuples, tampon de compression compris à un facteur constant près.

Les compteurs Python ont une taille qui peut croître avec $\log n$. Cette preuve ne revendique donc ni une borne en octets constants par tuple ni la borne originale $O(\varepsilon^{-1}\log(\varepsilon n))$. Le test par propriétés vérifie l’inégalité des paires survivantes et la conservation de la masse des rangs.

## Quantiles récents par blocs

### Requête groupée et budget

Le lot P50/P95/P99 trie les mêmes représentants une seule fois. Les rangs cibles triés sont consommés lors d’un balayage cumulatif commun. L’ordre demandé, les doublons de requêtes et les extrémités sont conservés. Sur $R$ représentants et $Q$ probabilités, le temps est $O(R\log R+Q\log Q+R+Q)$ et l’espace de travail $O(R+Q)$.

Poser B=⌊√N⌋ et S=⌈εB⌉. Le bloc en cours est exact. Dans chaque bloc fermé et trié, les groupes successifs de S valeurs sont représentés par leur maximum pondéré par leur effectif. Pour une valeur x, seule une grappe par bloc peut être coupée par x, donc la fonction cumulative pondérée sous-compte d’au plus S−1 par bloc. La fenêtre inclut temporairement u≤B−1 valeurs périmées du premier bloc. Une cible discrète ⌈qn⌉ décalée à ⌈q(n+u)⌉ augmente d’au plus u. En retirant les anciennes observations, le déficit de rang est borné par u. Le dépassement de rang est borné par u + (S−1) fois le nombre de blocs fermés, en évaluant les individus strictement sous la valeur retournée. Une valeur périmée peut tomber entre deux rangs actifs et on mesure alors l’écart à son insertion. La borne est additive, distincte de la borne GK.

Il faut O(B + (N/B)·min(B,1/ε)) entrées pour les blocs, soit O(√N/ε) à ε fixe, hors FIFO d’évaluation et historique d’affichage. Les compteurs temporels de cette structure restent absolus. Pour des petites fenêtres ou ε très faible, S=1 et l’état peut approcher N valeurs. Les requêtes trient les représentants et ne fusionnent aucun résumé GK.

### Deux inégalités pour le seuil retourné

Soit m=min(n,N), u le nombre de périmés dans le bloc frontière, C le nombre de blocs fermés retenus et E=C(S−1). Pour chaque seuil x, comparer les comptes stricts et larges dans le multiensemble retenu et sa représentation pondérée. Le résumé sous-compte chacun d’au plus E, car un seul groupe trié peut chevaucher chaque seuil dans un bloc. Le passage du multiensemble retenu à la fenêtre retire au plus u contributions. Pour le seuil x retourné, les comptes pondérés W₍<₎ et W₍≤₎ satisfont W₍<₎<k'≤W₍≤₎, où k'=max(1,⌈q(m+u)⌉). Comme k≤k'≤k+u pour k=max(1,⌈qm⌉), les comptes exacts L=#(a<x) et U=#(a≤x) vérifient L<k+u+E et U≥k−u. Ces inégalités restent valables quand x est absent. Pour N=4 et le flux [99,1,2,3,4], la requête maximale retourne 99 alors que L=U=4. Le 99 est un seuil d’insertion au-dessus du dernier actif et n’occupe aucun rang actif.

Il reste au plus ⌈N/B⌉+1 blocs fermés et B−1 valeurs ouvertes. Le nombre de représentants par bloc est ⌈B/S⌉. La borne explicite est donc B−1+(⌈N/B⌉+1)⌈B/S⌉ entrées, plus O(N/B) métadonnées. B=⌊√N⌋ équilibre la taille brute et le nombre de blocs à ε fixe. Le terme de frontière peut atteindre B−1.
