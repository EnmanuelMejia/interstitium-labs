# Part 2 — IL-20 M00 + sections, IL-21, IL-22, IL-23 sections

IL20_M00 = {
    "id": "IL-20-M00",
    "code": "IL-20",
    "title": "M00 · Mathematical Maturity Primer — Readiness for IL-20",
    "summary": ("A readiness module drawn from IL-02 (Mathematical Maturity Engine): propositional logic, "
                "truth tables, proof methods, and the study habits that make IL-20 work. Take this first — "
                "it tells you honestly whether you are ready for the full treatment, and fills the gaps if not."),
    "objectives": [
        "Evaluate compound propositions and build truth tables from memory.",
        "Apply De Morgan's laws and distinguish implication, converse, and contrapositive.",
        "Outline the four proof methods (direct, contrapositive, contradiction, induction) and name when each fits.",
        "Verify logical equivalences by brute-force enumeration in Python.",
        "Self-assess readiness for IL-20's calculus and linear-algebra modules and name your remediation plan.",
    ],
    "estimatedMinutes": 300,
    "weight": 0.05,
    "prerequisiteFor": ["m20-sets-logic"],
    "crossLinks": ["m20-sets-logic", "m20-proof-methods",
                   "il-02-mathematical-maturity-engine-math-logic",
                   "il-02-mathematical-maturity-engine-math-stats"],
    "cards": [
        {"front": "How many rows in a truth table with 4 variables?", "back": "2^4 = 16 rows — one per assignment."},
        {"front": "State De Morgan's law for AND.", "back": "NOT (p AND q) = (NOT p) OR (NOT q)."},
        {"front": "State De Morgan's law for OR.", "back": "NOT (p OR q) = (NOT p) AND (NOT q)."},
        {"front": "Which are equivalent to p → q: converse, contrapositive, inverse?", "back": "Only the contrapositive (¬q → ¬p). Converse and inverse are not equivalent."},
        {"front": "Name the four standard proof methods.", "back": "Direct, contrapositive, contradiction, induction."},
        {"front": "When is proof by contradiction the right tool?", "back": "When assuming the negation gives you something concrete to push to an absurdity (e.g., irrationality proofs)."},
        {"front": "What does the induction step require?", "back": "Base case P(n0) proven, then P(k) → P(k+1) for arbitrary k ≥ n0."},
        {"front": "Why verify logic by brute force in Python?", "back": "Exhaustive enumeration settles every row — the machine checks what your hand might miss."},
    ],
    "quiz": [
        {"q": "A truth table for (p ∧ q) → r has how many rows?", "choices": ["6", "8", "4", "16"], "answer": 1,
         "explain": "Three variables → 2^3 = 8 rows."},
        {"q": "Which is logically equivalent to 'If the server is patched, then it is compliant'?",
         "choices": ["If the server is compliant, then it is patched", "If the server is not compliant, then it is not patched",
                     "If the server is not patched, then it is not compliant", "Patching causes compliance"],
         "answer": 1, "explain": "The contrapositive (¬q → ¬p) is the only equivalent restatement."},
        {"q": "De Morgan's law: ¬(p ∨ q) equals…", "choices": ["¬p ∨ ¬q", "¬p ∧ ¬q", "p ∧ q", "p → q"], "answer": 1,
         "explain": "NOT (p OR q) = (NOT p) AND (NOT q)."},
        {"q": "To prove 'for all n, P(n)' by induction you must show…",
         "choices": ["P(1) only", "P(k) → P(k+1) only", "P(n0) and P(k) → P(k+1)", "P(n) for n up to 100"],
         "answer": 2, "explain": "Base case plus the inductive step — both, or the proof is incomplete."},
        {"q": "Proof by contradiction starts by assuming…", "choices": ["The statement is true", "The negation of the statement",
         "A counterexample exists", "Nothing"], "answer": 1, "explain": "Assume ¬P, derive an absurdity, conclude P."},
        {"q": "Which study habit does IL-20 demand most?",
         "choices": ["Re-reading notes", "Working problems with pencil and paper before checking solutions",
                     "Watching lectures at 2x speed", "Memorizing formulas"], "answer": 1,
         "explain": "Mathematics is learned by doing — the hand teaches what the eye skims."},
    ],
    "drills": [
        {"id": "il20-m00-drill1", "title": "Truth-table fluency",
         "items": [
             {"prompt": "Write the truth table for p → q and mark the one false row.", "answer": "False only when p is true and q is false; true on the other three rows.",
              "explain": "Implication is false exactly when the premise holds and the conclusion fails."},
             {"prompt": "Verify De Morgan's AND law on all 4 rows.", "answer": "¬(p∧q) and (¬p∨¬q) agree on all four assignments: T,T→F; T,F→T; F,T→T; F,F→T.",
              "explain": "Row-by-row agreement is the proof."},
             {"prompt": "Give the contrapositive of: 'If n² is even, then n is even.'", "answer": "If n is odd, then n² is odd.",
              "explain": "Contrapositive: negate both sides and swap."},
             {"prompt": "State the induction hypothesis for proving 1+2+…+n = n(n+1)/2.", "answer": "Assume the formula holds for k; prove it for k+1.",
              "explain": "The hypothesis is the bridge from k to k+1."},
         ]},
        {"id": "il20-m00-drill2", "title": "Readiness self-check",
         "items": [
             {"prompt": "Can you solve a 2x2 linear system by elimination without looking anything up?", "answer": "Honest self-assessment; if not, review elimination before M05.",
              "explain": "IL-20's linear algebra modules assume this is fluent."},
             {"prompt": "Do you know what a function, domain, and range are?", "answer": "Honest self-assessment; M04 builds on these from zero but rewards familiarity.",
              "explain": "M04 starts from definitions — familiarity is a head start, not a requirement."},
         ]},
    ],
    "handsOnLab": {
        "id": "il20-m00-lab", "title": "Brute-force logic verifier in Python",
        "brief": ("Write a Python script that enumerates all truth assignments for two and three variables, "
                  "verifies De Morgan's laws and the contrapositive equivalence on every row, and prints a formatted "
                  "truth table. The machine settles every row; your job is to make the machine do it correctly."),
        "steps": ["Write an enumerator yielding all 2^n assignments.",
                  "Verify ¬(p∧q) ≡ ¬p∨¬q and ¬(p∨q) ≡ ¬p∧¬q on all rows.",
                  "Verify (p→q) ≡ (¬q→¬p) and show (p→q) ≢ (q→p) with a counterexample row.",
                  "Print formatted truth tables."],
        "deliverable": "A Python script plus its printed truth tables.",
        "checkpoint": "Every equivalence verified on every row, with the counterexample row shown for the non-equivalence.",
    },
    "mockTask": {
        "id": "il20-m00-mock", "type": "choice",
        "q": "A policy states: 'If the device is unmanaged, then access is denied.' Which restatement is logically equivalent?",
        "choices": ["If access is granted, then the device is managed",
                    "If the device is managed, then access is granted",
                    "If access is denied, then the device is unmanaged",
                    "Unmanaged devices cause denial"],
        "answer": 0,
        "explain": "Contrapositive: ¬(access denied) → ¬(device unmanaged), i.e., access granted → device managed.",
    },
    "videos": [
        {"title": "Khan Academy — Math library", "url": "https://www.khanacademy.org/math", "source": "Khan Academy",
         "blurb": "Free logic, algebra, and precalculus practice aligned to this primer.", "durationMin": 60,
         "verifiedUtc": "2026-10-09T00:00:00Z", "httpStatus": 200},
    ],
    "pdfs": [
        {"title": "Interstitium Labs Visual Guide Library", "url": "https://interstitiumlabs.dev/pdf-library/",
         "source": "Interstitium Labs",
         "blurb": "Animated, illustrated explainers on the core concepts referenced across this course.",
         "verifiedUtc": "2026-10-09T00:00:00Z", "httpStatus": 200},
    ],
    "notes": [
        {"title": "Why this module exists",
         "body": "IL-20 is the full mathematical treatment; IL-02 (Mathematical Maturity Engine) is the primer. This M00 module is the bridge: it replays the IL-02 readiness material — logic, truth tables, proof methods — so you enter M01 (Sets & Propositional Logic) already warm. If this module feels easy, you are ready. If it feels hard, do IL-02 first."},
        {"title": "Drawn from IL-02",
         "body": "Content follows IL-02's Logic & Boolean Algebra and Probability & Statistics modules: propositions, truth tables, De Morgan's laws, quantifiers, and the four proof methods. Cross-links point at the IL-02 source modules for deeper review."},
        {"title": "How to work mathematics",
         "body": "Pencil and paper before screen. Attempt every problem cold, then check. The flashcards are for recall of definitions and laws; the drills are for fluency. Mathematics rewards the hand, not the eye."},
    ],
}

