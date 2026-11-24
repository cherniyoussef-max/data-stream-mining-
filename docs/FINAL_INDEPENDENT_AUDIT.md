# Audit indépendant

Base `adf2437`, branche `codex/project4-validation`, origine SSH `naseroz/dtata-stream-mining`, arbre initial propre. Baseline reproduite dans un nouveau processus : 71 tests réussis, aucun échec, trois avertissements de dépendances. Le rapport précédent compte sept pages.

| Priorité | Constat |
|---|---|
| P0 | GK relevait systématiquement qn à 1, ce qui peut modifier la borne brute quand un rang admissible existe déjà. La borne d’espace de GK original reste non démontrée pour la compression utilisée. |
| P1 | Les quantiles récents peuvent retourner un seuil périmé. Il faut distinguer les comptes de CDF des rangs d’observations. Il manquait également un oracle d’alerte et des mesures de croissance. |
| P1 | ACM confirme le DOI 10.1145/3651610, absent du corpus précédent. |
| P2 | Le minuteur et le téléchargement demandaient un test navigateur. Les supports de soutenance restaient à livrer. |
| P3 | Une trace réelle demeure optionnelle. |
