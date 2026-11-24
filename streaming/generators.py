import random
from collections.abc import Iterator


DISTRIBUTIONS = ("uniforme", "gaussienne", "dérive", "constante", "croissante",
                 "décroissante", "répétitions", "queue lourde", "rafales")


def values(kind: str, n: int, seed: int) -> Iterator[float]:
    rng = random.Random(seed)
    for i in range(n):
        match kind:
            case "uniforme": yield rng.uniform(5, 70)
            case "gaussienne": yield max(1, rng.gauss(30, 6))
            case "dérive": yield max(1, rng.gauss(160 if n // 3 <= i < 2 * n // 3 else 30, 6))
            case "constante": yield 30
            case "croissante": yield i
            case "décroissante": yield n - i
            case "répétitions": yield i % 7
            case "queue lourde": yield 10 * rng.paretovariate(1.5)
            case "rafales": yield rng.uniform(100, 200) if i % 50 < 5 else rng.uniform(20, 40)
            case _: raise ValueError(f"Distribution inconnue : {kind}")


def bernoulli(n: int, p: float, seed: int) -> Iterator[int]:
    rng = random.Random(seed)
    for _ in range(n):
        yield int(rng.random() < p)
