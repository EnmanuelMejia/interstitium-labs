#!/usr/bin/env python3
"""Retrofit il-02-mathematical-maturity-engine.json to the Multicloud (il-19) course template.
Writes ONLY docs/university/data/courses/il-02-mathematical-maturity-engine.json.
json.load BEFORE and AFTER writing; validates template shape + hard rules."""
import json, os, math, random, re, sys

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses/il-02-mathematical-maturity-engine.json')
doc = json.load(open(BASE))
print('loaded modules:', len(doc['modules']))

# ---------- computed values for worked examples (no hand-computed numbers) ----------
x = 0.5
p5 = x - x**3/6 + x**5/120
true_sin = math.sin(x)
err = abs(p5 - true_sin)
bound = x**7 / math.factorial(7)
print(f'taylor: P5={p5:.10f} true={true_sin:.10f} err={err:.2e} bound={bound:.2e}')

S0, u, d, r, K = 100.0, 1.1, 0.9, 0.05, 100.0
p_rn = (1 + r - d) / (u - d)
Suu, Sud, Sdd = S0*u*u, S0*u*d, S0*d*d
cuu, cud, cdd = max(Suu-K,0), max(Sud-K,0), max(Sdd-K,0)
cu = (p_rn*cuu + (1-p_rn)*cud)/(1+r)
cd = (p_rn*cud + (1-p_rn)*cdd)/(1+r)
c0 = (p_rn*cu + (1-p_rn)*cd)/(1+r)
print(f'binomial: p={p_rn:.4f} cu={cu:.4f} c0={c0:.4f}')

random.seed(7)
N = 100_000
state, count0 = 0, 0
for _ in range(N):
    if state == 0:
        state = 0 if random.random() < 0.7 else 1
    else:
        state = 0 if random.random() < 0.4 else 1
    if state == 0:
        count0 += 1
mc_est = count0 / N
print(f'markov sim: est={mc_est:.4f} exact4/7={4/7:.4f} diff={abs(mc_est-4/7):.4f}')

BRANDS = ['aleks','brilliant','khan academy','coursera','udemy','edx','palantir','nsa']

