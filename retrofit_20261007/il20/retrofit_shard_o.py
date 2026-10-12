#!/usr/bin/env python3
"""Retrofit il20/il21/il22 path entries in catalog/shard-o.json.

Adds per path: topics (string list), sources [{name,url,note}] (URLs already in
the repo only), il_provides (2-3 sentence instructor-voice blurb).
SKIPS il23-* paths entirely (sibling agent owns them).
Fresh json.load at write time; atomic write (temp + os.replace); re-validate.
"""
import json, os, sys

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/catalog')
PATH = os.path.join(BASE, 'shard-o.json')

ILU = "https://interstitiumlabs.dev/university/"
ISTA = "https://www.sacred-texts.com/"

NEW = {
 "il20-discrete-foundations": {
  "topics": [
   "Sets, operations, and the power set",
   "Propositions, connectives, and truth tables",
   "Quantifiers and necessary vs sufficient conditions",
   "Direct proof, contrapositive, contradiction, and induction",
   "Permutations, combinations, and the binomial theorem",
   "The pigeonhole principle",
   "Functions: injective, surjective, bijective",
   "Equivalence relations and partitions",
  ],
  "sources": [
   {"name": "Wikipedia — Mathematical proof", "url": "https://en.wikipedia.org/wiki/Mathematical_proof",
    "note": "Reference for the proof methods and logical structure used across the discrete modules."},
   {"name": "Interstitium Labs University", "url": ILU,
    "note": "Course home for the full IL-20 module sequence: notes, cards, quizzes, and labs."},
  ],
  "il_provides": (
   "The language mathematics is written in: sets and logic, the four proof moves, and counting "
   "done right. I teach discrete foundations as a working skill — truth tables you check by hand, "
   "induction proofs you carry out yourself, and combinatorics you apply to real systems — because "
   "every later module in this course assumes you read and write this language fluently."
  ),
 },
 "il20-algebra-calculus-core": {
  "topics": [
   "Vectors, dot products, and projections",
   "Vector spaces, span, bases, and dimension",
   "Matrix multiplication, determinants, inverses, and rank",
   "Eigenvalues, eigenvectors, and diagonalization",
   "Limits, continuity, and the derivative",
   "Product, quotient, and chain rules",
   "The Fundamental Theorem of Calculus",
   "Integration by parts and improper integrals",
   "Taylor series and convergence tests",
   "Gradients, critical points, and Lagrange multipliers",
  ],
  "sources": [
   {"name": "Wikipedia — Linear algebra", "url": "https://en.wikipedia.org/wiki/Linear_algebra",
    "note": "Reference for the vector/matrix/eigenvalue material in the algebra half of this path."},
   {"name": "Wikipedia — Calculus", "url": "https://en.wikipedia.org/wiki/Calculus",
    "note": "Reference for the limits/derivatives/integrals/series material in the calculus half."},
   {"name": "MIT OpenCourseWare — Linear Algebra (Strang)", "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
    "note": "Classic lecture sequence aligned with the matrix and eigenvalue modules."},
  ],
  "il_provides": (
   "The continuous machinery: linear algebra and calculus taught as one engine. I walk you from "
   "vectors and matrices through eigenvalues, then from limits through multivariable optimization — "
   "every rule paired with a worked procedure you verify yourself — so the mathematics of change "
   "and structure becomes a tool you reach for, not a wall you hit."
  ),
 },
 "il20-probability-computation": {
  "topics": [
   "Probability axioms, conditioning, and Bayes' theorem",
   "Random variables, expectation, and variance",
   "The Central Limit Theorem and confidence intervals",
   "Hypothesis testing and p-values",
   "Bisection and Newton's method",
   "Trapezoidal and Simpson quadrature",
   "Gaussian elimination and LU factorization",
   "Least squares and gradient descent",
  ],
  "sources": [
   {"name": "Wikipedia — Probability theory", "url": "https://en.wikipedia.org/wiki/Probability_theory",
    "note": "Reference for the probability and statistics modules in this path."},
   {"name": "Wikipedia — Numerical analysis", "url": "https://en.wikipedia.org/wiki/Numerical_analysis",
    "note": "Reference for the root-finding, quadrature, and linear-system methods."},
   {"name": "NumPy documentation", "url": "https://numpy.org/doc/",
    "note": "Reference for the executable labs: matrix ops, Monte Carlo, gradient descent, quadrature."},
  ],
  "il_provides": (
   "Decision-making under uncertainty, and computation when closed forms fail. I teach probability "
   "honestly — base rates first, p-values read correctly — and numerical methods with error bounds "
   "you compute before you trust an answer. The capstone skills: a Bayes update you can defend, "
   "and a root-finder you can guarantee."
  ),
 },
 "il21-philosophy-ethics": {
  "topics": [
   "What philosophy is and how it is done",
   "Logic, arguments, and common fallacies",
   "Virtue ethics, deontology, and consequentialism",
   "Applied technology ethics and the ACM code",
  ],
  "sources": [
   {"name": "Stanford Encyclopedia — Classical Logic", "url": "https://plato.stanford.edu/entries/logic-classical/",
    "note": "Reference for the logic and argument material in this path."},
   {"name": "Stanford Encyclopedia — Virtue Ethics", "url": "https://plato.stanford.edu/entries/ethics-virtue/",
    "note": "Reference for one of the three ethical traditions taught here."},
   {"name": "ACM Code of Ethics and Professional Conduct", "url": "https://www.acm.org/code-of-ethics",
    "note": "The professional-ethics frame for the applied technology ethics modules."},
  ],
  "il_provides": (
   "The disciplines of judgment: how to argue well and how to decide well. I teach the three "
   "ethical traditions as working tools — not museum pieces — so that when a deployment decision "
   "lands on your desk, you have a framework for it, not just an opinion."
  ),
 },
 "il21-history-science-tech": {
  "topics": [
   "Science from antiquity to the scientific revolution",
   "The industrial revolutions",
   "Computing and the internet revolutions",
   "Epistemology and the replication crisis",
  ],
  "sources": [
   {"name": "Wikipedia — History of science", "url": "https://en.wikipedia.org/wiki/History_of_science",
    "note": "Reference timeline for the history-of-science modules in this path."},
   {"name": "Stanford Encyclopedia — Karl Popper", "url": "https://plato.stanford.edu/entries/popper/",
    "note": "Reference for falsifiability and the epistemology material."},
   {"name": "Stanford Encyclopedia — Thomas Kuhn", "url": "https://plato.stanford.edu/entries/thomas-kuhn/",
    "note": "Reference for paradigm shifts across the scientific revolutions covered here."},
  ],
  "il_provides": (
   "How we got here: the long arc from ancient natural philosophy to the internet age. I teach "
   "the history of science and technology as a pattern library — revolutions rhyme — paired with "
   "epistemology's hard questions about what counts as knowing, so you build on firmer ground."
  ),
 },
 "il21-writing-economics-law": {
  "topics": [
   "Technical writing for engineers",
   "Rhetoric and persuasion",
   "Economics for engineers",
   "Law and policy literacy",
  ],
  "sources": [
   {"name": "ACM Code of Ethics and Professional Conduct", "url": "https://www.acm.org/code-of-ethics",
    "note": "Professional-conduct frame referenced by the policy-literacy material in this path."},
   {"name": "Stanford Encyclopedia — Consequentialism", "url": "https://plato.stanford.edu/entries/consequentialism/",
    "note": "Reference for the cost-benefit reasoning behind the economics-for-engineers modules."},
  ],
  "il_provides": (
   "The skills that turn technical work into impact: writing that explains, arguments that persuade, "
   "economics that prices trade-offs, and enough law to read the rules that govern your work. I "
   "teach these as working disciplines — every module ends with something you produce, not just "
   "something you know."
  ),
 },
 "il22-western-mystery-traditions": {
  "topics": [
   "Kabbalah and the Tree of Life",
   "Hermeticism and the Corpus Hermeticum",
   "Alchemy: exoteric craft and esoteric allegory",
   "Rosicrucianism",
  ],
  "sources": [
   {"name": "Wikipedia — Kabbalah", "url": "https://en.wikipedia.org/wiki/Kabbalah",
    "note": "Reference overview for the Kabbalah module in this path."},
   {"name": "Wikipedia — Hermeticism", "url": "https://en.wikipedia.org/wiki/Hermeticism",
    "note": "Reference overview for the Hermeticism module."},
   {"name": "Wikipedia — Alchemy", "url": "https://en.wikipedia.org/wiki/Alchemy",
    "note": "Reference overview for the alchemy module."},
   {"name": "Internet Sacred Text Archive", "url": ISTA,
    "note": "Primary-source archive for the traditional texts studied across this path."},
  ],
  "il_provides": (
   "The great symbolic systems of the Western mystery traditions, studied as traditions — "
   "scholarly and descriptive, never credulous. I present Kabbalah, Hermeticism, alchemy, and "
   "Rosicrucianism the way their practitioners understood them, with the historical and textual "
   "context that keeps the study honest."
  ),
 },
 "il22-divination-practices": {
  "topics": [
   "Astrology as a symbolic grammar",
   "Tarot: structure and reading methods",
   "The I Ching",
   "Runes and geomancy",
  ],
  "sources": [
   {"name": "Wikipedia — Astrology", "url": "https://en.wikipedia.org/wiki/Astrology",
    "note": "Reference overview for the astrology module in this path."},
   {"name": "Wikipedia — Tarot", "url": "https://en.wikipedia.org/wiki/Tarot",
    "note": "Reference overview for the tarot module."},
   {"name": "Internet Sacred Text Archive", "url": ISTA,
    "note": "Primary-source archive for traditional divinatory texts referenced in this path."},
  ],
  "il_provides": (
   "Divinatory systems read as symbolic instruments, not as verified science. I teach astrology, "
   "tarot, the I Ching, runes, and geomancy as grammars of meaning — what each system claims and "
   "how its symbols combine — while keeping the scholarly frame: knowledge of the traditions, "
   "never endorsement of their claims."
  ),
 },
 "il22-orders-modern-occultism": {
  "topics": [
   "Enochian magic",
   "Theosophy",
   "The Hermetic Order of the Golden Dawn",
   "Grimoires and Gnosticism",
   "The modern occult revival",
  ],
  "sources": [
   {"name": "Wikipedia — Enochian magic", "url": "https://en.wikipedia.org/wiki/Enochian_magic",
    "note": "Reference overview for the Enochian magic module."},
   {"name": "Wikipedia — Theosophy", "url": "https://en.wikipedia.org/wiki/Theosophy",
    "note": "Reference overview for the Theosophy module."},
   {"name": "Wikipedia — Hermetic Order of the Golden Dawn", "url": "https://en.wikipedia.org/wiki/Hermetic_Order_of_the_Golden_Dawn",
    "note": "Reference overview for the Golden Dawn module."},
   {"name": "Internet Sacred Text Archive", "url": ISTA,
    "note": "Primary-source archive for grimoire and esoteric texts studied in this path."},
  ],
  "il_provides": (
   "The orders and movements that shaped modern occultism, from Enochian magic through Theosophy "
   "and the Golden Dawn to the grimoire tradition and the contemporary revival. I keep the same "
   "contract throughout: the traditions presented as they present themselves, with sources you can "
   "check and history you can verify."
  ),
 },
}

