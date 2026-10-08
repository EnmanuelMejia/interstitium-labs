import { ASSETS, PAY_ADDRESS, PAY_DOMAIN, TIERS, spotAmount, stableAmount, verifyTransfer } from "./pay.js";
import { addressInMessage, buildMessage, recoverAddress } from "./siwe.js";
import { clearCookie, hasSecret, open, readCookie, seal, setCookie } from "./session.js";

const PROVIDERS = {
  google: {
    id: "GOOGLE_CLIENT_ID",
    secret: "GOOGLE_CLIENT_SECRET",
    auth: "https://accounts.google.com/o/oauth2/v2/auth",
    token: "https://oauth2.googleapis.com/token",
    scope: "openid email profile",
  },
  github: {
    id: "GITHUB_CLIENT_ID",
    secret: "GITHUB_CLIENT_SECRET",
    auth: "https://github.com/login/oauth/authorize",
    token: "https://github.com/login/oauth/access_token",
    scope: "read:user user:email",
  },
  x: {
    id: "X_CLIENT_ID",
    secret: "X_CLIENT_SECRET",
    auth: "https://twitter.com/i/oauth2/authorize",
    token: "https://api.twitter.com/2/oauth2/token",
    scope: "users.read tweet.read",
  },
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "www.interstitiumlabs.dev") {
      url.hostname = "interstitiumlabs.dev";
      return Response.redirect(url.toString(), 301);
    }
    if (url.pathname.startsWith("/api/")) return api(request, url, env);
    return env.ASSETS.fetch(request);
  },
};

function json(body, status = 200, extra = []) {
  const headers = new Headers({
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
  });
  for (const cookie of extra) headers.append("set-cookie", cookie);
  return new Response(JSON.stringify(body), { status, headers });
}

function sameOrigin(request, url) {
  const origin = request.headers.get("origin");
  if (!origin) return request.method === "GET";
  try {
    return new URL(origin).host === url.host;
  } catch {
    return false;
  }
}

async function api(request, url, env) {
  if (!sameOrigin(request, url) && request.method !== "GET") {
    return json({ error: "cross-origin" }, 403);
  }
  const path = url.pathname;
  if (path === "/api/session" && request.method === "GET") return session(request, env);
  if (path === "/api/auth/providers" && request.method === "GET") return providers(env);
  if (path === "/api/auth/logout" && request.method === "POST") {
    return json({ ok: true }, 200, [clearCookie("il_session")]);
  }
  if (path === "/api/account" && request.method === "POST") return saveAccount(request, env);
  if (path === "/api/pay/config" && request.method === "GET") return payConfig(env);
  if (path === "/api/pay/quote" && request.method === "GET") return quote(url, env);
  if (path === "/api/pay/verify" && request.method === "POST") return verify(request, env);
  if (path === "/api/checkout" && request.method === "POST") return checkout(request, url, env);
  const oauth = path.match(/^\/api\/auth\/(google|github|x)\/(start|callback)$/);
  if (oauth && request.method === "GET") {
    return oauth[2] === "start"
      ? startOAuth(oauth[1], request, url, env)
      : finishOAuth(oauth[1], request, url, env);
  }
  if (path === "/api/auth/siwe/nonce" && request.method === "POST") return siweNonce(url, env);
  if (path === "/api/auth/siwe/verify" && request.method === "POST") return siweVerify(request, env);
  return json({ error: "not-found" }, 404);
}

function providers(env) {
  const out = {};
  for (const name of Object.keys(PROVIDERS)) {
    const spec = PROVIDERS[name];
    out[name] = !!(env[spec.id] && env[spec.secret]);
  }
  out.ethereum = hasSecret(env);
  return json(out);
}

async function session(request, env) {
  if (!hasSecret(env)) return json({ user: null, secret: false });
  const user = await open(env.SESSION_SECRET, readCookie(request, "il_session"));
  if (!user) return json({ user: null, secret: true });
  let profile = null;
  if (env.ACCOUNTS) {
    profile = await env.ACCOUNTS.get("user:" + user.provider + ":" + user.sub, "json");
  }
  return json({
    secret: true,
    user: {
      provider: user.provider,
      name: (profile && profile.displayName) || user.name || "",
      email: user.email || "",
      address: user.address || "",
    },
  });
}

