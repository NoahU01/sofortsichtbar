#!/usr/bin/env python3
"""AVRG-Landingpage live schalten (Daniel, 22.11.2026).

Quelle ist Noahs Seite „Black Week 3.0“ (/zielgruppen/avrg-3/, Include src/_includes/avrg3/seite.njk) auf dem Branch daniel.
Daraus entsteht eine eigenständige Live-Seite unter /zielgruppen/avrg/ – genau dieser Look, aber:
  - links oben nur das sofort-sichtbar-Logo (ohne Link), keine Menüpunkte, kein Weg auf die Hauptseite
  - jeder Knopf „Termin auswählen“ öffnet die Terminbuchung (Cal.com) in einem neuen Tab
  - Kontaktbereich bleibt, Fußzeile nur mit Datenschutz und Impressum (Pflicht)
  - alle Bilder, Schriften, Skripte und die drei Landingpages im Konfigurator liegen als eigene Kopien unter
    src/static/zielgruppen/avrg/ – nichts verweist mehr auf /entwicklung/ (das gibt es auf main nicht).

Ablauf: npx @11ty/eleventy  →  python3 werkzeuge/avrg_live.py  →  npx @11ty/eleventy
Nach jeder Änderung an Noahs Seite oder den drei Landingpages erneut laufen lassen.
"""
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = f"{ROOT}/dist"
SRC = f"{ROOT}/src"
ZIEL_SEITEN = f"{SRC}/zielgruppen-avrg"
ZIEL_STATIC = f"{SRC}/static/zielgruppen/avrg"
URL = "/zielgruppen/avrg"
CAL = "https://cal.eu/sofortsichtbar/beratungstermin"
LOGO = "/entwicklung/storyboard/story6/assets/img/logo-dunkel.svg"

kopiert = {}


def asset_url(pfad):
    """/entwicklung/<bereich>/assets/<datei> → /zielgruppen/avrg/assets/<bereich>/<datei>, Datei wird kopiert."""
    pfad = pfad.split("?")[0].split("#")[0]
    m = re.match(r"/entwicklung/(.+?)/assets/(.+)$", pfad)
    if not m:
        raise SystemExit(f"Unbekannter Pfad: {pfad}")
    bereich, datei = m.group(1).replace("/", "-"), m.group(2)
    quelle = f"{SRC}/entwicklung/{m.group(1)}/assets/{datei}"
    if not os.path.isfile(quelle):
        raise SystemExit(f"Datei fehlt: {quelle}")
    ziel_url = f"{URL}/assets/{bereich}/{datei}"
    if ziel_url not in kopiert:
        ziel = f"{ZIEL_STATIC}/assets/{bereich}/{datei}"
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        kopiert[ziel_url] = quelle
        if quelle.endswith((".css", ".js", ".svg")):
            text = open(quelle, encoding="utf-8").read()
            if quelle.endswith(".css"):
                text = css_relativ(text, os.path.dirname(quelle))
            open(ziel, "w", encoding="utf-8").write(umschreiben(text))
        else:
            shutil.copyfile(quelle, ziel)
    return ziel_url


def css_relativ(text, ordner):
    """Relative url() in kopierten CSS-Dateien mitnehmen (z. B. Schriften neben der CSS-Datei)."""
    def ersetze(m):
        u = m.group(2)
        if u.startswith(("data:", "http", "/", "#")):
            return m.group(0)
        abs_quelle = os.path.normpath(os.path.join(ordner, u.split("?")[0].split("#")[0]))
        rel = os.path.relpath(abs_quelle, f"{SRC}")
        return f'url({m.group(1)}{asset_url("/" + rel)}{m.group(1)})'
    return re.sub(r"url\((['\"]?)([^'\")]+)\1\)", ersetze, text)


def umschreiben(text):
    text = text.replace("/entwicklung/kampagnen/avrg/landingpage-", f"{URL}/vorschau/landingpage-")
    return re.sub(r"/entwicklung/[A-Za-z0-9_./-]+?/assets/[A-Za-z0-9_./@-]+", lambda m: asset_url(m.group(0)), text)


