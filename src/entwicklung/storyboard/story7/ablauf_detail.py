"""Detailstufe zur Grundstory: was in Marketing und Vertrieb passiert (Daniel, 12.11.2026, Vorlage: Ablaufbild Marketing/Vertrieb).

Zweite Seite nach der Grundstory kompakt – als würde man in die drei Phasen hineinzoomen.
Gezeichnet als SVG in Millimetern (1 Einheit = 1 mm), Breite 380 mm (A3 quer abzüglich Rand).
Schrift: Inter (Text 2,4 mm ≈ 6,8 pt, Titel 3 mm SemiBold), Inter Tight nur für die Phasen-Überschriften.
Farben wie die Website: Tinte, Grau, Flächen #f5f5f7, Verlauf nur am Kern (Landingpage).
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
    MX1, MX2 = 0, 168          # Marketing
    MP = 176                   # Messpunkt
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

    # Messpunkt
    o.append(linie([(MP, 25), (MP, P1)], gestrichelt=True, pfeil=False, farbe=INK, sw=.3))
    o.append(zeilen(MP, 16.5, ["Messpunkt: Leads"], 2.5, 700, INK))
    o.append(zeilen(MP, 21, ["Person und Kontaktweg bekannt"], 2.05, 400, GRAU))

    # Kanäle (Marketing)
    KX = 0           # Kanalname
    C = [43, 78, 113, 148]   # Mitten der Schritte
    W = 30           # Schrittbreite
    def kanal(y, name):
        return zeilen(KX, y, umbruch(name, 24, 2.8), 2.8, 600, INK, anker="start")

    Y_LI, Y_SO, Y_LP, Y_MA = 52, 80, 120, 162
    # LinkedIn
    o.append(kanal(Y_LI, "LinkedIn"))
    li = ["Profil professionell anlegen", "Netzwerk gezielt aufbauen (Sales Navigator)", "Beiträge veröffentlichen", "Kontakte, Liker und Kommentierer ansprechen"]
    for i, s in enumerate(li):
        o.append(kasten(C[i], Y_LI, W, 11, s))
        if i:
            o.append(linie([(C[i - 1] + W / 2, Y_LI), (C[i] - W / 2 - .6, Y_LI)]))
    # Instagram und Facebook
    o.append(kanal(Y_SO, "Instagram und Facebook"))
    # gleiche Spalten wie LinkedIn: Profil · (Netzwerk) · Inhalte · Ansprache
    so = [(0, "Profil und Seite pflegen"), (2, "Postings je Zielgruppe veröffentlichen"), (3, "Kommentare und Nachrichten aufgreifen")]
    for k, (i, s) in enumerate(so):
        o.append(kasten(C[i], Y_SO, W, 11, s))
        if k:
            o.append(linie([(C[so[k - 1][0]] + W / 2, Y_SO), (C[i] - W / 2 - .6, Y_SO)]))
    # Landingpage (Kern) mit drei Wegen
    o.append(kanal(Y_LP, "Landingpage"))
    o.append(kasten(C[0], Y_LP, W, 13, "Landingpage je Zielgruppe", "kern", 2.5, 600))
    wege = [("Termin buchen", Y_LP - 16), ("Kontaktformular", Y_LP), ("Download", Y_LP + 16)]
    for s, y in wege:
        o.append(linie([(C[0] + W / 2, Y_LP), (C[0] + W / 2 + 2.5, Y_LP), (C[0] + W / 2 + 2.5, y), (C[1] - W / 2 - .6, y)], pfeil=False))
        o.append(kasten(C[1], y, W, 9, s))
    # Beiträge und Postings verweisen auf die Landingpage (gestrichelt)
    o.append(linie([(C[2], Y_SO + 5.5), (C[2], Y_LP - 30), (C[0], Y_LP - 30), (C[0], Y_LP - 7.1)], gestrichelt=True, farbe=GRAU, sw=.3))
    o.append(linie([(C[2], Y_LI + 5.5), (C[2], Y_SO - 5.5)], gestrichelt=True, pfeil=False, farbe=GRAU, sw=.3))
    o.append(zeilen(C[0] + 2, Y_LP - 27, ["Beiträge und Postings verlinken auf die Landingpage"], 2.05, 400, GRAU, anker="start"))
    # Mailings und Newsletter
    o.append(kanal(Y_MA, "Mailings und Newsletter"))
    o.append(kasten(C[0], Y_MA, W, 11, "Mailing an den Bestand versenden"))
    o.append(linie([(C[0], Y_MA - 5.5), (C[0], Y_LP + 7.1)], gestrichelt=True, farbe=GRAU, sw=.3))
    o.append(zeilen(C[0] + 2, Y_MA - 14, ["Link zur Landingpage"], 2.05, 400, GRAU, anker="start"))

    # Einstiege in den Vertrieb
    EX, EW = 202, 30
    Y_KE, Y_KL, Y_TE = 66, 104, 136
    ein = [("Kennenlerngespräch", Y_KE), ("Klärungsgespräch", Y_KL), ("Telefonakquise", Y_TE)]
    for s, y in ein:
        o.append(kasten(EX, y, EW, 9, s, "weiss"))
    # Linien Marketing → Einstiege (über den Messpunkt)
    o.append(linie([(C[3] + W / 2, Y_LI), (172, Y_LI), (172, Y_KE), (EX - EW / 2 - .6, Y_KE)]))
    o.append(linie([(C[3] + W / 2, Y_SO), (172, Y_SO), (172, Y_KE)], pfeil=False))
    o.append(linie([(C[1] + W / 2, wege[0][1]), (EX - EW / 2 - .6, Y_KL)][:1] + [(160, wege[0][1]), (160, Y_KL), (EX - EW / 2 - .6, Y_KL)]))
    o.append(linie([(C[1] + W / 2, wege[1][1]), (164, wege[1][1]), (164, Y_TE), (EX - EW / 2 - .6, Y_TE)]))
    o.append(linie([(C[1] + W / 2, wege[2][1]), (164, wege[2][1])], pfeil=False))
    o.append(linie([(C[0] + W / 2, Y_MA), (164, Y_MA), (164, Y_TE)], pfeil=False))

    # Prüffragen
    BUS = 221
    F1X, F2X, FY, FW, FH = 239.5, 276, 101, 29, 25
    for y in (Y_KE, Y_KL, Y_TE):
        o.append(linie([(EX + EW / 2, y), (BUS, y)], pfeil=False))
    o.append(linie([(BUS, Y_KE), (BUS, Y_TE)], pfeil=False))
    o.append(linie([(BUS, FY), (F1X - FW / 2 - .6, FY)]))
    o.append(kasten(F1X, FY, FW, FH, "Passt der Interessent zu uns und wollen wir die Zusammenarbeit vertiefen?", "frage", 2.25))
    o.append(kasten(F2X, FY, FW, FH, "Liegen alle Voraussetzungen für Bedarfsanalyse und Angebot vor?", "frage", 2.25))
    o.append(linie([(F1X + FW / 2, FY), (F2X - FW / 2 - .6, FY)]))
    o.append(zeilen((F1X + F2X) / 2, FY - 2.4, ["Ja"], 2.3, 700, INK))
    # Nein 1 → keine weiteren Aktionen
    o.append(linie([(F1X, FY + FH / 2), (F1X, 151 - 6.6)]))
    o.append(zeilen(F1X + 2, FY + FH / 2 + 7, ["Nein"], 2.3, 600, GRAU, anker="start"))
    o.append(kasten(F1X, 151, FW, 12, "Keine weiteren Aktionen", "leer"))
    # Ja 2 → Beratung → Abschluss → Kundenbetreuung
    Y_JA, Y_NEIN = 66, 151
    o.append(linie([(F2X + FW / 2, FY), (F2X + FW / 2 + 3.5, FY), (F2X + FW / 2 + 3.5, Y_JA), (310.6 - 11.8, Y_JA)]))
    o.append(zeilen(F2X + FW / 2 + 5, (FY + Y_JA) / 2, ["Ja"], 2.3, 700, INK, anker="start"))
    sp_m = [298 + 25.3 / 2, 326.3 + 25.3 / 2, 354.6 + 25.4 / 2]
    schritte = ["Beratungstermin", "Angebot und Abschluss", "Kunden halten und ausbauen"]
    for i, (x, s) in enumerate(zip(sp_m, schritte)):
        o.append(kasten(x, Y_JA, 22.5, 13, s, "kern" if i == 2 else "weiss", 2.3, 600 if i == 2 else 400))
        if i:
            o.append(linie([(sp_m[i - 1] + 11.25, Y_JA), (x - 11.25 - .6, Y_JA)]))
    # Nein 2 → vertrieblich warmhalten
    o.append(linie([(F2X + FW / 2 + 3.5, FY), (F2X + FW / 2 + 3.5, Y_NEIN), (sp_m[0] - 11.25 - .6, Y_NEIN)]))
    o.append(zeilen(F2X + FW / 2 + 5, (FY + Y_NEIN) / 2 + 6, ["Nein"], 2.3, 600, GRAU, anker="start"))
    o.append(kasten(sp_m[0], Y_NEIN, 22.5, 13, "Vertrieblich warmhalten", "weiss"))
    o.append(linie([(sp_m[0], Y_NEIN - 6.5), (sp_m[0], Y_JA + 7.1)], gestrichelt=True, farbe=GRAU, sw=.3))
    o.append(zeilen(sp_m[0] + 1.6, (Y_JA + Y_NEIN) / 2, ["später"], 2.05, 400, GRAU, anker="start"))
    # Rücklauf: Kundenbetreuung bringt neue Anlässe (Bestand → Mailings)
    YR = 190
    o.append(linie([(sp_m[2], Y_JA + 6.5), (sp_m[2], YR), (C[0], YR), (C[0], Y_MA + 5.5 + .6)], farbe=INK, sw=.35))
    o.append(f'<rect x="{(C[0] + sp_m[2]) / 2 - 52}" y="{YR - 2.5}" width="104" height="5" fill="#fff"/>')
    o.append(zeilen((C[0] + sp_m[2]) / 2, YR, ["Regelmäßige Präsenz pflegt deinen Bestand – und bringt neue Anlässe."], 2.4, 600, INK))

    defs = ('<defs><linearGradient id="ad-v" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b9fbd"/>'
            '<stop offset="1" stop-color="#8613a1"/></linearGradient>'
            '<marker id="ad-p" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto" markerUnits="strokeWidth">'
            f'<path d="M1 1 L8.5 5 L1 9" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    return f'<svg class="ablauf" viewBox="0 0 {B} {H}" xmlns="http://www.w3.org/2000/svg">{defs}{"".join(o)}</svg>'
