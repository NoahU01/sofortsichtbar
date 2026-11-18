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
    ("akzent", "Akzent", "„Die digitale Maschine“ klein in Grau, „vor deinem Vertrieb.“ groß im Verlauf – dahinter gedämpftes Licht."),
    ("oberflaeche", "Oberfläche", "Ein Stück unserer Produktoberfläche läuft dunkel aus dem Bild: Strecken, fertige Postings, „Heute dran“."),
]


def schriften():
    out = ""
    for fam, datei, w in (("Inter", "inter", 500), ("Inter Tight", "inter-tight", 700)):
        for sub in ("latin", "latin-ext"):
            out += f'@font-face{{font-family:"{fam}";font-weight:{w};src:url("file://{FONTS}/{datei}-{sub}-{w}-normal.woff2")}}'
    return out


def satz(art, var):
    zwei = art in ("iphone", "video")
    if var == "akzent":
        oben = "Die digitale Maschine"
        unten = "vor deinem<br>Vertrieb." if zwei else "vor deinem Vertrieb."
        return f'<span class="k">{oben}</span><span class="v gross">{unten}</span>'
    if zwei:
        return 'Die digitale<br>Maschine<br><span class="v">vor deinem<br>Vertrieb.</span>'
    return 'Die digitale Maschine<br><span class="v">vor deinem Vertrieb.</span>'


def oberflaeche(breite, mobil=False):
    """Arbeitsplatz aus Story 9 in dunkler Fassung (eine Breite in Punkten, alles relativ dazu)"""
    e = breite / 100
    if mobil:  # iPhone: zwei Benachrichtigungen statt Fenster
        def note(t, u):
            return (f'<div style="display:flex;align-items:center;gap:{3 * e}px;padding:{3.4 * e}px {4 * e}px;margin-top:{2.4 * e}px;border-radius:{5 * e}px;background:rgba(255,255,255,.08);box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)">'
                    f'<span style="flex:none;width:{9 * e}px;height:{9 * e}px;border-radius:{2.4 * e}px;background:linear-gradient(135deg,#0b9fbd,#8613a1)"></span>'
                    f'<div><b style="display:block;color:#f5f5f7;font:600 {4.2 * e}px Inter">{t}</b><span style="color:#8e8e93;font:500 {3.5 * e}px Inter">{u}</span></div></div>')
        return note("Posting ist live", "Private Bauherren · jetzt") + note("Neue Anfrage", "Familie K. · Rückruf gewünscht")
    def post(bg, t):
        return (f'<div><div style="height:{14 * e}px;border-radius:{1.6 * e}px;background:{bg};display:flex;align-items:flex-end;padding:{1.2 * e}px">'
                f'<b style="color:#fff;font:700 {1.7 * e}px/1.05 \'Inter Tight\'">{t}</b></div></div>')
    zeile = lambda t, an=False: (f'<p style="display:flex;align-items:center;gap:{1 * e}px;padding:{1 * e}px {1.2 * e}px;border-radius:{1.2 * e}px;margin-top:{.5 * e}px;'
                                 f'background:{"rgba(255,255,255,.07)" if an else "transparent"};color:{"#f5f5f7" if an else "#8e8e93"};font:600 {1.6 * e}px Inter">'
                                 f'<i style="width:{.9 * e}px;height:{.9 * e}px;border-radius:50%;background:{"linear-gradient(135deg,#0b9fbd,#8613a1)" if an else "#48484a"}"></i>{t}</p>')
    return (f'<div style="width:{breite}px;border-radius:{2.2 * e}px;background:#2c2c2e;box-shadow:0 {3 * e}px {8 * e}px rgba(0,0,0,.45),inset 0 0 0 1px rgba(255,255,255,.06);overflow:hidden">'
            f'<p style="display:flex;gap:{.8 * e}px;align-items:center;height:{4 * e}px;padding:0 {1.6 * e}px;border-bottom:1px solid rgba(255,255,255,.07)">'
            + "".join(f'<i style="width:{1 * e}px;height:{1 * e}px;border-radius:50%;background:#48484a"></i>' for _ in range(3))
            + f'<b style="margin-left:{1.4 * e}px;color:#a1a1a6;font:600 {1.4 * e}px Inter">sofort sichtbar · Arbeitsplatz</b></p>'
            f'<div style="display:grid;grid-template-columns:{20 * e}px 1fr {22 * e}px">'
            f'<div style="padding:{2 * e}px {1.4 * e}px;border-right:1px solid rgba(255,255,255,.07)">{zeile("Private Bauherren", True)}{zeile("Junge Familien")}{zeile("Berufseinsteiger")}{zeile("Landwirte")}</div>'
            f'<div style="padding:{2.2 * e}px"><b style="color:#f5f5f7;font:700 {2.6 * e}px \'Inter Tight\'">Private Bauherren</b>'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:{1.2 * e}px;margin-top:{2 * e}px">'
            + post("linear-gradient(160deg,#0b9fbd,#3d5bd1)", "Bauen ist teuer genug.") + post("#3a3a3c", "Checkliste Hausbau") + post("linear-gradient(160deg,#3d5bd1,#8613a1)", "Rohbau versichert?")
            + f'</div></div><div style="padding:{2 * e}px {1.6 * e}px;border-left:1px solid rgba(255,255,255,.07)">'
            f'<p style="color:#8e8e93;font:600 {1.3 * e}px Inter">Heute dran</p>'
            f'<div style="margin-top:{1 * e}px;padding:{1.4 * e}px;border-radius:{1.4 * e}px;background:rgba(255,255,255,.06);box-shadow:inset 0 0 0 {.2 * e}px #3d5bd1">'
            f'<b style="color:#f5f5f7;font:600 {1.5 * e}px Inter">Posting Bauherren</b><span style="display:inline-block;margin-top:{1 * e}px;padding:{.6 * e}px {1.4 * e}px;border-radius:99px;background:#f5f5f7;color:#1d1d1f;font:600 {1.3 * e}px Inter">Veröffentlichen</span></div>'
            f'<div style="margin-top:{1 * e}px;padding:{1.4 * e}px;border-radius:{1.4 * e}px;background:rgba(255,255,255,.04)"><b style="color:#d2d2d7;font:600 {1.5 * e}px Inter">Rückruf Familie K.</b></div>'
            f'</div></div></div>')


