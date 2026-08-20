# sofort sichtbar – Website

Statische Website, gebaut mit [Eleventy](https://www.11ty.dev/) (Nunjucks-Templates,
handgeschriebenes CSS, Vanilla-JS). Keine Frameworks im Browser, kein Webflow-Runtime.

Die Startseite ist ein 1:1-Nachbau von `https://www.sofortsichtbar.de/` – auf allen
geprüften Breakpoints (1440 / 1280 / 1024 / 991 / 768 / 480 / 390 / 375 / 320 px)
stimmen Position und Größe aller Sektionen sowie die Gesamthöhe der Seite exakt überein.

## Loslegen

```bash
npm install
npm run dev     # Dev-Server auf http://localhost:8181 (mit Live-Reload)
npm run build   # Produktions-Build nach dist/
npm run clean   # dist/ löschen
```

## Struktur

```
src/
├── _data/
│   ├── site.json          globale Daten: Navigation, Footer, Kontakt, Social
│   └── home.json          Inhalte der Startseite (Texte, Preise, FAQ, Slider)
├── _includes/
│   ├── layouts/base.njk   HTML-Gerüst, Meta-Tags, Font- und Asset-Einbindung
│   ├── partials/          nav, footer, Icon-Snippets, Tracking-Platzhalter
│   └── sections/          eine Datei pro Sektion der Startseite
├── assets/
│   ├── css/               nummerierte Basis-Module + sections/ (eine Datei pro Sektion)
│   ├── js/main.js         Navigation, Pricing-Tabs, FAQ, Marquee, Scroll-Reveal
│   └── img/               logos/, icons/, themes/ und Inhaltsbilder
├── static/robots.txt      wird unverändert nach dist/ kopiert
├── index.njk              Startseite (setzt die Sektionen zusammen)
└── 404.njk
```

**Inhalte stehen in `src/_data/`, nicht im Markup.** Texte, Preise und FAQ-Einträge
ändert man dort; die Templates rendern nur.

**CSS** liegt bewusst in kleinen Modulen. Der Eleventy-Build bündelt sie beim
Schreiben von `dist/` zu einer einzigen `assets/css/main.css` – eine Anfrage,
keine Import-Kette. Reihenfolge: `01-tokens` … `07-footer`, danach `sections/*`
alphabetisch. Neue Datei anlegen genügt, sie wird automatisch mitgebündelt.

**Farben, Abstände und Radien** kommen aus den Custom Properties in
`src/assets/css/01-tokens.css`.

**Breakpoints** folgen dem Original: `991px`, `767px`, `479px` (Desktop-First).

## Tracking

Noch nicht eingebaut. Die beiden Einhängepunkte stehen bereit:

- `src/_includes/partials/head-scripts.njk` – alles, was in den `<head>` gehört
  (Consent-Banner, Google Tag Manager, Pixel)
- `src/_includes/partials/body-scripts.njk` – alles direkt nach `<body>`
  (z. B. der GTM-`noscript`-Fallback)

Alle Sektionen haben IDs (`#problem`, `#solution`, `#themen`, `#vergleich`,
`#pricing`, `#support`, `#faq`, `#kontakt`), die sich als Tracking-Anker und
Sprungziele nutzen lassen.

## Bekannte Abweichungen zum Original

- Das Burger-Icon ist eine CSS-Animation statt einer Lottie-Datei
  (gleiche Maße, gleiche Darstellung, ~30 kB weniger).
- Die Bilder des Themen-Sliders wurden auf Anzeigegröße verkleinert und in WebP
  konvertiert (3,5 MB → 0,4 MB) – optisch identisch.
- Das Cookie-Banner (Usercentrics/Cookiebot) fehlt, weil es zum Tracking-Setup gehört.

## Noch offen

Die Unterseiten (`/vertriebsstrecken`, `/pricing`, `/vetriebsleiter`, `/kontakt`,
`/impressum`, `/datenschutzerklarung`, `/zielgruppen/*`) sind noch nicht gebaut –
die Links in Navigation und Footer zeigen bereits darauf.
