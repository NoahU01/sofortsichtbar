"""Infografik „Marketing as a Service“ – drei Entwürfe, gezeichnet in Millimetern (1 Einheit = 1 mm).

A  Querformat DIN A3 (420 × 297): Strategie oben · Maschine waagerecht mit Messpunkten · Stufentexte · Monatsrhythmus unten
B  Hochformat DIN A3 (297 × 420) und Roll-up 100 × 200 cm (gleiche Komposition, Seitenverhältnis 1 : 2)
C  Explosionszeichnung DIN A3 quer: der Trichter in seine vier Bausteine zerlegt, mit Beschriftungen; Vertrieb kleiner rechts

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


def svg_rahmen(w, h, inhalt, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" class="ig-svg" role="img" aria-label="{label}">'
            f'<rect width="{w}" height="{h}" fill="#fff"/>{pfeilkopf()}{inhalt}</svg>')


def kopf(x, y, size, breite_marker=None):
    breite_marker = breite_marker or size * 10.4
    """Kicker + H1 mit gelbem Marker auf „vor deinem Vertrieb.“ (ein Highlight wie im empiria-CD)"""
    o = t(x, y, "MARKETING AS A SERVICE · SOFORT SICHTBAR", size * .3, 700, INK, extra=' letter-spacing="0.8"')
    o += t(x, y + size * 1.25, "Die digitale Maschine", size, 700, font=LORA)
    o += f'<rect x="{x - size * .08}" y="{y + size * 1.55}" width="{breite_marker}" height="{size * 1.18}" rx="{size * .12}" fill="{GELB}"/>'
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


# ---------------------------------------------------------------------------- C · Explosionszeichnung
def entwurf_c():
    """Explosionszeichnung: Trichter in seine Lagen zerlegt (oben nach oben, unten nach unten), Beschriftung links
    mit kurzen waagerechten Hinweislinien; Vertrieb und Kundenbetreuung kompakt rechts; Monatsrhythmus unten."""
    W, H, m = 420, 297, 18
    o = [kopf(m, 22, 11)]
    o.append(zeilen(250, 34, "Was in der Maschine steckt: vier Bausteine, Lage für Lage. Jede Lage macht den Trichter größer – und schiebt mehr in deinen Vertrieb.", 62, 3.7, 5.6))
    c, xm, xo, xe = 152, 150, 292, 306
    mund = [16, 26, 36, 46]
    hals = [5, 9, 13, 17]
    gap = 12
    o.append(punkte_vor(xm - 12, xm - 4, c - 70, c + 70, 34, 1.0))
    o.append(f'<path d="{trichter_pfad(xm, xo, xe, c, mund[0], hals[0], 60)}" fill="{GELB}"/>')
    for k in (1, 2, 3):
        dy = k * gap
        for s_ in (-1, 1):
            o.append(f'<path d="{band_pfad(xm, xo, xe, c, (mund[k], hals[k]), (mund[k - 1], hals[k - 1]), 60, s_, s_ * dy)}" '
                     f'fill="{FARBEN[k]}" stroke="{INK}" stroke-width=".25"/>')
            # Explosionsrichtung als kleiner Pfeil an der Öffnung
        o.append(f'<path d="M{xm + 8} {c - mund[k - 1] - (k - 1) * gap - 1.5} V{c - mund[k - 1] - dy + 1.5}" stroke="{GRAU}" stroke-width=".3" stroke-dasharray="1 1"/>')
    # Beschriftung links, auf Höhe der oberen Lage
    for k in (3, 2, 1):
        nr, name, icon, vers, pkt = BAUSTEINE[k]
        yb = c - (mund[k] + mund[k - 1]) / 2 - k * gap
        o.append(f'<path d="M{xm - 16} {yb} H{xm + 3}" stroke="{INK}" stroke-width=".3"/><circle cx="{xm + 3}" cy="{yb}" r=".9" fill="{INK}"/>')
        o.append(t(xm - 18, yb - 4.5, f"BAUSTEIN {nr}", 2.7, 700, GRAU, "end", extra=' letter-spacing="0.4"'))
        o.append(t(xm - 18, yb + 1.5, name, 4.3, 700, anchor="end", font=LORA))
        o.append(t(xm - 18, yb + 7, " · ".join(pkt), 2.9, 400, TEXT2, "end"))
    nr, name, icon, vers, pkt = BAUSTEINE[0]
    o.append(ico(icon, xm + 6, c - 7, 5))
    o.append(t(xm + 13, c - 3, "Baustein 1", 3.2, 700))
    o.append(t(xm + 6, c + 5, "Kernpaket", 5, 700))
    o.append(f'<path d="M{xm - 16} {c} H{xm + 3}" stroke="{INK}" stroke-width=".3"/>')
    o.append(t(xm - 18, c - 4.5, "BAUSTEIN 1 · HERZSTÜCK", 2.7, 700, INK, "end", extra=' letter-spacing="0.4"'))
    o.append(t(xm - 18, c + 1.5, name, 4.3, 700, anchor="end", font=LORA))
    o.append(t(xm - 18, c + 7, " · ".join(pkt), 2.9, 400, TEXT2, "end"))
    for i in range(3):
        o.append(f'<circle cx="{xo - 8 + i * 6}" cy="{c + (i - 1) * 1.5}" r="1.1" fill="{INK}"/>')
    # rechts: Vertrieb und Kundenbetreuung
    A_ = 17
    xv1, xb1 = 360, W - m
    o.append(f'<path d="M{xe} {c - A_} H{xv1 - 7} L{xv1} {c} L{xv1 - 7} {c + A_} H{xe} Z" fill="#fff" stroke="{INK}" stroke-width=".6" stroke-linejoin="round"/>')
    o.append(t(xe + 6, c - 2, "Vertrieb", 5.4, 700, font=LORA))
    o.append(t(xe + 6, c + 4.5, "Termin › Beratung", 2.9, 500))
    o.append(t(xe + 6, c + 8.5, "› Abschluss", 2.9, 500))
    o.append(f'<path d="M{xv1 + 2} {c - A_} H{xb1 - 4} Q{xb1} {c - A_} {xb1} {c - A_ + 4} V{c + A_ - 4} Q{xb1} {c + A_} {xb1 - 4} {c + A_} H{xv1 + 2} L{xv1 + 8} {c} Z" fill="{INK}"/>')
    o.append(ico("heart-handshake", xv1 + 13, c - 10, 7, GELB))
    o.append(t(xv1 + 12, c + 3, "Kunden-", 4.4, 700, "#fff", font=LORA))
    o.append(t(xv1 + 12, c + 8.5, "betreuung", 4.4, 700, "#fff", font=LORA))
    for x, (_, _, _, mp), anc in zip([xe, xv1 - 20, xb1 - 8], STUFEN, ("middle", "middle", "end")):
        o.append(f'<circle cx="{x}" cy="{c + A_ + 6}" r="3" fill="{GELB}" stroke="{INK}" stroke-width=".5"/><circle cx="{x}" cy="{c + A_ + 6}" r="1" fill="{INK}"/>')
        o.append(t(x + (6 if anc == "end" else 0), c + A_ + 15, mp, 3.1, 700, anchor=anc))
    o.append(t(xe, c - A_ - 8, "DEIN VERTRIEB – WIR DOCKEN AN", 2.7, 700, GRAU, extra=' letter-spacing="0.4"'))
    o.append(t(xm, c - mund[3] - 3 * gap - 8, "UNSER SCHWERPUNKT: DIE BAUSTEINE", 2.7, 700, INK, extra=' letter-spacing="0.4"'))
    o.append(monat_band(m, 246, W - 2 * m, 28))
    o.append(t(m, H - 6, "Marketing as a Service · sofort sichtbar · Fundament: Strategie – wohin will deine Agentur, wen will sie gewinnen?", 2.9, 500, GRAU))
    return svg_rahmen(W, H, "".join(o), "Infografik Marketing as a Service, Explosionszeichnung")


ENTWUERFE = {"a": (entwurf_a, 420, 297), "b": (entwurf_b, 297, 420), "rollup": (lambda: entwurf_b(H=600, W=300), 1000, 2000),
             "c": (entwurf_c, 420, 297)}


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
        px = 1500 if k != "rollup" else 1200
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
