#!/usr/bin/env python3
"""One-Pager „Infografik sofort sichtbar“ im Look der Homepage (Story 7) – Daniel, 12.11.2026.

Zwei Geschichten in drei Formaten (Skizze freigegeben: beide Geschichten in allen Formaten):
  maschine  – Die Grundstory: die digitale Maschine vor deinem Vertrieb (Trichter, drei Schritte)
  maas      – Marketing as a Service: Wir bedienen die Maschine. Du verkaufst. (Gesamtlogik, Schnitt, 30-Tage-Plan)
Formate: DIN A3 quer (420 × 297), DIN A3 hoch (297 × 420), Roll-up 100 × 200 cm
         (Roll-up gestaltet auf 297 × 594 mm und beim Drucken auf 1000 × 2000 mm vergrößert – Seite im Originalmaß).

SCHRIFTSYSTEM (fest, wie die Website – nicht empiria):
  Inter Tight 700 – H1 (eine Größe je Format) und H2 (eine Größe für alle übrigen Überschriften)
  Inter 400/600   – Text in einer Größe (Regular, Hervorhebung SemiBold); Klein für Kicker und Nebeninfos (Medium-Grau)
  Farben          – Tinte #1d1d1f, Grau #6e6e73, Bühnen #f5f5f7, dunkles Kontaktband #1d1d1f;
                    Verlauf Cyan → Violett nur im Akzentwort der H1 und im Kern des Trichters.
  Logo            – rechts oben, Oberkante auf der Oberkante des Kickers.
Grafiken: s7.ek_quer, s7.ek_hoch, s7.ek_schnitt_quer, s7.ek_kopf_trichter – dieselben wie auf der Website.

Aufruf:  python3 src/entwicklung/storyboard/story7/onepager7.py
Ergebnis: story7/assets/onepager/<geschichte>-<format>.pdf und .png
"""
import html
import json
import os
import subprocess
import tempfile

from maas_pdf7 import SVG_CSS, VERLAUF_JS as _VJ

# Verlaufswörter als SVG-Text; beim Roll-up ist das Blatt gezoomt – Maße von getBoundingClientRect durch den Zoom teilen
VERLAUF_JS = _VJ.replace("const r = s.getBoundingClientRect(),",
                         "const z = parseFloat(getComputedStyle(document.querySelector('.blatt')).zoom) || 1, r0 = s.getBoundingClientRect(), r = {width: r0.width / z},")
assert "r0.width / z" in VERLAUF_JS

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
D7 = os.path.join(HERE, "story7.11tydata.json")
ZIEL = os.path.join(HERE, "assets", "onepager")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
e = html.escape

FORMATE = {  # Name: (Breite, Höhe, Druckbreite, Druckhöhe) in mm
    "a3-quer": (420, 297, 420, 297),
    "a3-hoch": (297, 420, 297, 420),
    "rollup": (297, 594, 1000, 2000),
}


