/* Interstitium Labs — Personal Notes vault (il-notes.js).
 * Obsidian/Logseq model, distilled and built original (see
 * ~/workspace/notes-integration/DISTILL.md):
 *   - local-first Markdown notes, one vault per user on this device
 *     (localStorage 'il-notes-v1'; KV adapter drops in when identity lands)
 *   - [[wikilinks]] between notes, automatic backlinks, full-text search
 *   - notes auto-created from lessons and from Noah/Genesis conversations
 *   - Notion-style block helpers + templates on plain portable Markdown
 * Vanilla JS, zero dependencies, ES5-compatible. Exposes window.ILNotes.
 * All user text is escaped before any HTML rendering — notes are data,
 * never markup. */
(function (g) {
  'use strict';

  var LS_KEY = 'il-notes-v1';

  /* ---------------- store ---------------- */

  function blank() { return { v: 1, notes: [], bookmarks: [] }; }

  function load() {
    try {
      var raw = g.localStorage && g.localStorage.getItem(LS_KEY);
      if (raw) {
        var d = JSON.parse(raw);
        if (d && Array.isArray(d.notes)) {
          if (!Array.isArray(d.bookmarks)) d.bookmarks = [];
          return d;
        }
      }
    } catch (e) {}
    return blank();
  }

  function save(d) {
    try { if (g.localStorage) g.localStorage.setItem(LS_KEY, JSON.stringify(d)); } catch (e) {}
    try { g.dispatchEvent(new g.CustomEvent('il-notes-changed', { detail: { count: d.notes.length } })); } catch (e) {}
  }

  function uid() {
    return 'n_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  }

  function normTitle(t) { return String(t == null ? '' : t).trim().toLowerCase().replace(/\s+/g, ' '); }

  /* ---------------- wikilinks ---------------- */

  function parseLinks(body) {
    var out = [], seen = {}, m;
    var re = /\[\[([^\]\n]{1,120})\]\]/g;
    var s = String(body || '');
    while ((m = re.exec(s))) {
      var t = m[1].split('|')[0].trim();
      var k = normTitle(t);
      if (t && !seen[k]) { seen[k] = 1; out.push(t); }
    }
    return out;
  }

  /* ---------------- CRUD ---------------- */

  function all() { return load().notes.slice(); }

  function get(id) {
    var d = load();
    for (var i = 0; i < d.notes.length; i++) if (d.notes[i].id === id) return d.notes[i];
    return null;
  }

  function findByTitle(title) {
    var k = normTitle(title), d = load();
    for (var i = 0; i < d.notes.length; i++) if (normTitle(d.notes[i].title) === k) return d.notes[i];
    return null;
  }

  function create(opts) {
    opts = opts || {};
    var d = load();
    var now = Date.now();
    var note = {
      id: uid(),
      title: String(opts.title || 'Untitled note').slice(0, 160),
      body: String(opts.body || ''),
      tags: Array.isArray(opts.tags) ? opts.tags.slice(0, 12) : [],
      kind: opts.kind === 'map' ? 'map' : 'note',
      map: opts.map || null,
      source: opts.source || { type: 'manual' },
      createdAt: now, updatedAt: now
    };
    d.notes.unshift(note);
    save(d);
    return note;
  }

  function update(id, patch) {
    var d = load();
    for (var i = 0; i < d.notes.length; i++) {
      if (d.notes[i].id === id) {
        var n = d.notes[i];
        if (patch.title != null) n.title = String(patch.title).slice(0, 160);
        if (patch.body != null) n.body = String(patch.body);
        if (patch.tags != null) n.tags = Array.isArray(patch.tags) ? patch.tags.slice(0, 12) : n.tags;
        if (patch.map !== undefined) n.map = patch.map;
        n.updatedAt = Date.now();
        save(d);
        return n;
      }
    }
    return null;
  }

  function remove(id) {
    var d = load(), before = d.notes.length;
    d.notes = d.notes.filter(function (n) { return n.id !== id; });
    if (d.notes.length !== before) { save(d); return true; }
    return false;
  }

  /* ---------------- links graph (derived, never stored) ---------------- */

  function outlinks(note) {
    var titles = parseLinks(note.body), resolved = [], unresolved = [];
    titles.forEach(function (t) {
      var hit = findByTitle(t);
      if (hit && hit.id !== note.id) resolved.push({ title: t, note: hit });
      else if (!hit) unresolved.push({ title: t, note: null });
    });
    return { resolved: resolved, unresolved: unresolved };
  }

  function backlinks(noteOrTitle) {
    var title = typeof noteOrTitle === 'string' ? noteOrTitle : noteOrTitle.title;
    var k = normTitle(title), d = load(), out = [];
    d.notes.forEach(function (n) {
      if (normTitle(n.title) === k) return;
      var links = parseLinks(n.body);
      for (var i = 0; i < links.length; i++) {
        if (normTitle(links[i]) === k) { out.push(n); return; }
      }
    });
    return out;
  }

  /* ---------------- search ---------------- */

  function excerpt(body, q) {
    var s = String(body || '').replace(/\s+/g, ' ');
    var idx = s.toLowerCase().indexOf(q.toLowerCase());
    if (idx === -1) return s.slice(0, 140);
    var start = Math.max(0, idx - 50);
    return (start ? '…' : '') + s.slice(start, idx + q.length + 90) + '…';
  }

  function search(q) {
    q = String(q || '').trim();
    if (!q) return all().map(function (n) { return { note: n, score: 1, excerpt: excerpt(n.body, '') }; });
    var terms = q.toLowerCase().split(/\s+/), d = load(), out = [];
    d.notes.forEach(function (n) {
      var hayT = n.title.toLowerCase(), hayB = String(n.body || '').toLowerCase(),
          hayTags = (n.tags || []).join(' ').toLowerCase(), score = 0;
      terms.forEach(function (t) {
        if (hayT.indexOf(t) !== -1) score += 5;
        if (hayTags.indexOf(t) !== -1) score += 3;
        var c = hayB.split(t).length - 1; score += Math.min(4, c);
      });
      if (score > 0) out.push({ note: n, score: score, excerpt: excerpt(n.body, terms[0]) });
    });
    out.sort(function (a, b) { return b.score - a.score || b.note.updatedAt - a.note.updatedAt; });
    return out;
  }

  /* ---------------- bookmarks ---------------- */

  function bookmarks() { return load().bookmarks.slice(); }

  function addBookmark(label, url) {
    var d = load();
    d.bookmarks = d.bookmarks.filter(function (b) { return b.url !== url; });
    d.bookmarks.unshift({ label: String(label || url).slice(0, 120), url: String(url), at: Date.now() });
    d.bookmarks = d.bookmarks.slice(0, 60);
    save(d);
    return d.bookmarks;
  }

  function removeBookmark(url) {
    var d = load();
    d.bookmarks = d.bookmarks.filter(function (b) { return b.url !== url; });
    save(d);
  }

  /* ---------------- markdown rendering (escape-first, wikilink-aware) ---------------- */

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function safeUrl(u) {
  /* only http(s), root-relative, or in-page anchors survive */
    u = String(u || '').trim();
    if (/^(https:\/\/|\/(?!\/)|#)/i.test(u) && !/[\s"'<>]/.test(u)) return u;
    return null;
  }

  function inline(s) {
    /* s is already HTML-escaped. Order: code, wikilinks, md links, bold, italic. */
    s = s.replace(/`([^`\n]{1,300})`/g, function (m, c) { return '\u0001' + c + '\u0002'; });
    s = s.replace(/\[\[([^\]\n]{1,120})\]\]/g, function (m, t) {
      var title = t.split('|')[0].trim(), label = (t.split('|')[1] || t).trim();
      var hit = findByTitle(title);
      return '<a href="#" class="iln-wikilink' + (hit ? '' : ' iln-unresolved') +
        '" data-iln-title="' + esc(title) + '">' + esc(label) + '</a>';
    });
    s = s.replace(/\[([^\]\n]{1,160})\]\(([^)\s]{1,600})\)/g, function (m, label, url) {
      var u = safeUrl(url.replace(/&amp;/g, '&'));
      return u ? '<a href="' + esc(u) + '" rel="noopener noreferrer">' + label + '</a>' : label;
    });
    s = s.replace(/\*\*([^*\n]{1,400})\*\*/g, '<strong>$1</strong>');
    s = s.replace(/(^|[^*])\*([^*\n]{1,300})\*/g, '$1<em>$2</em>');
    s = s.replace(/\u0001([^\u0002]*)\u0002/g, function (m, c) { return '<code>' + c + '</code>'; });
    return s;
  }

  function renderMarkdown(src) {
    var lines = String(src || '').replace(/\r\n?/g, '\n').split('\n');
    var html = [], i = 0, para = [], listType = null, codeBuf = null, tableBuf = null;

    function flushPara() { if (para.length) { html.push('<p>' + inline(esc(para.join(' '))) + '</p>'); para = []; } }
    function flushList() { if (listType) { html.push(listType === 'ol' ? '</ol>' : '</ul>'); listType = null; } }
    function flushTable() {
      if (!tableBuf) return;
      var rows = tableBuf.filter(function (r) { return !/^\|?[\s:|-]+\|?$/.test(r); });
      if (rows.length) {
        html.push('<div class="iln-tablewrap"><table>');
        rows.forEach(function (r, ri) {
          var cells = r.replace(/^\||\|$/g, '').split('|').map(function (c) { return c.trim(); });
          var tag = ri === 0 ? 'th' : 'td';
          html.push('<tr>' + cells.map(function (c) { return '<' + tag + '>' + inline(esc(c)) + '</' + tag + '>'; }).join('') + '</tr>');
        });
        html.push('</table></div>');
      }
      tableBuf = null;
    }
    function flushAll() { flushPara(); flushList(); flushTable(); }

    while (i < lines.length) {
      var line = lines[i];
      if (codeBuf !== null) {
        if (/^\s*```/.test(line)) { html.push('<pre><code>' + esc(codeBuf.join('\n')) + '</code></pre>'); codeBuf = null; }
        else codeBuf.push(line);
        i++; continue;
      }
      if (/^\s*```/.test(line)) { flushAll(); codeBuf = []; i++; continue; }
      if (/^\s*\|.*\|\s*$/.test(line)) { flushPara(); flushList(); (tableBuf = tableBuf || []).push(line.trim()); i++; continue; }
      flushTable();
      var h = /^(#{1,4})\s+(.*)$/.exec(line);
      if (h) { flushPara(); flushList(); html.push('<h' + h[1].length + '>' + inline(esc(h[2])) + '</h' + h[1].length + '>'); i++; continue; }
      if (/^\s*(-{3,}|\*{3,})\s*$/.test(line)) { flushAll(); html.push('<hr>'); i++; continue; }
      var q = /^>\s?(.*)$/.exec(line);
      if (q) { flushPara(); flushList(); html.push('<blockquote>' + inline(esc(q[1])) + '</blockquote>'); i++; continue; }
      var cb = /^(\s*)[-*]\s+\[( |x|X)\]\s+(.*)$/.exec(line);
      if (cb) {
        flushPara();
        if (listType !== 'ul') { flushList(); html.push('<ul class="iln-checks">'); listType = 'ul'; }
        html.push('<li><label><input type="checkbox" disabled' + (cb[2].toLowerCase() === 'x' ? ' checked' : '') + '> ' + inline(esc(cb[3])) + '</label></li>');
        i++; continue;
      }
      var li = /^(\s*)([-*]|\d+\.)\s+(.*)$/.exec(line);
      if (li) {
        flushPara();
        var want = /^\d/.test(li[2]) ? 'ol' : 'ul';
        if (listType !== want) { flushList(); html.push('<' + want + '>'); listType = want; }
        html.push('<li>' + inline(esc(li[3])) + '</li>');
        i++; continue;
      }
      if (!line.trim()) { flushAll(); i++; continue; }
      flushList();
      para.push(line.trim());
      i++;
    }
    if (codeBuf !== null) html.push('<pre><code>' + esc(codeBuf.join('\n')) + '</code></pre>');
    flushAll();
    return html.join('\n');
  }

  /* ---------------- templates (Notion-style, markdown-native) ---------------- */

  var TEMPLATES = [
    { id: 'study-plan', name: 'Study Plan', desc: 'A dated plan with goals, daily blocks, and a review checklist.',
      body: function () {
        return '# Study Plan — ' + new Date().toISOString().slice(0, 10) + '\n\n' +
          '## Goal\nWhat am I preparing for, and by when?\n\n' +
          '## Daily blocks\n- [ ] Session 1 — learn (new material)\n- [ ] Session 2 — practice (labs / drills)\n- [ ] Session 3 — review (notes + weak spots)\n\n' +
          '## This week\n- [ ] \n- [ ] \n- [ ] \n\n' +
          '## Concepts to connect\nLink ideas with [[wikilinks]] as they click.\n\n' +
          '## Review notes\nWhat is still fuzzy? What surprised me?\n';
      } },
    { id: 'interview-prep', name: 'Interview Prep', desc: 'Role brief, likely questions, STAR stories, day-of checklist.',
      body: function () {
        return '# Interview Prep\n\n## The role\nCompany, title, team, and what they actually do day to day.\n\n' +
          '## Likely questions\n- [ ] Tell me about yourself\n- [ ] My strongest technical topic\n- [ ] A hard problem I solved\n\n' +
          '## STAR stories\n**Situation** — \n**Task** — \n**Action** — \n**Result** — \n\n' +
          '## Questions I will ask them\n- \n- \n\n' +
          '## Day-of checklist\n- [ ] Route + arrival buffer\n- [ ] Printed resumes\n- [ ] Notebook + pen\n- [ ] Thank-you note drafted\n';
      } },
    { id: 'project-tracker', name: 'Project Tracker', desc: 'Scope, milestones, decisions, and open questions in one page.',
      body: function () {
        return '# Project\n\n## Scope\nWhat is being built, and what is explicitly out?\n\n' +
          '## Milestones\n- [ ] Milestone 1\n- [ ] Milestone 2\n- [ ] Milestone 3\n\n' +
          '## Decisions log\n| Date | Decision | Why |\n| --- | --- | --- |\n|  |  |  |\n\n' +
          '## Open questions\n- \n\n## Links\nConnect related notes with [[wikilinks]].\n';
      } }
  ];

  function createFromTemplate(id) {
    for (var i = 0; i < TEMPLATES.length; i++) {
      if (TEMPLATES[i].id === id) {
        return create({ title: TEMPLATES[i].name, body: TEMPLATES[i].body(), tags: ['template'],
          source: { type: 'template', ref: id } });
      }
    }
    return null;
  }

  /* ---------------- block helpers (Notion-style inserts, markdown-native) ---------------- */

  var BLOCKS = [
    { id: 'h2', label: 'Heading', snippet: '\n## ' },
    { id: 'checklist', label: 'Checklist', snippet: '\n- [ ] ' },
    { id: 'bullet', label: 'Bullet list', snippet: '\n- ' },
    { id: 'code', label: 'Code block', snippet: '\n```\n\n```\n' },
    { id: 'quote', label: 'Quote', snippet: '\n> ' },
    { id: 'divider', label: 'Divider', snippet: '\n---\n' },
    { id: 'table', label: 'Table', snippet: '\n| Column | Column |\n| --- | --- |\n|  |  |\n' },
    { id: 'link', label: 'Wikilink', snippet: '[[]]' }
  ];

  /* ---------------- lesson / chat capture ---------------- */

  function noteFromLesson(opts) {
    opts = opts || {};
    var title = String(opts.title || 'Lesson note');
    var existing = findByTitle(title + ' — notes');
    if (existing) return existing;
    var body = '# ' + title + ' — my notes\n\n';
    if (opts.ref) body += 'From: ' + opts.ref + '\n\n';
    if (opts.concepts && opts.concepts.length) {
      body += '## Key concepts\n';
      opts.concepts.slice(0, 8).forEach(function (c) { body += '- ' + String(c).replace(/\s+/g, ' ').slice(0, 220) + '\n'; });
      body += '\n';
    }
    body += '## What I understood\n\n## What is still fuzzy\n\n## Connect it\nLink related ideas with [[wikilinks]] — e.g. the concept this builds on.\n';
    return create({ title: title + ' — notes', body: body, tags: ['lesson'],
      source: { type: 'lesson', slug: opts.slug || '', ref: opts.ref || '' } });
  }

  function saveTextAsNote(title, text, source) {
    return create({ title: String(title || 'Saved from Noah').slice(0, 160),
      body: String(text || ''), tags: ['noah'], source: source || { type: 'chat' } });
  }

  /* ---------------- export ---------------- */

  function download(name, content) {
    try {
      var url = URL.createObjectURL(new Blob([content], { type: 'text/markdown;charset=utf-8' }));
      var a = document.createElement('a');
      a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 1200);
    } catch (e) {}
  }

  function exportNote(id) {
    var n = get(id); if (!n) return;
    download(n.title.replace(/[^\w\- ]+/g, '').trim().replace(/\s+/g, '-') + '.md', n.body);
  }

  function exportAll() {
    var d = load();
    var parts = d.notes.map(function (n) { return '<!-- note: ' + n.title + ' -->\n' + n.body; });
    download('interstitium-notes-export.md', parts.join('\n\n---\n\n'));
  }

  /* ---------------- editor modal ---------------- */

  var CSS = [
    '.iln-overlay{position:fixed;inset:0;background:rgba(3,5,9,.72);backdrop-filter:blur(4px);z-index:9990;display:flex;align-items:center;justify-content:center;padding:14px}',
    '.iln-modal{background:#0a0f1c;border:1px solid rgba(94,234,212,.25);border-radius:16px;width:min(1060px,100%);max-height:92vh;display:flex;flex-direction:column;color:#dbe4ee;font-family:system-ui,sans-serif;box-shadow:0 24px 80px rgba(0,0,0,.6)}',
    '.iln-head{display:flex;gap:10px;align-items:center;padding:14px 16px;border-bottom:1px solid rgba(255,255,255,.08)}',
    '.iln-head input{flex:1;background:#06080c;border:1px solid rgba(255,255,255,.14);border-radius:9px;color:#fff;font-size:16px;font-weight:700;padding:9px 12px;min-width:0}',
    '.iln-btn{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.16);color:#dbe4ee;border-radius:9px;padding:8px 13px;font-size:13px;cursor:pointer;white-space:nowrap}',
    '.iln-btn:hover{border-color:#5EEAD4}',
    '.iln-btn.primary{background:rgba(201,162,39,.22);border-color:#c9a227;color:#fff}',
    '.iln-btn.danger:hover{border-color:#ff3b5c;color:#ffb3c0}',
    '.iln-toolbar{display:flex;gap:6px;flex-wrap:wrap;padding:10px 16px;border-bottom:1px solid rgba(255,255,255,.06)}',
    '.iln-toolbar .iln-btn{padding:5px 10px;font-size:12px}',
    '.iln-toolbar span{font:600 10px "JetBrains Mono",monospace;color:#8b93a5;letter-spacing:.08em;align-self:center;margin-right:2px}',
    '.iln-split{display:grid;grid-template-columns:1fr 1fr;min-height:0;flex:1}',
    '@media (max-width:760px){.iln-split{grid-template-columns:1fr;overflow-y:auto}}',
    '.iln-edit{display:flex;flex-direction:column;border-right:1px solid rgba(255,255,255,.06)}',
    '.iln-edit textarea{flex:1;min-height:300px;background:#06080c;color:#e8eef5;border:0;resize:none;padding:14px 16px;font:13.5px/1.65 "JetBrains Mono",ui-monospace,monospace;outline:none}',
    '.iln-preview{padding:14px 18px;overflow-y:auto;font-size:14.5px;line-height:1.65;min-height:0}',
    '.iln-preview h1{font-size:22px;margin:.2em 0 .5em}.iln-preview h2{font-size:18px;margin:1em 0 .4em}.iln-preview h3{font-size:15.5px;margin:1em 0 .3em}',
    '.iln-preview code{background:rgba(255,255,255,.08);padding:1px 5px;border-radius:5px;font-size:.92em}',
    '.iln-preview pre{background:#04060a;border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:12px;overflow-x:auto}',
    '.iln-preview pre code{background:none;padding:0}',
    '.iln-preview blockquote{border-left:3px solid #c9a227;margin:10px 0;padding:2px 12px;color:#aeb9c9}',
    '.iln-preview a{color:#5EEAD4}',
    '.iln-wikilink{color:#4da6ff!important;text-decoration:none;border-bottom:1px dotted #4da6ff;cursor:pointer}',
    '.iln-wikilink.iln-unresolved{color:#ff8fab!important;border-bottom-color:#ff8fab}',
    '.iln-checks{list-style:none;padding-left:2px}.iln-checks li{margin:4px 0}',
    '.iln-tablewrap{overflow-x:auto}.iln-preview table{border-collapse:collapse;margin:10px 0}',
    '.iln-preview th,.iln-preview td{border:1px solid rgba(255,255,255,.16);padding:5px 10px;text-align:left}',
    '.iln-foot{padding:12px 16px;border-top:1px solid rgba(255,255,255,.08);display:flex;flex-direction:column;gap:8px}',
    '.iln-foot input{background:#06080c;border:1px solid rgba(255,255,255,.14);border-radius:9px;color:#fff;padding:8px 11px;font-size:13px;width:100%}',
    '.iln-backlinks{font-size:12.5px;color:#8b93a5}',
    '.iln-backlinks a{color:#4da6ff;cursor:pointer;text-decoration:none}',
    '.iln-meta{font:11px "JetBrains Mono",monospace;color:#8b93a5}'
  ].join('\n');

  var modal = null, currentId = null;

  function injectCSS() {
    if (typeof document === 'undefined' || document.getElementById('iln-css')) return;
    var st = document.createElement('style'); st.id = 'iln-css'; st.textContent = CSS;
    document.head.appendChild(st);
  }

  function buildModal() {
    injectCSS();
    var ov = document.createElement('div');
    ov.className = 'iln-overlay'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true');
    ov.innerHTML =
      '<div class="iln-modal">' +
        '<div class="iln-head">' +
          '<input type="text" id="iln-title" aria-label="Note title" placeholder="Note title">' +
          '<button type="button" class="iln-btn" id="iln-export">Export .md</button>' +
          '<button type="button" class="iln-btn danger" id="iln-delete">Delete</button>' +
          '<button type="button" class="iln-btn primary" id="iln-save">Save</button>' +
          '<button type="button" class="iln-btn" id="iln-close" aria-label="Close">✕</button>' +
        '</div>' +
        '<div class="iln-toolbar"><span>INSERT</span>' +
          BLOCKS.map(function (b) { return '<button type="button" class="iln-btn" data-iln-block="' + b.id + '">' + b.label + '</button>'; }).join('') +
        '</div>' +
        '<div class="iln-split">' +
          '<div class="iln-edit"><textarea id="iln-body" aria-label="Note body in Markdown" placeholder="Write in Markdown. Link ideas with [[double brackets]]."></textarea></div>' +
          '<div class="iln-preview" id="iln-preview"></div>' +
        '</div>' +
        '<div class="iln-foot">' +
          '<input type="text" id="iln-tags" aria-label="Tags, comma separated" placeholder="Tags, comma separated">' +
          '<div class="iln-backlinks" id="iln-backlinks"></div>' +
          '<div class="iln-meta" id="iln-meta"></div>' +
        '</div>' +
      '</div>';
    document.body.appendChild(ov);

    var ta = ov.querySelector('#iln-body'), pv = ov.querySelector('#iln-preview');
    function refreshPreview() { pv.innerHTML = renderMarkdown(ta.value); }
    ta.addEventListener('input', refreshPreview);
    ov.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 's') { e.preventDefault(); saveCurrent(); }
      if (e.key === 'Escape') closeEditor();
    });
    ov.addEventListener('click', function (e) {
      if (e.target === ov) closeEditor();
      var wl = e.target.closest ? e.target.closest('[data-iln-title]') : null;
      if (wl) { e.preventDefault(); openByTitle(wl.getAttribute('data-iln-title')); }
    });
    ov.querySelector('#iln-close').addEventListener('click', closeEditor);
    ov.querySelector('#iln-save').addEventListener('click', saveCurrent);
    ov.querySelector('#iln-export').addEventListener('click', function () { if (currentId) exportNote(currentId); });
    ov.querySelector('#iln-delete').addEventListener('click', function () {
      if (currentId && g.confirm('Delete this note? This cannot be undone.')) { remove(currentId); closeEditor(); }
    });
    ov.querySelectorAll('[data-iln-block]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var id = btn.getAttribute('data-iln-block');
        var snip = null;
        BLOCKS.forEach(function (b) { if (b.id === id) snip = b.snippet; });
        if (snip == null) return;
        var start = ta.selectionStart || ta.value.length, end = ta.selectionEnd || start;
        if (id === 'link') {
          var sel = ta.value.slice(start, end) || 'Note title';
          ta.setRangeText('[[' + sel + ']]', start, end, 'end');
        } else {
          ta.setRangeText(snip, start, end, 'end');
        }
        ta.focus(); refreshPreview();
      });
    });
    modal = ov;
    return ov;
  }

  function saveCurrent() {
    if (!modal || !currentId) return;
    var title = modal.querySelector('#iln-title').value;
    var body = modal.querySelector('#iln-body').value;
    var tags = modal.querySelector('#iln-tags').value.split(',').map(function (t) { return t.trim(); }).filter(Boolean);
    update(currentId, { title: title || 'Untitled note', body: body, tags: tags });
    fillBacklinks();
    var meta = modal.querySelector('#iln-meta');
    if (meta) meta.textContent = 'Saved ' + new Date().toLocaleTimeString();
  }

  function fillBacklinks() {
    if (!modal || !currentId) return;
    var n = get(currentId); if (!n) return;
    var bl = backlinks(n), out = outlinks(n);
    var box = modal.querySelector('#iln-backlinks');
    var parts = [];
    if (bl.length) parts.push('Linked from: ' + bl.map(function (b) {
      return '<a data-iln-title="' + esc(b.title) + '">' + esc(b.title) + '</a>';
    }).join(' · '));
    if (out.unresolved.length) parts.push('Unresolved links (click one in preview to create it): ' +
      out.unresolved.map(function (u) { return esc(u.title); }).join(', '));
    box.innerHTML = parts.join('<br>') || 'No backlinks yet — link this note from another note with [[' + esc(n.title) + ']].';
  }

  function openEditor(id) {
    if (typeof document === 'undefined') return null;
    var n = id ? get(id) : null;
    if (!n) n = create({ title: 'Untitled note', body: '' });
    currentId = n.id;
    if (!modal) buildModal();
    modal.style.display = 'flex';
    modal.querySelector('#iln-title').value = n.title;
    modal.querySelector('#iln-body').value = n.body;
    modal.querySelector('#iln-tags').value = (n.tags || []).join(', ');
    modal.querySelector('#iln-preview').innerHTML = renderMarkdown(n.body);
    modal.querySelector('#iln-meta').textContent = n.kind === 'map'
      ? 'Mind map note — edit the tree in My Notes → Mind Maps.'
      : 'Markdown · [[wikilinks]] connect notes · Ctrl/Cmd+S saves';
    fillBacklinks();
    setTimeout(function () { var t = modal.querySelector('#iln-title'); if (t) t.focus(); }, 30);
    return n;
  }

  function openByTitle(title) {
    var hit = findByTitle(title);
    if (hit) return openEditor(hit.id);
    var n = create({ title: title, body: '# ' + title + '\n\nNew note created from a [[wikilink]]. What is this concept, in your own words?\n' });
    return openEditor(n.id);
  }

  function closeEditor() {
    if (modal) { saveCurrent(); modal.style.display = 'none'; }
    currentId = null;
  }

  /* ---------------- seed ---------------- */

  function seedIfEmpty() {
    var d = load();
    if (d.notes.length) return;
    create({ title: 'Welcome to My Notes', tags: ['start-here'], source: { type: 'manual' },
      body: '# Welcome to My Notes\n\nThis is your personal vault — local-first, plain Markdown, yours.\n\n' +
        '## How it works\n- Write in **Markdown**\n- Connect ideas with [[double bracket links]] — try [[Knowledge Graph]]\n' +
        '- Every note shows **backlinks**: the notes that link to it\n- Ask Noah: *"What did I note about Kerberos?"*\n' +
        '- Press **Add note** inside any lesson to capture it here\n\n## Try it\n- [ ] Write your first note\n- [ ] Link it to another note\n- [ ] Open the Knowledge Graph in My Notes\n' });
    create({ title: 'Knowledge Graph', tags: ['start-here'], source: { type: 'manual' },
      body: '# Knowledge Graph\n\nYour notes and the concepts you are mastering, drawn as one living map in **My Notes → Graph**.\n\nMastered concepts glow gold. Things you are still learning stay blue. Click any node to jump in.\n\nLinked from [[Welcome to My Notes]].\n' });
  }

  /* ---------------- public API ---------------- */

  var api = {
    all: all, get: get, findByTitle: findByTitle, create: create, update: update, remove: remove,
    parseLinks: parseLinks, outlinks: outlinks, backlinks: backlinks, search: search,
    bookmarks: bookmarks, addBookmark: addBookmark, removeBookmark: removeBookmark,
    renderMarkdown: renderMarkdown, templates: TEMPLATES, createFromTemplate: createFromTemplate,
    blocks: BLOCKS, noteFromLesson: noteFromLesson, saveTextAsNote: saveTextAsNote,
    exportNote: exportNote, exportAll: exportAll,
    openEditor: openEditor, openByTitle: openByTitle, closeEditor: closeEditor,
    seedIfEmpty: seedIfEmpty, LS_KEY: LS_KEY, version: 1
  };
  g.ILNotes = api;

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', seedIfEmpty);
    else seedIfEmpty();
    /* global wikilink clicks inside any rendered note preview */
    document.addEventListener('click', function (e) {
      var t = e.target && e.target.closest ? e.target.closest('[data-iln-title]') : null;
      if (t && !e.target.closest('.iln-overlay')) { e.preventDefault(); openByTitle(t.getAttribute('data-iln-title')); }
    });
  }
})(typeof window !== 'undefined' ? window : this);
