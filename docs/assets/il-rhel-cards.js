/* ============================================================================
   Interstitium Labs — RHEL Card Auto-Enhancer (il-rhel-cards.js)
   Upgrades every .cine-card on the page to the RHEL-reel cinematic standard:
   adds .rhel class, injects circuit pulse, scanlines, and holographic labels.
   Idempotent: safe to run multiple times (guards via data attribute).
   All original work.
   ========================================================================== */
(function () {
  'use strict';

  var HOLO_SETS = [
    ['SYSTEMS', 'red'], ['SECURE', 'blue'], ['DEPLOY', 'blue'],
    ['KERNEL', 'red'], ['MESH', 'blue'], ['FABRIC', 'red'],
    ['NODES', 'blue'], ['SHIELD', 'red'], ['STACK', 'blue'],
    ['CORE', 'red'], ['GRID', 'blue'], ['VAULT', 'red']
  ];

  function pickHolos(seedStr) {
    var h = 0;
    for (var i = 0; i < seedStr.length; i++) h = (h * 31 + seedStr.charCodeAt(i)) >>> 0;
    var out = [];
    for (var k = 0; k < 3; k++) {
      out.push(HOLO_SETS[(h + k * 5) % HOLO_SETS.length]);
    }
    return out;
  }

  function enhance(card) {
    if (card.dataset.rhelEnhanced === '1') return;
    card.dataset.rhelEnhanced = '1';
    card.classList.add('rhel');

    var poster = card.querySelector('.cine-card__poster');
    if (poster) {
      // Circuit pulse sweep
      var pulse = document.createElement('span');
      pulse.className = 'rhel-pulse';
      pulse.setAttribute('aria-hidden', 'true');
      poster.appendChild(pulse);

      // Scanline texture
      var scan = document.createElement('span');
      scan.className = 'rhel-scan';
      scan.setAttribute('aria-hidden', 'true');
      poster.appendChild(scan);

      // Holographic floating labels (seeded by card title for variety)
      var titleEl = card.querySelector('.cine-card__title');
      var seed = titleEl ? titleEl.textContent : card.textContent.slice(0, 40);
      var holos = pickHolos(seed);
      var positions = ['cine-card__holo--1', 'cine-card__holo--2', 'cine-card__holo--3'];
      holos.forEach(function (pair, idx) {
        var holo = document.createElement('span');
        holo.className = 'cine-card__holo ' + positions[idx] + (pair[1] === 'red' ? ' cine-card__holo--red' : '');
        holo.textContent = pair[0];
        holo.setAttribute('aria-hidden', 'true');
        poster.appendChild(holo);
      });
    }
  }

  function enhanceAll(root) {
    var cards = (root || document).querySelectorAll('.cine-card:not([data-rhel-enhanced="1"])');
    for (var i = 0; i < cards.length; i++) enhance(cards[i]);
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { enhanceAll(document); });
  } else {
    enhanceAll(document);
  }

  // Watch for dynamically injected cards (SPA nav, lazy renders)
  if ('MutationObserver' in window) {
    var observer = new MutationObserver(function (mutations) {
      for (var m = 0; m < mutations.length; m++) {
        var added = mutations[m].addedNodes;
        for (var n = 0; n < added.length; n++) {
          var node = added[n];
          if (node.nodeType !== 1) continue;
          if (node.classList && node.classList.contains('cine-card')) {
            enhance(node);
          } else if (node.querySelectorAll) {
            enhanceAll(node);
          }
        }
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }

  // Expose for manual re-run
  window.ILRhelCards = { enhanceAll: enhanceAll, enhance: enhance };
})();

/* ============================================================================
   Cine-card video autoplay (added 2026-10-10)
   IntersectionObserver-driven: plays muted video when card scrolls into view,
   pauses when out. Click toggles sound. Respects prefers-reduced-motion.
   ========================================================================== */
(function () {
  'use strict';
  if (typeof window === 'undefined') return;
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initCardVideos(root) {
    var videos = (root || document).querySelectorAll('video.cine-card__video');
    videos.forEach(function (v) {
      if (v.dataset.ilVideoInit) return;
      v.dataset.ilVideoInit = '1';
      // Click toggles mute
      v.parentElement.style.cursor = 'pointer';
      v.parentElement.addEventListener('click', function (e) {
        if (v.muted) { v.muted = false; v.play().catch(function(){}); }
        else { v.muted = true; }
      });
      if (reduced) return; // no autoplay, click-to-play only
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting) { v.play().catch(function(){}); }
            else { v.pause(); }
          });
        }, { rootMargin: '100px' }).observe(v);
      } else {
        v.play().catch(function(){});
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { initCardVideos(document); });
  } else {
    initCardVideos(document);
  }
  // Handle dynamically added cards
  if ('MutationObserver' in window) {
    new MutationObserver(function (muts) {
      muts.forEach(function (m) {
        m.addedNodes.forEach(function (n) {
          if (n.querySelectorAll) initCardVideos(n);
        });
      });
    }).observe(document.body, { childList: true, subtree: true });
  }
})();