def css(fmt):
    w, h, pw, ph = FORMATE[fmt]
    f = os.path.join(HERE, "assets", "fonts")
    faces = ""
    for fam, datei, wt in [("Inter", "inter", 400), ("Inter", "inter", 600), ("Inter Tight", "inter-tight", 700)]:
        for sub in ("latin", "latin-ext"):
            faces += f'@font-face{{font-family:"{fam}";font-weight:{wt};src:url("file://{f}/{datei}-{sub}-{wt}-normal.woff2") format("woff2");}}\n'
    zoom = pw / w
    return faces + f"""
@page {{ size: {pw}mm {ph}mm; margin: 0; }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; }}
.blatt {{ zoom: {zoom}; position: relative; width: {w}mm; height: {h}mm; overflow: hidden; display: flex; flex-direction: column;
  padding: var(--rand) var(--rand) 0; background: #fff; color: #1d1d1f; font: 400 var(--text)/1.5 "Inter"; }}
""" + r"""
/* Größen je Format: H1 · H2 · Text · Klein · Rand */
.a3-quer { --h1: 42pt; --h2: 15pt; --text: 9pt; --klein: 7pt; --rand: 20mm; }
.a3-hoch { --h1: 42pt; --h2: 15pt; --text: 9pt; --klein: 7pt; --rand: 20mm; }
.rollup  { --h1: 60pt; --h2: 21pt; --text: 12pt; --klein: 9.5pt; --rand: 24mm; --logo: 11mm; }
.rollup .mini, .rollup .chip { font-size: 10.5pt; }
p { margin: 0; }
b { font-weight: 600; }
h1, h2, h3 { margin: 0; font-family: "Inter Tight"; font-weight: 700; letter-spacing: -0.025em; color: #1d1d1f; }
h1 { font-size: var(--h1); line-height: 1.0; }
h2, h3 { font-size: var(--h2); line-height: 1.12; }
.v { color: #0b9fbd; }
svg.vs { display: inline-block; overflow: visible; }
.kicker { color: #6e6e73; font-size: var(--klein); font-weight: 600; line-height: 1; }
.lead { color: #424245; }
.grau { color: #6e6e73; }
.klein { font-size: var(--klein); }

/* Kopf: Kicker und Logo auf einer Oberkante */
.kopf { display: grid; grid-template-columns: 1fr auto; column-gap: 10mm; align-items: start; padding-bottom: var(--luft); }
.a3-quer, .a3-hoch { --luft: 9mm; }
.rollup { --luft: 18mm; }
.kopf .kicker { margin-top: 0; }
.kopf h1 { margin-top: 4mm; }
.logo { display: block; height: var(--logo, 9mm); margin-top: calc(var(--klein) * 0.087); }
.kopf .lead { margin-top: 5mm; max-width: 150mm; font-size: calc(var(--text) * 1.18); line-height: 1.45; }
.a3-quer .kopf .lead { max-width: none; }
.a3-hoch .kopf .lead { max-width: 210mm; }
.buehne.schnitt svg { width: 86%; margin: 0 auto; }
.a3-hoch .buehne.schnitt svg { width: 80%; }
.a3-quer .buehne.schnitt svg { width: 74%; }
.a3-quer .gg-trichter svg { max-height: 21mm; }
.a3-quer .gg-inhalt { padding: 4mm 5mm; }
.a3-quer .dash .kacheln > div { padding: 2mm 2.6mm; font-size: var(--klein); }
.a3-quer .dash .kacheln svg { height: 3.5mm; margin-top: 1.2mm; }
.a3-quer .dash .empfs { gap: 1.8mm; }
.a3-quer .dash .empfs div { padding: 1.8mm 2.6mm; }
.a3-quer .dash .empfs b { font-size: var(--klein); }
.a3-quer .dash .lbl { margin: 3.5mm 0 1.6mm; }
.a3-quer .gg-fragen { display: flex; flex-wrap: wrap; align-content: center; gap: 1.8mm; }
.a3-hoch .dash .kacheln svg { height: 4mm; }
.a3-hoch .dash .kacheln > div { padding: 2.4mm 3mm; }
.a3-quer .band, .a3-hoch .band { padding-top: 10mm; padding-bottom: 11mm; }

/* Bühne mit Grafik der Website */
.buehne { border-radius: 6mm; background: #f5f5f7; }
.buehne svg { display: block; width: 100%; height: auto; overflow: visible; }
.buehne svg.ek2-svg--hoch { display: block !important; width: 140mm; margin: 0 auto; }
.ek2-kern-h { fill: url(#s7v-cyanviolett-h); }
.ek2-l2-h { fill: #d5d5db; } .ek2-l3-h { fill: #e1e1e6; } .ek2-l4-h { fill: #ececf0; }

/* Drei Schritte der Startseite */
.schritte { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); grid-template-rows: repeat(4, auto); column-gap: 8mm; }
.schritt { display: grid; grid-row: span 4; grid-template-rows: subgrid; row-gap: 0; }
.schritt.linie { grid-row: span 3; }
.schritt .bild { display: grid; align-items: center; padding: 5mm; border-radius: 4mm; background: #f5f5f7; }
.schritt .nr { margin-top: 4mm; }
.schritt h3 { margin-top: 1.5mm; }
.schritt p.t { margin-top: 2mm; color: #424245; }
.schritt.linie { padding-top: 4mm; border-top: 0.6mm solid #1d1d1f; }
.schritt.linie .nr { margin-top: 0; }

/* kleine Bilder (wie s7-mini) */
.mini { display: grid; gap: 2mm; font-size: var(--klein); line-height: 1.3; }
.mini .z { display: grid; grid-template-columns: 17mm 1fr; align-items: center; gap: 1.5mm; }
.mini .z > span { color: #6e6e73; font-size: calc(var(--klein) * .82); font-weight: 600; letter-spacing: .08em; text-transform: uppercase; }
.mini .z > div { display: flex; flex-wrap: wrap; gap: 1mm; }
.chip { display: inline-block; font-style: normal; padding: .7mm 2.2mm; border: 0.3mm solid #d2d2d7; border-radius: 9mm; background: #fff; white-space: nowrap; font-size: var(--klein); line-height: 1.35; }
.chip.an { border-color: #1d1d1f; background: #1d1d1f; color: #fff; font-weight: 600; }
.chip.ziel { border-color: transparent; background: linear-gradient(100deg, #0b9fbd, #8613a1); color: #fff; font-weight: 600; }
.chip.mehr { border-style: dashed; color: #6e6e73; background: none; }
.strecke { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 2mm; }
.strecke ul { display: grid; gap: 1.2mm; margin: 0; padding: 0; list-style: none; }
.strecke li { padding: 1.3mm 2mm; border: 0.3mm solid #d2d2d7; border-radius: 1.8mm; background: #fff; font-weight: 600; }
.strecke svg { width: 4mm; height: 4mm; fill: none; stroke: #1d1d1f; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.lead-k { display: grid; gap: .5mm; padding: 2.4mm 2.6mm; border-radius: 2.4mm; background: linear-gradient(100deg, #0b9fbd, #8613a1); color: rgba(255,255,255,.85); }
.lead-k b { color: #fff; }
.kacheln { display: grid; grid-template-columns: 1fr 1fr; gap: 1.4mm; }
.kacheln > div { padding: 1.5mm 2mm; border: 0.3mm solid #d2d2d7; border-radius: 1.8mm; background: #fff; font-weight: 600; }
.kacheln > div.ziel { border-color: transparent; background: linear-gradient(100deg, #0b9fbd, #8613a1); color: #fff; }
.kacheln svg { display: block; width: 100%; height: 3.2mm; margin-top: .8mm; fill: none; stroke: currentColor; stroke-width: 1.4; }
.empf { padding: 1.6mm 2mm; border: 0.3mm solid #d2d2d7; border-radius: 1.8mm; background: #fff; }

/* Gesamtlogik Marketing as a Service (wie Kopf der Website) */
.gg { padding: 9mm 10mm 8mm; border-radius: 6mm; background: #f5f5f7; }
.gg-klammer { padding-bottom: 2.5mm; border-bottom: 0.6mm solid #1d1d1f; font-weight: 600; }
.gg-spalten { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); grid-template-rows: auto auto 1fr; column-gap: 13mm; margin-top: 6mm; }
.gg-sp { position: relative; display: grid; grid-row: span 3; grid-template-rows: subgrid; }
.gg-sp:not(:last-child)::after { content: ""; position: absolute; top: 60%; right: -7.6mm; width: 2.4mm; height: 2.4mm; border-top: 0.6mm solid #1d1d1f; border-right: 0.6mm solid #1d1d1f; transform: rotate(45deg); }
.gg-titel { display: flex; align-items: center; gap: 2mm; font-family: "Inter Tight"; font-size: var(--h2); font-weight: 700; letter-spacing: -0.02em; line-height: 1.1; }
.gg-titel span { display: inline-grid; place-items: center; flex: none; width: 1.25em; height: 1.25em; border-radius: 50%; background: #1d1d1f; color: #fff; font-family: "Inter"; font-size: .5em; letter-spacing: 0; }
.gg-sub { margin-top: 1.2mm; color: #6e6e73; }
.gg-inhalt { display: grid; align-content: center; gap: 1.5mm; margin-top: 4.5mm; padding: 5mm 5.5mm; border-radius: 4mm; background: #fff; }
.gg-fragen { justify-items: start; }
.gg-fragen .chip { white-space: normal; }
.gg-trichter svg { display: block; width: 100%; height: auto; max-height: 26mm; }
.gg-trichter p { margin-top: 1mm; font-size: var(--klein); font-weight: 600; text-align: right; }
.gg-zurueck { position: relative; height: 7mm; margin: 4mm 16.5% 0; border: 0.6mm solid #1d1d1f; border-top: 0; border-radius: 0 0 3.5mm 3.5mm; }
.gg-zurueck::before { content: ""; position: absolute; left: -1.25mm; top: -.4mm; width: 1.9mm; height: 1.9mm; border-left: 0.6mm solid #1d1d1f; border-top: 0.6mm solid #1d1d1f; transform: rotate(45deg); }
.gg-zurueck span { position: absolute; left: 50%; bottom: 0; transform: translate(-50%, 52%); padding: 0 3mm; background: #f5f5f7; font-size: var(--klein); font-weight: 600; white-space: nowrap; }

/* Abschnitte */
.abschnitt h2 { margin-bottom: 6mm; }
.abschnitt .kicker { margin-bottom: 2mm; }
.wochen { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); column-gap: 6mm; }
.woche .w { font-weight: 600; }
.woche .punkt { position: relative; display: block; height: 7mm; }
.woche .punkt::before { content: ""; position: absolute; left: 0; right: -6mm; top: 50%; height: 0.5mm; background: #1d1d1f; }
.woche:last-child .punkt::before { right: 0; }
.woche .punkt::after { content: ""; position: absolute; left: 0; top: 50%; width: 3.4mm; height: 3.4mm; border: 0.5mm solid #1d1d1f; border-radius: 50%; background: #fff; transform: translateY(-50%); }
.woche:last-child .punkt::after { border: 0; width: 4.4mm; height: 4.4mm; background: linear-gradient(100deg, #0b9fbd, #8613a1); }
.woche h3 { margin-top: 1mm; font-family: "Inter"; font-size: var(--text); font-weight: 600; letter-spacing: 0; }
.woche p { margin-top: .8mm; color: #424245; font-size: var(--klein); line-height: 1.4; }
.wochen.senkrecht { grid-template-columns: minmax(0, 1fr); row-gap: 3mm; }
.wochen.senkrecht .woche { display: grid; grid-template-columns: 20mm minmax(0, 1fr); column-gap: 4mm; padding-top: 3mm; border-top: 0.3mm solid #d2d2d7; }
.wochen.senkrecht .woche .punkt { display: none; }
.wochen.senkrecht .woche h3 { margin-top: 0; }
.zitat { font-family: "Inter Tight"; font-size: var(--h2); font-weight: 700; letter-spacing: -0.02em; line-height: 1.2; }
.zitat + .klein { margin-top: 2mm; color: #6e6e73; }

/* Kontaktband (dunkel, bis zur Kante) */
.blatt > :nth-last-child(2) { margin-bottom: 14mm; }
.band { margin: auto calc(-1 * var(--rand)) 0; padding: 12mm var(--rand) 13mm; background: #1d1d1f; color: #d2d2d7; display: grid; grid-template-columns: minmax(0, 1fr) auto; column-gap: 12mm; align-items: end; }
.band h2 { color: #fff; }
.band .t { margin-top: 2.5mm; color: #a1a1a6; }
.band .wege { display: grid; gap: 1.2mm; color: #fff; font-weight: 600; }
.band .wege .k { color: #a1a1a6; font-size: var(--klein); font-weight: 600; }
.band .team { display: flex; align-items: center; gap: 3mm; margin-bottom: 2.5mm; color: #a1a1a6; font-size: var(--klein); font-weight: 400; }
.band .team span { display: flex; }
.band .team img { width: 9mm; height: 9mm; border-radius: 50%; object-fit: cover; margin-left: -2mm; border: 0.5mm solid #1d1d1f; filter: grayscale(1); }
.band .team img:first-child { margin-left: 0; }
/* Ausführliche Grundstory: 01 Strategie · 02 drei Stufen am Trichter · 03 Steuerung */
.teil { padding-top: 5mm; border-top: 0.6mm solid #1d1d1f; }
.teil-kopf { display: grid; grid-template-columns: auto minmax(0, 1fr); column-gap: 6mm; align-items: start; }
.teil-kopf .nr { font-family: "Inter Tight"; font-weight: 700; font-size: calc(var(--h2) * 2.2); line-height: .85; letter-spacing: -0.03em; }
.teil-kopf .kicker { margin-bottom: 1.6mm; }
.teil-kopf .sub { margin-top: 1.2mm; color: #6e6e73; }
.teil-inhalt { margin-top: 6mm; }
.a3-hoch .teil-inhalt { margin-top: 4.5mm; }
.a3-hoch .notiz { margin-top: 3.5mm; }
.a3-hoch .dash-inhalt { padding: 4mm; }
.a3-hoch .dash .lbl { margin: 3.5mm 0 1.6mm; }
.a3-hoch .pfad .chip { padding: .6mm 1.7mm; }
.a3-hoch .dash .kacheln svg { height: 3.5mm; margin-top: 1.5mm; }
.a3-hoch .dash .empfs div { padding: 2mm 3mm; }
.a3-hoch .dash-kopf { padding: 2mm 4mm; }
.a3-hoch .teil { padding-top: 4mm; }
.a3-hoch .pfad .chips { gap: 1.3mm; }
.a3-hoch .stufen-quer { margin-top: 5mm; row-gap: 3mm; }
.a3-hoch.kurz .band { padding-top: 8mm; padding-bottom: 9mm; }
.kurz .band .wege { grid-template-columns: auto auto; column-gap: 10mm; align-items: end; }
.kurz .band .team { grid-row: span 2; flex-direction: column; align-items: flex-start; margin: 0; max-width: 40mm; }
.stufen .texte { min-height: 0; }
.stufe.mess { margin-top: auto; padding-top: 1.6mm; }
.pfad { display: grid; grid-template-columns: auto auto auto auto minmax(0, 1fr); column-gap: 5mm; align-items: start; }
.pfad .pf { padding-top: 6.5mm; font-size: calc(var(--text) * 1.4); line-height: 1; }
.pfad .lbl { margin-bottom: 2mm; color: #6e6e73; font-size: calc(var(--klein) * .9); font-weight: 600; letter-spacing: .1em; text-transform: uppercase; }
.pfad .chips { display: flex; flex-wrap: wrap; gap: 1.6mm; }
.pfad .chips.spalte { flex-direction: column; align-items: flex-start; }
.pfad.senkrecht { grid-template-columns: minmax(0, 1fr); row-gap: 3mm; }
.pfad.senkrecht .pf { padding: 0 0 0 3mm; }
.notiz { margin-top: 5mm; color: #6e6e73; font-size: var(--klein); }
.stufen { display: grid; grid-template-columns: var(--tr, 64mm) minmax(0, 1fr); column-gap: 12mm; }
.stufen .grafik svg { display: block !important; width: 100%; height: auto; overflow: visible; }
.stufen .texte { position: relative; }
.stufen .texte { display: flex; flex-direction: column; gap: 4mm; }
.stufe.mess { margin-top: auto; }
.stufe.s2 { margin-top: 5mm; }
.stufe.s3 { margin-top: auto; }
.stufe .kicker { margin-bottom: 1.4mm; }
.stufe h3 { font-size: var(--h2); }
.stufe p.t { margin-top: 1.4mm; color: #424245; }
.stufe ul { margin: 3mm 0 0; padding: 0; list-style: none; display: grid; gap: 1.6mm; }
.stufe li { padding-left: 4mm; position: relative; color: #424245; }
.stufe li::before { content: ""; position: absolute; left: 0; top: .55em; width: 1.8mm; height: 1.8mm; border-radius: 50%; background: linear-gradient(100deg, #0b9fbd, #8613a1); }
.stufe li b { color: #1d1d1f; }
.stufe.mess { padding-top: 1.6mm; border-top: 0.4mm dashed #1d1d1f; }
.stufe.mess b { font-family: "Inter Tight"; font-size: var(--h2); font-weight: 700; letter-spacing: -0.02em; }
.dash { border: 0.5mm solid #1d1d1f; border-radius: 5mm; overflow: hidden; }
.dash-kopf { display: flex; align-items: center; gap: 1.4mm; padding: 2.6mm 5mm; border-bottom: 0.3mm solid #d2d2d7; font-weight: 600; font-size: var(--klein); }
.dash-kopf i { width: 2mm; height: 2mm; border-radius: 50%; background: #d2d2d7; }
.dash-kopf span { margin-left: 2mm; }
.dash-inhalt { padding: 5mm; }
.dash .kacheln { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 3mm; }
.dash .kacheln > div { padding: 3mm 3.5mm; background: #f5f5f7; border-color: transparent; font-size: var(--text); }
.dash .kacheln > div.ziel { background: linear-gradient(100deg, #0b9fbd, #8613a1); }
.rollup .pfad, .a3-hoch .pfad { grid-template-columns: auto auto minmax(0, 1fr); }
.rollup .pfad .pf2, .a3-hoch .pfad .pf2 { display: none; }
.rollup .pfad .zg, .a3-hoch .pfad .zg { grid-column: 1 / -1; margin-top: 4mm; }
.dash .kacheln svg { height: 5mm; margin-top: 2mm; }
.dash .lbl { margin: 5mm 0 2mm; color: #6e6e73; font-size: calc(var(--klein) * .9); font-weight: 600; letter-spacing: .1em; text-transform: uppercase; }
.dash .empfs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 3mm; }
.dash .empfs div { padding: 2.6mm 3.5mm; border: 0.3mm solid #d2d2d7; border-radius: 2.4mm; font-size: var(--klein); line-height: 1.35; }
.dash .empfs b { display: block; font-size: var(--text); }
.a3-quer .dash .kacheln { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.a3-quer .dash .empfs { grid-template-columns: minmax(0, 1fr); }
.stufen-quer { display: grid; grid-template-columns: minmax(0, 1.7fr) minmax(0, 1fr) minmax(0, 1fr); grid-template-rows: auto auto; column-gap: 9mm; row-gap: 4mm; margin-top: 6mm; }
.stufen-quer .s1 { grid-row: span 2; }
.stufen-quer .mess { grid-column: 2 / 4; grid-row: 1; padding-bottom: 3mm; border-bottom: 0.3mm solid #d2d2d7; }
.stufen-quer .s2 { grid-column: 2; grid-row: 2; }
.stufen-quer .s3 { grid-column: 3; grid-row: 2; }
.stufen-quer .stufe.mess, .stufen-quer .stufe.s2, .stufen-quer .stufe.s3 { margin-top: 0; }
.stufen-quer .stufe.mess { padding-top: 0; border-top: 0; }

.teil.red { display: grid; grid-template-columns: var(--links, 62mm) minmax(0, 1fr); column-gap: 10mm; padding-top: 5mm; }
.teil.red .teil-kopf { display: block; }
.teil.red .teil-kopf .nr { margin-bottom: 4mm; }
.teil.red .teil-kopf .sub { margin-top: 2mm; max-width: 58mm; }
.teil.red .teil-inhalt { margin-top: 1mm; }
.rollup .teil.red { --links: 68mm; }
.teil.red .pfad { grid-template-columns: auto auto minmax(0, 1fr); }
.teil.red .pfad .pf2 { display: none; }
.teil.red .pfad .zg { grid-column: 1 / -1; margin-top: 4mm; }
.teil.red .stufen-quer { grid-template-columns: repeat(3, minmax(0, 1fr)); grid-template-rows: auto auto; column-gap: 7mm; }
.teil.red .stufen-quer .s1 { grid-column: 1 / -1; grid-row: 1; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); column-gap: 7mm; padding-bottom: 4mm; border-bottom: 0.3mm solid #d2d2d7; }
.teil.red .stufen-quer .s1 ul { grid-column: 2; grid-row: 1 / span 3; margin-top: 0; align-self: center; }
.teil.red .stufen-quer .mess { grid-column: 1; grid-row: 2; padding: 0; border: 0; }
.teil.red .stufen-quer .s2 { grid-column: 2; grid-row: 2; }
.teil.red .stufen-quer .s3 { grid-column: 3; grid-row: 2; }
/* Teil 3 flacher: Kennzahlen und Empfehlungen nebeneinander */
.dash.flach .dash-inhalt { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); column-gap: 5mm; align-items: start; }
.dash.flach .kacheln { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 2mm; }
.dash.flach .kacheln > div { padding: 2mm 2.6mm; font-size: var(--klein); }
.dash.flach .kacheln svg { height: 3mm; margin-top: 1mm; }
.dash.flach .lbl { margin: 0 0 1.6mm; }
.dash.flach .empfs { grid-template-columns: minmax(0, 1fr); gap: 1.6mm; }
.dash.flach .empfs div { padding: 1.6mm 2.6mm; }
.dash.flach .empfs b { font-size: var(--klein); }

/* Druckfassung: ohne Band, Adresse unten rechts bündig mit dem Logo */
.druck { padding-bottom: var(--rand); }
.druck .verteilt { flex: 1; display: flex; flex-direction: column; justify-content: space-between; padding-bottom: 12mm; }
.druck.a3-quer .verteilt { justify-content: flex-start; }
.druck.a3-quer .verteilt > .drei-spalten { flex: 1; }
.fuss-url { padding-top: 3.5mm; border-top: 0.3mm solid #d2d2d7; text-align: right; color: #1d1d1f; font-size: var(--text); font-weight: 600; line-height: 1; }
.drei-spalten { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.75fr) minmax(0, .95fr); column-gap: 12mm; }

.a3-quer .band { padding-top: 7mm; padding-bottom: 8mm; }
.a3-quer .band .wege { grid-template-columns: auto auto; column-gap: 10mm; align-items: end; }
.a3-quer .band .team { grid-row: span 2; flex-direction: column; align-items: flex-start; margin: 0; max-width: 40mm; }
/* A3 hoch: größere kleine Bilder, mehr Luft */
.a3-hoch .schritt .bild { padding: 6mm 5mm; min-height: 58mm; }

.a3-hoch .mini, .a3-hoch .chip { font-size: 9.5pt; }
.a3-hoch .schritt .mini, .a3-hoch .schritt .chip { font-size: 9.5pt; }
"""


