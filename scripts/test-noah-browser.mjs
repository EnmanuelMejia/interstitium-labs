/** Disposable browser regression suite. No signed-in profile, production writes, or real AI requests.
 * npm run test:browser
 * NOAH_TEST_BASE_URL=http://127.0.0.1:8765 npm run test:browser
 * NOAH_TEST_BROWSER=chromium npm run test:browser (Windows defaults to installed Microsoft Edge; other systems use Chromium)
 */
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const docs = path.join(root, 'docs');
const evidence = path.join(root, 'test-results');
const shots = path.join(root, 'deploy-shots');
await Promise.all([mkdir(evidence, { recursive: true }), mkdir(shots, { recursive: true })]);
const results = { startedAt: new Date().toISOString(), scope: 'Disposable automated desktop browser and emulated viewports. No physical-device or universal-browser claim.',
  checks: [], screenshots: [], accessibility: [], pageErrors: [], consoleErrors: [] };
let server, browser, context, baseURL;
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.glb': 'model/gltf-binary', '.woff2': 'font/woff2', '.ico': 'image/x-icon', '.webp': 'image/webp' };

async function staticServer() {
  const headerFile = (await readFile(path.join(docs, '_headers'), 'utf8')).replaceAll('\r\n', '\n');
  const defaultBlock = headerFile.split('\n/*\n')[1]?.split('\n\n')[0];
  assert.ok(defaultBlock, 'Expected the real site-wide security header block');
  const securityHeaders = Object.fromEntries(defaultBlock.split('\n').filter(line => /^  [\w-]+:/.test(line)).map(line => {
    const split = line.trim().indexOf(':'); return [line.trim().slice(0, split), line.trim().slice(split + 1).trim()];
  }));
  server = createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
      let target = path.resolve(docs, '.' + pathname);
      if (target !== docs && !target.startsWith(docs + path.sep)) { response.writeHead(403); response.end(); return; }
      if ((await stat(target)).isDirectory()) target = path.join(target, 'index.html');
      const body = await readFile(target);
      response.writeHead(200, { ...securityHeaders, 'Content-Type': MIME[path.extname(target)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
      response.end(body);
    } catch (_) { response.writeHead(404, { 'Content-Type': 'text/plain' }); response.end('Not found'); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  results.securityHeaders = securityHeaders;
  return 'http://127.0.0.1:' + server.address().port;
}
async function check(name, run) {
  const start = performance.now();
  try { const detail = await run(); results.checks.push({ name, passed: true, durationMs: Math.round(performance.now() - start), detail }); console.log('PASS ' + name); }
  catch (error) { results.checks.push({ name, passed: false, durationMs: Math.round(performance.now() - start), error: error.message }); console.error('FAIL ' + name + ': ' + error.message); }
}
async function visit(page, pathname = '/noah/') {
  await page.goto(baseURL + pathname, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.IL?.noahAI?.session && window.NoahWorkflows);
}
async function view(page, name) { await page.locator('[data-view="' + name + '"]').click(); await page.locator('#view-' + name).waitFor({ state: 'visible' }); }
async function snapshot(page) { return page.evaluate(() => window.IL.noahAI.session.snapshot()); }
async function send(page, text) {
  await view(page, 'conversation'); await page.locator('#message').fill(text); await page.locator('#send').click();
  await page.waitForFunction(() => !document.getElementById('send').disabled);
}
async function addMemory(page, kind, text) {
  await view(page, 'memory'); await page.locator('#memory-kind').selectOption(kind); await page.locator('#memory-text').fill(text); await page.locator('#memory-form button[type=submit]').click();
}
async function workflow(page, topic) {
  await view(page, 'workflows'); await page.locator('#workflow-topic').fill(topic); await page.locator('#workflow-form button').click();
  return page.locator('.workflow-card').filter({ has: page.getByRole('heading', { name: topic, exact: true }) });
}
async function waitTask(page, topic, status) {
  await page.waitForFunction(({ topic, status }) => window.NoahWorkflows.list().some(t => t.title === topic && t.status === status), { topic, status });
  return page.evaluate(topic => window.NoahWorkflows.list().find(t => t.title === topic), topic);
}

try {
  baseURL = (process.env.NOAH_TEST_BASE_URL || await staticServer()).replace(/\/$/, '');
  results.baseURL = baseURL;
  results.channel = process.env.NOAH_TEST_BROWSER || (process.platform === 'win32' ? 'msedge' : 'chromium');
  browser = await chromium.launch({ headless: true, channel: results.channel === 'chromium' ? undefined : results.channel,
    args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] });
  results.browserVersion = browser.version();
  context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, acceptDownloads: true, reducedMotion: 'reduce' });
  const requests = [];
  await context.route('**/api/noah', async route => {
    const body = route.request().postDataJSON(); requests.push(body);
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ reply: 'Mocked remote answer for the consent regression test.' }) });
  });
  // No telemetry or external network calls from this test context.
  await context.route('**/api/noah-stats', route => route.fulfill({ status: 204, body: '' }));
  await context.route(/^https?:\/\/(?!127\.0\.0\.1|localhost)/, route => route.abort('blockedbyclient'));
  const page = await context.newPage();
  page.on('pageerror', error => results.pageErrors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') results.consoleErrors.push(message.text()); });
  await visit(page, '/noah/?token=qa-url-secret#private-fragment');

  await check('Workspace boots with WebGL and a real original graph', async () => {
    await page.waitForFunction(() => document.querySelector('.neural-stage').dataset.rendered === 'true');
    const graph = await page.evaluate(async () => {
      const canvas = document.getElementById('noah-neural'); const gl = canvas.getContext('webgl');
      const json = await (await fetch('/assets/noah/noah-neural.json')).json();
      return { rendered: canvas.parentElement.dataset.rendered, width: canvas.width, height: canvas.height,
        nodes: json.nodes.length, edges: json.edges.length, loopSeconds: json.loopSeconds, contextLost: gl.isContextLost(), glError: gl.getError(), version: gl.getParameter(gl.VERSION) };
    });
    assert.equal(graph.rendered, 'true'); assert.equal(graph.nodes, 96); assert.ok(graph.edges > 0); assert.equal(graph.loopSeconds, 20);
    assert.ok(graph.width > 0 && graph.height > 0); assert.equal(graph.contextLost, false); assert.equal(graph.glError, 0);
    assert.equal(await page.locator('#noah-launcher').count(), 0);
    assert.equal(await page.locator('#motion-toggle').getAttribute('aria-pressed'), 'true');
    await page.locator('#motion-toggle').click(); assert.equal(await page.locator('#motion-toggle').getAttribute('aria-pressed'), 'false');
    await page.locator('#motion-toggle').click(); assert.equal(await page.locator('#motion-toggle').getAttribute('aria-pressed'), 'true');
    return graph;
  });

  await check('Local conversation persists with device provenance and sends no remote request', async () => {
    const count = requests.length; await send(page, 'hello'); const saved = await snapshot(page);
    assert.equal(requests.length, count); assert.equal(saved.conversation.length, 2); assert.equal(saved.conversation[1].engine, 'device');
    assert.ok(saved.conversation[1].notice.includes('on-device')); assert.equal(saved.conversation[0].context.path, '/noah/');
    assert.equal(JSON.stringify(saved).includes('qa-url-secret'), false);
    await page.reload({ waitUntil: 'networkidle' });
    assert.equal(await page.locator('.message').count(), 2); assert.match(await page.locator('.message.assistant .notice').innerText(), /on-device/);
    return { savedMessages: 2, remoteRequests: 0, queryAndHashExcluded: true };
  });

  await check('Reply formatter keeps source links clickable and treats unsafe URLs and HTML as text', async () => {
    const detail = await page.evaluate(() => {
      const host = document.createElement('div');
      window.IL.noahAI.renderReply(host, '**Sources**\n\n- [Site lab](/paths/devops-zero-to-hire/)\n- [Official docs](https://example.com/guide)\n- [Bad script](javascript:alert(1))\n- [Bad data](data:text/html,test)\n- [Bad relative](//example.com/private)\n- [Bad credentials](https://user:password@example.com/)\n<img src=x onerror="window.qaInjected=true"><script>window.qaInjected=true</script>');
      return { hrefs: Array.from(host.querySelectorAll('a'), a => a.href), linkNames: Array.from(host.querySelectorAll('a'), a => a.textContent),
        dangerousElements: host.querySelectorAll('img,script,iframe,object').length, handlers: host.querySelectorAll('[onerror],[onclick],[onload]').length,
        visibleUnsafeText: host.textContent.includes('javascript:alert(1)') && host.textContent.includes('<img'), bold: host.querySelector('strong')?.textContent,
        injected: window.qaInjected === true };
    });
    assert.deepEqual(detail.linkNames, ['Site lab', 'Official docs']); assert.equal(detail.hrefs[0], baseURL + '/paths/devops-zero-to-hire/');
    assert.equal(detail.hrefs[1], 'https://example.com/guide'); assert.equal(detail.dangerousElements, 0); assert.equal(detail.handlers, 0);
    assert.equal(detail.visibleUnsafeText, true); assert.equal(detail.bold, 'Sources'); assert.equal(detail.injected, false);
    await send(page, 'What should I learn first?');
    assert.ok(await page.locator('.message.assistant a[href$="/paths/devops-zero-to-hire/"]').count() > 0);
    return detail;
  });

  await check('Memory notes and goals add, edit, survive reload, and redact familiar secrets', async () => {
    await addMemory(page, 'note', 'Prefer one example. api_key=qa-private-key');
    await addMemory(page, 'goal', 'Learn CIDR through a lab.');
    assert.equal(await page.locator('.memory-card').count(), 2);
    const note = page.locator('.memory-card').filter({ hasText: 'Prefer one example.' });
    await note.getByRole('button', { name: /^Edit note/ }).click(); await page.locator('#edit-text').fill('Prefer small Python examples.');
    await page.locator('#edit-form button[type=submit]').click(); await page.locator('#edit-dialog').waitFor({ state: 'hidden' });
    const saved = await snapshot(page); assert.equal(saved.memories[0].text, 'Prefer small Python examples.');
    assert.equal(saved.memories[1].kind, 'goal'); assert.equal(JSON.stringify(saved).includes('qa-private-key'), false);
    await page.reload({ waitUntil: 'networkidle' }); await view(page, 'memory');
    assert.equal(await page.locator('.memory-card').count(), 2); assert.match(await page.locator('#goal-summary').innerText(), /Learn CIDR/);
    return { savedNotes: 1, savedGoals: 1 };
  });

  await check('Remote request excludes saved conversation, notes, page context by default', async () => {
    await send(page, 'zyxwvutestunknown'); const body = requests.at(-1); assert.ok(body);
    assert.deepEqual(body.messages, [{ role: 'user', content: 'zyxwvutestunknown' }]);
    assert.deepEqual(body.context, { source: 'device', trust: 'untrusted-reference' });
    assert.equal(JSON.stringify(body).includes('Prefer small'), false); assert.equal(JSON.stringify(body).includes('qa-url-secret'), false);
    const assistant = (await snapshot(page)).conversation.at(-1); assert.equal(assistant.engine, 'remote');
    await page.reload({ waitUntil: 'networkidle' }); assert.match(await page.locator('.message.assistant .notice').last().innerText(), /remote Noah endpoint/);
    return { exactMessageCount: body.messages.length, referenceTrust: body.context.trust, savedRemoteProvenance: true };
  });

  await check('Explicit consent sends only allowlisted saved reference data with user-level trust', async () => {
    await view(page, 'memory'); await page.locator('#share-memory').check(); await page.locator('#share-context').check();
    await send(page, 'zyxwvutestunknownsecond'); const body = requests.at(-1);
    assert.ok(body.messages.length <= 12); assert.ok(body.messages.every(m => m.role === 'user' || m.role === 'assistant'));
    assert.match(body.messages[0].content, /untrusted data/); assert.match(JSON.stringify(body), /Prefer small Python/);
    assert.equal(body.context.page.path, '/noah/'); assert.equal(body.context.trust, 'untrusted-reference');
    assert.equal(JSON.stringify(body).includes('qa-url-secret'), false); assert.equal(JSON.stringify(body).includes('private-fragment'), false);
    await page.reload({ waitUntil: 'networkidle' }); await view(page, 'memory');
    assert.equal(await page.locator('#share-memory').isChecked(), true); assert.equal(await page.locator('#share-context').isChecked(), true);
    return { messageCount: body.messages.length, includedMemories: body.context.memories.length, pagePath: body.context.page.path };
  });

  await check('Session export downloads an allowlisted file; forget/clear/reset survive reopen', async () => {
    await page.evaluate(() => localStorage.setItem('qa-unrelated', 'qa-unrelated-secret'));
    await view(page, 'memory'); const downloadEvent = page.waitForEvent('download'); await page.locator('#export-session').click();
    const download = await downloadEvent; const filename = path.join(evidence, 'noah-device-data.json'); await download.saveAs(filename);
    const data = JSON.parse(await readFile(filename, 'utf8')); assert.equal(download.suggestedFilename(), 'noah-device-data.json');
    assert.equal(data.scope, 'device'); assert.equal(data.cloudSync, false); assert.equal(data.memories.length, 2);
    assert.equal(JSON.stringify(data).includes('qa-unrelated-secret'), false); assert.equal(JSON.stringify(data).includes('qa-private-key'), false);
    await page.locator('.memory-card').filter({ hasText: 'Prefer small Python examples.' }).getByRole('button', { name: /^Forget note/ }).click();
    await view(page, 'conversation'); await page.locator('#clear-chat').click(); await page.locator('#review-approve').click();
    assert.equal((await snapshot(page)).conversation.length, 0); assert.equal((await snapshot(page)).memories.length, 1);
    await page.reload({ waitUntil: 'networkidle' }); assert.equal((await snapshot(page)).conversation.length, 0);
    await view(page, 'memory'); assert.equal(await page.locator('.memory-card').count(), 1);
    await page.locator('#reset-session').click(); await page.locator('#review-approve').click();
    await page.reload({ waitUntil: 'networkidle' }); const reset = await snapshot(page);
    assert.equal(reset.conversation.length, 0); assert.equal(reset.memories.length, 0); assert.equal(reset.preferences.shareMemoryWithRemote, false);
    assert.equal(await page.evaluate(() => localStorage.getItem('qa-unrelated')), 'qa-unrelated-secret');
    return { exportFilename: download.suggestedFilename(), clearPreservesNotes: true, resetPreservesUnrelatedStorage: true };
  });

  await check('Workflow searches real sources, reloads checkpoint, reviews approval, downloads real brief', async () => {
    let card = await workflow(page, 'Kubernetes'); await card.getByRole('button', { name: /^Run workflow/ }).click();
    let task = await waitTask(page, 'Kubernetes', 'approval');
    assert.equal(task.steps[0].status, 'completed'); assert.ok(task.steps[0].output.matches.length > 0);
    assert.equal(task.steps[1].status, 'pending'); assert.equal(task.steps[1].output, null); assert.equal(await card.getByRole('button', { name: /^Download/ }).count(), 0);
    await page.reload({ waitUntil: 'networkidle' }); task = await waitTask(page, 'Kubernetes', 'paused');
    assert.equal(task.steps[0].attempts, 1); assert.equal(task.steps[1].approved, false);
    await view(page, 'workflows'); card = page.locator('.workflow-card').filter({ has: page.getByRole('heading', { name: 'Kubernetes', exact: true }) });
    await card.getByRole('button', { name: /^Resume workflow/ }).click(); await waitTask(page, 'Kubernetes', 'approval');
    await card.getByRole('button', { name: /^Review next step/ }).click(); assert.equal(await page.locator('#review-dialog').isVisible(), true);
    await page.locator('#review-cancel').click(); assert.equal((await waitTask(page, 'Kubernetes', 'approval')).steps[1].output, null);
    await card.getByRole('button', { name: /^Review next step/ }).click(); await page.locator('#review-approve').click();
    task = await waitTask(page, 'Kubernetes', 'completed'); assert.equal(task.steps[0].attempts, 1); assert.equal(task.steps[1].status, 'completed');
    const downloadEvent = page.waitForEvent('download'); await card.getByRole('button', { name: /^Download study brief/ }).click();
    const download = await downloadEvent; const target = path.join(evidence, 'noah-study-brief.md'); await download.saveAs(target);
    const text = await readFile(target, 'utf8'); assert.match(text, /# Noah study brief/); assert.match(text, /Topic: Kubernetes/);
    assert.match(text, /https:\/\/interstitiumlabs\.dev\//); assert.match(text, /SCIENTIA OMNIA VINCIT/);
    assert.equal(text, task.steps[1].output.markdown);
    return { sources: task.steps[0].output.matches.length, searchAttempts: task.steps[0].attempts, filename: download.suggestedFilename(), checkpointSurvivedReload: true };
  });

  await check('Cancelling during a real pending search prevents saved outputs and restart after reload', async () => {
    const catalog = await readFile(path.join(docs, 'assets/noah-knowledge.json'), 'utf8');
    let release, arrived;
    const gate = new Promise(resolve => { release = resolve; }); const intercepted = new Promise(resolve => { arrived = resolve; });
    const routeHandler = async route => { arrived(); await gate; await route.fulfill({ status: 200, contentType: 'application/json', body: catalog }); };
    await page.route('**/assets/noah-knowledge.json', routeHandler);
    try {
      const card = await workflow(page, 'SQL cancellation'); await card.getByRole('button', { name: /^Run workflow/ }).click(); await intercepted;
      await card.getByRole('button', { name: /^Cancel workflow/ }).click(); release();
      await page.waitForFunction(() => window.NoahWorkflows.list().find(t => t.title === 'SQL cancellation')?.events.some(e => /Stopped before saving/.test(e.text)));
      let task = await waitTask(page, 'SQL cancellation', 'cancelled'); assert.equal(task.steps[0].status, 'pending'); assert.equal(task.steps[0].output, null);
      await page.unroute('**/assets/noah-knowledge.json', routeHandler); await page.reload({ waitUntil: 'networkidle' });
      task = await waitTask(page, 'SQL cancellation', 'cancelled');
      const after = await page.evaluate(async id => window.NoahWorkflows.run(id), task.id);
      assert.equal(after.status, 'cancelled'); assert.equal(after.steps[0].output, null);
      return { savedOutput: false, terminalStatus: after.status, attempts: after.steps[0].attempts };
    } finally { release(); await page.unroute('**/assets/noah-knowledge.json', routeHandler); }
  });

  for (const name of ['conversation', 'workflows', 'memory']) {
    await check('Accessibility: ' + name + ' view (WCAG 2 A/AA and 2.1 AA)', async () => {
      await view(page, name);
      const audit = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
      const violations = audit.violations.map(v => ({ id: v.id, impact: v.impact, description: v.description, help: v.help,
        nodes: v.nodes.map(n => ({ target: n.target, html: n.html, summary: n.failureSummary })) }));
      results.accessibility.push({ view: name, violations, incomplete: audit.incomplete.map(v => ({ id: v.id, nodes: v.nodes.length })), passedRules: audit.passes.length });
      assert.deepEqual(violations, [], 'axe violations: ' + violations.map(v => v.id + ' (' + v.nodes.length + ')').join(', '));
      return { violations: 0, passedRules: audit.passes.length, incompleteRules: audit.incomplete.length };
    });
  }

  const sizes = [{ width: 360, height: 800 }, { width: 768, height: 1024 }, { width: 1920, height: 1080 }, { width: 5120, height: 1440 }];
  for (const size of sizes) {
    await check('Responsive layouts without horizontal overflow: ' + size.width + '×' + size.height, async () => {
      await page.setViewportSize(size); const detail = [];
      for (const name of ['conversation', 'workflows', 'memory']) {
        await view(page, name);
        const dimensions = await page.evaluate(() => ({ width: window.innerWidth, documentWidth: document.documentElement.scrollWidth, bodyWidth: document.body.scrollWidth }));
        detail.push({ view: name, ...dimensions });
        assert.ok(dimensions.documentWidth <= dimensions.width + 1 && dimensions.bodyWidth <= dimensions.width + 1, JSON.stringify(detail));
      }
      return detail;
    });
  }
  await check('200% zoom equivalent: 960×540 CSS viewport and doubled text', async () => {
    // A 1920×1080 viewport at 200% browser zoom exposes approximately 960×540 CSS pixels.
    await page.setViewportSize({ width: 960, height: 540 }); const detail = [];
    for (const name of ['conversation', 'workflows', 'memory']) {
      await view(page, name); const width = await page.evaluate(() => document.documentElement.scrollWidth); assert.ok(width <= 961);
      detail.push({ view: name, width, cssViewport: '960×540' });
    }
    const textCases = [{ size: '200%', family: '' }, { size: '32px', family: 'sans-serif' }, { size: '32px', family: 'monospace' }];
    const enlargedText = [];
    try {
      for (const textCase of textCases) {
        await page.evaluate(value => { document.documentElement.style.fontSize = value.size; document.documentElement.style.fontFamily = value.family; }, textCase);
        for (const name of ['conversation', 'workflows', 'memory']) {
          await view(page, name);
          const dimensions = await page.evaluate(() => {
            const width = innerWidth, overflow = Array.from(document.querySelectorAll('body *')).map(element => {
              const rect = element.getBoundingClientRect();
              return { tag: element.tagName, id: element.id, class: typeof element.className === 'string' ? element.className : '',
                left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width) };
            }).filter(value => value.width > 0 && value.right > width + 1).slice(0, 12);
            return { width, documentWidth: document.documentElement.scrollWidth, rootFont: getComputedStyle(document.documentElement).fontSize, overflow };
          });
          enlargedText.push({ view: name, ...textCase, ...dimensions });
          assert.ok(dimensions.documentWidth <= 961, JSON.stringify(enlargedText.at(-1)));
          const headerLinks = await page.locator('.masthead nav a').evaluateAll(elements => elements.map(element => {
            const rect = element.getBoundingClientRect(); return { text: element.textContent, left: rect.left, right: rect.right, width: rect.width, height: rect.height };
          }));
          assert.ok(headerLinks.every(link => link.width > 0 && link.height > 0 && link.left >= -1 && link.right <= 961), JSON.stringify(headerLinks));
        }
      }
    } finally { await page.evaluate(() => { document.documentElement.style.fontSize = ''; document.documentElement.style.fontFamily = ''; }); }
    return { cssZoomEquivalent: detail, enlargedText, textScale: '200% and 32px (200% of a 16px baseline)', physicalBrowserZoom: 'not directly measured' };
  });

  await check('Keyboard navigation, dialog escape and focus return', async () => {
    await page.setViewportSize({ width: 1920, height: 1080 }); await view(page, 'conversation');
    await page.locator('#clear-chat').focus(); await page.keyboard.press('Enter'); await page.locator('#review-dialog').waitFor({ state: 'visible' });
    await page.keyboard.press('Escape'); await page.locator('#review-dialog').waitFor({ state: 'hidden' });
    assert.equal(await page.evaluate(() => document.activeElement.id), 'clear-chat');
    await page.locator('#message').fill('日本語');
    await page.locator('#message').dispatchEvent('keydown', { key: 'Enter', isComposing: true });
    assert.equal(await page.locator('#message').inputValue(), '日本語');
    assert.equal((await snapshot(page)).conversation.length, 0);
    await page.locator('#message').fill(''); return { dialogEscapeRestoresFocus: true, imeEnterDidNotSubmit: true };
  });

  await check('Existing floating widget lazy-loads shared memory, stays hidden until opened and closes accessibly', async () => {
    const widget = await context.newPage();
    try {
      await widget.goto(baseURL + '/about/', { waitUntil: 'networkidle' }); await widget.waitForFunction(() => window.IL?.noahAI?.session);
      const launcher = widget.locator('#noah-launcher'), panel = widget.locator('#noah-panel');
      assert.equal(await panel.isVisible(), false); assert.equal(await launcher.getAttribute('aria-expanded'), 'false');
      await launcher.click(); await panel.waitFor({ state: 'visible' }); assert.equal(await launcher.getAttribute('aria-expanded'), 'true');
      await widget.locator('#noah-input').fill('日本語'); await widget.locator('#noah-input').dispatchEvent('keydown', { key: 'Enter', isComposing: true });
      assert.equal(await widget.locator('#noah-input').inputValue(), '日本語');
      await widget.keyboard.press('Escape'); await panel.waitFor({ state: 'hidden' });
      assert.equal(await widget.evaluate(() => document.activeElement.id), 'noah-launcher');
      const audit = await new AxeBuilder({ page: widget }).include('#noah-launcher').withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
      assert.equal(audit.violations.length, 0);
      return { sharedSessionLoaded: true, hiddenPanelIsNotVisible: true, imeSafe: true, escapeRestoresFocus: true };
    } finally { await widget.close(); }
  });

  await check('Two-tab Noah deletion clears the floating widget immediately and drops a late private reply', async () => {
    const widget = await context.newPage(), peer = await context.newPage();
    let release, arrived;
    const gate = new Promise(resolve => { release = resolve; }), intercepted = new Promise(resolve => { arrived = resolve; });
    const privateQuestion = 'qaWidgetDeleteSentinelZyxwvu', lateAnswer = 'qaLateWidgetAnswerSentinelZyxwvu';
    const handler = async route => { arrived(); await gate; await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ reply: lateAnswer }) }); };
    try {
      await widget.goto(baseURL + '/about/', { waitUntil: 'networkidle' }); await widget.waitForFunction(() => window.IL?.noahAI?.session);
      await visit(peer); await peer.evaluate(() => window.IL.noahAI.session.clearAll());
      await widget.route('**/api/noah', handler); await widget.locator('#noah-launcher').click();
      await widget.locator('#noah-input').fill(privateQuestion); await widget.locator('#noah-send').click(); await intercepted;
      assert.match(await widget.locator('#noah-msgs').innerText(), new RegExp(privateQuestion));
      await peer.evaluate(() => window.IL.noahAI.session.clearAll());
      await widget.waitForFunction(text => !document.getElementById('noah-msgs').textContent.includes(text), privateQuestion);
      assert.equal((await widget.evaluate(() => window.IL.noahAI.session.snapshot())).conversation.length, 0);
      release(); await widget.waitForFunction(() => !document.getElementById('noah-send').disabled);
      const text = await widget.locator('#noah-msgs').innerText();
      assert.equal(text.includes(privateQuestion), false); assert.equal(text.includes(lateAnswer), false);
      assert.equal((await widget.evaluate(() => window.IL.noahAI.session.snapshot())).conversation.length, 0);
      await widget.unroute('**/api/noah', handler); await widget.locator('#noah-input').fill('hello'); await widget.locator('#noah-send').click();
      await widget.waitForFunction(() => !document.getElementById('noah-send').disabled);
      assert.equal(await widget.locator('.noah-msg').count(), 2);
      assert.equal((await widget.evaluate(() => window.IL.noahAI.session.snapshot())).conversation.length, 2);
      return { deletedQuestionVisible: false, lateAnswerVisible: false, savedAfterDeletion: 0, subsequentConversationMessages: 2, duplicateAssistantMessages: 0 };
    } finally { release(); await widget.unroute('**/api/noah', handler); await widget.close(); await peer.close(); }
  });

  await check('Captures desktop, ultrawide and mobile workspace screenshots', async () => {
    await send(page, 'What should I learn first?');
    for (const size of [{ width: 1920, height: 1080, name: 'noah-1920.png' }, { width: 5120, height: 1440, name: 'noah-5120.png' }, { width: 360, height: 800, name: 'noah-mobile.png' }]) {
      await page.setViewportSize({ width: size.width, height: size.height }); await view(page, 'conversation');
      await page.evaluate(() => { if (document.activeElement instanceof HTMLElement) document.activeElement.blur(); });
      await page.screenshot({ path: path.join(shots, size.name), fullPage: true });
      results.screenshots.push({ path: path.relative(root, path.join(shots, size.name)).replaceAll('\\', '/'), cssWidth: size.width, cssHeight: size.height, fullPage: true });
    }
    return { count: results.screenshots.length };
  });

  const jobs = await context.newPage();
  jobs.on('pageerror', error => results.pageErrors.push('Jobs: ' + error.message));
  const jobsRequests = [];
  jobs.on('request', request => jobsRequests.push(request.url()));
  const jobState = () => jobs.evaluate(() => window.NoahJobs.createStore(localStorage).snapshot());
  const importedTitle = 'QA Junior DevOps Fixture';
  async function importJob(title, url, requirements) {
    await jobs.locator('#import-title').fill(title); await jobs.locator('#import-company').fill('QA browser fixture');
    await jobs.locator('#import-url').fill(url); await jobs.locator('#import-location').fill('Worldwide');
    await jobs.locator('#import-requirements').fill(requirements);
    await jobs.locator('#import-form button[type=submit]').click();
  }
  await check('Jobs boots privately and loads the real attributed same-origin public snapshot on request', async () => {
    await jobs.goto(baseURL + '/jobs/', { waitUntil: 'networkidle' });
    await jobs.waitForFunction(() => window.NoahJobs && window.IL?.noahAI?.session);
    let state = await jobState(); assert.equal(state.jobs.length, 0); assert.equal(state.profile.skills, '');
    assert.equal(state.profile.support, false); assert.equal(state.profile.aplus, false); assert.equal(state.profile.portfolio, false);
    assert.equal(jobsRequests.some(url => url.endsWith('/assets/noah-jobs-feed.json')), false);
    await jobs.locator('#job-lane').selectOption('all'); await jobs.locator('#load-jobs').click();
    await jobs.waitForFunction(() => !document.getElementById('load-jobs').disabled);
    state = await jobState(); const source = JSON.parse(await readFile(path.join(docs, 'assets/noah-jobs-feed.json'), 'utf8'));
    assert.equal(state.jobs.length, source.jobs.length); assert.ok(state.jobs.length > 0);
    assert.ok(state.jobs.every(job => {
      const sourceURL = new URL(job.url);
      return job.source === 'remotive' && sourceURL.protocol === 'https:' && sourceURL.origin === 'https://remotive.com' && sourceURL.pathname.startsWith('/remote-jobs/');
    }));
    assert.match(await jobs.locator('#feed-state').innerText(), /Remotive|snapshot/i);
    assert.ok(jobsRequests.some(url => url.endsWith('/assets/noah-jobs-feed.json')));
    assert.equal(jobsRequests.some(value => { const url = new URL(value); return url.origin === 'https://remotive.com' && url.pathname.startsWith('/api/'); }), false);
    const card = jobs.locator('.job-card').first();
    await card.getByRole('button', { name: /^Save / }).click(); await card.getByRole('button', { name: /^Review / }).click();
    await jobs.locator('#detail-stage').selectOption('applied'); const selected = (await jobState()).saved[0];
    await jobs.locator('#saved-only').check(); await jobs.locator('#job-stage').selectOption('applied'); await jobs.locator('#save-filters').click();
    await jobs.reload({ waitUntil: 'networkidle' }); state = await jobState();
    assert.equal(state.stages[selected], 'applied'); assert.equal(state.filters.stage, 'applied'); assert.equal(state.filters.saved, true);
    assert.equal(await jobs.locator('.job-card').count(), 1);
    assert.match(await jobs.locator('.tracking-stage').innerText(), /recorded by you/);
    return { sourceListings: source.jobs.length, snapshotAt: source.fetchedAt, visitorProviderRequests: 0, appliedStageIsManual: true };
  });

  await check('Imported jobs deduplicate, save, compare and produce evidence-based local preparation without a network call', async () => {
    const count = requests.length;
    await importJob(importedTitle, 'https://careers.example.com/qa-devops?gh_jid=123&utm_source=qa', 'QA fixture requirements: Python, Docker, Kubernetes, Linux. Eligibility must be confirmed.');
    const adversarialRequirements = 'QA fixture requirements: Python, Docker, Kubernetes, Linux. Updated actual supplied text.\n' +
      'Encoded: &lt;img src=x onerror="window.qaJobInjected=true"&gt; &lt;script&gt;window.qaJobInjected=true&lt;/script&gt;.\n' +
      'Nested: <script><script>window.qaJobInjected=true</script></script><style><style>.qaUnwantedStyle{display:none}</style></style>' +
      '<!-- <script>window.qaJobInjected=true</script> -->safe-marker <img title=">" src=x onerror="window.qaJobInjected=true"><b>literal-label</b>.\n' +
      'Malformed: <script>window.qaJobInjected=true';
    await importJob(importedTitle, 'https://careers.example.com/qa-devops?gh_jid=123', adversarialRequirements);
    await importJob('QA Support Fixture', 'https://careers.example.com/qa-support', 'QA fixture requirements: Windows and PowerShell. IT support and CompTIA A+ requested.');
    let state = await jobState(); assert.equal(state.jobs.filter(job => job.source === 'import').length, 2);
    const evidenceDetails = jobs.locator('details').filter({ has: jobs.locator('#profile-form') });
    if (!await jobs.locator('#profile-form').isVisible()) await evidenceDetails.locator('summary').click();
    await jobs.locator('#profile-skills').fill('Python, PowerShell'); await jobs.locator('#profile-notes').fill('QA stated lab evidence only; paid production experience not supplied. api_key=qa-jobs-fixture-secret');
    await jobs.locator('#profile-portfolio').check(); await jobs.locator('#profile-form button[type=submit]').click();
    const card = jobs.locator('.job-card').filter({ has: jobs.getByRole('heading', { name: importedTitle, exact: true }) });
    await card.getByRole('button', { name: /^Save / }).click(); await card.getByRole('button', { name: /^Review / }).click();
    const postingText = await jobs.locator('#job-detail .requirements').textContent();
    assert.match(postingText, /safe-marker/); assert.match(postingText, /literal-label/);
    assert.equal(postingText.includes('qaJobInjected'), false); assert.equal(postingText.includes('qaUnwantedStyle'), false);
    assert.equal(await jobs.locator('#job-detail img, #job-detail script, #job-detail [onerror], .job-card img, .job-card script, .job-card [onerror]').count(), 0);
    assert.equal(await jobs.evaluate(() => window.qaJobInjected === true), false);
    await jobs.locator('#detail-stage').selectOption('preparing'); await jobs.locator('#local-prep').click();
    assert.match(await jobs.locator('#noah-notice').innerText(), /No details were sent/);
    assert.match(await jobs.locator('#noah-response').innerText(), /Python|Docker/); assert.equal(requests.length, count);
    for (const item of await jobs.locator('.job-card').all()) await item.locator('input[type=checkbox]').check();
    await jobs.locator('#compare-jobs').click(); assert.equal(await jobs.locator('.compare-table').count(), 1);
    assert.match(await jobs.locator('.compare-table').innerText(), /QA Junior DevOps Fixture/);
    assert.match(await jobs.locator('.compare-table').innerText(), /QA Support Fixture/);
    assert.equal(jobsRequests.some(value => new URL(value).origin === 'https://careers.example.com'), false);
    return { importedPostings: 2, canonicalDuplicateAvoided: true, reviewedSourceNeverFetched: true, localRemoteRequests: 0,
      adversarialEncodedNestedAndMalformedMarkup: 'No injected elements or execution; unwanted nested content absent' };
  });

  await check('Job sharing reviews the exact bounded prompt, requires fresh consent, excludes other Noah data, and preserves actual provenance', async () => {
    await jobs.evaluate(() => {
      window.IL.noahAI.session.addMemory({ kind: 'note', text: 'QA private unrelated Noah note' });
      window.IL.noahAI.session.setPreferences({ shareMemoryWithRemote: true, sharePageContext: true });
      window.IL.noahAI.session.record('user', 'QA private earlier conversation');
    });
    const count = requests.length; await jobs.locator('#review-noah').click(); await jobs.locator('#share-dialog').waitFor({ state: 'visible' });
    assert.equal(await jobs.locator('#share-consent').isChecked(), false);
    const preview = await jobs.locator('#share-preview').innerText(); assert.ok(preview.length <= 3900);
    assert.match(preview, /QA Junior DevOps Fixture/); assert.match(preview, /learning evidence/);
    const sourceURLs = Array.from(preview.matchAll(/"url":\s*"([^\s",]+)/g), match => new URL(match[1]));
    assert.deepEqual(sourceURLs.map(url => ({ protocol: url.protocol, hostname: url.hostname, origin: url.origin, pathname: url.pathname, search: url.search, hash: url.hash })).sort((a, b) => a.pathname.localeCompare(b.pathname)), [
      { protocol: 'https:', hostname: 'careers.example.com', origin: 'https://careers.example.com', pathname: '/qa-devops', search: '', hash: '' },
      { protocol: 'https:', hostname: 'careers.example.com', origin: 'https://careers.example.com', pathname: '/qa-support', search: '', hash: '' }
    ]);
    assert.equal(preview.includes('QA private unrelated'), false); assert.equal(preview.includes('QA private earlier'), false);
    assert.equal(preview.includes('gh_jid=123'), false); assert.equal(preview.includes('qa-jobs-fixture-secret'), false);
    await jobs.locator('#send-noah').click(); assert.equal(requests.length, count);
    await jobs.locator('#cancel-share').click(); assert.equal(requests.length, count);
    await jobs.locator('#review-noah').click(); assert.equal(await jobs.locator('#share-consent').isChecked(), false);
    await jobs.locator('#share-consent').check(); await jobs.locator('#send-noah').click(); await jobs.locator('#share-dialog').waitFor({ state: 'hidden' });
    const body = requests.at(-1); assert.equal(requests.length, count + 1);
    assert.deepEqual(body.messages, [{ role: 'user', content: preview }]); assert.deepEqual(body.context, { source: 'device', trust: 'untrusted-reference' });
    assert.match(await jobs.locator('#noah-notice').innerText(), /remote Noah endpoint/);
    const session = await jobs.evaluate(() => window.IL.noahAI.session.snapshot());
    assert.equal(session.conversation.at(-1).engine, 'remote'); assert.equal(session.conversation.at(-2).content, preview);
    await jobs.locator('#review-noah').click(); assert.equal(await jobs.locator('#share-consent').isChecked(), false); await jobs.keyboard.press('Escape');
    return { previewLength: preview.length, transmittedMessages: 1, memoryOverrides: false, pageContextOverrides: false, responseEngine: 'remote (mocked endpoint)' };
  });

  await check('Two-tab Noah deletion hides previous job analysis and discards a pending job reply', async () => {
    const peer = await context.newPage(); let release, arrived;
    const gate = new Promise(resolve => { release = resolve; }), intercepted = new Promise(resolve => { arrived = resolve; });
    const lateAnswer = 'qaLateJobAnswerSentinelZyxwvu';
    const handler = async route => { arrived(); await gate; await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ reply: lateAnswer }) }); };
    try {
      assert.equal(await jobs.locator('#noah-response').isVisible(), true);
      await visit(peer); await jobs.route('**/api/noah', handler);
      await jobs.locator('#review-noah').click(); await jobs.locator('#share-consent').check(); await jobs.locator('#send-noah').click(); await intercepted;
      await peer.evaluate(() => window.IL.noahAI.session.clearAll());
      await jobs.locator('#noah-response').waitFor({ state: 'hidden' });
      release(); await jobs.waitForFunction(() => !document.getElementById('send-noah').disabled);
      assert.equal(await jobs.locator('#noah-response').isVisible(), false); assert.equal(await jobs.locator('#noah-response').textContent(), '');
      assert.equal((await jobs.evaluate(() => window.IL.noahAI.session.snapshot())).conversation.length, 0);
      assert.equal((await jobs.locator('body').innerText()).includes(lateAnswer), false);
      return { previousAnalysisCleared: true, lateAnswerVisible: false, savedAfterDeletion: 0 };
    } finally { release(); await jobs.unroute('**/api/noah', handler); await peer.close(); }
  });

  await check('Job export is allowlisted and forgetting jobs survives reload without deleting unrelated browser data', async () => {
    await jobs.evaluate(() => localStorage.setItem('qa-unrelated-jobs', 'QA unrelated data'));
    const before = await jobState(), sharedBefore = await jobs.evaluate(() => window.IL.noahAI.session.snapshot().conversation.length);
    const event = jobs.waitForEvent('download'); await jobs.locator('#export-jobs').click();
    const download = await event, target = path.join(evidence, 'noah-jobs-device-export.json'); await download.saveAs(target);
    const saved = JSON.parse(await readFile(target, 'utf8'));
    assert.equal(download.suggestedFilename(), 'noah-jobs-device-export.json'); assert.equal(saved.scope, 'device');
    assert.equal(saved.state.jobs.length, before.jobs.length); assert.equal(JSON.stringify(saved).includes('QA unrelated data'), false);
    assert.equal(JSON.stringify(saved).includes('QA private unrelated Noah note'), false);
    await jobs.locator('#forget-jobs').click(); await jobs.reload({ waitUntil: 'networkidle' });
    const empty = await jobState(); assert.equal(empty.jobs.length, 0); assert.equal(empty.saved.length, 0); assert.deepEqual(empty.stages, {});
    assert.equal(empty.profile.skills, ''); assert.equal(await jobs.evaluate(() => localStorage.getItem('qa-unrelated-jobs')), 'QA unrelated data');
    assert.equal((await jobs.evaluate(() => window.IL.noahAI.session.snapshot())).conversation.length, sharedBefore);
    return { downloadedJobs: saved.state.jobs.length, deletedJobsAfterReload: 0, unrelatedDataPreserved: true, NoahHistoryManagedSeparately: true };
  });

  await check('Jobs desktop and mobile accessibility plus responsive 360/768/1920/5120 layouts', async () => {
    await jobs.locator('#job-lane').selectOption('all'); await jobs.locator('#load-jobs').click(); await jobs.waitForFunction(() => !document.getElementById('load-jobs').disabled);
    await jobs.locator('.job-card').first().getByRole('button', { name: /^Review / }).click();
    const detail = [];
    for (const size of sizes) {
      await jobs.setViewportSize(size);
      const dimensions = await jobs.evaluate(() => ({ width: innerWidth, documentWidth: document.documentElement.scrollWidth, bodyWidth: document.body.scrollWidth }));
      assert.ok(dimensions.documentWidth <= dimensions.width + 1 && dimensions.bodyWidth <= dimensions.width + 1, JSON.stringify(dimensions)); detail.push(dimensions);
      if (size.width === 360 || size.width === 1920) {
        const audit = await new AxeBuilder({ page: jobs }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
        const violations = audit.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) }));
        results.accessibility.push({ view: 'jobs-' + size.width, violations, incomplete: audit.incomplete.map(v => ({ id: v.id, nodes: v.nodes.length })), passedRules: audit.passes.length });
        assert.deepEqual(violations, [], 'Jobs axe violations: ' + violations.map(v => v.id).join(', '));
        await jobs.evaluate(() => { if (document.activeElement instanceof HTMLElement) document.activeElement.blur(); });
        const name = size.width === 360 ? 'jobs-mobile.png' : 'jobs-1920.png'; await jobs.screenshot({ path: path.join(shots, name), fullPage: true });
        results.screenshots.push({ path: path.relative(root, path.join(shots, name)).replaceAll('\\', '/'), cssWidth: size.width, cssHeight: size.height, fullPage: true });
      }
    }
    return { dimensions: detail, auditedWidths: [360, 1920] };
  });

  await check('Homepage Jobs and Noah navigation remains reachable within 360/1024/1280/1920 layouts', async () => {
    const home = await context.newPage(), detail = [];
    try {
      await home.goto(baseURL + '/', { waitUntil: 'networkidle' });
      for (const width of [360, 1024, 1280, 1920]) {
        await home.setViewportSize({ width, height: 900 });
        const dimensions = await home.locator('.il-pillnav').evaluate(nav => {
          const rect = nav.getBoundingClientRect(); return { width: innerWidth, left: rect.left, right: rect.right, documentWidth: document.documentElement.scrollWidth };
        });
        assert.ok(dimensions.left >= -1 && dimensions.right <= width + 1, JSON.stringify(dimensions)); detail.push(dimensions);
        const desktop = home.locator('.il-pillnav__links a[href="/jobs/"]');
        if (await desktop.isVisible()) {
          assert.equal(await home.locator('.il-pillnav__links a[href="/noah/"]').isVisible(), true);
        } else {
          const menu = home.locator('.il-menu'); await menu.locator('summary').click();
          assert.equal(await menu.locator('a[href="/jobs/"]').isVisible(), true); assert.equal(await menu.locator('a[href="/noah/"]').isVisible(), true);
          const sheet = await menu.locator('.il-menu__sheet').boundingBox(); assert.ok(sheet.x >= -1 && sheet.x + sheet.width <= width + 1);
          await menu.locator('summary').click();
        }
      }
      await home.setViewportSize({ width: 1920, height: 1080 }); await home.locator('.il-pillnav__links a[href="/jobs/"]').click();
      assert.equal(new URL(home.url()).pathname, '/jobs/'); assert.equal(await home.locator('#jobs-workspace').isVisible(), true);
      return { bounds: detail, jobsReachedByNavigation: true };
    } finally { await home.close(); }
  });
  await jobs.close();
  await check('No uncaught workspace JavaScript errors', async () => { assert.deepEqual(results.pageErrors, []); return { errors: 0 }; });
} catch (error) {
  results.fatal = error.stack || error.message;
  console.error(error.stack || error.message);
} finally {
  if (context) await context.close(); if (browser) await browser.close(); if (server) await new Promise(resolve => server.close(resolve));
  results.finishedAt = new Date().toISOString(); results.passed = !results.fatal && results.checks.every(c => c.passed);
  results.total = results.checks.length; results.passCount = results.checks.filter(c => c.passed).length;
  await writeFile(path.join(evidence, 'noah-browser.json'), JSON.stringify(results, null, 2) + '\n');
  console.log(`${results.passCount}/${results.total} browser checks passed. Evidence: test-results/noah-browser.json`);
  if (!results.passed) process.exitCode = 1;
}
