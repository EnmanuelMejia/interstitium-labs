/* Noah/Genesis Ideas — the Ideas surface inside /noah/ (2026-10-11).
 *
 * Surface: idea cards the tutor suggests — concrete things Noah/Genesis
 * could build or do FOR the user on this platform (tutoring plans,
 * money / health / shopping / relationship help, job-search help, study
 * systems). Picking a card runs it: "Let's do it" turns the idea into a
 * tracked goal via the live goals engine. "Discuss first" hands the idea
 * text to the chat (ctx.discuss) so the user can talk it through before
 * committing. Cards retire on their own after ~two weeks.
 *
 * Storage: local-first in localStorage "il-ideas-v1":
 *   { cards: [], generatedOnce: bool }
 *   Card: { id, title, detail, effort: 'Quick'|'An afternoon'|'A project',
 *           domain: learn|money|health|shopping|relationships|general|platform,
 *           created_at ISO, expires_at ISO (created + 14 days),
 *           status: 'active'|'dismissed'|'run', goal_id (when run) }
 * This key is being registered as a sync store in a staged worker patch,
 * so ideas will follow the account through the sync layer too; today
 * they are local to this browser. Dismissed cards stay in storage (with
 * status 'dismissed') only so generation can dedupe against them;
 * expired ACTIVE cards are filtered from display and pruned from
 * storage on the next save.
 *
 * Governance: running an idea creates a tracked goal — nothing else.
 * Noah/Genesis prepares and drafts; nothing is sent, bought, or booked
 * without the user's approval. Signed-out visitors get an honest
 * sign-in prompt only — no example or fake cards are ever shown.
 *
 * Staged server upgrade: generation and run-dispatch are client-side
 * adapters over the LIVE /api/noah and /api/goals endpoints today.
 * A dedicated POST /api/ideas endpoint lands in
 * QUEUED-UI-WORKER-PATCH.md; the adapter spot is marked
 * "SERVER-ADAPTER:" below — swap the /api/noah prompt round-trip for
 * that endpoint there when it ships.
 *
 * Contract (mounted by the /noah/ views shell):
 *   window.ILIdeasView = { mount(el, ctx), unmount() }
 *   ctx = { tutor(): 'Noah'|'Genesis', discuss(text), go(viewName) }
 *   mount() may be called repeatedly; it re-renders into el. */
