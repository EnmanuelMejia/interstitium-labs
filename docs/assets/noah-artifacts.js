/* Noah/Genesis Artifacts — building as a first-class twin ability
 * (Phase 2 fold-in expansion, 2026-10-11).
 *
 * The twins build things for the user: web pages/apps, editable
 * documents, presentations, and spreadsheets (budget sheets, study
 * guides, trackers). The flow mirrors how the user already works:
 *   - Ask in chat ("build me a study guide") — long document-like
 *     replies gain a "💾 Save as artifact" action; the artifact is
 *     filed into the Library's Artifacts section.
 *   - Or open the builder (Library → Artifacts → Build): pick a kind,
 *     describe it, the twin drafts the content via /api/noah, edit it
 *     in the split-screen pane, preview it live beside the chat.
 *
 * Kinds and their content formats:
 *   page     — a complete single-file HTML document (sandboxed preview)
 *   document — Markdown (rendered preview, .md export)
 *   slides   — Markdown, slides separated by a line of "---"
 *   sheet    — CSV (table preview, .csv export)
 * Export: page → .html download; document → .md; slides → .md +
 * print view; sheet → .csv. PDF export rides the print view (the
 * browser's Save-as-PDF) — no fake one-click PDF claim.
 *
 * Governance: artifacts are the user's own drafts, stored on-device
 * (localStorage 'il-artifacts-v1', registered for account sync in the
 * staged UI worker patch). Publishing a public share link is OUTWARD —
 * it ships only in the staged server patch, behind draft → approve,
 * and the builder says so plainly. Nothing here sends anything.
 *
 * Server upgrade path is marked SERVER-ADAPTER: when /api/artifacts
 * lands (QUEUED-UI-WORKER-PATCH.md), the store functions below swap
 * their backing from localStorage to the API + sync store, and the
 * orchestrator gains artifact_build / artifact_inspect / artifact_list
 * tools for the tutor + lifecoach agents.
 */