def build_mod0():
    return {
      "id": "il02-math-spine",
      "code": "IL-02",
      "title": "The Unified Mathematical Spine",
      "weight": 1,
      "summary": ("Welcome to the Mathematical Maturity Engine. I'm your instructor, and this first module is the "
        "whole reason this course exists: the unified mathematical spine — college algebra through probability and "
        "statistics, in the verified course order. We climb it together: equations and functions, trigonometry and "
        "the unit circle, precalculus (complex numbers, vectors, the limits preview), calculus I (limits, "
        "derivatives, integrals, the Fundamental Theorem), calculus II (integration techniques, series, Taylor), "
        "discrete mathematics (logic, proofs, combinatorics, graphs), linear algebra (eigenvalues, least squares, "
        "SVD, matrix calculus for ML), and probability and statistics (distributions, Bayes and MLE/MAP, the law "
        "of large numbers and the central limit theorem, regression, hypothesis testing). I gate every node at "
        "mastery: no calculus without functions, no machine learning without linear algebra."),
      "objectives": [
        "Solve equations and work functions fluently: composition, inverses, graphs.",
        "Differentiate and integrate: rules, applications, the Fundamental Theorem.",
        "Prove: induction, contradiction, invariants — discrete math as a writing discipline.",
        "Diagonalize: eigenvalues, SVD, least squares — linear algebra for ML.",
        "Reason under uncertainty: Bayes, MLE, CLT, regression, testing."
      ],
      "notes": [
        {
          "title": "Concepts",
          "body": "\n".join([
            "- **Function** — a rule assigning each input exactly one output; the core object of algebra — domain, range, composition, inverses.",
            "- **Exponential and logarithm** — an inverse pair, the growth/decay language; change of base: log_a(b) = ln b / ln a.",
            "- **Unit circle** — x²+y²=1; every trigonometric identity lives here.",
            "- **Complex number** — a+bi, the algebraic closure: every polynomial equation has its solutions here.",
            "- **Limit** — the value a function approaches; continuity and the derivative both rest on the epsilon-delta idea.",
            "- **Derivative** — the instantaneous rate of change; definition → rules → the chain rule.",
            "- **Chain rule** — (f∘g)′ = f′(g(x))·g′(x); the whole game in disguise — backprop is the chain rule at scale.",
            "- **Integral** — accumulated area; the definite integral as a limit of Riemann sums.",
            "- **Fundamental Theorem** — differentiation and integration are inverses: ∫ₐᵇ f′ = f(b)−f(a).",
            "- **Series** — an infinite sum; convergence decided by tests — p-series (converges iff p>1), ratio, comparison.",
            "- **Taylor series** — the local polynomial approximation f(x) ≈ Σ f⁽ⁿ⁾(a)(x−a)ⁿ/n!; bound the error with the Lagrange remainder.",
            "- **Induction** — proof by domino: base case → hypothesis → step.",
            "- **Proof by contradiction** — assume the negation, derive the absurd; the contrapositive rides alongside.",
            "- **Pigeonhole principle** — n+1 items in n boxes forces a box with two or more; deceptively powerful.",
            "- **Combinatorics** — organized counting: every 'how many' reduces to product rule, sum rule, and choose.",
            "- **Graph** — vertices and edges; the universal model — paths, cycles, trees, coloring, Euler/Hamilton. When stuck, draw the graph.",
            "- **Modular arithmetic** — arithmetic on remainders; the road to RSA.",
            "- **Finite automaton** — the simplest computation model; the preview of theory.",
            "- **Eigenvalue/eigenvector** — the scalar λ and direction v with Av = λv: where the matrix acts by pure scaling — PCA, PageRank, quantum states.",
            "- **Least squares** — the projection of the data onto the model space; the geometry of regression.",
            "- **SVD** — A = UΣVᵀ, the everything-decomposition: rank, compression, latent factors.",
            "- **Matrix calculus** — gradients of vector-valued functions; the language ML optimizers speak.",
            "- **Distribution** — the zoo: normal, binomial, Poisson, exponential; know each one's story.",
            "- **Bayes' theorem** — P(H|E) = P(E|H)P(H)/P(E); the update rule for all reasoning under uncertainty.",
            "- **MLE/MAP** — fit by maximizing likelihood (MLE), or likelihood × prior (MAP).",
            "- **Law of large numbers** — sample averages converge to the expectation; frequencies become probabilities.",
            "- **Central limit theorem** — sums of many small independent effects go normal; the reason normal distributions are everywhere.",
            "- **Regression and hypothesis testing** — fit the model, then ask whether the fit means anything; p-values and confidence intervals — and their misuses."
          ])
        },
        {
          "title": "Worked estimation",
          "body": (
            "We estimate sin(0.5) with a Taylor polynomial — then prove how wrong we are allowed to be. "
            "This is the estimation discipline the whole spine trains.\n"
            "1. **Write the polynomial.** sin x at a=0: P₅(x) = x − x³/3! + x⁵/5! = x − x³/6 + x⁵/120.\n"
            f"2. **Evaluate at x = 0.5.** x³ = 0.125, x⁵ = 0.03125, so P₅(0.5) = 0.5 − 0.0208333 + 0.0002604 ≈ {p5:.7f}.\n"
            f"3. **Compute the true value and the error.** sin(0.5) = {true_sin:.7f}, so the actual error is ≈ {err:.2e}.\n"
            f"4. **Bound the error before trusting it.** The Lagrange remainder after degree 5 is bounded by the next term's magnitude: "
            f"|x|⁷/7! = 0.5⁷/5040 ≈ {bound:.2e}. The true error sits under the bound — this is estimation with a guarantee.\n"
            "5. **Read the lesson.** Three terms buy six correct digits at x = 0.5, and the remainder tells you what the next term is worth "
            "before you compute it. Approximation with guarantees is the whole of applied analysis — and the fluency gate here is real: "
            "differentiate and integrate the standard forms without pausing."
          )
        },
        {
          "title": "Project brief",
          "body": (
            "Your capstone: **The Spine Map**. Pick a destination — an IL-07 machine-learning module, the electrician aptitude battery, "
            "or the quant ladder in this course's fourth module. Trace its prerequisite chain back to arithmetic: list every spine node the "
            "destination depends on (ML needs gradients → derivatives → limits → functions; SVD → eigenvalues → matrix algebra; "
            "Bayes → distributions → probability). For each node, solve one problem drawn from this module's quizzes or the Taylor / "
            "Monte Carlo / least-squares script labs, and write out one proof (induction of your choice, or the epsilon-delta argument "
            "for a limit). Deliverable: a one-page prerequisite map — nodes, edges, and your honest mastery self-score per node — plus a "
            "two-week remediation plan for your weakest node with daily 15-minute drills. Grading rule: the map must name every dependency "
            "honestly. If you cannot derive it, the node is red. This module gates IL-03's algorithms and IL-08's theory — no induction, "
            "no algorithms."
          )
        },
        {
          "title": "Noah check-in",
          "body": (
            "Noah probes mastery — and honesty. What this module does NOT do: it does not certify you in anything (Interstitium Labs confers "
            "no certificate — see the course honesty note), and reading it once does not make you fluent; the script labs and the weekly proof "
            "are where fluency forms. Noah asks things like:\n"
            "- State the chain rule and name one place it appears outside a calculus class.\n"
            "- In one paragraph each: why no machine learning without linear algebra, and why no machine learning without probability.\n"
            "- Show Noah your spine-map's red nodes and the remediation plan — 'I read it' is not mastery."
          )
        }
      ],
      "cards": [
        {"front": "log_a(b) = ?", "back": "ln b / ln a — change of base. Exponentials and logs are inverses."},
        {"front": "Chain rule?", "back": "(f∘g)' = f'(g(x))·g'(x). Backprop is the chain rule at scale."},
        {"front": "Fundamental Theorem?", "back": "Differentiation and integration are inverses: ∫ₐᵇ f' = f(b)−f(a)."},
        {"front": "Taylor's idea?", "back": "Local polynomial approximation: f(x) ≈ Σ f⁽ⁿ⁾(a)(x−a)ⁿ/n!. Bound error with Lagrange remainder."},
        {"front": "Induction template?", "back": "Base → hypothesis → step. The domino principle."},
        {"front": "Pigeonhole principle?", "back": "n+1 items in n boxes → some box has 2+. Deceptively powerful."},
        {"front": "Eigenvector?", "back": "Av = λv — the direction the matrix only scales."},
        {"front": "SVD?", "back": "A = UΣVᵀ — rank, compression, latent factors in one factorization."},
        {"front": "Bayes' theorem?", "back": "P(H|E) = P(E|H)P(H)/P(E) — update beliefs with evidence."},
        {"front": "CLT?", "back": "Sums of many small independent effects → normal. Why normals are everywhere."}
      ],
      "quiz": [
        {"q": "d/dx [x³·sin x]?", "choices": ["3x²·cos x","3x² sin x + x³ cos x","3x² + cos x","x³·cos x"], "answer": 1,
         "explain": "The product rule — see 'Concepts': (uv)' = u'v + uv'."},
        {"q": "∫ x·eˣ dx?", "choices": ["x·eˣ","(x−1)eˣ + C","eˣ + C","x²eˣ/2"], "answer": 1,
         "explain": "Integration by parts — see 'Concepts': u=x, dv=eˣdx gives xeˣ − eˣ = (x−1)eˣ."},
        {"q": "lim (sin x)/x as x→0?", "choices": ["0","1","∞","undefined"], "answer": 1,
         "explain": "The fundamental trigonometric limit — see 'Concepts': it equals 1."},
        {"q": "Converges: Σ 1/n²?", "choices": ["diverges","converges (p-series, p=2>1)","oscillates","to 0"], "answer": 1,
         "explain": "p-series with p>1 converges — see 'Concepts' on convergence tests."},
        {"q": "Eigenvalues of [[2,0],[0,3]]?", "choices": ["2,2","2 and 3","5","6"], "answer": 1,
         "explain": "Diagonal matrix — eigenvalues sit on the diagonal. See 'Concepts'."},
        {"q": "P(disease|positive test), prevalence 1%, test 99% accurate?", "choices": ["99%","~50%","1%","0%"], "answer": 1,
         "explain": "Bayes' theorem — see 'Concepts': (0.99×0.01)/(0.99×0.01+0.01×0.99) ≈ 50%. The base-rate lesson."}
      ]
    }

