/*!
 * IL SPA Navigator (il-spa-nav.js)
 * ---------------------------------------------------------------------------
 * Seamless same-site navigation that keeps the ambient AudioContext (and the
 * floating audio widget) alive across page changes.
 *
 * How it works: internal link clicks are intercepted, the target page is
 * fetched, and the document is swapped via document.open/write/close.
 * The Window (and its JS realm) survives the swap, so:
 *   - ILAmbient's AudioContext keeps rendering — zero audio gap
 *   - The widget / synth / init singletons re-run against the new document
 *     (each is rebuild-aware: engine preserved, widget DOM rebuilt)
 *
 * Scope / safety:
 *   - Same-origin GET navigations only. External links, downloads, file
 *     URLs, mailto/tel/javascript, target=_blank, and [data-no-spa] are
 *     never intercepted — the browser handles those normally.
 *   - /bootcamps/ pages are excluded: the CBT shells manage their own
 *     interactive state and expect full page loads.
 *   - Any fetch/swap failure falls back to a normal hard navigation.
 *   - Back/forward buttons work via popstate + an in-memory page cache.
 *
 * Usage: loaded automatically by il-cinematic-init.js on cinematic pages.
 * No per-page markup needed. Add data-no-spa to any link to opt out.
 */
(function () {
  'use strict';

  // Re-bind per document: document.open/write/close creates a NEW Document
  // object, so listeners attached to the old one are gone. The Window (and
  // this flag's value) survives — re-attach when the document is fresh.
  if (window.__ilSpaNavDoc === document) return;
  window.__ilSpaNavDoc = document;

  var CACHE_MAX = 12;
  var cache = {};
  var cacheOrder = [];
  var scrollMem = {};   // url -> last scrollY (for back/forward restore)
  var navigating = false;

  function cachePut(url, html) {
    if (cache[url]) return;
    cache[url] = html;
    cacheOrder.push(url);
    while (cacheOrder.length > CACHE_MAX) {
      var old = cacheOrder.shift();
      delete cache[old];
    }
  }
  function cacheGet(url) {
    return Object.prototype.hasOwnProperty.call(cache, url) ? cache[url] : null;
  }

  // File types that must always trigger a real browser navigation/download.
  var FILE_EXT = /\.(pdf|zip|gz|tgz|mp4|m4v|webm|mp3|wav|ogg|flac|png|jpe?g|webp|avif|gif|svg|ico|csv|tsv|json|xml|txt|md|epub|dmg|exe|apk)(\?|#|$)/i;

  function shouldHandle(a) {
    if (!a || !a.getAttribute) return false;
    var href = a.getAttribute('href');
    if (!href) return false;
    if (href.charAt(0) === '#') return false;
    if (/^(javascript|mailto|tel|sms):/i.test(href)) return false;
    if (a.target && a.target !== '_self') return false;
    if (a.hasAttribute('download')) return false;
    if (a.hasAttribute('data-no-spa')) return false;
    // Never hijack clicks inside the audio widget.
    if (a.closest && a.closest('#il-audio-widget')) return false;
    var url;
    try { url = new URL(href, location.href); } catch (e) { return false; }
    if (url.origin !== location.origin) return false;
    if (url.protocol !== 'http:' && url.protocol !== 'https:') return false;
    if (FILE_EXT.test(url.pathname)) return false;
    // CBT interactive shells manage their own state — full loads there.
    if (/\/bootcamps\//i.test(url.pathname)) return false;
    // Same-page hash navigation: let the browser do its thing.
    try {
      var cur = new URL(location.href);
      if (url.pathname === cur.pathname && url.search === cur.search) return false;
    } catch (e) {}
    return true;
  }

  /* ---------- tiny top progress bar ---------- */
  var bar = null;
  function showProgress() {
    try {
      if (!bar) {
        bar = document.createElement('div');
        bar.className = 'il-spa-progress';
        bar.setAttribute('aria-hidden', 'true');
        document.body.appendChild(bar);
      }
      bar.style.opacity = '1';
      bar.style.width = '12%';
      // Fake ease toward 80% while fetching; completes on swap.
      setTimeout(function () { if (bar) bar.style.width = '72%'; }, 60);
    } catch (e) {}
  }
  function hideProgress() {
    try {
      if (!bar) return;
      bar.style.width = '100%';
      setTimeout(function () {
        if (!bar) return;
        bar.style.opacity = '0';
        setTimeout(function () {
          if (bar && bar.parentNode) bar.parentNode.removeChild(bar);
          bar = null;
        }, 350);
      }, 120);
    } catch (e) {}
  }

  function fetchPage(url) {
    return fetch(url, { credentials: 'same-origin', headers: { 'X-IL-SPA': '1' } })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        var ct = (r.headers.get('content-type') || '').toLowerCase();
        if (ct.indexOf('text/html') === -1) throw new Error('not html');
        return r.text();
      });
  }

  function swapDocument(html, url, push, restoreScroll) {
    try {
      document.open();
      document.write(html);
      document.close();
    } catch (e) {
      // Catastrophic swap failure — hard navigation as last resort.
      location.href = url;
      return;
    }
    if (push) {
      try { history.pushState({ ilSpa: 1 }, '', url); } catch (e) {}
    }
    // Scroll: new page → top; back/forward → remembered position or hash.
    var done = false;
    try {
      var h = new URL(url).hash;
      if (h) {
        var el = document.getElementById(h.slice(1));
        if (el) { el.scrollIntoView(); done = true; }
      }
      if (!done) {
        if (restoreScroll && typeof scrollMem[url] === 'number') {
          var sy = scrollMem[url];
          requestAnimationFrame(function () { window.scrollTo(0, sy); });
        } else {
          window.scrollTo(0, 0);
        }
      }
    } catch (e) {
      try { window.scrollTo(0, 0); } catch (e2) {}
    }
  }

  function navigate(url, push) {
    if (navigating) return;
    if (url === location.href) return;
    navigating = true;
    scrollMem[location.href] = window.scrollY || 0;
    showProgress();
    var hit = cacheGet(url);
    var p = hit ? Promise.resolve(hit) : fetchPage(url);
    p.then(function (html) {
      cachePut(url, html);
      navigating = false;
      hideProgress();
      swapDocument(html, url, push !== false, false);
    }).catch(function () {
      navigating = false;
      hideProgress();
      location.href = url; // hard fallback
    });
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented) return;
    if (e.button !== 0) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var t = e.target;
    var a = t && t.closest ? t.closest('a') : null;
    if (!a || !shouldHandle(a)) return;
    e.preventDefault();
    var url;
    try { url = new URL(a.getAttribute('href'), location.href).href; }
    catch (e2) { return; }
    navigate(url, true);
  }, true);

  window.addEventListener('popstate', function () {
    var url = location.href;
    showProgress();
    var hit = cacheGet(url);
    var p = hit ? Promise.resolve(hit) : fetchPage(url);
    p.then(function (html) {
      cachePut(url, html);
      hideProgress();
      swapDocument(html, url, false, true);
    }).catch(function () {
      hideProgress();
      location.reload();
    });
  });
})();
