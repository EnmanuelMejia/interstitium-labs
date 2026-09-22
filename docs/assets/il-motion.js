/**
 * Interstitium Labs — motion runtime (vanilla).
 * Scroll reveal · starfield · magnetic buttons · counters · sigil helpers
 * Respects prefers-reduced-motion and document.visibilityState
 */
(function (global) {
  "use strict";

  var reduced =
    global.matchMedia &&
    global.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function qs(sel, root) {
    return (root || global.document).querySelectorAll(sel);
  }

  /* ---------- Scroll reveal ---------- */
  function initReveal(root) {
    var nodes = qs(".il-reveal, [data-il-reveal]", root);
    if (!nodes.length) return;
    if (reduced || !("IntersectionObserver" in global)) {
      nodes.forEach(function (n) {
        n.classList.add("is-in");
      });
      return;
    }
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          en.target.classList.add("is-in");
          io.unobserve(en.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
    );
    nodes.forEach(function (n, i) {
      if (!n.classList.contains("il-reveal")) n.classList.add("il-reveal");
      if (!n.className.match(/il-reveal-delay/)) {
        var d = n.getAttribute("data-il-reveal-delay");
        if (d) n.classList.add("il-reveal-delay-" + d);
        else if (i % 4 === 1) n.classList.add("il-reveal-delay-1");
        else if (i % 4 === 2) n.classList.add("il-reveal-delay-2");
        else if (i % 4 === 3) n.classList.add("il-reveal-delay-3");
      }
      io.observe(n);
    });
  }

  /* ---------- Starfield / particle canvas ---------- */
  function initStarfield(host) {
    if (!host || reduced) return null;
    var canvas = host.querySelector("canvas");
    if (!canvas) {
      canvas = global.document.createElement("canvas");
      host.appendChild(canvas);
    }
    var ctx = canvas.getContext("2d", { alpha: true });
    var stars = [];
    var raf = 0;
    var running = false;
    var w = 0;
    var h = 0;
    var dpr = Math.min(global.devicePixelRatio || 1, 2);

    function resize() {
      var rect = host.getBoundingClientRect();
      w = Math.max(1, Math.floor(rect.width));
      h = Math.max(1, Math.floor(rect.height));
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var count = Math.min(140, Math.max(40, Math.floor((w * h) / 14000)));
      stars = [];
      for (var i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * w,
          y: Math.random() * h,
          z: 0.2 + Math.random() * 0.8,
          r: 0.4 + Math.random() * 1.4,
          tw: Math.random() * Math.PI * 2,
          sp: 0.15 + Math.random() * 0.35,
        });
      }
    }

    function frame(t) {
      if (!running) return;
      ctx.clearRect(0, 0, w, h);
      var cyan = "94,234,212";
      var gold = "201,162,39";
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        s.tw += 0.02 * s.sp;
        s.y += 0.08 * s.z;
        if (s.y > h + 2) {
          s.y = -2;
          s.x = Math.random() * w;
        }
        var a = 0.25 + 0.55 * (0.5 + 0.5 * Math.sin(s.tw));
        var col = i % 5 === 0 ? gold : cyan;
        ctx.beginPath();
        ctx.fillStyle = "rgba(" + col + "," + a * s.z + ")";
        ctx.arc(s.x, s.y, s.r * s.z, 0, Math.PI * 2);
        ctx.fill();
      }
      // soft vignette nucleus
      var g = ctx.createRadialGradient(
        w * 0.7,
        h * 0.35,
        0,
        w * 0.7,
        h * 0.35,
        Math.max(w, h) * 0.45
      );
      g.addColorStop(0, "rgba(94,234,212,0.04)");
      g.addColorStop(1, "rgba(7,11,22,0)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, w, h);
      raf = requestAnimationFrame(frame);
    }

    function start() {
      if (running || reduced) return;
      if (global.document.visibilityState === "hidden") return;
      running = true;
      raf = requestAnimationFrame(frame);
    }
    function stop() {
      running = false;
      if (raf) cancelAnimationFrame(raf);
      raf = 0;
    }

    resize();
    start();

    var ro =
      "ResizeObserver" in global
        ? new ResizeObserver(function () {
            resize();
          })
        : null;
    if (ro) ro.observe(host);
    else global.addEventListener("resize", resize);

    global.document.addEventListener("visibilitychange", function () {
      if (global.document.visibilityState === "hidden") stop();
      else start();
    });

    return { start: start, stop: stop, resize: resize };
  }

  function initAllStarfields(root) {
    qs("[data-il-starfield], .il-hero-field", root).forEach(function (host) {
      if (host.getAttribute("data-il-starfield-ready")) return;
      host.setAttribute("data-il-starfield-ready", "1");
      host.classList.add("il-hero-field");
      initStarfield(host);
    });
  }

  /* ---------- Magnetic buttons ---------- */
  function initMagnetic(root) {
    if (reduced) return;
    var nodes = qs(".il-magnetic, [data-il-magnetic]", root);
    nodes.forEach(function (el) {
      if (el.getAttribute("data-il-mag-ready")) return;
      el.setAttribute("data-il-mag-ready", "1");
      el.classList.add("il-magnetic");
      var strength = parseFloat(el.getAttribute("data-il-magnetic") || "10") || 10;
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var x = ((e.clientX - r.left) / r.width - 0.5) * strength;
        var y = ((e.clientY - r.top) / r.height - 0.5) * strength;
        el.style.setProperty("--mx", x.toFixed(2) + "px");
        el.style.setProperty("--my", y.toFixed(2) + "px");
      });
      el.addEventListener("pointerleave", function () {
        el.style.setProperty("--mx", "0px");
        el.style.setProperty("--my", "0px");
      });
    });
  }

  /* ---------- Number counters ---------- */
  function parseNum(text) {
    var t = String(text).replace(/,/g, "").trim();
    var n = parseFloat(t);
    return isNaN(n) ? null : n;
  }

  function formatNum(n, original) {
    if (original.indexOf(",") >= 0) {
      return Math.round(n).toLocaleString("en-US");
    }
    if (original.indexOf(".") >= 0) return n.toFixed(1);
    return String(Math.round(n));
  }

  function animateCount(el) {
    var targetAttr = el.getAttribute("data-il-count");
    var original = (targetAttr != null ? targetAttr : el.textContent).trim();
    var target = parseNum(original);
    if (target == null) return;
    if (reduced) {
      el.textContent = formatNum(target, original);
      return;
    }
    var dur = 1100;
    var start = performance.now();
    function tick(now) {
      var p = Math.min(1, (now - start) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = formatNum(target * eased, original);
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = formatNum(target, original);
    }
    requestAnimationFrame(tick);
  }

  function initCounters(root) {
    var nodes = qs("[data-il-count], .il-stat-num", root);
    if (!nodes.length) return;
    if (reduced) {
      nodes.forEach(function (n) {
        if (n.hasAttribute("data-il-count"))
          n.textContent = n.getAttribute("data-il-count");
      });
      return;
    }
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          if (en.target.getAttribute("data-il-counted")) return;
          en.target.setAttribute("data-il-counted", "1");
          animateCount(en.target);
          io.unobserve(en.target);
        });
      },
      { threshold: 0.4 }
    );
    nodes.forEach(function (n) {
      n.classList.add("il-stat-num");
      io.observe(n);
    });
  }

  /* ---------- Auto-tag common surfaces ---------- */
  function autoTag(root) {
    // Stats grid numbers on home
    qs("section .font-display.text-3xl, section .font-display.text-4xl", root).forEach(
      function (el) {
        if (el.closest("h1,h2,h3")) return;
        var t = el.textContent.trim();
        if (/^[\d,]+$/.test(t) && !el.hasAttribute("data-il-count")) {
          el.setAttribute("data-il-count", t);
          el.classList.add("il-stat-num");
        }
      }
    );
    // Cards as reveal
    qs(
      "#why-interstitium .rounded-xl, .il-diff-strip .rounded-xl, [data-il-auto-reveal] .rounded-xl, [data-il-auto-reveal] .il-surface",
      root
    ).forEach(function (el) {
      if (!el.classList.contains("il-reveal")) el.classList.add("il-reveal");
    });
    // Primary CTAs
    qs(
      'a.bg-paper, button.bg-paper, a[class*="bg-paper"]',
      root
    ).forEach(function (el) {
      if (!el.classList.contains("il-magnetic")) {
        el.classList.add("il-magnetic");
        el.setAttribute("data-il-magnetic", "8");
      }
      el.classList.add("il-press");
    });
  }

  function boot() {
    var root = global.document;
    autoTag(root);
    initReveal(root);
    initAllStarfields(root);
    initMagnetic(root);
    initCounters(root);
  }

  global.ILMotion = {
    initReveal: initReveal,
    initStarfield: initStarfield,
    initMagnetic: initMagnetic,
    initCounters: initCounters,
    boot: boot,
    reduced: reduced,
  };

  if (global.document && global.document.readyState === "loading") {
    global.document.addEventListener("DOMContentLoaded", boot);
  } else if (global.document) {
    boot();
  }
})(typeof window !== "undefined" ? window : this);
