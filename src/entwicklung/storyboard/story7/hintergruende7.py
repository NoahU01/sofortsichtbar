#!/usr/bin/env python3
"""Hintergrundbilder sofort sichtbar (Daniel, 18.11.2026) – dunkel, Logo + „Die digitale Maschine vor deinem Vertrieb.“

Formate und Regeln wie empiria (werkzeuge/ga/hintergruende.py):
  MacBook 3024×1964 · iPad 13″ 2752² · iPad mini 2266² (quadratisch: iPadOS schneidet quer/hoch aus der Mitte, Wichtiges im mittleren 75-%-Feld)
  iPhone 13 mini 1080×2340 · iPhone 13 Pro 1170×2532 · iPhone 16 Pro 1206×2622 (oben bis 30 % Uhr/Widgets, ab 85 % Dock frei)
  Teams/Zoom 1920×1080 (Person sitzt mittig – Inhalt am linken Rand)
Gestaltet in Punkten, exportiert in doppelter Auflösung (wie empiria).
Drei Varianten: klar · leuchten · faden.

Aufruf: python3 src/entwicklung/storyboard/story7/hintergruende7.py
Ergebnis: story7/assets/hintergruende/*.png (+ Vorschau *.webp), s7.hintergruende in story7.11tydata.json
"""
import json
import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ZIEL = os.path.join(HERE, "assets", "hintergruende")
FONTS = os.path.join(HERE, "assets", "fonts")
LOGO = os.path.join(SRC, "assets", "img", "logos", "logo-white.svg")
PILL = os.path.join(SRC, "assets", "img", "logos", "logo-icon.svg")  # nur die Pill aus dem Logo (Key Visual), 55 × 22
BG = "#000000"  # tiefschwarz (Daniel, 18.11.2026, auf dem iPad mini geprüft: Grau wirkt zu hell, als wäre am Bild etwas kaputt)

# Vorschau so, wie es auf dem Gerät aussieht: iPad quer ausgeschnitten (Bildschirmseitenverhältnis), Größen maßstäblich nach Bildschirmbreite (cm)
VORSCHAU = {"macbook": (None, 30.2), "ipad13": (4 / 3, 28.1), "ipadmini": (1.52, 19.5), "teams": (None, 30.2),
            "iphone13mini": (None, 5.4), "iphone13pro": (None, 6.4), "iphone16pro": (None, 6.6)}
GERAETE = [  # Schlüssel, Name, Breite, Höhe (Punkte), Art
    ("macbook", "MacBook Air 13″", 3024, 1964, "mac"),
    ("ipad13", "iPad Air 13″", 2752, 2752, "ipad"),
    ("ipadmini", "iPad mini", 2266, 2266, "ipad"),
    ("iphone13mini", "iPhone 13 mini", 1080, 2340, "iphone"),
    ("iphone13pro", "iPhone 13 Pro", 1170, 2532, "iphone"),
    ("iphone16pro", "iPhone 16 Pro", 1206, 2622, "iphone"),
    ("teams", "Teams und Zoom", 1920, 1080, "video"),
]
VARIANTEN = [
    ("klar", "Klar", "Die Grundform: Logo und Satz als ein Block, ruhig gesetzt. Nichts lenkt von Fenstern und Symbolen ab."),
    ("akzent", "Akzent", "Wie Klar, dahinter gedämpftes Licht in Violett und Cyan."),
    ("akzent-pill-satz", "Akzent · Pill statt Logo", "Wie Akzent mit demselben Satz, nur steht an der Stelle des Logos die Pill – das Key Visual, kleiner als das Logo. Für iPad mini und iPhone.", ("ipadmini", "iphone")),
    ("trichter", "Trichter", "Das Bild aus Story 8: Marketing – wir gewinnen Interessenten, Vertrieb – du machst daraus Kunden. Mit viel Rand, kein Bildschirm voll."),
    ("trichter-stilisiert", "Trichter stilisiert", "Der Trichter ohne ein Wort, rechts neben dem Satz – beide als eine Gruppe mittig, der Trichter auf der Höhe des Satzes."),
    ("nur-trichter", "Nur Trichter", "Nur der Trichter, ohne Blöcke. Quer mündet er direkt in den Satz – Maschine und Aussage auf einer Höhe."),
]


