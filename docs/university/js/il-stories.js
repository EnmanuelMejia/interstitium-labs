/* ==========================================================================
 * Interstitium Labs — "The story behind X" narrative supplements (2026-10-08)
 *
 * WORKSTREAM 1. Player-side join: the course JSONs were deliberately NOT
 * modified (a sibling worker owns them for video work). Stories join at
 * render time via docs/university/data/courses/stories/_index.json, which
 * maps course slug -> {file, count, stories:[{id,title,moduleId}]}.
 *
 * Paywall posture: full story text for gated courses (IL-01 through IL-26)
 * renders ONLY inside the course shell, where the worker 402s gated course
 * JSONs without a valid entitlement cookie. On public surfaces (catalog
 * browser, story of the day) gated courses surface title + lock badge only —
 * their story JSON is never fetched. Client code treats anything that is
 * not one of the three free slugs as gated (fail closed).
 *
 * Accessibility: semantic headings, aria labels; no animated reveals — the
 * CSS honors prefers-reduced-motion. Verified story content is rendered
 * verbatim (escaped); nothing here generates historical claims.
 * ========================================================================== */
(function () {
  'use strict';

  /* ---- paths ------------------------------------------------------------ */
  var BASE = null;
  function scriptDir() {
    if (BASE !== null) return BASE;
    try {
      var s = document.currentScript && document.currentScript.src;
      if (s) { BASE = s.replace(/\/[^\/]*$/, '/'); return BASE; }
    } catch (e) { /* fall through */ }
    BASE = '';
    return BASE;
  }
  function url(rel) { return scriptDir() + rel; }
  var STORIES_DIR = 'data/courses/stories/';
  var INDEX_URL = 'data/courses/stories/_index.json';

  /* ---- gating (mirror of docs/_worker.js FREE_COURSE_SLUGS) ------------- */
  var FREE_SLUGS = [
    'il-27-it-infrastructure-specialist-threatlocker-mastery',
    'il-28-devsecops-cloud-infrastructure-mastery',
    'il-29-threatlocker-ai-cybersecurity-mastery'
  ];
  function isFreeSlug(slug) { return FREE_SLUGS.indexOf(String(slug || '')) !== -1; }
  /* Fail closed: anything not explicitly free counts as gated. */
  function isGatedSlug(slug) { return !isFreeSlug(slug); }

  /* ---- utils ------------------------------------------------------------ */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function codeFromSlug(slug) {
    var m = /^il-(\d+)/.exec(String(slug || ''));
    return m ? 'IL-' + m[1] : 'IL';
  }
  function dateKey(d) {
    var y = d.getFullYear(),
        m = ('0' + (d.getMonth() + 1)).slice(-2),
        dd = ('0' + d.getDate()).slice(-2);
    return y + '-' + m + '-' + dd;
  }
  function hashStr(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = (h * 16777619) >>> 0; }
    return h;
  }

  /* ---- data loading (lazy, cached) -------------------------------------- */
  var indexPromise = null;
  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(url(INDEX_URL), { credentials: 'same-origin' })
        .then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.json();
        })
        .catch(function () { return { version: 1, totalStories: 0, courses: {} }; });
    }
    return indexPromise;
  }

  var coursePromises = {};
  var resolvedCourses = {}; /* slug -> stories array, for the sync getter */
  function loadCourseStories(slug) {
    if (!coursePromises[slug]) {
      coursePromises[slug] = loadIndex().then(function (idx) {
        var e = (idx.courses || {})[slug];
        if (!e || !e.file) return [];
        return fetch(url('data/courses/' + e.file), { credentials: 'same-origin' })
          .then(function (r) {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json();
          })
          .then(function (d) { return (d && d.stories) || []; })
          .catch(function () { return []; });
      }).then(function (arr) {
        resolvedCourses[slug] = arr;
        return arr;
      });
    }
    return coursePromises[slug];
  }

  /**
   * Sync lookup — returns the story object for (courseSlug, moduleId), or
   * null when the course's stories have not been loaded yet / none maps.
   * Call loadCourseStories(slug) first (or use enhanceModule) to hydrate.
   */
  function getStoryForModule(courseSlug, moduleId) {
    var arr = resolvedCourses[courseSlug];
    if (!arr || !moduleId) return null;
    for (var i = 0; i < arr.length; i++) {
      if (arr[i] && arr[i].moduleId === moduleId) return arr[i];
    }
    return null;
  }

  /* ---- story card ------------------------------------------------------- */
  /* Narratives are authored as one long paragraph (300-600 words). Split
     into ~140-word paragraphs at sentence boundaries for readability. */
  function storyParagraphs(narrative) {
    var txt = String(narrative || '');
    var sents = txt.split(/(?<=[.!?])\s+(?=[A-Z0-9"\u201c])/);
    var paras = [], cur = [], words = 0;
    sents.forEach(function (s) {
      s = s.trim();
      if (!s) return;
      cur.push(s);
      words += s.split(/\s+/).length;
      if (words >= 140) { paras.push(cur.join(' ')); cur = []; words = 0; }
    });
    if (cur.length) paras.push(cur.join(' '));
    return paras.length ? paras : [txt];
  }

  /**
   * storyCardHTML(story) -> HTML string. Hook as headline, narrative as body,
   * figures as a small cast line, bridge as the transition. Semantic
   * <aside>, heading + aria label, multicloud dark theme (gold accents).
   */
  function storyCardHTML(story) {
    var id = 'il-story-' + String(story.id || 'x').replace(/[^a-z0-9-]/gi, '-');
    var paras = storyParagraphs(story.narrative).map(function (p) {
      return '<p>' + esc(p) + '</p>';
    }).join('');
    var cast = (story.figures || []).map(function (f) {
      return esc(f.name) +
        (f.role ? ' — ' + esc(f.role) : '') +
        (f.dates ? ' (' + esc(f.dates) + ')' : '');
    }).join(' · ');
    return '<aside class="il-story" aria-labelledby="' + id + '-hook">' +
      '<div class="il-story__kicker">THE STORY BEHIND</div>' +
      '<h3 class="il-story__hook" id="' + id + '-hook">' + esc(story.hook) + '</h3>' +
      '<div class="il-story__narr">' + paras + '</div>' +
      (cast ? '<p class="il-story__cast"><span class="il-story__cast-label">Cast:</span> ' + cast + '</p>' : '') +
      (story.bridge ? '<p class="il-story__bridge">' + esc(story.bridge) + '</p>' : '') +
      '</aside>';
  }

  /**
   * enhanceModule(courseSlug, moduleId, bodyEl) — loads the course's stories
   * (cached) and prepends the story card as the FIRST element inside
   * bodyEl when a story maps to the module. No story -> renders nothing.
   */
  function enhanceModule(courseSlug, moduleId, bodyEl) {
    if (!courseSlug || !moduleId || !bodyEl) return Promise.resolve(null);
    return loadCourseStories(courseSlug).then(function () {
      var story = getStoryForModule(courseSlug, moduleId);
      if (!story) return null;
      var tmp = document.createElement('div');
      tmp.innerHTML = storyCardHTML(story);
      var card = tmp.firstElementChild;
      if (card && bodyEl.firstChild) bodyEl.insertBefore(card, bodyEl.firstChild);
      else if (card) bodyEl.appendChild(card);
      return story;
    });
  }

  /* ---- course overview "Stories" rail ----------------------------------- */
  /**
   * buildRail(hostEl, courseSlug) — fills hostEl with the course's stories:
   * title + hook per story, with a button that deep-opens the module the
   * story maps to (via window.__ilOpenModule, provided by course-shell.js).
   * Async; renders nothing when the course has no stories.
   */
  function buildRail(hostEl, courseSlug) {
    if (!hostEl) return Promise.resolve();
    return loadCourseStories(courseSlug).then(function (stories) {
      if (!stories.length) return;
      var html = '<h2 class="section-title" id="il-stories-rail-h">Stories</h2>' +
        '<p class="section-sub">The human stories behind the material — open one to reach its module.</p>' +
        '<div class="il-stories-rail" role="list" aria-labelledby="il-stories-rail-h">';
      stories.forEach(function (s) {
        html += '<article class="il-story-rail__item" role="listitem">' +
          '<h3>' + esc(s.title) + '</h3>' +
          '<p class="il-story-rail__hook">' + esc(s.hook) + '</p>' +
          '<button type="button" class="btn" data-story-module="' + esc(s.moduleId) + '"' +
          ' aria-label="Open the module for ' + esc(s.title) + '">' +
          'Open the module <span aria-hidden="true">&rarr;</span></button>' +
          '</article>';
      });
      html += '</div>';
      hostEl.innerHTML = html;
      var btns = hostEl.querySelectorAll('[data-story-module]');
      Array.prototype.forEach.call(btns, function (b) {
        b.addEventListener('click', function () {
          var mid = b.getAttribute('data-story-module');
          if (typeof window.__ilOpenModule === 'function') window.__ilOpenModule(mid);
        });
      });
    });
  }

  /* ---- cross-course browser --------------------------------------------- */
  function storyIndexEntries(idx) {
    var all = [];
    Object.keys(idx.courses || {}).sort().forEach(function (slug) {
      ((idx.courses[slug] || {}).stories || []).forEach(function (st) {
        all.push({ slug: slug, id: st.id, title: st.title, moduleId: st.moduleId });
      });
    });
    return all;
  }

  /**
   * storyOfTheDay() — deterministic pick from all 104 index entries by
   * calendar date (hash of YYYY-MM-DD mod N). Returns {slug,id,title,moduleId}.
   */
  function storyOfTheDay() {
    return loadIndex().then(function (idx) {
      var all = storyIndexEntries(idx);
      if (!all.length) return null;
      return all[hashStr(dateKey(new Date())) % all.length];
    });
  }

  /**
   * renderCatalogStories(hostEl) — cross-course browser: one group per
   * course (104 entries with course linkage). Gated courses show title +
   * lock badge ONLY (their story JSON is never fetched); free courses show
   * title + hook and link into the course shell at the mapped module.
   */
  function renderCatalogStories(hostEl) {
    if (!hostEl) return Promise.resolve();
    return loadIndex().then(function (idx) {
      var slugs = Object.keys(idx.courses || {}).sort();
      var html = '';
      slugs.forEach(function (slug) {
        var e = idx.courses[slug] || {};
        var gated = isGatedSlug(slug);
        var code = codeFromSlug(slug);
        html += '<div class="il-stories-course">' +
          '<h3 class="il-stories-course__h"><span>' + esc(code) + '</span> ' +
          (gated
            ? '<span class="il-badge il-badge-paid" aria-label="Requires enrollment">Enrolled only</span>'
            : '<span class="il-badge il-badge-free" aria-label="Free course">Free</span>') +
          '<span class="il-stories-course__count" aria-label="' + ((e.stories || []).length) + ' stories">' +
          (e.stories || []).length + '</span></h3>' +
          '<div class="il-stories-grid" role="list">';
        (e.stories || []).forEach(function (st) {
          var modLink = 'course.html?course=' + encodeURIComponent(slug) +
            (st.moduleId ? '&module=' + encodeURIComponent(st.moduleId) : '');
          html += '<article class="il-story-card" role="listitem">' +
            '<h4>' + esc(st.title) + '</h4>' +
            (gated
              ? '<p class="il-story-card__lock">🔒 The full story unlocks with ' + esc(code) +
                ' enrollment — the title is all that shows here.</p>' +
                '<p><a class="btn btn-sm" href="' + esc(modLink) + '">View the course</a></p>'
              : '<p class="il-story-card__hook">' + esc(st.hook || '') + '</p>' +
                '<p><a class="btn btn-sm" href="' + esc(modLink) + '"' +
                ' aria-label="Read ' + esc(st.title) + '">Read the story <span aria-hidden="true">&rarr;</span></a></p>') +
            '</article>';
        });
        html += '</div></div>';
      });
      hostEl.innerHTML = html;
    });
  }

  /**
   * renderStoryOfTheDay(hostEl) — the deterministic daily pick. Free-course
   * picks render title + hook + a link to read the full story in the shell;
   * gated-course picks render title + lock badge (story text never fetched).
   */
  function renderStoryOfTheDay(hostEl) {
    if (!hostEl) return Promise.resolve();
    return storyOfTheDay().then(function (pick) {
      if (!pick) { hostEl.innerHTML = ''; return; }
      var gated = isGatedSlug(pick.slug);
      var code = codeFromSlug(pick.slug);
      var modLink = 'course.html?course=' + encodeURIComponent(pick.slug) +
        (pick.moduleId ? '&module=' + encodeURIComponent(pick.moduleId) : '');
      return (gated ? Promise.resolve(null) : loadCourseStories(pick.slug).then(function (arr) {
        for (var i = 0; i < arr.length; i++) if (arr[i].id === pick.id) return arr[i];
        return null;
      })).then(function (full) {
        var html = '<article class="il-sotd" aria-labelledby="il-sotd-h">' +
          '<div class="il-sotd__kicker">STORY OF THE DAY · ' + esc(dateKey(new Date())) + '</div>' +
          '<h3 id="il-sotd-h">' + esc(pick.title) + '</h3>' +
          '<p class="il-sotd__course">' + esc(code) + ' ' +
          (gated
            ? '<span class="il-badge il-badge-paid">Enrolled only</span>'
            : '<span class="il-badge il-badge-free">Free</span>') + '</p>' +
          (full && full.hook ? '<p class="il-sotd__hook">“' + esc(full.hook) + '”</p>' : '') +
          (gated
            ? '<p class="il-sotd__lock">🔒 This story belongs to a gated course — unlock ' + esc(code) +
              ' to read it inside the course shell.</p>'
            : '<p><a class="btn" href="' + esc(modLink) + '"' +
              ' aria-label="Read the full story: ' + esc(pick.title) + '">' +
              'Read the full story <span aria-hidden="true">&rarr;</span></a></p>') +
          '</article>';
        hostEl.innerHTML = html;
      });
    });
  }

  /* ---- public API -------------------------------------------------------- */
  window.ILStories = {
    loadIndex: loadIndex,
    loadCourseStories: loadCourseStories,
    getStoryForModule: getStoryForModule,
    storyCardHTML: storyCardHTML,
    enhanceModule: enhanceModule,
    buildRail: buildRail,
    storyOfTheDay: storyOfTheDay,
    renderCatalogStories: renderCatalogStories,
    renderStoryOfTheDay: renderStoryOfTheDay,
    isFreeSlug: isFreeSlug,
    isGatedSlug: isGatedSlug,
    esc: esc,
    codeFromSlug: codeFromSlug
  };
})();
