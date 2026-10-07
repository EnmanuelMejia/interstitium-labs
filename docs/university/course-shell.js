/* =====================================================================
 * Interstitium Labs — unified course shell (course-shell.js) v1.0
 *
 * Renders any course JSON (see COURSE-SCHEMA.md) into the 6-tab shell:
 * 01 Brief · 02 Plan · 03 Study · 04 Labs · 05 Mock · 06 More
 *
 * Progress: localStorage primary, keys `ilc:<courseId>:<key>`, merged to
 * PUT /api/progress when authed (graceful 401/503 → local-only).
 * Noah: embedded panels reuse window.IL.noahAI.ask (POST /api/noah).
 * No invented content: everything renders from the course document.
 * ===================================================================== */
(function () {
'use strict';

/* ============================== utils ============================== */
function $(sel, root) { return (root || document).querySelector(sel); }
function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* markdown-lite: **bold**, `code`, ```fences```, - lists. Everything else escaped. */
function mdLite(src) {
  var h = esc(src), blocks = [];
  h = h.replace(/```([\s\S]*?)```/g, function (m, code) {
    blocks.push('<pre><code>' + code.replace(/^\n/, '') + '</code></pre>');
    return '\u0000B' + (blocks.length - 1) + '\u0000';
  });
  h = h.replace(/`([^`\n]+)`/g, '<code>$1</code>');
  h = h.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  var lines = h.split('\n'), out = [], inList = false;
  lines.forEach(function (ln) {
    var m = ln.match(/^\s*[-*]\s+(.*)/);
    if (m) {
      if (!inList) { out.push('<ul>'); inList = true; }
      out.push('<li>' + m[1] + '</li>');
    } else {
      if (inList) { out.push('</ul>'); inList = false; }
      out.push(ln === '' ? '' : ('<p>' + ln + '</p>'));
    }
  });
  if (inList) out.push('</ul>');
  h = out.join('');
  h = h.replace(/\u0000B(\d+)\u0000/g, function (m, i) { return blocks[+i]; });
  return h;
}

function el(tag, cls, html) {
  var d = document.createElement(tag);
  if (cls) d.className = cls;
  if (html != null) d.innerHTML = html;
  return d;
}

function debounce(fn, ms) {
  var t = null;
  return function () {
    var a = arguments, self = this;
    clearTimeout(t);
    t = setTimeout(function () { fn.apply(self, a); }, ms);
  };
}

/* ============================== data =============================== */
var COURSE = null;

function readInlineData() {
  var node = document.getElementById('il-course-data');
  if (!node) return null;
  var txt = (node.textContent || '').trim();
  if (!txt) return null;
  try { return JSON.parse(txt); } catch (e) { return { __parseError: String(e) }; }
}

function queryParam(name) {
  try {
    var m = new RegExp('[?&]' + name + '=([^&]*)').exec(location.search);
    return m ? decodeURIComponent(m[1]) : null;
  } catch (e) { return null; }
}

function loadCourseData() {
  return new Promise(function (resolve) {
    var inline = readInlineData();
    if (inline) { resolve(inline); return; }
    var url = queryParam('data');
    if (!url) {
      var cid = (document.body && document.body.dataset && document.body.dataset.course) ||
        queryParam('course');
      if (cid) url = 'data/courses/' + cid + '.json';
    }
    if (!url) { resolve(null); return; }
    fetch(url, { credentials: 'same-origin' })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(resolve)
      .catch(function () { resolve(null); });
  });
}

function normCourse(raw) {
  var d = raw || {};
  var out = {
    schemaVersion: d.schemaVersion || '1.0',
    courseId: d.courseId || 'unknown-course',
    code: d.code || '',
    title: d.title || 'Untitled course',
    tagline: d.tagline || '',
    blurb: d.blurb || '',
    hours: d.hours || null,
    updatedAt: d.updatedAt || '',
    objectives: d.objectives || [],
    arc: d.arc || [],
    priorities: d.priorities || [],
    battlePlan: d.battlePlan || [],
    modules: d.modules || [],
    scriptLabs: d.scriptLabs || [],
    drills: d.drills || [],
    policyDrills: d.policyDrills || [],
    scenarios: d.scenarios || [],
    trainers: d.trainers || [],
    terminalSims: d.terminalSims || [],
    mockMinutes: d.mockMinutes || 60,
    mockTasks: d.mockTasks || [],
    cheatSheets: d.cheatSheets || [],
    answerBank: d.answerBank || [],
    sourceLinks: d.sourceLinks || [],
    honestyNote: d.honestyNote || ''
  };
  return out;
}

/* ============================== progress =========================== */
var Progress = (function () {
  var mem = {};
  var memOnly = false;
  try {
    localStorage.setItem('ilc:__probe', '1');
    localStorage.removeItem('ilc:__probe');
  } catch (e) { memOnly = true; }

  function prefix() { return 'ilc:' + (COURSE ? COURSE.courseId : 'unknown') + ':'; }
  function k(key) { return prefix() + key; }

  function get(key, dflt) {
    var raw = memOnly ? mem[k(key)] : null;
    try {
      if (!memOnly) raw = localStorage.getItem(k(key));
    } catch (e) { raw = mem[k(key)]; }
    return (raw == null) ? (dflt === undefined ? null : dflt) : raw;
  }
  function set(key, val) {
    var v = (val == null) ? null : String(val);
    try {
      if (memOnly) { if (v == null) delete mem[k(key)]; else mem[k(key)] = v; }
      else if (v == null) localStorage.removeItem(k(key));
      else localStorage.setItem(k(key), v);
    } catch (e) {
      if (v == null) delete mem[k(key)]; else mem[k(key)] = v;
    }
    Sync.markDirty();
  }
  function all() {
    var out = {}, p = prefix(), i, kk, v;
    if (!memOnly) {
      try {
        for (i = 0; i < localStorage.length; i++) {
          kk = localStorage.key(i);
          if (kk && kk.indexOf(p) === 0) {
            v = localStorage.getItem(kk);
            out[kk.slice(p.length)] = v;
          }
        }
      } catch (e) {}
    }
    for (kk in mem) {
      if (kk.indexOf(p) === 0) out[kk.slice(p.length)] = mem[kk];
    }
    return out;
  }
  function absorb(obj) {
    /* Server-side values fill gaps; local wins on conflict (local is primary). */
    if (!obj) return;
    var p = prefix(), key;
    for (key in obj) {
      if (!Object.prototype.hasOwnProperty.call(obj, key)) continue;
      if (get(key, null) == null && obj[key] != null) {
        try {
          if (memOnly) mem[p + key] = String(obj[key]);
          else localStorage.setItem(p + key, String(obj[key]));
        } catch (e) {}
      }
    }
  }
  return { get: get, set: set, all: all, absorb: absorb };
})();

/* ============================== server sync ======================== */
var Sync = (function () {
  var state = 'unknown'; /* unknown | authed | local */
  var dirty = false;
  var noteEl = null;

  function setNote(text) {
    if (noteEl) noteEl.textContent = text;
    var hdr = $('#sync-note');
    if (hdr) hdr.textContent = text;
  }

  var push = debounce(function () {
    if (state !== 'authed' || !dirty) return;
    dirty = false;
    var body;
    try {
      var doc = {};
      doc[COURSE.courseId] = Progress.all();
      body = JSON.stringify({ progress: doc });
    } catch (e) { return; }
    fetch('/api/progress', {
      method: 'PUT',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: body
    }).then(function (r) {
      if (r.status === 401 || r.status === 503) { state = 'local'; setNote('progress: this device only'); }
    }).catch(function () { /* stay dirty-capable; next change retries */ dirty = true; });
  }, 2500);

  function markDirty() { dirty = true; push(); }

  function init(noteTarget) {
    noteEl = noteTarget || null;
    fetch('/api/progress', { credentials: 'same-origin' })
      .then(function (r) {
        if (r.status === 401) { state = 'local'; setNote('progress: this device only (signed out)'); return null; }
        if (r.status === 503) { state = 'local'; setNote('progress: this device only (sync unavailable)'); return null; }
        if (!r.ok) { state = 'local'; setNote('progress: this device only'); return null; }
        return r.json();
      })
      .then(function (data) {
        if (!data || !data.ok) return;
        state = 'authed';
        setNote('progress: synced to your account');
        try {
          var doc = (data.progress || {})[COURSE.courseId];
          Progress.absorb(doc);
        } catch (e) {}
        refreshReadiness();
      })
      .catch(function () { state = 'local'; setNote('progress: this device only'); });
  }

  return { init: init, markDirty: markDirty };
})();

/* ============================== readiness ========================== */
function frac(done, total) { return total > 0 ? done / total : 0; }

function readiness() {
  var battle = COURSE.battlePlan;
  var mods = COURSE.modules;
  var labs = COURSE.scriptLabs.concat(COURSE.drills, COURSE.scenarios, COURSE.policyDrills);

  var bDone = battle.filter(function (b) { return Progress.get('battle:' + b.id) === '1'; }).length;

  var wTot = 0, wDone = 0;
  mods.forEach(function (m) {
    var w = (typeof m.weight === 'number' && m.weight > 0) ? m.weight : 1;
    wTot += w;
    if (Progress.get('module:' + m.id) === '1') wDone += w;
  });

  var lDone = 0;
  COURSE.scriptLabs.forEach(function (l) { if (Progress.get('lab:' + l.id) === 'done') lDone++; });
  COURSE.drills.forEach(function (d) { if (Progress.get('drill:' + d.id) === '1') lDone++; });
  COURSE.scenarios.forEach(function (s) { if (Progress.get('scenario:' + s.id) === '1') lDone++; });
  COURSE.policyDrills.forEach(function (p, i) { if (Progress.get('policy:' + i) === '1') lDone++; });

  var best = parseFloat(Progress.get('mock:best', '0')) || 0;

  var pct = frac(bDone, battle.length) * 20
    + frac(wDone, wTot) * 25
    + frac(lDone, labs.length) * 35
    + (Math.min(best, 80) / 80) * 20;
  return {
    pct: Math.round(Math.min(100, Math.max(0, pct))),
    parts: {
      battle: [bDone, battle.length], modules: [wDone, wTot],
      labs: [lDone, labs.length], mock: best
    }
  };
}

function ringSVG(pct) {
  var r = 84, c = 2 * Math.PI * r, off = c * (1 - pct / 100);
  return '<svg viewBox="0 0 200 200" width="210" height="210" role="img" aria-label="Readiness ' + pct + ' percent">' +
    '<circle cx="100" cy="100" r="' + r + '" fill="none" stroke="var(--panel3)" stroke-width="16"/>' +
    '<circle cx="100" cy="100" r="' + r + '" fill="none" stroke="url(#rg)" stroke-width="16" ' +
    'stroke-linecap="round" stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '" ' +
    'transform="rotate(-90 100 100)"/>' +
    '<defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">' +
    '<stop offset="0" stop-color="#c9a227"/><stop offset="1" stop-color="#62d8e9"/></linearGradient></defs></svg>';
}

function refreshReadiness() {
  var r = readiness();
  $all('[data-readiness-ring]').forEach(function (host) {
    host.innerHTML = ringSVG(r.pct) +
      '<div class="ring-num"><b>' + r.pct + '%</b><span>READY</span></div>';
  });
  $all('[data-readiness-legend]').forEach(function (host) {
    host.innerHTML = '<ul>' +
      '<li>Battle plan ' + r.parts.battle[0] + '/' + r.parts.battle[1] + ' — 20%</li>' +
      '<li>Modules ' + (Math.round(r.parts.modules[0] * 10) / 10) + '/' + (Math.round(r.parts.modules[1] * 10) / 10) + ' (weighted) — 25%</li>' +
      '<li>Labs ' + r.parts.labs[0] + '/' + r.parts.labs[1] + ' — 35%</li>' +
      '<li>Mock best ' + r.parts.mock + '% — 20%</li></ul>';
  });
}

/* ============================== chrome / router ==================== */
var TABS = [
  { id: 'brief', num: '01', label: 'Brief' },
  { id: 'plan', num: '02', label: 'Plan' },
  { id: 'study', num: '03', label: 'Study' },
  { id: 'labs', num: '04', label: 'Labs' },
  { id: 'mock', num: '05', label: 'Mock' },
  { id: 'more', num: '06', label: 'More' }
];
var activeTab = 'brief';

function renderChrome() {
  $('#hdr-code').textContent = COURSE.code || '';
  $('#hdr-code').title = COURSE.title;
  $('#ft-course').textContent = COURSE.title + (COURSE.code ? ' · ' + COURSE.code : '');

  var nav = $('#shell-nav'), mnav = $('#mobile-nav .row');
  nav.innerHTML = ''; mnav.innerHTML = '';
  TABS.forEach(function (t) {
    var a = el('a', '', '<span class="num">' + t.num + '</span><span>' + esc(t.label) + '</span>');
    a.href = '#/' + t.id;
    a.dataset.tab = t.id;
    a.setAttribute('role', 'tab');
    a.setAttribute('aria-selected', t.id === activeTab ? 'true' : 'false');
    if (t.id === activeTab) a.setAttribute('aria-current', 'page');
    nav.appendChild(a);
    var m = el('a', '', '<span class="num">' + t.num + '</span>' + esc(t.label));
    m.href = '#/' + t.id;
    m.dataset.tab = t.id;
    if (t.id === activeTab) m.setAttribute('aria-current', 'page');
    mnav.appendChild(m);
  });

  var main = $('#shell-main');
  main.innerHTML = '';
  TABS.forEach(function (t) {
    var s = el('section', 'shell-tab' + (t.id === activeTab ? ' active' : ''));
    s.id = 'tab-' + t.id;
    s.setAttribute('role', 'tabpanel');
    s.setAttribute('aria-label', t.label);
    main.appendChild(s);
  });
}

function showTab(id) {
  if (!TABS.some(function (t) { return t.id === id; })) id = 'brief';
  activeTab = id;
  $all('#shell-nav a, #mobile-nav a').forEach(function (a) {
    var on = a.dataset.tab === id;
    a.setAttribute('aria-selected', on ? 'true' : 'false');
    if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
  });
  $all('.shell-tab').forEach(function (s) { s.classList.toggle('active', s.id === 'tab-' + id); });
  var pane = $('#tab-' + id);
  if (pane && !pane.dataset.built) { pane.dataset.built = '1'; BUILDERS[id](pane); }
  if (id === 'brief') refreshReadiness();
  try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch (e) { window.scrollTo(0, 0); }
}

function route() {
  var m = /^#\/([a-z]+)/.exec(location.hash || '');
  showTab(m ? m[1] : 'brief');
}

/* ============================== Brief ============================== */
function heroHTML() {
  var dl = COURSE.updatedAt ? esc(COURSE.updatedAt) + ' · ' : '';
  var hours = COURSE.hours ? ' · ' + COURSE.hours + ' hours' : '';
  return '<div class="hero">' +
    '<div class="dateline">' + dl + esc(COURSE.code) + ' · SCIENTIA OMNIA VINCIT' + hours + '</div>' +
    '<h1>' + esc(COURSE.title) + '</h1>' +
    (COURSE.tagline ? '<p class="tagline">' + esc(COURSE.tagline) + '</p>' : '') +
    '</div>';
}

function buildBrief(root) {
  var totalMin = COURSE.battlePlan.reduce(function (s, b) { return s + (b.minutes || 0); }, 0);
  var html = heroHTML() +
    '<div class="brief-grid"><div class="card ring-card"><h2>Readiness</h2>' +
    '<div class="ring-wrap" data-readiness-ring></div>' +
    '<div class="ring-legend small" data-readiness-legend></div></div>' +
    '<div><div class="card"><h2>Brief</h2>' + mdLite(COURSE.blurb) + '</div>' +
    '<h2 class="section-title">Objectives</h2><ul class="obj-list">' +
    COURSE.objectives.map(function (o) { return '<li>' + esc(o) + '</li>'; }).join('') +
    '</ul></div></div>';
  if (COURSE.arc.length) {
    html += '<h2 class="section-title">Synthesis arc</h2><div class="arc-grid">' +
      COURSE.arc.map(function (a) {
        return '<div class="arc-card"><div class="phase">' + esc(String(a.phase)) + '</div>' +
          '<h3>' + esc(a.title) + '</h3><p>' + esc(a.body) + '</p></div>';
      }).join('') + '</div>';
  }
  if (COURSE.priorities.length) {
    var maxMin = Math.max.apply(null, COURSE.priorities.map(function (p) { return p.minutes || 0; }).concat([1]));
    html += '<h2 class="section-title">Priorities</h2><div class="card">' +
      COURSE.priorities.map(function (p) {
        var w = Math.round(((p.minutes || 0) / maxMin) * 100);
        return '<div class="pbar-row"><div class="pbar-top"><span>' + esc(p.label) +
          '</span><span class="minutes">' + (p.minutes || 0) + ' min</span></div>' +
          '<div class="pbar-track"><div class="pbar-fill" style="width:' + w + '%"></div></div></div>';
      }).join('') + '</div>';
  }
  root.innerHTML = html;
  refreshReadiness();
}

/* ============================== Plan =============================== */
function buildPlan(root) {
  var totalMin = COURSE.battlePlan.reduce(function (s, b) { return s + (b.minutes || 0); }, 0);
  var hours = Math.round(totalMin / 60 * 10) / 10;
  root.innerHTML = heroHTML() +
    '<h2 class="section-title">Battle plan</h2>' +
    '<p class="section-sub">Work the list in order. Check an item only when its work is genuinely done.</p>' +
    '<div class="cutline">Cut line: <b>' + totalMin + ' minutes</b> (' + hours + 'h) of focused work separates ' +
    'starting this course from finishing it. Everything below is sequenced — do not skip ahead.</div>' +
    '<div id="plan-list"></div>' +
    '<div class="card"><h2>Plan progress</h2><div class="pbar-row">' +
    '<div class="pbar-top"><span id="plan-frac"></span><span class="minutes" id="plan-min"></span></div>' +
    '<div class="pbar-track"><div class="pbar-fill" id="plan-bar"></div></div></div></div>';

  var list = $('#plan-list', root);
  COURSE.battlePlan.forEach(function (b) {
    var done = Progress.get('battle:' + b.id) === '1';
    var row = el('div', 'plan-item' + (done ? ' done' : ''));
    row.setAttribute('role', 'checkbox');
    row.setAttribute('aria-checked', done ? 'true' : 'false');
    row.setAttribute('tabindex', '0');
    row.innerHTML = '<span class="plan-check">' + (done ? '✓' : '') + '</span>' +
      '<span><span class="plan-title">' + esc(b.title) + '</span>' +
      (b.detail ? '<div class="plan-detail">' + esc(b.detail) + '</div>' : '') + '</span>' +
      '<span class="minutes">' + (b.minutes || 0) + ' min</span>';
    function toggle() {
      var now = !(Progress.get('battle:' + b.id) === '1');
      Progress.set('battle:' + b.id, now ? '1' : null);
      row.classList.toggle('done', now);
      row.setAttribute('aria-checked', now ? 'true' : 'false');
      row.querySelector('.plan-check').textContent = now ? '✓' : '';
      updatePlanBar(); refreshReadiness();
    }
    row.addEventListener('click', toggle);
    row.addEventListener('keydown', function (e) {
      if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggle(); }
    });
    list.appendChild(row);
  });

  function updatePlanBar() {
    var n = COURSE.battlePlan.length;
    var d = COURSE.battlePlan.filter(function (b) { return Progress.get('battle:' + b.id) === '1'; }).length;
    var mins = COURSE.battlePlan.filter(function (b) { return Progress.get('battle:' + b.id) === '1'; })
      .reduce(function (s, b) { return s + (b.minutes || 0); }, 0);
    $('#plan-frac', root).textContent = d + ' / ' + n + ' items complete';
    $('#plan-min', root).textContent = mins + ' / ' + totalMin + ' min banked';
    $('#plan-bar', root).style.width = (n ? Math.round(d / n * 100) : 0) + '%';
  }
  updatePlanBar();
}

/* ============================== Study ============================== */
function noteHTML(n) {
  var body = '<div class="fold-body">' + mdLite(n.body || '');
  if (n.code) body += '<pre><code>' + esc(n.code) + '</code></pre>';
  body += '</div>';
  return '<details class="fold"><summary>' + esc(n.title) + '</summary>' + body + '</details>';
}

function quizHTML(mod, qi, q) {
  var key = 'quiz:' + mod.id + ':' + qi;
  var chosen = Progress.get(key, null);
  var box = el('div', 'quiz' + (chosen != null ? ' answered' : ''));
  box.innerHTML = '<div class="q">Quick check ' + (qi + 1) + ': ' + esc(q.q) + '</div>';
  var opts = el('div');
  q.choices.forEach(function (c, ci) {
    var b = el('button', 'opt', esc(c));
    b.type = 'button';
    if (chosen != null) {
      b.disabled = true;
      if (ci === q.answer) b.classList.add('right');
      else if (String(ci) === String(chosen)) b.classList.add('wrong');
    }
    b.addEventListener('click', function () {
      Progress.set(key, String(ci));
      $all('.opt', opts).forEach(function (o, oi) {
        o.disabled = true;
        if (oi === q.answer) o.classList.add('right');
        else if (oi === ci) o.classList.add('wrong');
      });
      box.classList.add('answered');
      refreshReadiness();
    });
    opts.appendChild(b);
  });
  box.appendChild(opts);
  var why = el('div', 'why', '<b>Why:</b> ' + esc(q.explain || ''));
  box.appendChild(why);
  if (chosen != null) {
    var note = el('div', 'small muted mt', 'You answered: <b>' + esc(q.choices[+chosen] || '') + '</b> — ' +
      (+chosen === q.answer ? 'correct.' : 'review the explanation above.'));
    box.appendChild(note);
  }
  return box;
}

function flashcardHTML(mod, ci, card) {
  var key = 'card:' + mod.id + ':' + ci;
  var rated = Progress.get(key, null);
  var wrap = el('div', 'flash');
  wrap.innerHTML =
    '<div class="flash-stage" role="button" tabindex="0" aria-label="Flashcard ' + (ci + 1) + ': tap to flip">' +
    '<div class="flash-inner"><div class="flash-face">' + esc(card.front) + '</div>' +
    '<div class="flash-face flash-back">' + esc(card.back) + '</div></div></div>';
  var bar = el('div', 'flash-bar');
  bar.innerHTML = '<span class="count">' + (ci + 1) + ' / ' + mod.cards.length + '</span>' +
    (rated ? '<span class="small muted">rated: ' + esc(rated) + '</span>' : '') + '<span class="spacer"></span>';
  var know = el('button', 'btn rate-know', '✓ Know');
  var again = el('button', 'btn rate-again', '↻ Again');
  know.type = 'button'; again.type = 'button';
  know.addEventListener('click', function (e) { e.stopPropagation(); Progress.set(key, 'know'); flip(1); });
  again.addEventListener('click', function (e) { e.stopPropagation(); Progress.set(key, 'again'); flip(-1); });
  bar.appendChild(know); bar.appendChild(again);
  wrap.appendChild(bar);

  function flip(dir) {
    wrap.classList.toggle('flipped', false);
    /* pager: move to next/prev card within this module's deck */
    var deck = wrap.parentNode;
    var cards = $all('.flash', deck);
    var ix = cards.indexOf(wrap);
    var nx = ix + dir;
    if (nx >= 0 && nx < cards.length) {
      cards.forEach(function (c) { c.style.display = 'none'; });
      cards[nx].style.display = '';
      cards[nx].scrollIntoView({ block: 'nearest' });
    }
  }
  var stage = wrap.querySelector('.flash-stage');
  stage.addEventListener('click', function () { wrap.classList.toggle('flipped'); });
  stage.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); wrap.classList.toggle('flipped'); }
  });
  return wrap;
}

function moduleHTML(m) {
  var done = Progress.get('module:' + m.id) === '1';
  var wrap = el('div', 'mod');
  wrap.id = 'mod-' + m.id;
  var head = el('div', 'mod-head');
  head.setAttribute('role', 'button'); head.setAttribute('tabindex', '0');
  head.setAttribute('aria-expanded', 'false');
  head.innerHTML = (m.code ? '<span class="mod-code">' + esc(m.code) + '</span>' : '') +
    '<span class="mod-title">' + esc(m.title) + '</span>' +
    '<span class="mod-done-flag">' + (done ? '✓ complete' : '') + '</span>';
  var body = el('div', 'mod-body');
  body.style.display = 'none';
  var inner = '<p class="mod-summary">' + esc(m.summary || '') + '</p>';
  if ((m.objectives || []).length) {
    inner += '<ul class="obj-list">' + m.objectives.map(function (o) { return '<li>' + esc(o) + '</li>'; }).join('') + '</ul>';
  }
  if ((m.notes || []).length) {
    inner += '<h3>Notes</h3><div class="notes-list">' + m.notes.map(noteHTML).join('') + '</div>';
  }
  body.innerHTML = inner;
  if ((m.cards || []).length) {
    body.appendChild(el('h3', '', 'Flashcards'));
    var deck = el('div', 'flash-deck');
    m.cards.forEach(function (c, ci) {
      var f = flashcardHTML(m, ci, c);
      if (ci > 0) f.style.display = 'none';
      deck.appendChild(f);
    });
    body.appendChild(deck);
  }
  if ((m.quiz || []).length) {
    body.appendChild(el('h3', '', 'Quick checks'));
    m.quiz.forEach(function (q, qi) { body.appendChild(quizHTML(m, qi, q)); });
  }
  var foot = el('div', 'btn-row');
  var doneBtn = el('button', 'btn' + (done ? '' : ' primary'), done ? '✓ Module complete' : 'Mark module complete');
  doneBtn.type = 'button';
  doneBtn.addEventListener('click', function () {
    var now = !(Progress.get('module:' + m.id) === '1');
    Progress.set('module:' + m.id, now ? '1' : null);
    head.querySelector('.mod-done-flag').textContent = now ? '✓ complete' : '';
    doneBtn.textContent = now ? '✓ Module complete' : 'Mark module complete';
    doneBtn.classList.toggle('primary', !now);
    refreshReadiness();
  });
  foot.appendChild(doneBtn);
  body.appendChild(foot);
  wrap.appendChild(head); wrap.appendChild(body);

  function toggle() {
    var open = body.style.display === 'none';
    body.style.display = open ? '' : 'none';
    head.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  head.addEventListener('click', toggle);
  head.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
  });
  return wrap;
}

function buildStudy(root) {
  root.innerHTML = heroHTML() +
    '<h2 class="section-title">Study modules</h2>' +
    '<p class="section-sub">' + COURSE.modules.length + ' modules. Open a module, work its notes, ' +
    'flip the cards, pass the quick checks — then mark it complete.</p>' +
    '<div id="mod-list"></div>' +
    '<div id="study-noah"></div>';
  var list = $('#mod-list', root);
  COURSE.modules.forEach(function (m) { list.appendChild(moduleHTML(m)); });
  $('#study-noah', root).appendChild(noahPanel('Study — ' + COURSE.title, COURSE.title));
}

/* ============================== Noah embedded panel ================ */
/* Reuses the existing contract: window.IL.noahAI.ask(text, history) →
   Promise<{reply, remote, notice}>. No new API surface invented. */
function noahPanel(contextLabel, courseTitle) {
  var panel = el('div', 'noah-panel');
  panel.innerHTML =
    '<div class="noah-head"><img src="assets/noah-avatar.png" alt="Noah AI avatar">' +
    '<div><div class="nm">Noah — personalized tutor</div>' +
    '<div class="ds">Socratic, adaptive · grounded in this course' +
    (courseTitle ? ' · ' + esc(courseTitle) : '') + '</div></div></div>' +
    '<div class="noah-msgs" aria-live="polite"></div>' +
    '<form class="noah-form"><input type="text" placeholder="Ask Noah about this material…" ' +
    'aria-label="Ask Noah, the personalized tutor">' +
    '<button class="btn primary" type="submit">Ask</button></form>';
  var msgs = panel.querySelector('.noah-msgs');
  var form = panel.querySelector('.noah-form');
  var input = panel.querySelector('input');
  var hist = [];

  function addMsg(cls, html, notice) {
    var m = el('div', 'noah-m ' + cls, html);
    if (notice) m.appendChild(el('span', 'notice', esc(notice)));
    msgs.appendChild(m);
    msgs.scrollTop = msgs.scrollHeight;
  }
  addMsg('n', 'I am <b>Noah</b>, your personalized tutor for this course. Bring me a hypothesis ' +
    'or a stuck point — I will guide with questions before answers.');

  function typing(on) {
    var t = panel.querySelector('.noah-typing');
    if (on && !t) { msgs.appendChild(el('div', 'noah-typing', '<span></span><span></span><span></span>')); }
    if (!on && t) t.remove();
    msgs.scrollTop = msgs.scrollHeight;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var text = input.value.trim();
    if (!text) return;
    input.value = '';
    addMsg('u', esc(text));
    hist.push({ role: 'user', content: text });
    typing(true);
    var api = (window.IL && window.IL.noahAI) ? window.IL.noahAI : null;
    var ctxPrefix = '[' + contextLabel + '] ';
    function finish(reply, notice) {
      typing(false);
      addMsg('n', mdLite(reply), notice);
      hist.push({ role: 'assistant', content: reply });
    }
    if (api && api.ask) {
      api.ask(ctxPrefix + text, hist.slice(0, -1)).then(
        function (out) { finish(out.reply, out.remote ? null : out.notice); },
        function () { typing(false); addMsg('n', 'Noah is unreachable right now — try again in a moment.'); }
      );
    } else {
      typing(false);
      addMsg('n', 'The Noah tutor service is not loaded on this page yet. ' +
        'Reload the page; if this persists the endpoint is unreachable.');
    }
  });
  return panel;
}

/* ============================== Labs =============================== */
function buildLabs(root) {
  root.innerHTML = heroHTML() +
    '<h2 class="section-title">Labs</h2>' +
    '<p class="section-sub">Hands-on work. Script tasks validate required fragments; ' +
    'solutions unlock only after an attempt.</p>' +
    '<div class="lab-subnav" role="tablist" aria-label="Lab types"></div>' +
    '<div class="lab-panes"></div>' +
    '<div id="labs-noah"></div>';

  var panes = [];
  function addPane(id, label, builder) {
    panes.push({ id: id, label: label, builder: builder });
  }
  if (COURSE.terminalSims.length) addPane('term', 'Terminal', buildTermPane);
  if (COURSE.scriptLabs.length) addPane('script', 'Script labs', buildScriptPane);
  if (COURSE.drills.length) addPane('drills', 'Drills', buildDrillsPane);
  if (COURSE.scenarios.length) addPane('scen', 'Scenarios', buildScenPane);
  if (COURSE.trainers.length) addPane('train', 'Trainers', buildTrainerPane);
  if (COURSE.policyDrills.length) addPane('policy', 'Policy', buildPolicyPane);
  if (!panes.length) {
    root.innerHTML += '<div class="card"><p class="muted">This course ships no lab items yet — lab data arrives with the Phase 2 course document.</p></div>';
  }

  var nav = $('.lab-subnav', root), holder = $('.lab-panes', root);
  panes.forEach(function (p, i) {
    var b = el('button', 'btn' + (i === 0 ? ' on' : ''), esc(p.label));
    b.type = 'button'; b.setAttribute('role', 'tab');
    b.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
    var pane = el('div', 'lab-pane' + (i === 0 ? ' on' : ''));
    pane.setAttribute('role', 'tabpanel');
    p.builder(pane);
    holder.appendChild(pane);
    b.addEventListener('click', function () {
      $all('.btn', nav).forEach(function (x) { x.classList.remove('on'); x.setAttribute('aria-selected', 'false'); });
      $all('.lab-pane', holder).forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on'); b.setAttribute('aria-selected', 'true'); pane.classList.add('on');
    });
    nav.appendChild(b);
  });
  $('#labs-noah', root).appendChild(noahPanel('Labs — ' + COURSE.title, COURSE.title));
}

/* ---- Terminal simulators ---- */
function buildTermPane(root) {
  COURSE.terminalSims.forEach(function (sim) {
    var card = el('div', 'scriptlab');
    card.innerHTML = '<h3>' + esc(sim.title) + '</h3><p class="muted small">' + esc(sim.brief || '') + '</p>';
    var term = el('div', 'term');
    var screen = el('div', 'term-screen');
    var row = el('div', 'term-input-row');
    row.innerHTML = '<span class="term-prompt">' + esc(sim.prompt || 'learner@il:~$') + '</span>';
    var input = document.createElement('input');
    input.className = 'term-input'; input.setAttribute('aria-label', 'Terminal input for ' + sim.title);
    input.setAttribute('autocomplete', 'off'); input.setAttribute('spellcheck', 'false');
    row.appendChild(input);
    term.appendChild(screen); term.appendChild(row);
    card.appendChild(term);
    root.appendChild(card);

    var hist = [], hi = -1;
    var cmds = {};
    (sim.commands || []).forEach(function (c) { cmds[c.cmd.trim()] = c.out; });

    function print(t) { screen.textContent += t + '\n'; screen.scrollTop = screen.scrollHeight; }
    print('# ' + sim.title);
    print('# type "help" to list available commands');
    if (!Progress.get('term:' + sim.id)) Progress.set('term:' + sim.id, 'seen');

    function suggest(raw) {
      var best = null, bs = 3;
      Object.keys(cmds).forEach(function (c) {
        var d = lev(raw, c);
        if (d < bs) { bs = d; best = c; }
      });
      return best;
    }
    function lev(a, b) {
      var m = a.length, n = b.length, dp = [];
      for (var i = 0; i <= m; i++) { dp[i] = [i]; }
      for (var j = 0; j <= n; j++) { dp[0][j] = j; }
      for (i = 1; i <= m; i++) for (j = 1; j <= n; j++)
        dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      return dp[m][n];
    }

    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (hist.length) { hi = hi < 0 ? hist.length - 1 : Math.max(0, hi - 1); input.value = hist[hi]; }
        return;
      }
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (hi >= 0) { hi++; input.value = hi >= hist.length ? '' : hist[hi]; if (hi >= hist.length) hi = -1; }
        return;
      }
      if (e.key !== 'Enter') return;
      var raw = input.value.trim();
      print((sim.prompt || 'learner@il:~$') + ' ' + raw);
      input.value = ''; hi = -1;
      if (!raw) return;
      hist.push(raw);
      if (raw === 'help') {
        print('available commands:\n  ' + Object.keys(cmds).join('\n  '));
        return;
      }
      if (raw === 'clear') { screen.textContent = ''; return; }
      if (Object.prototype.hasOwnProperty.call(cmds, raw)) { print(cmds[raw]); return; }
      var s = suggest(raw);
      print('command not found: ' + raw + (s ? '\ndid you mean: ' + s + ' ?' : ''));
    });
    term.addEventListener('click', function () { input.focus(); });
  });
}

/* ---- Script / code labs ---- */
function checkFragments(text, required) {
  return (required || []).map(function (frag) {
    return { frag: frag, met: text.indexOf(frag) !== -1 };
  });
}

function buildScriptPane(root) {
  COURSE.scriptLabs.forEach(function (lab) {
    var card = el('div', 'scriptlab');
    var done = Progress.get('lab:' + lab.id) === 'done';
    var attempted = Progress.get('lab:' + lab.id + ':attempted') === '1';
    card.innerHTML = '<h3>' + esc(lab.title) + ' ' +
      (done ? '<span class="pill">✓ done</span>' : '') + '</h3>' +
      '<div class="small">' + mdLite(lab.brief || '') + '</div>';
    var ta = document.createElement('textarea');
    ta.className = 'code-editor';
    ta.value = Progress.get('labdraft:' + lab.id, lab.starter || '');
    ta.setAttribute('aria-label', 'Code editor for ' + lab.title);
    card.appendChild(ta);
    var reqBox = el('ul', 'req-list');
    card.appendChild(reqBox);
    var verdict = el('div', 'lab-verdict');
    card.appendChild(verdict);
    var row = el('div', 'btn-row');
    var submit = el('button', 'btn primary', 'Run validation');
    var hintBtn = el('button', 'btn ghost', 'Hint');
    var solBtn = el('button', 'btn ghost', 'Reveal solution');
    submit.type = 'button'; hintBtn.type = 'button'; solBtn.type = 'button';
    row.appendChild(submit); row.appendChild(hintBtn); row.appendChild(solBtn);
    card.appendChild(row);
    var hint = el('div', 'hint-box', '<b>Hint:</b> ' + esc(lab.hint || 'No hint for this lab.'));
    card.appendChild(hint);
    var sol = el('div', 'solution-box');
    sol.innerHTML = '<h3>Solution</h3><pre><code>' + esc(lab.solution || '') + '</code></pre>';
    card.appendChild(sol);
    root.appendChild(card);

    function paint() {
      var res = checkFragments(ta.value, lab.required);
      reqBox.innerHTML = '';
      res.forEach(function (r) {
        var li = el('li', r.met ? 'met' : '', esc(r.frag));
        reqBox.appendChild(li);
      });
      return res;
    }
    ta.addEventListener('input', function () {
      Progress.set('labdraft:' + lab.id, ta.value);
      paint();
    });
    paint();

    submit.addEventListener('click', function () {
      var res = paint();
      attempted = true;
      Progress.set('lab:' + lab.id + ':attempted', '1');
      var allMet = res.length === 0 || res.every(function (r) { return r.met; });
      verdict.textContent = allMet
        ? '✓ All required fragments present — lab complete.'
        : '✗ ' + res.filter(function (r) { return !r.met; }).length + ' required fragment(s) still missing.';
      verdict.className = 'lab-verdict ' + (allMet ? 'ok' : '');
      if (allMet && Progress.get('lab:' + lab.id) !== 'done') {
        Progress.set('lab:' + lab.id, 'done');
        card.querySelector('h3').insertAdjacentHTML('beforeend', ' <span class="pill">✓ done</span>');
        refreshReadiness();
      }
    });
    hintBtn.addEventListener('click', function () { hint.classList.toggle('show'); });
    solBtn.addEventListener('click', function () {
      if (!attempted) {
        verdict.textContent = 'Submit at least one attempt before the solution unlocks.';
        verdict.className = 'lab-verdict';
        return;
      }
      sol.classList.toggle('show');
    });
  });
}

/* ---- Drills + Policy ---- */
function drillCard(item, key) {
  var done = Progress.get(key) === '1';
  var card = el('div', 'drill');
  card.innerHTML = '<div class="prompt">' + esc(item.title || item.prompt || 'Drill') + '</div>' +
    (item.prompt && item.title ? '<div class="small muted">' + esc(item.prompt) + '</div>' : '') +
    (item.snippet ? '<pre><code>' + esc(item.snippet) + '</code></pre>' : '');
  if (done) card.insertAdjacentHTML('beforeend', '<div class="small" style="color:var(--green)">✓ answered correctly</div>');
  var opts = el('div');
  (item.choices || []).forEach(function (c, ci) {
    var b = el('button', 'opt btn ghost', esc(c));
    b.type = 'button';
    b.style.display = 'block'; b.style.width = '100%'; b.style.textAlign = 'left'; b.style.margin = '6px 0';
    if (done) b.disabled = true;
    b.addEventListener('click', function () {
      var right = ci === item.answer;
      $all('button', opts).forEach(function (o) { o.disabled = true; });
      b.style.borderColor = right ? 'var(--green)' : 'var(--red)';
      $all('button', opts).forEach(function (o, oi) {
        if (oi === item.answer) o.style.borderColor = 'var(--green)';
      });
      var why = el('div', 'small muted mt', '<b>Why:</b> ' + esc(item.explain || ''));
      card.appendChild(why);
      if (right) {
        Progress.set(key, '1');
        card.insertAdjacentHTML('beforeend', '<div class="small" style="color:var(--green)">✓ correct</div>');
        refreshReadiness();
      }
    });
    opts.appendChild(b);
  });
  card.appendChild(opts);
  return card;
}

function buildDrillsPane(root) {
  COURSE.drills.forEach(function (d, i) { root.appendChild(drillCard(d, 'drill:' + (d.id || i))); });
}
function buildPolicyPane(root) {
  root.appendChild(el('p', 'section-sub', 'Control decisions — choose the action a defender should take.'));
  COURSE.policyDrills.forEach(function (d, i) { root.appendChild(drillCard(d, 'policy:' + i)); });
}

/* ---- Scenarios (decision trees) ---- */
function buildScenPane(root) {
  COURSE.scenarios.forEach(function (sc) {
    var done = Progress.get('scenario:' + sc.id) === '1';
    var card = el('div', 'scriptlab');
    card.innerHTML = '<h3>' + esc(sc.title) + ' ' + (done ? '<span class="pill">✓ done</span>' : '') + '</h3>' +
      '<div class="small">' + mdLite(sc.context || '') + '</div>';
    var stepsHost = el('div');
    card.appendChild(stepsHost);
    root.appendChild(card);

    function renderStep(si) {
      stepsHost.innerHTML = '';
      var step = sc.steps[si];
      var box = el('div', 'scn-step');
      box.innerHTML = '<div class="prompt"><b>Step ' + (si + 1) + ' of ' + sc.steps.length + ':</b> ' +
        esc(step.prompt) + '</div>';
      step.options.forEach(function (op, oi) {
        var b = el('button', 'btn ghost', esc(op.text));
        b.type = 'button';
        b.style.display = 'block'; b.style.width = '100%'; b.style.textAlign = 'left'; b.style.margin = '6px 0';
        b.addEventListener('click', function () {
          $all('button', box).forEach(function (o) { o.disabled = true; });
          b.style.borderColor = op.correct ? 'var(--green)' : 'var(--red)';
          box.classList.add('chosen');
          box.querySelector('.scn-why').textContent = (op.correct ? '✓ ' : '✗ ') + (op.why || '');
          Progress.set('scenario:' + sc.id + ':' + si, String(oi));
          var nav = el('div', 'btn-row');
          if (si + 1 < sc.steps.length) {
            var nx = el('button', 'btn primary', 'Next step →');
            nx.type = 'button';
            nx.addEventListener('click', function () { renderStep(si + 1); });
            nav.appendChild(nx);
          } else {
            var fin = el('button', 'btn primary', 'Finish scenario');
            fin.type = 'button';
            fin.addEventListener('click', function () {
              Progress.set('scenario:' + sc.id, '1');
              card.querySelector('h3').insertAdjacentHTML('beforeend', ' <span class="pill">✓ done</span>');
              refreshReadiness();
              stepsHost.innerHTML = '<div class="card"><p><b>Scenario complete.</b> Review the why-explanations above — they are the lesson.</p></div>';
            });
            nav.appendChild(fin);
          }
          box.appendChild(nav);
        });
        box.appendChild(b);
      });
      box.appendChild(el('p', 'scn-why', ''));
      stepsHost.appendChild(box);
    }
    renderStep(0);
  });
}

/* ---- Trainers ---- */
function cidrTrainer(t, root) {
  var card = el('div', 'trainer');
  card.innerHTML = '<h3>' + esc(t.title) + '</h3><p class="small muted">' + esc(t.brief || '') + '</p>';
  var q = el('div', 'mono', '');
  q.style.fontSize = '18px'; q.style.margin = '10px 0';
  card.appendChild(q);
  var fields = el('div', 'fields');
  var defs = [
    ['network', 'Network address'], ['broadcast', 'Broadcast address'],
    ['hosts', 'Usable hosts'], ['mask', 'Subnet mask (dotted)']
  ];
  var inputs = {};
  defs.forEach(function (d) {
    var lab = el('label', '', d[1]);
    var inp = document.createElement('input');
    inp.setAttribute('aria-label', d[1]);
    lab.appendChild(inp);
    fields.appendChild(lab);
    inputs[d[0]] = inp;
  });
  card.appendChild(fields);
  var streak = el('div', 'streak-line', '');
  card.appendChild(streak);
  var row = el('div', 'btn-row');
  var check = el('button', 'btn primary', 'Check');
  var next = el('button', 'btn ghost', 'New address');
  check.type = 'button'; next.type = 'button';
  row.appendChild(check); row.appendChild(next);
  card.appendChild(row);
  root.appendChild(card);

  var cur = null;
  function paintStreak() {
    var s = parseInt(Progress.get('trainer:' + t.id + ':streak', '0'), 10) || 0;
    var b = parseInt(Progress.get('trainer:' + t.id + ':best', '0'), 10) || 0;
    streak.textContent = 'streak: ' + s + ' · best: ' + b;
  }
  function maskToDotted(m) {
    var bits = [], i;
    for (i = 0; i < 4; i++) { bits.push((m >> (24 - i * 8)) & 255); }
    return bits.join('.');
  }
  function newQ() {
    var a = 1 + Math.floor(Math.random() * 223);
    var b = Math.floor(Math.random() * 256), c = Math.floor(Math.random() * 256), d = Math.floor(Math.random() * 256);
    var p = 8 + Math.floor(Math.random() * 23); /* /8–/30 */
    var ip = ((a << 24) | (b << 16) | (c << 8) | d) >>> 0;
    var mask = p === 0 ? 0 : (0xFFFFFFFF << (32 - p)) >>> 0;
    var net = (ip & mask) >>> 0;
    var bc = (net | (~mask >>> 0)) >>> 0;
    function dotted(n) { return [(n >>> 24) & 255, (n >>> 16) & 255, (n >>> 8) & 255, n & 255].join('.'); }
    var hostBits = 32 - p;
    var hosts = hostBits <= 1 ? 0 : Math.pow(2, hostBits) - 2;
    cur = { network: dotted(net), broadcast: dotted(bc), hosts: String(hosts), mask: maskToDotted(mask) };
    q.textContent = dotted(ip) + '/' + p;
    Object.keys(inputs).forEach(function (k) {
      inputs[k].value = '';
      inputs[k].classList.remove('right', 'wrong');
    });
  }
  check.addEventListener('click', function () {
    if (!cur) return;
    var allOk = true;
    Object.keys(inputs).forEach(function (k) {
      var ok = inputs[k].value.trim() === cur[k];
      inputs[k].classList.toggle('right', ok);
      inputs[k].classList.toggle('wrong', !ok);
      if (!ok) allOk = false;
    });
    var s = parseInt(Progress.get('trainer:' + t.id + ':streak', '0'), 10) || 0;
    var b = parseInt(Progress.get('trainer:' + t.id + ':best', '0'), 10) || 0;
    s = allOk ? s + 1 : 0;
    if (s > b) b = s;
    Progress.set('trainer:' + t.id + ':streak', String(s));
    Progress.set('trainer:' + t.id + ':best', String(b));
    paintStreak();
    if (allOk) setTimeout(newQ, 900);
  });
  next.addEventListener('click', newQ);
  paintStreak();
  newQ();
}

function buildTrainerPane(root) {
  COURSE.trainers.forEach(function (t) {
    if (t.kind === 'cidr') { cidrTrainer(t, root); return; }
    var card = el('div', 'trainer');
    card.innerHTML = '<h3>' + esc(t.title) + '</h3><p class="small muted">' + esc(t.brief || '') + '</p>' +
      '<p class="small">Trainer kind <code>' + esc(t.kind || 'custom') + '</code> ships with the Phase 2 course document.</p>';
    root.appendChild(card);
  });
}

/* ============================== Mock =============================== */
var Mock = (function () {
  var S = null; /* {t0, acc, running, answers, flags, cur} */
  var totalSec = 60 * 60;

  function load() {
    try {
      var raw = Progress.get('mock:session', null);
      S = raw ? JSON.parse(raw) : null;
    } catch (e) { S = null; }
    if (!S) S = { t0: 0, acc: 0, running: false, answers: {}, flags: [], cur: 0, started: false };
    if (!S.answers) S.answers = {};
    if (!S.flags) S.flags = [];
    return S;
  }
  function save() { Progress.set('mock:session', JSON.stringify(S)); }
  function clear() { S = { t0: 0, acc: 0, running: false, answers: {}, flags: [], cur: 0, started: false }; Progress.set('mock:session', null); }

  function elapsed() {
    if (!S.started) return 0;
    var e = S.acc;
    if (S.running) e += (Date.now() - S.t0) / 1000;
    return e;
  }
  function remaining() { return Math.max(0, totalSec - elapsed()); }

  return { load: load, save: save, clear: clear, elapsed: elapsed, remaining: remaining,
    get S() { return S; },
    set total(s) { totalSec = s; }, get total() { return totalSec; } };
})();

function fmtTime(sec) {
  sec = Math.max(0, Math.ceil(sec));
  var h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
  function p(n) { return (n < 10 ? '0' : '') + n; }
  return p(h) + ':' + p(m) + ':' + p(s);
}

function buildMock(root) {
  Mock.total = (COURSE.mockMinutes || 60) * 60;
  Mock.load();
  var best = parseFloat(Progress.get('mock:best', '0')) || 0;
  var sessions = parseInt(Progress.get('mock:sessions', '0'), 10) || 0;

  root.innerHTML = heroHTML() +
    '<h2 class="section-title">Mock assessment</h2>' +
    '<p class="section-sub">' + COURSE.mockTasks.length + ' tasks · ' + COURSE.mockMinutes +
    ' minutes · timed. Flag tasks for review; your best score feeds the readiness ring.</p>' +
    '<div class="mock-head"><div class="mock-timer" id="mock-clock" aria-live="off">--:--:--</div>' +
    '<div class="btn-row" style="margin:0"><button class="btn primary" id="mock-start" type="button">Start</button>' +
    '<button class="btn ghost" id="mock-pause" type="button">Pause</button>' +
    '<button class="btn danger" id="mock-reset" type="button">Reset</button></div>' +
    '<span class="small muted" id="mock-meta">best: ' + best + '% · sessions: ' + sessions + '</span></div>' +
    '<div class="qmap" id="mock-qmap" aria-label="Question map"></div>' +
    '<div id="mock-tasks"></div>' +
    '<div class="btn-row"><button class="btn primary" id="mock-finish" type="button">Finish &amp; score</button></div>' +
    '<div id="mock-result"></div>';

  var clock = $('#mock-clock', root);
  var timerId = null;

  function paintClock() {
    var r = Mock.remaining();
    clock.textContent = fmtTime(r);
    clock.classList.toggle('low', r < 300 && r > 0);
    clock.setAttribute('aria-live', r < 60 ? 'polite' : 'off');
    if (r <= 0 && Mock.S.running) finish(true);
  }
  function tick() { paintClock(); }

  function setRunning(on) {
    var S = Mock.S;
    if (on && !S.running) {
      if (!S.started) S.started = true;
      S.t0 = Date.now(); S.running = true;
      timerId = setInterval(tick, 1000);
    } else if (!on && S.running) {
      S.acc += (Date.now() - S.t0) / 1000; S.running = false;
      clearInterval(timerId); timerId = null;
    }
    Mock.save(); paintClock();
    $('#mock-start', root).textContent = S.running ? 'Running…' : (S.started ? 'Resume' : 'Start');
    $('#mock-start', root).disabled = S.running;
  }

  $('#mock-start', root).addEventListener('click', function () { setRunning(true); });
  $('#mock-pause', root).addEventListener('click', function () { setRunning(false); });
  $('#mock-reset', root).addEventListener('click', function () {
    if (!confirm('Reset the mock session? Answers, flags, and the timer will be cleared.')) return;
    setRunning(false); Mock.clear(); Mock.load();
    buildMockBody(); paintClock();
  });

  function flagToggle(id) {
    var f = Mock.S.flags, i = f.indexOf(id);
    if (i >= 0) f.splice(i, 1); else f.push(id);
    Mock.save(); paintQmap();
    var btn = $('#flag-' + id, root);
    if (btn) btn.textContent = i >= 0 ? '⚑ Flag' : '⚑ Flagged';
  }

  function paintQmap() {
    var qm = $('#mock-qmap', root);
    qm.innerHTML = '';
    COURSE.mockTasks.forEach(function (t, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = String(i + 1);
      var a = Mock.S.answers[t.id];
      if (a != null && a !== '') b.classList.add('answered');
      if (Mock.S.flags.indexOf(t.id) >= 0) b.classList.add('flagged');
      if (i === Mock.S.cur) b.classList.add('current');
      b.setAttribute('aria-label', 'Task ' + (i + 1) + (b.classList.contains('answered') ? ', answered' : '') +
        (b.classList.contains('flagged') ? ', flagged' : ''));
      b.addEventListener('click', function () {
        Mock.S.cur = i; Mock.save(); paintQmap();
        var tgt = $('#mocktask-' + t.id, root);
        if (tgt) tgt.scrollIntoView({ block: 'start' });
      });
      qm.appendChild(b);
    });
  }

  function taskHTML(t, i) {
    var box = el('div', 'mock-task');
    box.id = 'mocktask-' + t.id;
    var flagged = Mock.S.flags.indexOf(t.id) >= 0;
    box.innerHTML = '<button class="btn ghost flag-btn" id="flag-' + t.id + '" type="button">' +
      (flagged ? '⚑ Flagged' : '⚑ Flag') + '</button>' +
      '<div class="small muted mono">Task ' + (i + 1) + ' / ' + COURSE.mockTasks.length + '</div>' +
      '<div class="q" style="font-weight:600;margin:6px 0 10px">' + esc(t.q || t.prompt || 'Task') + '</div>';
    box.querySelector('.flag-btn').addEventListener('click', function () { flagToggle(t.id); });

    if (t.type === 'code') {
      var ta = document.createElement('textarea');
      ta.className = 'code-editor';
      ta.value = Mock.S.answers[t.id] || t.starter || '';
      ta.setAttribute('aria-label', 'Answer editor for task ' + (i + 1));
      box.appendChild(ta);
      ta.addEventListener('input', function () {
        Mock.S.answers[t.id] = ta.value; Mock.save(); paintQmap();
      });
      if (t.hint) {
        var hb = el('button', 'btn ghost', 'Hint');
        hb.type = 'button';
        var hx = el('div', 'hint-box', '<b>Hint:</b> ' + esc(t.hint));
        hb.addEventListener('click', function () { hx.classList.toggle('show'); });
        var wr = el('div', 'btn-row'); wr.appendChild(hb); box.appendChild(wr); box.appendChild(hx);
      }
    } else {
      var opts = el('div');
      (t.choices || []).forEach(function (c, ci) {
        var b = el('button', 'opt btn ghost', esc(c));
        b.type = 'button';
        b.style.display = 'block'; b.style.width = '100%'; b.style.textAlign = 'left'; b.style.margin = '6px 0';
        if (String(Mock.S.answers[t.id]) === String(ci)) b.style.borderColor = 'var(--cyan)';
        b.addEventListener('click', function () {
          Mock.S.answers[t.id] = String(ci); Mock.save(); paintQmap();
          $all('button.opt', opts).forEach(function (o) { o.style.borderColor = ''; });
          b.style.borderColor = 'var(--cyan)';
        });
        opts.appendChild(b);
      });
      box.appendChild(opts);
    }
    return box;
  }

  function buildMockBody() {
    var host = $('#mock-tasks', root);
    host.innerHTML = '';
    COURSE.mockTasks.forEach(function (t, i) { host.appendChild(taskHTML(t, i)); });
    paintQmap();
    $('#mock-start', root).textContent = Mock.S.running ? 'Running…' : (Mock.S.started ? 'Resume' : 'Start');
    $('#mock-start', root).disabled = Mock.S.running;
  }

  function finish(auto) {
    var snapshot = JSON.parse(JSON.stringify(Mock.S.answers || {}));
    setRunning(false);
    var sc = (function () {
      var right = 0;
      COURSE.mockTasks.forEach(function (t) {
        var a = snapshot[t.id];
        if (t.type === 'code') {
          if (a && checkFragments(a, t.required).every(function (r) { return r.met; })) right++;
        } else if (a != null && +a === t.answer) right++;
      });
      return { right: right, total: COURSE.mockTasks.length,
        pct: COURSE.mockTasks.length ? Math.round(right / COURSE.mockTasks.length * 100) : 0 };
    })();
    var prevBest = parseFloat(Progress.get('mock:best', '0')) || 0;
    var newBest = Math.max(prevBest, sc.pct);
    Progress.set('mock:best', String(newBest));
    Progress.set('mock:sessions', String(sessions + 1));
    sessions++;
    Mock.clear();

    var res = $('#mock-result', root);
    var html = '<div class="card"><h2>Score: ' + sc.pct + '%</h2>' +
      '<div class="mock-score">' + sc.right + ' / ' + sc.total + '</div>' +
      '<p class="muted small">' + (auto ? 'Time expired — auto-submitted. ' : '') +
      'Best score: ' + newBest + '% · Sessions: ' + sessions + '</p></div>' +
      '<h2 class="section-title">Review</h2>';
    COURSE.mockTasks.forEach(function (t, i) {
      var a = snapshot[t.id], ok;
      if (t.type === 'code') ok = !!(a && checkFragments(a, t.required).every(function (r) { return r.met; }));
      else ok = (a != null && +a === t.answer);
      html += '<div class="review-item"><div class="small muted mono">Task ' + (i + 1) + '</div>' +
        '<div style="font-weight:600">' + esc(t.q || t.prompt || '') + ' ' +
        '<span class="' + (ok ? 'ok' : 'bad') + '">' + (ok ? '✓' : '✗') + '</span></div>';
      if (t.type === 'choice') {
        html += '<div class="small">Your answer: <b>' + esc(a != null ? (t.choices[+a] || '—') : '—') + '</b><br>' +
          'Correct: <b>' + esc(t.choices[t.answer] || '') + '</b></div>';
      } else {
        html += '<div class="small">Model answer: ' + esc(t.answer || '') + '</div>';
      }
      if (t.explain) html += '<div class="small muted"><b>Why:</b> ' + esc(t.explain) + '</div>';
      html += '</div>';
    });
    res.innerHTML = html;
    buildMockBody();
    paintClock();
    $('#mock-meta', root).textContent = 'best: ' + newBest + '% · sessions: ' + sessions;
    refreshReadiness();
    res.scrollIntoView();
  };

  $('#mock-finish', root).addEventListener('click', function () {
    var un = COURSE.mockTasks.filter(function (t) {
      var a = Mock.S.answers[t.id]; return a == null || a === '';
    }).length;
    var msg = un ? un + ' task(s) unanswered. Submit anyway?' : 'Submit the mock for scoring?';
    if (confirm(msg)) finish(false);
  });

  buildMockBody();
  paintClock();
  if (Mock.S.running) { /* resumed across reload while running: re-anchor */
    Mock.S.acc += (Date.now() - Mock.S.t0) / 1000; Mock.S.t0 = Date.now();
    timerId = setInterval(tick, 1000); Mock.save();
  }
}

/* ============================== More =============================== */
function buildMore(root) {
  var html = heroHTML() +
    '<h2 class="section-title">Cheat sheets</h2>';
  if (COURSE.cheatSheets.length) {
    html += COURSE.cheatSheets.map(function (cs, i) {
      return '<details class="fold cs-toggle"' + (i === 0 ? ' open' : '') + '><summary>' + esc(cs.title) + '</summary>' +
        '<div class="fold-body">' + (cs.blocks || []).map(function (b) {
          var s = '<h3>' + esc(b.h) + '</h3>' + mdLite(b.body || '');
          if (b.code) s += '<pre><code>' + esc(b.code) + '</code></pre>';
          return s;
        }).join('') + '</div></details>';
    }).join('');
  } else {
    html += '<div class="card"><p class="muted small">No cheat sheets in this course document.</p></div>';
  }

  html += '<h2 class="section-title">Answer bank</h2>';
  if (COURSE.answerBank.length) {
    html += COURSE.answerBank.map(function (a) {
      return '<div class="answer-item"><div style="font-weight:600">' + esc(a.q) + '</div>' +
        '<div class="a">' + mdLite(a.a) + '</div>' +
        (a.ref ? '<div class="small muted">' + esc(a.ref) + '</div>' : '') + '</div>';
    }).join('');
  } else {
    html += '<div class="card"><p class="muted small">No answer bank in this course document.</p></div>';
  }

  html += '<h2 class="section-title">Source trail</h2>';
  if (COURSE.sourceLinks.length) {
    html += '<ul class="src-list">' + COURSE.sourceLinks.map(function (s) {
      return '<li><a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.name) + '</a>' +
        (s.note ? '<div class="small muted">' + esc(s.note) + '</div>' : '') +
        (s.retrieved ? '<span class="retrieved">retrieved ' + esc(s.retrieved) + '</span>' : '') + '</li>';
    }).join('') + '</ul>';
  } else {
    html += '<div class="card"><p class="muted small">No source links in this course document.</p></div>';
  }

  if (COURSE.honestyNote) {
    html += '<div class="honesty"><b>Honesty note:</b> ' + esc(COURSE.honestyNote) + '</div>';
  }
  html += '<div class="honesty">Created by Interstitium Labs · SCIENTIA OMNIA VINCIT · ' +
    'All practice content is original. No vendor-exam material is reproduced.</div>';
  root.innerHTML = html;
}

/* ============================== boot =============================== */
var BUILDERS = {
  brief: buildBrief, plan: buildPlan, study: buildStudy,
  labs: buildLabs, mock: buildMock, more: buildMore
};

function showError(msg) {
  var main = $('#shell-main');
  if (main) {
    main.innerHTML = '<div class="card"><h2>Course failed to load</h2>' +
      '<p class="muted">' + esc(msg) + '</p>' +
      '<p class="small muted">Provide course data via an inline ' +
      '<code>&lt;script id="il-course-data" type="application/json"&gt;</code> block, ' +
      'a <code>?data=</code> URL, or <code>?course=&lt;id&gt;</code>.</p></div>';
  }
  var err = $('#shell-error');
  if (err) err.textContent = msg;
  try { console.error('[course-shell]', msg); } catch (e) {}
}

function boot() {
  loadCourseData().then(function (raw) {
    if (!raw) { showError('No course JSON found.'); return; }
    if (raw.__parseError) { showError('Course JSON parse error: ' + raw.__parseError); return; }
    COURSE = normCourse(raw);
    document.title = COURSE.title + ' · ' + (COURSE.code || 'Interstitium Labs');
    renderChrome();
    Sync.init($('#sync-note'));
    window.addEventListener('hashchange', route);
    route();
    /* Deep-link support for module anchors: #/study then #mod-<id> handled by Study hash. */
  }).catch(function (e) {
    showError('Unexpected error loading course: ' + (e && e.message));
  });
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
}

/* Test hook (harmless in production): exposes pure helpers for verification. */
try {
  if (typeof window !== 'undefined') window.__ilCourseShell = {
    normCourse: normCourse, mdLite: mdLite, checkFragments: checkFragments,
    readiness: readiness, esc: esc
  };
} catch (e) {}

})();