def schriften():
    out = ""
    for fam, datei, w in (("Inter", "inter", 500), ("Inter Tight", "inter-tight", 700)):
        for sub in ("latin", "latin-ext"):
            out += f'@font-face{{font-family:"{fam}";font-weight:{w};src:url("file://{FONTS}/{datei}-{sub}-{w}-normal.woff2")}}'
    return out


def satz(art):
    if art in ("iphone", "video"):
        return 'Die digitale<br>Maschine<br><span class="v">vor deinem<br>Vertrieb.</span>'
    return 'Die digitale Maschine<br><span class="v">vor deinem Vertrieb.</span>'


S8 = json.load(open(os.path.join(HERE, "..", "story8", "story8.11tydata.json"), encoding="utf-8"))["s7"]

# Trichter aus Story 8 auf dunklem Grund: Lagen aufgehellt, Fuge und Lagenkanten in Grundfarbe, Vertriebsband mittelgrau
TRICHTER_CSS = (
    ".tr svg{display:block;width:100%;height:auto;overflow:visible}"
    f".tr .ek2-lage{{stroke:{BG};stroke-width:2}}"
    ".tr .ek2-l2,.tr .ek2-l2-h{fill:#3a3a3e}.tr .ek2-l3,.tr .ek2-l3-h{fill:#2a2a2d}.tr .ek2-l4,.tr .ek2-l4-h{fill:#1c1c1e}"
    ".tr .ek2-kern{fill:url(#hg-q)}.tr .ek2-kern-h{fill:url(#hg-h)}"
    ".tr .ek2-kern-t{fill:#fff}.tr .ek2-kern-s{fill:rgba(255,255,255,.82)}"
    f".tr .ek2-fuge{{fill:none;stroke:{BG};stroke-width:6;stroke-linecap:round}}"
    ".tr .ek2-band{fill:#2c2c2e}.tr .ek2-l2{fill:#3a3a3e}.tr .ek2-l3{fill:#2a2a2d}.tr .ek2-l4{fill:#1c1c1e}"
    ".tr .ek2-band-t{fill:#fff}.tr .ek2-band-s{fill:#a1a1a6}"
    ".tr .ek2-t{fill:#f5f5f7}.tr .ek2-grau{fill:#a1a1a6}"
    ".tr .ek2-linie{fill:none;stroke:#f5f5f7;stroke-width:2}.tr .ek2-linie--fein{stroke-width:1.4}"
    ".tr .ek2-pfeilkopf{fill:none;stroke:#f5f5f7}"
    ".tr text{font-family:Inter,sans-serif}"
    # stilisiert: nur Formen, kein Wort
    ".stil text,.stil .ek2-linie,.stil .ek2-pfeilkopf{display:none}"
)
VERLAUF_DEFS = ('<svg width="0" height="0" style="position:absolute"><defs>'
                '<linearGradient id="hg-q" x1="0" x2="1"><stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient>'
                '<linearGradient id="hg-h" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient>'
                '</defs></svg>')


# Stilisierter Trichter: Geometrie wie Story 8 (Bogen-Fuge, Form B), ohne Worte; Blöcke für Vertrieb und Betreuen optional und klein
MUND, HALS = [50, 74, 96, 118], [30, 38, 46, 54]
XF, XK, XH, XT, C = 250, 450, 510, 262, 120


def _lage(k):
    hm, hh = MUND[k], HALS[k]
    return (f"M0 {C - hm} H{XF} C{XF + 130} {C - hm} {XK - 100} {C - hh} {XK} {C - hh} H{XH} "
            f"V{C + hh} H{XK} C{XK - 100} {C + hh} {XF + 130} {C + hm} {XF} {C + hm} H0 Z")


