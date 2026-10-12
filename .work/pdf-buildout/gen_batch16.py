"""Batch 16: Math (discrete, linear, probability, stats, calculus, info theory,
graph theory, queueing, crypto math), Web (rendering, CSS, JS runtime,
security, caching, realtime), Mobile arch, Blockchain (basics, smart
contracts, hashing, P2P). All diagrams original."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def pdf_discrete_math(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Discrete Math\nfor Computer Science",
               "Sets, logic, induction, counting, and the pigeonhole\nprinciple — the math underneath every algorithm.",
               "Math Foundations", None); pg += 1

    # Step 1: sets
    y = section_header(c, 1, 6, "Sets: The Atoms of CS",
                       "A set is an unordered collection of distinct objects. Everything starts here.")
    box(c, 72, 420, 200, 120, BOX_BLUE, "A = {1, 2, 3}", "finite set")
    box(c, 300, 420, 168, 120, BOX_GREEN, "B = {2, 3, 4}", "finite set")
    c.setFillColor(ACCENT2); c.setFont(TITLE_FONT, 12)
    c.drawCentredString(306, 360, "A intersect B = {2, 3}")
    c.drawCentredString(306, 340, "A union B = {1, 2, 3, 4}")
    c.setFont(BODY_FONT, 11); c.setFillColor(INK)
    c.drawString(72, 300, "Key notation:  x in A (membership)   A subset of B   A \\ B (difference)")
    note(c, 72, 200, 468, "Databases, types, and access-control lists are all set operations in disguise.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: logic
    y = section_header(c, 1, 6, "Logic: Reasoning Without Ambiguity",
                       "Propositions combine with AND, OR, NOT. Truth tables enumerate every case.")
    for i, (op, t1, t2, r, fill) in enumerate([
        ("P AND Q", "T", "T", "T", BOX_BLUE), ("P AND Q", "T", "F", "F", BOX_BLUE),
        ("P OR Q", "F", "F", "F", BOX_GREEN), ("P OR Q", "T", "F", "T", BOX_GREEN)]):
        yy = y - i * 56
        box(c, 72, yy - 44, 160, 48, fill, op, "", font_size=11)
        box(c, 250, yy - 44, 80, 48, BOX_ORANGE, f"P={t1}", "", font_size=11)
        box(c, 340, yy - 44, 80, 48, BOX_ORANGE, f"Q={t2}", "", font_size=11)
        box(c, 430, yy - 44, 80, 48, BOX_RED, f"={r}", "", font_size=11)
    note(c, 72, 160, 468, "Implication P -> Q is only false when P is true and Q is false — the trap in half of all bug hunts.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: induction
    y = section_header(c, 3, 6, "Proof by Induction",
                       "Knock down the first domino, then prove every domino topples the next.")
    box(c, 72, 480, 468, 70, BOX_BLUE, "BASE CASE", "prove P(1) directly", font_size=13)
    arrow(c, 306, 478, 306, 430, color=ACCENT, label="then")
    box(c, 72, 350, 468, 70, BOX_GREEN, "INDUCTIVE STEP", "assume P(k), prove P(k+1)", font_size=13)
    arrow(c, 306, 348, 306, 300, color=ACCENT, label="then")
    box(c, 72, 220, 468, 70, BOX_PURP, "CONCLUSION", "P(n) holds for all n >= 1", font_size=13)
    note(c, 72, 120, 468, "Induction is recursion's mathematical twin — the proof structure of every recursive algorithm's correctness.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: counting
    y = section_header(c, 4, 6, "Combinatorics: Counting Without Listing",
                       "Two rules answer nearly every counting question.")
    box(c, 72, 480, 225, 120, BOX_BLUE, "PERMUTATIONS", "order matters: n! /(n-k)!", font_size=13)
    box(c, 315, 480, 225, 120, BOX_GREEN, "COMBINATIONS", "order free: n! / k!(n-k)!", font_size=13)
    box(c, 72, 330, 468, 80, BOX_ORANGE, "MULTIPLICATION RULE", "k independent choices with n1..nk options -> n1 * n2 * ... * nk", font_size=12)
    box(c, 72, 230, 468, 80, BOX_TEAL, "ADDITION RULE", "mutually exclusive cases -> add their counts", font_size=12)
    note(c, 72, 130, 468, "Passwords, shuffles, committee picks, packet routes: choose the right rule and the number falls out.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: pigeonhole
    y = section_header(c, 5, 6, "The Pigeonhole Principle",
                       "n items, m containers, n > m -> at least one container holds 2+ items.")
    for i in range(3):
        box(c, 82 + i * 155, 460, 130, 100, BOX_ORANGE, f"Hole {i+1}", "")
    c.setFillColor(ACCENT2); c.setFont(TITLE_FONT, 12)
    for i in range(4):
        c.drawCentredString(147 + i * 130 - 30 if i < 3 else 147, 585, "P")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 420, "4 pigeons, 3 holes -> Hole 1 must hold 2 pigeons. No escape.")
    box(c, 72, 300, 468, 70, BOX_RED, "POWER USE", "hash collisions MUST exist: 2^256 inputs, 2^256 outputs — wait, that matches...", font_size=12)
    note(c, 72, 200, 468, "General form: n items into m holes -> one hole has >= ceil(n/m). Collisions, birthdays, compression limits all follow.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: growth
    y = section_header(c, 6, 6, "Growth Orders: What Induction + Counting Buy You",
                       "Recurrences describe algorithms; growth orders compare them.")
    box(c, 72, 480, 468, 70, BOX_BLUE, "T(n) = 2*T(n/2) + n", "mergesort-style recurrence -> Theta(n log n)", font_size=12)
    orders = [("O(1)", "constant"), ("O(log n)", "binary search"), ("O(n)", "one pass"),
              ("O(n log n)", "fast sorts"), ("O(n^2)", "nested loops"), ("O(2^n)", "brute force")]
    yy = y - 90
    for i, (o, ex) in enumerate(orders):
        fill = [BOX_GREEN, BOX_TEAL, BOX_BLUE, BOX_ORANGE, BOX_RED, BOX_RED][i]
        box(c, 72, yy - 40, 140, 44, fill, o, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(228, yy - 12, ex)
        yy -= 54
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Discrete Math — Remember",
                 ["Sets and their operations (union, intersection, difference) model data collections everywhere.",
                  "Logic and truth tables give unambiguous rules for reasoning about program correctness.",
                  "Induction proves statements for all n: base case plus the k -> k+1 step.",
                  "Permutations count ordered selections; combinations count unordered ones; multiply or add accordingly.",
                  "The pigeonhole principle guarantees collisions whenever items outnumber containers.",
                  "Recurrences plus growth orders let you compare algorithms before writing a line of code."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_linear_algebra(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Linear Algebra\nVisual Guide",
               "Vectors, matrices, and eigenvalues —\nthe language machine learning speaks.",
               "Math Foundations", None); pg += 1

    # Step 1: vectors
    y = section_header(c, 1, 6, "Vectors: Direction + Magnitude",
                       "An ordered list of numbers is also an arrow in space.")
    box(c, 72, 430, 200, 110, BOX_BLUE, "v = [3, 4]", "|v| = 5 (3-4-5 triangle)")
    arrow(c, 400, 460, 500, 530, color=ACCENT2, width=3, label="v")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 400, "Add: tip-to-tail.  Scale: stretch the arrow.  Magnitude: sqrt(sum of squares).")
    box(c, 72, 290, 468, 80, BOX_GREEN, "FEATURE VECTORS", "[age, income, clicks] — one row of data = one vector", font_size=12)
    note(c, 72, 190, 468, "Every ML dataset is a cloud of vectors. The geometry of that cloud is what models learn.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: matrices as transforms
    y = section_header(c, 2, 6, "Matrices Are Transformations",
                       "Multiplying by a matrix moves every vector in space — rotate, scale, shear, project.")
    box(c, 72, 470, 140, 90, BOX_BLUE, "Rotation", "spins axes")
    box(c, 232, 470, 140, 90, BOX_GREEN, "Scaling", "stretches axes")
    box(c, 392, 470, 140, 90, BOX_ORANGE, "Projection", "flattens to a line")
    box(c, 72, 340, 468, 90, BOX_TEAL, "LINEAR LAYERS", "a neural net layer IS a matrix multiply plus bias: y = Wx + b", font_size=12)
    note(c, 72, 240, 468, "Think function, not table: a matrix maps input space to output space.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: dot product
    y = section_header(c, 3, 6, "The Dot Product: Similarity in One Number",
                       "a . b = |a||b| cos(theta) — big when vectors point the same way.")
    box(c, 72, 460, 200, 110, BOX_BLUE, "a . b = sum(ai*bi)", "algebraic view")
    box(c, 300, 460, 168, 110, BOX_GREEN, "a . b = |a||b|cos", "geometric view")
    yy = y - 150
    for label, val, fill in [("Parallel", "max positive", BOX_GREEN), ("Perpendicular", "zero", BOX_ORANGE), ("Opposite", "max negative", BOX_RED)]:
        box(c, 72, yy - 44, 160, 48, fill, label, "", font_size=11)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(250, yy - 12, "dot product -> " + val)
        yy -= 60
    note(c, 72, 160, 468, "Attention scores, cosine similarity, search ranking: dot products measuring alignment.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: matrix multiplication
    y = section_header(c, 4, 6, "Matrix Multiplication = Compose Transforms",
                       "AB means 'do B first, then A'. Order matters.")
    box(c, 72, 470, 150, 100, BOX_BLUE, "A (m x n)", "")
    box(c, 246, 470, 150, 100, BOX_GREEN, "B (n x p)", "")
    box(c, 420, 470, 120, 100, BOX_PURP, "AB (m x p)", "")
    arrow(c, 224, 520, 244, 520, color=ACCENT)
    arrow(c, 398, 520, 418, 520, color=ACCENT)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 12)
    c.drawCentredString(306, 420, "Inner dimensions must match: (m x n)(n x p)")
    box(c, 72, 300, 468, 70, BOX_ORANGE, "NOT COMMUTATIVE", "AB != BA in general — like 'rotate then scale' vs 'scale then rotate'", font_size=12)
    note(c, 72, 200, 468, "Dimension-check every layer: the inner numbers matching is how you debug shape errors in neural nets.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: eigen
    y = section_header(c, 5, 6, "Eigenvectors: The Unmoved Directions",
                       "Av = lambda*v — the matrix only stretches these vectors, never rotates them.")
    box(c, 72, 470, 468, 100, BOX_PURP, "A * v = lambda * v", "v: eigenvector (direction)   lambda: eigenvalue (stretch factor)", font_size=13)
    arrow(c, 200, 520, 330, 520, color=ACCENT2, width=3, label="v")
    arrow(c, 200, 470, 330, 470, color=ACCENT2, width=3, label="Av = 2v")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 430, "Stretch factor 2: same arrow, twice as long. That direction is an eigenvector.")
    box(c, 72, 300, 468, 80, BOX_TEAL, "PCA", "principal components = eigenvectors of the covariance matrix — the data's true axes", font_size=12)
    note(c, 72, 200, 468, "PageRank, PCA, spectral clustering, stability analysis: all eigenvalue problems in disguise.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: ML
    y = section_header(c, 6, 6, "How Linear Algebra Powers ML",
                       "The whole field is geometry at scale.")
    items = [("Embeddings", "words/images as vectors; meaning = position in space", BOX_BLUE),
             ("Cosine similarity", "normalized dot product for search & retrieval", BOX_GREEN),
             ("Linear regression", "projection of y onto the column space of X", BOX_ORANGE),
             ("SVD / low-rank", "compress matrices by keeping top singular directions", BOX_TEAL),
             ("Backprop", "gradients flow through matrix multiplies via the chain rule", BOX_PURP)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=12)
        yy -= 76
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Linear Algebra — Remember",
                 ["A vector is a direction plus magnitude; a dataset is a cloud of vectors.",
                  "Matrices are transformations: rotate, scale, shear, project — y = Wx + b is a neural layer.",
                  "The dot product measures alignment: the engine of attention and similarity search.",
                  "Matrix multiplication composes transforms; inner dimensions must match, and order matters.",
                  "Eigenvectors are the directions a matrix only stretches — the basis of PCA and PageRank.",
                  "ML is applied linear algebra: embeddings, projections, and gradients in high-dimensional space."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_probability(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Probability\nVisual Guide",
               "Bayes' theorem, distributions, and expectation —\nreasoning rigorously under uncertainty.",
               "Math Foundations", None); pg += 1

    # Step 1: axioms
    y = section_header(c, 1, 6, "The Three Axioms",
                       "Kolmogorov's rules — everything else is a consequence.")
    box(c, 72, 470, 468, 80, BOX_BLUE, "1.  0 <= P(A) <= 1", "probabilities live between zero and one", font_size=13)
    box(c, 72, 370, 468, 80, BOX_GREEN, "2.  P(Sample space) = 1", "something must happen", font_size=13)
    box(c, 72, 270, 468, 80, BOX_ORANGE, "3.  P(A or B) = P(A) + P(B)", "for disjoint A, B — probabilities add", font_size=13)
    note(c, 72, 170, 468, "These three lines imply every formula you will meet: complements, unions, conditionals.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: conditional
    y = section_header(c, 2, 6, "Conditional Probability & Independence",
                       "New evidence shrinks the sample space to what you observed.")
    box(c, 72, 470, 468, 90, BOX_TEAL, "P(A | B) = P(A and B) / P(B)", "'probability of A GIVEN that B happened'", font_size=13)
    box(c, 72, 340, 225, 100, BOX_GREEN, "INDEPENDENT", "P(A|B) = P(A) — B tells you nothing", font_size=12)
    box(c, 315, 340, 225, 100, BOX_RED, "DEPENDENT", "P(A|B) != P(A) — B changes the odds", font_size=12)
    note(c, 72, 240, 468, "Assuming independence where none exists is the most common modeling sin — and the most expensive.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: Bayes
    y = section_header(c, 3, 6, "Bayes' Theorem: Flip the Conditional",
                       "From P(evidence | hypothesis) to P(hypothesis | evidence).")
    box(c, 72, 470, 468, 90, BOX_PURP, "P(H | E) = P(E | H) * P(H) / P(E)", "posterior = likelihood * prior / evidence", font_size=13)
    box(c, 72, 350, 150, 80, BOX_BLUE, "PRIOR P(H)", "belief before data")
    arrow(c, 224, 390, 246, 390, color=ACCENT, label="x")
    box(c, 250, 350, 150, 80, BOX_GREEN, "LIKELIHOOD", "P(E | H)")
    arrow(c, 402, 390, 424, 390, color=ACCENT)
    box(c, 428, 350, 112, 80, BOX_ORANGE, "POSTERIOR", "updated belief")
    note(c, 72, 250, 468, "Rare diseases, spam filters, sensor fusion: Bayes is how evidence updates belief, correctly.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: distributions
    y = section_header(c, 4, 6, "Three Distributions to Know Cold",
                       "Each answers a different 'how many / how often' question.")
    box(c, 72, 470, 468, 80, BOX_BLUE, "BINOMIAL", "k successes in n trials: coin flips, A/B conversions", font_size=12)
    box(c, 72, 370, 468, 80, BOX_GREEN, "POISSON", "events per interval: arrivals/sec, errors per deploy", font_size=12)
    box(c, 72, 270, 468, 80, BOX_ORANGE, "NORMAL (Gaussian)", "bell curve: measurement noise, sums of many small effects", font_size=12)
    note(c, 72, 170, 468, "The normal distribution earns its fame from the Central Limit Theorem — averages become normal as n grows.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: expectation & variance
    y = section_header(c, 5, 6, "Expectation & Variance",
                       "The center of mass of a distribution, and how spread out it is.")
    box(c, 72, 470, 225, 110, BOX_TEAL, "E[X] = sum x*P(x)", "long-run average value")
    box(c, 315, 470, 225, 110, BOX_RED, "Var(X) = E[(X-mu)^2]", "average squared deviation")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 430, "Linearity: E[aX + bY] = aE[X] + bE[Y] — works even when X, Y are dependent.")
    box(c, 72, 310, 468, 80, BOX_PURP, "STD DEV = sqrt(Var)", "same units as X — the honest error bar on any estimate", font_size=12)
    note(c, 72, 210, 468, "Means deceive; variance tells you whether the mean is a promise or a rumor.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: LLN & CLT
    y = section_header(c, 6, 6, "LLN and CLT: Why Statistics Works",
                       "Two theorems that make measurement meaningful.")
    box(c, 72, 470, 468, 90, BOX_BLUE, "LAW OF LARGE NUMBERS", "sample mean -> true mean as n grows. More data = closer truth.", font_size=12)
    box(c, 72, 350, 468, 90, BOX_GREEN, "CENTRAL LIMIT THEOREM", "means of samples become normal — whatever the original shape.", font_size=12)
    note(c, 72, 250, 468, "CLT is why confidence intervals and A/B test math work even when your data is wildly non-normal.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Probability — Remember",
                 ["Three axioms (bounded, total = 1, additive) imply the entire theory.",
                  "Conditioning shrinks the world to what you observed; check independence assumptions ruthlessly.",
                  "Bayes flips the conditional: posterior = likelihood x prior / evidence.",
                  "Binomial counts successes in trials; Poisson counts events per interval; normal models noise.",
                  "Expectation is the long-run average; variance is the honest error bar.",
                  "LLN says more data approaches truth; CLT says sample means become normal."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_statistics(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Statistics\nVisual Guide",
               "Hypothesis tests, p-values, confidence intervals,\nand regression — inferring truth from samples.",
               "Math Foundations", None); pg += 1

    # Step 1: sampling
    y = section_header(c, 1, 6, "Samples vs Populations",
                       "You measure a sample; you care about the population. The gap is the whole game.")
    box(c, 72, 460, 200, 110, BOX_BLUE, "POPULATION", "everyone/everything (unknowable)")
    arrow(c, 280, 515, 330, 515, color=ACCENT, label="sample")
    box(c, 340, 460, 200, 110, BOX_GREEN, "SAMPLE", "what you actually measure")
    box(c, 72, 330, 468, 80, BOX_RED, "BIAS", "non-random sampling -> the sample lies about the population", font_size=12)
    note(c, 72, 230, 468, "No fancy test fixes a bad sample. Randomness of selection beats size of selection.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: confidence intervals
    y = section_header(c, 2, 6, "Confidence Intervals",
                       "A range that would trap the true value 95% of the time — if you repeated the study.")
    box(c, 72, 470, 468, 90, BOX_TEAL, "estimate  +/-  margin of error", "e.g. 52% +/- 3%  ->  interval [49%, 55%]", font_size=13)
    box(c, 72, 340, 225, 90, BOX_GREEN, "WIDER when...", "small n, high variance, high confidence", font_size=11)
    box(c, 315, 340, 225, 90, BOX_ORANGE, "NARROWER when...", "big n, low variance, lower confidence", font_size=11)
    note(c, 72, 240, 468, "A 95% CI is a property of the PROCEDURE, not a 95% chance the truth is inside this one interval.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: hypothesis testing
    y = section_header(c, 3, 6, "Hypothesis Testing Framework",
                       "Assume nothing is happening (H0); ask if the data is surprising under that assumption.")
    box(c, 72, 470, 225, 100, BOX_RED, "H0: NULL", "no effect, no difference — the skeptic's position")
    box(c, 315, 470, 225, 100, BOX_GREEN, "H1: ALTERNATIVE", "there IS an effect — what you hope to show")
    arrow(c, 306, 560, 306, 575, color=ACCENT, label="collect data")
    box(c, 72, 330, 468, 80, BOX_BLUE, "TEST STATISTIC", "how far is the data from H0's prediction? measured in standard errors", font_size=12)
    note(c, 72, 230, 468, "You never 'prove' H1. You reject H0 — or fail to. Absence of evidence is not evidence of absence.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: p-values & errors
    y = section_header(c, 4, 6, "P-values and Error Types",
                       "What a p-value actually is — and the two ways to be wrong.")
    box(c, 72, 470, 468, 90, BOX_PURP, "p = P(data this extreme | H0 true)", "small p -> data surprises the skeptic -> reject H0", font_size=12)
    box(c, 72, 340, 225, 100, BOX_RED, "TYPE I (alpha)", "reject a TRUE H0 — false alarm")
    box(c, 315, 340, 225, 100, BOX_ORANGE, "TYPE II (beta)", "keep a FALSE H0 — missed detection")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 300, "p < 0.05 is convention, not a law of nature. Report effect sizes, not just stars.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: regression
    y = section_header(c, 5, 6, "Regression Basics",
                       "Fit a line that minimizes squared error — then interrogate it.")
    box(c, 72, 470, 468, 90, BOX_BLUE, "y = b0 + b1*x + error", "least squares: minimize sum of squared residuals", font_size=13)
    yy = y - 60
    for label, desc, fill in [("R-squared", "fraction of variance explained", BOX_GREEN),
                             ("Residuals", "errors should look random, not patterned", BOX_ORANGE),
                             ("Coefficients", "b1 = change in y per unit of x, holding others fixed", BOX_TEAL)]:
        box(c, 72, yy - 52, 170, 56, fill, label, "", font_size=11)
        c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
        c.drawString(258, yy - 20, desc)
        yy -= 68
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: pitfalls
    y = section_header(c, 6, 6, "Correlation, Causation & Other Traps",
                       "The statistics are easy. The interpretation is where people get hurt.")
    box(c, 72, 470, 468, 80, BOX_RED, "CORRELATION != CAUSATION", "confounders, reverse causation, coincidence — always ask", font_size=12)
    box(c, 72, 370, 468, 80, BOX_ORANGE, "MULTIPLE TESTING", "20 tests at p<0.05 -> expect 1 false hit. Correct (Bonferroni/FDR).", font_size=12)
    box(c, 72, 270, 468, 80, BOX_TEAL, "P-HACKING", "stopping when p dips, trying every slice — preregister analyses", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Statistics — Remember",
                 ["You measure samples to learn about populations; biased sampling poisons everything downstream.",
                  "Confidence intervals quantify uncertainty — a 95% CI is about the procedure, repeated.",
                  "Hypothesis testing: assume H0, measure surprise. Reject or fail to reject — never 'prove'.",
                  "A p-value is P(data | H0), not P(H0 | data). Mind Type I and Type II errors.",
                  "Regression fits by least squares; check residuals and report effect sizes, not just significance.",
                  "Correlation is not causation; correct for multiple testing; preregister to avoid p-hacking."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_calculus_ml(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Calculus\nfor Machine Learning",
               "Derivatives, gradients, and the chain rule —\nthe engine that trains neural networks.",
               "Math Foundations", None); pg += 1

    # Step 1: derivative
    y = section_header(c, 1, 6, "The Derivative = Instantaneous Slope",
                       "f'(x): how fast f changes as x changes, right now.")
    box(c, 72, 470, 468, 90, BOX_BLUE, "f'(x) = limit of [f(x+h) - f(x)] / h  as h -> 0", "slope of the tangent line at x", font_size=12)
    box(c, 72, 340, 225, 90, BOX_GREEN, "f'(x) > 0", "going up — increase x to grow f")
    box(c, 315, 340, 225, 90, BOX_RED, "f'(x) < 0", "going down — decrease x to grow f")
    note(c, 72, 240, 468, "Optimization is just: follow the sign of the derivative until it hits zero.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: chain rule
    y = section_header(c, 2, 6, "The Chain Rule",
                       "Derivatives of nested functions multiply — this single rule trains deep nets.")
    box(c, 72, 470, 120, 90, BOX_BLUE, "f(x)", "")
    arrow(c, 194, 515, 222, 515, color=ACCENT, label="into")
    box(c, 226, 470, 120, 90, BOX_GREEN, "g(f)", "")
    arrow(c, 348, 515, 376, 515, color=ACCENT, label="into")
    box(c, 380, 470, 120, 90, BOX_ORANGE, "h(g)", "")
    box(c, 72, 340, 468, 90, BOX_PURP, "d/dx h(g(f)) = h'(g) * g'(f) * f'(x)", "peel layers outside-in, multiply each local slope", font_size=12)
    note(c, 72, 240, 468, "A 100-layer network is just a 100-deep nesting. The chain rule handles arbitrary depth.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: partial derivatives
    y = section_header(c, 3, 6, "Partial Derivatives",
                       "With many inputs, vary one at a time and freeze the rest.")
    box(c, 72, 470, 468, 90, BOX_TEAL, "df/dx treats y, z, ... as constants", "neural nets have millions of parameters — one partial each", font_size=12)
    box(c, 72, 340, 225, 100, BOX_BLUE, "df/dx > 0", "nudge x up, f grows")
    box(c, 315, 340, 225, 100, BOX_ORANGE, "df/dy < 0", "nudge y up, f shrinks")
    note(c, 72, 240, 468, "Each weight in a network gets its own partial derivative: its personal 'which way is down'.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: gradient descent
    y = section_header(c, 4, 6, "The Gradient & Gradient Descent",
                       "Stack all partials into one vector — it points uphill. Walk the other way.")
    box(c, 72, 470, 468, 90, BOX_PURP, "grad f = [df/dx1, df/dx2, ..., df/dxn]", "points in the direction of steepest INCREASE", font_size=12)
    box(c, 72, 350, 468, 80, BOX_GREEN, "w := w - lr * grad f(w)", "step downhill; lr = learning rate (step size)", font_size=12)
    box(c, 72, 240, 468, 70, BOX_RED, "lr too big -> diverge    lr too small -> crawl", "tuning lr is half of practical ML", font_size=11)
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: loss landscapes
    y = section_header(c, 5, 6, "Loss Landscapes",
                       "Training = descending a high-dimensional terrain to minimize loss.")
    box(c, 72, 470, 225, 100, BOX_GREEN, "GLOBAL MINIMUM", "best possible loss — rarely found, rarely needed")
    box(c, 315, 470, 225, 100, BOX_ORANGE, "LOCAL MINIMUM", "valley, not the deepest — usually good enough")
    box(c, 72, 340, 225, 100, BOX_RED, "SADDLE POINT", "flat in some directions, sloped in others — the real trap")
    box(c, 315, 340, 225, 100, BOX_TEAL, "PLATEAU", "tiny gradients — progress stalls; momentum helps")
    note(c, 72, 240, 468, "Deep nets have zillions of 'good enough' minima. Finding one of them is the whole job.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: backprop
    y = section_header(c, 6, 6, "Backprop = Chain Rule at Scale",
                       "One forward pass, then sweep gradients backward layer by layer.")
    box(c, 72, 520, 110, 70, BOX_BLUE, "Input", "")
    arrow(c, 184, 555, 212, 555, color=ACCENT, label="forward")
    box(c, 216, 520, 110, 70, BOX_GREEN, "Layer 1", "")
    arrow(c, 328, 555, 356, 555, color=ACCENT)
    box(c, 360, 520, 110, 70, BOX_ORANGE, "Layer 2", "")
    arrow(c, 472, 555, 500, 555, color=ACCENT)
    box(c, 72, 400, 468, 80, BOX_RED, "LOSS", "scalar error at the end — the single number everything flows from", font_size=12)
    arrow(c, 460, 398, 460, 370, color=RED, label="gradients flow back")
    box(c, 72, 280, 468, 70, BOX_PURP, "BACKWARD PASS", "chain rule per layer: dLoss/dW = dLoss/dout * dout/dW", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Calculus for ML — Remember",
                 ["The derivative is instantaneous slope; its sign says which way is up.",
                  "The chain rule multiplies local slopes through nested functions — the core of deep learning.",
                  "Partial derivatives isolate one parameter's effect while freezing the rest.",
                  "The gradient points uphill; gradient descent walks downhill with step size lr.",
                  "Loss landscapes hold minima, saddles, and plateaus — local minima are usually good enough.",
                  "Backpropagation is the chain rule applied layer-by-layer, forward once then backward."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_info_theory(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Information Theory\nVisual Guide",
               "Entropy, cross-entropy, and KL divergence —\nhow ML measures surprise and compresses reality.",
               "Math Foundations", None); pg += 1

    # Step 1: surprisal
    y = section_header(c, 1, 6, "Surprisal: Rare Events Carry More Bits",
                       "Information content of an event = -log2 P(event).")
    box(c, 72, 470, 225, 110, BOX_BLUE, "P = 1/2", "coin flip -> 1 bit of surprise")
    box(c, 315, 470, 225, 110, BOX_ORANGE, "P = 1/1024", "rare event -> 10 bits of surprise")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 430, "'The sun rose today' tells you ~0 bits. 'It snowed in July' tells you a lot.")
    note(c, 72, 330, 468, "Bits measure answers to yes/no questions. Surprise is the currency of information.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: entropy
    y = section_header(c, 2, 6, "Entropy: Expected Surprise",
                       "H = -sum p(x) log2 p(x) — the average bits per symbol.")
    box(c, 72, 470, 225, 110, BOX_GREEN, "FAIR COIN", "H = 1 bit — maximum uncertainty")
    box(c, 315, 470, 225, 110, BOX_RED, "ALWAYS HEADS", "H = 0 bits — no uncertainty at all")
    box(c, 72, 330, 468, 80, BOX_TEAL, "MAX ENTROPY = uniform", "a loaded die has LOWER entropy than a fair one", font_size=12)
    note(c, 72, 230, 468, "Entropy is the fundamental limit of compression: you cannot beat H bits per symbol on average.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: cross-entropy
    y = section_header(c, 3, 6, "Cross-Entropy: Coding With the Wrong Model",
                       "H(p, q): average bits when the world is p but you assumed q.")
    box(c, 72, 470, 225, 110, BOX_BLUE, "TRUE p", "reality's distribution")
    box(c, 315, 470, 225, 110, BOX_ORANGE, "MODEL q", "your approximation")
    box(c, 72, 330, 468, 80, BOX_PURP, "H(p,q) >= H(p)", "mismatch always costs extra bits — equality only if q = p", font_size=12)
    note(c, 72, 230, 468, "Training a classifier = shrinking the gap between your q and the world's p.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: KL divergence
    y = section_header(c, 4, 6, "KL Divergence: The Price of Being Wrong",
                       "D_KL(p || q) = H(p,q) - H(p) — extra bits from using q instead of p.")
    box(c, 72, 470, 468, 90, BOX_RED, "D_KL(p || q) >= 0,  = 0 iff p = q", "a directed distance between distributions", font_size=12)
    box(c, 72, 340, 225, 90, BOX_ORANGE, "NOT SYMMETRIC", "D(p||q) != D(q||p) — direction matters")
    box(c, 315, 340, 225, 90, BOX_TEAL, "MODE-SEEKING", "variational inference minimizes D_KL to fit q to p")
    note(c, 72, 240, 468, "Not a true distance (asymmetric), but the workhorse divergence of ML.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: Huffman
    y = section_header(c, 5, 6, "Huffman Coding: Entropy Made Practical",
                       "Frequent symbols get short codes; rare ones get long codes.")
    items = [("E (40%)", "code: 0", BOX_GREEN), ("T (25%)", "code: 10", BOX_BLUE),
             ("A (20%)", "code: 110", BOX_TEAL), ("Z (15%)", "code: 111", BOX_ORANGE)]
    yy = y
    for name, code, fill in items:
        box(c, 72, yy - 52, 200, 56, fill, name, "", font_size=11)
        c.setFillColor(INK); c.setFont(MONO_FONT, 12)
        c.drawString(290, yy - 20, code)
        yy -= 68
    box(c, 72, yy - 60, 468, 64, BOX_PURP, "AVERAGE LENGTH -> H", "Huffman approaches the entropy limit; no prefix code beats it", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: ML uses
    y = section_header(c, 6, 6, "Where ML Uses All of This",
                       "Your loss function is probably information theory.")
    items = [("Log loss", "classification loss IS cross-entropy between labels and predictions", BOX_BLUE),
             ("Decision trees", "splits chosen to maximize information gain (entropy drop)", BOX_GREEN),
             ("VAEs / diffusion", "KL terms keep learned distributions near a prior", BOX_ORANGE),
             ("Mutual information", "I(X;Y): how much X tells you about Y — feature selection", BOX_TEAL)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=12)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Information Theory — Remember",
                 ["Surprisal (-log p) measures how informative an event is; rare events carry more bits.",
                  "Entropy is expected surprise — the theoretical floor for compression.",
                  "Cross-entropy measures cost under your model q when reality is p; H(p,q) >= H(p).",
                  "KL divergence is the extra-bit price of model mismatch; zero only when q = p.",
                  "Huffman coding assigns short codes to frequent symbols, approaching the entropy limit.",
                  "Log loss, information gain, and VAE objectives are information theory wearing an ML costume."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_graph_theory(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Graph Theory\nVisual Guide",
               "Paths, flows, and colorings — the math\nbehind networks, schedules, and systems.",
               "Math Foundations", None); pg += 1

    # Step 1: basics
    y = section_header(c, 1, 6, "Graphs 101: Vertices + Edges",
                       "Everything is dots and lines: social nets, road maps, dependency trees.")
    c.setFillColor(ACCENT2)
    for (x, yy) in [(150, 520), (300, 560), (450, 520), (225, 430), (375, 430)]:
        c.circle(x, yy, 18, fill=1, stroke=0)
    c.setFillColor(white); c.setFont(TITLE_FONT, 11)
    for i, (x, yy) in enumerate([(150, 520), (300, 560), (450, 520), (225, 430), (375, 430)]):
        c.drawCentredString(x, yy - 4, chr(65 + i))
    c.setStrokeColor(ACCENT); c.setLineWidth(2)
    c.line(168, 520, 282, 560); c.line(318, 560, 432, 520)
    c.line(150, 502, 225, 448); c.line(450, 502, 375, 448); c.line(243, 430, 357, 430)
    box(c, 72, 300, 225, 80, BOX_BLUE, "UNDIRECTED", "edges have no direction — friendships")
    box(c, 315, 300, 225, 80, BOX_GREEN, "DIRECTED", "edges point — follows, dependencies")
    note(c, 72, 200, 468, "Weighted edges add costs/distances; then shortest-path and flow problems come alive.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: paths & cycles
    y = section_header(c, 2, 6, "Paths, Cycles, Connectivity",
                       "The vocabulary every graph algorithm speaks.")
    items = [("Path", "sequence of vertices with no repeats — A-B-D", BOX_BLUE),
             ("Cycle", "a path that returns to its start — A-B-D-A", BOX_GREEN),
             ("Connected", "a path exists between every pair of vertices", BOX_TEAL),
             ("DAG", "directed + acyclic — task dependencies, build order", BOX_ORANGE)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 56, 170, 60, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(258, yy - 24, desc)
        yy -= 76
    note(c, 72, 180, 468, "If your dependency graph has a cycle, nothing can build. Topo-sort a DAG to find the order.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: shortest path
    y = section_header(c, 3, 6, "Shortest Path: BFS and Dijkstra",
                       "Unweighted? BFS. Weighted non-negative? Dijkstra.")
    box(c, 72, 470, 468, 80, BOX_BLUE, "BFS", "layer by layer from the source — first visit = shortest (unweighted)", font_size=12)
    box(c, 72, 370, 468, 90, BOX_GREEN, "DIJKSTRA", "always expand the closest unsettled vertex (priority queue)", font_size=12)
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 340, "Greedy + priority queue = O((V+E) log V). Negative edges? Bellman-Ford instead.")
    box(c, 72, 230, 468, 70, BOX_ORANGE, "USE IN SYSTEMS", "routing tables, dependency resolution, game AI pathfinding", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: max flow
    y = section_header(c, 4, 6, "Max Flow / Min Cut",
                       "Push as much as possible from source to sink through capacitated edges.")
    box(c, 72, 470, 120, 90, BOX_BLUE, "SOURCE s", "")
    arrow(c, 194, 515, 232, 515, color=ACCENT, label="cap 10")
    box(c, 236, 470, 140, 90, BOX_GREEN, "NETWORK", "edges have capacities")
    arrow(c, 378, 515, 416, 515, color=ACCENT, label="cap 7")
    box(c, 420, 470, 120, 90, BOX_ORANGE, "SINK t", "")
    box(c, 72, 340, 468, 80, BOX_PURP, "MIN-CUT = MAX-FLOW", "the cheapest set of edges whose removal disconnects s from t", font_size=12)
    note(c, 72, 240, 468, "Bipartite matching, image segmentation, project selection — all max-flow in disguise.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: coloring
    y = section_header(c, 5, 6, "Graph Coloring",
                       "Adjacent vertices get different colors — scheduling's secret weapon.")
    fills = [BOX_RED, BOX_BLUE, BOX_GREEN]
    c.setStrokeColor(INK); c.setLineWidth(1.5)
    for i, (x, yy) in enumerate([(180, 520), (330, 560), (480, 520), (255, 430), (405, 430)]):
        c.setFillColor(fills[i % 3]); c.circle(x, yy, 20, fill=1, stroke=1)
    c.setFillColor(white); c.setFont(TITLE_FONT, 11)
    for i, (x, yy) in enumerate([(180, 520), (330, 560), (480, 520), (255, 430), (405, 430)]):
        c.drawCentredString(x, yy - 4, str(i + 1))
    c.setStrokeColor(MUTED); c.setLineWidth(1.5)
    c.line(200, 520, 310, 560); c.line(350, 560, 460, 520)
    c.line(180, 500, 255, 450); c.line(480, 500, 405, 450)
    box(c, 72, 320, 468, 80, BOX_ORANGE, "CHROMATIC NUMBER", "minimum colors needed — exam slots, register allocation, map coloring", font_size=12)
    note(c, 72, 220, 468, "Optimal coloring is NP-hard, but greedy orderings work well in practice.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: systems
    y = section_header(c, 6, 6, "Graphs in Real Systems",
                       "If it connects, it is a graph problem.")
    items = [("Dependency DAGs", "build systems, package managers — topo-sort for order", BOX_BLUE),
             ("Computer networks", "routers as vertices; OSPF runs Dijkstra on the topology", BOX_GREEN),
             ("PageRank", "eigenvector centrality: important pages are linked by important pages", BOX_PURP),
             ("Social graphs", "communities, influence, recommendations via graph algorithms", BOX_TEAL)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=12)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Graph Theory — Remember",
                 ["Vertices plus edges model anything connected: networks, dependencies, maps.",
                  "Paths and cycles are the vocabulary; DAGs give you build order via topological sort.",
                  "BFS for unweighted shortest path; Dijkstra with a priority queue for weighted.",
                  "Max flow equals min cut — matching, segmentation, and selection reduce to flow.",
                  "Coloring assigns resources so neighbors differ; greedy works well in practice.",
                  "Routing, PageRank, builds, and social graphs are all graph algorithms in production."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_queueing(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Queueing Theory\nVisual Guide",
               "Little's law, the utilization-latency knee,\nand M/M/1 intuition for capacity planning.",
               "Math Foundations", None); pg += 1

    # Step 1: anatomy
    y = section_header(c, 1, 6, "Anatomy of a Queue",
                       "Arrivals show up, wait if busy, get served, leave.")
    box(c, 72, 470, 130, 90, BOX_BLUE, "ARRIVALS", "rate lambda")
    arrow(c, 204, 515, 240, 515, color=ACCENT)
    box(c, 244, 470, 130, 90, BOX_ORANGE, "QUEUE", "waiting line")
    arrow(c, 376, 515, 412, 515, color=ACCENT)
    box(c, 416, 470, 124, 90, BOX_GREEN, "SERVER", "rate mu")
    arrow(c, 480, 470, 480, 400, color=GREEN, label="served")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 430, "Stability requires lambda < mu — arrivals slower than service, or the line grows forever.")
    note(c, 72, 330, 468, "Every checkout line, thread pool, and API gateway is this diagram.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: Little's law
    y = section_header(c, 2, 6, "Little's Law: L = lambda * W",
                       "Average number in system = arrival rate x average time in system. Always. Any system.")
    box(c, 72, 470, 468, 90, BOX_PURP, "L = lambda * W", "L: avg in system   lambda: arrival rate   W: avg time in system", font_size=13)
    box(c, 72, 340, 468, 90, BOX_TEAL, "EXAMPLE", "100 req/s, each spends 0.2s in system -> 20 requests in flight, always", font_size=12)
    note(c, 72, 240, 468, "No distributional assumptions at all — the most robust law in systems engineering. Measure two, get the third.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: utilization curve
    y = section_header(c, 3, 6, "The Utilization vs Latency Knee",
                       "Latency explodes as utilization approaches 100%. The knee is the danger zone.")
    c.setStrokeColor(INK); c.setLineWidth(1.5)
    c.line(100, 300, 500, 300)  # x axis
    c.line(100, 300, 100, 560)  # y axis
    c.setStrokeColor(RED); c.setLineWidth(3)
    p = c.beginPath()
    p.moveTo(100, 320)
    for i in range(1, 60):
        x = 100 + i * 6.5
        rho = i / 60.0
        yy = 320 + rho * 60 + (rho ** 8) * 160
        p.lineTo(x, min(yy, 555))
    c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(100, 280, "utilization ->  0%")
    c.drawString(430, 280, "100%")
    c.drawCentredString(88, 430, "latency")
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawString(330, 500, "THE KNEE ~ 70-80%")
    note(c, 72, 180, 468, "Running at 95% utilization does not give 95% efficiency — it gives unbounded queues. Plan headroom.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: M/M/1
    y = section_header(c, 4, 6, "M/M/1 Intuition",
                       "Markov arrivals, Markov service, 1 server — the simplest non-trivial queue, with closed forms.")
    box(c, 72, 470, 468, 80, BOX_BLUE, "rho = lambda / mu", "utilization: fraction of time the server is busy", font_size=13)
    box(c, 72, 370, 225, 90, BOX_GREEN, "L = rho / (1 - rho)", "avg number in system")
    box(c, 315, 370, 225, 90, BOX_ORANGE, "W = 1 / (mu - lambda)", "avg time in system")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 340, "At rho = 0.9: L = 9. At rho = 0.5: L = 1. Small utilization shifts, huge queue swings.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: capacity planning
    y = section_header(c, 5, 6, "Capacity Planning Rules of Thumb",
                       "Turn the math into decisions.")
    items = [("Target rho <= 0.7", "latency stays flat; spikes get absorbed by headroom", BOX_GREEN),
             ("Size for peak + growth", "measure lambda at p99 load, not the average Tuesday", BOX_BLUE),
             ("Queues hide, not fix", "a long queue means add capacity or shed load — not more buffering", BOX_ORANGE),
             ("Parallel servers help", "M/M/c: c servers split load; utilization per server = lambda/(c*mu)", BOX_TEAL)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=12)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: real systems
    y = section_header(c, 6, 6, "Queues in Real Systems",
                       "Spot the queue, apply the law.")
    items = [("Thread pools", "fixed c servers; queue depth is your backpressure signal", BOX_BLUE),
             ("Load balancers", "distribute lambda across servers to keep each rho low", BOX_GREEN),
             ("Backpressure", "slow producers when queues fill — don't let W explode", BOX_ORANGE),
             ("Load shedding", "when lambda > c*mu, drop or defer — protect latency for the rest", BOX_RED)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=12)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Queueing Theory — Remember",
                 ["A queue is arrivals (lambda), a waiting line, and service (mu); stability needs lambda < mu.",
                  "Little's law L = lambda*W holds for any system — measure two quantities, derive the third.",
                  "Latency explodes near 100% utilization; the knee around 70-80% is where planning lives.",
                  "M/M/1 gives closed forms: L = rho/(1-rho), W = 1/(mu - lambda).",
                  "Plan capacity for peak load with headroom; queues absorb bursts, they don't create capacity.",
                  "Backpressure and load shedding protect latency when demand exceeds service."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_crypto_math(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Crypto Math\nVisual Guide",
               "Modular arithmetic, RSA, Diffie-Hellman, and ECC —\nthe math that keeps secrets secret.",
               "Math Foundations", None); pg += 1

    # Step 1: modular arithmetic
    y = section_header(c, 1, 6, "Modular Arithmetic: Clock Math",
                       "a mod n = remainder after dividing a by n. Wraps around like a clock.")
    box(c, 72, 470, 225, 110, BOX_BLUE, "17 mod 12 = 5", "like 17:00 = 5 PM")
    box(c, 315, 470, 225, 110, BOX_GREEN, "(a+b) mod n", "= ((a mod n)+(b mod n)) mod n")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 430, "Addition, subtraction, multiplication all survive the wrap. Division needs inverses.")
    box(c, 72, 320, 468, 80, BOX_ORANGE, "MODULAR INVERSE", "a^(-1) mod n exists iff gcd(a,n)=1 — division's secret identity", font_size=12)
    note(c, 72, 220, 468, "Every public-key system lives inside a modular ring. The clock never lies.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: primes & trapdoors
    y = section_header(c, 2, 6, "Primes and Trapdoor Functions",
                       "Easy one way, hard the other — unless you hold the trapdoor.")
    box(c, 72, 470, 225, 100, BOX_GREEN, "EASY", "multiply two 1024-bit primes -> 2048-bit n")
    box(c, 315, 470, 225, 100, BOX_RED, "HARD", "factor n back into p and q — infeasible")
    box(c, 72, 340, 468, 80, BOX_PURP, "EULER'S THEOREM", "a^phi(n) = 1 mod n — the cycle that makes RSA decryption work", font_size=12)
    note(c, 72, 240, 468, "phi(n) = (p-1)(q-1) is easy if you know p, q — impossible-ish if you only know n.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: RSA keygen
    y = section_header(c, 3, 6, "RSA Key Generation",
                       "Three numbers become a lock anyone can use and only you can open.")
    box(c, 72, 500, 140, 80, BOX_BLUE, "1. Pick p, q", "large secret primes")
    arrow(c, 214, 540, 240, 540, color=ACCENT)
    box(c, 244, 500, 140, 80, BOX_GREEN, "2. n = p*q", "public modulus")
    arrow(c, 386, 540, 412, 540, color=ACCENT)
    box(c, 416, 500, 124, 80, BOX_ORANGE, "3. Pick e", "often 65537")
    box(c, 72, 390, 225, 80, BOX_TEAL, "PUBLIC (e, n)", "share with the world")
    box(c, 315, 390, 225, 80, BOX_RED, "PRIVATE (d, n)", "d = e^(-1) mod phi(n) — guard it")
    note(c, 72, 290, 468, "Security = factoring is hard. Quantum computers (Shor's) would break this — hence post-quantum work.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: RSA encrypt/decrypt
    y = section_header(c, 4, 6, "RSA Encrypt / Decrypt",
                       "Exponentiation modulo n, in both directions.")
    box(c, 72, 470, 225, 110, BOX_BLUE, "ENCRYPT", "c = m^e mod n  (public key)")
    box(c, 315, 470, 225, 110, BOX_GREEN, "DECRYPT", "m = c^d mod n  (private key)")
    arrow(c, 306, 575, 306, 470, color=ACCENT, label="")
    box(c, 72, 340, 468, 80, BOX_PURP, "WHY IT WORKS", "e*d = 1 mod phi(n), so m^(ed) = m mod n by Euler's theorem", font_size=12)
    note(c, 72, 240, 468, "In practice RSA encrypts a random session key, not the message — hybrid encryption.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: Diffie-Hellman
    y = section_header(c, 5, 6, "Diffie-Hellman Key Exchange",
                       "Two strangers agree on a secret over a public channel. Eavesdroppers learn nothing.")
    box(c, 72, 500, 225, 90, BOX_BLUE, "ALICE", "secret a -> sends g^a mod p")
    box(c, 315, 500, 225, 90, BOX_GREEN, "BOB", "secret b -> sends g^b mod p")
    arrow(c, 180, 498, 180, 440, color=ACCENT)
    arrow(c, 430, 498, 430, 440, color=ACCENT)
    box(c, 176, 350, 260, 80, BOX_PURP, "SHARED SECRET", "g^(ab) mod p — both compute it, nobody else can", font_size=12)
    note(c, 72, 250, 468, "Discrete log is the hard problem here. Ephemeral DH gives forward secrecy in TLS 1.3.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: ECC
    y = section_header(c, 6, 6, "ECC Intuition",
                       "Same discrete-log game, played on an elliptic curve — far smaller keys.")
    box(c, 72, 470, 468, 90, BOX_TEAL, "y^2 = x^3 + ax + b  (mod p)", "points on the curve form a group under 'chord-and-tangent' addition", font_size=12)
    box(c, 72, 340, 225, 100, BOX_BLUE, "PRIVATE", "secret scalar k")
    box(c, 315, 340, 225, 100, BOX_GREEN, "PUBLIC", "point k*G — scalar multiplication")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 310, "256-bit ECC ~= 3072-bit RSA security. Smaller keys, faster handshakes, happier phones.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Crypto Math — Remember",
                 ["Modular arithmetic wraps numbers on a clock; inverses exist when gcd(a,n) = 1.",
                  "Trapdoor functions are easy forward, hard backward without the secret — the basis of public-key crypto.",
                  "RSA: pick p, q; publish (e, n); keep d secret. Encrypt m^e, decrypt c^d mod n.",
                  "Diffie-Hellman lets strangers agree on a secret publicly; discrete logs protect it.",
                  "ECC gives RSA-grade security with far smaller keys via elliptic-curve discrete logs.",
                  "Hybrid encryption: public-key crypto protects a session key; symmetric crypto moves the data."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_browser_rendering(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "How Browsers Render\nVisual Guide",
               "HTML parsing, CSSOM, the render tree,\nlayout, paint, and composite — pixels from markup.",
               "Web Platform", None); pg += 1

    # Step 1: HTML parsing
    y = section_header(c, 1, 6, "Step 1: HTML Parsing -> DOM",
                       "Bytes become tokens, tokens become a tree of nodes.")
    box(c, 72, 500, 130, 80, BOX_BLUE, "BYTES", "raw HTML")
    arrow(c, 204, 540, 232, 540, color=ACCENT)
    box(c, 236, 500, 130, 80, BOX_GREEN, "TOKENS", "<div>, text...")
    arrow(c, 368, 540, 396, 540, color=ACCENT)
    box(c, 400, 500, 140, 80, BOX_ORANGE, "DOM TREE", "nodes")
    box(c, 72, 380, 468, 80, BOX_RED, "PARSER BLOCKING", "<script> without async/defer halts parsing until it runs", font_size=12)
    note(c, 72, 280, 468, "The DOM is the live, scriptable representation — what the HTML MEANS, not what it said.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: CSSOM
    y = section_header(c, 2, 6, "Step 2: CSS -> CSSOM",
                       "Stylesheets become a second tree: every node's computed styles.")
    box(c, 72, 500, 225, 90, BOX_TEAL, "CSS BYTES", "stylesheets, <style>, inline")
    arrow(c, 300, 540, 330, 540, color=ACCENT)
    box(c, 334, 500, 206, 90, BOX_PURP, "CSSOM", "selector -> declarations tree")
    box(c, 72, 380, 468, 80, BOX_RED, "RENDER BLOCKING", "CSS blocks rendering — the browser waits rather than flash unstyled", font_size=12)
    note(c, 72, 280, 468, "Inline critical CSS, defer the rest: the single biggest first-paint win on most sites.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: render tree
    y = section_header(c, 3, 6, "Step 3: DOM + CSSOM = Render Tree",
                       "Only visible nodes, each carrying its computed style.")
    box(c, 72, 500, 150, 90, BOX_BLUE, "DOM", "structure")
    box(c, 250, 500, 40, 90, BG, "+", "")
    box(c, 300, 500, 150, 90, BOX_TEAL, "CSSOM", "styles")
    arrow(c, 375, 545, 440, 545, color=ACCENT2, width=3)
    box(c, 380, 440, 160, 150, BOX_GREEN, "RENDER TREE", "visible nodes + styles")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 400, "display:none and <head> nodes are dropped — they render nothing.")
    note(c, 72, 300, 468, "visibility:hidden stays (takes space); display:none is gone from the tree entirely.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: layout/paint/composite
    y = section_header(c, 4, 6, "Step 4: Layout -> Paint -> Composite",
                       "Three phases turn the tree into pixels.")
    box(c, 72, 500, 150, 90, BOX_ORANGE, "LAYOUT", "geometry: x, y, width, height")
    arrow(c, 224, 545, 252, 545, color=ACCENT)
    box(c, 256, 500, 150, 90, BOX_RED, "PAINT", "fill pixels into layers")
    arrow(c, 408, 545, 436, 545, color=ACCENT)
    box(c, 440, 500, 100, 90, BOX_GREEN, "COMPOSITE", "GPU merges layers")
    box(c, 72, 380, 468, 80, BOX_PURP, "COST LADDER", "layout > paint > composite — animate transform/opacity to stay in composite", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: critical path
    y = section_header(c, 5, 6, "Step 5: The Critical Rendering Path",
                       "The minimum work before first pixels: optimize this chain.")
    box(c, 72, 520, 468, 70, BOX_BLUE, "HTML -> DOM", "stream-parse; scripts block unless async/defer", font_size=12)
    arrow(c, 306, 518, 306, 490, color=ACCENT)
    box(c, 72, 420, 468, 70, BOX_TEAL, "CSS -> CSSOM", "render-blocking; inline critical CSS", font_size=12)
    arrow(c, 306, 418, 306, 390, color=ACCENT)
    box(c, 72, 320, 468, 70, BOX_GREEN, "RENDER TREE -> LAYOUT -> PAINT", "first contentful paint happens here", font_size=12)
    note(c, 72, 220, 468, "FCP, LCP, CLS: the Core Web Vitals measure this pipeline's speed and stability.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: perf
    y = section_header(c, 6, 6, "Rendering Performance",
                       "Reflow is expensive; repaint is cheaper; composite is cheapest.")
    box(c, 72, 470, 225, 100, BOX_RED, "REFLOW", "geometry change — width, font, DOM insert")
    box(c, 315, 470, 225, 100, BOX_ORANGE, "REPAINT", "visual change — color, shadow (no geometry)")
    box(c, 72, 340, 468, 90, BOX_GREEN, "COMPOSITE-ONLY", "transform + opacity animate on the GPU — 60fps territory", font_size=12)
    box(c, 72, 230, 468, 70, BOX_BLUE, "will-change / layers", "promote sparingly — too many layers exhaust GPU memory", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Browser Rendering — Remember",
                 ["HTML parses into the DOM tree; scripts block parsing unless async/defer.",
                  "CSS builds the CSSOM — render-blocking by design to avoid unstyled flashes.",
                  "Render tree = visible DOM nodes plus computed styles; display:none is excluded.",
                  "Layout computes geometry, paint fills pixels, composite merges layers on the GPU.",
                  "The critical path is HTML->DOM + CSS->CSSOM -> render tree -> first paint; shorten it.",
                  "Animate transform and opacity to stay in the cheap composite phase."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_css_layout(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "CSS Layout\nVisual Guide",
               "Box model, flexbox, grid, positioning,\nand stacking contexts — layout, demystified.",
               "Web Platform", None); pg += 1

    # Step 1: box model
    y = section_header(c, 1, 6, "The Box Model",
                       "Every element is nested rectangles: content, padding, border, margin.")
    box(c, 150, 380, 312, 190, BOX_ORANGE, "MARGIN", "outside space", font_size=12)
    box(c, 175, 405, 262, 140, BOX_TEAL, "BORDER", "", font_size=11)
    box(c, 200, 430, 212, 90, BOX_GREEN, "PADDING", "", font_size=11)
    box(c, 240, 445, 132, 60, BOX_BLUE, "CONTENT", "text / image", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 340, "box-sizing: border-box -> width includes padding + border. Use it globally.")
    note(c, 72, 240, 468, "Margin collapse: adjacent vertical margins merge to the larger one — the classic 'where did my space go'.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: positioning
    y = section_header(c, 2, 6, "Positioning Schemes",
                       "How an element finds its place — and what it is placed relative to.")
    items = [("static", "default flow — top/left ignored", BOX_BLUE),
             ("relative", "offset from its normal spot; keeps its space", BOX_GREEN),
             ("absolute", "relative to nearest positioned ancestor; leaves flow", BOX_ORANGE),
             ("fixed", "relative to viewport; stays on scroll", BOX_RED),
             ("sticky", "flows until it hits the threshold, then sticks", BOX_TEAL)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 52, 150, 56, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(238, yy - 20, desc)
        yy -= 68
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: flexbox
    y = section_header(c, 3, 6, "Flexbox: One-Dimensional Layout",
                       "A container distributes space along a main axis; items can grow, shrink, wrap.")
    box(c, 72, 420, 468, 130, BOX_BLUE, "FLEX CONTAINER", "display:flex — main axis horizontal by default", font_size=12)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(100, 520, "flex-direction: row | column      justify-content: main-axis alignment")
    c.drawString(100, 500, "align-items: cross-axis alignment      flex-wrap: wrap to new lines")
    box(c, 72, 300, 225, 90, BOX_GREEN, "flex-grow", "take a share of free space")
    box(c, 315, 300, 225, 90, BOX_ORANGE, "flex-shrink", "give up space when cramped")
    note(c, 72, 200, 468, "Reach for flexbox for navbars, toolbars, centering, and any single row or column.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: grid
    y = section_header(c, 4, 6, "Grid: Two-Dimensional Layout",
                       "Define rows AND columns; place items on the grid explicitly.")
    c.setStrokeColor(INK); c.setLineWidth(1.2)
    for r in range(4):
        for col in range(3):
            x, yy = 130 + col * 130, 430 + r * 0
            pass
    # draw a 3x3 grid manually
    gx, gy, cell = 130, 400, 110
    for r in range(3):
        for col in range(3):
            x0, y0 = gx + col * (cell + 8), gy + (2 - r) * (cell + 8)
            c.setFillColor([BOX_BLUE, BOX_GREEN, BOX_ORANGE][(r + col) % 3])
            c.roundRect(x0, y0, cell, cell, 6, fill=1, stroke=1)
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 370, "grid-template-columns: 1fr 2fr 1fr   — fractional units split free space")
    c.drawString(72, 350, "grid-template-areas names regions: header header / sidebar main")
    box(c, 72, 230, 468, 70, BOX_PURP, "FLEX vs GRID", "flex = 1D flow; grid = 2D blueprint. Page skeleton -> grid.", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: stacking
    y = section_header(c, 5, 6, "Stacking Contexts & z-index",
                       "z-index only competes within the same stacking context.")
    box(c, 150, 460, 312, 110, BOX_PURP, "STACKING CONTEXT", "z-index: 1000 inside still loses to", font_size=11)
    box(c, 180, 480, 252, 60, BOX_BLUE, "child z-index: 9999", "trapped inside parent context", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 420, "New contexts: positioned + z-index, opacity < 1, transform, filter, will-change.")
    box(c, 72, 310, 468, 80, BOX_RED, "THE MODAL BUG", "'z-index: 99999 not working' = an ancestor created a context", font_size=12)
    note(c, 72, 210, 468, "Fix: move the overlay up the DOM or remove the ancestor's context-creating property.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: responsive units
    y = section_header(c, 6, 6, "Sizing & Responsive Units",
                       "Units that adapt instead of breaking.")
    items = [("rem / em", "relative to root / parent font size — scales with user settings", BOX_BLUE),
             ("vw / vh / %", "viewport- and container-relative lengths", BOX_GREEN),
             ("fr", "grid fractional unit — divides free space", BOX_TEAL),
             ("clamp()", "clamp(min, preferred, max) — fluid type without breakpoints", BOX_ORANGE),
             ("container queries", "style by the COMPONENT's size, not the viewport", BOX_PURP)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 56, 170, 60, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
        c.drawString(258, yy - 24, desc)
        yy -= 76
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "CSS Layout — Remember",
                 ["Every element is a box: content, padding, border, margin — use border-box globally.",
                  "Positioning: static flows, relative offsets, absolute/fixed break out, sticky hybridizes.",
                  "Flexbox lays out one dimension (rows or columns); great for components.",
                  "Grid lays out two dimensions; ideal for page skeletons and complex regions.",
                  "z-index only works within a stacking context — check ancestors before raising the number.",
                  "Prefer relative units (rem, %, fr, clamp) and container queries for resilient responsive design."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_js_runtime(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "JavaScript Runtime\nVisual Guide",
               "The event loop, task queues, closures,\nand the prototype chain — JS under the hood.",
               "Web Platform", None); pg += 1

    # Step 1: call stack
    y = section_header(c, 1, 6, "The Call Stack: One Thread",
                       "JS runs one thing at a time. Frames push on call, pop on return.")
    box(c, 226, 500, 160, 60, BOX_BLUE, "main()", "")
    box(c, 226, 430, 160, 60, BOX_GREEN, "fetchData()", "")
    box(c, 226, 360, 160, 60, BOX_ORANGE, "parse()", "")
    arrow(c, 400, 390, 400, 560, color=RED, label="stack grows")
    box(c, 72, 250, 468, 70, BOX_RED, "STACK OVERFLOW", "unbounded recursion — too many frames, the stack blows", font_size=12)
    note(c, 72, 150, 468, "Long synchronous work blocks EVERYTHING: rendering, input, timers. Never block the stack.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: event loop
    y = section_header(c, 2, 6, "The Event Loop",
                       "When the stack empties, the loop pulls the next task from the queue.")
    box(c, 72, 500, 150, 90, BOX_BLUE, "CALL STACK", "running now")
    box(c, 246, 500, 150, 90, BOX_GREEN, "TASK QUEUE", "waiting callbacks")
    box(c, 420, 500, 120, 90, BOX_ORANGE, "EVENT LOOP", "the pump")
    arrow(c, 320, 545, 396, 545, color=ACCENT)
    arrow(c, 480, 500, 480, 440, color=ACCENT)
    arrow(c, 480, 420, 150, 420, color=ACCENT)
    arrow(c, 150, 420, 150, 498, color=ACCENT)
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 380, "Loop: stack empty? -> take oldest task -> run to completion -> repeat.")
    note(c, 72, 280, 468, "Tasks run to COMPLETION — no preemption. A 2-second task freezes the page for 2 seconds.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: micro vs macro
    y = section_header(c, 3, 6, "Microtasks vs Macrotasks",
                       "Two queues, strict priority: drain ALL microtasks before the next macrotask.")
    box(c, 72, 470, 225, 110, BOX_PURP, "MICROTASKS", "promise.then, queueMicrotask — run ASAP")
    box(c, 315, 470, 225, 110, BOX_BLUE, "MACROTASKS", "setTimeout, I/O, UI events — one per loop turn")
    box(c, 72, 340, 468, 80, BOX_ORANGE, "ORDER", "macrotask -> ALL its microtasks -> render? -> next macrotask", font_size=12)
    note(c, 72, 240, 468, "Promise chains starving the loop: microtasks can delay rendering indefinitely. Yield with setTimeout(0).")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: closures
    y = section_header(c, 4, 6, "Closures: Functions Remember Scope",
                       "A function carries its birth environment wherever it goes.")
    box(c, 72, 480, 200, 110, BOX_BLUE, "OUTER SCOPE", "let count = 0")
    box(c, 300, 480, 200, 110, BOX_GREEN, "INNER FN", "returns () => ++count")
    arrow(c, 350, 478, 350, 420, color=ACCENT, label="captures")
    box(c, 176, 330, 260, 80, BOX_PURP, "CLOSURE", "fn + its captured variables — private state", font_size=12)
    note(c, 72, 230, 468, "Modules, callbacks, memoization, React hooks: all closures. Watch for accidental retention -> memory leaks.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: prototype chain
    y = section_header(c, 5, 6, "The Prototype Chain",
                       "Property lookup walks up: object -> prototype -> ... -> null.")
    box(c, 196, 520, 220, 70, BOX_BLUE, "myObj", "own props checked first")
    arrow(c, 306, 518, 306, 480, color=ACCENT, label="__proto__")
    box(c, 196, 410, 220, 70, BOX_GREEN, "MyClass.prototype", "shared methods live here")
    arrow(c, 306, 408, 306, 370, color=ACCENT, label="__proto__")
    box(c, 196, 300, 220, 70, BOX_ORANGE, "Object.prototype", "toString, hasOwnProperty...")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 260, "class syntax is sugar over this chain. Methods on the prototype are shared, not copied.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: async model
    y = section_header(c, 6, 6, "async/await: Syntax Over the Loop",
                       "No new threads — just promises scheduled on the queues you already know.")
    box(c, 72, 500, 468, 80, BOX_TEAL, "async function", "pauses at await; resumes as a microtask when the promise settles", font_size=12)
    box(c, 72, 390, 225, 90, BOX_BLUE, "SEQUENTIAL", "await a; await b — b waits for a")
    box(c, 315, 390, 225, 90, BOX_GREEN, "PARALLEL", "Promise.all([a, b]) — both in flight")
    note(c, 72, 290, 468, "await in a loop is the classic perf bug: independent calls should be Promise.all'd.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "JS Runtime — Remember",
                 ["One thread, one call stack: long sync work blocks rendering and input.",
                  "The event loop pumps tasks from the queue whenever the stack empties.",
                  "Microtasks (promises) drain fully before the next macrotask (timers, I/O).",
                  "Closures bundle a function with its birth scope — private state and the basis of modules.",
                  "Property lookup walks the prototype chain; class is sugar over prototypes.",
                  "async/await schedules on the same queues — use Promise.all for independent work."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_web_security(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Web Security\nEssentials",
               "CSP, CORS, cookie flags, and HTTPS —\nthe browser's defense layers, explained visually.",
               "Web Platform", None); pg += 1

    # Step 1: threat model
    y = section_header(c, 1, 6, "The Browser Threat Model",
                       "Your page runs attacker-influenced content: user input, third-party scripts, network foes.")
    box(c, 72, 500, 150, 90, BOX_RED, "ATTACKER", "injects scripts, sniffs traffic")
    arrow(c, 224, 545, 252, 545, color=RED, label="attacks")
    box(c, 256, 500, 150, 90, BOX_BLUE, "BROWSER", "your page + defenses")
    arrow(c, 408, 545, 436, 545, color=ACCENT, label="serves")
    box(c, 440, 500, 100, 90, BOX_GREEN, "SERVER", "your origin")
    box(c, 72, 380, 468, 80, BOX_ORANGE, "SAME-ORIGIN POLICY", "the foundation: origins can't read each other's data by default", font_size=12)
    note(c, 72, 280, 468, "Every defense below is a refinement of one idea: decide what each origin is allowed to do.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: HTTPS
    y = section_header(c, 2, 6, "HTTPS Everywhere",
                       "TLS gives confidentiality, integrity, and server authentication.")
    box(c, 72, 500, 225, 90, BOX_GREEN, "CONFIDENTIALITY", "encrypted — no eavesdropping")
    box(c, 315, 500, 225, 90, BOX_BLUE, "INTEGRITY", "tamper-evident — no silent edits")
    box(c, 72, 380, 468, 80, BOX_TEAL, "HSTS", "Strict-Transport-Security: browser refuses plain HTTP from now on", font_size=12)
    box(c, 72, 280, 468, 70, BOX_RED, "MIXED CONTENT", "HTTPS page loading HTTP subresources -> blocked or warned", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: CSP
    y = section_header(c, 3, 6, "Content Security Policy",
                       "A whitelist, delivered in a header, of what the page may load and run.")
    box(c, 72, 470, 468, 90, BOX_PURP, "Content-Security-Policy: default-src 'self'; script-src 'self' cdn.example", "only your origin + that CDN may run scripts", font_size=10)
    box(c, 72, 350, 225, 90, BOX_GREEN, "BLOCKS XSS PAYLOAD", "injected <script> from evil.com -> refused")
    box(c, 315, 350, 225, 90, BOX_ORANGE, "REPORT-ONLY MODE", "test policies without breaking the site")
    note(c, 72, 250, 468, "Start with report-only, watch violation reports, then enforce. Nonces beat 'unsafe-inline'.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: CORS
    y = section_header(c, 4, 6, "CORS: Who May Read Your Responses",
                       "The server opts in to cross-origin reads via Access-Control-Allow-Origin.")
    box(c, 72, 500, 200, 90, BOX_BLUE, "app.example", "wants api.example/data")
    arrow(c, 274, 545, 302, 545, color=ACCENT, label="Origin: app.example")
    box(c, 306, 500, 200, 90, BOX_GREEN, "api.example", "checks origin, replies with ACAO header")
    box(c, 72, 380, 468, 80, BOX_ORANGE, "PREFLIGHT (OPTIONS)", "non-simple requests ask permission first; server must answer", font_size=12)
    box(c, 72, 280, 468, 70, BOX_RED, "NEVER ACAO: * with credentials", "reflecting arbitrary origins + cookies = account takeover", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: cookies
    y = section_header(c, 5, 6, "Cookie Flags",
                       "Three attributes turn a tracking token into a hardened session cookie.")
    items = [("HttpOnly", "invisible to document.cookie — XSS can't steal it", BOX_BLUE),
             ("Secure", "sent only over HTTPS — no plaintext leaks", BOX_GREEN),
             ("SameSite=Lax/Strict", "not sent on cross-site requests — CSRF killer", BOX_ORANGE)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 56, 190, 60, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(278, yy - 24, desc)
        yy -= 76
    box(c, 72, yy - 60, 468, 64, BOX_RED, "RECIPE", "Set-Cookie: sid=...; HttpOnly; Secure; SameSite=Lax; Path=/", font_size=10)
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: checklist
    y = section_header(c, 6, 6, "Secure Defaults Checklist",
                       "The headers and habits that stop 90% of web attacks.")
    items = [("HTTPS + HSTS", "encrypt everything, pin the upgrade", BOX_GREEN),
             ("CSP enforced", "script-src whitelist, no unsafe-inline", BOX_PURP),
             ("CORS minimal", "exact origins only; no wildcard with credentials", BOX_BLUE),
             ("Hardened cookies", "HttpOnly + Secure + SameSite", BOX_ORANGE),
             ("X-Content-Type-Options: nosniff", "stop MIME-sniffing attacks", BOX_TEAL),
             ("Input handling", "validate server-side; encode output; parameterize queries", BOX_RED)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 50, 200, 54, fill, name, "", font_size=11)
        c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
        c.drawString(288, yy - 18, desc)
        yy -= 66
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Web Security — Remember",
                 ["The same-origin policy is the foundation: origins are isolated by default.",
                  "HTTPS everywhere plus HSTS gives confidentiality, integrity, and upgrade pinning.",
                  "CSP whitelists executable content — the strongest practical XSS mitigation.",
                  "CORS is the server opting in to cross-origin reads; never wildcard origins with credentials.",
                  "HttpOnly + Secure + SameSite cookies resist theft and CSRF.",
                  "Layer the defaults: HSTS, CSP, tight CORS, hardened cookies, nosniff, server-side validation."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_http_caching(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "HTTP Caching\nVisual Guide",
               "Cache-Control, validators, and CDN interplay —\nserve bytes once, reuse them a million times.",
               "Web Platform", None); pg += 1

    # Step 1: hierarchy
    y = section_header(c, 1, 6, "The Cache Hierarchy",
                       "Every layer that can answer without bothering origin saves time and money.")
    box(c, 72, 500, 130, 90, BOX_BLUE, "BROWSER", "memory + disk cache")
    arrow(c, 204, 545, 232, 545, color=ACCENT, label="miss")
    box(c, 236, 500, 130, 90, BOX_GREEN, "CDN EDGE", "PoP near user")
    arrow(c, 368, 545, 396, 545, color=ACCENT, label="miss")
    box(c, 400, 500, 140, 90, BOX_ORANGE, "ORIGIN", "your server")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 460, "Hits get faster and cheaper as you move left. Design for edge hits.")
    note(c, 72, 360, 468, "Shared caches (CDN) vs private caches (browser): directives decide who may store what.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: Cache-Control
    y = section_header(c, 2, 6, "Cache-Control Directives",
                       "The response header that is really a policy language.")
    items = [("max-age=31536000", "fresh for a year — immutable assets", BOX_GREEN),
             ("no-cache", "store it, but revalidate every time", BOX_ORANGE),
             ("no-store", "never store — secrets, sensitive data", BOX_RED),
             ("public / private", "CDN may cache / browser-only", BOX_BLUE),
             ("stale-while-revalidate", "serve stale instantly, refresh in background", BOX_TEAL)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 52, 230, 56, fill, name, "", font_size=11)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(318, yy - 20, desc)
        yy -= 68
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: validators
    y = section_header(c, 3, 6, "Validators: ETag & Last-Modified",
                       "Fingerprints that let caches ask 'did this change?' instead of re-downloading.")
    box(c, 72, 470, 225, 110, BOX_PURP, "ETag: \"a3f9c1\"", "strong validator — hash of content")
    box(c, 315, 470, 225, 110, BOX_TEAL, "Last-Modified", "weak validator — timestamp granularity")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 430, "Strong validators compare bytes; weak ones (W/) compare 'semantically same'.")
    note(c, 72, 330, 468, "Content-hashed filenames (app.a3f9c1.js) are the ultimate validator: the name IS the version.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: conditional flow
    y = section_header(c, 4, 6, "Conditional Requests: The 304 Dance",
                       "Revalidate cheaply — a 304 means 'your copy is still good'.")
    box(c, 72, 500, 200, 80, BOX_BLUE, "CLIENT", "has stale copy + ETag")
    arrow(c, 274, 540, 302, 540, color=ACCENT, label="If-None-Match")
    box(c, 306, 500, 200, 80, BOX_GREEN, "SERVER", "compares ETag")
    arrow(c, 404, 498, 200, 420, color=GREEN, label="304 Not Modified (empty body)")
    box(c, 72, 330, 468, 80, BOX_ORANGE, "CHANGED -> 200 + new body", "unchanged -> 304, client reuses cache, resets freshness", font_size=12)
    note(c, 72, 230, 468, "A 304 saves the body bytes but still costs a round trip — pair with long max-age for hot assets.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: CDN interplay
    y = section_header(c, 5, 6, "CDN Interplay",
                       "Edge caches, shielding, and tiered caching multiply hit rates.")
    box(c, 72, 500, 150, 90, BOX_BLUE, "USER", "")
    arrow(c, 224, 545, 252, 545, color=ACCENT)
    box(c, 256, 500, 130, 90, BOX_GREEN, "EDGE PoP", "serves region")
    arrow(c, 388, 545, 416, 545, color=ACCENT, label="miss")
    box(c, 420, 500, 120, 90, BOX_ORANGE, "SHIELD", "one upstream fetch")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 460, "Without shielding, 50 edge misses = 50 origin hits (thundering herd).")
    box(c, 72, 350, 468, 80, BOX_TEAL, "Vary", "Vary: Accept-Encoding — cache a variant per header value", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: invalidation
    y = section_header(c, 6, 6, "Invalidation Strategies",
                       "The two hard problems: naming things, cache invalidation, and off-by-one errors.")
    items = [("Content hashing", "new content -> new filename; old URLs stay cached forever", BOX_GREEN),
             ("Short TTL + SWR", "HTML shell: max-age=60, stale-while-revalidate", BOX_BLUE),
             ("Purge API", "explicit CDN purge on deploy — use sparingly", BOX_ORANGE),
             ("Versioned paths", "/v2/... prefixes — atomic cutover", BOX_TEAL)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 200, 64, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(288, yy - 24, desc)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "HTTP Caching — Remember",
                 ["Caches layer: browser, CDN edge, shield, origin — design for hits at the edge.",
                  "Cache-Control is a policy language: max-age, no-cache, no-store, public/private, SWR.",
                  "ETag and Last-Modified let caches revalidate with cheap conditional requests.",
                  "304 Not Modified reuses the cached copy; content-hashed filenames beat validators entirely.",
                  "Shielding collapses edge misses into one origin fetch; Vary splits cache variants.",
                  "Invalidate by renaming (hashing), short TTLs on HTML, and purge APIs as a last resort."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_realtime_web(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Real-time Web\nVisual Guide",
               "Polling, SSE, and WebSockets — a decision guide\nwith protocol flows for live data.",
               "Web Platform", None); pg += 1

    # Step 1: polling
    y = section_header(c, 1, 6, "Polling: Ask Repeatedly",
                       "Client fires requests on a timer. Simple, wasteful, laggy.")
    box(c, 72, 500, 200, 90, BOX_BLUE, "CLIENT", "setInterval(fetch, 5000)")
    arrow(c, 274, 545, 302, 545, color=ACCENT, label="GET /updates")
    box(c, 306, 500, 200, 90, BOX_GREEN, "SERVER", "mostly: 'nothing new'")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 460, "Latency up to the interval. 12 req/min/client even when idle — multiply by users.")
    box(c, 72, 350, 468, 70, BOX_ORANGE, "USE WHEN", "rarely-changing data, tiny scale, zero infra appetite", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: long polling
    y = section_header(c, 2, 6, "Long Polling: Ask and Wait",
                       "Server holds the request open until data arrives or timeout.")
    box(c, 72, 500, 200, 90, BOX_BLUE, "CLIENT", "request held open")
    arrow(c, 274, 545, 302, 545, color=ACCENT, label="GET (hangs)")
    box(c, 306, 500, 200, 90, BOX_ORANGE, "SERVER", "waits for event, then responds")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 460, "Near-instant delivery, but each event costs a new connection + held server threads.")
    box(c, 72, 350, 468, 70, BOX_TEAL, "USE WHEN", "server->client only, moderate scale, no socket infra", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: SSE
    y = section_header(c, 3, 6, "Server-Sent Events: One-Way Stream",
                       "A long-lived HTTP response; the server pushes text/event-stream chunks.")
    box(c, 72, 500, 200, 90, BOX_GREEN, "SERVER", "event: price\\ndata: 42.10\\n\\n")
    arrow(c, 274, 545, 302, 545, color=GREEN, width=3, label="stream")
    box(c, 306, 500, 200, 90, BOX_BLUE, "BROWSER", "EventSource API, auto-reconnect")
    box(c, 72, 380, 468, 80, BOX_TEAL, "STRENGTHS", "HTTP-friendly (proxies, auth), automatic reconnection, simple", font_size=12)
    box(c, 72, 280, 468, 70, BOX_RED, "LIMIT", "server -> client only; ~6 connections per browser", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: websockets
    y = section_header(c, 4, 6, "WebSockets: Full-Duplex Socket",
                       "HTTP upgrades to a persistent bidirectional frame channel.")
    box(c, 72, 520, 200, 80, BOX_BLUE, "CLIENT", "new WebSocket(url)")
    arrow(c, 274, 560, 302, 560, color=ACCENT, label="Upgrade: websocket")
    box(c, 306, 520, 200, 80, BOX_GREEN, "SERVER", "101 Switching Protocols")
    c.setStrokeColor(ACCENT2); c.setLineWidth(3)
    c.line(150, 460, 430, 460)
    c.setFillColor(ACCENT2); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(290, 470, "persistent frame channel — either side sends anytime")
    box(c, 72, 350, 468, 80, BOX_PURP, "USE WHEN", "chat, games, collaborative editing — true bidirectional, low latency", font_size=12)
    note(c, 72, 250, 468, "Needs sticky sessions or shared pub/sub behind the LB; heartbeats detect dead peers.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: decision guide
    y = section_header(c, 5, 6, "Decision Guide",
                       "Match the pattern to the traffic shape.")
    rows = [("Polling", "5s+ staleness OK", "tiny", BOX_ORANGE),
            ("Long polling", "server->client, instant", "medium", BOX_TEAL),
            ("SSE", "feeds, tickers, logs", "large 1-way", BOX_GREEN),
            ("WebSockets", "bidirectional, <100ms", "large 2-way", BOX_PURP)]
    yy = y
    for name, use, scale, fill in rows:
        box(c, 72, yy - 52, 170, 56, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(258, yy - 16, use)
        c.drawString(258, yy - 34, "scale: " + scale)
        yy -= 68
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: scaling
    y = section_header(c, 6, 6, "Scaling Real-time",
                       "Connections are stateful — plan for it.")
    items = [("Connection fan-out", "one origin can't hold 1M sockets — shard across nodes", BOX_BLUE),
             ("Pub/sub backbone", "Redis/NATS/Kafka broadcast events to all socket servers", BOX_GREEN),
             ("Sticky or stateless", "route by user id, or keep zero per-connection state", BOX_ORANGE),
             ("Backpressure", "slow consumers get sampled/coalesced updates, not an unbounded buffer", BOX_RED)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 200, 64, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(288, yy - 24, desc)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Real-time Web — Remember",
                 ["Polling is simplest but wastes requests and adds interval latency.",
                  "Long polling gives near-instant server->client delivery at connection cost.",
                  "SSE streams server->client over plain HTTP with auto-reconnect — great for feeds.",
                  "WebSockets are full-duplex and lowest-latency; use for chat, games, collaboration.",
                  "Decide by direction, latency budget, and scale — not by hype.",
                  "Scale with sharded socket servers, a pub/sub backbone, and backpressure for slow clients."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_mobile_arch(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Mobile App Architecture\nVisual Guide",
               "Native vs cross-platform, lifecycles,\noffline-first sync, and push notifications.",
               "Mobile", None); pg += 1

    # Step 1: native vs cross
    y = section_header(c, 1, 6, "Native vs Cross-Platform",
                       "One codebase or two — the founding tradeoff.")
    box(c, 72, 470, 225, 110, BOX_BLUE, "NATIVE", "Swift/Kotlin — max perf, full APIs, 2 codebases")
    box(c, 315, 470, 225, 110, BOX_GREEN, "CROSS-PLATFORM", "Flutter/RN — 1 codebase, near-native UI, some gaps")
    box(c, 72, 340, 468, 80, BOX_ORANGE, "DECIDE BY", "platform-specific hardware/UX depth vs team size and speed", font_size=12)
    note(c, 72, 240, 468, "Cross-platform wins on velocity for CRUD apps; native wins for games, AR, and deep OS integration.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: lifecycles
    y = section_header(c, 2, 6, "App Lifecycles",
                       "The OS can kill your app anytime — design for interruption.")
    box(c, 72, 520, 130, 70, BOX_GREEN, "ACTIVE", "")
    arrow(c, 204, 555, 232, 555, color=ACCENT, label="home")
    box(c, 236, 520, 130, 70, BOX_ORANGE, "BACKGROUND", "")
    arrow(c, 368, 555, 396, 555, color=ACCENT, label="memory pressure")
    box(c, 400, 520, 140, 70, BOX_RED, "TERMINATED", "")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 480, "Save state on backgrounding. Restore on launch. Never assume you will be resumed.")
    box(c, 72, 380, 468, 70, BOX_TEAL, "iOS vs ANDROID", "suspended vs cached processes — same lesson, different names", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: UI architecture
    y = section_header(c, 3, 6, "UI Architecture: Navigation & State",
                       "Screens are a stack; state flows down, events flow up.")
    box(c, 72, 500, 150, 90, BOX_BLUE, "NAV STACK", "push/pop screens")
    box(c, 246, 500, 150, 90, BOX_GREEN, "STATE STORE", "single source of truth")
    box(c, 420, 500, 120, 90, BOX_PURP, "VIEW", "renders state")
    arrow(c, 320, 545, 420, 545, color=ACCENT, label="renders")
    arrow(c, 480, 500, 480, 440, color=ACCENT)
    arrow(c, 480, 420, 320, 420, color=ACCENT, label="events")
    note(c, 72, 280, 468, "Unidirectional data flow keeps complex screens debuggable — the pattern behind Redux, Bloc, and friends.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: offline-first
    y = section_header(c, 4, 6, "Offline-First Sync",
                       "Treat the network as an optimization, not a requirement.")
    box(c, 72, 500, 200, 90, BOX_GREEN, "LOCAL DB", "source of truth on device")
    arrow(c, 274, 545, 302, 545, color=ACCENT, label="sync")
    box(c, 306, 500, 200, 90, BOX_BLUE, "SERVER", "authoritative copy")
    box(c, 72, 380, 468, 80, BOX_ORANGE, "CONFLICTS", "last-write-wins vs CRDTs vs manual merge — pick per data type", font_size=12)
    box(c, 72, 280, 468, 70, BOX_TEAL, "QUEUE MUTATIONS", "outbox pattern: write locally, sync when online", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: push
    y = section_header(c, 5, 6, "Push Notifications",
                       "Your server -> platform service -> device — you never reach the phone directly.")
    box(c, 72, 500, 140, 90, BOX_BLUE, "YOUR SERVER", "")
    arrow(c, 214, 545, 242, 545, color=ACCENT, label="send")
    box(c, 246, 500, 140, 90, BOX_GREEN, "APNs / FCM", "platform push service")
    arrow(c, 388, 545, 416, 545, color=ACCENT, label="push")
    box(c, 420, 500, 120, 90, BOX_ORANGE, "DEVICE", "badge/alert")
    box(c, 72, 380, 468, 80, BOX_RED, "PERMISSION", "users opt in — one spammy blast and you are muted forever", font_size=12)
    note(c, 72, 280, 468, "Silent pushes wake the app for background sync; visible pushes must earn attention.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: distribution
    y = section_header(c, 6, 6, "Distribution & Release",
                       "Stores gate releases — plan the pipeline.")
    items = [("Beta channels", "TestFlight / Play internal tracks — real devices before launch", BOX_BLUE),
             ("Staged rollouts", "1% -> 10% -> 100%; halt on crash spikes", BOX_GREEN),
             ("Code signing", "certificates + provisioning — lose the key, lose the app", BOX_ORANGE),
             ("OTA updates", "JS/bundled assets can update instantly; native code needs review", BOX_TEAL)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 200, 64, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(288, yy - 24, desc)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Mobile Architecture — Remember",
                 ["Native maximizes platform depth; cross-platform maximizes team velocity — choose deliberately.",
                  "The OS can kill your app anytime: save on background, restore on launch.",
                  "Unidirectional data flow (state down, events up) keeps complex UIs debuggable.",
                  "Offline-first: local DB as truth, outbox queue for mutations, explicit conflict policy.",
                  "Push flows server -> APNs/FCM -> device; permission is precious — never spam.",
                  "Ship via beta tracks and staged rollouts; guard your signing keys."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_blockchain(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Blockchain Basics\nVisual Guide",
               "Blocks, hashes, Merkle trees, and consensus —\nhow trust works without a trusted party.",
               "Blockchain", None); pg += 1

    # Step 1: blocks & hashing
    y = section_header(c, 1, 6, "Blocks & Hashing: The Chain",
                       "Each block commits to the previous block's hash — tampering breaks the link.")
    for i in range(3):
        x = 72 + i * 165
        box(c, x, 460, 150, 130, [BOX_BLUE, BOX_GREEN, BOX_TEAL][i], f"Block {i+1}", f"prev: {['genesis', 'hash1', 'hash2'][i]}")
    arrow(c, 224, 525, 235, 525, color=ACCENT2, width=3)
    arrow(c, 389, 525, 400, 525, color=ACCENT2, width=3)
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 420, "Change one byte in Block 1 -> its hash changes -> Block 2's 'prev' no longer matches.")
    box(c, 72, 310, 468, 80, BOX_RED, "IMMUTABILITY", "rewriting history means recomputing every later block — infeasible at scale", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: merkle trees
    y = section_header(c, 2, 6, "Merkle Trees",
                       "Hash transactions pairwise up to one root — prove inclusion with log(n) hashes.")
    box(c, 226, 540, 160, 60, BOX_PURP, "Merkle Root", "in block header")
    arrow(c, 260, 538, 200, 500, color=ACCENT); arrow(c, 352, 538, 412, 500, color=ACCENT)
    box(c, 140, 440, 130, 60, BOX_BLUE, "Hash AB", "")
    box(c, 342, 440, 130, 60, BOX_BLUE, "Hash CD", "")
    for (x1, x2) in [(150, 205), (290, 345), (352, 407), (492, 452)]:
        pass
    arrow(c, 170, 438, 130, 400, color=ACCENT); arrow(c, 240, 438, 280, 400, color=ACCENT)
    arrow(c, 372, 438, 332, 400, color=ACCENT); arrow(c, 442, 438, 482, 400, color=ACCENT)
    for i, x in enumerate([72, 207, 342 - 65 + 65, 407]):
        pass
    box(c, 72, 340, 110, 56, BOX_GREEN, "Tx A", "")
    box(c, 202, 340, 110, 56, BOX_GREEN, "Tx B", "")
    box(c, 332, 340, 110, 56, BOX_GREEN, "Tx C", "")
    box(c, 462, 340, 78, 56, BOX_GREEN, "Tx D", "")
    note(c, 72, 240, 468, "Light clients verify a transaction with just the root + log(n) sibling hashes — no full block needed.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: transactions & mempool
    y = section_header(c, 3, 6, "Transactions & the Mempool",
                       "Signed intents wait in the mempool; miners/validators pick them into blocks.")
    box(c, 72, 500, 150, 90, BOX_BLUE, "WALLET", "signs tx with private key")
    arrow(c, 224, 545, 252, 545, color=ACCENT, label="broadcast")
    box(c, 256, 500, 150, 90, BOX_ORANGE, "MEMPOOL", "pending tx pool")
    arrow(c, 408, 545, 436, 545, color=ACCENT, label="selected")
    box(c, 440, 500, 100, 90, BOX_GREEN, "BLOCK", "confirmed")
    box(c, 72, 380, 468, 80, BOX_TEAL, "FEES", "higher fee -> picked sooner; fee market rations block space", font_size=12)
    note(c, 72, 280, 468, "Signatures prove authorization; the mempool is just a waiting room with an auction.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: PoW vs PoS
    y = section_header(c, 4, 6, "Consensus: PoW vs PoS",
                       "How strangers agree on one history without a referee.")
    box(c, 72, 470, 225, 110, BOX_ORANGE, "PROOF OF WORK", "burn electricity racing to find a valid hash")
    box(c, 315, 470, 225, 110, BOX_GREEN, "PROOF OF STAKE", "lock capital; validators chosen by stake, slashed if dishonest")
    box(c, 72, 340, 468, 80, BOX_BLUE, "SYBIL RESISTANCE", "both make fake identities expensive — via energy or via capital", font_size=12)
    box(c, 72, 240, 468, 70, BOX_RED, "51% ATTACK", "control the majority of work/stake -> rewrite recent history", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: finality
    y = section_header(c, 5, 6, "Finality: When Is It Really Done?",
                       "Probabilistic vs absolute — know which chain you are on.")
    box(c, 72, 470, 225, 110, BOX_ORANGE, "PROBABILISTIC", "PoW: deeper = safer; 6 confirmations ~ settled")
    box(c, 315, 470, 225, 110, BOX_GREEN, "ABSOLUTE", "BFT PoS: 2/3 vote -> finalized, never reverted")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 430, "Forks happen: two valid blocks at once. The fork-choice rule picks the canonical chain.")
    note(c, 72, 330, 468, "Exchanges wait N confirmations because finality is a confidence level, not a switch — on PoW chains.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: nodes
    y = section_header(c, 6, 6, "Nodes & the Network",
                       "No center: full nodes verify everything, light nodes verify proofs.")
    items = [("Full nodes", "store + validate every block — the network's immune system", BOX_BLUE),
             ("Light clients", "headers + Merkle proofs — phones and browsers", BOX_GREEN),
             ("Miners / validators", "produce blocks under the consensus rules", BOX_ORANGE),
             ("Gossip network", "blocks and txs flood peer-to-peer; no central relay", BOX_TEAL)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 200, 64, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(288, yy - 24, desc)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Blockchain Basics — Remember",
                 ["Blocks link by hash: each commits to its predecessor, making history tamper-evident.",
                  "Merkle trees compress thousands of transactions into one root with log(n) proofs.",
                  "Transactions are signed intents; the mempool auctions block space by fee.",
                  "PoW spends energy, PoS risks capital — both buy Sybil resistance for consensus.",
                  "Finality is probabilistic on PoW (deeper = safer) and absolute under BFT voting.",
                  "Full nodes verify everything; light clients verify proofs; gossip spreads it all."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_smart_contracts(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Smart Contracts\nVisual Guide",
               "EVM execution, the gas model, Solidity basics,\nand the vulnerabilities auditors hunt.",
               "Blockchain", None); pg += 1

    # Step 1: EVM
    y = section_header(c, 1, 6, "EVM Execution Model",
                       "A deterministic world computer: same input + same state = same output, everywhere.")
    box(c, 72, 500, 150, 90, BOX_BLUE, "TX INPUT", "to, data, value")
    arrow(c, 224, 545, 252, 545, color=ACCENT)
    box(c, 256, 500, 150, 90, BOX_PURP, "EVM", "stack machine, 256-bit words")
    arrow(c, 408, 545, 436, 545, color=ACCENT)
    box(c, 440, 500, 100, 90, BOX_GREEN, "NEW STATE", "storage updated")
    box(c, 72, 380, 468, 80, BOX_ORANGE, "DETERMINISM", "no randomness, no wall-clock, no network — consensus demands it", font_size=12)
    note(c, 72, 280, 468, "Every node replays every transaction. The EVM is slow by design — verifiability over speed.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: gas
    y = section_header(c, 2, 6, "The Gas Model",
                       "Every opcode has a price. You prepay; unused gas refunds.")
    box(c, 72, 500, 150, 90, BOX_ORANGE, "GAS LIMIT", "max you will spend")
    arrow(c, 224, 545, 252, 545, color=ACCENT, label="x")
    box(c, 256, 500, 150, 90, BOX_RED, "GAS PRICE", "bid per unit")
    arrow(c, 408, 545, 436, 545, color=ACCENT, label="=")
    box(c, 440, 500, 100, 90, BOX_GREEN, "FEE", "total cost")
    box(c, 72, 380, 468, 80, BOX_TEAL, "WHY GAS EXISTS", "halts the halting problem: infinite loops just run out of money", font_size=12)
    note(c, 72, 280, 468, "Storage writes (SSTORE) are the most expensive ops — minimize on-chain state.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: Solidity basics
    y = section_header(c, 3, 6, "Solidity Basics: Contract Anatomy",
                       "State variables, functions, and who may call them.")
    box(c, 72, 500, 468, 80, BOX_BLUE, "contract Vault {  uint balance;  ... }", "state lives on-chain forever", font_size=11)
    items = [("external/public", "callable from outside / anywhere", BOX_GREEN),
             ("internal/private", "only this contract / + derived", BOX_ORANGE),
             ("view / pure", "reads state / touches nothing — free to call off-chain", BOX_TEAL)]
    yy = 470
    for name, desc, fill in items:
        box(c, 72, yy - 52, 190, 56, fill, name, "", font_size=11)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(278, yy - 20, desc)
        yy -= 68
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: storage
    y = section_header(c, 4, 6, "Storage vs Memory vs Calldata",
                       "Three data locations, three cost profiles.")
    box(c, 72, 470, 468, 80, BOX_RED, "STORAGE", "persistent, on-chain — $$$$ (SSTORE ~20k gas)", font_size=12)
    box(c, 72, 370, 468, 80, BOX_GREEN, "MEMORY", "per-call scratch space — cheap, wiped after", font_size=12)
    box(c, 72, 270, 468, 80, BOX_BLUE, "CALLDATA", "read-only function inputs — cheapest", font_size=12)
    note(c, 72, 170, 468, "Audit rule of thumb: every storage write should justify its gas. Pack variables into 32-byte slots.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: vulnerabilities
    y = section_header(c, 5, 6, "Common Vulnerabilities",
                       "The hits auditors find again and again.")
    items = [("Reentrancy", "external call before state update -> drained (checks-effects-interactions!)", BOX_RED),
             ("Access control", "missing onlyOwner -> anyone calls admin functions", BOX_ORANGE),
             ("Oracle manipulation", "single-source price feeds get gamed — use TWAP/decentralized oracles", BOX_PURP),
             ("Integer issues", "pre-0.8 overflow/underflow; still watch rounding in DeFi math", BOX_TEAL),
             ("Front-running", "public mempool reveals intent — commit-reveal or private relays", BOX_BLUE)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 56, 170, 60, fill, name, "", font_size=11)
        c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
        c.drawString(258, yy - 24, desc)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: audits
    y = section_header(c, 6, 6, "Audits & Secure Patterns",
                       "How serious teams ship contracts that hold money.")
    items = [("Checks-Effects-Interactions", "update state BEFORE calling out — kills reentrancy", BOX_GREEN),
             ("Battle-tested libs", "OpenZeppelin for tokens, access control, upgrades", BOX_BLUE),
             ("Tests + fuzzing", "unit, invariant, and fuzz tests — Foundry/Hardhat", BOX_TEAL),
             ("External audit", "independent review, then bug bounty before real TVL", BOX_ORANGE)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 220, 64, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(308, yy - 24, desc)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Smart Contracts — Remember",
                 ["The EVM is a deterministic stack machine: same input and state, same result on every node.",
                  "Gas prices every opcode; you prepay, and infinite loops just run out of money.",
                  "Solidity: state variables persist; function visibility and mutability define the attack surface.",
                  "Storage is persistent and expensive; memory is per-call; calldata is cheapest.",
                  "Top vulnerabilities: reentrancy, access control, oracle manipulation, rounding, front-running.",
                  "Ship with checks-effects-interactions, audited libraries, fuzzing, external audit, and a bounty."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_hashing(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Hash Functions\nVisual Guide",
               "SHA, Merkle trees, password hashing,\nand collisions — fingerprints for data.",
               "Blockchain", None); pg += 1

    # Step 1: properties
    y = section_header(c, 1, 6, "What Makes a Hash Function",
                       "Arbitrary input in, fixed-size fingerprint out — with four promises.")
    items = [("Deterministic", "same input -> same output, every time", BOX_BLUE),
             ("Fixed size", "SHA-256: always 256 bits, input any length", BOX_GREEN),
             ("Avalanche", "flip one input bit -> ~half the output bits flip", BOX_ORANGE),
             ("One-way", "infeasible to invert or find collisions (for crypto hashes)", BOX_RED)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 180, 64, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(268, yy - 24, desc)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: SHA family
    y = section_header(c, 2, 6, "The SHA Family",
                       "NIST standards, growing digest sizes — and retirements.")
    box(c, 72, 470, 225, 110, BOX_GREEN, "SHA-256", "256-bit — Bitcoin, TLS, Git")
    box(c, 315, 470, 225, 110, BOX_TEAL, "SHA-512", "512-bit — bigger digest, 64-bit optimized")
    box(c, 72, 330, 225, 110, BOX_BLUE, "SHA-3", "sponge construction — different design, backup standard")
    box(c, 315, 330, 225, 110, BOX_RED, "SHA-1 / MD5", "BROKEN — collisions demonstrated, do not use")
    note(c, 72, 230, 468, "Broken != useless everywhere: MD5 still fine for non-adversarial checksums — but never for security.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: merkle trees
    y = section_header(c, 3, 6, "Merkle Trees",
                       "Pairwise hashing up to one root — the data structure of verifiable lists.")
    box(c, 226, 540, 160, 60, BOX_PURP, "Root", "commitment to all data")
    arrow(c, 270, 538, 210, 500, color=ACCENT); arrow(c, 342, 538, 402, 500, color=ACCENT)
    box(c, 150, 440, 130, 56, BOX_BLUE, "H12", "")
    box(c, 332, 440, 130, 56, BOX_BLUE, "H34", "")
    arrow(c, 180, 438, 140, 400, color=ACCENT); arrow(c, 250, 438, 290, 400, color=ACCENT)
    arrow(c, 362, 438, 322, 400, color=ACCENT); arrow(c, 432, 438, 472, 400, color=ACCENT)
    for i, x in enumerate([72, 207, 342, 462]):
        box(c, x, 340, 100 if i < 3 else 78, 56, BOX_GREEN, f"D{i+1}", "")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 300, "Prove D2 is in the set: reveal H(D1), H34, and the root — verifier recomputes.")
    note(c, 72, 200, 468, "Git commits, blockchains, certificate transparency: all Merkle trees underneath.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: password hashing
    y = section_header(c, 4, 6, "Password Hashing: Slow on Purpose",
                       "Fast hashes let attackers try billions of guesses per second. So we go slow.")
    box(c, 72, 470, 225, 110, BOX_RED, "SHA-256(password)", "GPU: billions/sec — cracked in hours")
    box(c, 315, 470, 225, 110, BOX_GREEN, "bcrypt / Argon2", "tunable work factor — thousands/sec by design")
    box(c, 72, 340, 468, 80, BOX_ORANGE, "SALT", "unique random per password — defeats rainbow tables", font_size=12)
    box(c, 72, 240, 468, 70, BOX_PURP, "PEPPER (optional)", "server-side secret mixed in — database leak alone is not enough", font_size=12)
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: integrity hashing
    y = section_header(c, 5, 6, "Data-Integrity Hashing: Fast on Purpose",
                       "Detect corruption and verify downloads — speed is the point here.")
    box(c, 72, 500, 200, 90, BOX_BLUE, "FILE", "1.4 GB ISO")
    arrow(c, 274, 545, 302, 545, color=ACCENT, label="SHA-256")
    box(c, 306, 500, 200, 90, BOX_GREEN, "DIGEST", "publish alongside")
    box(c, 72, 380, 468, 80, BOX_TEAL, "VERIFY", "recompute after download — match means intact (and authentic, if signed)", font_size=12)
    note(c, 72, 280, 468, "Same primitive, opposite goal from passwords: here fast verification is a feature, not a bug.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: collisions
    y = section_header(c, 6, 6, "Collisions & the Birthday Bound",
                       "With n-bit hashes, collisions appear after ~2^(n/2) tries — not 2^n.")
    box(c, 72, 470, 468, 90, BOX_RED, "BIRTHDAY PARADOX", "23 people -> 50% chance of a shared birthday (365 days)", font_size=12)
    box(c, 72, 350, 225, 100, BOX_ORANGE, "SHA-256", "collision at ~2^128 — still infeasible")
    box(c, 315, 350, 225, 100, BOX_RED, "MD5 (128-bit)", "collision at ~2^64 — demonstrated in practice")
    note(c, 72, 250, 468, "Digest size halves under birthday attacks: 256-bit hashes give 128-bit collision resistance.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Hash Functions — Remember",
                 ["Crypto hashes promise determinism, fixed size, avalanche, and one-wayness.",
                  "SHA-256/512 and SHA-3 are current standards; SHA-1 and MD5 are broken for security use.",
                  "Merkle trees commit to whole datasets with one root and log(n) inclusion proofs.",
                  "Password hashing must be SLOW (bcrypt/Argon2) and salted; fast hashes get brute-forced.",
                  "Integrity hashing must be FAST: verify downloads and detect corruption cheaply.",
                  "Birthday attacks halve effective strength: n-bit digests give ~n/2 bits of collision resistance."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_p2p(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "P2P Networks\nVisual Guide",
               "DHTs, BitTorrent swarming, gossip,\nand NAT traversal — systems without servers.",
               "Blockchain", None); pg += 1

    # Step 1: why p2p
    y = section_header(c, 1, 6, "Why Peer-to-Peer?",
                       "No center to fail, censor, or pay for — capacity grows with users.")
    box(c, 72, 470, 200, 110, BOX_RED, "CLIENT-SERVER", "server = bottleneck + single point of failure")
    box(c, 316, 470, 200, 110, BOX_GREEN, "PEER-TO-PEER", "every node is client AND server")
    c.setFillColor(ACCENT2)
    for (x, yy) in [(160, 350), (280, 380), (400, 350), (220, 280), (340, 280)]:
        c.circle(x, yy, 14, fill=1, stroke=0)
    c.setStrokeColor(ACCENT); c.setLineWidth(1.5)
    c.line(174, 350, 266, 380); c.line(294, 380, 386, 350)
    c.line(160, 336, 220, 294); c.line(400, 336, 340, 294); c.line(234, 280, 326, 280)
    note(c, 72, 180, 468, "Tradeoff: you gain resilience and scale, you lose easy coordination and consistent views.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: discovery
    y = section_header(c, 2, 6, "Peer Discovery & Bootstrapping",
                       "The chicken-and-egg problem: finding your first peer.")
    items = [("Bootstrap nodes", "hardcoded well-known peers — the on-ramp", BOX_BLUE),
             ("Peer exchange", "ask peers for their peer lists — the network teaches itself", BOX_GREEN),
             ("mDNS / LAN", "local discovery without any server at all", BOX_TEAL),
             ("DHT bootstrap", "once in the DHT, find everything by key", BOX_PURP)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 200, 64, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(288, yy - 24, desc)
        yy -= 80
    note(c, 72, 180, 468, "Bootstrap nodes are the last centralization — eclipse attacks target this step.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: Kademlia
    y = section_header(c, 3, 6, "Kademlia DHT",
                       "A distributed hash table: keys map to the 'closest' nodes by XOR distance.")
    box(c, 72, 500, 468, 80, BOX_PURP, "node id XOR key id = distance", "both are 160-bit numbers; XOR is the metric", font_size=12)
    box(c, 72, 390, 150, 90, BOX_BLUE, "k-buckets", "peers grouped by distance")
    arrow(c, 224, 435, 252, 435, color=ACCENT, label="lookup")
    box(c, 256, 390, 150, 90, BOX_GREEN, "ITERATIVE", "ask closest, get closer, repeat")
    box(c, 430, 390, 110, 90, BOX_ORANGE, "O(log n)", "hops to any key")
    note(c, 72, 290, 468, "BitTorrent, IPFS, and Ethereum discovery all run Kademlia variants. It just works at planetary scale.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: BitTorrent
    y = section_header(c, 4, 6, "BitTorrent Swarming",
                       "Split the file; everyone uploads what they have. Downloaders become uploaders.")
    box(c, 72, 500, 468, 80, BOX_BLUE, "FILE -> PIECES", "e.g. 1 GB -> 4096 x 256 KB pieces, each hash-verified", font_size=12)
    c.setFillColor(ACCENT2)
    for (x, yy) in [(180, 400), (320, 430), (460, 400)]:
        c.circle(x, yy, 20, fill=1, stroke=0)
    c.setFillColor(white); c.setFont(TITLE_FONT, 10)
    for i, (x, yy) in enumerate([(180, 400), (320, 430), (460, 400)]):
        c.drawCentredString(x, yy - 4, f"P{i+1}")
    c.setStrokeColor(GREEN); c.setLineWidth(2.5)
    c.line(200, 400, 300, 430); c.line(340, 430, 440, 400); c.line(200, 410, 440, 410)
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 350, "Tit-for-tat: upload to those who upload to you. Rarest-first piece selection.")
    note(c, 72, 250, 468, "Aggregate bandwidth grows with the swarm — the opposite of a server melting under load.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: gossip
    y = section_header(c, 5, 6, "Gossip Protocols",
                       "Rumors spread exponentially: each node tells a few random peers, repeatedly.")
    box(c, 72, 500, 130, 80, BOX_RED, "INFECTED", "has the update")
    arrow(c, 204, 540, 232, 540, color=ACCENT, label="tells k random")
    box(c, 236, 500, 130, 80, BOX_ORANGE, "PEERS", "some already know")
    arrow(c, 368, 540, 396, 540, color=ACCENT, label="repeat")
    box(c, 400, 500, 140, 80, BOX_GREEN, "CONVERGED", "everyone knows")
    box(c, 72, 380, 468, 80, BOX_TEAL, "O(log n) ROUNDS", "exponential spread reaches millions in ~20 rounds", font_size=12)
    note(c, 72, 280, 468, "Eventual consistency with zero coordination — blockchains and membership protocols gossip constantly.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: NAT traversal
    y = section_header(c, 6, 6, "NAT Traversal",
                       "Most peers hide behind NATs. Getting two of them to connect directly takes tricks.")
    items = [("Hole punching", "both dial out simultaneously; NATs open return paths (STUN)", BOX_BLUE),
             ("Relay (TURN)", "when punching fails, bounce through a relay — slower but reliable", BOX_ORANGE),
             ("UPnP / PCP", "ask the router to forward a port — works on home networks", BOX_GREEN),
             ("ICE", "try everything in order: host -> reflexive -> relayed", BOX_PURP)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 60, 180, 64, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 11)
        c.drawString(268, yy - 24, desc)
        yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "P2P Networks — Remember",
                 ["P2P trades easy coordination for resilience: capacity grows with the user base.",
                  "Bootstrapping solves peer discovery; guard it against eclipse attacks.",
                  "Kademlia DHTs route by XOR distance in O(log n) hops — the backbone of BitTorrent/IPFS.",
                  "BitTorrent swarms split files into verified pieces; tit-for-tat aligns incentives.",
                  "Gossip protocols spread updates exponentially with zero coordination.",
                  "NAT traversal stacks hole punching, relays, and ICE to connect peers directly."],
                 pg)
    c.save()
    print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    jobs = [
        (pdf_discrete_math, "bbg-discrete-math.pdf"),
        (pdf_linear_algebra, "bbg-linear-algebra.pdf"),
        (pdf_probability, "bbg-probability.pdf"),
        (pdf_statistics, "bbg-statistics.pdf"),
        (pdf_calculus_ml, "bbg-calculus-ml.pdf"),
        (pdf_info_theory, "bbg-info-theory.pdf"),
        (pdf_graph_theory, "bbg-graph-theory.pdf"),
        (pdf_queueing, "bbg-queueing.pdf"),
        (pdf_crypto_math, "bbg-crypto-math.pdf"),
        (pdf_browser_rendering, "bbg-browser-rendering.pdf"),
        (pdf_css_layout, "bbg-css-layout.pdf"),
        (pdf_js_runtime, "bbg-js-runtime.pdf"),
        (pdf_web_security, "bbg-web-security.pdf"),
        (pdf_http_caching, "bbg-http-caching.pdf"),
        (pdf_realtime_web, "bbg-realtime-web.pdf"),
        (pdf_mobile_arch, "bbg-mobile-arch.pdf"),
        (pdf_blockchain, "bbg-blockchain.pdf"),
        (pdf_smart_contracts, "bbg-smart-contracts.pdf"),
        (pdf_hashing, "bbg-hashing.pdf"),
        (pdf_p2p, "bbg-p2p.pdf"),
    ]
    for fn, name in jobs:
        fn(os.path.join(out, name))
    print(f"done: {len(jobs)} PDFs")
