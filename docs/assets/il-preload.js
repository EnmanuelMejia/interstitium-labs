/* Interstitium Labs — Preload System (il-preload.js).
   Everything preloaded at shell init. Zero waiting.
   Bundles: connectors, onboarding scripts, Cloudflare setup scripts,
   provider OAuth flows, skill definitions. Background status checks.
   Vanilla JS, zero dependencies, ES5-compatible.
   Exposes window.ILPreload. */
(function () {
  'use strict';

  /* ---------------- preload manifest ---------------- */
  var MANIFEST = {
    version: 3,
    builtAt: '2026-10-11',
    bundles: {
      connectors: ['gmail', 'gcal', 'github'],
      onboarding: ['noah-onboarding'],
      cloudflare: ['workers', 'kv', 'd1', 'r2', 'ai', 'ai-gateway'],
      providers: ['google-oauth', 'github-oauth'],
      skills: ['tutor', 'lab-gen', 'research', 'code', 'viz', 'docs', 'voice', 'connectors', 'notes'],
      ai: ['ai-client', 'ai-dynamic', 'noah-ai', 'noah-viz', 'noah-docrender'],
      notes: ['il-notes', 'il-mindmap'],
    },
  };

  var state = {
    loaded: {},       /* bundle -> true when script confirmed present */
    status: {},       /* connector/skill id -> 'ready'|'setup-needed'|'checking'|'error' */
    ready: false,
    readyAt: null,
    backgroundDone: false,
  };

  /* ---------------- script preloading ---------------- */

  var PRELOAD_SCRIPTS = [
    '/assets/ai-client.js',
    '/assets/noah-connectors.js',
    '/assets/noah-onboarding.js',
    '/assets/noah-ai.js',
    '/assets/noah-viz.js',
    '/assets/noah-docrender.js',
    '/assets/il-noah-context.js',
    '/assets/il-notes.js',
    '/assets/il-mindmap.js',
  ];

  function ensureScript(src, cb) {
    if (document.querySelector('script[src="' + src + '"]')) {
      if (cb) cb(true);
      return;
    }
    var s = document.createElement('script');
    s.src = src;
    s.defer = true;
    s.onload = function () { if (cb) cb(true); };
    s.onerror = function () { if (cb) cb(false); };
    document.head.appendChild(s);
  }

  function preloadAll(done) {
    var pending = PRELOAD_SCRIPTS.length;
    var results = {};
    if (!pending) { if (done) done(results); return; }
    PRELOAD_SCRIPTS.forEach(function (src) {
      ensureScript(src, function (ok) {
        results[src] = ok;
        state.loaded[src] = ok;
        pending--;
        if (pending === 0 && done) done(results);
      });
    });
  }

  /* ---------------- Cloudflare setup scripts ----------------
     Preloaded definitions for provisioning Cloudflare resources.
     Each script is a declarative spec — the actual provisioning happens
     via the Cloudflare API or wrangler, guided by Noah. */

  var CF_SETUP_SCRIPTS = {
    workers: {
      label: 'Cloudflare Workers',
      desc: 'Serverless functions at the edge',
      steps: ['Create worker via API', 'Set compatibility date', 'Deploy code', 'Verify route'],
    },
    kv: {
      label: 'Workers KV',
      desc: 'Key-value storage',
      steps: ['Create namespace', 'Bind to worker', 'Verify read/write'],
    },
    d1: {
      label: 'D1 Database',
      desc: 'Serverless SQL',
      steps: ['Create database', 'Run migrations', 'Bind to worker'],
    },
    r2: {
      label: 'R2 Storage',
      desc: 'S3-compatible object storage',
      steps: ['Create bucket', 'Set CORS', 'Bind to worker'],
    },
    ai: {
      label: 'Workers AI',
      desc: 'GPU inference for open models',
      steps: ['Enable AI binding', 'Select models', 'Test inference'],
    },
    'ai-gateway': {
      label: 'AI Gateway',
      desc: 'Caching, rate limiting, observability for AI calls',
      steps: ['Create gateway', 'Configure cache', 'Route traffic'],
    },
  };

  /* ---------------- provider OAuth flows ---------------- */

  var PROVIDER_FLOWS = {
    'google-oauth': {
      label: 'Google OAuth',
      desc: 'Gmail, Calendar, Drive access',
      scopes: ['gmail.readonly', 'calendar', 'drive.readonly'],
      setupUrl: '/noah/#settings',
      steps: ['Create OAuth client', 'Configure redirect URI', 'User authorizes', 'Store tokens'],
    },
    'github-oauth': {
      label: 'GitHub OAuth',
      desc: 'Repo access, PRs, issues, workflows',
      scopes: ['repo', 'read:org'],
      setupUrl: '/noah/#settings',
      steps: ['Create OAuth app', 'Configure callback', 'User authorizes', 'Store tokens'],
    },
  };

  /* ---------------- skill registry ----------------
     All skills loaded at startup, not on-demand. */

  var SKILLS = {
    tutor: {
      label: 'Socratic Tutor', desc: 'Adaptive teaching with questions-first method',
      agent: 'tutor', taskType: 'tutor', unlocked: true,
    },
    'lab-gen': {
      label: 'Dynamic Labs', desc: 'AI-generated scenarios, evaluation, hints',
      agent: 'lab', taskType: 'lab-gen', unlocked: true,
    },
    research: {
      label: 'Research', desc: 'Web search and source synthesis',
      agent: 'research', taskType: 'chat', unlocked: true,
    },
    code: {
      label: 'Code Assistant', desc: 'Generation, debugging, review',
      agent: 'code', taskType: 'code', unlocked: true,
    },
    viz: {
      label: 'Visualizations', desc: 'Living diagrams and system anatomies',
      client: 'NoahViz', unlocked: true,
    },
    docs: {
      label: 'Documents', desc: 'Inline rendering of any document type',
      client: 'NoahDoc', unlocked: true,
    },
    voice: {
      label: 'Voice', desc: 'Speech input and neural voice output',
      client: 'IL.noahVoice', unlocked: false, unlockAfter: 10,
    },
    connectors: {
      label: 'Connectors', desc: 'Gmail, Calendar, GitHub automation',
      client: 'NoahConnectors', unlocked: false, manual: true,
    },
  };

  function listSkills() {
    return Object.keys(SKILLS).map(function (id) {
      var s = SKILLS[id];
      return { id: id, label: s.label, desc: s.desc, unlocked: s.unlocked,
               status: state.status['skill:' + id] || 'ready' };
    });
  }

  function getSkill(id) { return SKILLS[id] || null; }

  /* ---------------- background status checks ----------------
     Non-blocking. Runs after page is interactive. */

  function checkConnectorStatus() {
    /* Check each connector's auth status via the backend. */
    if (!window.NoahConnectors) return;
    var list = window.NoahConnectors.list();
    list.forEach(function (c) {
      state.status['connector:' + c.id] = 'checking';
    });
    /* Batch status check — single request. */
    try {
      fetch('/api/noah/connectors', { method: 'GET' })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data && data.connectors) {
            data.connectors.forEach(function (c) {
              state.status['connector:' + c.id] = c.connected ? 'ready' : 'setup-needed';
            });
          }
          state.backgroundDone = true;
        })
        .catch(function () {
          list.forEach(function (c) {
            state.status['connector:' + c.id] = 'unknown';
          });
          state.backgroundDone = true;
        });
    } catch (e) {
      state.backgroundDone = true;
    }
  }

  function checkAiStatus() {
    /* Verify the AI backend is reachable. */
    try {
      fetch('/api/ai/models', { method: 'GET' })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          state.status.ai = (data && data.ok) ? 'ready' : 'error';
          state.status.aiModels = (data && data.models) ? data.models.length : 0;
          state.status.aiAgents = (data && data.agents) ? data.agents.length : 0;
        })
        .catch(function () { state.status.ai = 'error'; });
    } catch (e) {
      state.status.ai = 'error';
    }
  }

  function runBackgroundChecks() {
    /* Defer until the browser is idle — never block page interaction. */
    function go() {
      checkConnectorStatus();
      checkAiStatus();
    }
    if (typeof requestIdleCallback !== 'undefined') {
      requestIdleCallback(go, { timeout: 5000 });
    } else {
      setTimeout(go, 2000);
    }
  }

  /* ---------------- init ---------------- */

  function init() {
    if (window.__ilPreloadDone) return;
    window.__ilPreloadDone = true;

    preloadAll(function () {
      state.ready = true;
      state.readyAt = new Date().toISOString();
      /* Fire ready event for dependent modules. */
      try {
        document.dispatchEvent(new CustomEvent('il:preload-ready', {
          detail: { manifest: MANIFEST, status: state.status },
        }));
      } catch (e) {}
      /* Background checks don't block readiness. */
      runBackgroundChecks();
    });
  }

  /* Auto-init on DOM ready. */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.ILPreload = {
    version: MANIFEST.version,
    manifest: MANIFEST,
    isReady: function () { return state.ready; },
    getStatus: function () { return JSON.parse(JSON.stringify(state.status)); },
    listSkills: listSkills,
    getSkill: getSkill,
    getSetupScript: function (id) { return CF_SETUP_SCRIPTS[id] || null; },
    listSetupScripts: function () {
      return Object.keys(CF_SETUP_SCRIPTS).map(function (id) {
        return { id: id, label: CF_SETUP_SCRIPTS[id].label, desc: CF_SETUP_SCRIPTS[id].desc };
      });
    },
    getProviderFlow: function (id) { return PROVIDER_FLOWS[id] || null; },
    listProviderFlows: function () {
      return Object.keys(PROVIDER_FLOWS).map(function (id) {
        return { id: id, label: PROVIDER_FLOWS[id].label, desc: PROVIDER_FLOWS[id].desc };
      });
    },
    listConnectors: function () {
      if (!window.NoahConnectors) return [];
      return window.NoahConnectors.list().map(function (c) {
        return { id: c.id, label: c.label, icon: c.icon,
                 status: state.status['connector:' + c.id] || 'unknown' };
      });
    },
    init: init,
  };
})();
