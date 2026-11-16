"""Strukturbild Homepage-Story 8 (Daniel, 16.11.2026): der Trichter in zwei Stufen, der Vertrieb als drei Verben.

Logik:  Aufbauen · Betreiben (Trichter, sofort sichtbar)  →  Ansprechen · Terminieren · Beraten (Vertrieb, Agentur)  →  Betreuen
Die zwei Trichterstufen sind deckungsgleich mit den Paketen:
  Mit deinem Team (A): wir bauen auf, du betreibst · Marketing as a Service (B): wir bauen auf und betreiben.
Baut auf story7/erklaerbild.py auf (Logo, Lagen, Formsprache) und schreibt s7.ek_quer und s7.ek_hoch in story8.11tydata.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "story7"))
import erklaerbild as eb  # noqa: E402

text, logo, svg = eb.text, eb.logo, eb.svg
MUND, HALS, MUND_H, LAGEN = eb.MUND, eb.HALS, eb.MUND_H, eb.LAGEN

TX = {
    "marketing": "Marketing – wir gewinnen Interessenten",
    "vertrieb": "Vertrieb – du machst daraus Kunden",
    "aufbauen": "Aufbauen", "aufbauen_unter": "Zielgruppen, Kanäle, Medien",
    "betreiben": "Betreiben", "betreiben_unter": "Posten, vernetzen, nachhalten",
    "messpunkt": "Messpunkt: Leads",
    "vertrieb_band": "Vertrieb", "vertrieb_unter": "Ansprechen · Terminieren · Beraten",
    "betreuen": "Betreuen", "betreuen_unter": "Bestand halten und ausbauen",
    "a": ("Mit deinem Team:", "Wir bauen auf, du betreibst."),
    "b": ("Marketing as a Service:", "Wir bauen auf und betreiben."),
    "rueck": "Regelmäßige Präsenz pflegt deinen Bestand – und bringt neue Anlässe.",
}


def quer(klammern=True):
    K, G = 15, 20
    W = 1120
    OX = 26                                   # Platz links für den Rückweg
    c = 236
    x_flach, x_kurve, x_hals = OX + 170, OX + 400, OX + 470
    x_teil = OX + 214                         # Grenze Aufbauen | Betreiben
    LU = eb.LUECKE
    o = []
    # Phasen-Klammern oben
    o.append(text(0, 20, TX["marketing"], "ek2-t", K, 600))
    o.append(f'<path d="M0 34 H{x_hals}" class="ek2-linie"/>')
    o.append(text(x_hals + LU, 20, TX["vertrieb"], "ek2-t", K, 600))
    o.append(f'<path d="M{x_hals + LU} 34 H{W}" class="ek2-linie"/>')
    # Stufen im Trichter: Aufbauen | Betreiben
    o.append(text(OX, 76, TX["aufbauen"], "ek2-t", G, 700))
    o.append(text(OX, 98, TX["aufbauen_unter"], "ek2-grau", K))
    o.append(text(x_teil + 14, 76, TX["betreiben"], "ek2-t", G, 700))
    o.append(text(x_teil + 14, 98, TX["betreiben_unter"], "ek2-grau", K))
    # Trichter aus Lagen
    for k in (3, 2, 1, 0):
        hm, hh = MUND[k], HALS[k]
        d = (f"M{OX} {c - hm} H{x_flach} C{x_flach + 130} {c - hm} {x_kurve - 100} {c - hh} {x_kurve} {c - hh} H{x_hals} "
             f"V{c + hh} H{x_kurve} C{x_kurve - 100} {c + hh} {x_flach + 130} {c + hm} {x_flach} {c + hm} H{OX} Z")
        o.append(f'<path d="{d}" class="{LAGEN[k][0]} ek2-lage"/>')
    # Trennlinie der beiden Stufen, durch den Trichter
    # Schnitt wie zwischen Vertrieb und Betreuen: spitz nach rechts, durch alle Lagen (weiße Fuge)
    o.append(f'<path d="M{x_teil - 11} {c - MUND[3] - 2} L{x_teil + 11} {c} L{x_teil - 11} {c + MUND[3] + 2}" class="ek2-schnitt"/>')
    o.append(logo(OX + 26, c, 150, "ek8q"))
    for i in range(3):
        o.append(f'<circle cx="{x_kurve - 30 + i * 16}" cy="{c}" r="4" class="ek2-kern-p"/>')
    # Messpunkt
    xm = x_hals + LU / 2
    o.append(f'<path d="M{xm} {c - HALS[3]} V{c - HALS[3] - 34}" class="ek2-linie ek2-linie--fein"/>')
    o.append(text(xm, c - HALS[3] - 42, TX["messpunkt"], "ek2-t", K, 700, "middle"))
    # Vertrieb und Betreuen als Band
    y0, y1 = c - HALS[3], c + HALS[3]
    xv = x_hals + LU
    o.append(f'<path d="M{xv} {y0} H800 L822 {c} L800 {y1} H{xv} Z" class="ek2-band"/>')
    o.append(f'<path d="M812 {y0} H{W - 16} Q{W} {y0} {W} {y0 + 16} V{y1 - 16} Q{W} {y1} {W - 16} {y1} H812 L834 {c} Z" class="ek2-band"/>')
    for x, titel, unter in ((xv + 28, TX["vertrieb_band"], TX["vertrieb_unter"]), (862, TX["betreuen"], TX["betreuen_unter"])):
        o.append(text(x, c - 3, titel, "ek2-band-t", G, 700))
        o.append(text(x, c + 21, unter, "ek2-band-s", K))
    # Pakete: welche Stufen sofort sichtbar übernimmt (Klammern unter dem Trichter) – nur im Detailbild
    ya, yb = c + MUND[3] + 34, c + MUND[3] + 72
    if not klammern:
        yb = c + MUND[3] + 2
    for y, x_ende, (fett, rest) in (((ya, x_teil, TX["a"]), (yb, x_hals, TX["b"])) if klammern else ()):
        o.append(f'<path d="M{OX} {y - 8} V{y} H{x_ende} V{y - 8}" class="ek2-linie"/>')
        o.append(f'<text x="{x_ende + 16}" y="{y + 5}" class="ek2-t" font-size="{K}"><tspan font-weight="700">{fett}</tspan> {rest}</text>')
    # Rückweg: von Betreuen um alles herum zurück an die Öffnung des Trichters
    yr = yb + 46
    o.append(f'<path d="M{W - 60} {y1} V{yr} H8 V{c} H{OX - 4}" class="ek2-linie ek2-linie--fein" marker-end="url(#ek2-pfeil-quer)"/>')
    o.append(f'<rect x="{W / 2 - 285}" y="{yr - 13}" width="570" height="26" class="ek2-grund"/>')
    o.append(text(W / 2, yr + 5, TX["rueck"], "ek2-t", K, anker="middle"))
    return svg(W, yr + 16, "".join(o), "ek2-svg--quer", "quer")


def hoch(kopf=False):
    """Handy: Bogen-Fuge mit großer Mündung (Form B, Daniel 16.11.2026) – Aufbauen im Kern, Betreiben rechts neben der schmalen Stelle"""
    W, c = 340, 170
    HB = [30, 38, 46, 54]            # Form B: graue Lagen an der Mündung bleiben breit
    y_oben = 56
    y_flach, y_kurve, y_hals = y_oben + 96, y_oben + 266, y_oben + 316
    y_teil = y_oben + 132
    o = []
    o.append(text(c, 30, TX["marketing"], "ek2-t", gewicht=600, anker="middle"))
    for k in (3, 2, 1, 0):
        hm, hh = MUND_H[k], HB[k]
        d = (f"M{c - hm} {y_oben} V{y_flach} C{c - hm} {y_flach + 90} {c - hh} {y_kurve - 70} {c - hh} {y_kurve} V{y_hals} "
             f"H{c + hh} V{y_kurve} C{c + hh} {y_kurve - 70} {c + hm} {y_flach + 90} {c + hm} {y_flach} V{y_oben} Z")
        o.append(f'<path d="{d}" class="{LAGEN[k][0]}-h ek2-lage"/>')
    # Aufbauen im Kern, wie im Querformat
    o.append(text(c, y_oben + 40, TX["aufbauen"], "ek2-kern-t", eb.T_GROSS, 700, "middle"))
    o.append(text(c, y_oben + 62, "Zielgruppen,", "ek2-kern-s", anker="middle"))
    o.append(text(c, y_oben + 78, "Kanäle, Medien", "ek2-kern-s", anker="middle"))
    # weiche Fuge, nach unten gewölbt wie die Strömung
    o.append(f'<path d="M{c - MUND_H[3] - 4} {y_teil - 8} C{c - 50} {y_teil + 16} {c + 50} {y_teil + 16} {c + MUND_H[3] + 4} {y_teil - 8}" class="ek2-fuge"/>')
    # Betreiben rechts neben der schmalen Stelle
    o.append(text(c + HB[3] + 18, y_kurve - 30, TX["betreiben"], "ek2-t", eb.T_GROSS, 700))
    o.append(text(c + HB[3] + 18, y_kurve - 10, "Posten, vernetzen,", "ek2-grau"))
    o.append(text(c + HB[3] + 18, y_kurve + 6, "nachhalten", "ek2-grau"))
    # Messpunkt links
    o.append(f'<path d="M{c - HB[3]} {y_hals - 14} H{c - HB[3] - 18}" class="ek2-linie ek2-linie--fein"/>')
    o.append(text(c - HB[3] - 24, y_hals - 18, "Messpunkt:", "ek2-t", gewicht=700, anker="end"))
    o.append(text(c - HB[3] - 24, y_hals - 2, "Leads", "ek2-t", gewicht=700, anker="end"))
    o.append(text(c, y_hals + 44, TX["vertrieb"], "ek2-t", gewicht=600, anker="middle"))
    y_hals += 42
    x0, x1 = 50, W - 50
    o.append(f'<path d="M{x0} {y_hals + 14} H{x1} V{y_hals + 84} L{c} {y_hals + 100} L{x0} {y_hals + 84} Z" class="ek2-band"/>')
    yk = y_hals + 108
    o.append(f'<path d="M{x0} {yk} L{c} {yk + 16} L{x1} {yk} V{yk + 70} Q{x1} {yk + 86} {x1 - 16} {yk + 86} H{x0 + 16} Q{x0} {yk + 86} {x0} {yk + 70} Z" class="ek2-band"/>')
    for y, titel, unter in ((y_hals + 48, TX["vertrieb_band"], TX["vertrieb_unter"]), (yk + 50, TX["betreuen"], TX["betreuen_unter"])):
        o.append(text(c, y, titel, "ek2-band-t", eb.T_GROSS, 700, "middle"))
        o.append(text(c, y + 21, unter, "ek2-band-s", anker="middle"))
    return svg(W, yk + 100, "".join(o), "ek2-svg--hoch", "hoch")

if __name__ == "__main__":
    p = os.path.join(HERE, "story8.11tydata.json")
    d = json.load(open(p, encoding="utf-8"))
    d["s7"]["ek_quer_detail"] = quer()
    d["s7"]["ek_hoch_detail"] = hoch()
    d["s7"]["ek_quer"] = quer(klammern=False)   # Kopf der Startseite: zwei Stufen, ohne Paket-Klammern
    d["s7"]["ek_hoch"] = hoch()
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    print("Strukturbild Story 8 geschrieben")
