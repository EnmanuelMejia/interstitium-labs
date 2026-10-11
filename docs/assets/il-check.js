/**
 * IL interactive self-check — per-module knowledge checks with feedback + answer keys.
 * Mount:  <div class="il-check" data-il-check data-id="btc-m1" data-title="Module 1 check"></div>
 * Bank:   <script type="application/json" data-il-check-bank>[{id,stem,choices:[{key,text}],answer,why,feedback:{A:"..",B:".."}}]</script>
 *         placed inside the mount or as its immediate next sibling.
 * Behavior: pick a choice -> immediate per-choice feedback (Socratic: wrong picks get
 * reasoning, not the answer letter); "Show answer key" reveals keys + why; score shown
 * once all items are answered; best score persisted to il.check.<id>.v1.
 * Vanilla JS, ES5. No network.
 */
(function (g) {
  'use strict';
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function bankFor(root) {
    try {
      var el = root.querySelector('script[data-il-check-bank]');
      if (!el) { var sib = root.nextElementSibling; if (sib && sib.tagName === 'SCRIPT' && sib.getAttribute('data-il-check-bank') !== null) el = sib; }
      if (el) { var b = JSON.parse(el.textContent); if (b && b.length) return b; }
    } catch (e) {}
    return [];
  }
  function loadBest(id) { try { var r = g.localStorage.getItem('il.check.' + id + '.v1'); return r ? JSON.parse(r).best : null; } catch (e) {} return null; }
  function saveBest(id, score) {
    try {
      var r = g.localStorage.getItem('il.check.' + id + '.v1');
      var o = r ? JSON.parse(r) : { best: 0, attempts: 0 };
      o.attempts = (o.attempts || 0) + 1;
      if (score > (o.best || 0)) o.best = score;
      g.localStorage.setItem('il.check.' + id + '.v1', JSON.stringify(o));
    } catch (e) {}
  }
  function feed(text) {
    try {
      var f = JSON.parse(g.localStorage.getItem('il.evidence.feed.v1') || '[]') || [];
      f.unshift({ t: Date.now(), kind: 'check', text: text });
      if (f.length > 48) f.length = 48;
      g.localStorage.setItem('il.evidence.feed.v1', JSON.stringify(f));
    } catch (e) {}
  }
  function mount(root) {
    var items = bankFor(root);
    var id = root.getAttribute('data-id') || 'check';
    var title = root.getAttribute('data-title') || 'Knowledge check';
    if (!items.length) { root.innerHTML = '<p class="text-sm text-muted">Check data unavailable.</p>'; return; }
    var state = { answers: {}, keyOpen: false };
    function render() {
      var answered = 0, correct = 0, i;
      for (i = 0; i < items.length; i++) { if (state.answers[items[i].id] !== undefined) { answered++; if (state.answers[items[i].id] === items[i].answer) correct++; } }
      var html = '<div class="il-check__head"><p class="il-kicker">Knowledge check</p><h3 class="il-check__title">' + esc(title) + '</h3>';
      var best = loadBest(id);
      html += '<p class="il-check__meta">' + items.length + ' questions' + (best !== null ? ' · best ' + best + '%' : '') + (answered ? ' · score so far ' + correct + '/' + answered : '') + '</p></div>';
      for (i = 0; i < items.length; i++) {
        (function (q, n) {
          var picked = state.answers[q.id];
          html += '<div class="il-check__item"><p class="il-check__stem"><span class="il-check__num">' + (n + 1) + '</span> ' + esc(q.stem) + '</p><div class="il-check__choices">';
          q.choices.forEach(function (c) {
            var cls = 'il-check__choice';
            if (picked !== undefined) {
              if (c.key === q.answer) cls += ' is-correct';
              else if (c.key === picked) cls += ' is-wrong';
              else cls += ' is-dim';
            }
            html += '<button type="button" class="' + cls + '" data-q="' + esc(q.id) + '" data-key="' + esc(c.key) + '"' + (picked !== undefined ? ' disabled' : '') + '><span class="il-check__key">' + esc(c.key) + '</span> ' + esc(c.text) + '</button>';
          });
          html += '</div>';
          if (picked !== undefined) {
            var ok = picked === q.answer;
            var fb = (q.feedback && q.feedback[picked]) || q.why || '';
            html += '<div class="il-check__feedback ' + (ok ? 'is-ok' : 'is-no') + '"><p><strong>' + (ok ? 'Correct.' : 'Not quite.') + '</strong> ' + esc(fb) + '</p></div>';
          }
          html += '</div>';
        })(items[i], i);
      }
      html += '<div class="il-check__foot"><button type="button" class="il-btn il-btn--small" data-il-check-key>' + (state.keyOpen ? 'Hide answer key' : 'Show answer key') + '</button>';
      html += '<button type="button" class="il-btn il-btn--ghost il-btn--small" data-il-check-reset>Reset</button></div>';
      if (state.keyOpen) {
        html += '<ol class="il-check__keylist">';
        items.forEach(function (q) { html += '<li><strong>' + esc(q.answer) + '</strong> — ' + esc(q.stem) + (q.why ? '<br/><span class="il-check__why">' + esc(q.why) + '</span>' : '') + '</li>'; });
        html += '</ol>';
      }
      root.innerHTML = html;
      [].forEach.call(root.querySelectorAll('[data-il-check-key]'), function (b) {
        b.addEventListener('click', function () { state.keyOpen = !state.keyOpen; render(); });
      });
      [].forEach.call(root.querySelectorAll('[data-il-check-reset]'), function (b) {
        b.addEventListener('click', function () { state = { answers: {}, keyOpen: false }; render(); });
      });
      [].forEach.call(root.querySelectorAll('.il-check__choice[data-q]'), function (b) {
        b.addEventListener('click', function () {
          var qid = b.getAttribute('data-q'), key = b.getAttribute('data-key');
          if (state.answers[qid] !== undefined) return;
          state.answers[qid] = key;
          var done = Object.keys(state.answers).length === items.length;
          render();
          if (done) {
            var c = 0; items.forEach(function (q) { if (state.answers[q.id] === q.answer) c++; });
            var pct = Math.round((c / items.length) * 100);
            saveBest(id, pct);
            feed('Knowledge check ' + id + ': ' + pct + '%');
          }
        });
      });
    }
    render();
  }
  function boot() {
    var nodes = document.querySelectorAll('[data-il-check]');
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
  }
  g.ILCheck = { boot: boot, mount: mount };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})(typeof window !== 'undefined' ? window : this);
