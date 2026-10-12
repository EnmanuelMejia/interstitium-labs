/* Noah/Genesis Split — the split-screen workspace pane for /noah/
 * (Phase 2 full-application fold-in, 2026-10-11).
 *
 * Purpose: let the learner keep the chat with Noah/Genesis open on one
 * side and the thing they are talking about on the other — a lesson, a
 * lab, a library document, an artifact, or one of the tab views (Feed /
 * Ideas / Goals / Library) — without ever losing the conversation.
 * On desktop this is a true split view (the chat column reflows beside
 * the pane); on mobile the two stack and a visible segmented switcher
 * moves between them.
 *
 * Public API:
 *   window.ILSplit = { open, close, toggle, isOpen, home, mountHtml, bodyEl }
 *
 *   ILSplit.open(spec) — show the pane with content:
 *     spec = { kind, title, html, src, text, view }
 *       kind 'html' : sandboxed iframe (sandbox="allow-scripts") whose
 *                     srcdoc renders spec.html — for artifacts and other
 *                     generated markup that must NOT run with page
 *                     privileges.
 *       kind 'url'  : iframe with src = spec.src — for same-origin
 *                     platform pages (lessons, labs, library docs).
 *       kind 'text' : <pre> holding spec.text, escaped — for raw notes,
 *                     transcripts, code, and other plain text.
 *       kind 'view' : mount a views-shell module into the pane body:
 *                     spec.view 'feed'    -> window.ILFeedView.mount
 *                               'ideas'   -> window.ILIdeasView.mount
 *                               'goals'   -> window.ILGoals.mountView
 *                               'library' -> window.ILLibraryView.mount
 *                     Each is called with a ctx { tutor, discuss, go }:
 *                     discuss/go delegate to window.ILViews.ctx when
 *                     the views shell is present; otherwise local
 *                     fallbacks are built here (tutor is read from the
 *                     localStorage 'il-noah-profile' profile, discuss
 *                     pre-fills the composer, go opens the view in the
 *                     pane or returns to chat). Calling open() with no
 *                     spec (or home()) shows the Home launcher.
 *   ILSplit.close()    — hide the pane (content is kept, not destroyed).
 *   ILSplit.toggle()   — hide if open; otherwise reopen the last spec,
 *                        or the Home launcher if nothing was opened yet.
 *   ILSplit.isOpen()   — boolean.
 *   ILSplit.home()     — open the pane on the Home launcher.
 *   ILSplit.mountHtml(htmlString, title)
 *                      — the LIVE DOM channel, for first-party app
 *                        modules (e.g. the artifacts builder) that need
 *                        real elements in the pane: an editor with
 *                        inputs and buttons cannot live inside the
 *                        sandboxed iframe used by kind 'html'. Opens the
 *                        pane (same responsive behaviour), sets the pane
 *                        title, sets the pane body's innerHTML to
 *                        htmlString, and RETURNS the pane body element
 *                        so the caller can wire its own events. Callers
 *                        pass their own static markup with values they
 *                        have already escaped — this channel is for the
 *                        app's own trusted markup only, never for model
 *                        output or user-supplied HTML.
 *   ILSplit.bodyEl()   — the current pane body element, or null.
 *
 * The "let me show you" path: the twin (or any other module) opens the
 * pane programmatically by simply calling ILSplit.open(...) — e.g.
 * Noah answers a question and calls open({ kind: 'url', src: <lesson>,
 * title: <lesson title> }) so the lesson appears beside the chat while
 * the explanation stays in the thread. No user click is required and
 * no new API is needed; open() IS the programmatic surface.
 *
 * Chat link interception (always-on): a delegated click handler on
 * #threadInner sends same-origin links whose path starts with
 * /university/, /library/, /my-notes/, /pdf-library/, /topics/, or
 * /bootcamps/ into the pane as kind 'url' instead of navigating away
 * from the conversation (preventDefault). Every other link — external,
 * off-list, target=_blank, modified-click — is left untouched.
 *
 * Responsive behaviour:
 *   Desktop (min-width: 1100px): the pane is position:fixed on the
 *     right, default width min(52vw, 760px). The user can drag its left
 *     edge (380–900px clamp); the chosen width persists in localStorage
 *     'il-split-w'. While open, <body> carries the class 'il-split-on'
 *     and .muse-app gets a margin-right equal to the pane width so the
 *     chat stays fully visible beside it (transition .25s). The pane
 *     is persistent on desktop — Escape does not close it there.
 *   Mobile (< 1100px): the pane covers the full screen
 *     (position:fixed; inset:0, z-index above the chat) and carries a
 *     visible switcher header — segmented [💬 Chat] [◫ Workspace]:
 *     Chat hides the pane, Workspace shows it (it is the active segment
 *     while the pane is up; the ◫ button in the chat header brings the
 *     pane back). Escape closes the pane on mobile only.
 *
 * Governance: the pane only DISPLAYS. It renders lessons, documents,
 * artifacts, and view modules; it takes no outward action of its own.
 * Anything irreversible that a mounted surface can start (sending,
 * buying, booking, deleting) still goes through that surface's own
 * draft -> human-approve flow — opening something in the pane is never
 * an approval.
 */
