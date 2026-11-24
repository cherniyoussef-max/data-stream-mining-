from bisect import bisect_left, bisect_right
from collections import deque
import itertools
import math

import pytest
from scipy.stats import chi2

from algorithms import GKQuantile, WindowQuantiles
from evaluation.statistics import uniform_trial, weighted_trial
from streaming.engine import Monitor


def test_pearson_covariance_adjustment():
    result = uniform_trial()
    squared = sum((count - 1000)**2 for count in result["counts"])
    assert result["statistic"] == pytest.approx(squared / 1000)
    assert result["adjusted_p"] == pytest.approx(chi2.sf(squared / (1000 * 90 / 99), 99))


@pytest.mark.parametrize("weights", [(1, 1, 1, 1, 1), (1, 2, 3, 7, 11)])
def test_weighted_larger_k(weights):
    result = weighted_trial(3, weights)
    for count, expected in zip(result["counts"], result["expected"]):
        assert abs(count - 10_000*expected) <= 5*math.sqrt(10_000*expected*(1-expected))
    if len(set(weights)) == 1:
        assert result["expected"] == pytest.approx([.6]*5)


@pytest.mark.parametrize("eps", [.001, .005, .01, .05, .10])
def test_gk_very_low_quantiles(eps):
    sketch = GKQuantile(eps)
    for n in range(1, 1801):
        sketch.add(n)
        for q in (.00001, .0001, .001, .01, .1, .33, .5, .99):
            target = q*n
            low = max(1, math.ceil(target - eps*n))
            high = min(n, math.floor(target + eps*n))
            answer = sketch.quantile(q)
            if low <= high:
                assert low <= answer <= high
            else:
                assert answer == max(1, round(target))


@pytest.mark.parametrize("size", [1, 4, 7, 9, 17, 100])
def test_recent_cdf_inequalities(size):
    sketch = WindowQuantiles(size, .25)
    oracle = deque(maxlen=size)
    feed = itertools.chain((99.,), (0.,)*size, (float((i*17)%13) for i in range(12*size)))
    for x in feed:
        sketch.add(x)
        oracle.append(x)
        ordered = sorted(oracle)
        assert 0 <= sketch.stale_count < sketch.block_size
        for q in (0., .01, .5, .99, 1.):
            value = sketch.quantile(q)
            target = max(1, math.ceil(q*len(ordered)))
            assert bisect_left(ordered, value) < target + sketch.rank_bound
            assert bisect_right(ordered, value) >= target - sketch.rank_bound


def test_expired_representative_is_a_threshold():
    sketch = WindowQuantiles(4, .2)
    for x in (99, 1, 2, 3, 4):
        sketch.add(x)
    assert sketch.quantile(1) == 99
    assert sketch.stale_count == 1
    assert sketch.rank_bound == 1


def test_exact_alert_reference_and_reset():
    monitor = Monitor(size=20, evaluate=True)
    output = [monitor.add(x) for x in [30]*30 + [140]*25 + [30]*25]
    assert [row["exact_state"] for row in output[:74]] == [row["state"] for row in output[:74]]
    assert output[30]["exact_state"] == "Alerte"
    assert output[74]["exact_state"] == "Rétablissement"
    assert output[74]["state"] == "Alerte"
    assert output[75]["state"] == "Rétablissement"
    assert Monitor(size=10, evaluate=True).add(100)["exact_state"] == "Initialisation"
