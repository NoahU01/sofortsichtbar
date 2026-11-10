#!/usr/bin/env python3
"""PDF „Marketing as a Service“ – im Stil der empiria-Download-PDFs (Muster: werkzeuge/pdf2 im empiria-Repo).

Inhalt: story6.11tydata.json → maas (dieselbe Quelle wie die Seite /entwicklung/storyboard/story6/marketing-as-a-service/).
Bausteine: lib.py und _marketing_teile.py aus ~/Projekte/empiria/werkzeuge/pdf2 – nur gelesen, nicht verändert.

Aufruf:  python3 src/entwicklung/storyboard/story6/maas_pdf.py
Ergebnis: assets/maas/marketing-as-a-service.pdf (Angebot, Team, Stellenbeschreibungen, Postings),
          -1.png/-2.png (Vorschau im Download-Kasten),
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
from lib import titelseite, kopfbild, seite, kopf, kicker, punkte, dokument, ico  # noqa: E402
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
    "paid-ads": 'Paid Ads <span class="hl">mit Betreuung.</span>',
}
# Leistungen, die nicht mit Luft auf eine Seite passen, laufen auf einer zweiten Seite weiter (Index = erste Leistung der Folgeseite).
# Bausteine mit mehreren Leistungsgruppen (Paid Ads: Einrichtung · Betreuung) bekommen je Gruppe eine Seite.
TEILEN = {"kern": 3, "website": 5}


def leistung(l):
    rechts = (f'<p>{l["text"]}</p>' if l.get("text") else "") + (
        '<ul>' + "".join(f"<li>{x}</li>" for x in l["liste"]) + '</ul>' if l.get("liste") else "")
    return f'<div><h3>{l["titel"]}</h3><div>{rechts}</div></div>'


def teile_von(b):
    """[(label, leistungen), …] – eine Liste je Seite."""
    if len(b["gruppen"]) > 1:
        return [(g["label"], g["leistungen"]) for g in b["gruppen"]]
    g = b["gruppen"][0]
    if b["id"] in TEILEN:
        i = TEILEN[b["id"]]
        return [(g["label"], g["leistungen"][:i]), (None, g["leistungen"][i:])]
    return [(g["label"], g["leistungen"])]


def kapitel(b, nr, n):
    """Ein Baustein: Kicker · H2 · Einleitung · Preis-Fakten · Leistungsumfang (ggf. auf mehreren Seiten)."""
    teile = teile_von(b)
    fk = b.get("fakten") or [["Abrechnung", b["abrechnung"]], ["Investition", b["preis"]]]
    fakten = (f'<div class="fakten mfakten" style="grid-template-columns:repeat({len(fk)},1fr)">'
              + "".join(f'<div><span>{l}</span><b>{v}</b></div>' for l, v in fk) + '</div>')
    hinweis = (f'<div class="kasten mkasten"><p class="label">Gut zu wissen</p><p>{b["hinweis"]}</p></div>'
               if b.get("hinweis") else "")
    seiten = []
    for k, (label, teil) in enumerate(teile):
        letzte = k == len(teile) - 1
        if k == 0:
            kopfteil = (kicker(f'Baustein {b["nr"]} · {b["art"]}') + f'<h2>{H2[b["id"]]}</h2>'
                        + "".join(f'<p class="lead mlead">{p}</p>' for p in b["intro"]) + fakten
                        + f'<p class="mlabel">{label}</p>')
        else:
            kopfteil = kicker(f'Baustein {b["nr"]} · {b["name"]} · Fortsetzung') + (
                f'<p class="mlabel" style="margin-top:7mm">{label}</p>' if label else "")
        inhalt = (kopf(T) + '<div class="rand" style="padding-top:16mm">' + kopfteil
                  + '<div class="liste mliste">' + "".join(leistung(l) for l in teil) + '</div>'
                  + (hinweis if letzte else "") + '</div>')
        if letzte and b["id"] == "kern":   # Kernpaket: Ergebnis als gelbes Band unter dem Rest des Leistungsumfangs
            inhalt += ('<div class="band band--gelb wachsen mitte" style="margin-top:12mm">' + kicker("Das bekommst du")
                       + '<h2>Sichtbarkeit, die zu Anfragen führt.</h2>' + ERGEBNIS + '</div>')
        seiten.append(seite(inhalt, nr + k, n))
    return seiten


def team_seite(PR, nr, n):
    """Dein Team: vier Profile im Kernpaket, eines mit Paid Ads; darunter gelbes Band als Übergang zu den Stellenbeschreibungen."""
    def zeile(x):
        return (f'<div><div><h3>{x["klartext"]}</h3><span class="rolle-in">Gesucht als: {x["stelle"]}</span></div>'
                f'<div><p>{x["denkweise"]}</p></div></div>')
    gruppen = ""
    for g, label in (("kern", "Im Kernpaket"), ("paid-ads", "Mit Paid Ads")):
        gruppen += (f'<p class="mlabel">{label}</p><div class="liste mliste mliste--team">'
                    + "".join(zeile(x) for x in PR["liste"] if x["gruppe"] == g) + '</div>')
    return seite(
        kopf(T) + '<div class="rand" style="padding-top:16mm">' + kicker("Dein Team")
        + '<h2>Fünf Profile. <span class="hl">Ein Team.</span></h2>'
        + f'<p class="lead" style="max-width:155mm">{PR["lead"]}</p>' + gruppen
        + f'<p class="notiz">{PR["hinweis_ergaenzungen"]}</p></div>', nr, n)


def uebergang_seite(PR, nr, n):
    """Kapitelseite (gelb): Lieber selbst einstellen? – mit Verzeichnis der Stellenbeschreibungen und Postings."""
    eintraege = "".join(
        f'<div><h3>{x["stelle"]}</h3><p>Stellenbeschreibung · Seite {nr + 1 + i:02d}</p></div>' for i, x in enumerate(PR["liste"]))
    eintraege += f'<div><h3>Fünf fertige Postings</h3><p>Zum Veröffentlichen · ab Seite {nr + 1 + len(PR["liste"]):02d}</p></div>'
    return seite(
        kopf(T) + '<div class="rand wachsen mitte" style="padding-top:10mm">' + kicker("Lieber selbst einstellen?")
        + '<h2>Hier ist alles drin.</h2>'
        + '<p class="lead" style="max-width:150mm">Wir sind überzeugt, dass es einfacher ist, uns zu buchen. Wenn du die Profile lieber selbst '
          'besetzt, findest du hier fünf komplette Stellenbeschreibungen und fertige Postings für die Suche.</p>'
        + f'<div class="liste mliste mliste--verz">{eintraege}</div></div>', nr, n, klasse="seite--gelb")


def stellen_seite(x, nr, n):
    """Eine Stellenbeschreibung – Aufbau wie das empiria-Anforderungsprofil (drei Bereiche nebeneinander, Hinweis als schwarzer Kasten)."""
    bereiche = "".join(
        f'<div class="bereich">{ico(i)}<h3>{t}</h3><ul>{"".join(f"<li>{y}</li>" for y in items)}</ul></div>'
        for i, t, items in (("clipboard-list", "Aufgaben", x["aufgaben"]), ("target", "Anforderungen", x["anforderungen"]),
                            ("graduation-cap", "Ausbildung und Erfahrung", x["ausbildung"])))
    wo = "im Kernpaket" if x["gruppe"] == "kern" else "mit Paid Ads"
    return seite(
        kopf(T) + '<div class="rand" style="padding-top:16mm">' + kicker(f'Stellenbeschreibung {x["nr"]} · {x["klartext"]}')
        + f'<h2>{x["h2"]}</h2><p class="lead" style="max-width:160mm">{x["einleitung"]}</p>'
        + f'<div class="profil">{bereiche}</div>'
        + f'<div class="kasten mkasten"><p class="label">Bei Marketing as a Service</p><p>Dieses Profil ist {wo} bereits besetzt – '
          'eingearbeitet und im Team abgestimmt.</p></div></div>', nr, n)


def posting_seiten(PR, nr, n):
    """Fertige Stellen-Postings: Motiv im Kartenstil (gelb · schwarz · hell) plus Text; Platzhalter statt Logo."""
    def zeile(x):
        q = x["posting"]
        return (f'<div class="posting"><div class="motiv motiv--{q["farbe"]}"><small>Stellenanzeige</small>'
                f'<div><b>{q["titel"]}</b><span>{q["sub"]}</span></div><i>Dein Logo</i></div>'
                f'<div><p class="label">Posting {x["nr"]} · {x["klartext"]}</p><h3>{q["headline"]}</h3>'
                + "".join(f"<p>{y}</p>" for y in q["text"]) + '</div></div>')
    L = PR["liste"]
    teile = [L[:3], L[3:]]
    seiten = []
    for k, teil in enumerate(teile):
        kopfteil = (kicker("Fertige Postings") + '<h2>Fünf Stellenanzeigen <span class="hl">zum Veröffentlichen.</span></h2>'
                    + '<p class="lead" style="max-width:160mm">Für LinkedIn, die Karriereseite oder Social Media – Logo, Unternehmensname '
                      'und Kontakt einfach ergänzen.</p>') if k == 0 else kicker("Fertige Postings · Fortsetzung")
        seiten.append(seite(kopf(T) + '<div class="rand" style="padding-top:16mm">' + kopfteil
                            + '<div class="postings">' + "".join(zeile(x) for x in teil) + '</div></div>', nr + k, n))
    return seiten


CSS_TEAM = """
.mliste--verz { margin-top: 10mm; }
.mliste--verz > div { grid-template-columns: 1fr 60mm; align-items: baseline; border-color: rgba(26,24,23,.25); }
.mliste--verz p { color: #1a1817; text-align: right; }
.mliste--team > div { grid-template-columns: 70mm 1fr; }
.mliste--team p { font-size: 9pt; color: #1a1817; }
.rolle-in { display: block; margin-top: 1.2mm; font-size: 8pt; color: #8a847c; line-height: 1.4; }
.profil { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8mm; margin-top: 9mm; }
.bereich { border-top: 1.6px solid #1a1817; padding-top: 4.5mm; }
.bereich svg { width: 7mm; height: 7mm; margin-bottom: 3mm; }
.bereich h3 { font-size: 12.5pt; }
.bereich ul { list-style: none; margin-top: 2.5mm; }
.bereich li { position: relative; padding: 1.6mm 0 1.6mm 4mm; border-bottom: 1px solid #e4e0db; font-size: 8.8pt; line-height: 1.5; }
.bereich li:last-child { border-bottom: 0; }
.bereich li::before { content: ""; position: absolute; left: 0; top: 3.7mm; width: 1.4mm; height: 1.4mm; border-radius: 50%; background: #1a1817; }
.postings { margin-top: 7mm; }
.posting { display: grid; grid-template-columns: 52mm 1fr; gap: 8mm; align-items: center; padding: 5.5mm 0; border-top: 1px solid #dcd8d1; }
.posting:first-child { border-top: 1.6px solid #1a1817; }
.motiv { width: 52mm; height: 52mm; border-radius: 3.5mm; padding: 4.6mm; display: flex; flex-direction: column; justify-content: space-between; }
.motiv small { font-size: 5.6pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
.motiv b { display: block; font-family: 'Lora', Georgia, serif; font-size: 12pt; line-height: 1.15; }
.motiv span { display: block; margin-top: 2mm; font-size: 6.4pt; line-height: 1.4; }
.motiv i { align-self: flex-start; font-style: normal; font-size: 5.8pt; font-weight: 600; padding: .8mm 2mm; border: 1px dashed currentColor; border-radius: 1.2mm; }
.motiv--gelb { background: #fff400; color: #1a1817; }
.motiv--schwarz { background: #1a1817; color: #fff; }
.motiv--hell { background: #f3f1ee; color: #1a1817; }
.posting .label { font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
.posting h3 { margin-top: 2mm; font-size: 12pt; }
.posting p:not(.label) { margin-top: 2mm; font-size: 8.8pt; line-height: 1.6; color: #3d3a37; }
"""


def bauen(M):
    B = M["bausteine"]
    PR = M["profile"]
    n = 3 + sum(len(teile_von(b)) for b in B) + 2 + len(PR["liste"]) + 2

    s1 = seite(titelseite(
        "Angebot", 'Marketing<br><span class="hl">as a Service.</span>', M["lead"], kopfbild("MarketingEcoSystem (MES)"),
        [("Bausteine", "Kern und Ergänzungen"), ("Team", "Fünf Profile"), ("Zum Selbermachen", "Stellenprofile"), ("Investition", "ab 1.800 € mtl.")]))

    zeilen = "".join(
        f'<div class="ue{" ue--kern" if b["id"] == "kern" else ""}"><span class="ue__nr">{b["nr"]}</span>'
        f'<div><small>{b["art"]}</small><h3>{b["name"]}</h3><p>{b["kurz"]}</p></div>'
        f'<b class="ue__preis">{b["preis"]}<span>{b["abrechnung"]}</span>'
        f'{"<span>" + b["zusatz"] + "</span>" if b.get("zusatz") else ""}</b></div>'
        for b in B)
    s2 = seite(
        kopf(T) + '<div class="rand" style="padding-top:16mm">' + kicker("Die Bausteine")
        + '<h2>Ein Kernpaket. <span class="hl">Drei Ergänzungen.</span></h2>'
        + '<p class="lead" style="max-width:150mm">Das Kernpaket „sofort sichtbar“ ist die Basis der Zusammenarbeit. '
          'Die Ergänzungen buchst du dazu, wenn du sie brauchst.</p>'
        + f'<div class="uebersicht">{zeilen}</div>'
        + f'<p class="notiz">{M["hinweis_preise"]} Paid Ads je Werbekanal, Werbebudget nicht enthalten.</p></div>', 2, n)

    seiten, nr = [s1, s2], 3
    for b in B:
        k = kapitel(b, nr, n)
        seiten += k
        nr += len(k)
    seiten.append(team_seite(PR, nr, n))
    nr += 1
    seiten.append(uebergang_seite(PR, nr, n))
    nr += 1
    for x in PR["liste"]:
        seiten.append(stellen_seite(x, nr, n))
        nr += 1
    p = posting_seiten(PR, nr, n)
    seiten += p
    nr += len(p)

    extra = '<div>' + mt.ico("app-window") + 'sofortsichtbar.de</div>'
    seiten.append(seite(
        kopf(T) + '<div class="rand weiss" style="padding-top:16mm">'
        + mt.schritte('Oder du buchst <span class="hl">das Team.</span>',
                      "Ohne Suche, ohne Einarbeitung, ohne Ausfallrisiko: Wir klären, welche Bausteine zu deinen Zielen passen, und melden uns zeitnah mit einem konkreten Vorschlag.")
        + '</div>' + mt.draht(extra), nr, n))
    return dokument(f"{T} – sofort sichtbar", seiten, extra_css=mt.CSS + CSS + CSS_TEAM)


ERGEBNIS = punkte([
    ("target", "Qualifizierte Anfragen", "Deine Sichtbarkeit übersetzt sich verlässlich in qualifizierte Anfragen."),
    ("layout-dashboard", "Jederzeit Überblick", "Alle Anfragen, Kampagnen und Kennzahlen laufen in einem zentralen Dashboard zusammen."),
    ("user-round", "Fester Ansprechpartner", "Wir übernehmen die operative Umsetzung – mit dir besprechen wir Ergebnisse und Prioritäten.")])

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
.ue { display: grid; grid-template-columns: 10mm 1fr 52mm; gap: 4mm; align-items: start; padding: 3.6mm 3mm; border-bottom: 1px solid #dcd8d1; }
.ue--kern { background: #fff400; border-bottom-color: #fff400; border-radius: 0 0 3mm 3mm; }
.ue__nr { font-size: 7pt; font-weight: 700; letter-spacing: .16em; padding-top: .8mm; }
.ue small { display: block; font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
.ue h3 { font-size: 11.5pt; margin-top: .8mm; }
.ue p { margin-top: 1mm; font-size: 8.4pt; line-height: 1.45; color: #3d3a37; }
.ue--kern p { color: #1a1817; }
.ue__preis { text-align: right; font-family: 'Lora', Georgia, serif; font-size: 13pt; padding-top: 3.6mm; white-space: nowrap; }
.ue__preis span + span { margin-top: .4mm; }
.ue__preis span { display: block; margin-top: .8mm; font-family: 'Poppins', Arial, sans-serif; font-weight: 400; font-size: 8pt; }
"""


def drucken(html, datei, praefix, meta):
    """HTML → PDF, Seitenbilder, Vorschau -1/-2; trägt Seitenzahl und Größe in meta ein."""
    src = os.path.join(BUILD, praefix + ".html")
    open(src, "w", encoding="utf-8").write(html)
    pdf = os.path.join(ZIEL, datei)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    "--virtual-time-budget=8000", "file://" + src], capture_output=True, timeout=180)
    seiten_dir = os.path.join(BUILD, praefix + "-seiten")
    shutil.rmtree(seiten_dir, ignore_errors=True)
    r = subprocess.run(["node", os.path.join(PDF2, "seiten.mjs"), src, seiten_dir, os.path.join(ZIEL, praefix)],
                       check=True, capture_output=True, text=True)
    for i in (1, 2):   # Vorschaubilder für den Download-Kasten verkleinern
        subprocess.run(["sips", "-Z", "900", os.path.join(ZIEL, f"{praefix}-{i}.png")], capture_output=True)
    kb = os.path.getsize(pdf) / 1024
    meta["seiten"] = int(re.match(r"(\d+)", r.stdout).group(1))
    meta["groesse"] = (f"{kb / 1024:.1f} MB" if kb >= 100 else f"{kb:.0f} KB").replace(".", ",")
    print(f"{r.stdout.strip()}\n{pdf}  ({meta['seiten']} Seiten, {meta['groesse']})\nSeitenbilder: {seiten_dir}")


def main():
    d = json.load(open(DATEN, encoding="utf-8"))
    M = d["maas"]
    os.makedirs(BUILD, exist_ok=True)
    link = os.path.join(BUILD, "assets")
    if not os.path.exists(link):
        os.symlink(os.path.join(EMPIRIA, "site", "assets"), link)
    drucken(bauen(M), M["pdf"]["datei"], "marketing-as-a-service", M["pdf"])
    json.dump(d, open(DATEN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(DATEN, "a").write("\n")


if __name__ == "__main__":
    main()
