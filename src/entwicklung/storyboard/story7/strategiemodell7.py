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
  Inter Tight 700 – Hauptüberschrift 32 pt (eine Größe, Akzentwort im Verlauf); alle übrigen Überschriften 15 pt
  Inter 400/600   – Text 10 pt (Regular, Hervorhebung SemiBold); Nebeninfos 8 pt (Grau)
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
.kopf{display:flex;justify-content:space-between;align-items:flex-start}
.kopf img{height:11mm}
.art{color:#6e6e73;font-size:8pt;font-weight:600}
h1{font:700 32pt/1.04 'Inter Tight';letter-spacing:-.03em}
h1 .v{background:linear-gradient(100deg,#0b9fbd,#8613a1);-webkit-background-clip:text;background-clip:text;color:transparent}
h2{font:700 15pt/1.15 'Inter Tight';letter-spacing:-.02em}
.klein{color:#6e6e73;font-size:8pt;line-height:1.4}
.grau{color:#6e6e73}
b{font-weight:600}
.nr{display:inline-grid;place-items:center;width:7mm;height:7mm;border-radius:50%;background:linear-gradient(135deg,#0b9fbd,#8613a1);color:#fff;font:700 10pt 'Inter Tight';flex:none}
.zone{color:#6e6e73;font-size:8pt;font-weight:600}
.fuss{position:absolute;right:18mm;bottom:12mm;color:#6e6e73;font-size:8pt;font-weight:600}
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


def kopf_quer(art):
    return (f'<div class="kopf" style="align-items:center">{logo()}<span style="display:flex;gap:10mm;align-items:center">'
            f'<span class="art">Strategiemodell · {art}</span><span class="art">Agentur: ______________________</span>'
            f'<span class="art">Datum: ____________</span></span></div>')


def arbeitsblatt_a():
    """Ausschnitt des Strategiemodells: links 1 Ausgangssituation, in der Mitte 3 Strategie, rechts 2 Vision."""
    # Zonen wie im Modell: 1 und 3 gehören zu „Wie kommen wir dorthin?“, 2 zu „Wie wollen wir wahrgenommen werden?“
    feld = lambda x: f'<div class="kasten" style="display:flex;padding:5mm 6mm;min-height:0">{teil(x, "flex:1")}</div>'
    inhalt = (kopf_quer("Arbeitsblatt A") +
              f'<div style="position:absolute;left:18mm;right:18mm;top:36mm;bottom:20mm;display:grid;grid-template-columns:1fr 1fr 1fr;'
              f'grid-template-rows:auto 1fr;gap:3mm 8mm">'
              f'<p class="zone" style="grid-column:1/3">{e(Z_WEG)}</p><p class="zone">{e(Z_WAHR)}</p>'
              + feld(AUSGANG) + feld(STRATEGIE) + feld(VISION)
              + '</div><p class="fuss">sofortsichtbar.de</p>')
    return f'<div class="blatt" style="width:420mm;height:297mm;padding:16mm 18mm">{inhalt}</div>', "420mm 297mm"


def arbeitsblatt_b():
    """Drei Kästen wie im Strategiemodell: oben quer „Wofür stehen wir?“ (Selbstverständnis), darunter links der breite Kasten
    „Wie kommen wir dorthin?“ mit 1 Ausgangssituation und 3 Strategie, rechts der schmälere „Wie wollen wir wahrgenommen werden?“
    mit 2 Vision. Der Pfeil vom Selbstverständnis zur Vision wie im Modell."""
    oben = (f'<div style="position:absolute;left:18mm;right:18mm;top:34mm;height:60mm;display:flex">'
            + kasten(Z_WOFUER, teil(LEITBILD, "flex:1"), "flex:1") + '</div>')
    links = kasten(Z_WEG, f'<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;min-height:0">'
                   f'{teil(AUSGANG, "padding-right:6mm")}{teil(STRATEGIE, "padding-left:6mm;border-left:0.35mm solid #d2d2d7")}</div>')
    rechts = kasten(Z_WAHR, teil(VISION, "flex:1"))
    unten = (f'<div style="position:absolute;left:18mm;right:18mm;top:104mm;bottom:20mm;display:grid;grid-template-columns:1.6fr 1fr;gap:8mm">'
             f'{links}{rechts}</div>')
    # rechte Säule: Start 18 + 376/2.6*1.6 + 8 = 257.4 mm, Mitte 329.7 mm
    pfeil = ('<svg style="position:absolute;left:0;top:0" width="420mm" height="297mm" viewBox="0 0 420 297">'
             '<defs><marker id="p" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#1d1d1f" stroke-width="1.6"/></marker></defs>'
             '<path d="M329.7 95.2 V102.6" stroke="#1d1d1f" stroke-width=".5" marker-end="url(#p)"/></svg>')
    inhalt = kopf_quer("Arbeitsblatt B") + oben + unten + pfeil + '<p class="fuss">sofortsichtbar.de</p>'
    return f'<div class="blatt" style="width:420mm;height:297mm;padding:16mm 18mm">{inhalt}</div>', "420mm 297mm"


def drucken(name, blatt, groesse):
    tmp = tempfile.mkdtemp(prefix="sm7_")
    h = os.path.join(tmp, name + ".html")
    open(h, "w").write(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{schriften()}{CSS}@page{{size:{groesse};margin:0}}</style></head><body>{blatt}</body></html>')
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
