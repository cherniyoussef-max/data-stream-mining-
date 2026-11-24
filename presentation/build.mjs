import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const read = async path => JSON.parse(await fs.readFile(path,"utf8"));
const analysis = await read("results/final_study.json");
const manifest = await read("presentation/animations/trace.json");
const statistic = (await read("results/statistical_results.json")).uniform;
const nTests = (await fs.readFile("results/pytest_results.txt","utf8")).match(/(\d+) passed/)[1];
const incident = analysis.alerts[1];
const names = ["Nasr elhak Khemiri","Wajdi Zayoud","Youssif Cherni"];
const sections = ["Introduction","Fondements théoriques","État de l’art","Approches et méthodes","Technologies","Conclusion et application concrète"];
const rows = [];
function add(section,title,focus,oral,extra={}) {
  rows.push({section,title,focus,oral,owner:names[section<2?0:section===2?1:2],...extra});
}
add(0,"Échantillonnage et fenêtres glissantes","Surveillance des latences en temps réel",
    "Nous sommes étudiants en Master D3S à l’ISTIC. Nous étudions comment examiner un flux de latences sans stocker toutes ses mesures. Le problème se découpe en échantillonnage, comptage et quantiles.");
add(0,"Les mesures arrivent sans taille finale","Une observation à la fois",
    "Une mesure élevée peut correspondre à un pic isolé. Quand les latences élevées se succèdent, l’effet apparaît aussi dans le P99 de la fenêtre. Suivre l’arrivée et les deux P99 dans la trace.",
    {anim:"flux"});
add(0,"Question et objectifs du projet","Conserver un échantillon et mesurer l’état récent",
    "La question est de savoir quels résumés donnent une estimation suffisamment précise avec peu d’état. Les quatre méthodes imposées sont R, A-Res, DGIM et GK. Notre prototype combine ces méthodes et des blocs récents pour la surveillance.",
    {items:["Échantillon de taille k sur un flux inconnu","Comptage des 1 et quantiles approchés","Validation T1–T5 et démonstration reproductible"]});
add(0,"Contributions","Implémentations, preuves et évaluation",
    "Nous avons implémenté les algorithmes classiques, formalisé le budget des blocs, comparé les décisions à deux références et testé l’interface dans Chrome. Nous avons gardé l’oracle FIFO facultatif afin de distinguer les coûts.");
add(0,"Plan de la soutenance","Six parties de la question à l’application",
    "Je présente le contexte et les quatre modèles de fenêtre. Wajdi situe sept travaux scientifiques et ouvre la partie méthodes. Youssif poursuit avec la fenêtre récente, les outils et la démonstration.",
    {items:sections});
add(1,"Données, information, connaissance, décision","Du signal brut à une action justifiable",
    "Une mesure de 156 ms est une donnée. Le P99 et les dépassements sont des informations. Une hausse durable de la fenêtre indique une détérioration. L’opérateur décide alors d’examiner l’alerte, puis de confirmer le rétablissement.",
    {items:["156 ms → mesure brute","P99 et bits lents → indicateurs","Hausse durable → interprétation","Alerte → diagnostic ou confirmation du retour"]});
add(1,"Médiane, P99 et unités d’erreur","Le haut de la distribution réagit aux extrêmes",
    "Dans la série [20, 21, 22, 23, 180], la médiane vaut 22 et le P99 au rang supérieur vaut 180. Une petite erreur de rang peut donc produire une grande erreur en millisecondes.",
    {items:["Rang médian : 3 sur 5","P99 : ceil(0,99 × 5) = 5","Écart de rang ≠ écart de valeur"]});
for (const [key,title,focus,oral] of [
  ["landmark","Fenêtre à repère fixe","Landmark","Le repère B reste fixe. La fenêtre grandit à chaque arrivée et l’influence des anciens points est conservée."],
  ["tumbling","Fenêtres disjointes","Tumbling","Le passage de la troisième à la quatrième position ouvre un nouveau bloc. Une observation appartient à un seul bilan."],
  ["glissante","Fenêtre de taille fixe","Sliding window","Trois positions sont mises en évidence. Quand une valeur arrive, la plus ancienne des trois sort. Nos fenêtres de surveillance utilisent les indices d’événement."],
  ["decroissance","Décroissance exponentielle","Poids en fonction de l’âge","L’arrivée reçoit le poids 1 et les poids précédents sont divisés par deux. Les anciens points perdent de l’influence graduellement. Je passe la parole à Wajdi pour les travaux récents."]
]) add(1,title,focus,oral,{anim:key});

