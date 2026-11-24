"""Paired comparison with the V3 single-quantile algorithm."""
import json
import math
from pathlib import Path
from statistics import median
from time import perf_counter_ns
import tracemalloc

from algorithms import WindowQuantiles
from streaming.engine import Monitor
from streaming.generators import values


PROBABILITIES = (.5,.95,.99)


def legacy_quantile(window, q):
    rows = [(x,1) for x in window._pending]
    for _, block in window._completed:
        rows.extend(block)
    target = max(1,math.ceil(q*sum(weight for _,weight in rows)))
    for x,weight in sorted(rows):
        target -= weight
        if target <= 0:
            return x
    raise AssertionError("Rang hors fenêtre")


def legacy_batch(window, qs):
    return tuple(legacy_quantile(window,q) for q in qs)


def run():
    results = []
    for size,eps in ((200,.01),(1000,.05),(5000,.05)):
        data = list(values("dérive", size+400, 42))
        window = WindowQuantiles(size,eps)
        warm = []
        for value in data[:size]:
            window.add(value)
        for value in data[size:]:
            window.add(value)
            assert window.quantiles(PROBABILITIES) == legacy_batch(window,PROBABILITIES)
            warm.append((window.quantiles(PROBABILITIES), value))
        paths = {
            "v3": lambda: legacy_batch(window,PROBABILITIES),
            "v4": lambda: window.quantiles(PROBABILITIES),
        }
        timings = {name: [] for name in paths}
        end_to_end = {name: [] for name in paths}
        updates = []
        for repetition in range(5):
            order = ("v3","v4") if repetition%2==0 else ("v4","v3")
            pure = WindowQuantiles(size,eps)
            start = perf_counter_ns()
            for x in data:
                pure.add(x)
            updates.append((perf_counter_ns()-start)/len(data))
            for name in order:
                path = paths[name]
                start = perf_counter_ns()
                for _ in range(80):
                    path()
                timings[name].append((perf_counter_ns()-start)/80)
                monitor = Monitor(size=size,eps=eps)
                if name=="v3":
                    monitor.recent.quantiles = lambda qs: legacy_batch(monitor.recent,qs)
                for x in data[:size]:
                    monitor.add(x)
                start = perf_counter_ns()
                for x in data[size:]:
                    monitor.add(x)
                end_to_end[name].append((perf_counter_ns()-start)/400)
        row = dict(N=size,eps=eps,seed=42,representatives=window.state_size,
                   events_checked=len(warm),update_only_ns=median(updates),measurements={})
        for name,path in paths.items():
            tracemalloc.start()
            path()
            _,peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            processing = median(end_to_end[name])
            row["measurements"][name] = dict(query_ns=median(timings[name]), full_ns=processing,
                                            events_per_second=1e9/processing, query_peak_bytes=peak,
                                            query_repetitions_ns=timings[name], full_repetitions_ns=end_to_end[name])
        results.append(row)
    return results


if __name__ == "__main__":
    rows = run()
    Path("results/query_benchmark.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8")
