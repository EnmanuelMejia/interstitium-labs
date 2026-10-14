/** Immersive 3D browser check (2026-10-06; +4 CKA sims & shuffled options 2026-10-07; +6 CKA drills, keyed answers by index 2026-10-08; +remediation loop 2026-10-13; +WebXR entry 2026-10-14): authored .glb really renders, LOD1 skipped, sims change the scene.
 * npm run test:immersive:browser   — disposable headless Chromium, local static server, no network writes.
 */
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFile, stat, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { chromium } from 'playwright';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const docs = path.join(root, 'docs');
const shots = path.join(root, 'deploy-shots');
await mkdir(shots, { recursive: true });
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.glb': 'model/gltf-binary' };
const server = createServer(async (req, res) => {
  try {
    let target = path.resolve(docs, '.' + decodeURIComponent(new URL(req.url, 'http://x').pathname));
    if (!target.startsWith(docs)) { res.writeHead(403); return res.end(); }
    if ((await stat(target)).isDirectory()) target = path.join(target, 'index.html');
    res.writeHead(200, { 'Content-Type': MIME[path.extname(target)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    res.end(await readFile(target));
  } catch { res.writeHead(404); res.end('nf'); }
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = 'http://127.0.0.1:' + server.address().port;
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.abort());
let failed = 0;
async function check(name, fn) {
  try { const d = await fn(); console.log('PASS ' + name + (d ? ' — ' + d : '')); }
  catch (e) { failed++; console.error('FAIL ' + name + ': ' + e.message); }
}
async function open(p) {
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(base + p, { waitUntil: 'load' });
  return { page, errors };
}
const waitAuthored = (page, n) => page.waitForFunction(k => document.querySelectorAll('.il-immersive__badge[data-il-mesh="authored"]').length >= k, n, { timeout: 30000 });

await check('/immersive/: every authored-glb stage renders authored meshes; WebGL contexts stay under the browser cap', async () => {
  const { page, errors } = await open('/immersive/');
  const warnings = [];
  page.on('console', m => { if (/Too many active WebGL contexts/.test(m.text())) warnings.push(m.text()); });
  const hosts = page.locator('[data-gltf$=".glb"]');
  const want = await hosts.count();
  let maxAwake = 0;
  for (let i = 0; i < want; i++) {
    const h = hosts.nth(i);
    await h.scrollIntoViewIfNeeded();
    await h.locator('.il-immersive__badge[data-il-mesh="authored"]').waitFor({ timeout: 30000 });
    maxAwake = Math.max(maxAwake, await page.evaluate(() => document.querySelectorAll('[data-il-gl="awake"]').length));
  }
  const info = await page.evaluate(() => ({
    authored: document.querySelectorAll('.il-immersive__badge[data-il-mesh="authored"]').length,
    delegated: document.querySelectorAll('[data-il-delegated="immersive-3d"]').length,
    lies: [...document.querySelectorAll('[data-imm-engine]')].filter(e => /Three\/glTF/.test(e.textContent)).length,
    lodCaps: [...document.querySelectorAll('.il-immersive__captions')].filter(c => /LOD1 skipped/.test(c.textContent)).length,
    uniqueGlb: new Set([...document.querySelectorAll('[data-gltf]')].map(h => h.getAttribute('data-gltf'))).size,
    psGltf: document.querySelectorAll('[data-engine="unreal"][data-gltf]').length
  }));
  assert.equal(info.authored, want, 'authored stages');
  assert.equal(info.delegated, 4, 'grid stages delegated');
  assert.equal(info.lies, 0, 'no "Three/glTF" label on procedural stages');
  assert.ok(info.lodCaps >= 10, 'LOD1 skip reported in captions');
  assert.ok(info.uniqueGlb >= 15, 'curriculum-sync must not collapse hosts onto one .glb (got ' + info.uniqueGlb + ')');
  assert.equal(info.psGltf, 0, 'Unreal PS stub must not be stamped with a glTF');
  assert.ok(maxAwake <= 10, 'awake contexts ' + maxAwake);
  assert.deepEqual(warnings, [], 'context-cap warnings');
  assert.deepEqual(errors, []);
  await page.close();
  return `${info.authored}/${want} authored · ${info.delegated} delegated · ${info.uniqueGlb} distinct glb · max ${maxAwake} live contexts`;
});

for (const [sim, scenario, expectVerdict] of [['aws-az-failure', 'single-az-db', 'down'], ['iam-eval', 'deny-wins', 'explicit-deny'], ['etcd-quorum', 'lose-two', 'down'],
  ['netpol-isolation', 'flannel', 'down'], ['rbac-authz', 'clusterrole-rb', 'degraded'], ['sched-taints', 'untaint', 'healthy'], ['hpa-scale', 'cap', 'degraded'],
  ['storage-csi', 'reclaim-retain', 'released'], ['ingress-routing', 'no-endpoints', 'degraded'], ['config-propagation', 'missing-key', 'down'],
  ['cni-network', 'no-cni', 'down'], ['mesh-mtls', 'strict-plain', 'down'], ['control-plane-failure', 'api-down', 'down']]) {
  await check(`sim ${sim}: predict → reveal changes scene state (${scenario} → ${expectVerdict})`, async () => {
    const { page, errors } = await open('/immersive/');
    await page.locator(`[data-il-sim="${sim}"]`).scrollIntoViewIfNeeded();
    const host = page.locator(`[data-il-sim-ready="${sim}"]`);
    await host.waitFor({ timeout: 30000 });
    const before = await host.getAttribute('data-il-sim-verdict');
    await host.locator(`[data-il-sim-scenario="${scenario}"]`).click();
    assert.equal(await host.getAttribute('data-il-sim-verdict'), before, 'scene must not change before the prediction');
    /* Click the keyed answer by its original index (answers are no longer always option 0). */
    const key = await page.evaluate(([id, scId]) => window.ILImmersiveSims.get(id).scenarios.find(x => x.id === scId).predict.answer, [sim, scenario]);
    await host.locator(`[data-il-sim-option="${key}"]`).click();
    assert.equal(await host.getAttribute('data-il-sim-verdict'), expectVerdict);
    const res = await host.locator('.il-immersive__sim-result').textContent();
    assert.match(res, /^Correct\./);
    const stored = await page.evaluate(() => JSON.parse(localStorage.getItem('il.immersiveSims.v1') || '{}'));
    assert.equal(stored[sim].correct, 1);
    await host.scrollIntoViewIfNeeded();
    await page.waitForTimeout(900);
    await host.screenshot({ path: path.join(shots, `immersive-sim-${sim}.png`) });
    assert.deepEqual(errors, []);
    await page.close();
    return `${before} → ${expectVerdict}`;
  });
}

await check('AZ toggle: lose us-east-1a with Multi-AZ → degraded + ASG surge revealed', async () => {
  const { page } = await open('/immersive/');
  await page.locator('[data-il-sim="aws-az-failure"]').scrollIntoViewIfNeeded();
  const host = page.locator('[data-il-sim-ready="aws-az-failure"]');
  await host.waitFor({ timeout: 30000 });
  await host.locator('[data-il-sim-toggle="azA"]').click();
  assert.equal(await host.getAttribute('data-il-sim-verdict'), 'degraded');
  const shown = await page.evaluate(() => {
    const el = document.querySelector('[data-il-sim-ready="aws-az-failure"]');
    return el._ilImmersive._authored.filter(v => /^sim-az-b-ec2-surge-\d$/.test(v.name) && v.simStyle && !v.simStyle.hide).length;
  });
  assert.equal(shown, 2);
  await page.close();
  return 'surge nodes visible: ' + shown;
});

await check('RBAC toggle: RoleBinding → ClusterRoleBinding grants cluster-scoped nodes → allow', async () => {
  const { page } = await open('/immersive/');
  await page.locator('[data-il-sim="rbac-authz"]').scrollIntoViewIfNeeded();
  const host = page.locator('[data-il-sim-ready="rbac-authz"]');
  await host.waitFor({ timeout: 30000 });
  assert.equal(await host.getAttribute('data-il-sim-verdict'), 'degraded');
  await host.locator('[data-il-sim-toggle="b2Cluster"]').click();
  assert.equal(await host.getAttribute('data-il-sim-verdict'), 'allow');
  const order = await host.evaluate(el => { el.querySelector('[data-il-sim-scenario="wrong-ns"]').click(); return [...el.querySelectorAll('[data-il-sim-option]')].map(b => b.getAttribute('data-il-sim-option')).join(''); });
  assert.equal([...order].sort().join(''), '012', 'options are a permutation of original indices');
  await page.close();
  return 'degraded → allow · option order ' + order;
});

await check('Storage toggle: delete a PVC still mounted → Terminating (pvc-protection), pod keeps I/O', async () => {
  const { page, errors } = await open('/immersive/');
  await page.locator('[data-il-sim="storage-csi"]').scrollIntoViewIfNeeded();
  const host = page.locator('[data-il-sim-ready="storage-csi"]');
  await host.waitFor({ timeout: 30000 });
  assert.equal(await host.getAttribute('data-il-sim-verdict'), 'healthy');
  await host.locator('[data-il-sim-toggle="pvcDeleted"]').click();
  assert.equal(await host.getAttribute('data-il-sim-verdict'), 'terminating');
  const st = await host.evaluate(el => { const a = el._ilImmersive._authored; const f = n => a.find(v => v.name === n).simStyle; return { pvc: f('pvc-1').hide, bead: f('io-bead-0').hide, pv: f('pv-1').hide }; });
  assert.deepEqual(st, { pvc: false, bead: false, pv: false });
  await host.locator('[data-il-sim-toggle="podDeleted"]').click();
  assert.equal(await host.getAttribute('data-il-sim-verdict'), 'data-deleted', 'pod gone → reclaim Delete runs');
  assert.equal(await host.evaluate(el => el._ilImmersive._authored.find(v => v.name === 'pv-1').simStyle.hide), true);
  assert.deepEqual(errors, []);
  await page.close();
  return 'healthy → terminating → data-deleted';
});

await check('Mesh toggle: pods pre-date the injection label → sidecar-0 hidden; STRICT rejects; PERMISSIVE accepts plaintext', async () => {
  const { page, errors } = await open('/immersive/');
  await page.locator('[data-il-sim="mesh-mtls"]').scrollIntoViewIfNeeded();
  const host = page.locator('[data-il-sim-ready="mesh-mtls"]');
  await host.waitFor({ timeout: 30000 });
  const sidecarHidden = () => host.evaluate(el => el._ilImmersive._authored.filter(v => v.name === 'sidecar-0').every(v => v.simStyle && v.simStyle.hide));
  assert.equal(await sidecarHidden(), false);
  await host.locator('[data-il-sim-toggle="restarted"]').click();
  assert.equal(await sidecarHidden(), true);
  assert.equal(await host.getAttribute('data-il-sim-verdict'), 'down');
  await host.locator('[data-il-sim-toggle="strict"]').click();
  assert.equal(await host.getAttribute('data-il-sim-verdict'), 'degraded');
  assert.match(await host.locator('.il-immersive__captions').first().textContent(), /plaintext accepted/);
  assert.deepEqual(errors, []);
  await page.close();
  return 'sidecar hidden · STRICT down → PERMISSIVE degraded';
});

await check('Ingress + CNI + control-plane toggles re-derive the authored scene', async () => {
  const { page, errors } = await open('/immersive/');
  const out = [];
  for (const [sim, toggle, want] of [['ingress-routing', 'controller', 'down'], ['ingress-routing', 'controller', 'healthy'], ['ingress-routing', 'apiExact', 'degraded'],
    ['cni-network', 'kubeProxy', 'degraded'], ['config-propagation', 'encryptAtRest', 'healthy'], ['control-plane-failure', 'cmUp', 'degraded']]) {
    await page.locator(`[data-il-sim="${sim}"]`).scrollIntoViewIfNeeded();
    const host = page.locator(`[data-il-sim-ready="${sim}"]`);
    await host.waitFor({ timeout: 30000 });
    await host.locator(`[data-il-sim-toggle="${toggle}"]`).click();
    assert.equal(await host.getAttribute('data-il-sim-verdict'), want, sim + ' ' + toggle);
    out.push(sim + ':' + toggle + '→' + want);
  }
  const simHosts = page.locator('[data-il-sim]');
  const nSims = await simHosts.count();
  const matched = [];
  for (let i = 0; i < nSims; i++) {
    const h = simHosts.nth(i);
    await h.scrollIntoViewIfNeeded();
    const id = await h.getAttribute('data-il-sim');
    await page.locator(`[data-il-sim-ready="${id}"]`).waitFor({ timeout: 30000 });
    /* Off-screen stages release their WebGL context (v1.4.0) and drop _authored; wait for the
     * wake → re-upload → sim re-apply cycle instead of reading a sleeping stage. */
    await h.evaluate(el => new Promise((ok, no) => {
      const t0 = Date.now();
      (function poll() {
        if ((el._ilImmersive._authored || []).length) return ok();
        if (Date.now() - t0 > 30000) return no(new Error('stage never re-uploaded after wake'));
        setTimeout(poll, 100);
      })();
    }));
    const n = await h.evaluate(el => (el._ilImmersive._authored || []).filter(v => v.simStyle && v.simStyle.matched).length);
    assert.ok(n > 0, id + ' rules hit authored nodes');
    assert.match(await h.locator('.il-immersive__captions').first().textContent(), /sim \(rules engine, not a live system\) · authored \.glb \(\d+ nodes/, id + ' caption keeps glTF provenance');
    matched.push(id);
  }
  assert.ok(matched.length >= 13, 'sims mounted: ' + matched.length);
  assert.deepEqual(errors, []);
  await page.close();
  return out.join(' · ') + ' · ' + matched.length + ' sims mounted';
});

/* 2026-10-12 merge with main: /learn/ and the AWS/CKA path heroes were deleted in the
 * Oct 10-11 nav simplification and now 301 → /topics/ (+ /topics/cloud-devops/). The
 * immersive suite above already covers authored glTF + all 13 sims on /immersive/.
 * Keep a smoke check that the worker redirect map still names those legacy URLs. */
await check('legacy learn/path URLs remain redirected in worker (nav simplification)', async () => {
  const worker = await readFile(path.join(docs, '_worker.js'), 'utf8');
  for (const [from, to] of [['/learn', '/topics/'], ['/paths/aws-cloud-ops', '/topics/cloud-devops/'],
    ['/paths/aws-cloud-practitioner-plus', '/topics/cloud-devops/'], ['/paths/k8s-cka-exceed', '/topics/cloud-devops/']]) {
    const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    assert.match(worker, new RegExp('"' + esc(from) + '"\\s*:\\s*"' + esc(to) + '"'), from + ' → ' + to);
  }
  return '4 legacy redirects intact';
});

await check('/immersive/exam/: lobby lists pool and a paper can be started', async () => {
  const { page, errors } = await open('/immersive/exam/');
  const pool = await page.locator('[data-il-exam-pool]').textContent();
  assert.ok(Number(pool) >= 40, 'pool ' + pool);
  await page.locator('[data-il-exam-start]').first().click();
  await page.locator('[data-il-exam-run]:not([hidden])').waitFor({ timeout: 15000 });
  await page.locator('[data-il-exam-option]').first().waitFor({ timeout: 30000 });
  // Answer with whatever option 0 is on screen — just prove commit advances or scores.
  const before = await page.locator('[data-il-exam-progress]').textContent();
  await page.locator('[data-il-exam-option]').first().click();
  await page.waitForTimeout(1600);
  const after = await page.locator('[data-il-exam-progress]').textContent();
  const finished = await page.locator('html').getAttribute('data-il-exam-finished');
  assert.ok(after !== before || finished, 'exam progressed or finished');
  assert.deepEqual(errors, []);
  await page.close();
  return 'pool ' + pool + ' · ' + before + ' → ' + (after || finished);
});

/* 2026-10-13 adaptive remediation loop: drills + exam papers feed an on-device SR queue that re-serves the 3D checkpoint. */
const keyFor = (page, qText) => page.evaluate((q) => {
  const S = window.ILImmersiveSims;
  for (const id of S.list()) for (const sc of S.get(id).scenarios) if (sc.predict && sc.predict.q === q) return { sim: id, sc: sc.id, answer: sc.predict.answer, n: sc.predict.options.length };
  return null;
}, qText);

await check('/immersive/: a free-play CKA drill miss lands in the review queue (box 0, due now) and the badge updates', async () => {
  const { page, errors } = await open('/immersive/');
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: 'load' });
  await page.locator('[data-il-sim="etcd-quorum"]').scrollIntoViewIfNeeded();
  const host = page.locator('[data-il-sim-ready="etcd-quorum"]');
  await host.waitFor({ timeout: 30000 });
  await host.locator('[data-il-sim-scenario="lose-two"]').click();
  const key = await page.evaluate(() => window.ILImmersiveSims.get('etcd-quorum').scenarios.find(x => x.id === 'lose-two').predict.answer);
  const wrong = (key + 1) % 2;
  await host.locator(`[data-il-sim-option="${wrong}"]`).click();
  const card = await page.evaluate(() => JSON.parse(localStorage.getItem('il.immersiveReview.v1')).cards['etcd-quorum::lose-two']);
  assert.equal(card.box, 0);
  assert.equal(card.lapses, 1);
  assert.equal(card.src.drill, 1);
  await page.waitForFunction(() => /1 due now/.test(document.querySelector('[data-il-review-due-badge]').textContent), null, { timeout: 5000 });
  /* AWS / mesh drills stay out of the CKA queue. */
  await page.locator('[data-il-sim="iam-eval"]').scrollIntoViewIfNeeded();
  const iam = page.locator('[data-il-sim-ready="iam-eval"]');
  await iam.waitFor({ timeout: 30000 });
  await iam.locator('[data-il-sim-scenario="deny-wins"]').click();
  await iam.locator('[data-il-sim-option="0"]').click();
  const n = await page.evaluate(() => Object.keys(JSON.parse(localStorage.getItem('il.immersiveReview.v1')).cards).length);
  assert.equal(n, 1, 'IAM drill not in CKA queue');
  assert.deepEqual(errors, []);
  await page.close();
  return 'etcd-quorum::lose-two box 0 · badge "1 due now" · AWS excluded';
});

await check('exam → remediation → 3D review: missed paper items are re-served on the authored scene, then rescheduled', async () => {
  const { page, errors } = await open('/immersive/exam/');
  let step = 'exam', total = 0, boxes = [];
  try {
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: 'load' });
  await page.locator('[data-il-exam-start][data-count="5"]').click();
  await page.locator('[data-il-exam-run]:not([hidden])').waitFor({ timeout: 15000 });
  for (let i = 0; i < 5; i++) {
    await page.waitForFunction(n => document.querySelector('[data-il-exam-progress]').textContent === 'Q ' + n + '/5', i + 1, { timeout: 30000 });
    await page.locator('[data-il-exam-option]').first().waitFor({ timeout: 30000 });
    const k = await keyFor(page, await page.locator('[data-il-exam-q]').textContent());
    assert.ok(k, 'question maps to a sim scenario');
    /* Answer wrong on purpose: every item should come back as a relearn card. */
    step = 'exam Q' + (i + 1);
    await page.locator(`[data-il-exam-option="${(k.answer + 1) % k.n}"]`).click();
  }
  await page.locator('[data-il-exam-done]:not([hidden])').waitFor({ timeout: 15000 });
  assert.equal(await page.locator('[data-il-exam-remediate]').getAttribute('data-lapses'), '5');
  assert.match(await page.locator('[data-il-exam-remediate]').textContent(), /5 checkpoints scheduled on this device · 5 to relearn now/);
  assert.match(await page.locator('[data-il-exam-adaptive-note]').textContent(), /weakest on-device domains: /);
  await page.locator('[data-il-exam-remediate-link]').click();
  await page.waitForURL(/\/immersive\/review\/$/);
  await page.locator('[data-il-review-due]').waitFor();
  assert.equal(await page.locator('[data-il-review-due]').textContent(), '5');
  assert.equal(await page.locator('[data-il-review-exams]').textContent(), '1');
  assert.match(await page.locator('[data-il-review-plan]').textContent(), /5 relearn \(missed\)/);
  assert.ok(await page.locator('[data-il-review-mastery] tbody tr').count() >= 7, 'mastery rows');
  step = 'review start';
  await page.locator('[data-il-review-start]').click();
  await page.locator('[data-il-review-run]:not([hidden])').waitFor({ timeout: 15000 });
  assert.match(await page.locator('[data-il-review-reason]').textContent(), /Relearn — missed 1× \(incl\. timed exam\)/);
  const stage = page.locator('[data-il-review-stage]');
  const k0 = await keyFor(page, await page.locator('[data-il-review-q]').textContent());
  await page.waitForFunction(id => document.querySelector('[data-il-review-stage]').getAttribute('data-il-sim-ready') === id, k0.sim, { timeout: 30000 });
  await stage.locator('.il-immersive__badge[data-il-mesh="authored"]').waitFor({ timeout: 30000 });
  const before = await stage.getAttribute('data-il-sim-verdict');
  await page.locator(`[data-il-review-option="${k0.answer}"]`).click();
  const fb = await page.locator('[data-il-review-feedback]').textContent();
  assert.match(fb, /^Correct\. .* Box 0 → 1\. Next review in 10 min\.$/);
  const after = await stage.getAttribute('data-il-sim-verdict');
  const expected = await page.evaluate(([id, sc]) => { const S = window.ILImmersiveSims, sim = S.get(id); return sim.derive(S.merge(sim.initial, sim.scenarios.find(x => x.id === sc).set)).verdict; }, [k0.sim, k0.sc]);
  assert.equal(after, expected, 'reveal re-derived the authored scene');
  await page.waitForTimeout(700);
  await stage.screenshot({ path: path.join(shots, 'immersive-review-card.png') });
  /* Queue = 5 relearn cards first, then weak-domain top-ups up to the 10-card session. */
  total = Number((await page.locator('[data-il-review-progress]').textContent()).split('/')[1]);
  assert.ok(total >= 5 && total <= 10, 'session size ' + total);
  for (let i = 1; i < total; i++) {
    step = 'review card ' + (i + 1);
    if (i === 5) assert.match(await page.locator('[data-il-review-reason]').textContent(), /Relearn/);
    await page.locator('[data-il-review-next-card]:not([hidden])').click();
    await page.waitForFunction(([n, t]) => document.querySelector('[data-il-review-progress]').textContent === 'Card ' + n + '/' + t, [i + 1, total], { timeout: 30000 });
    if (i >= 5) assert.match(await page.locator('[data-il-review-reason]').textContent(), /^New · (weak|untested) domain: /);
    await page.locator('[data-il-review-option]').first().waitFor({ timeout: 30000 });
    const k = await keyFor(page, await page.locator('[data-il-review-q]').textContent());
    await page.locator(`[data-il-review-option="${i === 4 ? (k.answer + 1) % k.n : k.answer}"]`).click();
  }
  await page.locator('[data-il-review-next-card]:not([hidden])').click();
  await page.locator('[data-il-review-done]:not([hidden])').waitFor({ timeout: 10000 });
  assert.equal(await page.locator('html').getAttribute('data-il-review-finished'), (total - 1) + '/' + total);
  const db = await page.evaluate(() => JSON.parse(localStorage.getItem('il.immersiveReview.v1')));
  const fromExam = Object.values(db.cards).filter(c => c.src.exam);
  boxes = fromExam.map(c => c.box).sort();
  assert.deepEqual(boxes, [0, 1, 1, 1, 1], 'four exam misses promoted to the 10-min step, one back to relearn');
  assert.ok(Object.values(db.cards).filter(c => !c.src.exam).every(c => c.box === 1 && c.src.review === 1), 'new top-up cards start at the 10-min step');
  assert.ok(Object.values(db.cards).every(c => !c.src.drill), 'exam/review stages never double-count as free-play drills');
  await page.locator('[data-il-review-again]').click();
  assert.equal(await page.locator('[data-il-review-due]').textContent(), '1');
  step = 'adaptive paper';
  await page.goto(base + '/immersive/exam/', { waitUntil: 'load' });
  await page.locator('[data-il-exam-start][data-adaptive="1"]').click();
  await page.locator('[data-il-exam-run]:not([hidden])').waitFor({ timeout: 15000 });
  assert.equal(await page.locator('html').getAttribute('data-il-exam-adaptive'), '1', 'adaptive paper used on-device focus');
  assert.deepEqual(errors, []);
  } catch (e) { e.message = '[' + step + '] ' + e.message; throw e; }
  await page.close();
  return 'paper 0/5 → 5 relearn → review ' + (total - 1) + '/' + total + ' → exam-card boxes ' + boxes.join(',') + ' · adaptive paper focused';
});

/* 2026-10-14 WebXR entry. Headless Chromium has no XR device, so the session is a scripted fake
 * (navigator.xr + XRWebGLLayer with framebuffer = null → frames draw into the real canvas via the
 * real WebGL context). This proves wiring + stereo render path + restore; it is NOT a headset demo. */
const XR_FAKE = () => {
  const frames = [];
  const persp = (aspect) => { const f = 1 / Math.tan(Math.PI / 4), n = 0.05, fa = 40, nf = 1 / (n - fa);
    return new Float32Array([f / aspect, 0, 0, 0, 0, f, 0, 0, 0, 0, (fa + n) * nf, -1, 0, 0, 2 * fa * n * nf, 0]); };
  const eye = (x) => new Float32Array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, -x, 0, 0, 1]);
  class FakeSession extends EventTarget {
    constructor(mode) { super(); this.mode = mode; this.environmentBlendMode = mode === 'immersive-ar' ? 'alpha-blend' : 'opaque'; this._t = new Set(); this.refAsked = []; }
    updateRenderState(s) { this.renderState = s; }
    requestReferenceSpace(t) { this.refAsked.push(t); return t === 'local-floor' ? Promise.reject(new DOMException('no floor', 'NotSupportedError')) : Promise.resolve({ type: t }); }
    requestAnimationFrame(cb) {
      const id = setTimeout(() => { this._t.delete(id); if (this.ended) return;
        const views = [{ eye: 'left', projectionMatrix: persp(1), transform: { inverse: { matrix: eye(-0.032) } } },
          { eye: 'right', projectionMatrix: persp(1), transform: { inverse: { matrix: eye(0.032) } } }];
        frames.push(views.length);
        cb(performance.now(), { session: this, getViewerPose: () => ({ views }) });
        /* Same task as the draw → drawing buffer not yet presented: count non-clear pixels per eye half. */
        const gl = window.__xr.gl;
        if (gl && this.mode === 'immersive-vr') {
          const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight, row = new Uint8Array(w * h * 4), lit = [0, 0];
          gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, row);
          for (let i = 0; i < w * h; i++) { const r = row[i * 4], g2 = row[i * 4 + 1], b = row[i * 4 + 2];
            if (Math.abs(r - 7) + Math.abs(g2 - 11) + Math.abs(b - 22) > 24) lit[(i % w) < w / 2 ? 0 : 1]++; }
          window.__xr.lit = lit;
        } }, 16);
      this._t.add(id); return id;
    }
    cancelAnimationFrame(id) { clearTimeout(id); }
    end() { if (this.ended) return Promise.resolve(); this.ended = true; this._t.forEach(clearTimeout);
      setTimeout(() => this.dispatchEvent(new Event('end')), 0); return Promise.resolve(); }
  }
  window.__xr = { frames, requests: [], compat: 0, layers: 0 };
  WebGLRenderingContext.prototype.makeXRCompatible = function () { window.__xr.compat++; return Promise.resolve(); };
  window.XRWebGLLayer = class { constructor(session, gl, opts) { window.__xr.layers++; window.__xr.gl = gl; this.opts = opts; this.framebuffer = null; this.w = gl.drawingBufferWidth; this.h = gl.drawingBufferHeight; }
    getViewport(v) { return { x: v.eye === 'left' ? 0 : Math.floor(this.w / 2), y: 0, width: Math.floor(this.w / 2), height: this.h }; } };
  Object.defineProperty(navigator, 'xr', { configurable: true, value: Object.assign(new EventTarget(), {
    isSessionSupported: (m) => Promise.resolve(m === 'immersive-vr' || m === 'immersive-ar'),
    requestSession: (mode, init) => { const s = new FakeSession(mode); if (init.domOverlay) s.domOverlayState = { type: 'screen' }; window.__xr.requests.push({ mode, req: [...(init.requiredFeatures || [])], opt: [...(init.optionalFeatures || [])], overlay: !!(init.domOverlay && init.domOverlay.root) }); window.__xr.session = s; return Promise.resolve(s); }
  }) });
};

