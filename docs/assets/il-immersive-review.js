/**
 * IL Immersive Review v1.3.0 (2026-10-21; v1.0.0 2026-10-13) — adaptive remediation loop for the CKA 3D sims.
 *
 * Closes the loop the 2026-10-12 exam left open: every exam miss, timeout, and free-play
 * drill result becomes a spaced-repetition card keyed to the exact predict checkpoint,
 * and the review queue re-serves that checkpoint on its authored 3D scene. Weak domains
 * (lowest on-device mastery) top up the queue with unseen checkpoints and steer the next
 * "adaptive" exam paper.
 *
 * Scheduler: Leitner-style boxes with latency-aware grading (correct-but-slow = "hard",
 * box held). Deterministic, documented intervals — not FSRS, not a trained model.
 * Storage: localStorage il.immersiveReview.v1 on this device only. No server, no account,
 * no cohort data: every number shown is computed from this device's own answers.
 *
 * Would Elon be impressed by a mock exam whose misses evaporate when the tab closes
 * (KodeKloud staff, 2026-04: "each session ... you start fresh")? No — this is the fix.
 * v1.1.0 (2026-10-14): speakLine() — the one-line Lab Muse briefing the review lobby reads
 * aloud through the browser's own Web Speech synthesis (no cloud TTS, no API key).
 * v1.2.0 (2026-10-20): coach-driven CLI cards — a CLI-lab step the learner needed `solution` for (or failed
 * `check` on twice) becomes a card in THIS queue (same store, same Leitner boxes), keyed
 * simId::cli:<taskId>:<step>. The review stage re-opens that drill's task with the earlier steps replayed, and
 * the card is graded by whether the learner gets the step verified without `solution`. Mastery % stays computed
 * from predict checkpoints (CLI cards are scheduled and counted, never invented as top-ups).
 * v1.3.0 (2026-10-21): + gateway-api checkpoints; blueprint() — on-device mastery weighted by the official CNCF CKA
 * domain weights, with the weakest domain by points at stake. speakLine() names it when there is evidence.
 */
