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
sys.path.insert(0, HERE)
import maas_strukturbild  # noqa: E402

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
TEILEN = {"kern": [2], "website": [5], "paid-ads": [4]}


def leistung(l):
    rechts = (f'<p>{l["text"]}</p>' if l.get("text") else "") + (
        '<ul>' + "".join(f"<li>{x}</li>" for x in l["liste"]) + '</ul>' if l.get("liste") else "")
    return f'<div><h3>{l["titel"]}</h3><div>{rechts}</div></div>'


def teile_von(b):
    """Seiten eines Kapitels: [[(label|None, leistungen), …], …]. Umbruch an den Leistungs-Indizes aus TEILEN (über alle Gruppen gezählt).
    label steht nur dort, wo eine Gruppe beginnt."""
    brueche = set(TEILEN.get(b["id"], []))
    seiten, akt, i = [], [], 0
    for g in b["gruppen"]:
        seg = [g["label"], []]
        for l in g["leistungen"]:
            if i in brueche and (seg[1] or akt):
                if seg[1]:
                    akt.append(tuple(seg))
                seiten.append(akt)
                akt, seg = [], [None, []]
            seg[1].append(l)
            i += 1
        akt.append(tuple(seg))
    seiten.append(akt)
    return seiten


def kapitel(b, nr, n):
    """Ein Baustein: Kicker · H2 · Einleitung · Preis-Fakten · Leistungsumfang (ggf. auf mehreren Seiten)."""
    teile = teile_von(b)
    einheit = "einmalig" if b["einheit"] != "mtl." else ("pro Monat und Kanal" if "Kanal" in b["abrechnung"] else "pro Monat")
    zusatz = f'<span class="kz__zusatz">{b["zusatz"]}</span>' if b.get("zusatz") else ""
    haken = "".join(f"<li>{x}</li>" for x in b["punkte"])
    fakten = (f'<div class="kz"><div class="kz__ico">{ico(b["ico"], strich=1.3)}</div>'
              f'<div class="kz__preis"><span class="kz__label">Investition</span><b>{b["preis"]}</b><span>{einheit}</span>{zusatz}</div>'
              f'<div class="kz__haken"><span class="kz__label">Das Wichtigste</span><ul>{haken}</ul></div>'
              + (f'<p class="kz__hinweis"><b>Gut zu wissen:</b> {b["hinweis"]}</p>' if b.get("hinweis") and len(teile) == 1 else "") + '</div>')
    # „Gut zu wissen“: bei einseitigen Kapiteln in der Kennzeile, sonst als ruhiger Kasten am Ende des Kapitels
    hinweis = (f'<div class="kz kz--fuss"><p class="kz__hinweis"><b>Gut zu wissen:</b> {b["hinweis"]}</p></div>'
               if b.get("hinweis") and len(teile) > 1 else "")
    seiten = []
    for k, segmente in enumerate(teile):
        letzte = k == len(teile) - 1
        if k == 0:
            kopfteil = (kicker(f'Baustein {b["nr"]} · {b["art"]}') + f'<h2>{H2[b["id"]]}</h2>' + fakten
                        + "".join(f'<p class="lead mlead">{p}</p>' for p in b["intro"]))
        else:
            kopfteil = kicker(f'Baustein {b["nr"]} · {b["name"]} · Fortsetzung')
        listen = ""
        for j, (label, teil) in enumerate(segmente):
            if label:
                listen += f'<p class="mlabel"{" style=&quot;margin-top:7mm&quot;" if (k > 0 and j == 0) else ""}>{label}</p>'.replace("&quot;", '"')
            listen += '<div class="liste mliste">' + "".join(leistung(l) for l in teil) + '</div>'
        inhalt = (kopf(T) + '<div class="rand" style="padding-top:16mm">' + kopfteil + listen
                  + (hinweis if letzte else "") + '</div>')
        if letzte and b["id"] == "kern":   # Kernpaket: Ergebnis als gelbes Band unter dem Rest des Leistungsumfangs
            inhalt += ('<div class="band band--gelb wachsen mitte" style="margin-top:12mm">' + kicker("Das bekommst du")
                       + '<h2>Sichtbarkeit, die zu Anfragen führt.</h2>' + ERGEBNIS + '</div>')
        seiten.append(seite(inhalt, nr + k, n))
    return seiten


