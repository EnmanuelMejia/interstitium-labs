"""Assemble IL-20 course JSON."""
import json, sys
sys.path.insert(0, "/home/hatch/workspace/apex-audit/docs/university/data/_build")
from il20_a import MODULES_A
from il20_b import MODULES_B

modules = MODULES_A + MODULES_B

SCRIPT_LABS = [
 {
  "id": "lab-matrix-ops",
  "title": "Matrix Ops with NumPy",
  "brief": "Load two matrices, multiply them, and verify the inverse identity: for an invertible A, A @ inv(A) should equal the identity (up to floating-point tolerance).",
  "starter": "import numpy as np\n\nA = np.array([[2., 1.], [1., 3.]])\nB = np.array([[1., 0.], [4., 2.]])\n\n# 1. Multiply A and B\nC = None  # TODO\n\n# 2. Determinant of A\ndetA = None  # TODO\n\n# 3. Inverse of A, then check A @ A_inv ~= identity\nA_inv = None  # TODO\ncheck = None  # TODO: A @ A_inv\n\nprint(\"C =\", C)\nprint(\"det(A) =\", detA)\nprint(\"A @ A_inv =\", check)\n",
  "required": ["np.matmul", "np.linalg.det", "np.linalg.inv"],
  "hint": "np.matmul(A, B) or the @ operator multiplies. np.linalg.det gives the determinant; np.linalg.inv gives the inverse. Compare check against np.eye(2) with np.allclose.",
  "solution": "import numpy as np\n\nA = np.array([[2., 1.], [1., 3.]])\nB = np.array([[1., 0.], [4., 2.]])\n\nC = np.matmul(A, B)\ndetA = np.linalg.det(A)\nA_inv = np.linalg.inv(A)\ncheck = np.matmul(A, A_inv)\n\nprint(\"C =\", C)\nprint(\"det(A) =\", detA)\nprint(\"A @ A_inv =\", check)\nprint(\"close to identity:\", np.allclose(check, np.eye(2)))"
 },
 {
  "id": "lab-monte-carlo",
  "title": "Monte Carlo Estimation of Pi",
  "brief": "Estimate pi by random sampling: throw N uniform points in the unit square and count the fraction landing inside the quarter circle x^2 + y^2 <= 1. That fraction times 4 approximates pi.",
  "starter": "import random\nimport math\n\nN = 200000\ninside = 0\n\nfor _ in range(N):\n    x = random.random()  # uniform in [0, 1)\n    y = random.random()\n    # TODO: test whether (x, y) is inside the quarter circle\n    pass\n\n# TODO: pi estimate = 4 * inside / N\npi_est = None\n\nprint(\"estimate:\", pi_est)\nprint(\"error:\", abs(pi_est - math.pi))\n",
  "required": ["random.random", "inside / N", "4 *"],
  "hint": "A point is inside the quarter circle when x*x + y*y <= 1. Increment inside when true, then pi_est = 4 * inside / N.",
  "solution": "import random\nimport math\n\nN = 200000\ninside = 0\n\nfor _ in range(N):\n    x = random.random()\n    y = random.random()\n    if x * x + y * y <= 1:\n        inside += 1\n\npi_est = 4 * inside / N\n\nprint(\"estimate:\", pi_est)\nprint(\"error:\", abs(pi_est - math.pi))"
 },
 {
  "id": "lab-gradient-descent",
  "title": "Gradient Descent from Scratch",
  "brief": "Minimize f(x) = x^2 + 4x + 6 by gradient descent: iterate x <- x - alpha * f'(x). The true minimum is at x = -2 (complete the square: (x+2)^2 + 2). Track convergence.",
  "starter": "def f(x):\n    return x ** 2 + 4 * x + 6\n\ndef grad(x):\n    # TODO: derivative of f\n    return None\n\nx = 5.0\nALPHA = 0.1\n\nfor step in range(100):\n    # TODO: gradient descent update\n    pass\n\nprint(\"x* =\", x, \" f(x*) =\", f(x))\n# True minimum: x = -2, f = 2\n",
  "required": ["2 * x + 4", "x - ALPHA", "grad(x)"],
  "hint": "f'(x) = 2x + 4. Each step: x = x - ALPHA * grad(x). With ALPHA=0.1 the iterates converge geometrically to -2.",
  "solution": "def f(x):\n    return x ** 2 + 4 * x + 6\n\ndef grad(x):\n    return 2 * x + 4\n\nx = 5.0\nALPHA = 0.1\n\nfor step in range(100):\n    x = x - ALPHA * grad(x)\n\nprint(\"x* =\", x, \" f(x*) =\", f(x))\n# True minimum: x = -2, f = 2"
 },
 {
  "id": "lab-numerical-integration",
  "title": "Trapezoidal & Simpson Integration",
  "brief": "Approximate the integral of sin(x) from 0 to pi (true value 2) with the composite trapezoidal and Simpson rules at several step counts. Verify Simpson converges far faster.",
  "starter": "import math\n\ndef f(x):\n    return math.sin(x)\n\na, b = 0.0, math.pi\nTRUE_VALUE = 2.0\n\ndef trapezoidal(n):\n    # TODO: h/2 * [f0 + 2*f1 + ... + 2*f_{n-1} + fn]\n    return None\n\ndef simpson(n):\n    # TODO: n even; h/3 * [f0 + 4*f1 + 2*f2 + ... + 4*f_{n-1} + fn]\n    return None\n\nfor n in [4, 8, 16, 32]:\n    t = trapezoidal(n)\n    s = simpson(n if n % 2 == 0 else n + 1)\n    print(f\"n={n:3d}  trap err={abs(t-TRUE_VALUE):.2e}  simp err={abs(s-TRUE_VALUE):.2e}\")\n",
  "required": ["h / 2", "h / 3", "4 *", "2 *"],
  "hint": "h = (b-a)/n. Trapezoidal weights: 1,2,2,...,2,1 times h/2. Simpson weights: 1,4,2,4,...,4,1 times h/3 with n even.",
  "solution": "import math\n\ndef f(x):\n    return math.sin(x)\n\na, b = 0.0, math.pi\nTRUE_VALUE = 2.0\n\ndef trapezoidal(n):\n    h = (b - a) / n\n    s = f(a) + f(b)\n    for i in range(1, n):\n        s += 2 * f(a + i * h)\n    return h / 2 * s\n\ndef simpson(n):\n    assert n % 2 == 0\n    h = (b - a) / n\n    s = f(a) + f(b)\n    for i in range(1, n):\n        w = 4 if i % 2 == 1 else 2\n        s += w * f(a + i * h)\n    return h / 3 * s\n\nfor n in [4, 8, 16, 32]:\n    t = trapezoidal(n)\n    s = simpson(n if n % 2 == 0 else n + 1)\n    print(f\"n={n:3d}  trap err={abs(t-TRUE_VALUE):.2e}  simp err={abs(s-TRUE_VALUE):.2e}\")"
 }
]

