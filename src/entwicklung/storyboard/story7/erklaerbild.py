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
MUND_H = [62, 84, 104, 122]  # Hochformat: breiterer Kern, damit das Logo am Handy lesbar bleibt


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


def logo(x, y, breite, praefix):
    """Einzeiliges sofort-sichtbar-Logo (story6/assets/img/sofort-sichtbar-logo-ink.svg), eingefärbt über die Klasse ek2-kern-t.
    Die Kennungen der Beschneidungspfade bekommen ein Präfix, damit Quer- und Hochfassung sich nicht in die Quere kommen."""
    import re
    quelle = open(os.path.join(HERE, "..", "story6", "assets", "img", "sofort-sichtbar-logo-ink.svg"), encoding="utf-8").read()
    innen = quelle[quelle.index(">", quelle.index("<svg")) + 1:quelle.rindex("</svg>")]
    innen = innen.replace('fill="#1a1817"', 'class="ek2-kern-t"')
    innen = re.sub(r'(id="|url\(#)clip-', lambda m: m.group(1) + praefix + "-clip-", innen)
    hoehe = breite * 23.6175 / 199.308
    return (f'<svg x="{x}" y="{y - hoehe / 2:.1f}" width="{breite}" height="{hoehe:.1f}" viewBox="0 0 199.308 23.6175" '
            f'aria-label="sofort sichtbar">{innen}</svg>')


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
    o.append(logo(28, c, 150, "ek2q"))
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
        hm, hh = MUND_H[k], HALS[k]
        d = (f"M{c - hm} {y_oben} V{y_flach} C{c - hm} {y_flach + 90} {c - hh} {y_kurve - 70} {c - hh} {y_kurve} V{y_hals} "
             f"H{c + hh} V{y_kurve} C{c + hh} {y_kurve - 70} {c + hm} {y_flach + 90} {c + hm} {y_flach} V{y_oben} Z")
        o.append(f'<path d="{d}" class="{LAGEN[k][0]}-h ek2-lage"/>')
    o.append(logo(c - 48, y_oben + 34, 96, "ek2h"))
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
    o.append(f'<path d="M{x0} {yk + 50} H18 V{y_oben + 30} H{c - MUND_H[3] - 6}" class="ek2-linie ek2-linie--fein" marker-end="url(#ek2-pfeil-hoch)"/>')
    o.append(text(c + 8, yk + 122, "Regelmäßige Präsenz pflegt deinen Bestand –", "ek2-t", anker="middle"))
    o.append(text(c + 8, yk + 139, "und bringt neue Anlässe.", "ek2-t", anker="middle"))
    return svg(W, H, "".join(o), "ek2-svg--hoch", "hoch")


def svg(w, h, inhalt, klasse, name):
    pfeil = (f'<defs><marker id="ek2-pfeil-{name}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
             '<path d="M1 1 L8 5 L1 9" class="ek2-pfeilkopf"/></marker></defs>')
    return f'<svg class="ek2-svg {klasse}" viewBox="0 0 {w} {h}" aria-hidden="true">{pfeil}{inhalt}</svg>'


# ---------------------------------------------------------------------------------------------
# Herangezoomter Trichter für die Unterseite Marketing as a Service (Daniel, 12.11.2026):
# Zielgruppen hinein → Trichter mit benannten Lagen → Leads → dein Vertrieb (Seite muss allein verständlich sein).
# Preise stehen bei den Bausteinen, nicht in der Grafik (keine Doppelung).
# Die ausführliche Fassung mit Strategie und Steuerung ist verworfen („nimmt der Grafik die Genialität“).
# ---------------------------------------------------------------------------------------------


