/**
 * Interstitium Labs — Paths OS (directory filters + per-path progress).
 * Storage: localStorage key il.paths.v1
 * Schema: /assets/il-paths.json
 * Public: window.ILPaths
 */
(function (global) {
  "use strict";

  var STORAGE = "il.paths.v1";
  var DATA_URL = "/assets/il-paths.json";
  var cache = null;

  function safeParse(raw, fallback) {
    try {
      if (raw == null) return fallback;
      return JSON.parse(raw);
    } catch (e) {
      return fallback;
    }
  }

  function loadState() {
    var s = safeParse(global.localStorage.getItem(STORAGE), null);
    if (!s || typeof s !== "object") {
      s = { version: 1, paths: {}, updated: null };
    }
    if (!s.paths) s.paths = {};
    return s;
  }

  function saveState(s) {
    try {
      s.updated = new Date().toISOString();
      global.localStorage.setItem(STORAGE, JSON.stringify(s));
    } catch (e) {}
  }

  function pathState(id) {
    var s = loadState();
    if (!s.paths[id]) {
      s.paths[id] = { started: false, phases: {}, evidence: [], last: null };
    }
    return s.paths[id];
  }

  function startPath(id) {
    var s = loadState();
    if (!s.paths[id]) s.paths[id] = { started: false, phases: {}, evidence: [], last: null };
    s.paths[id].started = true;
    s.paths[id].last = new Date().toISOString();
    saveState(s);
    return s.paths[id];
  }

  function togglePhase(pathId, phaseId, on) {
    var s = loadState();
    if (!s.paths[pathId]) s.paths[pathId] = { started: true, phases: {}, evidence: [], last: null };
    s.paths[pathId].started = true;
    s.paths[pathId].phases[phaseId] = !!on;
    s.paths[pathId].last = new Date().toISOString();
    saveState(s);
    return s.paths[pathId];
  }

  function addEvidence(pathId, note) {
    var s = loadState();
    if (!s.paths[pathId]) s.paths[pathId] = { started: true, phases: {}, evidence: [], last: null };
    s.paths[pathId].evidence = s.paths[pathId].evidence || [];
    s.paths[pathId].evidence.push({ t: new Date().toISOString(), note: String(note || "").slice(0, 280) });
    if (s.paths[pathId].evidence.length > 40) s.paths[pathId].evidence = s.paths[pathId].evidence.slice(-40);
    s.paths[pathId].last = new Date().toISOString();
    saveState(s);
    return s.paths[pathId];
  }

  function progressPct(pathId, phaseCount) {
    var ps = pathState(pathId);
    var n = phaseCount || 0;
    if (!n) return 0;
    var done = 0;
    Object.keys(ps.phases || {}).forEach(function (k) {
      if (ps.phases[k]) done++;
    });
    return Math.round((done / n) * 100);
  }

  function fetchPaths() {
    if (cache) return Promise.resolve(cache);
    return fetch(DATA_URL, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("paths json " + r.status);
        return r.json();
      })
      .then(function (data) {
        cache = data;
        return data;
      });
  }

  function matchesFilters(p, f) {
    if (f.role && f.role !== "all") {
      if (!(p.role || []).includes(f.role)) return false;
    }
    if (f.skill && f.skill !== "all") {
      if (!(p.skill || []).includes(f.skill)) return false;
    }
    if (f.cert && f.cert !== "all") {
      if (!(p.cert || []).includes(f.cert) && f.cert !== "any") return false;
      if (f.cert === "any" && !(p.cert || []).length) return false;
    }
    if (f.time && f.time !== "all") {
      if (p.time_band !== f.time) return false;
    }
    if (f.q) {
      var hay = (p.id + " " + p.title + " " + (p.tagline || "") + " " + (p.outcomes || []).join(" ")).toLowerCase();
      if (hay.indexOf(f.q.toLowerCase()) < 0) return false;
    }
    return true;
  }

  function unique(arr) {
    var o = {};
    (arr || []).forEach(function (x) {
      o[x] = true;
    });
    return Object.keys(o).sort();
  }

  function renderDirectory(root) {
    if (!root) return;
    fetchPaths()
      .then(function (data) {
        var paths = data.paths || [];
        var filtersEl = root.querySelector("[data-il-path-filters]");
        var grid = root.querySelector("[data-il-path-grid]");
        var countEl = root.querySelector("[data-il-path-count]");
        if (!grid) return;

        var roles = unique(
          paths.reduce(function (a, p) {
            return a.concat(p.role || []);
          }, [])
        );
        var skills = unique(
          paths.reduce(function (a, p) {
            return a.concat(p.skill || []);
          }, [])
        );
        var times = unique(
          paths.map(function (p) {
            return p.time_band;
          }).filter(Boolean)
        );

        if (filtersEl && !filtersEl.getAttribute("data-ready")) {
          filtersEl.setAttribute("data-ready", "1");
          filtersEl.innerHTML =
            '<div class="flex flex-wrap gap-3">' +
            selectHTML("role", "Role / Rol", ["all"].concat(roles), "all") +
            selectHTML("skill", "Skill", ["all"].concat(skills), "all") +
            selectHTML("cert", "Cert", ["all", "any", "cka", "cks", "az-104", "az-400", "clf-c02", "lf-essentials", "google-data-analytics", "ibm-ds", "nvidia-dli"], "all") +
            selectHTML("time", "Time / Tiempo", ["all"].concat(times), "all") +
            '<label class="flex min-w-[12rem] flex-1 flex-col gap-1 font-mono text-[0.58rem] uppercase tracking-[0.18em] text-muted">' +
            '<span data-i18n="paths.filter_search">Search</span>' +
            '<input type="search" data-il-filter="q" placeholder="k8s, sql, hire…" class="h-10 rounded-lg border border-paper/15 bg-void px-3 font-sans text-sm normal-case tracking-normal text-paper placeholder:text-muted"/>' +
            "</label></div>";
          filtersEl.addEventListener("change", redraw);
          filtersEl.addEventListener("input", redraw);
        }

        function currentFilters() {
          var f = { role: "all", skill: "all", cert: "all", time: "all", q: "" };
          root.querySelectorAll("[data-il-filter]").forEach(function (el) {
            f[el.getAttribute("data-il-filter")] = el.value || "all";
            if (el.getAttribute("data-il-filter") === "q") f.q = el.value || "";
          });
          return f;
        }

        function redraw() {
          var f = currentFilters();
          var lang = (global.document.documentElement.lang || "en").toLowerCase().indexOf("es") === 0 ? "es" : "en";
          var list = paths.filter(function (p) {
            return matchesFilters(p, f);
          });
          // Featured core first
          list.sort(function (a, b) {
            var aw = (a.featured ? 0 : 10) + (a.nest === "core" ? 0 : 1);
            var bw = (b.featured ? 0 : 10) + (b.nest === "core" ? 0 : 1);
            return aw - bw || (a.title || "").localeCompare(b.title || "");
          });
          if (countEl) {
            countEl.textContent =
              list.length + (lang === "es" ? " rutas" : " paths");
          }
          grid.innerHTML = list
            .map(function (p) {
              return cardHTML(p, lang);
            })
            .join("");
        }

        redraw();
      })
      .catch(function (err) {
        gridError(root, err);
      });
  }

  function selectHTML(key, label, options, selected) {
    var opts = options
      .map(function (o) {
        return '<option value="' + esc(o) + '"' + (o === selected ? " selected" : "") + ">" + esc(o) + "</option>";
      })
      .join("");
    return (
      '<label class="flex min-w-[9rem] flex-col gap-1 font-mono text-[0.58rem] uppercase tracking-[0.18em] text-muted">' +
      "<span>" +
      esc(label) +
      "</span>" +
      '<select data-il-filter="' +
      esc(key) +
      '" class="h-10 rounded-lg border border-paper/15 bg-void px-2 font-sans text-sm normal-case tracking-normal text-paper">' +
      opts +
      "</select></label>"
    );
  }

  function cardHTML(p, lang) {
    var title = lang === "es" && p.title_es ? p.title_es : p.title;
    var tag = lang === "es" && p.tagline_es ? p.tagline_es : p.tagline;
    var hero = lang === "es" && p.hero_do_es ? p.hero_do_es : p.hero_do;
    var pct = progressPct(p.id, (p.phases || []).length);
    var nest = p.nest || "core";
    var border = p.featured ? "border border-cyan/25" : "";
    return (
      '<a href="/paths/' +
      esc(p.id) +
      '/" class="il-surface rounded-xl bg-panel p-6 shadow-[0_0_0_1px_rgba(232,238,245,0.08)] sm:p-7 ' +
      border +
      '" data-path-id="' +
      esc(p.id) +
      '" data-role="' +
      esc((p.role || []).join(" ")) +
      '" data-skill="' +
      esc((p.skill || []).join(" ")) +
      '" data-cert="' +
      esc((p.cert || []).join(" ")) +
      '" data-time="' +
      esc(p.time_band || "") +
      '" data-lang-en="1" data-lang-es="1">' +
      '<div class="flex flex-wrap items-center justify-between gap-2">' +
      '<p class="font-mono text-[0.62rem] uppercase tracking-[0.22em] text-gold">' +
      esc(nest) +
      " · " +
      esc(String(p.duration_weeks || "?")) +
      "w · " +
      esc(p.difficulty || "") +
      "</p>" +
      (pct
        ? '<p class="font-mono text-[0.58rem] uppercase tracking-[0.14em] text-cyan">' + pct + "%</p>"
        : "") +
      "</div>" +
      '<h3 class="mt-3 font-display text-2xl tracking-[-0.02em]">' +
      esc(title) +
      "</h3>" +
      '<p class="mt-2 text-sm font-medium text-paper/90">' +
      esc(hero || tag) +
      "</p>" +
      '<p class="mt-2 text-sm text-muted">' +
      esc(tag) +
      "</p>" +
      '<p class="mt-5 font-mono text-[0.62rem] uppercase tracking-[0.18em] text-cyan">Enter →</p>' +
      "</a>"
    );
  }

  function gridError(root, err) {
    var grid = root.querySelector("[data-il-path-grid]");
    if (grid) {
      grid.innerHTML =
        '<p class="text-sm text-muted">Path catalog failed to load. Open <a class="text-cyan" href="/assets/il-paths.json">il-paths.json</a>.</p>';
    }
    if (global.console && console.warn) console.warn("ILPaths", err);
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /** Bind a path detail page: [data-il-path-page="id"] */
  function bindPathPage(root) {
    root = root || global.document;
    var page = root.querySelector("[data-il-path-page]");
    if (!page) return;
    var id = page.getAttribute("data-il-path-page");
    startPath(id);
    var ps = pathState(id);

    page.querySelectorAll("[data-il-phase]").forEach(function (el) {
      var ph = el.getAttribute("data-il-phase");
      var box = el.querySelector('input[type="checkbox"]');
      if (box) {
        box.checked = !!(ps.phases && ps.phases[ph]);
        box.addEventListener("change", function () {
          togglePhase(id, ph, box.checked);
          updatePct(page, id);
        });
      }
    });

    var startBtn = page.querySelector("[data-il-path-start]");
    if (startBtn) {
      startBtn.addEventListener("click", function () {
        startPath(id);
        startBtn.textContent = startBtn.getAttribute("data-started-label") || "In progress";
      });
      if (ps.started) startBtn.textContent = startBtn.getAttribute("data-started-label") || "In progress";
    }

    var evForm = page.querySelector("[data-il-evidence-form]");
    if (evForm) {
      evForm.addEventListener("submit", function (e) {
        e.preventDefault();
        var input = evForm.querySelector("input,textarea");
        if (!input || !input.value.trim()) return;
        addEvidence(id, input.value.trim());
        input.value = "";
        renderEvidence(page, id);
      });
    }
    renderEvidence(page, id);
    updatePct(page, id);

    // Muse prompt buttons → coach with query
    page.querySelectorAll("[data-il-muse-prompt]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var q = btn.getAttribute("data-il-muse-prompt") || "";
        var url = "/coach/?q=" + encodeURIComponent(q);
        global.location.href = url;
      });
    });
  }

  function updatePct(page, id) {
    var el = page.querySelector("[data-il-path-pct]");
    var n = page.querySelectorAll("[data-il-phase]").length;
    if (el) el.textContent = progressPct(id, n) + "%";
  }

  function renderEvidence(page, id) {
    var list = page.querySelector("[data-il-evidence-list]");
    if (!list) return;
    var ps = pathState(id);
    var items = (ps.evidence || []).slice().reverse();
    if (!items.length) {
      list.innerHTML = '<li class="text-sm text-muted">No evidence yet — ship a lab artifact.</li>';
      return;
    }
    list.innerHTML = items
      .map(function (it) {
        return "<li class=\"text-sm text-muted\"><span class=\"font-mono text-[0.58rem] text-gold\">" + esc((it.t || "").slice(0, 10)) + "</span> — " + esc(it.note) + "</li>";
      })
      .join("");
  }

  function boot() {
    var dir = global.document.querySelector("[data-il-paths-directory]");
    if (dir) renderDirectory(dir);
    bindPathPage(global.document);
  }

  global.ILPaths = {
    STORAGE: STORAGE,
    fetchPaths: fetchPaths,
    loadState: loadState,
    pathState: pathState,
    startPath: startPath,
    togglePhase: togglePhase,
    addEvidence: addEvidence,
    progressPct: progressPct,
    renderDirectory: renderDirectory,
    bindPathPage: bindPathPage,
  };

  if (global.document.readyState === "loading") {
    global.document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})(typeof window !== "undefined" ? window : this);
