/**
 * 2026-11-02 Musk-bar pass: CKS track part 2 — Supply Chain Security (20% of the CKS), which the 2026-10-29 CKS paper
 * honestly listed as "not covered". A NEW authored asset, cks-supply-chain.glb (kit-v2 + Blender CLI polish), its
 * rules-engine drill (7 predict checkpoints), a 4-task CLI pack (VAP allow-list, Trivy gate, SBOM, cosign + admission
 * verification), and the CKS paper now evidencing all 6 official domains. Generic tip/focus/replay/example coverage for
 * the new pack comes from the loops in immersive-cli.test.js / immersive-cli-packs.test.js (17 packs).
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
const R = require(path.join(root, 'docs/assets/il-immersive-review.js'));
const SIM = 'cks-supply-chain';
const TAG = 'registry.example.com/payments/api:2.4.1';

function session(taskId, extra) {
  const tk = taskId ? C.task(SIM, taskId) : null;
  let state = S.merge(S.merge(S.get(SIM).initial, tk ? tk.setup : {}), extra || {});
  const ctx = C.newCtx(taskId);
  return {
    ctx,
    get state() { return state; },
    run(line) { const r = C.run(SIM, state, line, ctx); if (r.set) state = S.merge(state, r.set); return r; },
    status() { return C.taskStatus(SIM, taskId, state, ctx); },
    verdict() { return S.get(SIM).derive(state).verdict; }
  };
}
function glbJson(rel) {
  const buf = readFileSync(path.join(root, 'docs', rel));
  const jl = buf.readUInt32LE(12);
  return JSON.parse(buf.toString('utf8', 20, 20 + jl).trim());
}

test('NEW asset: cks-supply-chain.glb is authored + Blender-polished, the second CKS scene; sim-* nodes hidden when secure', () => {
  const sim = S.get(SIM);
  assert.ok(['1.8.0', '1.9.0', '1.10.0', '1.11.0', '1.12.0'].includes(S.VERSION), 'cks-supply-chain arrived in v1.8.0; v1.9.0 (2026-11-03) keeps it');
  assert.equal(sim.cert, 'CKS');
  assert.equal(sim.glb, '/assets/immersive/cks-supply-chain.glb');
  assert.ok(!S.list().filter(id => id !== SIM).map(id => S.get(id).glb).includes(sim.glb), 'a new asset, not a re-read of an existing scene');
  const j = glbJson('assets/immersive/cks-supply-chain.glb');
  const names = j.nodes.map(n => n.name);
  for (const n of ['ci-pipeline', 'ci-build', 'trivy-scanner', 'sim-cve-flare', 'sim-ci-block', 'sbom-doc', 'cosign-key', 'signature-seal', 'registry-trusted', 'image-artifact', 'digest-pin',
    'sim-tag-drift', 'sim-unsigned-mark', 'registry-untrusted', 'untrusted-image', 'kube-apiserver', 'vap-gate', 'sim-vap-deny', 'sig-webhook', 'sim-sig-deny', 'ns-payments', 'payments-pod',
    'sim-vuln-halo', 'edge-registry-api', 'edge-untrusted-api', 'edge-api-pod', 'edge-push']) assert.ok(names.includes(n), n);
  assert.ok(names.some(n => /_LOD1$/.test(n)), 'Blender CLI polish ran (LOD1 decimate duplicates present)');
  const pod = j.nodes.find(n => n.name === 'payments-pod');
  assert.equal(pod.extras.il.topic, SIM, 'pedagogy extras survive polish');
  assert.equal(pod.extras.il.domain, 'supply-chain');
  assert.equal(j.nodes.find(n => n.name === 'sim-vap-deny').extras.simOnly, true);
  const base = sim.derive(sim.initial);
  assert.equal(base.verdict, 'healthy');
  for (const n of ['sim-cve-flare', 'sim-ci-block', 'sim-tag-drift', 'sim-unsigned-mark', 'sim-vap-deny', 'sim-sig-deny', 'sim-vuln-halo']) assert.equal(S.styleFor(n, base.rules).hide, true, n + ' hidden when secure');
  const at = set => sim.derive(S.merge(sim.initial, set)).rules;
  assert.equal(S.styleFor('sim-vap-deny', at({ fromTrusted: false })).hide, false);
  assert.equal(S.styleFor('sim-sig-deny', at({ signed: false })).hide, false);
  assert.equal(S.styleFor('sim-ci-block', at({ scanClean: false })).hide, false);
  assert.equal(S.styleFor('sim-tag-drift', at({ pinnedDigest: false })).hide, false);
  assert.equal(S.styleFor('sim-vuln-halo', at({ scanGate: false, scanClean: false })).hide, false);
});

test('rules engine: registry allow-list, scan gate, signature ≠ safety, provenance, digest pinning', () => {
  const sim = S.get(SIM);
  const at = set => S.cksSupplyDecide(S.merge(sim.initial, set));
  const v = set => sim.derive(S.merge(sim.initial, set)).verdict;
  /* no policy: Kubernetes admits anything */
  const open = at({ vapRegistry: false, verifySig: false, fromTrusted: false });
  assert.deepEqual([open.release, open.exposures], ['admitted', ['untrusted-registry']]);
  assert.equal(at({ fromTrusted: false, verifySig: false }).release, 'denied-registry');
  /* a docker.io image never carries our CI signature, even with the allow-list off */
  assert.equal(at({ vapRegistry: false, fromTrusted: false }).release, 'denied-signature');
  /* signed but vulnerable: the signature does not stop it */
  const vuln = at({ scanGate: false, scanClean: false });
  assert.deepEqual([vuln.release, vuln.sigValid, vuln.criticalCves, vuln.exposures], ['admitted', true, 1, ['critical-cve']]);
  /* the gate stops the release before push + sign; the previous digest keeps serving */
  const gate = at({ scanClean: false });
  assert.deepEqual([gate.release, gate.pushed, gate.runningDigest], ['blocked-in-ci', false, S.SC_DIGEST.prev]);
  /* allow-list passes a laptop push; only signature verification catches it */
  assert.deepEqual(at({ signed: false, verifySig: false }).exposures, ['unsigned-image']);
  assert.equal(at({ signed: false }).release, 'denied-signature');
  assert.equal(at({ pinnedDigest: false }).image, TAG);
  assert.match(at({}).image, /^registry\.example\.com\/payments\/api@sha256:[0-9a-f]{64}$/);
  for (const d of Object.values(S.SC_DIGEST)) assert.match(d, /^sha256:[0-9a-f]{64}$/);
  assert.notEqual(at({ scanGate: false, scanClean: false }).digest, at({}).digest, 'a different build is a different digest');
  assert.equal(v({ vapRegistry: false, verifySig: false, fromTrusted: false }), 'exposed');
  assert.equal(v({ fromTrusted: false }), 'rejected');
  assert.equal(v({ pinnedDigest: false }), 'degraded');
  assert.equal(v({ scanGate: false }), 'degraded', 'a missing control is a gap even when nothing bad shipped');
  assert.equal(v({ scanGate: false, scanClean: false }), 'exposed');
  assert.equal(v({ scanClean: false }), 'rejected');
  /* checkpoints */
  const pre = sim.scenarios.filter(sc => sc.predict);
  assert.equal(pre.length, 7);
  assert.equal(new Set(pre.map(sc => sc.predict.answer)).size, 3, 'keyed answers spread across positions 0-2');
  for (const sc of pre) {
    assert.notEqual(sim.derive(S.merge(sim.initial, sc.set)).verdict, 'healthy', sc.id + ' breaks something');
    assert.ok(sc.predict.why.length > 200, sc.id + ' explains the mechanism');
  }
  assert.match(sim.scenarios.find(s => s.id === 'untrusted-registry').predict.why, /trailing slash/);
  assert.match(sim.scenarios.find(s => s.id === 'critical-cve').predict.why, /--ignore-unfixed/);
});

