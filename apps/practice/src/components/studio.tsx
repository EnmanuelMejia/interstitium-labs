import { Link } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import { Blocks } from "@/components/blocks";
import { useProgress } from "@/lib/progress";
import { studioBySlug, type Sim } from "@/lib/studios";

function tierOf(load: number) {
  if (load < 0.34) return 0;
  if (load < 0.7) return 1;
  return 2;
}

function Record({
  label,
  onClick,
}: {
  label: string;
  onClick: () => void;
}) {
  return (
    <button type="button" onClick={onClick} className="min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg">
      {label}
    </button>
  );
}

function Verdict({ ok, text }: { ok: boolean; text: string }) {
  return <p className={"text-sm " + (ok ? "text-ok" : "text-muted")}>{text}</p>;
}

export function PathStudio({
  slug,
  load,
  onHold,
}: {
  slug: string;
  load: number;
  onHold: (hold: number | null) => void;
}) {
  const studio = studioBySlug(slug);
  const quiz = useProgress((s) => s.quizzes[`pathq:${slug}`]);
  const lab = useProgress((s) => s.labs[`path:${slug}`]);
  if (!studio) return null;
  const tier = tierOf(load);
  const repair = Boolean(quiz && !quiz.passed);
  const hints = tier === 0 || repair;

  return (
    <div className="mt-12">
      <Blocks blocks={studio.reading} />
      <section className="mt-10 rounded-xl border border-line bg-surface p-4 sm:p-6">
        <div className="flex flex-wrap items-baseline justify-between gap-3">
          <h2 className="text-2xl">Simulation</h2>
          <p className="text-xs tracking-[0.14em] text-muted uppercase">
            {repair ? "Repair · hints stay on" : tier === 0 ? "Quiet" : tier === 1 ? "Working load" : "Stress"}
            {lab?.passed ? " · cleared" : ""}
          </p>
        </div>
        <p className="mt-2 max-w-[68ch] text-sm text-muted">{studio.kicker}</p>
        <div className="mt-6">
          <SimView key={`${slug}-${tier}`} slug={slug} sim={studio.sim} tier={tier} hints={hints} onHold={onHold} />
        </div>
      </section>
    </div>
  );
}

function SimView({
  slug,
  sim,
  tier,
  hints,
  onHold,
}: {
  slug: string;
  sim: Sim;
  tier: number;
  hints: boolean;
  onHold: (hold: number | null) => void;
}) {
  if (sim.kind === "threshold") return <Threshold slug={slug} tier={tier} onHold={onHold} />;
  if (sim.kind === "fringe") return <Fringe slug={slug} items={sim.items} tier={tier} onHold={onHold} />;
  if (sim.kind === "budget") return <Budget slug={slug} tier={tier} hints={hints} onHold={onHold} />;
  if (sim.kind === "fault") return <Fault slug={slug} sim={sim} tier={tier} hints={hints} onHold={onHold} />;
  if (sim.kind === "triage") return <Triage slug={slug} sim={sim} tier={tier} onHold={onHold} />;
  if (sim.kind === "sequence") return <Sequence slug={slug} sim={sim} tier={tier} hints={hints} onHold={onHold} />;
  if (sim.kind === "classify") return <Classify slug={slug} sim={sim} tier={tier} onHold={onHold} />;
  if (sim.kind === "bits") return <Bits slug={slug} need={sim.need} mode={sim.mode} onHold={onHold} />;
  if (sim.kind === "units") return <Units slug={slug} tier={tier} onHold={onHold} />;
  if (sim.kind === "beacon") return <Beacon slug={slug} tier={tier} onHold={onHold} />;
  if (sim.kind === "gpu") return <Gpu slug={slug} tier={tier} onHold={onHold} />;
  if (sim.kind === "reduce") return <Reduce slug={slug} sim={sim} onHold={onHold} />;
  return null;
}

function useSave(slug: string) {
  const saveLab = useProgress((s) => s.saveLab);
  return (passed: boolean, detail: string, score = passed ? 1 : 0) => {
    saveLab(`path:${slug}`, { score, passed, detail });
  };
}

const THRESHOLD_ROWS = [
  { score: 0.92, bad: true },
  { score: 0.88, bad: true },
  { score: 0.81, bad: true },
  { score: 0.74, bad: true },
  { score: 0.66, bad: false },
  { score: 0.61, bad: true },
  { score: 0.55, bad: false },
  { score: 0.42, bad: false },
  { score: 0.33, bad: false },
  { score: 0.21, bad: false },
];

