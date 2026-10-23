/** Immersive 3D browser check (2026-10-06; +4 CKA sims & shuffled options 2026-10-07; +6 CKA drills, keyed answers by index 2026-10-08; +remediation loop 2026-10-13): authored .glb really renders, LOD1 skipped, sims change the scene.
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

await browser.close();
server.close();
if (failed) { console.error(failed + ' check(s) failed'); process.exit(1); }
console.log('immersive browser checks OK');
