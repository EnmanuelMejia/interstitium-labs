/* Noah/Genesis Views — the distilled Muse tab system for /noah/
 * (Phase 2 full-application fold-in, 2026-10-11).
 *
 * Muse's app is organized as tabs — Chat, Feed, Ideas, Goals, Library.
 * This shell distills that IA into Noah's own design language: a single
 * segmented view bar in the main column (sticky on mobile), hash-routed
 * (#feed, #ideas, #goals, #library; chat is the default), least clicks —
 * every surface is one tap from every other.
 *
 * Views are separate canonical modules, mounted lazily on first show:
 *   Chat    — the existing /noah/ thread + composer (untouched)
 *   Feed    — noah-feed.js    (window.ILFeedView.mount)
 *   Ideas   — noah-ideas.js   (window.ILIdeasView.mount)
 *   Goals   — noah-goals.js   (window.ILGoals.mountView — same module
 *             as the sidebar panel; one engine, one renderer family)
 *   Library — noah-library.js (window.ILLibraryView.mount)
 *
 * Both twins share this shell and every view module — the tutor is a
 * profile choice (il-noah-profile.avatar), never a fork. ctx.tutor()
 * is how view copy names the active twin.
 *
 * Discuss hand-off: a view's "Discuss" action switches to Chat and
 * pre-fills the composer with the item as context. The user presses
 * send — drafting is the agent's job, sending stays the user's
 * (draft → approve governance).
 */
