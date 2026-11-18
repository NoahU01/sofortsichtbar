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
BG = "#1d1d1f"  # wie der Footer der Website (Apple-Tinte), nicht tiefschwarz – Daniel 18.11.2026

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
    ("trichter", "Trichter", "Das Bild aus Story 8: Marketing – wir gewinnen Interessenten, Vertrieb – du machst daraus Kunden. Darunter der Trichter mit Vertrieb und Betreuen."),
    ("trichter-stilisiert", "Trichter stilisiert", "Der Trichter ohne ein Wort – nur die Formen. Je Gerät sinnvoll gesetzt: auf dem MacBook rechts neben dem Satz, auf iPad, iPhone und bei Teams senkrecht."),
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
    ".tr .ek2-l2,.tr .ek2-l2-h{fill:#46464b}.tr .ek2-l3,.tr .ek2-l3-h{fill:#38383c}.tr .ek2-l4,.tr .ek2-l4-h{fill:#2d2d31}"
    ".tr .ek2-kern{fill:url(#hg-q)}.tr .ek2-kern-h{fill:url(#hg-h)}"
    ".tr .ek2-kern-t{fill:#fff}.tr .ek2-kern-s{fill:rgba(255,255,255,.82)}"
    f".tr .ek2-fuge{{fill:none;stroke:{BG};stroke-width:6;stroke-linecap:round}}"
    ".tr .ek2-band{fill:#3a3a3e}.tr .ek2-band-t{fill:#fff}.tr .ek2-band-s{fill:#a1a1a6}"
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


def bild(gkey, w, h, art, var):
    """Logo und Satz bilden einen Block: Logo klein, linksbündig mit dem Satz, fester Abstand darüber. Eine Schriftgröße wie auf der Homepage."""
    trichter = var.startswith("trichter")
    stil = var == "trichter-stilisiert"
    hoch = trichter and (art in ("iphone", "video") or (stil and art == "ipad"))
    if art == "mac":
        size = .046 * w if not trichter else (.036 * w if not stil else .042 * w)
        block = dict(left=.08 * w, mitte_y=(.47 if not trichter or stil else .27) * h, align="left")
    elif art == "ipad":
        size = .06 * w if not trichter else (.046 * w if not stil else .042 * w)
        block = dict(left=0, mitte_y=(.45 if not trichter else (.30 if not stil else .27)) * h, align="center", breite=w)
    elif art == "iphone":
        size = .11 * w if not trichter else .075 * w
        block = dict(left=.10 * w, mitte_y=(.52 if not trichter else .405) * h, align="left")
    else:  # Teams/Zoom: Block am linken Rand, vertikal mittig – die Person sitzt in der Mitte
        size = .034 * w
        block = dict(left=.05 * w, mitte_y=.5 * h, align="left")
    logo_h = size * .72
    ausr = "flex-start" if block["align"] == "left" else "center"
    breite = f'width:{block["breite"]}px;' if block.get("breite") else ""
    blk = (f'<div style="position:absolute;left:{block["left"]:.1f}px;top:{block["mitte_y"]:.1f}px;transform:translateY(-50%);{breite}'
           f'display:flex;flex-direction:column;align-items:{ausr};gap:{size * .75:.1f}px">'
           f'<img src="file://{LOGO}" style="height:{logo_h:.1f}px;display:block">'
           f'<p style="margin:0;font:700 {size:.1f}px/1.03 \'Inter Tight\';letter-spacing:-.035em;color:#f5f5f7;text-align:{block["align"]}">{satz(art)}</p></div>')
    hintergrund = BG
    if var == "akzent":
        lage = {"mac": "26% 50%", "ipad": "50% 47%", "iphone": "34% 54%", "video": "18% 52%"}[art]
        hintergrund = f"radial-gradient(40% 36% at {lage}, rgba(134,19,161,.30), transparent 72%), radial-gradient(28% 26% at {lage}, rgba(11,159,189,.16), transparent 70%), {BG}"
    extra = ""
    if trichter:
        kl = "tr stil" if stil else "tr"
        if hoch:
            svgx = S8["ek_hoch"]
            if art == "ipad":  # senkrecht, mittig unter dem Satz – bleibt beim Drehen im Mittelfeld
                hoehe = .42 * h   # quer schneidet iPadOS oben/unten ab (iPad mini bis ca. 17 %) – alles zwischen 20 % und 80 %
                extra = f'<div class="{kl}" style="position:absolute;left:{(w - hoehe * 340 / 622) / 2:.0f}px;top:{.375 * h:.0f}px;width:{hoehe * 340 / 622:.0f}px">{svgx}</div>'
            elif art == "iphone":
                hoehe = .33 * h
                extra = f'<div class="{kl}" style="position:absolute;left:{.10 * w - 30 * hoehe / 622:.0f}px;top:{.52 * h:.0f}px;width:{hoehe * 340 / 622:.0f}px">{svgx}</div>'
            else:  # Teams: senkrechter Trichter rechts
                hoehe = .84 * h
                extra = f'<div class="{kl}" style="position:absolute;left:{.95 * w - hoehe * 340 / 622:.0f}px;top:{.08 * h:.0f}px;width:{hoehe * 340 / 622:.0f}px">{svgx}</div>'
        else:
            svgx = S8["ek_kopf"]
            if art == "mac" and stil:  # kompakt rechts neben dem Satz
                extra = f'<div class="{kl}" style="position:absolute;left:{.57 * w:.0f}px;top:{.47 * h - .35 * w * 320 / 1120 / 2:.0f}px;width:{.35 * w:.0f}px">{svgx}</div>'
            elif art == "mac":
                extra = f'<div class="{kl}" style="position:absolute;left:{.08 * w:.0f}px;top:{.46 * h:.0f}px;width:{.84 * w:.0f}px">{svgx}</div>'
            else:
                extra = f'<div class="{kl}" style="position:absolute;left:{.07 * w:.0f}px;top:{.44 * h:.0f}px;width:{.86 * w:.0f}px">{svgx}</div>'
    css = (schriften() + f"*{{margin:0;box-sizing:border-box}}html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{BG}}}"
           ".v{background:linear-gradient(100deg,#19b6d4,#a64fd0);-webkit-background-clip:text;background-clip:text;color:transparent}"
           + TRICHTER_CSS)
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{VERLAUF_DEFS}<div style="position:relative;width:{w}px;height:{h}px;background:{hintergrund};overflow:hidden">{extra}{blk}</div></body></html>'


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
    for vkey, vname, vtext in VARIANTEN:
        eintraege = []
        for gkey, gname, w, h, art in GERAETE:
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
        daten.append({"id": vkey, "name": vname, "text": vtext, "bilder": eintraege})
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
        im.thumbnail((1000, 1000))
        im.save(x["png"].replace(".png", ".webp"), quality=84)
    p = os.path.join(HERE, "story7.11tydata.json")
    d = json.load(open(p, encoding="utf-8"))
    d["s7"]["hintergruende"] = {"kicker": "Für deine Geräte", "h2": "Hintergrundbilder.",
                                "lead": "Dunkel wie der Footer der Website, damit nichts blendet – mit Logo und Grundaussage. Für MacBook, iPad, iPhone sowie Teams und Zoom; Uhr, Dock und die Person im Videocall bleiben frei. Klick auf ein Bild öffnet es in voller Größe.",
                                "varianten": daten}
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    print(len(liste), "Bilder")


if __name__ == "__main__":
    main()
