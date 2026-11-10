/**
 * IL CKS hands-on paper v1.1.0 (2026-11-10; v1.0.0 2026-11-09) — a timed, PERFORMANCE-BASED mock for the CKS, over the six authored CKS
 * glTF scenes (plus the RBAC and NetworkPolicy scenes the CKS blueprint shares with the CKA) and their CLI packs.
 *
 * Would Elon be impressed by a CKS track whose only "exam" is predict-then-reveal multiple choice, when the real CKS is
 * two hours of typed tasks against live clusters? No. So, like the Troubleshooting paper (il-immersive-troubleshoot.js),
 * each item is a task statement only (no step list), the authored 3D scene for that subsystem, and a simulated shell in
 * the task's starting state; the learner does it by typing under one clock. Scoring is partial credit per verified
 * checkpoint, a `hint` halves that checkpoint, `solution` is off until the paper ends. The headline score is weighted
 * by the published CNCF CKS domain weights over the domains the paper actually tested (never pretends an untested
 * domain was passed), the weakest domain is ranked by points at stake (weight × points lost), and missed / hinted
 * checkpoints become CLI review cards (src 'cks-paper') that the review page's CKS queue re-serves.
 *
 * Grading and staging reuse ILTroubleshootExam.gradeIncident / stage (same rules, one implementation).
 *
 * v1.1.0 (2026-11-10) — seeded task VARIANTS. Would Elon be impressed by a "mock exam" that is a replay of the free-play
 * drills, word for word? No — and killer.sh's CKS-A / CKS-B sets are fixed too (the Linux Foundation says the simulator
 * questions are "exactly the same for every attempt and every user (unlike those found on the actual exams)"). So every
 * paper seed now re-draws the task's entity names per task: namespace, user, ServiceAccount, Secret, AppArmor profile,
 * service port, registry host and image tags (VARY × POOLS). The rename is a strict SWAP (canonical ↔ variant, an
 * involution) applied at the terminal boundary: what you type is swapped before the rules engine sees it, and every line
 * the shell prints (output, hints, lab files, the sim panel) is swapped back. So the variant world is self-consistent,
 * and typing a drill-replay name (e.g. `alice` when this paper's user is `carol`) hits a name that does not exist in
 * this paper instead of silently working. Pools are unit-tested to never occur as a word anywhere in the CLI packs or
 * the sims, every task is solvable by typing the variant commands for 40 seeds, and nothing canonical leaks.
 * Honest scope: surface variants (names, port, registry, tags) over the same staged faults — not new fault logic;
 * CIS check ids, kubelet ports (10250/10255) and system paths stay real because they are the same on every cluster;
 * the authored 3D scene node names and the review cards stay canonical (cards re-open the free-play drill).
 *
 * Honest scope: SIMULATED shell over the in-browser rules engine (real CLI syntax, computed output). Not a live
 * cluster, not killer.sh, not the CNCF CKS — Falco, AppArmor, kube-bench, kubesec, KubeLinter, Trivy, cosign and gVisor
 * are rules-engine stand-ins, not real tools, kernels or sandboxes. Scores stay on this device (il.cksPaper.v1).
 */
