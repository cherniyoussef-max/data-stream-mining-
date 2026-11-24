"""Generate pedagogical GIFs and their static posters from documented traces."""
from collections import deque
import csv
import json
import math
from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFont

from algorithms import DGIM, GKQuantile, Reservoir, WeightedReservoir, WindowQuantiles

ROOT = Path("presentation/animations")
WIDTH, HEIGHT = 1200, 500
NAVY, TEAL, INK, PALE = "#112841", "#006D73", "#304a60", "#e7f3f2"
FONT_ROOT = Path("/usr/share/fonts/truetype/dejavu")


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_ROOT / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")), size)


def wrap(draw, message, face, width):
    lines = []
    for paragraph in message.splitlines():
        line = ""
        for word in paragraph.split():
            candidate = f"{line} {word}".strip()
            if line and draw.textlength(candidate,font=face) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return "\n".join(lines)


def cards(title, subtitle, frames, source):
    output = []
    for index, (heading, tokens, explanation) in enumerate(frames):
        image = Image.new("RGB", (WIDTH, HEIGHT), "#f5f9fb")
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 12, HEIGHT), fill=TEAL)
        draw.text((42,28), title, font=font(39,True), fill=NAVY)
        draw.text((44,84), subtitle, font=font(21), fill=INK)
        draw.text((44,146), heading, font=font(31,True), fill=TEAL)
        base_size = 23
        while sum(max(63,draw.textlength(text,font=font(base_size,bold))+28)+9
                  for text,bold in tokens) > WIDTH-90:
            base_size -= 1
        left = 43
        for token,active in tokens:
            token_font = font(base_size,active)
            width = max(63,int(draw.textlength(token,font=token_font))+28)
            draw.rounded_rectangle((left,209,left+width,274),radius=10,
                                   fill=TEAL if active else PALE)
            draw.text((left+14,226),token,font=token_font,fill="white" if active else NAVY)
            left += width+9
        draw.text((44,322),wrap(draw,explanation,font(23),WIDTH-92),font=font(23),fill=INK,spacing=9)
        draw.text((44,447),source,font=font(17),fill=TEAL)
        draw.text((1090,446),f"{index+1} / {len(frames)}",font=font(18,True),fill=NAVY)
        output.append(image)
    return output


def tokens(*items):
    return [(str(item), False) for item in items]


