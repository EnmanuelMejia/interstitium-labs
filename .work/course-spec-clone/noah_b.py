#!/usr/bin/env python3
"""Add structured `noahTutoring` sections to Group B courses (IL-07..IL-12).

Noah AI is the core learning-experience driver: 5 personas, 5 natural voices,
SM-2 adaptive learning, course-aware tutoring, voice-first chat, and
daily-fold bleeding-edge integration where relevant (IL-11 cybersecurity,
IL-12 AI agents; IL-07 frontier AI lightly).
"""
import json, os

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses/'
FILES = {
 "IL-07": "il-07-data-engineering-analytics-ai.json",
 "IL-08": "il-08-algorithms-compilers-distributed-formal.json",
 "IL-09": "il-09-adaptive-certification-command.json",
 "IL-10": "il-10-portfolio-career-professional-practice.json",
 "IL-11": "il-11-zero-trust-endpoint-defense.json",
 "IL-12": "il-12-ai-engineering.json",
}

VOICES = ("Five natural voices — one distinct voice per persona, switchable at any time. "
          "Voice chat runs alongside the module so learners can talk with Noah mid-lab "
          "without breaking flow.")
ADAPTIVE = ("SM-2 spaced repetition drives Noah's memory of the learner: every flashcard, "
            "quiz answer, and drill result feeds an SM-2 scheduler that re-surfaces weak items "
            "at the optimal interval. Noah adapts explanations to the learner's level and "
            "re-routes the study plan toward the weakest published exam domains or skill gaps.")
COURSE_AWARE = ("Noah is course-aware: it knows this course's modules, the learner's progress, "
                "the certification gates, and the cross-linked companion courses. It answers from "
                "the course's own material first, cites module IDs, and routes deeper questions "
                "to the right module or companion course.")

def persona(pid, name, role, modules, voice_note="Speaks in its own distinct natural voice."):
    return {"id": pid, "name": name, "role": role, "voice": voice_note, "modules": modules}

# ---------------------------------------------------------------- per-course
P07 = [
 persona("visionary", "The Visionary",
   "Paints the end-state: where the data platform and the AI system are going, and why this module matters on that arc.",
   ["il07-ai-ml", "il07-openweight", "il07-agents", "il07-frontier", "il07-aws-ml"]),
 persona("engineer", "The Engineer",
   "Pairs with you on labs: pipelines, dbt models, aggregation queries, and cloud builds — reviews your code and finds the bug.",
   ["il07-mongodb", "il07-data-schools", "il07-aws-data", "il07-aws-ml"]),
 persona("philosopher", "The Philosopher",
   "Goes deep on the why: the math behind the model, what a probability statement means, how brains inspired the architectures.",
   ["il-07-data-engineering-analytics-ai-math-stats",
    "il-07-data-engineering-analytics-ai-math-linalg",
    "il07-neuroai", "il07-frontier"]),
 persona("mentor", "The Mentor",
   "Runs review and readiness: Socratic check-ins, gate prep, study scheduling, and honest feedback on weak spots.",
   ["il07-data-schools", "il07-ai-ml"]),
 persona("trickster", "The Trickster",
   "Plants the traps so the exam can't: leaky features, silent data-quality failures, quiz distractors that punish shallow reading.",
   ["il07-mongodb", "il07-data-schools", "il07-ai-ml"]),
]
BE07 = {"source": "daily-fold trending pipeline",
        "note": "The frontier AI module (il07-frontier) is fed by the daily-fold trend pipeline: "
                "Noah surfaces fresh model releases, licensing changes, and architecture shifts "
                "as they happen, and ties them back to the module's concepts."}

