/**
 * Interstitium Labs — namespaced local progress (vanilla, no build).
 * Keys: il.progress.<scope>.<id>
 * Public API: window.ILProgress
 */
(function (global) {
  "use strict";
  var PREFIX = "il.progress.";

  function key(scope, id) {
    return PREFIX + String(scope) + "." + String(id);
  }

  function today() {
    return new Date().toISOString().slice(0, 10);
  }

  function safeParse(raw, fallback) {
    try {
      if (raw == null) return fallback;
      return JSON.parse(raw);
    } catch (e) {
      return fallback;
    }
  }

  function getJSON(scope, id, fallback) {
    return safeParse(global.localStorage.getItem(key(scope, id)), fallback);
  }

  function setJSON(scope, id, value) {
    global.localStorage.setItem(key(scope, id), JSON.stringify(value));
  }

  function getBool(scope, id) {
    return global.localStorage.getItem(key(scope, id)) === "1";
  }

  function setBool(scope, id, on) {
    if (on) global.localStorage.setItem(key(scope, id), "1");
    else global.localStorage.removeItem(key(scope, id));
  }

  function toggleBool(scope, id) {
    var next = !getBool(scope, id);
    setBool(scope, id, next);
    return next;
  }

  /** Streak object: { count, last } under il.progress.<scope>.streak */
  function loadStreak(scope) {
    return getJSON(scope, "streak", { count: 0, last: null });
  }

  function bumpStreak(scope) {
    var s = loadStreak(scope);
    var d = today();
    if (s.last === d) return s;
    var y = new Date();
    y.setDate(y.getDate() - 1);
    var ymd = y.toISOString().slice(0, 10);
    s.count = s.last === ymd ? s.count + 1 : 1;
    s.last = d;
    setJSON(scope, "streak", s);
    return s;
  }

  function listKeys(scope) {
    var out = [];
    var needle = PREFIX + scope + ".";
    for (var i = 0; i < global.localStorage.length; i++) {
      var k = global.localStorage.key(i);
      if (k && k.indexOf(needle) === 0) out.push(k);
    }
    return out;
  }

  function clearScope(scope) {
    listKeys(scope).forEach(function (k) {
      global.localStorage.removeItem(k);
    });
  }

  /**
   * Bind checklist: [data-il-progress="scope:id"] on checkbox or button.
   * Optional [data-il-streak-scope="scope"] bump on check.
   * Optional #il-streak-<scope> text content updated with count.
   */
  function bindChecklist(root) {
    root = root || global.document;
    var nodes = root.querySelectorAll("[data-il-progress]");
    nodes.forEach(function (el) {
      var spec = el.getAttribute("data-il-progress") || "";
      var parts = spec.split(":");
      if (parts.length < 2) return;
      var scope = parts[0];
      var id = parts.slice(1).join(":");
      var on = getBool(scope, id);

      if (el.type === "checkbox") {
        el.checked = on;
        el.setAttribute("aria-checked", on ? "true" : "false");
        el.addEventListener("change", function () {
          setBool(scope, id, el.checked);
          el.setAttribute("aria-checked", el.checked ? "true" : "false");
          if (el.checked) {
            var streakScope = el.getAttribute("data-il-streak-scope") || scope;
            bumpStreak(streakScope);
            paintStreak(streakScope);
          }
          paintCounts(scope);
          el.dispatchEvent(new CustomEvent("il:progress", { bubbles: true, detail: { scope: scope, id: id, on: el.checked } }));
        });
      } else {
        el.setAttribute("aria-pressed", on ? "true" : "false");
        if (on) el.classList.add("is-done");
        el.addEventListener("click", function () {
          var next = toggleBool(scope, id);
          el.setAttribute("aria-pressed", next ? "true" : "false");
          el.classList.toggle("is-done", next);
          if (next) {
            var streakScope = el.getAttribute("data-il-streak-scope") || scope;
            bumpStreak(streakScope);
            paintStreak(streakScope);
          }
          paintCounts(scope);
        });
      }
    });

    // paint all streak scopes found
    var streakEls = root.querySelectorAll("[data-il-streak]");
    streakEls.forEach(function (el) {
      paintStreak(el.getAttribute("data-il-streak"), el);
    });
    var countEls = root.querySelectorAll("[data-il-count-scope]");
    countEls.forEach(function (el) {
      paintCounts(el.getAttribute("data-il-count-scope"), el);
    });
  }

  function paintStreak(scope, el) {
    var target = el || global.document.querySelector('[data-il-streak="' + scope + '"]');
    if (!target) return;
    var s = loadStreak(scope);
    target.textContent = String(s.count || 0);
  }

  function paintCounts(scope, el) {
    var target = el || global.document.querySelector('[data-il-count-scope="' + scope + '"]');
    if (!target) return;
    var totalAttr = target.getAttribute("data-il-count-total");
    var idsAttr = target.getAttribute("data-il-count-ids");
    var done = 0;
    var total = 0;
    if (idsAttr) {
      var ids = idsAttr.split(",").map(function (s) { return s.trim(); }).filter(Boolean);
      total = ids.length;
      ids.forEach(function (id) { if (getBool(scope, id)) done++; });
    } else if (totalAttr) {
      total = parseInt(totalAttr, 10) || 0;
      var nodes = global.document.querySelectorAll('[data-il-progress^="' + scope + ':"]');
      nodes.forEach(function (n) {
        var spec = n.getAttribute("data-il-progress");
        var id = spec.split(":").slice(1).join(":");
        if (getBool(scope, id)) done++;
      });
      if (!total) total = nodes.length;
    }
    target.textContent = done + "/" + total;
    var bar = global.document.querySelector('[data-il-bar="' + scope + '"]');
    if (bar && total) {
      bar.style.width = Math.round((done / total) * 100) + "%";
      bar.setAttribute("aria-valuenow", String(done));
      bar.setAttribute("aria-valuemax", String(total));
    }
  }

  global.ILProgress = {
    PREFIX: PREFIX,
    key: key,
    getBool: getBool,
    setBool: setBool,
    toggleBool: toggleBool,
    getJSON: getJSON,
    setJSON: setJSON,
    loadStreak: loadStreak,
    bumpStreak: bumpStreak,
    clearScope: clearScope,
    bindChecklist: bindChecklist,
    paintStreak: paintStreak,
    paintCounts: paintCounts,
  };

  if (global.document && global.document.readyState === "loading") {
    global.document.addEventListener("DOMContentLoaded", function () {
      bindChecklist(global.document);
    });
  } else if (global.document) {
    bindChecklist(global.document);
  }
})(typeof window !== "undefined" ? window : this);
