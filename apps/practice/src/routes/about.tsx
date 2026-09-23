import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/about")({
  component: AboutPage,
});

export function AboutPage() {
  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">About</p>
      <h1 className="mt-3 max-w-[16ch] text-hero leading-[0.95]">The person who built the gap</h1>
      <article className="mt-8 grid gap-8 lg:grid-cols-[16rem_1fr] lg:items-start">
        <figure>
          <img
            src="/enmanuel-mejia.jpg"
            alt="Enmanuel D. Mejia, founder of Interstitium Labs"
            width={1200}
            height={1200}
            className="w-full rounded-xl border border-line object-cover"
          />
          <figcaption className="mt-3 text-xs tracking-[0.14em] text-muted uppercase">Founder · Student Zero</figcaption>
        </figure>
        <div className="max-w-[68ch]">
          <h2 className="text-3xl">Enmanuel D. Mejia</h2>
          <p className="mt-2 text-sm text-muted">Peabody / Greater Boston · Orlando targeting · EN / ES · Cloud and DevOps</p>
          <p className="mt-5 text-fg/85">
            Enmanuel is transitioning from IT operations and support into Cloud and DevOps engineering. Interstitium Labs
            and DevOps SuperLab are portfolio products, not a claim of senior production tenure or a paid studio payroll.
          </p>
          <ul className="mt-5 space-y-2 text-sm text-fg/85">
            <li>Philips Lifeline, Retention Specialist (2018–2021, Framingham): Salesforce, SAP, and Oracle data accuracy and reconnections.</li>
            <li>Certifications: CompTIA A+; Google IT Support Professional Certificate; a Boston University undergraduate computer science certificate.</li>
            <li>Earlier operations and data work includes Comcast Business, BU IT Labs, Intel, and Fidelity telecom.</li>
          </ul>
          <p className="mt-5 text-fg/85">
            Linux, networking, Azure-oriented cloud practice, infrastructure as code, containers, and CI/CD are labeled
            lab or portfolio unless paid ownership is true. Interview prep is prep, not employment.
          </p>
          <p className="mt-5 text-sm">
            <a className="underline" href="https://github.com/EnmanuelMejia">GitHub</a>
            {" · "}
            <a className="underline" href="https://www.linkedin.com/in/enmanuelmejia/">LinkedIn</a>
            {" · "}
            <a className="underline" href="mailto:edmejia@pm.me">edmejia@pm.me</a>
            {" · "}
            <a className="underline" href="https://interstitiumlabs.dev/about/">Public about</a>
          </p>
        </div>
      </article>
    </main>
  );
}