DRILLS = [
 {"id": "drill-mat-vec", "title": "Matrix-vector product", "prompt": "A = [[1,2],[3,4]], x = [5,6]. Compute Ax.",
  "snippet": "A = [[1,2],[3,4]]\nx = [5,6]",
  "choices": ["[17, 39]", "[5, 24]", "[11, 25]", "[16, 34]"], "answer": 0,
  "explain": "Row 1: 1*5+2*6=17. Row 2: 3*5+4*6=39."},
 {"id": "drill-chain", "title": "Chain rule sprint", "prompt": "d/dx of ln(x^2 + 1)?",
  "snippet": "f(x) = ln(x^2 + 1)",
  "choices": ["1/(x^2+1)", "2x/(x^2+1)", "2x*ln(x^2+1)", "x/(x^2+1)"], "answer": 1,
  "explain": "Outer derivative 1/(x^2+1) times inner derivative 2x."},
 {"id": "drill-bayes", "title": "Bayes sprint", "prompt": "P(B|A)=0.8, P(A)=0.25, P(B)=0.4. P(A|B)?",
  "choices": ["0.5", "0.8", "0.32", "0.2"], "answer": 0,
  "explain": "0.8*0.25/0.4 = 0.2/0.4 = 0.5."},
 {"id": "drill-eigen", "title": "Eigenvalue sprint", "prompt": "Eigenvalues of [[6,0],[0,1]]?",
  "choices": ["6 and 1", "7 and 0", "3 and 2", "6 and 0"], "answer": 0,
  "explain": "Diagonal matrix: eigenvalues are the diagonal entries."},
 {"id": "drill-series", "title": "Series sprint", "prompt": "Does sum 1/n^3 converge?",
  "choices": ["Yes (p-series, p=3>1)", "No (harmonic-like)", "Only conditionally", "Need ratio test"], "answer": 0,
  "explain": "p-series with p=3 > 1 converges absolutely."},
 {"id": "drill-newton", "title": "Newton sprint", "prompt": "One Newton step for f(x)=x^2-3 from x0=2?",
  "choices": ["1.75", "1.732", "2.0", "1.5"], "answer": 0,
  "explain": "x1 = 2 - (4-3)/4 = 2 - 0.25 = 1.75."}
]

