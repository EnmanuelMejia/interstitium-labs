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
    /* 2026-10-08 (scope fix): resolved via TRACK, not chain position.
       Returns the next course in the same track (or null). */
    var rel = relatedCourses(seq, courseId, 1);
    return rel.length ? rel[0] : null;
  }

  /* Same-track related courses, excluding self, in track order.
     Never the flat 29-course chain. */
  function relatedCourses(seq, courseId, limit) {
    limit = limit || 3;
    if (!seq || !seq.courses) return [];
    var self = findEntry(seq, courseId);
    if (!self || !self.track) return [];
    var out = [];
    for (var i = 0; i < seq.courses.length && out.length < limit; i++) {
      var e = seq.courses[i];
      if (e.track === self.track && e.courseId !== self.courseId) out.push(e);
    }
    /* Frontier cross-link: IL-23 also relates to IL-22 (esoteric). */
    if (self.track === 'frontier' && seq.tracks && seq.tracks.frontier && seq.tracks.frontier.related) {
      var rel = seq.tracks.frontier.related;
      for (var j = 0; j < rel.length && out.length < limit; j++) {
        var code = rel[j], k;
        for (k = 0; k < seq.courses.length; k++) {
          if (seq.courses[k].code === code) { out.push(seq.courses[k]); break; }
        }
      }
    }
    return out;
  }

  function trackName(seq, courseId) {
    var e = findEntry(seq, courseId);
    if (!e || !e.track) return '';
    if (seq.tracks && seq.tracks[e.track] && seq.tracks[e.track].name) return seq.tracks[e.track].name;
    return e.track;
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
    /* 2026-10-09: titles like "IL-28 · DevSecOps ..." already carry the
       code — don't print it twice (same guard as startPathHTML). */
    var cTitleShown = (cTitle && cTitle.indexOf(code) === 0)
      ? cTitle : (cTitle ? code + ' · ' + cTitle : code);
    return '<div class="ilprog-continue" role="region" aria-label="Continue where you left off">' +
      '<div class="ilprog-continue__txt">' +
      '<p class="ilprog-continue__eyebrow">Pick up right where you stopped</p>' +
      '<p class="ilprog-continue__desc"><strong>' + esc(cTitleShown) + '</strong>' +
      ' — ' + esc(mTitle) + '</p></div>' +
      '<a class="ilprog-continue__btn" href="' + esc(url) + '">' + esc(opts.ctaLabel || 'Continue where you left off') + '</a></div>';
  }

  /* "Start the {CODE} guided path" — course-scoped (2026-10-08 scope fix).
     Shown when the device has no progress yet AND a course context is
     known. courseId may be a courseId or a slug. Points at THAT course's
     first module (?course=<slug>&module=<firstModuleId>) — never a
     universal IL-01 push onto unrelated courses. No course context →
     returns '' (no banner). */
  function startPathHTML(seq, courseId, opts) {
    opts = opts || {};
    var entry = null;
    if (seq && seq.courses && courseId) {
      for (var i = 0; i < seq.courses.length; i++) {
        var e = seq.courses[i];
        if (e.courseId === courseId || e.slug === courseId) { entry = e; break; }
      }
    }
    if (!entry) return '';
    var firstModuleId = (entry.modules && entry.modules.length && entry.modules[0].id) || null;
    var url = courseURL(entry, firstModuleId);
    if (!url) return '';
    var cta = opts.ctaLabel || ('Start the ' + entry.code + ' guided path');
    /* 2026-10-08: titles like "IL-29 · ThreatLocker ..." already carry the
       code — don't print it twice. */
    var titleShown = entry.title.indexOf(entry.code) === 0
      ? entry.title : (entry.code + ' · ' + entry.title);
    return '<div class="ilprog-continue ilprog-continue--start" role="region" aria-label="' + esc(cta) + '">' +
      '<div class="ilprog-continue__txt">' +
      '<p class="ilprog-continue__eyebrow">Begin this course\'s guided sequence</p>' +
      '<p class="ilprog-continue__desc"><strong>' + esc(titleShown) + '</strong></p></div>' +
      '<a class="ilprog-continue__btn" href="' + esc(url) + '">' + esc(cta) + '</a></div>';
  }

  /* Paint the banner into a container if (and only if) a last position exists. */
  function paintContinue(container, opts) {
    if (!container) return;
    /* 2026-10-08 (scope fix): nuke stale .ilprog-continue nodes in this
       container's subtree before painting, so bfcache/pre-fix markup can
       never stack duplicates. */
    try {
      var stale = container.querySelectorAll('.ilprog-continue');
      for (var i = 0; i < stale.length; i++) {
        if (stale[i].parentNode) stale[i].parentNode.removeChild(stale[i]);
      }
    } catch (e) {}
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
     "Continue where you left off" banner; no progress yet → course-scoped
     "Start the {CODE} guided path" when opts.courseId is known, otherwise
     nothing (never a universal IL-01 push). */
  function paintResume(container, opts) {
    if (!container) return;
    opts = opts || {};
    try {
      var stale = container.querySelectorAll('.ilprog-continue');
      for (var i = 0; i < stale.length; i++) {
        if (stale[i].parentNode) stale[i].parentNode.removeChild(stale[i]);
      }
    } catch (e) {}
    var lp = getLastPosition();
    loadSequence(function (seq) {
      var html = lp ? continueHTML(lp, seq, opts)
                    : (opts.courseId ? startPathHTML(seq, opts.courseId, opts) : '');
      if (typeof opts.onDone === 'function') { try { opts.onDone(!!html); } catch (e2) {} }
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
    relatedCourses: relatedCourses,
    trackName: trackName,
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
