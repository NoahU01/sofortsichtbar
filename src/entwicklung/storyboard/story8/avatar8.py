"""sofort sichtbar Avatar (Daniel, 16.11.2026): menschliche Züge, aber keine echte Person.
Maßstab: moderne Editorial-Porträtillustration – normale Proportionen (keine Kulleraugen, kein 3D), klare Flächen,
Gesichtszüge reduziert (Brauen, Augen, Nase, Mund), Business-Kleidung, Kreis im Verlauf Cyan → Violett.
Schreibt assets/team/avatar-frau.svg und assets/team/avatar-mann.svg.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HERE, "assets", "team")


def avatar(art):
    haut, schatten, lippe = ("#efcfb9", "#ddb197", "#c9806d") if art == "frau" else ("#e2b796", "#cc9b78", "#b3735d")
    haar, haarlicht = ("#2b211d", "#4a3830") if art == "frau" else ("#3b2a20", "#5a4232")
    o = []
    o.append('<defs><linearGradient id="av-g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient>'
             '<clipPath id="av-k"><circle cx="100" cy="100" r="96"/></clipPath></defs>')
    o.append('<circle cx="100" cy="100" r="96" fill="url(#av-g)"/>')
    g = []
    # Haare hinten (Frau: Bob bis zum Kinn)
    if art == "frau":
        g.append(f'<path d="M62 86 C58 40 142 40 138 86 L142 140 C134 146 126 146 120 142 L120 100 L80 100 L80 142 C74 146 66 146 58 140 Z" fill="{haar}"/>')
    # Schultern: Sakko in Tinte, Hemd weiß
    g.append('<path d="M22 200 C24 166 46 152 76 147 L124 147 C154 152 176 166 178 200 Z" fill="#1d1d1f"/>')
    g.append('<path d="M84 147 L100 176 L116 147 Z" fill="#ffffff"/>')
    g.append('<path d="M80 146 L100 180 L86 170 L84 200 L70 200 C70 178 74 160 80 146 Z M120 146 L100 180 L114 170 L116 200 L130 200 C130 178 126 160 120 146 Z" fill="#3a3a3c"/>')
    # Hals
    g.append(f'<path d="M86 122 H114 V150 C108 158 92 158 86 150 Z" fill="{haut}"/>')
    g.append(f'<path d="M86 128 C92 140 108 140 114 128 V138 C107 148 93 148 86 138 Z" fill="{schatten}"/>')
    # Ohren und Kopf
    g.append(f'<ellipse cx="69" cy="98" rx="6" ry="9" fill="{schatten}"/><ellipse cx="131" cy="98" rx="6" ry="9" fill="{schatten}"/>')
    g.append(f'<path d="M70 86 C70 52 130 52 130 86 L130 100 C130 124 116 140 100 140 C84 140 70 124 70 100 Z" fill="{haut}"/>')
    g.append(f'<path d="M112 56 C125 62 130 72 130 86 L130 100 C130 124 116 140 100 140 C112 132 118 118 118 100 C118 80 116 66 112 56 Z" fill="{schatten}" opacity=".55"/>')
    # Haare vorn
    if art == "frau":
        g.append(f'<path d="M66 112 C58 58 96 42 120 52 C132 57 140 70 136 104 C134 86 126 70 112 64 C110 72 96 84 76 88 C72 94 69 102 66 112 Z" fill="{haar}"/>')
        g.append(f'<path d="M108 52 C118 53 128 60 132 70 C124 62 116 58 106 58 Z" fill="{haarlicht}"/>')
    else:
        g.append(f'<path d="M69 90 C64 54 92 44 112 48 C128 51 136 64 131 90 C129 76 124 68 116 65 C104 61 88 63 80 70 C75 75 71 82 69 90 Z" fill="{haar}"/>')
        g.append(f'<path d="M86 54 C98 49 114 50 122 57 C112 54 100 55 88 59 Z" fill="{haarlicht}"/>')
        # Dreitagebart
        g.append(f'<path d="M73 104 C75 128 88 140 100 140 C112 140 125 128 127 104 C124 118 114 126 100 126 C86 126 76 118 73 104 Z" fill="{haar}" opacity=".28"/>')
    # Gesicht: Brauen, Augen, Nase, Mund
    g.append(f'<path d="M80 86 C85 82 92 82 96 85" fill="none" stroke="{haar}" stroke-width="3" stroke-linecap="round"/>'
             f'<path d="M104 85 C108 82 115 82 120 86" fill="none" stroke="{haar}" stroke-width="3" stroke-linecap="round"/>')
    for x in (88, 112):
        g.append(f'<path d="M{x - 7} 97 C{x - 4} 92.5 {x + 4} 92.5 {x + 7} 97 C{x + 4} 99.6 {x - 4} 99.6 {x - 7} 97 Z" fill="#ffffff"/>'
                 f'<circle cx="{x}" cy="96.4" r="3.1" fill="#3a2a22"/><circle cx="{x}" cy="96.4" r="1.4" fill="#111"/>'
                 f'<path d="M{x - 7.6} 97 C{x - 4} 91.6 {x + 4} 91.6 {x + 7.6} 96.4" fill="none" stroke="#1d1d1f" stroke-width="1.8" stroke-linecap="round"/>')
    g.append(f'<path d="M102 99 C103 104 104.5 108 104 111 C102.5 112.6 99.5 112.8 97.5 111.6" fill="none" stroke="{schatten}" stroke-width="2" stroke-linecap="round"/>')
    g.append(f'<path d="M91 121.5 C95 120 98 120.6 100 121.4 C102 120.6 105 120 109 121.5 C105 125.6 95 125.6 91 121.5 Z" fill="{lippe}"/>'
             f'<path d="M91 121.5 C96 122.8 104 122.8 109 121.5" fill="none" stroke="#8f4f42" stroke-width="1" stroke-linecap="round"/>')
    if art == "mann":
        g.append('<path d="M78 92 h18 v5 a6 6 0 0 1-6 6 h-6 a6 6 0 0 1-6-6 z M104 92 h18 v5 a6 6 0 0 1-6 6 h-6 a6 6 0 0 1-6-6 z M96 94 h8" '
                 'fill="none" stroke="#1d1d1f" stroke-width="2.2" stroke-linejoin="round"/>')
    o.append('<g clip-path="url(#av-k)">' + "".join(g) + '</g>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">' + "".join(o) + '</svg>'


if __name__ == "__main__":
    os.makedirs(ZIEL, exist_ok=True)
    for art in ("frau", "mann"):
        open(os.path.join(ZIEL, f"avatar-{art}.svg"), "w").write(avatar(art))
    print("Avatare geschrieben")
