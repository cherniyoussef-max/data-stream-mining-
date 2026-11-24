# Démonstration locale

1. Lancer `python -m streamlit run dashboard/app.py --server.address 127.0.0.1`.
2. Garder « dérive », graine 42 et les seuils par défaut. Avancer d’un événement, puis d’un lot. Comparer les échantillons uniformes et pondérés.
3. Démarrer, mettre en pause près d’un incident, et examiner les âges et tailles des buckets. Avec N≥8 et des bits 1 consécutifs, le septième 1 produit deux fusions. Pour observer ce passage, avancer d’un événement à la fois.
4. Comparer le P99 récent, le P99 exact (option d’évaluation) et le P99 historique. Utiliser « Simuler un incident » et « Revenir à la normale » pour forcer les changements.
5. Exporter l’historique affiché (au plus 500 événements) et présenter les figures de l’expérience.

Le mode automatique avance périodiquement lorsqu’une session est active. L’alerte est initialisée après min(20,N) points et se déclenche si la médiane ou le P99 récent dépasse son seuil. L’état de rétablissement dure un événement. Il n’y a pas d’hystérésis. Utiliser le CLI pour une démo sans serveur.
