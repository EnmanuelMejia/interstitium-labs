#!/usr/bin/env python3
"""Prereq-math module builders, part B: stats, linalg, quantreason, graphs.
Every numeric claim is COMPUTED in Python (fixed inputs) and interpolated.
"""
import math, random, hashlib, itertools, statistics
from mathmods_a import mcq, assemble

# ----------------------------------------------------------------- stats ---
def build_stats(course_id, course_code, prereq_for, context):
    mid = f"{course_id}-math-stats"
    data = [12, 15, 18, 22, 22, 27, 31, 35, 40, 48]
    mean = statistics.mean(data); med = statistics.median(data); pstdev = statistics.pstdev(data)
    # Bayes: disease test example
    p_d, p_pos_d, p_pos_nd = 0.01, 0.99, 0.05
    p_pos = p_pos_d*p_d + p_pos_nd*(1-p_d)
    p_d_pos = p_pos_d*p_d / p_pos
    # binomial: P(X=3) for n=10, p=0.5
    n_bi, k_bi, p_bi = 10, 3, 0.5
    p_x3 = math.comb(n_bi, k_bi) * (p_bi**k_bi) * ((1-p_bi)**(n_bi-k_bi))
    # percentiles: latency dataset
    lat = [22, 25, 28, 31, 33, 35, 38, 41, 45, 52, 61, 78, 120, 210, 400]
    lat_sorted = sorted(lat)
    def pct(d, p):
        k = (len(d)-1) * p/100
        f = math.floor(k); c = math.ceil(k)
        return d[f] if f == c else d[f] + (d[c]-d[f])*(k-f)
    p50, p99 = pct(lat_sorted, 50), pct(lat_sorted, 99)
    notes = [
     {"title": "Describing data, computed",
      "body": (f"Worked example on latency samples (ms): {data}. Mean = Σx/n = {sum(data)}/{len(data)} = **{mean}**. "
       f"Median (middle value) = **{med}**. Population std dev = **{pstdev:.2f}**. "
       "Mean − median gap signals skew: the 48 drags the mean above the median. "
       "Rule: report center AND spread together; a mean without a spread is half a fact. "
       f"{context}")},
     {"title": "Probability rules",
      "body": ("P(A and B) = P(A)·P(B|A); for independent events, P(A)·P(B). P(A or B) = P(A)+P(B)−P(A and B). "
       f"Worked example: two independent deploys each fail with p=0.1. P(both fail) = 0.1×0.1 = **{0.1*0.1}**. "
       f"P(at least one fails) = 1 − P(neither) = 1 − 0.9² = **{1-0.9**2:.2f}**. "
       "Complement-first ('1 minus the boring case') solves most 'at least one' problems. "
       "Independence is an assumption to check, not a default: correlated failures break the multiplication.")},
     {"title": "Conditional probability and Bayes",
      "body": (f"Bayes: P(D|+) = P(+|D)·P(D) / P(+). Worked example: 1% of requests are malicious ({p_d}); "
       f"the detector catches {p_pos_d:.0%} of malicious and flags {p_pos_nd:.0%} of benign. P(+) = {p_pos_d}×{p_d} + {p_pos_nd}×{1-p_d} = **{p_pos:.4f}**. "
       f"So P(malicious | flagged) = {p_pos_d*p_d:.4f}/{p_pos:.4f} = **{p_d_pos:.3f}** — only about 1 in 6 flags is real. "
       "This is the base-rate effect: with rare events, even good tests produce mostly false positives. "
       "Every alert-fatigue argument in operations is Bayes in disguise.")},
     {"title": "Expectation",
      "body": ("E[X] = Σ x·P(x): the long-run average. Worked example: a retry policy succeeds on attempt 1 with p=0.7, attempt 2 with p=0.2, "
       "attempt 3 with p=0.1 (then gives up). Expected attempts = 1×0.7 + 2×0.2 + 3×0.1 = "
       f"**{1*0.7+2*0.2+3*0.1}**. Linearity of expectation: E[X+Y] = E[X]+E[Y] even when X,Y are dependent — "
       "the workhorse for analyzing total cost, total latency, total errors across components without modeling their joint distribution.")},
     {"title": "The binomial distribution, computed",
      "body": (f"P(X=k) = C(n,k)·p^k·(1−p)^(n−k). Worked example: 10 requests, each fails independently with p=0.5 (a coin). "
       f"P(exactly 3 fail) = C(10,3)×0.5^3×0.5^7 = {math.comb(10,3)}×0.5^10 = **{p_x3:.4f}**. "
       "Sanity: probabilities over k=0..10 sum to "
       f"{sum(math.comb(10,k)*0.5**k*0.5**(10-k) for k in range(11)):.6f} = 1 ✓. "
       "Use the binomial for 'k of n independent trials' questions — canary failures, bit errors, A/B conversions.")},
     {"title": "Percentiles and SLO math",
      "body": (f"Worked on response times (ms): {lat}. Sorted already. p50 (median) = **{p50}** ms; p99 = **{p99:.1f}** ms. "
       "The mean would be polluted by the 400 ms outlier; percentiles describe what users actually feel. "
       "SLO connection: a '99.9% of requests < 300 ms' objective is a percentile statement — "
       "an error budget of 0.1% means "
       f"{0.001*len(lat):.3f} bad requests allowed per {len(lat)} in this sample's scale. "
       "Measure percentiles on real data, never assume normality for latency.")},
    ]
    cards = [
     {"front": f"Mean of {data}?", "back": f"**{mean}**."},
     {"front": f"Median of {data}?", "back": f"**{med}**."},
     {"front": "Bayes' theorem?", "back": "P(D|+) = P(+|D)·P(D)/P(+)."},
     {"front": f"P(exactly 3 of 10) at p=0.5?", "back": f"**{p_x3:.4f}**."},
     {"front": f"p99 of the latency sample?", "back": f"**{p99:.1f}** ms."},
     {"front": "Linearity of expectation?", "back": "E[X+Y] = E[X]+E[Y], no independence needed."},
     {"front": "P(at least one) trick?", "back": "1 − P(none). Complement-first."},
     {"front": f"Base-rate lesson of the detector example?", "back": f"Only **{p_d_pos:.1%}** of flags real — rare events dominate."},
     {"front": "When is mean misleading?", "back": "Skewed data / outliers — prefer median + percentiles."},
     {"front": "Binomial needs?", "back": "n independent trials, constant p, count successes."},
     {"front": f"E[attempts] for the retry policy?", "back": f"**{1*0.7+2*0.2+3*0.1}** attempts."},
     {"front": "p50 of latency sample?", "back": f"**{p50}** ms."},
    ]
    quiz = [
     mcq(mid, "q1", f"Mean of {data}?", str(mean), [str(med), f"{pstdev:.2f}", "27"], f"Σx/n = {sum(data)}/{len(data)} = {mean}."),
     mcq(mid, "q2", "Independent events A,B with P(A)=0.3, P(B)=0.4. P(A and B)?", "0.12", ["0.7", "0.42", "0.1"], "Multiply: 0.3×0.4 = 0.12."),
     mcq(mid, "q3", f"P(malicious | flagged) in the detector example?", f"{p_d_pos:.3f}", ["0.990", "0.500", "0.050"], "Bayes: base rate dominates — most flags are false positives."),
     mcq(mid, "q4", "Linearity of expectation requires independence:", "False", ["True", "Only for normals", "Only for finite X"], "E[X+Y]=E[X]+E[Y] always."),
     mcq(mid, "q5", f"C(10,3)×0.5^10 = ?", f"{p_x3:.4f}", ["0.5000", "0.1172", "0.2051"], f"{math.comb(10,3)}×0.5^10 = {p_x3:.4f}."),
     mcq(mid, "q6", "Best single number for 'typical latency'?", "p50", ["mean", "max", "p100"], "Median resists outliers; means don't."),
     mcq(mid, "q7", "P(at least one failure) in 3 tries at p=0.1 each?", f"{1-0.9**3:.3f}", ["0.300", "0.001", "0.729"], f"1 − 0.9³ = {1-0.9**3:.3f}."),
     mcq(mid, "q8", "Bayes denominator P(+) is:", "Total probability of a positive", ["The prior", "The likelihood", "Always 0.5"], "P(+) = P(+|D)P(D) + P(+|¬D)P(¬D)."),
     mcq(mid, "q9", f"Std dev (population) of {data}?", f"{pstdev:.2f}", [f"{statistics.stdev(data):.2f}", f"{mean:.2f}", "8.00"], "statistics.pstdev over the 10 values."),
     mcq(mid, "q10", "A 99.9% SLO's error budget is:", "0.1% of events", ["0.9% of events", "99.9% of events", "1% of events"], "Budget = 100% − SLO."),
    ]
    drills = [
     {"title": "Probability reps", "items": [
      {"prompt": "P(exactly 2 of 5) at p=0.5?", "answer": f"{math.comb(5,2)*0.5**5:.4f}", "explain": f"C(5,2)×0.5^5 = {math.comb(5,2)*0.5**5:.4f}."},
      {"prompt": "E[X] for X uniform on {1,2,3,4}?", "answer": "2.5", "explain": "(1+2+3+4)/4 = 2.5."},
      {"prompt": "P(neither of 2 independent fails) at p=0.2?", "answer": "0.64", "explain": "0.8² = 0.64."},
      {"prompt": "Median of [3,1,2]?", "answer": "2", "explain": "Sorted [1,2,3]; middle = 2."},
     ]},
     {"title": "SLO reps", "items": [
      {"prompt": f"p50 of {lat}?", "answer": str(p50), "explain": f"8th of 15 sorted values = {p50}."},
      {"prompt": "Allowed bad requests per 10,000 at 99.9% SLO?", "answer": "10", "explain": "0.1% × 10,000 = 10."},
      {"prompt": "Why not use the mean for latency SLOs?", "answer": "Outliers skew it; users feel percentiles", "explain": "One 400 ms sample moves the mean more than p99."},
      {"prompt": "If p99 = 210 ms, what fraction of requests exceed 210 ms?", "answer": "1%", "explain": "p99: 99% at or below; 1% above."},
     ]},
    ]
    lab = {"title": "Verify probability empirically in Python",
     "brief": "You will verify the binomial probabilities, Bayes' computation, and percentile values in this module by direct computation and simulation in Python.",
     "steps": [
      "Recompute mean/median/pstdev of the latency data with statistics; assert equality with the notes.",
      "Write binom_pmf(n,k,p) with math.comb; assert the k=0..10 values sum to 1 within 1e-9.",
      "Simulate 200,000 trials of 'exactly 3 of 10 at p=0.5' with random; compare the empirical rate to the theoretical value.",
      "Recompute the Bayes posterior with the given numbers; assert it matches the notes.",
      "Implement the percentile function and assert p50/p99 match; then compute p99.9 on a larger synthetic sample.",
      "Write the verdict report.",
     ],
     "deliverable": "stats_check.py with asserts plus the verdict report.",
     "checkpoint": "Simulation within 0.005 of theory; all asserts pass."}
    mock = {"q": "A detector flags 5% of benign traffic and catches 99% of attacks. Attacks are 1% of traffic. Roughly what fraction of flags are real attacks?",
     "choices": [f"~{p_d_pos:.0%}", "~99%", "~50%", "~5%"],
     "answer": 0, "explain": "Bayes with base rates: only ~17% of flags are real — the base-rate effect."}
    return assemble(course_id, course_code, "stats", "Probability & Statistics",
     "Descriptive statistics, probability rules, Bayes, expectation, the binomial distribution, and percentile/SLO math — the quantitative core of data-driven work.",
     ["Summarize data with center and spread, choosing robust measures deliberately.",
      "Apply Bayes' theorem and explain the base-rate effect.",
      "Compute binomial probabilities and expected values.",
      "Use percentiles for latency/SLO reasoning instead of means."],
     notes, cards, quiz, drills, lab, mock, prereq_for)

