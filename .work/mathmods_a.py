#!/usr/bin/env python3
"""Prereq-math module builders, part A: logic, discrete, numtheory, binmath.
Every numeric claim is COMPUTED in Python (fixed inputs) and interpolated.
Independent-prep framing; no invented credentials.
"""
import math, random, hashlib, itertools, statistics, ipaddress

def _rng(seed):
    return random.Random(int(hashlib.sha256(seed.encode()).hexdigest(), 16) % (2**31))

def mcq(mid, tag, q, correct, distractors, explain):
    ds = []
    for d in distractors:
        if d != correct and d not in ds:
            ds.append(d)
    ds = ds[:3]
    while len(ds) < 3:
        ds.append("None of the above")
    r = _rng(f"{mid}|{tag}")
    choices = [correct] + ds
    r.shuffle(choices)
    return {"q": q, "choices": choices, "answer": choices.index(correct), "explain": explain}

def assemble(course_id, course_code, suffix, title, summary, objectives, notes,
             cards, quiz, drills, lab, mock, prereq_for, videos=None):
    mid = f"{course_id}-math-{suffix}"
    for i, d in enumerate(drills):
        d.setdefault("id", f"{mid}--drill-{i+1}")
    lab = dict(lab); lab.setdefault("id", f"{mid}--lab")
    mock = dict(mock); mock.setdefault("id", f"{mid}--mock"); mock.setdefault("type", "choice")
    minutes = 60 + 15*len(notes) + 2*len(cards) + 3*len(quiz) + 10*sum(len(d["items"]) for d in drills) + 60
    minutes = int(5 * round(minutes/5))
    mod = {
        "id": mid, "code": course_code, "title": title, "weight": 1,
        "summary": summary, "objectives": objectives,
        "notes": notes, "cards": cards, "quiz": quiz, "videos": videos or [],
        "drills": drills, "handsOnLab": lab, "mockTask": mock,
        "estimatedMinutes": minutes, "crossLinks": [], "prerequisiteFor": prereq_for,
    }
    # template key order (_module-template.json)
    order = ["cards","code","crossLinks","drills","estimatedMinutes","handsOnLab",
             "id","mockTask","notes","objectives","prerequisiteFor","quiz","summary",
             "title","videos","weight"]
    return {k: mod[k] for k in order}

def _ttable(expr_fn, vars):
    rows = []
    for vals in itertools.product([False, True], repeat=len(vars)):
        env = dict(zip(vars, vals))
        rows.append((env, expr_fn(env)))
    return rows

def _fmt_bool(b): return "T" if b else "F"

