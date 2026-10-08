/* =====================================================================
 * ILGuided — Rosetta-Stone-style guided learning engine.
 *
 * 2026-10-08. Extends ILProgress (localStorage "il-progress-v1") with a
 * guided layer for the Interstitium Labs course player:
 *
 *   1. Sequential unlock — module N+1 is LOCKED until module N passes.
 *      Passing = complete (ILProgress, user-toggled source of truth) AND
 *      quiz mastery (this store). The FIRST module of every course is
 *      always open.
 *   2. "You are here" wayfinding — guided path rail with states
 *      (done / current / next / locked), auto-scrolls to current.
 *   3. Guided practice — step-by-step drill walkthrough with progressive
 *      hints (hint 1 -> hint 2 -> worked solution). Hints eliminate the
 *      question's own distractors and reveal its own explanation — no
 *      invented content. Hint usage is tracked per module.
 *   4. Review loops — on module completion, 2-3 spaced-review prompts
 *      from earlier completed modules, drawn from those modules' OWN
 *      quiz questions (previously-missed first), or a recall prompt
 *      checked against the module's own summary.
 *   5. Mastery gates — a module's quiz must reach PASS_SCORE (>= 70%)
 *      before the module counts for UNLOCK purposes. The gate adds a
 *      separate "mastery" flag; ILProgress.markComplete stays the
 *      user-toggled completion truth. Modules with no quiz unlock on
 *      completion alone (no fake gates).
 *
 * Storage: localStorage key "il-guided-v1", local device only. No
 * account, no network, no entitlement check — guided locks are a
 * LEARNING-FLOW concept. The paywall stays enforced at the worker;
 * nothing here touches entitlement.
 *
 * Schema:
 *   {
 *     "version": 1,
 *     "courses": {
 *       "<courseId>": {
 *         "<moduleId>": {
 *           "mastery": true,        // quiz gate passed (>= PASS_SCORE), sticky
 *           "testOut": true,        // (WORKSTREAM 5) mastery via passing
 *                                   // diagnostic sitting (>= 80%); counts
 *                                   // as passed for unlock, "Tested out"
 *                                   // on the rail; sticky
 *           "testOutScore": 80,     // diagnostic pct that earned test-out
 *           "score": 0.85,          // best gate score 0..1; null when no quiz
 *           "correct": 17, "total": 20, "answered": 20,
 *           "hintsUsed": 3,         // guided-practice hint reveals
 *           "masteredAt": "<ISO 8601>",
 *           "noQuiz": true,         // mastery via completion alone (no quiz)
 *           "reviewShown": true     // spaced-review panel already surfaced
 *         }
 *       }
 *     }
 *   }
 *
 * Vanilla ES5. Honors prefers-reduced-motion (no smooth auto-scroll).
 * ===================================================================== */
