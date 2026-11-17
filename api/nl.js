/**
 * Newsletter-Links auf der eigenen Domain (Daten in der Sofortsichtbar-Datenbank).
 *
 *   GET  /n/<token>/<nr>          (Rewrite → /api/nl?k=<token>&l=<nr>)
 *        Klick-Weiterleitung: Ziel holen, Klick protokollieren (falls im
 *        Newsletter eingeschaltet), 302 aufs Ziel. Unbekannt → Startseite.
 *   GET  /api/nl?abmelden=<token>  → weiter zur Abmeldeseite (bestätigen per Klick;
 *        GET meldet NICHT ab, weil Link-Scanner der Mailprogramme Links vorab öffnen)
 *   POST /api/nl?abmelden=<token>  → abmelden. Das nutzen die Abmeldeseite und die
 *        Ein-Klick-Abmeldung der Mailprogramme (RFC 8058, List-Unsubscribe-Post).
 *
 * Keine Cookies, keine IP-Adressen. Für die Klickmessung wird nur der
 * User-Agent ausgewertet, um Link-Scanner herauszufiltern (nicht gespeichert).
 *
 * Umgebungsvariablen wie api/track.js: SUPABASE_URL, SUPABASE_SECRET_KEY
 */

const STARTSEITE = "https://www.sofortsichtbar.de/";
const TOKEN = /^[0-9a-f]{64}$/;

async function rpc(fn, args) {
  const url = process.env.SUPABASE_URL, key = process.env.SUPABASE_SECRET_KEY;
  if (!url || !key) throw new Error("SUPABASE_URL oder SUPABASE_SECRET_KEY fehlt");
  const r = await fetch(`${url.replace(/\/+$/, "")}/rest/v1/rpc/${fn}`, {
    method: "POST",
    headers: { apikey: key, "Content-Type": "application/json" },
    body: JSON.stringify(args),
  });
  if (!r.ok) throw new Error(`Supabase ${r.status}: ${(await r.text()).slice(0, 200)}`);
  return r.json();
}

const ohneCache = { "Cache-Control": "no-store", "X-Robots-Tag": "noindex" };
function weiter(ziel) {
  return new Response(null, { status: 302, headers: { Location: ziel, ...ohneCache, "Referrer-Policy": "no-referrer" } });
}

export async function GET(request) {
  const p = new URL(request.url).searchParams;
  const abmelden = p.get("abmelden");
  if (abmelden !== null) {
    return weiter("/newsletter/abmelden" + (TOKEN.test(abmelden) ? "?t=" + abmelden : ""));
  }
  const token = p.get("k") || "", nr = Number(p.get("l"));
  if (!TOKEN.test(token) || !Number.isInteger(nr) || nr < 0 || nr > 500) return weiter(STARTSEITE);
  try {
    const ziel = await rpc("newsletter_klick", { p_token: token, p_nr: nr, p_ua: (request.headers.get("user-agent") || "").slice(0, 300) || null });
    return weiter(typeof ziel === "string" && /^(https?:|mailto:)/i.test(ziel) ? ziel : STARTSEITE);
  } catch (err) {
    console.error("[nl] Klick", err);
    return weiter(STARTSEITE);
  }
}

export async function POST(request) {
  const token = new URL(request.url).searchParams.get("abmelden") || "";
  if (!TOKEN.test(token)) return new Response(JSON.stringify({ ok: false }), { status: 400, headers: { "Content-Type": "application/json", ...ohneCache } });
  try {
    const ok = await rpc("newsletter_abmelden", { p_token: token });
    return new Response(JSON.stringify({ ok: ok === true }), { status: ok === true ? 200 : 404, headers: { "Content-Type": "application/json", ...ohneCache } });
  } catch (err) {
    console.error("[nl] Abmelden", err);
    return new Response(JSON.stringify({ ok: false }), { status: 502, headers: { "Content-Type": "application/json", ...ohneCache } });
  }
}
