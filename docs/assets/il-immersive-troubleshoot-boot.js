/**
 * Boot the hands-on Troubleshooting exam paper (2026-10-28). Depends on ILTroubleshootExam + ILImmersiveCLI +
 * ILImmersiveSims + ILImmersive3D (ScenePlayer with cliExam). Optional: ILImmersiveExam (blueprint weights) and
 * ILImmersiveReview (missed checkpoints → CLI review cards). Relative assets only; simulated shell, no live cluster.
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
  function node(tag, cls, text, attrs) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    for (var k in (attrs || {})) n.setAttribute(k, attrs[k]);
    return n;
  }
  function now() { return (window.performance && performance.now()) || Date.now(); }

  function boot() {
    var T = window.ILTroubleshootExam, C = window.ILImmersiveCLI, S = window.ILImmersiveSims;
    var E = window.ILImmersiveExam || null, R = window.ILImmersiveReview || null;
    if (!T || !C || !S) return;
    var html = document.documentElement;
    var lobby = $('[data-il-ts-lobby]'), run = $('[data-il-ts-run]'), done = $('[data-il-ts-done]');
    var stage = $('[data-il-ts-stage]');
    var paper = null, idx = 0, timerId = null, incT0 = 0, live = null, finished = false;

    var bankEl = $('[data-il-ts-bank]');
    if (bankEl) bankEl.textContent = String(T.bank(C, {}).length);
    var meshEl = $('[data-il-ts-mesh-count]');
    if (meshEl) meshEl.textContent = String(T.bank(C, { mesh: true }).length - T.bank(C, {}).length);
    function renderHistory() {
      var h = $('[data-il-ts-history]'); if (!h) return;
      var last = T.loadStore().last;
      h.textContent = last
        ? ('Last paper on this device: ' + last.pct + '% on the CKA incidents · ' + last.resolved + '/' + last.incidents + ' resolved · ' + (last.passed ? 'pass bar cleared' : 'under pass bar') + '.')
        : 'No troubleshooting papers on this device yet.';
    }
    renderHistory();

    function stopTimer() { if (timerId) { clearInterval(timerId); timerId = null; } }
    function tick() {
      if (!paper || finished) return;
      var left = paper.endsAt - Date.now();
      var el = $('[data-il-ts-timer]');
      if (el) { el.textContent = fmt(left); el.setAttribute('data-urgent', left <= 120000 ? '1' : '0'); }
      if (left <= 0) { gradeCurrent(false); finish('time'); }
    }

    function player() { return stage && stage._ilImmersive; }

    function mountIncident(inc) {
      var API = window.ILImmersive3D;
      live = null;
      if (!stage || !API || !API.mount) return;
      try { if (stage._ilImmersive && stage._ilImmersive.destroy) stage._ilImmersive.destroy(); } catch (e) { /* ignore */ }
      try { delete stage._ilImmersive; } catch (e2) { stage._ilImmersive = null; }
      stage.innerHTML = '';
      ['data-il-sim-ready', 'data-il-sim-verdict', 'data-il-immersive-ready', 'data-il-cli-ready', 'data-il-cli-exam', 'data-il-cli-exam-progress', 'data-il-cli-task', 'data-il-cli-coach']
        .forEach(function (a) { stage.removeAttribute(a); });
      var sim = S.get(inc.simId);
      stage.setAttribute('data-il-sim', inc.simId);
      stage.setAttribute('data-gltf', sim.glb);
      stage.setAttribute('data-immersive', JSON.stringify({ mode: '3d-first', engine: 'three', asset: sim.glb, webgpu: true, sim: inc.simId,
        exam: true, cliExam: { task: inc.taskId, pre: inc.pre } }));
      try { API.mount(stage); } catch (e3) { /* ignore */ }
    }

    function renderIncident() {
      var inc = paper.incidents[idx];
      incT0 = now();
      $('[data-il-ts-progress]').textContent = 'Incident ' + (idx + 1) + '/' + paper.incidents.length;
      $('[data-il-ts-area]').textContent = inc.areaLabel;
      $('[data-il-ts-ticket]').textContent = inc.ticket;
      $('[data-il-ts-live]').textContent = 'Checkpoints verified: 0/' + (inc.steps - inc.pre);
      var nx = $('[data-il-ts-next]');
      nx.textContent = idx + 1 >= paper.incidents.length ? 'Submit & finish paper' : 'Submit & next incident →';
      nx.removeAttribute('data-resolved');
      html.setAttribute('data-il-ts-incident', inc.id);
      mountIncident(inc);
    }

    if (stage) stage.addEventListener('il-immersive-cli-exam', function (ev) {
      var d = ev.detail || {};
      if (!paper || finished || !paper.incidents[idx] || d.task !== paper.incidents[idx].taskId) return;
      live = d;
      var el = $('[data-il-ts-live]');
      if (el) el.textContent = 'Checkpoints verified: ' + d.completed + '/' + d.total + (d.hinted && d.hinted.length ? ' · ' + d.hinted.length + ' hinted' : '') + (d.done ? ' — resolved ✓ submit to move on' : '');
      if (d.done) $('[data-il-ts-next]').setAttribute('data-resolved', '1');
    });

    function gradeCurrent(skipped) {
      if (!paper || !paper.incidents[idx] || paper.incidents[idx].result) return;
      var inc = paper.incidents[idx], p = player(), x = null;
      try { x = p && p._cliExamStatus && p.cfg && p.cfg.cliExam ? p._cliExamStatus() : null; } catch (e) { x = null; }
      inc.result = T.gradeIncident(inc, x ? x.status : null, x ? x.hinted : [], { cmds: x ? x.cmds : 0, ms: now() - incT0, skipped: !!skipped || !x || !x.cmds });
    }

    function next() {
      if (!paper || finished) return;
      gradeCurrent(false);
      if (idx + 1 >= paper.incidents.length) return finish('done');
      idx += 1;
      renderIncident();
    }

    function finish(reason) {
      if (finished) return;
      finished = true;
      stopTimer();
      var sum = T.summarize(paper, E);
      T.recordAttempt(paper, sum);
      var rem = T.remediate(paper, R);
      try { var p = player(); if (p && p.destroy) p.destroy(); } catch (e) { /* ignore */ }
      show(lobby, false); show(run, false); show(done, true);
      $('[data-il-ts-summary]').textContent = 'CKA incidents: ' + sum.pct + '% credit · ' + sum.resolved + '/' + sum.incidents + ' incidents resolved. '
        + (sum.passed ? 'Pass bar (' + sum.passPct + '%) cleared.' : 'Under the ' + sum.passPct + '% pass bar.')
        + (reason === 'time' ? ' Time expired — unfinished incidents keep the checkpoints you verified; untouched ones score 0.' : '');
      renderIncidents();
      renderAreas(sum);
      var wk = $('[data-il-ts-weakest]');
      wk.textContent = '';
      if (sum.weakest) {
        wk.appendChild(document.createTextNode('Weakest troubleshooting area: ' + sum.weakest.label + ' (' + sum.weakest.pct + '%, ' + sum.weakest.lost + ' checkpoints lost). '));
        wk.appendChild(node('a', 'text-cyan', 'Drill it in 3D →', { href: sum.weakest.href, 'data-il-ts-weakest-link': sum.weakest.area }));
        html.setAttribute('data-il-ts-weakest', sum.weakest.area);
      } else {
        wk.textContent = 'No weak area on this paper — every CKA incident was resolved without hints.';
        html.setAttribute('data-il-ts-weakest', '');
      }
      var bp = $('[data-il-ts-blueprint]');
      if (bp) bp.textContent = sum.blueprint
        ? ('CKA blueprint: Troubleshooting is ' + sum.blueprint.weight + '% of the CKA. At ' + sum.blueprint.pct + '% here it leaves ' + sum.blueprint.atStake + ' of those ' + sum.blueprint.weight + ' points at stake. ' + sum.blueprint.honesty)
        : '';
      var ms = $('[data-il-ts-mesh-result]');
      if (ms) ms.textContent = sum.mesh ? ('Service-mesh incident (beyond CKA, not in the score above): ' + sum.mesh.pct + '%' + (sum.mesh.resolved ? ', resolved.' : '.')) : '';
      var rm = $('[data-il-ts-remediate]');
      rm.textContent = '';
      if (rem.queued) {
        rm.appendChild(document.createTextNode('Remediation loop: ' + rem.queued + ' checkpoint' + (rem.queued > 1 ? 's' : '') + ' you missed or needed a hint for became CLI review cards on this device (earlier steps get replayed for you). '));
        rm.appendChild(node('a', 'text-cyan', 'Open review queue →', { href: '/immersive/review/' }));
      } else if (R) rm.textContent = 'Nothing to remediate from this paper.';
      rm.setAttribute('data-queued', String(rem.queued));
      $('[data-il-ts-honesty]').textContent = sum.honesty;
      html.setAttribute('data-il-ts-finished', sum.passed ? 'pass' : 'fail');
      html.setAttribute('data-il-ts-pct', String(sum.pct));
      renderHistory();
    }

    function renderIncidents() {
      var list = $('[data-il-ts-incidents]');
      list.textContent = '';
      paper.incidents.forEach(function (inc, i) {
        var r = inc.result;
        var li = node('li', 'il-ts-inc', null, { 'data-il-ts-inc': inc.id, 'data-pct': String(r ? r.pct : 0), 'data-resolved': r && r.resolved ? '1' : '0' });
        li.appendChild(node('p', 'font-mono text-[0.62rem] uppercase tracking-[0.16em] text-gold', (i + 1) + ' · ' + inc.areaLabel + (inc.cka ? '' : ' · not in CKA score')));
        li.appendChild(node('p', 'mt-1 font-display text-base', inc.title + ' — ' + (r ? r.pct : 0) + '%'));
        li.appendChild(node('p', 'mt-1 text-sm', r ? r.feedback : 'Not reached.', { 'data-il-ts-feedback': '' }));
        if (r && r.notes.length) {
          var ul = node('ul', 'mt-2 space-y-1 text-xs text-muted');
          r.notes.slice(0, 4).forEach(function (n) {
            var row = node('li', null, null, { 'data-il-ts-note': n.how });
            row.appendChild(document.createTextNode((n.how === 'hinted' ? '½ ' : '✗ ') + 'Checkpoint ' + n.n + ': ' + n.label + (n.cmd ? ' — ' : '')));
            if (n.cmd) row.appendChild(node('code', 'text-paper', '$ ' + n.cmd));
            if (n.focus && C.focusLabel) row.appendChild(document.createTextNode(' · look at (3D nodes): ' + String(C.focusLabel(n.focus)).replace(/\\d/g, 'N').replace(/[\^$\\()?*+\[\]]/g, '')));
            ul.appendChild(row);
          });
          if (r.notes.length > 4) ul.appendChild(node('li', null, '… ' + (r.notes.length - 4) + ' more checkpoint(s) after that.'));
          li.appendChild(ul);
        }
        list.appendChild(li);
      });
    }

    function renderAreas(sum) {
      var tb = $('[data-il-ts-areas] tbody');
      tb.textContent = '';
      sum.areas.forEach(function (a) {
        var tr = node('tr', null, null, { 'data-il-ts-area-row': a.area });
        if (sum.weakest && sum.weakest.area === a.area) tr.setAttribute('data-weakest', '1');
        [[a.label + (a.cka ? '' : ' (not in CKA score)'), 'py-1 pr-4'], [String(a.incidents), 'pr-4'], [a.pct + '%', 'pr-4'], [String(a.lost), '']].forEach(function (c) {
          tr.appendChild(node('td', c[1], c[0]));
        });
        tb.appendChild(tr);
      });
    }

    function start(opts) {
      stopTimer();
      var q = /[?&]seed=(\d+)/.exec(location.search);
      if (q) opts.seed = +q[1];
      paper = T.buildPaper(C, opts);
      idx = 0; finished = false;
      html.removeAttribute('data-il-ts-finished');
      html.setAttribute('data-il-ts-seed', String(paper.seed));
      show(lobby, false); show(done, false); show(run, true);
      timerId = setInterval(tick, 250);
      tick();
      renderIncident();
    }

    document.querySelectorAll('[data-il-ts-start]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var mesh = $('[data-il-ts-mesh]');
        start({ count: Number(btn.getAttribute('data-count')) || T.DEFAULTS.count, minutes: Number(btn.getAttribute('data-minutes')) || T.DEFAULTS.minutes,
          mesh: !!(mesh && mesh.checked) });
      });
    });
    var nx = $('[data-il-ts-next]');
    if (nx) nx.addEventListener('click', next);
    var end = $('[data-il-ts-end]');
    if (end) end.addEventListener('click', function () { gradeCurrent(false); finish('done'); });
    var retry = $('[data-il-ts-retry]');
    if (retry) retry.addEventListener('click', function () { show(done, false); show(lobby, true); show(run, false); });
    window.ILTroubleshootExamUI = { paper: function () { return paper; }, next: next };
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