function scoresAt(cut: number) {
  let tp = 0, fp = 0, fn = 0, tn = 0;
  for (const r of THRESHOLD_ROWS) {
    const call = r.score >= cut;
    if (call && r.bad) tp++;
    else if (call && !r.bad) fp++;
    else if (!call && r.bad) fn++;
    else tn++;
  }
  const recall = tp + fn === 0 ? 0 : tp / (tp + fn);
  const fpr = fp + tn === 0 ? 0 : fp / (fp + tn);
  return { tp, fp, fn, tn, recall, fpr };
}

function Threshold({ slug, tier, onHold }: { slug: string; tier: number; onHold: (n: number | null) => void }) {
  const [cut, setCut] = useState(0.5);
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const m = scoresAt(cut);
  const fprCap = tier === 2 ? 0 : 0.21;
  const passed = m.recall >= 0.8 && m.fpr <= fprCap;
  useEffect(() => {
    onHold(passed ? null : Math.min(0.92, Math.max(0.08, 1 - cut)));
  }, [passed, cut, onHold]);
  return (
    <div className="grid gap-6 lg:grid-cols-[16rem_minmax(0,1fr)]">
      <div>
        <label className="block text-sm text-fg">
          Page if score ≥ <span className="num">{cut.toFixed(2)}</span>
          <input
            className="mt-3 w-full accent-fg"
            type="range"
            min={0.2}
            max={0.95}
            step={0.01}
            value={cut}
            onChange={(e) => {
              setCut(Number(e.target.value));
              setRan(false);
            }}
          />
        </label>
        <p className="mt-3 text-sm text-muted">
          {tier === 2 ? "Stress: no false pages. Recall still has to hold at 80%." : "Quiet and working load allow one false page. Recall still has to hold at 80%."}
        </p>
        <div className="mt-4">
          <Record
            label="Record the threshold"
            onClick={() => {
              setRan(true);
              save(passed, `recall ${m.recall.toFixed(2)}, FPR ${m.fpr.toFixed(2)} at ${cut.toFixed(2)}`);
            }}
          />
        </div>
      </div>
      <div>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <Stat label="Recall" value={m.recall.toFixed(2)} />
          <Stat label="False-page rate" value={m.fpr.toFixed(2)} />
          <Stat label="Caught" value={String(m.tp)} />
          <Stat label="False pages" value={String(m.fp)} />
        </div>
        <ul className="mt-4 divide-y divide-line border-y border-line">
          {THRESHOLD_ROWS.map((r) => {
            const page = r.score >= cut;
            return (
              <li key={r.score} className="flex items-baseline justify-between gap-3 py-2 text-sm">
                <span className="num text-muted">{r.score.toFixed(2)}</span>
                <span className="text-fg/80">{r.bad ? "Hostile" : "Benign"}</span>
                <span className={page ? (r.bad ? "text-ok" : "text-bad") : "text-faint"}>{page ? "Page" : "Hold"}</span>
              </li>
            );
          })}
        </ul>
        <div className="mt-4">
          <Verdict
            ok={ran && passed}
            text={
              passed
                ? ran
                  ? "Threshold recorded. The full benches are still the capstone."
                  : "This cut holds. Record it."
                : "Move the cut until recall holds and the false pages fit the load."
            }
          />
        </div>
        <p className="mt-4 flex flex-wrap gap-3">
          <Link to="/" className="inline-flex min-h-11 items-center rounded-md bg-accent px-4 text-sm font-medium text-accent-fg">
            Open the 17 sittings
          </Link>
          <Link to="/lab/$labId" params={{ labId: "capstone" }} className="inline-flex min-h-11 items-center rounded-md border border-line px-4 text-sm">
            Capstone bench
          </Link>
        </p>
      </div>
    </div>
  );
}

