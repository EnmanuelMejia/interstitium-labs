/**
 * solitary-sound / Cloudflare Worker — enterprise security headers
 * Copy into the Worker fetch handler. Keep in sync with docs/_headers
 * and docs/ops/ENTERPRISE-SECURITY.md §3.2.
 *
 * Usage:
 *   return applyEnterpriseSecurityHeaders(await env.ASSETS.fetch(request));
 * or wrap any Response.
 */
export function applyEnterpriseSecurityHeaders(response) {
  const headers = new Headers(response.headers);
  headers.set(
    "Content-Security-Policy",
    [
      "default-src 'self'",
      "script-src 'self'",
      "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
      "font-src 'self' https://fonts.gstatic.com",
      "img-src 'self' data: blob:",
      "connect-src 'self'",
      "worker-src 'self'",
      "manifest-src 'self'",
      "frame-ancestors 'none'",
      "base-uri 'self'",
      "form-action 'self' https://buy.stripe.com https://www.paypal.com",
      "object-src 'none'",
      "upgrade-insecure-requests",
    ].join("; ")
  );
  headers.set(
    "Strict-Transport-Security",
    "max-age=31536000; includeSubDomains; preload"
  );
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()"
  );
  headers.set("X-Frame-Options", "DENY");
  headers.set("Cross-Origin-Opener-Policy", "same-origin");
  headers.set("Cross-Origin-Resource-Policy", "same-origin");
  headers.set("X-DNS-Prefetch-Control", "off");
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}