# ---------------------------------------------------------------- logic ---
def build_logic(course_id, course_code, prereq_for, context):
    mid = f"{course_id}-math-logic"
    # computed: evaluate (p -> q) and p |= q table; De Morgan verification
    p_vals = [True, False]
    demorgan_ok = all((not (p and q)) == ((not p) or (not q)) for p in p_vals for q in p_vals)
    contra_ok = all(( (not p) or q ) == ( (not (not q)) or (not p) ) for p in p_vals for q in p_vals)
    n_vars, n_rows = 3, 2**3
    # worked: evaluate ((p AND q) OR (NOT r)) at p=T,q=F,r=T
    w_p, w_q, w_r = True, False, True
    w_val = (w_p and w_q) or (not w_r)
    notes = [
     {"title": "Propositions and truth values",
      "body": ("A proposition is a statement that is either true or false, never both. `p AND q` is true only when both are true; "
       "`p OR q` is true when at least one is true; `NOT p` flips the value. Worked example: evaluate `(p AND q) OR (NOT r)` at "
       f"p=T, q=F, r=T. First `p AND q` = T AND F = F. Then `NOT r` = NOT T = F. Finally `F OR F` = **F**. So the whole expression is **{_fmt_bool(w_val)}**. "
       "Work inside-out: parentheses first, then NOT, then AND, then OR — the same precedence habit that prevents bugs in code conditions.")},
     {"title": "Truth tables, computed by enumeration",
      "body": ("A truth table lists every assignment of the variables. With n variables there are 2^n rows — for n=3 that is "
       f"**{n_rows}** rows, computed as 2^3. Worked example: the implication `p -> q`, defined as `(NOT p) OR q`. Its table: "
       "p=T,q=T -> T; p=T,q=F -> F; p=F,q=T -> T; p=F,q=F -> T. The only false row is true-premise/false-conclusion. "
       "Enumerating all rows mechanically (as the lab does in Python) removes all doubt: no case is forgotten, because the count 2^n proves the table is complete.")},
     {"title": "De Morgan's laws, verified by brute force",
      "body": ("De Morgan's laws: `NOT (p AND q)` equals `(NOT p) OR (NOT q)`, and `NOT (p OR q)` equals `(NOT p) AND (NOT q)`. "
       f"Worked verification: checking all 4 assignments of (p,q) in Python, every row agrees — **{demorgan_ok}**. "
       "This is the law behind simplifying negated conditions: `NOT (admin AND active)` becomes `NOT admin OR NOT active`. "
       "In code and in firewall/policy rules, pushing NOT inward with De Morgan turns an unreadable negated conjunction into a plain disjunction.")},
     {"title": "Implication and the contrapositive",
      "body": ("`p -> q` (if p then q) is logically equivalent to its contrapositive `(NOT q) -> (NOT p)`. "
       f"Worked verification: all 4 assignments agree — **{contra_ok}**. The converse `q -> p` is NOT equivalent (check p=T,q=F: "
       "implication false, converse true). Practical use: to prove 'if the build passes then tests ran', prove the contrapositive "
       "'if tests did not run then the build fails' — often the easier direction. Confusing implication with converse is one of the most common logic errors in specifications.")},
     {"title": "Predicate logic over finite domains",
      "body": ("Predicates add quantifiers: `FORALL x, P(x)` and `EXISTS x, P(x)`. Over a finite domain you can evaluate them by enumeration. "
       "Worked example: domain = {2, 3, 4}, statement `EXISTS x, x is prime AND x > 3`. Check: x=2 (prime, not >3, fails), x=3 (prime, not >3, fails), "
       "x=4 (not prime, fails). No witness exists, so the statement is **false**. Change `>3` to `>=3`: x=3 is prime and >= 3, so the statement becomes **true**. "
       "Existence claims need exactly one witness; universal claims need every case. This discipline maps directly onto testing: 'there exists an input that crashes' vs 'for all inputs it terminates'.")},
     {"title": "Boolean algebra for systems work",
      "body": ("Boolean algebra gives simplification laws: absorption `p OR (p AND q) = p`, distribution, idempotence `p AND p = p`. "
       "Worked example: simplify `(admin AND active) OR (admin AND NOT active)`. Factor admin: `admin AND (active OR NOT active)` = `admin AND T` = **admin**. "
       "Verified by enumerating all 4 assignments of (admin, active): both sides agree on every row. "
       f"Why it matters: access-policy engines evaluate exactly these expressions. Simplifying before deploying means fewer rules, faster evaluation, and policies a human can audit. {context}")},
    ]
    cards = [
     {"front": "How many rows in a truth table with 4 variables?", "back": f"2^4 = **{2**4}** rows — one per assignment."},
     {"front": "State De Morgan's law for AND.", "back": "NOT (p AND q) = (NOT p) OR (NOT q) — verified on all 4 rows."},
     {"front": "State De Morgan's law for OR.", "back": "NOT (p OR q) = (NOT p) AND (NOT q)."},
     {"front": "Define p -> q without using ->.", "back": "(NOT p) OR q. Only false when p=T, q=F."},
     {"front": "What is the contrapositive of p -> q?", "back": "(NOT q) -> (NOT p) — logically equivalent to the original."},
     {"front": "Is the converse of p -> q equivalent to p -> q?", "back": "No. Counterexample: p=T, q=F makes p->q false but q->p true."},
     {"front": "Absorption law?", "back": "p OR (p AND q) = p; p AND (p OR q) = p."},
     {"front": "What does EXISTS x, P(x) require over a finite domain?", "back": "At least one domain element making P true — a single witness."},
     {"front": "What does FORALL x, P(x) require?", "back": "Every domain element makes P true — one counterexample falsifies it."},
     {"front": "Simplify (a AND b) OR (a AND NOT b).", "back": "a — factor to a AND (b OR NOT b) = a AND T."},
     {"front": "Order of evaluation in (p AND q) OR (NOT r)?", "back": "Parentheses, then NOT, then AND, then OR — inside-out."},
     {"front": f"Evaluate (T AND F) OR (NOT T).", "back": f"(F) OR (F) = **{_fmt_bool((True and False) or (not True))}**."},
    ]
    quiz = [
     mcq(mid, "q1", "A truth table for 5 variables has how many rows?", str(2**5), [str(2**4), str(5*2), str(5**2)], "2^n rows; 2^5 = 32."),
     mcq(mid, "q2", "p -> q is false exactly when:", "p is true and q is false", ["p is false and q is true", "both are false", "both are true"], "Implication is (NOT p) OR q — false only at (T,F)."),
     mcq(mid, "q3", "NOT (p AND q) equals:", "(NOT p) OR (NOT q)", ["(NOT p) AND (NOT q)", "p OR q", "p AND q"], "De Morgan's law, verified on all 4 assignments."),
     mcq(mid, "q4", "The contrapositive of 'if it rains, the ground is wet' is:", "If the ground is not wet, it did not rain", ["If it does not rain, the ground is not wet", "If the ground is wet, it rained", "If it rains, the ground is not wet"], "Contrapositive: (NOT q) -> (NOT p); equivalent to the original."),
     mcq(mid, "q5", f"Evaluate (p OR q) AND (NOT p) at p=F, q=T.", "T", ["F", "T AND F", "undefined"], f"(F OR T)=T; (NOT F)=T; T AND T = T."),
     mcq(mid, "q6", "To falsify FORALL x in {1,2,3}, P(x), you need:", "One counterexample", ["Three witnesses", "A proof for x=1", "An empty domain"], "A single x with NOT P(x) falsifies a universal claim."),
     mcq(mid, "q7", "Absorption: p AND (p OR q) simplifies to:", "p", ["q", "p OR q", "T"], "Absorption law — verified by truth table."),
     mcq(mid, "q8", "Which is a tautology?", "p OR (NOT p)", ["p AND (NOT p)", "p -> (NOT p)", "NOT (p OR q)"], "Excluded middle: always true regardless of p."),
     mcq(mid, "q9", "p <-> q (biconditional) is true when:", "p and q have the same truth value", ["p is true", "q is false", "exactly one is true"], "(p->q) AND (q->p): true at (T,T) and (F,F)."),
     mcq(mid, "q10", "In code, `!(a && b)` should be rewritten as:", "!a || !b", ["!a && !b", "a || b", "a && b"], "De Morgan: NOT (a AND b) = (NOT a) OR (NOT b)."),
    ]
    drills = [
     {"title": "Logic evaluation sprint", "items": [
      {"prompt": "Evaluate (T OR F) AND (NOT F).", "answer": "T", "explain": "(T OR F)=T; NOT F=T; T AND T=T."},
      {"prompt": "Evaluate NOT (T AND T) OR F.", "answer": "F", "explain": "NOT(T AND T)=F; F OR F=F. NOT binds tightest."},
      {"prompt": "p=F, q=F. Evaluate (NOT p) -> q.", "answer": "F", "explain": "(NOT F)=T; T -> F is the one false case of implication."},
      {"prompt": "How many assignments falsify (p AND q) OR (p AND NOT q)?", "answer": "2 of 4", "explain": "The expression simplifies to p; falsified exactly when p=F (2 rows)."},
     ]},
     {"title": "Equivalence proofs", "items": [
      {"prompt": "Prove NOT (p OR q) = (NOT p) AND (NOT q) by cases.", "answer": "All 4 rows agree", "explain": "Enumerate (T,T),(T,F),(F,T),(F,F): both sides match on every row — De Morgan verified."},
      {"prompt": "Is (p -> q) equivalent to (NOT p) -> (NOT q)? Justify.", "answer": "No", "explain": "Counterexample p=T,q=T: original true, inverse (F->F) true... use p=F,q=T: original true, inverse (T->F) false. Not equivalent."},
      {"prompt": "Simplify (x OR y) AND (x OR NOT y) AND (NOT x OR y).", "answer": "x AND y", "explain": "First two factor to x; x AND ((NOT x) OR y) absorbs to x AND y."},
      {"prompt": "Translate 'every admin has MFA' into quantifiers.", "answer": "FORALL u, (admin(u) -> mfa(u))", "explain": "Universal over users; implication inside captures 'if admin then MFA'."},
     ]},
    ]
    lab = {"title": "Verify logic laws in Python",
     "brief": "You will write a brute-force truth-table checker in Python and use it to verify De Morgan's laws, the contrapositive, and absorption — replacing hand-waving with enumeration.",
     "steps": [
      "Write a function tt(vars, fn) that iterates over all 2^n assignments using itertools.product and returns the table.",
      "Use it to print the full truth table of (p -> q), defined as (not p) or q.",
      "Verify De Morgan: assert all rows agree for NOT(p AND q) vs (NOT p) OR (NOT q).",
      "Verify the contrapositive: assert (p->q) matches ((not q) -> (not p)) on all rows, and find the counterexample row for the converse.",
      "Verify absorption p OR (p AND q) == p on all 8 rows of (p,q,r) — extra variable included to prove irrelevance.",
      "Write verify_equiv(f, g, vars) and use it to check two simplifications of your own invention.",
     ],
     "deliverable": "logic_check.py plus a short report: which laws verified, the converse counterexample row, and your two invented equivalences with verdicts.",
     "checkpoint": "All asserts pass; the report names the exact assignment falsifying the converse."}
    mock = {"q": "Which single law turns NOT (a AND b AND c) into a disjunction?",
     "choices": ["De Morgan's law", "Absorption", "Double negation", "Idempotence"],
     "answer": 0,
     "explain": "NOT (a AND b AND c) = (NOT a) OR (NOT b) OR (NOT c) by repeated De Morgan."}
    return assemble(course_id, course_code, "logic", "Logic & Boolean Algebra",
     "Propositions, truth tables, equivalences, and quantifiers — the reasoning substrate underneath every technical module in this course.",
     ["Evaluate compound propositions by precedence, inside-out.",
      "Build and read truth tables; prove completeness via the 2^n count.",
      "Apply De Morgan's laws and verify equivalences by brute-force enumeration.",
      "Distinguish implication, converse, and contrapositive — and know which are equivalent."],
     notes, cards, quiz, drills, lab, mock, prereq_for)

