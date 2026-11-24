"""Expériences reproductibles et export de figures, sans interface web."""
import argparse
from collections import deque
import csv
import importlib.metadata
import json
import math
from pathlib import Path
import platform
from statistics import median
from time import perf_counter_ns
import tracemalloc

from algorithms import DGIM, GKQuantile, Reservoir, WeightedReservoir, WindowQuantiles
from evaluation.statistics import rank_error, target_rank, uniform_trial, weighted_trial
from streaming.engine import Monitor
from streaming.generators import bernoulli, values


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(profile, output):
    full = profile == "full"
    lengths = (1000, 10_000, 100_000, 1_000_000) if full else (1000, 10_000)
    seeds = (42, 204, 313) if full else (42, 204)
    windows = (100, 500, 1000, 5000, 10_000) if full else (100, 500, 1000)
    statistical = dict(uniform=uniform_trial(), weighted=[weighted_trial(k) for k in (1, 2)])
    rows = []
    for seed in seeds:
        for n in windows:
            sketch, oracle = DGIM(n), deque(maxlen=n)
            runtime = 0
            maximum = 0
            for t, bit in enumerate(bernoulli(4*n, .7, seed), 1):
                start = perf_counter_ns()
                sketch.add(bit)
                runtime += perf_counter_ns() - start
                oracle.append(bit)
                maximum = max(maximum, sketch.num_buckets())
                if t % max(1, n // 100) == 0 or t == 1:
                    start = perf_counter_ns()
                    estimate = sketch.count()
                    query = perf_counter_ns() - start
                    exact = sum(oracle)
                    error = abs(estimate - exact) / max(1, exact)
                    rows.append(dict(algorithm="DGIM", seed=seed, window=n, n=t, estimate=estimate,
                                     exact=exact, error=error, bound=.5, violation=error>.5,
                                     state=maximum, structural_bound=2*n.bit_length(),
                                     update_ns=runtime/t, query_ns=query))
        for length in lengths:
            data = list(values("uniforme", length, seed))
            for k in ((10, 50, 100, 500) if full else (10, 50)):
                for cls in (Reservoir, WeightedReservoir):
                    sketch = cls(k, seed)
                    start = perf_counter_ns()
                    if cls is Reservoir:
                        for x in data:
                            sketch.add(x)
                    else:
                        for x in data:
                            sketch.add(x, x)
                    rows.append(dict(algorithm=cls.__name__, seed=seed, n=length, k=k,
                                     update_ns=(perf_counter_ns()-start)/length, state=len(sketch.sample())))
            if length == 1_000_000:
                continue
            for kind in ("uniforme", "gaussienne", "dérive"):
                data = list(values(kind, length, seed))
                ordered = sorted(data)
                for eps in (.001, .01, .05):
                    sketch = GKQuantile(eps)
                    start = perf_counter_ns()
                    for x in data:
                        sketch.add(x)
                    update = (perf_counter_ns()-start)/length
                    for q in (.01,.10,.25,.5,.75,.9,.95,.99):
                        start = perf_counter_ns()
                        estimate = sketch.quantile(q)
                        query = perf_counter_ns()-start
                        exact = ordered[math.ceil(q*length)-1]
                        error = rank_error(ordered, estimate, target_rank(q, length, eps))
                        bound = eps*length
                        rows.append(dict(algorithm="GK", seed=seed, n=length, eps=eps, q=q,
                                         distribution=kind, estimate=estimate, exact=exact, error=error,
                                         value_error=abs(estimate-exact), bound=bound, violation=error>bound,
                                         state=len(sketch.sample), update_ns=update, query_ns=query))
    memory_n = 10_000
    factories = {"FIFO exact": lambda: deque(maxlen=memory_n),
                 "Fenêtre approchée": lambda: WindowQuantiles(memory_n, .05)}
    for name, factory in factories.items():
        tracemalloc.start()
        instance = factory()
        add = instance.append if isinstance(instance, deque) else instance.add
        for x in values("gaussienne", 2*memory_n, 42):
            add(x)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        rows.append(dict(algorithm=name, seed=42, window=memory_n, n=2*memory_n,
                         state=len(instance) if isinstance(instance, deque) else instance.state_size,
                         memory_bytes=current, peak_bytes=peak))
    monitor = Monitor(evaluate=True)
    timeline = [monitor.add(x) for x in values("dérive", 1200, 42)]
    transitions = [row for i, row in enumerate(timeline) if i == 0 or row["state"] != timeline[i-1]["state"]]
    output.mkdir(parents=True, exist_ok=True)
    for path, data in ((output/"metrics.csv", rows), (output/"monitoring.csv", timeline)):
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=sorted(set().union(*(row.keys() for row in data))))
            writer.writeheader()
            writer.writerows(data)
    save_json(output/"statistical_results.json", statistical)
    save_json(output/"environment.json", dict(python=platform.python_version(), os=platform.platform(),
              architecture=platform.machine(), dependencies={d: importlib.metadata.version(d)
              for d in ("pytest","scipy","matplotlib","streamlit")}, seeds=seeds, profile=profile))
    summary = dict(profile=profile, rows=len(rows), seeds=seeds, lengths=lengths, windows=windows,
                   dgim_max_error=max(row["error"] for row in rows if row["algorithm"]=="DGIM"),
                   gk_max_error_fraction=max(row["error"]/row["n"] for row in rows if row["algorithm"]=="GK"),
                   violations=sum(bool(row.get("violation")) for row in rows),
                   timing_ns={a: {"median": median(times), "min": min(times), "max": max(times)}
                              for a in ("Reservoir","WeightedReservoir")
                              if (times := [row["update_ns"] for row in rows if row["algorithm"] == a
                                           and row["n"]==10_000 and row["k"]==10])},
                   memory=[row for row in rows if "peak_bytes" in row], transitions=transitions)
    save_json(output/"benchmark_summary.json", summary)
    from evaluation.plotting import figures
    figures(output/"figures", rows, statistical, timeline, monitor)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("quick", "full"), default="quick")
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    run(args.profile, args.output)