def build_mod1():
    return {
      "id": "il02-tech-math",
      "code": "IL-02",
      "title": "Tech Math: Trade-Applied Mathematics",
      "weight": 1,
      "summary": ("Welcome back — I'm your instructor, and this module trades the classroom for the shop: tech math, "
        "trade-applied mathematics. We drill whole-number operations and fractions, decimals, and percents until they're "
        "reflexes — no calculators on aptitude tests — then measurement in both US customary and metric, reading tape, "
        "calipers, and micrometers to the instrument's precision, with dimensional analysis on every conversion: units "
        "cancel like fractions. Then shop math: ratio and proportion, percent applications (markup, waste, discount), area "
        "and volume estimation from drawings, and reading scales. We finish with the readiness verification: a timed run "
        "against the aptitude battery with gap diagnosis — diagnostic, not judgmental."),
      "objectives": [
        "Compute fractions, decimals, percents fluently — under time.",
        "Convert units with dimensional analysis; read instruments to their precision.",
        "Estimate materials: area, volume, waste factors from drawings.",
        "Verify readiness against the aptitude battery; diagnose gaps."
      ],
      "notes": [
        {
          "title": "Concepts",
          "body": "\n".join([
            "- **Fraction** — a ratio of integers; fluency means adding unlike denominators and multiplying straight across without a calculator.",
            "- **Percent** — parts per hundred; part = percent × whole — the single formula behind markup, discount, and waste. Instant conversions are the fluency bar: 3/8 = 0.375 = 37.5%.",
            "- **Estimation** — an order-of-magnitude check before precise computation; Fermi-style: is it 10 or 100? Estimation first, calculation second — catch the decimal error before it costs material.",
            "- **Dimensional analysis** — treating units as algebraic quantities that cancel like fractions: ft × 12 in/ft = in. Write every conversion as a fraction and let the units guide the arithmetic.",
            "- **Tolerance** — the drawing's ± band (e.g., ±1/16″); the pass/fail law, not a suggestion. Measure to decide pass/fail, not from curiosity.",
            "- **Precision** — how finely an instrument reads; read to the instrument's precision, never beyond it.",
            "- **Waste factor** — the allowance for offcuts and error: order = net × (1 + waste%) — 10% for simple cuts, 15%+ for complex ones.",
            "- **Scale** — the drawing-to-reality ratio (e.g., 1/4″ = 1′); measure the drawing, multiply by the scale — and verify against a known dimension.",
            "- **Ratio and proportion** — relative quantities in the shop: mix ratios, gear ratios; solve by scaling to the total parts.",
            "- **The bridge constant** — 25.4 mm = 1 inch, exactly; the constant that joins the two measurement systems."
          ])
        },
        {
          "title": "Hands-on procedure",
          "body": (
            "We estimate material for a job from a drawing — the exact sequence a tradesperson runs before ordering. Follow it on your own room.\n"
            "1. **Read the drawing.** Confirm the scale (e.g., 1/4″ = 1′) and note every tolerance callout — the ± is the law.\n"
            "2. **Measure on paper, scale to reality.** Measure each dimension on the drawing, multiply by the scale factor — then verify against one printed known dimension. If 3.5″ on a 1/4″=1′ drawing, that's 14 feet real.\n"
            "3. **Compute the net quantity.** A 20′ × 12′ floor is 240 sq ft net. Write the units as fractions so they cancel.\n"
            "4. **Apply the waste factor.** Simple layout: order = net × (1 + waste%) = 240 × 1.10 = 264 sq ft. Complex cuts: use 15%+.\n"
            "5. **Convert units with dimensional analysis.** Flooring sells by the square yard: 264 sq ft × (1 sq yd / 9 sq ft) = 29.33… → order 30 sq yd. Units guide the arithmetic — if they don't cancel to sq yd, the setup is wrong.\n"
            "6. **Sanity-check by estimation first.** Your estimate said 'about 30'; if the arithmetic had said 264, the decimal is wrong — trust the estimate's order of magnitude. Estimation first, calculation second."
          )
        },
        {
          "title": "Project brief",
          "body": (
            "Your capstone: **The Contractor's Bid**. Measure a real room — or work from a one-room flooring drawing — and produce a materials "
            "estimate end to end: real dimensions from the scale, net area or volume, waste factor applied (state your percentage and why), unit "
            "conversions with the dimensional-analysis chain written out, and one percent application (a discount or markup) computed with the "
            "part = percent × whole formula. Deliverable: a one-page estimate sheet plus a two-minute timed fraction/percent self-test with your "
            "score and the problems that slowed you down — that list is your drill backlog. Grading rule: every number on the sheet must show "
            "its units cancelling; a number without units is a guess."
          )
        },
        {
          "title": "Noah check-in",
          "body": (
            "Noah probes mastery — and honesty. What this module does NOT do: trade-math fluency does not certify you for any trade, and the "
            "readiness verification is practice against the aptitude battery, not the battery itself. Noah asks things like:\n"
            "- Convert 5/8 to a decimal and a percent, under ten seconds.\n"
            "- Explain why estimation comes before calculation — and what a missed order of magnitude costs on a real job.\n"
            "- A drawing at 1/4″ = 1′ shows 3.5″ for a wall. How long is the wall, and how do you verify?"
          )
        }
      ],
      "cards": [
        {"front": "3/8 as decimal and percent?", "back": "0.375 = 37.5%. Instant conversion is the fluency bar."},
        {"front": "Dimensional analysis?", "back": "Units cancel like fractions — write conversions as fractions, let units guide."},
        {"front": "25.4 mm = ?", "back": "1 inch exactly. The bridge constant."},
        {"front": "Order quantity with waste?", "back": "Order = net × (1 + waste%). 10% simple, 15%+ complex."},
        {"front": "Drawing scale 1/4\" = 1'?", "back": "Measure inches on paper × 4 = feet real. Verify against a known dimension."},
        {"front": "Tolerance ±1/16\" means?", "back": "Pass/fail band — measure to decide, not from curiosity."}
      ],
      "quiz": [
        {"q": "5/8 − 1/4?", "choices": ["4/8","3/8","1/2","3/4"], "answer": 1,
         "explain": "5/8 − 2/8 = 3/8 — see 'Concepts' on fraction fluency."},
        {"q": "15% of 240?", "choices": ["30","36","24","40"], "answer": 1,
         "explain": "part = percent × whole: 0.15 × 240 = 36 — see 'Concepts'."},
        {"q": "Convert 6 ft to inches via dimensional analysis?", "choices": ["0.5","72","18","60"], "answer": 1,
         "explain": "6 ft × 12 in/ft = 72 in — units cancel. See 'Hands-on procedure'."},
        {"q": "Net 80 sq ft, 15% waste. Order?", "choices": ["80","92","95","100"], "answer": 1,
         "explain": "order = net × (1 + waste%) = 80 × 1.15 = 92 sq ft — see 'Concepts'."},
        {"q": "A 3:1 mix needs 12 gallons total. Part A?", "choices": ["3","9","4","6"], "answer": 1,
         "explain": "3:1 = 4 parts; 12/4 = 3 per part; A = 9 gallons — see 'Concepts' on ratio."},
        {"q": "Discount 20% on $85?", "choices": ["$68","$17","$65","$70"], "answer": 0,
         "explain": "85 × 0.80 = $68 (or 85 − 17) — see 'Concepts' on percent."}
      ]
    }

