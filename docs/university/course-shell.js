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
    tips: d.tips || [],
    legends: d.legends || {},
    answerBank: d.answerBank || [],
    sourceLinks: d.sourceLinks || [],
    glossary: d.glossary || [],
    faq: d.faq || [],
    honestyNote: d.honestyNote || '',
    crosswalk: d.crosswalk || [],
    certGates: d.certGates || [],
    readinessDashboard: d.readinessDashboard || null
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
    /* 2026-10-08: sweep the readiness ring from its previous value (il-animate.js). */
    if (window.ILAnimate) window.ILAnimate.animateRing(host, r.pct);
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

/* ============================== symbol legend ========================
 * 2026-10-08 (resume fix extension): "Legend" button in the player chrome.
 * Opens a dialog explaining the icon/badge/symbol vocabulary (COURSE.legends
 * from the course JSON) — no symbol is ever mysterious. Esc closes. */
function wireLegend() {
  try {
    var btn = document.getElementById('legend-btn');
    if (!btn || btn.dataset.wired) return;
    btn.dataset.wired = '1';
    var dlg = null;
    function close() {
      if (dlg) { dlg.style.display = 'none'; }
      btn.setAttribute('aria-expanded', 'false');
    }
    function open() {
      if (!dlg) {
        dlg = el('div', 'legend-dlg');
        dlg.setAttribute('role', 'dialog');
        dlg.setAttribute('aria-label', 'Symbol legend');
        var legends = (typeof COURSE !== 'undefined' && COURSE && COURSE.legends) || {};
        var keys = Object.keys(legends);
        var html = '<div class="legend-dlg__head"><strong>Symbol legend</strong>' +
          '<button class="legend-dlg__close" type="button" aria-label="Close legend">✕</button></div>';
        if (keys.length) {
          html += '<dl class="legend-dlg__list">';
          keys.forEach(function (k) {
            html += '<dt>' + esc(k) + '</dt><dd>' + esc(String(legends[k])) + '</dd>';
          });
          html += '</dl>';
        } else {
          html += '<p class="muted">No legend entries for this course.</p>';
        }
        dlg.innerHTML = html;
        dlg.style.display = 'none';
        document.body.appendChild(dlg);
        dlg.querySelector('.legend-dlg__close').addEventListener('click', close);
      }
      dlg.style.display = '';
      btn.setAttribute('aria-expanded', 'true');
    }
    btn.addEventListener('click', function () {
      if (btn.getAttribute('aria-expanded') === 'true') close(); else open();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
  } catch (e) {}
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
  /* 2026-10-08: scroll-reveal + progress-bar animation pass (il-animate.js). */
  if (pane && window.ILAnimate) window.ILAnimate.observe(pane);
  if (id === 'brief') {
    refreshReadiness();
    /* 2026-10-08 (fix round): BUILDERS.brief rebuilds the pane via
       innerHTML, wiping the "Continue where you left off" banner that
       refreshILProgress() injected into the un-built pane. Re-inject
       after every build/switch so the resume banner survives reloads
       and tab switches whenever progress exists. */
    try { refreshILProgress(); } catch (e) {}
  }
  try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch (e) { window.scrollTo(0, 0); }
}

function route() {
  var m = /^#\/([a-z]+)/.exec(location.hash || '');
  showTab(m ? m[1] : 'brief');
}

/* ============================== unified progress (2026-10-08) ======
 * Nav progress strip + next-up prompt, backed by ILProgress
 * (localStorage "il-progress-v1"). Mirrors the module toggles above
 * into the cross-course store without touching the existing readiness
 * ring or Sync pipeline.
 * ===================================================================== */
function refreshILProgress() {
  try {
    if (typeof ILProgress === 'undefined' || !ILProgress) return;
    if (typeof COURSE === 'undefined' || !COURSE) return;
    var total = (COURSE.modules || []).length;
    var stats = ILProgress.courseStats(COURSE.courseId, total);
    var nav = $('#shell-nav');
    var strip = document.getElementById('ilprog-navstrip');
    if (nav) {
      if (!strip) {
        strip = el('div', 'ilprog-nav');
        strip.id = 'ilprog-navstrip';
        strip.setAttribute('aria-live', 'polite');
        nav.appendChild(strip);
      }
      strip.innerHTML =
        '<div class="ilprog-bar__label">' + ILProgress.esc(COURSE.code || '') +
        ' · ' + stats.done + ' of ' + stats.total + ' modules · ' + stats.pct + '%</div>' +
        '<div class="ilprog-bar__track"><div class="ilprog-bar__fill" style="width:' + stats.pct + '%"></div></div>';
    }
    /* "Continue where you left off" at the top of the Brief tab — the
       resume anchor lands the student at the exact last module. No
       progress yet → "Start your guided path" variant (IL-01).
       Gating unchanged: resume into a gated course hits the paywall. */
    var lp = ILProgress.getLastPosition();
    var brief = $('#tab-brief');
    var cwrap = document.getElementById('ilprog-continue-wrap');
    if (brief) {
      ILProgress.loadSequence(function (seq) {
        var html = lp ? ILProgress.continueHTML(lp, seq, {}) : ILProgress.startPathHTML(seq, {});
        if (!html) { if (cwrap) cwrap.style.display = 'none'; return; }
        if (!cwrap) {
          cwrap = el('div', '');
          cwrap.id = 'ilprog-continue-wrap';
          brief.insertBefore(cwrap, brief.firstChild);
        }
        /* Re-render only when the resume anchor moved. */
        var sig = lp ? (lp.courseId + '|' + lp.moduleId + '|' + lp.timestamp) : 'start-path';
        if (cwrap.dataset.lp !== sig) {
          cwrap.dataset.lp = sig;
          cwrap.innerHTML = html;
        }
        cwrap.style.display = '';
      });
    } else if (cwrap) { cwrap.style.display = 'none'; }
    /* "Next up" prompt when this course is 100% complete. */
    var main = $('#shell-main');
    var wrap = document.getElementById('ilprog-nextup-wrap');
    if (stats.total > 0 && stats.done >= stats.total) {
      ILProgress.loadSequence(function (seq) {
        var next = seq ? ILProgress.nextEntry(seq, COURSE.courseId) : null;
        if (!next) { if (wrap) wrap.style.display = 'none'; return; }
        if (!wrap) {
          wrap = el('div', '');
          wrap.id = 'ilprog-nextup-wrap';
          main.insertBefore(wrap, main.firstChild);
        }
        wrap.innerHTML = '<div class="ilprog-nextup" role="region" aria-label="Course complete — next course">' +
          '<div><p class="ilprog-nextup__eyebrow">Course complete — next up in the sequence</p>' +
          '<p class="ilprog-nextup__desc"><strong>' + ILProgress.esc(next.code) + '</strong> · ' +
          ILProgress.esc(next.title) + ' (' + (next.moduleCount || (next.moduleIds || []).length) + ' modules)</p></div>' +
          '<a class="ilprog-nextup__btn" href="' + ILProgress.esc(ILProgress.courseURL(next)) + '">Start next course</a></div>';
        wrap.style.display = '';
      });
    } else if (wrap) {
      wrap.style.display = 'none';
    }
  } catch (e) {}
}

/* ============================== guided engine (2026-10-08) =========
 * Rosetta-Stone-style guided layer, backed by ILGuided
 * (localStorage "il-guided-v1"). Sequential unlock, path rail,
 * mastery gates, guided practice, review loops.
 *
 * Locks are a LEARNING-FLOW concept only — the paywall stays enforced
 * at the worker; nothing here touches entitlement.
 * ===================================================================== */
var Guided = {
  infos: function () {
    return (COURSE.modules || []).map(function (m) {
      return { id: m.id, title: m.title, code: m.code, quizTotal: (m.quiz || []).length };
    });
  },
  fullInfos: function () {
    return (COURSE.modules || []).map(function (m) {
      return {
        id: m.id, title: m.title, code: m.code, quizTotal: (m.quiz || []).length,
        quiz: m.quiz || [], summary: m.summary || '', objectives: m.objectives || []
      };
    });
  },
  findModule: function (id) {
    var ms = COURSE.modules || [];
    for (var i = 0; i < ms.length; i++) if (ms[i].id === id) return ms[i];
    return null;
  },
  answerOf: function (moduleId, qi) { return Progress.get('quiz:' + moduleId + ':' + qi, null); },
  seedMastery: function (m) {
    /* Grandfather answers stored before the guided engine shipped. */
    try {
      if (typeof ILGuided !== 'undefined' && ILGuided && (m.quiz || []).length) {
        ILGuided.recomputeMastery(COURSE.courseId, m.id, m.quiz, function (qqi) {
          return Guided.answerOf(m.id, qqi);
        });
      }
    } catch (e) {}
  },
  lockNotice: function (wrap) {
    var head = wrap.querySelector('.mod-head');
    if (!head || head.querySelector('.ilgd-locknote')) return;
    head.appendChild(el('span', 'ilgd-locknote', '🔒 Complete the previous lesson to unlock'));
  },
  /* Repaint the rail and every module's lock/badge/gate state. Called
     after any progress change (quiz answer, re-attempt, module toggle,
     auto-mark). */
  refresh: function () {
    try {
      if (typeof ILGuided === 'undefined' || !ILGuided) return;
      if (typeof COURSE === 'undefined' || !COURSE) return;
      var cid = COURSE.courseId;
      var infos = Guided.infos();
      ILGuided.syncNoGateMastery(cid, infos);
      var rail = document.getElementById('ilgd-rail');
      if (rail) ILGuided.paintRail(rail, cid, infos);
      var states = ILGuided.computeStates(cid, infos);
      states.forEach(function (s) {
        var wrap = document.getElementById('mod-' + s.id);
        if (!wrap) return;
        var locked = (s.state === 'locked' || s.state === 'next');
        wrap.classList.toggle('ilgd-locked', locked);
        var badge = wrap.querySelector('[data-ilgd-badge]');
        if (badge) {
          var txt = '', cls = 'ilgd-state';
          if (s.state === 'done') {
            /* 2026-10-08 (WORKSTREAM 5): tested-out modules read distinctly. */
            txt = s.testOut ? '✓ Tested out' : (s.hasGate ? '✓ Mastered' : '✓ Complete');
            cls += ' ilgd-state--done';
          } else if (s.state === 'current') {
            txt = '● You are here'; cls += ' ilgd-state--current';
          } else if (s.state === 'next') {
            txt = '→ Up next'; cls += ' ilgd-state--next';
          } else {
            txt = '🔒 Locked'; cls += ' ilgd-state--locked';
          }
          /* mastery-gate flag on the current module */
          if (s.state === 'current' && s.complete && s.hasGate && !s.mastered) {
            txt = '⚠ Mastery gate'; cls += ' ilgd-state--gate';
          }
          badge.className = cls;
          badge.textContent = txt;
        }
        /* mastery-gate messaging */
        var gate = wrap.querySelector('[data-ilgd-gate]');
        if (gate) {
          var msg = '';
          if (s.state === 'current' && s.hasGate && !s.mastered) {
            var fm = Guided.findModule(s.id);
            var qp = ILGuided.quizProgress((fm && fm.quiz) || [], function (qqi) {
              return Guided.answerOf(s.id, qqi);
            });
            if (qp.answered < qp.total) {
              msg = 'Mastery gate — quick checks ' + qp.answered + '/' + qp.total + ' answered' +
                (qp.answered ? ' · best ' + Math.round(qp.score * 100) + '%' : '') +
                '. Answer all and score ≥70% to unlock the next module.';
            } else {
              msg = 'Mastery gate — best score ' + Math.round(qp.score * 100) +
                '%, need ≥70%. Re-attempt the quick checks (best score counts) or practice with hints.';
            }
          } else if (s.state === 'current' && s.hasGate && s.mastered && !s.complete) {
            msg = 'Mastery earned ✓ — mark this module complete to unlock the next.';
          }
          gate.textContent = msg;
          gate.style.display = msg ? '' : 'none';
        }
        /* 2026-10-08 (resume fix extension): explicit "Next →" button at
           every module foot — advances in guided sequence, honors the
           mastery-gate lock (disabled with the reason when locked). */
        var nxtBtn = wrap.querySelector('[data-ilgd-next]');
        if (nxtBtn) {
          var following = (s.index + 1 < states.length) ? states[s.index + 1] : null;
          if (!following) {
            nxtBtn.style.display = 'none';
          } else {
            nxtBtn.style.display = '';
            if (following.state === 'current') {
              nxtBtn.disabled = false;
              nxtBtn.classList.add('primary');
              nxtBtn.innerHTML = 'Next → <span class="ilgd-next__t">' + esc(following.title) + '</span>';
              nxtBtn.title = 'Go to ' + following.title;
              nxtBtn.setAttribute('data-next-id', following.id);
            } else {
              nxtBtn.disabled = true;
              nxtBtn.classList.remove('primary');
              nxtBtn.removeAttribute('data-next-id');
              /* 2026-10-08 (fix round): keep the literal "Next →" label even
                 when locked — the gate reason follows the label, never
                 replaces it. */
              if (s.hasGate && !s.mastered) {
                nxtBtn.innerHTML = 'Next → <span class="ilgd-next__r">⚠ Pass the mastery check (≥70%) to unlock</span>';
              } else {
                nxtBtn.innerHTML = 'Next → <span class="ilgd-next__r">🔒 Complete this module to unlock</span>';
              }
              nxtBtn.title = 'Complete this module to unlock the next one';
            }
          }
        }
        /* drop stale lock notices once unlocked */
        if (!locked) {
          var ln = wrap.querySelector('.ilgd-locknote');
          if (ln && ln.parentNode) ln.parentNode.removeChild(ln);
        }
      });
    } catch (e) {}
  }
};

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
  if (COURSE.arc && COURSE.arc.length) {
    var arcItems = Array.isArray(COURSE.arc) ? COURSE.arc : [COURSE.arc];
    var arcCards = '', arcList = '';
    arcItems.forEach(function (a) {
      if (typeof a === 'string') {
        arcList += '<li>' + mdLite(a) + '</li>';
      } else if (a && typeof a === 'object') {
        arcCards += '<div class="arc-card"><div class="phase">' + esc(String(a.phase || '')) + '</div>' +
          '<h3>' + esc(String(a.title || '')) + '</h3><p>' + esc(String(a.body || a.text || '')) + '</p></div>';
      }
    });
    if (arcCards || arcList) {
      html += '<h2 class="section-title">Synthesis arc</h2>';
      if (arcCards) html += '<div class="arc-grid">' + arcCards + '</div>';
      if (arcList) html += '<div class="card"><ul class="obj-list">' + arcList + '</ul></div>';
    }
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
  /* 2026-10-08: "Stories" rail (WORKSTREAM 1) — fills in async from
     stories/_index.json; nothing renders when the course has no stories. */
  var storiesHost = el('div', '');
  storiesHost.id = 'il-stories-rail';
  root.appendChild(storiesHost);
  if (window.ILStories && COURSE && COURSE.courseId) {
    try { window.ILStories.buildRail(storiesHost, COURSE.courseId); } catch (e) {}
  }
  /* 2026-10-08 (resume fix extension): Study tips — practical, course-
     specific tips from the course JSON (COURSE.tips). Nothing renders
     when the course has no tips. */
  try {
    if (COURSE.tips && COURSE.tips.length) {
      var tipsHost = el('div', 'card');
      tipsHost.id = 'il-tips-card';
      var tipsHTML = '<h2>Study tips</h2><ul class="obj-list">';
      COURSE.tips.forEach(function (t) {
        tipsHTML += '<li>💡 ' + esc(String(t)) + '</li>';
      });
      tipsHTML += '</ul>';
      tipsHost.innerHTML = tipsHTML;
      root.appendChild(tipsHost);
    }
  } catch (e) {}
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
      /* 2026-10-08 (WORKSTREAM 3): struggle detection on quick checks.
         One-shot items feed the per-module quick-check streak. */
      try {
        if (typeof IL !== 'undefined' && IL && IL.noahTutor)
          IL.noahTutor.recordAnswer(mod, 'quiz:' + qi, q.q, ci === q.answer, box);
      } catch (e) {}
      refreshReadiness();
      /* 2026-10-08 (WORKSTREAM 2): guided mastery gate — recompute, then
         refresh rail/locks/gate messaging. */
      try {
        if (typeof ILGuided !== 'undefined' && ILGuided) {
          ILGuided.recomputeMastery(COURSE.courseId, mod.id, mod.quiz || [], function (qqi) {
            return Progress.get('quiz:' + mod.id + ':' + qqi, null);
          });
        }
        if (typeof Guided !== 'undefined' && Guided.refresh) Guided.refresh();
      } catch (e2) {}
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
  /* 2026-10-08 (WORKSTREAM 2): guided practice (unanswered) / re-attempt
     (answered). Re-attempts keep the mastery gate fair — best score counts,
     so a low first attempt can never permanently lock the path. */
  try {
    var gBar = el('div', 'ilgd-quizbar');
    if (chosen == null) {
      var pracBtn = el('button', 'btn ilgd-practice-btn', 'Guided practice');
      pracBtn.type = 'button';
      var pSlot = el('div', 'ilgd-practice-slot');
      pracBtn.addEventListener('click', function () {
        try {
          if (typeof ILGuided !== 'undefined' && ILGuided) {
            pSlot.innerHTML = ILGuided.practiceHTML(q, {
              courseId: COURSE.courseId, moduleId: mod.id,
              label: 'Guided practice · ' + (mod.title || '')
            });
            ILGuided.wirePractice(pSlot);
            pracBtn.style.display = 'none';
          }
        } catch (e) {}
      });
      gBar.appendChild(pracBtn);
      gBar.appendChild(pSlot);
    } else {
      var reBtn = el('button', 'ilgd-reattempt', 'Re-attempt this check');
      reBtn.type = 'button';
      reBtn.setAttribute('aria-label', 'Clear your answer and try this quick check again');
      reBtn.addEventListener('click', function () {
        Progress.set(key, null);
        var fresh = quizHTML(mod, qi, q);
        if (box.parentNode) box.parentNode.replaceChild(fresh, box);
        try { if (typeof Guided !== 'undefined' && Guided.refresh) Guided.refresh(); } catch (e) {}
      });
      gBar.appendChild(reBtn);
    }
    box.appendChild(gBar);
  } catch (e) {}
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

/* ============================== guided "Next →" navigation =========
 * 2026-10-08 (resume fix extension): programmatic module advance for the
 * explicit per-module "Next →" button. Respects the guided lock — a locked
 * target shows the unlock rule instead of opening. Reuses the real head
 * toggle so auto-mark arming, progress touch, and animations all fire. */
function goToModule(mid) {
  try {
    if (typeof COURSE === 'undefined' || !COURSE) return;
    var target = null;
    (COURSE.modules || []).forEach(function (mm) { if (mm.id === mid) target = mm; });
    if (!target) return;
    var locked = false;
    try {
      if (typeof ILGuided !== 'undefined' && ILGuided && typeof Guided !== 'undefined' && Guided.infos) {
        var st = ILGuided.stateFor(COURSE.courseId, mid, Guided.infos());
        locked = !st || st.state === 'locked' || (st.state === 'next' && !st.unlocked);
      }
    } catch (e) {}
    var mw = document.getElementById('mod-' + mid);
    if (!mw) return;
    if (locked) {
      try { if (typeof Guided !== 'undefined' && Guided.lockNotice) Guided.lockNotice(mw); } catch (e2) {}
      return;
    }
    var bdy = mw.querySelector('.mod-body');
    var hd = mw.querySelector('.mod-head');
    if (bdy && bdy.style.display === 'none' && hd && typeof hd.click === 'function') {
      hd.click();
    } else {
      try {
        if (typeof ILProgress !== 'undefined' && ILProgress) ILProgress.touch(COURSE.courseId, mid);
      } catch (e3) {}
    }
    try { mw.scrollIntoView({ block: 'start' }); } catch (e4) {}
    try { if (typeof refreshILProgress !== 'undefined') refreshILProgress(); } catch (e5) {}
  } catch (e) {}
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
  /* 2026-10-08 (WORKSTREAM 2): guided state badge (done/current/next/
     locked). Text/class painted by Guided.refresh(). */
  var gBadge = el('span', 'ilgd-state', '');
  gBadge.setAttribute('data-ilgd-badge', '1');
  head.appendChild(gBadge);
  /* 2026-10-08 (WORKSTREAM 3): "Ask Noah about this lesson" — opens Noah with
     the lesson context pre-loaded (js/il-noah-tutor.js). Guarded: silent
     no-op if the tutor module failed to load. stopPropagation so the header
     toggle does not fire. */
  try {
    if (typeof IL !== 'undefined' && IL && IL.noahTutor) {
      (function (mod) {
        var askBtn = el('button', 'noah-ask-btn', '◈ Ask Noah about this lesson');
        askBtn.type = 'button';
        askBtn.setAttribute('aria-label', 'Ask Noah AI about this lesson');
        askBtn.addEventListener('click', function (e) {
          e.stopPropagation();
          IL.noahTutor.askAboutLesson(mod, wrap);
        });
        askBtn.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') e.stopPropagation();
        });
        head.appendChild(askBtn);
      })(m);
    }
  } catch (e) {}
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
  /* 2026-10-08 (WORKSTREAM 2): guided — seed mastery from answers stored
     before the guided engine shipped; add the mastery-gate message box. */
  try { if (typeof Guided !== 'undefined' && Guided.seedMastery) Guided.seedMastery(m); } catch (e) {}
  var gateBox = el('div', 'ilgd-gate', '');
  gateBox.setAttribute('data-ilgd-gate', '1');
  gateBox.style.display = 'none';
  body.appendChild(gateBox);
  /* 2026-10-08 (WORKSTREAM 2): spaced review loop — on completion, surface
     2-3 recall prompts from earlier completed modules (their own quiz
     questions; never invented). Shown once per module. */
  function maybeReview() {
    try {
      if (typeof ILGuided === 'undefined' || !ILGuided) return;
      if (typeof Guided === 'undefined') return;
      if (ILGuided.reviewShown(COURSE.courseId, m.id)) return;
      if (document.getElementById('ilgd-review-' + m.id)) return;
      var rh = ILGuided.reviewHTML(COURSE.courseId, Guided.fullInfos(), m.id,
        function (mid) { var mm = Guided.findModule(mid); return (mm && mm.quiz) || []; },
        function (mid, qqi) { return Progress.get('quiz:' + mid + ':' + qqi, null); });
      if (rh) {
        var rwrap = document.createElement('div');
        rwrap.id = 'ilgd-review-' + m.id;
        rwrap.innerHTML = rh;
        body.insertBefore(rwrap, foot);
        ILGuided.wirePractice(rwrap);
      }
    } catch (e) {}
  }
  var foot = el('div', 'btn-row');
  var doneBtn = el('button', 'btn' + (done ? '' : ' primary'), done ? '✓ Module complete' : 'Mark module complete');
  doneBtn.type = 'button';
  doneBtn.setAttribute('data-mod-complete', '1');
  doneBtn.addEventListener('click', function () {
    var now = !(Progress.get('module:' + m.id) === '1');
    Progress.set('module:' + m.id, now ? '1' : null);
    /* 2026-10-08: mirror module completion into the unified cross-course
       store (localStorage "il-progress-v1") — drives resume/continue,
       course progress bars, and next-up prompts. */
    try {
      if (typeof ILProgress !== 'undefined') {
        if (now) { ILProgress.markComplete(COURSE.courseId, m.id); ILProgress.touch(COURSE.courseId, m.id); }
        else ILProgress.unmarkComplete(COURSE.courseId, m.id);
      }
    } catch (e) {}
    head.querySelector('.mod-done-flag').textContent = now ? '✓ complete' : '';
    doneBtn.textContent = now ? '✓ Module complete' : 'Mark module complete';
    doneBtn.classList.toggle('primary', !now);
    refreshReadiness();
    if (typeof refreshILProgress !== 'undefined') { try { refreshILProgress(); } catch (e) {} }
    /* 2026-10-08 (WORKSTREAM 3): end-of-module Noah check-in offer —
       "Check my understanding with Noah" (Socratic, 2–3 questions). */
    try {
      if (now && typeof IL !== 'undefined' && IL && IL.noahTutor) IL.noahTutor.onModuleComplete(m, foot);
    } catch (e) {}
    /* 2026-10-08 (WORKSTREAM 2): guided — review loop on completion,
       gate messaging + rail/lock refresh. */
    try {
      if (now) maybeReview();
      else {
        var oldRev = document.getElementById('ilgd-review-' + m.id);
        if (oldRev && oldRev.parentNode) oldRev.parentNode.removeChild(oldRev);
      }
      if (typeof Guided !== 'undefined' && Guided.refresh) Guided.refresh();
    } catch (e2) {}
  });
  foot.appendChild(doneBtn);
  /* 2026-10-08 (resume fix extension): explicit "Next →" button — advances
     to the next module in the guided sequence. State (enabled/disabled +
     reason) is painted by Guided.refresh(); the target id is stamped at
     repaint time. */
  var nextBtn = el('button', 'btn ilgd-next-btn', 'Next →');
  nextBtn.type = 'button';
  nextBtn.setAttribute('data-ilgd-next', '1');
  nextBtn.setAttribute('aria-label', 'Go to the next module');
  nextBtn.addEventListener('click', function () {
    if (nextBtn.disabled) return;
    var nid = nextBtn.getAttribute('data-next-id');
    if (nid) goToModule(nid);
  });
  foot.appendChild(nextBtn);
  body.appendChild(foot);
  wrap.appendChild(head); wrap.appendChild(body);

  /* 2026-10-08: auto-mark on reaching the end of an open module — once per
     open. When the module footer scrolls fully into view, the student has
     seen the whole module. */
  var autoMarked = false;
  var autoMarking = null;
  function autoMarkCheck() {
    if (autoMarked || autoMarking) return;
    if (!(typeof ILProgress !== 'undefined' && ILProgress)) return;
    if (body.style.display === 'none') return;
    if (ILProgress.isComplete(COURSE.courseId, m.id)) { autoMarked = true; return; }
    autoMarked = true;
    ILProgress.markComplete(COURSE.courseId, m.id);
    ILProgress.touch(COURSE.courseId, m.id);
    try { Progress.set('module:' + m.id, '1'); } catch (e) {}
    head.querySelector('.mod-done-flag').textContent = '✓ complete';
    doneBtn.textContent = '✓ Module complete';
    doneBtn.classList.remove('primary');
    try { refreshReadiness(); } catch (e) {}
    if (typeof refreshILProgress !== 'undefined') { try { refreshILProgress(); } catch (e) {} }
    /* 2026-10-08 (WORKSTREAM 3): end-of-module Noah check-in offer
       (auto-mark-on-scroll path). */
    try {
      if (typeof IL !== 'undefined' && IL && IL.noahTutor) IL.noahTutor.onModuleComplete(m, foot);
    } catch (e) {}
    /* 2026-10-08 (WORKSTREAM 2): guided — review loop + rail/lock refresh
       on auto-mark completion. */
    try {
      maybeReview();
      if (typeof Guided !== 'undefined' && Guided.refresh) Guided.refresh();
    } catch (e2) {}
  }

  function toggle() {
    /* 2026-10-08 (WORKSTREAM 2): guided lock — a locked module does not
       open; the learner gets the unlock rule instead. */
    if (wrap.classList.contains('ilgd-locked')) {
      try { if (typeof Guided !== 'undefined' && Guided.lockNotice) Guided.lockNotice(wrap); } catch (e) {}
      return;
    }
    var open = body.style.display === 'none';
    body.style.display = open ? '' : 'none';
    head.setAttribute('aria-expanded', open ? 'true' : 'false');
    /* 2026-10-08: staggered module-open entrance (il-animate.js). */
    if (window.ILAnimate) window.ILAnimate.moduleToggled(body, open);
    /* 2026-10-08: every module view is the resume anchor. */
    if (open) {
      try {
        if (typeof ILProgress !== 'undefined' && ILProgress) ILProgress.touch(COURSE.courseId, m.id);
      } catch (e) {}
      /* Arm the end-of-module auto-mark for this open session. */
      autoMarked = false;
      try {
        if (autoMarking) { autoMarking.disconnect(); autoMarking = null; }
        if (typeof IntersectionObserver !== 'undefined') {
          var obs = new IntersectionObserver(function (entries) {
            if (entries && entries[0] && entries[0].isIntersecting) autoMarkCheck();
          }, { threshold: 0.9 });
          obs.observe(foot);
          autoMarking = obs;
        }
      } catch (e) {}
    } else {
      try { if (autoMarking) { autoMarking.disconnect(); autoMarking = null; } } catch (e) {}
    }
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
    '<p class="section-sub">' + COURSE.modules.length + ' modules. Follow the guided path in order — ' +
    'each module unlocks the next. Open a module, work its notes, ' +
    'flip the cards, pass the quick checks (≥70% mastery) — then mark it complete.</p>' +
    '<div id="ilgd-rail" aria-live="polite"></div>' +
    '<div id="mod-list"></div>' +
    '<div id="study-noah"></div>';
  var list = $('#mod-list', root);
  COURSE.modules.forEach(function (m) { list.appendChild(moduleHTML(m)); });
  $('#study-noah', root).appendChild(noahPanel('Study — ' + COURSE.title, COURSE.title));
  /* 2026-10-08 (WORKSTREAM 2): guided engine — paint path rail, enforce locks. */
  try { if (typeof Guided !== 'undefined' && Guided.refresh) Guided.refresh(); } catch (e) {}
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

  if (COURSE.glossary.length) {
    html += '<h2 class="section-title">Glossary</h2><div class="card glossary-list">' +
      COURSE.glossary.map(function (g) {
        return '<div class="glossary-item"><div style="font-weight:600">' + esc(g.term) + '</div>' +
          '<div class="small">' + mdLite(g.definition || '') + '</div></div>';
      }).join('') + '</div>';
  }

  if (COURSE.faq.length) {
    html += '<h2 class="section-title">FAQ</h2>' +
      COURSE.faq.map(function (f, i) {
        return '<details class="fold"' + (i === 0 ? ' open' : '') + '><summary>' + esc(f.q) + '</summary>' +
          '<div class="fold-body">' + mdLite(f.a || '') + '</div></details>';
      }).join('');
  }

  if (COURSE.honestyNote) {
    html += '<div class="honesty"><b>Honesty note:</b> ' + esc(COURSE.honestyNote) + '</div>';
  }
  html += '<div class="honesty">Created by Interstitium Labs · SCIENTIA OMNIA VINCIT · ' +
    'All practice content is original. No vendor-exam material is reproduced.</div>';
  root.innerHTML = html;
}

/* ============================== boot =============================== */
/* ============================== Crosswalk (earn-readiness) ============================== */
/* Optional extension: renders when course JSON carries crosswalk / certGates /
   readinessDashboard (IL-26). Other courses are unaffected (tab is hidden). */
var XW_RUN = null; /* active gate-runner state */

function xwalkModMap() {
  var map = {};
  COURSE.modules.forEach(function (m) { map[m.id] = m; });
  return map;
}
function xwalkGateBest(gateId) { return parseFloat(Progress.get('gate:' + gateId + ':best', '0')) || 0; }
function xwalkCertReadiness(cert) {
  var mods = cert.requiredModules || [], done = 0;
  mods.forEach(function (id) { if (Progress.get('module:' + id) === '1') done++; });
  var modPct = mods.length ? (done / mods.length) * 100 : 0;
  var gatePct = xwalkGateBest(cert.gateId);
  var pct = Math.round(0.6 * modPct + 0.4 * gatePct);
  var th = (COURSE.readinessDashboard && COURSE.readinessDashboard.thresholds) || { ready: 85, nearlyReady: 70 };
  var labels = (COURSE.readinessDashboard && COURSE.readinessDashboard.statusLabels) ||
    { ready: 'READY TO SIT', nearlyReady: 'NEARLY READY', inProgress: 'IN PROGRESS' };
  var status = pct >= th.ready ? labels.ready : (pct >= th.nearlyReady ? labels.nearlyReady : labels.inProgress);
  return { pct: pct, status: status, done: done, total: mods.length, gatePct: Math.round(gatePct) };
}
function xwalkDashHTML() {
  var rd = COURSE.readinessDashboard;
  if (!rd || !rd.certs || !rd.certs.length) return '';
  var html = '<h2 class="section-title">Readiness dashboard</h2>' +
    '<p class="section-sub">' + esc(rd.concept || '') + '</p>' +
    '<div class="card"><p class="mono small">' + esc(rd.formula || '') + '</p>' +
    '<ol class="obj-list">' + (rd.howToUse || []).map(function (h) { return '<li>' + esc(h) + '</li>'; }).join('') + '</ol></div>' +
    '<div class="arc-grid">';
  rd.certs.forEach(function (c) {
    var r = xwalkCertReadiness(c);
    var cls = r.status === 'READY TO SIT' ? 'var(--cyan)' : (r.status === 'NEARLY READY' ? '#c9a227' : 'var(--panel3)');
    html += '<div class="arc-card"><div class="phase">' + esc(c.cert) + '</div>' +
      '<div style="margin:8px 0"><b style="font-size:2em;color:' + cls + '">' + r.pct + '%</b> <span class="small">' + esc(r.status) + '</span></div>' +
      '<ul class="obj-list small"><li>Modules ' + r.done + '/' + r.total + ' complete</li>' +
      '<li>Gate best ' + r.gatePct + '% (' + esc(c.gateFormat || '') + ')</li></ul></div>';
  });
  return html + '</div>';
}
function xwalkCertCard(cert, modMap) {
  var tm = cert.trackModule || '';
  var html = '<div class="card" style="margin:14px 0"><h3>' + esc(cert.cert) + '</h3>' +
    '<p class="small muted">' + esc(cert.framing || '') + '</p>' +
    '<h4 class="section-title" style="font-size:1em">Module sequence</h4><ul class="obj-list">';
  (cert.moduleSequence || []).forEach(function (mid) {
    var m = modMap[mid], label = m ? (m.code + ' · ' + m.title) : mid;
    var done = Progress.get('module:' + mid) === '1';
    html += '<li><label style="cursor:pointer"><input type="checkbox" data-xw="mod" data-id="' + esc(mid) + '"' +
      (done ? ' checked' : '') + '> ' + esc(label) + '</label></li>';
  });
  html += '</ul><h4 class="section-title" style="font-size:1em">Domain mapping</h4>';
  (cert.domains || []).forEach(function (d) {
    var mods = (d.modules || []).map(function (mid) { return modMap[mid] ? modMap[mid].code : mid; }).join(', ');
    var prac = (d.practice || []).join(', ');
    html += '<div class="small" style="margin:8px 0;padding:8px;border-left:3px solid var(--cyan)">' +
      '<b>' + esc(d.domain) + '</b> <span class="muted">(' + esc(d.coverage || '') + ')</span><br>' +
      '<span class="muted">Modules:</span> ' + esc(mods) +
      (prac ? '<br><span class="muted">Practice:</span> <span class="mono">' + esc(prac) + '</span>' : '') +
      (d.note ? '<br><span class="muted">' + esc(d.note) + '</span>' : '') + '</div>';
  });
  html += '<h4 class="section-title" style="font-size:1em">Readiness checklist</h4><ul class="obj-list">';
  (cert.readinessChecklist || []).forEach(function (item, i) {
    var done = Progress.get('xwalk:' + tm + ':check:' + i) === '1';
    html += '<li><label style="cursor:pointer"><input type="checkbox" data-xw="check" data-cert="' + esc(tm) + '" data-i="' + i + '"' +
      (done ? ' checked' : '') + '> ' + esc(item) + '</label></li>';
  });
  html += '</ul>';
  var gate = null;
  COURSE.certGates.forEach(function (g) { if (g.trackModule === tm) gate = g; });
  if (gate) {
    var best = xwalkGateBest(gate.id);
    var sessions = parseInt(Progress.get('gate:' + gate.id + ':sessions', '0'), 10) || 0;
    html += '<div class="btn-row" style="margin-top:10px"><button class="btn primary" type="button" data-xw="gate" data-gate="' + esc(gate.id) + '">' +
      'Start practice gate</button><span class="small muted">' + esc(gate.format) + ' · best ' + best + '% · sessions ' + sessions + '</span></div>' +
      '<p class="small muted">' + esc(gate.readinessRule || '') + '</p>';
  }
  return html + '</div>';
}
function xwalkGateRunnerHTML(gate) {
  var st = XW_RUN;
  var html = '<div class="card" style="margin:14px 0;border-color:var(--cyan)"><h3>Practice gate · ' + esc(gate.cert) + '</h3>' +
    '<p class="small muted">' + esc(gate.framing || '') + ' · ' + esc(gate.format) + '</p>' +
    '<div class="mock-head"><div class="mock-timer" id="xw-clock" aria-live="off">--:--:--</div>' +
    '<div class="btn-row" style="margin:0"><button class="btn primary" id="xw-finish" type="button">Finish &amp; score</button>' +
    '<button class="btn ghost" id="xw-close" type="button">Close</button></div></div>' +
    '<h4 class="section-title" style="font-size:1em">Domain weights</h4><ul class="obj-list small">';
  (gate.domainWeights || []).forEach(function (dw) {
    html += '<li>' + esc(dw.domain) + ' — ' + Math.round((dw.weight || 0) * 100) + '% (' + dw.questions + ' questions)</li>';
  });
  html += '</ul><div id="xw-qs">';
  gate.questions.forEach(function (q, qi) {
    html += '<div class="mock-task"><div class="small muted mono">Q' + (qi + 1) + ' / ' + gate.questions.length +
      ' · ' + esc(q.domain || '') + '</div>' +
      '<div class="q" style="font-weight:600;margin:6px 0 10px">' + esc(q.q) + '</div>';
    (q.choices || []).forEach(function (c, ci) {
      var sel = st.answers[qi] === ci;
      html += '<button type="button" class="opt btn ghost" data-xw="gopt" data-q="' + qi + '" data-ci="' + ci + '"' +
        ' style="display:block;width:100%;text-align:left;margin:6px 0' + (sel ? ';border-color:var(--cyan)' : '') + '">' +
        esc(c) + '</button>';
    });
    html += '</div>';
  });
  return html + '</div><div id="xw-result"></div></div>';
}
function xwalkTickClock() {
  if (!XW_RUN || !XW_RUN.running) return;
  var r = Math.max(0, XW_RUN.total - Math.floor((XW_RUN.acc + (Date.now() - XW_RUN.t0)) / 1000));
  var c = document.getElementById('xw-clock');
  if (c) c.textContent = fmtTime(r);
  if (r <= 0) xwalkFinishGate(true);
}
function xwalkFinishGate(auto) {
  var st = XW_RUN; if (!st || st.finished) return;
  st.finished = true; st.running = false;
  if (st.timerId) { clearInterval(st.timerId); st.timerId = null; }
  var gate = st.gate, correct = 0;
  gate.questions.forEach(function (q, qi) { if (st.answers[qi] === q.answer) correct++; });
  var pct = Math.round((correct / gate.questions.length) * 100);
  var prev = xwalkGateBest(gate.id);
  if (pct > prev) Progress.set('gate:' + gate.id + ':best', String(pct));
  Progress.set('gate:' + gate.id + ':sessions', String((parseInt(Progress.get('gate:' + gate.id + ':sessions', '0'), 10) || 0) + 1));
  var res = document.getElementById('xw-result');
  if (res) {
    var html = '<div class="card"><h3>Gate score: ' + pct + '%</h3>' +
      '<p class="small muted">' + (auto ? 'Time expired. ' : '') + correct + ' of ' + gate.questions.length +
      ' correct · best ' + Math.max(prev, pct) + '% · rule: ' + esc(gate.readinessRule || '') + '</p></div>';
    gate.questions.forEach(function (q, qi) {
      var ok = st.answers[qi] === q.answer;
      html += '<div class="mock-task"><div class="small muted mono">Q' + (qi + 1) + ' · ' + esc(q.domain || '') +
        ' — ' + (ok ? 'correct' : 'incorrect') + '</div>' +
        '<div class="q" style="font-weight:600;margin:6px 0">' + esc(q.q) + '</div>' +
        '<ul class="obj-list small">' + q.choices.map(function (c, ci) {
          var mark = ci === q.answer ? ' \u2713' : (st.answers[qi] === ci ? ' \u2717 (your pick)' : '');
          return '<li>' + esc(c) + mark + '</li>';
        }).join('') + '</ul><p class="small">' + esc(q.explain || '') + '</p></div>';
    });
    res.innerHTML = html;
    res.scrollIntoView({ block: 'start' });
  }
  var dash = document.getElementById('xw-dash');
  if (dash) dash.innerHTML = xwalkDashHTML();
}
function buildCrosswalk(root) {
  var modMap = xwalkModMap();
  var rd = COURSE.readinessDashboard || {};
  root.innerHTML = heroHTML() +
    '<h2 class="section-title">Certification crosswalk</h2>' +
    '<p class="section-sub"><b>Certifications you will be prepared to EARN.</b> ' +
    'Independent mappings to public exam objectives \u2014 not affiliated with or endorsed by any vendor. ' +
    'Work each module sequence in order, tick the readiness checklist, then sit the timed practice gate.</p>' +
    '<div id="xw-dash">' + xwalkDashHTML() + '</div>' +
    '<div id="xw-runner"></div>' +
    COURSE.crosswalk.map(function (c) { return xwalkCertCard(c, modMap); }).join('') +
    (rd.framing ? '<p class="small muted">' + esc(rd.framing) + '</p>' : '');
  root.addEventListener('change', function (e) {
    var t = e.target;
    if (t.dataset && t.dataset.xw === 'mod') {
      Progress.set('module:' + t.dataset.id, t.checked ? '1' : null);
      var dash = document.getElementById('xw-dash');
      if (dash) dash.innerHTML = xwalkDashHTML();
    } else if (t.dataset && t.dataset.xw === 'check') {
      Progress.set('xwalk:' + t.dataset.cert + ':check:' + t.dataset.i, t.checked ? '1' : null);
    }
  });
  root.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-xw]') : null;
    if (!b) return;
    var kind = b.dataset.xw;
    if (kind === 'gopt') {
      if (XW_RUN && !XW_RUN.finished) {
        XW_RUN.answers[parseInt(b.dataset.q, 10)] = parseInt(b.dataset.ci, 10);
        var sibs = b.parentElement.querySelectorAll('button.opt');
        for (var i = 0; i < sibs.length; i++) sibs[i].style.borderColor = '';
        b.style.borderColor = 'var(--cyan)';
      }
    } else if (kind === 'gate') {
      var gate = null;
      COURSE.certGates.forEach(function (g) { if (g.id === b.dataset.gate) gate = g; });
      if (!gate) return;
      if (XW_RUN && XW_RUN.timerId) { try { clearInterval(XW_RUN.timerId); } catch (e) {} }
      XW_RUN = { gate: gate, answers: {}, t0: Date.now(), acc: 0, running: true, finished: false,
        total: (gate.minutes || 60) * 60, timerId: null };
      var host = document.getElementById('xw-runner');
      host.innerHTML = xwalkGateRunnerHTML(gate);
      XW_RUN.timerId = setInterval(xwalkTickClock, 1000);
      xwalkTickClock();
      document.getElementById('xw-finish').addEventListener('click', function () { xwalkFinishGate(false); });
      document.getElementById('xw-close').addEventListener('click', function () {
        if (XW_RUN && XW_RUN.timerId) clearInterval(XW_RUN.timerId);
        XW_RUN = null; host.innerHTML = '';
      });
      host.scrollIntoView({ block: 'start' });
    }
  });
}


