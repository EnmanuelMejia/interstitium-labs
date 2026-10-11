import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { secp256k1 } from "@noble/curves/secp256k1";
import { keccak_256 } from "@noble/hashes/sha3";
import { bytesToHex, hexToBytes } from "@noble/hashes/utils";
import { moneroAddress, stableAmount } from "../../worker/pay.js";
import { buildMessage, recoverAddress } from "../../worker/siwe.js";

test("pinned domain address stays the resolved crypto.ETH.address", () => {
  const source = readFileSync(new URL("../../worker/pay.js", import.meta.url), "utf8");
  assert.match(source, /0xa0318208F98beDfC136D2f6bf3183eD4890Ab0a3/);
  assert.match(source, /enmanuelmejia\.crypto/);
});

test("Monero addresses are checked and never confused with the Ethereum record", () => {
  assert.equal(moneroAddress("0xa0318208F98beDfC136D2f6bf3183eD4890Ab0a3"), false);
  assert.equal(moneroAddress("4" + "1".repeat(94)), true);
  assert.equal(moneroAddress("8" + "1".repeat(94)), true);
  assert.equal(moneroAddress("4" + "1".repeat(93)), false);
  assert.equal(stableAmount("xmr", 14900), null);
});

test("stablecoin amounts are exact USD units, not a guessed price", () => {
  assert.equal(stableAmount("usdc", 14900).toString(), "149000000");
  assert.equal(stableAmount("dai", 79900).toString(), "799000000000000000000");
  assert.equal(stableAmount("qnt", 14900), null);
});

test("an Ethereum personal signature recovers the signer", () => {
  const priv = hexToBytes("11".repeat(32));
  const pub = secp256k1.getPublicKey(priv, false).slice(1);
  const address = "0x" + bytesToHex(keccak_256(pub).slice(-20));
  const message = buildMessage({
    domain: "interstitiumlabs.dev",
    address,
    nonce: "abc",
    issuedAt: "2026-10-08T00:00:00.000Z",
    uri: "https://interstitiumlabs.dev/account/",
  });
  const prefix = new TextEncoder().encode("\u0019Ethereum Signed Message:\n" + new TextEncoder().encode(message).length + message);
  const sig = secp256k1.sign(keccak_256(prefix), priv);
  const packed = "0x" + bytesToHex(sig.toCompactRawBytes()) + (27 + sig.recovery).toString(16);
  assert.equal(recoverAddress(message, packed), address);
});