def build_mod2():
    return {
      "id": "il02-electrician",
      "code": "IL-02",
      "title": "Electrician Apprenticeship: etA Entrance",
      "weight": 1,
      "summary": ("Welcome to the electrician apprenticeship track — I'm your instructor, and this module is your entry "
        "ramp into the electrical training ALLIANCE pipeline. We walk the interim credential sequence in order — "
        "Constructing Your Future, Electrical Job Information 1, Applied Codeology 2023, Electrical Theory 1 (DC), "
        "Construction Drawings — because sequence matters: each unlocks the next. You will learn SQ3R technical reading "
        "(survey, question, read, recite, review), because in the trades you read to perform, not to recall. We cover "
        "workplace conduct and well-being, apprentice-wage budgeting and credit, code literacy — finding articles under "
        "time, reading 'shall' versus 'shall be permitted', never assuming an exception — and the algebra fringe the "
        "aptitude batteries actually test: fractions through functions, number series."),
      "objectives": [
        "Complete the interim credential sequence in order.",
        "Read technically with SQ3R: survey → question → read → recite → review.",
        "Navigate code articles: organization, 'shall' language, exceptions.",
        "Pass the algebra fringe: fractions through functions, number series."
      ],
      "notes": [
        {
          "title": "Concepts",
          "body": "\n".join([
            "- **SQ3R** — Survey, Question, Read, Recite, Review; technical reading as reading to perform — the test is doing, not recalling. Recite from memory: recognition is not recall.",
            "- **Ohm's law** — V = IR; voltage drives current through resistance. The physics under everything electrical.",
            "- **Power** — P = VI; with V = IR, the DC trinity.",
            "- **Series circuit** — one path for current; resistances add directly: R_total = R₁ + R₂ + ….",
            "- **Parallel circuit** — voltage is common across branches; reciprocal resistances add: 1/R = 1/R₁ + 1/R₂.",
            "- **'Shall'** — mandatory language in code. Misreading it fails inspections.",
            "- **'Shall be permitted'** — permissive language: allowed, not required. The language of law — 'shall' = must, 'shall be permitted' = may.",
            "- **Exception** — a code carve-out that is never assumed; read the specific exception — it doesn't transfer to other articles.",
            "- **Construction drawings** — symbols, schedules, one-lines; read them to build.",
            "- **Workplace conduct** — standards, reporting channels, bystander responsibility: the trade's social contract.",
            "- **Apprentice-wage planning** — the wage grows in steps; budget to the step you're on, plan for the next. Budget construction: income − obligations = reality.",
            "- **Credit utilization** — the share of available credit in use; keep it under 30% — the fastest lever on the score.",
            "- **Number series** — aptitude-test pattern finding: differences first, ratios second, alternation third."
          ])
        },
        {
          "title": "Hands-on procedure",
          "body": (
            "Code literacy is a lookup skill, not a memory skill. Drill the timed article-finding procedure — the index is the map.\n"
            "1. **State the question precisely.** 'Which article covers conductor ampacity?' — not 'something about wires.'\n"
            "2. **Go to the index first.** Never browse chapters blind; the index maps keywords to articles.\n"
            "3. **Index → chapter → article.** Read the article's scope paragraph before its subsections — scope tells you whether you're even in the right place.\n"
            "4. **Read the language.** Distinguish 'shall' from 'shall be permitted' in every requirement; flag any exceptions and read them in full — exceptions are never assumed and never transfer.\n"
            "5. **Time the lookup.** Record every miss and its cause: wrong keyword, skipped index, misread exception.\n"
            "6. **Repeat with five articles** until lookups run under your target time. Practice the lookup, not just the reading."
          )
        },
        {
          "title": "Project brief",
          "body": (
            "Your capstone: **The Load Calc**. A mock small apartment: list its loads — lighting, receptacles, small appliances — and compute the "
            "total current on 120V circuits with the DC trinity (P = VI, rearranged). Size the conductors using the code's ampacity-table workflow: "
            "locate the tables with the timed lookup drill from 'Hands-on procedure', and document the full lookup path (index → chapter → article) "
            "for each table you used. Produce a one-page panel schedule: circuit, load, current, conductor size. Deliverable: the load table, the "
            "panel schedule, and the two articles you cited — each with the 'shall' language you found in it. Grading rule: no article number from "
            "memory — every citation must show its lookup path."
          )
        },
        {
          "title": "Noah check-in",
          "body": (
            "Noah probes mastery — and honesty. What this module does NOT do: the interim credentials are real programs run by real organizations — "
            "this module does not enroll you in them or confer them; confirm current requirements with the organizations. Code-literacy practice here "
            "does not replace the codebook, and the aptitude drills are practice, not the battery. Noah asks things like:\n"
            "- State Ohm's law from memory, then solve: 12V across 4Ω in series with 2Ω — what current?\n"
            "- Explain the difference between 'shall' and 'shall be permitted' — and why misreading it fails an inspection.\n"
            "- Continue this number series aloud and name the pattern: 2, 6, 12, 20, 30, ?"
          )
        }
      ],
      "cards": [
        {"front": "SQ3R?", "back": "Survey, Question, Read, Recite, Review — reading to perform."},
        {"front": "P = ?", "back": "VI. And V = IR. The DC trinity."},
        {"front": "'Shall' vs 'shall be permitted'?", "back": "Shall = mandatory. Shall be permitted = allowed. The language of law."},
        {"front": "Exceptions?", "back": "Never assumed — read the specific exception; it doesn't transfer."},
        {"front": "Credit utilization target?", "back": "Under 30% — the fastest lever on the score."},
        {"front": "Number series: 2, 6, 12, 20, 30, ?", "back": "42 — differences 4,6,8,10,12, so next is 30+12=42 (pattern n(n+1))."}
      ],
      "quiz": [
        {"q": "12V across 4Ω. Current?", "choices": ["3A","48A","0.33A","12A"], "answer": 0,
         "explain": "I = V/R = 12/4 = 3A — see 'Concepts': Ohm's law."},
        {"q": "100W bulb at 120V for 5 hours. Energy?", "choices": ["0.5 kWh","2.4 kWh","500 Wh = 0.5 kWh","12 kWh"], "answer": 0,
         "explain": "100W × 5h = 500Wh = 0.5 kWh — see 'Concepts' on power."},
        {"q": "Series: 10Ω + 20Ω + 30Ω. Total?", "choices": ["5.45Ω","60Ω","600Ω","30Ω"], "answer": 1,
         "explain": "Series resistances add: 60Ω — see 'Concepts'."},
        {"q": "Parallel: two 100Ω. Total?", "choices": ["200Ω","50Ω","100Ω","10Ω"], "answer": 1,
         "explain": "(100×100)/(100+100) = 50Ω — see 'Concepts' on parallel circuits."},
        {"q": "Series: 2, 4, 8, 16, ?", "choices": ["20","32","24","64"], "answer": 1,
         "explain": "Geometric ×2 — next is 32. See 'Concepts': differences first, ratios second."},
        {"q": "'Shall be permitted' in a code article means the action is?", "choices": ["required","allowed but not required","forbidden","optional only for masters"], "answer": 1,
         "explain": "Permissive language — may, not must. See 'Concepts'."}
      ]
    }