function Fringe({
  slug,
  items,
  tier,
  onHold,
}: {
  slug: string;
  items: { prompt: string; choices: string[]; answer: number; path: string }[];
  tier: number;
  onHold: (n: number | null) => void;
}) {
  const shown = items.slice(0, tier === 2 ? items.length : tier === 1 ? 3 : 2);
  const [picks, setPicks] = useState<number[]>(() => shown.map(() => -1));
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const misses = shown.filter((item, i) => picks[i] !== item.answer);
  const need = tier === 2 ? shown.length : Math.max(1, shown.length - 1);
  const correct = shown.length - misses.length;
  const passed = picks.every((p) => p >= 0) && correct >= need;
  useEffect(() => {
    onHold(passed ? null : misses.length / Math.max(1, shown.length));
  }, [passed, misses.length, shown.length, onHold]);
  const fringe = misses[0];
  return (
    <div>
      <ol className="space-y-6">
        {shown.map((item, i) => (
          <li key={item.prompt}>
            <p className="text-fg">{item.prompt}</p>
            <div className="mt-3 grid gap-2">
              {item.choices.map((c, ci) => (
                <button
                  key={c}
                  type="button"
                  onClick={() => {
                    setPicks((prev) => {
                      const next = prev.length === shown.length ? [...prev] : shown.map(() => -1);
                      next[i] = ci;
                      return next;
                    });
                    setRan(false);
                  }}
                  className={
                    "min-h-11 rounded-lg border px-3 py-2 text-left text-sm " +
                    (picks[i] === ci ? "border-fg bg-surface-2 text-fg" : "border-line text-fg/85")
                  }
                >
                  {c}
                </button>
              ))}
            </div>
          </li>
        ))}
      </ol>
      <div className="mt-6 flex flex-wrap items-center gap-3">
        <Record
          label="Record the fringe"
          onClick={() => {
            if (picks.some((p) => p < 0)) return;
            setRan(true);
            save(passed, fringe ? `Fringe → ${fringe.path}` : "No fringe on this set", correct / shown.length);
          }}
        />
        <Verdict
          ok={ran && passed}
          text={
            picks.some((p) => p < 0)
              ? "Answer every probe."
              : passed
                ? fringe
                  ? "Cleared, with a named fringe. That path is the repair, not a restart."
                  : "No miss on this set. Raise the load."
                : "Not yet. The miss is the assignment."
          }
        />
      </div>
      {fringe && picks.every((p) => p >= 0) ? (
        <p className="mt-4 text-sm">
          <Link to="/paths/$slug" params={{ slug: fringe.path }} className="text-fg underline">
            Repair on {fringe.path}
          </Link>
        </p>
      ) : null}
    </div>
  );
}

function Budget({ slug, tier, hints, onHold }: { slug: string; tier: number; hints: boolean; onHold: (n: number | null) => void }) {
  const rps = tier === 0 ? 100 : tier === 1 ? 250 : 1200;
  const days = 30;
  const sloFail = 0.001;
  const allowed = Math.round(rps * 86400 * days * sloFail);
  const spent = Math.round(allowed * 0.4);
  const [guess, setGuess] = useState("");
  const [left, setLeft] = useState("");
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const g = Number(guess.replace(/,/g, ""));
  const l = Number(left.replace(/,/g, ""));
  const budgetOk = Number.isFinite(g) && Math.abs(g - allowed) <= Math.max(1, allowed * 0.01);
  const remainOk = tier === 0 || (Number.isFinite(l) && l === allowed - spent);
  const passed = budgetOk && remainOk;
  useEffect(() => {
    onHold(passed ? null : 0.72);
  }, [passed, onHold]);
  return (
    <div className="max-w-[68ch]">
      <p className="text-fg/90">
        {rps} requests per second. SLO 99.9% over {days} days. How many failed requests are you allowed?
      </p>
      {hints ? (
        <p className="mt-2 text-sm text-muted">
          allowed = rate × 86400 × days × 0.001. {tier === 0 ? `Requests per day: ${rps * 86400}.` : ""}
        </p>
      ) : null}
      <label className="mt-4 block text-sm">
        Allowed failures
        <input
          inputMode="numeric"
          value={guess}
          onChange={(e) => {
            setGuess(e.target.value);
            setRan(false);
          }}
          className="mt-2 block min-h-11 w-full max-w-xs rounded-md border border-line bg-bg px-3 font-mono text-fg"
        />
      </label>
      {tier > 0 ? (
        <label className="mt-4 block text-sm">
          You already spent {spent.toLocaleString()}. How many remain?
          <input
            inputMode="numeric"
            value={left}
            onChange={(e) => {
              setLeft(e.target.value);
              setRan(false);
            }}
            className="mt-2 block min-h-11 w-full max-w-xs rounded-md border border-line bg-bg px-3 font-mono text-fg"
          />
        </label>
      ) : null}
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Record
          label="Check the budget"
          onClick={() => {
            setRan(true);
            save(passed, passed ? `${allowed} allowed` : "arithmetic off");
          }}
        />
        <Verdict ok={ran && passed} text={ran ? (passed ? "Budget holds. The change window knows its count." : "Off by more than a rounding. Check the window and the 0.1%.") : "Enter the count, then check."} />
      </div>
    </div>
  );
}

