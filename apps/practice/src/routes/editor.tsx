import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Rtfm } from "@/components/rtfm";
import { javaNotes, runSql } from "@/lib/sql-bench";

export const Route = createFileRoute("/editor")({
  component: EditorPage,
});

const files = {
  "query.sql": "select host, rate from readings where errors > 0 order by rate desc;\n",
  "Gate.java": "class Gate {\n  // There is no JVM on this page.\n}\n",
  "notes.md": "Read the manual for the tool you are not using.\n",
} as const;

type FileName = keyof typeof files;

function EditorPage() {
  const [name, setName] = useState<FileName>("query.sql");
  const [buffers, setBuffers] = useState<Record<FileName, string>>({ ...files });
  const [ran, setRan] = useState(false);
  const source = buffers[name];
  const result = useMemo(() => (name === "query.sql" && ran ? runSql(source) : null), [name, ran, source]);
  const notes = name === "Gate.java" && ran ? javaNotes(source) : [];
  const lines = source.split("\n");

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Bench · our editor</p>
      <h1 className="mt-3 max-w-[16ch] text-hero leading-[0.95]">Not their editor</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        A buffer, a run, and the manual. JetBrains, Eclipse, VS Code, Vim, and the JDKs stay on their own sites. This
        page does not embed them.
      </p>
      <div className="mt-6 flex gap-2 overflow-x-auto">
        {(Object.keys(files) as FileName[]).map((file) => (
          <button
            key={file}
            type="button"
            onClick={() => {
              setName(file);
              setRan(false);
            }}
            className={
              "min-h-11 shrink-0 rounded-md border px-3 font-mono text-sm " +
              (name === file ? "border-fg bg-surface-2 text-fg" : "border-line text-muted")
            }
          >
            {file}
          </button>
        ))}
      </div>
      <div className="mt-4 overflow-hidden rounded-xl border border-line bg-surface">
        <div className="flex">
          <div className="num hidden w-10 shrink-0 select-none border-r border-line py-3 text-right text-xs text-faint sm:block">
            {lines.map((_, i) => (
              <div key={i} className="px-2 leading-6">
                {i + 1}
              </div>
            ))}
          </div>
          <textarea
            value={source}
            onChange={(e) => {
              setBuffers((curr) => ({ ...curr, [name]: e.target.value }));
              setRan(false);
            }}
            spellCheck={false}
            className="min-h-64 w-full resize-y bg-bg px-3 py-3 font-mono text-sm leading-6 text-fg"
            aria-label={name}
          />
        </div>
      </div>
      <button
        type="button"
        onClick={() => setRan(true)}
        className="mt-4 min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg"
      >
        Run
      </button>
      {result ? (
        <div className="mt-4 max-w-3xl">
          {result.error ? (
            <Rtfm line={result.error + " The SQL language page is PostgreSQL’s, or SQLite’s if that is the dialect you meant."} />
          ) : (
            <div className="overflow-x-auto rounded-xl border border-line">
              <table className="w-full text-left text-sm">
                <thead className="text-muted">
                  <tr>
                    {result.columns.map((col) => (
                      <th key={col} className="px-3 py-2 font-medium">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.rows.map((row, i) => (
                    <tr key={i} className="border-t border-line">
                      {result.columns.map((col) => (
                        <td key={col} className="num px-3 py-2">
                          {String(row[col])}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ) : null}
      {notes.length ? (
        <div className="mt-4 max-w-[68ch] space-y-3">
          {notes.map((note) => (
            <Rtfm key={note} line={note + " Oracle JDK, Temurin, and OpenJDK each have a manual. This buffer is not one of them."} />
          ))}
        </div>
      ) : null}
      {name === "notes.md" && ran ? (
        <div className="mt-4 max-w-[68ch]">
          <Rtfm line="The note is saved in the buffer only. The manuals page is the shelf." />
        </div>
      ) : null}
    </main>
  );
}