def div_entfernen(html, anfang):
    """Entfernt ein <div …> samt Inhalt (verschachtelte divs werden mitgezählt)."""
    a = html.find(anfang)
    if a < 0:
        return html
    i, tiefe = a, 0
    for m in re.finditer(r"<div\b|</div>", html[a:]):
        tiefe += 1 if m.group(0) == "<div" else -1
        if tiefe == 0:
            return html[:a] + html[a + m.end():]
    raise SystemExit("div nicht geschlossen")


def kopf_live(html, titel, beschreibung, indexieren):
    k = html[: html.index("<style")]
    rest = html[html.index("<style"):]
    neu = ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           f"<title>{titel}</title>\n<meta name=\"description\" content=\"{beschreibung}\">\n"
           + ("{% if not env.isProduction %}<meta name=\"robots\" content=\"noindex,nofollow\">{% endif %}\n" if indexieren
              else '<meta name="robots" content="noindex,nofollow">\n')
           + '<link rel="canonical" href="{{ page.url | absoluteUrl(site.url) }}">\n'
           '<meta property="og:type" content="website">\n<meta property="og:site_name" content="sofort sichtbar">\n'
           f'<meta property="og:title" content="{titel}">\n<meta property="og:description" content="{beschreibung}">\n'
           '<meta property="og:url" content="{{ page.url | absoluteUrl(site.url) }}">\n<meta property="og:locale" content="de_DE">\n'
           '<link rel="icon" href="/assets/img/logos/favicon.png" type="image/png">\n'
           '<link rel="apple-touch-icon" href="/assets/img/logos/webclip.png">\n'
           + ('{% include "partials/head-scripts.njk" %}\n' if indexieren else ""))
    return neu, rest


def als_seite(permalink, kopf, rumpf, skripte_unten):
    return ("---\n" f"permalink: {permalink}\n" "layout: false\neleventyExcludeFromCollections: true\n---\n"
            "{#- Erzeugt von werkzeuge/avrg_live.py – nicht von Hand ändern. -#}\n"
            + kopf + "{% raw %}" + rumpf.replace("</body>", "{% endraw %}" + skripte_unten + "</body>", 1)
            + ("" if "</body>" in rumpf else "{% endraw %}"))


def hauptseite():
    html = open(f"{DIST}/zielgruppen/avrg-3/index.html", encoding="utf-8").read()
    # Kopf: nur Logo und Terminknopf
    a = html.index('<header class="s7-kopf">'); e = html.index("</header>", a) + len("</header>")
    kopfband = ('<header class="s7-kopf av9-live-kopf">\n<div class="s7-wrap">\n'
                f'<div class="s7-marke"><img src="{LOGO}" alt="sofort sichtbar" width="78" height="40"></div>\n'
                f'<a class="s7-knopf s7-kopf__termin" href="{CAL}" target="_blank" rel="noopener">Termin auswählen</a>\n'
                "</div>\n</header>")
    html = html[:a] + kopfband + html[e:]
    # Skripte für Menü und Entwicklungs-Dropdown fallen weg
    html = re.sub(r"<script>(?:(?!</script>).)*?(?:s7-burger|data-s7-dd)(?:(?!</script>).)*?</script>\s*", "", html, flags=re.S)
    # Terminbuchung statt Kontaktseite
    html = re.sub(r'href="/entwicklung/storyboard/story8/kontakt/"', f'href="{CAL}" target="_blank" rel="noopener"', html)
    # Fußzeile: Pflichtangaben absolut
    html = html.replace('href="/datenschutzerklarung"', 'href="/datenschutzerklarung/"').replace('href="/impressum"', 'href="/impressum/"')
    # Live-Kopf: im Entwicklungsstand ist der Terminknopf erst ab Desktop sichtbar – live auch mobil, dort ohne Menü daneben
    html = html.replace("</style>", "\n/* Live-Kopf ohne Menü (avrg_live.py) */\n.av9-live-kopf .s7-wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem}\n.av9-live-kopf .s7-kopf__termin{display:inline-flex}\n@media (max-width:600px){.av9-live-kopf .s7-kopf__termin{padding:.6rem 1.05rem;font-size:.9rem}}\n</style>", 1)
    html = re.sub(r"<!-- ENTWICKLUNG:START.*?(?:ENTWICKLUNG:END[^>]*-->|(?=</body>))", "", html, flags=re.S)
    html = umschreiben(html)
    reste = sorted(set(re.findall(r'(?:href|src)="(/(?!zielgruppen/avrg/|assets/img/logos/|datenschutzerklarung/|impressum/)[^"]*)"', html)))
    if reste:
        raise SystemExit("Noch Verweise auf andere Seiten: " + ", ".join(reste))
    rest_dev = sorted(set(re.findall(r"/entwicklung/[^\"'\s<)]*", html)))
    if rest_dev:
        raise SystemExit("Seite enthält noch Entwicklungsverweise: " + ", ".join(rest_dev[:10]))
    kopf, rest = kopf_live(html, "AVRG-Vertriebsstrecke für Agenturen und Makler · sofort sichtbar",
                           "Das Altersvorsorgedepot startet im Januar 2027. Mit der fertigen AVRG-Vertriebsstrecke bekommst du Landingpage, 40 Postings und 3 Mailings an deine Bestandskunden – in deinem Auftritt.", True)
    seite = als_seite(f"{URL}/index.html", kopf, rest, '{% include "partials/body-scripts.njk" %}\n')
    open(f"{ZIEL_SEITEN}/index.njk", "w", encoding="utf-8").write(seite)


