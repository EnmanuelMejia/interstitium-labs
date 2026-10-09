/** Immersive 3D browser check (2026-10-06; +4 CKA sims & shuffled options 2026-10-07; +6 CKA drills, keyed answers by index 2026-10-08): authored .glb really renders, LOD1 skipped, sims change the scene.
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

for (const p of ['/learn/', '/paths/aws-cloud-practitioner-plus/', '/paths/aws-cloud-ops/', '/paths/k8s-cka-exceed/']) {
  await check(p + ' hero stage renders authored glTF (scene-kit load order fixed)', async () => {
    const { page, errors } = await open(p);
    await waitAuthored(page, 1);
    const sim = await page.evaluate(() => document.querySelector('[data-il-sim-ready]')?.getAttribute('data-il-sim-ready') || '');
    if (p === '/paths/k8s-cka-exceed/' || p === '/paths/aws-cloud-practitioner-plus/') await page.locator('.il-immersive').first().screenshot({ path: path.join(shots, 'immersive-hero-' + p.split('/').filter(Boolean).pop() + '.png') });
    assert.deepEqual(errors, []);
    await page.close();
    return sim ? 'sim ' + sim : 'authored';
  });
}

await browser.close();
server.close();
if (failed) { console.error(failed + ' check(s) failed'); process.exit(1); }
console.log('immersive browser checks OK');