(function () {
  'use strict';
  if (window.ILArtifacts) return;
  if (!document.getElementById('newChatBtn')) return; /* /noah/ only */

  var LS_KEY = 'il-artifacts-v1';
  var KINDS = {
    page: { icon: '🌐', label: 'Web page / app', ext: 'html' },
    document: { icon: '📄', label: 'Document', ext: 'md' },
    slides: { icon: '🎞', label: 'Presentation', ext: 'md' },
    sheet: { icon: '📊', label: 'Spreadsheet', ext: 'csv' },
  };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function $(id) { return document.getElementById(id); }
  function tutorName() {
    try {
      var p = JSON.parse(localStorage.getItem('il-noah-profile') || '{}');
      return p && p.avatar === 'genesis' ? 'Genesis' : 'Noah';
    } catch (e) { return 'Noah'; }
  }
  function tutorId() { return tutorName() === 'Genesis' ? 'genesis' : 'noah'; }
  function uid() { return 'art-' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }

  /* ---------------- Store (SERVER-ADAPTER) ---------------- */
  function load() {
    try {
      var d = JSON.parse(localStorage.getItem(LS_KEY) || 'null');
      if (d && Array.isArray(d.items)) return d;
    } catch (e) {}
    return { items: [] };
  }
  function save(d) {
    try { localStorage.setItem(LS_KEY, JSON.stringify(d)); } catch (e) {}
  }
  function list() { return load().items.slice(); }
  function get(id) {
    var items = load().items;
    for (var i = 0; i < items.length; i++) if (items[i].id === id) return items[i];
    return null;
  }
  function create(kind, title, content) {
    if (!KINDS[kind]) kind = 'document';
    var now = new Date().toISOString();
    var item = {
      id: uid(), kind: kind,
      title: String(title || 'Untitled').slice(0, 120),
      content: String(content || ''),
      created_at: now, updated_at: now,
    };
    var d = load();
    d.items.unshift(item);
    if (d.items.length > 100) d.items = d.items.slice(0, 100);
    save(d);
    return item;
  }
  function update(id, patch) {
    var d = load();
    for (var i = 0; i < d.items.length; i++) {
      if (d.items[i].id === id) {
        if (patch.title != null) d.items[i].title = String(patch.title).slice(0, 120);
        if (patch.content != null) d.items[i].content = String(patch.content);
        if (patch.kind != null && KINDS[patch.kind]) d.items[i].kind = patch.kind;
        d.items[i].updated_at = new Date().toISOString();
        save(d);
        return d.items[i];
      }
    }
    return null;
  }
  function remove(id) {
    var d = load();
    d.items = d.items.filter(function (x) { return x.id !== id; });
    save(d);
  }

  /* ---------------- Rendering ---------------- */
  function mdLite(md) {
    var lines = String(md || '').split('\n');
    var out = [], inList = false;
    function inline(t) {
      return esc(t)
        .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
        .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<i>$2</i>')
        .replace(/`([^`]+)`/g, '<code>$1</code>');
    }
    function closeList() { if (inList) { out.push('</ul>'); inList = false; } }
    lines.forEach(function (ln) {
      var t = ln.replace(/\s+$/, '');
      if (/^#{1,3}\s/.test(t)) {
        closeList();
        var lvl = t.match(/^#+/)[0].length;
        out.push('<h' + lvl + '>' + inline(t.replace(/^#+\s/, '')) + '</h' + lvl + '>');
      } else if (/^\s*[-*]\s+/.test(t)) {
        if (!inList) { out.push('<ul>'); inList = true; }
        out.push('<li>' + inline(t.replace(/^\s*[-*]\s+/, '')) + '</li>');
      } else if (/^\s*$/.test(t)) {
        closeList();
      } else {
        closeList();
        out.push('<p>' + inline(t) + '</p>');
      }
    });
    closeList();
    return out.join('\n');
  }
  function csvTable(csv) {
    var rows = String(csv || '').split('\n').filter(function (r) { return r.trim().length; })
      .map(function (r) { return r.split(',').map(function (c) { return c.trim(); }); });
    if (!rows.length) return '<p>(empty sheet)</p>';
    var h = '<table class="ila-table"><thead><tr>' + rows[0].map(function (c) { return '<th>' + esc(c) + '</th>'; }).join('') + '</tr></thead><tbody>';
    for (var i = 1; i < rows.length; i++) {
      h += '<tr>' + rows[i].map(function (c) { return '<td>' + esc(c) + '</td>'; }).join('') + '</tr>';
    }
    return h + '</tbody></table>';
  }
  function previewSpec(item) {
    var frame = '<style>body{font-family:system-ui,sans-serif;background:#0d1117;color:#e8e4da;margin:0;padding:22px;line-height:1.55}h1,h2,h3{color:#e6c95c}table{border-collapse:collapse;width:100%}th,td{border:1px solid #333;padding:6px 9px;text-align:left}th{background:#161c28}code{background:#161c28;padding:1px 5px;border-radius:4px}.ila-slide{border:1px solid #333;border-radius:12px;padding:20px;margin:0 0 16px;background:#10141d}.ila-slide-n{color:#9a958a;font-size:12px;letter-spacing:.08em}</style>';
    if (item.kind === 'page') return { kind: 'html', title: item.title, html: item.content };
    if (item.kind === 'sheet') return { kind: 'html', title: item.title, html: frame + csvTable(item.content) };
    if (item.kind === 'slides') {
      var parts = String(item.content || '').split(/^\s*---\s*$/m);
      var body = parts.map(function (p, i) {
        return '<div class="ila-slide"><div class="ila-slide-n">SLIDE ' + (i + 1) + '</div>' + mdLite(p.trim()) + '</div>';
      }).join('');
      return { kind: 'html', title: item.title, html: frame + body };
    }
    return { kind: 'html', title: item.title, html: frame + mdLite(item.content) };
  }
  function openPreview(item) {
    if (window.ILSplit) { window.ILSplit.open(previewSpec(item)); return true; }
    return false;
  }

  /* ---------------- Export ---------------- */
  function download(name, text, type) {
    try {
      var blob = new Blob([text], { type: type || 'text/plain;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url; a.download = name;
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
    } catch (e) {}
  }
  function exportItem(item) {
    var base = (item.title || 'artifact').replace(/[^\w\- ]+/g, '').trim().replace(/\s+/g, '-').toLowerCase() || 'artifact';
    if (item.kind === 'page') download(base + '.html', item.content, 'text/html;charset=utf-8');
    else if (item.kind === 'sheet') download(base + '.csv', item.content, 'text/csv;charset=utf-8');
    else download(base + '.md', item.content, 'text/markdown;charset=utf-8');
  }
  function printItem(item) {
    var spec = previewSpec(item);
    var w = window.open('', '_blank');
    if (!w) return;
    w.document.write('<!doctype html><title>' + esc(item.title) + '</title>' + spec.html);
    w.document.close();
    w.focus();
    setTimeout(function () { try { w.print(); } catch (e) {} }, 350);
  }

  /* ---------------- Builder (split-pane editor) ---------------- */
  var bState = { id: null, kind: 'document', drafting: false };
  function builderHtml() {
    var item = bState.id ? get(bState.id) : null;
    var kind = item ? item.kind : bState.kind;
    var kinds = Object.keys(KINDS).map(function (k) {
      return '<button type="button" data-ilak="' + k + '"' + (k === kind ? ' class="on"' : '') +
        (item ? ' disabled' : '') + '>' + KINDS[k].icon + ' ' + KINDS[k].label + '</button>';
    }).join('');
    return '<div class="ila-builder">' +
      '<div class="ila-kinds" role="group" aria-label="Artifact kind">' + kinds + '</div>' +
      '<input type="text" id="ilaTitle" maxlength="120" placeholder="Title" value="' + esc(item ? item.title : '') + '" aria-label="Artifact title">' +
      '<div class="ila-draft"><input type="text" id="ilaPrompt" maxlength="500" placeholder="Describe it — ' +
        esc(tutorName()) + ' drafts it (e.g. “a study guide for the ThreatLocker interview, one page”)” aria-label="Describe the artifact">' +
      '<button type="button" id="ilaDraftBtn">✨ Draft with ' + esc(tutorName()) + '</button></div>' +
      '<textarea id="ilaContent" placeholder="Content — HTML for pages, Markdown for documents & slides (--- between slides), CSV for sheets." aria-label="Artifact content">' +
        esc(item ? item.content : '') + '</textarea>' +
      '<p class="ila-status" id="ilaStatus" role="status"></p>' +
      '<div class="ila-actions">' +
      '<button type="button" id="ilaSave" class="primary">Save artifact</button>' +
      '<button type="button" id="ilaPreview">Preview</button>' +
      '<button type="button" id="ilaExport">Export</button>' +
      '<button type="button" id="ilaPrint">Print / PDF</button>' +
      (item ? '<button type="button" id="ilaDelete">Delete</button>' : '') +
      '</div>' +
      '<p class="ila-note">Artifacts are your drafts, filed in the Library. Publishing a public share link is an outward action — it arrives with the next platform update and will always ask for your approval first.</p>' +
      '</div>';
  }
  function openBuilder(id) {
    bState.id = id || null;
    if (id) { var it = get(id); if (it) bState.kind = it.kind; }
    /* The builder needs live DOM (inputs, buttons), so it mounts
     * through the split pane's first-party mountHtml channel — the
     * sandboxed iframe channel is for artifact content, not editors. */
    if (!window.ILSplit || !window.ILSplit.mountHtml) return false;
    window.ILSplit.mountHtml(builderHtml(), id ? 'Edit artifact' : 'Build an artifact');
    wireBuilder();
    return true;
  }
  function currentDraft() {
    var t = $('ilaTitle'), c = $('ilaContent');
    return {
      title: t ? t.value.trim() : '',
      content: c ? c.value : '',
      kind: bState.id && get(bState.id) ? get(bState.id).kind : bState.kind,
    };
  }
  function wireBuilder() {
    document.querySelectorAll('button[data-ilak]').forEach(function (b) {
      b.addEventListener('click', function () {
        bState.kind = b.getAttribute('data-ilak');
        document.querySelectorAll('button[data-ilak]').forEach(function (x) {
          x.classList.toggle('on', x.getAttribute('data-ilak') === bState.kind);
        });
      });
    });
    var draftBtn = $('ilaDraftBtn');
    if (draftBtn) draftBtn.addEventListener('click', draftWithAI);
    var saveBtn = $('ilaSave');
    if (saveBtn) saveBtn.addEventListener('click', function () {
      var d = currentDraft();
      if (!d.title) d.title = 'Untitled ' + KINDS[d.kind].label;
      var item = bState.id ? update(bState.id, { title: d.title, content: d.content }) : create(d.kind, d.title, d.content);
      if (item) {
        bState.id = item.id;
        setStatus('✓ Saved to your Library → Artifacts.');
        document.dispatchEvent(new CustomEvent('il:artifacts-changed'));
      }
    });
    var pv = $('ilaPreview');
    if (pv) pv.addEventListener('click', function () {
      var d = currentDraft();
      openPreview({ id: bState.id || 'draft', kind: d.kind, title: d.title || 'Preview', content: d.content, created_at: '', updated_at: '' });
    });
    var ex = $('ilaExport');
    if (ex) ex.addEventListener('click', function () {
      var d = currentDraft();
      exportItem({ kind: d.kind, title: d.title || 'artifact', content: d.content });
    });
    var pr = $('ilaPrint');
    if (pr) pr.addEventListener('click', function () {
      var d = currentDraft();
      printItem({ kind: d.kind, title: d.title || 'artifact', content: d.content });
    });
    var del = $('ilaDelete');
    if (del) del.addEventListener('click', function () {
      if (!bState.id) return;
      if (del.getAttribute('data-arm')) {
        remove(bState.id);
        bState.id = null;
        document.dispatchEvent(new CustomEvent('il:artifacts-changed'));
        if (window.ILSplit) window.ILSplit.home();
      } else {
        del.setAttribute('data-arm', '1');
        del.textContent = 'Tap again to delete';
      }
    });
  }
  function setStatus(t) { var s = $('ilaStatus'); if (s) s.textContent = t; }
  function draftWithAI() {
    if (bState.drafting) return;
    var promptEl = $('ilaPrompt');
    var ask = promptEl ? promptEl.value.trim() : '';
    if (!ask) { setStatus('Describe what to build first.'); return; }
    bState.drafting = true;
    var btn = $('ilaDraftBtn');
    if (btn) { btn.disabled = true; btn.textContent = tutorName() + ' is drafting…'; }
    var kind = bState.id && get(bState.id) ? get(bState.id).kind : bState.kind;
    var fmt = kind === 'page'
      ? 'Return ONLY a complete single-file HTML document (inline CSS, no external assets) implementing it.'
      : kind === 'sheet'
        ? 'Return ONLY CSV (header row + data rows, no prose, no code fences).'
        : kind === 'slides'
          ? 'Return ONLY Markdown slides separated by a line containing only --- (no code fences).'
          : 'Return ONLY Markdown (no code fences).';
    fetch('/api/noah', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: [{ role: 'user', content: 'Build this artifact for me: ' + ask + '\n\nKind: ' + KINDS[kind].label + '. ' + fmt }],
        tutor: tutorId(), citations: false,
      }),
    }).then(function (res) { return res.json().catch(function () { return {}; }); })
      .then(function (data) {
        bState.drafting = false;
        if (btn) { btn.disabled = false; btn.textContent = '✨ Draft with ' + tutorName(); }
        var reply = data && typeof data.reply === 'string' ? data.reply.trim() : '';
        if (!reply) { setStatus('The draft came back empty — try again.'); return; }
        reply = reply.replace(/^```[a-z]*\n?/i, '').replace(/```\s*$/, '');
        var c = $('ilaContent');
        if (c) c.value = reply;
        var t = $('ilaTitle');
        if (t && !t.value.trim()) t.value = ask.slice(0, 80);
        setStatus('Draft ready — edit it, then Save. Nothing is published.');
      })
      .catch(function () {
        bState.drafting = false;
        if (btn) { btn.disabled = false; btn.textContent = '✨ Draft with ' + tutorName(); }
        setStatus('Drafting failed just now — you can still write it directly and Save.');
      });
  }

  /* ---------------- Chat → artifact ("Save as artifact") ---------------- */
  function wireChatSave() {
    var thread = $('threadInner');
    if (!thread || !window.MutationObserver) return;
    new MutationObserver(function (muts) {
      muts.forEach(function (m) {
        m.addedNodes.forEach(function (node) {
          if (node.nodeType !== 1) return;
          var msgs = node.classList && node.classList.contains('msg') ? [node]
            : (node.querySelectorAll ? Array.prototype.slice.call(node.querySelectorAll('.msg')) : []);
          msgs.forEach(maybeAddSaveBtn);
        });
      });
    }).observe(thread, { childList: true, subtree: true });
  }
  function maybeAddSaveBtn(msg) {
    if (!msg || msg.querySelector('.ila-save-btn')) return;
    var bubble = msg.querySelector('.bubble') || msg;
    var text = (bubble.innerText || '').trim();
    var isTutor = !/^(you|user)\b/i.test(text.slice(0, 12)) && msg.getAttribute('data-role') !== 'user';
    if (!isTutor || text.length < 600) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'ila-save-btn';
    b.textContent = '💾 Save as artifact';
    b.addEventListener('click', function () {
      var title = (text.split('\n')[0] || 'Saved from chat').replace(/^#+\s*/, '').slice(0, 80);
      var item = create('document', title, text);
      b.textContent = '✓ Saved to Library → Artifacts';
      b.disabled = true;
      document.dispatchEvent(new CustomEvent('il:artifacts-changed'));
      if (window.ILAvatarFx) window.ILAvatarFx.react('💾');
      return item;
    });
    msg.appendChild(b);
  }

  var css = [
    '.ila-save-btn{display:inline-block;margin:.4rem 0 0;background:rgba(201,162,39,.12);border:1px solid rgba(201,162,39,.45);color:#e6c95c;border-radius:999px;padding:.22rem .65rem;font-size:.75rem;cursor:pointer}',
    '.ila-builder{display:flex;flex-direction:column;gap:.6rem;padding:1rem;color:var(--text,#e8e4da);font:14px/1.5 system-ui,sans-serif;background:var(--panel,#10141d);min-height:100%;box-sizing:border-box}',
    '.ila-kinds{display:flex;gap:.4rem;flex-wrap:wrap}',
    '.ila-kinds button{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);color:inherit;border-radius:999px;padding:.35rem .7rem;cursor:pointer;font:inherit;font-size:.82rem}',
    '.ila-kinds button.on{background:#c9a227;color:#0a0e1a;border-color:#c9a227;font-weight:700}',
    '.ila-kinds button:disabled{opacity:.45;cursor:default}',
    '.ila-builder input[type="text"]{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:9px;color:inherit;padding:.55rem .65rem;font:inherit;width:100%;box-sizing:border-box}',
    '.ila-draft{display:flex;gap:.45rem}.ila-draft input{flex:1}',
    '.ila-draft button,.ila-actions button{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.16);color:inherit;border-radius:8px;padding:.5rem .8rem;font:inherit;font-size:.85rem;cursor:pointer}',
    '.ila-actions button.primary{background:#c9a227;color:#0a0e1a;border-color:#c9a227;font-weight:700}',
    '.ila-builder textarea{flex:1;min-height:300px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.14);border-radius:10px;color:inherit;padding:.7rem;font:13px/1.5 ui-monospace,Menlo,monospace;resize:vertical;width:100%;box-sizing:border-box}',
    '.ila-actions{display:flex;gap:.45rem;flex-wrap:wrap}',
    '.ila-status{margin:0;font-size:.83rem;color:#e6c95c;min-height:1.1em}',
    '.ila-note{margin:0;font-size:.78rem;color:var(--muted2,#9a958a)}',
    '.ila-table{border-collapse:collapse;width:100%}.ila-table th,.ila-table td{border:1px solid rgba(255,255,255,.15);padding:5px 8px;text-align:left}',
  ].join('\n');
  var style = document.createElement('style');
  style.id = 'il-artifacts-style';
  style.textContent = css;
  document.head.appendChild(style);

  window.ILArtifacts = {
    list: list, get: get, create: create, update: update, remove: remove,
    openPreview: openPreview, openBuilder: openBuilder,
    exportItem: exportItem, printItem: printItem, kinds: KINDS,
  };
  wireChatSave();
})();
