import math
from test_projet4 import Reservoir, WeightedReservoir, DGIM, GKQuantile

def test_reservoir_uniformity():
    k = 10
    n = 100
    res = Reservoir(k, seed=42)
    for i in range(n):
        res.add(i)
    assert len(res.sample()) == k

def test_dgim_count():
    N = 50
    dgim = DGIM(N)
    stream = [1, 0, 1, 1, 0, 1, 0, 1] * 10
    for bit in stream:
        dgim.add(bit)
    exact_count = sum(stream[-N:])
    approx_count = dgim.count()
    # La garantie DGIM assure une erreur d'au plus 50%
    assert abs(approx_count - exact_count) <= 0.5 * exact_count

def test_gk_quantile():
    eps = 0.01
    gk = GKQuantile(eps)
    for x in range(1, 1001):
        gk.add(x)
    med = gk.quantile(0.5)
    # Vérification que la médiane estimée est proche de la vraie médiane (500)
    assert 450 <= med <= 550

import pytest
from scipy.stats import chisquare
from test_projet4 import Reservoir, WeightedReservoir, DGIM, GKQuantile  # Remplacez "projet4" par le nom réel de votre fichier de classes

def test_reservoir_chi2_uniformity():
    n = 100
    k = 10
    num_simulations = 10000

    counts = {i: 0 for i in range(n)}
    for sim in range(num_simulations):
        res = Reservoir(k=k, seed=sim)
        for x in range(n):
            res.add(x)
        for item in res.sample():
            counts[item] += 1

    observed = [counts[i] for i in range(n)]
    expected_freq = (k / n) * num_simulations
    expected = [expected_freq] * n

    chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
    print(f"\n[Chi2] Statistique : {chi2_stat:.4f}, p-valeur : {p_value:.4f}")
    assert p_value > 0.05
####### tfarej ya naser chof il comentaire ijdid