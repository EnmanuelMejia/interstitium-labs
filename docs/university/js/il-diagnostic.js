/* =====================================================================
 * ILDiag — per-course "Test out" diagnostic (diagnostic-on-entry).
 *
 * WORKSTREAM 5 (2026-10-08): KodeKloud-pattern 10X implementation
 * (brief §1, priority #5 — adaptive pathing via diagnostic-on-entry).
 * Original implementation; patterns extracted, no KodeKloud content.
 *
 * Samples up to 5 questions from the course's OWN module quizzes —
 * the first unanswered quick-check question per module, in module order.
 * Nothing is invented: every stem, choice, answer, and explanation comes
 * from the loaded course JSON. Diagnostic attempts are session-only and
 * are NEVER written to the quick-check store (the real quick checks stay
 * the assessment of record).
 *
 * Scoring: >= 80% (>= 4 of 5) marks each sampled module's mastery flag
 * in il-guided-v1 via ILGuided.markTestOut (testOut: true, sticky). The
 * guided engine then treats them as passed and the rail shows
 * "Tested out" — the path visibly skips them.
 *
 * Vanilla ES5. Dark multicloud theme (styles live in il-mastery.js).
 * prefers-reduced-motion honored (no animation in this module).
 * ===================================================================== */
(function (g) {
  'use strict';

  var MAX_Q = 5;
  var PASS_PCT = 80;

  function M() {
    try { if (typeof ILMastery !== 'undefined' && ILMastery) return ILMastery; } catch (e) {}
    try { if (g.ILMastery) return g.ILMastery; } catch (e2) {}
    return null;
  }

  function G() {
    try { if (typeof ILGuided !== 'undefined' && ILGuided) return ILGuided; } catch (e) {}
    try { if (g.ILGuided) return g.ILGuided; } catch (e2) {}
    return null;
  }

  function esc(s) {
    var m = M();
    if (m && m.esc) return m.esc(s);
    return String(s == null ? '' : s).replace(/&/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* First unanswered quiz question per module, up to MAX_Q. Skips modules
     already mastered/tested-out and modules with no quiz. */
  function itemsFor(courseId, modules) {
    var m = M(), gd = G();
    if (!m || !gd || !courseId) return [];
    var out = [], i, mod, qs, qi;
    for (i = 0; i < (modules || []).length && out.length < MAX_Q; i++) {
      mod = modules[i] || {};
      if (!mod.id) continue;
      if (gd.isMastered(courseId, mod.id)) continue;
      var rec = null;
      try { rec = gd.getRecord(courseId, mod.id); } catch (e) {}
      if (rec && rec.testOut === true) continue;
      qs = mod.quiz || [];
      if (!qs.length) continue;
      for (qi = 0; qi < qs.length; qi++) {
        if (m.quizAnswer(courseId, mod.id, qi) == null) {
          out.push({ moduleId: mod.id, moduleTitle: mod.title || mod.id,
            moduleCode: mod.code || '', qi: qi, q: qs[qi] || {} });
          break;
        }
      }
    }
    return out;
  }

  /* Render + wire the diagnostic card into host. Returns false when there
     is nothing eligible to test out of (caller hides the card). */
  function mount(host, courseId, modules, opts) {
    opts = opts || {};
    var items = itemsFor(courseId, modules);
    if (!host || !items.length) return false;
    var gd = G();
    var picks = [];
    var i;
    for (i = 0; i < items.length; i++) picks.push(-1);

    var html = '<div class="il-diag" role="region" aria-label="Test-out diagnostic">' +
      '<h3>◈ Test out — diagnostic</h3>' +
      '<p class="il-diag__lede">Answer ' + items.length + ' question' +
      (items.length === 1 ? '' : 's') + ' drawn from this course\'s own quick checks ' +
      '(first unanswered question per module). Score ≥ ' + PASS_PCT + '% and Noah clears those ' +
      'modules from your guided path. Attempts here never touch your real quick-check answers.</p>';

    for (i = 0; i < items.length; i++) {
      (function (ix) {
        var it = items[ix];
        var q = it.q;
        html += '<div class="il-diag__q" data-diag-q="' + ix + '">' +
          '<div class="il-diag__stem">' + (ix + 1) + '. ' + esc(q.q || '') +
          ' <span class="il-diag__src">(' + esc(it.moduleCode ? it.moduleCode + ' · ' : '') +
          esc(it.moduleTitle) + ')</span></div>' +
          '<div class="il-diag__opts" role="group" aria-label="Diagnostic question ' + (ix + 1) + ' options">';
        var ci;
        for (ci = 0; ci < (q.choices || []).length; ci++) {
          html += '<button type="button" class="il-diag__opt" data-diag-pick="' + ix + ':' + ci + '">' +
            esc(q.choices[ci]) + '</button>';
        }
        html += '</div><div class="il-diag__why"><b>Why:</b> ' + esc(q.explain || 'No explanation shipped with this question.') + '</div></div>';
      })(i);
    }

    html += '<div class="il-diag__row">' +
      '<button type="button" class="btn primary" data-diag-submit>Grade the diagnostic</button>' +
      '<span class="small muted">Nothing is submitted anywhere — grading happens in your browser.</span>' +
      '</div><div class="il-diag__result" data-diag-result aria-live="polite"></div></div>';

    host.innerHTML = html;
    var diagBox = host.querySelector ? host.querySelector('.il-diag') : null;

    var btns = host.querySelectorAll('[data-diag-pick]');
    var b, j;
    for (j = 0; j < btns.length; j++) {
      (function (btn) {
        btn.addEventListener('click', function () {
          if (diagBox && diagBox.classList.contains('graded')) return;
          var parts = (btn.getAttribute('data-diag-pick') || '').split(':');
          var ix = parseInt(parts[0], 10), ci = parseInt(parts[1], 10);
          picks[ix] = ci;
          var sibs = host.querySelectorAll('[data-diag-pick^="' + ix + ':"]');
          var k;
          for (k = 0; k < sibs.length; k++) sibs[k].classList.remove('sel');
          btn.classList.add('sel');
        });
      })(btns[j]);
    }

    var submit = host.querySelector('[data-diag-submit]');
    var result = host.querySelector('[data-diag-result]');
    if (submit) {
      submit.addEventListener('click', function () {
        var unanswered = 0, k2;
        for (k2 = 0; k2 < picks.length; k2++) if (picks[k2] < 0) unanswered++;
        if (unanswered) {
          result.textContent = 'Answer all ' + items.length + ' questions first (' + unanswered + ' left).';
          result.className = 'il-diag__result fail';
          return;
        }
        var correct = 0;
        for (k2 = 0; k2 < items.length; k2++) {
          var it = items[k2], q = it.q;
          var box = host.querySelector('[data-diag-q="' + k2 + '"]');
          var obtns = box ? box.querySelectorAll('.il-diag__opt') : [];
          var ok = String(picks[k2]) === String(q.answer);
          if (ok) correct++;
          var o;
          for (o = 0; o < obtns.length; o++) {
            obtns[o].disabled = true;
            var oci = parseInt((obtns[o].getAttribute('data-diag-pick') || '').split(':')[1], 10);
            if (String(oci) === String(q.answer)) obtns[o].classList.add('right');
            else if (oci === picks[k2]) obtns[o].classList.add('wrongpick');
          }
        }
        if (diagBox) diagBox.classList.add('graded');
        submit.disabled = true;
        var pct = Math.round((correct / items.length) * 100);
        if (pct >= PASS_PCT && gd && gd.markTestOut) {
          var cleared = 0;
          for (k2 = 0; k2 < items.length; k2++) {
            try {
              gd.markTestOut(courseId, items[k2].moduleId, pct);
              cleared++;
            } catch (e) {}
          }
          result.innerHTML = '✓ ' + pct + '% — Noah cleared ' + cleared + ' module' +
            (cleared === 1 ? '' : 's') + ' you tested out of. They now show as tested-out on your guided path.';
          result.className = 'il-diag__result pass';
          /* Refresh the guided rail/locks. Guided lives inside the course
             player's IIFE, so the player exposes __ilWs5Refresh (set by the
             WORKSTREAM 5 block in course-shell.js); fall back to a global. */
          try {
            if (typeof Guided !== 'undefined' && Guided && Guided.refresh) Guided.refresh();
            else if (g && typeof g.__ilWs5Refresh === 'function') g.__ilWs5Refresh();
          } catch (e2) {}
        } else {
          result.textContent = pct + '% — not yet (need ≥ ' + PASS_PCT + '% to test out). ' +
            'Review the explanations above, work the real quick checks, and try again later.';
          result.className = 'il-diag__result fail';
        }
        if (typeof opts.onDone === 'function') {
          try { opts.onDone(pct >= PASS_PCT, correct, items.length); } catch (e3) {}
        }
      });
    }
    return true;
  }

  var api = {
    MAX_Q: MAX_Q,
    PASS_PCT: PASS_PCT,
    itemsFor: itemsFor,
    mount: mount
  };

  if (typeof g !== 'undefined') g.ILDiag = api;
  try {
    if (typeof module !== 'undefined' && module.exports) module.exports = api;
  } catch (e) {}
})(typeof window !== 'undefined' ? window : this);