IL20_BS = [
    {"id": "il20-bs-proof", "title": "Find the flaw: the broken induction",
     "moduleId": "m20-proof-methods", "start": "claim",
     "nodes": {
         "claim": {"text": "A classmate 'proves' by induction that all horses are the same color. Base case n=1: trivially true. Inductive step: assume any k horses share a color; for k+1 horses, remove one horse — the remaining k share a color by hypothesis — then put it back and remove a different one. All k+1 share a color. Where is the flaw?",
                   "choices": [{"t": "The inductive step fails at k=1: the two k-sets don't overlap", "to": "right"},
                               {"t": "The base case is wrong", "to": "wrong1"},
                               {"t": "Induction doesn't apply to colors", "to": "wrong2"}]},
         "right": {"text": "Correct. For k=1, the two 1-horse subsets are disjoint — there is no overlapping horse to transfer the color. The step k→k+1 needs the intersection of the two k-sets to be nonempty, which fails exactly at the base. A proof is a machine: one broken gear stops it.", "end": True},
         "wrong1": {"text": "The base case is fine — one horse trivially has 'one color'. The break is in the step. Look at k=1.", "end": True},
         "wrong2": {"text": "Induction applies to any well-defined property of natural numbers. The flaw is structural, not topical.", "end": True}}},
    {"id": "il20-bs-optimize", "title": "Minimize the cost function",
     "moduleId": "m20-linear-systems-optimization", "start": "problem",
     "nodes": {
         "problem": {"text": "Minimize f(x,y) = x² + 2y² subject to x + y = 10, with x,y ≥ 0. Which method fits?",
                     "choices": [{"t": "Lagrange multipliers — equality constraint, smooth objective", "to": "lagrange"},
                                 {"t": "Gradient descent by hand for 1000 iterations", "to": "gd"},
                                 {"t": "Ignore the constraint; minimize freely", "to": "ignore"}]},
         "lagrange": {"text": "Correct. L = x² + 2y² + λ(x+y−10): 2x + λ = 0, 4y + λ = 0 → x = 2y, so 3y = 10, y = 10/3, x = 20/3. Constraint active, boundary check confirms the minimum. Method matched to structure — that is the whole skill.", "end": True},
         "gd": {"text": "Gradient descent solves it numerically but teaches nothing about the structure — and on a contest or exam you don't have 1000 iterations. Match the method to the problem.", "end": True},
         "ignore": {"text": "Unconstrained minimum is (0,0), which violates x+y=10. Constraints are the problem; ignoring them is not solving.", "end": True}}},
]

