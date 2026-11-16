"""Personen-Grafiken für Story 8, Variante 2 (Daniel, 16.11.2026):
keine Stockfotos, keine echten Bilder des Teams, keine Strichmännchen – moderne, professionelle Team-Illustration.
Maßstab: Team-Illustrationen moderner Tech-Unternehmen – echte Proportionen, plastische Gesichter (Licht- und Schattenseite, Ohren),
verschiedene Hauttöne und Frisuren, Business-Kleidung mit Schattenflächen. Kleidung über die Klasse .k (Farbe = sofort sichtbar, Tinte = Agentur).
Schreibt s7.team8.figuren = {id: svg} in story8.11tydata.json.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

HAUT = {"hell": ("#f1d3bf", "#dfb59c"), "mittel": ("#d8a47c", "#c08b63"), "dunkel": ("#99674a", "#81533a"), "warm": ("#e7b891", "#d29f78")}
HAAR = {"schwarz": ("#221c1a", "#3a302c"), "braun": ("#4e3222", "#6b4630"), "blond": ("#c8995a", "#ddb57a"), "rot": ("#7a3a22", "#97502f")}

KOPF = "M41 54 C41 35 79 35 79 54 L79 62 C79 76 70 86 60 86 C50 86 41 76 41 62 Z"
KOPF_SCHATTEN = "M65 37 C75 40 79 46 79 54 L79 62 C79 76 70 86 60 86 C67 80 71 71 71 61 C71 50 69 42 65 37 Z"
HALS = "M51 78 L69 78 L70 99 C65 104 55 104 50 99 Z"
HALS_SCHATTEN = "M51 80 C55 89 65 89 69 80 L69 87 C64 93 56 93 51 87 Z"
TORSO = "M12 140 C12 113 28 101 47 97 L73 97 C92 101 108 113 108 140 Z"
TORSO_SCHATTEN = "M80 99 C95 105 108 116 108 140 L86 140 C86 124 84 110 80 99 Z"
BRILLE = ("M43 56 h13 a2 2 0 0 1 2 2 v3 a5 5 0 0 1-5 5 h-5 a5 5 0 0 1-5-5 v-3 a2 2 0 0 1 2-2 z "
          "M64 56 h13 a2 2 0 0 1 2 2 v3 a5 5 0 0 1-5 5 h-5 a5 5 0 0 1-5-5 v-3 a2 2 0 0 1 2-2 z M58 58.5 h4")


def p(d, fill, extra=""):
    return f'<path d="{d}" fill="{fill}"{extra}/>'


def figur(haut, haar, frisur, kleidung, brille=False, bart=False, headset=False):
    h, hs = HAUT[haut]
    ha, hl = HAAR[haar]
    o = []
    # Haare hinten (lang, Bob, Zopf)
    if frisur == "lang":
        o.append(p("M38 52 C35 28 85 28 82 52 L85 102 C76 107 44 107 35 102 Z", ha, ' class="r"'))
    if frisur == "bob":
        o.append(p("M38 56 C35 29 85 29 82 56 L83 82 C76 86 44 86 37 82 Z", ha, ' class="r"'))
    if frisur == "zopf":
        o.append(p("M76 44 C92 50 94 76 84 92 C82 78 80 64 74 54 Z", ha, ' class="r"'))
    # Körper
    o.append(p(TORSO, "", ' class="k r"'))
    o.append(p(TORSO_SCHATTEN, "rgba(0,0,0,.16)"))
    if kleidung in ("sakko", "sakko-krawatte"):
        o.append(p("M50 97 L60 118 L70 97 Z", "#ffffff"))
        if kleidung == "sakko-krawatte":
            o.append(p("M57.5 99 H62.5 L64.5 117 L60 123 L55.5 117 Z", "#1d1d1f"))
        o.append(p("M47 97 L60 124 L55 140 L38 140 C39 121 42 107 47 97 Z M73 97 L60 124 L65 140 L82 140 C81 121 78 107 73 97 Z", "rgba(0,0,0,.2)"))
    if kleidung == "bluse":
        o.append(p("M49 97 L60 110 L71 97 Z", "#ffffff"))
        o.append(p("M48 96 L60 108 L53 114 Z M72 96 L60 108 L67 114 Z", "rgba(255,255,255,.85)"))
    # Hals und Kopf
    if kleidung != "rolli":
        o.append(p(HALS, h))
        o.append(p(HALS_SCHATTEN, hs))
    else:
        o.append(p(HALS, h))
        o.append(p("M48 104 C48 110 72 110 72 104 L72 88 C66 93 54 93 48 88 Z", "", ' class="k"'))
        o.append(p("M48 104 C48 110 72 110 72 104 L72 99 C66 104 54 104 48 99 Z", "rgba(0,0,0,.18)"))
    o.append(f'<ellipse cx="41" cy="61" rx="4" ry="6" fill="{h}"/><ellipse cx="79" cy="61" rx="4" ry="6" fill="{hs}"/>')
    o.append(p(KOPF, h))
    o.append(p(KOPF_SCHATTEN, hs))
    # Haare vorn
    if frisur == "kurz":
        o.append(p("M40 56 C36 33 50 25 62 26 C75 26 84 35 80 56 C78 45 74 41 66 40 C57 39 48 41 44 47 C42 50 41 53 40 56 Z", ha))
        o.append(p("M48 33 C56 28 68 29 74 35 C66 32 57 32 48 36 Z", hl))
    if frisur == "seitenscheitel":
        o.append(p("M40 57 C36 32 52 24 64 26 C77 28 84 38 80 55 C76 42 66 36 54 39 C48 42 43 48 40 57 Z", ha))
        o.append(p("M54 31 C62 28 72 31 76 37 C68 33 61 33 54 36 Z", hl))
    if frisur in ("lang", "bob"):
        o.append(p("M39 60 C36 33 82 29 81 56 C77 43 66 37 55 40 C49 44 43 51 39 60 Z", ha))
        o.append(p("M55 34 C64 31 73 34 77 40 C70 36 62 36 55 38 Z", hl))
    if frisur == "dutt":
        o.append(f'<circle cx="60" cy="31" r="9" fill="{ha}"/>')
        o.append(p("M41 55 C38 34 82 32 79 55 C75 43 66 39 60 39 C54 39 45 43 41 55 Z", ha))
        o.append(p("M50 36 C57 33 66 34 72 38 C65 36 57 36 50 38 Z", hl))
    if frisur == "zopf":
        o.append(p("M40 57 C37 33 82 31 80 55 C76 42 66 38 58 39 C50 41 44 47 40 57 Z", ha))
        o.append(p("M51 34 C59 31 69 33 74 38 C67 35 59 35 51 37 Z", hl))
    if bart:
        o.append(p("M42 66 C43 81 52 89 60 89 C68 89 77 81 78 66 C74 74 68 77 60 77 C52 77 46 74 42 66 Z", ha))
        o.append(p("M53 72 C56 70 64 70 67 72 C64 74 56 74 53 72 Z", ha))
    if brille:
        o.append(f'<path d="{BRILLE}" fill="none" stroke="#1d1d1f" stroke-width="1.8" stroke-linejoin="round"/>')
    if headset:
        o.append('<path d="M38 60 C36 30 84 30 82 60" fill="none" stroke="#1d1d1f" stroke-width="2.4" stroke-linecap="round"/>'
                 '<path d="M40 68 C41 77 47 80 54 80" fill="none" stroke="#1d1d1f" stroke-width="2" stroke-linecap="round"/>'
                 '<rect x="34" y="55" width="8" height="13" rx="4" fill="#1d1d1f"/><circle cx="55" cy="80" r="2" fill="#1d1d1f"/>')
    return f'<svg viewBox="0 0 120 140" aria-hidden="true">{"".join(o)}</svg>'


FIGUREN = {
    # sofort sichtbar
    "strategie": dict(haut="hell", haar="braun", frisur="glatze", kleidung="sakko", brille=True, bart=True),
    "texte": dict(haut="mittel", haar="schwarz", frisur="lang", kleidung="sakko"),
    "technik": dict(haut="dunkel", haar="schwarz", frisur="kurz", kleidung="rolli"),
    "social": dict(haut="hell", haar="blond", frisur="dutt", kleidung="rolli"),
    # Agentur
    "marketing": dict(haut="warm", haar="schwarz", frisur="bob", kleidung="bluse"),
    "vertrieb": dict(haut="hell", haar="braun", frisur="seitenscheitel", kleidung="sakko-krawatte", brille=True),
    "innendienst": dict(haut="mittel", haar="rot", frisur="zopf", kleidung="sakko", headset=True),
}

def teambild(ids):
    """Gruppe für das Bild „Freiheit“: unser Team als eine Grafik (eigene Datei mit Verlauf)"""
    teile = []
    for i, k in enumerate(ids):
        teile.append(f'<g transform="translate({i * 92} {(i % 2) * 6})">' + figur(**FIGUREN[k]).replace('<svg viewBox="0 0 120 140" aria-hidden="true">', '').replace('</svg>', '') + '</g>')
    breite = 120 + 92 * (len(ids) - 1)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {breite} 146"><defs><linearGradient id="g" x1="0" x2="1">'
            '<stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient>'
            '<style>.k{fill:url(#g)}.r{stroke:#1d1d1f;stroke-width:2;paint-order:stroke}</style></defs>' + "".join(reversed(teile)) + '</svg>')


if __name__ == "__main__":
    pfad = os.path.join(HERE, "story8.11tydata.json")
    d = json.load(open(pfad, encoding="utf-8"))
    d["s7"]["team8"]["figuren"] = {k: figur(**v) for k, v in FIGUREN.items()}
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(pfad, "a").write("\n")
    open(os.path.join(HERE, "assets", "team", "team-wir.svg"), "w").write(teambild(["strategie", "texte", "technik", "social"]))
    print("Figuren geschrieben:", ", ".join(FIGUREN))
