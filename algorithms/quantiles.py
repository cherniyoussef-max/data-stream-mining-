from bisect import bisect_right
from collections import deque
import math
from typing import Collection, Iterable

from .sampling import positive_int


def _check_q(q: float) -> None:
    if not 0 <= q <= 1:
        raise ValueError("q doit appartenir à [0, 1].")


def _check_value(x: float) -> None:
    if not math.isfinite(x):
        raise ValueError("La mesure doit être finie.")


def exact_quantile(values: Collection[float], q: float) -> float:
    _check_q(q)
    if not values:
        raise ValueError("Le flux est vide.")
    return sorted(values)[max(1, math.ceil(q * len(values))) - 1]


class GKQuantile:
    """GK rank invariants with a simplified right-to-left compression pass."""

    def __init__(self, eps: float):
        if not 0 < eps < 0.5:
            raise ValueError("ε doit appartenir à ]0, 0.5[.")
        self.eps = eps
        self.n = 0
        self.sample: list[tuple[float, int, int]] = []
        numerator, denominator = eps.as_integer_ratio()
        self._twice_eps = 2 * numerator
        self._eps_denominator = denominator
        period = 0.5 / eps
        self._period = max(1, int(period) if math.isfinite(period) else denominator // self._twice_eps)

    def add(self, x: float) -> None:
        _check_value(x)
        index = bisect_right(self.sample, x, key=lambda row: row[0])
        self.n += 1
        limit = self._twice_eps * self.n // self._eps_denominator
        delta = max(0, limit - 1) if 0 < index < len(self.sample) else 0
        self.sample.insert(index, (x, 1, delta))
        if limit >= 2 and self.n % self._period == 0:
            self._compress(limit)

    def _compress(self, limit: int) -> None:
        reverse = [self.sample[-1]]
        for index in range(len(self.sample) - 2, 0, -1):
            value, gap, delta = self.sample[index]
            next_value, next_gap, next_delta = reverse[-1]
            if gap + next_gap + next_delta <= limit:
                reverse[-1] = (next_value, gap + next_gap, next_delta)
            else:
                reverse.append((value, gap, delta))
        reverse.append(self.sample[0])
        self.sample = reverse[::-1]

    def quantile(self, q: float) -> float:
        _check_q(q)
        if not self.sample:
            raise ValueError("Le résumé GK est vide.")
        if q == 0:
            return self.sample[0][0]
        if q == 1:
            return self.sample[-1][0]
        target = q * self.n
        error = self.eps * self.n
        if error < 0.5:
            return self.sample[max(1, round(target)) - 1][0]
        lower = 0
        previous = self.sample[0][0]
        for value, gap, delta in self.sample:
            lower += gap
            if lower + delta > target + error:
                return previous
            previous = value
        return previous


class WindowQuantiles:
    """Bounded recent quantiles using weighted representatives of fixed blocks."""

    def __init__(self, size: int, eps: float):
        positive_int(size, "N")
        if not 0 < eps < 0.5:
            raise ValueError("ε doit appartenir à ]0, 0.5[.")
        self.size = size
        self.block_size = math.isqrt(size)
        self.stride = max(1, math.ceil(eps * self.block_size))
        self._completed: deque[tuple[int, list[tuple[float, int]]]] = deque()
        self._pending: list[float] = []
        self.n = 0

    def add(self, x: float) -> None:
        _check_value(x)
        self.n += 1
        self._pending.append(x)
        if len(self._pending) == self.block_size:
            ordered = sorted(self._pending)
            representatives = []
            for start in range(0, len(ordered), self.stride):
                end = min(start + self.stride, len(ordered))
                representatives.append((ordered[end - 1], end - start))
            self._completed.append((self.n, representatives))
            self._pending.clear()
        while self._completed and self._completed[0][0] <= self.n - self.size:
            self._completed.popleft()

    @property
    def state_size(self) -> int:
        return len(self._pending) + sum(len(rows) for _, rows in self._completed)

    @property
    def stale_count(self) -> int:
        if not self._completed:
            return 0
        return max(0, self.n - self.size - self._completed[0][0] + self.block_size)

    @property
    def rank_bound(self) -> int:
        return self.stale_count + len(self._completed) * (self.stride - 1)

    def block_snapshot(self) -> list[tuple[int, bool, tuple[tuple[float, int], ...]]]:
        cutoff = self.n - self.size
        return [(end, end - self.block_size < cutoff, tuple(rows))
                for end, rows in self._completed]

    def open_block(self) -> tuple[float, ...]:
        return tuple(self._pending)

    def quantile(self, q: float) -> float:
        return self.quantiles((q,))[0]

    def quantiles(self, qs: Iterable[float]) -> tuple[float, ...]:
        """Return quantiles in caller order, using one sort and one scan."""
        probabilities = tuple(qs)
        for q in probabilities:
            _check_q(q)
        if not probabilities:
            return ()
        if not self.n:
            raise ValueError("La fenêtre est vide.")
        retained_count = min(self.n, self.size) + self.stale_count
        targets = sorted((max(1, math.ceil(q * retained_count)), index)
                         for index, q in enumerate(probabilities))
        rows = [(x, 1) for x in self._pending]
        for _, representatives in self._completed:
            rows.extend(representatives)
        answers = [0.] * len(targets)
        cumulative = 0
        cursor = 0
        for x, weight in sorted(rows):
            cumulative += weight
            while cursor < len(targets) and targets[cursor][0] <= cumulative:
                answers[targets[cursor][1]] = x
                cursor += 1
            if cursor == len(targets):
                return tuple(answers)
        raise AssertionError("Rang hors fenêtre")
