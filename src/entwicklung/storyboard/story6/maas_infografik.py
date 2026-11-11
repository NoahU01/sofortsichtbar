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
    lw = 30 if w >= 400 else 26          # wie ein Briefkopf-Logo: auf A3 rund 26–30 mm breit
    lh = lw * 40 / 78
    return (f'<image x="{w - 20 - lw}" y="11" width="{lw}" height="{lh:.1f}" href="data:image/svg+xml;base64,{daten}" '
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


# ---------------------------------------------------------------------------- A · Querformat: nur 02 – drei Stufen zum Vertriebserfolg
def entwurf_a():
    W, H, m = 420, 297, 18
    o = [kopf(m, 22, 11)]
    o.append(zeilen(250, 34, "Vertrieb läuft in drei Stufen. Wir optimieren die erste – damit aus regelmäßiger Wahrnehmung echte Anfragen werden, die direkt in deinen Vertrieb laufen.", 62, 3.7, 5.6))
    o.append(f'<rect x="{m}" y="72" width="{W - 2 * m}" height=".6" fill="{INK}"/>')
    o.append(t(m, 81, "MARKETING UND VERTRIEB", 2.9, 700, INK, extra=' letter-spacing="0.5"'))
    o.append(t(m, 90, "Drei Stufen zum Vertriebserfolg.", 7, 700, font=LORA))
    # Maschine waagerecht
    c, xm, xo, xe = 156, m + 4, 176, 196
    A_ = 21
    hals = [6, 11, 16, A_]
    mund = [20, 31, 42, 53]
    o.append(punkte_vor(m - 2, m + 3, c - 48, c + 48, 30, .9))
    for k in (3, 2, 1, 0):
        o.append(f'<path d="{trichter_pfad(xm, xo, xe, c, mund[k], hals[k], 76)}" fill="{FARBEN[k]}" stroke="#fff" stroke-width=".8"/>')
    for k in (3, 2, 1):
        nr, name, icon, vers, _ = BAUSTEINE[k]
        y = c - mund[k] + (mund[k] - mund[k - 1]) / 2 + 1.2
        o.append(ico(icon, xm + 4, y - 3.2, 4.4))
        o.append(t(xm + 10.5, y, f"Baustein {nr} · {name}", 3.3, 700))
        o.append(t(xm + 88, y, vers, 3.1, 400, TEXT2))
    nr, name, icon, vers, _ = BAUSTEINE[0]
    o.append(ico(icon, xm + 4, c - 12, 5))
    o.append(t(xm + 11, c - 8, "Baustein 1", 3.3, 700))
    o.append(t(xm + 4, c + 1.5, "Kernpaket sofort sichtbar", 5.4, 700))
    o.append(t(xm + 4, c + 8, vers, 3.3, 400))
    for i in range(3):
        o.append(f'<circle cx="{xo - 6 + i * 6}" cy="{c + (i - 1) * 2}" r="1.3" fill="{INK}"/>')
    # der eine Messpunkt: gestrichelte Linie vom Trichterausgang nach oben zum Text
    xl, yl = xo + 10, c - mund[3] - 4
    o.append(f'<path d="M{xl} {c - A_ - 1.5} V{yl}" stroke="{INK}" stroke-width=".45" stroke-dasharray="1.4 1.2"/>')
    o.append(t(xl + 3, yl - 3, "MESSPUNKT", 2.6, 700, GRAU, extra=' letter-spacing="0.5"'))
    o.append(t(xl + 3, yl + 2.6, "Leads: echte Anfragen", 4.2, 700))
    # Prozesspfeile
    xv0, xv1, xb1 = xe, 306, W - m
    o.append(f'<path d="M{xv0} {c - A_} H{xv1 - 8} L{xv1} {c} L{xv1 - 8} {c + A_} H{xv0} Z" fill="#fff" stroke="{INK}" stroke-width=".6" stroke-linejoin="round"/>')
    o.append(ico("handshake", xv0 + 9, c - 10, 9))
    o.append(t(xv0 + 21, c - 3.5, "Vertrieb", 6.4, 700, font=LORA))
    o.append(t(xv0 + 21, c + 5, "Terminierung  ›  Beratung  ›  Abschluss", 3.4, 500))
    o.append(f'<path d="M{xv1 + 2} {c - A_} H{xb1 - 4} Q{xb1} {c - A_} {xb1} {c - A_ + 4} V{c + A_ - 4} Q{xb1} {c + A_} {xb1 - 4} {c + A_} H{xv1 + 2} L{xv1 + 10} {c} Z" fill="{INK}"/>')
    o.append(ico("heart-handshake", xv1 + 17, c - 5, 10, GELB))
    o.append(t(xv1 + 31, c + 2.2, "Kundenbetreuung", 6.4, 700, "#fff", font=LORA))
    # Rückweg unter dem Fluss
    yr = c + 64
    o.append(f'<path d="M{xb1 - 40} {c + A_} V{yr} H{m + 30} V{c + mund[3] + 2}" fill="none" stroke="{INK}" stroke-width=".45" marker-end="url(#ig-pf)"/>')
    o.append(f'<rect x="{(m + xb1) / 2 - 56}" y="{yr - 4.4}" width="112" height="8.8" rx="4.4" fill="{GELB}"/>')
    o.append(t((m + xb1) / 2, yr + 1.3, RUECK, 3.3, 600, anchor="middle"))
    # Stufentexte
    ys = 238
    for (x0, bw), (name, claim, text, mp), nr in zip([(m, 150), (xv0, 100), (xv1 + 4, xb1 - xv1 - 4)], STUFEN, (1, 2, 3)):
        o.append(t(x0, ys, f"STUFE {nr} · {name.upper()}" + (" · UNSER SCHWERPUNKT" if nr == 1 else ""), 2.9, 700, INK if nr == 1 else GRAU, extra=' letter-spacing="0.5"'))
        o.append(t(x0, ys + 8.5, claim, 6.4, 700, font=LORA))
        o.append(zeilen(x0, ys + 15.5, text, int(bw / 1.75), 3.5, 5))
    o.append(t(m, H - 6, "Marketing as a Service · sofort sichtbar · ein festes Team, ein Ansprechpartner", 2.9, 500, GRAU))
    return svg_rahmen(W, H, "".join(o), "Infografik Marketing as a Service, Querformat: drei Stufen zum Vertriebserfolg")


# ---------------------------------------------------------------------------- A2 · Querformat: alle drei Sektionen nebeneinander
def entwurf_a2():
    W, H, m = 420, 297, 18
    o = [kopf(m, 22, 11)]
    o.append(zeilen(250, 34, "Erst klären wir, wo du wachsen willst. Dann bringt dein Marketing echte Anfragen in deinen Vertrieb. Und jeden Monat prüfen wir, ob es funktioniert.", 62, 3.7, 5.6))
    gap = 16
    w1, w3 = 86, 92
    w2 = W - 2 * m - w1 - w3 - 2 * gap
    x1, x2, x3 = m, m + w1 + gap, m + w1 + gap + w2 + gap
    y0 = 74

    def kopf_(x, w, nr, label, titel, sub=""):
        r = f'<rect x="{x}" y="{y0}" width="{w}" height=".6" fill="{INK}"/>'
        r += t(x, y0 + 12, nr, 10, 700, INK)
        r += t(x + 17, y0 + 6.5, label, 2.6, 700, INK, extra=' letter-spacing="0.5"')
        r += t(x + 17, y0 + 14, titel, 6, 700, font=LORA)
        if sub:
            r += zeilen(x + 17, y0 + 20, sub, int((w - 17) / 1.7), 3, 4.2)
        return r

    # 01 · Strategie: der Auswahlpfad senkrecht
    o.append(kopf_(x1, w1, "01", "STRATEGIE", "Wo willst du wachsen?", "Welche Ziele willst du erreichen – und mit welchen Zielgruppen?"))
    yy = y0 + 40
    for i, (kopf_name, werte) in enumerate(STRATEGIE):
        o.append(t(x1, yy, kopf_name.upper(), 2.6, 700, GRAU, extra=' letter-spacing="0.5"'))
        for j, w_ in enumerate(werte[:3]):
            py = yy + 3 + j * 8.5
            an = j == 0
            o.append(f'<rect x="{x1}" y="{py}" width="{w1}" height="6.8" rx="3.4" fill="{GELB if an else "#fff"}" stroke="{GELB if an else LINIE}" stroke-width=".45"/>')
            o.append(t(x1 + 4, py + 4.8, w_, 3.3, 600 if an else 400))
        yy += 3 + len(werte[:3]) * 8.5
        if i < 2:
            o.append(f'<path d="M{x1 + 8} {yy + 1} v4.5 m-1.6 -1.6 l1.6 1.6 l1.6 -1.6" fill="none" stroke="{INK}" stroke-width=".45" stroke-linecap="round" stroke-linejoin="round"/>')
            yy += 14
    o.append(zeilen(x1, yy + 6, "Daraus leiten wir alles Weitere ab: Themen, Landingpages, Kanäle.", int(w1 / 1.55), 3, 4.2, TEXT2))

    # 02 · Marketing und Vertrieb: Trichter senkrecht, Texte rechts
    o.append(kopf_(x2, w2, "02", "MARKETING UND VERTRIEB", "Drei Stufen zum Vertriebserfolg."))
    gw = 74
    cx = x2 + gw / 2 + 4
    A_ = 18
    mund, hals = [12, 19, 26, 33], [5, 9.5, 14, A_]
    yt0 = y0 + 34
    yk, yh = yt0 + 74, yt0 + 84
    o.append(punkte_vor(cx - 28, cx + 28, yt0 - 5, yt0 - 1.5, 24, .7))
    for k in (3, 2, 1, 0):
        hm, ha = mund[k], hals[k]
        d = (f"M{cx - hm} {yt0} C{cx - hm} {yt0 + 22} {cx - ha} {yk - 22} {cx - ha} {yk} V{yh} H{cx + ha} V{yk} "
             f"C{cx + ha} {yk - 22} {cx + hm} {yt0 + 22} {cx + hm} {yt0} Z")
        o.append(f'<path d="{d}" fill="{FARBEN[k]}" stroke="#fff" stroke-width=".6"/>')
    for k, nr in ((3, "4"), (2, "3"), (1, "2")):
        x = cx - (mund[k] + mund[k - 1]) / 2
        o.append(f'<circle cx="{x}" cy="{yt0 + 5.5}" r="2.3" fill="#fff" stroke="{INK}" stroke-width=".35"/>')
        o.append(t(x, yt0 + 6.5, nr, 2.7, 700, anchor="middle"))
    o.append(f'<circle cx="{cx}" cy="{yt0 + 5.5}" r="2.3" fill="{INK}"/>')
    o.append(t(cx, yt0 + 6.5, "1", 2.7, 700, GELB, "middle"))
    o.append(t(cx, yt0 + 13.5, "Kernpaket", 3.3, 700, anchor="middle"))
    for i in range(3):
        o.append(f'<circle cx="{cx + (i - 1) * 1.4}" cy="{yk - 3 + i * 3.4}" r="1" fill="{INK}"/>')
    yv1 = yh + 34
    o.append(f'<path d="M{cx - A_} {yh} H{cx + A_} V{yv1 - 6} L{cx} {yv1} L{cx - A_} {yv1 - 6} Z" fill="#fff" stroke="{INK}" stroke-width=".5" stroke-linejoin="round"/>')
    o.append(ico("handshake", cx - 3.2, yh + 3.5, 6.4))
    o.append(t(cx, yh + 15, "Vertrieb", 4.4, 700, anchor="middle", font=LORA))
    o.append(t(cx, yh + 20.5, "Termin · Beratung · Abschluss", 2.2, 500, anchor="middle"))
    yb0, yb1 = yv1 + 1.5, yv1 + 28
    o.append(f'<path d="M{cx - A_} {yb0} L{cx} {yb0 + 6} L{cx + A_} {yb0} V{yb1 - 3} Q{cx + A_} {yb1} {cx + A_ - 3} {yb1} H{cx - A_ + 3} Q{cx - A_} {yb1} {cx - A_} {yb1 - 3} Z" fill="{INK}"/>')
    o.append(ico("heart-handshake", cx - 3.2, yb0 + 8.5, 6.4, GELB))
    o.append(t(cx, yb0 + 21, "Kundenbetreuung", 3.1, 700, "#fff", "middle", font=LORA))
    o.append(f'<path d="M{cx - A_} {yb1 - 8} H{x2 + 1} V{yt0 - 8} H{cx - 35} V{yt0 - 1}" fill="none" stroke="{INK}" stroke-width=".4" marker-end="url(#ig-pf)"/>')
    tx = x2 + gw + 12
    n = int((x2 + w2 - tx) / 1.6)
    o.append(mess_linie(cx + A_ + 1.5, tx - 3, yh - 5, .85))
    ende = 0
    for (yy, i) in [(yt0 + 1, 0), (yh + 9, 1), (yb0 + 9, 2)]:
        yy = max(yy, ende + 9)
        name, claim, text, mp = STUFEN[i]
        o.append(t(tx, yy, f"STUFE {i + 1} · {name.upper()}", 2.6, 700, INK if i == 0 else GRAU, extra=' letter-spacing="0.5"'))
        o.append(t(tx, yy + 7.5, claim, 5.4, 700, font=LORA))
        o.append(zeilen(tx, yy + 13.5, text, n, 3.1, 4.4))
        ye = yy + 13.5 + (len(umbruch(text, n)) - 1) * 4.4
        if i == 0:
            for j, (nr, name_b, icon, vers, _) in enumerate(BAUSTEINE):
                by = ye + 6.5 + j * 6
                o.append(f'<circle cx="{tx + 2.3}" cy="{by}" r="2.3" fill="{INK if nr == "1" else "#fff"}" stroke="{INK}" stroke-width=".35"/>')
                o.append(t(tx + 2.3, by + 1, nr, 2.6, 700, GELB if nr == "1" else INK, "middle"))
                o.append(t(tx + 6.5, by + 1.1, name_b, 3.1, 700))
            ye += 6.5 + 3 * 6
        ende = ye
    yr = max(yb1, ende) + 9
    o.append(f'<rect x="{x2}" y="{yr - 3.8}" width="{w2}" height="7.6" rx="3.8" fill="{GELB}"/>')
    o.append(t(x2 + w2 / 2, yr + 1.1, "↑  " + RUECK, 3, 600, anchor="middle"))

    # 03 · Steuerung: Dashboard als Spalte
    o.append(kopf_(x3, w3, "03", "STEUERUNG", "Funktioniert es?", "Wo müssen wir nachsteuern? Jeden Monat im Report und im Betreuungscall."))
    dy = y0 + 40
    dh = 108
    o.append(f'<rect x="{x3}" y="{dy}" width="{w3}" height="{dh}" rx="3" fill="#fff" stroke="{INK}" stroke-width=".5"/>')
    o.append(f'<path d="M{x3} {dy + 6.5} H{x3 + w3}" stroke="{INK}" stroke-width=".3"/>')
    for i in range(3):
        o.append(f'<circle cx="{x3 + 4 + i * 3.2}" cy="{dy + 3.2}" r=".85" fill="{LINIE}"/>')
    o.append(t(x3 + 15, dy + 4.4, "Analytics-Dashboard", 2.7, 700))
    kw, kh = (w3 - 8 - 3) / 2, 20
    for i, (name, frage) in enumerate(STEUERUNG_KACHELN):
        kx = x3 + 4 + (i % 2) * (kw + 3)
        ky = dy + 10.5 + (i // 2) * (kh + 3)
        lead = name == "Leads"
        o.append(f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="1.8" fill="{GELB if lead else HELL}"/>')
        o.append(t(kx + 3, ky + 5.2, name, 3.1, 700))
        pts = " ".join(f"{kx + 3 + j * (kw - 6) / 6:.1f},{ky + kh - 2.5 - v:.1f}" for j, v in enumerate([.8, 2.5, 1.7, 3.8, 3, 4.8, 6.2]))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width=".45" stroke-linecap="round" stroke-linejoin="round"/>')
    ey = dy + 10.5 + 2 * (kh + 3) + 5
    o.append(t(x3 + 4, ey, "EMPFEHLUNGEN", 2.4, 700, GRAU, extra=' letter-spacing="0.5"'))
    for j, (bereich, was) in enumerate(STEUERUNG_EMPF):
        by = ey + 3 + j * 11.5
        o.append(f'<rect x="{x3 + 4}" y="{by}" width="{w3 - 8}" height="9.5" rx="1.6" fill="#fff" stroke="{LINIE}" stroke-width=".4"/>')
        o.append(t(x3 + 6.5, by + 4, bereich, 2.7, 700))
        o.append(t(x3 + 6.5, by + 7.8, was, 2.4, 400, TEXT2))
    o.append(zeilen(x3, dy + dh + 7, "Empfehlungen übernehmen wir und prüfen sie nach acht Wochen nach. Abschlüsse liegen im System deiner Agentur – die tracken wir bewusst nicht.", int(w3 / 1.5), 2.8, 4, TEXT2))
    o.append(t(m, H - 6, "Marketing as a Service · sofort sichtbar · ein festes Team, ein Ansprechpartner", 2.9, 500, GRAU))
    return svg_rahmen(W, H, "".join(o), "Infografik Marketing as a Service, Querformat mit drei Sektionen")


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
    blocks = [(yt0 + 2, 0), (yh + 12, 1), (yb0 + 12, 2)]
    o.append(mess_linie(cx + A_ + 2, tx - 3, yh - 6, s))   # der eine Messpunkt: Leads
    ende = 0
    for (yy, i) in blocks:
        yy = max(yy, ende + 10)
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
        ende = ye
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


def mess_linie(x0, x1, y, s=1.0, label="Leads: echte Anfragen", farbe=INK):
    """Der eine Messpunkt: gestrichelte Linie vom Trichterausgang bis zum Text, Text rechts davon (kein Punkt am Trichter)."""
    o = f'<path d="M{x0} {y} H{x1}" stroke="{farbe}" stroke-width="{.45 * s}" stroke-dasharray="{1.4 * s} {1.2 * s}"/>'
    o += t(x1 + 3 * s, y - 2.6 * s, "MESSPUNKT", 2.6 * s, 700, GRAU, extra=' letter-spacing="0.5"')
    o += t(x1 + 3 * s, y + 3.4 * s, label, 4.2 * s, 700)
    return o


def entwurf_rollup2(ss=False):
    """ss=True: Version 2.1 in den Farben von sofort sichtbar (Blau → Violett), hell; Inhalt und Schrift unverändert.
    Gewichtung: 01 und 03 kompakt, 02 bekommt den Raum; viel Luft zwischen den Sektionen."""
    W, H, m = 300, 600, 22
    if ss:
        FL, ST, AD, TST, LAGEN = "url(#ss-hell)", "url(#ss-voll)", "#b98cf0", "#fff", ["url(#ss-voll)", "#dcd3ec", "#e8e2f3", "#f3effa"]
    else:
        FL, ST, AD, TST, LAGEN = GELB, GELB, GELB, INK, FARBEN
    o = [kopf(m, 22, 16, marker=FL)]
    o.append(zeilen(m, 84, "Vertrieb läuft in drei Stufen. Wir optimieren die erste – damit aus regelmäßiger Wahrnehmung echte Anfragen werden, die direkt in deinen Vertrieb laufen.", 70, 4.3, 6.2))

    # 01 · Strategie – kompakt: Kopf und ein Auswahlpfad
    y = 108
    o.append(sektion_kompakt(m, W, y, "01", "STRATEGIE", "Wo willst du wachsen?", "Welche Ziele willst du erreichen – und mit welchen Zielgruppen?"))
    ys = y + 31
    sw = (W - 2 * m - 2 * 9) / 3
    for i, (kopf_, werte) in enumerate(STRATEGIE):
        x = m + i * (sw + 9)
        o.append(t(x, ys, kopf_.upper(), 2.7, 700, GRAU, extra=' letter-spacing="0.5"'))
        for j, w_ in enumerate(werte[:2]):
            yy = ys + 3 + j * 8.5
            an = j == 0
            o.append(f'<rect x="{x}" y="{yy}" width="{sw}" height="6.8" rx="3.4" fill="{FL if an else "#fff"}" stroke="{("#c9b6ec" if ss else GELB) if an else LINIE}" stroke-width=".45"/>')
            o.append(t(x + 4, yy + 4.8, w_, 3.3, 600 if an else 400, INK))
        if i < 2:
            xa = x + sw + 2
            o.append(f'<path d="M{xa} {ys + 6.4} l3.6 0 m-1.6 -1.6 l1.6 1.6 l-1.6 1.6" fill="none" stroke="{INK}" stroke-width=".45" stroke-linecap="round" stroke-linejoin="round"/>')

    # 02 · Marketing und Vertrieb – der Hauptteil
    y = 184
    o.append(sektion_kompakt(m, W, y, "02", "MARKETING UND VERTRIEB", "Drei Stufen zum Vertriebserfolg."))
    gx, gw = m, 118
    cx = gx + gw / 2
    A_ = 26
    mund = [18, 28, 38, 48]
    hals = [7, 13, 19, A_]
    yt0 = y + 36
    yk, yh = yt0 + 102, yt0 + 116
    o.append(punkte_vor(cx - 46, cx + 46, yt0 - 7, yt0 - 2, 30, .9))
    for k in (3, 2, 1, 0):
        hm, ha = mund[k], hals[k]
        d = (f"M{cx - hm} {yt0} C{cx - hm} {yt0 + 36} {cx - ha} {yk - 36} {cx - ha} {yk} V{yh} H{cx + ha} V{yk} "
             f"C{cx + ha} {yk - 36} {cx + hm} {yt0 + 36} {cx + hm} {yt0} Z")
        o.append(f'<path d="{d}" fill="{LAGEN[k]}" stroke="#fff" stroke-width=".8"/>')
    for k, nr in ((3, "4"), (2, "3"), (1, "2")):
        x = cx - (mund[k] + mund[k - 1]) / 2
        o.append(f'<circle cx="{x}" cy="{yt0 + 7}" r="3" fill="#fff" stroke="{INK}" stroke-width=".4"/>')
        o.append(t(x, yt0 + 8.2, nr, 3.4, 700, anchor="middle"))
    o.append(f'<circle cx="{cx}" cy="{yt0 + 7}" r="3" fill="{INK}"/>')
    o.append(t(cx, yt0 + 8.2, "1", 3.4, 700, AD if ss else GELB, "middle"))
    o.append(t(cx, yt0 + 18, "Kernpaket", 4.2, 700, TST, anchor="middle"))
    for i in range(3):
        o.append(f'<circle cx="{cx + (i - 1) * 2}" cy="{yk - 4 + i * 4.5}" r="1.3" fill="{TST}"/>')
    yv1 = yh + 50
    o.append(f'<path d="M{cx - A_} {yh} H{cx + A_} V{yv1 - 9} L{cx} {yv1} L{cx - A_} {yv1 - 9} Z" fill="#fff" stroke="{INK}" stroke-width=".6" stroke-linejoin="round"/>')
    o.append(ico("handshake", cx - 4.5, yh + 6, 9))
    o.append(t(cx, yh + 22, "Vertrieb", 6, 700, anchor="middle", font=LORA))
    for i, st in enumerate(["Terminierung", "Beratung", "Abschluss"]):
        o.append(t(cx, yh + 29 + i * 4.6, st, 3.4, 500, anchor="middle"))
    yb0, yb1 = yv1 + 2, yv1 + 40
    o.append(f'<path d="M{cx - A_} {yb0} L{cx} {yb0 + 9} L{cx + A_} {yb0} V{yb1 - 4} Q{cx + A_} {yb1} {cx + A_ - 4} {yb1} H{cx - A_ + 4} Q{cx - A_} {yb1} {cx - A_} {yb1 - 4} Z" fill="{INK}"/>')
    o.append(ico("heart-handshake", cx - 4.5, yb0 + 13, 9, AD))
    o.append(t(cx, yb0 + 30, "Kundenbetreuung", 5, 700, "#fff", "middle", font=LORA))
    o.append(f'<path d="M{cx - A_} {yb1 - 12} H{gx + 2} V{yt0 - 10} H{cx - 50} V{yt0 - 1}" fill="none" stroke="{INK}" stroke-width=".45" marker-end="url(#ig-pf)"/>')
    tx = gx + gw + 14
    n = int((W - m - tx) / 1.85)
    # der eine Messpunkt: gestrichelte Linie vom Trichterausgang zum Text
    ym_ = yh - 7
    o.append(mess_linie(cx + A_ + 2, tx - 3, ym_))
    ende = 0
    for (yy, i) in [(yt0 + 2, 0), (yh + 12, 1), (yb0 + 12, 2)]:
        yy = max(yy, ende + 12)
        name, claim, text, mp = STUFEN[i]
        o.append(t(tx, yy, f"STUFE {i + 1} · {name.upper()}", 3, 700, INK if i == 0 else GRAU, extra=' letter-spacing="0.5"'))
        o.append(t(tx, yy + 9, claim, 6.4, 700, font=LORA))
        o.append(zeilen(tx, yy + 16, text, n, 3.6, 5.2))
        ye = yy + 16 + len(umbruch(text, n)) * 5.2
        if i == 0:
            for j, (nr, name_b, icon, vers, _) in enumerate(BAUSTEINE):
                by = ye + 5 + j * 7.5
                o.append(f'<circle cx="{tx + 2.8}" cy="{by}" r="2.8" fill="{INK if nr == "1" else "#fff"}" stroke="{INK}" stroke-width=".4"/>')
                o.append(t(tx + 2.8, by + 1.15, nr, 3.1, 700, AD if nr == "1" else INK, "middle"))
                o.append(ico(icon, tx + 8, by - 2.4, 4.8))
                o.append(t(tx + 15, by + 1.3, name_b, 3.6, 700))
            ye += 5 + 4 * 7.5
        ende = ye
    yr = yb1 + 12
    o.append(f'<rect x="{m}" y="{yr - 5}" width="{W - 2 * m}" height="10" rx="5" fill="{ST}"/>')
    o.append(t(W / 2, yr + 1.4, "↑  " + RUECK, 3.7, 600, TST, anchor="middle"))

    # 03 · Steuerung – kompakt: vier Kacheln in einer Reihe, Empfehlungen als eine Reihe
    y = yr + 30
    o.append(sektion_kompakt(m, W, y, "03", "STEUERUNG", "Funktioniert es?", "Wo müssen wir nachsteuern? Jeden Monat im Report und im Betreuungscall."))
    dx, dy, dw = m, y + 29, W - 2 * m
    dh = 58
    o.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="3.5" fill="#fff" stroke="{INK}" stroke-width=".55"/>')
    o.append(f'<path d="M{dx} {dy + 7} H{dx + dw}" stroke="{INK}" stroke-width=".35"/>')
    for i in range(3):
        o.append(f'<circle cx="{dx + 4.5 + i * 3.5}" cy="{dy + 3.5}" r=".95" fill="{LINIE}"/>')
    o.append(t(dx + 17, dy + 4.7, "Analytics-Dashboard", 2.9, 700))
    kw, kh = (dw - 8 - 3 * 3) / 4, 20
    for i, (name, frage) in enumerate(STEUERUNG_KACHELN):
        kx, ky = dx + 4 + i * (kw + 3), dy + 11
        lead = name == "Leads"
        o.append(f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="2" fill="{FL if lead else HELL}"/>')
        o.append(t(kx + 3, ky + 5.4, name, 3.2, 700))
        pts = " ".join(f"{kx + 3 + j * (kw - 6) / 6:.1f},{ky + kh - 2.5 - v:.1f}" for j, v in enumerate([.8, 2.5, 1.7, 3.8, 3, 4.8, 6.2]))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width=".5" stroke-linecap="round" stroke-linejoin="round"/>')
    ey = dy + 36
    o.append(t(dx + 4, ey, "EMPFEHLUNGEN", 2.5, 700, GRAU, extra=' letter-spacing="0.5"'))
    ew = (dw - 8 - 2 * 3) / 3
    for j, (bereich, was) in enumerate(STEUERUNG_EMPF):
        ex = dx + 4 + j * (ew + 3)
        o.append(f'<rect x="{ex}" y="{ey + 2.5}" width="{ew}" height="11.5" rx="1.8" fill="#fff" stroke="{LINIE}" stroke-width=".4"/>')
        o.append(t(ex + 2.6, ey + 7, bereich, 2.8, 700))
        o.append(t(ex + 2.6, ey + 11.4, was, 2.4, 400, TEXT2))
    o.append(t(m, dy + dh + 7, "Empfehlungen übernehmen wir und prüfen sie nach acht Wochen nach. Abschlüsse liegen im System deiner Agentur – die tracken wir bewusst nicht.", 2.9, 500, TEXT2))
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
    """Version 3: Blick in die Maschine. Hauptpunkt: das Ökosystem aus Baustein 1 (Kanäle mit sauberen Profilen und gefülltem
    Content-Kalender, Bestandskunden-Mailings → Zielgruppen → Landingpages; Add-on Termine vor- und nachbereiten).
    Dann LinkedIn als Prozesspfeile (wir/du), Bausteine 3 und 4 klein, Nutzen."""
    W, H, m = 300, 600, 22
    o = [t(m, 22, "MARKETING AS A SERVICE · SOFORT SICHTBAR", 4.8, 700, INK, extra=' letter-spacing="0.8"')]
    o.append(t(m, 42, "Ein Blick in", 16, 700, font=LORA))
    o.append(f'<rect x="{m - 1.3}" y="47" width="112" height="19" rx="2" fill="{GELB}"/>')
    o.append(t(m, 61.5, "die Maschine.", 16, 700, font=LORA))
    o.append(zeilen(m, 80, "So läuft dein Vertrieb mit Baustein 1 und 2 – Woche für Woche. Paid Ads verstärken, die Website schließt die Lücke.", 70, 4.3, 6.2))

    # 1 · Das Ökosystem (Hauptpunkt)
    y = 98
    o.append(sektion(m, W, y, "1", "BAUSTEIN 1 · KERNPAKET", "Ein Ökosystem, das für dich läuft.",
                     "Saubere Profile, ein gefüllter Content-Kalender und Mailings an deinen Bestand – alles auf deine Zielgruppen ausgerichtet."))
    cw, gap = (W - 2 * m - 3 * 5) / 4, 5
    # Content-Kalender über den drei Kanälen
    ky = y + 44
    kb = 3 * cw + 2 * gap
    o.append(t(m, ky, "CONTENT-KALENDER · GEFÜLLT", 2.9, 700, GRAU, extra=' letter-spacing="0.5"'))
    for i in range(14):
        zx = m + i * (kb / 14)
        o.append(f'<rect x="{zx:.1f}" y="{ky + 2.5}" width="{kb / 14 - 1.2:.1f}" height="5" rx="1" fill="{INK if i % 3 == 0 else (GELB if i % 3 == 1 else LINIE)}"/>')
    # Kanäle
    kanaele = [("in", "LinkedIn"), ("f", "Facebook"), ("ig", "Instagram")]
    cy = ky + 13
    ch = 48
    for i in range(4):
        x = m + i * (cw + gap)
        mail = i == 3
        o.append(f'<rect x="{x}" y="{cy}" width="{cw}" height="{ch}" rx="3" fill="{INK if mail else "#fff"}" stroke="{INK}" stroke-width=".6"/>')
        if mail:
            o.append(ico("mail", x + 5, cy + 4.5, 8, GELB))
            o.append(t(x + 5, cy + 18, "BESTANDSKUNDEN", 2.6, 700, GELB, extra=' letter-spacing="0.4"'))
            o.append(t(x + 5, cy + 24, "Mailings", 4.4, 700, "#fff", font=LORA))
            pkt = ["per E-Mail", "gern auch per Post"]
        else:
            kurz, name = kanaele[i]
            o.append(f'<rect x="{x + 5}" y="{cy + 4.5}" width="8" height="8" rx="2" fill="{INK}"/>')
            o.append(t(x + 9, cy + 10, kurz, 3.6, 700, "#fff", "middle"))
            o.append(t(x + 5, cy + 24, name, 4.4, 700, font=LORA))
            pkt = ["Profil sauber", "Postings laufen"]
        for j, p_ in enumerate(pkt):
            yy = cy + 34 + j * 5.6
            o.append(f'<path d="M{x + 5} {yy - 1.5} l1.4 1.4 l2.8 -2.8" fill="none" stroke="{GELB if mail else INK}" stroke-width=".55" stroke-linecap="round" stroke-linejoin="round"/>')
            o.append(t(x + 10.5, yy, p_, 3.3, 500, "#fff" if mail else INK))
        # Pfeil nach unten zu den Zielgruppen
        o.append(f'<path d="M{x + cw / 2} {cy + ch + 1} V{cy + ch + 9}" fill="none" stroke="{INK}" stroke-width=".5" marker-end="url(#ig-pf)"/>')
    # Zielgruppen-Band
    zy = cy + ch + 13
    o.append(f'<rect x="{m}" y="{zy}" width="{W - 2 * m}" height="13" rx="6.5" fill="{HELL}"/>')
    o.append(t(m + 6, zy + 8.4, "DEINE ZIELGRUPPEN", 2.9, 700, GRAU, extra=' letter-spacing="0.5"'))
    for j, z in enumerate(["Junge Familien", "Ärzte und Zahnärzte", "Private Bauherren"]):
        o.append(t(m + 62 + j * 62, zy + 8.6, z, 3.8, 700))
    # Landingpages je Zielgruppe + Add-on
    ly = zy + 22
    lw = 52
    for j, z in enumerate(["Junge Familien", "Ärzte", "Bauherren"]):
        x = m + j * (lw + 5)
        o.append(f'<path d="M{m + 62 + j * 62 + 8} {zy + 13.5} V{ly - 1.5}" fill="none" stroke="{INK}" stroke-width=".45" marker-end="url(#ig-pf)"/>' if False else "")
        o.append(f'<rect x="{x}" y="{ly}" width="{lw}" height="58" rx="3" fill="#fff" stroke="{INK}" stroke-width=".6"/>')
        o.append(f'<rect x="{x + 3}" y="{ly + 3}" width="{lw - 6}" height="14" rx="1.6" fill="{GELB}"/>')
        o.append(t(x + 5.5, ly + 8, "LANDINGPAGE", 2.2, 700, INK, extra=' letter-spacing="0.3"'))
        o.append(t(x + 5.5, ly + 13.8, z, 3.9, 700, font=LORA))
        for k, (icon, txt) in enumerate([("clipboard-list", "Checkliste"), ("mic-vocal", "Podcast"), ("calendar", "Termin buchen")]):
            yy = ly + 23 + k * 10.5
            o.append(ico(icon, x + 4, yy, 4.6))
            o.append(t(x + 10.5, yy + 3.6, txt, 3.2, 500))
    o.append(t(m, ly + 67, "Wer dich sieht oder dein Mailing bekommt, findet hier mehr – und meldet sich direkt bei dir.", 3.5, 600))
    # Add-on
    ax = m + 3 * (lw + 5) + 2
    aw = W - m - ax
    o.append(f'<rect x="{ax}" y="{ly}" width="{aw}" height="58" rx="3" fill="#fff" stroke="{INK}" stroke-width=".6" stroke-dasharray="2 1.6"/>')
    o.append(t(ax + 5, ly + 7, "ADD-ON IM ALLTAG", 2.8, 700, GRAU, extra=' letter-spacing="0.5"'))
    o.append(t(ax + 5, ly + 15, "Termine vor- und", 4.6, 700, font=LORA))
    o.append(t(ax + 5, ly + 20.5, "nachbereiten", 4.6, 700, font=LORA))
    o.append(zeilen(ax + 5, ly + 30, "Vorher den Link zur Einstimmung, nachher zum Thema aus dem Gespräch.", 34, 3.2, 4.4))

    # 2 · LinkedIn als Prozesspfeile
    y = ly + 80
    o.append(sektion(m, W, y, "2", "BAUSTEIN 2 · LINKEDIN POWER PACKAGE", "LinkedIn als aktiver Vertriebskanal.",
                     "Mit dem Sales Navigator wissen wir, wen du gewinnen willst – und wann der richtige Moment für ein Gespräch ist."))
    py, ph = y + 40, 30
    sw = (W - 2 * m) / 6
    for i, (icon, titel, wer) in enumerate(LINKEDIN_WEG):
        x0 = m + i * sw
        spitze, kerbe = (5 if i < 5 else 0), (5 if i > 0 else 0)
        dunkel = wer == "du"
        fill = INK if dunkel else (GELB if wer == "gemeinsam" else HELL)
        d = f"M{x0} {py} H{x0 + sw - spitze + (1.2 if i < 5 else 0)} L{x0 + sw + (1.2 if i < 5 else 0)} {py + ph / 2} L{x0 + sw - spitze + (1.2 if i < 5 else 0)} {py + ph} H{x0} L{x0 + kerbe} {py + ph / 2} Z"
        o.append(f'<path d="{d}" fill="{fill}"/>')
        tc = "#fff" if dunkel else INK
        o.append(t(x0 + kerbe + 3.5, py + 7, str(i + 1), 3, 700, GELB if dunkel else GRAU))
        for k, z in enumerate(umbruch(titel, 12)):
            o.append(t(x0 + kerbe + 3.5, py + 13.5 + k * 4.4, z, 3.5, 700, tc))
    lg = py + ph + 7
    for j, (fill, txt) in enumerate([(GELB, "gemeinsam"), (HELL, "wir"), (INK, "du")]):
        x = m + j * 32
        o.append(f'<rect x="{x}" y="{lg - 3}" width="5" height="3.6" rx="1" fill="{fill}" stroke="{INK if fill == HELL else "none"}" stroke-width=".3"/>')
        o.append(t(x + 7, lg, txt, 3.2, 600))
    o.append(zeilen(m, lg + 9, "Wir werten regelmäßig aus, wer von deinen Fokus-Kunden etwas gepostet hat, und liefern dir den Link mit einem Antwortvorschlag. Den Kommentar schreibst du selbst – du entscheidest über Ton und Zungenschlag. Nach dem dritten Kommentar folgt die Einladung zum Gespräch.", 68, 3.6, 5.1))

    # 3 · Bausteine 3 und 4 – klein
    y = lg + 38
    o.append(f'<rect x="{m}" y="{y}" width="{W - 2 * m}" height=".6" fill="{INK}"/>')
    o.append(t(m, y + 7, "BAUSTEIN 3 UND 4 · VERSTÄRKEN UND ABRUNDEN", 2.9, 700, INK, extra=' letter-spacing="0.5"'))
    kw = (W - 2 * m - 8) / 2
    for i, (icon, titel, text) in enumerate([("trending-up", "Paid Ads: mehr Tempo.", "Mehr Menschen aus denselben Zielgruppen sehen dich."),
                                             ("app-window", "Website: die Lücke schließen.", "Deine Agentur, ordentlich dargestellt und auffindbar.")]):
        x = m + i * (kw + 8)
        o.append(ico(icon, x, y + 11, 7))
        o.append(t(x + 10, y + 16, titel, 4.4, 700, font=LORA))
        o.append(t(x + 10, y + 21.5, text, 3.2, 400, TEXT2))

    # Nutzen
    y = y + 36
    o.append(f'<rect x="{m}" y="{y}" width="{W - 2 * m}" height="52" rx="5" fill="{INK}"/>')
    o.append(t(m + 8, y + 10, "WAS DU DAVON HAST", 3, 700, GELB, extra=' letter-spacing="0.6"'))
    o.append(t(m + 8, y + 21, "Mehr Gespräche mit den Richtigen.", 7.2, 700, "#fff", font=LORA))
    for j, z in enumerate(["Deine Kanäle laufen – ohne dass du dir Gedanken machen musst.",
                           "Du weißt, wen du gewinnen willst – und wann du ihn ansprichst.",
                           "Du führst die Gespräche. Den Rest übernimmt die Maschine."]):
        yy = y + 30 + j * 7
        o.append(f'<path d="M{m + 8} {yy - 1.6} l1.6 1.6 l3.2 -3.2" fill="none" stroke="{GELB}" stroke-width=".6" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(t(m + 15, yy, z, 3.6, 500, "#fff"))
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
    o.append(mess_linie(cx + A_ + 2, tx - 3, ym_ - 2, .95))
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


# ---- Überblick für das Angebots-PDF (A4 hoch, Seite 2): die drei Sektionen aus Roll-up V2, nur die Funktionsweise ----
# gezeichnet im Maß der PDF-Seite: 174 mm breit (A4 minus 2 × 18 mm Rand); Schrift: Poppins 3,0 mm Text, 2,3 mm Kicker, Lora 4,4 mm Titel
def ueberblick_pdf(ss=False):
    W, m = 174, 0
    o = []

    def kopf_(y, nr, label, titel, sub=""):
        r = f'<rect x="0" y="{y}" width="{W}" height=".5" fill="{INK}"/>'
        r += t(0, y + 10, nr, 8, 700, INK)
        r += t(14, y + 5.2, label, 2.3, 700, INK, extra=' letter-spacing="0.4"')
        r += t(14, y + 11, titel, 4.4, 700, font=LORA)
        if sub:
            r += t(14, y + 15.6, sub, 2.9, 400, TEXT2)
        return r

    # 01 · Strategie
    o.append(kopf_(0, "01", "STRATEGIE", "Wo willst du wachsen?", "Welche Ziele willst du erreichen – und mit welchen Zielgruppen? Daraus leiten wir alles ab."))
    ys, sw = 24, (W - 2 * 7) / 3
    for i, (kopf_name, werte) in enumerate(STRATEGIE):
        x = i * (sw + 7)
        o.append(t(x, ys, kopf_name.upper(), 2.2, 700, GRAU, extra=' letter-spacing="0.4"'))
        for j, w_ in enumerate(werte[:2]):
            yy = ys + 2.5 + j * 7
            an = j == 0
            o.append(f'<rect x="{x}" y="{yy}" width="{sw}" height="5.6" rx="2.8" fill="{GELB if an else "#fff"}" stroke="{GELB if an else LINIE}" stroke-width=".4"/>')
            o.append(t(x + 3, yy + 3.9, w_, 2.8, 600 if an else 400))
        if i < 2:
            xa = x + sw + 1.6
            o.append(f'<path d="M{xa} {ys + 5.3} l3 0 m-1.4 -1.4 l1.4 1.4 l-1.4 1.4" fill="none" stroke="{INK}" stroke-width=".4" stroke-linecap="round" stroke-linejoin="round"/>')

    # 02 · Marketing und Vertrieb – Trichter, ein Messpunkt, drei Stufen
    y = 42
    o.append(kopf_(y, "02", "MARKETING UND VERTRIEB", "Drei Stufen zum Vertriebserfolg."))
    gw = 64
    cx = gw / 2 + 2
    A_ = 13.5
    mund, hals = [9, 14, 19.5, 25], [4, 7, 10.5, A_]
    yt0 = y + 23
    yk, yh = yt0 + 28, yt0 + 34
    o.append(punkte_vor(cx - 24, cx + 24, yt0 - 4, yt0 - 1, 20, .6))
    for k in (3, 2, 1, 0):
        hm, ha = mund[k], hals[k]
        d = (f"M{cx - hm} {yt0} C{cx - hm} {yt0 + 12} {cx - ha} {yk - 12} {cx - ha} {yk} V{yh} H{cx + ha} V{yk} "
             f"C{cx + ha} {yk - 12} {cx + hm} {yt0 + 12} {cx + hm} {yt0} Z")
        o.append(f'<path d="{d}" fill="{FARBEN[k]}" stroke="#fff" stroke-width=".5"/>')
    o.append(t(cx, yt0 + 6.5, "Marketing", 2.6, 700, anchor="middle"))
    for i in range(3):
        o.append(f'<circle cx="{cx + (i - 1) * 1.1}" cy="{yk - 7 + i * 2.6}" r=".75" fill="{INK}"/>')
    ym_ = yh - 2
    o.append(f'<circle cx="{cx + A_ + 5.5}" cy="{ym_}" r="3" fill="{GELB}" stroke="{INK}" stroke-width=".4"/><circle cx="{cx + A_ + 5.5}" cy="{ym_}" r="1.05" fill="{INK}"/>')
    o.append(f'<path d="M{cx + A_} {ym_} H{cx + A_ + 2.5}" stroke="{INK}" stroke-width=".4"/>')
    yv1 = yh + 23
    o.append(f'<path d="M{cx - A_} {yh} H{cx + A_} V{yv1 - 5} L{cx} {yv1} L{cx - A_} {yv1 - 5} Z" fill="#fff" stroke="{INK}" stroke-width=".45" stroke-linejoin="round"/>')
    o.append(ico("handshake", cx - 2.6, yh + 2.6, 5.2))
    o.append(t(cx, yh + 12, "Vertrieb", 3.4, 700, anchor="middle", font=LORA))
    yb0, yb1 = yv1 + 1.2, yv1 + 17
    o.append(f'<path d="M{cx - A_} {yb0} L{cx} {yb0 + 5} L{cx + A_} {yb0} V{yb1 - 2.5} Q{cx + A_} {yb1} {cx + A_ - 2.5} {yb1} H{cx - A_ + 2.5} Q{cx - A_} {yb1} {cx - A_} {yb1 - 2.5} Z" fill="{INK}"/>')
    o.append(ico("heart-handshake", cx - 2.6, yb0 + 5.4, 5.2, GELB))
    o.append(t(cx, yb0 + 13.6, "Kundenbetreuung", 2.6, 700, "#fff", "middle", font=LORA))
    o.append(f'<path d="M{cx - A_} {yb1 - 6} H1 V{yt0 - 6} H{cx - 27} V{yt0 - .8}" fill="none" stroke="{INK}" stroke-width=".35" marker-end="url(#ig-pf)"/>')
    tx = gw + 12
    n = 58   # Zeichen je Zeile bei 2,9 mm Poppins (Umbrüche geprüft: keine Einzelwörter)
    stufen = [(yt0 + 1, 1, "MARKETING · UNSER SCHWERPUNKT", INK), (yh + 9, 2, "VERTRIEB", GRAU), (yb0 + 6, 3, "KUNDENBETREUUNG", GRAU)]
    ende = 0
    for yy, nr, name, farbe in stufen:
        claim, text = STUFEN_KURZ[nr - 1]
        o.append(t(tx, yy, f"STUFE {nr} · {name}", 2.2, 700, farbe, extra=' letter-spacing="0.4"'))
        o.append(t(tx, yy + 5.6, claim, 4.4, 700, font=LORA))
        o.append(zeilen(tx, yy + 10.4, text, n, 2.9, 4.1))
        ende = yy + 10.4 + (len(umbruch(text, n)) - 1) * 4.1
    o.append(t(tx, ym_ - 1, "MESSPUNKT", 2.2, 700, GRAU, extra=' letter-spacing="0.4"'))
    o.append(t(tx, ym_ + 3.4, "Leads: echte Anfragen", 3.2, 700))
    yr = max(yb1, ende + 1) + 6
    o.append(f'<rect x="0" y="{yr - 3.4}" width="{W}" height="6.8" rx="3.4" fill="{GELB}"/>')
    o.append(t(W / 2, yr + 1, "↑  " + RUECK, 2.8, 600, anchor="middle"))

    # 03 · Steuerung – Dashboard als eine Reihe
    y = yr + 7.5
    o.append(kopf_(y, "03", "STEUERUNG", "Funktioniert es?", "Wo müssen wir nachsteuern? Jeden Monat im Report und im Betreuungscall."))
    dx, dy, dw, dh = 0, y + 20.5, W, 22
    o.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="2.6" fill="#fff" stroke="{INK}" stroke-width=".45"/>')
    o.append(f'<path d="M{dx} {dy + 5.6} H{dx + dw}" stroke="{INK}" stroke-width=".3"/>')
    for i in range(3):
        o.append(f'<circle cx="{dx + 3.6 + i * 2.8}" cy="{dy + 2.8}" r=".75" fill="{LINIE}"/>')
    o.append(t(dx + 13, dy + 3.8, "Analytics-Dashboard", 2.3, 700))
    kw, kh = (dw - 6 - 3 * 2.5) / 4, 13
    for i, (name, frage) in enumerate(STEUERUNG_KACHELN):
        kx, ky = dx + 3 + i * (kw + 2.5), dy + 8
        lead = name == "Leads"
        o.append(f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="1.6" fill="{GELB if lead else HELL}"/>')
        o.append(t(kx + 2.5, ky + 4.6, name, 2.8, 700))
        pts = " ".join(f"{kx + 2.5 + j * (kw - 5) / 6:.1f},{ky + kh - 2 - v:.1f}" for j, v in enumerate([0.5, 1.8, 1.2, 2.8, 2.1, 3.6, 4.8]))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width=".4" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(t(0, dy + dh + 5.6, "Daraus Empfehlungen für Landingpages, LinkedIn und Suche – übernommen und nach acht Wochen nachgeprüft.", 2.9, 400, TEXT2))
    H = dy + dh + 7
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1 {W} {H + 1}" width="{W}mm" height="{H + 1}mm" role="img" '
           f'aria-label="Marketing as a Service im Überblick: Strategie, Marketing und Vertrieb, Steuerung">{pfeilkopf()}{"".join(o)}</svg>')
    if ss:
        from maas_strukturbild import ss_faerben
        svg = ss_faerben(svg)
    return svg


ENTWUERFE = {"a": (entwurf_a, 420, 297), "a2": (entwurf_a2, 420, 297), "b": (entwurf_b, 297, 420), "b2": (entwurf_b2, 297, 420),
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
