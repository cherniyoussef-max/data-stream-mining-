"""Additional memory, adversarial-rank and alert experiments."""
from bisect import bisect_left, bisect_right
from collections import deque
import csv
import json
import math
from pathlib import Path
import platform
import random
from statistics import median, stdev
import subprocess
from time import perf_counter_ns
import tracemalloc

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from algorithms import GKQuantile, WindowQuantiles, exact_quantile
from streaming.engine import Monitor
from streaming.generators import values


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def memory_study():
    rows = []
    for n in (100, 500, 1000, 5000, 10_000, 50_000):
        data = list(values("gaussienne", 2*n, 42))
        for kind, eps in [("FIFO", None), ("GK historique", .01)] + [("Blocs récents", e) for e in (.001,.01,.05,.1)]:
            def factory():
                if kind == "FIFO":
                    state = deque(maxlen=n)
                    return state, state.append, lambda: exact_quantile(state, .99)
                state = GKQuantile(eps) if kind == "GK historique" else WindowQuantiles(n, eps)
                return state, state.add, lambda: state.quantile(.99)
            state, add, query = factory()
            for x in data[:min(100, n)]:
                add(x)
            query()
            del state, add, query
            runtime, querytime = [], []
            for _ in range(3):
                state, add, query = factory()
                start = perf_counter_ns()
                for x in data:
                    add(x)
                runtime.append((perf_counter_ns()-start)/len(data))
                start = perf_counter_ns()
                for _ in range(9):
                    query()
                querytime.append((perf_counter_ns()-start)/9)
                del state, add, query
            tracemalloc.start()
            state, add, query = factory()
            for i, x in enumerate(data):
                # Model streaming allocation without retaining new input outside the sketch.
                add(x + 0.0)
            retained, peak = tracemalloc.get_traced_memory()
            tracemalloc.reset_peak()
            query()
            _, query_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            count = len(state) if kind=="FIFO" else len(state.sample) if kind=="GK historique" else state.state_size
            rows.append(dict(method=kind, N=n, eps=eps, events=len(data), entries=count,
                             retained_bytes=retained, ingest_peak_bytes=peak, query_extra_peak_bytes=query_peak-retained,
                             update_ns=median(runtime), update_sd_ns=stdev(runtime),
                             throughput_per_second=1e9/median(runtime), query_ns=median(querytime),
                             query_sd_ns=stdev(querytime), oracle_entries=n if kind=="Blocs récents" else 0))
    return rows


def growth_study():
    results = []
    for kind in ("croissante", "décroissante", "extrêmes alternés", "répétitions",
                 "uniforme", "gaussienne", "queue lourde", "dérive", "rafales", "permutation modulaire"):
        for eps in (.001,.005,.01,.05,.1):
            gk = GKQuantile(eps)
            if kind == "extrêmes alternés":
                stream = ((-1)**i*i for i in range(100_000))
            elif kind == "permutation modulaire":
                stream = (((i*7919)%100_003) for i in range(100_000))
            else:
                stream = values(kind, 100_000, 42)
            for i,x in enumerate(stream, 1):
                gk.add(x)
                if i in (100, 1000, 10_000, 50_000, 100_000):
                    results.append(dict(distribution=kind, eps=eps, n=i, entries=len(gk.sample)))
    return results


def confusion(predictions, reference):
    tp = sum(a and b for a,b in zip(predictions, reference))
    fp = sum(a and not b for a,b in zip(predictions, reference))
    fn = sum(not a and b for a,b in zip(predictions, reference))
    tn = len(reference)-tp-fp-fn
    return dict(tp=tp, tn=tn, fp=fp, fn=fn, precision=tp/max(1,tp+fp), recall=tp/max(1,tp+fn),
                specificity=tn/max(1,tn+fp), accuracy=(tp+tn)/len(reference),
                f1=2*tp/max(1,2*tp+fp+fn), agreement=(tp+tn)/len(reference))


def alert_study(seed=42):
    configurations = (
        ("référence", 200, .01, 80, 110, 160, [(401,800)]),
        ("graduel", 100, .05, 70, 100, 145, [(301,580)]),
        ("répété", 500, .1, 90, 120, 200, [(101,180),(701,850)]),
        ("isolé", 50, .1, 80, 110, 250, [(311,311)]),
        ("sous seuil", 100, .005, 90, 150, 70, [(401,480)]),
    )
    all_rows, scores = [], []
    for name,n,eps,median_limit,p99_limit,severity,intervals in configurations:
        rng = random.Random(seed)
        monitor = Monitor(size=n, eps=eps, seed=seed, median=median_limit, p99=p99_limit, evaluate=True)
        rows = []
        for i in range(1, 1201):
            incident = next(((a,b) for a,b in intervals if a <= i <= b), None)
            center = severity if incident else 30
            if incident and name=="graduel":
                center = 30 + (severity-30)*min(1,(i-incident[0]+1)/60)
            row = monitor.add(max(1,rng.gauss(center,6)))
            ordered = sorted(monitor.exact)
            estimate = row["p99"]
            target = math.ceil(.99*len(ordered))
            lower, upper = bisect_left(ordered,estimate), bisect_right(ordered,estimate)
            error = max(0,lower+1-target,target-upper)
            bound = monitor.recent.rank_bound
            assert error <= bound
            rows.append(dict(scenario=name, N=n, B=monitor.recent.block_size, eps=eps,
                             active_count=len(ordered), normalized_error=error/len(ordered),
                             normalized_bound=bound/len(ordered),
                             group_budget=bound-monitor.recent.stale_count,
                             median_limit=median_limit, p99_limit=p99_limit,
                             severity=severity, incident=bool(incident), rank_error=error, rank_bound=bound,
                             boundary=monitor.recent.stale_count, exceeds_bound=error>bound,
                             value_error_ms=abs(estimate-row["exact_p99"]), **row))
        active = [r["state"]=="Alerte" for r in rows]
        exact = [r["exact_state"]=="Alerte" for r in rows]
        labels = [r["incident"] for r in rows]
        for label, reference in (("seuil exact",exact),("incident simulé",labels)):
            scores.append(dict(scenario=name, reference=label, **confusion(active,reference)))
        for index,(start,end) in enumerate(intervals):
            stop = intervals[index+1][0] if index+1<len(intervals) else len(rows)+1
            detected = next((r["t"] for r in rows[start-1:end] if r["state"]=="Alerte"),None)
            recovered = next((r["t"] for r in rows[end:stop-1] if r["state"]=="Rétablissement"),None)
            scores[-1].setdefault("intervals",[]).append(dict(start=start,end=end,
                detection_delay=detected-start if detected else None,
                recovery_delay=recovered-(end+1) if recovered else None))
        all_rows.extend(rows)
    return all_rows, scores


