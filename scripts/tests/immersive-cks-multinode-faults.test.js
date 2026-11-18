/**
 * 2026-11-11 Musk-bar pass: multi-node CKS tasks + seeded FAULT variants.
 * il-immersive-sims.js v1.13.0 (node01: a worker with its own kubelet state, w1-* nodes in the re-authored, Blender-polished
 * cks-cluster-hardening.glb), il-immersive-cli.js v1.13.0 (`ssh node01` sessions / one-shot commands, per-host kube-bench,
 * config.yaml, systemctl; 4 new tasks) and il-immersive-cks-paper.js v1.2.0 (the three kube-bench incidents draw one of 7
 * authored faults per seed, and node01 itself is a varied name). Pure: the same files the browser runs.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const require = createRequire(import.meta.url);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const S = require(path.join(root, 'docs/assets/il-immersive-sims.js'));
globalThis.ILImmersiveSims = S;
const C = require(path.join(root, 'docs/assets/il-immersive-cli.js'));
require(path.join(root, 'docs/assets/il-immersive-troubleshoot.js'));
const K = require(path.join(root, 'docs/assets/il-immersive-cks-paper.js'));

const SIM = 'cks-cluster-hardening';
const KCFG = '/var/lib/kubelet/config.yaml';
const APIM = '/etc/kubernetes/manifests/kube-apiserver.yaml';
const NEW_TASKS = ['worker-kubelet', 'worker-authz', 'worker-readonly', 'split-hardening'];
const SEEDS = Array.from({ length: 40 }, (_, i) => i + 1);
const split = (h) => String(h).split(/\s{2}then\s{2}/);
const esc = (t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const word = (t) => new RegExp('(^|[^A-Za-z0-9_])' + esc(t) + '(?![A-Za-z0-9_])');

function session(taskId, extra) {
  const tk = taskId ? C.task(SIM, taskId) : null;
  let state = S.merge(S.merge(S.get(SIM).initial, tk ? tk.setup : {}), extra || {});
  const ctx = C.newCtx(taskId);
  return {
    ctx,
    get state() { return state; },
    run(line) { const r = C.run(SIM, state, line, ctx); if (r.set) state = S.merge(state, r.set); C.reconcile(SIM, state, ctx); return r; },
    prompt() { return C.promptFor(SIM, ctx); },
    status() { return C.taskStatus(SIM, taskId, state, ctx); },
    derive() { return S.get(SIM).derive(state); }
  };
}
function glbJson(rel) {
  const buf = readFileSync(path.join(root, 'docs', rel));
  const jl = buf.readUInt32LE(12);
  return JSON.parse(buf.toString('utf8', 20, 20 + jl).trim());
}
/** A paper terminal like the stage's: learner line → swap → rules engine; every printed line → swap. */
function terminal(inc, pairs) {
  const sw = K.swapper(pairs);
  let { state, ctx } = K.stage(C, S, { ...inc, cka: true });
  const printed = [];
  return {
    type(line) {
      const r = C.run(inc.simId, state, sw(line), ctx);
      if (r.set) state = S.merge(state, r.set);
      C.reconcile(inc.simId, state, ctx);
      r.out.forEach((ln) => printed.push(sw(ln)));
      printed.push(sw(C.promptFor(inc.simId, ctx)));
      return r;
    },
    status() { return C.taskStatus(inc.simId, inc.taskId, state, ctx); },
    printed
  };
}

test('sims v1.13.0: node01 has its own kubelet state; secure by default; the re-authored glb carries a Blender-polished node01 bay', () => {
  assert.equal(S.VERSION, '1.13.0');
  const sim = S.get(SIM);
  for (const k of ['w1AnonOff', 'w1WebhookAuthz', 'w1RoPortClosed', 'w1KubeletRestarted']) assert.equal(sim.initial[k], true, k);
  assert.ok(['w1AnonOff', 'w1WebhookAuthz', 'w1RoPortClosed'].every((id) => sim.toggles.some((t) => t.id === id)));
  const j = glbJson('assets/immersive/cks-cluster-hardening.glb');
  const names = j.nodes.map((n) => n.name);
  for (const n of ['w1-node', 'w1-kubelet', 'w1-kubelet-config', 'sim-w1-stale-config', 'w1-authn-gate', 'w1-authz-gate', 'w1-port-10250', 'w1-port-10255',
    'sim-w1-ro-port-open', 'sim-w1-kubelet-open', 'sim-w1-kubelet-denied', 'w1-kube-bench', 'sim-w1-bench-fail', 'edge-ssh-w1', 'edge-bench-w1', 'edge-probe-w1']) {
    assert.ok(names.includes(n), n);
    assert.ok(names.includes(n + '_LOD1'), n + ' went through the Blender CLI polish (LOD1)');
  }
  assert.equal(j.nodes.find((n) => n.name === 'w1-kubelet').extras.il.topic, SIM);
  assert.equal(j.nodes.find((n) => n.name === 'sim-w1-kubelet-open').extras.simOnly, true);
  const base = sim.derive(sim.initial);
  assert.equal(base.verdict, 'healthy');
  for (const n of ['sim-w1-stale-config', 'sim-w1-ro-port-open', 'sim-w1-kubelet-open', 'sim-w1-kubelet-denied', 'sim-w1-bench-fail']) assert.equal(S.styleFor(n, base.rules).hide, true, n + ' hidden when secure');
});