const articles = [
  ["Tirage pondéré parallèle","Hübschle-Schneider et Sanders · ACM TOMS 2022","Le coût séquentiel devient dominant sur des lots pondérés. L’objectif est de distribuer le travail sans changer la loi de tirage.","Table alias et lots","Le tableau 1 distingue les coûts de construction et de requête selon la règle et le modèle parallèle. La masse 3 ou 9 de l’animation est un exemple pédagogique.", "10.1145/3549934"],
  ["Expiration pour les sketches","Gou et al. · IEEE TKDE 2023","Un historique complet ne suffit pas à isoler les fréquences récentes. L’étude utilise notamment CAIDA, Web, Zipf et StackOverflow (§8.1).","Zones temporelles","Le cadre adapte des sketches à une frontière temporelle. Les expériences dépendent de la requête et du budget ; notre P99 traite un autre agrégat.", "10.1109/TKDE.2022.3151140"],
  ["Comparer des esquisses de quantiles","Fernando, Bindra et Daudjee · EDBT 2023","Même problème, cinq méthodes, mais des choix de représentation et d’erreur différents. Jeux Pareto, Uniforme, NYT et Power.","Résultat conditionné au jeu","Dans la figure 6b, les cinq méthodes restent sous 1 % d’erreur relative moyenne sur le jeu uniforme. La figure 6a montre que la queue Pareto change le résultat.", "10.48786/edbt.2023.34"],
  ["Sélection sur des jointures","Dai, Hu et Yi · SIGMOD 2024","La taille d’une jointure dépasse parfois celle des entrées. L’objectif est d’échantillonner ses résultats sans les matérialiser.","Index et réservoir à prédicat","L’index propose des candidats compatibles. La section expérimentale inclut le graphe Epinions et des requêtes relationnelles. Notre réservoir cible une autre population.", "10.1145/3654921"],
  ["Résumé déterministe par comparaisons","Gribelyuk, Sawettamalya, Wu et Yu · PODS 2024","Peut-on simplifier un sketch déterministe tout en conservant une bonne borne d’espace dans le modèle de comparaison ?","Une borne en éléments stockés","Le théorème publié borne asymptotiquement l’état par (2+o(1)) ε⁻¹ log(εn). Notre passe sur les tuples n’implémente pas cette méthode.", "10.1145/3651610"],
  ["Estimation sur univers entier","Gupta, Singhal et Wu · FOCS 2024","Avec un univers entier borné, peut-on gagner de la place par rapport au modèle qui autorise seulement les comparaisons ?","L’hypothèse du modèle est essentielle","Les opérations sur l’univers permettent O(1/ε) mots dans le cadre théorique étudié. Le découpage illustré explique l’information disponible, pas le pseudocode exact.", "10.1109/FOCS61266.2024.00075"],
  ["Inférence conditionnelle","Xie, Yan, Jiang et Kong · Journal of Econometrics 2025","Une régression quantile suit un quantile de réponse associé à des covariables. Les lignes historiques ne sont pas conservées intégralement.","Mise à jour d’un modèle par lots","Le lissage et les résumés de lots rendent la mise à jour possible. Les applications de l’article incluent les vélos à Séoul et les fonds indiciels.", "10.1016/j.jeconom.2024.105924"],
];
for (const [index,[title,venue,problem,mechanism,result,doi]] of articles.entries()) {
  const source=`https://doi.org/${doi}`;
  add(2,title,venue,problem,{source,items:[problem]});
  add(2,mechanism,venue,result,{source,anim:`a${index+1}`});
}
add(2,"Comparaison fonctionnelle","Sept travaux, plusieurs populations et cibles",
    "Lire les deux colonnes. L’expiration d’une fréquence, l’uniformité d’une jointure et l’inférence conditionnelle s’appliquent à des populations et à des objectifs différents.",
    {table:[["Article","Cible"],["Hübschle-Schneider–Sanders","Pondération parallèle"],["Gou et al.","Fréquences récentes"],["Fernando et al.","Quantiles descriptifs"],["Dai et al.","Uniformité de jointures"],["Gribelyuk et al.","Rang comparatif"],["Gupta et al.","Rang sur entiers"],["Xie et al.","Quantiles conditionnels"]]});