def kopf(S, kicker, h1, akzent, lead, logo, umbruch=True):
    h = f'{e(h1)}{"<br>" if umbruch else " "}<span class="v">{e(akzent)}</span>'
    return (f'<div class="kopf"><div class="links"><p class="kicker">{e(kicker)}</p><h1>{h}</h1></div>'
            f'<p class="lead">{e(lead)}</p><img class="logo" src="{logo}" alt="sofort sichtbar"></div>')


def kopf_hoch(kicker, h1, akzent, lead, logo, br_akzent=True):
    h = f'{h1}{"<br>" if br_akzent else " "}<span class="v">{e(akzent)}</span>'
    return (f'<div class="kopf"><div><p class="kicker">{e(kicker)}</p><h1>{h}</h1><p class="lead">{e(lead)}</p></div>'
            f'<img class="logo" src="{logo}" alt="sofort sichtbar"></div>')


def band(S, img6, h2=None, t=None):
    K = S["kontakt"]
    team = "".join(f'<img src="file://{img6}/ansprechpartner-{n}.webp" alt="">' for n in ("kerstin", "daniel", "noah"))
    return (f'<div class="band"><div><h2>{e(h2 or K["h2"])} <span class="v">{e(K["h2_akzent"]) if not h2 else ""}</span></h2>'
            f'<p class="t">{e(t or K["t"])}</p></div>'
            f'<div class="wege"><p class="team"><span>{team}</span>{e(K["team_satz"])}</p>'
            f'<p><span class="k">Termin</span><br>sofortsichtbar.de/kontakt</p>'
            f'<p>{e(K["mail"])} · {e(K["tel"])}</p></div></div>')


