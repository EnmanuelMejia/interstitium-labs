/**
 * IL sequence progress — per-module completion persisted to il.progress.<slug>.v1.
 * Page contract: <body data-il-seq="bitcoin-protocol"> (or any ancestor with data-il-seq).
 * Modules: any [data-il-module] in DOM order; each gets a "Mark module complete" toggle.
 * Progress bar: rendered into [data-il-progress]; created at top of <main> if absent.
 * Vanilla JS, ES5. No network.
 */
(function (g) {
  'use strict';
  function host() {
    var el = document.querySelector('[data-il-seq]');
    return el ? { el: el, slug: el.getAttribute('data-il-seq') } : null;
  }
  function key(slug) { return 'il.progress.' + slug + '.v1'; }
  function load(slug) { try { var r = g.localStorage.getItem(key(slug)); if (r) return JSON.parse(r); } catch (e) {} return { v: 1, done: {} }; }
  function save(slug, s) { try { g.localStorage.setItem(key(slug), JSON.stringify(s)); } catch (e) {} }
  function feed(text) {
    try {
      var f = JSON.parse(g.localStorage.getItem('il.evidence.feed.v1') || '[]') || [];
      f.unshift({ t: Date.now(), kind: 'progress', text: text });
      if (f.length > 48) f.length = 48;
      g.localStorage.setItem('il.evidence.feed.v1', JSON.stringify(f));
    } catch (e) {}
  }
  function names(modules) {
    return modules.map(function (m, i) {
      var t = m.querySelector('h2, h3');
      return (t ? t.textContent.trim().replace(/\s+/g, ' ').slice(0, 60) : 'Module ' + (i + 1));
    });
  }
  function renderBar(bar, modules, state, titles) {
    var done = 0, i;
    for (i = 0; i < modules.length; i++) if (state.done['m' + (i + 1)]) done++;
    var pct = modules.length ? Math.round((done / modules.length) * 100) : 0;
    var html = '<div class="il-progress" role="status" aria-label="Sequence progress"><div class="il-progress__top"><span class="il-progress__label">Your progress</span><span class="il-progress__pct">' + done + ' / ' + modules.length + ' modules · ' + pct + '%</span></div>';
    html += '<div class="il-progress__track"><div class="il-progress__fill" style="width:' + pct + '%"></div></div>';
    html += '<ol class="il-progress__list">';
    for (i = 0; i < modules.length; i++) {
      var d = !!state.done['m' + (i + 1)];
      html += '<li class="' + (d ? 'is-done' : '') + '"><span class="il-progress__dot" aria-hidden="true">' + (d ? '✓' : (i + 1)) + '</span> ' + esc(titles[i]) + '</li>';
    }
    html += '</ol></div>';
    bar.innerHTML = html;
  }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function boot() {
    var h = host();
    if (!h) return;
    var modules = [].slice.call(document.querySelectorAll('[data-il-module]'));
    if (!modules.length) return;
    var state = load(h.slug);
    var titles = names(modules);
    var bar = document.querySelector('[data-il-progress]');
    if (!bar) {
      bar = document.createElement('div');
      bar.setAttribute('data-il-progress', '');
      var main = document.querySelector('main') || document.body;
      main.insertBefore(bar, main.firstChild);
    }
    function paint() {
      renderBar(bar, modules, state, titles);
      modules.forEach(function (m, i) {
        var k = 'm' + (i + 1), done = !!state.done[k];
        var btn = m.querySelector('[data-il-module-done]');
        if (btn) {
          btn.classList.toggle('is-done', done);
          btn.setAttribute('aria-pressed', done ? 'true' : 'false');
          btn.innerHTML = done ? '<span aria-hidden="true">✓</span> Module complete — undo' : 'Mark module complete';
        }
      });
    }
    modules.forEach(function (m, i) {
      var k = 'm' + (i + 1);
      var btn = m.querySelector('[data-il-module-done]');
      if (!btn) {
        btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'il-btn il-btn--small il-module-done';
        btn.setAttribute('data-il-module-done', '');
        var slot = m.querySelector('[data-il-module-done-slot]');
        (slot || m).appendChild(btn);
      }
      btn.addEventListener('click', function () {
        var was = !!state.done[k];
        if (was) delete state.done[k]; else state.done[k] = Date.now();
        save(h.slug, state);
        if (!was) feed('Completed module ' + (i + 1) + ' of ' + h.slug + ': ' + titles[i]);
        paint();
      });
    });
    paint();
  }
  g.ILSeq = { boot: boot };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})(typeof window !== 'undefined' ? window : this);