def bild(gkey, w, h, art, var):
    """Logo und Satz bilden einen Block: Logo klein, linksbündig mit dem Satz, fester Abstand darüber."""
    if art == "mac":
        size = .046 * w if var != "akzent" else .064 * w
        block = dict(left=.08 * w, mitte_y=.47 * h, align="left")
        if var == "oberflaeche":
            size = .04 * w
    elif art == "ipad":
        size = .06 * w if var != "akzent" else .075 * w
        block = dict(left=0, mitte_y=.45 * h if var != "oberflaeche" else .33 * h, align="center", breite=w)
    elif art == "iphone":
        size = .11 * w if var != "akzent" else .15 * w
        block = dict(left=.10 * w, mitte_y=.52 * h if var != "oberflaeche" else .47 * h, align="left")
    else:  # Teams/Zoom: Block am linken Rand, vertikal mittig – die Person sitzt in der Mitte
        size = .034 * w if var != "akzent" else .045 * w
        block = dict(left=.05 * w, mitte_y=.5 * h, align="left")
    logo_h = size * .72
    ausr = "flex-start" if block["align"] == "left" else "center"
    breite = f'width:{block["breite"]}px;' if block.get("breite") else ""
    blk = (f'<div style="position:absolute;left:{block["left"]:.1f}px;top:{block["mitte_y"]:.1f}px;transform:translateY(-50%);{breite}'
           f'display:flex;flex-direction:column;align-items:{ausr};gap:{size * .75:.1f}px">'
           f'<img src="file://{LOGO}" style="height:{logo_h:.1f}px;display:block">'
           f'<p style="margin:0;font:700 {size:.1f}px/1.03 \'Inter Tight\';letter-spacing:-.035em;color:#f5f5f7;text-align:{block["align"]}">{satz(art, var)}</p></div>')
    hintergrund = BG
    extra = ""
    if var == "akzent":
        lage = {"mac": "30% 62%", "ipad": "50% 58%", "iphone": "30% 60%", "video": "18% 60%"}[art]
        hintergrund = f"radial-gradient(42% 38% at {lage}, rgba(134,19,161,.28), transparent 72%), radial-gradient(30% 28% at {lage}, rgba(11,159,189,.16), transparent 70%), {BG}"
    if var == "oberflaeche":
        if art == "mac":
            extra = f'<div style="position:absolute;left:{.52 * w:.0f}px;top:{.24 * h:.0f}px">{oberflaeche(.78 * w)}</div>'
        elif art == "ipad":
            extra = f'<div style="position:absolute;left:{.16 * w:.0f}px;top:{.50 * h:.0f}px">{oberflaeche(.9 * w)}</div>'
        elif art == "iphone":
            extra = f'<div style="position:absolute;left:{.10 * w:.0f}px;top:{.62 * h:.0f}px;width:{.80 * w:.0f}px">{oberflaeche(.8 * w, True)}</div>'
        else:
            extra = f'<div style="position:absolute;left:{.66 * w:.0f}px;top:{.22 * h:.0f}px">{oberflaeche(.7 * w)}</div>'
    css = (schriften() + f"*{{margin:0;box-sizing:border-box}}html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{BG}}}"
           ".v{background:linear-gradient(100deg,#19b6d4,#a64fd0);-webkit-background-clip:text;background-clip:text;color:transparent}"
           ".k{display:block;color:#86868b;font-family:Inter;font-weight:500;font-size:.42em;letter-spacing:0;margin-bottom:.25em}.gross{display:block}"
           "p,b,span,i{font-style:normal}")
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div style="position:relative;width:{w}px;height:{h}px;background:{hintergrund};overflow:hidden">{extra}{blk}</div></body></html>'


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
                                "lead": "Dunkel wie der Footer der Website, damit nichts blendet – mit Logo und Grundaussage. Für MacBook, iPad, iPhone sowie Teams und Zoom; Uhr, Dock und die Person im Videocall bleiben frei. Klick auf ein Bild öffnet es in voller Größe.",
                                "varianten": daten}
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    print(len(liste), "Bilder")


if __name__ == "__main__":
    main()
