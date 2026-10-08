/* =====================================================================
 * ILProgress — unified course/module progress for Interstitium Labs.
 *
 * 2026-10-08: canonical sequential progress store for IL-01..IL-29.
 *
 * Storage: localStorage key "il-progress-v1", local device only. No
 * account, no network, no entitlement check — progress tracks regardless
 * of paywall gating (gating is enforced separately at the worker).
 *
 * Schema:
 *   {
 *     "version": 1,
 *     "courses": {
 *       "<courseId>": {
 *         "<moduleId>": { "completed": true, "completedAt": "<ISO 8601>" }
 *       }
 *     },
 *     "lastPosition": { "courseId": "...", "moduleId": "...", "timestamp": "<ISO 8601>" }
 *   }
 *
 * Sequence data (course order, module order, titles) lives in
 * /university/data/curriculum-sequence.json, loaded lazily and cached.
 *
 * Vanilla ES5. Honors prefers-reduced-motion (no animated progress fills).
 * ===================================================================== */
(function (g) {
  'use strict';

  var KEY = 'il-progress-v1';
  var SEQ_URL = 'data/curriculum-sequence.json'; /* resolved relative to /university/ */
  var memOnly = false;
  var mem = {};

  function probe() {
    try {
      g.localStorage.setItem(KEY + ':__probe', '1');
      g.localStorage.removeItem(KEY + ':__probe');
    } catch (e) { memOnly = true; }
  }
  probe();

  function nowISO() { return new Date().toISOString(); }

  function load() {
    var raw = memOnly ? (mem[KEY] || null) : null;
    try { if (!memOnly) raw = g.localStorage.getItem(KEY); } catch (e) { raw = mem[KEY] || null; }
    if (!raw) return { version: 1, courses: {}, lastPosition: null };
    try {
      var d = JSON.parse(raw);
      if (!d || typeof d !== 'object') throw new Error('bad shape');
      if (!d.courses || typeof d.courses !== 'object') d.courses = {};
      return d;
    } catch (e) {
      return { version: 1, courses: {}, lastPosition: null };
    }
  }

  function save(doc) {
    var raw;
    try { raw = JSON.stringify(doc); } catch (e) { return; }
    try {
      if (memOnly) mem[KEY] = raw;
      else g.localStorage.setItem(KEY, raw);
    } catch (e) { mem[KEY] = raw; }
  }

  function markComplete(courseId, moduleId) {
    if (!courseId || !moduleId) return;
    var d = load();
    d.courses[courseId] = d.courses[courseId] || {};
    d.courses[courseId][moduleId] = { completed: true, completedAt: nowISO() };
    save(d);
  }

  function unmarkComplete(courseId, moduleId) {
    if (!courseId || !moduleId) return;
    var d = load();
    var c = d.courses[courseId];
    if (c && c[moduleId]) {
      delete c[moduleId];
      save(d);
    }
  }

  function isComplete(courseId, moduleId) {
    var d = load();
    var c = d.courses[courseId];
    return !!(c && c[moduleId] && c[moduleId].completed === true);
  }

  /* Record the last-viewed module (the resume anchor). Called on every
     module view in the course player. */
  function touch(courseId, moduleId) {
    if (!courseId || !moduleId) return;
    var d = load();
    d.lastPosition = { courseId: courseId, moduleId: moduleId, timestamp: nowISO() };
    save(d);
  }

  function getLastPosition() {
    var d = load();
    var lp = d.lastPosition;
    if (!lp || !lp.courseId || !lp.moduleId) return null;
    return lp;
  }

  function courseStats(courseId, total) {
    var d = load();
    var c = d.courses[courseId] || {};
    var done = 0, k;
    for (k in c) {
      if (Object.prototype.hasOwnProperty.call(c, k) && c[k] && c[k].completed === true) done++;
    }
    total = Number(total) || 0;
    var pct = total > 0 ? Math.min(100, Math.round((done / total) * 100)) : 0;
    return { done: done, total: total, pct: pct };
  }

  function isCourseComplete(courseId, total) {
    if (!total) return false;
    var s = courseStats(courseId, total);
    return s.done >= s.total;
  }

  /* ---- canonical sequence (lazy, cached) ---- */
  var seqDoc = null, seqPending = null;

  function seqURL() {
    /* Works from /university/* pages and the site root: prefer absolute. */
    return '/university/data/curriculum-sequence.json';
  }

  function loadSequence(cb) {
    if (seqDoc) { cb(seqDoc); return; }
    if (seqPending) { seqPending.push(cb); return; }
    seqPending = [cb];
    function done(doc) {
      seqDoc = doc || null;
      var q = seqPending; seqPending = null;
      q.forEach(function (f) { try { f(seqDoc); } catch (e) {} });
    }
    try {
      g.fetch(seqURL()).then(function (r) {
        if (!r || !r.ok) { done(null); return; }
        return r.json();
      }).then(function (j) { done(j && j.courses ? j : null); })
        .catch(function () { done(null); });
    } catch (e) { done(null); }
  }

  function findEntry(seq, courseId) {
    if (!seq || !seq.courses) return null;
    for (var i = 0; i < seq.courses.length; i++) {
      if (seq.courses[i].courseId === courseId) return seq.courses[i];
    }
    return null;
  }

  function nextEntry(seq, courseId) {
    if (!seq || !seq.courses) return null;
    for (var i = 0; i < seq.courses.length - 1; i++) {
      if (seq.courses[i].courseId === courseId) return seq.courses[i + 1];
    }
    return null;
  }

  function findModuleTitle(entry, moduleId) {
    if (!entry || !entry.modules) return null;
    for (var i = 0; i < entry.modules.length; i++) {
      if (entry.modules[i].id === moduleId) return entry.modules[i].title || null;
    }
    return null;
  }

  /* Deep link that lands the student at the exact last module. The course
     shell honors ?module=<id> (opens + scrolls to the module). */
  function courseURL(entry, moduleId) {
    var slug = entry && entry.slug;
    if (!slug) return null;
    var u = '/university/course.html?course=' + encodeURIComponent(slug);
    if (moduleId) u += '&module=' + encodeURIComponent(moduleId);
    return u;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ---- render helpers (progress bars, continue banner) ---- */
  function progressBarHTML(stats, opts) {
    opts = opts || {};
    var label = opts.label != null ? opts.label :
      (stats.done + ' of ' + stats.total + ' modules · ' + stats.pct + '%');
    return '<div class="ilprog-bar" role="img" aria-label="Progress: ' + esc(label) + '">' +
      '<div class="ilprog-bar__meta"><span class="ilprog-bar__label">' + esc(label) + '</span></div>' +
      '<div class="ilprog-bar__track"><div class="ilprog-bar__fill" style="width:' + stats.pct + '%"></div></div>' +
      '</div>';
  }

  /* Continue banner HTML. Resolves titles from the sequence doc; falls back
     to course code + module id when the doc is unavailable. The CTA button
     always reads "Continue where you left off" unless opts.ctaLabel
     overrides it (user order 2026-10-08: explicit resume affordance). */
  function continueHTML(lp, seq, opts) {
    opts = opts || {};
    var entry = findEntry(seq, lp.courseId);
    var code = entry ? entry.code : lp.courseId;
    var cTitle = entry ? entry.title : '';
    var mTitle = findModuleTitle(entry, lp.moduleId) || lp.moduleId;
    var url = entry ? courseURL(entry, lp.moduleId) : null;
    if (!url) return '';
    return '<div class="ilprog-continue" role="region" aria-label="Continue where you left off">' +
      '<div class="ilprog-continue__txt">' +
      '<p class="ilprog-continue__eyebrow">Pick up right where you stopped</p>' +
      '<p class="ilprog-continue__desc"><strong>' + esc(code) + '</strong>' +
      (cTitle ? ' · ' + esc(cTitle) : '') +
      ' — ' + esc(mTitle) + '</p></div>' +
      '<a class="ilprog-continue__btn" href="' + esc(url) + '">' + esc(opts.ctaLabel || 'Continue where you left off') + '</a></div>';
  }

  /* "Start your guided path" variant — shown when the device has no
     progress yet. Points at the curriculum start (first sequence entry,
     IL-01). Falls back to the hardcoded IL-01 URL when the sequence doc
     is unavailable. */
  function startPathHTML(seq, opts) {
    opts = opts || {};
    var first = (seq && seq.courses && seq.courses.length) ? seq.courses[0] : null;
    var url = first ? courseURL(first) : '/university/course.html?course=il-01-esoteric-foundations';
    var code = first ? first.code : 'IL-01';
    var cTitle = first ? first.title : 'Esoteric Foundations';
    if (!url) return '';
    return '<div class="ilprog-continue ilprog-continue--start" role="region" aria-label="Start your guided path">' +
      '<div class="ilprog-continue__txt">' +
      '<p class="ilprog-continue__eyebrow">Begin the guided sequence</p>' +
      '<p class="ilprog-continue__desc"><strong>' + esc(code) + '</strong> · ' + esc(cTitle) +
      ' — the first step of the full curriculum</p></div>' +
      '<a class="ilprog-continue__btn" href="' + esc(url) + '">' + esc(opts.ctaLabel || 'Start your guided path') + '</a></div>';
  }

  /* Paint the banner into a container if (and only if) a last position exists. */
  function paintContinue(container, opts) {
    if (!container) return;
    var lp = getLastPosition();
    if (!lp) { container.style.display = 'none'; return; }
    loadSequence(function (seq) {
      var html = continueHTML(lp, seq, opts);
      if (!html) { container.style.display = 'none'; return; }
      container.innerHTML = html;
      container.style.display = '';
    });
  }

  /* Unified resume painter (user order 2026-10-08): last position exists →
     "Continue where you left off" banner; no progress yet → "Start your
     guided path" variant pointing at the curriculum start. */
  function paintResume(container, opts) {
    if (!container) return;
    var lp = getLastPosition();
    loadSequence(function (seq) {
      var html = lp ? continueHTML(lp, seq, opts) : startPathHTML(seq, opts);
      if (!html) { container.style.display = 'none'; return; }
      container.innerHTML = html;
      container.style.display = '';
    });
  }

  var api = {
    KEY: KEY,
    load: load,
    markComplete: markComplete,
    unmarkComplete: unmarkComplete,
    isComplete: isComplete,
    touch: touch,
    getLastPosition: getLastPosition,
    courseStats: courseStats,
    isCourseComplete: isCourseComplete,
    loadSequence: loadSequence,
    findEntry: findEntry,
    nextEntry: nextEntry,
    findModuleTitle: findModuleTitle,
    courseURL: courseURL,
    progressBarHTML: progressBarHTML,
    continueHTML: continueHTML,
    startPathHTML: startPathHTML,
    paintContinue: paintContinue,
    paintResume: paintResume,
    esc: esc
  };
  g.ILProgress = api;

  /* Node test hook: expose without DOM. */
  try {
    if (typeof module !== 'undefined' && module.exports) module.exports = api;
  } catch (e) {}
})(typeof window !== 'undefined' ? window : this);