function Fault({
  slug,
  sim,
  tier,
  hints,
  onHold,
}: {
  slug: string;
  sim: Extract<Sim, { kind: "fault" }>;
  tier: number;
  hints: boolean;
  onHold: (n: number | null) => void;
}) {
  const broken = sim.stages[Math.min(sim.stages.length - 1, tier === 0 ? sim.stages.length - 1 : tier)];
  const [stage, setStage] = useState("");
  const [fix, setFix] = useState("");
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const passed = stage === broken.id && fix === broken.fix;
  const idx = sim.stages.findIndex((s) => s.id === broken.id);
  useEffect(() => {
    onHold(passed ? null : (idx + 0.5) / sim.stages.length);
  }, [passed, idx, sim.stages.length, onHold]);
  const fixes = [...sim.stages.map((s) => s.fix)].sort();
  return (
    <div>
      <p className="text-sm tracking-[0.14em] text-muted uppercase">{sim.system}</p>
      <p className="mt-3 max-w-[68ch] text-fg/90">{broken.symptom}</p>
      {hints ? <p className="mt-2 text-sm text-muted">Quiet load names the neighborhood: look at {broken.name}.</p> : null}
      <div className="mt-4 flex flex-wrap gap-2">
        {sim.stages.map((s) => (
          <button
            key={s.id}
            type="button"
            onClick={() => {
              setStage(s.id);
              setRan(false);
            }}
            className={"min-h-11 rounded-md border px-3 text-sm " + (stage === s.id ? "border-fg bg-surface-2" : "border-line")}
          >
            {s.name}
          </button>
        ))}
      </div>
      <div className="mt-4 grid gap-2">
        {fixes.map((f) => (
          <button
            key={f}
            type="button"
            onClick={() => {
              setFix(f);
              setRan(false);
            }}
            className={"min-h-11 rounded-lg border px-3 py-2 text-left text-sm " + (fix === f ? "border-fg bg-surface-2" : "border-line text-fg/85")}
          >
            {f}
          </button>
        ))}
      </div>
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Record
          label="Apply the repair"
          onClick={() => {
            setRan(true);
            save(passed, passed ? broken.name : "wrong gate");
          }}
        />
        <Verdict ok={ran && passed} text={ran ? (passed ? "The gate opens. The packet can move." : "That repair belongs to a different station.") : "Pick the station and the repair."} />
      </div>
    </div>
  );
}

function Triage({
  slug,
  sim,
  tier,
  onHold,
}: {
  slug: string;
  sim: Extract<Sim, { kind: "triage" }>;
  tier: number;
  onHold: (n: number | null) => void;
}) {
  const cases = sim.cases.slice(0, 1 + tier);
  const [picks, setPicks] = useState<number[]>(() => cases.map(() => -1));
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const passed = cases.every((c, i) => c.choices[picks[i]]?.right);
  useEffect(() => {
    onHold(passed ? null : 0.66);
  }, [passed, onHold]);
  return (
    <div>
      <h3 className="text-lg">{sim.title}</h3>
      <ol className="mt-4 space-y-6">
        {cases.map((c, i) => (
          <li key={c.log}>
            <p className="font-mono text-sm text-fg/90">{c.log}</p>
            <div className="mt-3 grid gap-2">
              {c.choices.map((choice, ci) => (
                <button
                  key={choice.label}
                  type="button"
                  onClick={() => {
                    setPicks((prev) => {
                      const next = prev.length === cases.length ? [...prev] : cases.map(() => -1);
                      next[i] = ci;
                      return next;
                    });
                    setRan(false);
                  }}
                  className={"min-h-11 rounded-lg border px-3 py-2 text-left text-sm " + (picks[i] === ci ? "border-fg bg-surface-2" : "border-line")}
                >
                  {choice.label}
                </button>
              ))}
            </div>
            {ran && picks[i] >= 0 ? <p className="mt-2 text-sm text-muted">{c.choices[picks[i]].why}</p> : null}
          </li>
        ))}
      </ol>
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Record
          label="Record the triage"
          onClick={() => {
            if (picks.some((p) => p < 0)) return;
            setRan(true);
            save(passed, passed ? sim.title : "wrong object");
          }}
        />
        <Verdict ok={ran && passed} text={picks.some((p) => p < 0) ? "Choose an action for each scrap." : ran && passed ? "The object you changed is the one the event named." : ran ? "Read the event again. One of these actions treats a different object." : ""} />
      </div>
    </div>
  );
}