async function saveAccount(request, env) {
  if (!hasSecret(env)) return json({ error: "session-secret-missing" }, 503);
  const user = await open(env.SESSION_SECRET, readCookie(request, "il_session"));
  if (!user) return json({ error: "sign-in-required" }, 401);
  if (!env.ACCOUNTS) return json({ error: "account-store-missing" }, 503);
  const body = await request.json().catch(() => null);
  const displayName = body && typeof body.displayName === "string" ? body.displayName.trim() : "";
  if (displayName.length < 1 || displayName.length > 80) return json({ error: "bad-name" }, 400);
  const record = {
    provider: user.provider,
    sub: user.sub,
    email: user.email || "",
    address: user.address || "",
    displayName,
    updated: new Date().toISOString(),
  };
  await env.ACCOUNTS.put("user:" + user.provider + ":" + user.sub, JSON.stringify(record));
  return json({ ok: true, name: displayName });
}

async function issueSession(env, user) {
  const token = await seal(
    env.SESSION_SECRET,
    {
      provider: user.provider,
      sub: user.sub,
      name: user.name || "",
      email: user.email || "",
      address: user.address || "",
    },
    60 * 60 * 24 * 14
  );
  if (env.ACCOUNTS) {
    const key = "user:" + user.provider + ":" + user.sub;
    const existing = await env.ACCOUNTS.get(key, "json");
    if (!existing) {
      await env.ACCOUNTS.put(
        key,
        JSON.stringify({
          provider: user.provider,
          sub: user.sub,
          email: user.email || "",
          address: user.address || "",
          displayName: user.name || "",
          created: new Date().toISOString(),
        })
      );
    }
  }
  return json({ ok: true }, 200, [setCookie("il_session", token, 60 * 60 * 24 * 14), clearCookie("il_nonce")]);
}

async function siweNonce(url, env) {
  if (!hasSecret(env)) return json({ error: "session-secret-missing" }, 503);
  const nonce = crypto.randomUUID().replace(/-/g, "");
  const issuedAt = new Date().toISOString();
  const token = await seal(env.SESSION_SECRET, { nonce, issuedAt }, 600);
  return json({ nonce, issuedAt }, 200, [setCookie("il_nonce", token, 600)]);
}

async function siweVerify(request, env) {
  if (!hasSecret(env)) return json({ error: "session-secret-missing" }, 503);
  const pending = await open(env.SESSION_SECRET, readCookie(request, "il_nonce"));
  if (!pending) return json({ error: "nonce-expired" }, 401);
  const body = await request.json().catch(() => null);
  const address = body && body.address;
  const signature = body && body.signature;
  if (!/^0x[a-fA-F0-9]{40}$/.test(address || "") || typeof signature !== "string") {
    return json({ error: "bad-request" }, 400);
  }
  const url = new URL(request.url);
  const message = buildMessage({
    domain: url.host,
    address,
    nonce: pending.nonce,
    issuedAt: pending.issuedAt,
    uri: url.origin + "/account/",
  });
  const recovered = recoverAddress(message, signature);
  if (!recovered || recovered.toLowerCase() !== address.toLowerCase()) {
    return json({ error: "bad-signature" }, 401);
  }
  if (addressInMessage(message).toLowerCase() !== address.toLowerCase()) {
    return json({ error: "bad-signature" }, 401);
  }
  if (env.ACCOUNTS) {
    const used = await env.ACCOUNTS.get("nonce:" + pending.nonce);
    if (used) return json({ error: "nonce-used" }, 401);
    await env.ACCOUNTS.put("nonce:" + pending.nonce, "1", { expirationTtl: 600 });
  }
  return issueSession(env, {
    provider: "ethereum",
    sub: address.toLowerCase(),
    name: address.slice(0, 6) + "…" + address.slice(-4),
    address,
  });
}

function providerReady(env, name) {
  const spec = PROVIDERS[name];
  return !!(env[spec.id] && env[spec.secret]);
}

async function startOAuth(name, request, url, env) {
  if (!hasSecret(env)) return json({ error: "session-secret-missing" }, 503);
  if (!providerReady(env, name)) {
    return json(
      {
        error: "provider-not-configured",
        provider: name,
        callback: url.origin + "/api/auth/" + name + "/callback",
      },
      503
    );
  }
  const spec = PROVIDERS[name];
  const state = crypto.randomUUID();
  const verifier = b64(crypto.getRandomValues(new Uint8Array(32)));
  const challenge = await sha256url(verifier);
  const redirectUri = url.origin + "/api/auth/" + name + "/callback";
  const auth = new URL(spec.auth);
  auth.searchParams.set("client_id", env[spec.id]);
  auth.searchParams.set("redirect_uri", redirectUri);
  auth.searchParams.set("response_type", "code");
  auth.searchParams.set("scope", spec.scope);
  auth.searchParams.set("state", state);
  if (name === "google" || name === "x") {
    auth.searchParams.set("code_challenge", challenge);
    auth.searchParams.set("code_challenge_method", "S256");
  }
  const packed = await seal(env.SESSION_SECRET, { state, verifier, provider: name }, 600);
  return new Response(null, {
    status: 302,
    headers: {
      location: auth.toString(),
      "set-cookie": setCookie("il_oauth", packed, 600),
      "cache-control": "no-store",
    },
  });
}

