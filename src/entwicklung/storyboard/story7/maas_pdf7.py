#!/usr/bin/env python3
"""PDF „Marketing as a Service“ im Look von Homepage-Story 7 (Daniel, 12.11.2026: Seitenfolge freigegeben).

SCHRIFTSYSTEM (fest, vor dem Bauen festgelegt – Vorbild ist die Website Story 7, nicht empiria):
  Inter Tight 700  – Überschriften in genau zwei Größen: H1 44 pt (Deckblatt und Kontakt), H2 22 pt (alle übrigen Seiten, auch große Zahlen und Posting-Titel)
  Inter 400/600    – Text 10 pt (Regular, Hervorhebung SemiBold); Klein 8 pt für Kicker, Nebeninfos, Fußzeile
  Farben           – Tinte #1d1d1f, Grau #6e6e73; Verlauf Cyan → Violett höchstens einmal je Seite (ein Wort der Überschrift oder eine Fläche).
                     Ausnahme Stellenanzeigen: Sie zeigen, wie der Kunde postet (Entwürfe in seinem Namen) – dort kräftige Verläufe in
                     Cyan, Violett und Magenta und eine eigene Titelgröße im Posting-Bild (16 pt), wie bei einem echten Social-Media-Motiv.

Seitenfolge: Deckblatt · Die Maschine · 30-Tage-Plan (mit „danach jeden Monat“) · Bausteine · Bausteine im Detail ·
             Team · Lieber selbst einstellen? · Stellenbeschreibungen · Stellenanzeigen · Kontakt
Inhalte: story7.11tydata.json (s7) und story6.11tydata.json (maas: Profile, Monatsablauf) – dieselben Quellen wie die Website.
Grafiken: s7.ek_quer (Erklärbild), s7.ek_schnitt_quer (Schnitt durch die Maschine) – dieselben wie auf der Website.

Aufruf:  python3 src/entwicklung/storyboard/story7/maas_pdf7.py
Ergebnis: story7/assets/maas/marketing-as-a-service.pdf, -1.png/-2.png (Vorschau Download), Seitenzahl/Größe in s7.maas.download
"""
import html
import json
import os
import re
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
D7 = os.path.join(HERE, "story7.11tydata.json")
D6 = os.path.join(HERE, "..", "story6", "story6.11tydata.json")
ZIEL = os.path.join(HERE, "assets", "maas")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

e = html.escape
LEAD = [("qualifizierte Anfragen", "qualifizierte Leads"), ("Alle Anfragen", "Alle Leads"), ("Anfragen kommen", "Leads kommen")]


def lead(s):
    for a, b in LEAD:
        s = s.replace(a, b)
    return s


def grad(s):
    return f'<span class="v">{s}</span>'


def seite(inhalt, klasse=""):
    return f'<section class="seite {klasse}">{inhalt}</section>'


def kopf(kicker, h2):
    return f'<p class="kicker">{e(kicker)}</p><h2>{h2}</h2>'