P08 = [
 persona("visionary", "The Visionary",
   "Shows where the theory lands: how today's distributed systems and compilers are the theorems made real.",
   ["il08-cmu-cs", "il08-stanford-cs"]),
 persona("engineer", "The Engineer",
   "Proof-to-code partner: turns your recurrence into a timed implementation and hunts the off-by-one.",
   ["il08-mit-63", "il08-cmu-cs"]),
 persona("philosopher", "The Philosopher",
   "The home persona for this course: induction, invariants, complexity classes — why the proof is the program.",
   ["il-08-algorithms-compilers-distributed-formal-math-discrete",
    "il-08-algorithms-compilers-distributed-formal-math-logic",
    "il08-mit-63", "il08-stanford-cs"]),
 persona("mentor", "The Mentor",
   "Socratic proof review: asks for the invariant before the code, and schedules the hard proofs via SM-2.",
   ["il08-mit-63", "il08-cmu-cs", "il08-stanford-cs"]),
 persona("trickster", "The Trickster",
   "Edge-case assassin: the adversarial input, the exponential blowup, the reduction that almost works.",
   ["il08-mit-63", "il08-cmu-cs"]),
]
BE08 = {"source": None,
        "note": "Foundational course — Noah teaches from first principles; trending integration is not wired here by design."}

P09 = [
 persona("visionary", "The Visionary",
   "Maps the credential campaign to the career: which certs stack, in what order, and what each unlocks.",
   ["il09-comptia-core", "il09-vendor-ai"]),
 persona("engineer", "The Engineer",
   "PBQ and lab partner: walks through performance-based scenarios step by step until the workflow is automatic.",
   ["il09-comptia-core", "il09-comptia-security", "il09-comptia-data-cloud", "il09-oracle"]),
 persona("philosopher", "The Philosopher",
   "The concepts under the exam: why the networking model works, what the crypto actually proves.",
   ["il-09-adaptive-certification-command-math-binmath",
    "il-09-adaptive-certification-command-math-logic",
    "il09-comptia-core", "il09-comptia-security"]),
 persona("mentor", "The Mentor",
   "The command-deck driver: schedules study from your weakest domains, runs timed gates, and tells you honestly when to book.",
   ["il09-comptia-core", "il09-comptia-security", "il09-comptia-data-cloud",
    "il09-vendor-ai", "il09-oracle", "il09-lf-blockchain", "il09-cpp-python"]),
 persona("trickster", "The Trickster",
   "Exam-trap trainer: the 'two right answers' question, the PBQ misdirection, the version-change gotcha.",
   ["il09-comptia-core", "il09-comptia-security"]),
]
BE09 = {"source": None,
        "note": "Noah tracks published exam-objective changes and version retirements, and steers "
                "study away from retired content — always verify against the vendor's current page before booking."}

P10 = [
 persona("visionary", "The Visionary",
   "The venture and quant-ladder coach: sees the 5-year arc and works backward to this week's build.",
   ["il10-entrepreneurship", "il10-quant-finance"]),
 persona("engineer", "The Engineer",
   "Portfolio builder: reviews the shipped artifact, the repo, the dashboard — line by line.",
   ["il10-fde-career", "il10-quant-finance"]),
 persona("philosopher", "The Philosopher",
   "Self-knowledge work: typology as data, decision frameworks, knowing what game you're actually playing.",
   ["il10-humanmetrics",
    "il-10-portfolio-career-professional-practice-math-quantreason"]),
 persona("mentor", "The Mentor",
   "Career-arc driver: interview systems, behavioral narratives, offer evaluation — with honest feedback.",
   ["il10-fde-career", "il10-humanmetrics"]),
 persona("trickster", "The Trickster",
   "Behavioral-interview curveballs and offer-negotiation traps: the questions designed to rattle you.",
   ["il10-fde-career"]),
]
BE10 = {"source": None,
        "note": "Professional-practice course — Noah coaches from the learner's own history and "
                "the course's frameworks, not from trend feeds."}

