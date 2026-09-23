import { mulberry32 } from "./ml.ts";

export const IRIS_FEATURES = ["Sepal length", "Sepal width", "Petal length", "Petal width"] as const;

/** Teaching slice of Fisher's iris measurements — a clean control set, not a security dataset. */
export const IRIS: { x: number[]; y: string }[] = [
  [5.1, 3.5, 1.4, 0.2],
  [4.9, 3.0, 1.4, 0.2],
  [4.7, 3.2, 1.3, 0.2],
  [4.6, 3.1, 1.5, 0.2],
  [5.0, 3.6, 1.4, 0.2],
  [5.4, 3.9, 1.7, 0.4],
  [4.6, 3.4, 1.4, 0.3],
  [5.0, 3.4, 1.5, 0.2],
  [4.4, 2.9, 1.4, 0.2],
  [4.9, 3.1, 1.5, 0.1],
  [5.4, 3.7, 1.5, 0.2],
  [4.8, 3.4, 1.6, 0.2],
  [4.8, 3.0, 1.4, 0.1],
  [4.3, 3.0, 1.1, 0.1],
  [5.8, 4.0, 1.2, 0.2],
  [7.0, 3.2, 4.7, 1.4],
  [6.4, 3.2, 4.5, 1.5],
  [6.9, 3.1, 4.9, 1.5],
  [5.5, 2.3, 4.0, 1.3],
  [6.5, 2.8, 4.6, 1.5],
  [5.7, 2.8, 4.5, 1.3],
  [6.3, 3.3, 4.7, 1.6],
  [4.9, 2.4, 3.3, 1.0],
  [6.6, 2.9, 4.6, 1.3],
  [5.2, 2.7, 3.9, 1.4],
  [5.0, 2.0, 3.5, 1.0],
  [5.9, 3.0, 4.2, 1.5],
  [6.0, 2.2, 4.0, 1.0],
  [6.1, 2.9, 4.7, 1.4],
  [5.6, 2.9, 3.6, 1.3],
  [6.3, 3.3, 6.0, 2.5],
  [5.8, 2.7, 5.1, 1.9],
  [7.1, 3.0, 5.9, 2.1],
  [6.3, 2.9, 5.6, 1.8],
  [6.5, 3.0, 5.8, 2.2],
  [7.6, 3.0, 6.6, 2.1],
  [4.9, 2.5, 4.5, 1.7],
  [7.3, 2.9, 6.3, 1.8],
  [6.7, 2.5, 5.8, 1.8],
  [7.2, 3.6, 6.1, 2.5],
  [6.5, 3.2, 5.1, 2.0],
  [6.4, 2.7, 5.3, 1.9],
  [6.8, 3.0, 5.5, 2.1],
  [5.7, 2.5, 5.0, 2.0],
  [5.8, 2.8, 5.1, 2.4],
].map((x, i) => ({ x, y: i < 15 ? "setosa" : i < 30 ? "versicolor" : "virginica" }));

export const MALWARE_FEATURES = [
  "Entropy",
  "Imports",
  "Sections",
  "Suspicious APIs",
  "Packed",
  "Unsigned",
  "Beacon rate",
  "Obfuscated strings",
] as const;

export type Telemetry = { id: string; x: number[]; y: "benign" | "malware" };

function round1(n: number) {
  return Math.round(n * 10) / 10;
}

