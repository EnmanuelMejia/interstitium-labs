import { createFileRoute, Link } from "@tanstack/react-router";
import { useCallback, useState } from "react";
import { Quiz, Slider } from "@/components/blocks";
import { Stage } from "@/components/stage";
import { PathStudio } from "@/components/studio";
import { pathBySlug } from "@/lib/paths";
import { useProgress } from "@/lib/progress";
import { studioBySlug } from "@/lib/studios";

export const Route = createFileRoute("/paths/$slug")({
  component: PathPage,
});

function PathPage() {
  const { slug } = Route.useParams();
  return <PathBody key={slug} slug={slug} />;
}

function PathBody({ slug }: { slug: string }) {
  const path = pathBySlug(slug);
  const studio = studioBySlug(slug);
  const [load, setLoad] = useState(0.35);
  const [hold, setHold] = useState<number | null>(0.45);
  const onHold = useCallback((n: number | null) => setHold(n), []);
  const lab = useProgress((s) => s.labs[`path:${slug}`]);
  if (!path) {
    return (
      <main>
        <h1 className="text-3xl">No such path</h1>
        <Link to="/paths" className="mt-4 inline-flex min-h-11 items-center underline">
          All paths
        </Link>
      </main>
    );
  }
  const signal = lab?.passed ? Math.min(1, load * 0.45) : load;
  return (
    <main>
      <p className="text-xs tracking-[0.16em] text-muted uppercase">Path · {path.scene} · three · adaptive</p>
      <h1 className="mt-3 max-w-[18ch] text-4xl sm:text-5xl">{path.title}</h1>
      <p className="mt-4 max-w-[68ch] text-lg text-fg/85">{path.outcome}</p>
      <div className="mt-8 grid gap-6 lg:grid-cols-[minmax(0,1fr)_16rem] lg:items-start">
        <Stage scene={path.scene} signal={signal} hold={hold} label={lab?.passed ? `Cleared. ${path.live}` : path.live} />
        <div className="rounded-xl border border-line bg-surface p-4">
          <Slider label="Adaptive load" min={0} max={1} step={0.01} value={load} onChange={setLoad} display={load.toFixed(2)} />
          <p className="mt-3 text-sm text-muted">
            {load < 0.34
              ? "Quiet. Fewer cases, and the stage holds a baseline."
              : load < 0.7
                ? "Working load. More of the simulation is in play. Watch what separates."
                : "Stress. The pass bar tightens and the stage shows the stall."}
          </p>
          <p className="mt-3 text-sm text-muted">{lab?.passed ? `Studio cleared. ${lab.detail}` : "The studio below is the lab. Clearing it eases the stage."}</p>
        </div>
      </div>
      <ol className="mt-10 max-w-[68ch] space-y-6">
        {path.phases.map((phase, i) => (
          <li key={phase.name}>
            <p className="text-xs tracking-[0.14em] text-muted uppercase">
              0{i + 1} · {phase.name}
            </p>
            <p className="mt-2 text-fg/90">{phase.text}</p>
          </li>
        ))}
      </ol>
      {studio ? (
        <>
          <PathStudio slug={slug} load={load} onHold={onHold} />
          <Quiz sessionId={`pathq:${slug}`} questions={studio.quiz} />
        </>
      ) : null}
    </main>
  );
}