test('rules engine: node01 follows the same documented kubelet rules; a clean controlplane report says nothing about node01', () => {
  const sim = S.get(SIM);
  const at = (set) => S.cksHardenDecide(S.merge(sim.initial, set));
  const open = at({ w1AnonOff: false, w1WebhookAuthz: false, probe: true });
  assert.equal(open.kubeletCode, 401, 'controlplane kubelet untouched');
  assert.equal(open.w1.kubeletCode, 200);
  assert.deepEqual(open.w1.fails.map((b) => b.id), ['4.2.1', '4.2.2']);
  assert.ok(open.exposures.includes('node01-kubelet-api-open'));
  assert.equal(open.cpAllPass, true);
  assert.equal(open.allPass, false);
  assert.equal(sim.derive(S.merge(sim.initial, { w1AnonOff: false, w1WebhookAuthz: false, probe: true })).verdict, 'exposed');
  assert.equal(at({ w1AnonOff: false }).w1.kubeletCode, 403);
  assert.equal(at({ w1WebhookAuthz: false, probeToken: true }).w1.kubeletCode, 200, 'any SA token under AlwaysAllow');
  assert.deepEqual(at({ w1RoPortClosed: false }).w1.fails.map((b) => b.result), ['WARN']);
  assert.ok(at({}).w1.bench.every((b) => b.target === 'node'), 'a worker has no master checks');
  const stale = at({ w1AnonOff: true, w1KubeletRestarted: false, w1RunAnonOff: false, w1RunWebhookAuthz: true, w1RunRoClosed: true });
  assert.deepEqual([stale.w1.stale, stale.w1.kubeletCode, stale.w1.allPass], [true, 403, true], 'file PASSes, the running kubelet is still the old one');
  const r = sim.derive(S.merge(sim.initial, { w1AnonOff: false, w1WebhookAuthz: false, probe: true })).rules;
  assert.equal(S.styleFor('sim-w1-kubelet-open', r).hide, false);
  assert.equal(S.styleFor('sim-w1-bench-fail', r).hide, false);
  assert.equal(S.styleFor('sim-bench-fail', r).hide, true, 'the controlplane report itself is clean');
  assert.equal(S.styleFor('sim-bench-pass', r).hide, false, 'a green controlplane report shown in warn while node01 fails');
  assert.equal(S.styleFor('sim-w1-ro-port-open', sim.derive(S.merge(sim.initial, { w1RoPortClosed: false })).rules).hide, false);
});

