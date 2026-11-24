# Exercices corrigés

## 1. Algorithm R

Flux A à H, k=3, graine 42. Remplissage : [A], [A,B], [A,B,C]. Puis indices 0,0,5,2,3 pour D à H. États successifs [D,B,C], [E,B,C], [E,B,C], [E,B,G], [E,B,G]. Les indices 5 et 3 sont refusés. Chaque position a une probabilité 3/8. Temps constant et trois places.

## 2. A-Res

k=2, poids de A,B,C,D : 1,2,4,2. U: 0,25 ; 0,25 ; 0,25 ; 0,16. Clés U^(1/w) : 0,25 ; 0,50 ; √0,5 ≈ 0,7071 ; 0,40. Le tas garde A,B, puis remplace A par C, puis rejette D. L’ordre des priorités logarithmiques est identique. La mise à jour du tas coûte au plus O(log k), avec O(k) entrées.

## 3. DGIM

N=8, flux `11111111000000000000`. Ci-dessous les tailles dans l’ordre du plus récent au plus ancien. À t=7, les buckets de tailles 1 finissant en 6 et 5 fusionnent en un bucket de taille 2 finissant en 6. Ensuite ceux de taille 2 finissant en 4 et 2 fusionnent en taille 4 horodatée à 4. À t=12, cet horodatage atteint l’âge 8 et expire.

| t | Tailles | Exact | Estimé |
|---|---|---:|---:|
| 1, 2 | 1 puis 1,1 | 1, 2 | 1, 2 |
| 3, 4 | 1,2 puis 1,1,2 | 3, 4 | 2, 3 |
| 5, 6 | 1,2,2 puis 1,1,2,2 | 5, 6 | 4, 5 |
| 7, 8 | 1,2,4 puis 1,1,2,4 | 7, 8 | 5, 6 |
| 9, 10, 11 | 1,1,2,4 | 7, 6, 5 | 6 |
| 12, 13 | 1,1,2 | 4, 3 | 3 |
| 14, 15 | 1,1 puis 1 | 2, 1 | 2, 1 |
| 16–20 | vide | 0 | 0 |

À t=11 l’erreur est 1/5=20 %. Le nombre de buckets est logarithmique en N.

## 4. GK

Flux [5,1,3,2,4,6], ε=0,25, compression aux multiples de 2 lorsque le seuil atteint 2.

| Valeur entrante | Résumé après traitement (v,g,Δ) |
|---|---|
| 5 | (5,1,0) |
| 1 | (1,1,0) (5,1,0) |
| 3 | (1,1,0) (3,1,0) (5,1,0) |
| 2 | (1,1,0) (2,1,1) (5,2,0) |
| 4 | (1,1,0) (2,1,1) (4,1,1) (5,2,0) |
| 6 | (1,1,0) (4,2,1) (6,3,0) |

À t=4, le tuple de 3 fusionne dans celui de 5 puisque 1+1+0≤2. À t=6, le tuple de 4 a la borne [3,4]. Pour q=0,5 la cible est 3 et la borne supérieure admissible 4,5. Le 6 la dépasse, donc la médiane approchée est 4, de rang réel 4, avec erreur 1≤1,5. Temps d’insertion dominé par le déplacement dans la liste et balayage linéaire du résumé pour la requête.

## 5. Exemple complémentaire : fenêtre récente

N=4, B=2, ε=0,2, S=1 et flux [99,1,2,3,4,5]. À t=4 les blocs fermés sont [(1,1),(99,1)] et [(2,1),(3,1)]. À t=5, 99 est périmé, mais le premier bloc contient encore 1. Le bloc ouvert contient 4. Le maximum calculé est 99. Dans [1,2,3,4], ses comptes strict et large valent 4 et 4. La cible est 4 et le budget vaut 1. À t=6 le premier bloc expire, [4,5] ferme le troisième bloc, la cible maximale donne 5 et le budget retombe à 0.