def vorschau(nr):
    html = open(f"{DIST}/entwicklung/kampagnen/avrg/landingpage-{nr}/index.html", encoding="utf-8").read()
    html = div_entfernen(html, '<div class="lp-leiste"')
    # Entwicklungsblöcke (Variantenumschalter) gehören nicht auf die Live-Seite
    html = re.sub(r"<!-- ENTWICKLUNG:START.*?(?:ENTWICKLUNG:END[^>]*-->|(?=</body>))", "", html, flags=re.S)
    html = re.sub(r'href="/entwicklung/kampagnen/avrg/"', 'href="#"', html)
    html = umschreiben(html)
    reste = sorted(set(re.findall(r'(?:href|src)="(/(?!zielgruppen/avrg/|assets/img/logos/)[^"]*)"', html)))
    if reste:
        raise SystemExit(f"Landingpage {nr}: noch Verweise: " + ", ".join(reste))
    if "/entwicklung/" in html:
        raise SystemExit(f"Landingpage {nr}: Entwicklungsverweise übrig")
    for muster in ("data-dev-dd", "ENTWICKLUNG:START", "Nur in der Entwicklungsumgebung sichtbar", "/ Entwicklung /"):
        if muster in html:
            raise SystemExit(f"Landingpage {nr}: Entwicklungsinhalt übrig ({muster})")
    i = html.index("<head>") + len("<head>")
    html = html[:i] + '\n<meta name="robots" content="noindex,nofollow">' + html[i:]
    seite = ("---\n" f"permalink: {URL}/vorschau/landingpage-{nr}/index.html\n" "layout: false\neleventyExcludeFromCollections: true\n---\n"
             "{#- Erzeugt von werkzeuge/avrg_live.py – Vorschau für den Konfigurator der Live-Seite, nicht indexiert. -#}\n"
             "{% raw %}" + html + "{% endraw %}")
    open(f"{ZIEL_SEITEN}/vorschau-{nr}.njk", "w", encoding="utf-8").write(seite)


if __name__ == "__main__":
    if not os.path.isfile(f"{DIST}/zielgruppen/avrg-3/index.html"):
        sys.exit("Erst bauen: npx @11ty/eleventy")
    for d in (ZIEL_SEITEN, ZIEL_STATIC):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    hauptseite()
    for n in (1, 2, 3):
        vorschau(n)
    print(f"Live-Seite {URL}/ erzeugt, {len(kopiert)} Dateien kopiert:")
    for u in sorted(kopiert):
        print("  ", u)
