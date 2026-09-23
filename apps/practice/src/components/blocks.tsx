import { useState } from "react";
import type { Block, QuizQ } from "@/lib/course";
import { useProgress } from "@/lib/progress";

export function Blocks({ blocks }: { blocks: Block[] }) {
  return (
    <div className="space-y-5">
      {blocks.map((b, i) => {
        if (b.kind === "h") return <h2 key={i} className="pt-2 text-2xl text-fg">{b.text}</h2>;
        if (b.kind === "p") return <p key={i} className="max-w-[68ch] text-fg/90">{b.text}</p>;
        if (b.kind === "ul")
          return (
            <ul key={i} className="max-w-[68ch] space-y-2 border-l border-line pl-4 text-fg/90">
              {b.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          );
        if (b.kind === "note")
          return (
            <aside key={i} className="max-w-[68ch] rounded-xl border border-line bg-surface p-5">
              <p className="text-xs tracking-[0.14em] text-muted uppercase">{b.title}</p>
              <p className="mt-2 text-fg/90">{b.text}</p>
            </aside>
          );
        return <CodeBlock key={i} title={b.title} text={b.text} />;
      })}
    </div>
  );
}

export function CodeBlock({ title, text }: { title: string; text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <div className="max-w-[68ch] overflow-hidden rounded-xl border border-line bg-surface">
      <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-2">
        <p className="text-xs tracking-[0.12em] text-muted uppercase">{title}</p>
        <button
          type="button"
          className="min-h-11 px-2 text-sm text-fg"
          onClick={() => {
            void navigator.clipboard?.writeText(text).then(() => {
              setCopied(true);
              window.setTimeout(() => setCopied(false), 1200);
            });
          }}
        >
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre className="overflow-x-auto p-4 font-mono text-sm leading-relaxed text-fg/90">{text}</pre>
    </div>
  );
}

export function Quiz({ sessionId, questions }: { sessionId: string; questions: QuizQ[] }) {
  const saved = useProgress((s) => s.quizzes[sessionId]);
  const saveQuiz = useProgress((s) => s.saveQuiz);
  const [picks, setPicks] = useState<number[]>(() => questions.map(() => -1));
  const [checked, setChecked] = useState(false);

  const correct = questions.reduce((n, q, i) => n + (picks[i] === q.answer ? 1 : 0), 0);
  const passed = correct === questions.length;

  return (
    <section className="mt-12 max-w-[68ch]">
      <div className="flex items-baseline justify-between gap-3">
        <h2 className="text-2xl">Checkpoint</h2>
        {saved?.passed ? <span className="text-sm text-ok">Cleared</span> : null}
      </div>
      <ol className="mt-5 space-y-6">
        {questions.map((q, qi) => (
          <li key={q.q}>
            <p className="text-fg">{q.q}</p>
            <div className="mt-3 grid gap-2">
              {q.choices.map((c, ci) => {
                const on = picks[qi] === ci;
                const show = checked && on;
                const good = show && ci === q.answer;
                const bad = show && ci !== q.answer;
                return (
                  <button
                    key={c}
                    type="button"
                    onClick={() => {
                      setPicks((prev) => prev.map((v, i) => (i === qi ? ci : v)));
                      setChecked(false);
                    }}
                    className={
                      "min-h-11 rounded-lg border px-3 py-2 text-left text-sm " +
                      (good
                        ? "border-ok text-ok"
                        : bad
                          ? "border-bad text-bad"
                          : on
                            ? "border-fg bg-surface-2 text-fg"
                            : "border-line text-fg/85 hover:border-fg/40")
                    }
                  >
                    {c}
                  </button>
                );
              })}
            </div>
            {checked && picks[qi] !== -1 ? <p className="mt-2 text-sm text-muted">{q.why}</p> : null}
          </li>
        ))}
      </ol>
      <button
        type="button"
        className="mt-6 min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg"
        onClick={() => {
          if (picks.some((p) => p < 0)) return;
          setChecked(true);
          saveQuiz(sessionId, { correct, total: questions.length, passed });
        }}
      >
        {checked ? `${correct}/${questions.length}` : "Check answers"}
      </button>
      {checked && !passed ? (
        <p className="mt-3 text-sm text-muted">All of them, to clear the briefing. The why is under each pick.</p>
      ) : null}
    </section>
  );
}

export function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-bg px-3 py-3">
      <p className="text-xs tracking-[0.12em] text-muted uppercase">{label}</p>
      <p className="num mt-1 text-xl text-fg">{value}</p>
    </div>
  );
}

export function Toggle({
  on,
  label,
  onChange,
}: {
  on: boolean;
  label: string;
  onChange: (v: boolean) => void;
}) {
  return (
    <button
      type="button"
      aria-pressed={on}
      onClick={() => onChange(!on)}
      className={
        "min-h-11 rounded-md border px-3 text-left text-sm " +
        (on ? "border-fg bg-surface-2 text-fg" : "border-line text-muted")
      }
    >
      {label}
    </button>
  );
}

export function Slider({
  label,
  min,
  max,
  step,
  value,
  onChange,
  display,
}: {
  label: string;
  min: number;
  max: number;
  step: number;
  value: number;
  onChange: (n: number) => void;
  display?: string;
}) {
  return (
    <label className="block">
      <span className="flex items-baseline justify-between text-sm">
        <span className="text-muted">{label}</span>
        <span className="num text-fg">{display ?? value}</span>
      </span>
      <input
        className="mt-2 h-11 w-full accent-[var(--color-accent)]"
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </label>
  );
}
