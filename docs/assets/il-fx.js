/**
 * Interstitium Labs — cinema FX runtime (canvas 2d, no Three.js)
 * Starfield + aurora + parallax · living sigil · command palette · demo mode
 * Page enter · lockup repair · HDR-aware · ultrawide-safe · prefers-reduced-motion
 */
(function (global) {
  "use strict";

  var doc = global.document;
  var reduced =
    global.matchMedia &&
    global.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hdr =
    global.matchMedia &&
    global.matchMedia("(dynamic-range: high)").matches;

  function qs(sel, root) {
    return Array.prototype.slice.call((root || doc).querySelectorAll(sel));
  }

  /* ---------- Lockup / sigil size repair ---------- */
  function repairChrome() {
    qs('header a img[src*="canonical-lockup"], header img[src*="canonical-lockup"]').forEach(function (img) {
      img.classList.add("il-lockup");
      img.removeAttribute("width");
      img.removeAttribute("height");
      img.style.maxHeight = "40px";
      img.style.height = "auto";
      img.style.width = "auto";
      img.style.maxWidth = "min(240px, 58vw)";
      img.style.objectFit = "contain";
      img.style.display = "block";
      var a = img.closest("a");
      if (a) {
        a.style.display = "inline-flex";
        a.style.alignItems = "center";
        a.style.minHeight = "40px";
      }
      // Force decode so 0×0 never sticks
      if (img.decode) {
        img.decode().catch(function () {});
      }
      if (!img.complete || img.naturalWidth === 0) {
        img.addEventListener(
          "load",
          function () {
            img.style.maxHeight = "40px";
            img.style.height = "auto";
            img.style.width = "auto";
          },
          { once: true }
        );
      }
    });
    qs(".il-sigil img, .il-hero-sigil img, .il-emblem img").forEach(function (img) {
      if (!img.getAttribute("width")) img.setAttribute("width", "280");
      if (!img.getAttribute("height")) img.setAttribute("height", "280");
      img.style.width = "100%";
      img.style.height = "auto";
      img.style.minHeight = "80px";
      img.style.display = "block";
    });
  }

  /* ---------- Page enter fade ---------- */
  function pageEnter() {
    doc.documentElement.classList.add("il-fx-ready");
    if (reduced) {
      doc.documentElement.classList.add("il-page-in");
      return;
    }
    requestAnimationFrame(function () {
      doc.documentElement.classList.add("il-page-in");
    });
  }

  /* ---------- Cinema starfield + aurora ---------- */
  function initCinemaField(host) {
    if (!host || host.getAttribute("data-il-fx-field")) return null;
    host.setAttribute("data-il-fx-field", "1");
    host.setAttribute("data-il-starfield-ready", "1");
    host.classList.add("il-hero-field", "il-fx-field");

    // CSS aurora layers (visible even if canvas skipped)
    if (!host.querySelector(".il-aurora")) {
      var aurora = doc.createElement("div");
      aurora.className = "il-aurora";
      aurora.setAttribute("aria-hidden", "true");
      aurora.innerHTML =
        '<span class="il-aurora-a"></span><span class="il-aurora-b"></span><span class="il-aurora-c"></span><span class="il-nebula"></span>';
      host.appendChild(aurora);
    }

    if (reduced) return { start: function () {}, stop: function () {} };

    var canvas = host.querySelector("canvas.il-fx-canvas");
    if (!canvas) {
      // replace any prior plain canvas from il-motion
      var old = host.querySelector("canvas");
      if (old) old.remove();
      canvas = doc.createElement("canvas");
      canvas.className = "il-fx-canvas";
      canvas.setAttribute("aria-hidden", "true");
      host.appendChild(canvas);
    }
    var ctx = canvas.getContext("2d", { alpha: true });
    var stars = [];
    var meteors = [];
    var raf = 0;
    var running = false;
    var w = 0;
    var h = 0;
    var dpr = Math.min(global.devicePixelRatio || 1, 2);
    var mx = 0.5;
    var my = 0.5;
    var t0 = performance.now();
    var glowMul = hdr ? 1.55 : 1;

    function resize() {
      var rect = host.getBoundingClientRect();
      w = Math.max(1, Math.floor(rect.width));
      h = Math.max(1, Math.floor(rect.height));
      // Ultrawide: cap work, still fill
      if (w > 3840) dpr = Math.min(dpr, 1.5);
      if (w > 5000) dpr = 1;
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var area = w * h;
      var count = Math.min(220, Math.max(70, Math.floor(area / 11000)));
      if (w > 3840) count = Math.min(count, 160);
      stars = [];
      for (var i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * w,
          y: Math.random() * h,
          z: 0.15 + Math.random() * 0.85,
          r: 0.5 + Math.random() * 1.8,
          tw: Math.random() * Math.PI * 2,
          sp: 0.12 + Math.random() * 0.45,
          kind: Math.random() < 0.12 ? 1 : 0, // gold
        });
      }
      meteors = [];
    }

    function spawnMeteor() {
      if (meteors.length > 2) return;
      meteors.push({
        x: Math.random() * w * 0.9,
        y: -20,
        vx: 2.2 + Math.random() * 3.5,
        vy: 3.5 + Math.random() * 4.5,
        life: 1,
        len: 40 + Math.random() * 70,
      });
    }

    function frame(now) {
      if (!running) return;
      var t = (now - t0) / 1000;
      ctx.clearRect(0, 0, w, h);

      // Parallax nebula wash (canvas)
      var px = (mx - 0.5) * 36;
      var py = (my - 0.5) * 24;
      var g1 = ctx.createRadialGradient(
        w * 0.72 + px,
        h * 0.28 + py,
        0,
        w * 0.72 + px,
        h * 0.28 + py,
        Math.max(w, h) * 0.55
      );
      g1.addColorStop(0, "rgba(94,234,212," + (0.14 * glowMul).toFixed(3) + ")");
      g1.addColorStop(0.45, "rgba(56,189,248," + (0.06 * glowMul).toFixed(3) + ")");
      g1.addColorStop(1, "rgba(7,11,22,0)");
      ctx.fillStyle = g1;
      ctx.fillRect(0, 0, w, h);

      var g2 = ctx.createRadialGradient(
        w * 0.22 - px * 0.6,
        h * 0.75 - py * 0.5,
        0,
        w * 0.22,
        h * 0.75,
        Math.max(w, h) * 0.4
      );
      g2.addColorStop(0, "rgba(201,162,39," + (0.1 * glowMul).toFixed(3) + ")");
      g2.addColorStop(1, "rgba(7,11,22,0)");
      ctx.fillStyle = g2;
      ctx.fillRect(0, 0, w, h);

      // Aurora ribbons
      ctx.save();
      ctx.globalCompositeOperation = "lighter";
      for (var band = 0; band < 3; band++) {
        var baseY = h * (0.25 + band * 0.18);
        ctx.beginPath();
        for (var x = 0; x <= w; x += 8) {
          var y =
            baseY +
            Math.sin(x * 0.0035 + t * (0.55 + band * 0.15) + band) * (28 + band * 12) +
            Math.sin(x * 0.0012 - t * 0.3) * 18 +
            py * (0.3 + band * 0.1);
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.strokeStyle =
          band === 1
            ? "rgba(201,162,39," + (0.18 * glowMul).toFixed(3) + ")"
            : "rgba(94,234,212," + ((0.22 - band * 0.04) * glowMul).toFixed(3) + ")";
        ctx.lineWidth = 2.5 + band;
        ctx.stroke();
      }
      ctx.restore();

      // Stars
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        var parallax = (s.z - 0.5) * 18;
        s.tw += 0.025 * s.sp;
        s.y += 0.06 * s.z;
        if (s.y > h + 4) {
          s.y = -4;
          s.x = Math.random() * w;
        }
        var a = (0.35 + 0.65 * (0.5 + 0.5 * Math.sin(s.tw))) * s.z * glowMul;
        a = Math.min(1, a);
        var col = s.kind ? "201,162,39" : "94,234,212";
        var sx = s.x + px * s.z * 0.4 + parallax * (mx - 0.5);
        var sy = s.y + py * s.z * 0.3;
        ctx.beginPath();
        ctx.fillStyle = "rgba(" + col + "," + a.toFixed(3) + ")";
        ctx.arc(sx, sy, s.r * s.z, 0, Math.PI * 2);
        ctx.fill();
        if (s.r > 1.2 && a > 0.55) {
          ctx.beginPath();
          ctx.fillStyle = "rgba(" + col + "," + (a * 0.25).toFixed(3) + ")";
          ctx.arc(sx, sy, s.r * s.z * 3.2, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // Meteors
      if (Math.random() < 0.008) spawnMeteor();
      for (var m = meteors.length - 1; m >= 0; m--) {
        var met = meteors[m];
        met.x += met.vx;
        met.y += met.vy;
        met.life -= 0.016;
        if (met.life <= 0 || met.y > h + 40) {
          meteors.splice(m, 1);
          continue;
        }
        var grad = ctx.createLinearGradient(
          met.x,
          met.y,
          met.x - met.vx * (met.len / 8),
          met.y - met.vy * (met.len / 8)
        );
        grad.addColorStop(0, "rgba(232,238,245," + (0.9 * met.life).toFixed(3) + ")");
        grad.addColorStop(1, "rgba(94,234,212,0)");
        ctx.strokeStyle = grad;
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.moveTo(met.x, met.y);
        ctx.lineTo(met.x - met.vx * (met.len / 8), met.y - met.vy * (met.len / 8));
        ctx.stroke();
      }

      raf = requestAnimationFrame(frame);
    }

    function onPointer(e) {
      var r = host.getBoundingClientRect();
      if (!r.width || !r.height) return;
      mx = (e.clientX - r.left) / r.width;
      my = (e.clientY - r.top) / r.height;
    }

    function start() {
      if (running || reduced) return;
      if (doc.visibilityState === "hidden") return;
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
    if ("ResizeObserver" in global) {
      new ResizeObserver(resize).observe(host);
    } else {
      global.addEventListener("resize", resize);
    }
    global.addEventListener("pointermove", onPointer, { passive: true });
    doc.addEventListener("visibilitychange", function () {
      if (doc.visibilityState === "hidden") stop();
      else start();
    });
    return { start: start, stop: stop, resize: resize };
  }

  function ensureHeroHosts() {
    var existing = qs("[data-il-starfield], .il-hero-field");
    if (existing.length) {
      existing.forEach(initCinemaField);
      return;
    }
    // Auto-mount under first main section / hero
    var section =
      doc.querySelector("main > section:first-of-type") ||
      doc.querySelector(".flex-1 > section:first-of-type") ||
      doc.querySelector("section.relative");
    if (!section) return;
    var cs = global.getComputedStyle(section);
    if (cs.position === "static") section.style.position = "relative";
    section.classList.add("overflow-hidden");
    var host = doc.createElement("div");
    host.className = "il-hero-field";
    host.setAttribute("data-il-starfield", "");
    host.setAttribute("aria-hidden", "true");
    section.insertBefore(host, section.firstChild);
    initCinemaField(host);
  }

  /* ---------- Living sigil ---------- */
  function initSigils() {
    qs(".il-sigil, .il-hero-sigil, .il-emblem").forEach(function (el) {
      if (el.getAttribute("data-il-fx-sigil")) return;
      el.setAttribute("data-il-fx-sigil", "1");
      el.classList.add("il-sigil", "il-sigil--live");
      if (!el.className.match(/il-sigil--float|il-sigil--spin/)) {
        el.classList.add("il-sigil--float", "il-sigil-glow");
      }
      if (reduced) return;
      el.addEventListener("pointerenter", function () {
        el.classList.add("is-hot");
      });
      el.addEventListener("pointerleave", function () {
        el.classList.remove("is-hot");
      });
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var x = ((e.clientX - r.left) / r.width - 0.5) * 12;
        var y = ((e.clientY - r.top) / r.height - 0.5) * 12;
        el.style.setAttribute && el.style.setProperty("--sx", x.toFixed(2) + "px");
        el.style.setProperty("--sy", y.toFixed(2) + "px");
      });
    });
  }

  /* ---------- Scroll cinema (boost motion auto-tag) ---------- */
  function boostReveal() {
    qs(
      "main .rounded-xl, main .il-surface, .il-diff-strip .rounded-xl, [data-il-auto-reveal] .rounded-xl, section .grid > a, section .grid > div.rounded-xl, section .grid > article"
    ).forEach(function (el, i) {
      if (el.closest("header, footer, nav, .il-hud, .il-cmd")) return;
      if (!el.classList.contains("il-reveal")) el.classList.add("il-reveal");
      if (!el.className.match(/il-reveal-delay/)) {
        el.classList.add("il-reveal-delay-" + ((i % 4) + 1));
      }
    });
    if (global.ILMotion && typeof global.ILMotion.initReveal === "function") {
      global.ILMotion.initReveal(doc);
    } else if (!reduced && "IntersectionObserver" in global) {
      var nodes = qs(".il-reveal:not(.is-in)");
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (en) {
            if (!en.isIntersecting) return;
            en.target.classList.add("is-in");
            io.unobserve(en.target);
          });
        },
        { rootMargin: "0px 0px -6% 0px", threshold: 0.1 }
      );
      nodes.forEach(function (n) {
        io.observe(n);
      });
    } else {
      qs(".il-reveal").forEach(function (n) {
        n.classList.add("is-in");
      });
    }
  }

  /* ---------- Magnetic CTAs ---------- */
  function boostMagnetic() {
    qs('a.bg-paper, a[class*="bg-paper"], button.bg-paper, .il-magnetic').forEach(function (el) {
      el.classList.add("il-magnetic", "il-press");
      if (!el.getAttribute("data-il-magnetic")) el.setAttribute("data-il-magnetic", "10");
    });
    if (global.ILMotion && global.ILMotion.initMagnetic) global.ILMotion.initMagnetic(doc);
  }

  /* ---------- Command palette ---------- */
  var ROUTES = [
    { k: "Home", h: "/", g: "Navigate" },
    { k: "Learning OS", h: "/learn/", g: "Navigate" },
    { k: "Adaptive OS", h: "/adapt/", g: "Navigate" },
    { k: "Founders / Student Zero", h: "/founders/", g: "Navigate" },
    { k: "Interview Prep", h: "/prep/", g: "Navigate" },
    { k: "Paths / Curriculum", h: "/paths/", g: "Navigate" },
    { k: "Labs hub", h: "/labs/", g: "Navigate" },
    { k: "DevOps SuperLab", h: "/labs/superlab/", g: "Navigate" },
    { k: "Coach", h: "/coach/", g: "Navigate" },
    { k: "Play / Quests", h: "/play/", g: "Navigate" },
    { k: "Enroll", h: "/enroll/", g: "Navigate" },
    { k: "About", h: "/about/", g: "Navigate" },
    { k: "Skills map", h: "/learn/skills/", g: "Navigate" },
    { k: "Run demo mode", h: "#demo", g: "FX", action: "demo" },
    { k: "Award +25 XP", h: "#xp", g: "FX", action: "xp" },
    { k: "Celebrate level-up", h: "#lvl", g: "FX", action: "level" },
  ];

  function ensureCmdStyles() {
    if (doc.getElementById("il-fx-cmd-css")) return;
    var s = doc.createElement("style");
    s.id = "il-fx-cmd-css";
    s.textContent =
      ".il-cmd{position:fixed;inset:0;z-index:80;display:none;align-items:flex-start;justify-content:center;padding:12vh 1rem 2rem;background:rgba(7,11,22,.72);backdrop-filter:blur(10px)}" +
      ".il-cmd.is-open{display:flex}" +
      ".il-cmd-panel{width:min(560px,100%);border-radius:1rem;background:#0c1222;border:1px solid rgba(94,234,212,.25);box-shadow:0 0 0 1px rgba(201,162,39,.12),0 24px 80px rgba(0,0,0,.55);overflow:hidden}" +
      ".il-cmd input{width:100%;background:transparent;border:0;border-bottom:1px solid rgba(232,238,245,.08);padding:1rem 1.1rem;color:#e8eef5;font:500 1rem Space Grotesk,Inter,system-ui,sans-serif;outline:none}" +
      ".il-cmd ul{list-style:none;margin:0;padding:.4rem;max-height:min(50vh,360px);overflow:auto}" +
      ".il-cmd li button{width:100%;text-align:left;display:flex;justify-content:space-between;gap:1rem;padding:.7rem .85rem;border-radius:.65rem;border:0;background:transparent;color:#e8eef5;font:500 .9rem Space Grotesk,Inter,system-ui,sans-serif;cursor:pointer}" +
      ".il-cmd li button:hover,.il-cmd li.is-active button{background:rgba(94,234,212,.1)}" +
      ".il-cmd .g{font:500 .62rem JetBrains Mono,monospace;letter-spacing:.14em;text-transform:uppercase;color:#c9a227}" +
      ".il-cmd-hint{padding:.55rem 1rem .8rem;font:500 .58rem JetBrains Mono,monospace;letter-spacing:.16em;text-transform:uppercase;color:#8b9bb4}";
    doc.head.appendChild(s);
  }

  function runAction(item) {
    if (item.action === "demo") {
      runDemo();
      return;
    }
    if (item.action === "xp") {
      if (global.ILGame && global.ILGame.award) global.ILGame.award("demo_xp", 25, { label: "Command XP" });
      return;
    }
    if (item.action === "level") {
      if (global.ILGame) {
        if (global.ILGame.celebrate) global.ILGame.celebrate();
        else if (global.ILGame.confetti) global.ILGame.confetti();
        global.ILGame.award("demo_level", 120, { label: "Demo level" });
      }
      return;
    }
    if (item.h && item.h.charAt(0) !== "#") global.location.href = item.h;
  }

  function mountCommandPalette() {
    ensureCmdStyles();
    if (doc.getElementById("il-cmd")) return;
    var root = doc.createElement("div");
    root.id = "il-cmd";
    root.className = "il-cmd";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-label", "Command palette");
    root.innerHTML =
      '<div class="il-cmd-panel">' +
      '<input type="search" placeholder="Jump anywhere… (demo, learn, prep)" aria-label="Command search" autocomplete="off"/>' +
      "<ul></ul>" +
      '<div class="il-cmd-hint">⌘K / Ctrl+K · Esc to close · Demo mode included</div>' +
      "</div>";
    doc.body.appendChild(root);
    var input = root.querySelector("input");
    var list = root.querySelector("ul");
    var active = 0;
    var filtered = ROUTES.slice();

    function paint() {
      list.innerHTML = filtered
        .map(function (r, i) {
          return (
            '<li class="' +
            (i === active ? "is-active" : "") +
            '"><button type="button" data-i="' +
            i +
            '"><span>' +
            r.k +
            '</span><span class="g">' +
            r.g +
            "</span></button></li>"
          );
        })
        .join("");
    }

    function open() {
      root.classList.add("is-open");
      input.value = "";
      filtered = ROUTES.slice();
      active = 0;
      paint();
      setTimeout(function () {
        input.focus();
      }, 10);
    }
    function close() {
      root.classList.remove("is-open");
    }

    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      filtered = ROUTES.filter(function (r) {
        return !q || r.k.toLowerCase().indexOf(q) >= 0 || r.g.toLowerCase().indexOf(q) >= 0;
      });
      active = 0;
      paint();
    });
    list.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-i]");
      if (!btn) return;
      var item = filtered[+btn.getAttribute("data-i")];
      close();
      if (item) runAction(item);
    });
    root.addEventListener("click", function (e) {
      if (e.target === root) close();
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        active = Math.min(filtered.length - 1, active + 1);
        paint();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        active = Math.max(0, active - 1);
        paint();
      } else if (e.key === "Enter") {
        e.preventDefault();
        var item = filtered[active];
        close();
        if (item) runAction(item);
      } else if (e.key === "Escape") {
        close();
      }
    });
    doc.addEventListener("keydown", function (e) {
      if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) {
        e.preventDefault();
        if (root.classList.contains("is-open")) close();
        else open();
      } else if (e.key === "Escape" && root.classList.contains("is-open")) {
        close();
      }
    });
    global.ILFX = global.ILFX || {};
    global.ILFX.openCommand = open;
    global.ILFX.closeCommand = close;
  }

  /* ---------- Demo mode (3-second wow) ---------- */
  function runDemo() {
    doc.documentElement.classList.add("il-demo");
    // Burst pointer parallax center-sweep
    qs(".il-fx-field").forEach(function (host) {
      host.classList.add("il-fx-demo-burst");
      setTimeout(function () {
        host.classList.remove("il-fx-demo-burst");
      }, 2800);
    });
    qs(".il-sigil--live").forEach(function (el) {
      el.classList.add("is-hot");
      setTimeout(function () {
        el.classList.remove("is-hot");
      }, 3000);
    });
    if (global.ILGame) {
      if (global.ILGame.award) global.ILGame.award("demo_mode", 40, { label: "Demo mode" });
      setTimeout(function () {
        if (global.ILGame.award) global.ILGame.award("demo_mode_2", 80, { label: "Demo surge" });
        if (global.ILGame.confetti) global.ILGame.confetti();
        else if (global.ILGame.celebrate) global.ILGame.celebrate();
      }, 900);
    }
    var toast = doc.createElement("div");
    toast.className = "il-fx-toast";
    toast.textContent = "DEMO MODE · cinema FX live · ⌘K for command palette";
    doc.body.appendChild(toast);
    setTimeout(function () {
      toast.classList.add("is-out");
      setTimeout(function () {
        toast.remove();
      }, 400);
    }, 2600);
  }

  function maybeAutoDemo() {
    try {
      if (reduced) return;
      if (global.sessionStorage.getItem("il.fx.demo") === "1") return;
      var params = new URLSearchParams(global.location.search);
      if (params.get("demo") === "1" || params.get("fx") === "demo") {
        global.sessionStorage.setItem("il.fx.demo", "1");
        setTimeout(runDemo, 600);
        return;
      }
      // First visit this session: subtle auto-wow once on home/learn
      var path = global.location.pathname || "/";
      if ((path === "/" || path.indexOf("/learn") === 0) && !global.sessionStorage.getItem("il.fx.seen")) {
        global.sessionStorage.setItem("il.fx.seen", "1");
        setTimeout(function () {
          doc.documentElement.classList.add("il-fx-wow");
          setTimeout(function () {
            doc.documentElement.classList.remove("il-fx-wow");
          }, 3200);
        }, 200);
      }
    } catch (e) {}
  }

  /* ---------- Game chip pulse hook ---------- */
  function wireGameChips() {
    doc.addEventListener("il:game", function (ev) {
      var d = (ev && ev.detail) || {};
      qs("[data-il-game-xp], [data-il-game-level], [data-il-game-streak], #il-game-hud").forEach(function (el) {
        el.classList.add("il-chip-pulse");
        setTimeout(function () {
          el.classList.remove("il-chip-pulse");
        }, 420);
      });
      if (d.leveled || d.type === "level_up") {
        doc.documentElement.classList.add("il-level-flash");
        setTimeout(function () {
          doc.documentElement.classList.remove("il-level-flash");
        }, 900);
      }
    });
  }

  /* ---------- Soften hero plate that buried prior FX ---------- */
  function liftHeroStack() {
    qs("section:has(.il-hero-field), section.relative.isolate").forEach(function (sec) {
      qs(":scope > .pointer-events-none.absolute.inset-0", sec).forEach(function (plate) {
        plate.classList.add("il-hero-plate");
      });
    });
    // Fallback without :has support — previous sibling of content after field
    qs(".il-hero-field").forEach(function (field) {
      var n = field.nextElementSibling;
      while (n) {
        if (n.classList && n.classList.contains("pointer-events-none") && n.classList.contains("absolute")) {
          n.classList.add("il-hero-plate");
          break;
        }
        n = n.nextElementSibling;
      }
    });
  }

  function boot() {
    repairChrome();
    pageEnter();
    liftHeroStack();
    ensureHeroHosts();
    initSigils();
    boostReveal();
    boostMagnetic();
    mountCommandPalette();
    wireGameChips();
    maybeAutoDemo();
    // Re-repair after late layout / SPA chrome
    setTimeout(repairChrome, 400);
    setTimeout(repairChrome, 1200);
  }

  global.ILFX = {
    boot: boot,
    runDemo: runDemo,
    initCinemaField: initCinemaField,
    reduced: reduced,
    hdr: hdr,
  };

  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", boot);
  else boot();
})(typeof window !== "undefined" ? window : this);
