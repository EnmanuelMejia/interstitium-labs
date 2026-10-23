/**
 * 2026-10-23 Musk-bar pass: Service + DNS troubleshooting (the other half of CKA Troubleshooting = 30%) on a NEW
 * authored asset, service-dns.glb (kit-v2 + Blender CLI polish), its rules-engine drill (service-dns) and a 4-task CLI
 * pack with a dnsutils debug pod. Pure UMD — the browser runs exactly this code. Generic tip/focus/replay coverage for
 * the new pack comes from the loops in immersive-cli.test.js / immersive-cli-packs.test.js, which iterate C.list() (13 packs).
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
const C = require(path.join(root, 'docs/assets/il-immersive-cli.js'));
const E = require(path.join(root, 'docs/assets/il-immersive-exam.js'));
const SIM = 'service-dns';
const NSL = 'kubectl exec -n shop dnsutils -- nslookup ';
const CURL = 'kubectl exec -n shop deploy/web -- curl -s -m 3 ';

function session(taskId, extra) {
  const tk = taskId ? C.task(SIM, taskId) : null;
  let state = S.merge(S.merge(S.get(SIM).initial, tk ? tk.setup : {}), extra || {});
  const ctx = C.newCtx(taskId);
  return {
    ctx,
    get state() { return state; },
    run(line) { const r = C.run(SIM, state, line, ctx); if (r.set) state = S.merge(state, r.set); return r; },
    status() { return C.taskStatus(SIM, taskId, state, ctx); },
    derived() { return S.get(SIM).derive(state); }
  };
}
function glbJson(rel) {
  const buf = readFileSync(path.join(root, 'docs', rel));
  const jl = buf.readUInt32LE(12);
  return JSON.parse(buf.toString('utf8', 20, 20 + jl).trim());
}

test('NEW asset: service-dns.glb is authored + Blender-polished, keeps names and pedagogy extras, sim-* nodes hidden by default', () => {
  const sim = S.get(SIM);
  assert.equal(sim.glb, '/assets/immersive/service-dns.glb');
  const others = S.list().filter(id => id !== SIM).map(id => S.get(id).glb);
  assert.ok(!others.includes(sim.glb), 'a new asset, not a re-read of an existing scene');
  const j = glbJson('assets/immersive/service-dns.glb');
  const names = j.nodes.map(n => n.name);
  for (const n of ['client-pod', 'resolv-conf', 'svc-api', 'svc-api-port', 'svc-api-selector', 'endpointslice-api', 'api-pod-0', 'api-pod-1', 'container-port-0',
    'kube-proxy-rules', 'svc-kube-dns', 'coredns-0', 'coredns-1', 'corefile', 'sim-crash-ring-0', 'sim-netpol-wall', 'netpol-tablet', 'svc-db', 'sim-nxdomain-flag', 'edge-client-dns']) {
    assert.ok(names.includes(n), n);
  }
  assert.ok(names.some(n => /_LOD1$/.test(n)), 'Blender CLI polish ran (LOD1 decimate duplicates present)');
  const svc = j.nodes.find(n => n.name === 'svc-api');
  assert.equal(svc.extras && svc.extras.il && svc.extras.il.topic, 'service-dns', 'pedagogy extras survive polish');
  const base = sim.derive(sim.initial).rules;
  for (const n of ['sim-crash-ring-0', 'sim-netpol-wall', 'sim-nxdomain-flag']) assert.equal(S.styleFor(n, base).hide, true, n + ' hidden when healthy');
  assert.equal(S.styleFor('sim-crash-ring-1', sim.derive(S.merge(sim.initial, { corefileOk: false })).rules).hide, false);
  assert.equal(S.styleFor('sim-netpol-wall', sim.derive(S.merge(sim.initial, { dnsEgress: false })).rules).hide, false);
  assert.equal(S.styleFor('sim-nxdomain-flag', sim.derive(S.merge(sim.initial, { fqdnOk: false })).rules).hide, false);
});

test('resolver: resolv.conf search list + ndots:5 — short names stay in the namespace, <svc>.<ns> crosses, failures differ by cause', () => {
  const ok = S.get(SIM).initial;
  assert.equal(S.svcDnsResolve(ok, 'api').fqdn, 'api.shop.svc.cluster.local');
  assert.deepEqual(S.svcDnsResolve(ok, 'db').tried, ['db.shop.svc.cluster.local', 'db.svc.cluster.local', 'db.cluster.local', 'db']);
  assert.equal(S.svcDnsResolve(ok, 'db').status, 'nxdomain');
  assert.equal(S.svcDnsResolve(ok, 'db.data').fqdn, 'db.data.svc.cluster.local');
  assert.equal(S.svcDnsResolve(ok, 'kubernetes.default').ip, '10.96.0.1');
  assert.equal(S.svcDnsResolve(ok, 'api.shop.svc.cluster.local.').tried.length, 1, 'a trailing dot is absolute');
  assert.equal(S.svcDnsResolve(ok, 'api', { noSearch: true }).status, 'nxdomain', 'dig without +search does not expand');
  assert.equal(S.svcDnsResolve(S.merge(ok, { dnsEgress: false }), 'api').status, 'timeout', 'a NetworkPolicy drop is silent');
  assert.equal(S.svcDnsResolve(S.merge(ok, { corefileOk: false }), 'api').status, 'refused', 'no ready kube-dns endpoints → rejected');
});

test('rules engine: Service / EndpointSlice / kube-proxy / CoreDNS / NetworkPolicy semantics', () => {
  const sim = S.get(SIM);
  const at = set => S.serviceDnsDecide(S.merge(sim.initial, set));
  assert.equal(S.VERSION, '1.6.0');
  assert.equal(sim.derive(sim.initial).verdict, 'healthy');
  const sel = at({ selectorOk: false });
  assert.equal(sel.endpoints, 0);
  assert.equal(sel.apiByIp, 'refused-no-endpoints');
  assert.equal(sel.apiResolves, true, 'a ClusterIP Service keeps its A record with no endpoints');
  const tp = at({ targetPortOk: false });
  assert.equal(tp.endpoints, 2, 'the selector still matches');
  assert.equal(tp.endpointPort, 80, 'EndpointSlices copy targetPort, not containerPort');
  assert.equal(tp.apiByIp, 'refused-target-port');
  const cf = at({ corefileOk: false });
  assert.equal(cf.corednsPods, 'CrashLoopBackOff');
  assert.equal(cf.kubeDnsReadyEndpoints, 0);
  assert.equal(cf.dns, false);
  assert.equal(cf.apiByIp, 'ok', 'Service routing is kube-proxy’s job, not CoreDNS’s');
  const np = at({ dnsEgress: false });
  assert.equal(np.dnsFailure, 'timeout');
  assert.equal(np.apiByIp, 'ok', 'same-namespace egress after DNAT is allowed');
  const fq = at({ fqdnOk: false });
  assert.equal(fq.dbLookup, 'nxdomain');
  assert.equal(fq.dns, true);
  assert.equal(sim.derive(S.merge(sim.initial, { corefileOk: false })).verdict, 'down');
  assert.equal(sim.derive(S.merge(sim.initial, { dnsEgress: false })).verdict, 'down');
  assert.equal(sim.derive(S.merge(sim.initial, { targetPortOk: false })).verdict, 'degraded');
  assert.equal(sim.derive(S.merge(sim.initial, { fqdnOk: false })).verdict, 'degraded');
  const keys = sim.scenarios.filter(sc => sc.predict).map(sc => sc.predict.answer);
  assert.equal(keys.length, 5);
  assert.equal(new Set(keys).size, 3, 'keyed answers spread across positions 0-2');
  for (const sc of sim.scenarios.filter(x => x.predict)) assert.notEqual(sim.derive(S.merge(sim.initial, sc.set)).verdict, 'healthy', sc.id + ' breaks something');
});

test('target-port: endpoints present on :80, describe svc vs describe deployment, strategic-merge patch fixes it; task verifies 6/6', () => {
  const s = session('target-port');
  const c = s.run(CURL + 'http://api');
  assert.equal(c.exit, 7);
  assert.match(c.out[0], /curl: \(7\) Failed to connect to api port 80/);
  assert.ok(s.run('kubectl get endpointslices -n shop -l kubernetes.io/service-name=api').out.some(l => /^api-\w+\s+IPv4\s+80\s+10\.244\.1\.21,10\.244\.2\.17/.test(l)));
  assert.ok(s.run('kubectl describe svc api -n shop').out.includes('TargetPort:               80/TCP'));
  assert.ok(s.run('kubectl describe deployment api -n shop').out.some(l => /Port:\s+8080\/TCP/.test(l)));
  assert.match(s.run("kubectl patch svc api -n shop -p '{\"spec\":{\"ports\":[{\"targetPort\":8080}]}}'").out[0], /merged on its `port` key/, 'a ports entry without port is rejected');
  s.run("kubectl patch svc api -n shop -p '{\"spec\":{\"ports\":[{\"port\":80,\"targetPort\":8080}]}}'");
  assert.equal(s.state.targetPortOk, true);
  const ok = s.run(CURL + 'http://api');
  assert.equal(ok.exit, 0);
  assert.equal(s.status().total, 6);
  assert.equal(s.status().done, true);
});

test('selector (free play): empty EndpointSlice is refused fast, the name still resolves, set selector restores it', () => {
  const s = session(null, { selectorOk: false });
  assert.ok(s.run('kubectl get endpointslices -n shop -l kubernetes.io/service-name=api').out.some(l => /<unset>\s+<unset>/.test(l)));
  assert.match(s.run('kubectl get endpoints -n shop api').out[0], /deprecated in v1\.33\+/);
  assert.equal(s.run(NSL + 'api').exit, 0, 'DNS still answers for a Service without endpoints');
  assert.equal(s.run(CURL + 'http://api').exit, 7);
  assert.ok(s.run('kubectl get svc api -n shop -o wide').out.some(l => /app=api-v2$/.test(l)));
  s.run('kubectl set selector service api app=api -n shop');
  assert.equal(s.state.selectorOk, true);
  assert.equal(s.run(CURL + 'http://api').exit, 0);
});

test('coredns-corefile: refused lookups, CrashLoopBackOff, parse error in logs; save > file, sed -i, apply -f; task verifies 7/7', () => {
  const s = session('coredns-corefile');
  const r = s.run(NSL + 'api');
  assert.equal(r.exit, 1);
  assert.match(r.out[0], /communications error to 10\.96\.0\.10#53: connection refused/);
  assert.equal(s.run(CURL + 'http://10.96.88.20').exit, 0, 'ClusterIP by IP still works with DNS down');
  assert.equal(s.run(CURL + 'http://api').exit, 6, 'by name it cannot resolve');
  assert.ok(s.run('kubectl get pods -n kube-system -l k8s-app=kube-dns').out.every((l, i) => i === 0 || /CrashLoopBackOff/.test(l)));
  const logs = s.run('kubectl logs -n kube-system -l k8s-app=kube-dns').out;
  assert.match(logs[0], /representative/);
  assert.match(logs[1], /Corefile:\d+ - Error during parsing: Unknown directive 'forwrd'/);
  assert.ok(s.run('kubectl get configmap coredns -n kube-system -o yaml').out.includes('        forwrd . /etc/resolv.conf {'));
  /* sed / apply on a file that does not exist yet fail like the real tools */
  assert.match(s.run("sed -i 's/forwrd/forward/' coredns.yaml").out[0], /can't read coredns\.yaml/);
  assert.match(s.run('kubectl apply -f coredns.yaml').out[0], /does not exist/);
  assert.equal(s.run('kubectl get configmap coredns -n kube-system -o yaml > coredns.yaml').out.length, 0);
  assert.match(s.run('ls').out[0], /coredns\.yaml/);
  /* applying the unedited file changes nothing; sed without -i writes nothing */
  assert.equal(s.run('kubectl apply -f coredns.yaml').out[0], 'configmap/coredns unchanged');
  s.run("sed 's/forwrd/forward/' coredns.yaml");
  assert.ok(s.run('cat coredns.yaml').out.some(l => /forwrd/.test(l)));
  s.run('kubectl -n kube-system rollout restart deployment coredns');
  assert.equal(s.state.corefileOk, false, 'restarting does not fix a bad Corefile');
  s.run("sed -i 's/forwrd/forward/' coredns.yaml");
  assert.ok(s.run('cat coredns.yaml').out.some(l => /^\s+forward \. \/etc\/resolv\.conf/.test(l)));
  assert.equal(s.run('kubectl apply -f coredns.yaml').out[0], 'configmap/coredns configured');
  assert.equal(s.state.corefileOk, true);
  assert.ok(s.run('kubectl get pods -n kube-system -l k8s-app=kube-dns').out.slice(1).every(l => /Running/.test(l)));
  assert.equal(s.run(NSL + 'api').exit, 0);
  assert.equal(s.status().total, 7);
  assert.equal(s.status().done, true);
  assert.match(s.run('kubectl get pods -n kube-system > out.txt').out[0], /redirection is modelled only/, 'no invented redirects');
});