def main():
    with open(PATH, encoding='utf-8') as f:
        before = json.load(f)

    sib_before = None
    for p in before["paths"]:
        if p["id"] == "il23-ai-frontier":
            sib_before = len(p.get("modules", []))
    if not sib_before or sib_before <= 0:
        print("SIBLING MARKER NOT FOUND (il23-ai-frontier has no modules) — aborting per task.")
        sys.exit(2)
    print(f"sibling marker present: il23-ai-frontier has {sib_before} modules; proceeding.")

    data = before  # fresh load above; apply edits now, write immediately
    touched = []
    for p in data["paths"]:
        pid = p["id"]
        if pid in NEW:
            p["topics"] = NEW[pid]["topics"]
            p["sources"] = NEW[pid]["sources"]
            p["il_provides"] = NEW[pid]["il_provides"]
            touched.append(pid)
        elif pid.startswith("il23-"):
            pass  # sibling-owned; never touch
    assert len(touched) == 9, f"expected 9 paths, touched {touched}"

    # validate every one of my 9 paths
    for p in data["paths"]:
        if p["id"] in NEW:
            assert isinstance(p["topics"], list) and all(isinstance(t, str) for t in p["topics"])
            assert isinstance(p["sources"], list) and all(
                set(s.keys()) == {"name", "url", "note"} for s in p["sources"])
            assert isinstance(p["il_provides"], str) and len(p["il_provides"]) > 50

    tmp = PATH + ".retrofit-tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, PATH)

    with open(PATH, encoding="utf-8") as f:
        check = json.load(f)
    sib_after = None
    for p in check["paths"]:
        if p["id"] == "il23-ai-frontier":
            sib_after = p.get("modules", [])
    assert sib_after and len(sib_after) >= sib_before, "sibling il23 modules lost!"
    assert [p["id"] for p in check["paths"]] == [p["id"] for p in before["paths"]], "path order/ids changed"
    print(f"OK: retrofitted {len(touched)} paths; sibling il23-ai-frontier intact with {len(sib_after)} modules.")

if __name__ == "__main__":
    main()
