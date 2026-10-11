/**
 * il-widgets.js — in-browser lab validation engine for Interstitium Labs study sequences.
 * Config-driven: each <div class="il-lab-widget"> carries a JSON config in a
 * <script type="application/json" class="il-widget-cfg"> child.
 * Widget types: quiz | order | input | spot.
 * Also: per-module completion buttons + progress line. Vanilla ES5. No network.
 */
(function () {
  'use strict';
  var SLUG = (function () {
    var m = location.pathname.match(/\/sequences\/([^\/]+)\//);
    return m ? m[1] : 'sequence';
  })();
  var PROG_KEY = 'il.progress.' + SLUG + '.v1';

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function el(tag, cls, html) {
    var d = document.createElement(tag);
    if (cls) d.className = cls;
    if (html != null) d.innerHTML = html;
    return d;
  }
  function storeGet(k, dflt) {
    try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : dflt; } catch (e) { return dflt; }
  }
  function storeSet(k, v) {
    try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {}
  }
  function shuffle(a) {
    var x = a.slice(), i, j, t;
    for (i = x.length - 1; i > 0; i--) { j = Math.floor(Math.random() * (i + 1)); t = x[i]; x[i] = x[j]; x[j] = t; }
    return x;
  }

  function feedbackBox() {
    return el('div', 'il-widget-fb', '');
  }
  function setFb(box, ok, html) {
    box.className = 'il-widget-fb ' + (ok ? 'il-widget-fb--ok' : 'il-widget-fb--bad');
    box.innerHTML = html;
  }

  /* ---------- quiz: questions with choices, instant feedback ---------- */
  function mountQuiz(root, cfg) {
    var fb = feedbackBox();
    var qs = cfg.questions || [];
    var answered = 0, correct = 0;
    qs.forEach(function (q, qi) {
      var box = el('div', 'il-widget-q');
      box.appendChild(el('p', 'il-widget-qtext', '<strong>Q' + (qi + 1) + '.</strong> ' + esc(q.q)));
      var opts = el('div', 'il-widget-opts');
      shuffle(q.choices).forEach(function (c) {
        var b = el('button', 'il-widget-opt', '<span class="il-widget-key">' + esc(c.key) + '</span> ' + esc(c.text));
        b.type = 'button';
        b.addEventListener('click', function () {
          if (b.disabled) return;
          var kids = opts.children, i;
          for (i = 0; i < kids.length; i++) kids[i].disabled = true;
          var good = (c.key === q.answer);
          b.classList.add(good ? 'il-widget-opt--ok' : 'il-widget-opt--bad');
          for (i = 0; i < kids.length; i++) {
            if (kids[i].textContent.indexOf(q.answer + '') === 1 || kids[i].querySelector('.il-widget-key').textContent === q.answer)
              kids[i].classList.add('il-widget-opt--ans');
          }
          answered++; if (good) correct++;
          var note = el('p', 'il-widget-why', '<strong>' + (good ? 'Correct.' : 'Not quite.') + '</strong> ' + esc(q.why || ''));
          box.appendChild(note);
          if (answered === qs.length) {
            setFb(fb, correct === qs.length,
              '<strong>' + correct + ' / ' + qs.length + ' correct.</strong> ' +
              (correct === qs.length ? 'Clean run — this concept is yours.' : 'Re-read the misses above, then retry the widget.'));
            if (correct === qs.length) {
              var s = storeGet('il.lab.' + SLUG + '.v1', {});
              s['quiz:' + (cfg.id || root.id)] = Date.now(); storeSet('il.lab.' + SLUG + '.v1', s);
            }
          }
        });
        opts.appendChild(b);
      });
      box.appendChild(opts);
      root.appendChild(box);
    });
    root.appendChild(fb);
    var retry = el('button', 'il-btn il-btn--small', 'Reset quiz');
    retry.type = 'button';
    retry.addEventListener('click', function () {
      while (root.firstChild) root.removeChild(root.firstChild);
      mountQuiz(root, cfg);
    });
    root.appendChild(retry);
  }

  /* ---------- order: click items in the correct sequence ---------- */
  function mountOrder(root, cfg) {
    var fb = feedbackBox();
    var picked = [];
    var list = el('div', 'il-widget-order');
    shuffle(cfg.items).forEach(function (it) {
      var b = el('button', 'il-widget-opt', esc(it));
      b.type = 'button';
      b.addEventListener('click', function () {
        if (b.disabled) return;
        b.disabled = true; b.classList.add('il-widget-opt--picked');
        picked.push(it);
        seq.textContent = picked.map(function (p, i) { return (i + 1) + '. ' + p; }).join('  →  ');
      });
      list.appendChild(b);
    });
    var seq = el('p', 'il-widget-seq', 'Your order: (click the steps in order)');
    root.appendChild(list); root.appendChild(seq); root.appendChild(fb);
    var row = el('div', 'il-widget-row');
    var check = el('button', 'il-btn il-btn--small', 'Check order');
    check.type = 'button';
    check.addEventListener('click', function () {
      var want = cfg.items, ok = picked.length === want.length && picked.every(function (p, i) { return p === want[i]; });
      if (ok) {
        setFb(fb, true, '<strong>Correct order.</strong> ' + esc(cfg.why || ''));
        var s = storeGet('il.lab.' + SLUG + '.v1', {});
        s['order:' + (cfg.id || root.id)] = Date.now(); storeSet('il.lab.' + SLUG + '.v1', s);
      } else {
        setFb(fb, false, '<strong>Not the right order.</strong> Expected first step: <em>' + esc(want[0]) + '</em>. Reset and try again — think about what must exist before the next step can run.');
      }
    });
    var reset = el('button', 'il-btn il-btn--small', 'Reset');
    reset.type = 'button';
    reset.addEventListener('click', function () { picked = []; seq.textContent = 'Your order: (click the steps in order)'; setFb(fb, true, ''); fb.className = 'il-widget-fb';
      var kids = list.children, i; for (i = 0; i < kids.length; i++) { kids[i].disabled = false; kids[i].classList.remove('il-widget-opt--picked'); } });
    row.appendChild(check); row.appendChild(reset);
    root.appendChild(row);
  }

  /* ---------- input: free-text validation (cidr | chmod | contains | lines) ---------- */
  function ipToInt(ip) {
    var p = ip.split('.'); if (p.length !== 4) return null;
    var n = 0, i, v;
    for (i = 0; i < 4; i++) { v = parseInt(p[i], 10); if (isNaN(v) || v < 0 || v > 255 || String(v) !== p[i].replace(/^0+(\d)/, '$1')) { if (isNaN(v) || v < 0 || v > 255) return null; } n = n * 256 + v; }
    return n >>> 0;
  }
  function cidrInfo(c) {
    var m = String(c).trim().match(/^(\d{1,3}(?:\.\d{1,3}){3})\/(\d{1,2})$/);
    if (!m) return null;
    var ip = ipToInt(m[1]); if (ip == null) return null;
    var bits = parseInt(m[2], 10); if (bits < 0 || bits > 32) return null;
    var hostBits = 32 - bits;
    var size = Math.pow(2, hostBits);
    var usable = bits >= 31 ? size : size - 2;
    return { bits: bits, size: size, usable: usable };
  }
  function chmodInfo(sym, isDir) {
    // sym like rwxr-x--- ; returns octal string or null
    var m = String(sym).trim().match(/^([r-][w-][x-]){3}$/);
    if (!m) return null;
    var tri = String(sym).trim().match(/([r-][w-][x-])([r-][w-][x-])([r-][w-][x-])/);
    function triVal(t) { var v = 0; if (t[0] === 'r') v += 4; if (t[1] === 'w') v += 2; if (t[2] === 'x' || t[2] === 's' || t[2] === 't') v += 1; return v; }
    return '' + triVal(tri[1]) + triVal(tri[2]) + triVal(tri[3]);
  }
  function mountInput(root, cfg) {
    var fb = feedbackBox();
    if (cfg.prompt) root.appendChild(el('p', 'il-widget-qtext', esc(cfg.prompt)));
    var ta = el('textarea', 'il-widget-input');
    ta.rows = cfg.rows || 3;
    ta.placeholder = cfg.placeholder || 'Type your answer here…';
    ta.setAttribute('aria-label', cfg.id || 'lab input');
    root.appendChild(ta); root.appendChild(fb);
    var btn = el('button', 'il-btn il-btn--small', cfg.button || 'Check my answer');
    btn.type = 'button';
    btn.addEventListener('click', function () {
      var v = ta.value.trim(), ok = false, msg = '';
      var val = cfg.validate || {};
      if (val.kind === 'cidr') {
        var info = cidrInfo(v);
        if (!info) { msg = 'Not a valid CIDR block. Format: a.b.c.d/n, e.g. 10.0.4.0/22.'; }
        else if (val.expectBits != null && info.bits !== val.expectBits) { msg = 'Valid CIDR, but /' + info.bits + ' gives ' + info.usable + ' usable hosts — the task needs ' + val.need + '.'; }
        else if (val.minUsable != null && info.usable < val.minUsable) { msg = 'Valid CIDR, but only ' + info.usable + ' usable hosts — you need at least ' + val.minUsable + '.'; }
        else { ok = true; msg = 'Correct: /' + info.bits + ' = ' + info.size + ' addresses, ' + info.usable + ' usable hosts. ' + (val.why || ''); }
      } else if (val.kind === 'chmod') {
        var o = chmodInfo(v);
        if (!o) { msg = 'Not a 9-character symbolic mode (e.g. rwxr-x---).'; }
        else if (o !== val.expect) { msg = 'That is ' + o + ', not ' + val.expect + '. ' + (val.hint || ''); }
        else { ok = true; msg = 'Correct: ' + v + ' = ' + o + '. ' + (val.why || ''); }
      } else if (val.kind === 'contains') {
        var missing = (val.need || []).filter(function (s) { return v.toLowerCase().indexOf(s.toLowerCase()) < 0; });
        var banned = (val.forbid || []).filter(function (s) { return v.toLowerCase().indexOf(s.toLowerCase()) >= 0; });
        if (missing.length) { msg = 'Missing: ' + missing.join(', ') + '. ' + (val.hint || ''); }
        else if (banned.length) { msg = 'Remove: ' + banned.join(', ') + ' — ' + (val.whyForbid || 'not wanted here.'); }
        else { ok = true; msg = val.success || 'Good — all required elements are present.'; }
      } else if (val.kind === 'number') {
        var num = parseFloat(v);
        if (isNaN(num)) { msg = 'Enter a number.'; }
        else if (Math.abs(num - val.expect) > (val.tol || 0)) { msg = 'Got ' + num + ' — expected ' + val.expect + '. ' + (val.hint || ''); }
        else { ok = true; msg = val.success || 'Correct.'; }
      } else { ok = v.length > 0; msg = ok ? 'Recorded.' : 'Type something first.'; }
      setFb(fb, ok, '<strong>' + (ok ? 'Correct.' : 'Not yet.') + '</strong> ' + esc(msg));
      if (ok) { var s = storeGet('il.lab.' + SLUG + '.v1', {}); s['input:' + (cfg.id || root.id)] = Date.now(); storeSet('il.lab.' + SLUG + '.v1', s); }
    });
    root.appendChild(btn);
  }

  /* ---------- spot: find the misconfiguration ---------- */
  function mountSpot(root, cfg) {
    var fb = feedbackBox();
    if (cfg.intro) root.appendChild(el('p', 'il-widget-qtext', esc(cfg.intro)));
    root.appendChild(el('pre', 'il-widget-code', esc(cfg.code || '')));
    var opts = el('div', 'il-widget-opts');
    (cfg.choices || []).forEach(function (c) {
      var b = el('button', 'il-widget-opt', '<span class="il-widget-key">' + esc(c.key) + '</span> ' + esc(c.text));
      b.type = 'button';
      b.addEventListener('click', function () {
        var kids = opts.children, i;
        for (i = 0; i < kids.length; i++) kids[i].disabled = true;
        var good = (c.key === cfg.answer);
        b.classList.add(good ? 'il-widget-opt--ok' : 'il-widget-opt--bad');
        setFb(fb, good, '<strong>' + (good ? 'Found it.' : 'Keep looking.') + '</strong> ' + esc(cfg.why || ''));
        if (good) { var s = storeGet('il.lab.' + SLUG + '.v1', {}); s['spot:' + (cfg.id || root.id)] = Date.now(); storeSet('il.lab.' + SLUG + '.v1', s); }
      });
      opts.appendChild(b);
    });
    root.appendChild(opts); root.appendChild(fb);
  }

  /* ---------- module progress ---------- */
  function refreshProgress() {
    var line = document.querySelector('[data-il-progress]');
    var btns = document.querySelectorAll('[data-il-module-done]');
    if (!btns.length) return;
    var done = storeGet(PROG_KEY, {});
    var n = 0;
    btns.forEach(function (b) {
      var id = b.getAttribute('data-il-module-done');
      var isDone = !!done[id];
      if (isDone) n++;
      b.classList.toggle('il-mod-done--on', isDone);
      b.innerHTML = isDone ? '✓ Module complete — click to unmark' : 'Mark module complete';
      b.setAttribute('aria-pressed', isDone ? 'true' : 'false');
    });
    if (line) {
      var pct = Math.round(n / btns.length * 100);
      line.innerHTML = '<strong>' + n + ' / ' + btns.length + ' modules complete (' + pct + '%)</strong> — progress is saved on this device.';
      var bar = line.querySelector('.il-progress-bar i') || line.parentNode.querySelector('.il-progress-bar i');
      if (bar) bar.style.width = pct + '%';
    }
  }

  function boot() {
    var widgets = document.querySelectorAll('.il-lab-widget');
    for (var i = 0; i < widgets.length; i++) {
      (function (root) {
        var cfgEl = root.querySelector('script.il-widget-cfg');
        if (!cfgEl) return;
        var cfg;
        try { cfg = JSON.parse(cfgEl.textContent); } catch (e) { return; }
        root.setAttribute('id', root.getAttribute('id') || ('ilw-' + i));
        if (cfg.title) root.insertBefore(el('p', 'il-eyebrow', esc(cfg.title)), root.firstChild);
        try {
          if (cfg.type === 'quiz') mountQuiz(root, cfg);
          else if (cfg.type === 'order') mountOrder(root, cfg);
          else if (cfg.type === 'input') mountInput(root, cfg);
          else if (cfg.type === 'spot') mountSpot(root, cfg);
        } catch (e) {}
      })(widgets[i]);
    }
    var btns = document.querySelectorAll('[data-il-module-done]');
    for (var j = 0; j < btns.length; j++) {
      (function (b) {
        b.addEventListener('click', function () {
          var id = b.getAttribute('data-il-module-done');
          var done = storeGet(PROG_KEY, {});
          if (done[id]) delete done[id]; else done[id] = Date.now();
          storeSet(PROG_KEY, done);
          refreshProgress();
        });
      })(btns[j]);
    }
    refreshProgress();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
