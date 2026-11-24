# Validation indépendante V3

## Baseline et corrections

La [revue initiale](FINAL_REVIEW_V3.md) a confirmé 87 tests de référence, 41 slides statiques et un PDF à auteur anonyme. La V3 conserve les API et algorithmes validés. Elle ajoute l’affichage des rangs GK, un parcours Streamlit, des analyses de rafales et un balayage de sensibilité sur une trace identique. Les méthodes et résultats sont intégrés à un nouvel article LaTeX plutôt qu’à une extension de l’ancien PDF.

## Contrôles scientifiques

- `python -m pytest -v` : **87 réussites, 0 échec, 0 omis**. Les avertissements de plugins installés sont consignés dans [le journal](../results/pytest_results.txt).
- T1 : Pearson 93,316, p=0,642188, p ajustée=0,380806. T2 : essais k=1,2,3, poids égaux, distincts et extrêmes.
- T3/T4 : invariants structuraux et borne vérifiés. Maximum DGIM du benchmark : 33,33 %. T5 : rang admissible, cas de doublons et cibles près de zéro. Maximum GK normalisé : 5 % pour ε=0,05.
- Les deux profils ont été rejoués : 2 710 et 6 758 mesures. Étude mémoire pour six tailles, 36 configurations. Pour le GK simplifié, 250 points de croissance sur dix ordres, cinq ε et cinq longueurs. Le choix C conserve la variante testée avec sa garantie de rang. Ces mesures ne prouvent pas la borne d’espace du GK original.
- Les 6 000 requêtes P99 récentes montrent au plus six rangs d’écart et 2,00 % d’erreur normalisée au maximum. Zéro violation de la borne de CDF. Les exports distinguent population active, budget de compression et valeurs périmées.
- À N=10 000 et ε=0,05, le profil standard enregistre 327 080 octets de pic FIFO contre 191 752 pour les blocs, et 10 000 contre 2 000 entrées. Le protocole complémentaire mesure séparément le coût de tri en requête.
- Scénario principal : incident 401–800, alerte 403, retour 998. L’accord avec la règle exacte est de 100 % dans ce scénario. Contre les étiquettes d’incident, exactitude 83,42 %, précision 66,89 %, rappel 99,50 %, spécificité 75,38 % et F1=0,80. Douze configurations supplémentaires varient N et ε sur le même flux.

## Documents, navigateur et soutenance

- Sept articles récents et cinq fondateurs avec DOI. Les [fiches](ARTICLE_ANALYSIS_DETAILED.md) distinguent résultats primaires, schémas pédagogiques et protocoles locaux. La vérification intégrale de tous les tableaux et dépôts d’articles n’est pas achevée.
- [Article LaTeX](report/rapport-projet4-final.pdf) : huit pages, auteurs renseignés, citations numérotées, figures et tables, architecture, états de l’art et protocole. Compilation Tectonic. Les huit pages ont été rendues et contrôlées visuellement.
- [PowerPoint](../presentation/Data_Stream_Mining_Final_Anime.pptx) : 44 diapositives et 44 notes, 18 GIF incorporés, 99 images distinctes. Les médias utilisent de 3 à 16 états d’animation. [Validation détaillée](../presentation/ANIMATION_VALIDATION.md). Impress ouvre le PPTX, Chrome lit les 18 GIF extraits. Lecture directe dans Microsoft PowerPoint non effectuée.
- [Journal Chrome](../results/browser_validation/report.json) : démarrage et pause répétés, vérification du minuteur, changements de paramètres et lecture du CSV téléchargé. 500 lignes concordantes avec l’affichage et aucune erreur console.
- Cinq exercices dont celui des blocs, quatre scripts PDF synchronisés et 57 réponses. Durées indicatives : Nasr 4 min 44 s, Wajdi 5 min 38 s, Youssif 4 min 56 s, hors questions et démonstration libre.

## Verdict et reproduction

Le code est exploitable pour la démonstration. La [matrice](REQUIREMENTS_TRACEABILITY.md) traite séparément les deux exigences partielles, à savoir le détail des études et le théorème d’espace de la variante GK. Les données sont synthétiques et la procédure d’alerte reste un seuil expérimental. L’article, le PowerPoint, sa version statique et les supports oraux sont livrés avec leurs sources.

```bash
python -m pip install -r requirements.txt
python -m pytest -v
python demo.py
python -m evaluation.benchmark --profile quick --output results/quick
python -m evaluation.benchmark --profile full
python -m evaluation.final_study
python -m evaluation.sensitivity
python -m evaluation.article
python -m streamlit run dashboard/app.py --server.address 127.0.0.1
```
