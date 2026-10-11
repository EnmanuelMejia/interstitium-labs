/* Noah/Genesis Library — the documents, certificates, and files home
 * inside /noah/ (2026-10-11).
 *
 * Surface: distilled from the Muse app's Library — the user's documents,
 * certificates, and files in one searchable place; every item can be
 * opened, pinned so it shows first, and attached to the conversation
 * via Discuss (ctx.discuss). A separate views shell mounts this module
 * through window.ILLibraryView = { mount(el, ctx), unmount() }, where
 * ctx = { tutor(): 'Noah'|'Genesis', discuss(text), go(viewName) }.
 *
 * Aggregation sources (client-side aggregation is the established
 * pattern here — the Settings "Files & documents" section does the
 * same; this Library is the full home those links point at):
 *   - Certificates:      GET /api/certificates (account session)
 *   - Notes & documents: localStorage "il-notes-v1" (.notes array)
 *   - Mock interviews:   localStorage "il-mock-interviews-v1"
 *   - More of your files: canonical link rows (/pdf-library/,
 *     /library/, /jobs/, /my-notes/) + GET /api/account/export
 * Data is fetched once per mount session and cached; the Refresh
 * button re-runs the whole aggregation. One section failing never
 * blanks the others — each section carries its own loading, empty,
 * sign-in, and error states.
 *
 * Pins: localStorage "il-library-pins-v1" — a JSON array of unified
 * item keys; pinned items render again in the "📌 Pinned" section
 * shown first. Pinning is client-side organization only.
 *
 * Residual (documented, deliberate): there is NO upload vault and no
 * file editor here. No object storage exists on this platform, so
 * uploads are a documented residual — files arrive through the
 * surfaces that create them (the notes app at /my-notes/ is the
 * canonical notes editor; certificates are issued by courses), and
 * this Library aggregates, opens, pins, downloads, and discusses
 * them. Never build a second editor or a fake upload store here. */
