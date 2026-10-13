/* Farbwahl für die AVRG-Landingpages: ?farbe=rot|blau|gruen|gelb, sonst die zuletzt gewählte.
   Läuft im <head>, damit die Seite gleich in der richtigen Farbe erscheint. */
(function () {
  var FARBEN = ['rot', 'blau', 'gruen', 'gelb'];
  var wahl = new URLSearchParams(location.search).get('farbe');
  if (FARBEN.indexOf(wahl) < 0) { try { wahl = localStorage.getItem('avrg-farbe'); } catch (e) { wahl = null; } }
  if (FARBEN.indexOf(wahl) < 0) wahl = 'rot';
  document.documentElement.setAttribute('data-farbe', wahl);
  // Eingebettet (Vorschau auf der Kampagnenseite) oder als Bild: ohne Arbeitsleiste
  if (window.self !== window.top || new URLSearchParams(location.search).has('vorschau')) document.documentElement.classList.add('ist-eingebettet');

  function setze(f) {
    document.documentElement.setAttribute('data-farbe', f);
    try { localStorage.setItem('avrg-farbe', f); } catch (e) {}
    var u = new URL(location.href); u.searchParams.set('farbe', f);
    history.replaceState(null, '', u);
    markiere(f);
  }
  function markiere(f) {
    document.querySelectorAll('[data-farbe-wahl]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-farbe-wahl') === f ? 'true' : 'false');
    });
    // Links zu den anderen Varianten nehmen die Farbe mit
    document.querySelectorAll('[data-mit-farbe]').forEach(function (a) {
      var u = new URL(a.getAttribute('href'), location.href); u.searchParams.set('farbe', f);
      a.setAttribute('href', u.pathname + u.search);
    });
  }
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-farbe-wahl]').forEach(function (b) {
      b.addEventListener('click', function () { setze(b.getAttribute('data-farbe-wahl')); });
    });
    markiere(document.documentElement.getAttribute('data-farbe'));
  });
})();
