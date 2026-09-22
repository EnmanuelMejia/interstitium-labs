/**
 * IL Muse / Lab Muse — Muse-class interaction shell (Interstitium Labs).
 * Mobile hooks: full-bleed shell ≤768px / standalone / Capacitor (see il-muse-mobile.css).
 * Brand: cyan/gold/void + Interstitium lockup — not Meta colors or trademarks.
 * Default avatar theme: Dee (Monas-derived geometric mark) — Interstitium original artwork;
 *   inspired by historical John Dee; not a museum portrait or Meta Muse avatar.
 * Interaction patterns inspired by public Muse design posts (introducing.muse.ai).
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
      name: 'Lab Muse',
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
    nav.setAttribute('aria-label', 'Lab Muse companion');
    var path = (g.location && g.location.pathname) || '';
    var items = [
      ['/coach/', 'Muse', '◆', path.indexOf('/coach') === 0],
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
    var u = new g.SpeechSynthesisUtterance(String(text).slice(0, 1400));
    var voices = listVoices();
    if (state.voiceURI) {
      for (var i = 0; i < voices.length; i++) {
        if (voices[i].voiceURI === state.voiceURI) { u.voice = voices[i]; break; }
      }
    }
    u.rate = 1.02;
    u.onend = function () { if (onEnd) onEnd(); };
    u.onerror = function () { if (onEnd) onEnd(); };
    g.speechSynthesis.speak(u);
  }

  function detectTopic(text) {
    if (/cidr|subnet|netmask|\/2[0-9]/i.test(text)) return 'cidr';
    if (/git|rebase|merge|commit|detached/i.test(text)) return 'git';
    if (/pod|kubectl|k8s|kubernetes|crashloop/i.test(text)) return 'k8s';
    if (/terraform|tfstate|iac/i.test(text)) return 'terraform';
    if (/jenkins|github actions|pipeline|ci\/?cd|workflow/i.test(text)) return 'ci';
    if (/linux|systemd|journalctl|chmod|ssh|oom/i.test(text)) return 'linux';
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
        body: 'Lean T0 stays default. Approve to open Muse settings → Model (local policy only).',
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
        body: 'Practice beats answer dumps. Bring Muse a hypothesis after one lab sitting.',
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
        body: 'Export inspectable markdown from local adaptive + Muse + exam state — no invented server claims.',
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
        body: 'Jump the hire loop — Adapt placement → path phase → lab → Muse → proof.',
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
      if (!g0.done) add('goal:' + g0.id, 'Goal nudge · ' + g0.title, 'Open goal · ask Muse for a Socratic next step', '/coach/');
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
      var n = new Notification(title || 'Lab Muse', {
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
          tryLocalNotification('Lab Muse · study nudge', top.title);
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
      var log = app.querySelector('[data-muse-transcript]');
      if (log) log.scrollTop = log.scrollHeight;
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
      return '<div class="il-muse-mobile-bar" role="toolbar" aria-label="Lab Muse drawers">' +
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
        ' title="Lab Muse · ' + esc(av.label) + '" aria-label="Lab Muse activity">' +
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
      if (!bubbles) {
        bubbles = '<div class="il-muse-bubble il-muse-bubble--system">One long main chat · interrupt anytime · side chats for topic contexts. I stay Socratic — show your work.</div>';
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
        '<textarea class="il-muse-composer__input" data-muse-input rows="1" placeholder="Ask a stuck question — interrupt anytime…" aria-label="Message Lab Muse"></textarea>' +
        '<button type="submit" class="il-muse-send" data-i18n="muse.send">Send</button>' +
        '</form>' + voiceFb +
        '<p class="il-muse-disclaimer"><strong>Honesty:</strong> Inspired by Muse <em>interaction design</em> (public posts) — educational agent, not Meta’s product. Avatar theme inspired by historical John Dee (Monas / hermetic scholar energy); Interstitium original artwork — not a museum portrait or Meta Muse asset. Voice = browser Web Speech. Models: local rules by default; Ollama / lab-control optional. No fake API keys. Prefer lean tier; scale when demand grows.</p>' +
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
        return '<a href="' + esc(l.href) + '">' + esc(l.label) + '</a>';
      }).join('');
      var list = (a.checklist || []).map(function (c) { return '<li>' + esc(c) + '</li>'; }).join('');
      return '<div class="il-muse-artifact">' +
        '<div class="il-muse-artifact__kicker">Artifact · ' + esc(a.kind || 'card') + '</div>' +
        '<h4 class="il-muse-artifact__title">' + esc(a.title) + '</h4>' +
        '<div class="il-muse-artifact__body">' + esc(a.body || '') + '</div>' +
        (a.command ? '<pre class="il-muse-artifact__cmd">' + esc(a.command) + '</pre>' : '') +
        (list ? '<ul class="il-muse-artifact__list">' + list + '</ul>' : '') +
        (links ? '<div class="il-muse-artifact__links">' + links + '</div>' : '') +
        '</div>';
    }

    function panelHTML(ideas, demand, routerState, active, catalog, vs) {
      var tabs = [
        ['goals', 'Goals'], ['ideas', 'Ideas'], ['library', 'Library'],
        ['model', 'Model'], ['settings', 'Muse']
      ];
      var tabBtns = tabs.map(function (t) {
        return '<button type="button" class="il-muse-tab' + (panelTab === t[0] ? ' is-on' : '') + '" data-muse-tab="' + t[0] + '">' + t[1] + '</button>';
      }).join('');
      var body = '';
      if (panelTab === 'goals') body = goalsPanel();
      else if (panelTab === 'ideas') body = ideasPanel(ideas);
      else if (panelTab === 'library') body = libraryPanel();
      else if (panelTab === 'model') body = modelPanel(demand, routerState, active, catalog);
      else body = settingsPanel(vs);
      return '<aside class="il-muse-panel" aria-label="Lab Muse panels">' +
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
          '<button type="button" data-muse-idea-ask="' + esc(idea.title) + '" class="il-muse-chip-btn">Ask Muse</button></div></div>';
      }).join('');
      return '<div class="il-muse-panel-section"><h3 data-i18n="muse.ideas">Ideas</h3>' +
        '<p class="hint">Suggestions from Adaptive weak topics when present.</p>' + rows + '</div>';
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
        ? '<p class="hint" style="color:#d4a853">' + esc(demand.suggestReason || ('Consider ' + demand.suggestedTier)) + '</p>'
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

    function settingsPanel(vs) {
      var voices = listVoices();
      var vopts = '<option value="">Browser default</option>' + voices.map(function (v) {
        return '<option value="' + esc(v.voiceURI) + '"' + (state.voiceURI === v.voiceURI ? ' selected' : '') + '>' + esc(v.name) + '</option>';
      }).join('');
      var mems = (state.memories || []).map(function (m, i) {
        return '<li><span>' + esc(m) + '</span><button type="button" data-muse-mem-del="' + i + '">Remove</button></li>';
      }).join('');
      return '<div class="il-muse-panel-section"><h3 data-i18n="muse.settings">Muse settings</h3>' +
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
          var idx = parseInt(btn.getAttribute('data-idx'), 10);
          var chat = getChat(state, state.activeChatId);
          var msg = chat.messages[idx];
          if (!msg || !msg.approval) return;
          var which = btn.getAttribute('data-muse-approve');
          var ap = msg.approval;
          var act = which === 'primary' ? (ap.primary || {}) : (ap.secondary || {});
          msg.approval.dismissed = true;
          pushActivity(state, 'Approval · ' + (act.label || which));
          persist();
          if (act.href) {
            g.location.href = act.href;
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
        if (epEl && epEl.value && router().setCreds) {
          router().setCreds(bid, epEl.value.trim(), '');
        }
        router().setPolicy({ backend: bid, primary: mid, mode: 'manual' });
        pushActivity(state, 'Model set ' + bid + '/' + mid);
        persist(); render();
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
        if (n) state.name = n.value.trim() || 'Lab Muse';
        if (p) state.personality = p.value.trim() || state.personality;
        if (ton) state.tone = ton.value;
        if (vo) state.voiceURI = vo.value;
        pushActivity(state, 'Updated Muse settings');
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
      chat.messages.push({ role: 'user', text: text, t: Date.now() });
      pushActivity(state, 'User message');
      persist();
      setStatus('thinking');
      render();

      askModel(chat, topic, state).then(function (raw) {
        var res = normRes(raw);
        var art = maybeArtifact(text, res.text, topic);
        var parts = splitBubbles(res.text, 4);
        var i;
        for (i = 0; i < parts.length; i++) {
          var msg = {
            role: 'assistant',
            text: parts[i],
            t: Date.now() + i,
            source: res.source,
            backendId: res.backendId,
            modelId: res.modelId,
            partIndex: i + 1,
            partOf: parts.length
          };
          if (art && i === parts.length - 1) {
            msg.artifact = art;
            state.artifacts = state.artifacts || [];
            state.artifacts.push(art);
          }
          chat.messages.push(msg);
        }
        var appr = maybeApproval(text, res.text, topic);
        if (appr) {
          chat.messages.push({ role: 'approval', approval: appr, t: Date.now() });
        }
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
          if (router() && router().recommend) {
            var promo = analytics() && analytics().recommendPrimary
              ? analytics().recommendPrimary({ current: { backendId: res.backendId, modelId: res.modelId } })
              : null;
            if (promo && promo.switchTo && router().setPolicy) {
              router().setPolicy({ primary: promo.switchTo.modelId });
              pushActivity(state, 'Auto-promoted ' + promo.switchTo.modelId);
            }
          }
          if (g.ILGame && g.ILGame.award) g.ILGame.award('muse_ask', 5, { id: 'muse:' + Date.now() });
        } catch (e) {}
        speakText(res.text, state, function () { setStatus('idle'); });
      }, function (err) {
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

  g.ILMuse = { mount: mount, boot: boot, load: load, save: save, STORAGE: STORAGE, voiceSupport: voiceSupport, promptFrom: promptFrom, isMobileShell: isMobileShell, splitBubbles: splitBubbles, localNudges: localNudges };
  g.IL_MUSE = g.IL_MUSE || {};

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