(function (g) {
  'use strict';

  var KEY = 'il-guided-v1';
  var PASS_SCORE = 0.70;
  var REVIEW_COUNT = 3;
  var memOnly = false;
  var mem = {};

  function probe() {
    try {
      g.localStorage.setItem(KEY + ':__probe', '1');
      g.localStorage.removeItem(KEY + ':__probe');
    } catch (e) { memOnly = true; }
  }
  probe();

  function nowISO() { return new Date().toISOString(); }

  /* ILProgress is the completion source of truth; resolve lazily so this
     file also loads in contexts (tests) where it is absent. */
  function prog() {
    try { if (typeof ILProgress !== 'undefined' && ILProgress) return ILProgress; } catch (e) {}
    try { if (g.ILProgress) return g.ILProgress; } catch (e2) {}
    return null;
  }

  function prefersReduced() {
    try {
      return !!(g.matchMedia && g.matchMedia('(prefers-reduced-motion: reduce)').matches);
    } catch (e) { return false; }
  }

  function load() {
    var raw = memOnly ? (mem[KEY] || null) : null;
    try { if (!memOnly) raw = g.localStorage.getItem(KEY); } catch (e) { raw = mem[KEY] || null; }
    if (!raw) return { version: 1, courses: {} };
    try {
      var d = JSON.parse(raw);
      if (!d || typeof d !== 'object') throw new Error('bad shape');
      if (!d.courses || typeof d.courses !== 'object') d.courses = {};
      return d;
    } catch (e) {
      return { version: 1, courses: {} };
    }
  }

  function save(doc) {
    var raw;
    try { raw = JSON.stringify(doc); } catch (e) { return; }
    try {
      if (memOnly) mem[KEY] = raw;
      else g.localStorage.setItem(KEY, raw);
    } catch (e) { mem[KEY] = raw; }
  }

  function getRecord(courseId, moduleId) {
    if (!courseId || !moduleId) return null;
    var d = load();
    var c = d.courses[courseId];
    if (!c) return null;
    return c[moduleId] || null;
  }

  function upsert(courseId, moduleId, fields) {
    if (!courseId || !moduleId) return null;
    var d = load();
    d.courses[courseId] = d.courses[courseId] || {};
    var rec = d.courses[courseId][moduleId] || {};
    var k;
    for (k in fields) {
      if (Object.prototype.hasOwnProperty.call(fields, k)) rec[k] = fields[k];
    }
    d.courses[courseId][moduleId] = rec;
    save(d);
    return rec;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ---- mastery gate ------------------------------------------------ */
  /* Pure score computation over a module quiz. getAnswer(qi, question)
     returns the stored chosen index (string) or null. Unanswered counts
     as wrong: the gate requires the full quick-check set. */
  function quizProgress(quiz, getAnswer) {
    var qs = quiz || [];
    var total = qs.length, correct = 0, answered = 0, i, chosen;
    for (i = 0; i < total; i++) {
      chosen = null;
      try { chosen = getAnswer(i, qs[i]); } catch (e) { chosen = null; }
      if (chosen == null || chosen === '') continue;
      answered++;
      if (String(chosen) === String(qs[i].answer)) correct++;
    }
    return {
      total: total, answered: answered, correct: correct,
      score: total ? correct / total : null,
      needed: Math.ceil(PASS_SCORE * total)
    };
  }

  /* Recompute (and persist) the mastery flag from stored quiz answers.
     Mastery is sticky: once earned it is never revoked by a later,
     lower re-attempt. Best score is kept. */
  function recomputeMastery(courseId, moduleId, quiz, getAnswer) {
    var p = quizProgress(quiz, getAnswer);
    if (!p.total) return { hasGate: false, passed: false };
    var prev = getRecord(courseId, moduleId) || {};
    var best = (typeof prev.score === 'number') ? prev.score : 0;
    if (p.score > best) best = p.score;
    var fields = {
      correct: p.correct, total: p.total, answered: p.answered,
      score: best, hintsUsed: prev.hintsUsed || 0
    };
    if (prev.mastery === true) {
      fields.mastery = true;
      if (prev.masteredAt) fields.masteredAt = prev.masteredAt;
    } else if (best >= PASS_SCORE) {
      fields.mastery = true;
      fields.masteredAt = nowISO();
    }
    if (prev.reviewShown) fields.reviewShown = true;
    if (prev.noQuiz) fields.noQuiz = prev.noQuiz;
    upsert(courseId, moduleId, fields);
    return {
      hasGate: true, passed: fields.mastery === true, score: best,
      answered: p.answered, total: p.total, correct: p.correct, needed: p.needed
    };
  }

  function isMastered(courseId, moduleId) {
    var rec = getRecord(courseId, moduleId);
    return !!(rec && rec.mastery === true);
  }

  function recordHint(courseId, moduleId) {
    var prev = getRecord(courseId, moduleId) || {};
    var n = (prev.hintsUsed || 0) + 1;
    upsert(courseId, moduleId, { hintsUsed: n });
    return n;
  }

  function reviewShown(courseId, moduleId) {
    var rec = getRecord(courseId, moduleId);
    return !!(rec && rec.reviewShown === true);
  }

  /* 2026-10-08 (WORKSTREAM 5): test-out diagnostic (il-diagnostic.js).
     Marks a module's mastery flag from a passing diagnostic sitting.
     Sticky like recomputeMastery: once tested out, later answers cannot
     revoke it. Score keeps the diagnostic pct for display. */
  function markTestOut(courseId, moduleId, pct) {
    if (!courseId || !moduleId) return null;
    var prev = getRecord(courseId, moduleId) || {};
    var fields = {
      mastery: true, testOut: true, masteredAt: nowISO(),
      testOutScore: (typeof pct === 'number') ? pct : null,
      hintsUsed: prev.hintsUsed || 0
    };
    if (typeof prev.score === 'number') fields.score = prev.score;
    else fields.score = (typeof pct === 'number') ? pct / 100 : null;
    if (prev.reviewShown) fields.reviewShown = true;
    if (prev.noQuiz) fields.noQuiz = prev.noQuiz;
    if (prev.correct != null) fields.correct = prev.correct;
    if (prev.total != null) fields.total = prev.total;
    return upsert(courseId, moduleId, fields);
  }

  /* Modules with no quiz unlock on completion alone. Mirror that into
     the guided store (idempotent) so "mastered" counts stay consistent
     for the academy display. */
  function syncNoGateMastery(courseId, modules) {
    var P = prog();
    if (!P) return;
    (modules || []).forEach(function (mi) {
      if (!mi || (mi.quizTotal || 0) > 0) return;
      if (!P.isComplete(courseId, mi.id)) return;
      var rec = getRecord(courseId, mi.id);
      if (rec && rec.mastery === true) return;
      upsert(courseId, mi.id, { mastery: true, noQuiz: true, score: null, masteredAt: nowISO() });
    });
  }

  /* ---- sequential unlock ------------------------------------------ */
  /* modules: [{id, title, code, quizTotal}] in course order.
     Returns per-module state objects. Rules:
       - module 0 is always open
       - module i>0 unlocked iff module i-1 "passed"
       - passed = complete (ILProgress) AND (no quiz gate OR mastery)
       - states: done (passed) / current (first open, not passed —
         "you are here") / next (the locked module right after current,
         the up-next teaser) / locked (everything else) */
  function computeStates(courseId, modules) {
    var P = prog();
    var list = modules || [];
    var out = [];
    var firstOpen = -1;
    var i, mi, rec, complete, hasGate, mastered, testOut, passed, unlocked, st;
    for (i = 0; i < list.length; i++) {
      mi = list[i] || {};
      hasGate = (mi.quizTotal || 0) > 0;
      rec = getRecord(courseId, mi.id);
      mastered = !!(rec && rec.mastery === true);
      /* 2026-10-08 (WORKSTREAM 5): test-out diagnostic — a tested-out
         module counts as passed for unlock purposes without requiring the
         user-toggled completion flag. */
      testOut = !!(rec && rec.testOut === true);
      complete = P ? P.isComplete(courseId, mi.id) : false;
      passed = testOut || (complete && (!hasGate || mastered));
      unlocked = (i === 0) || (out.length > 0 && out[i - 1].passed);
      if (!unlocked) st = 'locked';
      else if (passed) st = 'done';
      else if (firstOpen < 0) { firstOpen = i; st = 'current'; }
      else st = 'locked';
      out.push({
        id: mi.id, title: mi.title || mi.id, code: mi.code || '',
        index: i, state: st, unlocked: !!unlocked, complete: !!complete,
        hasGate: hasGate, mastered: mastered, testOut: testOut, passed: !!passed,
        score: (rec && typeof rec.score === 'number') ? rec.score : null,
        hintsUsed: (rec && rec.hintsUsed) || 0
      });
    }
    if (firstOpen >= 0 && firstOpen + 1 < out.length) {
      out[firstOpen + 1].state = 'next';
    }
    return out;
  }

  function stateFor(courseId, moduleId, modules) {
    var states = computeStates(courseId, modules);
    for (var i = 0; i < states.length; i++) {
      if (states[i].id === moduleId) return states[i];
    }
    return null;
  }

  function firstOpenModule(courseId, modules) {
    var states = computeStates(courseId, modules);
    for (var i = 0; i < states.length; i++) {
      if (states[i].state === 'current') return states[i];
    }
    return null;
  }

  /* ---- wayfinding rail -------------------------------------------- */
  function stateBadge(s) {
    /* 2026-10-08 (WORKSTREAM 5): tested-out modules read distinctly. */
    if (s.state === 'done' && s.testOut) return 'Tested out';
    if (s.state === 'done') return s.hasGate ? 'Mastered' : 'Complete';
    if (s.state === 'current') return 'You are here';
    if (s.state === 'next') return 'Up next';
    return 'Locked';
  }

  function stateIcon(s) {
    if (s.state === 'done') return '✓';
    if (s.state === 'current') return '●';
    if (s.state === 'next') return '→';
    return '🔒';
  }

  function lockNote(s, states) {
    if (s.state === 'next') {
      var cur = null, i;
      for (i = 0; i < states.length; i++) {
        if (states[i].state === 'current') { cur = states[i]; break; }
      }
      return 'Complete "' + (cur ? cur.title : 'the previous lesson') + '" to unlock';
    }
    return 'Complete the previous lesson to unlock';
  }

  function pathRailHTML(courseId, modules) {
    var states = computeStates(courseId, modules);
    var html = '<div class="ilgd-rail" role="list" aria-label="Guided learning path">' +
      '<p class="ilgd-rail__head">Guided path — follow in order</p>';
    for (var i = 0; i < states.length; i++) {
      var s = states[i];
      var cls = 'ilgd-rail__item ilgd-rail__item--' + s.state;
      var inner = '<span class="ilgd-rail__icon" aria-hidden="true">' + stateIcon(s) + '</span>' +
        '<span class="ilgd-rail__txt">' +
        '<span class="ilgd-rail__title">' + esc(s.title) + '</span>' +
        '<span class="ilgd-rail__badge">' + esc(stateBadge(s)) +
        (s.hasGate && typeof s.score === 'number' && !s.mastered
          ? ' · ' + Math.round(s.score * 100) + '%' : '') +
        '</span></span>';
      if (s.unlocked) {
        html += '<button type="button" role="listitem" class="' + cls + '" data-ilgd-goto="' +
          esc(s.id) + '" aria-label="' + esc(s.title + ' — ' + stateBadge(s)) + '">' + inner + '</button>';
      } else {
        html += '<div role="listitem" class="' + cls + '" aria-disabled="true" title="' +
          esc(lockNote(s, states)) + '">' + inner + '</div>';
      }
    }
    html += '</div>';
    return html;
  }

  function wireRail(container) {
    if (!container || !container.querySelectorAll) return;
    var btns = container.querySelectorAll('[data-ilgd-goto]');
    for (var i = 0; i < btns.length; i++) {
      (function (btn) {
        btn.addEventListener('click', function () {
          var id = btn.getAttribute('data-ilgd-goto');
          var target = document.getElementById('mod-' + id);
          if (!target) return;
          try {
            var body = target.querySelector('.mod-body');
            var head = target.querySelector('.mod-head');
            if (body && head && body.style.display === 'none') head.click();
            target.scrollIntoView({ block: 'start', behavior: prefersReduced() ? 'auto' : 'smooth' });
          } catch (e) {}
        });
      })(btns[i]);
    }
  }

  function paintRail(container, courseId, modules) {
    if (!container) return;
    container.innerHTML = pathRailHTML(courseId, modules);
    wireRail(container);
    /* Auto-scroll the rail to "you are here". Page position untouched. */
    try {
      var cur = container.querySelector('.ilgd-rail__item--current');
      if (cur && typeof cur.scrollIntoView === 'function') {
        cur.scrollIntoView({ block: 'nearest', behavior: prefersReduced() ? 'auto' : 'smooth' });
      }
    } catch (e) {}
  }

  /* ---- guided practice -------------------------------------------- */
  /* Step-by-step walkthrough of one drill question. Progressive hints
     derive ONLY from the question's own content: hint 1 / hint 2 each
     rule out one of the question's own distractors; the worked solution
     is the question's own explanation. Practice attempts never write to
     the module quiz — the quick check stays the assessment. */
  function practiceHTML(q, opts) {
    opts = opts || {};
    q = q || {};
    var choices = q.choices || [];
    var answer = (typeof q.answer === 'number') ? q.answer : -1;
    var wrongCount = 0, i;
    for (i = 0; i < choices.length; i++) { if (i !== answer) wrongCount++; }
    var html = '<div class="ilgd-practice" data-answer="' + answer + '"' +
      ' data-explain="' + esc(q.explain || '') + '"' +
      ' data-ilgd-course="' + esc(opts.courseId || '') + '"' +
      ' data-ilgd-module="' + esc(opts.moduleId || '') + '">';
    html += '<p class="ilgd-practice__label">' + esc(opts.label || 'Guided practice') + '</p>';
    html += '<p class="ilgd-practice__q">' + esc(q.q || '') + '</p>';
    html += '<div class="ilgd-practice__opts" role="group" aria-label="Practice options">';
    for (i = 0; i < choices.length; i++) {
      html += '<button type="button" class="ilgd-practice__opt" data-ci="' + i + '">' +
        esc(choices[i]) + '</button>';
    }
    html += '</div>';
    html += '<div class="ilgd-practice__fb" aria-live="polite"></div>';
    html += '<div class="ilgd-practice__hintbar" role="group" aria-label="Progressive hints">';
    html += '<button type="button" class="ilgd-hintbtn" data-hint="1"' +
      (wrongCount < 1 || answer < 0 ? ' disabled' : '') + '>Hint 1</button>';
    html += '<button type="button" class="ilgd-hintbtn" data-hint="2" disabled>Hint 2</button>';
    html += '<button type="button" class="ilgd-hintbtn" data-hint="3"' +
      (wrongCount >= 1 && answer >= 0 ? ' disabled' : '') + '>Worked solution</button>';
    html += '</div><div class="ilgd-practice__hintout" aria-live="polite"></div>';
    html += '</div>';
    return html;
  }

  function wirePractice(container) {
    if (!container || !container.querySelectorAll) return;
    var panels = container.querySelectorAll('.ilgd-practice');
    for (var p = 0; p < panels.length; p++) wirePracticePanel(panels[p]);
    /* recall-check toggles (review loops) */
    var checks = container.querySelectorAll('[data-ilgd-recallcheck]');
    for (var c = 0; c < checks.length; c++) {
      (function (btn) {
        if (btn.getAttribute('data-ilgd-wired') === '1') return;
        btn.setAttribute('data-ilgd-wired', '1');
        btn.addEventListener('click', function () {
          var out = btn.parentNode ? btn.parentNode.querySelector('.ilgd-recallout') : null;
          if (!out) return;
          var hidden = out.hasAttribute('hidden');
          if (hidden) out.removeAttribute('hidden'); else out.setAttribute('hidden', '');
          btn.textContent = hidden ? 'Hide the module text' : 'Check against the module';
        });
      })(checks[c]);
    }
  }

  function wirePracticePanel(panel) {
    if (!panel || panel.getAttribute('data-ilgd-wired') === '1') return;
    panel.setAttribute('data-ilgd-wired', '1');
    var answer = parseInt(panel.getAttribute('data-answer'), 10);
    var explain = panel.getAttribute('data-explain') || '';
    var courseId = panel.getAttribute('data-ilgd-course') || '';
    var moduleId = panel.getAttribute('data-ilgd-module') || '';
    var fb = panel.querySelector('.ilgd-practice__fb');
    var hintout = panel.querySelector('.ilgd-practice__hintout');
    var optNodes = panel.querySelectorAll('.ilgd-practice__opt');
    var opts = [];
    for (var i = 0; i < optNodes.length; i++) opts.push(optNodes[i]);

    function say(msg) { if (fb) fb.textContent = msg; }
    function hintButton(n) { return panel.querySelector('[data-hint="' + n + '"]'); }
    function nthWrong(n) {
      var seen = 0;
      for (var j = 0; j < opts.length; j++) {
        if (parseInt(opts[j].getAttribute('data-ci'), 10) === answer) continue;
        if (seen === n) return opts[j];
        seen++;
      }
      return null;
    }

    opts.forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (btn.disabled) return;
        var ci = parseInt(btn.getAttribute('data-ci'), 10);
        if (ci === answer) {
          btn.classList.add('ilgd-right');
          opts.forEach(function (o) { o.disabled = true; });
          say('Correct ✓ — now answer the quick check to bank it toward mastery.');
        } else {
          btn.classList.add('ilgd-wrong');
          btn.disabled = true;
          say('Not quite — try again, or take a hint below.');
        }
      });
    });

    function takeHint(n) {
      var b1 = hintButton(1), b2 = hintButton(2), b3 = hintButton(3);
      if (n === 1) {
        var w = nthWrong(0);
        if (w) {
          w.disabled = true;
          w.classList.add('ilgd-eliminated');
          hintout.innerHTML = '<p><b>Hint 1 — rule out:</b> ' + esc(w.textContent) + '</p>';
        }
        if (b1) b1.disabled = true;
        if (b2 && nthWrong(1)) b2.disabled = false;
        else if (b3) b3.disabled = false;
      } else if (n === 2) {
        var w2 = nthWrong(1);
        if (w2) {
          w2.disabled = true;
          w2.classList.add('ilgd-eliminated');
          hintout.innerHTML = '<p><b>Hint 2 — rule out:</b> ' + esc(w2.textContent) + '</p>';
        }
        if (b2) b2.disabled = true;
        if (b3) b3.disabled = false;
      } else {
        hintout.innerHTML = '<p><b>Worked solution:</b> ' + esc(explain || 'No explanation shipped with this question.') + '</p>';
        if (b3) b3.disabled = true;
      }
      if (courseId && moduleId) {
        try { recordHint(courseId, moduleId); } catch (e) {}
      }
    }

    [1, 2, 3].forEach(function (n) {
      var b = hintButton(n);
      if (b) b.addEventListener('click', function () { if (!b.disabled) takeHint(n); });
    });
  }

  /* ---- review loops ------------------------------------------------ */
  /* 2-3 spaced-review prompts from earlier completed modules, surfaced
     when a module is completed. Questions are the earlier modules' OWN
     quiz questions — previously-missed first, then unanswered, then the
     first question. Never invented. */
  function completedByRecency(courseId) {
    var P = prog();
    if (!P || !P.load) return [];
    var d;
    try { d = P.load(); } catch (e) { return []; }
    var c = (d && d.courses && d.courses[courseId]) || {};
    var arr = [], k;
    for (k in c) {
      if (Object.prototype.hasOwnProperty.call(c, k) && c[k] && c[k].completed === true) {
        arr.push({ id: k, at: c[k].completedAt || '' });
      }
    }
    arr.sort(function (a, b) { return a.at < b.at ? 1 : a.at > b.at ? -1 : 0; });
    return arr;
  }

  function pickReviewQuestion(qs, moduleId, answerOf) {
    var unanswered = -1;
    for (var i = 0; i < qs.length; i++) {
      var chosen = null;
      try { chosen = answerOf(moduleId, i); } catch (e) { chosen = null; }
      if (chosen == null || chosen === '') { if (unanswered < 0) unanswered = i; continue; }
      if (String(chosen) !== String(qs[i].answer)) return i;
    }
    return unanswered >= 0 ? unanswered : 0;
  }

  function reviewHTML(courseId, modules, justCompletedId, quizOf, answerOf) {
    var recents = completedByRecency(courseId);
    var picks = [], i;
    for (i = 0; i < recents.length && picks.length < REVIEW_COUNT; i++) {
      if (recents[i].id !== justCompletedId) picks.push(recents[i].id);
    }
    if (!picks.length) return '';
    var byId = {};
    (modules || []).forEach(function (m) { if (m && m.id) byId[m.id] = m; });
    var html = '<div class="ilgd-review" role="region" aria-label="Spaced review">' +
      '<p class="ilgd-review__head">Spaced review — strengthen earlier material</p>';
    var count = 0;
    for (i = 0; i < picks.length; i++) {
      var m = byId[picks[i]];
      if (!m) continue;
      var qs = [];
      try { qs = quizOf(m.id) || []; } catch (e) { qs = []; }
      html += '<div class="ilgd-review__item">';
      if (qs.length) {
        var q = qs[pickReviewQuestion(qs, m.id, answerOf)];
        html += '<p class="ilgd-review__src">Review · ' + esc(m.title || m.id) + '</p>';
        html += practiceHTML(q, { courseId: courseId, moduleId: m.id, label: 'Recall check' });
      } else {
        html += '<p class="ilgd-review__src">Recall · ' + esc(m.title || m.id) + '</p>' +
          '<p class="ilgd-review__prompt">In your own words, state the key idea of this module.</p>';
        var check = m.summary || ((m.objectives && m.objectives[0]) || '');
        if (check) {
          html += '<button type="button" class="ilgd-hintbtn" data-ilgd-recallcheck>' +
            'Check against the module</button>' +
            '<div class="ilgd-recallout" hidden>' + esc(check) + '</div>';
        } else {
          html += '<p class="ilgd-review__note">Say it aloud or write it down — ' +
            'this module ships no check text.</p>';
        }
      }
      html += '</div>';
      count++;
    }
    html += '</div>';
    if (!count) return '';
    try { upsert(courseId, justCompletedId, { reviewShown: true }); } catch (e) {}
    return html;
  }

  /* ---- academy ----------------------------------------------------- */
  function masteryStats(courseId, total) {
    var d = load();
    var c = (d.courses && d.courses[courseId]) || {};
    var n = 0, k;
    for (k in c) {
      if (Object.prototype.hasOwnProperty.call(c, k) && c[k] && c[k].mastery === true) n++;
    }
    total = Number(total) || 0;
    return {
      mastered: n, total: total,
      pct: total > 0 ? Math.min(100, Math.round((n / total) * 100)) : 0
    };
  }

  function masteryLineHTML(courseId, total) {
    var st = masteryStats(courseId, total);
    return '<div class="ilgd-masteryline"><span class="ilprog-bar__label">Guided mastery · ' +
      st.mastered + ' of ' + st.total + ' modules mastered</span>' +
      '<div class="ilprog-bar__track"><div class="ilprog-bar__fill" style="width:' +
      st.pct + '%"></div></div></div>';
  }

  var api = {
    KEY: KEY,
    PASS_SCORE: PASS_SCORE,
    getRecord: getRecord,
    isMastered: isMastered,
    recomputeMastery: recomputeMastery,
    quizProgress: quizProgress,
    recordHint: recordHint,
    reviewShown: reviewShown,
    markTestOut: markTestOut,
    syncNoGateMastery: syncNoGateMastery,
    computeStates: computeStates,
    stateFor: stateFor,
    firstOpenModule: firstOpenModule,
    pathRailHTML: pathRailHTML,
    paintRail: paintRail,
    practiceHTML: practiceHTML,
    wirePractice: wirePractice,
    reviewHTML: reviewHTML,
    masteryStats: masteryStats,
    masteryLineHTML: masteryLineHTML,
    esc: esc
  };
  g.ILGuided = api;

  /* Node test hook: expose without DOM. */
  try {
    if (typeof module !== 'undefined' && module.exports) module.exports = api;
  } catch (e) {}
})(typeof window !== 'undefined' ? window : this);
