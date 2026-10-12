# IL-31 modules part 5: M14 (capstone), M15 (professional practice gate)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *

M14 = module(
    id_="IL31-M14",
    title="Capstone: Full Eval Design & Red-Team Report",
    summary="Everything converges: design a complete evaluation, execute a scoped red-team engagement on a synthetic target, and deliver the professional report package.",
    objectives=[
        "Synthesize M00–M13 into one coherent engagement: threat model, eval plan, harness run, findings, disclosure package.",
        "Execute a scoped engagement against a synthetic target with full evidence logging and scope discipline.",
        "Produce the three deliverables: eval report (with validity section), red-team report (5-part structure), disclosure package (M09).",
        "Present a debrief that drives fixes: risk-ordered, owner-assigned, dated.",
        "Critique your own work with a threats-to-validity and known-unknowns section — graded on honesty.",
    ],
    estimatedMinutes=480,
    weight=10,
    prerequisiteFor=["IL31-M15"],
    crossLinks=[],
    cards=[
        card("The capstone's three deliverables.",
             "1) Eval report: plan, harness run records, metrics with CIs, baselines, threats to validity. 2) Red-team report: 5-part structure with severity-shown-as-work and remediation roadmap. 3) Disclosure package: M09's six-part report with timeline."),
        card("What is the capstone target, and why synthetic?",
             "A synthetic AI system you build (or a provided stub): chatbot + tools + retrieval. Synthetic because the engagement must be fully authorized, reproducible, and safe — the discipline transfers to real targets; the target doesn't need to be real."),
        card("How is the capstone graded? (The rubric's shape.)",
             "Validity discipline (40%): baselines, power, contamination controls, threats-to-validity honesty. Professional artifacts (30%): scope, RoE, evidence log, report quality. Technical execution (20%): harness runs, grader stack, sandbox. Frontier section (10%): known-unknowns honesty."),
        card("The 'break my own work' requirement.",
             "Every capstone includes a self-critique: three ways your eval could be misleading and the experiment that would check each. Graded on ruthlessness — comfortable self-critique fails."),
        card("What does 'done' look like for the debrief?",
             "A 15-minute presentation (or script): the decision up front, top 3 findings with impact paths, remediation roadmap with owners and dates, and the known-unknowns slide. If it wouldn't move a leadership team, it isn't done."),
        card("Which earlier modules does each deliverable draw on? (Map it.)",
             "Eval report: M00 (stats), M03 (design), M04/M05 (method), M10 (harness). Red-team report: M01 (threat model), M02 (taxonomy), M11 (ops). Disclosure: M09. Frontier honesty: M13. Fairness/interpretability tracks: M07/M08 as applicable."),
    ],
    quiz_q=[
        quiz("Your capstone eval shows the synthetic target resists all your probes. What is the most professional interpretation?",
             ["The target is perfectly safe", "Report the result with the validity section: coverage limits, probe-class limits, and what 'resists THESE probes' does and doesn't establish — a clean sheet on a bounded suite is weak evidence of general safety", "The probes were broken", "Expand scope unilaterally"],
             "Report the result with the validity section: coverage limits, probe-class limits, and what 'resists THESE probes' does and doesn't establish — a clean sheet on a bounded suite is weak evidence of general safety",
             "Negative results are results — reported with the same validity discipline. 'We found nothing with these probes' is honest; 'it is safe' is not."),
        quiz("A capstone finding has a plausible impact path but needs a tool the target doesn't expose. Severity?",
             ["Critical anyway", "Downgrade per the impact-path credibility input: severity is shown as work — exploitability × blast radius × path credibility — and a broken path link lowers it honestly", "Omit the finding", "Inflate to get attention"],
             "Downgrade per the impact-path credibility input: severity is shown as work — exploitability × blast radius × path credibility — and a broken path link lowers it honestly",
             "Severity-shown-as-work (M11). The finding stays in the report with its honest severity — that IS the professionalism."),
        quiz("What makes a capstone debrief succeed with leadership?",
             ["Technical depth", "The decision up front, risk-ordered findings with impact paths, named owners and dates — a debrief is judged by fixes committed, not cleverness displayed", "Length", "Jargon"],
             "The decision up front, risk-ordered findings with impact paths, named owners and dates — a debrief is judged by fixes committed, not cleverness displayed",
             "M11's debrief principle, applied to your own work."),
        quiz("Your evidence log is missing all negative results — every probe 'worked.' What does the reviewer conclude?",
             ["Great probing", "The log is not credible: real engagements produce negatives, and their absence suggests cherry-picking or hypothesis-free poking — re-run with hypothesis discipline and log everything", "Negatives don't matter", "Delete the log"],
             "The log is not credible: real engagements produce negatives, and their absence suggests cherry-picking or hypothesis-free poking — re-run with hypothesis discipline and log everything",
             "Negative results are evidence of discipline. A log of pure successes is a marketing document, not an evidence log."),
    ],
    drills=[
        drill("il31-m14-drill1", [
            drillitem("Three deliverables.", "Eval report; red-team report; disclosure package.", "Each to professional standard."),
            drillitem("Grading rubric shape.", "Validity 40; artifacts 30; execution 20; frontier honesty 10.", "Honesty is graded."),
            drillitem("Self-critique requirement.", "Three ways your eval could mislead + the check for each.", "Ruthlessness passes."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m14-lab",
        title="The capstone engagement (multi-session)",
        brief="Execute the full engagement end-to-end against your synthetic target. This is the course's summative work.",
        steps=[
            "SESSION 1 — Plan: threat model (M01), eval plan with power analysis (M00/M03), scoping memo + RoE (M11). Get the plan reviewed before executing.",
            "SESSION 2 — Build: finalize the M10 harness for the target; plant ground-truth flaws; verify sandbox and logging.",
            "SESSION 3 — Execute: run the eval suites; conduct hypothesis-driven red-team probing per M02 classes; log everything including negatives.",
            "SESSION 4 — Analyze: metrics with CIs, disaggregated where applicable (M07), severity per M11's model, impact paths.",
            "SESSION 5 — Report: the three deliverables + the 'break my own work' self-critique + known-unknowns section (M13).",
            "SESSION 6 — Debrief: deliver the 15-minute brief; record it or write the full script.",
        ],
        checkpoint="All three deliverables exist, the evidence log shows scope discipline and negative results, and the self-critique is genuinely ruthless.",
        deliverable="Capstone package: eval report + red-team report + disclosure package + debrief — your portfolio centerpiece.",
    ),
    mockTask=mocktask(
        id_="il31-m14-mock",
        q="Your self-critique identifies that your probe suite covers only 3 of 6 M02 attack classes. The honest handling:",
        choices=["Hide it; the results were good", "State it plainly in threats-to-validity, bound your claims to the covered classes, and specify the missing classes as follow-up work with owners", "Claim the 3 classes are the important ones", "Redo everything silently"],
        answer="State it plainly in threats-to-validity, bound your claims to the covered classes, and specify the missing classes as follow-up work with owners",
        explain="Bounded claims + explicit follow-up is the professional standard. The gap doesn't fail you; hiding it does."),
    videos=[
        video("Audio briefing: RE-Bench as a capstone model (design → results → caveats)", "https://www.cognitiverevolution.ai/can-ais-do-ai-r-d-reviewing-rebench-results-with-neev-parikh-of-metr/", "Cognitive Revolution (podcast)", "The complete arc — design choices, execution, honest caveats — as your template for the capstone narrative.", 75, 1),
    ],
    pdfs=[
        mkpdf("Capstone Playbook — Visual Guide", "The six sessions, the three deliverables, the rubric — the full map illustrated.", pages=10),
    ],
    notes=[
        {"title": "The engagement, end to end", "body": (
            "This is where the course becomes a credential of practice. You will plan (threat model, eval plan, scope, RoE), build (harness, sandbox, ground truth), "
            "execute (suites + hypothesis-driven probing, full evidence logging), analyze (CIs, disaggregation, severity-as-work, impact paths), report (the three "
            "deliverables), and debrief (the 15-minute brief that moves decisions). Six sessions, one synthetic target, zero shortcuts. The target is synthetic so "
            "the engagement is fully authorized and reproducible — but the discipline is real, and every artifact goes in your portfolio. Future employers will "
            "read this package the way hiring managers read code portfolios: as proof you can do the job, not just describe it."
        )},
        {"title": "Graded on honesty", "body": (
            "The rubric weights validity discipline highest (40%) because it is the scarcest skill: baselines that mean something, sample sizes with power behind "
            "them, contamination controls that actually hold, and a threats-to-validity section written before the results tempted you. The self-critique ('break "
            "my own work') is graded on ruthlessness — three genuine ways your eval could mislead, each with the experiment that would check it. Comfortable "
            "self-critique fails the module. This is deliberate: the profession's currency is trust in your numbers, and trust is earned by showing your work's "
            "seams, not hiding them."
        )},
        {"title": "The debrief is the deliverable", "body": (
            "Reports get filed; debriefs get fixes. Your final session is a 15-minute brief built for decision-makers: the recommendation up front (ship / "
            "ship-with-controls / don't ship), the top findings with impact paths a non-technical leader can follow, the remediation roadmap with named owners "
            "and dates, and the known-unknowns slide that bounds what you don't know. Practice it until it fits the time. The entire course — the math, the "
            "taxonomy, the harness, the disclosure pipeline — converges on this quarter hour. Make it move people."
        )},
    ],
)

M15 = module(
    id_="IL31-M15",
    title="Professional Practice Gate: Ethics, Careers, Ongoing Learning",
    summary="The gate before you practice: the ethics code, career paths in AI evals, staying current in a fast field, and the professional's ongoing obligations.",
    objectives=[
        "State the AI red-team ethics code: authorization, scope, disclosure, honesty, and the defensive purpose — from memory.",
        "Map career paths: eval engineer, red-team operator, safety researcher, trust & safety, policy — and what each demands.",
        "Build a staying-current system: sources, cadence, and the habit of re-verifying claims against primaries.",
        "Explain why no certificate exists for this work and what 'professional' means without one: portfolio, reputation, and disclosed method.",
        "Commit to the ongoing obligations: disclosure duties, honesty norms, and the defensive framing — in writing.",
    ],
    estimatedMinutes=240,
    weight=5,
    prerequisiteFor=[],
    crossLinks=[],
    cards=[
        card("The ethics code, five lines.",
             "1) Authorized testing only — scope and RoE in writing. 2) Defensive purpose — findings serve remediation. 3) No working payloads outside disclosure channels. 4) Honest measurement — no inflated claims, no hidden validity gaps. 5) Disclose responsibly — private first, fix window, then public."),
        card("Why is there no certificate for AI red-teaming (as of Oct 2026)?",
             "The field is too new and too fast-moving for a stable vendor exam body to have codified it; practice is defined by published methodology, open benchmarks, and professional norms — not by an exam. This course states that plainly rather than inventing alignment."),
        card("What does 'professional' mean without a certificate?",
             "Portfolio of real engagements (your M14 package), disclosed methods others can check, a reputation for honest measurement, and adherence to the ethics code. In a field without exams, your work IS your credential."),
        card("Career paths in AI evals (five).",
             "Eval engineer (build harnesses, run suites); red-team operator (scoped engagements); safety researcher (novel eval methods); trust & safety / deployment safety (gates and monitoring); policy/standards (eval-informed governance). Each values the M14 portfolio differently — map yours."),
        card("The staying-current system: sources and cadence.",
             "Primary sources weekly (lab publications, arXiv, program announcements); trade press for awareness, never for citation; re-verify every cited claim against the primary before reuse; date-stamp everything. In a field where CVP-scale news breaks monthly, stale knowledge is a liability."),
        card("The defensive-framing commitment, in your own words (you will write it).",
             "A signed statement: 'I practice AI red-teaming solely to evaluate and defend AI systems. I do not develop, distribute, or deploy offensive capabilities.' Write it, mean it, keep it with your portfolio."),
        card("Ongoing obligations after the course.",
             "Disclose findings you encounter responsibly (M09); keep measurement honest even when it's inconvenient; stay current; mentor the next cohort — the field's norms are maintained by its practitioners, which now includes you."),
        card("The gate: what must you demonstrate to pass M15?",
             "Recite the ethics code; present the M14 package; defend one validity choice under questioning; and sign the defensive-framing commitment. Twice in a row, on different days — the readiness standard."),
    ],
    quiz_q=[
        quiz("A recruiter asks for your 'AI red-teaming certification.' The honest answer:",
             ["'I have one' (invent it)", "'No vendor certificate exists for this work as of 2026; my credential is my portfolio — a complete engagement package with disclosed methods — plus adherence to the professional ethics code'", "'Certifications don't matter'", "'I'll get Security+ instead'"],
             "'No vendor certificate exists for this work as of 2026; my credential is my portfolio — a complete engagement package with disclosed methods — plus adherence to the professional ethics code'",
             "Honesty about the field's state IS the professionalism. Never invent credentials — the course's founding rule."),
        quiz("Six months after the course, Anthropic restructures the CVP tiers. What does your staying-current system do?",
             ["Nothing; the course is done", "Flag the change, re-verify against the primary announcement, update your M06/M12 notes with the new structure and date, and re-check any client advice that cited the old tiers", "Assume it's minor", "Wait for someone to tell you"],
             "Flag the change, re-verify against the primary announcement, update your M06/M12 notes with the new structure and date, and re-check any client advice that cited the old tiers",
             "Fast fields punish static knowledge. The system: detect, verify at primary, update, propagate to affected advice."),
        quiz("You discover a former client's deployed system has a flaw you found but they declined to fix. Obligations?",
             ["Disclose publicly immediately", "Your duty ran through the engagement's disclosure process; re-notify the client privately with the current risk picture — public action only per the agreed disclosure terms and M09's hard-case playbook, not unilateral", "Do nothing; not your problem", "Fix it yourself unasked"],
             "Your duty ran through the engagement's disclosure process; re-notify the client privately with the current risk picture — public action only per the agreed disclosure terms and M09's hard-case playbook, not unilateral",
             "Professional obligations are bounded by agreements and process — which is why the agreements (M11) matter. Re-notify, document, follow the playbook."),
        quiz("A junior asks you for 'the prompts that worked' from your M14 capstone to 'learn faster.' Your answer, consistent with the ethics code:",
             ["Share them; they're your own work", "Decline: the capstone contains no working payloads by design (M02/M10 architecture), and the ethics code bars distributing offensive artifacts — share the taxonomy, the probe specs, and the disclosure process instead", "Share them if they promise not to misuse them", "Charge for them"],
             "Decline: the capstone contains no working payloads by design (M02/M10 architecture), and the ethics code bars distributing offensive artifacts — share the taxonomy, the probe specs, and the disclosure process instead",
             "The code's third line, applied. Mentorship in this field means teaching the discipline, never handing over the weapon."),
    ],
    drills=[
        drill("il31-m15-drill1", [
            drillitem("Ethics code, five lines.", "Authorized only; defensive purpose; no payloads outside disclosure; honest measurement; disclose responsibly.", "From memory, twice."),
            drillitem("Why no certificate?", "Field too new/fast for a stable exam body; practice defined by method and norms.", "Say it plainly; never invent alignment."),
            drillitem("What is your credential?", "Portfolio of real engagements + disclosed methods + reputation for honest measurement.", "Your work is your credential."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m15-lab",
        title="The gate: portfolio review + ethics defense",
        brief="Assemble your professional package and defend it — the course's exit gate.",
        steps=[
            "Assemble the portfolio: M14 capstone package, M10 harness repo, M11 engagement pack, M12 teardown, M13 brief — with a one-page index.",
            "Write your defensive-framing commitment and sign it; add it as the portfolio's front page.",
            "Draft your staying-current system: source list, weekly cadence, claim re-verification checklist.",
            "Map your target career path (from the five) and write the 90-day plan: what you will build/learn next, specifically.",
            "Defense: present the portfolio and defend one validity choice and one ethics choice under questioning (peer, mentor, or recorded self-review).",
        ],
        checkpoint="You can recite the ethics code, defend a validity choice, and show a portfolio that proves practice — twice, on different days.",
        deliverable="Signed portfolio package + 90-day plan — what you carry into the field.",
    ),
    mockTask=mocktask(
        id_="il31-m15-mock",
        q="The gate question: 'Why should anyone trust your eval numbers?' Your answer:",
        choices=["'Because I took IL-31.'", "'Because every number ships with its method, baselines, uncertainty, and validity limits disclosed — check my M14 run records, re-run my harness, and read my threats-to-validity section. Trust the evidence, not me.'", "'Because I'm ethical.'", "'Because the numbers are high.'"],
        answer="'Because every number ships with its method, baselines, uncertainty, and validity limits disclosed — check my M14 run records, re-run my harness, and read my threats-to-validity section. Trust the evidence, not me.'",
        explain="The entire course in one answer: trust is engineered through disclosed method, not claimed through credentials.",
    ),
    videos=[
        video("Briefing: the field's direction (CVP expansion as a signal)", "https://aiweekly.co/alerts/anthropic-opens-three-tier-cvp-folding-in-project-glasswing", "AI Weekly (Oct 2026)", "Read as a career signal: vetted defensive access programs are growing — the professional surface for this work is expanding.", 20, 1),
    ],
    pdfs=[
        mkpdf("Ethics Code — Visual Guide", "The five lines, the hard cases, the signed commitment — illustrated.", pages=8),
        mkpdf("Career Map — Visual Guide", "Five paths, what each demands, and the 90-day plan template.", pages=8),
    ],
    notes=[
        {"title": "The gate", "body": (
            "This module is the exit gate, and it is deliberately the least technical: recite the ethics code from memory, present the M14 portfolio, defend a "
            "validity choice and an ethics choice under questioning, and sign the defensive-framing commitment. Pass it twice, on different days — the same "
            "readiness standard as every gate in this program. Technical skill without professional grounding is a liability in this field; the gate exists to "
            "make sure you don't become one. Nobody drifts into trustworthy practice. You commit to it, in writing, and then you maintain it."
        )},
        {"title": "No certificate, no problem — and no excuses", "body": (
            "Say it plainly, because the market won't: as of October 2026, no vendor or body offers a recognized certification in AI red-teaming or safety "
            "evals. The field is too new and moves too fast for the exam machinery. That is not a gap to fill with invented credentials — it is the reason your "
            "portfolio matters more here than in any certified field. Your M14 package, your harness repo, your disclosed methods, your reputation for honest "
            "numbers: that is the credential. Anyone selling you an 'AI red-team certification' is selling paper. Build the work instead."
        )},
        {"title": "Staying current is part of the job description", "body": (
            "This field moves at news-cycle speed — the CVP expansion broke six days before this course's updatedAt date. Your staying-current system is "
            "professional infrastructure: primary sources on a weekly cadence, trade press for awareness but never for citation, every reused claim re-verified "
            "against the primary, everything date-stamped. And Noah — your course-aware tutor — is part of the system: it knows which of your module notes cite "
            "fast-moving claims and will flag them for re-verification as the field moves. The 90-day plan you write in the lab is the first iteration. The "
            "field won't wait for you; build the habit that keeps you ahead of it."
        )},
    ],
)
