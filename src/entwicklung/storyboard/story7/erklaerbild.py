"""Erklärbild „Die digitale Maschine“ für die Startseite (Homepage-Story 7) – quer (Desktop) und hochkant (Handy).

Schema (Daniel, 11.11.2026):
- eine Leserichtung, eine Aussage: links mehr hinein, rechts mehr heraus
- nur zwei Formen: Trichter aus Lagen (Kern = Kernpaket, jeder Baustein eine Lage, die ihn breiter macht)
  und ein Prozessband so hoch wie die Mündung (Vertrieb · Kundenbetreuung, gleich gestaltet)
- ein Highlight: Farbe nur im Kern; alles andere Grautöne und Tinte
- Messpunkt als feine Linie, Rückweg als dünne Linie mit Text
- Schrift: zwei Größen (13 für Lagen und Nebentexte, 18 für das Band)

Farben und Schrift kommen per CSS-Klassen aus den Stellschrauben der Seite (keine festen Farben hier).
Aufruf: python3 erklaerbild.py → schreibt s7.ek_quer und s7.ek_hoch in story7.11tydata.json
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
T_KLEIN, T_GROSS = 13, 18

LAGEN = [  # innen → außen: (Klasse, Name)
    ("ek2-kern", "Kernpaket"),
    ("ek2-l2", "LinkedIn"),
    ("ek2-l3", "Paid Ads"),
    ("ek2-l4", "Website"),
]
MUND = [46, 70, 94, 118]   # halbe Höhe je Lage an der Öffnung
HALS = [20, 27, 34, 40]    # halbe Höhe je Lage an der Mündung (außen = halbe Bandhöhe)


# Texte der Grafik – kein Begriff doppelt (Daniel, 11.11.2026: nicht „Anfragen“, sondern Interessenten/Leads)
TX = {
    "marketing": "Marketing – wir gewinnen Interessenten",
    "vertrieb": "Vertrieb – du machst daraus Kunden",
    "kern": "sofort sichtbar",
    "messpunkt": "Messpunkt: Leads",
    "vertrieb_unter": "Termin · Beratung · Abschluss",
    "kunden_unter": "Halten und ausbauen",
    "rueck": "Regelmäßige Präsenz pflegt deinen Bestand – und bringt neue Anlässe.",
}
LUECKE = 12   # gleicher Abstand Trichter → Vertrieb wie Vertrieb → Kundenbetreuung


def text(x, y, s, klasse, groesse=T_KLEIN, gewicht=500, anker="start", extra=""):
    return (f'<text x="{x}" y="{y}" class="{klasse}" font-size="{groesse}" font-weight="{gewicht}" '
            f'text-anchor="{anker}"{extra}>{s}</text>')


def quer():
    """Querfassung mit größerer Schrift (15/20), damit sie auch bei Tablet-Breite lesbar bleibt."""
    K, G = 15, 20
    W, H, c = 1120, 380, 186
    x_flach, x_kurve, x_hals = 170, 400, 470
    o = []
    # Klammern oben: aktiv und für alle Pakete gültig; kein Begriff doppelt (Daniel, 11.11.2026)
    # Klammer = Text mit Linie darunter über genau dem Bereich, den sie meint
    o.append(text(0, 20, TX["marketing"], "ek2-t", K, 600))
    o.append(f'<path d="M0 34 H{x_hals}" class="ek2-linie"/>')
    o.append(text(x_hals + LUECKE, 20, TX["vertrieb"], "ek2-t", K, 600))
    o.append(f'<path d="M{x_hals + LUECKE} 34 H{W}" class="ek2-linie"/>')
    # Trichter aus Lagen (außen zuerst)
    for k in (3, 2, 1, 0):
        hm, hh = MUND[k], HALS[k]
        d = (f"M0 {c - hm} H{x_flach} C{x_flach + 130} {c - hm} {x_kurve - 100} {c - hh} {x_kurve} {c - hh} H{x_hals} "
             f"V{c + hh} H{x_kurve} C{x_kurve - 100} {c + hh} {x_flach + 130} {c + hm} {x_flach} {c + hm} H0 Z")
        o.append(f'<path d="{d}" class="{LAGEN[k][0]} ek2-lage"/>')
    # Unser Teil trägt den Namen: „sofort sichtbar“ im Kern; Lagen ohne Paketnamen
    o.append(text(26, c + 7, TX["kern"], "ek2-kern-t", G, 700))
    for i in range(3):
        o.append(f'<circle cx="{x_kurve - 30 + i * 16}" cy="{c}" r="4" class="ek2-kern-p"/>')
    # Messpunkt: feine Linie an der Mündung
    xm = x_hals + LUECKE / 2   # genau in der Mitte der Lücke zwischen Trichter und Vertrieb
    o.append(f'<path d="M{xm} {c - HALS[3]} V{c - HALS[3] - 34}" class="ek2-linie ek2-linie--fein"/>')
    o.append(text(xm, c - HALS[3] - 42, TX["messpunkt"], "ek2-t", K, 700, "middle"))
    # Prozessband: so hoch wie die Mündung, zwei gleich gestaltete Abschnitte
    y0, y1 = c - HALS[3], c + HALS[3]
    xv = x_hals + LUECKE
    o.append(f'<path d="M{xv} {y0} H780 L802 {c} L780 {y1} H{xv} Z" class="ek2-band"/>')
    o.append(f'<path d="M792 {y0} H{W - 16} Q{W} {y0} {W} {y0 + 16} V{y1 - 16} Q{W} {y1} {W - 16} {y1} H792 L814 {c} Z" class="ek2-band"/>')
    for x, titel, unter in ((xv + 28, "Vertrieb", TX["vertrieb_unter"]), (842, "Kundenbetreuung", TX["kunden_unter"])):
        o.append(text(x, c - 3, titel, "ek2-band-t", G, 700))
        o.append(text(x, c + 21, unter, "ek2-band-s", K))
    # Rückweg: dünne Linie mit Text, mit Abstand zum Trichter
    yr = c + MUND[3] + 58
    o.append(f'<path d="M{W - 60} {y1} V{yr} H60 V{c + MUND[3] + 8}" class="ek2-linie ek2-linie--fein" marker-end="url(#ek2-pfeil-quer)"/>')
    o.append(f'<rect x="{W / 2 - 285}" y="{yr - 13}" width="570" height="26" class="ek2-grund"/>')
    o.append(text(W / 2, yr + 5, TX["rueck"], "ek2-t", K, anker="middle"))
    return svg(W, H, "".join(o), "ek2-svg--quer", "quer")


def hoch():
    W, H, c = 340, 730, 170
    y_oben = 98
    y_flach, y_kurve, y_hals = y_oben + 86, y_oben + 266, y_oben + 316
    o = []
    o.append(text(c, 30, TX["marketing"], "ek2-t", gewicht=600, anker="middle"))
    for k in (3, 2, 1, 0):
        hm, hh = MUND[k], HALS[k]
        d = (f"M{c - hm} {y_oben} V{y_flach} C{c - hm} {y_flach + 90} {c - hh} {y_kurve - 70} {c - hh} {y_kurve} V{y_hals} "
             f"H{c + hh} V{y_kurve} C{c + hh} {y_kurve - 70} {c + hm} {y_flach + 90} {c + hm} {y_flach} V{y_oben} Z")
        o.append(f'<path d="{d}" class="{LAGEN[k][0]}-h ek2-lage"/>')
    o.append(text(c, y_oben + 36, "sofort", "ek2-kern-t", T_GROSS, 700, "middle"))
    o.append(text(c, y_oben + 58, "sichtbar", "ek2-kern-t", T_GROSS, 700, "middle"))
    for i in range(3):
        o.append(f'<circle cx="{c}" cy="{y_kurve - 30 + i * 15}" r="4" class="ek2-kern-p"/>')
    # Messpunkt
    o.append(f'<path d="M{c + HALS[3]} {y_hals - 14} H{c + HALS[3] + 22}" class="ek2-linie ek2-linie--fein"/>')
    o.append(text(c + HALS[3] + 28, y_hals - 18, "Messpunkt:", "ek2-t", gewicht=700))
    o.append(text(c + HALS[3] + 28, y_hals - 2, "Leads", "ek2-t", gewicht=700))
    # Band (gleich gestaltet, untereinander), davor mit Abstand die Klammer zum Vertrieb
    o.append(text(c, y_hals + 44, TX["vertrieb"], "ek2-t", gewicht=600, anker="middle"))
    y_hals += 42
    x0, x1 = 50, W - 50
    o.append(f'<path d="M{x0} {y_hals + 14} H{x1} V{y_hals + 84} L{c} {y_hals + 100} L{x0} {y_hals + 84} Z" class="ek2-band"/>')
    yk = y_hals + 108
    o.append(f'<path d="M{x0} {yk} L{c} {yk + 16} L{x1} {yk} V{yk + 70} Q{x1} {yk + 86} {x1 - 16} {yk + 86} H{x0 + 16} Q{x0} {yk + 86} {x0} {yk + 70} Z" class="ek2-band"/>')
    for y, titel, unter in ((y_hals + 48, "Vertrieb", TX["vertrieb_unter"]), (yk + 50, "Kundenbetreuung", TX["kunden_unter"])):
        o.append(text(c, y, titel, "ek2-band-t", T_GROSS, 700, "middle"))
        o.append(text(c, y + 21, unter, "ek2-band-s", anker="middle"))
    # Rückweg links hoch zum Trichter
    o.append(f'<path d="M{x0} {yk + 50} H18 V{y_oben + 30} H{c - MUND[3] - 6}" class="ek2-linie ek2-linie--fein" marker-end="url(#ek2-pfeil-hoch)"/>')
    o.append(text(c + 8, yk + 122, "Regelmäßige Präsenz pflegt deinen Bestand –", "ek2-t", anker="middle"))
    o.append(text(c + 8, yk + 139, "und bringt neue Anlässe.", "ek2-t", anker="middle"))
    return svg(W, H, "".join(o), "ek2-svg--hoch", "hoch")


def svg(w, h, inhalt, klasse, name):
    pfeil = (f'<defs><marker id="ek2-pfeil-{name}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
             '<path d="M1 1 L8 5 L1 9" class="ek2-pfeilkopf"/></marker></defs>')
    return f'<svg class="ek2-svg {klasse}" viewBox="0 0 {w} {h}" aria-hidden="true">{pfeil}{inhalt}</svg>'


if __name__ == "__main__":
    p = os.path.join(HERE, "story7.11tydata.json")
    d = json.load(open(p, encoding="utf-8"))
    d["s7"]["ek_quer"] = quer()
    d["s7"]["ek_hoch"] = hoch()
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    print("Erklärbild quer und hochkant geschrieben")
