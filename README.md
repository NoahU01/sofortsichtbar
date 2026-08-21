# sofort sichtbar – Website

Statische Website, gebaut mit [Eleventy](https://www.11ty.dev/) (Nunjucks-Templates,
handgeschriebenes CSS, Vanilla-JS). Keine Frameworks im Browser, keine Webflow-Runtime.

Nachbau von `https://www.sofortsichtbar.de/` – alle 27 Seiten. Abgenommen wird nicht
nach Augenmaß, sondern gemessen: beide Seiten werden mit Puppeteer geladen und für
jede Sektion Position und Größe verglichen, dazu die Gesamthöhe der Seite. Geprüfte
Breiten: 1440 / 1280 / 1024 / 991 / 768 / 480 / 390 / 375 / 320 px.

## Loslegen

```bash
npm install
npm run dev     # Dev-Server auf http://localhost:8181 (mit Live-Reload)
npm run build   # Produktions-Build nach dist/
npm run clean   # dist/ löschen
```

## Seiten

| Pfad | Inhalt |
|---|---|
| `/` | Startseite |
| `/vertriebsstrecken` | Themen-Übersicht mit Filter (Zielgruppen / Anspracheanlässe) |
| `/pricing` | Pakete plus technischer Vergleich |
| `/vetriebsleiter` | Seite für Führungskräfte |
| `/kontakt` | Kontakt mit Cal.com-Terminbuchung |
| `/zielgruppen/<slug>` | 20 Zielgruppen-Detailseiten aus einem Template |
| `/impressum`, `/datenschutzerklarung` | Rechtstexte |
| `/styleguide` | interne Design-Referenz (`noindex`) |
| `/404.html`, `/sitemap.xml`, `/robots.txt` | |

## Struktur

```
src/
├── _data/                 alle Inhalte als JSON
│   ├── site.json          Navigation, Footer, Kontaktdaten, Social
│   ├── home.json          Startseite
│   ├── faq.json           FAQ (Startseite, /pricing, /kontakt)
│   ├── pricing.json       Pakete (Startseite und /pricing)
│   ├── pricingOverview.json   technischer Vergleich
│   ├── vertriebsstrecken.json Themenliste und Filter
│   ├── vertriebsleiter.json
│   ├── kontakt.json
│   ├── zielgruppen.json       die 20 Detailseiten
│   └── zielgruppenShared.json was auf allen 20 gleich ist
├── _includes/
│   ├── layouts/           base.njk, legal.njk
│   ├── partials/          nav, footer, Icons, Cal-Embed, Tracking-Platzhalter
│   ├── sections/          eine Datei pro Sektion
│   └── legal/             Rechtstexte als HTML
├── assets/
│   ├── css/               nummerierte Basis-Module + sections/
│   ├── js/main.js         Navigation, Tabs, FAQ, Marquee, Themen-Filter, Reveal
│   └── img/               logos/, icons/, themes/, zielgruppen/, pages/
├── static/                robots.txt
├── index.njk · pricing.njk · kontakt.njk · …
├── zielgruppen.njk        erzeugt alle 20 Detailseiten (Eleventy-Pagination)
└── sitemap.njk
```

**Inhalte stehen in `src/_data/`, nicht im Markup.** Texte, Preise, FAQ-Einträge und
Zielgruppen ändert man dort; die Templates rendern nur. Eine neue Zielgruppe braucht
einen Eintrag in `zielgruppen.json` – Seite, Sitemap und Verlinkung entstehen daraus.

**CSS** liegt in kleinen Modulen. Der Build bündelt sie zu einer `assets/css/main.css` –
eine Anfrage, keine Import-Kette. Reihenfolge: `01-tokens` … `07-footer`, danach
`sections/*` alphabetisch. Neue Datei anlegen genügt.

**Farben, Abstände und Radien** kommen aus `src/assets/css/01-tokens.css`.
`/styleguide` zeigt alles gerendert.

**Breakpoints** wie im Original: `991px`, `767px`, `479px` (Desktop-First).

## Tracking

Noch nicht eingebaut. Die Einhängepunkte stehen bereit:

- `src/_includes/partials/head-scripts.njk` – alles für den `<head>`
  (Consent-Banner, Google Tag Manager, Pixel)
- `src/_includes/partials/body-scripts.njk` – alles direkt nach `<body>`
  (z. B. GTM-`noscript`)

Alle Sektionen haben IDs als Tracking-Anker und Sprungziele. Der Cal.com-Embed in
`partials/cal-embed.njk` lädt ein Drittanbieter-Script und gehört beim Tracking-Setup
hinter die Consent-Abfrage.

## Details, die leicht kippen

- **`-webkit-font-smoothing` bleibt auf `auto`.** Auf `antialiased` gesetzt rendert
  macOS die Schrift sichtbar dünner als das Original (rund 8 % weniger Deckung).
  Headless-Screenshots zeigen den Unterschied nicht – nur echtes Chrome.
- **Kein `scroll-margin-top` auf Ankerzielen.** Die Navigation ist nicht fixiert;
  ein Versatz würde die Sprungziele gegenüber dem Original verschieben.

## Bewusste Abweichungen zum Original

- **Burger-Icon** als CSS statt Lottie – gleiche Maße, ~30 kB weniger.
- **Bilder** als WebP und auf Anzeigegröße verkleinert (30 MB → 6 MB), optisch identisch.
- **Cookie-Banner und Cookiebot-Cookie-Erklärung** fehlen – gehören zum Tracking-Setup.
  Dadurch ist `/datenschutzerklarung` um genau den Block kürzer, in dem die Erklärung steht.
- **Seitentitel der Zielgruppen-Seiten**: im Original heißen alle 20 `sofort sichtbar`.
  Hier trägt jede ihren eigenen Titel, sonst konkurrieren 20 identische Seiten in der Suche.
- **Überschriften-Ebenen**: `/pricing` bekommt eine `h1` (im Original beginnt die
  Seite mit `h2`). Rein semantisch, optisch unverändert.
- **`/styleguide`**: im Original die unveränderte Client-First-Demo von Webflow, die
  nirgends verlinkt ist. Hier stattdessen eine Referenz der tatsächlich genutzten
  Tokens und Komponenten.
- **Aktiver Filter auf `/vertriebsstrecken`** ist immer fett *und* unterstrichen.
  Im Original verliert er beim Umschalten das Fett (die Klasse landet dort nur auf
  dem äußeren Element) – hier bleibt es konsistent.
- **Lightbox auf den Zielgruppen-Seiten**: im Original vorhanden, aber dauerhaft
  `display:none` und ohne Klick-Handler – also nicht übernommen.
