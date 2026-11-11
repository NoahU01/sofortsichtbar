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
    ("Marketing", "Interessenten gewinnen.", ["Deine Zielgruppen nehmen dich regelmäßig wahr – und daraus", "entstehen echte Anfragen. Jeder weitere Baustein macht den", "Trichter größer und schiebt mehr in deinen Vertrieb."], "Echte Anfragen aus deinen Zielgruppen"),
    ("Vertrieb", "Abschließen.", ["Termin vereinbaren, beraten, abschließen –", "dein Vertrieb, wie du ihn kennst.", "Nur mit mehr Gesprächen."], "Mehr Abschlüsse"),
    ("Kundenbetreuung", "Kunden halten.", ["Wer regelmäßig von dir hört, bleibt –", "und bringt neue Anlässe mit."], "Kunden, die bleiben"),
]

# Bausteine im Trichter: (Nr, Name, Icon) – von innen (Kern) nach außen
BAUSTEINE = [("1", "Kernpaket sofort sichtbar", "layout-dashboard"), ("2", "LinkedIn Power Package", "handshake"),
             ("3", "Paid Ads", "trending-up"), ("4", "Website-Entwicklung", "app-window")]


def marketing_svg():
    o = []
    c = 196                         # Mittellinie
    H = 60                          # Halbhöhe der Prozesspfeile = Halbhöhe des Trichter-Ausgangs mit allen Bausteinen
    mund_x, hals_x, rohr_ende = 34, 372, 452
    # je Baustein: Halbhöhe an der Öffnung und am Ausgang (gestapelt bis H), Füllung
    schicht = [(60, 21, GELB), (94, 34, "#dcd8d2"), (128, 47, "#e8e5e0"), (162, H, "#f3f1ee")]

    def trichter(hm, ha):
        return (f"M{mund_x} {c - hm} C{mund_x + 230} {c - hm} {hals_x - 120} {c - ha} {hals_x} {c - ha} H{rohr_ende} "
                f"V{c + ha} H{hals_x} C{hals_x - 120} {c + ha} {mund_x + 230} {c + hm} {mund_x} {c + hm} Z")
    # Klammern oben
    o.append(t(0, 16, "UNSER SCHWERPUNKT", 10.5, 700, INK, extra=' letter-spacing="1.6"'))
    o.append(f'<rect x="150" y="10" width="302" height="2.5" fill="{INK}"/>')
    o.append(t(474, 16, "DEIN VERTRIEB – WIR DOCKEN AN", 10.5, 700, GRAU, extra=' letter-spacing="1.6"'))
    o.append(f'<rect x="722" y="10" width="478" height="1.5" fill="{LINIE}"/>')
    # Aufmerksamkeit vor der Öffnung
    import random
    rnd = random.Random(7)
    for _ in range(28):
        o.append(f'<circle cx="{rnd.uniform(0, 24):.1f}" cy="{rnd.uniform(c - 150, c + 150):.1f}" r="{rnd.uniform(2.2, 3.6):.1f}" fill="#cfcac3"/>')
    # Schichten von außen nach innen
    for (hm, ha, fill) in reversed(schicht):
        o.append(f'<path d="{trichter(hm, ha)}" fill="{fill}" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>')
    # Beschriftung: Bausteine 2–4 oben in ihrer Schicht, Baustein 1 im Kern
    for (nr, name, icon), (hm, ha, fill), (hm_innen, _, _) in zip(BAUSTEINE[1:], schicht[1:], schicht[:-1]):
        y = c - hm + (hm - hm_innen) / 2 + 4
        o.append(ico(icon, mund_x + 14, y - 12, 15))
        o.append(t(mund_x + 36, y, f"Baustein {nr} · {name}", 11.5, 600))
    nr, name, icon = BAUSTEINE[0]
    o.append(ico(icon, mund_x + 14, c - 24, 17))
    o.append(t(mund_x + 38, c - 11, f"Baustein {nr}", 11.5, 600))
    o.append(t(mund_x + 14, c + 13, "Kernpaket", 17, 700))
    o.append(t(mund_x + 14, c + 32, "sofort sichtbar", 12.5, 400))
    # Leads im Kern-Rohr
    for i, x in enumerate([392, 414, 436]):
        o.append(f'<circle cx="{x}" cy="{c + (i - 1) * 7}" r="4.2" fill="{INK}"/>')
    # Prozesspfeile: Vertrieb (mit drei Schritten) und Kundenbetreuung – gleiche Höhe wie der Trichter-Ausgang
    x0, xm, x1 = rohr_ende, 860, 1200
    o.append(f'<path d="M{x0} {c - H} H{xm - 26} L{xm} {c} L{xm - 26} {c + H} H{x0} Z" fill="#fff" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')
    o.append(f'<path d="M{xm + 6} {c - H} H{x1 - 14} Q{x1} {c - H} {x1} {c - H + 14} V{c + H - 14} Q{x1} {c + H} {x1 - 14} {c + H} '
             f'H{xm + 6} L{xm + 32} {c} Z" fill="{INK}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')
    o.append(ico("handshake", x0 + 30, c - 30, 26))
    o.append(t(x0 + 66, c - 10, "Vertrieb", 18, 700, font=LORA))
    # drei Schritte mit Abstand nach Textbreite, dazwischen ein kleiner Pfeil
    sx = x0 + 66
    for i, (s, breite) in enumerate([("Terminierung", 84), ("Beratung", 58), ("Abschluss", 64)]):
        o.append(t(sx, c + 22, s, 12.5, 500))
        if i < 2:
            px = sx + breite + 12
            o.append(f'<path d="M{px} {c + 13} l5 4.5 l-5 4.5" fill="none" stroke="{GRAU}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
            sx = px + 17
    o.append(ico("heart-handshake", xm + 52, c - 13, 26, GELB))
    o.append(t(xm + 88, c + 6, "Kundenbetreuung", 18, 700, "#fff", font=LORA))
    # Texte je Stufe – gleiche Höhe in allen Spalten
    spalten = [(0, 440), (474, 820), (884, 1200)]
    for (sx0, sx1), (name, claim, zeilen, erg), nr in zip(spalten, STUFEN_TEXT, range(1, 4)):
        y = 418
        o.append(t(sx0, y, f"STUFE {nr} · {name.upper()}", 10.5, 700, INK if nr == 1 else GRAU, extra=' letter-spacing="1.4"'))
        o.append(t(sx0, y + 34, claim, 23, 700, font=LORA))
        for j, z in enumerate(zeilen):
            o.append(t(sx0, y + 62 + j * 19, z, 13, 400, "#3d3a37"))
        o.append(f'<rect x="{sx0}" y="{y + 128}" width="{min(sx1 - sx0, 230)}" height="1.2" fill="{LINIE}"/>')
        o.append(t(sx0, y + 150, erg, 13.5, 700))
    # Rückweg Kundenbetreuung → Marketing
    o.append(f'<path d="M1040 592 V624 H220 V598" fill="none" stroke="{INK}" stroke-width="1.6" marker-end="url(#mb-pfeil)"/>')
    o.append(f'<rect x="390" y="607" width="480" height="34" rx="17" fill="{GELB}"/>')
    o.append(t(630, 629, "Sichtbarkeit pflegt auch deinen Bestand – und bringt neue Anlässe.", 12.5, 600, anchor="middle"))
    defs = (f'<defs><marker id="mb-pfeil" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M1 1 L8 5 L1 9" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 0 1210 652" class="mx-strukturbild" role="img" '
            f'aria-label="Die digitale Maschine: ein Trichter aus vier Bausteinen mündet in deinen Vertrieb und die Kundenbetreuung">'
            + defs + "".join(o) + '</svg>')


# ---------------------------------------------------------------------------
# Hochformat-Variante fürs PDF: dieselbe Logik senkrecht, gezeichnet in Millimetern (1 Einheit = 1 mm),
# damit Beschriftungen auf Papier mindestens 8 pt groß sind. Vier Zeilen: Trichter · Vertrieb · Kundenbetreuung · Rückweg.
HOCH_B = 70                      # Breite der Grafikspalte in mm
HOCH_ZEILEN = [86, 48, 48, 12]   # Höhen der Zeilen in mm


def hoch_teile():
    cx, A = 39.0, 18.0            # Mitte und halbe Breite der Prozesspfeile (= Trichter-Ausgang mit allen Bausteinen)
    W = HOCH_B
    pt = 0.3528                   # 1 pt in mm
    teile = []

    def svgw(h, inhalt):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}mm" height="{h}mm" style="display:block">'
                f'<defs><marker id="hp" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
                f'<path d="M1 1 L8 5 L1 9" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
                f'{inhalt}</svg>')

    linie = f'stroke="{INK}" stroke-width="0.45" fill="none"'
    # Zeile 1: Trichter von oben nach unten
    h1 = HOCH_ZEILEN[0]
    schicht = [(14, 6, GELB), (20.5, 10, "#dcd8d2"), (27, 14, "#e8e5e0"), (33.5, A, "#f3f1ee")]   # (halbe Breite oben, unten)
    y0, yk, y1 = 8, 62, h1

    def kegel(hm, ha):
        return (f"M{cx - hm} {y0} C{cx - hm} {y0 + 14} {cx - ha} {yk - 26} {cx - ha} {yk} V{y1} H{cx + ha} V{yk} "
                f"C{cx + ha} {yk - 26} {cx + hm} {y0 + 14} {cx + hm} {y0} Z")
    o = []
    import random
    rnd = random.Random(3)
    for _ in range(22):
        o.append(f'<circle cx="{rnd.uniform(cx - 32, cx + 32):.1f}" cy="{rnd.uniform(1, 5.5):.1f}" r="{rnd.uniform(.5, .85):.2f}" fill="#cfcac3"/>')
    for hm, ha, f in reversed(schicht):
        o.append(f'<path d="{kegel(hm, ha)}" fill="{f}" stroke="#fff" stroke-width="0.7" stroke-linejoin="round"/>')
    # Nummern der Bausteine in ihren Schichten (links), Kern mittig
    for nr, x in (("4", cx - 30.25), ("3", cx - 23.75), ("2", cx - 17.25)):
        o.append(f'<circle cx="{x}" cy="{y0 + 6}" r="2.3" fill="#fff" stroke="{INK}" stroke-width="0.35"/>')
        o.append(t(x, y0 + 7.05, nr, 8.5 * pt, 700, anchor="middle"))
    o.append(f'<circle cx="{cx}" cy="{y0 + 6}" r="2.3" fill="{INK}"/>')
    o.append(t(cx, y0 + 7.05, "1", 8.5 * pt, 700, GELB, "middle"))
    o.append(t(cx, y0 + 16, "Kernpaket", 9.5 * pt, 700, anchor="middle"))
    for i, y in enumerate([72, 77.5, 83]):
        o.append(f'<circle cx="{cx + (i - 1) * 1.6}" cy="{y}" r="1.1" fill="{INK}"/>')
    # Rückweg: linke Kante nach oben, oben in die Öffnung
    o.append(f'<path d="M1 {h1} V3 H{cx - 35}" {linie} marker-end="url(#hp)"/>')
    teile.append(svgw(h1, "".join(o)))

    # Zeile 2: Vertrieb (Pfeil nach unten, weiß)
    h2 = HOCH_ZEILEN[1]
    o = [f'<path d="M{cx - A} 0 H{cx + A} V{h2 - 9} L{cx} {h2} L{cx - A} {h2 - 9} Z" fill="#fff" stroke="{INK}" stroke-width="0.6" stroke-linejoin="round"/>']
    o.append(ico("handshake", cx - 3.6, 4.5, 7.2))
    o.append(t(cx, 18, "Vertrieb", 12 * pt, 700, anchor="middle", font=LORA))
    for i, s in enumerate(["Terminierung", "Beratung", "Abschluss"]):
        o.append(t(cx, 24.5 + i * 4.6, s, 8.5 * pt, 500, anchor="middle"))
    o.append(f'<path d="M1 0 V{h2}" {linie}/>')
    teile.append(svgw(h2, "".join(o)))

    # Zeile 3: Kundenbetreuung (schwarz, oben eingekerbt)
    h3 = HOCH_ZEILEN[2]
    o = [f'<path d="M{cx - A} 1.5 L{cx} 10 L{cx + A} 1.5 V{h3 - 3} Q{cx + A} {h3} {cx + A - 3} {h3} H{cx - A + 3} Q{cx - A} {h3} {cx - A} {h3 - 3} Z" '
         f'fill="{INK}" stroke="{INK}" stroke-width="0.6" stroke-linejoin="round"/>']
    o.append(ico("heart-handshake", cx - 3.6, 13, 7.2, GELB))
    o.append(t(cx, 27, "Kunden-", 11 * pt, 700, "#fff", "middle", font=LORA))
    o.append(t(cx, 31.6, "betreuung", 11 * pt, 700, "#fff", "middle", font=LORA))
    o.append(f'<path d="M1 0 V{h3}" {linie}/>')
    teile.append(svgw(h3, "".join(o)))

    # Zeile 4: Rückweg unten herum
    h4 = HOCH_ZEILEN[3]
    o = [f'<path d="M{cx} 0 V6 H1 V0" {linie}/>']
    teile.append(svgw(h4, "".join(o)))
    return teile
