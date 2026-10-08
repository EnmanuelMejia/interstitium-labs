import json, glob, os

BASE = "/home/hatch/workspace/apex-audit/docs/university/data/courses/stories"

TAILS = {
"il-17-agentic-ai-engineering-story-2": " The society governs itself, or it doesn't govern at all.",
"il-17-agentic-ai-engineering-story-3": " Assume the adversary is already in the loop — then design accordingly.",
"il-19-multicloud-devops-ai-bootcamp-story-2": " Packaging is the breakthrough; the primitive was waiting thirty-four years for its user interface.",
"il-19-multicloud-devops-ai-bootcamp-story-3": " The console is for reading. The code is for building — and the plan is for thinking before you build.",
"il-20-mathematics-story-3": " Learn the rigor; honor the farm.",
"il-20-mathematics-story-5": " Same move, bigger bridges — learn it well.",
"il-21-humanities-story-2": " Normal science builds careers; revolutions make them. Learn to tell which phase you're in.",
"il-21-humanities-story-4": " Clarity is the achievement; jargon is the hiding place.",
"il-22-esoteric-secret-knowledge-story-4": " The fiction organized the seekers; study the organizing.",
"il-23-frontier-knowledge-story-4": " Read the landscape as data, not destiny.",
"il-24-threatlocker-assessment-prep-cbt-story-2": " Observe, baseline, enforce, contain — the 1975 principles, operationalized for your triage shift.",
"il-24-threatlocker-assessment-prep-cbt-story-3": " Grammar, map, vocabulary — learn all three, and you'll read any intrusion.",
"il-24-threatlocker-assessment-prep-cbt-story-4": " Update against the base rate, correctly, every time — that's the whole discipline.",
"il-25-cybersecurity-professional-certificate-story-2": " Trust the contest, not the cipher alone.",
"il-25-cybersecurity-professional-certificate-story-3": " Air gaps delay; they don't defend. Plan accordingly.",
"il-26-data-analyst-certification-senior-mastery-story-1": " Bars for comparison, lines for time — Playfair's grammar, still spoken.",
"il-26-data-analyst-certification-senior-mastery-story-3": " Fit the model; never let it do the moral reasoning.",
"il-26-data-analyst-certification-senior-mastery-story-4": " Small samples, honest math — the brewer's discipline.",
"il-27-it-infrastructure-specialist-threatlocker-mastery-story-2": " The 1983 protocol, still resolving, still under attack — learn it cold.",
"il-27-it-infrastructure-specialist-threatlocker-mastery-story-3": " Replace luck with design: offline, immutable, rehearsed.",
"il-27-it-infrastructure-specialist-threatlocker-mastery-story-4": " Virtualize boldly; understand the layer you're standing on.",
"il-28-devsecops-cloud-infrastructure-mastery-story-1": " The wire is hostile; prove the endpoints, every session.",
"il-28-devsecops-cloud-infrastructure-mastery-story-2": " The package is easy; the hardening is the product.",
"il-28-devsecops-cloud-infrastructure-mastery-story-3": " Scan on commit, inventory always, patch fast — the shift-left liturgy that would have caught it.",
"il-28-devsecops-cloud-infrastructure-mastery-story-4": " What made SolarWinds historic wasn't just the technique but the patience: the operators chose targets carefully, moved slowly, and stayed quiet for months — the opposite of smash-and-grab crime. The industry's answer has been to treat the software supply chain as critical infrastructure: attestations, provenance, reproducible builds. In this module you'll implement the defenses as daily practice, not theory — because the next trojanized update is already being planned somewhere, and your pipeline is someone's target.",
"il-29-threatlocker-ai-cybersecurity-mastery-story-1": " Learn the attack to build the defense — that's the 6.858 way.",
"il-29-threatlocker-ai-cybersecurity-mastery-story-2": " Audit the implementation, fund the infrastructure.",
"il-29-threatlocker-ai-cybersecurity-mastery-story-3": " The eviction notice was polite — twelve years of warning — and the industry still barely moved in time. In your work, schedule the migration before the break: crypto agility isn't a feature, it's the plan.",
"il-29-threatlocker-ai-cybersecurity-mastery-story-4": " See the behavior, name the technique, deploy the detection — until it's reflexive.",
}

ID_FIXES = {
    "il-28-devsecops-cloud-security-interview-prep-story-4": "il-28-devsecops-cloud-infrastructure-mastery-story-4",
}

# apply id fixes first (rename keys in TAILS accordingly already done above)
for f in sorted(glob.glob(os.path.join(BASE, "il-*.json"))):
    if f.endswith("_index.json"):
        continue
    d = json.load(open(f))
    changed = False
    for s in d["stories"]:
        if s["id"] in ID_FIXES:
            s["id"] = ID_FIXES[s["id"]]
            changed = True
        tail = TAILS.get(s["id"])
        if tail:
            s["narrative"] = s["narrative"].rstrip() + tail
            changed = True
    if changed:
        json.dump(d, open(f, "w"), ensure_ascii=False, indent=1)

bad = []
total = 0
for f in sorted(glob.glob(os.path.join(BASE, "il-*.json"))):
    if f.endswith("_index.json"):
        continue
    slug = os.path.basename(f).replace("-stories.json", "")
    d = json.load(open(f))
    for i, s in enumerate(d["stories"], 1):
        total += 1
        w = len(s["narrative"].split())
        if not (300 <= w <= 600):
            bad.append((s["id"], w))
print("still out of range:", bad if bad else "none", "| total:", total)