P11 = [
 persona("visionary", "The Visionary",
   "The maturity-model view: where your defense program sits on the CISA model and the path to Optimal.",
   ["il11-zero-trust-foundations--zt-cisa-maturity",
    "il11-zero-trust-foundations--zt-nist-tenets"]),
 persona("engineer", "The Engineer",
   "Lab partner for the operator work: allowlist policies, ringfence profiles, KQL hunts, PowerShell troubleshooting.",
   ["il11-allowlisting-ringfencing--zt-allowlist",
    "il11-allowlisting-ringfencing--zt-ringfence",
    "il11-allowlisting-ringfencing--zt-storage-elevation",
    "il11-entra-identity--sc300-troubleshoot"]),
 persona("philosopher", "The Philosopher",
   "The doctrine: why 'never trust, always verify' follows from assume-breach, and what the math proves.",
   ["il11-zero-trust-foundations--zt-perimeter-fall",
    "il11-zero-trust-foundations--zt-nist-tenets",
    "il-11-zero-trust-endpoint-defense-math-numtheory",
    "il-11-zero-trust-endpoint-defense-math-logic",
    "il11-network-crypto-foundations--zt-encryption"]),
 persona("mentor", "The Mentor",
   "Review and readiness: Socratic check-ins, the hero-review gate, SC-300 exam prep, honest readiness calls.",
   ["il11-cyber-hero-prep--zt-hero-review",
    "il11-cyber-hero-prep--zt-hero-scenarios",
    "il11-entra-identity--sc300-exam-prep"]),
 persona("trickster", "The Trickster",
   "Red-team mind: runs the phishing scenario, the AD attack path, the 'vendor says Zero Trust' trap — so attackers can't surprise you.",
   ["il11-red-blue-operations--zt-social-engineering",
    "il11-red-blue-operations--zt-web-attacks",
    "il11-red-blue-operations--zt-blue-detect",
    "il11-active-directory-defense--zt-ad-attacks"]),
]
BE11 = {"source": "daily-fold trending pipeline",
        "note": "Bleeding-edge integration: the daily-fold trend pipeline feeds Noah fresh "
                "threat-intel, vulnerability, and attack-technique developments. Noah weaves them "
                "into the red/blue modules and the Cyber Hero scenarios as living examples — "
                "tied back to the module concepts, never as unvetted claims."}

P12 = [
 persona("visionary", "The Visionary",
   "The frontier view: agents, autonomy ceilings, edge AI — where the field is going and what to build for it.",
   ["aieng-agentic-ai--agent-architectures",
    "aieng-agentic-ai--agent-autonomy-ceilings",
    "aieng-production--edge-ondevice-ai",
    "aieng-generative-ai--multimodal-foundation-models"]),
 persona("engineer", "The Engineer",
   "Build partner: PyTorch training loops, RAG pipelines, serving configs, eval harnesses — reviews your diffs.",
   ["aieng-deep-learning--pytorch-workflows",
    "aieng-generative-ai--llm-apis-rag",
    "aieng-generative-ai--vecdb-depth",
    "aieng-production--prod-serving",
    "aieng-production--prod-pipelines",
    "aieng-capstone--capstone-build"]),
 persona("philosopher", "The Philosopher",
   "First principles: why attention works, what alignment means, the math the models stand on.",
   ["il-12-ai-engineering-math-linalg",
    "il-12-ai-engineering-math-stats",
    "il-12-ai-engineering-math-discrete",
    "aieng-generative-ai--transformers-attention",
    "aieng-generative-ai--llm-alignment-rlhf-dpo",
    "aieng-deep-learning--backprop-optimization"]),
 persona("mentor", "The Mentor",
   "Capstone and readiness coach: evaluation discipline, model cards, responsible-AI review, gate prep.",
   ["aieng-capstone--capstone-framing",
    "aieng-capstone--capstone-eval",
    "aieng-capstone--capstone-rai",
    "aieng-capstone--capstone-portfolio",
    "aieng-production--prod-red-team"]),
 persona("trickster", "The Trickster",
   "Adversarial mind: plants the data leak, the prompt injection, the eval that passes and lies — so production can't fool you.",
   ["aieng-data-science--statistics-for-ml",
    "aieng-machine-learning--validation-tuning",
    "aieng-machine-learning--evaluation-metrics",
    "aieng-production--prod-red-team",
    "aieng-production--trajectory-eval-agents",
    "aieng-agentic-ai--context-engineering"]),
]
BE12 = {"source": "daily-fold trending pipeline",
        "note": "Bleeding-edge integration: the daily-fold trend pipeline feeds Noah fresh AI-agent "
                "developments — new agent frameworks, protocol changes (MCP and successors), eval "
                "results, and serving breakthroughs. Noah weaves them into the agentic, generative-AI, "
                "and production modules as living examples tied back to module concepts."}