async function xrContext(opts = {}, init) {
  const c = await browser.newContext({ viewport: { width: 1280, height: 900 }, ...opts });
  await c.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.abort());
  if (init) await c.addInitScript(init);
  return c;
}

await check('WebXR absent (no navigator.xr): no Enter VR/AR buttons on any stage', async () => {
  const c = await xrContext({}, () => { Object.defineProperty(Navigator.prototype, 'xr', { configurable: true, get: () => undefined }); });
  const page = await c.newPage(); const errors = []; page.on('pageerror', e => errors.push(String(e)));
  await page.goto(base + '/immersive/', { waitUntil: 'load' });
  await page.waitForFunction(() => { const r = [...document.querySelectorAll('.il-immersive[data-il-xr]')]; return r.length > 0 && r.every(x => x.getAttribute('data-il-xr') !== 'probing'); }, null, { timeout: 15000 });
  const info = await page.evaluate(() => ({
    stages: document.querySelectorAll('.il-immersive[data-il-xr]').length,
    unsupported: document.querySelectorAll('.il-immersive[data-il-xr="unsupported"][data-il-xr-support="no-webxr"]').length,
    visibleBtns: [...document.querySelectorAll('[data-il-xr-enter]')].filter(b => b.offsetParent !== null).length
  }));
  assert.ok(info.stages >= 13, 'stages probed ' + info.stages);
  assert.equal(info.unsupported, info.stages);
  assert.equal(info.visibleBtns, 0);
  assert.deepEqual(errors, []);
  await c.close();
  return `${info.stages} stages · all unsupported · 0 buttons`;
});

