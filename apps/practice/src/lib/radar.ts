/** Public posts scanned 2026-09-22. Not a firehose, not verified incidents. */
export type RadarHit = {
  id: string;
  author: string;
  handle: string;
  url: string;
  when: string;
  claim: string;
  study: string;
  nodeId: string;
};

export const radarScanned = "2026-09-22";

export const radarHits: RadarHit[] = [
  {
    id: "2102506322277355745",
    author: "Pumpkin Security",
    handle: "PumpkinSecurity",
    url: "https://x.com/PumpkinSecurity/status/2102506322277355745",
    when: "2026-09-22",
    claim: "An npm import that pulls a stealer in one click mixes extension storage, browser trust, and supply-chain risk.",
    study: "Treat install popularity as nothing. Map the post onto the provenance question before you call it a detection.",
    nodeId: "sec-chain",
  },
  {
    id: "2102380662200074412",
    author: "0xTangent",
    handle: "loftyarcher",
    url: "https://x.com/loftyarcher/status/2102380662200074412",
    when: "2026-09-22",
    claim: "A widely downloaded B-tree package can hide runtime malware. Download count is not a review.",
    study: "The check they name is install-hook scrutiny plus a runtime diff against published source.",
    nodeId: "sec-chain",
  },
  {
    id: "2102373462379552834",
    author: "CyberSignal",
    handle: "XQOPTRX",
    url: "https://x.com/XQOPTRX/status/2102373462379552834",
    when: "2026-09-22",
    claim: "A public write-up of the GHAPPIER campaign: valid npm provenance after a GitHub Actions workflow was manipulated. They cite CloudSEK.",
    study: "Provenance answers where the artifact was built. It does not answer whether the source was already compromised.",
    nodeId: "sec-chain",
  },
  {
    id: "2102259301926744117",
    author: "Zeeshan Khan",
    handle: "zeeshankghouri",
    url: "https://x.com/zeeshankghouri/status/2102259301926744117",
    when: "2026-09-22",
    claim: "A public note on indexed-btree: payload in normal runtime code, not a lifecycle script. They cite Checkmarx Zero, 17 September 2026, and mention an Ethereum contract used as a pointer.",
    study: "Blocking postinstall is one path. It is not trust. Read the claim as a hypothesis until you have the primary report.",
    nodeId: "sec-chain",
  },
];

export const radarDropped = [
  "Post-quantum token threads with no named primitive (ML-KEM or ML-DSA). Noise, not a path.",
  "Accounts named John Dee that were posting about pizza and securities. Not scholarship.",
  "LinkedIn was not scanned. There is no connector for it.",
];
