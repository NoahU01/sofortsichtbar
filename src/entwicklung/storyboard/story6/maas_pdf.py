#!/usr/bin/env python3
"""PDF „Marketing as a Service“ – im Stil der empiria-Download-PDFs (Muster: werkzeuge/pdf2 im empiria-Repo).

Inhalt: story6.11tydata.json → maas (dieselbe Quelle wie die Seite /entwicklung/storyboard/story6/marketing-as-a-service/).
Bausteine: lib.py und _marketing_teile.py aus ~/Projekte/empiria/werkzeuge/pdf2 – nur gelesen, nicht verändert.

Aufruf:  python3 src/entwicklung/storyboard/story6/maas_pdf.py
Ergebnis: assets/maas/marketing-as-a-service.pdf und marketing-as-a-service-team.pdf (Teamvergleich),
          je -1.png/-2.png (Vorschau im Download-Kasten),
          Seitenbilder zum Prüfen im Temp-Ordner maas_pdf_build/seiten/ (Pfad wird ausgegeben), Seitenzahl/Größe und die berechneten Teamkosten zurück in die JSON.
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


def bauen(M):
    B = M["bausteine"]
    n = 3 + sum(len(teile_von(b)) for b in B)

    s1 = seite(titelseite(
        "Angebot", 'Marketing<br><span class="hl">as a Service.</span>', M["lead"], kopfbild("MarketingEcoSystem (MES)"),
        [("Betreuung", "Laufend"), ("Steuerung", "Zentrales Dashboard"), ("Aufbau", "Kern und Ergänzungen"), ("Investition", "ab 1.800 € mtl.")]))

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

    extra = '<div>' + mt.ico("app-window") + 'sofortsichtbar.de</div>'
    seiten.append(seite(
        kopf(T) + '<div class="rand weiss" style="padding-top:16mm">'
        + mt.schritte('Lass uns <span class="hl">sprechen.</span>',
                      "Wir klären, welche Bausteine zu deinen Zielen passen, und melden uns zeitnah mit einem konkreten Vorschlag.")
        + '</div>' + mt.draht(extra), nr, n))
    return dokument(f"{T} – sofort sichtbar", seiten, extra_css=mt.CSS + CSS)


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


def euro(x):
    return f"{x:,.0f} €".replace(",", ".")


def team_rechnen(M):
    """Arbeitgeberkosten je Rolle (Gehalt × (1 + AG-Anteil) / 12, auf 10 € gerundet) und die Summe (auf 100 € gerundet)."""
    tm = M["team"]
    summe = 0
    for r in tm["rollen"]:
        k = r["gehalt_jahr"] * (1 + tm["ag_anteil"]) / 12
        summe += k
        r["gehalt_text"] = euro(r["gehalt_jahr"])
        r["kosten_monat"] = euro(round(k, -1))
    tm["summe_monat"] = euro(round(summe, -2))
    tm["ag_prozent"] = f'{tm["ag_anteil"] * 100:.0f} %'


def bauen_team(M):
    tm = M["team"]
    R = tm["rollen"]
    T2 = "Dein Marketing-Team"
    n = 4
    s1 = seite(titelseite(
        "Marketing as a Service", 'Vier Fachleute.<br><span class="hl">Ein Team.</span>',
        "Hinter den Bausteinen von Marketing as a Service stehen vier Fachleute, die für deine Themen verantwortlich sind. "
        "Du buchst das Team – statt vier Stellen zu besetzen.",
        kopfbild("sofort sichtbar"),
        [("Team", "Vier Fachleute"), ("Selbst eingestellt", f'rund {tm["summe_monat"]} mtl.'), ("Mit uns", f'{tm["maas_monat"]} mtl.')]))

    zeilen = "".join(
        f'<div><div><h3>{r["rolle"]}</h3><span class="rolle-in">{r["bausteine"]}</span></div>'
        f'<div><ul>{"".join(f"<li>{x}</li>" for x in r["aufgaben"])}</ul></div></div>' for r in R)
    s2 = seite(
        kopf(T2) + '<div class="rand" style="padding-top:16mm">' + kicker("Wer für dich arbeitet")
        + '<h2>Vier Rollen. <span class="hl">Klar verantwortlich.</span></h2>'
        + '<p class="lead" style="max-width:150mm">Jede Rolle steht für einen Teil der Leistungen. Zusammen decken sie alles ab, '
          'was in den Bausteinen steckt – von der Landingpage bis zur Anzeige.</p>'
        + f'<div class="liste mliste">{zeilen}</div></div>', 2, n)

    tab = "".join(f'<tr><td>{r["rolle"]}</td><td class="r">{r["gehalt_text"]}</td><td class="r"><b>{r["kosten_monat"]}</b></td></tr>' for r in R)
    tab = (f'<table class="vgl"><thead><tr><th>Rolle in Vollzeit</th><th class="r">Gehalt im Jahr</th><th class="r">Kosten im Monat</th></tr></thead>'
           f'<tbody>{tab}</tbody></table>')
    gegen = (f'<div class="gegen"><div><span>Selbst eingestellt</span><b>rund {tm["summe_monat"]}</b><small>im Monat, vier Vollzeitstellen</small></div>'
             f'<div class="gegen--gelb"><span>Mit uns</span><b>{tm["maas_monat"]}</b><small>im Monat: {tm["maas_erklaerung"]}</small></div></div>')
    kasten = ('<div class="kasten mkasten"><p class="label">Beim Einstellen kommen dazu</p><ul class="zk">'
              + "".join(f"<li>{x}</li>" for x in tm["zusatzkosten"]) + '</ul></div>')
    quellen = ("Gehälter: StepStone-Durchschnitt brutto, abgerufen am 10.11.2026. Kosten im Monat = Gehalt plus rund "
               f'{tm["ag_prozent"]} Arbeitgeberanteil zur Sozialversicherung, geteilt durch zwölf. '
               "Einmalige Leistungen (Website, Einrichtung Paid Ads) sind nicht eingerechnet. Alle Preise zzgl. Umsatzsteuer.")
    s3 = seite(
        kopf(T2) + '<div class="rand" style="padding-top:16mm">' + kicker("Der Vergleich")
        + '<h2>Weniger als <span class="hl">eine Stelle.</span></h2>'
        + '<p class="lead" style="max-width:150mm">Schon eine einzige Vollzeitkraft kostet mehr als alle laufenden Bausteine zusammen.</p>'
        + tab + gegen + kasten + f'<p class="notiz">{quellen}</p></div>', 3, n)

    extra = '<div>' + mt.ico("app-window") + 'sofortsichtbar.de</div>'
    s4 = seite(
        kopf(T2) + '<div class="rand weiss" style="padding-top:16mm">'
        + mt.schritte('Lass uns <span class="hl">sprechen.</span>',
                      "Wir klären, welche Bausteine zu deinen Zielen passen, und melden uns zeitnah mit einem konkreten Vorschlag.")
        + '</div>' + mt.draht(extra), 4, n)
    return dokument(f"{T2} – Marketing as a Service", [s1, s2, s3, s4], extra_css=mt.CSS + CSS + CSS_TEAM)


CSS_TEAM = """
.vgl { width: 100%; border-collapse: collapse; margin-top: 8mm; font-size: 9pt; }
.vgl th { padding: 0 0 2.6mm; text-align: left; font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; border-bottom: 1.6px solid #1a1817; }
.vgl td { padding: 3mm 0; border-bottom: 1px solid #dcd8d1; }
.vgl .r { text-align: right; }
.vgl td b { font-weight: 600; }
.vgl tfoot td { padding-top: 3.4mm; font-weight: 700; border-bottom: 0; }
.gegen { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; margin-top: 8mm; }
.gegen > div { padding: 5mm 6mm 5.5mm; border-radius: 4.5mm; background: #f3f1ee; }
.gegen > div.gegen--gelb { background: #fff400; }
.gegen span { display: block; font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
.gegen b { display: block; margin-top: 2mm; font-family: 'Poppins', Arial, sans-serif; font-weight: 700; font-size: 22pt; line-height: 1.1; }
.gegen small { display: block; margin-top: 1.6mm; font-size: 8pt; line-height: 1.45; }
.zk { list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 1.6mm 8mm; margin-top: 3mm; }
.zk li { position: relative; padding-left: 3.6mm; font-size: 9pt; color: rgba(255,255,255,.85); }
.zk li::before { content: ""; position: absolute; left: 0; top: 2mm; width: 1.3mm; height: 1.3mm; border-radius: 50%; background: #fff400; }
.rolle-in { display: block; margin-top: 1.2mm; font-size: 8pt; color: #8a847c; line-height: 1.4; }
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
    team_rechnen(M)
    os.makedirs(BUILD, exist_ok=True)
    link = os.path.join(BUILD, "assets")
    if not os.path.exists(link):
        os.symlink(os.path.join(EMPIRIA, "site", "assets"), link)
    drucken(bauen(M), M["pdf"]["datei"], "marketing-as-a-service", M["pdf"])
    drucken(bauen_team(M), M["pdf_team"]["datei"], "marketing-as-a-service-team", M["pdf_team"])
    json.dump(d, open(DATEN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(DATEN, "a").write("\n")


if __name__ == "__main__":
    main()
