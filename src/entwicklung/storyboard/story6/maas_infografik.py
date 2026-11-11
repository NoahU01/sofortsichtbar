"""Infografik „Marketing as a Service“ – drei Entwürfe, gezeichnet in Millimetern (1 Einheit = 1 mm).

A  Querformat DIN A3 (420 × 297): Strategie oben · Maschine waagerecht mit Messpunkten · Stufentexte · Monatsrhythmus unten
B  Hochformat DIN A3 (297 × 420) und Roll-up 100 × 200 cm (gleiche Komposition, Seitenverhältnis 1 : 2)
B2 Hochformat DIN A3 mit drei Sektionen (Strategie · Marketing und Vertrieb · Steuerung), verdichtet aus Roll-up V2

Inhalte wie auf der Seite Marketing as a Service (ohne Preise, ohne Team). Farben: Tinte, Grau, Gelb als Fläche/Marker.
Schriften: Lora (Überschriften), Poppins (Text). Alle drei aus einer Quelle (BAUSTEINE, STUFEN, MONAT, FRAGEN).
"""
import random
from maas_strukturbild import t, ico, INK, GRAU, LINIE, HELL, GELB, LORA

TEXT2 = "#3d3a37"
BAUSTEINE = [  # Nr, Name, Icon, Versprechen (eine Zeile), zwei Punkte für die Explosionszeichnung
    ("1", "Kernpaket sofort sichtbar", "layout-dashboard", "Landingpages, laufende Postings, Dashboard",
     ["Fünf Landingpages, laufende Postings", "Dashboard, Report, Betreuungscall"]),
    ("2", "LinkedIn Power Package", "handshake", "Sichtbar bei Entscheidern",
     ["Vier Postings im Monat", "Netzwerk und Direktansprache"]),
    ("3", "Paid Ads", "trending-up", "Mehr Reichweite, gleiche Zielgruppen",
     ["Google, Meta und LinkedIn", "Laufend gesteuert und getestet"]),
    ("4", "Website-Entwicklung", "app-window", "Gefunden in Google und KI-Systemen",
     ["Sichtbar in Google und KI-Systemen", "Mit Tracking und DSGVO"]),
]
STUFEN = [  # Name, Anspruch, Text, Messpunkt
    ("Marketing", "Interessenten gewinnen.", "Deine Zielgruppen nehmen dich regelmäßig wahr – und daraus entstehen echte Anfragen.", "Anfragen"),
    ("Vertrieb", "Abschließen.", "Terminierung, Beratung, Abschluss – dein Vertrieb, wie du ihn kennst. Nur mit mehr Gesprächen.", "Abschlüsse"),
    ("Kundenbetreuung", "Kunden halten.", "Wer regelmäßig von dir hört, bleibt – und bringt neue Anlässe mit.", "Kunden, die bleiben"),
]
MONAT = [("app-window", "Umsetzen"), ("layout-dashboard", "Messen"), ("messages-square", "Besprechen"), ("refresh-cw", "Verbessern")]
FRAGEN = ["Welche Ziele?", "Welche Zielgruppen?", "Wie wahrgenommen?", "Wie ins Gespräch?", "Wie zum Abschluss?", "Funktioniert es?"]
FARBEN = [GELB, "#dcd8d2", "#e8e5e0", "#f3f1ee"]   # Kern innen → außen
RUECK = "Sichtbarkeit pflegt deinen Bestand und bringt neue Anlässe."


def umbruch(s, n):
    """einfacher Zeilenumbruch nach Zeichenzahl"""
    w, z = s.split(), [""]
    for x in w:
        if len(z[-1]) + len(x) + 1 > n and z[-1]:
            z.append(x)
        else:
            z[-1] = (z[-1] + " " + x).strip()
    return z


def zeilen(x, y, s, n, size, lh, fill=TEXT2, w=400, anchor="start"):
    return "".join(t(x, y + i * lh, z, size, w, fill, anchor) for i, z in enumerate(umbruch(s, n)))


def kanten(xm, xo, c, hm, ha, flach):
    """Steuerpunkte der oberen (s=-1) bzw. unteren (s=+1) Trichterkante: Öffnung (xm, Halbhöhe hm) → Hals (xo, ha)."""
    def k(s):
        return [(xm, c + s * hm), (xm + flach, c + s * hm), (xo - flach * .7, c + s * ha), (xo, c + s * ha)]
    return k


def trichter_pfad(xm, xo, xe, c, hm, ha, flach):
    o, u = kanten(xm, xo, c, hm, ha, flach)(-1), kanten(xm, xo, c, hm, ha, flach)(1)
    return (f"M{o[0][0]} {o[0][1]} C{o[1][0]} {o[1][1]} {o[2][0]} {o[2][1]} {o[3][0]} {o[3][1]} H{xe} V{u[3][1]} H{u[3][0]} "
            f"C{u[2][0]} {u[2][1]} {u[1][0]} {u[1][1]} {u[0][0]} {u[0][1]} Z")


def band_pfad(xm, xo, xe, c, aussen, innen, flach, s, dy=0):
    """Ein Band (Lage) eines Bausteins oben (s=-1) oder unten (s=+1), optional verschoben um dy (Explosion)."""
    a = kanten(xm, xo, c + dy, aussen[0], aussen[1], flach)(s)
    i = kanten(xm, xo, c + dy, innen[0], innen[1], flach)(s)
    return (f"M{a[0][0]} {a[0][1]} C{a[1][0]} {a[1][1]} {a[2][0]} {a[2][1]} {a[3][0]} {a[3][1]} H{xe} V{i[3][1]} H{i[3][0]} "
            f"C{i[2][0]} {i[2][1]} {i[1][0]} {i[1][1]} {i[0][0]} {i[0][1]} Z")


def punkte_vor(x0, x1, y0, y1, n, r, seed=5):
    rnd = random.Random(seed)
    return "".join(f'<circle cx="{rnd.uniform(x0, x1):.1f}" cy="{rnd.uniform(y0, y1):.1f}" r="{rnd.uniform(r * .6, r):.2f}" fill="#cfcac3"/>' for _ in range(n))


def messpunkt(x, y, label, s=1.0, oben=True):
    dy = -7.5 * s if oben else 9.5 * s
    return (f'<circle cx="{x}" cy="{y}" r="{3.2 * s}" fill="{GELB}" stroke="{INK}" stroke-width="{.5 * s}"/>'
            f'<circle cx="{x}" cy="{y}" r="{1 * s}" fill="{INK}"/>'
            + t(x, y + dy, label, 3.1 * s, 700, anchor="middle"))


def pfeilkopf():
    return (f'<defs><marker id="ig-pf" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
            f'<path d="M1 1 L8 5 L1 9" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')


def logo(w):
    """sofort-sichtbar-Logo (wie im Seitenkopf, logo-dunkel.svg) oben rechts, als eingebettetes Bild – steht so in SVG, PDF und PNG."""
    import base64, os
    pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "img", "logo-dunkel.svg")
    daten = base64.b64encode(open(pfad, "rb").read()).decode()
    lw = 46 if w >= 400 else 40
    lh = lw * 40 / 78
    return (f'<image x="{w - 20 - lw}" y="8" width="{lw}" height="{lh:.1f}" href="data:image/svg+xml;base64,{daten}" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="data:image/svg+xml;base64,{daten}"/>')


def svg_rahmen(w, h, inhalt, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" class="ig-svg" role="img" aria-label="{label}">'
            f'<rect width="{w}" height="{h}" fill="#fff"/>{pfeilkopf()}{inhalt}{logo(w)}</svg>')


