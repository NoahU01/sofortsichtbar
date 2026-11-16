"""Personen für Story 8, Variante 2 – gezeichnet, straight, modern (Daniel, 16.11.2026).
Maßstab: Ganzkörper, aufrecht, schlanke Proportionen wie eine Modezeichnung; Ausdruck über Haltung und Arbeitsgerät,
nicht über Gesichter; flache Formen ohne Konturen; je Person EIN Akzentton (sofort sichtbar) bzw. Tinte/Grau (Agentur).
Schreibt s7.team8.figuren = {id: svg} in story8.11tydata.json und assets/team/team-wir.svg (Bild „Freiheit“).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

HAUT = {"a": "#ecd3c1", "b": "#d4ab8c", "c": "#a7765a"}
HAAR = "#1d1d1f"
HAAR2 = "#5a4031"
TINTE, GRAU, GRAU2, WEISS = "#1d1d1f", "#48484a", "#8e8e93", "#ffffff"
CYAN, BLAU, VIOLETT = "#0b9fbd", "#3d5bd1", "#8613a1"


def r(d, f):
    return f'<path d="{d}" fill="{f}"/>'


def figur(jacke, hose, haut, frisur, pose, rock=False, haar=HAAR, headset=False, spiel=0):
    h = HAUT[haut]
    o = []
    # Haare hinten
    if frisur == "lang":
        o.append(r("M21.5 14 C21 2.5 39 2.5 38.5 14 L40 36 C34 38 26 38 20 36 Z", haar))
    if frisur == "bob":
        o.append(r("M21.5 15 C21 3 39 3 38.5 15 L39 25 C35 27 25 27 21 25 Z", haar))
    if frisur == "zopf":
        o.append(r("M36 9 C44 11 45 26 41 33 C40.5 25 39 18 35 14 Z", haar))
    # Beine
    if rock:
        o.append(r("M23 108 H27.6 L27 151 H23.6 Z M32.4 108 H37 L36.4 151 H33 Z", h))
        o.append(r("M20 72 H40 L43.5 110 H16.5 Z", hose))
    else:
        o.append(r(f"M19.5 78 H29.6 L28.4 151 H22.6 Z M30.4 78 H40.5 L{37.4 + spiel} 151 H{31.6 + spiel} Z", hose))
    # Schuhe
    o.append(r("M21.5 150 H29 C30.6 150 30.6 154.5 29 154.5 H20.4 C19.4 154.5 19.6 150 21.5 150 Z", TINTE))
    o.append(r(f"M{31 + spiel} 150 H{38.6 + spiel} C{40.6 + spiel} 150 {40.4 + spiel} 154.5 {39.6 + spiel} 154.5 H{31 + spiel} C{29.4 + spiel} 154.5 {29.4 + spiel} 150 {31 + spiel} 150 Z", TINTE))
    # Hals, Rumpf
    o.append(r("M27.4 21 H32.6 V30 H27.4 Z", h))
    unten = 74 if rock else 80
    o.append(r(f"M16.5 33.5 C16.5 29 20.5 27 25.5 27 H34.5 C39.5 27 43.5 29 43.5 33.5 L41.5 {unten} H18.5 Z", jacke))
    o.append(r("M25.6 27 L30 41 L34.4 27 Z", WEISS))
    o.append(r(f"M25.6 27 L30 41 L29 {unten} H27.5 L23.5 33 Z M34.4 27 L30 41 L31 {unten} H32.5 L36.5 33 Z", "rgba(0,0,0,.14)"))
    # Arme je Haltung
    links_unten = "M16.5 33.5 C13.8 34.5 13 38 13 42 L13.6 77 C13.7 79.5 17.6 79.5 17.8 77 L19 44 Z"
    rechts_unten = "M43.5 33.5 C46.2 34.5 47 38 47 42 L46.4 77 C46.3 79.5 42.4 79.5 42.2 77 L41 44 Z"
    if pose == "locker":            # Arme hängen, linke Hand in der Tasche
        o.append(r("M16.5 33.5 C13.8 34.5 13 38 13 42 L14.5 72 C15 74 19 74 19.2 72 L19 44 Z", jacke))
        o.append(r(rechts_unten, jacke))
        o.append(f'<circle cx="44.4" cy="80.6" r="2.6" fill="{h}"/>')
    elif pose == "verschraenkt":    # Arme vor der Brust verschränkt: zwei Unterarme schräg übereinander
        o.append(r("M16.5 33.5 C13.8 34.5 13 38 13 42 L13.6 57 C14 60 18.4 60 18.6 57 L19 44 Z", jacke))
        o.append(r("M43.5 33.5 C46.2 34.5 47 38 47 42 L46.4 57 C46 60 41.6 60 41.4 57 L41 44 Z", jacke))
        o.append(f'<circle cx="41" cy="50.6" r="2.3" fill="{h}"/>')
        o.append(r("M14.6 55.6 C13.6 52.6 15.6 50.6 18.4 50.8 L41.2 48.6 C43.6 48.4 44.4 52.6 41.8 53.6 L18.6 59.6 C16.8 60 15.2 58 14.6 55.6 Z", jacke))
        o.append(f'<circle cx="19" cy="55.6" r="2.3" fill="{h}"/>')
        o.append(r("M45.4 56.2 C46.4 53.2 44.4 51.2 41.6 51.4 L18.8 52.6 C16.4 52.8 15.6 56.8 18.2 57.8 L41.4 60.2 C43.2 60.4 44.8 58.6 45.4 56.2 Z", jacke))
        o.append(r("M18.8 52.6 L41.6 51.4 L41.8 53.2 L19 54.4 Z", "rgba(0,0,0,.18)"))
    elif pose == "laptop":          # Laptop unter dem rechten Arm
        o.append(r(links_unten, jacke))
        o.append(f'<circle cx="15.7" cy="80.6" r="2.6" fill="{h}"/>')
        o.append(r("M42.6 44 L50.6 45.2 L48.8 79 L40.8 77.8 Z", "#c7c7cc"))
        o.append(r("M49.4 45.1 L50.6 45.2 L48.8 79 L47.6 78.8 Z", "#8e8e93"))
        o.append(r(rechts_unten, jacke))
        o.append(f'<circle cx="44.4" cy="80.6" r="2.6" fill="{h}"/>')
    elif pose == "handy":           # Handy vor der Brust
        o.append(r(links_unten, jacke))
        o.append(f'<circle cx="15.7" cy="80.6" r="2.6" fill="{h}"/>')
        o.append(r("M43.5 33.5 C46.2 34.5 47 38 47 42 L46.6 58 C46.4 60.5 42.6 60.5 42.4 58 L41 44 Z", jacke))
        o.append(r("M46.6 56 C46.6 60 44 61 40 59.5 L33 55.5 C31.4 54.5 32.6 51.6 34.4 52.4 L42.4 56 Z", jacke))
        o.append(r("M31 44.5 H37 V56 H31 Z", TINTE))
        o.append(f'<circle cx="33" cy="54.4" r="2.4" fill="{h}"/>')
    # Kopf
    o.append(f'<ellipse cx="30" cy="14.5" rx="7.2" ry="8.6" fill="{h}"/>')
    # Haare vorn
    if frisur == "kurz":
        o.append(r("M22.6 13.5 C21.6 4.5 38.4 3.8 37.4 13.5 C35.5 9.6 27 9 22.6 13.5 Z", haar))
    if frisur == "scheitel":
        o.append(r("M22.6 14 C21.4 4 38.6 3.4 37.4 13 C34 8.6 29 8.4 26.6 10 C25 11 23.6 12.4 22.6 14 Z", haar))
    if frisur == "glatze":
        o.append(r("M23 17 C24 25.5 36 25.5 37 17 C34 21 26 21 23 17 Z", haar))
    if frisur in ("lang", "bob", "zopf"):
        o.append(r("M22.6 15 C21.6 4 38.4 3.6 37.4 14 C34 9 27.6 8.4 22.6 15 Z", haar))
    if frisur == "dutt":
        o.append(f'<circle cx="30" cy="5.2" r="3.8" fill="{haar}"/>')
        o.append(r("M22.8 14 C22 5.8 38 5.4 37.2 14 C34.6 9.6 25.4 9.6 22.8 14 Z", haar))
    if headset:
        o.append('<path d="M22 15 C21.4 3.4 38.6 3.4 38 15" fill="none" stroke="#1d1d1f" stroke-width="1.2"/>'
                 '<rect x="20.6" y="12.6" width="3" height="5.6" rx="1.5" fill="#1d1d1f"/>'
                 '<path d="M22.2 18 C22.6 21.6 25 22.6 27.6 22.4" fill="none" stroke="#1d1d1f" stroke-width="1"/>')
    return f'<svg viewBox="0 0 60 158" aria-hidden="true">{"".join(o)}</svg>'


FIGUREN = {
    # sofort sichtbar – je Person ein Ton
    "strategie": dict(jacke=CYAN, hose=TINTE, haut="a", frisur="scheitel", pose="verschraenkt", haar=HAAR2, spiel=2.4),
    "texte": dict(jacke=VIOLETT, hose=TINTE, haut="b", frisur="lang", pose="handy", rock=True),
    "technik": dict(jacke=BLAU, hose=TINTE, haut="c", frisur="kurz", pose="laptop", spiel=1.6),
    "social": dict(jacke=BLAU, hose=TINTE, haut="a", frisur="dutt", pose="handy", haar=HAAR2),
    # Agentur
    "marketing": dict(jacke=GRAU, hose=TINTE, haut="b", frisur="bob", pose="handy", spiel=1.2),
    "vertrieb": dict(jacke=TINTE, hose=GRAU, haut="a", frisur="kurz", pose="locker", haar=HAAR2, spiel=2.4),
    "innendienst": dict(jacke=GRAU, hose=TINTE, haut="c", frisur="zopf", pose="laptop", headset=True),
}


def teambild(ids):
    teile = "".join(f'<g transform="translate({i * 46} 0)">' + figur(**FIGUREN[k]).replace('<svg viewBox="0 0 60 158" aria-hidden="true">', '').replace('</svg>', '') + '</g>'
                    for i, k in enumerate(ids))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {60 + 46 * (len(ids) - 1)} 158">{teile}</svg>'


if __name__ == "__main__":
    pfad = os.path.join(HERE, "story8.11tydata.json")
    d = json.load(open(pfad, encoding="utf-8"))
    d["s7"]["team8"]["figuren"] = {k: figur(**v) for k, v in FIGUREN.items()}
    d["s7"]["team8"].pop("stile", None)
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(pfad, "a").write("\n")
    open(os.path.join(HERE, "assets", "team", "team-wir.svg"), "w").write(teambild(["strategie", "texte", "technik", "social"]))
    print("Figuren geschrieben:", ", ".join(FIGUREN))
