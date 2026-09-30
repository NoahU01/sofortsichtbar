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
  var graphFlaeche = wurzel.querySelector(".g2__flaeche");

  /* --- Graph: Kette vor und nach einem Knoten ------------------------- */
  var knoten = {};
  wurzel.querySelectorAll("[data-knoten]").forEach(function (el) {
    knoten[el.dataset.knoten] = {
      el: el,
      braucht: (el.dataset.braucht || "").split(" ").filter(Boolean),
      nachfolger: (el.dataset.nachfolger || "").split(" ").filter(Boolean),
      vorher: (el.dataset.vorher || "").split(" ").filter(Boolean),
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
    graphFlaeche.querySelectorAll(".g2__kante").forEach(function (kante) {
      if (inKette(kante.dataset.von) && inKette(kante.dataset.nach)) kante.classList.add("is-hell");
    });
  }

  /* --- Liniennetz: die Route zu einem Halt zeigen ----------------------
     Wie eine Verbindungsauskunft: alles, was nicht zu diesem Halt führt,
     tritt zurück. Übrig bleiben die nötigen Halte, die Linienabschnitte
     dorthin und die Umstiege zwischen den Bahnen. */
  var metroPlan = wurzel.querySelector(".me__plan");
  var routeLeiste = wurzel.querySelector("[data-route-leiste]");
  var routeText = wurzel.querySelector("[data-route-text]");

  function metroZuruecksetzen() {
    if (!metroPlan) return;
    metroPlan.classList.remove("is-route");
    metroPlan.querySelectorAll(".is-route-teil, .is-gewaehlt, .is-hell").forEach(function (el) {
      el.classList.remove("is-route-teil", "is-gewaehlt", "is-hell");
    });
    if (routeLeiste) routeLeiste.hidden = true;
    if (/#route=/.test(location.hash)) history.replaceState(null, "", location.pathname);
  }

  function metroMarkieren(id) {
    if (!metroPlan) return;
    metroZuruecksetzen();

    var ziel = metroPlan.querySelector('[data-halt="' + id + '"]');
    if (!ziel) return;

    /* Zur Route gehören nicht nur die formalen Abhängigkeiten, sondern auch
       alle früheren Halte auf denselben Linien: durch die fährt man mit. */
    var route = {};
    var stapel = [id];
    while (stapel.length) {
      var k = stapel.pop();
      if (route[k] || !knoten[k]) continue;
      route[k] = true;
      knoten[k].braucht.forEach(function (n) { stapel.push(n); });
      knoten[k].vorher.forEach(function (n) { stapel.push(n); });
    }

    metroPlan.classList.add("is-route");
    ziel.classList.add("is-gewaehlt");

    var offen = 0;
    var bahnen = {};
    metroPlan.querySelectorAll("[data-halt]").forEach(function (halt) {
      if (!route[halt.dataset.halt]) return;
      halt.classList.add("is-route-teil");
      if (!halt.classList.contains("me__halt--erreicht")) offen++;
      var bahn = halt.style.getPropertyValue("--f");
      if (bahn) bahnen[bahn] = true;
    });

    metroPlan.querySelectorAll("[data-bis]").forEach(function (seg) {
      if (route[seg.dataset.bis]) seg.classList.add("is-route-teil");
    });

    var umstiege = 0;
    metroPlan.querySelectorAll(".me__quer").forEach(function (q) {
      if (route[q.dataset.von] && route[q.dataset.nach]) {
        q.classList.add("is-route-teil");
        umstiege++;
      }
    });

    // Route in den Link schreiben, damit sie teilbar ist
    history.replaceState(null, "", "#route=" + id);

    if (routeLeiste && routeText) {
      var gesamt = Object.keys(route).length;
      var titel = ziel.querySelector(".me__halt-label");
      routeText.textContent =
        "Weg zu „" + (titel ? titel.textContent.trim() : id) + "“: " +
        gesamt + " Schritte über " + Object.keys(bahnen).length + " Bahnen, " +
        offen + " davon noch offen" +
        (umstiege ? ", " + umstiege + " Umstieg" + (umstiege > 1 ? "e" : "") : "") + ".";
      routeLeiste.hidden = false;
    }
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

  /* --- Popover verschieben ---------------------------------------------
     Die Position gilt nur für das geöffnete Fenster. Beim nächsten Öffnen
     setzt platziere() es wieder neben den Auslöser. */
  if (pop) {
    var zieht = false;
    var versatzX = 0;
    var versatzY = 0;

    pop.addEventListener("pointerdown", function (e) {
      // Nur an ruhigen Stellen greifen, nicht auf Knöpfen oder Text zum Markieren
      if (e.target.closest("button") || e.target.closest("a")) return;
      if (!e.target.closest(".k-detail__kopf") && e.target !== pop) return;

      var r = pop.getBoundingClientRect();
      versatzX = e.clientX - r.left;
      versatzY = e.clientY - r.top;
      zieht = true;
      pop.classList.add("wird-gezogen");
      pop.setPointerCapture(e.pointerId);
      e.preventDefault();
    });

    pop.addEventListener("pointermove", function (e) {
      if (!zieht) return;
      var links = Math.min(Math.max(4, e.clientX - versatzX), window.innerWidth - pop.offsetWidth - 4);
      var oben = Math.min(Math.max(4, e.clientY - versatzY), window.innerHeight - pop.offsetHeight - 4);
      pop.style.left = Math.round(links) + "px";
      pop.style.top = Math.round(oben) + "px";
    });

    ["pointerup", "pointercancel"].forEach(function (ev) {
      pop.addEventListener(ev, function () {
        zieht = false;
        pop.classList.remove("wird-gezogen");
      });
    });
  }

  wurzel.addEventListener("click", function (e) {
    if (e.target.closest("[data-pop-zu]")) { schliesse(); return; }
    if (e.target.closest("[data-metro-reset]")) { metroZuruecksetzen(); schliesse(); return; }

    var ausloeser = e.target.closest("[data-schritt]");
    if (ausloeser) {
      zeigeDetail(ausloeser.dataset.schritt, ausloeser.closest("[data-pop]") ? null : ausloeser);
      return;
    }
  });

  // Klick ins Leere schließt das Popover und hebt die Route auf
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-pop]")) return;
    if (e.target.closest("[data-schritt]")) return;
    if (e.target.closest("[data-route-leiste]")) return;

    if (pop && !pop.hidden) schliesse();
    if (metroPlan && metroPlan.classList.contains("is-route")) metroZuruecksetzen();
    if (graphFlaeche && graphFlaeche.classList.contains("is-auswahl")) graphZuruecksetzen();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && pop && !pop.hidden) schliesse();
  });

  window.addEventListener("resize", schliesse);

  /* --- Route aus dem Link vorauswählen --------------------------------- */
  if (metroPlan) {
    var routeHash = (location.hash.match(/route=([a-z0-9_-]+)/i) || [])[1];
    if (routeHash) metroMarkieren(routeHash);
  }

})();
