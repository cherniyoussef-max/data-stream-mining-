# Validation des animations

La V4 conserve 44 diapositives, 44 notes et **18 GIF incorporés avec 99 images distinctes au total**. Les empreintes SHA-256 des 18 GIF sont identiques à celles du PPTX de la V3. Le paquet ZIP PPTX est valide. Chaque GIF est lié depuis sa diapositive via une relation d’image interne de type `image/gif`.

| Famille | Images par GIF |
|---|---|
| Arrivée et quatre modèles de fenêtres | 5 par GIF |
| Algorithm R, A-Res, DGIM, GK | 8, 4, 16, 7 |
| Blocs récents | 8 |
| Sept illustrations d’articles | 3 par GIF |
| Incident et rétablissement | 10 |

Chaque animation utilise des états de deux secondes et un état final de 3,8 secondes, puis boucle. [Preuve machine](animation_validation.json) : numéros des diapositives, durées, empreintes, nombre d’images uniques et détection de changement de pixels sous Chrome pour les 18 GIF extraits du PPTX. LibreOffice Impress a ouvert et exporté le PPTX animé. Le contrôle Chrome porte sur la lecture des GIF extraits. La lecture dans Microsoft PowerPoint n’a pas été testée. Le PDF d’affiches présente les états finaux, et les notes contiennent la séquence complète.