await check('WebXR supported but prefers-reduced-motion: no XR buttons (static fallback only)', async () => {
  const c = await xrContext({ reducedMotion: 'reduce' }, XR_FAKE);
  const page = await c.newPage();
  await page.goto(base + '/immersive/', { waitUntil: 'load' });
  await page.waitForTimeout(500);
  const n = await page.evaluate(() => ({ btns: document.querySelectorAll('[data-il-xr-enter]').length, reduced: document.querySelectorAll('.il-immersive.is-reduced').length }));
  assert.ok(n.reduced > 0, 'reduced stages');
  assert.equal(n.btns, 0);
  assert.equal(await page.evaluate(() => window.__xr.requests.length), 0);
  await c.close();
  return n.reduced + ' reduced stages · 0 buttons';
});

await check('WebXR mocked supported: Enter VR on an authored CKA sim → stereo XR frames → select re-tints → Exit restores 2D orbit', async () => {
  const c = await xrContext({}, XR_FAKE);
  const page = await c.newPage(); const errors = []; page.on('pageerror', e => errors.push(String(e)));
  await page.goto(base + '/immersive/', { waitUntil: 'load' });
  await page.locator('[data-il-sim="etcd-quorum"]').scrollIntoViewIfNeeded();
  const host = page.locator('[data-il-sim-ready="etcd-quorum"]');
  await host.waitFor({ timeout: 30000 });
  await host.locator('.il-immersive__badge[data-il-mesh="authored"]').waitFor({ timeout: 30000 });
  assert.equal(await host.getAttribute('data-il-xr'), 'available');
  assert.equal(await host.getAttribute('data-il-xr-support'), 'vr ar');
  const vr = host.locator('[data-il-xr-enter="vr"]'), ar = host.locator('[data-il-xr-enter="ar"]');
  assert.ok(await vr.isVisible() && await ar.isVisible(), 'both buttons visible');
  assert.equal(await vr.textContent(), 'Enter VR');
  assert.equal(await ar.textContent(), 'Enter AR');
  assert.match(await host.locator('.il-immersive__xr-note').textContent(), /authored glTF.*not Unreal Pixel Streaming.*no hosted cluster/);
  const visibleOnPage = await page.evaluate(() => document.querySelectorAll('.il-immersive[data-il-xr="available"]').length);
  assert.ok(visibleOnPage >= 13, 'every stage got the entry: ' + visibleOnPage);
  const verdict0 = await host.getAttribute('data-il-sim-verdict');
  await vr.click();
  await page.waitForFunction(() => document.querySelector('[data-il-sim-ready="etcd-quorum"]').getAttribute('data-il-xr-state') === 'active', null, { timeout: 10000 });
  await host.evaluate(el => new Promise((ok, no) => { const t0 = Date.now(); (function p() { if (el._ilImmersive._xrFrames >= 6) return ok(); if (Date.now() - t0 > 10000) return no(new Error('xr frames ' + el._ilImmersive._xrFrames)); setTimeout(p, 50); })(); }));
  const live = await host.evaluate(el => { const P = el._ilImmersive; return {
    raf: P.raf, frames: P._xrFrames, views: el.getAttribute('data-il-xr-views'), ref: el.getAttribute('data-il-xr-ref'),
    glErr: P.gl.getError(), cap: el.querySelector('.il-immersive__captions').textContent, badge: el.querySelector('.il-immersive__badge').textContent,
    exit: el.querySelector('[data-il-xr-enter="vr"]').textContent, arDisabled: el.querySelector('[data-il-xr-enter="ar"]').disabled }; });
  const req = await page.evaluate(() => window.__xr.requests[0]);
  assert.deepEqual(req, { mode: 'immersive-vr', req: [], opt: ['local-floor'], overlay: false });
  assert.equal(await page.evaluate(() => window.__xr.compat), 1, 'makeXRCompatible on the existing context');
  assert.equal(await page.evaluate(() => window.__xr.session.refAsked.join('>')), 'local-floor>local');
  assert.equal(live.ref, 'local', 'graceful fallback when local-floor is refused');
  assert.equal(live.views, '2', 'stereo views');
  assert.equal(live.raf, 0, 'page orbit RAF paused');
  assert.equal(live.glErr, 0, 'no GL error from per-view draws');
  const lit = await page.evaluate(() => window.__xr.lit);
  assert.ok(lit && lit[0] > 500 && lit[1] > 500, 'authored geometry drawn in BOTH eye viewports: ' + JSON.stringify(lit));
  assert.match(live.cap, /in WebXR VR \(local render, not Pixel Streaming\)/);
  assert.match(live.cap, /authored \.glb \(\d+ nodes/);
  assert.match(live.badge, /authored \.glb · WebXR VR/);
  assert.equal(live.exit, 'Exit VR');
  assert.equal(live.arDisabled, true);
  const otherDisabled = await page.evaluate(() => [...document.querySelectorAll('.il-immersive[data-il-xr="available"]:not([data-il-sim-ready="etcd-quorum"]) [data-il-xr-enter="vr"]')].every(b => b.disabled));
  assert.ok(otherDisabled, 'one session per page');
  /* Controller select flips the next free-play toggle → authored nodes re-tint in the headset. */
  await page.evaluate(() => window.__xr.session.dispatchEvent(new Event('select')));
  const st = await host.evaluate(el => ({ v: el.getAttribute('data-il-sim-verdict'), s: JSON.stringify(el._ilImmersive._simState) }));
  const st0 = await page.evaluate(() => JSON.stringify(window.ILImmersiveSims.get('etcd-quorum').initial));
  assert.notEqual(st.s, st0, 'select changed sim state');
  await host.screenshot({ path: path.join(shots, 'immersive-webxr-vr-stereo.png') });
  await vr.click();
  await page.waitForFunction(() => document.querySelector('[data-il-sim-ready="etcd-quorum"]').getAttribute('data-il-xr-state') === 'idle', null, { timeout: 10000 });
  await page.waitForTimeout(100);
  const after = await host.evaluate(el => ({ raf: el._ilImmersive.raf, cap: el.querySelector('.il-immersive__captions').textContent, badge: el.querySelector('.il-immersive__badge').textContent, label: el.querySelector('[data-il-xr-enter="vr"]').textContent, mode: el.getAttribute('data-il-xr-mode') }));
  assert.ok(after.raf > 0, '2D orbit RAF resumed');
  assert.doesNotMatch(after.cap, /in WebXR/);
  assert.doesNotMatch(after.badge, /WebXR/);
  assert.equal(after.label, 'Enter VR');
  assert.equal(after.mode, null);
  assert.equal(await page.evaluate(() => window.ILImmersive3D.xr.active()), null);
  assert.deepEqual(errors, []);
  await c.close();
  return `${live.frames}+ stereo frames (lit px L/R ${lit.join('/')}) · ref ${live.ref} · ${verdict0} → select → ${st.v} · exit → 2D RAF resumed`;
});

await check('WebXR AR: requests dom-overlay optionally, shows Exit overlay only when granted, denial is reported honestly', async () => {
  const c = await xrContext({}, XR_FAKE);
  const page = await c.newPage(); const errors = []; page.on('pageerror', e => errors.push(String(e)));
  await page.goto(base + '/immersive/', { waitUntil: 'load' });
  await page.locator('[data-il-sim="rbac-authz"]').scrollIntoViewIfNeeded();
  const host = page.locator('[data-il-sim-ready="rbac-authz"]');
  await host.waitFor({ timeout: 30000 });
  await host.locator('[data-il-xr-enter="ar"]:not([hidden])').click();
  await page.waitForFunction(() => document.querySelector('[data-il-sim-ready="rbac-authz"]').getAttribute('data-il-xr-state') === 'active', null, { timeout: 10000 });
  const req = await page.evaluate(() => window.__xr.requests[0]);
  assert.deepEqual(req, { mode: 'immersive-ar', req: [], opt: ['local-floor', 'dom-overlay'], overlay: true });
  assert.ok(await host.locator('.il-immersive__xr-overlay').isVisible(), 'AR overlay shown');
  assert.match(await host.locator('.il-immersive__xr-overlay-cap').textContent(), /not Unreal Pixel Streaming, not a hosted cluster/);
  /* A granted dom-overlay sits in the top layer; headless has none, so dispatch instead of hit-testing past page chrome. */
  await host.locator('[data-il-xr-exit]').dispatchEvent('click');
  await page.waitForFunction(() => document.querySelector('[data-il-sim-ready="rbac-authz"]').getAttribute('data-il-xr-state') === 'idle', null, { timeout: 10000 });
  /* User / UA refuses the session → back to idle, no fake "in headset" caption. */
  await page.evaluate(() => { navigator.xr.requestSession = () => Promise.reject(new DOMException('denied', 'NotAllowedError')); });
  await host.locator('[data-il-xr-enter="vr"]').click();
  await page.waitForFunction(() => document.querySelector('[data-il-sim-ready="rbac-authz"]').getAttribute('data-il-xr-error') === 'NotAllowedError', null, { timeout: 5000 });
  assert.equal(await host.getAttribute('data-il-xr-state'), 'idle');
  assert.match(await host.locator('.il-immersive__captions').first().textContent(), /WebXR VR not started \(NotAllowedError\)/);
  assert.ok(await host.evaluate(el => el._ilImmersive.raf > 0), '2D loop never stopped');
  assert.deepEqual(errors, []);
  await c.close();
  return 'AR dom-overlay optional · exit via overlay · NotAllowedError → idle';
});

await check('WebXR on /immersive/review/: the remounted review stage inherits Enter VR; next card ends the session', async () => {
  const c = await xrContext({}, XR_FAKE);
  const page = await c.newPage(); const errors = []; page.on('pageerror', e => errors.push(String(e)));
  await page.goto(base + '/immersive/review/', { waitUntil: 'load' });
  await page.locator('[data-il-review-start]').click();
  await page.locator('[data-il-review-run]:not([hidden])').waitFor({ timeout: 15000 });
  const stage = page.locator('[data-il-review-stage]');
  await stage.locator('.il-immersive__badge[data-il-mesh="authored"]').waitFor({ timeout: 30000 });
  await page.waitForFunction(() => document.querySelector('[data-il-review-stage]').getAttribute('data-il-xr') === 'available', null, { timeout: 10000 });
  await stage.locator('[data-il-xr-enter="vr"]').click();
  await page.waitForFunction(() => document.querySelector('[data-il-review-stage]').getAttribute('data-il-xr-state') === 'active', null, { timeout: 10000 });
  /* select is a no-op on graded stages (review owns grading). */
  const s0 = await stage.evaluate(el => JSON.stringify(el._ilImmersive._simState));
  await page.evaluate(() => window.__xr.session.dispatchEvent(new Event('select')));
  assert.equal(await stage.evaluate(el => JSON.stringify(el._ilImmersive._simState)), s0);
  await page.locator('[data-il-review-option]').first().click();
  await page.locator('[data-il-review-next-card]:not([hidden])').click();
  await page.waitForFunction(() => window.__xr.session.ended === true, null, { timeout: 10000 });
  await page.waitForFunction(() => document.querySelector('[data-il-review-stage]').getAttribute('data-il-xr') === 'available', null, { timeout: 30000 });
  assert.equal(await page.evaluate(() => window.ILImmersive3D.xr.active()), null);
  assert.equal(await stage.getAttribute('data-il-xr-state'), 'idle');
  assert.deepEqual(errors, []);
  await c.close();
  return 'review stage XR available · select no-op on graded stage · remount ended session';
});

await check('/immersive/review/: Lab Muse reads the relearn queue aloud via browser speechSynthesis (hidden when unavailable)', async () => {
  const c = await xrContext({}, () => {
    window.__spoken = [];
    window.SpeechSynthesisUtterance = class { constructor(t) { this.text = t; } };
    Object.defineProperty(window, 'speechSynthesis', { configurable: true, value: { cancel() {}, speak(u) { window.__spoken.push(u.text); }, getVoices: () => [] } });
  });
  const page = await c.newPage(); const errors = []; page.on('pageerror', e => errors.push(String(e)));
  await page.goto(base + '/immersive/', { waitUntil: 'load' });
  /* Seed one real miss through a free-play drill so the line has a relearn card. */
  await page.locator('[data-il-sim="etcd-quorum"]').scrollIntoViewIfNeeded();
  const host = page.locator('[data-il-sim-ready="etcd-quorum"]');
  await host.waitFor({ timeout: 30000 });
  await host.locator('[data-il-sim-scenario="lose-two"]').click();
  const key = await page.evaluate(() => window.ILImmersiveSims.get('etcd-quorum').scenarios.find(x => x.id === 'lose-two').predict.answer);
  await host.locator(`[data-il-sim-option="${(key + 1) % 2}"]`).click();
  await page.goto(base + '/immersive/review/', { waitUntil: 'load' });
  const btn = page.locator('[data-il-review-speak]');
  assert.ok(await btn.isVisible(), 'CTA visible when speech synthesis exists');
  await btn.click();
  const spoken = await page.evaluate(() => window.__spoken);
  assert.equal(spoken.length, 1);
  assert.match(spoken[0], /^Lab Muse: 1 checkpoint due now on this device\. Next session is \d+ cards: 1 to relearn from misses/);
  assert.match(spoken[0], /Weakest domain: [^,]+, \d+ percent mastery\./);
  assert.match(await page.locator('[data-il-review-spoken]').textContent(), /spoken by this browser’s speech synthesis/);
  await c.close();
  const c2 = await xrContext({}, () => { Object.defineProperty(window, 'speechSynthesis', { configurable: true, value: undefined }); });
  const p2 = await c2.newPage();
  await p2.goto(base + '/immersive/review/', { waitUntil: 'load' });
  await p2.locator('[data-il-review-due]').waitFor();
  assert.equal(await p2.locator('[data-il-review-speak]').isVisible(), false, 'hidden without speechSynthesis');
  await c2.close();
  assert.deepEqual(errors, []);
  return spoken[0].slice(0, 96) + '…';
});

await browser.close();
server.close();
if (failed) { console.error(failed + ' check(s) failed'); process.exit(1); }
console.log('immersive browser checks OK');
