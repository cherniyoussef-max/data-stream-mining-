"""Interface locale de surveillance de latences synthétiques."""
from collections import deque
import csv
import io
import json
from pathlib import Path
import random
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from streaming.engine import Monitor
from streaming.generators import DISTRIBUTIONS, values

st.set_page_config(page_title="Stream Analytics Lab", layout="wide")
st.title("Stream Analytics Lab")
st.caption("Projet 4 · Master D3S · Latences réseau synthétiques")
with st.expander("Parcours de démonstration"):
    st.markdown(
        "1. Avancer d’un événement et comparer les deux réservoirs.\n"
        "2. Forcer un incident et avancer par lots. Comparer le P99 récent et le P99 historique.\n"
        "3. Examiner les groupes DGIM et les rangs GK. Revenir à la normale et observer la sortie progressive.\n"
        "4. Exporter les mesures et comparer les décisions exacte et approchée."
    )

with st.sidebar.form("parameters"):
    st.subheader("Configuration du flux")
    distribution = st.selectbox("Distribution", DISTRIBUTIONS, index=2)
    length = st.number_input("Longueur du flux", 1, 100_000, 1200)
    k = st.number_input("Capacité des réservoirs", 1, 500, 20)
    size = st.number_input("Taille de fenêtre N", 1, 10_000, 200)
    eps = st.number_input("Précision ε", .001, .25, .01, .001, format="%.3f")
    policy = st.selectbox("Pondération A-Res", ("Latence", "Uniforme"))
    slow = st.number_input("Événement lent (ms)", 1., 10000., 90.)
    median = st.number_input("Seuil médiane (ms)", 1., 10000., 80.)
    p99 = st.number_input("Seuil P99 (ms)", 1., 10000., 110.)
    seed = st.number_input("Graine", 0, 2**31-1, 42)
    evaluate = st.checkbox("Activer les oracles exacts (mémoire supplémentaire)", True)
    submitted = st.form_submit_button("Appliquer et réinitialiser")

state = st.session_state
if submitted or "config" not in state:
    state.config = (distribution, length, k, size, eps, policy, slow, median, p99, seed, evaluate)


def reset():
    kind, limit, k, size, eps, policy, slow, median, p99, seed, evaluate = state.config
    state.monitor = Monitor(k, size, eps, seed, slow, median, p99, policy=="Latence", evaluate)
    state.stream = values(kind, limit, seed)
    state.intervention_rng = random.Random(seed + 2)
    state.history = deque(maxlen=500)
    state.mode = "Scénario"
    state.play = False


if submitted or "monitor" not in state:
    reset()

batch = st.sidebar.slider("Événements par lot", 1, 500, 50)
if st.sidebar.button("Réinitialiser"):
    reset()
if st.sidebar.button("Simuler un incident"):
    state.mode = "Incident"
if st.sidebar.button("Revenir à la normale"):
    state.mode = "Normal forcé"
st.sidebar.caption(f"Mode actif · {state.mode}")


def advance(count):
    for _ in range(count):
        x = next(state.stream, None)
        if x is None:
            return
        if state.mode != "Scénario":
            center = 160 if state.mode == "Incident" else 30
            x = max(1, state.intervention_rng.gauss(center, 6))
        state.history.append(state.monitor.add(x))