def team_seite(M, nr, n):
    """Dein Team (schwarz): vier Profile im Kernpaket als 2 × 2, eines mit Paid Ads; gelbe Icons wie auf der Seite; Band „Immer dabei“."""
    PR = M["profile"]
    def karte(x):
        return (f'<div class="tk">{ico(x["ico"], farbe="#fff400", strich=1.4)}<h3>{x["klartext"]}</h3>'
                f'<span class="tk__stelle">{x["stelle"]}</span><p>{x["denkweise"]}</p></div>')
    kern = "".join(karte(x) for x in PR["liste"] if x["gruppe"] == "kern")
    ads = "".join(karte(x) for x in PR["liste"] if x["gruppe"] == "paid-ads")
    immer = "".join(f"<b>{x}</b>" for x in M["immer"])
    return seite(
        kopf(T).replace("empiria-logo.svg", "empiria-logo-weiss.svg") + '<div class="rand dunkel" style="padding-top:16mm">' + kicker("Dein Team")
        + '<h2>Fünf Profile. Ein Team.</h2>'
        + f'<p class="lead" style="max-width:155mm">{PR["lead"]}</p>'
        + '<p class="tklammer tklammer--kern">Im Kernpaket</p>' + f'<div class="tgrid">{kern}</div>'
        + '<p class="tklammer">Mit Paid Ads</p>' + f'<div class="tgrid">{ads}<p class="tnotiz">{PR["hinweis_ergaenzungen"]}</p></div>'
        + f'<div class="immer"><span>Immer dabei</span>{immer}</div></div>', nr, n, hell_fuss=True, klasse="seite--schwarz")


def hoch_seite(M, nr, n):
    """Die digitale Maschine im Hochformat: links die senkrechte Grafik (Trichter · Vertrieb · Kundenbetreuung · Rückweg),
    rechts je Stufe der Text auf Höhe seines Grafikteils."""
    ST, W = M["stufen"], M["weg"]
    teile = maas_strukturbild.hoch_teile()
    texte = maas_strukturbild.STUFEN_TEXT
    nummern = maas_strukturbild.BAUSTEINE
    zellen = ""
    for i, (svg, h) in enumerate(zip(teile, maas_strukturbild.HOCH_ZEILEN)):
        if i < 3:
            name, claim, zeilen, erg = texte[i]
            legende = ""
            if i == 0:
                legende = '<ul class="hs__bs">' + "".join(
                    f'<li><span class="hs__nr{" hs__nr--kern" if nr == "1" else ""}">{nr}</span>{ico(icon, strich=1.5)}{name}</li>'
                    for nr, name, icon in nummern) + '</ul>'
            text = (f'<p class="hs__stufe{" hs__stufe--wir" if i == 0 else ""}">Stufe {i + 1} · {name}'
                    f'{" · unser Schwerpunkt" if i == 0 else ""}</p><h3>{claim}</h3><p class="hs__text">{" ".join(zeilen)}</p>'
                    f'{legende}<p class="hs__erg"><span>Ergebnis</span>{erg}</p>')
        else:
            text = '<p class="hs__rueck">Sichtbarkeit pflegt deinen Bestand und bringt neue Anlässe.</p>'
        zellen += f'<div class="hs__bild" style="height:{h}mm">{svg}</div><div class="hs__zelle{" hs__zelle--rueck" if i == 3 else ""}" style="height:{h}mm">{text}</div>'
    return seite(
        kopf(T) + '<div class="rand" style="padding-top:12mm">' + kicker(W["kicker"])
        + f'<h2>{W["h2"]}</h2><p class="lead" style="max-width:165mm">{ST["lead"]}</p>'
        + f'<div class="hs">{zellen}</div></div>', nr, n)


