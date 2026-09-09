/* =========================================================
   Conversion- und Modul-Tracking

   Ein zentraler Sender, damit Event-Namen an genau einer Stelle stehen.
   Namen sind das Vertragsstück Richtung GA4: einmal festlegen, nicht mehr
   ändern – sonst brechen Berichte und importierte Conversions.

   Konvention: alles klein, Unterstriche, <was>_<passiert>.
   ========================================================= */
(function () {
  "use strict";

  var EVENTS = {
    ctaKontakt:    "kontakt_cta_klick",   // Klick auf einen Button/Link Richtung /kontakt
    mail:          "mail_klick",
    telefon:       "telefon_klick",
    terminGeoeffnet: "termin_geoeffnet",  // Kalender wurde sichtbar (nach Einwilligung)
    terminGebucht: "termin_gebucht",      // die eigentliche Conversion
    pricingWechsel: "pricing_wechsel",    // monatlich <-> jährlich
    themaKlick:    "vertriebsstrecke_klick"
  };

  /** Sendet direkt über gtag; ohne gtag als dataLayer-Push, damit ein
      späterer Umzug auf GTM ohne Code-Änderung funktioniert. */
  function track(name, params) {
    params = params || {};
    if (typeof window.gtag === "function") {
      window.gtag("event", name, params);
    } else {
      window.dataLayer = window.dataLayer || [];
      var payload = { event: name };
      for (var k in params) if (params.hasOwnProperty(k)) payload[k] = params[k];
      window.dataLayer.push(payload);
    }
  }

  /* --- Klicks ---------------------------------------------------------- */
  function initKlicks() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a");
      if (!a) return;
      var href = a.getAttribute("href") || "";

      if (href.indexOf("mailto:") === 0) {
        track(EVENTS.mail, { ziel: href.replace("mailto:", "") });
      } else if (href.indexOf("tel:") === 0) {
        track(EVENTS.telefon, { ziel: href.replace("tel:", "") });
      } else if (href.indexOf("/kontakt") === 0) {
        track(EVENTS.ctaKontakt, { quelle: location.pathname, text: (a.textContent || "").trim().slice(0, 60) });
      } else if (href.indexOf("/zielgruppen/") === 0) {
        track(EVENTS.themaKlick, { zielgruppe: href.replace("/zielgruppen/", "").replace(/\/$/, "") });
      }
    });

    // Preis-Umschalter
    document.querySelectorAll("[data-tabs] [role='tab']").forEach(function (tab) {
      tab.addEventListener("click", function () {
        track(EVENTS.pricingWechsel, { intervall: (tab.id || "").replace("tab-", "") });
      });
    });
  }

  /* --- Terminbuchung (Cal.com) ----------------------------------------- */
  function initTermin() {
    var ns = document.querySelector("[id^='cal-inline-']");
    if (!ns) return;
    var name = ns.id.replace("cal-inline-", "");

    // Cal wird erst nach der Einwilligung geladen – daher warten statt annehmen.
    var versuche = 0;
    var timer = setInterval(function () {
      versuche++;
      var api = window.Cal && window.Cal.ns && window.Cal.ns[name];
      if (!api) { if (versuche > 60) clearInterval(timer); return; }
      clearInterval(timer);

      track(EVENTS.terminGeoeffnet, {});

      // Neuere Embeds feuern beide Varianten – einmal zählen reicht.
      function gebucht() {
        if (window.__terminGetrackt) return;
        window.__terminGetrackt = true;
        track(EVENTS.terminGebucht, {});
      }
      ["bookingSuccessful", "bookingSuccessfulV2"].forEach(function (action) {
        try { api("on", { action: action, callback: gebucht }); } catch (e) {}
      });
    }, 500);
  }

  /* --- Modul-Tracking (Phase 10) --------------------------------------- */
  function initSektionen() {
    var sektionen = document.querySelectorAll("section[id]");
    if (!sektionen.length || !("IntersectionObserver" in window)) return;

    var gesehen = {};
    var beobachter = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var id = e.target.id;
        if (gesehen[id] || !e.isIntersecting) return;

        // Zwei Wege, damit auch sehr hohe Sektionen zählen: entweder 15 %
        // der Sektion sind sichtbar, oder sie füllt über 30 % des Fensters.
        var anteilSektion = e.intersectionRatio;
        var anteilFenster = e.intersectionRect.height / window.innerHeight;
        if (anteilSektion < 0.15 && anteilFenster <= 0.30) return;

        gesehen[id] = true;
        beobachter.unobserve(e.target);
        // Sektion steckt im Namen – erspart eine Custom Dimension in GA4.
        track("section_view_" + id.replace(/-/g, "_"), {});
      });
    }, { threshold: [0, 0.15, 0.3, 0.5, 0.75, 1] });

    sektionen.forEach(function (s) { beobachter.observe(s); });
  }

  function init() {
    initKlicks();
    initTermin();
    initSektionen();
  }

  document.readyState === "loading"
    ? document.addEventListener("DOMContentLoaded", init)
    : init();
})();