@st.fragment(run_every="0.6s" if state.play else None)
def live():
    monitor = state.monitor
    finished = monitor.gk.n >= state.config[1]
    controls = st.columns(4)
    if controls[0].button("Démarrer", disabled=finished or state.play):
        state.play = True
        st.rerun()
    if controls[1].button("Pause", disabled=not state.play):
        state.play = False
        st.rerun()
    if controls[2].button("Avancer d’un événement", disabled=finished):
        advance(1)
    if controls[3].button("Avancer d’un lot", disabled=finished):
        advance(batch)
    if state.play:
        advance(batch)
        if monitor.gk.n >= state.config[1]:
            state.play = False
            st.rerun()
    if not state.history:
        st.info("Démarrez le flux ou avancez d’un événement pour afficher les mesures.")
        return
    row = state.history[-1]
    history = list(state.history)
    st.progress(monitor.gk.n / state.config[1], text=f"{monitor.gk.n} / {state.config[1]} événements")
    cols = st.columns(6)
    for col, label, value in zip(cols, ("Fenêtre N", "Médiane récente", "P95 récent", "P99 récent",
                                       "Événements lents (estimés)", "État"),
                                  (monitor.dgim.N, f"{row['median']:.1f} ms", f"{row['p95']:.1f} ms",
                                   f"{row['p99']:.1f} ms", row["estimated"], row["state"])):
        col.metric(label, value)
    stream, reservoir, weighted, dgim, quantiles = st.tabs(
        ["Surveillance", "Réservoir uniforme", "A-Res", "DGIM", "Quantiles"])
    with stream:
        import pandas as pd

        frame = pd.DataFrame(history).set_index("t")
        st.line_chart(frame[["latency","p99","historical"]].rename(columns={
            "latency":"Latence", "p99":"P99 récent", "historical":"P99 historique"}))
        st.caption("Latences en millisecondes. Derniers 500 événements affichés.")
        with io.StringIO() as handle:
            writer = csv.DictWriter(handle, fieldnames=list(row))
            writer.writeheader()
            writer.writerows(history)
            csv_data = handle.getvalue()
        st.download_button("Exporter les dernières mesures", csv_data, "latences.csv", "text/csv")
    with reservoir:
        st.write(f"Capacité {monitor.uniform.k} · {monitor.uniform.n} observations · probabilité "
                 f"{min(1, monitor.uniform.k / monitor.uniform.n):.3f} par position.")
        st.dataframe([{"Latence (ms)": x} for x in monitor.uniform.sample()], hide_index=True)
        st.caption("Chaque nouvel événement peut remplacer une position du réservoir.")
    with weighted:
        st.dataframe([{"Latence (ms)": x, "Poids": w, "Priorité": key}
                      for x, w, key in monitor.weighted.entries()], hide_index=True)
        st.caption("A-Res garde les plus grandes priorités. Un poids élevé favorise l’inclusion.")
    with dgim:
        st.write(f"Fenêtre : {monitor.dgim.N} positions. Borne d’erreur relative : 50 %.")
        st.dataframe([{"Âge": monitor.dgim.age(t), "Taille": n} for t, n in monitor.dgim.buckets],
                     hide_index=True)
        st.write("Fusions du dernier événement", [f"{a}+{a} → {b}" for a,b in monitor.dgim.merges])
        binary = "".join(str(int(r["latency"] > monitor.slow)) for r in history[-min(100,monitor.dgim.N):])
        st.code(binary, language=None)
        if "exact_count" in row:
            error = abs(row["estimated"]-row["exact_count"])/max(1,row["exact_count"])
            st.write(f"Exact : {row['exact_count']} · Erreur relative : {error:.1%}")
    with quantiles:
        st.write(f"GK historique : {monitor.gk.n} événements, {len(monitor.gk.sample)} tuples, ε={monitor.gk.eps}.")
        st.write(f"Médiane historique : {monitor.gk.quantile(.5):.2f} ms · P99 historique : {row['historical']:.2f} ms.")
        st.caption("Chaque tuple (valeur, g, Δ) borne le rang de sa valeur. La compression fusionne des voisins compatibles.")
        lower = 0
        tuples = []
        for value, gap, delta in monitor.gk.sample[:25]:
            lower += gap
            tuples.append({"Valeur": value, "g": gap, "Δ": delta,
                           "Rang inférieur": lower, "Rang supérieur": lower + delta})
        st.dataframe(tuples, hide_index=True)
        st.write(f"Fenêtre approchée : {monitor.recent.state_size} valeurs pondérées, borne de rang {monitor.recent.rank_bound}.")
        st.write(f"Bloc frontière : {monitor.recent.stale_count} positions périmées encore représentées.")
        with st.expander("Voir les blocs récents"):
            st.write("Bloc ouvert", monitor.recent.open_block())
            st.dataframe([
                {"Fin du bloc": end, "Bloc frontière": boundary, "Valeur (ms)": value, "Poids": weight}
                for end, boundary, entries in monitor.recent.block_snapshot() for value, weight in entries
            ], hide_index=True)
        if "exact_p99" in row:
            st.write(f"Décision approchée : {row['state']} · Décision exacte : {row['exact_state']}")
            ordered = sorted(monitor.exact)
            from evaluation.statistics import rank_error
            import math
            for name, q in (("median", .5), ("p95", .95), ("p99", .99)):
                error = rank_error(ordered, row[name], math.ceil(q*len(ordered)))
                st.write(f"{name.upper()} exact : {row['exact_'+name]:.2f} ms · écart de rang récent : {error:g}")


live()
with st.expander("Résultats des expériences"):
    path = ROOT / "results" / "statistical_results.json"
    if path.exists():
        stats = json.loads(path.read_text())
        st.write(f"T1 · p = {stats['uniform']['p']:.4f}")
        images = sorted((path.parent/"figures").glob("*.png"))
        if images:
            selection = st.selectbox("Figure", images, format_func=lambda path: path.stem)
            st.image(str(selection))
    else:
        st.info("Produisez les résultats avec python -m evaluation.benchmark --profile quick.")
