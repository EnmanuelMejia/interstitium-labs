/**
 * Disposable production smoke. Run only after the verified release:
 * $env:NOAH_LIVE_RELEASED='yes'; node scripts/test-noah-live.mjs
 *
 * This script makes at most ONE real Noah request containing a public posting
 * and blank candidate evidence. It does not apply, contact employers, import
 * private facts, use a signed-in browser profile, or submit external forms.
 */
import assert from 'node:assert/strict';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { chromium } from 'playwright';

if (process.env.NOAH_LIVE_RELEASED !== 'yes') {
  throw new Error('Production release has not been confirmed. Set NOAH_LIVE_RELEASED=yes only after the release is verified.');
}
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const baseURL = 'https://interstitiumlabs.dev';
const endpointURL = 'https://learn.interstitiumlabs.dev/api/noah';
const receiptDir = path.join(root, 'test-results'), shots = path.join(root, 'deploy-shots');
await Promise.all([mkdir(receiptDir, { recursive: true }), mkdir(shots, { recursive: true })]);
const receipt = { startedAt: new Date().toISOString(), baseURL, endpointURL, scope: 'Fresh disposable browser; public posting only; at most one real AI request; no application submission.',
  checks: [], screenshots: [], pageErrors: [], blockedWrites: [], requestCount: 0 };
let browser, context, reviewedPrompt = '', actualRequest, actualResponse;

async function check(name, run) {
  const start = performance.now();
  try {
    const detail = await run();
    receipt.checks.push({ name, passed: true, durationMs: Math.round(performance.now() - start), detail });
    console.log('PASS ' + name);
    return detail;
  } catch (error) {
    receipt.checks.push({ name, passed: false, durationMs: Math.round(performance.now() - start), error: error.message });
    throw error;
  }
}

