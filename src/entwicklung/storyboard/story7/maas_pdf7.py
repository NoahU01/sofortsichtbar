#!/usr/bin/env python3
"""PDF „Marketing as a Service“ im Look von Homepage-Story 7 (Daniel, 12.11.2026: Seitenfolge freigegeben).

SCHRIFTSYSTEM (fest, vor dem Bauen festgelegt – Vorbild ist die Website Story 7, nicht empiria):
  Inter Tight 700  – Überschriften in genau zwei Größen: H1 36 pt (nur Deckblatt), H2 22 pt (alle übrigen Seiten, auch große Zahlen)
  Inter 400/600    – Text 10 pt (Regular, Hervorhebung SemiBold); Klein 8 pt für Kicker, Nebeninfos, Fußzeile
  Farben           – Tinte #1d1d1f, Grau #6e6e73; Verlauf Cyan → Violett höchstens einmal je Seite (ein Wort der Überschrift oder eine Fläche)

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
h1 { font-size: 36pt; line-height: 1.04; }
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
.dunkel h2, .dunkel h3 { color: #fff; }
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
.leistung { padding: 2.8mm 0; border-bottom: 0.3mm solid #e5e5ea; break-inside: avoid; }
.leistung h3 { margin-bottom: 1mm; }
.leistung ul { margin: 1.5mm 0 0; padding-left: 5mm; }
.leistung li { margin: .6mm 0; }
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
    img = os.path.join(SRC, "entwicklung", "storyboard", "story6", "assets", "img")
    logo = f'file://{img}/logo-dunkel.svg'
    logo_hell = f'file://{os.path.join(SRC, "assets", "img", "logos", "logo-white.svg")}'
    s = []

    # 1 · Deckblatt
    s.append(seite(
        f'<img class="logo" src="{logo}" alt="sofort sichtbar">'
        f'<h1>{e(M["held"]["h1"])}<br>{grad(e(M["held"]["h1_akzent"]))}</h1>'
        f'<p class="kicker" style="margin-top:6mm">{e(M["held"]["kicker"])}</p>'
        f'<p class="lead">{e(M["held"]["lead"])}</p>'
        f'<div class="buehne">{S["ek_schnitt_quer"]}</div>'
        '<div class="fakten"><div><b>ab 1.800 €</b><span class="klein">im Monat für das Kernpaket</span></div>'
        '<div><b>30 Tage</b><span class="klein">bis zum ersten Report</span></div>'
        '<div><b>1</b><span class="klein">fester Ansprechpartner</span></div></div>', "voll deck"))

    # 2 · Die Maschine
    s.append(seite(
        kopf("Das Prinzip", f'Die digitale Maschine<br>{grad("vor deinem Vertrieb.")}')
        + f'<p class="lead">{e(S["hero"]["lead"])}</p>'
        + f'<div class="buehne">{S["ek_quer"]}</div>'
        + '<div class="drei">'
        '<div><h3>Marketing – wir gewinnen Interessenten</h3><p>Landingpages, Postings und Kundenmailings je Zielgruppe – laufend betreut.</p></div>'
        '<div><h3>Messpunkt: Leads</h3><p>Jeder Lead landet direkt bei dir und ist im Dashboard messbar.</p></div>'
        '<div><h3>Vertrieb – du machst daraus Kunden</h3><p>Du fasst nach, berätst und schließt ab – so, wie du es kennst.</p></div>'
        '</div>'))

    # 3 · 30-Tage-Plan
    ST = M["start"]
    wochen = "".join(f'<div class="woche"><div><span class="w">{e(x["wann"].replace("Woche ", ""))}</span><p class="klein">Woche</p></div>'
                     f'<div><h3>{e(x["titel"])}</h3><p>{e(x["text"])}</p></div></div>' for x in ST["liste"])
    s.append(seite(
        kopf(ST["kicker"], f'Der {grad("30-Tage-Plan.")}')
        + f'<p class="lead">{e(ST["lead"])}</p><div class="wochen">{wochen}</div>'
        + f'<div class="kasten"><h3>{e(ST["aufwand_titel"])}</h3><ul class="haken">'
        + "".join(f"<li>{e(x)}</li>" for x in ST["aufwand"]) + '</ul></div>'))

    # 4 · Danach jeden Monat – auf derselben Seite wie der 30-Tage-Plan (vorher zwei halbe Seiten)
    vier = "".join(f'<div><span class="nr">0{i + 1}</span><h3>{e(a["titel"])}</h3><p>{e(lead(a["text"]))}</p></div>' for i, a in enumerate(M6["ablauf"]))
    s[-1] = s[-1].replace("</section>", f'<p class="gruppe" style="margin-top:9mm">Danach: jeden Monat ein Stück besser</p><div class="vier">{vier}</div></section>')

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

    # 6 · Bausteine im Detail (fließen über so viele Seiten wie nötig, jeder Baustein beginnt neu)
    for i, b in enumerate(BS["liste"]):
        F = b["fenster"]
        teile = ""
        for g in F["gruppen"]:
            teile += f'<p class="gruppe">{e(g["label"])}</p>'
            for l in g["leistungen"]:
                teile += (f'<div class="leistung"><h3>{e(l["titel"])}</h3>' + (f'<p>{e(l["text"])}</p>' if l.get("text") else "")
                          + ("<ul>" + "".join(f"<li>{e(x)}</li>" for x in l["liste"]) + "</ul>" if l.get("liste") else "") + "</div>")
        name = F["titel"].replace("Kernpaket „sofort sichtbar“", "Kernpaket sofort sichtbar")
        s.append(seite(
            kopf(f'Baustein 0{i + 1} · {b["art"]}', e(name))
            + f'<p class="meta">{e(F["meta"])}</p>'
            + "".join(f'<p class="lead">{e(x)}</p>' for x in F["intro"]) + teile
            + (f'<p class="hinweis">{e(F["hinweis"])}</p>' if F.get("hinweis") else "")))

    # 7 · Team
    PR = M6["profile"]
    zeilen_k = "".join(f'<div class="profil"><div><h3>{e(x["klartext"])}</h3><p class="klein">{e(x["stelle"])}</p></div><p>{e(x["denkweise"])}</p></div>' for x in PR["liste"] if x["gruppe"] == "kern")
    zeilen_p = "".join(f'<div class="profil"><div><h3>{e(x["klartext"])}</h3><p class="klein">{e(x["stelle"])}</p></div><p>{e(x["denkweise"])}</p></div>' for x in PR["liste"] if x["gruppe"] != "kern")
    s.append(seite(
        kopf("Dein Team", f'Fünf Profile. {grad("Ein Team.")}')
        + f'<p class="lead">{e(PR["lead"])}</p>'
        + f'<p class="gruppe-team">Im Kernpaket</p><div>{zeilen_k}</div><p class="gruppe-team">Mit Paid Ads</p><div>{zeilen_p}</div>'
        + '<div class="immer">' + "".join(f"<span>{e(x)}</span>" for x in M6["immer"]) + '</div>'))

    # 8 · Lieber selbst einstellen?
    verz = "".join(f'<div class="profil"><div><h3>{e(x["stelle"])}</h3><p class="klein">{e(x["klartext"])}</p></div><p>Stellenbeschreibung und fertige Anzeige</p></div>' for x in PR["liste"])
    s.append(seite(
        kopf("Zum Selbermachen", f'Lieber selbst {grad("einstellen?")}')
        + '<p class="lead">Du willst die Profile lieber selbst besetzen? Auf den nächsten Seiten stehen alle fünf Stellenbeschreibungen – und fertige Anzeigen für LinkedIn, die Karriereseite oder Social Media.</p>'
        + f'<div class="profile">{verz}</div>'))

    # 9 · Stellenbeschreibungen
    for i, x in enumerate(PR["liste"]):
        wo = "Im Kernpaket" if x["gruppe"] == "kern" else "Mit Paid Ads"
        teile = "".join(f'<div class="stelle-teil"><p class="gruppe">{t2}</p><ul>' + "".join(f"<li>{e(y)}</li>" for y in liste) + '</ul></div>'
                        for t2, liste in (("Aufgaben", x["aufgaben"]), ("Anforderungen", x["anforderungen"]), ("Ausbildung und Erfahrung", x["ausbildung"])))
        s.append(seite(kopf(f'Stellenbeschreibung 0{i + 1} · {wo}', e(x["stelle"])) + f'<p class="lead">{e(lead(x["einleitung"]))}</p>' + teile))

    # 10 · Stellenanzeigen
    anz = "".join(
        f'<div class="anzeige"><div class="anz-bild"><span class="klein">Wir suchen</span><b>{e(x["posting"]["titel"])}</b><span class="klein">{e(x["posting"]["sub"])}</span></div>'
        f'<div><h3>{e(x["posting"]["headline"])}</h3>' + "".join(f"<p>{e(t)}</p>" for t in x["posting"]["text"]) + '</div></div>'
        for x in PR["liste"])
    s.append(seite(kopf("Stellenanzeigen", f'Fünf Anzeigen {grad("zum Veröffentlichen.")}')
                   + '<p class="lead">Bild und Text für LinkedIn, die Karriereseite oder Social Media – Logo und Kontaktdaten setzt du ein.</p>' + anz))

    # 11 · Kontakt
    gesichter = "".join(f'<img src="file://{img}/ansprechpartner-{n}.webp" alt="">' for n in ("kerstin", "daniel", "noah"))
    s.append(seite(
        f'<img class="logo" src="{logo_hell}" alt="sofort sichtbar">'
        + f'<p class="kicker" style="margin-top:40mm">Kontakt</p><h2 style="font-size:36pt;line-height:1.04">Lass uns sprechen.<br>{grad("Ganz konkret.")}</h2>'
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