def stufen_seite(M, nr, n):
    """Erste Ebene: das Strukturbild (vier Stufen, Entscheidungen, Rückweg) auf einer Querseite, darunter das Fundament Strategie."""
    ST, W = M["stufen"], M["weg"]
    return seite(
        kopf(T) + '<div class="rand" style="padding-top:9mm">' + kicker(W["kicker"])
        + f'<h2>{W["h2"]}</h2><p class="lead" style="max-width:220mm">{ST["lead"]}</p>'
        + f'<div class="sbild sbild--m">{M["maschine"]}</div>'
        + '</div>', nr, n, klasse="seite--quer")


def detail_seite(M, nr, n):
    """Arbeitsgrundlage: der Ablauf im Detail (technisches Strukturbild) auf einer Querseite."""
    return seite(
        kopf(T) + '<div class="rand" style="padding-top:9mm">' + kicker("Arbeitsgrundlage")
        + '<h2>Der Ablauf im Detail.</h2><p class="lead" style="max-width:220mm">Mit diesem Bild klären wir im Auftakt, welche Kanäle wir nutzen, '
          'wer Interessenten qualifiziert und wie wir sie warmhalten, bis sie abschlussbereit sind.</p>'
        + f'<div class="sbild">{M["strukturbild"]}</div>'
        + '<div class="sbild__fuss"><span class="sbild__leg sbild__leg--wir">übernehmen wir</span><span class="sbild__leg">dein Vertrieb – wir docken an</span><p></p></div>'
        + '</div>', nr, n, klasse="seite--quer")


def weg_seite(M, nr, n):
    """Die Grundstory: der Weg in sechs Schritten (Homepage-Story, Szene 05) – Aufstellen grau, Übergabe gelb, Verkaufen schwarz, Steuern grau."""
    W = M["weg"]
    def zeile(s):
        return (f'<div class="wg__z"><span class="wg__nr">{s["nr"]}</span><h3>{s["frage"]}</h3>'
                f'<p class="wg__wir">{s["wir"]}</p><p class="wg__du">{s["du"]}</p></div>')
    bloecke = ""
    for i, ph in enumerate(W["phasen"]):
        if i == 1:
            bloecke += f'<p class="wg__ueb"><b>{W["uebergabe"]["label"]}</b>{W["uebergabe"]["text"]}</p>'
        bloecke += (f'<div class="wg__block{" wg__block--dunkel" if ph["dunkel"] else ""}">'
                    f'<p class="wg__phase"><b>{ph["name"]}</b><span>{ph["hinweis"]}</span></p>'
                    + "".join(zeile(s) for s in ph["schritte"]) + '</div>')
    kopfzeile = '<div class="wg__z wg__kopf"><span></span>' + "".join(f"<span>{s}</span>" for s in W["spalten"]) + '</div>'
    return seite(
        kopf(T) + '<div class="rand" style="padding-top:14mm">' + kicker(W["kicker"] + " · " + M["stufen"]["fundament"]["label"])
        + f'<h2>{W["h2_fenster"]}</h2><p class="lead" style="max-width:160mm">{W["lead"]}</p>'
        + f'<div class="wg">{kopfzeile}{bloecke}</div></div>', nr, n)