/* =====================================================================
 * IL-26 extension — Data Analyst Certification Senior Mastery.
 * Everything below is scoped to courseId
 * 'il-26-data-analyst-certification-senior-mastery' and must not alter
 * rendering for any other course. All state uses the existing Progress
 * system (localStorage ilc:<courseId>:<key> + /api/progress sync).
 * ===================================================================== */
function isIL26() {
  return typeof COURSE !== 'undefined' && COURSE &&
    COURSE.courseId === 'il-26-data-analyst-certification-senior-mastery';
}

/* ---- normCourse wrapper: carry IL-26 top-level keys through ---- */
var _il26_normCourse = normCourse;
normCourse = function (raw) {
  var c = _il26_normCourse(raw);
  if (raw && raw.courseId === 'il-26-data-analyst-certification-senior-mastery') {
    ['toolLabs', 'multicloudLabs', 'sampleDatasets', 'installSteps', 'installLabs',
     'installPrereqOrder', 'employerMappings', 'jdMatrix', 'employerCompetencies',
     'sqlPlaygrounds', 'pythonExercises', 'daxPlaygrounds', 'branchingScenarios',
     'clickSims', 'interactivityAudit', 'studyGuide', 'dossierUrl'].forEach(function (k) {
      if (raw[k] !== undefined) c[k] = raw[k];
    });
    if (raw.terminalSims) c.terminalSims = raw.terminalSims;
  }
  return c;
};

/* ================= Stage gating (4a) =================
 * Enforced per-module order: video → reading → drill → lab → mock task.
 * Progress keys: stage:<mid>:video|reading|drill|lab|mock  ("1" when done)
 * video:<mid>:<i> watched flags; note:<mid>:<i> expansion flags;
 * drill:<mid>:<di>:<ii> chosen index; mocktask:<mid> correct flag;
 * install:<id>:cp:<i> checkpoint ticks; install:<id>:done derived.
 */
function il26_stageList(m) {
  var stages = [];
  if ((m.videos || []).length) stages.push('video');
  stages.push('reading');
  if ((m.drills || []).length) stages.push('drill');
  if (m.handsOnLab || il26_moduleToolLabs(m.id).length) stages.push('lab');
  if (m.mockTask) stages.push('mock');
  return stages;
}
function il26_moduleToolLabs(mid) {
  return (COURSE.toolLabs || []).filter(function (t) { return t.moduleId === mid; });
}
function il26_stageDone(m, stage) {
  var mid = m.id;
  if (stage === 'video') {
    var vs = m.videos || [];
    if (!vs.length) return true;
    return vs.every(function (v, i) { return Progress.get('video:' + mid + ':' + i) === '1'; });
  }
  if (stage === 'reading') {
    var notes = m.notes || [], cards = m.cards || [];
    var notesOk = notes.every(function (n, i) { return Progress.get('note:' + mid + ':' + i) === '1'; });
    var cardsOk = cards.every(function (c, i) {
      var v = Progress.get('card:' + mid + ':' + i); return v === 'know' || v === 'again';
    });
    return notesOk && cardsOk;
  }
  if (stage === 'drill') {
    var ds = m.drills || [];
    if (!ds.length) return true;
    return ds.every(function (d, di) {
      return (d.items || []).every(function (it, ii) {
        return Progress.get('drill:' + mid + ':' + di + ':' + ii) === String(it.answer);
      });
    });
  }
  if (stage === 'lab') {
    var labOk = !m.handsOnLab || Progress.get('labdone:' + mid) === '1';
    var toolsOk = il26_moduleToolLabs(mid).every(function (t) {
      return Progress.get('toollab:' + t.id + ':done') === '1';
    });
    return labOk && toolsOk;
  }
  if (stage === 'mock') {
    if (!m.mockTask) return true;
    return Progress.get('mocktask:' + mid) === '1';
  }
  return true;
}
function il26_stageLabel(s) {
  return { video: 'Watch', reading: 'Read', drill: 'Drill', lab: 'Lab', mock: 'Mock task' }[s] || s;
}
function il26_installDone(lab) {
  var cps = lab.checkpoints || [];
  if (!cps.length) return Progress.get('install:' + lab.id + ':done') === '1';
  return cps.every(function (c, i) { return Progress.get('install:' + lab.id + ':cp:' + i) === '1'; });
}
function il26_toolLabUnlocked(t) {
  return (t.requiresInstall || []).every(function (iid) {
    var lab = (COURSE.installLabs || []).filter(function (l) { return l.id === iid; })[0];
    return lab && il26_installDone(lab);
  });
}

/* ================= Objective-level tracker (4b) =================
 * Every learning objective tracked individually. Quiz/drill items map to
 * objectives round-robin (item k -> objective k % n). Score per objective:
 * 40% quiz + 30% drill + 30% applied (lab/mock). Percent-complete = evidence
 * collected / evidence available. Progress keys: quiz:<mid>:<qi> (existing),
 * drill:<mid>:<di>:<ii>, labdone:<mid>, mocktask:<mid>, toollab:<id>:done.
 */
function il26_objectiveStats(m) {
  var objs = m.objectives || [];
  var n = objs.length;
  if (!n) return [];
  var quiz = m.quiz || [];
  var ditems = [];
  (m.drills || []).forEach(function (d) { (d.items || []).forEach(function (it) { ditems.push(it); }); });
  var applied = [];
  if (m.handsOnLab) applied.push(Progress.get('labdone:' + m.id) === '1' ? 1 : 0);
  if (m.mockTask) applied.push(Progress.get('mocktask:' + m.id) === '1' ? 1 : 0);
  il26_moduleToolLabs(m.id).forEach(function (t) {
    applied.push(Progress.get('toollab:' + t.id + ':done') === '1' ? 1 : 0);
  });
  var appliedAvg = applied.length ? applied.reduce(function (a, b) { return a + b; }, 0) / applied.length : null;
  var out = [];
  for (var oi = 0; oi < n; oi++) {
    var qIdx = [], dIdx = [];
    quiz.forEach(function (q, qi) { if (qi % n === oi) qIdx.push(qi); });
    ditems.forEach(function (it, ii) { if (ii % n === oi) dIdx.push(ii); });
    var qOk = 0, qTot = 0;
    qIdx.forEach(function (qi) {
      var ch = Progress.get('quiz:' + m.id + ':' + qi, null);
      if (ch != null) { qTot++; if (String(ch) === String(quiz[qi].answer)) qOk++; }
    });
    var dOk = 0, dTot = 0;
    dIdx.forEach(function (ii) {
      var di = 0, rem = ii, it = null, key = null;
      (m.drills || []).forEach(function (d, ddi) {
        (d.items || []).forEach(function (x, xii) {
          if (di + xii === ii) { it = x; key = 'drill:' + m.id + ':' + ddi + ':' + xii; }
        });
        di += (d.items || []).length;
      });
      if (it && key) {
        var ch2 = Progress.get(key, null);
        if (ch2 != null) { dTot++; if (String(ch2) === String(it.answer)) dOk++; }
      }
    });
    var evAvail = qIdx.length + dIdx.length + applied.length;
    var evGot = qTot + dTot + applied.filter(function (a) { return a === 1; }).length;
    var qScore = qTot ? qOk / qTot : null;
    var dScore = dTot ? dOk / dTot : null;
    var parts = [], wsum = 0;
    if (qScore != null) { parts.push(qScore * 0.4); wsum += 0.4; }
    if (dScore != null) { parts.push(dScore * 0.3); wsum += 0.3; }
    if (appliedAvg != null) { parts.push(appliedAvg * 0.3); wsum += 0.3; }
    var score = wsum ? parts.reduce(function (a, b) { return a + b; }, 0) / wsum : null;
    var status = score == null ? 'ready' : (score >= 0.85 ? 'mastered' : (score >= 0.6 ? 'learning' : 'ready'));
    out.push({
      index: oi, text: objs[oi], score: score,
      pct: evAvail ? Math.round((evGot / evAvail) * 100) : 0, status: status,
      detail: { quiz: qTot ? (qOk + '/' + qTot) : '—', drill: dTot ? (dOk + '/' + dTot) : '—' }
    });
  }
  return out;
}
var IL26_BANDS = [
  { name: 'Foundations', ids: ['IL26-M26', 'IL26-M27', 'IL26-M28'] },
  { name: 'Math', ids: ['IL26-M29', 'IL26-M30', 'IL26-M31', 'IL26-M32', 'IL26-M33', 'IL26-M34'] },
  { name: 'Tools', ids: ['IL26-M08', 'IL26-M09', 'IL26-M10', 'IL26-M11', 'IL26-M12', 'IL26-M13', 'IL26-M14', 'IL26-M15', 'IL26-M16', 'IL26-M17', 'IL26-M18', 'IL26-M25', 'IL26-M41', 'IL26-M42', 'IL26-M43', 'IL26-M44', 'IL26-M45', 'IL26-M46', 'IL26-M47', 'IL26-M48', 'IL26-M49', 'IL26-M50', 'IL26-M51'] },
  { name: 'Certifications', ids: ['IL26-M01', 'IL26-M02', 'IL26-M03', 'IL26-M04', 'IL26-M05', 'IL26-M06', 'IL26-M07', 'IL26-M35', 'IL26-M36', 'IL26-M37', 'IL26-M38', 'IL26-M39', 'IL26-M40'] },
  { name: 'Portfolio', ids: ['IL26-M19', 'IL26-M20', 'IL26-M21', 'IL26-M22', 'IL26-M23', 'IL26-M24'] }
];
function il26_bandProgress(band) {
  var map = {};
  COURSE.modules.forEach(function (m) { map[m.id] = m; });
  var mods = band.ids.map(function (id) { return map[id]; }).filter(Boolean);
  var tot = 0, done = 0, objTot = 0, objMastered = 0;
  mods.forEach(function (m) {
    var stages = il26_stageList(m);
    stages.forEach(function (s) { tot++; if (il26_stageDone(m, s)) done++; });
    il26_objectiveStats(m).forEach(function (o) { objTot++; if (o.status === 'mastered') objMastered++; });
  });
  return {
    name: band.name, modules: mods.length,
    pct: tot ? Math.round((done / tot) * 100) : 0,
    objPct: objTot ? Math.round((objMastered / objTot) * 100) : 0,
    mods: mods
  };
}
function il26_objectivesHTML() {
  var html = '<h2 class="section-title">Objective tracker</h2>' +
    '<p class="section-sub">Every learning objective, tracked individually. ' +
    'Mastery signals come from your quiz and drill scores per objective, plus applied lab/mock evidence. ' +
    'Map runs foundations → math → tools → certifications → portfolio.</p><div class="arc-grid">';
  IL26_BANDS.forEach(function (b) {
    var p = il26_bandProgress(b);
    var cls = p.pct === 100 ? 'var(--cyan)' : (p.pct >= 50 ? '#c9a227' : 'var(--panel3)');
    html += '<div class="arc-card"><div class="phase">' + esc(b.name) + ' · ' + p.modules + ' modules</div>' +
      '<div style="margin:8px 0"><b style="font-size:1.6em;color:' + cls + '">' + p.pct + '%</b> ' +
      '<span class="small">stages complete</span> · <b>' + p.objPct + '%</b> <span class="small">objectives mastered</span></div>' +
      '<div class="small muted">' + p.mods.map(function (m) {
        var st = il26_stageList(m), dn = st.filter(function (s) { return il26_stageDone(m, s); }).length;
        var dot = dn === st.length ? 'var(--cyan)' : (dn > 0 ? '#c9a227' : 'var(--panel3)');
        return '<span title="' + esc(m.title) + ': ' + dn + '/' + st.length + ' stages" style="display:inline-block;width:10px;height:10px;border-radius:50%;background:' + dot + ';margin:2px"></span>';
      }).join('') + '</div></div>';
  });
  return html + '</div>';
}

