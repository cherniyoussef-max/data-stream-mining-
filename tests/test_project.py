from collections import Counter, deque
from itertools import product
import math

import pytest

from algorithms import DGIM, GKQuantile, Reservoir, WeightedReservoir, WindowQuantiles, exact_quantile
from evaluation.statistics import rank_error, target_rank, uniform_trial, weighted_trial
from streaming.engine import Monitor
from streaming.generators import DISTRIBUTIONS, bernoulli, values


def test_t1_uniform():
    result = uniform_trial()
    assert sum(result["counts"]) == 100_000
    assert result["p"] > .05


@pytest.mark.parametrize("k", [1, 2])
def test_t2_weighted(k):
    result = weighted_trial(k)
    frequencies = [x / result["trials"] for x in result["counts"]]
    assert frequencies[0] < frequencies[1] < frequencies[2]
    for frequency, expected in zip(frequencies, result["expected"]):
        assert abs(frequency - expected) <= 5 * math.sqrt(expected * (1 - expected) / result["trials"])


def check_dgim(n, bits):
    sketch = DGIM(n)
    oracle = deque(maxlen=n)
    for bit in bits:
        sketch.add(bit)
        oracle.append(bit)
        exact = sum(oracle)
        assert abs(sketch.count() - exact) <= .5 * exact
        ages = [sketch.age(t) for t, _ in sketch.buckets]
        sizes = [size for _, size in sketch.buckets]
        assert ages == sorted(set(ages))
        assert all(0 <= a < n and oracle[-1-a] for a in ages)
        assert sizes == sorted(sizes)
        assert all(s > 0 and s & (s - 1) == 0 for s in sizes)
        assert max(Counter(sizes).values(), default=0) <= 2
        assert sketch.num_buckets() <= 2 * n.bit_length()


@pytest.mark.parametrize("n", [1, 2, 3, 5, 8, 13])
def test_t3_t4_exhaustive(n):
    for bits in product((0, 1), repeat=9):
        check_dgim(n, bits)


@pytest.mark.parametrize("n", [32, 100, 500, 1000, 5000])
def test_t3_t4_wrap_and_patterns(n):
    for density in (0., .01, .5, .99, 1.):
        check_dgim(n, bernoulli(3*n+20, density, 42))
    check_dgim(n, (i % 2 for i in range(3*n+20)))
    check_dgim(n, (int(i % 37 < 10) for i in range(3*n+20)))


@pytest.mark.parametrize("eps", [.001, .005, .01, .05, .1])
@pytest.mark.parametrize("kind", DISTRIBUTIONS)
def test_t5_rank(kind, eps):
    sketch = GKQuantile(eps)
    seen = []
    for x in values(kind, 6000, 42):
        seen.append(x)
        sketch.add(x)
        n = len(seen)
        if n in (1, 2, 3, 10, 100, 499, 1000, 3001, 6000):
            ordered = sorted(seen)
            assert sketch.quantile(0) == ordered[0]
            assert sketch.quantile(1) == ordered[-1]
            assert sum(g for _, g, _ in sketch.sample) == n
            assert all(g + d <= max(1, math.floor(2 * eps * n)) for _, g, d in sketch.sample)
            for q in (.01, .1, .25, .5, .75, .9, .95, .99):
                assert rank_error(ordered, sketch.quantile(q), target_rank(q, n, eps)) <= eps*n + 1e-10
    assert len(sketch.sample) < len(seen)


@pytest.mark.parametrize("n", [1, 4, 100, 625])
def test_recent_bound(n):
    sketch = WindowQuantiles(n, .15)
    oracle = deque(maxlen=n)
    for x in values("dérive", 1500, 204):
        sketch.add(x)
        oracle.append(x)
        if len(oracle) < 5 or sketch.n % 7 == 0:
            ordered = sorted(oracle)
            for q in (.01, .5, .99):
                estimate = sketch.quantile(q)
                # An expired representative can lie in a rank gap; measure its insertion rank.
                low = sum(y < estimate for y in ordered)
                high = sum(y <= estimate for y in ordered)
                target = math.ceil(q * len(oracle))
                assert max(0, low + 1 - target, target - high) <= sketch.rank_bound


def test_alert_and_recovery():
    monitor = Monitor(size=50, evaluate=True)
    states = [monitor.add(x)["state"] for x in values("dérive", 450, 42)]
    assert states[0] == "Initialisation"
    assert 150 <= states.index("Alerte") < 200
    assert 300 <= states.index("Rétablissement") < 360
    assert states[-1] == "Normal"
    assert monitor.recent.quantile(.99) < monitor.gk.quantile(.99)


def test_invalid_inputs_and_compatibility():
    import test_projet4
    assert test_projet4.GKQuantile is GKQuantile
    for cls in (Reservoir, WeightedReservoir, DGIM):
        with pytest.raises(ValueError):
            cls(0)
    for cls in (GKQuantile, lambda eps: WindowQuantiles(10, eps)):
        with pytest.raises(ValueError):
            cls(float("nan"))
        obj = cls(.1)
        with pytest.raises(ValueError):
            obj.quantile(.5)
        with pytest.raises(ValueError):
            obj.add(float("inf"))
    with pytest.raises(ValueError):
        DGIM(1).add(2)
    weighted = WeightedReservoir(1, 42)
    for weight in (0, -1, float("inf"), float("nan")):
        with pytest.raises(ValueError):
            weighted.add({}, weight)
    weighted.add({}, 5e-324)
    weighted.add({"large": True}, 1e308)
    assert weighted.sample() == [{"large": True}]


def test_reproducibility_and_sample_copy():
    a, b = Reservoir(3, 42), Reservoir(3, 42)
    assert a.sample() == []
    for i in range(50):
        a.add(i % 3)
        Reservoir(1, i).add(i)
        b.add(i % 3)
    assert a.sample() == b.sample()
    a.sample().clear()
    assert len(a.sample()) == 3
    assert exact_quantile([1, 2, 3, 4], .5) == 2