(function () {
  'use strict';
  if (window.ILSplit) return;
  if (!document.getElementById('newChatBtn')) return; /* /noah/ only */

  var WIDTH_KEY = 'il-split-w';
  var GOLD = '#c9a227';
  var DOC_PREFIXES = ['/university/', '/library/', '/my-notes/', '/pdf-library/', '/topics/', '/bootcamps/'];
  var VIEW_TITLES = { feed: '☀️ Feed', ideas: '✨ Ideas', goals: '🎯 Goals', library: '📚 Library' };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function $(id) { return document.getElementById(id); }
  function isDesktop() {
    if (window.matchMedia) {
      try { return window.matchMedia('(min-width: 1100px)').matches; } catch (e) {}
    }
    return window.innerWidth >= 1100;
  }
  function clampWidth(w) {
    w = parseInt(w, 10);
    if (isNaN(w)) return 0;
    if (w < 380) return 380;
    if (w > 900) return 900;
    return w;
  }
  function loadWidth() {
    var raw = null;
    try { raw = localStorage.getItem(WIDTH_KEY); } catch (e) {}
    return raw ? clampWidth(raw) : 0;
  }
  function saveWidth(w) {
    try { localStorage.setItem(WIDTH_KEY, String(w)); } catch (e) {}
  }
  function profileTutor() {
    try {
      var p = JSON.parse(localStorage.getItem('il-noah-profile') || '{}');
      return p && p.avatar === 'genesis' ? 'Genesis' : 'Noah';
    } catch (e) { return 'Noah'; }
  }
  function profileTutorId() { return profileTutor() === 'Genesis' ? 'genesis' : 'noah'; }

  /* ---------------- State ---------------- */
  var state = {
    open: false,
    everOpened: false,
    lastSpec: null, /* last spec passed to open(); {kind:'mountHtml'} for the live-DOM channel */
    width: loadWidth(), /* 0 = CSS default min(52vw, 760px) */
    title: 'Workspace'
  };

  /* ---------------- CSS (ilsx- prefix) ---------------- */
  var css = [
    '.muse-app{transition:margin-right .25s ease}',
    '.ilsx-pane{position:fixed;top:0;right:0;height:100dvh;width:min(52vw,760px);z-index:80;',
    'background:var(--panel,#10141d);color:var(--text,#e8e4da);border-left:1px solid rgba(201,162,39,.28);',
    'box-shadow:-18px 0 50px rgba(0,0,0,.5);display:flex;flex-direction:column;',
    'transform:translateX(105%);transition:transform .25s ease;box-sizing:border-box}',
    '.ilsx-pane *{box-sizing:border-box}',
    '.ilsx-pane.ilsx-on{transform:none}',
    '.ilsx-drag{position:absolute;left:-4px;top:0;bottom:0;width:9px;cursor:ew-resize;z-index:3;touch-action:none}',
    '.ilsx-drag:hover,.ilsx-drag.ilsx-dragging{background:rgba(201,162,39,.35)}',
    '.ilsx-switcher{display:none;padding:.55rem .8rem 0}',
    '.ilsx-seg{display:flex;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:999px;padding:3px;gap:3px}',
    '.ilsx-seg button{flex:1;background:none;border:none;color:var(--text,#e8e4da);border-radius:999px;',
    'padding:.42rem .6rem;font:inherit;font-size:.86rem;cursor:pointer;white-space:nowrap}',
    '.ilsx-seg button[aria-pressed="true"]{background:' + GOLD + ';color:#0a0e1a;font-weight:700}',
    '.ilsx-head{display:flex;align-items:center;gap:.5rem;padding:.65rem .8rem;border-bottom:1px solid rgba(255,255,255,.08);flex:none}',
    '.ilsx-title{flex:1;min-width:0;font-size:.95rem;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.ilsx-btn{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);color:inherit;',
    'border-radius:8px;padding:.35rem .6rem;font:inherit;font-size:.85rem;cursor:pointer;flex:none}',
    '.ilsx-btn:hover{border-color:rgba(201,162,39,.6)}',
    '.ilsx-body{flex:1;min-height:0;overflow-y:auto;position:relative}',
    '.ilsx-body.ilsx-frame-mode{overflow:hidden;display:flex;flex-direction:column}',
    '.ilsx-frame{border:0;width:100%;height:100%;flex:1;display:block;background:#fff}',
    '.ilsx-pre{margin:0;padding:1rem 1.1rem;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;',
    'font-size:.86rem;line-height:1.6;white-space:pre-wrap;word-break:break-word;color:var(--text,#e8e4da)}',
    '.ilsx-viewhost{min-height:100%}',
    '.ilsx-note{color:var(--muted2,#9a958a);font-size:.9rem;line-height:1.55;padding:1rem 1.1rem;margin:0}',
    '.ilsx-home{padding:1.1rem}',
    '.ilsx-home h2{font-size:1.08rem;margin:0 0 .35rem}',
    '.ilsx-home p{color:var(--muted2,#9a958a);font-size:.9rem;line-height:1.55;margin:0 0 1rem}',
    '.ilsx-home-grid{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}',
    '.ilsx-home-btn{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.12);color:inherit;',
    'border-radius:12px;padding:.9rem .8rem;font:inherit;font-size:.92rem;cursor:pointer;text-align:left}',
    '.ilsx-home-btn:hover{border-color:rgba(201,162,39,.65);background:rgba(201,162,39,.08)}',
    '.ilsx-home-btn b{display:block;font-size:1rem;margin-bottom:.2rem}',
    '.ilsx-home-btn span{color:var(--muted2,#9a958a);font-size:.8rem;line-height:1.4;display:block}',
    '#ilSplitBtn[aria-pressed="true"]{background:rgba(201,162,39,.2);border-color:rgba(201,162,39,.65);color:#e6c95c}',
    '@media (max-width:1099px){',
    '.ilsx-pane{inset:0;width:100%!important;height:100dvh;border-left:none;box-shadow:none}',
    '.ilsx-switcher{display:block}',
    '.ilsx-drag{display:none}',
    '}'
  ].join('\n');
  if (!document.getElementById('il-split-style')) {
    var style = document.createElement('style');
    style.id = 'il-split-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  /* ---------------- DOM ---------------- */
  var pane = document.createElement('aside');
  pane.className = 'ilsx-pane';
  pane.setAttribute('aria-label', 'Workspace pane');
  pane.setAttribute('aria-hidden', 'true');
  pane.innerHTML =
    '<div class="ilsx-drag" aria-hidden="true"></div>' +
    '<div class="ilsx-switcher"><div class="ilsx-seg" role="group" aria-label="Switch between chat and workspace">' +
    '<button type="button" data-ilsx-switch="chat" aria-pressed="false">💬 Chat</button>' +
    '<button type="button" data-ilsx-switch="workspace" aria-pressed="true">◫ Workspace</button>' +
    '</div></div>' +
    '<div class="ilsx-head">' +
    '<span class="ilsx-title"></span>' +
    '<button type="button" class="ilsx-btn" data-ilsx-home aria-label="Workspace home" title="Workspace home">🏠 Home</button>' +
    '<button type="button" class="ilsx-btn" data-ilsx-close aria-label="Close workspace pane" title="Close workspace pane">✕</button>' +
    '</div>' +
    '<div class="ilsx-body"></div>';
  document.body.appendChild(pane);

  var titleEl = pane.querySelector('.ilsx-title');
  var bodyElmnt = pane.querySelector('.ilsx-body');
  var dragEl = pane.querySelector('.ilsx-drag');
  if (state.width) pane.style.width = state.width + 'px';
  setTitle(state.title);

  function setTitle(t) {
    state.title = t ? String(t) : 'Workspace';
    if (titleEl) titleEl.textContent = state.title;
  }

  /* ---------------- View ctx ----------------
   * discuss/go delegate to window.ILViews.ctx when the views shell is
   * available. The wrappers add one pane-aware behaviour on top of the
   * delegation: on mobile, discuss returns the user to the chat (the
   * pane covers it), which is what "discuss this beside the chat"
   * means on a stacked layout. Without ILViews, fallbacks are built
   * from the profile + composer directly. */
  function makeCtx() {
    var shared = (window.ILViews && window.ILViews.ctx) ? window.ILViews.ctx : null;
    return {
      tutor: function () {
        if (shared && typeof shared.tutor === 'function') {
          try { return shared.tutor(); } catch (e) {}
        }
        return profileTutor();
      },
      tutorId: function () {
        if (shared && typeof shared.tutorId === 'function') {
          try { return shared.tutorId(); } catch (e) {}
        }
        return profileTutorId();
      },
      discuss: function (text) {
        if (shared && typeof shared.discuss === 'function') {
          try { shared.discuss(text); } catch (e) {}
        } else {
          var ta = $('composerInput');
          if (ta) {
            ta.value = String(text || '');
            try { ta.dispatchEvent(new Event('input', { bubbles: true })); } catch (e2) {}
            try { ta.focus(); } catch (e3) {}
          }
        }
        if (!isDesktop() && state.open) closePane();
      },
      go: function (name) {
        if (shared && typeof shared.go === 'function') {
          try { shared.go(name); return; } catch (e) {}
        }
        if (name === 'chat') { if (!isDesktop()) closePane(); return; }
        if (VIEW_TITLES[name]) openPane({ kind: 'view', view: name, title: VIEW_TITLES[name] });
      }
    };
  }

  /* ---------------- Layout ---------------- */
  function applyLayout() {
    var app = document.querySelector('.muse-app');
    if (!app) return;
    if (state.open && isDesktop()) {
      document.body.classList.add('il-split-on');
      var w = state.width || pane.offsetWidth;
      if (w) app.style.marginRight = w + 'px';
    } else {
      document.body.classList.remove('il-split-on');
      app.style.marginRight = '';
    }
  }
  function showPane() {
    state.open = true;
    state.everOpened = true;
    pane.classList.add('ilsx-on');
    pane.setAttribute('aria-hidden', 'false');
    var btn = $('ilSplitBtn');
    if (btn) btn.setAttribute('aria-pressed', 'true');
    applyLayout();
  }
  function closePane() {
    state.open = false;
    pane.classList.remove('ilsx-on');
    pane.setAttribute('aria-hidden', 'true');
    var btn = $('ilSplitBtn');
    if (btn) btn.setAttribute('aria-pressed', 'false');
    applyLayout();
  }

  /* ---------------- Rendering ---------------- */
  function setFrameMode(on) {
    if (on) bodyElmnt.classList.add('ilsx-frame-mode');
    else bodyElmnt.classList.remove('ilsx-frame-mode');
  }
  function noteHtml(msg) {
    setFrameMode(false);
    bodyElmnt.innerHTML = '<p class="ilsx-note">' + esc(msg) + '</p>';
  }

  function renderHome() {
    setFrameMode(false);
    setTitle('Workspace');
    bodyElmnt.innerHTML =
      '<div class="ilsx-home"><h2>◫ Workspace</h2>' +
      '<p>Lessons, labs, documents and artifacts you open will appear here beside the chat.</p>' +
      '<div class="ilsx-home-grid">' +
      '<button type="button" class="ilsx-home-btn" data-ilsx-view="feed"><b>☀️ Feed</b><span>Short posts written for you by your tutor</span></button>' +
      '<button type="button" class="ilsx-home-btn" data-ilsx-view="ideas"><b>✨ Ideas</b><span>Concrete things your tutor could do for you</span></button>' +
      '<button type="button" class="ilsx-home-btn" data-ilsx-view="goals"><b>🎯 Goals</b><span>Goals your tutor is carrying with you</span></button>' +
      '<button type="button" class="ilsx-home-btn" data-ilsx-view="library"><b>📚 Library</b><span>Your documents, certificates, and files</span></button>' +
      '</div></div>';
    var btns = bodyElmnt.querySelectorAll('[data-ilsx-view]');
    for (var i = 0; i < btns.length; i++) (function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-ilsx-view');
        openPane({ kind: 'view', view: v, title: VIEW_TITLES[v] || 'Workspace' });
      });
    })(btns[i]);
  }

  function renderView(name) {
    setFrameMode(false);
    bodyElmnt.innerHTML = '';
    var host = document.createElement('div');
    host.className = 'ilsx-viewhost';
    bodyElmnt.appendChild(host);
    var ctx = makeCtx();
    try {
      if (name === 'feed' && window.ILFeedView && window.ILFeedView.mount) { window.ILFeedView.mount(host, ctx); return; }
      if (name === 'ideas' && window.ILIdeasView && window.ILIdeasView.mount) { window.ILIdeasView.mount(host, ctx); return; }
      if (name === 'goals' && window.ILGoals && window.ILGoals.mountView) { window.ILGoals.mountView(host, ctx); return; }
      if (name === 'library' && window.ILLibraryView && window.ILLibraryView.mount) { window.ILLibraryView.mount(host, ctx); return; }
    } catch (e) {
      noteHtml('This view could not load just now.');
      return;
    }
    noteHtml('This view is still loading — try again in a moment.');
  }

  function renderSpec(spec) {
    var kind = spec.kind || (spec.src ? 'url' : (spec.html ? 'html' : (spec.view ? 'view' : '')));
    setTitle(spec.title || VIEW_TITLES[spec.view] || 'Workspace');
    if (kind === 'html') {
      setFrameMode(true);
      bodyElmnt.innerHTML = '';
      var hf = document.createElement('iframe');
      hf.className = 'ilsx-frame';
      hf.setAttribute('sandbox', 'allow-scripts');
      hf.setAttribute('title', state.title);
      hf.srcdoc = spec.html == null ? '' : String(spec.html);
      bodyElmnt.appendChild(hf);
    } else if (kind === 'url') {
      setFrameMode(true);
      bodyElmnt.innerHTML = '';
      var uf = document.createElement('iframe');
      uf.className = 'ilsx-frame';
      uf.setAttribute('title', state.title);
      if (spec.src) uf.src = String(spec.src);
      bodyElmnt.appendChild(uf);
    } else if (kind === 'text') {
      setFrameMode(false);
      bodyElmnt.innerHTML = '';
      var pre = document.createElement('pre');
      pre.className = 'ilsx-pre';
      pre.textContent = spec.text == null ? '' : String(spec.text);
      bodyElmnt.appendChild(pre);
    } else if (kind === 'view') {
      renderView(spec.view);
    } else {
      renderHome();
    }
  }

  /* ---------------- Public API ---------------- */
  function openPane(spec) {
    if (!spec || typeof spec !== 'object') { homePane(); return; }
    state.lastSpec = spec;
    renderSpec(spec);
    showPane();
  }
  function homePane() {
    state.lastSpec = null;
    renderHome();
    showPane();
  }
  function togglePane() {
    if (state.open) { closePane(); return; }
    if (state.lastSpec) {
      /* mountHtml content is live DOM wired by its caller — closing
         only hid it, so reshowing must not re-render over its wiring. */
      if (state.lastSpec.kind === 'mountHtml') { showPane(); return; }
      openPane(state.lastSpec);
      return;
    }
    homePane();
  }
  /* Live-DOM channel for first-party modules (see header comment). */
  function mountHtml(htmlString, title) {
    state.lastSpec = { kind: 'mountHtml', title: title ? String(title) : 'Workspace' };
    setFrameMode(false);
    setTitle(title || 'Workspace');
    bodyElmnt.innerHTML = htmlString == null ? '' : String(htmlString);
    showPane();
    return bodyElmnt;
  }
  function getBodyEl() { return bodyElmnt || null; }

  window.ILSplit = {
    open: openPane,
    close: closePane,
    toggle: togglePane,
    isOpen: function () { return !!state.open; },
    home: homePane,
    mountHtml: mountHtml,
    bodyEl: getBodyEl
  };

  /* ---------------- Chrome wiring ---------------- */
  pane.querySelector('[data-ilsx-close]').addEventListener('click', closePane);
  pane.querySelector('[data-ilsx-home]').addEventListener('click', homePane);
  var switchBtns = pane.querySelectorAll('[data-ilsx-switch]');
  for (var s = 0; s < switchBtns.length; s++) (function (b) {
    b.addEventListener('click', function () {
      if (b.getAttribute('data-ilsx-switch') === 'chat') closePane();
      else showPane();
    });
  })(switchBtns[s]);

  /* Header toggle in the chat header. */
  var actions = document.querySelector('.muse-head .head-actions') || document.querySelector('.head-actions');
  if (actions && !$('ilSplitBtn')) {
    var toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.className = 'icon-btn';
    toggleBtn.id = 'ilSplitBtn';
    toggleBtn.textContent = '◫';
    toggleBtn.setAttribute('aria-label', 'Toggle workspace pane');
    toggleBtn.setAttribute('aria-pressed', 'false');
    toggleBtn.setAttribute('title', 'Toggle workspace pane');
    toggleBtn.addEventListener('click', togglePane);
    actions.appendChild(toggleBtn);
  }

  /* Escape closes the pane on mobile only; on desktop the split is
     persistent by design. */
  document.addEventListener('keydown', function (ev) {
    var key = ev.key || (ev.keyCode === 27 ? 'Escape' : '');
    if (key === 'Escape' && state.open && !isDesktop()) closePane();
  });

  window.addEventListener('resize', function () { if (state.open) applyLayout(); });

  /* ---------------- Drag to resize (desktop) ---------------- */
  if (dragEl) {
    dragEl.addEventListener('mousedown', function (ev) {
      if (!isDesktop()) return;
      ev.preventDefault();
      var startX = ev.clientX;
      var startW = state.width || pane.offsetWidth;
      dragEl.classList.add('ilsx-dragging');
      function onMove(e2) {
        var w = clampWidth(startW + (startX - e2.clientX));
        if (!w) return;
        state.width = w;
        pane.style.width = w + 'px';
        applyLayout();
      }
      function onUp() {
        dragEl.classList.remove('ilsx-dragging');
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
        if (state.width) saveWidth(state.width);
      }
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
    });
    dragEl.addEventListener('touchstart', function (ev) {
      if (!isDesktop() || !ev.touches || !ev.touches.length) return;
      var startX = ev.touches[0].clientX;
      var startW = state.width || pane.offsetWidth;
      function onMove(e2) {
        if (!e2.touches || !e2.touches.length) return;
        var w = clampWidth(startW + (startX - e2.touches[0].clientX));
        if (!w) return;
        state.width = w;
        pane.style.width = w + 'px';
        applyLayout();
      }
      function onEnd() {
        document.removeEventListener('touchmove', onMove);
        document.removeEventListener('touchend', onEnd);
        if (state.width) saveWidth(state.width);
      }
      document.addEventListener('touchmove', onMove);
      document.addEventListener('touchend', onEnd);
    }, { passive: true });
  }

  /* ---------------- Chat link interception (always-on) ---------------- */
  var threadInner = $('threadInner');
  if (threadInner) {
    threadInner.addEventListener('click', function (ev) {
      if (ev.defaultPrevented) return;
      if (ev.button != null && ev.button !== 0) return;
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
      var node = ev.target;
      var anchor = null;
      while (node && node !== threadInner) {
        if (node.tagName === 'A' && node.getAttribute('href')) { anchor = node; break; }
        node = node.parentNode;
      }
      if (!anchor) return;
      if (anchor.target && anchor.target !== '_self') return;
      var path = anchor.pathname || '';
      if (!path && anchor.href) {
        try { path = new URL(anchor.href).pathname || ''; } catch (e) { path = ''; }
      }
      /* Same-origin only: anchor.host is '' for relative URLs and the
         page host for absolute same-origin URLs. */
      if (anchor.host && anchor.host !== window.location.host) return;
      var hit = false;
      for (var i = 0; i < DOC_PREFIXES.length; i++) {
        if (path.indexOf(DOC_PREFIXES[i]) === 0) { hit = true; break; }
      }
      if (!hit) return;
      ev.preventDefault();
      var label = (anchor.textContent || '').replace(/\s+/g, ' ').replace(/^\s+|\s+$/g, '');
      openPane({
        kind: 'url',
        src: anchor.href,
        title: label || path
      });
    });
  }
})();
