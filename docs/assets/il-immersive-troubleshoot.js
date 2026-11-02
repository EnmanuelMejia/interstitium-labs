/**
 * IL Troubleshooting Exam v1.0.0 (2026-10-28) — a timed, HANDS-ON mixed-incident paper for the CKA Troubleshooting
 * domain (30% of the CKA, its biggest domain), over the authored glTF drills and their CLI packs.
 *
 * Would Elon be impressed by a "troubleshooting" mock that is still multiple choice, when the real CKA is a
 * performance-based exam where you type kubectl / systemctl / crictl against a broken cluster? No. So each incident is
 * a ticket (symptom only — no step list), the authored 3D scene for that subsystem, and a simulated shell that is
 * already broken; the learner diagnoses and fixes it by typing, under one clock across several incidents. Scoring is
 * partial credit per verified checkpoint (like the CKA's per-task partial credit), a `hint` halves that checkpoint, and
 * `solution` is switched off until the paper ends. Results: per-incident feedback (what was verified, the first
 * checkpoint you missed, the exact command and the 3D nodes to look at), per-area scores, the weakest area by
 * checkpoints lost with a link to its free-play drill, and the CKA Troubleshooting domain score via the official
 * blueprint weights (ILImmersiveExam.blueprintScore when present).
 *
 * Incidents reuse the existing CLI tasks (il-immersive-cli.js). Most packs start an incident already broken (setup);
 * the control-plane tasks start healthy, so their first `pre` steps are replayed silently from the pack's own
 * commands before the learner is handed the shell (the ticket then says what the on-call colleague did).
 *
 * Honest scope: SIMULATED shell over the in-browser rules engine (real CLI syntax, computed output). Not a live
 * cluster, not killer.sh, not a CNCF exam, no hosted lab fleet; scores stay on this device (il.troubleshootExam.v1).
 * The service-mesh incidents are Istio semantics — beyond the CKA curriculum — so they are opt-in and scored
 * separately, never folded into the CKA Troubleshooting score.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.ILTroubleshootExam = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  var VERSION = '1.0.0';
  var STORE_KEY = 'il.troubleshootExam.v1';
  var HINT_CREDIT = 0.5;
  var DEFAULTS = { count: 5, minutes: 30, passPct: 66 };
  var HONESTY = 'Timed hands-on paper in a SIMULATED shell over in-browser 3D drills (rules engine, computed output). Not a live cluster, not killer.sh, not the CNCF CKA — a study signal, not a predicted exam score.';

  /** Sub-areas of the official CKA Troubleshooting domain (+ one opt-in, off-blueprint mesh area). */
  var AREAS = {
    components: { label: 'Cluster components (control plane)', cka: true, sim: 'control-plane-failure', anchor: 'cka-control-plane' },
    nodes: { label: 'Nodes & kubelet', cka: true, sim: 'node-troubleshoot', anchor: 'cka-node-troubleshoot' },
    services: { label: 'Services & DNS', cka: true, sim: 'service-dns', anchor: 'cka-service-dns' },
    network: { label: 'Cluster networking (CNI · kube-proxy)', cka: true, sim: 'cni-network', anchor: 'cka-cni' },
    mesh: { label: 'Service mesh mTLS (Istio · beyond CKA)', cka: false, sim: 'mesh-mtls', anchor: 'cka-service-mesh' }
  };
  var AREA_ORDER = ['components', 'nodes', 'services', 'network', 'mesh'];

  /**
   * The incident bank. ticket = what an on-call page would say (symptom + context needed to act), never the steps.
   * pre = number of the task's leading steps replayed (silently) before hand-over.
   */
  var INCIDENTS = [
    { id: 'cp-api-down', area: 'components', simId: 'control-plane-failure', taskId: 'api-blind', pre: 1,
      ticket: 'kubectl on controlplane cannot reach the API server. During maintenance a colleague moved the kube-apiserver static-pod manifest to /tmp/. Confirm kubectl is blind, prove what is (not) running with the container runtime, and bring the API server back.' },
    { id: 'cp-pending', area: 'components', simId: 'control-plane-failure', taskId: 'pending-scale', pre: 2,
      ticket: 'web was scaled to 5 replicas during control-plane maintenance and two new pods never started. The kube-scheduler static-pod manifest was parked in /tmp/. Find the stuck pods, restore the scheduler, and confirm every web pod is Running.' },
    { id: 'cp-worker-notready', area: 'components', simId: 'control-plane-failure', taskId: 'notready', pre: 1,
      ticket: 'An alert says worker-2 stopped reporting after someone stopped a service on it. Confirm the node status from the API, then bring worker-2 back and confirm all nodes are Ready.' },
    { id: 'node-kubelet-203', area: 'nodes', simId: 'node-troubleshoot', taskId: 'kubelet-203', pre: 0,
      ticket: 'node-01 went NotReady after an in-place upgrade and stays that way. Find out why its kubelet will not stay up, fix it on the node, and get node-01 Ready.' },
    { id: 'node-runtime', area: 'nodes', simId: 'node-troubleshoot', taskId: 'runtime-down', pre: 0,
      ticket: 'node-01 is NotReady and nothing new starts on it. Find the failing component on the node, fix it so it survives a reboot, and confirm Ready.' },
    { id: 'node-cni', area: 'nodes', simId: 'node-troubleshoot', taskId: 'cni-missing', pre: 0,
      ticket: 'node-01 is NotReady and new pods will not land there; the other nodes are fine. Trace the cause on the node and fix it without hand-writing CNI config.' },
    { id: 'node-disk', area: 'nodes', simId: 'node-troubleshoot', taskId: 'disk-pressure', pre: 0,
      ticket: 'Pods on node-01 are being evicted and rescheduled elsewhere. Find the node condition behind it, reclaim what is needed on the node, and confirm the condition clears.' },
    { id: 'svc-target-port', area: 'services', simId: 'service-dns', taskId: 'target-port', pre: 0,
      ticket: 'In ns shop, web cannot reach Service api, yet both api pods are Running and Ready. Find the break between the Service and the pods, fix it, and get a 200 from web.' },
    { id: 'dns-coredns', area: 'services', simId: 'service-dns', taskId: 'coredns-corefile', pre: 0,
      ticket: 'Name resolution fails in every namespace after a ConfigMap change in kube-system. Find out why cluster DNS is down, fix it declaratively, and resolve api from ns shop again.' },
    { id: 'dns-egress', area: 'services', simId: 'service-dns', taskId: 'dns-egress', pre: 0,
      ticket: 'Pods in ns shop cannot resolve any name; other namespaces can. Show whether the network path itself works, find what blocks DNS for shop only, and fix it.' },
    { id: 'dns-cross-ns', area: 'services', simId: 'service-dns', taskId: 'cross-ns-fqdn', pre: 0,
      ticket: 'web in ns shop logs “no such host” for its database, but cluster DNS is healthy. Find what web actually asks for, where the database Service lives, and fix web’s configuration.' },
    { id: 'net-no-cni', area: 'network', simId: 'cni-network', taskId: 'no-cni', pre: 0,
      ticket: 'kubeadm init and join finished on a fresh cluster, but every node is NotReady and CoreDNS will not start. Find the missing piece, install it, and get nodes and CoreDNS healthy.' },
    { id: 'net-cidr-overlap', area: 'network', simId: 'cni-network', taskId: 'cidr-overlap', pre: 0,
      ticket: 'Pods on the same node reach each other, but nothing crosses to node-1. Find why pod addressing breaks cross-node traffic and migrate the pods the way the CNI documents it.' },
    { id: 'net-no-kube-proxy', area: 'network', simId: 'cni-network', taskId: 'no-kube-proxy', pre: 0,
      ticket: 'The client cannot reach Service web by name or ClusterIP, yet the web pods answer on their own IPs. Find which component should program Services on the nodes and restore it.' },
    { id: 'mesh-strict-reset', area: 'mesh', simId: 'mesh-mtls', taskId: 'strict-reset', pre: 0,
      ticket: 'frontend (ns shop) → payments (ns payments) fails with “connection reset by peer”. payments requires mTLS. Find why frontend cannot speak it and fix it the way sidecar injection really works.' },
    { id: 'mesh-istiod-down', area: 'mesh', simId: 'mesh-mtls', taskId: 'istiod-down', pre: 0,
      ticket: 'Meshed traffic is fine, but redeploying frontend creates no new pods. Find what is blocking pod creation and restore the mesh control plane.' }
  ];
  var BY_ID = {};
  INCIDENTS.forEach(function (x) { BY_ID[x.id] = x; });

  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      var t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function shuffle(arr, rnd) {
    for (var i = arr.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)); var t = arr[i]; arr[i] = arr[j]; arr[j] = t; }
    return arr;
  }

  /** Incidents whose CLI task exists in the loaded pack (C = ILImmersiveCLI); bank order. */
  function bank(C, opts) {
    opts = opts || {};
    return INCIDENTS.filter(function (x) {
      if (!opts.mesh && !AREAS[x.area].cka) return false;
      if (!C || !C.task) return true;
      var tk = C.task(x.simId, x.taskId);
      return !!tk && x.pre < tk.steps.length;
    });
  }

  /**
   * Build a paper: round-robin across areas (shuffled) so a 4+ incident paper touches every CKA area, then fill.
   * opts: count, minutes, seed, mesh (bool: add ONE mesh incident on top, scored separately), now, passPct.
   */
  function buildPaper(C, opts) {
    opts = opts || {};
    var count = Math.max(1, Math.min(opts.count || DEFAULTS.count, 12));
    var minutes = Math.max(1, opts.minutes || DEFAULTS.minutes);
    var seed = opts.seed != null ? (opts.seed >>> 0) : ((Date.now() ^ (Math.random() * 0x100000000)) >>> 0);
    var rnd = mulberry32(seed);
    var ckaBank = bank(C, {});
    if (!ckaBank.length) throw new Error('ILTroubleshootExam: no incidents (CLI packs not loaded?)');
    var byArea = {};
    ckaBank.forEach(function (x) { (byArea[x.area] || (byArea[x.area] = [])).push(x); });
    var areas = shuffle(Object.keys(byArea).sort(), rnd);
    var buckets = areas.map(function (a) { return shuffle(byArea[a].slice(), rnd); });
    var picked = [];
    var more = true;
    while (picked.length < count && more) {
      more = false;
      for (var b = 0; b < buckets.length && picked.length < count; b++) if (buckets[b].length) { picked.push(buckets[b].shift()); more = true; }
    }
    if (opts.mesh) {
      var meshBank = bank(C, { mesh: true }).filter(function (x) { return !AREAS[x.area].cka; });
      if (meshBank.length) picked.push(shuffle(meshBank.slice(), rnd)[0]);
    }
    var startedAt = opts.now || Date.now();
    return {
      version: VERSION,
      kind: 'troubleshoot',
      seed: seed,
      minutes: minutes,
      passPct: opts.passPct != null ? opts.passPct : DEFAULTS.passPct,
      startedAt: startedAt,
      endsAt: startedAt + minutes * 60 * 1000,
      incidents: picked.map(function (x, i) {
        var tk = C && C.task ? C.task(x.simId, x.taskId) : null;
        return { i: i, id: x.id, area: x.area, areaLabel: AREAS[x.area].label, cka: AREAS[x.area].cka, simId: x.simId, taskId: x.taskId,
          pre: x.pre, ticket: x.ticket, title: tk ? tk.title : x.id, steps: tk ? tk.steps.length : null,
          result: null };
      }),
      honesty: HONESTY
    };
  }

  /**
   * Grade one incident from ILImmersiveCLI.taskStatus output. hinted = step indices where `hint` was used.
   * Learner checkpoints are steps pre..n-1. Credit: 1 per verified checkpoint, HINT_CREDIT if hinted. Steps are
   * verified in order, so the first unverified learner step is where the incident stalled.
   */
  function gradeIncident(inc, status, hinted, extra) {
    extra = extra || {};
    var h = {};
    (hinted || []).forEach(function (i) { h[i] = 1; });
    var steps = (status && status.steps) || [];
    var pre = inc.pre || 0;
    /* No status (never staged / clock ran out first): every learner checkpoint counts as missed. */
    var learner = steps.length ? Math.max(0, steps.length - pre) : Math.max(0, (inc.steps || 0) - pre);
    var credit = 0, verified = 0, firstMiss = null, notes = [];
    for (var i = pre; i < steps.length; i++) {
      var st = steps[i];
      if (st.done) {
        verified += 1;
        credit += h[i] ? HINT_CREDIT : 1;
        if (h[i]) notes.push({ step: i, n: i - pre + 1, how: 'hinted', label: st.label, cmd: st.hint || null, focus: st.focus || null });
      } else {
        if (firstMiss == null) firstMiss = i;
        notes.push({ step: i, n: i - pre + 1, how: h[i] ? 'hinted-missed' : 'missed', label: st.label, cmd: st.hint || null, focus: st.focus || null });
      }
    }
    var pct = learner ? Math.round((credit / learner) * 100) : 0;
    var r = { id: inc.id, area: inc.area, cka: !!inc.cka, total: learner, verified: verified, credit: credit, pct: pct,
      resolved: learner > 0 && verified === learner, hints: Object.keys(h).length, firstMiss: firstMiss, notes: notes,
      cmds: extra.cmds == null ? null : extra.cmds, ms: extra.ms == null ? null : Math.max(0, Math.round(extra.ms)), skipped: !!extra.skipped };
    r.feedback = feedbackLine(inc, r);
    return r;
  }

  function feedbackLine(inc, r) {
    if (!r.total) return 'No checkpoints to grade.';
    if (r.resolved && !r.hints) return 'Resolved: all ' + r.total + ' checkpoints verified without help.';
    if (r.resolved) return 'Resolved with ' + r.hints + ' hint' + (r.hints > 1 ? 's' : '') + ' (' + r.pct + '% credit).';
    var miss = r.notes.filter(function (n) { return n.how !== 'hinted'; })[0];
    return (r.verified ? 'Stalled after ' + r.verified + '/' + r.total + ' checkpoints. ' : (r.skipped ? 'Skipped — 0/' + r.total + ' checkpoints. ' : 'Not started. '))
      + (miss ? 'Next checkpoint: ' + miss.label + '.' : '');
  }

  /** Paper summary: overall %, pass bar, per-area table, weakest CKA area, CKA Troubleshooting blueprint view. */
  function summarize(paper, E) {
    var incs = paper.incidents || [];
    var byArea = {}, ckaCredit = 0, ckaN = 0, all = 0, allN = 0, mesh = null;
    incs.forEach(function (inc) {
      var r = inc.result || gradeIncident(inc, null, [], { skipped: true });
      var frac = r.total ? r.credit / r.total : 0;
      var a = byArea[inc.area] || (byArea[inc.area] = { area: inc.area, label: AREAS[inc.area].label, cka: AREAS[inc.area].cka, incidents: 0, credit: 0, lost: 0, checkpoints: 0 });
      a.incidents += 1; a.credit += frac; a.checkpoints += r.total; a.lost += r.total - r.credit;
      if (inc.cka) { ckaCredit += frac; ckaN += 1; }
      else mesh = { pct: Math.round(frac * 100), resolved: r.resolved };
      all += frac; allN += 1;
    });
    var areas = AREA_ORDER.filter(function (k) { return byArea[k]; }).map(function (k) {
      var a = byArea[k]; a.pct = Math.round((a.credit / a.incidents) * 100); a.lost = Math.round(a.lost * 10) / 10;
      a.href = '/immersive/#' + AREAS[k].anchor; return a;
    });
    var weakest = null;
    areas.forEach(function (a) {
      if (!a.cka || a.pct >= 100) return;
      if (!weakest || a.pct < weakest.pct || (a.pct === weakest.pct && a.lost > weakest.lost)) weakest = a;
    });
    var pct = ckaN ? Math.round((ckaCredit / ckaN) * 100) : 0;
    var passPct = paper.passPct != null ? paper.passPct : DEFAULTS.passPct;
    var bp = null;
    if (E && E.blueprintScore && ckaN) {
      var full = E.blueprintScore({ Troubleshooting: { correct: ckaCredit, total: ckaN } });
      var row = full.rows.filter(function (x) { return x.domain === 'Troubleshooting'; })[0];
      bp = { domain: 'Troubleshooting', weight: row.weight, pct: row.pct, atStake: row.atStake, honesty: full.honesty };
    }
    return {
      incidents: incs.length, ckaIncidents: ckaN, pct: pct, passPct: passPct, passed: ckaN > 0 && pct >= passPct,
      resolved: incs.filter(function (x) { return x.result && x.result.resolved; }).length,
      overallPct: allN ? Math.round((all / allN) * 100) : 0, mesh: mesh, areas: areas, weakest: weakest, blueprint: bp,
      honesty: HONESTY
    };
  }

  function loadStore() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || '{}') || {}; } catch (e) { return {}; }
  }
  function saveStore(db) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(db)); } catch (e) { /* private mode */ }
  }
  function recordAttempt(paper, summary) {
    var db = loadStore();
    var list = db.attempts || (db.attempts = []);
    list.unshift({ at: Date.now(), seed: paper.seed, incidents: summary.incidents, resolved: summary.resolved, pct: summary.pct,
      passed: summary.passed, minutes: paper.minutes, weakest: summary.weakest ? summary.weakest.area : null });
    if (list.length > 20) list.length = 20;
    db.last = list[0];
    saveStore(db);
    return db;
  }

  /** Missed / hinted checkpoints become CLI review cards (ILImmersiveReview.recordCli), one per incident (first gap). */
  function remediate(paper, R) {
    var out = { queued: 0, cards: [] };
    if (!R || !R.recordCli) return out;
    (paper.incidents || []).forEach(function (inc) {
      var r = inc.result; if (!r) return;
      var gap = r.notes[0];
      if (!gap) return;
      try { R.recordCli({ simId: inc.simId, taskId: inc.taskId, step: gap.step, how: 'exam-miss', src: 'troubleshoot-exam' }); out.queued += 1; out.cards.push(inc.taskId + ':' + (gap.step + 1)); }
      catch (e) { /* ignore */ }
    });
    return out;
  }

  /**
   * Headless helper (tests, previews): start an incident like the player does — task setup state, then replay the
   * `pre` steps from the pack's own commands. Returns { state, ctx } ready for the learner.
   */
  function stage(C, S, inc) {
    var sim = S.get(inc.simId), tk = C.task(inc.simId, inc.taskId);
    var state = S.merge(sim.initial, tk.setup || {});
    var ctx = C.newCtx(inc.taskId);
    for (var i = 0; i < (inc.pre || 0); i++) {
      String(tk.steps[i].hint).split(/\s{2}then\s{2}/).forEach(function (cmd) {
        var r = C.run(inc.simId, state, cmd, ctx);
        if (r.set) state = S.merge(state, r.set);
        C.reconcile(inc.simId, state, ctx);
      });
    }
    ctx.history = [];
    return { state: state, ctx: ctx };
  }

  return {
    VERSION: VERSION, STORE_KEY: STORE_KEY, HINT_CREDIT: HINT_CREDIT, DEFAULTS: DEFAULTS, HONESTY: HONESTY, honesty: HONESTY,
    AREAS: AREAS, AREA_ORDER: AREA_ORDER, INCIDENTS: INCIDENTS, get: function (id) { return BY_ID[id] || null; },
    bank: bank, buildPaper: buildPaper, gradeIncident: gradeIncident, summarize: summarize,
    loadStore: loadStore, recordAttempt: recordAttempt, remediate: remediate, stage: stage, mulberry32: mulberry32
  };
});
