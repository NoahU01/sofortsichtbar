"""Detailstufe zur Grundstory: was in Marketing und Vertrieb passiert (Daniel, 12.11.2026, Vorlage: Ablaufbild Marketing/Vertrieb).

Zweite Seite nach der Grundstory kompakt – als würde man in die drei Phasen hineinzoomen.
Gezeichnet als SVG in Millimetern (1 Einheit = 1 mm), Breite 380 mm (A3 quer abzüglich Rand).
Schrift: Inter (Text 2,4 mm ≈ 6,8 pt, Titel 3 mm SemiBold), Inter Tight nur für die Phasen-Überschriften.
Farben wie die Website: Tinte, Grau, Flächen #f5f5f7; Verlauf nur am Ziel: Beratungstermin (Daniel: Beratungstermine sind das oberste Ziel).
"""
import html

e = html.escape
INK, GRAU, LINIE, FLAECHE = "#1d1d1f", "#6e6e73", "#c7c7cc", "#f5f5f7"
B = 380  # Breite
T = 2.4  # Textgröße in mm


def umbruch(s, breite, groesse=T):
    """Zeilenumbruch nach geschätzter Zeichenbreite (Inter ≈ 0,53 × Größe)"""
    n = max(4, int((breite - 3.2) / (0.53 * groesse)))
    w, z = s.split(), [""]
    for x in w:
        if len(z[-1]) + len(x) + (1 if z[-1] else 0) > n and z[-1]:
            z.append(x)
        else:
            z[-1] = (z[-1] + " " + x).strip()
    return z


def text(x, y, s, groesse=T, gewicht=400, farbe=INK, anker="start", familie="Inter"):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{familie}" font-size="{groesse}" font-weight="{gewicht}" '
            f'fill="{farbe}" text-anchor="{anker}">{e(s)}</text>')


def zeilen(x, y_mitte, zs, groesse=T, gewicht=400, farbe=INK, anker="middle", lh=1.32):
    h = groesse * lh
    y0 = y_mitte - (len(zs) - 1) * h / 2 + groesse * 0.36
    return "".join(text(x, y0 + i * h, z, groesse, gewicht, farbe, anker) for i, z in enumerate(zs))


def kasten(x, y, w, h, s, art="hell", groesse=T, gewicht=400):
    """Kasten mit Mitte (x, y): hell (Fläche), weiß (auf Fläche), frage (Rand Tinte), dunkel, kern (Verlauf)"""
    fill, stroke, sw, farbe = {"hell": (FLAECHE, "none", 0, INK), "weiss": ("#fff", LINIE, .3, INK),
                               "frage": ("#fff", INK, .45, INK), "dunkel": (INK, "none", 0, "#fff"),
                               "kern": ("url(#ad-v)", "none", 0, "#fff"), "leer": ("#fff", GRAU, .3, GRAU)}[art]
    r = 2.6 if art == "frage" else 1.6
    out = f'<rect x="{x - w / 2:.2f}" y="{y - h / 2:.2f}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    return out + zeilen(x, y, umbruch(s, w, groesse), groesse, gewicht, farbe)


def linie(pts, gestrichelt=False, pfeil=True, farbe=INK, sw=.35):
    d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    strich = ' stroke-dasharray="1.2 1.2"' if gestrichelt else ""
    spitze = ' marker-end="url(#ad-p)"' if pfeil else ""
    return f'<path d="{d}" fill="none" stroke="{farbe}" stroke-width="{sw}" stroke-linejoin="round"{strich}{spitze}/>'


