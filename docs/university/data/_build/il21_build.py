"""Assemble IL-21 course JSON."""
import json, sys
sys.path.insert(0, "/home/hatch/workspace/apex-audit/docs/university/data/_build")
from il21_a import MODULES_A
from il21_b import MODULES_B

modules = MODULES_A + MODULES_B

DRILLS = [
 {"id": "drill-fallacy", "title": "Fallacy spotter", "prompt": "'We must rewrite or the system will collapse' (no evidence given).",
  "choices": ["Ad hominem", "False dilemma", "Straw man", "Valid argument"], "answer": 1,
  "explain": "Two options asserted without ruling out the rest."},
 {"id": "drill-kant", "title": "Tradition check", "prompt": "'Act only on maxims you could will as universal law' is:",
  "choices": ["Utilitarianism", "Virtue ethics", "Kant's categorical imperative", "Egoism"], "answer": 2,
  "explain": "First formulation of the categorical imperative (Groundwork, 1785)."},
 {"id": "drill-popper", "title": "Science check", "prompt": "A claim compatible with every observation is:",
  "choices": ["Well confirmed", "Unfalsifiable \u2014 unscientific by Popper's criterion", "A paradigm", "Statistically proven"], "answer": 1,
  "explain": "Falsifiability is Popper's demarcation line."},
 {"id": "drill-sunk", "title": "Cost check", "prompt": "$2M spent; next phase costs $200K for $150K value. Decide:",
  "choices": ["Continue to protect the $2M", "Stop \u2014 sunk cost; marginal cost > benefit", "Spend $2M more", "Pause and hope"], "answer": 1,
  "explain": "Sunk costs are irrelevant; decide at the margin."},
 {"id": "drill-nash", "title": "Game check", "prompt": "A Nash equilibrium is a profile where:",
  "choices": ["Everyone is happiest", "No one gains by unilateral deviation", "All cooperate", "Payoffs are equal"], "answer": 1,
  "explain": "Stable against unilateral moves \u2014 not necessarily good."},
 {"id": "drill-ip", "title": "IP check", "prompt": "An MIT license on code is:",
  "choices": ["A patent", "A copyright license granting permissions", "A trademark", "Legally void"], "answer": 1,
  "explain": "Copyright vests automatically; the license grants permissions with conditions."}
]

