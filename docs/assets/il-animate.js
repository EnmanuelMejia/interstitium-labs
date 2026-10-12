/* =====================================================================
 * Interstitium Labs — course content animation runtime (il-animate.js)
 *
 * Vanilla JS companion to il-animate.css for the university course shell.
 * No libraries, no scroll listeners — a single shared IntersectionObserver
 * drives scroll reveals; the shell calls into window.ILAnimate at three
 * hook points (tab built, module toggled, readiness ring painted).
 *
 * Public surface (also used by course-shell.js):
 *   ILAnimate.observe(root)            — tag + reveal-gate a tab pane
 *   ILAnimate.moduleToggled(body, open)— replay module-open stagger
 *   ILAnimate.animateRing(host, pct)   — sweep the readiness ring
 *   ILAnimate.staggerWhy(whyEl)        — sentence-stagger a quiz "why"
 *   ILAnimate.stepThrough(container)   — Prev/Next stepper for
 *                                        [data-ila-step] children
 * Honors prefers-reduced-motion: everything resolves to a static,
 * fully-visible state.
 * ===================================================================== */
(function (global) {
  'use strict';

  var doc = global.document;
  var reduced = !!(
    global.matchMedia &&
    global.matchMedia('(prefers-reduced-motion: reduce)').matches
  );
  var canObserve = !reduced && 'IntersectionObserver' in global;
  var io = null;
  var DELAYS = ['0s', '0.07s', '0.14s'];

  function each(list, fn) {
    Array.prototype.forEach.call(list, fn);
  }

  /* ---------- shared reveal observer ---------- */
  function ensureIO() {
    if (io || !canObserve) return io;
    io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var t = en.target;
          io.unobserve(t);
          t.classList.add('ila-in');
          onReveal(t);
        });
      },
      { rootMargin: '0px 0px -6% 0px', threshold: 0.08 }
    );
    return io;
  }

  /* When a revealed subtree contains progress bars, fill them to target. */
  function onReveal(el) {
    each(el.querySelectorAll('.pbar-fill[data-ila-w]'), fillBar);
  }

  function fillBar(bar) {
    if (!bar || bar.getAttribute('data-ila-wdone')) return;
    bar.setAttribute('data-ila-wdone', '1');
    bar.style.width = bar.getAttribute('data-ila-w');
  }

  /* ---------- auto-tag course surfaces ---------- */
  var TAG_SEL = [
    '.hero',
    '.section-title',
    '.section-sub',
    '.cutline',
    '.card',
    '.arc-card',
    '.fold',
    '.quiz',
    '.plan-item',
    '.pbar-row',
    '.ring-card',
    '.noah-panel',
    '.brief-grid > div',
    '.il27-engines > *'
  ].join(',');

  function autoTag(root) {
    if (!root || reduced) return;
    var nodes = root.querySelectorAll(TAG_SEL);
    each(nodes, function (n, i) {
      if (n.getAttribute('data-ila-tagged')) return;
      n.setAttribute('data-ila-tagged', '1');
      /* Module bodies get the open-stagger treatment instead of
       * scroll reveals (avoids double-animating the same content). */
      if (n.closest && n.closest('.mod-body')) return;
      n.classList.add('ila-reveal');
      n.style.setProperty('--ila-d', DELAYS[i % DELAYS.length]);
    });
    /* Progress bars: capture the target width, park at 0, fill on reveal. */
    each(root.querySelectorAll('.pbar-fill'), function (bar) {
      if (bar.getAttribute('data-ila-w')) return;
      if (bar.closest && bar.closest('.mod-body')) return;
      var w = bar.style.width;
      if (w && w !== '0%' && w !== '0px') {
        bar.setAttribute('data-ila-w', w);
        bar.style.width = '0%';
      }
    });
    /* Already-answered quizzes: structure their explanations for stagger. */
    each(root.querySelectorAll('.quiz.answered .why'), staggerWhy);
  }

  function observe(root) {
    if (!root) return;
    autoTag(root);
    var pending = root.querySelectorAll('.ila-reveal:not(.ila-in)');
    if (!canObserve) {
      /* Reduced motion or no IntersectionObserver: everything visible,
       * bars jump straight to target. */
      each(pending, function (n) {
        n.classList.add('ila-in');
      });
      each(root.querySelectorAll('.pbar-fill[data-ila-w]'), function (bar) {
        bar.style.width = bar.getAttribute('data-ila-w');
      });
      return;
    }
    var ob = ensureIO();
    each(pending, function (n) {
      ob.observe(n);
    });
  }

  /* ---------- module expand / collapse ---------- */
  function moduleToggled(body, open) {
    if (!body) return;
    body.classList.remove('ila-opening');
    if (!open || reduced) return;
    /* Force reflow so the stagger keyframes replay on every open. */
    void body.offsetWidth;
    body.classList.add('ila-opening');
  }

  /* ---------- readiness ring sweep ---------- */
  function animateRing(host, pct) {
    if (!host) return;
    var circles = host.querySelectorAll('circle');
    var prog = null;
    each(circles, function (c) {
      if (c.getAttribute('stroke-dasharray')) prog = c;
    });
    if (!prog) return;
    var C = parseFloat(prog.getAttribute('stroke-dasharray')) || 0;
    var prev = parseFloat(host.getAttribute('data-ila-pct') || '0');
    host.setAttribute('data-ila-pct', String(pct));
    if (reduced || !C) return; /* static at the final offset */
    var from = C * (1 - prev / 100);
    var to = C * (1 - pct / 100);
    if (from === to) return;
    try {
      prog.style.transition = 'none';
      prog.style.strokeDashoffset = String(from);
      /* Reflow, then ease to the target (paint-only property). */
      void prog.getBoundingClientRect();
      prog.style.transition =
        'stroke-dashoffset 1.1s cubic-bezier(0.22, 1, 0.36, 1)';
      var apply = function () {
        prog.style.strokeDashoffset = String(to);
      };
      if ('requestAnimationFrame' in global) {
        global.requestAnimationFrame(function () {
          global.requestAnimationFrame(apply);
        });
      } else {
        apply();
      }
    } catch (e) {
      /* Leave the ring static at its final offset. */
    }
  }

  /* ---------- quiz "why": sentence stagger ---------- */
  function staggerWhy(why) {
    if (!why || !doc || why.getAttribute('data-ila-why')) return;
    why.setAttribute('data-ila-why', '1');
    var kids = Array.prototype.slice.call(why.childNodes);
    if (!kids.length) return;
    var label = null;
    var text = '';
    kids.forEach(function (n) {
      if (n.nodeType === 1 && !label) label = n;
      else text += n.textContent;
    });
    kids.forEach(function (n) {
      if (n !== label && n.parentNode) n.parentNode.removeChild(n);
    });
    var parts =
      text.match(/[^.!?…]+[.!?…]+["'”)]?\s*/g) || (text.trim() ? [text] : []);
    var frag = doc.createDocumentFragment();
    parts.forEach(function (p, i) {
      var s = doc.createElement('span');
      s.className = 'ila-why-line';
      s.style.setProperty(
        '--ila-d',
        Math.min(0.1 + i * 0.09, 0.8).toFixed(2) + 's'
      );
      s.textContent = p.trim();
      frag.appendChild(s);
    });
    why.appendChild(frag);
    why.classList.add('ila-why-lines');
  }

  /* Newly-answered quizzes: course-shell's own .opt click handler runs at
   * target phase first and adds .answered; this bubble listener then
   * structures the revealed explanation. */
  function watchQuizAnswers() {
    doc.addEventListener(
      'click',
      function (e) {
        if (reduced) return;
        var t = e.target;
        var quiz = t && t.closest ? t.closest('.quiz') : null;
        if (!quiz || quiz.getAttribute('data-ila-why-watched')) return;
        if (!quiz.classList.contains('answered')) return;
        quiz.setAttribute('data-ila-why-watched', '1');
        staggerWhy(quiz.querySelector('.why'));
      },
      false
    );
  }

  /* ---------- generic step-through ---------- */
  function stepThrough(container) {
    if (!container || !doc) return;
    if (container.getAttribute('data-ila-stepper-done')) return;
    var steps = Array.prototype.slice.call(
      container.querySelectorAll(':scope [data-ila-step]')
    );
    if (steps.length < 2) return;
    container.setAttribute('data-ila-stepper-done', '1');
    container.classList.add('ila-steps');
    var i = 0;

    var nav = doc.createElement('div');
    nav.className = 'ila-steps-nav';
    nav.innerHTML =
      '<button class="btn" type="button" data-sp>← Prev</button>' +
      '<span class="ila-steps-count" data-sc></span>' +
      '<span class="ila-steps-dots" data-sd></span>' +
      '<button class="btn primary" type="button" data-sn>Next →</button>';
    var dots = nav.querySelector('[data-sd]');
    steps.forEach(function () {
      dots.appendChild(doc.createElement('i'));
    });
    container.appendChild(nav);

    function paint(dir) {
      each(steps, function (s, k) {
        s.classList.remove('ila-step', 'ila-step-on', 'ila-step-back');
        if (k === i) {
          s.classList.add('ila-step', 'ila-step-on');
          if (dir < 0) s.classList.add('ila-step-back');
        } else {
          s.classList.add('ila-step');
        }
      });
      nav.querySelector('[data-sc]').textContent =
        'Step ' + (i + 1) + ' / ' + steps.length;
      each(dots.children, function (d, k) {
        d.classList.toggle('on', k === i);
      });
      nav.querySelector('[data-sp]').disabled = i === 0;
      nav.querySelector('[data-sn]').disabled = i === steps.length - 1;
    }
    nav.querySelector('[data-sp]').addEventListener('click', function () {
      if (i > 0) {
        i--;
        paint(-1);
      }
    });
    nav.querySelector('[data-sn]').addEventListener('click', function () {
      if (i < steps.length - 1) {
        i++;
        paint(1);
      }
    });
    container.tabIndex = 0;
    container.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft' && i > 0) {
        i--;
        paint(-1);
      } else if (e.key === 'ArrowRight' && i < steps.length - 1) {
        i++;
        paint(1);
      }
    });
    paint(0);
  }

  function boot() {
    watchQuizAnswers();
    each(doc.querySelectorAll('[data-ila-stepper]'), stepThrough);
  }

  global.ILAnimate = {
    observe: observe,
    moduleToggled: moduleToggled,
    animateRing: animateRing,
    staggerWhy: staggerWhy,
    stepThrough: stepThrough,
    reduced: reduced
  };

  if (doc) {
    if (doc.readyState === 'loading') {
      doc.addEventListener('DOMContentLoaded', boot);
    } else {
      boot();
    }
  }
})(typeof window !== 'undefined' ? window : this);
