"""sofort sichtbar Avatar (Daniel, 16.11.2026): menschliche Züge, aber keine echte Person.
Maßstab: moderne Editorial-Porträtillustration, normale Proportionen nach Porträtregeln:
  Augen auf halber Kopfhöhe (Schädel bis Kinn), Nasenunterkante mittig zwischen Augen und Kinn, Mund ein Drittel darunter,
  Ohren von Braue bis Nase, Kopfbreite etwa zwei Drittel der Kopfhöhe, sichtbarer Hals, Schultern etwa drei Kopfbreiten, abfallend.
Kreis im Verlauf Cyan → Violett, Sakko in Tinte. Schreibt assets/team/avatar-frau.svg und assets/team/avatar-mann.svg.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HERE, "assets", "team")

# Kopf: Schädel 50 bis Kinn 130 (Höhe 80), Breite 56 (72 bis 128)
OBEN, KINN, L, R, M = 50, 130, 72, 128, 100
AUGE = (OBEN + KINN) / 2            # 90
NASE = (AUGE + KINN) / 2            # 110
MUND = NASE + (KINN - NASE) / 3     # 116.7
BRAUE = AUGE - 8                    # 82


def avatar(art):
    haut, schatten, lippe = ("#efcfb9", "#ddb197", "#c27a68") if art == "frau" else ("#e2b796", "#cc9b78", "#a96c58")
    haar, haarlicht = ("#2b211d", "#4a3830") if art == "frau" else ("#3b2a20", "#5a4232")
    kopf = (f"M{L} {OBEN + 32} C{L} {OBEN - 4} {R} {OBEN - 4} {R} {OBEN + 32} L{R} {NASE - 4} "
            f"C{R} {KINN - 10} {M + 12} {KINN} {M} {KINN} C{M - 12} {KINN} {L} {KINN - 10} {L} {NASE - 4} Z")
    g = []
    if art == "frau":   # Bob bis knapp unter das Kinn, hinter dem Kopf
        g.append(f'<path d="M66 {OBEN + 30} C62 {OBEN - 12} 138 {OBEN - 12} 134 {OBEN + 30} L137 {KINN + 4} C130 {KINN + 9} 122 {KINN + 8} 118 {KINN + 2} L82 {KINN + 2} C78 {KINN + 8} 70 {KINN + 9} 63 {KINN + 4} Z" fill="{haar}"/>')
    # Körper: abfallende Schultern, Sakko, Hemd
    g.append('<path d="M20 200 C22 176 36 166 58 160 L84 150 H116 L142 160 C164 166 178 176 180 200 Z" fill="#1d1d1f"/>')
    g.append('<path d="M86 150 L100 178 L114 150 Z" fill="#ffffff"/>')
    g.append('<path d="M82 151 L100 180 L88 172 L86 200 L72 200 C73 182 76 164 82 151 Z M118 151 L100 180 L112 172 L114 200 L128 200 C127 182 124 164 118 151 Z" fill="#3a3a3c"/>')
    # Hals
    g.append(f'<path d="M89 {KINN - 12} H111 V152 C106 158 94 158 89 152 Z" fill="{haut}"/>')
    g.append(f'<path d="M89 {KINN - 6} C94 {KINN + 6} 106 {KINN + 6} 111 {KINN - 6} V{KINN + 4} C105 {KINN + 12} 95 {KINN + 12} 89 {KINN + 4} Z" fill="{schatten}"/>')
    # Ohren (Braue bis Nase)
    oh = (NASE - BRAUE) / 2
    if art != "frau":   # bei der Frau liegen die Ohren unter dem Haar
        g.append(f'<ellipse cx="{L + 1}" cy="{(BRAUE + NASE) / 2}" rx="3.6" ry="{oh}" fill="{schatten}"/><ellipse cx="{R - 1}" cy="{(BRAUE + NASE) / 2}" rx="3.6" ry="{oh}" fill="{schatten}"/>')
    # Kopf mit Schattenseite
    g.append(f'<path d="{kopf}" fill="{haut}"/>')
    g.append(f'<path d="M112 {OBEN + 2} C122 {OBEN + 8} {R} {OBEN + 18} {R} {OBEN + 32} L{R} {NASE - 4} C{R} {KINN - 10} {M + 12} {KINN} {M} {KINN} '
             f'C{M + 10} {KINN - 8} 117 {NASE + 2} 117 {NASE - 10} C117 {OBEN + 30} 116 {OBEN + 14} 112 {OBEN + 2} Z" fill="{schatten}" opacity=".5"/>')
    # Haare vorn
    if art == "frau":   # Seitenscheitel, Stirn rechts frei
        g.append(f'<path d="M68 {AUGE + 18} C60 {OBEN} 98 {OBEN - 14} 120 {OBEN - 4} C132 {OBEN + 2} 138 {OBEN + 16} 134 {AUGE + 6} '
                 f'C132 {OBEN + 32} 124 {OBEN + 18} 110 {OBEN + 12} C106 {OBEN + 22} 92 {OBEN + 32} 76 {OBEN + 34} C72 {OBEN + 42} 70 {AUGE + 6} 68 {AUGE + 18} Z" fill="{haar}"/>')
        g.append(f'<path d="M106 {OBEN - 6} C118 {OBEN - 5} 128 {OBEN + 2} 131 {OBEN + 12} C124 {OBEN + 4} 116 {OBEN} 104 {OBEN} Z" fill="{haarlicht}"/>')
    else:               # kurz, Seiten kürzer
        g.append(f'<path d="M71.5 {AUGE - 6} C68 {OBEN + 2} 92 {OBEN - 9} 110 {OBEN - 6} C126 {OBEN - 3} 133 {OBEN + 8} 128.5 {AUGE - 6} '
                 f'C128 {OBEN + 22} 122 {OBEN + 14} 114 {OBEN + 12} C102 {OBEN + 8} 88 {OBEN + 10} 80 {OBEN + 16} C75 {OBEN + 22} 72 {OBEN + 30} 71 {AUGE - 2} Z" fill="{haar}"/>')
        g.append(f'<path d="M88 {OBEN - 3} C99 {OBEN - 7} 113 {OBEN - 6} 120 {OBEN} C111 {OBEN - 3} 100 {OBEN - 2} 89 {OBEN + 1} Z" fill="{haarlicht}"/>')
        g.append(f'<path d="M{L + 1} {NASE - 8} C{L + 3} {KINN - 6} {M - 12} {KINN + 1} {M} {KINN + 1} C{M + 12} {KINN + 1} {R - 3} {KINN - 6} {R - 1} {NASE - 8} '
                 f'C{R - 4} {MUND + 6} {M + 12} {MUND + 9} {M} {MUND + 9} C{M - 12} {MUND + 9} {L + 4} {MUND + 6} {L + 1} {NASE - 8} Z" fill="{haar}" opacity=".16"/>')
    # Brauen
    g.append(f'<path d="M80 {BRAUE + 2} C84 {BRAUE - 2} 91 {BRAUE - 2.5} 95 {BRAUE + 0.5}" fill="none" stroke="{haar}" stroke-width="2.6" stroke-linecap="round"/>'
             f'<path d="M105 {BRAUE + 0.5} C109 {BRAUE - 2.5} 116 {BRAUE - 2} 120 {BRAUE + 2}" fill="none" stroke="{haar}" stroke-width="2.6" stroke-linecap="round"/>')
    # Augen: Mandelform, Iris, Lidstrich
    for x in (88, 112):
        g.append(f'<path d="M{x - 6.5} {AUGE} C{x - 3.5} {AUGE - 4} {x + 3.5} {AUGE - 4} {x + 6.5} {AUGE} C{x + 3.5} {AUGE + 2.4} {x - 3.5} {AUGE + 2.4} {x - 6.5} {AUGE} Z" fill="#ffffff"/>'
                 f'<circle cx="{x}" cy="{AUGE - 0.4}" r="2.8" fill="#4a3428"/><circle cx="{x}" cy="{AUGE - 0.4}" r="1.3" fill="#111"/>'
                 f'<path d="M{x - 7} {AUGE} C{x - 3.5} {AUGE - 5} {x + 3.5} {AUGE - 5} {x + 7} {AUGE - 0.6}" fill="none" stroke="#1d1d1f" stroke-width="1.7" stroke-linecap="round"/>')
    # Nase (Schattenkante bis zur Nasenunterkante) und Mund
    g.append(f'<path d="M102 {AUGE + 4} C103 {AUGE + 10} 104.5 {NASE - 4} 104 {NASE - 1} C102.4 {NASE + 0.8} 99.4 {NASE + 1} 97.2 {NASE}" fill="none" stroke="{schatten}" stroke-width="2" stroke-linecap="round"/>')
    g.append(f'<path d="M92 {MUND} C95.5 {MUND - 1.6} 98.2 {MUND - 1} 100 {MUND - 0.2} C101.8 {MUND - 1} 104.5 {MUND - 1.6} 108 {MUND} C104.5 {MUND + 3.8} 95.5 {MUND + 3.8} 92 {MUND} Z" fill="{lippe}"/>'
             f'<path d="M92 {MUND} C96.5 {MUND + 1.2} 103.5 {MUND + 1.2} 108 {MUND}" fill="none" stroke="#8a4a3e" stroke-width="1" stroke-linecap="round"/>')
    if art == "mann":   # Brille mit schmalem Rand
        y = AUGE - 5
        g.append(f'<path d="M79 {y} h17 v4 a6 6 0 0 1-6 6 h-5 a6 6 0 0 1-6-6 z M104 {y} h17 v4 a6 6 0 0 1-6 6 h-5 a6 6 0 0 1-6-6 z M96 {y + 2} h8" '
                 'fill="none" stroke="#1d1d1f" stroke-width="1.8" stroke-linejoin="round"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><defs><linearGradient id="av-g" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient>'
            '<clipPath id="av-k"><circle cx="100" cy="100" r="96"/></clipPath></defs>'
            '<circle cx="100" cy="100" r="96" fill="url(#av-g)"/><g clip-path="url(#av-k)">' + "".join(g) + '</g></svg>')


if __name__ == "__main__":
    os.makedirs(ZIEL, exist_ok=True)
    for art in ("frau", "mann"):
        open(os.path.join(ZIEL, f"avatar-{art}.svg"), "w").write(avatar(art))
    print("Avatare geschrieben")