test('CLI v1.13.0 hosts: ssh session + prompt, one-shot ssh, unknown host, worker has no API server manifest or etcd, master checks refused on node01', () => {
  assert.equal(C.VERSION, '1.13.0');
  const s = session(null);
  assert.equal(s.prompt(), 'root@controlplane:~#');
  assert.equal(s.run('ssh node02').exit, 255);
  assert.match(s.run('ssh node01').out[0], /logged in to node01/);
  assert.equal(s.prompt(), 'root@node01:~#');
  assert.deepEqual(s.run('hostname').out, ['node01']);
  for (const l of ['cat ' + APIM, 'grep profiling ' + APIM, "sed -i 's/--profiling=true/--profiling=false/' " + APIM, 'stat -c %a /var/lib/etcd', 'chmod 700 /var/lib/etcd']) {
    const r = s.run(l);
    assert.notEqual(r.exit, 0, l);
    assert.match(r.out[0], /No such file or directory/, l);
    assert.ok(r.events.includes('wrong-host'));
  }
  const m = s.run('kube-bench run --targets master');
  assert.equal(m.exit, 1);
  assert.match(m.out[0], /audits only the node it runs on/);
  assert.match(s.run('kube-bench run').out[0], /Worker Node Security Configuration/, 'default targets on a worker = node');
  assert.match(s.run('exit').out[1], /Connection to node01 closed/);
  assert.equal(s.prompt(), 'root@controlplane:~#');
  assert.deepEqual(s.run('ssh node01 hostname').out, ['node01'], 'one-shot ssh does not leave a session open');
  assert.equal(s.prompt(), 'root@controlplane:~#');
  assert.match(s.run('help').out.join('\n'), /node01 \(a worker with its own kubelet/);
});

test('traps: fixing the controlplane kubelet does not fix node01; restarting the wrong kubelet leaves node01 stale', () => {
  const s = session('worker-kubelet');
  assert.match(s.run('curl -sk https://node01:10250/pods').out[0], /PodList/);
  assert.deepEqual(s.run("sed -i '5s/true/false/' " + KCFG).events, ['sed-nochange'], 'controlplane config is already right');
  assert.match(s.run('curl -sk https://10.0.0.11:10250/pods').out[0], /PodList/, 'node01 by IP, still open');
  s.run("ssh node01 sed -i '5s/true/false/' " + KCFG);
  s.run("ssh node01 sed -i 's/mode: AlwaysAllow/mode: Webhook/' " + KCFG);
  s.run('systemctl restart kubelet');
  assert.match(s.run('curl -sk https://node01:10250/pods').out[0], /PodList/, 'restarted controlplane, not node01');
  assert.match(s.run('ssh node01 systemctl status kubelet').out[1], /started before the last/);
  assert.equal(S.styleFor('sim-w1-stale-config', s.derive().rules).hide, false);
  s.run('ssh node01 systemctl restart kubelet');
  assert.deepEqual(s.run('curl -sk https://node01:10250/pods').out, ['Unauthorized']);
  assert.deepEqual(s.run('curl -sk https://localhost:10250/pods').out, ['Unauthorized']);
});

test('the four multi-node tasks are solvable through an interactive ssh session too (not only the one-shot hints)', () => {
  const plans = {
    'worker-kubelet': ['kube-bench run --targets node', 'curl -sk https://node01:10250/pods', 'ssh node01', 'kube-bench run --targets node', 'cat -n ' + KCFG, "sed -i '5s/true/false/' " + KCFG,
      "sed -i 's/mode: AlwaysAllow/mode: Webhook/' " + KCFG, 'systemctl restart kubelet', 'curl -sk https://localhost:10250/pods', 'kube-bench run --targets node --check 4.2.1,4.2.2', 'exit'],
    'worker-authz': ['ssh node01', 'kube-bench run --targets node', 'curl -sk https://localhost:10250/pods', 'curl -sk -H "Authorization: Bearer $TOKEN" https://localhost:10250/pods',
      "sed -i 's/mode: AlwaysAllow/mode: Webhook/' " + KCFG, 'systemctl restart kubelet', 'curl -sk -H "Authorization: Bearer $TOKEN" https://localhost:10250/pods', 'kube-bench run --targets node --check 4.2.2'],
    'worker-readonly': ['curl -s http://node01:10255/pods', 'curl -s http://localhost:10255/pods', 'ssh node01', 'kube-bench run --targets node --check 4.2.4', "sed -i 's/readOnlyPort: 10255/readOnlyPort: 0/' " + KCFG,
      'systemctl restart kubelet', 'curl -s http://localhost:10255/pods'],
    'split-hardening': ['kube-bench run --targets master', "sed -i 's/--profiling=true/--profiling=false/' " + APIM, 'kube-bench run --targets master --check 1.2.15', 'curl -sk https://node01:10250/pods',
      'ssh node01', 'kube-bench run --targets node --check 4.2.1', "sed -i '5s/true/false/' " + KCFG, 'systemctl restart kubelet', 'curl -sk https://node01:10250/pods', 'kube-bench run --targets node --check 4.2.1']
  };
  for (const id of NEW_TASKS) {
    const s = session(id);
    assert.equal(s.status().completed, 0, id);
    for (const l of plans[id]) s.run(l);
    assert.equal(s.status().done, true, id + ' ' + s.status().completed + '/' + s.status().total);
    assert.equal(s.derive().verdict, 'healthy', id + ' leaves the cluster healthy');
  }
  assert.deepEqual(NEW_TASKS.map((id) => C.task(SIM, id).steps.length), [8, 7, 6, 9]);
  const sp = session('split-hardening');
  sp.run('ssh node01');
  assert.match(sp.run('kube-bench run --targets master').out[0], /node01 is a worker/, 'the API server finding cannot be fixed from node01');
});

test('paper v1.2.0 FAULTS: canonical first, every fault is a real task on the same scene, tickets never leak a command or a step label', () => {
  assert.equal(K.VERSION, '1.2.0');
  assert.deepEqual(Object.keys(K.FAULTS).sort(), ['cks-bench-control-plane', 'cks-bench-kubelet', 'cks-bench-readonly']);
  let n = 0, multi = 0;
  for (const [id, list] of Object.entries(K.FAULTS)) {
    const inc = K.get(id);
    assert.equal(list[0].taskId, inc.taskId, id + ': [0] is the free-play (v1.0.0) fault');
    assert.equal(list[0].ticket, undefined, 'canonical keeps the bank ticket');
    assert.ok(list.length >= 2);
    for (const f of list) {
      n += 1;
      const tk = C.task(inc.simId, f.taskId);
      assert.ok(tk, f.id);
      assert.equal(K.fault(f.id), f);
      if (f.host !== 'controlplane') multi += 1;
      const ticket = f.ticket || inc.ticket;
      assert.ok(ticket.length > 80);
      for (const st of tk.steps) {
        for (const cmd of split(st.hint)) assert.equal(ticket.includes(cmd), false, f.id + ' leaks ' + cmd);
        assert.equal(ticket.includes(st.label), false, f.id + ' leaks a label');
      }
      for (const t of f.vary) assert.ok(word(t).test(ticket + tk.steps.map((s) => s.hint).join('\n')), f.id + ' varies ' + t);
    }
  }
  assert.equal(n, 7);
  assert.equal(multi, 4);
  assert.deepEqual(K.POOLS.node01, ['compute-03', 'wk-east-2', 'k8s-w7']);
});

test('faultFor: deterministic, every fault reachable, independent of the task draw and of the v1.1.0 name draw; variants off = canonical', () => {
  const seen = new Set();
  for (let seed = 1; seed <= 80; seed++) for (const id of Object.keys(K.FAULTS)) { assert.equal(K.faultFor(id, seed), K.faultFor(id, seed)); seen.add(K.faultFor(id, seed).id); }
  assert.equal(seen.size, 7, 'all 7 authored faults are drawn within 80 seeds');
  for (const seed of SEEDS) {
    const on = K.buildPaper(C, { seed, count: 18 }), off = K.buildPaper(C, { seed, count: 18, variants: false }), nf = K.buildPaper(C, { seed, count: 18, faults: false });
    assert.deepEqual(on.incidents.map((i) => i.id), off.incidents.map((i) => i.id), 'same task draw');
    assert.equal(on.faults, true); assert.equal(off.faults, false); assert.equal(nf.faults, false);
    for (const inc of off.incidents) { assert.equal(inc.fault, null); assert.equal(inc.taskId, K.get(inc.id).taskId); }
    for (const inc of on.incidents) {
      if (!K.FAULTS[inc.id]) {
        assert.equal(inc.fault, null);
        assert.deepEqual(inc.variant ? inc.variant.pairs : [], K.variantFor(inc.id, seed).pairs, 'v1.1.0 name draw unchanged');
        continue;
      }
      assert.equal(inc.fault.id, K.faultFor(inc.id, seed).id);
      assert.equal(inc.taskId, K.fault(inc.fault.id).taskId);
      assert.equal(inc.steps, C.task(inc.simId, inc.taskId).steps.length);
      assert.equal(inc.fault.canonical, inc.fault.id === K.FAULTS[inc.id][0].id);
      if (K.fault(inc.fault.id).vary.includes('node01')) {
        assert.ok(inc.variant && inc.variant.pairs.some(([c]) => c === 'node01'));
        assert.equal(word('node01').test(inc.ticket), false, 'the ticket names the drawn worker, not node01');
      }
    }
  }
  /* every one of the 24 incidents now varies per seed: by names (21) or by fault + host name (3) */
  for (const x of K.INCIDENTS) {
    const sig = new Set(SEEDS.map((seed) => { const f = K.faultFor(x.id, seed); return (f ? f.id : '') + '|' + K.variantFor(x.id, seed, f ? f.id : null).label; }));
    assert.ok(sig.size >= 2, x.id + ' varies');
  }
});

test('every fault is solvable at 100% by typing its commands in the paper\'s names (40 seeds), and the shell never prints node01 when it was re-drawn', () => {
  for (const [id, list] of Object.entries(K.FAULTS)) {
    const base = K.get(id);
    for (const f of list) {
      const tk = C.task(base.simId, f.taskId);
      for (const seed of f.vary.length ? SEEDS : [1]) {
        const v = K.variantFor(id, seed, f.id), sw = K.swapper(v.pairs);
        const inc = { ...base, taskId: f.taskId };
        const term = terminal(inc, v.pairs);
        for (const st of tk.steps) for (const cmd of split(st.hint)) term.type(sw(cmd));
        assert.equal(term.status().done, true, f.id + ' seed ' + seed + ' (' + v.label + ')');
        const g = K.gradeIncident({ ...inc, cka: true, steps: tk.steps.length, variant: v.pairs.length ? v : null, fault: { id: f.id, label: f.label } }, term.status(), [], { cmds: 9 });
        assert.equal(g.pct, 100);
        assert.equal(g.fault, f.label);
        term.type('help'); term.type(sw('ssh node01')); term.type('hostname'); term.type('exit');
        const out = term.printed.join('\n');
        for (const [c] of v.pairs) assert.equal(word(c).test(out), false, f.id + ' seed ' + seed + ' leaks ' + c);
      }
    }
  }
});

test('a drill replay does not pass: the canonical fault\'s commands leave every other fault unresolved; typing node01 from memory does not resolve the worker', () => {
  let checked = 0;
  for (const [id, list] of Object.entries(K.FAULTS)) {
    const base = K.get(id), canon = C.task(base.simId, list[0].taskId);
    for (const f of list.slice(1)) {
      for (const seed of [3, 11, 29]) {
        const v = K.variantFor(id, seed, f.id);
        const term = terminal({ ...base, taskId: f.taskId }, v.pairs);
        for (const st of canon.steps) for (const cmd of split(st.hint)) term.type(cmd); /* the free-play replay */
        assert.equal(term.status().done, false, f.id + ': the ' + list[0].taskId + ' replay must not resolve it');
        const term2 = terminal({ ...base, taskId: f.taskId }, v.pairs);
        for (const st of C.task(base.simId, f.taskId).steps) for (const cmd of split(st.hint)) term2.type(cmd); /* right fault, canonical host name */
        assert.equal(term2.status().done, false, f.id + ' seed ' + seed + ': node01 is ' + v.label + ' on this paper');
        assert.ok(term2.printed.some((l) => /^ssh: Could not resolve hostname node01: /.test(l)), 'ssh to the drill name does not resolve (in the learner\'s view, node01 does not exist on this paper)');
        checked += 1;
      }
    }
  }
  assert.equal(checked, 12);
});

test('wiring: boot marks the stage and results with the fault, page copy is honest, manifest + docs record v1.2.0 / v1.13.0', () => {
  const boot = readFileSync(path.join(root, 'docs/assets/il-immersive-troubleshoot-boot.js'), 'utf8');
  assert.match(boot, /data-il-ts-fault', inc\.fault\.id/);
  assert.match(boot, /Fault staged on this paper: /);
  assert.match(boot, /data-il-ts-faults/);
  const page = readFileSync(path.join(root, 'docs/immersive/cks/index.html'), 'utf8');
  assert.match(page, /Seeded fault variants \+ two nodes/);
  assert.match(page, /7 authored faults over 3 tasks, not procedurally generated faults/);
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  assert.equal(m.cks_paper.version, K.VERSION);
  assert.equal(m.cks_paper.faults.version, '1.2.0');
  assert.equal(m.cks_paper.faults.authored_faults, 7);
  assert.equal(m.cks_paper.faults.multi_node_faults, 4);
  assert.match(m.cks_paper.faults.honesty, /not procedurally generated/);
  assert.equal(m.sims.runtime_version, '1.13.0');
  assert.equal(m.sims.cli.version, '1.13.0');
  assert.match(m.sims.cli.hardeningNote, /No VM and no real ssh/);
  assert.match(m.scenes.find((x) => x.sim === SIM).note, /node01 worker bay/);
  const doc = readFileSync(path.join(root, 'docs/ops/MUSK-BAR-RECURSIVE.md'), 'utf8');
  assert.match(doc, /2026-11-11/);
  assert.match(K.HONESTY, /7 authored faults/);
});
