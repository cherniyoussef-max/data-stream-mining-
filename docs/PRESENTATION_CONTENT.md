# Trame de soutenance

| Partie | Orateur proposé | Contenu à montrer |
|---|---|---|
| 1. Introduction | Nasr | Flux de latences, stockage limité, deux horizons d’analyse. |
| 2. Fondements | Nasr | Transformer des événements en indicateurs utiles à la décision. Comparer les quatre types de fenêtres, montrer les exercices R et A-Res. |
| 3. État de l’art | Wajdi | Un tirage pondéré réparti sur des lots, les fréquences d’une fenêtre, l’évaluation du P99 sur deux distributions, une jointure clients–commandes, un univers entier pour sketch optimal, et un P99 conditionnel à la charge pour la régression. |
| 4. Méthodes | Wajdi | Tracer DGIM au 7e bit et GK au 4e élément. Montrer les figures 04 et 08. |
| 5. Technologies | Youssif | Python et listes/tas, pytest, SciPy, Matplotlib, Streamlit. Montrer les commandes reproductibles et la figure mémoire. |
| 6. Application et conclusion | Youssif | Lancer le scénario de dérive. Montrer l’alerte puis la récupération et la figure 14. Expliquer la frontière des blocs et les hypothèses des données simulées. |

Phrase finale proposée : « Pendant l’incident, la fenêtre récente réagit. Après l’incident, elle revient à la normale alors que le résumé historique conserve la trace des latences élevées. »
