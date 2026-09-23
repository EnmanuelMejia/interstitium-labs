import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { bashGoalMet, bashPicture, initialBash, runBash, type BashState } from "@/lib/bash-lab";
import { useProgress } from "@/lib/progress";

export const Route = createFileRoute("/desk")({
  component: DeskPage,
});

function DeskPage() {
  const saveLab = useProgress((s) => s.saveLab);
  const saved = useProgress((s) => s.labs["desk:bash"]);
  const [state, setState] = useState<BashState>(() => initialBash());
  const [line, setLine] = useState("ls /var/log");
  const [out, setOut] = useState("");
  const [error, setError] = useState("");
  const met = bashGoalMet(state);

  function submit(text: string) {
    const result = runBash(state, text);
    setState(result.state);
    setOut(result.out);
    setError(result.error ?? "");
    if (bashGoalMet(result.state)) {
      saveLab("desk:bash", { score: 1, passed: true, detail: "app.log is 640 and intact" });
    }
  }

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Desk · parser, not a host</p>
      <h1 className="mt-3 max-w-[16ch] text-hero leading-[0.95]">Make the log 640</h1>
      <p className="mt-5 max-w-[66ch] text-lg text-fg/85">
        <span className="font-mono text-base">/var/log/app.log</span> is mode 666. The service account should be the only
        writer. Group may read. Others nothing. Leave the contents alone. Java, C, C++, Perl, PowerShell, and SQL traces
        are questions on Muse — this page does not pretend to ship their compilers.
      </p>
      <div className="mt-8 grid gap-4 lg:grid-cols-[minmax(0,1fr)_18rem]">
        <div className="rounded-xl border border-line bg-surface p-4">
          <p className="font-mono text-xs text-muted">{state.cwd}</p>
          <pre className="mt-3 min-h-36 overflow-x-auto font-mono text-sm leading-6 text-fg/90">
            {bashPicture(state)}
            {out ? `\n${out}` : ""}
            {error ? `\n${error}` : ""}
          </pre>
          <form
            className="mt-3 flex flex-col gap-2 sm:flex-row"
            onSubmit={(e) => {
              e.preventDefault();
              submit(line);
            }}
          >
            <label className="sr-only" htmlFor="bash-line">
              Command
            </label>
            <input
              id="bash-line"
              value={line}
              onChange={(e) => setLine(e.target.value.slice(0, 120))}
              className="min-h-11 w-full rounded-md border border-line bg-bg px-3 font-mono text-sm"
              autoCapitalize="off"
              autoCorrect="off"
              spellCheck={false}
            />
            <button type="submit" className="min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg">
              Run
            </button>
          </form>
          <div className="mt-3 flex flex-wrap gap-2">
            {["pwd", "ls /var/log", "cat /var/log/app.log", "chmod 640 /var/log/app.log"].map((sample) => (
              <button
                key={sample}
                type="button"
                className="min-h-11 rounded-md border border-line px-3 font-mono text-xs"
                onClick={() => {
                  setLine(sample);
                  submit(sample);
                }}
              >
                {sample}
              </button>
            ))}
          </div>
        </div>
        <aside className="rounded-xl border border-line bg-surface p-4 text-sm">
          <p className="text-xs tracking-[0.14em] text-muted uppercase">Bar</p>
          <p className={"mt-2 " + (met ? "text-ok" : "text-fg/85")}>
            {met || saved?.passed ? "Cleared. The file is 640 and still says started." : "Not cleared."}
          </p>
          <p className="mt-4 text-muted">
            Pipes, redirects, substitution, and backticks are rejected. A teaching shell that calls a real shell would be
            the bug.
          </p>
          <button
            type="button"
            className="mt-4 min-h-11 rounded-md border border-line px-3"
            onClick={() => {
              setState(initialBash());
              setOut("");
              setError("");
            }}
          >
            Reset the disk
          </button>
        </aside>
      </div>
    </main>
  );
}
