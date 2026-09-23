import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { Run } from "@/components/run";
import { academyPhases } from "@/lib/works";
import { useProgress } from "@/lib/progress";

export const Route = createFileRoute("/academy")({
  component: AcademyPage,
});

function AcademyPage() {
  const saveQuiz = useProgress((s) => s.saveQuiz);
  const quizzes = useProgress((s) => s.quizzes);
  const obsession = useProgress((s) => s.obsession);
  const setObsession = useProgress((s) => s.setObsession);
  const build = useProgress((s) => s.build);
  const setBuild = useProgress((s) => s.setBuild);
  const [index, setIndex] = useState(0);
  const [pick, setPick] = useState(-1);
  const [checked, setChecked] = useState(false);
  const phase = academyPhases[index];
  const saved = quizzes[`academy:${index}`];

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Academy · the build</p>
      <h1 className="mt-3 max-w-[14ch] text-hero leading-[0.95]">Build, field, return</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        The other half. One obsession, proof it exists, then a hand-off. Their campus runs September to April, then a
        month away, then a co-op. Those dates are not yours. Noah holds the name. The engineering half stays on Works.
      </p>
      <p className="mt-4">
        <Link to="/works" className="text-sm underline">
          The engineering works
        </Link>
      </p>
      <div className="mt-8 flex gap-2 overflow-x-auto">
        {academyPhases.map((item, i) => (
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
            {quizzes[`academy:${i}`]?.passed ? " · held" : ""}
          </button>
        ))}
      </div>
      <article className="mt-6 max-w-3xl">
        <p className="max-w-[68ch] text-muted">{phase.text}</p>
        <div className="mt-4">
          <Run steps={phase.steps} />
        </div>
        <h2 className="mt-8 text-2xl">Check</h2>
        <p className="mt-3">{phase.check.q}</p>
        <div className="mt-3 grid max-w-[68ch] gap-2">
          {phase.check.choices.map((choice, i) => {
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
                  (show && i === phase.check.answer ? "border-ok text-ok" : show ? "border-bad text-bad" : on ? "border-fg bg-surface-2" : "border-line")
                }
              >
                {choice}
              </button>
            );
          })}
        </div>
        {checked ? <p className="mt-3 text-sm text-muted">{phase.check.why}</p> : null}
        <button
          type="button"
          disabled={pick < 0}
          onClick={() => {
            setChecked(true);
            const passed = pick === phase.check.answer;
            saveQuiz(`academy:${index}`, { correct: passed ? 1 : 0, total: 1, passed });
          }}
          className="mt-4 min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg disabled:opacity-40"
        >
          {saved?.passed ? "Held" : "Commit"}
        </button>
      </article>
      <section className="mt-14 max-w-[68ch]">
        <h2 className="text-3xl">Proof</h2>
        <label className="mt-4 block text-sm text-muted" htmlFor="work-name">
          The work
        </label>
        <input id="work-name" value={obsession} onChange={(e) => setObsession(e.target.value)} maxLength={140} className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm" />
        <label className="mt-4 block text-sm text-muted" htmlFor="artifact">
          The artifact someone can run
        </label>
        <input id="artifact" value={build.artifact} onChange={(e) => setBuild({ artifact: e.target.value.slice(0, 160) })} className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm" />
        <label className="mt-4 block text-sm text-muted" htmlFor="who">
          Who uses it
        </label>
        <input id="who" value={build.who} onChange={(e) => setBuild({ who: e.target.value.slice(0, 160) })} className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm" />
        <label className="mt-4 block text-sm text-muted" htmlFor="fails">
          How it fails in the open
        </label>
        <input id="fails" value={build.fails} onChange={(e) => setBuild({ fails: e.target.value.slice(0, 160) })} className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm" />
        <Link to="/muse" className="mt-4 inline-flex min-h-11 items-center rounded-md bg-accent px-4 text-sm font-medium text-accent-fg">
          Take it to Noah
        </Link>
      </section>
    </main>
  );
}