test('allowed-registries: docker.io running → VAP applied (running pods untouched) → digest rollback → docker.io denied with the documented message; 5/5', () => {
  const s = session('allowed-registries');
  assert.equal(s.verdict(), 'exposed');
  assert.ok(s.run('kubectl get deployment payments-api -n payments -o wide').out[1].includes('docker.io/payments-tools/api:latest'));
  const pol = s.run('cat allowed-registries.yaml').out.join('\n');
  assert.match(pol, /kind: ValidatingAdmissionPolicy\n/);
  assert.match(pol, /c\.image\.startsWith\('registry\.example\.com\/'\)/);
  assert.match(pol, /validationActions: \[Deny\]/);
  const ap = s.run('kubectl apply -f allowed-registries.yaml');
  assert.deepEqual(ap.out.slice(0, 2), ['validatingadmissionpolicy.admissionregistration.k8s.io/allowed-registries created', 'validatingadmissionpolicybinding.admissionregistration.k8s.io/allowed-registries-binding created']);
  assert.match(ap.out[2], /running docker\.io pods keep running/);
  assert.ok(s.run('kubectl get validatingadmissionpolicybindings').out.some(l => /^allowed-registries-binding\s+allowed-registries\s/.test(l)));
  s.run('kubectl apply -f payments-api-digest.yaml');
  assert.deepEqual([s.state.fromTrusted, s.state.pinnedDigest], [true, true]);
  const den = s.run('kubectl apply -f payments-api-dockerio.yaml');
  assert.equal(den.exit, 1);
  assert.equal(den.out[0], 'The deployments "payments-api" is invalid: : ValidatingAdmissionPolicy \'allowed-registries\' with binding \'allowed-registries-binding\' denied request: images must come from registry.example.com/');
  assert.equal(s.state.fromTrusted, true, 'the denied write changed nothing');
  assert.equal(s.run('kubectl set image deployment/payments-api api=docker.io/library/nginx:1.27 -n payments').exit, 1);
  assert.equal(s.status().total, 5);
  assert.equal(s.status().done, true);
});

