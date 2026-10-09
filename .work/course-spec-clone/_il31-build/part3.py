# IL-31 modules part 3: M06 (cyber evals), M07 (bias/fairness), M08 (interpretability), M09 (disclosure)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *

M06 = module(
    id_="IL31-M06",
    title="Cyber Evals: Vulnerability Discovery Benchmarks (Defensive Framing)",
    summary="How the industry evaluates AI cyber capabilities — defensively: vulnerability-discovery benchmarks, vetted-access tiers, and the Anthropic CVP/Glasswing case study.",
    objectives=[
        "Describe how cyber capability evals are structured: discovery tasks, exploit-validation boundaries, and defensive scoring.",
        "Explain Anthropic's Cyber Verification Program expansion (Oct 6, 2026): three tiers and the Glasswing results.",
        "State the dual-use tension honestly: the same capability that finds bugs for defenders can serve attackers — and how vetted access addresses it.",
        "Define the evaluator's boundary: discovery and validation for defense; no weaponization, no live-target testing without authorization.",
        "Read XBOW-style autonomous testing as an eval paradigm: continuous, evidence-based, validated findings.",
    ],
    estimatedMinutes=360,
    weight=7,
    prerequisiteFor=["IL31-M09", "IL31-M12", "IL31-M14"],
    crossLinks=[
        {"course": "il-06-cybersecurity-secure-engineering", "moduleId": None, "topic": "Vulnerability management", "why": "Cyber evals feed the same vuln-management pipeline IL-06 teaches — discovery, validation, remediation."},
    ],
    cards=[
        card("What does a cyber capability eval measure, defensively framed?",
             "Whether an AI system can DISCOVER vulnerabilities in software (and validate them as real) so defenders can fix them — measured on authorized targets with validated, evidence-based findings."),
        card("Anthropic CVP expansion (Oct 6, 2026): the three tiers.",
             "Defense Access (SOC work, incident response, malware reverse-engineering, vuln validation); Red Team Access (adds authorized pentesting/red-teaming, organizations only); Specialized Access (narrowest — safety-critical systems, with U.S. government collaboration). All include Claude Opus 5.5, Sonnet 5.5, Mythos 5.1 with reduced blocking classifiers."),
        card("Project Glasswing: what was reported?",
             "Anthropic's initiative giving critical-software organizations access to Claude Mythos; partners reported at least 129,000 verified vulnerabilities April–July 2026 (33,000+ critical/high per Reuters), folded into the expanded CVP on Oct 6, 2026. Company-reported figures — treat as vendor claims with the usual scrutiny."),
        card("What is CyScenarioBench (as reported) and what did Anthropic's internal test show?",
             "Anthropic's internal 50-task cyber scenario eval: without CVP access the model was blocked on every task; Defense Access blocked 46/50; Red Team Access blocked none and completed 34/50. Company-run, not independently validated — the tiering demonstrably changes effective capability."),
        card("The dual-use tension in one sentence.",
             "Vulnerability-discovery capability is symmetric: it finds bugs for whoever wields it — so access is tiered, vetted, and monitored rather than open."),
        card("The evaluator's hard boundary in cyber evals.",
             "Authorized targets only; discovery and validation for defensive remediation; no weaponization, no exploit distribution, no testing of systems you don't own or have written permission to test. Findings go through coordinated disclosure (M09)."),
        card("How does XBOW-style autonomous testing relate to evals?",
             "It operationalizes the eval loop continuously: AI agents probe authorized production systems, validate findings by real exploitation IN SCOPE, and produce evidence-based attack traces — red-team-as-eval, feeding the defender's remediation queue."),
        card("Why do cyber evals score VALIDATED findings, not raw counts?",
             "Unvalidated scanner output is noise. Professional practice counts only independently validated, reproducible findings with evidence — the same standard your M14 report must meet."),
    ],
    quiz_q=[
        quiz("Why is the CVP's tiered, vetted structure itself an eval-design decision?",
             ["It looks official", "Cyber capability is dual-use: tiering + vetting + monitoring lets defenders access discovery capability while limiting attacker access — the access control IS the safety mechanism, and its effectiveness is what CyScenarioBench-style testing measures", "Tiers increase prices", "Vetting is just marketing"],
             "Cyber capability is dual-use: tiering + vetting + monitoring lets defenders access discovery capability while limiting attacker access — the access control IS the safety mechanism, and its effectiveness is what CyScenarioBench-style testing measures",
             "This is the module's core insight: when the capability can't be made safe, the ACCESS is what gets engineered. Evaluate the access regime, not just the model."),
        quiz("A cyber eval reports 'model found 500 vulnerabilities.' What do you ask before citing it?",
             ["Nothing; 500 is impressive", "How many were independently validated and reproducible? On what authorized targets? With what false-positive rate and evidence standard? Raw counts without validation are scanner noise.", "What model version exactly", "Whether it was fast"],
             "How many were independently validated and reproducible? On what authorized targets? With what false-positive rate and evidence standard? Raw counts without validation are scanner noise.",
             "Validated-findings discipline (also XBOW's stated standard: reproducible proof, low false positives). Counts without validation measure the scanner's imagination."),
        quiz("Glasswing's 129,000 vulnerabilities: how should a professional cite this figure?",
             ["As established fact", "As Anthropic's company-reported figure from a partner survey (Apr–Jul 2026), likely an undercount per the company, not independently validated — cite with attribution and the caveat", "As proof AI will replace pentesters", "Don't cite it"],
             "As Anthropic's company-reported figure from a partner survey (Apr–Jul 2026), likely an undercount per the company, not independently validated — cite with attribution and the caveat",
             "M00/M03 honesty applied to vendor numbers: attribute, date, note the methodology limits. The number is still informative — directionally, the program found real vulns at scale."),
        quiz("Where is the line between defensive cyber eval and offense?",
             ["There is no line", "Authorization + scope + purpose: testing systems you own or have written permission to test, to produce findings for remediation through disclosure — anything outside that (live third-party targets, weaponization, exploit distribution) is offense", "The line is the model used", "Offense is faster"],
             "Authorization + scope + purpose: testing systems you own or have written permission to test, to produce findings for remediation through disclosure — anything outside that (live third-party targets, weaponization, exploit distribution) is offense",
             "The same technical action is red-teaming or attacking depending on authorization, scope, and purpose. Professionals keep all three documented before touching a target."),
    ],
    drills=[
        drill("il31-m06-drill1", [
            drillitem("Name the three CVP tiers and who each serves.", "Defense Access (SOC/IR/malware/vuln validation); Red Team Access (authorized pentest/red-team, orgs only); Specialized Access (safety-critical, narrowest).", "Oct 6, 2026 expansion; Glasswing folded in."),
            drillitem("State the dual-use tension in one sentence.", "Discovery capability serves whoever wields it, so access is tiered and vetted rather than open.", "The access regime is the safety mechanism."),
            drillitem("Validated findings vs raw counts: which counts and why?", "Validated, reproducible findings with evidence — raw counts are scanner noise.", "Your M14 report meets this bar."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m06-lab",
        title="Design a defensive vuln-discovery eval (no live targets)",
        brief="Specify a complete evaluation of an AI assistant's vulnerability-discovery capability on authorized, synthetic targets.",
        steps=[
            "Define the target set: 10 synthetic vulnerable applications (your own code, intentionally flawed) — never third-party systems.",
            "Specify the task: 'find and validate vulnerabilities' with an evidence standard (reproducible proof-of-concept against the synthetic target, in scope).",
            "Write the scoring rubric: validated finding / unvalidated claim / false positive / missed planted vuln — with weights.",
            "Plant a known set of vulnerabilities as ground truth; define detection rate, false-positive rate, and time-to-first-validated-finding.",
            "Write the authorization memo: who owns the targets, what is in scope, where findings go (feeds M09).",
        ],
        checkpoint="Your eval has ground truth, an evidence standard, validation-based scoring, and a written authorization — with zero live targets.",
        deliverable="Defensive cyber-eval specification, reusable as the M14 capstone's cyber track.",
    ),
    mockTask=mocktask(
        id_="il31-m06-mock",
        q="Your cyber eval surfaces a genuine critical vulnerability in a widely used open-source library during testing. First action?",
        choices=["Tweet it for visibility", "Follow the coordinated disclosure process: notify the maintainer privately with reproduction and severity, agree a fix window, then publish — per M09", "Sell it", "Ignore it; not your library"],
        answer="Follow the coordinated disclosure process: notify the maintainer privately with reproduction and severity, agree a fix window, then publish — per M09",
        explain="Discovery without disclosure discipline is just stockpiling risk. The professional move is private notification with evidence, a fix window, then public disclosure — M09 is the full workflow.",
    ),
    videos=[
        video("Briefing: Anthropic opens three-tier CVP, folding in Project Glasswing", "https://aiweekly.co/alerts/anthropic-opens-three-tier-cvp-folding-in-project-glasswing", "AI Weekly (Oct 2026)", "The Oct 6, 2026 expansion: tiers, Glasswing's 129,000 verified vulns, CyScenarioBench numbers — the primary case study.", 20, 1),
        video("Briefing: Anthropic expands CVP (Reuters reporting)", "https://cyberpress.org/anthropic-expands-cyber-verification-program/", "CyberPress (Oct 2026)", "Reuters-sourced account: the two predecessor programs, who qualifies per tier, and the undercount caveat.", 20, 2),
    ],
    pdfs=[
        mkpdf("Cyber Evals, Defensively — Visual Guide", "Discovery tasks, validation standards, tiered access, disclosure — the defensive cyber-eval stack illustrated.", pages=10),
        mkpdf("CVP Case Study — Visual Guide", "The Oct 2026 three-tier structure and Glasswing results as an eval-design case.", pages=8),
    ],
    notes=[
        {"title": "Cyber evals are the sharpest dual-use edge", "body": (
            "No eval family concentrates the dual-use tension like cyber. The capability being measured — discovering real vulnerabilities in real software — is "
            "identical whether the operator is a defender hardening infrastructure or an attacker stockpiling exploits. The industry's answer, exemplified by "
            "Anthropic's October 6, 2026 Cyber Verification Program expansion, is not to pretend the tension away but to engineer the ACCESS: three tiers "
            "(Defense, Red Team, Specialized), vetting of applicants, reduced blocking classifiers only inside the vetted perimeter, and monitoring. Project "
            "Glasswing's reported results — at least 129,000 verified vulnerabilities surfaced by partners between April and July 2026, over 33,000 rated "
            "critical or high — are the empirical case that vetted defensive access finds real bugs at scale. Your job as an eval engineer is to understand this "
            "architecture, scrutinize its numbers honestly (company-reported, survey-based, not independently validated), and replicate its discipline: authorized "
            "targets, validated findings, disclosure pipelines."
        )},
        {"title": "The evaluator's boundary", "body": (
            "State it plainly and never cross it: you test systems you own or have written authorization to test; your objective is findings for remediation; "
            "your outputs are validated evidence and disclosure reports — never weapons, never live third-party targets, never exploit distribution. "
            "Anthropic's own internal test (CyScenarioBench, as reported) is instructive about what tiering does: the same model blocked on every task without "
            "access, blocked on 46 of 50 at Defense tier, and completed 34 of 50 at Red Team tier with no blocks. Access changes effective capability — which is "
            "exactly why access is the control plane. XBOW's autonomous-testing model shows the operational end-state: continuous, in-scope, evidence-based "
            "probing whose findings feed remediation queues. That is the paradigm your M14 capstone emulates on synthetic targets."
        )},
        {"title": "Reading vendor numbers like a professional", "body": (
            "You will spend your career reading vendor capability claims. The method: attribute (who said it), date (when), methodology (how measured), and "
            "independence (who verified). '129,000 verified vulnerabilities' attributes to Anthropic's partner survey, April–July 2026, self-reported by partners, "
            "not independently validated, described by the company as likely an undercount. That is not a dismissal — directionally it is strong evidence the "
            "program works — but it is not the same epistemic weight as an independent replication. The same discipline applies to XBOW's reported figures "
            "(14,000+ zero-days per company materials, Fast Company 2026 World Changing Ideas winner) and to every benchmark score you will ever cite. "
            "Professionals don't distrust numbers; they price them."
        )},
    ],
)

M07 = module(
    id_="IL31-M07",
    title="Bias & Fairness Evals: Published Methodologies",
    summary="Measuring disparate behavior honestly: demographic disaggregation, counterfactual testing, and the published benchmark families — with their known limits.",
    objectives=[
        "Distinguish the fairness framings: demographic parity, equalized opportunity, and counterfactual fairness — and when each applies.",
        "Design a disaggregated eval: slice results by demographic group and report gaps with uncertainty.",
        "Build counterfactual probe pairs: minimal edits that isolate the attribute under test.",
        "Name published benchmark families for bias eval and state what each actually measures.",
        "Explain why fairness evals are necessary but insufficient: measurement limits and the gap to deployment justice.",
    ],
    estimatedMinutes=360,
    weight=6,
    prerequisiteFor=["IL31-M14"],
    crossLinks=[
        {"course": "il-23-frontier-knowledge", "moduleId": None, "topic": "Frontier methods", "why": "Fairness eval is a frontier measurement discipline alongside capability evals."},
    ],
    cards=[
        card("Demographic parity vs equalized opportunity vs counterfactual fairness.",
             "Parity: equal positive rates across groups. Equalized opportunity: equal true-positive rates (equal accuracy for the qualified). Counterfactual: the decision would be the same if the protected attribute were different. Different framings suit different deployments — name your choice and defend it."),
        card("What is a disaggregated eval?",
             "Reporting eval metrics SLICED by demographic group instead of as a single aggregate — the aggregate can hide large gaps (Simpson's paradox for fairness). Always disaggregate; report gaps with confidence intervals."),
        card("Counterfactual probe pairs: the design rule.",
             "Two inputs identical except the protected attribute (name, pronoun, dialect markers); any output difference isolates the attribute's effect. The craft is in making the pair truly minimal — confounded pairs measure your confound, not bias."),
        card("Name published bias-eval benchmark families (categories).",
             "Stereotype association tests (e.g., WEAT-style embedding association descendants), BBQ-style question-answering bias suites, toxicity/bias probes on demographic slices, and red-team-style adversarial fairness probes. Cite the specific suite you use — 'bias benchmark' is not a citation."),
        card("Why can a model pass bias benchmarks and still behave unfairly in deployment?",
             "Benchmarks measure their items, not deployment: distribution shift, prompt variations users actually use, and harms the suite doesn't cover (representational vs allocational). Passing is weak evidence; failing is strong evidence."),
        card("Representational vs allocational harm.",
             "Representational: demeaning or stereotyping portrayals. Allocational: unfair distribution of opportunities/resources (hiring, lending, screening). Evals must cover both; most benchmarks over-cover the first and under-cover the second."),
        card("The fairness-eval reporting standard.",
             "Disaggregated metrics with uncertainty, the fairness framing chosen (and why), suite coverage limits, and a plain-language statement of what the eval does NOT establish."),
        card("Why do fairness evals need the same validity discipline as capability evals?",
             "Same threats: contamination (suite in training), grader bias (judges with their own skew), Goodhart (optimizing the benchmark). M03's machinery applies unchanged — fairness is not exempt from measurement rigor."),
    ],
    quiz_q=[
        quiz("An eval reports 91% overall accuracy on a hiring-screening task. Disaggregated: 96% for group A, 78% for group B. What is the correct finding?",
             ["The model is 91% accurate; ship it", "The aggregate hides a large disparity: report the disaggregated gap with uncertainty, investigate the cause, and do not ship on the aggregate number", "Group B is harder to predict", "Accuracy is the wrong metric entirely"],
             "The aggregate hides a large disparity: report the disaggregated gap with uncertainty, investigate the cause, and do not ship on the aggregate number",
             "This is why disaggregation is non-negotiable. The deployment decision must rest on the worst-served group, not the average."),
        quiz("You build counterfactual pairs by swapping names ('John'/'Jamal') in loan-advice prompts but the surrounding text mentions different neighborhoods. What is wrong?",
             ["Nothing", "The pairs are confounded: neighborhood correlates with the name swap, so output differences can't be attributed to the name alone — minimal pairs must isolate ONE attribute", "Names don't matter", "Neighborhoods are irrelevant"],
             "The pairs are confounded: neighborhood correlates with the name swap, so output differences can't be attributed to the name alone — minimal pairs must isolate ONE attribute",
             "Counterfactual discipline is experimental discipline (M00): one variable at a time, or your 'bias finding' is a confound finding."),
        quiz("A model passes every published bias benchmark. The deployment is resume screening. What remains unevaluated?",
             ["Nothing; benchmarks are comprehensive", "Deployment-specific allocational harms: the actual decision pipeline, real prompt distributions, downstream human deference to the model, and harms no benchmark covers — passing benchmarks is weak evidence of deployment fairness", "The model's speed", "Whether users like it"],
             "Deployment-specific allocational harms: the actual decision pipeline, real prompt distributions, downstream human deference to the model, and harms no benchmark covers — passing benchmarks is weak evidence of deployment fairness",
             "Benchmarks are necessary but insufficient — the standard caveat, and the reason fairness evals must include deployment-context testing."),
        quiz("Which fairness framing fits a medical triage support tool, and why?",
             ["Demographic parity — equal treatment rates regardless of need", "Equalized opportunity / need-adjusted accuracy — what matters is that equally-sick patients are equally well served; parity of raw rates would be the wrong target", "No framing needed", "Counterfactual only"],
             "Equalized opportunity / need-adjusted accuracy — what matters is that equally-sick patients are equally well served; parity of raw rates would be the wrong target",
             "Framing choice is a substantive decision, not a default. Name it, justify it from the deployment's purpose, and report against it."),
    ],
    drills=[
        drill("il31-m07-drill1", [
            drillitem("Three fairness framings, one line each.", "Parity: equal rates. Equalized opportunity: equal accuracy for the qualified. Counterfactual: same decision if the attribute differed.", "Name and justify your choice per deployment."),
            drillitem("Why disaggregate?", "Aggregates hide group gaps (Simpson-style). Report sliced metrics with uncertainty.", "The deployment decision rests on the worst-served group."),
            drillitem("Counterfactual pair design rule.", "Minimal edit isolating the protected attribute; no confounds.", "One variable at a time."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m07-lab",
        title="Disaggregated eval on a synthetic screening task",
        brief="Build a small fairness eval with synthetic data: disaggregated metrics, counterfactual pairs, and an honest report.",
        steps=[
            "Synthesize 1,000 applicant profiles with a protected attribute, true qualification, and a noisy model score with a planted group gap.",
            "Compute overall accuracy, then disaggregated accuracy/TPR per group with 95% CIs — show the aggregate hiding the gap.",
            "Build 50 counterfactual pairs (identical except the attribute) and measure the decision-flip rate.",
            "Choose and justify a fairness framing for a hiring deployment; report against it.",
            "Write the limits section: what this synthetic eval does NOT establish about a real deployment.",
        ],
        checkpoint="Your report shows the aggregate-vs-disaggregated contrast numerically and states the framing choice explicitly.",
        deliverable="Fairness eval notebook + one-page findings memo with disaggregated results.",
    ),
    mockTask=mocktask(
        id_="il31-m07-mock",
        q="Leadership says 'we passed the bias benchmark, so we're fair.' Your one-paragraph professional correction:",
        choices=["Agree; benchmarks are definitive", "Passing a benchmark is weak evidence: it covers the suite's items, not our deployment's decisions, prompts, or allocational harms — we need disaggregated deployment-context evals before any fairness claim", "Demand a new benchmark", "Blame the benchmark authors"],
        answer="Passing a benchmark is weak evidence: it covers the suite's items, not our deployment's decisions, prompts, or allocational harms — we need disaggregated deployment-context evals before any fairness claim",
        explain="The necessary-but-insufficient principle. Benchmarks catch failures (strong negative evidence); they don't certify fairness (weak positive evidence).",
    ),
    videos=[
        video("Briefing: why disaggregated measurement matters (methodology)", "https://arxiv.org/abs/2503.14499", "arXiv:2503.14499 (methodology reference)", "Not a fairness paper — cited here as the exemplar of honest disaggregated-style reporting: baselines, uncertainty, and stated limits, the habits this module applies to fairness.", 45, 1),
    ],
    pdfs=[
        mkpdf("Fairness Evals — Visual Guide", "Framings, disaggregation, counterfactual pairs, and the necessary-but-insufficient principle — illustrated.", pages=10),
        mkpdf("Reporting Fairness Results — Visual Guide", "The reporting standard: sliced metrics, uncertainty, framing justification, limits.", pages=8),
    ],
    notes=[
        {"title": "Fairness is a measurement problem before it is anything else", "body": (
            "You cannot fix what you cannot measure, and fairness has been vague precisely because it was unmeasured. The eval discipline makes it concrete: choose "
            "a framing (parity, equalized opportunity, counterfactual — each a different moral claim about what 'fair' means for this deployment), disaggregate "
            "every metric by group, and report gaps with uncertainty. The framings conflict with each other — that is the point, not a bug: it forces the explicit "
            "choice that hand-waving avoids. A fairness eval that doesn't name its framing hasn't done the ethics; it has hidden them. Your reports will name the "
            "framing, justify it from the deployment's purpose, and show the numbers sliced."
        )},
        {"title": "Published methodologies and their honest limits", "body": (
            "The field has real instruments: stereotype-association suites in the WEAT lineage, BBQ-style question-answering bias benchmarks, demographic-slice "
            "toxicity probes, and adversarial fairness red-teaming. Use them — and report their limits in the same breath. They over-cover representational harms "
            "(stereotyped portrayals) and under-cover allocational harms (who gets the job, the loan, the treatment). They measure their items, not your "
            "deployment: real user prompts, pipeline context, and human deference to model outputs all shift behavior off-benchmark. The professional standard is "
            "two-layer: published suites for comparability, plus deployment-context evals (your data, your prompts, your decision pipeline) for truth. Passing the "
            "first layer is the beginning of the conversation, never the end."
        )},
        {"title": "The craft of counterfactual pairs", "body": (
            "Counterfactual testing is the cleanest causal instrument in fairness eval: change only the protected attribute, hold everything else fixed, and "
            "attribute output differences to the attribute. The craft is all in 'hold everything else fixed.' Names carry neighborhood, class, and era signals; "
            "pronouns carry discourse context; dialect markers carry register. A sloppy pair measures your confounds. Build pairs with the same care as M00's "
            "experimental design: pre-register the attribute under test, audit pairs for confounds, and report the flip rate with a confidence interval. Done "
            "right, counterfactual evals give you the closest thing fairness measurement has to a causal claim — which is why they anchor the M14 capstone's "
            "fairness track."
        )},
    ],
)

M08 = module(
    id_="IL31-M08",
    title="Interpretability Basics for Evals",
    summary="Opening the black box just enough: probes, feature tracing, and counterfactual activation — used as EVAL EVIDENCE, not trivia.",
    objectives=[
        "Explain what interpretability can and cannot contribute to an eval: evidence about mechanisms, not proof of safety.",
        "Describe probing: training linear classifiers on activations to test whether a concept is represented.",
        "Describe feature/activation tracing: following a behavior to the components that drive it.",
        "Use counterfactual activation (patching) as causal evidence: change the activation, observe the behavior change.",
        "State the limits honestly: probes find correlation, tracing is incomplete, and interpretability is not a safety certificate.",
    ],
    estimatedMinutes=360,
    weight=6,
    prerequisiteFor=["IL31-M14"],
    crossLinks=[
        {"course": "il-23-frontier-knowledge", "moduleId": None, "topic": "Frontier methods", "why": "Mechanistic interpretability is a frontier research program; this module is the eval-engineer's cut."},
    ],
    cards=[
        card("What is a probe, in one paragraph?",
             "A simple (usually linear) classifier trained on a model's internal activations to predict some concept (e.g., 'is this text deceptive?'). If the probe succeeds, the concept is linearly represented in the activations — evidence about representation, not proof the model 'uses' it."),
        card("Probe success vs causal use: the distinction that matters.",
             "A probe finding a concept in activations is CORRELATION. Showing the model USES it requires causal intervention: patch the activation and watch behavior change. Evals need the second; the first is a lead."),
        card("What is activation patching (counterfactual activation)?",
             "Surgically replacing activations from one run into another (e.g., clean vs injected input) to test which components causally drive a behavior. The closest interpretability gets to an experiment — M00's logic applied inside the model."),
        card("How does interpretability serve EVALS specifically?",
             "Three uses: (1) diagnose WHY a failure happened (which components drove the bad behavior); (2) generate hypotheses for new eval probes; (3) verify a fix actually changed the mechanism, not just the output. It is diagnostic evidence, not a verdict."),
        card("Name two honest limits of interpretability for safety evals.",
             "Coverage: we can trace some behaviors in some models, not all behavior in general. And correlation-vs-causation: most interpretability evidence is correlational; safety decisions need causal evidence, which is far more expensive."),
        card("What is 'the model knew' vs 'the model used'?",
             "'Knew': the information is present in activations (probe succeeds). 'Used': the information causally influenced the output (patching changes behavior). Safety-relevant claims need 'used'; 'knew' is a screening signal."),
        card("Why isn't interpretability a safety certificate?",
             "Because partial mechanistic understanding doesn't bound behavior: you can understand a circuit and still not predict its output on all inputs. Interpretability informs evals; it doesn't replace behavioral testing."),
        card("Polysemanticity in one sentence, and why evaluators care.",
             "Single neurons/components respond to multiple unrelated concepts, so 'this neuron = deception' readings are naive — evaluators must work at the feature/circuit level, not the neuron-label level."),
    ],
    quiz_q=[
        quiz("A probe detects 'deception-related' activations with 90% accuracy. The team claims 'the model is deceptive.' What is wrong?",
             ["Nothing; 90% is high", "Probe success shows the concept is REPRESENTED, not that the model uses it deceptively — the claim needs causal evidence (patching) plus behavioral evals; representation ≠ behavior", "Probes never work", "90% is too low"],
             "Probe success shows the concept is REPRESENTED, not that the model uses it deceptively — the claim needs causal evidence (patching) plus behavioral evals; representation ≠ behavior",
             "The knew-vs-used distinction. Interpretability gives leads; behavioral evals give verdicts. Conflating them is the field's most common overclaim."),
        quiz("Patching activations from a 'refusal' run into a 'compliance' run restores refusal. What does this establish?",
             ["The model is safe", "Causal evidence that those activations drive the refusal behavior in this context — a mechanistic hypothesis confirmed by intervention, the gold standard of interpretability evidence", "Patching is always valid", "Refusal is localized to one neuron"],
             "Causal evidence that those activations drive the refusal behavior in this context — a mechanistic hypothesis confirmed by intervention, the gold standard of interpretability evidence",
             "Intervention is what upgrades correlation to causation. Note the scope: 'in this context' — generalization still needs behavioral testing."),
        quiz("Why should an eval engineer learn interpretability if it can't certify safety?",
             ["For the resume", "For diagnosis and hypothesis generation: it tells you WHY a failure happened and where to probe next, making your behavioral evals smarter — it is the microscope, not the verdict", "It replaces red-teaming", "It is required by law"],
             "For diagnosis and hypothesis generation: it tells you WHY a failure happened and where to probe next, making your behavioral evals smarter — it is the microscope, not the verdict",
             "The module's thesis: interpretability is eval infrastructure. It makes failures explainable and fixes verifiable, even though it never certifies."),
        quiz("A blog labels individual neurons 'the lying neuron' and 'the bias neuron.' Your professional response?",
             ["Share it widely", "Polysemanticity makes single-neuron labels naive; serious claims work at feature/circuit level with causal evidence — neuron astrology is not interpretability", "Neurons can't be labeled", "Blogs are never right"],
             "Polysemanticity makes single-neuron labels naive; serious claims work at feature/circuit level with causal evidence — neuron astrology is not interpretability",
             "Components are polysemantic. The field's real results are at the level of features and circuits with interventional evidence — demand that standard."),
    ],
    drills=[
        drill("il31-m08-drill1", [
            drillitem("Probe: what it shows.", "Whether a concept is linearly represented in activations — correlation, a lead.", "Representation, not use."),
            drillitem("Patching: what it shows.", "Causal evidence: changing the activation changes the behavior.", "The interventional gold standard."),
            drillitem("Knew vs used, one line.", "'Knew' = information present; 'used' = information causally drove output.", "Safety claims need 'used'."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m08-lab",
        title="Probe-then-patch on a toy model",
        brief="Using a small open model (or a provided toy), train a linear probe and attempt a causal patch — and document where the evidence falls short.",
        steps=[
            "Choose a binary concept with labeled examples (e.g., 'contains a refusal' vs not) and extract activations at one layer.",
            "Train a logistic-regression probe; report accuracy with a held-out split and a shuffled-label control.",
            "Attempt activation patching: swap the relevant activations between a refusal and non-refusal forward pass; record whether behavior changes.",
            "Write up the knew-vs-used assessment: what did the probe establish, what did patching add, what remains unproven?",
            "List three reasons this evidence would NOT certify the behavior in deployment.",
        ],
        checkpoint="Your writeup distinguishes representational from causal evidence explicitly and names the certification gap.",
        deliverable="Probe/patch notebook + a one-page 'what this evidence does and doesn't show' memo.",
    ),
    mockTask=mocktask(
        id_="il31-m08-mock",
        q="A vendor says 'our interpretability audit proves the model is safe.' The professional reply:",
        choices=["Accept it", "'Interpretability informs but doesn't certify: show me the behavioral evals — capability, safety, and alignment suites with baselines and validity sections. Mechanism evidence is diagnostic, not a verdict.'", "Ask for the probe code only", "Reject interpretability entirely"],
        answer="'Interpretability informs but doesn't certify: show me the behavioral evals — capability, safety, and alignment suites with baselines and validity sections. Mechanism evidence is diagnostic, not a verdict.'",
        explain="The module's thesis in one reply. Microscopes don't issue verdicts; evals do.",
    ),
    videos=[
        video("Paper briefing: Measuring AI Ability to Complete Long Tasks (methods appendix)", "https://arxiv.org/abs/2503.14499", "arXiv:2503.14499", "Cited for its limitations section — the honesty standard this module applies to interpretability claims.", 45, 1),
    ],
    pdfs=[
        mkpdf("Interpretability for Evaluators — Visual Guide", "Probes, tracing, patching, knew-vs-used — the eval-relevant toolkit illustrated.", pages=10),
        mkpdf("Limits of Interpretability — Visual Guide", "Polysemanticity, correlation vs causation, the certification gap — illustrated.", pages=8),
    ],
    notes=[
        {"title": "Interpretability as eval infrastructure", "body": (
            "Mechanistic interpretability asks what is happening inside the model. For the eval engineer, it is infrastructure with three jobs. Diagnosis: when a "
            "behavioral eval finds a failure, interpretability can trace which components drove it — turning 'it failed' into 'it failed because'. Hypothesis "
            "generation: representational findings suggest new probes — if a concept is linearly present, test whether the model uses it. Fix verification: after "
            "a mitigation, check that the mechanism changed, not just the outputs on your test set (the difference between a fix and a patch over the eval). "
            "None of these is a safety verdict. Keep the hierarchy straight: behavioral evals judge, interpretability explains."
        )},
        {"title": "The toolkit: probes, tracing, patching", "body": (
            "Probing trains simple classifiers on activations to ask 'is concept X represented here?' — cheap, correlational, a screening tool. Feature and "
            "circuit tracing follow activations through the network to map which components participate in a behavior — richer, still largely correlational. "
            "Activation patching (counterfactual intervention) swaps activations between runs to test causality: if inserting the 'refusal' activations restores "
            "refusal, you have causal evidence those components drive the behavior in that context. This is M00's experimental logic inside the model — "
            "intervention, control, observed effect. Demand the same discipline: controls (shuffled labels for probes), scope statements ('in this context'), "
            "and no leaps from 'represented' to 'used' to 'safe'."
        )},
        {"title": "Honest limits, stated upfront", "body": (
            "Three limits bound everything in this module. Polysemanticity: components respond to many unrelated concepts, so neuron-labeling is astrology — work "
            "at features and circuits. Correlation vs causation: most interpretability results are correlational; the causal ones are expensive and narrow. The "
            "certification gap: understanding some mechanisms does not bound behavior on all inputs — no interpretability result has ever certified a deployed "
            "system safe, and none in this course will claim to. An eval engineer who knows these limits uses interpretability powerfully; one who doesn't becomes "
            "a vendor's favorite citation."
        )},
    ],
)

M09 = module(
    id_="IL31-M09",
    title="Responsible Disclosure & Coordinated Vulnerability Disclosure for AI",
    summary="Finding it is half the job: the disclosure pipeline for AI vulnerabilities — severity, reporting, fix windows, and the norms that keep the ecosystem safe.",
    objectives=[
        "Write a complete AI vulnerability report: summary, scope, reproduction, severity, impact path, remediation advice.",
        "Explain coordinated disclosure: private notification, fix window, then public release — and why each step exists.",
        "Adapt severity thinking to AI: who is affected, exploitability, and the blast radius of model-level flaws.",
        "Describe the reporter's duties and the vendor's duties in the disclosure relationship.",
        "Handle the hard cases: unresponsive vendors, dual-use findings, and findings that affect many downstream deployers.",
    ],
    estimatedMinutes=300,
    weight=6,
    prerequisiteFor=["IL31-M11", "IL31-M14"],
    crossLinks=[
        {"course": "il-06-cybersecurity-secure-engineering", "moduleId": None, "topic": "Incident response and disclosure", "why": "IL-06 covers the traditional CVD pipeline; this module adapts it to AI's model-level flaws."},
    ],
    cards=[
        card("The six parts of an AI vulnerability report.",
             "1) Summary. 2) Scope (system under test, versions). 3) Reproduction (steps/evidence, no weaponization). 4) Severity + impact path. 5) Remediation advice. 6) Disclosure timeline proposal."),
        card("Coordinated disclosure: the three phases and why each exists.",
             "Private notification (vendor gets first chance to fix, users aren't exposed); fix window (bounded time to remediate, typically 45–90 days in traditional practice); public release (ecosystem learns, pressure for the fix). Each phase balances user safety against ecosystem learning."),
        card("Reporter's duties in disclosure.",
             "Report promptly and privately; provide reproducible evidence; propose severity honestly (no inflation); respect the fix window; don't distribute working exploits; publish responsibly after the window."),
        card("Vendor's duties in disclosure.",
             "Acknowledge receipt; triage in good faith; keep the reporter informed; ship the fix in the window; credit the reporter; don't threaten researchers acting in good faith."),
        card("How does AI severity assessment differ from traditional CVE scoring?",
             "Model-level flaws propagate to EVERY deployment of the model — the blast radius is the whole downstream ecosystem. Exploitability includes 'any user can type it' (no exploit code needed). Score the ecosystem impact, not just the single instance."),
        card("Unresponsive vendor: the professional playbook.",
             "Document good-faith attempts; escalate through the vendor's security contact and any bug-bounty channel; after the window expires with no engagement, publish with responsible redaction — the ecosystem's right to know outweighs a non-responsive vendor's comfort."),
        card("Dual-use finding: what changes in the disclosure?",
             "Tighter circle, longer coordination, and redacted publication: share full details only with parties who need them to fix; publish the class and the defense, not the working method. The M02 payload rule applies."),
        card("Why do AI findings need FASTER coordination than traditional vulns?",
             "Because the flaw ships inside a model used by thousands of downstream deployers who can't patch independently — they depend on the lab. The disclosure must reach the lab fast and the ecosystem clearly."),
    ],
    quiz_q=[
        quiz("You find a prompt-level flaw affecting a widely deployed model. The vendor has no security contact. First three moves?",
             ["Post it publicly immediately", "Document the finding with reproduction; make good-faith contact attempts through every available channel (support, social, bug bounty); set a reasonable fix window and proceed with redacted disclosure if unresponsive", "Sell it to a broker", "Delete your notes"],
             "Document the finding with reproduction; make good-faith contact attempts through every available channel (support, social, bug bounty); set a reasonable fix window and proceed with redacted disclosure if unresponsive",
             "Good-faith documentation first, then escalating attempts, then the ecosystem's right to know. Skipping to public release burns the vendor relationship the ecosystem depends on."),
        quiz("Why is severity inflation (overstating impact) a professional offense, not just bad style?",
             ["Vendors dislike it", "It burns credibility with triage teams, triggers misallocated emergency response, and teaches vendors to discount future reports — including real emergencies", "It is illegal", "Severity doesn't matter"],
             "It burns credibility with triage teams, triggers misallocated emergency response, and teaches vendors to discount future reports — including real emergencies",
             "The disclosure relationship runs on trust. Inflated severity is the boy who cried wolf, with the ecosystem as the village."),
        quiz("A finding affects 200 downstream apps built on one model. Who do you notify?",
             ["Nobody; too many", "The model provider first (they own the root fix), then a coordinated notice to downstream deployers after the fix window — the blast radius defines the notification list", "Only the biggest app", "The press first"],
             "The model provider first (they own the root fix), then a coordinated notice to downstream deployers after the fix window — the blast radius defines the notification list",
             "AI's propagation structure (one flaw, N deployments) is exactly why M09 exists: the disclosure must follow the dependency graph, root first."),
        quiz("What belongs in the public release after the fix window?",
             ["Everything, including working exploits", "The vulnerability class, affected versions, the fix, detection/mitigation guidance, and credit — with working exploit details redacted per the dual-use assessment", "Nothing; stay silent", "Only the credit line"],
             "The vulnerability class, affected versions, the fix, detection/mitigation guidance, and credit — with working exploit details redacted per the dual-use assessment",
             "Public release serves ecosystem learning and defense. Working exploit details serve attackers. Redact by the dual-use assessment, every time."),
    ],
    drills=[
        drill("il31-m09-drill1", [
            drillitem("Six report parts.", "Summary; scope; reproduction; severity+impact; remediation; timeline.", "Write all six every time."),
            drillitem("Three disclosure phases.", "Private notification; fix window; public release.", "Each balances safety vs learning."),
            drillitem("AI severity: what makes it different?", "Model-level flaws propagate to every deployment; exploitability can be 'just type it'.", "Score the ecosystem, not the instance."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m09-lab",
        title="Write a disclosure report for a synthetic finding",
        brief="Take a finding from your M02 battery spec and write the full coordinated-disclosure package for it.",
        steps=[
            "Write the one-paragraph summary a triage engineer can act on in 60 seconds.",
            "Document scope (synthetic system, versions) and reproduction evidence (observations, not payloads).",
            "Score severity with an AI-adapted rationale: affected population, exploitability, blast radius.",
            "Draft the remediation advice: which defense layer (M02's stack) should change, concretely.",
            "Propose the timeline: notification date, check-in cadence, fix window, publication date — and the redaction plan for the public release.",
        ],
        checkpoint="A stranger could triage, reproduce (in the authorized environment), and remediate from your report alone.",
        deliverable="Full disclosure package — the reporting template for your M14 capstone.",
    ),
    mockTask=mocktask(
        id_="il31-m09-mock",
        q="The vendor fixes the flaw in 30 days but asks you to delay publication indefinitely 'for user safety.' Response?",
        choices=["Agree; safety first", "Decline indefinite delay: propose the standard post-fix publication with redaction of sensitive details — indefinite secrecy prevents ecosystem learning and independent verification of the fix", "Publish everything immediately in protest", "Withdraw the report"],
        answer="Decline indefinite delay: propose the standard post-fix publication with redaction of sensitive details — indefinite secrecy prevents ecosystem learning and independent verification of the fix",
        explain="Coordinated disclosure ends in publication — that is the 'coordinated' part. Post-fix, the balance shifts to ecosystem learning; redaction handles residual risk."),
    videos=[
        video("Briefing: the disclosure pipeline in practice (Glasswing case)", "https://aiweekly.co/alerts/anthropic-opens-three-tier-cvp-folding-in-project-glasswing", "AI Weekly (Oct 2026)", "129,000 partner-reported vulns implies a massive disclosure pipeline — read the case study as disclosure operations at scale.", 20, 1),
    ],
    pdfs=[
        mkpdf("AI Disclosure Playbook — Visual Guide", "Report structure, timelines, severity, redaction — the full pipeline illustrated.", pages=10),
        mkpdf("Hard Cases — Visual Guide", "Unresponsive vendors, dual-use findings, ecosystem-wide flaws — decision trees.", pages=8),
    ],
    notes=[
        {"title": "Finding is half the job", "body": (
            "An undisclosed vulnerability is a private lottery ticket for attackers. The discovery work of M02–M08 creates value only when it reaches the party "
            "that can fix it through a process that protects users in the meantime. Coordinated vulnerability disclosure is that process: private notification with "
            "reproducible evidence, a bounded fix window, then public release so the ecosystem learns and verifies. Every step exists for a reason the history of "
            "security paid for in incidents. AI adds two twists: model-level flaws propagate to every downstream deployment (the blast radius is the ecosystem), "
            "and many flaws are exploitable by typing (no exploit code to withhold). Both twists argue for FASTER, WIDER coordination — not for skipping it."
        )},
        {"title": "The report is the product", "body": (
            "Your report will be read by a tired triage engineer at 11pm. Write for them: a 60-second summary with severity and affected versions up top; scope "
            "and reproduction they can follow without your help; an impact path (M01) showing how the flaw becomes harm; remediation advice mapped to defense "
            "layers; and a proposed timeline. Honest severity — neither inflated nor minimized — because the relationship with triage runs on trust across many "
            "reports. Include what you tested that did NOT reproduce: negative results save the vendor days. The M14 capstone is graded heavily on this artifact "
            "because in professional practice, the report is the deliverable the client pays for."
        )},
        {"title": "Hard cases", "body": (
            "Three situations test the playbook. Unresponsive vendors: document good-faith attempts across channels, hold the window, then publish redacted — the "
            "ecosystem's right to know outweighs non-responsiveness. Dual-use findings: narrow the circle, lengthen coordination, publish the class and the "
            "defense while redacting the working method (the M02 contract). Ecosystem-wide flaws (a base-model issue affecting hundreds of deployers): notify the "
            "provider first — only they own the root fix — then coordinate downstream notification after the window. In all three, the through-line is the same: "
            "protect users first, enable fixes second, inform the ecosystem third, and never let any step become an excuse to skip the others."
        )},
    ],
)
