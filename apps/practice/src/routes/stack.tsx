import { createFileRoute } from "@tanstack/react-router";
import { stack } from "@/lib/course";

export const Route = createFileRoute("/stack")({
  component: StackPage,
});

function StackPage() {
  const groups = [...new Set(stack.map((s) => s.group))];
  return (
    <main>
      <p className="text-xs tracking-[0.16em] text-muted uppercase">Stack</p>
      <h1 className="mt-3 max-w-[16ch] text-4xl sm:text-5xl">What the labs stand on</h1>
      <p className="mt-4 max-w-[62ch] text-lg text-fg/85">
        Public references for the same work: the Python stack named in the outline, the methods behind each bench, and
        the security frames a detection program actually cites.
      </p>
      <div className="mt-10 space-y-10">
        {groups.map((group) => (
          <section key={group}>
            <h2 className="text-sm tracking-[0.16em] text-muted uppercase">{group}</h2>
            <ul className="mt-3 divide-y divide-line border-y border-line">
              {stack
                .filter((item) => item.group === group)
                .map((item) => (
                  <li key={item.href}>
                    <a href={item.href} className="block py-3" target="_blank" rel="noreferrer">
                      <span className="text-fg underline decoration-line underline-offset-4">{item.label}</span>
                      <span className="mt-1 block text-sm text-muted">{item.note}</span>
                    </a>
                  </li>
                ))}
            </ul>
          </section>
        ))}
      </div>
    </main>
  );
}
