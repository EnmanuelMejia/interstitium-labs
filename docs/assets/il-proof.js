/**
 * Proof-of-work portfolio generator from localStorage → markdown / print.
 * Mount: [data-il-proof]
 */
(function (g) {
  'use strict';
  var EXPORT_FLAG = 'il.proof.exported.v1';
  function esc(s) { return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function safeJSON(key, fallback) { try { var raw = g.localStorage.getItem(key); if (raw == null) return fallback; return JSON.parse(raw); } catch (e) { return fallback; } }
  function collect() {
    var evidence = safeJSON('il.evidence.feed.v1', []) || [];
    var adaptive = safeJSON('il.adaptive.v1', null);
    var muse = safeJSON('il.muse.v1', null);
    var demo = safeJSON('il.demo.path.v1', null);
    var challenge = safeJSON('il.challenge.done.v1', {}) || {};
    var game = safeJSON('il.game.v1', null);
    var exam = safeJSON('il.exam.v1', null);
    var pathPick = null; try { pathPick = g.localStorage.getItem('il.os.path.v1'); } catch (e) {}
    var progress = [];
    try { for (var i = 0; i < g.localStorage.length; i++) { var k = g.localStorage.key(i); if (k && k.indexOf('il.progress.') === 0 && g.localStorage.getItem(k) === '1') progress.push(k.replace('il.progress.', '')); } } catch (e2) {}
    var museTurns = 0;
    if (muse && muse.chats && muse.chats.main && muse.chats.main.messages) museTurns = muse.chats.main.messages.filter(function (m) { return m.role === 'user'; }).length;
    return {
      generatedAt: new Date().toISOString(), pathPick: pathPick, evidence: evidence.slice(0, 40),
      adaptive: adaptive ? { placed: !!(adaptive.placed || (adaptive.history && adaptive.history.length)), historyLen: (adaptive.history && adaptive.history.length) || 0, theta: adaptive.theta } : null,
      challengeDone: Object.keys(challenge), demo: demo,
      game: game ? { xp: game.xp, level: game.level } : null,
      museTurns: museTurns, museGoals: muse && muse.goals ? muse.goals.filter(function (x) { return x.done; }).length : 0,
      progress: progress.sort(),
      exam: exam ? { lastScore: exam.lastScore, attempts: exam.attempts || 0, lastAt: exam.lastAt } : null
    };
  }
  function toMarkdown(data) {
    var lines = ['# Interstitium Labs — Proof of Work', '', '_Generated ' + data.generatedAt + ' from local browser progress._', '',
      '> **Honesty label:** Portfolio / study evidence. Not an employment claim, not a cert, not affiliation with any employer named in JD maps.', ''];
    if (data.pathPick) { lines.push('## Committed path', '- `' + data.pathPick + '`', ''); }
    lines.push('## Adaptive placement');
    if (data.adaptive && data.adaptive.placed) { lines.push('- Placement activity recorded (' + data.adaptive.historyLen + ' history events)'); if (data.adaptive.theta != null) lines.push('- Ability estimate θ ≈ ' + data.adaptive.theta); }
    else lines.push('- Not yet placed — open `/adapt/`');
    lines.push('', '## Lab / challenge proof');
    if (data.challengeDone.length) data.challengeDone.forEach(function (id) { lines.push('- Challenge step done: `' + id + '`'); });
    else lines.push('- No CotD steps marked yet — open `/labs/challenge/`');
    lines.push('');
    if (data.evidence.length) { lines.push('## Evidence feed'); data.evidence.forEach(function (e) { var t = e.t ? new Date(e.t).toISOString().slice(0, 10) : '?'; lines.push('- [' + t + '] ' + (e.text || e.title || e.kind || 'entry')); }); lines.push(''); }
    lines.push('## Muse / coach', '- User turns: ' + data.museTurns, '- Goals completed: ' + data.museGoals, '');
    if (data.exam) { lines.push('## Scenario exam', '- Attempts: ' + data.exam.attempts); if (data.exam.lastScore != null) lines.push('- Last score: ' + data.exam.lastScore); lines.push(''); }
    if (data.game) { lines.push('## XP (secondary)', '- Level ' + (data.game.level || 1) + ' · XP ' + (data.game.xp || 0), ''); }
    if (data.progress.length) { lines.push('## Checklist progress'); data.progress.forEach(function (p) { lines.push('- [x] `' + p + '`'); }); lines.push(''); }
    lines.push('## Links', '- Time-to-hire OS: https://interstitiumlabs.dev/os/', '- SuperLab: https://interstitiumlabs.dev/labs/superlab/', '- Adaptive OS: https://interstitiumlabs.dev/adapt/', '- Lab Muse: https://interstitiumlabs.dev/coach/', '', '— Scientia Omnia Vincit');
    return lines.join('\n');
  }
  function markExported() { try { g.localStorage.setItem(EXPORT_FLAG, String(Date.now())); } catch (e) {} }
  function downloadMd(md) { var blob = new Blob([md], { type: 'text/markdown;charset=utf-8' }); var url = URL.createObjectURL(blob); var a = document.createElement('a'); a.href = url; a.download = 'interstitium-proof-of-work.md'; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(url); }, 500); markExported(); }
  function copyMd(md) { if (g.navigator && g.navigator.clipboard && g.navigator.clipboard.writeText) return g.navigator.clipboard.writeText(md).then(function () { markExported(); return true; }); return Promise.reject(new Error('clipboard unavailable')); }
  function printProof(md) {
    markExported();
    var w = g.open('', '_blank');
    if (!w) { g.print(); return; }
    w.document.write('<!DOCTYPE html><html><head><title>IL Proof of Work</title><style>body{font:15px/1.5 system-ui,sans-serif;max-width:42rem;margin:2rem auto;padding:0 1rem;color:#111}pre{white-space:pre-wrap;font:13px/1.45 ui-monospace,monospace;background:#f6f7f9;padding:1rem;border-radius:8px}@media print{body{margin:0}}h1{font-size:1.4rem}</style></head><body><h1>Interstitium Labs — Proof of Work</h1><p><em>Portfolio / study evidence. Not employment or cert claims.</em></p><pre>' + esc(md) + '</pre></body></html>');
    w.document.close(); setTimeout(function () { w.focus(); w.print(); }, 250);
  }
  function paintPreview(root, md) { var pre = root.querySelector('[data-il-proof-md]'); if (pre) pre.textContent = md; var meta = root.querySelector('[data-il-proof-meta]'); if (meta) meta.textContent = 'Snapshot · ' + new Date().toLocaleString(); }
  function mount(root) {
    var md = toMarkdown(collect());
    root.innerHTML = '<div class="il-proof"><p class="il-kicker">Proof-of-work · localStorage → markdown / print</p><h2 class="mt-2 font-display text-3xl tracking-[-0.03em]">Export inspectable evidence</h2><p class="mt-3 max-w-2xl text-sm text-muted">Aggregates adaptive history, CotD / evidence feed, Muse turns, checklist progress, and scenario exam scores. Nothing is invented server-side.</p><p class="mt-2 text-xs text-muted" data-il-proof-meta></p><div class="il-proof-actions mt-6 flex flex-wrap gap-3"><button type="button" class="inline-flex h-10 items-center rounded-lg bg-paper px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em] text-void" data-il-proof-dl>Download .md</button><button type="button" class="inline-flex h-10 items-center rounded-lg border border-cyan/40 px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em] text-cyan" data-il-proof-copy>Copy markdown</button><button type="button" class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em] text-paper" data-il-proof-print>Print / PDF</button><button type="button" class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em] text-paper" data-il-proof-refresh>Refresh</button></div><pre class="il-proof-md mt-6" data-il-proof-md></pre><p class="mt-4 text-xs text-muted">Tip: Print → Save as PDF. Keep honesty labels when pasting into applications.</p></div>';
    paintPreview(root, md);
    root.querySelector('[data-il-proof-dl]').addEventListener('click', function () { downloadMd(toMarkdown(collect())); });
    root.querySelector('[data-il-proof-copy]').addEventListener('click', function () { var btn = root.querySelector('[data-il-proof-copy]'); copyMd(toMarkdown(collect())).then(function () { btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = 'Copy markdown'; }, 1500); }, function () { btn.textContent = 'Select + copy below'; }); });
    root.querySelector('[data-il-proof-print]').addEventListener('click', function () { printProof(toMarkdown(collect())); });
    root.querySelector('[data-il-proof-refresh]').addEventListener('click', function () { paintPreview(root, toMarkdown(collect())); });
  }
  function boot() { var nodes = document.querySelectorAll('[data-il-proof]'); for (var i = 0; i < nodes.length; i++) mount(nodes[i]); }
  g.ILProof = { boot: boot, collect: collect, toMarkdown: toMarkdown, mount: mount };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})(typeof window !== 'undefined' ? window : this);
