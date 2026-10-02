/** Read-only public HTTP checks. Does not infer product capabilities from status 200. */
const targets = [
  { url: 'https://interstitiumlabs.dev/', kind: 'apex' },
  { url: 'https://app.interstitiumlabs.dev/', kind: 'page' },
  { url: 'https://api.interstitiumlabs.dev/api/health', kind: 'health' },
  { url: 'https://learn.interstitiumlabs.dev/', kind: 'page' },
  { url: 'https://interstitiumlabs.dev/coach/', kind: 'voice' },
  { url: 'https://interstitiumlabs.dev/cinema/', kind: 'voice' },
];

const checks = await Promise.all(targets.map(async ({ url, kind }) => {
  try {
    const response = await fetch(url, { signal: AbortSignal.timeout(15000), redirect: 'error' });
    const result = { url, status: response.status, pass: response.status === 200 };
    if (kind === 'health') {
      const health = await response.json();
      result.health = { ok: health.ok === true, database: health.database === 'connected' ? 'connected' : 'unverified' };
      result.pass &&= result.health.ok && result.health.database === 'connected';
    } else {
      result.contentType = response.headers.get('content-type');
      result.pass &&= result.contentType?.includes('text/html') === true;
      // Consume the body, without retaining or printing arbitrary site contents.
      await response.arrayBuffer();
    }
    if (kind === 'apex') {
      result.hsts = response.headers.has('strict-transport-security');
      result.csp = response.headers.has('content-security-policy');
      result.pass &&= result.hsts && result.csp;
    }
    if (kind === 'voice') {
      const policy = response.headers.get('permissions-policy') || '';
      result.microphoneDisabled = /\bmicrophone\s*=\s*\(\s*\)/.test(policy);
      result.microphoneSelf = /\bmicrophone\s*=\s*\(\s*self\s*\)/.test(policy);
      if (result.microphoneDisabled && result.microphoneSelf) {
        result.warning = 'Conflicting microphone policies; voice permission remains unverified.';
      } else if (result.microphoneDisabled) {
        result.warning = 'Microphone disabled; voice permission requires a scoped policy change.';
      }
    }
    return result;
  } catch (error) {
    // Avoid including exception text that might contain environment-specific data.
    return { url, pass: false, error: error.name || 'RequestError' };
  }
}));

console.log(JSON.stringify({ observedAt: new Date().toISOString(), checks, limitations: 'Public checks do not verify release IDs, authentication, data isolation, licenses, or agent capability.' }, null, 2));
if (checks.some(check => !check.pass)) process.exitCode = 1;
