/* =========================================================
   First-Party-Tracking → /api/track → Sofortsichtbar-Datenbank

   Läuft neben GA4, ersetzt es nicht. Event-Namen sind die des festen
   Katalogs in der Datenbank (core.event_types) – nicht frei erfinden.

   Einwilligung: Maßgeblich ist die Cookiebot-Kategorie "Statistik".
   - erteilt   → Sitzung (sessionStorage) + visitor_id-Cookie (setzt der Server)
   - fehlt     → Events gehen anonym raus: keine Sitzung, kein Cookie
   - noch offen (Banner steht) → anonym senden; stimmt die Person zu,
     beginnt ab da eine Sitzung mit Landingpage und Herkunft.
   Ohne Cookie-Banner (Vorschau, lokal) gilt Einwilligung als erteilt; der
   Server markiert diese Events als internal.

   Öffentlich: window.ssTrack(name, props)
   ========================================================= */
(function () {
  "use strict";

  var ENDPOINT = "/api/track";
  var SITZUNG_TIMEOUT = 30 * 60 * 1000;
  var HERKUNFT = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
    "gclid", "gbraid", "wbraid", "fbclid", "li_fat_id", "ttclid"];

  var warteschlange = [];
  var timer = null;
  var bereit = false;          // Einwilligungsstand bekannt?
  var einwilligung = false;
  var sitzung = null;
  // Beim Seitenwechsel kommt nur pagehide, kein visibilitychange. Was danach
  // noch gemeldet wird (section_time aus tracking.js), muss sofort raus.
  var verlassen = false;

  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
      var r = (Math.random() * 16) | 0;
      return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
    });
  }

  function intern() {
    try { return localStorage.getItem("ss_internal") === "1"; } catch (e) { return false; }
  }

  var mitBanner = !!document.getElementById("Cookiebot");

  function statistikErlaubt() {
    if (!mitBanner) return true;
    var cb = window.Cookiebot;
    return !!(cb && cb.consent && cb.consent.statistics);
  }

  /* --- Sitzung (nur mit Einwilligung) ----------------------------------- */
  function sitzungHolen() {
    var jetzt = Date.now();
    var s = null;
    try { s = JSON.parse(sessionStorage.getItem("ss_sid") || "null"); } catch (e) {}
    var neu = !s || !s.id || jetzt - s.last > SITZUNG_TIMEOUT;
    if (neu) s = { id: uuid(), last: jetzt };
    s.last = jetzt;
    try { sessionStorage.setItem("ss_sid", JSON.stringify(s)); } catch (e) {}
    return { id: s.id, neu: neu };
  }

  function herkunft() {
    var p = new URLSearchParams(location.search);
    var out = {};
    HERKUNFT.forEach(function (k) { if (p.has(k)) out[k] = p.get(k).slice(0, 200); });
    return out;
  }

  function sitzungStarten() {
    var s = sitzungHolen();
    sitzung = s.id;
    if (s.neu) {
      einreihen("session_start", herkunft(), { referrer: document.referrer, vorne: true });
    }
  }

  /* --- Senden ------------------------------------------------------------ */
  function einreihen(name, props, opt) {
    opt = opt || {};
    var e = {
      id: uuid(),
      name: name,
      ts: Date.now(),
      url: location.href,
      props: props || {}
    };
    if (opt.referrer !== undefined) e.referrer = opt.referrer;
    opt.vorne ? warteschlange.unshift(e) : warteschlange.push(e);
    // Seite wird gerade verlassen (z.B. section_time aus pagehide): sofort
    // per Beacon raus, sonst ginge das Event nach dem letzten Senden verloren.
    if (bereit && (verlassen || document.visibilityState === "hidden")) senden(true);
    else if (bereit && !timer) timer = setTimeout(senden, 1500);
  }

  function paket(events) {
    if (einwilligung && sitzung) sitzungHolen();   // Aktivität verlängert die Sitzung
    return JSON.stringify({
      consent: einwilligung,
      session_id: einwilligung ? sitzung : null,
      internal: intern(),
      events: events
    });
  }

  function senden(beimVerlassen) {
    clearTimeout(timer);
    timer = null;
    if (!bereit || !warteschlange.length) return;
    var events = warteschlange.splice(0, 25);
    var body = paket(events);
    if (beimVerlassen && navigator.sendBeacon) {
      navigator.sendBeacon(ENDPOINT, new Blob([body], { type: "text/plain" }));
    } else {
      fetch(ENDPOINT, {
        method: "POST",
        body: body,
        keepalive: true,
        credentials: "same-origin",
        headers: { "Content-Type": "text/plain" }
      }).catch(function () {});
    }
    if (warteschlange.length) senden(beimVerlassen);
  }

  function freigeben() {
    bereit = true;
    einwilligung = statistikErlaubt();
    if (einwilligung) sitzungStarten();
    senden();
  }

  /* --- Öffentliche Schnittstelle ---------------------------------------- */
  window.ssTrack = function (name, props) {
    einreihen(name, props);
  };

  // Vor der Einwilligungsabfrage einreihen, damit er im ersten Paket mitgeht.
  einreihen("page_view", {}, { referrer: document.referrer });

  /* --- Einwilligung abwarten -------------------------------------------- */
  if (!mitBanner) {
    freigeben();
  } else {
    // Wiederkehrende Besucher: Entscheidung steht beim Laden fest.
    window.addEventListener("CookiebotOnLoad", function () {
      if (!bereit) freigeben();
    });
    // Erstbesuch: Banner steht noch. Nicht ewig warten – anonym senden.
    setTimeout(function () { if (!bereit) freigeben(); }, 3000);

    window.addEventListener("CookiebotOnAccept", function () {
      var vorher = einwilligung;
      einwilligung = statistikErlaubt();
      if (einwilligung && !vorher) { sitzungStarten(); senden(); }
    });
    window.addEventListener("CookiebotOnDecline", function () {
      einwilligung = false;
      sitzung = null;
      try { sessionStorage.removeItem("ss_sid"); } catch (e) {}
    });
  }

  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") senden(true);
  });
  window.addEventListener("pagehide", function () { verlassen = true; senden(true); });
  // Zurück-Button aus dem bfcache: Seite lebt weiter.
  window.addEventListener("pageshow", function (e) { if (e.persisted) verlassen = false; });
})();