SCENARIOS = [
 {
  "id": "sc-ai-deployment", "title": "AI Deployment Ethics Review",
  "context": "Your team built a resume-screening model. It is 12% more 'accurate' than human screeners on historical data, but an audit shows it downgrades resumes with employment gaps \u2014 disproportionately affecting caregivers returning to work. Leadership wants to ship Friday.",
  "steps": [
   {"prompt": "How do you frame the decision?",
    "options": [
     {"text": "Run the three-traditions analysis before deciding: duties, consequences, and character", "correct": True, "why": "The traditions structure the trade-off instead of letting urgency decide: deontology flags treating applicants as mere means, consequentialism weighs aggregate hiring gains vs. harms, virtue asks what a good craftsperson ships."},
     {"text": "Ship it \u2014 12% accuracy gain is the only metric that matters", "correct": False, "why": "Accuracy on biased historical data is not the same as a good hiring decision; the metric begs the question."},
     {"text": "Kill the project quietly without analysis", "correct": False, "why": "Avoidance without reasoning teaches the org nothing and may forfeit real benefits a constrained deployment could capture."}]},
   {"prompt": "Analysis done. What do you recommend?",
    "options": [
     {"text": "Constrained pilot: remove the gap-penalizing features, add human review of edge cases, instrument outcomes, revisit in 90 days", "correct": True, "why": "Collingridge-aware: reversible, monitored, humble. It captures value while containing the foreseeable harm \u2014 and generates the data a fuller decision needs."},
     {"text": "Full deployment with a fairness statement on the website", "correct": False, "why": "A statement doesn't change the model's behavior; this is ethics theater."},
     {"text": "Hand the decision to legal alone", "correct": False, "why": "Legal sets the floor, not the ceiling \u2014 'lawful' and 'right' are different questions."}]}
  ]
 },
 {
  "id": "sc-dual-use", "title": "The Dual-Use Dilemma",
  "context": "Your open-source computer-vision library \u2014 built for wildlife conservation \u2014 is being forked for automated targeting in a conflict zone. Contributors are split: pull the repo, or keep shipping?",
  "steps": [
   {"prompt": "First, how do you think about it?",
    "options": [
     {"text": "Dual-use analysis: same mechanism, divergent uses \u2014 ask which uses, under what controls", "correct": True, "why": "Neither 'technology is neutral' nor 'ban everything' survives contact with the case; the serious question is always about specific uses and controls."},
     {"text": "It's neutral \u2014 tools have no moral character", "correct": False, "why": "Affordances shape use; a targeting-ready vision stack is not morally identical to a spreadsheet."},
     {"text": "Delete the repo immediately", "correct": False, "why": "Deletion also kills the conservation work and won't un-publish the forks \u2014 consequences matter too."}]},
   {"prompt": "What concrete step best fits the analysis?",
    "options": [
     {"text": "Keep the conservation core open; gate the targeting-enabling modules behind review, document foreseeable misuse, add a use policy", "correct": True, "why": "Differentiated controls: preserve the benign use, add friction to the harmful one, document the reasoning \u2014 the engineer's four moves."},
     {"text": "Do nothing \u2014 open source means no control", "correct": False, "why": "License terms, module structure, and documentation are all levers; 'no control' is false."},
     {"text": "Secretly sabotage the targeting forks", "correct": False, "why": "Deception violates professional duties and destroys the trust the conservation work depends on."}]}
  ]
 },
 {
  "id": "sc-writing-pressure", "title": "Writing Under Pressure",
  "context": "A Sev-1 outage just ended. You must write the incident review: it will be read by engineers, executives, and possibly a customer. The root cause implicates a shortcut your own team took.",
  "steps": [
   {"prompt": "How do you structure it?",
    "options": [
     {"text": "BLUF: impact and resolution first, then timeline, root cause (honest), action items with owners", "correct": True, "why": "Scanners get the essentials in paragraph one; the honest root cause preserves credibility; owned actions make it a tool, not a ritual."},
     {"text": "Chronological narrative from the first alert", "correct": False, "why": "Chronology buries the conclusion; busy readers never reach the decisions."},
     {"text": "Emphasize external factors to protect the team", "correct": False, "why": "Selective framing is manipulation; blameless review requires honest causation \u2014 blame the system, describe it truthfully."}]},
   {"prompt": "How do you phrase the team's shortcut?",
    "options": [
     {"text": "State it plainly with the reasoning at the time, then the systemic fix that removes the temptation", "correct": True, "why": "Honest, blameless, and forward-looking: it names the cause without personal attack and fixes the incentive."},
     {"text": "Omit it \u2014 the fix is what matters", "correct": False, "why": "Omitting known causation corrupts the record and guarantees recurrence."},
     {"text": "Name and shame the engineer who took it", "correct": False, "why": "Blame ends learning; the next shortcut will just be hidden better."}]}
  ]
 }
]

mock = []
qid = 0
for m in modules:
    for q in m["quiz"]:
        qid += 1
        if qid > 36: break
        mock.append({"id": f"mock-m21-{qid:02d}", "type": "choice",
                     "q": q["q"], "choices": q["choices"],
                     "answer": q["answer"], "explain": q["explain"]})
    if qid > 36: break

CHEAT_SHEETS = [
 {"title": "Argument & Fallacy Quick Reference",
  "blocks": [
   {"h": "Valid forms", "body": "- Modus ponens: P\u2192Q, P \u22a2 Q\n- Modus tollens: P\u2192Q, \u00acQ \u22a2 \u00acP\n- Valid = form; sound = valid + true premises"},
   {"h": "Fallacies", "body": "- Ad hominem, straw man, false dilemma, post hoc\n- Appeal to authority, begging the question, slippery slope\n- Name it, then give the substantive reply"},
   {"h": "Toulmin", "body": "- Claim, grounds, warrant, backing, qualifier, rebuttal\n- Fights are usually about warrants"}]},
 {"title": "Ethics Traditions at a Glance",
  "blocks": [
   {"h": "The three", "body": "- Virtue (Aristotle): what kind of person? Habits, character.\n- Deontology (Kant): duty; universalizable maxims; persons as ends.\n- Consequentialism (Bentham/Mill): maximize good outcomes."},
   {"h": "Applied moves", "body": "- Collingridge: design reversible, anticipatory, humble\n- Dual use: which uses, under what controls?\n- Document misuse, add friction, instrument, preserve override"}]},
 {"title": "Writing & Speaking Checklist",
  "blocks": [
   {"h": "Prose", "body": "- BLUF; headings; short paragraphs\n- Active voice, concrete subjects, numbers over adjectives\n- Define terms; cut 20% on second pass"},
   {"h": "Persuasion", "body": "- Ethos, pathos, logos (Aristotle)\n- Audience: values, knowledge, decision criteria\n- Persuasion respects agency; manipulation bypasses it"}]}
]

