/* =====================================================================
 * Interstitium Labs — Noah AI Unified Loader (2026-10-09)
 *
 * Loads the complete Noah AI capability suite in dependency order:
 *   1. noah-ai.js       — base widget (window.IL.noahAI)
 *   2. noah-voice.js    — voice input/output, model selector, mode toggle
 *   3. noah-personas.js — 5 personas, 5 voice profiles, 4 avatars
 *   4. noah-adaptive.js — adaptive learning, SM-2, analytics
 *
 * Usage: <script src="/assets/noah-full.js" defer></script>
 * Replaces individual <script> tags for noah-ai.js and related files.
 *
 * All files must be present at /assets/. If a file fails to load,
 * the loader continues with the remaining files (graceful degradation).
 * ===================================================================== */
(function () {
  'use strict';

  // Signal to noah-ai.js that the full loader is in charge: it must skip
  // its own auto-inject of the capability modules (its guards run at parse
  // time, before we inject the module scripts, so attribute guards alone
  // cannot prevent the double-load).
  try { window.__noahFullLoader = true; } catch (e) {}

  var BASE = '/assets/';
  // Map each file to its data-noah-* guard attribute. noah-ai.js auto-injects
  // the capability modules unless it sees these attributes, so we set them
  // here to prevent double-loading (2026-10-09 perf fix).
  var FILES = [
    { src: 'noah-ai.js',       attr: 'data-noah-core' },      // Base widget — must load first
    { src: 'noah-voice.js',    attr: 'data-noah-voice' },    // Voice + models — patches noah-ai.js
    { src: 'noah-personas.js',  attr: 'data-noah-personas' }, // Personas + avatars
    { src: 'noah-adaptive.js',  attr: 'data-noah-adaptive' }, // Adaptive learning
    { src: 'il-noah-context.js', attr: 'data-noah-context' } // Page-context awareness (noah-everywhere Phase 1)
  ];

  var loaded = 0;
  var failed = [];

  function loadNext() {
    if (loaded + failed.length >= FILES.length) {
      // All done — signal readiness
      if (typeof window !== 'undefined') {
        window.ILNoahFullLoaded = true;
        window.dispatchEvent(new CustomEvent('noah-full-ready', {
          detail: { loaded: loaded, failed: failed }
        }));
      }
      return;
    }

    var entry = FILES[loaded + failed.length];
    var file = entry.src;
    var script = document.createElement('script');
    script.src = BASE + file;
    script.async = false; // Preserve order
    // Set the guard attribute so noah-ai.js auto-inject skips re-adding us.
    if (entry.attr) script.setAttribute(entry.attr, '1');

    script.onload = function () {
      loaded++;
      loadNext();
    };

    script.onerror = function () {
      failed.push(file);
      if (typeof console !== 'undefined' && console.warn) {
        console.warn('[noah-full] Failed to load: ' + file);
      }
      loadNext();
    };

    document.head.appendChild(script);
  }

  // Start loading when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadNext);
  } else {
    loadNext();
  }
})();