test('dns-egress: timeout (not refused), ClusterIP by IP still works, describe shows the deny policy, additive allow fixes it; 5/5', () => {
  const s = session('dns-egress');
  const r = s.run(NSL + 'api');
  assert.match(r.out[0], /connection timed out; no servers could be reached/);
  assert.equal(s.run(CURL + 'http://10.96.88.20').exit, 0);
  assert.ok(s.run('kubectl get networkpolicy -n shop').out.some(l => /^default-deny-egress/.test(l)));
  assert.match(s.run('kubectl describe networkpolicy default-deny-egress -n shop').out.join('\n'), /Policy Types: Egress[\s\S]*nothing reaches kube-system/);
  assert.match(s.run('cat allow-dns-egress.yaml').out.join('\n'), /k8s-app: kube-dns[\s\S]*protocol: UDP\n\s+port: 53\n\s+- protocol: TCP\n\s+port: 53/);
  s.run('kubectl apply -f allow-dns-egress.yaml');
  assert.equal(s.state.dnsEgress, true);
  assert.ok(s.run('kubectl get networkpolicy -n shop').out.some(l => /^allow-dns-egress/.test(l)), 'the deny policy stays; the allow adds to it');
  assert.equal(s.run(NSL + 'api').exit, 0);
  assert.equal(s.status().done, true);
});