def build_mod3(p_rn, Suu, Sud, Sdd, cuu, cud, cdd, cu, cd, c0, mc_est):
    return {
      "id": "il02-quant-math",
      "code": "IL-02",
      "title": "Quantitative Finance Mathematics",
      "weight": 1,
      "summary": ("Welcome to the quant summit — I'm your instructor, and this module is the mathematical prerequisites "
        "beneath the quant ladder: nothing more, nothing less. We survey measure-theoretic probability — sigma-algebras, "
        "measures, random variables as measurable functions, expectation as integration, the convergence hierarchy — "
        "because that is the language the quant literature speaks. Then stochastic processes: Markov chains and their "
        "stationary distributions, queues with Little's law, Monte Carlo simulation, random walks and the Brownian motion "
        "preview. Finally the financial-math prerequisites: time value of money, returns with variance and covariance, the "
        "Black-Scholes prerequisites without hand-waving — know what each assumption buys — and discrete-time binomial "
        "pricing by replication."),
      "objectives": [
        "State the measure-theoretic foundations: sigma-algebras, expectation as integration.",
        "Analyze Markov chains: stationary distributions, absorption.",
        "Price time: present value, returns, variance/covariance, discrete models.",
        "Connect the math to Black-Scholes prerequisites without hand-waving."
      ],
      "notes": [
        {
          "title": "Concepts",
          "body": "\n".join([
            "- **Sigma-algebra** — a collection of events closed under complement and countable union: the events we can assign probability to.",
            "- **Measure** — a nonnegative, countably additive set function; probability is a measure with total 1.",
            "- **Random variable** — a measurable function X: Ω → ℝ; the grown-up view of a random quantity.",
            "- **Expectation** — E[X] = ∫X dP: expectation as Lebesgue integral.",
            "- **Convergence modes** — almost-sure ⇒ in probability ⇒ in distribution, plus Lᵖ; know the hierarchy and the implications.",
            "- **Markov chain** — a memoryless stochastic process; the future depends only on the present state.",
            "- **Stationary distribution** — π with πP = π and Σπ = 1: the chain's long-run behavior; solve it, don't guess it.",
            "- **Queueing and Little's law** — M/M/1 basics; L = λW: the long-run average number in the system equals arrival rate times average time — deceptively deep.",
            "- **Monte Carlo simulation** — when analysis fails, simulation answers, with confidence intervals; error shrinks as 1/√N.",
            "- **Random walk** — the discrete-time ancestor of Brownian motion; scaling limits give the continuous-time intuition.",
            "- **Brownian motion** — the continuous-time scaling limit of random walks; the noise engine of continuous finance models.",
            "- **Present value** — PV = FV/(1+r)ᵗ: discounting — a dollar today is not a dollar tomorrow; the atom of finance math.",
            "- **Returns, variance, covariance** — the statistics of portfolios; diversification as variance reduction, needing correlation below 1 — the almost-free lunch.",
            "- **Binomial tree** — up/down moves with risk-neutral probabilities; price by replication and backward induction — the computable foundation beneath the continuous models.",
            "- **Risk-neutral pricing** — price as if investors were risk-neutral; replication, not preferences, determines the price."
          ])
        },
        {
          "title": "Worked estimation",
          "body": (
            "We find a Markov chain's stationary distribution two ways: exactly, then by estimation — and compare. "
            "The chain: P = [[0.7, 0.3], [0.4, 0.6]].\n"
            "1. **Solve it exactly.** πP = π with π₀ + π₁ = 1 gives π₀ = 0.7π₀ + 0.4π₁ → π₀ = 4/7 ≈ 0.5714, π₁ = 3/7 ≈ 0.4286. "
            "That's the chain's long-run behavior, in closed form.\n"
            f"2. **Estimate it by simulation.** Run 100,000 transitions from state 0 and count the fraction of steps spent in state 0. "
            f"Result: ≈ {mc_est:.4f} — the law of large numbers converging frequencies onto the stationary distribution.\n"
            f"3. **Compare.** The estimate lands within {abs(mc_est-4/7):.4f} of 4/7 ≈ 0.5714. Estimation agrees with analysis.\n"
            "4. **Read the lesson.** Simulation is estimation with a rate: error shrinks as 1/√N, so each extra decimal costs roughly 100× the "
            "samples. When analysis gives 4/7, you verify; when analysis fails, Monte Carlo answers — with confidence intervals."
          )
        },
        {
          "title": "Project brief",
          "body": (
            "Your capstone: **The Binomial Pricer**. Price a two-step European call with S₀ = 100, up factor u = 1.1, down factor d = 0.9, "
            f"rate r = 5% per step, strike K = 100. Compute the risk-neutral probability p = (1+r−d)/(u−d) = {p_rn:.2f}; build the stock tree "
            f"(up-up {Suu:.0f}, up-down {Sud:.0f}, down-down {Sdd:.0f}); write the terminal payoffs ({cuu:.0f}, {cud:.0f}, {cdd:.0f}); "
            f"work backward — the up-node value is {cu:.2f}, the down-node is {cd:.2f} — to the root price of {c0:.2f}. Then show the replication "
            "portfolio at each node: Δ shares plus the bond position that reproduces the option's payoff. Deliverable: the tree diagram, the price, "
            "the replication table, and one paragraph stating what each Black-Scholes ingredient (lognormal prices, constant volatility, frictionless "
            "markets) assumes and what that assumption buys — no hand-waving. Grading rule: the replication table must balance at every node; "
            "an unbalanced hedge is a wrong price."
          )
        },
        {
          "title": "Noah check-in",
          "body": (
            "Noah probes mastery — and honesty. What this module does NOT do: it is prerequisites, not trading — it does not teach you to trade, "
            "predict markets, or pass a quant interview on its own. Measure theory is surveyed here, not mastered; and the Black-Scholes ingredients "
            "assume constant volatility and frictionless markets, assumptions that fail in practice. Noah asks things like:\n"
            "- State the convergence hierarchy: what does almost-sure convergence imply?\n"
            "- Explain what risk-neutral pricing does NOT mean — and what actually determines the price.\n"
            "- Compute the present value of $100 in 2 years at 5%, and say in one sentence what discounting means."
          )
        }
      ],
      "cards": [
        {"front": "Sigma-algebra?", "back": "Events we can measure: closed under complement and countable unions."},
        {"front": "E[X] grown-up definition?", "back": "∫X dP — expectation as Lebesgue integral."},
        {"front": "Stationary distribution?", "back": "πP = π, Σπ = 1 — the chain's long-run behavior."},
        {"front": "Little's law?", "back": "L = λW — average number = arrival rate × average time."},
        {"front": "PV of $100 in 2 years at 5%?", "back": "100/1.05² ≈ $90.70. Discounting."},
        {"front": "Binomial tree prices by?", "back": "Replication — risk-neutral probabilities, backward induction."}
      ],
      "quiz": [
        {"q": "Convergence a.s. implies?", "choices": ["nothing","in probability (and in distribution)","divergence","L¹ always"], "answer": 1,
         "explain": "a.s. ⇒ in prob ⇒ in dist — the hierarchy. See 'Concepts'."},
        {"q": "2-state chain P=[[0.7,0.3],[0.4,0.6]]. Stationary π?", "choices": ["[0.5,0.5]","[4/7,3/7]","[0.7,0.3]","[0.4,0.6]"], "answer": 1,
         "explain": "Solve πP=π with Σπ=1: π₀=4/7, π₁=3/7 — see 'Worked estimation'."},
        {"q": "M/M/1, λ=2/min, W=3 min. L?", "choices": ["6","1.5","5","0.67"], "answer": 0,
         "explain": "L = λW = 6 customers average — Little's law, see 'Concepts'."},
        {"q": "Diversification reduces?", "choices": ["return","portfolio variance (via imperfect correlation)","risk to zero","taxes"], "answer": 1,
         "explain": "Covariance < 1 → combined variance < weighted average — see 'Concepts'."},
        {"q": "$1000 at 6% for 3 years (annual)?", "choices": ["$1180","$1191.02","$180","$1000"], "answer": 1,
         "explain": "1000 × 1.06³ = $1,191.02 — see 'Concepts' on present value."},
        {"q": "Risk-neutral pricing means?", "choices": ["no risk","price as if investors risk-neutral — replication determines price","ignore risk","high returns"], "answer": 1,
         "explain": "No-arbitrage + replication — preferences drop out. See 'Concepts'."}
      ]
    }