async function finishOAuth(name, request, url, env) {
  if (!hasSecret(env) || !providerReady(env, name)) return json({ error: "provider-not-configured" }, 503);
  const pending = await open(env.SESSION_SECRET, readCookie(request, "il_oauth"));
  if (!pending || pending.provider !== name || pending.state !== url.searchParams.get("state")) {
    return json({ error: "state-mismatch" }, 401);
  }
  const code = url.searchParams.get("code");
  if (!code) return json({ error: "missing-code" }, 400);
  const spec = PROVIDERS[name];
  const redirectUri = url.origin + "/api/auth/" + name + "/callback";
  const profile = await exchange(name, env, spec, code, redirectUri, pending.verifier);
  if (!profile) return json({ error: "provider-rejected" }, 502);
  const token = await seal(
    env.SESSION_SECRET,
    {
      provider: name,
      sub: profile.sub,
      name: profile.name || "",
      email: profile.email || "",
      address: "",
    },
    60 * 60 * 24 * 14
  );
  if (env.ACCOUNTS) {
    const key = "user:" + name + ":" + profile.sub;
    const existing = await env.ACCOUNTS.get(key, "json");
    if (!existing) {
      await env.ACCOUNTS.put(
        key,
        JSON.stringify({
          provider: name,
          sub: profile.sub,
          email: profile.email || "",
          displayName: profile.name || "",
          created: new Date().toISOString(),
        })
      );
    }
  }
  const headers = new Headers({
    location: url.origin + "/account/",
    "cache-control": "no-store",
  });
  headers.append("set-cookie", setCookie("il_session", token, 60 * 60 * 24 * 14));
  headers.append("set-cookie", clearCookie("il_oauth"));
  return new Response(null, { status: 302, headers });
}

async function exchange(name, env, spec, code, redirectUri, verifier) {
  const body = new URLSearchParams({
    grant_type: "authorization_code",
    code,
    redirect_uri: redirectUri,
    client_id: env[spec.id],
  });
  if (name !== "github") body.set("code_verifier", verifier);
  const headers = { "content-type": "application/x-www-form-urlencoded", accept: "application/json" };
  if (name === "github") {
    body.set("client_secret", env[spec.secret]);
  } else if (name === "google") {
    body.set("client_secret", env[spec.secret]);
  } else {
    headers.authorization = "Basic " + btoa(env[spec.id] + ":" + env[spec.secret]);
  }
  const tokenRes = await fetch(spec.token, { method: "POST", headers, body });
  if (!tokenRes.ok) return null;
  const token = await tokenRes.json();
  if (!token.access_token) return null;
  if (name === "github") {
    const userRes = await fetch("https://api.github.com/user", {
      headers: { authorization: "Bearer " + token.access_token, accept: "application/vnd.github+json", "user-agent": "interstitium-labs" },
    });
    if (!userRes.ok) return null;
    const user = await userRes.json();
    return { sub: String(user.id), name: user.name || user.login || "", email: user.email || "" };
  }
  if (name === "google") {
    const userRes = await fetch("https://openidconnect.googleapis.com/v1/userinfo", {
      headers: { authorization: "Bearer " + token.access_token },
    });
    if (!userRes.ok) return null;
    const user = await userRes.json();
    return { sub: user.sub, name: user.name || "", email: user.email || "" };
  }
  const userRes = await fetch("https://api.twitter.com/2/users/me", {
    headers: { authorization: "Bearer " + token.access_token },
  });
  if (!userRes.ok) return null;
  const user = await userRes.json();
  const data = user.data || {};
  return { sub: data.id, name: data.name || data.username || "", email: "" };
}

