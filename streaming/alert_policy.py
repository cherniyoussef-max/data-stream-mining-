"""Optional incident detector with corroboration and persistence."""
from algorithms import DGIM


class PersistentAlerts:
    """Require threshold exceedance and a minimum recent slow-event fraction."""

    def __init__(self, size, median_limit, p99_limit, slow=90., fraction=.15, persistence=3):
        self.evidence = DGIM(min(size,50))
        self.median_limit = median_limit
        self.p99_limit = p99_limit
        self.slow = slow
        self.fraction = fraction
        self.persistence = persistence
        self.minimum = min(20,size)
        self.n = 0
        self.active = False
        self.opposite_run = 0

    def add(self, latency, median, p99):
        self.n += 1
        self.evidence.add(latency > self.slow)
        if self.n < self.minimum:
            return "Initialisation"
        active_count = min(self.n,self.evidence.N)
        changed = (median > self.median_limit or p99 > self.p99_limit) and (
            self.evidence.count() >= self.fraction*active_count
        )
        if changed == self.active:
            self.opposite_run = 0
        else:
            self.opposite_run += 1
            if self.opposite_run >= self.persistence:
                self.active = changed
                self.opposite_run = 0
                if not self.active:
                    return "Rétablissement"
        return "Alerte" if self.active else "Normal"
