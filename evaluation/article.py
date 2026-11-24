"""Build the final LaTeX article from measured results."""
import csv
import json
from pathlib import Path
import shutil
from statistics import mean, median, quantiles
import subprocess
from tempfile import TemporaryDirectory


def build():
    root = Path(__file__).resolve().parents[1]
    results = root / "results"
    target = root / "docs/report"

    def read_json(name):
        return json.loads((results / name).read_text(encoding="utf-8"))

    def read_csv(name):
        with (results / name).open(encoding="utf-8", newline="") as source:
            return list(csv.DictReader(source))

    stats = read_json("statistical_results.json")["uniform"]
    benchmark = read_json("benchmark_summary.json")
    study = read_json("final_study.json")
    incident = study["alerts"][1]
    memory = read_csv("memory_scaling.csv")
    fifo = next(r for r in memory if r["N"] == "10000" and r["method"] == "FIFO")
    blocks = next(r for r in memory if r["N"] == "10000" and r["method"] == "Blocs récents" and r["eps"] == "0.05")
    raw = read_csv("metrics.csv")
    dgim = [float(r["error"]) for r in raw if r["algorithm"] == "DGIM"]
    gk = [r for r in raw if r["algorithm"] == "GK"]
    growth = read_csv("gk_growth.csv")
    sensitivity = read_csv("alert_sensitivity.csv")
    identifiers = ("algorithm", "seed", "window", "n", "k", "eps", "q", "distribution")
    assert len(raw) == len({tuple(row[key] for key in identifiers) for row in raw})

    def number(value, decimals=3):
        return f"{float(value):.{decimals}f}".replace(".", "{,}")

    def percent(value):
        return number(float(value)*100, 2) + r"\,\%"

    def lookup_state(state):
        return next(r["t"] for r in benchmark["transitions"] if r["state"] == state)

    def f1(size):
        return number(next(r["f1"] for r in sensitivity if r["N"] == str(size) and r["eps"] == "0.05"))

    data = {
        "Pearson": number(stats["statistic"]), "PearsonP": number(stats["p"], 6),
        "PearsonAdj": number(stats["adjusted_p"], 6), "DgMax": percent(max(dgim)),
        "DgMean": percent(mean(dgim)), "DgP": percent(quantiles(dgim, n=20)[-1]),
        "AlertAt": lookup_state("Alerte"), "RecoverAt": lookup_state("Rétablissement"),
        "StudyCPU": study["cpu"], "StudyRAM": int(study["ram"].split()[0])//1024,
        "StudyPython": study["python"], "MedErr": number(median(float(r["value_error"]) for r in gk if r["q"]=="0.5")),
        "TailErr": number(median(float(r["value_error"]) for r in gk if r["q"]=="0.99")),
        "GKState": max(int(r["entries"]) for r in growth if r["eps"]=="0.01" and r["n"]=="100000"),
        "RecentCount": study["measurements"]["alerts"], "RecentMax": study["recent_rank_max"],
        "RecentNorm": percent(study["recent_max_normalized_error"]),
        "FifoBytes": fifo["ingest_peak_bytes"], "BlockBytes": blocks["ingest_peak_bytes"],
        "FifoQueryMem": fifo["query_extra_peak_bytes"], "BlockQueryMem": blocks["query_extra_peak_bytes"],
        "FifoTime": number(fifo["update_ns"], 1), "BlockTime": number(blocks["update_ns"], 1),
        "FifoQuery": number(float(fifo["query_ns"])/1e6), "BlockQuery": number(float(blocks["query_ns"])/1e6),
        "Accuracy": percent(incident["accuracy"]), "Precision": percent(incident["precision"]),
        "Recall": percent(incident["recall"]), "Specificity": percent(incident["specificity"]),
        "Fone": number(incident["f1"], 2), "SmallF": f1(50), "LargeF": f1(500),
    }
    (target/"measurements.tex").write_text(
        "% Fichier produit à partir des résultats exportés.\n" +
        "".join(r"\newcommand{\%s}{%s}" % (k,v) + "\n" for k,v in data.items()), encoding="utf-8")
    with TemporaryDirectory() as output:
        subprocess.run(["tectonic", "--keep-logs", "--outdir", output, "main.tex"], cwd=target, check=True)
        metadata = subprocess.check_output(["pdfinfo", str(Path(output)/"main.pdf")], text=True)
        pages = int(next(line.split(":")[1] for line in metadata.splitlines() if line.startswith("Pages:")))
        if not 6 <= pages <= 8:
            raise ValueError(f"Rapport hors du budget de 6 à 8 pages : {pages}")
        shutil.copyfile(Path(output)/"main.pdf", target/"rapport-projet4-final.pdf")
        print(metadata)


if __name__ == "__main__":
    build()
