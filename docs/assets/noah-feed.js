/* Noah/Genesis Feed — the personal Feed surface inside /noah/ (2026-10-11).
 *
 * Distilled from the Muse app's Feed semantics (see ~/docs/feed.md):
 * a personal feed of short posts written BY the tutor FOR the signed-in
 * user, steered by one plain-text brief. It is NOT an aggregator —
 * nothing is ingested or reposted from outside sources, there is no
 * source list to subscribe to, and no ranking algorithm decides what
 * the user sees. Every generated post is authored fresh by Noah/Genesis
 * over the live /api/noah, from the brief plus the user's OWN platform
 * data only (their goals and goal check-ins). Never outside sources,
 * never invented facts about the user.
 *
 * A separate views shell mounts this module:
 *   window.ILFeedView = { mount(el, ctx), unmount() }
 *   ctx = { tutor(): 'Noah'|'Genesis', discuss(text), go(viewName) }
 * mount() may be called repeatedly; module state is kept and the
 * surface re-renders into el each time.
 *
 * STORAGE: localStorage key 'il-feed-v1':
 *   { brief, briefUpdatedAt, units: [], seeded: bool, lastGenAt }
 * Units: { id, kicker, title, body, why, created_at, loved, seed }
 * (seed units also carry category: 'Getting started'.)
 *
 * SEED / BRIEF SEMANTICS (mirrors the reference Feed exactly):
 *   - On first run (no stored state) the feed is seeded with 5 intro
 *     posts — kicker AND category 'Getting started', seed: true —
 *     introducing (1) the Feed + how the brief steers it, (2) Goals,
 *     (3) Ideas, (4) Library, (5) Settings + the Secure Store. They are
 *     shipped with the build, written generically in the tutor's voice,
 *     and draw on NO user data. The `seeded` flag persists even if the
 *     user deletes every unit — a deleted seed stays deleted and the
 *     feed is never re-seeded.
 *   - The shipped DEFAULT BRIEF (below) is editable. Saving UNCHANGED
 *     text does nothing — no save, no generation. Saving CHANGED text
 *     saves and immediately generates one fresh post, prepended when
 *     ready. While the brief has never been edited, the brief shows as
 *     a full card with [Edit] + [Write a post now]; once edited, it
 *     collapses to a compact line in the header with [Edit brief]. An
 *     empty feed whose brief was edited shows 'Write a post now' again.
 *   - Lazy generation: on mount, if signed in and units exist and the
 *     newest unit is >24h old and lastGenAt is not today, one post is
 *     generated quietly (max once/day), prepended with no announcement.
 *   - Signed-out visitors (GET /api/goals -> 401, same detection as
 *     noah-goals.js) can still read the seeds; generation controls are
 *     replaced with a sign-in prompt linking /account/.
 *
 * STAGED SERVER UPGRADE: this store is local-first today. The key
 * 'il-feed-v1' is being registered as a cross-device sync store
 * server-side in a staged worker patch, and POST /api/feed lands in
 * QUEUED-UI-WORKER-PATCH.md. When that ships, the store adapter below
 * (marked SERVER-ADAPTER) is the single migration point — swap its
 * localStorage read/write for the server calls and nothing else in
 * this module changes. */
