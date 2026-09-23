import { createFileRoute, Link } from "@tanstack/react-router";
import { Blocks, Quiz } from "@/components/blocks";
import { sessionById, sessions } from "@/lib/course";
import { useProgress } from "@/lib/progress";

export const Route = createFileRoute("/session/$sessionId")({
  component: SessionPage,
});

function SessionPage() {
  const { sessionId } = Route.useParams();
  const session = sessionById(sessionId);
  const setNote = useProgress((s) => s.setNote);
  const noteOn = useProgress((s) => (session?.assignment ? Boolean(s.notes[session.assignment.id]) : false));
  const lab = useProgress((s) => (session?.labId ? s.labs[session.labId] : undefined));

  if (!session) {
    return (
      <main>
        <h1 className="text-3xl">No such briefing</h1>
        <Link to="/" className="mt-4 inline-flex min-h-11 items-center text-fg underline">
          Back to the domain
        </Link>
      </main>
    );
  }

  const idx = sessions.findIndex((s) => s.id === session.id);
  const prev = sessions[idx - 1];
  const next = sessions[idx + 1];

  return (
    <main>
      <p className="text-xs tracking-[0.16em] text-muted uppercase">
        {session.index} · {session.kicker} · {session.minutes} min
      </p>
      <h1 className="mt-3 max-w-[18ch] text-4xl text-fg sm:text-5xl">{session.title}</h1>
      <p className="mt-3 text-sm text-muted">Self-paced · no deadline · about {session.minutes} min</p>
      <p className="mt-6 max-w-[68ch] text-lg text-fg/85">{session.summary}</p>
      <ul className="mt-6 max-w-[68ch] space-y-2 border-l border-line pl-4 text-fg/90">
        {session.objectives.map((o) => (
          <li key={o}>{o}</li>
        ))}
      </ul>
      <div className="mt-10">
        <Blocks blocks={session.blocks} />
      </div>
      {session.labId ? (
        <p className="mt-8">
          <Link
            to="/lab/$labId"
            params={{ labId: session.labId }}
            className="inline-flex min-h-11 items-center rounded-md bg-accent px-4 text-sm font-medium text-accent-fg"
          >
            Open the bench{lab?.passed ? " · cleared" : ""}
          </Link>
        </p>
      ) : null}
      {session.assignment ? (
        <section className="mt-10 max-w-[68ch] rounded-xl border border-line bg-surface p-5">
          <p className="text-xs tracking-[0.14em] text-muted uppercase">{session.assignment.title}</p>
          <p className="mt-2 text-fg/90">{session.assignment.prompt}</p>
          {session.assignment.id === "a1" ? (
            <button
              type="button"
              onClick={() => setNote("a1", !noteOn)}
              className="mt-4 min-h-11 rounded-md border border-line px-4 text-sm"
            >
              {noteOn ? "Marked done" : "Mark the runtime ready"}
            </button>
          ) : (
            <p className={"mt-3 text-sm " + (noteOn ? "text-ok" : "text-muted")}>
              {noteOn ? "Cleared from the bench." : "Clears when the bench hits its bar."}
            </p>
          )}
        </section>
      ) : null}
      <Quiz key={session.id} sessionId={session.id} questions={session.quiz} />
      <nav className="mt-12 flex flex-wrap gap-3 border-t border-line pt-6">
        {prev ? (
          <Link to="/session/$sessionId" params={{ sessionId: prev.id }} className="inline-flex min-h-11 items-center text-sm text-muted">
            ← {prev.index} {prev.title}
          </Link>
        ) : null}
        {next ? (
          <Link
            to="/session/$sessionId"
            params={{ sessionId: next.id }}
            className="inline-flex min-h-11 items-center text-sm text-fg sm:ml-auto"
          >
            {next.index} {next.title} →
          </Link>
        ) : null}
      </nav>
    </main>
  );
}