# Schnitt durch die Maschine (Daniel, 12.11.2026: „erklärt nicht, was passiert“):
# der Trichter flach und breit wie auf der Startseite, aber aufgeschnitten – jede Lage ist eine Zeile mit dem,
# was darin passiert. Ganzer Trichter: obere Hälfte dick zum Beschriften, untere dünn (Daniel, 12.11.2026). Eine Quelle für Grafik (quer) und Liste (Handy).
SCHNITT = [  # innen → außen
    {"klasse": "ek2-kern", "name": "Kernpaket", "marke": "Die Basis",
     "text": ["Fünf Landingpages, laufende Postings je Zielgruppe,", "Dashboard, monatlicher Report und Betreuungscall"]},
    {"klasse": "ek2-l2", "name": "LinkedIn Power Package", "marke": "dazu buchbar",
     "text": ["Mit Netzwerkaufbau und Direktansprache zum aktiven Vertriebskanal"]},
    {"klasse": "ek2-l3", "name": "Paid Ads", "marke": "dazu buchbar",
     "text": ["Kampagnen auf Google, Meta oder LinkedIn – laufend gesteuert"]},
    {"klasse": "ek2-l4", "name": "Website-Entwicklung", "marke": "dazu buchbar",
     "text": ["Deine Versicherungsagentur sauber positioniert"]},
]


def schnitt_quer():
    """Ganzer Trichter: obere Hälfte dick (dort steht, was in jeder Lage passiert), untere Hälfte dünn."""
    W = 1120
    hoch = [90, 154, 218, 282]               # Abstand der Oberkante von der Mitte, innen → außen
    tief = [34, 74, 114, 154]                # Abstand der Unterkante von der Mitte: gut halb so dick wie oben, damit die Form als Trichter liest
    hals = [14, 20, 26, 32]                  # halbe Höhe an der Mündung
    c = hoch[3]
    x_flach, x_kurve, x_hals = 610, 880, 910
    o = []
    for k in (3, 2, 1, 0):
        yo, yu, h = c - hoch[k], c + tief[k], hals[k]
        d = (f"M0 {yo} H{x_flach} C{x_flach + 150} {yo} {x_kurve - 130} {c - h} {x_kurve} {c - h} H{x_hals} "
             f"V{c + h} H{x_kurve} C{x_kurve - 130} {c + h} {x_flach + 150} {yu} {x_flach} {yu} H0 Z")
        o.append(f'<path d="{d}" class="{SCHNITT[k]["klasse"]} ek2-lage"/>')
    for k, z in enumerate(SCHNITT):
        yo = c - hoch[k]
        kern = k == 0
        kt = "ek2-kern-t" if kern else "ek2-t"
        # Etikett direkt hinter dem Namen – keine zweite Spalte, in die die Sätze hineinlaufen
        o.append(f'<text x="28" y="{yo + (34 if kern else 27)}" class="{kt}" font-size="{20 if kern else 17}" font-weight="700">{z["name"]}'
                 f'<tspan class="{kt if kern else "ek2-grau"}" font-size="13" font-weight="600" dx="12">{z["marke"]}</tspan></text>')
        for n, zeile in enumerate(z["text"]):
            o.append(text(28, yo + (59 if kern else 50) + n * 21, zeile, kt, 15, 500))
    for i in range(3):
        o.append(f'<circle cx="{x_kurve - 40 + i * 16}" cy="{c}" r="3.5" class="ek2-kern-p"/>')
    xm = x_hals + LUECKE / 2
    y0, y1 = c - hals[3], c + hals[3]
    o.append(f'<path d="M{xm} {y0} V{y0 - 34}" class="ek2-linie ek2-linie--fein"/>')
    o.append(text(xm, y0 - 42, TX["messpunkt"], "ek2-t", 15, 700, "middle"))
    xv = x_hals + LUECKE
    o.append(f'<path d="M{xv} {y0} H{W - 16} Q{W} {y0} {W} {y0 + 16} V{y1 - 16} Q{W} {y1} {W - 16} {y1} H{xv} Z" class="ek2-band"/>')
    o.append(text(xv + 22, c - 3, "Dein Vertrieb", "ek2-band-t", 18, 700))
    o.append(text(xv + 22, c + 18, "macht daraus Kunden", "ek2-band-s", 14))
    return svg(W, c + tief[3] + 2, "".join(o), "ek2-svg--quer", "schnitt")

