import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Stage } from "@/components/stage";
import { atlas, canon, canonDomains, type CanonDomain } from "@/lib/canon";

export const Route = createFileRoute("/canon")({
  component: CanonPage,
});

function CanonPage() {
  const [domain, setDomain] = useState<CanonDomain | "all">("all");
  const rows = useMemo(
    () => (domain === "all" ? canon : canon.filter((entry) => entry.domain === domain)),
    [domain],
  );

  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Canon · primary sources</p>
      <h1 className="mt-3 max-w-[14ch] text-hero leading-[0.95]">What we cite, and what we run</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        OpenStax, NIST, the man pages, the Stanford Encyclopedia, and the public-domain Hermetica. This is a map of
        sources, not a claim to hold every paper on earth. Where a work is copyrighted, the link is the source. Exam
        questions are not stored. Occult shelves are historical texts, read beside philosophy, not as hidden physics.
      </p>
      <div className="mt-8">
        <Stage scene="monas" signal={0.35} label="The mark stands in for the shelf. The texts stay at their sources." />
      </div>
      <div className="mt-4 flex gap-2 overflow-x-auto pb-1">
        {canonDomains.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => setDomain(item.id)}
            className={
              "min-h-11 shrink-0 rounded-md border px-3 text-sm " +
              (domain === item.id ? "border-fg bg-surface-2 text-fg" : "border-line text-muted")
            }
          >
            {item.label}
          </button>
        ))}
      </div>
      <p className="num mt-3 text-sm text-muted">
        {rows.length} sources in view · {canon.length} on the shelf
      </p>
      <ul className="mt-6 divide-y divide-line border-y border-line">
        {rows.map((entry) => (
          <li key={entry.id} className="py-4">
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <h2 className="text-2xl">{entry.title}</h2>
              <span className="text-xs tracking-[0.14em] text-muted uppercase">{entry.license}</span>
            </div>
            <p className="mt-1 text-sm text-muted">{entry.source}</p>
            <p className="mt-2 max-w-[68ch] text-fg/85">{entry.implements}</p>
            <a href={entry.href} className="mt-2 inline-flex min-h-11 items-center text-sm underline" {...(entry.href.startsWith("/") ? {} : { target: "_blank", rel: "noreferrer" })}>
              {entry.href.startsWith("/") ? "Open here" : "Open the source"}
            </a>
          </li>
        ))}
      </ul>

      <section className="mt-16">
        <h2 className="text-3xl">Where the previous site went</h2>
        <p className="mt-3 max-w-[68ch] text-muted">
          The public pages — academy, cinema, coach, plant, trending, and the rest — are folded into this design. A row
          marked gap is not quietly implied.
        </p>
        <ul className="mt-6 divide-y divide-line border-y border-line">
          {atlas.map((room) => (
            <li key={room.room} className="py-4">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <h3 className="text-xl">{room.room}</h3>
                <span className={"text-xs tracking-[0.14em] uppercase " + (room.gap ? "text-warn" : "text-ok")}>
                  {room.gap ? "Gap" : "Here"}
                </span>
              </div>
              <p className="mt-1 text-sm text-muted">{room.was}</p>
              <p className="mt-2 text-fg/85">{room.now}</p>
              {room.href ? (
                <a href={room.href} className="mt-2 inline-flex min-h-11 items-center text-sm underline">
                  Go
                </a>
              ) : null}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
