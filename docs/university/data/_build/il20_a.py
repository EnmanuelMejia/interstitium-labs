"""IL-20 Mathematics for Engineers & Scientists — modules 1-8 (discrete + linear algebra)."""
MODULES_A = [
{
 "id": "m20-sets-logic", "code": "IL-20", "title": "Sets & Propositional Logic",
 "weight": 1,
 "summary": "Sets, set operations, propositions, connectives, truth tables, quantifiers, and the logical language every proof in this course is written in.",
 "objectives": ["Use set notation and the core operations: union, intersection, difference, complement", "Evaluate compound propositions with truth tables", "Translate statements into quantifier notation", "Distinguish necessary from sufficient conditions"],
 "notes": [
  {"title": "Sets and operations",
   "body": "A **set** is a collection of distinct objects. `x \u2208 A` means x is an element of A. Key operations:\n- **Union** `A \u222a B`: everything in A or B\n- **Intersection** `A \u2229 B`: everything in both\n- **Difference** `A \\ B`: everything in A but not B\n- **Complement** `A\u1d9c`: everything in the universe not in A\n- **Power set** `P(A)`: the set of all subsets; if `|A| = n`, then `|P(A)| = 2^n`."},
  {"title": "Propositions and connectives",
   "body": "A **proposition** is a statement that is either true or false, never both. Connectives:\n- **Negation** `\u00acp`: true exactly when p is false\n- **Conjunction** `p \u2227 q`: true only when both are true\n- **Disjunction** `p \u2228 q`: true when at least one is true (inclusive or)\n- **Implication** `p \u2192 q`: false only when p is true and q is false\n- **Biconditional** `p \u2194 q`: true when p and q agree.\nImplication `p \u2192 q` is **not** the same as causation \u2014 it is a truth-functional claim: 'it is not the case that p holds and q fails.'"},
  {"title": "Quantifiers",
   "body": "**Universal** `\u2200x P(x)`: P holds for every x. **Existential** `\u2203x P(x)`: P holds for at least one x.\nNegating a quantifier flips it: `\u00ac\u2200x P(x)` is equivalent to `\u2203x \u00acP(x)`; `\u2203x \u2200y P(x,y)` is generally **not** the same as `\u2200y \u2203x P(x,y)` \u2014 order matters. In the definition of a limit, the `\u2203\u03b4 \u2200x` ordering is the whole point."},
  {"title": "Necessary vs sufficient",
   "body": "`p \u2192 q` says p is **sufficient** for q and q is **necessary** for p. Conflating them is the most common logical error in engineering arguments: 'the tests pass' is not sufficient for 'the code is correct', and 'the code is correct' is not necessary for 'the tests pass.'"}
 ],
 "cards": [
  {"front": "What is the power set of a set with n elements, and how large is it?", "back": "P(A) is the set of all subsets of A. |P(A)| = 2^n."},
  {"front": "When is p \u2192 q false?", "back": "Only when p is true and q is false. All other rows are true."},
  {"front": "Negate: \u2200x \u2203y P(x,y)", "back": "\u2203x \u2200y \u00acP(x,y) \u2014 flip each quantifier and negate the predicate."},
  {"front": "If p \u2192 q, what is p relative to q? What is q relative to p?", "back": "p is sufficient for q; q is necessary for p."},
  {"front": "De Morgan's laws (sets and logic)?", "back": "(A \u222a B)\u1d9c = A\u1d9c \u2229 B\u1d9c; \u00ac(p \u2228 q) \u2261 \u00acp \u2227 \u00acq. Complement flips union/intersection; negation flips and/or."},
  {"front": "Contrapositive of p \u2192 q?", "back": "\u00acq \u2192 \u00acp \u2014 logically equivalent to the original implication."}
 ],
 "quiz": [
  {"q": "Which truth assignment makes (p \u2228 q) \u2192 (p \u2227 q) false?",
   "choices": ["p=T, q=T", "p=T, q=F", "p=F, q=T", "p=F, q=F"],
   "answer": 1,
   "explain": "p=T,q=F gives antecedent (T\u2228F)=T and consequent (T\u2227F)=F, so T\u2192F is false. (Same for p=F,q=T.)"},
  {"q": "A \u00acB \u2229 (A \u222a B) equals:",
   "choices": ["A", "B", "A \\ B", "\u2205"],
   "answer": 2,
   "explain": "Elements of A that are also in A\u222aB but not in B: exactly A \\ B."},
  {"q": "The statement '\u2203x \u2200y P(x,y)' says:",
   "choices": ["For each y there is some x with P(x,y)", "There is one x that works for every y", "P holds for all pairs", "P holds for no pair"],
   "answer": 1,
   "explain": "The existential comes first: a single x that works uniformly for all y \u2014 a much stronger claim than \u2200y\u2203x."},
  {"q": "'The build succeeds' is claimed to imply 'tests pass'. Tests fail. What follows?",
   "choices": ["The build must have succeeded", "The build did not succeed", "Nothing can be concluded", "The claim is disproven"],
   "answer": 1,
   "explain": "Modus tollens: (build \u2192 tests) \u2227 \u00actests \u22a2 \u00acbuild."}
 ]
},
{
 "id": "m20-proof-methods", "code": "IL-20", "title": "Proof Methods",
 "weight": 1,
 "summary": "Direct proof, contrapositive, contradiction, and mathematical induction \u2014 the four moves that prove theorems, verify algorithms, and certify loop invariants.",
 "objectives": ["Prove a statement directly from definitions", "Use contrapositive and contradiction correctly", "Carry out an induction proof including the base case and inductive step", "Recognize where induction applies to algorithms and recurrences"],
 "notes": [
  {"title": "Direct proof",
   "body": "Assume the hypotheses, unpack **definitions**, and derive the conclusion by valid steps. Example: to prove the sum of two even integers is even, write them as `2k` and `2m`; their sum is `2(k+m)`, which is even by definition. Direct proof fails when the definitions give you nothing to grab \u2014 then reach for contrapositive or contradiction."},
  {"title": "Contrapositive and contradiction",
   "body": "**Contrapositive**: prove `\u00acq \u2192 \u00acp` instead of `p \u2192 q`. Useful when the negated conclusion is easier to work with (e.g., proving '\u221a2 is irrational' style results via parity).\n**Contradiction**: assume p and `\u00acq`, derive a statement that contradicts a known fact or itself. Then `\u00acq` is impossible, so q holds."},
  {"title": "Mathematical induction",
   "body": "To prove P(n) for all natural n \u2265 n\u2080:\n1. **Base case**: prove P(n\u2080).\n2. **Inductive step**: assume P(k) (the inductive hypothesis) and prove P(k+1).\nThen P(n) holds for all n \u2265 n\u2080. Classic: `1 + 2 + ... + n = n(n+1)/2`. Base n=1: 1 = 1\u00b72/2. Step: adding (k+1) to k(k+1)/2 gives (k+1)(k+2)/2. Strong induction lets the hypothesis assume P(j) for all j \u2264 k."},
  {"title": "Induction in engineering",
   "body": "Induction is the proof method for **loop invariants** and **recurrences**: prove the invariant holds before the loop (base), and that each iteration preserves it (step). Recurrence relations like `T(n) = 2T(n/2) + n` (mergesort) are solved and verified by the same pattern."}
 ],
 "cards": [
  {"front": "The two parts of an induction proof?", "back": "Base case P(n\u2080), and the inductive step: P(k) \u21d2 P(k+1)."},
  {"front": "Prove p \u2192 q by contradiction: what do you assume?", "back": "Assume p and \u00acq together, then derive a contradiction."},
  {"front": "Sum 1+2+...+n closed form?", "back": "n(n+1)/2 \u2014 proved by induction."},
  {"front": "What is a loop invariant, and how is it proved?", "back": "A property true before and after each loop iteration \u2014 proved by induction on the iteration count."},
  {"front": "Strong vs weak induction?", "back": "Weak assumes P(k) to prove P(k+1); strong assumes all of P(n\u2080)...P(k). Strong is needed when P(k+1) depends on earlier cases, e.g. Fibonacci."}
 ],
 "quiz": [
  {"q": "In an induction proof of P(n), the inductive hypothesis is:",
   "choices": ["P(n\u2080)", "The assumption P(k) for a fixed k", "The conclusion P(k+1)", "The statement for all n"],
   "answer": 1,
   "explain": "We assume P(k) for an arbitrary fixed k and derive P(k+1)."},
  {"q": "Which proof strategy fits 'If n\u00b2 is even then n is even'?",
   "choices": ["Direct from the definition of even", "Contrapositive: if n is odd then n\u00b2 is odd", "Induction on n", "Proof by cases on divisibility by 4"],
   "answer": 1,
   "explain": "Direct proof stalls (no handle on n); the contrapositive is easy: odd n = 2k+1 gives n\u00b2 = 4k\u00b2+4k+1, odd."},
  {"q": "A proof that assumes the conclusion is guilty of:",
   "choices": ["Contrapositive", "Begging the question (circular reasoning)", "Induction", "Case analysis"],
   "answer": 1,
   "explain": "Using the conclusion as a premise is circular \u2014 the most common flaw in novice proofs."},
  {"q": "1 + 3 + 5 + ... + (2n\u22121) equals:",
   "choices": ["n\u00b2", "n(n+1)", "2n\u22121", "n\u00b3"],
   "answer": 0,
   "explain": "Sum of the first n odd numbers is n\u00b2 \u2014 provable by induction."}
 ]
},
{
 "id": "m20-counting", "code": "IL-20", "title": "Counting & Combinatorics",
 "weight": 1,
 "summary": "Product and sum rules, permutations, combinations, the binomial theorem, and the pigeonhole principle \u2014 the mathematics of 'how many'.",
 "objectives": ["Apply the product and sum rules to counting problems", "Distinguish permutations from combinations", "Use the binomial theorem and Pascal's identity", "Apply the pigeonhole principle"],
 "notes": [
  {"title": "Product and sum rules",
   "body": "**Product rule**: if a task has k stages with n\u1d62, n\u2082, \u2026, n\u2096 options, total outcomes = n\u1d62\u00b7n\u2082\u00b7\u2026\u00b7n\u2096. **Sum rule**: if two tasks are disjoint, total = sum of their counts. An n-bit string has `2^n` possibilities (product rule); counting them is the same as counting subsets of an n-element set."},
  {"title": "Permutations vs combinations",
   "body": "**Permutation** P(n,k) = n!/(n\u2212k)! \u2014 ordered selection of k from n. **Combination** C(n,k) = n!/(k!(n\u2212k)!) \u2014 unordered selection. Rule of thumb: ask 'does rearranging change the outcome?' If yes, permutation; if no, combination. Choosing a 3-person committee from 10: C(10,3) = 120. Assigning them president/VP/treasurer: P(10,3) = 720."},
  {"title": "Binomial theorem",
   "body": "`(x+y)^n = \u03a3 C(n,k) x^(n\u2212k) y^k` for k=0..n. Pascal's identity `C(n,k) = C(n\u22121,k\u22121) + C(n\u22121,k)` builds the triangle. Setting x=y=1 gives `\u03a3 C(n,k) = 2^n` \u2014 the number of subsets of an n-element set, matching the product rule."},
  {"title": "Pigeonhole principle",
   "body": "If n+1 items go into n boxes, some box holds at least 2 items. Generalization: with N items and k boxes, some box holds at least \u2308N/k\u2309 items. Used constantly in hashing (collisions are unavoidable when keys exceed slots), scheduling, and lower-bound arguments."}
 ],
 "cards": [
  {"front": "P(n,k) formula?", "back": "n!/(n\u2212k)! \u2014 ordered selection."},
  {"front": "C(n,k) formula?", "back": "n!/(k!(n\u2212k)!) \u2014 unordered selection."},
  {"front": "Binomial theorem statement?", "back": "(x+y)^n = \u03a3_{k=0}^n C(n,k) x^(n\u2212k) y^k."},
  {"front": "Pigeonhole principle?", "back": "n+1 items into n boxes \u21d2 some box has \u22652 items."},
  {"front": "How many 8-bit strings?", "back": "2^8 = 256 (product rule)."},
  {"front": "C(n,0) + C(n,1) + ... + C(n,n) = ?", "back": "2^n \u2014 set x=y=1 in the binomial theorem."}
 ],
 "quiz": [
  {"q": "Number of ways to choose an unordered 4-person team from 9 people?",
   "choices": ["3024", "126", "6561", "36"],
   "answer": 1,
   "explain": "C(9,4) = 9!/(4!5!) = 126. Order within the team doesn't matter."},
  {"q": "With 367 people in a room, by the pigeonhole principle:",
   "choices": ["Two share a birth month", "Two share a birthday (ignoring leap years)", "Two were born in the same year", "Two have the same name"],
   "answer": 1,
   "explain": "367 people, 366 possible birthdays (incl. Feb 29): some date is shared."},
  {"q": "The coefficient of x\u00b3 in (x+2)^5 is:",
   "choices": ["10", "20", "40", "80"],
   "answer": 2,
   "explain": "C(5,3)\u00b7x\u00b3\u00b72\u00b2 = 10\u00b74\u00b7x\u00b3 = 40x\u00b3."},
  {"q": "Passwords of length 6 over 26 lowercase letters: how many?",
   "choices": ["26\u00d76", "6^26", "26^6", "P(26,6)"],
   "answer": 2,
   "explain": "Each of 6 positions has 26 independent choices: 26^6 (product rule with repetition)."}
 ]
},
{
 "id": "m20-relations-functions", "code": "IL-20", "title": "Relations & Functions",
 "weight": 1,
 "summary": "Injective, surjective, and bijective functions; composition and inverses; equivalence relations and partitions \u2014 the language of mappings between structures.",
 "objectives": ["Classify functions as injective, surjective, or bijective", "Compose functions and find inverses", "Verify an equivalence relation and describe its classes", "Connect bijections to counting (cardinality)"],
 "notes": [
  {"title": "Function properties",
   "body": "f: A \u2192 B is **injective** (one-to-one) if f(x\u2081)=f(x\u2082) implies x\u2081=x\u2082 \u2014 distinct inputs map to distinct outputs. **Surjective** (onto) if every y in B has some x with f(x)=y \u2014 the image covers B. **Bijective** if both: a perfect pairing, which is exactly when an **inverse** f\u207b\u00b9: B \u2192 A exists."},
  {"title": "Composition",
   "body": "(g\u2218f)(x) = g(f(x)): apply f first, then g. Composition is **associative** but generally **not commutative** \u2014 order matters. If f and g are both bijective, g\u2218f is bijective with inverse f\u207b\u00b9\u2218g\u207b\u00b9 (note the reversed order)."},
  {"title": "Equivalence relations",
   "body": "A relation ~ on A is an **equivalence relation** if it is: **reflexive** (x~x), **symmetric** (x~y \u21d2 y~x), **transitive** (x~y, y~z \u21d2 x~z). Every equivalence relation **partitions** A into disjoint equivalence classes. Example: congruence mod n partitions the integers into n residue classes \u2014 the foundation of modular arithmetic used in cryptography."},
  {"title": "Partial orders (glimpse)",
   "body": "Replace symmetric with **antisymmetric** (x\u2264y, y\u2264x \u21d2 x=y) and you get a **partial order** \u2014 reflexive, antisymmetric, transitive. Task-dependency graphs, version ordering, and type hierarchies are partial orders; topological sort linearizes them."}
 ],
 "cards": [
  {"front": "Define injective, surjective, bijective.", "back": "Injective: distinct inputs \u2192 distinct outputs. Surjective: image covers the codomain. Bijective: both \u2014 invertible."},
  {"front": "Inverse of g\u2218f (both bijective)?", "back": "f\u207b\u00b9\u2218g\u207b\u00b9 \u2014 order reverses."},
  {"front": "Three properties of an equivalence relation?", "back": "Reflexive, symmetric, transitive."},
  {"front": "Equivalence classes of congruence mod 5?", "back": "Five classes: [0],[1],[2],[3],[4] \u2014 the residue classes."},
  {"front": "What does a bijection between finite sets tell you?", "back": "They have the same cardinality \u2014 counting via pairing."}
 ],
 "quiz": [
  {"q": "f: \u211d \u2192 \u211d, f(x) = x\u00b3 \u2212 x. This function is:",
   "choices": ["Injective only", "Surjective only", "Bijective", "Neither"],
   "answer": 1,
   "explain": "f(0)=f(1)=f(\u22121)=0, so not injective; as a continuous cubic with limits \u00b1\u221e it attains every real value, so surjective."},
  {"q": "Which relation on \u2124 is an equivalence relation?",
   "choices": ["xRy iff x < y", "xRy iff x\u2212y is even", "xRy iff x divides y", "xRy iff x+y > 0"],
   "answer": 1,
   "explain": "Same parity: reflexive, symmetric, transitive. < is not symmetric; divisibility is not symmetric; x+y>0 fails reflexivity (0+0>0 false)."},
  {"q": "(g\u2218f)(x) means:",
   "choices": ["g(x) then f", "f(x) then g", "g(x)\u00b7f(x)", "g(x)+f(x)"],
   "answer": 1,
   "explain": "Rightmost applies first: (g\u2218f)(x) = g(f(x))."},
  {"q": "If f: A \u2192 B is bijective and |A| = 7, then |B| =",
   "choices": ["At least 7", "At most 7", "Exactly 7", "Cannot determine"],
   "answer": 2,
   "explain": "A bijection pairs elements one-to-one, so the sets have equal cardinality."}
 ]
},
{
 "id": "m20-linear-algebra-1", "code": "IL-20", "title": "Linear Algebra I \u2014 Vectors & Spaces",
 "weight": 1,
 "summary": "Vectors, dot products, vector spaces, span, and linear independence \u2014 the geometric core behind graphics, ML features, and simulation.",
 "objectives": ["Add, scale, and take dot products of vectors", "Test a set for linear independence", "Describe span and identify a basis", "Compute projections and angles via the dot product"],
 "notes": [
  {"title": "Vectors and the dot product",
   "body": "A vector **v** in \u211d\u207f is an ordered n-tuple. Addition and scalar multiplication are componentwise. The **dot product** `u\u00b7v = \u03a3 u\u1d62v\u1d62` measures alignment: `u\u00b7v = |u||v|cos \u03b8`. The **norm** `|v| = \u221a(v\u00b7v)`. Two nonzero vectors are **orthogonal** iff their dot product is 0."},
  {"title": "Vector spaces",
   "body": "A **vector space** is a set closed under addition and scalar multiplication, satisfying the vector axioms (associativity, zero vector, additive inverses, distributivity). Examples: \u211d\u207f, matrices of fixed size, polynomials of degree \u2264 n, functions \u211d \u2192 \u211d. Closure is the key test: is the sum of two members always a member?"},
  {"title": "Span and linear independence",
   "body": "The **span** of a set is all its linear combinations. Vectors v\u2081..v\u2096 are **linearly independent** if `c\u2081v\u2081+\u2026+c\u2096v\u2096 = 0` forces all c\u1d62 = 0 \u2014 no vector is a combination of the others. A **basis** is an independent spanning set; every vector has a **unique** coordinate representation in a basis. dim(\u211d\u207f) = n."},
  {"title": "Projection",
   "body": "The projection of u onto v is `proj_v(u) = ((u\u00b7v)/(v\u00b7v)) v`. This single formula powers least-squares fitting, Gram\u2013Schmidt orthogonalization, and attention-free similarity search: the dot product with a unit vector is the signed length of the projection."}
 ],
 "cards": [
  {"front": "u\u00b7v in terms of norms and angle?", "back": "u\u00b7v = |u||v|cos \u03b8."},
  {"front": "When is a set of vectors linearly independent?", "back": "When c\u2081v\u2081+\u2026+c\u2096v\u2096=0 implies every c\u1d62=0."},
  {"front": "What is a basis? What is dimension?", "back": "An independent spanning set; the number of vectors in any basis."},
  {"front": "Projection of u onto v?", "back": "((u\u00b7v)/(v\u00b7v)) v."},
  {"front": "Maximum size of an independent set in \u211d\u207f?", "back": "n \u2014 any n+1 vectors in \u211d\u207f are dependent."},
  {"front": "What is the norm |v| in terms of the dot product?", "back": "|v| = \u221a(v\u00b7v)."}
 ],
 "quiz": [
  {"q": "Are (1,2), (3,4) linearly independent in \u211d\u00b2?",
   "choices": ["Yes", "No", "Only over \u2102", "Need more info"],
   "answer": 0,
   "explain": "c\u2081(1,2)+c\u2082(3,4)=(0,0) gives c\u2081+3c\u2082=0, 2c\u2081+4c\u2082=0 \u21d2 only c\u2081=c\u2082=0."},
  {"q": "Angle between (1,0) and (1,1)?",
   "choices": ["30\u00b0", "45\u00b0", "60\u00b0", "90\u00b0"],
   "answer": 1,
   "explain": "cos \u03b8 = 1/(1\u00b7\u221a2) = 1/\u221a2 \u21d2 \u03b8 = 45\u00b0."},
  {"q": "Which set is a basis of \u211d\u00b3?",
   "choices": ["{(1,0,0),(0,1,0)}", "{(1,1,0),(2,2,0),(0,0,1)}", "{(1,0,0),(0,1,0),(0,0,1)}", "{(1,2,3)}"],
   "answer": 2,
   "explain": "Three vectors in \u211d\u00b3 that are independent and span \u2014 the standard basis. The others are too few or dependent."},
  {"q": "proj of (3,4) onto (1,0)?",
   "choices": ["(3,0)", "(0,4)", "(3,4)", "(1,0)"],
   "answer": 0,
   "explain": "((3,4)\u00b7(1,0))/((1,0)\u00b7(1,0)) \u00b7 (1,0) = 3(1,0) = (3,0)."}
 ]
},
{
 "id": "m20-linear-algebra-2", "code": "IL-20", "title": "Linear Algebra II \u2014 Matrices",
 "weight": 1,
 "summary": "Matrix multiplication, transposes, determinants, inverses, and rank \u2014 the computational engine of applied mathematics.",
 "objectives": ["Multiply matrices with correct dimensions", "Compute 2\u00d72 and 3\u00d73 determinants", "Invert a matrix and test invertibility", "Find rank and interpret it"],
 "notes": [
  {"title": "Matrix multiplication",
   "body": "If A is m\u00d7n and B is n\u00d7p, then AB is m\u00d7p with `(AB)\u1d62\u2c7c = \u03a3\u2096 A\u1d62\u2096B\u2096\u2c7c` \u2014 row i of A dotted with column j of B. The inner dimensions must match. Multiplication is **associative** and distributes over addition, but is **not commutative**: AB \u2260 BA in general. `(AB)\u1d5b = B\u1d5bA\u1d5b` \u2014 order reverses, like function composition."},
  {"title": "Determinants",
   "body": "The determinant measures signed volume scaling. 2\u00d72: `det [[a,b],[c,d]] = ad \u2212 bc`. 3\u00d73: cofactor expansion along any row/column. det(A) \u2260 0 iff A is invertible; det(AB) = det(A)det(B). A zero determinant means the transformation collapses at least one dimension."},
  {"title": "Inverses",
   "body": "A\u207b\u00b9 satisfies AA\u207b\u00b9 = A\u207b\u00b9A = I. 2\u00d72: `[[a,b],[c,d]]\u207b\u00b9 = (1/(ad\u2212bc)) [[d,\u2212b],[\u2212c,a]]`. For larger matrices use Gauss\u2013Jordan elimination on [A|I]. `(AB)\u207b\u00b9 = B\u207b\u00b9A\u207b\u00b9`. Never compute an explicit inverse to solve Ax=b in practice \u2014 factor instead (LU/QR); inversion is slower and less stable."},
  {"title": "Rank",
   "body": "**Rank** = number of linearly independent rows = number of independent columns = dimension of the column space. For Ax=b: rank(A) = rank([A|b]) means a solution exists; rank(A) = n (full column rank) means it is unique. Rank deficiency signals redundancy \u2014 or multicollinearity in data."}
 ],
 "cards": [
  {"front": "When can you multiply A (m\u00d7n) by B?", "back": "B must be n\u00d7p; the result is m\u00d7p."},
  {"front": "2\u00d72 determinant and inverse?", "back": "det = ad\u2212bc; inverse = 1/det \u00b7 [[d,\u2212b],[\u2212c,a]]."},
  {"front": "(AB)\u1d5b and (AB)\u207b\u00b9?", "back": "(AB)\u1d5b = B\u1d5bA\u1d5b; (AB)\u207b\u00b9 = B\u207b\u00b9A\u207b\u00b9."},
  {"front": "What does det(A) = 0 mean?", "back": "A is not invertible; it collapses dimension (zero volume scaling)."},
  {"front": "Rank of a matrix?", "back": "Number of independent rows/columns = dim of column space."},
  {"front": "Why not solve Ax=b via x = A\u207b\u00b9b numerically?", "back": "Explicit inversion is slower and numerically less stable than factorization (LU/QR)."}
 ],
 "quiz": [
  {"q": "[[2,1],[4,3]] \u00b7 [[1,0],[0,1]] =",
   "choices": ["[[2,1],[4,3]]", "[[1,0],[0,1]]", "[[3,1],[4,4]]", "[[2,4],[1,3]]"],
   "answer": 0,
   "explain": "Multiplying by the identity leaves A unchanged."},
  {"q": "det of [[3,1],[2,4]]?",
   "choices": ["10", "14", "12\u22122=10", "5"],
   "answer": 0,
   "explain": "3\u00b74 \u2212 1\u00b72 = 12 \u2212 2 = 10."},
  {"q": "A is 3\u00d72, B is 2\u00d74. Shape of AB?",
   "choices": ["2\u00d72", "3\u00d74", "4\u00d73", "Undefined"],
   "answer": 1,
   "explain": "Inner dims agree (2); outer dims give 3\u00d74."},
  {"q": "If rank(A) = 2 for a 4\u00d73 matrix A, then Ax = 0 has:",
   "choices": ["Only the trivial solution", "Infinitely many solutions", "No solution", "Exactly 2 solutions"],
   "answer": 1,
   "explain": "3 columns but rank 2 \u21d2 columns dependent \u21d2 nontrivial null space \u21d2 infinitely many solutions."}
 ]
},
{
 "id": "m20-linear-algebra-3", "code": "IL-20", "title": "Linear Algebra III \u2014 Eigenvalues",
 "weight": 1,
 "summary": "Eigenvalues, eigenvectors, diagonalization, and symmetric matrices \u2014 the structure behind PCA, stability analysis, and PageRank.",
 "objectives": ["Solve det(A \u2212 \u03bbI) = 0 for eigenvalues", "Find eigenvectors for a given eigenvalue", "Test whether a matrix is diagonalizable", "State the spectral theorem for symmetric matrices"],
 "notes": [
  {"title": "Eigenvalues and eigenvectors",
   "body": "A nonzero vector v is an **eigenvector** of A with **eigenvalue** \u03bb if `Av = \u03bbv` \u2014 A stretches v without rotating it. Eigenvalues solve the **characteristic equation** `det(A \u2212 \u03bbI) = 0`. For 2\u00d72 this is a quadratic; its roots are the eigenvalues (possibly complex)."},
  {"title": "Diagonalization",
   "body": "A is **diagonalizable** if A = PDP\u207b\u00b9 with D diagonal: then A\u1d4f = PD\u1d4fP\u207b\u00b9, and powers become trivial. A sufficient condition: n distinct eigenvalues for an n\u00d7n matrix. Diagonalization is why eigenvalues govern long-term behavior \u2014 Markov chains, linear recurrences, and dynamical systems all reduce to '\u03bb\u1d4f grows or decays?'"},
  {"title": "Symmetric matrices",
   "body": "The **spectral theorem**: every real symmetric matrix has real eigenvalues and an orthonormal eigenbasis. Covariance matrices are symmetric, so PCA's principal components are real, orthogonal directions \u2014 no complex arithmetic, no defective cases."},
  {"title": "Trace and determinant via eigenvalues",
   "body": "**Trace**(A) = sum of diagonal entries = sum of eigenvalues. **det**(A) = product of eigenvalues. Quick sanity checks: for [[4,1],[2,3]], trace 7 and det 10, so eigenvalues sum to 7 and multiply to 10 \u2014 they are 5 and 2."}
 ],
 "cards": [
  {"front": "Characteristic equation?", "back": "det(A \u2212 \u03bbI) = 0; its roots are the eigenvalues."},
  {"front": "When is A diagonalizable (sufficient condition)?", "back": "A = PDP\u207b\u00b9 exists when A has n distinct eigenvalues (n\u00d7n)."},
  {"front": "Spectral theorem?", "back": "Real symmetric matrices have real eigenvalues and an orthonormal eigenbasis."},
  {"front": "Trace and determinant from eigenvalues?", "back": "trace = sum of eigenvalues; det = product of eigenvalues."},
  {"front": "Why do eigenvalues govern A\u1d4f?", "back": "If A = PDP\u207b\u00b9, then A\u1d4f = PD\u1d4fP\u207b\u00b9 \u2014 powers act diagonally on eigen-components."}
 ],
 "quiz": [
  {"q": "Eigenvalues of [[2,0],[0,5]]?",
   "choices": ["2 and 5", "0 and 7", "2 and 3", "10 and 1"],
   "answer": 0,
   "explain": "Diagonal matrix: eigenvalues are the diagonal entries."},
  {"q": "Eigenvalues of [[4,1],[2,3]]?",
   "choices": ["4 and 3", "5 and 2", "6 and 1", "7 and 0"],
   "answer": 1,
   "explain": "det(A\u2212\u03bbI) = (4\u2212\u03bb)(3\u2212\u03bb)\u22122 = \u03bb\u00b2\u22127\u03bb+10 = (\u03bb\u22125)(\u03bb\u22122)."},
  {"q": "An eigenvector v of A with eigenvalue 3 satisfies:",
   "choices": ["Av = 3", "Av = 3v", "A\u00b7v = 9", "det(A) = 3"],
   "answer": 1,
   "explain": "Definition: Av = \u03bbv with v \u2260 0."},
  {"q": "A real symmetric 3\u00d73 matrix must have:",
   "choices": ["Three distinct eigenvalues", "Real eigenvalues and orthogonal eigenvectors", "Determinant 1", "A zero eigenvalue"],
   "answer": 1,
   "explain": "Spectral theorem: real eigenvalues, orthonormal eigenbasis. Distinctness and det=1 are not guaranteed."}
 ]
},
{
 "id": "m20-calculus-1", "code": "IL-20", "title": "Calculus I \u2014 Limits & Derivatives",
 "weight": 1,
 "summary": "Limits, continuity, the derivative as a rate of change, and the differentiation rules \u2014 the mathematics of change.",
 "objectives": ["Evaluate limits including indeterminate forms", "Differentiate using product, quotient, and chain rules", "Interpret the derivative as rate of change and slope", "Find critical points and classify extrema"],
 "notes": [
  {"title": "Limits and continuity",
   "body": "`lim(x\u2192a) f(x) = L` means f(x) can be made arbitrarily close to L by taking x close to a. f is **continuous** at a if the limit equals f(a). Indeterminate forms 0/0 or \u221e/\u221e: try factoring, rationalizing, or **l'H\u00f4pital's rule** \u2014 differentiate numerator and denominator separately (check the form first!)."},
  {"title": "The derivative",
   "body": "`f'(x) = lim(h\u21920) [f(x+h) \u2212 f(x)]/h` \u2014 instantaneous rate of change, slope of the tangent line. Rules: **power** `(x\u207f)' = nx\u207f\u207b\u00b9`; **product** `(uv)' = u'v + uv'`; **quotient** `(u/v)' = (u'v \u2212 uv')/v\u00b2`; **chain** `[f(g(x))]' = f'(g(x))\u00b7g'(x)`. The chain rule is the workhorse \u2014 it is also what backpropagation computes."},
  {"title": "Key derivatives",
   "body": "Memorize: `(e\u02e3)' = e\u02e3`; `(ln x)' = 1/x`; `(sin x)' = cos x`; `(cos x)' = \u2212sin x`; `(a\u02e3)' = a\u02e3 ln a`; `(arctan x)' = 1/(1+x\u00b2)`. Every ML loss gradient is built from these plus the chain rule."},
  {"title": "Optimization",
   "body": "**Critical points**: f'(x) = 0 or undefined. **First derivative test**: sign change of f' classifies max/min. **Second derivative test**: f''(c) > 0 \u21d2 local min; f''(c) < 0 \u21d2 local max at a critical point c. On a closed interval, also check the endpoints \u2014 global extrema live at critical points or boundaries."}
 ],
 "cards": [
  {"front": "Definition of f'(x)?", "back": "lim(h\u21920) [f(x+h)\u2212f(x)]/h."},
  {"front": "Product, quotient, chain rules?", "back": "(uv)'=u'v+uv'; (u/v)'=(u'v\u2212uv')/v\u00b2; [f(g)]'=f'(g)\u00b7g'."},
  {"front": "Derivatives of e\u02e3, ln x, sin x, cos x?", "back": "e\u02e3; 1/x; cos x; \u2212sin x."},
  {"front": "l'H\u00f4pital's rule?", "back": "For 0/0 or \u221e/\u221e: lim f/g = lim f'/g' (if the latter exists)."},
  {"front": "Second derivative test?", "back": "f'(c)=0, f''(c)>0 \u21d2 local min; f''(c)<0 \u21d2 local max."},
  {"front": "Where can a global max on [a,b] occur?", "back": "At a critical point inside, or at an endpoint a or b."}
 ],
 "quiz": [
  {"q": "d/dx [x\u00b3 \u00b7 sin x] =",
   "choices": ["3x\u00b2 cos x", "3x\u00b2 sin x + x\u00b3 cos x", "3x\u00b2 sin x", "x\u00b3 cos x \u2212 3x\u00b2 sin x"],
   "answer": 1,
   "explain": "Product rule: (x\u00b3)' sin x + x\u00b3 (sin x)' = 3x\u00b2 sin x + x\u00b3 cos x."},
  {"q": "d/dx [e^(2x)] =",
   "choices": ["e^(2x)", "2e^(2x)", "2xe^(2x)", "e^(x\u00b2)"],
   "answer": 1,
   "explain": "Chain rule: derivative of 2x is 2, so 2e^(2x)."},
  {"q": "lim(x\u21920) sin(x)/x =",
   "choices": ["0", "1", "\u221e", "Does not exist"],
   "answer": 1,
   "explain": "The fundamental trigonometric limit equals 1 (l'H\u00f4pital also gives cos(0)/1 = 1)."},
  {"q": "Critical points of f(x) = x\u00b3 \u2212 3x?",
   "choices": ["x = 0 only", "x = \u00b11", "x = \u00b1\u221a3", "None"],
   "answer": 1,
   "explain": "f'(x) = 3x\u00b2 \u2212 3 = 0 \u21d2 x\u00b2 = 1 \u21d2 x = \u00b11."}
 ]
}
]
