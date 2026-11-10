#!/usr/bin/env python3
"""PDF „Marketing as a Service“ – im Stil der empiria-Download-PDFs (Muster: werkzeuge/pdf2 im empiria-Repo).

Inhalt: story6.11tydata.json → maas (dieselbe Quelle wie die Seite /entwicklung/storyboard/story6/marketing-as-a-service/).
Bausteine: lib.py und _marketing_teile.py aus ~/Projekte/empiria/werkzeuge/pdf2 – nur gelesen, nicht verändert.

Aufruf:  python3 src/entwicklung/storyboard/story6/maas_pdf.py
Ergebnis: assets/maas/marketing-as-a-service.pdf, -1.png/-2.png (Vorschau im Download-Kasten),
          Seitenbilder zum Prüfen im Temp-Ordner maas_pdf_build/seiten/ (Pfad wird ausgegeben), Seitenzahl/Größe zurück in die JSON.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMPIRIA = os.path.expanduser("~/Projekte/empiria")
PDF2 = os.path.join(EMPIRIA, "werkzeuge", "pdf2")
sys.path.insert(0, PDF2)
from lib import titelseite, kopfbild, seite, kopf, kicker, punkte, dokument  # noqa: E402
import _marketing_teile as mt  # noqa: E402

DATEN = os.path.join(HERE, "story6.11tydata.json")
ZIEL = os.path.join(HERE, "assets", "maas")
BUILD = os.path.join(tempfile.gettempdir(), "maas_pdf_build")   # Arbeitsordner außerhalb des Repos (enthält einen Verweis auf empiria/site/assets)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
T = "Marketing as a Service"

# Überschriften der Kapitel – je eine Hervorhebung, nie über zwei Zeilen
H2 = {
    "kern": 'Kernpaket <span class="hl">sofort sichtbar.</span>',
    "linkedin": 'LinkedIn <span class="hl">Power Package.</span>',
    "website": 'Website-<span class="hl">Entwicklung.</span>',
    "ads-einrichtung": 'Paid Ads <span class="hl">Einrichtung.</span>',
    "ads-betreuung": 'Paid Ads <span class="hl">Betreuung.</span>',
}
# Leistungen, die nicht mit Luft auf eine Seite passen, laufen auf einer zweiten Seite weiter (Index = erste Leistung der Folgeseite)
TEILEN = {"kern": 3, "website": 5}


def leistung(l):
    rechts = (f'<p>{l["text"]}</p>' if l.get("text") else "") + (
        '<ul>' + "".join(f"<li>{x}</li>" for x in l["liste"]) + '</ul>' if l.get("liste") else "")
    return f'<div><h3>{l["titel"]}</h3><div>{rechts}</div></div>'


def kapitel(b, nr, n):
    """Ein Baustein: Kicker · H2 · Einleitung · Abrechnung/Investition · Leistungsumfang (ggf. auf zwei Seiten)."""
    teile = [b["leistungen"]]
    if b["id"] in TEILEN:
        i = TEILEN[b["id"]]
        teile = [b["leistungen"][:i], b["leistungen"][i:]]
    fakten = (f'<div class="fakten mfakten"><div><span>Abrechnung</span><b>{b["abrechnung"]}</b></div>'
              f'<div><span>Investition</span><b>{b["preis"]}</b></div></div>')
    hinweis = (f'<div class="kasten mkasten"><p class="label">Gut zu wissen</p><p>{b["hinweis"]}</p></div>'
               if b.get("hinweis") else "")
    seiten = []
    for k, teil in enumerate(teile):
        letzte = k == len(teile) - 1
        if k == 0:
            kopfteil = (kicker(f'Baustein {b["nr"]} · {b["art"]}') + f'<h2>{H2[b["id"]]}</h2>'
                        + "".join(f'<p class="lead mlead">{p}</p>' for p in b["intro"]) + fakten
                        + '<p class="mlabel">Leistungsumfang</p>')
        else:
            kopfteil = kicker(f'Baustein {b["nr"]} · {b["name"]} · Fortsetzung')
        inhalt = (kopf(T) + '<div class="rand" style="padding-top:16mm">' + kopfteil
                  + '<div class="liste mliste">' + "".join(leistung(l) for l in teil) + '</div>'
                  + (hinweis if letzte else "") + '</div>')
        if letzte and b["id"] == "kern":   # Kernpaket: Ergebnis als gelbes Band unter dem Rest des Leistungsumfangs
            inhalt += ('<div class="band band--gelb wachsen mitte" style="margin-top:12mm">' + kicker("Das bekommen Sie")
                       + '<h2>Sichtbarkeit, die zu Anfragen führt.</h2>' + ERGEBNIS + '</div>')
        seiten.append(seite(inhalt, nr + k, n))
    return seiten


def bauen(M):
    B = M["bausteine"]
    n = 3 + sum(2 if b["id"] in TEILEN else 1 for b in B)

    s1 = seite(titelseite(
        "Angebot", 'Marketing<br><span class="hl">as a Service.</span>', M["lead"], kopfbild("MarketingEcoSystem (MES)"),
        [("Betreuung", "Laufend"), ("Steuerung", "Zentrales Dashboard"), ("Aufbau", "Kern und Ergänzungen"), ("Investition", "ab 1.800 € mtl.")]))

    zeilen = "".join(
        f'<div class="ue{" ue--kern" if b["id"] == "kern" else ""}"><span class="ue__nr">{b["nr"]}</span>'
        f'<div><small>{b["art"]}</small><h3>{b["name"]}</h3><p>{b["kurz"]}</p></div>'
        f'<b class="ue__preis">{b["preis"]}<span>{b["abrechnung"]}</span></b></div>'
        for b in B)
    s2 = seite(
        kopf(T) + '<div class="rand" style="padding-top:16mm">' + kicker("Die Bausteine")
        + '<h2>Ein Kernpaket. <span class="hl">Vier Ergänzungen.</span></h2>'
        + '<p class="lead" style="max-width:150mm">Das Kernpaket „sofort sichtbar“ ist die Basis der Zusammenarbeit. '
          'Die Ergänzungen buchen Sie dazu, wenn Sie sie brauchen.</p>'
        + f'<div class="uebersicht">{zeilen}</div>'
        + f'<p class="notiz">{M["hinweis_preise"]} Paid Ads je Werbekanal, Werbebudget nicht enthalten.</p></div>', 2, n)

    seiten, nr = [s1, s2], 3
    for b in B:
        k = kapitel(b, nr, n)
        seiten += k
        nr += len(k)

    extra = '<div>' + mt.ico("app-window") + 'sofortsichtbar.de</div>'
    seiten.append(seite(
        kopf(T) + '<div class="rand weiss" style="padding-top:16mm">'
        + mt.schritte('Lassen Sie uns <span class="hl">sprechen.</span>',
                      "Wir klären, welche Bausteine zu Ihren Zielen passen, und melden uns zeitnah mit einem konkreten Vorschlag.")
        + '</div>' + mt.draht(extra).replace("Dein direkter Draht", "Ihr direkter Draht"), nr, n))
    return dokument(f"{T} – sofort sichtbar", seiten, extra_css=mt.CSS + CSS)


ERGEBNIS = punkte([
    ("target", "Qualifizierte Anfragen", "Ihre Sichtbarkeit übersetzt sich verlässlich in qualifizierte Anfragen."),
    ("layout-dashboard", "Jederzeit Überblick", "Alle Anfragen, Kampagnen und Kennzahlen laufen in einem zentralen Dashboard zusammen."),
    ("user-round", "Fester Ansprechpartner", "Wir übernehmen die operative Umsetzung – mit Ihnen besprechen wir Ergebnisse und Prioritäten.")])

CSS = """
.mlead { max-width: 160mm; margin-top: 3.5mm; }
.mlead + .mlead { margin-top: 2.5mm; }
.mfakten { margin: 7mm 0 0; grid-template-columns: 1fr 1fr; }
.mfakten em { font-style: normal; }
.mlabel { margin-top: 9mm; font-size: 7.6pt; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; }
.mliste { margin-top: 3mm; }
.mliste > div { grid-template-columns: 56mm 1fr; }
.mliste h3 { font-size: 11pt; }
.mliste p + ul { margin-top: 1.6mm; }
.mliste ul { list-style: none; }
.mliste li { position: relative; padding-left: 3.6mm; margin-top: 1mm; font-size: 8.8pt; line-height: 1.5; color: #3d3a37; }
.mliste li:first-child { margin-top: 0; }
.mliste li::before { content: ""; position: absolute; left: 0; top: 1.9mm; width: 1.3mm; height: 1.3mm; border-radius: 50%; background: #1a1817; }
.mkasten { margin-top: 7mm; padding: 5mm 7mm 5.5mm; }
.mkasten p:not(.label) { margin-top: 1.6mm; }
.team3 .kontaktdaten { display: grid; grid-template-columns: 1fr 1fr; }   /* vier Kontakt-Pillen wie im PDF „sofort sichtbar“: zwei Spalten */
.weiss .zs .punkt { box-shadow: 0 0 0 1.2mm #fff; }
.uebersicht { margin-top: 7mm; border-top: 1.6px solid #1a1817; }
.ue { display: grid; grid-template-columns: 10mm 1fr 40mm; gap: 4mm; align-items: start; padding: 3.6mm 3mm; border-bottom: 1px solid #dcd8d1; }
.ue--kern { background: #fff400; border-bottom-color: #fff400; border-radius: 0 0 3mm 3mm; }
.ue__nr { font-size: 7pt; font-weight: 700; letter-spacing: .16em; padding-top: .8mm; }
.ue small { display: block; font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
.ue h3 { font-size: 11.5pt; margin-top: .8mm; }
.ue p { margin-top: 1mm; font-size: 8.4pt; line-height: 1.45; color: #3d3a37; }
.ue--kern p { color: #1a1817; }
.ue__preis { text-align: right; font-family: 'Lora', Georgia, serif; font-size: 13pt; padding-top: 3.6mm; white-space: nowrap; }
.ue__preis span { display: block; margin-top: .8mm; font-family: 'Poppins', Arial, sans-serif; font-weight: 400; font-size: 8pt; }
"""


def main():
    d = json.load(open(DATEN, encoding="utf-8"))
    M = d["maas"]
    os.makedirs(BUILD, exist_ok=True)
    link = os.path.join(BUILD, "assets")
    if not os.path.exists(link):
        os.symlink(os.path.join(EMPIRIA, "site", "assets"), link)
    src = os.path.join(BUILD, "marketing-as-a-service.html")
    open(src, "w", encoding="utf-8").write(bauen(M))
    pdf = os.path.join(ZIEL, M["pdf"]["datei"])
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    "--virtual-time-budget=8000", "file://" + src], capture_output=True, timeout=180)
    seiten_dir = os.path.join(BUILD, "seiten")
    shutil.rmtree(seiten_dir, ignore_errors=True)
    r = subprocess.run(["node", os.path.join(PDF2, "seiten.mjs"), src, seiten_dir,
                        os.path.join(ZIEL, "marketing-as-a-service")], check=True, capture_output=True, text=True)
    print(r.stdout.strip())
    # Vorschaubilder für den Download-Kasten verkleinern (1588 px Breite reicht nicht als Original im Repo)
    for i in (1, 2):
        png = os.path.join(ZIEL, f"marketing-as-a-service-{i}.png")
        subprocess.run(["sips", "-Z", "900", png], capture_output=True)
    anzahl = int(re.match(r"(\d+)", r.stdout).group(1))
    kb = os.path.getsize(pdf) / 1024
    M["pdf"]["seiten"] = anzahl
    M["pdf"]["groesse"] = (f"{kb / 1024:.1f} MB" if kb >= 100 else f"{kb:.0f} KB").replace(".", ",")
    json.dump(d, open(DATEN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(DATEN, "a").write("\n")
    print(f"{pdf}  ({anzahl} Seiten, {M['pdf']['groesse']})\nSeitenbilder: {seiten_dir}")


if __name__ == "__main__":
    main()
