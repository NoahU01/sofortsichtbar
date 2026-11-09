/**
 * First-Party-Tracking: nimmt Events der Website an und schreibt sie in die
 * Sofortsichtbar-Datenbank (Supabase, core.events über public.ingest_events).
 *
 * Warum eine Funktion auf der eigenen Domain statt direkt zu Supabase:
 *   - Nur so kann die visitor_id als HttpOnly-Cookie vom SERVER gesetzt
 *     werden. Per JavaScript gesetzte Cookies kappt Safari auf 7 Tage.
 *   - Der Browser sieht keinen fremden Dienst (Adblocker, ITP).
 *   - Der Secret Key bleibt auf dem Server.
 *
 * Einwilligung (§ 25 TDDDG):
 *   consent = true  → visitor_id-Cookie lesen/setzen, session_id übernehmen.
 *   consent = false → nichts lesen, nichts setzen; Events gehen anonym ein
 *                     (keine visitor_id, keine session_id). Ein vorhandenes
 *                     Cookie wird gelöscht (Widerruf).
 * IP-Adressen werden nie gespeichert.
 *
 * Umgebungsvariablen (Vercel → Settings → Environment Variables):
 *   SUPABASE_URL         https://<ref>.supabase.co
 *   SUPABASE_SECRET_KEY  sb_secret_…  (nie ins Repo)
 */

const COOKIE = "ss_vid";
// Chrome deckelt Cookie-Laufzeiten bei 400 Tagen.
const COOKIE_MAX_AGE = 400 * 24 * 60 * 60;
const MAX_BODY = 16 * 1024;
const MAX_EVENTS = 25;

/** Nur diese Namen nimmt der Endpunkt an – gleiche Liste wie core.event_types (Quelle website). */
const ERLAUBT = new Set([
  "page_view", "session_start", "section_view", "section_time", "scroll_depth",
  "cta_click", "form_start", "form_submit", "file_download",
  "booking_widget_view", "pricing_toggle", "meeting_booked",
]);

const BOT = /bot|crawl|spider|slurp|headless|lighthouse|pagespeed|gtmetrix|preview|facebookexternalhit|embedly|curl|wget|python|axios|node-fetch|go-http|java\/|monitor|uptime|pingdom/i;

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/** URL-Parameter, die mitgespeichert werden. Alles andere fliegt raus –
    Query-Strings können sonst E-Mails oder Tokens enthalten. */
const BEHALTEN = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
  "gclid", "gbraid", "wbraid", "fbclid", "li_fat_id", "ttclid"];

/** Seitentyp aus dem Pfad. Scoring arbeitet mit Typen, nicht mit URLs. */
function seitentyp(pfad) {
  const p = pfad.replace(/\/+$/, "") || "/";
  if (p === "/") return "home";
  if (p === "/pricing") return "preis";
  if (p === "/kontakt") return "kontakt";
  if (p === "/zielgruppen" || p.startsWith("/zielgruppen/")) return "zielgruppe";
  if (p === "/vertriebsstrecken" || p === "/prozess" || p === "/vetriebsleiter") return "produkt";
  if (p === "/impressum" || p === "/datenschutzerklarung") return "rechtliches";
  if (p.startsWith("/karriere") || p.startsWith("/jobs")) return "karriere";
  if (p.startsWith("/blog")) return "blog";
  if (p.startsWith("/referenzen") || p.startsWith("/cases")) return "referenz";
  return "sonstige";
}

/** URL auf Pfad + erlaubte Parameter kürzen. Gibt null zurück, wenn fremde Domain. */
function bereinigeUrl(roh, host) {
  try {
    const u = new URL(roh);
    if (u.host !== host) return null;
    const q = new URLSearchParams();
    for (const k of BEHALTEN) if (u.searchParams.has(k)) q.set(k, u.searchParams.get(k).slice(0, 200));
    const s = q.toString();
    return { pfad: u.pathname, url: u.origin + u.pathname + (s ? "?" + s : "") };
  } catch {
    return null;
  }
}

/** Referrer nur als Herkunft (Origin), nie mit Pfad oder Query. */
function bereinigeReferrer(roh) {
  if (!roh || typeof roh !== "string") return null;
  try { return new URL(roh).origin; } catch { return null; }
}

/** Eigenschaften flach und klein halten: nur Strings, Zahlen, Booleans. */
function bereinigeProps(props) {
  const out = {};
  if (!props || typeof props !== "object") return out;
  let n = 0;
  for (const [k, v] of Object.entries(props)) {
    if (n++ >= 20 || !/^[a-z][a-z0-9_]{0,39}$/.test(k)) continue;
    if (typeof v === "string") out[k] = v.slice(0, 200);
    else if (typeof v === "number" && Number.isFinite(v)) out[k] = v;
    else if (typeof v === "boolean") out[k] = v;
  }
  return out;
}

