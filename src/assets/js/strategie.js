/* =========================================================
   Strategie-Konzepte – Detailschublade, Graph, Fokus, Cockpit
   Läuft nur auf den Seiten unter /entwicklung/strategie/.
   ========================================================= */
(function () {
  "use strict";

  var wurzel = document.querySelector(".k");
  if (!wurzel) return;

  var drawer = wurzel.querySelector("[data-drawer]");
  var schatten = wurzel.querySelector("[data-schatten]");
  var details = wurzel.querySelectorAll("[data-detail]");
  var graphFlaeche = wurzel.querySelector(".gr__flaeche");

  /* --- Graph: Kette vor und nach einem Knoten ------------------------- */
  var knoten = {};
  wurzel.querySelectorAll("[data-knoten]").forEach(function (el) {
    knoten[el.dataset.knoten] = {
      el: el,
      braucht: (el.dataset.braucht || "").split(" ").filter(Boolean),
      nachfolger: (el.dataset.nachfolger || "").split(" ").filter(Boolean),
    };
  });

  function sammle(id, richtung) {
    var gesehen = {};
    var stapel = (knoten[id] || { braucht: [], nachfolger: [] })[richtung].slice();
    while (stapel.length) {
      var aktuell = stapel.pop();
      if (gesehen[aktuell] || !knoten[aktuell]) continue;
      gesehen[aktuell] = true;
      knoten[aktuell][richtung].forEach(function (n) { stapel.push(n); });
    }
    return gesehen;
  }

  function graphZuruecksetzen() {
    if (!graphFlaeche) return;
    graphFlaeche.classList.remove("is-auswahl");
    graphFlaeche.querySelectorAll(".is-gewaehlt, .is-vor, .is-nach, .is-hell").forEach(function (el) {
      el.classList.remove("is-gewaehlt", "is-vor", "is-nach", "is-hell");
    });
    var reset = wurzel.querySelector("[data-graph-reset]");
    if (reset) reset.hidden = true;
  }

  function graphMarkieren(id) {
    if (!graphFlaeche || !knoten[id]) return;
    graphZuruecksetzen();
    graphFlaeche.classList.add("is-auswahl");

    var vor = sammle(id, "braucht");
    var nach = sammle(id, "nachfolger");
    knoten[id].el.classList.add("is-gewaehlt");
    Object.keys(vor).forEach(function (k) { knoten[k].el.classList.add("is-vor"); });
    Object.keys(nach).forEach(function (k) { knoten[k].el.classList.add("is-nach"); });

    var inKette = function (x) { return x === id || vor[x] || nach[x]; };
    graphFlaeche.querySelectorAll(".gr__kante").forEach(function (kante) {
      if (inKette(kante.dataset.von) && inKette(kante.dataset.nach)) kante.classList.add("is-hell");
    });

    var reset = wurzel.querySelector("[data-graph-reset]");
    if (reset) reset.hidden = false;
  }

  /* --- Liniennetz: Umstiege eines Halts hervorheben -------------------- */
  function metroMarkieren(id) {
    wurzel.querySelectorAll(".me__quer").forEach(function (pfad) {
      pfad.classList.toggle("is-hell", pfad.dataset.von === id || pfad.dataset.nach === id);
    });
    wurzel.querySelectorAll("[data-halt]").forEach(function (halt) {
      halt.classList.toggle("is-gewaehlt", halt.dataset.halt === id);
    });
  }

  /* --- Detailschublade ------------------------------------------------- */
  function schliesse() {
    if (!drawer) return;
    drawer.hidden = true;
    if (schatten) schatten.hidden = true;
    drawer.classList.remove("is-offen");
  }

  function zeigeDetail(id) {
    if (!drawer) return;
    var treffer = false;
    details.forEach(function (el) {
      var an = el.dataset.detail === id;
      el.hidden = !an;
      if (an) treffer = true;
    });
    if (!treffer) return;

    drawer.hidden = false;
    if (schatten) schatten.hidden = false;
    drawer.scrollTop = 0;
    // Erst im nächsten Frame, damit die Einblend-Animation greift
    requestAnimationFrame(function () { drawer.classList.add("is-offen"); });

    graphMarkieren(id);
    metroMarkieren(id);
  }

  wurzel.addEventListener("click", function (e) {
    var ausloeser = e.target.closest("[data-schritt]");
    if (ausloeser) {
      zeigeDetail(ausloeser.dataset.schritt);
      return;
    }
    if (e.target.closest("[data-drawer-zu]") || e.target.closest("[data-schatten]")) schliesse();
    if (e.target.closest("[data-graph-reset]")) graphZuruecksetzen();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && drawer && !drawer.hidden) schliesse();
  });

  /* --- Fokus: zwischen den Ergebnisstufen wechseln --------------------- */
  var stufen = wurzel.querySelectorAll("[data-stufe]");
  if (stufen.length) {
    wurzel.querySelectorAll("[data-stufe-zu]").forEach(function (button) {
      button.addEventListener("click", function () {
        var ziel = button.dataset.stufeZu;
        stufen.forEach(function (s) { s.hidden = s.dataset.stufe !== ziel; });
        wurzel.querySelectorAll("[data-stufe-zu]").forEach(function (b) {
          b.classList.toggle("is-aktiv", b === button);
        });
      });
    });
  }

  /* --- Cockpit: nach Strang filtern ------------------------------------ */
  var filter = wurzel.querySelectorAll("[data-filter]");
  if (filter.length) {
    filter.forEach(function (chip) {
      chip.addEventListener("click", function () {
        var wahl = chip.dataset.filter;
        filter.forEach(function (c) { c.classList.toggle("is-aktiv", c === chip); });
        wurzel.querySelectorAll("[data-strang]").forEach(function (karte) {
          karte.hidden = wahl !== "alle" && karte.dataset.strang !== wahl;
        });
      });
    });
  }
})();