(function () {
  'use strict';
  if (window.ILViews) return;
  if (!document.getElementById('newChatBtn')) return; /* /noah/ only */

  var VIEWS = ['chat', 'feed', 'ideas', 'goals', 'library'];
  var LABELS = {
    chat: '💬 Chat',
    feed: '☀️ Feed',
    ideas: '✨ Ideas',
    goals: '🎯 Goals',
    library: '📚 Library',
  };
  var current = 'chat';
  var mounted = {};
  var containers = {};

  function $(id) { return document.getElementById(id); }

  function tutorName() {
    try {
      var p = JSON.parse(localStorage.getItem('il-noah-profile') || '{}');
      return p && p.avatar === 'genesis' ? 'Genesis' : 'Noah';
    } catch (e) { return 'Noah'; }
  }
  function tutorId() { return tutorName() === 'Genesis' ? 'genesis' : 'noah'; }

  var css = [
    '.ilv-tabs{position:sticky;top:0;z-index:30;display:flex;gap:.35rem;overflow-x:auto;',
    'padding:.5rem .7rem;background:var(--panel,#10141d);border-bottom:1px solid rgba(255,255,255,.08);',
    'scrollbar-width:none}',
    '.ilv-tabs::-webkit-scrollbar{display:none}',
    '.ilv-tabs button{flex:1 0 auto;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);',
    'color:var(--text,#e8e4da);border-radius:999px;padding:.42rem .8rem;font:inherit;font-size:.86rem;cursor:pointer;position:relative;white-space:nowrap}',
    '.ilv-tabs button[aria-pressed="true"]{background:#c9a227;color:#0a0e1a;border-color:#c9a227;font-weight:700}',
    '.ilv-tabs .ilv-badge{position:absolute;top:-5px;right:-2px;background:#b3372f;color:#fff;border-radius:999px;',
    'font-size:.62rem;font-weight:700;padding:0 5px;line-height:1.5}',
    '.ilv-tabs button[aria-pressed="true"] .ilv-badge{background:#b3372f;color:#fff}',
    '.ilv-view{flex:1;overflow-y:auto;padding:1rem clamp(.8rem,3vw,1.6rem) 2rem;max-width:860px;width:100%;margin:0 auto;box-sizing:border-box}',
    '.ilv-view[hidden]{display:none}',
  ].join('\n');
  var style = document.createElement('style');
  style.id = 'il-views-style';
  style.textContent = css;
  document.head.appendChild(style);

  /* ---------- DOM ---------- */
  var main = document.querySelector('.muse-main');
  var thread = $('thread');
  if (!main || !thread) return;
  var composerZone = document.querySelector('.composer-zone');

  var tabs = document.createElement('nav');
  tabs.className = 'ilv-tabs';
  tabs.setAttribute('aria-label', 'Noah views');
  tabs.innerHTML = VIEWS.map(function (v) {
    return '<button type="button" data-view="' + v + '" aria-pressed="' + (v === 'chat') + '">' +
      LABELS[v] + (v === 'goals' ? '<span class="ilv-badge" id="ilvGoalsBadge" hidden></span>' : '') + '</button>';
  }).join('');
  main.insertBefore(tabs, thread);

  VIEWS.slice(1).forEach(function (v) {
    var sec = document.createElement('section');
    sec.className = 'ilv-view';
    sec.id = 'ilv-view-' + v;
    sec.setAttribute('aria-label', LABELS[v].replace(/^\S+\s/, ''));
    sec.hidden = true;
    main.appendChild(sec);
    containers[v] = sec;
  });

  var ctx = {
    tutor: tutorName,
    tutorId: tutorId,
    discuss: discuss,
    go: function (name) { show(name); },
  };

  function discuss(text) {
    show('chat');
    var ta = $('composerInput');
    if (ta) {
      ta.value = String(text || '');
      try { ta.dispatchEvent(new Event('input', { bubbles: true })); } catch (e) {}
      ta.focus();
    }
  }

  function mountView(name) {
    var el = containers[name];
    if (!el) return;
    try {
      if (name === 'feed' && window.ILFeedView) window.ILFeedView.mount(el, ctx);
      else if (name === 'ideas' && window.ILIdeasView) window.ILIdeasView.mount(el, ctx);
      else if (name === 'goals' && window.ILGoals && window.ILGoals.mountView) window.ILGoals.mountView(el);
      else if (name === 'library' && window.ILLibraryView) window.ILLibraryView.mount(el, ctx);
      else if (!mounted[name]) {
        el.innerHTML = '<p style="color:var(--muted2,#9a958a)">This view is still loading — try again in a moment.</p>';
        return;
      }
      mounted[name] = true;
    } catch (e) {
      el.innerHTML = '<p style="color:var(--muted2,#9a958a)">This view could not load just now.</p>';
    }
  }

  function show(name) {
    if (VIEWS.indexOf(name) === -1) name = 'chat';
    current = name;
    tabs.querySelectorAll('button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-view') === name ? 'true' : 'false');
    });
    var isChat = name === 'chat';
    if (thread) thread.style.display = isChat ? '' : 'none';
    if (composerZone) composerZone.style.display = isChat ? '' : 'none';
    VIEWS.slice(1).forEach(function (v) { containers[v].hidden = v !== name; });
    if (!isChat) mountView(name);
    var want = isChat ? '' : '#' + name;
    if (location.hash !== want && location.hash.indexOf('#settings') !== 0) {
      try { history.replaceState(null, '', want || location.pathname + location.search); } catch (e) {}
    }
    if (name === 'goals') refreshBadge();
  }

  tabs.querySelectorAll('button').forEach(function (b) {
    b.addEventListener('click', function () { show(b.getAttribute('data-view')); });
  });

  window.addEventListener('hashchange', function () {
    var h = location.hash.replace('#', '');
    if (VIEWS.indexOf(h) !== -1 && h !== current) show(h);
    else if (h === '' && current !== 'chat') show('chat');
    /* #settings* belongs to the Settings slide-over — not a view. */
  });

  /* Goals badge: active-goal count on the tab (best-effort). */
  function refreshBadge() {
    fetch('/api/goals', { headers: { accept: 'application/json' } })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (j) {
        var b = $('ilvGoalsBadge');
        if (!b) return;
        var goals = (j && j.goals) || [];
        var n = goals.filter(function (g) { return g.status === 'active'; }).length;
        if (n) { b.textContent = n; b.hidden = false; } else b.hidden = true;
      })
      .catch(function () {});
  }

  window.ILViews = { show: show, current: function () { return current; }, ctx: ctx };

  var initial = location.hash.replace('#', '');
  if (VIEWS.indexOf(initial) !== -1 && initial !== 'chat') show(initial);
  refreshBadge();
})();