SCENARIOS = [
 {
  "id": "sc-root-finding", "title": "Choosing a Root-Finding Method",
  "context": "You must find where a sensor calibration curve f(x) crosses zero on [0, 5]. f is smooth, you can evaluate f and f' cheaply, and you know f(0) < 0 < f(5). A wrong answer ships bad calibrations.",
  "steps": [
   {"prompt": "First decision: which method do you start with?",
    "options": [
     {"text": "Bisection on [0,5] — guaranteed, then polish with Newton", "correct": True, "why": "The sign change guarantees a root exists; bisection brackets it safely, and Newton's method then converges quadratically near the root."},
     {"text": "Newton's method from x=0 immediately", "correct": False, "why": "Newton's method has no global guarantee — a poor start can diverge or cycle. Bracket first."},
     {"text": "Sample f at 1000 points and pick the smallest |f|", "correct": False, "why": "Grid sampling gives no error bound and can miss narrow crossings entirely."}]},
   {"prompt": "After bisection narrows the bracket to width 1e-3, the root is needed to 1e-9. Next step?",
    "options": [
     {"text": "Switch to Newton's method inside the bracket", "correct": True, "why": "Quadratic convergence near a simple root reaches 1e-9 in a few iterations from a 1e-3 bracket."},
     {"text": "Keep bisecting — 30 more halvings", "correct": False, "why": "Works but wasteful: bisection needs ~10 more steps per decimal digit; Newton does it in 2-3."},
     {"text": "Accept 1e-3 as good enough", "correct": False, "why": "The requirement is 1e-9; shipping 1e-3 violates the spec."}]}
  ]
 },
 {
  "id": "sc-which-test", "title": "Which Statistical Test?",
  "context": "Two web-page variants ran for a week: A converted 120/2000 visitors, B converted 150/2000. The team wants to know if B is really better or the gap is noise.",
  "steps": [
   {"prompt": "What is the right first analysis?",
    "options": [
     {"text": "Two-proportion z-test (or chi-square) for the difference", "correct": True, "why": "Two independent binomial proportions — the z-test for difference in proportions (equivalently chi-square) is the standard tool."},
     {"text": "A t-test on the raw conversion counts", "correct": False, "why": "A t-test assumes roughly normal continuous data; these are binary outcomes aggregated as proportions."},
     {"text": "Just ship B — 150 > 120", "correct": False, "why": "The 30-visitor gap may be noise; without a test you cannot separate signal from sampling variation."}]},
   {"prompt": "The test gives p = 0.04. The correct conclusion?",
    "options": [
     {"text": "Reject the null at 5%: evidence B differs from A, and the direction favors B", "correct": True, "why": "p < 0.05 with the observed direction favoring B supports a real difference — while reporting the effect size (1.5 percentage points) and CI."},
     {"text": "There is a 96% chance B is better", "correct": False, "why": "A p-value is not the probability the alternative is true — it is P(data this extreme | null)."},
     {"text": "p = 0.04 is too close to 0.05 to act on", "correct": False, "why": "The pre-chosen alpha was 0.05; moving the goalpost after seeing the data invalidates the test."}]}
  ]
 },
 {
  "id": "sc-optimization-choice", "title": "Formulating an Optimization",
  "context": "A warehouse must assign delivery routes minimizing total fuel cost. Costs are linear in distance, each truck has a capacity limit, every stop must be visited exactly once. 200 stops, 12 trucks.",
  "steps": [
   {"prompt": "How do you frame this problem?",
    "options": [
     {"text": "Mixed-integer linear program (or VRP heuristic) — discrete routing with capacity constraints", "correct": True, "why": "Visit-once + capacity + linear costs is a vehicle-routing / integer-programming structure; gradient descent cannot handle the discrete assignment."},
     {"text": "Gradient descent on a smooth relaxation of the routes", "correct": False, "why": "Routes are discrete permutations; a smooth relaxation loses the visit-once structure and rounds badly."},
     {"text": "Least squares fit of cost vs distance", "correct": False, "why": "That estimates a cost model — it does not choose routes."}]},
   {"prompt": "The MILP solver stalls on 200 stops. What now?",
    "options": [
     {"text": "Use a construction + local-search heuristic (e.g., savings algorithm + 2-opt) and bound the gap", "correct": True, "why": "VRP is NP-hard; industry practice is good heuristics with lower bounds to certify solution quality."},
     {"text": "Reduce to 12 stops so the solver finishes", "correct": False, "why": "Solving a different, smaller problem does not serve the 200 real stops."},
     {"text": "Run gradient descent longer", "correct": False, "why": "The problem is combinatorial, not smooth — more gradient steps solve nothing."}]}
  ]
 }
]