VERLAUF_H = '<svg width="0" height="0" style="position:absolute"><defs><linearGradient id="s7v-cyanviolett-h" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient></defs></svg>'
PFEIL = '<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
AUF = '<svg viewBox="0 0 60 16" preserveAspectRatio="none"><polyline points="0,13 12,11 24,12 36,8 48,6 60,3"/></svg>'
AB = '<svg viewBox="0 0 60 16" preserveAspectRatio="none"><polyline points="0,4 12,5 24,4 36,8 48,10 60,13"/></svg>'
MINI = [
    '<div class="mini"><div class="z"><span>Segment</span><div><i class="chip an">Privatkunden</i><i class="chip">Firmenkunden</i></div></div>'
    '<div class="z"><span>Sparte</span><div><i class="chip an">Leben</i><i class="chip">Kranken</i><i class="chip">Kfz</i></div></div>'
    '<div class="z"><span>Zielgruppe</span><div><i class="chip ziel">Junge Familien</i><i class="chip an">Bauherren</i><i class="chip mehr">+ weitere</i></div></div></div>',
    f'<div class="mini"><div class="strecke"><ul><li>Landingpage</li><li>Postings</li><li>Kundenmailing</li></ul>{PFEIL}'
    '<div class="lead-k"><b>Neuer Lead</b><span>Familie M.</span><span>Rückruf heute</span></div></div></div>',
    f'<div class="mini"><div class="kacheln"><div>Aufmerksamkeit{AUF}</div><div class="ziel">Verweildauer{AB}</div><div>Google{AUF}</div><div>Leads{AUF}</div></div>'
    '<p class="empf"><b>Empfehlung:</b> Bauherren – Abschnitt umstellen, der kaum gelesen wird</p></div>',
]


