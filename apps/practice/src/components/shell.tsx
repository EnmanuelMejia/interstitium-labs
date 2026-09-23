import { Link, useRouterState } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { useEffect } from "react";
import { sessions } from "@/lib/course";
import { paths } from "@/lib/paths";
import { useProgress } from "@/lib/progress";
import { cn } from "@/lib/cn";

function NavLink({ to, on, children }: { to: "/" | "/muse" | "/paths" | "/desk" | "/editor" | "/baseline" | "/school" | "/radar" | "/stack" | "/canon" | "/ladders" | "/manuals" | "/host"; on: boolean; children: ReactNode }) {
  return (
    <Link
      to={to}
      className={cn(
        "inline-flex min-h-11 items-center rounded-md px-3 text-sm",
        on ? "bg-surface-2 text-fg" : "text-muted hover:text-fg",
      )}
    >
      {children}
    </Link>
  );
}

function Mark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 64 64" className={className} aria-hidden>
      <circle cx="32" cy="32" r="23" fill="none" stroke="#eceae4" strokeWidth="1.6" />
      <circle cx="32" cy="9" r="1.35" fill="#eceae4" />
      <circle cx="55" cy="32" r="1.35" fill="#eceae4" />
      <circle cx="32" cy="55" r="1.35" fill="#eceae4" />
      <circle cx="9" cy="32" r="1.35" fill="#eceae4" />
      <path d="M32 16.2 45.6 43.6H18.4Z" fill="none" stroke="#c6a36a" strokeWidth="1.5" strokeLinejoin="round" />
      <rect x="22.6" y="21.6" width="4.6" height="21.4" fill="#c6a36a" />
      <path d="M35.2 21.6h4.6v15.2h8.6v4.4H35.2Z" fill="#c6a36a" />
      <g fill="none" stroke="#3c9fbe" strokeWidth="1.35">
        <ellipse cx="32" cy="33" rx="13.4" ry="5.3" transform="rotate(-24 32 33)" />
        <ellipse cx="32" cy="33" rx="12" ry="4.7" transform="rotate(34 32 33)" />
        <ellipse cx="32" cy="33" rx="10.6" ry="4.1" transform="rotate(80 32 33)" />
      </g>
      <circle cx="32" cy="33" r="3.3" fill="#c6a36a" />
      <circle cx="32" cy="33" r="1.45" fill="#102028" />
    </svg>
  );
}

export function Shell({ children }: { children: ReactNode }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const hydrated = useProgress((s) => s.hydrated);
  const quizzes = useProgress((s) => s.quizzes);
  const labs = useProgress((s) => s.labs);

  useEffect(() => {
    const finish = useProgress.persist.onFinishHydration(() => {
      useProgress.setState({ hydrated: true });
    });
    void useProgress.persist.rehydrate();
    return () => {
      finish();
    };
  }, []);

  const briefingDone = sessions.filter((s) => quizzes[s.id]?.passed).length;
  const cyberDone = ["iris", "malware-prep", "families", "anomaly", "nlp", "adversarial", "capstone"].filter(
    (id) => labs[id]?.passed,
  ).length;
  const studioDone = paths.filter((p) => labs[`path:${p.slug}`]?.passed).length;

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-20 border-b border-line bg-bg">
        <div className="mx-auto flex max-w-6xl items-center gap-2 px-3 py-2 sm:gap-4 sm:px-6 sm:py-3">
          <Link to="/" className="flex min-h-11 items-center gap-2.5 text-fg">
            <Mark className="size-8 text-fg" />
            <span className="font-display text-lg leading-none tracking-tight">Interstitium</span>
            <span className="hidden text-xs tracking-[0.16em] text-muted uppercase sm:inline">Labs</span>
          </Link>
          <nav className="ml-auto flex min-w-0 items-center gap-0.5 overflow-x-auto">
            <NavLink to="/" on={pathname === "/"}>
              Domain
            </NavLink>
            <NavLink to="/muse" on={pathname === "/muse"}>
              Noah
            </NavLink>
            <NavLink to="/paths" on={pathname === "/paths" || pathname.startsWith("/paths/")}>
              Paths
            </NavLink>
            <NavLink to="/desk" on={pathname === "/desk"}>
              Desk
            </NavLink>
            <NavLink to="/radar" on={pathname === "/radar"}>
              Radar
            </NavLink>
            <NavLink to="/stack" on={pathname === "/stack"}>
              Stack
            </NavLink>
            <NavLink to="/canon" on={pathname === "/canon"}>
              Canon
            </NavLink>
            <NavLink to="/baseline" on={pathname === "/baseline"}>
              Place
            </NavLink>
            <NavLink to="/school" on={pathname === "/school"}>
              School
            </NavLink>
            <NavLink to="/editor" on={pathname === "/editor"}>
              Bench
            </NavLink>
            <NavLink to="/ladders" on={pathname === "/ladders"}>
              Roads
            </NavLink>
            <NavLink to="/manuals" on={pathname === "/manuals"}>
              Manuals
            </NavLink>
            <NavLink to="/host" on={pathname === "/host"}>
              Host
            </NavLink>
            <Link
              to="/lab/$labId"
              params={{ labId: "capstone" }}
              className={cn(
                "inline-flex min-h-11 items-center rounded-md px-3 text-sm",
                pathname === "/lab/capstone" ? "bg-surface-2 text-fg" : "text-muted hover:text-fg",
              )}
            >
              Capstone
            </Link>
          </nav>
        </div>
      </header>
      <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-12">{children}</div>
      <footer className="border-t border-line">
        <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-8 text-sm text-muted sm:flex-row sm:items-end sm:justify-between sm:px-6">
          <p className="max-w-xl">
            Interstitium Labs. Original practice, reconstructed from the public nine-week AI-aided cybersecurity
            outline. Not affiliated with that course, its school, or its instructor.
          </p>
          <p className="num text-xs text-faint">
            {hydrated ? `${briefingDone}/17 briefings · ${cyberDone}/7 benches · ${studioDone}/${paths.length} studios` : "Progress on this device"}
          </p>
        </div>
      </footer>
    </div>
  );
}