# Mock: reuse module quiz items as timed tasks + add code tasks
mock = []
qid = 0
for m in modules:
    for q in m["quiz"]:
        qid += 1
        mock.append({"id": f"mock-m20-{qid:02d}", "type": "choice",
                     "q": q["q"], "choices": q["choices"],
                     "answer": q["answer"], "explain": q["explain"]})
# 16 modules x 4 = 64 quizzes; keep 44 + 4 code tasks = 48
mock = mock[:44]
for lab in SCRIPT_LABS:
    mock.append({"id": f"mock-{lab['id']}", "type": "code",
                 "prompt": lab["brief"], "starter": lab["starter"],
                 "required": lab["required"], "answer": lab["solution"],
                 "explain": "Model solution shown; scored by required-fragment presence."})

CHEAT_SHEETS = [
 {"title": "Discrete Math Formula Sheet",
  "blocks": [
   {"h": "Sets & logic", "body": "- |P(A)| = 2^|A|\n- De Morgan: (A\u222aB)\u1d9c = A\u1d9c\u2229B\u1d9c; \u00ac(p\u2228q) \u2261 \u00acp\u2227\u00acq\n- p\u2192q false only when p=T, q=F\n- Contrapositive: \u00acq\u2192\u00acp \u2261 p\u2192q"},
   {"h": "Counting", "body": "- P(n,k) = n!/(n\u2212k)! (ordered)\n- C(n,k) = n!/(k!(n\u2212k)!) (unordered)\n- (x+y)\u207f = \u03a3C(n,k)x\u207f\u207bk y\u1d4f\n- Pigeonhole: n+1 items, n boxes \u21d2 collision"},
   {"h": "Graphs", "body": "- \u03a3deg(v) = 2|E|\n- Tree on n vertices: n\u22121 edges\n- K\u2099 has n(n\u22121)/2 edges\n- BFS: queue, shortest path; DFS: stack, cycles/topo"}]},
 {"title": "Linear Algebra Formula Sheet",
  "blocks": [
   {"h": "Core identities", "body": "- (AB)\u1d5b = B\u1d5bA\u1d5b; (AB)\u207b\u00b9 = B\u207b\u00b9A\u207b\u00b9\n- det(AB) = det(A)det(B); det\u22600 \u21d4 invertible\n- 2\u00d72 inverse: 1/(ad\u2212bc)\u00b7[[d,\u2212b],[\u2212c,a]]"},
   {"h": "Eigen", "body": "- det(A\u2212\u03bbI) = 0 \u21d2 eigenvalues\n- trace = \u03a3\u03bb\u1d62; det = \u220f\u03bb\u1d62\n- Symmetric \u21d2 real eigenvalues, orthonormal eigenbasis\n- A=PDP\u207b\u00b9 \u21d2 A\u1d4f=PD\u1d4fP\u207b\u00b9"},
   {"h": "Geometry", "body": "- u\u00b7v = |u||v|cos\u03b8; |v|=\u221a(v\u00b7v)\n- proj_v(u) = ((u\u00b7v)/(v\u00b7v))v\n- Rank = # independent rows/cols"}]},
 {"title": "Calculus Formula Sheet",
  "blocks": [
   {"h": "Derivatives", "body": "- (uv)'=u'v+uv'; (u/v)'=(u'v\u2212uv')/v\u00b2; [f(g)]'=f'(g)g'\n- (e\u02e3)'=e\u02e3; (ln x)'=1/x; (sin x)'=cos x; (cos x)'=\u2212sin x\n- l'H\u00f4pital for 0/0, \u221e/\u221e"},
   {"h": "Integrals", "body": "- \u222b[a\u2192b]f = F(b)\u2212F(a)\n- \u222bu dv = uv \u2212 \u222bv du (LIATE)\n- Avg value: (1/(b\u2212a))\u222bf"},
   {"h": "Series", "body": "- e\u02e3=\u03a3x\u207f/n!; sin x=\u03a3(\u22121)\u207fx^(2n+1)/(2n+1)!; cos x=\u03a3(\u22121)\u207fx^(2n)/(2n)!\n- 1/(1\u2212x)=\u03a3x\u207f (|x|<1)\n- p-series converges iff p>1; ratio test L<1"}]},
 {"title": "Probability & Statistics Sheet",
  "blocks": [
   {"h": "Probability", "body": "- P(A|B)=P(A\u2229B)/P(B); Bayes: P(A|B)=P(B|A)P(A)/P(B)\n- E[aX+bY]=aE[X]+bE[Y]; Var=E[X\u00b2]\u2212E[X]\u00b2\n- Binomial: E=np, Var=np(1\u2212p)\n- 68\u201395\u201399.7 rule for normal"},
   {"h": "Statistics", "body": "- SE of mean = \u03c3/\u221an\n- 95% CI: x\u0304 \u00b1 1.96\u00b7\u03c3/\u221an\n- p-value = P(data this extreme | H\u2080)\n- CI width \u221d 1/\u221an"}]},
 {"title": "Numerical Methods Sheet",
  "blocks": [
   {"h": "Root finding", "body": "- Bisection error \u2264 (b\u2212a)/2\u207f\n- Newton: x\u2099\u208a\u2081 = x\u2099 \u2212 f/f' (quadratic near simple root)"},
   {"h": "Quadrature", "body": "- Trapezoid: h/2[1,2,\u2026,2,1], err O(h\u00b2)\n- Simpson: h/3[1,4,2,\u2026,4,1] (n even), err O(h\u2074)"},
   {"h": "Linear systems", "body": "- Elimination O(n\u00b3); LU then O(n\u00b2)/solve\n- Normal equations: A\u1d5bAx=A\u1d5bb (prefer QR)\n- Gradient descent: x\u2190x\u2212\u03b1\u2207f"}]}
]