/* ================= Study guide (3) — course's first section ================= */
function il26_studyGuideHTML() {
  var sg = COURSE.studyGuide;
  if (!sg) return '';
  var html = '<h2 class="section-title">' + esc(sg.title) + '</h2>' +
    '<p class="section-sub">Honest total: <b>' + sg.totalHours + ' hours</b> (' +
    sg.totalMinutes + ' minutes), computed from per-module estimates. ' +
    esc(sg.timeFormula || '') + '</p>';
  var p = sg.pacing || {};
  html += '<div class="card"><h3>Pacing plan — ' + (p.dailyMinutes || 90) + ' min/day, ' +
    (p.daysPerWeek || 5) + ' days/week (~' + (p.estimatedWeeks || '?') + ' weeks)</h3><ul class="obj-list">' +
    (p.plan || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>' +
    '<p class="small muted">' + esc(p.note || '') + '</p></div>';
  var ws = sg.whenStuck || {};
  html += '<div class="card"><h3>' + esc(ws.title || 'When stuck') + '</h3><ol class="obj-list">' +
    (ws.steps || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ol></div>';
  var eo = sg.examOrder || {};
  html += '<div class="card"><h3>' + esc(eo.title || 'Exam order') + '</h3><p class="small">' +
    esc(eo.rule || '') + '</p><ol class="obj-list">' +
    (eo.order || []).map(function (e) {
      return '<li><b>' + esc(e.cert) + '</b> <span class="muted mono small">' + esc(e.gateId) + '</span><br>' +
        '<span class="small">' + esc(e.why) + '</span></li>';
    }).join('') + '</ol></div>';
  return html;
}

/* ================= Interactive renderers (4c) — IL-26 only ================= */

/* ---- SQL playground: DuckDB-WASM via CDN, graceful fallback ---- */
var IL26_DUCKDB = { loading: null, db: null, blocked: false };
function il26_loadDuckDB() {
  if (IL26_DUCKDB.loading) return IL26_DUCKDB.loading;
  IL26_DUCKDB.loading = new Promise(function (resolve) {
    if (IL26_DUCKDB.blocked) { resolve(null); return; }
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/dist/duckdb-browser.js';
    var done = false;
    function finish(db) { if (!done) { done = true; resolve(db); } }
    s.onload = function () {
      try {
        var DUCKDB = window.duckdb;
        var bundles = DUCKDB.getJsDelivrBundles();
        var bundle = bundles.mvp.bundle;
        var worker = new Worker(bundle.mainWorker);
        var logger = new DUCKDB.ConsoleLogger();
        var db = new DUCKDB.AsyncDuckDB(logger, worker);
        db.instantiate(bundle.mainModule, bundle.pthreadWorker).then(function () {
          IL26_DUCKDB.db = db; finish(db);
        }).catch(function () { IL26_DUCKDB.blocked = true; finish(null); });
        setTimeout(function () { if (!IL26_DUCKDB.db) { IL26_DUCKDB.blocked = true; finish(null); } }, 20000);
      } catch (e) { IL26_DUCKDB.blocked = true; finish(null); }
    };
    s.onerror = function () { IL26_DUCKDB.blocked = true; finish(null); };
    setTimeout(function () { if (!done) { IL26_DUCKDB.blocked = true; finish(null); } }, 25000);
    document.head.appendChild(s);
  });
  return IL26_DUCKDB.loading;
}
function il26_sqlValue(v) {
  if (v === null || v === undefined) return 'NULL';
  if (typeof v === 'bigint') return v.toString();
  return String(v);
}
function il26_renderSQLPlayground(pg, host) {
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>' + esc(pg.title) + '</h3>' +
    '<p class="muted small">Dataset: <code>' + esc(pg.dataset.name) + '</code> (' +
    esc(pg.dataset.columns.join(', ')) + ') · DuckDB-WASM in your browser' +
    (pg.moduleId ? ' · module ' + esc(pg.moduleId) : '') + '</p>';
  var prev = el('pre', 'small mono', pg.dataset.columns.join(' | ') + '\n' +
    pg.dataset.rows.slice(0, 5).map(function (r) { return r.join(' | '); }).join('\n') +
    (pg.dataset.rows.length > 5 ? '\n… (' + pg.dataset.rows.length + ' rows)' : ''));
  card.appendChild(prev);
  var tasks = pg.tasks || [];
  tasks.forEach(function (t, ti) {
    var box = el('div', 'mock-task');
    box.innerHTML = '<div class="q" style="font-weight:600;margin:6px 0">Task ' + (ti + 1) + ': ' +
      esc(t.prompt) + '</div>';
    var ta = document.createElement('textarea');
    ta.className = 'term-input'; ta.rows = 5; ta.style.width = '100%';
    ta.value = t.starterSQL || ''; ta.setAttribute('spellcheck', 'false');
    ta.setAttribute('aria-label', 'SQL for ' + pg.title + ' task ' + (ti + 1));
    box.appendChild(ta);
    var row = el('div', 'btn-row');
    var run = el('button', 'btn primary', 'Run query'); run.type = 'button';
    var show = el('button', 'btn ghost', 'Show solution'); show.type = 'button';
    var hintB = el('button', 'btn ghost', 'Hint'); hintB.type = 'button';
    row.appendChild(run); row.appendChild(show); row.appendChild(hintB);
    box.appendChild(row);
    var out = el('div', 'small');
    box.appendChild(out);
    function fallback() {
      out.innerHTML = '<p class="muted">The DuckDB-WASM CDN is blocked or failed to load in this browser, ' +
        'so queries cannot execute here. The task is still fully gradable by inspection:</p>' +
        '<p class="small"><b>Expected:</b> ' + (t.expectedRows || '?') + ' rows.</p>' +
        '<pre class="small mono">' + esc(t.solutionSQL || '') + '</pre>' +
        (t.hint ? '<p class="small"><b>Hint:</b> ' + esc(t.hint) + '</p>' : '');
    }
    run.addEventListener('click', function () {
      out.innerHTML = '<p class="muted">Loading DuckDB-WASM…</p>';
      il26_loadDuckDB().then(function (db) {
        if (!db) { fallback(); return; }
        db.connect().then(function (conn) {
          var cols = pg.dataset.columns.map(function (c) { return '"' + c + '" VARCHAR'; }).join(', ');
          var vals = pg.dataset.rows.map(function (r) {
            return '(' + r.map(function (v) { return "'" + String(v).replace(/'/g, "''") + "'"; }).join(', ') + ')';
          }).join(', ');
          conn.query('CREATE OR REPLACE TABLE "' + pg.dataset.name + '" (' + cols + ')').then(function () {
            return conn.query('INSERT INTO "' + pg.dataset.name + '" VALUES ' + vals);
          }).then(function () {
            return conn.query(ta.value);
          }).then(function (res) {
            var names = res.schema.fields.map(function (f) { return f.name; });
            var rows = res.toArray().map(function (r) {
              return names.map(function (n) { return il26_sqlValue(r[n]); });
            });
            var ok = t.expectedRows ? rows.length === t.expectedRows : true;
            var html = '<p class="' + (ok ? '' : 'muted') + '">' + rows.length + ' rows' +
              (t.expectedRows ? ' (expected ' + t.expectedRows + ')' : '') +
              ' — ' + (ok ? 'row count matches' : 'row count differs; compare with the solution') + '</p>' +
              '<pre class="small mono">' + esc(names.join(' | ') + '\n' +
                rows.slice(0, 20).map(function (r) { return r.join(' | '); }).join('\n')) +
              (rows.length > 20 ? '\n… (' + rows.length + ' rows)' : '') + '</pre>';
            out.innerHTML = html;
            if (ok && t.expectedRows) Progress.set('sqlpg:' + pg.id + ':' + ti, '1');
          }).catch(function (e) {
            out.innerHTML = '<p>Query error: ' + esc(e && e.message || e) + '</p>';
          }).finally(function () { try { conn.close(); } catch (e) {} });
        }).catch(function (e) {
          out.innerHTML = '<p>Database connection error: ' + esc(e && e.message || String(e)) + '</p>';
        });
      });
    });
    show.addEventListener('click', function () {
      out.innerHTML = '<pre class="small mono">' + esc(t.solutionSQL || 'No solution recorded.') + '</pre>';
    });
    hintB.addEventListener('click', function () {
      out.innerHTML = '<p class="small"><b>Hint:</b> ' + esc(t.hint || 'No hint recorded.') + '</p>';
    });
    card.appendChild(box);
  });
  host.appendChild(card);
}

/* ---- Python exercises: Pyodide via CDN, graceful fallback to static check ---- */
var IL26_PYODIDE = { loading: null, py: null, blocked: false };
function il26_loadPyodide() {
  if (IL26_PYODIDE.loading) return IL26_PYODIDE.loading;
  IL26_PYODIDE.loading = new Promise(function (resolve) {
    if (IL26_PYODIDE.blocked) { resolve(null); return; }
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js';
    var done = false;
    function finish(py) { if (!done) { done = true; resolve(py); } }
    s.onload = function () {
      try {
        window.loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/' }).then(function (py) {
          IL26_PYODIDE.py = py; finish(py);
        }).catch(function () { IL26_PYODIDE.blocked = true; finish(null); });
        setTimeout(function () { if (!IL26_PYODIDE.py) { IL26_PYODIDE.blocked = true; finish(null); } }, 45000);
      } catch (e) { IL26_PYODIDE.blocked = true; finish(null); }
    };
    s.onerror = function () { IL26_PYODIDE.blocked = true; finish(null); };
    setTimeout(function () { if (!done) { IL26_PYODIDE.blocked = true; finish(null); } }, 50000);
    document.head.appendChild(s);
  });
  return IL26_PYODIDE.loading;
}
function il26_renderPythonExercise(ex, host) {
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>' + esc(ex.title) + '</h3>' +
    '<p class="muted small">Python in your browser via Pyodide' +
    (ex.moduleId ? ' · module ' + esc(ex.moduleId) : '') + '</p>';
  (ex.tasks || []).forEach(function (t, ti) {
    var box = el('div', 'mock-task');
    box.innerHTML = '<div class="q" style="font-weight:600;margin:6px 0">Task ' + (ti + 1) + ': ' +
      esc(t.prompt) + '</div>';
    var ta = document.createElement('textarea');
    ta.className = 'term-input'; ta.rows = 4; ta.style.width = '100%';
    ta.value = t.starterCode || ''; ta.setAttribute('spellcheck', 'false');
    box.appendChild(ta);
    var row = el('div', 'btn-row');
    var run = el('button', 'btn primary', 'Run & check'); run.type = 'button';
    var show = el('button', 'btn ghost', 'Show solution'); show.type = 'button';
    row.appendChild(run); row.appendChild(show);
    box.appendChild(row);
    var out = el('div', 'small');
    box.appendChild(out);
    function staticFallback() {
      out.innerHTML = '<p class="muted">The Pyodide CDN is blocked or failed to load, so code cannot execute here. ' +
        'The task remains gradable by static inspection — compare your code with the solution:</p>' +
        '<pre class="small mono">' + esc(t.solutionCode || '') + '</pre>' +
        '<ul class="obj-list small">' + (t.checks || []).map(function (c) {
          return '<li>Check: ' + esc(c.description || '') + '</li>';
        }).join('') + '</ul>';
    }
    run.addEventListener('click', function () {
      out.innerHTML = '<p class="muted">Loading Pyodide (first run downloads ~10 MB)…</p>';
      il26_loadPyodide().then(function (py) {
        if (!py) { staticFallback(); return; }
        try {
          var code = ta.value + '\n__il26_results = []\n';
          (t.checks || []).forEach(function (c, ci) {
            code += '__il26_results.append((' + JSON.stringify(c.description || ('check ' + (ci + 1))) +
              ', bool(' + (c.test || 'True') + ')))\n';
          });
          py.runPython(code);
          var res = py.globals.get('__il26_results').toJs();
          var allOk = res.every(function (r) { return r[1]; });
          out.innerHTML = '<ul class="obj-list">' + res.map(function (r) {
            return '<li>' + (r[1] ? '✓' : '✗') + ' ' + esc(r[0]) + '</li>';
          }).join('') + '</ul>';
          if (allOk) Progress.set('pyex:' + ex.id + ':' + ti, '1');
        } catch (e) {
          out.innerHTML = '<p>Python error: ' + esc(e && e.message || e) + '</p>';
        }
      });
    });
    show.addEventListener('click', function () {
      out.innerHTML = '<pre class="small mono">' + esc(t.solutionCode || 'No solution recorded.') + '</pre>';
    });
    card.appendChild(box);
  });
  host.appendChild(card);
}

/* ---- DAX grader: normalize whitespace/case, match accept lists ---- */
function il26_normDAX(s) {
  return String(s || '').toLowerCase().replace(/\s+/g, ' ').replace(/:=/g, '=').replace(/\s*([=\(\),])\s*/g, '$1').trim();
}
function il26_renderDAXPlayground(dg, host) {
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>' + esc(dg.title) + '</h3>' +
    '<p class="muted small">DAX is graded locally: whitespace and case are ignored; your measure must match an accepted form' +
    (dg.moduleId ? ' · module ' + esc(dg.moduleId) : '') + '</p>';
  (dg.tasks || []).forEach(function (t, ti) {
    var box = el('div', 'mock-task');
    box.innerHTML = '<div class="q" style="font-weight:600;margin:6px 0">Task ' + (ti + 1) + ': ' +
      esc(t.prompt) + (t.table ? ' <span class="muted small">Table: <code>' + esc(t.table) + '</code></span>' : '') + '</div>';
    var input = document.createElement('input');
    input.className = 'term-input'; input.style.width = '100%';
    input.setAttribute('spellcheck', 'false');
    input.setAttribute('aria-label', 'DAX measure for ' + dg.title + ' task ' + (ti + 1));
    input.placeholder = 'Total Revenue := SUM(Sales[Amount])';
    box.appendChild(input);
    var row = el('div', 'btn-row');
    var check = el('button', 'btn primary', 'Check measure'); check.type = 'button';
    row.appendChild(check);
    box.appendChild(row);
    var out = el('div', 'small');
    box.appendChild(out);
    check.addEventListener('click', function () {
      var norm = il26_normDAX(input.value);
      var accepts = (t.accept || []).concat(t.expectedDAX ? [t.expectedDAX] : []).map(il26_normDAX);
      var ok = accepts.some(function (a) { return a === norm; });
      out.innerHTML = ok
        ? '<p>✓ Accepted.' + (t.explain ? ' ' + esc(t.explain) : '') + '</p>'
        : '<p>✗ Not yet. ' + esc(t.explain || 'Compare with the expected form.') + '</p>' +
          '<p class="muted">Expected shape: <code>' + esc(t.expectedDAX || '') + '</code></p>';
      if (ok) Progress.set('dax:' + dg.id + ':' + ti, '1');
    });
    card.appendChild(box);
  });
  host.appendChild(card);
}

/* ---- Terminal sim (graded): variants split on "|", hint after 2 failures ---- */
function il26_renderGradedTerm(sim, host) {
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>' + esc(sim.title) + '</h3><p class="muted small">' + esc(sim.scenario || '') + '</p>';
  var screen = el('div', 'term-screen');
  var row = el('div', 'term-input-row');
  row.innerHTML = '<span class="term-prompt">$</span>';
  var input = document.createElement('input');
  input.className = 'term-input'; input.setAttribute('autocomplete', 'off');
  input.setAttribute('spellcheck', 'false');
  input.setAttribute('aria-label', 'Terminal input for ' + sim.title);
  row.appendChild(input);
  var term = el('div', 'term');
  term.appendChild(screen); term.appendChild(row);
  card.appendChild(term);
  host.appendChild(card);
  var cmds = (sim.gradedCommands || []).map(function (g) {
    return { variants: String(g.command || '').split('|').map(function (v) { return v.trim(); }), out: g.response || '', hint: g.hint || '' };
  });
  var idx = 0, fails = {};
  function print(t) { screen.textContent += t + '\n'; screen.scrollTop = screen.scrollHeight; }
  print('# ' + sim.title);
  print('# type the expected command; `hint` shows a nudge');
  function normCmd(s) { return s.trim().replace(/\s+/g, ' '); }
  input.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter') return;
    var raw = normCmd(input.value);
    input.value = '';
    print('$ ' + raw);
    if (raw === 'hint') {
      print(cmds[idx] && cmds[idx].hint ? 'hint: ' + cmds[idx].hint : 'no hint recorded');
      return;
    }
    var cur = cmds[idx];
    if (!cur) { print('scenario complete.'); return; }
    var ok = cur.variants.some(function (v) { return normCmd(v) === raw; });
    if (ok) {
      print(cur.out);
      Progress.set('gterm:' + sim.id + ':' + idx, '1');
      fails[idx] = 0; idx++;
      if (idx >= cmds.length) {
        print('# scenario complete — well done.');
        Progress.set('gterm:' + sim.id + ':done', '1');
      }
    } else {
      fails[idx] = (fails[idx] || 0) + 1;
      print('not quite.' + (fails[idx] >= 2 && cur.hint ? ' hint: ' + cur.hint : ' (type `hint` for a nudge)'));
    }
  });
}

/* ---- Branching scenario player ---- */
function il26_renderBranching(bs, host) {
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>' + esc(bs.title) + '</h3>' +
    (bs.moduleId ? '<p class="muted small">module ' + esc(bs.moduleId) + '</p>' : '');
  var body = el('div');
  card.appendChild(body);
  host.appendChild(card);
  var fails = 0;
  function showNode(nid) {
    var node = (bs.nodes || {})[nid];
    if (!node) { body.innerHTML = '<p class="muted">Scenario complete.</p>'; return; }
    var html = '<div class="mock-task"><p>' + esc(node.text || '') + '</p>';
    (node.choices || []).forEach(function (c, ci) {
      html += '<button type="button" class="opt btn ghost" data-ci="' + ci +
        '" style="display:block;width:100%;text-align:left;margin:6px 0">' + esc(c.label) + '</button>';
    });
    html += '<div class="small" data-fb style="margin-top:8px"></div></div>';
    body.innerHTML = html;
    $all('[data-ci]', body).forEach(function (b) {
      b.addEventListener('click', function () {
        var c = node.choices[+b.dataset.ci];
        var fb = $('[data-fb]', body);
        fb.innerHTML = '<b>Feedback:</b> ' + esc(c.feedback || '');
        $all('[data-ci]', body).forEach(function (x) { x.disabled = true; });
        b.style.borderColor = 'var(--cyan)';
        if (c.next) {
          var nx = el('button', 'btn primary', 'Continue'); nx.type = 'button';
          nx.style.marginTop = '8px';
          nx.addEventListener('click', function () { showNode(c.next); });
          fb.appendChild(document.createElement('br'));
          fb.appendChild(nx);
        } else {
          Progress.set('branch:' + bs.id + ':done', '1');
          fb.innerHTML += '<p class="muted">Scenario complete.</p>';
        }
      });
    });
  }
  showNode(bs.start);
}

/* ---- Click-through sim player: mock UI screens with hotspots ---- */
function il26_renderClickSim(cs, host) {
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>' + esc(cs.title) + '</h3>' +
    '<p class="muted small">Tool: ' + esc(cs.tool || '') +
    (cs.moduleId ? ' · module ' + esc(cs.moduleId) : '') + '</p>';
  var body = el('div');
  card.appendChild(body);
  host.appendChild(card);
  var si = 0, fails = 0;
  function showStep() {
    var st = (cs.steps || [])[si];
    if (!st) {
      body.innerHTML = '<p>✓ Simulation complete.</p>';
      Progress.set('clicksim:' + cs.id + ':done', '1');
      return;
    }
    var html = '<div class="mock-task"><p class="small muted">Screen ' + (si + 1) + ' / ' + cs.steps.length +
      ': ' + esc(st.screen || '') + '</p>' +
      '<p><b>Do this:</b> ' + esc(st.instruction || '') + '</p><p class="small muted">Click the target hotspot:</p><div>';
    (st.hotspots || []).forEach(function (h, hi) {
      html += '<button type="button" class="opt btn ghost" data-h="' + hi + '" style="margin:4px">' +
        esc(h) + '</button>';
    });
    html += '</div><div class="small" data-fb style="margin-top:8px"></div></div>';
    body.innerHTML = html;
    $all('[data-h]', body).forEach(function (b) {
      b.addEventListener('click', function () {
        var fb = $('[data-fb]', body);
        fb.innerHTML = '<b>' + esc(st.feedback || 'Correct.') + '</b>';
        Progress.set('clicksim:' + cs.id + ':' + si, '1');
        si++;
        var nx = el('button', 'btn primary', si < cs.steps.length ? 'Next screen' : 'Finish');
        nx.type = 'button'; nx.style.marginTop = '8px';
        nx.addEventListener('click', showStep);
        fb.appendChild(document.createElement('br'));
        fb.appendChild(nx);
      });
    });
  }
  showStep();
}

/* ---- Module drill / handsOnLab / mockTask renderers ---- */
function il26_renderModuleDrills(m, host) {
  (m.drills || []).forEach(function (d) {
    var card = el('div', 'scriptlab');
    card.innerHTML = '<h3>' + esc(d.title || 'Drill') + '</h3>';
    (d.items || []).forEach(function (it, ii) {
      var key = 'drill:' + m.id + ':' + (m.drills.indexOf(d)) + ':' + ii;
      var chosen = Progress.get(key, null);
      /* Heal pre-fix state: the old renderer stored wrong picks and disabled
         every option, permanently bricking the drill stage. A stored wrong
         value is not a completed drill — clear it so the learner can retry. */
      if (chosen != null && String(chosen) !== String(it.answer)) {
        Progress.set(key, null);
        chosen = null;
      }
      var box = el('div', 'quiz' + (chosen != null ? ' answered' : ''));
      box.innerHTML = '<div class="q">Drill ' + (ii + 1) + ': ' + esc(it.q) + '</div>';
      var opts = el('div');
      it.choices.forEach(function (c, ci) {
        var b = el('button', 'opt', esc(c));
        b.type = 'button';
        if (chosen != null) {
          b.disabled = true;
          if (ci === it.answer) b.classList.add('right');
          else if (String(ci) === String(chosen)) b.classList.add('wrong');
        }
        b.addEventListener('click', function () {
          if (ci !== it.answer) {
            /* Wrong pick: flag it and allow a retry. Nothing is persisted, so
               a wrong answer can never brick the drill stage gate. */
            b.classList.add('wrong');
            /* 2026-10-08 (WORKSTREAM 3): struggle detection → Noah nudge.
               Never auto-sends; the nudge only opens Noah. */
            try {
              if (typeof IL !== 'undefined' && IL && IL.noahTutor)
                IL.noahTutor.recordAnswer(m, 'drill:' + (m.drills.indexOf(d)) + ':' + ii, it.q, false, box);
            } catch (e) {}
            return;
          }
          Progress.set(key, String(ci));
          $all('.opt', opts).forEach(function (o, oi) {
            o.disabled = true;
            if (oi === it.answer) o.classList.add('right');
            else if (oi === ci) o.classList.add('wrong');
          });
          var why = $('.drill-why', box);
          if (why) why.style.display = '';
          box.classList.add('answered');
          /* 2026-10-08 (WORKSTREAM 3): correct drill answer resets the
             struggle streak for this item. */
          try {
            if (typeof IL !== 'undefined' && IL && IL.noahTutor)
              IL.noahTutor.recordAnswer(m, 'drill:' + (m.drills.indexOf(d)) + ':' + ii, it.q, true, box);
          } catch (e) {}
          refreshReadiness();
          il26_rebuildStagesNear(box);
        });
        opts.appendChild(b);
      });
      box.appendChild(opts);
      var why = el('div', 'why drill-why', '<b>Why:</b> ' + esc(it.explain || ''));
      if (chosen == null) why.style.display = 'none';
      box.appendChild(why);
      card.appendChild(box);
    });
    host.appendChild(card);
  });
}
function il26_renderHandsOnLab(m, host) {
  var lab = m.handsOnLab;
  if (!lab) return;
  var done = Progress.get('labdone:' + m.id) === '1';
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>Hands-on lab: ' + esc(lab.title) + '</h3>' +
    '<p>' + esc(lab.brief || '') + '</p>' +
    '<ol class="obj-list">' + (lab.steps || []).map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ol>' +
    '<p class="small"><b>Deliverable:</b> ' + esc(lab.deliverable || '') + '</p>' +
    '<p class="small muted"><b>Checkpoint:</b> ' + esc(lab.checkpoint || '') + '</p>';
  var btn = el('button', 'btn' + (done ? '' : ' primary'), done ? '✓ Lab complete' : 'Mark lab complete');
  btn.type = 'button';
  btn.addEventListener('click', function () {
    var now = !(Progress.get('labdone:' + m.id) === '1');
    Progress.set('labdone:' + m.id, now ? '1' : null);
    btn.textContent = now ? '✓ Lab complete' : 'Mark lab complete';
    btn.classList.toggle('primary', !now);
    refreshReadiness();
    il26_rebuildStagesNear(btn);
  });
  var row = el('div', 'btn-row'); row.appendChild(btn); card.appendChild(row);
  host.appendChild(card);
}
function il26_renderMockTask(m, host) {
  var t = m.mockTask;
  if (!t) return;
  var key = 'mocktask:' + m.id;
  var chosen = Progress.get(key, null);
  /* Heal pre-fix state: the old renderer stored the raw picked index on every
     attempt, which never satisfied the '1' stage-gate check and locked the
     mock stage after a single wrong answer. Only '1' (correct) is valid now. */
  if (chosen != null && chosen !== '1') { Progress.set(key, null); chosen = null; }
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>Mock task</h3><div class="q" style="font-weight:600;margin:6px 0">' + esc(t.q) + '</div>';
  var opts = el('div');
  (t.choices || []).forEach(function (c, ci) {
    var b = el('button', 'opt', esc(c));
    b.type = 'button';
    if (chosen != null) {
      b.disabled = true;
      if (ci === t.answer) b.classList.add('right');
    }
    b.addEventListener('click', function () {
      if (ci !== t.answer) {
        /* Wrong pick: flag it and allow a retry. Only a correct answer is
           persisted ('1'), which is exactly what the mock stage gate checks. */
        b.classList.add('wrong');
        return;
      }
      Progress.set(key, '1');
      $all('.opt', opts).forEach(function (o, oi) {
        o.disabled = true;
        if (oi === t.answer) o.classList.add('right');
      });
      var why = $('.mock-why', card);
      if (why) why.style.display = '';
      refreshReadiness();
      il26_rebuildStagesNear(card);
    });
    opts.appendChild(b);
  });
  card.appendChild(opts);
  var why = el('div', 'why mock-why', '<b>Why:</b> ' + esc(t.explain || ''));
  if (chosen == null) why.style.display = 'none';
  card.appendChild(why);
  host.appendChild(card);
}
function il26_renderModuleVideos(m, host) {
  if (!(m.videos || []).length) return;
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>Videos</h3><p class="small muted">Third-party videos are linked, not hosted. ' +
    'Watch in order; each unlocks the next stage.</p>';
  m.videos.forEach(function (v, i) {
    var watched = Progress.get('video:' + m.id + ':' + i) === '1';
    var row = el('div', 'mock-task');
    row.innerHTML = '<div><b>' + (i + 1) + '. ' + esc(v.title) + '</b> ' +
      '<span class="muted small">(' + esc(v.source || '') + (v.durationMin ? ' · ' + esc(String(v.durationMin)) + ' min' : '') +
      (v.watchBefore ? ' · watch before ' + esc(v.watchBefore) : '') + ')</span></div>' +
      '<div class="small muted">' + esc(v.blurb || '') + '</div>' +
      '<div class="btn-row" style="margin-top:6px"><a class="btn ghost" href="' + esc(v.url) +
      '" target="_blank" rel="noopener">Watch</a></div>';
    var btn = el('button', 'btn' + (watched ? '' : ' primary'), watched ? '✓ Watched' : 'Mark watched');
    btn.type = 'button';
    btn.addEventListener('click', function () {
      var now = !(Progress.get('video:' + m.id + ':' + i) === '1');
      Progress.set('video:' + m.id + ':' + i, now ? '1' : null);
      btn.textContent = now ? '✓ Watched' : 'Mark watched';
      btn.classList.toggle('primary', !now);
      il26_rebuildStagesNear(btn);
    });
    $('.btn-row', row).appendChild(btn);
    card.appendChild(row);
  });
  host.appendChild(card);
}

/* ================= Rich media (4d) — IL-26 only =================
 * Lightweight SVG/Canvas: function grapher, distribution shader, SQL
 * execution-order diagram, ETL pipeline diagram, regression fitter.
 * All drawing is original code; no chart library is bundled.
 */

/* Safe expression evaluator: x, numbers, + - * / ^ ( ) and
   sin cos tan exp log sqrt abs floor ceil min max PI E */
function il26_parseExpr(src) {
  var s = String(src).replace(/\^/g, '**'), i = 0;
  function peek() { return s[i]; }
  function eatSp() { while (s[i] === ' ' || s[i] === '\t') i++; }
  function parseE() {
    var v = parseT();
    for (;;) { eatSp(); var c = peek(); if (c === '+' || c === '-') { i++; var r = parseT(); v = c === '+' ? v + r : v - r; } else return v; }
  }
  function parseT() {
    var v = parseF();
    for (;;) { eatSp(); var c = peek(); if (c === '*' || c === '/') { i++; var r = parseF(); v = c === '*' ? v * r : v / r; } else return v; }
  }
  function parseF() {
    eatSp(); var v = parseP(); eatSp();
    if (s.substr(i, 2) === '**') { i += 2; var e = parseF(); v = Math.pow(v, e); }
    return v;
  }
  function parseP() {
    eatSp();
    var c = peek();
    if (c === '-') { i++; return -parseP(); }
    if (c === '(') { i++; var v = parseE(); eatSp(); if (peek() === ')') i++; return v; }
    var m = /^[a-zA-Z_][a-zA-Z0-9_]*/.exec(s.slice(i));
    if (m) {
      var name = m[0]; i += name.length; eatSp();
      if (name === 'x') return (typeof il26_parseExpr._x === 'number') ? il26_parseExpr._x : NaN;
      if (name === 'PI') return Math.PI;
      if (name === 'E') return Math.E;
      var fns = { sin: Math.sin, cos: Math.cos, tan: Math.tan, exp: Math.exp, log: Math.log, sqrt: Math.sqrt, abs: Math.abs, floor: Math.floor, ceil: Math.ceil };
      if (fns[name] && peek() === '(') { i++; var a = parseE(); eatSp(); if (peek() === ')') i++; var r2 = fns[name](a); return r2; }
      if (name === 'min' || name === 'max') {
        if (peek() === '(') { i++; var args = [parseE()]; eatSp(); while (peek() === ',') { i++; args.push(parseE()); eatSp(); } if (peek() === ')') i++; return name === 'min' ? Math.min.apply(null, args) : Math.max.apply(null, args); }
      }
      throw new Error('unknown name ' + name);
    }
    var n = /^\d*\.?\d+(e[+-]?\d+)?/i.exec(s.slice(i));
    if (n) { i += n[0].length; return parseFloat(n[0]); }
    throw new Error('unexpected ' + c);
  }
  var val = parseE();
  eatSp();
  if (i < s.length) throw new Error('trailing ' + s.slice(i));
  return val;
}
function il26_evalExpr(src, x) {
  il26_parseExpr._x = x;
  try { var v = il26_parseExpr(src); return (typeof v === 'number' && isFinite(v)) ? v : NaN; }
  catch (e) { return NaN; }
}

/* Canvas plotter: axes + one or more series + optional shading */
function il26_plot(canvas, opts) {
  var ctx = canvas.getContext('2d');
  var W = canvas.width, H = canvas.height, pad = 34;
  var xs = opts.series.reduce(function (a, s) { return a.concat(s.xs); }, []);
  var ys = opts.series.reduce(function (a, s) { return a.concat(s.ys.filter(function (y) { return isFinite(y); })); }, []);
  var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs);
  var y0 = Math.min.apply(null, ys.concat([0])), y1 = Math.max.apply(null, ys.concat([0]));
  if (x1 === x0) { x1 = x0 + 1; }
  if (y1 === y0) { y1 = y0 + 1; }
  var xr = (x1 - x0) || 1, yr = (y1 - y0) || 1;
  x0 -= xr * 0.04; x1 += xr * 0.04; y0 -= yr * 0.08; y1 += yr * 0.08;
  function X(x) { return pad + (x - x0) / (x1 - x0) * (W - 2 * pad); }
  function Y(y) { return H - pad - (y - y0) / (y1 - y0) * (H - 2 * pad); }
  ctx.clearRect(0, 0, W, H);
  ctx.strokeStyle = '#3a4a5a'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(X(0), pad - 8); ctx.lineTo(X(0), H - pad); ctx.lineTo(W - pad + 8, H - pad); ctx.stroke();
  ctx.fillStyle = '#8aa0b4'; ctx.font = '10px sans-serif';
  ctx.fillText(opts.xlabel || 'x', W - pad - 4, H - pad + 14);
  ctx.fillText(opts.ylabel || 'y', 8, pad - 8);
  (opts.shade || []).forEach(function (sh) {
    ctx.beginPath();
    var started = false;
    sh.xs.forEach(function (x, i) {
      var y = sh.ys[i];
      if (!isFinite(y)) { started = false; return; }
      if (!started) { ctx.moveTo(X(x), Y(0)); ctx.lineTo(X(x), Y(y)); started = true; }
      else ctx.lineTo(X(x), Y(y));
    });
    ctx.lineTo(X(sh.xs[sh.xs.length - 1]), Y(0));
    ctx.closePath();
    ctx.fillStyle = sh.color || 'rgba(0,180,216,0.25)';
    ctx.fill();
  });
  opts.series.forEach(function (s, si) {
    ctx.beginPath();
    var started = false;
    s.xs.forEach(function (x, i) {
      var y = s.ys[i];
      if (!isFinite(y)) { started = false; return; }
      if (!started) { ctx.moveTo(X(x), Y(y)); started = true; }
      else ctx.lineTo(X(x), Y(y));
    });
    ctx.strokeStyle = s.color || (si === 0 ? '#00b4d8' : '#c9a227');
    ctx.lineWidth = 2; ctx.stroke();
  });
  (opts.points || []).forEach(function (p) {
    ctx.beginPath(); ctx.arc(X(p[0]), Y(p[1]), 3.5, 0, 7);
    ctx.fillStyle = p[2] || '#ff6b6b'; ctx.fill();
  });
  if (opts.caption) { ctx.fillStyle = '#8aa0b4'; ctx.fillText(opts.caption, pad, H - 8); }
}
function il26_fnSeries(expr, x0, x1, n) {
  var xs = [], ys = [];
  for (var i = 0; i <= n; i++) { var x = x0 + (x1 - x0) * i / n; xs.push(x); ys.push(il26_evalExpr(expr, x)); }
  return { xs: xs, ys: ys };
}
function il26_normPdf(x, mu, sd) {
  return Math.exp(-0.5 * Math.pow((x - mu) / sd, 2)) / (sd * Math.sqrt(2 * Math.PI));
}

