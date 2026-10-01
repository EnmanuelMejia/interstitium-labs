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

  function toggle() {
    var next = current() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try {
      window.localStorage.setItem(KEY, next);
    } catch (e) {}
    paint();
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
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