function Sequence({
  slug,
  sim,
  tier,
  hints,
  onHold,
}: {
  slug: string;
  sim: Extract<Sim, { kind: "sequence" }>;
  tier: number;
  hints: boolean;
  onHold: (n: number | null) => void;
}) {
  const [picked, setPicked] = useState<string[]>([]);
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const passed = picked.length === sim.order.length && picked.every((id, i) => id === sim.order[i]);
  useEffect(() => {
    const at = picked.length === 0 ? 0.15 : picked.length / sim.order.length;
    onHold(passed ? null : at);
  }, [passed, picked.length, sim.order.length, onHold]);
  const remain = sim.steps.filter((s) => !picked.includes(s.id));
  return (
    <div>
      <h3 className="text-lg">{sim.title}</h3>
      <p className="mt-2 max-w-[68ch] text-sm text-muted">{sim.intro}</p>
      {hints ? <p className="mt-2 text-sm text-muted">Quiet load: there are {sim.order.length} stations. Undo is allowed.</p> : null}
      {tier === 2 ? <p className="mt-2 text-sm text-warn">Stress: one wrong station and you should undo before you record.</p> : null}
      <ol className="mt-4 space-y-2">
        {picked.map((id, i) => {
          const step = sim.steps.find((s) => s.id === id);
          return (
            <li key={id} className="flex items-center justify-between gap-3 rounded-lg border border-line px-3 py-2 text-sm">
              <span>
                <span className="num text-muted">{i + 1}. </span>
                {step?.label}
              </span>
            </li>
          );
        })}
      </ol>
      <div className="mt-3 flex flex-wrap gap-2">
        {remain.map((s) => (
          <button
            key={s.id}
            type="button"
            onClick={() => {
              setPicked((p) => [...p, s.id]);
              setRan(false);
            }}
            className="min-h-11 rounded-md border border-line px-3 text-left text-sm"
          >
            {s.label}
          </button>
        ))}
        {picked.length > 0 ? (
          <button type="button" onClick={() => { setPicked((p) => p.slice(0, -1)); setRan(false); }} className="min-h-11 rounded-md px-3 text-sm text-muted">
            Undo
          </button>
        ) : null}
      </div>
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Record
          label="Record the order"
          onClick={() => {
            setRan(true);
            save(passed, passed ? "order holds" : "wrong order");
          }}
        />
        <Verdict ok={ran && passed} text={ran ? (passed ? "That is the order a careful operator uses." : "A station is early or late. Undo and place it again.") : "Place every station."} />
      </div>
    </div>
  );
}

function Classify({
  slug,
  sim,
  tier,
  onHold,
}: {
  slug: string;
  sim: Extract<Sim, { kind: "classify" }>;
  tier: number;
  onHold: (n: number | null) => void;
}) {
  const cards = sim.cards.slice(0, tier === 0 ? Math.max(3, sim.cards.length - 2) : tier === 1 ? Math.max(4, sim.cards.length - 1) : sim.cards.length);
  const [picks, setPicks] = useState<Record<string, string>>({});
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const passed = cards.every((c) => picks[c.id] === c.bucket);
  useEffect(() => {
    const done = cards.filter((c) => picks[c.id] === c.bucket).length;
    onHold(passed ? null : 1 - done / cards.length);
  }, [passed, cards, picks, onHold]);
  return (
    <div>
      <h3 className="text-lg">{sim.title}</h3>
      <p className="mt-2 max-w-[68ch] text-sm text-muted">{sim.intro}</p>
      <ul className="mt-4 space-y-4">
        {cards.map((c) => (
          <li key={c.id} className="rounded-lg border border-line p-3">
            <p className="text-sm text-fg/90">{c.text}</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {sim.buckets.map((b) => (
                <button
                  key={b.id}
                  type="button"
                  onClick={() => {
                    setPicks((prev) => ({ ...prev, [c.id]: b.id }));
                    setRan(false);
                  }}
                  className={"min-h-11 rounded-md border px-3 text-sm " + (picks[c.id] === b.id ? "border-fg bg-surface-2" : "border-line text-muted")}
                >
                  {b.label}
                </button>
              ))}
            </div>
          </li>
        ))}
      </ul>
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Record
          label="Record the sort"
          onClick={() => {
            setRan(true);
            save(passed, passed ? sim.title : "a card is in the wrong bucket");
          }}
        />
        <Verdict ok={ran && passed} text={ran ? (passed ? "Every card is in the bucket that matches the rule." : "One card is in the wrong bucket. The rule is in the reading.") : "Sort every card."} />
      </div>
    </div>
  );
}

