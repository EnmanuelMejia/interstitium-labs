import { useEffect, useState } from "react";

export function Run({ steps }: { steps: { title: string; text: string }[] }) {
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const step = steps[index];

  useEffect(() => {
    if (!playing) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const timer = window.setTimeout(() => {
      setIndex((current) => {
        if (current >= steps.length - 1) {
          setPlaying(false);
          return current;
        }
        return current + 1;
      });
    }, 4200);
    return () => window.clearTimeout(timer);
  }, [playing, index, steps.length]);

  return (
    <div className="rounded-xl border border-line bg-surface p-5">
      <p className="text-xs tracking-[0.14em] text-muted uppercase">
        Open run · {index + 1} / {steps.length}
      </p>
      <h3 className="mt-2 text-2xl">{step.title}</h3>
      <p className="mt-3 max-w-[62ch] text-fg/90">{step.text}</p>
      <div className="mt-4 flex flex-wrap gap-3">
        <button
          type="button"
          onClick={() => {
            if (index >= steps.length - 1) setIndex(0);
            setPlaying((on) => !on);
          }}
          className="min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg"
        >
          {playing ? "Pause" : index >= steps.length - 1 ? "Replay" : "Play"}
        </button>
        <button
          type="button"
          onClick={() => {
            setPlaying(false);
            setIndex((current) => Math.min(steps.length - 1, current + 1));
          }}
          className="min-h-11 rounded-md border border-line px-4 text-sm"
        >
          Next
        </button>
      </div>
      <p className="mt-3 text-sm text-muted">A transcript you can play. Not a recording of someone else’s class.</p>
    </div>
  );
}