function leseCookie(header, name) {
  if (!header) return null;
  for (const teil of header.split(";")) {
    const [k, ...rest] = teil.trim().split("=");
    if (k === name) return rest.join("=");
  }
  return null;
}

function geraet(ua) {
  return /mobi|android|iphone|ipod/i.test(ua) ? "mobil" : /ipad|tablet/i.test(ua) ? "tablet" : "desktop";
}

const antwort = (status, headers = {}) => new Response(null, { status, headers });

export async function POST(request) {
  const ua = request.headers.get("user-agent") || "";
  if (BOT.test(ua)) return antwort(204);

  const host = request.headers.get("host") || "";
  // Nur Anfragen von der eigenen Seite.
  const origin = request.headers.get("origin");
  if (origin && new URL(origin).host !== host) return antwort(403);

  const text = await request.text();
  if (text.length > MAX_BODY) return antwort(413);

  let body;
  try { body = JSON.parse(text); } catch { return antwort(400); }
  if (!body || !Array.isArray(body.events) || body.events.length === 0) return antwort(400);

  const consent = body.consent === true;
  const internal = process.env.VERCEL_ENV !== "production" || body.internal === true;
  const headers = { "Cache-Control": "no-store" };

  // visitor_id nur mit Einwilligung.
  let visitorId = null;
  if (consent) {
    const vorhanden = leseCookie(request.headers.get("cookie"), COOKIE);
    visitorId = vorhanden && UUID.test(vorhanden) ? vorhanden : crypto.randomUUID();
    // Bei jedem Aufruf erneuern, damit die Laufzeit ab dem letzten Besuch zählt.
    headers["Set-Cookie"] = `${COOKIE}=${visitorId}; Path=/; Max-Age=${COOKIE_MAX_AGE}; HttpOnly; Secure; SameSite=Lax`;
  } else if (leseCookie(request.headers.get("cookie"), COOKIE)) {
    headers["Set-Cookie"] = `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`;
  }

  const jetzt = Date.now();
  const events = [];
  for (const e of body.events.slice(0, MAX_EVENTS)) {
    if (!e || !ERLAUBT.has(e.name) || !UUID.test(e.id || "")) continue;
    const seite = bereinigeUrl(e.url, host);
    if (!seite) continue;

    // Zeitstempel vom Browser nur, wenn plausibel (± 1 Tag), sonst Serverzeit.
    const ts = Number(e.ts);
    const occurred = Number.isFinite(ts) && Math.abs(jetzt - ts) < 864e5 ? ts : jetzt;

    const props = bereinigeProps(e.props);
    props.geraet = geraet(ua);
    if (e.name === "session_start" || e.name === "page_view") {
      const ref = bereinigeReferrer(e.referrer);
      if (ref && new URL(ref).host !== host) props.referrer = ref;
    }

    events.push({
      event_id: "web:" + e.id.toLowerCase(),
      event_name: e.name,
      occurred_at: new Date(occurred).toISOString(),
      visitor_id: visitorId,
      session_id: consent && UUID.test(body.session_id || "") ? body.session_id : null,
      source: "website",
      page_url: seite.url,
      page_type: seitentyp(seite.pfad),
      properties: props,
      consent_state: consent ? "granted" : "denied",
      internal,
    });
  }
  // X-Track verrät nur den Ausgang (keine Daten) – zur Fehlersuche im Netzwerk-Tab.
  if (events.length === 0) return antwort(204, { ...headers, "X-Track": "keine-gueltigen-events" });

  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SECRET_KEY;
  if (!url || !key) {
    console.error("[track] SUPABASE_URL oder SUPABASE_SECRET_KEY fehlt");
    // Besucher merkt nichts, Fehler steht im Log
    return antwort(204, { ...headers, "X-Track": "config-fehlt" + (url ? "" : ":url") + (key ? "" : ":key") });
  }

  let ausgang = "gespeichert";
  try {
    const r = await fetch(`${url.replace(/\/+$/, "")}/rest/v1/rpc/ingest_events`, {
      method: "POST",
      headers: { apikey: key, "Content-Type": "application/json" },
      body: JSON.stringify({ p_events: events }),
    });
    if (!r.ok) {
      ausgang = "supabase-" + r.status;
      console.error("[track] Supabase", r.status, (await r.text()).slice(0, 300));
    }
  } catch (err) {
    ausgang = "supabase-nicht-erreichbar";
    console.error("[track] Supabase nicht erreichbar", err);
  }

  return antwort(204, { ...headers, "X-Track": ausgang });
}
