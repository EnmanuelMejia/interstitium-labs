/* Interstitium Labs — rAF governor (2026-10-09 perf).
 * Pauses ALL requestAnimationFrame callbacks while the document is hidden
 * (background tab), flushing them on return. Prevents battery drain and
 * main-thread saturation from canvas animations in hidden tabs.
 * Safe: preserves cancelAnimationFrame semantics for queued callbacks. */
(function () {
  'use strict';
  try {
    var origRAF = window.requestAnimationFrame.bind(window);
    var origCAF = window.cancelAnimationFrame.bind(window);
    var queue = [];
    var nextId = 1;
    window.requestAnimationFrame = function (cb) {
      if (typeof cb !== 'function') return origRAF(cb);
      if (document.hidden) {
        var id = nextId++;
        queue.push({ id: id, cb: cb });
        return id;
      }
      return origRAF(cb);
    };
    window.cancelAnimationFrame = function (id) {
      for (var i = 0; i < queue.length; i++) {
        if (queue[i].id === id) { queue.splice(i, 1); return; }
      }
      origCAF(id);
    };
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden && queue.length) {
        var q = queue; queue = [];
        for (var i = 0; i < q.length; i++) { origRAF(q[i].cb); }
      }
    });
  } catch (e) { /* fail-open: leave native rAF untouched */ }
})();

/* Interstitium Labs — theme boot + toggle (2026-10-01).
 * Dark mode is the default across the board. This script runs
 * synchronously in <head> so <html data-theme> is set before first
 * paint (no flash). The toggle is injected into the pill nav once the
 * DOM is ready; the choice persists in localStorage ("il-theme"). */
(function () {
  var root = document.documentElement;
  var KEY = "il-theme";

  function resolve() {
    try {
      var saved = window.localStorage.getItem(KEY);
      return saved === "light" ? "light" : "dark";
    } catch (e) {
      return "dark";
    }
  }

  function current() {
    return root.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  root.setAttribute("data-theme", resolve());

  var SUN =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  var MOON =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';

  var btn = null;

  function paint() {
    if (!btn) return;
    var isDark = current() === "dark";
    btn.innerHTML = isDark ? MOON : SUN;
    btn.setAttribute(
      "aria-label",
      isDark ? "Switch to light mode" : "Switch to dark mode"
    );
    btn.title = isDark ? "Light mode" : "Dark mode";
  }

  /* Keep the browser-chrome theme-color in sync with the active theme. */
  function paintChrome() {
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", current() === "dark" ? "#0a0f1d" : "#f7f4ee");
  }

  function toggle() {
    var next = current() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try {
      window.localStorage.setItem(KEY, next);
    } catch (e) {}
    paint();
    paintChrome();
  }

  function mount() {
    if (document.getElementById("il-theme-toggle")) return;
    var host =
      document.querySelector(".il-pillnav__row > div:last-child") ||
      document.querySelector(".il-pillnav__row") ||
      document.querySelector(".il-pillnav");
    if (!host) return;
    btn = document.createElement("button");
    btn.id = "il-theme-toggle";
    btn.type = "button";
    btn.className = "il-theme-toggle";
    btn.addEventListener("click", toggle);
    host.insertBefore(btn, host.firstChild);
    paint();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      mount();
      paintChrome();
    });
  } else {
    mount();
    paintChrome();
  }
})();

/* Interstitium Labs — back-to-top (2026-10-09). A floating gold button
 * appears once the reader scrolls past ~600px on every page; clicking it
 * smooth-scrolls to the top. Injected here because il-theme.js already
 * loads synchronously on every page. */
(function () {
  function initTop() {
    if (document.getElementById("il-to-top")) return;
    var b = document.createElement("button");
    b.id = "il-to-top";
    b.type = "button";
    b.className = "il-to-top";
    b.setAttribute("aria-label", "Scroll back to top");
    b.title = "Back to top";
    b.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>';
    b.addEventListener("click", function () {
      try {
        window.scrollTo({ top: 0, behavior: "smooth" });
      } catch (e) {
        window.scrollTo(0, 0);
      }
    });
    document.body.appendChild(b);
    var onScroll = function () {
      var y = window.pageYOffset || document.documentElement.scrollTop || 0;
      b.classList.toggle("il-to-top--show", y > 600);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTop);
  } else {
    initTop();
  }
})();
