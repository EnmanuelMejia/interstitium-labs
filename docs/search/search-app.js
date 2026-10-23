// __PURE_LOGIC__ (above this marker: no DOM, safe to eval in node for tests)

/** Tokenize a string into lowercase word tokens. */
function ilTokens(s) {
  return (s || "").toLowerCase().match(/[a-z0-9][a-z0-9+\-#.]*/g) || [];
}

/**
 * Ranked site search over the build-time index.
 * index: [{u:url, t:title, h:[headings], s:snippet}]
 * AND semantics across tokens; title hits outrank headings, headings outrank body.
 * Returns [{u, t, s, score}] sorted by score desc.
 */
function ilSearch(index, query) {
  var qt = ilTokens(query);
  if (!qt.length) return [];
  var out = [];
  for (var i = 0; i < index.length; i++) {
    var p = index[i];
    var t = ilTokens(p.t).join(" ");
    var h = ilTokens(p.h ? p.h.join(" ") : "").join(" ");
    var s = ilTokens(p.s).join(" ");
    var score = 0, ok = true;
    for (var j = 0; j < qt.length; j++) {
      var q = qt[j];
      var inT = t.indexOf(q) !== -1;
      var inH = h.indexOf(q) !== -1;
      var inS = s.indexOf(q) !== -1;
      if (!inT && !inH && !inS) { ok = false; break; }
      score += (inT ? 5 : 0) + (inH ? 2 : 0) + (inS ? 1 : 0);
    }
    if (ok) out.push({ u: p.u, t: p.t, s: p.s, score: score });
  }
  out.sort(function (a, b) { return b.score - a.score || (a.u < b.u ? -1 : 1); });
  return out.slice(0, 25);
}

// __DOM__ (below this marker: browser wiring only)

(function () {
  var input = document.getElementById("q");
  var results = document.getElementById("results");
  var count = document.getElementById("count");
  var index = null;

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function render(hits, query) {
    if (!query.trim()) {
      results.innerHTML = "";
      count.textContent = "";
      return;
    }
    count.textContent = hits.length + (hits.length === 1 ? " result" : " results");
    if (!hits.length) {
      results.innerHTML = '<p class="il-search__empty">No pages matched "' + esc(query) + '". Try fewer words.</p>';
      return;
    }
    var html = "";
    for (var i = 0; i < hits.length; i++) {
      var h = hits[i];
      html += '<article class="il-search__hit"><a class="il-search__title" href="' +
        esc(h.u) + '">' + esc(h.t || h.u) + '</a>' +
        '<div class="il-search__url">' + esc(h.u) + '</div>' +
        '<p class="il-search__snippet">' + esc(h.s) + '</p></article>';
    }
    results.innerHTML = html;
  }

  function run() {
    if (!index) return;
    render(ilSearch(index, input.value), input.value);
  }

  fetch("/assets/search-index.json", { cache: "no-store" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (data) {
      index = (data && data.items) || [];
      count.textContent = "Index ready · " + index.length + " pages";
      var hash = decodeURIComponent((location.hash || "").replace(/^#q=/, ""));
      if (hash) { input.value = hash; }
      run();
      // deep-link support: /search/#q=cinema
      if (!hash && (new URLSearchParams(location.search).get("q"))) {
        input.value = new URLSearchParams(location.search).get("q");
        run();
      }
    })
    .catch(function () {
      count.textContent = "Could not load the search index.";
    });

  var t = null;
  input.addEventListener("input", function () {
    clearTimeout(t);
    t = setTimeout(run, 120);
  });
})();