ANSWER_BANK = [
 {"q": "Prove: the sum of two odd integers is even.", "a": "Write them as 2k+1 and 2m+1. Sum = 2k+2m+2 = 2(k+m+1), which is twice an integer \u2014 even by definition. This is a direct proof: unpack the definition, do algebra, repack."},
 {"q": "Compute the inverse of [[2,1],[1,3]] and verify.", "a": "det = 2\u00b73\u22121\u00b71 = 5. Inverse = (1/5)[[3,\u22121],[\u22121,2]]. Verify: [[2,1],[1,3]]\u00b7(1/5)[[3,\u22121],[\u22121,2]] = (1/5)[[5,0],[0,5]] = I."},
 {"q": "Find the eigenvalues of [[4,1],[2,3]].", "a": "det(A\u2212\u03bbI) = (4\u2212\u03bb)(3\u2212\u03bb)\u22122 = \u03bb\u00b2\u22127\u03bb+10 = (\u03bb\u22125)(\u03bb\u22122). Eigenvalues 5 and 2; trace 7 = sum, det 10 = product \u2014 checks out."},
 {"q": "Evaluate \u222b[0\u2192\u03c0] x\u00b7sin x dx.", "a": "Parts: u=x, dv=sin x dx \u21d2 du=dx, v=\u2212cos x. [\u2212x cos x]\u2080^\u03c0 + \u222b[0\u2192\u03c0]cos x dx = \u03c0 + [sin x]\u2080^\u03c0 = \u03c0 + 0 = \u03c0."},
 {"q": "A fair coin is flipped 100 times; approximate P(heads \u2265 60).", "a": "Binomial(100, 0.5): \u03bc=50, \u03c3=5. CLT: Z=(60\u221250)/5=2 \u21d2 P(Z\u22652)\u22480.0228 (about 2.3%). With continuity correction, P(X\u226559.5): Z=1.9 \u2248 2.9%."},
 {"q": "Why does gradient descent need a small learning rate?", "a": "The update x\u2212\u03b1\u2207f overshoots when \u03b1 is large relative to the curvature: for convex quadratic with max curvature L, convergence needs \u03b1 < 2/L. Too large \u21d2 oscillation/divergence; too small \u21d2 slow but steady."}
]

