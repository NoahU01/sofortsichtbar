# sofort sichtbar

Eleventy-Projekt, Quellcode in `src/`, Build nach `dist/`. Deploy über Vercel.

## Branches

| Branch   | Zweck                                                              |
| -------- | ------------------------------------------------------------------ |
| `main`   | geht live auf https://www.sofortsichtbar.de                          |
| `daniel` | Entwicklungsbranch, Preview: https://sofortsichtbar-git-daniel-empiria-gmb-h.vercel.app |

## Harte Regel: "/ Entwicklung /" bleibt auf `daniel`

Der Navigationspunkt **"/ Entwicklung /"** und alle Seiten unter `/entwicklung/`
sind Arbeitsstände und dürfen **niemals** auf `main` gelangen — weder per Merge
noch per Cherry-Pick.

Betroffene Dateien:

- `src/entwicklung/**`
- `src/_includes/layouts/dev.njk`
- `src/assets/css/sections/dev-page.css`
- der Eintrag mit `"devOnly": true` in `src/_data/site.json`

Vor jedem Weg nach `main` prüfen: `git diff main...daniel --stat` darf keine
dieser Dateien enthalten.

Zusätzlich technisch abgesichert: Nav-Einträge mit `devOnly: true` werden in
`src/_includes/partials/nav.njk` ausgeblendet, sobald `env.isProduction` gilt.
Die Seiten stehen auf `noindex` und fehlen in `src/sitemap.njk`.
