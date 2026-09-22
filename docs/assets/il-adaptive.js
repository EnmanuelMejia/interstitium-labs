/**
 * IL Adaptive Learning OS — CAT-like + ALEKS-like local engine.
 * Storage: localStorage key il.adaptive.v1
 * API: ILAdaptive.place(), next(), answer(id, correct), readyTopics(),
 *      pieState(), render(el), loadBank(), getState(), reset(), gates()
 * No cloud VMs, no LLM/Stripe secrets.
 */
(function (g) {
  'use strict';

  var STORAGE = 'il.adaptive.v1';
  var BANK_URL = '/assets/il-item-bank.json';
  var PLACE_MIN = 8;
  var PLACE_MAX = 12;
  var MASTERY_KNOWN = 0.75;
  var MASTERY_LEARNING = 0.35;
  var DECAY_MS = 1000 * 60 * 60 * 24 * 5; // ~5 days soft decay nudge
  var bank = null;
  var session = { mode: 'idle', queue: [], seen: {}, n: 0, why: '' };

  function clamp(x, lo, hi) { return Math.max(lo, Math.min(hi, x)); }

  function emptyState() {
    return {
      v: 1,
      placed: false,
      theta: 0,
      se: 1,
      n: 0,
      topics: {},
      exposure: {},
      recentIds: [],
      pathId: null,
      challengeCorrect: 0,
      history: [],
      updatedAt: Date.now()
    };
  }

  function loadState() {
    try {
      var raw = g.localStorage.getItem(STORAGE);
      if (raw) {
        var s = JSON.parse(raw);
        if (s && s.v === 1) return s;
      }
    } catch (e) {}
    return emptyState();
  }

  function saveState(s) {
    s.updatedAt = Date.now();
    try { g.localStorage.setItem(STORAGE, JSON.stringify(s)); } catch (e) {}
    return s;
  }

  function ensureTopic(state, id) {
    if (!state.topics[id]) {
      state.topics[id] = { mastery: 0.2, exposure: 0, streak: 0, lastSeen: 0, status: 'locked' };
    }
    return state.topics[id];
  }

  function conceptById(id) {
    if (!bank) return null;
    for (var i = 0; i < bank.concepts.length; i++) {
      if (bank.concepts[i].id === id) return bank.concepts[i];
    }
    return null;
  }

  function itemById(id) {
    if (!bank) return null;
    for (var i = 0; i < bank.items.length; i++) {
      if (bank.items[i].id === id) return bank.items[i];
    }
    return null;
  }

  function prereqsMet(state, concept, thr) {
    thr = thr == null ? 0.55 : thr;
    var ps = concept.prereqs || [];
    for (var i = 0; i < ps.length; i++) {
      var t = ensureTopic(state, ps[i]);
      if ((t.mastery || 0) < thr) return false;
    }
    return true;
  }

  function refreshStatuses(state) {
    if (!bank) return;
    bank.concepts.forEach(function (c) {
      var t = ensureTopic(state, c.id);
      // soft decay
      if (t.lastSeen && t.mastery >= MASTERY_KNOWN) {
        var age = Date.now() - t.lastSeen;
        if (age > DECAY_MS) {
          var steps = Math.floor(age / DECAY_MS);
          t.mastery = clamp(t.mastery - 0.04 * steps, 0.45, 1);
        }
      }
      var thr = c.threshold || MASTERY_KNOWN;
      if (!prereqsMet(state, c, 0.55) && t.mastery < thr) {
        t.status = 'locked';
      } else if (t.mastery >= thr) {
        t.status = 'known';
      } else if (prereqsMet(state, c, 0.55)) {
        t.status = 'learning';
      } else {
        t.status = 'locked';
      }
    });
  }

  function readyTopics(state) {
    state = state || loadState();
    if (!bank) return [];
    refreshStatuses(state);
    var ready = [];
    bank.concepts.forEach(function (c) {
      var t = state.topics[c.id];
      if (t && t.status === 'learning') {
        ready.push({
          id: c.id,
          title: c.title,
          domain: c.domain,
          mastery: t.mastery,
          status: t.status
        });
      }
    });
    ready.sort(function (a, b) { return b.mastery - a.mastery; });
    return ready;
  }

  function pieState(state) {
    state = state || loadState();
    if (!bank) return { known: 0, learning: 0, locked: 0, total: 0, slices: [] };
    refreshStatuses(state);
    var known = 0, learning = 0, locked = 0;
    var slices = bank.concepts.map(function (c) {
      var t = state.topics[c.id];
      var st = (t && t.status) || 'locked';
      if (st === 'known') known++;
      else if (st === 'learning') learning++;
      else locked++;
      return { id: c.id, title: c.title, domain: c.domain, status: st, mastery: t ? t.mastery : 0 };
    });
    return { known: known, learning: learning, locked: locked, total: bank.concepts.length, slices: slices };
  }

  // 2PL IRT helpers
  function sigmoid(x) { return 1 / (1 + Math.exp(-x)); }

  function pCorrect(theta, item) {
    var a = item.a || 1;
    var b = item.b || 0;
    var c = item.c != null ? item.c : 0.25;
    return c + (1 - c) * sigmoid(a * (theta - b));
  }

  function fisherInfo(theta, item) {
    var a = item.a || 1;
    var b = item.b || 0;
    var c = item.c != null ? item.c : 0.25;
    var pStar = sigmoid(a * (theta - b));
    var p = c + (1 - c) * pStar;
    var q = 1 - p;
    if (p < 1e-6 || q < 1e-6) return 0;
    var num = Math.pow(a * (1 - c) * pStar * (1 - pStar), 2);
    return num / (p * q);
  }

  function updateTheta(state, item, correct) {
    var a = item.a || 1;
    var b = item.b || 0;
    var c = item.c != null ? item.c : 0.25;
    var theta = state.theta;
    // one Newton / EAP-lite step
    var p = pCorrect(theta, item);
    var residual = (correct ? 1 : 0) - p;
    var info = Math.max(fisherInfo(theta, item), 0.15);
    theta = theta + residual / info;
    // mild prior pull toward 0
    theta = 0.92 * theta;
    state.theta = clamp(theta, -3, 3);
    state.n = (state.n || 0) + 1;
    state.se = clamp(1 / Math.sqrt(Math.max(info * state.n, 0.2)), 0.25, 1.5);
  }

  function updateMastery(state, item, correct) {
    (item.conceptIds || []).forEach(function (cid) {
      var t = ensureTopic(state, cid);
      var prior = t.mastery;
      // BKT-ish / Elo blend
      if (correct) {
        t.mastery = clamp(prior + 0.12 * (1 - prior), 0, 1);
        t.streak = (t.streak || 0) + 1;
      } else {
        t.mastery = clamp(prior - 0.1 * prior - 0.05, 0, 1);
        t.streak = 0;
        // reopen prereq nudge: slight demotion of first unmet? skip — fringe handles
      }
      t.exposure = (t.exposure || 0) + 1;
      t.lastSeen = Date.now();
    });
    state.exposure[item.id] = (state.exposure[item.id] || 0) + 1;
    state.recentIds = (state.recentIds || []).concat([item.id]).slice(-40);
  }

  function domainCounts(recentItems) {
    var counts = {};
    recentItems.forEach(function (it) {
      (it.conceptIds || []).forEach(function (cid) {
        var c = conceptById(cid);
        if (c) counts[c.domain] = (counts[c.domain] || 0) + 1;
      });
    });
    return counts;
  }

  function selectNextItem(state, mode) {
    if (!bank || !bank.items.length) return null;
    refreshStatuses(state);
    var theta = state.theta || 0;
    var recent = state.recentIds || [];
    var exclude = {};
    recent.slice(-12).forEach(function (id) { exclude[id] = true; });
    if (session.seen) {
      Object.keys(session.seen).forEach(function (id) { exclude[id] = true; });
    }

    var fringeIds = {};
    readyTopics(state).forEach(function (r) { fringeIds[r.id] = true; });

    var candidates = bank.items.filter(function (it) {
      if (exclude[it.id]) return false;
      if (mode === 'place') return true;
      // practice: prefer fringe / learning concepts; allow known for SR
      var ok = false;
      var due = false;
      (it.conceptIds || []).forEach(function (cid) {
        var t = ensureTopic(state, cid);
        if (fringeIds[cid]) ok = true;
        if (t.status === 'learning') ok = true;
        if (t.status === 'known' && t.lastSeen && (Date.now() - t.lastSeen) > DECAY_MS * 0.6) {
          due = true; ok = true;
        }
      });
      return ok || mode === 'challenge';
    });

    if (!candidates.length) {
      candidates = bank.items.filter(function (it) { return !exclude[it.id]; });
    }
    if (!candidates.length) candidates = bank.items.slice();

    var recentObjs = recent.slice(-8).map(itemById).filter(Boolean);
    var dcounts = domainCounts(recentObjs);

    var best = null;
    var bestScore = -1e9;
    var why = '';

    candidates.forEach(function (it) {
      var info = fisherInfo(theta, it);
      // prefer difficulty near ability: |b - theta| small
      var band = 1 / (1 + Math.pow((it.b || 0) - theta, 2));
      var exposurePenalty = 0.08 * (state.exposure[it.id] || 0);
      // content quota: penalize over-represented domains in recent window
      var domPenalty = 0;
      (it.conceptIds || []).forEach(function (cid) {
        var c = conceptById(cid);
        if (c && dcounts[c.domain] >= 3) domPenalty += 0.35;
        if (mode !== 'place' && fringeIds[cid]) info += 0.15;
      });
      var score = info * 1.4 + band - exposurePenalty - domPenalty;
      if (mode === 'place') {
        // breadth: slight boost for low-exposure concepts
        (it.conceptIds || []).forEach(function (cid) {
          var t = ensureTopic(state, cid);
          if (t.exposure < 1) score += 0.2;
        });
      }
      if (score > bestScore) {
        bestScore = score;
        best = it;
        why = 'Max information near θ=' + theta.toFixed(2) +
          ' (b=' + (it.b || 0) + ', I≈' + info.toFixed(2) + ')';
        if (mode !== 'place') why += '; fringe/ready preference applied';
      }
    });

    session.why = why;
    return best;
  }

  function recommendPath(state) {
    if (!bank || !bank.paths) return null;
    refreshStatuses(state);
    var pie = pieState(state);
    var knownRatio = pie.total ? pie.known / pie.total : 0;
    // Associate if early; Engineer if associate concepts mostly known
    var assoc = bank.paths[0];
    var eng = bank.paths[1];
    var assocReady = 0;
    (assoc.conceptIds || []).forEach(function (id) {
      var t = ensureTopic(state, id);
      if (t.mastery >= 0.55) assocReady++;
    });
    if (assocReady >= Math.ceil((assoc.conceptIds.length || 1) * 0.65) || knownRatio > 0.4) {
      return eng;
    }
    return assoc;
  }

  function evaluateGates(state) {
    state = state || loadState();
    if (!bank) return [];
    refreshStatuses(state);
    var path = null;
    if (state.pathId) {
      for (var i = 0; i < bank.paths.length; i++) {
        if (bank.paths[i].id === state.pathId) path = bank.paths[i];
      }
    }
    if (!path) path = recommendPath(state);
    if (!path) return [];
    return (path.gates || []).map(function (g) {
      var ok = true;
      var details = [];
      (g.rules || []).forEach(function (r) {
        if (r.type === 'mastery') {
          (r.conceptIds || []).forEach(function (cid) {
            var t = ensureTopic(state, cid);
            var pass = (t.mastery || 0) >= (r.min || 0.7);
            details.push({ conceptId: cid, mastery: t.mastery, pass: pass });
            if (!pass) ok = false;
          });
        } else if (r.type === 'challenge') {
          var pass = (state.challengeCorrect || 0) >= (r.minCorrect || 8);
          details.push({ challenge: true, have: state.challengeCorrect || 0, need: r.minCorrect || 8, pass: pass });
          if (!pass) ok = false;
        }
      });
      return { id: g.id, title: g.title, unlocked: ok, details: details };
    });
  }

  function answer(id, correct) {
    var state = loadState();
    var item = itemById(id);
    if (!item) return { ok: false, error: 'unknown item' };
    correct = !!correct;
    updateTheta(state, item, correct);
    updateMastery(state, item, correct);
    if (session.mode === 'challenge' && correct) {
      state.challengeCorrect = (state.challengeCorrect || 0) + 1;
    }
    session.seen[id] = true;
    session.n = (session.n || 0) + 1;
    state.history = (state.history || []).concat([{
      id: id, correct: correct, t: Date.now(), mode: session.mode, theta: state.theta
    }]).slice(-200);

    var tip = '';
    if (item.feedback) {
      if (correct) tip = item.feedback[item.answerKey] || 'Correct.';
      else {
        // Socratic: wrong choice tip preferred if we knew key — callers pass via answerChoice
        tip = 'Not yet — rethink the concept; hints stay Socratic (no answer dump).';
      }
    }

    if (session.mode === 'place') {
      if (session.n >= PLACE_MAX || (session.n >= PLACE_MIN && state.se < 0.45)) {
        state.placed = true;
        var rec = recommendPath(state);
        if (rec) state.pathId = rec.id;
        session.mode = 'practice';
      }
    }

    refreshStatuses(state);
    saveState(state);
    return {
      ok: true,
      correct: correct,
      tip: tip,
      state: state,
      pie: pieState(state),
      ready: readyTopics(state),
      why: session.why,
      placed: state.placed,
      pathId: state.pathId
    };
  }

  function answerChoice(id, choiceKey) {
    var item = itemById(id);
    if (!item) return { ok: false, error: 'unknown item' };
    var correct = choiceKey === item.answerKey;
    var res = answer(id, correct);
    if (item.feedback && item.feedback[choiceKey]) {
      res.tip = correct
        ? ('✓ ' + item.feedback[choiceKey])
        : ('Not yet — ' + item.feedback[choiceKey] + ' Try another angle; do not memorize the letter.');
    }
    res.choiceKey = choiceKey;
    return res;
  }

  function next() {
    var state = loadState();
    if (!bank) return null;
    if (session.mode === 'idle') session.mode = state.placed ? 'practice' : 'place';
    var item = selectNextItem(state, session.mode);
    if (!item) return null;
    return {
      item: item,
      mode: session.mode,
      why: session.why,
      theta: state.theta,
      se: state.se,
      n: session.n,
      pie: pieState(state),
      ready: readyTopics(state)
    };
  }

  function place() {
    var state = loadState();
    session = { mode: 'place', queue: [], seen: {}, n: 0, why: '' };
    // soft reset of session counters but keep prior mastery if re-placing
    state.placed = false;
    saveState(state);
    return next();
  }

  function startPractice() {
    session = { mode: 'practice', queue: [], seen: {}, n: 0, why: '' };
    return next();
  }

  function startChallenge() {
    session = { mode: 'challenge', queue: [], seen: {}, n: 0, why: '' };
    return next();
  }

  function reset() {
    session = { mode: 'idle', queue: [], seen: {}, n: 0, why: '' };
    var s = emptyState();
    saveState(s);
    return s;
  }

  function loadBank(url) {
    url = url || BANK_URL;
    return fetch(url, { credentials: 'same-origin' })
      .then(function (r) {
        if (!r.ok) throw new Error('bank ' + r.status);
        return r.json();
      })
      .then(function (data) {
        bank = data;
        var state = loadState();
        refreshStatuses(state);
        saveState(state);
        return data;
      });
  }

  function setBank(data) {
    bank = data;
    return bank;
  }

  /* —— UI render —— */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function renderPie(host, pie) {
    host.innerHTML = '';
    var wrap = el('div', 'il-adapt-pie');
    var total = Math.max(pie.total, 1);
    var k = pie.known / total, l = pie.learning / total, x = pie.locked / total;
    var svg = '<svg viewBox="0 0 42 42" role="img" aria-label="Knowledge pie: ' +
      pie.known + ' known, ' + pie.learning + ' learning, ' + pie.locked + ' locked">' +
      '<circle cx="21" cy="21" r="15.915" fill="transparent" stroke="rgba(232,238,245,0.08)" stroke-width="6"/>';
    var off = 0;
    function arc(frac, color) {
      if (frac <= 0) return '';
      var dash = (frac * 100).toFixed(2);
      var gap = (100 - frac * 100).toFixed(2);
      var s = '<circle cx="21" cy="21" r="15.915" fill="transparent" stroke="' + color +
        '" stroke-width="6" stroke-dasharray="' + dash + ' ' + gap +
        '" stroke-dashoffset="' + (-off).toFixed(2) + '" transform="rotate(-90 21 21)"/>';
      off += frac * 100;
      return s;
    }
    svg += arc(k, '#34d399') + arc(l, '#5eead4') + arc(x, '#475569') + '</svg>';
    var svgWrap = el('div', 'il-adapt-pie__svg');
    svgWrap.innerHTML = svg;
    var legend = el('div', 'il-adapt-pie__legend');
    legend.innerHTML =
      '<div><span class="il-dot il-dot--known"></span> Known <strong>' + pie.known + '</strong></div>' +
      '<div><span class="il-dot il-dot--learning"></span> Learning <strong>' + pie.learning + '</strong></div>' +
      '<div><span class="il-dot il-dot--locked"></span> Locked <strong>' + pie.locked + '</strong></div>';
    wrap.appendChild(svgWrap);
    wrap.appendChild(legend);
    host.appendChild(wrap);
  }

  function render(root) {
    if (!root) return;
    root.setAttribute('data-il-adapt-ready', '1');
    root.innerHTML = '';
    root.classList.add('il-adapt');

    var status = el('p', 'il-kicker');
    status.setAttribute('data-i18n', 'adapt.status');
    status.textContent = 'Adaptive OS · local CAT + ALEKS fringe';
    root.appendChild(status);

    var grid = el('div', 'il-adapt__grid');
    var pieHost = el('div', 'il-adapt__pie-host');
    var side = el('div', 'il-adapt__side');
    var readyBox = el('div', 'il-honest-note');
    var gatesBox = el('div', 'il-adapt__gates');
    side.appendChild(readyBox);
    side.appendChild(gatesBox);
    grid.appendChild(pieHost);
    grid.appendChild(side);
    root.appendChild(grid);

    var chrome = el('div', 'il-adapt__chrome il-ux-card');
    var meta = el('p', 'il-kicker');
    var prompt = el('p', 'il-drill__prompt');
    var choices = el('div', 'il-drill__choices');
    var fb = el('div', 'il-feedback');
    fb.setAttribute('aria-live', 'polite');
    var why = el('p', 'il-adapt__why');
    var nav = el('div', 'il-adapt__nav');
    chrome.appendChild(meta);
    chrome.appendChild(prompt);
    chrome.appendChild(choices);
    chrome.appendChild(fb);
    chrome.appendChild(why);
    chrome.appendChild(nav);
    root.appendChild(chrome);

    var toolbar = el('div', 'il-adapt__toolbar');
    function btn(label, fn, cls) {
      var b = el('button', cls || 'il-coach-topic');
      b.type = 'button';
      b.textContent = label;
      b.addEventListener('click', fn);
      return b;
    }
    toolbar.appendChild(btn('Placement', function () { begin('place'); }, 'il-coach-topic'));
    toolbar.appendChild(btn('Daily practice', function () { begin('practice'); }, 'il-coach-topic'));
    toolbar.appendChild(btn('Challenge gate', function () { begin('challenge'); }, 'il-coach-topic'));
    toolbar.appendChild(btn('Reset local state', function () {
      if (g.confirm && !g.confirm('Reset adaptive mastery on this device?')) return;
      reset(); paintShell(); begin('place');
    }, 'il-coach-topic'));
    root.appendChild(toolbar);

    var current = null;
    var locked = false;

    function paintShell() {
      var state = loadState();
      var pie = pieState(state);
      renderPie(pieHost, pie);
      var ready = readyTopics(state);
      readyBox.innerHTML = '<strong>Ready-to-learn (ALEKS fringe):</strong> ' +
        (ready.length
          ? ready.slice(0, 5).map(function (r) {
              return r.title + ' (' + Math.round(r.mastery * 100) + '%)';
            }).join(' · ')
          : 'Complete Placement to unlock the fringe.');
      var gates = evaluateGates(state);
      var pathLabel = state.pathId || (recommendPath(state) || {}).id || '—';
      gatesBox.innerHTML = '<p class="il-kicker">Path · ' + pathLabel + '</p>' +
        gates.map(function (g) {
          return '<div class="il-adapt-gate' + (g.unlocked ? ' is-open' : '') + '">' +
            (g.unlocked ? '🔓 ' : '🔒 ') + g.title + '</div>';
        }).join('') || '<p class="text-sm text-muted">Gates appear after bank load.</p>';
    }

    function showItem(pack) {
      locked = false;
      fb.className = 'il-feedback';
      fb.textContent = '';
      if (!pack || !pack.item) {
        meta.textContent = 'Session complete · fringe updated';
        prompt.textContent = 'No more items in this band. Review ready topics or deepen via vendor map.';
        choices.innerHTML = '';
        why.textContent = '';
        return;
      }
      current = pack.item;
      meta.textContent = (pack.mode || 'practice').toUpperCase() +
        ' · item ' + ((pack.n || 0) + 1) +
        ' · θ ' + (pack.theta != null ? pack.theta.toFixed(2) : '0') +
        ' · SE ' + (pack.se != null ? pack.se.toFixed(2) : '—');
      prompt.textContent = current.stem;
      why.textContent = pack.why ? ('Why this item: ' + pack.why) : '';
      choices.innerHTML = '';
      (current.choices || []).forEach(function (c) {
        var b = el('button', 'il-drill__choice');
        b.type = 'button';
        b.innerHTML = '<span class="il-drill__key"></span><span></span>';
        b.querySelector('.il-drill__key').textContent = c.key;
        b.querySelectorAll('span')[1].textContent = c.text;
        b.addEventListener('click', function () {
          if (locked) return;
          locked = true;
          var res = answerChoice(current.id, c.key);
          Array.prototype.forEach.call(choices.querySelectorAll('button'), function (btn) {
            btn.disabled = true;
            var key = btn.querySelector('.il-drill__key').textContent;
            if (key === current.answerKey) btn.classList.add('is-correct');
            if (key === c.key && !res.correct) btn.classList.add('is-wrong');
          });
          fb.classList.add('is-on', res.correct ? 'il-feedback--ok' : 'il-feedback--bad');
          fb.textContent = res.tip || (res.correct ? '✓ Correct.' : 'Not yet — rethink.');
          paintShell();
          try {
            if (g.ILGame && typeof g.ILGame.award === 'function') {
              g.ILGame.award(res.correct ? 'adapt_ok' : 'adapt_try', res.correct ? 18 : 4, { id: 'adapt:' + current.id });
            }
          } catch (e) {}
        });
        choices.appendChild(b);
      });
    }

    function begin(mode) {
      var pack;
      if (mode === 'place') pack = place();
      else if (mode === 'challenge') pack = startChallenge();
      else pack = startPractice();
      paintShell();
      showItem(pack);
    }

    nav.appendChild(btn('Next item', function () {
      var pack = next();
      showItem(pack);
      paintShell();
    }));

    paintShell();
    var state = loadState();
    begin(state.placed ? 'practice' : 'place');
  }

  function boot() {
    var nodes = document.querySelectorAll('[data-il-adaptive]');
    if (!nodes.length) return;
    loadBank().then(function () {
      for (var i = 0; i < nodes.length; i++) render(nodes[i]);
    }).catch(function (err) {
      for (var i = 0; i < nodes.length; i++) {
        nodes[i].innerHTML = '<p class="il-honest-note">Adaptive bank failed to load (local JSON). Check /assets/il-item-bank.json. ' +
          String(err && err.message || err) + '</p>';
      }
    });
  }

  g.ILAdaptive = {
    place: place,
    next: next,
    answer: answer,
    answerChoice: answerChoice,
    readyTopics: function () { return readyTopics(loadState()); },
    pieState: function () { return pieState(loadState()); },
    render: render,
    loadBank: loadBank,
    setBank: setBank,
    getState: loadState,
    reset: reset,
    gates: evaluateGates,
    startPractice: startPractice,
    startChallenge: startChallenge,
    recommendPath: function () { return recommendPath(loadState()); },
    boot: boot
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