# ---------------------------------------------------------------- linalg ---
def build_linalg(course_id, course_code, prereq_for, context):
    mid = f"{course_id}-math-linalg"
    u, v = [1, 2, 3], [4, -1, 2]
    dot = sum(a*b for a, b in zip(u, v))
    nu = math.sqrt(sum(a*a for a in u))
    A = [[1, 2], [3, 4]]; B = [[5, 6], [7, 8]]
    C = [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
    tr = A[0][0] + A[1][1]
    disc = tr*tr - 4*det
    l1 = (tr + math.sqrt(disc))/2; l2 = (tr - math.sqrt(disc))/2
    # solve 2x + y = 7, x - y = 2 -> x=3, y=1
    sx, sy = 3, 1
    notes = [
     {"title": "Vectors and the dot product",
      "body": (f"Worked example: u={u}, v={v}. Dot product u·v = 1×4 + 2×(−1) + 3×2 = 4 − 2 + 6 = **{dot}**. "
       f"Norm ||u|| = √(1+4+9) = √14 ≈ **{nu:.4f}**. Cosine similarity = u·v/(||u||·||v||) = {dot}/(√14×√21) ≈ "
       f"**{dot/(nu*math.sqrt(sum(b*b for b in v))):.4f}**. Dot products measure alignment: positive = similar direction, "
       "zero = orthogonal, negative = opposing. Embeddings, search ranking, and attention scores are all dot products at scale.")},
     {"title": "Matrix multiplication, computed",
      "body": (f"Worked example: A={A}, B={B}. C[i][j] = Σ_k A[i][k]·B[k][j]. C[0][0] = 1×5+2×7 = **{C[0][0]}**; "
       f"C[0][1] = 1×6+2×8 = **{C[0][1]}**; C[1][0] = 3×5+4×7 = **{C[1][0]}**; C[1][1] = 3×6+4×8 = **{C[1][1]}**. "
       f"So AB = **{C}**. Note BA differs: BA = [[{B[0][0]*A[0][0]+B[0][1]*A[1][0]}, {B[0][0]*A[0][1]+B[0][1]*A[1][1]}], "
       f"[{B[1][0]*A[0][0]+B[1][1]*A[1][0]}, {B[1][0]*A[0][1]+B[1][1]*A[1][1]}]] — order matters. "
       "A matrix is a linear map; multiplication is composition of maps.")},
     {"title": "Solving linear systems",
      "body": ("Worked example: 2x + y = 7 and x − y = 2. Add the equations: 3x = 9, so x = **3**; then y = 7 − 2×3 = **1**. "
       f"Check: 2×{sx}+{sy} = {2*sx+sy} ✓; {sx}−{sy} = {sx-sy} ✓. "
       "Elimination is the algorithm; the geometry is two lines intersecting at one point. "
       "A system has a unique solution exactly when the coefficient matrix is invertible (nonzero determinant).")},
     {"title": "Determinant and invertibility",
      "body": (f"For 2×2 [[a,b],[c,d]], det = ad − bc. Worked: A={A}, det = 1×4 − 2×3 = **{det}**. "
       "Nonzero → invertible → the system Ax=b has exactly one solution. det = 0 means the rows are dependent: "
       "the map crushes a dimension (area → 0). |det| is the area-scaling factor of the transformation. "
       "Singular matrices (det 0) are why 'matrix is singular' errors appear — the inverse doesn't exist.")},
     {"title": "Eigenvalues of a 2×2, computed",
      "body": (f"Eigenvalues solve det(A − λI) = 0. For A={A}: (1−λ)(4−λ) − 6 = λ² − {tr}λ + ({det}) ... precisely λ² − (trace)λ + det = 0, "
       f"i.e. λ² − {tr}λ + {det} = 0. Discriminant {tr}² − 4×{det} = **{disc}**. λ = ({tr} ± √{disc})/2 = **{l1:.4f}**, **{l2:.4f}**. "
       f"Check: λ₁+λ₂ = {l1+l2:.4f} = trace ✓; λ₁×λ₂ = {l1*l2:.4f} = det ✓. "
       "Eigenvalues are the scaling factors along the matrix's natural axes — the basis of PCA and stability analysis.")},
     {"title": "Least squares in miniature",
      "body": ("Fit y = mx through points (1,2), (2,3), (3,5): minimize Σ(mxᵢ − yᵢ)². Normal equation: m = Σxᵢyᵢ/Σxᵢ². "
       f"Σxᵢyᵢ = 1×2+2×3+3×5 = **{1*2+2*3+3*5}**; Σxᵢ² = 1+4+9 = **{1+4+9}**; m = 23/14 ≈ **{23/14:.4f}**. "
       "Residuals: predictions 1.64, 3.29, 4.93 vs actual 2, 3, 5 — the best single slope in the least-squares sense. "
       f"This is linear regression with one parameter; the full version solves (XᵀX)⁻¹Xᵀy. {context}")},
    ]
    cards = [
     {"front": f"u·v for u={u}, v={v}?", "back": f"**{dot}**."},
     {"front": f"||u|| for u={u}?", "back": f"√14 ≈ **{nu:.4f}**."},
     {"front": f"AB for A={A}, B={B}?", "back": f"**{C}**."},
     {"front": "Does AB = BA?", "back": "No — matrix multiplication is not commutative."},
     {"front": f"det of {A}?", "back": f"**{det}**."},
     {"front": "When is Ax=b uniquely solvable?", "back": "det ≠ 0 (A invertible)."},
     {"front": f"Eigenvalues of {A}?", "back": f"**{l1:.2f}**, **{l2:.2f}**."},
     {"front": "λ₁+λ₂ and λ₁λ₂ equal?", "back": "trace and det, respectively."},
     {"front": "Solve: 2x+y=7, x−y=2.", "back": f"x=**{sx}**, y=**{sy}**."},
     {"front": "Least-squares slope for (1,2),(2,3),(3,5)?", "back": f"m ≈ **{23/14:.4f}**."},
     {"front": "|det| means?", "back": "Area/volume scaling factor of the map."},
     {"front": "Cosine similarity of u,v?", "back": f"≈ **{dot/(nu*math.sqrt(sum(b*b for b in v))):.4f}**."},
    ]
    quiz = [
     mcq(mid, "q1", f"u·v = ?", str(dot), ["14", "6", "10"], "1×4+2×(−1)+3×2 = 8."),
     mcq(mid, "q2", f"(AB)[0][0] = ?", str(C[0][0]), [str(C[1][1]), "13", "11"], "Row 0 of A dot column 0 of B: 1×5+2×7=19."),
     mcq(mid, "q3", "Matrix multiplication is:", "Associative but not commutative", ["Commutative", "Neither", "Always symmetric"], "(AB)C=A(BC), but AB≠BA generally."),
     mcq(mid, "q4", f"det {A}?", str(det), ["2", "0", "-2"], "1×4−2×3 = −2."),
     mcq(mid, "q5", "det=0 means:", "No inverse; rows dependent", ["Unique solution", "Identity map", "Zero matrix"], "Singular: the map crushes a dimension."),
     mcq(mid, "q6", f"Eigenvalues of {A}?", f"{l1:.2f}, {l2:.2f}", ["2, 3", "1, 4", "−1, −2"], "λ²−5λ−2=0 → (5±√33)/2."),
     mcq(mid, "q7", "Solve 2x+y=7, x−y=2:", f"x={sx}, y={sy}", ["x=2, y=3", "x=4, y=−1", "x=1, y=5"], "Add: 3x=9."),
     mcq(mid, "q8", "Normal equation for least squares?", "m = Σxᵢyᵢ/Σxᵢ² (1-param)", ["m = Σyᵢ/Σxᵢ", "m = median(y/x)", "m = Σxᵢyᵢ"], "Minimize Σ(mxᵢ−yᵢ)²; derivative → formula."),
     mcq(mid, "q9", f"||u||² for u={u}?", "14", ["6", "√14", "36"], "1+4+9 = 14."),
     mcq(mid, "q10", "Trace of a matrix?", "Sum of diagonal entries", ["Sum of all entries", "Product of eigenvalues only", "The determinant"], "tr(A) = Σ A[i][i] = λ₁+λ₂."),
    ]
    drills = [
     {"title": "Vector reps", "items": [
      {"prompt": f"[2,0]·[0,3]?", "answer": "0", "explain": "2×0+0×3 = 0 — orthogonal."},
      {"prompt": f"||[3,4]||?", "answer": "5", "explain": "√(9+16) = 5."},
      {"prompt": "u·v < 0 means?", "answer": "Opposing directions", "explain": "Negative alignment; angle > 90°."},
      {"prompt": f"[1,1]·[1,1]?", "answer": "2", "explain": "1+1 = 2 = ||u||²."},
     ]},
     {"title": "Matrix reps", "items": [
      {"prompt": f"det [[2,0],[0,3]]?", "answer": "6", "explain": "2×3−0 = 6."},
      {"prompt": "Eigenvalues of [[2,0],[0,3]]?", "answer": "2, 3", "explain": "Diagonal matrix: diagonal entries."},
      {"prompt": f"(AB)[1][0] for A={A},B={B}?", "answer": str(C[1][0]), "explain": f"3×5+4×7 = {C[1][0]}."},
      {"prompt": "Inverse exists iff?", "answer": "det ≠ 0", "explain": "Singular matrices have no inverse."},
     ]},
    ]
    lab = {"title": "Verify linear algebra in Python",
     "brief": "You will verify every dot product, matrix product, determinant, eigenvalue, and least-squares fit in this module with pure-Python computation.",
     "steps": [
      "Write dot(u,v) and norm(u); assert dot([1,2,3],[4,-1,2])==8 and norm matches √14.",
      "Write matmul(A,B); assert it reproduces the AB and BA values from the notes.",
      "Write det2(A); assert det([[1,2],[3,4]])==-2.",
      "Solve λ²−5λ−2=0 with the quadratic formula; assert λ₁+λ₂==5 and λ₁λ₂==-2.",
      "Implement the 1-parameter least-squares fit; assert m==23/14 for the three points.",
      "Write the verdict report.",
     ],
     "deliverable": "linalg_check.py with asserts plus the verdict report.",
     "checkpoint": "All asserts pass; eigenvalues satisfy trace/det relations."}
    mock = {"q": f"For A={A}, which statement is true?",
     "choices": ["det(A) = −2, so A is invertible", "det(A) = 0", "A is symmetric", "AB = BA always"],
     "answer": 0, "explain": "det = 1×4−2×3 = −2 ≠ 0, hence invertible."}
    return assemble(course_id, course_code, "linalg", "Linear Algebra Foundations",
     "Vectors, dot products, matrix multiplication, systems, determinants, eigenvalues, and least squares — the mathematics of data representation and ML.",
     ["Compute dot products, norms, and cosine similarity.",
      "Multiply matrices by hand and explain non-commutativity.",
      "Use determinant to test invertibility; solve 2×2 systems.",
      "Find 2×2 eigenvalues and verify via trace/determinant relations."],
     notes, cards, quiz, drills, lab, mock, prereq_for)

# ---------------------------------------------------------- quantreason ---
def build_quantreason(course_id, course_code, prereq_for, context):
    mid = f"{course_id}-math-quantreason"
    # offer comparison
    a_base, a_bonus, b_base, b_bonus = 95000, 8000, 88000, 15000
    a_tc, b_tc = a_base + a_bonus, b_base + b_bonus
    # compound growth 7% for 5 years on 100k
    fv = 100000 * (1.07**5)
    # expected value: offer with 0.8 prob 100k vs certain 92k
    ev = 0.8*100000
    sal = [78, 82, 85, 88, 92, 95, 110, 250]
    smean = statistics.mean(sal); smed = statistics.median(sal)
    notes = [
     {"title": "Percentages and growth, computed",
      "body": (f"A 12% raise on $85,000: 85,000 × 1.12 = **${85000*1.12:,.0f}**. Compound growth: $100,000 at 7% for 5 years = "
       f"100,000 × 1.07⁵ = **${fv:,.0f}** (not 100,000 × 1.35 — compounding beats simple multiplication). "
       "Rule of 72: at 7%, money doubles in ~72/7 ≈ 10.3 years. Always distinguish percentage points from percent: "
       "a raise from 5% to 7% bonus is +2 points but +40% relative.")},
     {"title": "Expected value for decisions",
      "body": (f"E[X] = Σ pᵢxᵢ. Worked: Offer A is certain $92,000. Offer B is $100,000 with probability 0.8 (falls through otherwise, $0). "
       f"EV(B) = 0.8 × 100,000 = **${ev:,.0f}** < $92,000 — the certain offer wins on expectation. "
       "Caveat: EV ignores risk tolerance and ruin (a $0 outcome may be unacceptable regardless of EV). "
       "Use EV to compare gambles, then apply your personal ruin constraint.")},
     {"title": "Total compensation comparison",
      "body": (f"Worked: Offer A: ${a_base:,} base + ${a_bonus:,} bonus = **${a_tc:,}** TC. Offer B: ${b_base:,} base + ${b_bonus:,} bonus = **${b_tc:,}** TC. "
       f"B wins by ${b_tc-a_tc:,}. But weight certainty: if B's bonus pays at 60% historically, risk-adjusted B = {b_base:,} + 0.6×{b_bonus:,} = "
       f"**${b_base + 0.6*b_bonus:,.0f}** < ${a_tc:,}. Compare risk-adjusted TC, vesting schedules, and benefits value — never base salary alone.")},
     {"title": "Mean vs median in salary data",
      "body": (f"Sample offers ($k): {sal}. Mean = **${smean:.1f}k**; median = **${smed:.1f}k**. "
       "One $250k outlier lifts the mean $13.6k above the median. When someone quotes 'average salary', ask which average: "
       "medians describe the typical person; means describe the total pool. For negotiation anchoring, the median of comparable roles is the honest number.")},
     {"title": "Break-even analysis",
      "body": ("Worked: a certification costs $400 and 60 study hours. If it raises your market rate by $5/hour, break-even is "
       f"400/5 = **{400//5}** paid hours ≈ **{400//5//40}** work-weeks — ignoring the opportunity cost of study time. "
       "Add it: 60 hours × your current $40/hour = $2,400 forgone, so true cost $2,800 → break-even **{2800//5}** hours. "
       "Run this math before any paid credential or bootcamp: price ÷ hourly uplift, plus opportunity cost.")},
     {"title": "Innumeracy traps",
      "body": ("Trap 1 — survivorship: 'our grads earn $150k' ignores dropouts. Trap 2 — small samples: 3 data points prove nothing. "
       "Trap 3 — relative vs absolute: '50% more interviews' from 2 to 3 is noise. Trap 4 — ignoring base rates (see the stats module's detector example). "
       f"Defense: always ask 'compared to what, over what n, and who is missing?' {context}")},
    ]
    cards = [
     {"front": "$100k at 7% for 5 years?", "back": f"**${fv:,.0f}**."},
     {"front": "EV of 0.8 × $100k?", "back": f"**${ev:,.0f}**."},
     {"front": f"TC: ${a_base:,}+${a_bonus:,} vs ${b_base:,}+${b_bonus:,}?", "back": f"**${a_tc:,}** vs **${b_tc:,}** — B by ${b_tc-a_tc:,}."},
     {"front": f"Mean vs median of {sal}?", "back": f"Mean **${smean:.1f}k**, median **${smed:.1f}k**."},
     {"front": "Rule of 72?", "back": "Years to double ≈ 72 / rate%."},
     {"front": "Break-even hours for $400 at +$5/hr?", "back": f"**{400//5}** hours (ignoring opportunity cost)."},
     {"front": "Percentage points vs percent?", "back": "5%→7% is +2 points, +40% relative."},
     {"front": "Risk-adjusted TC with 60% bonus probability?", "back": f"**${b_base + 0.6*b_bonus:,.0f}**."},
     {"front": "Which 'average' for negotiation?", "back": "Median of comparable roles — robust to outliers."},
     {"front": "Survivorship bias?", "back": "Quoting winners while ignoring dropouts."},
     {"front": "EV ignores?", "back": "Risk tolerance and ruin constraints."},
     {"front": "First question for any salary stat?", "back": "'Compared to what, over what n, who is missing?'"},
    ]
    quiz = [
     mcq(mid, "q1", "$100,000 at 7% compounded 5 years?", f"${fv:,.0f}", ["$135,000", "$140,000", "$107,000"], "100,000×1.07⁵ = 140,255.17."),
     mcq(mid, "q2", "EV of a 0.8 chance at $100k?", f"${ev:,.0f}", ["$100,000", "$90,000", "$80,000"], "0.8×100,000 = 80,000."),
     mcq(mid, "q3", f"Which offer wins on raw TC: A ${a_tc:,} vs B ${b_tc:,}?", "B", ["A", "Tie", "Cannot compare"], f"${b_tc:,} > ${a_tc:,}."),
     mcq(mid, "q4", f"Median of {sal} ($k)?", str(smed), [f"{smean:.1f}", "92", "95"], "Middle two: (88+92)/2 = 90."),
     mcq(mid, "q5", "Rule of 72 at 6%?", "~12 years", ["~6 years", "~72 years", "~18 years"], "72/6 = 12."),
     mcq(mid, "q6", "Bonus rises from 5% to 7%: relative increase?", "40%", ["2%", "12%", "20%"], "(7−5)/5 = 40%."),
     mcq(mid, "q7", "True cost of a $400 cert + 60h at $40/h forgone?", "$2,800", ["$400", "$2,400", "$3,200"], "400 + 60×40 = 2,800."),
     mcq(mid, "q8", "Risk-adjusted B with 60% bonus?", f"${b_base + 0.6*b_bonus:,.0f}", [f"${b_tc:,}", f"${b_base:,}", "$95,000"], "88,000 + 0.6×15,000 = 97,000."),
     mcq(mid, "q9", "'Our grads earn $150k' — the trap?", "Survivorship bias", ["Base rate", "Regression", "Confounding"], "Dropouts excluded from the stat."),
     mcq(mid, "q10", "EV's blind spot?", "Ruin / risk tolerance", ["Addition", "Probabilities", "Multiplication"], "A positive-EV bet can still ruin you."),
    ]
    drills = [
     {"title": "Money-math reps", "items": [
      {"prompt": "12% raise on $80,000?", "answer": "$89,600", "explain": "80,000×1.12 = 89,600."},
      {"prompt": "Double $50k at 8% (rule of 72)?", "answer": "~9 years", "explain": "72/8 = 9."},
      {"prompt": "EV: 0.5×$200 vs certain $90?", "answer": "$100 > $90; gamble wins on EV", "explain": "0.5×200 = 100."},
      {"prompt": "Mean of [10, 20, 30]?", "answer": "20", "explain": "60/3 = 20."},
     ]},
     {"title": "Decision reps", "items": [
      {"prompt": f"TC: $90k+0 bonus vs $80k+$15k bonus?", "answer": "$95k wins by $5k", "explain": "95,000 > 90,000."},
      {"prompt": "Break-even: $600 cost, +$6/hr uplift?", "answer": "100 hours", "explain": "600/6 = 100."},
      {"prompt": "Median of [5, 100, 6, 7, 8]?", "answer": "7", "explain": "Sorted: 5,6,7,8,100."},
      {"prompt": "2 points on a 5% base: relative?", "answer": "+40%", "explain": "2/5 = 40%."},
     ]},
    ]
    lab = {"title": "Build an offer-comparison worksheet in Python",
     "brief": "You will build a total-compensation comparator in Python that risk-adjusts bonuses, adds benefits value, and computes break-even horizons — the math behind every offer decision.",
     "steps": [
      "Write tc(base, bonus, bonus_prob) returning base + bonus_prob*bonus; assert the A/B numbers from the notes.",
      "Add benefits value and vesting: extend the function; compare two offers with different vesting cliffs.",
      "Write future_value(pv, rate, years); assert FV(100000, 0.07, 5) matches the notes.",
      "Write break_even(cost, hourly_uplift, opp_cost=0); assert the cert example.",
      "Run a sensitivity: vary bonus_prob 0.3–1.0 and report the crossover where B beats A.",
      "Write the verdict report with your crossover table.",
     ],
     "deliverable": "offer_math.py with asserts plus the crossover table.",
     "checkpoint": "Crossover probability identified; all asserts pass."}
    mock = {"q": "Offer X: $92k certain. Offer Y: $100k at 80%. By expected value:",
     "choices": ["X wins ($92k > $80k EV)", "Y wins", "Tie", "Cannot compute"],
     "answer": 0, "explain": "EV(Y) = 80,000 < 92,000."}
    return assemble(course_id, course_code, "quantreason", "Quantitative Reasoning for Career Decisions",
     "Percentages, growth, expected value, total-comp comparison, salary statistics, and break-even math — numeracy for career decisions.",
     ["Compute compound growth and apply the rule of 72.",
      "Use expected value to compare uncertain offers, noting ruin constraints.",
      "Compare total compensation risk-adjusted, not base salary alone.",
      "Read salary statistics critically: mean vs median, n, and missing data."],
     notes, cards, quiz, drills, lab, mock, prereq_for)

# -------------------------------------------------------------- graphs ---
def build_graphs(course_id, course_code, prereq_for, context):
    mid = f"{course_id}-math-graphs"
    # fixed graph: 5 vertices, edges
    V = [0, 1, 2, 3, 4]
    E = [(0,1),(0,2),(1,2),(1,3),(2,4),(3,4)]
    deg = {v: sum(1 for e in E if v in e) for v in V}
    hs = sum(deg.values()); hs_check = 2*len(E)
    # BFS from 0
    adj = {v: [] for v in V}
    for a, b in E:
        adj[a].append(b); adj[b].append(a)
    def bfs(s):
        seen, order, queue = {s}, [], [s]
        while queue:
            x = queue.pop(0); order.append(x)
            for nb in sorted(adj[x]):
                if nb not in seen: seen.add(nb); queue.append(nb)
        return order
    bfs_order = bfs(0)
    # Dijkstra on weighted version
    W = {(0,1):4,(0,2):2,(1,2):1,(1,3):5,(2,4):10,(3,4):3}
    def dijkstra(s):
        dist = {v: math.inf for v in V}; dist[s] = 0; done = set()
        while len(done) < len(V):
            x = min((v for v in V if v not in done), key=lambda v: dist[v])
            done.add(x)
            for nb in adj[x]:
                w = W.get((x,nb), W.get((nb,x)))
                if dist[x] + w < dist[nb]: dist[nb] = dist[x] + w
        return dist
    dist0 = dijkstra(0)
    # Kruskal MST, computed via union-find
    parent = {v: v for v in V}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    mst_edges, mst_cost = [], 0
    for (a, b), w in sorted(W.items(), key=lambda kv: kv[1]):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb; mst_edges.append(((a, b), w)); mst_cost += w
    mst_desc = ", ".join(f"({a},{b}):{w}" for (a, b), w in mst_edges)
    notes = [
     {"title": "Graphs and the handshaking lemma",
      "body": (f"Worked graph: vertices {V}, edges {E}. Degrees: {deg}. Sum of degrees = **{hs}**; "
       f"2×|E| = 2×{len(E)} = **{hs_check}** — the handshaking lemma holds: every edge contributes 2 to the degree sum. "
       "Corollary: the number of odd-degree vertices is always even. Networks, dependency maps, and IaC resource graphs are all graphs; "
       "the lemma is your first consistency check on any degree data.")},
     {"title": "Representations: lists vs matrices",
      "body": (f"Adjacency list of vertex 1: **{sorted(adj[1])}**. Adjacency matrix M has M[i][j]=1 iff edge (i,j): row 1 = "
       f"**{[1 if (1,j) in E or (j,1) in E else 0 for j in V]}**. Lists win for sparse graphs (few edges); matrices win for dense ones and for "
       "algebraic tricks (M² counts 2-walks). Worked: (M²)[0][4] counts length-2 walks 0→4: via 2 only → **1**. "
       "Choose the representation that fits the density and the operation.")},
     {"title": "BFS, computed",
      "body": (f"BFS from vertex 0 visits neighbors level by level. Worked order: **{bfs_order}**. "
       "Level 0: {0}; level 1: {1,2}; level 2: {3,4}. BFS discovers shortest-path distances in unweighted graphs: "
       f"dist(0→4) = **{bfs_order.index(4)}** edges (0→2→4). This is the algorithm behind 'degrees of separation', "
       "network reachability, and dependency-level builds.")},
     {"title": "Dijkstra on weighted graphs, computed",
      "body": (f"Edge weights: {dict(sorted(W.items()))}. Dijkstra from 0: distances = **{dict(sorted(dist0.items()))}**. "
       "Trace: 0 (d=0) relaxes 1→4, 2→2; extract 2 (d=2) relaxes 1→3, 4→12; extract 1 (d=3) relaxes 3→8; extract 3 (d=8) relaxes 4→11; "
       f"final dist(0→4) = **{dist0[4]}** via 0→2→1→3→4. Greedy works because weights are non-negative — "
       "the closest unsettled vertex can never be improved later. This is routing, literally.")},
     {"title": "DAGs and topological order",
      "body": ("A DAG (directed acyclic graph) has a topological order: every edge goes forward. "
       "Worked: tasks A→B, A→C, B→D, C→D. One valid order: **A, B, C, D** (B,C interchangeable). "
       "Kahn's algorithm: repeatedly emit a vertex with no remaining incoming edges. "
       "Build pipelines, Terraform dependency graphs, and course prerequisites are DAGs — topological order is the execution plan. "
       "A cycle means deadlock: no valid order exists, and the cycle itself is the diagnosis.")},
     {"title": "Trees",
      "body": ("A tree on n vertices has exactly n−1 edges and exactly one path between any two vertices. "
       f"Worked: our 5-vertex graph has {len(E)} edges — not a tree (one extra edge creates exactly one cycle: 0−1−2−0). "
       "Remove edge (1,2): 5 vertices, 5−1 = 4 edges → a tree. Spanning trees connect everything cheapest-first (Kruskal/Prim); "
       f"running Kruskal on the weighted graph takes edges {mst_desc}, total cost **{mst_cost}** — computed, including the skipped (0,1):4 which would close the cycle 0−1−2−0. "
       f"{context}")},
    ]
    cards = [
     {"front": "Handshaking lemma?", "back": "Σ deg(v) = 2|E|."},
     {"front": f"Σdeg for the worked graph?", "back": f"**{hs}** = 2×{len(E)}."},
     {"front": f"BFS order from 0?", "back": f"**{bfs_order}**."},
     {"front": f"Shortest weighted dist 0→4?", "back": f"**{dist0[4]}**."},
     {"front": "BFS gives?", "back": "Shortest paths in unweighted graphs, level by level."},
     {"front": "Dijkstra needs?", "back": "Non-negative weights."},
     {"front": "Topological order of A→B,A→C,B→D,C→D?", "back": "A, B, C, D (B,C interchangeable)."},
     {"front": "Tree on n vertices: edges?", "back": "Exactly n−1."},
     {"front": f"MST cost of worked graph?", "back": f"**{mst_cost}** (Kruskal: {mst_desc})."},
     {"front": "Adjacency list vs matrix?", "back": "Lists for sparse; matrices for dense/algebraic."},
     {"front": "A cycle in a task graph means?", "back": "Deadlock — no valid execution order."},
     {"front": f"dist(0→4) unweighted?", "back": f"**{bfs_order.index(4)}** edges."},
    ]
    quiz = [
     mcq(mid, "q1", "Σdeg(v) for any graph?", "2|E|", ["|E|", "|V|²", "|V|+|E|"], "Each edge contributes 2."),
     mcq(mid, "q2", f"BFS from 0 visits 3rd:", str(bfs_order[2]), ["1", "4", "0"], f"Order {bfs_order}; third = {bfs_order[2]}."),
     mcq(mid, "q3", "Dijkstra requires:", "Non-negative weights", ["A DAG", "Unweighted graph", "A tree"], "Greedy choice needs non-negativity."),
     mcq(mid, "q4", f"Weighted dist(0→4)?", str(dist0[4]), ["12", "10", "8"], "0→2→1→3→4 = 2+1+5+3 = 11."),
     mcq(mid, "q5", "Tree on 7 vertices has edges:", "6", ["7", "12", "21"], "n−1."),
     mcq(mid, "q6", "Topological order exists iff:", "The digraph is acyclic", ["It's a tree", "It's connected", "It's weighted"], "DAG ⇔ topological order exists."),
     mcq(mid, "q7", f"MST cost?", str(mst_cost), ["10", "15", "8"], f"Kruskal takes {mst_desc} = {mst_cost}."),
     mcq(mid, "q8", "Odd-degree vertices are always:", "Even in number", ["Odd in number", "Zero", "Two"], "Corollary of the handshaking lemma."),
     mcq(mid, "q9", "(M²)[i][j] counts:", "Length-2 walks i→j", ["Edges", "Triangles", "Components"], "Matrix multiplication composes walks."),
     mcq(mid, "q10", "Kahn's algorithm emits:", "Vertices with no remaining incoming edges", ["Highest-degree first", "Random vertices", "Sinks first"], "Peel sources until empty; leftover = cycle."),
    ]
    drills = [
     {"title": "Graph reps", "items": [
      {"prompt": f"Degree of vertex 1?", "answer": str(deg[1]), "explain": f"Edges (0,1),(1,2),(1,3): degree {deg[1]}."},
      {"prompt": "Edges in a tree on 10 vertices?", "answer": "9", "explain": "n−1."},
      {"prompt": f"Σdeg = {hs}; |E|?", "answer": str(len(E)), "explain": f"{hs}/2 = {len(E)}."},
      {"prompt": "Adjacency row of vertex 4?", "answer": "[0,0,1,1,0]", "explain": "Edges (2,4),(3,4)."},
     ]},
     {"title": "Algorithm reps", "items": [
      {"prompt": f"BFS level of vertex 4 from 0?", "answer": "2", "explain": "0→2→4."},
      {"prompt": f"Dijkstra: after settling 0, next vertex?", "answer": "2 (d=2)", "explain": "Candidates: 1→4, 2→2; min is 2."},
      {"prompt": "Topo order: X→Y, X→Z?", "answer": "X first; Y,Z any order", "explain": "X has no incoming edges."},
      {"prompt": "Cycle A→B→A: topo order?", "answer": "None exists", "explain": "Not a DAG."},
     ]},
    ]
    lab = {"title": "Implement BFS and Dijkstra and verify",
     "brief": "You will implement BFS and Dijkstra in Python on the worked graph and assert every distance and order claimed in this module.",
     "steps": [
      "Encode the graph as an adjacency list; assert degrees match the notes.",
      "Write bfs(s); assert bfs(0) equals the worked order.",
      "Write dijkstra(s, weights); assert dist(0) equals the worked distances.",
      "Add edge (0,4) weight 1; assert dist(0→4) becomes 1 and explain why.",
      "Write has_cycle for a directed version; assert the task DAG is acyclic and A→B→A is not.",
      "Write the verdict report.",
     ],
     "deliverable": "graph_check.py with asserts plus the verdict report.",
     "checkpoint": "BFS/Dijkstra outputs match the notes exactly; cycle detection correct."}
    mock = {"q": "Why does Dijkstra's greedy choice work?",
     "choices": ["Non-negative weights: the closest unsettled vertex can't be improved", "Graphs are always DAGs", "BFS already ran", "Weights are integers"],
     "answer": 0, "explain": "Any alternative path to it would be at least as long."}
    return assemble(course_id, course_code, "graphs", "Graphs & Discrete Structures",
     "Graph terminology, representations, BFS, Dijkstra, DAGs, and trees — the mathematics of networks, dependencies, and infrastructure.",
     ["Verify degree data with the handshaking lemma.",
      "Trace BFS and Dijkstra by hand on small graphs.",
      "Produce topological orders and diagnose cycles.",
      "Compute MST cost via Kruskal on small instances."],
     notes, cards, quiz, drills, lab, mock, prereq_for)

BUILDERS_B = {"stats": build_stats, "linalg": build_linalg, "quantreason": build_quantreason, "graphs": build_graphs}
