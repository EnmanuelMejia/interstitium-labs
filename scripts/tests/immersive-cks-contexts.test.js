/**
 * 2026-11-13 Musk-bar pass: kubeconfig CONTEXTS on the hands-on CKS paper.
 * il-immersive-cli.js v1.14.0 (kubeContext: a pure gate in front of run()), il-immersive-cks-paper.js v1.3.0 (a seeded
 * context per scene + a decoy, carried from task to task) and il-immersive-3d.js v1.15.0 (cliExam.kube; the authored WebGL
 * scene renders dimmed while kubectl points at another context). Pure: the same files the browser runs.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import test from 'node:test';

const require = createRequire(import.meta.url);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const S = require(path.join(root, 'docs/assets/il-immersive-sims.js'));
globalThis.ILImmersiveSims = S;
const C = require(path.join(root, 'docs/assets/il-immersive-cli.js'));
require(path.join(root, 'docs/assets/il-immersive-troubleshoot.js'));
const K = require(path.join(root, 'docs/assets/il-immersive-cks-paper.js'));

const KC = () => ({
  contexts: [
    { name: 'gate-east', cluster: 'gate-east', user: 'gate-east-admin' },
    { name: 'sec-alpha', cluster: 'sec-alpha', user: 'sec-alpha-admin' }
  ],
  current: 'gate-east', target: 'sec-alpha'
});
const split = (h) => String(h).split(/\s{2}then\s{2}/);
const esc = (t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const word = (t) => new RegExp('(^|[^A-Za-z0-9_])' + esc(t) + '(?![A-Za-z0-9_])');
const isKubectl = (line) => { const t = C.tokenize(line); const h = t[0] === 'sudo' ? t[1] : t[0]; return h === 'kubectl' || h === 'k'; };

/** A paper terminal like the stage's: learner line → swap → kubeconfig gate → rules engine; every printed line → swap. */
function terminal(inc, pairs, kube) {
  const sw = K.swapper(pairs);
  let { state, ctx } = K.stage(C, S, { ...inc, cka: true });
  const rec = { wrong: 0, firstOk: null };
  return {
    kube,
    rec,
    type(line) {
      const g = C.kubeContext(sw(line), kube, !!(ctx.vars && ctx.vars.host));
      if (g.kind === 'config') { kube.current = g.current; return { out: g.out.map(sw), exit: g.exit }; }
      if (g.kind === 'wrong') { rec.wrong += 1; if (rec.firstOk === null) rec.firstOk = false; return { out: g.out.map(sw), exit: g.exit }; }
      if (g.kubectl && rec.firstOk === null) rec.firstOk = true;
      const r = C.run(inc.simId, state, g.line, ctx);
      if (r.set) state = S.merge(state, r.set);
      C.reconcile(inc.simId, state, ctx);
      return { out: r.out.map(sw), exit: r.exit };
    },
    status() { return C.taskStatus(inc.simId, inc.taskId, state, ctx); }
  };
}

test('CLI v1.14.0 kubeContext: kubectl config get-contexts / current-context / use-context / view answer from the paper kubeconfig', () => {
  assert.equal(C.VERSION, '1.14.0');
  assert.equal(typeof C.kubeContext, 'function');
  const kc = KC();
  const g = C.kubeContext('kubectl config get-contexts', kc);
  assert.equal(g.kind, 'config');
  assert.match(g.out[0], /^CURRENT\s+NAME\s+CLUSTER\s+AUTHINFO\s+NAMESPACE$/);
  assert.match(g.out[1], /^\*\s+gate-east\s+gate-east\s+gate-east-admin$/, 'current context starred');
  assert.match(g.out[2], /^\s+sec-alpha\s+sec-alpha\s+sec-alpha-admin$/);
  assert.deepEqual(C.kubeContext('k config get-contexts -o name', kc).out, ['gate-east', 'sec-alpha']);
  assert.deepEqual(C.kubeContext('kubectl config current-context', kc).out, ['gate-east']);
  const sw = C.kubeContext('kubectl config use-context sec-alpha', kc);
  assert.deepEqual(sw.out, ['Switched to context "sec-alpha".']);
  assert.equal(sw.current, 'sec-alpha');
  assert.equal(kc.current, 'gate-east', 'pure: the caller applies `current`');
  const bad = C.kubeContext('kubectl config use-context sec-alfa', kc);
  assert.equal(bad.exit, 1);
  assert.deepEqual(bad.out, ['error: no context exists with the name: "sec-alfa"']);
  assert.equal(bad.current, 'gate-east');
  const view = C.kubeContext('kubectl config view', kc).out.join('\n');
  assert.match(view, /current-context: gate-east/);
  assert.match(view, /name: sec-alpha/);
  assert.doesNotMatch(view, /server:|token|client-key/, 'no invented server addresses or credentials');
  const ns = C.kubeContext('kubectl config set-context --current --namespace=payments', kc);
  assert.equal(ns.exit, 2);
  assert.match(ns.out[0], /not modelled/);
});

