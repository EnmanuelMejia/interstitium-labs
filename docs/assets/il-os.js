/**
 * Time-to-hire OS — Adapt → Path → Lab → Noah → Evidence export
 * Mount: [data-il-os]
 */
(function (g) {
  'use strict';
  var STAGES = [
    { id: 'adapt', n: '01', title: 'Adapt placement', href: '/adapt/#session', body: 'CAT probe + fringe. Wrong is a locator.',
      done: function () { try { var s = JSON.parse(g.localStorage.getItem('il.adaptive.v1') || 'null'); return !!(s && (s.placed || (s.history && s.history.length) || s.theta != null)); } catch (e) { return false; } } },
    { id: 'path', n: '02', title: 'Path commitment', href: '/paths/', body: 'Pick a JD-shaped track. Exceed peers without fake fleets.',
      done: function () { try { if (g.localStorage.getItem('il.os.path.v1')) return true; for (var i = 0; i < g.localStorage.length; i++) { var k = g.localStorage.key(i); if (k && k.indexOf('il.progress.') === 0 && g.localStorage.getItem(k) === '1') return true; if (k && k.indexOf('il.mastery.') === 0) return true; } } catch (e) {} return false; } },
    { id: 'lab', n: '03', title: 'Lab proof', href: '/labs/challenge/', body: 'SuperLab / CotD verify — one deep lab, not 800 VMs.',
      done: function () { try { var done = JSON.parse(g.localStorage.getItem('il.challenge.done.v1') || '{}') || {}; if (Object.keys(done).length) return true; var feed = JSON.parse(g.localStorage.getItem('il.evidence.feed.v1') || '[]') || []; return feed.some(function (e) { return e && (e.kind === 'challenge' || e.kind === 'lab' || e.source === 'challenge'); }); } catch (e) { return false; } } },
    { id: 'muse', n: '04', title: 'Noah', href: '/coach/', body: 'Socratic handoff. Local rules → Ollama when demand grows.',
      done: function () { try { var s = JSON.parse(g.localStorage.getItem('il.muse.v1') || 'null'); var msgs = s && s.chats && s.chats.main && s.chats.main.messages; return !!(msgs && msgs.length > 1); } catch (e) { return false; } } },
    { id: 'export', n: '05', title: 'Evidence export', href: '/proof/', body: 'Proof-of-work portfolio from localStorage — markdown / print.',
      done: function () { try { return !!g.localStorage.getItem('il.proof.exported.v1'); } catch (e) { return false; } } }
  ];
  var PATH_PICKS = [
    { id: 'devops-zero-to-hire', label: 'DevOps zero → hire', href: '/paths/devops-zero-to-hire/' },
    { id: 'k8s-cka-exceed', label: 'K8s CKA exceed', href: '/paths/k8s-cka-exceed/' },
    { id: 'devsecops-mastery', label: 'DevSecOps mastery', href: '/paths/devsecops-mastery/' },
    { id: 'aws-cloud-ops', label: 'AWS cloud ops', href: '/paths/aws-cloud-ops/' },
    { id: 'aleks-ops-math', label: 'Ops math (ALEKS-shape)', href: '/paths/aleks-ops-math/' }
  ];
  function esc(s) { return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function pathPick() { try { return g.localStorage.getItem('il.os.path.v1') || ''; } catch (e) { return ''; } }
  function setPathPick(id) { try { g.localStorage.setItem('il.os.path.v1', id); } catch (e) {} }
  function score() { var n = 0; STAGES.forEach(function (s) { if (s.done()) n++; }); return { done: n, total: STAGES.length, pct: Math.round((n / STAGES.length) * 100) }; }
  function paint(root) {
    var sc = score(); var pick = pathPick();
    var html = '<div class="il-os"><p class="il-kicker">Time-to-hire OS · one URL</p><h2 class="mt-2 font-display text-3xl tracking-[-0.03em]">Place → Path → Lab → Noah → Proof</h2><p class="mt-3 max-w-2xl text-sm text-muted">Career-changer loop in five honest stages. Progress is <code class="text-cyan">localStorage</code> you can inspect — never a fake completion certificate.</p>';
    html += '<div class="il-os-meter mt-6" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + sc.pct + '"><div class="il-os-meter-fill" style="width:' + sc.pct + '%"></div><span class="il-os-meter-label">' + sc.done + ' / ' + sc.total + ' stages · ' + sc.pct + '%</span></div><ol class="il-os-stages mt-8">';
    STAGES.forEach(function (s) {
      var ok = s.done();
      html += '<li class="il-os-stage' + (ok ? ' is-done' : '') + '"><div class="il-os-stage-n">' + s.n + '</div><div class="il-os-stage-body"><p class="il-os-stage-title">' + esc(s.title) + (ok ? ' <span class="il-os-check">done</span>' : '') + '</p><p class="il-os-stage-text">' + esc(s.body) + '</p><a class="il-os-stage-cta" href="' + s.href + '">' + (ok ? 'Revisit' : 'Open') + ' →</a></div></li>';
    });
    html += '</ol><div class="il-os-pathpick mt-10"><p class="il-kicker">Path commitment</p><p class="mt-2 text-sm text-muted">Mark one track so the OS can route lab + Noah's prompts.</p><div class="il-os-pathgrid mt-4">';
    PATH_PICKS.forEach(function (p) {
      html += '<button type="button" class="il-os-pathbtn' + (pick === p.id ? ' is-on' : '') + '" data-il-os-path="' + esc(p.id) + '">' + esc(p.label) + '</button>';
    });
    html += '</div></div><div class="il-os-actions mt-8 flex flex-wrap gap-3"><a href="/cinema/" class="inline-flex h-10 items-center rounded-lg border border-cyan/40 px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em] text-cyan">499P9 cinema canvas</a><a href="/exam/" class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em] text-paper">Scenario exam</a><a href="/proof/" class="inline-flex h-10 items-center rounded-lg bg-paper px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em] text-void">Export proof</a><a href="/demo/" class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em] text-paper">Instant demo</a></div><p class="mt-6 text-xs text-muted">Honesty: one SuperLab + CotD ≠ KodeKloud fleet. Noah stays on local questions first.</p></div>';
    root.innerHTML = html;
    root.querySelectorAll('[data-il-os-path]').forEach(function (btn) {
      btn.addEventListener('click', function () { setPathPick(btn.getAttribute('data-il-os-path')); paint(root); });
    });
  }
  function boot() { var nodes = document.querySelectorAll('[data-il-os]'); for (var i = 0; i < nodes.length; i++) paint(nodes[i]); }
  g.ILOS = { boot: boot, paint: paint, stages: STAGES, score: score };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})(typeof window !== 'undefined' ? window : this);