test('scan-gate: report-only trivy → --exit-code 1 via sed → job stops before push/sign → distroless base → clean release; 6/6', () => {
  const s = session('scan-gate');
  assert.equal(s.verdict(), 'exposed');
  const scan = s.run('trivy image --severity CRITICAL ' + TAG);
  assert.equal(scan.exit, 0, 'trivy exits 0 by default even with findings');
  assert.ok(scan.out.some(l => /^zlib1g\s+CVE-2023-45853\s+CRITICAL\s+will_not_fix/.test(l)));
  assert.equal(s.run('trivy image --severity CRITICAL --exit-code 1 ' + TAG).exit, 1);
  const hid = s.run('trivy image --severity CRITICAL --exit-code 1 --ignore-unfixed ' + TAG);
  assert.equal(hid.exit, 0);
  assert.match(hid.out.join(' '), /--ignore-unfixed hid CVE-2023-45853/);
  assert.ok(s.run('cat ci/build.sh').out.includes('trivy image --severity CRITICAL "$IMAGE"'));
  assert.match(s.run("sed -i 's|--severity CRITICAL|--severity CRITICAL --ignore-unfixed --exit-code 1|' ci/build.sh").out[0], /would let CVE-2023-45853/);
  assert.equal(s.state.scanGate, false);
  s.run("sed -i 's|--severity CRITICAL|--severity CRITICAL --exit-code 1|' ci/build.sh");
  assert.equal(s.state.scanGate, true);
  const blocked = s.run('./ci/build.sh');
  assert.equal(blocked.exit, 1);
  assert.ok(!blocked.out.some(l => /docker push|cosign sign/.test(l)), 'nothing pushed or signed');
  assert.equal(s.verdict(), 'rejected');
  assert.match(s.run("sed -i 's|debian:bookworm-20230904|ubuntu:24.04|' Dockerfile").out[0], /minimal base/);
  s.run("sed -i 's|debian:bookworm-20230904|gcr.io/distroless/static-debian12:nonroot|' Dockerfile");
  assert.ok(s.run('cat Dockerfile').out.includes('FROM gcr.io/distroless/static-debian12:nonroot'));
  const ok = s.run('bash ci/build.sh');
  assert.equal(ok.exit, 0);
  assert.ok(ok.out.some(l => l === 'released registry.example.com/payments/api@' + S.SC_DIGEST.good));
  assert.equal(s.verdict(), 'healthy');
  assert.equal(s.status().total, 6);
  assert.equal(s.status().done, true);
});