test('CLI v1.14.0 kubeContext: kubectl on another context reaches an empty stand-in cluster; --context picks one per command; non-kubectl lines pass', () => {
  const kc = KC();
  const w = (line) => C.kubeContext(line, kc);
  assert.deepEqual(w('kubectl get pods -n payments'), { kind: 'wrong', out: ['No resources found in payments namespace.'], exit: 0, context: 'gate-east' });
  assert.deepEqual(w('kubectl get pods -A').out, ['No resources found']);
  const nodes = w('k get nodes');
  assert.equal(nodes.kind, 'wrong');
  assert.match(nodes.out[1], /^gate-east-cp1\s+Ready\s+control-plane/, 'the other cluster shows its own nodes');
  assert.deepEqual(w('kubectl describe deploy payments-api -n payments').out, ['Error from server (NotFound): namespaces "payments" not found']);
  assert.deepEqual(w('kubectl get deploy web').out, ['Error from server (NotFound): deployments.apps "web" not found']);
  assert.deepEqual(w('kubectl apply -f allowed-registries.yaml').out, ['Error from server (NotFound): the server could not find the requested resource']);
  assert.equal(w('kubectl apply -f allowed-registries.yaml').exit, 1);
  assert.deepEqual(w('kubectl auth can-i list secrets --as alice -n dev').out, ['no']);
  /* --context NAME for one command */
  assert.deepEqual(w('kubectl --context sec-alpha get pods -n payments'), { kind: 'pass', line: 'kubectl get pods -n payments', kubectl: true });
  assert.deepEqual(w('kubectl get pods --context=sec-alpha -n payments'), { kind: 'pass', line: 'kubectl get pods -n payments', kubectl: true });
  assert.equal(w('kubectl --context gate-east get pods').kind, 'wrong');
  assert.deepEqual(w('kubectl --context nope get pods').out, ['error: context "nope" does not exist']);
  /* on target: pass untouched */
  const on = { ...KC(), current: 'sec-alpha' };
  assert.deepEqual(C.kubeContext('sudo kubectl get pods -n payments', on), { kind: 'pass', line: 'sudo kubectl get pods -n payments', kubectl: true });
  /* only kubectl is context-bound */
  for (const line of ['kube-bench run --targets node', 'ssh node01', 'ssh node01 kubectl get pods', 'sed -i "s/a/b/" /var/lib/kubelet/config.yaml', 'trivy image x', 'cat payments-api.yaml', 'check', 'hint'])
    assert.deepEqual(w(line), { kind: 'pass', line }, line);
  assert.deepEqual(C.kubeContext('kubectl get pods', kc, true), { kind: 'pass', line: 'kubectl get pods' }, 'inside an ssh session kubectl is the node\'s business');
  assert.deepEqual(C.kubeContext('kubectl get pods', null), { kind: 'pass', line: 'kubectl get pods' }, 'no kubeconfig → no gate (free play, CKA paper)');
});

