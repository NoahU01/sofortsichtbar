"""Strukturbild „Die digitale Maschine vor deinem Vertrieb“ – ein SVG für Seite, PDF und Download.

Prozessual von links nach rechts (kein Kreis): Stufe 1 Marketing (gelb = unser Schwerpunkt) → Lead →
Stufe 2 Qualifizierung mit zwei Entscheidungen (Passt es? / Abschlussbereit?) inkl. Ende und Warmhalten →
Stufe 3 Vertriebsstrang → Stufe 4 Kundenbetreuung; Rückweg als Linie unten von Stufe 4 zu Stufe 1.
Farben: Tinte, Grau, Gelb nur als Fläche/Marker. Schriften: Lora (Titel), Poppins (Text).
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/Projekte/empiria/werkzeuge"))
from e2_lucide import ICONS  # noqa: E402

INK, GRAU, LINIE, HELL, GELB = "#1a1817", "#6f6a64", "#cfcac3", "#f4f3f0", "#fff400"
LORA = "font-family=\"Lora, Georgia, serif\""
POP = "font-family=\"Poppins, Arial, sans-serif\""


def t(x, y, s, size=13, w=400, fill=INK, anchor="start", font=POP, extra=""):
    return f'<text x="{x}" y="{y}" {font} font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}"{extra}>{s}</text>'


def ico(name, x, y, size=18, farbe=INK):
    s = size / 24
    return (f'<g transform="translate({x} {y}) scale({s:.4f})" fill="none" stroke="{farbe}" stroke-width="{1.6 / s * s:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def pfeil(d, gestrichelt=False, farbe=INK):
    dash = ' stroke-dasharray="6 5"' if gestrichelt else ""
    return f'<path d="{d}" fill="none" stroke="{farbe}" stroke-width="2"{dash} marker-end="url(#sb-pfeil)"/>'


def haken(x, y):
    return f'<path d="M{x} {y} l3.5 3.5 l7 -7" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'


def raute(cx, cy, z1, z2=""):
    h = 46
    pts = f"{cx},{cy - h} {cx + h},{cy} {cx},{cy + h} {cx - h},{cy}"
    txt = (t(cx, cy - 2 if z2 else cy + 4, z1, 11.5, 600, anchor="middle")
           + (t(cx, cy + 13, z2, 11.5, 600, anchor="middle") if z2 else ""))
    return f'<polygon points="{pts}" fill="#fff" stroke="{INK}" stroke-width="2"/>' + txt


def svg():
    o = []
    # Spalten der Stufen: (x0, x1, nr, titel, schwerpunkt)
    sp = [(0, 250, "1", "Marketing", True), (272, 818, "2", "Qualifizierung", False),
          (840, 1000, "3", "Vertrieb", False), (1022, 1210, "4", "Kundenbetreuung", False)]
    for x0, x1, nr, titel, wir in sp:
        o.append(t(x0, 26, f"STUFE {nr}" + (" · UNSER SCHWERPUNKT" if wir else ""), 10.5, 700, INK if wir else GRAU, extra=' letter-spacing="1.6"'))
        o.append(t(x0, 58, titel, 22, 700, font=LORA))
        o.append(f'<rect x="{x0}" y="72" width="{x1 - x0}" height="{4 if wir else 2}" fill="{INK if wir else LINIE}"/>')

    # Stufe 1: regelmäßige Wahrnehmung (gelb)
    o.append(f'<rect x="0" y="104" width="250" height="250" rx="18" fill="{GELB}"/>')
    o.append(t(22, 138, "Regelmäßig", 15, 600))
    o.append(t(22, 158, "wahrgenommen werden", 15, 600))
    for i, k in enumerate(["Postings und Social Media", "LinkedIn", "Landingpages", "Mailings", "Paid Ads", "Post (ergänzend)"]):
        y = 196 + i * 25
        o.append(haken(24, y - 6))
        o.append(t(44, y, k, 13, 400))
    o.append(pfeil("M250 229 H284"))

    # Lead
    o.append(f'<rect x="288" y="210" width="74" height="38" rx="19" fill="{INK}"/>')
    o.append(t(325, 234, "Lead", 14, 700, GELB, "middle"))
    o.append(t(325, 268, "Interessent aus", 10.5, 400, GRAU, "middle"))
    o.append(t(325, 282, "deiner Zielgruppe", 10.5, 400, GRAU, "middle"))
    o.append(pfeil("M362 229 H386"))

    # Kontakt aufnehmen
    o.append(f'<rect x="390" y="168" width="150" height="122" rx="14" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    o.append(t(406, 196, "Erstkontakt", 13.5, 600))
    o.append(ico("calendar", 406, 212, 16))
    o.append(t(429, 225, "Terminierungs-", 12, 400))
    o.append(t(429, 240, "tool", 12, 400))
    o.append(t(406, 262, "oder", 11, 400, GRAU))
    o.append(ico("phone", 406, 266, 16))
    o.append(t(429, 279, "aktiv nachfassen", 12, 400))
    o.append(pfeil("M540 229 H560"))

    # Entscheidung 1: Passt es?
    o.append(raute(608, 229, "Passt es?"))
    o.append(pfeil("M608 275 V322"))
    o.append(t(616, 300, "nein", 11, 600, GRAU))
    o.append(f'<rect x="556" y="326" width="104" height="34" rx="17" fill="{HELL}" stroke="{LINIE}" stroke-width="1.5"/>')
    o.append(t(608, 348, "Ende", 12.5, 600, GRAU, "middle"))
    o.append(pfeil("M654 229 H670"))
    o.append(t(656, 220, "ja", 11, 600, GRAU))

    # Entscheidung 2: Abschlussbereit?
    o.append(raute(718, 229, "Abschluss-", "bereit?"))
    o.append(pfeil("M764 229 H836"))
    o.append(t(774, 220, "ja", 11, 600, GRAU))
    o.append(pfeil("M718 275 V346"))
    o.append(t(726, 316, "noch nicht", 11, 600, GRAU))

    # Warmhalten
    o.append(f'<rect x="652" y="350" width="166" height="132" rx="14" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<rect x="652" y="350" width="166" height="34" rx="14" fill="{INK}"/><rect x="652" y="368" width="166" height="16" fill="{INK}"/>')
    o.append(t(668, 373, "Warmhalten", 13.5, 600, GELB))
    for i, k in enumerate(["Erinnerungs-Mailings", "Webinar, Tag der", "offenen Tür", "Weihnachtspost"]):
        y = 406 + i * 19
        if i != 2:
            o.append(haken(668, y - 5))
        o.append(t(686, y, k, 12, 400))
    o.append(pfeil("M818 416 H905 V352", gestrichelt=True))
    o.append(t(830, 436, "sobald bereit", 11, 600, GRAU))

    # Stufe 3: Vertriebsstrang
    o.append(f'<rect x="840" y="118" width="160" height="232" rx="14" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    o.append(t(856, 146, "Vertriebsstrang", 13.5, 600))
    for i, k in enumerate([("Analysetermin",), ("Absicherungs-", "konzept"), ("Beratung und", "Abschluss")]):
        y = 186 + i * 54
        o.append(f'<circle cx="868" cy="{y}" r="12" fill="#fff" stroke="{INK}" stroke-width="1.8"/>')
        o.append(t(868, y + 4.5, str(i + 1), 11.5, 600, anchor="middle"))
        o.append(t(888, y + (4.5 if len(k) == 1 else -3), k[0], 12.5, 400))
        if len(k) > 1:
            o.append(t(888, y + 12, k[1], 12.5, 400))
        if i < 2:
            o.append(f'<path d="M868 {y + 14} V{y + 38}" stroke="{LINIE}" stroke-width="1.6"/>')
    o.append(pfeil("M1000 229 H1018"))

    # Stufe 4: Kundenbetreuung
    o.append(f'<rect x="1022" y="168" width="184" height="122" rx="14" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    o.append(t(1040, 196, "Laufende Betreuung", 13.5, 600))
    for i, k in enumerate(["Bestandskunden", "betreuen", "Neue Anlässe", "erkennen"]):
        o.append(t(1040, 224 + i * 16 + (6 if i > 1 else 0), k, 12, 400))

    # Rückweg von Stufe 4 zu Stufe 1 (prozessual, kein Kreis)
    o.append(pfeil("M1114 290 V524 H125 V358"))
    o.append(f'<rect x="372" y="506" width="456" height="36" rx="18" fill="{GELB}"/>')
    o.append(t(600, 529, "Wahrnehmung wirkt auch im Bestand: neue Anlässe für Stufe 1", 12.5, 600, anchor="middle"))

    defs = (f'<defs><marker id="sb-pfeil" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M1 1 L8 5 L1 9" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 0 1218 556" class="mx-strukturbild" role="img" '
            f'aria-label="Strukturbild: vier Stufen von Marketing über Qualifizierung und Vertrieb bis Kundenbetreuung, mit Rückweg in Stufe 1">'
            + defs + "".join(o) + '</svg>')


if __name__ == "__main__":
    print(svg())


# ---------------------------------------------------------------------------
# Marketing-Grafik (erste Ebene der Seite): liegender Trichter aus geschachtelten Schichten (Kern = Kernpaket,
# außen die Ergänzungen) mündet in die Vertriebs-Pipeline (Qualifizierung · Vertrieb · Kundenbetreuung).
# Darunter je Stufe: Anspruch · was passiert · was du davon hast. Rückweg von Stufe 4 zu Stufe 1 als ruhige Linie.
# Das technische Bild (svg()) bleibt als Arbeitsgrundlage erhalten.

STUFEN_TEXT = [
    ("Marketing", "Gesehen werden.", ["Deine Zielgruppen nehmen dich regelmäßig wahr –", "auf den Kanälen, die sie nutzen. Jede Ergänzung", "macht den Trichter größer."], "Echte Anfragen aus deinen Zielgruppen"),
    ("Qualifizierung", "Die Richtigen finden.", ["Wer passt, bekommt einen Termin.", "Wer noch nicht so weit ist,", "bleibt warm, bis er es ist."], "Termine, die sich lohnen"),
    ("Vertrieb", "Abschließen.", ["Analyse, Konzept, Beratung –", "dein Vertrieb, wie du ihn kennst.", "Nur mit mehr Gesprächen."], "Mehr Abschlüsse"),
    ("Kundenbetreuung", "Kunden halten.", ["Wer regelmäßig von dir hört,", "bleibt – und bringt neue", "Anlässe mit."], "Kunden, die bleiben"),
]


def marketing_svg():
    o = []
    c = 196                      # Mittellinie von Trichter und Pipeline
    hals_x, hals_ende, n = 372, 474, 30   # Kegel endet bei hals_x, danach das Rohr bis hals_ende (Halbhöhe n)
    mund_x = 34
    # Kegel von außen nach innen: (Halbhöhe an der Öffnung, Füllung, Beschriftung)
    schichten = [(158, "#f3f1ee", "Paid Ads"), (124, "#e8e5e0", "Website"), (92, "#dcd8d2", "LinkedIn"), (60, GELB, "")]

    def trichter(h):
        return (f"M{mund_x} {c - h} L{hals_x} {c - n} Q{hals_x + 14} {c - n} {hals_x + 28} {c - n} H{hals_ende} "
                f"V{c + n} H{hals_x + 28} Q{hals_x + 14} {c + n} {hals_x} {c + n} L{mund_x} {c + h} Z")
    # Klammern oben
    o.append(t(0, 16, "UNSER SCHWERPUNKT", 10.5, 700, INK, extra=' letter-spacing="1.6"'))
    o.append(f'<rect x="150" y="10" width="300" height="2.5" fill="{INK}"/>')
    o.append(t(494, 16, "DEIN VERTRIEB – WIR DOCKEN AN", 10.5, 700, GRAU, extra=' letter-spacing="1.6"'))
    o.append(f'<rect x="742" y="10" width="458" height="1.5" fill="{LINIE}"/>')
    # Aufmerksamkeit: Punkte vor der Öffnung
    import random
    rnd = random.Random(7)
    for _ in range(26):
        x = rnd.uniform(0, 26); y = rnd.uniform(c - 140, c + 140)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(2.2, 3.6):.1f}" fill="#cfcac3"/>')
    # Schichten
    for h, fill, label in schichten:
        o.append(f'<path d="{trichter(h)}" fill="{fill}" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>')
    for h, fill, label in schichten[:-1]:
        o.append(t(mund_x + 14, c - h + 22, "+ " + label, 12, 600, INK))
    o.append(t(mund_x + 18, c - 5, "Kernpaket", 16, 700))
    o.append(t(mund_x + 18, c + 15, "sofort sichtbar", 12.5, 400))
    # Pipeline: drei Pfeilsegmente
    neck_h = n + 12
    seg = [(hals_ende + 18, 742, "filter", "Qualifizierung"), (742, 970, "handshake", "Vertrieb"), (970, 1200, "heart-handshake", "Kundenbetreuung")]
    for i, (x0, x1, icon, name) in enumerate(seg):
        spitze = 0 if i == 2 else 22
        einkerb = 0 if i == 0 else 22
        d = (f"M{x0} {c - neck_h - 14} H{x1 - spitze} L{x1} {c} L{x1 - spitze} {c + neck_h + 14} H{x0} "
             f"L{x0 + einkerb} {c} Z") if i < 2 else (f"M{x0} {c - neck_h - 14} H{x1 - 14} Q{x1} {c - neck_h - 14} {x1} {c - neck_h} "
                                                       f"V{c + neck_h} Q{x1} {c + neck_h + 14} {x1 - 14} {c + neck_h + 14} H{x0} L{x0 + einkerb} {c} Z")
        o.append(f'<path d="{d}" fill="{INK if i == 2 else "#fff"}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')
        tx = x0 + (34 if i else 22)
        o.append(ico(icon, tx, c - 13, 26, GELB if i == 2 else INK))
        o.append(t(tx + 36, c + 6, name, 16, 700, "#fff" if i == 2 else INK, font=LORA))
    # Leads im Hals
    for i, x in enumerate([404, 428, 452]):
        o.append(f'<circle cx="{x}" cy="{c + (i - 1) * 9}" r="4.5" fill="{INK}"/>')
    # Texte je Stufe – gleiche Höhe in allen Spalten
    spalten = [(0, 440), (494, 720), (764, 950), (994, 1200)]
    for (x0, x1), (name, claim, zeilen, erg), nr in zip(spalten, STUFEN_TEXT, range(1, 5)):
        y = 418
        o.append(t(x0, y, f"STUFE {nr} · {name.upper()}", 10.5, 700, INK if nr == 1 else GRAU, extra=' letter-spacing="1.4"'))
        o.append(t(x0, y + 34, claim, 23, 700, font=LORA))
        for j, z in enumerate(zeilen):
            o.append(t(x0, y + 62 + j * 19, z, 13, 400, "#3d3a37"))
        o.append(f'<rect x="{x0}" y="{y + 128}" width="{min(x1 - x0, 210)}" height="1.2" fill="{LINIE}"/>')
        o.append(t(x0, y + 150, erg, 13.5, 700))
    # Rückweg 4 → 1
    o.append(f'<path d="M1097 592 V624 H220 V598" fill="none" stroke="{INK}" stroke-width="1.6" marker-end="url(#mb-pfeil)"/>')
    o.append(f'<rect x="420" y="607" width="480" height="34" rx="17" fill="{GELB}"/>')
    o.append(t(660, 629, "Sichtbarkeit pflegt auch deinen Bestand – und bringt neue Anlässe.", 12.5, 600, anchor="middle"))
    defs = (f'<defs><marker id="mb-pfeil" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M1 1 L8 5 L1 9" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 0 1210 652" class="mx-strukturbild" role="img" '
            f'aria-label="Die digitale Maschine: ein Trichter aus Kernpaket und Ergänzungen mündet in deinen Vertrieb – Qualifizierung, Vertrieb, Kundenbetreuung">'
            + defs + "".join(o) + '</svg>')