def schritte(S, mit_bild=True):
    out = ""
    for k, x in enumerate(S["schritte"]["liste"]):
        bild = f'<div class="bild">{MINI[k]}</div>' if mit_bild else ""
        out += (f'<div class="schritt{"" if mit_bild else " linie"}">{bild}<p class="nr kicker">{x["nr"]} · {e(x["label"])}</p>'
                f'<h3>{x["h"].replace("|", " ")}</h3><p class="t">{e(x["t"])}</p></div>')
    return f'<div class="schritte">{out}</div>'


def gesamtlogik(S):
    KP = S["maas"]["kopf"]
    sp = KP["spalten"]
    fragen = "".join(f'<span class="chip">„{e(f)}“</span>' for f in KP["fragen"])
    inhalt = [fragen, f'{S["ek_kopf_trichter"]}<p>{e(KP["leads"])}</p>',
              f'<div class="mini"><div class="kacheln"><div>Aufmerksamkeit{AUF}</div><div>Verweildauer{AB}</div><div>Google{AUF}</div><div class="ziel">Leads{AUF}</div></div>'
              f'<p class="empf"><b>Empfehlung:</b> {e(KP["empf"])}</p></div>']
    kl = ["gg-fragen", "gg-trichter", ""]
    spalten = "".join(f'<div class="gg-sp"><p class="gg-titel"><span>{sp[k]["nr"]}</span>{e(sp[k]["titel"])}</p>'
                      f'<p class="gg-sub">{e(sp[k]["sub"])}</p><div class="gg-inhalt {kl[k]}">{inhalt[k]}</div></div>' for k in range(3))
    return (f'<div class="gg"><p class="gg-klammer">{e(KP["klammer"])}</p><div class="gg-spalten">{spalten}</div>'
            f'<p class="gg-zurueck"><span>{e(KP["zurueck"])}</span></p></div>')


