/* Interstitium Labs — nav behavior (il-nav.js)
   Mega-dropdown toggles + active-link marking. No dependencies.
   Safe to load multiple times (guards on data-il-nav-init). */
(function () {
  "use strict";
  if (document.documentElement.hasAttribute("data-il-nav-init")) return;
  document.documentElement.setAttribute("data-il-nav-init", "1");

  function closeAll(except) {
    document.querySelectorAll('[data-il-navdrop][data-open="true"]').forEach(function (d) {
      if (d !== except) { d.setAttribute("data-open", "false"); caret(d, false); }
    });
  }
  function caret(drop, open) {
    var c = drop.querySelector(".il-navdrop__caret");
    if (c) c.setAttribute("aria-expanded", open ? "true" : "false");
  }

  document.querySelectorAll("[data-il-navdrop]").forEach(function (drop) {
    var btn = drop.querySelector(".il-navdrop__caret");
    if (!btn) return;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var isOpen = drop.getAttribute("data-open") === "true";
      closeAll(drop);
      drop.setAttribute("data-open", isOpen ? "false" : "true");
      caret(drop, !isOpen);
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest || !e.target.closest("[data-il-navdrop]")) closeAll(null);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeAll(null);
  });

  // Mark the active section link (works for both plain links and dropdown links).
  try {
    var path = location.pathname;
    document.querySelectorAll(".il-pillnav__links a[data-navkey]").forEach(function (a) {
      var key = a.getAttribute("data-navkey");
      if (key && (path === key || path.indexOf(key) === 0) && key !== "/") {
        a.setAttribute("aria-current", "page");
      }
    });
  } catch (err) { /* never break nav for a cosmetic mark */ }
})();