function payConfig(env) {
  const tiers = Object.entries(TIERS).map(([id, tier]) => ({
    id,
    name: tier.name,
    usdCents: tier.usdCents,
    stable: {
      usdc: stableAmount("usdc", tier.usdCents).toString(),
      usdt: stableAmount("usdt", tier.usdCents).toString(),
      dai: stableAmount("dai", tier.usdCents).toString(),
    },
  }));
  return json({
    domain: PAY_DOMAIN,
    address: PAY_ADDRESS,
    chainId: 1,
    record: "crypto.ETH.address",
    stripe: typeof env.STRIPE_SECRET_KEY === "string" && env.STRIPE_SECRET_KEY.startsWith("sk_"),
    assets: ASSETS,
    tiers,
    iso20022:
      "XRP, XLM, ALGO, HBAR, XDC, and IOTA have no address on this domain, so they are not offered. QNT is an ERC-20 and is quoted in USD. ISO/IEC 2022 is a character encoding, not a payment network.",
  });
}

async function quote(url, env) {
  if (!hasSecret(env)) return json({ error: "session-secret-missing" }, 503);
  const tier = TIERS[url.searchParams.get("tier") || ""];
  const asset = url.searchParams.get("asset");
  if (!tier || (asset !== "eth" && asset !== "qnt")) return json({ error: "bad-quote" }, 400);
  const amount = await spotAmount(asset, tier.usdCents);
  if (amount == null) return json({ error: "price-unavailable" }, 503);
  const token = await seal(
    env.SESSION_SECRET,
    { tier: url.searchParams.get("tier"), asset, amount: amount.toString() },
    900
  );
  return json({ asset, amount: amount.toString(), quote: token });
}

async function verify(request, env) {
  const body = await request.json().catch(() => null);
  if (!body) return json({ error: "bad-request" }, 400);
  const tier = TIERS[body.tier];
  const asset = ASSETS[body.asset] ? body.asset : "";
  if (!tier || !asset) return json({ error: "bad-request" }, 400);
  let minimum = stableAmount(asset, tier.usdCents);
  if (minimum == null) {
    if (!hasSecret(env)) return json({ error: "session-secret-missing" }, 503);
    const quoted = await open(env.SESSION_SECRET, body.quote || "");
    if (!quoted || quoted.tier !== body.tier || quoted.asset !== asset) {
      return json({ error: "quote-expired" }, 401);
    }
    minimum = BigInt(quoted.amount);
  }
  let result;
  try {
    result = await verifyTransfer(body.txHash, asset, minimum);
  } catch {
    return json({ error: "rpc-unavailable" }, 503);
  }
  if (result.ok && env.ACCOUNTS) {
    await env.ACCOUNTS.put(
      "pay:" + body.txHash.toLowerCase(),
      JSON.stringify({
        tier: body.tier,
        asset,
        from: result.from,
        status: result.status,
        at: new Date().toISOString(),
        to: PAY_ADDRESS,
      })
    );
  }
  return json(result, result.ok ? 200 : 402);
}

async function checkout(request, url, env) {
  if (typeof env.STRIPE_SECRET_KEY !== "string" || !env.STRIPE_SECRET_KEY.startsWith("sk_")) {
    return json({ error: "stripe-not-configured" }, 503);
  }
  const body = await request.json().catch(() => null);
  const tierId = body && body.tier;
  const tier = TIERS[tierId];
  if (!tier) return json({ error: "bad-tier" }, 400);
  const form = new URLSearchParams();
  form.set("mode", "payment");
  form.set("success_url", url.origin + "/enroll/success?session_id={CHECKOUT_SESSION_ID}");
  form.set("cancel_url", url.origin + "/enroll/cancel");
  form.set("line_items[0][quantity]", "1");
  form.set("line_items[0][price_data][currency]", "usd");
  form.set("line_items[0][price_data][unit_amount]", String(tier.usdCents));
  form.set("line_items[0][price_data][product_data][name]", tier.name);
  form.set("metadata[tier]", tierId);
  const res = await fetch("https://api.stripe.com/v1/checkout/sessions", {
    method: "POST",
    headers: {
      authorization: "Bearer " + env.STRIPE_SECRET_KEY,
      "content-type": "application/x-www-form-urlencoded",
    },
    body: form,
  });
  const payload = await res.json().catch(() => null);
  if (!res.ok || !payload || typeof payload.url !== "string" || !payload.url.startsWith("https://checkout.stripe.com/")) {
    return json({ error: "stripe-rejected" }, 502);
  }
  return json({ url: payload.url });
}

function b64(bytes) {
  let bin = "";
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

async function sha256url(text) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return b64(new Uint8Array(digest));
}