def kopf(x, y, size, breite_marker=None, marker=GELB):
    breite_marker = breite_marker or size * 10.4
    """Kicker + H1 mit gelbem Marker auf „vor deinem Vertrieb.“ (ein Highlight wie im empiria-CD)"""
    o = t(x, y, "MARKETING AS A SERVICE · SOFORT SICHTBAR", size * .3, 700, INK, extra=' letter-spacing="0.8"')
    o += t(x, y + size * 1.25, "Die digitale Maschine", size, 700, font=LORA)
    o += f'<rect x="{x - size * .08}" y="{y + size * 1.55}" width="{breite_marker}" height="{size * 1.18}" rx="{size * .12}" fill="{marker}"/>'
    o += t(x, y + size * 2.45, "vor deinem Vertrieb.", size, 700, font=LORA)
    return o


def fundament_band(x, y, w, h, s=1.0, spalten=6):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{4 * s}" fill="{INK}"/>'
    o += t(x + 7 * s, y + 9 * s, "FUNDAMENT: STRATEGIE", 3 * s, 700, GELB, extra=' letter-spacing="0.6"')
    o += t(x + 7 * s, y + 15.5 * s, "Wohin will deine Agentur – und wen will sie gewinnen?", 3.6 * s, 600, "#fff")
    zeilen_n = 6 // spalten
    sw = (w - 14 * s) / spalten
    for i, f in enumerate(FRAGEN):
        zx = x + 7 * s + (i % spalten) * sw
        zy = y + 23 * s + (i // spalten) * 9 * s
        o += f'<circle cx="{zx + 2.6 * s}" cy="{zy + 2.6 * s}" r="{2.6 * s}" fill="none" stroke="{GELB}" stroke-width="{.45 * s}"/>'
        o += t(zx + 2.6 * s, zy + 3.7 * s, str(i + 1), 2.9 * s, 700, GELB, "middle")
        o += t(zx + 7 * s, zy + 3.8 * s, f, 3.2 * s, 500, "#cfcac3")
    return o


def monat_band(x, y, w, h, s=1.0, titel="Jeden Monat ein Stück besser."):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{4 * s}" fill="{GELB}"/>'
    o += t(x + 7 * s, y + 9 * s, "SO ARBEITEN WIR", 3 * s, 700, INK, extra=' letter-spacing="0.6"')
    o += t(x + 7 * s, y + 18 * s, titel, 6 * s, 700, font=LORA)
    schmal = w < 330
    sx0 = x + 7 * s if schmal else x + w * .44
    sw = (x + w - 7 * s - sx0) / 4
    ym = y + h - 12 * s if schmal else y + h / 2
    for i, (icon, name) in enumerate(MONAT):
        zx = sx0 + i * sw
        o += ico(icon, zx, ym - 4.5 * s, 9 * s)
        o += t(zx + 12 * s, ym + 2 * s, name, 4.2 * s, 700, font=LORA)
        if i < 3:
            px = zx + sw - 7 * s
            o += f'<path d="M{px} {ym - 2 * s} l{2.4 * s} {2 * s} l{-2.4 * s} {2 * s}" fill="none" stroke="{INK}" stroke-width="{.5 * s}" stroke-linecap="round" stroke-linejoin="round"/>'
    return o


# ---------------------------------------------------------------------------- A · Querformat
def entwurf_a():
    W, H, m = 420, 297, 18
    o = [kopf(m, 22, 11)]
    o.append(zeilen(250, 34, "Vertrieb läuft in drei Stufen. Wir optimieren die erste – damit aus regelmäßiger Wahrnehmung echte Anfragen werden, die direkt in deinen Vertrieb laufen.", 62, 3.7, 5.6))
    o.append(fundament_band(m, 64, W - 2 * m, 34))
    # Maschine
    c, xm, xo, xe = 158, m + 4, 168, 186
    hals = [5, 9, 13, 17]
    mund = [17, 26, 35, 44]
    o.append(punkte_vor(m - 2, m + 3, c - 40, c + 40, 26, .9))
    for k in (3, 2, 1, 0):
        o.append(f'<path d="{trichter_pfad(xm, xo, xe, c, mund[k], hals[k], 70)}" fill="{FARBEN[k]}" stroke="#fff" stroke-width=".8"/>')
    for k in (3, 2, 1):
        nr, name, icon, vers, _ = BAUSTEINE[k]
        y = c - mund[k] + (mund[k] - mund[k - 1]) / 2 + 1.2
        o.append(ico(icon, xm + 4, y - 3.2, 4.4))
        o.append(t(xm + 10.5, y, f"Baustein {nr} · {name}", 3.3, 700))
        o.append(t(xm + 88, y, vers, 3.1, 400, TEXT2))
    nr, name, icon, vers, _ = BAUSTEINE[0]
    o.append(ico(icon, xm + 4, c - 10, 5))
    o.append(t(xm + 11, c - 6, "Baustein 1", 3.3, 700))
    o.append(t(xm + 4, c + 2.5, "Kernpaket sofort sichtbar", 5, 700))
    o.append(t(xm + 4, c + 8.5, vers, 3.2, 400))
    for i in range(3):
        o.append(f'<circle cx="{xo - 6 + i * 6}" cy="{c + (i - 1) * 2}" r="1.2" fill="{INK}"/>')
    # Prozesspfeile
    A_ = 17
    xv0, xv1, xb1 = xe, 300, W - m
    o.append(f'<path d="M{xv0} {c - A_} H{xv1 - 8} L{xv1} {c} L{xv1 - 8} {c + A_} H{xv0} Z" fill="#fff" stroke="{INK}" stroke-width=".6" stroke-linejoin="round"/>')
    o.append(ico("handshake", xv0 + 8, c - 9, 8))
    o.append(t(xv0 + 19, c - 3.5, "Vertrieb", 6, 700, font=LORA))
    o.append(t(xv0 + 19, c + 4.5, "Terminierung  ›  Beratung  ›  Abschluss", 3.4, 500))
    o.append(f'<path d="M{xv1 + 2} {c - A_} H{xb1 - 4} Q{xb1} {c - A_} {xb1} {c - A_ + 4} V{c + A_ - 4} Q{xb1} {c + A_} {xb1 - 4} {c + A_} H{xv1 + 2} L{xv1 + 10} {c} Z" fill="{INK}"/>')
    o.append(ico("heart-handshake", xv1 + 16, c - 4.5, 9, GELB))
    o.append(t(xv1 + 29, c + 2, "Kundenbetreuung", 6, 700, "#fff", font=LORA))
    # Messpunkte oben auf dem Fluss
    for x, (_, _, _, mp) in zip([xo + 4, xv1 - 4, xb1 - 22], STUFEN):
        o.append(messpunkt(x, c - A_ - 1, mp))
    o.append(t(xb1, c - A_ - 18, "● Messpunkte im Dashboard", 3, 600, GRAU, "end"))
    # Rückweg unter dem Fluss
    yr = c + 50
    o.append(f'<path d="M{xb1 - 40} {c + A_} V{yr} H{m + 30} V{c + mund[3] + 2}" fill="none" stroke="{INK}" stroke-width=".45" marker-end="url(#ig-pf)"/>')
    o.append(f'<rect x="{(m + xb1) / 2 - 55}" y="{yr - 4.2}" width="110" height="8.4" rx="4.2" fill="{GELB}"/>')
    o.append(t((m + xb1) / 2, yr + 1.2, RUECK, 3.2, 600, anchor="middle"))
    # Stufentexte
    ys = 222
    for (x0, bw), (name, claim, text, mp), nr in zip([(m, 150), (xv0, 105), (xv1 + 4, xb1 - xv1 - 4)], STUFEN, (1, 2, 3)):
        o.append(t(x0, ys, f"STUFE {nr} · {name.upper()}" + (" · UNSER SCHWERPUNKT" if nr == 1 else ""), 2.9, 700, INK if nr == 1 else GRAU, extra=' letter-spacing="0.5"'))
        o.append(t(x0, ys + 8, claim, 6, 700, font=LORA))
        o.append(zeilen(x0, ys + 14.5, text, int(bw / 1.75), 3.4, 4.8))
    o.append(monat_band(m, 252, W - 2 * m, 28))
    o.append(t(m, H - 6, "Marketing as a Service · sofort sichtbar · ein festes Team, ein Ansprechpartner", 2.9, 500, GRAU))
    return svg_rahmen(W, H, "".join(o), "Infografik Marketing as a Service, Querformat")


# ---------------------------------------------------------------------------- B · Hochformat (A3 und Roll-up)
def entwurf_b(H=420, W=297):
    roll = H / W > 1.6
    m = 20 if not roll else 26
    s = 1.0 if not roll else 1.08
    o = [kopf(m, 26 if not roll else 60, 14 if not roll else 17)]
    y = 82 if not roll else 128
    o.append(zeilen(m, y, "Vertrieb läuft in drei Stufen. Wir optimieren die erste – damit aus regelmäßiger Wahrnehmung echte Anfragen werden, die direkt in deinen Vertrieb laufen.", 70, 4.2 * s, 6.3 * s))
    y += 20 * s
    o.append(fundament_band(m, y, W - 2 * m, 41 * s, s, spalten=3))
    y += 41 * s + (14 if not roll else 40)
    # senkrechter Trichter links, Texte rechts
    gx, gw = m, 118          # Grafikspalte
    cx = gx + gw / 2
    A_ = 26
    mund = [18, 28, 38, 48]
    hals = [7, 13, 19, A_]
    yt0 = y + 8
    yk = yt0 + (78 if not roll else 125)
    yh = yk + 14
    o.append(punkte_vor(cx - 46, cx + 46, yt0 - 7, yt0 - 2, 30, .9))
    for k in (3, 2, 1, 0):
        hm, ha = mund[k], hals[k]
        d = (f"M{cx - hm} {yt0} C{cx - hm} {yt0 + 30} {cx - ha} {yk - 30} {cx - ha} {yk} V{yh} H{cx + ha} V{yk} "
             f"C{cx + ha} {yk - 30} {cx + hm} {yt0 + 30} {cx + hm} {yt0} Z")
        o.append(f'<path d="{d}" fill="{FARBEN[k]}" stroke="#fff" stroke-width=".8"/>')
    for k, nr in ((3, "4"), (2, "3"), (1, "2")):
        x = cx - (mund[k] + mund[k - 1]) / 2
        o.append(f'<circle cx="{x}" cy="{yt0 + 7}" r="3" fill="#fff" stroke="{INK}" stroke-width=".4"/>')
        o.append(t(x, yt0 + 8.2, nr, 3.4, 700, anchor="middle"))
    o.append(f'<circle cx="{cx}" cy="{yt0 + 7}" r="3" fill="{INK}"/>')
    o.append(t(cx, yt0 + 8.2, "1", 3.4, 700, GELB, "middle"))
    o.append(t(cx, yt0 + 18, "Kernpaket", 4.2, 700, anchor="middle"))
    for i in range(3):
        o.append(f'<circle cx="{cx + (i - 1) * 2}" cy="{yk + 2 + i * 5}" r="1.3" fill="{INK}"/>')
    # Vertrieb + Kundenbetreuung als Pfeile nach unten
    yv1 = yh + (42 if not roll else 60)
    o.append(f'<path d="M{cx - A_} {yh} H{cx + A_} V{yv1 - 9} L{cx} {yv1} L{cx - A_} {yv1 - 9} Z" fill="#fff" stroke="{INK}" stroke-width=".6" stroke-linejoin="round"/>')
    o.append(ico("handshake", cx - 4.5, yh + 5, 9))
    o.append(t(cx, yh + 21, "Vertrieb", 6, 700, anchor="middle", font=LORA))
    for i, st in enumerate(["Terminierung", "Beratung", "Abschluss"]):
        o.append(t(cx, yh + 28 + i * 4.6, st, 3.4, 500, anchor="middle"))
    yb0, yb1 = yv1 + 2, yv1 + (40 if not roll else 54)
    o.append(f'<path d="M{cx - A_} {yb0} L{cx} {yb0 + 9} L{cx + A_} {yb0} V{yb1 - 4} Q{cx + A_} {yb1} {cx + A_ - 4} {yb1} H{cx - A_ + 4} Q{cx - A_} {yb1} {cx - A_} {yb1 - 4} Z" fill="{INK}"/>')
    o.append(ico("heart-handshake", cx - 4.5, yb0 + 12, 9, GELB))
    o.append(t(cx, yb0 + 28, "Kundenbetreuung", 5, 700, "#fff", "middle", font=LORA))
    # Messpunkte rechts an den Übergängen
    # Rückweg links
    o.append(f'<path d="M{cx - A_} {yb1 - 12} H{gx + 2} V{yt0 - 10} H{cx - 50} V{yt0 - 1}" fill="none" stroke="{INK}" stroke-width=".45" marker-end="url(#ig-pf)"/>')
    # Texte rechts
    tx = gx + gw + 14
    tw = W - m - tx
    n = int(tw / 1.85)
    blocks = [(yt0 + 2, 0), (yh + 4, 1), (yb0 + 6, 2)]
    for (yy, i) in blocks:
        name, claim, text, mp = STUFEN[i]
        o.append(t(tx, yy, f"STUFE {i + 1} · {name.upper()}", 3 * s, 700, INK if i == 0 else GRAU, extra=' letter-spacing="0.5"'))
        o.append(t(tx, yy + 9 * s, claim, 6.4 * s, 700, font=LORA))
        zl = umbruch(text, n)
        o.append(zeilen(tx, yy + 16 * s, text, n, 3.6 * s, 5.2 * s))
        ye = yy + 16 * s + len(zl) * 5.2 * s + 2
        if i == 0:
            for j, (nr, name_b, icon, vers, _) in enumerate(BAUSTEINE):
                by = ye + 2 + j * 7 * s
                fill = INK if nr == "1" else "#fff"
                o.append(f'<circle cx="{tx + 2.8}" cy="{by}" r="2.8" fill="{fill}" stroke="{INK}" stroke-width=".4"/>')
                o.append(t(tx + 2.8, by + 1.15, nr, 3.1, 700, GELB if nr == "1" else INK, "middle"))
                o.append(ico(icon, tx + 8, by - 2.4, 4.8))
                o.append(t(tx + 15, by + 1.3, name_b, 3.6 * s, 700))
            ye += 2 + 4 * 7 * s
        # Messpunkt direkt unter dem Stufentext, gestrichelt mit der Grafik verbunden
        yy = ye + 6 * s
        o.append(f'<path d="M{gx + gw - 6} {yy} H{gx + gw + 6}" stroke="{INK}" stroke-width=".35" stroke-dasharray="1.2 1.2"/>')
        o.append(f'<circle cx="{gx + gw + 6}" cy="{yy}" r="3" fill="{GELB}" stroke="{INK}" stroke-width=".5"/><circle cx="{gx + gw + 6}" cy="{yy}" r="1" fill="{INK}"/>')
        o.append(t(tx, yy - 1.2, "MESSPUNKT", 2.6 * s, 700, GRAU, extra=' letter-spacing="0.5"'))
        o.append(t(tx, yy + 3.8 * s, mp, 4 * s, 700))
    yr = yb1 + (12 if not roll else 22)
    o.append(f'<rect x="{m}" y="{yr - 5}" width="{W - 2 * m}" height="10" rx="5" fill="{GELB}"/>')
    o.append(t(W / 2, yr + 1.4, "↑  " + RUECK, 3.7 * s, 600, anchor="middle"))
    ym = yr + (10 if not roll else 16)
    o.append(monat_band(m, ym, W - 2 * m, 36 * s, s))
    o.append(t(m, H - (8 if not roll else 20), "Marketing as a Service · sofort sichtbar · ein festes Team, ein Ansprechpartner", 3 * s, 500, GRAU))
    return svg_rahmen(W, H, "".join(o), "Infografik Marketing as a Service, Hochformat")


# ---------------------------------------------------------------------------- Roll-up, Version 2: drei Sektionen
STRATEGIE = [("Segment", ["Privatkunden", "Gewerbekunden"]),
             ("Sparte", ["Leben", "Kranken", "Schaden/Unfall", "Kfz"]),
             ("Zielgruppe", ["Junge Familien", "Ärzte und Zahnärzte", "Private Bauherren", "Landwirte"])]
STEUERUNG = ["Funktioniert, was wir tun?", "Wo müssen wir nachsteuern?", "Wo liegen Möglichkeiten zur Optimierung?"]


def sektion(m, W, y, nr, label, titel, sub=""):
    """Abschnittskopf: durchgehende Linie, große Nummer, Kicker, Lora-Titel (wie die Abschnittsköpfe der Volksfest-Seite)."""
    o = f'<rect x="{m}" y="{y}" width="{W - 2 * m}" height=".7" fill="{INK}"/>'
    o += t(m, y + 15, nr, 13, 700, INK)
    o += t(m + 24, y + 8, label, 3.3, 700, INK, extra=' letter-spacing="0.6"')
    o += t(m + 24, y + 18, titel, 9, 700, font=LORA)
    if sub:
        o += zeilen(m + 24, y + 26, sub, 62, 3.9, 5.4)
    return o


STEUERUNG_KACHELN = [("Aufmerksamkeit", "Kommen mehr Leute – über welchen Kanal?"), ("Halten", "Bleiben sie – oder gehen sie schnell?"),
                     ("Google", "Werden wir gesehen und geklickt?"), ("Leads", "Was kommt dabei heraus?")]
STEUERUNG_EMPF = [("Landingpage", "Abschnitt umstellen, der kaum gelesen wird"), ("LinkedIn", "Thema verstärken, das Anfragen bringt"),
                  ("SEO", "Seite für einen gesuchten Begriff ausbauen")]


def entwurf_rollup2(ss=False):
    """ss=True: Version 2.1 in den Farben von sofort sichtbar (Blau → Violett), hell; Inhalt und Schrift unverändert."""
    W, H, m = 300, 600, 22
    if ss:
        FL, ST, AD, TST, LAGEN = "url(#ss-hell)", "url(#ss-voll)", "#b98cf0", "#fff", ["url(#ss-voll)", "#dcd3ec", "#e8e2f3", "#f3effa"]
    else:
        FL, ST, AD, TST, LAGEN = GELB, GELB, GELB, INK, FARBEN
    o = [kopf(m, 22, 16, marker=FL)]
    o.append(zeilen(m, 84, "Vertrieb läuft in drei Stufen. Wir optimieren die erste – damit aus regelmäßiger Wahrnehmung echte Anfragen werden, die direkt in deinen Vertrieb laufen.", 70, 4.3, 6.2))

    # 01 · Strategie
    y = 108
    o.append(sektion(m, W, y, "01", "STRATEGIE", "Wo willst du wachsen?", "Welche Ziele willst du erreichen – und mit welchen Zielgruppen? Daraus leiten wir alles Weitere ab."))
    ys = y + 43
    sw = (W - 2 * m - 2 * 10) / 3
    for i, (kopf_, werte) in enumerate(STRATEGIE):
        x = m + i * (sw + 10)
        o.append(t(x, ys, kopf_.upper(), 3.2, 700, GRAU, extra=' letter-spacing="0.5"'))
        for j, w_ in enumerate(werte):
            yy = ys + 4 + j * 10.5
            an = j == 0
            o.append(f'<rect x="{x}" y="{yy}" width="{sw}" height="8.4" rx="4.2" fill="{FL if an else "#fff"}" stroke="{("#c9b6ec" if ss else GELB) if an else LINIE}" stroke-width=".5"/>')
            o.append(t(x + 4.5, yy + 5.8, w_, 3.8, 600 if an else 400, INK))
        if i < 2:
            xa = x + sw + 2.5
            o.append(f'<path d="M{xa} {ys + 8.2} l4 0 m-1.8 -1.8 l1.8 1.8 l-1.8 1.8" fill="none" stroke="{INK}" stroke-width=".5" stroke-linecap="round" stroke-linejoin="round"/>')

    # 02 · Marketing und Vertrieb – ein zentraler Messpunkt: Leads
    y = 210
    o.append(sektion(m, W, y, "02", "MARKETING UND VERTRIEB", "Drei Stufen zum Vertriebserfolg."))
    gx, gw = m, 118
    cx = gx + gw / 2
    A_ = 26
    mund = [18, 28, 38, 48]
    hals = [7, 13, 19, A_]
    yt0 = y + 38
    yk, yh = yt0 + 70, yt0 + 84
    o.append(punkte_vor(cx - 46, cx + 46, yt0 - 7, yt0 - 2, 30, .9))
    for k in (3, 2, 1, 0):
        hm, ha = mund[k], hals[k]
        d = (f"M{cx - hm} {yt0} C{cx - hm} {yt0 + 28} {cx - ha} {yk - 28} {cx - ha} {yk} V{yh} H{cx + ha} V{yk} "
             f"C{cx + ha} {yk - 28} {cx + hm} {yt0 + 28} {cx + hm} {yt0} Z")
        o.append(f'<path d="{d}" fill="{LAGEN[k]}" stroke="#fff" stroke-width=".8"/>')
    for k, nr in ((3, "4"), (2, "3"), (1, "2")):
        x = cx - (mund[k] + mund[k - 1]) / 2
        o.append(f'<circle cx="{x}" cy="{yt0 + 7}" r="3" fill="#fff" stroke="{INK}" stroke-width=".4"/>')
        o.append(t(x, yt0 + 8.2, nr, 3.4, 700, anchor="middle"))
    o.append(f'<circle cx="{cx}" cy="{yt0 + 7}" r="3" fill="{INK}"/>')
    o.append(t(cx, yt0 + 8.2, "1", 3.4, 700, AD if ss else GELB, "middle"))
    o.append(t(cx, yt0 + 18, "Kernpaket", 4.2, 700, TST, anchor="middle"))
    for i in range(3):
        o.append(f'<circle cx="{cx + (i - 1) * 2}" cy="{yk - 8 + i * 4.5}" r="1.3" fill="{TST}"/>')
    # der eine Messpunkt: am Trichterausgang, groß
    ym_ = yh - 3
    o.append(f'<circle cx="{cx + A_ + 9}" cy="{ym_}" r="5" fill="{ST}" stroke="{INK if not ss else "none"}" stroke-width=".6"/><circle cx="{cx + A_ + 9}" cy="{ym_}" r="1.7" fill="{TST if ss else INK}"/>')
    o.append(f'<path d="M{cx + A_} {ym_} H{cx + A_ + 4}" stroke="{INK}" stroke-width=".5"/>')
    yv1 = yh + 40
    o.append(f'<path d="M{cx - A_} {yh} H{cx + A_} V{yv1 - 9} L{cx} {yv1} L{cx - A_} {yv1 - 9} Z" fill="#fff" stroke="{INK}" stroke-width=".6" stroke-linejoin="round"/>')
    o.append(ico("handshake", cx - 4.5, yh + 4, 9))
    o.append(t(cx, yh + 19, "Vertrieb", 6, 700, anchor="middle", font=LORA))
    for i, st in enumerate(["Terminierung", "Beratung", "Abschluss"]):
        o.append(t(cx, yh + 25.5 + i * 4.4, st, 3.4, 500, anchor="middle"))
    yb0, yb1 = yv1 + 2, yv1 + 34
    o.append(f'<path d="M{cx - A_} {yb0} L{cx} {yb0 + 9} L{cx + A_} {yb0} V{yb1 - 4} Q{cx + A_} {yb1} {cx + A_ - 4} {yb1} H{cx - A_ + 4} Q{cx - A_} {yb1} {cx - A_} {yb1 - 4} Z" fill="{INK}"/>')
    o.append(ico("heart-handshake", cx - 4.5, yb0 + 10, 9, AD))
    o.append(t(cx, yb0 + 26, "Kundenbetreuung", 5, 700, "#fff", "middle", font=LORA))
    o.append(f'<path d="M{cx - A_} {yb1 - 10} H{gx + 2} V{yt0 - 10} H{cx - 50} V{yt0 - 1}" fill="none" stroke="{INK}" stroke-width=".45" marker-end="url(#ig-pf)"/>')
    tx = gx + gw + 14
    n = int((W - m - tx) / 1.85)
    ende = 0
    for (yy, i) in [(yt0 + 2, 0), (yh - 3 + 16, 1), (yb0 + 8, 2)]:
        yy = max(yy, ende + 10)
        name, claim, text, mp = STUFEN[i]
        o.append(t(tx, yy, f"STUFE {i + 1} · {name.upper()}", 3, 700, INK if i == 0 else GRAU, extra=' letter-spacing="0.5"'))
        o.append(t(tx, yy + 9, claim, 6.4, 700, font=LORA))
        o.append(zeilen(tx, yy + 16, text, n, 3.6, 5.2))
        ye = yy + 16 + len(umbruch(text, n)) * 5.2
        if i == 0:
            for j, (nr, name_b, icon, vers, _) in enumerate(BAUSTEINE):
                by = ye + 4 + j * 7
                o.append(f'<circle cx="{tx + 2.8}" cy="{by}" r="2.8" fill="{INK if nr == "1" else "#fff"}" stroke="{INK}" stroke-width=".4"/>')
                o.append(t(tx + 2.8, by + 1.15, nr, 3.1, 700, AD if nr == "1" else INK, "middle"))
                o.append(ico(icon, tx + 8, by - 2.4, 4.8))
                o.append(t(tx + 15, by + 1.3, name_b, 3.6, 700))
            ye += 4 + 4 * 7
        ende = ye
    # Beschriftung des Messpunkts auf Höhe des Trichterausgangs
    o.append(t(tx, ym_ - 1.5, "MESSPUNKT", 2.8, 700, GRAU, extra=' letter-spacing="0.5"'))
    o.append(t(tx, ym_ + 4.5, "Leads: echte Anfragen", 4.6, 700))
    yr = yb1 + 10
    o.append(f'<rect x="{m}" y="{yr - 5}" width="{W - 2 * m}" height="10" rx="5" fill="{ST}"/>')
    o.append(t(W / 2, yr + 1.4, "↑  " + RUECK, 3.7, 600, TST, anchor="middle"))

    # 03 · Steuerung: Analytics-Dashboard (Noahs Dashboard) – vier Wirkungsfragen + Empfehlungen
    y = yr + 12
    o.append(sektion(m, W, y, "03", "STEUERUNG", "Funktioniert es?", "Wo müssen wir nachsteuern, wo liegen Möglichkeiten? Jeden Monat im Report und im Betreuungscall."))
    dx, dy, dw = m, y + 39, W - 2 * m
    dh = 76
    o.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="4" fill="#fff" stroke="{INK}" stroke-width=".6"/>')
    o.append(f'<path d="M{dx} {dy + 8} H{dx + dw}" stroke="{INK}" stroke-width=".4"/>')
    for i in range(3):
        o.append(f'<circle cx="{dx + 5 + i * 4}" cy="{dy + 4}" r="1.1" fill="{LINIE}"/>')
    o.append(t(dx + 20, dy + 5.3, "Analytics-Dashboard", 3.3, 700))
    # Kacheln 2 × 2
    kx0, ky0, kw, kh = dx + 5, dy + 13, 70, 28
    for i, (name, frage) in enumerate(STEUERUNG_KACHELN):
        kx = kx0 + (i % 2) * (kw + 4)
        ky = ky0 + (i // 2) * (kh + 4)
        lead = name == "Leads"
        o.append(f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="2.5" fill="{FL if lead else HELL}"/>')
        if lead:
            o.append(f'<circle cx="{kx + 5}" cy="{ky + 5.5}" r="2.4" fill="{ST}" stroke="{INK if not ss else "none"}" stroke-width=".45"/><circle cx="{kx + 5}" cy="{ky + 5.5}" r=".8" fill="{TST if ss else INK}"/>')
        o.append(t(kx + (10 if lead else 4), ky + 6.8, name, 3.6, 700))
        o.append(t(kx + 4, ky + 12.5, frage, 2.9, 400, INK if lead else TEXT2))
        pts = " ".join(f"{kx + 4 + j * (kw - 8) / 6:.1f},{ky + kh - 2.5 - v:.1f}" for j, v in enumerate([1, 3, 2, 4.5, 3.5, 5.5, 7]))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width=".55" stroke-linecap="round" stroke-linejoin="round"/>')
    # Empfehlungen
    ex = kx0 + 2 * kw + 4 + 7
    ew = dx + dw - 5 - ex
    o.append(t(ex, dy + 15, "EMPFEHLUNGEN", 2.8, 700, GRAU, extra=' letter-spacing="0.5"'))
    for j, (bereich, was) in enumerate(STEUERUNG_EMPF):
        ey = dy + 19 + j * 15.5
        o.append(f'<rect x="{ex}" y="{ey}" width="{ew}" height="12" rx="2" fill="#fff" stroke="{LINIE}" stroke-width=".45"/>')
        o.append(t(ex + 3, ey + 4.6, bereich, 3, 700))
        o.append(t(ex + 3, ey + 9.2, was, 2.7, 400, TEXT2))
    o.append(t(ex, dy + dh - 4, "Übernehmen – nach acht Wochen nachgeprüft", 2.8, 600, INK))
    o.append(t(m, dy + dh + 8, "Abschlüsse liegen im System deiner Agentur – die tracken wir bewusst nicht.", 3.4, 500, TEXT2))
    o.append(t(m, H - 5, "Marketing as a Service · sofort sichtbar · ein festes Team, ein Ansprechpartner", 3, 500, GRAU))
    defs = ('<defs><linearGradient id="ss-voll" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f55c8"/><stop offset=".55" stop-color="#8324b9"/><stop offset="1" stop-color="#a23edb"/></linearGradient>'
            '<linearGradient id="ss-hell" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2f55c8" stop-opacity=".16"/><stop offset="1" stop-color="#a23edb" stop-opacity=".22"/></linearGradient></defs>') if ss else ""
    return svg_rahmen(W, H, defs + "".join(o), "Infografik Marketing as a Service, Roll-up Version 2" + (".1 in den Farben von sofort sichtbar" if ss else ""))


# ---------------------------------------------------------------------------- Roll-up, Version 3: ein Blick in die Maschine
EINSATZ = [("megaphone", "Wahrgenommen werden", "Laufende Postings auf LinkedIn, Facebook und Instagram. Wer dich sieht, findet hier mehr."),
           ("mail", "Mailings verschicken", "Per E-Mail, gern auch per Post: Du schickst den Link – deine Kunden landen auf der Seite."),
           ("calendar", "Termine vor- und nachbereiten", "Vorher zur Einstimmung mit Checkliste und Podcast, nachher zum Thema aus dem Gespräch.")]
LINKEDIN_WEG = [("target", "Fokus-Kunden festlegen", "gemeinsam"), ("users", "Netzwerk gezielt aufbauen", "wir"),
                ("eye", "Ihre Postings auswerten", "wir"), ("message-square-text", "Antwortvorschlag mit Link", "wir"),
                ("message-circle", "Kommentieren in deinem Ton", "du"), ("calendar", "Nach dem dritten: Termin", "du")]


def entwurf_rollup3():
    W, H, m = 300, 600, 22
    o = [t(m, 22, "MARKETING AS A SERVICE · SOFORT SICHTBAR", 4.8, 700, INK, extra=' letter-spacing="0.8"')]
    o.append(t(m, 42, "Ein Blick in", 16, 700, font=LORA))
    o.append(f'<rect x="{m - 1.3}" y="{47}" width="{112}" height="{19}" rx="2" fill="{GELB}"/>')
    o.append(t(m, 61.5, "die Maschine.", 16, 700, font=LORA))
    o.append(zeilen(m, 80, "So läuft dein Vertrieb mit Baustein 1 und 2 – Woche für Woche. Paid Ads verstärken, die Website schließt die Lücke.", 70, 4.3, 6.2))

    # 1 · Landingpage als Mittelpunkt
    y = 98
    o.append(sektion(m, W, y, "1", "BAUSTEIN 1 · KERNPAKET", "Für jede Zielgruppe eine Landingpage."))
    lx, ly, lw, lh = 178, y + 32, 100, 116
    o.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="4" fill="#fff" stroke="{INK}" stroke-width=".7"/>')
    o.append(f'<path d="M{lx} {ly + 8} H{lx + lw}" stroke="{INK}" stroke-width=".4"/>')
    for i in range(3):
        o.append(f'<circle cx="{lx + 5 + i * 4}" cy="{ly + 4}" r="1.1" fill="{LINIE}"/>')
    o.append(f'<rect x="{lx + 5}" y="{ly + 13}" width="{lw - 10}" height="26" rx="2.5" fill="{GELB}"/>')
    o.append(t(lx + 9, ly + 20, "LANDINGPAGE", 2.6, 700, INK, extra=' letter-spacing="0.5"'))
    o.append(t(lx + 9, ly + 29, "Junge Familien", 6, 700, font=LORA))
    o.append(t(lx + 9, ly + 35, "mit deinem Logo und Kontakt", 3, 400))
    for j, (icon, txt) in enumerate([("clipboard-list", "Checkliste zum Download"), ("mic-vocal", "Podcast-Folge"), ("calendar", "Termin direkt buchen")]):
        yy = ly + 47 + j * 13
        o.append(f'<rect x="{lx + 5}" y="{yy}" width="{lw - 10}" height="10" rx="2" fill="{HELL}"/>')
        o.append(ico(icon, lx + 8, yy + 2.3, 5.4))
        o.append(t(lx + 16, yy + 6.6, txt, 3.4, 600))
    o.append(t(lx + 5, ly + lh - 5, "Echte Anfrage – direkt bei dir.", 3.2, 700))
    for j, (icon, titel, text) in enumerate(EINSATZ):
        yy = ly + 4 + j * 38
        o.append(ico(icon, m, yy - 4, 9))
        o.append(t(m + 13, yy + 3, titel, 5.2, 700, font=LORA))
        o.append(zeilen(m + 13, yy + 11, text, 40, 3.6, 5.1))
        o.append(f'<path d="M{m + 150} {yy + 1} H{lx - 2}" fill="none" stroke="{INK}" stroke-width=".5" marker-end="url(#ig-pf)"/>')

    # 2 · LinkedIn als aktiver Vertriebskanal
    y = 262
    o.append(sektion(m, W, y, "2", "BAUSTEIN 2 · LINKEDIN POWER PACKAGE", "LinkedIn als aktiver Vertriebskanal.",
                     "Mit dem Sales Navigator wissen wir, wen du gewinnen willst – und wann der richtige Moment für ein Gespräch ist."))
    ty = y + 52
    sw = (W - 2 * m) / 6
    o.append(f'<path d="M{m + sw / 2} {ty} H{W - m - sw / 2}" stroke="{INK}" stroke-width=".5" stroke-dasharray="1.6 1.4"/>')
    for i, (icon, titel, wer) in enumerate(LINKEDIN_WEG):
        x = m + i * sw + sw / 2
        letzter = i == 5
        o.append(f'<circle cx="{x}" cy="{ty}" r="8" fill="{GELB if letzter else "#fff"}" stroke="{INK}" stroke-width=".6"/>')
        o.append(ico(icon, x - 4.5, ty - 4.5, 9))
        o.append(t(x, ty + 15, str(i + 1), 3, 700, GRAU, "middle"))
        for k, z in enumerate(umbruch(titel, 13)):
            o.append(t(x, ty + 22 + k * 4.6, z, 3.7, 700, anchor="middle"))
        farbe = INK if wer == "du" else "#fff"
        bw = len(wer) * 1.9 + 7
        o.append(f'<rect x="{x - bw / 2}" y="{ty + 37}" width="{bw}" height="6" rx="3" fill="{farbe}" stroke="{INK}" stroke-width=".4"/>')
        o.append(t(x, ty + 41.2, wer, 3, 700, "#fff" if wer == "du" else INK, "middle"))
    o.append(zeilen(m, ty + 54, "Wir werten regelmäßig aus, wer von deinen Fokus-Kunden etwas gepostet hat, und liefern dir den Link mit einem Antwortvorschlag. Den Kommentar schreibst du selbst – du entscheidest über Ton und Zungenschlag. Nach dem dritten Kommentar folgt die Einladung zum Gespräch.", 66, 3.8, 5.4))

    # 3 · Verstärken und abrunden
    y = 400
    o.append(sektion(m, W, y, "3", "BAUSTEIN 3 UND 4", "Verstärken und abrunden."))
    kw = (W - 2 * m - 8) / 2
    karten = [("trending-up", "BAUSTEIN 3 · PAID ADS", "Mehr Tempo.",
               "Mehr Menschen aus denselben Zielgruppen sehen dich. Was in Baustein 1 und 2 läuft, läuft mit mehr Schwung."),
              ("app-window", "BAUSTEIN 4 · WEBSITE", "Die Lücke schließen.",
               "Die Landingpages zeigen deine Themen, die Website zeigt deine Agentur – ordentlich, schnell und auffindbar in Google und KI-Systemen.")]
    for i, (icon, label, titel, text) in enumerate(karten):
        x = m + i * (kw + 8)
        yy = y + 30
        o.append(f'<rect x="{x}" y="{yy}" width="{kw}" height="62" rx="4" fill="{HELL}"/>')
        o.append(ico(icon, x + 6, yy + 6, 9))
        o.append(t(x + 6, yy + 23, label, 2.9, 700, GRAU, extra=' letter-spacing="0.4"'))
        o.append(t(x + 6, yy + 32, titel, 6.4, 700, font=LORA))
        o.append(zeilen(x + 6, yy + 40, text, 34, 3.6, 5.1))

    # Abschluss: was du davon hast
    y = 504
    o.append(f'<rect x="{m}" y="{y}" width="{W - 2 * m}" height="58" rx="5" fill="{INK}"/>')
    o.append(t(m + 8, y + 11, "WAS DU DAVON HAST", 3, 700, GELB, extra=' letter-spacing="0.6"'))
    o.append(t(m + 8, y + 23, "Mehr Gespräche mit den Richtigen.", 7.6, 700, "#fff", font=LORA))
    for j, z in enumerate(["Du weißt, wen du gewinnen willst – und wann du ihn ansprichst.",
                           "Jede Zielgruppe hat ihre Seite: zum Finden, Verschicken, Vor- und Nachbereiten.",
                           "Du führst die Gespräche. Den Rest übernimmt die Maschine."]):
        yy = y + 33 + j * 7.5
        o.append(f'<path d="M{m + 8} {yy - 1.6} l1.6 1.6 l3.2 -3.2" fill="none" stroke="{GELB}" stroke-width=".6" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(t(m + 15, yy, z, 3.7, 500, "#fff"))
    o.append(t(m, H - 5, "Marketing as a Service · sofort sichtbar · ein festes Team, ein Ansprechpartner", 3, 500, GRAU))
    return svg_rahmen(W, H, "".join(o), "Infografik Marketing as a Service, Roll-up Version 3: ein Blick in die Maschine")


# ---------------------------------------------------------------------------- B2: Hochformat A3 mit drei Sektionen (verdichtet aus Roll-up V2)
STUFEN_KURZ = [("Interessenten gewinnen.", "Deine Zielgruppen nehmen dich regelmäßig wahr – daraus entstehen echte Anfragen."),
               ("Abschließen.", "Terminierung, Beratung, Abschluss – wie du es kennst. Nur mit mehr Gesprächen."),
               ("Kunden halten.", "Wer regelmäßig von dir hört, bleibt – und bringt neue Anlässe mit.")]


def sektion_kompakt(m, W, y, nr, label, titel, sub=""):
    o = f'<rect x="{m}" y="{y}" width="{W - 2 * m}" height=".6" fill="{INK}"/>'
    o += t(m, y + 12, nr, 10, 700, INK)
    o += t(m + 18, y + 6.5, label, 2.8, 700, INK, extra=' letter-spacing="0.5"')
    o += t(m + 18, y + 14.5, titel, 7.4, 700, font=LORA)
    if sub:
        o += t(m + 18, y + 20.5, sub, 3.3, 400, TEXT2)
    return o


def entwurf_b2():
    W, H, m = 297, 420, 18
    o = [kopf(m, 18, 12)]
    o.append(zeilen(m + 150, 34, "Vertrieb läuft in drei Stufen. Wir optimieren die erste – damit aus regelmäßiger Wahrnehmung echte Anfragen werden, die direkt in deinen Vertrieb laufen.", 48, 3.5, 5))

    # 01 · Strategie – eine Zeile mit dem Auswahlpfad
    y = 62
    o.append(sektion_kompakt(m, W, y, "01", "STRATEGIE", "Wo willst du wachsen?", "Welche Ziele willst du erreichen – und mit welchen Zielgruppen?"))
    ys = y + 29
    sw = (W - 2 * m - 2 * 8) / 3
    for i, (kopf_, werte) in enumerate(STRATEGIE):
        x = m + i * (sw + 8)
        o.append(t(x, ys, kopf_.upper(), 2.7, 700, GRAU, extra=' letter-spacing="0.4"'))
        for j, w_ in enumerate(werte[:3]):
            yy = ys + 3 + j * 8
            an = j == 0
            o.append(f'<rect x="{x}" y="{yy}" width="{sw}" height="6.4" rx="3.2" fill="{GELB if an else "#fff"}" stroke="{GELB if an else LINIE}" stroke-width=".45"/>')
            o.append(t(x + 3.5, yy + 4.5, w_, 3.2, 600 if an else 400))
        if i < 2:
            xa = x + sw + 1.8
            o.append(f'<path d="M{xa} {ys + 6.2} l3.2 0 m-1.5 -1.5 l1.5 1.5 l-1.5 1.5" fill="none" stroke="{INK}" stroke-width=".45" stroke-linecap="round" stroke-linejoin="round"/>')

    # 02 · Marketing und Vertrieb – kompakter Trichter, ein Messpunkt
    y = 128
    o.append(sektion_kompakt(m, W, y, "02", "MARKETING UND VERTRIEB", "Drei Stufen zum Vertriebserfolg."))
    gx, gw = m, 96
    cx = gx + gw / 2
    A_ = 21
    mund = [14, 22, 30, 38]
    hals = [6, 11, 16, A_]
    yt0 = y + 27
    yk, yh = yt0 + 50, yt0 + 60
    o.append(punkte_vor(cx - 36, cx + 36, yt0 - 5.5, yt0 - 1.5, 26, .75))
    for k in (3, 2, 1, 0):
        hm, ha = mund[k], hals[k]
        d = (f"M{cx - hm} {yt0} C{cx - hm} {yt0 + 20} {cx - ha} {yk - 20} {cx - ha} {yk} V{yh} H{cx + ha} V{yk} "
             f"C{cx + ha} {yk - 20} {cx + hm} {yt0 + 20} {cx + hm} {yt0} Z")
        o.append(f'<path d="{d}" fill="{FARBEN[k]}" stroke="#fff" stroke-width=".7"/>')
    for k, nr in ((3, "4"), (2, "3"), (1, "2")):
        x = cx - (mund[k] + mund[k - 1]) / 2
        o.append(f'<circle cx="{x}" cy="{yt0 + 5.5}" r="2.4" fill="#fff" stroke="{INK}" stroke-width=".35"/>')
        o.append(t(x, yt0 + 6.5, nr, 2.8, 700, anchor="middle"))
    o.append(f'<circle cx="{cx}" cy="{yt0 + 5.5}" r="2.4" fill="{INK}"/>')
    o.append(t(cx, yt0 + 6.5, "1", 2.8, 700, GELB, "middle"))
    o.append(t(cx, yt0 + 14, "Kernpaket", 3.4, 700, anchor="middle"))
    for i in range(3):
        o.append(f'<circle cx="{cx + (i - 1) * 1.6}" cy="{yk - 7 + i * 3.6}" r="1.05" fill="{INK}"/>')
    ym_ = yh - 2.5
    o.append(f'<circle cx="{cx + A_ + 7}" cy="{ym_}" r="4" fill="{GELB}" stroke="{INK}" stroke-width=".5"/><circle cx="{cx + A_ + 7}" cy="{ym_}" r="1.4" fill="{INK}"/>')
    o.append(f'<path d="M{cx + A_} {ym_} H{cx + A_ + 3}" stroke="{INK}" stroke-width=".45"/>')
    yv1 = yh + 30
    o.append(f'<path d="M{cx - A_} {yh} H{cx + A_} V{yv1 - 7} L{cx} {yv1} L{cx - A_} {yv1 - 7} Z" fill="#fff" stroke="{INK}" stroke-width=".55" stroke-linejoin="round"/>')
    o.append(ico("handshake", cx - 3.5, yh + 3, 7))
    o.append(t(cx, yh + 14.5, "Vertrieb", 4.8, 700, anchor="middle", font=LORA))
    o.append(t(cx, yh + 19.5, "Termin · Beratung · Abschluss", 2.6, 500, anchor="middle"))
    yb0, yb1 = yv1 + 1.5, yv1 + 26
    o.append(f'<path d="M{cx - A_} {yb0} L{cx} {yb0 + 7} L{cx + A_} {yb0} V{yb1 - 3} Q{cx + A_} {yb1} {cx + A_ - 3} {yb1} H{cx - A_ + 3} Q{cx - A_} {yb1} {cx - A_} {yb1 - 3} Z" fill="{INK}"/>')
    o.append(ico("heart-handshake", cx - 3.5, yb0 + 8, 7, GELB))
    o.append(t(cx, yb0 + 20, "Kundenbetreuung", 4, 700, "#fff", "middle", font=LORA))
    o.append(f'<path d="M{cx - A_} {yb1 - 8} H{gx + 1.5} V{yt0 - 8} H{cx - 40} V{yt0 - 1}" fill="none" stroke="{INK}" stroke-width=".4" marker-end="url(#ig-pf)"/>')
    tx = gx + gw + 12
    n = int((W - m - tx) / 1.6)
    # Stufe 1 mit Legende der Bausteine (zweispaltig), dann Messpunkt auf Höhe des Ausgangs, dann Stufe 2 und 3
    claim, text = STUFEN_KURZ[0]
    yy = yt0 + 1
    o.append(t(tx, yy, "STUFE 1 · MARKETING", 2.7, 700, INK, extra=' letter-spacing="0.4"'))
    o.append(t(tx, yy + 7.5, claim, 5.4, 700, font=LORA))
    o.append(zeilen(tx, yy + 13.5, text, n, 3.3, 4.6))
    by0 = yy + 13.5 + len(umbruch(text, n)) * 4.6 + 2
    halb = (W - m - tx) / 2
    for j, (nr, name_b, icon, vers, _) in enumerate(BAUSTEINE):
        bx = tx + (j % 2) * halb
        by = by0 + (j // 2) * 6
        o.append(f'<circle cx="{bx + 2.3}" cy="{by}" r="2.3" fill="{INK if nr == "1" else "#fff"}" stroke="{INK}" stroke-width=".35"/>')
        o.append(t(bx + 2.3, by + 1, nr, 2.6, 700, GELB if nr == "1" else INK, "middle"))
        o.append(t(bx + 6.5, by + 1.1, name_b.replace(" sofort sichtbar", ""), 3.1, 700))
    o.append(t(tx, ym_ - 1.2, "MESSPUNKT", 2.4, 700, GRAU, extra=' letter-spacing="0.4"'))
    o.append(t(tx, ym_ + 3.8, "Leads: echte Anfragen", 4, 700))
    for i, (yy, nr, name) in enumerate([(yh + 13, 2, "VERTRIEB"), (yb0 + 8, 3, "KUNDENBETREUUNG")]):
        claim, text = STUFEN_KURZ[nr - 1]
        o.append(t(tx, yy, f"STUFE {nr} · {name}", 2.7, 700, GRAU, extra=' letter-spacing="0.4"'))
        o.append(t(tx, yy + 7.5, claim, 5.4, 700, font=LORA))
        o.append(zeilen(tx, yy + 13.5, text, n, 3.3, 4.6))
    yr = yb1 + 7
    o.append(f'<rect x="{m}" y="{yr - 4}" width="{W - 2 * m}" height="8" rx="4" fill="{GELB}"/>')
    o.append(t(W / 2, yr + 1.2, "↑  " + RUECK, 3.2, 600, anchor="middle"))

    # 03 · Steuerung – Dashboard flach
    y = yr + 9
    o.append(sektion_kompakt(m, W, y, "03", "STEUERUNG", "Funktioniert es?", "Wo müssen wir nachsteuern? Jeden Monat im Report und im Betreuungscall."))
    dx, dy, dw, dh = m, y + 26, W - 2 * m, 60
    o.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="3.5" fill="#fff" stroke="{INK}" stroke-width=".55"/>')
    o.append(f'<path d="M{dx} {dy + 7} H{dx + dw}" stroke="{INK}" stroke-width=".35"/>')
    for i in range(3):
        o.append(f'<circle cx="{dx + 4.5 + i * 3.5}" cy="{dy + 3.5}" r=".95" fill="{LINIE}"/>')
    o.append(t(dx + 17, dy + 4.7, "Analytics-Dashboard", 2.9, 700))
    kw, kh = 54, 22
    for i, (name, frage) in enumerate(STEUERUNG_KACHELN):
        kx = dx + 4 + (i % 2) * (kw + 3)
        ky = dy + 10 + (i // 2) * (kh + 3)
        lead = name == "Leads"
        o.append(f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="2" fill="{GELB if lead else HELL}"/>')
        o.append(t(kx + 3, ky + 5.2, name, 3.1, 700))
        o.append(zeilen(kx + 3, ky + 10, frage, 32, 2.5, 3.2, INK if lead else TEXT2))
        pts = " ".join(f"{kx + 3 + j * (kw - 6) / 6:.1f},{ky + kh - 2 - v:.1f}" for j, v in enumerate([0.6, 2, 1.4, 3, 2.3, 3.6, 4.6]))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width=".45" stroke-linecap="round" stroke-linejoin="round"/>')
    ex = dx + 4 + 2 * kw + 3 + 7
    ew = dx + dw - 4 - ex
    o.append(t(ex, dy + 12, "EMPFEHLUNGEN", 2.5, 700, GRAU, extra=' letter-spacing="0.4"'))
    for j, (bereich, was) in enumerate(STEUERUNG_EMPF):
        ey = dy + 15 + j * 12
        o.append(f'<rect x="{ex}" y="{ey}" width="{ew}" height="8" rx="1.6" fill="#fff" stroke="{LINIE}" stroke-width=".4"/>')
        o.append(t(ex + 2.5, ey + 5.2, bereich + ":", 2.8, 700))
        o.append(t(ex + 2.5 + len(bereich) * 1.75 + 3, ey + 5.2, was, 2.6, 400, TEXT2))
    o.append(t(ex, dy + dh - 3, "Übernehmen – nach acht Wochen nachgeprüft", 2.5, 600))
    o.append(t(m, dy + dh + 6, "Abschlüsse liegen im System deiner Agentur – die tracken wir bewusst nicht.", 3, 500, TEXT2))
    o.append(t(m, H - 6, "Marketing as a Service · sofort sichtbar · ein festes Team, ein Ansprechpartner", 2.7, 500, GRAU))
    return svg_rahmen(W, H, "".join(o), "Infografik Marketing as a Service, Hochformat mit drei Sektionen")


ENTWUERFE = {"a": (entwurf_a, 420, 297), "b": (entwurf_b, 297, 420), "b2": (entwurf_b2, 297, 420),
             "rollup2": (entwurf_rollup2, 1000, 2000), "rollup21": (lambda: entwurf_rollup2(ss=True), 1000, 2000), "rollup3": (entwurf_rollup3, 1000, 2000)}


# ---------------------------------------------------------------------------- Export
def exportieren():
    """Schreibt je Entwurf SVG, PDF (echtes Format) und PNG nach assets/maas/infografik/ und die SVGs in die JSON (für die Seite)."""
    import json, os, subprocess, tempfile
    here = os.path.dirname(os.path.abspath(__file__))
    ziel = os.path.join(here, "assets", "maas", "infografik")
    os.makedirs(ziel, exist_ok=True)
    build = os.path.join(tempfile.gettempdir(), "maas_infografik_build")
    os.makedirs(build, exist_ok=True)
    fonts = "file://" + os.path.expanduser("~/Projekte/empiria/site/assets/fonts/fonts.local.css")
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    daten = os.path.join(here, "story6.11tydata.json")
    d = json.load(open(daten, encoding="utf-8"))
    svgs = {}
    for k, (f, wmm, hmm) in ENTWUERFE.items():
        s = f()
        svgs[k] = s
        open(os.path.join(ziel, f"{k}.svg"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n' + s)
        # PDF im echten Format
        html = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{fonts}">'
                f'<style>@page{{size:{wmm}mm {hmm}mm;margin:0}}html,body{{margin:0}}svg{{display:block;width:{wmm}mm;height:{hmm}mm}}</style></head>'
                f'<body>{s}</body></html>')
        src = os.path.join(build, f"{k}.html")
        open(src, "w", encoding="utf-8").write(html)
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                        f"--print-to-pdf={os.path.join(ziel, k + '.pdf')}", "--virtual-time-budget=5000", "file://" + src],
                       capture_output=True, timeout=180)
        # PNG: 3000 px Breite (Roll-up 2400)
        vb = s.split('viewBox="0 0 ')[1].split('"')[0].split()
        px = 1500 if not k.startswith("rollup") else 1200
        ph = round(px * float(vb[1]) / float(vb[0]))
        html2 = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{fonts}">'
                 f'<style>html,body{{margin:0}}svg{{display:block;width:{px}px;height:{ph}px}}</style></head><body>{s}</body></html>')
        src2 = os.path.join(build, f"{k}-png.html")
        open(src2, "w", encoding="utf-8").write(html2)
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        "--force-device-scale-factor=2", f"--window-size={px},{ph}", "--virtual-time-budget=5000",
                        f"--screenshot={os.path.join(ziel, k + '.png')}", "file://" + src2], capture_output=True, timeout=180)
        print(k, "ok")
    d["maas"]["infografik"] = svgs
    json.dump(d, open(daten, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(daten, "a").write("\n")


if __name__ == "__main__":
    exportieren()
