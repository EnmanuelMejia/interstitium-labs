import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import {
  AdversarialBench,
  AnomalyBench,
  CapstoneBench,
  FamiliesBench,
  IrisBench,
  MalwarePrepBench,
  NlpBench,
} from "@/components/benches";
import { Slider } from "@/components/blocks";
import { Stage } from "@/components/stage";
import { labById, sessionById } from "@/lib/course";
import type { SceneId } from "@/lib/paths";
import { useProgress } from "@/lib/progress";

export const Route = createFileRoute("/lab/$labId")({
  component: LabPage,
});

const benches = {
  iris: IrisBench,
  "malware-prep": MalwarePrepBench,
  families: FamiliesBench,
  anomaly: AnomalyBench,
  nlp: NlpBench,
  adversarial: AdversarialBench,
  capstone: CapstoneBench,
} as const;

const scenes: Record<string, SceneId> = {
  iris: "detector",
  "malware-prep": "detector",
  families: "detector",
  anomaly: "packets",
  nlp: "lattice",
  adversarial: "detector",
  capstone: "packets",
};

function LabPage() {
  const { labId } = Route.useParams();
  return <LabBody key={labId} labId={labId} />;
}

function LabBody({ labId }: { labId: string }) {
  const meta = labById(labId);
  const saved = useProgress((s) => s.labs[labId]);
  const [stress, setStress] = useState(0.3);
  if (!meta || !(labId in benches)) {
    return (
      <main>
        <h1 className="text-3xl">No such bench</h1>
        <Link to="/" className="mt-4 inline-flex min-h-11 items-center underline">
          Back to the domain
        </Link>
      </main>
    );
  }
  const Bench = benches[labId as keyof typeof benches];
  const session = sessionById(meta.sessionId);
  const signal = Math.min(1, stress + (saved?.passed ? 0.25 : 0));
  return (
    <main>
      <p className="text-xs tracking-[0.16em] text-muted uppercase">Bench {meta.index}</p>
      <h1 className="mt-3 max-w-[16ch] text-4xl sm:text-5xl">{meta.title}</h1>
      <p className="mt-4 max-w-[62ch] text-lg text-fg/85">{meta.blurb}</p>
      <p className="mt-3 max-w-[62ch] text-sm text-muted">Pass bar: {meta.pass}</p>
      {session ? (
        <p className="mt-4">
          <Link to="/session/$sessionId" params={{ sessionId: session.id }} className="text-sm text-fg underline">
            Briefing {session.index} · {session.title}
          </Link>
        </p>
      ) : null}
      <div className="mt-8 grid gap-6 lg:grid-cols-[minmax(0,1fr)_16rem] lg:items-start">
        <Stage scene={scenes[labId] ?? "detector"} signal={signal} label="The stage tracks load, and lifts again when this bench is cleared." />
        <div className="rounded-xl border border-line bg-surface p-4">
          <Slider label="Stage load" min={0} max={1} step={0.01} value={stress} onChange={setStress} display={stress.toFixed(2)} />
          <p className="mt-3 text-sm text-muted">{saved?.passed ? `Cleared. ${saved.detail}` : "Not cleared yet."}</p>
        </div>
      </div>
      <div className="mt-8">
        <Bench />
      </div>
    </main>
  );
}
