/**
 * Boot the 3D remediation queue UI (2026-10-13). Depends on ILImmersiveReview + ILImmersiveSims
 * + ILImmersive3D (ScenePlayer). Every card re-mounts its authored .glb and reveals the
 * failure mode on the 3D stage after the learner commits. On-device only; never invents
 * a live cluster, hosted fleet, cohort, or server-side analytics.
 * 2026-10-14: "Lab Muse · read my queue aloud" speaks R.speakLine() via the browser's own
 * speechSynthesis (hidden when unavailable). Review stages also inherit WebXR entry from ScenePlayer v1.7.0.
 * 2026-10-20: coach-driven CLI cards (kind 'cli') re-open their CLI-lab task on the authored stage with the earlier
 * steps replayed; the learner types the step; verified without `solution` = recalled, `solution` / give-up = miss.
 * 2026-10-21: CKA blueprint readiness table (official CNCF domains + weights) with a weakest-domain callout and 3D drill link.
 */
(function () {
  'use strict';
  function $(sel, root) { return (root || document).querySelector(sel); }
  function show(el, on) {
    if (!el) return;
    if (on) { el.hidden = false; el.classList.remove('hidden'); }
    else { el.hidden = true; el.classList.add('hidden'); }
  }
  function txt(sel, v) { var el = $(sel); if (el) el.textContent = v; }
  function td(text, cls) { var c = document.createElement('td'); if (cls) c.className = cls; c.textContent = text; return c; }
  function track(name, props) {
    try { if (window.ILAnalytics && window.ILAnalytics.track) window.ILAnalytics.track(name, props); } catch (e) { /* ignore */ }
  }

  function boot() {
    var R = window.ILImmersiveReview, S = window.ILImmersiveSims;
    if (!R || !S) return;
    var lobby = $('[data-il-review-lobby]');
    var run = $('[data-il-review-run]');
    var done = $('[data-il-review-done]');
    var stage = $('[data-il-review-stage]');
    var items = [], idx = 0, answering = false, itemT0 = 0, session = null;
    var cliShell = $('[data-il-review-shell] p');
    var cliShellText = cliShell ? cliShell.textContent : '';

    function renderLobby() {
      var st = R.stats();
      txt('[data-il-review-due]', String(st.dueNow));
      txt('[data-il-review-cards]', String(st.cards));
      txt('[data-il-review-mature]', String(st.mature));
      txt('[data-il-review-learning]', String(st.learning));
      txt('[data-il-review-retention]', st.retentionPct == null ? 'n/a (no graduated card reviewed yet)' : (st.retentionPct + '% of ' + st.retentionN + ' due reviews'));
      txt('[data-il-review-streak]', st.streakDays + (st.streakDays === 1 ? ' day' : ' days'));
      txt('[data-il-review-next]', st.dueNow ? 'now' : (st.nextDueAt ? R.humanInterval(st.nextDueAt - Date.now()) : '—'));
      txt('[data-il-review-exams]', String(st.examsIngested));
      document.documentElement.setAttribute('data-il-review-due-now', String(st.dueNow));
      var tb = $('[data-il-review-mastery] tbody');
      if (tb) {
        tb.textContent = '';
        R.mastery(S).forEach(function (d) {
          var tr = document.createElement('tr');
          tr.setAttribute('data-il-review-domain', d.domain);
          tr.appendChild(td(d.domain, 'py-1 pr-4'));
          var cell = document.createElement('td');
          cell.className = 'py-1 pr-4';
          var bar = document.createElement('span');
          bar.className = 'il-review-bar';
          var fill = document.createElement('span');
          fill.className = 'il-review-bar__fill';
          fill.style.width = Math.max(2, d.pct) + '%';
          bar.appendChild(fill);
          cell.appendChild(bar);
          cell.appendChild(document.createTextNode(' ' + d.pct + '%'));
          tr.appendChild(cell);
          tr.appendChild(td(d.seen + '/' + d.checkpoints));
          tr.appendChild(td(String(d.lapses)));
          tr.appendChild(td(String(d.due)));
          tb.appendChild(tr);
        });
      }
      renderBlueprint();
      var q = R.queue(S, { limit: 10 });
      var startBtn = $('[data-il-review-start]');
      if (startBtn) startBtn.textContent = q.length ? ('Start session · ' + q.length + ' card' + (q.length === 1 ? '' : 's')) : 'Nothing to review';
      if (startBtn) startBtn.disabled = !q.length;
      var why = $('[data-il-review-plan]');
      if (why) {
        var counts = {};
        q.forEach(function (x) { counts[x.reason] = (counts[x.reason] || 0) + 1; });
        var parts = [];
        if (counts.relearn) parts.push(counts.relearn + ' relearn (missed)');
        if (counts.due) parts.push(counts.due + ' due for spaced review');
        if (counts['weak-domain']) parts.push(counts['weak-domain'] + ' new from weak domains');
        if (counts['untested-domain']) parts.push(counts['untested-domain'] + ' new from untested domains');
        if (counts['cold-start']) parts.push(counts['cold-start'] + ' cold-start (no evidence yet)');
        why.textContent = parts.length ? ('Next session: ' + parts.join(' · ') + '.') : 'Queue empty.';
      }
    }
    /* 2026-10-21: CKA blueprint readiness — mastery per official CNCF domain, weighted, weakest by points at stake. */
    function renderBlueprint() {
      var tb = $('[data-il-review-blueprint] tbody');
      var bp = R.blueprint ? R.blueprint(S) : null;
      if (!tb || !bp) return;
      tb.textContent = '';
      bp.rows.forEach(function (r) {
        var tr = document.createElement('tr');
        tr.setAttribute('data-il-review-bp-domain', r.domain);
        if (bp.evidence && bp.weakest && bp.weakest.domain === r.domain) tr.setAttribute('data-weakest', '1');
        tr.appendChild(td(r.domain, 'py-1 pr-4'));
        tr.appendChild(td(r.weight + '%', 'pr-4'));
        tr.appendChild(td(r.pct + '%', 'pr-4'));
        tr.appendChild(td(r.seen + '/' + r.total, 'pr-4'));
        tr.appendChild(td(String(r.atStake)));
        tb.appendChild(tr);
      });
      var wk = $('[data-il-review-weakest]');
      if (wk) {
        wk.textContent = '';
        if (!bp.evidence) wk.textContent = 'No evidence on this device yet — every CKA domain counts as 0%. Sit a paper or run a drill. Blueprint-weighted readiness: 0%.';
        else {
          wk.appendChild(document.createTextNode('Blueprint-weighted readiness: ' + bp.weightedPct + '%. Biggest gap: ' + bp.weakest.domain + ' (' + bp.weakest.weight + '% of the CKA, ' + bp.weakest.pct + '% mastery). '));
          var a = document.createElement('a');
          a.className = 'text-cyan';
          a.href = bp.drill.href;
          a.setAttribute('data-il-review-weakest-link', bp.drill.sim);
          a.textContent = 'Drill it in 3D →';
          wk.appendChild(a);
        }
        document.documentElement.setAttribute('data-il-review-weighted-pct', String(bp.weightedPct == null ? 0 : bp.weightedPct));
        document.documentElement.setAttribute('data-il-review-weakest-domain', bp.evidence && bp.weakest ? bp.weakest.domain : '');
      }
    }
    renderLobby();

    /* 2026-10-14: Lab Muse reads the relearn queue aloud — browser Web Speech only (ILMuse.speakText when
     * the coach is on the page, else the same speechSynthesis path directly). No cloud TTS, no key. */
    var speakBtn = $('[data-il-review-speak]');
    var canSpeak = !!(window.speechSynthesis && window.SpeechSynthesisUtterance) && typeof R.speakLine === 'function';
    if (speakBtn && canSpeak) {
      show(speakBtn, true);
      speakBtn.addEventListener('click', function () {
        var line = R.speakLine(R.stats(), R.queue(S, { limit: 10 }), R.mastery(S), R.blueprint ? R.blueprint(S) : null);
        var out = $('[data-il-review-spoken]');
        if (out) { out.textContent = '\u201c' + line + '\u201d \u2014 spoken by this browser\u2019s speech synthesis.'; show(out, true); }
        try {
          if (window.ILMuse && typeof window.ILMuse.speakText === 'function') {
            window.ILMuse.speakText(line, { speak: true });
          } else {
            window.speechSynthesis.cancel();
            var u = new window.SpeechSynthesisUtterance(line);
            u.rate = 1.02;
            window.speechSynthesis.speak(u);
          }
        } catch (e) { /* ignore */ }
        document.documentElement.setAttribute('data-il-review-spoke', '1');
        track('immersive_review_speak', { due: R.stats().dueNow });
      });
    }

    function mountScene(item) {
      var API = window.ILImmersive3D;
      if (!stage || !API || !API.mount) return Promise.resolve();
      return new Promise(function (resolve) {
        try { if (stage._ilImmersive && stage._ilImmersive.destroy) stage._ilImmersive.destroy(); } catch (e) { /* ignore */ }
        try { delete stage._ilImmersive; } catch (e2) { stage._ilImmersive = null; }
        stage.textContent = '';
        stage.removeAttribute('data-il-sim-ready');
        stage.removeAttribute('data-il-sim-verdict');
        stage.removeAttribute('data-il-immersive-ready');
        stage.setAttribute('data-il-sim', item.simId);
        stage.setAttribute('data-gltf', item.glb);
        var conf = { mode: '3d-first', engine: 'three', asset: item.glb, webgpu: true, sim: item.simId, review: true };
        if (item.kind === 'cli') conf.cliReview = { task: item.taskId, step: item.step };
        stage.setAttribute('data-immersive', JSON.stringify(conf));
        ['data-il-cli-review', 'data-il-cli-review-result', 'data-il-cli-ready', 'data-il-cli-task'].forEach(function (a) { stage.removeAttribute(a); });
        try { API.mount(stage); } catch (e3) { /* ignore */ }
        var t0 = Date.now();
        (function poll() {
          if (stage.getAttribute('data-il-sim-ready') === item.simId) return resolve();
          if (Date.now() - t0 > 20000) return resolve();
          setTimeout(poll, 100);
        })();
      });
    }

    function scenarioOf(item) {
      var sim = S.get(item.simId);
      if (!sim) return null;
      for (var i = 0; i < sim.scenarios.length; i++) if (sim.scenarios[i].id === item.scenarioId) return sim.scenarios[i];
      return null;
    }

    function openScenario(item) {
      /* 2026-10-19: the scene can finish mounting after a fast answer (mount polls every 100 ms); never reset the
       * stage over a reveal that already happened, or for a card the learner has moved past. */
      if (answering || items[idx] !== item) return;
      var player = stage && stage._ilImmersive;
      if (!player || !player._sim) return;
      var sc = scenarioOf(item);
      if (!sc) return;
      player._simState = S.merge(player._sim.initial, {});
      player._simApply('review-reset');
      player._simScenario(sc);
      if (player._simPredict) player._simPredict.hidden = true;
    }

    /* CLI card: the stage's terminal reports the target step as 'pass' (verified without `solution`) or 'solution'. */
    if (stage) stage.addEventListener('il-immersive-cli-review', function (ev) {
      var item = items[idx], d = ev && ev.detail;
      if (!item || item.kind !== 'cli' || !d || d.task !== item.taskId || d.step !== item.step) return;
      commitCli(d.result === 'pass');
    });

    function renderCliCard(item) {
      txt('[data-il-review-q]', 'Type it: ' + item.q);
      var box = $('[data-il-review-options]');
      var p = document.createElement('p');
      p.className = 'text-sm text-muted';
      p.textContent = 'Lab Muse queued this step because the coach had to help last time. The simulated shell below re-opens the task with the earlier steps replayed — type the command for this step yourself (check and hint are fine; solution counts as a miss).';
      box.appendChild(p);
      var give = document.createElement('button');
      give.type = 'button';
      give.className = 'il-exam-opt';
      give.setAttribute('data-il-review-cli-giveup', '');
      give.textContent = 'Show the solution (counts as a miss)';
      give.addEventListener('click', function () {
        var player = stage && stage._ilImmersive;
        if (player && player.cliExec && player._cli) player.cliExec('solution');
        else commitCli(false);
      });
      box.appendChild(give);
      if (cliShell) cliShell.textContent = 'Authored scene + simulated shell — type the step; the 3D scene reacts';
      mountScene(item).then(function () {
        if (answering || items[idx] !== item) return;
        var player = stage && stage._ilImmersive;
        if (player && player._cliInput) { try { player._cliInput.focus(); } catch (e) { /* ignore */ } }
      });
    }

    function commitCli(passed) {
      if (answering) return;
      answering = true;
      var item = items[idx];
      var ms = ((window.performance && performance.now()) || Date.now()) - itemT0;
      var r = R.recordCli({ simId: item.simId, taskId: item.taskId, step: item.step, how: passed ? 'pass' : 'review-solution', ms: ms });
      session.done += 1;
      if (passed) session.correct += 1;
      if (r && r.from != null && r.to > r.from) session.promoted += 1;
      if (r && r.grade === 'again') session.lapsed += 1;
      if (r && r.grade === 'hard') session.hard += 1;
      var give = $('[data-il-review-cli-giveup]');
      if (give) give.disabled = true;
      var gradeText = !r ? '' : (r.grade === 'again' ? 'Relearn: back to box 0 — it leads your next session.'
        : (r.grade === 'hard' ? 'Verified but slow (>' + Math.round(R.SLOW_MS / 1000) + 's): box held at ' + r.to + '.' : 'Box ' + (r.from == null ? 'new' : r.from) + ' → ' + r.to + '.'));
      txt('[data-il-review-feedback]', (passed ? 'Verified without the solution. ' : 'Needed the solution. ' + item.why + ' ') + gradeText + (r && r.dueIn > 0 ? ' Next review in ' + R.humanInterval(r.dueIn) + '.' : ' Due again now.'));
      var fb = $('[data-il-review-feedback]');
      if (fb && r) fb.setAttribute('data-grade', r.grade);
      track('immersive_review_answer', { sim: item.simId, scenario: 'cli', grade: r ? r.grade : 'again', reason: item.reason, kind: 'cli' });
      var next = $('[data-il-review-next-card]');
      if (next) { next.textContent = idx + 1 >= items.length ? 'Finish session' : 'Next card'; show(next, true); }
    }

    function renderCard() {
      var item = items[idx];
      answering = false;
      itemT0 = (window.performance && performance.now()) || Date.now();
      txt('[data-il-review-progress]', 'Card ' + (idx + 1) + '/' + items.length);
      txt('[data-il-review-domain]', item.domain);
      var chip = $('[data-il-review-reason]');
      if (chip) { chip.textContent = item.reasonText; chip.setAttribute('data-reason', item.reason); }
      txt('[data-il-review-label]', item.title + ' · ' + item.label);
      txt('[data-il-review-q]', item.q);
      txt('[data-il-review-feedback]', '');
      var box = $('[data-il-review-options]');
      box.textContent = '';
      var next = $('[data-il-review-next-card]');
      show(next, false);
      if (item.kind === 'cli') return renderCliCard(item);
      if (cliShell) cliShell.textContent = cliShellText;
      S.shuffleOrder(item.options.length).forEach(function (optIdx) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'il-exam-opt';
        b.textContent = item.options[optIdx];
        b.setAttribute('data-il-review-option', String(optIdx));
        b.addEventListener('click', function () { commit(optIdx); });
        box.appendChild(b);
      });
      mountScene(item).then(function () { openScenario(item); });
    }

    function commit(choice) {
      if (answering) return;
      answering = true;
      var item = items[idx];
      var ms = ((window.performance && performance.now()) || Date.now()) - itemT0;
      var correct = choice === item.answer;
      var r = R.record({ simId: item.simId, scenarioId: item.scenarioId, domain: item.domain, correct: correct, ms: ms, src: 'review' });
      session.done += 1;
      if (correct) session.correct += 1;
      if (r.from != null && r.to > r.from) session.promoted += 1;
      if (r.grade === 'again') session.lapsed += 1;
      if (r.grade === 'hard') session.hard += 1;
      var opts = document.querySelectorAll('[data-il-review-option]');
      for (var i = 0; i < opts.length; i++) {
        opts[i].disabled = true;
        var oi = Number(opts[i].getAttribute('data-il-review-option'));
        if (oi === choice) opts[i].setAttribute('data-picked', '1');
        if (oi === item.answer) opts[i].setAttribute('data-correct', '1');
        else if (oi === choice) opts[i].setAttribute('data-correct', '0');
      }
      var gradeText = r.grade === 'again' ? 'Relearn: back to box 0 — it leads your next session.'
        : (r.grade === 'hard' ? 'Correct but slow (>' + Math.round(R.SLOW_MS / 1000) + 's): box held at ' + r.to + '.'
          : 'Box ' + (r.from == null ? 'new' : r.from) + ' → ' + r.to + '.');
      txt('[data-il-review-feedback]', (correct ? 'Correct. ' : 'Not quite. ') + item.why + ' ' + gradeText + (r.dueIn > 0 ? ' Next review in ' + R.humanInterval(r.dueIn) + '.' : ' Due again now.'));
      $('[data-il-review-feedback]').setAttribute('data-grade', r.grade);
      /* Reveal the consequence on the authored 3D stage. */
      var player = stage && stage._ilImmersive;
      if (player && player._simPending) {
        try { player._simCommit(choice); } catch (e) { /* ignore */ }
      } else if (player && player._sim) {
        var sc = scenarioOf(item);
        if (sc) { player._simState = S.merge(player._simState, sc.set); player._simApply('review:' + sc.id); }
      }
      track('immersive_review_answer', { sim: item.simId, scenario: item.scenarioId, grade: r.grade, reason: item.reason });
      var next = $('[data-il-review-next-card]');
      if (next) { next.textContent = idx + 1 >= items.length ? 'Finish session' : 'Next card'; show(next, true); try { next.focus(); } catch (e2) { /* ignore */ } }
    }

    function advance() {
      if (idx + 1 >= items.length) return finish();
      idx += 1;
      renderCard();
    }

    function finish() {
      show(run, false); show(done, true); show(lobby, false);
      var st = R.stats();
      txt('[data-il-review-summary]', session.correct + ' / ' + session.done + ' recalled · ' + session.promoted + ' promoted · '
        + session.hard + ' hard (slow) · ' + session.lapsed + ' back to relearn. '
        + (st.dueNow ? st.dueNow + ' still due now.' : (st.nextDueAt ? 'Next card due in ' + R.humanInterval(st.nextDueAt - Date.now()) + '.' : '')));
      document.documentElement.setAttribute('data-il-review-finished', String(session.correct) + '/' + String(session.done));
      track('immersive_review_session', { done: session.done, correct: session.correct });
    }

    function start() {
      items = R.queue(S, { limit: 10 });
      if (!items.length) { renderLobby(); return; }
      idx = 0;
      session = { done: 0, correct: 0, promoted: 0, hard: 0, lapsed: 0, n: R.noteSession() };
      document.documentElement.removeAttribute('data-il-review-finished');
      show(lobby, false); show(done, false); show(run, true);
      renderCard();
    }

    var startBtn = $('[data-il-review-start]');
    if (startBtn) startBtn.addEventListener('click', start);
    var nextBtn = $('[data-il-review-next-card]');
    if (nextBtn) nextBtn.addEventListener('click', advance);
    var again = $('[data-il-review-again]');
    if (again) again.addEventListener('click', function () { show(done, false); show(lobby, true); renderLobby(); });
    var exp = $('[data-il-review-export]');
    if (exp) exp.addEventListener('click', function () {
      try {
        var blob = new Blob([R.exportJson()], { type: 'application/json' });
        var a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'interstitium-review-' + new Date().toISOString().slice(0, 10) + '.json';
        document.body.appendChild(a); a.click();
        setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
      } catch (e) { /* ignore */ }
    });
    var rst = $('[data-il-review-reset]');
    if (rst) rst.addEventListener('click', function () {
      if (window.confirm && !window.confirm('Erase the review queue on this device? Exam history stays.')) return;
      R.reset();
      renderLobby();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
