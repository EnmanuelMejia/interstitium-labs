/**
 * Payments for enmanuelmejia.crypto.
 * crypto.ETH.address was read from the Polygon UNS ProxyReader on 2026-10-08.
 * If that record changes, this pin must change too. Other chains were empty.
 */
export const PAY_DOMAIN = "enmanuelmejia.crypto";
export const PAY_ADDRESS = "0xa0318208F98beDfC136D2f6bf3183eD4890Ab0a3";
export const CHAIN_ID = 1;

export const TIERS = {
  "prep-sprint": { name: "Prep Sprint", usdCents: 14900 },
  "devsecops-mastery": { name: "DevSecOps Mastery", usdCents: 49900 },
  "full-academy": { name: "Full Academy", usdCents: 79900 },
};

// Ethereum mainnet contracts. symbol() and decimals() were read on 2026-10-08.
export const ASSETS = {
  eth: { symbol: "ETH", kind: "native", decimals: 18 },
  usdc: {
    symbol: "USDC",
    kind: "erc20",
    decimals: 6,
    token: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  },
  usdt: {
    symbol: "USDT",
    kind: "erc20",
    decimals: 6,
    token: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
  },
  dai: {
    symbol: "DAI",
    kind: "erc20",
    decimals: 18,
    token: "0x6B175474E89094C44Da98b954EedeAC495271d0F",
  },
  qnt: {
    symbol: "QNT",
    kind: "erc20",
    decimals: 18,
    token: "0x4a220E6096B25EADb88358cb44068A3248254675",
    priced: true,
  },
  xmr: { symbol: "XMR", kind: "monero", decimals: 12, priced: true },
};

export const TRANSFER_TOPIC =
  "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef";

const RPCS = ["https://ethereum-rpc.publicnode.com", "https://1rpc.io/eth"];

const B58 = "[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]";
const XMR_STANDARD = new RegExp("^4" + B58 + "{94}$");
const XMR_SUB = new RegExp("^8" + B58 + "{94}$");
const XMR_INTEGRATED = new RegExp("^4" + B58 + "{105}$");

export function moneroAddress(value) {
  return XMR_STANDARD.test(value) || XMR_SUB.test(value) || XMR_INTEGRATED.test(value);
}

export function stableAmount(asset, usdCents) {
  const spec = ASSETS[asset];
  if (!spec || spec.kind !== "erc20" || spec.priced) return null;
  const scale = 10n ** BigInt(spec.decimals);
  return (BigInt(usdCents) * scale) / 100n;
}

export async function spotAmount(asset, usdCents) {
  const pair = { eth: "ETH-USD", qnt: "QNT-USD", xmr: "XMR-USD" }[asset];
  if (!pair) return null;
  const res = await fetch("https://api.coinbase.com/v2/prices/" + pair + "/spot", {
    headers: { accept: "application/json" },
  });
  if (!res.ok) return null;
  const body = await res.json();
  const priceText = String(body && body.data && body.data.amount || "");
  if (!/^\d+(\.\d+)?$/.test(priceText)) return null;
  const [whole, frac = ""] = priceText.split(".");
  const priceScale = 10n ** BigInt(frac.length);
  const priceInt = BigInt(whole + frac);
  if (priceInt <= 0n) return null;
  const scale = 10n ** BigInt(ASSETS[asset].decimals);
  const num = BigInt(usdCents) * scale * priceScale;
  const den = 100n * priceInt;
  return (num + den - 1n) / den;
}

async function rpc(method, params) {
  let last;
  for (const url of RPCS) {
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
      });
      if (!res.ok) {
        last = res.status;
        continue;
      }
      const body = await res.json();
      if (body.error) {
        last = body.error.message || "rpc";
        continue;
      }
      return body.result;
    } catch (err) {
      last = err;
    }
  }
  throw new Error("rpc failed: " + last);
}

function padAddress(address) {
  return "0x" + address.slice(2).toLowerCase().padStart(64, "0");
}

export async function verifyTransfer(txHash, asset, minimum) {
  if (!/^0x[0-9a-fA-F]{64}$/.test(txHash)) return { ok: false, status: "bad-hash" };
  const spec = ASSETS[asset];
  if (!spec || spec.kind === "monero") return { ok: false, status: "bad-asset" };
  const tx = await rpc("eth_getTransactionByHash", [txHash]);
  if (!tx) return { ok: false, status: "not-found" };
  const receipt = await rpc("eth_getTransactionReceipt", [txHash]);
  if (!receipt) return { ok: false, status: "pending" };
  if (receipt.status !== "0x1") return { ok: false, status: "reverted" };

  if (spec.kind === "native") {
    const to = (tx.to || "").toLowerCase();
    if (to !== PAY_ADDRESS.toLowerCase()) return { ok: false, status: "wrong-recipient" };
    if (BigInt(tx.value) < minimum) return { ok: false, status: "short" };
    return { ok: true, status: "confirmed", from: tx.from };
  }

  const want = padAddress(PAY_ADDRESS);
  const token = spec.token.toLowerCase();
  for (const log of receipt.logs || []) {
    if ((log.address || "").toLowerCase() !== token) continue;
    if (!log.topics || log.topics[0] !== TRANSFER_TOPIC) continue;
    if ((log.topics[2] || "").toLowerCase() !== want) continue;
    const moved = BigInt(log.data);
    if (moved < minimum) return { ok: false, status: "short" };
    return { ok: true, status: "confirmed", from: tx.from };
  }
  return { ok: false, status: "wrong-recipient" };
}
