import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import { Stage } from "@/components/stage";
import { TutorDesk } from "@/components/tutor-desk";
import { askMuse } from "@/lib/muse-ask";
import { domains, fringeOf, knowledge, passedSet, type Domain } from "@/lib/knowledge";
import { useProgress } from "@/lib/progress";

export const Route = createFileRoute("/muse")({
  component: MusePage,
});

function MusePage() {
  const quizzes = useProgress((s) => s.quizzes);
  const saveQuiz = useProgress((s) => s.saveQuiz);
  const [domain, setDomain] = useState<Domain | "all">("all");
  const [holdId, setHoldId] = useState<string | null>(null);
  const [pick, setPick] = useState(-1);
  const [checked, setChecked] = useState(false);
  const [attempt, setAttempt] = useState("");
  const [reply, setReply] = useState("");
  const [pending, setPending] = useState(false);
  const [museError, setMuseError] = useState("");

  const passed = useMemo(() => passedSet(quizzes), [quizzes]);
  const fringe = fringeOf(passed, domain === "all" ? undefined : domain);
  const node = knowledge.find((n) => n.id === holdId) ?? fringe.ready[0];
  const signal = knowledge.length ? passed.size / knowledge.length : 0;

  useEffect(() => {
    setPick(-1);
    setChecked(false);
    setReply("");
    setMuseError("");
  }, [node?.id]);

  function selectDomain(next: Domain | "all") {
    setDomain(next);
    setHoldId(null);
    setPick(-1);
    setChecked(false);
    setReply("");
    setMuseError("");
  }

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Noah · assistant, and tutor</p>
      <h1 className="mt-3 max-w-[16ch] text-hero leading-[0.95]">Tell Noah the work</h1>
      <p className="mt-5 max-w-[66ch] text-lg text-fg/85">
        Noah is the assistant. Tutoring is one of the jobs. A question still gets a question back. A task gets the draft.
        Memory and goals stay on this device. Noah does not send mail, spend money, or keep working after you leave.
      </p>
      <TutorDesk />
      <div className="mt-8">
        <Stage
          scene="lattice"
          signal={signal}
          label={`${passed.size} of ${knowledge.length} nodes held. The lattice tightens as the fringe shrinks.`}
        />
      </div>
      <div className="mt-4 flex gap-2 overflow-x-auto pb-1">
        <Chip on={domain === "all"} label="All" onClick={() => selectDomain("all")} />
        {domains.map((d) => (
          <Chip key={d.id} on={domain === d.id} label={d.label} onClick={() => selectDomain(d.id)} />
        ))}
      </div>
      <p className="num mt-3 text-sm text-muted">
        {fringe.ready.length} ready · {fringe.blocked.length} blocked · {fringe.done.length} held
      </p>

      {node ? (
        <section className="mt-8 max-w-[68ch] rounded-xl border border-line bg-surface p-5">
          <p className="text-xs tracking-[0.14em] text-muted uppercase">{node.domain} · {node.title}</p>
          <h2 className="mt-3 text-2xl">{node.ask}</h2>
          <p className="mt-3 text-sm text-muted">{node.nudge}</p>
          <div className="mt-4 grid gap-2">
            {node.choices.map((choice, i) => {
              const on = pick === i;
              const show = checked && on;
              const good = show && i === node.answer;
              const bad = show && i !== node.answer;
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
          {checked ? <p className="mt-3 text-sm text-fg/85">{node.why}</p> : null}
          <div className="mt-4 flex flex-wrap gap-3">
            <button
              type="button"
              className="min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg"
              onClick={() => {
                if (pick < 0) return;
                setChecked(true);
                const ok = pick === node.answer;
                if (ok) setHoldId(node.id);
                saveQuiz(`ks:${node.id}`, { correct: ok ? 1 : 0, total: 1, passed: ok });
              }}
            >
              {checked ? (pick === node.answer ? "Held" : "Not yet") : "Commit an answer"}
            </button>
            {checked && pick === node.answer ? (
              <button type="button" className="min-h-11 rounded-md border border-line px-4 text-sm" onClick={() => setHoldId(null)}>
                Next on the fringe
              </button>
            ) : null}
            {node.path ? (
              <Link
                to="/paths/$slug"
                params={{ slug: node.path }}
                className="inline-flex min-h-11 items-center text-sm underline"
              >
                Open the path
              </Link>
            ) : null}
          </div>
          <label className="mt-6 block text-sm text-muted" htmlFor="muse-attempt">
            Say what you tried. One press. Noah will not hand you the key.
          </label>
          <textarea
            id="muse-attempt"
            value={attempt}
            onChange={(e) => setAttempt(e.target.value.slice(0, 500))}
            rows={3}
            className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm text-fg"
          />
          <button
            type="button"
            disabled={pending || attempt.trim().length < 2}
            className="mt-3 min-h-11 rounded-md border border-line px-4 text-sm disabled:opacity-40"
            onClick={() => {
              setPending(true);
              setMuseError("");
              void askMuse({ data: { topic: node.title, attempt, note: node.nudge } })
                .then((res) => {
                  if (res.ok) setReply(res.text);
                  else setMuseError(res.error);
                })
                .catch(() => setMuseError("Noah could not be reached."))
                .finally(() => setPending(false));
            }}
          >
            {pending ? "Asking" : "Ask Noah"}
          </button>
          {museError ? <p className="mt-3 text-sm text-warn">{museError}</p> : null}
          {reply ? <p className="mt-3 max-w-[68ch] text-sm text-fg/90">{reply}</p> : null}
        </section>
      ) : (
        <p className="mt-8 max-w-[62ch] text-fg/85">
          {fringe.blocked.length
            ? "Nothing in this slice is ready. Hold a prerequisite, or switch the slice."
            : "This slice is held. Raise the work on a path studio, or pick another domain."}
        </p>
      )}
      {fringe.blocked.length ? (
        <ul className="mt-8 max-w-[68ch] divide-y divide-line border-y border-line text-sm">
          {fringe.blocked.slice(0, 6).map((n) => (
            <li key={n.id} className="py-3">
              <span className="text-fg">{n.title}</span>
              <span className="mt-1 block text-muted">Waiting on {n.prereqs.join(", ")}</span>
            </li>
          ))}
        </ul>
      ) : null}
    </main>
  );
}

function Chip({ on, label, onClick }: { on: boolean; label: string; onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={"min-h-11 shrink-0 rounded-full border px-3 text-sm " + (on ? "border-fg bg-surface-2 text-fg" : "border-line text-muted")}
    >
      {label}
    </button>
  );
}
