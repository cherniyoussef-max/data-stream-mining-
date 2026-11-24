from bisect import bisect_left, bisect_right, insort
from collections import Counter, deque
import math

from hypothesis import given, settings, strategies as st
import pytest

from algorithms import DGIM, GKQuantile, WindowQuantiles
from evaluation.query_benchmark import legacy_quantile
from streaming.alert_policy import PersistentAlerts


@settings(max_examples=100, derandomize=True, deadline=None)
@given(st.lists(st.integers(-50, 50), min_size=1, max_size=240),
       st.sampled_from((.001, .01, .03, .05, .12, .25)))
def test_gk_rank_and_compression(values, eps):
    sketch = GKQuantile(eps)
    ordered = []
    for n, value in enumerate(values, 1):
        sketch.add(value)
        insort(ordered, value)
        limit = sketch._twice_eps * n // sketch._eps_denominator
        assert sum(g for _, g, _ in sketch.sample) == n
        assert all(1 <= g and 0 <= d and g+d <= max(1, limit) for _,g,d in sketch.sample)
        assert sketch.quantile(0) == ordered[0] and sketch.quantile(1) == ordered[-1]
        if limit >= 2 and n % sketch._period == 0:
            tail = sketch.sample[1:]
            assert all(left[1] + right[1] + right[2] > limit
                       for left,right in zip(tail,tail[1:]))
        for q in (.001, .025, .20, .5, .75, .975, .99):
            result = sketch.quantile(q)
            target = q*n
            closest = max(1, round(target))
            if abs(closest-target) > eps*n:
                target = closest
            assert bisect_left(ordered, result)+1 <= target+eps*n+1e-10
            assert bisect_right(ordered, result) >= target-eps*n-1e-10


@settings(max_examples=125, derandomize=True, deadline=None)
@given(st.integers(1,96), st.lists(st.tuples(st.integers(0,1), st.integers(1,40)), max_size=30))
def test_dgim_adversarial_runs(n, runs):
    sketch, exact = DGIM(n), deque(maxlen=n)
    for bit, length in runs:
        for _ in range(length):
            sketch.add(bit)
            exact.append(bit)
            actual = sum(exact)
            assert 2*abs(sketch.count()-actual) <= actual
            ages = [sketch.age(t) for t,_ in sketch.buckets]
            assert ages == sorted(set(ages))
            assert all(age < len(exact) and exact[-1-age] == 1 for age in ages)
            sizes = [s for _,s in sketch.buckets]
            assert sizes == sorted(sizes)
            assert all(s > 0 and s & (s-1) == 0 for s in sizes)
            assert all(c<=2 for c in Counter(sizes).values())


@settings(max_examples=110, derandomize=True, deadline=None)
@given(st.integers(1,144), st.sampled_from((.001,.05,.15,.45)),
       st.lists(st.integers(-20,20), min_size=1, max_size=210),
       st.lists(st.integers(0,100).map(lambda x:x/100), max_size=8))
def test_recent_batch_matches_v3_and_cdf(size, eps, values, probabilities):
    sketch, active = WindowQuantiles(size,eps), deque(maxlen=size)
    qs = (*probabilities, 1., .5, 0., .5)
    for t,value in enumerate(values,1):
        sketch.add(value)
        active.append(value)
        result = sketch.quantiles(iter(qs))
        assert result == tuple(legacy_quantile(sketch,q) for q in qs)
        b,s = sketch.block_size,sketch.stride
        assert sketch.state_size <= b-1 + (math.ceil(size/b)+1)*math.ceil(b/s)
        assert sketch.stale_count == (max(0,t-size) % b)
        ordered = sorted(active)
        for q,x in zip(qs,result):
            k = max(1,math.ceil(q*len(ordered)))
            assert bisect_left(ordered,x) < k+sketch.rank_bound
            assert bisect_right(ordered,x) >= k-sketch.stale_count


def test_batch_validation_and_tiny_epsilon_schedule():
    window = WindowQuantiles(4,.1)
    assert window.quantiles([]) == ()
    with pytest.raises(ValueError):
        window.quantiles([.5])
    window.add(1)
    with pytest.raises(ValueError):
        window.quantiles([.5, float("nan")])
    gk = GKQuantile(5e-324)
    assert gk._period > 0
    for x in (3,1,2):
        gk.add(x)
    assert gk.quantile(.5) == 2


def test_persistent_alert_rejects_isolated_evidence_and_recovers():
    policy = PersistentAlerts(50,80,110)
    for _ in range(50):
        policy.add(30,30,30)
    assert policy.add(180,30,180) == "Normal"
    assert "Alerte" in [policy.add(180,180,180) for _ in range(20)]
    states = [policy.add(30,30,30) for _ in range(5)]
    assert states[:3] == ["Alerte","Alerte","Rétablissement"]
    assert states[3:] == ["Normal","Normal"]
