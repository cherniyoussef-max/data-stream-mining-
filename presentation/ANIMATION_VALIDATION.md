# Validation des animations

La base contenait 41 pages statiques et huit PNG. La V3 contient 44 diapositives, 44 notes et **18 GIF incorporés avec 99 images distinctes au total**. Le paquet ZIP PPTX est valide. Chaque GIF est lié depuis sa diapositive via une relation d’image interne, avec type `image/gif`. Aucun téléchargement externe n’est nécessaire. Aucun XML de timing PowerPoint natif, aucune transition ni vidéo n’est utilisé.

| Famille | Images par GIF |
|---|---|
| Arrivée et quatre modèles de fenêtres | 5 par GIF |
| Algorithm R, A-Res, DGIM, GK | 8, 4, 16, 7 |
| Blocs récents | 8 |
| Sept illustrations d’articles | 3 par GIF |
| Incident et rétablissement | 10 |

Chaque animation utilise des états de deux secondes et un état final de 3,8 secondes, puis boucle. [Preuve machine](animation_validation.json) : numéros des diapositives, durées, empreintes, nombre d’images uniques et détection de changement de pixels sous Chrome pour les 18 GIF extraits du PPTX. LibreOffice Impress a ouvert et exporté le PPTX animé. Le contrôle Chrome porte sur la lecture des GIF extraits. La lecture dans Microsoft PowerPoint n’a pas été testée. Le PDF d’affiches présente les états finaux, et les notes contiennent la séquence complète.