(function () {
  'use strict';
  if (window.ILFeedView) return;
  if (!document.getElementById('newChatBtn')) return; /* /noah/ only */

  var STORE_KEY = 'il-feed-v1';
  var GOALS_CACHE_KEY = 'il-goals-v1';
  var DAY_MS = 24 * 60 * 60 * 1000;

  var DEFAULT_BRIEF = 'Write short posts for me about my goals and learning on Interstitium Labs: progress on my goals, study focus for my courses and bootcamps, job-search momentum, and one useful idea at a time. Keep each post short, warm, and concrete. Never invent facts about me — write only from my goals and activity on this platform.';
  var SEED_WHY = 'Shipped with your feed to introduce it. Delete any of these and they stay deleted.';
  var DEFAULT_WHY = 'Written from your brief and your recent goal activity.';
  var GEN_ERROR = "Couldn't write a post just now — try again.";

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function todayStr() { return new Date().toISOString().slice(0, 10); }
  function nowIso() { return new Date().toISOString(); }
  function fmtDate(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d.getTime())) return String(iso).slice(0, 10);
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
  }
  function clamp(s, n) {
    s = String(s == null ? '' : s);
    return s.length > n ? s.slice(0, n) : s;
  }
  var idCounter = 0;
  function newId() {
    idCounter += 1;
    return 'ilf-' + Date.now().toString(36) + '-' + idCounter + '-' +
      Math.floor(Math.random() * 1e6).toString(36);
  }
  function tutorName() {
    if (state.ctx && typeof state.ctx.tutor === 'function') {
      try { return state.ctx.tutor() === 'Genesis' ? 'Genesis' : 'Noah'; } catch (e) {}
    }
    return apiTutorId() === 'genesis' ? 'Genesis' : 'Noah';
  }
  function apiTutorId() {
    try {
      var p = JSON.parse(localStorage.getItem('il-noah-profile') || '{}');
      return p && p.avatar === 'genesis' ? 'genesis' : 'noah';
    } catch (e) { return 'noah'; }
  }

  /* ---------------- Seeds ---------------- */
  function seedUnits() {
    var t = Date.now();
    function seed(i, title, body) {
      return {
        id: 'ilf-seed-' + (i + 1), kicker: 'Getting started', category: 'Getting started',
        title: title, body: body, why: SEED_WHY,
        created_at: new Date(t - i * 60000).toISOString(), loved: false, seed: true
      };
    }
    return [
      seed(0, 'Welcome to your Feed',
        'This is your Feed — a quiet stream of short posts written for you, by your tutor, right here on Interstitium Labs. Nothing here is pulled in from outside: no news wire, no social timeline, no algorithm deciding what you see. Every new post is written fresh, for you alone.\n\n' +
        'What steers it is your brief — the plain-text note pinned at the top of this page. It says what you want to hear about: your goals, your learning, your momentum. Edit the brief and the very next post follows it. Change it any time; saving a real change writes a fresh post straight away.\n\n' +
        'Each post is yours to keep or clear: love the ones that land, discuss any of them with me, move them up or down, or delete them. Ask me about any of it — I wrote it, and I am happy to explain why.'),
      seed(1, 'Goals: hand me one, I will help you carry it',
        'Goals are where I stop being just a tutor and start being your agent. Tell me an outcome — finish a course, prep for a bootcamp, build job-search momentum, save money, get healthier, stay close to someone — and I will turn it into a plan with steps, check-ins, and a next action that is always in front of you.\n\n' +
        'Your Feed and your goals feed each other: posts here can celebrate a finished step, nudge you on one that is due, or suggest a study focus for the week — always from your actual goals, never invented.\n\n' +
        'You can open Goals from the Noah panel, or simply tell me in chat: “I want to…” is all it takes to start one.'),
      seed(2, 'Ideas: one useful idea at a time',
        'Some posts in this Feed carry a single useful idea — a study technique, a way to frame a hard topic, a small experiment to try this week. The point is not volume; it is one idea you can actually use, at a pace you can absorb.\n\n' +
        'When an idea sparks something, hit Discuss on the post and we will develop it together in chat — stretch it, challenge it, or turn it into a goal. The ideas that land well, and the ones you love, teach me what to bring you more of.\n\n' +
        'And if an idea misses? Delete it and steer the brief. Your Feed gets sharper every time you react to it.'),
      seed(3, 'Your Library: everything you are learning, in one place',
        'The Library holds the material behind your learning: your courses and bootcamps on Interstitium Labs, your notes, and the PDF library of reference books and study guides.\n\n' +
        'Posts in this Feed can point you back into it — a chapter worth revisiting before a practice session, a reference that matches the goal you are working on, or a reminder of where you left off.\n\n' +
        'Think of it this way: the Library is what you know, Goals are where you are going, and this Feed is the gentle thread that keeps the two connected.'),
      seed(4, 'Settings and your Secure Store',
        'Settings is the control room for everything I can do for you: your account and profile, which tutor you talk to, your goals and reminders, memory controls, your files, and your privacy and data controls — including downloading or erasing your data.\n\n' +
        'At its center sits the Secure Store: a place to save logins for services you ask me to work with, encrypted on the server and never shown anywhere — not even here. You add a login once on a protected capture page, and from then on I can use it on your behalf without ever seeing or displaying the secret itself.\n\n' +
        'The rule everywhere, Secure Store included: I draft and prepare, you approve anything irreversible. Take a look around Settings when you are ready — and ask me about any of it.')
    ];
  }

  /* ---------------- Store ----------------
   * SERVER-ADAPTER: the single migration point for the staged server
   * upgrade. Today this reads/writes localStorage 'il-feed-v1'
   * (local-first). When POST /api/feed ships (see
   * QUEUED-UI-WORKER-PATCH.md) and 'il-feed-v1' is registered as a
   * cross-device sync store server-side, replace ONLY the bodies of
   * storeLoad()/storeSave() with the server calls — every other part
   * of this module talks to the store exclusively through them. */
  function storeLoad() {
    var raw = null;
    try { raw = localStorage.getItem(STORE_KEY); } catch (e) {}
    if (raw) {
      try {
        var parsed = JSON.parse(raw);
        if (parsed && typeof parsed === 'object' && parsed.units instanceof Array) {
          return {
            brief: typeof parsed.brief === 'string' ? parsed.brief : DEFAULT_BRIEF,
            briefUpdatedAt: parsed.briefUpdatedAt || null,
            units: parsed.units,
            seeded: !!parsed.seeded,
            lastGenAt: parsed.lastGenAt || null
          };
        }
      } catch (e) {}
    }
    /* First run: seed once. `seeded` persists from here on, even if the
       user deletes every unit — never re-seed. */
    var fresh = {
      brief: DEFAULT_BRIEF, briefUpdatedAt: null,
      units: seedUnits(), seeded: true, lastGenAt: null
    };
    storeSave(fresh);
    return fresh;
  }
  function storeSave(store) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(store)); } catch (e) {}
  }

  /* ---------------- Module state ---------------- */
  var state = {
    store: storeLoad(),
    el: null, ctx: null,
    signedIn: null, /* null=unknown, true, false */
    generating: false,
    genError: '',
    editingBrief: false,
    query: '',
    whyOpen: {},
    confirmDeleteId: null
  };
  function save() { storeSave(state.store); }
  function briefEdited() { return !!state.store.briefUpdatedAt; }

  /* ---------------- CSS ---------------- */
  var css = [
    '.ilf-wrap{color:var(--text,#e8e4da);font:inherit;line-height:1.5}',
    '.ilf-wrap *{box-sizing:border-box}',
    '.ilf-head{margin-bottom:1rem}',
    '.ilf-head h2{font-size:1.15rem;margin:0 0 .3rem}',
    '.ilf-sub{font-size:.85rem;color:var(--muted2,#9a958a);margin:0}',
    '.ilf-briefcard{border:1px solid rgba(201,162,39,.4);background:rgba(201,162,39,.07);border-radius:12px;padding:.9rem 1rem;margin-bottom:1rem}',
    '.ilf-briefcard .ilf-brief-label{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:#e6c95c;margin:0 0 .4rem;font-weight:700}',
    '.ilf-briefcard p.ilf-brief-text{margin:0 0 .7rem;font-size:.92rem;line-height:1.55}',
    '.ilf-brieflabel{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:#e6c95c;font-weight:700}',
    '.ilf-briefline{display:flex;gap:.6rem;align-items:flex-start;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.03);border-radius:12px;padding:.7rem .9rem;margin-bottom:1rem}',
    '.ilf-briefline p{margin:.15rem 0 0;font-size:.85rem;color:var(--muted2,#9a958a);flex:1;line-height:1.5}',
    '.ilf-actions{display:flex;gap:.45rem;flex-wrap:wrap;align-items:center}',
    '.ilf-btn{background:#c9a227;color:#0a0e1a;border:1px solid #c9a227;border-radius:8px;padding:.45rem .85rem;font:inherit;font-size:.85rem;font-weight:700;cursor:pointer}',
    '.ilf-btn.ghost{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14);color:inherit;font-weight:400}',
    '.ilf-btn.small{padding:.3rem .6rem;font-size:.8rem}',
    '.ilf-btn:disabled{opacity:.55;cursor:wait}',
    '.ilf-btn.danger{background:rgba(185,28,28,.18);border-color:rgba(185,28,28,.6);color:#fca5a5;font-weight:700}',
    '.ilf-link{color:#e6c95c}',
    '.ilf-editor{margin-bottom:1rem}',
    '.ilf-editor textarea{width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:10px;color:inherit;padding:.65rem .75rem;font:inherit;resize:vertical;min-height:110px}',
    '.ilf-editor .ilf-actions{margin-top:.55rem}',
    '.ilf-hint{font-size:.78rem;color:var(--muted2,#9a958a);margin:.45rem 0 0}',
    '.ilf-signin{border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.03);border-radius:12px;padding:.8rem .95rem;margin-bottom:1rem;font-size:.9rem}',
    '.ilf-signin p{margin:0}',
    '.ilf-error{color:#e08a8a;font-size:.85rem;margin:.5rem 0 0}',
    '.ilf-search{margin-bottom:1rem}',
    '.ilf-search input{width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:10px;color:inherit;padding:.55rem .75rem;font:inherit;font-size:.9rem}',
    '.ilf-card{border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:.85rem .95rem;margin-bottom:.8rem;background:rgba(255,255,255,.03)}',
    '.ilf-kicker{font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted2,#9a958a);margin:0 0 .3rem}',
    '.ilf-kicker b{color:#e6c95c;font-weight:700}',
    '.ilf-card h3{margin:0 0 .45rem;font-size:1rem;line-height:1.35}',
    '.ilf-body p{margin:0 0 .55rem;font-size:.9rem;line-height:1.6}',
    '.ilf-body p:last-child{margin-bottom:0}',
    '.ilf-why{margin:.65rem 0 0;border-top:1px dashed rgba(255,255,255,.08);padding-top:.55rem}',
    '.ilf-why p{margin:0;font-size:.82rem;color:var(--muted2,#9a958a);line-height:1.5}',
    '.ilf-card .ilf-actions{margin-top:.65rem}',
    '.ilf-love.loved{background:rgba(201,162,39,.18);border-color:#c9a227;color:#e6c95c}',
    '.ilf-empty{border:1px dashed rgba(255,255,255,.16);border-radius:12px;padding:1.1rem 1rem;text-align:center;color:var(--muted2,#9a958a);font-size:.9rem;line-height:1.55}',
    '.ilf-empty p{margin:0 0 .7rem}',
    '.ilf-noresults{color:var(--muted2,#9a958a);font-size:.9rem}'
  ].join('\n');
  if (!document.getElementById('il-feed-style')) {
    var style = document.createElement('style');
    style.id = 'il-feed-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  /* ---------------- API helpers ---------------- */
  function apiJson(path, opts) {
    opts = opts || {};
    return fetch(path, {
      method: opts.method || 'GET', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: opts.body != null ? JSON.stringify(opts.body) : undefined
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        return { status: res.status, data: data };
      });
    }).catch(function () { return { status: 0, data: {} }; });
  }

  function detectSignedIn() {
    return apiJson('/api/goals').then(function (out) {
      if (out.status === 401) state.signedIn = false;
      else if (out.status === 200) state.signedIn = true;
      return state.signedIn;
    });
  }

  /* Context for generation: ONLY the user's own platform data —
     /api/goals/checkin (due + brief) and /api/goals (summaries),
     falling back to the localStorage 'il-goals-v1' cache. */
  function gatherContext() {
    return Promise.all([
      apiJson('/api/goals/checkin'),
      apiJson('/api/goals')
    ]).then(function (outs) {
      var lines = [];
      var checkin = outs[0].data || {};
      var goalsOut = outs[1].data || {};
      if (checkin.brief) lines.push('Check-in brief: ' + checkin.brief);
      var due = checkin.due || [];
      due.slice(0, 6).forEach(function (d) {
        lines.push('Goal step due' + (d.overdue ? ' (overdue)' : '') + ': "' +
          (d.step || '') + '" for goal "' + (d.title || '') + '"' +
          (d.due ? ' (due ' + d.due + ')' : ''));
      });
      var goals = goalsOut.goals || [];
      if (!goals.length) {
        try {
          var cache = JSON.parse(localStorage.getItem(GOALS_CACHE_KEY) || '{}');
          if (cache && cache.goals instanceof Array) goals = cache.goals;
        } catch (e) {}
      }
      goals.slice(0, 8).forEach(function (g) {
        lines.push('Goal: "' + (g.title || '') + '"' +
          (g.domain ? ' (' + g.domain + ')' : '') +
          ', status ' + (g.status || 'active') +
          (typeof g.pct === 'number' ? ', ' + g.pct + '% complete' : '') +
          (g.next_action ? ', next action: ' + g.next_action : ''));
      });
      return lines;
    }).catch(function () { return []; });
  }

  function parsePost(reply, name) {
    var text = String(reply == null ? '' : reply);
    var start = text.indexOf('{');
    var end = text.lastIndexOf('}');
    if (start !== -1 && end > start) {
      try {
        var j = JSON.parse(text.slice(start, end + 1));
        if (j && (j.title || j.body)) {
          return {
            kicker: clamp(j.kicker || ('From ' + name), 60),
            title: clamp(j.title || 'A note for you', 120),
            body: clamp(j.body || '', 4000),
            why: clamp(j.why || DEFAULT_WHY, 300)
          };
        }
      } catch (e) {}
    }
    var lines = text.split('\n').filter(function (l) { return l.trim().length; });
    var title = lines.length ? lines[0].replace(/^#+\s*/, '').trim() : 'A note for you';
    var body = lines.slice(1).join('\n\n').trim() || text.trim();
    return {
      kicker: 'From ' + name, title: clamp(title, 120),
      body: clamp(body, 4000), why: DEFAULT_WHY
    };
  }

  /* The tutor writes: one post via the live /api/noah. On any failure
     this resolves null — never fabricate a post. */
  function generate(opts) {
    opts = opts || {};
    if (state.generating) return Promise.resolve(false);
    state.generating = true;
    state.genError = '';
    if (opts.claimDay) { state.store.lastGenAt = nowIso(); save(); }
    renderHeader();
    renderList();
    return gatherContext().then(function (lines) {
      var name = tutorName();
      var prompt = [
        'Write ONE short post for my personal Feed on Interstitium Labs. You are ' + name + ', my tutor, writing directly to me.',
        '',
        'My brief (what my Feed should be about):',
        state.store.brief,
        '',
        'Context from my own goals and activity on this platform — these are the ONLY facts you may use about me:',
        lines.length ? lines.join('\n') : '(No goal activity recorded yet. Write a gentle, general post that fits the brief without stating any facts about me.)',
        '',
        'Rules: never invent facts about me; write only from the brief and the context above. Keep it short, warm, and concrete. Return ONLY a JSON object, no markdown fences, no extra text:',
        '{"kicker": "a short category for the post", "title": "the post title", "body": "2-4 short paragraphs separated by blank lines", "why": "one sentence on why this post, for this user, now"}'
      ].join('\n');
      return apiJson('/api/noah', {
        method: 'POST',
        body: {
          messages: [{ role: 'user', content: prompt }],
          tutor: apiTutorId(),
          citations: false
        }
      }).then(function (out) {
        var reply = out.data && out.data.reply;
        if (out.status !== 200 || !reply || !String(reply).trim()) return false;
        var post = parsePost(reply, name);
        if (!post.body) return false;
        state.store.units.unshift({
          id: newId(), kicker: post.kicker, title: post.title, body: post.body,
          why: post.why, created_at: nowIso(), loved: false, seed: false
        });
        state.store.lastGenAt = nowIso();
        save();
        return true;
      });
    }).catch(function () { return false; }).then(function (ok) {
      state.generating = false;
      if (!ok && !opts.quiet) state.genError = GEN_ERROR;
      if (!ok && opts.quiet) state.genError = '';
      renderHeader();
      renderList();
      return ok;
    });
  }

  /* ---------------- Rendering ---------------- */
  function headerEl() { return state.el ? state.el.querySelector('.ilf-headslot') : null; }
  function listEl() { return state.el ? state.el.querySelector('.ilf-listslot') : null; }

  function writeBtnHtml(cls, label) {
    return '<button type="button" class="' + cls + '" data-ilf-write' +
      (state.generating ? ' disabled' : '') + '>' +
      (state.generating ? 'Writing…' : label) + '</button>';
  }
  function genControlsHtml() {
    if (state.signedIn === false) {
      return '<div class="ilf-signin"><p>Sign in so ' + esc(tutorName()) +
        ' can write new posts for you from your goals and activity. ' +
        '<a class="ilf-link" href="/account/">Sign in</a></p></div>';
    }
    return '';
  }
  function errorHtml() {
    return state.genError ? '<p class="ilf-error" role="alert">' + esc(state.genError) + '</p>' : '';
  }

  function renderHeader() {
    var host = headerEl();
    if (!host) return;
    var h = '';
    if (state.editingBrief) {
      h += '<div class="ilf-editor"><label class="ilf-brieflabel" for="ilfBriefText">Your brief</label>' +
        '<textarea id="ilfBriefText" maxlength="2000">' + esc(state.store.brief) + '</textarea>' +
        '<div class="ilf-actions">' +
        '<button type="button" class="ilf-btn" data-ilf-brief-save' + (state.generating ? ' disabled' : '') + '>Save brief</button>' +
        '<button type="button" class="ilf-btn ghost" data-ilf-brief-cancel>Cancel</button></div>' +
        '<p class="ilf-hint">Saving a changed brief writes a fresh post straight away. Re-saving the same text changes nothing.</p></div>';
    } else if (!briefEdited()) {
      /* Brief never edited: full prompt card with Edit + Write a post now. */
      h += '<div class="ilf-briefcard"><p class="ilf-brief-label">Your brief — what ' + esc(tutorName()) + ' writes about</p>' +
        '<p class="ilf-brief-text">' + esc(state.store.brief) + '</p>';
      if (state.signedIn === false) {
        h += '<div class="ilf-actions">' +
          '<button type="button" class="ilf-btn ghost" data-ilf-brief-edit>Edit</button></div>' +
          genControlsHtml();
      } else {
        h += '<div class="ilf-actions">' +
          '<button type="button" class="ilf-btn ghost" data-ilf-brief-edit>Edit</button>' +
          writeBtnHtml('ilf-btn', 'Write a post now') + '</div>';
      }
      h += errorHtml() + '</div>';
    } else {
      /* Brief edited: compact line in the header area + Edit brief. */
      h += '<div class="ilf-briefline"><div><span class="ilf-brieflabel">Your brief</span>' +
        '<p>' + esc(state.store.brief) + '</p></div>' +
        '<button type="button" class="ilf-btn ghost small" data-ilf-brief-edit>Edit brief</button></div>';
      if (state.signedIn === false) h += genControlsHtml();
      h += errorHtml();
    }
    host.innerHTML = h;
    bindHeader(host);
  }

  function bindHeader(host) {
    var editBtn = host.querySelector('[data-ilf-brief-edit]');
    if (editBtn) editBtn.addEventListener('click', function () {
      state.editingBrief = true; state.genError = ''; renderHeader();
      var ta = host.querySelector('#ilfBriefText');
      if (ta) ta.focus();
    });
    var cancelBtn = host.querySelector('[data-ilf-brief-cancel]');
    if (cancelBtn) cancelBtn.addEventListener('click', function () {
      state.editingBrief = false; renderHeader();
    });
    var saveBtn = host.querySelector('[data-ilf-brief-save]');
    if (saveBtn) saveBtn.addEventListener('click', function () {
      var ta = host.querySelector('#ilfBriefText');
      var text = ta ? ta.value.trim() : '';
      state.editingBrief = false;
      if (!text || text === state.store.brief) { renderHeader(); return; } /* unchanged: does nothing */
      state.store.brief = text;
      state.store.briefUpdatedAt = nowIso();
      save();
      renderHeader();
      if (state.signedIn !== false) generate({}); /* a real edit starts a fresh post */
    });
    var writeBtn = host.querySelector('[data-ilf-write]');
    if (writeBtn) writeBtn.addEventListener('click', function () { generate({}); });
  }

  function bodyHtml(body) {
    return String(body || '').split(/\n\s*\n|\n/).filter(function (p) {
      return p.trim().length;
    }).map(function (p) { return '<p>' + esc(p.trim()) + '</p>'; }).join('');
  }

  function cardHtml(u, idx, total) {
    var h = '<article class="ilf-card" data-ilf-id="' + esc(u.id) + '">';
    h += '<p class="ilf-kicker"><b>' + esc(u.kicker || '') + '</b> · ' + esc(fmtDate(u.created_at)) + '</p>';
    h += '<h3>' + esc(u.title) + '</h3>';
    h += '<div class="ilf-body">' + bodyHtml(u.body) + '</div>';
    if (u.why) {
      h += '<div class="ilf-why-slot">';
      if (state.whyOpen[u.id]) {
        h += '<div class="ilf-why"><p><b>Why this post:</b> ' + esc(u.why) + '</p></div>';
      }
      h += '</div>';
    }
    h += '<div class="ilf-actions">';
    h += '<button type="button" class="ilf-btn ghost small ilf-love' + (u.loved ? ' loved' : '') +
      '" data-ilf-love aria-pressed="' + (u.loved ? 'true' : 'false') + '">' + (u.loved ? '♥ Loved' : '♥ Love') + '</button>';
    h += '<button type="button" class="ilf-btn ghost small" data-ilf-discuss>💬 Discuss</button>';
    if (u.why) h += '<button type="button" class="ilf-btn ghost small" data-ilf-why>' + (state.whyOpen[u.id] ? 'Hide why' : 'Why this post') + '</button>';
    h += '<button type="button" class="ilf-btn ghost small" data-ilf-up' + (idx === 0 ? ' disabled' : '') + ' aria-label="Move post up">↑</button>';
    h += '<button type="button" class="ilf-btn ghost small" data-ilf-down' + (idx === total - 1 ? ' disabled' : '') + ' aria-label="Move post down">↓</button>';
    if (state.confirmDeleteId === u.id) {
      h += '<button type="button" class="ilf-btn small danger" data-ilf-delete>Tap again to delete</button>';
      h += '<button type="button" class="ilf-btn ghost small" data-ilf-delete-cancel>Keep</button>';
    } else {
      h += '<button type="button" class="ilf-btn ghost small" data-ilf-delete>Delete</button>';
    }
    h += '</div></article>';
    return h;
  }

  function renderList() {
    var host = listEl();
    if (!host) return;
    var units = state.store.units;
    var q = state.query.trim().toLowerCase();
    var visible = units.filter(function (u) {
      if (!q) return true;
      return (String(u.title || '').toLowerCase().indexOf(q) !== -1 ||
        String(u.body || '').toLowerCase().indexOf(q) !== -1);
    });
    var h = '';
    if (!units.length) {
      h += '<div class="ilf-empty"><p>Your feed is empty — every post here was written for you by ' +
        esc(tutorName()) + ', and the next one starts from your brief above.</p>';
      if (state.signedIn === false) h += genControlsHtml();
      else h += writeBtnHtml('ilf-btn', 'Write a post now');
      h += errorHtml() + '</div>';
    } else if (!visible.length) {
      h += '<p class="ilf-noresults">No posts match “' + esc(state.query) + '”.</p>';
    } else {
      h += visible.map(function (u) {
        return cardHtml(u, units.indexOf(u), units.length);
      }).join('');
    }
    host.innerHTML = h;
    var writeBtn = host.querySelector('[data-ilf-write]');
    if (writeBtn) writeBtn.addEventListener('click', function () { generate({}); });
    host.querySelectorAll('.ilf-card').forEach(function (card) {
      var id = card.getAttribute('data-ilf-id');
      function on(sel, fn) {
        var b = card.querySelector(sel);
        if (b) b.addEventListener('click', function () { fn(b); });
      }
      on('[data-ilf-love]', function () {
        var u = findUnit(id);
        if (u) { u.loved = !u.loved; save(); renderList(); }
      });
      on('[data-ilf-discuss]', function () {
        var u = findUnit(id);
        if (u && state.ctx && typeof state.ctx.discuss === 'function') {
          state.ctx.discuss('About this post from my Feed — "' + u.title + '":\n' + u.body);
        }
      });
      on('[data-ilf-why]', function () {
        state.whyOpen[id] = !state.whyOpen[id]; renderList();
      });
      on('[data-ilf-up]', function () { moveUnit(id, -1); });
      on('[data-ilf-down]', function () { moveUnit(id, 1); });
      on('[data-ilf-delete]', function () {
        if (state.confirmDeleteId === id) {
          state.store.units = state.store.units.filter(function (u) { return u.id !== id; });
          state.confirmDeleteId = null;
          save(); renderList();
        } else {
          state.confirmDeleteId = id; renderList();
        }
      });
      on('[data-ilf-delete-cancel]', function () {
        state.confirmDeleteId = null; renderList();
      });
    });
  }

  function findUnit(id) {
    for (var i = 0; i < state.store.units.length; i++) {
      if (state.store.units[i].id === id) return state.store.units[i];
    }
    return null;
  }
  function moveUnit(id, delta) {
    var units = state.store.units;
    for (var i = 0; i < units.length; i++) {
      if (units[i].id === id) {
        var j = i + delta;
        if (j < 0 || j >= units.length) return;
        var tmp = units[i]; units[i] = units[j]; units[j] = tmp;
        save(); renderList();
        return;
      }
    }
  }

  function render() {
    if (!state.el) return;
    state.el.innerHTML =
      '<div class="ilf-wrap">' +
      '<div class="ilf-head"><h2>📰 Your Feed</h2>' +
      '<p class="ilf-sub">Short posts written for you by ' + esc(tutorName()) +
      ', steered by your brief — nothing from outside sources, ever.</p></div>' +
      '<div class="ilf-headslot"></div>' +
      '<div class="ilf-search"><input type="search" data-ilf-search placeholder="Search past posts…" aria-label="Search past posts" value="' + esc(state.query) + '"></div>' +
      '<div class="ilf-listslot"></div>' +
      '</div>';
    var search = state.el.querySelector('[data-ilf-search]');
    if (search) search.addEventListener('input', function () {
      state.query = search.value;
      renderList(); /* list only — keeps focus in the search box */
    });
    renderHeader();
    renderList();
  }

  /* Lazy generation: once a day, quietly, only when the newest post
     is more than 24h old. No announcement — the post simply appears. */
  function maybeLazyGenerate() {
    if (state.signedIn !== true || state.generating) return;
    var units = state.store.units;
    if (!units.length) return;
    var newest = new Date(units[0].created_at).getTime();
    if (isNaN(newest) || Date.now() - newest <= DAY_MS) return;
    if (state.store.lastGenAt && String(state.store.lastGenAt).slice(0, 10) === todayStr()) return;
    generate({ quiet: true, claimDay: true });
  }

  /* ---------------- Public surface ---------------- */
  function mount(el, ctx) {
    if (!el) return;
    state.el = el;
    state.ctx = ctx || null;
    render();
    if (state.signedIn === null) {
      detectSignedIn().then(function () {
        if (!state.el) return;
        renderHeader();
        renderList();
        maybeLazyGenerate();
      });
    } else {
      maybeLazyGenerate();
    }
  }
  function unmount() {
    if (state.el) state.el.innerHTML = '';
    state.el = null;
    state.ctx = null;
  }

  window.ILFeedView = { mount: mount, unmount: unmount };
})();
