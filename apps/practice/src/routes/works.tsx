import { createFileRoute, Link } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Run } from "@/components/run";
import { evalAt, evalRows, passages, practiceExam, retrievalAnswer, retrievalQuery, runSteps, shelves } from "@/lib/works";
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
  const [picks, setPicks] = useState<number[]>(() => practiceExam.map(() => -1));
  const [checked, setChecked] = useState(false);
  const [passage, setPassage] = useState("");
  const [threshold, setThreshold] = useState(0.9);
  const scores = useMemo(() => evalAt(threshold), [threshold]);
  const examCorrect = practiceExam.filter((item, i) => picks[i] === item.answer).length;
  const examPassed = examCorrect === practiceExam.length;

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Works · engineering</p>
      <h1 className="mt-3 max-w-[16ch] text-hero leading-[0.95]">Understand it, then measure it</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        This is the engineering half. One system at a time: a run, a practice exam, a retrieval, a line you move. The
        build half is the academy. Both are open. Neither is a certificate from those schools.
      </p>
      <p className="mt-4">
        <Link to="/academy" className="text-sm underline">
          The academy build
        </Link>
      </p>

      <section className="mt-10 max-w-3xl space-y-8">
        <h2 className="text-3xl">Both shelves</h2>
        <p className="max-w-[68ch] text-muted">
          MIT’s lecture videos and the Hugging Face course. Play our order, then open theirs. We do not rehost the files.
        </p>
        {shelves.map((shelf) => (
          <div key={shelf.id}>
            <div className="mb-3 flex flex-wrap items-baseline justify-between gap-3">
              <h3 className="text-2xl">{shelf.title}</h3>
              <a href={shelf.href} className="text-sm underline" target="_blank" rel="noreferrer">
                Open the source
              </a>
            </div>
            <Run steps={shelf.steps} />
            <p className="mt-2 text-sm text-muted">{shelf.note}</p>
          </div>
        ))}
      </section>

      <section className="mt-14">
        <h2 className="text-3xl">Understand</h2>
        <p className="mt-3 max-w-[68ch] text-muted">Our run, then the practice exam. Four of four to clear it. CC BY 4.0.</p>
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
    </main>
  );
}
