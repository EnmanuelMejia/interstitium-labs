/* Interstitium Labs — command palette (il-search.js v2, 2026-10-10)
   Least-clicks quick-jump: Ctrl+K / Cmd+K / "/" / tap the nav search button.
   Fuzzy search across /assets/search-index.json (courses, bootcamps, themes,
   paths, practice, pages, shortcuts). Fully keyboard navigable, mobile
   bottom-sheet styling via /assets/il-command-palette.css.

   BACKWARD COMPAT: same file name, same [data-il-search-open] hook and "/"
   shortcut as the v1 site search — every page that loaded v1 gets the
   palette with no markup changes. */
(function () {
  "use strict";
  if (window.__ilCmdkInit) return;
  window.__ilCmdkInit = true;

  var INDEX_URL = "/assets/search-index.json";
  var MAX_RESULTS = 10;
  var RECENT_KEY = "il-cmdk-recent";
  var RECENT_MAX = 6;

  var TYPE_LABEL = {
    course: "Course", bootcamp: "Bootcamp", path: "Path", guide: "Guide",
    theme: "Theme", practice: "Practice", ai: "Noah AI", job: "Job",
    page: "Page", shortcut: "Shortcut"
  };

  /* Curated quick-jump actions shown when the palette is empty. All URLs are
     FINAL canonical destinations — no redirect hops. */
  var QUICK = [
    { t: "IL-29 · ThreatLocker Zero-Trust", u: "/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery", type: "shortcut", k: "il29 threatlocker flagship newest" },
    { t: "IL-28 · DevSecOps & Cloud", u: "/university/course?course=il-28-devsecops-cloud-infrastructure-mastery", type: "shortcut", k: "il28 devsecops flagship" },
    { t: "IL-27 · IT Infrastructure", u: "/university/course?course=il-27-it-infrastructure-specialist-threatlocker-mastery", type: "shortcut", k: "il27 infrastructure flagship" },
    { t: "IL-26 · Data Analyst", u: "/university/course?course=il-26-data-analyst-certification-senior-mastery", type: "shortcut", k: "il26 data analyst flagship" },
    { t: "ThreatLocker assessment prep bootcamp", u: "/bootcamps/threatlocker-assessment-prep/", type: "bootcamp", k: "bootcamp threatlocker assessment" },
    { t: "Bootcamp catalog", u: "/bootcamp-catalog/", type: "bootcamp", k: "bootcamps catalog" },
    { t: "Browse all 16 themed worlds", u: "/topics/", type: "theme", k: "topics themes" },
    { t: "Practice drills & labs", u: "/prep/drills/", type: "practice", k: "practice drills labs" },
    { t: "Ask Noah AI", u: "/noah/", type: "ai", k: "noah ai tutor" },
    { t: "Enroll", u: "/enroll/", type: "shortcut", k: "enroll signup pricing" },
    { t: "Log in", u: "/account/", type: "shortcut", k: "login sign in account" }
  ];

  var items = null;        // index items (lazy)
  var overlay, panel, input, results, live;
  var current = [];        // currently rendered result rows
  var active = -1;         // keyboard-active row index
  var lastFocus = null;

  /* ---------- helpers ---------- */
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function norm(s) { return String(s || "").toLowerCase().replace(/[^a-z0-9+ ]/g, " ").replace(/\s+/g, " ").trim(); }

  function getRecents() {
    try { return JSON.parse(localStorage.getItem(RECENT_KEY) || "[]"); }
    catch (e) { return []; }
  }
  function addRecent(r) {
    try {
      var list = getRecents().filter(function (x) { return x.u !== r.u; });
      list.unshift({ t: r.t, u: r.u, type: r.type });
      localStorage.setItem(RECENT_KEY, JSON.stringify(list.slice(0, RECENT_MAX)));
    } catch (e) { /* private mode — skip */ }
  }

  /* ---------- fuzzy scoring ----------
     AND over query tokens; per token the best of: title-start, substring,
     word-initials, subsequence (compactness-weighted). Title wins big;
     keywords/description contribute less. Returns 0 = no match. */
  function tokenFieldScore(tok, field, wStart, wSub, wInit, wSeq) {
    if (!field || !tok) return 0;
    var f = norm(field);
    if (!f) return 0;
    if (f === tok) return (wStart + 40);
    if (f.indexOf(tok) === 0) return wStart;
    if (f.indexOf(tok) > -1) return wSub;
    // word initials: "tl" matches "ThreatLocker" / "t l" in "ThreatLocker Lab"
    var initials = f.split(" ").map(function (w) { return w.charAt(0); }).join("");
    if (initials && initials.indexOf(tok) > -1) return wInit;
    // subsequence: all chars in order; reward compact spans
    var fi = 0, ti = 0, first = -1, last = -1;
    while (fi < f.length && ti < tok.length) {
      if (f.charAt(fi) === tok.charAt(ti)) {
        if (first < 0) first = fi;
        last = fi; ti++;
      }
      fi++;
    }
    if (ti === tok.length) {
      var span = Math.max(1, last - first + 1);
      return Math.max(1, Math.round(wSeq * (tok.length / span)));
    }
    return 0;
  }

  function score(item, rawQ) {
    var toks = norm(rawQ).split(" ").filter(Boolean);
    if (!toks.length) return 0;
    var total = 0;
    for (var i = 0; i < toks.length; i++) {
      var tok = toks[i];
      var best = Math.max(
        tokenFieldScore(tok, item.t, 100, 55, 45, 34),
        tokenFieldScore(tok, item.tn, 40, 26, 20, 14),
        tokenFieldScore(tok, item.k, 30, 18, 12, 8),
        tokenFieldScore(tok, item.d, 16, 9, 0, 5)
      );
      if (best <= 0) return 0; // AND semantics
      total += best;
    }
    if (item.type === "course" || item.type === "bootcamp" || item.type === "theme") total += 3;
    return total;
  }

  function search(q) {
    var pool = items ? items.concat(QUICK) : QUICK.slice();
    if (!q || norm(q).length < 1) return [];
    var scored = [];
    var seen = {};
    for (var i = 0; i < pool.length; i++) {
      var it = pool[i];
      if (seen[it.u]) continue;
      seen[it.u] = 1;
      var s = score(it, q);
      if (s > 0) scored.push([s, it]);
    }
    scored.sort(function (a, b) { return b[0] - a[0]; });
    return scored.slice(0, MAX_RESULTS).map(function (x) { return x[1]; });
  }

  /* highlight the title's matched subsequence for the first query token */
  function highlight(title, rawQ) {
    var tok = norm(rawQ).split(" ").filter(Boolean)[0];
    var t = String(title || "");
    if (!tok || !t) return esc(t);
    var tl = t.toLowerCase(), ti = 0, fi = 0, pos = [];
    while (fi < tl.length && ti < tok.length) {
      if (tl.charAt(fi) === tok.charAt(ti)) { pos.push(fi); ti++; }
      fi++;
    }
    if (ti < tok.length) return esc(t);
    var out = "", last = 0;
    pos.forEach(function (p) {
      out += esc(t.slice(last, p)) + "<mark>" + esc(t.charAt(p)) + "</mark>";
      last = p + 1;
    });
    return out + esc(t.slice(last));
  }

  /* ---------- rendering ---------- */
  /* Result URLs come from the first-party search index, the static
     QUICK list, or localStorage recents. Never let a stored/indexed
     value navigate off-origin or carry a script scheme: resolve it
     against the current origin and keep only same-origin targets. */
  function safeUrl(u) {
    var s = String(u == null ? "" : u);
    if (!s) return "#";
    try {
      var url = new URL(s, window.location.href);
      if (url.origin !== window.location.origin) return "#";
      return url.pathname + url.search + url.hash;
    } catch (e) { return "#"; }
  }

  function rowNode(r, q) {
    var a = el("a", "il-search__item", "");
    a.href = safeUrl(r.u);
    a.setAttribute("role", "option");
    var label = TYPE_LABEL[r.type] || "Page";
    a.innerHTML =
      '<span class="il-search__type">' + esc(label) + "</span>" +
      '<span class="il-search__body"><span class="il-search__title">' + highlight(r.t, q) + "</span>" +
      (r.d ? '<span class="il-search__desc">' + esc(r.d) + "</span>" : "") + "</span>" +
      (r.tn ? ' <span class="il-search__theme">' + esc(r.tn) + "</span>" : "");
    a.addEventListener("click", function () { addRecent(r); });
    a.addEventListener("mousemove", function () { setActive(current.indexOf(r), false); });
    return a;
  }

  function renderSections(sections, q) {
    results.innerHTML = "";
    current = [];
    sections.forEach(function (sec) {
      if (!sec.items.length) return;
      results.appendChild(el("div", "il-search__section", esc(sec.label)));
      sec.items.forEach(function (r) {
        results.appendChild(rowNode(r, q));
        current.push(r);
      });
    });
    setActive(current.length ? 0 : -1, false);
    live.textContent = current.length ? current.length + " results" : "No results";
  }

  function render() {
    var q = input.value;
    if (!q || !norm(q)) {
      var recents = getRecents();
      renderSections([
        { label: "Recent", items: recents },
        { label: "Jump to", items: QUICK }
      ], "");
      return;
    }
    var res = search(q);
    if (!res.length) {
      results.innerHTML = '<div class="il-search__hint">No results for &ldquo;' + esc(q) +
        "&rdquo; — try a course code like <kbd>IL-29</kbd>, a theme like <kbd>crypto</kbd>, or <kbd>bootcamp</kbd>.</div>";
      current = []; setActive(-1, false);
      live.textContent = "No results";
      return;
    }
    renderSections([{ label: "Results", items: res }], q);
  }

  function setActive(idx, scroll) {
    active = idx;
    var nodes = results.querySelectorAll(".il-search__item");
    for (var i = 0; i < nodes.length; i++) {
      var on = i === idx;
      nodes[i].classList.toggle("il-search__item--active", on);
      nodes[i].setAttribute("aria-selected", on ? "true" : "false");
      if (on && scroll !== false && nodes[i].scrollIntoView) {
        nodes[i].scrollIntoView({ block: "nearest" });
      }
    }
  }

  function go(r, newTab) {
    if (!r) return;
    addRecent(r);
    if (newTab) { window.open(safeUrl(r.u), "_blank", "noopener"); }
    else { location.href = safeUrl(r.u); }
  }

  /* ---------- open / close ---------- */
  function loadIndex(cb) {
    if (items) { cb(); return; }
    fetch(INDEX_URL, { credentials: "same-origin" })
      .then(function (r) { return r.json(); })
      .then(function (d) { items = d.items || []; cb(); })
      .catch(function () { items = []; cb(); });
  }

  function buildUI() {
    overlay = el("div", "il-search__overlay", "");
    overlay.hidden = true;
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Quick jump");
    overlay.innerHTML =
      '<div class="il-search__panel" role="listbox" aria-label="Quick jump results">' +
        '<div class="il-search__bar">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>' +
          '<input class="il-search__input" type="search" inputmode="search" autocomplete="off" autocapitalize="off" spellcheck="false" ' +
            'placeholder="Jump to a course, bootcamp, theme, lab…" aria-label="Jump to content">' +
          '<button type="button" class="il-search__close" aria-label="Close (Esc)">×</button>' +
        "</div>" +
        '<div class="il-search__results"></div>' +
        '<div class="il-search__foot" aria-hidden="true">' +
          "<span><kbd>↑</kbd><kbd>↓</kbd> navigate</span>" +
          "<span><kbd>↵</kbd> open</span>" +
          "<span><kbd>⌘↵</kbd> new tab</span>" +
          "<span><kbd>esc</kbd> close</span>" +
        "</div>" +
      "</div>" +
      '<div aria-live="polite" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)"></div>';
    document.body.appendChild(overlay);
    panel = overlay.querySelector(".il-search__panel");
    input = overlay.querySelector(".il-search__input");
    results = overlay.querySelector(".il-search__results");
    live = overlay.querySelector("[aria-live]");

    var cssHref = "/assets/il-command-palette.css";
    if (!document.querySelector('link[href="' + cssHref + '"]')) {
      var lk = document.createElement("link");
      lk.rel = "stylesheet"; lk.href = cssHref;
      document.head.appendChild(lk);
    }

    overlay.querySelector(".il-search__close").addEventListener("click", close);
    overlay.addEventListener("mousedown", function (e) { if (e.target === overlay) close(); });
    input.addEventListener("input", render);
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); if (current.length) setActive((active + 1) % current.length); }
      else if (e.key === "ArrowUp") { e.preventDefault(); if (current.length) setActive((active - 1 + current.length) % current.length); }
      else if (e.key === "Enter") { e.preventDefault(); go(current[active], e.metaKey || e.ctrlKey); }
      else if (e.key === "Escape") { e.preventDefault(); close(); }
      else if (e.key === "Tab") {
        // light focus trap: keep tabbing inside the palette
        var f = panel.querySelectorAll("a.il-search__item, button, input");
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }

  function open() {
    if (!overlay) buildUI();
    lastFocus = document.activeElement;
    loadIndex(function () {
      overlay.hidden = false;
      document.body.style.overflow = "hidden";
      input.value = "";
      render();
      // focus inside the user gesture so mobile keyboards open
      try { input.focus({ preventScroll: true }); } catch (e) { input.focus(); }
    });
  }
  function close() {
    if (!overlay || overlay.hidden) return;
    overlay.hidden = true;
    document.body.style.overflow = "";
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus({ preventScroll: true }); } catch (e) {} }
  }
  function toggle() { (overlay && !overlay.hidden) ? close() : open(); }

  /* ---------- wiring ---------- */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest ? e.target.closest("[data-il-search-open]") : null;
    if (btn) { e.preventDefault(); toggle(); }
  });
  document.addEventListener("keydown", function (e) {
    var inField = /^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName || "");
    var mod = e.metaKey || e.ctrlKey;
    if ((e.key === "k" || e.key === "K") && mod) { e.preventDefault(); toggle(); return; }
    if (e.key === "/" && !inField && !(overlay && !overlay.hidden)) { e.preventDefault(); open(); return; }
    if (e.key === "Escape" && overlay && !overlay.hidden) { close(); }
  });
  // warm the index when the browser is idle so first open is instant
  function warm() { loadIndex(function () {}); }
  if ("requestIdleCallback" in window) requestIdleCallback(warm, { timeout: 4000 });
  else setTimeout(warm, 2500);
})();
