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
      href: "/prep/drills/bny-interview/#tell-me",
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
    var s = safeParse(global.localStorage.getItem(STORAGE_KEY), null);
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