def css():
    f = os.path.join(HERE, "assets", "fonts")
    faces = ""
    for fam, datei, w in [("Inter", "inter", 400), ("Inter", "inter", 600), ("Inter Tight", "inter-tight", 700)]:
        for sub in ("latin", "latin-ext"):
            faces += f'@font-face{{font-family:"{fam}";font-weight:{w};src:url("file://{f}/{datei}-{sub}-{w}-normal.woff2") format("woff2");}}\n'
    return faces + r'''
@page { size: A4; margin: 18mm 18mm 20mm;
  @bottom-left { content: "sofort sichtbar · Marketing as a Service"; font: 600 8pt "Inter"; color: #6e6e73; }
  @bottom-right { content: counter(page); font: 600 8pt "Inter"; color: #6e6e73; } }
@page voll { margin: 0; @bottom-left { content: none; } @bottom-right { content: none; } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; color: #1d1d1f; font: 400 10pt/1.5 "Inter"; }
p { margin: 0; }
b, strong { font-weight: 600; }
h1, h2, h3 { margin: 0; font-family: "Inter Tight"; font-weight: 700; letter-spacing: -0.02em; color: #1d1d1f; }
h1 { font-size: 44pt; line-height: 1.02; }
h2 { font-size: 22pt; line-height: 1.1; }
h3 { font-family: "Inter"; font-weight: 600; font-size: 10pt; letter-spacing: 0; }
.v { color: #0b9fbd; } /* wird vor dem Drucken durch SVG-Text mit Verlauf ersetzt (Hintergrund-Clip erzeugt im PDF Kanten) */
svg.vs { display: inline-block; overflow: visible; }
.kicker { margin-bottom: 3mm; color: #6e6e73; font-size: 8pt; font-weight: 600; }
.klein { color: #6e6e73; font-size: 8pt; }
.grau { color: #6e6e73; }
.lead { margin-top: 4mm; max-width: 150mm; }
.seite { break-before: page; }
.seite:first-child { break-before: auto; }
.voll { page: voll; position: relative; width: 210mm; height: 297mm; overflow: hidden; padding: 18mm; }
.dunkel { background: #1d1d1f; color: #d2d2d7; }
.dunkel h1, .dunkel h2, .dunkel h3 { color: #fff; }
.dunkel .kicker, .dunkel .klein { color: #a1a1a6; }
.buehne { margin-top: 7mm; padding: 7mm 6mm; border-radius: 5mm; background: #f5f5f7; }
.buehne svg { display: block; width: 100%; height: auto; overflow: visible; }
.logo { height: 11mm; }
.zeile { break-inside: avoid; }
.trenn { border-top: 0.3mm solid #e5e5ea; }

/* Deckblatt */
.deck h1 { margin-top: 30mm; }
.deck .lead { margin-top: 6mm; }
.deck .buehne { margin-top: 14mm; }
.fakten { position: absolute; left: 18mm; right: 18mm; bottom: 18mm; display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; padding-top: 5mm; border-top: 0.3mm solid #1d1d1f; }
.fakten b { display: block; font-family: "Inter Tight"; font-weight: 700; font-size: 22pt; letter-spacing: -0.02em; line-height: 1.1; }

/* Maschine */
.drei { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; margin-top: 8mm; }
.drei > div { padding-top: 3mm; border-top: 0.6mm solid #1d1d1f; }
.drei h3 { margin-bottom: 1.5mm; }

/* 30-Tage-Plan */
.wochen { margin-top: 6mm; }
.woche { display: grid; grid-template-columns: 22mm 1fr; gap: 6mm; padding: 3.5mm 0; border-top: 0.3mm solid #e5e5ea; break-inside: avoid; }
.woche:last-child { border-bottom: 0.3mm solid #e5e5ea; }
.woche .w { font-family: "Inter Tight"; font-weight: 700; font-size: 22pt; letter-spacing: -0.02em; line-height: 1; }
.woche h3 { margin-bottom: 1mm; }
.kasten { margin-top: 6mm; padding: 5mm 6mm; border-radius: 4mm; background: #f5f5f7; break-inside: avoid; }
.kasten h3 { margin-bottom: 2mm; }
.haken { margin: 0; padding: 0; list-style: none; }
.haken li { position: relative; padding: 1.2mm 0 1.2mm 6mm; }
.haken li::before { content: ""; position: absolute; left: .5mm; top: 2.6mm; width: 2.6mm; height: 1.3mm; border-left: 0.5mm solid currentColor; border-bottom: 0.5mm solid currentColor; transform: rotate(-45deg); }

/* Monat */
.vier { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; margin-top: 4mm; }
.vier > div { padding: 4.5mm; border-radius: 4mm; background: #f5f5f7; break-inside: avoid; }
.vier .nr { display: block; margin-bottom: 3mm; color: #6e6e73; font-size: 8pt; font-weight: 600; }
.vier h3 { margin-bottom: 1.5mm; }

/* Bausteine */
.basis { margin-top: 8mm; padding: 8mm; border-radius: 5mm; background: linear-gradient(140deg, #0b9fbd, #8613a1); color: #fff; break-inside: avoid; }
.basis h3, .basis .kicker { color: #fff; }
.basis .preis b { font-family: "Inter Tight"; font-weight: 700; font-size: 22pt; letter-spacing: -0.02em; }
.basis .gr { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; margin-top: 5mm; padding-top: 4mm; border-top: 0.3mm solid rgba(255,255,255,.35); }
.erg { display: grid; grid-template-columns: 1fr auto; gap: 2mm 8mm; padding: 5mm 0; border-bottom: 0.3mm solid #e5e5ea; break-inside: avoid; }
.erg .preis { text-align: right; }
.erg .preis b { display: block; font-family: "Inter Tight"; font-weight: 700; font-size: 22pt; letter-spacing: -0.02em; line-height: 1.1; white-space: nowrap; }
.erg-kopf { margin-top: 8mm; padding-bottom: 2mm; border-bottom: 0.6mm solid #1d1d1f; }

/* Detail */
.meta { margin-top: 2mm; color: #6e6e73; }
.gruppe { margin-top: 6mm; padding-bottom: 2mm; border-bottom: 0.6mm solid #1d1d1f; font-weight: 600; }
.leistung { padding: 2.4mm 0; border-bottom: 0.3mm solid #e5e5ea; break-inside: avoid; }
.leistung h3 { margin-bottom: 1mm; }
.leistung ul { margin: 1.5mm 0 0; padding-left: 5mm; }
.leistung li { margin: .3mm 0; }
.hinweis { margin-top: 5mm; color: #6e6e73; font-size: 8pt; }

/* Team */
.profile { margin-top: 8mm; }
.profil { display: grid; grid-template-columns: 52mm 1fr; gap: 6mm; padding: 4.5mm 0; border-top: 0.3mm solid #e5e5ea; break-inside: avoid; }
.profil:last-child { border-bottom: 0.3mm solid #e5e5ea; }
.gruppe-team { margin-top: 7mm; padding-bottom: 2mm; color: #6e6e73; font-size: 8pt; font-weight: 600; }
.immer { display: flex; flex-wrap: wrap; gap: 3mm; margin-top: 8mm; }
.immer span { padding: 1.6mm 4mm; border: 0.3mm solid #1d1d1f; border-radius: 10mm; font-weight: 600; }

/* Stellen */
.stelle-teil { margin-top: 6mm; break-inside: avoid; }
.stelle-teil ul { margin: 2mm 0 0; padding-left: 5mm; }
.stelle-teil li { margin: .8mm 0; }

/* Anzeigen */
.anzeige { display: grid; grid-template-columns: 62mm 1fr; gap: 7mm; margin-top: 7mm; break-inside: avoid; }
.anz-bild { display: flex; flex-direction: column; justify-content: space-between; aspect-ratio: 1; padding: 6mm; border-radius: 4mm; background: #1d1d1f; color: #fff; }
.anz-bild b { font-family: "Inter Tight"; font-weight: 700; font-size: 22pt; line-height: 1.05; letter-spacing: -0.02em; }
.anz-bild .klein { color: #d2d2d7; }
.anzeige h3 { margin-bottom: 2mm; }
.anzeige p + p { margin-top: 2mm; }

/* Kontakt */
.kontakt h2 { margin-top: 0; }
.gesichter { display: flex; align-items: center; gap: 5mm; margin-top: 12mm; color: #fff; font-weight: 600; }
.gesichter span { display: flex; }
.gesichter img { width: 16mm; height: 16mm; border: 0.8mm solid #1d1d1f; border-radius: 50%; object-fit: cover; }
.gesichter img + img { margin-left: -4mm; }
.wege { position: absolute; left: 18mm; right: 18mm; bottom: 24mm; display: grid; gap: 2mm; padding-top: 6mm; border-top: 0.3mm solid #3a3a3c; }
.wege b { color: #fff; font-family: "Inter Tight"; font-weight: 700; font-size: 22pt; letter-spacing: -0.02em; line-height: 1.15; }

/* ===== v2 (12.11.2026) ===== */
/* Deckblatt: vollflächig im Verlauf */
.cover { background: linear-gradient(150deg, #0b9fbd 0%, #3f4fb5 55%, #8613a1 100%); color: #fff; }
.cover .logo { height: 12mm; }
.cover h1 { position: absolute; left: 18mm; right: 18mm; bottom: 74mm; color: #fff; }
.cover .unter { position: absolute; left: 18mm; right: 40mm; bottom: 52mm; font-size: 10pt; color: rgba(255,255,255,.9); }
.cover .fuss { position: absolute; left: 18mm; right: 18mm; bottom: 18mm; display: flex; justify-content: space-between; padding-top: 4mm; border-top: 0.3mm solid rgba(255,255,255,.5); font-size: 8pt; font-weight: 600; color: rgba(255,255,255,.9); }
.cover .gross { position: absolute; right: -40mm; top: 30mm; width: 170mm; height: 170mm; border-radius: 50%; border: 0.4mm solid rgba(255,255,255,.35); }
.cover .gross + .gross { right: -10mm; top: 60mm; width: 110mm; height: 110mm; }
/* Grundgrafik (wie Website): Klammer, drei Spalten, Rücklauf */
.gg { margin-top: 7mm; padding: 6mm; border-radius: 5mm; background: #f5f5f7; }
.gg-klammer { padding-bottom: 2.5mm; border-bottom: 0.5mm solid #1d1d1f; font-weight: 600; }
.gg-spalten { display: grid; grid-template-columns: repeat(3, 1fr); gap: 7mm; margin-top: 5mm; }
.gg-titel { display: flex; align-items: center; gap: 2mm; font-weight: 600; }
.gg-titel span { display: inline-grid; place-items: center; width: 5mm; height: 5mm; border-radius: 50%; background: #1d1d1f; color: #fff; font-size: 8pt; }
.gg-sub { margin-top: 1mm; color: #6e6e73; font-size: 8pt; }
.gg-inhalt { display: grid; align-content: center; gap: 1.6mm; min-height: 42mm; margin-top: 3mm; padding: 3.5mm; border-radius: 3mm; background: #fff; }
.chip { justify-self: start; padding: 1mm 2.6mm; border: 0.3mm solid #e5e5ea; border-radius: 4mm; font-size: 8pt; line-height: 1.35; }
.chip.an { border-color: #1d1d1f; background: #1d1d1f; color: #fff; font-weight: 600; }
.chip.mehr { border-style: dashed; color: #6e6e73; }
.kacheln { display: grid; grid-template-columns: 1fr 1fr; gap: 1.6mm; }
.kacheln > div { padding: 1.6mm 2mm; border: 0.3mm solid #e5e5ea; border-radius: 1.6mm; font-size: 8pt; font-weight: 600; }
.kacheln svg { display: block; width: 100%; height: 3.5mm; margin-top: 1mm; fill: none; stroke: #1d1d1f; stroke-width: 1.4; }
.empf { padding: 1.6mm 2mm; border: 0.3mm solid #e5e5ea; border-radius: 1.6mm; font-size: 8pt; line-height: 1.35; }
.gg-zurueck { position: relative; height: 7mm; margin: 2mm 16% 0; border: 0.5mm solid #1d1d1f; border-top: 0; border-radius: 0 0 3mm 3mm; }
.gg-zurueck span { position: absolute; left: 50%; bottom: 0; transform: translate(-50%, 50%); padding: 0 3mm; background: #f5f5f7; font-size: 8pt; font-weight: 600; white-space: nowrap; }
.gg-trichter svg { display: block; width: 100%; height: auto; }
.gg-trichter p { margin-top: 1mm; font-size: 8pt; font-weight: 600; text-align: right; }
/* Detailgrafik (nach Infografik) */
.teil { display: grid; grid-template-columns: 16mm 1fr; gap: 4mm; margin-top: 6mm; padding-top: 4mm; border-top: 0.6mm solid #1d1d1f; break-inside: avoid; }
.teil .nr { font-family: "Inter Tight"; font-weight: 700; font-size: 22pt; line-height: 1; }
.teil h3 { margin-bottom: .8mm; }
.reihe { display: flex; align-items: center; gap: 2.5mm; margin-top: 3mm; flex-wrap: wrap; }
.reihe .lbl { width: 100%; color: #6e6e73; font-size: 8pt; font-weight: 600; }
.reihe .pf { color: #1d1d1f; font-size: 14pt; line-height: 1; }
.teil .buehne { margin-top: 3mm; padding: 4mm; }
/* Baustein-Seiten */
.bs-kopf { display: grid; grid-template-columns: 1fr auto; gap: 6mm; align-items: end; }
.bs-preis { text-align: right; }
.bs-preis b { display: block; font-family: "Inter Tight"; font-weight: 700; font-size: 22pt; letter-spacing: -0.02em; line-height: 1; }
.bs-bild { height: 40mm; margin-top: 6mm; border-radius: 5mm; background: #f5f5f7; overflow: hidden; display: flex; align-items: flex-end; justify-content: center; }
.bs-bild .anzeige-mock { align-self: center; margin: 0; }
.bs-bild img { display: block; width: 92%; height: auto; margin-bottom: -6mm; }
.bs-bild--flach { height: 24mm; }
.bs-intro { column-count: 2; column-gap: 8mm; margin-top: 6mm; }
.bs-intro p + p { margin-top: 2mm; }
.bs-gruppe { margin-top: 6mm; padding-bottom: 2mm; border-bottom: 0.6mm solid #1d1d1f; font-weight: 600; }
.bs-liste { display: grid; grid-template-columns: 1fr 1fr; gap: 0 8mm; }
.bs-liste .leistung { border-bottom: 0.3mm solid #e5e5ea; }
.anzeige-mock { width: 110mm; padding: 4mm; border-radius: 4mm; background: #fff; box-shadow: 0 2mm 6mm rgba(0,0,0,.12); margin-bottom: 8mm; }
.anzeige-mock .bild { height: 16mm; border-radius: 2.5mm; background: linear-gradient(120deg, #0b9fbd, #8613a1); }
.anzeige-mock b { display: block; margin-top: 3mm; font-size: 10pt; }
.anzeige-mock .knopf { display: inline-block; margin-top: 2mm; padding: 1.2mm 3.5mm; border-radius: 4mm; background: #1d1d1f; color: #fff; font-size: 8pt; font-weight: 600; }
/* Stellenbeschreibung mit Profilkarte */
.stelle { display: grid; grid-template-columns: 1fr 74mm; gap: 8mm; margin-top: 6mm; }
.profilkarte { align-self: start; padding: 6mm; border-radius: 4mm; background: linear-gradient(150deg, #0b9fbd, #8613a1); color: #fff; }
.profilkarte h3, .profilkarte .kicker { color: #fff; }
.profilkarte .kicker { opacity: .85; }
.profilkarte .gross { display: block; margin: 2mm 0 4mm; hyphens: manual; font-family: "Inter Tight"; font-weight: 700; font-size: 22pt; line-height: 1.05; letter-spacing: -0.02em; }
.profilkarte p + p { margin-top: 3mm; }
.stelle .stelle-teil:first-child { margin-top: 0; }
/* Stellenanzeigen als echte Postings */
.post { display: grid; grid-template-columns: 54mm 1fr; gap: 7mm; margin-top: 5mm; break-inside: avoid; }
.post-karte { border: 0.3mm solid #e5e5ea; border-radius: 3mm; overflow: hidden; background: #fff; }
.post-kopf { display: flex; align-items: center; gap: 2mm; padding: 2.4mm 3mm; font-size: 8pt; }
.post-kopf i { width: 6mm; height: 6mm; border-radius: 50%; background: #1d1d1f; }
.post-kopf b { display: block; }
.post-kopf span { color: #6e6e73; }
.post-bild { position: relative; aspect-ratio: 1; overflow: hidden; padding: 4mm; color: #fff; display: flex; flex-direction: column; justify-content: space-between; }
.post-bild .badge { align-self: flex-start; padding: 1mm 3mm; border-radius: 4mm; background: #fff; color: #1d1d1f; font-size: 8pt; font-weight: 600; position: relative; z-index: 1; }
.post-bild b { position: relative; z-index: 1; font-family: "Inter Tight"; font-weight: 700; font-size: 16pt; hyphens: manual; line-height: 1.02; letter-spacing: -0.02em; }
.post-bild .sub { position: relative; z-index: 1; font-size: 8pt; font-weight: 600; }
.post-bild .kreis { position: absolute; border-radius: 50%; }
.post-fuss { display: flex; gap: 5mm; white-space: nowrap; padding: 2.4mm 3mm; border-top: 0.3mm solid #e5e5ea; color: #6e6e73; font-size: 8pt; font-weight: 600; }
.p1 { background: linear-gradient(150deg, #0b9fbd, #8613a1); }
.p2 { background: linear-gradient(150deg, #c51f5d, #8613a1); }
.p3 { background: #8613a1; }
.p4 { background: #0b9fbd; }
.p5 { background: linear-gradient(150deg, #8613a1, #c51f5d); }
.p1 .kreis, .p4 .kreis { right: -18mm; top: -18mm; width: 60mm; height: 60mm; background: rgba(255,255,255,.16); }
.p2 .kreis, .p5 .kreis { left: -14mm; bottom: -22mm; width: 64mm; height: 64mm; background: rgba(255,255,255,.14); }
.p3 .kreis { right: 8mm; top: 8mm; width: 30mm; height: 30mm; background: #c51f5d; }
.post-text h3 { margin-bottom: 2mm; }
.post-text p + p { margin-top: 2mm; }
.post-text .tags { margin-top: 3mm; color: #0b9fbd; font-weight: 600; }
'''