def svg():
    o = []
    H = 198
    P0, P1 = 30, 178   # Flächen der Vertriebsspalten (oben, unten)
    # Phasen-Überschriften (wie im Erklärbild der Website)
    MX1, MX2 = 0, 176          # Marketing
    VX1, VX2 = 184, B          # Vertrieb
    o.append(text(MX1, 5, "Marketing – wir gewinnen Interessenten", 3.6, 700, INK, familie="Inter Tight"))
    o.append(f'<rect x="{MX1}" y="8" width="{MX2 - MX1}" height=".6" fill="{INK}"/>')
    o.append(text(VX1, 5, "Vertrieb – du machst daraus Kunden", 3.6, 700, INK, familie="Inter Tight"))
    o.append(f'<rect x="{VX1}" y="8" width="{VX2 - VX1}" height=".6" fill="{INK}"/>')

    # Vertriebsspalten als Flächen
    sp = [("Qualifizierung und Terminierung", 184, 110), ("Beratung", 298, 25.3), ("Abschluss", 326.3, 25.3), ("Kundenbetreuung", 354.6, 25.4)]
    for name, x, w in sp:
        o.append(f'<rect x="{x}" y="{P0}" width="{w}" height="{P1 - P0}" rx="2.6" fill="{FLAECHE}"/>')
        o.append(zeilen(x + w / 2, P0 + 7, umbruch(name, w + 2, 2.7), 2.7, 600, INK))
    o.append(zeilen(184 + 55, P0 + 16, umbruch("Klärung, ob die Voraussetzungen für einen zeitnahen Abschluss vorliegen (Checkliste) und ein direktes weiteres vertriebliches Vorgehen zielführend ist.", 100, 2.2), 2.2, 400, GRAU))

    # Spalten Marketing (wie in der Vorlage untereinander): Kanal · Profil · Netzwerk/Inhalte/Kern · Wege der Landingpage · Messpunkt · Ansprache
    KX = 0
    C1, C2, C3, C4 = 36, 70, 105, 150
    W1, W2, W3, W4 = 26, 30, 26, 30
    MP = 130
    def kanal(y, name):
        return zeilen(KX, y, umbruch(name, 24, 2.8), 2.8, 600, INK, anker="start")
    SW = .35   # eine Strichstärke für alle Verbindungen; nichts doppelt zeichnen (überlagerte Linien wirken dicker)
    def gerade(x1, y1, x2, y2, pfeil=True):
        return linie([(x1, y1), (x2 - (.6 if pfeil and x2 > x1 else 0), y2)], pfeil=pfeil, sw=SW)
    def baum(quelle, ziele, knick):
        """eine Quelle (x, y) verzweigt bei knick senkrecht auf mehrere Ziele (x_links, y) – Stamm und Steg je einmal"""
        xq, yq = quelle
        ys = [y for _, y in ziele] + [yq]
        s = gerade(xq, yq, knick, yq, pfeil=False) + linie([(knick, min(ys)), (knick, max(ys))], pfeil=False, sw=SW)
        return s + "".join(gerade(knick, y, x, y) for x, y in ziele)
    def sammler(quellen, bus, ziel):
        """mehrere Quellen (x_rechts, y) laufen auf eine senkrechte Sammellinie bei bus und weiter zum Ziel (x_links, y)"""
        xz, yz = ziel
        ys = [y for _, y in quellen] + [yz]
        s = "".join(gerade(x, y, bus, y, pfeil=False) for x, y in quellen if y != yz)
        s += linie([(bus, min(ys)), (bus, max(ys))], pfeil=False, sw=SW)
        quelle_gerade = [q for q in quellen if q[1] == yz]
        start = quelle_gerade[0][0] if quelle_gerade else bus
        return s + gerade(start, yz, xz, yz)
    def gestrichelt(pts, pfeil=True):
        return linie(pts, gestrichelt=True, pfeil=pfeil, farbe=GRAU, sw=SW)

    # Messpunkt: Personen und Kontaktwege sind bekannt – hervorgehoben (Verlauf, kräftigere Linie)
    o.append(f'<path d="M{MP} 25 V{P1}" fill="none" stroke="url(#ad-vh)" stroke-width=".7" stroke-dasharray="1.6 1.2"/>')
    o.append(f'<text x="{MP}" y="17.4" font-family="Inter" font-size="2.9" font-weight="700" fill="url(#ad-vt)" text-anchor="middle">Messpunkt: Leads</text>')
    o.append(zeilen(MP, 21.6, ["Person und Kontaktweg bekannt"], 2.1, 400, GRAU))

    # LinkedIn – zwei Stränge: Netzwerk → Ansprache der Kontakte · Beiträge → Ansprache der Liker und Kommentierer
    Y_P, Y_N, Y_B = 54, 46, 62
    o.append(kanal(Y_P, "LinkedIn"))
    o.append(kasten(C1, Y_P, W1, 11, "Profil professionell anlegen"))
    o.append(zeilen(C2, Y_N - 8.6, ["mit Sales Navigator"], 2.05, 400, GRAU))
    o.append(kasten(C2, Y_N, W2, 9, "Netzwerk gezielt aufbauen"))
    o.append(kasten(C2, Y_B, W2, 9, "Beiträge veröffentlichen"))
    o.append(baum((C1 + W1 / 2, Y_P), [(C2 - W2 / 2, Y_N), (C2 - W2 / 2, Y_B)], 52))
    o.append(kasten(C4, Y_N, W4, 9, "Kontakte aktiv ansprechen"))
    o.append(kasten(C4, Y_B, W4, 11, "Liker und Kommentierer aktiv ansprechen"))
    o.append(gerade(C2 + W2 / 2, Y_N, C4 - W4 / 2, Y_N))
    o.append(gerade(C2 + W2 / 2, Y_B, C4 - W4 / 2, Y_B))

    # Instagram und Facebook – gleiche Spalten: Profil · Postings · Ansprache
    Y_SO = 84
    o.append(kanal(Y_SO, "Instagram und Facebook"))
    o.append(kasten(C1, Y_SO, W1, 11, "Profil und Seite anlegen"))
    o.append(kasten(C2, Y_SO, W2, 11, "Postings je Zielgruppe veröffentlichen"))
    o.append(kasten(C4, Y_SO, W4, 11, "Kommentare und Nachrichten aufgreifen"))
    o.append(gerade(C1 + W1 / 2, Y_SO, C2 - W2 / 2, Y_SO))
    o.append(gerade(C2 + W2 / 2, Y_SO, C4 - W4 / 2, Y_SO))

    # Landingpage – drei Wege
    Y_LP = 122
    o.append(kanal(Y_LP, "Landingpage"))
    o.append(kasten(C2, Y_LP, W2, 13, "Landingpage je Zielgruppe", "dunkel", 2.5, 600))
    wege = [("Termin buchen", Y_LP - 14), ("Kontaktformular", Y_LP), ("Download", Y_LP + 14)]
    for s, y in wege:
        o.append(kasten(C3, y, W3, 9, s))
    o.append(baum((C2 + W2 / 2, Y_LP), [(C3 - W3 / 2, y) for _, y in wege], C2 + W2 / 2 + 3.5))

    # Mailings und Newsletter
    Y_MA = 162
    o.append(kanal(Y_MA, "Mailings und Newsletter"))
    o.append(kasten(C2, Y_MA, W2, 11, "Mailing an den Bestand versenden"))

    # Inhalte führen auf die Landingpage (gestrichelte Achse in Spalte 2)
    o.append(gestrichelt([(C2, Y_B + 4.5), (C2, Y_SO - 5.5)], pfeil=False))
    o.append(gestrichelt([(C2, Y_SO + 5.5), (C2, Y_LP - 6.5 - .6)]))
    o.append(gestrichelt([(C2, Y_MA - 5.5), (C2, Y_LP + 6.5 + .6)]))
    o.append(zeilen(C2 - 1.6, (Y_SO + Y_LP) / 2 - 1, ["verlinken auf", "die Landingpage"], 2.05, 400, GRAU, anker="end"))
    o.append(zeilen(C2 - 1.6, (Y_LP + Y_MA) / 2, ["Link zur", "Landingpage"], 2.05, 400, GRAU, anker="end"))

    # Einstiege in den Vertrieb: Kennenlerngespräch (LinkedIn, Instagram/Facebook, Termin buchen) · Telefonakquise
    EX, EW = 202, 30
    Y_KE, Y_TE = Y_SO, wege[2][1]
    L = EX - EW / 2
    for s, y in (("Kennenlerngespräch", Y_KE), ("Telefonakquise", Y_TE)):
        o.append(kasten(EX, y, EW, 9, s, "weiss"))
    o.append(sammler([(C4 + W4 / 2, Y_N), (C4 + W4 / 2, Y_B), (C4 + W4 / 2, Y_SO), (C3 + W3 / 2, wege[0][1])], 172, (L, Y_KE)))
    o.append(sammler([(C3 + W3 / 2, wege[1][1]), (C3 + W3 / 2, Y_TE), (C2 + W2 / 2, Y_MA)], 168, (L, Y_TE)))

    # Prüffragen
    BUS = 221
    F1X, F2X, FY, FW, FH = 239.5, 276, (Y_KE + Y_TE) / 2, 29, 25
    o.append(sammler([(EX + EW / 2, Y_KE), (EX + EW / 2, Y_TE)], BUS, (F1X - FW / 2, FY)))
    o.append(kasten(F1X, FY, FW, FH, "Passt der Interessent zu uns und wollen wir die Zusammenarbeit vertiefen?", "frage", 2.25))
    o.append(kasten(F2X, FY, FW, FH, "Liegen alle Voraussetzungen für Bedarfsanalyse und Angebot vor?", "frage", 2.25))
    o.append(gerade(F1X + FW / 2, FY, F2X - FW / 2, FY))
    o.append(zeilen((F1X + F2X) / 2, FY - 2.4, ["Ja"], 2.3, 700, INK))
    # Ja → Beratung → Abschluss → Kundenbetreuung · Nein → vertrieblich warmhalten
    Y_JA, Y_NEIN = Y_KE, 150
    sp_m = [298 + 25.3 / 2, 326.3 + 25.3 / 2, 354.6 + 25.4 / 2]
    K = F2X + FW / 2 + 3.5
    o.append(baum((F2X + FW / 2, FY), [(sp_m[0] - 11.25, Y_JA), (sp_m[0] - 11.25, Y_NEIN)], K))
    o.append(zeilen(K + 1.5, (FY + Y_JA) / 2, ["Ja"], 2.3, 700, INK, anker="start"))
    o.append(zeilen(K + 1.5, (FY + Y_NEIN) / 2 + 6, ["Nein"], 2.3, 600, GRAU, anker="start"))
    schritte = ["Beratungstermin", "Angebot und Abschluss", "Kunden halten und ausbauen"]
    for i, (x, s) in enumerate(zip(sp_m, schritte)):
        o.append(kasten(x, Y_JA, 22.5, 13, s, "kern" if i == 0 else "weiss", 2.3, 600 if i == 0 else 400))
        if i:
            o.append(gerade(sp_m[i - 1] + 11.25, Y_JA, x - 11.25, Y_JA))
    o.append(kasten(sp_m[0], Y_NEIN, 22.5, 13, "Vertrieblich warmhalten", "weiss"))
    o.append(gestrichelt([(sp_m[0], Y_NEIN - 6.5), (sp_m[0], Y_JA + 7.1)]))
    o.append(zeilen(sp_m[0] + 1.6, (Y_JA + Y_NEIN) / 2, ["später"], 2.05, 400, GRAU, anker="start"))
    # Rücklauf: Kundenbetreuung bringt neue Anlässe – zurück in den Marketingbereich (kein bestimmter Punkt)
    YR, XR = 190, 112
    o.append(linie([(sp_m[2], Y_JA + 6.5), (sp_m[2], YR), (XR, YR), (XR, YR - 10)], farbe=INK, sw=SW))
    o.append(f'<rect x="{(XR + sp_m[2]) / 2 - 52}" y="{YR - 2.5}" width="104" height="5" fill="#fff"/>')
    o.append(zeilen((XR + sp_m[2]) / 2, YR, ["Regelmäßige Präsenz pflegt deinen Bestand – und bringt neue Anlässe."], 2.4, 600, INK))

    defs = ('<defs><linearGradient id="ad-v" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b9fbd"/>'
            '<stop offset="1" stop-color="#8613a1"/></linearGradient>'
            '<linearGradient id="ad-vh" gradientUnits="userSpaceOnUse" x1="0" y1="25" x2="0" y2="178"><stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient>'
            '<linearGradient id="ad-vt" gradientUnits="userSpaceOnUse" x1="115" y1="0" x2="145" y2="0"><stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient>'
            '<marker id="ad-p" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto" markerUnits="strokeWidth">'
            f'<path d="M1 1 L8.5 5 L1 9" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    return f'<svg class="ablauf" viewBox="0 0 {B} {H}" xmlns="http://www.w3.org/2000/svg">{defs}{"".join(o)}</svg>'