add(2,"Comparaison scientifique","La garantie dépend du problème et du modèle",
    "Deux articles formalisent l’espace dans des modèles différents. Fernando et ses collègues étudient des mesures. D’autres articles traitent l’expiration, la loi de tirage ou l’inférence. Aucune méthode avancée n’est présentée comme implémentée dans le prototype.",
    {table:[["Axe","Exemples et limites"],["Tirage","Loi d’inclusion, tas ou construction parallèle"],["Fenêtres","Expiration selon la structure et la requête"],["Rang","Borne additive, modèle comparatif ou entier"],["Statistique","Erreur empirique ou inférence conditionnelle"]]});

add(3,"Architecture logicielle","Un moteur commun à la simulation, aux tests et à l’interface",
    "Le générateur synthétique envoie une mesure à Monitor.add. Le moteur met à jour chaque résumé et, sur demande, l’oracle exact. Le CLI et Streamlit consomment le même état. Les scripts d’évaluation exportent les mesures.",
    {owner:names[1],arch:true});
add(3,"Algorithm R","O(k) entrées et mise à jour O(1)",
    "Avec k égal à trois, la trace montre les trois admissions initiales, les remplacements D puis E, le rejet F, l’admission G et le rejet H. Une position a une probabilité k/n. T1 compare les fréquences à 1000.",
    {owner:names[1],anim:"reservoir"});
add(3,"Réservoir A-Res","Clé U^(1/w) et minimum du tas",
    "L’animation impose les mêmes U que l’exercice. C a une priorité supérieure à A et l’éjecte. D est rejeté. Le test T2 compare les probabilités pour k égal à un, deux ou trois.",
    {owner:names[1],anim:"ares"});
add(3,"DGIM : compter les bits égaux à 1","Au plus deux groupes par taille, erreur relative ≤50 %",
    "À sept, deux fusions se propagent. Observer le huitième bit puis les zéros. À douze, l’ancien groupe expire. La borne utilise les bits égaux à 1 plus récents et le demi-compte du groupe frontière.",
    {owner:names[1],anim:"dgim"});
add(3,"GK : retrouver un rang historique","Tuples (valeur, g, Δ) et tolérance εn",
    "Suivre les six arrivées. Les rangs minimal et maximal encadrent chaque valeur. Le prédécesseur admissible donne 4 pour une cible de rang 3. L’erreur est de 1. La mémoire de la variante est mesurée, sans théorème général.",
    {owner:names[1],anim:"gk"});
add(3,"Quantiles récents par blocs","État brut entre les fermetures, résumés pondérés après tri",
    "Le bloc ouvert reste exact. Un groupe fermé transmet un maximum et son effectif. Le premier bloc peut retenir des valeurs périmées. À t égal à 20, il expire et la valeur 99 ne contribue plus.",
    {anim:"blocs"});
add(3,"Borne de rang récente","Budget = périmés + omissions des groupes",
    "Pour une cible k, la cible de la population retenue peut augmenter d’au plus u. La compression sous-compte chaque seuil d’au plus S−1 par bloc. Donc C strict est inférieur à k+u+E et C large vaut au moins k−u. Un seuil périmé se juge par ces comptes.",
    {items:["u < B positions périmées au plus","E = nombre de blocs fermés × (S − 1)","FIFO exacte facultative, P99 récent séparé de GK"]});
add(3,"Tests T1 à T5","Garanties et mesures jouent des rôles distincts",
    `T1 donne p = ${statistic.p.toFixed(4)}. T2 teste les marginales pondérées. T3 et T4 contrôlent le compte et la structure de DGIM. T5 compare les rangs avec et sans doublons. Le journal final compte ${nTests} tests.`,
    {table:[["Tests","Preuve expérimentale"],["T1–T2","Inclusion uniforme et pondérée"],["T3–T4","Erreur relative et invariants par insertion"],["T5","Rangs exacts et cas près de zéro"]]});
add(3,"Mémoire et temps, même horizon","FIFO et blocs récents jusqu’à N = 50 000",
    "La FIFO insère rapidement mais trie davantage de valeurs à la requête. À N=10 000 et epsilon 0,05, les blocs gardent 2 000 entrées. À précision plus fine, les groupes peuvent rester unitaires.",
    {img:"results/figures/18_memoire_echelle.png"});