SVG_CSS = '''<style>
.ek2 text, svg text { font-family: "Inter"; }
.ek2-t { fill: #1d1d1f; } .ek2-grau { fill: #6e6e73; }
.ek2-lage { stroke: #f5f5f7; stroke-width: 2; }
.ek2-l2 { fill: #d5d5db; } .ek2-l3 { fill: #e1e1e6; } .ek2-l4 { fill: #ececf0; }
.ek2-kern { fill: url(#s7v-cyanviolett); }
.ek2-kern-t, .ek2-kern-p { fill: #ffffff; }
.ek2-band { fill: #1d1d1f; } .ek2-band-t { fill: #fff; } .ek2-band-s { fill: #a1a1a6; }
.ek2-linie { fill: none; stroke: #1d1d1f; stroke-width: 2; } .ek2-linie--fein { stroke-width: 1.4; }
.ek2-pfeilkopf { fill: none; stroke: #1d1d1f; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.ek2-grund { fill: #f5f5f7; }
.ek2-svg--hoch { display: none; }
</style>
<svg width="0" height="0" style="position:absolute"><defs><linearGradient id="s7v-cyanviolett" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient></defs></svg>'''


# Verlaufswörter als SVG-Text: Chrome druckt background-clip:text als Fläche mit Textmaske – PDF-Betrachter zeigen deren Kanten.
VERLAUF_JS = """<script>
document.fonts.ready.then(() => { document.querySelectorAll('.v').forEach((s, n) => {
  const r = s.getBoundingClientRect(), cs = getComputedStyle(s), fs = parseFloat(cs.fontSize), ns = 'http://www.w3.org/2000/svg';
  const sv = document.createElementNS(ns, 'svg');
  sv.setAttribute('class', 'vs'); sv.setAttribute('width', r.width); sv.setAttribute('height', fs);
  sv.style.marginBottom = (-fs * 0.22) + 'px';
  sv.innerHTML = '<defs><linearGradient id="vg' + n + '" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="' + r.width + '" y2="0">'
    + '<stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient></defs>';
  const t = document.createElementNS(ns, 'text');
  t.setAttribute('x', 0); t.setAttribute('y', fs * 0.78); t.setAttribute('fill', 'url(#vg' + n + ')');
  t.style.font = cs.font; t.style.letterSpacing = cs.letterSpacing; t.textContent = s.textContent;
  sv.appendChild(t); s.replaceWith(sv);
}); });
</script>"""


