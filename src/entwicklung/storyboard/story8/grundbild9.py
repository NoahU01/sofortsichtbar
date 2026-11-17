"""Grundstory in einem Bild: „Der Weg von Familie K.“ (Daniel, 17.11.2026).
Eine Hauptfigur (Familie K.) als farbiger Faden von links nach rechts; alles andere in einem Stil:
weiße Karten mit grauer Kontur, Tinte für die Agentur, Grau für das Netz, Farbe nur für Familie K.
Kapitel: Auswählen (Stapel) · Betreiben (Postings im Netz) · Vertrieb (Checkliste, Anruf, Termin) · Betreuen (Kundenkreis, neuer Anlass, zurück).
Schreibt s7.s9.grundbild (SVG) in story8.11tydata.json.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 540
TINTE, GRAU, LINIE, HELL = "#1d1d1f", "#8e8e93", "#d2d2d7", "#ececf0"
FK = "url(#gb-g)"


def t(x, y, s, gr=12, gew=500, farbe=GRAU, anker="start", fam="Inter"):
    return f'<text x="{x}" y="{y}" font-family="{fam}, system-ui, sans-serif" font-size="{gr}" font-weight="{gew}" fill="{farbe}" text-anchor="{anker}">{s}</text>'


def karte(x, y, w, h, inhalt="", dreh=0, schatten=True):
    tr = f' transform="rotate({dreh} {x + w / 2} {y + h / 2})"' if dreh else ""
    sch = f'<rect x="{x}" y="{y + 4}" width="{w}" height="{h}" rx="10" fill="#000" opacity=".05"/>' if schatten else ""
    return f'<g{tr}>{sch}<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="{LINIE}" stroke-width="1.5"/>{inhalt}</g>'


def zeilen(x, y, breiten, abst=9, dicke=4, farbe=HELL):
    return "".join(f'<rect x="{x}" y="{y + i * abst}" width="{b}" height="{dicke}" rx="2" fill="{farbe}"/>' for i, b in enumerate(breiten))


def posting(x, y, w=74, h=92, dreh=0, kanal=""):
    i = (f'<rect x="{x + 8}" y="{y + 8}" width="12" height="12" rx="3" fill="{TINTE}"/>{zeilen(x + 25, y + 11, [26], dicke=4)}'
         f'<rect x="{x + 8}" y="{y + 26}" width="{w - 16}" height="{h - 48}" rx="5" fill="{HELL}"/>'
         f'{zeilen(x + 8, y + h - 16, [w - 30], dicke=4)}')
    if kanal:
        i += t(x + 14, y + 18.5, kanal, 7.5, 700, "#fff", "middle")
    return karte(x, y, w, h, i, dreh)


def svg():
    o = []
    o.append('<defs><linearGradient id="gb-g" x1="0" x2="1"><stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient>'
             '<marker id="gb-p" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#3d5bd1" stroke-width="1.8"/></marker></defs>')
    # Kapitel
    for i, name in enumerate(["Auswählen", "Betreiben", "Vertrieb", "Betreuen"]):
        x = i * 300 + 20
        o.append(t(x, 30, name, 16, 700, TINTE, fam="Inter Tight"))
        o.append(f'<rect x="{x}" y="42" width="260" height="2" fill="{TINTE}"/>')
    # Fläche „deine Agentur“ hinter Vertrieb und Betreuen
    o.append(f'<rect x="604" y="64" width="592" height="372" rx="22" fill="#f5f5f7"/>')
    o.append(t(624, 90, "Ab hier: deine Agentur", 12, 600))

    # 1 Auswählen: die Strecke als Stapel
    o.append(karte(34, 116, 150, 104, f'<path d="M54 140 h110 v62 h-110 z M54 140 l55 34 l55 -34" fill="none" stroke="{GRAU}" stroke-width="1.5"/>', -10))
    o.append(posting(150, 120, 92, 112, 7, "in"))
    lp = (f'<circle cx="68" cy="168" r="3" fill="{LINIE}"/><circle cx="78" cy="168" r="3" fill="{LINIE}"/><circle cx="88" cy="168" r="3" fill="{LINIE}"/>'
          f'<line x1="56" y1="178" x2="236" y2="178" stroke="{HELL}" stroke-width="1.5"/>'
          + t(70, 198, "Deine Agentur", 9, 700, "#3d5bd1")
          + f'<rect x="70" y="207" width="96" height="9" rx="3" fill="{TINTE}"/><rect x="70" y="221" width="78" height="9" rx="3" fill="{TINTE}"/>'
          + zeilen(70, 240, [88, 70], dicke=4)
          + f'<rect x="70" y="262" width="62" height="16" rx="8" fill="#3d5bd1"/>'
          + f'<rect x="178" y="200" width="46" height="78" rx="6" fill="{HELL}"/><path d="M190 232 l11-9 l11 9 M193 230 v14 h16 v-14" fill="none" stroke="{GRAU}" stroke-width="1.5"/>'
          + zeilen(70, 296, [160, 140, 150], dicke=4))
    o.append(karte(56, 158, 184, 172, lp))
    o.append(t(148, 360, "Landingpage, Postings, Mailing", 12, 600, TINTE, "middle"))
    o.append(t(148, 377, "für Private Bauherren", 12, 500, GRAU, "middle"))

    # 2 Betreiben: der Stapel fächert sich auf, Postings gehen ins Netz
    for (x, y, d, k) in ((318, 104, -6, "in"), (362, 172, 3, "f"), (318, 246, -2, "ig")):
        o.append(posting(x, y, 64, 78, d, k))
        o.append(f'<path d="M244 {y + 40} C 270 {y + 40} 290 {y + 40} {x - 4} {y + 40}" fill="none" stroke="{LINIE}" stroke-width="1.5" stroke-dasharray="3 4"/>')
    random.seed(7)
    punkte = []
    while len(punkte) < 26:
        x, y = random.uniform(448, 584), random.uniform(100, 400)
        if all(math.hypot(x - a, y - b) > 22 for a, b in punkte):
            punkte.append((x, y))
    fk = (548, 300)
    punkte = [p for p in punkte if math.hypot(p[0] - fk[0], p[1] - fk[1]) > 24]
    for x, y in punkte[:14]:
        qx, qy = (382, 143) if y < 190 else ((426, 211) if y < 280 else (382, 285))
        o.append(f'<line x1="{qx}" y1="{qy}" x2="{x}" y2="{y}" stroke="{HELL}" stroke-width="1.2"/>')
    o.append(f'<line x1="426" y1="211" x2="{fk[0]}" y2="{fk[1]}" stroke="#3d5bd1" stroke-width="1.6" opacity=".55"/>')
    for x, y in punkte:
        o.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" stroke="{GRAU}" stroke-width="1.5"/>')
    o.append(t(516, 432, "Bauherren in der Region", 12, 600, GRAU, "middle"))

    # Familie K. – der Faden
    faden = f"M{fk[0]} {fk[1]} C 600 300 620 300 670 300 S 730 250 768 250 S 830 300 872 300"
    o.append(f'<path d="{faden}" fill="none" stroke="{FK}" stroke-width="4" stroke-linecap="round"/>')
    # 3 Vertrieb: Checkliste, Anruf, Termin
    o.append(karte(646, 272, 48, 58, f'<path d="M656 286 l4 4 l7 -8 M656 302 l4 4 l7 -8 M656 318 l4 4 l7 -8" fill="none" stroke="#3d5bd1" stroke-width="1.8"/>' + zeilen(672, 286, [14, 14, 14], abst=16, dicke=3, farbe=LINIE)))
    o.append(t(670, 352, "Checkliste geladen", 11.5, 600, TINTE, "middle"))
    o.append(f'<circle cx="768" cy="250" r="28" fill="{TINTE}"/><path d="M757 240 h6 l3 7 -4 3 a15 15 0 0 0 8 8 l3-4 7 3 v6 a3 3 0 0 1-3 3 a24 24 0 0 1-23-23 a3 3 0 0 1 3-3z" fill="#fff"/>')
    o.append(t(768, 298, "Anruf", 11.5, 600, TINTE, "middle"))
    o.append(karte(840, 268, 66, 66, f'<rect x="840" y="268" width="66" height="18" rx="9" fill="{TINTE}"/><rect x="840" y="277" width="66" height="9" fill="{TINTE}"/>'
                   + t(873, 281, "Di", 10, 700, "#fff", "middle") + t(873, 316, "17:00", 15, 700, TINTE, "middle", "Inter Tight")))
    o.append(t(873, 352, "Beratung", 11.5, 600, TINTE, "middle"))

    # 4 Betreuen: Kundenkreis der Agentur, Familie K. ist drin, neuer Anlass
    cx, cy, r = 1062, 290, 92
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINIE}" stroke-width="1.5"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="{TINTE}"/>' + t(cx, cy - 2, "Deine", 11, 700, "#fff", "middle") + t(cx, cy + 12, "Agentur", 11, 700, "#fff", "middle"))
    pos = []
    for k in range(8):
        a = math.radians(-90 + k * 45)
        pos.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    fk2 = pos[5]  # unten links
    for i, (x, y) in enumerate(pos):
        if i == 5:
            continue
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#fff" stroke="{GRAU}" stroke-width="1.5"/>')
    # neues Posting erreicht den Kreis
    o.append(posting(1032, 96, 60, 70, 0, "in"))
    for i in (0, 1, 7):
        x, y = pos[i]
        o.append(f'<line x1="1062" y1="166" x2="{x:.1f}" y2="{y:.1f}" stroke="{LINIE}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    o.append(f'<line x1="1050" y1="166" x2="{fk2[0]:.1f}" y2="{fk2[1]:.1f}" stroke="#3d5bd1" stroke-width="1.6" opacity=".55"/>')
    # Familie K. im Kreis + Anlass
    o.append(f'<circle cx="{fk2[0]:.1f}" cy="{fk2[1]:.1f}" r="16" fill="#8613a1" opacity=".15"/><circle cx="{fk2[0]:.1f}" cy="{fk2[1]:.1f}" r="11" fill="{FK}"/>')
    o.append(f'<g transform="translate({fk2[0] - 108:.1f} {fk2[1] + 26:.1f})">' + karte(0, 0, 118, 42, t(10, 17, "Neuer Anlass", 11.5, 700, TINTE) + t(10, 32, "Zweitwagen", 11, 500, GRAU)) + '</g>')
    # Faden in den Kreis
    o.append(f'<path d="M906 300 C 940 300 {fk2[0] - 30:.1f} {fk2[1]:.1f} {fk2[0]:.1f} {fk2[1]:.1f}" fill="none" stroke="{FK}" stroke-width="4" stroke-linecap="round"/>')
    # Familie K. im Netz (Start der Hauptfigur)
    o.append(f'<circle cx="{fk[0]}" cy="{fk[1]}" r="16" fill="#0b9fbd" opacity=".15"/><circle cx="{fk[0]}" cy="{fk[1]}" r="11" fill="{FK}"/>')
    o.append(f'<g transform="translate({fk[0] - 46} {fk[1] - 52})">' + karte(0, 0, 92, 30, t(46, 20, "Familie K.", 12, 700, TINTE, "middle")) + '</g>')
    # zurück zum Anfang
    o.append(f'<path d="M{fk2[0]:.1f} {fk2[1] + 80:.1f} V 470 H 148 V 396" fill="none" stroke="#3d5bd1" stroke-width="1.8" stroke-dasharray="5 6" marker-end="url(#gb-p)" opacity=".7"/>')
    o.append(t(560, 464, "Der nächste Anlass startet die nächste Strecke", 12, 600, "#3d5bd1", "middle"))
    # Ergebnisse
    for i, (a, b) in enumerate((("Fertig, im Look", "deiner Agentur."), ("Sichtbar bei Bauherren", "in der Region."), ("Aus dem Kontakt", "wird ein Termin."), ("Präsent im Bestand.", "Der nächste Anlass kommt."))):
        x = i * 300 + 20
        o.append(t(x, 506, a, 16, 700, TINTE, fam="Inter Tight") + t(x, 526, b, 16, 700, TINTE, fam="Inter Tight"))
    return f'<svg class="gb9" viewBox="0 0 {W} {H}" role="img" aria-label="Der Weg von Familie K.: Die Strecke steht fertig, Postings gehen ins Netz der Bauherren in der Region, Familie K. lädt die Checkliste, ein Anruf, ein Beratungstermin, Familie K. ist Kundin im Bestand, ein neuer Anlass startet die nächste Strecke.">{"".join(o)}</svg>'


if __name__ == "__main__":
    p = os.path.join(HERE, "story8.11tydata.json")
    d = json.load(open(p, encoding="utf-8"))
    d["s7"]["s9"]["grundbild"] = svg()
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    print("Grundbild geschrieben")