add(4,"Technologies du prototype","Le noyau s’exécute localement",
    "Python rend les algorithmes lisibles. heapq expose le minimum d’A-Res. pytest automatise les assertions et SciPy évalue le chi carré. Matplotlib lit les mesures et Streamlit offre le pilotage.",
    {table:[["Outil","Rôle"],["Python · heapq","Algorithmes, listes et tas"],["pytest · SciPy","Tests et statistiques"],["Matplotlib · Streamlit","Figures et interface"],["Git · GitHub","Versions et collaboration"]]});
add(4,"Plateformes étudiées","Options pour une mise en production future",
    "Kafka transporte des événements. Flink et Spark peuvent les traiter en flux réparti. DataSketches fournit des structures approchées réutilisables. Notre prototype sert à examiner les états et n’en déploie aucune.",
    {table:[["Plateforme","Fonction"],["Kafka","Collecte et transport"],["Flink","Calcul et fenêtres"],["Spark Structured Streaming","Traitement distribué"],["Apache DataSketches","Résumés approchés prêts à l’emploi"]]});
add(5,"Tableau de bord Streamlit","Navigation, paramètres et oracle optionnel",
    "Montrer la configuration de 200 positions et les indicateurs récents. Les onglets exposent réservoirs, groupes DGIM et tuples GK. Dans Chrome, le test alterne démarrage et pause et contrôle le CSV téléchargé.",
    {img:"presentation/screenshots/alerte.png"});
add(5,"Incident, détection et retour","Trace réelle du scénario simulé",
    "Le générateur introduit l’incident à 401. L’alerte arrive à 403. Après le retour à 801, le P99 récent diminue au fil des expirations. Le rétablissement apparaît à 998 pendant que l’historique reste élevé.",
    {anim:"incident"});
add(5,"Deux références d’alerte","Règle exacte et étiquette du générateur",
    `Le scénario de référence produit ${analysis.alerts[0].tp+analysis.alerts[0].tn} décisions identiques à la règle exacte. Contre les étiquettes, F1 vaut ${incident.f1.toFixed(2)}, avec ${incident.fp} faux positifs et ${incident.fn} manqués. Les fausses alertes incluent le délai de vidange.`,
    {img:"results/figures/21_confusion.png"});
add(5,"Sensibilité de la surveillance","Modifier N et ε sur la même trace",
    "Les paramètres, la graine et les seuils restent fixes sauf N et epsilon. Expliquer sur le graphe comment une grande fenêtre peut retarder le retour et modifier le score face aux étiquettes.",
    {img:"results/figures/20_sensibilite.png"});
add(5,"Conclusion et perspectives","Des résumés distincts rendent les décisions interprétables",
    "Les résultats répondent à notre question : R et A-Res échantillonnent, DGIM compte, et les deux horizons de quantiles répondent à des usages distincts. Tester une vraie trace, une hystérésis et la compression GK originale serait la suite.",
    {items:["T1–T5 validés, budget de rang récent explicite","Alerte reproductible, pareil à la règle exacte sur le cas principal","Limites : données simulées, absence de preuve d’espace pour la variante GK"]});
add(5,"Références et questions","Douze notices dans le rapport et le BibTeX",
    "Les fondations viennent de Vitter, Efraimidis–Spirakis, Datar et al., Greenwald–Khanna et Arasu–Manku. Les sept DOI récents sont indiqués dans leurs diapositives et dans le rapport.",
    {items:["Vitter, 1985 · Reservoir Sampling","Efraimidis–Spirakis, 2006 · A-Res","Datar et al., 2002 · DGIM","Greenwald–Khanna, 2001 · rang historique","Arasu–Manku, 2004 · quantiles glissants","Merci. Questions et démonstration libre."]});

