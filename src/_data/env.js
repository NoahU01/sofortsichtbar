/**
 * Umgebung, in der gebaut wird.
 *
 * Vercel setzt VERCEL_ENV beim Build auf "production", "preview" oder
 * "development". Lokal ist die Variable nicht gesetzt.
 *
 * Daran hängt, ob Tracking und Cookie-Banner mitgebaut werden: Auf einer
 * Vorschau-Umgebung würden sonst Testklicks in derselben GA4-Property
 * landen wie echte Besucher.
 */
const name = process.env.VERCEL_ENV || "development";

export default {
  name,
  isProduction: name === "production",
  isPreview: name === "preview",
};