test('paper v1.3.0 contexts: one seeded context per scene + a decoy no task uses; task, name and fault draws unchanged; ?contexts=0 off', () => {
  assert.equal(K.VERSION, '1.3.0');
  assert.equal(K.CONTEXT_POOL.length, 10);
  assert.equal(new Set(K.CONTEXT_POOL).size, 10);
  for (let seed = 1; seed <= 60; seed++) {
    for (const count of [3, 6, 12]) {
      const p = K.buildPaper(C, { seed, count, now: 0 });
      const off = K.buildPaper(C, { seed, count, now: 0, contexts: false });
      assert.deepEqual(p.incidents.map((i) => [i.id, i.taskId, i.ticket, i.variant && i.variant.label, i.fault && i.fault.id]),
        off.incidents.map((i) => [i.id, i.taskId, i.ticket, i.variant && i.variant.label, i.fault && i.fault.id]), 'contexts do not move the other draws');
      assert.equal(off.contexts, null);
      assert.equal(off.startContext, null);
      assert.ok(off.incidents.every((i) => i.context === null));
      const names = p.contexts.map((c) => c.name);
      assert.deepEqual(names, names.slice().sort(), 'sorted like get-contexts');
      assert.ok(names.every((n) => K.CONTEXT_POOL.includes(n)));
      const sims = [...new Set(p.incidents.map((i) => i.simId))];
      assert.equal(p.contexts.length, sims.length + 1, 'one per scene + one decoy');
      for (const inc of p.incidents) {
        assert.ok(names.includes(inc.context));
        assert.equal(inc.context, p.incidents.find((x) => x.simId === inc.simId).context, 'same scene, same cluster');
        assert.notEqual(inc.context, p.startContext, 'the decoy is no task\'s context');
      }
      assert.equal(new Set(p.incidents.map((i) => i.context)).size, sims.length, 'different scenes, different clusters');
      assert.ok(names.includes(p.startContext));
      assert.deepEqual(K.buildPaper(C, { seed, count, now: 0 }).contexts, p.contexts, 'deterministic per seed');
    }
  }
  const draws = new Set();
  for (let seed = 1; seed <= 30; seed++) draws.add(K.buildPaper(C, { seed, count: 6, now: 0 }).startContext);
  assert.ok(draws.size >= 4, 'the decoy varies by seed');
});

test('context names survive every variant swap unchanged and never occur as a word in the CLI packs or sims', () => {
  const cli = readFileSync(path.join(root, 'docs/assets/il-immersive-cli.js'), 'utf8');
  const sims = readFileSync(path.join(root, 'docs/assets/il-immersive-sims.js'), 'utf8');
  const pairs = [];
  for (const [c, pool] of Object.entries(K.POOLS)) for (const v of pool) pairs.push([c, v]);
  const sw = K.swapper(pairs);
  for (const n of K.CONTEXT_POOL) {
    assert.match(n, /^[a-z0-9][a-z0-9.-]{0,40}$/, 'player accepts the name');
    assert.equal(sw(n), n, n + ' is untouched by the variant swap');
    assert.equal(sw('kubectl config use-context ' + n), 'kubectl config use-context ' + n);
    assert.equal(word(n).test(cli), false, n + ' occurs in the CLI');
    assert.equal(word(n).test(sims), false, n + ' occurs in the sims');
    for (const p of pairs) assert.equal(word(p[1]).test(n) || word(p[0]).test(n), false, n + ' contains pool token ' + p.join('/'));
  }
});