def bauen():
    d7 = json.load(open(D7, encoding="utf-8"))
    S = d7["s7"]
    M6 = json.load(open(D6, encoding="utf-8"))["maas"]
    M = S["maas"]
    img6 = os.path.join(SRC, "entwicklung", "storyboard", "story6", "assets", "img")
    imgL = os.path.join(SRC, "assets", "img")
    logo = f'file://{img6}/logo-dunkel.svg'
    logo_hell = f'file://{imgL}/logos/logo-white.svg'
    spark_auf = '<svg viewBox="0 0 60 16" preserveAspectRatio="none"><polyline points="0,13 12,11 24,12 36,8 48,6 60,3"/></svg>'
    spark_ab = '<svg viewBox="0 0 60 16" preserveAspectRatio="none"><polyline points="0,4 12,5 24,4 36,8 48,10 60,13"/></svg>'
    s = []

    # 1 · Deckblatt – vollflächig, schlicht
    s.append(seite(
        f'<img class="logo" src="{logo_hell}" alt="sofort sichtbar">'
        '<h1>Marketing<br>as a Service.</h1>'
        '<p class="unter">Deine strategische Marketingabteilung – für Versicherungsagenturen und Maklerbüros.</p>'
        '<div class="fuss"><span>sofort sichtbar</span><span>Angebot und Leistungen</span></div>', "voll cover"))

    # 2 · Grundgrafik (wie Website-Kopf)
    KP = M["kopf"]
    sp = KP["spalten"]
    fragen = "".join(f'<span class="chip">„{e(f)}“</span>' for f in KP["fragen"])
    kacheln = (f'<div class="kacheln"><div>Aufmerksamkeit{spark_auf}</div><div>Verweildauer{spark_ab}</div>'
               f'<div>Google{spark_auf}</div><div>Leads{spark_auf}</div></div><div class="empf"><b>Empfehlung:</b> {e(KP["empf"])}</div>')
    spalten = ""
    for k, inhalt in ((0, fragen), (1, f'<div class="gg-trichter">{S["ek_kopf_trichter"]}<p>{e(KP["leads"])}</p></div>'), (2, kacheln)):
        spalten += (f'<div><p class="gg-titel"><span>{sp[k]["nr"]}</span>{e(sp[k]["titel"])}</p><p class="gg-sub">{e(sp[k]["sub"])}</p>'
                    f'<div class="gg-inhalt">{inhalt}</div></div>')
    s.append(seite(
        kopf("Das Prinzip", f'{e(M["held"]["h1"])}<br>{grad(e(M["held"]["h1_akzent"]))}')
        + f'<p class="lead">{e(M["held"]["lead"])}</p>'
        + f'<div class="gg"><p class="gg-klammer">{e(KP["klammer"])}</p><div class="gg-spalten">{spalten}</div>'
        + f'<p class="gg-zurueck"><span>{e(KP["zurueck"])}</span></p></div>'
        + '<div class="drei">'
        '<div><h3>Du gibst Verantwortung ab</h3><p>Wir denken an alles, was mit deinem Marketing zusammenhängt – auch an Aktionen deines Versicherers und eigene Mailings.</p></div>'
        '<div><h3>Du bekommst Leads</h3><p>Jeder Lead landet direkt bei dir und ist im Dashboard messbar.</p></div>'
        '<div><h3>Du entscheidest mit</h3><p>Einmal im Monat legen wir gemeinsam fest, was als Nächstes zählt.</p></div>'
        '</div>'))

    # 3 · Die drei Teile im Detail (nach Infografik)
    def chips(liste, an=()):
        return "".join(f'<span class="chip{" an" if x in an else ""}{" mehr" if x.startswith("+") else ""}">{e(x)}</span>' for x in liste)
    s.append(seite(
        kopf("Im Detail", f'Was in deiner {grad("Marketingabteilung")} passiert.')
        + '<div class="teil"><span class="nr">01</span><div><h3>Wir fragen: Wo willst du wachsen?</h3>'
        '<p>Zum Start und in jedem monatlichen Call. Daraus folgen die Zielgruppen – und damit die Pakete, die wirklich zu dir passen.</p>'
        f'<div class="reihe"><span class="lbl">Segment › Sparte › Zielgruppe</span>{chips(["Privatkunden", "Firmenkunden"], ["Privatkunden"])}<span class="pf">›</span>'
        f'{chips(["Leben", "Kranken", "Schaden/Unfall", "Kfz"], ["Leben"])}<span class="pf">›</span>'
        f'{chips(["Junge Familien", "Private Bauherren", "Berufseinsteiger", "+ weitere"], ["Junge Familien", "Private Bauherren"])}</div>'
        f'<div class="reihe"><span class="lbl">Und was läuft sonst bei dir?</span>{chips(["Mailing-Aktion im Bestand", "Aktion deines Versicherers", "Termine und Veranstaltungen", "Schwerpunkte im Team"])}</div>'
        '</div></div>'
        + f'<div class="teil"><span class="nr">02</span><div><h3>Wir setzen um: Die Maschine vor deinem Vertrieb</h3>'
        '<p>Landingpages, Postings und Kundenmailings je Zielgruppe – Leads landen direkt in deinem Vertrieb.</p>'
        f'<div class="buehne">{S["ek_quer"]}</div></div></div>'
        + f'<div class="teil"><span class="nr">03</span><div><h3>Wir werten aus: Funktioniert es?</h3>'
        '<p>Jeden Monat im Report und im Betreuungscall – mit konkreten Empfehlungen.</p>'
        f'<div class="kacheln" style="grid-template-columns:repeat(4,1fr);margin-top:3mm"><div>Aufmerksamkeit{spark_auf}</div><div>Verweildauer{spark_ab}</div><div>Google{spark_auf}</div><div>Leads{spark_auf}</div></div>'
        '<div class="kacheln" style="grid-template-columns:repeat(3,1fr);margin-top:1.6mm">'
        '<div class="empf" style="font-weight:400"><b>Landingpage</b><br>Abschnitt umstellen, der kaum gelesen wird</div>'
        '<div class="empf" style="font-weight:400"><b>LinkedIn</b><br>Thema verstärken, das Leads bringt</div>'
        '<div class="empf" style="font-weight:400"><b>Google</b><br>Seite für einen gesuchten Begriff ausbauen</div></div>'
        '<p class="hinweis">Empfehlungen setzen wir um und prüfen sie nach acht Wochen nach.</p></div></div>'))

    # 4 · 30-Tage-Plan mit „danach jeden Monat“
    ST = M["start"]
    wochen = "".join(f'<div class="woche"><div><span class="w">{e(x["wann"].replace("Woche ", ""))}</span><p class="klein">Woche</p></div>'
                     f'<div><h3>{e(x["titel"])}</h3><p>{e(x["text"])}</p></div></div>' for x in ST["liste"])
    vier = "".join(f'<div><span class="nr">0{i + 1}</span><h3>{e(a["titel"])}</h3><p>{e(lead(a["text"]))}</p></div>' for i, a in enumerate(M6["ablauf"]))
    s.append(seite(
        kopf(ST["kicker"], f'Der {grad("30-Tage-Plan.")}')
        + f'<p class="lead">{e(ST["lead"])}</p><div class="wochen">{wochen}</div>'
        + f'<div class="kasten"><h3>{e(ST["aufwand_titel"])}</h3><ul class="haken">' + "".join(f"<li>{e(x)}</li>" for x in ST["aufwand"]) + '</ul></div>'
        + f'<p class="gruppe" style="margin-top:9mm">Danach: jeden Monat ein Stück besser</p><div class="vier">{vier}</div>'))

    # 5 · Bausteine und Preise
    BS = M["bausteine"]
    K = BS["liste"][0]
    gr = "".join(f'<div><h3>{e(g["titel"])}</h3><ul class="haken">' + "".join(f"<li>{e(x)}</li>" for x in g["punkte"]) + '</ul></div>' for g in K["gruppen"])
    erg = "".join(
        f'<div class="erg"><div><h3>{e(b["name"])}</h3><p>{e(b["kurz"])}</p><p class="klein" style="margin-top:1.5mm">{e(" · ".join(b["punkte"]))}</p></div>'
        f'<div class="preis"><b>{e(b["preis"])}</b><span class="klein">{e(b["einheit"])}</span>'
        + (f'<br><span class="klein">{e(b["zusatz"])}</span>' if b["zusatz"] else "") + '</div></div>'
        for b in BS["liste"][1:])
    s.append(seite(
        kopf(BS["kicker"], "Ein Kernpaket. Drei Ergänzungen.")
        + f'<p class="lead">{e(BS["lead"])}</p>'
        + f'<div class="basis"><p class="kicker">{e(BS["basis"])}</p><h3 style="font-size:10pt">Kernpaket „{e(K["name"])}“</h3>'
        + f'<p class="preis"><b>{e(K["preis"])}</b> {e(K["einheit"])}</p><p style="margin-top:2mm">{e(K["kurz"])}</p><div class="gr">{gr}</div></div>'
        + f'<p class="erg-kopf"><b>{e(BS["dazu"])}</b></p>{erg}'
        + f'<p class="hinweis">{e(BS["hinweis"])}</p>'))

    # 6 · Bausteine im Detail: Bildfläche, Preis groß, Leistungen in zwei Spalten
    bilder = {"kern": f'<img src="file://{imgL}/pages/vertriebsstrecken-hero-2.webp" alt="">',
              "linkedin": f'<img src="file://{imgL}/preview-postings.png" alt="" style="width:78%">',
              "website": f'<img src="file://{imgL}/preview-landingpages.png" alt="" style="width:80%">',
              "paid-ads": '<div class="anzeige-mock"><div class="bild"></div><b>Gut abgesichert ins Familienleben</b>'
                          '<span class="klein">Gesponsert · In 30 Minuten wissen, was wirklich wichtig ist.</span><br><span class="knopf">Mehr erfahren</span></div>'}
    for i, b in enumerate(BS["liste"]):
        F = b["fenster"]
        teile = ""
        for g in F["gruppen"]:
            teile += f'<p class="bs-gruppe">{e(g["label"])}</p><div class="bs-liste">'
            for l in g["leistungen"]:
                teile += (f'<div class="leistung"><h3>{e(l["titel"])}</h3>' + (f'<p>{e(l["text"])}</p>' if l.get("text") else "")
                          + ("<ul>" + "".join(f"<li>{e(x)}</li>" for x in l["liste"]) + "</ul>" if l.get("liste") else "") + "</div>")
            teile += "</div>"
        name = F["titel"].replace("Kernpaket „sofort sichtbar“", "Kernpaket sofort sichtbar")
        s.append(seite(
            '<div class="bs-kopf"><div>' + kopf("Baustein 0%d · %s" % (i + 1, b["art"]), e(name)) + '</div>'
            f'<div class="bs-preis"><b>{e(b["preis"])}</b><span class="klein">{e(b["einheit"])}</span>'
            + (f'<br><span class="klein">{e(b["zusatz"])}</span>' if b["zusatz"] else "") + '</div></div>'
            + f'<div class="bs-bild{" bs-bild--flach" if i == 0 else ""}">{bilder[b["id"]]}</div>'
            + '<div class="bs-intro">' + "".join(f'<p>{e(x)}</p>' for x in F["intro"]) + '</div>' + teile
            + (f'<p class="hinweis">{e(F["hinweis"])}</p>' if F.get("hinweis") else "")))

    # 7 · Team
    PR = M6["profile"]
    zeilen = lambda gr: "".join(f'<div class="profil"><div><h3>{e(x["klartext"])}</h3><p class="klein">{e(x["stelle"])}</p></div><p>{e(x["denkweise"])}</p></div>'
                                for x in PR["liste"] if (x["gruppe"] == "kern") == gr)
    s.append(seite(
        kopf("Dein Team", f'Fünf Profile. {grad("Ein Team.")}')
        + f'<p class="lead">{e(PR["lead"])}</p>'
        + f'<p class="gruppe-team">Im Kernpaket</p><div>{zeilen(True)}</div><p class="gruppe-team">Mit Paid Ads</p><div>{zeilen(False)}</div>'
        + '<div class="immer">' + "".join(f"<span>{e(x)}</span>" for x in M6["immer"]) + '</div>'))

    # 8 · Lieber selbst einstellen?
    verz = "".join(f'<div class="profil"><div><h3>{e(x["stelle"])}</h3><p class="klein">{e(x["klartext"])}</p></div><p>Stellenbeschreibung und fertige Anzeige</p></div>' for x in PR["liste"])
    s.append(seite(
        kopf("Zum Selbermachen", f'Lieber selbst {grad("einstellen?")}')
        + '<p class="lead">Du willst die Profile lieber selbst besetzen? Auf den nächsten Seiten stehen alle fünf Stellenbeschreibungen – und fertige Anzeigen für LinkedIn, die Karriereseite oder Social Media.</p>'
        + f'<div class="profile">{verz}</div>'))

    # 9 · Stellenbeschreibungen mit Profilkarte
    for i, x in enumerate(PR["liste"]):
        wo = "Im Kernpaket" if x["gruppe"] == "kern" else "Mit Paid Ads"
        teile = "".join(f'<div class="stelle-teil"><p class="gruppe">{t2}</p><ul>' + "".join(f"<li>{e(y)}</li>" for y in liste) + '</ul></div>'
                        for t2, liste in (("Aufgaben", x["aufgaben"]), ("Anforderungen", x["anforderungen"]), ("Ausbildung und Erfahrung", x["ausbildung"])))
        karte = (f'<div class="profilkarte"><p class="kicker">{e(wo)}</p><span class="gross">{e(x["klartext"]).replace("Werbekampagnen", "Werbe&shy;kampagnen")}</span>'
                 f'<p>{e(x["denkweise"])}</p></div>')
        s.append(seite(kopf(f'Stellenbeschreibung 0{i + 1}', e(x["stelle"])) + f'<p class="lead">{e(lead(x["einleitung"]))}</p>'
                       + f'<div class="stelle"><div>{teile}</div>{karte}</div>'))

    # 10 · Stellenanzeigen – als echte, farbige Postings
    posts = ""
    for k, x in enumerate(PR["liste"]):
        P = x["posting"]
        posts += (f'<div class="post"><div class="post-karte"><div class="post-kopf"><i></i><div><b>Deine Agentur</b><span>Jetzt · Karriere</span></div></div>'
                  f'<div class="post-bild p{k + 1}"><span class="kreis"></span><span class="badge">Wir suchen</span><b>{e(P["titel"])}</b><span class="sub">{e(P["sub"])}</span></div>'
                  '<div class="post-fuss"><span>Gefällt mir · Kommentieren · Teilen</span></div></div>'
                  f'<div class="post-text"><h3>{e(P["headline"])}</h3>' + "".join(f"<p>{e(t)}</p>" for t in P["text"])
                  + '<p class="tags">#Karriere #Versicherung #Jobs</p></div></div>')
    s.append(seite(kopf("Stellenanzeigen", f'Fünf Anzeigen {grad("zum Veröffentlichen.")}')
                   + '<p class="lead">Bild und Text für LinkedIn, die Karriereseite oder Social Media – Logo und Kontaktdaten setzt du ein.</p>' + posts))

    # 11 · Kontakt
    gesichter = "".join(f'<img src="file://{img6}/ansprechpartner-{n}.webp" alt="">' for n in ("kerstin", "daniel", "noah"))
    s.append(seite(
        f'<img class="logo" src="{logo_hell}" alt="sofort sichtbar">'
        + f'<p class="kicker" style="margin-top:40mm">Kontakt</p><h1>Lass uns sprechen.<br>{grad("Ganz konkret.")}</h1>'
        + f'<p class="lead">{e(S["kontaktseite"]["lead"])}</p>'
        + f'<div class="gesichter"><span>{gesichter}</span>{e(S["kontakt"]["team_satz"])}</div>'
        + f'<div class="wege"><span class="klein">Termin auswählen</span><b>sofortsichtbar.de/kontakt</b>'
        + f'<span class="klein" style="margin-top:3mm">Lieber direkt?</span><b>{e(S["kontakt"]["mail"])}</b><b>{e(S["kontakt"]["tel"])}</b></div>',
        "voll dunkel kontakt"))

    dok = (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Marketing as a Service – sofort sichtbar</title>'
           f'<style>{css()}</style></head><body>{SVG_CSS}{"".join(s)}{VERLAUF_JS}</body></html>')
    return dok, d7