# ---------------- assemble ----------------
doc['modules'] = [build_mod0(), build_mod1(), build_mod2(),
                   build_mod3(p_rn, Suu, Sud, Sdd, cuu, cud, cdd, cu, cd, c0, mc_est)]

# battlePlan: fix off-by-one module numbering -> module titles (consistent with module order)
for b in doc['battlePlan']:
    if b['id'] == 'bp-spine':
        b['detail'] = ("The spine module: algebra → trig → precalc → calc I → calc II → discrete → "
                       "linear algebra → probability. Gate each node at 85%+.")
    elif b['id'] == 'bp-fluency':
        b['detail'] = ("The Tech Math module: arithmetic under time, dimensional analysis, shop math. "
                       "Daily 15-minute sprints.")
    elif b['id'] == 'bp-trade':
        b['detail'] = ("The Electrician module (if electrician-bound): etA credentials, SQ3R reading, "
                       "aptitude batteries, code literacy.")
    elif b['id'] == 'bp-quant':
        b['detail'] = ("The Quant module: measure-theoretic probability, stochastic processes, financial math — "
                       "the prerequisites beneath the quant ladder.")

# ---------------- validate ----------------
errs = []
# course-level keys present
for k in ['arc','priorities','battlePlan','mockTasks','cheatSheets','answerBank','mockMinutes','sourceLinks','honestyNote']:
    if k not in doc: errs.append(f'missing course key {k}')
