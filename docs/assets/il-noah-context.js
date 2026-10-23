/*!
 * IL Noah Context — page-context derivation for the Noah AI widget.
 * ---------------------------------------------------------------------------
 * Derives lightweight, privacy-safe page metadata and publishes it to the
 * Noah widget via window.IL.noahAI.setPageContext(). Runs on initial load
 * and after every SPA navigation swap (rebuild-aware, idempotent).
 *
 * Privacy: reads ONLY explicitly authored data-* attributes, document.title,
 * and location.pathname. Never innerText, code, selections, or form values.
 *
 * Usage: <script src="/assets/il-noah-context.js" defer></script>
 * Requires: /assets/noah-ai.js loaded (or loads alongside; waits for
 *           window.IL.noahAI to exist before publishing).
 */
(function () {
  'use strict';

  // Theme values used across the site -> Noah local-engine topic names.
  var THEME_TO_TOPIC = {
    cybersecurity: 'security',
    'system-design': 'general',
    networking: 'networking',
    'cloud-devops': 'devops',
    'ai-ml': 'general',
    'data-engineering': 'sql',
    programming: 'python',
    databases: 'sql',
    'linux-systems': 'linux',
    mathematics: 'algebra',
    'web-development': 'web',
    blockchain: 'blockchain',
    cryptocurrency: 'blockchain',
    cybernetics: 'general',
    esoteric: 'general',
    om: 'general'
  };

  function deriveContext() {
    var doc = document, loc = window.location;
    var path = loc.pathname || '/';
    var ctx = {
      title: doc.title || '',
      path: path,
      page_type: 'other',
      theme: '',
      topic: 'general',
      cbt_slug: '',
      course_code: '',
      lesson: null
    };

    // Theme from body attributes (same priority as the cinematic audio init).
    var body = doc.body;
    if (body) {
      ctx.theme = body.getAttribute('data-il-theme') ||
                  body.getAttribute('data-audio-topic') ||
                  body.getAttribute('data-topic-theme') || '';
      if (ctx.theme && THEME_TO_TOPIC[ctx.theme]) ctx.topic = THEME_TO_TOPIC[ctx.theme];
    }

    // Page type + slugs from URL shape.
    var bootcampM = path.match(/^\/bootcamps\/([^\/]+)\/?/);
    if (bootcampM) {
      ctx.page_type = 'cbt';
      ctx.cbt_slug = bootcampM[1];
    } else if (/^\/university\/course/.test(path)) {
      ctx.page_type = 'course';
      try {
        var q = new URLSearchParams(loc.search);
        ctx.course_code = q.get('course') || '';
      } catch (e) {}
    } else if (/^\/university/.test(path)) {
      ctx.page_type = 'course';
    } else if (/^\/topics\//.test(path)) {
      ctx.page_type = 'topic';
    } else if (/^\/labs\//.test(path) || /\/lab\//.test(path)) {
      ctx.page_type = 'lab';
    } else if (path === '/' || path === '/index.html') {
      ctx.page_type = 'home';
    } else if (/^\/paths\//.test(path)) {
      ctx.page_type = 'path';
    }

    // Lesson metadata (CBT shell sets these in learn.js).
    try {
      var host = doc.querySelector('[data-noah-lesson-id], [data-il-lesson-id]');
      if (host) {
        ctx.lesson = {
          id: host.getAttribute('data-noah-lesson-id') || host.getAttribute('data-il-lesson-id') || '',
          title: host.getAttribute('data-noah-lesson-title') || host.getAttribute('data-il-lesson-title') || '',
          topic: host.getAttribute('data-noah-lesson-topic') || host.getAttribute('data-il-lesson-topic') || '',
          domain: host.getAttribute('data-noah-lesson-domain') || host.getAttribute('data-il-lesson-domain') || ''
        };
        if (ctx.lesson.topic && THEME_TO_TOPIC[ctx.lesson.topic]) {
          ctx.topic = THEME_TO_TOPIC[ctx.lesson.topic];
        }
      }
    } catch (e) {}

    return ctx;
  }

  // Context-aware suggestion chips per page type. The widget prepends these
  // to its default chips (deduped). Short imperative labels, tap-to-ask.
  function chipsFor(ctx) {
    switch (ctx.page_type) {
      case 'cbt':
        if (ctx.lesson && ctx.lesson.title) return ['Explain this lesson', 'Give me a hint', 'Quiz me on this'];
        return ['Explain a concept from this CBT', 'How should I study this?', 'What should I practice next?'];
      case 'course':
        return ['Summarize this module', 'Explain a difficult concept', 'Give me practice questions'];
      case 'lab':
        return ['I\'m stuck — what next?', 'Explain this command', 'What is this lab teaching?'];
      case 'topic':
        return ['What should I learn first here?', 'Explain a key concept', 'How does this connect to other topics?'];
      case 'home':
        return ['Help me pick a learning path', 'What should I learn first?', 'I have an interview coming up'];
      case 'path':
        return ['Where do I start on this path?', 'How long will this take?', 'What comes after this?'];
      default:
        return [];
    }
  }

  var lastSig = '';
  function refresh() {
    var ctx = deriveContext();
    var sig = JSON.stringify([ctx.path, ctx.title, ctx.lesson && ctx.lesson.id]);
    var changed = sig !== lastSig;
    lastSig = sig;
    try {
      window.IL = window.IL || {};
      window.IL.noahPageContext = function () { return ctx; };
      var api = window.IL.noahAI;
      if (api && typeof api.setPageContext === 'function') {
        api.setPageContext(ctx, chipsFor(ctx));
      } else if (changed) {
        // Widget not ready yet — retry shortly (bounded).
        var tries = 0;
        var timer = setInterval(function () {
          tries++;
          var a2 = window.IL && window.IL.noahAI;
          if (a2 && typeof a2.setPageContext === 'function') {
            clearInterval(timer);
            a2.setPageContext(ctx, chipsFor(ctx));
          } else if (tries > 40) clearInterval(timer);
        }, 250);
      }
    } catch (e) {}
    return ctx;
  }

  // Public: re-derive after SPA swaps or dynamic lesson renders.
  window.IL = window.IL || {};
  window.IL.noahContextRefresh = refresh;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', refresh);
  } else {
    refresh();
  }
  // Re-derive after SPA navigation swaps the document.
  window.addEventListener('noah:context-refresh', refresh);
  window.addEventListener('popstate', function () { setTimeout(refresh, 50); });
})();
