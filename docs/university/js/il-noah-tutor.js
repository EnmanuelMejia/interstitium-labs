/* =====================================================================
 * Interstitium Labs — Noah Tutor integration (js/il-noah-tutor.js)
 *
 * WORKSTREAM 3 (2026-10-08): Noah AI woven through the learning flow.
 *
 * Four integrations, one contract — the existing widget API:
 *   window.IL.noahAI = { open, close, toggle, ask, endpoint }
 * (js/noah.js). The widget's own send path calls IL.noahAI.ask(text, hist),
 * so every integration below "uses IL.noahAI.ask with a context string" by
 * pre-loading the widget input with a lesson/story/stuck context prefix.
 * The student always presses send themselves — nothing is auto-sent to the
 * /api/noah backend. (Struggle nudges, item 2: the nudge opens Noah; the
 * student asks.)
 *
 *  1. "Ask Noah about this lesson" button in every module header
 *     (wired from course-shell.js moduleHTML).
 *  2. Struggle detection: after 2 consecutive wrong answers on the same
 *     drill item (or 2 consecutive wrong quick-checks in a module), an
 *     inline "Stuck? Noah can walk you through this." card appears.
 *     Max 1 nudge per module per session (in-memory + localStorage
 *     "il-noah-nudges-v1", nudges expire after 24h).
 *  3. Story cards (il-stories.js, sibling worker) get a "Discuss with Noah"
 *     affordance: IL.noahTutor.discussStory(story) plus automatic
 *     enhancement of the sibling's real markup — in-module asides
 *     (.il-story: hook + cast + bridge), catalog cards (.il-story-card),
 *     story-of-the-day (.il-sotd) — via MutationObserver. Any other
 *     renderer can opt in with the data-story-* contract:
 *       <div data-story-title="..." data-story-figures="A|B"
 *            data-story-claims="x|y"></div>   (| separated, optional).
 *  4. End-of-module "Check my understanding with Noah" — opens Noah with
 *     a Socratic-quiz prompt built from the module title + objectives
 *     (client-side template; no invented content claims).
 *
 * Safety: every public entry guards `noahReady()` (typeof IL !==
 * 'undefined' && IL.noahAI) so the player never crashes if Noah fails to
 * load. ES5 only. Dark multicloud theme (gold #c9a227 / cyan #62d8e9 on
 * deep-navy), dark-mode default untouched, paywall untouched, footer
 * untouched. prefers-reduced-motion honored (no motion except under
 * prefers-reduced-motion: no-preference).
 *
 * Noah must never claim to be Muse — the honesty line is baked into every
 * prefill: HONESTY.
 * ===================================================================== */
