const enc = new TextEncoder();

function b64url(bytes) {
  let bin = "";
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

function b64urlDecode(text) {
  const pad = text.length % 4 === 0 ? "" : "=".repeat(4 - (text.length % 4));
  const bin = atob(text.replace(/-/g, "+").replace(/_/g, "/") + pad);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

async function hmac(secret, data) {
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const mac = await crypto.subtle.sign("HMAC", key, enc.encode(data));
  return b64url(new Uint8Array(mac));
}

export function hasSecret(env) {
  return typeof env.SESSION_SECRET === "string" && env.SESSION_SECRET.length >= 32;
}

export async function seal(secret, payload, maxAgeSec) {
  const body = b64url(enc.encode(JSON.stringify({ ...payload, exp: Date.now() + maxAgeSec * 1000 })));
  const sig = await hmac(secret, body);
  return body + "." + sig;
}

export async function open(secret, token) {
  if (!token || !secret) return null;
  const cut = token.lastIndexOf(".");
  if (cut < 1) return null;
  const body = token.slice(0, cut);
  const sig = token.slice(cut + 1);
  const expect = await hmac(secret, body);
  if (expect.length !== sig.length) return null;
  let diff = 0;
  for (let i = 0; i < expect.length; i++) diff |= expect.charCodeAt(i) ^ sig.charCodeAt(i);
  if (diff !== 0) return null;
  try {
    const payload = JSON.parse(new TextDecoder().decode(b64urlDecode(body)));
    if (!payload.exp || payload.exp < Date.now()) return null;
    return payload;
  } catch {
    return null;
  }
}

export function readCookie(request, name) {
  const raw = request.headers.get("cookie") || "";
  const parts = raw.split(/;\s*/);
  for (const part of parts) {
    const i = part.indexOf("=");
    if (i < 1) continue;
    if (part.slice(0, i) === name) return decodeURIComponent(part.slice(i + 1));
  }
  return "";
}

export function setCookie(name, value, maxAgeSec) {
  return (
    name +
    "=" +
    encodeURIComponent(value) +
    "; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=" +
    maxAgeSec
  );
}

export function clearCookie(name) {
  return name + "=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0";
}
