/* Interstitium Labs — Knowledge Sources client (il-sources.js).
   Front door to the Knowledge Source Layer (/api/sources/*):
     ILSources.search(name, q, opts)  -> Promise<api json>
     ILSources.panel(topic)           -> Promise<api json>
     ILSources.renderPanel(el, topic) -> renders an attributed panel
     ILSources.wikiCard(el, term)     -> renders a Wikipedia card
   Auto-mount: elements with [data-il-sources="<topic>"] get a panel;
   elements with [data-il-wiki="<term>"] get a Wikipedia summary card.
   Honesty: every rendered item carries its source label + canonical
   link; excerpts are attributed, never presented as site-original.
   Vanilla JS, zero dependencies. Fails silent (leaves element empty)
   when the API is unreachable. */
(function (g) {
  'use strict';

  var API = '/api/sources';

  var CSS = [
    '.ils-panel{border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:16px 18px;background:rgba(255,255,255,.03)}',
    '.ils-panel h4{margin:0 0 10px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;opacity:.75}',
    '.ils-src{margin:10px 0;padding:10px 12px;border:1px solid rgba(255,255,255,.09);border-radius:8px;overflow:hidden}',
    '.ils-src h5{margin:0 0 4px;font-size:14px;line-height:1.4}',
    '.ils-src p{font-size:13.5px;line-height:1.55;margin:0 0 6px;opacity:.92}',
    '.ils-src img{float:right;width:54px;height:54px;object-fit:contain;border-radius:6px;margin:0 0 6px 10px;background:#fff}',
    '.ils-src blockquote{margin:6px 0;padding:6px 10px;border-left:3px solid #c9a227;font-size:13px;opacity:.85}',
    '.ils-attr{font-size:11.5px;opacity:.6;margin-top:8px}',
    '.ils-links{margin:6px 0;padding-left:18px}',
    '.ils-links li{margin:4px 0;font-size:13.5px}',
    '.ils-meta{font-size:11.5px;opacity:.6}'
  ].join('\n');

  function injectCSS() {
    if (document.getElementById('ils-css')) return;
    var st = document.createElement('style');
    st.id = 'ils-css'; st.textContent = CSS;
    document.head.appendChild(st);
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function get(path) {
    return fetch(API + path).then(function (r) {
      if (!r.ok) throw new Error('sources-' + r.status);
      return r.json();
    });
  }

  function search(name, q, opts) {
    opts = opts || {};
    var qs = '?q=' + encodeURIComponent(q) + '&limit=' + (opts.limit || 3);
    if (opts.sort) qs += '&sort=' + encodeURIComponent(opts.sort);
    return get('/' + encodeURIComponent(name) + qs);
  }
  function panel(topic) {
    return get('/panel?topic=' + encodeURIComponent(topic));
  }
  function wikiSummary(term) {
    return get('/wikipedia?title=' + encodeURIComponent(term)).then(function (j) {
      if (j && j.results && j.results.length) return j;
      return search('wikipedia', term, { limit: 1 });
    });
  }

  function renderPanelData(j) {
    if (!j || !j.ok || !j.sections) return '';
    var byName = {};
    j.sections.forEach(function (s) { byName[s.name] = s; });
    var html = '<h4>Sources &amp; deep dives — ' + esc(j.topic || '') + '</h4>';
    var wiki = byName.wikipedia && byName.wikipedia.results[0];
    if (wiki) {
      html += '<div class="ils-src">' +
        (wiki.meta && wiki.meta.thumbnail ? '<img src="' + esc(wiki.meta.thumbnail) + '" alt="">' : '') +
        '<h5><a href="' + esc(wiki.url) + '" target="_blank" rel="noopener">' + esc(wiki.title) + '</a> — Wikipedia</h5>' +
        '<p>' + esc(wiki.summary) + '</p>' +
        '<p class="ils-attr">Summary from Wikipedia (CC BY-SA).</p></div>';
    }
    var so = (byName.stackoverflow && byName.stackoverflow.results) || [];
    if (so.length) {
      html += '<p><strong>Stack Overflow — how practitioners solve it:</strong></p>';
      so.forEach(function (r) {
        html += '<div class="ils-src"><h5><a href="' + esc(r.url) + '" target="_blank" rel="noopener">' + esc(r.title) + '</a></h5>' +
          '<p class="ils-meta">Score ' + esc(r.meta.score != null ? r.meta.score : 0) + ' · ' + esc(r.meta.answers || 0) + ' answers</p>';
        if (r.meta.topAnswer) {
          html += '<blockquote><strong>Top answer' + (r.meta.topAnswerAccepted ? ' (accepted)' : '') + ':</strong> ' + esc(r.meta.topAnswer) + '</blockquote>';
        }
        html += '</div>';
      });
    }
    var gh = (byName.github && byName.github.results) || [];
    if (gh.length) {
      html += '<p><strong>GitHub — real-world code:</strong></p><ul class="ils-links">';
      gh.forEach(function (r) {
        html += '<li><a href="' + esc(r.url) + '" target="_blank" rel="noopener">' + esc(r.title) + '</a>' +
          ' <span class="ils-meta">★ ' + esc(r.meta.stars != null ? r.meta.stars : '') +
          (r.meta.language ? ' · ' + esc(r.meta.language) : '') +
          (r.meta.license ? ' · ' + esc(r.meta.license) : '') + '</span></li>';
      });
      html += '</ul>';
    }
    var more = [];
    ['arxiv', 'mdn', 'substack', 'hackernews', 'reddit', 'youtube'].forEach(function (n) {
      var sec = byName[n];
      if (!sec) return;
      sec.results.forEach(function (r) { more.push({ label: sec.label, r: r }); });
    });
    if (more.length) {
      html += '<p><strong>Go deeper:</strong></p><ul class="ils-links">';
      more.slice(0, 8).forEach(function (m) {
        html += '<li><a href="' + esc(m.r.url) + '" target="_blank" rel="noopener">' + esc(m.r.title) + '</a>' +
          ' <span class="ils-meta">— ' + esc(m.label) + '</span></li>';
      });
      html += '</ul>';
    }
    html += '<p class="ils-attr">' + esc(j.attribution || 'Supplemental material shown with attribution; verify at the source.') + '</p>';
    return html;
  }

  function renderPanel(el, topic) {
    if (!el) return Promise.resolve(false);
    injectCSS();
    el.classList.add('ils-panel');
    el.innerHTML = '<p class="ils-meta">Gathering sources…</p>';
    return panel(topic).then(function (j) {
      var html = renderPanelData(j);
      el.innerHTML = html || '<p class="ils-meta">No live sources for this topic right now.</p>';
      return !!html;
    }).catch(function () {
      el.innerHTML = '<p class="ils-meta">Sources are unreachable right now.</p>';
      return false;
    });
  }

  function wikiCard(el, term) {
    if (!el) return Promise.resolve(false);
    injectCSS();
    return wikiSummary(term).then(function (j) {
      var r = j && j.results && j.results[0];
      if (!r) { el.innerHTML = ''; return false; }
      el.classList.add('ils-src');
      el.innerHTML =
        (r.meta && r.meta.thumbnail ? '<img src="' + esc(r.meta.thumbnail) + '" alt="">' : '') +
        '<h5><a href="' + esc(r.url) + '" target="_blank" rel="noopener">' + esc(r.title) + '</a> — Wikipedia</h5>' +
        '<p>' + esc(r.summary) + '</p>' +
        '<p class="ils-attr">Summary from Wikipedia (CC BY-SA 4.0) — read the full article at the source.</p>';
      return true;
    }).catch(function () { el.innerHTML = ''; return false; });
  }

  function autoMount() {
    injectCSS();
    var panels = document.querySelectorAll('[data-il-sources]');
    for (var i = 0; i < panels.length; i++) {
      var topic = panels[i].getAttribute('data-il-sources');
      if (topic) renderPanel(panels[i], topic);
    }
    var cards = document.querySelectorAll('[data-il-wiki]');
    for (var k = 0; k < cards.length; k++) {
      var term = cards[k].getAttribute('data-il-wiki');
      if (term) wikiCard(cards[k], term);
    }
  }

  g.ILSources = {
    search: search,
    panel: panel,
    wikiSummary: wikiSummary,
    renderPanel: renderPanel,
    wikiCard: wikiCard,
    autoMount: autoMount
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoMount);
  } else { autoMount(); }
})(window);