test('every bank task (every fault): the solution typed on the wrong context verifies only its kubectl-free steps; after use-context it resolves', () => {
  let kubectlTasks = 0, kubectlFree = [];
  for (let seed = 1; seed <= 12; seed++) {
    const p = K.buildPaper(C, { seed, count: 18, now: 0 });
    for (const inc of p.incidents) {
      const tk = C.task(inc.simId, inc.taskId);
      const pairs = inc.variant ? inc.variant.pairs : [];
      const sw = K.swapper(pairs);
      const cmds = tk.steps.flatMap((s) => split(s.hint)).map(sw);
      const anyKubectl = cmds.some(isKubectl);
      /* 1. wrong context: replay the full solution */
      const kube = { contexts: p.contexts, current: p.startContext, target: inc.context };
      const t = terminal(inc, pairs, kube);
      for (const c of cmds) t.type(c);
      if (anyKubectl) {
        assert.equal(t.status().done, false, inc.taskId + ' resolved on the wrong context (seed ' + seed + ')');
        assert.ok(t.rec.wrong > 0);
        assert.equal(t.rec.firstOk, false);
      } else {
        assert.equal(t.status().done, true, inc.taskId + ' (no kubectl) still resolves: only kubectl is context-bound');
        if (seed === 1) kubectlFree.push(inc.taskId);
      }
      /* 2. switch first, then the same solution */
      const kube2 = { contexts: p.contexts, current: p.startContext, target: inc.context };
      const t2 = terminal(inc, pairs, kube2);
      assert.deepEqual(t2.type('kubectl config use-context ' + inc.context).out, ['Switched to context "' + inc.context + '".']);
      for (const c of cmds) t2.type(c);
      assert.equal(t2.status().done, true, inc.taskId + ' resolves after use-context (seed ' + seed + ')');
      assert.equal(t2.rec.wrong, 0);
      if (anyKubectl) { assert.equal(t2.rec.firstOk, true); if (seed === 1) kubectlTasks += 1; }
    }
  }
  assert.ok(kubectlTasks > 0 && kubectlFree.length > 0);
});

test('scope, counted: 17 of the 28 paper task variants (24 tasks + 4 extra faults) use kubectl and are context-bound; the 11 kube-bench / CI-runner ones are not', () => {
  const all = new Map();
  for (const x of K.INCIDENTS) for (const f of (K.FAULTS[x.id] || [{ taskId: x.taskId }])) {
    const tk = C.task(x.simId, f.taskId);
    all.set(x.simId + ':' + f.taskId, tk.steps.flatMap((s) => split(s.hint)).some(isKubectl));
  }
  assert.equal(all.size, 28);
  assert.equal([...all.values()].filter(Boolean).length, 17);
  assert.deepEqual([...all].filter(([, v]) => !v).map(([k]) => k).sort(), [
    'cks-cluster-hardening:control-plane', 'cks-cluster-hardening:kubelet-auth', 'cks-cluster-hardening:readonly-port', 'cks-cluster-hardening:split-hardening',
    'cks-cluster-hardening:worker-authz', 'cks-cluster-hardening:worker-kubelet', 'cks-cluster-hardening:worker-readonly',
    'cks-static-analysis:kube-linter', 'cks-static-analysis:kubesec-gate', 'cks-supply-chain:sbom', 'cks-supply-chain:scan-gate']);
});

test('summarize + ui: the context habit is reported per task and per paper, never scored', () => {
  const p = K.buildPaper(C, { seed: 1113, count: 3, now: 0 });
  p.incidents[0].kube = { start: p.startContext, target: p.incidents[0].context, current: p.incidents[0].context, wrong: 0, firstOk: true, firstWrong: null };
  p.incidents[1].kube = { start: p.incidents[0].context, target: p.incidents[1].context, current: p.incidents[1].context, wrong: 3, firstOk: false, firstWrong: p.incidents[0].context };
  p.incidents[2].kube = null;
  const sum = K.summarize(p);
  assert.deepEqual(sum.contexts, { tasks: 3, usedKubectl: 2, landed: 1, wrongCmds: 3, wrongTasks: 1 });
  const offSum = K.summarize(K.buildPaper(C, { seed: 1113, count: 3, now: 0, contexts: false }));
  assert.equal(offSum.contexts, null);
  assert.equal(sum.pct, offSum.pct, 'contexts never change the score');
  assert.match(K.ui.contexts(sum), /^Cluster contexts: 1\/2 tasks that used kubectl started on the right cluster; 3 kubectl commands on 1 task went to another context/);
  assert.match(K.ui.contexts(sum), /empty stand-in clusters/);
  assert.match(K.ui.contextNote(p.incidents[0]), /switched before your first kubectl command ✓/);
  assert.match(K.ui.contextNote(p.incidents[1]), new RegExp('first kubectl command went to ' + p.incidents[0].context + ' ✗ · 3 kubectl commands hit another cluster'));
  assert.match(K.ui.contextNote(p.incidents[2]), /no kubectl command reached a cluster/);
  assert.equal(K.ui.contextPanel('sec-alpha'), 'Context for this task: sec-alpha · kubectl config use-context sec-alpha');
  assert.match(K.HONESTY, /seeded kubectl context/);
});