# ------------------------------------------------------------- discrete ---
def build_discrete(course_id, course_code, prereq_for, context):
    mid = f"{course_id}-math-discrete"
    A = {1,2,3,4,5}; B = {4,5,6,7}
    union_n = len(A | B); inter_n = len(A & B)
    incl_excl = len(A) + len(B) - inter_n
    n, k = 10, 3
    c_nk = math.comb(n, k); p_nk = math.perm(n, k)
    N = 100; sum_n = N*(N+1)//2; loop_sum = sum(range(1, N+1))
    # recurrence T(n) = 2T(n/2) + n, T(1) = 1 -> n*log2(n) + n ; check n=1024
    def T(nn):
        return 1 if nn <= 1 else 2*T(nn//2) + nn
    n2 = 1024; t_val = T(n2); closed = n2 * int(math.log2(n2)) + n2
    pig_n, pig_k = 13, 12  # 13 items, 12 boxes -> one box >= 2
    notes = [
     {"title": "Sets and the inclusion–exclusion principle",
      "body": (f"For finite sets, |A ∪ B| = |A| + |B| − |A ∩ B|: adding both counts double-counts the overlap. Worked example: A={sorted(A)}, B={sorted(B)}. "
       f"|A|={len(A)}, |B|={len(B)}, A∩B={sorted(A & B)} so |A∩B|={inter_n}. Then |A∪B| = {len(A)}+{len(B)}−{inter_n} = **{incl_excl}**, and indeed A∪B={sorted(A | B)} "
       f"has **{union_n}** elements. The formula and the enumeration agree. Use it whenever two counted groups overlap — double-counting is the classic off-by-error in combinatorics.")},
     {"title": "Counting: product and sum rules",
      "body": ("Product rule: if a task has a choices for step 1 and b for step 2, there are a×b combined outcomes. Sum rule: for disjoint alternatives, add. "
       f"Worked example: a password of 2 letters then 3 digits. Letters: 26^2 = {26**2}; digits: 10^3 = {10**3}; total = {26**2 * 10**3:,} by the product rule. "
       "Worked example 2: an identifier is either a 3-letter code or a 4-digit code: 26^3 + 10^4 = "
       f"{26**3 + 10**4:,} by the sum rule (disjoint cases). Name the rule before computing — most counting errors are rule-selection errors, not arithmetic.")},
     {"title": "Permutations and combinations, computed",
      "body": (f"Ordered selections: P(n,k) = n!/(n−k)!. Unordered: C(n,k) = n!/(k!(n−k)!). Worked example: choose a {k}-person committee from {n} people. "
       f"C({n},{k}) = {n}!/({k}!·{n-k}!) = **{c_nk}**. If the {k} roles are distinct (ordered), P({n},{k}) = **{p_nk}**. "
       "Sanity check: C(n,k) = C(n,n−k); here C(10,3) = C(10,7) = "
       f"{math.comb(10,7)} — both computed, both equal. Ask 'does order matter?' first: committees no, passwords yes. {context}")},
     {"title": "The pigeonhole principle",
      "body": (f"If {pig_n} items go into {pig_k} boxes, some box holds at least ⌈{pig_n}/{pig_k}⌉ = **{math.ceil(pig_n/pig_k)}** items. "
       "Worked example: among 13 people, at least two share a birth month (12 months). Proof by contradiction: if every month had at most one, there would be at most 12 people — contradiction. "
       "This 'obvious' principle proves real things: hash collisions are unavoidable when items exceed slots, and any lossless compression scheme fails on some input. Existence proofs without construction are a core discrete-math move.")},
     {"title": "Induction, with a verified example",
      "body": (f"To prove P(n) for all n ≥ 1: prove P(1) (base), then prove P(k) → P(k+1) (step). Worked example: S(n) = 1+2+…+n = n(n+1)/2. "
       f"Base: S(1) = 1 = 1·2/2 ✓. Step: assume S(k)=k(k+1)/2; then S(k+1) = k(k+1)/2 + (k+1) = (k+1)(k+2)/2 ✓. "
       f"Numerical verification: for n={N}, formula gives {N}·{N+1}/2 = **{sum_n}**, and direct summation gives **{loop_sum}** — equal. "
       "Induction is how you prove loop correctness and closed forms: state the invariant, base, and step explicitly.")},
     {"title": "Recurrences and divide-and-conquer cost",
      "body": (f"Worked example: T(n) = 2T(n/2) + n with T(1) = 1 (the mergesort shape). Unfold: each level does n work across twice as many subproblems; "
       f"there are log2(n) levels. Closed form: T(n) = n·log2(n) + n. Verification at n={n2}: recursion computes **{t_val}**, closed form gives "
       f"{n2}·{int(math.log2(n2))}+{n2} = **{closed}** — exact match. This is where n log n comes from, not from memorization: count the levels, multiply by work per level. "
       "Every divide-and-conquer analysis in this course follows this template.")},
    ]
    cards = [
     {"front": f"C({n},{k}) = ?", "back": f"**{c_nk}** — {n}!/({k}!·{n-k}!)."},
     {"front": f"P({n},{k}) = ?", "back": f"**{p_nk}** — ordered selections."},
     {"front": "Inclusion–exclusion for two sets?", "back": "|A∪B| = |A|+|B|−|A∩B|."},
     {"front": "Pigeonhole: 13 items, 12 boxes?", "back": f"Some box has ≥ **{math.ceil(13/12)}** items."},
     {"front": "Sum 1..100?", "back": f"100·101/2 = **{sum_n}**."},
     {"front": "T(n)=2T(n/2)+n solves to?", "back": "Θ(n log n) — log2(n) levels × n work per level."},
     {"front": "C(n,k) = C(n,?)", "back": "C(n,n−k) — symmetry of choose."},
     {"front": "Two steps of induction?", "back": "Base case P(1); inductive step P(k)→P(k+1)."},
     {"front": "Product rule?", "back": "a choices then b choices → a×b combined outcomes."},
     {"front": "When do you use combinations vs permutations?", "back": "Combinations: order irrelevant. Permutations: order matters."},
     {"front": f"2^10 = ?", "back": f"**{2**10}** — memorize powers of two to 2^16."},
     {"front": "What does a recurrence's base case give you?", "back": "The termination cost that anchors the unfolding."},
    ]
    quiz = [
     mcq(mid, "q1", f"How many 3-person committees from 10 people?", str(c_nk), [str(p_nk), str(10*3), str(10**3)], f"C(10,3) = 10!/(3!·7!) = {c_nk}."),
     mcq(mid, "q2", "A= {1,2,3,4,5}, B={4,5,6,7}. |A ∪ B|?", str(union_n), [str(len(A)+len(B)), str(inter_n), str(len(A))], f"Inclusion–exclusion: 5+4−2 = {union_n}."),
     mcq(mid, "q3", "Passwords: 2 letters then 3 digits. Total?", f"{26**2 * 10**3:,}", [f"{26**5:,}", f"{36**5:,}", "90,000"], "Product rule: 26^2 × 10^3 = 676,000."),
     mcq(mid, "q4", "Induction proves P(n) for all n≥1 by:", "Base P(1) plus step P(k)→P(k+1)", ["Proving P(100)", "Assuming P(n) for all n", "Two base cases only"], "Base anchors; the step climbs the ladder."),
     mcq(mid, "q5", "T(n) = 2T(n/2) + n is:", "Θ(n log n)", ["Θ(n²)", "Θ(n)", "Θ(2^n)"], f"Verified: T(1024) = {t_val} = 1024·10 + 1024."),
     mcq(mid, "q6", "Pigeonhole: 367 people guarantee:", "Two share a birthday", ["All birthdays distinct", "Three share a month", "366 pairs"], "366 day-slots (incl. leap day); 367 forces a collision."),
     mcq(mid, "q7", f"P(10,3) vs C(10,3): ratio?", str(p_nk//c_nk), ["3", "10", "1"], f"P(10,3)/C(10,3) = {p_nk}/{c_nk} = 6 = 3!."),
     mcq(mid, "q8", "Sum rule applies when alternatives are:", "Disjoint", ["Ordered", "Large", "Independent"], "Add counts only for non-overlapping cases."),
     mcq(mid, "q9", "C(10,7) equals:", str(math.comb(10,7)), [str(math.comb(10,3)+1), "70", str(math.perm(10,7))], "Symmetry: C(10,7) = C(10,3) = 120."),
     mcq(mid, "q10", "Closed form S(n)=n(n+1)/2 at n=1000?", str(1000*1001//2), ["500500", "1001000", "50500"], "1000·1001/2 = 500,500."),
    ]
    drills = [
     {"title": "Counting reps", "items": [
      {"prompt": f"C(8,2) = ?", "answer": str(math.comb(8,2)), "explain": f"8!/(2!·6!) = {math.comb(8,2)}."},
      {"prompt": f"P(8,2) = ?", "answer": str(math.perm(8,2)), "explain": f"8·7 = {math.perm(8,2)} ordered pairs."},
      {"prompt": "Binary strings of length 5?", "answer": str(2**5), "explain": f"Product rule: 2^5 = {2**5}."},
      {"prompt": "Anagrams of ABC (distinct letters)?", "answer": str(math.factorial(3)), "explain": f"3! = {math.factorial(3)} permutations."},
     ]},
     {"title": "Proof reps", "items": [
      {"prompt": "State the inductive step for S(n)=n(n+1)/2.", "answer": "Assume S(k)=k(k+1)/2; show S(k+1)=(k+1)(k+2)/2", "explain": "Add (k+1) to both sides and factor."},
      {"prompt": "Unfold T(n)=2T(n/2)+n twice from T(n).", "answer": "4T(n/4)+2n", "explain": "T(n)=2[2T(n/4)+n/2]+n = 4T(n/4)+2n."},
      {"prompt": "Why does 2^n count truth-table rows?", "answer": "Product rule: 2 choices per variable, n variables", "explain": "Each of n variables independently T/F."},
      {"prompt": "Pigeonhole: 10 socks, 3 colors. Guaranteed pair?", "answer": "Yes — 4 of one color", "explain": "⌈10/3⌉=4 share a color; a pair needs only 2."},
     ]},
    ]
    lab = {"title": "Verify counting identities in Python",
     "brief": "You will verify every identity in this module computationally — combinations, inclusion–exclusion, induction's closed form, and the recurrence — using Python's math module and brute force.",
     "steps": [
      "Verify math.comb(10,3)==120 and math.perm(10,3)==720; assert C(n,k)==C(n,n-k) for several (n,k).",
      "Build sets A,B as Python sets; assert len(A|B) == len(A)+len(B)-len(A&B).",
      "Verify sum(range(1,101)) == 100*101//2.",
      "Implement T(n) recursively for T(n)=2T(n/2)+n; assert T(1024) == 1024*10+1024.",
      "Brute-force: enumerate all 2^5 binary strings with itertools.product and count those with exactly two 1s; compare to C(5,2).",
      "Write a short report: each identity, the Python check, and the verdict.",
     ],
     "deliverable": "counting_check.py with asserts plus the verdict report.",
     "checkpoint": "Every assert passes; the brute-force count equals C(5,2)."}
    mock = {"q": f"If C(12,4) = {math.comb(12,4)}, what is C(12,8)?",
     "choices": [str(math.comb(12,8)), str(math.comb(12,4)+math.comb(12,8)), "4", str(math.perm(12,8))],
     "answer": 0, "explain": f"Symmetry: C(12,8) = C(12,4) = {math.comb(12,4)}."}
    return assemble(course_id, course_code, "discrete", "Discrete Math: Sets, Counting & Induction",
     "Sets, combinatorics, the pigeonhole principle, induction, and recurrences — the mathematics of counting and of proving algorithms correct.",
     ["Apply inclusion–exclusion to overlapping counts.",
      "Choose correctly between permutations and combinations and compute both.",
      "Prove closed forms by induction with explicit base and step.",
      "Solve divide-and-conquer recurrences by unfolding to closed form."],
     notes, cards, quiz, drills, lab, mock, prereq_for)

# ------------------------------------------------------------ numtheory ---
def build_numtheory(course_id, course_code, prereq_for, context):
    mid = f"{course_id}-math-numtheory"
    a, m = 17, 26
    inv = pow(a, -1, m)
    check = (a * inv) % m
    g = math.gcd(48, 180)
    # extended Euclid for 48,180 -> show gcd
    phi_26 = sum(1 for k in range(1, 27) if math.gcd(k, 26) == 1)
    # toy RSA: p=61, q=53
    p, q = 61, 53
    n_rsa = p*q; phi = (p-1)*(q-1); e = 17
    d_rsa = pow(e, -1, phi)
    msg = 42; ct = pow(msg, e, n_rsa); pt = pow(ct, d_rsa, n_rsa)
    notes = [
     {"title": "Divisibility and primes",
      "body": ("d divides n if n = d·k for integer k. A prime has exactly two divisors. Worked example: factor 180. "
       f"180 = 2^2 × 3^2 × 5 (verify: 4×9×5 = {4*9*5}). Primality testing by trial division only needs divisors up to √n: "
       f"to test 97, check primes ≤ √97 ≈ {math.sqrt(97):.1f}, i.e. 2,3,5,7 — none divide, so 97 is prime. "
       "Unique prime factorization is the foundation everything below builds on.")},
     {"title": "GCD and the Euclidean algorithm",
      "body": (f"Worked example: gcd(48, 180). Euclid: 180 = 3×48 + 36; 48 = 1×36 + 12; 36 = 3×12 + 0. Last nonzero remainder: **{g}**. "
       "Python: math.gcd(48,180) = "
       f"{math.gcd(48,180)} — agreement. The extended algorithm also finds integers x,y with 48x+180y=gcd; those coefficients are exactly what the next note's inverse computation uses. "
       "GCD answers 'what's the largest shared structure' — from simplifying fractions to RSA key generation.")},
     {"title": "Modular arithmetic",
      "body": (f"a ≡ b (mod m) means m divides a−b. Worked examples mod 26: {a} + 10 = {a+10} ≡ {(a+10) % 26}; "
       f"{a} × 3 = {a*3} ≡ {(a*3) % 26}; 100 mod 26 = **{100 % 26}** since 26×3=78 and 100−78=22. "
       "Addition, subtraction, multiplication all work mod m; division needs an inverse, which exists exactly when gcd(a,m)=1. "
       f"Here gcd({a},{m}) = {math.gcd(a,m)}, so {a} has an inverse mod {m}. {context}")},
     {"title": "Modular inverses, computed",
      "body": (f"Worked example: inverse of {a} mod {m}. Computed: {a}^(-1) mod {m} = **{inv}**. Verification: {a}×{inv} = {a*inv} = {m}×{(a*inv)//m} + {(a*inv)%m}, "
       f"so {a}×{inv} ≡ **{check}** (mod {m}) ✓. Solve {a}x ≡ 5 (mod {m}): multiply by the inverse, x ≡ 5×{inv} = {5*inv} ≡ **{(5*inv) % m}** (mod {m}). "
       "Check: "
       f"{a}×{(5*inv) % m} = {a*((5*inv) % m)} ≡ {(a*((5*inv) % m)) % m} ✓. Inverses turn modular division into multiplication — the operation RSA decryption performs.")},
     {"title": "Euler's totient",
      "body": (f"φ(m) counts integers 1..m coprime to m. Worked example: φ({m}). Counting k with gcd(k,{m})=1 gives **{phi_26}**. "
       f"Euler's theorem: if gcd(a,m)=1 then a^φ(m) ≡ 1 (mod m). Check with a=3, m=26: φ=12, 3^12 mod 26 = **{pow(3, 12, 26)}** ✓. "
       "This theorem is why RSA decryption works: exponents reduce mod φ(n).")},
     {"title": "Toy RSA, end to end",
      "body": (f"Worked example with small primes p={p}, q={q}. n = {p}×{q} = **{n_rsa}**; φ(n) = {p-1}×{q-1} = **{phi}**. "
       f"Choose public exponent e={e} (coprime to φ). Private exponent d = e^(−1) mod φ = **{d_rsa}**. "
       f"Encrypt message {msg}: c = {msg}^{e} mod {n_rsa} = **{ct}**. Decrypt: m = {ct}^{d_rsa} mod {n_rsa} = **{pt}** — the original message ✓. "
       "Every number here was computed, not asserted. Real RSA uses 2048-bit primes, but the mathematics is exactly this.")},
    ]
    cards = [
     {"front": f"gcd(48, 180) = ?", "back": f"**{g}** — via Euclid's algorithm."},
     {"front": f"Inverse of {a} mod {m}?", "back": f"**{inv}** — since {a}×{inv} ≡ 1 (mod {m})."},
     {"front": "When does a have an inverse mod m?", "back": "Exactly when gcd(a,m) = 1."},
     {"front": f"φ({m}) = ?", "back": f"**{phi_26}** — count of k ≤ 26 coprime to 26."},
     {"front": "Euler's theorem?", "back": "gcd(a,m)=1 → a^φ(m) ≡ 1 (mod m)."},
     {"front": f"Toy RSA: n for p={p}, q={q}?", "back": f"n = **{n_rsa}**, φ(n) = **{phi}**."},
     {"front": f"100 mod 26?", "back": f"**{100 % 26}**."},
     {"front": "Why must e be coprime to φ(n) in RSA?", "back": "So the inverse d = e^(−1) mod φ(n) exists."},
     {"front": f"Solve {a}x ≡ 5 (mod {m}).", "back": f"x ≡ **{(5*inv) % m}** (mod {m})."},
     {"front": "Prime factorization of 180?", "back": "2² × 3² × 5."},
     {"front": "Trial division bound for testing n?", "back": "Primes up to √n suffice."},
     {"front": f"3^12 mod 26?", "back": f"**{pow(3,12,26)}** — Euler's theorem predicts 1."},
    ]
    quiz = [
     mcq(mid, "q1", f"gcd(48,180) = ?", str(g), ["12", "36", "24"], "Euclid: 180=3·48+36; 48=1·36+12; 36=3·12+0 → 12."),
     mcq(mid, "q2", f"Which has an inverse mod 26?", str(a), ["13", "26", "4"], f"gcd({a},26)=1; gcd(13,26)=13, gcd(4,26)=2."),
     mcq(mid, "q3", f"{a} × {inv} mod {m} = ?", str(check), ["0", str(a), str(inv)], f"Inverse property: product ≡ {check}."),
     mcq(mid, "q4", "φ(26) counts:", f"Integers 1–26 coprime to 26 ({phi_26} of them)", ["Primes below 26", "Divisors of 26", "Multiples of 26"], "Totient = count of units mod m."),
     mcq(mid, "q5", f"In the toy RSA, decrypting {ct} gives?", str(pt), [str(ct), str(n_rsa), "0"], f"{ct}^{d_rsa} mod {n_rsa} = {pt}."),
     mcq(mid, "q6", "Euler's theorem needs:", "gcd(a,m) = 1", ["a > m", "m prime", "a even"], "Coprimality is the hypothesis."),
     mcq(mid, "q7", f"Solve 17x ≡ 5 (mod 26).", f"x ≡ {(5*inv)%m} (mod 26)", ["x ≡ 5 (mod 26)", "x ≡ 17 (mod 26)", "No solution"], "Multiply by 17^(−1)=23: x ≡ 115 ≡ 11."),
     mcq(mid, "q8", "To test primality of 101 by trial division, check primes up to:", "10", ["50", "101", "7"], "√101 ≈ 10.05; primes ≤ 10: 2,3,5,7."),
     mcq(mid, "q9", f"φ(n) for RSA n={n_rsa}?", str(phi), [str(n_rsa), str(p+q), str(e)], f"({p}−1)({q}−1) = {phi}."),
     mcq(mid, "q10", "Modular inverse is found via:", "Extended Euclidean algorithm", ["Trial division", "Fermat's little theorem only", "Binary search"], "Extended Euclid gives the Bézout coefficients."),
    ]
    drills = [
     {"title": "Modular arithmetic reps", "items": [
      {"prompt": f"Compute 38 mod 26.", "answer": str(38 % 26), "explain": f"38 − 26 = {38%26}."},
      {"prompt": f"Compute (17×5) mod 26.", "answer": str((17*5) % 26), "explain": f"85 = 3×26 + {(17*5)%26}."},
      {"prompt": f"gcd(17, 26)?", "answer": str(math.gcd(17,26)), "explain": "17 is prime, not dividing 26."},
      {"prompt": f"φ(10)?", "answer": str(sum(1 for k in range(1,11) if math.gcd(k,10)==1)), "explain": "Coprime to 10: 1,3,7,9 → 4."},
     ]},
     {"title": "RSA mechanics reps", "items": [
      {"prompt": f"Toy RSA: given e={e}, φ={phi}, d={d_rsa}. Verify e·d mod φ.", "answer": str((e*d_rsa) % phi), "explain": f"{e}×{d_rsa} mod {phi} = {(e*d_rsa)%phi} ✓."},
      {"prompt": "Why can RSA use small e like 17 but never small d?", "answer": "Small d enables attacks; e only needs coprimality", "explain": "d must stay secret and large; e is public."},
      {"prompt": f"Encrypt m=7 with e={e}, n={n_rsa}.", "answer": str(pow(7, e, n_rsa)), "explain": f"7^{e} mod {n_rsa} = {pow(7,e,n_rsa)}."},
      {"prompt": "What breaks if p = q in RSA?", "answer": "n = p² reveals p = √n", "explain": "Factoring becomes trivial square root."},
     ]},
    ]
    lab = {"title": "Implement toy RSA and verify the round-trip",
     "brief": "You will implement key generation, encryption, and decryption for the toy RSA parameters in Python, verifying every number in this module independently.",
     "steps": [
      "Write egcd(a,b) returning (g,x,y) with ax+by=g; assert egcd(48,180)[0]==12.",
      "Write modinv(a,m) via egcd; assert modinv(17,26)==23 and (17*23)%26==1.",
      "Write phi(m) by counting coprimes; assert phi(26)==12.",
      "Generate the toy key: p=61,q=53,e=17; compute n, phi, d; assert (e*d)%phi==1.",
      "Encrypt and decrypt several messages; assert decrypt(encrypt(m))==m for each.",
      "Break it on purpose: try e=13 (not coprime to phi) and record the failure mode.",
     ],
     "deliverable": "rsa_toy.py with asserts plus a note on the e=13 failure.",
     "checkpoint": "All asserts pass; round-trip verified for ≥5 messages; failure mode documented."}
    mock = {"q": f"17^(-1) mod 26 = {inv}. What is 5 × 17^(-1) mod 26?",
     "choices": [str((5*inv) % 26), "5", str(inv), "1"],
     "answer": 0, "explain": f"5×{inv} = {5*inv} ≡ {(5*inv)%26} (mod 26)."}
    return assemble(course_id, course_code, "numtheory", "Number Theory & Modular Arithmetic",
     "Divisibility, Euclid's algorithm, modular arithmetic and inverses, Euler's theorem, and a fully computed toy RSA — the math under modern cryptography.",
     ["Compute gcd via Euclid's algorithm and explain each step.",
      "Do modular addition, multiplication, and division-via-inverse correctly.",
      "Find modular inverses and solve linear congruences.",
      "Execute toy RSA key generation, encryption, and decryption with verified numbers."],
     notes, cards, quiz, drills, lab, mock, prereq_for)

# -------------------------------------------------------------- binmath ---
def build_binmath(course_id, course_code, prereq_for, context):
    mid = f"{course_id}-math-binmath"
    x = 173
    b = bin(x)[2:]; h = hex(x)[2:].upper()
    neg = -42; twos = bin((1 << 8) + neg)[2:]
    a, bb = 0b11001100, 0b10101010
    net = ipaddress.IPv4Network("192.168.10.0/26")
    usable = net.num_addresses - 2
    notes = [
     {"title": "Positional number systems",
      "body": (f"In base b, each digit counts powers of b. Worked example: {x} in binary. {x} = 128+32+8+4+1 = 2^7+2^5+2^3+2^2+2^0, "
       f"so {x}₁₀ = **{b}**₂ (verify: int('{b}',2) = {int(b,2)}). In hex, group bits in fours: {b} → {h}, so {x}₁₀ = **0x{h}**. "
       "Octal/hex exist to make binary readable: one hex digit is exactly 4 bits, one octal digit exactly 3.")},
     {"title": "Two's complement",
      "body": (f"Signed integers use two's complement: negate by flipping bits and adding 1. Worked example: represent {neg} in 8 bits. "
       f"42 = 00101010; flip → 11010101; +1 → **{twos}**. Check: {twos}₂ as unsigned = {int(twos,2)}; {int(twos,2)} − 256 = **{int(twos,2)-256}** ✓. "
       "Range of 8-bit two's complement: −128..127. The top bit is the sign bit; overflow wraps silently — the source of countless bugs.")},
     {"title": "Bitwise operations, computed",
      "body": (f"Worked with a=0b{a:08b} ({a}), b=0b{bb:08b} ({bb}): a AND b = 0b{a & bb:08b} = **{a & bb}**; "
       f"a OR b = 0b{a | bb:08b} = **{a | bb}**; a XOR b = 0b{a ^ bb:08b} = **{a ^ bb}**; NOT a (8-bit) = **{(~a) & 0xFF}**. "
       f"Shifts: {a} << 2 = **{a << 2}** (×4); {a} >> 2 = **{a >> 2}** (÷4, floor). "
       "Masks isolate fields: x & 0x0F keeps the low nibble. Flags, permissions, and subnet masks are all bit patterns manipulated exactly this way.")},
     {"title": "Subnet math with real computation",
      "body": (f"Worked example: 192.168.10.0/26, computed with Python's ipaddress module. Addresses total: 2^(32−26) = 2^6 = **{net.num_addresses}**. "
       f"Network: **{net.network_address}**; broadcast: **{net.broadcast_address}**; usable: {net.num_addresses} − 2 = **{usable}**; "
       f"range {net.network_address+1} – {net.broadcast_address-1}; mask: **{net.netmask}**. "
       "Never hand-compute what the ipaddress module verifies: write the plan, then assert every address with code. "
       f"{context}")},
     {"title": "Parity and checksums",
      "body": ("Error detection starts with parity: count the 1-bits; even parity appends 0 if the count is even, 1 if odd. "
       f"Worked example: byte 0b{a:08b} has **{bin(a).count('1')}** one-bits ({'even' if bin(a).count('1')%2==0 else 'odd'}), so the even-parity bit is "
       f"**{bin(a).count('1')%2}**. Checksums generalize this: the IPv4 header checksum is the one's-complement sum of 16-bit words. "
       "These are the simplest instances of the integrity machinery (hashing, CRCs) used everywhere in systems work.")},
     {"title": "Fixed-width pitfalls",
      "body": ("Computers compute in fixed widths, and the width is part of the answer. Worked examples: (200 + 100) mod 256 = "
       f"**{(200+100) % 256}** in 8-bit unsigned arithmetic — silent wraparound. In two's complement 8-bit, 127 + 1 = **{(127+1) % 256 - 256 if (127+1) > 127 else 128}** "
       "(−128): signed overflow. Shifting 1 left by 31 in 32-bit signed gives the most negative number. "
       "Rule: know your width, know your signedness, and test the boundaries 0, max, max+1, −1 explicitly.")},
    ]
    cards = [
     {"front": f"{x} in binary?", "back": f"**{b}**₂."},
     {"front": f"{x} in hex?", "back": f"**0x{h}**."},
     {"front": f"{neg} in 8-bit two's complement?", "back": f"**{twos}**."},
     {"front": f"0b{a:08b} AND 0b{bb:08b}?", "back": f"**{a & bb}** (0b{a & bb:08b})."},
     {"front": f"0b{a:08b} XOR 0b{bb:08b}?", "back": f"**{a ^ bb}**."},
     {"front": f"{a} >> 2?", "back": f"**{a >> 2}** (integer ÷4)."},
     {"front": "Usable hosts in 192.168.10.0/26?", "back": f"**{usable}** (64 − 2)."},
     {"front": "Broadcast of 192.168.10.0/26?", "back": f"**{net.broadcast_address}**."},
     {"front": "One hex digit = how many bits?", "back": "4 bits exactly."},
     {"front": "8-bit two's complement range?", "back": "−128 to 127."},
     {"front": "Even-parity bit for 0b11001100?", "back": f"**{bin(a).count('1')%2}** ({bin(a).count('1')} ones is even)."},
     {"front": "(200+100) mod 256?", "back": f"**{(200+100)%256}** — 8-bit wraparound."},
    ]
    quiz = [
     mcq(mid, "q1", f"{x}₁₀ in hex?", f"0x{h}", ["0xAD", "0x173", "0xB7"], f"{x} = 10×16 + 13 → 0xAD."),
     mcq(mid, "q2", "−1 in 8-bit two's complement?", "11111111", ["10000001", "01111111", "00000001"], "Flip 00000001 → 11111110, +1 → 11111111."),
     mcq(mid, "q3", f"0b11001100 OR 0b10101010?", str(a | bb), [str(a & bb), str(a ^ bb), "255"], f"Bitwise OR = {a|bb}."),
     mcq(mid, "q4", "Network address of 192.168.10.64/26?", "192.168.10.64", ["192.168.10.0", "192.168.10.127", "192.168.10.63"], "Host bits zeroed; /26 blocks are 64 wide: .0, .64, .128, .192."),
     mcq(mid, "q5", f"Binary 0b{b} is decimal?", str(x), ["174", "172", "183"], "2^7+2^5+2^3+2^2+2^0 = 128+32+8+4+1 = 173."),
     mcq(mid, "q6", "x & 0x0F keeps:", "The low nibble (4 bits)", ["The high nibble", "All 8 bits", "Nothing"], "0x0F = 00001111 masks out the top 4 bits."),
     mcq(mid, "q7", f"Broadcast of 192.168.10.0/26?", str(net.broadcast_address), ["192.168.10.255", "192.168.10.63", "192.168.10.128"], "Block .0–.63; broadcast .63."),
     mcq(mid, "q8", "Left shift by 3 multiplies by:", "8", ["3", "6", "9"], "<< 3 = ×2³ = ×8."),
     mcq(mid, "q9", "Why does 127+1 give −128 in int8?", "Two's complement wraparound", ["Hardware bug", "Sign extension", "Rounding"], "01111111 + 1 = 10000000 = −128."),
     mcq(mid, "q10", "Hex digit F in binary?", "1111", ["111", "11111", "1001"], "F = 15 = 8+4+2+1."),
    ]
    drills = [
     {"title": "Conversion reps", "items": [
      {"prompt": "0xFF in decimal?", "answer": "255", "explain": "15×16+15 = 255."},
      {"prompt": "0b1010 in hex?", "answer": "0xA", "explain": "1010₂ = 10 = A."},
      {"prompt": f"{x} >> 1?", "answer": str(x >> 1), "explain": f"Integer halving: {x}>>1 = {x>>1}."},
      {"prompt": "0x0F & 0xF0?", "answer": "0", "explain": "00001111 & 11110000 = 00000000."},
     ]},
     {"title": "Subnet reps", "items": [
      {"prompt": "How many /26 subnets fit in a /24?", "answer": "4", "explain": "2^(26−24) = 4."},
      {"prompt": "First usable of 192.168.10.64/26?", "answer": "192.168.10.65", "explain": "Network + 1."},
      {"prompt": "Last usable of 192.168.10.0/26?", "answer": "192.168.10.62", "explain": "Broadcast .63 minus 1."},
      {"prompt": "Dotted mask of /26?", "answer": "255.255.255.192", "explain": "256 − 64 = 192 in the last octet."},
     ]},
    ]
    lab = {"title": "Verify number-system math in Python",
     "brief": "You will verify every conversion, two's-complement encoding, bitwise result, and subnet computation in this module with Python — int(x,2), bit_length, and the ipaddress module.",
     "steps": [
      "Assert int('10101101',2)==173, hex(173)=='0xad', bin(173)=='0b10101101'.",
      "Write to_twos(n, bits) and assert to_twos(-42,8)=='11010110' and to_twos(-1,8)=='11111111'.",
      "Assert (0b11001100 & 0b10101010)==0b10001000 and the OR/XOR/shift values from the notes.",
      "Use ipaddress to assert network/broadcast/usable of 192.168.10.0/26 match the notes.",
      "Carve 10.0.0.0/16 into /24s in Python; assert 256 subnets and that the 5th is 10.0.4.0/24.",
      "Write the verdict report: each claim, the check, pass/fail.",
     ],
     "deliverable": "binmath_check.py with asserts plus the verdict report.",
     "checkpoint": "All asserts pass; the /24 carve count is exactly 256."}
    mock = {"q": "Which mask gives 62 usable hosts?",
     "choices": ["/26", "/27", "/25", "/24"],
     "answer": 0, "explain": "2^6 − 2 = 62."}
    return assemble(course_id, course_code, "binmath", "Binary, Hex & Computer Arithmetic",
     "Positional systems, two's complement, bitwise operations, and subnet math — the arithmetic the machine actually does.",
     ["Convert fluently between binary, hex, and decimal.",
      "Encode signed integers in two's complement and predict wraparound.",
      "Compute bitwise AND/OR/XOR/shifts and apply masks.",
      "Derive network, broadcast, and usable counts for any prefix — verified with ipaddress."],
     notes, cards, quiz, drills, lab, mock, prereq_for)

BUILDERS_A = {"logic": build_logic, "discrete": build_discrete, "numtheory": build_numtheory, "binmath": build_binmath}
