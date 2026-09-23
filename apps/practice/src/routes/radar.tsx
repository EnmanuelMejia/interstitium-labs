import { createFileRoute, Link } from "@tanstack/react-router";
import { knowledge } from "@/lib/knowledge";
import { radarDropped, radarHits, radarScanned } from "@/lib/radar";

export const Route = createFileRoute("/radar")({
  component: RadarPage,
});

const bench = [
  ["Fringe, not a playlist", "ALEKS-style", "Noah only offers a node whose prerequisites are held."],
  ["One problem", "Brilliant-style", "The question is on screen before the explanation."],
  ["Language reps", "boot.dev-style", "Traces live with Noah. Bash is a real parser on the desk, not a video."],
  ["Proof", "Codecademy-style projects", "Cyber benches and path studios record a pass, not a watch-time."],
  ["Video wall", "Often the product", "Not shipped. On purpose."],
  ["Compiler fleet", "Hosted sandboxes", "Not claimed. Java, C, C++, Perl, and PowerShell are traces, not their compilers."],
  ["3D delivery", "Unreal or Blender marketing", "Three.js, orbitable, on both viewports. Those tools author assets. They are not this runtime."],
  ["Social firehose", "A feed", "A dated scan of public posts. Claims stay claims. LinkedIn is not connected."],
];

function RadarPage() {
  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Radar · scanned {radarScanned}</p>
      <h1 className="mt-3 max-w-[16ch] text-hero leading-[0.95]">What is actually being said</h1>
      <p className="mt-5 max-w-[66ch] text-lg text-fg/85">
        Public posts, filtered. A token thread with no named primitive does not become a course. A post is not an incident
        report. Each hit maps to a node you can be questioned on.
      </p>
      <ol className="mt-8 max-w-[72ch] space-y-4">
        {radarHits.map((hit) => {
          const node = knowledge.find((n) => n.id === hit.nodeId);
          return (
            <li key={hit.id} className="rounded-xl border border-line bg-surface p-5">
              <p className="text-xs tracking-[0.14em] text-muted uppercase">
                {hit.when} · {hit.author}
              </p>
              <p className="mt-2 text-fg/90">{hit.claim}</p>
              <p className="mt-2 text-sm text-muted">{hit.study}</p>
              <p className="mt-3 flex flex-wrap gap-4 text-sm">
                <a href={hit.url} className="underline" target="_blank" rel="noreferrer">
                  @{hit.handle}
                </a>
                {node ? (
                  <Link to="/muse" className="underline">
                    Study · {node.title}
                  </Link>
                ) : null}
              </p>
            </li>
          );
        })}
      </ol>
      <section className="mt-12 max-w-[72ch]">
        <h2 className="text-2xl">Left on the floor</h2>
        <ul className="mt-4 space-y-2 border-l border-line pl-4 text-sm text-muted">
          {radarDropped.map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      </section>
      <section className="mt-12">
        <h2 className="text-2xl">Against the pattern, not a fake score</h2>
        <p className="mt-3 max-w-[66ch] text-sm text-muted">
          No percentage versus Khan, ALEKS, Codecademy, Brilliant, boot.dev, or a vendor academy. Those names are patterns.
          Their items, videos, and marks are not ours.
        </p>
        <div className="mt-4 overflow-x-auto rounded-xl border border-line">
          <table className="w-full min-w-[36rem] text-left text-sm">
            <thead className="bg-surface text-xs tracking-[0.12em] text-muted uppercase">
              <tr>
                <th className="px-3 py-3 font-medium">Pattern</th>
                <th className="px-3 py-3 font-medium">Where it shows up</th>
                <th className="px-3 py-3 font-medium">Here</th>
              </tr>
            </thead>
            <tbody>
              {bench.map(([a, b, c]) => (
                <tr key={a} className="border-t border-line">
                  <td className="px-3 py-3 text-fg">{a}</td>
                  <td className="px-3 py-3 text-muted">{b}</td>
                  <td className="px-3 py-3 text-fg/90">{c}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