# ---------------------------------------------------------------------------------------------
# Regionsgrafik für die Seite „Für Vertriebsleiter“ (Daniel, 12.11.2026, statt Stockfoto):
# jedes Büro der Region hat seine eigene Maschine (kleiner Trichter wie auf der Startseite),
# die Leads aller Büros ergeben den Umsatz der Region; davor das Strategie-Sparring mit dir,
# zurück die monatliche Rückmeldung: was läuft, was nicht, was wir anpassen.
# ---------------------------------------------------------------------------------------------
def kasten(x, y, b, h, titel, unter, K, G, anker="start"):
    """Umrandeter Kasten (Titel + Zeile darunter) – gleiche Form für alles, was neben der Maschine steht."""
    o = [f'<rect x="{x}" y="{y}" width="{b}" height="{h}" rx="16" class="ek2-kasten"/>']
    tx = x + 24 if anker == "start" else x + b / 2
    o.append(text(tx, y + h / 2 - 3, titel, "ek2-t", G, 700, anker))
    o.append(text(tx, y + h / 2 + 21, unter, "ek2-grau", K, 500, anker))
    return "".join(o)


MINI_MUND = [14, 22, 30, 38]
MINI_HALS = [6, 9, 12, 15]


def mini_trichter(x, c, b=380):
    """Trichter der Startseite im Kleinen – gleiche Lagen, gleiche Farben."""
    xf, xk, xh = x + b * .38, x + b * .86, x + b
    o = []
    for k in (3, 2, 1, 0):
        hm, hh = MINI_MUND[k], MINI_HALS[k]
        o.append(f'<path d="M{x} {c - hm} H{xf:.0f} C{xf + 70:.0f} {c - hm} {xk - 50:.0f} {c - hh} {xk:.0f} {c - hh} H{xh:.0f} V{c + hh} '
                 f'H{xk:.0f} C{xk - 50:.0f} {c + hh} {xf + 70:.0f} {c + hm} {xf:.0f} {c + hm} H{x} Z" class="{LAGEN[k][0]} ek2-lage"/>')
    return "".join(o)


# Regionsgrafik „Für Vertriebsleiter“ (überarbeitet 12.11.2026): nur die Formen des Erklärbilds –
# Klammer mit Linie, Trichter aus Lagen, dunkles Band, dünne Rücklauflinie mit Text. Keine Kästen, keine Pillen.
RG = {"klammer_links": "Jede Agentur – fertige Vertriebsstrecken für ihre Zielgruppen",
      "klammer_rechts": "Deine Region",
      "agenturen": ["Agentur 1", "Agentur 2", "Agentur 3"], "weitere": "… und alle weiteren Agenturen deiner Region",
      "band": ("Mehr Neugeschäft", "in deiner Region"), "messpunkt": "Leads je Agentur",
      "zurueck": "Jeden Monat im Dashboard und im Sparring: welche Agentur wo steht – und was wir anpassen"}


def region_quer():
    W, H = 1120, 470
    ys = [96, 196, 296]
    xl, xt, b = 0, 130, 420                     # Beschriftung, Beginn der Trichter, Länge
    xm = xt + b                                  # Mündungen
    xv = xm + 90                                 # Band
    o = []
    o.append(text(xt, 20, RG["klammer_links"], "ek2-t", 15, 600))
    o.append(f'<path d="M{xt} 34 H{xm}" class="ek2-linie"/>')
    o.append(text(xv, 20, RG["klammer_rechts"], "ek2-t", 15, 600))
    o.append(f'<path d="M{xv} 34 H{W}" class="ek2-linie"/>')
    for y, name in zip(ys, RG["agenturen"]):
        o.append(text(xl, y + 5, name, "ek2-t", 15, 700))
        o.append(mini_trichter(xt, y, b))
        o.append(f'<path d="M{xm} {y} C{xm + 50} {y} {xv - 50} 196 {xv} 196" class="ek2-linie ek2-linie--fein"/>')
    o.append(text(xt, ys[-1] + 66, RG["weitere"], "ek2-grau", 14, 500))
    # Band: wie Vertrieb im Erklärbild, so hoch wie die drei Agenturen zusammen
    y0, y1 = 196 - 52, 196 + 52
    o.append(f'<path d="M{xv} {y0} H{W - 16} Q{W} {y0} {W} {y0 + 16} V{y1 - 16} Q{W} {y1} {W - 16} {y1} H{xv} Z" class="ek2-band"/>')
    o.append(text(xv + 30, 192, RG["band"][0], "ek2-band-t", 24, 700))
    o.append(text(xv + 30, 220, RG["band"][1], "ek2-band-s", 16))
    # Rücklauf: vom Band zurück zu den Agenturen
    yr = H - 22
    o.append(f'<path d="M{(xv + W) / 2} {y1} V{yr} H60 V{ys[-1] + 20}" class="ek2-linie ek2-linie--fein" marker-end="url(#ek2-pfeil-rquer)"/>')
    o.append(f'<rect x="{W / 2 - 330}" y="{yr - 13}" width="660" height="26" class="ek2-grund"/>')
    o.append(text(W / 2, yr + 5, RG["zurueck"], "ek2-t", 14, 600, "middle"))
    return svg(W, H, "".join(o), "ek2-svg--quer", "rquer")


