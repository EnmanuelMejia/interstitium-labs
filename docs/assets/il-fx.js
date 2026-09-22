/**
 * Interstitium Labs — Musk-bar FX runtime
 * Full-viewport starfield + cyan/gold aurora · sigil tilt · ⌘K palette ·
 * Demo mode · optional sound (OFF) · Adaptive mini CAT · level haptic pulse
 * DPR capped · pauses when hidden/offscreen · reduced-motion → static gradient
 */
(function (global) {
  "use strict";

  var doc = global.document;
  var reduced =
    global.matchMedia &&
    global.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var DPR_CAP = 1.5;
  var SOUND_KEY = "il.sound";
  var soundOn = false;
  try {
    soundOn = global.localStorage.getItem(SOUND_KEY) === "1";
  } catch (e0) {}
  var audioCtx = null;
  var unlocked = false;

  function dpr() {
    return Math.min(global.devicePixelRatio || 1, DPR_CAP);
  }

  function qs(sel, root) {
    return (root || doc).querySelector(sel);
  }
  function qsa(sel, root) {
    return Array.prototype.slice.call((root || doc).querySelectorAll(sel));
  }

  /* ---------- Optional UI blip (gesture-gated, OFF by default) ---------- */
  function ensureAudio() {
    if (!soundOn) return null;
    if (!audioCtx) {
      var AC = global.AudioContext || global.webkitAudioContext;
      if (!AC) return null;
      audioCtx = new AC();
    }
    if (audioCtx.state === "suspended") {
      audioCtx.resume().catch(function () {});
    }
    unlocked = true;
    return audioCtx;
  }

  function blip(kind) {
    if (!soundOn || !unlocked) return;
    var ctx = ensureAudio();
    if (!ctx) return;
    try {
      var o = ctx.createOscillator();
      var g = ctx.createGain();
      o.type = "sine";
      var now = ctx.currentTime;
      var f0 = kind === "level" ? 520 : kind === "ok" ? 440 : 280;
      o.frequency.setValueAtTime(f0, now);
      o.frequency.exponentialRampToValueAtTime(f0 * 1.35, now + 0.08);
      g.gain.setValueAtTime(0.0001, now);
      g.gain.exponentialRampToValueAtTime(0.045, now + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, now + 0.14);
      o.connect(g);
      g.connect(ctx.destination);
      o.start(now);
      o.stop(now + 0.16);
    } catch (e1) {}
  }

  function unlockSoundOnce() {
    if (!soundOn) return;
    ensureAudio();
  }

  /* ---------- Full-viewport aurora + starfield ---------- */
  function ensureFxRoot() {
    var root = qs("#il-fx-root");
    if (root) return root;
    root = doc.createElement("div");
    root.id = "il-fx-root";
    root.className = "il-fx-root";
    root.setAttribute("aria-hidden", "true");
    if (doc.body.firstChild) doc.body.insertBefore(root, doc.body.firstChild);
    else doc.body.appendChild(root);
    return root;
  }

  function initAurora() {
    var root = ensureFxRoot();
    if (reduced) {
      root.classList.add("is-static");
      return null;
    }
    var canvas = root.querySelector("canvas");
    if (!canvas) {
      canvas = doc.createElement("canvas");
      root.appendChild(canvas);
    }
    var ctx = canvas.getContext("2d", { alpha: true });
    var stars = [];
    var bands = [];
    var raf = 0;
    var running = false;
    var w = 0;
    var h = 0;
    var t0 = performance.now();

    function rebuild() {
      w = Math.max(1, global.innerWidth || doc.documentElement.clientWidth);
      h = Math.max(1, global.innerHeight || doc.documentElement.clientHeight);
      var r = dpr();
      canvas.width = Math.floor(w * r);
      canvas.height = Math.floor(h * r);
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      ctx.setTransform(r, 0, 0, r, 0, 0);
      var area = w * h;
      var count = Math.min(140, Math.max(48, Math.floor(area / 28000)));
      // Cap particle load on ultrawide 5k
      if (w >= 3840) count = Math.min(count, 110);
      stars = [];
      for (var i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * w,
          y: Math.random() * h,
          z: 0.25 + Math.random() * 0.85,
          r: 0.45 + Math.random() * 1.7,
          tw: Math.random() * Math.PI * 2,
          sp: 0.2 + Math.random() * 0.55,
          gold: i % 6 === 0,
        });
      }
      bands = [
        { y: h * 0.22, amp: h * 0.08, hue: "cyan", phase: 0.2, thick: h * 0.18 },
        { y: h * 0.55, amp: h * 0.1, hue: "gold", phase: 1.4, thick: h * 0.22 },
        { y: h * 0.78, amp: h * 0.07, hue: "cyan", phase: 2.6, thick: h * 0.16 },
      ];
    }

    function drawAurora(t) {
      for (var i = 0; i < bands.length; i++) {
        var b = bands[i];
        var wave = Math.sin(t * 0.00035 + b.phase) * b.amp;
        var g = ctx.createLinearGradient(0, b.y + wave - b.thick, 0, b.y + wave + b.thick);
        if (b.hue === "cyan") {
          g.addColorStop(0, "rgba(126,212,224,0)");
          g.addColorStop(0.45, "rgba(126,212,224,0.22)");
          g.addColorStop(0.55, "rgba(94,234,212,0.34)");
          g.addColorStop(1, "rgba(126,212,224,0)");
        } else {
          g.addColorStop(0, "rgba(198,165,114,0)");
          g.addColorStop(0.5, "rgba(198,165,114,0.26)");
          g.addColorStop(1, "rgba(198,165,114,0)");
        }
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.moveTo(0, b.y + wave);
        var steps = Math.max(24, Math.floor(w / 80));
        for (var s = 0; s <= steps; s++) {
          var x = (s / steps) * w;
          var y =
            b.y +
            wave +
            Math.sin(t * 0.00055 + s * 0.45 + b.phase) * (b.amp * 0.55) +
            Math.sin(t * 0.00025 + s * 0.18) * (b.amp * 0.25);
          ctx.lineTo(x, y);
        }
        ctx.lineTo(w, h);
        ctx.lineTo(0, h);
        ctx.closePath();
        ctx.globalCompositeOperation = "lighter";
        ctx.fill();
        ctx.globalCompositeOperation = "source-over";
      }
    }

    function frame(now) {
      if (!running) return;
      var t = now - t0;
      ctx.clearRect(0, 0, w, h);
      // void wash so aurora reads on any page bg
      ctx.fillStyle = "rgba(7,11,22,0.15)";
      ctx.fillRect(0, 0, w, h);
      drawAurora(t);
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        s.tw += 0.025 * s.sp;
        s.x += 0.04 * s.z * (s.gold ? 0.6 : 1);
        s.y += 0.055 * s.z;
        if (s.y > h + 2) {
          s.y = -2;
          s.x = Math.random() * w;
        }
        if (s.x > w + 2) s.x = -2;
        var a = 0.28 + 0.62 * (0.5 + 0.5 * Math.sin(s.tw));
        ctx.beginPath();
        ctx.fillStyle = s.gold
          ? "rgba(198,165,114," + a * s.z + ")"
          : "rgba(126,212,224," + a * s.z + ")";
        ctx.arc(s.x, s.y, s.r * s.z, 0, Math.PI * 2);
        ctx.fill();
      }
      // nucleus bloom
      var nx = w * 0.62;
      var ny = h * 0.28;
      var rg = ctx.createRadialGradient(nx, ny, 0, nx, ny, Math.max(w, h) * 0.38);
      rg.addColorStop(0, "rgba(126,212,224,0.14)");
      rg.addColorStop(0.45, "rgba(198,165,114,0.04)");
      rg.addColorStop(1, "rgba(7,11,22,0)");
      ctx.fillStyle = rg;
      ctx.fillRect(0, 0, w, h);
      raf = requestAnimationFrame(frame);
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

    rebuild();
    start();
    global.addEventListener(
      "resize",
      function () {
        rebuild();
      },
      { passive: true }
    );
    doc.addEventListener("visibilitychange", function () {
      if (doc.visibilityState === "hidden") stop();
      else start();
    });
    // Pause when tab scrolled far / IntersectionObserver on root viewport proxy
    if ("IntersectionObserver" in global) {
      var probe = doc.createElement("div");
      probe.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:-1;";
      probe.setAttribute("aria-hidden", "true");
      doc.body.appendChild(probe);
      var io = new IntersectionObserver(
        function (ents) {
          ents.forEach(function (en) {
            if (en.isIntersecting) start();
            else stop();
          });
        },
        { threshold: 0.01 }
      );
      io.observe(probe);
    }
    return { start: start, stop: stop, rebuild: rebuild };
  }

  /* ---------- Sigil magnetic tilt + orbit ---------- */
  function initSigilTilt() {
    if (reduced) return;
    var nodes = qsa(".il-sigil, .il-hero-sigil, [data-il-sigil-tilt]");
    nodes.forEach(function (el) {
      if (el.getAttribute("data-il-tilt-ready")) return;
      el.setAttribute("data-il-tilt-ready", "1");
      el.classList.add("il-sigil-tilt", "is-orbiting");
      var target = el;
      function onMove(e) {
        var r = target.getBoundingClientRect();
        var px = (e.clientX - r.left) / Math.max(1, r.width) - 0.5;
        var py = (e.clientY - r.top) / Math.max(1, r.height) - 0.5;
        var ry = (px * 14).toFixed(2) + "deg";
        var rx = (-py * 10).toFixed(2) + "deg";
        target.style.setProperty("--il-ry", ry);
        target.style.setProperty("--il-rx", rx);
      }
      function onLeave() {
        target.style.setProperty("--il-ry", "0deg");
        target.style.setProperty("--il-rx", "0deg");
      }
      // tilt on nearby pointer for floating hero sigil (pointer-events none) via document
      if (getComputedStyle(el).pointerEvents === "none") {
        doc.addEventListener(
          "pointermove",
          function (e) {
            var r = el.getBoundingClientRect();
            var cx = r.left + r.width / 2;
            var cy = r.top + r.height / 2;
            var dx = (e.clientX - cx) / Math.max(r.width, 1);
            var dy = (e.clientY - cy) / Math.max(r.height, 1);
            if (Math.abs(dx) > 2 || Math.abs(dy) > 2) {
              onLeave();
              return;
            }
            el.style.setProperty("--il-ry", (dx * 12).toFixed(2) + "deg");
            el.style.setProperty("--il-rx", (-dy * 10).toFixed(2) + "deg");
          },
          { passive: true }
        );
      } else {
        el.addEventListener("pointermove", onMove);
        el.addEventListener("pointerleave", onLeave);
      }
    });
  }

  /* ---------- Kinetic type accents ---------- */
  function initKinetic() {
    var h1 = qs("section.relative.isolate h1, .il-hero-uw h1, main h1");
    if (h1 && !h1.classList.contains("il-kinetic")) {
      h1.classList.add("il-kinetic");
    }
    qsa("#why-interstitium h2, #exceed-peers h2, [data-il-auto-reveal] h2").forEach(
      function (h, i) {
        if (i > 2) return;
        if (!h.querySelector(".il-kinetic-underline")) {
          var wrap = doc.createElement("span");
          wrap.className = "il-kinetic-underline";
          while (h.firstChild) wrap.appendChild(h.firstChild);
          h.appendChild(wrap);
        }
      }
    );
  }

  /* ---------- Command palette ⌘K / Ctrl+K ---------- */
  var CMD = [
    { label: "Instant Demo Path", href: "/demo/", keys: "demo instant musk" },
    { label: "Challenge of the Day", href: "/labs/challenge/", keys: "challenge cotd" },
    { label: "Trending MIT LinkedIn X", href: "/trending/", keys: "trending mit linkedin x" },
    { label: "Lab Muse", href: "/coach/", keys: "muse coach" },
    { label: "Time-to-hire OS", href: "/os/", keys: "os hire" },
    { label: "Scenario exam", href: "/exam/", keys: "exam" },
    { label: "Proof export", href: "/proof/", keys: "proof" },
    { label: "Adapt", href: "/adapt/", keys: "adapt" },
    { label: "Paths exceed", href: "/paths/#exceed-paths", keys: "paths" },
    { label: "Zero to Hire", href: "/paths/devops-zero-to-hire/", keys: "hire" },
    { label: "Learn", href: "/learn/", keys: "learn" },
    { label: "Prep", href: "/prep/", keys: "prep" },
    { label: "Labs", href: "/labs/", keys: "labs" },
    { label: "Peer matrix", href: "/about/#peer-matrix", keys: "matrix" },
  ];

  function ensureCmd() {
    var el = qs("#il-cmd");
    if (el) return el;
    el = doc.createElement("div");
    el.id = "il-cmd";
    el.className = "il-cmd";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    el.setAttribute("aria-label", "Command palette");
    el.innerHTML =
      '<div class="il-cmd-panel">' +
      '<input class="il-cmd-input" type="search" placeholder="Jump to learn, prep, adapt, labs, coach…" aria-label="Jump" autocomplete="off" spellcheck="false"/>' +
      '<ul class="il-cmd-list" role="listbox"></ul>' +
      '<div class="il-cmd-hint">⌘K / Ctrl+K · Esc close · ↑↓ · Enter</div>' +
      "</div>";
    doc.body.appendChild(el);
    return el;
  }

  var cmdIndex = 0;
  var cmdFilter = "";

  function paintCmd() {
    var el = ensureCmd();
    var list = el.querySelector(".il-cmd-list");
    var q = cmdFilter.trim().toLowerCase();
    var items = CMD.filter(function (c) {
      if (!q) return true;
      return (
        c.label.toLowerCase().indexOf(q) >= 0 ||
        c.keys.indexOf(q) >= 0 ||
        c.href.indexOf(q) >= 0
      );
    });
    if (!items.length) {
      list.innerHTML = '<li class="il-cmd-item">No matches</li>';
      return items;
    }
    if (cmdIndex >= items.length) cmdIndex = 0;
    list.innerHTML = items
      .map(function (c, i) {
        return (
          '<li class="il-cmd-item" role="option" aria-selected="' +
          (i === cmdIndex ? "true" : "false") +
          '" data-href="' +
          c.href +
          '"><span>' +
          c.label +
          "</span><kbd>" +
          c.href +
          "</kbd></li>"
        );
      })
      .join("");
    qsa(".il-cmd-item", list).forEach(function (li) {
      li.addEventListener("click", function () {
        var href = li.getAttribute("data-href");
        if (href) global.location.href = href;
      });
    });
    return items;
  }

  function openCmd() {
    var el = ensureCmd();
    el.classList.add("is-open");
    cmdFilter = "";
    cmdIndex = 0;
    var input = el.querySelector(".il-cmd-input");
    input.value = "";
    paintCmd();
    setTimeout(function () {
      input.focus();
    }, 10);
    blip("ok");
  }

  function closeCmd() {
    var el = qs("#il-cmd");
    if (!el) return;
    el.classList.remove("is-open");
  }

  function initCmd() {
    ensureCmd();
    var el = qs("#il-cmd");
    var input = el.querySelector(".il-cmd-input");
    input.addEventListener("input", function () {
      cmdFilter = input.value;
      cmdIndex = 0;
      paintCmd();
    });
    input.addEventListener("keydown", function (e) {
      var items = paintCmd();
      if (e.key === "ArrowDown") {
        e.preventDefault();
        cmdIndex = Math.min(items.length - 1, cmdIndex + 1);
        paintCmd();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        cmdIndex = Math.max(0, cmdIndex - 1);
        paintCmd();
      } else if (e.key === "Enter") {
        e.preventDefault();
        if (items[cmdIndex]) global.location.href = items[cmdIndex].href;
      } else if (e.key === "Escape") {
        closeCmd();
      }
    });
    el.addEventListener("click", function (e) {
      if (e.target === el) closeCmd();
    });
    doc.addEventListener("keydown", function (e) {
      var meta = e.metaKey || e.ctrlKey;
      if (meta && (e.key === "k" || e.key === "K")) {
        e.preventDefault();
        if (el.classList.contains("is-open")) closeCmd();
        else openCmd();
      } else if (e.key === "Escape") closeCmd();
    });
  }

  /* ---------- Demo mode (20s wow) ---------- */
  var demoTimer = null;
  var demoRunning = false;

  function setDemoStatus(msg) {
    var s = qs(".il-demo-status");
    if (s) s.textContent = msg || "";
  }

  function runDemo() {
    if (demoRunning) {
      stopDemo();
      return;
    }
    demoRunning = true;
    var btn = qs("[data-il-demo]");
    if (btn) btn.classList.add("is-on");
    setDemoStatus("Demo · placement");
    blip("ok");
    // Sigil pulse
    qsa(".il-sigil-tilt").forEach(function (el) {
      el.classList.add("is-orbiting");
    });
    // Fake placement answers on mini widget if present
    var choices = qsa(".il-adapt-mini .choice");
    var step = 0;
    var sequence = [
      function () {
        setDemoStatus("Demo · CAT probe");
        if (choices[0]) choices[0].click();
      },
      function () {
        setDemoStatus("Demo · XP pulse");
        if (global.ILGame && typeof global.ILGame.award === "function") {
          global.ILGame.award("demo_pulse");
        } else {
          // fallback: dispatch level celebrate
          hapticPulse();
          if (global.ILGame && global.ILGame.celebrate) global.ILGame.celebrate((global.ILGame.getState && global.ILGame.getState().level) || 2);
        }
        blip("level");
      },
      function () {
        setDemoStatus("Demo · sigil orbit");
        qsa(".il-hero-sigil, .il-sigil--spin-slow").forEach(function (el) {
          el.style.transition = "filter 0.4s";
          el.style.filter = "drop-shadow(0 0 48px rgba(126,212,224,0.85))";
        });
      },
      function () {
        setDemoStatus("Demo · level burst");
        hapticPulse();
        if (global.ILGame && global.ILGame.celebrate) {
          var lvl = (global.ILGame.getState && global.ILGame.getState().level) || 3;
          global.ILGame.celebrate(lvl);
        }
        blip("level");
      },
      function () {
        setDemoStatus("Demo · Adaptive OS");
        // flash mini CTA
        var mini = qs(".il-adapt-mini");
        if (mini) {
          mini.style.boxShadow = "0 0 0 1px rgba(126,212,224,0.55), 0 0 48px rgba(126,212,224,0.25)";
        }
      },
      function () {
        stopDemo();
      },
    ];
    var marks = [1500, 4500, 8000, 12000, 16000, 20000];
    demoTimer = [];
    marks.forEach(function (ms, i) {
      demoTimer.push(
        setTimeout(function () {
          if (!demoRunning) return;
          sequence[i]();
        }, ms)
      );
    });
  }

  function stopDemo() {
    demoRunning = false;
    if (demoTimer) {
      demoTimer.forEach(clearTimeout);
      demoTimer = null;
    }
    var btn = qs("[data-il-demo]");
    if (btn) btn.classList.remove("is-on");
    setDemoStatus("");
    qsa(".il-hero-sigil, .il-sigil--spin-slow").forEach(function (el) {
      el.style.filter = "";
    });
    var mini = qs(".il-adapt-mini");
    if (mini) mini.style.boxShadow = "";
  }

  function hapticPulse() {
    if (reduced) return;
    var ring = doc.createElement("div");
    ring.className = "il-haptic-ring";
    doc.body.appendChild(ring);
    setTimeout(function () {
      ring.remove();
    }, 750);
    if (global.navigator && global.navigator.vibrate) {
      try {
        global.navigator.vibrate([12, 30, 12]);
      } catch (e2) {}
    }
  }

  function initDemoBar() {
    if (qs(".il-demo-bar")) return;
    var bar = doc.createElement("div");
    bar.className = "il-demo-bar no-print";
    bar.innerHTML =
      '<a class="il-demo-path-link" data-il-demo-path-link href="/demo/">Instant path</a>' + '<button type="button" data-il-demo title="FX demo">Demo FX</button>' +
      '<button type="button" class="il-cmd-open" data-il-cmd title="Command palette">⌘K</button>' +
      '<button type="button" class="il-sound-toggle" data-il-sound title="UI sound (off by default)" aria-pressed="false">Sound</button>' +
      '<span class="il-demo-status" aria-live="polite"></span>';
    doc.body.appendChild(bar);
    bar.querySelector("[data-il-demo]").addEventListener("click", function () {
      unlockSoundOnce();
      runDemo();
    });
    bar.querySelector("[data-il-cmd]").addEventListener("click", function () {
      openCmd();
    });
    var snd = bar.querySelector("[data-il-sound]");
    if (soundOn) {
      snd.classList.add("is-on");
      snd.setAttribute("aria-pressed", "true");
    }
    snd.addEventListener("click", function () {
      soundOn = !soundOn;
      try {
        global.localStorage.setItem(SOUND_KEY, soundOn ? "1" : "0");
      } catch (e3) {}
      snd.classList.toggle("is-on", soundOn);
      snd.setAttribute("aria-pressed", soundOn ? "true" : "false");
      if (soundOn) {
        unlocked = true;
        ensureAudio();
        blip("ok");
      }
    });
  }

  /* ---------- Adaptive mini CAT (1 sample item inline) ---------- */
  var SAMPLE = {
    id: "linux-shell.ls-home",
    stem: "Which command lists all files including hidden ones in the current directory?",
    choices: [
      { key: "A", text: "ls -a" },
      { key: "B", text: "ls -l" },
      { key: "C", text: "cd ~" },
      { key: "D", text: "pwd" },
    ],
    answerKey: "A",
    feedback: {
      A: "Correct — -a shows entries starting with '.' (hidden).",
      B: "-l is long format; it does not imply hidden files.",
      C: "That changes directory to home; it does not list.",
      D: "pwd prints the working directory path.",
    },
  };

  function mountAdaptMini() {
    var host = qs("[data-il-adapt-mini]");
    if (!host || host.getAttribute("data-ready")) return;
    host.setAttribute("data-ready", "1");
    host.classList.add("il-adapt-mini");
    var html =
      '<p class="il-kicker" data-i18n="adapt.mini.kicker">Live CAT sample · Adaptive OS</p>' +
      "<h3 data-i18n=\"adapt.mini.title\">One probe. Instant fringe signal.</h3>" +
      '<p class="stem">' +
      SAMPLE.stem +
      "</p>" +
      '<div class="choices" role="group" aria-label="Answer choices">';
    SAMPLE.choices.forEach(function (c) {
      html +=
        '<button type="button" class="choice" data-key="' +
        c.key +
        '"><strong>' +
        c.key +
        "</strong> · " +
        c.text +
        "</button>";
    });
    html +=
      '</div><p class="fb" aria-live="polite"></p>' +
      '<div class="cta-row">' +
      '<a href="/adapt/" class="inline-flex h-10 items-center rounded-lg bg-paper px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em] text-void" data-i18n="cta.adaptive">Adaptive OS</a>' +
      '<a href="/adapt/#session" class="inline-flex h-10 items-center rounded-lg border border-cyan/40 px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em] text-cyan">Full session</a>' +
      "</div>";
    host.innerHTML = html;
    var fb = host.querySelector(".fb");
    var locked = false;
    qsa(".choice", host).forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (locked) return;
        locked = true;
        unlockSoundOnce();
        var key = btn.getAttribute("data-key");
        var ok = key === SAMPLE.answerKey;
        qsa(".choice", host).forEach(function (b) {
          var k = b.getAttribute("data-key");
          if (k === SAMPLE.answerKey) b.classList.add("is-ok");
          else if (k === key) b.classList.add("is-bad");
          b.disabled = true;
        });
        fb.textContent = SAMPLE.feedback[key] || "";
        fb.classList.toggle("is-ok", ok);
        blip(ok ? "ok" : "bad");
        if (ok && global.ILGame && typeof global.ILGame.award === "function") {
          try {
            global.ILGame.award("adapt_mini_ok");
          } catch (e4) {}
        } else if (ok) {
          pulseHudFallback();
        }
      });
    });
  }

  function pulseHudFallback() {
    var hud = qs("#il-game-hud");
    if (hud) {
      hud.classList.add("is-pulse");
      setTimeout(function () {
        hud.classList.remove("is-pulse");
      }, 280);
    }
  }

  /* ---------- Level-up haptic hook ---------- */
  function initLevelHooks() {
    doc.addEventListener("il:game", function (ev) {
      var d = ev.detail || {};
      if (d.type === "level_up" || d.leveled) {
        hapticPulse();
        blip("level");
      } else if (d.gained > 0) {
        blip("ok");
      }
    });
  }

  /* ---------- Hero CTA rewrite helpers already in HTML; ensure dead links fixed via stubs ---------- */


  /* ---------- Lockup repair + page enter ---------- */
  function repairChrome() {
    qsa('header a img[src*="canonical-lockup"], header img[src*="canonical-lockup"], footer img[src*="canonical-lockup"], img.il-lockup, picture.il-lockup img').forEach(function (img) {
      img.classList.add("il-lockup");
      // P0 brand: industry lockup heights — never postage stamp, never height:auto.
      var uw = window.matchMedia("(min-width: 2560px)").matches;
      var xl = window.matchMedia("(min-width: 3840px)").matches;
      var sm = window.matchMedia("(min-width: 640px)").matches;
      var h = xl ? "80px" : uw ? "72px" : sm ? "64px" : "56px";
      var maxH = xl || uw ? "80px" : "72px";
      var inFooter = !!(img.closest && img.closest("footer"));
      if (inFooter) {
        h = sm ? "56px" : "48px";
        maxH = "64px";
      }
      img.style.setProperty("height", h, "important");
      img.style.setProperty("max-height", maxH, "important");
      img.style.setProperty("min-height", h, "important");
      img.style.setProperty("width", "auto", "important");
      img.style.setProperty("max-width", inFooter ? "min(320px, 70vw)" : "min(360px, 70vw)", "important");
      img.style.setProperty("min-width", sm ? "144px" : "120px", "important");
      img.style.setProperty("object-fit", "contain", "important");
      img.style.setProperty("object-position", "left center", "important");
      img.style.setProperty("display", "block", "important");
      img.style.setProperty("flex-shrink", "0", "important");
      if (!img.getAttribute("width")) img.setAttribute("width", "178");
      if (!img.getAttribute("height")) img.setAttribute("height", "80");
      var a = img.closest("a");
      if (a) {
        a.style.display = "inline-flex";
        a.style.alignItems = "center";
        a.style.minHeight = h;
        a.style.maxHeight = "none";
        a.style.overflow = "visible";
        a.style.flexShrink = "0";
      }
      if (img.decode) img.decode().catch(function () {});
    });
    // Keep header row tall enough for the lockup
    qsa("header .mx-auto.flex, header.sticky > .mx-auto.flex").forEach(function (row) {
      var uw = window.matchMedia("(min-width: 2560px)").matches;
      var sm = window.matchMedia("(min-width: 640px)").matches;
      row.style.minHeight = uw ? "5.25rem" : sm ? "5rem" : "4.5rem";
      row.style.height = "auto";
      row.style.overflowY = "visible";
      row.style.alignItems = "center";
    });
    qsa(".il-sigil img, .il-hero-sigil img, .il-emblem img").forEach(function (img) {
      if (!img.getAttribute("width")) img.setAttribute("width", "200");
      if (!img.getAttribute("height")) img.setAttribute("height", "200");
      img.style.width = "100%";
      img.style.height = "auto";
      img.style.minHeight = "120px";
      img.style.display = "block";
    });
  }

  function pageEnter() {
    doc.documentElement.classList.add("il-fx-ready");
    requestAnimationFrame(function () {
      doc.documentElement.classList.add("il-page-in");
    });
  }

  function boot() {
    if (!doc.body) return;
    pageEnter();
    repairChrome();
    initAurora();
    initSigilTilt();
    initKinetic();
    initCmd();
    initDemoBar();
    mountAdaptMini();
    initLevelHooks();
    setTimeout(repairChrome, 400);
    setTimeout(repairChrome, 1200);
    // First gesture unlocks audio if user already opted in
    ["pointerdown", "keydown"].forEach(function (evt) {
      doc.addEventListener(
        evt,
        function () {
          unlockSoundOnce();
        },
        { once: true, passive: true }
      );
    });
  }

  global.ILFX = global.ILFx = {
    boot: boot,
    openCmd: openCmd,
    closeCmd: closeCmd,
    runDemo: runDemo,
    stopDemo: stopDemo,
    blip: blip,
    hapticPulse: hapticPulse,
    reduced: reduced,
  };

  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", boot);
  else boot();
})(typeof window !== "undefined" ? window : this);