ANSWER_BANK = [
 {"q": "Argue for or against deploying a hiring model that is more accurate on average but disadvantages one group.", "a": "Framework: (1) Epistemology \u2014 what does 'accurate' mean on biased labels? (2) Deontology \u2014 does it treat applicants as ends? (3) Consequentialism \u2014 aggregate gains vs. concentrated harms, including second-order effects on the applicant pool. (4) Reversibility \u2014 can the decision be undone and monitored? A defensible answer works all four and lands on a constrained, monitored pilot or a no-go with reasons \u2014 never on the metric alone."},
 {"q": "Is open-sourcing a powerful model dual-use? What follows?", "a": "Framework: identify the mechanism's affordances for benign and harmful uses separately; assess how much the release *marginally* enables harm versus the status quo; consider controls (staged release, use policies, monitoring). 'Neutral' and 'ban it' are both evasions \u2014 the answer is always which uses under what controls, with the reasoning documented."},
 {"q": "Explain a technical trade-off to a non-technical executive.", "a": "Framework: stakes first (what changes for them), options with honest trade-offs, recommendation with reasons. One defined term per jargon item, or none. End with the decision you need from them and by when. Anticipate the values question ('is it fair/safe?') and answer it as a values question."},
 {"q": "A paper claims a breakthrough. How do you read it as an epistemologist?", "a": "Framework: Popper \u2014 what would falsify it? Kuhn \u2014 which paradigm does it extend or challenge? Replication \u2014 sample size, pre-registration, effect size with uncertainty, independent replication. Treat it as conjecture until the field converges; never cite the press release."},
 {"q": "Build vs. buy: make the economic case.", "a": "Framework: total cost of ownership over the realistic lifetime \u2014 license/fees + integration + operations + opportunity cost of diverted engineers + maintenance. Compare marginal costs at expected scale. Name the sunk-cost fallacy explicitly if past spend is invoked. Decide on forward-looking numbers."},
 {"q": "Your team is split on a rewrite. How do you decide?", "a": "Framework: Toulmin \u2014 surface the warrants ('rewrites always fail' vs. 'the debt is fatal'), not just the data. Economics \u2014 opportunity cost of the rewrite vs. incremental repair. History \u2014 second-system effect (Brooks) as a caution. Decide with a time-boxed spike that could falsify the rewrite case."}
]

