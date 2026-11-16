#!/usr/bin/env python3
"""PDF „Selbst machen“ (Daniel, 16.11.2026: Download auf beiden Unterseiten, Rollen gehören ins PDF).

SCHRIFTSYSTEM (fest, übernommen aus story7/maas_pdf7.py – dasselbe Deckblatt-System):
  Inter Tight 700  – H1 44 pt (Deckblatt, Kontakt), H2 22 pt (alle übrigen Seiten, auch große Zahlen)
  Inter 400/600    – Text 10 pt, Klein 8 pt für Kicker, Nebeninfos, Fußzeile
  Farben           – Tinte #1d1d1f, Grau #6e6e73; Verlauf Cyan → Violett höchstens einmal je Seite

Seitenfolge: Deckblatt · Warum Selbst machen (Trichter, drei Punkte) · Wer macht was · Was dein Team bekommt ·
             Start und Pakete · Kontakt
Inhalte: story8.11tydata.json (s7) – dieselben Quellen wie die Unterseite.
Aufruf:  python3 src/entwicklung/storyboard/story8/selbst_pdf8.py
Ergebnis: story8/assets/team/selbst-machen.pdf, -1.png/-2.png; Seitenzahl/Größe in s7.weg_a.download
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "story7"))
import maas_pdf7 as mp  # noqa: E402

e, grad, seite, kopf = mp.e, mp.grad, mp.seite, mp.kopf
D8 = os.path.join(HERE, "story8.11tydata.json")
ZIEL = os.path.join(HERE, "assets", "team")

CSS_ZUSATZ = r'''
/* Selbst machen: Betreiben ausgegraut, Begriff bleibt lesbar */
.aus .tr-betreiben:not(.tr-text) { opacity: .32; }
.aus .tr-betreiben .ek2-kern { fill: #b9b9c0; }
.aus .tr-text.tr-betreiben .ek2-kern-t { fill: #1d1d1f; }
.aus .tr-text.tr-betreiben .ek2-kern-s { fill: #6e6e73; }
.ek2-kern-s { fill: rgba(255,255,255,.85); }
.ek2-fuge { fill: none; stroke: #fff; stroke-width: 6; stroke-linecap: round; }
.passt { margin-top: 8mm; padding: 5mm 6mm; border-radius: 4mm; background: #f5f5f7; font-weight: 600; }
/* Wer macht was */
.rl-gruppe { margin-top: 7mm; padding-bottom: 2mm; border-bottom: 0.6mm solid #1d1d1f; font-weight: 600; }
.rl-zeile { display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; padding: 3.5mm 0; border-bottom: 0.3mm solid #e5e5ea; break-inside: avoid; }
.rl-zeile p.klein { margin-top: .8mm; }
.wer { display: inline-block; margin-bottom: 1.4mm; padding: .8mm 2.6mm; border: 0.3mm solid #d2d2d7; border-radius: 4mm; font-size: 8pt; font-weight: 600; }
.wer.wir { border-color: #1d1d1f; background: #1d1d1f; color: #fff; }
/* Pakete */
.pk { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; margin-top: 6mm; }
.pk > div { padding: 6mm; border: 0.3mm solid #d2d2d7; border-radius: 4mm; break-inside: avoid; }
.pk .preis { margin: 3mm 0; }
.pk .preis b { font-family: "Inter Tight"; font-weight: 700; font-size: 22pt; letter-spacing: -0.02em; }
'''


def bauen(seiten_zahl="6"):
    d = json.load(open(D8, encoding="utf-8"))
    S = d["s7"]
    A = S["weg_a"]
    imgL = os.path.join(mp.SRC, "assets", "img")
    img6 = os.path.join(mp.SRC, "entwicklung", "storyboard", "story6", "assets", "img")
    logo_hell = f'file://{imgL}/logos/logo-white.svg'
    s = []

    # 1 · Deckblatt (dunkles Deckblatt-System: wechseln nur Art, Titel, Satz, drei Punkte)
    s.append(seite(
        f'<div class="c-kopf"><span class="c-art">Angebot und Leistungen</span><img class="logo" src="{logo_hell}" alt="sofort sichtbar"></div>'
        f'<h1>Selbst<br>{grad("machen.")}</h1>'
        '<p class="c-satz">Fertige Vertriebsstrecken für dein Team – für Versicherungsagenturen und Maklerbüros.</p>'
        '<div class="c-karte"><p class="lbl">Was dich erwartet</p><ol>'
        '<li><span>01</span>Warum dein Team mit uns schneller ist</li>'
        '<li><span>02</span>Wer welche Stufe übernimmt</li>'
        '<li><span>03</span>Der Start und die Pakete mit Preisen</li></ol>'
        f'<p class="meta"><span>PDF · {seiten_zahl} Seiten</span><b>sofortsichtbar.de</b></p></div>', "voll cover"))

    # 2 · Warum Selbst machen
    MW = A["mehrwert"]
    drei = "".join(f'<div><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in MW["punkte"])
    s.append(seite(
        kopf(MW["kicker"], f'{e(MW["h2"])}<br>{grad(e(MW["h2_akzent"]))}')
        + f'<p class="lead">{e(A["held"]["lead"])}</p>'
        + f'<div class="buehne aus">{S["ek_kopf"]}</div>'
        + f'<div class="drei">{drei}</div><p class="passt">{e(MW["passt"])}</p>'))

    # 3 · Wer macht was (nur Spalte Selbst machen)
    R = S["rollen"]
    T = R["seite"]["a"]
    tab = ""
    for g in R["gruppen"]:
        tab += f'<p class="rl-gruppe">{e(g["titel"])}</p>'
        for z in g["zeilen"]:
            art, txt = z["a"]
            wer = "sofort sichtbar" if art == "wir" else ("Dein Team" if z["stufe"] == "Betreiben" else "Deine Agentur")
            tab += (f'<div class="rl-zeile"><div><h3>{e(z["stufe"])}</h3><p class="klein">{e(z["was"])}</p></div>'
                    f'<div><span class="wer{" wir" if art == "wir" else ""}">{wer}</span>' + (f'<p>{e(txt)}</p>' if txt else "") + '</div></div>')
    s.append(seite(kopf(R["kicker"], e(T["h2"])) + f'<p class="lead">{e(T["lead"])}</p>' + tab))

    # 4 · Was dein Team bekommt
    ST = A["stufen"]
    teile = ""
    for x in ST["liste"]:
        chips = ""
        if x.get("teile"):
            chips = '<div class="reihe">' + "".join(f'<span class="chip an">{e(t["name"])}</span>' for t in x["teile"]) + '</div>'
        teile += (f'<div class="teil"><span class="nr">{e(x["nr"])}</span><div><p class="kicker">{e(x["label"])}</p>'
                  f'<h3>{e(x["h"])}</h3><p>{e(x["t"])}</p>{chips}</div></div>')
    s.append(seite(kopf(ST["kicker"], f'{e(ST["h2"])} {grad(e(ST["h2_akzent"]))}') + f'<p class="lead">{e(ST["lead"])}</p>' + teile))

    # 5 · Start und Pakete
    SR = A["start"]
    wochen = "".join(f'<div class="woche"><div><span class="w">{e(x["wann"].replace("Schritt ", ""))}</span><p class="klein">Schritt</p></div>'
                     f'<div><h3>{e(x["titel"])}</h3><p>{e(x["text"])}</p></div></div>' for x in SR["liste"])
    pk = ""
    for p in S["pakete"]["liste"]:
        if p["id"] == "komplett":
            continue
        preis = p["preis"] or "Auf Anfrage"
        pk += (f'<div><h3 style="font-family:Inter Tight;font-size:22pt;letter-spacing:-0.02em">{e(p["name"])}</h3><p class="klein">{e(p["fuer"])}</p>'
               f'<p class="preis"><b>{e(preis)}</b> <span class="klein">{e(p["einheit"])}</span></p><p>{e(p["vorspann"])}</p>'
               '<ul class="haken" style="margin-top:2mm">' + "".join(f"<li>{e(y)}</li>" for y in p["punkte"]) + '</ul></div>')
    s.append(seite(kopf(SR["kicker"], e(SR["h2"])) + f'<p class="lead">{e(SR["lead"])}</p><div class="wochen">{wochen}</div>'
                   + f'<p class="rl-gruppe" style="margin-top:10mm">Die Pakete</p><div class="pk">{pk}</div>'))

    # 6 · Kontakt
    gesichter = "".join(f'<img src="file://{img6}/ansprechpartner-{n}.webp" alt="">' for n in ("kerstin", "daniel", "noah"))
    s.append(seite(
        f'<img class="logo" src="{logo_hell}" alt="sofort sichtbar">'
        + f'<p class="kicker" style="margin-top:40mm">Kontakt</p><h1>Lass uns sprechen.<br>{grad("Ganz konkret.")}</h1>'
        + f'<p class="lead">{e(S["kontaktseite"]["lead"])}</p>'
        + f'<div class="gesichter"><span>{gesichter}</span>{e(S["kontakt"]["team_satz"])}</div>'
        + f'<div class="wege"><span class="klein">Termin auswählen</span><b>sofortsichtbar.de/kontakt</b>'
        + f'<span class="klein" style="margin-top:3mm">Lieber direkt?</span><b>{e(S["kontakt"]["mail"])}</b><b>{e(S["kontakt"]["tel"])}</b></div>',
        "voll dunkel kontakt"))

    css = mp.css().replace("sofort sichtbar · Marketing as a Service", "sofort sichtbar · Selbst machen") + CSS_ZUSATZ
    dok = (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Selbst machen – sofort sichtbar</title>'
           f'<style>{css}</style></head><body>{mp.SVG_CSS}{"".join(s)}{mp.VERLAUF_JS}</body></html>')
    return dok, d


def drucken(dok, pdf):
    tmp = tempfile.mkdtemp(prefix="selbst8_")
    h = os.path.join(tmp, "selbst.html")
    open(h, "w", encoding="utf-8").write(dok)
    for _ in range(3):
        r = subprocess.run([mp.CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                            "--virtual-time-budget=6000", f"--print-to-pdf={pdf}", "file://" + h], capture_output=True)
        if r.returncode == 0 and os.path.exists(pdf):
            break
    return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))


def main():
    os.makedirs(ZIEL, exist_ok=True)
    pdf = os.path.join(ZIEL, "selbst-machen.pdf")
    dok, _ = bauen()
    n = drucken(dok, pdf)
    dok, d = bauen(str(n))          # zweiter Lauf mit der echten Seitenzahl auf dem Deckblatt
    n = drucken(dok, pdf)
    groesse = f'{os.path.getsize(pdf) / 1e6:.1f} MB'.replace(".", ",")
    for k in (1, 2):
        subprocess.run(["pdftoppm", "-r", "110", "-png", "-f", str(k), "-l", str(k), "-singlefile", pdf, os.path.join(ZIEL, f"selbst-machen-{k}")], check=True)
    stempel = hashlib.md5(open(pdf, "rb").read()).hexdigest()[:8]
    d["s7"]["weg_a"]["download"].update({"meta": ["PDF", f"{n} Seiten", groesse], "pfad": "/entwicklung/storyboard/story8/assets/team",
                                         "datei": "selbst-machen.pdf?v=" + stempel, "bild1": "selbst-machen-1.png?v=" + stempel,
                                         "bild2": "selbst-machen-2.png?v=" + stempel})
    json.dump(d, open(D8, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(D8, "a").write("\n")
    print(pdf, n, "Seiten", groesse)


if __name__ == "__main__":
    main()
