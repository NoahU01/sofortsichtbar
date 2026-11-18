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
BG = "#0b0b0d"

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
    ("klar", "Klar", "Nur Schwarz, Logo und Satz. Am ruhigsten, nichts lenkt von Fenstern und Symbolen ab."),
    ("leuchten", "Leuchten", "Gedämpftes Licht in Cyan und Violett aus zwei Ecken – Tiefe, ohne zu blenden."),
    ("faden", "Faden", "Eine feine Linie im Verlauf zieht durch das Bild und endet in einem leuchtenden Punkt – wie der Faden der Grundstory."),
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


def bild(gkey, w, h, art, var):
    # Lage von Logo und Satz je Geräteart (in Punkten)
    if art == "mac":
        logo = dict(left=.07 * w, top=.10 * h, height=.075 * h)
        txt = dict(left=.07 * w, bottom=.20 * h, size=.056 * w, align="left")
        glow = ("85% 100%", "8% 0%")
        faden = f"M{-0.02 * w} {.93 * h} C {.30 * w} {.99 * h} {.58 * w} {.86 * h} {.82 * w} {.66 * h}"
        punkt = (.82 * w, .66 * h)
    elif art == "ipad":
        logo = dict(left=.5 * w, top=.30 * h, height=.065 * h, mitte=True)
        txt = dict(left=0, top=.43 * h, size=.058 * w, align="center", breite=w)
        glow = ("88% 92%", "12% 8%")
        faden = f"M{-0.02 * w} {.80 * h} C {.30 * w} {.92 * h} {.62 * w} {.66 * h} {.86 * w} {.70 * h}"
        punkt = (.86 * w, .70 * h)
    elif art == "iphone":
        logo = dict(left=.10 * w, top=.335 * h, height=.046 * h)
        txt = dict(left=.10 * w, top=.42 * h, size=.13 * w, align="left")
        glow = ("100% 88%", "0% 20%")
        faden = f"M{-0.04 * w} {.82 * h} C {.35 * w} {.77 * h} {.55 * w} {.90 * h} {.90 * w} {.76 * h}"
        punkt = (.90 * w, .76 * h)
    else:  # Teams/Zoom: Inhalt am linken Rand, die Person sitzt in der Mitte
        logo = dict(left=.05 * w, top=.08 * h, height=.075 * h)
        txt = dict(left=.05 * w, bottom=.09 * h, size=.04 * w, align="left")
        glow = ("100% 100%", "0% 0%")
        faden = f"M{.16 * w} {.13 * h} C {.40 * w} {.02 * h} {.62 * w} {.20 * h} {1.02 * w} {.06 * h}"
        punkt = (.16 * w, .13 * h)
    hintergrund = BG
    if var == "leuchten":
        a, b = glow
        hintergrund = (f"radial-gradient(55% 55% at {a}, rgba(134,19,161,.42), transparent 72%),"
                       f"radial-gradient(45% 45% at {b}, rgba(11,159,189,.26), transparent 72%), {BG}")
    lg = (f'<img src="file://{LOGO}" style="position:absolute;height:{logo["height"]:.1f}px;top:{logo["top"]:.1f}px;'
          + (f'left:{logo["left"]:.1f}px;transform:translateX(-50%)' if logo.get("mitte") else f'left:{logo["left"]:.1f}px') + '">')
    pos = f'left:{txt["left"]:.1f}px;' + (f'top:{txt["top"]:.1f}px;' if "top" in txt else f'bottom:{txt["bottom"]:.1f}px;')
    if txt.get("breite"):
        pos += f'width:{txt["breite"]}px;'
    tx = (f'<p style="position:absolute;{pos}margin:0;font:700 {txt["size"]:.1f}px/1.02 \'Inter Tight\';letter-spacing:-.035em;'
          f'color:#fff;text-align:{txt["align"]}">{satz(art)}</p>')
    fd = ""
    if var == "faden":
        sw = max(w, h) * .004
        px, py = punkt
        fd = (f'<svg width="{w}" height="{h}" style="position:absolute;left:0;top:0"><defs><linearGradient id="g" x1="0" x2="1">'
              f'<stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient>'
              f'<radialGradient id="r"><stop offset="0" stop-color="#8613a1" stop-opacity=".55"/><stop offset="1" stop-color="#8613a1" stop-opacity="0"/></radialGradient></defs>'
              f'<path d="{faden}" fill="none" stroke="url(#g)" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
              f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{sw * 9:.1f}" fill="url(#r)"/><circle cx="{px:.1f}" cy="{py:.1f}" r="{sw * 2.4:.1f}" fill="#b45ad0"/></svg>')
    css = (schriften() + f"*{{margin:0}}html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{BG}}}"
           ".v{background:linear-gradient(100deg,#19b6d4,#a64fd0);-webkit-background-clip:text;background-clip:text;color:transparent}")
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div style="position:relative;width:{w}px;height:{h}px;background:{hintergrund}">{fd}{lg}{tx}</div></body></html>'


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
    tmp = tempfile.mkdtemp(prefix="hg7_")
    liste, daten = [], []
    for vkey, vname, vtext in VARIANTEN:
        eintraege = []
        for gkey, gname, w, h, art in GERAETE:
            html = os.path.join(tmp, f"{vkey}-{gkey}.html")
            open(html, "w").write(bild(gkey, w, h, art, vkey))
            datei = f"sofortsichtbar-hintergrund-{vkey}-{gkey}-{2 * w}x{2 * h}.png"
            liste.append({"html": html, "png": os.path.join(ZIEL, datei), "w": w, "h": h})
            eintraege.append({"geraet": gname, "datei": datei, "vorschau": datei.replace(".png", ".webp"), "masse": f"{2 * w} × {2 * h}", "art": art})
        daten.append({"id": vkey, "name": vname, "text": vtext, "bilder": eintraege})
    js = os.path.join(tmp, "aufnahme.mjs")
    open(js, "w").write(AUFNAHME)
    lp = os.path.join(tmp, "liste.json")
    json.dump(liste, open(lp, "w"))
    subprocess.run(["node", js, lp], check=True)
    from PIL import Image
    for x in liste:
        im = Image.open(x["png"]).convert("RGB")
        im.thumbnail((900, 900))
        im.save(x["png"].replace(".png", ".webp"), quality=84)
    p = os.path.join(HERE, "story7.11tydata.json")
    d = json.load(open(p, encoding="utf-8"))
    d["s7"]["hintergruende"] = {"kicker": "Für deine Geräte", "h2": "Hintergrundbilder.",
                                "lead": "Dunkel, damit nichts blendet – mit Logo und Grundaussage. Für MacBook, iPad, iPhone sowie Teams und Zoom; Uhr, Dock und die Person im Videocall bleiben frei.",
                                "varianten": daten}
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    print(len(liste), "Bilder")


if __name__ == "__main__":
    main()