/* Animated SVG pipeline diagram (ETL) */
function il26_pipelineSVG(stages) {
  var w = 620, h = 120, bw = 110, gap = (w - bw * stages.length) / (stages.length + 1);
  var s = '<svg viewBox="0 0 ' + w + ' ' + h + '" style="width:100%;max-width:640px" role="img" aria-label="Pipeline diagram">';
  var xs = [];
  stages.forEach(function (st, i) {
    var x = gap + i * (bw + gap);
    xs.push(x + bw / 2);
    s += '<rect x="' + x + '" y="30" width="' + bw + '" height="60" rx="8" fill="#14232f" stroke="#00b4d8"/>' +
      '<text x="' + (x + bw / 2) + '" y="55" text-anchor="middle" fill="#e8f1f8" font-size="12">' + st[0] + '</text>' +
      '<text x="' + (x + bw / 2) + '" y="72" text-anchor="middle" fill="#8aa0b4" font-size="10">' + st[1] + '</text>';
    if (i > 0) {
      s += '<line x1="' + (x - gap) + '" y1="60" x2="' + x + '" y2="60" stroke="#c9a227" stroke-width="2"/>' +
        '<circle r="4" fill="#c9a227"><animateMotion dur="1.6s" repeatCount="indefinite" path="M' +
        (x - gap) + ',60 L' + x + ',60"/></circle>';
    }
  });
  return s + '</svg>';
}
/* SQL execution-order diagram: written order vs execution order */
function il26_sqlOrderSVG() {
  var written = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT'];
  var execOrd = ['FROM', 'WHERE', 'GROUP BY', 'HAVING', 'SELECT', 'ORDER BY', 'LIMIT'];
  var s = '<svg viewBox="0 0 640 210" style="width:100%;max-width:660px" role="img" aria-label="SQL execution order">';
  s += '<text x="10" y="20" fill="#8aa0b4" font-size="12">Written order</text>';
  written.forEach(function (w, i) {
    var x = 10 + i * 88;
    s += '<rect x="' + x + '" y="30" width="80" height="34" rx="6" fill="#14232f" stroke="#5a6b7d"/>' +
      '<text x="' + (x + 40) + '" y="52" text-anchor="middle" fill="#8aa0b4" font-size="11">' + w + '</text>';
  });
  s += '<text x="10" y="105" fill="#00b4d8" font-size="12">Execution order (click to animate)</text>';
  execOrd.forEach(function (w, i) {
    var x = 10 + i * 88;
    s += '<rect class="il26-sqlstep" data-i="' + i + '" x="' + x + '" y="115" width="80" height="34" rx="6" fill="#14232f" stroke="#00b4d8" style="cursor:pointer"/>' +
      '<text x="' + (x + 40) + '" y="137" text-anchor="middle" fill="#e8f1f8" font-size="11">' + (i + 1) + '. ' + w + '</text>';
  });
  return s + '</svg>';
}

/* Visual lab per math module (M26-M34): presets + interactive controls */
var IL26_VISUAL_PRESETS = {
  'IL26-M26': [
    { kind: 'fn', title: 'Linear: f(x) = 2x + 1 — slope is the rate of change', expr: '2*x+1', x0: -5, x1: 5, note: 'Drag the slope slider: every +1 of slope tips the line steeper. Intercept shifts it up/down.' },
    { kind: 'fn', title: 'Quadratic: f(x) = x^2 - 3x + 2 — roots where it crosses zero', expr: 'x^2-3*x+2', x0: -2, x1: 5, note: 'The parabola crosses y=0 at x=1 and x=2 — those are the roots.' }
  ],
  'IL26-M27': [
    { kind: 'fn', title: 'Transformations: f(x) = (x-2)^2 + 1 shifts right 2, up 1', expr: '(x-2)^2+1', x0: -3, x1: 7, note: 'Inside the function: opposite direction (x-2 moves right). Outside: same direction (+1 moves up).' },
    { kind: 'fn', title: 'Exponential vs linear: 2^x outruns 3x', expr: '2^x', expr2: '3*x', x0: -2, x1: 5, note: 'Exponentials eventually beat any line — the engine of compound growth.' }
  ],
  'IL26-M28': [
    { kind: 'fn', title: 'Logarithm: ln(x) linearizes exponential growth', expr: 'log(x)', x0: 0.1, x1: 10, note: 'log grows fast early, then flattens — that is why log scales compress wide ranges.' }
  ],
  'IL26-M29': [
    { kind: 'fn', title: 'Sigmoid: 1/(1+e^-x) — the logistic curve', expr: '1/(1+exp(-x))', x0: -6, x1: 6, note: 'Maps any input to (0,1): the shape behind logistic regression and churn probabilities.' }
  ],
  'IL26-M30': [
    { kind: 'dist', title: 'Normal distribution: shade any region', note: 'Move the sliders: mean shifts the curve, sd widens it, the shaded band is the probability.' },
    { kind: 'dist', title: 'Sampling distribution: means cluster tighter than individuals', note: 'Larger n → narrower sampling distribution → tighter confidence intervals.' }
  ],
  'IL26-M31': [
    { kind: 'regress', title: 'Least squares: the line that minimizes squared error', note: 'Press regenerate: each dataset fits a new least-squares line. Watch R² move with the noise slider.' }
  ],
  'IL26-M32': [
    { kind: 'dist', title: 'Probability as area: P(a < X < b) is the shaded region', note: 'Probability IS area under the curve. Shade a band and read its probability.' },
    { kind: 'fn', title: 'Binomial shape: C(n,k) p^k (1-p)^(n-k) via cumulative demo', expr: 'exp(-x^2/2)/sqrt(2*PI())', x0: -4, x1: 4, note: 'The bell curve is the limit of the binomial — the Central Limit Theorem in one picture.' }
  ],
  'IL26-M33': [
    { kind: 'regress', title: 'Vectors as arrows: projection is a shadow', note: 'Least squares is a projection: the fitted line is the shadow of y onto the column space of X.' }
  ],
  'IL26-M34': [
    { kind: 'fn', title: 'Derivative as slope: d/dx x^2 = 2x', expr: 'x^2', expr2: '2*x', x0: -3, x1: 3, note: 'Gold: the function. Blue: its slope at every point. Gradient descent walks downhill on the gold curve.' },
    { kind: 'fn', title: 'Diminishing returns: sqrt(x)', expr: 'sqrt(x)', x0: 0, x1: 16, note: 'Slope falls as x grows — the shape of every saturation curve in marketing analytics.' }
  ]
};
function il26_renderVisualLab(m, host) {
  var presets = IL26_VISUAL_PRESETS[m.id];
  if (!presets || !presets.length) return;
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>Visual lab — interactive charts</h3>' +
    '<p class="small muted">Every chart below is computed live in your browser. Move the controls and watch the math move.</p>';
  presets.forEach(function (p, pi) {
    var box = el('div', 'mock-task');
    box.innerHTML = '<div class="q" style="font-weight:600;margin:6px 0">' + esc(p.title) + '</div>' +
      '<p class="small muted">' + esc(p.note || '') + '</p>';
    var cv = document.createElement('canvas');
    cv.width = 560; cv.height = 320; cv.style.width = '100%'; cv.style.maxWidth = '560px';
    cv.style.border = '1px solid var(--panel3)'; cv.style.borderRadius = '8px';
    box.appendChild(cv);
    var ctrls = el('div', 'btn-row');
    box.appendChild(ctrls);
    if (p.kind === 'fn') {
      var exprInput = document.createElement('input');
      exprInput.className = 'term-input'; exprInput.value = p.expr; exprInput.style.width = '220px';
      exprInput.setAttribute('aria-label', 'Function to graph');
      exprInput.setAttribute('spellcheck', 'false');
      var drawB = el('button', 'btn primary', 'Graph'); drawB.type = 'button';
      ctrls.appendChild(exprInput); ctrls.appendChild(drawB);
      var draw = function () {
        var s1 = il26_fnSeries(exprInput.value, p.x0, p.x1, 200);
        var series = [{ xs: s1.xs, ys: s1.ys, color: '#00b4d8' }];
        if (p.expr2) { var s2 = il26_fnSeries(p.expr2, p.x0, p.x1, 200); series.push({ xs: s2.xs, ys: s2.ys, color: '#c9a227' }); }
        il26_plot(cv, { series: series, xlabel: 'x', ylabel: 'f(x)' });
      };
      drawB.addEventListener('click', draw);
      exprInput.addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
      draw();
    } else if (p.kind === 'dist') {
      var mu = 0, sd = 1, a = -1, b = 1;
      var drawD = function () {
        var xs = [], ys = [], sxs = [], sys = [];
        for (var i = 0; i <= 200; i++) {
          var x = mu - 4 * sd + 8 * sd * i / 200;
          xs.push(x); ys.push(il26_normPdf(x, mu, sd));
          if (x >= a && x <= b) { sxs.push(x); sys.push(il26_normPdf(x, mu, sd)); }
        }
        var prob = 0;
        for (var j = 1; j < sxs.length; j++) prob += (sxs[j] - sxs[j - 1]) * (sys[j] + sys[j - 1]) / 2;
        il26_plot(cv, {
          series: [{ xs: xs, ys: ys, color: '#00b4d8' }],
          shade: [{ xs: sxs, ys: sys, color: 'rgba(0,180,216,0.3)' }],
          caption: 'P(' + a.toFixed(2) + ' < X < ' + b.toFixed(2) + ') = ' + prob.toFixed(4)
        });
      };
      [['mean', -3, 3, 0.5], ['sd', 0.5, 3, 0.1], ['a', -4, 4, 0.5], ['b', -4, 4, 0.5]].forEach(function (cfg) {
        var lab = el('label', 'small muted', cfg[0] + ' ');
        var inp = document.createElement('input');
        inp.type = 'range'; inp.min = cfg[1]; inp.max = cfg[2]; inp.step = cfg[3];
        inp.value = cfg[0] === 'mean' ? mu : (cfg[0] === 'sd' ? sd : (cfg[0] === 'a' ? a : b));
        inp.style.width = '90px';
        inp.setAttribute('aria-label', cfg[0]);
        inp.addEventListener('input', function () {
          var v = parseFloat(inp.value);
          if (cfg[0] === 'mean') mu = v; else if (cfg[0] === 'sd') sd = Math.max(0.2, v);
          else if (cfg[0] === 'a') a = v; else b = v;
          drawD();
        });
        lab.appendChild(inp); ctrls.appendChild(lab);
      });
      drawD();
    } else if (p.kind === 'regress') {
      var noise = 1.0, pts = [];
      var regen = function () {
        pts = [];
        for (var i = 0; i < 30; i++) {
          var x = Math.random() * 10;
          pts.push([x, 2 * x + 3 + (Math.random() - 0.5) * 2 * noise * 3]);
        }
        var sx = 0, sy = 0, sxx = 0, sxy = 0, n = pts.length;
        pts.forEach(function (pt) { sx += pt[0]; sy += pt[1]; sxx += pt[0] * pt[0]; sxy += pt[0] * pt[1]; });
        var slope = (n * sxy - sx * sy) / (n * sxx - sx * sx);
        var icept = (sy - slope * sx) / n;
        var ybar = sy / n, ssTot = 0, ssRes = 0;
        pts.forEach(function (pt) { ssTot += Math.pow(pt[1] - ybar, 2); ssRes += Math.pow(pt[1] - (slope * pt[0] + icept), 2); });
        var r2 = 1 - ssRes / ssTot;
        var xs = [], ys = [];
        for (var j = 0; j <= 50; j++) { var xx = j / 5; xs.push(xx); ys.push(slope * xx + icept); }
        il26_plot(cv, {
          series: [{ xs: xs, ys: ys, color: '#c9a227' }], points: pts,
          xlabel: 'x', ylabel: 'y',
          caption: 'fit: y = ' + slope.toFixed(2) + 'x + ' + icept.toFixed(2) + '   R² = ' + r2.toFixed(3)
        });
      };
      var noiseLab = el('label', 'small muted', 'noise ');
      var noiseInp = document.createElement('input');
      noiseInp.type = 'range'; noiseInp.min = 0.1; noiseInp.max = 3; noiseInp.step = 0.1; noiseInp.value = 1;
      noiseInp.setAttribute('aria-label', 'noise');
      noiseInp.addEventListener('input', function () { noise = parseFloat(noiseInp.value); regen(); });
      var rg = el('button', 'btn primary', 'Regenerate data'); rg.type = 'button';
      rg.addEventListener('click', regen);
      noiseLab.appendChild(noiseInp); ctrls.appendChild(noiseLab); ctrls.appendChild(rg);
      regen();
    }
    card.appendChild(box);
  });
  /* SQL execution-order + ETL pipeline diagrams inside tool modules */
  if (m.id === 'IL26-M08' || m.id === 'IL26-M41') {
    var sqlBox = el('div', 'mock-task');
    sqlBox.innerHTML = '<div class="q" style="font-weight:600;margin:6px 0">SQL is written in one order and executed in another</div>' +
      il26_sqlOrderSVG();
    card.appendChild(sqlBox);
    var anim = false;
    $all('.il26-sqlstep', sqlBox).forEach(function (r) {
      r.addEventListener('click', function () {
        if (anim) return; anim = true;
        var steps = $all('.il26-sqlstep', sqlBox), i = 0;
        var t = setInterval(function () {
          steps.forEach(function (x) { x.setAttribute('fill', '#14232f'); });
          if (i >= steps.length) { clearInterval(t); anim = false; return; }
          steps[i].setAttribute('fill', '#0b3d6e'); i++;
        }, 600);
      });
    });
  }
  if (m.id === 'IL26-M12' || m.id === 'IL26-M13' || m.id === 'IL26-M43') {
    var etlBox = el('div', 'mock-task');
    etlBox.innerHTML = '<div class="q" style="font-weight:600;margin:6px 0">Pipeline anatomy: data flows left to right</div>' +
      il26_pipelineSVG([['Source', 'raw events'], ['Extract', 'incremental'], ['Transform', 'dbt models'], ['Load', 'warehouse'], ['Serve', 'BI / API']]);
    card.appendChild(etlBox);
  }
  host.appendChild(card);
}

/* ================= Adaptive math lab (4e) — IL-26 only =================
 * Original design: knowledge check → personalized topic path (M26-M34) →
 * mastery-based progression (demonstrate mastery, not completion) →
 * periodic re-checks for decayed topics → visual mastery map →
 * infinite original practice problems with step-by-step solutions.
 * Progress keys: mathlab:check:<i>, mathlab:mastery:<mid>,
 * mathlab:streak:<mid>, mathlab:last:<mid>, mathlab:level:<mid>.
 */
