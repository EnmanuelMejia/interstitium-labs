import { readFile, writeFile, mkdir, rename } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const jobs = require('../docs/assets/noah-jobs.js');
const output = fileURLToPath(new URL('../docs/assets/noah-jobs-feed.json', import.meta.url));
const attemptFile = fileURLToPath(new URL('../.tools/noah-jobs-refresh-state.json', import.meta.url));
const attemptDir = fileURLToPath(new URL('../.tools/', import.meta.url));
let previous;
try { previous = JSON.parse(await readFile(output, 'utf8')); } catch (error) { if (error.code !== 'ENOENT') throw error; }
const now = Date.now();
let attempt;
try { attempt = JSON.parse(await readFile(attemptFile, 'utf8')); } catch (error) { if (error.code !== 'ENOENT') throw error; }
// One shared snapshot avoids multiplying API calls by the number of visitors.
// Keep provider's recommended maximum of four requests a day, including local reruns.
if (previous && now - Date.parse(previous.fetchedAt) < 6 * 60 * 60 * 1000) {
  console.log(`Kept Remotive snapshot from ${previous.fetchedAt}; the six-hour refresh interval has not elapsed.`);
  process.exit(0);
}
if (attempt && Number.isFinite(attempt.at) && now - attempt.at < 6 * 60 * 60 * 1000) {
  console.log('Skipped Remotive request; the six-hour interval since the last attempt has not elapsed. Existing snapshot is preserved.');
  process.exit(0);
}
await mkdir(attemptDir, { recursive: true });
await writeFile(attemptFile, JSON.stringify({ at: now }) + '\n', 'utf8');
const response = await fetch(jobs.FEED_URL, { headers: { Accept: 'application/json' }, signal: AbortSignal.timeout(30000) });
if (!response.ok) throw new Error(`Remotive returned ${response.status}. Existing snapshot is preserved.`);
const text = await response.text();
if (text.length > 4000000) throw new Error('Remotive response is larger than the supported snapshot. Existing file is preserved.');
const payload = JSON.parse(text);
if (!Array.isArray(payload.jobs)) throw new Error('Remotive did not return a jobs array.');
const normalized = jobs.mergeJobs([], payload.jobs.slice(0, jobs.LIMITS.feed).map(job => jobs.normalizeJob(job, 'remotive')).filter(Boolean));
if (!normalized.length) throw new Error('No valid public jobs were returned. Existing snapshot is preserved.');
const snapshot = { version: 1, provider: 'Remotive', providerURL: 'https://remotive.com', documentationURL: 'https://github.com/remotive-com/remote-jobs-api',
  fetchedAt: new Date(now).toISOString(), providerDelayHours: 24, endpoint: jobs.FEED_URL,
  notice: 'Public Remotive listings are delayed 24 hours. Verify current availability at the original Remotive URL. No signup is required.', jobs: normalized };
jobs.validateFeed(snapshot);
await writeFile(output + '.tmp', JSON.stringify(snapshot, null, 2) + '\n', 'utf8');
await rename(output + '.tmp', output);
console.log(`Saved ${normalized.length} attributed Remotive listings, retrieved ${snapshot.fetchedAt}.`);