if not isinstance(doc.get('mockMinutes'), int): errs.append('mockMinutes not int')

GLOSS = re.compile(r'^- \*\*[^*]+\*\* — ', re.M)
for m in doc['modules']:
    titles = [n['title'] for n in m['notes']]
    if len(m['notes']) != 4: errs.append(f"{m['id']}: {len(m['notes'])} notes, want 4")
    if titles[0] != 'Concepts': errs.append(f"{m['id']}: note1={titles[0]}")
    if titles[1] not in ('Hands-on procedure','Worked estimation'): errs.append(f"{m['id']}: note2={titles[1]}")
    if titles[2] != 'Project brief': errs.append(f"{m['id']}: note3={titles[2]}")
    if titles[3] != 'Noah check-in': errs.append(f"{m['id']}: note4={titles[3]}")
    if not GLOSS.search(m['notes'][0]['body']): errs.append(f"{m['id']}: Concepts lacks glossary bullets")
    if not re.search(r'^\d+\. ', m['notes'][1]['body'], re.M): errs.append(f"{m['id']}: note2 lacks numbered steps")
    if len(m.get('cards', [])) < 5: errs.append(f"{m['id']}: {len(m.get('cards',[]))} cards <5")
    if len(m.get('quiz', [])) < 4: errs.append(f"{m['id']}: {len(m.get('quiz',[]))} quiz <4")
    s = m.get('summary','')
    if not (s.startswith('Welcome') and "I'm your instructor" in s): errs.append(f"{m['id']}: summary not instructor voice")
    for qi, q in enumerate(m.get('quiz', [])):
        if len(q.get('choices', [])) != 4: errs.append(f"{m['id']} quiz{qi}: {len(q.get('choices',[]))} choices")
        if not isinstance(q.get('answer'), int) or not 0 <= q['answer'] <= 3: errs.append(f"{m['id']} quiz{qi}: bad answer index")
        if not q.get('explain'): errs.append(f"{m['id']} quiz{qi}: empty explain")
for t in doc['mockTasks']:
    if len(t.get('choices', t.get('required', [1]))) != 4 and t.get('type') == 'choice':
        errs.append(f"mockTask {t['id']}: choices != 4")
    if t.get('type') == 'choice' and not (isinstance(t.get('answer'), int) and 0 <= t['answer'] <= 3):
        errs.append(f"mockTask {t['id']}: bad answer")
    if not t.get('explain'): errs.append(f"mockTask {t['id']}: empty explain")

blob = json.dumps(doc, ensure_ascii=False)
for b in BRANDS:
    if b in blob.lower(): errs.append(f'brand/policy hit: {b}')

if errs:
    print('VALIDATION ERRORS:')
    for e in errs: print(' -', e)
    sys.exit(1)
print('validation OK: 4 modules, 4 notes each, quizzes/cards/mockTasks shaped, no brands')

with open(BASE + '.new', 'w', encoding='utf-8') as f:
    f.write(json.dumps(doc, ensure_ascii=False, separators=(',', ':')))
json.load(open(BASE + '.new'))  # validate written file
os.replace(BASE + '.new', BASE)
json.load(open(BASE))  # validate final file
print('wrote', BASE)
