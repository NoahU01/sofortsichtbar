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

  /* --- Modul-Tracking --------------------------------------------------
     Misst pro Sektion zwei Dinge, gleiche Logik wie bei AdMemory:

     1. section_view_<id> — einmal pro Seitenaufruf, sobald die Sektion im
        sichtbaren Bereich war. Das ist die Reichweite: bis wohin wird gescrollt.
     2. section_time_<id> — die dort verbrachte Zeit in Sekunden, als `value`.
        GA4 summiert das zur Metrik "Ereigniswert"; Durchschnitt ergibt sich aus
        Ereigniswert geteilt durch die Anzahl der section_view-Events.
        `value` ist ein Standardfeld – dafür braucht es keine Custom Dimension.

     Zwei Dinge, die bei AdMemory Zahlen verfälscht hatten:
     - page_location muss an JEDEM Event hängen, sonst ordnet GA4 Events der
       falschen Seite zu (geteilte Sektionen liegen auf mehreren Seiten).
     - Der Observer hängt sich sofort an und danach nochmal, statt erst nach
       einer Verzögerung – sonst fehlen alle, die sofort weiterscrollen.
     --------------------------------------------------------------------- */
  var SICHTBAR_ANTEIL = 0.15;
  /** Sehr hohe Sektionen erreichen den Anteil nie, füllen aber das Fenster. */
  var FENSTER_ANTEIL = 0.3;
  /** Deckel gegen Tabs, die stundenlang offen liegen. */
  var MAX_SEKUNDEN = 600;
  /** Unter einer Sekunde ist Durchscrollen, keine Aufmerksamkeit. */
  var MIN_SEKUNDEN = 1;

  function initSektionen() {
    var sektionen = document.querySelectorAll("section[id]");
    if (!sektionen.length || !("IntersectionObserver" in window)) return;

    var pfad = location.pathname;
    var seitenUrl = location.href;
    var gesehen = {};     // schon als view gemeldet
    var sichtbar = {};    // gerade im Bild
    var seit = {};        // laufender Timer je Sektion
    var summe = {};       // aufgelaufene Millisekunden

    function jetzt() { return performance.now(); }

    /** Laufende Timer stoppen und aufaddieren (Tabwechsel, Seitenwechsel). */
    function alleAnhalten() {
      for (var id in seit) {
        if (!seit.hasOwnProperty(id)) continue;
        summe[id] = (summe[id] || 0) + (jetzt() - seit[id]);
      }
      seit = {};
    }

    /** Timer für alles wieder starten, was gerade sichtbar ist.
        Nur im Vordergrund – sonst läuft die Uhr im Hintergrund-Tab weiter.
        (Diese Prüfung fehlt in der AdMemory-Vorlage: dort wird nach dem
        Senden bedingungslos fortgesetzt, wodurch Hintergrundzeit in die
        nächste Meldung einfließt.) */
    function alleFortsetzen() {
      if (document.visibilityState !== "visible") return;
      for (var id in sichtbar) {
        if (sichtbar.hasOwnProperty(id) && !seit.hasOwnProperty(id)) seit[id] = jetzt();
      }
    }

    function senden() {
      alleAnhalten();
      for (var id in summe) {
        if (!summe.hasOwnProperty(id)) continue;
        // Erst gegen die Rohzeit prüfen: Math.round würde aus 0,6s eine 1s
        // machen und Durchscrollen als Verweildauer durchgehen lassen.
        if (summe[id] < MIN_SEKUNDEN * 1000) continue;
        var sekunden = Math.round(summe[id] / 1000);
        track("section_time_" + id.replace(/-/g, "_"), {
          value: Math.min(sekunden, MAX_SEKUNDEN),
          page: pfad,
          page_location: seitenUrl,
          // beacon überlebt das Verlassen der Seite
          transport_type: "beacon"
        });
      }
      summe = {};
      // Sichtbares läuft weiter, falls die Person zurückkommt.
      alleFortsetzen();
    }

    var beobachter = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var id = e.target.id;
        if (!id) return;

        var istSichtbar = e.isIntersecting &&
          (e.intersectionRatio >= SICHTBAR_ANTEIL ||
           e.intersectionRect.height > window.innerHeight * FENSTER_ANTEIL);

        if (istSichtbar) {
          if (!gesehen[id]) {
            gesehen[id] = true;
            track("section_view_" + id.replace(/-/g, "_"), { page: pfad, page_location: seitenUrl });
          }
          sichtbar[id] = true;
          if (document.visibilityState === "visible" && !seit.hasOwnProperty(id)) seit[id] = jetzt();
        } else {
          delete sichtbar[id];
          if (seit.hasOwnProperty(id)) {
            summe[id] = (summe[id] || 0) + (jetzt() - seit[id]);
            delete seit[id];
          }
        }
      });
    }, { threshold: [0, SICHTBAR_ANTEIL, 0.5] });

    // Sofort anhängen, dann nochmal für spät gerenderte Sektionen.
    // observe() auf ein bereits beobachtetes Element ist folgenlos.
    function anhaengen() {
      document.querySelectorAll("section[id]").forEach(function (s) { beobachter.observe(s); });
    }
    anhaengen();
    setTimeout(anhaengen, 400);
    setTimeout(anhaengen, 1200);

    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden") senden();
      else alleFortsetzen();
    });
    window.addEventListener("pagehide", senden);
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
