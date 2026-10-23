/**
 * IL Immersive Exam v1.0.0 (2026-10-12) — timed CKA mock exam over authored 3D sims.
 *
 * Chains predict-then-reveal checkpoints from the CKA interactive sims under a
 * countdown. Rules engine only — not a live cluster, not killer.sh, not a CNCF exam.
 * Scores + attempt history stay on-device (localStorage il.immersiveExam.v1).
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

  var VERSION = '1.0.0';
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
    'ingress-routing'
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
    'ingress-routing': 'Networking'
  };

  var DEFAULTS = { count: 10, minutes: 15, passPct: 66 };

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
    var picked = [];
    var used = {};
    for (var s = 0; s < simIds.length && picked.length < count; s++) {
      var bucket = bySim[simIds[s]].slice();
      shuffleInPlace(bucket, rnd);
      var first = bucket[0];
      picked.push(first);
      used[first.simId + '::' + first.scenarioId] = 1;
    }
    var rest = all.filter(function (x) { return !used[x.simId + '::' + x.scenarioId]; });
    shuffleInPlace(rest, rnd);
    for (var r = 0; r < rest.length && picked.length < count; r++) picked.push(rest[r]);
    shuffleInPlace(picked, rnd);

    var startedAt = opts.now || Date.now();
    return {
      version: VERSION,
      seed: seed,
      count: picked.length,
      minutes: minutes,
      passPct: opts.passPct != null ? opts.passPct : DEFAULTS.passPct,
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
    DEFAULTS: DEFAULTS,
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