(function () {
  'use strict';
  if (window.ILIdeasView) return;
  if (!document.getElementById('newChatBtn')) return; /* /noah/ only */

  var STORE_KEY = 'il-ideas-v1';
  var GOALS_CACHE_KEY = 'il-goals-v1';
  var PROFILE_KEY = 'il-noah-profile';
  var GOALS_API = '/api/goals';
  var NOAH_API = '/api/noah';
  var RETIRE_MS = 14 * 24 * 60 * 60 * 1000;

  var EFFORTS = ['Quick', 'An afternoon', 'A project'];
  var DOMAIN_META = {
    learn: { icon: '🎓', label: 'Learning' },
    money: { icon: '💰', label: 'Money' },
    health: { icon: '💪', label: 'Health' },
    shopping: { icon: '🛒', label: 'Shopping' },
    relationships: { icon: '💛', label: 'Relationships' },
    general: { icon: '✨', label: 'Life' },
    platform: { icon: '🧩', label: 'Platform' }
  };
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  var state = {
    root: null, ctx: null,
    cards: [], generatedOnce: false,
    signedIn: null, /* null=unknown, true/false once /api/goals answers */
    checked: false, checking: null,
    goalSummaries: null, /* last GET /api/goals summaries (or cache) */
    generating: false,
    running: {}, /* card id -> true while its goal POST is in flight */
    cardErrors: {} /* card id -> inline error text (not persisted) */
  };

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function tutorId() {
    try {
      var p = JSON.parse(localStorage.getItem(PROFILE_KEY) || '{}');
      if (p && p.avatar === 'genesis') return 'genesis';
      if (p && p.avatar === 'noah') return 'noah';
    } catch (e) {}
    if (state.ctx && typeof state.ctx.tutor === 'function') {
      try { return state.ctx.tutor() === 'Genesis' ? 'genesis' : 'noah'; } catch (e2) {}
    }
    return 'noah';
  }
  function tutorName() {
    if (state.ctx && typeof state.ctx.tutor === 'function') {
      try {
        var t = state.ctx.tutor();
        if (t === 'Noah' || t === 'Genesis') return t;
      } catch (e) {}
    }
    return tutorId() === 'genesis' ? 'Genesis' : 'Noah';
  }
  function api(path, opts) {
    opts = opts || {};
    var headers = { 'Content-Type': 'application/json' };
    return fetch(path, {
      method: opts.method || 'GET',
      credentials: 'same-origin',
      headers: headers,
      body: opts.body != null ? JSON.stringify(opts.body) : undefined
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        return { status: res.status, data: data || {} };
      });
    });
  }
  function retireLabel(iso) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    return 'Retires ' + MONTHS[d.getMonth()] + ' ' + d.getDate();
  }
  function newId() {
    return 'idea-' + Date.now().toString(36) + '-' +
      Math.floor(Math.random() * 1000000000).toString(36);
  }

  /* ---------- CSS (own, ili- prefix) ---------- */
  if (!document.getElementById('il-ideas-style')) {
    var css = [
      '.ili-root{background:var(--panel,#10141d);color:var(--text,#e8e4da);',
      'padding:1rem 1.1rem 1.4rem;font:inherit}',
      '.ili-head{display:flex;align-items:flex-start;gap:.7rem;flex-wrap:wrap;margin-bottom:.4rem}',
      '.ili-head h2{font-size:1.1rem;margin:0;flex:1;min-width:180px}',
      '.ili-gov{font-size:.82rem;color:var(--muted2,#9a958a);line-height:1.5;margin:.2rem 0 1rem;max-width:640px}',
      '.ili-gov b{color:#e6c95c;font-weight:600}',
      '.ili-new{background:#c9a227;color:#0a0e1a;border:none;border-radius:8px;',
      'padding:.5rem .9rem;font-weight:700;cursor:pointer;font:inherit;font-size:.88rem;flex:none}',
      '.ili-new:disabled{opacity:.55;cursor:wait}',
      '.ili-grid{display:grid;grid-template-columns:1fr;gap:.8rem}',
      '@media (min-width:700px){.ili-grid{grid-template-columns:1fr 1fr}}',
      '.ili-card{border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:.85rem .95rem;',
      'background:rgba(255,255,255,.03);display:flex;flex-direction:column}',
      '.ili-card h3{margin:0 0 .3rem;font-size:.98rem;line-height:1.35}',
      '.ili-detail{font-size:.87rem;line-height:1.5;color:var(--text,#e8e4da);margin:0 0 .6rem;',
      'display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}',
      '.ili-chips{display:flex;gap:.35rem;flex-wrap:wrap;margin:0 0 .7rem}',
      '.ili-chip{font-size:.7rem;border:1px solid rgba(255,255,255,.16);border-radius:999px;',
      'padding:.14rem .55rem;color:var(--muted2,#9a958a);white-space:nowrap}',
      '.ili-chip.effort{border-color:rgba(201,162,39,.45);color:#e6c95c}',
      '.ili-actions{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:auto}',
      '.ili-actions button{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);',
      'color:inherit;border-radius:8px;padding:.4rem .65rem;font-size:.8rem;cursor:pointer;font:inherit}',
      '.ili-actions button.primary{background:#c9a227;color:#0a0e1a;border-color:#c9a227;font-weight:700}',
      '.ili-actions button:disabled{opacity:.55;cursor:wait}',
      '.ili-actions button.ili-dismiss{margin-left:auto}',
      '.ili-done{font-size:.88rem;color:#34d399;margin:0 0 .55rem;font-weight:600}',
      '.ili-error{font-size:.8rem;color:#e08a8a;margin:.55rem 0 0;line-height:1.45}',
      '.ili-empty{color:var(--muted2,#9a958a);font-size:.9rem;line-height:1.55;max-width:560px}',
      '.ili-signin a{color:#e6c95c}',
      '.ili-status{font-size:.85rem;color:var(--muted2,#9a958a);margin:.4rem 0}'
    ].join('\n');
    var style = document.createElement('style');
    style.id = 'il-ideas-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  /* ---------- storage ---------- */
  function isExpiredActive(card, now) {
    if (!card || card.status !== 'active') return false;
    var t = new Date(card.expires_at).getTime();
    return !isNaN(t) && t <= now;
  }
  function loadStore() {
    var raw = null;
    try { raw = JSON.parse(localStorage.getItem(STORE_KEY) || 'null'); } catch (e) {}
    state.cards = (raw && Array.isArray(raw.cards)) ? raw.cards : [];
    state.generatedOnce = !!(raw && raw.generatedOnce);
    /* Prune expired active cards on load; saveStore persists the prune. */
    var now = Date.now();
    var before = state.cards.length;
    state.cards = state.cards.filter(function (c) { return !isExpiredActive(c, now); });
    if (state.cards.length !== before) saveStore();
  }
  function saveStore() {
    /* Expired active cards are pruned from storage on every save. */
    var now = Date.now();
    state.cards = state.cards.filter(function (c) { return !isExpiredActive(c, now); });
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({
        cards: state.cards, generatedOnce: state.generatedOnce
      }));
    } catch (e) {}
  }
  function findCard(id) {
    for (var i = 0; i < state.cards.length; i++) {
      if (state.cards[i].id === id) return state.cards[i];
    }
    return null;
  }
  function titleTaken(title, extra) {
    var t = String(title || '').toLowerCase();
    var i;
    for (i = 0; i < state.cards.length; i++) {
      if (String(state.cards[i].title || '').toLowerCase() === t) return true;
    }
    if (extra) {
      for (i = 0; i < extra.length; i++) {
        if (String(extra[i].title || '').toLowerCase() === t) return true;
      }
    }
    return false;
  }
  function makeCard(idea) {
    var now = new Date();
    return {
      id: newId(),
      title: idea.title,
      detail: idea.detail,
      effort: idea.effort,
      domain: idea.domain,
      created_at: now.toISOString(),
      expires_at: new Date(now.getTime() + RETIRE_MS).toISOString(),
      status: 'active',
      goal_id: null
    };
  }

  /* ---------- goal context ---------- */
  function cachedGoalSummaries() {
    try {
      var raw = JSON.parse(localStorage.getItem(GOALS_CACHE_KEY) || 'null');
      if (Array.isArray(raw)) return raw;
      if (raw && Array.isArray(raw.goals)) return raw.goals;
    } catch (e) {}
    return null;
  }
  /* GET /api/goals — resolves { status, goals } ; goals is null when the
   * endpoint gave us nothing usable, in which case the caller falls back
   * to the localStorage "il-goals-v1" summaries cache. */
  function fetchGoalSummaries() {
    return api(GOALS_API).then(function (out) {
      if (out.status === 401) return { status: 401, goals: null };
      if (out.data && Array.isArray(out.data.goals)) {
        return { status: out.status, goals: out.data.goals };
      }
      return { status: out.status, goals: cachedGoalSummaries() };
    }).catch(function () {
      return { status: 0, goals: cachedGoalSummaries() };
    });
  }
  function activeGoals(goals) {
    return (goals || []).filter(function (g) {
      return g && g.title && (!g.status || g.status === 'active');
    });
  }
  function goalContextText(goals) {
    var act = activeGoals(goals);
    if (!act.length) return 'The user has no tracked goals yet.';
    var lines = act.slice(0, 8).map(function (g) {
      var meta = DOMAIN_META[g.domain] || DOMAIN_META.general;
      return '- ' + String(g.title).slice(0, 120) + ' (' + meta.label + ')';
    });
    return 'The user is already working on these goals:\n' + lines.join('\n');
  }

  /* ---------- generation ----------
   * SERVER-ADAPTER: today generation is a prompt round-trip over the
   * LIVE /api/noah endpoint (below). When POST /api/ideas ships (see
   * QUEUED-UI-WORKER-PATCH.md), replace requestIdeas() with a call to
   * that endpoint returning the same validated [{title, detail, effort,
   * domain}] shape — the fallback, dedupe, and storage code stay. */
  function validateIdea(raw, batch) {
    if (!raw || typeof raw !== 'object') return null;
    var title = String(raw.title == null ? '' : raw.title).trim().slice(0, 90);
    var detail = String(raw.detail == null ? '' : raw.detail).trim().slice(0, 300);
    if (title.length < 3 || detail.length < 10) return null;
    var effort = EFFORTS.indexOf(raw.effort) >= 0 ? raw.effort : 'Quick';
    var domain = DOMAIN_META[raw.domain] ? raw.domain : 'general';
    if (titleTaken(title, batch)) return null;
    return { title: title, detail: detail, effort: effort, domain: domain };
  }
  function parseIdeas(reply) {
    if (Array.isArray(reply)) return reply;
    if (typeof reply !== 'string') return null;
    var start = reply.indexOf('[');
    var end = reply.lastIndexOf(']');
    if (start < 0 || end <= start) return null;
    try {
      var arr = JSON.parse(reply.slice(start, end + 1));
      return Array.isArray(arr) ? arr : null;
    } catch (e) { return null; }
  }
  function buildPrompt(goals) {
    var t = tutorName();
    return 'You are ' + t + ', a personal agent on the Interstitium Labs platform. ' +
      'Propose exactly 3 concrete ideas you could do FOR this user on this platform — ' +
      'things like tutoring plans, money help, health help, smart shopping help, ' +
      'relationship help, job-search help, and study systems. Build on what the ' +
      'user is already working on where it fits, and make each idea specific and ' +
      'actionable, not generic advice. Governance: you prepare and draft only — ' +
      'never propose autonomous sends, purchases, or bookings; anything like that ' +
      'is drafted for the user\'s approval.\n\n' +
      goalContextText(goals) + '\n\n' +
      'Return ONLY a JSON array of 3 objects, no other text, in exactly this shape: ' +
      '[{"title":"short idea title (max 90 characters)",' +
      '"detail":"2-3 sentences on what you would do (max 300 characters)",' +
      '"effort":"Quick" or "An afternoon" or "A project",' +
      '"domain":"learn" or "money" or "health" or "shopping" or "relationships" or "general" or "platform"}]';
  }
  function requestIdeas(goals) {
    return api(NOAH_API, {
      method: 'POST',
      body: {
        messages: [{ role: 'user', content: buildPrompt(goals) }],
        tutor: tutorId(),
        citations: false
      }
    }).then(function (out) {
      if (out.status === 401) return { status: 401, ideas: null };
      var parsed = parseIdeas(out.data && out.data.reply);
      if (!parsed) return { status: out.status, ideas: null };
      var batch = [];
      parsed.forEach(function (raw) {
        var v = validateIdea(raw, batch);
        if (v) batch.push(v);
      });
      return { status: out.status, ideas: batch.length ? batch.slice(0, 3) : null };
    }).catch(function () {
      return { status: 0, ideas: null };
    });
  }

  /* Deterministic fallback — used whenever the AI round-trip fails or
   * returns nothing usable. Derived only from the user's own active
   * goal domains/titles (never invents facts about the user) plus
   * platform staples that are always true. */
  var DOMAIN_TEMPLATES = {
    learn: {
      title: 'Study sprint plan',
      detail: '{tutor} turns "{goal}" into focused study sessions with short checks after each one, so progress is visible every sitting.',
      effort: 'An afternoon'
    },
    money: {
      title: 'Subscription sweep',
      detail: '{tutor} lists every recurring charge tied to "{goal}" and drafts the cancellations for your approval — nothing is cancelled without you.',
      effort: 'Quick'
    },
    health: {
      title: 'Gentle weekly health plan',
      detail: '{tutor} builds a realistic weekly routine around "{goal}" — small daily steps, a check-in rhythm, and adjustments when a week goes sideways.',
      effort: 'An afternoon'
    },
    shopping: {
      title: 'Smart shopping shortlist',
      detail: '{tutor} researches options for "{goal}", compares prices and trade-offs, and drafts a shortlist for your approval — nothing is bought without you.',
      effort: 'Quick'
    },
    relationships: {
      title: 'Stay-close drafts',
      detail: '{tutor} drafts thoughtful check-in messages and plans around "{goal}" for your review — you edit and send every one yourself.',
      effort: 'Quick'
    },
    general: {
      title: 'Next-step breakdown',
      detail: '{tutor} breaks "{goal}" into the next three concrete steps with a realistic order and pace, then tracks them with you.',
      effort: 'Quick'
    },
    platform: {
      title: 'Platform setup pass',
      detail: '{tutor} walks your Interstitium Labs setup for "{goal}" — profile, goals, and study tools — and drafts the fixes for your approval.',
      effort: 'Quick'
    }
  };
  var STAPLES = [
    {
      title: 'Verbal mock interview practice',
      detail: '{tutor} runs a spoken mock interview out loud, asks the follow-ups a real interviewer would, and gives honest feedback on each answer.',
      effort: 'An afternoon', domain: 'learn'
    },
    {
      title: 'Study-plan build',
      detail: '{tutor} builds you a study plan from the Interstitium Labs tracks — sequenced topics, daily targets, and review checkpoints that adapt as you go.',
      effort: 'An afternoon', domain: 'learn'
    },
    {
      title: 'Resume tailoring session',
      detail: '{tutor} tailors your resume to a role you paste in — matching keywords, tightening bullets, and drafting the cover letter for your approval.',
      effort: 'An afternoon', domain: 'general'
    }
  ];
  function fillTemplate(text, goalTitle) {
    return text
      .replace(/\{tutor\}/g, tutorName())
      .replace(/\{goal\}/g, goalTitle || 'your goal');
  }
  function fallbackIdeas(goals) {
    var pool = [];
    activeGoals(goals).forEach(function (g) {
      var tpl = DOMAIN_TEMPLATES[g.domain] || DOMAIN_TEMPLATES.general;
      pool.push({
        title: tpl.title,
        detail: fillTemplate(tpl.detail, String(g.title).slice(0, 80)),
        effort: tpl.effort,
        domain: DOMAIN_META[g.domain] ? g.domain : 'general'
      });
    });
    STAPLES.forEach(function (s) {
      pool.push({
        title: s.title,
        detail: fillTemplate(s.detail, ''),
        effort: s.effort,
        domain: s.domain
      });
    });
    var batch = [];
    pool.forEach(function (raw) {
      if (batch.length >= 3) return;
      var v = validateIdea(raw, batch);
      if (v) batch.push(v);
    });
    return batch;
  }

  function generate() {
    if (state.generating) return Promise.resolve();
    if (state.signedIn === false) { render(); return Promise.resolve(); }
    state.generating = true;
    render();
    var summariesP = state.goalSummaries
      ? Promise.resolve({ status: 200, goals: state.goalSummaries })
      : fetchGoalSummaries();
    return summariesP.then(function (ctxOut) {
      if (ctxOut.status === 401) {
        state.signedIn = false;
        state.generating = false;
        render();
        return null;
      }
      state.signedIn = true;
      if (ctxOut.goals) state.goalSummaries = ctxOut.goals;
      return requestIdeas(ctxOut.goals || []).then(function (out) {
        if (out.status === 401) {
          state.signedIn = false;
          return;
        }
        var ideas = out.ideas || fallbackIdeas(ctxOut.goals || []);
        ideas.forEach(function (idea) { state.cards.push(makeCard(idea)); });
        state.generatedOnce = true;
        saveStore();
      });
    }).catch(function () {
      /* Never hard-fail: fall back to the deterministic templates. */
      try {
        fallbackIdeas(state.goalSummaries || []).forEach(function (idea) {
          if (!titleTaken(idea.title)) state.cards.push(makeCard(idea));
        });
        state.generatedOnce = true;
        saveStore();
      } catch (e) {}
    }).then(function () {
      state.generating = false;
      render();
    });
  }

  /* ---------- sign-in check + first-open auto-generation ---------- */
  function ensureChecked() {
    if (state.checked) {
      if (state.signedIn === true && !state.generatedOnce) generate();
      return Promise.resolve();
    }
    if (state.checking) return state.checking;
    state.checking = fetchGoalSummaries().then(function (out) {
      state.checked = true;
      state.checking = null;
      if (out.status === 401) {
        state.signedIn = false;
      } else if (out.goals) {
        state.signedIn = true;
        state.goalSummaries = out.goals;
      }
      render();
      if (state.signedIn === true && !state.generatedOnce) generate();
    }).catch(function () {
      state.checked = true;
      state.checking = null;
      render();
    });
    return state.checking;
  }

  /* ---------- run / dismiss / discuss ---------- */
  function runCard(id) {
    var card = findCard(id);
    if (!card || card.status !== 'active' || state.running[id]) return;
    state.running[id] = true;
    delete state.cardErrors[id];
    render();
    api(GOALS_API, {
      method: 'POST',
      body: { text: card.title + ' — ' + card.detail }
    }).then(function (out) {
      delete state.running[id];
      if (out.status === 401) {
        state.signedIn = false;
        render();
        return;
      }
      var goal = out.data && (out.data.goal || out.data.goal || out.data);
      var goalId = goal && goal.id ? String(goal.id) : null;
      if ((out.status === 201 || out.status === 200) && goalId) {
        card.status = 'run';
        card.goal_id = goalId;
        saveStore();
      } else if (out.status === 201 || out.status === 200) {
        card.status = 'run';
        card.goal_id = null;
        saveStore();
      } else {
        state.cardErrors[id] = 'Could not create the goal' +
          (out.data && out.data.error ? ': ' + String(out.data.error) : ' (status ' + out.status + ')') +
          '. The idea is still here — try again.';
      }
      render();
    }).catch(function () {
      delete state.running[id];
      state.cardErrors[id] = 'Could not create the goal — the connection failed. The idea is still here — try again.';
      render();
    });
  }
  function dismissCard(id) {
    var card = findCard(id);
    if (!card) return;
    card.status = 'dismissed';
    delete state.cardErrors[id];
    saveStore();
    render();
  }
  function discussCard(id) {
    var card = findCard(id);
    if (!card) return;
    var text = card.title + ' — ' + card.detail;
    if (state.ctx && typeof state.ctx.discuss === 'function') {
      state.ctx.discuss(text);
    } else if (state.ctx && typeof state.ctx.go === 'function') {
      state.ctx.go('chat');
    }
  }
  function viewGoals() {
    if (state.ctx && typeof state.ctx.go === 'function') {
      state.ctx.go('goals');
    } else if (window.ILGoals && ILGoals.open) {
      ILGoals.open();
    }
  }

  /* ---------- render ---------- */
  function visibleCards() {
    var now = Date.now();
    return state.cards.filter(function (c) {
      if (c.status === 'dismissed') return false;
      if (isExpiredActive(c, now)) return false;
      return c.status === 'active' || c.status === 'run';
    }).slice().reverse(); /* newest first */
  }
  function cardHtml(card) {
    var meta = DOMAIN_META[card.domain] || DOMAIN_META.general;
    var h = '<article class="ili-card" data-ili-id="' + esc(card.id) + '">';
    h += '<h3>' + esc(card.title) + '</h3>';
    h += '<p class="ili-detail">' + esc(card.detail) + '</p>';
    h += '<div class="ili-chips">' +
      '<span class="ili-chip effort">' + esc(card.effort) + '</span>' +
      '<span class="ili-chip">' + meta.icon + ' ' + esc(meta.label) + '</span>';
    if (card.status === 'active') {
      h += '<span class="ili-chip">' + esc(retireLabel(card.expires_at)) + '</span>';
    }
    h += '</div>';
    if (card.status === 'run') {
      h += '<p class="ili-done">✓ Goal created</p>';
      h += '<div class="ili-actions">' +
        '<button type="button" class="primary" data-ili-act="goals">View in Goals</button></div>';
    } else {
      h += '<div class="ili-actions">' +
        '<button type="button" class="primary" data-ili-act="run"' +
        (state.running[card.id] ? ' disabled' : '') + '>' +
        (state.running[card.id] ? 'Creating goal…' : 'Let\'s do it') + '</button>' +
        '<button type="button" data-ili-act="discuss">💬 Discuss first</button>' +
        '<button type="button" class="ili-dismiss" data-ili-act="dismiss" aria-label="Dismiss this idea">Dismiss ✕</button>' +
        '</div>';
      if (state.cardErrors[card.id]) {
        h += '<p class="ili-error" role="alert">' + esc(state.cardErrors[card.id]) + '</p>';
      }
    }
    h += '</article>';
    return h;
  }
  function bind(root) {
    var newBtn = root.querySelector('[data-ili-new]');
    if (newBtn) newBtn.addEventListener('click', function () { generate(); });
    var cards = root.querySelectorAll('.ili-card');
    for (var i = 0; i < cards.length; i++) {
      (function (cardEl) {
        var id = cardEl.getAttribute('data-ili-id');
        var btns = cardEl.querySelectorAll('button[data-ili-act]');
        for (var j = 0; j < btns.length; j++) {
          (function (b) {
            b.addEventListener('click', function () {
              var act = b.getAttribute('data-ili-act');
              if (act === 'run') runCard(id);
              else if (act === 'dismiss') dismissCard(id);
              else if (act === 'discuss') discussCard(id);
              else if (act === 'goals') viewGoals();
            });
          })(btns[j]);
        }
      })(cards[i]);
    }
  }
  function render() {
    var root = state.root;
    if (!root) return;
    if (state.signedIn === false) {
      root.innerHTML = '<div class="ili-root"><p class="ili-empty ili-signin">' +
        'Ideas live in your account so ' + esc(tutorName()) + ' can suggest things ' +
        'built on your goals and carry them across every device. ' +
        '<a href="/account/">Sign in</a> to see ideas made for you.</p></div>';
      return;
    }
    var t = tutorName();
    var h = '<div class="ili-root">';
    h += '<div class="ili-head"><h2>💡 Ideas for you</h2>' +
      '<button type="button" class="ili-new" data-ili-new' +
      (state.generating ? ' disabled' : '') + '>' +
      (state.generating ? '✨ Thinking…' : '✨ New ideas') + '</button></div>';
    h += '<p class="ili-gov">Running an idea creates a tracked goal. <b>' + esc(t) +
      '</b> prepares and drafts — nothing is sent, bought, or booked without your approval.</p>';
    var vis = visibleCards();
    if (state.signedIn === null && !state.checked) {
      h += '<p class="ili-status">Loading your ideas…</p>';
    } else if (!vis.length) {
      h += '<div class="ili-empty"><p>No ideas right now. This is where ' + esc(t) +
        ' suggests concrete things it could build or do for you — a study plan, a ' +
        'subscription sweep, a shopping shortlist, a mock interview. Pick one and ' +
        'it becomes a tracked goal ' + esc(t) + ' works with you. Cards retire on ' +
        'their own after about two weeks.</p>' +
        '<p><button type="button" class="ili-new" data-ili-new' +
        (state.generating ? ' disabled' : '') + '>' +
        (state.generating ? '✨ Thinking…' : '✨ Generate ideas') + '</button></p></div>';
    } else {
      if (state.generating) h += '<p class="ili-status">' + esc(t) + ' is thinking up new ideas…</p>';
      h += '<div class="ili-grid">' + vis.map(cardHtml).join('') + '</div>';
    }
    h += '</div>';
    root.innerHTML = h;
    bind(root);
  }

  /* ---------- public contract ---------- */
  loadStore();
  window.ILIdeasView = {
    mount: function (el, ctx) {
      if (!el) return;
      state.root = el;
      if (ctx) state.ctx = ctx;
      render();
      ensureChecked();
    },
    unmount: function () {
      if (state.root) state.root.innerHTML = '';
      state.root = null;
      state.ctx = null;
    }
  };
})();