var IL26_MATH_TOPICS = [
  { mid: 'IL26-M26', name: 'Arithmetic & Algebra' },
  { mid: 'IL26-M27', name: 'Functions & Graphing' },
  { mid: 'IL26-M28', name: 'Exponents & Logarithms' },
  { mid: 'IL26-M29', name: 'Summation Notation' },
  { mid: 'IL26-M30', name: 'Set Theory & Logic' },
  { mid: 'IL26-M31', name: 'Descriptive Statistics' },
  { mid: 'IL26-M32', name: 'Probability' },
  { mid: 'IL26-M33', name: 'Linear Algebra' },
  { mid: 'IL26-M34', name: 'Calculus Concepts' }
];
function il26_rand(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
function il26_pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function il26_shuffle(arr) {
  var a = arr.slice();
  for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
  return a;
}
/* Each generator: function(level 1..3) -> {q, choices[4], answer, steps[]} */
var IL26_MATH_GEN = {
  'IL26-M26': function (lv) {
    var a = il26_rand(2, 9), b = il26_rand(2, 9), c = il26_rand(2, 12);
    if (lv === 1) {
      var ans = a + b * c;
      return { q: 'Evaluate: ' + a + ' + ' + b + ' × ' + c,
        choices: il26_shuffle([ans, a + b * c, (a + b) * c, ans + 1, ans - 2]).slice(0, 4).sort(function (x, y) { return x - y; }),
        answer: 0, steps: ['Multiplication before addition (order of operations).', b + ' × ' + c + ' = ' + (b * c), a + ' + ' + (b * c) + ' = ' + ans] };
    }
    var x = il26_rand(2, 9), m = il26_rand(2, 5);
    var rhs = m * x + il26_rand(1, 6);
    var b2 = rhs - m * x;
    var opts = [x, x + 1, x - 1, x + 2];
    return { q: 'Solve for x: ' + m + 'x + ' + b2 + ' = ' + rhs,
      choices: opts, answer: 0,
      steps: ['Subtract ' + b2 + ' from both sides: ' + m + 'x = ' + (m * x), 'Divide by ' + m + ': x = ' + x] };
  },
  'IL26-M27': function (lv) {
    var m = il26_rand(1, 5) * (Math.random() < 0.5 ? -1 : 1), b = il26_rand(-6, 6), x = il26_rand(-4, 4);
    var fx = 'f(x) = ' + m + 'x ' + (b >= 0 ? '+ ' + b : '− ' + Math.abs(b));
    var ans = m * x + b;
    var opts = il26_shuffle([ans, ans + 2, ans - 3, m * x]).slice(0, 4);
    return { q: 'If ' + fx + ', what is f(' + x + ')?', choices: opts, answer: opts.indexOf(ans),
      steps: ['Substitute x = ' + x + ' into the function.', 'f(' + x + ') = ' + m + '·(' + x + ') ' + (b >= 0 ? '+ ' + b : '− ' + Math.abs(b)) + ' = ' + ans] };
  },
  'IL26-M28': function (lv) {
    if (lv === 1) {
      var e = il26_rand(2, 4);
      var opts = il26_shuffle([Math.pow(2, e), e * 2, Math.pow(2, e) + 1, e * e]).slice(0, 4);
      return { q: 'Evaluate 2^' + e, choices: opts, answer: opts.indexOf(Math.pow(2, e)),
        steps: ['2^' + e + ' means 2 multiplied by itself ' + e + ' times.', 'Result: ' + Math.pow(2, e)] };
    }
    var v = Math.pow(10, il26_rand(1, 3));
    var opts2 = il26_shuffle([Math.log10(v), Math.log10(v) + 1, Math.log10(v) - 1, v / 10]).slice(0, 4);
    return { q: 'log₁₀(' + v + ') = ?', choices: opts2, answer: opts2.indexOf(Math.log10(v)),
      steps: ['log₁₀ asks: 10 to what power gives ' + v + '?', '10^' + Math.log10(v) + ' = ' + v + ', so the answer is ' + Math.log10(v)] };
  },
  'IL26-M29': function (lv) {
    var n = il26_rand(3, 6), k = il26_rand(1, 3);
    var ans = 0; for (var i = 1; i <= n; i++) ans += Math.pow(i, k > 1 ? 2 : 1);
    var expr = k > 1 ? 'i²' : 'i';
    var opts = il26_shuffle([ans, ans + n, ans - 1, n * n]).slice(0, 4);
    return { q: 'Evaluate Σ (i=1 to ' + n + ') ' + expr, choices: opts, answer: opts.indexOf(ans),
      steps: ['Expand the sum term by term.', 'Sum = ' + ans] };
  },
  'IL26-M30': function (lv) {
    var a = il26_rand(10, 30), b = il26_rand(10, 30), inter = il26_rand(2, 8);
    var uni = a + b - inter;
    var opts = il26_shuffle([uni, a + b, uni + 1, Math.abs(a - b)]).slice(0, 4);
    return { q: '|A| = ' + a + ', |B| = ' + b + ', |A ∩ B| = ' + inter + '. What is |A ∪ B|?',
      choices: opts, answer: opts.indexOf(uni),
      steps: ['Inclusion–exclusion: |A ∪ B| = |A| + |B| − |A ∩ B|.', '= ' + a + ' + ' + b + ' − ' + inter + ' = ' + uni] };
  },
  'IL26-M31': function (lv) {
    var n = 5, vals = [];
    for (var i = 0; i < n; i++) vals.push(il26_rand(2, 20) * 2);
    var sum = vals.reduce(function (x, y) { return x + y; }, 0);
    var mean = sum / n;
    var sorted = vals.slice().sort(function (x, y) { return x - y; });
    var med = sorted[2];
    var opts = il26_shuffle([mean, med, mean + 1, sum]).slice(0, 4);
    return { q: 'Data: [' + vals.join(', ') + ']. The mean is?', choices: opts, answer: opts.indexOf(mean),
      steps: ['Sum = ' + sum + ', n = ' + n + '.', 'Mean = ' + sum + ' / ' + n + ' = ' + mean] };
  },
  'IL26-M32': function (lv) {
    var fav = il26_rand(1, 3), tot = il26_rand(4, 6);
    var p = fav / tot;
    var pct = Math.round(p * 100);
    var opts = il26_shuffle([pct + '%', Math.round((1 - p) * 100) + '%', (fav + 1) + '%', '50%']).slice(0, 4);
    return { q: 'A bag has ' + tot + ' marbles, ' + fav + ' red. P(red) on one draw?',
      choices: opts, answer: 0,
      steps: ['Probability = favorable / total = ' + fav + '/' + tot + '.', '= ' + pct + '%'] };
  },
  'IL26-M33': function (lv) {
    var ax = il26_rand(1, 5), ay = il26_rand(1, 5), bx = il26_rand(1, 5), by = il26_rand(1, 5);
    var dot = ax * bx + ay * by;
    var opts = il26_shuffle([dot, dot + 2, ax + bx + ay + by, ax * bx]).slice(0, 4);
    return { q: 'Dot product of (' + ax + ', ' + ay + ') · (' + bx + ', ' + by + ')?',
      choices: opts, answer: 0,
      steps: ['Dot product: multiply matching components, then add.', '= ' + ax + '·' + bx + ' + ' + ay + '·' + by + ' = ' + dot] };
  },
  'IL26-M34': function (lv) {
    var k = il26_rand(2, 4);
    var opts = il26_shuffle([k + 'x', (k - 1) + 'x', k + 'x²', String(k)]).slice(0, 4);
    var ans = k + 'x';
    return { q: 'd/dx of x^' + k + ' is?', choices: opts, answer: opts.indexOf(ans),
      steps: ['Power rule: d/dx xⁿ = n·xⁿ⁻¹.', '= ' + k + '·x^' + (k - 1) + (k - 1 === 1 ? ' = ' + k + 'x' : '')] };
  }
};
/* Knowledge check: one diagnostic question per topic (fixed seed-ish, original) */
var IL26_MATH_CHECK = [
  { mid: 'IL26-M26', q: 'What is 3 + 4 × 2²?', choices: ['19', '28', '11', '24'], answer: 0,
    why: 'Exponents first: 2² = 4. Then multiplication: 4 × 4 = 16. Then addition: 3 + 16 = 19.' },
  { mid: 'IL26-M27', q: 'If f(x) = 2x − 3, what is f(5)?', choices: ['7', '4', '13', '10'], answer: 0,
    why: 'Substitute: f(5) = 2(5) − 3 = 10 − 3 = 7.' },
  { mid: 'IL26-M28', q: 'log₂(32) = ?', choices: ['5', '16', '6', '4'], answer: 0,
    why: '2⁵ = 32, so the base-2 log of 32 is 5.' },
  { mid: 'IL26-M29', q: 'Σ (i=1 to 4) i = ?', choices: ['10', '8', '12', '24'], answer: 0,
    why: '1 + 2 + 3 + 4 = 10.' },
  { mid: 'IL26-M30', q: 'A = {1,2,3}, B = {3,4}. |A ∪ B| = ?', choices: ['4', '5', '3', '6'], answer: 0,
    why: 'Union = {1,2,3,4}: 3 counted once, so 3 + 2 − 1 = 4.' },
  { mid: 'IL26-M31', q: 'Mean of [4, 8, 6, 10]?', choices: ['7', '6', '8', '28'], answer: 0,
    why: '(4 + 8 + 6 + 10) / 4 = 28 / 4 = 7.' },
  { mid: 'IL26-M32', q: 'P(rolling a 6 on a fair die)?', choices: ['1/6', '1/2', '1/3', '6'], answer: 0,
    why: 'One favorable face out of six equally likely faces.' },
  { mid: 'IL26-M33', q: '(1,2) · (3,4) = ?', choices: ['11', '7', '10', '14'], answer: 0,
    why: '1·3 + 2·4 = 3 + 8 = 11.' },
  { mid: 'IL26-M34', q: 'd/dx (x³) = ?', choices: ['3x²', 'x²', '3x', 'x³/3'], answer: 0,
    why: 'Power rule: bring down the 3, reduce the exponent by 1.' }
];
function il26_mathMastery(mid) { return parseFloat(Progress.get('mathlab:mastery:' + mid, '0')) || 0; }
function il26_mathLevel(mid) { return parseInt(Progress.get('mathlab:level:' + mid, '1'), 10) || 1; }
function il26_mathDecayed(mid) {
  var last = parseInt(Progress.get('mathlab:last:' + mid, '0'), 10) || 0;
  return last > 0 && (Date.now() - last) > 14 * 864e5 && il26_mathMastery(mid) >= 60;
}
function il26_renderMathLab(host) {
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>Adaptive math lab</h3>' +
    '<p class="small muted">Original design: a knowledge check places you, then you practice topics ' +
    'until you demonstrate mastery (not just completion). Topics you have not touched in 14+ days ' +
    'resurface for re-checks. Infinite original problems with step-by-step solutions.</p>';
  var mapBox = el('div'); card.appendChild(mapBox);
  var workBox = el('div'); card.appendChild(workBox);
  host.appendChild(card);

  function masteryMap() {
    var html = '<h4 class="section-title" style="font-size:1em">Mastery map</h4><div class="arc-grid">';
    IL26_MATH_TOPICS.forEach(function (t) {
      var m = il26_mathMastery(t.mid), lv = il26_mathLevel(t.mid), dec = il26_mathDecayed(t.mid);
      var st = m >= 85 ? 'mastered' : (m >= 40 || Progress.get('mathlab:check:' + t.mid) ? 'learning' : 'ready');
      var cls = st === 'mastered' ? 'var(--cyan)' : (st === 'learning' ? '#c9a227' : 'var(--panel3)');
      html += '<div class="arc-card" style="border-left:4px solid ' + cls + '"><div class="phase">' + esc(t.name) + '</div>' +
        '<div class="small">' + Math.round(m) + '% mastery · level ' + lv + '/3 · ' + st.toUpperCase() +
        (dec ? ' · <b>RE-CHECK DUE</b>' : '') + '</div>' +
        '<div class="btn-row" style="margin-top:6px"><button type="button" class="btn ghost" data-practice="' +
        esc(t.mid) + '">Practice</button></div></div>';
    });
    mapBox.innerHTML = html + '</div>';
    $all('[data-practice]', mapBox).forEach(function (b) {
      b.addEventListener('click', function () { practice(b.dataset.practice); });
    });
  }
  function knowledgeCheck() {
    var answered = IL26_MATH_CHECK.filter(function (q) { return Progress.get('mathlab:check:' + q.mid, null) != null; }).length;
    if (answered >= IL26_MATH_CHECK.length) return;
    workBox.innerHTML = '<h4 class="section-title" style="font-size:1em">Knowledge check (' +
      answered + '/' + IL26_MATH_CHECK.length + ')</h4><p class="small muted">One diagnostic per topic. ' +
      'This sets your starting path — wrong answers route you to the right module, not a grade.</p>';
    IL26_MATH_CHECK.forEach(function (q, qi) {
      if (Progress.get('mathlab:check:' + q.mid, null) != null) return;
      var box = el('div', 'quiz');
      box.innerHTML = '<div class="q">' + esc(q.q) + ' <span class="muted small">(' + esc(q.mid.replace('IL26-', '')) + ')</span></div>';
      var opts = el('div');
      q.choices.forEach(function (c, ci) {
        var b = el('button', 'opt', esc(c)); b.type = 'button';
        b.addEventListener('click', function () {
          Progress.set('mathlab:check:' + q.mid, ci === q.answer ? '1' : '0');
          if (ci !== q.answer) Progress.set('mathlab:mastery:' + q.mid, '20');
          else Progress.set('mathlab:mastery:' + q.mid, Math.max(il26_mathMastery(q.mid), 45));
          $all('.opt', opts).forEach(function (o, oi) {
            o.disabled = true;
            if (oi === q.answer) o.classList.add('right');
            else if (oi === ci) o.classList.add('wrong');
          });
          var why = el('div', 'why', '<b>Why:</b> ' + esc(q.why));
          box.appendChild(why);
          box.classList.add('answered');
          setTimeout(function () { masteryMap(); knowledgeCheck(); }, 400);
        });
        opts.appendChild(b);
      });
      box.appendChild(opts);
      workBox.appendChild(box);
    });
  }
  function practice(mid) {
    var t = IL26_MATH_TOPICS.filter(function (x) { return x.mid === mid; })[0];
    var gen = IL26_MATH_GEN[mid];
    var lv = il26_mathLevel(mid);
    var p = gen(lv);
    workBox.innerHTML = '<h4 class="section-title" style="font-size:1em">Practice: ' + esc(t.name) +
      ' (level ' + lv + '/3)</h4>';
    var box = el('div', 'quiz');
    box.innerHTML = '<div class="q">' + esc(p.q) + '</div>';
    var opts = el('div');
    p.choices.forEach(function (c, ci) {
      var b = el('button', 'opt', esc(String(c))); b.type = 'button';
      b.addEventListener('click', function () {
        var ok = ci === p.answer;
        var streak = parseInt(Progress.get('mathlab:streak:' + mid, '0'), 10) || 0;
        streak = ok ? streak + 1 : 0;
        Progress.set('mathlab:streak:' + mid, String(streak));
        Progress.set('mathlab:last:' + mid, String(Date.now()));
        var mastery = il26_mathMastery(mid);
        mastery = Math.min(100, mastery + (ok ? (lv * 4) : -6));
        if (streak >= 3 && lv < 3) {
          Progress.set('mathlab:level:' + mid, String(lv + 1));
          Progress.set('mathlab:streak:' + mid, '0');
          mastery = Math.min(100, mastery + 10);
        }
        if (mastery >= 85 && lv === 3) Progress.set('mathlab:mastery:' + mid, '100');
        else Progress.set('mathlab:mastery:' + mid, String(Math.max(0, mastery)));
        $all('.opt', opts).forEach(function (o, oi) {
          o.disabled = true;
          if (oi === p.answer) o.classList.add('right');
          else if (oi === ci) o.classList.add('wrong');
        });
        var why = el('div', 'why', '<b>Step-by-step:</b><ol class="obj-list">' +
          p.steps.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ol>' +
          (streak >= 3 && lv < 3 ? '<p><b>Level up!</b> Harder problems unlocked.</p>' : ''));
        box.appendChild(why);
        var nx = el('button', 'btn primary', 'Next problem'); nx.type = 'button';
        nx.style.marginTop = '8px';
        nx.addEventListener('click', function () { masteryMap(); practice(mid); });
        box.appendChild(nx);
        masteryMap();
      });
      opts.appendChild(b);
    });
    box.appendChild(opts);
    workBox.appendChild(box);
    workBox.scrollIntoView({ block: 'start' });
  }
  masteryMap();
  knowledgeCheck();
}

/* ================= Integration wrappers (IL-26) ================= */

/* ---- quizHTML: instant per-answer explanations (IL-26 hides Why until answered) ---- */
var _il26_quizHTML = quizHTML;
quizHTML = function (mod, qi, q) {
  var box = _il26_quizHTML(mod, qi, q);
  if (isIL26()) {
    var key = 'quiz:' + mod.id + ':' + qi;
    var why = box.querySelector('.why');
    if (why && Progress.get(key, null) == null) why.style.display = 'none';
    var opts = box.querySelectorAll('.opt');
    Array.prototype.forEach.call(opts, function (b) {
      b.addEventListener('click', function () {
        var w = box.querySelector('.why');
        if (w) w.style.display = '';
      });
    });
  }
  return box;
};

/* ---- moduleHTML: stage gating + stage sections (IL-26); full sections (IL-27) ---- */
var _il26_moduleHTML = moduleHTML;
function il27_renderSupplementalResources(m, host) {
  var rs = m.supplementalResources || [];
  if (!rs.length) return;
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>Supplemental resources</h3><p class="small muted">Curated further reading — official docs and references.</p>' +
    '<ul class="obj-list">' + rs.map(function (r) {
      return '<li><a href="' + esc(r.url) + '" target="_blank" rel="noopener">' + esc(r.title) + '</a>' +
        (r.kind ? ' <span class="small muted">(' + esc(r.kind) + ')</span>' : '') + '</li>';
    }).join('') + '</ul>';
  host.appendChild(card);
}
moduleHTML = function (m) {
  var wrap = _il26_moduleHTML(m);
  var body = wrap.querySelector('.mod-body');
  if (!body) return wrap;
  if (isIL27()) {
    /* IL-27: render every content section (no stage gating) */
    il26_renderModuleVideos(m, body);
    il26_renderModuleDrills(m, body);
    il26_renderHandsOnLab(m, body);
    il26_renderMockTask(m, body);
    il27_renderSupplementalResources(m, body);
    return wrap;
  }
  if (!isIL26()) return wrap;

  /* track note expansions for the reading stage */
  var folds = body.querySelectorAll('details.fold');
  Array.prototype.forEach.call(folds, function (d, i) {
    d.addEventListener('toggle', function () {
      if (d.open && Progress.get('note:' + m.id + ':' + i) !== '1') {
        Progress.set('note:' + m.id + ':' + i, '1');
        il26_refreshStages(wrap, m);
      }
    });
  });

  /* stage tracker bar */
  var tracker = el('div', 'il26-stages');
  body.insertBefore(tracker, body.firstChild);

  /* stage content sections (locked until prior stage complete) */
  var stageHost = el('div', 'il26-stagehost');
  body.appendChild(stageHost);

  function buildStages() {
    var stages = il26_stageList(m);
    var th = '<div class="il26-stagebar">';
    var unlocked = true;
    stages.forEach(function (s, si) {
      var done = il26_stageDone(m, s);
      th += '<span class="il26-stagepill ' + (done ? 'done' : (unlocked ? 'open' : 'locked')) + '" title="' +
        esc(il26_stageLabel(s)) + '">' + (done ? '✓ ' : '') + esc(il26_stageLabel(s)) + '</span>';
      if (!done) unlocked = false;
    });
    th += '</div>';
    tracker.innerHTML = th +
      '<p class="small muted">Enforced order: video → reading → drill → lab → mock task. ' +
      'Each stage unlocks when the previous is complete. Progress is saved automatically.</p>';

    stageHost.innerHTML = '';
    var canOpen = true;
    stages.forEach(function (s) {
      var sec = el('div', 'il26-stagesec' + (canOpen ? '' : ' locked'));
      var done = il26_stageDone(m, s);
      sec.innerHTML = '<h3>' + esc(il26_stageLabel(s)) + (done ? ' ✓' : '') + '</h3>' +
        (canOpen ? '' : '<p class="small muted">🔒 Complete the previous stage to unlock.</p>');
      if (canOpen) {
        if (s === 'video') il26_renderModuleVideos(m, sec);
        else if (s === 'drill') il26_renderModuleDrills(m, sec);
        else if (s === 'lab') {
          il26_renderHandsOnLab(m, sec);
          il26_moduleToolLabs(m.id).forEach(function (t) { il26_renderToolLabCard(t, sec); });
        }
        else if (s === 'mock') il26_renderMockTask(m, sec);
        else if (s === 'reading') {
          var os = il26_objectiveStats(m);
          if (os.length) {
            sec.innerHTML += '<h4 class="section-title" style="font-size:1em">Learning objectives — live mastery</h4>';
            os.forEach(function (o) {
              var cls = o.status === 'mastered' ? 'var(--cyan)' : (o.status === 'learning' ? '#c9a227' : 'var(--panel3)');
              sec.innerHTML += '<div class="small" style="margin:6px 0;padding:6px 8px;border-left:3px solid ' + cls + '">' +
                '<b>' + (o.index + 1) + '.</b> ' + esc(o.text) +
                '<br><span class="muted">mastery ' + (o.score == null ? '—' : Math.round(o.score * 100) + '%') +
                ' · evidence ' + o.pct + '% · quiz ' + esc(o.detail.quiz) + ' · drill ' + esc(o.detail.drill) +
                ' · <b>' + o.status.toUpperCase() + '</b></span></div>';
            });
          }
        }
      }
      stageHost.appendChild(sec);
      if (!done) canOpen = false;
    });
    /* visual lab for math modules (always available, never gated) */
    var visHost = el('div');
    il26_renderVisualLab(m, visHost);
    if (visHost.children.length) stageHost.appendChild(visHost);
  }
  buildStages();
  wrap._il26_rebuildStages = function () { buildStages(); };

  /* gate the "Mark module complete" button on stages (IL-26 only) */
  wrap.addEventListener('click', function (e) {
    /* Scope to the module-complete button only: a '.btn-row .btn' selector
       would also swallow stage-completion clicks (Mark watched, Mark lab
       complete, Run query), making stages impossible to finish. */
    var btn = e.target.closest ? e.target.closest('[data-mod-complete]') : null;
    if (!btn) return;
    var stages = il26_stageList(m);
    var remaining = stages.filter(function (s) { return !il26_stageDone(m, s); });
    var marking = !(Progress.get('module:' + m.id) === '1');
    if (marking && remaining.length) {
      e.stopPropagation();
      e.preventDefault();
      var msg = 'Finish these stages first: ' + remaining.map(il26_stageLabel).join(', ');
      var note = wrap.querySelector('.il26-gatemsg');
      if (!note) { note = el('p', 'il26-gatemsg small'); wrap.querySelector('.mod-body').appendChild(note); }
      note.innerHTML = '<b>🔒 ' + esc(msg) + '</b>';
      note.scrollIntoView({ block: 'nearest' });
    }
  }, true);

  return wrap;
};
function il26_refreshStages(wrap, m) {
  if (wrap && wrap._il26_rebuildStages) wrap._il26_rebuildStages();
}

/* Rebuild the stage pills/sections of the module wrap containing `node`.
   Called after video/drill/mock/lab completions so pills and locks update
   live; previously only note-toggles refreshed, leaving stages stale until
   a page reload. Returns false when no stage wrapper is found (e.g. Labs tab). */
function il26_rebuildStagesNear(node) {
  var n = node;
  while (n) {
    if (n._il26_rebuildStages) { try { n._il26_rebuildStages(); } catch (e) {} return true; }
    n = n.parentNode;
  }
  return false;
}

/* ---- tool lab card with install gating ---- */
function il26_renderToolLabCard(t, host) {
  var unlocked = il26_toolLabUnlocked(t);
  var done = Progress.get('toollab:' + t.id + ':done') === '1';
  var card = el('div', 'scriptlab' + (unlocked ? '' : ' locked'));
  var missing = (t.requiresInstall || []).filter(function (iid) {
    var lab = (COURSE.installLabs || []).filter(function (l) { return l.id === iid; })[0];
    return !(lab && il26_installDone(lab));
  });
  card.innerHTML = '<h3>Tool lab: ' + esc(t.title) + (done ? ' ✓' : '') + '</h3>' +
    '<p>' + esc(t.brief || '') + '</p>' +
    (unlocked ? '' : '<p class="small"><b>🔒 Locked.</b> Complete install checkpoint(s): ' +
      missing.map(function (iid) {
        var lab = (COURSE.installLabs || []).filter(function (l) { return l.id === iid; })[0];
        return esc(lab ? lab.tool : iid);
      }).join(', ') + '</p>') +
    (t.datasetRef ? '<p class="small muted">Dataset: <code>' + esc(t.datasetRef) + '</code></p>' : '');
  if (unlocked) {
    card.innerHTML += '<ol class="obj-list">' + (t.steps || []).map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ol>' +
      '<p class="small"><b>Deliverable:</b> ' + esc(t.deliverable || '') + '</p>' +
      '<p class="small muted"><b>Checkpoint:</b> ' + esc(t.checkpoint || '') + '</p>';
    var btn = el('button', 'btn' + (done ? '' : ' primary'), done ? '✓ Tool lab complete' : 'Mark tool lab complete');
    btn.type = 'button';
    btn.addEventListener('click', function () {
      var now = !(Progress.get('toollab:' + t.id + ':done') === '1');
      Progress.set('toollab:' + t.id + ':done', now ? '1' : null);
      btn.textContent = now ? '✓ Tool lab complete' : 'Mark tool lab complete';
      btn.classList.toggle('primary', !now);
      refreshReadiness();
      il26_rebuildStagesNear(btn);
    });
    var row = el('div', 'btn-row'); row.appendChild(btn); card.appendChild(row);
  }
  host.appendChild(card);
}

/* ---- install lab card with checkpoint ticks ---- */
function il26_renderInstallLab(lab, host) {
  var card = el('div', 'scriptlab');
  card.innerHTML = '<h3>Install: ' + esc(lab.tool) + '</h3>' +
    '<p class="small muted">' + esc(lab.category || '') +
    (lab.costNote ? ' · ' + esc(lab.costNote) : '') +
    (lab.estimatedMinutes ? ' · ~' + lab.estimatedMinutes + ' min' : '') + '</p>';
  var plats = lab.platforms || {};
  ['windows', 'macos', 'linux'].forEach(function (pl) {
    if (plats[pl] && plats[pl].steps) {
      card.innerHTML += '<h4 class="section-title" style="font-size:1em">' + pl + '</h4><ol class="obj-list small">' +
        plats[pl].steps.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ol>' +
        (plats[pl].notes ? '<p class="small muted">' + esc(plats[pl].notes) + '</p>' : '');
    }
  });
  card.innerHTML += '<h4 class="section-title" style="font-size:1em">Verification checkpoints</h4>';
  (lab.checkpoints || []).forEach(function (cp, i) {
    var key = 'install:' + lab.id + ':cp:' + i;
    var ticked = Progress.get(key) === '1';
    var lab2 = el('label', 'small', '');
    lab2.style.display = 'block'; lab2.style.cursor = 'pointer'; lab2.style.margin = '6px 0';
    var cb = document.createElement('input');
    cb.type = 'checkbox'; cb.checked = ticked;
    cb.addEventListener('change', function () {
      Progress.set(key, cb.checked ? '1' : null);
      if (il26_installDone(lab)) Progress.set('install:' + lab.id + ':done', '1');
      else Progress.set('install:' + lab.id + ':done', null);
      refreshReadiness();
    });
    lab2.appendChild(cb);
    lab2.appendChild(document.createTextNode(' '));
    var code = el('code', '', esc(cp.command || ''));
    lab2.appendChild(code);
    lab2.appendChild(el('span', 'muted', ' → ' + esc(cp.expected || '')));
    card.appendChild(lab2);
  });
  if ((lab.troubleshoot || []).length) {
    card.innerHTML += '<h4 class="section-title" style="font-size:1em">Troubleshooting</h4><ul class="obj-list small">' +
      lab.troubleshoot.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ul>';
  }
  host.appendChild(card);
}

/* ---- buildStudy wrapper: study guide first, then objective tracker + math lab ---- */
var _il26_buildStudy = buildStudy;
buildStudy = function (root) {
  _il26_buildStudy(root);
  if (!isIL26()) return;
  var guideHost = el('div', 'il26-guide');
  guideHost.innerHTML = il26_studyGuideHTML();
  var h2 = root.querySelector('h2.section-title');
  if (h2) root.insertBefore(guideHost, h2);
  else root.insertBefore(guideHost, root.firstChild);
  var objHost = el('div', 'il26-objectives');
  objHost.innerHTML = il26_objectivesHTML();
  root.appendChild(objHost);
  var mathHost = el('div', 'il26-mathlab');
  root.appendChild(mathHost);
  il26_renderMathLab(mathHost);
};

/* ---- buildLabs wrapper: IL-26 interactive panes ---- */
var _il26_buildLabs = buildLabs;
buildLabs = function (root) {
  _il26_buildLabs(root);
  if (!isIL26()) return;
  var holder = root.querySelector('.lab-panes');
  var nav = root.querySelector('.lab-subnav');
  if (!holder || !nav) return;
  function addILPane(id, label, render) {
    var b = el('button', 'btn', esc(label));
    b.type = 'button'; b.setAttribute('role', 'tab'); b.setAttribute('aria-selected', 'false');
    var pane = el('div', 'lab-pane');
    pane.setAttribute('role', 'tabpanel');
    render(pane);
    holder.appendChild(pane);
    b.addEventListener('click', function () {
      $all('.btn', nav).forEach(function (x) { x.classList.remove('on'); x.setAttribute('aria-selected', 'false'); });
      $all('.lab-pane', holder).forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on'); b.setAttribute('aria-selected', 'true'); pane.classList.add('on');
    });
    nav.appendChild(b);
  }
  if ((COURSE.installLabs || []).length) addILPane('install', 'Install labs', function (p) {
    p.innerHTML = '<p class="section-sub">Install each tool and tick every verification checkpoint. ' +
      'Tool labs unlock only when their required installs are verified.</p>';
    COURSE.installLabs.forEach(function (l) { il26_renderInstallLab(l, p); });
  });
  if ((COURSE.toolLabs || []).length) addILPane('toollabs', 'Tool labs', function (p) {
    p.innerHTML = '<p class="section-sub">Chained tool labs. A lab stays locked until its ' +
      '<code>requiresInstall</code> checkpoints are confirmed.</p>';
    COURSE.toolLabs.slice().sort(function (a, b) { return (a.chain || 0) - (b.chain || 0); })
      .forEach(function (t) { il26_renderToolLabCard(t, p); });
  });
  if ((COURSE.multicloudLabs || []).length) addILPane('multicloud', 'Multicloud', function (p) {
    COURSE.multicloudLabs.forEach(function (t) {
      var card = el('div', 'scriptlab');
      card.innerHTML = '<h3>' + esc(t.title) + '</h3><p class="small muted">' + esc(t.cloud || '') + '</p>' +
        '<p>' + esc(t.brief || '') + '</p>' +
        '<ol class="obj-list">' + (t.steps || []).map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ol>' +
        (t.costGuardrails ? '<p class="small"><b>Cost guardrails:</b> ' + esc(t.costGuardrails) + '</p>' : '') +
        (t.cleanup ? '<p class="small muted"><b>Cleanup:</b> ' + esc(t.cleanup) + '</p>' : '') +
        (t.checkpoint ? '<p class="small"><b>Checkpoint:</b> ' + esc(t.checkpoint) + '</p>' : '');
      p.appendChild(card);
    });
  });
  if ((COURSE.sqlPlaygrounds || []).length) addILPane('sql', 'SQL playgrounds', function (p) {
    COURSE.sqlPlaygrounds.forEach(function (pg) { il26_renderSQLPlayground(pg, p); });
  });
  if ((COURSE.pythonExercises || []).length) addILPane('py', 'Python exercises', function (p) {
    COURSE.pythonExercises.forEach(function (ex) { il26_renderPythonExercise(ex, p); });
  });
  if ((COURSE.daxPlaygrounds || []).length) addILPane('dax', 'DAX', function (p) {
    COURSE.daxPlaygrounds.forEach(function (dg) { il26_renderDAXPlayground(dg, p); });
  });
  var graded = (COURSE.terminalSims || []).filter(function (s) { return s.gradedCommands; });
  if (graded.length) addILPane('gterm', 'Terminal sims', function (p) {
    graded.forEach(function (s) { il26_renderGradedTerm(s, p); });
  });
  if ((COURSE.branchingScenarios || []).length) addILPane('branch', 'Scenarios', function (p) {
    COURSE.branchingScenarios.forEach(function (bs) { il26_renderBranching(bs, p); });
  });
  if ((COURSE.clickSims || []).length) addILPane('click', 'Click sims', function (p) {
    COURSE.clickSims.forEach(function (cs) { il26_renderClickSim(cs, p); });
  });
  if ((COURSE.sampleDatasets || []).length) addILPane('data', 'Datasets', function (p) {
    COURSE.sampleDatasets.forEach(function (d) {
      var card = el('div', 'scriptlab');
      card.innerHTML = '<h3>' + esc(d.name) + '</h3><p class="small muted">' + esc(d.format || '') +
        (d.note ? ' · ' + esc(d.note) : '') + '</p>' +
        '<pre class="small mono">' + esc(d.columns.join(' | ') + '\n' +
          d.rows.slice(0, 8).map(function (r) { return r.join(' | '); }).join('\n')) + '</pre>';
      p.appendChild(card);
    });
  });
};

/* ---- buildCrosswalk wrapper: employer mappings + JD matrix + dossier (4f) ---- */
var _il26_buildCrosswalk = buildCrosswalk;
buildCrosswalk = function (root) {
  _il26_buildCrosswalk(root);
  if (!isIL26()) return;
  var extra = el('div', 'il26-xw-extra');
  var html = '';
  if (COURSE.dossierUrl) {
    html += '<div class="card"><h3>Graduate evidence dossier</h3>' +
      '<p class="small">Printable evidence map of coursework, practice scores, and portfolio artifacts — ' +
      'built for hiring conversations. Independent coursework; confers no certification.</p>' +
      '<div class="btn-row"><a class="btn primary" href="' + esc(COURSE.dossierUrl) + '">Open dossier (HTML)</a>' +
      '<a class="btn ghost" href="' + esc(COURSE.dossierUrl.replace(/\.html$/, '.pdf')) + '">Download PDF</a></div></div>';
  }
  var maps = COURSE.employerMappings || [];
  if (maps.length) {
    html += '<h2 class="section-title">Employer mappings</h2>' +
      '<p class="section-sub">Independent mapping of course competencies to publicly posted employer requirements. ' +
      'Not affiliated with or endorsed by any employer.</p>';
    var byEmp = {};
    maps.forEach(function (r) {
      var e = r.employer || 'Other';
      (byEmp[e] = byEmp[e] || []).push(r);
    });
    Object.keys(byEmp).forEach(function (e) {
      html += '<div class="card"><h3>' + esc(e) + '</h3>' +
        '<div class="arc-grid" style="grid-template-columns:1fr 1fr 1fr">' +
        '<div><h4 class="section-title" style="font-size:0.95em">Competency they ask for</h4><ul class="obj-list small">' +
        byEmp[e].map(function (r) { return '<li>' + esc(r.competency || '') + '</li>'; }).join('') + '</ul></div>' +
        '<div><h4 class="section-title" style="font-size:0.95em">Course evidence</h4><ul class="obj-list small">' +
        byEmp[e].map(function (r) {
          return '<li>' + esc(r.evidence || '') +
            (r.moduleId ? ' <span class="muted mono">[' + esc(r.moduleId) + ']</span>' : '') + '</li>';
        }).join('') + '</ul></div>' +
        '<div><h4 class="section-title" style="font-size:0.95em">Certification domain</h4><ul class="obj-list small">' +
        byEmp[e].map(function (r) {
          return '<li>' + esc(r.certification || '') + (r.certDomain ? ' — ' + esc(r.certDomain) : '') + '</li>';
        }).join('') + '</ul></div>' +
        '</div></div>';
    });
  }
  var jd = COURSE.jdMatrix || [];
  if (jd.length) {
    html += '<h2 class="section-title">JD matrix</h2><div class="card" style="overflow-x:auto"><table class="small" style="width:100%;border-collapse:collapse">' +
      '<thead><tr>' + Object.keys(jd[0]).map(function (k) {
        return '<th style="text-align:left;padding:6px;border-bottom:1px solid var(--panel3)">' + esc(k) + '</th>';
      }).join('') + '</tr></thead><tbody>' +
      jd.map(function (r) {
        return '<tr>' + Object.keys(jd[0]).map(function (k) {
          var v = r[k];
          return '<td style="padding:6px;border-bottom:1px solid var(--panel3)">' +
            esc(Array.isArray(v) ? v.join(', ') : (v == null ? '' : String(v))) + '</td>';
        }).join('') + '</tr>';
      }).join('') + '</tbody></table></div>';
  }
  extra.innerHTML = html;
  root.appendChild(extra);
};


var BUILDERS = {
  brief: buildBrief, plan: buildPlan, study: buildStudy,
  labs: buildLabs, mock: buildMock, more: buildMore, crosswalk: buildCrosswalk
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
    if (COURSE.crosswalk && COURSE.crosswalk.length && !TABS.some(function (t) { return t.id === 'crosswalk'; })) {
      TABS.push({ id: 'crosswalk', num: '07', label: 'Crosswalk' });
    /* IL-27: Fast Track + Objectives tabs (course-scoped; other courses unaffected) */
    if (typeof isIL27 === 'function' && isIL27()) {
      if (COURSE.fastTrack && !TABS.some(function (t) { return t.id === 'fasttrack'; })) {
        TABS.push({ id: 'fasttrack', num: '08', label: 'Fast Track' });
      }
      if (!TABS.some(function (t) { return t.id === 'objectives'; })) {
        TABS.push({ id: 'objectives', num: '09', label: 'Objectives' });
      }
    }
    }
    document.title = COURSE.title + ' · ' + (COURSE.code || 'Interstitium Labs');
    renderChrome();
    Sync.init($('#sync-note'));
    wireLegend();
    window.addEventListener('hashchange', route);
    route();
    /* Deep-link support for module anchors: #/study then #mod-<id> handled by Study hash. */
    /* 2026-10-08: ?module=<id> deep-link — resume drops the student at the
       exact module: open the study tab, expand the module, scroll to it. */
    try {
      var modId = queryParam('module');
      if (modId) {
        var found = null;
        (COURSE.modules || []).forEach(function (m) { if (m.id === modId) found = m; });
        if (found) {
          /* 2026-10-08 (WORKSTREAM 2): guided — a deep link into a locked
             module lands on the learner's current module instead. */
          var dlRedirected = false;
          try {
            if (typeof ILGuided !== 'undefined' && ILGuided && typeof Guided !== 'undefined') {
              var dst = ILGuided.stateFor(COURSE.courseId, found.id, Guided.infos());
              if (dst && (dst.state === 'locked' || dst.state === 'next')) {
                var cur = ILGuided.firstOpenModule(COURSE.courseId, Guided.infos());
                if (cur && cur.id !== found.id) {
                  var alt = Guided.findModule(cur.id);
                  if (alt) { found = alt; dlRedirected = true; }
                }
              }
            }
          } catch (e2) {}
          showTab('study');
          if (dlRedirected) {
            var dlList = document.getElementById('mod-list');
            if (dlList && !document.getElementById('ilgd-deeplink-note')) {
              var dlNote = document.createElement('div');
              dlNote.id = 'ilgd-deeplink-note';
              dlNote.className = 'ilgd-notice';
              dlNote.textContent = 'That module is locked — complete the previous lesson to unlock it. You are here:';
              dlList.insertBefore(dlNote, dlList.firstChild);
            }
          }
          var mw = document.getElementById('mod-' + found.id);
          if (mw) {
            var bdy = mw.querySelector('.mod-body');
            var hd = mw.querySelector('.mod-head');
            if (bdy && bdy.style.display === 'none') {
              bdy.style.display = '';
              /* 2026-10-08: staggered module-open entrance (il-animate.js). */
              if (window.ILAnimate) window.ILAnimate.moduleToggled(bdy, true);
            }
            if (hd) hd.setAttribute('aria-expanded', 'true');
            if (typeof ILProgress !== 'undefined' && ILProgress) ILProgress.touch(COURSE.courseId, found.id);
            try { mw.scrollIntoView({ block: 'start' }); } catch (e2) {}
          }
        }
      }
    } catch (e) {}
    /* 2026-10-08: paint unified progress strip + next-up prompt. */
    try { refreshILProgress(); } catch (e) {}
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



/* =====================================================================
 * IL-27 extension — IT Infrastructure Specialist: Zero Trust Infrastructure Mastery.
 *
 * Everything below is scoped to courseId
 * 'il-27-it-infrastructure-specialist-threatlocker-mastery' and must not alter
 * rendering for any other course. All state uses the existing Progress
 * system (localStorage ilc:<courseId>:<key> + /api/progress sync).
 *
 * Framing: independent preparation and practice material. Not affiliated with,
 * endorsed by, or sponsored by any vendor named herein; confers no
 * certification. No vendor text is reproduced.
 * ===================================================================== */
function isIL27() {
  return typeof COURSE !== 'undefined' && COURSE &&
    COURSE.courseId === 'il-27-it-infrastructure-specialist-threatlocker-mastery';
}

/* ---- normCourse wrapper: carry IL-27 top-level keys through ---- */
var _il27_normCourse = normCourse;
normCourse = function (raw) {
  var c = _il27_normCourse(raw);
  if (raw && raw.courseId === 'il-27-it-infrastructure-specialist-threatlocker-mastery') {
    ['fastTrack', 'mathLab', 'scriptingLab', 'animations', 'installLabs', 'toolLabs',
     'branchingScenarios', 'clickSims', 'studyGuide', 'dossier', 'dossierUrl',
     'interactivityAudit', 'jdMatrix'].forEach(function (k) {
      if (raw[k] !== undefined) c[k] = raw[k];
    });
  }
  return c;
};

/* ============================== Fast Track tab ============================== */
var il27CdTimer = null;

function il27CountdownTick(host, targetMs) {
  var now = Date.now();
  var diff = Math.max(0, targetMs - now);
  var d = Math.floor(diff / 86400000);
  var h = Math.floor(diff % 86400000 / 3600000);
  var m = Math.floor(diff % 3600000 / 60000);
  var s = Math.floor(diff % 60000 / 1000);
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  host.innerHTML =
    '<div class="il27-cd-grid">' +
    '<div class="il27-cd-cell"><b>' + d + '</b><span>days</span></div>' +
    '<div class="il27-cd-cell"><b>' + pad(h) + '</b><span>hours</span></div>' +
    '<div class="il27-cd-cell"><b>' + pad(m) + '</b><span>min</span></div>' +
    '<div class="il27-cd-cell"><b>' + pad(s) + '</b><span>sec</span></div>' +
    '</div>' +
    (diff <= 0 ? '<p class="small"><b>Interview time.</b> Breathe, walk in with your 60-second answers ready.</p>'
               : '<p class="small muted">Until the interview · ' + esc(new Date(targetMs).toString()) + '</p>');
}

function il27BuildFastTrack(root) {
  var ft = COURSE.fastTrack || {};
  var targetMs = new Date(ft.interviewDate || '2026-10-13T09:00:00-04:00').getTime();
  root.innerHTML = heroHTML() +
    '<div class="card il27-countdown"><h2>Interview countdown</h2>' +
    '<div class="il27-cd" data-cd></div>' +
    (ft.interviewDayNote ? '<p class="small muted">' + esc(ft.interviewDayNote) + '</p>' : '') +
    '</div>' +
    '<h2 class="section-title">' + esc(ft.title || '6-day interview fast track') + '</h2>' +
    '<p class="section-sub">' + esc(ft.framing || '') + '</p>' +
    '<div id="il27-ft-days"></div>' +
    '<h2 class="section-title">Fast-track modules</h2>' +
    '<p class="section-sub">Compressed sprint modules for the interview week — quiz-first, cards-second. ' +
    'Day plans above tell you which to take each day.</p>' +
    '<div id="il27-ft-mods"></div>' +
    '<div id="il27-ft-noah"></div>';

  var cdHost = root.querySelector('[data-cd]');
  function tick() {
    if (!document.body.contains(cdHost)) {
      /* Tab re-rendered without us: stop ticking instead of waking every second forever. */
      if (il27CdTimer) { try { clearInterval(il27CdTimer); } catch (e) {} il27CdTimer = null; }
      return;
    }
    il27CountdownTick(cdHost, targetMs);
  }
  if (il27CdTimer) { try { clearInterval(il27CdTimer); } catch (e) {} }
  tick();
  il27CdTimer = setInterval(tick, 1000);

  var daysEl = $('#il27-ft-days', root);
  (ft.plan || []).forEach(function (d) {
    var card = el('div', 'card');
    card.innerHTML = '<h3>Day ' + esc(String(d.day)) + ' — ' + esc(d.theme || '') + '</h3>' +
      '<p class="small muted">' + esc(d.date || '') + ' · ' + esc(String(d.minutes || '')) + ' min planned</p>' +
      '<ul class="obj-list">' + (d.tasks || []).map(function (t) {
        return '<li>' + esc(t) + '</li>';
      }).join('') + '</ul>' +
      ((d.modules || []).length ? '<p class="small"><b>Modules:</b> ' +
        d.modules.map(function (mid) { return '<span class="mono">' + esc(mid) + '</span>'; }).join(', ') + '</p>' : '') +
      (d.questionBank ? '<p class="small"><b>Question bank:</b> ' + esc(d.questionBank) + '</p>' : '');
    daysEl.appendChild(card);
  });

  var modsEl = $('#il27-ft-mods', root);
  var ftMods = (COURSE.modules || []).filter(function (m) { return m.fastTrack; })
    .sort(function (a, b) { return (a.fastTrackDay || 0) - (b.fastTrackDay || 0); });
  if (!ftMods.length) {
    modsEl.appendChild(el('div', 'card', '<p class="muted">No fast-track modules shipped in this course document.</p>'));
  } else {
    ftMods.forEach(function (m) { modsEl.appendChild(moduleHTML(m)); });
  }
  $('#il27-ft-noah', root).appendChild(noahPanel('Fast Track — ' + COURSE.title, COURSE.title));
}

/* ============================== Objectives tab ============================== */
var IL27_MASTERY_LEVELS = ['Not started', 'Developing', 'Proficient', 'Mastery'];

function il27BuildObjectives(root) {
  var objs = COURSE.objectives || [];
  root.innerHTML = heroHTML() +
    '<h2 class="section-title">Objectives</h2>' +
    '<p class="section-sub">Rate your mastery per course objective. Ratings persist on this device ' +
    'and feed the mastery signals below — re-rate after each study block.</p>' +
    '<div class="card" id="il27-obj-sum"></div>' +
    '<div id="il27-obj-list"></div>';

  var listEl = $('#il27-obj-list', root);
  var sumEl = $('#il27-obj-sum', root);

  function getLevel(i) {
    var v = parseInt(Progress.get('obj27:' + i, '0'), 10);
    return isNaN(v) ? 0 : Math.min(3, Math.max(0, v));
  }

  function renderSummary() {
    var counts = [0, 0, 0, 0];
    objs.forEach(function (_, i) { counts[getLevel(i)]++; });
    var total = objs.length || 1;
    var score = objs.reduce(function (s, _, i) { return s + getLevel(i); }, 0) / (total * 3);
    sumEl.innerHTML = '<h3>Mastery signals</h3>' +
      '<div class="il27-obj-bars">' +
      IL27_MASTERY_LEVELS.map(function (label, li) {
        var pct = Math.round(counts[li] / total * 100);
        return '<div class="il27-obj-bar"><span class="il27-obj-bar-label">' + esc(label) + '</span>' +
          '<div class="il27-obj-bar-track"><div class="il27-obj-bar-fill il27-lvl-' + li + '" style="width:' + pct + '%"></div></div>' +
          '<span class="il27-obj-bar-n">' + counts[li] + '/' + total + '</span></div>';
      }).join('') + '</div>' +
      '<p class="small muted">Overall objective mastery: <b>' + Math.round(score * 100) + '%</b> · ' +
      counts[3] + ' objectives at Mastery.</p>';
  }

  objs.forEach(function (o, i) {
    var card = el('div', 'card il27-obj-card');
    var btns = el('div', 'btn-row il27-obj-btns');
    function paint() {
      var lvl = getLevel(i);
      card.innerHTML = '<h3>Objective ' + (i + 1) + '</h3><p>' + esc(typeof o === 'string' ? o : (o.title || o.text || '')) + '</p>';
      card.appendChild(btns);
      btns.innerHTML = '';
      IL27_MASTERY_LEVELS.forEach(function (label, li) {
        var b = el('button', 'btn' + (li === lvl ? ' primary' : ''), esc(label));
        b.type = 'button';
        b.setAttribute('aria-pressed', li === lvl ? 'true' : 'false');
        b.addEventListener('click', function () {
          Progress.set('obj27:' + i, String(li));
          paint();
          renderSummary();
        });
        btns.appendChild(b);
      });
      var note = el('p', 'small muted', 'Current signal: <b>' + esc(IL27_MASTERY_LEVELS[getLevel(i)]) + '</b>');
      card.appendChild(note);
    }
    paint();
    listEl.appendChild(card);
  });
  renderSummary();
}

/* ================== Adaptive lab engines (mathLab + scriptingLab) ==================
 * Knowledge check → personalized path → mastery progression → re-checks → mastery map.
 * All state via Progress (localStorage ilc:<courseId>:<key> + /api/progress sync).
 */
var IL27_LAB_LEVELS = ['novice', 'developing', 'proficient', 'mastery'];
var IL27_LAB_LEVEL_LABELS = ['Novice', 'Developing', 'Proficient', 'Mastery'];

function il27NormAnswer(s) {
  return String(s == null ? '' : s).trim().toLowerCase().replace(/\s+/g, ' ').replace(/^0b/, '').replace(/^0x/, '');
}

function il27Shuffle(arr) {
  var a = arr.slice();
  for (var i = a.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}

/* Instantiate parameterized generators (range-int + option variables; notEqual honored).
 * Auto-checkable only for binary/decimal/hex conversion templates; other topics practice from the bank. */
function il27InstantiateGenerator(gen) {
  var vars = gen.variables || {};
  var vals = {};
  var keys = Object.keys(vars);
  for (var i = 0; i < keys.length; i++) {
    var k = keys[i], spec = vars[k];
    if (spec.range && spec.type === 'int') {
      vals[k] = spec.range[0] + Math.floor(Math.random() * (spec.range[1] - spec.range[0] + 1));
    } else if (spec.options) {
      var opts = spec.options.slice();
      if (spec.notEqual && vals[spec.notEqual] !== undefined) {
        opts = opts.filter(function (o) { return o !== vals[spec.notEqual]; });
      }
      vals[k] = opts[Math.floor(Math.random() * opts.length)];
    } else {
      return null;
    }
  }
  var q = gen.template || '';
  keys.forEach(function (k) { q = q.split('{' + k + '}').join(String(vals[k])); });
  return { q: q, vals: vals, id: gen.id };
}

function il27SolveConversion(inst) {
  var v = inst.vals;
  if (v.value === undefined || !v.from_base || !v.to_base) return null;
  var n;
  if (v.from_base === 'binary') { n = parseInt(String(v.value), 10); n = il27BinDigitsToInt(n); }
  else if (v.from_base === 'decimal') { n = v.value; }
  else if (v.from_base === 'hex') { n = parseInt(String(v.value), 16); }
  else return null;
  if (isNaN(n)) return null;
  if (v.to_base === 'binary') return n.toString(2);
  if (v.to_base === 'decimal') return String(n);
  if (v.to_base === 'hex') return n.toString(16).toUpperCase();
  return null;
}

function il27BinDigitsToInt(digits) {
  var s = String(digits), n = 0;
  for (var i = 0; i < s.length; i++) { n = n * 2 + (s[i] === '1' ? 1 : 0); }
  return n;
}

function il27AdaptiveLab(host, lab) {
  var eng = String(lab.engine || lab.id || 'lab').replace(/[^a-z0-9-]/gi, '').toLowerCase();
  var topics = lab.topics || [];
  var kc = lab.knowledgeCheck || [];
  var bank = lab.exerciseBank || {};
  var gens = lab.generators || [];

  var PK = 'alab:' + eng + ':';
  function mapGet() { var m = {}; try { m = JSON.parse(Progress.get(PK + 'map', '{}')); } catch (e) {} return m; }
  function mapSet(m) { Progress.set(PK + 'map', JSON.stringify(m)); }
  function tState(m, tid) {
    return m[tid] || { level: 0, streak: 0, attempts: 0, correct: 0, lastRecheck: null };
  }
  function kcGet() { var m = {}; try { m = JSON.parse(Progress.get(PK + 'kc', '{}')); } catch (e) {} return m; }
  function kcSet(m) { Progress.set(PK + 'kc', JSON.stringify(m)); }

  var card = el('div', 'card il27-alab');
  card.innerHTML = '<h3>' + esc(lab.title || 'Adaptive lab') + '</h3>' +
    '<p class="small muted">Knowledge check → personalized path → mastery progression → re-checks → mastery map. ' +
    'Progress persists on this device.</p>' +
    '<div class="btn-row il27-alab-nav" role="tablist" aria-label="Adaptive lab stages"></div>' +
    '<div class="il27-alab-body"></div>';
  host.appendChild(card);
  var nav = card.querySelector('.il27-alab-nav');
  var body = card.querySelector('.il27-alab-body');

  var stages = [
    { id: 'check', label: '1 · Knowledge check' },
    { id: 'path', label: '2 · My path' },
    { id: 'practice', label: '3 · Practice' },
    { id: 'map', label: '4 · Mastery map' }
  ];
  var active = 'check';
  var pathOrder = [];
  var practiceIdx = 0;

  stages.forEach(function (st, si) {
    var b = el('button', 'btn' + (si === 0 ? ' on' : ''), esc(st.label));
    b.type = 'button'; b.setAttribute('role', 'tab');
    b.addEventListener('click', function () {
      active = st.id;
      Array.prototype.forEach.call(nav.children, function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      renderStage();
    });
    nav.appendChild(b);
  });

  function topicById(tid) {
    for (var i = 0; i < topics.length; i++) if (topics[i].id === tid) return topics[i];
    return { id: tid, title: tid };
  }

  /* ---------- stage 1: knowledge check ---------- */
  function renderCheck() {
    body.innerHTML = '';
    if (!kc.length) {
      body.appendChild(el('p', 'muted', 'No knowledge-check questions shipped for this lab.'));
      return;
    }
    var saved = kcGet();
    var answers = {};
    kc.forEach(function (q, qi) {
      var wrap = el('div', 'il27-q');
      wrap.innerHTML = '<p><b>Q' + (qi + 1) + '.</b> ' + esc(q.q) +
        ' <span class="muted small">[' + esc(q.topic || 'general') + ']</span></p>';
      var opts = el('div', 'il27-opts');
      (q.choices || []).forEach(function (ch) {
        var b = el('button', 'btn', esc(ch));
        b.type = 'button';
        b.addEventListener('click', function () {
          answers[qi] = ch;
          Array.prototype.forEach.call(opts.children, function (x) { x.classList.remove('on'); });
          b.classList.add('on');
        });
        opts.appendChild(b);
      });
      wrap.appendChild(opts);
      body.appendChild(wrap);
    });
    var sub = el('button', 'btn primary', 'Score my knowledge check');
    sub.type = 'button';
    var out = el('div', 'il27-kc-out');
    sub.addEventListener('click', function () {
      var per = {}, shown = 0, right = 0;
      kc.forEach(function (q, qi) {
        var t = q.topic || 'general';
        per[t] = per[t] || { right: 0, total: 0 };
        per[t].total++;
        var ok = il27NormAnswer(answers[qi]) === il27NormAnswer(q.answer);
        if (ok) { per[t].right++; right++; }
        shown++;
      });
      kcSet(per);
      var order = Object.keys(per).sort(function (a, b) {
        var sa = per[a].right / per[a].total, sb = per[b].right / per[b].total;
        return sa - sb;
      });
      pathOrder = order;
      Progress.set(PK + 'path', JSON.stringify(order));
      out.innerHTML = '<div class="card"><h3>Result: ' + right + '/' + shown + '</h3>' +
        '<ul class="obj-list">' + Object.keys(per).map(function (t) {
          var p = per[t], pct = Math.round(p.right / p.total * 100);
          return '<li><b>' + esc(topicById(t).title) + '</b>: ' + p.right + '/' + p.total +
            ' (' + pct + '%)</li>';
        }).join('') + '</ul>' +
        '<p class="small">Your personalized path (weakest first): <b>' +
        order.map(function (t) { return esc(topicById(t).title); }).join(' → ') + '</b>. ' +
        'Head to <b>2 · My path</b> to start practicing.</p></div>';
    });
    body.appendChild(sub);
    body.appendChild(out);
  }

  /* ---------- stage 2: personalized path ---------- */
  function renderPath() {
    body.innerHTML = '';
    var per = kcGet();
    var order = pathOrder.length ? pathOrder : (function () {
      try { return JSON.parse(Progress.get(PK + 'path', '[]')); } catch (e) { return []; }
    })();
    if (!order.length) {
      order = topics.map(function (t) { return t.id; });
    }
    var intro = el('p', 'small muted',
      'Practice order is personalized: weakest knowledge-check topics first, strongest last. ' +
      'Complete a topic to unlock the next. Promotion: 8 consecutive correct answers moves a topic up one level.');
    body.appendChild(intro);
    var map = mapGet();
    order.forEach(function (tid, idx) {
      var st = tState(map, tid);
      var t = topicById(tid);
      var sc = per[tid];
      var row = el('div', 'il27-path-row');
      row.innerHTML = '<div><b>' + (idx + 1) + '. ' + esc(t.title) + '</b>' +
        '<div class="small muted">' + esc(t.description || '') + '</div>' +
        (sc ? '<div class="small">Knowledge check: ' + sc.right + '/' + sc.total + '</div>' : '') + '</div>' +
        '<div class="small"><span class="il27-lvl-pill il27-lvl-' + st.level + '">' +
        esc(IL27_LAB_LEVEL_LABELS[st.level]) + '</span></div>';
      var go = el('button', 'btn', 'Practice');
      go.type = 'button';
      go.addEventListener('click', function () {
        practiceIdx = 0;
        active = 'practice';
        Array.prototype.forEach.call(nav.children, function (x, xi) { x.classList.toggle('on', xi === 2); });
        renderStage();
      });
      row.appendChild(go);
      body.appendChild(row);
    });
    if (!order.length) body.appendChild(el('p', 'muted', 'No topics shipped for this lab.'));
  }

  /* ---------- stage 3: practice with mastery progression ---------- */
  function buildQueue(tid) {
    var q = [];
    (bank[tid] || []).forEach(function (e) {
      q.push({ q: e.q, answer: e.answer, steps: e.solutionSteps || [], kind: 'bank' });
    });
    gens.forEach(function (g) {
      if (g.topic !== tid) return;
      for (var i = 0; i < 4; i++) {
        var inst = il27InstantiateGenerator(g);
        if (!inst) continue;
        var sol = il27SolveConversion(inst);
        if (sol === null) continue;
        q.push({ q: inst.q, answer: sol, steps: ['Solve via decimal as the pivot, then convert to the target base.'], kind: 'generated' });
      }
    });
    return il27Shuffle(q);
  }

  function renderPractice() {
    body.innerHTML = '';
    var per = kcGet();
    var order = pathOrder.length ? pathOrder : (function () {
      try { return JSON.parse(Progress.get(PK + 'path', '[]')); } catch (e) { return []; }
    })();
    if (!order.length) order = topics.map(function (t) { return t.id; });
    if (!order.length) { body.appendChild(el('p', 'muted', 'No topics to practice.')); return; }

    var tid = order[Math.min(practiceIdx, order.length - 1)];
    var t = topicById(tid);
    var map = mapGet();
    var st = tState(map, tid);

    var head = el('div', 'card');
    head.innerHTML = '<h3>Practicing: ' + esc(t.title) + '</h3>' +
      '<p class="small muted">' + esc(t.description || '') + '</p>' +
      '<p class="small">Level: <span class="il27-lvl-pill il27-lvl-' + st.level + '">' +
      esc(IL27_LAB_LEVEL_LABELS[st.level]) + '</span> · streak <b>' + st.streak +
      '</b>/8 · attempts <b>' + st.attempts + '</b></p>' +
      '<div class="btn-row">' +
      '<button class="btn" data-prev type="button">← Prev topic</button>' +
      '<button class="btn" data-next type="button">Next topic →</button></div>';
    body.appendChild(head);
    head.querySelector('[data-prev]').addEventListener('click', function () {
      practiceIdx = (practiceIdx + order.length - 1) % order.length;
      renderPractice();
    });
    head.querySelector('[data-next]').addEventListener('click', function () {
      practiceIdx = (practiceIdx + 1) % order.length;
      renderPractice();
    });

    var queue = buildQueue(tid);
    if (!queue.length) {
      body.appendChild(el('p', 'muted', 'No practice exercises shipped for this topic yet.'));
      return;
    }
    var qi = 0;
    var exWrap = el('div', 'il27-ex');
    body.appendChild(exWrap);

    function renderExercise() {
      var item = queue[qi % queue.length];
      exWrap.innerHTML = '<div class="card"><p><b>Exercise ' + ((qi % queue.length) + 1) + '/' +
        queue.length + '</b> <span class="muted small">(' + esc(item.kind) + ')</span></p>' +
        '<p>' + esc(item.q) + '</p>' +
        '<div class="il27-ex-row"><input type="text" data-ans aria-label="Your answer" ' +
        'placeholder="Type your answer…">' +
        '<button class="btn primary" data-check type="button">Check</button></div>' +
        '<div data-fb></div></div>';
      var input = exWrap.querySelector('[data-ans]');
      var fb = exWrap.querySelector('[data-fb]');
      function check() {
        var ok = il27NormAnswer(input.value) === il27NormAnswer(item.answer);
        var m2 = mapGet();
        var s2 = tState(m2, tid);
        s2.attempts++;
        var promoted = false;
        if (ok) {
          s2.correct++; s2.streak++;
          if (s2.streak >= 8 && s2.level < 3) {
            s2.level++; s2.streak = 0; promoted = true;
          }
        } else {
          s2.streak = 0;
        }
        m2[tid] = s2;
        mapSet(m2);
        fb.innerHTML = '<p class="' + (ok ? 'il27-ok' : 'il27-bad') + '">' +
          (ok ? '✓ Correct.' : '✗ Not quite — accepted answer: <b>' + esc(item.answer) + '</b>.') +
          (promoted ? ' <b>Promoted to ' + esc(IL27_LAB_LEVEL_LABELS[s2.level]) + '!</b>' : '') + '</p>' +
          (item.steps.length ? '<ol class="small">' + item.steps.map(function (x) {
            return '<li>' + esc(x) + '</li>';
          }).join('') + '</ol>' : '') +
          '<div class="btn-row"><button class="btn" data-nx type="button">Next exercise →</button></div>';
        fb.querySelector('[data-nx]').addEventListener('click', function () {
          qi++;
          renderPracticeQueueOnly();
        });
        function renderPracticeQueueOnly() { renderPractice(); }
      }
      exWrap.querySelector('[data-check]').addEventListener('click', check);
      input.addEventListener('keydown', function (e) { if (e.key === 'Enter') check(); });
      try { input.focus(); } catch (e) {}
    }
    renderExercise();

    /* re-check for proficient+ topics */
    if (st.level >= 2) {
      var rc = el('div', 'card');
      rc.innerHTML = '<h3>Spaced re-check</h3><p class="small muted">This topic is ' +
        esc(IL27_LAB_LEVEL_LABELS[st.level]) + '. Answer 3 questions to confirm it sticks — ' +
        'a miss drops the topic one level and queues remedial practice.</p>' +
        '<button class="btn" data-rc type="button">Start re-check (3 questions)</button><div data-rcb></div>';
      body.appendChild(rc);
      rc.querySelector('[data-rc]').addEventListener('click', function () {
        var pool = [];
        kc.forEach(function (q) { if ((q.topic || 'general') === tid) pool.push(q); });
        (bank[tid] || []).forEach(function (e) { pool.push({ q: e.q, answer: e.answer, choices: null }); });
        pool = il27Shuffle(pool).slice(0, 3);
        var host2 = rc.querySelector('[data-rcb]');
        host2.innerHTML = '';
        if (!pool.length) { host2.appendChild(el('p', 'muted', 'No re-check questions available for this topic.')); return; }
        var ri = 0, rRight = 0;
        function renderR() {
          if (ri >= pool.length) {
            var m3 = mapGet();
            var s3 = tState(m3, tid);
            if (rRight === pool.length) {
              s3.lastRecheck = new Date().toISOString();
              host2.innerHTML = '<p class="il27-ok">✓ Re-check passed (' + rRight + '/' + pool.length +
                '). Level holds.</p>';
            } else {
              s3.level = Math.max(0, s3.level - 1);
              s3.streak = 0;
              host2.innerHTML = '<p class="il27-bad">✗ Re-check: ' + rRight + '/' + pool.length +
                ' — dropped to <b>' + esc(IL27_LAB_LEVEL_LABELS[s3.level]) +
                '</b>. Practice the topic again to climb back.</p>';
            }
            m3[tid] = s3;
            mapSet(m3);
            return;
          }
          var item = pool[ri];
          var w = el('div', 'il27-q');
          w.innerHTML = '<p><b>Re-check ' + (ri + 1) + '/3.</b> ' + esc(item.q) + '</p>';
          if (item.choices && item.choices.length) {
            var opts = el('div', 'il27-opts');
            item.choices.forEach(function (ch) {
              var b = el('button', 'btn', esc(ch));
              b.type = 'button';
              b.addEventListener('click', function () {
                if (il27NormAnswer(ch) === il27NormAnswer(item.answer)) rRight++;
                ri++;
                renderR();
              });
              opts.appendChild(b);
            });
            w.appendChild(opts);
          } else {
            w.innerHTML += '<div class="il27-ex-row"><input type="text" data-ra aria-label="Your answer">' +
              '<button class="btn primary" data-rb type="button">Check</button></div>';
            w.querySelector('[data-rb]').addEventListener('click', function () {
              if (il27NormAnswer(w.querySelector('[data-ra]').value) === il27NormAnswer(item.answer)) rRight++;
              ri++;
              renderR();
            });
          }
          host2.innerHTML = '';
          host2.appendChild(w);
        }
        renderR();
      });
    }
  }

  /* ---------- stage 4: mastery map ---------- */
  function renderMap() {
    body.innerHTML = '';
    var map = mapGet();
    var per = kcGet();
    var grid = el('div', 'il27-heat');
    topics.forEach(function (t) {
      var st = tState(map, t.id);
      var sc = per[t.id];
      var cell = el('div', 'il27-heat-cell il27-lvl-' + st.level);
      cell.innerHTML = '<b>' + esc(t.title) + '</b>' +
        '<span>' + esc(IL27_LAB_LEVEL_LABELS[st.level]) + '</span>' +
        '<span class="small">streak ' + st.streak + ' · ' + st.attempts + ' attempts</span>' +
        (sc ? '<span class="small">KC ' + sc.right + '/' + sc.total + '</span>' : '');
      grid.appendChild(cell);
    });
    body.appendChild(grid);
    var mastered = topics.filter(function (t) { return tState(map, t.id).level >= 3; }).length;
    body.appendChild(el('p', 'small muted',
      mastered + '/' + topics.length + ' topics at Mastery. The engine always serves your weakest ' +
      'topic first (70/30 weak/strong mix). Export your map any time:'));
    var exp = el('button', 'btn', 'Copy mastery map JSON');
    exp.type = 'button';
    exp.addEventListener('click', function () {
      var txt = JSON.stringify({ engine: eng, updatedAt: new Date().toISOString(), map: mapGet() }, null, 1);
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(txt);
          exp.textContent = '✓ Copied';
        }
      } catch (e) {}
    });
    body.appendChild(exp);
  }

  function renderStage() {
    if (active === 'check') renderCheck();
    else if (active === 'path') renderPath();
    else if (active === 'practice') renderPractice();
    else renderMap();
  }
  renderStage();
}

/* ================== IL-27 animation renderers (8 specs) ==================
 * SVG/Canvas interactive visuals: topology, AD tree, Zero Trust flow,
 * DHCP DORA, DNS chain, GPO order, backup rotation, IR lifecycle.
 */
function il27AnimWrap(spec) {
  var w = el('div', 'il27-anim card');
  w.innerHTML = '<h3>' + esc(spec.title || 'Interactive visual') + '</h3>' +
    '<p class="small muted">' + esc(spec.description || '') + '</p>' +
    '<div class="il27-anim-body"></div>';
  return w;
}

function il27SvgTag(w, h, inner) {
  return '<svg viewBox="0 0 ' + w + ' ' + h + '" width="100%" role="img" ' +
    'style="max-width:760px;display:block;margin:0 auto;background:#0e1622;border-radius:8px">' +
    inner + '</svg>';
}

function il27NodeBox(id, x, y, w, h, label, sub, on) {
  return '<g id="' + id + '" class="il27-node' + (on ? ' on' : '') + '">' +
    '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="8" ' +
    'fill="#16202e" stroke="#3a4a5f" stroke-width="2"/>' +
    '<text x="' + (x + w / 2) + '" y="' + (y + h / 2 - 2) + '" text-anchor="middle" ' +
    'fill="#e8eef4" font-size="13" font-weight="600">' + label + '</text>' +
    (sub ? '<text x="' + (x + w / 2) + '" y="' + (y + h / 2 + 15) + '" text-anchor="middle" ' +
      'fill="#8fa3b8" font-size="11">' + sub + '</text>' : '') + '</g>';
}

function il27Wire(x1, y1, x2, y2, id) {
  return '<line ' + (id ? 'id="' + id + '" ' : '') + 'x1="' + x1 + '" y1="' + y1 +
    '" x2="' + x2 + '" y2="' + y2 + '" stroke="#3a4a5f" stroke-width="2"/>';
}

/* Generic step-through player: steps = [{hl:[ids], dim:[ids], caption}]. */
function il27Stepper(body, svgHTML, steps) {
  var idx = 0;
  var stage = el('div', 'il27-anim-stage');
  var cap = el('p', 'small il27-cap');
  var row = el('div', 'btn-row');
  var prev = el('button', 'btn', '← Prev');
  var next = el('button', 'btn primary', 'Next →');
  var ctr = el('span', 'small muted');
  prev.type = 'button'; next.type = 'button';
  row.appendChild(prev); row.appendChild(next); row.appendChild(ctr);
  body.appendChild(stage); body.appendChild(cap); body.appendChild(row);

  function paint() {
    stage.innerHTML = svgHTML;
    var st = steps[idx];
    (st.hl || []).forEach(function (id) {
      var g = stage.querySelector('#' + id);
      if (g) {
        var r = g.querySelector('rect, circle, ellipse');
        if (r) { r.setAttribute('stroke', '#62d8e9'); r.setAttribute('stroke-width', '3'); }
      }
    });
    (st.dim || []).forEach(function (id) {
      var g = stage.querySelector('#' + id);
      if (g) g.setAttribute('opacity', '0.35');
    });
    cap.textContent = (idx + 1) + '/' + steps.length + ' — ' + st.caption;
    ctr.textContent = 'Step ' + (idx + 1) + ' of ' + steps.length;
    prev.disabled = idx === 0;
    next.disabled = idx === steps.length - 1;
  }
  prev.addEventListener('click', function () { if (idx > 0) { idx--; paint(); } });
  next.addEventListener('click', function () { if (idx < steps.length - 1) { idx++; paint(); } });
  paint();
}

/* ---- ANIM-03: Zero Trust request flow (step-through) ---- */
function il27AnimZT(body, spec) {
  var ids = ['a-client', 'a-engine', 'a-ident', 'a-device', 'a-allow', 'a-decide'];
  var labels = [
    ['Workstation', '10.0.1.44'],
    ['Policy engine', 'evaluate'],
    ['Identity', 'MFA check'],
    ['Device posture', 'healthy?'],
    ['Allowlist', 'app allowed?'],
    ['Decision', 'allow / deny']
  ];
  var inner = '';
  labels.forEach(function (L, i) {
    var x = 20 + i * 118;
    inner += il27NodeBox(ids[i], x, 60, 104, 64, L[0], L[1]);
    if (i < labels.length - 1) inner += il27Wire(x + 104, 92, x + 118, 92);
  });
  var steps = [
    { hl: ['a-client'], dim: ids.slice(1), caption: '1 · A user on the LAN workstation requests the file share. Nothing is trusted yet.' },
    { hl: ['a-client', 'a-engine'], dim: ids.slice(2), caption: '2 · The request hits the policy engine — every request is evaluated, every time.' },
    { hl: ['a-engine', 'a-ident'], dim: ids.slice(3), caption: '3 · Identity is verified (MFA, session risk). Identity alone is not enough.' },
    { hl: ['a-ident', 'a-device'], dim: ids.slice(4), caption: '4 · Device posture is checked: patched, encrypted, EDR healthy.' },
    { hl: ['a-device', 'a-allow'], dim: ['a-decide'], caption: '5 · The requested app must be on the explicit allowlist — default deny.' },
    { hl: ['a-decide'], dim: ids.slice(0, 5), caption: '6 · Decision: allow with least privilege, or deny. Logged either way.' }
  ];
  il27Stepper(body, il27SvgTag(740, 180, inner), steps);
}

/* ---- ANIM-04: DHCP DORA sequence ---- */
function il27AnimDORA(body, spec) {
  var inner =
    il27NodeBox('a-pc', 40, 70, 130, 70, 'Client', '00:11:22:33:44:55') +
    il27NodeBox('a-dhcp', 570, 70, 130, 70, 'DHCP server', '10.0.0.5') +
    il27NodeBox('a-p1', 230, 30, 280, 34, 'DISCOVER', 'broadcast → 255.255.255.255') +
    il27NodeBox('a-p2', 230, 74, 280, 34, 'OFFER', 'unicast · offers 10.0.1.100') +
    il27NodeBox('a-p3', 230, 118, 280, 34, 'REQUEST', 'broadcast · "I want 10.0.1.100"') +
    il27NodeBox('a-p4', 230, 162, 280, 34, 'ACK', 'unicast · lease confirmed');
  var all = ['a-pc', 'a-dhcp', 'a-p1', 'a-p2', 'a-p3', 'a-p4'];
  var steps = [
    { hl: ['a-pc', 'a-p1'], dim: ['a-dhcp', 'a-p2', 'a-p3', 'a-p4'], caption: 'D · DISCOVER: the client broadcasts — it has no IP yet, so it shouts to everyone.' },
    { hl: ['a-dhcp', 'a-p2'], dim: ['a-pc', 'a-p1', 'a-p3', 'a-p4'], caption: 'O · OFFER: the server unicasts back an offered address (10.0.1.100) plus options.' },
    { hl: ['a-pc', 'a-p3'], dim: ['a-dhcp', 'a-p1', 'a-p2', 'a-p4'], caption: 'R · REQUEST: the client broadcasts its choice so other servers back off.' },
    { hl: ['a-dhcp', 'a-p4'], dim: ['a-pc', 'a-p1', 'a-p2', 'a-p3'], caption: 'A · ACK: the server confirms the lease. DORA complete — the client now has an address.' }
  ];
  il27Stepper(body, il27SvgTag(740, 220, inner), steps);
}

/* ---- ANIM-05: DNS resolution chain ---- */
function il27AnimDNS(body, spec) {
  var ids = ['a-stub', 'a-fwd', 'a-root', 'a-tld', 'a-auth'];
  var labels = [
    ['Stub resolver', 'workstation'],
    ['pfSense', 'forwarder'],
    ['Root hints', '". " zone'],
    ['TLD', '".com"'],
    ['Authoritative', 'example.com']
  ];
  var inner = '';
  labels.forEach(function (L, i) {
    var x = 20 + i * 142;
    inner += il27NodeBox(ids[i], x, 60, 128, 64, L[0], L[1]);
    if (i < labels.length - 1) inner += il27Wire(x + 128, 92, x + 142, 92);
  });
  inner += '<text x="370" y="170" text-anchor="middle" fill="#8fa3b8" font-size="12">query: files.example.com → answer walks back down the chain</text>';
  var steps = [
    { hl: ['a-stub'], dim: ids.slice(1), caption: '1 · The app asks the stub resolver for files.example.com.' },
    { hl: ['a-stub', 'a-fwd'], dim: ids.slice(2), caption: '2 · The stub forwards to pfSense (the configured forwarder).' },
    { hl: ['a-fwd', 'a-root'], dim: ids.slice(3), caption: '3 · pfSense asks a root server, which refers down: "ask .com".' },
    { hl: ['a-fwd', 'a-tld'], dim: ['a-root', 'a-auth'], caption: '4 · The .com TLD server refers down: "ask example.com\'s nameserver".' },
    { hl: ['a-fwd', 'a-auth'], dim: ['a-root', 'a-tld'], caption: '5 · The authoritative server answers: files.example.com = 93.184.216.34.' },
    { hl: ids, dim: [], caption: '6 · The answer walks back down the chain and is cached at each layer.' }
  ];
  il27Stepper(body, il27SvgTag(760, 200, inner), steps);
}

/* ---- ANIM-02: AD forest / domain tree (click to expand) ---- */
function il27AnimAD(body, spec) {
  var ous = [
    ['ou-ws', 'Workstations', ['WS-FIN-01', 'WS-HR-02']],
    ['ou-srv', 'Servers', ['LAB-DC01', 'LAB-FS01']],
    ['ou-usr', 'Users', ['jdoe', 'asmith']],
    ['ou-grp', 'Groups', ['GG-Finance', 'GG-IT-Admins']],
    ['ou-svc', 'ServiceAccounts', ['svc-backup', 'svc-monitor']]
  ];
  var inner = il27NodeBox('a-root', 300, 20, 160, 60, 'lab.local', 'domain root (click me)');
  ous.forEach(function (o, i) {
    var x = 20 + i * 146;
    inner += '<g id="' + o[0] + '" style="display:none;cursor:pointer">' +
      il27NodeBox(o[0] + '-box', x, 120, 132, 54, o[1], 'OU (click)') +
      o[2].map(function (leaf, li) {
        return '<g id="' + o[0] + '-leaf' + li + '" style="display:none">' +
          '<rect x="' + (x + 6) + '" y="' + (196 + li * 30) + '" width="120" height="24" rx="5" ' +
          'fill="#101826" stroke="#3a4a5f"/>' +
          '<text x="' + (x + 66) + '" y="' + (212 + li * 30) + '" text-anchor="middle" ' +
          'fill="#9fd8e8" font-size="11">' + leaf + '</text></g>';
      }).join('') + '</g>';
    inner += il27Wire(380, 80, x + 66, 120);
  });
  var stage = el('div', 'il27-anim-stage');
  stage.innerHTML = il27SvgTag(760, 300, inner);
  body.appendChild(stage);
  body.appendChild(el('p', 'small muted', 'Click the domain root to expand the five OUs; click an OU to expand its objects.'));
  var rootG = stage.querySelector('#a-root');
  rootG.style.cursor = 'pointer';
  var open = false;
  rootG.addEventListener('click', function () {
    open = !open;
    ous.forEach(function (o) {
      var g = stage.querySelector('#' + o[0]);
      if (g) g.style.display = open ? '' : 'none';
    });
  });
  ous.forEach(function (o) {
    var g = stage.querySelector('#' + o[0]);
    g.addEventListener('click', function (e) {
      e.stopPropagation();
      o[2].forEach(function (_, li) {
        var leaf = stage.querySelector('#' + o[0] + '-leaf' + li);
        if (leaf) leaf.style.display = leaf.style.display === 'none' ? '' : 'none';
      });
    });
  });
}

/* ---- ANIM-06: GPO processing order (LSDOU, later wins) ---- */
function il27AnimGPO(body, spec) {
  var layers = [
    ['L', 'Local', 'Screen-saver timeout = 15 min'],
    ['S', 'Site', 'Screen-saver timeout = 10 min'],
    ['D', 'Domain', 'Screen-saver timeout = 5 min'],
    ['O', 'OU', 'Screen-saver timeout = 2 min']
  ];
  var applied = [];
  var stage = el('div', 'il27-anim-stage');
  var out = el('div', 'card il27-gpo-out');
  var row = el('div', 'btn-row');
  body.appendChild(stage); body.appendChild(row); body.appendChild(out);

  function paint() {
    var inner = '';
    layers.forEach(function (L, i) {
      var on = applied.indexOf(i) !== -1;
      inner += il27NodeBox('a-gpo-' + i, 60, 20 + i * 74, 300, 58,
        L[0] + ' — ' + L[1], L[2].split('= ')[1], on);
      if (on) {
        var r = null;
      }
      if (i < layers.length - 1) inner += il27Wire(210, 78 + i * 74, 210, 94 + i * 74);
    });
    stage.innerHTML = il27SvgTag(420, 330, inner);
    applied.forEach(function (i) {
      var g = stage.querySelector('#a-gpo-' + i + ' rect');
      if (g) { g.setAttribute('stroke', '#62d8e9'); g.setAttribute('stroke-width', '3'); }
    });
    var eff = applied.length ? layers[applied[applied.length - 1]][2] : 'no policies applied yet';
    out.innerHTML = '<h3>Effective setting</h3><p><b>' + esc(eff) + '</b></p>' +
      '<p class="small muted">LSDOU processes Local → Site → Domain → OU. Later layers win on conflict ' +
      '(unless Enforced / Block Inheritance changes the math). Applied so far: ' +
      (applied.length ? applied.map(function (i) { return layers[i][0]; }).join(' → ') : 'none') + '.</p>';
  }
  layers.forEach(function (L, i) {
    var b = el('button', 'btn', 'Apply ' + L[1]);
    b.type = 'button';
    b.addEventListener('click', function () {
      if (applied.indexOf(i) === -1) applied.push(i);
      paint();
    });
    row.appendChild(b);
  });
  var reset = el('button', 'btn', 'Reset');
  reset.type = 'button';
  reset.addEventListener('click', function () { applied = []; paint(); });
  row.appendChild(reset);
  paint();
}

/* ---- ANIM-08: Incident response lifecycle (clickable wheel) ---- */
function il27AnimIR(body, spec) {
  var phases = [
    ['Preparation', 'Playbooks, tooling, and training before anything happens.'],
    ['Detection & Analysis', 'Alerts triage; scope the incident; preserve evidence.'],
    ['Containment', 'Isolate hosts, block C2, stop the bleeding — short and long term.'],
    ['Eradication', 'Remove the attacker foothold: malware, persistence, bad accounts.'],
    ['Recovery', 'Restore systems to production, verify clean, monitor closely.'],
    ['Lessons Learned', 'Blameless postmortem; feed findings back into Preparation.']
  ];
  var cx = 210, cy = 150, R = 105;
  var inner = '';
  var pos = [];
  phases.forEach(function (p, i) {
    var a = -Math.PI / 2 + i * Math.PI * 2 / phases.length;
    var x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
    pos.push([x, y]);
    var x2 = cx + R * Math.cos(a + Math.PI * 2 / phases.length), y2 = cy + R * Math.sin(a + Math.PI * 2 / phases.length);
    inner += '<line x1="' + x.toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) +
      '" stroke="#3a4a5f" stroke-width="2" marker-end="url(#ilh-arrow)"/>';
  });
  inner = '<defs><marker id="ilh-arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">' +
    '<path d="M0,0 L8,4 L0,8" fill="none" stroke="#3a4a5f" stroke-width="1.5"/></marker></defs>' + inner;
  phases.forEach(function (p, i) {
    var x = pos[i][0], y = pos[i][1];
    inner += '<g id="a-ir-' + i + '" style="cursor:pointer">' +
      '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="34" fill="#16202e" stroke="#3a4a5f" stroke-width="2"/>' +
      '<text x="' + x.toFixed(1) + '" y="' + (y - 4).toFixed(1) + '" text-anchor="middle" fill="#e8eef4" font-size="12" font-weight="700">' + (i + 1) + '</text>' +
      '<text x="' + x.toFixed(1) + '" y="' + (y + 14).toFixed(1) + '" text-anchor="middle" fill="#8fa3b8" font-size="9">' +
      p[0].split(' ')[0] + '</text></g>';
  });
  var stage = el('div', 'il27-anim-stage');
  stage.innerHTML = il27SvgTag(420, 300, inner);
  var desc = el('div', 'card');
  desc.innerHTML = '<h3>Click a phase</h3><p class="small muted">The lifecycle is a loop — Lessons Learned feeds Preparation.</p>';
  body.appendChild(stage); body.appendChild(desc);
  phases.forEach(function (p, i) {
    var g = stage.querySelector('#a-ir-' + i);
    g.addEventListener('click', function () {
      phases.forEach(function (_, j) {
        var c = stage.querySelector('#a-ir-' + j + ' circle');
        if (c) { c.setAttribute('stroke', '#3a4a5f'); c.setAttribute('stroke-width', '2'); }
      });
      var c = stage.querySelector('#a-ir-' + i + ' circle');
      if (c) { c.setAttribute('stroke', '#62d8e9'); c.setAttribute('stroke-width', '3'); }
      desc.innerHTML = '<h3>' + (i + 1) + ' · ' + esc(p[0]) + '</h3><p>' + esc(p[1]) + '</p>';
    });
  });
}

/* ---- ANIM-01: Network topology builder (canvas) ---- */
function il27AnimTopo(body, spec) {
  var TYPES = [
    ['firewall', '#e26d5a'], ['switch', '#62d8e9'], ['server', '#c9a227'],
    ['workstation', '#7fb069'], ['printer', '#9b8cf0'], ['cloud', '#8fa3b8']
  ];
  var sel = 'switch';
  var nodes = [];
  var drag = null;

  var bar = el('div', 'btn-row');
  TYPES.forEach(function (t) {
    var b = el('button', 'btn' + (t[0] === sel ? ' on' : ''), t[0]);
    b.type = 'button';
    b.addEventListener('click', function () {
      sel = t[0];
      Array.prototype.forEach.call(bar.children, function (x) { x.classList.remove('on'); });
      b.classList.add('on');
    });
    bar.appendChild(b);
  });
  var reset = el('button', 'btn', 'Reset');
  reset.type = 'button';
  reset.addEventListener('click', function () { nodes = []; draw(); paintLinks(); });
  bar.appendChild(reset);

  var cv = document.createElement('canvas');
  cv.width = 720; cv.height = 380;
  cv.style.cssText = 'width:100%;max-width:720px;background:#0e1622;border-radius:8px;cursor:crosshair;display:block;margin:8px auto';
  var linksEl = el('p', 'small muted', 'Click the canvas to place the selected device. Drag devices to move them. Links connect devices in placement order.');
  body.appendChild(bar); body.appendChild(cv); body.appendChild(linksEl);

  function colorFor(t) {
    for (var i = 0; i < TYPES.length; i++) if (TYPES[i][0] === t) return TYPES[i][1];
    return '#fff';
  }
  function draw() {
    var ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, cv.width, cv.height);
    ctx.strokeStyle = '#2c3a4d'; ctx.lineWidth = 2;
    for (var i = 1; i < nodes.length; i++) {
      ctx.beginPath();
      ctx.moveTo(nodes[i - 1].x, nodes[i - 1].y);
      ctx.lineTo(nodes[i].x, nodes[i].y);
      ctx.stroke();
    }
    nodes.forEach(function (n) {
      ctx.fillStyle = '#16202e';
      ctx.strokeStyle = colorFor(n.type);
      ctx.lineWidth = 2.5;
      if (n.type === 'cloud') {
        ctx.beginPath(); ctx.ellipse(n.x, n.y, 34, 20, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      } else {
        ctx.beginPath(); ctx.rect(n.x - 30, n.y - 22, 60, 44); ctx.fill(); ctx.stroke();
      }
      ctx.fillStyle = '#e8eef4'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(n.type, n.x, n.y + 4);
    });
  }
  function paintLinks() {
    linksEl.textContent = nodes.length < 2
      ? 'Click the canvas to place the selected device. Drag devices to move them.'
      : nodes.map(function (n) { return n.type; }).join(' → ') + '  (' + (nodes.length - 1) + ' links)';
  }
  function pos(e) {
    var r = cv.getBoundingClientRect();
    return { x: (e.clientX - r.left) * (cv.width / r.width), y: (e.clientY - r.top) * (cv.height / r.height) };
  }
  cv.addEventListener('mousedown', function (e) {
    var p = pos(e);
    for (var i = nodes.length - 1; i >= 0; i--) {
      var n = nodes[i];
      if (Math.abs(p.x - n.x) < 34 && Math.abs(p.y - n.y) < 26) { drag = n; return; }
    }
    nodes.push({ type: sel, x: Math.round(p.x), y: Math.round(p.y) });
    draw(); paintLinks();
  });
  cv.addEventListener('mousemove', function (e) {
    if (!drag) return;
    var p = pos(e);
    drag.x = Math.round(p.x); drag.y = Math.round(p.y);
    draw();
  });
  window.addEventListener('mouseup', function () { if (drag) { drag = null; paintLinks(); } });
  draw();
}

/* ---- ANIM-07: Backup rotation visualizer (canvas GFS calendar) ---- */
function il27AnimBackup(body, spec) {
  var info = el('div', 'card');
  var cv = document.createElement('canvas');
  cv.width = 720; cv.height = 300;
  cv.style.cssText = 'width:100%;max-width:720px;background:#0e1622;border-radius:8px;display:block;margin:8px auto;cursor:pointer';
  body.appendChild(cv);
  body.appendChild(info);

  var cells = [];
  function kindFor(week, dow) {
    if (week === 0 && dow === 0) return ['grandfather', '#c9a227', 'Monthly FULL (grandfather)'];
    if (dow === 0) return ['father', '#62d8e9', 'Weekly FULL (father)'];
    return ['son', '#3f6f7f', 'Daily incremental (son)'];
  }
  function draw() {
    var ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, cv.width, cv.height);
    cells = [];
    var cw = 96, ch = 44, ox = 24, oy = 30;
    var days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    ctx.fillStyle = '#8fa3b8'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
    days.forEach(function (d, i) { ctx.fillText(d, ox + i * cw + cw / 2, oy - 8); });
    for (var w = 0; w < 4; w++) {
      for (var d = 0; d < 7; d++) {
        var x = ox + d * cw, y = oy + w * ch;
        var k = kindFor(w, d);
        ctx.fillStyle = k[1];
        ctx.globalAlpha = 0.85;
        ctx.fillRect(x + 2, y + 2, cw - 4, ch - 4);
        ctx.globalAlpha = 1;
        ctx.fillStyle = '#0e1622'; ctx.font = 'bold 10px sans-serif';
        ctx.fillText(k[0].toUpperCase(), x + cw / 2, y + ch / 2 + 4);
        cells.push({ x: x, y: y, w: cw, h: ch, week: w + 1, dow: days[d], kind: k });
      }
    }
    ctx.fillStyle = '#8fa3b8'; ctx.font = '11px sans-serif'; ctx.textAlign = 'left';
    ctx.fillText('Legend:', 24, 268);
    ctx.fillStyle = '#c9a227'; ctx.fillRect(80, 258, 14, 14);
    ctx.fillStyle = '#8fa3b8'; ctx.fillText('grandfather = monthly full', 100, 269);
    ctx.fillStyle = '#62d8e9'; ctx.fillRect(260, 258, 14, 14);
    ctx.fillStyle = '#8fa3b8'; ctx.fillText('father = weekly full', 280, 269);
    ctx.fillStyle = '#3f6f7f'; ctx.fillRect(420, 258, 14, 14);
    ctx.fillStyle = '#8fa3b8'; ctx.fillText('son = daily incremental', 440, 269);
  }
  function paintInfo(week, dow, kind) {
    info.innerHTML = '<h3>Week ' + week + ' · ' + dow + '</h3><p><b>' + esc(kind[2]) + '</b></p>' +
      '<p class="small muted">Grandfather-Father-Son: daily incrementals (sons) ride on weekly fulls (fathers), ' +
      'which ride on monthly fulls (grandfathers). Restores walk the chain: latest full + incrementals since. ' +
      'Retention example: 7 daily, 4 weekly, 12 monthly.</p>';
  }
  cv.addEventListener('click', function (e) {
    var r = cv.getBoundingClientRect();
    var x = (e.clientX - r.left) * (cv.width / r.width), y = (e.clientY - r.top) * (cv.height / r.height);
    for (var i = 0; i < cells.length; i++) {
      var c = cells[i];
      if (x >= c.x && x <= c.x + c.w && y >= c.y && y <= c.y + c.h) {
        paintInfo(c.week, c.dow, c.kind);
        return;
      }
    }
  });
  draw();
  paintInfo(1, 'Mon', kindFor(0, 0));
}

