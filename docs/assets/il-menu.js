/**
 * Interstitium Labs — mobile menu sheet + bottom-nav active state (vanilla).
 * - Hamburger (#il-menu-btn) toggles the all-destinations sheet (#il-menu-sheet).
 * - Marks the current tab in nav[aria-label="App"] with aria-current="page".
 * Safe to load with defer; idempotent; no-ops on pages without the markup.
 */
(function (g) {
  "use strict";
  var d = g.document;
  if (!d || d.__IL_MENU__) return;
  d.__IL_MENU__ = true;

  /* ---------- Bottom-nav active state ---------- */
  function markActiveNav() {
    var nav = d.querySelector('nav[aria-label="App"]');
    if (!nav) return;
    var path = (g.location && g.location.pathname ? g.location.pathname : "/").replace(/\/+$/, "") || "/";
    var links = nav.querySelectorAll('a[href]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = a.getAttribute("href") || "";
      if (href.charAt(0) !== "/") continue;
      var p = href.replace(/\/+$/, "") || "/";
      var active = p === "/" ? path === "/" : path === p || path.indexOf(p + "/") === 0;
      if (active) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    }
  }

  /* ---------- Menu sheet ---------- */
  function initSheet() {
    var btn = d.getElementById("il-menu-btn");
    var sheet = d.getElementById("il-menu-sheet");
    if (!btn || !sheet) return;
    var panel = sheet.querySelector(".il-menu-panel");
    var lastFocus = null;

    function open() {
      lastFocus = d.activeElement;
      sheet.hidden = false;
      btn.setAttribute("aria-expanded", "true");
      var close = sheet.querySelector("[data-il-menu-close]");
      if (close && close.focus) close.focus();
      d.addEventListener("keydown", onKey);
    }
    function close() {
      if (sheet.hidden) return;
      sheet.hidden = true;
      btn.setAttribute("aria-expanded", "false");
      d.removeEventListener("keydown", onKey);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    function onKey(e) {
      if (e.key === "Escape") close();
    }
    btn.addEventListener("click", function () {
      if (sheet.hidden) open();
      else close();
    });
    var closers = sheet.querySelectorAll("[data-il-menu-close]");
    for (var i = 0; i < closers.length; i++) {
      closers[i].addEventListener("click", close);
    }
    // Close when a destination is chosen.
    var links = sheet.querySelectorAll('a[href]');
    for (var j = 0; j < links.length; j++) {
      links[j].addEventListener("click", close);
    }
    if (panel) panel.addEventListener("click", function (e) { e.stopPropagation(); });
  }

  function ready() {
    markActiveNav();
    initSheet();
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", ready, { once: true });
  else ready();
})(window);
