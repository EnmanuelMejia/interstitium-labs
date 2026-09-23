/**
 * Scenario exam simulator — remediations into /adapt and /coach.
 * Storage: il.exam.v1  Mount: [data-il-exam]
 */
(function (g) {
  'use strict';
  var STORAGE = 'il.exam.v1';
  var BANK = [
    { id: 'ex-cidr', domain: 'Networking', stem: 'A VPC uses 10.0.0.0/16. You need a public subnet with ~250 usable hosts. Which CIDR is correct?', choices: [{ key: 'A', text: '10.0.1.0/24' }, { key: 'B', text: '10.0.1.0/28' }, { key: 'C', text: '10.0.0.0/8' }, { key: 'D', text: '10.0.1.0/32' }], answer: 'A', why: '/24 yields 256 addresses (~254 usable classic).', remediate: { adapt: '/adapt/#session', coach: '/coach/?prompt=' + encodeURIComponent('Explain CIDR /24 vs /28 for a VPC public subnet.') } },
    { id: 'ex-crashloop', domain: 'Kubernetes', stem: 'A Deployment is CrashLoopBackOff. First three checks?', choices: [{ key: 'A', text: 'kubectl describe pod → logs → events / probes / config' }, { key: 'B', text: 'Delete the namespace and recreate from memory' }, { key: 'C', text: 'Scale to 100 replicas immediately' }, { key: 'D', text: 'Disable RBAC cluster-wide' }], answer: 'A', why: 'Describe + logs + events locate probe/config/image faults.', remediate: { adapt: '/adapt/#session', coach: '/coach/?prompt=' + encodeURIComponent('CrashLoopBackOff — first three checks.') } },
    { id: 'ex-iam', domain: 'Cloud IAM', stem: 'Least privilege for a CI job that pushes an image to a private registry?', choices: [{ key: 'A', text: 'Scoped push role / short-lived token to that registry only' }, { key: 'B', text: 'Root / Owner on the whole cloud account' }, { key: 'C', text: 'Commit long-lived admin keys into the repo' }, { key: 'D', text: 'Disable MFA for the service account' }], answer: 'A', why: 'Scope + short-lived credentials. Never commit admin keys.', remediate: { adapt: '/adapt/#session', coach: '/coach/?prompt=' + encodeURIComponent('Least-privilege IAM for a CI push to a private registry.') } },
    { id: 'ex-gitops', domain: 'GitOps', stem: 'Argo CD shows OutOfSync after a bad overlay. Safest next move?', choices: [{ key: 'A', text: 'Diff the sync, fix Git, then sync — never kubectl-edit production drift' }, { key: 'B', text: 'kubectl edit live objects and leave Git stale' }, { key: 'C', text: 'Force sync --prune without reading the diff' }, { key: 'D', text: 'Delete the Application CR and hope' }], answer: 'A', why: 'Git is source of truth. Diff → fix → sync.', remediate: { adapt: '/paths/iac-terraform-gitops/', coach: '/coach/?prompt=' + encodeURIComponent('Diff a bad overlay before sync.') } },
    { id: 'ex-slo', domain: 'SRE', stem: 'Error budget is burning fast on a demo API. What do you stop?', choices: [{ key: 'A', text: 'Feature launches / risky changes until burn cools; focus on reliability' }, { key: 'B', text: 'All monitoring (noise)' }, { key: 'C', text: 'Incident reviews' }, { key: 'D', text: 'Rollback capability' }], answer: 'A', why: 'Burning budget means freeze risk and restore reliability.', remediate: { adapt: '/paths/platform-sre/', coach: '/coach/?prompt=' + encodeURIComponent('Error budget burn — what do you stop shipping?') } },
    { id: 'ex-honesty', domain: 'Interview', stem: 'Interviewer asks about a production K8s incident you have never owned. Best answer?', choices: [{ key: 'A', text: 'Honest: lab/portfolio practice + how you would run RCA; no fake tenure' }, { key: 'B', text: 'Invent a multi-year SRE war story' }, { key: 'C', text: 'Claim SuperLab was a paid bank job' }, { key: 'D', text: 'Refuse to discuss incidents at all' }], answer: 'A', why: 'Honesty compounds. Label portfolio labs as labs.', remediate: { adapt: '/prep/drills/desk-interview/', coach: '/coach/?prompt=' + encodeURIComponent('Mock: production incident you never had — answer honestly.') } },
    { id: 'ex-chmod', domain: 'Linux', stem: 'chmod 4755 on a binary — when is setuid dangerous?', choices: [{ key: 'A', text: 'When the binary can be hijacked or is writable by untrusted users' }, { key: 'B', text: 'Never — 4755 is always safe' }, { key: 'C', text: 'Only on directories' }, { key: 'D', text: 'Only if the file is owned by nobody' }], answer: 'A', why: 'setuid elevates to owner UID. Writable setuid binaries are classic privilege escalation.', remediate: { adapt: '/adapt/#session', coach: '/coach/?prompt=' + encodeURIComponent('chmod 4755 — when is setuid dangerous?') } },
    { id: 'ex-probe', domain: 'Kubernetes', stem: 'Readiness vs liveness — which statement is true?', choices: [{ key: 'A', text: 'Readiness removes from Service endpoints; liveness may restart the container' }, { key: 'B', text: 'They are identical' }, { key: 'C', text: 'Liveness controls Service membership only' }, { key: 'D', text: 'Neither should ever be configured' }], answer: 'A', why: 'Readiness = traffic; liveness = restart.', remediate: { adapt: '/paths/kubernetes-sre/', coach: '/coach/?prompt=' + encodeURIComponent('Explain readiness vs liveness to a hiring manager.') } }
  ];
  function load() { try { var raw = g.localStorage.getItem(STORAGE); if (raw) return JSON.parse(raw); } catch (e) {} return { v: 1, attempts: 0, lastScore: null, lastAt: null, history: [] }; }
  function save(s) { try { g.localStorage.setItem(STORAGE, JSON.stringify(s)); } catch (e) {} }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function shuffle(arr) { var a = arr.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function mount(root) {
    var state = { items: shuffle(BANK).slice(0, 6), idx: 0, answers: {}, finished: false };
    function render() {
      if (state.finished) {
        var correct = 0; var miss = [];
        state.items.forEach(function (q) { if (state.answers[q.id] === q.answer) correct++; else miss.push(q); });
        var pct = Math.round((correct / state.items.length) * 100);
        var store = load(); store.attempts = (store.attempts || 0) + 1; store.lastScore = pct; store.lastAt = Date.now(); store.history = store.history || []; store.history.unshift({ t: Date.now(), score: pct, n: state.items.length }); if (store.history.length > 20) store.history.length = 20; save(store);
        try { var feed = JSON.parse(g.localStorage.getItem('il.evidence.feed.v1') || '[]') || []; feed.unshift({ t: Date.now(), kind: 'exam', text: 'Scenario exam ' + pct + '% (' + correct + '/' + state.items.length + ')' }); if (feed.length > 48) feed.length = 48; g.localStorage.setItem('il.evidence.feed.v1', JSON.stringify(feed)); } catch (e2) {}
        if (g.ILGame && g.ILGame.award) { try { g.ILGame.award('exam_finish', Math.max(5, Math.round(pct / 10)), { id: 'exam:' + Date.now() }); } catch (e3) {} }
        var html = '<div class="il-exam"><p class="il-kicker">Scenario exam · result</p><h2 class="mt-2 font-display text-3xl">' + pct + '%</h2><p class="mt-2 text-sm text-muted">' + correct + ' / ' + state.items.length + ' correct · attempt #' + store.attempts + '</p>';
        if (!miss.length) {
          html += '<p class="mt-4 text-sm text-cyan">Clean pass. Export proof or deepen a path.</p><div class="mt-6 flex flex-wrap gap-3"><a class="inline-flex h-10 items-center rounded-lg bg-paper px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-void" href="/proof/">Export proof</a><a class="inline-flex h-10 items-center rounded-lg border border-cyan/40 px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-cyan" href="/os/">Time-to-hire OS</a><button type="button" class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-paper" data-il-exam-retry>Retry</button></div>';
        } else {
          html += '<p class="mt-4 text-sm text-muted">Misses remediate into Adapt + Noah — not an answer dump.</p><ul class="il-exam-remediate mt-6">';
          miss.forEach(function (q) {
            html += '<li class="il-exam-miss"><p class="font-mono text-[0.58rem] uppercase tracking-[0.16em] text-gold">' + esc(q.domain) + '</p><p class="mt-1 text-sm text-paper">' + esc(q.stem) + '</p><p class="mt-2 text-xs text-muted">' + esc(q.why) + '</p><div class="mt-3 flex flex-wrap gap-2"><a class="text-cyan text-xs uppercase tracking-[0.14em]" href="' + q.remediate.adapt + '">Adapt remediations →</a><a class="text-cyan text-xs uppercase tracking-[0.14em]" href="' + q.remediate.coach + '">Ask Noah →</a></div></li>';
          });
          html += '</ul><div class="mt-6 flex flex-wrap gap-3"><button type="button" class="inline-flex h-10 items-center rounded-lg bg-paper px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-void" data-il-exam-retry>Retry exam</button><a class="inline-flex h-10 items-center rounded-lg border border-cyan/40 px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-cyan" href="/adapt/">Open Adapt</a><a class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-paper" href="/coach/">Noah</a></div>';
        }
        html += '</div>'; root.innerHTML = html;
        var retry = root.querySelector('[data-il-exam-retry]');
        if (retry) retry.addEventListener('click', function () { state = { items: shuffle(BANK).slice(0, 6), idx: 0, answers: {}, finished: false }; render(); });
        return;
      }
      var q = state.items[state.idx];
      var html2 = '<div class="il-exam"><p class="il-kicker">Scenario exam · ' + (state.idx + 1) + ' / ' + state.items.length + ' · ' + esc(q.domain) + '</p><h2 class="mt-3 font-display text-2xl tracking-[-0.02em]">' + esc(q.stem) + '</h2><div class="il-exam-choices mt-6">';
      q.choices.forEach(function (c) { html2 += '<button type="button" class="il-exam-choice" data-key="' + c.key + '"><span class="il-exam-key">' + c.key + '</span> ' + esc(c.text) + '</button>'; });
      html2 += '</div><p class="mt-4 text-xs text-muted">Misses open remediations into <a class="text-cyan" href="/adapt/">/adapt</a> and <a class="text-cyan" href="/coach/">/coach</a>.</p></div>';
      root.innerHTML = html2;
      root.querySelectorAll('[data-key]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          state.answers[q.id] = btn.getAttribute('data-key');
          if (state.idx >= state.items.length - 1) state.finished = true; else state.idx++;
          render();
        });
      });
    }
    render();
  }
  function boot() { var nodes = document.querySelectorAll('[data-il-exam]'); for (var i = 0; i < nodes.length; i++) mount(nodes[i]); }
  g.ILExam = { boot: boot, mount: mount, BANK: BANK };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})(typeof window !== 'undefined' ? window : this);
