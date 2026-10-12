#!/usr/bin/env python3
"""Retrofit IL-20 (Mathematics) modules to the IL-19 Multicloud course template.

Per-module: instructor-voice summary; notes -> [Concepts, Hands-on procedure,
Project brief, Honesty note]; cards unchanged; quiz explains get section refs.
Preserves ALL existing factual content (restructured, never deleted).
Atomic write (temp + os.replace); json.load before and after.
"""
import json, os, sys

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
PATH = os.path.join(BASE, 'il-20-mathematics.json')

def note(title, body):
    return {"title": title, "body": body}

HONESTY = (
    "Standard, established mathematics throughout — definitions, theorems, and procedures "
    "presented in original instructional prose; nothing here is invented. Every worked step is "
    "checkable by hand, and you should check it: recompute the examples yourself rather than "
    "taking my word for them. Practice material only — this course confers no certificate."
)

MODULES = []

# ---------------------------------------------------------------- Module 1
MODULES.append({
 "id": "m20-sets-logic",
 "summary": (
    "Welcome to IL-20, Mathematics for Engineers & Scientists. I'm your instructor for this course, "
    "and this is Module 1: Sets & Propositional Logic. Over the next few lessons we're going to build "
    "the logical language every proof in this course is written in — sets and their operations, "
    "propositions and connectives, truth tables, and quantifiers. By the end you'll read and write "
    "statements like \u2203x \u2200y P(x,y) without flinching, and you'll never confuse necessary with "
    "sufficient again."
 ),
 "notes": [
  note("Concepts",
   "- **set** \u2014 a collection of distinct objects; `x \u2208 A` means x is an element of A.\n"
   "- **union** \u2014 `A \u222a B`: everything in A or B.\n"
   "- **intersection** \u2014 `A \u2229 B`: everything in both A and B.\n"
   "- **difference** \u2014 `A \\ B`: everything in A but not B.\n"
   "- **complement** \u2014 `A\u1d9c`: everything in the universe not in A.\n"
   "- **power set** \u2014 `P(A)`: the set of all subsets; if `|A| = n`, then `|P(A)| = 2^n`.\n"
   "- **proposition** \u2014 a statement that is either true or false, never both.\n"
   "- **negation** \u2014 `\u00acp`: true exactly when p is false.\n"
   "- **conjunction** \u2014 `p \u2227 q`: true only when both are true.\n"
   "- **disjunction** \u2014 `p \u2228 q`: true when at least one is true (inclusive or).\n"
   "- **implication** \u2014 `p \u2192 q`: false only when p is true and q is false. This is not causation — "
   "it is a truth-functional claim: \u2018it is not the case that p holds and q fails.\u2019\n"
   "- **biconditional** \u2014 `p \u2194 q`: true when p and q agree.\n"
   "- **universal quantifier** \u2014 `\u2200x P(x)`: P holds for every x.\n"
   "- **existential quantifier** \u2014 `\u2203x P(x)`: P holds for at least one x. Negating a quantifier "
   "flips it: `\u00ac\u2200x P(x)` is equivalent to `\u2203x \u00acP(x)`; `\u2203x \u2200y P(x,y)` is generally "
   "not the same as `\u2200y \u2203x P(x,y)` — order matters. In the definition of a limit, the "
   "`\u2203\u03b4 \u2200x` ordering is the whole point.\n"
   "- **sufficient condition** \u2014 in `p \u2192 q`, p is sufficient for q.\n"
   "- **necessary condition** \u2014 in `p \u2192 q`, q is necessary for p. Conflating them is the most "
   "common logical error in engineering arguments: \u2018the tests pass\u2019 is not sufficient for \u2018the "
   "code is correct\u2019, and \u2018the code is correct\u2019 is not necessary for \u2018the tests pass.\u2019\n"
   "- **contrapositive** \u2014 `\u00acq \u2192 \u00acp`: logically equivalent to the original implication `p \u2192 q`.\n"
   "- **De Morgan's laws** \u2014 `(A \u222a B)\u1d9c = A\u1d9c \u2229 B\u1d9c`; `\u00ac(p \u2228 q) \u2261 \u00acp \u2227 \u00acq`: "
   "complement flips union/intersection; negation flips and/or."),
  note("Hands-on procedure",
   "Evaluate a compound proposition with a truth table — the mechanical procedure that settles "
   "any finite logical question:\n"
   "1. Count the distinct propositional variables (n); your table needs 2^n rows.\n"
   "2. List every combination of truth values, one row per combination.\n"
   "3. Work inside-out: compute each connective's column from its input columns.\n"
   "4. Read the final column — that is the proposition's truth value for each assignment.\n"
   "5. To test equivalence, build both tables side by side and compare final columns.\n"
   "Worked example: `(p \u2228 q) \u2192 (p \u2227 q)`. Row (T,T): T\u2192T = T. Row (T,F): antecedent T, "
   "consequent F, so T\u2192F = F. Row (F,T): same, F. Row (F,F): F\u2192F = T. The implication is false "
   "exactly on the mixed rows — which is why you check every row, not the ones that feel typical."),
  note("Project brief",
   "Specify the access rules for a small internal tool as propositions. Define two sets — users and "
   "resources — and write the authorization rule as a compound proposition over membership "
   "statements (e.g., `admin \u2228 (owner \u2227 \u00acsuspended)`). Build its truth table, then use De Morgan's "
   "laws to write the exact negation of your rule, and prove the two tables are complements. "
   "Deliverable: the rule, both truth tables, and one paragraph arguing whether your rule makes "
   "access the necessary or the sufficient condition — and which direction is safer when the rule "
   "is wrong."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Concepts section: implication truth table.",
  "Concepts section: set difference and intersection.",
  "Concepts section: quantifier order.",
  "Concepts section: modus tollens on necessary/sufficient.",
 ],
})

# ---------------------------------------------------------------- Module 2
MODULES.append({
 "id": "m20-proof-methods",
 "summary": (
    "Welcome to Module 2: Proof Methods. I'm your instructor, and this is the module where "
    "mathematics becomes a skill instead of a spectator sport. We're going to drill the four moves "
    "that prove theorems, verify algorithms, and certify loop invariants — direct proof, "
    "contrapositive, contradiction, and mathematical induction. By the end you'll look at a claim "
    "like \u2018the sum of the first n odd numbers is n\u00b2\u2019 and reach for the right tool without hesitation."
 ),
 "notes": [
  note("Concepts",
   "- **direct proof** \u2014 assume the hypotheses, unpack definitions, and derive the conclusion by "
   "valid steps. Example: write two even integers as `2k` and `2m`; their sum is `2(k+m)`, even by "
   "definition. Reach for contrapositive or contradiction when the definitions give you nothing to grab.\n"
   "- **contrapositive** \u2014 to prove `p \u2192 q`, prove `\u00acq \u2192 \u00acp` instead; useful when the "
   "negated conclusion is easier to work with (e.g., parity-style results like \u2018if n\u00b2 is even "
   "then n is even\u2019).\n"
   "- **proof by contradiction** \u2014 assume p and `\u00acq` together, then derive a statement that "
   "contradicts a known fact or itself; then `\u00acq` is impossible, so q holds.\n"
   "- **mathematical induction** \u2014 to prove P(n) for all natural n \u2265 n\u2080: prove the base case "
   "P(n\u2080), then the inductive step (assume P(k), prove P(k+1)).\n"
   "- **base case** \u2014 the proof of P(n\u2080), where the induction starts.\n"
   "- **inductive hypothesis** \u2014 the assumption P(k) for a fixed k, made inside the inductive step.\n"
   "- **inductive step** \u2014 the derivation of P(k+1) from the inductive hypothesis.\n"
   "- **strong induction** \u2014 the hypothesis assumes P(j) for all j \u2264 k; needed when P(k+1) "
   "depends on earlier cases, e.g., Fibonacci.\n"
   "- **loop invariant** \u2014 a property true before and after each loop iteration, proved by induction "
   "on the iteration count.\n"
   "- **recurrence relation** \u2014 a sequence defined by earlier terms, e.g., mergesort's "
   "`T(n) = 2T(n/2) + n`, solved and verified by the induction pattern.\n"
   "- **begging the question** \u2014 circular reasoning: using the conclusion as a premise — the most "
   "common flaw in novice proofs."),
  note("Hands-on procedure",
   "Carry out an induction proof, step by step:\n"
   "1. State P(n) precisely and choose n\u2080.\n"
   "2. Prove the base case P(n\u2080) by direct computation.\n"
   "3. Write the inductive hypothesis: assume P(k) for a fixed k.\n"
   "4. Derive P(k+1) from it, showing every algebraic step — no leaps.\n"
   "5. Conclude: P(n) holds for all n \u2265 n\u2080.\n"
   "Worked example: `1 + 2 + ... + n = n(n+1)/2`. Base n=1: 1 = 1\u00b72/2. Step: assume the formula for "
   "k, then adding (k+1) to both sides gives k(k+1)/2 + (k+1) = (k+1)(k+2)/2 — exactly the formula at "
   "k+1. Done."),
  note("Project brief",
   "Prove a loop invariant for a small algorithm of your choice — for example, binary search's "
   "\u2018if the target is present, it lies in [lo, hi]\u2019, or insertion sort's \u2018the prefix is sorted\u2019. "
   "Write the base case (invariant holds before the first iteration), the inductive step (each "
   "iteration preserves it), and the conclusion (the invariant plus the exit condition implies "
   "correctness). Deliverable: the invariant, the two proofs, and one paragraph naming the exact "
   "line where a plausible bug would break the step — induction finds bugs by forcing you to name "
   "what each iteration preserves."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Concepts section: the inductive hypothesis.",
  "Hands-on procedure section: choosing a proof strategy.",
  "Concepts section: circular reasoning.",
  "Hands-on procedure section: the odd-numbers induction.",
 ],
})

# ---------------------------------------------------------------- Module 3
MODULES.append({
 "id": "m20-counting",
 "summary": (
    "Welcome to Module 3: Counting & Combinatorics. I'm your instructor, and this module answers the "
    "question \u2018how many?\u2019 — the mathematics behind password spaces, hash collisions, and every "
    "probability computation you'll meet in Module 12. Product and sum rules, permutations, "
    "combinations, the binomial theorem, and the pigeonhole principle: by the end you'll count an "
    "8-bit string space in your sleep and know exactly why 367 people guarantee a shared birthday."
 ),
 "notes": [
  note("Concepts",
   "- **product rule** \u2014 if a task has k stages with n\u1d62, n\u2082, \u2026, n\u2096 options, total outcomes = "
   "n\u1d62\u00b7n\u2082\u00b7\u2026\u00b7n\u2096. An n-bit string has `2^n` possibilities; counting them is the same as "
   "counting subsets of an n-element set.\n"
   "- **sum rule** \u2014 if two tasks are disjoint, the total count is the sum of their counts.\n"
   "- **permutation** \u2014 `P(n,k) = n!/(n\u2212k)!`: ordered selection of k from n.\n"
   "- **combination** \u2014 `C(n,k) = n!/(k!(n\u2212k)!)`: unordered selection of k from n.\n"
   "- **ordering test** \u2014 rule of thumb: ask \u2018does rearranging change the outcome?\u2019 If yes, "
   "permutation; if no, combination. Choosing a 3-person committee from 10: C(10,3) = 120. "
   "Assigning them president/VP/treasurer: P(10,3) = 720.\n"
   "- **binomial theorem** \u2014 `(x+y)^n = \u03a3 C(n,k) x^(n\u2212k) y^k` for k=0..n.\n"
   "- **Pascal's identity** \u2014 `C(n,k) = C(n\u22121,k\u22121) + C(n\u22121,k)`: builds the triangle row by row.\n"
   "- **subset count** \u2014 setting x=y=1 in the binomial theorem gives `\u03a3 C(n,k) = 2^n`: the number "
   "of subsets of an n-element set, matching the product rule.\n"
   "- **pigeonhole principle** \u2014 if n+1 items go into n boxes, some box holds at least 2 items. "
   "Generalization: with N items and k boxes, some box holds at least \u2308N/k\u2309 items. Used constantly "
   "in hashing (collisions are unavoidable when keys exceed slots), scheduling, and lower-bound arguments."),
  note("Hands-on procedure",
   "Choose the right counting formula:\n"
   "1. Ask the ordering question: does rearranging change the outcome? Yes \u2192 permutation `P(n,k)`; "
   "no \u2192 combination `C(n,k)`.\n"
   "2. Is repetition allowed? Then it's the product rule: n^k (e.g., passwords).\n"
   "3. Are the cases disjoint alternatives? Add them (sum rule).\n"
   "4. Compute: expand the factorials and cancel before multiplying.\n"
   "Worked example: unordered 4-person team from 9 people. Order within the team doesn't matter "
   "\u2192 combination: C(9,4) = 9!/(4!5!) = (9\u00b78\u00b77\u00b76)/(4\u00b73\u00b72\u00b71) = 126."),
  note("Project brief",
   "You are sizing a system. (a) A password policy requires length 6 over 26 lowercase letters — "
   "compute the password space and, assuming an attacker tries 10^9 guesses per second, the "
   "expected time to exhaust it. (b) A hash table has k slots and will hold N keys — use the "
   "generalized pigeonhole principle to state exactly when collisions become unavoidable and how "
   "many items the fullest slot must hold. Deliverable: both computations with the formula choice "
   "justified by the ordering/repetition test from the Hands-on procedure section."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Hands-on procedure section: order doesn't matter, so combine.",
  "Concepts section: pigeonhole with 366 boxes.",
  "Concepts section: the binomial theorem.",
  "Hands-on procedure section: repetition allowed, use the product rule.",
 ],
})

# ---------------------------------------------------------------- Module 4
MODULES.append({
 "id": "m20-relations-functions",
 "summary": (
    "Welcome to Module 4: Relations & Functions. I'm your instructor. Functions are the mappings "
    "between structures — every API, every hash table, every encoding is one — and this module "
    "gives you the precise vocabulary: injective, surjective, bijective, composition, inverses, "
    "equivalence relations, and partitions. By the end you'll classify any mapping on sight and "
    "understand why congruence classes mod n are the foundation of the cryptography in Module 12's "
    "successor courses."
 ),
 "notes": [
  note("Concepts",
   "- **injective** \u2014 f: A \u2192 B is one-to-one if f(x\u1d62)=f(x\u2082) implies x\u1d62=x\u2082: distinct inputs "
   "map to distinct outputs.\n"
   "- **surjective** \u2014 onto: every y in B has some x with f(x)=y — the image covers B.\n"
   "- **bijective** \u2014 both injective and surjective: a perfect pairing, which is exactly when an "
   "inverse exists.\n"
   "- **inverse** \u2014 `f\u207b\u00b9: B \u2192 A` undoes f; exists if and only if f is bijective.\n"
   "- **composition** \u2014 `(g\u2218f)(x) = g(f(x))`: apply f first, then g. Associative but generally "
   "not commutative — order matters. If f and g are both bijective, g\u2218f is bijective with inverse "
   "f\u207b\u00b9\u2218g\u207b\u00b9 (note the reversed order).\n"
   "- **equivalence relation** \u2014 a relation ~ on A that is reflexive (x~x), symmetric (x~y \u21d2 y~x), "
   "and transitive (x~y, y~z \u21d2 x~z).\n"
   "- **equivalence class / partition** \u2014 every equivalence relation partitions A into disjoint "
   "equivalence classes.\n"
   "- **congruence mod n** \u2014 x \u2261 y (mod n) iff n divides x\u2212y; partitions the integers into n "
   "residue classes — the foundation of modular arithmetic used in cryptography.\n"
   "- **partial order** \u2014 reflexive, antisymmetric (x\u2264y, y\u2264x \u21d2 x=y), transitive: replace "
   "symmetric with antisymmetric. Task-dependency graphs, version ordering, and type hierarchies are "
   "partial orders; topological sort linearizes them."),
  note("Hands-on procedure",
   "Classify a function f: A \u2192 B:\n"
   "1. Injectivity: does f(x\u1d62)=f(x\u2082) force x\u1d62=x\u2082? Hunt for a counterexample — two distinct "
   "inputs with the same output.\n"
   "2. Surjectivity: pick an arbitrary y in B and try to solve f(x)=y. If some y has no preimage, "
   "not surjective.\n"
   "3. Both hold \u2192 bijective: an inverse exists, and finite A, B have equal cardinality.\n"
   "Worked example: f(x) = x\u00b3 \u2212 x on \u211d. f(0)=f(1)=f(\u22121)=0, so not injective. But it is a "
   "continuous cubic with limits \u00b1\u221e, hence attains every real value: surjective. Verdict: "
   "surjective only."),
  note("Project brief",
   "Model an organization's user\u2192role assignment as a function. Classify it (injective? "
   "surjective? bijective?) and justify each answer with the Hands-on procedure. Then define the "
   "equivalence relation \u2018same clearance level\u2019 on users, list its equivalence classes, and show "
   "they partition the user set. Deliverable: the classification with counterexamples where it "
   "fails, the classes, and one paragraph on what breaks operationally if the assignment function "
   "is not surjective onto the roles that must be staffed."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Hands-on procedure section: injectivity and surjectivity checks.",
  "Concepts section: equivalence relation properties.",
  "Concepts section: composition order.",
  "Concepts section: bijections preserve cardinality.",
 ],
})

# ---------------------------------------------------------------- Module 5
MODULES.append({
 "id": "m20-linear-algebra-1",
 "summary": (
    "Welcome to Module 5: Linear Algebra I — Vectors & Spaces. I'm your instructor, and we're entering "
    "the engine room: vectors, dot products, vector spaces, span, and linear independence — the "
    "geometric core behind graphics, ML features, and simulation. By the end you'll test "
    "independence mechanically, describe any subspace by its basis, and see why the projection "
    "formula is secretly doing least-squares fitting."
 ),
 "notes": [
  note("Concepts",
   "- **vector** \u2014 an ordered n-tuple in \u211d\u207f; addition and scalar multiplication are componentwise.\n"
   "- **dot product** \u2014 `u\u00b7v = \u03a3 u\u1d62v\u1d62 = |u||v|cos \u03b8`: measures alignment of u and v.\n"
   "- **norm** \u2014 `|v| = \u221a(v\u00b7v)`: the length of v.\n"
   "- **orthogonal** \u2014 two nonzero vectors are orthogonal iff their dot product is 0.\n"
   "- **vector space** \u2014 a set closed under addition and scalar multiplication, satisfying the vector "
   "axioms (associativity, zero vector, additive inverses, distributivity). Examples: \u211d\u207f, matrices of "
   "fixed size, polynomials of degree \u2264 n, functions \u211d \u2192 \u211d. Closure is the key test: is the sum "
   "of two members always a member?\n"
   "- **span** \u2014 the set of all linear combinations of a given set of vectors.\n"
   "- **linear independence** \u2014 v\u1d62..\u2096 are independent if `c\u1d62v\u1d62+\u2026+c\u2096v\u2096 = 0` forces "
   "all c\u1d62 = 0: no vector is a combination of the others. Any n+1 vectors in \u211d\u207f are dependent.\n"
   "- **basis** \u2014 an independent spanning set; every vector has a unique coordinate representation "
   "in a basis.\n"
   "- **dimension** \u2014 the number of vectors in any basis; dim(\u211d\u207f) = n.\n"
   "- **projection** \u2014 `proj_v(u) = ((u\u00b7v)/(v\u00b7v)) v`. This single formula powers least-squares "
   "fitting, Gram\u2013Schmidt orthogonalization, and similarity search: the dot product with a unit "
   "vector is the signed length of the projection."),
  note("Hands-on procedure",
   "Test a set of vectors for linear independence:\n"
   "1. Write `c\u1d62v\u1d62 + \u2026 + c\u2096v\u2096 = 0`.\n"
   "2. Expand into one scalar equation per coordinate — a homogeneous system in the c\u1d62.\n"
   "3. Solve it. Only the trivial solution (all c\u1d62 = 0) \u2192 independent.\n"
   "4. A nontrivial solution \u2192 dependent; the solution itself exhibits one vector as a combination "
   "of the others.\n"
   "Worked example: (1,2), (3,4) in \u211d\u00b2. c\u1d62(1,2)+c\u2082(3,4)=(0,0) gives c\u1d62+3c\u2082=0 and "
   "2c\u1d62+4c\u2082=0. From the first, c\u1d62=\u22123c\u2082; substituting: \u22126c\u2082+4c\u2082=0 \u21d2 c\u2082=0, "
   "c\u1d62=0. Independent."),
  note("Project brief",
   "Build a tiny similarity search. Represent five short documents as term-frequency vectors over a "
   "shared vocabulary, normalize each to a unit vector, and rank the documents by cosine similarity "
   "(dot product) against a query vector. Deliverable: the vectors, the ranked list, and one "
   "paragraph explaining — via the projection formula — why the dot product with a unit vector "
   "measures \u2018how much of the query lies along each document\u2019, and what breaks when two vocabulary "
   "terms are linearly dependent."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Hands-on procedure section: solving the dependence system.",
  "Concepts section: the dot product and angle.",
  "Concepts section: basis criteria.",
  "Concepts section: the projection formula.",
 ],
})

# ---------------------------------------------------------------- Module 6
MODULES.append({
 "id": "m20-linear-algebra-2",
 "summary": (
    "Welcome to Module 6: Linear Algebra II — Matrices. I'm your instructor. Matrices are the "
    "computational engine of applied mathematics: multiplication, transposes, determinants, "
    "inverses, and rank. By the end you'll multiply with correct dimensions in your sleep, invert a "
    "2\u00d72 by hand, read rank as \u2018how much redundancy is in this system\u2019, and — most practically — "
    "you'll know why you never compute an explicit inverse to solve Ax=b."
 ),
 "notes": [
  note("Concepts",
   "- **matrix multiplication** \u2014 if A is m\u00d7n and B is n\u00d7p, then AB is m\u00d7p with "
   "`(AB)\u1d62\u2c7c = \u03a3\u2096 A\u1d62\u2096B\u2096\u2c7c`: row i of A dotted with column j of B. The inner dimensions "
   "must match. Associative and distributive, but not commutative: AB \u2260 BA in general.\n"
   "- **transpose** \u2014 `(AB)\u1d5b = B\u1d5bA\u1d5b`: order reverses, like function composition.\n"
   "- **determinant** \u2014 measures signed volume scaling. 2\u00d72: `det [[a,b],[c,d]] = ad \u2212 bc`. "
   "3\u00d73: cofactor expansion along any row or column. det(A) \u2260 0 iff A is invertible; "
   "det(AB) = det(A)det(B). A zero determinant means the transformation collapses at least one dimension.\n"
   "- **inverse** \u2014 A\u207b\u00b9 satisfies AA\u207b\u00b9 = A\u207b\u00b9A = I. 2\u00d72: "
   "`[[a,b],[c,d]]\u207b\u00b9 = (1/(ad\u2212bc)) [[d,\u2212b],[\u2212c,a]]`. For larger matrices use Gauss\u2013Jordan "
   "elimination on [A|I]. `(AB)\u207b\u00b9 = B\u207b\u00b9A\u207b\u00b9`. Practical rule: never compute an explicit "
   "inverse to solve Ax=b — factor instead (LU/QR); inversion is slower and less stable.\n"
   "- **rank** \u2014 the number of linearly independent rows = number of independent columns = "
   "dimension of the column space. For Ax=b: rank(A) = rank([A|b]) means a solution exists; "
   "rank(A) = n (full column rank) means it is unique. Rank deficiency signals redundancy — or "
   "multicollinearity in data."),
  note("Hands-on procedure",
   "Invert a 2\u00d72 matrix and verify:\n"
   "1. Compute det = ad \u2212 bc. If it is 0, stop — the matrix is not invertible.\n"
   "2. Apply the formula: `(1/det) [[d, \u2212b], [\u2212c, a]]`.\n"
   "3. Multiply A\u00b7A\u207b\u00b9 and confirm you get the identity — never trust an unchecked inverse.\n"
   "Worked example: [[2,1],[1,3]]. det = 2\u00b73\u22121\u00b71 = 5. Inverse = (1/5)[[3,\u22121],[\u22121,2]]. "
   "Verify: [[2,1],[1,3]]\u00b7(1/5)[[3,\u22121],[\u22121,2]] = (1/5)[[5,0],[0,5]] = I. \u2713"),
  note("Project brief",
   "Set up a small linear system from a blend problem: two raw materials with known compositions must "
   "be mixed to hit target percentages. Write it as Ax=b, solve by Gaussian elimination with partial "
   "pivoting (show the row operations), and verify A\u00b7x = b. Then write one paragraph explaining why "
   "you solved it by elimination rather than forming A\u207b\u00b9 — citing the stability and cost reasons "
   "from the Concepts section — and what the rank of A tells you about whether the blend is uniquely "
   "determined."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Concepts section: the identity matrix.",
  "Hands-on procedure section: the 2\u00d72 determinant.",
  "Concepts section: the dimension rule for products.",
  "Concepts section: rank and the null space.",
 ],
})

# ---------------------------------------------------------------- Module 7
MODULES.append({
 "id": "m20-linear-algebra-3",
 "summary": (
    "Welcome to Module 7: Linear Algebra III — Eigenvalues. I'm your instructor, and this is where "
    "matrices reveal their hidden structure: eigenvalues, eigenvectors, diagonalization, and "
    "symmetric matrices. This is the mathematics behind PCA, stability analysis, and PageRank. By "
    "the end you'll solve det(A \u2212 \u03bbI) = 0 in your sleep and read \u2018\u03bb\u1d4f grows or decays?\u2019 as the "
    "fate of every linear dynamical system."
 ),
 "notes": [
  note("Concepts",
   "- **eigenvector** \u2014 a nonzero vector v with `Av = \u03bbv`: A stretches v without rotating it.\n"
   "- **eigenvalue** \u2014 the scalar \u03bb in `Av = \u03bbv`.\n"
   "- **characteristic equation** \u2014 `det(A \u2212 \u03bbI) = 0`; its roots are the eigenvalues. For 2\u00d72 "
   "this is a quadratic; roots may be complex.\n"
   "- **diagonalization** \u2014 A = PDP\u207b\u00b9 with D diagonal: then A\u1d4f = PD\u1d4fP\u207b\u00b9, and powers become "
   "trivial. Sufficient condition: n distinct eigenvalues for an n\u00d7n matrix. This is why eigenvalues "
   "govern long-term behavior — Markov chains, linear recurrences, and dynamical systems all reduce to "
   "\u2018\u03bb\u1d4f grows or decays?\u2019\n"
   "- **spectral theorem** \u2014 every real symmetric matrix has real eigenvalues and an orthonormal "
   "eigenbasis. Covariance matrices are symmetric, so PCA's principal components are real, orthogonal "
   "directions — no complex arithmetic, no defective cases.\n"
   "- **trace** \u2014 trace(A) = sum of diagonal entries = sum of eigenvalues.\n"
   "- **determinant via eigenvalues** \u2014 det(A) = product of eigenvalues.\n"
   "- **sanity-check example** \u2014 for [[4,1],[2,3]]: trace 7 and det 10, so the eigenvalues sum to 7 "
   "and multiply to 10 — they are 5 and 2."),
  note("Hands-on procedure",
   "Find the eigenvalues of a 2\u00d72 matrix:\n"
   "1. Form A \u2212 \u03bbI.\n"
   "2. Compute its determinant \u2014 a quadratic in \u03bb.\n"
   "3. Solve the quadratic; the roots are the eigenvalues (possibly complex).\n"
   "4. Sanity-check: do they sum to the trace and multiply to the determinant?\n"
   "Worked example: [[4,1],[2,3]]. det(A\u2212\u03bbI) = (4\u2212\u03bb)(3\u2212\u03bb)\u22122 = \u03bb\u00b2\u22127\u03bb+10 = "
   "(\u03bb\u22125)(\u03bb\u22122). Eigenvalues 5 and 2; check: 5+2=7=trace \u2713, 5\u00b72=10=det \u2713."),
  note("Project brief",
   "Analyze a 2-state Markov chain — e.g., customers switching between two brands each month with a "
   "given transition matrix. Find its eigenvalues and eigenvectors, diagonalize the transition "
   "matrix, and predict the long-run market share. Deliverable: the eigenvalues, the diagonalized "
   "form, the steady state, and one paragraph explaining which eigenvalue governs the transient "
   "decay and how fast the chain forgets its starting state (| \u03bb\u2082 |^k)."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Concepts section: diagonal matrices.",
  "Hands-on procedure section: the characteristic quadratic.",
  "Concepts section: the eigenvector definition.",
  "Concepts section: the spectral theorem.",
 ],
})

# ---------------------------------------------------------------- Module 8
MODULES.append({
 "id": "m20-calculus-1",
 "summary": (
    "Welcome to Module 8: Calculus I — Limits & Derivatives. I'm your instructor. This is the "
    "mathematics of change: limits, continuity, the derivative as a rate of change, and the "
    "differentiation rules. The chain rule you drill here is the same chain rule that backpropagation "
    "computes — every ML gradient in Module 16 traces back to this module. By the end you'll "
    "differentiate composites mechanically and locate extrema with confidence."
 ),
 "notes": [
  note("Concepts",
   "- **limit** \u2014 `lim(x\u2192a) f(x) = L` means f(x) can be made arbitrarily close to L by taking x "
   "close to a.\n"
   "- **continuity** \u2014 f is continuous at a if the limit equals f(a).\n"
   "- **indeterminate form** \u2014 0/0 or \u221e/\u221e: try factoring, rationalizing, or l'H\u00f4pital's rule — "
   "differentiate numerator and denominator separately (check the form first!).\n"
   "- **l'H\u00f4pital's rule** \u2014 for 0/0 or \u221e/\u221e: lim f/g = lim f'/g' (if the latter exists).\n"
   "- **derivative** \u2014 `f'(x) = lim(h\u21920) [f(x+h) \u2212 f(x)]/h`: instantaneous rate of change, slope of "
   "the tangent line.\n"
   "- **power rule** \u2014 `(x\u207f)' = nx\u207f\u207b\u00b9`.\n"
   "- **product rule** \u2014 `(uv)' = u'v + uv'`.\n"
   "- **quotient rule** \u2014 `(u/v)' = (u'v \u2212 uv')/v\u00b2`.\n"
   "- **chain rule** \u2014 `[f(g(x))]' = f'(g(x))\u00b7g'(x)`: the workhorse — it is also what backpropagation "
   "computes.\n"
   "- **key derivatives** \u2014 memorize: `(e\u02e3)' = e\u02e3`; `(ln x)' = 1/x`; `(sin x)' = cos x`; "
   "`(cos x)' = \u2212sin x`; `(a\u02e3)' = a\u02e3 ln a`; `(arctan x)' = 1/(1+x\u00b2)`. Every ML loss gradient is "
   "built from these plus the chain rule.\n"
   "- **critical point** \u2014 f'(x) = 0 or undefined.\n"
   "- **first derivative test** \u2014 a sign change of f' classifies max/min.\n"
   "- **second derivative test** \u2014 at a critical point c: f''(c) > 0 \u21d2 local min; f''(c) < 0 \u21d2 "
   "local max.\n"
   "- **global extrema** \u2014 on a closed interval, check the critical points and the endpoints: global "
   "extrema live at critical points or boundaries."),
  note("Hands-on procedure",
   "Differentiate a composite function and find its extrema:\n"
   "1. Identify the outer and inner functions (peel the layers).\n"
   "2. Differentiate outside-in: derivative of the outer at the inner, times the inner's derivative — "
   "repeat for each layer.\n"
   "3. Set f'(x) = 0 (and note where f' is undefined) to find critical points.\n"
   "4. Classify each with the second derivative test; for a closed interval, also evaluate the "
   "endpoints.\n"
   "Worked example: f(x) = x\u00b3 \u2212 3x. f'(x) = 3x\u00b2 \u2212 3 = 0 \u21d2 x\u00b2 = 1 \u21d2 x = \u00b11. "
   "f''(x) = 6x: f''(\u22121) = \u22126 < 0 \u21d2 local max at \u22121; f''(1) = 6 > 0 \u21d2 local min at 1."),
  note("Project brief",
   "Optimize a cylindrical can of fixed volume V: choose radius r and height h to minimize the "
   "surface area (material cost). Write area as a function of r alone, differentiate, find the "
   "critical point, classify it, and check the boundary behavior as r \u2192 0 and r \u2192 \u221e. "
   "Deliverable: the model, the derivative work, the optimal h/r ratio, and one paragraph on why "
   "the endpoint check mattered — or didn't — for this problem."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Hands-on procedure section: the product rule.",
  "Concepts section: the chain rule.",
  "Concepts section: the fundamental trigonometric limit.",
  "Hands-on procedure section: finding critical points.",
 ],
})

# ---------------------------------------------------------------- Module 9
MODULES.append({
 "id": "m20-calculus-2",
 "summary": (
    "Welcome to Module 9: Calculus II — Integration. I'm your instructor. If derivatives are the "
    "mathematics of change, integrals are the mathematics of accumulation: antiderivatives, the "
    "Fundamental Theorem, integration techniques, and improper integrals. By the end you'll move "
    "fluently between a rate and its total — and you'll see why expected value in Module 12 is "
    "exactly the average-value idea from this module wearing a probability costume."
 ),
 "notes": [
  note("Concepts",
   "- **antiderivative** \u2014 F with F' = f; determined up to an additive constant.\n"
   "- **FTC Part 1** \u2014 if F(x) = \u222b[a\u2192x] f(t) dt, then F'(x) = f(x): differentiation undoes "
   "accumulation.\n"
   "- **FTC Part 2** \u2014 `\u222bx[a\u2192b] f = F(b) \u2212 F(a)` for any antiderivative F: evaluate definite "
   "integrals by finding antiderivatives instead of Riemann sums.\n"
   "- **substitution** \u2014 `\u222b f(g(x)) g'(x) dx = \u222b f(u) du` with u = g(x): the chain rule in reverse.\n"
   "- **integration by parts** \u2014 `\u222b u dv = uv \u2212 \u222b v du`: choose u by LIATE priority.\n"
   "- **LIATE** \u2014 Logarithmic, Inverse trig, Algebraic, Trigonometric, Exponential: the priority "
   "order for choosing u in integration by parts.\n"
   "- **partial fractions** \u2014 split rational functions into integrable pieces.\n"
   "- **improper integral** \u2014 an integral over an infinite interval or with a singularity, defined "
   "by limits. `\u222b[1\u2192\u221e] (1/x\u00b2) dx = lim(b\u2192\u221e) [1 \u2212 1/b] = 1` — converges. But "
   "`\u222b[1\u2192\u221e] (1/x) dx` diverges (grows like ln b). Always split at each singularity and take "
   "limits separately.\n"
   "- **area between curves** \u2014 `\u222b (top \u2212 bottom) dx`.\n"
   "- **volume of revolution** \u2014 disks: `\u03c0\u222b [f(x)]\u00b2 dx`.\n"
   "- **average value** \u2014 of f on [a,b]: `(1/(b\u2212a)) \u222b[a\u2192b] f`. Expected value in probability "
   "is exactly this idea with a density function."),
  note("Hands-on procedure",
   "Evaluate `\u222b x\u00b7e\u02e3 dx` by parts, then a definite version:\n"
   "1. Choose u and dv by LIATE: u = x (algebraic beats exponential), dv = e\u02e3 dx.\n"
   "2. Compute du = dx and v = e\u02e3.\n"
   "3. Apply uv \u2212 \u222bv du: xe\u02e3 \u2212 \u222be\u02e3 dx.\n"
   "4. Finish: xe\u02e3 \u2212 e\u02e3 + C = (x\u22121)e\u02e3 + C.\n"
   "5. For a definite integral, evaluate the antiderivative at the bounds (FTC Part 2) — or carry the "
   "bounds through the substitution/parts steps.\n"
   "Check: differentiate (x\u22121)e\u02e3: product rule gives e\u02e3 + (x\u22121)e\u02e3 = xe\u02e3 \u2713."),
  note("Project brief",
   "A server's network throughput is modeled by r(t) = 50 + 30 sin(\u03c0t/12) MB/s over a 24-hour "
   "period. Compute the total data transferred (integrate r over [0,24]) and the average throughput "
   "(average value), showing the substitution you used. Then consider the improper integral that "
   "arises for a decaying tail r(t) = 100e^(−t/10): set it up as a limit and decide convergence. "
   "Deliverable: both totals, the limit computation, and one paragraph on when \u2018integrate the rate\u2019 "
   "is the right model versus \u2018sum the samples\u2019."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Hands-on procedure section: integration by parts.",
  "Concepts section: FTC Part 2.",
  "Concepts section: FTC Part 1 with the chain rule.",
  "Concepts section: average value.",
 ],
})

# ---------------------------------------------------------------- Module 10
MODULES.append({
 "id": "m20-series",
 "summary": (
    "Welcome to Module 10: Sequences & Series. I'm your instructor. Infinite sums are how functions "
    "become computable: convergence tests tell you when a series means something, power series give "
    "you intervals of validity, and Taylor expansions turn e\u02e3 and sin x into polynomials your "
    "hardware can actually evaluate. By the end you'll wield the ratio test like a reflex and bound "
    "approximation error the way calculators guarantee digits."
 ),
 "notes": [
  note("Concepts",
   "- **divergence test** \u2014 if a\u2099 does not tend to 0, \u03a3a\u2099 diverges. (Terms \u2192 0 is necessary, "
   "not sufficient.)\n"
   "- **integral test** \u2014 compare \u03a3f(n) with \u222bf for positive decreasing f.\n"
   "- **p-series** \u2014 \u03a31/n\u1d56 converges iff p > 1.\n"
   "- **ratio test** \u2014 L = lim |a\u2099\u208a\u2081/a\u2099|: L<1 converges, L>1 diverges, L=1 inconclusive.\n"
   "- **alternating series test** \u2014 decreasing terms tending to 0 imply convergence.\n"
   "- **absolute vs conditional convergence** \u2014 absolute: \u03a3|a\u2099| converges. Conditional: \u03a3a\u2099 "
   "converges but \u03a3|a\u2099| diverges (e.g., the alternating harmonic series).\n"
   "- **power series** \u2014 `\u03a3 c\u2099(x\u2212a)\u207f` converges on an interval around a.\n"
   "- **radius of convergence** \u2014 from the ratio test: converge for |x\u2212a|<R, diverge outside; check "
   "endpoints individually. Example: `\u03a3 x\u207f/n!` has R = \u221e.\n"
   "- **Taylor series** \u2014 `f(x) = \u03a3 f\u207f(a)/n! \u00b7 (x\u2212a)\u207f`.\n"
   "- **Maclaurin series (essentials)** \u2014 `e\u02e3 = \u03a3 x\u207f/n!`; `sin x = \u03a3 (\u22121)\u207f x^(2n+1)/(2n+1)!`; "
   "`cos x = \u03a3 (\u22121)\u207f x^(2n)/(2n)!`; `1/(1\u2212x) = \u03a3 x\u207f` for |x|<1; "
   "`ln(1+x) = \u03a3 (\u22121)\u207f\u207a\u00b9 x\u207f/n` for |x|<1, x\u2260\u22121.\n"
   "- **Taylor's inequality** \u2014 |R\u2099(x)| \u2264 M|x\u2212a|\u207f\u207a\u00b9/(n+1)! where M bounds |f\u207f\u207a\u00b9|: "
   "pick n so the bound beats your tolerance — this is how calculators guarantee digits.\n"
   "- **alternating series error bound** \u2014 the error is at most the first dropped term."),
  note("Hands-on procedure",
   "Decide whether a series converges:\n"
   "1. Do the terms tend to 0? If not \u2192 diverges (divergence test). Stop.\n"
   "2. Recognize a p-series or geometric series \u2192 decide immediately.\n"
   "3. Factorials or exponentials in n \u2192 ratio test.\n"
   "4. Alternating signs with decreasing terms \u2192 alternating series test; then check \u03a3|a\u2099| for "
   "absolute vs conditional.\n"
   "Worked example: \u03a3 1/n\u00b2. Terms \u2192 0 \u2713. It is a p-series with p=2 > 1 \u2192 converges "
   "(absolutely, since all terms are positive)."),
  note("Project brief",
   "Approximate sin(0.5) with a Maclaurin polynomial and guarantee the error below 10\u207b\u2076. Choose n "
   "using Taylor's inequality (bound the next derivative on the interval), compute the partial sum, "
   "and state the certified error bound. Deliverable: your n, the approximation, the bound, and one "
   "paragraph on why the alternating-series bound would have been simpler here — and the case where "
   "it wouldn't apply."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Concepts section: p-series.",
  "Concepts section: the ratio test on the exponential series.",
  "Concepts section: the Maclaurin series of sin x.",
  "Concepts section: conditional convergence.",
 ],
})

# ---------------------------------------------------------------- Module 11
MODULES.append({
 "id": "m20-multivariable",
 "summary": (
    "Welcome to Module 11: Multivariable Calculus. I'm your instructor. Real problems have many "
    "variables: partial derivatives, gradients, the chain rule in higher dimensions, and "
    "optimization of functions of several variables. The gradient you meet here is the same object "
    "gradient descent follows in Module 16 — this module is where you learn what it means. By the "
    "end you'll find and classify critical points in 2D and optimize under constraints with "
    "Lagrange multipliers."
 ),
 "notes": [
  note("Concepts",
   "- **partial derivative** \u2014 `\u2202f/\u2202x` treats the other variables as constants.\n"
   "- **gradient** \u2014 `\u2207f = \u27e8f_x, f_y, f_z\u27e9`: points in the direction of steepest increase; its "
   "magnitude is the slope in that direction.\n"
   "- **directional derivative** \u2014 in unit direction u: `D_u f = \u2207f \u00b7 u`.\n"
   "- **multivariable chain rule** \u2014 if z = f(x,y) with x(t), y(t): `dz/dt = f_x dx/dt + f_y dy/dt`.\n"
   "- **total differential** \u2014 `dz = f_x dx + f_y dy`: the linear approximation — the seed of error "
   "propagation: small input errors scale by the partial derivatives.\n"
   "- **critical point (2D)** \u2014 `\u2207f = 0` (or undefined).\n"
   "- **second derivative test (D test)** \u2014 with `D = f_xx f_yy \u2212 (f_xy)\u00b2`: D>0 and f_xx>0 \u21d2 min; "
   "D>0 and f_xx<0 \u21d2 max; D<0 \u21d2 saddle point; D=0 inconclusive.\n"
   "- **saddle point** \u2014 a critical point that is a min in one direction and a max in another; the "
   "generic obstacle in neural-network training.\n"
   "- **Lagrange multipliers** \u2014 to optimize f(x,y) subject to g(x,y)=c, solve `\u2207f = \u03bb\u2207g` "
   "together with the constraint. Geometrically: at the optimum the level curves are tangent. "
   "Example: maximize xy subject to x+y=10 \u21d2 solving gives x=y=5, value 25."),
  note("Hands-on procedure",
   "Find and classify the critical points of f(x,y):\n"
   "1. Compute f_x and f_y; set both to zero and solve \u2014 these are the critical points.\n"
   "2. Compute the second partials f_xx, f_yy, f_xy.\n"
   "3. At each critical point evaluate D = f_xx f_yy \u2212 (f_xy)\u00b2.\n"
   "4. Classify: D>0 and f_xx>0 \u21d2 local min; D>0 and f_xx<0 \u21d2 local max; D<0 \u21d2 saddle; "
   "D=0 \u21d2 inconclusive, investigate directly.\n"
   "Worked example: f(x,y) = x\u00b2 \u2212 y\u00b2. \u2207f = \u27e82x, \u22122y\u27e9 = 0 \u21d2 (0,0). f_xx=2, f_yy=\u22122, "
   "f_xy=0 \u21d2 D = (2)(\u22122) \u2212 0 = \u22124 < 0 \u2014 saddle point."),
  note("Project brief",
   "A factory's output is modeled by P(x,y) = 40x + 60y \u2212 x\u00b2 \u2212 2y\u00b2 (x, y = labor and machine "
   "hours in hundreds), subject to the budget constraint 10x + 20y = 200. Solve with Lagrange "
   "multipliers: set up \u2207P = \u03bb\u2207g, solve the system with the constraint, and verify the "
   "solution is a maximum. Deliverable: the optimal (x, y), the maximum output, \u03bb, and one "
   "paragraph interpreting \u03bb as the shadow price — how much extra output one more budget dollar "
   "buys at the optimum."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Hands-on procedure section: computing partial derivatives.",
  "Concepts section: the gradient.",
  "Hands-on procedure section: the D test.",
  "Concepts section: Lagrange multipliers.",
 ],
})

# ---------------------------------------------------------------- Module 12
MODULES.append({
 "id": "m20-probability",
 "summary": (
    "Welcome to Module 12: Probability. I'm your instructor, and we're now reasoning under "
    "uncertainty: axioms, conditional probability, Bayes' theorem, random variables, and "
    "expectation. The single most valuable idea here is Bayes' rule done honestly — prior, "
    "likelihood, posterior — because base-rate neglect is the classic applied error, and you are "
    "about to see exactly how a 99%-accurate test can still be wrong 91% of the time."
 ),
 "notes": [
  note("Concepts",
   "- **Kolmogorov axioms** \u2014 P(A) \u2265 0; P(S) = 1; disjoint events add.\n"
   "- **complement rule** \u2014 P(A\u1d9c) = 1 \u2212 P(A).\n"
   "- **addition rule** \u2014 P(A\u222aB) = P(A)+P(B)\u2212P(A\u2229B).\n"
   "- **independence** \u2014 A and B are independent iff P(A\u2229B) = P(A)P(B): a property of the "
   "probability measure, not of intuition.\n"
   "- **conditional probability** \u2014 `P(A|B) = P(A\u2229B)/P(B)`.\n"
   "- **law of total probability** \u2014 P(B) = \u03a3 P(B|A\u1d62)P(A\u1d62).\n"
   "- **Bayes' theorem** \u2014 `P(A|B) = P(B|A)P(A)/P(B)`: update prior belief P(A) with evidence B.\n"
   "- **base-rate neglect** \u2014 ignoring P(A): the classic applied error. A 99%-accurate test on a "
   "1-in-10,000 condition still yields mostly false positives.\n"
   "- **random variable** \u2014 X maps outcomes to numbers.\n"
   "- **expectation** \u2014 E[X] = \u03a3 x\u1d62P(X=x\u1d62) (discrete) or \u222b x f(x)dx (continuous): the "
   "long-run average.\n"
   "- **linearity of expectation** \u2014 E[aX+bY] = aE[X]+bE[Y], even when X and Y are dependent.\n"
   "- **variance** \u2014 Var(X) = E[(X\u2212E[X])\u00b2] = E[X\u00b2]\u2212E[X]\u00b2.\n"
   "- **standard deviation** \u2014 \u03c3 = \u221aVar(X).\n"
   "- **binomial distribution** \u2014 Binomial(n,p): P(X=k) = C(n,k)p\u1d4f(1\u2212p)\u207f\u207b\u1d4f; E[X]=np, "
   "Var=np(1\u2212p).\n"
   "- **normal distribution** \u2014 N(\u03bc,\u03c3\u00b2): the bell curve; the 68\u201395\u201399.7 rule for \u00b11,2,3 \u03c3. "
   "Standardize with Z = (X\u2212\u03bc)/\u03c3. The normal is the limit of sums — which is the Central Limit "
   "Theorem, next module."),
  note("Hands-on procedure",
   "Run a Bayes update end to end:\n"
   "1. Name the prior: P(condition) before seeing evidence.\n"
   "2. Name the likelihoods: P(positive | condition) and P(positive | no condition).\n"
   "3. Compute the total probability of the evidence via the law of total probability.\n"
   "4. Posterior = prior \u00d7 likelihood / total.\n"
   "Worked example: a test is 99% accurate (1% false-positive rate); 1 in 1000 people have the "
   "condition. P(positive) = 0.99\u00d70.001 + 0.01\u00d70.999 = 0.01098. Posterior = 0.99\u00d70.001/0.01098 "
   "\u2248 0.09 \u2014 about 9%. The base rate dominates: most positives are false positives."),
  note("Project brief",
   "You are the analyst asked to sign off on a screening program. A test with 99% sensitivity and "
   "99% specificity is proposed for a condition with prevalence 1 in 10,000, then for a high-risk "
   "subpopulation with prevalence 1 in 50. Compute the positive predictive value in both cases "
   "with the Hands-on procedure, and write the one-page memo you'd send the decision-maker: the "
   "two numbers, what changes between them, and your recommendation on whether a positive result "
   "alone should trigger action. Deliverable: both posteriors and the memo."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Hands-on procedure section: the Bayes update.",
  "Concepts section: counting equally likely outcomes.",
  "Concepts section: expectation.",
  "Concepts section: independence and the addition rule.",
 ],
})

# ---------------------------------------------------------------- Module 13
MODULES.append({
 "id": "m20-statistics",
 "summary": (
    "Welcome to Module 13: Statistics. I'm your instructor. Probability told you how uncertainty "
    "behaves; statistics tells you how to learn from data anyway: sampling, the Central Limit "
    "Theorem, confidence intervals, and hypothesis testing. The two sentences that matter most: a "
    "95% confidence interval describes the procedure, not the parameter — and a p-value is "
    "P(data | H\u2080), never P(H\u2080 | data). Get those right and you'll avoid the two most expensive "
    "misreadings in applied science."
 ),
 "notes": [
  note("Concepts",
   "- **statistic** \u2014 a quantity computed from the sample (e.g., the sample mean x\u0304); estimates a "
   "parameter.\n"
   "- **parameter** \u2014 the unknown population quantity (e.g., \u03bc) the statistic estimates.\n"
   "- **Central Limit Theorem** \u2014 for iid samples with mean \u03bc and finite variance \u03c3\u00b2, x\u0304 is "
   "approximately N(\u03bc, \u03c3\u00b2/n) for large n — regardless of the population's shape. This is why "
   "averages of enough data behave normally.\n"
   "- **standard error** \u2014 of the mean: \u03c3/\u221an.\n"
   "- **confidence interval** \u2014 95% CI for \u03bc: `x\u0304 \u00b1 z*\u00b7\u03c3/\u221an` (z* \u2248 1.96; use t* for "
   "small n or estimated \u03c3). Correct interpretation: 95% of intervals constructed this way capture "
   "the true \u03bc — not \u2018there is a 95% chance \u03bc is in this interval.\u2019 Width shrinks as 1/\u221an: "
   "quadrupling the sample halves the width.\n"
   "- **hypothesis test** \u2014 H\u2080 (null) vs H\u2081 (alternative).\n"
   "- **p-value** \u2014 P(data at least this extreme | H\u2080 true): not P(H\u2080 true | data).\n"
   "- **rejection rule** \u2014 reject H\u2080 if p < \u03b1 (often 0.05).\n"
   "- **Type I error** \u2014 rejecting a true H\u2080 (rate \u03b1): a false positive.\n"
   "- **Type II error** \u2014 failing to reject a false H\u2080: a false negative (missing a real effect).\n"
   "- **power** \u2014 1 \u2212 P(Type II error).\n"
   "- **practical vs statistical significance** \u2014 a tiny effect can be statistically significant with "
   "enough data; always report effect sizes with uncertainty, not just p-values.\n"
   "- **correlation** \u2014 measures linear association (\u22121 \u2264 r \u2264 1); never establishes causation. "
   "Confounders, reverse causation, and selection effects produce correlations without causation. The "
   "honest pipeline: randomize (experiments), control (regression), or instrument."),
  note("Hands-on procedure",
   "Run a hypothesis test for two proportions (the A/B-test workhorse):\n"
   "1. State H\u2080 (no difference) and H\u2081, and fix \u03b1 = 0.05 before looking at the data.\n"
   "2. Compute the pooled proportion, the standard error of the difference, and the z-statistic.\n"
   "3. Convert z to a p-value.\n"
   "4. Reject H\u2080 iff p < \u03b1; then report the effect size and its confidence interval — the "
   "p-value alone is not a conclusion.\n"
   "Worked sketch: A converts 120/2000, B converts 150/2000. The two-proportion z-test gives "
   "p \u2248 0.04 < 0.05 \u21d2 reject H\u2080 at 5%: evidence B differs, direction favoring B — while "
   "reporting the 1.5-percentage-point effect size and its CI."),
  note("Project brief",
   "Design the analysis plan for an A/B test before any data is collected: two page variants, "
   "expected baseline conversion 6%, minimum detectable effect 1.5 percentage points. Choose the "
   "test (two-proportion z), pre-register \u03b1, compute the required sample size per variant for 80% "
   "power, and write the decision rule — including what you will conclude if p = 0.06. Deliverable: "
   "the plan, the sample-size computation, and one paragraph on why the decision rule is written "
   "before the data arrives (hint: the Concepts section on p-values)."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Concepts section: confidence-interval interpretation.",
  "Hands-on procedure section: the rejection rule.",
  "Concepts section: standard error.",
  "Concepts section: correlation is not causation.",
 ],
})

# ---------------------------------------------------------------- Module 14
MODULES.append({
 "id": "m20-graphs-recurrence",
 "summary": (
    "Welcome to Module 14: Graphs & Recurrences. I'm your instructor. Networks and algorithms live "
    "here: graph terminology, trees, traversal orders, and solving recurrence relations. BFS and DFS "
    "are the two verbs of graph algorithms, trees are the data structure that keeps showing up, and "
    "recurrences like T(n) = 2T(n/2)+n are how you prove an algorithm's cost. By the end you'll trace "
    "a traversal by hand and solve a linear recurrence by characteristic equation."
 ),
 "notes": [
  note("Concepts",
   "- **graph** \u2014 G=(V,E): vertices and edges.\n"
   "- **degree** \u2014 of v: the number of incident edges.\n"
   "- **handshaking lemma** \u2014 \u03a3 deg(v) = 2|E|: every edge contributes 2.\n"
   "- **path** \u2014 a walk with no repeated vertices; a **cycle** returns to its start.\n"
   "- **connected** \u2014 a path exists between every pair of vertices.\n"
   "- **complete graph** \u2014 K\u2099 has n(n\u22121)/2 edges.\n"
   "- **tree** \u2014 a connected acyclic graph. Equivalent characterizations: connected with n\u22121 "
   "edges; acyclic with n\u22121 edges; exactly one simple path between any two vertices.\n"
   "- **spanning tree** \u2014 a tree on all of G's vertices; minimum spanning trees (Kruskal/Prim) "
   "minimize total edge weight.\n"
   "- **BFS** \u2014 breadth-first search (queue): explores level by level — finds shortest paths in "
   "unweighted graphs.\n"
   "- **DFS** \u2014 depth-first search (stack/recursion): goes deep first — detects cycles, produces "
   "topological orderings.\n"
   "- **traversal cost** \u2014 both BFS and DFS visit each vertex and edge once: O(V+E). Choose BFS "
   "for shortest-path, DFS for structure (components, cycles, topo sort).\n"
   "- **recurrence relation** \u2014 defines a sequence by earlier terms: Fibonacci `F\u2099 = F\u2099\u208a\u2081 + "
   "F\u2099\u208a\u2082`, F\u2080=0, F\u2081=1.\n"
   "- **characteristic equation** \u2014 for a\u2099 = c\u1d62a\u2099\u208a\u2081 + c\u2082a\u2099\u208a\u2082, solve r\u00b2 = c\u1d62r + c\u2082.\n"
   "- **divide-and-conquer recurrence** \u2014 e.g., T(n) = 2T(n/2)+n solves to \u0398(n log n): mergesort's "
   "recurrence. The Master Theorem generalizes this."),
  note("Hands-on procedure",
   "Solve a linear recurrence with constant coefficients:\n"
   "1. Assume a\u2099 = r\u207f and substitute into the recurrence.\n"
   "2. Divide out the lowest power of r to get the characteristic equation.\n"
   "3. Solve for r; the general solution is a linear combination of the r\u207f terms (multiply by n "
   "for repeated roots).\n"
   "4. Use the base cases to solve for the constants.\n"
   "Worked example: a\u2099 = 5a\u2099\u208a\u2081 \u2212 6a\u2099\u208a\u2082. Assume r\u207f: r\u207f = 5r\u207f\u207b\u00b9 \u2212 6r\u207f\u207b\u00b2 \u21d2 "
   "r\u00b2 = 5r \u2212 6 \u21d2 r = 2, 3. General solution: a\u2099 = A\u00b72\u207f + B\u00b73\u207f; fit A, B to a\u2080, a\u2081."),
  note("Project brief",
   "Model a software build's task dependencies as a directed graph: 12 tasks with given "
   "prerequisites. (a) Produce a topological ordering via DFS and prove it is valid (every "
   "prerequisite precedes its dependent). (b) A recursive build step costs T(n) = 2T(n/2)+n on n "
   "files — solve the recurrence and state the asymptotic cost. Deliverable: the graph, the "
   "ordering with the DFS trace, the solved recurrence, and one paragraph on what a cycle in the "
   "dependency graph would mean operationally."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Concepts section: trees.",
  "Concepts section: the handshaking lemma.",
  "Concepts section: BFS.",
  "Hands-on procedure section: the characteristic equation.",
 ],
})

# ---------------------------------------------------------------- Module 15
MODULES.append({
 "id": "m20-numerical-methods",
 "summary": (
    "Welcome to Module 15: Numerical Methods. I'm your instructor. Closed forms fail more often "
    "than textbooks admit — this module is the honest toolkit for computing answers anyway: "
    "bisection, Newton's method, numerical integration, and error analysis. The mantra: guarantee "
    "first (bracket the root), then go fast (Newton inside the bracket). By the end you'll bound "
    "errors before you compute and distinguish a bad algorithm from a hard problem."
 ),
 "notes": [
  note("Concepts",
   "- **bisection** \u2014 if f is continuous with f(a)f(b) < 0, a root lies in (a,b). Halve repeatedly, "
   "keeping the sign change: after n steps the error is at most (b\u2212a)/2\u207f. Guaranteed but linear "
   "convergence — slow and sure. Always check the sign-change precondition; without it, bisection "
   "proves nothing.\n"
   "- **Newton's method** \u2014 `x\u2099\u208a\u2081 = x\u2099 \u2212 f(x\u2099)/f'(x\u2099)`: follow the tangent line to its "
   "x-intercept. Near a simple root it converges quadratically (correct digits roughly double per "
   "step). Requirements: a good starting guess, f'(x\u2099) \u2260 0, and smoothness. Bad starts diverge "
   "or cycle — pair with bisection bracketing for safety.\n"
   "- **trapezoidal rule** \u2014 h/2 \u00b7 [f\u2080 + 2f\u1d62 + \u2026 + 2f\u2099\u208a\u2081 + f\u2099], error O(h\u00b2).\n"
   "- **Simpson's rule** \u2014 (n even): h/3 \u00b7 [f\u2080 + 4f\u1d62 + 2f\u2082 + \u2026 + 4f\u2099\u208a\u2081 + f\u2099], error "
   "O(h\u2074): halving h cuts Simpson error ~16\u00d7. Simpson fits parabolas; it is exact for cubics too.\n"
   "- **truncation error** \u2014 error from the method's approximation (e.g., stopping a series, "
   "discretizing an integral).\n"
   "- **roundoff error** \u2014 error from finite floating-point precision.\n"
   "- **conditioning** \u2014 sensitivity of the problem itself: solving near-singular systems amplifies "
   "input errors.\n"
   "- **condition number** \u2014 \u03ba(A) = ||A||\u00b7||A\u207b\u00b9|| bounds the blowup. A stable algorithm on an "
   "ill-conditioned problem still gives garbage: distinguish the two."),
  note("Hands-on procedure",
   "Bracket a root, then polish it:\n"
   "1. Find [a,b] with f(a)f(b) < 0 — the sign change guarantees a root exists.\n"
   "2. Bisect to a coarse tolerance: n steps give error \u2264 (b\u2212a)/2\u207f.\n"
   "3. Switch to Newton's method inside the bracket for quadratic convergence.\n"
   "4. Guard every Newton step: if f'(x\u2099) \u2248 0 or the iterate leaves the bracket, fall back to "
   "bisection.\n"
   "Worked example: one Newton step for f(x)=x\u00b2\u22122 from x\u2080=1: x\u2081 = 1 \u2212 (1\u22122)/2 = "
   "1 + 0.5 = 1.5 — already within 0.09 of \u221a2."),
  note("Project brief",
   "Ship a root-finder for a sensor calibration curve f on [0,5] with f(0) < 0 < f(5), f smooth, f' "
   "cheap to evaluate, and a required accuracy of 10\u207b\u2079. Specify the method sequence (bracket \u2192 "
   "bisect \u2192 Newton), compute how many bisection steps reach 10\u207b\u00b3 before switching, bound the "
   "final error, and list the failure modes you guard against (zero derivative, leaving the "
   "bracket, multiple roots). Deliverable: the procedure, the step counts, and one paragraph on "
   "why \u2018Newton from x=0 immediately\u2019 was rejected."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Concepts section: the bisection error bound.",
  "Hands-on procedure section: one Newton step.",
  "Concepts section: Simpson's O(h\u2074) error.",
  "Concepts section: Newton's failure modes.",
 ],
})

# ---------------------------------------------------------------- Module 16
MODULES.append({
 "id": "m20-linear-systems-optimization",
 "summary": (
    "Welcome to Module 16: Linear Systems & Optimization — the final module. I'm your instructor, "
    "and we close the course where engineering lives: solving Ax=b at scale and minimizing "
    "objectives. Gaussian elimination, LU factorization, least squares, and gradient descent — the "
    "last one being the engine of neural-network training, built from the chain rule you learned in "
    "Module 8 and the gradients from Module 11. By the end you'll solve systems like a library does "
    "and tune a learning rate without superstition."
 ),
 "notes": [
  note("Concepts",
   "- **Gaussian elimination** \u2014 forward elimination reduces [A|b] to upper-triangular form using row "
   "operations (swap, scale, add multiples); back substitution solves from the bottom up. Cost: "
   "O(n\u00b3).\n"
   "- **partial pivoting** \u2014 swap in the largest available pivot: controls roundoff — never divide by "
   "a tiny pivot when a larger one is available.\n"
   "- **LU factorization** \u2014 elimination factors A = LU (lower \u00d7 upper, with row permutations). "
   "Factor once at O(n\u00b3), then solve each new right-hand side at O(n\u00b2) via Ly=b, Ux=y. This is what "
   "libraries actually do — `numpy.linalg.solve` uses LU-style factorization, not explicit inversion.\n"
   "- **least squares** \u2014 for overdetermined Ax \u2248 b, minimize ||Ax\u2212b||\u00b2. Geometrically: project b "
   "onto the column space of A.\n"
   "- **normal equations** \u2014 `A\u1d5bAx = A\u1d5bb`: setting the least-squares gradient to zero.\n"
   "- **QR preference** \u2014 in practice prefer QR factorization over the normal equations: the normal "
   "equations square the condition number (\u03ba(A\u1d5bA) = \u03ba(A)\u00b2), amplifying numerical error.\n"
   "- **gradient descent** \u2014 `x \u2190 x \u2212 \u03b1\u2207f(x)`: step downhill. For convex f with Lipschitz "
   "gradient, a small enough learning rate \u03b1 converges; too large diverges.\n"
   "- **learning rate** \u2014 the step-size \u03b1: too large \u21d2 oscillation or divergence (overshooting the "
   "minimum); too small \u21d2 slow but steady.\n"
   "- **stochastic gradient descent** \u2014 uses one sample's gradient per step: noisy but fast per "
   "iteration, the engine of neural-network training. The gradient itself comes from the chain rule "
   "(Module 8)."),
  note("Hands-on procedure",
   "Solve Ax=b by elimination with back substitution:\n"
   "1. Write the augmented matrix [A|b].\n"
   "2. Forward elimination: for each column, pivot (swap in the largest available entry), then "
   "eliminate below — reaching upper-triangular form.\n"
   "3. Back substitution: solve the last row, substitute upward.\n"
   "4. Verify: multiply A\u00b7x and confirm it equals b.\n"
   "Worked example: [[2,1],[1,3]] [x,y]\u1d5b = [5,6]\u1d5b. Eliminate: row2 \u2190 row2 \u2212 0.5\u00b7row1 \u21d2 "
   "[[2,1],[0,2.5]] | [5,3.5]. Back-substitute: y = 3.5/2.5 = 7/5; 2x = 5 \u2212 7/5 = 18/5 \u21d2 x = 9/5. "
   "Verify: 2(9/5)+7/5 = 25/5 = 5 \u2713; 9/5+3(7/5) = 30/5 = 6 \u2713."),
  note("Project brief",
   "Fit a least-squares line to a small dataset (six (x,y) points of your choosing, roughly linear "
   "with noise) twice: once via the normal equations A\u1d5bAx = A\u1d5bb, once via QR factorization. "
   "Compare the solutions and explain — via the condition-number squaring from the Concepts section "
   "\u2014 why they can differ on ill-conditioned data. Then run five gradient-descent steps by hand on "
   "f(x) = x\u00b2+4x+6 with \u03b1 = 0.1 from x=5 and report the trajectory toward the true minimum at "
   "x=\u22122. Deliverable: both fits, the comparison paragraph, and the descent trajectory."),
  note("Honesty note", HONESTY),
 ],
 "refs": [
  "Hands-on procedure section: elimination.",
  "Concepts section: learning-rate overshoot.",
  "Concepts section: LU factorization.",
  "Concepts section: least squares.",
 ],
})


def main():
    with open(PATH, encoding='utf-8') as f:
        course = json.load(f)

    by_id = {m["id"]: m for m in MODULES}
    assert set(by_id) == {m["id"] for m in course["modules"]}, "module id mismatch"

    changed = 0
    for m in course["modules"]:
        spec = by_id[m["id"]]
        m["summary"] = spec["summary"]
        m["notes"] = spec["notes"]
        assert [n["title"] for n in m["notes"]] == ["Concepts", "Hands-on procedure", "Project brief", "Honesty note"], m["id"]
        assert len(m["cards"]) >= 5, m["id"]
        for c in m["cards"]:
            assert set(c.keys()) == {"front", "back"} and c["front"] and c["back"], m["id"]
        assert len(spec["refs"]) == len(m["quiz"]), m["id"]
        for qi, q in enumerate(m["quiz"]):
            assert len(q["choices"]) == 4, (m["id"], qi)
            assert isinstance(q["answer"], int) and 0 <= q["answer"] <= 3, (m["id"], qi)
            assert q["explain"], (m["id"], qi)
            if "section" not in q["explain"].lower():
                q["explain"] = q["explain"].rstrip() + " (" + spec["refs"][qi] + ")"
        changed += 1

    # course-level sanity: all template keys present
    for key in ["arc", "priorities", "battlePlan", "mockTasks", "cheatSheets",
                "answerBank", "mockMinutes", "sourceLinks", "honestyNote"]:
        assert key in course and course[key], key
    assert isinstance(course["mockMinutes"], int)
    assert len(course["mockTasks"]) == 48, len(course["mockTasks"])

    tmp = PATH + ".retrofit-tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(course, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, PATH)

    with open(PATH, encoding="utf-8") as f:
        check = json.load(f)
    assert len(check["modules"]) == 16
    print(f"OK: retrofitted {changed} modules; file re-validated, {len(check['modules'])} modules.")

if __name__ == "__main__":
    main()