/** Synthetic endpoint telemetry. No real malware, no binaries. */
export function makeBinaryTelemetry(seed = 11): Telemetry[] {
  const rng = mulberry32(seed);
  const rows: Telemetry[] = [];
  const gauss = () => {
    const u = Math.max(1e-6, rng());
    const v = Math.max(1e-6, rng());
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  for (let i = 0; i < 72; i++) {
    const mal = i >= 44;
    const entropy = round1((mal ? 7.25 : 6.05) + gauss() * (mal ? 0.32 : 0.42));
    const imports = Math.max(8, Math.round((mal ? 86 : 42) + gauss() * (mal ? 18 : 14)));
    const sections = Math.max(2, Math.round((mal ? 6.2 : 4.4) + gauss() * 1.1));
    const apis = Math.max(0, Math.round((mal ? 14 : 3.2) + gauss() * (mal ? 4 : 1.8)));
    const packed = mal ? (rng() < 0.72 ? 1 : 0) : rng() < 0.12 ? 1 : 0;
    const unsigned = mal ? (rng() < 0.8 ? 1 : 0) : rng() < 0.22 ? 1 : 0;
    const beacon = round1(Math.max(0, (mal ? 4.8 : 0.4) + gauss() * (mal ? 1.4 : 0.35)));
    const obf = round1(Math.max(0, (mal ? 0.62 : 0.12) + gauss() * 0.12));
    rows.push({
      id: `ep-${String(i + 1).padStart(3, "0")}`,
      x: [entropy, imports, sections, apis, packed, unsigned, beacon, obf],
      y: mal ? "malware" : "benign",
    });
  }
  return rows;
}

export const BINARY_TELEMETRY = makeBinaryTelemetry();

export const FAMILY_FEATURES = ["Entropy", "File writes", "Net calls", "Clipboard", "Packed", "Sections"] as const;

export type FamilyRow = { id: string; x: number[]; y: "locker" | "stealer" | "loader" };

export function makeFamilies(seed = 21): FamilyRow[] {
  const rng = mulberry32(seed);
  const gauss = () => {
    const u = Math.max(1e-6, rng());
    const v = Math.max(1e-6, rng());
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  const spec = {
    locker: { e: 7.5, w: 18, n: 4, c: 1, p: 0.8, s: 5 },
    stealer: { e: 6.4, w: 6, n: 9, c: 8, p: 0.35, s: 6 },
    loader: { e: 6.9, w: 3, n: 14, c: 0.4, p: 0.55, s: 3.2 },
  } as const;
  const rows: FamilyRow[] = [];
  (["locker", "stealer", "loader"] as const).forEach((y) => {
    const s = spec[y];
    for (let i = 0; i < 18; i++) {
      rows.push({
        id: `${y.slice(0, 2)}-${i + 1}`,
        y,
        x: [
          Math.round((s.e + gauss() * 0.25) * 10) / 10,
          Math.max(0, Math.round(s.w + gauss() * 2.2)),
          Math.max(0, Math.round(s.n + gauss() * 1.8)),
          Math.max(0, Math.round(s.c + gauss() * 1.1)),
          rng() < s.p ? 1 : 0,
          Math.max(1, Math.round(s.s + gauss() * 0.7)),
        ],
      });
    }
  });
  return rows;
}

export const FAMILIES = makeFamilies();

export const FLOW_FEATURES = ["Mean bytes", "Interval regularity", "Rare port", "Duration"] as const;

export type Flow = { id: string; x: number[]; y: "normal" | "beacon" };

export function makeFlows(seed = 31): Flow[] {
  const rng = mulberry32(seed);
  const gauss = () => {
    const u = Math.max(1e-6, rng());
    const v = Math.max(1e-6, rng());
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  const rows: Flow[] = [];
  for (let i = 0; i < 70; i++) {
    rows.push({
      id: `fl-${i + 1}`,
      y: "normal",
      x: [
        Math.max(40, Math.round(1800 + gauss() * 700)),
        Math.round((0.35 + Math.abs(gauss()) * 0.18) * 100) / 100,
        Math.round(Math.abs(gauss()) * 0.15 * 100) / 100,
        Math.max(0.1, Math.round((12 + gauss() * 6) * 10) / 10),
      ],
    });
  }
  for (let i = 0; i < 12; i++) {
    rows.push({
      id: `bc-${i + 1}`,
      y: "beacon",
      x: [
        Math.max(20, Math.round(90 + Math.abs(gauss()) * 30)),
        Math.round((0.92 + gauss() * 0.03) * 100) / 100,
        Math.round((0.7 + Math.abs(gauss()) * 0.12) * 100) / 100,
        Math.max(0.2, Math.round((1.2 + Math.abs(gauss())) * 10) / 10),
      ],
    });
  }
  return rows;
}

export const FLOWS = makeFlows();

export type Msg = { id: string; text: string; y: "benign" | "phish" | "alert"; holdout: boolean };

export const MESSAGES: Msg[] = [
  { id: "b1", y: "benign", holdout: false, text: "The deployment window for the billing service is Thursday 02:00 UTC. No customer impact expected." },
  { id: "b2", y: "benign", holdout: false, text: "Please review the Q3 access recertification in the identity portal by Friday." },
  { id: "b3", y: "benign", holdout: false, text: "Lunch and learn: how we rotate service principals. Conference room 4." },
  { id: "b4", y: "benign", holdout: false, text: "Your password will expire in 14 days. Change it at the company SSO page only." },
  { id: "b5", y: "benign", holdout: false, text: "Build 4419 is green. Release notes are in the repo wiki." },
  { id: "b6", y: "benign", holdout: false, text: "Reminder: badge office closed Monday for the holiday." },
  { id: "b7", y: "benign", holdout: true, text: "THE VPN concentrator will reboot at 01:00. Expect a 5 minute drop." },
  { id: "b8", y: "benign", holdout: true, text: "Shared calendar: incident review moved to 15:30 in the usual room." },
  { id: "p1", y: "phish", holdout: false, text: "Your mailbox is over quota. Open the secure document and sign in to avoid deletion today." },
  { id: "p2", y: "phish", holdout: false, text: "Payroll correction: confirm your direct deposit using the attached portal link before noon." },
  { id: "p3", y: "phish", holdout: false, text: "IT desk: we detected a login issue. Reply with your password so we can resync." },
  { id: "p4", y: "phish", holdout: false, text: "DocuSign completed copy: view the invoice and enter your corporate credentials." },
  { id: "p5", y: "phish", holdout: false, text: "Urgent: the CEO needs gift cards. Buy them now and send the codes on chat. Do not call." },
  { id: "p6", y: "phish", holdout: false, text: "VPN certificate expired. Install this profile from the link to keep working remotely." },
  { id: "p7", y: "phish", holdout: true, text: "Security alert: your account will LOCK in 30 minutes unless you verify at this sign-in page." },
  { id: "p8", y: "phish", holdout: true, text: "Shared file: you were mentioned. Log in with email and password to view the board deck." },
  { id: "a1", y: "alert", holdout: false, text: "EDR: powershell encoded command on host FIN-14, parent is outlook.exe. Severity high." },
  { id: "a2", y: "alert", holdout: false, text: "Identity: 26 failed sign-ins for svc-backup from an unseen ASN, then one success." },
  { id: "a3", y: "alert", holdout: false, text: "Proxy: host DEV-3 posted 2.1 GB to an unclassified storage domain after hours." },
  { id: "a4", y: "alert", holdout: false, text: "DLP: spreadsheet of customer account numbers emailed to a personal domain." },
  { id: "a5", y: "alert", holdout: false, text: "Mail rule created to forward all messages to an external address on user priya." },
  { id: "a6", y: "alert", holdout: false, text: "Token: OAuth app Notes Helper granted Mail.Read and offline access for 40 users in an hour." },
  { id: "a7", y: "alert", holdout: true, text: "EDR: rundll32 spawned from a word document on host HR-2. Child opened a network socket." },
  { id: "a8", y: "alert", holdout: true, text: "Identity protection: unfamiliar OAuth consent for Mail.Send on the finance shared mailbox." },
];

export type DirtyRow = {
  id: string;
  entropy: number | null;
  imports: number | null;
  sections: number | null;
  apis: number | null;
  packed: number | null;
  unsigned: number | null;
  beacons: number | null;
  obfuscation: number | null;
  label: 0 | 1;
};

export function makeCapstoneTable(): DirtyRow[] {
  const base = makeBinaryTelemetry(44).slice(0, 56);
  const rows: DirtyRow[] = base.map((r) => ({
    id: r.id,
    entropy: r.x[0],
    imports: r.x[1],
    sections: r.x[2],
    apis: r.x[3],
    packed: r.x[4],
    unsigned: r.x[5],
    beacons: r.x[6],
    obfuscation: r.x[7],
    label: r.y === "malware" ? 1 : 0,
  }));
  rows[3].entropy = null;
  rows[8].apis = null;
  rows[14].imports = null;
  rows[21].entropy = 99;
  rows[33].entropy = 40;
  rows.push({ ...rows[2], id: rows[2].id });
  rows.push({ ...rows[10], id: rows[10].id });
  return rows;
}

export const CAPSTONE_RAW = makeCapstoneTable();

export const ADV_SAMPLES: { x: number[]; y: 0 | 1 }[] = (() => {
  const rng = mulberry32(51);
  const gauss = () => {
    const u = Math.max(1e-6, rng());
    const v = Math.max(1e-6, rng());
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  const rows: { x: number[]; y: 0 | 1 }[] = [];
  for (let i = 0; i < 36; i++) {
    const mal = i >= 18;
    rows.push({
      y: mal ? 1 : 0,
      x: [
        Math.round(((mal ? 7.2 : 5.8) + gauss() * 0.45) * 100) / 100,
        Math.max(0, Math.round((mal ? 16 : 4) + gauss() * 2.4)),
      ],
    });
  }
  return rows;
})();
