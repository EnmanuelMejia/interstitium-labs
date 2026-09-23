import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { dataModules, dataSwaps } from "@/lib/data-science";
import { readings } from "@/lib/sql-bench";
import { useProgress } from "@/lib/progress";

export const Route = createFileRoute("/data")({
  component: DataPage,
});

function DataPage() {
  const saveQuiz = useProgress((s) => s.saveQuiz);
  const quizzes = useProgress((s) => s.quizzes);
  const [index, setIndex] = useState(0);
  const [pick, setPick] = useState(-1);
  const [checked, setChecked] = useState(false);
  const module = dataModules[index];
  const max = Math.max(...readings.map((row) => Number(row.rate)));

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Data · open tools</p>
      <h1 className="mt-3 max-w-[14ch] text-hero leading-[0.95]">The grain, then the chart</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        Analyst work is a row you can define, a query you can read, and a chart that uses the measure. Tableau,
        Power BI, and the certifications stay on their sites. The picture below is ours.
      </p>
      <div className="mt-8 max-w-xl rounded-xl border border-line bg-surface p-5">
        <p className="text-xs tracking-[0.14em] text-muted uppercase">Rate by host · readings</p>
        <ul className="mt-4 space-y-3">
          {readings.map((row) => (
            <li key={String(row.id)} className="grid grid-cols-[4rem_1fr_3rem] items-center gap-3 text-sm">
              <span>{String(row.host)}</span>
              <span className="h-3 rounded-sm bg-gold" style={{ width: `${(Number(row.rate) / max) * 100}%` }} />
              <span className="num text-muted">{String(row.rate)}</span>
            </li>
          ))}
        </ul>
      </div>
      <div className="mt-8 overflow-x-auto rounded-xl border border-line">
        <table className="w-full min-w-[36rem] text-left text-sm">
          <thead className="text-muted">
            <tr>
              <th className="px-3 py-2 font-medium">Theirs</th>
              <th className="px-3 py-2 font-medium">Here</th>
            </tr>
          </thead>
          <tbody>
            {dataSwaps.map((swap) => (
              <tr key={swap.theirs} className="border-t border-line">
                <td className="px-3 py-3 text-muted">{swap.theirs}</td>
                <td className="px-3 py-3">
                  <a href={swap.href} className="underline" target="_blank" rel="noreferrer">
                    {swap.ours}
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-8 flex gap-2 overflow-x-auto">
        {dataModules.map((item, i) => (
          <button
            key={item.name}
            type="button"
            onClick={() => {
              setIndex(i);
              setPick(-1);
              setChecked(false);
            }}
            className={
              "min-h-11 shrink-0 rounded-md border px-3 text-sm " +
              (i === index ? "border-fg bg-surface-2 text-fg" : "border-line text-muted")
            }
          >
            0{i + 1} {item.name}
            {quizzes[`data:${i}`]?.passed ? " · held" : ""}
          </button>
        ))}
      </div>
      <article className="mt-6 max-w-[68ch]">
        <ul className="space-y-3 border-l border-line pl-4">
          {module.units.map((unit) => (
            <li key={unit}>{unit}</li>
          ))}
        </ul>
        <h2 className="mt-6 text-2xl">Check</h2>
        <p className="mt-3">{module.check.q}</p>
        <div className="mt-3 grid gap-2">
          {module.check.choices.map((choice, i) => {
            const on = pick === i;
            const show = checked && on;
            return (
              <button
                key={choice}
                type="button"
                onClick={() => {
                  setPick(i);
                  setChecked(false);
                }}
                className={
                  "min-h-11 rounded-lg border px-3 py-2 text-left text-sm " +
                  (show && i === 0 ? "border-ok text-ok" : show ? "border-bad text-bad" : on ? "border-fg bg-surface-2" : "border-line")
                }
              >
                {choice}
              </button>
            );
          })}
        </div>
        {checked ? <p className="mt-3 text-sm text-muted">{module.check.why}</p> : null}
        <div className="mt-4 flex flex-wrap gap-3">
          <button
            type="button"
            disabled={pick < 0}
            onClick={() => {
              setChecked(true);
              saveQuiz(`data:${index}`, { correct: pick === 0 ? 1 : 0, total: 1, passed: pick === 0 });
            }}
            className="min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg disabled:opacity-40"
          >
            Commit
          </button>
          <Link to="/editor" className="inline-flex min-h-11 items-center text-sm underline">
            SQL bench
          </Link>
        </div>
      </article>
    </main>
  );
}
