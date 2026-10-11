/*!
 * IL Cinematic Framework — Global Initializer (il-cinematic-init.js)
 * ---------------------------------------------------------------------------
 * SINGLETON: guards against double-initialization. All pages reference this
 * one file; no per-page inline init scripts.
 *
 * Auto-detects the ambient audio theme from (in priority order):
 *   1. document.body[data-il-theme]
 *   2. document.body[data-audio-topic]
 *   3. document.body[data-topic-theme] (mapped via ILAmbient.topicTheme)
 *   4. Falls back to 'cyberpunk' (homepage default)
 *
 * Behavior:
 *   - Calls ILAmbient.arm(theme) for armed autoplay (first-gesture start)
 *   - Wires any #il-ambient-toggle button as master mute toggle
 *   - Syncs toggle visual state via light polling
 *
 * Usage: <script src="/assets/il-cinematic-init.js" defer></script>
 * Requires: /assets/il-ambient-synth.js loaded before (or with defer order).
 */
(function () {
  'use strict';

  // Singleton guard — rebuild-aware for SPA navigation.
  // il-spa-nav.js swaps documents via document.open/write/close: the Window
  // survives (flag stays set) but the widget DOM is wiped. Re-run the
  // asset loading when the widget element is missing from this document.
  if (window.__ilCinematicInitDone && document.getElementById('il-audio-widget')) return;
  window.__ilCinematicInitDone = true;

  // Dynamically load the floating widget's CSS + JS (each guarded internally),
  // plus the SPA navigator that keeps audio alive across page changes.
  function loadWidgetAssets() {
    try {
      if (!document.querySelector('link[href="/assets/il-audio-widget.css"]')) {
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/assets/il-audio-widget.css';
        document.head.appendChild(link);
      }
      if (!document.querySelector('link[href="/assets/il-rhel-cards.css"]')) {
        var rhelCss = document.createElement('link');
        rhelCss.rel = 'stylesheet';
        rhelCss.href = '/assets/il-rhel-cards.css';
        document.head.appendChild(rhelCss);
      }
      if (!document.querySelector('script[src="/assets/il-audio-widget.js"]')) {
        var s = document.createElement('script');
        s.src = '/assets/il-audio-widget.js';
        s.defer = true;
        document.head.appendChild(s);
      }
      if (!document.querySelector('script[src="/assets/il-rhel-cards.js"]')) {
        var rhelJs = document.createElement('script');
        rhelJs.src = '/assets/il-rhel-cards.js';
        rhelJs.defer = true;
        document.head.appendChild(rhelJs);
      }
      if (!document.querySelector('script[src="/assets/il-spa-nav.js"]')) {
        var nav = document.createElement('script');
        nav.src = '/assets/il-spa-nav.js';
        nav.defer = true;
        document.head.appendChild(nav);
      }
    } catch (e) {}
  }

  function detectTheme() {
    var body = document.body;
    if (!body) return 'cyberpunk';
    // 1. Explicit data-il-theme (highest priority, per user spec)
    var t = body.getAttribute('data-il-theme');
    if (t) return t;
    // 2. data-audio-topic (topic slug)
    var slug = body.getAttribute('data-audio-topic');
    // 3. data-topic-theme (visual theme key → map via topicTheme if it's a slug)
    if (!slug) slug = body.getAttribute('data-topic-theme');
    if (window.ILAmbient && window.ILAmbient.topicTheme && slug) {
      try { return window.ILAmbient.topicTheme(slug); } catch (e) {}
    }
    return 'cyberpunk';
  }

  function syncToggle(btn) {
    if (!btn || !window.ILAmbient) return;
    try {
      var on = window.ILAmbient.isPlaying && window.ILAmbient.isPlaying();
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    } catch (e) {}
  }

  // ---- Noah AI widget (noah-everywhere Phase 1) ----
  // Floating context-aware assistant on every page. Rebuild-aware for SPA
  // navigation: the widget DOM (#noah-launcher) is wiped on document swaps,
  // so re-run the load when the launcher element is missing.
  /* PRELOAD (2026-10-11): everything ready at init — zero waiting.
     Loads the preload system FIRST: connectors, onboarding, AI client,
     skills registry, Cloudflare setup scripts, provider flows.
     Background status checks run non-blocking via requestIdleCallback. */
  function loadPreloadAssets() {
    try {
      if (!document.querySelector('script[src="/assets/il-preload.js"]')) {
        var p = document.createElement('script');
        p.src = '/assets/il-preload.js';
        p.defer = true;
        document.head.appendChild(p);
      }
    } catch (e) {}
  }

  function loadNoahAssets() {
    try {
      if (document.getElementById('noah-launcher')) return; // already live
      if (!document.querySelector('link[href="/assets/il-noah-avatar.css"]')) {
        var ac = document.createElement('link');
        ac.rel = 'stylesheet';
        ac.href = '/assets/il-noah-avatar.css';
        document.head.appendChild(ac);
      }
      if (!document.querySelector('script[src="/assets/il-noah-avatar.js"]')) {
        var av = document.createElement('script');
        av.src = '/assets/il-noah-avatar.js';
        av.defer = true;
        document.head.appendChild(av);
      }
      if (!document.querySelector('script[src="/assets/noah-ai.js"]')) {
        var s = document.createElement('script');
        s.src = '/assets/noah-ai.js';
        s.defer = true;
        document.head.appendChild(s);
      }
      if (!document.querySelector('script[src="/assets/il-noah-context.js"]')) {
        var c = document.createElement('script');
        c.src = '/assets/il-noah-context.js';
        c.defer = true;
        document.head.appendChild(c);
      }
      if (!document.querySelector('script[src="/assets/noah-viz.js"]')) {
        var v = document.createElement('script');
        v.src = '/assets/noah-viz.js';
        v.defer = true;
        document.head.appendChild(v);
      }
      if (!document.querySelector('script[src="/assets/noah-docrender.js"]')) {
        var dr = document.createElement('script');
        dr.src = '/assets/noah-docrender.js';
        dr.defer = true;
        document.head.appendChild(dr);
      }
      if (!document.querySelector('script[src="/assets/noah-connectors.js"]')) {
        var nc = document.createElement('script');
        nc.src = '/assets/noah-connectors.js';
        nc.defer = true;
        document.head.appendChild(nc);
      }
      if (!document.querySelector('link[href="/assets/noah-onboarding.css"]')) {
        var oc = document.createElement('link');
        oc.rel = 'stylesheet';
        oc.href = '/assets/noah-onboarding.css';
        document.head.appendChild(oc);
      }
      if (!document.querySelector('script[src="/assets/noah-onboarding.js"]')) {
        var ob = document.createElement('script');
        ob.src = '/assets/noah-onboarding.js';
        ob.defer = true;
        document.head.appendChild(ob);
      }
      if (!document.querySelector('script[src="/assets/noah-interview.js"]')) {
        var iv = document.createElement('script');
        iv.src = '/assets/noah-interview.js';
        iv.defer = true;
        document.head.appendChild(iv);
      }
      /* Personal notes vault + mind maps (2026-10-10): il-notes.js must be
         present before Noah answers so the notes intents in noah-ai.js can
         read/search the vault; il-mindmap.js powers /my-notes/ maps and
         the CBT "Mind map" button. */
      if (!document.querySelector('script[src="/assets/il-notes.js"]')) {
        var nt = document.createElement('script');
        nt.src = '/assets/il-notes.js';
        nt.defer = true;
        document.head.appendChild(nt);
      }
      if (!document.querySelector('script[src="/assets/il-mindmap.js"]')) {
        var mm = document.createElement('script');
        mm.src = '/assets/il-mindmap.js';
        mm.defer = true;
        document.head.appendChild(mm);
      }
      if (!document.querySelector('script[src="/assets/il-sources.js"]')) {
        var so = document.createElement('script');
        so.src = '/assets/il-sources.js';
        so.defer = true;
        document.head.appendChild(so);
      }
      /* Account session library (2026-10-10): loaded sitewide so the
         session is known everywhere; mounts sign-in forms only where
         [data-il-auth] exists and gates only [data-il-auth-required]. */
      if (!document.querySelector('script[src="/assets/il-account.js"]') &&
          !document.querySelector('script[src="https://interstitiumlabs.dev/assets/il-account.js"]')) {
        var ac = document.createElement('script');
        ac.src = '/assets/il-account.js';
        ac.defer = true;
        document.head.appendChild(ac);
      }
      /* Cross-device sync (2026-10-10): when signed in, il-sync.js keeps
         the notes vault, interview history, Noah memory, and preferences
         reconciled with /api/user/sync so they follow the learner. */
      if (!document.querySelector('script[src="/assets/il-sync.js"]') &&
          !document.querySelector('script[src="https://interstitiumlabs.dev/assets/il-sync.js"]')) {
        var sy = document.createElement('script');
        sy.src = '/assets/il-sync.js';
        sy.defer = true;
        document.head.appendChild(sy);
      }
    } catch (e) {}
  }

  // ---- Global search / command palette (unified shell) ----
  // ⌘K/Ctrl+K fuzzy search across the whole site. Loaded once per page.
  function loadSearchAssets() {
    try {
      if (document.querySelector('[data-il-search-open]')) return; // already live
      if (!document.querySelector('link[href="/assets/il-command-palette.css"]')) {
        var sc = document.createElement('link');
        sc.rel = 'stylesheet';
        sc.href = '/assets/il-command-palette.css';
        document.head.appendChild(sc);
      }
      if (!document.querySelector('script[src="/assets/il-search.js"]')) {
        var ss = document.createElement('script');
        ss.src = '/assets/il-search.js';
        ss.defer = true;
        document.head.appendChild(ss);
      }
    } catch (e) {}
  }

  function init() {
    // PRELOAD: everything bundled and ready at init — zero waiting.
    // Loads connectors, onboarding, AI client, skills registry, and
    // kicks off background status checks. Non-blocking.
    loadPreloadAssets();

    // Noah AI widget loads independently of the audio engine — never gate
    // the assistant on ambient-audio availability.
    loadNoahAssets();

    // Global search / command palette on every page.
    loadSearchAssets();

    if (!window.ILAmbient) {
      // Synth not loaded yet — retry once after a short delay.
      setTimeout(init, 500);
      return;
    }

    // Auto-load the floating audio widget (CSS + JS) — singleton guarded.
    loadWidgetAssets();

    var theme = detectTheme();

    // Armed autoplay: start on first user gesture.
    try {
      if (window.ILAmbient.arm) window.ILAmbient.arm(theme);
    } catch (e) {}

    // Master mute toggle (if present on this page).
    var btn = document.getElementById('il-ambient-toggle');
    if (btn) {
      // Guard against double-binding if init runs twice.
      if (!btn.__ilAmbientBound) {
        btn.__ilAmbientBound = true;
        btn.addEventListener('click', function () {
          try {
            if (window.ILAmbient.isPlaying && window.ILAmbient.isPlaying()) {
              window.ILAmbient.stop();
            } else {
              window.ILAmbient.play(theme);
            }
          } catch (e) {}
          setTimeout(function () { syncToggle(btn); }, 350);
        });
      }
      // Keep toggle visual in sync. Clear any timer left by a previous
      // document (SPA navigation rebuild) before starting a new one.
      try { if (window.__ilCiToggleT) clearInterval(window.__ilCiToggleT); } catch (e) {}
      window.__ilCiToggleT = setInterval(function () {
        if (!document.contains(btn)) { clearInterval(window.__ilCiToggleT); return; }
        syncToggle(btn);
      }, 1500);
      syncToggle(btn);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    // Defer slightly so the synth script (also deferred) runs first.
    setTimeout(init, 50);
  }
})();