const deck=Presentation.create({slideSize:{width:1280,height:720}});
const navy="#112841", teal="#006D73", gray="#40576B";
function box(slide, content, left, top, width, height, size, color=navy, bold=false, fill="none") {
  const shape=slide.shapes.add({name:content.slice(0,40),geometry:"textbox",
    position:{left,top,width,height},fill,line:{fill:"none",width:0}});
  shape.text=content;
  shape.text.style={fontFamily:"Liberation Sans",fontSize:`${size}pt`,color,bold,verticalAlignment:"middle"};
}
async function image(slide,path,name,top,height) {
  const data=await fs.readFile(path);
  slide.images.add({blob:data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength),contentType:"image/png",
    alt:name,fit:"contain",position:{left:62,top,width:1156,height}});
}
function table(slide, cells) {
  const height = Math.min(56, 409/cells.length);
  for (const [i,row] of cells.entries()) for (const [j,content] of row.entries()) {
    box(slide,content,j===0?66:469,218+i*height,j===0?402:735,height, i===0?18:17,
        i===0?"#FFFFFF":navy,i===0,i===0?teal:i%2?"#eaf3f4":"#f5f9fb");
  }
}
function architecture(slide) {
  box(slide,"streaming/generators.py · flux synthétique",65,220,1135,57,22,navy,true,"#eaf3f4");
  box(slide,"↓",620,274,44,45,24,teal);
  box(slide,"streaming/engine.py · Monitor.add · alerte",65,315,1135,57,22,navy,true,"#eaf3f4");
  box(slide,"↓",620,370,44,44,24,teal);
  box(slide,"R · A-Res · DGIM · GK · blocs récents",65,405,700,62,20,navy,true,"#eaf3f4");
  box(slide,"Oracle FIFO exact facultatif",777,405,423,62,18,teal,true,"#eaf3f4");
  box(slide,"↓",362,468,44,42,24,teal);
  box(slide,"demo.py · dashboard/app.py",65,512,620,62,20,navy,true,"#eaf3f4");
  box(slide,"evaluation/ · tests et mesures",696,512,504,62,19,navy,true,"#eaf3f4");
}
for (const [i,row] of rows.entries()) {
  const slide=deck.slides.add();
  slide.background.fill="#FAFCFD";
  row.number=i+1;
  row.duration=row.owner===names[1] ? (row.anim ? (row.section===2?18:23) : 12) : row.anim?28:24;
  row.cue=row.anim?`Observer le média « ${manifest[row.anim].title} » et commenter les états indiqués.`:
    row.img?"Montrer la figure, puis lire les axes et la référence.":"Pointer les termes clés avant l’explication.";
  const next=rows[i+1];
  row.transition=next?next.owner===row.owner?`Passer à « ${next.title} ».`:
    `Je passe la parole à ${next.owner.split(" ")[0]}, qui présente « ${next.title} ».`:"Ouvrir les questions.";
  box(slide,`${sections[row.section]} · ${i===0?"Master D3S · ISTIC":row.owner}`,64,27,1150,39,15,teal,true);
  box(slide,row.title,63,i===0?155:76,1158,i===0?120:91,i===0?50:34,navy,true);
  box(slide,row.focus,65,i===0?304:157,1150,60,i===0?27:20,teal,true);
  if(i===0) {
    box(slide,names.join(" · "),66,445,1120,80,24,gray);
  } else if(row.anim) {
    await image(slide,`presentation/animations/${row.anim}.png`,`animation:${row.anim}`,221,400);
  } else if(row.img) {
    await image(slide,row.img,row.title,214,425);
  } else if(row.table) {
    table(slide,row.table);
  } else if(row.arch) {
    architecture(slide);
  } else if(row.items) {
    for(const [index,item] of row.items.entries())
      box(slide,item,82,235+index*58,1100,54,row.items.length===1?23:21,navy,index===0);
  } else {
    box(slide,row.oral,66,233,1040,188,23,gray);
  }
  if(row.source) box(slide,row.source,66,628,1130,31,13,teal);
  box(slide,`${String(i+1).padStart(2,"0")} / ${rows.length}`,65,665,1150,31,13,gray);
  const frameNotes=row.anim?manifest[row.anim].states.map(([h,e])=>`${h}. ${e}`).join("\n"):"";
  row.frameNotes=frameNotes;
  slide.speakerNotes.text=[row.oral,row.cue,frameNotes,row.transition,row.source].filter(Boolean).join("\n\n");
}
await fs.writeFile("presentation/slides.json",JSON.stringify(rows,null,2)+"\n");
await (await PresentationFile.exportPptx(deck)).save(process.argv[2]);
console.log(`${rows.length} slides, ${rows.filter(row=>row.anim).length} affiches associées à des GIF`);
