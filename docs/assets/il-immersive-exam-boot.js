/**
 * Boot the timed CKA mock exam UI (2026-10-12). Depends on ILImmersiveExam + ILImmersiveSims + ScenePlayer.
 * Relative-asset page only; never invents a live cluster or hosted fleet.
 */
(function () {
  'use strict';
  function $(sel, root) { return (root || document).querySelector(sel); }
  function show(el, on) {
    if (!el) return;
    if (on) { el.hidden = false; el.classList.remove('hidden'); }
    else { el.hidden = true; el.classList.add('hidden'); }
  }
  function fmt(ms) {
    var s = Math.max(0, Math.ceil(ms / 1000));
    var m = Math.floor(s / 60); s = s % 60;
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  function boot() {
    var E = window.ILImmersiveExam, S = window.ILImmersiveSims;
    if (!E || !S) return;
    var lobby = $('[data-il-exam-lobby]');
    var run = $('[data-il-exam-run]');
    var done = $('[data-il-exam-done]');
    var stage = $('[data-il-exam-stage]');
    var poolEl = $('[data-il-exam-pool]');
    var historyEl = $('[data-il-exam-history]');
    var exam = null, idx = 0, timerId = null, answering = false, itemT0 = 0;

    if (poolEl) poolEl.textContent = String(E.pool(S).length);
    function renderHistory() {
      if (!historyEl) return;
      var db = E.loadStore();
      var last = db.last;
      historyEl.textContent = last
        ? ('Last paper on this device: ' + last.correct + '/' + last.total + ' (' + last.pct + '%) · ' + (last.passed ? 'pass bar cleared' : 'under pass bar') + '.')
        : 'No papers on this device yet.';
    }
    renderHistory();

    function stopTimer() { if (timerId) { clearInterval(timerId); timerId = null; } }
    function tick() {
      if (!exam) return;
      var left = exam.endsAt - Date.now();
      var el = $('[data-il-exam-timer]');
      if (el) {
        el.textContent = fmt(left);
        el.setAttribute('data-urgent', left <= 60000 ? '1' : '0');
      }
      if (left <= 0) finish('time');
    }

    function mountScene(item) {
      var API = window.ILImmersive3D;
      if (!stage || !API || !API.mount) return Promise.resolve();
      return new Promise(function (resolve) {
        try {
          if (stage._ilImmersive && stage._ilImmersive.destroy) stage._ilImmersive.destroy();
        } catch (e) { /* ignore */ }
        try { delete stage._ilImmersive; } catch (e2) { stage._ilImmersive = null; }
        stage.innerHTML = '';
        stage.removeAttribute('data-il-sim-ready');
        stage.removeAttribute('data-il-sim-verdict');
        stage.removeAttribute('data-il-immersive-ready');
        stage.setAttribute('data-il-sim', item.simId);
        stage.setAttribute('data-gltf', item.glb);
        stage.setAttribute('data-immersive', JSON.stringify({
          mode: '3d-first', engine: 'three', asset: item.glb, webgpu: true, sim: item.simId, exam: true
        }));
        try { API.mount(stage); } catch (e3) { /* ignore */ }
        var t0 = Date.now();
        (function poll() {
          if (stage.getAttribute('data-il-sim-ready') === item.simId) return resolve();
          if (Date.now() - t0 > 20000) return resolve();
          setTimeout(poll, 100);
        })();
      });
    }

    function openScenario(item) {
      var player = stage && stage._ilImmersive;
      if (!player || !player._sim) return;
      var sim = S.get(item.simId);
      var sc = null;
      for (var i = 0; i < sim.scenarios.length; i++) if (sim.scenarios[i].id === item.scenarioId) sc = sim.scenarios[i];
      if (!sc) return;
      /* Reset to initial, then open predict UI (scene stays calm until commit). */
      player._simState = S.merge(sim.initial, {});
      player._simApply('exam-reset');
      player._simScenario(sc);
      /* Hide the player's own predict box — exam chrome owns the question. */
      if (player._simPredict) player._simPredict.hidden = true;
    }

    function renderQuestion() {
      if (!exam) return;
      var item = exam.items[idx];
      answering = false;
      itemT0 = (window.performance && performance.now()) || Date.now();
      $('[data-il-exam-progress]').textContent = 'Q ' + (idx + 1) + '/' + exam.items.length;
      $('[data-il-exam-domain]').textContent = item.domain;
      $('[data-il-exam-label]').textContent = item.title + ' · ' + item.label;
      $('[data-il-exam-q]').textContent = item.q;
      $('[data-il-exam-feedback]').textContent = '';
      var box = $('[data-il-exam-options]');
      box.innerHTML = '';
      item.order = S.shuffleOrder(item.options.length);
      item.order.forEach(function (optIdx) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'il-exam-opt';
        b.textContent = item.options[optIdx];
        b.setAttribute('data-il-exam-option', String(optIdx));
        b.addEventListener('click', function () { commit(optIdx, b); });
        box.appendChild(b);
      });
      mountScene(item).then(function () { openScenario(item); });
    }

    function commit(choice, btn) {
      if (!exam || answering) return;
      answering = true;
      var item = exam.items[idx];
      var ms = ((window.performance && performance.now()) || Date.now()) - itemT0;
      var graded = E.gradeItem(item, choice, ms);
      item.choice = graded.choice;
      item.correct = graded.correct;
      item.ms = graded.ms;
      var opts = document.querySelectorAll('[data-il-exam-option]');
      for (var i = 0; i < opts.length; i++) {
        opts[i].disabled = true;
        var oi = Number(opts[i].getAttribute('data-il-exam-option'));
        if (oi === choice) opts[i].setAttribute('data-picked', '1');
        if (oi === item.answer) opts[i].setAttribute('data-correct', '1');
        else if (oi === choice) opts[i].setAttribute('data-correct', '0');
      }
      $('[data-il-exam-feedback]').textContent = (graded.correct ? 'Correct. ' : 'Not quite. ') + item.why;
      /* Reveal on the 3D stage via the player's pending commit path if still open. */
      var player = stage && stage._ilImmersive;
      if (player && player._simPending) {
        try { player._simCommit(choice); } catch (e) { /* ignore */ }
      } else if (player) {
        var sim = S.get(item.simId);
        var sc = sim.scenarios.filter(function (x) { return x.id === item.scenarioId; })[0];
        if (sc) {
          player._simState = S.merge(player._simState, sc.set);
          player._simApply('exam:' + sc.id);
        }
      }
      setTimeout(function () {
        if (idx + 1 >= exam.items.length) finish('done');
        else { idx += 1; renderQuestion(); }
      }, graded.correct ? 900 : 1400);
    }

    function finish(reason) {
      stopTimer();
      if (!exam) return;
      var summary = E.summarize(exam);
      E.recordAttempt(exam, summary);
      show(lobby, false); show(run, false); show(done, true);
      var sum = $('[data-il-exam-summary]');
      if (sum) {
        sum.textContent = summary.correct + ' / ' + summary.total + ' correct (' + summary.pct + '%). '
          + (summary.passed ? 'Pass bar (' + summary.passPct + '%) cleared.' : 'Under the ' + summary.passPct + '% pass bar.')
          + (reason === 'time' ? ' Time expired — unanswered items count as incorrect.' : '');
      }
      var tb = $('[data-il-exam-domains] tbody');
      if (tb) {
        tb.innerHTML = '';
        Object.keys(summary.byDomain).sort().forEach(function (dom) {
          var d = summary.byDomain[dom];
          var tr = document.createElement('tr');
          tr.innerHTML = '<td class="py-1 pr-4">' + dom + '</td><td>' + d.correct + '/' + d.total + '</td>';
          tb.appendChild(tr);
        });
      }
      var hon = $('[data-il-exam-honesty]');
      if (hon) hon.textContent = exam.honesty;
      document.documentElement.setAttribute('data-il-exam-finished', summary.passed ? 'pass' : 'fail');
      document.documentElement.setAttribute('data-il-exam-score', String(summary.correct) + '/' + String(summary.total));
      renderHistory();
    }

    function start(opts) {
      stopTimer();
      exam = E.buildExam(S, opts || {});
      idx = 0;
      document.documentElement.removeAttribute('data-il-exam-finished');
      document.documentElement.removeAttribute('data-il-exam-score');
      show(lobby, false); show(done, false); show(run, true);
      timerId = setInterval(tick, 250);
      tick();
      renderQuestion();
    }

    document.querySelectorAll('[data-il-exam-start]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var count = Number(btn.getAttribute('data-count')) || E.DEFAULTS.count;
        var minutes = Number(btn.getAttribute('data-minutes')) || E.DEFAULTS.minutes;
        start({ count: count, minutes: minutes });
      });
    });
    var retry = $('[data-il-exam-retry]');
    if (retry) retry.addEventListener('click', function () {
      show(done, false); show(lobby, true); show(run, false);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