def ablauf_seite(M, nr, n):
    """So arbeiten wir (gelb): der Monatsablauf als nummerierter Zeitstrahl mit Icons – wie auf der Seite."""
    schritte = "".join(
        f'<li><span class="ab__nr">{i}</span>{ico(a["ico"], strich=1.4)}<h3>{a["titel"]}</h3><p>{a["text"]}</p></li>'
        for i, a in enumerate(M["ablauf"], 1))
    return seite(
        kopf(T) + '<div class="rand wachsen mitte">' + kicker("So arbeiten wir")
        + '<h2>Jeden Monat ein Stück besser.</h2>'
        + f'<p class="lead" style="max-width:150mm">{M["ablauf_lead"]}</p>'
        + f'<ol class="ab">{schritte}</ol></div>', nr, n, klasse="seite--gelb")


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
/* Hochformat: Grafikspalte 70 mm, Textspalte daneben; jede Stufe auf Höhe ihres Grafikteils */
.hs { display: grid; grid-template-columns: 70mm 1fr; column-gap: 9mm; margin-top: 7mm; }
.hs__bild { overflow: visible; }
.hs__zelle { display: flex; flex-direction: column; justify-content: flex-start; padding-top: 6mm; border-top: 1px solid #dcd8d1; }
.hs__zelle:nth-child(2) { border-top: 0; padding-top: 3mm; }
.hs__zelle--rueck { justify-content: center; padding-top: 0; border-top: 0; }
.hs__stufe { font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #8a847c; }
.hs__stufe--wir { color: #1a1817; }
.hs h3 { margin-top: 1.6mm; font-size: 14pt; }
.hs__text { text-wrap: pretty; margin-top: 1.8mm; font-size: 9pt; line-height: 1.55; color: #3d3a37; }
.hs__bs { list-style: none; display: grid; gap: 1.6mm; margin-top: 3.5mm; }
.hs__bs li { display: flex; align-items: center; gap: 2.2mm; font-size: 8.6pt; font-weight: 600; }
.hs__bs svg { width: 4mm; height: 4mm; }
.hs__nr { display: grid; place-items: center; width: 4.6mm; height: 4.6mm; border: 1px solid #1a1817; border-radius: 50%; font-size: 7pt; font-weight: 700; }
.hs__nr--kern { background: #1a1817; color: #fff400; }
.hs__erg { margin-top: 3.5mm; font-size: 9pt; font-weight: 600; }
.hs__erg span { display: block; font-size: 6.4pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #8a847c; }
.hs__rueck { align-self: flex-start; white-space: nowrap; padding: 1.8mm 4mm; border-radius: 9mm; background: #fff400; font-size: 8.4pt; font-weight: 600; }
/* Querseite für das Strukturbild (benannte Seite) */
@page quer { size: 297mm 210mm; margin: 0; }
.seite--quer { page: quer; width: 297mm; height: 210mm; }
.seite--quer h2 { font-size: 21pt; }
.seite--quer .lead { margin-top: 2.5mm; font-size: 9.6pt; }
.sbild { margin-top: 5mm; }
.sbild--m { margin-top: 8mm; padding: 0 10mm; }
.sbild__fuss--m { display: block; margin-top: 2mm; }
.sbild svg { display: block; width: 100%; height: auto; }
.sbild__fuss { display: grid; grid-template-columns: auto auto 1fr; gap: 6mm; align-items: start; margin-top: 3mm; font-size: 7.6pt; }
.sbild__leg { display: flex; align-items: center; gap: 2mm; white-space: nowrap; color: #6f6a64; }
.sbild__leg::before { content: ""; width: 3.6mm; height: 3.6mm; border-radius: 1mm; border: 1.2px solid #1a1817; background: #fff; }
.sbild__leg--wir::before { background: #fff400; border-color: #fff400; }
.sbild__fuss p { font-size: 7.6pt; line-height: 1.5; color: #3d3a37; }
.sbild__fuss b { color: #1a1817; }
/* Vier Stufen */
.sfk { display: grid; grid-template-columns: 1fr 3fr; gap: 3mm; margin-top: 8mm; font-size: 6.6pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #8a847c; }
.sfk span { display: flex; align-items: center; gap: 2mm; }
.sfk span::after { content: ""; flex: 1; height: 1.2px; background: #cfcac3; }
.sfk .sfk--wir { color: #1a1817; } .sfk .sfk--wir::after { background: #1a1817; }
.sfg { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(5, auto); column-gap: 3mm; margin-top: 3mm; }
.sf { display: grid; grid-row: span 5; grid-template-rows: subgrid; padding: 4.5mm 4mm 4.5mm; border-radius: 3.5mm; background: #f3f1ee; }
.sf--wir { background: #fff400; }
.sf__kopf { display: flex; justify-content: space-between; align-items: center; font-size: 6.4pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
.sf__kopf svg { width: 6mm; height: 6mm; }
.sf h3 { margin-top: 3mm; font-size: 12pt; }
.sf > p { margin-top: 1.6mm; font-size: 8pt; line-height: 1.5; color: #3d3a37; }
.sf--wir > p { color: #1a1817; }
.sf__extra { margin-top: 3mm; }
.sf__label { display: block; margin-bottom: 1.4mm; font-size: 6.2pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
.sf__extra ul { list-style: none; display: grid; gap: 1.2mm; }
.sf__extra li { position: relative; padding-left: 4mm; font-size: 7.8pt; line-height: 1.4; }
.sf__extra li::before { content: ""; position: absolute; left: .2mm; top: 1mm; width: 2.2mm; height: 1.1mm; border-left: 1.4px solid #1a1817; border-bottom: 1.4px solid #1a1817; transform: rotate(-45deg); }
.sf .sf__erg { margin-top: 3.5mm; padding-top: 2.6mm; border-top: 1px solid rgba(26,24,23,.2); font-size: 8.4pt; font-weight: 600; color: #1a1817; }
.sf__erg span { display: block; margin-bottom: .8mm; font-size: 6.2pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #8a847c; }
.sf--wir .sf__erg span { color: #1a1817; }
.fund { margin-top: 6mm; padding: 5mm 6mm; }
.fund p:not(.label) { margin-top: 1.6mm; font-size: 9pt; }
/* Der Weg: Raster Nr · Frage · Wir · Du; Aufstellen/Steuern grau, Verkaufen schwarz, Übergabe gelb */
.wg { margin-top: 7mm; }
.wg__z { display: grid; grid-template-columns: 8mm 42mm 1fr 40mm; column-gap: 5mm; align-items: start; }
.wg__kopf { padding: 0 5mm 2mm; font-size: 6.4pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #8a847c; }
.wg__block { padding: 1mm 5mm 1mm; border-radius: 3.5mm; background: #f3f1ee; }
.wg__block + .wg__block { margin-top: 2.5mm; }
.wg__phase { display: flex; align-items: baseline; gap: 2.5mm; margin: 3mm 0 1mm; }
.wg__phase b { font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
.wg__phase span { font-size: 7.8pt; color: #8a847c; }
.wg__block .wg__z { padding: 3mm 0; border-top: 1px solid #dcd8d1; }
.wg__nr { display: grid; place-items: center; width: 6.4mm; height: 6.4mm; border: 1.4px solid #1a1817; border-radius: 50%; font-size: 7.4pt; font-weight: 600; }
.wg h3 { font-size: 10.5pt; line-height: 1.25; margin-top: .6mm; }
.wg__wir, .wg__du { font-size: 8.2pt; line-height: 1.5; color: #3d3a37; margin-top: .4mm; }
.wg__du { color: #1a1817; font-weight: 600; }
.wg__block--dunkel { background: #1a1817; color: #fff; }
.wg__block--dunkel .wg__phase b { color: #fff400; }
.wg__block--dunkel .wg__phase span { color: #cfcac3; }
.wg__block--dunkel .wg__z { border-top-color: rgba(255,255,255,.16); }
.wg__block--dunkel .wg__nr { border-color: #fff400; color: #fff400; }
.wg__block--dunkel h3, .wg__block--dunkel .wg__du { color: #fff; }
.wg__block--dunkel .wg__wir { color: #cfcac3; }
.wg__ueb { display: flex; gap: 4mm; align-items: baseline; margin: 2.5mm 0; padding: 3.5mm 5mm; border-radius: 3.5mm; background: #fff400; font-size: 8.6pt; line-height: 1.5; }
.wg__ueb b { flex: 0 0 auto; font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
/* Kennzeile je Baustein: Icon · Preis groß (Poppins Bold) · das Wichtigste mit Häkchen */
.kz { display: grid; grid-template-columns: 20mm 50mm 1fr; gap: 6mm; align-items: start; margin-top: 7mm; padding: 6mm 7mm; border-radius: 4.5mm; background: #f3f1ee; }
.kz__ico svg { width: 16mm; height: 16mm; }
.kz__label { display: block; margin-bottom: 1.6mm; font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
.kz__preis b { display: block; font-family: 'Poppins', Arial, sans-serif; font-weight: 700; font-size: 22pt; line-height: 1.05; }
.kz__preis span:not(.kz__label) { display: block; margin-top: 1mm; font-size: 8.6pt; color: #3d3a37; }
.kz__preis .kz__zusatz { color: #1a1817 !important; font-weight: 600; }
.kz__haken ul { list-style: none; display: grid; gap: 1.6mm; }
.kz__haken li { position: relative; padding-left: 5mm; font-size: 8.8pt; line-height: 1.4; }
.kz__haken li::before { content: ""; position: absolute; left: .3mm; top: 1.1mm; width: 2.6mm; height: 1.3mm; border-left: 1.5px solid #1a1817; border-bottom: 1.5px solid #1a1817; transform: rotate(-45deg); }
.kz__hinweis { grid-column: 1 / -1; padding-top: 3.5mm; border-top: 1px solid #dcd8d1; font-size: 8.6pt; line-height: 1.5; color: #3d3a37; }
.kz__hinweis b { color: #1a1817; font-weight: 600; }
.kz--fuss { display: block; margin-top: 7mm; padding: 5mm 7mm; }
.kz--fuss .kz__hinweis { padding-top: 0; border-top: 0; }
.mlead { margin-top: 6mm; }
.mlead + .mlead { margin-top: 2.5mm; }
/* Ablauf (gelb) */
.ab { list-style: none; display: grid; grid-template-columns: repeat(4, 1fr); gap: 6mm; margin-top: 12mm; }
.ab li { position: relative; }
.ab li:not(:last-child)::after { content: ""; position: absolute; top: 4mm; left: 10mm; right: -4mm; border-top: 1.5px dashed rgba(26,24,23,.5); }
.ab__nr { display: grid; place-items: center; width: 8mm; height: 8mm; border: 1.5px solid #1a1817; border-radius: 50%; font-size: 8pt; font-weight: 600; }
.ab svg { display: block; width: 8mm; height: 8mm; margin-top: 7mm; }
.ab h3 { margin-top: 3.5mm; font-size: 13pt; }
.ab p { margin-top: 2mm; font-size: 8.8pt; line-height: 1.55; }
/* Team (schwarz) */
.seite--schwarz { background: #1a1817; color: #fff; }
.seite--schwarz .kicker { color: #fff400; }
.seite--schwarz .lead { color: #cfcac3; }
.tklammer { display: flex; align-items: center; gap: 3mm; margin-top: 8mm; font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #cfcac3; }
.tklammer::after { content: ""; flex: 1; height: 1.2px; background: rgba(255,255,255,.3); }
.tklammer--kern { color: #fff400; } .tklammer--kern::after { background: #fff400; }
.tgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-top: 4mm; }
.tk { padding: 5mm 5.5mm 5.5mm; border-radius: 3.5mm; background: #262321; }
.tk svg { width: 7mm; height: 7mm; }
.tk h3 { margin-top: 3mm; font-size: 12pt; color: #fff; }
.tk__stelle { display: block; margin-top: 1mm; padding-bottom: 2.4mm; border-bottom: 1px solid rgba(255,255,255,.14); font-size: 7.8pt; font-weight: 600; color: #fff; }
.tk p { margin-top: 2.4mm; font-size: 8.4pt; line-height: 1.5; color: #cfcac3; }
.tnotiz { align-self: center; padding: 0 2mm; font-size: 8.4pt; line-height: 1.55; color: #9b958e; }
.immer { display: flex; flex-wrap: nowrap; white-space: nowrap; align-items: center; gap: 2mm 5mm; margin-top: 7mm; padding: 4mm 5mm; border-radius: 3.5mm; background: #fff400; color: #1a1817; }
.immer span { font-size: 6.8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
.immer b { position: relative; padding-left: 4.4mm; font-size: 8.4pt; font-weight: 600; }
.immer b::before { content: ""; position: absolute; left: .3mm; top: 1.1mm; width: 2.4mm; height: 1.2mm; border-left: 1.5px solid #1a1817; border-bottom: 1.5px solid #1a1817; transform: rotate(-45deg); }
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
    n = 7 + sum(len(teile_von(b)) for b in B) + 2 + len(PR["liste"]) + 2

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
        + f'<p class="notiz">{M["hinweis_preise"]} Paid Ads je Werbekanal, Werbebudget nicht enthalten.</p></div>', 6, n)

    seiten, nr = [s1, hoch_seite(M, 2, n), stufen_seite(M, 3, n), weg_seite(M, 4, n), ablauf_seite(M, 5, n), s2], 7
    for b in B:
        k = kapitel(b, nr, n)
        seiten += k
        nr += len(k)
    seiten.append(team_seite(M, nr, n))
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


def bild_png(svg, datei, hoehe):
    """Bild als PNG zum Herunterladen (2-fache Auflösung, Schriften aus dem empiria-Repo)."""
    src = os.path.join(BUILD, datei + ".html")
    open(src, "w", encoding="utf-8").write(
        '<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="assets/fonts/fonts.local.css">'
        '<style>html,body{margin:0;background:#fff}div{padding:48px;width:1218px}svg{width:1218px;height:auto;display:block}</style></head>'
        f'<body><div>{svg}</div></body></html>')
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    f"--window-size=1314,{hoehe}", "--virtual-time-budget=4000", f"--screenshot={os.path.join(ZIEL, datei + '.png')}",
                    "file://" + src], capture_output=True, timeout=120)


def main():
    d = json.load(open(DATEN, encoding="utf-8"))
    M = d["maas"]
    os.makedirs(BUILD, exist_ok=True)
    link = os.path.join(BUILD, "assets")
    if not os.path.exists(link):
        os.symlink(os.path.join(EMPIRIA, "site", "assets"), link)
    # Kopfbild der Seite = Kopfbild der PDF-Titelseite (CD-Bildsprache, eine Quelle)
    svg = kopfbild("MarketingEcoSystem (MES)")
    open(os.path.join(ZIEL, "kopfbild.svg"), "w", encoding="utf-8").write(
        svg if svg.startswith("<svg") and 'xmlns=' in svg else svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1))
    M["strukturbild"] = maas_strukturbild.svg()            # Ablauf im Detail (Arbeitsgrundlage)
    M["maschine"] = maas_strukturbild.marketing_svg()       # Marketing-Grafik (erste Ebene)
    M["maschine_ss"] = maas_strukturbild.marketing_svg(ss=True)          # Farben sofort sichtbar (Seite 2.0)
    M["strukturbild_ss"] = maas_strukturbild.ss_faerben(M["strukturbild"])
    bild_png(M["strukturbild"], "strukturbild", 652)
    bild_png(M["maschine"], "maschine", 748)
    bild_png(M["maschine_ss"], "maschine-ss", 748)
    bild_png(M["strukturbild_ss"], "strukturbild-ss", 652)
    drucken(bauen(M), M["pdf"]["datei"], "marketing-as-a-service", M["pdf"])
    # Arbeitsgrundlage als eigenes PDF (nicht im Angebots-PDF): Ablauf im Detail, A4 quer
    M.setdefault("pdf_ablauf", {"datei": "marketing-as-a-service-ablauf.pdf"})
    drucken(dokument(f"Ablauf im Detail – {T}", [detail_seite(M, 1, 1)], extra_css=mt.CSS + CSS + CSS_TEAM),
            M["pdf_ablauf"]["datei"], "marketing-as-a-service-ablauf", M["pdf_ablauf"])
    for i in (1, 2):   # Vorschaubilder braucht das Arbeits-PDF nicht
        f = os.path.join(ZIEL, f"marketing-as-a-service-ablauf-{i}.png")
        if os.path.exists(f):
            os.remove(f)
    json.dump(d, open(DATEN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(DATEN, "a").write("\n")


if __name__ == "__main__":
    main()
