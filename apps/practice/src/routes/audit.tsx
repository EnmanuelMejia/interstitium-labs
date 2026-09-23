import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { findings } from "@/lib/audit";
import { noahGraph } from "@/lib/harness";
import { harnessState } from "@/lib/muse-ask";

export const Route = createFileRoute("/audit")({
  component: AuditPage,
});

type Live = Awaited<ReturnType<typeof harnessState>>;

function AuditPage() {
  const [live, setLive] = useState<Live | null>(null);
  useEffect(() => {
    void harnessState().then(setLive).catch(() => setLive(null));
  }, []);

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Audit</p>
      <h1 className="mt-3 max-w-[14ch] text-hero leading-[0.95]">What this build actually holds</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        Every parameter so far, marked held, partial, or still a gap. Open weight comes before a frontier model. Where
        an open tool does not beat a vendor’s product yet, the row says so.
      </p>
      {live ? (
        <ul className="mt-6 max-w-[68ch] space-y-2 text-sm">
          <li>Ollama {live.ollama ? `configured · ${live.ollamaModel}` : `not set · would use ${live.ollamaModel}`}</li>
          <li>Hugging Face {live.huggingface ? `configured · ${live.hfModel}` : `not set · would use ${live.hfModel}`}</li>
          <li>Frontier {live.frontier ? `configured · ${live.frontierModel}` : "not set"}</li>
        </ul>
      ) : (
        <p className="mt-6 text-sm text-muted">The harness has not reported yet.</p>
      )}
      <ol className="mt-8 max-w-[68ch] space-y-3 border-l border-line pl-4">
        {noahGraph.map((node) => (
          <li key={node.id}>
            <span className="text-xs tracking-[0.14em] text-muted uppercase">{node.id}</span>
            <span className="mt-1 block">{node.does}</span>
          </li>
        ))}
      </ol>
      <div className="mt-8 overflow-x-auto rounded-xl border border-line">
        <table className="w-full min-w-[40rem] text-left text-sm">
          <thead className="text-muted">
            <tr>
              <th className="px-3 py-2 font-medium">Parameter</th>
              <th className="px-3 py-2 font-medium">Decision</th>
              <th className="px-3 py-2 font-medium">State</th>
            </tr>
          </thead>
          <tbody>
            {findings.map((row) => (
              <tr key={row.name} className="border-t border-line align-top">
                <td className="px-3 py-3 text-fg">{row.name}</td>
                <td className="px-3 py-3 text-fg/85">{row.decision}</td>
                <td className={"px-3 py-3 " + (row.state === "Gap" ? "text-bad" : row.state === "Partial" ? "text-warn" : "text-ok")}>
                  {row.state}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-6 max-w-[68ch] text-sm text-muted">
        On the host, Noah uses an open weight when <span className="num">OLLAMA_BASE_URL</span> is set. Hugging Face is
        the second open path. The frontier model runs only if both are absent. This page does not ship Tableau, and it
        does not claim a filmed avatar.
      </p>
      <div className="mt-4 flex flex-wrap gap-3">
        <Link to="/muse" className="text-sm underline">
          Noah
        </Link>
        <Link to="/data" className="text-sm underline">
          Data
        </Link>
      </div>
    </main>
  );
}
