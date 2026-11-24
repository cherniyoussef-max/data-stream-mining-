"""Controlled sweep of window size and epsilon on the reference incident."""
import json
from pathlib import Path

from evaluation.final_study import confusion, plt, write_csv
from streaming.engine import Monitor
from streaming.generators import values


def sweep():
    rows = []
    signal = list(values("dérive", 1200, 42))
    labels = [401 <= t <= 800 for t in range(1, 1201)]
    for n in (50, 100, 200, 500):
        for eps in (.005, .05, .15):
            monitor = Monitor(size=n, eps=eps, evaluate=True)
            events = [monitor.add(latency) for latency in signal]
            states = [event["state"] == "Alerte" for event in events]
            exact = [event["exact_state"] == "Alerte" for event in events]
            first = next((event["t"] for event in events[400:800] if event["state"]=="Alerte"), None)
            recovered = next((event["t"] for event in events[800:] if event["state"]=="Rétablissement"), None)
            rows.append(dict(N=n, B=monitor.recent.block_size, eps=eps, seed=42,
                            exact_agreement=confusion(states,exact)["agreement"],
                            detection_delay=None if first is None else first-401,
                            recovery_delay=None if recovered is None else recovered-801,
                            **confusion(states,labels)))
    return rows


def main():
    root = Path("results")
    rows = sweep()
    write_csv(root/"alert_sensitivity.csv", rows)
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.1), layout="constrained")
    for eps in sorted({row["eps"] for row in rows}):
        selected = [r for r in rows if r["eps"] == eps]
        axes[0].plot([r["N"] for r in selected], [r["f1"] for r in selected], "o-", label=f"ε={eps}")
        axes[1].plot([r["N"] for r in selected], [r["recovery_delay"] for r in selected], "o-")
    axes[0].set(title="Accord avec l’incident simulé", xlabel="Fenêtre N", ylabel="F1")
    axes[1].set(title="Rétablissement après fin d’incident", xlabel="Fenêtre N", ylabel="Délai (événements)")
    axes[0].legend()
    axes[1].text(.04,.90,"Points absents : délai non observé", transform=axes[1].transAxes)
    fig.savefig(root/"figures/20_sensibilite.png",dpi=220)
    plt.close(fig)
    scores = json.loads((root/"final_study.json").read_text())["alerts"][1]
    fig, ax = plt.subplots(figsize=(5.1,4.2), layout="constrained")
    grid = [[scores["tn"],scores["fp"]],[scores["fn"],scores["tp"]]]
    ax.imshow(grid,cmap="Blues")
    for y, row in enumerate(grid):
        for x, count in enumerate(row):
            ax.text(x,y,str(count),ha="center",va="center",fontsize=16,color="white" if count>400 else "#112841")
    ax.set(xticks=(0,1),yticks=(0,1),xticklabels=("Normal","Alerte"),
           yticklabels=("Hors incident","Incident"),xlabel="Décision",ylabel="Étiquette du générateur",
           title="Scénario de référence · 1 200 événements")
    fig.savefig(root/"figures/21_confusion.png",dpi=220)


if __name__ == "__main__":
    main()