test('report-only pipeline signs a vulnerable digest — and says so', () => {
  const s = session(null, { scanGate: false, scanClean: false, signed: false, verifySig: false });
  const r = s.run('./ci/build.sh');
  assert.equal(r.exit, 0);
  assert.match(r.out.join('\n'), /a report is not a gate; the vulnerable digest is now signed/);
  assert.equal(s.state.signed, true);
  assert.equal(s.verdict(), 'exposed');
  assert.match(s.run('cosign sign --key cosign.key ' + TAG).out.join(' '), /uses a tag, not a digest[\s\S]*CRITICAL CVE/);
});

test('sbom: CycloneDX from trivy, grep answers "is zlib in it?", trivy sbom scans without a pull, cosign attest + verify-attestation; 5/5', () => {
  const s = session('sbom');
  assert.match(s.run('cat sbom.cdx.json').out[0], /No such file/);
  assert.match(s.run('cosign verify-attestation --key cosign.pub --type cyclonedx ' + TAG).out[0], /no matching attestations/);
  s.run('trivy image --format cyclonedx --output sbom.cdx.json ' + TAG);
  assert.ok(s.run('ls').out[0].includes('sbom.cdx.json'));
  const doc = JSON.parse(s.run('cat sbom.cdx.json').out.join('\n'));
  assert.equal(doc.bomFormat, 'CycloneDX');
  assert.ok(doc.components.some(c => c.purl === 'pkg:golang/stdlib@v1.23.2'));
  const g = s.run('grep -i zlib sbom.cdx.json');
  assert.deepEqual([g.out, g.exit], [[], 1], 'distroless static carries no zlib1g');
  assert.match(s.run('trivy sbom sbom.cdx.json').out.join('\n'), /Total: 0 \(CRITICAL: 0\)/);
  const at = s.run('cosign attest --key cosign.key --type cyclonedx --predicate sbom.cdx.json registry.example.com/payments/api@' + S.SC_DIGEST.good);
  assert.ok(!/WARNING/.test(at.out[0]), 'a digest reference gets no tag warning');
  const ver = s.run('cosign verify-attestation --key cosign.pub --type cyclonedx ' + TAG);
  assert.equal(ver.exit, 0);
  assert.match(ver.out.join(' '), /predicateType https:\/\/cyclonedx\.org\/bom/);
  assert.equal(s.status().total, 5);
  assert.equal(s.status().done, true);
  /* the vulnerable base would answer "yes" */
  const v = session(null, { scanGate: false, scanClean: false });
  v.run('trivy image --format cyclonedx --output sbom.cdx.json ' + TAG);
  assert.equal(v.run('grep zlib1g sbom.cdx.json').exit, 0);
  assert.ok(v.run('trivy sbom sbom.cdx.json').out.some(l => /CVE-2023-45853/.test(l)));
});

