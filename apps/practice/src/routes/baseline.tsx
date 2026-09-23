import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { bandCopy, bandOf, BASELINE_LENGTH, nextItem, stepTheta, type MathItem } from "@/lib/baseline";
import { useProgress } from "@/lib/progress";

export const Route = createFileRoute("/baseline")({
  component: BaselinePage,
});

function BaselinePage() {
  const saved = useProgress((s) => s.baseline);
  const setBaseline = useProgress((s) => s.setBaseline);
  const [theta, setTheta] = useState(0);
  const [used, setUsed] = useState<string[]>([]);
  const [pick, setPick] = useState(-1);
  const [done, setDone] = useState(false);
  const [current, setCurrent] = useState<MathItem | null>(() => nextItem(0, []));

  function commit() {
    if (!current || pick < 0) return;
    const correct = pick === current.answer;
    const nextTheta = stepTheta(theta, correct);
    const nextUsed = [...used, current.id];
    if (nextUsed.length >= BASELINE_LENGTH) {
      const band = bandOf(nextTheta);
      setTheta(nextTheta);
      setUsed(nextUsed);
      setDone(true);
      setCurrent(null);
      setBaseline({ theta: nextTheta, band, asked: nextUsed.length });
      return;
    }
    setTheta(nextTheta);
    setUsed(nextUsed);
    setPick(-1);
    setCurrent(nextItem(nextTheta, nextUsed));
  }

  function retake() {
    setTheta(0);
    setUsed([]);
    setPick(-1);
    setDone(false);
    setCurrent(nextItem(0, []));
  }

  const band = done ? bandOf(theta) : saved?.band;

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Math · baseline</p>
      <h1 className="mt-3 max-w-[14ch] text-hero leading-[0.95]">Eight items, then a band</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        A computer-adaptive placement. A correct answer raises the next item. A miss lowers it. No timer, no cohort, no
        score you can buy. The band says where the ops-math reading should start.
      </p>
      {saved && !done && used.length === 0 ? (
        <p className="mt-4 text-sm text-muted">
          Last band on this device: {saved.band}. {bandCopy[saved.band]}
        </p>
      ) : null}
      {current && !done ? (
        <section className="mt-8 max-w-[68ch] rounded-xl border border-line bg-surface p-5">
          <p className="num text-xs tracking-[0.14em] text-muted uppercase">
            {used.length + 1} / {BASELINE_LENGTH} · {current.topic}
          </p>
          <h2 className="mt-3 text-2xl">{current.prompt}</h2>
          <div className="mt-4 grid gap-2">
            {current.choices.map((choice, i) => (
              <button
                key={choice}
                type="button"
                onClick={() => setPick(i)}
                className={
                  "min-h-11 rounded-lg border px-3 py-2 text-left text-sm " +
                  (pick === i ? "border-fg bg-surface-2 text-fg" : "border-line text-fg/85")
                }
              >
                {choice}
              </button>
            ))}
          </div>
          <button
            type="button"
            disabled={pick < 0}
            onClick={commit}
            className="mt-4 min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg disabled:opacity-40"
          >
            Commit
          </button>
        </section>
      ) : null}
      {done && band ? (
        <section className="mt-8 max-w-[68ch] rounded-xl border border-line bg-surface p-5">
          <p className="text-xs tracking-[0.14em] text-muted uppercase">Band</p>
          <h2 className="mt-2 text-3xl capitalize">{band}</h2>
          <p className="mt-3 text-fg/90">{bandCopy[band]}</p>
          <div className="mt-4 flex flex-wrap gap-3">
            <Link to="/ladders" className="inline-flex min-h-11 items-center rounded-md bg-accent px-4 text-sm font-medium text-accent-fg">
              Open the roads
            </Link>
            <button type="button" onClick={retake} className="min-h-11 rounded-md border border-line px-4 text-sm">
              Retake
            </button>
          </div>
        </section>
      ) : null}
    </main>
  );
}