def stil_svg(bloecke=False, senkrecht=False):
    o = [f'<path d="{_lage(k)}" class="{("ek2-kern" if k == 0 else f"ek2-l{k + 1}")} ek2-lage"/>' for k in (3, 2, 1, 0)]
    yo, yu = C - MUND[3] - 2, C + MUND[3] + 2
    o.append(f'<path d="M{XT - 10} {yo} C{XT + 14} {C - 50} {XT + 14} {C + 50} {XT - 10} {yu}" class="ek2-fuge"/>')
    breite = XH
    if bloecke:  # klein: halbe Höhe des Halses, kurze Pfeile
        bh, x0 = HALS[3] * .7, XH + 14
        o.append(f'<path d="M{x0} {C - bh} H{x0 + 58} L{x0 + 72} {C} L{x0 + 58} {C + bh} H{x0} L{x0 + 14} {C} Z" class="ek2-band"/>')
        x1 = x0 + 80
        o.append(f'<path d="M{x1} {C - bh} H{x1 + 64} Q{x1 + 74} {C - bh} {x1 + 74} {C - bh + 10} V{C + bh - 10} Q{x1 + 74} {C + bh} {x1 + 64} {C + bh} H{x1} L{x1 + 14} {C} Z" class="ek2-band"/>')
        breite = x1 + 74
    inhalt = "".join(o)
    if senkrecht:  # Öffnung oben, Hals unten
        return f'<svg viewBox="0 0 240 {breite}" aria-hidden="true"><g transform="translate(240 0) rotate(90)">{inhalt}</g></svg>', 240 / breite
    return f'<svg viewBox="0 0 {breite} 240" aria-hidden="true">{inhalt}</svg>', breite / 240


def block(art, left, mitte_y, size, align="left", breite=None, logo=None):
    logo_h = size * (.36 if logo == PILL else .72)  # Pill deutlich kleiner als das Logo (Daniel, 20.11.2026)
    ausr = "flex-start" if align == "left" else "center"
    br = f"width:{breite}px;" if breite else ""
    return (f'<div style="position:absolute;left:{left:.1f}px;top:{mitte_y:.1f}px;transform:translateY(-50%);{br}'
            f'display:flex;flex-direction:column;align-items:{ausr};gap:{size * .75:.1f}px">'
            f'<img src="file://{logo or LOGO}" style="height:{logo_h:.1f}px;display:block">'
            f'<p style="margin:0;font:700 {size:.1f}px/1.03 \'Inter Tight\';letter-spacing:-.035em;color:#f5f5f7;text-align:{align}">{satz(art)}</p></div>')


def setze(kl, svgx, left, top, breite):
    return f'<div class="{kl}" style="position:absolute;left:{left:.0f}px;top:{top:.0f}px;width:{breite:.0f}px">{svgx}</div>'