SOURCE_LINKS = [
 {"name": "Stanford Encyclopedia \u2014 Classical Logic", "url": "https://plato.stanford.edu/entries/logic-classical/", "retrieved": "2026-10-07"},
 {"name": "Stanford Encyclopedia \u2014 Virtue Ethics", "url": "https://plato.stanford.edu/entries/ethics-virtue/", "retrieved": "2026-10-07"},
 {"name": "Stanford Encyclopedia \u2014 Kant's Moral Philosophy", "url": "https://plato.stanford.edu/entries/kant-moral/", "retrieved": "2026-10-07"},
 {"name": "Stanford Encyclopedia \u2014 Consequentialism", "url": "https://plato.stanford.edu/entries/consequentialism/", "retrieved": "2026-10-07"},
 {"name": "Stanford Encyclopedia \u2014 Karl Popper", "url": "https://plato.stanford.edu/entries/popper/", "retrieved": "2026-10-07"},
 {"name": "Stanford Encyclopedia \u2014 Thomas Kuhn", "url": "https://plato.stanford.edu/entries/thomas-kuhn/", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 History of science", "url": "https://en.wikipedia.org/wiki/History_of_science", "retrieved": "2026-10-07"},
 {"name": "ACM Code of Ethics and Professional Conduct", "url": "https://www.acm.org/code-of-ethics", "retrieved": "2026-10-07"}
]

doc = {
 "schemaVersion": "1.0",
 "courseId": "il-21-humanities",
 "code": "IL-21",
 "title": "Humanities for Technologists",
 "tagline": "Philosophy, history, writing, rhetoric, economics, and law \u2014 the disciplines of judgment for people who build.",
 "blurb": "Fourteen modules on the humanities as working disciplines: what philosophy is, logic and fallacies, three ethical traditions plus applied technology ethics, epistemology and philosophy of science, history of science and technology, technical writing, rhetoric, economics for engineers, law and policy literacy, and a synthesis on judgment. Discussion-framework answer bank, three ethical decision-tree scenarios, and quiz content drawn only from well-established facts \u2014 ideas attributed to their traditions, paraphrased, never fabricated. Original instructional content; confers no certificate.",
 "hours": 52,
 "updatedAt": "2026-10-07",
 "objectives": [
  "Reason with logic: validity, induction, abduction, and the classic fallacies",
  "Apply three ethical traditions \u2014 virtue, deontology, consequentialism \u2014 to technology dilemmas",
  "Evaluate knowledge claims with falsifiability, paradigms, and replication thinking",
  "Trace the history of science and technology from antiquity to the internet",
  "Write and speak with clarity: BLUF, active voice, Toulmin-structured argument",
  "Think economically: opportunity cost, incentives, externalities, game theory",
  "Read law and policy as a literate citizen, not a lawyer"
 ],
 "arc": [
  {"phase": "Phase 1 \u2014 Thinking", "title": "Reason well", "body": "What philosophy is, logic and argumentation, the three ethical traditions, applied technology ethics, epistemology and philosophy of science. Modules 1\u20135."},
  {"phase": "Phase 2 \u2014 Context", "title": "Know the story", "body": "History of science (antiquity to Newton, 1800 to present) and history of technology: how we got here and what recurs. Modules 6\u20138."},
  {"phase": "Phase 3 \u2014 Action", "title": "Communicate and decide", "body": "Technical writing, rhetoric, economics I\u2013II, law and policy, and the synthesis: judgment as the integration of every lens. Modules 9\u201314."}
 ],
 "priorities": [
  {"label": "Ethics I\u2013II + scenarios (modules 3\u20134)", "minutes": 420},
  {"label": "Logic + epistemology (modules 2, 5)", "minutes": 360},
  {"label": "History of science & technology (modules 6\u20138)", "minutes": 420},
  {"label": "Writing + rhetoric (modules 9\u201310)", "minutes": 360},
  {"label": "Economics I\u2013II + law (modules 11\u201313)", "minutes": 420},
  {"label": "Philosophy intro + synthesis (modules 1, 14) + mock", "minutes": 300}
 ],
 "battlePlan": [
  {"id": "bp21-1", "title": "Complete thinking block (modules 1\u20135): notes, cards, quizzes", "minutes": 480},
  {"id": "bp21-2", "title": "Complete history block (modules 6\u20138)", "minutes": 420},
  {"id": "bp21-3", "title": "Complete action block (modules 9\u201313)", "minutes": 480},
  {"id": "bp21-4", "title": "Work all three scenarios; write your own position using the answer-bank frameworks", "minutes": 240},
  {"id": "bp21-5", "title": "Complete synthesis module (14); draft one real memo using the writing checklist", "minutes": 180},
  {"id": "bp21-6", "title": "Sit the 36-task timed mock; review misses against the cheat sheets", "minutes": 150}
 ],
 "modules": modules,
 "scriptLabs": [],
 "drills": DRILLS,
 "scenarios": SCENARIOS,
 "trainers": [],
 "mockMinutes": 120,
 "mockTasks": mock,
 "cheatSheets": CHEAT_SHEETS,
 "answerBank": ANSWER_BANK,
 "sourceLinks": SOURCE_LINKS,
 "honestyNote": "Original instructional content; historical and philosophical claims are well-established facts attributed to their traditions \u2014 ideas are paraphrased, quotations are not fabricated. Not legal advice. Confers no certificate."
}

out = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-21-humanities.json"
with open(out, "w") as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", out, "modules:", len(modules), "mock:", len(mock))