IL20_CS = [
    {"id": "il20-cs-eigen", "moduleId": "m20-linear-algebra-3", "tool": "Interactive eigenvector explorer",
     "title": "Watch eigenvectors survive a transformation",
     "steps": [
         {"screen": "A 2x2 matrix shown with sliders; the unit square and its image are drawn.",
          "action": "Drag the matrix entries — watch most vectors rotate, but a few only stretch."},
         {"screen": "The stretched-only vectors are highlighted: the eigenvectors.",
          "action": "Read off the stretch factors — the eigenvalues."},
         {"screen": "Switch to a rotation matrix: no real eigenvectors remain.",
          "action": "Note which matrices have them and which don't — that distinction is the module's core."}]},
    {"id": "il20-cs-integral", "moduleId": "m20-calculus-2", "tool": "Riemann sum explorer",
     "title": "Build the definite integral from rectangles",
     "steps": [
         {"screen": "A curve with n rectangles under it; n starts at 4.",
          "action": "Increase n with the slider — watch the sum converge to the shaded area."},
         {"screen": "Toggle left, right, and midpoint rules.",
          "action": "Compare which converges fastest and why the midpoint wins."},
         {"screen": "The limit as n→∞ is named: the definite integral.",
          "action": "Connect the picture to the Fundamental Theorem in your notes."}]},
]

