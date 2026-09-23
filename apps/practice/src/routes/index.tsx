import { createFileRoute, Link } from "@tanstack/react-router";
import { labs, outlineMap, sessions, weeks } from "@/lib/course";
import { paths } from "@/lib/paths";
import { useProgress } from "@/lib/progress";
import { Stage } from "@/components/stage";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  const hydrated = useProgress((s) => s.hydrated);
  const quizzes = useProgress((s) => s.quizzes);
  const labState = useProgress((s) => s.labs);
  const notes = useProgress((s) => s.notes);
  const next = sessions.find((s) => !quizzes[s.id]?.passed) ?? sessions[0];
  const clearedNotes = sessions.filter((s) => s.assignment && notes[s.assignment.id]).length;
  const noteTotal = sessions.filter((s) => s.assignment).length;

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Domain 01</p>
      <h1 className="mt-3 max-w-[14ch] text-hero leading-[0.95] text-fg">AI-aided cybersecurity</h1>
      <p className="mt-6 max-w-[62ch] text-lg text-fg/85">
        The practice for every course, before it is folded into the public site. No deadlines. Noah holds the one thing
        you are building. The open stack replaces a vendor bootcamp. Nine weeks of cybersecurity remain a sequence you
        can walk in any number of days.
      </p>
      <div className="mt-8 flex flex-wrap items-center gap-3">
        <Link
          to="/session/$sessionId"
          params={{ sessionId: hydrated ? next.id : "s00" }}
          className="inline-flex min-h-11 items-center rounded-md bg-accent px-4 text-sm font-medium text-accent-fg"
        >
          {hydrated && quizzes[sessions[0].id]?.passed ? `Continue · ${next.index} ${next.title}` : "Begin with the orientation"}
        </Link>
        <Link to="/baseline" className="inline-flex min-h-11 items-center rounded-md border border-line px-4 text-sm text-fg">
          Place your math
        </Link>
        <Link to="/muse" className="inline-flex min-h-11 items-center rounded-md border border-line px-4 text-sm text-fg">
          Ask Noah first
        </Link>
        <Link to="/school" className="inline-flex min-h-11 items-center rounded-md border border-line px-4 text-sm text-fg">
          Open stack
        </Link>
        <Link to="/works" className="inline-flex min-h-11 items-center rounded-md border border-line px-4 text-sm text-fg">
          Engineering works
        </Link>
        <Link to="/host" className="inline-flex min-h-11 items-center rounded-md border border-line px-4 text-sm text-fg">
          P920 host
        </Link>
        <Link
          to="/lab/$labId"
          params={{ labId: "capstone" }}
          className="inline-flex min-h-11 items-center rounded-md border border-line px-4 text-sm text-fg"
        >
          Open the capstone
        </Link>
      </div>
      <div className="mt-10">
        <Stage
          scene="lattice"
          signal={0.42}
          label="Interstitium: the space between the cells. Paths and detections live in the gaps."
        />
      </div>
      <dl className="mt-6 grid grid-cols-2 gap-px overflow-hidden rounded-xl border border-line bg-line sm:grid-cols-4">
        {[
          ["17", "Briefings", "Two sittings a week"],
          ["6", "Labs", "Run in the browser"],
          ["6", "Field notes", "Cleared from a bench"],
          ["1", "Capstone", "A detector you can defend"],
        ].map(([n, label, note]) => (
          <div key={label} className="bg-bg px-4 py-4">
            <dt className="text-xs tracking-[0.14em] text-muted uppercase">{label}</dt>
            <dd className="num mt-1 text-2xl">{n}</dd>
            <p className="mt-1 text-sm text-muted">{note}</p>
          </div>
        ))}
      </dl>
      {hydrated ? (
        <p className="num mt-4 text-sm text-muted">
          {sessions.filter((s) => quizzes[s.id]?.passed).length} briefings cleared · {Object.values(labState).filter((l) => l.passed).length} benches · {clearedNotes}/{noteTotal} field notes
        </p>
      ) : null}

      <section className="mt-14">
        <div className="flex items-end justify-between gap-3">
          <h2 className="text-3xl">Paths</h2>
          <Link to="/paths" className="text-sm text-fg underline">
            All {paths.length}
          </Link>
        </div>
        <ul className="mt-4 grid gap-px overflow-hidden rounded-xl border border-line bg-line sm:grid-cols-2">
          {paths.slice(0, 6).map((p) => (
            <li key={p.slug} className="bg-bg">
              <Link to="/paths/$slug" params={{ slug: p.slug }} className="block min-h-28 px-4 py-4">
                <span className="text-xs tracking-[0.14em] text-muted uppercase">{p.scene}</span>
                <span className="mt-2 block text-fg">{p.title}</span>
                <span className="mt-1 block text-sm text-muted">{p.outcome}</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-14">
        <h2 className="text-3xl">The sequence</h2>
        <p className="mt-3 max-w-[62ch] text-muted">
          Self-paced. Part numbers are an order, not a calendar. There is no cohort date and nothing closes.
        </p>
        <div className="mt-8 space-y-10">
          {weeks.map((w) => (
            <section key={w.week}>
              <h3 className="text-sm tracking-[0.16em] text-muted uppercase">
                Part {w.week} · {w.title}
              </h3>
              <ol className="mt-3 divide-y divide-line border-y border-line">
                {w.sessions.map((s) => {
                  const done = Boolean(quizzes[s.id]?.passed && (!s.labId || labState[s.labId]?.passed));
                  return (
                    <li key={s.id}>
                      <Link
                        to="/session/$sessionId"
                        params={{ sessionId: s.id }}
                        className="flex min-h-16 items-baseline gap-4 py-3 sm:gap-6"
                      >
                        <span className="num w-8 shrink-0 text-sm text-muted">{s.index}</span>
                        <span className="min-w-0 flex-1">
                          <span className="block text-fg">{s.title}</span>
                          <span className="mt-1 block text-sm text-muted">{s.minutes} min · no deadline</span>
                        </span>
                        <span className="hidden text-sm text-faint sm:inline">{s.kicker}</span>
                        <span className={"w-14 shrink-0 text-right text-sm " + (done ? "text-ok" : "text-faint")}>
                          {done ? "Clear" : "Open"}
                        </span>
                      </Link>
                    </li>
                  );
                })}
              </ol>
            </section>
          ))}
        </div>
      </section>

      <section className="mt-16">
        <h2 className="text-3xl">Benches</h2>
        <ul className="mt-4 divide-y divide-line border-y border-line">
          {labs.map((lab) => (
            <li key={lab.id}>
              <Link to="/lab/$labId" params={{ labId: lab.id }} className="flex min-h-16 items-baseline gap-4 py-3">
                <span className="num w-8 shrink-0 text-sm text-muted">{lab.index}</span>
                <span className="min-w-0 flex-1">
                  <span className="block text-fg">{lab.title}</span>
                  <span className="mt-1 block text-sm text-muted">{lab.blurb}</span>
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-16 max-w-[68ch]">
        <h2 className="text-3xl">What was reconstructed</h2>
        <p className="mt-3 text-fg/85">
          A public course page lists a nine-week live sequence taught by a principal security architect: machine
          learning fundamentals, six Python labs, and a capstone that detects malware. The lectures, guest talks, and
          notebooks are not public, and they are not reproduced here. The topic arc, lab targets, assignment rhythm,
          and capstone shape are.
        </p>
        <ol className="mt-6 space-y-2 text-sm">
          {outlineMap.map((row) => (
            <li key={row.here} className="grid gap-1 border-t border-line py-2 sm:grid-cols-2 sm:gap-6">
              <span className="text-muted">{row.source}</span>
              <span>{row.here}</span>
            </li>
          ))}
        </ol>
      </section>
    </main>
  );
}