(function () {
  'use strict';
  if (window.ILLibraryView) return;
  if (!document.getElementById('newChatBtn')) return; /* /noah/ only */

  var PINS_KEY = 'il-library-pins-v1';
  var NOTES_KEY = 'il-notes-v1';
  var MOCK_KEY = 'il-mock-interviews-v1';
  var CERTS_API = '/api/certificates';
  var EXPORT_API = '/api/account/export';

  var state = {
    el: null, ctx: null, query: '',
    pins: loadPins(),
    certs: { status: 'idle', items: [] }, /* idle|loading|ok|unauth|error */
    artifacts: { status: 'ok', items: [] }, /* from window.ILArtifacts (noah-artifacts.js) */
    notes: { status: 'idle', items: [] }, /* idle|ok|error */
    mocks: { status: 'idle', item: null, count: 0 }, /* idle|ok|error */
    signedIn: null, /* null=unknown, true/false once certificates answer */
    aggregated: false
  };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function tutorName() {
    try {
      if (state.ctx && typeof state.ctx.tutor === 'function') {
        return state.ctx.tutor() === 'Genesis' ? 'Genesis' : 'Noah';
      }
    } catch (e) {}
    return 'Noah';
  }
  function fmtDate(v) {
    if (!v) return '';
    var d = new Date(v);
    if (isNaN(d.getTime())) return String(v).slice(0, 10);
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
  }
  function dateVal(v) {
    if (!v) return 0;
    var t = new Date(v).getTime();
    return isNaN(t) ? 0 : t;
  }
  function safeFilename(name, fallback) {
    var s = String(name == null ? '' : name).replace(/[^\w\- ]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '');
    return s || fallback || 'download';
  }

  /* ---------------- Pins ---------------- */
  function loadPins() {
    try {
      var arr = JSON.parse(localStorage.getItem(PINS_KEY) || '[]');
      var out = [];
      if (arr && typeof arr.length === 'number') {
        for (var i = 0; i < arr.length; i++) if (typeof arr[i] === 'string') out.push(arr[i]);
      }
      return out;
    } catch (e) { return []; }
  }
  function savePins() {
    try { localStorage.setItem(PINS_KEY, JSON.stringify(state.pins)); } catch (e) {}
  }
  function isPinned(key) { return state.pins.indexOf(key) !== -1; }
  function togglePin(key) {
    var i = state.pins.indexOf(key);
    if (i === -1) state.pins.push(key); else state.pins.splice(i, 1);
    savePins();
    renderSections();
  }

  /* ---------------- CSS ---------------- */
  var css = [
    '.ill-root{color:var(--text,#e8e4da)}',
    '.ill-head{display:flex;align-items:center;gap:.6rem;margin-bottom:.4rem}',
    '.ill-head h2{font-size:1.15rem;margin:0;flex:1}',
    '.ill-intro{color:var(--muted2,#9a958a);font-size:.88rem;line-height:1.5;margin:.2rem 0 .8rem}',
    '.ill-refresh{background:none;border:1px solid rgba(255,255,255,.15);color:inherit;border-radius:8px;padding:.35rem .7rem;cursor:pointer;font:inherit;font-size:.85rem}',
    '.ill-refresh:hover{border-color:rgba(201,162,39,.6)}',
    '.ill-search{margin-bottom:.6rem}',
    '.ill-search input{width:100%;box-sizing:border-box;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);',
    'border-radius:10px;color:inherit;padding:.6rem .75rem;font:inherit;font-size:.95rem}',
    '.ill-search input:focus{outline:none;border-color:rgba(201,162,39,.65)}',
    '.ill-status{font-size:.85rem;min-height:1.1em;margin:.2rem 0 .4rem;color:#e6c95c}',
    '.ill-sec{padding:.9rem 0 .3rem;border-bottom:1px solid rgba(255,255,255,.06)}',
    '.ill-sec:last-child{border-bottom:none}',
    '.ill-sec h3{font-size:.98rem;margin:0 0 .55rem;display:flex;align-items:center;gap:.45rem}',
    '.ill-note{color:var(--muted2,#9a958a);font-size:.88rem;line-height:1.5;margin:.35rem 0}',
    '.ill-note.ill-err{color:#e08a8a}',
    '.ill-card{border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:.75rem .9rem;margin-bottom:.7rem;background:rgba(255,255,255,.03)}',
    '.ill-card-title{font-size:.95rem;font-weight:600;display:flex;gap:.5rem;align-items:baseline;word-break:break-word}',
    '.ill-sub{color:var(--muted2,#9a958a);font-size:.82rem;line-height:1.45;margin-top:.25rem;word-break:break-word}',
    '.ill-meta{color:var(--muted2,#9a958a);font-size:.75rem;margin-top:.3rem}',
    '.ill-actions{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:.6rem}',
    '.ill-btn{display:inline-block;background:rgba(201,162,39,.14);border:1px solid rgba(201,162,39,.45);color:inherit;',
    'border-radius:8px;padding:.35rem .65rem;font:inherit;font-size:.8rem;cursor:pointer;text-decoration:none}',
    '.ill-btn:hover{background:rgba(201,162,39,.24)}',
    '.ill-btn.primary{background:#c9a227;color:#0a0e1a;border-color:#c9a227;font-weight:700}',
    '.ill-btn.ghost{background:none;border-color:rgba(255,255,255,.18)}',
    '.ill-btn:disabled{opacity:.55;cursor:wait}',
    '.ill-row{display:flex;align-items:center;gap:.6rem;padding:.55rem 0;border-top:1px solid rgba(255,255,255,.05)}',
    '.ill-row:first-of-type{border-top:none}',
    '.ill-row .ill-grow{flex:1;min-width:0}',
    '.ill-row .ill-row-title{font-size:.92rem}',
    '.ill-foot{margin-top:.6rem}'
  ].join('\n');
  if (!document.getElementById('il-library-style')) {
    var style = document.createElement('style');
    style.id = 'il-library-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  /* ---------------- Downloads ---------------- */
  function setStatus(msg) {
    if (!state.el) return;
    var el = state.el.querySelector('.ill-status');
    if (el) el.textContent = msg || '';
  }
  function triggerDownload(blob, filename) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    if (a.parentNode) a.parentNode.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 500);
  }
  function downloadUrl(url, filename) {
    return fetch(url, { credentials: 'same-origin', headers: { accept: 'application/json' } })
      .then(function (res) {
        if (!res.ok) throw new Error('http_' + res.status);
        return res.blob();
      })
      .then(function (blob) {
        triggerDownload(blob, filename);
        setStatus('✓ Download saved: ' + filename);
      })
      .catch(function () { setStatus('Couldn\'t download that just now.'); });
  }

  /* ---------------- Aggregation: certificates ---------------- */
  function certItem(c, idx) {
    var id = c.id != null ? String(c.id) : (c.cert_id != null ? String(c.cert_id) : '');
    var title = c.course_title || c.title || c.course || c.name || 'Certificate';
    var sub = '';
    if (c.course && String(c.course) !== String(title)) sub = String(c.course);
    else if (c.issuer) sub = String(c.issuer);
    else sub = 'Verifiable credential (W3C VC)';
    var item = {
      key: 'cert:' + (id || ('idx' + idx)),
      kind: 'cert', icon: '🎓',
      title: String(title), sub: sub,
      date: c.issued_at || c.created_at || '',
      openUrl: id ? '/api/certificates/credential?id=' + encodeURIComponent(id) : '',
      verifyUrl: id ? '/api/certificates/verify?id=' + encodeURIComponent(id) : '',
      openNewTab: true,
      discussText: 'Let\'s talk about my certificate: ' + String(title)
    };
    if (id) {
      var credUrl = item.openUrl;
      var fname = safeFilename(title, 'certificate') + '.json';
      item.downloadFn = function () { return downloadUrl(credUrl, fname); };
    }
    return item;
  }
  function loadCertificates() {
    state.certs.status = 'loading';
    return fetch(CERTS_API, { credentials: 'same-origin', headers: { accept: 'application/json' } })
      .then(function (res) {
        if (res.status === 401) {
          state.certs = { status: 'unauth', items: [] };
          state.signedIn = false;
          return null;
        }
        return res.json().catch(function () { return null; }).then(function (j) {
          if (!res.ok || !j || j.ok === false) {
            state.certs = { status: 'error', items: [] };
            return;
          }
          var list = j.certificates || j.certs || [];
          var items = [];
          for (var i = 0; i < list.length; i++) if (list[i] && typeof list[i] === 'object') items.push(certItem(list[i], i));
          state.certs = { status: 'ok', items: items };
          state.signedIn = true;
        });
      })
      .catch(function () {
        if (state.certs.status === 'loading') state.certs = { status: 'error', items: [] };
      });
  }

  /* ---------------- Aggregation: notes ---------------- */
  function noteItem(n, idx) {
    var body = n.body != null ? String(n.body) : (n.content != null ? String(n.content) : (n.text != null ? String(n.text) : ''));
    var lines = body.split(/\r?\n/);
    var first = '', rest = '', i, line;
    for (i = 0; i < lines.length; i++) { line = lines[i].replace(/^\s+|\s+$/g, ''); if (line) { first = line; break; } }
    var title = n.title ? String(n.title) : (first || 'Untitled note');
    if (n.title) rest = body.replace(/^\s+|\s+$/g, '');
    else if (first) {
      var pos = body.indexOf(first);
      rest = (pos === -1 ? '' : body.slice(pos + first.length)).replace(/^\s+|\s+$/g, '');
    }
    var snippet = rest ? rest.slice(0, 120) : '';
    return {
      key: 'note:' + (n.id != null ? String(n.id) : ('idx' + idx)),
      kind: 'note', icon: '📝',
      title: title,
      sub: snippet,
      date: n.updated || n.updated_at || n.created || n.created_at || '',
      openUrl: '/my-notes/',
      discussText: 'Let\'s talk about my note: ' + title + (snippet ? ' — ' + snippet : '')
    };
  }
  function readNotes() {
    var raw;
    try { raw = localStorage.getItem(NOTES_KEY); } catch (e) { state.notes = { status: 'error', items: [] }; return; }
    if (!raw) { state.notes = { status: 'ok', items: [] }; return; }
    var parsed;
    try { parsed = JSON.parse(raw); } catch (e) { state.notes = { status: 'error', items: [] }; return; }
    var list = null, i;
    if (parsed && typeof parsed.length === 'number' && typeof parsed !== 'string') list = parsed;
    else if (parsed && parsed.notes && typeof parsed.notes.length === 'number') list = parsed.notes;
    else if (parsed && typeof parsed === 'object') {
      list = [];
      for (var k in parsed) if (Object.prototype.hasOwnProperty.call(parsed, k) && parsed[k] && typeof parsed[k] === 'object') list.push(parsed[k]);
    }
    var items = [];
    if (list) for (i = 0; i < list.length; i++) if (list[i] && typeof list[i] === 'object') items.push(noteItem(list[i], i));
    items.sort(function (a, b) { return dateVal(b.date) - dateVal(a.date); });
    state.notes = { status: 'ok', items: items };
  }

  /* ---------------- Aggregation: mock interviews ---------------- */
  function readMocks() {
    var raw;
    try { raw = localStorage.getItem(MOCK_KEY); } catch (e) { state.mocks = { status: 'error', item: null, count: 0 }; return; }
    if (!raw) { state.mocks = { status: 'ok', item: null, count: 0 }; return; }
    var parsed;
    try { parsed = JSON.parse(raw); } catch (e) { state.mocks = { status: 'error', item: null, count: 0 }; return; }
    var list = null;
    if (parsed && typeof parsed.length === 'number' && typeof parsed !== 'string') list = parsed;
    else if (parsed && typeof parsed === 'object') {
      var cand = parsed.sessions || parsed.history || parsed.interviews || parsed.items;
      if (cand && typeof cand.length === 'number') list = cand;
      else {
        list = [];
        for (var k in parsed) if (Object.prototype.hasOwnProperty.call(parsed, k) && parsed[k] && typeof parsed[k] === 'object') list.push(parsed[k]);
      }
    }
    if (!list || !list.length) { state.mocks = { status: 'ok', item: null, count: 0 }; return; }
    var latest = '', latestVal = 0, i, s, dv;
    for (i = 0; i < list.length; i++) {
      s = list[i] || {};
      var d = s.ended_at || s.date || s.created_at || s.created || s.updated_at || s.ts || s.timestamp || s.at || '';
      dv = dateVal(d);
      if (d && (dv >= latestVal || !latest)) { latest = d; latestVal = dv; }
    }
    var item = {
      key: 'mock:summary',
      kind: 'mock', icon: '🎙',
      title: 'Mock interviews',
      sub: list.length + (list.length === 1 ? ' session' : ' sessions') + ' saved on this device',
      date: latest,
      openUrl: '',
      discussText: 'Let\'s talk about my mock interviews — ' + list.length +
        (list.length === 1 ? ' session' : ' sessions') + (latest ? ', most recent ' + fmtDate(latest) : '') + '.'
    };
    state.mocks = { status: 'ok', item: item, count: list.length };
  }

  /* ---------------- Artifacts (built by the twins) ---------------- */
  function artifactItem(a) {
    var meta = (window.ILArtifacts && window.ILArtifacts.kinds[a.kind]) || { icon: '🛠', label: 'Artifact' };
    return {
      key: 'art:' + a.id,
      kind: 'artifact',
      icon: meta.icon,
      title: a.title || 'Untitled',
      sub: meta.label + (a.content ? ' · ' + String(a.content).replace(/\s+/g, ' ').slice(0, 90) : ''),
      date: a.updated_at || a.created_at,
      discussText: 'Let\'s talk about my artifact "' + (a.title || 'Untitled') + '" (' + meta.label + ').',
      downloadFn: function () { if (window.ILArtifacts) window.ILArtifacts.exportItem(a); },
      openFn: function () { if (window.ILArtifacts) window.ILArtifacts.openPreview(a); },
      editId: a.id
    };
  }
  function readArtifacts() {
    state.artifacts.items = [];
    if (!window.ILArtifacts) return;
    try {
      state.artifacts.items = window.ILArtifacts.list().map(artifactItem);
    } catch (e) { state.artifacts.items = []; }
  }

  /* ---------------- Aggregation driver ---------------- */
  function aggregate(force) {
    state.pins = loadPins();
    readArtifacts();
    readNotes();
    readMocks();
    if (state.aggregated && !force) { renderSections(); return; }
    state.aggregated = true;
    renderSections(); /* local sections land immediately; certificates stream in */
    loadCertificates().then(renderSections);
  }
  function allItems() {
    var out = [], i;
    for (i = 0; i < state.certs.items.length; i++) out.push(state.certs.items[i]);
    for (i = 0; i < state.artifacts.items.length; i++) out.push(state.artifacts.items[i]);
    for (i = 0; i < state.notes.items.length; i++) out.push(state.notes.items[i]);
    if (state.mocks.item) out.push(state.mocks.item);
    return out;
  }
  function itemByKey(key) {
    var items = allItems();
    for (var i = 0; i < items.length; i++) if (items[i].key === key) return items[i];
    return null;
  }
  function matches(item) {
    if (!state.query) return true;
    var q = state.query.toLowerCase();
    return (item.title && item.title.toLowerCase().indexOf(q) !== -1) ||
      (item.sub && item.sub.toLowerCase().indexOf(q) !== -1);
  }
  function anyMatch(items) {
    for (var i = 0; i < items.length; i++) if (matches(items[i])) return true;
    return false;
  }

  /* ---------------- Rendering ---------------- */
  function cardHtml(item) {
    var h = '<article class="ill-card" data-ill-key="' + esc(item.key) + '">';
    h += '<div class="ill-card-title"><span aria-hidden="true">' + esc(item.icon) + '</span><span>' + esc(item.title) + '</span></div>';
    if (item.sub) h += '<div class="ill-sub">' + esc(item.sub) + '</div>';
    if (item.date) h += '<div class="ill-meta">' + esc(fmtDate(item.date)) + '</div>';
    h += '<div class="ill-actions">';
    if (item.kind === 'mock') {
      h += '<button type="button" class="ill-btn primary" data-ill-open="' + esc(item.key) + '">Open</button>';
    } else if (item.openUrl) {
      h += '<a class="ill-btn primary" href="' + esc(item.openUrl) + '"' +
        (item.openNewTab ? ' target="_blank" rel="noopener"' : '') + '>Open</a>';
    }
    if (item.openFn) {
      h += '<button type="button" class="ill-btn primary" data-ill-openfn="' + esc(item.key) + '">Preview</button>';
    }
    if (item.editId) {
      h += '<button type="button" class="ill-btn ghost" data-ill-edit="' + esc(item.editId) + '">Edit</button>';
    }
    if (item.verifyUrl) {
      h += '<a class="ill-btn ghost" href="' + esc(item.verifyUrl) + '" target="_blank" rel="noopener">Verify</a>';
    }
    if (item.downloadFn) {
      h += '<button type="button" class="ill-btn ghost" data-ill-download="' + esc(item.key) + '">Download</button>';
    }
    h += '<button type="button" class="ill-btn ghost" data-ill-pin="' + esc(item.key) + '">' +
      (isPinned(item.key) ? '📌 Unpin' : '📌 Pin') + '</button>';
    h += '<button type="button" class="ill-btn" data-ill-discuss="' + esc(item.key) + '">Discuss</button>';
    h += '</div></article>';
    return h;
  }
  function cardsHtml(items) {
    var h = '';
    for (var i = 0; i < items.length; i++) if (matches(items[i])) h += cardHtml(items[i]);
    return h;
  }
  function secHtml(name, inner) {
    return '<section class="ill-sec" data-ill-sec="' + name + '"><h3>' + inner.head + '</h3>' + inner.body + '</section>';
  }

  function pinnedHtml() {
    var items = allItems(), pinned = [], i;
    for (i = 0; i < items.length; i++) if (isPinned(items[i].key) && matches(items[i])) pinned.push(items[i]);
    if (!pinned.length) return ''; /* empty state hides the section */
    var h = '';
    for (i = 0; i < pinned.length; i++) h += cardHtml(pinned[i]);
    return secHtml('pinned', { head: '📌 Pinned', body: h });
  }
  function certsHtml() {
    var body;
    if (state.certs.status === 'idle' || state.certs.status === 'loading') {
      body = '<p class="ill-note">Loading certificates…</p>';
    } else if (state.certs.status === 'unauth') {
      body = '<p class="ill-note">Sign in to see your certificates — they follow your account, not this browser.</p>' +
        '<p><a class="ill-btn" href="/account/">Sign in</a></p>';
    } else if (state.certs.status === 'error') {
      body = '<p class="ill-note ill-err">Couldn\'t load certificates just now.</p>';
    } else if (!state.certs.items.length) {
      body = '<p class="ill-note">No certificates yet — finish a course and your verifiable certificate lands here.</p>';
    } else if (!anyMatch(state.certs.items)) {
      body = '<p class="ill-note">No certificates match your search.</p>';
    } else {
      body = cardsHtml(state.certs.items);
    }
    return secHtml('certs', { head: '🎓 Certificates', body: body });
  }
  function artifactsHtml() {
    var body;
    if (!window.ILArtifacts) {
      body = '<p class="ill-note">The artifact builder is still loading — reopen Library in a moment.</p>';
    } else if (!state.artifacts.items.length) {
      body = '<p class="ill-note">Nothing built yet. Ask ' + esc(tutorName()) + ' in chat to build you a study guide, ' +
        'a web page, a budget sheet — long replies can be saved as artifacts — or start one yourself below.</p>';
    } else if (!anyMatch(state.artifacts.items)) {
      body = '<p class="ill-note">No artifacts match your search.</p>';
    } else {
      body = cardsHtml(state.artifacts.items);
    }
    body += '<p class="ill-foot"><button type="button" class="ill-btn" data-ill-build="1">＋ Build something</button></p>';
    return secHtml('artifacts', { head: '🛠 Artifacts', body: body });
  }
  function notesHtml() {
    var body;
    if (state.notes.status === 'idle') body = '<p class="ill-note">Loading notes…</p>';
    else if (state.notes.status === 'error') body = '<p class="ill-note ill-err">Couldn\'t load notes just now.</p>';
    else if (!state.notes.items.length) body = '<p class="ill-note">No notes yet — start one in your notes workspace and it shows up here.</p>';
    else if (!anyMatch(state.notes.items)) body = '<p class="ill-note">No notes match your search.</p>';
    else body = cardsHtml(state.notes.items);
    body += '<p class="ill-foot"><a class="ill-btn" href="/my-notes/">＋ New note</a></p>';
    return secHtml('notes', { head: '📝 Notes &amp; documents', body: body });
  }
  function mocksHtml() {
    var body;
    if (state.mocks.status === 'idle') body = '<p class="ill-note">Loading mock interviews…</p>';
    else if (state.mocks.status === 'error') body = '<p class="ill-note ill-err">Couldn\'t load mock interviews just now.</p>';
    else if (!state.mocks.item) {
      body = '<p class="ill-note">No mock interviews yet — start one from the 🎙 button in chat.</p>';
    } else if (!matches(state.mocks.item)) {
      body = '<p class="ill-note">No mock interviews match your search.</p>';
    } else {
      body = cardHtml(state.mocks.item) +
        '<p class="ill-note">Interviews start from the 🎙 button in chat — Open takes you there.</p>';
    }
    return secHtml('mocks', { head: '🎙 Mock interviews', body: body });
  }
  function moreHtml() {
    var exportAction;
    if (state.signedIn === false) {
      exportAction = '<a class="ill-btn ghost" href="/account/">Sign in</a>';
    } else {
      exportAction = '<button type="button" class="ill-btn ghost" data-ill-export="1">Download</button>';
    }
    function row(icon, title, sub, action) {
      return '<div class="ill-row"><div class="ill-grow"><div class="ill-row-title">' + icon + ' ' + esc(title) + '</div>' +
        '<div class="ill-sub">' + esc(sub) + '</div></div>' + action + '</div>';
    }
    function linkRow(icon, title, sub, url) {
      return row(icon, title, sub, '<a class="ill-btn ghost" href="' + esc(url) + '">Open</a>');
    }
    var body =
      row('⬇', 'Download your data export', 'A JSON copy of everything your account holds', exportAction) +
      linkRow('📕', 'PDF library', 'Reference books and study PDFs', '/pdf-library/') +
      linkRow('📚', 'Course library', 'All your courses, paths, and study collections', '/library/') +
      linkRow('💼', 'Job documents & tracker', 'Resumes, cover letters, and your application tracker', '/jobs/') +
      linkRow('📝', 'Your notes workspace', 'Your notes vault, synced to your account', '/my-notes/');
    /* Search filters every section: hide rows that do not match. */
    if (state.query) {
      var tmp = document.createElement('div');
      tmp.innerHTML = body;
      var rows = tmp.querySelectorAll('.ill-row'), kept = '';
      for (var i = 0; i < rows.length; i++) {
        if (rows[i].textContent.toLowerCase().indexOf(state.query.toLowerCase()) !== -1) kept += rows[i].outerHTML;
      }
      body = kept || '<p class="ill-note">Nothing here matches your search.</p>';
    }
    return secHtml('more', { head: '🧰 More of your files', body: body });
  }

  function bindSectionActions(container) {
    var i, els;
    els = container.querySelectorAll('[data-ill-pin]');
    for (i = 0; i < els.length; i++) (function (b) {
      b.addEventListener('click', function () { togglePin(b.getAttribute('data-ill-pin')); });
    })(els[i]);
    els = container.querySelectorAll('[data-ill-discuss]');
    for (i = 0; i < els.length; i++) (function (b) {
      b.addEventListener('click', function () {
        var item = itemByKey(b.getAttribute('data-ill-discuss'));
        if (item && state.ctx && typeof state.ctx.discuss === 'function') {
          try { state.ctx.discuss(item.discussText); } catch (e) {}
        }
      });
    })(els[i]);
    els = container.querySelectorAll('[data-ill-download]');
    for (i = 0; i < els.length; i++) (function (b) {
      b.addEventListener('click', function () {
        var item = itemByKey(b.getAttribute('data-ill-download'));
        if (item && item.downloadFn) { b.disabled = true; item.downloadFn(); b.disabled = false; }
      });
    })(els[i]);
    els = container.querySelectorAll('[data-ill-open]');
    for (i = 0; i < els.length; i++) (function (b) {
      b.addEventListener('click', function () {
        if (state.ctx && typeof state.ctx.go === 'function') {
          try { state.ctx.go('chat'); } catch (e) {}
          setStatus('Interviews start from the 🎙 button in chat.');
        } else {
          setStatus('Interviews start from the 🎙 button in chat.');
        }
      });
    })(els[i]);
    els = container.querySelectorAll('[data-ill-export]');
    for (i = 0; i < els.length; i++) (function (b) {
      b.addEventListener('click', function () {
        b.disabled = true;
        downloadUrl(EXPORT_API, 'interstitium-data-export.json');
        b.disabled = false;
      });
    })(els[i]);
    els = container.querySelectorAll('[data-ill-openfn]');
    for (i = 0; i < els.length; i++) (function (b) {
      b.addEventListener('click', function () {
        var item = itemByKey(b.getAttribute('data-ill-openfn'));
        if (item && item.openFn) item.openFn();
      });
    })(els[i]);
    els = container.querySelectorAll('[data-ill-edit]');
    for (i = 0; i < els.length; i++) (function (b) {
      b.addEventListener('click', function () {
        if (window.ILArtifacts && !window.ILArtifacts.openBuilder(b.getAttribute('data-ill-edit'))) {
          setStatus('The builder opens in the workspace pane — it is still loading.');
        }
      });
    })(els[i]);
    els = container.querySelectorAll('[data-ill-build]');
    for (i = 0; i < els.length; i++) (function (b) {
      b.addEventListener('click', function () {
        if (window.ILArtifacts && !window.ILArtifacts.openBuilder(null)) {
          setStatus('The builder opens in the workspace pane — it is still loading.');
        }
      });
    })(els[i]);
  }

  function renderSections() {
    if (!state.el) return;
    var host = state.el.querySelector('[data-ill-sections]');
    if (!host) return;
    host.innerHTML = pinnedHtml() + artifactsHtml() + certsHtml() + notesHtml() + mocksHtml() + moreHtml();
    bindSectionActions(host);
  }

  /* ---------------- Mount / unmount ---------------- */
  function mount(el, ctx) {
    if (!el) return;
    state.el = el;
    state.ctx = ctx || {};
    state.pins = loadPins();
    el.innerHTML =
      '<div class="ill-root">' +
      '<div class="ill-head"><h2>📚 Library</h2>' +
      '<button type="button" class="ill-refresh" data-ill-refresh="1">Refresh</button></div>' +
      '<p class="ill-intro">Your documents, certificates, and files in one place. Open anything, ' +
      'pin what matters, or hand it to ' + esc(tutorName()) + ' with Discuss.</p>' +
      '<div class="ill-search"><input type="search" data-ill-search="1" placeholder="Search your library…" aria-label="Search your library"></div>' +
      '<p class="ill-status" role="status" aria-live="polite"></p>' +
      '<div data-ill-sections="1"></div>' +
      '</div>';
    var input = el.querySelector('[data-ill-search]');
    if (input) {
      input.value = state.query || '';
      input.addEventListener('input', function () {
        state.query = input.value.replace(/^\s+|\s+$/g, '');
        renderSections();
      });
    }
    var refreshBtn = el.querySelector('[data-ill-refresh]');
    if (refreshBtn) refreshBtn.addEventListener('click', function () { aggregate(true); });
    aggregate(false);
  }
  function unmount() {
    if (state.el) state.el.innerHTML = '';
    state.el = null;
    state.ctx = null;
  }

  document.addEventListener('il:artifacts-changed', function () {
    if (state.el) { readArtifacts(); renderSections(); }
  });

  window.ILLibraryView = { mount: mount, unmount: unmount };
})();
