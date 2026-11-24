"""Démonstration reproductible sans serveur web."""
import argparse

from streaming.engine import Monitor
from streaming.generators import values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--events", type=int, default=1200)
    args = parser.parse_args()
    if args.events < 1:
        parser.error("--events doit être positif")
    monitor = Monitor(size=min(200, max(1, args.events // 6)), seed=args.seed, evaluate=True)
    print(f"Latence synthétique | graine={args.seed} | événements={args.events} | N={monitor.dgim.N}")
    previous = None
    for x in values("dérive", args.events, args.seed):
        row = monitor.add(x)
        if row["state"] != previous:
            print(f"t={row['t']}: {row['state']} (P99 récent {row['p99']:.2f} ms)")
            previous = row["state"]
    print("Réservoir uniforme :", monitor.uniform.sample())
    print("Réservoir pondéré :", monitor.weighted.sample())
    print("DGIM, estimé / exact :", row["estimated"], "/", row["exact_count"])
    print(f"GK historique, médiane / P99 : {monitor.gk.quantile(.5):.2f} / {row['historical']:.2f} ms")
    print(f"Fenêtre récente, médiane / P99 : {row['median']:.2f} / {row['p99']:.2f} ms")
    print(f"Fenêtre exacte, médiane / P99 : {row['exact_median']:.2f} / {row['exact_p99']:.2f} ms")
    print("Expériences et figures : python -m evaluation.benchmark --profile quick")


if __name__ == "__main__":
    main()
