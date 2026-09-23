import { useMemo, useState } from "react";
import { ADV_SAMPLES, BINARY_TELEMETRY, CAPSTONE_RAW, FAMILIES, FAMILY_FEATURES, FLOWS, FLOW_FEATURES, IRIS, IRIS_FEATURES, MALWARE_FEATURES, MESSAGES } from "@/lib/datasets";
import {
  applyScale,
  binaryScores,
  confusion,
  fitLogistic,
  fitNB,
  fitTree,
  fmtNum,
  fmtPct,
  invertScale,
  iqrFences,
  isolationScores,
  kmeans,
  knnPredict,
  linearProba,
  type LinearModel,
  predictNB,
  splitRows,
  tokenize,
  univariateGain,
} from "@/lib/ml";
import { useProgress } from "@/lib/progress";
import { Metric, Slider, Toggle } from "@/components/blocks";

function Scatter({
  points,
  xLabel,
  yLabel,
}: {
  points: { x: number; y: number; mark: "fg" | "bad" | "ok" | "faint"; open?: boolean }[];
  xLabel: string;
  yLabel: string;
}) {
  if (!points.length) return null;
  const xs = points.map((p) => p.x);
  const ys = points.map((p) => p.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  const sx = (v: number) => 36 + ((v - minX) / (maxX - minX || 1)) * 250;
  const sy = (v: number) => 148 - ((v - minY) / (maxY - minY || 1)) * 120;
  const fill = {
    fg: "var(--color-fg)",
    bad: "var(--color-bad)",
    ok: "var(--color-ok)",
    faint: "var(--color-faint)",
  };
  return (
    <svg viewBox="0 0 320 176" className="w-full max-w-md" role="img" aria-label={`${yLabel} against ${xLabel}`}>
      <line x1="36" y1="148" x2="300" y2="148" stroke="var(--color-line)" />
      <line x1="36" y1="20" x2="36" y2="148" stroke="var(--color-line)" />
      {points.map((p, i) => (
        <circle
          key={i}
          cx={sx(p.x)}
          cy={sy(p.y)}
          r={p.open ? 4 : 3.4}
          fill={p.open ? "none" : fill[p.mark]}
          stroke={fill[p.mark]}
          strokeWidth="1.25"
        />
      ))}
      <text x="36" y="168" fill="var(--color-muted)" fontSize="11">
        {xLabel}
      </text>
      <text x="8" y="16" fill="var(--color-muted)" fontSize="11">
        {yLabel}
      </text>
    </svg>
  );
}

function Matrix({ labels, matrix }: { labels: string[]; matrix: number[][] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[16rem] text-left text-sm">
        <thead>
          <tr className="text-muted">
            <th className="py-2 pr-3 font-medium">True \ predicted</th>
            {labels.map((l) => (
              <th key={l} className="px-2 py-2 font-medium">
                {l}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {labels.map((l, i) => (
            <tr key={l} className="border-t border-line">
              <th className="py-2 pr-3 font-medium text-fg">{l}</th>
              {matrix[i].map((n, j) => (
                <td key={j} className={"num px-2 py-2 " + (i === j ? "text-fg" : "text-muted")}>
                  {n}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Run({ onClick, label = "Fit" }: { onClick: () => void; label?: string }) {
  return (
    <button type="button" onClick={onClick} className="min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg">
      {label}
    </button>
  );
}

function Verdict({ passed, text }: { passed: boolean; text: string }) {
  return <p className={"text-sm " + (passed ? "text-ok" : "text-muted")}>{text}</p>;
}

export function IrisBench() {
  const saveLab = useProgress((s) => s.saveLab);
  const setNote = useProgress((s) => s.setNote);
  const [use, setUse] = useState([false, false, true, true]);
  const [scale, setScale] = useState(true);
  const [k, setK] = useState(5);
  const [out, setOut] = useState<null | { acc: number; cm: ReturnType<typeof confusion>; points: { x: number; y: number; mark: "ok" | "bad" }[] }>(null);

  function run() {
    const cols = use.flatMap((on, i) => (on ? [i] : []));
    if (!cols.length) return;
    const rows = IRIS.map((r) => ({ x: cols.map((i) => r.x[i]), y: r.y, full: r.x }));
    const { train, test } = splitRows(rows, 0.3, 7);
    const pred = test.map((row) => knnPredict(train.map((t) => t.x), train.map((t) => t.y), row.x, k, scale));
    const cm = confusion(test.map((t) => t.y), pred);
    const xi = cols.includes(2) ? 2 : cols[0];
    const yi = cols.includes(3) ? 3 : cols[Math.min(1, cols.length - 1)];
    const points = test.map((row, i) => ({
      x: row.full[xi],
      y: row.full[yi],
      mark: (pred[i] === row.y ? "ok" : "bad") as "ok" | "bad",
    }));
    setOut({ acc: cm.accuracy, cm, points });
    const passed = scale && cm.accuracy >= 0.8;
    saveLab("iris", {
      score: cm.accuracy,
      passed,
      detail: `${fmtPct(cm.accuracy)} hold-out, k=${k}, scale ${scale ? "on" : "off"}`,
    });
    if (passed) setNote("a2", true);
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,18rem)_1fr]">
      <div className="space-y-4">
        <p className="text-sm text-muted">Features</p>
        <div className="flex flex-wrap gap-2">
          {IRIS_FEATURES.map((name, i) => (
            <Toggle key={name} label={name} on={use[i]} onChange={(v) => setUse((u) => u.map((x, j) => (j === i ? v : x)))} />
          ))}
        </div>
        <Toggle label="Standardize on the training rows" on={scale} onChange={setScale} />
        <Slider label="Neighbors" min={1} max={11} step={2} value={k} onChange={setK} />
        <Run onClick={run} />
        <p className="text-sm text-muted">Petal measurements separate the species. Sepals alone are a harder control. Scaling is required to clear the field note.</p>
      </div>
      <div className="rounded-xl border border-line bg-surface p-5">
        {out ? (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Metric label="Hold-out accuracy" value={fmtPct(out.acc)} />
              <Metric label="Test rows" value={String(out.cm.matrix.reduce((s, r) => s + r.reduce((a, b) => a + b, 0), 0))} />
            </div>
            <Scatter points={out.points} xLabel="Horizontal feature" yLabel="Vertical" />
            <p className="text-xs text-muted">Filled marks: correct on the hold-out. Clay marks: missed.</p>
            <Matrix labels={out.cm.labels} matrix={out.cm.matrix} />
            <Verdict
              passed={scale && out.acc >= 0.8}
              text={scale && out.acc >= 0.8 ? "Field note 2 cleared." : "Need scaling on and at least 80% hold-out accuracy."}
            />
          </div>
        ) : (
          <p className="text-muted">Fit to see the hold-out. Seed is fixed, so the same settings replay.</p>
        )}
      </div>
    </div>
  );
}

export function MalwarePrepBench() {
  const saveLab = useProgress((s) => s.saveLab);
  const setNote = useProgress((s) => s.setNote);
  const [use, setUse] = useState(MALWARE_FEATURES.map(() => true));
  const fence = useMemo(() => iqrFences(BINARY_TELEMETRY.map((r) => r.x[0])), []);
  const outlierN = BINARY_TELEMETRY.filter((r) => r.x[0] < fence.lo || r.x[0] > fence.hi).length;
  const [out, setOut] = useState<null | ReturnType<typeof binaryScores>>(null);

  function run() {
    const cols = use.flatMap((on, i) => (on ? [i] : []));
    if (!cols.length) return;
    const rows = BINARY_TELEMETRY.map((r) => ({ x: cols.map((i) => r.x[i]), y: r.y === "malware" ? 1 : 0 }));
    const { train, test } = splitRows(rows, 0.3, 11);
    const model = fitLogistic(train.map((r) => r.x), train.map((r) => r.y));
    const probs = test.map((r) => linearProba(model, r.x));
    const scores = binaryScores(test.map((r) => r.y), probs, 0.5);
    setOut(scores);
    const passed = use[3] && scores.recall >= 0.6;
    saveLab("malware-prep", {
      score: scores.f1,
      passed,
      detail: `recall ${fmtPct(scores.recall)}, precision ${fmtPct(scores.precision)}`,
    });
    if (passed) setNote("a3", true);
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-3 sm:grid-cols-3">
        <Metric label="Rows imported" value={String(BINARY_TELEMETRY.length)} />
        <Metric label="Entropy fence" value={`${fmtNum(fence.lo)} – ${fmtNum(fence.hi)}`} />
        <Metric label="Entropy outliers" value={String(outlierN)} />
      </div>
      <div className="overflow-x-auto rounded-xl border border-line">
        <table className="w-full min-w-[36rem] text-left text-sm">
          <thead className="text-muted">
            <tr>
              <th className="px-3 py-2 font-medium">id</th>
              <th className="px-3 py-2 font-medium">entropy</th>
              <th className="px-3 py-2 font-medium">APIs</th>
              <th className="px-3 py-2 font-medium">packed</th>
              <th className="px-3 py-2 font-medium">label</th>
            </tr>
          </thead>
          <tbody>
            {BINARY_TELEMETRY.slice(0, 6).map((r) => (
              <tr key={r.id} className="border-t border-line">
                <td className="num px-3 py-2">{r.id}</td>
                <td className="num px-3 py-2">{fmtNum(r.x[0], 1)}</td>
                <td className="num px-3 py-2">{r.x[3]}</td>
                <td className="num px-3 py-2">{r.x[4]}</td>
                <td className="px-3 py-2">{r.y}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex flex-wrap gap-2">
        {MALWARE_FEATURES.map((name, i) => (
          <Toggle key={name} label={name} on={use[i]} onChange={(v) => setUse((u) => u.map((x, j) => (j === i ? v : x)))} />
        ))}
      </div>
      <Run onClick={run} label="Train logistic regression" />
      {out ? (
        <div className="grid gap-3 sm:grid-cols-4">
          <Metric label="Precision" value={fmtPct(out.precision)} />
          <Metric label="Recall" value={fmtPct(out.recall)} />
          <Metric label="F1" value={fmtPct(out.f1)} />
          <Metric label="False positive rate" value={fmtPct(out.fpr)} />
        </div>
      ) : null}
      <Verdict
        passed={Boolean(out && use[3] && out.recall >= 0.6)}
        text={
          out && use[3] && out.recall >= 0.6
            ? "Field note 3 cleared. Outliers were counted, not convicted."
            : "Keep suspicious APIs in the set and reach 60% malware recall."
        }
      />
    </div>
  );
}

export function FamiliesBench() {
  const saveLab = useProgress((s) => s.saveLab);
  const setNote = useProgress((s) => s.setNote);
  const gain = useMemo(() => univariateGain(FAMILIES.map((r) => r.x), FAMILIES.map((r) => r.y)), []);
  const maxG = Math.max(...gain, 0.001);
  const [out, setOut] = useState<null | { acc: number; rules: string[]; cm: ReturnType<typeof confusion> }>(null);

  function run() {
    const { train, test } = splitRows(FAMILIES, 0.3, 21);
    const tree = fitTree(train.map((r) => r.x), train.map((r) => r.y), [...FAMILY_FEATURES], 3);
    const pred = test.map((r) => tree.predict(r.x));
    const cm = confusion(test.map((r) => r.y), pred);
    setOut({ acc: cm.accuracy, rules: tree.rules.map((r) => r.text), cm });
    const passed = cm.accuracy >= 0.7;
    saveLab("families", { score: cm.accuracy, passed, detail: fmtPct(cm.accuracy) });
    if (passed) setNote("a4", true);
  }

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted">How cleanly one midpoint splits the three families. This is the picture field note 4 asks seaborn to draw.</p>
        <ul className="mt-3 space-y-2">
          {FAMILY_FEATURES.map((name, i) => (
            <li key={name} className="grid grid-cols-[9rem_1fr_3rem] items-center gap-3 text-sm">
              <span>{name}</span>
              <span className="h-2 rounded-full bg-surface-2">
                <span className="block h-2 rounded-full bg-accent" style={{ width: `${(gain[i] / maxG) * 100}%` }} />
              </span>
              <span className="num text-muted">{fmtNum(gain[i], 2)}</span>
            </li>
          ))}
        </ul>
      </div>
      <Run onClick={run} label="Fit a depth-3 tree" />
      {out ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <div>
            <Metric label="Hold-out accuracy" value={fmtPct(out.acc)} />
            <ul className="mt-4 space-y-2 text-sm text-fg/90">
              {out.rules.map((r) => (
                <li key={r} className="border-l border-line pl-3 font-mono text-[13px] leading-relaxed">
                  {r}
                </li>
              ))}
            </ul>
          </div>
          <Matrix labels={out.cm.labels} matrix={out.cm.matrix} />
        </div>
      ) : null}
      <Verdict passed={Boolean(out && out.acc >= 0.7)} text={out && out.acc >= 0.7 ? "Field note 4 cleared." : "Fit the tree and clear 70% on the hold-out."} />
    </div>
  );
}

export function AnomalyBench() {
  const saveLab = useProgress((s) => s.saveLab);
  const setNote = useProgress((s) => s.setNote);
  const [use, setUse] = useState([true, true, true, false]);
  const [method, setMethod] = useState<"iso" | "km">("iso");
  const [cut, setCut] = useState(0.54);
  const [out, setOut] = useState<null | { recall: number; precision: number; points: { x: number; y: number; mark: "ok" | "bad" | "faint"; open?: boolean }[] }>(null);

  function run() {
    const cols = use.flatMap((on, i) => (on ? [i] : []));
    if (!cols.length) return;
    const X = FLOWS.map((r) => cols.map((i) => r.x[i]));
    let flagged: boolean[];
    if (method === "iso") {
      const scores = isolationScores(X, 31, 48);
      flagged = scores.map((s) => s >= cut);
    } else {
      const { dist } = kmeans(X, 2, 5);
      const sorted = dist.slice().sort((a, b) => a - b);
      const thr = sorted[Math.floor(sorted.length * 0.82)] ?? 1;
      flagged = dist.map((d) => d >= Math.max(thr, cut));
    }
    const y = FLOWS.map((r) => r.y === "beacon");
    const tp = y.filter((v, i) => v && flagged[i]).length;
    const fp = y.filter((v, i) => !v && flagged[i]).length;
    const fn = y.filter((v, i) => v && !flagged[i]).length;
    const recall = tp + fn ? tp / (tp + fn) : 0;
    const precision = tp + fp ? tp / (tp + fp) : 0;
    const points = FLOWS.map((r, i) => ({
      x: r.x[0],
      y: r.x[1],
      mark: (r.y === "beacon" ? "bad" : "faint") as "bad" | "faint",
      open: flagged[i],
    }));
    setOut({ recall, precision, points });
    const passed = recall >= 0.5;
    saveLab("anomaly", { score: recall, passed, detail: `${method} recall ${fmtPct(recall)}` });
    if (passed) setNote("a5", true);
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,18rem)_1fr]">
      <div className="space-y-4">
        <div className="flex flex-wrap gap-2">
          <Toggle label="Isolation Forest" on={method === "iso"} onChange={() => setMethod("iso")} />
          <Toggle label="K-means distance" on={method === "km"} onChange={() => setMethod("km")} />
        </div>
        <div className="flex flex-wrap gap-2">
          {FLOW_FEATURES.map((name, i) => (
            <Toggle key={name} label={name} on={use[i]} onChange={(v) => setUse((u) => u.map((x, j) => (j === i ? v : x)))} />
          ))}
        </div>
        <Slider
          label={method === "iso" ? "Score cutoff" : "Distance floor"}
          min={method === "iso" ? 0.45 : 0.4}
          max={method === "iso" ? 0.75 : 2.5}
          step={0.01}
          value={cut}
          onChange={setCut}
          display={fmtNum(cut, 2)}
        />
        <Run onClick={run} label="Score anomalies" />
        <p className="text-sm text-muted">One-Class SVM is the third method in the outline. It is fussy about kernels; the reading is on the Stack page. Rings mark what you flagged. Clay marks are true beacons.</p>
      </div>
      <div className="rounded-xl border border-line bg-surface p-5">
        {out ? (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Metric label="Beacon recall" value={fmtPct(out.recall)} />
              <Metric label="Precision" value={fmtPct(out.precision)} />
            </div>
            <Scatter points={out.points} xLabel="Mean bytes" yLabel="Regularity" />
            <Verdict passed={out.recall >= 0.5} text={out.recall >= 0.5 ? "Field note 5 cleared." : "Recall is under 50%. Regularity and rare port are doing the work, not duration."} />
          </div>
        ) : (
          <p className="text-muted">Duration alone will disappoint you. That is the lab.</p>
        )}
      </div>
    </div>
  );
}

export function NlpBench() {
  const saveLab = useProgress((s) => s.saveLab);
  const setNote = useProgress((s) => s.setNote);
  const [lower, setLower] = useState(true);
  const [punct, setPunct] = useState(true);
  const [stop, setStop] = useState(true);
  const [out, setOut] = useState<null | { acc: number; rows: { id: string; y: string; pred: string; text: string }[] }>(null);

  function run() {
    const opts = { lower, punct, stop };
    const train = MESSAGES.filter((m) => !m.holdout);
    const test = MESSAGES.filter((m) => m.holdout);
    const model = fitNB(train.map((m) => tokenize(m.text, opts)), train.map((m) => m.y));
    const rows = test.map((m) => ({ id: m.id, y: m.y, pred: predictNB(model, tokenize(m.text, opts)), text: m.text }));
    const acc = rows.filter((r) => r.y === r.pred).length / rows.length;
    setOut({ acc, rows });
    const passed = lower && punct && acc >= 0.6;
    saveLab("nlp", { score: acc, passed, detail: fmtPct(acc) });
    if (passed) setNote("a6", true);
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-2">
        <Toggle label="Lowercase" on={lower} onChange={setLower} />
        <Toggle label="Strip punctuation" on={punct} onChange={setPunct} />
        <Toggle label="Drop function words" on={stop} onChange={setStop} />
      </div>
      <Run onClick={run} label="Fit on train, score the hold-out" />
      <p className="max-w-[68ch] text-sm text-muted">
        {MESSAGES.filter((m) => !m.holdout).length} lines train. {MESSAGES.filter((m) => m.holdout).length} stay locked, including two written in capitals so lowercase has a job.
      </p>
      {out ? (
        <>
          <Metric label="Hold-out accuracy" value={fmtPct(out.acc)} />
          <ul className="space-y-3">
            {out.rows.map((r) => (
              <li key={r.id} className="rounded-lg border border-line px-3 py-3 text-sm">
                <p className="text-muted">
                  true {r.y} · predicted {r.pred}
                  {r.y === r.pred ? "" : " · miss"}
                </p>
                <p className="mt-1 text-fg/90">{r.text}</p>
              </li>
            ))}
          </ul>
          <Verdict passed={lower && punct && out.acc >= 0.6} text={lower && punct && out.acc >= 0.6 ? "Field note 6 cleared." : "Turn lowercase and punctuation stripping on, then clear 60%."} />
        </>
      ) : null}
    </div>
  );
}

function evade(raw: number[], model: LinearModel, eps: number, clip: boolean) {
  const z = applyScale(raw, model.mean, model.std);
  let zp = z.map((v, j) => v - eps * Math.sign(model.w[j] || 0));
  if (clip) zp = zp.map((v) => Math.max(-2.2, Math.min(2.2, v)));
  return invertScale(zp, model.mean, model.std);
}

function flips(samples: { x: number[]; y: 0 | 1 }[], model: LinearModel, eps: number, clip: boolean) {
  return samples.filter((s) => {
    const before = linearProba(model, s.x) >= 0.5 ? 1 : 0;
    const after = linearProba(model, evade(s.x, model, eps, clip)) >= 0.5 ? 1 : 0;
    return before !== after;
  }).length;
}

export function AdversarialBench() {
  const saveLab = useProgress((s) => s.saveLab);
  const [eps, setEps] = useState(0.4);
  const [clip, setClip] = useState(false);
  const [retrain, setRetrain] = useState(false);
  const [ran, setRan] = useState(false);

  const base = useMemo(() => fitLogistic(ADV_SAMPLES.map((s) => s.x), ADV_SAMPLES.map((s) => s.y)), []);
  const bareFlips = flips(ADV_SAMPLES, base, eps, false);

  const model = useMemo(() => {
    if (!retrain) return base;
    const extraX = ADV_SAMPLES.map((s) => evade(s.x, base, Math.max(eps, 0.35), false));
    return fitLogistic(
      [...ADV_SAMPLES.map((s) => s.x), ...extraX],
      [...ADV_SAMPLES.map((s) => s.y), ...ADV_SAMPLES.map((s) => s.y)],
    );
  }, [base, retrain, eps]);

  const usedFlips = flips(ADV_SAMPLES, model, eps, clip);
  const points = ADV_SAMPLES.flatMap((s) => {
    const nudged = evade(s.x, model, eps, clip);
    return [
      { x: s.x[0], y: s.x[1], mark: (s.y ? "bad" : "ok") as "bad" | "ok" },
      { x: nudged[0], y: nudged[1], mark: (s.y ? "bad" : "ok") as "bad" | "ok", open: true },
    ];
  });
  const passed = bareFlips >= 1 && (clip || retrain) && usedFlips < bareFlips;

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,18rem)_1fr]">
      <div className="space-y-4">
        <Slider label="Nudge size, standardized units" min={0} max={1.6} step={0.05} value={eps} onChange={setEps} display={fmtNum(eps, 2)} />
        <Toggle label="Clip features to a sane range" on={clip} onChange={setClip} />
        <Toggle label="Refit including the nudged points" on={retrain} onChange={setRetrain} />
        <Run
          label="Record this setting"
          onClick={() => {
            setRan(true);
            saveLab("adversarial", {
              score: 1 - usedFlips / ADV_SAMPLES.length,
              passed,
              detail: `${usedFlips} flips at eps ${fmtNum(eps, 2)}`,
            });
          }}
        />
        <p className="text-sm text-muted">The step moves against the weights, which lowers a malicious score. This is a chart, not a binary editor.</p>
      </div>
      <div className="rounded-xl border border-line bg-surface p-5">
        <div className="grid grid-cols-2 gap-3">
          <Metric label="Flips, no defense" value={String(bareFlips)} />
          <Metric label="Flips, your settings" value={String(usedFlips)} />
        </div>
        <div className="mt-4">
          <Scatter points={points} xLabel="Entropy" yLabel="Suspicious APIs" />
        </div>
        <p className="mt-2 text-xs text-muted">Filled: original dots. Rings: after the nudge. Clay is the malicious class, green is benign.</p>
        <div className="mt-4">
          <Verdict
            passed={ran && passed}
            text={
              passed
                ? ran
                  ? "Bench 06 cleared."
                  : "Defenses are holding. Record the setting to clear the bench."
                : "Raise the nudge until something flips, then turn on a defense that removes at least one flip."
            }
          />
        </div>
      </div>
    </div>
  );
}

const CAP_KEYS = ["entropy", "imports", "sections", "apis", "packed", "unsigned", "beacons", "obfuscation"] as const;
const CAP_LABELS = ["Entropy", "Imports", "Sections", "Suspicious APIs", "Packed", "Unsigned", "Beacon rate", "Obfuscated strings"];

export function CapstoneBench() {
  const saveLab = useProgress((s) => s.saveLab);
  const [dropNull, setDropNull] = useState(false);
  const [clipEntropy, setClipEntropy] = useState(false);
  const [dedupe, setDedupe] = useState(false);
  const [use, setUse] = useState(CAP_KEYS.map(() => true));
  const [threshold, setThreshold] = useState(0.45);
  const [error, setError] = useState("");
  const [out, setOut] = useState<null | ReturnType<typeof binaryScores> & { n: number }>(null);

  const stats = useMemo(() => {
    const ids = new Map<string, number>();
    CAPSTONE_RAW.forEach((r) => ids.set(r.id, (ids.get(r.id) ?? 0) + 1));
    const dupes = [...ids.values()].filter((n) => n > 1).length;
    const nulls = CAPSTONE_RAW.filter((r) => CAP_KEYS.some((k) => r[k] == null)).length;
    const glitches = CAPSTONE_RAW.filter((r) => r.entropy != null && r.entropy > 8).length;
    return { n: CAPSTONE_RAW.length, dupes, nulls, glitches };
  }, []);

  function run() {
    let rows = CAPSTONE_RAW.map((r) => ({ ...r }));
    if (dedupe) {
      const seen = new Set<string>();
      rows = rows.filter((r) => {
        if (seen.has(r.id)) return false;
        seen.add(r.id);
        return true;
      });
    }
    if (clipEntropy) {
      rows = rows.map((r) => (r.entropy != null && r.entropy > 8 ? { ...r, entropy: 8 } : r));
    }
    if (dropNull) {
      rows = rows.filter((r) => CAP_KEYS.every((k) => r[k] != null));
    }
    const cols = CAP_KEYS.flatMap((k, i) => (use[i] ? [k] : []));
    if (cols.length < 2) {
      setError("Pick at least two features.");
      setOut(null);
      return;
    }
    if (rows.some((r) => cols.some((k) => r[k] == null))) {
      setError("Selected columns still contain missing values. Drop incomplete rows.");
      setOut(null);
      return;
    }
    setError("");
    const data = rows.map((r) => ({ x: cols.map((k) => r[k] as number), y: r.label }));
    const { train, test } = splitRows(data, 0.3, 44);
    const model = fitLogistic(train.map((r) => r.x), train.map((r) => r.y), 0.7, 500);
    const probs = test.map((r) => linearProba(model, r.x));
    const scores = binaryScores(test.map((r) => r.y), probs, threshold);
    setOut({ ...scores, n: test.length });
    const cleaned = dropNull && clipEntropy && dedupe;
    const featuresOk = use[0] && use[3] && cols.length >= 4;
    const passed = cleaned && featuresOk && scores.f1 >= 0.72 && scores.fpr < 0.2;
    saveLab("capstone", {
      score: scores.f1,
      passed,
      detail: `F1 ${fmtPct(scores.f1)} at threshold ${fmtNum(threshold, 2)}`,
    });
  }

  const cleaned = dropNull && clipEntropy && dedupe;
  const passed = Boolean(out && cleaned && use[0] && use[3] && use.filter(Boolean).length >= 4 && out.f1 >= 0.72 && out.fpr < 0.2);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Metric label="Export rows" value={String(stats.n)} />
        <Metric label="Duplicate ids" value={String(stats.dupes)} />
        <Metric label="Rows with gaps" value={String(stats.nulls)} />
        <Metric label="Entropy glitches" value={String(stats.glitches)} />
      </div>
      <div className="flex flex-wrap gap-2">
        <Toggle label="Drop incomplete rows" on={dropNull} onChange={setDropNull} />
        <Toggle label="Clip entropy above 8" on={clipEntropy} onChange={setClipEntropy} />
        <Toggle label="Drop duplicate ids" on={dedupe} onChange={setDedupe} />
      </div>
      <div className="flex flex-wrap gap-2">
        {CAP_LABELS.map((name, i) => (
          <Toggle key={name} label={name} on={use[i]} onChange={(v) => setUse((u) => u.map((x, j) => (j === i ? v : x)))} />
        ))}
      </div>
      <div className="max-w-md">
        <Slider label="Page the SOC above this probability" min={0.2} max={0.8} step={0.01} value={threshold} onChange={setThreshold} display={fmtNum(threshold, 2)} />
      </div>
      <Run onClick={run} label="Train the detector" />
      {error ? <p className="text-sm text-bad">{error}</p> : null}
      {out ? (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <Metric label="Hold-out rows" value={String(out.n)} />
          <Metric label="Precision" value={fmtPct(out.precision)} />
          <Metric label="Recall" value={fmtPct(out.recall)} />
          <Metric label="F1" value={fmtPct(out.f1)} />
          <Metric label="False positives" value={String(out.fp)} />
          <Metric label="False positive rate" value={fmtPct(out.fpr)} />
          <Metric label="Missed malware" value={String(out.fn)} />
          <Metric label="True malware" value={String(out.tp)} />
        </div>
      ) : null}
      <Verdict
        passed={passed}
        text={
          passed
            ? "Capstone cleared. You can say what you cleaned, which features you kept, and what the threshold costs."
            : "Clean all three faults, keep entropy and suspicious APIs among at least four features, then reach F1 of 72% with a false-positive rate under 20%."
        }
      />
    </div>
  );
}
