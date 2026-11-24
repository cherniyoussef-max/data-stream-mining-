"""Compare the fixed V3 threshold rule and an optional corroboration policy."""
import json
from itertools import groupby
from pathlib import Path

from evaluation.final_study import alert_study, confusion, plt, write_csv
from streaming.alert_policy import PersistentAlerts


SEEDS = (42,204,313)


def delays(events, states):
    episodes = []
    for label, items in groupby(enumerate(events),key=lambda pair:pair[1]["incident"]):
        segment = [index for index,_ in items]
        if label:
            episodes.append((segment[0],segment[-1]))
    result = []
    for i,(start,end) in enumerate(episodes):
        next_start = episodes[i+1][0] if i+1<len(episodes) else len(events)
        detected = next((j for j in range(start,end+1) if states[j]=="Alerte"),None)
        # Zero means a detected alert was already inactive at the first normal event.
        recovered = next((j for j in range(end+1,next_start) if states[j]!="Alerte"),None)
        result.append(dict(start=start+1,end=end+1,detected_at=None if detected is None else detected+1,
                           detection_delay=None if detected is None else detected-start,
                           recovery_delay=None if detected is None or recovered is None else recovered-end-1,
                           active_at_start=states[start]=="Alerte"))
    return result


def compare():
    scores, episodes = [], []
    for seed in SEEDS:
        timeline,_ = alert_study(seed)
        for name,group in groupby(timeline,key=lambda row:row["scenario"]):
            events = list(group)
            config = events[0]
            policy = PersistentAlerts(config["N"],config["median_limit"],config["p99_limit"])
            improved = [policy.add(r["latency"],r["median"],r["p99"]) for r in events]
            for strategy,states in (("seuil", [row["state"] for row in events]),("persistance",improved)):
                labels = [row["incident"] for row in events]
                oracle = [row["exact_state"]=="Alerte" for row in events]
                decisions = [state=="Alerte" for state in states]
                scores.append(dict(seed=seed,scenario=name,strategy=strategy,
                                   exact_rule_agreement=confusion(decisions,oracle)["agreement"],
                                   **confusion(decisions,labels)))
                episodes.extend(dict(seed=seed,scenario=name,strategy=strategy,**episode)
                                for episode in delays(events,states))
    return scores,episodes


def main():
    root = Path("results")
    scores,episodes = compare()
    write_csv(root/"alert_comparison.csv",scores)
    write_csv(root/"alert_episode_delays.csv",episodes)
    names = list(dict.fromkeys(row["scenario"] for row in scores))
    means = {strategy: {name: sum(row["f1"] for row in scores
                                  if row["strategy"]==strategy and row["scenario"]==name)/len(SEEDS)
                        for name in names} for strategy in ("seuil","persistance")}
    (root/"alert_comparison.json").write_text(
        json.dumps(dict(seeds=SEEDS,means=means,parameters=dict(evidence_max_window=50,
                   slow=90.,fraction=.15,persistence=3)),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    fig,ax = plt.subplots(figsize=(8.5,4),layout="constrained")
    for strategy,offset in (("seuil",-.18),("persistance",.18)):
        ax.bar([i+offset for i in range(len(names))],[means[strategy][name] for name in names],
               width=.36,label=strategy)
    ax.set(xticks=list(range(len(names))),xticklabels=names,ylim=(0,1.05),
           ylabel="F1 moyen (graines 42, 204, 313)",title="Détection d’incidents : règle de seuil et persistance")
    ax.legend()
    ax.grid(axis="y",alpha=.2)
    fig.savefig(root/"figures/22_alertes_strategies.png",dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    main()