def figures(output, memory, growth, timeline):
    def draw(name,title,x,y,content):
        fig,ax = plt.subplots(figsize=(8,4),layout="constrained")
        content(ax)
        ax.set(title=title,xlabel=x,ylabel=y)
        ax.grid(alpha=.2)
        if ax.get_legend_handles_labels()[0]:
            ax.legend()
        for extension in ("png","svg"):
            fig.savefig(output/f"{name}.{extension}",dpi=220)
        plt.close(fig)

    shift = [r for r in timeline if r["scenario"]=="répété"]
    draw("15_rang_recent","Erreur du P99 récent et borne","Événement","Rangs",
         lambda ax: [ax.plot([r["t"] for r in shift],[r[k] for r in shift],label=k)
                     for k in ("rank_error","rank_bound")])
    draw("16_frontiere","Données périmées dans le bloc frontière","Événement","Observations périmées",
         lambda ax: ax.plot([r["t"] for r in shift[:550]],[r["boundary"] for r in shift[:550]]))
    base = [r for r in timeline if r["scenario"]=="référence"]
    draw("17_decisions","Décisions de surveillance et incident simulé","Événement","Indicateur actif",
         lambda ax: [ax.step([r["t"] for r in base],
                             [int(r[k]=="Alerte" if k!="incident" else r[k])+.04*i for r in base],
                             label=label,where="post") for i,(k,label) in enumerate(
                        (("state","Approché"),("exact_state","Seuil exact"),("incident","Incident")))])
    def memory_chart(ax):
        for eps in (None,.01,.05,.1):
            chosen = [r for r in memory if r["eps"]==eps and r["method"]!="GK historique"]
            ax.loglog([r["N"] for r in chosen],[r["ingest_peak_bytes"]/1024 for r in chosen],
                      "o-",label=f"Blocs, ε={eps}" if eps else "FIFO")
    draw("18_memoire_echelle","Mémoire des méthodes sur la fenêtre récente","N","Pic ingestion (Kio)",memory_chart)
    def growth_chart(ax):
        for kind in ("croissante","décroissante","extrêmes alternés","rafales","permutation modulaire"):
            selected = [r for r in growth if r["distribution"]==kind and r["eps"]==.01]
            ax.loglog([r["n"] for r in selected],[r["entries"] for r in selected],"o-",label=kind)
    draw("19_gk_adversarial","Taille GK sous plusieurs ordres, ε=0,01","n","Tuples",growth_chart)


def main():
    output = Path("results")
    memory = memory_study()
    growth = growth_study()
    timeline,scores = alert_study()
    for name,rows in (("memory_scaling",memory),("gk_growth",growth),("alert_timeline",timeline)):
        write_csv(output/f"{name}.csv",rows)
    figures(output/"figures",memory,growth,timeline)
    cpu = next((x.split(":",1)[1].strip() for x in Path("/proc/cpuinfo").read_text().splitlines()
                if x.startswith("model name")),platform.machine())
    ram = Path("/proc/meminfo").read_text().splitlines()[0].split(":",1)[1].strip()
    source = subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip() if Path(".git").exists() else None
    baseline = [r for r in memory if r["N"]==10_000 and (r["method"]=="FIFO" or r["eps"]==.05)]
    summary = dict(seed=42,cpu=cpu,ram=ram,python=platform.python_version(),os=platform.platform(),
                   base_commit=source, timing_repetitions=3, measurements=dict(memory=len(memory),
                   growth=len(growth),alerts=len(timeline)), alerts=scores,
                   recent_rank_max=max(r["rank_error"] for r in timeline),
                   recent_violations=sum(r["exceeds_bound"] for r in timeline),
                   recent_max_normalized_error=max(r["normalized_error"] for r in timeline),
                   recent_max_normalized_bound=max(r["normalized_bound"] for r in timeline),
                   relative_memory_reduction=1-baseline[1]["ingest_peak_bytes"]/baseline[0]["ingest_peak_bytes"])
    (output/"final_study.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


if __name__ == "__main__":
    main()