(function (root, factory) {
  var TS = (typeof module === 'object' && module.exports) ? require('./il-immersive-troubleshoot.js') : (root && root.ILTroubleshootExam);
  var api = factory(TS);
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.ILCksPaper = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function (TS) {
  'use strict';

  var VERSION = '1.1.0';
  var STORE_KEY = 'il.cksPaper.v1';
  var SRC = 'cks-paper';
  var HINT_CREDIT = TS ? TS.HINT_CREDIT : 0.5;
  /* The CKS passing score is 67% (Linux Foundation candidate handbook); this bar mirrors it as a study bar, not a CNCF result. */
  var DEFAULTS = { count: 6, minutes: 36, passPct: 67 };
  var HONESTY = 'Timed hands-on CKS paper in a SIMULATED shell over in-browser 3D drills (rules engine, computed output). Not a live cluster, not killer.sh, not the CNCF CKS. Falco, AppArmor, kube-bench, kubesec, KubeLinter, Trivy, cosign and gVisor are rules-engine stand-ins — a study signal, not a predicted exam score. Names, ports, registry and tags are re-drawn per paper seed (surface variants over the same staged faults).';

  /**
   * The six official CNCF CKS domains (curriculum v1.34 weights, identical to ILImmersiveExam.CKS_BLUEPRINT).
   * sim/anchor = the free-play 3D drill a gap in this domain links to.
   */
  var AREAS = {
    setup: { label: 'Cluster Setup', domain: 'Cluster Setup', weight: 15, sim: 'cks-cluster-hardening', anchor: 'cks-cluster-hardening' },
    hardening: { label: 'Cluster Hardening', domain: 'Cluster Hardening', weight: 15, sim: 'cks-pod-security', anchor: 'cks-pod-security' },
    system: { label: 'System Hardening', domain: 'System Hardening', weight: 10, sim: 'cks-runtime-security', anchor: 'cks-runtime-security' },
    microservice: { label: 'Minimize Microservice Vulnerabilities', domain: 'Minimize Microservice Vulnerabilities', weight: 20, sim: 'cks-sandbox-runtime', anchor: 'cks-sandbox-runtime' },
    supply: { label: 'Supply Chain Security', domain: 'Supply Chain Security', weight: 20, sim: 'cks-supply-chain', anchor: 'cks-supply-chain' },
    runtime: { label: 'Monitoring, Logging & Runtime Security', domain: 'Monitoring, Logging & Runtime Security', weight: 20, sim: 'cks-runtime-security', anchor: 'cks-runtime-security' }
  };
  var AREA_ORDER = ['setup', 'hardening', 'system', 'microservice', 'supply', 'runtime'];
  /** /immersive/ anchor per sim, for "drill the exact scene you lost points on". */
  var ANCHOR = {
    'cks-pod-security': 'cks-pod-security', 'cks-supply-chain': 'cks-supply-chain', 'cks-runtime-security': 'cks-runtime-security',
    'cks-cluster-hardening': 'cks-cluster-hardening', 'cks-static-analysis': 'cks-static-analysis', 'cks-sandbox-runtime': 'cks-sandbox-runtime',
    'rbac-authz': 'cka-rbac', 'netpol-isolation': 'cka-network-policy'
  };

  /**
   * Task bank. ticket = a CKS-style task statement: names, namespaces, files and what must be proven — never the
   * commands. pre = leading steps replayed silently (0 everywhere: every CKS task starts in its own setup state).
   */
  var INCIDENTS = [
    /* Cluster Setup — CIS benchmark, NetworkPolicy. */
    { id: 'cks-bench-kubelet', area: 'setup', simId: 'cks-cluster-hardening', taskId: 'kubelet-auth', pre: 0,
      ticket: 'Host controlplane. kube-bench reports node checks 4.2.1 and 4.2.2 as FAIL. Show the failing checks, prove the kubelet API on 10250 answers an anonymous request, fix /var/lib/kubelet/config.yaml (anonymous auth off, authorization through the API server), make the kubelet pick it up, prove the anonymous request is now refused, and re-run only those two checks.' },
    { id: 'cks-bench-control-plane', area: 'setup', simId: 'cks-cluster-hardening', taskId: 'control-plane', pre: 0,
      ticket: 'Host controlplane. kube-bench reports master checks 1.1.11 (etcd data directory permissions) and 1.2.15 (API server profiling) as FAIL. Show them, restrict /var/lib/etcd to its owner, turn profiling off in the kube-apiserver static-pod manifest, and re-run only those two checks to PASS.' },
    { id: 'cks-bench-readonly', area: 'setup', simId: 'cks-cluster-hardening', taskId: 'readonly-port', pre: 0,
      ticket: 'Host controlplane. The kubelet still serves pod data on its unauthenticated read-only port. Prove it, show how kube-bench classifies check 4.2.4, close the port in the kubelet config, apply it, and prove the port refuses connections.' },
    { id: 'cks-netpol-default-deny', area: 'setup', simId: 'cks-pod-security', taskId: 'default-deny', pre: 0,
      ticket: 'Namespace payments. A pod in namespace default can call payments-api on 8080. Reproduce it, isolate payments with the prepared default-deny ingress policy (default-deny-ingress.yaml), show what else that blocks, then admit only namespace frontend on TCP 8080 (allow-frontend.yaml) and prove the real client works while the attacker still cannot.' },
    { id: 'cks-netpol-lock-api', area: 'setup', simId: 'netpol-isolation', taskId: 'lock-api', pre: 0,
      ticket: 'Namespace backend. No NetworkPolicy selects app=api, so ns untrusted reaches it. Prove it, apply the prepared deny-all policy for api, show the side effect on frontend, then allow ns frontend on 8080 only and prove both outcomes.' },
    /* Cluster Hardening — RBAC, ServiceAccounts. */
    { id: 'cks-rbac-sa-admin', area: 'hardening', simId: 'cks-pod-security', taskId: 'sa-least-privilege', pre: 0,
      ticket: 'ServiceAccount payments:api-sa only needs to read ConfigMaps in payments, but its token can read Secrets cluster-wide. Prove the blast radius, find and delete the binding responsible, grant read on ConfigMaps in payments only (Role config-reader, RoleBinding api-sa-config-reader), and verify both answers.' },
    { id: 'cks-rbac-least', area: 'hardening', simId: 'rbac-authz', taskId: 'least-privilege', pre: 0,
      ticket: 'User alice must list pods in namespace dev and nothing more. Prove she cannot today, bind her to the existing Role pod-reader in dev (RoleBinding alice-pod-reader), and prove the grant stops at the namespace boundary (prod).' },
    { id: 'cks-rbac-revoke', area: 'hardening', simId: 'rbac-authz', taskId: 'revoke', pre: 0,
      ticket: 'User bob can read Secrets in namespace dev and must not. Confirm it, find the binding that grants it, remove it, and prove the API now answers Forbidden.' },
    /* System Hardening — kernel-level confinement. */
    { id: 'cks-apparmor', area: 'system', simId: 'cks-runtime-security', taskId: 'apparmor', pre: 0,
      ticket: 'Host node01. payments-api must not be able to write anywhere on its filesystem using the AppArmor profile k8s-deny-write. Read the profile, roll out payments-api-apparmor.yaml, find why the new pod does not start, fix it on the node, and prove a write inside the pod is denied.' },
    /* Minimize Microservice Vulnerabilities — Pod Security, securityContext, sandboxed runtimes. */
    { id: 'cks-psa-enforce', area: 'microservice', simId: 'cks-pod-security', taskId: 'psa-enforce', pre: 0,
      ticket: 'Namespace payments must enforce the Pod Security Standard "restricted". Show its current labels, preview the change server-side without applying it, enforce it, and prove privileged-debug.yaml is now refused.' },
    { id: 'cks-harden-pod', area: 'microservice', simId: 'cks-pod-security', taskId: 'harden-pod', pre: 0,
      ticket: 'Deployment payments-api in the restricted namespace payments has 0 ready pods. Find the admission reason, roll out payments-api-hardened.yaml, and prove from inside the container that it runs non-root under a seccomp filter.' },
    { id: 'cks-gvisor-runtimeclass', area: 'microservice', simId: 'cks-sandbox-runtime', taskId: 'create-runtimeclass', pre: 0,
      ticket: 'Host node01 has gVisor (handler runsc). Run payments-api sandboxed: check which RuntimeClasses exist, apply payments-api-gvisor.yaml, explain the ReplicaSet\'s failure from events, create RuntimeClass gvisor from runtimeclass-gvisor.yaml, get a new pod rolled now, and prove from inside it which kernel it sees.' },
    { id: 'cks-gvisor-handler', area: 'microservice', simId: 'cks-sandbox-runtime', taskId: 'node-handler', pre: 0,
      ticket: 'Host node01. RuntimeClass gvisor exists and the new payments-api pod is scheduled to node01, but it never starts. Find the kubelet\'s reason, enable the runsc runtime in containerd\'s configuration, apply it, prove the same pod starts, and show gVisor\'s boot messages from inside it.' },
    { id: 'cks-gvisor-overhead', area: 'microservice', simId: 'cks-sandbox-runtime', taskId: 'blast-radius', pre: 0,
      ticket: 'Host node01. Show what the lab kernel-bug PoC (/lab/kernel-bug-poc) does from the runc pod, inspect RuntimeClass gvisor, apply the complete runtimeclass-gvisor.yaml, try the 800m variant (payments-api-gvisor-big.yaml) and explain its state, fall back to payments-api-gvisor.yaml, and re-run the PoC in the sandboxed pod.' },
    /* Supply Chain Security — admission allow-list, scanning, SBOM, signing, static analysis. */
    { id: 'cks-allowed-registries', area: 'supply', simId: 'cks-supply-chain', taskId: 'allowed-registries', pre: 0,
      ticket: 'Namespace payments. payments-api was switched to an unvetted docker.io image. Show which image runs, read and apply allowed-registries.yaml (only registry.example.com/ admitted), roll back to the CI-built digest (payments-api-digest.yaml), and prove payments-api-dockerio.yaml is now denied.' },
    { id: 'cks-trivy-gate', area: 'supply', simId: 'cks-supply-chain', taskId: 'scan-gate', pre: 0,
      ticket: 'Release registry.example.com/payments/api:2.4.1 shipped a CRITICAL CVE because ci/build.sh only prints the Trivy report. Find the CVE, make the scan fail the job on CRITICAL, prove the job now stops before push, move the Dockerfile runtime stage to gcr.io/distroless/static-debian12:nonroot, and release cleanly.' },
    { id: 'cks-sbom', area: 'supply', simId: 'cks-supply-chain', taskId: 'sbom', pre: 0,
      ticket: 'Is registry.example.com/payments/api:2.4.1 affected by the zlib CVE-2023-45853? Answer from a CycloneDX SBOM written to sbom.cdx.json: generate it, query it, scan the SBOM itself, attach it as a signed attestation with cosign.key and verify it with cosign.pub.' },
    { id: 'cks-cosign-verify', area: 'supply', simId: 'cks-supply-chain', taskId: 'sign-verify', pre: 0,
      ticket: 'registry.example.com/payments/api:2.4.1 was pushed from a laptop, skipping CI. Prove it carries no signature for cosign.pub, enforce signature verification at admission (verify-images.yaml), prove an unsigned roll is refused, release through ci/build.sh, verify the new signature and deploy the signed digest.' },
    { id: 'cks-kubesec-gate', area: 'supply', simId: 'cks-static-analysis', taskId: 'kubesec-gate', pre: 0,
      ticket: 'Runner shell. payments-api.yaml requests a privileged container and ci/lint.sh never fails. Score the manifest with kubesec, prove the pipeline ships it anyway, make the scanners fail the job, prove the gate stops it, fix the field, re-score and ship through the gated pipeline.' },
    { id: 'cks-kube-linter', area: 'supply', simId: 'cks-static-analysis', taskId: 'kube-linter', pre: 0,
      ticket: 'Runner shell. Lint payments-api.yaml with KubeLinter (.kube-linter.yaml): someone silenced a check with an ignore annotation, the API secret is a literal env value and the image is :latest. Remove the annotation, fix privileged, move the secret to a secretKeyRef (Secret payments-api, key api-secret), pin payments-api:1.4.2 and lint clean.' },
    { id: 'cks-image-user', area: 'supply', simId: 'cks-static-analysis', taskId: 'image-user', pre: 0,
      ticket: 'Runner shell. payments-api.yaml sets runAsNonRoot: true over payments-api:latest. Apply it, find the stuck pod and the kubelet\'s reason, show what KubeLinter does and does not catch, pin the non-root build payments-api:1.4.2, roll it out and prove both new pods run.' },
    /* Monitoring, Logging & Runtime Security — audit, Falco, immutability. */
    { id: 'cks-audit-log', area: 'runtime', simId: 'cks-pod-security', taskId: 'audit-log', pre: 0,
      ticket: 'Host controlplane. Security needs to know who reads Secret payments/db-creds, but the API server writes no audit log. Find why from the kube-apiserver manifest and the audit policy, enable the log backend, wait for the API server, read the Secret once and find that event in /var/log/kubernetes/audit/audit.log.' },
    { id: 'cks-falco-silent', area: 'runtime', simId: 'cks-runtime-security', taskId: 'falco-detect', pre: 0,
      ticket: 'Host node01. Someone opened a shell in payments-api and Falco stayed silent. Check the Falco pod and its output, find the local rules override responsible, re-enable the rule, and prove the alert now names the namespace, pod and command.' },
    { id: 'cks-falco-contain', area: 'runtime', simId: 'cks-runtime-security', taskId: 'contain', pre: 0,
      ticket: 'Host node01. Falco fired on payments-api. Read the alert, confirm what was dropped in /usr/local/bin, find who opened the shell in the API audit log, replace the pods with payments-api-readonly.yaml and prove the root filesystem is now immutable.' }
  ];
  var BY_ID = {};
  INCIDENTS.forEach(function (x) { BY_ID[x.id] = x; });

  /**
   * v1.1.0 variant pools: canonical token → replacements. Pools are disjoint, never contain a canonical token, and are
   * unit-tested to never occur as a word in il-immersive-cli.js / il-immersive-sims.js (so the swap is a bijection).
   */
  var POOLS = {
    'payments': ['billing', 'ledger', 'invoices', 'treasury', 'remit'],
    'alice': ['carol', 'dana', 'erin'],
    'bob': ['mallory', 'trent', 'victor'],
    'dev': ['staging', 'qa', 'team-blue'],
    'frontend': ['storefront', 'webui', 'portal'],
    'backend': ['platform', 'mid-tier', 'apps-core'],
    'untrusted': ['guest', 'partner', 'outsider'],
    '8080': ['9091', '7070', '8181'],
    'registry.example.com': ['registry.corp.internal', 'cr.acme.internal', 'images.lab.internal'],
    '2.4.1': ['3.1.0', '2.7.3', '3.0.4'],
    '1.4.2': ['2.0.9', '1.6.0', '2.1.3'],
    'api-sa': ['app-sa', 'svc-runner', 'web-sa'],
    'db-creds': ['api-token', 'stripe-key', 'vault-pass'],
    'k8s-deny-write': ['k8s-ro-root', 'k8s-no-write', 'k8s-lockdown']
  };
  /** Which canonical tokens each task re-draws. [] = fixed on purpose (CIS ids, kubelet ports and paths are the same on every cluster). */
  var VARY = {
    'cks-bench-kubelet': [], 'cks-bench-control-plane': [], 'cks-bench-readonly': [],
    'cks-netpol-default-deny': ['payments', 'frontend', '8080'],
    'cks-netpol-lock-api': ['backend', 'frontend', 'untrusted', '8080'],
    'cks-rbac-sa-admin': ['payments', 'api-sa'],
    'cks-rbac-least': ['alice', 'dev'],
    'cks-rbac-revoke': ['bob', 'dev'],
    'cks-apparmor': ['payments', 'k8s-deny-write'],
    'cks-psa-enforce': ['payments'], 'cks-harden-pod': ['payments'],
    'cks-gvisor-runtimeclass': ['payments'], 'cks-gvisor-handler': ['payments'], 'cks-gvisor-overhead': ['payments'],
    'cks-allowed-registries': ['payments', 'registry.example.com'],
    'cks-trivy-gate': ['payments', 'registry.example.com', '2.4.1'],
    'cks-sbom': ['payments', 'registry.example.com', '2.4.1'],
    'cks-cosign-verify': ['payments', 'registry.example.com', '2.4.1'],
    'cks-kubesec-gate': ['payments'], 'cks-kube-linter': ['payments', '1.4.2'], 'cks-image-user': ['payments', '1.4.2'],
    'cks-audit-log': ['payments', 'db-creds'],
    'cks-falco-silent': ['payments'], 'cks-falco-contain': ['payments']
  };

  function reEsc(t) { return String(t).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  /**
   * swapper(pairs) → fn(text): swaps every whole-word occurrence of a or b for the other (pairs = [[canonical, variant], …]).
   * Word = not adjacent to [A-Za-z0-9_], so `payments-api`, `ns/payments`, `payments:api-sa` and `:2.4.1` all swap, while
   * `paymentsX` or `12.4.1` do not. It is an involution: swap(swap(x)) === x.
   */
  function swapper(pairs) {
    var map = {}, toks = [];
    (pairs || []).forEach(function (p) {
      if (!p || !p[0] || !p[1] || p[0] === p[1]) return;
      map[p[0]] = p[1]; map[p[1]] = p[0]; toks.push(p[0], p[1]);
    });
    if (!toks.length) return function (x) { return x; };
    toks.sort(function (a, b) { return b.length - a.length; });
    var re = new RegExp('(^|[^A-Za-z0-9_])(' + toks.map(reEsc).join('|') + ')(?![A-Za-z0-9_])', 'g');
    return function (text) {
      if (text == null) return text;
      return String(text).replace(re, function (m, pre, tok) { return pre + map[tok]; });
    };
  }
  function hashStr(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  /** Deterministic variant for (paper seed, task id): its own PRNG stream, so the task draw is unchanged from v1.0.0. */
  function variantFor(id, seed) {
    var toks = VARY[id] || [];
    var rnd = mulberry32(((seed >>> 0) ^ hashStr(id)) >>> 0);
    var pairs = toks.map(function (t) { var pool = POOLS[t]; return [t, pool[Math.floor(rnd() * pool.length)]]; });
    return { pairs: pairs, label: pairs.map(function (p) { return p[0] + '→' + p[1]; }).join(', ') };
  }

  function mulberry32(a) {
    if (TS && TS.mulberry32) return TS.mulberry32(a);
    return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  }
  function shuffle(arr, rnd) {
    for (var i = arr.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)); var t = arr[i]; arr[i] = arr[j]; arr[j] = t; }
    return arr;
  }

  /** Tasks whose CLI task exists in the loaded packs (C = ILImmersiveCLI); bank order. */
  function bank(C) {
    return INCIDENTS.filter(function (x) {
      if (!C || !C.task) return true;
      var tk = C.task(x.simId, x.taskId);
      return !!tk && x.pre < tk.steps.length;
    });
  }

  /**
   * Build a paper: domains are visited heaviest first (ties shuffled), one task per domain per round, so a 6-task paper
   * touches all six CKS domains and a 3-task paper spends its time on the three 20% domains. opts: count, minutes, seed.
   */
  function buildPaper(C, opts) {
    opts = opts || {};
    var count = Math.max(1, Math.min(opts.count || DEFAULTS.count, 18));
    var minutes = Math.max(1, opts.minutes || DEFAULTS.minutes);
    var seed = opts.seed != null ? (opts.seed >>> 0) : ((Date.now() ^ (Math.random() * 0x100000000)) >>> 0);
    var rnd = mulberry32(seed);
    var all = bank(C);
    if (!all.length) throw new Error('ILCksPaper: no tasks (CLI packs not loaded?)');
    var byArea = {};
    all.forEach(function (x) { (byArea[x.area] || (byArea[x.area] = [])).push(x); });
    var areas = shuffle(Object.keys(byArea).sort(), rnd).sort(function (a, b) { return AREAS[b].weight - AREAS[a].weight; });
    var buckets = areas.map(function (a) { return shuffle(byArea[a].slice(), rnd); });
    var picked = [], more = true;
    while (picked.length < count && more) {
      more = false;
      for (var b = 0; b < buckets.length && picked.length < count; b++) if (buckets[b].length) { picked.push(buckets[b].shift()); more = true; }
    }
    shuffle(picked, rnd); /* the real exam does not group tasks by domain either */
    var startedAt = opts.now != null ? opts.now : Date.now();
    var variants = opts.variants !== false;
    return {
      version: VERSION, kind: 'cks', seed: seed, minutes: minutes,
      passPct: opts.passPct != null ? opts.passPct : DEFAULTS.passPct,
      startedAt: startedAt, endsAt: startedAt + minutes * 60 * 1000,
      variants: variants,
      incidents: picked.map(function (x, i) {
        var tk = C && C.task ? C.task(x.simId, x.taskId) : null;
        var v = variants ? variantFor(x.id, seed) : null, sw = swapper(v ? v.pairs : null);
        return { i: i, id: x.id, area: x.area, areaLabel: AREAS[x.area].label + ' · ' + AREAS[x.area].weight + '%', cka: true, simId: x.simId, taskId: x.taskId,
          pre: x.pre, ticket: sw(x.ticket), title: sw(tk ? tk.title : x.id), steps: tk ? tk.steps.length : null,
          variant: v && v.pairs.length ? v : null, result: null };
      }),
      honesty: HONESTY
    };
  }

  function gradeIncident(inc, status, hinted, extra) {
    if (!TS) throw new Error('ILCksPaper needs ILTroubleshootExam (grading rules)');
    var r = TS.gradeIncident(inc, status, hinted, extra);
    if (inc && inc.variant) {
      /* results screen: show the commands / labels in this paper's names, never the drill's */
      var sw = swapper(inc.variant.pairs);
      r.notes.forEach(function (n) { n.label = sw(n.label); if (n.cmd) n.cmd = sw(n.cmd); });
      r.feedback = sw(r.feedback);
      r.variant = inc.variant.label;
    }
    return r;
  }

  /**
   * Paper summary. Per domain: credit = mean incident credit. Headline pct = blueprint-weighted over the domains this
   * paper tested (renormalised), rawPct = plain mean. Weakest = most CKS points at stake (weight × (1 − pct)); its link
   * goes to the drill of the lowest-scoring task in that domain.
   */
  function summarize(paper) {
    var incs = paper.incidents || [];
    var by = {}, rawSum = 0;
    incs.forEach(function (inc) {
      var r = inc.result || gradeIncident(inc, null, [], { skipped: true });
      var frac = r.total ? r.credit / r.total : 0;
      var a = by[inc.area] || (by[inc.area] = { area: inc.area, label: AREAS[inc.area].label + ' (' + AREAS[inc.area].weight + '%)', domain: AREAS[inc.area].domain,
        weight: AREAS[inc.area].weight, cka: true, incidents: 0, credit: 0, lost: 0, checkpoints: 0, worst: null });
      a.incidents += 1; a.credit += frac; a.checkpoints += r.total; a.lost += r.total - r.credit;
      if (!a.worst || frac < a.worst.frac) a.worst = { frac: frac, simId: inc.simId };
      rawSum += frac;
    });
    var wSum = 0, wPct = 0, weakest = null;
    var areas = AREA_ORDER.filter(function (k) { return by[k]; }).map(function (k) {
      var a = by[k];
      a.pct = Math.round((a.credit / a.incidents) * 100);
      a.lost = Math.round(a.lost * 10) / 10;
      a.atStake = Math.round(a.weight * (100 - a.pct)) / 100;
      a.href = '/immersive/#' + (ANCHOR[a.worst.simId] || AREAS[k].anchor);
      a.drillSim = a.worst.simId;
      delete a.worst;
      wSum += a.weight; wPct += a.weight * a.pct;
      if (a.pct < 100 && (!weakest || a.atStake > weakest.atStake || (a.atStake === weakest.atStake && a.lost > weakest.lost))) weakest = a;
      return a;
    });
    var untested = AREA_ORDER.filter(function (k) { return !by[k]; }).map(function (k) { return AREAS[k].domain; });
    var pct = wSum ? Math.round(wPct / wSum) : 0;
    var passPct = paper.passPct != null ? paper.passPct : DEFAULTS.passPct;
    return {
      incidents: incs.length, ckaIncidents: incs.length, pct: pct, rawPct: incs.length ? Math.round((rawSum / incs.length) * 100) : 0,
      passPct: passPct, passed: incs.length > 0 && pct >= passPct,
      resolved: incs.filter(function (x) { return x.result && x.result.resolved; }).length,
      coveragePct: wSum, untested: untested, areas: areas, weakest: weakest, mesh: null,
      blueprint: { weightedPct: pct, coveragePct: wSum, untested: untested,
        honesty: 'Weights are the published CNCF CKS domain weights (15/15/10/20/20/20), renormalised over the domains this paper tested; scores are typed checkpoints in a simulated shell — a study signal, not a predicted CNCF exam score.' },
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
    list.unshift({ at: Date.now(), seed: paper.seed, incidents: summary.incidents, resolved: summary.resolved, pct: summary.pct, rawPct: summary.rawPct,
      coveragePct: summary.coveragePct, passed: summary.passed, minutes: paper.minutes, variants: paper.variants !== false, weakest: summary.weakest ? summary.weakest.area : null });
    if (list.length > 20) list.length = 20;
    db.last = list[0];
    saveStore(db);
    return db;
  }

  /** Missed / hinted checkpoints become CLI review cards (src 'cks-paper'), one per task (its first gap). */
  function remediate(paper, R) {
    var out = { queued: 0, cards: [] };
    if (!R || !R.recordCli) return out;
    (paper.incidents || []).forEach(function (inc) {
      var r = inc.result; if (!r) return;
      var gap = r.notes[0];
      if (!gap) return;
      try { R.recordCli({ simId: inc.simId, taskId: inc.taskId, step: gap.step, how: 'exam-miss', src: SRC }); out.queued += 1; out.cards.push(inc.taskId + ':' + (gap.step + 1)); }
      catch (e) { /* ignore */ }
    });
    return out;
  }

  function stage(C, S, inc) {
    if (!TS) throw new Error('ILCksPaper needs ILTroubleshootExam (staging rules)');
    return TS.stage(C, S, inc);
  }

  /** Page copy for the shared paper UI (il-immersive-troubleshoot-boot.js reads T.ui when present). */
  var ui = {
    history: function (last) {
      return last
        ? ('Last CKS paper on this device: ' + last.pct + '% (CKS-weighted, ' + (last.coveragePct != null ? last.coveragePct : '?') + '% of the blueprint tested) · ' + last.resolved + '/' + last.incidents + ' tasks done · ' + (last.passed ? 'pass bar cleared' : 'under pass bar') + '.')
        : 'No CKS papers on this device yet.';
    },
    progress: function (i, n) { return 'Task ' + i + '/' + n; },
    nextLabel: function (last) { return last ? 'Submit & finish paper' : 'Submit & next task →'; },
    summary: function (sum, reason) {
      return 'CKS score: ' + sum.pct + '% (weighted by the CNCF CKS domain weights over the ' + sum.coveragePct + '% of the blueprint this paper tested; unweighted ' + sum.rawPct + '%) · '
        + sum.resolved + '/' + sum.incidents + ' tasks done. ' + (sum.passed ? 'Pass bar (' + sum.passPct + '%) cleared.' : 'Under the ' + sum.passPct + '% pass bar.')
        + (reason === 'time' ? ' Time expired — the open task keeps the checkpoints you verified; untouched ones score 0.' : '');
    },
    weakest: function (w) { return 'Weakest CKS domain: ' + w.label + ' — ' + w.pct + '%, ' + w.atStake + ' of its ' + w.weight + ' blueprint points at stake. '; },
    noWeakest: 'No weak domain on this paper — every task was done without hints.',
    blueprint: function (sum) {
      return 'CKS blueprint: ' + sum.coveragePct + '% of the exam weight was tested' + (sum.untested.length ? ' (not on this paper: ' + sum.untested.join(', ') + ')' : ' — all six domains') + '. ' + sum.blueprint.honesty;
    },
    remediate: function (n) { return 'Remediation loop: ' + n + ' checkpoint' + (n > 1 ? 's' : '') + ' you missed or needed a hint for became CLI review cards on this device. '; },
    reviewHref: '/immersive/review/?track=cks',
    reviewLabel: 'Open the CKS review queue →'
  };

  return {
    VERSION: VERSION, STORE_KEY: STORE_KEY, SRC: SRC, HINT_CREDIT: HINT_CREDIT, DEFAULTS: DEFAULTS, HONESTY: HONESTY, honesty: HONESTY,
    AREAS: AREAS, AREA_ORDER: AREA_ORDER, ANCHOR: ANCHOR, INCIDENTS: INCIDENTS, POOLS: POOLS, VARY: VARY, swapper: swapper, variantFor: variantFor, get: function (id) { return BY_ID[id] || null; },
    bank: bank, buildPaper: buildPaper, gradeIncident: gradeIncident, summarize: summarize,
    loadStore: loadStore, recordAttempt: recordAttempt, remediate: remediate, stage: stage, mulberry32: mulberry32, ui: ui
  };
});