def main():
    dok, d7 = bauen()
    tmp = tempfile.mkdtemp(prefix="maas7_")
    h = os.path.join(tmp, "maas.html")
    open(h, "w", encoding="utf-8").write(dok)
    os.makedirs(ZIEL, exist_ok=True)
    pdf = os.path.join(ZIEL, "marketing-as-a-service.pdf")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    "--virtual-time-budget=6000", f"--print-to-pdf={pdf}", "file://" + h], check=True, capture_output=True)
    seiten = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    groesse = f'{os.path.getsize(pdf) / 1e6:.1f} MB'.replace(".", ",")
    for n in (1, 2):
        subprocess.run(["pdftoppm", "-r", "110", "-png", "-f", str(n), "-l", str(n), "-singlefile", pdf, os.path.join(ZIEL, f"marketing-as-a-service-{n}")], check=True)
    vorschau = os.path.join(tmp, "seiten")
    os.makedirs(vorschau)
    subprocess.run(["pdftoppm", "-r", "60", "-png", pdf, os.path.join(vorschau, "s")], check=True)
    dl = d7["s7"]["maas"]["download"]
    dl.update({"meta": ["PDF", f"{seiten} Seiten", groesse], "datei": "marketing-as-a-service.pdf",
               "bild1": "marketing-as-a-service-1.png", "bild2": "marketing-as-a-service-2.png", "ordner": "story7"})
    d7["s7"]["maas"]["bausteine"]["pdf"] = f"Alle Leistungen im Detail (PDF, {seiten} Seiten)"
    json.dump(d7, open(D7, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(D7, "a").write("\n")
    print(pdf, seiten, "Seiten", groesse)
    print("Seitenbilder:", vorschau)


if __name__ == "__main__":
    main()
