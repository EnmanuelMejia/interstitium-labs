# TPM track retrofit content (il-18) — keys: summary, concepts, procedure, brief, honesty, quiz
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["tpm-interview-prep--program-design-iv"] = {
"summary": (
"Welcome to the Technical Program Management track — I'm your instructor, and this is Module 1: Program Design. "
"Program design is the TPM's core artifact: turning an ambiguous mandate into scope, milestones, dependencies, "
"risks, and a communication plan that survives contact with four teams and two time zones. "
"By the end of this module you will be able to scope an ambiguous initiative on the fly, map milestones and "
"dependencies explicitly, define success criteria with real exit conditions, and walk an interviewer through a "
"program brief the way the case rounds score it."
),
"concepts": """- **Program design** — The TPM's core artifact: turning an ambiguous mandate into scope, milestones, dependency maps, risks, and a communication plan.
- **Scoping ambiguous initiatives** — Drawing the boundary of a program: what is in, what is out, and what is explicitly deferred — before execution starts.
- **Milestones** — Named, dated, verifiable waypoints on the path to the program outcome; the skeleton the schedule hangs on.
- **Dependency mapping** — Making cross-team commitments explicit, owned, and sequenced — hidden dependencies are where programs die.
- **Success criteria** — The measurable definition of done; without them, "launch" is a matter of opinion.
- **Exit conditions** — The conditions under which the program stops: done, de-scoped, or cancelled — preventing zombie programs that never end.
- **Risk register** — The program's risk ledger: each risk with likelihood, impact, mitigation, and an owner — reviewed on a cadence, not filed away.
- **Stakeholder mapping** — Knowing who is impacted, who decides, and who needs informing — drawn before the program needs them.
- **Communication cadence** — The rhythm of information flow: right information to right stakeholders at the right tempo — preventing both surprise escalations and meeting sprawl.
- **Launch readiness** — The checklist proving the program can ship: owners, rollback, comms, and support — readiness verified, not assumed.""" ,
"procedure": """Run the 45-minute program-design interview rep. Set a timer — the case rounds are scored under pressure, so rehearse under pressure.
1. Take a blank page and write the ambiguous mandate at the top in one sentence — e.g. "Ship a new checkout flow across four teams in one quarter."
2. Scope it aloud: name three things in scope, two things explicitly out, and one thing deferred — ambiguity resolved on paper first.
3. List five milestones with verifiable done-states — "API contract frozen" not "API work done."
4. Draw the dependency map: every arrow is a cross-team commitment with an owner; circle the two you would worry about most and say why.
5. Write the success criteria with exit conditions: the metric that says "done," and the condition that would stop the program.
6. Fill a risk register: three risks, each with likelihood, impact, a mitigation, and an owner.
7. Design the communication cadence: who gets what, on what rhythm — the escalation path for when a dependency slips.
8. Close by reading back the one-page program brief: problem, scope, milestones, risks, asks — in under two minutes, as you would to the interviewer.""",
"brief": """Your interview prep brief: produce the one-page program brief for a cross-team launch and defend it in a 45-minute case rep.
The scenario. You are the TPM for a new checkout flow that touches the storefront team, payments team, fraud team, and data platform team, with two of the four teams in different time zones. Launch is one quarter out and the mandate is still ambiguous.
Deliverables.
- A one-page program brief: problem, scope (in/out/deferred), five milestones with verifiable done-states, a dependency map with owners, success criteria with exit conditions, a risk register (likelihood, impact, mitigation, owner), and a communication cadence with escalation paths.
- A two-minute verbal walkthrough of the brief as you would deliver it in the case round.
Grading lens. The interviewer scores structured thinking, not the right answer: did ambiguity shrink on paper, are dependencies owned, are exit conditions real, and did the verbal walkthrough land the structure without rambling? Time yourself; the round is 45 minutes.""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. TPM case rounds score how you structure ambiguity, and the strongest answers are built from your own real programs: use the frameworks here to organize your own experience, not to narrate someone else's. Interviewers can always tell the difference.""",
"quiz": [
("The TPM's core artifact for ambiguity is:", ["A date", "Scope, milestones, dependencies, risks, and a comms plan", "A budget", "A headcount"], 1, "Program design turns an ambiguous mandate into executable structure — the Concepts note lists every piece of the artifact."),
("Exit conditions exist to prevent:", ["Launches", "Zombie programs that never end", "Planning", "Having risks"], 1, "Done must be defined and the stop conditions written down, or the program can never officially end — the Concepts glossary defines exit conditions as the conditions under which the program stops."),
("A risk register needs, at minimum:", ["Hopes", "Likelihood, impact, mitigations, and owners — reviewed on cadence", "A long document", "Secrecy"], 1, "The Concepts note is explicit: each risk carries likelihood, impact, mitigation, and an owner, and the register is reviewed on a cadence — not filed away."),
("Stakeholder maps are drawn:", ["After launch", "Before the program needs them", "Never", "At the retrospective"], 1, "The Concepts note says stakeholder mapping is drawn before the program needs them — you map who is impacted, who decides, and who informs upfront."),
("A milestone is strongest when it is:", ["A named, dated, verifiable waypoint with a done-state", "A vague phase name", "A meeting on the calendar", "A team name"], 0, "Milestones are the schedule's skeleton — the Hands-on procedure requires verifiable done-states like 'API contract frozen,' not 'API work done.'"),
("In the 45-minute program-design rep, scoping comes:", ["Last", "Before execution planning — in scope, out of scope, deferred", "Never", "After the retrospective"], 1, "The procedure puts scoping first: name what is in, what is out, and what is deferred before any milestones — ambiguity resolved on paper first."),
("A dependency map is dangerous when it contains:", ["Named owners", "Unowned arrows — commitments nobody owns", "Sequencing", "Dates"], 1, "The Concepts note warns that hidden, unowned dependencies are where programs die — every arrow in the map must be owned."),
("The communication cadence must include:", ["The holiday schedule", "An escalation path for when a dependency slips", "Everyone's lunch preferences", "A logo"], 1, "The procedure ends the brief with the escalation path: who gets what, on what rhythm, and what happens when a dependency slips."),
("Launch readiness is proven by:", ["A date on the calendar", "Verified owners, rollback, comms, and support — not assumed", "A press release", "Hope"], 1, "The Concepts glossary defines launch readiness as a verified checklist: owners, rollback, comms, support — verified, not assumed."),
("The two-minute verbal walkthrough of the brief is scored on:", ["Charisma", "Landing the structure — scope, milestones, dependencies, risks, asks — without rambling", "Speed of speech", "Slide design"], 1, "The Project brief's grading lens: the interviewer scores structured thinking, not the right answer — and no rambling."),
]}
