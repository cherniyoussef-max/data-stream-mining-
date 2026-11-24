from bisect import bisect_left, bisect_right
from collections import Counter
from itertools import permutations
from scipy.stats import chi2, chisquare

from algorithms import Reservoir, WeightedReservoir


def rank_error(ordered, value, target):
    low = bisect_left(ordered, value) + 1
    high = bisect_right(ordered, value)
    return max(0, low - target, target - high)


def uniform_trial():
    counts = [0] * 100
    for seed in range(10_000):
        reservoir = Reservoir(10, seed)
        for x in range(100):
            reservoir.add(x)
        for x in reservoir.sample():
            counts[x] += 1
    statistic, p = chisquare(counts, [1000] * 100)
    return dict(counts=counts, expected=1000, statistic=float(statistic), p=float(p),
                adjusted_p=float(chi2.sf(statistic * 99 / 90, 99)))


def weighted_trial(k, weights=(1, 2, 4)):
    counts = Counter()
    for seed in range(10_000, 20_000):
        reservoir = WeightedReservoir(k, seed)
        for x, w in enumerate(weights):
            reservoir.add(x, w)
        counts.update(reservoir.sample())
    expected = [0.] * len(weights)
    for sequence in permutations(range(len(weights)), k):
        remaining = sum(weights)
        probability = 1.
        for x in sequence:
            probability *= weights[x] / remaining
            remaining -= weights[x]
        for x in sequence:
            expected[x] += probability
    return dict(k=k, weights=weights, counts=[counts[x] for x in range(len(weights))],
                expected=expected, trials=10_000)


def target_rank(q, n, eps):
    target = q * n
    nearest = max(1, round(target))
    if abs(nearest - target) > eps * n:
        return nearest
    return target