(function (root, factory) {
  var api = factory(root);
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.ILImmersiveReview = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function (g) {
  'use strict';

  var VERSION = '1.3.0';
  var STORE_KEY = 'il.immersiveReview.v1';
  var MIN = 60 * 1000, HOUR = 60 * MIN, DAY = 24 * HOUR;
  /** Box → interval until next due. Box 0 = relearn now; box 1 = 10-minute relearning step. */
  var INTERVALS = [0, 10 * MIN, 1 * DAY, 3 * DAY, 7 * DAY, 16 * DAY, 35 * DAY];
  var MAX_BOX = INTERVALS.length - 1;
  /** Correct answers slower than this are graded "hard" (box held, not promoted). */
  var SLOW_MS = 45000;
  var LOG_CAP = 500;
  var HONESTY = 'On-device spaced repetition (Leitner boxes, latency-aware) over the in-browser 3D rules engine. ' +
    'Not FSRS, not a trained model, no server or cohort data, not a live cluster.';

  /* CKA scope mirrors ILImmersiveExam so the loop and the paper agree on domains. */
  var CKA_DOMAIN = {
    'etcd-quorum': 'Cluster Architecture',
    'control-plane-failure': 'Troubleshooting',
    'sched-taints': 'Scheduling',
    'hpa-scale': 'Workloads',
    'storage-csi': 'Storage',
    'config-propagation': 'Configuration',
    'rbac-authz': 'Security',
    'netpol-isolation': 'Networking',
    'cni-network': 'Networking',
    'ingress-routing': 'Networking',
    'gateway-api': 'Networking',
    'node-troubleshoot': 'Troubleshooting'
  };

  function key(simId, scenarioId) { return simId + '::' + scenarioId; }
  /** CLI-lab drills outside the CKA scope still get coach cards, under an honest domain label. */
  var CLI_DOMAIN_EXTRA = { 'aws-az-failure': 'AWS SAA-C03 · Resilience' };
  function cliScenarioId(taskId, step) { return 'cli:' + taskId + ':' + step; }
  function parseCli(scenarioId) {
    var m = /^cli:([a-z0-9-]+):(\d+)$/.exec(String(scenarioId || ''));
    return m ? { taskId: m[1], step: +m[2] } : null;
  }
  function now0(n) { return n != null ? n : Date.now(); }

  var mem = null; /* fallback when localStorage is unavailable (private mode / node) */
  function ls() {
    try { return (g && g.localStorage) || (typeof localStorage !== 'undefined' ? localStorage : null); } catch (e) { return null; }
  }
  function emptyDb() { return { v: 1, cards: {}, log: [], sessions: 0, examsIngested: 0 }; }
  function load() {
    var s = ls();
    if (!s) return mem || (mem = emptyDb());
    try {
      var db = JSON.parse(s.getItem(STORE_KEY) || 'null');
      if (!db || typeof db !== 'object' || !db.cards) return emptyDb();
      if (!Array.isArray(db.log)) db.log = [];
      return db;
    } catch (e) { return emptyDb(); }
  }
  function save(db) {
    if (db.log.length > LOG_CAP) db.log = db.log.slice(db.log.length - LOG_CAP);
    var s = ls();
    if (!s) { mem = db; return db; }
    try { s.setItem(STORE_KEY, JSON.stringify(db)); } catch (e) { mem = db; }
    if (typeof setTimeout === 'function' && typeof document !== 'undefined') setTimeout(paintBadges, 0);
    return db;
  }
  function reset() {
    var s = ls();
    mem = null;
    if (s) { try { s.removeItem(STORE_KEY); } catch (e) { /* ignore */ } }
    return emptyDb();
  }

  /** CKA predict checkpoints, one entry per (sim, scenario). */
  function checkpoints(S) {
    var out = [];
    if (!S || !S.get) return out;
    for (var id in CKA_DOMAIN) {
      var sim = S.get(id);
      if (!sim || !sim.scenarios) continue;
      for (var j = 0; j < sim.scenarios.length; j++) {
        var sc = sim.scenarios[j];
        if (!sc || !sc.predict) continue;
        out.push({
          k: key(id, sc.id), simId: id, scenarioId: sc.id, domain: CKA_DOMAIN[id],
          title: sim.title, label: sc.label, glb: sim.glb,
          q: sc.predict.q, options: sc.predict.options.slice(), answer: sc.predict.answer, why: sc.predict.why
        });
      }
    }
    return out;
  }

  /** One checkpoint per CLI-lab task step (ILImmersiveCLI packs). Only used to re-serve coach-driven cards. */
  function cliCheckpoints(C, S) {
    C = C || (g && g.ILImmersiveCLI);
    S = S || (g && g.ILImmersiveSims);
    var out = [];
    if (!C || !C.list || !C.pack) return out;
    C.list().forEach(function (simId) {
      var p = C.pack(simId), sim = S && S.get ? S.get(simId) : null;
      var domain = CKA_DOMAIN[simId] || CLI_DOMAIN_EXTRA[simId] || 'Other';
      p.tasks.forEach(function (tk) {
        tk.steps.forEach(function (st, i) {
          var sid = cliScenarioId(tk.id, i);
          out.push({
            k: key(simId, sid), kind: 'cli', simId: simId, scenarioId: sid, taskId: tk.id, step: i, domain: domain,
            title: sim ? sim.title : simId, label: tk.title + ' · step ' + (i + 1) + '/' + tk.steps.length, glb: sim ? sim.glb : null,
            q: st.label, nudge: st.nudge || null, options: [], answer: null,
            why: 'Solution: $ ' + String(st.hint).split(/\s{2}then\s{2}/).join('  then  $ ')
          });
        });
      });
    });
    return out;
  }

  /**
   * Grade one answer into the schedule. grade: 'again' (wrong / timeout), 'hard' (correct but slow),
   * 'good' (correct). Pure transition, exported for tests.
   */
  function gradeOf(correct, ms) {
    if (!correct) return 'again';
    if (ms != null && ms > SLOW_MS) return 'hard';
    return 'good';
  }
  function nextBox(box, grade, isNew, src) {
    if (grade === 'again') return 0;
    if (grade === 'hard') return Math.max(1, box);
    /* A correct first sighting on a timed exam is evidence, not mastery: start at 1 day. */
    if (isNew) return src === 'exam' ? 2 : 1;
    return Math.min(MAX_BOX, box + 1);
  }

  /**
   * Record one answer. opts: { simId, scenarioId, correct, ms, src: 'exam'|'drill'|'review', timeout, now, domain }
   * Returns { card, grade, from, to, dueIn }.
   */
  function record(opts, dbIn) {
    var db = dbIn || load();
    var t = now0(opts.now);
    var k = key(opts.simId, opts.scenarioId);
    var c = db.cards[k];
    var isNew = !c;
    if (!c) {
      c = db.cards[k] = {
        k: k, simId: opts.simId, scenarioId: opts.scenarioId,
        domain: opts.domain || CKA_DOMAIN[opts.simId] || 'Other',
        box: 0, due: t, reps: 0, lapses: 0, correct: 0, lastMs: null, lastAt: null, src: {}
      };
    }
    var grade = gradeOf(!!opts.correct, opts.ms);
    var from = c.box;
    var wasDue = !isNew && c.due <= t;
    var to = nextBox(c.box, grade, isNew, opts.src);
    c.box = to;
    c.due = t + INTERVALS[to];
    c.reps += 1;
    if (grade === 'again') c.lapses += 1; else c.correct += 1;
    c.lastMs = opts.ms == null ? null : Math.max(0, Math.round(opts.ms));
    c.lastAt = t;
    c.src[opts.src || 'drill'] = (c.src[opts.src || 'drill'] || 0) + 1;
    db.log.push({ at: t, k: k, ok: !!opts.correct, g: grade, ms: c.lastMs, src: opts.src || 'drill', from: isNew ? null : from, to: to, due: wasDue ? 1 : 0, timeout: opts.timeout ? 1 : 0 });
    if (!dbIn) save(db);
    return { card: c, grade: grade, from: isNew ? null : from, to: to, dueIn: INTERVALS[to] };
  }

  /**
   * Coach-driven CLI card. how: 'solution' | 'check-fail' (free-play coach: the learner needed help → 'again'),
   * 'pass' (re-served step verified without `solution` → graded by latency), 'review-solution' (needed it again).
   */
  function recordCli(opts) {
    var pc = { taskId: opts.taskId, step: opts.step };
    if (!pc.taskId || !(pc.step >= 0)) return null;
    var db = load();
    var coachSrc = opts.how === 'solution' || opts.how === 'check-fail';
    var r = record({ simId: opts.simId, scenarioId: cliScenarioId(pc.taskId, pc.step), correct: opts.how === 'pass', ms: opts.ms,
      src: opts.src || (coachSrc ? 'cli-coach' : 'review'), now: opts.now,
      domain: CKA_DOMAIN[opts.simId] || CLI_DOMAIN_EXTRA[opts.simId] || 'Other' }, db);
    r.card.kind = 'cli'; r.card.taskId = pc.taskId; r.card.step = pc.step;
    r.card.why = r.card.why || {};
    if (coachSrc) r.card.why[opts.how] = (r.card.why[opts.how] || 0) + 1;
    db.log[db.log.length - 1].kind = 'cli';
    save(db);
    return r;
  }

  /**
   * Feed a finished ILImmersiveExam paper into the queue. Unanswered items (clock ran out)
   * count as misses — the exam scored them that way too.
   */
  function ingestExam(exam, opts) {
    opts = opts || {};
    var db = load();
    var t = now0(opts.now);
    var out = { queued: 0, lapses: 0, timeouts: 0, correct: 0, keys: [] };
    for (var i = 0; i < (exam && exam.items ? exam.items.length : 0); i++) {
      var it = exam.items[i];
      var timeout = it.choice == null;
      var r = record({ simId: it.simId, scenarioId: it.scenarioId, domain: it.domain, correct: !timeout && !!it.correct, ms: it.ms, src: 'exam', timeout: timeout, now: t }, db);
      out.queued += 1;
      out.keys.push(r.card.k);
      if (r.grade === 'again') out.lapses += 1; else out.correct += 1;
      if (timeout) out.timeouts += 1;
    }
    db.examsIngested = (db.examsIngested || 0) + 1;
    save(db);
    return out;
  }

  function dueCards(db, t) {
    var due = [];
    for (var k in db.cards) if (db.cards[k].due <= t) due.push(db.cards[k]);
    due.sort(function (a, b) { return (a.box - b.box) || (a.due - b.due) || (b.lapses - a.lapses) || (a.k < b.k ? -1 : 1); });
    return due;
  }

  /**
   * Per-domain mastery from this device's cards. Unseen checkpoints count as 0 so a domain
   * you never touched is never reported as strong.
   */
  function mastery(S, opts) {
    opts = opts || {};
    var db = opts.db || load();
    var t = now0(opts.now);
    var cps = checkpoints(S);
    var dom = {};
    for (var i = 0; i < cps.length; i++) {
      var cp = cps[i];
      var d = dom[cp.domain] || (dom[cp.domain] = { domain: cp.domain, checkpoints: 0, seen: 0, due: 0, lapses: 0, reps: 0, correct: 0, boxSum: 0 });
      d.checkpoints += 1;
      var c = db.cards[cp.k];
      if (!c) continue;
      d.seen += 1; d.lapses += c.lapses; d.reps += c.reps; d.correct += c.correct; d.boxSum += c.box;
      if (c.due <= t) d.due += 1;
    }
    var list = Object.keys(dom).map(function (n) {
      var d = dom[n];
      d.pct = d.checkpoints ? Math.round((d.boxSum / (d.checkpoints * MAX_BOX)) * 100) : 0;
      d.accuracy = d.reps ? Math.round((d.correct / d.reps) * 100) : null;
      delete d.boxSum;
      return d;
    });
    list.sort(function (a, b) { return (a.pct - b.pct) || (b.lapses - a.lapses) || (a.domain < b.domain ? -1 : 1); });
    return list;
  }

  /**
   * v1.3.0 (2026-10-21): readiness against the official CNCF CKA blueprint (ILImmersiveExam.BLUEPRINT weights).
   * Per official domain: mastery share = Σ box / (checkpoints × MAX_BOX), unseen checkpoints count 0. Returns
   * ILImmersiveExam.blueprintScore() over every domain (all have checkpoints, so nothing is "untested" — an unseen
   * domain is 0%, never strong), plus seen/checkpoints per row. Null when the exam module is not loaded.
   */
  function blueprint(S, opts) {
    opts = opts || {};
    var E = opts.E || (g && g.ILImmersiveExam);
    if (!E && typeof require === 'function') { try { E = require('./il-immersive-exam.js'); } catch (e) { E = null; } }
    if (!E || !E.blueprintScore) return null;
    var db = opts.db || load();
    var cps = checkpoints(S), sc = {}, seen = {};
    for (var i = 0; i < cps.length; i++) {
      var dom = E.OFFICIAL[cps[i].simId]; if (!dom) continue;
      var d = sc[dom] || (sc[dom] = { correct: 0, total: 0 });
      var c = db.cards[cps[i].k];
      d.total += 1;
      if (c) { d.correct += c.box / MAX_BOX; seen[dom] = (seen[dom] || 0) + 1; }
    }
    var out = E.blueprintScore(sc);
    out.rows.forEach(function (r) { r.seen = seen[r.domain] || 0; r.correct = Math.round(r.correct * 100) / 100; });
    out.evidence = Object.keys(seen).length > 0;
    return out;
  }

  /** Domains to drill first: weakest mastery among domains with any evidence; else []. */
  function weakDomains(S, n, opts) {
    var m = mastery(S, opts).filter(function (d) { return d.seen > 0 && d.pct < 100; });
    return m.slice(0, n || 3).map(function (d) { return d.domain; });
  }

  /** Sim ids for an adaptive exam paper (focus the weakest evidenced domains). */
  function focusSims(S, n, opts) {
    var doms = weakDomains(S, n || 3, opts);
    var out = [];
    for (var i = 0; i < doms.length; i++) for (var id in CKA_DOMAIN) if (CKA_DOMAIN[id] === doms[i] && out.indexOf(id) < 0) out.push(id);
    return out;
  }

  /**
   * Build a review session: due cards first (relearn → young → mature), then — if room and
   * topUp — unseen checkpoints from the weakest evidenced domains. Each item says why it is here.
   */
  function queue(S, opts) {
    opts = opts || {};
    var db = opts.db || load();
    var t = now0(opts.now);
    var limit = Math.max(1, opts.limit || 10);
    var cps = checkpoints(S);
    var byKey = {};
    for (var i = 0; i < cps.length; i++) byKey[cps[i].k] = cps[i];
    /* v1.2.0: coach-driven CLI cards are re-served when the CLI lab is on the page; never used for top-ups. */
    var clis = cliCheckpoints(opts.C, S);
    for (var ci = 0; ci < clis.length; ci++) byKey[clis[ci].k] = clis[ci];
    var items = [];
    var due = dueCards(db, t);
    for (var j = 0; j < due.length && items.length < limit; j++) {
      var c = due[j], cp = byKey[c.k];
      if (!cp) continue; /* checkpoint retired from the sims (or CLI lab not loaded) — skip, never invent */
      var isCli = cp.kind === 'cli';
      items.push(Object.assign({}, cp, {
        reason: c.box === 0 ? 'relearn' : 'due',
        reasonText: c.box === 0
          ? (isCli ? ('Relearn CLI step — Lab Muse had to help ' + c.lapses + '×') : ('Relearn — missed ' + c.lapses + '×' + (c.src.exam ? ' (incl. timed exam)' : '')))
          : ((isCli ? 'CLI step due' : 'Due') + ' · box ' + c.box + ' of ' + MAX_BOX),
        box: c.box, lapses: c.lapses
      }));
    }
    if (opts.topUp !== false && items.length < limit) {
      /* Top-up order per round-robin pass: weakest evidenced domains first, then domains this
       * device has never tested (an untested domain is a gap, never shown as strong). Domains at
       * 100% mastery are not topped up. With no evidence at all, every domain is a cold start. */
      var weak = weakDomains(S, 3, { db: db, now: t });
      var m = mastery(S, { db: db, now: t });
      var untested = m.filter(function (x) { return x.seen === 0; }).map(function (x) { return x.domain; });
      var cold = !weak.length && untested.length === m.length;
      var tiers = weak.map(function (n) { return { domain: n, reason: 'weak-domain' }; })
        .concat(untested.map(function (n) { return { domain: n, reason: cold ? 'cold-start' : 'untested-domain' }; }));
      var LABEL = {
        'weak-domain': 'New · weak domain: ',
        'untested-domain': 'New · untested domain: ',
        'cold-start': 'New · cold start (no on-device evidence yet): '
      };
      var picked = {};
      for (var p = 0; p < items.length; p++) picked[items[p].k] = 1;
      var progress = true;
      while (items.length < limit && progress) {
        progress = false;
        for (var d = 0; d < tiers.length && items.length < limit; d++) {
          for (var q = 0; q < cps.length; q++) {
            var cand = cps[q];
            if (cand.domain !== tiers[d].domain || db.cards[cand.k] || picked[cand.k]) continue;
            picked[cand.k] = 1;
            items.push(Object.assign({}, cand, { reason: tiers[d].reason, reasonText: LABEL[tiers[d].reason] + cand.domain, box: null, lapses: 0 }));
            progress = true;
            break;
          }
        }
      }
    }
    return items;
  }

  function localDay(t) {
    var d = new Date(t);
    return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
  }

  /** Honest on-device analytics: counts derived only from this device's log + cards. */
  /** One spoken sentence block for the lobby (Lab Muse voice). Pure: built from stats/queue/mastery. */
  function speakLine(st, q, mast, bp) {
    st = st || {}; q = q || []; mast = mast || [];
    var plural = function (n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); };
    if (!q.length) return 'Lab Muse: nothing is due on this device. Sit a timed paper or a free-play drill to seed the queue.';
    var c = {}, cli = 0;
    q.forEach(function (x) { c[x.reason] = (c[x.reason] || 0) + 1; if (x.kind === 'cli') cli += 1; });
    var parts = [];
    if (c.relearn) parts.push(c.relearn + ' to relearn from misses');
    if (c.due) parts.push(c.due + ' due for spaced review');
    if (c['weak-domain']) parts.push(c['weak-domain'] + ' new from your weakest domains');
    if (c['untested-domain']) parts.push(c['untested-domain'] + ' new from untested domains');
    if (c['cold-start']) parts.push(c['cold-start'] + ' cold-start');
    var out = 'Lab Muse: ' + plural(st.dueNow || 0, 'checkpoint') + ' due now on this device. Next session is ' +
      plural(q.length, 'card') + ': ' + parts.join(', ') + (cli ? ' (' + plural(cli, 'typed CLI step') + ')' : '') + '.';
    var weak = null;
    for (var i = 0; i < mast.length; i++) if (mast[i].seen > 0) { weak = mast[i]; break; }
    if (weak) out += ' Weakest domain: ' + weak.domain + ', ' + weak.pct + ' percent mastery.';
    if (bp && bp.evidence && bp.weakest) out += ' Biggest gap on the official CKA blueprint: ' + bp.weakest.domain + ', weighted ' + bp.weakest.weight + ' percent of the exam, at ' + bp.weakest.pct + ' percent.';
    return out + ' Start the session to re-serve them on the authored 3D scenes.';
  }

  function stats(opts) {
    opts = opts || {};
    var db = opts.db || load();
    var t = now0(opts.now);
    var byBox = [];
    for (var b = 0; b <= MAX_BOX; b++) byBox.push(0);
    var cards = 0, dueNow = 0, nextDue = null, lapses = 0;
    for (var k in db.cards) {
      var c = db.cards[k];
      cards += 1; byBox[c.box] += 1; lapses += c.lapses;
      if (c.due <= t) dueNow += 1;
      else if (nextDue == null || c.due < nextDue) nextDue = c.due;
    }
    var reviews = 0, dueReviews = 0, dueOk = 0, days = {};
    for (var i = 0; i < db.log.length; i++) {
      var e = db.log[i];
      days[localDay(e.at)] = 1;
      if (e.src !== 'review') continue;
      reviews += 1;
      /* Retention = recall on cards that had graduated (box ≥ 2) and were due — the SR-honest metric. */
      if (e.due && e.from != null && e.from >= 2) { dueReviews += 1; if (e.ok) dueOk += 1; }
    }
    var streak = 0;
    var cursor = new Date(t);
    if (!days[localDay(cursor.getTime())]) cursor.setDate(cursor.getDate() - 1);
    while (days[localDay(cursor.getTime())]) { streak += 1; cursor.setDate(cursor.getDate() - 1); }
    return {
      cards: cards,
      dueNow: dueNow,
      nextDueAt: nextDue,
      learning: byBox[0] + byBox[1],
      mature: byBox.slice(4).reduce(function (a, x) { return a + x; }, 0),
      byBox: byBox,
      lapses: lapses,
      reviews: reviews,
      retentionPct: dueReviews ? Math.round((dueOk / dueReviews) * 100) : null,
      retentionN: dueReviews,
      streakDays: streak,
      examsIngested: db.examsIngested || 0,
      events: db.log.length
    };
  }

  function exportJson(opts) {
    var db = (opts && opts.db) || load();
    return JSON.stringify({ exportedAt: new Date(now0(opts && opts.now)).toISOString(), version: VERSION, honesty: HONESTY, store: db }, null, 2);
  }

  function humanInterval(ms) {
    if (ms <= 0) return 'now';
    if (ms < HOUR) return Math.round(ms / MIN) + ' min';
    if (ms < DAY) return Math.round(ms / HOUR) + ' h';
    var dd = Math.round(ms / DAY);
    return dd + (dd === 1 ? ' day' : ' days');
  }

  /* Optional DOM hook: any page can show the live due count via [data-il-review-due-badge]. */
  function paintBadges() {
    if (typeof document === 'undefined' || !document.querySelectorAll) return;
    var els = document.querySelectorAll('[data-il-review-due-badge]');
    if (!els.length) return;
    var st = stats();
    for (var i = 0; i < els.length; i++) {
      els[i].textContent = st.cards
        ? (st.dueNow + ' due now · ' + st.cards + ' tracked on this device')
        : 'empty — sit a paper or run a drill to seed it';
    }
  }
  if (typeof document !== 'undefined' && document.addEventListener) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', paintBadges);
    else setTimeout(paintBadges, 0);
  }

  function noteSession() { var db = load(); db.sessions = (db.sessions || 0) + 1; save(db); return db.sessions; }

  return {
    VERSION: VERSION,
    STORE_KEY: STORE_KEY,
    INTERVALS: INTERVALS.slice(),
    MAX_BOX: MAX_BOX,
    SLOW_MS: SLOW_MS,
    CKA_DOMAIN: CKA_DOMAIN,
    honesty: HONESTY,
    key: key,
    load: load,
    reset: reset,
    checkpoints: checkpoints,
    cliCheckpoints: cliCheckpoints,
    cliScenarioId: cliScenarioId,
    parseCli: parseCli,
    recordCli: recordCli,
    gradeOf: gradeOf,
    nextBox: nextBox,
    record: record,
    ingestExam: ingestExam,
    mastery: mastery,
    weakDomains: weakDomains,
    blueprint: blueprint,
    focusSims: focusSims,
    queue: queue,
    stats: stats,
    speakLine: speakLine,
    exportJson: exportJson,
    humanInterval: humanInterval,
    noteSession: noteSession,
    paintBadges: paintBadges
  };
});
