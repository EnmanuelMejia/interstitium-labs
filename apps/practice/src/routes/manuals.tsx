import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Rtfm } from "@/components/rtfm";
import { manuals, type Manual } from "@/lib/manuals";

export const Route = createFileRoute("/manuals")({
  component: ManualsPage,
});

const groups = ["All", "Editor", "JVM", "Data", "Chain"] as const;

function ManualsPage() {
  const [group, setGroup] = useState<(typeof groups)[number]>("All");
  const [open, setOpen] = useState<Manual | null>(manuals[0]);
  const rows = group === "All" ? manuals : manuals.filter((manual) => manual.group === group);

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Manuals</p>
      <h1 className="mt-3 max-w-[14ch] text-hero leading-[0.95]">Read the one you run</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        Editors, JDK builds, SQL, Wolfram, and the ledgers. This is a shelf of their manuals. Forks not listed still
        have a manual. Open that one.
      </p>
      <div className="mt-6 flex gap-2 overflow-x-auto">
        {groups.map((item) => (
          <button
            key={item}
            type="button"
            onClick={() => setGroup(item)}
            className={
              "min-h-11 shrink-0 rounded-full border px-3 text-sm " +
              (group === item ? "border-fg bg-surface-2 text-fg" : "border-line text-muted")
            }
          >
            {item}
          </button>
        ))}
      </div>
      <div className="mt-6 grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,20rem)]">
        <ul className="divide-y divide-line border-y border-line">
          {rows.map((manual) => (
            <li key={manual.id}>
              <button type="button" onClick={() => setOpen(manual)} className="flex min-h-16 w-full items-baseline gap-3 py-3 text-left">
                <span className="text-xs tracking-[0.14em] text-muted uppercase">{manual.group}</span>
                <span className="text-fg">{manual.name}</span>
              </button>
            </li>
          ))}
        </ul>
        {open ? (
          <aside className="rounded-xl border border-line bg-surface p-5">
            <p className="text-xs tracking-[0.14em] text-muted uppercase">{open.group}</p>
            <h2 className="mt-2 text-3xl">{open.name}</h2>
            <p className="mt-3 text-sm text-fg/90">{open.holds}</p>
            <div className="mt-4">
              <Rtfm line={open.rtfm} />
            </div>
            <a href={open.href} target="_blank" rel="noreferrer" className="mt-4 inline-flex min-h-11 items-center text-sm underline">
              Open the manual
            </a>
          </aside>
        ) : null}
      </div>
    </main>
  );
}
