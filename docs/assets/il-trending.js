/**
 * IL Frontier Tracks — MIT / LinkedIn / X ingest UI
 * Catalog: /assets/il-trending-catalog.json
 * Join: course.frontierTrackIds ↔ il-paths.json frontier_track_ids[]
 * Brand: Interstitium cyan/gold/void + lockup language — do NOT Meta-skin.
 * Muse: deep-link /coach/ only; never mutate il-muse*.
 */
(function (global) {
  "use strict";

  var CATALOG_URL = "/assets/il-trending-catalog.json";
  var SCORES_KEY = "il.frontier.scores.v1";
  var cache = null;

  function track(name, props) {
    try {
      if (global.ILAnalytics && typeof global.ILAnalytics.track === "function") {
        global.ILAnalytics.track(name, props || {});
      }
    } catch (e) {}
  }

  function readScores() {
    try {
      var raw = global.localStorage.getItem(SCORES_KEY);
      return raw ? JSON.parse(raw) : { v: 1, byId: {} };
    } catch (e) {
      return { v: 1, byId: {} };
    }
  }

  function writeScores(s) {
    try {
      s.updatedAt = Date.now();
      global.localStorage.setItem(SCORES_KEY, JSON.stringify(s));
    } catch (e) {}
  }

  function ensure(scores, id) {
    if (!scores.byId[id]) {
      scores.byId[id] = { clicks: 0, opens: 0, completes: 0, up: 0, down: 0, score: 0 };
    }
    return scores.byId[id];
  }

  function recompute(row) {
    row.score =
      (row.clicks || 0) * 1 +
      (row.opens || 0) * 2 +
      (row.completes || 0) * 5 +
      (row.up || 0) * 3 -
      (row.down || 0) * 4;
    return row.score;
  }

  function bump(id, field, eventName, extra) {
    var scores = readScores();
    var row = ensure(scores, id);
    row[field] = (row[field] || 0) + 1;
    recompute(row);
    writeScores(scores);
    var props = Object.assign({ courseId: id, score: row.score }, extra || {});
    track(eventName, props);
    try {
      global.document.dispatchEvent(
        new CustomEvent("il:frontier", { detail: { id: id, field: field, row: row } })
      );
    } catch (e) {}
    return row;
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function loadCatalog() {
    if (cache) return Promise.resolve(cache);
    return fetch(CATALOG_URL, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("catalog " + r.status);
        return r.json();
      })
      .then(function (j) {
        cache = j;
        return j;
      });
  }

  function sortCourses(courses) {
    var scores = readScores();
    return courses.slice().sort(function (a, b) {
      var sa = (scores.byId[a.id] && scores.byId[a.id].score) || 0;
      var sb = (scores.byId[b.id] && scores.byId[b.id].score) || 0;
      if (sb !== sa) return sb - sa;
      return String(a.title).localeCompare(String(b.title));
    });
  }

  function sourceBadge(src) {
    if (src === "mit") return "MIT";
    if (src === "linkedin") return "LinkedIn";
    if (src === "x") return "X signal";
    return src;
  }

  function overlayLinks(c) {
    var parts = [];
    var o = c.overlays || [];
    if (o.indexOf("adapt") >= 0) {
      parts.push('<a class="text-cyan hover:text-paper" href="/adapt/">Adapt</a>');
    }
    if (o.indexOf("lab") >= 0) {
      parts.push('<a class="text-cyan hover:text-paper" href="/labs/superlab/">Lab</a>');
    }
    if (o.indexOf("muse") >= 0) {
      parts.push('<a class="text-cyan hover:text-paper" href="/coach/" data-il-frontier-muse="' + esc(c.id) + '">Lab Muse</a>');
    }
    if (c.mapTarget) {
      parts.push('<a class="text-gold hover:text-paper" href="' + esc(c.mapTarget) + '">Path map</a>');
    }
    return parts.join(" · ");
  }

  function cardHTML(c, rank) {
    var scores = readScores();
    var row = scores.byId[c.id] || {};
    var ids = (c.frontierTrackIds || []).join(", ");
    return (
      '<article class="il-frontier-card rounded-xl border border-paper/10 bg-panel p-5 shadow-[0_0_0_1px_rgba(232,238,245,0.06)] sm:p-6" data-frontier-id="' +
      esc(c.id) +
      '" data-source="' +
      esc(c.source) +
      '">' +
      '<div class="flex flex-wrap items-center gap-2">' +
      '<p class="font-mono text-[0.58rem] uppercase tracking-[0.18em] text-cyan">' +
      esc(sourceBadge(c.source)) +
      (c.courseId ? " · " + esc(c.courseId) : "") +
      "</p>" +
      (rank <= 3 && (row.score || 0) > 0
        ? '<span class="rounded border border-gold/40 px-1.5 py-0.5 font-mono text-[0.55rem] uppercase tracking-[0.14em] text-gold">Promoted</span>'
        : "") +
      "</div>" +
      '<h3 class="mt-2 font-display text-xl tracking-[-0.02em] text-paper">' +
      esc(c.title) +
      "</h3>" +
      '<p class="mt-1 font-mono text-[0.58rem] uppercase tracking-[0.14em] text-muted">' +
      esc(c.level || "") +
      (c.term ? " · " + esc(c.term) : "") +
      "</p>" +
      '<p class="mt-3 text-sm text-muted">' +
      esc(c.whyAdvanced || "") +
      "</p>" +
      '<p class="mt-3 font-mono text-[0.58rem] text-muted">Join: ' +
      esc(ids) +
      "</p>" +
      '<p class="mt-2 text-[0.7rem] text-muted">Overlays: ' +
      overlayLinks(c) +
      "</p>" +
      '<div class="mt-4 flex flex-wrap gap-2">' +
      '<a class="inline-flex h-10 items-center rounded-lg bg-paper px-3 font-display text-[0.65rem] uppercase tracking-[0.14em] text-void" href="' +
      esc(c.url) +
      '" target="_blank" rel="noopener noreferrer" data-il-frontier-ext="' +
      esc(c.id) +
      '">Open source →</a>' +
      '<button type="button" class="inline-flex h-10 items-center rounded-lg border border-cyan/40 px-3 font-display text-[0.65rem] uppercase tracking-[0.14em] text-cyan" data-il-frontier-complete="' +
      esc(c.id) +
      '">Mark done</button>' +
      '<button type="button" class="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-paper/15 text-paper" data-il-frontier-up="' +
      esc(c.id) +
      '" aria-label="Thumb up">▲</button>' +
      '<button type="button" class="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-paper/15 text-paper" data-il-frontier-down="' +
      esc(c.id) +
      '" aria-label="Thumb down">▼</button>' +
      "</div>" +
      '<p class="mt-3 font-mono text-[0.55rem] uppercase tracking-[0.12em] text-muted">score ' +
      (row.score || 0) +
      " · clicks " +
      (row.clicks || 0) +
      " · done " +
      (row.completes || 0) +
      "</p>" +
      "</article>"
    );
  }

  function filterCourses(courses, opts) {
    opts = opts || {};
    var src = opts.source || "all";
    var q = (opts.q || "").toLowerCase();
    var track = opts.track || "";
    return courses.filter(function (c) {
      if (src !== "all" && c.source !== src) return false;
      if (track && (c.frontierTrackIds || []).indexOf(track) < 0) return false;
      if (!q) return true;
      var blob = (
        c.title +
        " " +
        (c.topics || []).join(" ") +
        " " +
        (c.frontierTrackIds || []).join(" ") +
        " " +
        (c.courseId || "")
      ).toLowerCase();
      return blob.indexOf(q) >= 0;
    });
  }

  function render(el, opts) {
    if (!el) return Promise.resolve();
    opts = opts || {};
    el.innerHTML =
      '<p class="font-mono text-[0.62rem] uppercase tracking-[0.18em] text-muted">Loading Frontier catalog…</p>';
    return loadCatalog()
      .then(function (cat) {
        var list = sortCourses(filterCourses(cat.courses || [], opts));
        var html = "";
        html +=
          '<div class="mb-6 flex flex-wrap items-end justify-between gap-3">' +
          '<div><p class="font-mono text-[0.62rem] uppercase tracking-[0.22em] text-gold" data-i18n="frontier.kicker">Frontier · MIT · LinkedIn · X</p>' +
          '<p class="mt-2 text-sm text-muted" data-i18n="frontier.lede">External advanced courses mapped onto path <code class="text-cyan">frontier_track_ids</code>. We link out — we do not pirate video.</p></div>' +
          '<p class="font-mono text-[0.58rem] uppercase tracking-[0.14em] text-muted" data-il-frontier-refreshed>Refreshed ' +
          esc(cat.refreshedAtLabel || cat.refreshedAt || "") +
          "</p></div>";
        html +=
          '<div class="mb-6 flex flex-wrap gap-2" role="toolbar" aria-label="Frontier filters">' +
          '<button type="button" class="il-frontier-filter rounded-lg border border-cyan/40 px-3 py-2 font-display text-[0.62rem] uppercase tracking-[0.14em] text-cyan" data-src="all">All</button>' +
          '<button type="button" class="il-frontier-filter rounded-lg border border-paper/15 px-3 py-2 font-display text-[0.62rem] uppercase tracking-[0.14em] text-paper" data-src="mit">MIT</button>' +
          '<button type="button" class="il-frontier-filter rounded-lg border border-paper/15 px-3 py-2 font-display text-[0.62rem] uppercase tracking-[0.14em] text-paper" data-src="linkedin">LinkedIn</button>' +
          '<button type="button" class="il-frontier-filter rounded-lg border border-paper/15 px-3 py-2 font-display text-[0.62rem] uppercase tracking-[0.14em] text-paper" data-src="x">X signal</button>' +
          '<input type="search" class="min-w-[12rem] flex-1 rounded-lg border border-paper/15 bg-void px-3 py-2 font-mono text-sm text-paper" placeholder="Filter…" data-il-frontier-q aria-label="Filter frontier courses"/>' +
          "</div>";
        html +=
          '<p class="mb-4 font-mono text-[0.58rem] uppercase tracking-[0.14em] text-muted">' +
          list.length +
          " courses · MIT " +
          ((cat.counts && cat.counts.mit) || 0) +
          " · LinkedIn " +
          ((cat.counts && cat.counts.linkedin) || 0) +
          " · X " +
          ((cat.counts && cat.counts.x) || 0) +
          "</p>";
        if (!list.length) {
          html +=
            '<p class="text-sm text-muted">No courses match. Clear filters or refresh catalog.</p>';
        } else {
          html += '<div class="grid gap-4 lg:grid-cols-2">';
          list.forEach(function (c, i) {
            html += cardHTML(c, i + 1);
          });
          html += "</div>";
        }
        html +=
          '<p class="mt-8 text-xs text-muted">Musk honesty: cite source URLs, label LinkedIn login gaps, never invent MIT course numbers. Interstitium chrome stays cyan/gold/void — Lab Muse mobile shell is a sibling surface.</p>';
        el.innerHTML = html;
        track("frontier_open", {
          count: list.length,
          source: opts.source || "all",
          track: opts.track || null,
        });
        bind(el, opts);
      })
      .catch(function (err) {
        el.innerHTML =
          '<p class="text-sm text-muted">Frontier catalog failed to load. Check <code class="text-cyan">/assets/il-trending-catalog.json</code>.</p>';
        track("frontier_open", { error: String(err && err.message) });
      });
  }

  function bind(el, opts) {
    el.addEventListener("click", function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      var ext = t.closest("[data-il-frontier-ext]");
      if (ext) {
        bump(ext.getAttribute("data-il-frontier-ext"), "clicks", "frontier_click", {
          href: ext.getAttribute("href"),
        });
        return;
      }
      var done = t.closest("[data-il-frontier-complete]");
      if (done) {
        bump(done.getAttribute("data-il-frontier-complete"), "completes", "frontier_complete");
        render(el, opts);
        return;
      }
      var up = t.closest("[data-il-frontier-up]");
      if (up) {
        bump(up.getAttribute("data-il-frontier-up"), "up", "frontier_thumb_up");
        render(el, opts);
        return;
      }
      var down = t.closest("[data-il-frontier-down]");
      if (down) {
        bump(down.getAttribute("data-il-frontier-down"), "down", "frontier_thumb_down");
        render(el, opts);
        return;
      }
      var muse = t.closest("[data-il-frontier-muse]");
      if (muse) {
        bump(muse.getAttribute("data-il-frontier-muse"), "opens", "frontier_click", {
          overlay: "muse",
        });
        return;
      }
      var filt = t.closest(".il-frontier-filter");
      if (filt) {
        opts.source = filt.getAttribute("data-src") || "all";
        render(el, opts);
      }
    });
    var q = el.querySelector("[data-il-frontier-q]");
    if (q) {
      var timer = null;
      q.addEventListener("input", function () {
        clearTimeout(timer);
        timer = setTimeout(function () {
          opts.q = q.value || "";
          render(el, opts);
        }, 180);
      });
    }
  }

  function mountAll() {
    var nodes = global.document.querySelectorAll("[data-il-frontier]");
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      var opts = {
        source: n.getAttribute("data-source") || "all",
        track: n.getAttribute("data-track") || "",
        q: "",
      };
      render(n, opts);
    }
  }

  function coursesForTrack(trackId) {
    return loadCatalog().then(function (cat) {
      return (cat.courses || []).filter(function (c) {
        return (c.frontierTrackIds || []).indexOf(trackId) >= 0;
      });
    });
  }

  function getScores() {
    return readScores();
  }

  global.ILTrending = {
    loadCatalog: loadCatalog,
    render: render,
    mountAll: mountAll,
    coursesForTrack: coursesForTrack,
    getScores: getScores,
    bump: bump,
  };

  if (global.document.readyState === "loading") {
    global.document.addEventListener("DOMContentLoaded", mountAll);
  } else {
    mountAll();
  }
})(typeof window !== "undefined" ? window : this);