function il27RenderAnimation(spec) {
  var wrap = il27AnimWrap(spec);
  var body = wrap.querySelector('.il27-anim-body');
  try {
    if (spec.id === 'IL27-ANIM-01') il27AnimTopo(body, spec);
    else if (spec.id === 'IL27-ANIM-02') il27AnimAD(body, spec);
    else if (spec.id === 'IL27-ANIM-03') il27AnimZT(body, spec);
    else if (spec.id === 'IL27-ANIM-04') il27AnimDORA(body, spec);
    else if (spec.id === 'IL27-ANIM-05') il27AnimDNS(body, spec);
    else if (spec.id === 'IL27-ANIM-06') il27AnimGPO(body, spec);
    else if (spec.id === 'IL27-ANIM-07') il27AnimBackup(body, spec);
    else if (spec.id === 'IL27-ANIM-08') il27AnimIR(body, spec);
    else body.appendChild(el('p', 'muted', 'No renderer for animation spec ' + spec.id + '.'));
  } catch (e) {
    body.appendChild(el('p', 'muted', 'This visual failed to render: ' + String(e && e.message || e)));
  }
  return wrap;
}

/* ================== module hook: attach animations ================== */
var _il27_moduleHTML = moduleHTML;
moduleHTML = function (m) {
  var w = _il27_moduleHTML(m);
  if (!isIL27()) return w;
  var anims = (COURSE.animations || []).filter(function (a) { return a.moduleId === m.id; });
  if (!anims.length) return w;
  var body = w.querySelector('.mod-body');
  if (!body) return w;
  body.appendChild(el('h3', '', 'Interactive visuals'));
  anims.forEach(function (a) { body.appendChild(il27RenderAnimation(a)); });
  return w;
};

