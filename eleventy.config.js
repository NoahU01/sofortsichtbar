import fs from "node:fs";
import path from "node:path";

const CSS_DIR = "src/assets/css";
const CSS_OUT = "dist/assets/css/main.css";

/**
 * Bündelt alle CSS-Module in genau eine Datei (eine Anfrage, keine Import-Kette).
 * Reihenfolge: nummerierte Basis-Module zuerst, danach die Sektionen alphabetisch.
 */
function buildCss() {
  const base = fs.readdirSync(CSS_DIR).filter((f) => f.endsWith(".css")).sort();
  const sections = fs
    .readdirSync(path.join(CSS_DIR, "sections"))
    .filter((f) => f.endsWith(".css"))
    .sort()
    .map((f) => path.join("sections", f));

  const css = [...base, ...sections]
    .map((f) => `/* ---- ${f} ---- */\n${fs.readFileSync(path.join(CSS_DIR, f), "utf8")}`)
    .join("\n");

  fs.mkdirSync(path.dirname(CSS_OUT), { recursive: true });
  fs.writeFileSync(CSS_OUT, css);
  return { files: base.length + sections.length, bytes: css.length };
}

/** Pfad auf einen Vergleichs-Schlüssel bringen: "/pricing/" und "/pricing" werden gleich. */
function normalizePath(value) {
  return String(value || "").replace(/index\.html$/, "").replace(/^\/+|\/+$/g, "");
}

export default function (eleventyConfig) {
  // Absolute URL ohne Schrägstrich am Ende – gleiche Form in Canonical, og:url und Sitemap
  eleventyConfig.addFilter("absoluteUrl", (pageUrl, base) => {
    const path = normalizePath(pageUrl);
    return path ? `${base}/${path}` : `${base}/`;
  });

  // Markiert den aktiven Navigationspunkt (aria-current)
  eleventyConfig.addFilter("isCurrentPath", (href, pageUrl) => {
    const target = normalizePath(href);
    return target !== "" && target === normalizePath(pageUrl);
  });

  // Statische Assets 1:1 nach dist kopieren (CSS wird gebündelt, siehe unten)
  eleventyConfig.addPassthroughCopy({ "src/assets/img": "assets/img" });
  eleventyConfig.addPassthroughCopy({ "src/assets/js": "assets/js" });
  eleventyConfig.addPassthroughCopy({ "src/static": "." });

  eleventyConfig.addWatchTarget("src/assets/css/");

  eleventyConfig.on("eleventy.after", () => {
    const { files, bytes } = buildCss();
    console.log(`[css] ${files} Module gebündelt → ${CSS_OUT} (${(bytes / 1024).toFixed(1)} kB)`);
  });

  eleventyConfig.setServerOptions({ showAllHosts: true });

  return {
    dir: {
      input: "src",
      output: "dist",
      includes: "_includes",
      data: "_data",
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
}
