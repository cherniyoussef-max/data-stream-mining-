from collections import deque
from dataclasses import dataclass
import math

from algorithms import DGIM, GKQuantile, Reservoir, WeightedReservoir, WindowQuantiles


@dataclass
class Alerts:
    median_limit: float
    p99_limit: float
    minimum: int
    active: bool = False
    state: str = "Initialisation"

    def update(self, count: int, median: float, p99: float) -> str:
        if count < self.minimum:
            return self.state
        exceeded = median > self.median_limit or p99 > self.p99_limit
        self.state = "Alerte" if exceeded else "Rétablissement" if self.active else "Normal"
        self.active = exceeded
        return self.state


class Monitor:
    def __init__(self, k=20, size=200, eps=.01, seed=42, slow=90., median=80.,
                 p99=110., weighted=True, evaluate=False):
        if any(not math.isfinite(v) or v <= 0 for v in (slow, median, p99)):
            raise ValueError("Les seuils doivent être finis et positifs.")
        self.uniform = Reservoir(k, seed)
        self.weighted = WeightedReservoir(k, seed + 1)
        self.dgim = DGIM(size)
        self.gk = GKQuantile(eps)
        self.recent = WindowQuantiles(size, eps)
        self.alerts = Alerts(median, p99, min(20, size))
        self.exact = deque(maxlen=size) if evaluate else None
        self.exact_alerts = Alerts(median, p99, min(20, size)) if evaluate else None
        self.slow = slow
        self.weighted_by_latency = weighted

    def add(self, latency: float) -> dict:
        if not math.isfinite(latency) or latency < 0:
            raise ValueError("Latence finie et positive ou nulle requise.")
        self.uniform.add(latency)
        self.weighted.add(latency, max(1., latency) if self.weighted_by_latency else 1.)
        self.dgim.add(latency > self.slow)
        self.gk.add(latency)
        self.recent.add(latency)
        if self.exact is not None:
            self.exact.append(latency)
        n = self.gk.n
        median, p95, p99 = self.recent.quantiles((.50, .95, .99))
        row = dict(t=n, latency=latency, median=median, p95=p95, p99=p99,
                   historical=self.gk.quantile(.99), estimated=self.dgim.count(),
                   state=self.alerts.update(min(n, self.dgim.N), median, p99))
        if self.exact is not None:
            ordered = sorted(self.exact)
            for name, q in (("median", .50), ("p95", .95), ("p99", .99)):
                row[f"exact_{name}"] = ordered[max(1, math.ceil(q * len(ordered))) - 1]
            row["exact_count"] = sum(x > self.slow for x in ordered)
            row["exact_state"] = self.exact_alerts.update(len(ordered), row["exact_median"], row["exact_p99"])
        return row