IL20_PYEX = [
    {"id": "il20-py-truth", "title": "Truth-table enumerator", "moduleId": "IL-20-M00",
     "brief": "Generalize the M00 lab: a function taking any propositional formula over n variables and printing its full truth table."},
    {"id": "il20-py-matrix", "title": "Matrix multiplication from scratch", "moduleId": "m20-linear-algebra-2",
     "brief": "Implement matrix multiplication with pure Python lists, then verify against the definition on random 3x3 matrices. No libraries — the point is the definition."},
    {"id": "il20-py-integrate", "title": "Numeric integration", "moduleId": "m20-calculus-2",
     "brief": "Implement left, right, midpoint, and trapezoidal rules; compare convergence rates on ∫x²dx over [0,1] and report which wins."},
    {"id": "il20-py-series", "title": "Series partial sums", "moduleId": "m20-series",
     "brief": "Compute partial sums of the harmonic and geometric series to n=10^5; plot the divergence/convergence and explain the difference."},
]

IL20_TOOLLABS = [
    {"id": "il20-tool-sympy", "title": "SymPy symbolic lab", "moduleId": "m20-calculus-1",
     "brief": "Use SymPy to differentiate, integrate, and solve symbolically — then do the same problems by hand and reconcile. The machine checks the hand."},
    {"id": "il20-tool-jupyter", "title": "Jupyter notebook lab", "moduleId": "m20-linear-algebra-1",
     "brief": "Work a full module's problem set inside a Jupyter notebook: exposition, computation, and plots in one document. The notebook is the lab report."},
]
IL20_INSTALL = [
    {"id": "install-python", "title": "Install Python 3",
     "steps": ["Install Python 3 from the vendor's official downloads page.", "Verify with python3 --version.",
               "Create a virtual environment for the course."],
     "verify": "python3 --version prints 3.x."},
    {"id": "install-jupyter-sympy", "title": "Install Jupyter and SymPy",
     "steps": ["pip install jupyter sympy matplotlib numpy inside the virtual environment.",
               "Launch jupyter notebook and open a test notebook.", "Run a SymPy differentiation to confirm."],
     "verify": "A notebook cell computing diff(x**2) returns 2*x."},
]
IL20_INSTALL_ORDER = ["install-python", "install-jupyter-sympy"]