def wochen(S, senkrecht=False):
    ST = S["maas"]["start"]
    w = "".join(f'<div class="woche"><p class="w">{e(x["wann"])}</p><span class="punkt"></span><div><h3>{e(x["titel"])}</h3><p>{e(x["text"])}</p></div></div>'
                for x in ST["liste"])
    return f'<div class="wochen{" senkrecht" if senkrecht else ""}">{w}</div>'


ZG = ["Junge Familien", "Berufseinsteiger", "Private Bauherren", "Ärzte und Zahnärzte", "Immobilienmakler", "Landwirte", "Gründer & Freelancer", "Vereine"]


def teil_kopf(nr, kicker, h2, sub):
    return (f'<div class="teil-kopf"><p class="nr">{nr}</p><div><p class="kicker">{e(kicker)}</p><h2>{e(h2)}</h2>'
            f'<p class="sub">{e(sub)}</p></div></div>')


def pfad(senkrecht=False):
    seg = '<i class="chip an">Privatkunden</i><i class="chip">Firmenkunden</i>'
    sp = '<i class="chip an">Leben</i><i class="chip">Kranken</i><i class="chip">Schaden/Unfall</i><i class="chip">Kfz</i>'
    zg = '<i class="chip ziel">Junge Familien</i>' + "".join(f'<i class="chip">{e(z)}</i>' for z in ZG[1:]) + '<i class="chip mehr">+ weitere</i>'
    pf = '<p class="pf">↓</p>' if senkrecht else '<p class="pf">›</p>'
    pf2 = pf.replace('class="pf"', 'class="pf pf2"')
    return (f'<div class="pfad{" senkrecht" if senkrecht else ""}"><div><p class="lbl">Segment</p><div class="chips">{seg}</div></div>{pf}'
            f'<div><p class="lbl">Sparte</p><div class="chips">{sp}</div></div>{pf2}'
            f'<div class="zg"><p class="lbl">Zielgruppe</p><div class="chips">{zg}</div></div></div>')


