"""Run against a local Streamlit server with Playwright and Chrome."""
import argparse
import csv
import io
import json
from pathlib import Path
import re
import time

from playwright.sync_api import expect, sync_playwright


def run(url, output, executable):
    output.mkdir(parents=True, exist_ok=True)
    screenshots = Path("presentation/screenshots")
    screenshots.mkdir(parents=True, exist_ok=True)
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=executable)
        page = browser.new_page(viewport={"width": 1440, "height": 1050}, accept_downloads=True)
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.goto(url)
        expect(page.get_by_role("heading", name="Stream Analytics Lab")).to_be_visible()

        def button(name):
            return page.get_by_role("button", name=name, exact=True)

        def at(n, total=1200):
            expect(page.get_by_text(f"{n} / {total} événements", exact=True)).to_be_visible()

        def count():
            text = page.get_by_text(re.compile(r"^\d+ / \d+ événements$")).inner_text()
            return int(text.split()[0])

        button("Avancer d’un événement").click()
        at(1)
        expect(page.get_by_test_id("stVegaLiteChart")).to_be_visible(timeout=15_000)
        button("Avancer d’un lot").click()
        at(51)
        cadence = []
        for _ in range(2):
            start = count()
            clock = time.monotonic()
            button("Démarrer").click()
            expect(button("Avancer d’un événement")).to_be_disabled()
            expect(button("Avancer d’un lot")).to_be_disabled()
            page.wait_for_function(
                "(n) => Array.from(document.querySelectorAll('p')).some(p => p.innerText === n)",
                arg=f"{start+100} / 1200 événements",
            )
            cadence.append(round(time.monotonic()-clock, 3))
            button("Pause").click()
            expect(button("Démarrer")).to_be_enabled()
            paused = count()
            assert (paused-start) % 50 == 0
            page.wait_for_timeout(1400)
            at(paused)

        button("Simuler un incident").click()
        button("Avancer d’un lot").click()
        expect(page.get_by_test_id("stMetricValue").filter(has_text="Alerte")).to_be_visible()
        expect(page.get_by_test_id("stVegaLiteChart")).to_be_visible()
        page.screenshot(path=str(screenshots/"alerte.png"))
        for tab in ("Réservoir uniforme", "A-Res", "DGIM", "Quantiles", "Surveillance"):
            page.get_by_role("tab", name=tab, exact=True).click()
            expect(page.get_by_role("tab", name=tab, exact=True)).to_have_attribute("aria-selected", "true")
        button("Revenir à la normale").click()
        for _ in range(5):
            before = count()
            button("Avancer d’un lot").click()
            at(before + 50)
        expect(page.get_by_test_id("stMetricValue").filter(has_text="Normal")).to_be_visible()
        page.screenshot(path=str(screenshots/"retour.png"))
        last = count()
        with page.expect_download() as download_info:
            button("Exporter les 500 dernières observations").click()
        download = download_info.value
        data = download.path().read_text(encoding="utf-8")
        rows = list(csv.DictReader(io.StringIO(data)))
        assert download.suggested_filename == "latences.csv"
        assert [int(row["t"]) for row in rows] == list(range(max(1, last-499), last+1))
        assert rows[-1]["state"] == "Normal"
        assert abs(float(rows[-1]["p99"]) - float(
            page.get_by_test_id("stMetricValue").nth(3).inner_text().split()[0]
        )) <= .051
        at(last)
        (output/"latences.csv").write_text(data, encoding="utf-8")
        oracle = page.get_by_role("checkbox", name="Activer les oracles exacts (mémoire supplémentaire)")
        expect(oracle).to_be_checked()
        oracle.press("Space")
        expect(oracle).not_to_be_checked()
        page.get_by_role("spinbutton", name="Taille de fenêtre N").fill("100")
        button("Appliquer et réinitialiser").click()
        expect(page.get_by_text("Démarrez le flux", exact=False)).to_be_visible()
        expect(page.get_by_text("Mode résumés seuls", exact=False)).to_be_visible()
        button("Avancer d’un événement").click()
        at(1)
        expect(page.get_by_test_id("stMetricValue").first).to_have_text("100")
        page.get_by_role("tab", name="Quantiles", exact=True).click()
        expect(page.get_by_text("budget effectif", exact=False)).to_be_visible()
        expect(page.get_by_text("positions périmées", exact=False)).to_be_visible()
        button("Réinitialiser").click()
        expect(page.get_by_text("Démarrez le flux", exact=False)).to_be_visible()
        assert not page.get_by_test_id("stException").count()
        assert not errors, errors
        version = browser.version
        browser.close()
    (output/"report.json").write_text(json.dumps({
        "status": "passed", "browser": version, "url": url, "timer_config_seconds": .6,
        "two_batch_elapsed_seconds": cadence, "paused_observation_seconds": 1.4,
        "download_rows": len(rows), "download_last_event": last,
        "manual_controls_disabled_during_playback": True,
        "download_without_advancing": True,
        "oracle_disabled_and_rank_budget_visible": True,
        "console_errors": errors,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:18765")
    parser.add_argument("--chrome", default="/usr/bin/google-chrome")
    parser.add_argument("--output", type=Path, default=Path("results/browser_validation"))
    args = parser.parse_args()
    run(args.url, args.output, args.chrome)
