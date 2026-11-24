import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def figures(output, rows, statistical, timeline, monitor):
    output.mkdir(parents=True, exist_ok=True)

    def chart(name, title, xlabel, ylabel, plot):
        fig, ax = plt.subplots(figsize=(7, 3.4), layout="constrained")
        plot(ax)
        ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
        ax.grid(alpha=.2)
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend()
        fig.savefig(output/f"{name}.png", dpi=200)
        plt.close(fig)

    u = statistical["uniform"]
    chart("01_uniforme", "Inclusions du réservoir uniforme", "Position", "Inclusions",
          lambda ax: (ax.bar(range(100), u["counts"]), ax.axhline(u["expected"], color="orange", label="Espérance")))
    weighted = statistical["weighted"]
    def weighted_plot(ax):
        for result in weighted:
            k = result["k"]
            ax.plot(result["weights"], result["expected"], "--", label=f"Référence k={k}")
            ax.scatter(result["weights"], [x/result["trials"] for x in result["counts"]], label=f"Observé k={k}")
    chart("02_pondere", "Inclusions A-Res", "Poids", "Probabilité d’inclusion", weighted_plot)
    dg = [r for r in rows if r["algorithm"]=="DGIM"]
    gk = [r for r in rows if r["algorithm"]=="GK"]
    def parity(ax, selected):
        lo = min(r["exact"] for r in selected)
        hi = max(r["exact"] for r in selected)
        ax.plot([lo,hi],[lo,hi], "--", color="orange", label="Égalité")
        ax.scatter([r["exact"] for r in selected],[r["estimate"] for r in selected], s=12, alpha=.5)
    chart("03_dgim_exact", "DGIM et oracle exact", "Comptage exact", "Comptage estimé", lambda ax: parity(ax,dg))
    chart("04_dgim_erreur", "Erreur DGIM et borne maximale", "Taille de fenêtre N", "Erreur relative",
          lambda ax: (ax.scatter([r["window"] for r in dg],[r["error"] for r in dg], alpha=.2),
                      ax.axhline(.5,color="orange",label="Borne 50 %")))
    sizes = sorted({r["window"] for r in dg})
    chart("05_dgim_memoire", "Croissance du nombre de buckets", "Taille de fenêtre N", "Buckets",
          lambda ax: (ax.semilogx(sizes,[max(r["state"] for r in dg if r["window"]==n) for n in sizes],"o-",label="Maximum mesuré"),
                      ax.semilogx(sizes,[2*n.bit_length() for n in sizes],"--",label="Borne")))
    for name, q, label in (("06_gk_mediane",.5,"Médiane"),("07_gk_p99",.99,"P99")):
        chart(name, f"{label} historique avec GK", "Valeur exacte (ms)", "Valeur estimée (ms)",
              lambda ax: parity(ax,[r for r in gk if r["q"]==q]))
    chart("08_gk_erreur", "Erreur de rang GK", "ε", "Erreur de rang / n",
          lambda ax: (ax.loglog([.001,.05],[.001,.05],"--",label="Borne"),
                      ax.scatter([r["eps"] for r in gk if r["error"]],[r["error"]/r["n"] for r in gk if r["error"]],alpha=.4)))
    def growth(ax):
        for eps in sorted({r["eps"] for r in gk}):
            ns = sorted({r["n"] for r in gk if r["eps"]==eps})
            ax.semilogx(ns,[max(r["state"] for r in gk if r["eps"]==eps and r["n"]==n) for n in ns],"o-",label=f"ε={eps}")
    chart("09_gk_taille", "Nombre maximal de tuples GK", "Observations", "Tuples", growth)
    memory = [r for r in rows if "peak_bytes" in r]
    chart("10_memoire", "Quantiles récents, pic tracemalloc", "Méthode, N=10 000", "Pic (Kio)",
          lambda ax: ax.bar([r["algorithm"] for r in memory],[r["peak_bytes"]/1024 for r in memory]))
    throughput = [r for r in rows if r["algorithm"] in ("Reservoir","WeightedReservoir") and r["n"]==10_000 and r["k"]==10]
    chart("11_debit", "Débit des réservoirs, n=10 000 et k=10", "Réservoir", "Événements/s",
          lambda ax: ax.scatter([r["algorithm"] for r in throughput],[1e9/r["update_ns"] for r in throughput]))
    def line(ax, key, label):
        ax.plot([r["t"] for r in timeline],[r[key] for r in timeline],label=label,linewidth=1)
    chart("12_scenario", "Latence simulée, incident et retour", "Événement", "Latence (ms)",
          lambda ax: line(ax,"latency","Mesure synthétique"))
    def alert(ax):
        line(ax,"p99","P99 récent")
        line(ax,"median","Médiane récente")
        ax.axhline(monitor.alerts.p99_limit,ls="--",label="Seuil P99")
        ax.axhline(monitor.alerts.median_limit,ls=":",label="Seuil médiane")
        for state, color in (("Alerte","red"),("Rétablissement","green")):
            first = next(r for r in timeline if r["state"]==state)
            ax.axvline(first["t"],color=color,alpha=.5,label=state)
    chart("13_alertes", "Déclenchement et rétablissement", "Événement", "Latence (ms)", alert)
    chart("14_historique_recent","P99 historique et récent","Événement","Latence (ms)",
          lambda ax: (line(ax,"historical","GK historique"),line(ax,"p99","Fenêtre approchée"),line(ax,"exact_p99","Fenêtre exacte")))
