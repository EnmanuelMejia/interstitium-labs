import { secp256k1 } from "@noble/curves/secp256k1";
import { keccak_256 } from "@noble/hashes/sha3";
import { bytesToHex, hexToBytes } from "@noble/hashes/utils";

const enc = new TextEncoder();

export function buildMessage({ domain, address, nonce, issuedAt, uri }) {
  return [
    domain + " wants you to sign in with your Ethereum account:",
    address,
    "",
    "Sign in to Interstitium Labs",
    "",
    "URI: " + uri,
    "Version: 1",
    "Chain ID: 1",
    "Nonce: " + nonce,
    "Issued At: " + issuedAt,
  ].join("\n");
}

export function recoverAddress(message, signature) {
  const clean = signature.startsWith("0x") ? signature.slice(2) : signature;
  if (!/^[0-9a-fA-F]{130}$/.test(clean)) return null;
  const bytes = hexToBytes(clean);
  let v = bytes[64];
  if (v >= 27) v -= 27;
  if (v !== 0 && v !== 1) return null;
  const prefix = "\u0019Ethereum Signed Message:\n" + enc.encode(message).length;
  const hash = keccak_256(enc.encode(prefix + message));
  const sig = secp256k1.Signature.fromCompact(bytes.slice(0, 64)).addRecoveryBit(v);
  const pub = sig.recoverPublicKey(hash).toRawBytes(false).slice(1);
  return "0x" + bytesToHex(keccak_256(pub).slice(-20));
}

export function addressInMessage(message) {
  const line = (message || "").split("\n")[1] || "";
  return /^0x[a-fA-F0-9]{40}$/.test(line) ? line : "";
}