/* ================== extra lab sections for IL-27 ================== */
function il27InstallLabCard(lab) {
  var card = el('div', 'card');
  var cps = lab.checkpoints || [];
  var inner = '<h3>' + esc(lab.tool || lab.id) + '</h3>' +
    '<p class="small muted">' + esc(lab.category || '') +
    (lab.estimatedMinutes ? ' · ' + lab.estimatedMinutes + ' min' : '') + '</p>' +
    '<p class="small"><b>Platforms:</b> ' + esc((lab.platforms || []).join(', ')) + '</p>' +
    ((lab.gates || []).length ? '<p class="small"><b>Gate:</b> ' + esc(lab.gates.join(' · ')) + '</p>' : '') +
    (lab.costNote ? '<p class="small muted">' + esc(lab.costNote) + '</p>' : '') +
    '<h4 class="section-title" style="font-size:0.9em">Checkpoints</h4><ul class="obj-list">';
  card.innerHTML = inner + '</ul>';
  var ul = card.querySelector('ul');
  cps.forEach(function (cp, i) {
    var li = document.createElement('li');
    var key = 'install:' + lab.id + ':cp:' + i;
    var done = Progress.get(key) === '1';
    var cb = document.createElement('input');
    cb.type = 'checkbox'; cb.checked = done;
    cb.setAttribute('aria-label', 'Checkpoint ' + (i + 1));
    var span = el('span', '', esc(cp));
    if (done) span.style.textDecoration = 'line-through';
    cb.addEventListener('change', function () {
      Progress.set(key, cb.checked ? '1' : null);
      span.style.textDecoration = cb.checked ? 'line-through' : '';
    });
    li.appendChild(cb); li.appendChild(document.createTextNode(' ')); li.appendChild(span);
    ul.appendChild(li);
  });
  if ((lab.troubleshoot || []).length) {
    card.appendChild(el('h4', 'section-title', 'Troubleshooting'));
    var tb = el('ul', 'obj-list small');
    lab.troubleshoot.forEach(function (t) { tb.appendChild(el('li', '', esc(t))); });
    card.appendChild(tb);
  }
  return card;
}

