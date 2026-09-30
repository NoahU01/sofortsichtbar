/* =========================================================
   Strategie-Konzepte – Detailschublade, Graph, Fokus, Cockpit
   Läuft nur auf den Seiten unter /entwicklung/strategie/.
   ========================================================= */
(function () {
  "use strict";

  var wurzel = document.querySelector(".k");
  if (!wurzel) return;

  var pop = wurzel.querySelector("[data-pop]");
  var details = wurzel.querySelectorAll("[data-detail]");
  var graphFlaeche = wurzel.querySelector(".gr__flaeche, .g2__flaeche");

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
    graphFlaeche.classList.remove("zeigt-kritisch");
    var kk = wurzel.querySelector("[data-kritisch]");
    if (kk) { kk.classList.remove("is-an"); kk.textContent = "Längsten Weg zeigen"; }
    graphZuruecksetzen();
    graphFlaeche.classList.add("is-auswahl");

    var vor = sammle(id, "braucht");
    var nach = sammle(id, "nachfolger");
    knoten[id].el.classList.add("is-gewaehlt");
    Object.keys(vor).forEach(function (k) { knoten[k].el.classList.add("is-vor"); });
    Object.keys(nach).forEach(function (k) { knoten[k].el.classList.add("is-nach"); });

    var inKette = function (x) { return x === id || vor[x] || nach[x]; };
    graphFlaeche.querySelectorAll(".gr__kante, .g2__kante").forEach(function (kante) {
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

  /* --- Detail-Popover am angeklickten Element -------------------------- */
  function schliesse() {
    if (!pop) return;
    pop.hidden = true;
    pop.classList.remove("is-offen");
    wurzel.querySelectorAll(".is-offen-quelle").forEach(function (el) {
      el.classList.remove("is-offen-quelle");
    });
  }

  // Neben den Auslöser legen und dabei im Sichtfeld halten
  function platziere(ausloeser) {
    var r = ausloeser.getBoundingClientRect();
    var breite = pop.offsetWidth;
    var hoehe = pop.offsetHeight;
    var luft = 10;

    var links = r.right + luft;
    if (links + breite > window.innerWidth - luft) links = r.left - breite - luft;
    if (links < luft) links = Math.max(luft, (window.innerWidth - breite) / 2);

    var oben = r.top;
    if (oben + hoehe > window.innerHeight - luft) oben = window.innerHeight - hoehe - luft;
    if (oben < luft) oben = luft;

    pop.style.left = Math.round(links) + "px";
    pop.style.top = Math.round(oben) + "px";
  }

  function zeigeDetail(id, ausloeser) {
    if (!pop) return;
    var treffer = false;
    details.forEach(function (el) {
      var an = el.dataset.detail === id;
      el.hidden = !an;
      if (an) treffer = true;
    });
    if (!treffer) return;

    wurzel.querySelectorAll(".is-offen-quelle").forEach(function (el) {
      el.classList.remove("is-offen-quelle");
    });
    if (ausloeser) ausloeser.classList.add("is-offen-quelle");

    pop.hidden = false;
    pop.scrollTop = 0;
    // Ohne Auslöser (Sprung über einen Chip im Popover) bleibt die Position stehen
    if (ausloeser) {
      platziere(ausloeser);
      requestAnimationFrame(function () { platziere(ausloeser); });
    }
    requestAnimationFrame(function () { pop.classList.add("is-offen"); });

    graphMarkieren(id);
    metroMarkieren(id);
  }

  /* --- Längster Weg ---------------------------------------------------- */
  function kritischUmschalten(knopf) {
    if (!graphFlaeche) return;
    graphZuruecksetzen();
    schliesse();
    var an = graphFlaeche.classList.toggle("zeigt-kritisch");
    knopf.classList.toggle("is-an", an);
    knopf.textContent = an ? "Längsten Weg ausblenden" : "Längsten Weg zeigen";
  }

  wurzel.addEventListener("click", function (e) {
    if (e.target.closest("[data-pop-zu]")) { schliesse(); return; }
    var kk = e.target.closest("[data-kritisch]");
    if (kk) { kritischUmschalten(kk); return; }
    if (e.target.closest("[data-graph-reset]")) { graphZuruecksetzen(); schliesse(); return; }

    var ausloeser = e.target.closest("[data-schritt]");
    if (ausloeser) {
      zeigeDetail(ausloeser.dataset.schritt, ausloeser.closest("[data-pop]") ? null : ausloeser);
      return;
    }
  });

  // Klick daneben schließt
  document.addEventListener("click", function (e) {
    if (!pop || pop.hidden) return;
    if (e.target.closest("[data-pop]") || e.target.closest("[data-schritt]")) return;
    schliesse();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && pop && !pop.hidden) schliesse();
  });

  window.addEventListener("resize", schliesse);

  /* --- Graph V2/V3: Hervorhebungsvariante A/B/C ------------------------ */
  var g2 = wurzel.querySelector("[data-g2]");
  if (g2) {
    var vbtns = wurzel.querySelectorAll("[data-variante]");
    vbtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var wahl = btn.dataset.variante;
        g2.classList.remove("g2--a", "g2--b", "g2--c");
        g2.classList.add("g2--" + wahl);
        vbtns.forEach(function (b) { b.classList.toggle("is-an", b === btn); });
        history.replaceState(null, "", "#hervorhebung=" + wahl);
      });
    });

    var ausHash = (location.hash.match(/hervorhebung=([abc])/) || [])[1];
    if (ausHash) {
      var treffer = wurzel.querySelector('[data-variante="' + ausHash + '"]');
      if (treffer) treffer.click();
    }
  }

  /* --- Tafel: beim Überfahren zeigen, was ein Schritt braucht ---------- */
  wurzel.querySelectorAll(".ta__chip[data-braucht]").forEach(function (chip) {
    var ids = (chip.dataset.braucht || "").split(" ").filter(Boolean);
    if (!ids.length) return;

    function setze(an) {
      ids.forEach(function (id) {
        var ziel = wurzel.querySelector('.ta__chip[data-chip="' + id + '"]');
        if (ziel) ziel.classList.toggle("is-voraussetzung", an);
      });
    }
    chip.addEventListener("mouseenter", function () { setze(true); });
    chip.addEventListener("mouseleave", function () { setze(false); });
    chip.addEventListener("focus", function () { setze(true); });
    chip.addEventListener("blur", function () { setze(false); });
  });
})();