# ---------------------------------------------------------------- IL-21 sections
IL21_BS = [
    {"id": "il21-bs-trolley", "title": "The autonomous vehicle swerve",
     "moduleId": "m21-ethics-2", "start": "brief",
     "nodes": {
         "brief": {"text": "You write the decision policy for an autonomous shuttle. A brake failure is unavoidable: swerve left into one pedestrian, or continue into five? The utilitarian, deontological, and virtue-ethics answers differ. Which tradition does your policy encode, and can you defend it publicly?",
                   "choices": [{"t": "Utilitarian: minimize harm — swerve", "to": "util"},
                               {"t": "Deontological: never use a person as a mere means — do not swerve", "to": "deon"},
                               {"t": "Refuse to encode any — kick it to a human", "to": "refuse"}]},
         "util": {"text": "A defensible position — but note what it commits you to: the policy now trades lives by arithmetic. The module's point is not the answer; it is that shipping the system IS choosing a tradition, whether you name it or not.", "end": True},
         "deon": {"text": "A defensible position — but note the cost: five deaths you could have prevented by acting. Deontology forbids using the one, even to save five. Name the tradition in the design doc, or the choice gets made by accident.", "end": True},
         "refuse": {"text": "There is no human to kick it to at 60 mph — the refusal IS a policy (continue straight). Every deployed system encodes an ethic. The only choice is whether it is examined.", "end": True}}},
    {"id": "il21-bs-rhetoric", "title": "Argue the budget: make the case",
     "moduleId": "m21-rhetoric", "start": "ask",
     "nodes": {
         "ask": {"text": "Leadership will fund either the security overhaul or the feature team — not both. You have ten minutes. Do you open with data, story, or authority?",
                 "choices": [{"t": "Story: the 2 AM outage, then the numbers", "to": "story"},
                             {"t": "Data: lead with the incident-cost table", "to": "data"},
                             {"t": "Authority: quote the CISO's own memo", "to": "authority"}]},
         "story": {"text": "Strong open — narrative buys attention, then numbers buy the decision. But watch the failure mode: if the story doesn't connect to the ask within 90 seconds, you've told an anecdote, not made a case.", "end": True},
         "data": {"text": "Respectable — and the fastest way to lose a non-technical room. Data persuades after attention is won; lead with it only if the room already trusts the premise.", "end": True},
         "authority": {"text": "Effective if the authority is present and aligned; borrowed authority collapses under one skeptical question. Prefer evidence you can defend yourself.", "end": True}}},
]
IL21_CS = [
    {"id": "il21-cs-argmap", "moduleId": "m21-logic-argument", "tool": "Argument map builder",
     "title": "Map an argument: premises, inferences, objections",
     "steps": [
         {"screen": "A blank canvas with a contested claim in the center.",
          "action": "Add the premises as nodes and draw the inference arrows."},
         {"screen": "Each inference is labeled: deductive, inductive, or abductive.",
          "action": "Attach one objection to the weakest inference."},
         {"screen": "The map shows the argument's load-bearing joint.",
          "action": "Write the one-sentence verdict: where does it actually break?"}]},
]

