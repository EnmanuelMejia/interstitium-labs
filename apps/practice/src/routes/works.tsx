import { createFileRoute, Link } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Run } from "@/components/run";
import { evalAt, evalRows, passages, practiceExam, retrievalAnswer, retrievalQuery, runSteps } from "@/lib/works";
import { useProgress } from "@/lib/progress";

export const Route = createFileRoute("/works")({
  component: WorksPage,
});

function pct(n: number) {
  return `${Math.round(n * 100)}%`;
}

function WorksPage() {
  const saveQuiz = useProgress((s) => s.saveQuiz);
  const saveLab = useProgress((s) => s.saveLab);
  const obsession = useProgress((s) => s.obsession);
  const setObsession = useProgress((s) => s.setObsession);
  const build = useProgress((s) => s.build);
  const setBuild = useProgress((s) => s.setBuild);
  const [picks, setPicks] = useState<number[]>(() => practiceExam.map(() => -1));
  const [checked, setChecked] = useState(false);
  const [passage, setPassage] = useState("");
  const [threshold, setThreshold] = useState(0.9);
  const scores = useMemo(() => evalAt(threshold), [threshold]);
  const examCorrect = practiceExam.filter((item, i) => picks[i] === item.answer).length;
  const examPassed = examCorrect === practiceExam.length;

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Works · open</p>
      <h1 className="mt-3 max-w-[16ch] text-hero leading-[0.95]">Understand it, run it, then build</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        One business bootcamp builds a single system, then another, across three levels. The San Francisco academy
        asks for one obsession and proof the thing exists. Those are the methods. Their videos, their campus calendar,
        and their certificates are not here. These runs, labs, and the practice exam are original and released under
        CC BY 4.0.
      </p>

      <section className="mt-10">
        <h2 className="text-3xl">Understand</h2>
        <p className="mt-3 max-w-[68ch] text-muted">Play the run. Then sit the practice exam. Four of four to clear it.</p>
        <div className="mt-4 max-w-3xl">
          <Run steps={runSteps} />
        </div>
        <ol className="mt-6 max-w-[68ch] space-y-6">
          {practiceExam.map((item, qi) => (
            <li key={item.q}>
              <p>{item.q}</p>
              <div className="mt-3 grid gap-2">
                {item.choices.map((choice, ci) => {
                  const on = picks[qi] === ci;
                  const show = checked && on;
                  return (
                    <button
                      key={choice}
                      type="button"
                      onClick={() => {
                        setPicks((prev) => prev.map((value, i) => (i === qi ? ci : value)));
                        setChecked(false);
                      }}
                      className={
                        "min-h-11 rounded-lg border px-3 py-2 text-left text-sm " +
                        (show && ci === item.answer ? "border-ok text-ok" : show ? "border-bad text-bad" : on ? "border-fg bg-surface-2" : "border-line")
                      }
                    >
                      {choice}
                    </button>
                  );
                })}
              </div>
              {checked && picks[qi] !== -1 ? <p className="mt-2 text-sm text-muted">{item.why}</p> : null}
            </li>
          ))}
        </ol>
        <button
          type="button"
          className="mt-4 min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg"
          onClick={() => {
            if (picks.some((pick) => pick < 0)) return;
            setChecked(true);
            saveQuiz("works:exam", { correct: examCorrect, total: practiceExam.length, passed: examPassed });
          }}
        >
          {checked ? `${examCorrect}/${practiceExam.length}` : "Score the practice exam"}
        </button>
      </section>

      <section className="mt-14 max-w-[68ch]">
        <h2 className="text-3xl">Implement</h2>
        <p className="mt-3 text-muted">{retrievalQuery}</p>
        <div className="mt-4 grid gap-2">
          {passages.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => {
                setPassage(item.id);
                const passed = item.id === retrievalAnswer;
                saveLab("works:retrieval", { score: passed ? 1 : 0, passed, detail: item.id });
              }}
              className={
                "min-h-11 rounded-lg border px-3 py-3 text-left text-sm " +
                (passage === item.id && item.id === retrievalAnswer
                  ? "border-ok text-ok"
                  : passage === item.id
                    ? "border-bad text-bad"
                    : "border-line")
              }
            >
              {item.text}
            </button>
          ))}
        </div>
      </section>

      <section className="mt-14 max-w-[68ch]">
        <h2 className="text-3xl">Systemize</h2>
        <p className="mt-3 text-muted">
          Six scores. Page when the score is at or above the line. Clear it with precision at least 60% and recall at least 66%.
        </p>
        <label className="mt-4 block text-sm">
          <span className="flex justify-between text-muted">
            <span>Line</span>
            <span className="num text-fg">{threshold.toFixed(2)}</span>
          </span>
          <input
            className="mt-2 h-11 w-full"
            type="range"
            min={0.1}
            max={0.95}
            step={0.01}
            value={threshold}
            onChange={(e) => {
              const next = Number(e.target.value);
              setThreshold(next);
              const result = evalAt(next);
              saveLab("works:eval", {
                score: result.precision,
                passed: result.passed,
                detail: `${pct(result.precision)} / ${pct(result.recall)}`,
              });
            }}
          />
        </label>
        <p className="num mt-3 text-sm text-muted">
          Precision {pct(scores.precision)} · recall {pct(scores.recall)} · {scores.passed ? "cleared" : "not yet"}
        </p>
        <ul className="mt-3 text-sm text-muted">
          {evalRows.map((row) => (
            <li key={row.p}>
              score {row.p.toFixed(2)} · truth {row.y ? "positive" : "negative"} · {row.p >= threshold ? "page" : "hold"}
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-14 max-w-[68ch]">
        <h2 className="text-3xl">The build</h2>
        <p className="mt-3 text-muted">
          One thing, named. Who it is for. How you will know it failed. No term dates, no city requirement, no admission
          office. Noah can hold the name. The proof stays on this device.
        </p>
        <label className="mt-4 block text-sm text-muted" htmlFor="obsession-works">
          The work
        </label>
        <input
          id="obsession-works"
          value={obsession}
          onChange={(e) => setObsession(e.target.value)}
          maxLength={140}
          className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm"
        />
        <label className="mt-4 block text-sm text-muted" htmlFor="artifact">
          The artifact someone can run
        </label>
        <input
          id="artifact"
          value={build.artifact}
          onChange={(e) => setBuild({ artifact: e.target.value.slice(0, 160) })}
          className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm"
        />
        <label className="mt-4 block text-sm text-muted" htmlFor="who">
          Who uses it
        </label>
        <input
          id="who"
          value={build.who}
          onChange={(e) => setBuild({ who: e.target.value.slice(0, 160) })}
          className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm"
        />
        <label className="mt-4 block text-sm text-muted" htmlFor="fails">
          How it fails in the open
        </label>
        <input
          id="fails"
          value={build.fails}
          onChange={(e) => setBuild({ fails: e.target.value.slice(0, 160) })}
          className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm"
        />
        <div className="mt-4 flex flex-wrap gap-3">
          <Link to="/muse" className="inline-flex min-h-11 items-center rounded-md bg-accent px-4 text-sm font-medium text-accent-fg">
            Take it to Noah
          </Link>
          <a className="inline-flex min-h-11 items-center text-sm underline" href="https://huggingface.co/learn" target="_blank" rel="noreferrer">
            Hugging Face course
          </a>
          <a className="inline-flex min-h-11 items-center text-sm underline" href="https://ocw.mit.edu/" target="_blank" rel="noreferrer">
            MIT OpenCourseWare
          </a>
        </div>
      </section>
    </main>
  );
}
