/**
 * Instant Demo Path — place → drill → coach handoff in <30s.
 * Storage: il.demo.path.v1  Mount: [data-il-demo-path]
 */
(function (g) {
  'use strict';
  var STORAGE = 'il.demo.path.v1';
  var EVIDENCE = 'il.evidence.feed.v1';
  var PLACE = {
    id: 'demo-place-cidr',
    stem: 'A /24 IPv4 prefix holds how many usable host addresses (classic host math)?',
    choices: [{ key: 'A', text: '254' }, { key: 'B', text: '256' }, { key: 'C', text: '24' }, { key: 'D', text: '512' }],
    answerKey: 'A',
    tip: { A: 'Correct — 2^(32-24)=256 addresses; classic usable hosts = 254.', B: '256 is the block size, not classic usable hosts.', C: '24 is the prefix length.', D: 'That is /23 neighborhood — not /24 usable hosts.' }
  };
  var DRILL = {
    id: 'demo-drill-kind',
    stem: 'After `make kind-up` in DevOps SuperLab, which command shows deployments in the lab namespace?',
    choices: [
      { key: 'A', text: 'kubectl -n superlab-dev get deploy,svc,hpa' },
      { key: 'B', text: 'docker ps --filter superlab' },
      { key: 'C', text: 'helm list -A | grep kind' },
      { key: 'D', text: 'kubectl get nodes -o wide --all-namespaces' }
    ],
    answerKey: 'A',
    tip: { A: 'Correct — namespace-scoped get of deploy/svc/hpa.', B: 'Docker alone does not show k8s Deployments.', C: 'Helm may not be the install path.', D: 'Nodes are cluster-scoped; --all-namespaces is wrong here.' }
  };
  function esc(s) { return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function load() { try { var raw = g.localStorage.getItem(STORAGE); if (raw) return JSON.parse(raw); } catch (e) {} return { v: 1, step: 'place', answers: {}, t0: Date.now() }; }
  function save(s) { try { g.localStorage.setItem(STORAGE, JSON.stringify(s)); } catch (e) {} }
  function pushEvidence(text) {
    try { var feed = JSON.parse(g.localStorage.getItem(EVIDENCE) || '[]') || []; feed.unshift({ t: Date.now(), kind: 'demo', text: text }); if (feed.length > 48) feed.length = 48; g.localStorage.setItem(EVIDENCE, JSON.stringify(feed)); } catch (e) {}
  }
  function paintQ(root, state, q, nextStep) {
    var html = '<div class="il-demo-card il-ux-card"><p class="il-demo-stem">' + esc(q.stem) + '</p><div class="il-demo-choices">';
    q.choices.forEach(function (c) {
      html += '<button type="button" class="il-demo-choice" data-key="' + c.key + '"><strong>' + c.key + '.</strong> ' + esc(c.text) + '</button>';
    });
    html += '</div><p class="il-demo-fb" data-fb></p></div>';
    root.querySelector('[data-il-demo-body]').innerHTML = html;
    root.querySelectorAll('.il-demo-choice').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var key = btn.getAttribute('data-key');
        var ok = key === q.answerKey;
        state.answers[q.id] = key;
        root.querySelectorAll('.il-demo-choice').forEach(function (b) { b.disabled = true; b.classList.toggle('is-ok', b.getAttribute('data-key') === q.answerKey); b.classList.toggle('is-bad', b.getAttribute('data-key') === key && !ok); });
        var fb = root.querySelector('[data-fb]');
        fb.textContent = q.tip[key] || q.tip[q.answerKey];
        fb.className = 'il-demo-fb ' + (ok ? 'is-ok' : 'is-bad');
        setTimeout(function () { state.step = nextStep; save(state); render(root, state); }, ok ? 700 : 1100);
      });
    });
  }
  function render(root, state) {
    var elapsed = Math.max(0, Math.round((Date.now() - (state.t0 || Date.now())) / 1000));
    var steps = ['place', 'drill', 'muse'];
    var rail = steps.map(function (id) {
      var on = state.step === id; var done = steps.indexOf(id) < steps.indexOf(state.step) || state.step === 'done';
      return '<li class="il-demo-rail-step' + (on ? ' is-on' : '') + (done && !on ? ' is-done' : '') + '"><span>' + id + '</span><strong>' + ({ place: 'Place', drill: 'Drill', muse: 'Coach' }[id]) + '</strong></li>';
    }).join('');
    root.innerHTML = '<div class="il-demo-path"><p class="il-demo-timer font-mono text-[0.62rem] uppercase tracking-[0.18em] text-muted">Elapsed ' + elapsed + 's · target &lt;30s</p><ul class="il-demo-rail">' + rail + '</ul><div data-il-demo-body></div></div>';
    if (state.step === 'place') paintQ(root, state, PLACE, 'drill');
    else if (state.step === 'drill') paintQ(root, state, DRILL, 'muse');
    else if (state.step === 'muse' || state.step === 'done') {
      state.step = 'done'; save(state); pushEvidence('Instant demo path completed');
      root.querySelector('[data-il-demo-body]').innerHTML =
        '<div class="il-demo-card il-ux-card"><p class="il-demo-stem">Socratic handoff ready.</p><p class="mt-3 text-sm text-muted">Local coach rules now. Noah wires Ollama when demand grows — never fake API keys.</p><div class="mt-5 flex flex-wrap gap-3"><a class="inline-flex h-10 items-center rounded-lg bg-paper px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-void" href="/coach/?prompt=' + encodeURIComponent('I just finished the Instant Demo Path. Quiz me on /24 usable hosts and kubectl -n superlab-dev get deploy.') + '">Open Noah</a><a class="inline-flex h-10 items-center rounded-lg border border-cyan/40 px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-cyan" href="/os/">Time-to-hire OS</a><button type="button" class="il-demo-reset text-sm text-muted" data-reset>Reset demo</button></div></div>';
      var r = root.querySelector('[data-reset]');
      if (r) r.addEventListener('click', function () { try { g.localStorage.removeItem(STORAGE); } catch (e) {} render(root, { v: 1, step: 'place', answers: {}, t0: Date.now() }); });
    }
  }
  function mount(root) { render(root, load()); }
  function boot() { var nodes = document.querySelectorAll('[data-il-demo-path]'); for (var i = 0; i < nodes.length; i++) mount(nodes[i]); }
  g.ILDemoPath = { boot: boot, mount: mount };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})(typeof window !== 'undefined' ? window : this);