SOURCE_LINKS = [
 {"name": "Wikipedia \u2014 Linear algebra", "url": "https://en.wikipedia.org/wiki/Linear_algebra", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Mathematical proof", "url": "https://en.wikipedia.org/wiki/Mathematical_proof", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Calculus", "url": "https://en.wikipedia.org/wiki/Calculus", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Probability theory", "url": "https://en.wikipedia.org/wiki/Probability_theory", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Numerical analysis", "url": "https://en.wikipedia.org/wiki/Numerical_analysis", "retrieved": "2026-10-07"},
 {"name": "NumPy documentation", "url": "https://numpy.org/doc/", "retrieved": "2026-10-07"},
 {"name": "Khan Academy \u2014 Math library", "url": "https://www.khanacademy.org/math", "retrieved": "2026-10-07"},
 {"name": "MIT OpenCourseWare \u2014 Linear Algebra (Strang)", "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", "retrieved": "2026-10-07"}
]

doc = {
 "schemaVersion": "1.0",
 "courseId": "il-20-mathematics",
 "code": "IL-20",
 "title": "Mathematics for Engineers & Scientists",
 "tagline": "The mathematical spine of engineering: discrete structures, linear algebra, calculus, probability, and numerical computation.",
 "blurb": "Sixteen modules covering the mathematics working engineers and scientists actually use: sets and logic, proof methods, combinatorics, linear algebra through eigenvalues, single- and multi-variable calculus, series, probability, statistics, graphs, and numerical methods. Every module pairs definitions and theorems with worked examples, flashcards, and quick-check quizzes; four Python labs make the math executable (NumPy matrix ops, Monte Carlo estimation, gradient descent, numerical quadrature). Original practice content; confers no certificate.",
 "hours": 72,
 "updatedAt": "2026-10-07",
 "objectives": [
  "Reason with sets, logic, and proof: direct, contrapositive, contradiction, induction",
  "Count with combinatorics and model discrete structure with graphs and recurrences",
  "Compute with vectors and matrices: products, determinants, inverses, eigenvalues",
  "Differentiate and integrate single- and multi-variable functions; expand Taylor series",
  "Reason under uncertainty: probability, Bayes, expectation, confidence intervals, hypothesis tests",
  "Solve numerically: bisection, Newton, quadrature, linear systems, gradient descent"
 ],
 "arc": [
  {"phase": "Phase 1 \u2014 Discrete foundations", "title": "Speak mathematics", "body": "Sets, logic, proofs, counting, relations, and graphs: the language and the discrete structures. Modules 1\u20134 and 14."},
  {"phase": "Phase 2 \u2014 Continuous machinery", "title": "Compute with structure", "body": "Linear algebra (modules 5\u20137), calculus (8\u201311): the vector/matrix engine and the mathematics of change and accumulation."},
  {"phase": "Phase 3 \u2014 Uncertainty & approximation", "title": "Decide with data", "body": "Probability, statistics (12\u201313), numerical methods and optimization (15\u201316): inference and computation when closed forms fail."}
 ],
 "priorities": [
  {"label": "Linear algebra core (modules 5\u20137)", "minutes": 540},
  {"label": "Calculus core (modules 8\u201311)", "minutes": 660},
  {"label": "Probability & statistics (12\u201313)", "minutes": 420},
  {"label": "Discrete & proofs (1\u20134, 14)", "minutes": 480},
  {"label": "Numerical methods & optimization (15\u201316)", "minutes": 360},
  {"label": "Labs + mock assessment", "minutes": 420}
 ],
 "battlePlan": [
  {"id": "bp20-1", "title": "Complete discrete foundations (modules 1\u20134): notes, cards, quizzes", "minutes": 360},
  {"id": "bp20-2", "title": "Complete linear algebra I\u2013III (modules 5\u20137) + matrix-ops lab", "minutes": 540},
  {"id": "bp20-3", "title": "Complete calculus I\u2013II + series + multivariable (modules 8\u201311)", "minutes": 660},
  {"id": "bp20-4", "title": "Complete probability + statistics (modules 12\u201313) + Monte Carlo lab", "minutes": 420},
  {"id": "bp20-5", "title": "Complete graphs/recurrences + numerical methods + optimization (14\u201316)", "minutes": 480},
  {"id": "bp20-6", "title": "Finish gradient-descent + quadrature labs and all three scenarios", "minutes": 300},
  {"id": "bp20-7", "title": "Sit the 48-task timed mock; review every miss against the cheat sheets", "minutes": 180}
 ],
 "modules": modules,
 "scriptLabs": SCRIPT_LABS,
 "drills": DRILLS,
 "scenarios": SCENARIOS,
 "trainers": [],
 "mockMinutes": 120,
 "mockTasks": mock,
 "cheatSheets": CHEAT_SHEETS,
 "answerBank": ANSWER_BANK,
 "sourceLinks": SOURCE_LINKS,
 "honestyNote": "Original instructional content written for this course \u2014 standard mathematics, no invented theorems. Practice material only; confers no certificate and is not affiliated with any university or vendor."
}

out = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-20-mathematics.json"
with open(out, "w") as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", out, "modules:", len(modules), "mock:", len(mock))