test('cross-ns-fqdn: no such host in the app log, NXDOMAIN + search list, set env DB_HOST=db.data…; 6/6; dig needs +search', () => {
  const s = session('cross-ns-fqdn');
  assert.ok(s.run('kubectl logs -n shop deploy/web').out.some(l => /lookup db on 10\.96\.0\.10:53: no such host/.test(l)));
  assert.match(s.run(NSL + 'db').out.join('\n'), /\*\* server can't find db: NXDOMAIN/);
  assert.equal(s.run(NSL + 'db.data').exit, 0);
  assert.deepEqual(s.run('kubectl exec -n shop dnsutils -- dig +short db.data.svc.cluster.local').out, ['10.96.140.5']);
  assert.match(s.run('kubectl exec -n shop dnsutils -- dig api').out.join('\n'), /status: NXDOMAIN[\s\S]*\+search/);
  assert.match(s.run('kubectl exec -n shop dnsutils -- dig +search api').out.join('\n'), /status: NOERROR/);
  assert.deepEqual(s.run('kubectl exec -n shop dnsutils -- cat /etc/resolv.conf').out, ['search shop.svc.cluster.local svc.cluster.local cluster.local', 'nameserver 10.96.0.10', 'options ndots:5']);
  assert.ok(s.run('kubectl get svc -A').out.some(l => /^data\s+db\s/.test(l)));
  assert.equal(s.run('kubectl set env deployment/web -n shop --list').out[1], 'DB_HOST=db');
  s.run('kubectl set env deployment/web -n shop DB_HOST=database.data');
  assert.equal(s.state.fqdnOk, false, 'a wrong name stays wrong');
  s.run('kubectl set env deployment/web -n shop DB_HOST=db.data.svc.cluster.local');
  assert.equal(s.state.fqdnOk, true);
  assert.ok(s.run('kubectl logs -n shop deploy/web').out.some(l => /connected to db\.data\.svc\.cluster\.local:5432/.test(l)));
  assert.equal(s.status().done, true);
});

test('honesty: lookups only from pods, no DNS tools in the web image, no internet upstream, no editor, help states the scope', () => {
  const s = session(null);
  assert.match(s.run('nslookup api').out[0], /run the lookup from a pod/);
  assert.equal(s.run('kubectl exec -n shop deploy/web -- nslookup api').exit, 126);
  assert.match(s.run(NSL + 'example.com').out[0], /cluster names only/);
  assert.equal(s.run('kubectl edit cm coredns -n kube-system').exit, 2);
  assert.equal(s.run('kubectl exec -n default dnsutils -- nslookup api').exit, 1);
  const h = s.run('help').out.join('\n');
  assert.match(h, /Not a real shell, not a cluster/);
  assert.match(h, /dnsutils is a debug pod/);
  const run = s.run('kubectl run tmp -n shop --rm -it --restart=Never --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- nslookup kubernetes.default');
  assert.equal(run.exit, 0);
  assert.match(run.out[run.out.length - 1], /pod "tmp" deleted/);
});

test('voice + coach: spoken nslookup / coredns / configmap normalise; coach never leaks the command', () => {
  assert.deepEqual(C.fromSpeech('kubectl exec dash n shop dnsutils dash dash n s lookup api', SIM), { line: NSL + 'api', verb: false });
  assert.deepEqual(C.fromSpeech('kubectl get config map core dns dash n kube dash system dash o yaml', SIM), { line: 'kubectl get configmap coredns -n kube-system -o yaml', verb: false });
  const s = session('coredns-corefile');
  for (const l of [NSL + 'api', 'kubectl get pods -n kube-system -l k8s-app=kube-dns', 'kubectl logs -n kube-system -l k8s-app=kube-dns']) s.run(l);
  C.coach(SIM, 'coredns-corefile', s.state, s.ctx);
  const c = C.coach(SIM, 'coredns-corefile', s.state, s.ctx);
  assert.equal(c.step, 3);
  assert.equal(c.level, 'hint');
  assert.ok(!c.lines.join('\n').includes('> coredns.yaml'), 'hint level does not print the command');
  assert.match(c.focus, /corefile/);
  const sol = C.coach(SIM, 'coredns-corefile', s.state, s.ctx, { count: false, level: 'solution' });
  assert.equal(sol.solution, 'kubectl get configmap coredns -n kube-system -o yaml > coredns.yaml');
});

test('blueprint: Troubleshooting (30%) now has three drills; service-dns is graded CKA scope with its own 3D anchor', () => {
  const tr = E.BLUEPRINT.find(b => b.domain === 'Troubleshooting');
  assert.deepEqual(tr.sims, ['control-plane-failure', 'node-troubleshoot', 'service-dns']);
  assert.equal(E.OFFICIAL[SIM], 'Troubleshooting');
  const all = E.BLUEPRINT.reduce((a, b) => a.concat(b.sims), []);
  assert.equal(new Set(all).size, all.length, 'every drill maps to exactly one domain');
});

test('wiring: /immersive/ host, exam lobby copy, curriculum mirror, manifest (new scene, pack, honest notes)', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(html, /id="cka-service-dns"[\s\S]*?data-il-sim="service-dns"\s*\n\s*data-gltf="\/assets\/immersive\/service-dns\.glb"/);
  assert.match(html, /The shell is simulated and runs on a rules engine: there is no live cluster and no real CoreDNS/);
  assert.match(readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8'), /13 drills \([^)]*Service &amp; DNS/);
  for (const f of ['labs.json', 'mirror.json']) {
    const j = JSON.parse(readFileSync(path.join(root, 'docs/curriculum-os', f), 'utf8'));
    const lab = (j.items || j.labs).find(l => l.immersive && l.immersive.sim === SIM);
    assert.ok(lab && lab.id === 'lab-sim-service-dns' && lab.publishStatus === 'published' && lab.gltf === '/assets/immersive/service-dns.glb', f);
  }
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const sc = m.scenes.find(x => x.sim === SIM);
  assert.equal(sc.gltf, '/assets/immersive/service-dns.glb');
  assert.equal(sc.polishedOn, '2026-10-23');
  assert.ok(m.sims.list.includes(SIM) && m.cka_coverage.interactive.includes(SIM));
  assert.equal(m.sims.cli.version, C.VERSION);
  assert.match(m.sims.cli.serviceDnsNote, /No live cluster, no real CoreDNS, no internet upstream, no clock/);
  assert.equal(m.sims.runtime_version, S.VERSION);
  assert.equal(m.cka_coverage.liveUnrealHost, false);
  assert.equal(m.cka_coverage.hostedFleet, false);
});
