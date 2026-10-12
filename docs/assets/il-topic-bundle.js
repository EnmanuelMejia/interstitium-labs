/* =====================================================================
 * Interstitium Labs — Topic Pages Bundle (2026-10-09)
 * Concatenation of 15 deferred topic-page scripts in original load order.
 * Replaces 15 separate <script defer> requests with 1.
 * il-theme.js stays separate (must run synchronously before first paint).
 * noah-full.js stays separate (ordered capability loader).
 * Sources (in order):
 *   - assets/il-compat.js
 *   - assets/il-game.js
 *   - assets/il-motion.js
 *   - assets/il-pwa.js
 *   - analytics/config.js
 *   - assets/il-analytics.js
 *   - assets/il-i18n.js
 *   - assets/il-coach.js
 *   - assets/il-model-router.js
 *   - assets/il-model-analytics.js
 *   - assets/il-model-panel.js
 *   - assets/il-scene-kit.js
 *   - assets/il-noah-avatar.js
 *   - assets/il-muse.js
 *   - assets/il-challenge.js
 * ===================================================================== */

/* ---- source: assets/il-compat.js (2563 bytes) ---- */
/**
 * Interstitium Labs — lightweight compatibility helpers
 * - --il-vh fallback for older Safari / WebViews without dvh
 * - Detect PWA standalone + Capacitor for safe-area CSS hooks
 * Safe to load with defer; idempotent.
 */
(function (w, d) {
  "use strict";
  if (w.__IL_COMPAT__) return;
  w.__IL_COMPAT__ = true;

  if (!d.getElementById("il-logo")) {
    var logo = d.createElement("script");
    logo.id = "il-logo";
    logo.src = "/assets/il-logo.js";
    logo.defer = true;
    d.head.appendChild(logo);
  }

  // Practice-language theme is opt-in only: pages add class="il-practice-lang"
  // to <body> (or <html>). Never loaded globally — the brand Space Grotesk /
  // Inter stack stays the one global stack.
  var practiceOptIn =
    d.body && d.body.classList && d.body.classList.contains("il-practice-lang");
  if (practiceOptIn && !d.getElementById("il-practice-language")) {
    var link = d.createElement("link");
    link.id = "il-practice-language";
    link.rel = "stylesheet";
    link.href = "/assets/il-practice-language.css";
    d.head.appendChild(link);
  }

  var root = d.documentElement;

  function setVh() {
    var h = w.innerHeight || (d.documentElement && d.documentElement.clientHeight) || 0;
    if (!h) return;
    root.style.setProperty("--il-vh", h / 100 + "px");
  }

  function detectShell() {
    var standalone = false;
    try {
      standalone =
        (w.matchMedia && w.matchMedia("(display-mode: standalone)").matches) ||
        (w.navigator && w.navigator.standalone === true);
    } catch (_) {}
    if (standalone) root.classList.add("il-standalone");

    var cap = false;
    try {
      cap = !!(
        w.Capacitor ||
        (w.navigator && /capacitor/i.test(w.navigator.userAgent || "")) ||
        (w.navigator && /InterstitiumLabs/i.test(w.navigator.userAgent || ""))
      );
    } catch (_) {}
    if (cap) root.classList.add("il-capacitor");
  }

  setVh();
  detectShell();

  var resizeTimer = null;
  function onResize() {
    if (resizeTimer) w.clearTimeout(resizeTimer);
    resizeTimer = w.setTimeout(setVh, 100);
  }

  w.addEventListener("resize", onResize, { passive: true });
  w.addEventListener("orientationchange", function () {
    w.setTimeout(setVh, 200);
  }, { passive: true });

  // VisualViewport accounts for iOS URL bar show/hide
  if (w.visualViewport) {
    w.visualViewport.addEventListener("resize", onResize, { passive: true });
  }

  if (d.readyState === "loading") {
    d.addEventListener("DOMContentLoaded", setVh, { once: true });
  }
})(window, document);
;

/* ---- source: assets/il-game.js (25162 bytes) ---- */
/**
 * Interstitium Labs — Learning OS gamification (vanilla).
 * Namespace: localStorage key `il.game.v1`
 * API: window.ILGame = { award, getState, renderHUD, celebrate, bindProgress, mountQuestBoard }
 */
(function (global) {
  "use strict";

  var STORAGE_KEY = "il.game.v1";
  var MAX_LEVEL = 50;
  var reduced =
    global.matchMedia &&
    global.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var EVENT_XP = {
    checklist_tick: 15,
    path_open: 10,
    drill_complete: 50,
    daily_login: 25,
    radar_update: 20,
    quest_claim: 35,
    badge_bonus: 100,
    adapt_mini_ok: 40,
    demo_pulse: 55,
  };

  /** Cumulative XP required to reach level L (1-indexed). Soft curve → L50. */
  function xpForLevel(level) {
    if (level <= 1) return 0;
    var n = Math.min(MAX_LEVEL, Math.max(1, level));
    // ~ sum_{i=1}^{n-1} (80 + 18*i + floor(i^1.35))
    var total = 0;
    for (var i = 1; i < n; i++) {
      total += 80 + 18 * i + Math.floor(Math.pow(i, 1.35));
    }
    return total;
  }

  var XP_CAP = xpForLevel(MAX_LEVEL);

  var BADGES = [
    {
      id: "first_commit",
      name: "First Commit",
      blurb: "First checklist tick in the Learning OS",
      event: "checklist_tick",
      min: 1,
    },
    {
      id: "cidr_cleared",
      name: "CIDR Cleared",
      blurb: "Complete Prep Math (or founders math block)",
      unlock: function (s) {
        return !!(s.flags && (s.flags.prep_math || s.flags.founders_math));
      },
    },
    {
      id: "pipeline_pilot",
      name: "Pipeline Pilot",
      blurb: "Ship a CI/CD or lab checklist item",
      unlock: function (s) {
        return !!(s.flags && (s.flags.founders_lab || s.flags.prep_devops));
      },
    },
    {
      id: "streak_7",
      name: "Week Flame",
      blurb: "7-day study streak",
      unlock: function (s) {
        return (s.streak || 0) >= 7;
      },
    },
    {
      id: "streak_30",
      name: "Month Forge",
      blurb: "30-day study streak",
      unlock: function (s) {
        return (s.streak || 0) >= 30;
      },
    },
    {
      id: "level_10",
      name: "Operative L10",
      blurb: "Reach level 10",
      unlock: function (s) {
        return (s.level || 1) >= 10;
      },
    },
    {
      id: "level_25",
      name: "Architect L25",
      blurb: "Reach level 25",
      unlock: function (s) {
        return (s.level || 1) >= 25;
      },
    },
    {
      id: "radar_ping",
      name: "Radar Ping",
      blurb: "Update the skills radar",
      event: "radar_update",
      min: 1,
    },
    {
      id: "drill_ace",
      name: "Drill Ace",
      blurb: "Complete an interview drill",
      event: "drill_complete",
      min: 1,
    },
    {
      id: "pathfinder",
      name: "Pathfinder",
      blurb: "Open 5 distinct paths",
      unlock: function (s) {
        return Object.keys((s.paths && s.paths) || {}).length >= 5;
      },
    },
    {
      id: "quest_runner",
      name: "Quest Runner",
      blurb: "Claim 3 daily quests",
      unlock: function (s) {
        return (s.questsClaimed || 0) >= 3;
      },
    },
    {
      id: "star_teller",
      name: "STAR Teller",
      blurb: "Complete a STAR / elevator drill tick",
      unlock: function (s) {
        return !!(s.flags && s.flags.founders_star);
      },
    },
    {
      id: "superlab_scout",
      name: "SuperLab Scout",
      blurb: "Claim Clone SuperLab XP",
      unlock: function (s) {
        return !!(s.flags && s.flags.superlab_clone);
      },
    },
  ];

  var DAILY_QUESTS = [
    {
      id: "q_math",
      title: "Math fluency block",
      xp: 35,
      href: "/prep/math/",
      hint: "30 min Boolean / CIDR",
    },
    {
      id: "q_code",
      title: "Coding kata",
      xp: 40,
      href: "/prep/programming/",
      hint: "Python / Bash sitting",
    },
    {
      id: "q_lab",
      title: "Tool lab",
      xp: 40,
      href: "/prep/devops/",
      hint: "Terraform · Docker · Jenkins",
    },
    {
      id: "q_star",
      title: "STAR elevator",
      xp: 30,
      href: "/prep/drills/desk-interview/#tell-me",
      hint: "One honest story out loud",
    },
    {
      id: "q_ship",
      title: "Ship something small",
      xp: 45,
      href: "/founders/#weekly-os",
      hint: "README, lab, or PR",
    },
    {
      id: "q_radar",
      title: "Radar honesty pass",
      xp: 25,
      href: "/founders/#radar",
      hint: "Re-rate one competency",
    },
    {
      id: "q_superlab",
      title: "Clone SuperLab",
      xp: 40,
      href: "/labs/superlab/#quickstart",
      hint: "Open hub · clone the flagship lab",
    },
  ];

  function today() {
    return new Date().toISOString().slice(0, 10);
  }

  function safeParse(raw, fallback) {
    try {
      if (raw == null) return fallback;
      return JSON.parse(raw);
    } catch (e) {
      return fallback;
    }
  }

  function defaultState() {
    return {
      v: 1,
      xp: 0,
      level: 1,
      streak: 0,
      lastLogin: null,
      events: {},
      badges: {},
      flags: {},
      paths: {},
      quests: {},
      questsDay: null,
      questsClaimed: 0,
      history: [],
    };
  }

  function load() {
    var raw = null;
    try {
      raw = global.localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      /* private mode — fall through to default state */
    }
    var s = safeParse(raw, null);
    if (!s || typeof s !== "object") s = defaultState();
    if (s.v !== 1) s.v = 1;
    s.xp = Math.max(0, Number(s.xp) || 0);
    s.level = levelFromXp(s.xp);
    s.events = s.events || {};
    s.badges = s.badges || {};
    s.flags = s.flags || {};
    s.paths = s.paths || {};
    s.quests = s.quests || {};
    s.history = Array.isArray(s.history) ? s.history.slice(-40) : [];
    return s;
  }

  function save(s) {
    try {
      global.localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
    } catch (e) {
      /* quota / private mode */
    }
  }

  function levelFromXp(xp) {
    var lvl = 1;
    for (var L = 2; L <= MAX_LEVEL; L++) {
      if (xp >= xpForLevel(L)) lvl = L;
      else break;
    }
    return lvl;
  }

  function progressInLevel(s) {
    var lvl = s.level || 1;
    var floor = xpForLevel(lvl);
    var ceil = lvl >= MAX_LEVEL ? floor : xpForLevel(lvl + 1);
    var span = Math.max(1, ceil - floor);
    var into = Math.max(0, (s.xp || 0) - floor);
    return {
      floor: floor,
      ceil: ceil,
      into: into,
      span: span,
      pct: Math.min(100, Math.round((into / span) * 100)),
    };
  }

  function bumpStreak(s) {
    var d = today();
    if (s.lastLogin === d) return s;
    var y = new Date();
    y.setDate(y.getDate() - 1);
    var ymd = y.toISOString().slice(0, 10);
    s.streak = s.lastLogin === ymd ? (s.streak || 0) + 1 : 1;
    s.lastLogin = d;
    return s;
  }

  function unlockBadges(s, newly) {
    newly = newly || [];
    BADGES.forEach(function (b) {
      if (s.badges[b.id]) return;
      var ok = false;
      if (typeof b.unlock === "function") ok = !!b.unlock(s);
      else if (b.event) ok = (s.events[b.event] || 0) >= (b.min || 1);
      if (ok) {
        s.badges[b.id] = { at: Date.now(), name: b.name };
        newly.push(b);
      }
    });
    return newly;
  }

  function award(event, xp, meta) {
    meta = meta || {};
    var amount =
      typeof xp === "number" && !isNaN(xp)
        ? xp
        : EVENT_XP[event] != null
          ? EVENT_XP[event]
          : 10;
    var s = load();
    var prevLevel = s.level;
    bumpStreak(s);

    // Idempotent daily_login
    if (event === "daily_login") {
      var dayKey = "daily:" + today();
      if (s.events[dayKey]) {
        save(s);
        paintAll();
        return { state: getState(), gained: 0, leveled: false, badges: [] };
      }
      s.events[dayKey] = 1;
    }

    // Dedup checklist / flag events when meta.id provided
    if (meta.id && meta.once) {
      var onceKey = event + ":" + meta.id;
      if (s.events[onceKey]) {
        save(s);
        paintAll();
        return { state: getState(), gained: 0, leveled: false, badges: [] };
      }
      s.events[onceKey] = 1;
    }

    s.events[event] = (s.events[event] || 0) + 1;
    if (meta.flag) s.flags[meta.flag] = true;
    if (meta.path) s.paths[meta.path] = Date.now();

    s.xp = Math.min(XP_CAP + 5000, (s.xp || 0) + amount);
    s.level = levelFromXp(s.xp);
    s.history.push({
      t: Date.now(),
      e: event,
      xp: amount,
      m: meta.label || null,
    });
    if (s.history.length > 40) s.history = s.history.slice(-40);

    var newBadges = unlockBadges(s, []);
    // Small bonus XP for brand-new badges (once)
    if (newBadges.length) {
      s.xp += newBadges.length * 25;
      s.level = levelFromXp(s.xp);
    }

    save(s);
    var leveled = s.level > prevLevel;
    var result = {
      type: event,
      event: event,
      state: getState(),
      gained: amount,
      leveled: leveled,
      badges: newBadges,
      prevLevel: prevLevel,
      meta: meta,
    };

    paintAll();
    if (leveled) {
      celebrateLevelUp(s.level);
      try {
        dispatch("il:game", { type: "level_up", event: "hud_level_up", level: s.level, prevLevel: prevLevel });
      } catch (e0) {}
    } else if (amount > 0) pulseHUD();
    if (newBadges.length) toastBadges(newBadges);
    dispatch("il:game", result);
    return result;
  }

  function getState() {
    var s = load();
    var prog = progressInLevel(s);
    return {
      xp: s.xp,
      level: s.level,
      streak: s.streak || 0,
      lastLogin: s.lastLogin,
      badges: Object.keys(s.badges || {}),
      badgeDetail: s.badges,
      flags: s.flags,
      paths: s.paths,
      events: s.events,
      progress: prog,
      maxLevel: MAX_LEVEL,
      xpToNext: Math.max(0, prog.ceil - s.xp),
      questsClaimed: s.questsClaimed || 0,
    };
  }

  function dispatch(name, detail) {
    try {
      global.document.dispatchEvent(
        new CustomEvent(name, { bubbles: true, detail: detail })
      );
    } catch (e) {}
  }

  /* ---------- HUD ---------- */

  function ensureHUDStyles() {
    if (global.document.getElementById("il-game-hud-css")) return;
    var css = global.document.createElement("style");
    css.id = "il-game-hud-css";
    css.textContent =
      ".il-hud{position:fixed;z-index:45;right:max(0.75rem,env(safe-area-inset-right));" +
      "bottom:calc(4.75rem + env(safe-area-inset-bottom));" +
      "display:flex;align-items:center;gap:0.65rem;padding:0.45rem 0.7rem 0.45rem 0.55rem;" +
      "border-radius:999px;background:rgba(7,11,22,0.88);backdrop-filter:blur(12px);" +
      "border:1px solid rgba(232,238,245,0.12);box-shadow:0 8px 32px rgba(0,0,0,0.45);" +
      "font-family:Space Grotesk,Inter,system-ui,sans-serif;color:#e8eef5;" +
      "transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease}" +
      "@media(min-width:1024px){.il-hud{bottom:max(1rem,env(safe-area-inset-bottom))}}" +
      ".il-hud.is-pulse{transform:scale(1.04);border-color:rgba(94,234,212,0.55);" +
      "box-shadow:0 0 0 1px rgba(94,234,212,0.35),0 8px 32px rgba(0,0,0,0.45)}" +
      ".il-hud-lvl{font-size:0.62rem;letter-spacing:0.14em;text-transform:uppercase;" +
      "color:#5eead4;font-weight:600;white-space:nowrap}" +
      ".il-hud-bar{width:4.5rem;height:0.35rem;border-radius:99px;background:rgba(232,238,245,0.1);overflow:hidden}" +
      ".il-hud-bar>i{display:block;height:100%;width:0;background:linear-gradient(90deg,#5eead4,#c9a227);" +
      "border-radius:99px;transition:width .4s cubic-bezier(.22,1,.36,1)}" +
      ".il-hud-xp{font-family:JetBrains Mono,ui-monospace,monospace;font-size:0.58rem;" +
      "color:#8b9bb4;letter-spacing:0.04em;min-width:2.4rem}" +
      ".il-hud-flame{display:inline-flex;align-items:center;gap:0.2rem;font-family:JetBrains Mono,monospace;" +
      "font-size:0.62rem;color:#c9a227}" +
      ".il-hud-flame svg{width:0.85rem;height:0.85rem}" +
      ".il-toast{position:fixed;z-index:50;left:50%;top:max(1rem,env(safe-area-inset-top));" +
      "transform:translateX(-50%) translateY(-120%);opacity:0;transition:transform .35s ease,opacity .35s ease;" +
      "padding:0.65rem 1rem;border-radius:0.75rem;background:rgba(12,18,34,0.95);" +
      "border:1px solid rgba(201,162,39,0.45);color:#e8eef5;font-size:0.8rem;max-width:min(22rem,92vw);" +
      "box-shadow:0 12px 40px rgba(0,0,0,0.5)}" +
      ".il-toast.is-on{transform:translateX(-50%) translateY(0);opacity:1}" +
      ".il-confetti{position:fixed;inset:0;pointer-events:none;z-index:60}" +
      ".il-badge-row{display:flex;flex-wrap:wrap;gap:0.5rem}" +
      ".il-badge{display:inline-flex;flex-direction:column;gap:0.15rem;min-width:6.5rem;max-width:9rem;" +
      "padding:0.55rem 0.65rem;border-radius:0.75rem;background:rgba(12,18,34,0.9);" +
      "border:1px solid rgba(232,238,245,0.1);opacity:0.42;transition:opacity .25s,border-color .25s,transform .2s}" +
      ".il-badge.is-on{opacity:1;border-color:rgba(94,234,212,0.35)}" +
      ".il-badge strong{font-size:0.72rem;font-weight:600;color:#e8eef5}" +
      ".il-badge span{font-family:JetBrains Mono,monospace;font-size:0.55rem;letter-spacing:0.08em;" +
      "text-transform:uppercase;color:#8b9bb4}" +
      ".il-quest{display:flex;flex-direction:column;gap:0.35rem;padding:1rem;border-radius:0.9rem;" +
      "background:rgba(12,18,34,0.95);border:1px solid rgba(232,238,245,0.1)}" +
      ".il-quest.is-done{border-color:rgba(94,234,212,0.35);opacity:0.75}" +
      ".il-quest button{align-self:flex-start;margin-top:0.35rem}";
    global.document.head.appendChild(css);
  }

  function renderHUD(el) {
    ensureHUDStyles();
    var host = el;
    if (!host) {
      host = global.document.getElementById("il-game-hud");
      if (!host) {
        host = global.document.createElement("div");
        host.id = "il-game-hud";
        host.className = "il-hud";
        host.setAttribute("role", "status");
        host.setAttribute("aria-live", "polite");
        host.setAttribute("aria-label", "Learning OS progress");
        global.document.body.appendChild(host);
      }
    }
    var st = getState();
    var pct = st.progress.pct;
    host.innerHTML =
      '<span class="il-hud-lvl">L' +
      st.level +
      '</span>' +
      '<span class="il-hud-bar" title="XP to next level: ' +
      st.xpToNext +
      '"><i style="width:' +
      pct +
      '%"></i></span>' +
      '<span class="il-hud-xp">' +
      st.xp +
      " XP</span>" +
      '<span class="il-hud-flame" title="Study streak">' +
      '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2c.4 3.2-1.8 5.2-3.5 6.8C6.5 10.5 5 12.4 5 15.2 5 18.9 8 22 12 22s7-3.1 7-6.8c0-2.2-1-4.1-2.4-5.5-.5 2.1-1.7 3.2-1.7 3.2S16.2 8.4 12 2z"/></svg>' +
      st.streak +
      "</span>";
    return host;
  }

  function paintAll() {
    var hud = global.document.getElementById("il-game-hud");
    if (hud || global.document.body) renderHUD(hud || null);
    var badgeHosts = global.document.querySelectorAll("[data-il-badges]");
    badgeHosts.forEach(function (h) {
      renderBadges(h);
    });
    var streakEls = global.document.querySelectorAll("[data-il-game-streak]");
    var st = getState();
    streakEls.forEach(function (el) {
      el.textContent = String(st.streak);
    });
    var lvlEls = global.document.querySelectorAll("[data-il-game-level]");
    lvlEls.forEach(function (el) {
      el.textContent = "L" + st.level;
    });
    var xpEls = global.document.querySelectorAll("[data-il-game-xp]");
    xpEls.forEach(function (el) {
      el.textContent = String(st.xp);
    });
  }

  function pulseHUD() {
    if (reduced) return;
    var hud = global.document.getElementById("il-game-hud");
    if (hud) {
      hud.classList.add("is-pulse");
      setTimeout(function () {
        hud.classList.remove("is-pulse");
      }, 280);
    }
    var chips = global.document.querySelectorAll(
      "[data-il-game-xp], [data-il-game-level], [data-il-game-streak]"
    );
    chips.forEach(function (el) {
      el.classList.add("il-chip-pulse");
      setTimeout(function () {
        el.classList.remove("il-chip-pulse");
      }, 420);
    });
  }

  function toast(msg) {
    ensureHUDStyles();
    var t = global.document.createElement("div");
    t.className = "il-toast";
    t.textContent = msg;
    global.document.body.appendChild(t);
    requestAnimationFrame(function () {
      t.classList.add("is-on");
    });
    setTimeout(function () {
      t.classList.remove("is-on");
      setTimeout(function () {
        t.remove();
      }, 400);
    }, 2800);
  }

  function toastBadges(list) {
    list.forEach(function (b, i) {
      setTimeout(function () {
        toast("Badge unlocked · " + b.name);
      }, i * 400);
    });
  }

  function celebrateLevelUp(level) {
    toast("Level up · L" + level);
    if (reduced) return;
    confettiBurst();
    try {
      if (global.ILFx && typeof global.ILFx.hapticPulse === "function") {
        global.ILFx.hapticPulse();
      }
      if (global.ILFx && typeof global.ILFx.blip === "function") {
        global.ILFx.blip("level");
      }
    } catch (eH) {}
  }

  function confettiBurst() {
    ensureHUDStyles();
    var canvas = global.document.createElement("canvas");
    canvas.className = "il-confetti";
    canvas.width = global.innerWidth;
    canvas.height = global.innerHeight;
    global.document.body.appendChild(canvas);
    var ctx = canvas.getContext("2d");
    var colors = ["#5eead4", "#c9a227", "#e8eef5", "#38bdf8", "#f472b6"];
    var parts = [];
    var n = Math.min(90, Math.floor(global.innerWidth / 12));
    for (var i = 0; i < n; i++) {
      parts.push({
        x: global.innerWidth * 0.5 + (Math.random() - 0.5) * 80,
        y: global.innerHeight * 0.35,
        vx: (Math.random() - 0.5) * 14,
        vy: -Math.random() * 12 - 4,
        g: 0.28 + Math.random() * 0.12,
        r: 2 + Math.random() * 3,
        c: colors[(Math.random() * colors.length) | 0],
        life: 60 + ((Math.random() * 40) | 0),
      });
    }
    var frame = 0;
    function tick() {
      frame++;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      var alive = false;
      parts.forEach(function (p) {
        if (p.life <= 0) return;
        alive = true;
        p.life--;
        p.vy += p.g;
        p.x += p.vx;
        p.y += p.vy;
        ctx.globalAlpha = Math.max(0, p.life / 50);
        ctx.fillStyle = p.c;
        ctx.fillRect(p.x, p.y, p.r, p.r * 1.4);
      });
      if (alive && frame < 120) requestAnimationFrame(tick);
      else canvas.remove();
    }
    requestAnimationFrame(tick);
  }

  function renderBadges(host) {
    ensureHUDStyles();
    if (!host) return;
    var st = getState();
    host.classList.add("il-badge-row");
    host.innerHTML = BADGES.map(function (b) {
      var on = !!st.badgeDetail[b.id];
      return (
        '<div class="il-badge' +
        (on ? " is-on" : "") +
        '" title="' +
        b.blurb +
        '"><strong>' +
        b.name +
        "</strong><span>" +
        (on ? "Unlocked" : "Locked") +
        "</span></div>"
      );
    }).join("");
  }

  /* ---------- Quest board ---------- */

  function todaysQuests(s) {
    var d = today();
    if (s.questsDay !== d) {
      s.questsDay = d;
      s.quests = {};
      // pick 3 stable-ish by day hash
      var seed = 0;
      for (var i = 0; i < d.length; i++) seed = (seed * 31 + d.charCodeAt(i)) | 0;
      var idx = [];
      var pool = DAILY_QUESTS.slice();
      for (var k = 0; k < 3 && pool.length; k++) {
        seed = (seed * 1103515245 + 12345) | 0;
        var j = Math.abs(seed) % pool.length;
        idx.push(pool.splice(j, 1)[0]);
      }
      s.quests._ids = idx.map(function (q) {
        return q.id;
      });
      save(s);
    }
    var ids = (s.quests && s.quests._ids) || [];
    return DAILY_QUESTS.filter(function (q) {
      return ids.indexOf(q.id) >= 0;
    });
  }

  function mountQuestBoard(el) {
    if (!el) return;
    ensureHUDStyles();
    var s = load();
    var quests = todaysQuests(s);
    el.innerHTML = quests
      .map(function (q) {
        var done = !!(s.quests && s.quests[q.id]);
        return (
          '<article class="il-quest' +
          (done ? " is-done" : "") +
          '" data-quest="' +
          q.id +
          '">' +
          '<p class="font-mono text-[0.58rem] uppercase tracking-[0.18em] text-gold">Daily mission · +' +
          q.xp +
          " XP</p>" +
          "<h3 class=\"mt-1 font-display text-lg\">" +
          q.title +
          "</h3>" +
          '<p class="text-sm text-muted">' +
          q.hint +
          ' · <a class="text-cyan" href="' +
          q.href +
          '">Open</a></p>' +
          (done
            ? '<p class="font-mono text-[0.58rem] uppercase tracking-[0.14em] text-cyan">Claimed</p>'
            : '<button type="button" class="inline-flex h-9 items-center rounded-md bg-paper px-3 font-display text-[0.62rem] uppercase tracking-[0.14em] text-void" data-claim="' +
              q.id +
              '">Claim +' +
              q.xp +
              " XP</button>") +
          "</article>"
        );
      })
      .join("");

    el.querySelectorAll("[data-claim]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-claim");
        var s2 = load();
        if (s2.quests[id]) return;
        var q = DAILY_QUESTS.filter(function (x) {
          return x.id === id;
        })[0];
        if (!q) return;
        s2.quests[id] = Date.now();
        s2.questsClaimed = (s2.questsClaimed || 0) + 1;
        save(s2);
        award("quest_claim", q.xp, { id: id, once: true, label: q.title });
        mountQuestBoard(el);
      });
    });
  }

  /* ---------- Progress bridge ---------- */

  function bindProgress() {
    global.document.addEventListener("il:progress", function (ev) {
      var d = ev.detail || {};
      if (!d.on) return;
      var flag = null;
      if (d.scope === "founders" && d.id) flag = "founders_" + d.id;
      if (d.scope === "prep" && d.id) flag = "prep_" + d.id;
      award("checklist_tick", EVENT_XP.checklist_tick, {
        id: (d.scope || "") + ":" + (d.id || ""),
        once: true,
        flag: flag,
        label: d.id,
      });
    });

    // Path open: once per path slug per session/storage
    try {
      var path = global.location.pathname.replace(/\/+$/, "") || "/";
      if (
        path.indexOf("/paths/") === 0 ||
        path.indexOf("/prep/") === 0 ||
        path.indexOf("/learn") === 0 ||
        path.indexOf("/founders") === 0 ||
        path.indexOf("/labs/") === 0
      ) {
        award("path_open", EVENT_XP.path_open, {
          id: path,
          once: true,
          path: path,
          label: path,
        });
      }
    } catch (e) {}

    // Drill pages
    if (global.location.pathname.indexOf("/prep/drills/") === 0) {
      var mark = global.document.querySelector("[data-il-drill-complete]");
      if (mark) {
        mark.addEventListener("click", function () {
          award("drill_complete", EVENT_XP.drill_complete, {
            id: global.location.pathname,
            once: true,
          });
        });
      }
    }

    // Radar section visit awards soft XP once/day
    if (global.location.hash === "#radar" || global.document.getElementById("radar")) {
      /* deferred to intersection below via data attr */
    }
  }

  function boot() {
    ensureHUDStyles();
    var s = load();
    bumpStreak(s);
    save(s);
    award("daily_login", EVENT_XP.daily_login);
    renderHUD();
    bindProgress();

    global.document.querySelectorAll("[data-il-badges]").forEach(function (h) {
      renderBadges(h);
    });
    global.document.querySelectorAll("[data-il-quests]").forEach(function (h) {
      mountQuestBoard(h);
    });

    // Radar update when radar section enters view (once/day)
    var radar = global.document.getElementById("radar");
    if (radar && "IntersectionObserver" in global) {
      var seen = false;
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (en) {
            if (!en.isIntersecting || seen) return;
            seen = true;
            award("radar_update", EVENT_XP.radar_update, {
              id: "radar:" + today(),
              once: true,
            });
            io.disconnect();
          });
        },
        { threshold: 0.35 }
      );
      io.observe(radar);
    }

    paintAll();
  }

  global.ILGame = {
    STORAGE_KEY: STORAGE_KEY,
    EVENT_XP: EVENT_XP,
    BADGES: BADGES,
    award: award,
    getState: getState,
    renderHUD: renderHUD,
    renderBadges: renderBadges,
    mountQuestBoard: mountQuestBoard,
    celebrate: celebrateLevelUp,
    confetti: confettiBurst,
    xpForLevel: xpForLevel,
    progressInLevel: function () {
      return progressInLevel(load());
    },
  };

  if (global.document && global.document.readyState === "loading") {
    global.document.addEventListener("DOMContentLoaded", boot);
  } else if (global.document) {
    boot();
  }
})(typeof window !== "undefined" ? window : this);
;

/* ---- source: assets/il-motion.js (12896 bytes) ---- */
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
    var dpr = Math.min(global.devicePixelRatio || 1, 1.5);

    function resize() {
      var rect = host.getBoundingClientRect();
      w = Math.max(1, Math.floor(rect.width));
      h = Math.max(1, Math.floor(rect.height));
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var count = Math.min(220, Math.max(70, Math.floor((w * h) / 9000)));
      stars = [];
      for (var i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * w,
          y: Math.random() * h,
          z: 0.2 + Math.random() * 0.8,
          r: 0.55 + Math.random() * 1.8,
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
        var a = 0.4 + 0.6 * (0.5 + 0.5 * Math.sin(s.tw));
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
      g.addColorStop(0, "rgba(94,234,212,0.09)");
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
    // Full-viewport aurora/starfield is owned by il-fx.js (Musk-bar).
    // Section hosts get a static vignette only — no second canvas (5k-wide perf).
    qs("[data-il-starfield], .il-hero-field", root).forEach(function (host) {
      if (host.getAttribute("data-il-starfield-ready")) return;
      host.setAttribute("data-il-starfield-ready", "1");
      host.classList.add("il-hero-field");
      if (!host.querySelector(".il-hero-vignette")) {
        var v = global.document.createElement("div");
        v.className = "il-hero-vignette";
        v.setAttribute("aria-hidden", "true");
        v.style.cssText =
          "position:absolute;inset:0;pointer-events:none;" +
          "background:radial-gradient(ellipse at 68% 28%,rgba(126,212,224,0.10),transparent 58%)," +
          "radial-gradient(ellipse at 18% 78%,rgba(198,165,114,0.07),transparent 52%);";
        host.appendChild(v);
      }
    });
  }

  /* ---------- Magnetic buttons (rAF-throttled, fine pointers only) ---------- */
  var finePointer =
    !global.matchMedia || global.matchMedia("(pointer: fine)").matches;
  function initMagnetic(root) {
    if (reduced || !finePointer) return;
    var nodes = qs(".il-magnetic, [data-il-magnetic]", root);
    nodes.forEach(function (el) {
      if (el.getAttribute("data-il-mag-ready")) return;
      el.setAttribute("data-il-mag-ready", "1");
      el.classList.add("il-magnetic");
      var strength = parseFloat(el.getAttribute("data-il-magnetic") || "10") || 10;
      var raf = 0;
      var px = 0;
      var py = 0;
      function apply() {
        raf = 0;
        el.style.setProperty("--mx", px.toFixed(2) + "px");
        el.style.setProperty("--my", py.toFixed(2) + "px");
      }
      el.addEventListener("pointermove", function (e) {
        if (e.pointerType === "touch" || e.pointerType === "pen") return;
        var r = el.getBoundingClientRect();
        px = ((e.clientX - r.left) / r.width - 0.5) * strength;
        py = ((e.clientY - r.top) / r.height - 0.5) * strength;
        if (!raf) raf = global.requestAnimationFrame(apply);
      });
      el.addEventListener("pointerleave", function () {
        if (raf) {
          global.cancelAnimationFrame(raf);
          raf = 0;
        }
        px = 0;
        py = 0;
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
      "#why-interstitium .rounded-xl, .il-diff-strip .rounded-xl, [data-il-auto-reveal] .rounded-xl, [data-il-auto-reveal] .il-surface, main .rounded-xl.bg-panel, main .il-surface, section .rounded-xl.bg-panel",
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

  
  /* FX INJECT 20260922 */
  function ensureHeroFX(root) {
    var heroes = qs("section.relative.isolate, section.relative.overflow-hidden, .il-hero-uw", root);
    if (!heroes.length) {
      var main = (root || global.document).querySelector("main") || (root || global.document).body;
      if (main) {
        var host = global.document.createElement("div");
        host.className = "il-hero-field";
        host.setAttribute("data-il-starfield", "");
        host.setAttribute("aria-hidden", "true");
        host.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:0;opacity:0.55;";
        if (main.firstChild) main.insertBefore(host, main.firstChild);
        else main.appendChild(host);
      }
      return;
    }
    for (var i = 0; i < Math.min(heroes.length, 2); i++) {
      var sec = heroes[i];
      if (!sec.querySelector(".il-hero-field, [data-il-starfield]")) {
        var h = global.document.createElement("div");
        h.className = "il-hero-field";
        h.setAttribute("data-il-starfield", "");
        h.setAttribute("aria-hidden", "true");
        sec.insertBefore(h, sec.firstChild);
      }
      if (!sec.getAttribute("data-il-auto-reveal")) sec.setAttribute("data-il-auto-reveal", "");
    }
  }

  /* ---------- Cinematic hero video: reduced-motion + offscreen pause ---------- */
  function initHeroVideo(root) {
    var vids = qs(".il-hero__video", root);
    if (!vids.length) return;
    vids.forEach(function (v) {
      if (reduced) {
        v.removeAttribute("autoplay");
        v.pause();
        return; /* poster frame remains as the still */
      }
      if ("IntersectionObserver" in global) {
        var io = new IntersectionObserver(
          function (entries) {
            entries.forEach(function (en) {
              if (en.isIntersecting) {
                if (v.paused) v.play().catch(function () {});
              } else v.pause();
            });
          },
          { threshold: 0.05 }
        );
        io.observe(v);
      }
    });
  }

  function boot() {
    var root = global.document;
    autoTag(root);
    ensureHeroFX(root);
    initReveal(root);
    initAllStarfields(root);
    initMagnetic(root);
    initCounters(root);
    initHeroVideo(root);
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
;

/* ---- source: assets/il-pwa.js (1032 bytes) ---- */
/**
 * Interstitium Labs — service worker RETIRED (2026-10-01).
 * The offline worker poisoned mobile caches and broke rendering during
 * hiring-manager audits. This script now unregisters any service worker
 * and deletes every cache, then stays out of the way. The page always
 * loads fresh from the network. PWA re-introduction (if ever) will be
 * deliberate, versioned, and fail-open.
 */
(function (global) {
  "use strict";
  try {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker
        .getRegistrations()
        .then(function (regs) {
          regs.forEach(function (r) {
            try { r.unregister(); } catch (_) {}
          });
        })
        .catch(function () {});
    }
    if ("caches" in global) {
      caches
        .keys()
        .then(function (keys) {
          keys.forEach(function (k) {
            try { caches.delete(k); } catch (_) {}
          });
        })
        .catch(function () {});
    }
  } catch (_) {}
})(typeof window !== "undefined" ? window : this);
;

/* ---- source: analytics/config.js (604 bytes) ---- */
/**
 * First-party analytics config (public, client-side).
 *
 * HONEST STATUS: endpoint is null until Enmanuel pastes a Cloudflare Worker /
 * Analytics Engine ingest URL. Local ring buffer always works (`il.analytics.v1`).
 *
 * Cloudflare Web Analytics: set cloudflareBeaconToken from
 * Cloudflare → Web Analytics → Manage site. Leave null to skip (no fake tokens).
 * See /ops/ANALYTICS.md
 */
window.IL_ANALYTICS = {
  endpoint: null, // e.g. "https://analytics.interstitiumlabs.dev/ingest"
  cloudflareBeaconToken: null, // paste real token only
  sampleRate: 1,
  maxBuffer: 400,
  version: 1
};
;

/* ---- source: assets/il-analytics.js (7723 bytes) ---- */
/**
 * Interstitium Labs — privacy-friendly first-party analytics
 * API: ILAnalytics.track(name, props)
 * Ring buffer: localStorage `il.analytics.v1`
 * Optional beacon: docs/analytics/config.js → endpoint
 * A/B: localStorage `il.exp.v1`
 */
(function (global) {
  "use strict";

  var BUF_KEY = "il.analytics.v1";
  var EXP_KEY = "il.exp.v1";
  var cfg = global.IL_ANALYTICS || {};
  var maxBuffer = cfg.maxBuffer || 400;
  var sampleRate = typeof cfg.sampleRate === "number" ? cfg.sampleRate : 1;

  function readBuf() {
    try {
      var raw = global.localStorage.getItem(BUF_KEY);
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function writeBuf(arr) {
    try {
      global.localStorage.setItem(BUF_KEY, JSON.stringify(arr.slice(-maxBuffer)));
    } catch (e) {}
  }

  function pagePath() {
    try { return global.location.pathname || "/"; } catch (e) { return "/"; }
  }

  function currentLang() {
    try {
      if (global.ILi18n && typeof global.ILi18n.getLang === "function") return global.ILi18n.getLang();
      return global.localStorage.getItem("il.lang") ||
        (global.document.documentElement && global.document.documentElement.lang) || "en";
    } catch (e) { return "en"; }
  }

  function beacon(evt) {
    var endpoint = cfg.endpoint;
    if (!endpoint) return;
    var body = JSON.stringify(evt);
    try {
      if (global.navigator && typeof global.navigator.sendBeacon === "function") {
        global.navigator.sendBeacon(endpoint, new Blob([body], { type: "application/json" }));
        return;
      }
    } catch (e) {}
    try {
      fetch(endpoint, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: body,
        keepalive: true,
        mode: "cors",
        credentials: "omit"
      }).catch(function () {});
    } catch (e2) {}
  }

  function track(name, props) {
    if (!name) return null;
    if (sampleRate < 1 && Math.random() > sampleRate) return null;
    var evt = {
      n: String(name),
      t: Date.now(),
      p: pagePath(),
      lang: currentLang(),
      props: props && typeof props === "object" ? props : {}
    };
    var buf = readBuf();
    buf.push(evt);
    writeBuf(buf);
    beacon(evt);
    try {
      global.document.dispatchEvent(new CustomEvent("il:analytics", { detail: evt }));
    } catch (e) {}
    return evt;
  }

  function getBuffer() { return readBuf(); }
  function clearBuffer() {
    try { global.localStorage.removeItem(BUF_KEY); } catch (e) {}
  }

  function getExperiments() {
    try {
      var raw = global.localStorage.getItem(EXP_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) { return {}; }
  }

  function assignVariant(expId, variants) {
    var list = variants && variants.length ? variants : ["A", "B"];
    var store = getExperiments();
    if (store[expId] && list.indexOf(store[expId]) >= 0) return store[expId];
    var pick = list[Math.floor(Math.random() * list.length)];
    store[expId] = pick;
    try { global.localStorage.setItem(EXP_KEY, JSON.stringify(store)); } catch (e) {}
    track("exp_assign", { exp: expId, variant: pick });
    return pick;
  }

  function applyCTAExperiments() {
    var prepVar = assignVariant("cta_prep_copy", ["A", "B"]);
    var enrollVar = assignVariant("cta_enroll_copy", ["A", "B"]);
    var prepNodes = global.document.querySelectorAll('[data-il-exp="cta_prep_copy"]');
    for (var i = 0; i < prepNodes.length; i++) {
      prepNodes[i].setAttribute("data-il-variant", prepVar);
      if (prepVar === "B" && prepNodes[i].childElementCount === 0) {
        prepNodes[i].textContent = prepNodes[i].getAttribute("data-il-exp-b") || "Crush Prep";
      }
    }
    var enNodes = global.document.querySelectorAll('[data-il-exp="cta_enroll_copy"]');
    for (var j = 0; j < enNodes.length; j++) {
      enNodes[j].setAttribute("data-il-variant", enrollVar);
      if (enrollVar === "B" && enNodes[j].childElementCount === 0) {
        enNodes[j].textContent = enNodes[j].getAttribute("data-il-exp-b") || "Join the cohort";
      }
    }
  }

  function bindAuto() {
    global.document.addEventListener("click", function (e) {
      var t = e.target;
      if (!t || !t.closest) return;
      var el = t.closest("[data-il-track], a[href]");
      if (!el) return;
      var href = el.getAttribute("href") || "";
      var explicit = el.getAttribute("data-il-track");
      var name = explicit;
      if (!name) {
        if (/\/enroll\/?/.test(href)) name = "enroll_click";
        else if (/\/paths\//.test(href) || href === "/paths/" || href === "/paths") name = "path_open";
        else if (el.classList.contains("il-cta") || el.hasAttribute("data-il-exp")) name = "cta_click";
        else if (/\/(prep|learn|play|founders|about)\//.test(href) && el.closest("main")) name = "cta_click";
        else return;
      }
      track(name, {
        href: href,
        id: el.id || null,
        exp: el.getAttribute("data-il-exp") || null,
        variant: el.getAttribute("data-il-variant") || null,
        text: (el.textContent || "").trim().slice(0, 80)
      });
    }, true);

    global.document.addEventListener("change", function (e) {
      var el = e.target;
      if (!el || el.type !== "checkbox") return;
      if (el.hasAttribute("data-il-progress") || el.closest(".check-row") || el.closest("[data-il-checklist]")) {
        track("checklist_tick", {
          id: el.id || el.getAttribute("data-il-progress") || null,
          checked: !!el.checked
        });
      }
    }, true);

    global.document.addEventListener("il:game", function (ev) {
      var d = (ev && ev.detail) || {};
      if (d.type === "quest_claim" || d.event === "quest_claim") track("quest_claim", d);
      if (d.type === "level_up" || d.event === "hud_level_up" || d.leveled) track("hud_level_up", d);
    });

    // Bridge lang picker
    global.document.addEventListener("il:lang", function (ev) {
      var d = (ev && ev.detail) || {};
      track("lang_select", { lang: d.lang || currentLang() });
    });
  }

  function detectFriction() {
    try {
      var k = "il.analytics.reload";
      var arr = JSON.parse(global.sessionStorage.getItem(k) || "[]");
      var t = Date.now();
      arr = arr.filter(function (x) { return t - x < 60000; });
      arr.push(t);
      global.sessionStorage.setItem(k, JSON.stringify(arr));
      if (arr.length >= 4) track("friction_reload", { count: arr.length, windowMs: 60000 });
    } catch (e) {}
  }

  function maybeCloudflareBeacon() {
    var token = cfg.cloudflareBeaconToken;
    if (!token || /PASTE|PLACEHOLDER|null/i.test(String(token))) return;
    if (global.document.getElementById("il-cf-wa")) return;
    var s = global.document.createElement("script");
    s.id = "il-cf-wa";
    s.defer = true;
    s.src = "https://static.cloudflareinsights.com/beacon.min.js";
    s.setAttribute("data-cf-beacon", JSON.stringify({ token: token }));
    (global.document.head || global.document.documentElement).appendChild(s);
  }

  function boot() {
    track("page_view", {
      title: global.document.title || "",
      ref: (global.document.referrer || "").slice(0, 200)
    });
    bindAuto();
    applyCTAExperiments();
    detectFriction();
    maybeCloudflareBeacon();
  }

  global.ILAnalytics = {
    track: track,
    getBuffer: getBuffer,
    clearBuffer: clearBuffer,
    assignVariant: assignVariant,
    getExperiments: getExperiments
  };

  if (global.document.readyState === "loading") {
    global.document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})(typeof window !== "undefined" ? window : this);
;

/* ---- source: assets/il-i18n.js (23919 bytes) ---- */
/**
 * Interstitium Labs — first-party i18n (privacy-first, Musk-practical)
 *
 * Detection priority:
 * 1) localStorage `il.lang` (picker override)
 * 2) navigator.languages / Accept-Language
 * 3) Geo hint: CF-IPCountry (optional inject) + Intl timezone → region default
 * 4) Fallback `en`
 *
 * Never forces geo over a strong browser language preference.
 */
(function (global) {
  "use strict";

  var STORAGE_KEY = "il.lang";
  var BASE = "/i18n/";
  var CACHE_V = "20260924";
  var RTL = { ar: 1, he: 1, fa: 1, ur: 1 };

  var LOCALES = [
    { code: "en", name: "English", completeness: "full" },
    { code: "es", name: "Español", completeness: "full" },
    { code: "pt-BR", name: "Português (BR)", completeness: "chrome" },
    { code: "fr", name: "Français", completeness: "chrome" },
    { code: "de", name: "Deutsch", completeness: "chrome" },
    { code: "zh-CN", name: "简体中文", completeness: "chrome" },
    { code: "ja", name: "日本語", completeness: "chrome" },
    { code: "ko", name: "한국어", completeness: "chrome" },
    { code: "hi", name: "हिन्दी", completeness: "chrome" },
    { code: "ar", name: "العربية", completeness: "chrome" }
  ];

  var TZ_DEFAULT = {
    "America/Santo_Domingo": "es",
    "America/Mexico_City": "es",
    "America/Bogota": "es",
    "America/Lima": "es",
    "America/Santiago": "es",
    "America/Buenos_Aires": "es",
    "America/Argentina/Buenos_Aires": "es",
    "America/Caracas": "es",
    "America/Guayaquil": "es",
    "America/La_Paz": "es",
    "America/Asuncion": "es",
    "America/Montevideo": "es",
    "America/Havana": "es",
    "America/Puerto_Rico": "es",
    "America/Panama": "es",
    "America/Costa_Rica": "es",
    "America/Guatemala": "es",
    "America/Sao_Paulo": "pt-BR",
    "America/Fortaleza": "pt-BR",
    "America/Recife": "pt-BR",
    "America/Manaus": "pt-BR",
    "America/Belem": "pt-BR",
    "Europe/Madrid": "es",
    "Europe/Paris": "fr",
    "Europe/Berlin": "de",
    "Europe/Rome": "it",
    "Europe/Lisbon": "pt-BR",
    "Asia/Shanghai": "zh-CN",
    "Asia/Chongqing": "zh-CN",
    "Asia/Hong_Kong": "zh-CN",
    "Asia/Taipei": "zh-CN",
    "Asia/Tokyo": "ja",
    "Asia/Seoul": "ko",
    "Asia/Kolkata": "hi",
    "Asia/Calcutta": "hi",
    "Asia/Dubai": "ar",
    "Asia/Riyadh": "ar",
    "Africa/Cairo": "ar",
    "Africa/Casablanca": "ar"
  };

  var CF_COUNTRY_LANG = {
    MX: "es", ES: "es", AR: "es", CO: "es", CL: "es", PE: "es", VE: "es",
    DO: "es", PR: "es", EC: "es", GT: "es", CR: "es", PA: "es", UY: "es",
    PY: "es", BO: "es", HN: "es", SV: "es", NI: "es", CU: "es",
    BR: "pt-BR", PT: "pt-BR",
    FR: "fr", BE: "fr",
    DE: "de", AT: "de", CH: "de",
    CN: "zh-CN", TW: "zh-CN", HK: "zh-CN", SG: "zh-CN",
    JP: "ja", KR: "ko", IN: "hi",
    SA: "ar", AE: "ar", EG: "ar", MA: "ar", QA: "ar", KW: "ar"
  };

  var catalog = {};
  var bodyMap = {};
  var bodyApplying = false;
  var current = "en";
  var completeness = "full";
  var ready = false;

  var INLINE_OK = {
    CODE: 1, EM: 1, STRONG: 1, B: 1, I: 1, SPAN: 1, A: 1, BR: 1,
    SMALL: 1, KBD: 1, ABBR: 1, MARK: 1, SUB: 1, SUP: 1, WBR: 1
  };
  var SKIP_TAGS = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, SVG: 1, CODE: 1, PRE: 1, KBD: 1, SAMP: 1, TEXTAREA: 1 };

  function supportedCodes() {
    return LOCALES.map(function (l) { return l.code; });
  }

  function normalize(tag) {
    if (!tag) return null;
    var t = String(tag).replace(/_/g, "-").trim();
    if (!t) return null;
    var lower = t.toLowerCase();
    var codes = supportedCodes();
    for (var i = 0; i < codes.length; i++) {
      if (codes[i].toLowerCase() === lower) return codes[i];
    }
    var base = lower.split("-")[0];
    if (base === "pt") return "pt-BR";
    if (base === "zh") return "zh-CN";
    for (var j = 0; j < codes.length; j++) {
      if (codes[j].toLowerCase().split("-")[0] === base) return codes[j];
    }
    return null;
  }

  function browserLangs() {
    var list = [];
    try {
      if (global.navigator && global.navigator.languages) {
        list = Array.prototype.slice.call(global.navigator.languages);
      } else if (global.navigator && global.navigator.language) {
        list = [global.navigator.language];
      }
    } catch (e) {}
    return list;
  }

  function strongBrowserPref() {
    var langs = browserLangs();
    for (var i = 0; i < langs.length; i++) {
      var n = normalize(langs[i]);
      if (n) return n;
    }
    return null;
  }

  function timezoneHint() {
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      if (tz && TZ_DEFAULT[tz]) return TZ_DEFAULT[tz];
      if (tz && tz.indexOf("America/") === 0) {
        // Generic Americas without explicit mapping: do not force Spanish over EN
        return null;
      }
    } catch (e) {}
    return null;
  }

  function cfCountryHint() {
    var c = null;
    try {
      if (global.IL_CF_COUNTRY) c = String(global.IL_CF_COUNTRY).toUpperCase();
      if (!c && global.document) {
        var meta = global.document.querySelector('meta[name="cf-ipcountry"]');
        if (meta) c = String(meta.getAttribute("content") || "").toUpperCase();
      }
    } catch (e) {}
    if (c && CF_COUNTRY_LANG[c]) return CF_COUNTRY_LANG[c];
    return null;
  }

  /**
   * Resolve locale. Geo never overrides a strong browser language when they conflict.
   * Example: en-US browser in Mexico → en.
   */
  function detect() {
    try {
      var stored = global.localStorage && global.localStorage.getItem(STORAGE_KEY);
      var fromStore = normalize(stored);
      if (fromStore) return { lang: fromStore, source: "storage" };
    } catch (e) {}

    var browser = strongBrowserPref();
    var geo = cfCountryHint() || timezoneHint();

    if (browser) {
      // Soft geo: only fill when browser is English AND geo suggests a local tongue?
      // Spec: never force geo over explicit browser preference when they conflict strongly.
      // So if browser resolved to anything, keep it.
      return { lang: browser, source: "browser", geoHint: geo || null };
    }

    if (geo) return { lang: geo, source: "geo" };
    return { lang: "en", source: "fallback" };
  }

  function t(key, fallback) {
    if (!key) return fallback || "";
    if (catalog && Object.prototype.hasOwnProperty.call(catalog, key) && catalog[key] != null) {
      return String(catalog[key]);
    }
    return fallback != null ? String(fallback) : key;
  }

  function setDir(lang) {
    var html = global.document.documentElement;
    var dir = RTL[lang] || RTL[lang.split("-")[0]] ? "rtl" : "ltr";
    html.setAttribute("lang", lang);
    html.setAttribute("dir", dir);
  }

  function sanitizeInline(html) {
    var tpl = global.document.createElement("template");
    tpl.innerHTML = String(html);
    function walk(node) {
      var kids = Array.prototype.slice.call(node.childNodes);
      for (var i = 0; i < kids.length; i++) {
        var ch = kids[i];
        if (ch.nodeType !== 1) continue;
        if (!INLINE_OK[ch.tagName]) {
          node.replaceChild(global.document.createTextNode(ch.textContent || ""), ch);
          continue;
        }
        var attrs = Array.prototype.slice.call(ch.attributes);
        for (var a = 0; a < attrs.length; a++) {
          var n = attrs[a].name.toLowerCase();
          var v = attrs[a].value || "";
          if (n.indexOf("on") === 0 || n === "srcdoc" || n === "style") {
            ch.removeAttribute(attrs[a].name);
            continue;
          }
          if ((n === "href" || n === "src") && !/^(\/|https?:|#|mailto:)/i.test(v)) {
            ch.removeAttribute(attrs[a].name);
          }
        }
        walk(ch);
      }
    }
    walk(tpl.content);
    return tpl.innerHTML;
  }

  function writeTranslation(el, val) {
    var slot = el.querySelector("[data-i18n-text]");
    if (el.childElementCount && slot) {
      slot.textContent = val;
      return;
    }
    if (/<[a-z]/i.test(val)) {
      el.innerHTML = sanitizeInline(val);
      return;
    }
    el.textContent = val;
  }

  function lookupBody(text) {
    if (!text || current === "en") return null;
    var key = String(text).replace(/\s+/g, " ").trim();
    if (!key || !Object.prototype.hasOwnProperty.call(bodyMap, key)) return null;
    var v = bodyMap[key];
    if (v == null || v === key) return null;
    return String(v);
  }

  function inSkipped(el) {
    while (el) {
      if (el.nodeType === 1) {
        if (SKIP_TAGS[el.tagName]) return true;
        if (el.getAttribute && (el.getAttribute("translate") === "no" || el.hasAttribute("data-i18n") || el.hasAttribute("data-il-no-body"))) return true;
      }
      el = el.parentElement || el.parentNode;
    }
    return false;
  }

  function applyBodyText(node) {
    if (!node || node.nodeType !== 3 || inSkipped(node.parentElement)) return;
    if (node.__ilOrig == null) node.__ilOrig = node.nodeValue;
    var orig = node.__ilOrig;
    var match = orig.match(/^(\s*)([\s\S]*?)(\s*)$/);
    if (!match) return;
    var core = match[2].replace(/\s+/g, " ").trim();
    var translated = lookupBody(core);
    var next = translated ? (match[1] + translated + match[3]) : orig;
    if (node.nodeValue !== next) node.nodeValue = next;
  }

  function applyBodyAttrs(el) {
    if (!el || el.nodeType !== 1 || SKIP_TAGS[el.tagName]) return;
    if (el.getAttribute("translate") === "no" || el.hasAttribute("data-il-no-body")) return;
    var names = ["aria-label", "title", "placeholder", "alt"];
    for (var i = 0; i < names.length; i++) {
      var name = names[i];
      if (!el.hasAttribute(name)) continue;
      var store = "data-il-orig-" + name;
      if (!el.hasAttribute(store)) el.setAttribute(store, el.getAttribute(name) || "");
      var orig = el.getAttribute(store) || "";
      var translated = lookupBody(orig);
      var next = translated || orig;
      if (el.getAttribute(name) !== next) el.setAttribute(name, next);
    }
    if (el.tagName === "META") {
      var prop = (el.getAttribute("property") || el.getAttribute("name") || "").toLowerCase();
      if (prop === "description" || prop === "og:description" || prop === "og:title" || prop === "twitter:title" || prop === "twitter:description") {
        if (!el.hasAttribute("data-il-orig-content")) el.setAttribute("data-il-orig-content", el.getAttribute("content") || "");
        var oc = el.getAttribute("data-il-orig-content") || "";
        var tv = lookupBody(oc);
        var nc = tv || oc;
        if (el.getAttribute("content") !== nc) el.setAttribute("content", nc);
      }
    }
  }

  function applyBody(root) {
    if (!global.document || !global.document.documentElement) return;
    bodyApplying = true;
    try {
      var scope = root || global.document.documentElement;
      if (scope.nodeType === 1) applyBodyAttrs(scope);
      var walker = global.document.createTreeWalker(scope, 5 /* SHOW_ELEMENT | SHOW_TEXT */, null);
      var n = walker.nextNode();
      while (n) {
        if (n.nodeType === 3) applyBodyText(n);
        else applyBodyAttrs(n);
        n = walker.nextNode();
      }
    } finally {
      bodyApplying = false;
    }
  }

  function loadBody(lang) {
    if (!lang || lang === "en") {
      bodyMap = {};
      return Promise.resolve(bodyMap);
    }
    return fetch(BASE + lang + ".body.json?v=" + CACHE_V, { credentials: "same-origin", cache: "no-cache" })
      .then(function (res) {
        if (!res.ok) throw new Error("i18n body " + lang);
        return res.json();
      })
      .then(function (json) {
        bodyMap = json && typeof json === "object" ? json : {};
        return bodyMap;
      })
      .catch(function () {
        bodyMap = {};
        return bodyMap;
      });
  }

  function applyAttrs(root) {
    var scope = root || global.document;
    var nodes = scope.querySelectorAll("[data-i18n]");
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var key = el.getAttribute("data-i18n");
      if (!key) continue;
      var val = t(key, el.getAttribute("data-i18n-fallback") || el.textContent);
      writeTranslation(el, val);
    }
    var attrs = scope.querySelectorAll("[data-i18n-attr]");
    for (var j = 0; j < attrs.length; j++) {
      var ael = attrs[j];
      var spec = ael.getAttribute("data-i18n-attr") || "";
      // format: "placeholder:nav.search|aria-label:nav.aria"
      var parts = spec.split("|");
      for (var k = 0; k < parts.length; k++) {
        var pair = parts[k].split(":");
        if (pair.length < 2) continue;
        var attr = pair[0].trim();
        var akey = pair.slice(1).join(":").trim();
        ael.setAttribute(attr, t(akey, ael.getAttribute(attr) || ""));
      }
    }
  }

  function injectHreflang() {
    if (!global.document || !global.document.head) return;
    var canonical = global.document.querySelector('link[rel="canonical"]');
    var href = canonical ? canonical.getAttribute("href") : global.location.href.split("?")[0];
    if (!href) return;
    // Remove prior IL hreflang
    var old = global.document.querySelectorAll('link[data-il-hreflang]');
    for (var i = 0; i < old.length; i++) old[i].parentNode.removeChild(old[i]);
    var codes = supportedCodes();
    for (var j = 0; j < codes.length; j++) {
      var link = global.document.createElement("link");
      link.rel = "alternate";
      link.hreflang = codes[j];
      link.href = href + (href.indexOf("?") >= 0 ? "&" : "?") + "lang=" + encodeURIComponent(codes[j]);
      link.setAttribute("data-il-hreflang", "1");
      global.document.head.appendChild(link);
    }
    var xdef = global.document.createElement("link");
    xdef.rel = "alternate";
    xdef.hreflang = "x-default";
    xdef.href = href;
    xdef.setAttribute("data-il-hreflang", "1");
    global.document.head.appendChild(xdef);
  }

  function showScaffoldNote() {
    if (completeness === "full") {
      var existing = global.document.getElementById("il-i18n-scaffold-note");
      if (existing) existing.parentNode.removeChild(existing);
      return;
    }
    var main = global.document.querySelector("main") || global.document.body;
    if (!main) return;
    var note = global.document.getElementById("il-i18n-scaffold-note");
    if (!note) {
      note = global.document.createElement("div");
      note.id = "il-i18n-scaffold-note";
      note.className = "il-i18n-note no-print";
      note.setAttribute("role", "status");
      if (main.firstChild) main.insertBefore(note, main.firstChild);
      else main.appendChild(note);
    }
    note.innerHTML = "";
    var span = global.document.createElement("span");
    span.textContent = t("i18n.scaffold_note", "Original EN · translating… chrome is localized; long-form may still be English.");
    note.appendChild(span);
    var btn = global.document.createElement("button");
    btn.type = "button";
    btn.textContent = t("i18n.browser_translate", "Use browser translate");
    btn.addEventListener("click", function () {
      try {
        global.alert(t("i18n.browser_translate_help", "Use your browser menu: Translate page. Chrome/Edge: right-click → Translate."));
      } catch (e) {}
    });
    note.appendChild(btn);
  }

  function closeMenus() {
    var menus = global.document.querySelectorAll(".il-lang-menu.is-open");
    for (var i = 0; i < menus.length; i++) menus[i].classList.remove("is-open");
  }

  function mountSwitcher(host) {
    if (!host || host.getAttribute("data-il-lang-mounted")) return;
    host.setAttribute("data-il-lang-mounted", "1");
    host.classList.add("il-lang");

    var btn = global.document.createElement("button");
    btn.type = "button";
    btn.className = "il-lang-btn";
    btn.setAttribute("aria-haspopup", "listbox");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-label", t("nav.language", "Language"));
    btn.innerHTML =
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 3 2.5 15 0 18M12 3c-2.5 3-2.5 15 0 18"/></svg>' +
      '<span data-il-lang-code>' + current + "</span>";

    var menu = global.document.createElement("div");
    menu.className = "il-lang-menu";
    menu.setAttribute("role", "listbox");

    LOCALES.forEach(function (loc) {
      var opt = global.document.createElement("button");
      opt.type = "button";
      opt.setAttribute("role", "option");
      if (loc.code === current) opt.setAttribute("aria-current", "true");
      opt.innerHTML =
        "<span>" + loc.name + '</span><span class="il-lang-meta">' +
        (loc.completeness === "full" ? "full" : "chrome") + "</span>";
      opt.addEventListener("click", function () {
        setLang(loc.code, true);
        closeMenus();
        btn.setAttribute("aria-expanded", "false");
      });
      menu.appendChild(opt);
    });

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !menu.classList.contains("is-open");
      closeMenus();
      if (open) {
        menu.classList.add("is-open");
        btn.setAttribute("aria-expanded", "true");
      } else {
        btn.setAttribute("aria-expanded", "false");
      }
    });

    host.appendChild(btn);
    host.appendChild(menu);
  }

  function ensureSwitcherHosts() {
    var hosts = global.document.querySelectorAll("[data-il-lang-switcher]");
    if (hosts.length) {
      for (var i = 0; i < hosts.length; i++) mountSwitcher(hosts[i]);
      return;
    }
    // Auto-inject into header / footer when missing
    var headerRow = global.document.querySelector("header .mx-auto.flex");
    if (headerRow && !headerRow.querySelector("[data-il-lang-switcher]")) {
      var slot = global.document.createElement("div");
      slot.setAttribute("data-il-lang-switcher", "");
      slot.className = "no-print";
      // Prefer placing before the mobile CTA (last child often)
      headerRow.appendChild(slot);
      mountSwitcher(slot);
    }
    var footer = global.document.querySelector("footer .mx-auto");
    if (footer && !footer.querySelector("[data-il-lang-switcher]")) {
      var fslot = global.document.createElement("div");
      fslot.setAttribute("data-il-lang-switcher", "");
      fslot.className = "no-print";
      footer.appendChild(fslot);
      mountSwitcher(fslot);
    }
  }

  function refreshSwitcherLabels() {
    var codes = global.document.querySelectorAll("[data-il-lang-code]");
    for (var i = 0; i < codes.length; i++) codes[i].textContent = current;
    var opts = global.document.querySelectorAll(".il-lang-menu [role=\"option\"]");
    for (var j = 0; j < opts.length; j++) {
      var meta = opts[j].querySelector(".il-lang-meta");
      var codeGuess = null;
      // Match by LOCALES order
      if (LOCALES[j]) {
        if (LOCALES[j].code === current) opts[j].setAttribute("aria-current", "true");
        else opts[j].removeAttribute("aria-current");
      }
    }
    // Sync any native <select aria-label=Language> leftovers
    var selects = global.document.querySelectorAll('select[aria-label="Language"], select[data-il-lang-select]');
    for (var s = 0; s < selects.length; s++) {
      try { selects[s].value = current; } catch (e) {}
    }
  }

  function wireNativeSelects() {
    var selects = global.document.querySelectorAll('select[aria-label="Language"], select[data-il-lang-select]');
    for (var i = 0; i < selects.length; i++) {
      var sel = selects[i];
      if (sel.getAttribute("data-il-lang-wired")) continue;
      sel.setAttribute("data-il-lang-wired", "1");
      sel.setAttribute("data-il-lang-select", "");
      // Replace dead SPA option values (zh, pt, …) with supported codes where possible
      sel.addEventListener("change", function (ev) {
        var v = ev.target.value;
        var map = { zh: "zh-CN", pt: "pt-BR", "pt-br": "pt-BR", "zh-cn": "zh-CN" };
        var mapped = map[String(v).toLowerCase()] || v;
        setLang(mapped, true);
      });
    }
  }

  function loadCatalog(lang) {
    return fetch(BASE + lang + ".json?v=" + CACHE_V, { credentials: "same-origin", cache: "no-cache" })
      .then(function (res) {
        if (!res.ok) throw new Error("i18n " + lang);
        return res.json();
      })
      .then(function (json) {
        catalog = json || {};
        completeness = catalog._meta && catalog._meta.completeness
          ? catalog._meta.completeness
          : (lang === "en" || lang === "es" ? "full" : "chrome");
        return catalog;
      });
  }

  function setLang(lang, persist) {
    var n = normalize(lang) || "en";
    current = n;
    if (persist) {
      try {
        global.localStorage.setItem(STORAGE_KEY, n);
      } catch (e) {}
      try {
        if (global.ILAnalytics && typeof global.ILAnalytics.track === "function") {
          global.ILAnalytics.track("lang_select", { lang: n });
        }
      } catch (e2) {}
    }
    setDir(n);
    return loadCatalog(n)
      .catch(function () {
        if (n !== "en") return loadCatalog("en").then(function () {
          current = "en";
          setDir("en");
        });
        catalog = {};
        completeness = "full";
      })
      .then(function () { return loadBody(current); })
      .then(function () {
        applyAttrs(global.document);
        applyBody(global.document);
        showScaffoldNote();
        ensureSwitcherHosts();
        wireNativeSelects();
        refreshSwitcherLabels();
        injectHreflang();
        ready = true;
        try {
          global.document.dispatchEvent(new CustomEvent("il:i18n", { detail: { lang: current, completeness: completeness } }));
          global.document.dispatchEvent(new CustomEvent("il:lang", { detail: { lang: current } }));
        } catch (e) {}
        return current;
      });
  }

  function queryLang() {
    try {
      var q = new URLSearchParams(global.location.search).get("lang");
      return normalize(q);
    } catch (e) {
      return null;
    }
  }

  function boot() {
    // Optional one-line CF country: window.IL_CF_COUNTRY from Worker
    var q = queryLang();
    var detected = detect();
    var lang = q || detected.lang;
    if (q) {
      try { global.localStorage.setItem(STORAGE_KEY, q); } catch (e) {}
    }
    global.document.addEventListener("click", function () { closeMenus(); });
    setLang(lang, false).then(function () {
      // Expose detection for admin insights
      try {
        global.sessionStorage.setItem("il.lang.detect", JSON.stringify(detected));
      } catch (e) {}
    });
    if (global.MutationObserver && global.document.documentElement) {
      var pending = 0;
      var obs = new global.MutationObserver(function () {
        if (bodyApplying || current === "en") return;
        if (pending) return;
        pending = global.setTimeout(function () {
          pending = 0;
          if (!bodyApplying && current !== "en") applyBody(global.document);
        }, 30);
      });
      var target = global.document.documentElement;
      var startObs = function () {
        try {
          obs.observe(target, {
            subtree: true,
            childList: true,
            characterData: true,
            attributes: true,
            attributeFilter: ["aria-label", "title", "placeholder", "alt", "content"]
          });
        } catch (e) {}
      };
      if (global.document.body) startObs();
      else global.document.addEventListener("DOMContentLoaded", startObs);
    }
  }

  var api = {
    t: t,
    setLang: setLang,
    getLang: function () { return current; },
    detect: detect,
    apply: applyAttrs,
    applyBody: applyBody,
    locales: LOCALES.slice(),
    ready: function () { return ready; },
    completeness: function () { return completeness; }
  };

  global.ILi18n = api;

  if (global.document.readyState === "loading") {
    global.document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})(typeof window !== "undefined" ? window : this);
;

/* ---- source: assets/il-coach.js (17290 bytes) ---- */
/**
 * Noah Live Assist — local Socratic in-lab coach. NO fake API keys.
 * Exceeds hosted AI-tutor live assist on honesty: lab-context prompts, no spoiler dumps,
 * demand-tier OSS router (Ollama) when present, 3D curriculum stages stay separate.
 * Optional: window.IL_COACH / IL_MUSE / IL_MODEL_ROUTER (never commit secrets).
 * Topics: CIDR, Git, K8s pods (+ Terraform, CI, Linux) + lab-paste triage.
 */
(function (g) {
  'use strict';

  var TOPICS = [
    { id: 'cidr', label: 'CIDR' },
    { id: 'git', label: 'Git' },
    { id: 'k8s', label: 'K8s pods' },
    { id: 'terraform', label: 'Terraform' },
    { id: 'ci', label: 'CI/CD' },
    { id: 'linux', label: 'Linux' }
  ];

  function labContext(el) {
    var ctx = {
      surface: '',
      challenge: '',
      scene: '',
      mode: 'coach'
    };
    try {
      var path = (g.location && g.location.pathname) || '';
      if (path.indexOf('/labs/challenge') === 0) ctx.surface = 'challenge';
      else if (path.indexOf('/labs') === 0) ctx.surface = 'labs';
      else if (path.indexOf('/coach') === 0) ctx.surface = 'coach';
      else if (path.indexOf('/prep') === 0) ctx.surface = 'prep';
      var host = el || (g.document && g.document.querySelector('[data-il-live-assist], [data-il-coach]'));
      if (host) {
        ctx.challenge = host.getAttribute('data-il-lab-challenge') || '';
        ctx.scene = host.getAttribute('data-il-lab-scene') || '';
        if (host.getAttribute('data-il-live-assist') != null) ctx.mode = 'live-assist';
      }
      var ch = g.document && g.document.querySelector('[data-il-challenge-id], [data-challenge]');
      if (ch && !ctx.challenge) {
        ctx.challenge = ch.getAttribute('data-il-challenge-id') || ch.getAttribute('data-challenge') || '';
      }
    } catch (e) {}
    return ctx;
  }

  function liveAssistPreface(ctx) {
    var bits = ['Noah Live Assist'];
    if (ctx.surface) bits.push(ctx.surface);
    if (ctx.challenge) bits.push('challenge ' + ctx.challenge);
    if (ctx.scene) bits.push('scene ' + ctx.scene);
    return bits.join(' · ') + ' — Socratic, lab-context, no spoiler dump. Paste an error or hypothesis.';
  }

  var RULES = [
    // meta
    { re: /(answer|just tell me|give me the (answer|solution)|solve it for me)/i, topic: null,
      reply: 'I will not dump the answer. What have you already tried? Name one observation (error text, command output, or hypothesis).' },
    // Live Assist — lab paste / terminal triage (still Socratic)
    { re: /(error:|Traceback|E\d{4}|ImagePullBackOff|CrashLoopBackOff|ErrImagePull|CreateContainerConfigError)/i, topic: null,
      reply: 'Live Assist triage: quote the *first* failing line only. What command or apply produced it? Do not paste secrets. What did you expect to happen instead?' },
    { re: /(kubectl\s+(apply|get|describe|logs)|helm\s+|argocd\s+|terraform\s+)/i, topic: 'k8s',
      reply: 'Live Assist: name the resource kind + namespace (no cluster credentials). Is the failure at apply-time validation, schedule, or runtime? One hypothesis before I nudge the next check.' },
    { re: /(micro-?lesson|on-?demand|explain this lab|what should I do next)/i, topic: null,
      reply: 'Micro-lesson mode: I will not narrate the whole lab. Pick one concept (CIDR, probes, selectors, state lock, pipeline stage). What have you already verified?' },

    { re: /^(hi|hello|hey)\b/i, topic: null,
      reply: 'Welcome. Ask about CIDR, Git, K8s, blockchain, quantum, deep work, or Linux. I stay Socratic for coaching — factual questions get direct answers from the site\u2019s curriculum.' },
    // CIDR
    { re: /(cidr|subnet|\/2[0-9]|netmask|usable hosts?)/i, topic: 'cidr',
      reply: 'CIDR check: (1) How many host bits remain? (2) What are network vs broadcast? (3) Are you designing for hosts or for routes? Reply with your prefix and intended host count.' },
    { re: /(overlap|supernet|longest\s*prefix)/i, topic: 'cidr',
      reply: 'Overlap thinking: draw both ranges as bit prefixes. Does one contain the other? Routers pick longest prefix match — which prefix is more specific?' },
    // Git
    { re: /(detached|head|rebase|merge conflict|force.?push)/i, topic: 'git',
      reply: 'Git: Is the commit published to a shared branch? If yes, avoid history rewrites. If no, what named branch should hold this work? Paste the status line you care about (redact secrets).' },
    { re: /(cherry-?pick|revert|reset)/i, topic: 'git',
      reply: 'Choose the tool by intent: undo on a public branch → usually revert. Discard local only → reset. Replay a commit elsewhere → cherry-pick. Which intent is yours?' },
    // K8s
    { re: /(crashloop|pending|imagepull|readiness|liveness|pod)/i, topic: 'k8s',
      reply: 'Pod triage order: describe events → logs (--previous if restarting) → probes/resources/image. Which phase is the Pod in right now, and what does the last event say?' },
    { re: /(service|clusterip|endpoint|selector)/i, topic: 'k8s',
      reply: 'Service path: do labels on the Pod match spec.selector? Do Endpoints populate? From inside the cluster, can you curl the ClusterIP? Where does the chain break?' },
    // Terraform
    { re: /(terraform|state|plan|apply|drift)/i, topic: 'terraform',
      reply: 'Terraform: Is state remote and locked? Did plan show destroy you did not expect? Never apply a surprise destroy in shared state — quote the resource address that worries you.' },
    // CI
    { re: /(jenkins|github actions|pipeline|ci\/?cd|workflow)/i, topic: 'ci',
      reply: 'CI: Is the failure at lint, unit, build, push, or deploy? Separate “test red” from “secrets/registry auth”. Which stage failed first?' },
    // Blockchain (site carries a full ledger-engineering track)
    { re: /(blockchain|bitcoin|ethereum|solidity|smart contract|utxo|monero|stellar|xrpl|ledger)/i, topic: 'blockchain',
      reply: 'Ledger first: which layer is your question on — the protocol (consensus, UTXO/account model), the cryptography (hashes, signatures), or the application (contracts, wallets)? Name the layer, then state your hypothesis.' },
    // Quantum
    { re: /(quantum|qubit|superposition|entanglement)/i, topic: 'quantum',
      reply: 'Quantum: are you asking about the physics, an algorithm (Shor, Grover), or the engineering of qubits? Write the smallest state involved — what operation are you uncertain about?' },
    // Study method (Cal Newport content now on site)
    { re: /(deep work|procrastinat|study plan|time block|focus)/i, topic: 'study',
      reply: 'Study method: are you stuck on attention, retention, or pacing? Name one 90-minute distraction-free session you could run this week — same time, same place, phone elsewhere. What would it cover?' },
    // Zero Trust / IL-11 (honest: no such track exists on the site)
    { re: /(il-?11|zero.?trust)/i, topic: null,
      reply: 'Honest correction: there is no IL-11 Zero Trust track on this site — the name matches no published academy or path. The real Zero Trust material lives in two labs: the K8s CKA network-policies lab (default-deny-all, explicit allow rules) and the Security+/CySA+ microsegmentation lab. Which one do you want to work through, and what is your first hypothesis about it?' },
    // Career
    { re: /(interview|resume|job application|career|salary|hiring)/i, topic: 'career',
      reply: 'Career: are you optimizing the application, the interview, or the offer? Name your single strongest proof of work — a shipped project beats a claimed skill. What is yours?' },
    // Linux
    { re: /(linux|systemd|journalctl|chmod|ssh|disk|oom)/i, topic: 'linux',
      reply: 'Linux: What is the symptom — exit code, service status, or resource pressure? Check unit status / journal / df / free before changing configs. What command output do you have?' }
  ];

  var FALLBACK = 'I only have local rule-based coaching right now (AI model hookup pending). Ask about CIDR, Git, K8s pods, Terraform, CI/CD, Linux, blockchain, quantum, or study method — or ask any factual question and I will answer it from the site\u2019s curriculum on-device.';

  function config() {
    return g.IL_COACH || {};
  }

  function socratic(text, topic) {
    var cfg = config();
    /* NOTE (2026-10-01, noah-recovery-2): socratic() must NEVER delegate back to
       IL_MODEL_ROUTER.chat(). socratic IS the router's local-rules backend
       (il-model-router.js: localRulesReply -> ILCoach.ask -> socratic), so calling
       router.chat() from in here ping-pongs forever: router -> localRulesReply ->
       socratic -> router -> ... Each hop schedules more microtasks, the microtask
       queue never drains, and the renderer goes terminally unresponsive on the very
       first send (reproduced: 680k+ router.chat calls in 20s, timers starved).
       The old "prefer router" branch could only fire after the router had already
       selected the local-rules backend, so it could never have reached a real model
       anyway — removing it loses nothing. Real model backends (Ollama / OpenAI-
       compat) are still selected directly by the router's own selectModel(). */
    // Legacy: endpoint set without router — honesty stub (CSP + key safety).
    if (cfg.endpoint) {
      var lr2 = asReply(localReply(text, topic));
      return Promise.resolve({
        text: 'IL_COACH.endpoint is set, but load il-model-router.js (or a same-origin Worker proxy) before enabling remote chat. Meanwhile: ' + lr2.text,
        source: 'stub-remote'
      });
    }
    return Promise.resolve(asReply(localReply(text, topic)));
  }

  /* localReply returns a string for Socratic rules, or {text, source} for the
     knowledge-bundle branch. Normalize before handing to the chat shell. */
  function asReply(r) {
    if (r && typeof r === 'object' && typeof r.text === 'string') {
      return { text: r.text, source: r.source || 'local-rules' };
    }
    return { text: String(r), source: 'local-rules' };
  }

  function localReply(text, topic) {
    for (var i = 0; i < RULES.length; i++) {
      var r = RULES[i];
      if (r.re.test(text) && (!r.topic || !topic || r.topic === topic || topic === r.topic)) {
        return r.reply;
      }
    }
    if (topic) {
      var topical = RULES.filter(function (r) { return r.topic === topic; });
      if (topical.length) return topical[0].reply + ' Your question: “' + String(text).slice(0, 120) + '”';
    }
    /* On-device knowledge bundle: direct grounded answers when no Socratic rule
       fires. Socratic stays the coach doctrine; the bundle answers factual
       "tell me about X" questions from the site's real curriculum. Plain text
       only — the coach chat renders escaped bubbles, no markdown. */
    try {
      var kbApi = g.__ilNoahKB;
      if (kbApi && kbApi.get && kbApi.answer && kbApi.get()) {
        var hit = kbApi.answer(text);
        if (hit && hit.entry) {
          var plain = String(hit.reply)
            .replace(/\[([^\]]+)\]\((\/[^)]+)\)/g, '$1 ($2)')
            .replace(/\*\*/g, '');
          return { text: plain + '\n\nWant to go Socratic on it? State your first hypothesis and we will reason from there.', source: 'kb-local' };
        }
      }
    } catch (e) { /* bundle unreachable — Socratic fallback below */ }
    return FALLBACK;
  }

  function mount(el) {
    if (el.getAttribute('data-il-coach-ready')) return;
    var topic = el.getAttribute('data-il-coach-topic') || '';
    var ctx = labContext(el);
    var live = ctx.mode === 'live-assist' || el.getAttribute('data-il-live-assist') != null;

    var shell = document.createElement('div');
    shell.className = 'il-coach-shell' + (live ? ' il-coach-shell--live-assist' : '');

    var left = document.createElement('div');
    left.className = 'il-ux-card il-ux-card--quiet';
    left.innerHTML =
      '<span class="il-coach-status"><span class="il-coach-status__dot" aria-hidden="true"></span> ' + (live ? 'Noah Live Assist · online (local)' : 'Noah · Socratic coach') + '</span>' +
      '<h2 class="mt-4 font-display text-2xl tracking-[-0.02em]" style="margin-top:1rem;font-family:Space Grotesk,system-ui,sans-serif;font-size:1.5rem;color:#e8eef5">' + (live ? 'Live Assist in the lab' : 'Local Socratic hints') + '</h2>' +
      '<p style="margin-top:0.75rem;font-size:0.875rem;color:#8b9bb4;line-height:1.55">' + (live
        ? 'Real-time <em>in-lab</em> help without a leading platform\'s hosted fleet claim. Paste an error or hypothesis. On-demand micro-lessons stay Socratic — no spoiler dump. Demand-tier OSS router when Ollama is present. No fake keys.'
        : 'No API keys in this repo. Optional <code style="color:#5eead4">window.IL_COACH</code> stub for a future same-origin proxy. I ask questions; I do not dump final answers.') + '</p>' +
      '<p class="il-kicker" style="margin-top:1.25rem">Topics</p>';
    var topics = document.createElement('div');
    topics.className = 'il-coach-topics';
    topics.style.marginTop = '0.75rem';
    TOPICS.forEach(function (t) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'il-coach-topic' + (topic === t.id ? ' is-on' : '');
      b.textContent = t.label;
      b.addEventListener('click', function () {
        topic = t.id;
        Array.prototype.forEach.call(topics.children, function (c) { c.classList.remove('is-on'); });
        b.classList.add('is-on');
        push('bot', 'Topic set to ' + t.label + '. What are you stuck on? One sentence on what you already tried.');
      });
      topics.appendChild(b);
    });
    left.appendChild(topics);
    left.insertAdjacentHTML('beforeend',
      '<p class="il-honest-note" style="margin-top:1.25rem"><strong>Honesty vs hosted live assist:</strong> We ship Socratic lab-context coaching + optional local Ollama router. We do <em>not</em> claim a hosted multi-cloud playground fleet or terminal keylogger. SuperLab is cloneable proof; paste your own lab state.</p>');

    var right = document.createElement('div');
    right.className = 'il-ux-card';
    var log = document.createElement('div');
    log.className = 'il-coach-log';
    log.setAttribute('role', 'log');
    log.setAttribute('aria-live', 'polite');
    var form = document.createElement('form');
    form.className = 'il-coach-form';
    form.setAttribute('autocomplete', 'off');
    var input = document.createElement('input');
    input.type = 'text';
    input.name = 'q';
    input.placeholder = 'Ask a stuck question (not “just give the answer”)…';
    input.setAttribute('aria-label', 'Coach question');
    var send = document.createElement('button');
    send.type = 'submit';
    send.textContent = 'Ask';
    form.appendChild(input);
    form.appendChild(send);
    right.appendChild(log);
    right.appendChild(form);

    function push(who, text) {
      var m = document.createElement('div');
      m.className = 'il-coach-msg il-coach-msg--' + who;
      m.textContent = text;
      log.appendChild(m);
      log.scrollTop = log.scrollHeight;
    }

    function ask(q) {
      q = (q || '').trim();
      if (!q) return;
      push('user', q);
      input.value = '';
      send.disabled = true;
      socratic(q, topic).then(function (res) {
        push('bot', res.text);
        send.disabled = false;
        input.focus();
        try {
          if (g.ILGame && g.ILGame.award) g.ILGame.award('coach_ask', 5, { id: 'coach:' + Date.now() });
        } catch (e) {}
      });
    }

    push('bot', live ? liveAssistPreface(ctx) : 'Interstitium Coach (local rules). Topics: CIDR, Git, K8s, Terraform, CI/CD, Linux. I will not answer-dump — show your work.');

    /* ?prompt= deep links (exam remediation, side-quests): prefill the input
       AND start the Socratic session with it, so the link actually does something. */
    try {
      var qp = (g.location && g.location.search) ? g.location.search.replace(/^\?/, '').split('&') : [];
      var promptQ = '';
      for (var pi = 0; pi < qp.length; pi++) {
        var kv = qp[pi].split('=');
        if (decodeURIComponent(kv[0] || '') === 'prompt') { promptQ = decodeURIComponent((kv[1] || '').replace(/\+/g, ' ')); break; }
      }
      if (promptQ) {
        input.value = promptQ;
        ask(promptQ);
        /* consume the param so back/forward doesn't re-fire the session */
        try { g.history.replaceState(null, '', g.location.pathname + g.location.hash); } catch (e2) {}
      }
    } catch (e3) {}

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var q = (input.value || '').trim();
      if (!q) return;
      ask(q);
    });

    shell.appendChild(left);
    shell.appendChild(right);
    el.innerHTML = '';
    el.appendChild(shell);
    el.setAttribute('data-il-coach-ready', '1');
  }

  function boot() {
    var nodes = document.querySelectorAll('[data-il-coach], [data-il-live-assist]');
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
  }

  g.ILCoach = { mount: mount, boot: boot, ask: socratic, topics: TOPICS,
    labContext: labContext, liveAssistPreface: liveAssistPreface,
    usesRouter: function () { return !!(g.IL_MODEL_ROUTER || g.ILModelRouter); } };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
;

/* ---- source: assets/il-model-router.js (33679 bytes) ---- */
/**
 * IL Model Router — local-first OSS backends + demand-tier scaling for Noah / Coach.
 *
 * Product policy: scale relative to demand (T0 → T1 → T2). Auto-switch only among
 * models that are currently healthy/online. Never pretend a 70B is local GPU.
 *
 * API: selectModel({task, forceId}), chat(messages), healthCheck(),
 *      setPolicy({mode, primary, challengers}), recommend()
 *
 * Storage: localStorage il.model.router.v1 (policy), il.model.creds.v1 (base URL + key only)
 * Catalog: /assets/il-model-catalog.json
 * Never commit secrets. Optional window.IL_MUSE / IL_COACH / IL_LLM_BASE hooks.
 */
(function (g) {
  'use strict';

  var POLICY_KEY = 'il.model.router.v1';
  var CREDS_KEY = 'il.model.creds.v1';
  var HEALTH_KEY = 'il.model.health.v1';
  var CATALOG_URL = '/assets/il-model-catalog.json';
  var DEFAULT_TIMEOUT_MS = 45000;
  var HEALTH_TTL_MS = 60000;

  var catalogCache = null;
  var catalogPromise = null;

  function cfg() {
    return g.IL_MODEL_ROUTER_CFG || g.IL_MODEL_ROUTER || g.IL_MUSE || g.IL_COACH || {};
  }

  function readJSON(key, fallback) {
    try {
      var raw = g.localStorage.getItem(key);
      if (!raw) return fallback;
      var parsed = JSON.parse(raw);
      return parsed && typeof parsed === 'object' ? parsed : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function writeJSON(key, val) {
    try { g.localStorage.setItem(key, JSON.stringify(val)); } catch (e) {}
  }

  function defaultPolicy(cat) {
    var d = (cat && cat.defaults) || {};
    var r = d.routing || {};
    return {
      v: 1,
      mode: r.mode || 'auto',
      primary: 'qwen2.5-coder-3b',
      challengers: ['phi-3-mini', 'qwen2.5-coder-7b'],
      demand_tier: d.demand_tier || 'T0',
      hardware_profile: d.hardware_profile || 'p920-p1000-4gb',
      backend: 'ollama',
      healthy_only: r.healthy_only !== false,
      min_samples: r.min_samples || 8,
      win_rate_margin: r.win_rate_margin || 0.08,
      latency_slack_ms: r.latency_slack_ms || 1500,
      explore_ratio: r.explore_ratio || 0.2,
      updatedAt: Date.now()
    };
  }

  function getPolicy() {
    var p = readJSON(POLICY_KEY, null);
    if (p && p.v === 1) return p;
    return defaultPolicy(catalogCache);
  }

  function setPolicy( partial ) {
    var cur = getPolicy();
    if (!partial || typeof partial !== 'object') return cur;
    if (partial.mode === 'auto' || partial.mode === 'manual') cur.mode = partial.mode;
    if (partial.primary) cur.primary = String(partial.primary);
    if (Array.isArray(partial.challengers)) cur.challengers = partial.challengers.slice();
    if (partial.demand_tier) cur.demand_tier = String(partial.demand_tier);
    if (partial.hardware_profile) cur.hardware_profile = String(partial.hardware_profile);
    if (partial.backend) cur.backend = String(partial.backend);
    if (typeof partial.healthy_only === 'boolean') cur.healthy_only = partial.healthy_only;
    if (typeof partial.min_samples === 'number') cur.min_samples = partial.min_samples;
    if (typeof partial.win_rate_margin === 'number') cur.win_rate_margin = partial.win_rate_margin;
    if (typeof partial.latency_slack_ms === 'number') cur.latency_slack_ms = partial.latency_slack_ms;
    if (typeof partial.explore_ratio === 'number') cur.explore_ratio = partial.explore_ratio;
    cur.updatedAt = Date.now();
    writeJSON(POLICY_KEY, cur);
    syncMuseHook(cur);
    return cur;
  }

  function getCreds() {
    return readJSON(CREDS_KEY, { bases: {}, keys: {} });
  }

  function setCreds(backendId, baseUrl, apiKey) {
    var c = getCreds();
    c.bases = c.bases || {};
    c.keys = c.keys || {};
    if (baseUrl != null) {
      if (baseUrl) c.bases[backendId] = String(baseUrl).replace(/\/$/, '');
      else delete c.bases[backendId];
    }
    if (apiKey != null) {
      if (apiKey) c.keys[backendId] = String(apiKey);
      else delete c.keys[backendId];
    }
    writeJSON(CREDS_KEY, c);
    return c;
  }

  function loadCatalog() {
    if (catalogCache) return Promise.resolve(catalogCache);
    if (catalogPromise) return catalogPromise;
    var embedded = g.IL_MODEL_CATALOG;
    if (embedded && embedded.models) {
      catalogCache = embedded;
      return Promise.resolve(catalogCache);
    }
    catalogPromise = fetch(CATALOG_URL, { credentials: 'omit' })
      .then(function (r) {
        if (!r.ok) throw new Error('catalog HTTP ' + r.status);
        return r.json();
      })
      .then(function (j) {
        catalogCache = j;
        catalogPromise = null;
        return j;
      })
      .catch(function (err) {
        catalogPromise = null;
        catalogCache = minimalCatalog();
        return catalogCache;
      });
    return catalogPromise;
  }

  function minimalCatalog() {
    return {
      version: 0,
      demand_tiers: {
        T0: { id: 'T0', label: 'Local P920', next_tier: 'T1', models_gpu: ['local-rules'], models_cpu: [] }
      },
      defaults: { demand_tier: 'T0', base_urls: { ollama: 'http://127.0.0.1:11434' }, routing: { healthy_only: true } },
      backends: [{ id: 'ollama', kind: 'ollama' }, { id: 'local-rules', kind: 'local', always_on: true }],
      models: [{
        id: 'local-rules', family: 'rules', label: 'Local rules', size_b: 0,
        backends: ['local-rules'], tags: ['chat'], min_vram_gb: 0, always_healthy: true,
        demand_tiers: ['T0', 'T1', 'T2'], placement: 'local'
      }]
    };
  }

  function modelById(id) {
    var cat = catalogCache || minimalCatalog();
    var models = cat.models || [];
    for (var i = 0; i < models.length; i++) if (models[i].id === id) return models[i];
    return null;
  }

  function backendById(id) {
    var cat = catalogCache || minimalCatalog();
    var backends = cat.backends || [];
    for (var i = 0; i < backends.length; i++) if (backends[i].id === id) return backends[i];
    return null;
  }

  function tierOrder(t) {
    if (t === 'T2') return 2;
    if (t === 'T1') return 1;
    return 0;
  }

  function modelAllowedOnTier(m, tier) {
    if (!m) return false;
    if (m.always_healthy) return true;
    var tiers = m.demand_tiers || ['T0'];
    return tiers.indexOf(tier) >= 0;
  }

  function baseUrlFor(backendId) {
    var c = cfg();
    var creds = getCreds();
    if (c.IL_LLM_BASE || (typeof g.IL_LLM_BASE === 'string' && g.IL_LLM_BASE)) {
      // Global override for lab-control tunnel
      if (backendId === 'ollama' || backendId === (getPolicy().backend)) {
        return String(c.IL_LLM_BASE || g.IL_LLM_BASE).replace(/\/$/, '');
      }
    }
    if (c.endpoint && (backendId === 'openai-compat' || backendId === getPolicy().backend)) {
      return String(c.endpoint).replace(/\/$/, '');
    }
    if (c.ollamaEndpoint && backendId === 'ollama') {
      return String(c.ollamaEndpoint).replace(/\/$/, '');
    }
    if (creds.bases && creds.bases[backendId]) return creds.bases[backendId];
    var cat = catalogCache || minimalCatalog();
    var bases = (cat.defaults && cat.defaults.base_urls) || {};
    return bases[backendId] || '';
  }

  function apiKeyFor(backendId) {
    var creds = getCreds();
    if (creds.keys && creds.keys[backendId]) return creds.keys[backendId];
    var c = cfg();
    // Never invent keys; only pass if operator set on window (still not committed)
    if (c.apiKey && backendId === (getPolicy().backend || 'openai-compat')) return c.apiKey;
    return '';
  }

  function readHealth() {
    return readJSON(HEALTH_KEY, { checkedAt: 0, backends: {}, models: {} });
  }

  function writeHealth(h) {
    writeJSON(HEALTH_KEY, h);
    return h;
  }

  function isHealthy(modelId, backendId) {
    var m = modelById(modelId);
    if (m && m.always_healthy) return true;
    var h = readHealth();
    var now = Date.now();
    if (now - (h.checkedAt || 0) > HEALTH_TTL_MS * 3) {
      // Stale — treat unknown as unhealthy for auto-switch (policy healthy_only)
      if (getPolicy().healthy_only && modelId !== 'local-rules') return false;
    }
    if (backendId && h.backends && h.backends[backendId]) {
      if (!h.backends[backendId].ok) return false;
    }
    if (h.models && h.models[modelId]) return !!h.models[modelId].ok;
    // If backend ok but model not probed, allow explore only when not healthy_only
    if (!getPolicy().healthy_only && backendId && h.backends && h.backends[backendId] && h.backends[backendId].ok) {
      return true;
    }
    return modelId === 'local-rules';
  }

  function fetchWithTimeout(url, opts, ms) {
    var ctrl = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var t = null;
    opts = opts || {};
    if (ctrl) {
      opts = Object.assign({}, opts, { signal: ctrl.signal });
      t = setTimeout(function () { try { ctrl.abort(); } catch (e) {} }, ms || DEFAULT_TIMEOUT_MS);
    }
    return fetch(url, opts).then(function (r) {
      if (t) clearTimeout(t);
      return r;
    }, function (err) {
      if (t) clearTimeout(t);
      throw err;
    });
  }

  function healthCheck(opts) {
    opts = opts || {};
    return loadCatalog().then(function (cat) {
      var policy = getPolicy();
      var backends = cat.backends || [];
      var results = { checkedAt: Date.now(), backends: {}, models: {}, tier: policy.demand_tier };
      var jobs = [];

      backends.forEach(function (b) {
        if (b.kind === 'local' || b.always_on) {
          results.backends[b.id] = { ok: true, latencyMs: 0, kind: 'local' };
          return;
        }
        // Only probe backends allowed at current tier or below T2 remote when configured
        var tMin = b.tier_min || 'T0';
        if (tierOrder(tMin) > tierOrder(policy.demand_tier) && !baseUrlFor(b.id)) {
          results.backends[b.id] = { ok: false, reason: 'tier-skip', tier_min: tMin };
          return;
        }
        var ep = baseUrlFor(b.id);
        if (!ep) {
          results.backends[b.id] = { ok: false, reason: 'no-endpoint' };
          return;
        }
        jobs.push((function (backend, endpoint) {
          var t0 = Date.now();
          var url = backend.kind === 'ollama'
            ? endpoint + (backend.tags_path || '/api/tags')
            : endpoint.replace(/\/v1\/?$/, '/v1') + (backend.models_path || '/models');
          // openai path already includes /v1 often
          if (backend.kind === 'openai' && /\/v1$/.test(endpoint)) {
            url = endpoint + (backend.models_path || '/models');
          }
          var headers = {};
          var key = apiKeyFor(backend.id);
          if (key) headers.Authorization = 'Bearer ' + key;
          return fetchWithTimeout(url, { method: 'GET', headers: headers }, opts.timeoutMs || 5000)
            .then(function (res) {
              var entry = { ok: res.ok, status: res.status, latencyMs: Date.now() - t0 };
              results.backends[backend.id] = entry;
              if (res.ok && backend.kind === 'ollama') {
                return res.json().then(function (data) {
                  var names = {};
                  (data.models || []).forEach(function (m) {
                    if (m && m.name) names[m.name] = true;
                    if (m && m.model) names[m.model] = true;
                  });
                  (cat.models || []).forEach(function (cm) {
                    if ((cm.backends || []).indexOf(backend.id) < 0) return;
                    var pull = cm.ollama_pull || '';
                    var ok = !!(names[pull] || names[cm.id] || cm.always_healthy);
                    // Also match prefix (qwen2.5-coder:3b vs tags)
                    if (!ok && pull) {
                      Object.keys(names).forEach(function (n) {
                        if (n === pull || n.indexOf(pull.split(':')[0]) === 0) ok = true;
                      });
                    }
                    results.models[cm.id] = {
                      ok: ok,
                      backend: backend.id,
                      pull: pull
                    };
                  });
                  return entry;
                }).catch(function () { return entry; });
              }
              if (res.ok) {
                (cat.models || []).forEach(function (cm) {
                  if ((cm.backends || []).indexOf(backend.id) < 0) return;
                  if (!results.models[cm.id]) {
                    results.models[cm.id] = { ok: true, backend: backend.id, inferred: true };
                  }
                });
              }
              return entry;
            }, function (err) {
              results.backends[backend.id] = {
                ok: false,
                reason: err && err.message ? err.message : String(err),
                latencyMs: Date.now() - t0
              };
            });
        })(b, ep));
      });

      // local-rules always healthy
      results.models['local-rules'] = { ok: true, backend: 'local-rules' };

      return Promise.all(jobs).then(function () {
        writeHealth(results);
        if (g.ILAnalytics && g.ILAnalytics.track) {
          g.ILAnalytics.track('model_health_check', {
            tier: policy.demand_tier,
            backends: Object.keys(results.backends).filter(function (k) { return results.backends[k].ok; })
          });
        }
        return results;
      });
    });
  }

  function taskTags(task) {
    if (task === 'code') return ['code'];
    if (task === 'reason') return ['reason'];
    return ['chat'];
  }

  function scoreCandidate(m, task, policy) {
    var tags = m.tags || [];
    var want = taskTags(task);
    var tagScore = 0;
    want.forEach(function (t) { if (tags.indexOf(t) >= 0) tagScore += 2; });
    if (tags.indexOf('chat') >= 0) tagScore += 0.5;
    var sizePenalty = (m.size_b || 0) > 7 ? 1 : 0;
    var placementBonus = 0;
    if (m.placement === 'gpu' && policy.demand_tier === 'T0') placementBonus = 1;
    if (m.placement === 'cpu' && task === 'code' && (m.size_b || 0) >= 7) placementBonus = 0.5;
    return tagScore + placementBonus - sizePenalty;
  }

  /**
   * Select a model for a task. Auto mode explores challengers; only healthy+tier-allowed.
   */
  function selectModel(opts) {
    opts = opts || {};
    var policy = getPolicy();
    var task = opts.task || 'chat';
    if (opts.forceId) {
      var forced = modelById(opts.forceId);
      if (!forced) return { id: 'local-rules', reason: 'unknown-force', model: modelById('local-rules') };
      if (policy.healthy_only && !isHealthy(forced.id, pickBackend(forced))) {
        return {
          id: 'local-rules',
          reason: 'force-unhealthy',
          requested: opts.forceId,
          model: modelById('local-rules'),
          honesty: 'Refusing unhealthy/offline model; never pretend large local GPU.'
        };
      }
      return { id: forced.id, reason: 'force', model: forced, backend: pickBackend(forced) };
    }

    var cat = catalogCache || minimalCatalog();
    var tier = policy.demand_tier || 'T0';
    var pool = (cat.models || []).filter(function (m) {
      if (!modelAllowedOnTier(m, tier)) return false;
      if (m.id === 'local-rules') return true;
      // Honesty: forbid local GPU claims for huge models on P1000 profile
      var hp = (cat.hardware_profiles || {})[policy.hardware_profile];
      if (hp && hp.forbid_local_gpu && hp.forbid_local_gpu.indexOf(m.id) >= 0) return false;
      if (policy.healthy_only && !isHealthy(m.id, pickBackend(m))) return false;
      return true;
    });

    if (policy.mode === 'manual') {
      var primary = modelById(policy.primary);
      if (primary && pool.some(function (m) { return m.id === primary.id; })) {
        return { id: primary.id, reason: 'manual-primary', model: primary, backend: pickBackend(primary) };
      }
      var fallback = pool[0] || modelById('local-rules');
      return { id: fallback.id, reason: 'manual-fallback', model: fallback, backend: pickBackend(fallback) };
    }

    // auto: primary vs explore challenger
    var primaryId = policy.primary;
    var challengers = policy.challengers || [];
    var explore = Math.random() < (policy.explore_ratio || 0.2);
    var pickId = primaryId;
    var reason = 'auto-primary';
    if (explore && challengers.length) {
      var healthyCh = challengers.filter(function (id) {
        return pool.some(function (m) { return m.id === id; });
      });
      if (healthyCh.length) {
        pickId = healthyCh[Math.floor(Math.random() * healthyCh.length)];
        reason = 'auto-explore';
      }
    }
    var chosen = pool.filter(function (m) { return m.id === pickId; })[0];
    if (!chosen) {
      // Best score in pool
      pool.sort(function (a, b) { return scoreCandidate(b, task, policy) - scoreCandidate(a, task, policy); });
      chosen = pool[0] || modelById('local-rules');
      reason = 'auto-best-available';
    }
    return { id: chosen.id, reason: reason, model: chosen, backend: pickBackend(chosen), task: task };
  }

  function pickBackend(m) {
    if (!m) return 'local-rules';
    var policy = getPolicy();
    var preferred = policy.backend || 'ollama';
    var list = m.backends || [];
    if (list.indexOf(preferred) >= 0 && isHealthy(m.id, preferred)) return preferred;
    for (var i = 0; i < list.length; i++) {
      if (list[i] === 'local-rules') continue;
      if (!getPolicy().healthy_only || isHealthy(m.id, list[i]) || (readHealth().backends[list[i]] && readHealth().backends[list[i]].ok)) {
        if (baseUrlFor(list[i]) || list[i] === 'local-rules') return list[i];
      }
    }
    if (list.indexOf('local-rules') >= 0) return 'local-rules';
    return list[0] || 'local-rules';
  }

  function systemPrompt(ctx) {
    ctx = ctx || {};
    var lines = [
      'You are Noah / Interstitium Labs coach — Socratic DevOps tutor.',
      'Ask questions and give hints; never dump full exam answers.',
      'Topics: CIDR, Git, Kubernetes, Terraform, CI/CD, Linux.',
      'Hardware honesty: student lab may be P920 Quadro P1000 4GB — do not claim 70B local GPU.',
      'Scale policy: capacity grows relative to demand (T0 local → T1 CPU hosts → T2 remote OSS).'
    ];
    if (ctx.topic) lines.push('Topic focus: ' + ctx.topic + '.');
    if (ctx.tier) lines.push('Demand tier: ' + ctx.tier + '.');
    return lines.join('\n');
  }

  function localRulesReply(messages, ctx) {
    var last = '';
    for (var i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role === 'user') { last = messages[i].content || ''; break; }
    }
    var topic = (ctx && ctx.topic) || '';
    if (g.ILCoach && typeof g.ILCoach.ask === 'function') {
      return g.ILCoach.ask(last, topic).then(function (res) {
        return {
          text: res.text || String(res),
          source: 'local-rules',
          modelId: 'local-rules',
          backendId: 'local-rules',
          latencyMs: 0,
          demand_tier: getPolicy().demand_tier
        };
      });
    }
    return Promise.resolve({
      text: 'Local rules only (no healthy LLM). Ask CIDR/Git/K8s/Terraform/CI/Linux — share what you tried. Configure Ollama (T0) or scale per demand.',
      source: 'local-rules',
      modelId: 'local-rules',
      backendId: 'local-rules',
      latencyMs: 0,
      demand_tier: getPolicy().demand_tier
    });
  }

  function callOllama(ep, model, messages, ctx, timeoutMs) {
    var pull = model.ollama_pull || model.id;
    var params = model.default_params || {};
    var body = {
      model: pull,
      stream: false,
      messages: [{ role: 'system', content: systemPrompt(ctx) }].concat(messages),
      options: {
        temperature: params.temperature != null ? params.temperature : 0.3,
        num_predict: params.num_predict || 1024
      }
    };
    var t0 = Date.now();
    return fetchWithTimeout(ep + '/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }, timeoutMs).then(function (res) {
      if (!res.ok) throw new Error('Ollama HTTP ' + res.status);
      return res.json();
    }).then(function (data) {
      var text = (data.message && data.message.content) || data.response || '';
      return {
        text: text,
        source: 'ollama',
        backendId: 'ollama',
        modelId: model.id,
        latencyMs: Date.now() - t0,
        tokensApprox: Math.ceil(text.length / 4)
      };
    });
  }

  function callOpenAI(ep, backendId, model, messages, ctx, timeoutMs) {
    var url = /\/chat\/completions$/.test(ep) ? ep : ep.replace(/\/$/, '') + '/chat/completions';
    var params = model.default_params || {};
    var body = {
      model: model.ollama_pull || model.id,
      messages: [{ role: 'system', content: systemPrompt(ctx) }].concat(messages),
      temperature: params.temperature != null ? params.temperature : 0.3,
      max_tokens: params.num_predict || 1024
    };
    var headers = { 'Content-Type': 'application/json' };
    var key = apiKeyFor(backendId);
    if (key) headers.Authorization = 'Bearer ' + key;
    var t0 = Date.now();
    return fetchWithTimeout(url, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(body)
    }, timeoutMs).then(function (res) {
      if (!res.ok) throw new Error(backendId + ' HTTP ' + res.status);
      return res.json();
    }).then(function (data) {
      var text = '';
      if (data.choices && data.choices[0]) {
        var c = data.choices[0];
        text = (c.message && c.message.content) || c.text || '';
      }
      return {
        text: text,
        source: backendId,
        backendId: backendId,
        modelId: model.id,
        latencyMs: Date.now() - t0,
        tokensApprox: (data.usage && data.usage.total_tokens) || Math.ceil(text.length / 4)
      };
    });
  }

  function invoke(sel, messages, ctx) {
    var model = sel.model || modelById(sel.id);
    var backendId = sel.backend || pickBackend(model);
    var b = backendById(backendId);
    if (!model || model.id === 'local-rules' || !b || b.kind === 'local') {
      return localRulesReply(messages, ctx);
    }
    var ep = baseUrlFor(backendId);
    if (!ep) return localRulesReply(messages, ctx);
    if (b.kind === 'ollama') return callOllama(ep, model, messages, ctx, DEFAULT_TIMEOUT_MS);
    if (b.kind === 'openai') return callOpenAI(ep, backendId, model, messages, ctx, DEFAULT_TIMEOUT_MS);
    return localRulesReply(messages, ctx);
  }

  /* Fail-safe against circular backend delegation (2026-10-01, noah-recovery-2):
     a backend must never re-enter chat() unboundedly — the 2026-10-01 renderer
     hang was exactly such a ping-pong (router -> localRules -> ILCoach.ask ->
     router -> ...), starving the event loop on the first send. Normal use nests
     at most a couple of concurrent chats (multi-send while thinking); anything
     deeper is a bug, and it now fails safe with an honest local reply instead
     of hanging the page. */
  var CHAT_DEPTH = 0, CHAT_DEPTH_MAX = 8;
  function chatGuardReply() {
    return {
      text: 'Local rules only (recursion guard tripped — refusing to loop). Ask about CIDR, Git, K8s, Terraform, CI/CD, Linux, blockchain, or quantum, and share what you tried.',
      source: 'local-rules',
      modelId: 'local-rules',
      backendId: 'local-rules',
      latencyMs: 0,
      demand_tier: (getPolicy() || {}).demand_tier
    };
  }
  function chat(messages, ctx) {
    ctx = ctx || {};
    if (CHAT_DEPTH >= CHAT_DEPTH_MAX) return Promise.resolve(chatGuardReply());
    CHAT_DEPTH++;
    return loadCatalog().then(function () {
      var policy = getPolicy();
      ctx.tier = policy.demand_tier;
      var sel = selectModel({ task: ctx.task || ctx.taskType || 'chat', forceId: ctx.forceId });
      var t0 = Date.now();
      return invoke(sel, messages, ctx).then(function (res) {
        res.demand_tier = policy.demand_tier;
        res.selectReason = sel.reason;
        if (g.ILModelAnalytics && g.ILModelAnalytics.record) {
          g.ILModelAnalytics.record({
            modelId: res.modelId,
            backendId: res.backendId,
            latencyMs: res.latencyMs != null ? res.latencyMs : (Date.now() - t0),
            ok: true,
            task: ctx.task || 'chat',
            reason: sel.reason,
            demand_tier: policy.demand_tier
          });
        }
        maybePromote();
        maybeScaleSignal();
        return res;
      }, function (err) {
        if (g.ILModelAnalytics && g.ILModelAnalytics.record) {
          g.ILModelAnalytics.record({
            modelId: sel.id,
            backendId: sel.backend,
            latencyMs: Date.now() - t0,
            ok: false,
            error: err && err.message,
            task: ctx.task || 'chat',
            demand_tier: policy.demand_tier
          });
        }
        maybeScaleSignal();
        // Fallback to local rules — never invent a 70B
        return localRulesReply(messages, ctx).then(function (local) {
          local.fallbackFrom = sel.id;
          local.error = err && err.message;
          return local;
        });
      });
    }).then(function (res) { CHAT_DEPTH--; return res; },
            function (err) { CHAT_DEPTH--; throw err; });
  }

  function maybePromote() {
    var policy = getPolicy();
    if (policy.mode !== 'auto') return;
    if (!g.ILModelAnalytics || !g.ILModelAnalytics.shouldPromote) return;
    var decision = g.ILModelAnalytics.shouldPromote(policy);
    if (decision && decision.promote && decision.challenger) {
      // Only promote if challenger currently healthy
      if (policy.healthy_only && !isHealthy(decision.challenger)) return;
      var prev = policy.primary;
      setPolicy({
        primary: decision.challenger,
        challengers: unique([prev].concat((policy.challengers || []).filter(function (c) {
          return c !== decision.challenger;
        })))
      });
      if (g.ILAnalytics && g.ILAnalytics.track) {
        g.ILAnalytics.track('model_auto_switch', {
          from: prev,
          to: decision.challenger,
          winRate: decision.winRate,
          latencyMs: decision.latencyMs,
          demand_tier: policy.demand_tier
        });
      }
    }
  }

  function unique(arr) {
    var s = {};
    var out = [];
    arr.forEach(function (x) {
      if (!x || s[x]) return;
      s[x] = true;
      out.push(x);
    });
    return out;
  }

  function maybeScaleSignal() {
    if (!g.ILModelAnalytics || !g.ILModelAnalytics.scaleRecommendation) return;
    var rec = g.ILModelAnalytics.scaleRecommendation(getPolicy(), catalogCache);
    if (rec && rec.suggest_tier && g.ILAnalytics && g.ILAnalytics.track) {
      g.ILAnalytics.track('model_scale_recommend', rec);
    }
  }

  function recommend() {
    var policy = getPolicy();
    var analyticsRec = (g.ILModelAnalytics && g.ILModelAnalytics.recommend)
      ? g.ILModelAnalytics.recommend(policy)
      : null;
    var scale = (g.ILModelAnalytics && g.ILModelAnalytics.scaleRecommendation)
      ? g.ILModelAnalytics.scaleRecommendation(policy, catalogCache)
      : null;
    var sel = selectModel({ task: 'chat' });
    return {
      primary: policy.primary,
      selected: sel,
      demand_tier: policy.demand_tier,
      next_tier: scale && scale.suggest_tier,
      scale: scale,
      analytics: analyticsRec,
      honesty: 'Auto-switch only among healthy models on the current demand tier. Scale relative to demand — recommendations only, no auto-purchase.',
      health: readHealth()
    };
  }

  function syncMuseHook(policy) {
    try {
      g.IL_MUSE = g.IL_MUSE || {};
      g.IL_COACH = g.IL_COACH || {};
      var ep = baseUrlFor(policy.backend || 'ollama');
      if (ep) {
        if (!(g.IL_MUSE.endpoint)) g.IL_MUSE.endpoint = ep;
        g.IL_MUSE.modelRouter = true;
        g.IL_MUSE.demand_tier = policy.demand_tier;
      }
      g.IL_COACH.modelRouter = true;
    } catch (e) {}
  }

  function listModels() {
    return loadCatalog().then(function (cat) {
      return (cat.models || []).slice();
    });
  }

  function getDemandTiers() {
    return loadCatalog().then(function (cat) {
      return cat.demand_tiers || {};
    });
  }


  /* —— Muse executor compatibility (lean|standard|heavy ↔ T0|T1|T2) —— */
  var TIER_MAP = { lean: 'T0', standard: 'T1', heavy: 'T2', T0: 'T0', T1: 'T1', T2: 'T2' };
  var TIER_REV = { T0: 'lean', T1: 'standard', T2: 'heavy' };

  function normalizeTierId(id) {
    return TIER_MAP[id] || 'T0';
  }

  function endpointFor(backendId) { return baseUrlFor(backendId); }
  function setEndpoint(backendId, url) { return setCreds(backendId, url, null); }

  function load() {
    var p = getPolicy();
    var creds = getCreds();
    return {
      v: 1,
      profileId: p.hardware_profile,
      primary: { backendId: p.backend || 'ollama', modelId: p.primary },
      override: p.mode === 'manual' ? { backendId: p.backend || 'ollama', modelId: p.primary } : null,
      order: [p.backend || 'ollama', 'local-rules'],
      endpoints: creds.bases || {},
      enabled: {},
      autoSwitch: p.mode === 'auto',
      demandTier: TIER_REV[p.demand_tier] || 'lean',
      demand_tier: p.demand_tier,
      updatedAt: p.updatedAt
    };
  }

  function save(s) {
    if (!s) return getPolicy();
    var partial = {};
    if (s.autoSwitch != null) partial.mode = s.autoSwitch ? 'auto' : 'manual';
    if (s.primary && s.primary.modelId) {
      partial.primary = s.primary.modelId;
      if (s.primary.backendId) partial.backend = s.primary.backendId;
    }
    if (s.demandTier) partial.demand_tier = normalizeTierId(s.demandTier);
    if (s.demand_tier) partial.demand_tier = normalizeTierId(s.demand_tier);
    if (s.endpoints) {
      Object.keys(s.endpoints).forEach(function (k) { setCreds(k, s.endpoints[k], null); });
    }
    setPolicy(partial);
    return load();
  }

  function activeTarget() {
    var p = getPolicy();
    var m = modelById(p.primary) || modelById('local-rules');
    return { backendId: pickBackend(m), modelId: m ? m.id : 'local-rules' };
  }

  function catalog() {
    var cat = catalogCache || minimalCatalog();
    // Shape Muse expects: array of backends with nested models
    return (cat.backends || []).map(function (b) {
      var models = (cat.models || []).filter(function (m) {
        return (m.backends || []).indexOf(b.id) >= 0;
      }).map(function (m) {
        return { id: m.ollama_pull || m.id, label: m.label, tier: m.placement, vramGb: m.min_vram_gb, catalogId: m.id };
      });
      return {
        id: b.id,
        label: b.label,
        kind: b.kind === 'local' ? 'local' : b.kind,
        alwaysOn: !!b.always_on,
        defaultEndpoint: (cat.defaults && cat.defaults.base_urls && cat.defaults.base_urls[b.id]) || '',
        models: models.length ? models : [{ id: 'rules', label: 'Hint engine' }],
        defaultModel: models[0] ? models[0].id : 'rules',
        notes: b.note || ''
      };
    });
  }

  function setOverride(backendId, modelId) {
    if (!backendId) {
      setPolicy({ mode: 'auto' });
      return getPolicy();
    }
    // Map ollama pull name back to catalog id when possible
    var id = modelId;
    var cat = catalogCache || minimalCatalog();
    (cat.models || []).forEach(function (m) {
      if (m.id === modelId || m.ollama_pull === modelId) id = m.id;
    });
    setPolicy({ mode: 'manual', primary: id, backend: backendId });
    return getPolicy();
  }

  function setPrimary(backendId, modelId) {
    return setOverride(backendId, modelId);
  }

  function probe(backendId) {
    return healthCheck().then(function (h) {
      var b = (h.backends || {})[backendId] || { ok: false, reason: 'unknown' };
      return b;
    });
  }

  function applyProfile(profileId) {
    setPolicy({ hardware_profile: profileId });
    return load();
  }

  function profiles() {
    var cat = catalogCache || minimalCatalog();
    return cat.hardware_profiles || {};
  }

  function chain() {
    var t = activeTarget();
    return [t, { backendId: 'local-rules', modelId: 'local-rules' }];
  }


  // Public surface — deliverable API + Noah aliases
  var api = {
    POLICY_KEY: POLICY_KEY,
    CREDS_KEY: CREDS_KEY,
    loadCatalog: loadCatalog,
    getCatalog: function () { return catalogCache; },
    selectModel: selectModel,
    chat: chat,
    healthCheck: healthCheck,
    setPolicy: setPolicy,
    getPolicy: getPolicy,
    setCreds: setCreds,
    getCreds: getCreds,
    recommend: recommend,
    modelById: modelById,
    backendById: backendById,
    baseUrlFor: baseUrlFor,
    isHealthy: isHealthy,
    listModels: listModels,
    getDemandTiers: getDemandTiers,
    systemPrompt: systemPrompt,
    readHealth: readHealth,
    // Muse aliases
    STORAGE: POLICY_KEY,
    catalog: catalog,
    profiles: profiles,
    load: load,
    save: save,
    applyProfile: applyProfile,
    setOverride: setOverride,
    setPrimary: setPrimary,
    setEndpoint: setEndpoint,
    setOrder: function () { return load(); },
    activeTarget: activeTarget,
    chain: chain,
    endpointFor: endpointFor,
    endpointForBackend: endpointFor,
    invokeOne: function (target, messages, ctx) {
      return invoke({ id: target.modelId, model: modelById(target.modelId) || { id: target.modelId, backends: [target.backendId] }, backend: target.backendId }, messages, ctx || {});
    },
    probe: probe,
    maybeAutoSwitch: maybePromote,
    normalizeTierId: normalizeTierId
  };

  g.IL_MODEL_ROUTER = api;
  g.ILModelRouter = api; // alias for older Muse drafts

  // Eager catalog + hook sync
  if (typeof fetch === 'function') {
    loadCatalog().then(function () {
      syncMuseHook(getPolicy());
    });
  } else {
    catalogCache = minimalCatalog();
    syncMuseHook(getPolicy());
  }
})(typeof window !== 'undefined' ? window : (typeof global !== 'undefined' ? global : this));
;

/* ---- source: assets/il-model-analytics.js (14497 bytes) ---- */
/**
 * IL Model Analytics — rolling scores + auto-promote + scale-relative-to-demand signals.
 *
 * Events → ILAnalytics (il.analytics.v1) and local il.insights.model.v1 / il.model.metrics.v1
 * Promote challenger when win-rate + latency thresholds met AND challenger is healthy.
 * Scale recommendations suggest next demand tier — never auto-buy hardware.
 */
(function (g) {
  'use strict';

  var METRICS_KEY = 'il.model.metrics.v1';
  var INSIGHTS_KEY = 'il.insights.model.v1';
  var MAX_EVENTS = 400;

  function read(key, fb) {
    try {
      var raw = g.localStorage.getItem(key);
      if (!raw) return fb;
      var p = JSON.parse(raw);
      return p && typeof p === 'object' ? p : fb;
    } catch (e) { return fb; }
  }

  function write(key, val) {
    try { g.localStorage.setItem(key, JSON.stringify(val)); } catch (e) {}
  }

  function emptyMetrics() {
    return { v: 1, events: [], byModel: {}, concurrencyHint: 0, updatedAt: Date.now() };
  }

  function loadMetrics() {
    var m = read(METRICS_KEY, null);
    if (m && m.v === 1) return m;
    return emptyMetrics();
  }

  function saveMetrics(m) {
    m.updatedAt = Date.now();
    if (m.events && m.events.length > MAX_EVENTS) m.events = m.events.slice(-MAX_EVENTS);
    write(METRICS_KEY, m);
    write(INSIGHTS_KEY, {
      v: 1,
      updatedAt: m.updatedAt,
      byModel: m.byModel,
      scale: m.lastScale || null,
      concurrencyHint: m.concurrencyHint || 0
    });
    return m;
  }

  function ensureModel(byModel, id) {
    if (!byModel[id]) {
      byModel[id] = {
        n: 0, ok: 0, fail: 0,
        latencies: [],
        thumbsUp: 0, thumbsDown: 0,
        wins: 0, explores: 0
      };
    }
    return byModel[id];
  }

  function percentile(sorted, p) {
    if (!sorted.length) return 0;
    var idx = Math.min(sorted.length - 1, Math.max(0, Math.ceil(p * sorted.length) - 1));
    return sorted[idx];
  }

  function rollingStats(row) {
    var lats = (row.latencies || []).slice().sort(function (a, b) { return a - b; });
    var n = row.n || 0;
    var ok = row.ok || 0;
    var thumbs = (row.thumbsUp || 0) + (row.thumbsDown || 0);
    var winRate = n ? ok / n : 0;
    if (thumbs >= 3) {
      winRate = 0.5 * winRate + 0.5 * ((row.thumbsUp || 0) / thumbs);
    }
    return {
      n: n,
      ok: ok,
      fail: row.fail || 0,
      errorRate: n ? (row.fail || 0) / n : 0,
      winRate: winRate,
      p50: percentile(lats, 0.5),
      p95: percentile(lats, 0.95),
      meanLatency: lats.length ? lats.reduce(function (a, b) { return a + b; }, 0) / lats.length : 0,
      thumbsUp: row.thumbsUp || 0,
      thumbsDown: row.thumbsDown || 0
    };
  }

  /** Pure scoring policy for promote decisions + node smoke tests. */
  function scoringPolicy(primaryStats, challengerStats, policy) {
    policy = policy || {};
    var minN = policy.min_samples || 8;
    var margin = policy.win_rate_margin != null ? policy.win_rate_margin : 0.08;
    var slack = policy.latency_slack_ms != null ? policy.latency_slack_ms : 1500;
    if (!primaryStats || !challengerStats) return { promote: false, reason: 'missing-stats' };
    if (challengerStats.n < minN || primaryStats.n < minN) {
      return { promote: false, reason: 'insufficient-samples', need: minN };
    }
    if (challengerStats.winRate < primaryStats.winRate + margin) {
      return {
        promote: false,
        reason: 'win-rate',
        primary: primaryStats.winRate,
        challenger: challengerStats.winRate,
        margin: margin
      };
    }
    var cLat = challengerStats.p95 || challengerStats.meanLatency || 0;
    var pLat = primaryStats.p95 || primaryStats.meanLatency || 0;
    if (cLat > pLat + slack) {
      return {
        promote: false,
        reason: 'latency',
        primaryP95: pLat,
        challengerP95: cLat,
        slack: slack
      };
    }
    return {
      promote: true,
      reason: 'challenger-better',
      winRate: challengerStats.winRate,
      latencyMs: cLat,
      primaryWinRate: primaryStats.winRate
    };
  }

  function record(evt) {
    if (!evt || !evt.modelId) return null;
    var m = loadMetrics();
    var now = Date.now();
    var entry = {
      t: now,
      modelId: evt.modelId,
      backendId: evt.backendId || '',
      latencyMs: evt.latencyMs || 0,
      ok: !!evt.ok,
      task: evt.task || 'chat',
      reason: evt.reason || '',
      demand_tier: evt.demand_tier || '',
      error: evt.error || null
    };
    m.events.push(entry);
    var row = ensureModel(m.byModel, evt.modelId);
    row.n += 1;
    if (evt.ok) {
      row.ok += 1;
      row.latencies.push(evt.latencyMs || 0);
      if (row.latencies.length > 100) row.latencies = row.latencies.slice(-100);
    } else {
      row.fail += 1;
    }
    if (evt.reason === 'auto-explore') row.explores += 1;
    var recent = m.events.filter(function (e) { return now - e.t < 60000; });
    m.concurrencyHint = recent.length;
    saveMetrics(m);
    if (g.ILAnalytics && g.ILAnalytics.track) {
      g.ILAnalytics.track('model_completion', {
        modelId: evt.modelId,
        backendId: evt.backendId,
        ok: !!evt.ok,
        latencyMs: evt.latencyMs || 0,
        demand_tier: evt.demand_tier || '',
        task: evt.task || 'chat'
      });
    }
    return entry;
  }

  function thumb(modelId, up) {
    var m = loadMetrics();
    var row = ensureModel(m.byModel, modelId);
    if (up) row.thumbsUp += 1;
    else row.thumbsDown += 1;
    saveMetrics(m);
    if (g.ILAnalytics && g.ILAnalytics.track) {
      g.ILAnalytics.track('model_thumb', { modelId: modelId, up: !!up });
    }
    return rollingStats(row);
  }

  function scores() {
    var m = loadMetrics();
    var out = {};
    Object.keys(m.byModel).forEach(function (id) {
      out[id] = rollingStats(m.byModel[id]);
    });
    return out;
  }

  function shouldPromote(policy) {
    policy = policy || {};
    var all = scores();
    var primary = policy.primary;
    var challengers = policy.challengers || [];
    if (!primary || !all[primary]) return { promote: false, reason: 'no-primary-stats' };
    var best = null;
    challengers.forEach(function (cid) {
      if (!all[cid]) return;
      var decision = scoringPolicy(all[primary], all[cid], policy);
      if (decision.promote) {
        if (!best || all[cid].winRate > ((all[best.challenger] && all[best.challenger].winRate) || 0)) {
          best = {
            promote: true,
            challenger: cid,
            winRate: decision.winRate,
            latencyMs: decision.latencyMs,
            primaryWinRate: decision.primaryWinRate
          };
        }
      }
    });
    return best || { promote: false, reason: 'no-challenger-ready' };
  }

  function scaleRecommendation(policy, catalog) {
    policy = policy || {};
    catalog = catalog || g.IL_MODEL_CATALOG || {};
    var defaults = catalog.defaults || {};
    var sig = defaults.scale_signals || {
      p95_latency_ms: 8000,
      error_rate: 0.15,
      concurrency_hint: 4,
      thumbs_down_rate: 0.25,
      window_events: 40
    };
    var m = loadMetrics();
    var tier = policy.demand_tier || 'T0';
    var tiers = catalog.demand_tiers || {};
    var tierInfo = tiers[tier] || {};
    var next = tierInfo.next_tier || null;
    var windowN = sig.window_events || 40;
    var recent = (m.events || []).slice(-windowN);
    if (recent.length < Math.min(10, windowN)) {
      return {
        suggest_tier: null,
        current_tier: tier,
        reason: 'insufficient-demand-sample',
        action: 'observe',
        honesty: 'Scale relative to demand — no recommendation yet.'
      };
    }
    var fails = recent.filter(function (e) { return !e.ok; }).length;
    var errorRate = fails / recent.length;
    var lats = recent.filter(function (e) { return e.ok; }).map(function (e) { return e.latencyMs || 0; }).sort(function (a, b) { return a - b; });
    var p95 = percentile(lats, 0.95);
    var conc = m.concurrencyHint || 0;
    var thumbsDown = 0, thumbsTotal = 0;
    Object.keys(m.byModel).forEach(function (id) {
      var row = m.byModel[id];
      thumbsDown += row.thumbsDown || 0;
      thumbsTotal += (row.thumbsUp || 0) + (row.thumbsDown || 0);
    });
    var tdRate = thumbsTotal ? thumbsDown / thumbsTotal : 0;
    var fires = [];
    if (p95 >= (sig.p95_latency_ms || 8000)) fires.push({ signal: 'p95_latency', value: p95, threshold: sig.p95_latency_ms });
    if (errorRate >= (sig.error_rate || 0.15)) fires.push({ signal: 'error_rate', value: errorRate, threshold: sig.error_rate });
    if (conc >= (sig.concurrency_hint || 4)) fires.push({ signal: 'concurrency', value: conc, threshold: sig.concurrency_hint });
    if (thumbsTotal >= 8 && tdRate >= (sig.thumbs_down_rate || 0.25)) {
      fires.push({ signal: 'thumbs_down_rate', value: tdRate, threshold: sig.thumbs_down_rate });
    }
    var rec = {
      current_tier: tier,
      suggest_tier: null,
      signals: fires,
      metrics: { p95: p95, errorRate: errorRate, concurrencyHint: conc, thumbsDownRate: tdRate, window: recent.length },
      action: 'hold',
      honesty: 'Recommendations only — do not auto-buy hardware or invent local 70B GPU.',
      next_tier_label: next && tiers[next] ? tiers[next].label : null
    };
    if (fires.length >= 1 && next) {
      rec.suggest_tier = next;
      rec.action = 'consider_scale';
      rec.reason = 'demand_signals';
      rec.message = 'Demand signals suggest moving toward ' + next + ' (' + (rec.next_tier_label || next) + '). Operator decision — router will not purchase hosts.';
    } else if (fires.length >= 1 && !next) {
      rec.action = 'optimize_or_quota';
      rec.reason = 'at_max_tier';
      rec.message = 'Already at highest catalog tier (T2). Optimize models, add quotas, or accept latency — still no auto-buy.';
    } else {
      rec.reason = 'within_thresholds';
      rec.message = 'Capacity OK relative to current demand.';
    }
    m.lastScale = rec;
    saveMetrics(m);
    return rec;
  }

  function recommend(policy) {
    policy = policy || (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getPolicy && g.IL_MODEL_ROUTER.getPolicy()) || {};
    var all = scores();
    var promo = shouldPromote(policy);
    var cat = g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getCatalog && g.IL_MODEL_ROUTER.getCatalog();
    var scale = scaleRecommendation(policy, cat);
    return { scores: all, promote: promo, scale: scale, primary: policy.primary, demand_tier: policy.demand_tier };
  }

  function logCompletion(evt) {
    return record({
      modelId: evt.modelId,
      backendId: evt.backendId,
      latencyMs: evt.latencyMs,
      ok: evt.ok !== false,
      task: evt.taskType || evt.task,
      demand_tier: evt.demand_tier,
      error: evt.error
    });
  }

  function recommendPrimary(opts) {
    opts = opts || {};
    var policy = (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getPolicy && g.IL_MODEL_ROUTER.getPolicy()) || {};
    policy.min_samples = opts.winsNeeded || policy.min_samples;
    var d = shouldPromote(policy);
    if (d.promote) {
      return { switchTo: { backendId: 'ollama', modelId: d.challenger }, from: opts.current, score: d.winRate };
    }
    return null;
  }


  /* Muse lean|standard|heavy ↔ T0|T1|T2 */
  var MUSE_TIERS = [
    { id: 'lean', label: 'Lean', blurb: 'T0 — local P920: rules + ≤3B GPU / 7B CPU. Prefer lean defaults.', catalog: 'T0' },
    { id: 'standard', label: 'Standard', blurb: 'T1 — extra CPU inference hosts when demand grows.', catalog: 'T1' },
    { id: 'heavy', label: 'Heavy', blurb: 'T2 — remote OSS API / bigger GPU later. Recommend only — never auto-buy.', catalog: 'T2' }
  ];
  var MUSE_TO_CAT = { lean: 'T0', standard: 'T1', heavy: 'T2', T0: 'T0', T1: 'T1', T2: 'T2' };
  var CAT_TO_MUSE = { T0: 'lean', T1: 'standard', T2: 'heavy' };

  function tiers() { return MUSE_TIERS.slice(); }

  function setTier(id) {
    var catTier = MUSE_TO_CAT[id] || 'T0';
    if (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.setPolicy) {
      g.IL_MODEL_ROUTER.setPolicy({ demand_tier: catTier });
    }
    var m = loadMetrics();
    m.museTier = CAT_TO_MUSE[catTier] || 'lean';
    saveMetrics(m);
    return demandStatus();
  }

  function load() {
    var m = loadMetrics();
    var policy = (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getPolicy) ? g.IL_MODEL_ROUTER.getPolicy() : {};
    return {
      demandTier: m.museTier || CAT_TO_MUSE[policy.demand_tier] || 'lean',
      byModel: m.byModel,
      events: m.events,
      lastScale: m.lastScale
    };
  }

  function demandStatus() {
    var policy = (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getPolicy) ? g.IL_MODEL_ROUTER.getPolicy() : { demand_tier: 'T0' };
    var museId = CAT_TO_MUSE[policy.demand_tier] || 'lean';
    var tierObj = MUSE_TIERS.filter(function (t) { return t.id === museId; })[0] || MUSE_TIERS[0];
    var cat = (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getCatalog) ? g.IL_MODEL_ROUTER.getCatalog() : {};
    var scale = scaleRecommendation(policy, cat);
    var sc = scores();
    var ranking = Object.keys(sc).map(function (id) {
      return { modelId: id, backendId: 'ollama', winRate: sc[id].winRate, p95: sc[id].p95, n: sc[id].n };
    }).sort(function (a, b) { return (b.winRate - a.winRate) || (a.p95 - b.p95); });
    return {
      tier: tierObj,
      suggestedTier: scale.suggest_tier ? (CAT_TO_MUSE[scale.suggest_tier] || scale.suggest_tier) : null,
      suggestReason: scale.message || scale.reason,
      scaleNote: 'Scale relative to demand. Prefer lean (T0) defaults; grow to T1/T2 when signals fire — never auto-buy hardware.',
      ranking: ranking,
      scale: scale
    };
  }

  function setThumb(backendId, modelId, v) {
    return thumb(modelId, v > 0 || v === true || v === 'up');
  }

  var api = {
    METRICS_KEY: METRICS_KEY,
    INSIGHTS_KEY: INSIGHTS_KEY,
    record: record,
    thumb: thumb,
    scores: scores,
    shouldPromote: shouldPromote,
    scoringPolicy: scoringPolicy,
    scaleRecommendation: scaleRecommendation,
    recommend: recommend,
    loadMetrics: loadMetrics,
    logCompletion: logCompletion,
    recommendPrimary: recommendPrimary,
    rollingStats: rollingStats,
    // Muse aliases
    load: load,
    setTier: setTier,
    demandStatus: demandStatus,
    tiers: tiers,
    setThumb: setThumb
  };

  g.ILModelAnalytics = api;
  g.IL_MODEL_ANALYTICS = api;

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  }
})(typeof window !== 'undefined' ? window : (typeof global !== 'undefined' ? global : this));
;

/* ---- source: assets/il-model-panel.js (11073 bytes) ---- */
/**
 * Admin/Coach model switcher panel — on-demand primary, auto-iterate, live scores.
 * Mount: <div data-il-model-panel></div>
 * i18n keys: model.* (EN/ES)
 */
(function (g) {
  'use strict';

  function t(key, fb) {
    try {
      if (g.ILi18n && typeof g.ILi18n.t === 'function') {
        var v = g.ILi18n.t(key);
        if (v && v !== key) return v;
      }
    } catch (e) {}
    return fb || key;
  }

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  function mount(root) {
    if (!root || root.getAttribute('data-il-model-panel-ready')) return;
    root.setAttribute('data-il-model-panel-ready', '1');
    root.className = (root.className ? root.className + ' ' : '') + 'il-model-panel';

    var router = g.IL_MODEL_ROUTER || g.ILModelRouter;
    var analytics = g.ILModelAnalytics || g.IL_MODEL_ANALYTICS;

    var header = el('div', 'il-model-panel__head');
    header.innerHTML =
      '<p class="il-model-panel__kicker" data-i18n="model.kicker">' + t('model.kicker', 'Model router · Scale relative to demand') + '</p>' +
      '<h2 class="il-model-panel__title" data-i18n="model.title">' + t('model.title', 'Lab LLM switcher') + '</h2>' +
      '<p class="il-model-panel__lede" data-i18n="model.lede">' +
        t('model.lede', 'T0 local P920 (3B GPU / 7B CPU) → T1 extra CPU hosts → T2 remote OSS. Auto-switch only among healthy models. Never claim 70B local GPU.') +
      '</p>';

    var controls = el('div', 'il-model-panel__controls');
    var modeLabel = el('label', 'il-model-panel__toggle');
    var modeCb = document.createElement('input');
    modeCb.type = 'checkbox';
    modeCb.id = 'il-model-auto';
    modeLabel.appendChild(modeCb);
    modeLabel.appendChild(document.createTextNode(' '));
    var modeSpan = el('span', null, t('model.auto_iterate', 'Auto-iterate (analytics promote)'));
    modeSpan.setAttribute('data-i18n', 'model.auto_iterate');
    modeLabel.appendChild(modeSpan);

    var primarySel = document.createElement('select');
    primarySel.className = 'il-model-panel__select';
    primarySel.setAttribute('aria-label', t('model.primary', 'Primary model'));
    primarySel.id = 'il-model-primary';

    var tierSel = document.createElement('select');
    tierSel.className = 'il-model-panel__select';
    tierSel.id = 'il-model-tier';
    tierSel.setAttribute('aria-label', t('model.demand_tier', 'Demand tier'));

    var applyBtn = el('button', 'il-model-panel__btn');
    applyBtn.type = 'button';
    applyBtn.setAttribute('data-i18n', 'model.apply');
    applyBtn.textContent = t('model.apply', 'Set primary');

    var healthBtn = el('button', 'il-model-panel__btn il-model-panel__btn--ghost');
    healthBtn.type = 'button';
    healthBtn.setAttribute('data-i18n', 'model.health');
    healthBtn.textContent = t('model.health', 'Health check');

    var refreshBtn = el('button', 'il-model-panel__btn il-model-panel__btn--ghost');
    refreshBtn.type = 'button';
    refreshBtn.setAttribute('data-i18n', 'model.refresh');
    refreshBtn.textContent = t('model.refresh', 'Refresh scores');

    controls.appendChild(modeLabel);
    controls.appendChild(tierSel);
    controls.appendChild(primarySel);
    controls.appendChild(applyBtn);
    controls.appendChild(healthBtn);
    controls.appendChild(refreshBtn);

    var status = el('p', 'il-model-panel__status');
    status.id = 'il-model-status';
    var scaleBox = el('div', 'il-model-panel__scale');
    scaleBox.id = 'il-model-scale';
    var tableWrap = el('div', 'il-model-panel__table-wrap');
    var table = el('table', 'il-model-panel__table');
    table.innerHTML =
      '<thead><tr>' +
      '<th data-i18n="model.col_model">' + t('model.col_model', 'Model') + '</th>' +
      '<th data-i18n="model.col_n">' + t('model.col_n', 'N') + '</th>' +
      '<th data-i18n="model.col_win">' + t('model.col_win', 'Win rate') + '</th>' +
      '<th data-i18n="model.col_p95">' + t('model.col_p95', 'p95 ms') + '</th>' +
      '<th data-i18n="model.col_err">' + t('model.col_err', 'Errors') + '</th>' +
      '<th data-i18n="model.col_health">' + t('model.col_health', 'Healthy') + '</th>' +
      '</tr></thead><tbody id="il-model-scores-body"></tbody>';
    tableWrap.appendChild(table);

    var baseRow = el('div', 'il-model-panel__base');
    baseRow.innerHTML =
      '<label class="il-model-panel__field"><span data-i18n="model.base_url">' + t('model.base_url', 'LLM base URL') + '</span></label>';
    var baseInput = document.createElement('input');
    baseInput.type = 'url';
    baseInput.className = 'il-model-panel__input';
    baseInput.id = 'il-model-base';
    baseInput.placeholder = 'http://127.0.0.1:11434 or tunnel URL';
    var keyInput = document.createElement('input');
    keyInput.type = 'password';
    keyInput.className = 'il-model-panel__input';
    keyInput.id = 'il-model-key';
    keyInput.placeholder = t('model.api_key_ph', 'API key (localStorage only — never commit)');
    keyInput.setAttribute('autocomplete', 'off');
    var saveBase = el('button', 'il-model-panel__btn il-model-panel__btn--ghost');
    saveBase.type = 'button';
    saveBase.textContent = t('model.save_endpoint', 'Save endpoint');
    saveBase.setAttribute('data-i18n', 'model.save_endpoint');
    baseRow.appendChild(baseInput);
    baseRow.appendChild(keyInput);
    baseRow.appendChild(saveBase);

    root.appendChild(header);
    root.appendChild(controls);
    root.appendChild(baseRow);
    root.appendChild(status);
    root.appendChild(scaleBox);
    root.appendChild(tableWrap);

    function paint() {
      if (!router) {
        status.textContent = t('model.missing_router', 'Router not loaded.');
        return;
      }
      var policy = router.getPolicy();
      modeCb.checked = policy.mode === 'auto';
      router.loadCatalog().then(function (cat) {
        // tiers
        tierSel.innerHTML = '';
        var tiers = cat.demand_tiers || {};
        Object.keys(tiers).forEach(function (tid) {
          var o = document.createElement('option');
          o.value = tid;
          o.textContent = tid + ' — ' + (tiers[tid].label || tid);
          if (tid === policy.demand_tier) o.selected = true;
          tierSel.appendChild(o);
        });
        // models for tier
        primarySel.innerHTML = '';
        (cat.models || []).forEach(function (m) {
          var allowed = !m.demand_tiers || m.demand_tiers.indexOf(policy.demand_tier) >= 0;
          if (!allowed && m.id !== 'local-rules') return;
          var o = document.createElement('option');
          o.value = m.id;
          o.textContent = m.label + ' (' + (m.placement || '?') + ', ' + (m.size_b || 0) + 'B)';
          if (m.id === policy.primary) o.selected = true;
          primarySel.appendChild(o);
        });
        var ep = router.baseUrlFor(policy.backend || 'ollama');
        if (ep) baseInput.value = ep;
        var health = router.readHealth ? router.readHealth() : { models: {} };
        status.textContent = t('model.status_line', 'Mode') + ': ' + policy.mode +
          ' · ' + t('model.demand_tier', 'Demand tier') + ': ' + policy.demand_tier +
          ' · ' + t('model.primary', 'Primary') + ': ' + policy.primary;

        // scale box
        var scale = analytics && analytics.scaleRecommendation
          ? analytics.scaleRecommendation(policy, cat)
          : null;
        if (scale) {
          scaleBox.innerHTML =
            '<p class="il-model-panel__scale-title" data-i18n="model.scale_title">' +
            t('model.scale_title', 'Scale relative to demand') + '</p>' +
            '<p>' + (scale.message || scale.reason || '') + '</p>' +
            (scale.suggest_tier
              ? '<p class="il-model-panel__scale-next"><strong>' + t('model.suggest_tier', 'Suggested tier') + ':</strong> ' + scale.suggest_tier + '</p>'
              : '') +
            '<p class="il-model-panel__honesty">' + (scale.honesty || '') + '</p>';
        }

        // scores table
        var body = root.querySelector('#il-model-scores-body');
        body.innerHTML = '';
        var sc = analytics && analytics.scores ? analytics.scores() : {};
        var ids = Object.keys(sc);
        if (!ids.length) {
          (cat.models || []).slice(0, 6).forEach(function (m) { ids.push(m.id); });
        }
        ids.forEach(function (id) {
          var s = sc[id] || { n: 0, winRate: 0, p95: 0, fail: 0 };
          var healthy = router.isHealthy ? router.isHealthy(id) : (id === 'local-rules');
          var tr = document.createElement('tr');
          if (id === policy.primary) tr.className = 'is-primary';
          tr.innerHTML =
            '<td>' + id + '</td>' +
            '<td>' + (s.n || 0) + '</td>' +
            '<td>' + ((s.winRate || 0) * 100).toFixed(0) + '%</td>' +
            '<td>' + Math.round(s.p95 || 0) + '</td>' +
            '<td>' + (s.fail || 0) + '</td>' +
            '<td>' + (healthy ? '✓' : '—') + '</td>';
          body.appendChild(tr);
        });
      });
    }

    modeCb.addEventListener('change', function () {
      if (!router) return;
      router.setPolicy({ mode: modeCb.checked ? 'auto' : 'manual' });
      paint();
    });

    tierSel.addEventListener('change', function () {
      if (!router) return;
      router.setPolicy({ demand_tier: tierSel.value });
      paint();
    });

    applyBtn.addEventListener('click', function () {
      if (!router) return;
      router.setPolicy({
        primary: primarySel.value,
        mode: modeCb.checked ? 'auto' : 'manual',
        demand_tier: tierSel.value
      });
      if (g.ILAnalytics && g.ILAnalytics.track) {
        g.ILAnalytics.track('model_manual_switch', { primary: primarySel.value, tier: tierSel.value });
      }
      paint();
    });

    healthBtn.addEventListener('click', function () {
      if (!router || !router.healthCheck) return;
      status.textContent = t('model.checking', 'Checking…');
      router.healthCheck().then(function () { paint(); });
    });

    refreshBtn.addEventListener('click', paint);

    saveBase.addEventListener('click', function () {
      if (!router) return;
      var policy = router.getPolicy();
      var backend = policy.backend || 'ollama';
      router.setCreds(backend, baseInput.value.trim(), keyInput.value.trim() || null);
      // Also set ollama specifically when URL looks like ollama
      if (/11434/.test(baseInput.value)) router.setCreds('ollama', baseInput.value.trim(), null);
      keyInput.value = '';
      status.textContent = t('model.saved_local', 'Endpoint saved to localStorage only.');
      paint();
    });

    paint();
    root._ilModelPaint = paint;
  }

  function boot() {
    var nodes = document.querySelectorAll('[data-il-model-panel]');
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
  }

  g.ILModelPanel = { mount: mount, boot: boot };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
;

/* ---- source: assets/il-scene-kit.js (18344 bytes) ---- */
/**
 * IL Scene Kit — shared WebGL / curriculum 3D utilities (CSP-safe, no CDN).
 * Used by Noah 3D familiar + Immersive Player (lectures / cert labs / sims).
 * Palette: cyan #5EEAD4 · gold #c9a227 · void #070B16. Interstitium original.
 * Optional Three.js/glTF path: see docs/ops/IMMERSIVE-3D.md (vendored when present).
 */
(function (g) {
  'use strict';

  var CYAN = [0.369, 0.918, 0.831];
  var GOLD = [0.831, 0.659, 0.325];
  var VOID = [0.027, 0.043, 0.086];

  function prefersReducedMotion() {
    try { return !!(g.matchMedia && g.matchMedia('(prefers-reduced-motion: reduce)').matches); }
    catch (e) { return false; }
  }

  function isMobile() {
    try { return !!(g.matchMedia && g.matchMedia('(max-width: 768px)').matches); }
    catch (e) { return false; }
  }

  function dprCap(max) {
    var d = g.devicePixelRatio || 1;
    return Math.min(d, max == null ? (isMobile() ? 1.75 : 2) : max);
  }

  function compileShader(gl, type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      try { console.warn('[ILSceneKit] shader', gl.getShaderInfoLog(sh)); } catch (e) {}
      gl.deleteShader(sh);
      return null;
    }
    return sh;
  }

  function linkProgram(gl, vsSrc, fsSrc) {
    var vs = compileShader(gl, gl.VERTEX_SHADER, vsSrc);
    var fs = compileShader(gl, gl.FRAGMENT_SHADER, fsSrc);
    if (!vs || !fs) return null;
    var p = gl.createProgram();
    gl.attachShader(p, vs);
    gl.attachShader(p, fs);
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      try { console.warn('[ILSceneKit] link', gl.getProgramInfoLog(p)); } catch (e) {}
      return null;
    }
    return p;
  }

  function resizeCanvas(canvas, gl, root, mobile) {
    var dpr = dprCap(mobile ? 1.75 : 2);
    var w = Math.max(1, (root && root.clientWidth) || canvas.clientWidth || 320);
    var h = Math.max(1, (root && root.clientHeight) || canvas.clientHeight || 180);
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    if (gl) gl.viewport(0, 0, canvas.width, canvas.height);
    return { w: w, h: h, dpr: dpr, aspect: w / h };
  }

  /* —— minimal mat4 —— */
  function mat4() { return new Float32Array(16); }
  function mat4Identity(out) {
    out = out || mat4();
    out[0]=1;out[1]=0;out[2]=0;out[3]=0;
    out[4]=0;out[5]=1;out[6]=0;out[7]=0;
    out[8]=0;out[9]=0;out[10]=1;out[11]=0;
    out[12]=0;out[13]=0;out[14]=0;out[15]=1;
    return out;
  }
  function mat4Perspective(out, fovy, aspect, near, far) {
    var f = 1 / Math.tan(fovy / 2), nf = 1 / (near - far);
    out[0]=f/aspect;out[1]=0;out[2]=0;out[3]=0;
    out[4]=0;out[5]=f;out[6]=0;out[7]=0;
    out[8]=0;out[9]=0;out[10]=(far+near)*nf;out[11]=-1;
    out[12]=0;out[13]=0;out[14]=(2*far*near)*nf;out[15]=0;
    return out;
  }
  function mat4LookAt(out, eye, center, up) {
    var zx=eye[0]-center[0], zy=eye[1]-center[1], zz=eye[2]-center[2];
    var len=1/Math.max(Math.hypot(zx,zy,zz),1e-6); zx*=len; zy*=len; zz*=len;
    var xx=up[1]*zz-up[2]*zy, xy=up[2]*zx-up[0]*zz, xz=up[0]*zy-up[1]*zx;
    len=1/Math.max(Math.hypot(xx,xy,xz),1e-6); xx*=len; xy*=len; xz*=len;
    var yx=zy*xz-zz*xy, yy=zz*xx-zx*xz, yz=zx*xy-zy*xx;
    out[0]=xx;out[1]=yx;out[2]=zx;out[3]=0;
    out[4]=xy;out[5]=yy;out[6]=zy;out[7]=0;
    out[8]=xz;out[9]=yz;out[10]=zz;out[11]=0;
    out[12]=-(xx*eye[0]+xy*eye[1]+xz*eye[2]);
    out[13]=-(yx*eye[0]+yy*eye[1]+yz*eye[2]);
    out[14]=-(zx*eye[0]+zy*eye[1]+zz*eye[2]);
    out[15]=1;
    return out;
  }
  function mat4Multiply(out, a, b) {
    var a00=a[0],a01=a[1],a02=a[2],a03=a[3],a10=a[4],a11=a[5],a12=a[6],a13=a[7];
    var a20=a[8],a21=a[9],a22=a[10],a23=a[11],a30=a[12],a31=a[13],a32=a[14],a33=a[15];
    var i,b0,b1,b2,b3;
    for (i=0;i<4;i++){
      b0=b[i*4];b1=b[i*4+1];b2=b[i*4+2];b3=b[i*4+3];
      out[i*4]=b0*a00+b1*a10+b2*a20+b3*a30;
      out[i*4+1]=b0*a01+b1*a11+b2*a21+b3*a31;
      out[i*4+2]=b0*a02+b1*a12+b2*a22+b3*a32;
      out[i*4+3]=b0*a03+b1*a13+b2*a23+b3*a33;
    }
    return out;
  }
  function mat4FromRTS(out, rx, ry, rz, tx, ty, tz, sx, sy, sz) {
    var cx=Math.cos(rx),sxr=Math.sin(rx),cy=Math.cos(ry),syr=Math.sin(ry),cz=Math.cos(rz),szr=Math.sin(rz);
    var m00=cy*cz,m01=cy*szr,m02=-syr;
    var m10=sxr*syr*cz-cx*szr,m11=sxr*syr*szr+cx*cz,m12=sxr*cy;
    var m20=cx*syr*cz+sxr*szr,m21=cx*syr*szr-sxr*cz,m22=cx*cy;
    out[0]=m00*sx;out[1]=m01*sx;out[2]=m02*sx;out[3]=0;
    out[4]=m10*sy;out[5]=m11*sy;out[6]=m12*sy;out[7]=0;
    out[8]=m20*sz;out[9]=m21*sz;out[10]=m22*sz;out[11]=0;
    out[12]=tx;out[13]=ty;out[14]=tz;out[15]=1;
    return out;
  }


  /** WebGPU capability + preference (flag path). Full WGSL renderer lands later; callers fall back to WebGL. */
  function hasWebGPU() {
    return !!(g.navigator && g.navigator.gpu);
  }
  function preferWebGPU(opts) {
    opts = opts || {};
    if (opts.forceWebGL) return false;
    if (opts.forceWebGPU) return hasWebGPU();
    try {
      if (g.location && /[?&]webgpu=1\b/.test(g.location.search || '')) return hasWebGPU();
      if (g.localStorage && g.localStorage.getItem('il-webgpu') === '1') return hasWebGPU();
    } catch (e) {}
    if (opts.webgpu === false) return false;
    if (opts.engine === 'webgpu' || opts.webgpu === true) return hasWebGPU();
    return false;
  }
  /**
   * Acquire best canvas context: WebGPU adapter probe when preferred, else WebGL.
   * Returns { api:'webgpu'|'webgl'|'none', gl?, gpu?, adapter?, canvas, label }
   */
  function acquireGraphics(canvas, opts) {
    opts = opts || {};
    var out = { api: 'none', canvas: canvas, label: 'none' };
    if (!canvas) return out;
    if (preferWebGPU(opts) && hasWebGPU()) {
      out.api = 'webgpu';
      out.gpu = g.navigator.gpu;
      out.label = 'WebGPU';
      /* Adapter request is async — callers may upgrade; procedural path still uses WebGL today. */
      try {
        g.navigator.gpu.requestAdapter().then(function (a) {
          out.adapter = a || null;
          emitSceneEvent('il-webgpu-adapter', { ok: !!a });
        }).catch(function () {
          emitSceneEvent('il-webgpu-adapter', { ok: false });
        });
      } catch (e) {}
      /* Honest dual-path: still provide WebGL for procedural mesh until WGSL port */
    }
    var gl = canvas.getContext('webgl', opts.webglAttrs || { antialias: true, alpha: !!opts.alpha, powerPreference: 'high-performance' })
      || canvas.getContext('experimental-webgl');
    if (gl) {
      out.gl = gl;
      if (out.api !== 'webgpu') { out.api = 'webgl'; out.label = 'WebGL'; }
      else out.label = 'WebGPU·WebGL-fallback';
      return out;
    }
    if (out.api === 'webgpu') return out;
    return out;
  }

  /** Detect vendored Three (optional). Place at /assets/vendor/three.min.js */
  function hasThree() {
    return !!(g.THREE && g.THREE.WebGLRenderer);
  }

  function hasGLTFLoader() {
    return !!(g.THREE && (g.THREE.GLTFLoader || g.GLTFLoader));
  }

  /**
   * Native GLB (glTF 2.0 binary) parser — CSP-safe, no Three CDN.
   * Returns { ok, meshes:[{positions,normals,indices,material}], materials, url?, reason? }.
   */
  function parseGlb(arrayBuffer) {
    try {
      if (!arrayBuffer || arrayBuffer.byteLength < 20) {
        return { ok: false, reason: 'too_short', meshes: [] };
      }
      var u8 = new Uint8Array(arrayBuffer);
      var dv = new DataView(arrayBuffer);
      if (u8[0] !== 0x67 || u8[1] !== 0x6c || u8[2] !== 0x54 || u8[3] !== 0x46) {
        return { ok: false, reason: 'bad_magic', meshes: [] };
      }
      var version = dv.getUint32(4, true);
      var total = dv.getUint32(8, true);
      if (version !== 2) return { ok: false, reason: 'unsupported_version', meshes: [] };
      var offset = 12;
      var json = null;
      var bin = null;
      while (offset + 8 <= u8.byteLength && offset < total) {
        var chunkLen = dv.getUint32(offset, true);
        var chunkType = String.fromCharCode(u8[offset + 4], u8[offset + 5], u8[offset + 6], u8[offset + 7]);
        offset += 8;
        if (chunkType.indexOf('JSON') === 0) {
          var js = '';
          for (var i = 0; i < chunkLen; i++) js += String.fromCharCode(u8[offset + i]);
          json = JSON.parse(js.trim());
        } else if (chunkType.indexOf('BIN') === 0) {
          bin = arrayBuffer.slice(offset, offset + chunkLen);
        }
        offset += chunkLen;
      }
      if (!json || !bin) return { ok: false, reason: 'missing_chunks', meshes: [] };
      var accessors = json.accessors || [];
      var views = json.bufferViews || [];
      var mats = json.materials || [];

      function readAccessor(ai) {
        var acc = accessors[ai];
        if (!acc) return null;
        var view = views[acc.bufferView];
        if (!view) return null;
        var byteOffset = (view.byteOffset || 0) + (acc.byteOffset || 0);
        var count = acc.count;
        var comp = acc.componentType;
        var type = acc.type;
        var comps = type === 'SCALAR' ? 1 : type === 'VEC2' ? 2 : type === 'VEC3' ? 3 : type === 'VEC4' ? 4 : 1;
        var bdv = new DataView(bin);
        var out;
        var j, k, o;
        if (comp === 5126) {
          out = new Float32Array(count * comps);
          for (j = 0; j < count * comps; j++) out[j] = bdv.getFloat32(byteOffset + j * 4, true);
        } else if (comp === 5123) {
          out = new Uint16Array(count * comps);
          for (j = 0; j < count * comps; j++) out[j] = bdv.getUint16(byteOffset + j * 2, true);
        } else if (comp === 5125) {
          out = new Uint32Array(count * comps);
          for (j = 0; j < count * comps; j++) out[j] = bdv.getUint32(byteOffset + j * 4, true);
        } else if (comp === 5121) {
          out = new Uint8Array(count * comps);
          for (j = 0; j < count * comps; j++) out[j] = bdv.getUint8(byteOffset + j);
        } else {
          return null;
        }
        return { data: out, count: count, type: type, componentType: comp, min: acc.min, max: acc.max };
      }

      function matColor(mi) {
        var m = mats[mi];
        if (!m || !m.pbrMetallicRoughness || !m.pbrMetallicRoughness.baseColorFactor) {
          return { color: [0.369, 0.918, 0.831], emissive: [0.05, 0.18, 0.15], name: (m && m.name) || 'default' };
        }
        var bc = m.pbrMetallicRoughness.baseColorFactor;
        var em = m.emissiveFactor || [0, 0, 0];
        return {
          color: [bc[0], bc[1], bc[2]],
          emissive: [em[0] || 0, em[1] || 0, em[2] || 0],
          name: m.name || 'mat'
        };
      }

      var meshes = [];
      var meshDefs = json.meshes || [];
      for (var mi = 0; mi < meshDefs.length; mi++) {
        var prims = meshDefs[mi].primitives || [];
        for (var pi = 0; pi < prims.length; pi++) {
          var prim = prims[pi];
          if (prim.mode != null && prim.mode !== 4) continue; /* TRIANGLES only */
          var posA = readAccessor(prim.attributes && prim.attributes.POSITION);
          var nrmA = readAccessor(prim.attributes && prim.attributes.NORMAL);
          var idxA = prim.indices != null ? readAccessor(prim.indices) : null;
          if (!posA) continue;
          var positions = posA.data instanceof Float32Array ? posA.data : new Float32Array(posA.data);
          var normals;
          if (nrmA && nrmA.data) {
            normals = nrmA.data instanceof Float32Array ? nrmA.data : new Float32Array(nrmA.data);
          } else {
            normals = new Float32Array(positions.length);
            for (k = 0; k < normals.length; k += 3) normals[k + 1] = 1;
          }
          var indices;
          if (idxA && idxA.data) {
            indices = idxA.data instanceof Uint16Array || idxA.data instanceof Uint32Array
              ? idxA.data
              : new Uint16Array(idxA.data);
          } else {
            indices = new Uint16Array(positions.length / 3);
            for (k = 0; k < indices.length; k++) indices[k] = k;
          }
          /* WebGL1 drawElements UNSIGNED_SHORT path — split if needed later; kit assets stay <65k */
          if (!(indices instanceof Uint16Array) && maxOf(indices) > 65535) {
            /* keep Uint32 — caller may use OES_element_index_uint */
          } else if (!(indices instanceof Uint16Array)) {
            indices = new Uint16Array(indices);
          }
          var mc = matColor(prim.material != null ? prim.material : 0);
          meshes.push({
            name: (meshDefs[mi].name || 'mesh') + (prims.length > 1 ? ':' + pi : ''),
            positions: positions,
            normals: normals,
            indices: indices,
            material: mc
          });
        }
      }
      return {
        ok: meshes.length > 0,
        reason: meshes.length ? undefined : 'no_triangles',
        meshes: meshes,
        materials: mats,
        asset: json.asset || {}
      };
    } catch (err) {
      return { ok: false, reason: 'parse_error', error: String(err && err.message || err), meshes: [] };
    }
  }

  function maxOf(arr) {
    var m = 0;
    for (var i = 0; i < arr.length; i++) if (arr[i] > m) m = arr[i];
    return m;
  }

  /**
   * Fetch + parse GLB via native parser (preferred) or vendored Three GLTFLoader.
   * Does not fetch CDN — CSP script-src 'self' only.
   */
  function loadGltf(url, opts) {
    opts = opts || {};
    return new Promise(function (resolve, reject) {
      if (!url) {
        resolve({ ok: false, reason: 'no_url', url: url });
        return;
      }
      /* Prefer native GLB path — no Three required */
      if (/\.glb($|\?)/i.test(url) || opts.forceNative) {
        g.fetch(url).then(function (res) {
          if (!res || !res.ok) {
            resolve({ ok: false, reason: 'http_' + (res && res.status), url: url });
            return null;
          }
          return res.arrayBuffer();
        }).then(function (buf) {
          if (!buf) return;
          var parsed = parseGlb(buf);
          parsed.url = url;
          resolve(parsed);
        }).catch(function (err) {
          resolve({ ok: false, reason: 'fetch_error', error: String(err && err.message || err), url: url, meshes: [] });
        });
        return;
      }
      if (!hasThree() || !hasGLTFLoader()) {
        resolve({ ok: false, reason: 'three_not_vendored', url: url, meshes: [] });
        return;
      }
      var Loader = g.THREE.GLTFLoader || g.GLTFLoader;
      var loader = new Loader();
      loader.load(
        url,
        function (gltf) { resolve({ ok: true, gltf: gltf, url: url, meshes: [] }); },
        opts.onProgress || null,
        function (err) { reject(err); }
      );
    });
  }

  /**
   * Unreal Pixel Streaming embed — honest stub or iframe/player mount.
   * Never fakes a live stream. Prefer dedicated /immersive/pixel-stream/ client page.
   */
  function pixelStreamEmbed(host, signalingUrl, opts) {
    opts = opts || {};
    if (!host) return null;
    host.innerHTML = '';
    host.classList.add('il-scene-kit__ps-host');
    if (!signalingUrl) {
      host.innerHTML = '<div class="il-scene-kit__ps-stub" role="status">' +
        '<p class="il-scene-kit__ps-kicker">Unreal Pixel Streaming</p>' +
        '<p>Connect a Unreal Pixel Streaming host — set signaling when UE5 streamer is up on lab GPU host.</p>' +
        '<p class="il-scene-kit__ps-hint">Pass <code>?signaling=</code>, <code>data-ps-signaling</code>, or open ' +
        '<a class="il-scene-kit__ps-link" href="/immersive/pixel-stream/">/immersive/pixel-stream/</a>. ' +
        'Unreal Pixel Streaming: bring up a local signaling host to mount a live stream; the client never invents UE video.</p>' +
        '</div>';
      return { mode: 'stub', signaling: null };
    }
    /* Prefer navigating the dedicated client when mountMode=page */
    if (opts.mountMode === 'page') {
      var frame = document.createElement('iframe');
      var q = '/immersive/pixel-stream/?signaling=' + encodeURIComponent(signalingUrl);
      frame.src = q;
      frame.title = opts.title || 'Unreal Pixel Streaming';
      frame.allow = 'autoplay; fullscreen; microphone; camera';
      frame.setAttribute('allowfullscreen', 'true');
      frame.className = 'il-scene-kit__ps-frame';
      host.appendChild(frame);
      return { mode: 'client-page', iframe: frame, signaling: signalingUrl };
    }
    var iframe = document.createElement('iframe');
    iframe.src = signalingUrl;
    iframe.title = opts.title || 'Unreal Pixel Streaming';
    iframe.allow = 'autoplay; fullscreen; microphone; camera';
    iframe.setAttribute('allowfullscreen', 'true');
    iframe.className = 'il-scene-kit__ps-frame';
    host.appendChild(iframe);
    return { mode: 'iframe', iframe: iframe, signaling: signalingUrl };
  }

  /** Shared voice-amp bus — Muse TTS + immersive lecture stages. */
  function onSpeakAmp(fn) {
    var h = function (ev) { fn(ev && ev.detail ? ev.detail : { amp: 0 }); };
    var b = function () { fn({ amp: 1, beat: 1, boundary: 1 }); };
    g.addEventListener('il-muse-speak-amp', h);
    g.addEventListener('il-muse-speak-boundary', b);
    return function off() {
      g.removeEventListener('il-muse-speak-amp', h);
      g.removeEventListener('il-muse-speak-boundary', b);
    };
  }

  function emitSceneEvent(name, detail) {
    try { g.dispatchEvent(new CustomEvent(name, { detail: detail || {} })); } catch (e) {}
  }

  g.ILSceneKit = {
    CYAN: CYAN, GOLD: GOLD, VOID: VOID,
    HEX: { cyan: '#5EEAD4', gold: '#c9a227', void: '#070B16' },
    prefersReducedMotion: prefersReducedMotion,
    isMobile: isMobile,
    dprCap: dprCap,
    compileShader: compileShader,
    linkProgram: linkProgram,
    resizeCanvas: resizeCanvas,
    mat4: mat4,
    mat4Identity: mat4Identity,
    mat4Perspective: mat4Perspective,
    mat4LookAt: mat4LookAt,
    mat4Multiply: mat4Multiply,
    mat4FromRTS: mat4FromRTS,
    hasThree: hasThree,
    hasGLTFLoader: hasGLTFLoader,
    hasWebGPU: hasWebGPU,
    preferWebGPU: preferWebGPU,
    acquireGraphics: acquireGraphics,
    loadGltf: loadGltf,
    parseGlb: parseGlb,
    pixelStreamEmbed: pixelStreamEmbed,
    onSpeakAmp: onSpeakAmp,
    emitSceneEvent: emitSceneEvent,
    VERSION: '1.3.0'
  };

  /* Muse 3D may re-export kit when both present */
  if (g.ILMuse3D) g.ILMuse3D.kit = g.ILSceneKit;
})(typeof window !== 'undefined' ? window : this);
;

/* ---- source: assets/il-noah-avatar.js (45967 bytes) ---- */
/**
 * IL Noah Avatar — full-featured 3D avatar system (Interstitium original).
 *
 * Self-contained WebGL (CSP-safe; no CDN, no Three.js, no external assets).
 * Four procedural avatars, all voice-reactive, driven by Noah status:
 *   idle | listening | thinking | speaking
 *   - monas : crystalline Monas / orrery (default — the classic Dee stage)
 *   - orrery: ringed worlds · orbital mechanics
 *   - sigil : radiant sigil core · counter-rotating glyph rings
 *   - wisp  : nebula ghost · drifting star-wisp
 *
 * Personalization persisted in localStorage 'il-noah-profile':
 *   { avatar, name, accent, intensity } — applied on every mount, everywhere Noah appears.
 *
 * Honesty standard: everything renders on-device in the visitor's browser.
 * No cloud rendering, no uploads, no fake "AI cloud". NOT Meta assets/code.
 */
(function (g) {
  'use strict';

  var PROFILE_KEY = 'il-noah-profile';

  var ACCENTS = {
    cyan:    { label: 'Cyan',    rgb: [0.369, 0.918, 0.831], css: '#5EEAD4' },
    gold:    { label: 'Gold',    rgb: [0.831, 0.659, 0.325], css: '#c9a227' },
    violet:  { label: 'Violet',  rgb: [0.654, 0.545, 0.980], css: '#A78BFA' },
    emerald: { label: 'Emerald', rgb: [0.204, 0.831, 0.600], css: '#34D399' }
  };
  var INTENSITY = {
    calm:     { label: 'Calm',     scale: 0.45 },
    balanced: { label: 'Balanced', scale: 1.0 },
    vivid:    { label: 'Vivid',    scale: 1.6 }
  };
  var VOID = [0.027, 0.043, 0.086];

  /* ---------------- profile store ---------------- */

  function defaultProfile() {
    return { v: 1, avatar: 'monas', name: 'Noah', accent: 'cyan', intensity: 'balanced' };
  }

  function getProfile() {
    var d = defaultProfile();
    try {
      var raw = g.localStorage && g.localStorage.getItem(PROFILE_KEY);
      if (raw) {
        var p = JSON.parse(raw) || {};
        return {
          v: 1,
          avatar: AVATARS_BY_ID[p.avatar] ? p.avatar : d.avatar,
          name: (typeof p.name === 'string' && p.name.trim()) ? p.name.trim().slice(0, 40) : d.name,
          accent: ACCENTS[p.accent] ? p.accent : d.accent,
          intensity: INTENSITY[p.intensity] ? p.intensity : d.intensity
        };
      }
    } catch (e) { /* corrupted or unavailable storage -> defaults */ }
    return d;
  }

  function saveProfile(p) {
    var d = defaultProfile();
    var clean = {
      v: 1,
      avatar: AVATARS_BY_ID[p.avatar] ? p.avatar : d.avatar,
      name: (typeof p.name === 'string' && p.name.trim()) ? p.name.trim().slice(0, 40) : d.name,
      accent: ACCENTS[p.accent] ? p.accent : d.accent,
      intensity: INTENSITY[p.intensity] ? p.intensity : d.intensity
    };
    try { if (g.localStorage) g.localStorage.setItem(PROFILE_KEY, JSON.stringify(clean)); } catch (e) {}
    return clean;
  }

  /* ---------------- math ---------------- */

  function mat4Identity() {
    return new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
  }

  function mat4Perspective(out, fovy, aspect, near, far) {
    var f = 1 / Math.tan(fovy / 2);
    var nf = 1 / (near - far);
    out[0] = f / aspect; out[1] = 0; out[2] = 0; out[3] = 0;
    out[4] = 0; out[5] = f; out[6] = 0; out[7] = 0;
    out[8] = 0; out[9] = 0; out[10] = (far + near) * nf; out[11] = -1;
    out[12] = 0; out[13] = 0; out[14] = 2 * far * near * nf; out[15] = 0;
    return out;
  }

  function mat4LookAt(out, eye, center, up) {
    var zx = eye[0] - center[0], zy = eye[1] - center[1], zz = eye[2] - center[2];
    var len = 1 / Math.max(Math.hypot(zx, zy, zz), 1e-6);
    zx *= len; zy *= len; zz *= len;
    var xx = up[1] * zz - up[2] * zy;
    var xy = up[2] * zx - up[0] * zz;
    var xz = up[0] * zy - up[1] * zx;
    len = 1 / Math.max(Math.hypot(xx, xy, xz), 1e-6);
    xx *= len; xy *= len; xz *= len;
    var yx = zy * xz - zz * xy;
    var yy = zz * xx - zx * xz;
    var yz = zx * xy - zy * xx;
    out[0] = xx; out[1] = yx; out[2] = zx; out[3] = 0;
    out[4] = xy; out[5] = yy; out[6] = zy; out[7] = 0;
    out[8] = xz; out[9] = yz; out[10] = zz; out[11] = 0;
    out[12] = -(xx * eye[0] + xy * eye[1] + xz * eye[2]);
    out[13] = -(yx * eye[0] + yy * eye[1] + yz * eye[2]);
    out[14] = -(zx * eye[0] + zy * eye[1] + zz * eye[2]);
    out[15] = 1;
    return out;
  }

  function mat4Multiply(out, a, b) {
    var a00=a[0],a01=a[1],a02=a[2],a03=a[3],a10=a[4],a11=a[5],a12=a[6],a13=a[7];
    var a20=a[8],a21=a[9],a22=a[10],a23=a[11],a30=a[12],a31=a[13],a32=a[14],a33=a[15];
    var b0,b1,b2,b3,i;
    for (i = 0; i < 4; i++) {
      b0 = b[i*4]; b1 = b[i*4+1]; b2 = b[i*4+2]; b3 = b[i*4+3];
      out[i*4]   = b0*a00 + b1*a10 + b2*a20 + b3*a30;
      out[i*4+1] = b0*a01 + b1*a11 + b2*a21 + b3*a31;
      out[i*4+2] = b0*a02 + b1*a12 + b2*a22 + b3*a32;
      out[i*4+3] = b0*a03 + b1*a13 + b2*a23 + b3*a33;
    }
    return out;
  }

  function mat4FromRTS(out, rx, ry, rz, tx, ty, tz, sx, sy, sz) {
    var cx = Math.cos(rx), sxr = Math.sin(rx);
    var cy = Math.cos(ry), syr = Math.sin(ry);
    var cz = Math.cos(rz), szr = Math.sin(rz);
    var m00 = cy * cz, m01 = cy * szr, m02 = -syr;
    var m10 = sxr * syr * cz - cx * szr;
    var m11 = sxr * syr * szr + cx * cz;
    var m12 = sxr * cy;
    var m20 = cx * syr * cz + sxr * szr;
    var m21 = cx * syr * szr - sxr * cz;
    var m22 = cx * cy;
    out[0] = m00 * sx; out[1] = m01 * sx; out[2] = m02 * sx; out[3] = 0;
    out[4] = m10 * sy; out[5] = m11 * sy; out[6] = m12 * sy; out[7] = 0;
    out[8] = m20 * sz; out[9] = m21 * sz; out[10] = m22 * sz; out[11] = 0;
    out[12] = tx; out[13] = ty; out[14] = tz; out[15] = 1;
    return out;
  }

  function mat3NormalFromMat4(out, m) {
    out[0] = m[0]; out[1] = m[1]; out[2] = m[2];
    out[3] = m[4]; out[4] = m[5]; out[5] = m[6];
    out[6] = m[8]; out[7] = m[9]; out[8] = m[10];
    return out;
  }

  /* ---------------- shaders ---------------- */

  var VERT = [
    'attribute vec3 aPos;',
    'attribute vec3 aNrm;',
    'uniform mat4 uMVP;',
    'uniform mat3 uN;',
    'varying vec3 vN;',
    'varying vec3 vW;',
    'void main(){',
    '  vN = normalize(uN * aNrm);',
    '  vW = aPos;',
    '  gl_Position = uMVP * vec4(aPos,1.0);',
    '}'
  ].join('\n');

  var FRAG = [
    'precision mediump float;',
    'varying vec3 vN;',
    'varying vec3 vW;',
    'uniform vec3 uColor;',
    'uniform vec3 uEmissive;',
    'uniform float uGlow;',
    'uniform float uTime;',
    'uniform float uAlpha;',
    'void main(){',
    '  vec3 N = normalize(vN);',
    '  vec3 L = normalize(vec3(0.35,0.85,0.45));',
    '  vec3 V = normalize(vec3(0.0,0.15,1.0));',
    '  float ndl = max(dot(N,L),0.0);',
    '  float rim = pow(1.0 - max(dot(N,V),0.0), 2.4);',
    '  float fres = pow(1.0 - max(dot(N,V),0.0), 3.0);',
    '  vec3 gold = vec3(0.831,0.659,0.325);',
    '  vec3 base = uColor * (0.22 + 0.78 * ndl);',
    '  vec3 spec = vec3(1.0) * pow(max(dot(reflect(-L,N),V),0.0), 42.0) * 0.55;',
    '  vec3 col = base + spec + uEmissive * uGlow + gold * rim * 0.65 + uColor * fres * 0.35;',
    '  col += 0.04 * sin(vW.y * 18.0 + uTime * 2.0);',
    '  gl_FragColor = vec4(col, uAlpha);',
    '}'
  ].join('\n');

  var PVERT = [
    'attribute vec3 aPos;',
    'attribute float aSize;',
    'attribute float aSeed;',
    'uniform mat4 uMVP;',
    'uniform float uTime;',
    'uniform float uAmp;',
    'uniform float uGather;',
    'uniform float uSwirl;',
    'uniform float uDrift;',
    'varying float vA;',
    'void main(){',
    '  float spin = uTime * (0.4 + aSeed * 1.2) * (1.0 + uSwirl) + aSeed * 6.28;',
    '  vec3 p = aPos;',
    '  p.xy += vec2(cos(spin), sin(spin)) * (0.08 + uAmp * 0.2);',
    '  p *= (1.0 + uAmp * 0.15) * (1.0 - uGather * 0.45);',
    '  p += vec3(sin(uTime*0.30+aSeed*6.28), cos(uTime*0.23+aSeed*4.00), sin(uTime*0.27+aSeed*5.00)) * uDrift;',
    '  vec4 mv = uMVP * vec4(p,1.0);',
    '  gl_Position = mv;',
    '  gl_PointSize = aSize * (1.0 + uAmp * 1.8) * (26.0 / max(mv.w, 0.4));',
    '  vA = 0.35 + 0.65 * fract(aSeed + uTime * 0.05);',
    '}'
  ].join('\n');

  var PFRAG = [
    'precision mediump float;',
    'varying float vA;',
    'uniform vec3 uColor;',
    'void main(){',
    '  vec2 c = gl_PointCoord - 0.5;',
    '  float d = dot(c,c);',
    '  if(d > 0.25) discard;',
    '  float a = (1.0 - smoothstep(0.05, 0.25, d)) * vA;',
    '  gl_FragColor = vec4(uColor, a);',
    '}'
  ].join('\n');

  function compile(gl, type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      try { console.warn('[ILNoahAvatar] shader', gl.getShaderInfoLog(sh)); } catch (e) {}
      gl.deleteShader(sh);
      return null;
    }
    return sh;
  }

  function makeProgram(gl, vs, fs) {
    var v = compile(gl, gl.VERTEX_SHADER, vs);
    var f = compile(gl, gl.FRAGMENT_SHADER, fs);
    if (!v || !f) return null;
    var p = gl.createProgram();
    gl.attachShader(p, v);
    gl.attachShader(p, f);
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      try { console.warn('[ILNoahAvatar] link', gl.getProgramInfoLog(p)); } catch (e) {}
      return null;
    }
    return p;
  }

  /* ---------------- geometry ---------------- */

  function pushTri(pos, nrm, ax,ay,az, bx,by,bz, cx,cy,cz) {
    var ux = bx - ax, uy = by - ay, uz = bz - az;
    var vx = cx - ax, vy = cy - ay, vz = cz - az;
    var nx = uy * vz - uz * vy;
    var ny = uz * vx - ux * vz;
    var nz = ux * vy - uy * vx;
    var len = Math.hypot(nx, ny, nz) || 1;
    nx /= len; ny /= len; nz /= len;
    pos.push(ax,ay,az, bx,by,bz, cx,cy,cz);
    nrm.push(nx,ny,nz, nx,ny,nz, nx,ny,nz);
  }

  function pushTriN(pos, nrm, pa,na, pb,nb, pc,nc) {
    pos.push(pa[0],pa[1],pa[2], pb[0],pb[1],pb[2], pc[0],pc[1],pc[2]);
    nrm.push(na[0],na[1],na[2], nb[0],nb[1],nb[2], nc[0],nc[1],nc[2]);
  }

  function pack(pos, nrm) {
    return { pos: new Float32Array(pos), nrm: new Float32Array(nrm), count: pos.length / 3 };
  }

  function icosahedron(scale) {
    var t = (1 + Math.sqrt(5)) / 2;
    var verts = [
      [-1,t,0],[1,t,0],[-1,-t,0],[1,-t,0],
      [0,-1,t],[0,1,t],[0,-1,-t],[0,1,-t],
      [t,0,-1],[t,0,1],[-t,0,-1],[-t,0,1]
    ].map(function (v) {
      var l = Math.hypot(v[0], v[1], v[2]) || 1;
      return [v[0] / l * scale, v[1] / l * scale, v[2] / l * scale];
    });
    var faces = [
      [0,11,5],[0,5,1],[0,1,7],[0,7,10],[0,10,11],
      [1,5,9],[5,11,4],[11,10,2],[10,7,6],[7,1,8],
      [3,9,4],[3,4,2],[3,2,6],[3,6,8],[3,8,9],
      [4,9,5],[2,4,11],[6,2,10],[8,6,7],[9,8,1]
    ];
    var pos = [], nrm = [];
    faces.forEach(function (f) {
      var a = verts[f[0]], b = verts[f[1]], c = verts[f[2]];
      pushTri(pos, nrm, a[0],a[1],a[2], b[0],b[1],b[2], c[0],c[1],c[2]);
    });
    return pack(pos, nrm);
  }

  function octahedron(scale) {
    var s = scale;
    var v = [[0,s,0],[0,-s,0],[s,0,0],[-s,0,0],[0,0,s],[0,0,-s]];
    /* outward-CCW winding (verified): top ring 0-4-2, 0-3-4, 0-5-3, 0-2-5;
       bottom ring 1-2-4, 1-4-3, 1-3-5, 1-5-2 */
    var faces = [
      [0,4,2],[0,3,4],[0,5,3],[0,2,5],
      [1,2,4],[1,4,3],[1,3,5],[1,5,2]
    ];
    var pos = [], nrm = [];
    faces.forEach(function (f) {
      var a = v[f[0]], b = v[f[1]], c = v[f[2]];
      pushTri(pos, nrm, a[0],a[1],a[2], b[0],b[1],b[2], c[0],c[1],c[2]);
    });
    return pack(pos, nrm);
  }

  function torus(R, r, seg, tube) {
    var pos = [], nrm = [];
    var i, j;
    function pt(a, b) {
      var x = Math.cos(a) * (R + Math.cos(b) * r);
      var y = Math.sin(b) * r;
      var z = Math.sin(a) * (R + Math.cos(b) * r);
      return [[x, y, z], [Math.cos(a) * Math.cos(b), Math.sin(b), Math.sin(a) * Math.cos(b)]];
    }
    for (i = 0; i < seg; i++) {
      var a0 = (i / seg) * Math.PI * 2;
      var a1 = ((i + 1) / seg) * Math.PI * 2;
      for (j = 0; j < tube; j++) {
        var b0 = (j / tube) * Math.PI * 2;
        var b1 = ((j + 1) / tube) * Math.PI * 2;
        var p00 = pt(a0, b0), p10 = pt(a1, b0), p01 = pt(a0, b1), p11 = pt(a1, b1);
        pushTriN(pos, nrm, p00[0],p00[1], p10[0],p10[1], p11[0],p11[1]);
        pushTriN(pos, nrm, p00[0],p00[1], p11[0],p11[1], p01[0],p01[1]);
      }
    }
    return pack(pos, nrm);
  }

  function cylinder(r, h, seg) {
    var pos = [], nrm = [];
    var i, y0 = -h / 2, y1 = h / 2;
    for (i = 0; i < seg; i++) {
      var a0 = (i / seg) * Math.PI * 2;
      var a1 = ((i + 1) / seg) * Math.PI * 2;
      var x0 = Math.cos(a0) * r, z0 = Math.sin(a0) * r;
      var x1 = Math.cos(a1) * r, z1 = Math.sin(a1) * r;
      var n0 = [Math.cos(a0), 0, Math.sin(a0)];
      var n1 = [Math.cos(a1), 0, Math.sin(a1)];
      pushTriN(pos, nrm, [x0,y0,z0],n0, [x1,y0,z1],n1, [x1,y1,z1],n1);
      pushTriN(pos, nrm, [x0,y0,z0],n0, [x1,y1,z1],n1, [x0,y1,z0],n0);
    }
    return pack(pos, nrm);
  }

  function crescentShell(scale) {
    var geo = icosahedron(scale);
    var p = geo.pos, i;
    for (i = 0; i < p.length; i += 3) {
      if (p[i] > 0.15 * scale) { p[i] *= 0.55; p[i + 2] *= 1.08; }
      p[i + 1] *= 0.92;
    }
    return geo;
  }

  function makeMesh(gl, geo) {
    var m = { pos: trackBuf(gl.createBuffer()), nrm: trackBuf(gl.createBuffer()), count: geo.count };
    gl.bindBuffer(gl.ARRAY_BUFFER, m.pos);
    gl.bufferData(gl.ARRAY_BUFFER, geo.pos, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, m.nrm);
    gl.bufferData(gl.ARRAY_BUFFER, geo.nrm, gl.STATIC_DRAW);
    return m;
  }

  function makeParticles(gl, n, opt) {
    opt = opt || {};
    var rMin = opt.rMin == null ? 0.7 : opt.rMin;
    var rMax = opt.rMax == null ? 2.1 : opt.rMax;
    var sMin = opt.sMin == null ? 1.2 : opt.sMin;
    var sMax = opt.sMax == null ? 3.6 : opt.sMax;
    var flat = opt.flat || 0.7;
    var pos = new Float32Array(n * 3);
    var size = new Float32Array(n);
    var seed = new Float32Array(n);
    var i, ra, rb, rr;
    for (i = 0; i < n; i++) {
      ra = Math.random() * Math.PI * 2;
      rb = (Math.random() - 0.5) * Math.PI;
      rr = rMin + Math.random() * (rMax - rMin);
      pos[i * 3] = Math.cos(ra) * Math.cos(rb) * rr;
      pos[i * 3 + 1] = Math.sin(rb) * rr * flat;
      pos[i * 3 + 2] = Math.sin(ra) * Math.cos(rb) * rr;
      size[i] = sMin + Math.random() * (sMax - sMin);
      seed[i] = Math.random();
    }
    function buf(arr) {
      var b = trackBuf(gl.createBuffer());
      gl.bindBuffer(gl.ARRAY_BUFFER, b);
      gl.bufferData(gl.ARRAY_BUFFER, arr, gl.STATIC_DRAW);
      return b;
    }
    return { pos: buf(pos), size: buf(size), seed: buf(seed), count: n };
  }

  /* ---------------- avatar scenes ----------------
     Each avatar: build(gl, q) -> scene; draw(scene, rc).
     rc = { gl, t, status, amp, beat, accent, accent2, k, uView, uProj,
            mesh(mesh,color,emissive,glow,model,alpha),
            points(p,color,o,model) }                                  */

  /* ---- 1 · Monas — crystalline Monas / orrery (default) ---- */

  function buildMonas(gl, q) {
    var seg = q.mobile ? 48 : 72, tube = q.mobile ? 10 : 14;
    return {
      moon:  makeMesh(gl, crescentShell(0.55)),
      core:  makeMesh(gl, icosahedron(0.42)),
      ringA: makeMesh(gl, torus(0.95, 0.025, seg, tube)),
      ringB: makeMesh(gl, torus(1.25, 0.018, seg, tube)),
      stem:  makeMesh(gl, cylinder(0.035, 1.15, 10)),
      cross: makeMesh(gl, cylinder(0.03, 0.7, 8)),
      parts: makeParticles(gl, q.mobile ? 120 : 220, {})
    };
  }

  function drawMonas(sc, rc) {
    var t = rc.t, k = rc.k, st = rc.status;
    var amp = rc.amp, beat = rc.beat;
    var glow = 0.35, spin = t * 0.35 * k, bob = Math.sin(t * 1.2) * 0.04;
    var partAmp = 0.15, eyeZ = 3.35;
    if (st === 'listening') {
      glow = 0.75 + amp * 1.35; spin = t * 0.55 * k;
      bob = Math.sin(t * 6) * (0.03 + amp * 0.08); partAmp = 0.55 + amp * 1.1;
    } else if (st === 'thinking') {
      glow = 0.7 + 0.25 * Math.sin(t * 4); spin = t * 1.25 * k;
      bob = Math.sin(t * 2.2) * 0.05; partAmp = 0.85 + 0.3 * Math.sin(t * 3); eyeZ = 3.15;
    } else if (st === 'speaking') {
      var b = Math.max(beat, amp, 0.35 + 0.35 * Math.sin(t * 14));
      amp = b; glow = 1.05 + b * 1.45; spin = t * 0.45 * k;
      bob = Math.sin(t * 18) * (0.02 + b * 0.06); partAmp = 0.45 + b * 0.7;
    } else {
      glow = 0.32 + 0.08 * Math.sin(t * 1.5); partAmp = 0.12;
    }
    var sAmp = 1 + amp * 0.08;
    var M = mat4Identity(), em = st === 'speaking' ? rc.accent : (st === 'listening' ? rc.accent2 : rc.accent);

    mat4FromRTS(M, 0.25, spin * 0.7, 0.1, 0, 0.28 + bob, 0, sAmp, sAmp, sAmp);
    rc.mesh(sc.moon, rc.accent2, em, glow * 0.7, M);
    mat4FromRTS(M, t * 0.2 * k, spin, 0, 0, bob * 0.5, 0, sAmp, sAmp, sAmp);
    rc.mesh(sc.core, rc.accent, em, glow, M);
    mat4FromRTS(M, Math.PI / 2.2, spin * 0.4, 0.2, 0, bob, 0, 1, 1, 1);
    rc.mesh(sc.ringA, rc.accent2, rc.accent2, glow * 0.55, M);
    mat4FromRTS(M, 0.4, -spin * 0.55, Math.PI / 5, 0, bob * 0.3, 0, 1, 1, 1);
    rc.mesh(sc.ringB, rc.accent, rc.accent, glow * 0.4, M);
    mat4FromRTS(M, 0, 0, 0, 0, -0.15 + bob * 0.2, 0, 1, 1, 1);
    rc.mesh(sc.stem, rc.accent2, rc.accent2, glow * 0.35, M);
    mat4FromRTS(M, 0, 0, Math.PI / 2, 0, -0.35 + bob * 0.2, 0, 1, 1, 1);
    rc.mesh(sc.cross, rc.accent2, rc.accent2, glow * 0.3, M);

    mat4FromRTS(M, 0, spin * 0.25, 0, 0, bob * 0.4, 0, 1, 1, 1);
    rc.points(sc.parts, st === 'listening' ? rc.accent2 : rc.accent,
      { amp: partAmp, gather: 0, swirl: 0, drift: 0 }, M);
    return eyeZ;
  }

  /* ---- 2 · Orrery — ringed worlds ---- */

  function buildOrrery(gl, q) {
    var seg = q.mobile ? 40 : 64;
    var planets = [];
    var defs = [
      { ring: 0, n: 2, size: 0.055 }, { ring: 1, n: 2, size: 0.075 }, { ring: 2, n: 2, size: 0.06 }
    ];
    var pi = 0;
    defs.forEach(function (d, ri) {
      for (var i = 0; i < d.n; i++) {
        planets.push({
          mesh: makeMesh(gl, icosahedron(d.size)),
          ring: ri,
          phase: (i / d.n) * Math.PI * 2 + ri * 1.3,
          speed: (0.55 + ri * 0.28) * (ri % 2 ? -1 : 1),
          size: d.size
        });
        pi++;
      }
    });
    return {
      core: makeMesh(gl, icosahedron(0.34)),
      rings: [
        { mesh: makeMesh(gl, torus(0.70, 0.014, seg, 8)), tilt: [Math.PI / 2.4, 0.15],  prec: 0.10 },
        { mesh: makeMesh(gl, torus(1.00, 0.011, seg, 8)), tilt: [0.50, Math.PI / 6],     prec: -0.07 },
        { mesh: makeMesh(gl, torus(1.30, 0.009, seg, 8)), tilt: [Math.PI / 2.8, -0.30],  prec: 0.05 }
      ],
      radii: [0.70, 1.00, 1.30],
      planets: planets,
      parts: makeParticles(gl, q.mobile ? 90 : 160, { rMin: 1.5, rMax: 2.6 })
    };
  }

  var _omA = new Float32Array(16), _omB = new Float32Array(16), _omC = new Float32Array(16);

  function drawOrrery(sc, rc) {
    var t = rc.t, k = rc.k, st = rc.status;
    var amp = rc.amp, beat = rc.beat;
    var speedMul = 1, glow = 0.5, precMul = 1, bob = Math.sin(t * 1.1) * 0.03;
    if (st === 'listening')      { speedMul = 2.2; glow = 0.8 + amp * 1.2; }
    else if (st === 'thinking')  { speedMul = 3.0; precMul = 4.0; glow = 0.75 + 0.25 * Math.sin(t * 5); }
    else if (st === 'speaking')  { var b = Math.max(beat, amp); speedMul = 1.4; glow = 1.0 + b * 1.4; }
    else                         { glow = 0.45 + 0.08 * Math.sin(t * 1.4); }
    var M = mat4Identity();
    var coreS = 1 + (st === 'speaking' ? Math.max(beat, amp) * 0.14 : amp * 0.06);
    mat4FromRTS(M, t * 0.25 * k, t * 0.4 * k, 0, 0, bob, 0, coreS, coreS, coreS);
    rc.mesh(sc.core, rc.accent, rc.accent, glow, M);

    var ri, r;
    for (ri = 0; ri < sc.rings.length; ri++) {
      r = sc.rings[ri];
      mat4FromRTS(M, r.tilt[0] + t * r.prec * precMul * k, t * 0.12 * k, r.tilt[1], 0, bob * 0.5, 0, 1, 1, 1);
      rc.mesh(r.mesh, rc.accent2, rc.accent2, glow * 0.5, M);
    }
    var pi, p, a, R;
    for (pi = 0; pi < sc.planets.length; pi++) {
      p = sc.planets[pi]; R = sc.radii[p.ring]; r = sc.rings[p.ring];
      a = p.phase + t * p.speed * speedMul * k;
      mat4FromRTS(_omA, 0, a, 0, 0, 0, 0, 1, 1, 1);
      mat4FromRTS(_omB, 0, 0, 0, R, 0, 0, p.size / 0.06, p.size / 0.06, p.size / 0.06);
      mat4Multiply(_omC, _omA, _omB);
      mat4FromRTS(_omA, r.tilt[0], 0, r.tilt[1], 0, bob * 0.5, 0, 1, 1, 1);
      mat4Multiply(M, _omA, _omC);
      var pg = glow * (0.8 + 0.4 * Math.sin(t * 3 + p.phase));
      rc.mesh(p.mesh, rc.accent, rc.accent2, pg, M);
    }
    mat4FromRTS(M, 0, t * 0.1 * k, 0, 0, 0, 0, 1, 1, 1);
    rc.points(sc.parts, rc.accent, { amp: 0.2 + amp * 0.5, gather: 0, swirl: 0.4 * speedMul * k, drift: 0 }, M);
    return 3.6;
  }

  /* ---- 3 · Sigil — radiant sigil core ---- */

  function buildSigil(gl, q) {
    var seg = q.mobile ? 40 : 64;
    function tickRing(R, nTicks) {
      var ticks = [];
      for (var i = 0; i < nTicks; i++) {
        var a = (i / nTicks) * Math.PI * 2;
        ticks.push({ mesh: makeMesh(gl, cylinder(0.008, 0.07, 6)), ang: a, R: R });
      }
      return ticks;
    }
    var spokes = [];
    for (var s = 0; s < 8; s++) {
      spokes.push({ mesh: makeMesh(gl, cylinder(0.01, 0.5, 6)), ang: (s / 8) * Math.PI * 2 });
    }
    return {
      core: makeMesh(gl, octahedron(0.36)),
      ringIn: makeMesh(gl, torus(0.62, 0.016, seg, 8)),
      ringOut: makeMesh(gl, torus(0.86, 0.012, seg, 8)),
      ticksIn: tickRing(0.62, 12),
      ticksOut: tickRing(0.86, 16),
      spokes: spokes,
      parts: makeParticles(gl, q.mobile ? 80 : 140, { rMin: 0.9, rMax: 1.8, flat: 0.25 })
    };
  }

  var _sgA = new Float32Array(16), _sgB = new Float32Array(16), _sgC = new Float32Array(16);

  function sigilTick(rc, tick, groupM, glow) {
    mat4FromRTS(_sgA, 0, 0, tick.ang, 0, 0, 0, 1, 1, 1);
    mat4FromRTS(_sgB, 0, 0, 0, Math.cos(tick.ang) * tick.R, Math.sin(tick.ang) * tick.R, 0, 1, 1, 1);
    mat4Multiply(_sgC, _sgA, _sgB);
    var M = mat4Identity();
    mat4Multiply(M, groupM, _sgC);
    rc.mesh(tick.mesh, rc.accent2, rc.accent2, glow, M);
  }

  function drawSigil(sc, rc) {
    var t = rc.t, k = rc.k, st = rc.status;
    var amp = rc.amp, beat = rc.beat;
    var spinIn = 0.5, spinOut = -0.35, glow = 0.55, strobe = 0;
    if (st === 'listening')      { spinIn = 1.6; spinOut = -1.2; glow = 0.85 + amp * 1.1; }
    else if (st === 'thinking')  { spinIn = 3.2; spinOut = -2.6; glow = 0.8; strobe = 0.3 * Math.sin(t * 9); }
    else if (st === 'speaking')  { var b = Math.max(beat, amp); spinIn = 0.9; spinOut = -0.7; glow = 1.0 + b * 1.4; }
    else                         { glow = 0.5 + 0.1 * Math.sin(t * 1.6); }
    glow = Math.max(0.15, glow + strobe);
    var M = mat4Identity();
    var coreS = 1 + (st === 'speaking' ? Math.max(beat, amp) * 0.22 : 0.05 * Math.sin(t * 2));
    mat4FromRTS(M, t * 0.3 * k, t * 0.5 * k, 0, 0, 0, 0, coreS, coreS, coreS);
    rc.mesh(sc.core, rc.accent, rc.accent, glow * 1.1, M);

    var gIn = mat4Identity(), gOut = mat4Identity();
    mat4FromRTS(gIn, 0, 0, t * spinIn * k, 0, 0, 0, 1, 1, 1);
    mat4FromRTS(gOut, 0, 0, t * spinOut * k, 0, 0, 0, 1, 1, 1);
    rc.mesh(sc.ringIn, rc.accent, rc.accent2, glow * 0.7, gIn);
    rc.mesh(sc.ringOut, rc.accent2, rc.accent, glow * 0.55, gOut);
    var i;
    for (i = 0; i < sc.ticksIn.length; i++) sigilTick(rc, sc.ticksIn[i], gIn, glow * 0.8);
    for (i = 0; i < sc.ticksOut.length; i++) sigilTick(rc, sc.ticksOut[i], gOut, glow * 0.65);
    for (i = 0; i < sc.spokes.length; i++) {
      var sp = sc.spokes[i];
      mat4FromRTS(_sgA, 0, 0, sp.ang, 0, 0, 0, 1, 1, 1);
      mat4FromRTS(_sgB, 0, 0, 0, Math.cos(sp.ang) * 0.44, Math.sin(sp.ang) * 0.44, 0, 1, 1 + amp * 0.35, 1);
      mat4Multiply(_sgC, _sgA, _sgB);
      mat4Multiply(M, gIn, _sgC);
      rc.mesh(sp.mesh, rc.accent2, rc.accent2, glow * 0.5, M);
    }
    mat4FromRTS(M, 0, 0, t * 0.2 * k, 0, 0, 0, 1, 1, 1);
    rc.points(sc.parts, rc.accent, { amp: 0.25 + amp * 0.6, gather: 0, swirl: spinIn * 0.4, drift: 0 }, M);
    return 3.4;
  }

  /* ---- 4 · Wisp — nebula ghost ---- */

  function buildWisp(gl, q) {
    var seg = q.mobile ? 40 : 64;
    var knots = [];
    for (var i = 0; i < 5; i++) {
      knots.push({
        mesh: makeMesh(gl, icosahedron(0.05)),
        p1: i * 1.7, p2: i * 2.3, p3: i * 1.1,
        f1: 0.31 + i * 0.05, f2: 0.23 + i * 0.04, f3: 0.27 + i * 0.06
      });
    }
    return {
      core: makeMesh(gl, icosahedron(0.16)),
      ghostA: makeMesh(gl, torus(1.05, 0.02, seg, 8)),
      ghostB: makeMesh(gl, torus(1.45, 0.015, seg, 8)),
      knots: knots,
      nebula: makeParticles(gl, q.mobile ? 200 : 420,
        { rMin: 0.3, rMax: 2.3, sMin: 2.5, sMax: 7.0, flat: 0.8 })
    };
  }

  function drawWisp(sc, rc) {
    var t = rc.t, k = rc.k, st = rc.status;
    var amp = rc.amp, beat = rc.beat;
    var gather = 0, swirl = 1, drift = 0.35, glow = 0.4, knotMul = 1;
    if (st === 'listening')      { gather = 0.55; swirl = 1.8; glow = 0.7 + amp * 1.0; }
    else if (st === 'thinking')  { swirl = 3.0; knotMul = 2.0; glow = 0.65 + 0.25 * Math.sin(t * 4); drift = 0.5; }
    else if (st === 'speaking')  { var b = Math.max(beat, amp); gather = 0.15; glow = 0.9 + b * 1.2; drift = 0.3 + b * 0.3; }
    else                         { glow = 0.35 + 0.08 * Math.sin(t * 1.3); }
    var M = mat4Identity();
    var breathe = 1 + 0.06 * Math.sin(t * 1.8) + (st === 'speaking' ? Math.max(beat, amp) * 0.1 : 0);
    mat4FromRTS(M, t * 0.2 * k, t * 0.33 * k, 0, 0, 0, 0, breathe, breathe, breathe);
    rc.mesh(sc.core, rc.accent, rc.accent, glow * 0.8, M);

    mat4FromRTS(M, Math.PI / 2.5, t * 0.08 * k, 0.3, 0, 0, 0, 1, 1, 1);
    rc.mesh(sc.ghostA, rc.accent2, rc.accent2, glow * 0.35, M, 0.55);
    mat4FromRTS(M, 0.6, -t * 0.06 * k, Math.PI / 4, 0, 0, 0, 1, 1, 1);
    rc.mesh(sc.ghostB, rc.accent, rc.accent, glow * 0.3, M, 0.5);

    var i, kn;
    for (i = 0; i < sc.knots.length; i++) {
      kn = sc.knots[i];
      var x = Math.sin(t * kn.f1 * knotMul * k + kn.p1) * 1.2;
      var y = Math.sin(t * kn.f2 * knotMul * k + kn.p2) * 0.7;
      var z = Math.cos(t * kn.f3 * knotMul * k + kn.p3) * 1.2;
      mat4FromRTS(M, t * k + kn.p1, kn.p2, 0, x, y, z, 1, 1, 1);
      rc.mesh(kn.mesh, rc.accent, rc.accent2, glow * (0.9 + 0.4 * Math.sin(t * 2 + kn.p1)), M);
    }
    mat4FromRTS(M, 0, t * 0.05 * k, 0, 0, 0, 0, 1, 1, 1);
    rc.points(sc.nebula, rc.accent,
      { amp: 0.3 + amp * 0.8, gather: gather, swirl: swirl, drift: drift * k }, M);
    return 3.8;
  }

  /* ---------------- catalog ---------------- */

  var AVATARS = [
    { id: 'monas',  label: 'Monas',      hint: 'Crystalline Monas · orrery rings',   build: buildMonas,  draw: drawMonas },
    { id: 'orrery', label: 'Orrery',      hint: 'Ringed worlds · orbital mechanics',  build: buildOrrery, draw: drawOrrery },
    { id: 'sigil',  label: 'Sigil Core',  hint: 'Radiant sigil · counter-rotating glyph rings', build: buildSigil, draw: drawSigil },
    { id: 'wisp',   label: 'Wisp',        hint: 'Nebula ghost · drifting star-wisp',  build: buildWisp,  draw: drawWisp }
  ];
  var AVATARS_BY_ID = {};
  AVATARS.forEach(function (a) { AVATARS_BY_ID[a.id] = a; });

  /* ---------------- engine ---------------- */

  /* buffer tracking so avatar switches don't leak GL resources */
  var _track = null;
  function trackBuf(b) { if (_track) _track.push(b); return b; }

  function prefersReduced() {
    try {
      return !!(g.matchMedia && g.matchMedia('(prefers-reduced-motion: reduce)').matches);
    } catch (e) { return false; }
  }

  function fallbackHTML(name, label) {
    return '<div class="il-muse-3d__fallback" aria-hidden="true">' +
      '<div class="il-muse-3d__monas"><span class="il-muse-3d__core"></span><span class="il-muse-3d__glyph"></span></div>' +
      '</div>' +
      '<span class="il-muse-3d__badge" data-noah-badge title="Renders on-device in your browser · no cloud">' +
      name + ' · ' + label + ' 3D</span>';
  }

  function accentPair(key) {
    var a = ACCENTS[key] || ACCENTS.cyan;
    var second = (key === 'gold') ? ACCENTS.cyan.rgb : [0.831, 0.659, 0.325];
    return { primary: a.rgb, secondary: second, css: a.css, label: a.label };
  }

  function createInstance(slot, opts) {
    opts = opts || {};
    var prof = getProfile();
    var root = document.createElement('div');
    root.className = 'il-muse-3d';
    root.setAttribute('data-noah-avatar', '1');
    root.setAttribute('role', 'img');
    root.setAttribute('aria-label', 'Noah voice-reactive 3D avatar');
    root.innerHTML = fallbackHTML(prof.name, AVATARS_BY_ID[prof.avatar].label);
    slot.appendChild(root);
    if (opts.cinema) slot.classList.add('il-muse-3d-slot--cinema');

    var mobile = (typeof opts.mobile === 'boolean')
      ? opts.mobile
      : (g.matchMedia && g.matchMedia('(max-width: 768px)').matches);

    var state = {
      status: 'idle',
      avatar: AVATARS_BY_ID[opts.avatar] ? opts.avatar : prof.avatar,
      accentKey: ACCENTS[opts.accent] ? opts.accent : prof.accent,
      intensityKey: INTENSITY[opts.intensity] ? opts.intensity : prof.intensity,
      name: (typeof opts.name === 'string' && opts.name.trim()) ? opts.name.trim().slice(0, 40) : prof.name,
      amp: 0, speakBeat: 0, time: 0,
      alive: true, paused: false, reduced: prefersReduced(),
      cinema: !!opts.cinema, mobile: mobile,
      eyeZCur: null, bornAt: null /* status-transition smoothing fields */
    };
    var pair = accentPair(state.accentKey);
    var kScale = INTENSITY[state.intensityKey].scale;

    var api = {
      root: root, slot: slot,
      setStatus: function (s) {
        state.status = (s === 'listening' || s === 'thinking' || s === 'speaking') ? s : 'idle';
        if (state.reduced) renderStatic();
      },
      setAvatar: function (id) {
        if (!AVATARS_BY_ID[id] || id === state.avatar) return;
        state.avatar = id;
        rebuildScene();
        updateBadge();
        if (state.reduced) renderStatic();
      },
      setAccent: function (key) {
        if (!ACCENTS[key]) return;
        state.accentKey = key; pair = accentPair(key);
        if (state.reduced) renderStatic();
      },
      setIntensity: function (key) {
        if (!INTENSITY[key]) return;
        state.intensityKey = key; kScale = INTENSITY[key].scale;
        if (state.reduced) renderStatic();
      },
      setName: function (n) {
        if (typeof n === 'string' && n.trim()) { state.name = n.trim().slice(0, 40); updateBadge(); }
      },
      setAmplitude: function (a) { state.amp = Math.max(0, Math.min(1, a || 0)); },
      pulseSpeak: function (v) { state.speakBeat = Math.max(state.speakBeat, v == null ? 1 : v); },
      getStatus: function () { return state.status; },
      getAvatar: function () { return state.avatar; },
      applyProfile: function () {
        var p = getProfile();
        api.setName(p.name);
        api.setAccent(p.accent);
        api.setIntensity(p.intensity);
        api.setAvatar(p.avatar);
      },
      destroy: function () {
        state.alive = false;
        try { if (raf) g.cancelAnimationFrame(raf); } catch (e) {}
        if (io) { try { io.disconnect(); } catch (e2) {} }
        if (ro) { try { ro.disconnect(); } catch (e3) {} }
        g.removeEventListener('il-muse-speak-boundary', onBoundary);
        g.removeEventListener('il-muse-speak-amp', onAmp);
        stopMic();
        freeScene();
        var ix = registry.indexOf(api);
        if (ix >= 0) registry.splice(ix, 1);
        if (root.parentNode) root.parentNode.removeChild(root);
      }
    };

    function updateBadge() {
      var b = root.querySelector('[data-noah-badge]');
      if (b) b.textContent = state.name + ' · ' + AVATARS_BY_ID[state.avatar].label + ' 3D';
    }

    if (!g.WebGLRenderingContext) {
      root.classList.add('is-fallback');
      return api;
    }
    /* reduced-motion keeps going: one static WebGL frame, no animation loop */

    var canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    root.insertBefore(canvas, root.firstChild);
    var gl = canvas.getContext('webgl', {
      alpha: true, antialias: true, premultipliedAlpha: true, powerPreference: 'high-performance'
    }) || canvas.getContext('experimental-webgl');
    if (!gl) { root.classList.add('is-fallback'); return api; }
    root.classList.add('is-webgl');

    var meshProg = makeProgram(gl, VERT, FRAG);
    var partProg = makeProgram(gl, PVERT, PFRAG);
    if (!meshProg || !partProg) {
      root.classList.add('is-fallback');
      root.classList.remove('is-webgl');
      return api;
    }

    var L = {
      mesh: {
        aPos: gl.getAttribLocation(meshProg, 'aPos'),
        aNrm: gl.getAttribLocation(meshProg, 'aNrm'),
        uMVP: gl.getUniformLocation(meshProg, 'uMVP'),
        uN: gl.getUniformLocation(meshProg, 'uN'),
        uColor: gl.getUniformLocation(meshProg, 'uColor'),
        uEmissive: gl.getUniformLocation(meshProg, 'uEmissive'),
        uGlow: gl.getUniformLocation(meshProg, 'uGlow'),
        uTime: gl.getUniformLocation(meshProg, 'uTime'),
        uAlpha: gl.getUniformLocation(meshProg, 'uAlpha')
      },
      part: {
        aPos: gl.getAttribLocation(partProg, 'aPos'),
        aSize: gl.getAttribLocation(partProg, 'aSize'),
        aSeed: gl.getAttribLocation(partProg, 'aSeed'),
        uMVP: gl.getUniformLocation(partProg, 'uMVP'),
        uTime: gl.getUniformLocation(partProg, 'uTime'),
        uAmp: gl.getUniformLocation(partProg, 'uAmp'),
        uGather: gl.getUniformLocation(partProg, 'uGather'),
        uSwirl: gl.getUniformLocation(partProg, 'uSwirl'),
        uDrift: gl.getUniformLocation(partProg, 'uDrift'),
        uColor: gl.getUniformLocation(partProg, 'uColor')
      }
    };

    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.clearColor(VOID[0], VOID[1], VOID[2], 0);

    var uMVP = mat4Identity(), uView = mat4Identity(), uProj = mat4Identity();
    var uModel = mat4Identity(), uN = new Float32Array(9), tmp = mat4Identity();

    function drawMeshEntry(mesh, color, emissive, glow, model, alpha) {
      mat4Multiply(uMVP, uView, model);
      mat4Multiply(tmp, uProj, uMVP);
      mat3NormalFromMat4(uN, model);
      gl.useProgram(meshProg);
      gl.uniformMatrix4fv(L.mesh.uMVP, false, tmp);
      gl.uniformMatrix3fv(L.mesh.uN, false, uN);
      gl.uniform3fv(L.mesh.uColor, color);
      gl.uniform3fv(L.mesh.uEmissive, emissive);
      gl.uniform1f(L.mesh.uGlow, glow);
      gl.uniform1f(L.mesh.uTime, state.time);
      gl.uniform1f(L.mesh.uAlpha, alpha == null ? 0.96 : alpha);
      gl.bindBuffer(gl.ARRAY_BUFFER, mesh.pos);
      gl.enableVertexAttribArray(L.mesh.aPos);
      gl.vertexAttribPointer(L.mesh.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, mesh.nrm);
      gl.enableVertexAttribArray(L.mesh.aNrm);
      gl.vertexAttribPointer(L.mesh.aNrm, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, mesh.count);
    }

    function drawPointsEntry(p, color, o, model) {
      mat4Multiply(uMVP, uView, model);
      mat4Multiply(tmp, uProj, uMVP);
      gl.useProgram(partProg);
      gl.uniformMatrix4fv(L.part.uMVP, false, tmp);
      gl.uniform1f(L.part.uTime, state.time);
      gl.uniform1f(L.part.uAmp, o.amp || 0);
      gl.uniform1f(L.part.uGather, o.gather || 0);
      gl.uniform1f(L.part.uSwirl, o.swirl || 0);
      gl.uniform1f(L.part.uDrift, o.drift || 0);
      gl.uniform3fv(L.part.uColor, color);
      gl.bindBuffer(gl.ARRAY_BUFFER, p.pos);
      gl.enableVertexAttribArray(L.part.aPos);
      gl.vertexAttribPointer(L.part.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, p.size);
      gl.enableVertexAttribArray(L.part.aSize);
      gl.vertexAttribPointer(L.part.aSize, 1, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, p.seed);
      gl.enableVertexAttribArray(L.part.aSeed);
      gl.vertexAttribPointer(L.part.aSeed, 1, gl.FLOAT, false, 0, 0);
      gl.depthMask(false);
      gl.drawArrays(gl.POINTS, 0, p.count);
      gl.depthMask(true);
    }

    /* scene (re)build with GL-resource tracking */
    var scene = null, avatarDef = null;
    function freeScene() {
      if (scene && scene.buffers) {
        scene.buffers.forEach(function (b) { try { gl.deleteBuffer(b); } catch (e) {} });
      }
      scene = null;
    }
    function rebuildScene() {
      freeScene();
      avatarDef = AVATARS_BY_ID[state.avatar];
      _track = [];
      var s = avatarDef.build(gl, { mobile: state.mobile });
      s.buffers = _track;
      _track = null;
      scene = s;
    }
    rebuildScene();

    /* mic (voice-reactive listening) */
    var mic = { stream: null, ctx: null, analyser: null, data: null, allowed: false, _trying: false };
    function stopMic() {
      try { if (mic.stream) mic.stream.getTracks().forEach(function (t) { t.stop(); }); } catch (e) {}
      try { if (mic.ctx && mic.ctx.close) mic.ctx.close(); } catch (e2) {}
      mic.stream = null; mic.ctx = null; mic.analyser = null; mic.data = null; mic.allowed = false;
    }
    function ensureMic() {
      if (mic.allowed || mic._trying || state.reduced) return;
      if (!g.navigator || !g.navigator.mediaDevices || !g.navigator.mediaDevices.getUserMedia) return;
      mic._trying = true;
      g.navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(function (stream) {
        mic.stream = stream;
        var AC = g.AudioContext || g.webkitAudioContext;
        if (!AC) { mic._trying = false; return; }
        mic.ctx = new AC();
        var src = mic.ctx.createMediaStreamSource(stream);
        mic.analyser = mic.ctx.createAnalyser();
        mic.analyser.fftSize = 256;
        mic.analyser.smoothingTimeConstant = 0.78;
        src.connect(mic.analyser);
        mic.data = new Uint8Array(mic.analyser.frequencyBinCount);
        mic.allowed = true;
        mic._trying = false;
      }).catch(function () { mic._trying = false; mic.allowed = false; });
    }
    function micLevel() {
      if (!mic.allowed || !mic.analyser || !mic.data) return 0;
      mic.analyser.getByteFrequencyData(mic.data);
      var sum = 0, i, n = mic.data.length;
      for (i = 0; i < n; i++) sum += mic.data[i];
      return Math.min(1, (sum / n) / 90);
    }

    function resize() {
      var dpr = Math.min(g.devicePixelRatio || 1, state.mobile ? 1.5 : 2);
      var w = Math.max(1, root.clientWidth || slot.clientWidth || 320);
      var h = Math.max(1, root.clientHeight || 200);
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
      mat4Perspective(uProj, Math.PI / 3.4, canvas.width / canvas.height, 0.1, 40);
    }

    var EYES = { monas: 3.35, orrery: 3.6, sigil: 3.4, wisp: 3.8 };

    function renderFrame() {
      var st = state.status, t = state.time;
      var amp = state.amp;
      if (st === 'listening') {
        if (!mic.allowed) ensureMic();
        var ml = micLevel();
        procPhase += 0.016 * (8 + amp * 10);
        var procedural = 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(procPhase));
        amp = Math.max(amp, mic.allowed ? ml : procedural);
        state.amp = amp;
      }
      var eyeTarget = (EYES[state.avatar] || 3.4) + (st === 'thinking' ? -0.2 : 0);
      /* Smooth camera: lerp eyeZ toward the status target instead of snapping. */
      state.eyeZCur = (state.eyeZCur == null) ? eyeTarget : state.eyeZCur + (eyeTarget - state.eyeZCur) * 0.08;
      /* Wake-in: ease animation time from stillness over the first 1.5 s. */
      if (state.bornAt == null) state.bornAt = t;
      var wake = 1, age = t - state.bornAt;
      if (age < 1.5 && age >= 0) wake = (1 - Math.cos(Math.PI * age / 1.5)) / 2;
      var bob = Math.sin(t * 1.2) * 0.04;
      mat4LookAt(uView, [0, 0.15 + bob * 0.2, state.eyeZCur], [0, 0.05, 0], [0, 1, 0]);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      var rc = {
        gl: gl, t: t * wake, status: st, amp: amp, beat: state.speakBeat,
        accent: pair.primary, accent2: pair.secondary, k: kScale,
        uView: uView, uProj: uProj,
        mesh: drawMeshEntry, points: drawPointsEntry
      };
      avatarDef.draw(scene, rc);
    }

    function renderStatic() {
      if (!gl || !scene) return;
      if (root.clientWidth && canvas.width === 0) resize();
      renderFrame();
    }

    var raf = 0, last = 0, procPhase = 0, io = null, ro = null;

    function frame(ts) {
      if (!state.alive || state.paused) { raf = 0; return; }
      raf = g.requestAnimationFrame(frame);
      if (!last) last = ts;
      var dt = Math.min(0.05, (ts - last) / 1000);
      last = ts;
      state.time += dt;
      state.speakBeat *= Math.pow(0.08, dt);
      if (root.clientWidth && (canvas.width === 0 ||
          Math.abs(canvas.width / (g.devicePixelRatio || 1) - root.clientWidth) > 2)) {
        resize();
      }
      renderFrame();
    }

    function kickLoop() {
      if (state.reduced || raf || !state.alive || state.paused) return;
      last = 0;
      raf = g.requestAnimationFrame(frame);
    }

    resize();

    if (state.reduced) {
      renderStatic();
      /* layout may settle after deferred scripts run — keep the still frame correct */
      var rsT = 0;
      g.addEventListener('resize', function () {
        if (!state.alive) return;
        if (rsT) return;
        rsT = g.setTimeout(function () { rsT = 0; resize(); renderStatic(); }, 150);
      }, { passive: true });
    } else {
      kickLoop();
      /* pause when offscreen (mobile perf + battery) */
      if (g.IntersectionObserver) {
        io = new IntersectionObserver(function (entries) {
          var vis = entries.length && entries[0].isIntersecting;
          state.paused = !vis;
          if (vis) kickLoop();
          else if (raf) { try { g.cancelAnimationFrame(raf); } catch (e) {} raf = 0; }
        }, { threshold: 0.02 });
        io.observe(root);
      }
      if (g.ResizeObserver) {
        ro = new ResizeObserver(function () { resize(); });
        ro.observe(root);
      } else {
        g.addEventListener('resize', resize, { passive: true });
      }
      /* idle vitality: first 3s must feel alive on phone */
      api.pulseSpeak(0.85);
      api.setAmplitude(0.55);
      try {
        var t0 = Date.now();
        var bootPulse = function () {
          if (!state.alive || Date.now() - t0 > 3200) return;
          api.pulseSpeak(0.35 + 0.4 * Math.random());
          api.setAmplitude(0.25 + 0.35 * Math.random());
          g.setTimeout(bootPulse, 280);
        };
        g.setTimeout(bootPulse, 180);
      } catch (eBoot) {}
    }

    var onBoundary = function () { api.pulseSpeak(1); };
    var onAmp = function (ev) {
      var d = ev && ev.detail;
      if (d && typeof d.amp === 'number') api.setAmplitude(d.amp);
      if (d && d.beat) api.pulseSpeak(d.beat);
    };
    g.addEventListener('il-muse-speak-boundary', onBoundary);
    g.addEventListener('il-muse-speak-amp', onAmp);

    return api;
  }

  /* ---------------- registry / public API ---------------- */

  var registry = [];

  function findForSlot(slot) {
    for (var i = 0; i < registry.length; i++) {
      if (registry[i].slot === slot) return registry[i];
    }
    return null;
  }

  /* An instance is orphaned when its root lost its parent, or when its slot has
     left the document (e.g. a widget rebuilt its innerHTML around the slot).
     Recovery 2026-10-01: the old check missed detached-tree orphans, leaking one
     WebGL context + rAF loop per chat re-render until the renderer hung. */
  function isOrphaned(inst) {
    if (!inst || !inst.root || !inst.root.parentNode) return true;
    try {
      if (inst.slot && typeof document !== 'undefined' && !document.contains(inst.slot)) return true;
    } catch (e) {}
    return false;
  }

  function mount(slot, opts) {
    if (!slot) return null;
    var existing = findForSlot(slot);
    if (existing) {
      if (existing.root.parentNode !== slot) slot.appendChild(existing.root);
      existing.applyProfile();
      return existing;
    }
    /* reuse orphaned instance whose root was detached (e.g. widget re-render) */
    for (var j = 0; j < registry.length; j++) {
      if (isOrphaned(registry[j])) {
        slot.appendChild(registry[j].root);
        registry[j].slot = slot;
        registry[j].applyProfile();
        return registry[j];
      }
    }
    /* self-healing cap: destroy any other detached instances before allocating
       another WebGL context, so a re-render storm can never exhaust the GPU */
    for (var k = registry.length - 1; k >= 0; k--) {
      if (isOrphaned(registry[k])) {
        try { registry[k].destroy(); } catch (eD) {}
      }
    }
    var inst = createInstance(slot, opts || {});
    registry.push(inst);
    return inst;
  }

  function syncFromApp(app, opts) {
    if (!app) return null;
    var slot = app.querySelector('[data-muse-3d-slot]');
    if (!slot) return null;
    var cinema = !!(opts && opts.cinema) || !!app.closest('[data-il-cinema], .il-cinema-muse-host');
    var inst = mount(slot, { cinema: cinema });
    if (inst) inst.setStatus(app.getAttribute('data-status') || 'idle');
    return inst;
  }

  function setProfilePatch(patch) {
    var p = saveProfile(Object.assign(getProfile(), patch || {}));
    for (var i = 0; i < registry.length; i++) {
      try { registry[i].applyProfile(); } catch (e) {}
    }
    try {
      var ev;
      if (typeof CustomEvent === 'function') ev = new CustomEvent('il-noah-profile', { detail: p });
      else { ev = document.createEvent('CustomEvent'); ev.initCustomEvent('il-noah-profile', false, false, p); }
      g.dispatchEvent(ev);
    } catch (e2) {}
    return p;
  }

  g.ILNoahAvatar = {
    mount: mount,
    syncFromApp: syncFromApp,
    getProfile: getProfile,
    saveProfile: saveProfile,
    setProfilePatch: setProfilePatch,
    AVATARS: AVATARS,
    ACCENTS: ACCENTS,
    INTENSITY: INTENSITY,
    PROFILE_KEY: PROFILE_KEY,
    VERSION: '2.0.0',
    get instances() { return registry.slice(); }
  };

})(typeof window !== 'undefined' ? window : this);
;

/* ---- source: assets/il-muse.js (90003 bytes) ---- */
/**
 * IL Muse / Noah — Muse-class interaction shell (Interstitium Labs).
 * Mobile hooks: full-bleed shell ≤768px / standalone / Capacitor (see il-muse-mobile.css).
 * Brand: cyan/gold/void + Interstitium lockup — not Meta colors or trademarks.
 * Default avatar theme: Dee (Monas-derived geometric mark) — Interstitium original artwork;
 *   inspired by historical John Dee; not a museum portrait or Meta Noah.
 * Voice-reactive 3D stage: optional il-muse-3d.js (WebGL monas/orrery). SVG picker remains fallback.
 * Interaction patterns inspired by a public assistant design posts (introducing.muse.ai).
 * NOT Meta proprietary code, assets, or trademarks. Educational Socratic DevOps tutor.
 *
 * Optional deps: il-coach.js, il-model-router.js, il-model-analytics.js, il-adaptive.js
 * Config: window.IL_MUSE = { endpoint?, ollamaEndpoint? } — never commit secrets.
 * Storage: localStorage il.muse.v1
 */
(function (g) {
  'use strict';

  var STORAGE = 'il.muse.v1';

  /** Avatar themes — SVG marks in /assets/. Dee is default. */
  var AVATARS = [
    { id: 'dee', label: 'Dee', src: '/assets/il-muse-avatar-dee.svg', hint: 'Monas / hermetic scholar' },
    { id: 'sigil', label: 'Sigil', src: '/assets/il-muse-avatar-sigil.svg', hint: 'Interstitium orbital' },
    { id: 'cap', label: 'Cap', src: '/assets/il-muse-avatar-cap.svg', hint: 'Scholar hood silhouette' }
  ];
  var AVATAR_DEFAULT = 'dee';
  var PERSONALITY_DEE = 'Dee · precise · Socratic · hermetic scholar';
  var PERSONALITY_LEGACY = 'Socratic · precise · patient';

  function avatarById(id) {
    var i;
    for (i = 0; i < AVATARS.length; i++) {
      if (AVATARS[i].id === id) return AVATARS[i];
    }
    return AVATARS[0];
  }


  function router() {
    return g.IL_MODEL_ROUTER || g.ILModelRouter || null;
  }

  function analytics() {
    return g.ILModelAnalytics || g.IL_MODEL_ANALYTICS || null;
  }
  var ST = { idle: 'Idle', thinking: 'Thinking', listening: 'Listening', speaking: 'Speaking' };

  function uid(p) {
    return (p || 'id') + '-' + Math.random().toString(36).slice(2, 9);
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function emptyState() {
    return {
      v: 1,
      name: 'Noah',
      personality: PERSONALITY_DEE,
      avatarId: AVATAR_DEFAULT,
      tone: 'coach',
      memories: [],
      speak: true,
      voiceURI: '',
      goals: [
        { id: 'g1', title: 'Place the adaptive field', done: false },
        { id: 'g2', title: 'Finish one SuperLab drill', done: false },
        { id: 'g3', title: 'Explain a CIDR prefix out loud', done: false }
      ],
      artifacts: [],
      activity: [],
      inbox: [],
      lastNudgeAt: 0,
      notifOptIn: false,
      chats: {
        main: { id: 'main', title: 'Main chat', messages: [] },
        sides: []
      },
      activeChatId: 'main',
      updatedAt: Date.now()
    };
  }

  function load() {
    try {
      var raw = g.localStorage.getItem(STORAGE);
      if (raw) {
        var s = JSON.parse(raw);
        if (s && s.v === 1) {
          var b = emptyState();
          var merged = Object.assign(b, s, {
            chats: s.chats || b.chats,
            goals: s.goals && s.goals.length ? s.goals : b.goals,
            memories: s.memories || [],
            artifacts: s.artifacts || [],
            activity: s.activity || [],
            inbox: Array.isArray(s.inbox) ? s.inbox : [],
            lastNudgeAt: s.lastNudgeAt || 0,
            notifOptIn: !!s.notifOptIn
          });
          if (!merged.avatarId || !avatarById(merged.avatarId)) merged.avatarId = AVATAR_DEFAULT;
          if (!merged.personality || merged.personality === PERSONALITY_LEGACY) {
            merged.personality = PERSONALITY_DEE;
          }
          return merged;
        }
      }
    } catch (e) {}
    return emptyState();
  }

  function save(s) {
    s.updatedAt = Date.now();
    try { g.localStorage.setItem(STORAGE, JSON.stringify(s)); } catch (e) {}
    return s;
  }

  function pushActivity(s, text) {
    s.activity = s.activity || [];
    s.activity.unshift({ t: Date.now(), text: text });
    if (s.activity.length > 48) s.activity.length = 48;
  }

  function getChat(s, id) {
    if (!id || id === 'main') return s.chats.main;
    for (var i = 0; i < (s.chats.sides || []).length; i++) {
      if (s.chats.sides[i].id === id) return s.chats.sides[i];
    }
    return s.chats.main;
  }


  function isNarrow() {
    try { return !!(g.matchMedia && g.matchMedia('(max-width: 768px)').matches); } catch (e) { return false; }
  }
  function isNativeShell() {
    try {
      var root = document.documentElement;
      if (root && (root.classList.contains('il-capacitor') || root.classList.contains('il-standalone'))) return true;
      if (g.Capacitor) return true;
      if (g.matchMedia && g.matchMedia('(display-mode: standalone)').matches) return true;
      if (g.navigator && g.navigator.standalone === true) return true;
    } catch (e) {}
    return false;
  }
  function isMobileShell() { return isNarrow() || isNativeShell(); }

  function ensureTabNav() {
    if (document.querySelector('[data-il-muse-tabnav]')) return;
    var nav = document.createElement('nav');
    nav.className = 'il-muse-tabnav';
    nav.setAttribute('data-il-muse-tabnav', '1');
    nav.setAttribute('aria-label', 'Noah companion');
    var path = (g.location && g.location.pathname) || '';
    var items = [
      ['/coach/', 'Noah', '◆', path.indexOf('/coach') === 0],
      ['/paths/', 'Paths', '⬡', path.indexOf('/paths') === 0],
      ['/labs/', 'Labs', '▣', path.indexOf('/labs') === 0],
      ['/os/', 'OS', '◎', path.indexOf('/os') === 0 || path.indexOf('/founders') === 0]
    ];
    nav.innerHTML = items.map(function (it) {
      return '<a href="' + it[0] + '"' + (it[3] ? ' class="is-on" aria-current="page"' : '') + '>' +
        '<span class="il-muse-tabnav__glyph" aria-hidden="true">' + it[2] + '</span>' +
        '<span>' + it[1] + '</span></a>';
    }).join('');
    document.body.appendChild(nav);
  }

  function wireKeyboardAware() {
    if (g.__IL_MUSE_KB__) return;
    g.__IL_MUSE_KB__ = true;
    var vv = g.visualViewport;
    if (!vv) return;
    function sync() {
      var h = vv.height || g.innerHeight;
      var offset = (g.innerHeight || 0) - h - (vv.offsetTop || 0);
      document.documentElement.style.setProperty('--muse-vv-h', Math.round(h) + 'px');
      if (offset > 80) document.body.classList.add('il-muse-kb-open');
      else document.body.classList.remove('il-muse-kb-open');
    }
    vv.addEventListener('resize', sync, { passive: true });
    vv.addEventListener('scroll', sync, { passive: true });
    sync();
  }

  function voiceSupport() {
    var Rec = g.SpeechRecognition || g.webkitSpeechRecognition || null;
    return {
      recognition: !!Rec,
      Rec: Rec,
      synthesis: !!(g.speechSynthesis && g.SpeechSynthesisUtterance)
    };
  }

  function listVoices() {
    try { return g.speechSynthesis ? g.speechSynthesis.getVoices() || [] : []; }
    catch (e) { return []; }
  }

  function speakText(text, state, onEnd) {
    var vs = voiceSupport();
    if (!vs.synthesis || !state.speak || !text) { if (onEnd) onEnd(); return; }
    try { g.speechSynthesis.cancel(); } catch (e) {}
    var clipped = String(text).slice(0, 1400);
    var u = new g.SpeechSynthesisUtterance(clipped);
    var voices = listVoices();
    if (state.voiceURI) {
      for (var i = 0; i < voices.length; i++) {
        if (voices[i].voiceURI === state.voiceURI) { u.voice = voices[i]; break; }
      }
    }
    u.rate = 1.02;
    var ampTimer = null;
    var startAt = Date.now();
    /* ~14 chars/sec at rate 1.02 — fake amplitude if boundary events are sparse */
    var estMs = Math.max(900, Math.min(28000, (clipped.length / 14) * 1000 / 1.02));
    function emitAmp(amp, beat) {
      try {
        g.dispatchEvent(new CustomEvent('il-muse-speak-amp', { detail: { amp: amp, beat: beat || 0 } }));
      } catch (e) {}
    }
    function tickAmp() {
      var t = (Date.now() - startAt) / estMs;
      if (t >= 1) return;
      var wave = 0.35 + 0.65 * Math.abs(Math.sin(t * Math.PI * 10));
      emitAmp(wave, 0);
      ampTimer = g.setTimeout(tickAmp, 80);
    }
    u.onboundary = function (ev) {
      try {
        g.dispatchEvent(new CustomEvent('il-muse-speak-boundary', {
          detail: { charIndex: ev.charIndex || 0, name: ev.name || 'word' }
        }));
      } catch (e) {}
      emitAmp(1, 1);
    };
    function done() {
      if (ampTimer) try { clearTimeout(ampTimer); } catch (e) {}
      emitAmp(0, 0);
      if (onEnd) onEnd();
    }
    u.onend = done;
    u.onerror = done;
    g.speechSynthesis.speak(u);
    tickAmp();
  }

  function detectTopic(text) {
    if (/cidr|subnet|netmask|\/2[0-9]/i.test(text)) return 'cidr';
    if (/git|rebase|merge|commit|detached/i.test(text)) return 'git';
    if (/pod|kubectl|k8s|kubernetes|crashloop/i.test(text)) return 'k8s';
    if (/terraform|tfstate|iac/i.test(text)) return 'terraform';
    if (/jenkins|github actions|pipeline|ci\/?cd|workflow/i.test(text)) return 'ci';
    if (/linux|systemd|journalctl|chmod|ssh|oom/i.test(text)) return 'linux';
    if (/blockchain|bitcoin|ethereum|solidity|smart contract|utxo/i.test(text)) return 'blockchain';
    if (/quantum|qubit|superposition|entanglement/i.test(text)) return 'quantum';
    if (/deep work|procrastinat|study plan|time block/i.test(text)) return 'study';
    if (/interview|resume|career|salary/i.test(text)) return 'career';
    if (/devops|sre|docker|container/i.test(text)) return 'devops';
    return '';
  }

  function ideasFromAdaptive() {
    var ideas = [];
    try {
      if (g.ILAdaptive && typeof g.ILAdaptive.getState === 'function') {
        var st = g.ILAdaptive.getState();
        var topics = (st && st.topics) || {};
        Object.keys(topics).map(function (id) {
          return { id: id, mastery: topics[id].mastery || 0, status: topics[id].status };
        }).filter(function (t) {
          return t.status === 'learning' || (t.mastery > 0 && t.mastery < 0.55);
        }).sort(function (a, b) { return a.mastery - b.mastery; }).slice(0, 5)
          .forEach(function (t) {
            ideas.push({
              id: 'w-' + t.id,
              title: 'Drill weak topic: ' + t.id,
              meta: 'Mastery ' + Math.round(t.mastery * 100) + '% · Adaptive',
              href: '/adapt/'
            });
          });
      }
    } catch (e) {}
    if (!ideas.length) {
      ideas = [
        { id: 'i1', title: 'Warm up CIDR host bits', meta: 'Socratic check', href: null },
        { id: 'i2', title: 'Pod triage order', meta: 'describe → logs → probes', href: '/labs/superlab/' },
        { id: 'i3', title: 'Open Adaptive placement', meta: 'Build a weak-topic signal', href: '/adapt/' }
      ];
    }
    ideas.push({ id: 'i-sl', title: 'Enter DevOps SuperLab', meta: 'kind · Kustomize · Argo', href: '/labs/superlab/' });
    return ideas;
  }

  function isFirstPartyHref(href) {
    if (!href) return false;
    if (href.charAt(0) === '/' && href.charAt(1) !== '/') return true;
    try {
      var u = new URL(href, g.location && g.location.origin ? g.location.origin : 'https://interstitiumlabs.dev');
      var h = (u.hostname || '').toLowerCase();
      return h === 'interstitiumlabs.dev' || h === 'localhost' || h === '127.0.0.1';
    } catch (e) { return false; }
  }


  /** Muse-class multi-bubble: short sequential assistant turns (local split). */
  function splitBubbles(text, maxParts) {
    maxParts = maxParts || 4;
    var raw = String(text || '').trim();
    if (!raw) return [];
    var parts = raw.split(/\n{2,}/).map(function (p) { return p.trim(); }).filter(Boolean);
    if (parts.length === 1 && raw.length > 160) {
      var sentences = raw.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [raw];
      parts = [];
      var buf = '';
      sentences.forEach(function (s) {
        s = s.trim();
        if (!s) return;
        if ((buf + ' ' + s).trim().length > 140 && buf) {
          parts.push(buf.trim());
          buf = s;
        } else {
          buf = (buf ? buf + ' ' : '') + s;
        }
      });
      if (buf.trim()) parts.push(buf.trim());
    }
    if (parts.length > maxParts) {
      var head = parts.slice(0, maxParts - 1);
      head.push(parts.slice(maxParts - 1).join(' '));
      parts = head;
    }
    return parts.length ? parts : [raw];
  }

  /** Local-only proactive nudges (adaptive + goals). No cloud connectors. */
  function localNudges(state) {
    var out = [];
    var openGoals = (state.goals || []).filter(function (g0) { return !g0.done; }).slice(0, 2);
    openGoals.forEach(function (g0) {
      out.push({
        id: 'goal-' + g0.id,
        kind: 'goal',
        text: 'Continue goal: ' + g0.title,
        ask: 'Help me with my lab goal: ' + g0.title
      });
    });
    try {
      if (g.ILAdaptive && typeof g.ILAdaptive.getState === 'function') {
        var st = g.ILAdaptive.getState();
        var topics = (st && st.topics) || {};
        Object.keys(topics).map(function (id) {
          return { id: id, mastery: topics[id].mastery || 0, status: topics[id].status };
        }).filter(function (t) {
          return t.status === 'learning' || (t.mastery > 0 && t.mastery < 0.5);
        }).sort(function (a, b) { return a.mastery - b.mastery; }).slice(0, 2)
          .forEach(function (t) {
            out.push({
              id: 'weak-' + t.id,
              kind: 'adaptive',
              text: 'Weak signal · ' + t.id + ' (' + Math.round(t.mastery * 100) + '%)',
              ask: 'Quiz me Socratically on ' + t.id,
              href: '/adapt/'
            });
          });
      }
    } catch (e) {}
    if (!out.length) {
      out.push({
        id: 'boot-adapt',
        kind: 'boot',
        text: 'Place the adaptive field',
        ask: 'Walk me through placing the adaptive field',
        href: '/adapt/'
      });
      out.push({
        id: 'boot-sl',
        kind: 'boot',
        text: 'Enter SuperLab',
        ask: 'What should I attempt first in DevOps SuperLab?',
        href: '/labs/superlab/'
      });
    }
    return out.slice(0, 4);
  }

  function maybeApproval(userText, replyText, topic) {
    var t = ((userText || '') + ' ' + (replyText || '')).toLowerCase();
    if (/superlab|kind cluster|argo|kustomize/.test(t) || topic === 'k8s') {
      return {
        id: uid('appr'),
        title: 'Open DevOps SuperLab?',
        body: 'Local lab path — no third-party connectors. Approve to jump, or keep chatting.',
        primary: { label: 'Open SuperLab', href: '/labs/superlab/' },
        secondary: { label: 'Stay in chat', dismiss: true }
      };
    }
    if (/adaptive|placement|mastery|weak topic/.test(t)) {
      return {
        id: uid('appr'),
        title: 'Open Adaptive placement?',
        body: 'Build a weak-topic signal on-device. First-party Interstitium only.',
        primary: { label: 'Open Adaptive', href: '/adapt/' },
        secondary: { label: 'Not now', dismiss: true }
      };
    }
    if (/ollama|endpoint|model router|demand tier|scale/.test(t)) {
      return {
        id: uid('appr'),
        title: 'Review model / demand panel?',
        body: 'Lean T0 stays default. Approve to open Noah settings → Model (local policy only).',
        primary: { label: 'Open Model panel', panel: 'model' },
        secondary: { label: 'Keep lean', dismiss: true }
      };
    }
    return null;
  }

  function maybeArtifact(userText, replyText, topic) {
    var t = (userText || '') + ' ' + (replyText || '');
    if (/cidr|subnet|\/2[0-9]|prefix length|host bits/i.test(t) || topic === 'cidr') {
      return {
        id: uid('art'), kind: 'cidr', title: 'CIDR check card',
        body: 'Count host bits, name network vs broadcast, then size for hosts or routes. Say the prefix out loud before the calculator.',
        command: "python3 -c \"import ipaddress; n=ipaddress.ip_network('10.0.0.0/24'); print(n.num_addresses, list(n.hosts())[:3])\"",
        checklist: ['Prefix length?', 'Usable hosts?', 'Network vs broadcast?', 'Overlap with another route?'],
        links: [
          { href: '/adapt/', label: 'Adaptive' },
          { href: '/labs/superlab/', label: 'SuperLab' },
          { href: '/proof/', label: 'Proof export' }
        ]
      };
    }
    if (/pod|crashloop|kubectl|k8s|namespace/i.test(t) || topic === 'k8s') {
      return {
        id: uid('art'), kind: 'lab-checklist', title: 'Pod triage lab checklist',
        body: 'Stay in order — do not jump to delete/recreate. Capture evidence for proof export.',
        command: 'kubectl describe pod <name> -n <ns>; kubectl logs <name> -n <ns> --previous; kubectl get events -n <ns> --sort-by=.lastTimestamp | tail',
        checklist: ['Phase + last event', 'Logs (--previous)', 'Probes / resources / image', 'Export proof note'],
        links: [
          { href: '/labs/superlab/', label: 'SuperLab' },
          { href: '/paths/', label: 'Paths' },
          { href: '/proof/', label: 'Proof export' }
        ]
      };
    }
    if (/git|rebase|merge|cherry-pick/i.test(t) || topic === 'git') {
      return {
        id: uid('art'), kind: 'command', title: 'Git intent card',
        body: 'Published → revert. Local only → reset. Replay → cherry-pick.',
        command: 'git status -sb; git log --oneline -5; git remote -v',
        checklist: ['Is it published?', 'Named branch target?', 'Redact secrets'],
        links: [{ href: '/adapt/', label: 'Adaptive' }, { href: '/proof/', label: 'Proof export' }]
      };
    }
    if (/terraform|pipeline|ci\/?cd|linux|systemd|ansible/i.test(t)) {
      return {
        id: uid('art'), kind: 'lab-checklist', title: 'Lab drill checklist',
        body: 'Practice beats answer dumps. Bring Noah a hypothesis after one lab sitting.',
        checklist: ['One observation', 'One hypothesis', 'One command tried', 'Link proof export'],
        links: [
          { href: '/labs/superlab/', label: 'SuperLab' },
          { href: '/adapt/', label: 'Adaptive OS' },
          { href: '/proof/', label: 'Proof export' },
          { href: '/os/', label: 'Hire OS' }
        ]
      };
    }
    if (/proof|portfolio|evidence|export/i.test(t)) {
      return {
        id: uid('art'), kind: 'proof', title: 'Proof-of-work link',
        body: 'Export inspectable markdown from local adaptive + Noah + exam state — no invented server claims.',
        checklist: ['Refresh snapshot', 'Download .md or print PDF', 'Keep honesty labels'],
        links: [
          { href: '/proof/', label: 'Open proof export' },
          { href: '/os/', label: 'Hire OS loop' },
          { href: '/evidence/', label: 'Evidence wall' }
        ]
      };
    }
    if (/path|frontier|career|hire|interview/i.test(t)) {
      return {
        id: uid('art'), kind: 'link', title: 'Path / frontier deep links',
        body: 'Jump the hire loop — Adapt placement → path phase → lab → Noah → proof.',
        links: [
          { href: '/paths/', label: 'Paths' },
          { href: '/os/', label: 'Hire OS' },
          { href: '/adapt/', label: 'Adapt' },
          { href: '/labs/superlab/', label: 'SuperLab' }
        ]
      };
    }
    return null;
  }

  /** Local study nudges from goals + Adapt weak topics (no Meta push infra). */
  function buildNudgeCandidates(state) {
    var out = [];
    var seen = {};
    function add(id, title, meta, href) {
      if (seen[id]) return;
      seen[id] = 1;
      out.push({ id: id, title: title, meta: meta || '', href: href || '/coach/', t: Date.now(), read: false });
    }
    (state.goals || []).forEach(function (g0) {
      if (!g0.done) add('goal:' + g0.id, 'Goal nudge · ' + g0.title, 'Open goal · ask Noah for a Socratic next step', '/coach/');
    });
    ideasFromAdaptive().forEach(function (idea) {
      add('idea:' + idea.id, idea.title, idea.meta || 'Weak Adapt topic', idea.href || '/adapt/');
    });
    if (!out.length) {
      add('default:superlab', 'Study nudge · SuperLab sitting', '15 min · Kind + Kustomize + Argo', '/labs/superlab/');
      add('default:cidr', 'Study nudge · CIDR out loud', 'Explain a /24 before the calculator', '/adapt/');
    }
    return out.slice(0, 8);
  }

  function tryLocalNotification(title, body) {
    try {
      if (!g.Notification || Notification.permission !== 'granted') return false;
      var n = new Notification(title || 'Noah', {
        body: body || 'Time for a short study sitting.',
        tag: 'il-muse-nudge',
        silent: false
      });
      setTimeout(function () { try { n.close(); } catch (e) {} }, 8000);
      return true;
    } catch (e) { return false; }
  }

  function splitReplyBubbles(text) {
    var raw = String(text || '').trim();
    if (!raw) return [''];
    var parts = raw.split(/\n{2,}/).map(function (p) { return p.trim(); }).filter(Boolean);
    if (parts.length >= 2) return parts.slice(0, 4);
    if (raw.length > 220) {
      var mid = Math.floor(raw.length / 2);
      var cut = raw.lastIndexOf('. ', mid);
      if (cut < 40) cut = raw.lastIndexOf('? ', mid);
      if (cut < 40) cut = mid;
      return [raw.slice(0, cut + 1).trim(), raw.slice(cut + 1).trim()].filter(Boolean);
    }
    return [raw];
  }


  function toRouterMessages(chat) {
    var out = [];
    (chat.messages || []).forEach(function (m) {
      if (m.role === 'user') out.push({ role: 'user', content: m.text });
      else if (m.role === 'assistant') out.push({ role: 'assistant', content: m.text });
    });
    return out.slice(-16);
  }

  function askModel(chat, topic, state) {
    var ctx = {
      museName: state.name,
      personality: state.personality + ' · tone:' + state.tone,
      memories: state.memories || [],
      topic: topic,
      task: 'coach_chat',
      taskType: 'coach_chat'
    };
    var messages = toRouterMessages(chat);
    var R = router();
    if (R && typeof R.chat === 'function') {
      return R.chat(messages, ctx);
    }
    // Fallback: ILCoach local rules
    var last = '';
    for (var i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role === 'user') { last = messages[i].content; break; }
    }
    if (g.ILCoach && typeof g.ILCoach.ask === 'function') {
      return g.ILCoach.ask(last, topic).then(function (res) {
        return {
          text: res.text || String(res),
          backendId: 'local-rules',
          modelId: 'rules',
          source: 'local-rules',
          latencyMs: 0
        };
      });
    }
    return Promise.resolve({
      text: 'Local hint engine unavailable. Load il-coach.js or configure IL_MUSE.endpoint.',
      backendId: 'local-rules',
      modelId: 'rules',
      source: 'none',
      latencyMs: 0
    });
  }

  /* Normalize router response field names */
  function normRes(res) {
    return {
      text: res.text || '',
      backendId: res.backendId || res.backend || 'local-rules',
      modelId: res.modelId || res.model || 'rules',
      source: res.source || res.backendId || 'local',
      latencyMs: res.latencyMs != null ? res.latencyMs : 0
    };
  }

  function mount(el) {
    if (!el || el.getAttribute('data-il-muse-ready')) return;
    var state = load();
    /* Noah 3D avatar profile (il-noah-profile) overlays the widget state:
       display name + avatar + accent + intensity apply on every page load. */
    try {
      if (g.ILNoahAvatar && g.ILNoahAvatar.getProfile) {
        var __nprof = g.ILNoahAvatar.getProfile();
        if (__nprof && __nprof.name) state.name = __nprof.name;
      }
    } catch (eProf) {}
    var statusKey = 'idle';
    var panelTab = 'goals';
    var recognition = null;
    var listening = false;
    var lastThumbMeta = null;
    var inflightGen = 0;
    var streamTimers = [];
    var pendingApproval = null;

    // Prefer lean T0 demand tier (scale only when demand grows)
    try {
      if (router() && router().getPolicy && router().setPolicy) {
        var pol0 = router().getPolicy();
        if (!pol0.demand_tier) router().setPolicy({ demand_tier: 'T0' });
      }
      if (router() && router().loadCatalog) router().loadCatalog();
    } catch (e) {}

    var app = document.createElement('div');
    app.className = 'il-muse-app';
    app.setAttribute('data-status', statusKey);

    function persist() { save(state); }

    function setStatus(key) {
      statusKey = key;
      app.setAttribute('data-status', key);
      var pill = app.querySelector('[data-muse-status]');
      if (pill) pill.textContent = ST[key] || key;
      var act = app.querySelector('[data-muse-activity]');
      if (act) {
        act.textContent = (state.activity[0] && state.activity[0].text) || 'Idle · waiting for your stuck question';
      }
      var live = app.querySelector('[data-muse-live]');
      var liveTxt = app.querySelector('[data-muse-live-text]');
      if (live && liveTxt) {
        var labels = {
          idle: 'Ready · ask a stuck question',
          thinking: 'Thinking…',
          listening: 'Listening…',
          speaking: 'Speaking…'
        };
        liveTxt.textContent = labels[key] || (ST[key] || key);
        live.hidden = false;
        live.setAttribute('data-live', key);
      }
      try {
        if (app.__ilMuse3d && typeof app.__ilMuse3d.setStatus === 'function') {
          app.__ilMuse3d.setStatus(key);
        }
      } catch (e3) {}
    }

    function clearStreamTimers() {
      while (streamTimers.length) {
        try { clearTimeout(streamTimers.shift()); } catch (e) {}
      }
    }

    function interruptInflight(reason) {
      inflightGen += 1;
      clearStreamTimers();
      try { if (g.speechSynthesis) g.speechSynthesis.cancel(); } catch (e) {}
      if (reason) pushActivity(state, reason);
    }

    function showApproval(opts) {
      pendingApproval = opts || null;
      render();
    }

    function dismissApproval(accepted) {
      var a = pendingApproval;
      pendingApproval = null;
      if (a && accepted && typeof a.onConfirm === 'function') a.onConfirm();
      else if (a && !accepted && typeof a.onCancel === 'function') a.onCancel();
      render();
    }

    function approvalHTML() {
      if (!pendingApproval) return '';
      var a = pendingApproval;
      return '<div class="il-muse-approve" role="dialog" aria-modal="true" aria-labelledby="il-muse-approve-title">' +
        '<div class="il-muse-approve__card">' +
        '<p class="il-muse-approve__kicker">Approval</p>' +
        '<h3 id="il-muse-approve-title">' + esc(a.title || 'Confirm') + '</h3>' +
        '<p class="il-muse-approve__body">' + esc(a.body || '') + '</p>' +
        '<div class="il-muse-approve__actions">' +
        '<button type="button" class="il-muse-approve__deny" data-muse-approve="no">' + esc(a.cancelLabel || 'Cancel') + '</button>' +
        '<button type="button" class="il-muse-approve__allow" data-muse-approve="yes">' + esc(a.confirmLabel || 'Allow') + '</button>' +
        '</div></div></div>';
    }

    function harvestNudges(force) {
      var now = Date.now();
      var minGap = 4 * 60 * 60 * 1000; /* 4h local cadence */
      if (!force && state.lastNudgeAt && (now - state.lastNudgeAt) < minGap) return;
      state.inbox = state.inbox || [];
      var cands = buildNudgeCandidates(state);
      var existing = {};
      state.inbox.forEach(function (n) { existing[n.id] = 1; });
      var added = 0;
      cands.forEach(function (c) {
        if (existing[c.id]) return;
        state.inbox.unshift(c);
        added += 1;
      });
      if (added) {
        state.lastNudgeAt = now;
        if (state.inbox.length > 24) state.inbox.length = 24;
        pushActivity(state, 'Study nudges · +' + added);
        var top = state.inbox[0];
        if (state.notifOptIn && top) {
          tryLocalNotification('Noah · study nudge', top.title);
        }
        persist();
      } else if (force) {
        state.lastNudgeAt = now;
        persist();
      }
    }

    function render() {
      var vs = voiceSupport();
      var chat = getChat(state, state.activeChatId);
      var ideas = ideasFromAdaptive();
      var demand = demandView();
      var routerState = (router() && router().getPolicy) ? router().getPolicy() : null;
      var active = activeTarget();
      var catalog = modelCatalog();
      var shell = isMobileShell();
      app.classList.toggle('il-muse-app--shell', shell);
      app.setAttribute('data-avatar', state.avatarId || AVATAR_DEFAULT);
      if (shell) {
        document.body.classList.add('il-muse-page');
        ensureTabNav();
        wireKeyboardAware();
      }

      app.innerHTML =
        mobileBar() +
        '<button type="button" class="il-muse-drawer-scrim" data-muse-scrim aria-label="Close drawer"></button>' +
        railHTML() +
        stageHTML(chat, vs) +
        panelHTML(ideas, demand, routerState, active, catalog, vs) +
        approvalHTML();

      wire(vs);
      setStatus(statusKey);
      try {
        if (panelTab === 'model' && g.ILModelPanel && typeof g.ILModelPanel.mount === 'function') {
          var mp = app.querySelector('[data-il-model-panel]');
          if (mp) g.ILModelPanel.mount(mp);
        }
      } catch (ePanel) {}
      try { attachMuse3d(); } catch (e3d) {}
      var log = app.querySelector('[data-muse-transcript]');
      if (log) log.scrollTop = log.scrollHeight;
    }

    function attachMuse3d() {
      var cinema = !!app.closest('[data-il-cinema], .il-cinema-muse-host');
      var slot = app.querySelector('[data-muse-3d-slot]');
      if (!slot) return;
      /* Recovery 2026-10-01: render() rebuilds app.innerHTML on every message, which
         orphaned the 3D slot and leaked one WebGL context + rAF loop per render
         (~6 per SEND) until the renderer hung. Reattach the single live instance
         instead of mounting anew — the expando survives innerHTML rebuilds. */
      var prev = app.__ilNoahAvatar;
      if (prev && prev.root && typeof prev.setStatus === 'function') {
        try {
          if (prev.slot !== slot) {
            slot.appendChild(prev.root);
            prev.slot = slot;
          }
          if (typeof prev.applyProfile === 'function') { try { prev.applyProfile(); } catch (eP) {} }
          prev.setStatus(statusKey);
          app.__ilMuse3d = prev; /* compat: setStatus forwarder uses __ilMuse3d */
          return;
        } catch (eRe) { /* fall through to a fresh mount */ }
      }
      /* Prefer the full Noah 3D avatar system (profile-driven); fall back to legacy stage. */
      if (g.ILNoahAvatar && typeof g.ILNoahAvatar.syncFromApp === 'function') {
        try {
          var ninst = g.ILNoahAvatar.syncFromApp(app, { cinema: cinema });
          if (ninst) {
            app.__ilNoahAvatar = ninst;
            app.__ilMuse3d = ninst; /* compat: setStatus forwarder uses __ilMuse3d */
            ninst.setStatus(statusKey);
            return;
          }
        } catch (eN3d) {}
      }
      if (!g.ILMuse3D || typeof g.ILMuse3D.syncFromApp !== 'function') return;
      var inst = g.ILMuse3D.syncFromApp(app, {
        cinema: cinema
      });
      if (inst) {
        app.__ilMuse3d = inst;
        inst.setAvatar(state.avatarId || AVATAR_DEFAULT);
        inst.setStatus(statusKey);
      }
    }

    function demandView() {
      var policy = (router() && router().getPolicy) ? router().getPolicy() : { demand_tier: 'T0', primary: 'local-rules', mode: 'auto' };
      var cat = (router() && router().getCatalog) ? router().getCatalog() : null;
      var tiersMap = (cat && cat.demand_tiers) || {
        T0: { id: 'T0', label: 'T0 Lean', description: 'Local rules + optional ≤3B on P1000. Prefer lean defaults.' },
        T1: { id: 'T1', label: 'T1 Standard', description: 'More CPU workers / 7B when concurrency grows.' },
        T2: { id: 'T2', label: 'T2 Heavy', description: 'Remote OSS GPU / OpenAI-compatible proxies when demand requires it.' }
      };
      var tid = policy.demand_tier || 'T0';
      var meta = tiersMap[tid] || { id: tid, label: tid, description: '' };
      var scale = (analytics() && analytics().scaleRecommendation)
        ? analytics().scaleRecommendation(policy)
        : { suggest_tier: null, honesty: 'Scale relative to demand — prefer lean until load grows.' };
      var ranking = [];
      try {
        if (analytics() && analytics().scores) {
          var sc = analytics().scores();
          ranking = Object.keys(sc).map(function (k) {
            var s = sc[k];
            return {
              backendId: s.backendId || '',
              modelId: s.modelId || k,
              score: s.score,
              avgLatencyMs: s.avgLatencyMs,
              n: s.n
            };
          }).sort(function (a, b) { return (b.score || 0) - (a.score || 0); }).slice(0, 5);
        }
      } catch (e) {}
      return {
        tier: { id: meta.id || tid, label: meta.label || tid, blurb: meta.description || '' },
        tiers: Object.keys(tiersMap).map(function (k) {
          return { id: k, label: (tiersMap[k].label || k), blurb: tiersMap[k].description || '' };
        }),
        suggestedTier: scale.suggest_tier || null,
        suggestReason: scale.honesty || scale.reason || null,
        scaleNote: 'Prefer lean (T0). Scale LLM relative to demand — upgrade only when concurrent seats, latency, or errors climb.',
        ranking: ranking,
        policy: policy
      };
    }

    function modelCatalog() {
      var cat = (router() && router().getCatalog) ? router().getCatalog() : null;
      if (cat && cat.models && cat.models.length) {
        // Flatten to single "catalog" select: one virtual backend per real backend id, models filtered later
        var byBackend = {};
        (cat.backends || []).forEach(function (b) {
          byBackend[b.id] = { id: b.id, label: b.label || b.id, models: [] };
        });
        (cat.models || []).forEach(function (m) {
          (m.backends || ['local-rules']).forEach(function (bid) {
            if (!byBackend[bid]) byBackend[bid] = { id: bid, label: bid, models: [] };
            byBackend[bid].models.push({ id: m.id, label: m.label || m.id, size_b: m.size_b, demand_tiers: m.demand_tiers });
          });
        });
        if (!byBackend['local-rules']) {
          byBackend['local-rules'] = { id: 'local-rules', label: 'Local Socratic rules', models: [{ id: 'local-rules', label: 'Hint engine' }] };
        }
        return Object.keys(byBackend).map(function (k) { return byBackend[k]; });
      }
      return defaultCatalog();
    }

    function defaultDemand() {
      return demandView();
    }

    function defaultCatalog() {
      return [
        { id: 'local-rules', label: 'Local Socratic rules', models: [{ id: 'local-rules', label: 'Hint engine' }] },
        { id: 'ollama', label: 'Ollama (local)', models: [
          { id: 'qwen2.5-coder-3b', label: 'Qwen2.5-Coder 3B (lean GPU)' },
          { id: 'qwen2.5-coder-7b', label: 'Qwen2.5-Coder 7B (CPU)' }
        ] }
      ];
    }

    function activeTarget() {
      var R = router();
      if (R && R.activeTarget) {
        try {
          var t = R.activeTarget();
          if (t) return { backendId: t.backendId || 'local-rules', modelId: t.modelId || 'local-rules' };
        } catch (e) {}
      }
      if (R && R.getPolicy) {
        var p = R.getPolicy();
        var rec = null;
        try { if (R.recommend) rec = R.recommend(); } catch (e2) {}
        var sel = rec && rec.selected;
        var modelId = (sel && (sel.id || sel.modelId)) || rec.primary || p.primary || 'local-rules';
        var backendId = (sel && (sel.backend || sel.backendId)) || p.backend || 'local-rules';
        if (rec && rec.primary && !rec.selected) modelId = rec.primary;
        return { backendId: backendId, modelId: modelId };
      }
      return { backendId: 'local-rules', modelId: 'local-rules' };
    }

    function mobileBar() {
      return '<div class="il-muse-mobile-bar" role="toolbar" aria-label="Noah drawers">' +
        '<button type="button" data-muse-toggle-rail aria-label="Open chats">Chats</button>' +
        '<button type="button" data-muse-toggle-panel aria-label="Open goals and artifacts">Goals</button></div>';
    }

    function railHTML() {
      var items = chatBtn('main', 'Main chat', state.activeChatId === 'main');
      (state.chats.sides || []).forEach(function (c) {
        items += chatBtn(c.id, c.title || 'Side chat', state.activeChatId === c.id);
      });
      return '<aside class="il-muse-rail" aria-label="Chats">' +
        '<div class="il-muse-rail__label" data-i18n="muse.chats">Chats</div>' +
        '<div class="il-muse-chat-list">' + items + '</div>' +
        '<button type="button" class="il-muse-btn-new" data-muse-new-side data-i18n="muse.new_side">+ New side chat</button>' +
        '</aside>';
    }

    function chatBtn(id, title, on) {
      return '<button type="button" class="il-muse-chat-item' + (on ? ' is-active' : '') + '" data-muse-chat="' + esc(id) + '">' +
        '<span class="il-muse-chat-item__dot" aria-hidden="true"></span><span>' + esc(title) + '</span></button>';
    }

    function avatarMarkHTML() {
      var av = avatarById(state.avatarId || AVATAR_DEFAULT);
      return '<button type="button" class="il-muse-avatar il-muse-avatar--' + esc(av.id) + '" data-muse-avatar data-avatar="' + esc(av.id) + '"' +
        ' title="Noah · ' + esc(av.label) + '" aria-label="Noah activity">' +
        '<span class="il-muse-avatar__ring" aria-hidden="true"></span>' +
        '<img class="il-muse-avatar__mark" src="' + esc(av.src) + '" width="40" height="40" alt="" decoding="async"/>' +
        '</button>';
    }

    function stageHTML(chat, vs) {
      var bubbles = '';
      (chat.messages || []).forEach(function (m, idx) {
        if (m.role === 'system') {
          bubbles += '<div class="il-muse-bubble il-muse-bubble--system">' + esc(m.text) + '</div>';
          return;
        }
        if (m.role === 'approval' && m.approval) {
          bubbles += approvalCardHTML(m.approval, idx);
          return;
        }
        var who = m.role === 'user' ? 'user' : 'bot';
        var partCls = m.partOf ? ' il-muse-bubble--part' : '';
        var meta = m.role === 'user' ? 'You' : esc(state.name) + (m.source ? ' · ' + esc(m.source) : '') +
          (m.partOf ? ' · ' + (m.partIndex || 1) + '/' + (m.partOf || 1) : '');
        bubbles += '<div class="il-muse-bubble il-muse-bubble--' + who + partCls + '">' +
          '<span class="il-muse-bubble__meta">' + meta + '</span>' + esc(m.text);
        if (m.role === 'assistant' && (!m.partOf || m.partIndex === m.partOf)) {
          bubbles += '<div class="il-muse-bubble__thumbs">' +
            '<button type="button" class="il-muse-icon-btn" data-muse-thumb="up" data-idx="' + idx + '" title="Helpful" aria-label="Helpful">👍</button>' +
            '<button type="button" class="il-muse-icon-btn" data-muse-thumb="down" data-idx="' + idx + '" title="Not helpful" aria-label="Not helpful">👎</button></div>';
        }
        bubbles += '</div>';
        if (m.artifact) bubbles += artifactHTML(m.artifact);
      });
      if (statusKey === 'thinking') {
        bubbles += '<div class="il-muse-bubble il-muse-bubble--bot is-streaming" data-muse-thinking-bubble>' +
          '<span class="il-muse-bubble__meta">' + esc(state.name) + ' · thinking</span>' +
          '<span class="il-muse-typing" aria-hidden="true"><i></i><i></i><i></i></span></div>';
      }
      if (!bubbles) {
        bubbles = '<div class="il-muse-bubble il-muse-bubble--system">One long main chat · interrupt anytime · multi-send while thinking · side chats for topics. I stay Socratic — show your work.</div>';
      }

      var voiceFb = '';
      if (!vs.recognition && !vs.synthesis) {
        voiceFb = '<p class="il-muse-voice-fallback" data-i18n="muse.voice_unsupported">Voice unsupported in this browser. Text still works. Chrome/Edge recommended for Web Speech.</p>';
      } else if (!vs.recognition) {
        voiceFb = '<p class="il-muse-voice-fallback">Dictation unsupported; spoken replies may still work.</p>';
      } else if (!vs.synthesis) {
        voiceFb = '<p class="il-muse-voice-fallback">speechSynthesis unavailable; mic dictation still works.</p>';
      }

      return '<section class="il-muse-stage">' +
        '<header class="il-muse-header">' +
        avatarMarkHTML() +
        '<div class="il-muse-header__meta">' +
        '<p class="il-muse-header__name">' + esc(state.name) + '</p>' +
        '<p class="il-muse-header__activity" data-muse-activity>Idle</p></div>' +
        '<span class="il-muse-status-pill"><span class="il-muse-status-pill__dot" aria-hidden="true"></span>' +
        '<span data-muse-status>Idle</span></span>' +
        '<div class="il-muse-header__actions">' +
        '<button type="button" class="il-muse-icon-btn' + (state.speak ? ' is-on' : '') + '" data-muse-toggle-speak title="Speak replies" aria-pressed="' + !!state.speak + '">🔊</button>' +
        '<button type="button" class="il-muse-icon-btn" data-muse-open-settings title="Settings">⚙</button>' +
        '</div></header>' +
        '<div class="il-muse-3d-slot" data-muse-3d-slot aria-hidden="false"></div>' +
        '<div class="il-muse-live" data-muse-live data-live="idle" role="status" aria-live="polite">' +
        '<span class="il-muse-live__dot" aria-hidden="true"></span>' +
        '<span data-muse-live-text>Ready · ask a stuck question</span></div>' +
        nudgeStripHTML() +
        '<div class="il-muse-transcript" data-muse-transcript role="log" aria-live="polite">' + bubbles + '</div>' +
        '<div class="il-muse-composer">' +
        '<p class="il-muse-composer__interim" data-muse-interim hidden></p>' +
        '<form class="il-muse-composer__row" data-muse-form autocomplete="off">' +
        '<button type="button" class="il-muse-icon-btn" data-muse-attach title="Attach (stub)" aria-label="Attach">📎</button>' +
        '<button type="button" class="il-muse-icon-btn il-muse-mic" data-muse-mic title="Dictate" ' +
          (vs.recognition ? '' : 'disabled ') + 'aria-label="Microphone">🎙</button>' +
        '<textarea class="il-muse-composer__input" data-muse-input rows="1" placeholder="Ask a stuck question — interrupt anytime…" aria-label="Message Noah"></textarea>' +
        (statusKey === 'thinking' || statusKey === 'speaking'
          ? '<button type="button" class="il-muse-send il-muse-send--stop" data-muse-stop title="Stop / interrupt">Stop</button>'
          : '<button type="submit" class="il-muse-send" data-i18n="muse.send">Send</button>') +
        '</form>' + voiceFb +
        '<p class="il-muse-disclaimer"><strong>Honesty:</strong> Noah is the assistant. Not a filmed character, and not another company’s product. Avatar theme inspired by historical John Dee (Monas / hermetic scholar energy); Interstitium original artwork — not a museum portrait or a filmed assistant. Voice = browser Web Speech. Models: local rules by default; Ollama / lab-control optional. No fake API keys. Prefer lean tier; scale when demand grows.</p>' +
        '</div></section>';
    }

    function approvalCardHTML(ap, idx) {
      if (!ap || ap.dismissed) return '';
      var prim = ap.primary || {};
      var sec = ap.secondary || {};
      return '<div class="il-muse-approval" data-muse-approval="' + esc(ap.id || '') + '" data-idx="' + idx + '" role="group" aria-label="Approval">' +
        '<p class="il-muse-approval__kicker">Approve · local only</p>' +
        '<h4 class="il-muse-approval__title">' + esc(ap.title || 'Continue?') + '</h4>' +
        '<p class="il-muse-approval__body">' + esc(ap.body || '') + '</p>' +
        '<div class="il-muse-approval__actions">' +
        '<button type="button" class="il-muse-approval__primary" data-muse-approve="primary" data-idx="' + idx + '">' +
        esc(prim.label || 'Approve') + '</button>' +
        '<button type="button" class="il-muse-approval__secondary" data-muse-approve="secondary" data-idx="' + idx + '">' +
        esc(sec.label || 'Dismiss') + '</button></div>' +
        '<p class="il-muse-approval__note">No Meta / Gmail / Spotify connectors — Interstitium first-party paths only.</p></div>';
    }

    function nudgeStripHTML() {
      var nudges = localNudges(state);
      if (!nudges.length) return '';
      return '<div class="il-muse-nudges" role="list" aria-label="Local nudges">' +
        nudges.map(function (n) {
          return '<button type="button" class="il-muse-nudge" role="listitem" data-muse-nudge="' + esc(n.id) + '"' +
            (n.ask ? ' data-muse-nudge-ask="' + esc(n.ask) + '"' : '') +
            (n.href ? ' data-muse-nudge-href="' + esc(n.href) + '"' : '') +
            '>' + esc(n.text) + '</button>';
        }).join('') + '</div>';
    }

    function artifactHTML(a) {
      var links = (a.links || []).map(function (l) {
        var external = !isFirstPartyHref(l.href);
        return '<a href="' + esc(l.href) + '" class="il-muse-artifact__link' + (external ? ' is-external' : '') + '"' +
          (external ? ' data-muse-external="' + esc(l.href) + '"' : '') + '>' + esc(l.label) +
          (external ? ' ↗' : '') + '</a>';
      }).join('');
      var list = (a.checklist || []).map(function (c, i) {
        return '<li><label class="il-muse-artifact__check"><input type="checkbox" data-muse-art-check="' +
          esc(a.id || '') + ':' + i + '"/> <span>' + esc(c) + '</span></label></li>';
      }).join('');
      var kind = a.kind || 'card';
      return '<div class="il-muse-artifact il-muse-artifact--' + esc(kind) + '" data-artifact-id="' + esc(a.id || '') + '">' +
        '<div class="il-muse-artifact__kicker">Artifact · ' + esc(kind) + '</div>' +
        '<h4 class="il-muse-artifact__title">' + esc(a.title) + '</h4>' +
        '<div class="il-muse-artifact__body">' + esc(a.body || '') + '</div>' +
        (a.command ? '<pre class="il-muse-artifact__cmd"><code>' + esc(a.command) + '</code></pre>' : '') +
        (list ? '<ul class="il-muse-artifact__list">' + list + '</ul>' : '') +
        (links ? '<div class="il-muse-artifact__links">' + links + '</div>' : '') +
        '</div>';
    }

    function panelHTML(ideas, demand, routerState, active, catalog, vs) {
      var unread = (state.inbox || []).filter(function (n) { return !n.read; }).length;
      var tabs = [
        ['goals', 'Goals'], ['ideas', 'Ideas'],
        ['inbox', 'Inbox' + (unread ? ' · ' + unread : '')],
        ['library', 'Library'],
        ['model', 'Model'], ['settings', 'Noah']
      ];
      var tabBtns = tabs.map(function (t) {
        return '<button type="button" class="il-muse-tab' + (panelTab === t[0] ? ' is-on' : '') + '" data-muse-tab="' + t[0] + '">' + t[1] + '</button>';
      }).join('');
      var body = '';
      if (panelTab === 'goals') body = goalsPanel();
      else if (panelTab === 'ideas') body = ideasPanel(ideas);
      else if (panelTab === 'inbox') body = inboxPanel();
      else if (panelTab === 'library') body = libraryPanel();
      else if (panelTab === 'model') body = modelPanel(demand, routerState, active, catalog);
      else body = settingsPanel(vs);
      return '<aside class="il-muse-panel" aria-label="Noah panels">' +
        '<div class="il-muse-tabs">' + tabBtns + '</div>' +
        '<div class="il-muse-panel__body">' + body + '</div></aside>';
    }

    function goalsPanel() {
      var rows = (state.goals || []).map(function (g0) {
        return '<div class="il-muse-goal' + (g0.done ? ' is-done' : '') + '"><label class="il-muse-goal-row">' +
          '<input type="checkbox" data-muse-goal-toggle="' + esc(g0.id) + '"' + (g0.done ? ' checked' : '') + '/>' +
          '<span><p class="il-muse-goal__title">' + esc(g0.title) + '</p></span></label></div>';
      }).join('');
      return '<div class="il-muse-panel-section"><h3 data-i18n="muse.goals">Lab goals</h3>' +
        '<p class="hint">Persisted in localStorage. Chat about them anytime.</p>' + rows +
        '<div class="il-muse-add-row"><input data-muse-goal-input placeholder="Add a lab goal…" />' +
        '<button type="button" data-muse-goal-add>Add</button></div></div>' + activityBlock();
    }

    function ideasPanel(ideas) {
      var rows = ideas.map(function (idea) {
        return '<div class="il-muse-idea">' +
          '<p class="il-muse-idea__title">' + esc(idea.title) + '</p>' +
          '<p class="il-muse-idea__meta">' + esc(idea.meta || '') + '</p>' +
          '<div class="il-muse-artifact__links" style="margin-top:0.5rem">' +
          (idea.href ? '<a href="' + esc(idea.href) + '">Open</a>' : '') +
          '<button type="button" data-muse-idea-ask="' + esc(idea.title) + '" class="il-muse-chip-btn">Ask Noah</button></div></div>';
      }).join('');
      return '<div class="il-muse-panel-section"><h3 data-i18n="muse.ideas">Ideas</h3>' +
        '<p class="hint">Suggestions from Adaptive weak topics when present.</p>' + rows + '</div>';
    }

    function inboxPanel() {
      var rows = (state.inbox || []).map(function (n) {
        return '<div class="il-muse-idea' + (n.read ? '' : ' is-unread') + '">' +
          '<p class="il-muse-idea__title">' + esc(n.title) + '</p>' +
          '<p class="il-muse-idea__meta">' + esc(n.meta || '') + '</p>' +
          '<div class="il-muse-artifact__links" style="margin-top:0.5rem">' +
          (n.href ? '<a href="' + esc(n.href) + '"' + (isFirstPartyHref(n.href) ? '' : ' data-muse-external="' + esc(n.href) + '"') + '>Open</a>' : '') +
          '<button type="button" data-muse-nudge-ask="' + esc(n.title) + '" class="il-muse-chip-btn">Ask Noah</button>' +
          '<button type="button" data-muse-nudge-read="' + esc(n.id) + '" class="il-muse-chip-btn">Mark read</button></div></div>';
      }).join('');
      return '<div class="il-muse-panel-section"><h3>Study inbox</h3>' +
        '<p class="hint">Local proactive nudges from open goals + weak Adapt topics. No Meta push — optional Notification API on this device.</p>' +
        (rows || '<p class="hint">Inbox empty — add a lab goal or place Adaptive to seed nudges.</p>') +
        '<div class="il-muse-add-row" style="margin-top:0.75rem">' +
        '<button type="button" data-muse-nudge-now>Refresh nudges</button>' +
        '<button type="button" data-muse-notif-opt>' + (state.notifOptIn ? 'Disable device alerts' : 'Enable device alerts') + '</button></div></div>';
    }

    function libraryPanel() {
      var arts = state.artifacts || [];
      if (!arts.length) {
        return '<div class="il-muse-panel-section"><h3>Library / Artifacts</h3><p class="hint">Rich cards from chat land here.</p></div>';
      }
      return '<div class="il-muse-panel-section"><h3>Library / Artifacts</h3>' +
        arts.slice().reverse().map(function (a) {
          return '<div class="il-muse-lib-item"><strong>' + esc(a.title) + '</strong>' +
            '<p class="il-muse-idea__meta">' + esc(a.kind) + '</p></div>';
        }).join('') + '</div>';
    }

    function modelPanel(demand, routerState, active, catalog) {
      var tier = (demand && demand.tier) ? demand.tier : { id: 'T0', label: 'T0 Lean', blurb: 'Local rules default.' };
      var tiers = (demand && demand.tiers) ? demand.tiers : [
        { id: 'T0', label: 'T0 Lean' }, { id: 'T1', label: 'T1 Standard' }, { id: 'T2', label: 'T2 Heavy' }
      ];
      var tierBtns = tiers.map(function (t) {
        var on = tier.id === t.id;
        return '<button type="button" class="il-muse-chip-btn' + (on ? ' is-on' : '') + '" data-muse-tier="' + esc(t.id) + '">' + esc(t.label || t.id) + '</button>';
      }).join(' ');

      var backendOpts = catalog.map(function (b) {
        return '<option value="' + esc(b.id) + '"' + (active.backendId === b.id ? ' selected' : '') + '>' + esc(b.label || b.id) + '</option>';
      }).join('');

      var models = [];
      catalog.forEach(function (b) {
        if (b.id === active.backendId) models = b.models || [];
      });
      if (!models.length) models = [{ id: 'local-rules', label: 'Hint engine' }];
      // Prefer lean models first in the list
      models = models.slice().sort(function (a, b) {
        return (a.size_b || 0) - (b.size_b || 0);
      });
      var modelOpts = models.map(function (m) {
        return '<option value="' + esc(m.id) + '"' + (active.modelId === m.id ? ' selected' : '') + '>' + esc(m.label || m.id) + '</option>';
      }).join('');

      var ep = '';
      if (router() && router().baseUrlFor) {
        ep = router().baseUrlFor(active.backendId) || '';
      }
      var creds = (router() && router().getCreds) ? router().getCreds() : {};
      if (!ep && creds[active.backendId]) ep = creds[active.backendId].baseUrl || '';

      var suggest = (demand && demand.suggestedTier)
        ? '<p class="hint" style="color:#c9a227">' + esc(demand.suggestReason || ('Consider ' + demand.suggestedTier)) + '</p>'
        : '';

      var rank = ((demand && demand.ranking) || []).map(function (r) {
        return '<li style="font-size:0.72rem;color:#8b9bb4;margin:0.25rem 0">' +
          esc((r.backendId || '') + '/' + (r.modelId || '')) +
          ' · score ' + (r.score != null ? r.score : '?') +
          (r.avgLatencyMs != null ? ' · ' + r.avgLatencyMs + 'ms' : '') +
          (r.n != null ? ' · n=' + r.n : '') + '</li>';
      }).join('');

      var mode = (routerState && routerState.mode) || 'auto';
      var autoOn = mode === 'auto';

      return '<div class="il-muse-panel-section">' +
        '<h3 data-i18n="muse.model">Model · demand</h3>' +
        '<p class="hint"><strong>Current tier: ' + esc(tier.label || tier.id) + '</strong> — ' +
        esc(tier.blurb || '') + '</p>' +
        '<p class="il-muse-scale-note"><strong>Scale when demand grows.</strong> Prefer lean defaults ' +
        '(local rules / ≤3B on P1000 4GB). Move T0 → T1 → T2 only when concurrent seats, latency, or errors climb. Never pretend a 70B fits this GPU.</p>' +
        '<div class="il-muse-tier-row">' + tierBtns + '</div>' + suggest +
        '<div class="il-muse-field"><label>Backend</label><select data-muse-backend>' + backendOpts + '</select></div>' +
        '<div class="il-muse-field"><label>Primary model</label><select data-muse-model>' + modelOpts + '</select></div>' +
        '<div class="il-muse-field"><label>Endpoint (optional)</label>' +
        '<input data-muse-endpoint type="url" placeholder="http://127.0.0.1:11434 or https://lab-control/v1" value="' + esc(ep) + '"/></div>' +
        '<div class="il-muse-add-row">' +
        '<button type="button" data-muse-apply-model>Apply</button>' +
        '<button type="button" data-muse-clear-override>Reset lean</button>' +
        '<button type="button" data-muse-probe>Health check</button></div>' +
        '<p class="hint" style="margin-top:0.75rem">Active: <code class="il-muse-code">' + esc(active.backendId) +
        '</code> / <code class="il-muse-code">' + esc(active.modelId) + '</code>' +
        (autoOn ? ' · auto mode' : ' · manual mode') + '</p>' +
        '<label class="il-muse-check"><input type="checkbox" data-muse-auto-switch' + (autoOn ? ' checked' : '') +
        '/> Auto-select among healthy models (analytics can promote challengers)</label>' +
        '<p class="hint">Rolling score from latency · errors · thumbs. Set endpoint via UI or <code class="il-muse-code">window.IL_MUSE.endpoint</code> — never commit API keys.</p>' +
        (rank ? '<ul style="margin:0.5rem 0;padding-left:1rem">' + rank + '</ul>' : '') +
        '</div>';
    }

    function noahProfile() {
      try {
        if (g.ILNoahAvatar && g.ILNoahAvatar.getProfile) return g.ILNoahAvatar.getProfile();
      } catch (e) {}
      return { avatar: 'monas', name: 'Noah', accent: 'cyan', intensity: 'balanced' };
    }

    /* 3D avatar gallery + accent + motion personalization (il-noah-profile). */
    function noahAvatarPanel() {
      var P = noahProfile();
      var list = (g.ILNoahAvatar && g.ILNoahAvatar.AVATARS) || [
        { id: 'monas', label: 'Monas', hint: 'Crystalline Monas · orrery rings' },
        { id: 'orrery', label: 'Orrery', hint: 'Ringed worlds · orbital mechanics' },
        { id: 'sigil', label: 'Sigil Core', hint: 'Radiant sigil · counter-rotating glyph rings' },
        { id: 'wisp', label: 'Wisp', hint: 'Nebula ghost · drifting star-wisp' }
      ];
      var accents = (g.ILNoahAvatar && g.ILNoahAvatar.ACCENTS) || {
        cyan: { label: 'Cyan', css: '#5EEAD4' }, gold: { label: 'Gold', css: '#c9a227' },
        violet: { label: 'Violet', css: '#A78BFA' }, emerald: { label: 'Emerald', css: '#34D399' }
      };
      var inten = (g.ILNoahAvatar && g.ILNoahAvatar.INTENSITY) || {
        calm: { label: 'Calm' }, balanced: { label: 'Balanced' }, vivid: { label: 'Vivid' }
      };
      var cards = list.map(function (a) {
        var on = P.avatar === a.id;
        return '<button type="button" class="il-noah-3d-card' + (on ? ' is-on' : '') + '" data-noah-3d-pick="' + esc(a.id) + '"' +
          ' data-noah-3d="' + esc(a.id) + '" role="radio" aria-checked="' + (on ? 'true' : 'false') + '"' +
          ' title="' + esc(a.hint || a.label) + '">' +
          '<span class="il-noah-3d-card__art" aria-hidden="true"></span>' +
          '<span class="il-noah-3d-card__name">' + esc(a.label) + '</span>' +
          '<span class="il-noah-3d-card__hint">' + esc(a.hint || '') + '</span></button>';
      }).join('');
      var sw = Object.keys(accents).map(function (key) {
        var ac = accents[key];
        var on = P.accent === key;
        return '<button type="button" class="il-noah-accent' + (on ? ' is-on' : '') + '" data-noah-accent-pick="' + esc(key) + '"' +
          ' role="radio" aria-checked="' + (on ? 'true' : 'false') + '" title="' + esc(ac.label) + '" aria-label="Accent ' + esc(ac.label) + '"' +
          ' style="background:' + esc(ac.css) + ';color:' + esc(ac.css) + '"></button>';
      }).join('');
      var seg = Object.keys(inten).map(function (key) {
        var on = P.intensity === key;
        return '<button type="button" class="' + (on ? 'is-on' : '') + '" data-noah-intensity-pick="' + esc(key) + '"' +
          ' role="radio" aria-checked="' + (on ? 'true' : 'false') + '">' + esc(inten[key].label) + '</button>';
      }).join('');
      return '<div class="il-muse-field"><label>3D avatar</label>' +
        '<div class="il-noah-3d-gallery" role="radiogroup" aria-label="3D avatar">' + cards + '</div>' +
        '<p class="hint">Live 3D stage · renders on-device in your browser, no cloud. Switches instantly and reacts to Idle / Listening / Thinking / Speaking.</p></div>' +
        '<div class="il-muse-field"><label>Accent</label>' +
        '<div class="il-noah-accents" role="radiogroup" aria-label="Accent color">' + sw + '</div></div>' +
        '<div class="il-muse-field"><label>Motion</label>' +
        '<div class="il-noah-intensity" role="radiogroup" aria-label="Animation intensity">' + seg + '</div>' +
        '<p class="hint">Your OS reduced-motion setting always wins — then the avatar renders a single still frame.</p></div>';
    }

    function settingsPanel(vs) {
      var voices = listVoices();
      var vopts = '<option value="">Browser default</option>' + voices.map(function (v) {
        return '<option value="' + esc(v.voiceURI) + '"' + (state.voiceURI === v.voiceURI ? ' selected' : '') + '>' + esc(v.name) + '</option>';
      }).join('');
      var mems = (state.memories || []).map(function (m, i) {
        return '<li><span>' + esc(m) + '</span><button type="button" data-muse-mem-del="' + i + '">Remove</button></li>';
      }).join('');
      return '<div class="il-muse-panel-section"><h3 data-i18n="muse.settings">Noah settings</h3>' +
        '<div class="il-muse-field"><label>Name</label><input data-muse-name value="' + esc(state.name) + '"/></div>' +
        '<div class="il-muse-field"><label>Avatar</label><div class="il-muse-avatar-picker" role="radiogroup" aria-label="Avatar theme">' +
        AVATARS.map(function (a) {
          var on = (state.avatarId || AVATAR_DEFAULT) === a.id;
          return '<button type="button" class="il-muse-avatar-pick' + (on ? ' is-on' : '') + '" data-muse-avatar-pick="' + esc(a.id) + '"' +
            ' role="radio" aria-checked="' + (on ? 'true' : 'false') + '" title="' + esc(a.hint) + '">' +
            '<img src="' + esc(a.src) + '" width="40" height="40" alt="" decoding="async"/>' +
            '<span>' + esc(a.label) + '</span></button>';
        }).join('') + '</div>' +
        '<p class="hint">Default: Dee (Monas-derived). Alts: Interstitium sigil / scholar cap. Original artwork.</p></div>' +
        noahAvatarPanel() +
        '<div class="il-muse-field"><label>Personality</label><input data-muse-personality value="' + esc(state.personality) + '"/></div>' +
        '<div class="il-muse-field"><label>Tone</label><select data-muse-tone">' +
        ['coach', 'terse', 'warm', 'exam-strict'].map(function (t) {
          return '<option value="' + t + '"' + (state.tone === t ? ' selected' : '') + '>' + t + '</option>';
        }).join('') + '</select></div>' +
        '<div class="il-muse-field"><label>Voice' + (vs.synthesis ? '' : ' (unavailable)') + '</label>' +
        '<select data-muse-voice ' + (vs.synthesis ? '' : 'disabled') + '>' + vopts + '</select></div>' +
        '<div class="il-muse-field"><label>Add memory</label>' +
        '<input data-muse-mem-input placeholder="e.g. Prefers kubectl over dashboards"/></div>' +
        '<div class="il-muse-add-row"><button type="button" data-muse-mem-add>Save memory</button></div>' +
        '<ul class="il-muse-mem-list">' + mems + '</ul>' +
        '<div class="il-muse-add-row" style="margin-top:1rem">' +
        '<button type="button" data-muse-save-settings>Save settings</button></div></div>' + activityBlock();
    }

    function activityBlock() {
      var items = (state.activity || []).slice(0, 8).map(function (a) {
        return '<li><time>' + new Date(a.t).toLocaleTimeString() + '</time>' + esc(a.text) + '</li>';
      }).join('');
      return '<div class="il-muse-panel-section" style="margin-top:1rem"><h3>Activity</h3>' +
        '<ul class="il-muse-activity">' + (items || '<li>No activity yet</li>') + '</ul></div>';
    }

    function wire(vs) {
      app.querySelectorAll('[data-muse-chat]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          state.activeChatId = btn.getAttribute('data-muse-chat');
          persist(); render();
        });
      });
      var neu = app.querySelector('[data-muse-new-side]');
      if (neu) neu.addEventListener('click', function () {
        var id = uid('side');
        state.chats.sides.push({ id: id, title: 'Side chat', messages: [] });
        state.activeChatId = id;
        pushActivity(state, 'Opened side chat');
        persist(); render();
      });

      app.querySelectorAll('[data-muse-tab]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          panelTab = btn.getAttribute('data-muse-tab');
          render();
        });
      });

      var tr = app.querySelector('[data-muse-toggle-rail]');
      if (tr) tr.addEventListener('click', function () {
        app.classList.toggle('is-rail-open');
        app.classList.remove('is-panel-open');
      });
      var tp = app.querySelector('[data-muse-toggle-panel]');
      if (tp) tp.addEventListener('click', function () {
        app.classList.toggle('is-panel-open');
        app.classList.remove('is-rail-open');
      });
      var scrim = app.querySelector('[data-muse-scrim]');
      if (scrim) scrim.addEventListener('click', function () {
        app.classList.remove('is-rail-open');
        app.classList.remove('is-panel-open');
      });
      wireSwipe();


      app.querySelectorAll('[data-muse-nudge]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var ask = btn.getAttribute('data-muse-nudge-ask');
          var href = btn.getAttribute('data-muse-nudge-href');
          pushActivity(state, 'Nudge · ' + (btn.textContent || '').trim());
          persist();
          if (ask) sendMessage(ask);
          else if (href) g.location.href = href;
        });
      });
      app.querySelectorAll('[data-muse-approve]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var which = btn.getAttribute('data-muse-approve');
          /* Modal overlay (yes/no) */
          if (which === 'yes' || which === 'no') {
            dismissApproval(which === 'yes');
            return;
          }
          var idx = parseInt(btn.getAttribute('data-idx'), 10);
          var chat = getChat(state, state.activeChatId);
          var msg = chat.messages[idx];
          if (!msg || !msg.approval) return;
          var ap = msg.approval;
          var act = which === 'primary' ? (ap.primary || {}) : (ap.secondary || {});
          msg.approval.dismissed = true;
          pushActivity(state, 'Approval · ' + (act.label || which));
          persist();
          if (act.href) {
            openHrefApproved(act.href);
            return;
          }
          if (act.panel) {
            panelTab = act.panel;
            app.classList.add('is-panel-open');
            render();
            return;
          }
          render();
        });
      });

      function openHrefApproved(href) {
        if (!href) return;
        if (isFirstPartyHref(href)) {
          g.location.href = href;
          return;
        }
        showApproval({
          title: 'Open external link?',
          body: 'Leave Interstitium and open: ' + href,
          confirmLabel: 'Open',
          cancelLabel: 'Stay',
          onConfirm: function () { g.location.href = href; }
        });
      }

      app.querySelectorAll('[data-muse-external]').forEach(function (a) {
        a.addEventListener('click', function (ev) {
          ev.preventDefault();
          openHrefApproved(a.getAttribute('data-muse-external') || a.getAttribute('href'));
        });
      });

      var stopBtn = app.querySelector('[data-muse-stop]');
      if (stopBtn) stopBtn.addEventListener('click', function () {
        interruptInflight('Interrupted by user');
        setStatus('idle');
        render();
      });

      var nudgeNow = app.querySelector('[data-muse-nudge-now]');
      if (nudgeNow) nudgeNow.addEventListener('click', function () {
        harvestNudges(true);
        render();
      });
      var notifOpt = app.querySelector('[data-muse-notif-opt]');
      if (notifOpt) notifOpt.addEventListener('click', function () {
        if (state.notifOptIn) {
          state.notifOptIn = false;
          pushActivity(state, 'Device alerts off');
          persist(); render();
          return;
        }
        if (!g.Notification) {
          pushActivity(state, 'Notification API unavailable — inbox still works');
          persist(); render();
          return;
        }
        Notification.requestPermission().then(function (p) {
          state.notifOptIn = (p === 'granted');
          pushActivity(state, state.notifOptIn ? 'Device alerts on' : 'Notification permission denied');
          if (state.notifOptIn) harvestNudges(true);
          persist(); render();
        }, function () {
          pushActivity(state, 'Notification permission error');
          persist(); render();
        });
      });
      app.querySelectorAll('[data-muse-nudge-read]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var id = btn.getAttribute('data-muse-nudge-read');
          (state.inbox || []).forEach(function (n) { if (n.id === id) n.read = true; });
          persist(); render();
        });
      });

      var speakBtn = app.querySelector('[data-muse-toggle-speak]');
      if (speakBtn) speakBtn.addEventListener('click', function () {
        state.speak = !state.speak;
        if (!state.speak && g.speechSynthesis) try { g.speechSynthesis.cancel(); } catch (e) {}
        persist(); render();
      });

      var openSet = app.querySelector('[data-muse-open-settings]');
      if (openSet) openSet.addEventListener('click', function () {
        panelTab = 'settings'; render(); app.classList.add('is-panel-open');
      });
      var avatar = app.querySelector('[data-muse-avatar]');
      if (avatar) avatar.addEventListener('click', function () {
        panelTab = 'goals'; render(); app.classList.add('is-panel-open');
      });

      app.querySelectorAll('[data-muse-goal-toggle]').forEach(function (cb) {
        cb.addEventListener('change', function () {
          var id = cb.getAttribute('data-muse-goal-toggle');
          state.goals.forEach(function (g0) { if (g0.id === id) g0.done = cb.checked; });
          pushActivity(state, 'Goal ' + (cb.checked ? 'done' : 'reopened'));
          persist(); render();
        });
      });
      var ga = app.querySelector('[data-muse-goal-add]');
      if (ga) ga.addEventListener('click', function () {
        var inp = app.querySelector('[data-muse-goal-input]');
        var t = inp && inp.value.trim();
        if (!t) return;
        state.goals.push({ id: uid('g'), title: t, done: false });
        persist(); render();
      });

      app.querySelectorAll('[data-muse-idea-ask]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          sendMessage(btn.getAttribute('data-muse-idea-ask'));
        });
      });

      app.querySelectorAll('[data-muse-thumb]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var chat = getChat(state, state.activeChatId);
          var idx = parseInt(btn.getAttribute('data-idx'), 10);
          var msg = chat.messages[idx];
          if (!msg || !analytics()) return;
          var v = btn.getAttribute('data-muse-thumb') === 'up' ? 1 : -1;
          if (typeof analytics().thumb === 'function') {
            analytics().thumb({ modelId: msg.modelId || 'local-rules', backendId: msg.backendId || 'local-rules', value: v });
          } else if (typeof analytics().setThumb === 'function') {
            analytics().setThumb(msg.backendId || 'local-rules', msg.modelId || 'rules', v);
          }
          pushActivity(state, 'Feedback ' + (v > 0 ? 'up' : 'down'));
          persist();
        });
      });

      app.querySelectorAll('[data-muse-tier]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var tid = btn.getAttribute('data-muse-tier');
          if (router() && router().setPolicy) {
            router().setPolicy({ demand_tier: tid });
          }
          pushActivity(state, 'Demand tier → ' + tid + ' (scale only with demand)');
          persist(); render();
        });
      });

      var be = app.querySelector('[data-muse-backend]');
      if (be) be.addEventListener('change', function () {
        var cat = modelCatalog();
        var b = null;
        for (var i = 0; i < cat.length; i++) if (cat[i].id === be.value) b = cat[i];
        var ms = app.querySelector('[data-muse-model]');
        if (ms && b) {
          ms.innerHTML = (b.models || []).map(function (m) {
            return '<option value="' + esc(m.id) + '">' + esc(m.label || m.id) + '</option>';
          }).join('');
        }
        var epEl = app.querySelector('[data-muse-endpoint]');
        if (epEl && router() && router().baseUrlFor) {
          epEl.value = router().baseUrlFor(be.value) || '';
        }
      });

      var apply = app.querySelector('[data-muse-apply-model]');
      if (apply) apply.addEventListener('click', function () {
        if (!router() || !router().setPolicy) return;
        var bid = (app.querySelector('[data-muse-backend]') || {}).value;
        var mid = (app.querySelector('[data-muse-model]') || {}).value;
        var epEl = app.querySelector('[data-muse-endpoint]');
        var epVal = epEl && epEl.value ? epEl.value.trim() : '';
        showApproval({
          title: 'Switch model backend?',
          body: 'Apply ' + bid + ' / ' + mid + (epVal ? ' · endpoint ' + epVal : '') +
            '. Lean T0 local-rules stays safest. No cloud keys are inventable here.',
          confirmLabel: 'Apply model',
          cancelLabel: 'Cancel',
          onConfirm: function () {
            if (epVal && router().setCreds) router().setCreds(bid, epVal, '');
            router().setPolicy({ backend: bid, primary: mid, mode: 'manual' });
            pushActivity(state, 'Model set ' + bid + '/' + mid);
            persist(); render();
          }
        });
      });
      var clr = app.querySelector('[data-muse-clear-override]');
      if (clr) clr.addEventListener('click', function () {
        if (router() && router().setPolicy) {
          router().setPolicy({ mode: 'auto', demand_tier: 'T0', primary: 'qwen2.5-coder-3b', backend: 'ollama' });
        }
        pushActivity(state, 'Reset to lean T0 auto');
        persist(); render();
      });
      var probe = app.querySelector('[data-muse-probe]');
      if (probe) probe.addEventListener('click', function () {
        if (!router() || !router().healthCheck) return;
        setStatus('thinking');
        router().healthCheck({ force: true }).then(function (r) {
          var n = r && r.results ? r.results.filter(function (x) { return x.ok; }).length : 0;
          pushActivity(state, 'Health: ' + n + ' healthy endpoint(s)');
          persist(); setStatus('idle'); render();
        }, function () {
          pushActivity(state, 'Health check failed');
          setStatus('idle'); render();
        });
      });
      var auto = app.querySelector('[data-muse-auto-switch]');
      if (auto) auto.addEventListener('change', function () {
        if (!router() || !router().setPolicy) return;
        router().setPolicy({ mode: auto.checked ? 'auto' : 'manual' });
      });

      var saveSet = app.querySelector('[data-muse-save-settings]');
      if (saveSet) saveSet.addEventListener('click', function () {
        var n = app.querySelector('[data-muse-name]');
        var p = app.querySelector('[data-muse-personality]');
        var ton = app.querySelector('[data-muse-tone]');
        var vo = app.querySelector('[data-muse-voice]');
        if (n) state.name = n.value.trim() || 'Noah';
        /* keep the Noah 3D profile name in sync (il-noah-profile) */
        try {
          if (g.ILNoahAvatar && g.ILNoahAvatar.setProfilePatch) {
            g.ILNoahAvatar.setProfilePatch({ name: state.name });
          } else if (g.ILNoahAvatar && g.ILNoahAvatar.getProfile) {
            var __pp = g.ILNoahAvatar.getProfile(); __pp.name = state.name;
            g.ILNoahAvatar.saveProfile(__pp);
          }
          if (app.__ilNoahAvatar && app.__ilNoahAvatar.setName) app.__ilNoahAvatar.setName(state.name);
        } catch (eName) {}
        if (p) state.personality = p.value.trim() || state.personality;
        if (ton) state.tone = ton.value;
        if (vo) state.voiceURI = vo.value;
        pushActivity(state, 'Updated Noah settings');
        persist(); render();
      });
      app.querySelectorAll('[data-muse-avatar-pick]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var id = btn.getAttribute('data-muse-avatar-pick');
          if (!avatarById(id)) return;
          state.avatarId = id;
          pushActivity(state, 'Avatar · ' + avatarById(id).label);
          persist(); render();
        });
      });
      /* Noah 3D avatar system: gallery / accent / motion — live, persisted to il-noah-profile */
      function noahPatch(patch, activityText) {
        if (!g.ILNoahAvatar || !g.ILNoahAvatar.setProfilePatch) return;
        g.ILNoahAvatar.setProfilePatch(patch);
        if (activityText) pushActivity(state, activityText);
        render();
      }
      app.querySelectorAll('[data-noah-3d-pick]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var id = btn.getAttribute('data-noah-3d-pick');
          var known = g.ILNoahAvatar && g.ILNoahAvatar.AVATARS &&
            g.ILNoahAvatar.AVATARS.some(function (a) { return a.id === id; });
          if (!known) return;
          noahPatch({ avatar: id }, '3D avatar · ' + id);
        });
      });
      app.querySelectorAll('[data-noah-accent-pick]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var key = btn.getAttribute('data-noah-accent-pick');
          var known = g.ILNoahAvatar && g.ILNoahAvatar.ACCENTS && g.ILNoahAvatar.ACCENTS[key];
          if (!known) return;
          noahPatch({ accent: key }, 'Accent · ' + known.label);
        });
      });
      app.querySelectorAll('[data-noah-intensity-pick]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var key = btn.getAttribute('data-noah-intensity-pick');
          var known = g.ILNoahAvatar && g.ILNoahAvatar.INTENSITY && g.ILNoahAvatar.INTENSITY[key];
          if (!known) return;
          noahPatch({ intensity: key }, 'Motion · ' + known.label);
        });
      });
      var memAdd = app.querySelector('[data-muse-mem-add]');
      if (memAdd) memAdd.addEventListener('click', function () {
        var inp = app.querySelector('[data-muse-mem-input]');
        var t = inp && inp.value.trim();
        if (!t) return;
        state.memories = state.memories || [];
        state.memories.push(t);
        persist(); render();
      });
      app.querySelectorAll('[data-muse-mem-del]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var i = parseInt(btn.getAttribute('data-muse-mem-del'), 10);
          state.memories.splice(i, 1);
          persist(); render();
        });
      });

      var form = app.querySelector('[data-muse-form]');
      var input = app.querySelector('[data-muse-input]');
      if (form && input) {
        form.addEventListener('submit', function (ev) {
          ev.preventDefault();
          var q = input.value.trim();
          if (!q) return;
          input.value = '';
          sendMessage(q);
        });
        input.addEventListener('keydown', function (ev) {
          if (ev.key === 'Enter' && !ev.shiftKey) {
            ev.preventDefault();
            if (form.requestSubmit) form.requestSubmit();
            else form.dispatchEvent(new Event('submit', { cancelable: true }));
          }
        });
      }

      var attach = app.querySelector('[data-muse-attach]');
      if (attach) attach.addEventListener('click', function () {
        var chat = getChat(state, state.activeChatId);
        chat.messages.push({
          role: 'system',
          text: 'Attach is a stub. Paste redacted logs or hypotheses in the composer instead.'
        });
        pushActivity(state, 'Attach stub');
        persist(); render();
      });

      var mic = app.querySelector('[data-muse-mic]');
      if (mic && vs.recognition) {
        mic.addEventListener('click', function () { toggleMic(mic, vs); });
      }
    }

    function wireSwipe() {
      var stage = app.querySelector('.il-muse-stage');
      if (!stage || stage.getAttribute('data-muse-swipe')) return;
      stage.setAttribute('data-muse-swipe', '1');
      var sx = 0, sy = 0, tracking = false;
      stage.addEventListener('touchstart', function (ev) {
        if (!ev.touches || !ev.touches[0]) return;
        sx = ev.touches[0].clientX;
        sy = ev.touches[0].clientY;
        tracking = true;
      }, { passive: true });
      stage.addEventListener('touchend', function (ev) {
        if (!tracking) return;
        tracking = false;
        var t = ev.changedTouches && ev.changedTouches[0];
        if (!t) return;
        var dx = t.clientX - sx;
        var dy = t.clientY - sy;
        if (Math.abs(dx) < 64 || Math.abs(dx) < Math.abs(dy) * 1.4) return;
        if (dx > 0) {
          app.classList.add('is-rail-open');
          app.classList.remove('is-panel-open');
        } else {
          app.classList.add('is-panel-open');
          app.classList.remove('is-rail-open');
        }
      }, { passive: true });
    }

    function toggleMic(micBtn, vs) {
      if (!vs.Rec) return;
      if (listening && recognition) {
        try { recognition.stop(); } catch (e) {}
        listening = false;
        micBtn.classList.remove('is-listening');
        setStatus('idle');
        return;
      }
      recognition = new vs.Rec();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = (document.documentElement.lang || 'en').indexOf('es') === 0 ? 'es-ES' : 'en-US';
      var interim = app.querySelector('[data-muse-interim]');
      var finalText = '';
      recognition.onstart = function () {
        listening = true;
        micBtn.classList.add('is-listening');
        setStatus('listening');
        pushActivity(state, 'Listening…');
        if (interim) { interim.hidden = false; interim.textContent = 'Listening…'; }
      };
      recognition.onresult = function (ev) {
        var interimTxt = '';
        finalText = '';
        for (var i = 0; i < ev.results.length; i++) {
          var r = ev.results[i];
          if (r.isFinal) finalText += r[0].transcript;
          else interimTxt += r[0].transcript;
        }
        if (interim) interim.textContent = finalText || interimTxt;
        var input = app.querySelector('[data-muse-input]');
        if (input && finalText) input.value = (input.value ? input.value + ' ' : '') + finalText.trim();
      };
      recognition.onerror = function () {
        listening = false;
        micBtn.classList.remove('is-listening');
        setStatus('idle');
        if (interim) interim.textContent = 'Mic error — try again or type.';
      };
      recognition.onend = function () {
        listening = false;
        micBtn.classList.remove('is-listening');
        if (statusKey === 'listening') setStatus('idle');
        if (interim) setTimeout(function () { if (interim) interim.hidden = true; }, 1000);
      };
      try { recognition.start(); } catch (e) {
        listening = false;
        setStatus('idle');
      }
    }

    function sendMessage(text) {
      var chat = getChat(state, state.activeChatId);
      var topic = detectTopic(text);
      if (state.activeChatId !== 'main' && topic) chat.title = 'Side · ' + topic;
      /* Interruptible multi-send: cancel prior in-flight reply */
      if (statusKey === 'thinking' || statusKey === 'speaking') {
        interruptInflight('Interrupted · new message');
      }
      var myGen = ++inflightGen;
      chat.messages.push({ role: 'user', text: text, t: Date.now() });
      pushActivity(state, 'User message');
      persist();
      setStatus('thinking');
      render();

      askModel(chat, topic, state).then(function (raw) {
        if (myGen !== inflightGen) return; /* interrupted */
        var res = normRes(raw);
        var art = maybeArtifact(text, res.text, topic);
        var parts = splitBubbles(res.text, 4);
        if (!parts.length) parts = [res.text || ''];

        function pushPart(i) {
          if (myGen !== inflightGen) return;
          if (i >= parts.length) {
            var appr = maybeApproval(text, res.text, topic);
            if (appr) chat.messages.push({ role: 'approval', approval: appr, t: Date.now() });
            lastThumbMeta = { backendId: res.backendId, modelId: res.modelId };
            pushActivity(state, 'Replied via ' + res.backendId + (res.latencyMs ? ' · ' + res.latencyMs + 'ms' : '') +
              (parts.length > 1 ? ' · ' + parts.length + ' bubbles' : ''));
            persist();
            setStatus(state.speak ? 'speaking' : 'idle');
            render();
            try {
              if (analytics() && analytics().logCompletion) {
                analytics().logCompletion({
                  modelId: res.modelId,
                  backendId: res.backendId,
                  latencyMs: res.latencyMs,
                  ok: true,
                  taskType: 'coach_chat',
                  demand_tier: (router() && router().getPolicy) ? router().getPolicy().demand_tier : 'T0'
                });
              }
              if (g.ILGame && g.ILGame.award) g.ILGame.award('muse_ask', 5, { id: 'muse:' + Date.now() });
            } catch (e) {}
            speakText(res.text, state, function () {
              if (myGen === inflightGen) setStatus('idle');
            });
            return;
          }
          var msg = {
            role: 'assistant',
            text: parts[i],
            t: Date.now(),
            source: res.source,
            backendId: res.backendId,
            modelId: res.modelId,
            partIndex: i + 1,
            partOf: parts.length,
            partial: i < parts.length - 1
          };
          if (art && i === parts.length - 1) {
            msg.artifact = art;
            msg.partial = false;
            state.artifacts = state.artifacts || [];
            state.artifacts.push(art);
          }
          chat.messages.push(msg);
          persist();
          render();
          var delay = parts.length > 1 ? 280 : 0;
          var tid = setTimeout(function () { pushPart(i + 1); }, delay);
          streamTimers.push(tid);
        }
        pushPart(0);
      }, function (err) {
        if (myGen !== inflightGen) return;
        chat.messages.push({
          role: 'assistant',
          text: 'Error: ' + (err && err.message ? err.message : String(err)),
          source: 'error'
        });
        pushActivity(state, 'Reply failed');
        persist();
        setStatus('idle');
        render();
      });
    }

    // Welcome once — multi-bubble Muse cadence + local boot approval
    if (!state.chats.main.messages.length) {
      var bootParts = [
        'I\'m ' + state.name + ' — Interstitium\'s lab-aware coach (Dee theme).',
        'One long main chat, side chats for topics, artifacts for drills. Interrupt anytime.',
        'Lean local rules by default; Ollama / lab-control when demand grows. No Meta connectors.',
        'What are you stuck on?'
      ];
      bootParts.forEach(function (p, i) {
        state.chats.main.messages.push({
          role: 'assistant',
          text: p,
          source: 'local-rules',
          backendId: 'local-rules',
          modelId: 'rules',
          partIndex: i + 1,
          partOf: bootParts.length,
          t: Date.now() + i
        });
      });
      state.chats.main.messages.push({
        role: 'approval',
        t: Date.now(),
        approval: {
          id: uid('boot'),
          title: 'Start with Adaptive placement?',
          body: 'Proactive local nudge — place the field to build weak-topic signals. First-party only.',
          primary: { label: 'Open Adaptive', href: '/adapt/' },
          secondary: { label: 'Ask a stuck question', dismiss: true }
        }
      });
      pushActivity(state, 'Boot · lean tier · Dee · multi-bubble');
      persist();
    }

    el.innerHTML = '';
    el.appendChild(app);
    el.setAttribute('data-il-muse-ready', '1');
    el.__ilMuseSend = sendMessage;
    consumePendingPrompt(sendMessage);

    if (g.speechSynthesis) {
      try { g.speechSynthesis.addEventListener('voiceschanged', function () {}); } catch (e) {}
    }
    try { harvestNudges(false); } catch (eN) {}
    render();
  }


  function promptFrom(text, opts) {
    opts = opts || {};
    text = String(text || '').trim();
    if (!text) return;
    // Prefer live mount input if present
    var root = document.querySelector('[data-il-muse][data-il-muse-ready="1"]') || document.querySelector('[data-il-muse]');
    if (root && root.__ilMuseSend) {
      root.__ilMuseSend(text);
      return true;
    }
    // Persist pending prompt for /coach mount
    try {
      g.sessionStorage.setItem('il.muse.pending.prompt', text);
    } catch (e) {}
    if (opts.navigate !== false && !document.querySelector('[data-il-muse]')) {
      g.location.href = '/coach/?prompt=' + encodeURIComponent(text);
      return true;
    }
    return false;
  }

  function consumePendingPrompt(sendFn) {
    var q = '';
    try {
      var u = new URL(g.location.href);
      q = u.searchParams.get('prompt') || '';
    } catch (e) {}
    if (!q) {
      try { q = g.sessionStorage.getItem('il.muse.pending.prompt') || ''; } catch (e2) {}
    }
    if (!q) return;
    try { g.sessionStorage.removeItem('il.muse.pending.prompt'); } catch (e3) {}
    try {
      var u2 = new URL(g.location.href);
      if (u2.searchParams.has('prompt')) {
        u2.searchParams.delete('prompt');
        g.history.replaceState({}, '', u2.pathname + u2.search + u2.hash);
      }
    } catch (e4) {}
    if (typeof sendFn === 'function') {
      setTimeout(function () { sendFn(q); }, 60);
    }
  }

  function bindMusePromptButtons() {
    document.addEventListener('click', function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      var btn = t.closest('[data-il-muse-prompt]');
      if (!btn) return;
      ev.preventDefault();
      var text = btn.getAttribute('data-il-muse-prompt') || btn.textContent || '';
      promptFrom(text, { navigate: true });
    });
  }

  function boot() {
    bindMusePromptButtons();
    if (document.body) document.body.classList.add('il-muse-page');
    if (isMobileShell()) {
      ensureTabNav();
      wireKeyboardAware();
    }
    var nodes = document.querySelectorAll('[data-il-muse]');
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
  }

  g.ILMuse = { mount: mount, boot: boot, load: load, save: save, STORAGE: STORAGE, voiceSupport: voiceSupport, promptFrom: promptFrom, isMobileShell: isMobileShell, splitBubbles: splitBubbles, localNudges: localNudges, speakText: speakText };
  g.IL_MUSE = g.IL_MUSE || {};

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
;

/* ---- source: assets/il-challenge.js (5217 bytes) ---- */
/**
 * SuperLab Challenge of the Day — copy-paste verify + local proof feed.
 * Storage: il.challenge.done.v1, il.evidence.feed.v1  Mount: [data-il-challenge]
 */
(function (g) {
  'use strict';
  var DONE = 'il.challenge.done.v1';
  var EVIDENCE = 'il.evidence.feed.v1';
  function dayKey() {
    var d = new Date();
    var start = new Date(Date.UTC(2026, 0, 1));
    var day = Math.floor((d - start) / 86400000);
    return day;
  }
  var CHALLENGES = [
    { id: 'cotd-kind-get', title: 'Namespace inventory', steps: ['cd devops-superlab (or your clone)', 'make kind-up  # if cluster not up', 'kubectl -n superlab-dev get deploy,svc,hpa'], prove: 'Paste: you see deploy + svc lines (or honest empty if not provisioned yet).' },
    { id: 'cotd-kustomize', title: 'Kustomize dry-run', steps: ['kustomize build overlays/dev | head -n 40', 'OR: kubectl kustomize overlays/dev | head -n 40'], prove: 'Manifest heads show Namespace / Deployment without secrets in plain text.' },
    { id: 'cotd-argo', title: 'GitOps sync story', steps: ['Open Argo CD UI or CLI for the SuperLab app', 'Explain OutOfSync vs Synced in one sentence'], prove: 'Write: source of truth is Git; live edits are drift.' },
    { id: 'cotd-gatekeeper', title: 'Policy deny demo', steps: ['kubectl apply -f apps/demo/ (or policy sample)', 'Watch admit deny for privileged pod'], prove: 'Note the constraint name that denied the object.' },
    { id: 'cotd-gha', title: 'CI graph', steps: ['Open .github/workflows in SuperLab', 'Name the job that builds or lints'], prove: 'Job name + one honest limitation (no cloud deploy required).' }
  ];
  function esc(s) { return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function loadDone() { try { return JSON.parse(g.localStorage.getItem(DONE) || '{}') || {}; } catch (e) { return {}; } }
  function saveDone(d) { try { g.localStorage.setItem(DONE, JSON.stringify(d)); } catch (e) {} }
  function pushEvidence(text) {
    try { var feed = JSON.parse(g.localStorage.getItem(EVIDENCE) || '[]') || []; feed.unshift({ t: Date.now(), kind: 'challenge', text: text }); if (feed.length > 48) feed.length = 48; g.localStorage.setItem(EVIDENCE, JSON.stringify(feed)); } catch (e) {}
  }
  function todayChallenge() { return CHALLENGES[Math.abs(dayKey()) % CHALLENGES.length]; }
  function paint(root) {
    var ch = todayChallenge();
    var done = loadDone();
    var isDone = !!done[ch.id];
    var html = '<div class="il-challenge"><p class="il-kicker">Challenge of the Day</p><h3 class="mt-2 font-display text-2xl">' + esc(ch.title) + '</h3><p class="mt-2 text-sm text-muted">One deep SuperLab rhythm — not a fake fleet. Mark done only if you actually ran or honestly simulated the steps.</p><ol class="il-challenge-steps mt-5">';
    ch.steps.forEach(function (s, i) {
      html += '<li class="il-challenge-step"><div class="il-challenge-step-head"><span class="font-mono text-[0.58rem] uppercase tracking-[0.16em] text-gold">Step ' + (i + 1) + '</span><button type="button" class="il-challenge-copy" data-copy="' + esc(s) + '">Copy</button></div><pre class="il-challenge-pre">' + esc(s) + '</pre></li>';
    });
    html += '</ol><p class="mt-4 text-sm text-muted"><strong class="text-paper">Prove:</strong> ' + esc(ch.prove) + '</p>';
    html += '<div class="mt-5 flex flex-wrap gap-3"><button type="button" class="inline-flex h-10 items-center rounded-lg ' + (isDone ? 'border border-cyan/40 text-cyan' : 'bg-paper text-void') + ' px-4 font-display text-[0.65rem] font-medium uppercase tracking-[0.14em]" data-il-challenge-done>' + (isDone ? 'Done ✓' : 'Mark verified') + '</button><a href="/labs/superlab/" class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-paper">SuperLab hub</a><a href="/proof/" class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-paper">Export proof</a></div></div>';
    root.innerHTML = html;
    root.querySelectorAll('[data-copy]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var t = btn.getAttribute('data-copy');
        if (g.navigator && g.navigator.clipboard && g.navigator.clipboard.writeText) g.navigator.clipboard.writeText(t);
        btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = 'Copy'; }, 1200);
      });
    });
    var mark = root.querySelector('[data-il-challenge-done]');
    if (mark) mark.addEventListener('click', function () {
      var d = loadDone(); d[ch.id] = Date.now(); saveDone(d); pushEvidence('CotD verified: ' + ch.title); if (g.ILGame && g.ILGame.award) try { g.ILGame.award('cotd', 10, { id: 'cotd:' + ch.id }); } catch (e) {} paint(root);
    });
  }
  function boot() { var nodes = document.querySelectorAll('[data-il-challenge]'); for (var i = 0; i < nodes.length; i++) paint(nodes[i]); }
  g.ILChallenge = { boot: boot, paint: paint, todayChallenge: todayChallenge };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})(typeof window !== 'undefined' ? window : this);
;