def stufen_teil(S, tr, quer=False):
    st = (
        '<div class="stufe s1"><p class="kicker">Stufe 1 · Marketing</p><h3>Interessenten gewinnen.</h3>'
        '<p class="t">Deine Zielgruppen nehmen dich regelmäßig wahr – daraus entstehen Leads.</p>'
        '<ul><li><b>Landingpage</b> – je Zielgruppe, gebaut für Leads</li><li><b>Postings</b> – erscheinen automatisch auf deinen Kanälen</li>'
        '<li><b>Kundenmailing</b> – aktiviert deinen Bestand</li></ul></div>'
        '<div class="stufe mess"><p class="kicker">Messpunkt</p><b>Leads: echte Anfragen</b></div>'
        '<div class="stufe s2"><p class="kicker">Stufe 2 · Vertrieb</p><h3>Abschließen.</h3>'
        '<p class="t">Termin, Beratung, Abschluss – wie du es kennst. Nur mit mehr Gesprächen.</p></div>'
        '<div class="stufe s3"><p class="kicker">Stufe 3 · Kundenbetreuung</p><h3>Kunden halten.</h3>'
        '<p class="t">Wer regelmäßig von dir hört, bleibt – und bringt neue Anlässe mit.</p></div>')
    if quer:  # Trichter quer, darunter die Stufen in Spalten unter dem passenden Teil der Grafik
        return (f'<div class="buehne" style="padding:6mm 9mm 5mm">{S["ek_quer"]}</div>'
                f'<div class="stufen-quer">{st}</div>')
    return f'<div class="stufen" style="--tr:{tr}"><div class="grafik">{S["ek_hoch"]}</div><div class="texte">{st}</div></div>'


def dashboard(flach=False):
    k = (f'<div class="kacheln"><div>Aufmerksamkeit{AUF}</div><div>Verweildauer{AB}</div><div>Google{AUF}</div>'
         f'<div class="ziel">Leads{AUF}</div></div>')
    em = ('<div class="empfs"><div><b>Landingpage</b>Abschnitt umstellen, der kaum gelesen wird</div>'
          '<div><b>LinkedIn</b>Thema verstärken, das Leads bringt</div><div><b>Google</b>Seite für einen gesuchten Begriff ausbauen</div></div>')
    if flach:
        return (f'<div class="dash flach"><p class="dash-kopf"><i></i><i></i><i></i><span>Dashboard</span></p>'
                f'<div class="dash-inhalt">{k}<div><p class="lbl">Empfehlungen</p>{em}</div></div></div>')
    return (f'<div class="dash"><p class="dash-kopf"><i></i><i></i><i></i><span>Dashboard</span></p>'
            f'<div class="dash-inhalt">{k}<p class="lbl">Empfehlungen</p>{em}</div></div>')


def detail(S, logo, img6, fmt, druck=False):
    H = S["hero"]
    k1 = teil_kopf("01", "Strategie", "Wo willst du wachsen?", "Welche Ziele willst du erreichen – und mit welchen Zielgruppen?")
    k2 = teil_kopf("02", "Marketing und Vertrieb", "Drei Stufen zum Vertriebserfolg.", "Die Maschine arbeitet vor deinem Vertrieb – gemessen wird an Leads.")
    k3 = teil_kopf("03", "Steuerung", "Funktioniert es?", "Das Dashboard misst Landingpages, Postings und Mailings. Daraus folgt, was als Nächstes wirkt.")
    notiz1 = '<p class="notiz">Daraus leitet sich alles Weitere ab: Themen, Landingpages, Kanäle.</p>'
    notiz3 = '<p class="notiz">Abschlüsse liegen im System deiner Agentur – die tracken wir bewusst nicht.</p>'
    gap = None
    if fmt == "a3-quer":
        kopf_ = kopf_hoch(H["kicker"], e(H["h1"]), H["h1_akzent"], H["lead"], logo, br_akzent=False)
        body = (f'<div class="drei-spalten" style="margin-top:10mm">'
                f'<div class="teil">{k1}<div class="teil-inhalt">{pfad(senkrecht=True)}{notiz1}</div></div>'
                f'<div class="teil">{k2}<div class="teil-inhalt">{stufen_teil(S, "76mm" if druck else "64mm")}</div></div>'
                f'<div class="teil">{k3}<div class="teil-inhalt">{dashboard()}{notiz3}</div></div></div>')
    else:
        gap = "19mm" if fmt == "a3-hoch" else "24mm"
        kopf_ = kopf_hoch(H["kicker"], e(H["h1"]) if fmt == "a3-hoch" else "Die digitale<br>Maschine", H["h1_akzent"], H["lead"], logo)
        st = stufen_teil(S, None, quer=True) if fmt == "a3-hoch" else stufen_teil(S, "72mm")
        body = (f'<div class="teil red">{k1}<div class="teil-inhalt">{pfad()}{notiz1}</div></div>'
                f'<div class="teil red" style="margin-top:{gap}">{k2}<div class="teil-inhalt">{st}</div></div>'
                f'<div class="teil red" style="margin-top:{gap}">{k3}<div class="teil-inhalt">{dashboard(flach=True)}{notiz3}</div></div>')
    if druck:  # zum Selbstausdrucken: kein Band, keine Gesichter, keine Kontaktdaten – nur die Adresse unten rechts
        body = body.replace(f' style="margin-top:{gap}"', "") if fmt != "a3-quer" else body.replace('style="margin-top:10mm"', "")
        return kopf_ + f'<div class="verteilt">{body}</div>' + '<p class="fuss-url">sofortsichtbar.de</p>'
    return kopf_ + body + band(S, img6)