(function () {
  'use strict';

  var VERSION = '1.0.0';
  var LS_KEY = 'il-noah-nudges-v1';
  var NUDGE_EXPIRE_MS = 24 * 60 * 60 * 1000; /* re-arm next day, not mid-session */
  var WRONG_THRESHOLD = 2;

  /* Noah honesty guardrail — appended to every context prefill. */
  var HONESTY = ' You are Noah AI, the resident tutor of Interstitium Labs — ' +
    'never claim to be Muse or any other assistant.';

  var w = (typeof window !== 'undefined') ? window : null;
  var nudgedThisSession = {}; /* moduleId -> true (per-session cap) */

  /* ================= guards ========================================= */

  function noahReady() {
    return (typeof IL !== 'undefined') && !!IL && !!IL.noahAI &&
      typeof IL.noahAI.open === 'function';
  }

  function hasLocalStorage() {
    try { return (typeof localStorage !== 'undefined') && !!localStorage; }
    catch (e) { return false; }
  }

  /* ================= context builders ================================ */

  function courseLabel() {
    try {
      if (typeof COURSE !== 'undefined' && COURSE) {
        return (COURSE.code ? COURSE.code + ' · ' : '') +
          (COURSE.title || COURSE.courseId || 'this course');
      }
    } catch (e) {}
    return 'this course';
  }

  function moduleLabel(mod) {
    if (!mod) return 'this module';
    return (mod.code ? mod.code + ' · ' : '') + (mod.title || mod.id || 'this module');
  }

  function moduleIdOf(mod) {
    return String((mod && (mod.id || mod.code)) || 'unknown-module');
  }

  function trunc(s, n) {
    s = String(s == null ? '' : s);
    return s.length > n ? s.slice(0, n - 1) + '…' : s;
  }

  /* "The student is studying IL-29 · ThreatLocker Zero-Trust CBT, module
     <title>." — the context prefix IL.noahAI.ask receives. */
  function lessonContext(mod, section) {
    var s = 'The student is studying ' + courseLabel() +
      ', module "' + moduleLabel(mod) + '"';
    if (section) s += ' (current section: ' + trunc(section, 90) + ')';
    return s + '.';
  }

  function currentSection(wrapEl) {
    if (!wrapEl || !wrapEl.querySelector) return '';
    try {
      var body = wrapEl.querySelector('.mod-body');
      if (!body) return '';
      var open = body.querySelectorAll('details[open] summary');
      if (open && open.length) return trunc(open[open.length - 1].textContent || '', 90);
      var h3 = body.querySelectorAll('h3');
      var i, t;
      for (i = 0; i < h3.length; i++) {
        t = h3[i].textContent || '';
        if (t && !/quick checks|flashcards/i.test(t)) return trunc(t, 90);
      }
      if (h3.length) return trunc(h3[0].textContent || '', 90);
    } catch (e) {}
    return '';
  }

  function moduleTopics(mod) {
    var t = [];
    try {
      if (mod && mod.objectives && mod.objectives.length) t = t.concat(mod.objectives.slice(0, 4));
      else if (mod && mod.summary) t.push(mod.summary);
    } catch (e) {}
    return trunc(t.join('; '), 280) || 'the module material';
  }

  /* ================= widget plumbing ================================= */

  /* Open the Noah widget and pre-load its input with context text.
     Returns true if Noah was ready (prefill attempted), false otherwise.
     Never auto-sends: the student reviews and presses send. */
  function openWithPrefill(text) {
    if (!noahReady() || !w) return false;
    try {
      IL.noahAI.open();
    } catch (e) { return false; }
    var tries = 0;
    (function fill() {
      tries++;
      var input = null;
      try { input = w.document.querySelector('#noah-input'); } catch (e) {}
      if (input) {
        try {
          input.value = String(text);
          if (input.setSelectionRange) input.setSelectionRange(input.value.length, input.value.length);
          input.focus();
        } catch (e2) {}
        return;
      }
      if (tries < 12) setTimeout(fill, 120);
    })();
    return true;
  }

  /* ================= 1. Ask-about-lesson ============================= */

  function askAboutLesson(mod, wrapEl) {
    var section = currentSection(wrapEl);
    var pre = lessonContext(mod, section) +
      ' The student wants to ask about this lesson. ' +
      'Answer Socratic-style (guide with questions before answers) and stay grounded in the lesson above.' +
      HONESTY +
      '\n\nTheir question: ';
    return openWithPrefill(pre);
  }

  /* ================= 2. Struggle detection =========================== */

  function loadStore() {
    var s = { streaks: {}, nudged: {} };
    if (!hasLocalStorage()) return s;
    try {
      var raw = localStorage.getItem(LS_KEY);
      if (raw) {
        var p = JSON.parse(raw);
        if (p && typeof p === 'object') {
          if (p.streaks && typeof p.streaks === 'object') s.streaks = p.streaks;
          if (p.nudged && typeof p.nudged === 'object') s.nudged = p.nudged;
        }
      }
    } catch (e) {}
    /* Expire nudges older than 24h so tomorrow's session can nudge again. */
    try {
      var now = Date.now(), k, changed = false;
      for (k in s.nudged) {
        if (s.nudged.hasOwnProperty(k) && (now - Number(s.nudged[k]) > NUDGE_EXPIRE_MS)) {
          delete s.nudged[k]; changed = true;
        }
      }
      if (changed) saveStore(s);
    } catch (e2) {}
    return s;
  }

  function saveStore(s) {
    if (!hasLocalStorage()) return;
    try { localStorage.setItem(LS_KEY, JSON.stringify(s)); } catch (e) {}
  }

  /* recordAnswer(mod, itemKey, stem, correct, anchorEl)
     mod      — course module object (for id + lesson context)
     itemKey  — 'drill:<di>:<ii>' (retryable) or 'quiz:<qi>' (one-shot)
     stem     — question text (used only in the nudge prefill)
     correct  — boolean
     anchorEl — the .quiz box to host the inline nudge card
     Drill items track per-item streaks (2 consecutive wrong on the same
     item). One-shot quick-checks track a per-module streak (2 consecutive
     wrong quick-checks in the module). */
  function recordAnswer(mod, itemKey, stem, correct, anchorEl) {
    if (!mod || itemKey == null) return;
    var moduleId = moduleIdOf(mod);
    var ik = String(itemKey);
    var key = (ik.indexOf('quiz:') === 0) ? moduleId + '|quiz-streak' : moduleId + '|' + ik;
    var store = loadStore();
    if (correct) {
      store.streaks[key] = 0;
      saveStore(store);
      return;
    }
    store.streaks[key] = (Number(store.streaks[key]) || 0) + 1;
    saveStore(store);
    if (store.streaks[key] >= WRONG_THRESHOLD) maybeNudge(mod, stem, anchorEl, store);
  }

  function maybeNudge(mod, stem, anchorEl, store) {
    var moduleId = moduleIdOf(mod);
    if (nudgedThisSession[moduleId]) return;          /* per-session cap */
    if (store.nudged && store.nudged[moduleId]) return; /* persisted cap */
    if (!anchorEl || !anchorEl.querySelector || !anchorEl.appendChild) return;
    var existing = null;
    try { existing = anchorEl.querySelector('.noah-nudge'); } catch (e) {}
    if (existing) return;
    if (!w || !w.document || !w.document.createElement) return;

    var card = w.document.createElement('div');
    card.className = 'noah-nudge';
    card.setAttribute('role', 'note');
    card.setAttribute('aria-label', 'Noah AI can help with this question');
    var title = w.document.createElement('div');
    title.className = 'noah-nudge-title';
    title.textContent = 'Stuck? Noah can walk you through this.';
    var sub = w.document.createElement('div');
    sub.className = 'noah-nudge-sub';
    sub.textContent = 'Two misses on this one — talk it through Socratic-style instead of guessing.';
    var btn = w.document.createElement('button');
    btn.type = 'button';
    btn.className = 'noah-nudge-btn';
    btn.textContent = '◈ Ask Noah about this question';
    btn.setAttribute('aria-label', 'Ask Noah AI about this question');
    btn.addEventListener('click', function () { openStuckNudge(mod, stem); });
    card.appendChild(title);
    card.appendChild(sub);
    card.appendChild(btn);
    try { anchorEl.appendChild(card); } catch (e2) { return; }

    nudgedThisSession[moduleId] = true;
    store.nudged = store.nudged || {};
    try { store.nudged[moduleId] = Date.now(); } catch (e3) { store.nudged[moduleId] = 1; }
    saveStore(store);
  }

  function openStuckNudge(mod, stem) {
    var pre = lessonContext(mod, '') +
      ' The student is stuck on this question: "' + trunc(stem, 220) + '".' +
      ' Help them reason through it Socratic-style — one guiding question at a time; ' +
      'do not hand them the answer outright.' +
      HONESTY +
      '\n\nTheir question: ';
    return openWithPrefill(pre);
  }

  /* ================= 3. Story discussions ============================ */

  function storyFromCard(card) {
    var title = textOf(card, '.il-story__hook') || textOf(card, '#il-sotd-h') ||
      (function () {
        var h = null;
        try { h = card.querySelector('h4,h3,h2'); } catch (e) {}
        return h ? (h.textContent || '').trim() : '';
      })();
    /* Explicit contract (any renderer may set these, | separated). */
    var g = function (name) {
      try { return card.getAttribute('data-story-' + name) || ''; } catch (e) { return ''; }
    };
    if (!title) title = g('title');
    var split = function (v) {
      return String(v || '').split('|').map(function (x) { return x.trim(); })
        .filter(function (x) { return !!x; });
    };
    /* In-module aside (.il-story): cast line holds the figures, hook/bridge
       hold the claims. Catalog cards (.il-story-card): h4 + hook paragraph.
       Story of the day (.il-sotd): h3 + hook. */
    var castRaw = textOf(card, '.il-story__cast').replace(/^\s*Cast:\s*/i, '');
    var figures = castRaw ? castRaw.split(/\s*[·;]\s*/).filter(function (x) { return !!x.trim(); }) : [];
    figures = figures.concat(split(g('figures')));
    var claims = [];
    var hook = textOf(card, '.il-story-card__hook') || textOf(card, '.il-sotd__hook');
    var bridge = textOf(card, '.il-story__bridge');
    if (hook) claims.push(hook.replace(/^[\s"“”]+|[\s"“”]+$/g, ''));
    if (bridge) claims.push(bridge);
    claims = claims.concat(split(g('claims')));
    return {
      title: trunc(title || 'this story', 120),
      figures: figures,
      claims: claims
    };
  }

  function textOf(card, sel) {
    try {
      var n = card.querySelector(sel);
      return n ? (n.textContent || '').trim() : '';
    } catch (e) { return ''; }
  }

  function figName(f) {
    if (f == null) return '';
    if (typeof f === 'string') return f.trim();
    if (typeof f === 'object') {
      var parts = [];
      if (f.name) parts.push(String(f.name));
      if (f.role) parts.push('— ' + String(f.role));
      if (f.dates) parts.push('(' + String(f.dates) + ')');
      return parts.join(' ').trim();
    }
    return String(f);
  }

  function discussStory(story) {
    story = story || {};
    var parts = ['The student wants to discuss a course story with Noah.'];
    if (story.title) parts.push('Story: "' + trunc(story.title, 160) + '"');
    var figs = (story.figures || []).map(figName).filter(function (x) { return !!x; });
    if (figs.length) parts.push('Key figures: ' + figs.join('; '));
    if (story.claims && story.claims.length) parts.push('Key claims: ' + story.claims.join(' | '));
    parts.push('Discuss this Socratic-style — probe the student\'s grasp of the figures ' +
      'and claims, one question at a time. Stay grounded in the story above; do not invent new claims.' +
      HONESTY);
    return openWithPrefill(parts.join('\n'));
  }

  /* Enhance rendered story cards with a "Discuss with Noah" button.
     Covers the sibling renderer's markup: in-module asides (.il-story),
     catalog cards (.il-story-card), story-of-the-day (.il-sotd), plus any
     element carrying the data-story-* attribute contract.
     Idempotent via data-noah-bound. Returns number of cards bound. */
  function attachStoryCards(root) {
    if (!w || !w.document || !w.document.createElement) return 0;
    root = root || w.document;
    var nodes;
    try { nodes = root.querySelectorAll('.il-story,.il-story-card,.il-sotd,[data-story-title]'); } catch (e) { return 0; }
    var n = 0, i, card, btn, story;
    for (i = 0; i < nodes.length; i++) {
      card = nodes[i];
      try {
        if (card.getAttribute('data-noah-bound')) continue;
        card.setAttribute('data-noah-bound', '1');
      } catch (e2) { continue; }
      story = storyFromCard(card);
      btn = w.document.createElement('button');
      btn.type = 'button';
      btn.className = 'noah-story-btn';
      btn.textContent = '◈ Discuss with Noah';
      btn.setAttribute('aria-label', 'Discuss this story with Noah AI');
      (function (st) {
        btn.addEventListener('click', function (ev) {
          if (ev && ev.stopPropagation) ev.stopPropagation();
          discussStory(st);
        });
      })(story);
      try { card.appendChild(btn); n++; } catch (e3) {}
    }
    return n;
  }

  function initStories() {
    try { attachStoryCards(w.document); } catch (e) {}
    if (typeof MutationObserver === 'undefined') return;
    var pending = null;
    try {
      var obs = new MutationObserver(function () {
        if (pending) return;
        pending = setTimeout(function () {
          pending = null;
          try { attachStoryCards(w.document); } catch (e) {}
        }, 300);
      });
      if (w.document.body) obs.observe(w.document.body, { childList: true, subtree: true });
    } catch (e) {}
  }

  /* ================= 4. End-of-module check-in ======================= */

  function onModuleComplete(mod, footEl) {
    if (!noahReady() || !mod || !footEl || !footEl.querySelector || !footEl.appendChild) return false;
    try { if (footEl.querySelector('.noah-checkin')) return false; } catch (e) { return false; }
    if (!w || !w.document || !w.document.createElement) return false;

    var row = w.document.createElement('div');
    row.className = 'noah-checkin';
    row.setAttribute('role', 'note');
    var label = w.document.createElement('span');
    label.className = 'noah-checkin-label';
    label.textContent = 'Module complete — want to lock it in?';
    var btn = w.document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn noah-checkin-btn';
    btn.textContent = '◈ Check my understanding with Noah';
    btn.setAttribute('aria-label', 'Check your understanding of this module with Noah AI');
    btn.addEventListener('click', function () { openSocraticCheckin(mod); });
    row.appendChild(label);
    row.appendChild(btn);
    try { footEl.appendChild(row); } catch (e2) { return false; }
    return true;
  }

  function openSocraticCheckin(mod) {
    var pre = 'The student just completed ' + lessonContext(mod, '') +
      ' Module topics: ' + moduleTopics(mod) + '.' +
      ' Quiz them Socratic-style: ask 2–3 questions, one at a time, drawn ONLY from the module ' +
      'title and topics above — do not invent content claims.' +
      HONESTY +
      ' Begin with the first question now.';
    return openWithPrefill(pre);
  }

  /* ================= styles (dark multicloud theme) ================== */

  var CSS = [
    '.noah-ask-btn{flex-shrink:0;font:inherit;font-size:12px;font-weight:600;color:var(--gold,#c9a227);',
    ' background:transparent;border:1px solid var(--hairline,rgba(201,162,39,.45));border-radius:999px;',
    ' padding:6px 12px;cursor:pointer;line-height:1.2;white-space:nowrap;}',
    '.noah-ask-btn:hover{background:rgba(201,162,39,.12);border-color:var(--gold,#c9a227);}',
    '.noah-ask-btn:focus-visible{outline:2px solid var(--gold,#c9a227);outline-offset:2px;}',
    '.noah-nudge{margin:12px 0;padding:14px 16px;border:1px solid var(--hairline,rgba(201,162,39,.35));',
    ' border-left:3px solid var(--gold,#c9a227);border-radius:10px;background:var(--panel2,#10161f);}',
    '.noah-nudge-title{font-weight:700;color:var(--gold,#c9a227);margin-bottom:4px;}',
    '.noah-nudge-sub{font-size:13.5px;color:var(--muted,#9aa3b2);margin-bottom:10px;}',
    '.noah-nudge-btn{font:inherit;font-size:13px;font-weight:600;color:#0a0f16;background:var(--gold,#c9a227);',
    ' border:none;border-radius:8px;padding:8px 14px;cursor:pointer;}',
    '.noah-nudge-btn:hover{filter:brightness(1.08);}',
    '.noah-nudge-btn:focus-visible{outline:2px solid #fff;outline-offset:2px;}',
    '.noah-checkin{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:14px;padding:12px 16px;',
    ' border:1px dashed var(--line2,rgba(98,216,233,.4));border-radius:10px;background:rgba(98,216,233,.05);}',
    '.noah-checkin-label{font-size:14px;color:var(--ink,#e8e4d8);}',
    '.noah-checkin-btn{font:inherit;font-size:13px;font-weight:600;color:var(--cyan,#62d8e9);background:transparent;',
    ' border:1px solid var(--line2,rgba(98,216,233,.5));border-radius:8px;padding:8px 14px;cursor:pointer;}',
    '.noah-checkin-btn:hover{background:rgba(98,216,233,.12);}',
    '.noah-checkin-btn:focus-visible{outline:2px solid var(--cyan,#62d8e9);outline-offset:2px;}',
    '.noah-story-btn{font:inherit;font-size:12.5px;font-weight:600;color:var(--gold,#c9a227);background:transparent;',
    ' border:1px solid var(--hairline,rgba(201,162,39,.45));border-radius:999px;padding:6px 12px;cursor:pointer;',
    ' margin-top:10px;}',
    '.noah-story-btn:hover{background:rgba(201,162,39,.12);}',
    '.noah-story-btn:focus-visible{outline:2px solid var(--gold,#c9a227);outline-offset:2px;}',
    '@media (prefers-reduced-motion: no-preference){',
    ' .noah-nudge{animation:noahNudgeIn .28s ease-out;}',
    ' @keyframes noahNudgeIn{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:none;}}',
    '}'
  ].join('\n');

  function injectCSS() {
    if (!w || !w.document) return;
    try {
      if (w.document.getElementById && w.document.getElementById('il-noah-tutor-css')) return;
      var st = w.document.createElement('style');
      st.id = 'il-noah-tutor-css';
      st.setAttribute('data-source', 'il-noah-tutor');
      if (st.styleSheet) st.styleSheet.cssText = CSS; else st.textContent = CSS;
      var head = w.document.head || w.document.getElementsByTagName('head')[0];
      if (head && head.appendChild) head.appendChild(st);
    } catch (e) {}
  }

  /* ================= boot ============================================ */

  function init() {
    injectCSS();
    initStories();
  }

  if (w && w.document) {
    if (w.document.readyState === 'loading' && w.document.addEventListener) {
      w.document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
  }

  /* Export onto the real global window (never a shadowed local). */
  var __exportWin = (typeof window !== 'undefined') ? window : null;
  if (__exportWin) {
    __exportWin.IL = __exportWin.IL || {};
    __exportWin.IL.noahTutor = {
      version: VERSION,
      noahReady: noahReady,
      openWithPrefill: openWithPrefill,
      askAboutLesson: askAboutLesson,
      recordAnswer: recordAnswer,
      discussStory: discussStory,
      attachStoryCards: attachStoryCards,
      onModuleComplete: onModuleComplete
    };
  }
})();