function Bits({ slug, need, mode, onHold }: { slug: string; need: string; mode: string; onHold: (n: number | null) => void }) {
  const [bits, setBits] = useState<[boolean, boolean, boolean][]>([
    [false, false, false],
    [false, false, false],
    [false, false, false],
  ]);
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const oct = bits
    .map((row) => row.reduce((n, on, i) => n + (on ? 1 << (2 - i) : 0), 0))
    .join("");
  const passed = oct === mode;
  useEffect(() => {
    onHold(passed ? null : 0.55);
  }, [passed, onHold]);
  const labels = ["r", "w", "x"];
  return (
    <div>
      <p className="max-w-[68ch] text-fg/90">{need}</p>
      <div className="mt-4 overflow-x-auto">
        <table className="text-sm">
          <thead>
            <tr className="text-left text-muted">
              <th className="pr-4 font-normal"> </th>
              {labels.map((l) => (
                <th key={l} className="px-2 font-normal">{l}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {["user", "group", "other"].map((who, ri) => (
              <tr key={who}>
                <td className="py-1 pr-4 text-muted">{who}</td>
                {bits[ri].map((on, ci) => (
                  <td key={labels[ci]} className="px-2 py-1">
                    <button
                      type="button"
                      aria-pressed={on}
                      onClick={() => {
                        setBits((prev) => {
                          const next = prev.map((row) => [...row]) as [boolean, boolean, boolean][];
                          next[ri][ci] = !next[ri][ci];
                          return next;
                        });
                        setRan(false);
                      }}
                      className={"min-h-11 min-w-11 rounded-md border " + (on ? "border-fg bg-surface-2 text-fg" : "border-line text-faint")}
                    >
                      {on ? "on" : "off"}
                    </button>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="num mt-3 text-sm text-muted">mode {oct}</p>
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Record
          label="Set the mode"
          onClick={() => {
            setRan(true);
            save(passed, `mode ${oct}`);
          }}
        />
        <Verdict ok={ran && passed} text={ran ? (passed ? `${mode}. Others stay out.` : `${oct} is not the mode this file needs.`) : "Toggle the bits, then set it."} />
      </div>
    </div>
  );
}

const UNIT_CASES = [
  {
    log: "The unit is running. After a reboot it is gone.",
    choices: [
      { label: "systemctl enable — wire it for the next boot", right: true, why: "start already happened. enable is the missing verb." },
      { label: "chmod 777 the unit file", why: "Permissions are not why it skipped boot." },
      { label: "systemctl start again, and assume reboot will remember", why: "start does not persist." },
    ],
  },
  {
    log: "You need it now, and you also need it after reboot. It is currently stopped and disabled.",
    choices: [
      { label: "enable --now", right: true, why: "One verb for now, one for the next boot." },
      { label: "Only enable", why: "It will still be stopped until the next boot." },
      { label: "Only start", why: "The next boot will not bring it back." },
    ],
  },
  {
    log: "The host will not reach multi-user. You need a root shell to repair the unit.",
    choices: [
      { label: "Boot to an emergency or rescue target you have practiced", right: true, why: "You need a target, not another start of the broken unit." },
      { label: "Add a second replica", why: "This is a machine, not a Deployment." },
      { label: "Turn the unit world-executable", why: "That is not a boot repair." },
    ],
  },
];

function Units({ slug, tier, onHold }: { slug: string; tier: number; onHold: (n: number | null) => void }) {
  const cases = UNIT_CASES.slice(0, 1 + tier);
  const [picks, setPicks] = useState<number[]>(() => cases.map(() => -1));
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const passed = cases.every((c, i) => c.choices[picks[i]]?.right);
  useEffect(() => {
    onHold(passed ? null : 0.48);
  }, [passed, onHold]);
  return (
    <div>
      <ol className="space-y-6">
        {cases.map((c, i) => (
          <li key={c.log}>
            <p className="text-fg/90">{c.log}</p>
            <div className="mt-3 grid gap-2">
              {c.choices.map((choice, ci) => (
                <button
                  key={choice.label}
                  type="button"
                  onClick={() => {
                    setPicks((prev) => {
                      const next = prev.length === cases.length ? [...prev] : cases.map(() => -1);
                      next[i] = ci;
                      return next;
                    });
                    setRan(false);
                  }}
                  className={"min-h-11 rounded-lg border px-3 py-2 text-left text-sm " + (picks[i] === ci ? "border-fg bg-surface-2" : "border-line")}
                >
                  {choice.label}
                </button>
              ))}
            </div>
            {ran && picks[i] >= 0 ? <p className="mt-2 text-sm text-muted">{c.choices[picks[i]].why}</p> : null}
          </li>
        ))}
      </ol>
      <div className="mt-4">
        <Record
          label="Record the verbs"
          onClick={() => {
            if (picks.some((p) => p < 0)) return;
            setRan(true);
            save(passed, passed ? "enable and start distinguished" : "wrong verb");
          }}
        />
        <div className="mt-3">
          <Verdict ok={ran && passed} text={picks.some((p) => p < 0) ? "Pick a verb for each scrap." : ran && passed ? "Start, enable, and the rescue target are different tools." : ran ? "One verb is doing the wrong job." : ""} />
        </div>
      </div>
    </div>
  );
}

const HOSTS = [
  { id: "h1", gaps: [30, 30, 30, 30], beacon: true },
  { id: "h2", gaps: [30, 31, 29, 30], beacon: true },
  { id: "h3", gaps: [2, 40, 3, 90], beacon: false },
  { id: "h4", gaps: [45, 44, 46, 45], beacon: true },
  { id: "h5", gaps: [8, 80, 12, 70], beacon: false },
  { id: "h6", gaps: [12, 12, 13, 12], beacon: true },
];

function stdev(xs: number[]) {
  const mean = xs.reduce((a, b) => a + b, 0) / xs.length;
  const v = xs.reduce((a, b) => a + (b - mean) ** 2, 0) / xs.length;
  return Math.sqrt(v);
}

function Beacon({ slug, tier, onHold }: { slug: string; tier: number; onHold: (n: number | null) => void }) {
  const [tol, setTol] = useState(2);
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const calls = useMemo(
    () =>
      HOSTS.map((h) => ({
        ...h,
        call: stdev(h.gaps) <= tol && h.gaps.length >= 4,
      })),
    [tol],
  );
  const tp = calls.filter((c) => c.call && c.beacon).length;
  const fp = calls.filter((c) => c.call && !c.beacon).length;
  const fn = calls.filter((c) => !c.call && c.beacon).length;
  const recall = tp / (tp + fn || 1);
  const precision = tp + fp === 0 ? 0 : tp / (tp + fp);
  const passed = tier === 2 ? fn === 0 && fp === 0 : recall >= 0.75 && precision >= 0.75;
  useEffect(() => {
    onHold(passed ? null : 0.2 + fp * 0.15 + fn * 0.1);
  }, [passed, fp, fn, onHold]);
  return (
    <div>
      <label className="block text-sm">
        Max gap jitter (stdev, seconds) <span className="num">{tol.toFixed(1)}</span>
        <input
          className="mt-3 w-full max-w-md accent-fg"
          type="range"
          min={0}
          max={20}
          step={0.5}
          value={tol}
          onChange={(e) => {
            setTol(Number(e.target.value));
            setRan(false);
          }}
        />
      </label>
      <p className="mt-2 text-sm text-muted">
        A host is a beacon when the gaps between its calls stay inside this jitter. {tier === 2 ? "Stress wants every beacon and no benign host." : "Working load wants recall and precision both at 75%."}
      </p>
      <ul className="mt-4 divide-y divide-line border-y border-line">
        {calls.map((h) => (
          <li key={h.id} className="flex flex-wrap items-baseline justify-between gap-3 py-2 text-sm">
            <span className="num text-muted">{h.id}</span>
            <span className="font-mono text-fg/80">{h.gaps.join(", ")}</span>
            <span className={h.call ? "text-warn" : "text-faint"}>{h.call ? "Case" : "Quiet"}</span>
          </li>
        ))}
      </ul>
      <p className="num mt-3 text-sm text-muted">
        recall {recall.toFixed(2)} · precision {precision.toFixed(2)}
      </p>
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Record
          label="Record the rule"
          onClick={() => {
            setRan(true);
            save(passed, `jitter ${tol}`, recall);
          }}
        />
        <Verdict ok={ran && passed} text={passed ? (ran ? "The rule separates regularity from noise." : "This jitter holds. Record it.") : "Too tight and you miss beacons. Too loose and benign hosts become cases."} />
      </div>
    </div>
  );
}

const JOBS = [
  {
    name: "Tabular model, 8,000 rows",
    deadline: "before lunch (4 hours)",
    cpuH: 0.07,
    gpuH: 0.05,
    cpuPrice: 0.05,
    gpuPrice: 3,
    pick: "cpu" as const,
    why: "Both finish immediately. The GPU's hourly price is the whole story.",
  },
  {
    name: "Wide training run, repeated epochs",
    deadline: "overnight, 8 hours",
    cpuH: 40,
    gpuH: 1.2,
    cpuPrice: 0.05,
    gpuPrice: 3,
    pick: "gpu" as const,
    why: "The CPU misses the deadline. The GPU costs more per hour and still wins the clock.",
  },
];

function Gpu({ slug, tier, onHold }: { slug: string; tier: number; onHold: (n: number | null) => void }) {
  const jobs = JOBS.slice(0, tier === 0 ? 1 : 2);
  const [picks, setPicks] = useState<Record<string, "cpu" | "gpu" | "">>({});
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const passed = jobs.every((j) => picks[j.name] === j.pick);
  useEffect(() => {
    onHold(passed ? null : 0.8);
  }, [passed, onHold]);
  return (
    <div className="space-y-4">
      {jobs.map((j) => {
        const cpuCost = j.cpuH * j.cpuPrice;
        const gpuCost = j.gpuH * j.gpuPrice;
        return (
          <div key={j.name} className="rounded-lg border border-line p-3">
            <p className="text-fg">{j.name}</p>
            <p className="mt-1 text-sm text-muted">Deadline: {j.deadline}</p>
            <p className="num mt-2 text-sm text-muted">
              CPU {j.cpuH}h × ${j.cpuPrice}/h = ${cpuCost.toFixed(2)} · GPU {j.gpuH}h × ${j.gpuPrice}/h = ${gpuCost.toFixed(2)}
            </p>
            <div className="mt-3 flex gap-2">
              {(["cpu", "gpu"] as const).map((d) => (
                <button
                  key={d}
                  type="button"
                  onClick={() => {
                    setPicks((p) => ({ ...p, [j.name]: d }));
                    setRan(false);
                  }}
                  className={"min-h-11 rounded-md border px-3 text-sm uppercase " + (picks[j.name] === d ? "border-fg bg-surface-2" : "border-line")}
                >
                  {d}
                </button>
              ))}
            </div>
            {ran ? <p className="mt-2 text-sm text-muted">{j.why}</p> : null}
          </div>
        );
      })}
      <Record
        label="Record the devices"
        onClick={() => {
          setRan(true);
          save(passed, passed ? "clock and bill" : "wrong device");
        }}
      />
      <Verdict ok={ran && passed} text={ran ? (passed ? "You paid for a deadline, not for a logo." : "One job missed either the clock or the bill.") : "Pick a device for each job."} />
    </div>
  );
}

function Reduce({
  slug,
  sim,
  onHold,
}: {
  slug: string;
  sim: Extract<Sim, { kind: "reduce" }>;
  onHold: (n: number | null) => void;
}) {
  const [cur, setCur] = useState(sim.start);
  const [log, setLog] = useState<string[]>([]);
  const [ran, setRan] = useState(false);
  const save = useSave(slug);
  const passed = cur === sim.goal;
  useEffect(() => {
    onHold(passed ? null : Math.min(0.9, 0.25 + log.length * 0.15));
  }, [passed, log.length, onHold]);
  return (
    <div>
      <p className="text-sm text-muted">
        Start <span className="num text-fg">{sim.start}</span>. Stop at <span className="num text-fg">{sim.goal}</span>. A rule that does not match does not fire.
      </p>
      <p className="num mt-4 text-3xl text-fg">{cur}</p>
      <div className="mt-4 flex flex-wrap gap-2">
        {sim.rules.map((r) => (
          <button
            key={r.id}
            type="button"
            onClick={() => {
              setRan(false);
              if (!cur.includes(r.from)) {
                setLog((l) => [...l, `${r.label} — no match`]);
                return;
              }
              setCur((c) => c.replace(r.from, r.to));
              setLog((l) => [...l, r.label]);
            }}
            className="min-h-11 rounded-md border border-line px-3 font-mono text-sm"
          >
            {r.label}
          </button>
        ))}
        <button
          type="button"
          onClick={() => {
            setCur(sim.start);
            setLog([]);
            setRan(false);
          }}
          className="min-h-11 rounded-md px-3 text-sm text-muted"
        >
          Reset
        </button>
      </div>
      <ul className="mt-4 space-y-1 text-sm text-muted">
        {log.slice(-4).map((line, i) => (
          <li key={`${line}-${i}`}>{line}</li>
        ))}
      </ul>
      <div className="mt-4">
        <Record
          label="Record the reduction"
          onClick={() => {
            setRan(true);
            save(passed, passed ? "stopped" : cur);
          }}
        />
        <div className="mt-3">
          <Verdict ok={ran && passed} text={passed ? "The stop token is the rule you wrote, not the picture." : ran ? "You have not reached the stop token." : "Reduce, then record."} />
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-bg px-3 py-3">
      <p className="text-xs tracking-[0.12em] text-muted uppercase">{label}</p>
      <p className="num mt-1 text-xl">{value}</p>
    </div>
  );
}
