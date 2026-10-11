"""IL-20 modules 9-16 (calculus II through optimization)."""
MODULES_B = [
{
 "id": "m20-calculus-2", "code": "IL-20", "title": "Calculus II \u2014 Integration",
 "weight": 1,
 "summary": "Antiderivatives, the Fundamental Theorem, integration techniques, and improper integrals \u2014 accumulation made rigorous.",
 "objectives": ["State and apply the Fundamental Theorem of Calculus", "Integrate by substitution and by parts", "Evaluate improper integrals via limits", "Compute areas, volumes, and averages with integrals"],
 "notes": [
  {"title": "The Fundamental Theorem",
   "body": "**FTC Part 1**: if F(x) = \u222b[a\u2192x] f(t) dt, then F'(x) = f(x) \u2014 differentiation undoes accumulation. **FTC Part 2**: `\u222bx[a\u2192b] f = F(b) \u2212 F(a)` for any antiderivative F. This is why we can evaluate definite integrals by finding antiderivatives instead of Riemann sums."},
  {"title": "Techniques",
   "body": "**Substitution**: `\u222b f(g(x)) g'(x) dx = \u222b f(u) du` with u = g(x) \u2014 the chain rule in reverse. **Integration by parts**: `\u222b u dv = uv \u2212 \u222b v du` \u2014 choose u by LIATE priority (Log, Inverse trig, Algebraic, Trig, Exponential). **Partial fractions** split rational functions into integrable pieces."},
  {"title": "Improper integrals",
   "body": "Integrals over infinite intervals or with singularities are defined by **limits**: `\u222b[1\u2192\u221e] (1/x\u00b2) dx = lim(b\u2192\u221e) [1 \u2212 1/b] = 1` \u2014 converges. But `\u222b[1\u2192\u221e] (1/x) dx` diverges (grows like ln b). Always split at each singularity and take limits separately."},
  {"title": "Applications",
   "body": "Area between curves: `\u222b (top \u2212 bottom) dx`. Volume of revolution (disks): `\u03c0\u222b [f(x)]\u00b2 dx`. **Average value** of f on [a,b]: `(1/(b\u2212a)) \u222b[a\u2192b] f`. Expected value in probability is exactly this idea with a density function."}
 ],
 "cards": [
  {"front": "FTC Part 2?", "back": "\u222b[a\u2192b] f = F(b) \u2212 F(a) for any antiderivative F."},
  {"front": "Integration by parts formula?", "back": "\u222b u dv = uv \u2212 \u222b v du."},
  {"front": "LIATE order for choosing u?", "back": "Logarithmic, Inverse trig, Algebraic, Trigonometric, Exponential."},
  {"front": "Does \u222b[1\u2192\u221e] dx/x converge?", "back": "No \u2014 it diverges like ln b."},
  {"front": "Average value of f on [a,b]?", "back": "(1/(b\u2212a)) \u222b[a\u2192b] f(x) dx."}
 ],
 "quiz": [
  {"q": "\u222b x\u00b7e\u02e3 dx =",
   "choices": ["xe\u02e3 + C", "(x\u22121)e\u02e3 + C", "x\u00b2e\u02e3/2 + C", "e\u02e3 + C"],
   "answer": 1,
   "explain": "Parts with u=x, dv=e\u02e3dx: xe\u02e3 \u2212 \u222be\u02e3dx = (x\u22121)e\u02e3 + C."},
  {"q": "\u222b[0\u2192\u03c0] sin x dx =",
   "choices": ["0", "1", "2", "\u03c0"],
   "answer": 2,
   "explain": "[\u2212cos x]\u2080^\u03c0 = \u2212cos(\u03c0) + cos(0) = 1 + 1 = 2."},
  {"q": "d/dx \u222b[2\u2192x\u00b2] e^t dt =",
   "choices": ["e^(x\u00b2)", "2xe^(x\u00b2)", "e^(x\u00b2) \u2212 e\u00b2", "2x"],
   "answer": 1,
   "explain": "FTC Part 1 + chain rule: e^(x\u00b2) \u00b7 d/dx(x\u00b2) = 2xe^(x\u00b2)."},
  {"q": "Average value of f(x) = x\u00b2 on [0,2]?",
   "choices": ["2", "4/3", "8/3", "4"],
   "answer": 1,
   "explain": "(1/2)\u222b[0\u21922] x\u00b2 dx = (1/2)(8/3) = 4/3."}
 ]
},
{
 "id": "m20-series", "code": "IL-20", "title": "Sequences & Series",
 "weight": 1,
 "summary": "Convergence tests, power series, and Taylor expansions \u2014 how functions become computable polynomials.",
 "objectives": ["Test series for convergence with the standard tests", "Find radius and interval of convergence", "Write Taylor/Maclaurin series for elementary functions", "Estimate error with Taylor's remainder"],
 "notes": [
  {"title": "Convergence tests",
   "body": "**Divergence test**: if a\u2099 \u21db 0, \u03a3a\u2099 diverges. **Integral test**: compare \u03a3f(n) with \u222bf. **p-series** \u03a31/n\u1d56 converges iff p > 1. **Ratio test**: L = lim |a\u2099\u208a\u2081/a\u2099|; L<1 converges, L>1 diverges, L=1 inconclusive. **Alternating series test**: decreasing terms \u2192 0 implies convergence."},
  {"title": "Power series",
   "body": "`\u03a3 c\u2099(x\u2212a)\u207f` converges on an interval around a. The **ratio test** gives the **radius of convergence** R: converge for |x\u2212a|<R, diverge outside; check endpoints individually. Example: `\u03a3 x\u207f/n!` has R = \u221e."},
  {"title": "Taylor series",
   "body": "`f(x) = \u03a3 f\u207f(a)/n! \u00b7 (x\u2212a)\u207f`. Maclaurin (a=0) essentials: `e\u02e3 = \u03a3 x\u207f/n!`; `sin x = \u03a3 (\u22121)\u207f x^(2n+1)/(2n+1)!`; `cos x = \u03a3 (\u22121)\u207f x^(2n)/(2n)!`; `1/(1\u2212x) = \u03a3 x\u207f` for |x|<1; `ln(1+x) = \u03a3 (\u22121)\u207f\u207a\u00b9 x\u207f/n` for |x|<1, x\u2260\u22121."},
  {"title": "Error bounds",
   "body": "**Taylor's inequality**: |R\u2099(x)| \u2264 M|x\u2212a|\u207f\u207a\u00b9/(n+1)! where M bounds |f\u207f\u207a\u00b9|. This is how calculators guarantee digits: pick n so the bound beats your tolerance. Alternating series have an even simpler bound \u2014 the error is at most the first dropped term."}
 ],
 "cards": [
  {"front": "p-series \u03a31/n\u1d56: when does it converge?", "back": "Converges iff p > 1."},
  {"front": "Ratio test decision rule?", "back": "L<1 converges; L>1 diverges; L=1 inconclusive."},
  {"front": "Maclaurin series of e\u02e3, sin x, cos x?", "back": "e\u02e3=\u03a3x\u207f/n!; sin x=\u03a3(\u22121)\u207fx^(2n+1)/(2n+1)!; cos x=\u03a3(\u22121)\u207fx^(2n)/(2n)!."},
  {"front": "Radius of convergence: how found?", "back": "Ratio test on |a\u2099\u208a\u2081/a\u2099|; check endpoints separately."},
  {"front": "Alternating series error bound?", "back": "|error| \u2264 first omitted term."}
 ],
 "quiz": [
  {"q": "\u03a3 1/n\u00b2 converges because:",
   "choices": ["Terms go to zero", "It is a p-series with p=2>1", "Ratio test gives L=1/2", "It is geometric"],
   "answer": 1,
   "explain": "p-series with p=2 > 1 converges. (Terms \u2192 0 is necessary, not sufficient.)"},
  {"q": "Radius of convergence of \u03a3 x\u207f/n!?",
   "choices": ["1", "e", "0", "\u221e"],
   "answer": 3,
   "explain": "|a\u2099\u208a\u2081/a\u2099| = 1/(n+1) \u2192 0 < 1 for all x."},
  {"q": "Coefficient of x\u00b3 in the Maclaurin series of sin x?",
   "choices": ["1/6", "\u22121/6", "1/3", "\u22121/2"],
   "answer": 1,
   "explain": "sin x = x \u2212 x\u00b3/3! + \u2026 = x \u2212 x\u00b3/6 + \u2026."},
  {"q": "\u03a3 (\u22121)\u207f/n (n\u22651) converges:",
   "choices": ["Absolutely", "Conditionally", "Diverges", "Only for even n"],
   "answer": 1,
   "explain": "Alternating harmonic series: converges by AST, but \u03a31/n diverges \u2014 conditional."}
 ]
},
{
 "id": "m20-multivariable", "code": "IL-20", "title": "Multivariable Calculus",
 "weight": 1,
 "summary": "Partial derivatives, gradients, the chain rule in higher dimensions, and optimization of functions of several variables.",
 "objectives": ["Compute partial derivatives and gradients", "Use the gradient for direction of steepest ascent", "Find and classify critical points of f(x,y)", "Apply Lagrange multipliers for constrained optimization"],
 "notes": [
  {"title": "Partial derivatives and the gradient",
   "body": "`\u2202f/\u2202x` treats other variables as constants. The **gradient** `\u2207f = \u27e8f_x, f_y, f_z\u27e9` points in the direction of **steepest increase**; its magnitude is the slope in that direction. The **directional derivative** in unit direction u is `D_u f = \u2207f \u00b7 u`."},
  {"title": "Chain rule and differentials",
   "body": "If z = f(x,y) with x(t), y(t): `dz/dt = f_x dx/dt + f_y dy/dt`. The **total differential** `dz = f_x dx + f_y dy` is the linear approximation \u2014 the seed of error propagation: small input errors scale by the partial derivatives."},
  {"title": "Critical points in 2D",
   "body": "Critical point: `\u2207f = 0` (or undefined). **Second derivative test** with `D = f_xx f_yy \u2212 (f_xy)\u00b2`: D>0 and f_xx>0 \u21d2 min; D>0 and f_xx<0 \u21d2 max; D<0 \u21d2 **saddle point**; D=0 inconclusive. Saddles are the generic obstacle in neural-network training."},
  {"title": "Lagrange multipliers",
   "body": "To optimize f(x,y) subject to g(x,y)=c, solve `\u2207f = \u03bb\u2207g` together with the constraint. Geometrically: at the optimum the level curves are tangent. Example: maximize xy subject to x+y=10 \u21d2 \u27e81/y\u27e9... solving gives x=y=5, value 25."}
 ],
 "cards": [
  {"front": "Gradient \u2207f and what it means?", "back": "\u27e8f_x,f_y,f_z\u27e9 \u2014 direction of steepest increase of f."},
  {"front": "Directional derivative D_u f?", "back": "\u2207f \u00b7 u for unit vector u."},
  {"front": "Second derivative test in 2D (D test)?", "back": "D=f_xx f_yy\u2212f_xy\u00b2: D>0,f_xx>0 min; D>0,f_xx<0 max; D<0 saddle."},
  {"front": "Lagrange multiplier setup?", "back": "\u2207f = \u03bb\u2207g plus constraint g(x,y)=c."},
  {"front": "Chain rule: dz/dt for z=f(x(t),y(t))?", "back": "dz/dt = f_x dx/dt + f_y dy/dt."}
 ],
 "quiz": [
  {"q": "f(x,y) = x\u00b2y + y\u00b3. \u2202f/\u2202x =",
   "choices": ["2xy + 3y\u00b2", "2xy", "x\u00b2 + 3y\u00b2", "2x + 3y\u00b2"],
   "answer": 1,
   "explain": "Treat y as constant: derivative of x\u00b2y is 2xy; y\u00b3 is constant w.r.t. x."},
  {"q": "Gradient of f(x,y) = x\u00b2 + y\u00b2 at (1,2)?",
   "choices": ["\u27e81,2\u27e9", "\u27e82,4\u27e9", "\u27e82,2\u27e9", "\u27e85,0\u27e9"],
   "answer": 1,
   "explain": "\u2207f = \u27e82x, 2y\u27e9 = \u27e82,4\u27e9 at (1,2)."},
  {"q": "f(x,y)=x\u00b2\u2212y\u00b2 at (0,0) is a:",
   "choices": ["Local max", "Local min", "Saddle point", "Global min"],
   "answer": 2,
   "explain": "f_xx=2, f_yy=\u22122, f_xy=0 \u21d2 D = \u22124 < 0 \u2014 saddle."},
  {"q": "Maximize f=xy subject to x+y=10 (x,y\u22650):",
   "choices": ["25 at (5,5)", "50 at (10,0)", "20 at (4,6)", "100 at (10,10)"],
   "answer": 0,
   "explain": "Lagrange: y=\u03bb, x=\u03bb \u21d2 x=y=5, f=25. (10,10) violates the constraint."}
 ]
},
{
 "id": "m20-probability", "code": "IL-20", "title": "Probability",
 "weight": 1,
 "summary": "Axioms, conditional probability, Bayes' theorem, random variables, and expectation \u2014 reasoning under uncertainty.",
 "objectives": ["Apply the probability axioms and counting to probability", "Compute conditional probabilities and use Bayes' theorem", "Find expectation and variance of a random variable", "Work with the binomial and normal distributions"],
 "notes": [
  {"title": "Axioms and basic rules",
   "body": "**Kolmogorov axioms**: P(A) \u2265 0; P(S) = 1; disjoint events add. Consequences: P(A\u1d9c) = 1 \u2212 P(A); **addition rule** P(A\u222aB) = P(A)+P(B)\u2212P(A\u2229B). Two events are **independent** iff P(A\u2229B) = P(A)P(B) \u2014 independence is a property of the probability measure, not of intuition."},
  {"title": "Conditional probability and Bayes",
   "body": "`P(A|B) = P(A\u2229B)/P(B)`. **Law of total probability**: P(B) = \u03a3 P(B|A\u1d62)P(A\u1d62). **Bayes' theorem**: `P(A|B) = P(B|A)P(A)/P(B)` \u2014 update prior belief P(A) with evidence B. Base-rate neglect (ignoring P(A)) is the classic applied error: a 99%-accurate test on a 1-in-10,000 condition still yields mostly false positives."},
  {"title": "Random variables, expectation, variance",
   "body": "A **random variable** X maps outcomes to numbers. **Expectation** E[X] = \u03a3 x\u1d62P(X=x\u1d62) (discrete) or \u222b x f(x)dx (continuous) \u2014 the long-run average. Linearity: E[aX+bY] = aE[X]+bE[Y] even when dependent. **Variance** Var(X) = E[(X\u2212E[X])\u00b2] = E[X\u00b2]\u2212E[X]\u00b2; standard deviation \u03c3 = \u221aVar."},
  {"title": "Binomial and normal",
   "body": "**Binomial**(n,p): P(X=k) = C(n,k)p\u1d4f(1\u2212p)\u207f\u207b\u1d4f; E[X]=np, Var=np(1\u2212p). **Normal** N(\u03bc,\u03c3\u00b2): the bell curve; the **68\u201395\u201399.7 rule** for \u00b11,2,3 \u03c3. Standardize with Z = (X\u2212\u03bc)/\u03c3. The normal is the limit of sums \u2014 which is the Central Limit Theorem, next module."}
 ],
 "cards": [
  {"front": "Bayes' theorem?", "back": "P(A|B) = P(B|A)P(A)/P(B)."},
  {"front": "When are A and B independent?", "back": "P(A\u2229B) = P(A)P(B)."},
  {"front": "Linearity of expectation?", "back": "E[aX+bY] = aE[X]+bE[Y], even if dependent."},
  {"front": "Variance formula (computational)?", "back": "Var(X) = E[X\u00b2] \u2212 E[X]\u00b2."},
  {"front": "Binomial(n,p): mean and variance?", "back": "E[X]=np, Var(X)=np(1\u2212p)."},
  {"front": "68\u201395\u201399.7 rule?", "back": "For normal data: ~68% within 1\u03c3, ~95% within 2\u03c3, ~99.7% within 3\u03c3 of the mean."}
 ],
 "quiz": [
  {"q": "A test is 99% accurate; 1 in 1000 people have the condition. P(condition | positive) \u2248",
   "choices": ["99%", "50%", "9%", "0.1%"],
   "answer": 2,
   "explain": "Bayes: (0.99\u00b70.001)/(0.99\u00b70.001 + 0.01\u00b70.999) \u2248 0.00099/0.01098 \u2248 9%. Base rates dominate."},
  {"q": "Roll two fair dice. P(sum = 7)?",
   "choices": ["1/6", "7/36", "1/12", "5/36"],
   "answer": 0,
   "explain": "6 of 36 outcomes: (1,6),(2,5),...,(6,1). 6/36 = 1/6."},
  {"q": "X takes values 1,2,3 with probabilities 0.2,0.5,0.3. E[X] =",
   "choices": ["2.0", "2.1", "2.2", "1.8"],
   "answer": 1,
   "explain": "1(0.2)+2(0.5)+3(0.3) = 0.2+1.0+0.9 = 2.1."},
  {"q": "If P(A)=0.4, P(B)=0.5, and A,B independent, P(A\u222aB) =",
   "choices": ["0.9", "0.2", "0.7", "0.45"],
   "answer": 2,
   "explain": "0.4+0.5\u22120.4\u00b70.5 = 0.9\u22120.2 = 0.7."}
 ]
},
{
 "id": "m20-statistics", "code": "IL-20", "title": "Statistics",
 "weight": 1,
 "summary": "Sampling, the Central Limit Theorem, confidence intervals, and hypothesis testing \u2014 inference from data to populations.",
 "objectives": ["Explain the Central Limit Theorem and its conditions", "Construct and interpret a confidence interval", "Run a hypothesis test and interpret the p-value correctly", "Distinguish correlation from causation"],
 "notes": [
  {"title": "Sampling and the CLT",
   "body": "A **statistic** (e.g., sample mean x\u0304) estimates a **parameter** (\u03bc). The **Central Limit Theorem**: for iid samples with mean \u03bc and finite variance \u03c3\u00b2, x\u0304 is approximately N(\u03bc, \u03c3\u00b2/n) for large n \u2014 regardless of the population's shape. Standard error of the mean = \u03c3/\u221an. This is why averages of enough data behave normally."},
  {"title": "Confidence intervals",
   "body": "A 95% CI for \u03bc: `x\u0304 \u00b1 z*\u00b7\u03c3/\u221an` (z* \u2248 1.96; use t* for small n or estimated \u03c3). Correct interpretation: **95% of intervals constructed this way capture the true \u03bc** \u2014 not 'there is a 95% chance \u03bc is in this interval.' Width shrinks as 1/\u221an: quadrupling the sample halves the width."},
  {"title": "Hypothesis testing",
   "body": "H\u2080 (null) vs H\u2081 (alternative). The **p-value** = P(data this extreme | H\u2080 true) \u2014 **not** P(H\u2080 true | data). Reject H\u2080 if p < \u03b1 (often 0.05). **Type I error**: rejecting a true H\u2080 (rate \u03b1). **Type II error**: missing a real effect; **power** = 1 \u2212 P(Type II). Practical significance \u2260 statistical significance."},
  {"title": "Correlation is not causation",
   "body": "Correlation measures linear association (\u22121 \u2264 r \u2264 1). Confounders, reverse causation, and selection effects produce correlations without causation. The honest pipeline: randomize (experiments), control (regression), or instrument \u2014 and report effect sizes with uncertainty, not just p-values."}
 ],
 "cards": [
  {"front": "Central Limit Theorem (statement)?", "back": "Sample means of iid data with finite variance are approx. normal: x\u0304 ~ N(\u03bc, \u03c3\u00b2/n) for large n."},
  {"front": "Correct interpretation of a 95% CI?", "back": "95% of such intervals capture the true parameter \u2014 a property of the procedure, not of this interval."},
  {"front": "What is a p-value?", "back": "P(data at least this extreme | H\u2080 true). Not P(H\u2080 is true)."},
  {"front": "Type I vs Type II error?", "back": "Type I: false positive (reject true H\u2080). Type II: false negative (miss a real effect)."},
  {"front": "How does CI width scale with sample size?", "back": "Proportional to 1/\u221an \u2014 4\u00d7 data halves the width."},
  {"front": "z* for a 95% CI?", "back": "\u22481.96."}
 ],
 "quiz": [
  {"q": "A 95% CI for \u03bc is (4.1, 5.9). The correct reading is:",
   "choices": ["P(4.1<\u03bc<5.9)=0.95", "95% of intervals from this procedure contain \u03bc", "\u03bc is definitely between 4.1 and 5.9", "The sample mean is 5.9"],
   "answer": 1,
   "explain": "Frequentist CIs describe the procedure's long-run capture rate, not a probability about this fixed interval."},
  {"q": "p = 0.03 with \u03b1 = 0.05. Decision?",
   "choices": ["Fail to reject H\u2080", "Reject H\u2080", "Accept H\u2080", "Increase \u03b1"],
   "answer": 1,
   "explain": "p < \u03b1 \u21d2 reject the null at the 5% level."},
  {"q": "Standard error of the mean for \u03c3=10, n=100?",
   "choices": ["10", "1", "0.1", "100"],
   "answer": 1,
   "explain": "\u03c3/\u221an = 10/10 = 1."},
  {"q": "Two variables correlate at r=0.9. This proves:",
   "choices": ["One causes the other", "Strong linear association only", "A third variable is involved", "The relationship is nonlinear"],
   "answer": 1,
   "explain": "Correlation alone never establishes causation \u2014 confounders and reverse causation remain open."}
 ]
},
{
 "id": "m20-graphs-recurrence", "code": "IL-20", "title": "Graphs & Recurrences",
 "weight": 1,
 "summary": "Graph terminology, trees, traversal orders, and solving recurrence relations \u2014 the discrete structures behind networks and algorithms.",
 "objectives": ["Use graph vocabulary: degree, path, cycle, connectivity", "Characterize trees and count their edges", "Trace BFS and DFS orders", "Solve linear recurrences (Fibonacci, divide-and-conquer)"],
 "notes": [
  {"title": "Graph basics",
   "body": "A **graph** G=(V,E): vertices and edges. **Degree** of v = incident edges. **Handshaking lemma**: \u03a3 deg(v) = 2|E| \u2014 every edge contributes 2. A **path** with no repeated vertices; a **cycle** returns to start. **Connected** = a path exists between every pair. A **complete graph** K\u2099 has n(n\u22121)/2 edges."},
  {"title": "Trees",
   "body": "A **tree** is a connected acyclic graph. Equivalent characterizations: connected with n\u22121 edges; acyclic with n\u22121 edges; exactly one simple path between any two vertices. A **spanning tree** of G is a tree on all of G's vertices \u2014 minimum spanning trees (Kruskal/Prim) minimize total edge weight."},
  {"title": "BFS and DFS",
   "body": "**BFS** (queue): explores level by level \u2014 finds shortest paths in unweighted graphs. **DFS** (stack/recursion): goes deep first \u2014 detects cycles, produces topological orderings. Both visit each vertex and edge once: O(V+E). Choose BFS for shortest-path, DFS for structure (components, cycles, topo sort)."},
  {"title": "Recurrence relations",
   "body": "Define sequences by earlier terms: Fibonacci `F\u2099 = F\u2099\u208b\u2081 + F\u2099\u208b\u2082`, F\u2080=0, F\u2081=1. **Linear recurrences** with constant coefficients solve via the **characteristic equation**: for a\u2099 = c\u2081a\u2099\u208b\u2081 + c\u2082a\u2099\u208b\u2082, solve r\u00b2 = c\u2081r + c\u2082. Divide-and-conquer recurrences like T(n) = 2T(n/2)+n solve to \u0398(n log n) \u2014 the Master Theorem generalizes this."}
 ],
 "cards": [
  {"front": "Handshaking lemma?", "back": "\u03a3 deg(v) = 2|E|."},
  {"front": "Three equivalent definitions of a tree?", "back": "Connected + acyclic; connected with n\u22121 edges; unique simple path between any two vertices."},
  {"front": "BFS vs DFS: data structure and use?", "back": "BFS: queue, shortest paths unweighted. DFS: stack/recursion, cycles and topological order."},
  {"front": "Fibonacci recurrence and base cases?", "back": "F\u2099=F\u2099\u208b\u2081+F\u2099\u208b\u2082, F\u2080=0, F\u2081=1."},
  {"front": "T(n)=2T(n/2)+n solves to?", "back": "\u0398(n log n) \u2014 mergesort's recurrence."},
  {"front": "Edges in K\u2099 (complete graph)?", "back": "n(n\u22121)/2."}
 ],
 "quiz": [
  {"q": "A tree on 12 vertices has how many edges?",
   "choices": ["12", "11", "13", "66"],
   "answer": 1,
   "explain": "Any tree on n vertices has exactly n\u22121 edges."},
  {"q": "Sum of degrees in a graph with 9 edges?",
   "choices": ["9", "18", "81", "4.5"],
   "answer": 1,
   "explain": "Handshaking lemma: \u03a3deg = 2|E| = 18."},
  {"q": "Which finds shortest paths in an unweighted graph?",
   "choices": ["DFS", "BFS", "Topological sort", "Kruskal's"],
   "answer": 1,
   "explain": "BFS explores in increasing distance from the source \u2014 first visit is via a shortest path."},
  {"q": "Characteristic equation of a\u2099 = 5a\u2099\u208b\u2081 \u2212 6a\u2099\u208b\u2082?",
   "choices": ["r\u00b2 = 5r + 6", "r\u00b2 = 5r \u2212 6", "r = 5 \u2212 6r", "r\u00b2 + 5r \u2212 6 = 0"],
   "answer": 1,
   "explain": "Assume a\u2099 = r\u207f: r\u207f = 5r\u207f\u207b\u00b9 \u2212 6r\u207f\u207b\u00b2 \u21d2 r\u00b2 = 5r \u2212 6."}
 ]
},
{
 "id": "m20-numerical-methods", "code": "IL-20", "title": "Numerical Methods",
 "weight": 1,
 "summary": "Bisection, Newton's method, numerical integration, and error analysis \u2014 computing answers when closed forms don't exist.",
 "objectives": ["Bracket a root with bisection and bound its error", "Apply Newton's method and state its convergence requirement", "Approximate integrals with trapezoidal and Simpson's rules", "Quantify error order and condition sensitivity"],
 "notes": [
  {"title": "Bisection",
   "body": "If f is continuous with f(a)f(b) < 0, a root lies in (a,b). Halve repeatedly, keeping the sign change: after n steps the error is at most (b\u2212a)/2\u207f. **Guaranteed but linear** convergence \u2014 slow and sure. Always check the sign-change precondition; without it, bisection proves nothing."},
  {"title": "Newton's method",
   "body": "`x\u2099\u208a\u2081 = x\u2099 \u2212 f(x\u2099)/f'(x\u2099)` \u2014 follow the tangent line to its x-intercept. Near a simple root it converges **quadratically** (correct digits roughly double per step). Requirements: a good starting guess, f'(x\u2099) \u2260 0, and smoothness. Bad starts diverge or cycle \u2014 pair with bisection bracketing for safety."},
  {"title": "Numerical integration",
   "body": "**Trapezoidal rule**: h/2 \u00b7 [f\u2080 + 2f\u2081 + \u2026 + 2f\u2099\u208b\u2081 + f\u2099], error O(h\u00b2). **Simpson's rule** (n even): h/3 \u00b7 [f\u2080 + 4f\u2081 + 2f\u2082 + \u2026 + 4f\u2099\u208b\u2081 + f\u2099], error O(h\u2074) \u2014 halving h cuts Simpson error ~16\u00d7. Simpson fits parabolas; it is exact for cubics too."},
  {"title": "Error and conditioning",
   "body": "Two error sources: **truncation** (method's approximation) and **roundoff** (finite precision). **Conditioning** measures sensitivity: solving near-singular systems amplifies input errors \u2014 the condition number \u03ba(A) = ||A||\u00b7||A\u207b\u00b9|| bounds the blowup. A stable algorithm on an ill-conditioned problem still gives garbage: distinguish the two."}
 ],
 "cards": [
  {"front": "Bisection error after n steps?", "back": "\u2264 (b\u2212a)/2\u207f."},
  {"front": "Newton's iteration formula?", "back": "x\u2099\u208a\u2081 = x\u2099 \u2212 f(x\u2099)/f'(x\u2099)."},
  {"front": "Simpson's rule coefficients pattern?", "back": "h/3 \u00b7 [1, 4, 2, 4, 2, \u2026, 4, 1]; n must be even; error O(h\u2074)."},
  {"front": "Truncation vs roundoff error?", "back": "Truncation: error from the method's approximation. Roundoff: error from finite floating-point precision."},
  {"front": "What does the condition number measure?", "back": "Sensitivity of the problem's answer to input perturbations \u2014 not the algorithm's quality."}
 ],
 "quiz": [
  {"q": "Bisection on [1,2] for 10 iterations bounds the root error by:",
   "choices": ["1/2^10 \u2248 0.001", "1/10", "1/2^5", "It depends on f"],
   "answer": 0,
   "explain": "(b\u2212a)/2\u207f = 1/1024 \u2248 0.001."},
  {"q": "One Newton step for f(x)=x\u00b2\u22122 from x\u2080=1:",
   "choices": ["1.25", "1.5", "1.414", "2"],
   "answer": 1,
   "explain": "x\u2081 = 1 \u2212 (1\u22122)/(2) = 1 + 0.5 = 1.5."},
  {"q": "Halving h in Simpson's rule roughly divides error by:",
   "choices": ["2", "4", "8", "16"],
   "answer": 3,
   "explain": "Error is O(h\u2074): (1/2)\u2074 = 1/16."},
  {"q": "Newton's method can fail when:",
   "choices": ["f'(x\u2099) = 0", "The root is simple", "f is a polynomial", "Starting exactly at the root"],
   "answer": 0,
   "explain": "Division by f'(x\u2099): a zero derivative blows up the step (also bad for flat regions and poor starts)."}
 ]
},
{
 "id": "m20-linear-systems-optimization", "code": "IL-20", "title": "Linear Systems & Optimization",
 "weight": 1,
 "summary": "Gaussian elimination, LU factorization, least squares, and gradient descent \u2014 solving systems and minimizing objectives at scale.",
 "objectives": ["Solve Ax=b by Gaussian elimination with back substitution", "Formulate and solve a least-squares problem", "Run gradient descent on a convex objective", "Explain the normal equations and when to avoid them"],
 "notes": [
  {"title": "Gaussian elimination",
   "body": "Forward elimination reduces [A|b] to upper-triangular form using row operations (swap, scale, add multiples); **back substitution** solves from the bottom up. Cost: O(n\u00b3). **Partial pivoting** (swap in the largest available pivot) controls roundoff \u2014 never divide by a tiny pivot when a larger one is available."},
  {"title": "LU factorization",
   "body": "Elimination factors A = LU (lower \u00d7 upper, with row permutations). Factor once at O(n\u00b3), then solve each new right-hand side at O(n\u00b2) via Ly=b, Ux=y. This is what libraries actually do \u2014 `numpy.linalg.solve` uses LU-style factorization, not explicit inversion."},
  {"title": "Least squares",
   "body": "For overdetermined Ax \u2248 b, minimize ||Ax\u2212b||\u00b2. Setting the gradient to zero gives the **normal equations** `A\u1d5bAx = A\u1d5bb`. Geometrically: project b onto the column space of A. In practice prefer **QR factorization** \u2014 the normal equations square the condition number (\u03ba(A\u1d5bA) = \u03ba(A)\u00b2), amplifying numerical error."},
  {"title": "Gradient descent",
   "body": "`x \u2190 x \u2212 \u03b1\u2207f(x)`: step downhill. For convex f with Lipschitz gradient, a small enough **learning rate** \u03b1 converges; too large diverges. **Stochastic** GD uses one sample's gradient per step \u2014 noisy but fast per iteration, the engine of neural-network training. The gradient itself comes from the chain rule (module 8)."}
 ],
 "cards": [
  {"front": "Cost of Gaussian elimination?", "back": "O(n\u00b3) for the factorization; O(n\u00b2) per solve after LU."},
  {"front": "Normal equations?", "back": "A\u1d5bAx = A\u1d5bb \u2014 least-squares solution of Ax\u2248b."},
  {"front": "Why prefer QR over normal equations numerically?", "back": "Normal equations square the condition number: \u03ba(A\u1d5bA)=\u03ba(A)\u00b2."},
  {"front": "Gradient descent update?", "back": "x \u2190 x \u2212 \u03b1\u2207f(x)."},
  {"front": "What is partial pivoting for?", "back": "Choosing the largest available pivot to control roundoff error."},
  {"front": "Least squares, geometrically?", "back": "Orthogonal projection of b onto the column space of A."}
 ],
 "quiz": [
  {"q": "Solving [[2,1],[1,3]] [x,y]\u1d5b = [5,6]\u1d5b by elimination gives:",
   "choices": ["x=1, y=2", "x=9/5, y=7/5", "x=2, y=1", "x=3, y=\u22121"],
   "answer": 1,
   "explain": "det=5; x=(5\u00b73\u22121\u00b76)/5=9/5; y=(2\u00b76\u22121\u00b75)/5=7/5."},
  {"q": "Gradient descent with too-large learning rate \u03b1:",
   "choices": ["Converges faster", "May oscillate or diverge", "Converges to a better minimum", "Has no effect"],
   "answer": 1,
   "explain": "Overshooting the minimum repeatedly \u2014 the classic divergence mode."},
  {"q": "After one LU factorization of A, each additional solve costs:",
   "choices": ["O(n\u00b3)", "O(n\u00b2)", "O(n)", "O(1)"],
   "answer": 1,
   "explain": "Forward/back substitution on triangular factors is O(n\u00b2)."},
  {"q": "Least squares minimizes:",
   "choices": ["||Ax\u2212b||\u2081", "||Ax\u2212b||\u00b2", "max|Ax\u2212b|", "rank(A)"],
   "answer": 1,
   "explain": "The squared Euclidean residual \u2014 equivalently the projection residual."}
 ]
}
]
