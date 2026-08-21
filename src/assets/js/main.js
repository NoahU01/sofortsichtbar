/* =========================================================
   sofort sichtbar – Interaktionen
   Reine Vanilla-Module, jedes läuft unabhängig.
   ========================================================= */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Navigation ---------------------------------------------------- */
  function initNav() {
    var toggle = document.querySelector(".nav__toggle");
    var menu = document.getElementById("nav-menu");
    var header = document.querySelector(".nav");
    if (!toggle || !menu || !header) return;

    function setNavHeight() {
      document.documentElement.style.setProperty(
        "--nav-height",
        header.getBoundingClientRect().height + "px"
      );
    }
    setNavHeight();
    window.addEventListener("resize", setNavHeight, { passive: true });

    function close() {
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Menü öffnen");
      menu.classList.remove("is-open");
      document.body.classList.remove("is-locked");
    }

    function open() {
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Menü schließen");
      menu.classList.add("is-open");
      document.body.classList.add("is-locked");
    }

    toggle.addEventListener("click", function () {
      toggle.getAttribute("aria-expanded") === "true" ? close() : open();
    });

    // Menü nach Klick auf einen Link schließen
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) close();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        close();
        toggle.focus();
      }
    });

    // Beim Wechsel auf Desktop-Breite aufräumen
    var desktop = window.matchMedia("(min-width: 992px)");
    desktop.addEventListener("change", function (e) {
      if (e.matches) close();
    });
  }

  /* --- Pricing-Tabs --------------------------------------------------- */
  function initTabs() {
    document.querySelectorAll("[data-tabs]").forEach(function (root) {
      var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
      if (!tabs.length) return;

      function select(tab) {
        tabs.forEach(function (t) {
          var active = t === tab;
          t.setAttribute("aria-selected", active ? "true" : "false");
          t.setAttribute("tabindex", active ? "0" : "-1");
          var panel = document.getElementById(t.getAttribute("aria-controls"));
          if (panel) panel.hidden = !active;
        });
      }

      tabs.forEach(function (tab, i) {
        tab.addEventListener("click", function () { select(tab); });
        tab.addEventListener("keydown", function (e) {
          var next = null;
          if (e.key === "ArrowRight") next = tabs[(i + 1) % tabs.length];
          if (e.key === "ArrowLeft") next = tabs[(i - 1 + tabs.length) % tabs.length];
          if (!next) return;
          e.preventDefault();
          select(next);
          next.focus();
        });
      });
    });
  }

  /* --- FAQ-Akkordeon -------------------------------------------------- */
  function initAccordion() {
    document.querySelectorAll(".faq__question").forEach(function (button) {
      button.addEventListener("click", function () {
        var open = button.getAttribute("aria-expanded") === "true";
        button.setAttribute("aria-expanded", open ? "false" : "true");
      });
    });
  }

  /* --- Endlos-Marquee (Themen-Slider) --------------------------------- */
  function initMarquee() {
    document.querySelectorAll("[data-marquee]").forEach(function (wrapper) {
      wrapper.querySelectorAll("[data-marquee-track]").forEach(function (track) {
        var speed = parseFloat(track.dataset.speed) || 0.5;
        var originals = Array.prototype.slice.call(track.children);
        if (!originals.length) return;

        var offset = 0;
        var loopWidth = 0;
        var running = false;

        function measure() {
          // Track auf die Originale zurücksetzen und neu klonen
          track.innerHTML = "";
          originals.forEach(function (el) { track.appendChild(el); });

          loopWidth = originals.reduce(function (sum, el) {
            var style = getComputedStyle(el);
            return sum + el.getBoundingClientRect().width +
              (parseFloat(style.marginLeft) || 0) + (parseFloat(style.marginRight) || 0);
          }, 0);
          // Lücke zwischen den Elementen mitzählen
          loopWidth += (parseFloat(getComputedStyle(track).columnGap) || 0) * originals.length;
          if (!loopWidth) return;

          var target = wrapper.getBoundingClientRect().width * 2 + loopWidth;
          var width = loopWidth;
          while (width < target) {
            originals.forEach(function (el) { track.appendChild(el.cloneNode(true)); });
            width += loopWidth;
          }
        }

        function frame() {
          if (loopWidth) {
            offset -= speed;
            if (offset <= -loopWidth) offset += loopWidth;
            track.style.transform = "translate3d(" + offset + "px,0,0)";
          }
          requestAnimationFrame(frame);
        }

        measure();
        // Bilder und Schriften ändern die Maße nachträglich
        window.addEventListener("load", measure);
        var resizeTimer;
        window.addEventListener("resize", function () {
          clearTimeout(resizeTimer);
          resizeTimer = setTimeout(measure, 150);
        }, { passive: true });

        if (!reduceMotion && !running) { running = true; requestAnimationFrame(frame); }
      });
    });
  }

  /* --- Themen-Filter (/vertriebsstrecken) ----------------------------- */
  function initThemeFilter() {
    var buttons = document.querySelectorAll("[data-theme-filter]");
    if (!buttons.length) return;

    var lists = {};
    document.querySelectorAll("[data-theme-list]").forEach(function (el) {
      lists[el.dataset.themeList] = el;
    });

    function apply(value) {
      // "all" zeigt beide Listen, "anspracheanlaesse" nur die Anlässe,
      // alles andere nur die Zielgruppen – gefiltert nach ihrem Wert.
      var onlyAnlaesse = value === "anspracheanlaesse";
      var showAll = value === "all";

      if (lists.zielgruppen) lists.zielgruppen.hidden = onlyAnlaesse;
      if (lists.anlaesse) lists.anlaesse.hidden = !(showAll || onlyAnlaesse);

      document.querySelectorAll(".theme-card[data-theme-value]").forEach(function (card) {
        card.hidden = !(showAll || onlyAnlaesse || card.dataset.themeValue === value);
      });

      buttons.forEach(function (b) {
        var active = b.dataset.themeFilter === value;
        b.classList.toggle("is-active", active);
        b.setAttribute("aria-selected", active ? "true" : "false");
      });
    }

    buttons.forEach(function (b) {
      b.addEventListener("click", function () { apply(b.dataset.themeFilter); });
    });

    apply("all");
  }

  /* --- Anker-Links weich scrollen ------------------------------------- */
  function initAnchors() {
    function samePage(link) {
      return link.pathname === location.pathname && link.hash && link.hash.length > 1;
    }

    document.addEventListener("click", function (e) {
      var link = e.target.closest('a[href*="#"]');
      if (!link || link.target === "_blank" || !samePage(link)) return;

      var target = document.querySelector(link.hash);
      if (!target) return;

      e.preventDefault();
      target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
      history.pushState(null, "", link.hash);
    });

    // Aufruf mit Hash von einer anderen Seite: erst nach dem Layout scrollen
    if (location.hash.length > 1) {
      var target = document.querySelector(location.hash);
      if (target) {
        window.addEventListener("load", function () {
          target.scrollIntoView({ behavior: "auto", block: "start" });
        });
      }
    }
  }

  /* --- Scroll-Reveal --------------------------------------------------- */
  function initReveal() {
    var els = document.querySelectorAll(".reveal");
    if (!els.length) return;

    if (reduceMotion || !("IntersectionObserver" in window)) {
      els.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.05 });

    els.forEach(function (el) { observer.observe(el); });
  }

  function init() {
    initNav();
    initTabs();
    initAccordion();
    initMarquee();
    initThemeFilter();
    initAnchors();
    initReveal();
  }

  document.readyState === "loading"
    ? document.addEventListener("DOMContentLoaded", init)
    : init();
})();