def bild(gkey, w, h, art, var):
    """Logo und Satz bilden einen Block (Logo klein, linksbündig, fester Abstand). Eine Schriftgröße wie auf der Homepage.
    iPad: Inhalt nur im Mittelband – oben App-Reihen (13″ zwei, mini eine), unten Dock; quer schneidet iPadOS zusätzlich oben/unten ab."""
    mini = gkey == "ipadmini"
    band = (.53 if mini else .58) * h          # Mitte des freien Bands auf dem iPad
    teile = []
    hintergrund = BG
    if var in ("klar", "akzent", "akzent-pill-satz"):
        logo = PILL if var == "akzent-pill-satz" else None
        if art == "ipad":
            teile.append(block(art, 0, band, .056 * w, "center", w, logo))
        elif art == "mac":
            teile.append(block(art, .08 * w, .47 * h, .046 * w))
        elif art == "iphone":
            teile.append(block(art, .10 * w, .52 * h, .11 * w, logo=logo))
        else:
            teile.append(block(art, .05 * w, .5 * h, .034 * w))
        if var in ("akzent", "akzent-pill-satz"):
            lage = {"mac": "26% 47%", "ipad": f"50% {band / h * 100:.0f}%", "iphone": "34% 54%", "video": "18% 52%"}[art]
            hintergrund = f"radial-gradient(40% 36% at {lage}, rgba(134,19,161,.30), transparent 72%), radial-gradient(28% 26% at {lage}, rgba(11,159,189,.16), transparent 70%), {BG}"
    elif var == "trichter":  # Bild aus Story 8 mit Worten, viel Rand
        if art == "mac":
            teile.append(block(art, .19 * w, .30 * h, .032 * w))
            teile.append(setze("tr", S8["ek_kopf"], .19 * w, .43 * h, .62 * w))
        elif art == "ipad":
            fb = .64 * w
            teile.append(block(art, 0, band - .13 * h, .036 * w, "center", w))
            teile.append(setze("tr", S8["ek_kopf"], (w - fb) / 2, band - .04 * h, fb))
        elif art == "iphone":
            hoehe = .33 * h
            teile.append(block(art, .10 * w, .405 * h, .075 * w))
            teile.append(setze("tr", S8["ek_hoch"], .10 * w - 30 * hoehe / 622, .52 * h, hoehe * 340 / 622))
        else:
            hoehe = .84 * h
            teile.append(block(art, .05 * w, .5 * h, .034 * w))
            teile.append(setze("tr", S8["ek_hoch"], .95 * w - hoehe * 340 / 622, .08 * h, hoehe * 340 / 622))
    elif var == "trichter-stilisiert":  # ohne Blöcke (Daniel, 18.11.2026: „sieht aus, als würde der Trichter etwas schießen“)
        if art in ("mac", "ipad"):
            # Satz links, Trichter rechts als eine Gruppe, mittig auf dem Bildschirm; Trichter auf der Achse des Satzes (nicht von Logo und Satz)
            svgx, verh = stil_svg(False)
            size, fb, mitte = (.040 * w, .30 * w, .48 * h) if art == "mac" else (.033 * w, .25 * w, band)
            versatz = (size * .72 + size * .75) / 2
            teile.append(f'<div style="position:absolute;left:0;top:{mitte:.0f}px;width:{w}px;transform:translateY(calc(-50% - {versatz:.1f}px));'
                         f'display:flex;align-items:center;justify-content:center;gap:{.05 * w:.0f}px">'
                         f'<div style="display:flex;flex-direction:column;gap:{size * .75:.1f}px"><img src="file://{LOGO}" style="height:{size * .72:.1f}px;align-self:flex-start">'
                         f'<p style="margin:0;font:700 {size:.1f}px/1.03 \'Inter Tight\';letter-spacing:-.035em;color:#f5f5f7">{satz("mac")}</p></div>'
                         f'<div class="tr" style="width:{fb:.0f}px;transform:translateY({versatz:.1f}px)">{svgx}</div></div>')
        elif art == "iphone":  # Trichter bündig unter dem Satz
            svgx, verh = stil_svg(False, True)
            hoehe = .30 * h
            teile.append(block(art, .10 * w, .40 * h, .075 * w))
            teile.append(setze("tr", svgx, .10 * w, .53 * h, hoehe * verh))
        else:  # Teams: Satz links, Trichter rechts auf derselben Mittellinie
            svgx, verh = stil_svg(False, True)
            hoehe = .62 * h
            teile.append(block(art, .05 * w, .5 * h, .034 * w))
            teile.append(setze("tr", svgx, .92 * w - hoehe * verh, .5 * h - hoehe / 2, hoehe * verh))
    else:  # nur-trichter: quer mündet der Trichter in den Satz – gleiche Höhe
        if art in ("mac", "ipad"):
            svgx, verh = stil_svg(False)
            if art == "mac":
                fb, x0, mitte, size = .34 * w, .13 * w, .48 * h, .040 * w
            else:
                fb, x0, mitte, size = .28 * w, .13 * w, band, .033 * w
            teile.append(setze("tr", svgx, x0, mitte - fb / verh / 2, fb))
            # Satz auf der Achse des Trichters, Logo darüber
            xs = x0 + fb + .025 * w
            hs = 2 * 1.03 * size
            teile.append(f'<p style="position:absolute;left:{xs:.0f}px;top:{mitte - hs / 2:.0f}px;margin:0;font:700 {size:.1f}px/1.03 \'Inter Tight\';letter-spacing:-.035em;color:#f5f5f7">{satz("mac")}</p>')
            teile.append(f'<img src="file://{LOGO}" style="position:absolute;left:{xs:.0f}px;top:{mitte - hs / 2 - size * .75 - size * .72:.0f}px;height:{size * .72:.1f}px">')
        elif art == "iphone":
            svgx, verh = stil_svg(False, True)
            hoehe = .30 * h
            teile.append(block(art, .10 * w, .40 * h, .075 * w))
            teile.append(setze("tr", svgx, .10 * w, .53 * h, hoehe * verh))
        else:
            svgx, verh = stil_svg(False, True)
            hoehe = .62 * h
            teile.append(block(art, .05 * w, .5 * h, .034 * w))
            teile.append(setze("tr", svgx, .92 * w - hoehe * verh, .19 * h, hoehe * verh))
    css = (schriften() + f"*{{margin:0;box-sizing:border-box}}html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{BG}}}"
           ".v{background:linear-gradient(100deg,#19b6d4,#a64fd0);-webkit-background-clip:text;background-clip:text;color:transparent}"
           + TRICHTER_CSS)
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{VERLAUF_DEFS}<div style="position:relative;width:{w}px;height:{h}px;background:{hintergrund};overflow:hidden">{"".join(teile)}</div></body></html>'


