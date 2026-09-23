import { createFileRoute, Link, Outlet, useRouterState } from "@tanstack/react-router";
import { paths } from "@/lib/paths";

export const Route = createFileRoute("/paths")({
  component: PathsPage,
});

function PathsPage() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  if (pathname !== "/paths") return <Outlet />;
  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Paths · curriculum OS</p>
      <h1 className="mt-3 max-w-[16ch] text-hero leading-[0.95]">What you will be able to do</h1>
      <p className="mt-5 max-w-[62ch] text-lg text-fg/85">
        Every path on the curriculum, including the AI-aided cybersecurity domain folded in from the public nine-week
        outline. Each path has a Three.js stage, a reading, and a simulation whose pass bar tightens as you raise the
        load. The cybersecurity path is the long one: seventeen briefings and seven benches under Domain.
      </p>
      <ul className="mt-10 divide-y divide-line border-y border-line">
        {paths.map((p) => (
          <li key={p.slug}>
            <Link to="/paths/$slug" params={{ slug: p.slug }} className="flex min-h-16 items-baseline gap-4 py-3">
              <span className="min-w-0 flex-1">
                <span className="block text-fg">{p.title}</span>
                <span className="mt-1 block text-sm text-muted">{p.outcome}</span>
              </span>
              <span className="hidden shrink-0 text-sm text-faint sm:inline">{p.scene}</span>
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
