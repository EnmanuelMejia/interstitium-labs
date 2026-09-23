import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { roadVendors, roads } from "@/lib/roadmap";
import { useProgress } from "@/lib/progress";

export const Route = createFileRoute("/ladders")({
  component: RoadsPage,
});

function RoadsPage() {
  const [vendor, setVendor] = useState("All");
  const [roadId, setRoadId] = useState(roads[0].id);
  const [moduleIndex, setModuleIndex] = useState(0);
  const [pick, setPick] = useState(-1);
  const [checked, setChecked] = useState(false);
  const saveQuiz = useProgress((s) => s.saveQuiz);
  const quizzes = useProgress((s) => s.quizzes);
  const visible = vendor === "All" ? roads : roads.filter((road) => road.vendor === vendor);
  const road = visible.find((item) => item.id === roadId) ?? visible[0];
  const module = road.modules[Math.min(moduleIndex, road.modules.length - 1)];
  const saved = quizzes[`road:${road.id}:${moduleIndex}`];

  function chooseRoad(id: string) {
    setRoadId(id);
    setModuleIndex(0);
    setPick(-1);
    setChecked(false);
  }

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Roads · no deadline</p>
      <h1 className="mt-3 max-w-[14ch] text-hero leading-[0.95]">Path, module, unit, check</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        The order is the one used by a learning path: role, then modules, then a short check. Catalogs are the
        vendors’. Questions are not their exams. Nothing is due.
      </p>
      <div className="mt-6 flex gap-2 overflow-x-auto pb-1">
        {roadVendors.map((item) => (
          <button
            key={item}
            type="button"
            onClick={() => {
              setVendor(item);
              const first = item === "All" ? roads[0] : roads.find((road) => road.vendor === item);
              if (first) chooseRoad(first.id);
            }}
            className={
              "min-h-11 shrink-0 rounded-full border px-3 text-sm " +
              (vendor === item ? "border-fg bg-surface-2 text-fg" : "border-line text-muted")
            }
          >
            {item}
          </button>
        ))}
      </div>
      <div className="mt-6 grid gap-6 lg:grid-cols-[16rem_minmax(0,1fr)]">
        <ul className="divide-y divide-line border-y border-line">
          {visible.map((item) => (
            <li key={item.id}>
              <button type="button" onClick={() => chooseRoad(item.id)} className="w-full py-3 text-left">
                <span className="text-xs tracking-[0.14em] text-muted uppercase">{item.vendor}</span>
                <span className={"mt-1 block " + (item.id === road.id ? "text-fg" : "text-muted")}>{item.title}</span>
              </button>
            </li>
          ))}
        </ul>
        <article>
          <p className="text-sm text-muted">{road.note}</p>
          <a href={road.catalog.href} target="_blank" rel="noreferrer" className="mt-3 inline-flex min-h-11 items-center text-sm underline">
            {road.catalog.label}
          </a>
          <div className="mt-4 flex gap-2 overflow-x-auto">
            {road.modules.map((item, i) => (
              <button
                key={item.name}
                type="button"
                onClick={() => {
                  setModuleIndex(i);
                  setPick(-1);
                  setChecked(false);
                }}
                className={
                  "min-h-11 shrink-0 rounded-md border px-3 text-sm " +
                  (i === moduleIndex ? "border-fg bg-surface-2 text-fg" : "border-line text-muted")
                }
              >
                0{i + 1} {item.name}
                {quizzes[`road:${road.id}:${i}`]?.passed ? " · held" : ""}
              </button>
            ))}
          </div>
          <ol className="mt-6 max-w-[68ch] space-y-3 border-l border-line pl-4">
            {module.units.map((unit) => (
              <li key={unit}>{unit}</li>
            ))}
          </ol>
          <section className="mt-8 max-w-[68ch]">
            <h2 className="text-2xl">Check</h2>
            <p className="mt-3 text-fg">{module.check.q}</p>
            <div className="mt-3 grid gap-2">
              {module.check.choices.map((choice, i) => {
                const on = pick === i;
                const show = checked && on;
                const good = show && i === module.check.answer;
                const bad = show && i !== module.check.answer;
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
                      (good ? "border-ok text-ok" : bad ? "border-bad text-bad" : on ? "border-fg bg-surface-2" : "border-line")
                    }
                  >
                    {choice}
                  </button>
                );
              })}
            </div>
            {checked ? <p className="mt-3 text-sm text-muted">{module.check.why}</p> : null}
            <button
              type="button"
              disabled={pick < 0}
              onClick={() => {
                setChecked(true);
                const passed = pick === module.check.answer;
                saveQuiz(`road:${road.id}:${moduleIndex}`, { correct: passed ? 1 : 0, total: 1, passed });
              }}
              className="mt-4 min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg disabled:opacity-40"
            >
              {saved?.passed ? "Held" : checked ? "Recorded" : "Commit"}
            </button>
          </section>
        </article>
      </div>
    </main>
  );
}
