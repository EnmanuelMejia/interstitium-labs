/**
 * SuperLab Challenge of the Day — copy-paste verify + local proof feed.
 * Storage: il.challenge.done.v1, il.evidence.feed.v1  Mount: [data-il-challenge]
 */
(function (g) {
  'use strict';
  var DONE = 'il.challenge.done.v1';
  var EVIDENCE = 'il.evidence.feed.v1';
  function dayKey() {
    var d = new Date();
    var start = new Date(Date.UTC(2026, 0, 1));
    var day = Math.floor((d - start) / 86400000);
    return day;
  }
  var CHALLENGES = [
    { id: 'cotd-kind-get', title: 'Namespace inventory', steps: ['cd devops-superlab (or your clone)', 'make kind-up  # if cluster not up', 'kubectl -n superlab-dev get deploy,svc,hpa'], prove: 'Paste: you see deploy + svc lines (or honest empty if not provisioned yet).' },
    { id: 'cotd-kustomize', title: 'Kustomize dry-run', steps: ['kustomize build overlays/dev | head -n 40', 'OR: kubectl kustomize overlays/dev | head -n 40'], prove: 'Manifest heads show Namespace / Deployment without secrets in plain text.' },
    { id: 'cotd-argo', title: 'GitOps sync story', steps: ['Open Argo CD UI or CLI for the SuperLab app', 'Explain OutOfSync vs Synced in one sentence'], prove: 'Write: source of truth is Git; live edits are drift.' },
    { id: 'cotd-gatekeeper', title: 'Policy deny demo', steps: ['kubectl apply -f apps/demo/ (or policy sample)', 'Watch admit deny for privileged pod'], prove: 'Note the constraint name that denied the object.' },
    { id: 'cotd-gha', title: 'CI graph', steps: ['Open .github/workflows in SuperLab', 'Name the job that builds or lints'], prove: 'Job name + one honest limitation (no cloud deploy required).' }
  ];
  function esc(s) { return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function loadDone() { try { return JSON.parse(g.localStorage.getItem(DONE) || '{}') || {}; } catch (e) { return {}; } }
  function saveDone(d) { try { g.localStorage.setItem(DONE, JSON.stringify(d)); } catch (e) {} }
  function pushEvidence(text) {
    try { var feed = JSON.parse(g.localStorage.getItem(EVIDENCE) || '[]') || []; feed.unshift({ t: Date.now(), kind: 'challenge', text: text }); if (feed.length > 48) feed.length = 48; g.localStorage.setItem(EVIDENCE, JSON.stringify(feed)); } catch (e) {}
  }
  function todayChallenge() { return CHALLENGES[Math.abs(dayKey()) % CHALLENGES.length]; }
  function paint(root) {
    var ch = todayChallenge();
    var done = loadDone();
    var isDone = !!done[ch.id];
    var html = '<div class="il-challenge"><p class="il-kicker">Challenge of the Day</p><h3 class="mt-2 font-display text-2xl">' + esc(ch.title) + '</h3><p class="mt-2 text-sm text-muted">One deep SuperLab rhythm — not a fake fleet. Mark done only if you actually ran or honestly simulated the steps.</p><ol class="il-challenge-steps mt-5">';
    ch.steps.forEach(function (s, i) {
      html += '<li class="il-challenge-step"><div class="il-challenge-step-head"><span class="font-mono text-[0.58rem] uppercase tracking-[0.16em] text-gold">Step ' + (i + 1) + '</span><button type="button" class="il-challenge-copy" data-copy="' + esc(s) + '">Copy</button></div><pre class="il-challenge-pre">' + esc(s) + '</pre></li>';
    });
    html += '</ol><p class="mt-4 text-sm text-muted"><strong class="text-paper">Prove:</strong> ' + esc(ch.prove) + '</p>';
    html += '<div class="mt-5 flex flex-wrap gap-3"><button type="button" class="inline-flex h-10 items-center rounded-lg ' + (isDone ? 'border border-cyan/40 text-cyan' : 'bg-paper text-void') + ' px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em]" data-il-challenge-done>' + (isDone ? 'Done ✓' : 'Mark verified') + '</button><a href="/labs/superlab/" class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-paper">SuperLab hub</a><a href="/proof/" class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-paper">Export proof</a></div></div>';
    root.innerHTML = html;
    root.querySelectorAll('[data-copy]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var t = btn.getAttribute('data-copy');
        if (g.navigator && g.navigator.clipboard && g.navigator.clipboard.writeText) g.navigator.clipboard.writeText(t);
        btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = 'Copy'; }, 1200);
      });
    });
    var mark = root.querySelector('[data-il-challenge-done]');
    if (mark) mark.addEventListener('click', function () {
      var d = loadDone(); d[ch.id] = Date.now(); saveDone(d); pushEvidence('CotD verified: ' + ch.title); if (g.ILGame && g.ILGame.award) try { g.ILGame.award('cotd', 10, { id: 'cotd:' + ch.id }); } catch (e) {} paint(root);
    });
  }
  function boot() { var nodes = document.querySelectorAll('[data-il-challenge]'); for (var i = 0; i < nodes.length; i++) paint(nodes[i]); }
  g.ILChallenge = { boot: boot, paint: paint, todayChallenge: todayChallenge };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})(typeof window !== 'undefined' ? window : this);