def region_hoch():
    W, c = 340, 170
    o = []
    o.append(text(c, 16, "Jede Agentur – fertige", "ek2-t", 13, 600, "middle"))
    o.append(text(c, 33, "Vertriebsstrecken für ihre Zielgruppen", "ek2-t", 13, 600, "middle"))
    y = 80
    for name in RG["agenturen"]:
        o.append(text(0, y + 5, name, "ek2-t", 13, 700))
        o.append(mini_trichter(90, y, 230))
        y += 92
    o.append(text(90, y - 30, "… und alle weiteren", "ek2-grau", 12, 500))
    o.append(f'<path d="M{c} {y - 10} V{y + 16}" class="ek2-linie" marker-end="url(#ek2-pfeil-rhoch)"/>')
    yb = y + 28
    o.append(f'<rect x="30" y="{yb}" width="{W - 60}" height="96" rx="16" class="ek2-band"/>')
    o.append(text(c, yb + 44, RG["band"][0], "ek2-band-t", 20, 700, "middle"))
    o.append(text(c, yb + 68, RG["band"][1], "ek2-band-s", 14, 500, "middle"))
    o.append(text(c, yb + 130, "Jeden Monat im Dashboard und im Sparring:", "ek2-t", 13, 600, "middle"))
    o.append(text(c, yb + 148, "welche Agentur wo steht – und was wir anpassen", "ek2-t", 13, 500, "middle"))
    return svg(W, yb + 158, "".join(o), "ek2-svg--hoch", "rhoch")

def kopf_trichter():
    """Kleiner Trichter für den Kopf von Marketing as a Service (Spalte „Wir setzen um“): Form wie auf der Startseite, Kern mit Logo."""
    W, H, c = 360, 250, 125
    x_flach, x_kurve, x_hals = 100, 270, 330
    o = []
    for k in (3, 2, 1, 0):
        hm, hh = MUND[k], HALS[k]
        d = (f"M0 {c - hm} H{x_flach} C{x_flach + 90} {c - hm} {x_kurve - 70} {c - hh} {x_kurve} {c - hh} H{x_hals} "
             f"V{c + hh} H{x_kurve} C{x_kurve - 70} {c + hh} {x_flach + 90} {c + hm} {x_flach} {c + hm} H0 Z")
        o.append(f'<path d="{d}" class="{LAGEN[k][0]} ek2-lage"/>')
    o.append(logo(16, c, 130, "ek2kt"))
    for i in range(3):
        o.append(f'<circle cx="{x_kurve - 22 + i * 12}" cy="{c}" r="3.5" class="ek2-kern-p"/>')
    o.append(f'<path d="M{x_hals + 6} {c} H{W - 6}" class="ek2-linie" marker-end="url(#ek2-pfeil-kt)"/>')
    return svg(W, H, "".join(o), "ek2-svg--kt", "kt")

if __name__ == "__main__":
    p = os.path.join(HERE, "story7.11tydata.json")
    d = json.load(open(p, encoding="utf-8"))
    d["s7"]["ek_quer"] = quer()
    d["s7"]["ek_hoch"] = hoch()
    d["s7"]["ek_schnitt_quer"] = schnitt_quer()
    d["s7"]["ek_kopf_trichter"] = kopf_trichter()
    d["s7"]["ek_region_quer"] = region_quer()
    d["s7"]["ek_region_hoch"] = region_hoch()
    d["s7"]["maas"]["schnitt"] = [{"name": z["name"], "marke": z["marke"], "text": " ".join(z["text"]).replace(", Dashboard", ", Dashboard")} for z in SCHNITT]
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    print("Erklärbild quer und hochkant geschrieben")
