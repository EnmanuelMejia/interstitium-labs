import { createFileRoute } from "@tanstack/react-router";
import { ladders } from "@/lib/ladders";

export const Route = createFileRoute("/ladders")({
  component: LaddersPage,
});

function LaddersPage() {
  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Ladders · by role</p>
      <h1 className="mt-3 max-w-[14ch] text-hero leading-[0.95]">A role, then a rung, never a date</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        The shape borrowed from career-path schools is the order: role, certification catalog, practice. The exams,
        the IDEs, and the textbooks stay at their publishers. Nothing here is proprietary courseware, and nothing is due.
      </p>
      <ol className="mt-10 space-y-10">
        {ladders.map((ladder) => (
          <li key={ladder.id} className="rounded-xl border border-line bg-surface p-5">
            <p className="text-xs tracking-[0.14em] text-muted uppercase">{ladder.pace}</p>
            <h2 className="mt-2 text-3xl">{ladder.role}</h2>
            <p className="mt-3 max-w-[68ch] text-sm text-muted">{ladder.note}</p>
            <ol className="mt-5 divide-y divide-line border-y border-line">
              {ladder.rungs.map((rung, i) => (
                <li key={rung.name} className="py-3">
                  <p className="text-fg">
                    <span className="num mr-3 text-sm text-muted">0{i + 1}</span>
                    {rung.name}
                  </p>
                  <p className="mt-1 text-sm text-muted">{rung.practice}</p>
                  {rung.href ? (
                    <a href={rung.href} className="mt-2 inline-flex min-h-11 items-center text-sm underline" target={rung.href.startsWith("/") ? undefined : "_blank"} rel={rung.href.startsWith("/") ? undefined : "noreferrer"}>
                      {rung.href.startsWith("/") ? "Open the practice" : "Source"}
                    </a>
                  ) : null}
                </li>
              ))}
            </ol>
            <a href={ladder.catalog.href} className="mt-4 inline-flex min-h-11 items-center text-sm underline" target="_blank" rel="noreferrer">
              {ladder.catalog.label}
            </a>
          </li>
        ))}
      </ol>
      <p className="mt-8 max-w-[68ch] text-sm text-muted">
        Open lectures live in the canon: MIT OpenCourseWare, Carnegie Mellon’s Open Learning Initiative, and CS50.
        Khan, Brilliant, ALEKS, Codecademy, boot.dev, and KodeKloud are the delivery ideas — one problem, a real
        terminal, a role ladder — not content we host.
      </p>
    </main>
  );
}