test('player v1.15.0: contextDim greys + darkens authored colours (identity at 0), cliExam.kube is validated, the gate runs before the rules engine', () => {
  const SRC = readFileSync(path.join(root, 'docs/assets/il-immersive-3d.js'), 'utf8');
  const sb = { console, Promise, navigator: {}, performance: { now: () => 0 }, document: { readyState: 'loading', addEventListener() {}, querySelectorAll: () => [] },
    addEventListener() {}, matchMedia: () => ({ matches: false }) };
  sb.window = sb; sb.globalThis = sb;
  vm.runInNewContext(SRC, sb, { filename: 'il-immersive-3d.js' });
  const API = sb.ILImmersive3D;
  assert.equal(API.version, '1.15.0');
  assert.equal(API.cliExamContexts, true);
  const c = [0.369, 0.918, 0.831];
  assert.equal(API.contextDim(c, 0), c);
  const d = API.contextDim(c, 1);
  const lum = (x) => 0.2126 * x[0] + 0.7152 * x[1] + 0.0722 * x[2];
  assert.ok(lum(d) < lum(c) * 0.5, 'darker');
  assert.ok(Math.max(...d) - Math.min(...d) < (Math.max(...c) - Math.min(...c)) * 0.3, 'desaturated');
  const half = API.contextDim(c, 0.5);
  assert.ok(lum(half) < lum(c) && lum(half) > lum(d), 'eases');
  assert.match(SRC, /var gate = this\._ctxGate\(engineLine\);[\s\S]{0,700}var r = C\.run\(sim\.id, this\._simState, engineLine, this\._cliCtx\);/);
  assert.match(SRC, /if \(dim\) \{ color = contextDim\(color, dim\);/);
  assert.match(SRC, /okName = function \(n\)\{ return typeof n === 'string' && \/\^\[a-z0-9\]\[a-z0-9\.-\]\{0,40\}\$\/\.test\(n\); \}/);
  assert.match(SRC, /il-immersive-cli-context/);
  assert.match(SRC, /instant: !!\(first \|\| prefersReduced\(\)\)/);
});

test('wiring: boot passes cliExam.kube and carries the context, page shows the context line and copy, manifest + docs record v1.3.0 / v1.14.0 / v1.15.0', () => {
  const boot = readFileSync(path.join(root, 'docs/assets/il-immersive-troubleshoot-boot.js'), 'utf8');
  assert.match(boot, /kube: inc\.context && paper\.contexts \? \{ contexts: paper\.contexts, current: kubeCurrent \|\| paper\.startContext, target: inc\.context \} : null/);
  assert.match(boot, /contexts=0/);
  assert.match(boot, /data-il-ts-context-note/);
  assert.match(boot, /inc\.kube = x && x\.kube \? x\.kube : null/);
  const page = readFileSync(path.join(root, 'docs/immersive/cks/index.html'), 'utf8');
  assert.match(page, /data-il-ts-context hidden/);
  assert.match(page, /data-il-ts-contexts/);
  assert.match(page, /Cluster contexts:/);
  assert.match(page, /a study cue the exam does not give/);
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  assert.equal(m.cks_paper.version, K.VERSION);
  assert.equal(m.cks_paper.contexts.version, '1.3.0');
  assert.equal(m.cks_paper.contexts.pool, K.CONTEXT_POOL.length);
  assert.match(m.cks_paper.contexts.honesty, /empty stand-in clusters/);
  assert.equal(m.sims.cli.version, C.VERSION);
  assert.match(m.sims.cli.contextsNote, /21 packs \/ 69 tasks \/ 383 steps/);
  const doc = readFileSync(path.join(root, 'docs/ops/MUSK-BAR-RECURSIVE.md'), 'utf8');
  assert.match(doc, /2026-11-13/);
});