AUFNAHME = r"""
import puppeteer from '/Users/danielstroebel/Projekte/empiria/site/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js';
import fs from 'fs';
const liste = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--allow-file-access-from-files'], protocolTimeout: 300000 });
for (const x of liste) {
  const p = await b.newPage(); await p.setViewport({ width: x.w, height: x.h, deviceScaleFactor: 2 });
  await p.goto('file://' + x.html, { waitUntil: 'networkidle0' }); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: x.png }); await p.close();
}
await b.close();
"""


def main():
    os.makedirs(ZIEL, exist_ok=True)
    for f in os.listdir(ZIEL):
        os.remove(os.path.join(ZIEL, f))
    tmp = tempfile.mkdtemp(prefix="hg7_")
    liste, daten = [], []
    for vkey, vname, vtext, *nur in VARIANTEN:
        eintraege = []
        for gkey, gname, w, h, art in GERAETE:
            if nur and art not in nur[0] and gkey not in nur[0]:
                continue
            html = os.path.join(tmp, f"{vkey}-{gkey}.html")
            open(html, "w").write(bild(gkey, w, h, art, vkey))
            datei = f"sofortsichtbar-hintergrund-{vkey}-{gkey}-{2 * w}x{2 * h}.png"
            liste.append({"html": html, "png": os.path.join(ZIEL, datei), "w": w, "h": h})
            eintraege.append({"geraet": gname, "datei": datei, "vorschau": datei.replace(".png", ".webp"), "masse": f"{2 * w} × {2 * h}", "art": art,
                              "reihe": "telefon" if art == "iphone" else "gross", "cm": VORSCHAU[gkey][1],
                              "hinweis": "Datei quadratisch, iPad zeigt die Mitte" if art == "ipad" else ""})
        for reihe in ("gross", "telefon"):
            summe = sum(e["cm"] for e in eintraege if e["reihe"] == reihe)
            for e in eintraege:
                if e["reihe"] == reihe:
                    e["anteil"] = round(e["cm"] / summe * 100, 2)
        daten.append({"id": vkey, "name": vname, "text": vtext, "bilder": eintraege,
                      "reihen": [r for r in ("gross", "telefon") if any(e["reihe"] == r for e in eintraege)]})
    js = os.path.join(tmp, "aufnahme.mjs")
    open(js, "w").write(AUFNAHME)
    lp = os.path.join(tmp, "liste.json")
    json.dump(liste, open(lp, "w"))
    subprocess.run(["node", js, lp], check=True)
    from PIL import Image
    for x in liste:
        im = Image.open(x["png"]).convert("RGB")
        if x["w"] == x["h"]:  # iPad: Vorschau quer wie der Bildschirm
            verh = 1.52 if x["w"] < 2500 else 4 / 3
            hh = int(im.width / verh)
            oben = (im.height - hh) // 2
            im = im.crop((0, oben, im.width, oben + hh))
        im.thumbnail((1800, 1800), Image.LANCZOS)  # scharf auch auf Retina
        im.save(x["png"].replace(".png", ".webp"), quality=92, method=6)
    p = os.path.join(HERE, "story7.11tydata.json")
    d = json.load(open(p, encoding="utf-8"))
    d["s7"]["hintergruende"] = {"kicker": "Für deine Geräte", "h2": "Hintergrundbilder.",
                                "lead": "Tiefschwarz, damit nichts blendet und der Bildschirmrand nahtlos ins Schwarze läuft – mit Logo und Grundaussage. Für MacBook, iPad, iPhone sowie Teams und Zoom; Uhr, Dock und die Person im Videocall bleiben frei. Klick auf ein Bild öffnet es in voller Größe.",
                                "varianten": daten}
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    print(len(liste), "Bilder")


if __name__ == "__main__":
    main()