def blaetter(S, logo, img6):
    H, M = S["hero"], S["maas"]
    out = {}
    # ---------- Grundstory: die Maschine ----------
    out[("maschine", "a3-quer")] = (
        kopf_hoch(H["kicker"], e(H["h1"]), H["h1_akzent"], H["lead"], logo, br_akzent=False)
        + f'<div class="buehne" style="margin-top:9mm;padding:9mm 16mm 8mm">{S["ek_quer"]}</div>'
        + f'<div style="margin-top:8mm">{schritte(S, mit_bild=False)}</div>'
        + band(S, img6))
    out[("maschine", "a3-hoch")] = (
        kopf_hoch(H["kicker"], e(H["h1"]), H["h1_akzent"], H["lead"], logo)
        + f'<div class="buehne" style="margin-top:16mm;padding:18mm 12mm 16mm">{S["ek_quer"]}</div>'
        + f'<div style="margin-top:26mm">{schritte(S)}</div>'
        + band(S, img6))
    out[("maschine", "rollup")] = (
        kopf_hoch(H["kicker"], "Die digitale<br>Maschine", H["h1_akzent"], H["lead"], logo)
        + f'<div class="buehne" style="margin-top:12mm;padding:10mm 0 8mm">{S["ek_hoch"]}</div>'
        + f'<div style="margin-top:9mm">{schritte(S, mit_bild=False)}</div>'
        + band(S, img6))
    # ---------- Marketing as a Service ----------
    MH = M["held"]
    beleg = f'<p class="zitat">„{e(M["beleg"]["zitat"])}“</p><p class="klein">{e(M["beleg"]["quelle"])}</p>'
    out[("maas", "a3-quer")] = (
        kopf_hoch(MH["kicker"], e(MH["h1"]), MH["h1_akzent"], MH["lead"], logo, br_akzent=False)
        + f'<div style="margin-top:7mm">{gesamtlogik(S)}</div>'
        + '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:14mm;margin-top:9mm">'
        + f'<div class="abschnitt"><h2>Ein Kernpaket. Drei Ergänzungen.</h2><div class="buehne schnitt" style="padding:5mm 6mm">{S["ek_schnitt_quer"]}</div></div>'
        + f'<div class="abschnitt"><h2>{e(M["start"]["h2"])}</h2>{wochen(S, senkrecht=True)}</div></div>'
        + band(S, img6))
    out[("maas", "a3-hoch")] = (
        kopf_hoch(MH["kicker"], e(MH["h1"]), MH["h1_akzent"], MH["lead"], logo)
        + f'<div style="margin-top:8mm">{gesamtlogik(S)}</div>'
        + f'<div class="abschnitt" style="margin-top:8mm"><h2>Ein Kernpaket. Drei Ergänzungen.</h2><div class="buehne schnitt" style="padding:6mm 6mm">{S["ek_schnitt_quer"]}</div></div>'
        + f'<div class="abschnitt" style="margin-top:8mm"><h2>{e(M["start"]["h2"])}</h2>{wochen(S)}</div>'
        + band(S, img6))
    out[("maas", "rollup")] = (
        kopf_hoch(MH["kicker"], "Wir bedienen<br>die Maschine.", MH["h1_akzent"], MH["lead"], logo)
        + f'<div style="margin-top:15mm">{gesamtlogik(S)}</div>'
        + f'<div class="abschnitt" style="margin-top:15mm"><p class="kicker">Was in der Maschine steckt</p><h2>Ein Kernpaket. Drei Ergänzungen.</h2><div class="buehne schnitt" style="padding:9mm 8mm">{S["ek_schnitt_quer"]}</div></div>'
        + f'<div class="abschnitt" style="margin-top:15mm"><p class="kicker">{e(M["start"]["kicker"])}</p><h2>{e(M["start"]["h2"])}</h2>{wochen(S)}</div>'
        + f'<div style="margin-top:15mm">{beleg}</div>'
        + band(S, img6))
    for fmt in FORMATE:
        out[("maschine-ausfuehrlich", fmt)] = detail(S, logo, img6, fmt)
    for fmt in ("a3-quer", "a3-hoch"):
        out[("maschine-ausfuehrlich-druck", fmt)] = detail(S, logo, img6, fmt, druck=True)
    return out


def main():
    S = json.load(open(D7, encoding="utf-8"))["s7"]
    img6 = os.path.join(SRC, "entwicklung", "storyboard", "story6", "assets", "img")
    logo = f'file://{img6}/logo-dunkel.svg'
    os.makedirs(ZIEL, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="op7_")
    for (g, fmt), inhalt in blaetter(S, logo, img6).items():
        name = f"{g}-{fmt}"
        h = os.path.join(tmp, name + ".html")
        open(h, "w", encoding="utf-8").write(
            f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{css(fmt)}</style></head><body>{SVG_CSS}{VERLAUF_H}'
            f'<div class="blatt {fmt}{" kurz" if (g, fmt) == ("maschine-ausfuehrlich", "a3-hoch") else ""}{" druck" if g.endswith("-druck") else ""}">{inhalt}</div>{VERLAUF_JS}</body></html>')
        pdf = os.path.join(ZIEL, name + ".pdf")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                        "--virtual-time-budget=6000", f"--print-to-pdf={pdf}", "file://" + h], check=True, capture_output=True)
        subprocess.run(["pdftoppm", "-r", "40", "-scale-to", "1600", "-png", "-singlefile", pdf, os.path.join(ZIEL, name)], check=True)
        print(name, subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout.split("Page size:")[1].split("\n")[0].strip())
    print("HTML:", tmp)


if __name__ == "__main__":
    main()