function il27ToolLabCard(lab) {
  var card = el('div', 'card');
  var done = Progress.get('toollab:' + lab.id) === '1';
  card.innerHTML = '<h3>' + esc(lab.title || lab.id) + '</h3>' +
    '<p class="small muted">' + esc(lab.brief || '') + '</p>' +
    ((lab.requiresInstall || lab.requiresLab) ?
      '<p class="small"><b>Requires:</b> ' + esc([lab.requiresInstall, lab.requiresLab].filter(Boolean).join(' + ')) + '</p>' : '') +
    '<ol class="small">' + (lab.steps || []).map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ol>' +
    (lab.deliverable ? '<p class="small"><b>Deliverable:</b> ' + esc(lab.deliverable) + '</p>' : '') +
    (lab.checkpoint ? '<p class="small"><b>Checkpoint:</b> ' + esc(lab.checkpoint) + '</p>' : '');
  var b = el('button', 'btn' + (done ? '' : ' primary'), done ? '✓ Complete' : 'Mark complete');
  b.type = 'button';
  b.addEventListener('click', function () {
    var now = !(Progress.get('toollab:' + lab.id) === '1');
    Progress.set('toollab:' + lab.id, now ? '1' : null);
    b.textContent = now ? '✓ Complete' : 'Mark complete';
    b.classList.toggle('primary', !now);
  });
  card.appendChild(b);
  return card;
}

function il27ClickSimCard(sim) {
  var card = el('div', 'card');
  card.innerHTML = '<h3>' + esc(sim.title || sim.id) + '</h3>' +
    '<p class="small muted">' + esc(sim.tool || '') + ' · ' + esc(sim.moduleId || '') + '</p>' +
    '<div class="il27-clickstep small"></div>' +
    '<div class="btn-row"><button class="btn" data-p type="button">← Prev</button>' +
    '<button class="btn primary" data-n type="button">Next →</button></div>';
  var steps = sim.steps || [];
  var i = 0;
  var stepEl = card.querySelector('.il27-clickstep');
  function paintStep(s) {
    if (s && typeof s === 'object') {
      var h = '<p><b>Screen:</b> ' + esc(s.screen || '') + '</p>' +
        '<p><b>Do this:</b> ' + esc(s.instruction || '') + '</p>';
      if (s.hotspots && s.hotspots.length) h += '<p class="muted"><b>Click:</b> ' + s.hotspots.map(esc).join(' → ') + '</p>';
      if (s.feedback) h += '<p><b>Result:</b> ' + esc(s.feedback) + '</p>';
      return h;
    }
    return '<p>' + esc(s) + '</p>';
  }
  function paint() {
    stepEl.innerHTML = steps.length
      ? '<p><b>Step ' + (i + 1) + '/' + steps.length + '.</b></p>' + paintStep(steps[i])
      : '<p class="muted">No steps shipped.</p>';
  }
  card.querySelector('[data-p]').addEventListener('click', function () { if (i > 0) { i--; paint(); } });
  card.querySelector('[data-n]').addEventListener('click', function () { if (i < steps.length - 1) { i++; paint(); } });
  paint();
  return card;
}

function il27BranchCard(br) {
  var card = el('div', 'card');
  card.innerHTML = '<h3>' + esc(br.title || br.id) + '</h3>' +
    '<p class="small muted">Branching scenario — ' + esc(br.moduleId || '') + '. Choose; read the feedback; continue.</p>' +
    '<div class="il27-branch-body"></div>';
  var body = card.querySelector('.il27-branch-body');
  var nodes = br.nodes || {};
  var doneKey = 'branch:' + br.id;

  function renderNode(key) {
    var n = nodes[key];
    body.innerHTML = '';
    if (!n) {
      body.appendChild(el('p', 'il27-ok', '✓ Scenario complete. ' +
        (Progress.get(doneKey) === '1' ? 'Logged as complete.' : '')));
      Progress.set(doneKey, '1');
      return;
    }
    body.appendChild(el('p', '', esc(n.text || '')));
    (n.choices || []).forEach(function (ch) {
      var b = el('button', 'btn', esc(ch.label || ''));
      b.type = 'button';
      b.style.display = 'block';
      b.style.margin = '6px 0';
      b.style.textAlign = 'left';
      b.addEventListener('click', function () {
        body.innerHTML = '<div class="card"><p>' + esc(ch.feedback || 'Noted.') + '</p>' +
          '<button class="btn primary" data-c type="button">Continue →</button></div>';
        body.querySelector('[data-c]').addEventListener('click', function () { renderNode(ch.next); });
      });
      body.appendChild(b);
    });
    if (!(n.choices || []).length) {
      var fin = el('button', 'btn primary', 'Finish scenario');
      fin.type = 'button';
      fin.addEventListener('click', function () { renderNode('__end__'); });
      body.appendChild(fin);
    }
  }
  renderNode(br.start);
  return card;
}

function il27ExtraLabs(root) {
  var sec = el('div', 'il27-extra-labs');
  sec.innerHTML = '<h2 class="section-title" style="margin-top:2em">Adaptive lab engines</h2>' +
    '<p class="section-sub">Knowledge check → personalized path → mastery progression → re-checks → mastery map.</p>' +
    '<div class="il27-engines"></div>';
  root.appendChild(sec);
  var engHost = sec.querySelector('.il27-engines');
  [['mathLab', COURSE.mathLab], ['scriptingLab', COURSE.scriptingLab]].forEach(function (pair) {
    if (pair[1]) il27AdaptiveLab(engHost, pair[1]);
  });

  function addSection(title, sub, items, cardFn, emptyMsg) {
    if (!items || !items.length) return;
    var h = el('h2', 'section-title', title);
    h.style.marginTop = '2em';
    root.appendChild(h);
    root.appendChild(el('p', 'section-sub', sub));
    var grid = el('div', 'il27-lab-grid');
    items.forEach(function (it) { grid.appendChild(cardFn(it)); });
    root.appendChild(grid);
  }
  addSection('Install labs', 'Get the homelab tools installed — checkpoints persist as you tick them.',
    COURSE.installLabs, il27InstallLabCard);
  addSection('Tool labs', 'Chained tool exercises with deliverables.',
    COURSE.toolLabs, il27ToolLabCard);
  addSection('Click-through sims', 'Step through admin-console workflows one click at a time.',
    COURSE.clickSims, il27ClickSimCard);
  addSection('Branching scenarios', 'Troubleshooting stories where your choices change the outcome.',
    COURSE.branchingScenarios, il27BranchCard);
}

/* ================== wiring (IL-27 only) ================== */
BUILDERS.fasttrack = il27BuildFastTrack;
BUILDERS.objectives = il27BuildObjectives;
var _il27_BUILDERS_labs = BUILDERS.labs;
BUILDERS.labs = function (root) {
  _il27_BUILDERS_labs(root);
  if (isIL27()) il27ExtraLabs(root);
};

/* ==========================================================================
 * WORKSTREAM 1 (2026-10-08): "The story behind X" narrative supplements.
 *
 * Player-side join: course JSONs were NOT modified, so stories join at
 * render time via stories/_index.json (see js/il-stories.js). The outermost
 * moduleHTML wrapper prepends the story card as the FIRST element inside
 * .mod-body when the module maps to a story; modules without a story render
 * nothing extra.
 *
 * Paywall: the story card rides with module content — gated course JSONs
 * 402 at the worker without a valid entitlement cookie, so a story can only
 * ever appear where its course content already shows. IL-27/28/29 are free.
 * ========================================================================== */
var _ilstory_moduleHTML = moduleHTML;
moduleHTML = function (m) {
  var w = _ilstory_moduleHTML(m);
  try {
    var body = w.querySelector('.mod-body');
    if (body && window.ILStories && COURSE && COURSE.courseId) {
      /* async; story card prepends as first child when the fetch resolves */
      window.ILStories.enhanceModule(COURSE.courseId, m.id, body);
    }
  } catch (e) {}
  return w;
};

/* Module deep-open helper for the stories rail (2026-10-08).
 * Opens the Study tab, expands the module, scrolls to it — same mechanics
 * as the ?module=<id> deep-link in boot(). */
window.__ilOpenModule = function (moduleId) {
  if (!moduleId) return;
  try {
    showTab('study');
    setTimeout(function () {
      var mw = document.getElementById('mod-' + moduleId);
      if (!mw) return;
      var bdy = mw.querySelector('.mod-body');
      var hd = mw.querySelector('.mod-head');
      if (bdy && bdy.style.display === 'none') bdy.style.display = '';
      if (hd) hd.setAttribute('aria-expanded', 'true');
      try { mw.scrollIntoView({ block: 'start' }); } catch (e2) {}
    }, 60);
  } catch (e) {}
};


/* ==========================================================================
 * WORKSTREAM 5 (2026-10-08): KodeKloud-pattern 10X implementation pass.
 *
 * Abstract interaction patterns extracted from public research (brief:
 * .work/kodekloud-pattern-brief-20261008.md). Original implementations
 * below — no KodeKloud content, text, or copy reproduced.
 *
 *  1. (§5/#1) Skill-mastery dashboard + exam readiness — see academy.html
 *     "Mastery" section (js/il-mastery.js: heatFor/heatHTML/readinessFor).
 *  2. (§4/#3) Always-on solutions — quizHTML wrapper: after ANY answer the
 *     official explanation shows (existing .quiz.answered .why reveal) and
 *     a "Noah: compare my approach" button opens Noah (guarded
 *     IL.noahTutor.openWithPrefill) primed with question + learner pick vs
 *     official answer. Method comparison becomes the signature moment.
 *  3. (§4/#8) Repair queue — il-mastery.js repairItems/repairHTML fed by
 *     missed quick checks; Study-tab section + academy section; items link
 *     back to the exact module/question and clear when re-answered
 *     correctly (session repaired counter).
 *  4. (§3/#4) Lab environment-context headers — persistent "YOU ARE HERE"
 *     bar on every lab/practice/assessment block (course code, location,
 *     lab name, simulated-environment descriptor).
 *  5. (§1/#5) Diagnostic-on-entry — js/il-diagnostic.js: per-course
 *     "Test out" card sampling the first unanswered question per module
 *     (real course content only); ≥80% marks ILGuided test-out mastery and
 *     the guided path visibly skips those modules ("Tested out").
 *
 * Paywall untouched (content gating stays at the worker), dark-mode
 * default untouched, multicloud theme untouched. Sibling APIs are only
 * extended (ILGuided.markTestOut, quizHTML/moduleHTML wrappers), never
 * rewritten. Vanilla ES5; prefers-reduced-motion honored (no animation
 * except the guarded .ilflash transition in il-mastery.css).
 * ========================================================================== */

/* ---- pattern 4: environment-context headers ---------------------------- */

function ws5_ctxBar(courseCode, location, name, env) {
  return '<div class="ilctx" role="note" aria-label="Environment context: you are here">' +
    '<span class="ilctx-you">YOU ARE HERE</span><span class="ilctx-sep">·</span>' +
    '<span>' + esc(courseCode || '') + '</span><span class="ilctx-sep">·</span>' +
    '<span>' + esc(location || '') + '</span><span class="ilctx-sep">·</span>' +
    '<span>' + esc(name || 'Lab') + '</span><span class="ilctx-sep">·</span>' +
    '<span class="ilctx-env">' + esc(env || '') + '</span></div>';
}

/* Prepend context bars to .scriptlab/.drill cards newly appended to host. */
function ws5_barNewCards(host, beforeCount, location, env) {
  if (!host || !host.children) return;
  for (var i = beforeCount; i < host.children.length; i++) {
    (function (card) {
      if (!card || !card.classList) return;
      if (!(card.classList.contains('scriptlab') || card.classList.contains('drill'))) return;
      try { if (card.querySelector('.ilctx')) return; } catch (e) { return; }
      var name = '';
      try {
        var h3 = card.querySelector('h3');
        if (h3) name = (h3.textContent || '').replace(/✓ done/g, '').trim();
        else {
          var pr = card.querySelector('.prompt');
          if (pr) name = (pr.textContent || '').trim();
        }
      } catch (e2) {}
      if (!name) name = 'Lab';
      if (name.length > 70) name = name.slice(0, 69) + '…';
      try { card.insertAdjacentHTML('afterbegin', ws5_ctxBar(COURSE.code, location, name, env)); }
      catch (e3) {}
    })(host.children[i]);
  }
}

function ws5_wrapLabPane(builder, location, env) {
  return function (root) {
    var before = (root && root.children) ? root.children.length : 0;
    builder(root);
    try { ws5_barNewCards(root, before, location, env); } catch (e) {}
  };
}

try {
  buildTermPane = ws5_wrapLabPane(buildTermPane, 'Labs tab · Terminal', 'Simulated lab · no real infrastructure');
  buildScriptPane = ws5_wrapLabPane(buildScriptPane, 'Labs tab · Script labs', 'Simulated lab · no real infrastructure');
  buildDrillsPane = ws5_wrapLabPane(buildDrillsPane, 'Labs tab · Drills', 'Simulated practice · no real infrastructure');
  buildPolicyPane = ws5_wrapLabPane(buildPolicyPane, 'Labs tab · Policy drills', 'Simulated practice · no real infrastructure');
  buildScenPane = ws5_wrapLabPane(buildScenPane, 'Labs tab · Scenarios', 'Simulated lab · no real infrastructure');
  buildTrainerPane = ws5_wrapLabPane(buildTrainerPane, 'Labs tab · Trainers', 'Simulated lab · no real infrastructure');
} catch (e_ws5_panes) {}

/* In-module lab renderers (IL-26 stage sections): module context in the bar. */
function ws5_wrapModuleLab(renderer, env) {
  return function (m, host) {
    var before = (host && host.children) ? host.children.length : 0;
    renderer(m, host);
    try {
      ws5_barNewCards(host, before,
        (m && m.code ? m.code + ' · ' : '') + ((m && m.title) || (m && m.id) || 'Module'), env);
    } catch (e) {}
  };
}
try {
  il26_renderHandsOnLab = ws5_wrapModuleLab(il26_renderHandsOnLab, 'Simulated lab · no real infrastructure');
  il26_renderMockTask = ws5_wrapModuleLab(il26_renderMockTask, 'Simulated assessment · no real infrastructure');
  il26_renderModuleDrills = ws5_wrapModuleLab(il26_renderModuleDrills, 'Simulated practice · no real infrastructure');
} catch (e_ws5_modlabs) {}

/* Mock assessment tab: per-task bars (tasks re-render on reset/finish, so
   scan + MutationObserver, idempotent via the .ilctx presence check). */
function ws5_scanMock(host) {
  if (!host || !host.querySelectorAll) return;
  var tasks = host.querySelectorAll('.mock-task');
  for (var i = 0; i < tasks.length; i++) {
    (function (t, ix) {
      try { if (t.querySelector('.ilctx')) return; } catch (e) { return; }
      var name = 'Mock task ' + (ix + 1);
      try {
        var q = t.querySelector('.q');
        if (q && q.textContent) {
          name = q.textContent.trim();
          if (name.length > 70) name = name.slice(0, 69) + '…';
        }
      } catch (e2) {}
      try {
        t.insertAdjacentHTML('afterbegin',
          ws5_ctxBar(COURSE.code, 'Mock assessment', name, 'Simulated assessment · no real infrastructure'));
      } catch (e3) {}
    })(tasks[i], i);
  }
}
try {
  var _ws5_buildMock = buildMock;
  buildMock = function (root) {
    _ws5_buildMock(root);
    try {
      var host = root.querySelector ? root.querySelector('#mock-tasks') : null;
      ws5_scanMock(host);
      if (host && typeof MutationObserver !== 'undefined') {
        var obs = new MutationObserver(function () { try { ws5_scanMock(host); } catch (e) {} });
        obs.observe(host, { childList: true });
      }
    } catch (e) {}
  };
} catch (e_ws5_mock) {}

/* ---- pattern 2: always-on solutions + Noah method comparison ---------- */

function ws5_chosenIndex(mod, qi) {
  try {
    var v = Progress.get('quiz:' + mod.id + ':' + qi, null);
    return (v == null || v === '') ? -1 : parseInt(v, 10);
  } catch (e) { return -1; }
}

function ws5_addCompare(box, mod, q, qi) {
  if (!box || !box.querySelector || box.querySelector('.ilcompare-row')) return;
  if (typeof document === 'undefined' || !document.createElement) return;
  var row = document.createElement('div');
  row.className = 'ilcompare-row';
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'ilcompare-btn';
  btn.textContent = '◈ Noah: compare my approach';
  btn.setAttribute('aria-label', 'Ask Noah AI to compare your approach with the official solution');
  btn.addEventListener('click', function () {
    var ci = ws5_chosenIndex(mod, qi);
    var pre = 'The student is studying ' + (COURSE.code ? COURSE.code + ' · ' : '') +
      (COURSE.title || 'this course') + ', module "' + (mod.title || mod.id) +
      '", and just answered a quick check.\n' +
      'Question: ' + (q.q || '') + '\n' +
      'The learner picked: ' + (ci >= 0 && q.choices && q.choices[ci] != null ? q.choices[ci] : '(no pick recorded)') + '\n' +
      'The official answer is: ' + (q.choices && q.choices[q.answer] != null ? q.choices[q.answer] : '') + '\n' +
      'The official explanation: ' + (q.explain || '(no explanation shipped with this question)') + '\n' +
      'Compare their approach with the official one: name anything their pick gets right, ' +
      'the key difference from the official answer, and the one idea to lock in. ' +
      'You are Noah AI, the resident tutor of Interstitium Labs — never claim to be Muse or any other assistant. ' +
      'Do not invent facts beyond the question above.';
    try {
      var t = (typeof IL !== 'undefined' && IL && IL.noahTutor) ? IL.noahTutor : null;
      if (t && typeof t.openWithPrefill === 'function' &&
          typeof t.noahReady === 'function' && t.noahReady()) {
        t.openWithPrefill(pre);
      } else if (typeof IL !== 'undefined' && IL && IL.noahAI &&
                 typeof IL.noahAI.open === 'function') {
        IL.noahAI.open();
      }
    } catch (e) {}
  });
  row.appendChild(btn);
  try { box.appendChild(row); } catch (e2) {}
}

try {
  var _ws5_quizHTML = quizHTML;
  quizHTML = function (mod, qi, q) {
    var box = _ws5_quizHTML(mod, qi, q);
    try {
      /* Stable anchor for repair-queue deep links. */
      if (box && !box.id) box.id = 'quiz-' + mod.id + '-' + qi;
      if (box && box.classList && box.classList.contains('answered')) {
        /* Reloaded with a stored answer: explanation already revealed by
           .quiz.answered .why — add the comparison affordance. */
        ws5_addCompare(box, mod, q, qi);
      } else if (box && typeof MutationObserver !== 'undefined') {
        (function (b) {
          var obs = new MutationObserver(function () {
            if (b.classList.contains('answered')) {
              try { obs.disconnect(); } catch (e) {}
              ws5_addCompare(b, mod, q, qi);
              ws5_refreshRepair();
            }
          });
          obs.observe(b, { attributes: true, attributeFilter: ['class'] });
        })(box);
      }
    } catch (e) {}
    return box;
  };
} catch (e_ws5_quiz) {}

/* ---- pattern 3: repair queue (Study tab) ------------------------------- */

var ws5_repairOpen = {};
var ws5_repairFixed = 0;
var ws5_repairItems = [];

function ws5_gotoQuestion(moduleId, qi) {
  try {
    if (typeof window !== 'undefined' && typeof window.__ilOpenModule === 'function') {
      window.__ilOpenModule(moduleId);
    } else if (typeof showTab === 'function') {
      showTab('study');
    }
    var tries = 0;
    (function seek() {
      tries++;
      var t = document.getElementById('quiz-' + moduleId + '-' + qi);
      if (t) {
        try {
          t.scrollIntoView({ block: 'center', behavior: 'auto' });
          t.classList.add('ilflash');
          setTimeout(function () { try { t.classList.remove('ilflash'); } catch (e) {} }, 1600);
        } catch (e2) {}
        return;
      }
      if (tries < 30) setTimeout(seek, 150);
    })();
  } catch (e3) {}
}

function ws5_refreshRepair() {
  try {
    var host = document.getElementById('il-repair');
    if (!host || typeof ILMastery === 'undefined' || typeof COURSE === 'undefined' || !COURSE) return;
    var items = ILMastery.repairItems(COURSE.courseId, COURSE.modules || []);
    var now = {}, i, k;
    for (i = 0; i < items.length; i++) now[items[i].moduleId + ':' + items[i].qi] = true;
    for (k in ws5_repairOpen) {
      if (Object.prototype.hasOwnProperty.call(ws5_repairOpen, k) && !now[k]) ws5_repairFixed++;
    }
    ws5_repairOpen = now;
    ws5_repairItems = items;
    host.innerHTML = '<h2 class="section-title">Repair queue</h2>' +
      '<p class="section-sub">Missed quick checks, routed back to the exact question. ' +
      'Answer one correctly on retry and it clears the queue.</p>' +
      ILMastery.repairHTML(items, {
        repairedCount: ws5_repairFixed,
        linkFor: function () { return '#/study'; }
      });
    var as = host.querySelectorAll('.il-repair__go');
    for (i = 0; i < as.length && i < items.length; i++) {
      (function (a, it) {
        a.addEventListener('click', function (ev) {
          if (ev && ev.preventDefault) ev.preventDefault();
          ws5_gotoQuestion(it.moduleId, it.qi);
        });
      })(as[i], items[i]);
    }
  } catch (e) {}
}

/* ---- patterns 3 + 5: Study-tab sections -------------------------------- */

/* Refresh hook for il-diagnostic.js: Guided lives inside this IIFE, so the
   standalone diagnostic module cannot reach it as a global. */
try {
  window.__ilWs5Refresh = function () {
    try { if (typeof Guided !== 'undefined' && Guided.refresh) Guided.refresh(); } catch (e) {}
  };
} catch (e_ws5_hook) {}

try {
  var _ws5_buildStudy = buildStudy;
  buildStudy = function (root) {
    _ws5_buildStudy(root);
    try {
      if (document.getElementById('il-ws5')) return;
      var list = root.querySelector ? root.querySelector('#mod-list') : null;
      if (!list) return;
      var wrap = document.createElement('section');
      wrap.id = 'il-ws5';
      wrap.setAttribute('aria-label', 'Test-out diagnostic and repair queue');
      var dslot = document.createElement('div');
      dslot.id = 'il-diag';
      var rslot = document.createElement('div');
      rslot.id = 'il-repair';
      wrap.appendChild(dslot);
      wrap.appendChild(rslot);
      list.parentNode.insertBefore(wrap, list);
      /* Pattern 5: diagnostic-on-entry. Hidden when nothing is eligible. */
      try {
        if (typeof ILDiag !== 'undefined' && ILDiag) {
          var has = ILDiag.mount(dslot, COURSE.courseId, COURSE.modules || [], {
            onDone: function (passed) {
              if (passed) {
                try { if (typeof Guided !== 'undefined' && Guided.refresh) Guided.refresh(); } catch (e) {}
                ws5_refreshRepair();
              }
            }
          });
          if (!has && dslot.parentNode) dslot.parentNode.removeChild(dslot);
        }
      } catch (e2) {}
      /* Pattern 3: repair queue. */
      ws5_repairOpen = {};
      ws5_repairFixed = 0;
      ws5_refreshRepair();
    } catch (e3) {}
  };
} catch (e_ws5_study) {}

/* ---- academy deep links: ?module=<id>&q=<qi> -----------------------------
   Repair-queue links from academy.html land here. Boot's ?module= deep link
   opens the module; this scrolls to the exact question once rendered. */
try {
  if (typeof window !== 'undefined' && window.addEventListener) {
    window.addEventListener('load', function () {
      var modId = null, qi = -1;
      try {
        modId = queryParam('module');
        var qv = queryParam('q');
        if (qv != null && qv !== '') qi = parseInt(qv, 10);
      } catch (e) {}
      if (!modId || !(qi >= 0)) return;
      var tries = 0;
      (function seek() {
        tries++;
        var t = document.getElementById('quiz-' + modId + '-' + qi);
        if (t) {
          try {
            t.scrollIntoView({ block: 'center', behavior: 'auto' });
            t.classList.add('ilflash');
            setTimeout(function () { try { t.classList.remove('ilflash'); } catch (e2) {} }, 1600);
          } catch (e3) {}
          return;
        }
        if (tries < 40) setTimeout(seek, 200);
      })();
    });
  }
} catch (e_ws5_deep) {}

})();
