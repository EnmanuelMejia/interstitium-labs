import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { schoolModules, swaps } from "@/lib/school";
import { useProgress } from "@/lib/progress";

export const Route = createFileRoute("/school")({
  component: SchoolPage,
});

function SchoolPage() {
  const saveQuiz = useProgress((s) => s.saveQuiz);
  const quizzes = useProgress((s) => s.quizzes);
  const [index, setIndex] = useState(0);
  const [pick, setPick] = useState(-1);
  const [checked, setChecked] = useState(false);
  const module = schoolModules[index];
  const saved = quizzes[`school:${index}`];

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">School · open stack</p>
      <h1 className="mt-3 max-w-[14ch] text-hero leading-[0.95]">Their outline, our manuals</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        Webucator’s full-stack bundle and Per Scholas’s software course are the map of topics: markup, behavior, a
        service, a database, and delivery. The lessons are not theirs. Noah is the tutor. Nothing is due.
      </p>
      <div className="mt-8 overflow-x-auto rounded-xl border border-line">
        <table className="w-full min-w-[36rem] text-left text-sm">
          <thead className="text-muted">
            <tr>
              <th className="px-3 py-2 font-medium">Theirs</th>
              <th className="px-3 py-2 font-medium">Here</th>
            </tr>
          </thead>
          <tbody>
            {swaps.map((swap) => (
              <tr key={swap.theirs} className="border-t border-line">
                <td className="px-3 py-3 text-muted">{swap.theirs}</td>
                <td className="px-3 py-3">
                  {swap.href.startsWith("/") ? (
                    <Link to="/muse" className="underline">
                      {swap.ours}
                    </Link>
                  ) : (
                    <a href={swap.href} className="underline" target="_blank" rel="noreferrer">
                      {swap.ours}
                    </a>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-8 flex gap-2 overflow-x-auto">
        {schoolModules.map((item, i) => (
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
            {quizzes[`school:${i}`]?.passed ? " · held" : ""}
          </button>
        ))}
      </div>
      <article className="mt-6 max-w-[68ch]">
        <h2 className="text-3xl">{module.name}</h2>
        <ul className="mt-4 space-y-3 border-l border-line pl-4">
          {module.units.map((unit) => (
            <li key={unit}>{unit}</li>
          ))}
        </ul>
        <a href={module.href} className="mt-4 inline-flex min-h-11 items-center text-sm underline" target="_blank" rel="noreferrer">
          {module.hrefLabel}
        </a>
        <h3 className="mt-8 text-2xl">Check</h3>
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
                  (show && i === module.check.answer
                    ? "border-ok text-ok"
                    : show
                      ? "border-bad text-bad"
                      : on
                        ? "border-fg bg-surface-2"
                        : "border-line")
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
              const passed = pick === module.check.answer;
              saveQuiz(`school:${index}`, { correct: passed ? 1 : 0, total: 1, passed });
            }}
            className="min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg disabled:opacity-40"
          >
            {saved?.passed ? "Held" : "Commit"}
          </button>
          <Link to="/editor" className="inline-flex min-h-11 items-center text-sm underline">
            Open the bench
          </Link>
        </div>
      </article>
    </main>
  );
}
