/* =====================================================================
 * ILMastery — skill-mastery dashboard, repair queue, and exam-readiness
 * library shared by the course player and the academy page.
 *
 * WORKSTREAM 5 (2026-10-08): KodeKloud-pattern 10X implementation.
 * Original implementation; patterns extracted, no KodeKloud content.
 *
 * Reads (local device only, no network, no entitlement):
 *   - localStorage "il-guided-v1"   (ILGuided mastery records)
 *   - localStorage "ilc:<courseId>:quiz:<moduleId>:<qi>" (quick-check answers)
 *   - docs/university/data/cert-index.json (cert name -> courses)
 *
 * Heat rule (per module, documented on the dashboard):
 *   green  = mastery gate passed (>=70%) or tested-out diagnostic
 *   yellow = attempted, best score >= 40% but below the gate
 *   red    = attempted, best score < 40%
 *   gray   = not attempted (no record, no answers)
 *
 * Vanilla ES5. Dark multicloud theme. No animation except under
 * prefers-reduced-motion: no-preference.
 * ===================================================================== */
(function (g) {
  'use strict';

  var GUIDED_KEY = 'il-guided-v1';
  var ILCC = 'ilc:';

  function hasLS() {
    try { return typeof g.localStorage !== 'undefined' && !!g.localStorage; }
    catch (e) { return false; }
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function trunc(s, n) {
    s = String(s == null ? '' : s);
    return s.length > n ? s.slice(0, n - 1) + '…' : s;
  }

  /* ---- storage reads ------------------------------------------------ */

  function guidedDoc() {
    if (!hasLS()) return { version: 1, courses: {} };
    var raw = null;
    try { raw = g.localStorage.getItem(GUIDED_KEY); } catch (e) { return { version: 1, courses: {} }; }
    if (!raw) return { version: 1, courses: {} };
    try {
      var d = JSON.parse(raw);
      if (!d || typeof d !== 'object' || !d.courses) return { version: 1, courses: {} };
      return d;
    } catch (e) { return { version: 1, courses: {} }; }
  }

  function guidedRec(courseId, moduleId) {
    var d = guidedDoc();
    var c = d.courses[courseId];
    if (!c) return null;
    return c[moduleId] || null;
  }

  /* Stored quick-check answer, mirroring course-shell's Progress keys. */
  function quizAnswer(courseId, moduleId, qi) {
    if (!hasLS() || !courseId) return null;
    try {
      var v = g.localStorage.getItem(ILCC + courseId + ':quiz:' + moduleId + ':' + qi);
      return (v == null || v === '') ? null : v;
    } catch (e) { return null; }
  }

  function quizTotals(courseId, moduleId, quiz) {
    var total = (quiz || []).length, answered = 0, correct = 0, i, chosen;
    for (i = 0; i < total; i++) {
      chosen = quizAnswer(courseId, moduleId, i);
      if (chosen == null) continue;
      answered++;
      if (String(chosen) === String(quiz[i].answer)) correct++;
    }
    return { total: total, answered: answered, correct: correct,
      score: answered ? correct / answered : 0 };
  }

  /* ---- heat ---------------------------------------------------------- */

  function heatFor(courseId, modules) {
    var out = [], i, m, rec, qt, cell, label, score;
    for (i = 0; i < (modules || []).length; i++) {
      m = modules[i] || {};
      rec = guidedRec(courseId, m.id);
      qt = quizTotals(courseId, m.id, m.quiz || []);
      cell = 'gray'; label = 'Not attempted'; score = null;
      if (rec && rec.mastery === true) {
        cell = 'green';
        score = (typeof rec.score === 'number') ? rec.score : null;
        label = rec.testOut ? 'Tested out' : (rec.noQuiz ? 'Complete' :
          (score != null ? Math.round(score * 100) + '% mastery' : 'Mastered'));
      } else if ((m.quiz || []).length) {
        if (qt.answered > 0) {
          score = qt.score;
          if (score >= 0.7) { cell = 'green'; label = Math.round(score * 100) + '% (gate soon)'; }
          else if (score >= 0.4) { cell = 'yellow'; label = Math.round(score * 100) + '% — building'; }
          else { cell = 'red'; label = Math.round(score * 100) + '% — needs work'; }
        } else if (rec && (rec.hintsUsed || 0) > 0) {
          cell = 'yellow'; label = 'Practiced — no answers yet';
        }
      } else if (rec && rec.noQuiz) {
        cell = 'green'; label = 'Complete';
      }
      out.push({ id: m.id, code: m.code || '', title: m.title || m.id,
        cell: cell, label: label, score: score,
        answered: qt.answered, total: qt.total,
        testOut: !!(rec && rec.testOut), noQuiz: !(m.quiz || []).length });
    }
    return out;
  }

  function heatCounts(cells) {
    var c = { green: 0, yellow: 0, red: 0, gray: 0 }, i;
    for (i = 0; i < cells.length; i++) c[cells[i].cell]++;
    return c;
  }

  function heatHTML(courseId, modules, opts) {
    opts = opts || {};
    var cells = heatFor(courseId, modules);
    var counts = heatCounts(cells);
    var html = '<div class="il-heat" role="list" aria-label="Concept mastery heatmap">';
    var i, cell;
    for (i = 0; i < cells.length; i++) {
      cell = cells[i];
      var inner = '<span class="il-heat__code">' + esc(cell.code || ('M' + (i + 1))) + '</span>' +
        '<span class="il-heat__title">' + esc(trunc(cell.title, 42)) + '</span>' +
        '<span class="il-heat__label">' + esc(cell.label) + '</span>';
      var tip = esc(cell.title + ' — ' + cell.label +
        (cell.total ? ' (' + cell.answered + '/' + cell.total + ' answered)' : ''));
      if (opts.linkFor) {
        html += '<a role="listitem" class="il-heat__cell il-heat__cell--' + cell.cell + '"' +
          ' href="' + esc(opts.linkFor(cell)) + '" title="' + tip + '">' + inner + '</a>';
      } else {
        html += '<div role="listitem" class="il-heat__cell il-heat__cell--' + cell.cell +
          '" title="' + tip + '">' + inner + '</div>';
      }
    }
    html += '</div>';
    html += '<div class="il-heat__legend" aria-label="Heatmap legend">' +
      '<span><i class="il-dot il-dot--green"></i>Mastered ' + counts.green + '</span>' +
      '<span><i class="il-dot il-dot--yellow"></i>Building ' + counts.yellow + '</span>' +
      '<span><i class="il-dot il-dot--red"></i>Needs work ' + counts.red + '</span>' +
      '<span><i class="il-dot il-dot--gray"></i>Not attempted ' + counts.gray + '</span>' +
      '<span class="il-heat__rule">Mastery = ≥70% on the module quick check (demonstrated skill, not watch time).</span>' +
      '</div>';
    return html;
  }

  /* ---- repair queue --------------------------------------------------- */
  /* Missed quick-check questions: stored answer exists and is wrong.
     Re-attempts that fix the answer drop off automatically. */

  function repairItems(courseId, modules) {
    var items = [], i, m, qs, qi, q, chosen;
    for (i = 0; i < (modules || []).length; i++) {
      m = modules[i] || {};
      qs = m.quiz || [];
      for (qi = 0; qi < qs.length; qi++) {
        q = qs[qi] || {};
        chosen = quizAnswer(courseId, m.id, qi);
        if (chosen == null) continue;
        if (String(chosen) === String(q.answer)) continue;
        items.push({
          moduleId: m.id, moduleTitle: m.title || m.id, moduleCode: m.code || '',
          qi: qi, q: q.q || '', choices: q.choices || [],
          answer: q.answer, chosen: chosen,
          chosenText: (q.choices || [])[+chosen],
          answerText: (q.choices || [])[+q.answer],
          explain: q.explain || ''
        });
      }
    }
    return items;
  }

  function repairHTML(items, opts) {
    opts = opts || {};
    var html = '<div class="il-repair" role="region" aria-label="Repair queue">';
    if (!items.length) {
      html += '<div class="il-repair__empty">✓ No open misses — every answered quick check is currently correct. ' +
        'New misses land here automatically.</div>';
    } else {
      html += '<p class="il-repair__head">' + items.length + ' missed concept' +
        (items.length === 1 ? '' : 's') + ' — fix each one at its source question:</p>';
      html += '<ol class="il-repair__list">';
      var i, it;
      for (i = 0; i < items.length; i++) {
        it = items[i];
        var link = opts.linkFor ? opts.linkFor(it) : null;
        html += '<li class="il-repair__item">' +
          '<div class="il-repair__q">' + esc(trunc(it.q, 140)) + '</div>' +
          '<div class="il-repair__meta">' + esc(it.moduleCode ? it.moduleCode + ' · ' : '') +
          esc(trunc(it.moduleTitle, 48)) + ' · question ' + (it.qi + 1) + '</div>' +
          '<div class="il-repair__diff"><span class="il-repair__you">You picked: ' +
          esc(trunc(String(it.chosenText == null ? it.chosen : it.chosenText), 60)) + '</span>' +
          '<span class="il-repair__right">Correct: ' +
          esc(trunc(String(it.answerText == null ? it.answer : it.answerText), 60)) + '</span></div>' +
          (link ? '<a class="il-repair__go" href="' + esc(link) + '">Revisit question →</a>' : '') +
          '</li>';
      }
      html += '</ol>';
    }
    if (opts.repairedCount) {
      html += '<p class="il-repair__fixed">✓ ' + opts.repairedCount +
        ' repaired this session — closed the loop.</p>';
    }
    html += '</div>';
    return html;
  }

  /* ---- exam readiness -------------------------------------------------- */
  /* Weighted demonstrated-mastery across every course mapped to a cert
     name (cert-index.json). Weight = quiz-bearing modules (falls back to
     total modules). ILGuided.masteryStats supplies per-course pct. */

  function readinessFor(certName, index) {
    var entry = index && index.certs && index.certs[certName];
    if (!entry) return null;
    var per = [], wsum = 0, acc = 0, i, c, pct, w;
    var useGuided = (typeof ILGuided !== 'undefined' && ILGuided && ILGuided.masteryStats);
    for (i = 0; i < entry.courses.length; i++) {
      c = entry.courses[i];
      pct = 0;
      if (useGuided) {
        try { pct = ILGuided.masteryStats(c.courseId, c.moduleCount).pct || 0; }
        catch (e) { pct = 0; }
      }
      w = c.quizModules > 0 ? c.quizModules : (c.moduleCount || 1);
      per.push({ code: c.code, slug: c.slug, pct: pct, modules: c.moduleCount });
      acc += pct * w; wsum += w;
    }
    return {
      cert: certName, issuer: entry.issuer,
      pct: wsum ? Math.round(acc / wsum) : 0,
      courses: per
    };
  }

  function readinessBand(pct, hasData) {
    if (!hasData) return 'No demonstrated mastery yet — answer quick checks to light this up.';
    if (pct >= 85) return 'Exam-ready signal — strong demonstrated mastery.';
    if (pct >= 70) return 'Nearly there — close the remaining gaps.';
    if (pct > 0) return 'Early — build foundations before booking an exam.';
    return 'No demonstrated mastery yet — answer quick checks to light this up.';
  }

  function readinessHTML(r) {
    if (!r) return '';
    var cls = r.pct >= 85 ? 'ready' : (r.pct >= 70 ? 'near' : 'early');
    var html = '<div class="il-cert il-cert--' + cls + '">' +
      '<div class="il-cert__head"><div><div class="il-cert__name">' + esc(r.cert) + '</div>' +
      '<div class="il-cert__issuer">' + esc(r.issuer || '') + ' · independent prep, not affiliated</div></div>' +
      '<div class="il-cert__pct">' + r.pct + '%</div></div>' +
      '<div class="ilprog-bar__track"><div class="ilprog-bar__fill" style="width:' + r.pct + '%"></div></div>' +
      '<p class="il-cert__band">' + esc(readinessBand(r.pct, r.courses.some(function (c) { return c.pct > 0; }))) + '</p>' +
      '<ul class="il-cert__courses">';
    var i;
    for (i = 0; i < r.courses.length; i++) {
      var c = r.courses[i];
      html += '<li>' + esc(c.code || c.slug) + ' — ' + c.pct + '% of ' + c.modules +
        ' modules mastered</li>';
    }
    html += '</ul>' +
      '<p class="il-cert__note">Readiness = weighted demonstrated mastery across mapped courses ' +
      '(≥70% quick-check gate per module). A readiness signal, not a pass guarantee.</p>' +
      '</div>';
    return html;
  }

  function isUnmappedCert(name, issuer) {
    if (issuer === 'N/A') return true;
    return /no certification/i.test(String(name || ''));
  }

  /* ---- styles ---------------------------------------------------------- */

  var CSS = [
    '.il-heat{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:14px 0}',
    '.il-heat__cell{display:flex;flex-direction:column;gap:4px;padding:10px 12px;border-radius:10px;',
    ' border:1px solid var(--hairline,rgba(201,162,39,.25));background:var(--panel2,#10161f);color:inherit;text-decoration:none}',
    'a.il-heat__cell:hover{border-color:var(--gold,#c9a227)}',
    '.il-heat__code{font-family:ui-monospace,Menlo,monospace;font-size:11px;letter-spacing:.08em;color:var(--muted,#9aa3b2)}',
    '.il-heat__title{font-size:13px;font-weight:600;line-height:1.3}',
    '.il-heat__label{font-size:11.5px;color:var(--muted,#9aa3b2)}',
    '.il-heat__cell--green{border-left:4px solid #34d399}',
    '.il-heat__cell--yellow{border-left:4px solid #fbbf24}',
    '.il-heat__cell--red{border-left:4px solid #f87171}',
    '.il-heat__cell--gray{border-left:4px solid #4b5563;opacity:.75}',
    '.il-heat__legend{display:flex;flex-wrap:wrap;gap:14px;font-size:12.5px;color:var(--muted,#9aa3b2);align-items:center}',
    '.il-dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}',
    '.il-dot--green{background:#34d399}.il-dot--yellow{background:#fbbf24}.il-dot--red{background:#f87171}.il-dot--gray{background:#4b5563}',
    '.il-heat__rule{flex-basis:100%;font-size:12px}',
    '.ilctx{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:-4px -4px 12px;padding:10px 14px;',
    ' border:1px solid var(--hairline,rgba(201,162,39,.45));border-left:4px solid var(--gold,#c9a227);',
    ' border-radius:10px;background:rgba(201,162,39,.07);font-size:12.5px;color:var(--ink,#e8e4d8)}',
    '.ilctx-you{font-weight:800;letter-spacing:.14em;font-size:11px;color:var(--gold,#c9a227)}',
    '.ilctx-sep{color:var(--muted,#9aa3b2)}',
    '.ilctx-env{color:var(--cyan,#62d8e9);font-weight:600}',
    '.il-repair{margin:12px 0}',
    '.il-repair__head{font-weight:700;margin-bottom:8px}',
    '.il-repair__empty{padding:14px 16px;border:1px dashed var(--hairline,rgba(201,162,39,.4));border-radius:10px;color:var(--muted,#9aa3b2)}',
    '.il-repair__list{list-style:none;margin:0;padding:0;display:grid;gap:10px}',
    '.il-repair__item{padding:12px 14px;border:1px solid var(--line,rgba(255,255,255,.09));border-left:3px solid #f87171;border-radius:10px;background:var(--panel2,#10161f)}',
    '.il-repair__q{font-weight:600;margin-bottom:4px}',
    '.il-repair__meta{font-size:12px;color:var(--muted,#9aa3b2);margin-bottom:6px}',
    '.il-repair__diff{display:flex;flex-wrap:wrap;gap:12px;font-size:13px;margin-bottom:8px}',
    '.il-repair__you{color:#f87171}.il-repair__right{color:#34d399}',
    '.il-repair__go{font-size:13px;font-weight:600;color:var(--cyan,#62d8e9);text-decoration:none}',
    '.il-repair__go:hover{text-decoration:underline}',
    '.il-repair__fixed{color:#34d399;font-weight:600;margin-top:10px}',
    '.il-cert{border:1px solid var(--hairline,rgba(201,162,39,.25));border-radius:12px;padding:16px 18px;margin:14px 0;background:var(--panel2,#10161f)}',
    '.il-cert__head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:10px}',
    '.il-cert__name{font-weight:700;font-size:16px}',
    '.il-cert__issuer{font-size:12.5px;color:var(--muted,#9aa3b2);margin-top:2px}',
    '.il-cert__pct{font-size:28px;font-weight:800;font-family:ui-monospace,Menlo,monospace}',
    '.il-cert--ready .il-cert__pct{color:#34d399}.il-cert--near .il-cert__pct{color:#fbbf24}.il-cert--early .il-cert__pct{color:#9aa3b2}',
    '.il-cert__band{font-size:13.5px;margin:8px 0 4px}',
    '.il-cert__courses{margin:6px 0;padding-left:20px;font-size:13px;color:var(--muted,#9aa3b2)}',
    '.il-cert__note{font-size:12px;color:var(--muted,#9aa3b2);margin:8px 0 0}',
    '.il-cert__none{padding:14px 16px;border:1px dashed var(--hairline,rgba(201,162,39,.4));border-radius:10px;color:var(--muted,#9aa3b2);font-size:13.5px}',
    '.il-diag{border:1px solid var(--line2,rgba(98,216,233,.4));border-radius:12px;padding:18px;margin:16px 0;background:rgba(98,216,233,.04)}',
    '.il-diag h3{margin:0 0 6px;color:var(--cyan,#62d8e9)}',
    '.il-diag__lede{font-size:13.5px;color:var(--muted,#9aa3b2);margin-bottom:12px}',
    '.il-diag__q{margin:12px 0;padding:12px 14px;border:1px solid var(--line,rgba(255,255,255,.09));border-radius:10px;background:var(--panel2,#10161f)}',
    '.il-diag__stem{font-weight:600;margin-bottom:8px}',
    '.il-diag__opts{display:grid;gap:6px}',
    '.il-diag__opt{text-align:left;font:inherit;font-size:13.5px;padding:8px 12px;border:1px solid var(--line,rgba(255,255,255,.12));border-radius:8px;background:transparent;color:inherit;cursor:pointer}',
    '.il-diag__opt:hover:not(:disabled){border-color:var(--cyan,#62d8e9)}',
    '.il-diag__opt.sel{border-color:var(--gold,#c9a227);background:rgba(201,162,39,.1)}',
    '.il-diag__opt:disabled{cursor:default}',
    '.il-diag__opt.right{border-color:#34d399;background:rgba(52,211,153,.1)}',
    '.il-diag__opt.wrongpick{border-color:#f87171;background:rgba(248,113,113,.1)}',
    '.il-diag__why{font-size:13px;color:var(--muted,#9aa3b2);border-left:3px solid var(--gold,#c9a227);padding:6px 12px;margin-top:8px;display:none}',
    '.il-diag.graded .il-diag__why{display:block}',
    '.il-diag__row{display:flex;gap:10px;align-items:center;margin-top:12px;flex-wrap:wrap}',
    '.il-diag__result{font-weight:700;margin-top:10px}',
    '.il-diag__result.pass{color:#34d399}.il-diag__result.fail{color:#fbbf24}',
    '.ilcompare-row{margin-top:10px}',
    '.ilcompare-btn{font:inherit;font-size:13px;font-weight:600;color:var(--gold,#c9a227);background:transparent;',
    ' border:1px solid var(--hairline,rgba(201,162,39,.5));border-radius:999px;padding:7px 14px;cursor:pointer}',
    '.ilcompare-btn:hover{background:rgba(201,162,39,.12)}',
    '.ilcompare-btn:focus-visible{outline:2px solid var(--gold,#c9a227);outline-offset:2px}',
    '.ilflash{box-shadow:0 0 0 3px rgba(201,162,39,.55);border-radius:10px}',
    '@media (prefers-reduced-motion: no-preference){',
    ' .ilflash{transition:box-shadow .3s ease-out}',
    '}'
  ].join('\n');

  function injectCSS() {
    try {
      if (g.document && g.document.getElementById && g.document.getElementById('il-mastery-css')) return;
      var st = g.document.createElement('style');
      st.id = 'il-mastery-css';
      st.setAttribute('data-source', 'il-mastery');
      if (st.styleSheet) st.styleSheet.cssText = CSS; else st.textContent = CSS;
      var head = g.document.head || g.document.getElementsByTagName('head')[0];
      if (head && head.appendChild) head.appendChild(st);
    } catch (e) {}
  }

  var api = {
    guidedDoc: guidedDoc,
    guidedRec: guidedRec,
    quizAnswer: quizAnswer,
    quizTotals: quizTotals,
    heatFor: heatFor,
    heatCounts: heatCounts,
    heatHTML: heatHTML,
    repairItems: repairItems,
    repairHTML: repairHTML,
    readinessFor: readinessFor,
    readinessBand: readinessBand,
    readinessHTML: readinessHTML,
    isUnmappedCert: isUnmappedCert,
    esc: esc
  };

  if (typeof g !== 'undefined') g.ILMastery = api;
  try {
    if (typeof module !== 'undefined' && module.exports) module.exports = api;
  } catch (e) {}

  if (g && g.document) {
    try {
      if (g.document.readyState === 'loading' && g.document.addEventListener)
        g.document.addEventListener('DOMContentLoaded', injectCSS);
      else injectCSS();
    } catch (e) {}
  }
})(typeof window !== 'undefined' ? window : this);
