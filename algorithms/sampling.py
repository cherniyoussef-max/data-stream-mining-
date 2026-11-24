import heapq
import math
import random
from typing import Generic, TypeVar

T = TypeVar("T")


def positive_int(value: int, name: str) -> None:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} doit être un entier positif.")


class Reservoir(Generic[T]):
    """Algorithm R, sampling stream positions without replacement."""

    def __init__(self, k: int, seed: int | None = None):
        positive_int(k, "k")
        self.k = k
        self.n = 0
        self.rng = random.Random(seed)
        self._items: list[T] = []

    def add(self, x: T) -> None:
        self.n += 1
        if self.n <= self.k:
            self._items.append(x)
            return
        index = self.rng.randrange(self.n)
        if index < self.k:
            self._items[index] = x

    def sample(self) -> list[T]:
        return self._items.copy()


class WeightedReservoir(Generic[T]):
    """A-Res with a logarithm of the exponential race time."""

    def __init__(self, k: int, seed: int | None = None):
        positive_int(k, "k")
        self.k = k
        self.n = 0
        self.rng = random.Random(seed)
        self._heap: list[tuple[float, int, float, T]] = []

    def add(self, x: T, w: float) -> None:
        if not math.isfinite(w) or w <= 0:
            raise ValueError("Le poids doit être fini et positif.")
        u = self.rng.random()
        while u == 0:
            u = self.rng.random()
        priority = math.log(w) - math.log(-math.log(u))
        self.n += 1
        entry = (priority, self.n, w, x)
        if len(self._heap) < self.k:
            heapq.heappush(self._heap, entry)
        elif entry > self._heap[0]:
            heapq.heapreplace(self._heap, entry)

    def sample(self) -> list[T]:
        return [entry[3] for entry in self._heap]

    def entries(self) -> list[tuple[T, float, float]]:
        return [(item, weight, key) for key, _, weight, item in sorted(self._heap, reverse=True)]
