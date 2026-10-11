/* Interstitium Labs — rAF governor (2026-10-09 perf).
 * Pauses ALL requestAnimationFrame callbacks while the document is hidden
 * (background tab), flushing them on return. Prevents battery drain and
 * main-thread saturation from canvas animations in hidden tabs.
 * Safe: preserves cancelAnimationFrame semantics for queued callbacks. */
(function () {
  'use strict';
  try {
    var origRAF = window.requestAnimationFrame.bind(window);
    var origCAF = window.cancelAnimationFrame.bind(window);
    var queue = [];
    var nextId = 1;
    window.requestAnimationFrame = function (cb) {
      if (typeof cb !== 'function') return origRAF(cb);
      if (document.hidden) {
        var id = nextId++;
        queue.push({ id: id, cb: cb });
        return id;
      }
      return origRAF(cb);
    };
    window.cancelAnimationFrame = function (id) {
      for (var i = 0; i < queue.length; i++) {
        if (queue[i].id === id) { queue.splice(i, 1); return; }
      }
      origCAF(id);
    };
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden && queue.length) {
        var q = queue; queue = [];
        for (var i = 0; i < q.length; i++) { origRAF(q[i].cb); }
      }
    });
  } catch (e) { /* fail-open: leave native rAF untouched */ }
})();

