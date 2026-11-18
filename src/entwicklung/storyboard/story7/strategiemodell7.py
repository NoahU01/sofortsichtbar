#!/usr/bin/env python3
"""Strategiemodell für Versicherungsagenturen – im Stil von sofort sichtbar (Daniel, 18.11.2026).

Grundlogik und Nummern aus dem empiria-Strategiemodell (empiria-Repo, werkzeuge/pdf-seiten/sk/strategiemodell.svg), für das
Unternehmen (die Agentur): 1 Ausgangssituation, 2 Vision mit dem zukünftigen Geschäftsmodell, Positionierung und Pitch
(„Wie wollen wir wahrgenommen werden?“, das Zentrale), 3 Strategie („Wie kommen wir dorthin?“); darüber das
Selbstverständnis („Wofür stehen wir?“).

Zwei Blätter, hell, ohne schwarzen Balken (zum Drucken); die Übersicht A3 hoch ist gestrichen (Daniel, 18.11.2026):
  Arbeitsblatt A  A3 quer – Ausschnitt: links 1 Ausgangssituation, Mitte 3 Strategie, rechts 2 Vision
  Arbeitsblatt B  A3 quer – drei Kästen wie im Strategiemodell: oben „Wofür stehen wir?“, links breit 1 + 3, rechts schmal 2

SCHRIFTSYSTEM (fest):
  Kopf 1:1 wie das Arbeitsblatt „Vom ersten Kontakt zum Kunden“ (onepager7.py, kopf_hoch): links Subheadline, Überschrift,
  ein Satz; rechts oben das Logo; Rand 20 mm; unten rechts sofortsichtbar.de
  Inter Tight 700 – Hauptüberschrift 42 pt (eine Größe, Akzentwort im Verlauf); alle übrigen Überschriften 15 pt
  Inter 400/600   – Text 10 pt (Regular, Hervorhebung SemiBold), Satz unter der Überschrift 10,6 pt wie im Vorbild;
                    Nebeninfos 8 pt (Grau)
  Farben          – Tinte #1d1d1f, Grau #6e6e73, Linien #d2d2d7; Verlauf Cyan → Violett nur im Akzentwort der Hauptüberschrift
                    und in den Nummernkreisen

Aufruf: python3 src/entwicklung/storyboard/story7/strategiemodell7.py
Ergebnis: story7/assets/strategiemodell/*.pdf und *.png, s7.strategiemodell in story7.11tydata.json
"""
import hashlib
import html
import json
import os
import subprocess
import tempfile

from maas_pdf7 import VERLAUF_JS  # Verlaufswort als SVG-Text wie im Vorbild (keine Randlinien im Druck)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ZIEL = os.path.join(HERE, "assets", "strategiemodell")
FONTS = os.path.join(HERE, "assets", "fonts")
LOGO = os.path.join(SRC, "entwicklung", "storyboard", "story6", "assets", "img", "logo-dunkel.svg")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
e = html.escape

# Inhalte (eine Quelle für Übersicht und Arbeitsblätter)
Z_WAHR, Z_WEG, Z_WOFUER = "Wie wollen wir wahrgenommen werden?", "Wie kommen wir dorthin?", "Wofür stehen wir?"
GM = {
    "nr": "2", "titel": "Zukünftiges Geschäftsmodell", "unter": "mit Positionierung und Pitch",
    "kurz": "Das Zentrale: wie die Agentur in drei bis fünf Jahren arbeitet – und warum Kunden genau zu ihr kommen.",
    "punkte": [("Zielgruppen und Sparten", "Wen sprechen wir an, womit wachsen wir?"),
               ("Problem und Mehrwert", "Welches Problem lösen wir für diese Kunden?"),
               ("Positionierung", "Was macht uns einzigartig – im Vergleich zu anderen Agenturen und Maklern?"),
               ("Organisationsmodell", "Team, Rollen und Wege zum Kunden: vor Ort, digital, im Bestand."),
               ("Pitch", "Wie erklären wir das in einem Satz?")],
    "frage": "Welches Problem lösen wir – und was macht uns einzigartig?",
    "vision": "Vision: das Zielbild in einem Satz · Mission: was wir dafür jeden Tag tun",
}
AUSGANG = {"nr": "1", "titel": "Ausgangssituation", "unter": "Heutiges Geschäfts- und Organisationsmodell",
           "kurz": "Wo stehen wir heute? Bestand, Sparten, Team, Abläufe – was ist stark, was fehlt?"}