def interval_frames(model):
    result = []
    for i in range(3,8):
        observed = "ABCDEFGH"[:i]
        if model=="landmark":
            selected = [j>=1 for j in range(i)]
            note = "Le repère B reste fixe et les nouveaux points agrandissent la fenêtre."
        elif model=="tumbling":
            selected = [j//3==(i-1)//3 for j in range(i)]
            note = "Un nouveau bloc commence après trois positions. Les blocs sont disjoints."
        elif model=="glissante":
            selected = [j>=i-3 for j in range(i)]
            note = "La fenêtre garde trois positions. La plus ancienne sort à chaque arrivée."
        else:
            selected = [j>=i-3 for j in range(i)]
            observed = [f"{letter} : {0.5**(i-1-j):.3f}" for j,letter in enumerate(observed)]
            note = "À chaque arrivée les poids précédents sont divisés par deux."
        result.append((f"Arrivée {i}", list(zip(observed,selected)), note))
    return result


def reservoir_frames():
    sketch = Reservoir(3,42)
    oracle = random.Random(42)
    frames = []
    for i, item in enumerate("ABCDEFGH",1):
        index = oracle.randrange(i) if i>3 else None
        sketch.add(item)
        choice = "remplissage" if index is None else f"j={index} · {'remplacement' if index < 3 else 'rejet'}"
        frames.append((f"{item} arrive · {choice}", [(x,x==item) for x in sketch.sample()],
                       f"Capacité k=3 · {i} observations traitées · identifiant distinct par position."))
    return frames


class FixedRandom:
    def __init__(self):
        self.values = iter((.25,.25,.25,.16))

    def random(self):
        return next(self.values)


def weighted_frames():
    sketch = WeightedReservoir(2,42)
    sketch.rng = FixedRandom()
    frames = []
    for item,weight,u in zip("ABCD",(1,2,4,2),(.25,.25,.25,.16)):
        previous = sketch.entries()
        sketch.add(item,weight)
        key = u**(1/weight)
        status = "inséré" if len(previous)<2 else "remplace le minimum" if item in sketch.sample() else "rejeté"
        minimum = f"{min(float(k) for _,_,k in previous):.3f}" if previous else "vide"
        frames.append((f"{item} · poids {weight} · U={u:.2f} · {status}",
                       [(f"{x}  ρ={k:.3f}",x==item) for x,_,k in sketch.entries()],
                       f"Clé équivalente U^(1/w) = {key:.4f}. Minimum ρ avant l’arrivée : {minimum}."))
    return frames


def dgim_frames():
    sketch, window = DGIM(8), deque(maxlen=8)
    trace = []
    for t,bit in enumerate([1]*8+[0]*8,1):
        old = sketch.buckets[-1] if sketch.buckets else None
        expires = old and sketch.age(old[0])+1==8
        sketch.add(bit)
        window.append(bit)
        action = " ; ".join(f"{a}+{a}→{b}" for a,b in sketch.merges)
        exact = sum(window)
        error = abs(sketch.count()-exact)/max(1,exact)
        trace.append((f"t={t} · bit {bit} · fenêtre {''.join(map(str,window))}",
                      [(f"{size}@{stamp}",sketch.age(stamp)==0) for stamp,size in sketch.buckets],
                      f"Exact {exact} · estimé {sketch.count()} · erreur {error:.1%}.\n"
                      f"{'Expiration du plus ancien. ' if expires else ''}{'Fusions : '+ action if action else 'Aucune fusion.'}"))
    return trace


def gk_frames():
    sketch = GKQuantile(.25)
    frames = []
    for x in (5,1,3,2,4,6):
        sketch.add(x)
        frames.append((f"Insérer {x} · n={sketch.n}", [(str(row),row[0]==x) for row in sketch.sample],
                       "g : incrément du rang inférieur. Δ : marge jusqu’au rang supérieur.\n"
                       f"Budget de compression : ⌊2εn⌋ = {math.floor(2*.25*sketch.n)}."))
    frames.append(("Sélection du quantile q=0,5",tokens("cible 3","valeur 4","rang 4"),
                   "Le tuple de 4 a pour bornes [3,4]. Erreur de rang 1, dans la marge 1,5."))
    return frames


def block_frames():
    sketch = WindowQuantiles(16,.3)
    active = deque(maxlen=16)
    stream = [99,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    frames = []
    for t,x in enumerate(stream,1):
        active.append(x)
        sketch.add(x)
        if t not in (1,3,4,8,16,17,19,20):
            continue
        groups = [("F"+str(end)+": "+"/".join(f"{v}×{weight}" for v,weight in rows),boundary)
                  for end,boundary,rows in sketch.block_snapshot()]
        if sketch.open_block():
            groups += [("O : "+",".join(map(str,sketch.open_block())),True)]
        frames.append((f"t={t} · B=4 · S=2 · fenêtre [{active[0]}…{active[-1]}]",
                       groups, f"F : bloc fermé, O : bloc ouvert. Périmés : {sketch.stale_count}. "
                       f"Budget : {sketch.rank_bound}.\nP99 récent {sketch.quantile(.99)}. "
                       f"Maximum actif {max(active)}."))
    return frames


ARTICLES = {
    "a1": ("Lots pondérés distribués","Hübschle-Schneider et Sanders · ACM TOMS 2022", [
        ("Événements pondérés", tokens("A : 1","B : 2","C : 6","D : 3"), "Le poids traduit une préférence de sélection."),
        ("Deux unités de calcul", tokens("PU 1 : A, B","PU 2 : C, D"), "Les structures de tirage se construisent par partition."),
        ("Requête pondérée", tokens("Masse 3","Masse 9","Tirage"), "Le modèle parallèle dépend de la loi de tirage demandée.")]),
    "a2": ("Un sketch qui expire","Gou et al. · IEEE TKDE 2023", [
        ("Zones temporelles",tokens("Zone 1","Zone 2","Nouveau paquet"),"Chaque zone couvre un intervalle."),
        ("Mise à jour",tokens("Zone 1","Zone 2 + paquet"),"Le sketch compte par zone et interroge l’intervalle actif."),
        ("Frontière déplacée",tokens("Zone 1 expire","Zone 2","Zone 3"),"La sortie de la première zone évite de compter des fréquences anciennes.")]),
    "a3": ("Un même flux, plusieurs esquisses","Fernando et al. · EDBT 2023", [
        ("Entrée commune",tokens("Pareto","Uniforme","NYT","Power"),"Même entrée pour chaque méthode dans une expérience."),
        ("Cinq résumés",tokens("KLL","Moments","DDS","UDDS","REQ"),"Les représentations et notions d’erreur diffèrent."),
        ("Lecture de la figure 6b",tokens("Uniforme","Erreur relative moyenne <1 %"),"Le résultat publié est propre à ce jeu et à ce protocole.")]),
    "a4": ("Réservoir de jointure","Dai, Hu et Yi · SIGMOD 2024", [
        ("Deux flux",tokens("Client A","Client B","Commande d’A"),"Le réservoir cible les tuples joints."),
        ("Index de correspondance",tokens("A ↔ commande","B sans commande"),"L’index aide à trouver les candidats."),
        ("Sélection sous prédicat",tokens("Candidat compatible","Réservoir"),"Le réservoir est construit sans matérialiser toute la jointure.")]),
    "a5": ("Compression déterministe","Gribelyuk et al. · PODS 2024", [
        ("Univers totalement ordonné",tokens("Rang 20","Rang 28","Rang 36"),"Les comparaisons ordonnent les éléments."),
        ("Grouper dans une marge",tokens("Borne basse","Représentant","Borne haute"),"Illustration de la marge additive, sans exécuter l’algorithme publié."),
        ("Énoncé asymptotique",tokens("(2+o(1))","ε⁻¹","log(εn)"),"La borne de l’article se compte en éléments stockés.")]),
    "a6": ("Exploiter un univers d’entiers","Gupta, Singhal et Wu · FOCS 2024", [
        ("Latences entières",tokens("0","1","2","3","4","5","6","7"),"On connaît l’univers de valeurs de l’exemple."),
        ("Découpage numérique",tokens("[0,3]","[4,7]"),"Les opérations sur les entiers fournissent une information supplémentaire."),
        ("Garantie propre au modèle",tokens("Univers borné","O(1/ε) mots"),"La borne ne se transpose pas au GK par comparaison.")]),
    "a7": ("Quantile conditionnel en ligne","Xie et al. · Journal of Econometrics 2025", [
        ("Mesures et covariable",tokens("Latence","Charge faible","Charge forte"),"Le modèle utilise une variable explicative."),
        ("Ajustement par lot",tokens("Résumé historique","Nouveau lot"),"La régression quantile est mise à jour après l’arrivée."),
        ("Deux charges, deux cibles",tokens("P99 | faible","P99 | forte"),"Les quantiles dépendent de la charge. Notre P99 est marginal.")]),
}


def incident_frames():
    with Path("results/monitoring.csv").open(encoding="utf-8",newline="") as handle:
        rows = list(csv.DictReader(handle))
    frames = []
    for t in (200,400,401,403,600,800,801,925,998,1200):
        row = rows[t-1]
        frames.append((f"Événement {t} · {row['state']}",
                       tokens(f"latence {float(row['latency']):.1f} ms",
                              f"P99 récent {float(row['p99']):.1f}",
                              f"historique {float(row['historical']):.1f}"),
                       f"État exact : {row['exact_state']}. Fenêtre 200, seuil P99 110 ms.\n"
                       "L’incident est injecté aux événements 401 à 800."))
    return frames


def main():
    trace = {
        "flux": ("Arrivées sur le réseau","Trace mesurée dans le simulateur",incident_frames()[:5],"résultats · monitoring.csv"),
        "reservoir": ("Algorithm R","Trace canonique · k=3, graine 42",reservoir_frames(),"algorithms/sampling.py"),
        "ares": ("A-Res","Trace canonique · k=2, U imposés",weighted_frames(),"algorithms/sampling.py"),
        "dgim": ("DGIM · groupes du plus récent au plus ancien","Trace canonique · N=8, taille@timestamp modulo 9",dgim_frames(),"algorithms/dgim.py"),
        "gk": ("GK · résumé historique","Trace canonique · ε=0,25, flux 5, 1, 3, 2, 4, 6",gk_frames(),"algorithms/quantiles.py"),
        "blocs": ("Quantiles récents","Trace canonique · N=16, ε=0,30, groupe de taille 2",block_frames(),"algorithms/quantiles.py"),
        "incident": ("Détection et rétablissement","Trace mesurée dans le simulateur · graine 42",incident_frames(),"résultats · monitoring.csv"),
    }
    for model in ("landmark","tumbling","glissante","decroissance"):
        trace[model]=(model.capitalize(),"Schéma pédagogique · arrivées A à H",interval_frames(model),"Exemple pédagogique")
    for key,(title,subtitle,frames) in ARTICLES.items():
        trace[key]=(title,subtitle,frames,"Schéma pédagogique · mécanisme illustré, article non exécuté")
    manifest = {}
    for key,(title,subtitle,frames,source) in trace.items():
        images = cards(title,subtitle,frames,source)
        durations = [2000]*len(images)
        durations[-1] = 3800
        images[0].save(ROOT/f"{key}.gif",save_all=True,append_images=images[1:],
                       duration=durations,loop=0,disposal=2,optimize=True)
        images[-1].save(ROOT/f"{key}.png")
        manifest[key] = {"title": title, "frames": len(images), "durations_ms": durations,
                         "states": [[heading,explanation] for heading,_,explanation in frames]}
    (ROOT/"trace.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


if __name__ == "__main__":
    main()
