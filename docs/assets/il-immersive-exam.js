/**
 * IL Immersive Exam v1.2.0 (2026-10-21; v1.1.0 2026-10-12; adaptive focus 2026-10-13) — timed CKA mock exam over authored 3D sims.
 *
 * Chains predict-then-reveal checkpoints from the CKA interactive sims under a
 * countdown. Rules engine only — not a live cluster, not killer.sh, not a CNCF exam.
 * Scores + attempt history stay on-device (localStorage il.immersiveExam.v1).
 *
 * v1.2.0 (2026-10-21): + gateway-api drill; official CNCF CKA blueprint — every result is also scored per official
 * domain, weighted by the published exam weights, with the weakest domain chosen by points at stake (weight × miss).
 *
 * Would Elon be impressed by thirteen free-play drills with no exam pressure while
 * KodeKloud ships timed mock exams? No — this is the honest pressure layer on top
 * of the 3D mental model peers still teach as video + terminal.
 */
(function (root, factory) {
  var api = factory(root);
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.ILImmersiveExam = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  var VERSION = '1.2.0';
  var STORE_KEY = 'il.immersiveExam.v1';

  /** CKA-domain sims only. AWS IAM / Multi-AZ and Istio mesh stay on /immersive/ free-play. */
  var CKA_SIMS = [
    'etcd-quorum',
    'control-plane-failure',
    'sched-taints',
    'hpa-scale',
    'storage-csi',
    'config-propagation',
    'rbac-authz',
    'netpol-isolation',
    'cni-network',
    'ingress-routing',
    'gateway-api',
    'node-troubleshoot',
    'service-dns'
  ];

  var DOMAIN = {
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
    'node-troubleshoot': 'Troubleshooting',
    'service-dns': 'Troubleshooting'
  };

  /**
   * v1.2.0 (2026-10-21): the official CNCF CKA blueprint (curriculum domains + exam weights, as published by the Linux
   * Foundation / CNCF for the current CKA). Every CKA drill maps to exactly ONE official domain — the one its predict
   * checkpoints exercise most. The fine-grained DOMAIN labels above stay (on-device review cards are keyed by them).
   */
  var BLUEPRINT = [
    { domain: 'Troubleshooting', weight: 30, sims: ['control-plane-failure', 'node-troubleshoot', 'service-dns'] },
    { domain: 'Cluster Architecture, Installation & Configuration', weight: 25, sims: ['etcd-quorum', 'rbac-authz'] },
    { domain: 'Services & Networking', weight: 20, sims: ['netpol-isolation', 'cni-network', 'ingress-routing', 'gateway-api'] },
    { domain: 'Workloads & Scheduling', weight: 15, sims: ['sched-taints', 'hpa-scale', 'config-propagation'] },
    { domain: 'Storage', weight: 10, sims: ['storage-csi'] }
  ];
  var OFFICIAL = {};
  BLUEPRINT.forEach(function (b) { b.sims.forEach(function (id) { OFFICIAL[id] = b.domain; }); });
  /** Drill anchors on /immersive/ so a weakest-domain callout can send the learner straight to the 3D scene. */
  var ANCHOR = {
    'etcd-quorum': 'cka-etcd', 'control-plane-failure': 'cka-control-plane', 'sched-taints': 'cka-scheduling', 'hpa-scale': 'cka-hpa',
    'storage-csi': 'cka-storage', 'config-propagation': 'cka-secrets-configmaps', 'rbac-authz': 'cka-rbac', 'netpol-isolation': 'cka-network-policy',
    'cni-network': 'cka-cni', 'ingress-routing': 'cka-ingress', 'gateway-api': 'cka-gateway-api', 'node-troubleshoot': 'cka-node-troubleshoot',
    'service-dns': 'cka-service-dns'
  };

  /**
   * Weight per-domain evidence by the official blueprint. scores: { officialDomain: { correct, total } } with
   * total = number of graded items (exam) or checkpoints (mastery) and correct possibly fractional (mastery share).
   * Returns rows in blueprint order, weightedPct over EVIDENCED domains only (renormalised — never pretends an
   * untested domain was passed), coveragePct (blueprint weight that had any evidence), untested domains, and the
   * weakest domain by points at stake = weight × (1 − pct): a 30% domain at 50% outranks a 10% domain at 0%.
   */
  function blueprintScore(scores) {
    scores = scores || {};
    var rows = [], wSum = 0, wPct = 0, cover = 0, untested = [], weakest = null;
    BLUEPRINT.forEach(function (b) {
      var sc = scores[b.domain] || { correct: 0, total: 0 };
      var pct = sc.total ? Math.round((sc.correct / sc.total) * 100) : null;
      var row = { domain: b.domain, weight: b.weight, correct: sc.correct, total: sc.total, pct: pct, sims: b.sims.slice(),
        atStake: pct == null ? null : Math.round(b.weight * (100 - pct)) / 100 };
      rows.push(row);
      if (pct == null) { untested.push(b.domain); return; }
      wSum += b.weight; wPct += b.weight * pct; cover += b.weight;
      if (row.atStake > 0 && (!weakest || row.atStake > weakest.atStake || (row.atStake === weakest.atStake && b.weight > weakest.weight))) weakest = row;
    });
    return {
      rows: rows,
      weightedPct: wSum ? Math.round(wPct / wSum) : null,
      coveragePct: cover,
      untested: untested,
      weakest: weakest,
      drill: weakest ? { sim: weakest.sims[0], href: '/immersive/#' + (ANCHOR[weakest.sims[0]] || '') } : null,
      honesty: 'Weights are the published CNCF CKA domain weights; scores are this device’s answers on in-browser 3D drills — a study signal, not a predicted CNCF exam score.'
    };
  }
  /** Official-blueprint view of one graded paper (unanswered items count as incorrect, like the exam). */
  function examBlueprint(exam) {
    var sc = {};
    (exam.items || []).forEach(function (it) {
      var dom = OFFICIAL[it.simId]; if (!dom) return;
      var d = sc[dom] || (sc[dom] = { correct: 0, total: 0 });
      d.total += 1; if (it.correct) d.correct += 1;
    });
    return blueprintScore(sc);
  }

  var DEFAULTS = { count: 10, minutes: 15, passPct: 66 };
  /** Share of an adaptive paper drawn from weak-domain sims (rest keeps coverage honest). */
  var FOCUS_SHARE = 0.6;

  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      var t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function shuffleInPlace(arr, rnd) {
    var r = rnd || Math.random;
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(r() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  /** Build the full CKA predict pool from an ILImmersiveSims-compatible API. */
  function pool(S) {
    if (!S || !S.get) return [];
    var out = [];
    for (var i = 0; i < CKA_SIMS.length; i++) {
      var id = CKA_SIMS[i];
      var sim = S.get(id);
      if (!sim || !sim.scenarios) continue;
      for (var j = 0; j < sim.scenarios.length; j++) {
        var sc = sim.scenarios[j];
        if (!sc || !sc.predict) continue;
        out.push({
          simId: id,
          scenarioId: sc.id,
          domain: DOMAIN[id] || sim.cert || 'CKA',
          title: sim.title,
          label: sc.label,
          glb: sim.glb,
          q: sc.predict.q,
          options: sc.predict.options.slice(),
          answer: sc.predict.answer,
          why: sc.predict.why
        });
      }
    }
    return out;
  }

  /**
   * Build a timed exam. Prefer one question per CKA sim first, then fill from the
   * remaining pool so a 10-question paper covers every domain when possible.
   * opts.focus (2026-10-13): sim ids from ILImmersiveReview.focusSims. Those sims fill
   * FOCUS_SHARE of the paper (round-robin), then one per other sim, so an adaptive paper
   * over-samples the learner's weakest on-device domains. Empty/absent focus = identical to v1.0.0.
   */
  function buildExam(S, opts) {
    opts = opts || {};
    var count = Math.max(1, Math.min(opts.count || DEFAULTS.count, 45));
    var minutes = Math.max(1, opts.minutes || DEFAULTS.minutes);
    var seed = opts.seed != null ? (opts.seed >>> 0) : ((Date.now() ^ (Math.random() * 0x100000000)) >>> 0);
    var rnd = opts.rnd || mulberry32(seed);
    var all = pool(S);
    if (!all.length) throw new Error('ILImmersiveExam: empty CKA predict pool');

    var bySim = {};
    for (var i = 0; i < all.length; i++) {
      var it = all[i];
      (bySim[it.simId] || (bySim[it.simId] = [])).push(it);
    }
    var simIds = Object.keys(bySim);
    shuffleInPlace(simIds, rnd);
    var focus = {};
    (opts.focus || []).forEach(function (id) { if (bySim[id]) focus[id] = 1; });
    var hasFocus = Object.keys(focus).length > 0;
    var picked = [];
    var used = {};
    function take(x) { picked.push(x); used[x.simId + '::' + x.scenarioId] = 1; }
    if (hasFocus) {
      /* Phase A: FOCUS_SHARE of the paper round-robins the weak-domain sims. */
      var quota = Math.min(count, Math.ceil(count * FOCUS_SHARE));
      var fIds = simIds.filter(function (id) { return focus[id]; });
      var fBuckets = fIds.map(function (id) { return shuffleInPlace(bySim[id].slice(), rnd); });
      var more = true;
      while (picked.length < quota && more) {
        more = false;
        for (var fb = 0; fb < fBuckets.length && picked.length < quota; fb++) {
          if (fBuckets[fb].length) { take(fBuckets[fb].shift()); more = true; }
        }
      }
      simIds = simIds.filter(function (id) { return !focus[id]; });
    }
    /* One per (remaining) sim for domain coverage. */
    for (var s = 0; s < simIds.length && picked.length < count; s++) {
      var bucket = bySim[simIds[s]].slice();
      shuffleInPlace(bucket, rnd);
      take(bucket[0]);
    }
    var rest = all.filter(function (x) { return !used[x.simId + '::' + x.scenarioId]; });
    shuffleInPlace(rest, rnd);
    if (hasFocus) {
      rest = rest.filter(function (x) { return focus[x.simId]; }).concat(rest.filter(function (x) { return !focus[x.simId]; }));
    }
    for (var r = 0; r < rest.length && picked.length < count; r++) picked.push(rest[r]);
    shuffleInPlace(picked, rnd);

    var startedAt = opts.now || Date.now();
    return {
      version: VERSION,
      seed: seed,
      count: picked.length,
      minutes: minutes,
      passPct: opts.passPct != null ? opts.passPct : DEFAULTS.passPct,
      focus: hasFocus ? Object.keys(focus) : [],
      startedAt: startedAt,
      endsAt: startedAt + minutes * 60 * 1000,
      items: picked.map(function (x, idx) {
        return {
          i: idx,
          simId: x.simId,
          scenarioId: x.scenarioId,
          domain: x.domain,
          title: x.title,
          label: x.label,
          glb: x.glb,
          q: x.q,
          options: x.options,
          answer: x.answer,
          why: x.why,
          order: null,
          choice: null,
          correct: null,
          ms: null
        };
      }),
      honesty: 'Timed mock over in-browser 3D sims (rules engine). Not a live cluster, not killer.sh, not the CNCF CKA.'
    };
  }

  function gradeItem(item, choice, ms) {
    var correct = choice === item.answer;
    return {
      choice: choice,
      correct: correct,
      ms: ms == null ? null : Math.max(0, Math.round(ms)),
      why: item.why,
      answer: item.answer
    };
  }

  function summarize(exam) {
    var total = exam.items.length;
    var answered = 0, correct = 0;
    var byDomain = {};
    for (var i = 0; i < exam.items.length; i++) {
      var it = exam.items[i];
      var d = byDomain[it.domain] || (byDomain[it.domain] = { correct: 0, answered: 0, total: 0 });
      d.total += 1;
      if (it.choice != null) {
        answered += 1; d.answered += 1;
        if (it.correct) { correct += 1; d.correct += 1; }
      }
    }
    var pct = total ? Math.round((correct / total) * 100) : 0;
    var passPct = exam.passPct != null ? exam.passPct : DEFAULTS.passPct;
    return {
      total: total,
      answered: answered,
      correct: correct,
      pct: pct,
      passed: pct >= passPct,
      passPct: passPct,
      byDomain: byDomain,
      blueprint: examBlueprint(exam),
      remainingMs: Math.max(0, (exam.endsAt || 0) - Date.now())
    };
  }

  function loadStore() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || '{}') || {}; } catch (e) { return {}; }
  }
  function saveStore(db) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(db)); } catch (e) { /* private mode */ }
  }
  function recordAttempt(exam, summary) {
    var db = loadStore();
    var list = db.attempts || (db.attempts = []);
    list.unshift({
      at: Date.now(),
      seed: exam.seed,
      correct: summary.correct,
      total: summary.total,
      pct: summary.pct,
      passed: summary.passed,
      minutes: exam.minutes
    });
    if (list.length > 20) list.length = 20;
    db.last = list[0];
    saveStore(db);
    return db;
  }

  return {
    VERSION: VERSION,
    STORE_KEY: STORE_KEY,
    CKA_SIMS: CKA_SIMS.slice(),
    DOMAIN: DOMAIN,
    BLUEPRINT: BLUEPRINT,
    OFFICIAL: OFFICIAL,
    ANCHOR: ANCHOR,
    blueprintScore: blueprintScore,
    examBlueprint: examBlueprint,
    DEFAULTS: DEFAULTS,
    FOCUS_SHARE: FOCUS_SHARE,
    pool: pool,
    buildExam: buildExam,
    gradeItem: gradeItem,
    summarize: summarize,
    shuffleInPlace: shuffleInPlace,
    mulberry32: mulberry32,
    loadStore: loadStore,
    recordAttempt: recordAttempt,
    honesty: 'Timed mock over in-browser 3D sims (rules engine). Not a live cluster, not killer.sh, not the CNCF CKA.'
  };
});