test('sign-verify: no matching signatures → verifyImages enforced → restart denied → CI release → verified → digest pinned; 6/6', () => {
  const s = session('sign-verify');
  assert.equal(s.verdict(), 'exposed');
  assert.match(s.run('cosign verify ' + TAG).out[0], /--certificate-identity/, 'no --key means keyless mode');
  const nv = s.run('cosign verify --key cosign.pub ' + TAG);
  assert.deepEqual([nv.out[0], nv.exit], ['Error: no matching signatures', 1]);
  const kp = s.run('kubectl apply -f verify-images.yaml');
  assert.match(kp.out.join(' '), /Kyverno is not running here/);
  assert.match(s.run('kubectl get clusterpolicies').out[1], /^verify-payments-images\s+true/);
  const den = s.run('kubectl rollout restart deployment payments-api -n payments');
  assert.equal(den.exit, 1);
  assert.match(den.out.join('\n'), /failed to verify image registry\.example\.com\/payments\/api:2\.4\.1: \.attestors\[0\]\.entries\[0\]\.keys: no matching signatures/);
  assert.match(den.out.join('\n'), /representative Kyverno message/);
  s.run('./ci/build.sh');
  assert.equal(s.state.signed, true);
  const ok = s.run('cosign verify --key cosign.pub ' + TAG);
  assert.equal(ok.exit, 0);
  assert.equal(JSON.parse(ok.out[ok.out.length - 1])[0].critical.image['docker-manifest-digest'], S.SC_DIGEST.good);
  s.run('kubectl apply -f payments-api-digest.yaml');
  assert.ok(s.run('kubectl get deployment payments-api -n payments -o wide').out[1].includes('registry.example.com/payments/api@' + S.SC_DIGEST.good));
  assert.equal(s.verdict(), 'healthy');
  assert.equal(s.status().total, 6);
  assert.equal(s.status().done, true);
});

test('honesty: unmodelled trivy/cosign/kubectl forms never invent output; help and note say simulated', () => {
  const s = session();
  assert.equal(s.run('trivy fs .').exit, 2);
  assert.equal(s.run('cosign triangulate ' + TAG).exit, 2);
  assert.equal(s.run('kubectl get secrets -n payments').exit, 2);
  assert.equal(s.run('crane digest ' + TAG).exit, 127);
  const help = s.run('help').out.join('\n');
  assert.match(help, /Simulated shell/);
  assert.match(help, /no registry, no CI runner, no Kyverno/);
  assert.match(C.pack(SIM).note, /computed by the rules engine/);
});

test('CKS paper: Supply Chain Security now has evidence — 6/6 domains, 100% coverage, gap links to the new drill', () => {
  assert.ok(['1.4.0', '1.5.0', '1.6.0', '1.7.0', '1.8.0'].includes(E.VERSION));
  assert.equal(E.CKS_BLUEPRINT.find(b => b.domain === 'Supply Chain Security').sims[0], SIM, 'gap link stays on the supply-chain drill (cks-static-analysis joined the domain on 2026-11-05)');
  for (const sc of S.get(SIM).scenarios.filter(x => x.predict)) assert.equal(E.cksDomain(SIM, sc.id), 'Supply Chain Security');
  assert.ok(E.CKS_SIMS.includes(SIM));
  assert.equal(E.pool(S, 'CKS').filter(it => it.simId === SIM).length, 7);
  assert.ok(!E.pool(S).some(it => it.simId === SIM), 'the CKA paper never draws a CKS checkpoint');
  for (const seed of [1, 7, 42, 2026]) {
    const ex = E.buildExam(S, { track: 'CKS', seed });
    assert.equal(ex.count, 8);
    assert.equal(new Set(ex.items.map(i => i.domain)).size, 6, 'one item per official domain first (seed ' + seed + ')');
    assert.ok(ex.items.some(i => i.domain === 'Supply Chain Security' && [SIM, 'cks-static-analysis'].includes(i.simId)), 'Supply Chain drawn from its drills (cks-static-analysis joined on 2026-11-05)');
    assert.doesNotMatch(ex.honesty, /no drill yet/);
  }
  const ex2 = E.buildExam(S, { track: 'CKS', seed: 7 });
  ex2.items.forEach(it => { const miss = it.domain === 'Supply Chain Security'; it.choice = miss ? (it.answer + 1) % 3 : it.answer; it.correct = !miss; });
  const bp = E.summarize(ex2).blueprint;
  assert.equal(bp.coveragePct, 100);
  assert.deepEqual(bp.untested, []);
  assert.equal(bp.weakest.domain, 'Supply Chain Security');
  assert.deepEqual(bp.drill, { sim: SIM, href: '/immersive/#cks-supply-chain' });
});

