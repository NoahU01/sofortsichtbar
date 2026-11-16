"""Kopfbild Story 8 – drei Varianten der Zweiteilung (Daniel, 16.11.2026):
Trichter bündig links unter „Marketing“, kein Rückweg-Pfeil, Begriffe innen wie im Vertriebsband,
jede Stufe als eigene Gruppe (.tr-aufbauen / .tr-betreiben), damit sie sich einzeln ausgrauen lässt.
  v1  Bogen-Fuge: eine weiche, nach rechts gewölbte Fuge durch alle Lagen – folgt der Strömung
  v2  Zwei Kapseln: nur der farbige Kern ist geteilt, mit runden Enden; die grauen Lagen laufen durch
  v3  Durchgehend: der Trichter bleibt ganz, die Teilung steht in der Klammer darüber (wie beim Vertrieb)
Schreibt s7.ek_varianten = {"v1": svg, "v2": svg, "v3": svg} in story8.11tydata.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "story7"))
import erklaerbild as eb  # noqa: E402

text, svg = eb.text, eb.svg
K, G = 15, 20
W, c = 1120, 196
X_FLACH, X_KURVE, X_HALS = 250, 450, 510
X_TEIL = 262
MUND = [50, 74, 96, 118]
HALS = [24, 30, 36, 40]
LU = eb.LUECKE


def bez(p0, p1, p2, p3, t):
    return tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * cc + t ** 3 * d for a, b, cc, d in zip(p0, p1, p2, p3))


def halbe(k, x):
    """halbe Höhe der Lage k an der Stelle x"""
    hm, hh = MUND[k], HALS[k]
    if x <= X_FLACH:
        return hm
    if x >= X_KURVE:
        return hh
    p = [(X_FLACH, hm), (X_FLACH + 130, hm), (X_KURVE - 100, hh), (X_KURVE, hh)]
    lo, hi = 0.0, 1.0
    for _ in range(40):
        m = (lo + hi) / 2
        if bez(*p, m)[0] < x:
            lo = m
        else:
            hi = m
    return bez(*p, lo)[1]


def lage(k):
    hm, hh = MUND[k], HALS[k]
    return (f"M0 {c - hm} H{X_FLACH} C{X_FLACH + 130} {c - hm} {X_KURVE - 100} {c - hh} {X_KURVE} {c - hh} H{X_HALS} "
            f"V{c + hh} H{X_KURVE} C{X_KURVE - 100} {c + hh} {X_FLACH + 130} {c + hm} {X_FLACH} {c + hm} H0 Z")


def kern_stueck(x0, x1, rund_links, rund_rechts):
    """Abschnitt des Kerns zwischen x0 und x1, Enden auf Wunsch rund (Kapsel)"""
    n = 24
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    oben = [(x, c - halbe(0, x)) for x in xs]
    unten = [(x, c + halbe(0, x)) for x in reversed(xs)]
    r1, r0 = halbe(0, x1), halbe(0, x0)
    d = f"M{oben[0][0]:.1f} {oben[0][1]:.1f} " + " ".join(f"L{x:.1f} {y:.1f}" for x, y in oben[1:])
    d += (f" A{r1 * .55:.1f} {r1:.1f} 0 0 1 {unten[0][0]:.1f} {unten[0][1]:.1f}" if rund_rechts else f" L{unten[0][0]:.1f} {unten[0][1]:.1f}")
    d += " " + " ".join(f"L{x:.1f} {y:.1f}" for x, y in unten[1:])
    # links rund: konkav (Bogen nach rechts eingezogen), damit die Kapsel die vorige aufnimmt statt sie zu überlappen
    d += (f" A{r0 * .55:.1f} {r0:.1f} 0 0 0 {oben[0][0]:.1f} {oben[0][1]:.1f}" if rund_links else " Z")
    return d + (" Z" if rund_links else "")


def kopf(o, geteilt_oben=False):
    if geteilt_oben:   # v3: die Linie unter „Marketing“ ist in zwei Abschnitte geteilt – wie die zwei Blöcke im Vertrieb
        o.append(text(0, 20, "Marketing – wir gewinnen Interessenten", "ek2-t", K, 600))
        o.append(f'<path d="M0 34 H{X_TEIL - 5} M{X_TEIL + 5} 34 H{X_HALS}" class="ek2-linie"/>')
    else:
        o.append(text(0, 20, "Marketing – wir gewinnen Interessenten", "ek2-t", K, 600))
        o.append(f'<path d="M0 34 H{X_HALS}" class="ek2-linie"/>')
    o.append(text(X_HALS + LU, 20, "Vertrieb – du machst daraus Kunden", "ek2-t", K, 600))
    o.append(f'<path d="M{X_HALS + LU} 34 H{W}" class="ek2-linie"/>')


def vertrieb(o):
    xm = X_HALS + LU / 2
    o.append(f'<path d="M{xm} {c - HALS[3]} V{c - HALS[3] - 34}" class="ek2-linie ek2-linie--fein"/>')
    o.append(text(xm, c - HALS[3] - 42, "Messpunkt: Leads", "ek2-t", K, 700, "middle"))
    y0, y1 = c - HALS[3], c + HALS[3]
    xv = X_HALS + LU
    o.append(f'<path d="M{xv} {y0} H806 L828 {c} L806 {y1} H{xv} Z" class="ek2-band"/>')
    o.append(f'<path d="M818 {y0} H{W - 16} Q{W} {y0} {W} {y0 + 16} V{y1 - 16} Q{W} {y1} {W - 16} {y1} H818 L840 {c} Z" class="ek2-band"/>')
    for x, titel, unter in ((xv + 26, "Vertrieb", "Ansprechen · Terminieren · Beraten"), (866, "Betreuen", "Bestand halten und ausbauen")):
        o.append(text(x, c - 3, titel, "ek2-band-t", G, 700))
        o.append(text(x, c + 21, unter, "ek2-band-s", K))


def beschriftung(o, v):
    """Begriffe im farbigen Kern – wie im Vertriebsband: Titel und Zeile darunter"""
    xa, xb = 26, X_TEIL + (30 if v != 3 else 26)
    o.append(f'<g class="tr-aufbauen tr-text">{text(xa, c - 3, "Aufbauen", "ek2-kern-t", G, 700)}{text(xa, c + 21, "Zielgruppen, Kanäle, Medien", "ek2-kern-s", K)}</g>')
    o.append(f'<g class="tr-betreiben tr-text">{text(xb, c - 3, "Betreiben", "ek2-kern-t", G, 700)}{text(xb, c + 21, "Posten, vernetzen, nachhalten", "ek2-kern-s", 13.5)}</g>')


def variante(v):
    o = []
    kopf(o, geteilt_oben=(v == 3))
    clip = (f'<defs><clipPath id="tr{v}-a"><rect x="-10" y="0" width="{X_TEIL + 10}" height="400"/></clipPath>'
            f'<clipPath id="tr{v}-b"><rect x="{X_TEIL - .6}" y="0" width="{X_HALS - X_TEIL + 10}" height="400"/></clipPath></defs>')
    o.append(clip)
    if v in (1, 3):
        if v == 3:   # ungeteilt darunter, damit an der Grenze keine feine Naht sichtbar wird
            o.append('<g class="tr-unten">' + "".join(f'<path d="{lage(k)}" class="{eb.LAGEN[k][0]} ek2-lage"/>' for k in (3, 2, 1, 0)) + '</g>')
        for teil, cid in (("tr-aufbauen", "a"), ("tr-betreiben", "b")):
            g = "".join(f'<path d="{lage(k)}" class="{eb.LAGEN[k][0]} ek2-lage"/>' for k in (3, 2, 1, 0))
            o.append(f'<g class="{teil}{" tr-teil" if v == 3 else ""}" clip-path="url(#tr{v}-{cid})">{g}</g>')
        if v == 1:   # weiche Fuge, nach rechts gewölbt wie die Strömung
            yo, yu = c - MUND[3] - 2, c + MUND[3] + 2
            o.append(f'<path d="M{X_TEIL - 10} {yo} C{X_TEIL + 14} {c - 50} {X_TEIL + 14} {c + 50} {X_TEIL - 10} {yu}" class="ek2-fuge"/>')
    else:        # v2: graue Lagen durchgehend, nur der Kern in zwei Kapseln
        o.append("".join(f'<path d="{lage(k)}" class="{eb.LAGEN[k][0]} ek2-lage"/>' for k in (3, 2, 1)))
        o.append(f'<path d="{lage(0)}" class="ek2-l2"/>')
        o.append(f'<g class="tr-aufbauen"><path d="{kern_stueck(0, X_TEIL - 14, False, True)}" class="ek2-kern"/></g>')
        o.append(f'<g class="tr-betreiben"><path d="{kern_stueck(X_TEIL - 6, X_HALS, True, False)}" class="ek2-kern"/></g>')
    beschriftung(o, v)
    vertrieb(o)
    return svg(W, c + MUND[3] + 6, "".join(o), "ek2-svg--quer ek2-var", f"v{v}")


if __name__ == "__main__":
    p = os.path.join(HERE, "story8.11tydata.json")
    d = json.load(open(p, encoding="utf-8"))
    d["s7"]["ek_varianten"] = {f"v{v}": variante(v) for v in (1, 2, 3)}
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")
    print("drei Varianten geschrieben")