STRATEGIE = {"nr": "3", "titel": "Strategie", "unter": "Stoßrichtungen und Handlungsfelder",
             "kurz": "Der Weg vom Heute zum Zielbild: wenige Stoßrichtungen, je mit konkreten Handlungsfeldern und einem Zeitplan.",
             "detail": [("Führungs- und Arbeitsalltag", "Wie sichern wir die Zielerreichung?"),
                        ("Strategiekommunikation", "Wie erklären wir die Strategie im Team?")]}
LEITBILD = {"titel": "Selbstverständnis", "unter": "Leitbild der Agentur",
            "kurz": "Entsteht zuletzt und fasst alles zusammen: was für uns, unser Team und unsere Kunden gilt.",
            "punkte": [("Selbstbild", "Wer wir sind und was uns antreibt."),
                       ("Unternehmensstrategie", "Wohin wir als Agentur wollen – in einem Satz."),
                       ("Führungsverständnis", "Wie wir führen und zusammenarbeiten."),
                       ("Zielgruppe", "„What's in it for me?“ – was unsere Kunden davon haben.")]}
REIHENFOLGE = "Erst die Ausgangssituation, dann die Vision mit dem zukünftigen Geschäftsmodell, dann die Strategie als Weg dorthin. Das Selbstverständnis fasst zuletzt alles zusammen."


def schriften():
    out = ""
    for fam, datei, w in (("Inter", "inter", 400), ("Inter", "inter", 600), ("Inter Tight", "inter-tight", 700)):
        for sub in ("latin", "latin-ext"):
            out += f'@font-face{{font-family:"{fam}";font-weight:{w};src:url("file://{FONTS}/{datei}-{sub}-{w}-normal.woff2")}}'
    return out


CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{color:#1d1d1f;font:400 10pt/1.45 Inter,sans-serif}
.blatt{position:relative;overflow:hidden;background:#fff}
.blatt{display:flex;flex-direction:column;width:420mm;height:297mm;padding:20mm 20mm 0}
.kopf{display:grid;grid-template-columns:1fr auto;column-gap:10mm;align-items:start;padding-bottom:9mm}
.kopf img{display:block;height:9mm;margin-top:.7pt}
.kopf .kicker{color:#6e6e73;font-size:8pt;font-weight:600;line-height:1}
.kopf h1{margin-top:4mm}
.kopf .lead{margin-top:5mm;color:#424245;font-size:10.6pt;line-height:1.45}
.flaeche{flex:1;min-height:0}
.art{color:#6e6e73;font-size:8pt;font-weight:600}
h1{font:700 42pt/1 'Inter Tight';letter-spacing:-.025em}
h1 .v{color:#0b9fbd}
h2{font:700 15pt/1.15 'Inter Tight';letter-spacing:-.02em}
.klein{color:#6e6e73;font-size:8pt;line-height:1.4}
.grau{color:#6e6e73}
b{font-weight:600}
.nr{display:inline-grid;place-items:center;width:7mm;height:7mm;border-radius:50%;background:linear-gradient(135deg,#0b9fbd,#8613a1);color:#fff;font:700 10pt 'Inter Tight';flex:none}
.zone{color:#6e6e73;font-size:8pt;font-weight:600}
.fuss{padding:7mm 0 12mm;text-align:right;color:#1d1d1f;font-size:10pt;font-weight:600;line-height:1}
.kasten{border:0.35mm solid #d2d2d7;border-radius:4mm;padding:7.5mm}
.kasten--kern{border:0.7mm solid #1d1d1f}
.titel{display:flex;align-items:center;gap:3.2mm}
.titel > span:not(.nr){display:block}
.frage{margin-top:4mm;padding-top:3mm;border-top:0.3mm solid #d2d2d7}
.frage .klein{display:block;margin-bottom:.6mm}
.linien{flex:1}
"""


def logo():
    return f'<img src="file://{LOGO}" alt="sofort sichtbar">'


def titel(x, gross=True):
    nr = f'<span class="nr">{x["nr"]}</span>' if x.get("nr") else ""
    return f'<div class="titel">{nr}<span><h2>{e(x["titel"])}</h2>' + (f'<span class="klein" style="display:block">{e(x["unter"])}</span>' if x.get("unter") else "") + '</span></div>'


def punkte(liste):
    return "".join(f'<p style="margin-top:3.2mm"><b>{e(a)}</b> – {e(b)}</p>' for a, b in liste)


VISION = dict(GM, titel="Vision", unter="Zukünftiges Geschäfts- und Organisationsmodell inklusive Positionierung",
              kurz="Das Zentrale: Zielgruppen und Sparten, das Problem, das wir lösen, was uns einzigartig macht – und der Pitch in einem Satz.")


def teil(x, stil=""):
    """Ein Bereich zum Reinschreiben: Nummer, Titel, kurze Erklärung, darunter freie Fläche."""
    return (f'<div style="display:flex;flex-direction:column;min-width:0;{stil}">{titel(x)}'
            f'<p class="klein" style="margin-top:1.5mm;max-width:95mm">{e(x["kurz"])}</p><div class="linien"></div></div>')


def kasten(frage, inhalt, stil=""):
    return (f'<div class="kasten" style="display:flex;flex-direction:column;gap:4mm;padding:5mm 6mm;{stil}">'
            f'<p class="zone" style="text-align:center">{e(frage)}</p>{inhalt}</div>')


def kopf(kicker, h1, akzent, lead):
    return (f'<div class="kopf"><div><p class="kicker">{e(kicker)}</p><h1>{e(h1)} <span class="v">{e(akzent)}</span></h1>'
            f'<p class="lead">{e(lead)}</p></div>{logo()}</div>')


def blatt(kopf_, flaeche):
    return f'<div class="blatt">{kopf_}<div class="flaeche">{flaeche}</div><p class="fuss">sofortsichtbar.de</p></div>', "420mm 297mm"


def arbeitsblatt_a():
    """Ausschnitt des Strategiemodells: links 1 Ausgangssituation, in der Mitte 3 Strategie, rechts 2 Vision."""
    # Zonen wie im Modell: 1 und 3 gehören zu „Wie kommen wir dorthin?“, 2 zu „Wie wollen wir wahrgenommen werden?“
    feld = lambda x: f'<div class="kasten" style="display:flex;padding:5mm 6mm;min-height:0">{teil(x, "flex:1")}</div>'
    flaeche = (f'<div style="height:100%;display:grid;grid-template-columns:1fr 1fr 1fr;grid-template-rows:auto 1fr;gap:3mm 8mm">'
               f'<p class="zone" style="grid-column:1/3">{e(Z_WEG)}</p><p class="zone">{e(Z_WAHR)}</p>'
               + feld(AUSGANG) + feld(STRATEGIE) + feld(VISION) + '</div>')
    return blatt(kopf("Strategiemodell für deine Agentur", "Vom Heute", "zur Vision.",
                      "Wo deine Agentur heute steht, wie sie in Zukunft wahrgenommen werden will und welche Strategie dorthin führt."), flaeche)


def arbeitsblatt_b():
    """Drei Kästen wie im Strategiemodell: oben quer „Wofür stehen wir?“ (Selbstverständnis), darunter links der breite Kasten
    „Wie kommen wir dorthin?“ mit 1 Ausgangssituation und 3 Strategie, rechts der schmälere „Wie wollen wir wahrgenommen werden?“
    mit 2 Vision. Der Pfeil vom Selbstverständnis zur Vision wie im Modell."""
    oben = kasten(Z_WOFUER, teil(LEITBILD, "flex:1"), "height:46mm")
    links = kasten(Z_WEG, f'<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;min-height:0">'
                   f'{teil(AUSGANG, "padding-right:6mm")}{teil(STRATEGIE, "padding-left:6mm;border-left:0.35mm solid #d2d2d7")}</div>')
    rechts = kasten(Z_WAHR, teil(VISION, "flex:1"))
    pfeil = ('<svg width="3mm" height="7mm" viewBox="0 0 3 7" style="display:block;margin:0 auto">'
             '<path d="M1.5 .6 V6.2 M.4 5 L1.5 6.3 L2.6 5" fill="none" stroke="#1d1d1f" stroke-width=".3"/></svg>')
    flaeche = (f'<div style="height:100%;display:grid;grid-template-columns:1.6fr 1fr;grid-template-rows:auto 7mm 1fr;column-gap:8mm">'
               f'<div style="grid-column:1/3;display:flex;flex-direction:column">{oben}</div>'
               f'<div></div><div>{pfeil}</div>{links}{rechts}</div>')
    return blatt(kopf("Strategiemodell für deine Agentur", "Das Strategiemodell", "auf einem Blatt.",
                      "Wofür deine Agentur steht, wie sie wahrgenommen werden will und wie sie dorthin kommt."), flaeche)


def drucken(name, blatt, groesse):
    tmp = tempfile.mkdtemp(prefix="sm7_")
    h = os.path.join(tmp, name + ".html")
    open(h, "w").write(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{schriften()}{CSS}@page{{size:{groesse};margin:0}}</style></head><body>{blatt}{VERLAUF_JS}</body></html>')
    pdf = os.path.join(ZIEL, name + ".pdf")
    for _ in range(3):
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                            "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", "file://" + h], capture_output=True)
        if r.returncode == 0:
            break
    subprocess.run(["pdftoppm", "-r", "90", "-png", "-singlefile", pdf, os.path.join(ZIEL, name)], check=True)
    return hashlib.md5(open(pdf, "rb").read()).hexdigest()[:8]


def main():
    os.makedirs(ZIEL, exist_ok=True)
    blaetter = [("strategiemodell-arbeitsblatt-a-a3-quer", "Arbeitsblatt A", "A3 quer · Ausschnitt des Strategiemodells", arbeitsblatt_a),
                ("strategiemodell-arbeitsblatt-b-a3-quer", "Arbeitsblatt B", "A3 quer · drei Kästen wie im Strategiemodell", arbeitsblatt_b)]
    daten = []
    for name, titel_, text, fn in blaetter:
        blatt, groesse = fn()
        v = drucken(name, blatt, groesse)
        daten.append({"name": titel_, "text": text, "pdf": f"{name}.pdf?v={v}", "png": f"{name}.png?v={v}"})
    p = os.path.join(HERE, "story7.11tydata.json")
    d = json.load(open(p, encoding="utf-8"))
    d["s7"]["strategiemodell"] = {"kicker": "Arbeitsblatt", "h2": "Das Strategiemodell.",
                                  "lead": "Für die Agentur, nummeriert wie im Strategiemodell: 1 Ausgangssituation, 2 Vision mit dem zukünftigen Geschäfts- und Organisationsmodell inklusive Positionierung, 3 Strategie – darüber das Selbstverständnis. Hell und ohne Balken – zum Ausdrucken.",
                                  "blaetter": daten}
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    print("ok", [x["name"] for x in daten])


if __name__ == "__main__":
    main()