test('review: supply-chain coach cards get an honest CKS label; CKA mastery stays CKA-only', () => {
  assert.match(R.VERSION, /^1\.3\.[23456]$/);
  const cards = R.cliCheckpoints(C, S).filter(c => c.simId === SIM);
  assert.equal(cards.length, 22);
  assert.ok(cards.every(c => c.domain === 'CKS · Supply chain security'));
  assert.ok(!R.checkpoints(S).some(c => c.simId === SIM));
});

test('wiring: /immersive/ host, exam lobby copy, curriculum rows, manifest (new scene, cks_coverage, pack, honest notes)', () => {
  const html = readFileSync(path.join(root, 'docs/immersive/index.html'), 'utf8');
  assert.match(html, /id="cks-supply-chain"/);
  assert.match(html, /data-il-sim="cks-supply-chain"\s*\n\s*data-gltf="\/assets\/immersive\/cks-supply-chain\.glb"/);
  assert.match(html, /there is no live cluster, registry, CI runner, Trivy, cosign or Kyverno/);
  const exam = readFileSync(path.join(root, 'docs/immersive/exam/index.html'), 'utf8');
  assert.match(exam, /every domain now has a drill/);
  assert.doesNotMatch(exam, /has no drill yet/);
  for (const f of ['labs.json', 'mirror.json']) {
    const j = JSON.parse(readFileSync(path.join(root, 'docs/curriculum-os', f), 'utf8'));
    const row = (j.items || j.labs).find(l => l.id === 'lab-sim-cks-supply-chain');
    assert.ok(row, f);
    assert.equal(row.gltf, S.get(SIM).glb);
    assert.equal(row.immersive.sim, SIM);
    assert.equal(row.immersive.mode, '3d-first');
    assert.match(row.summary, /no live cluster, registry or CI runner/);
  }
  const m = JSON.parse(readFileSync(path.join(root, 'docs/assets/scenes/manifest.json'), 'utf8'));
  const sc = m.scenes.find(x => x.sim === SIM);
  assert.deepEqual([sc.gltf, sc.cert, sc.polish, sc.polishedOn], [S.get(SIM).glb, 'CKS', 'blender-cli', '2026-11-02']);
  assert.ok(m.sims.list.includes(SIM));
  assert.ok(!m.cka_coverage.interactive.includes(SIM), 'not counted as CKA coverage');
  assert.deepEqual(m.cks_coverage.interactive.slice(0, 2), ['cks-pod-security', SIM]);
  assert.match(m.cks_coverage.covered['Supply Chain Security'], /cks-supply-chain/);
  assert.ok(!m.cks_coverage.notCovered.some(x => /^Supply Chain Security/.test(x)));
  assert.ok(m.cks_coverage.notCovered.some(x => /kube-bench/.test(x)), 'kube-bench still honestly missing (Falco/AppArmor drilled since 2026-11-03)');
  assert.equal(m.cks_coverage.hostedFleet, false);
  assert.equal(m.cks_coverage.liveUnrealHost, false);
  assert.equal(m.sims.runtime_version, S.VERSION);
  assert.equal(m.sims.exam.version, E.VERSION);
  assert.equal(m.sims.cli.version, C.VERSION);
  assert.deepEqual(m.sims.cli.packs.find(p => p.sim === SIM).tasks, ['allowed-registries', 'scan-gate', 'sbom', 'sign-verify']);
  assert.match(m.sims.cli.supplyChainNote, /No registry, no CI runner, no real trivy, cosign, Rekor or Kyverno, no clock/);
});

test('voice: "co sign" and "s bom" normalise to real syntax', () => {
  assert.match(C.fromSpeech('co sign verify dash dash key co sign dot pub ' + TAG, SIM).line || '', /^cosign verify --key cosign\.pub/);
  assert.match(C.fromSpeech('trivy s bom s bom dot cdx dot json', SIM).line || '', /^trivy sbom sbom\.cdx\.json$/);
});