CONFIG = {
 "IL-07": {"personas": P07, "bleedingEdge": BE07,
            "concept": "Noah is the tutoring driver for the data-to-model journey: it teaches the "
                       "math, pairs on the pipelines, and stress-tests your ML reasoning — by voice, "
                       "adaptively, and always grounded in this course's modules."},
 "IL-08": {"personas": P08, "bleedingEdge": BE08,
            "concept": "Noah is the tutoring driver for the deep core: a philosopher-first tutor that "
                       "demands the proof before the code, an engineer that times your implementation, "
                       "and a trickster that hunts your edge cases."},
 "IL-09": {"personas": P09, "bleedingEdge": BE09,
            "concept": "Noah runs the certification command deck: it schedules from your weakest "
                       "domains, drills PBQs with the Engineer, traps you with the Trickster, and the "
                       "Mentor tells you honestly when you're ready to book."},
 "IL-10": {"personas": P10, "bleedingEdge": BE10,
            "concept": "Noah is the career co-pilot: the Mentor runs your interview systems, the "
                       "Visionary works backward from the 5-year arc, and the Trickster throws the "
                       "curveballs before a real interviewer does."},
 "IL-11": {"personas": P11, "bleedingEdge": BE11,
            "concept": "Noah is the tutoring driver for the defender's discipline: doctrine from the "
                       "Philosopher, operator labs with the Engineer, red-team pressure from the "
                       "Trickster — with live threat developments woven in from the trend pipeline."},
 "IL-12": {"personas": P12, "bleedingEdge": BE12,
            "concept": "Noah is the tutoring driver for the AI-engineer spine: theory from the "
                       "Philosopher, builds with the Engineer, adversarial evals from the Trickster — "
                       "with fresh agent developments woven in from the trend pipeline."},
}

def build_noah(code):
    cfg = CONFIG[code]
    return {
        "enabled": True,
        "concept": cfg["concept"],
        "personas": cfg["personas"],
        "voices": {"count": 5, "description": VOICES,
                   "voiceFirst": "Learners talk with Noah via voice chat while working through "
                                 "modules — ask mid-lab, get answers without breaking flow."},
        "adaptive": {"method": "SM-2 spaced repetition", "description": ADAPTIVE},
        "courseAware": {"description": COURSE_AWARE},
        "bleedingEdge": cfg["bleedingEdge"],
        "rule": ("Noah teaches from this course's material and its cross-linked companions; "
                 "it never invents credentials, exam content, or vendor claims."),
    }

def main():
    for code, fn in FILES.items():
        path = BASE + fn
        d = json.load(open(path))
        d["noahTutoring"] = build_noah(code)
        # validate persona module ids
        mids = {m["id"] for m in d["modules"]}
        bad = []
        for p in d["noahTutoring"]["personas"]:
            for mid in p["modules"]:
                if mid not in mids:
                    bad.append((p["id"], mid))
        assert not bad, (code, bad)
        assert len(d["noahTutoring"]["personas"]) == 5, code
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        json.load(open(tmp))
        os.replace(tmp, path)
        print(code, "noahTutoring added; persona module refs valid")

if __name__ == "__main__":
    main()