# ---------------------------------------------------------------- IL-22 sections
IL22_BS = [
    {"id": "il22-bs-correspondence", "title": "'As above, so below': test the correspondence",
     "moduleId": "m22-hermeticism", "start": "text",
     "nodes": {
         "text": {"text": "The Emerald Tablet's most famous line is read as a metaphysical principle, a laboratory instruction, and a psychological maxim. A historian, an alchemist, and a Jungian each claim it. Which reading does the text itself best support?",
                  "choices": [{"t": "All three are later receptions; the text is a short, cryptic recipe-like document", "to": "reception"},
                              {"t": "The psychological reading — it was always about the mind", "to": "psych"},
                              {"t": "The literal laboratory reading", "to": "lab"}]},
         "reception": {"text": "Correct. The responsible move is reception history: the Tablet is brief and obscure, and each era found its own mirror in it. The module's discipline is distinguishing the text from its receptions.", "end": True},
         "psych": {"text": "That reading is Jung's 20th-century reception, not the text's own context. Valuable — but label it as reception.", "end": True},
         "lab": {"text": "Plausible for parts — but the Tablet's obscurity is deliberate, and 'laboratory' meant something different in late antiquity. Check the primary source before the commentary.", "end": True}}},
    {"id": "il22-bs-grimoire", "title": "The grimoire claim: critical reading drill",
     "moduleId": "m22-grimoires", "start": "claim",
     "nodes": {
         "claim": {"text": "A popular book claims a famous grimoire is 'a medieval text of ancient Egyptian magic.' You have the critical edition's introduction. What do you check first?",
                   "choices": [{"t": "Date, language, and manuscript tradition of the actual text", "to": "manuscript"},
                               {"t": "Whether the magic 'works'", "to": "works"},
                               {"t": "The author's other books", "to": "author"}]},
         "manuscript": {"text": "Correct. Most 'ancient' grimoires are early-modern compilations in Latin or vernaculars. The manuscript facts settle the claim in one paragraph; everything else is commentary.", "end": True},
         "works": {"text": "Efficacy is a separate question from provenance — and unanswerable without defining 'works'. Settle the historical claim first.", "end": True},
         "author": {"text": "Useful context, but ad hominem is not evidence. The manuscript tradition is.", "end": True}}},
]
IL22_CS = [
    {"id": "il22-cs-arcana", "moduleId": "m22-tarot", "tool": "Major Arcana timeline explorer",
     "title": "Trace the Major Arcana across five centuries",
     "steps": [
         {"screen": "A timeline: 15th-century Visconti-Sforza cards beside the 1910 Rider-Waite deck.",
          "action": "Compare the Fool across both — note what changed and what persisted."},
         {"screen": "The 22 trumps laid in order with dates of first attestation.",
          "action": "Identify which images are stable across centuries and which are 19th-century occultist additions."},
         {"screen": "The occultist layer is highlighted separately from the game layer.",
          "action": "State the historical verdict: game first, esoteric system later."}]},
]
IL22_XLINKS = {
    "m22-approaching": ["il01-hermetic-foundations"],
    "m22-kabbalah": ["il01-hermetic-foundations"],
    "m22-hermeticism": ["il01-hermetic-foundations"],
    "m22-alchemy": ["il01-hermetic-foundations"],
    "m22-astrology": ["il01-hermetic-foundations"],
    "m22-tarot": ["il01-hermetic-foundations"],
    "m22-enochian": ["il01-dee-enochian"],
    "m22-rosicrucianism": ["il01-hermetic-foundations"],
    "m22-theosophy": ["il01-ccru-seminar"],
    "m22-golden-dawn": ["il01-hermetic-foundations"],
    "m22-grimoires": ["il01-dee-enochian"],
    "m22-gnosticism": ["il01-hermetic-foundations"],
    "m22-eastern-esoteric": ["il01-hermetic-foundations"],
    "m22-divination": ["il01-dee-enochian"],
    "m22-symbolism": ["il-01-esoteric-foundations-math-numtheory"],
    "m22-modern-revival": ["il01-ccru-seminar"],
    "IL-22-PM-NUMTH": ["il-01-esoteric-foundations-math-numtheory"],
    "IL-22-PM-LOGIC": ["il-01-esoteric-foundations-math-logic"],
}