try {
  const channel = process.env.NOAH_TEST_BROWSER || (process.platform === 'win32' ? 'msedge' : 'chromium');
  browser = await chromium.launch({ headless: true, channel: channel === 'chromium' ? undefined : channel,
    args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] });
  receipt.browserVersion = browser.version(); receipt.channel = channel;
  context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, reducedMotion: 'reduce' });
  await context.route('**/*', async route => {
    const request = route.request(), method = request.method();
    if (method === 'GET' || method === 'HEAD' || method === 'OPTIONS') return route.continue();
    if (method !== 'POST' || request.url() !== endpointURL || receipt.requestCount >= 1 || !reviewedPrompt) {
      receipt.blockedWrites.push({ method, url: request.url() }); return route.abort('blockedbyclient');
    }
    actualRequest = request.postDataJSON();
    assert.deepEqual(actualRequest.messages, [{ role: 'user', content: reviewedPrompt }]);
    assert.deepEqual(actualRequest.context, { source: 'device', trust: 'untrusted-reference' });
    receipt.requestCount++;
    return route.continue();
  });
  const page = await context.newPage();
  page.on('pageerror', error => receipt.pageErrors.push(error.message));

  await check('Production homepage links reach the new Jobs and Noah workspaces', async () => {
    const response = await page.goto(baseURL + '/', { waitUntil: 'networkidle' });
    assert.equal(response.status(), 200);
    assert.equal(await page.locator('.il-pillnav__links a[href="/jobs/"]').isVisible(), true);
    assert.equal(await page.locator('.il-pillnav__links a[href="/noah/"]').isVisible(), true);
    await page.locator('.il-pillnav__links a[href="/jobs/"]').click();
    await page.waitForFunction(() => window.NoahJobs && window.IL?.noahAI?.session);
    const state = await page.evaluate(() => window.NoahJobs.createStore(localStorage).snapshot());
    assert.equal(state.jobs.length, 0); assert.equal(state.profile.skills, ''); assert.equal(state.profile.notes, '');
    assert.equal(state.profile.support, false); assert.equal(state.profile.aplus, false); assert.equal(state.profile.portfolio, false);
    assert.equal(receipt.requestCount, 0);
    return { jobsURL: page.url(), blankEvidenceVerified: true };
  });

  await check('Production serves the expected same-origin feed; first public posting opens and saves locally', async () => {
    const localFeed = JSON.parse(await readFile(path.join(root, 'docs/assets/noah-jobs-feed.json'), 'utf8'));
    const response = await page.request.get(baseURL + '/assets/noah-jobs-feed.json');
    assert.equal(response.status(), 200);
    const feed = await response.json(); assert.equal(feed.provider, 'Remotive'); assert.equal(feed.fetchedAt, localFeed.fetchedAt);
    assert.equal(feed.jobs.length, localFeed.jobs.length); assert.ok(feed.jobs.length > 0);
    await page.locator('#job-lane').selectOption('all'); await page.locator('#load-jobs').click();
    await page.waitForFunction(() => !document.getElementById('load-jobs').disabled);
    const state = await page.evaluate(() => window.NoahJobs.createStore(localStorage).snapshot());
    assert.equal(state.jobs.length, feed.jobs.length);
    const card = page.locator('.job-card').first();
    const title = await card.locator('h3').innerText();
    await card.getByRole('button', { name: /^Save / }).click(); await card.getByRole('button', { name: /^Review / }).click();
    assert.equal(await page.locator('#review-title').innerText(), title);
    assert.equal(await card.getByRole('button', { name: /^Save / }).getAttribute('aria-pressed'), 'true');
    const source = await page.locator('#job-detail a.detail-source').getAttribute('href');
    assert.ok(source.startsWith('https://remotive.com/'));
    return { count: feed.jobs.length, snapshotAt: feed.fetchedAt, reviewedTitle: title, reviewedSource: source, savedOnlyInDisposableBrowser: true };
  });

  await check('Exactly reviewed public posting is consented to once and receives an actual remote reply', async () => {
    // A generic target avoids supplying a private career preference or candidate fact.
    await page.locator('details').filter({ has: page.locator('#profile-form') }).locator('summary').click();
    await page.locator('#profile-goal').fill('Review this public posting; no candidate profile supplied.');
    await page.locator('#profile-form button[type=submit]').click();
    const profile = await page.evaluate(() => window.NoahJobs.createStore(localStorage).snapshot().profile);
    assert.equal(profile.skills, ''); assert.equal(profile.notes, ''); assert.equal(profile.support, false); assert.equal(profile.aplus, false); assert.equal(profile.portfolio, false);
    await page.locator('#review-noah').click(); await page.locator('#share-dialog').waitFor({ state: 'visible' });
    assert.equal(await page.locator('#share-consent').isChecked(), false);
    reviewedPrompt = await page.locator('#share-preview').innerText();
    assert.ok(reviewedPrompt.length <= 3900); assert.ok(reviewedPrompt.includes('https://remotive.com/'));
    assert.ok(reviewedPrompt.includes('"statedSkills": ""') && reviewedPrompt.includes('"evidenceNotes": ""'));
    assert.equal(receipt.requestCount, 0);
    const responseEvent = page.waitForResponse(response => response.url() === endpointURL && response.request().method() === 'POST', { timeout: 25000 });
    await page.locator('#share-consent').check(); await page.locator('#send-noah').click();
    const response = await responseEvent; actualResponse = await response.json();
    await page.locator('#share-dialog').waitFor({ state: 'hidden', timeout: 25000 });
    assert.equal(response.status(), 200); assert.equal(actualResponse.fallback === true, false);
    assert.ok(typeof actualResponse.reply === 'string' && actualResponse.reply.trim().length > 0);
    assert.equal(receipt.requestCount, 1);
    const session = await page.evaluate(() => window.IL.noahAI.session.snapshot());
    assert.equal(session.conversation.at(-1).engine, 'remote'); assert.equal(session.conversation.at(-2).content, reviewedPrompt);
    assert.match(await page.locator('#noah-notice').innerText(), /remote Noah endpoint/);
    return { requestCount: receipt.requestCount, reviewedPromptLength: reviewedPrompt.length,
      reviewedPromptSHA256: createHash('sha256').update(reviewedPrompt).digest('hex'), transmittedMessages: actualRequest.messages.length,
      savedHistoryTransmitted: false, savedMemoryTransmitted: false, pageContextTransmitted: false,
      responseStatus: response.status(), serverFallback: actualResponse.fallback === true, responseCharacters: actualResponse.reply.length, savedEngine: 'remote' };
  });

  await check('Production jobs and Noah screenshots show the shared reply and working neural canvas', async () => {
    await page.evaluate(() => { if (document.activeElement instanceof HTMLElement) document.activeElement.blur(); scrollTo(0, 0); });
    await page.screenshot({ path: path.join(shots, 'jobs-live.png'), fullPage: false });
    receipt.screenshots.push('deploy-shots/jobs-live.png');
    await page.goto(baseURL + '/noah/', { waitUntil: 'networkidle' });
    await page.waitForFunction(() => window.IL?.noahAI?.session && document.querySelector('.neural-stage')?.dataset.rendered === 'true');
    const session = await page.evaluate(() => window.IL.noahAI.session.snapshot());
    assert.equal(session.conversation.at(-1).engine, 'remote'); assert.equal(session.preferences.shareMemoryWithRemote, false); assert.equal(session.preferences.sharePageContext, false);
    assert.equal(await page.locator('.message.assistant').count(), 1);
    await page.evaluate(() => { if (document.activeElement instanceof HTMLElement) document.activeElement.blur(); scrollTo(0, 0); });
    await page.screenshot({ path: path.join(shots, 'noah-live.png'), fullPage: false });
    receipt.screenshots.push('deploy-shots/noah-live.png');
    assert.equal(receipt.requestCount, 1); assert.deepEqual(receipt.pageErrors, []);
    return { renderedNeuralCanvas: true, sharedRemoteReplySurvivedNavigation: true, screenshots: 2, uncaughtPageErrors: 0 };
  });
} catch (error) {
  receipt.fatal = error.stack || error.message; console.error(error.stack || error.message);
  if (receipt.requestCount) console.error('One real request was already attempted. Do not repeat this smoke automatically.');
} finally {
  if (context) await context.close(); if (browser) await browser.close();
  receipt.finishedAt = new Date().toISOString(); receipt.passed = !receipt.fatal && receipt.checks.every(check => check.passed);
  await writeFile(path.join(receiptDir, 'noah-live.json'), JSON.stringify(receipt, null, 2) + '\n');
  console.log(receipt.checks.filter(check => check.passed).length + '/' + receipt.checks.length + ' production checks passed; ' + receipt.requestCount + ' real Noah request(s). Receipt: test-results/noah-live.json');
  if (!receipt.passed) process.exitCode = 1;
}