# ---------------------------------------------------------------- IL-23 sections
IL23_BS = [
    {"id": "il23-bs-scaling", "title": "The scaling bet: where does the next 10x come from?",
     "moduleId": "m23-transformers", "start": "bet",
     "nodes": {
         "bet": {"text": "Your lab has budget for one big bet: 10x more training compute, or 10x more inference-time compute per query? The scaling literature and the inference-time results point in different directions. Which do you fund?",
                 "choices": [{"t": "Inference-time compute — the task-time horizon results show reasoning scales there", "to": "inference"},
                             {"t": "Training compute — pretraining scaling laws are the proven curve", "to": "training"},
                             {"t": "Split evenly and hope", "to": "split"}]},
         "inference": {"text": "Defensible per the METR task-time horizon work: inference-time compute extends the tasks agents can complete. But note the dependence — inference scaling rides on a strong base model, which still comes from training scale.", "end": True},
         "training": {"text": "Defensible per the classic scaling laws — but the marginal returns and the cost curve are the debate. The frontier method: state your crux (which curve you believe) before spending.", "end": True},
         "split": {"text": "A split with no crux is indecision with a budget. The module's discipline: write the crux first, then allocate.", "end": True}}},
    {"id": "il23-bs-fusion", "title": "Fusion portfolio: bet the decade",
     "moduleId": "m23-fusion", "start": "fund",
     "nodes": {
         "fund": {"text": "A fund asks you to allocate across magnetic confinement, inertial confinement, and alternative approaches. Breakeven claims arrive monthly. What is your first filter?",
                  "choices": [{"t": "Net energy gain demonstrated and independently diagnosed — Q metrics, not press releases", "to": "physics"},
                              {"t": "Total funding raised — follow the smart money", "to": "money"},
                              {"t": "Founder pedigree", "to": "founder"}]},
         "physics": {"text": "Correct. The frontier method's first filter is always the demonstrated physical result, independently diagnosed. Everything else — funding, team, timeline — is secondary evidence.", "end": True},
         "money": {"text": "Funding follows narratives as well as physics. Capital is a lagging indicator of belief, not a measurement of Q.", "end": True},
         "founder": {"text": "Pedigree predicts fundraising, not breakeven. Filter on the physics first.", "end": True}}},
    {"id": "il23-bs-quantum", "title": "The quantum timeline: when does RSA break?",
     "moduleId": "m23-quantum", "start": "plan",
     "nodes": {
         "plan": {"text": "Your CISO asks when to migrate to post-quantum cryptography. Estimates range from 5 to 30 years. The honest planning input is not a date — what is it?",
                  "choices": [{"t": "The harvest-now-decrypt-later window: data lifetime vs. migration lead time", "to": "hndl"},
                              {"t": "The loudest expert prediction", "to": "expert"},
                              {"t": "Wait for NIST to finish", "to": "wait"}]},
         "hndl": {"text": "Correct. If your data must stay secret 15 years and migration takes 5, you needed to start 5 years before the break — whatever year that is. Plan on windows, not dates.", "end": True},
         "expert": {"text": "Expert timelines disagree by decades. A decision input that varies 6x across experts is not an input — it's noise.", "end": True},
         "wait": {"text": "NIST has published PQC standards; the waiting rationale expired. The question is now migration sequencing.", "end": True}}},
]
IL23_CS = [
    {"id": "il23-cs-epoch", "moduleId": "m23-epoch-ai", "tool": "Capability chart reader",
     "title": "Read an Epoch AI-style capability chart honestly",
     "steps": [
         {"screen": "A chart of benchmark scores over time with a fitted trend line.",
          "action": "Identify what the benchmark actually measures — and what it doesn't."},
         {"screen": "The same data with error bars and a shaded projection cone.",
          "action": "Note how wide the honest projection is versus the headline trend."},
         {"screen": "A second benchmark measuring a different capability, trending differently.",
          "action": "State the verdict: capabilities are plural, and single-curve stories mislead."}]},
]
# frontier fold destinations: IL-23 module -> [(target course, target module id)]
IL23_FOLDS = {
    "m23-transformers": [("IL-12", "aieng-generative-ai--transformers-attention"),
                         ("IL-16", "advanced-genai--transformer-arch-practice")],
    "m23-agents": [("IL-17", "agentic-ai-foundations--agent-loops"),
                   ("IL-12", "aieng-agentic-ai--agent-architectures")],
    "m23-quantum": [("IL-11", "il11-network-crypto-foundations--zt-encryption"),
                    ("IL-11", "il11-network-crypto-foundations--zt-hashing")],
    "m23-semiconductors": [("IL-05", "il05-cloud-native"),
                           ("IL-12", "aieng-production--edge-ondevice-ai")],
    "m23-metr-evals": [("IL-16", "advanced-ml--re-bench-agents-ml-research")],
    "m23-epoch-ai": [("IL-16", "advanced-genai--genai-eval-practice")],
    "m23-crispr": [],
    "m23-fusion": [],
    "m23-bci": [],
    "m23-synbio": [],
    "m23-space": [],
    "m23-frontier-method": [],
}
IL23_FOLD_NOTE = ("Frontier fold-in: this survey module's topic is developed at depth in the listed course(s); "
                  "IL-23 remains the survey source.")
