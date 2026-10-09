#!/usr/bin/env python3
"""W2 diagram kits — IL-07 through IL-12. Each kit = 4 diagram specs for one topic.
Spec: (kind, args, caption, alt, note_keywords)
kind in: flow | layers | compare | table | concept
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diag_framework import Diagram, GREEN, ORANGE, RED, PURPLE, CYAN, ACCENT

def S(kind, args, cap, alt, nk):
    return (kind, args, cap, alt, nk)

def build(spec, fig_num):
    kind, args, caption, alt = spec[0], spec[1], spec[2], spec[3]
    d = Diagram(fig_num=fig_num, caption=caption, alt=alt)
    rest = {k: v for k, v in args.items() if k not in
            ('steps', 'layers', 'lt', 'li', 'rt', 'ri', 'name', 'cols', 'title', 'lines')}
    if kind == 'flow':
        d.flow(args['steps'], **rest)
    elif kind == 'layers':
        d.layers(args['layers'], **rest)
    elif kind == 'compare':
        d.compare(args['lt'], args['li'], args['rt'], args['ri'], **rest)
    elif kind == 'table':
        d.table_schema(args['name'], args['cols'], **rest)
    elif kind == 'concept':
        d.concept_box(args['title'], args['lines'], **rest)
    else:
        raise ValueError(kind)
    d.animate()  # user order 2026-10-09: ALL diagrams animated, no static SVGs
    return d.render_figure()

KITS = {}

# ================= SHARED MATH KITS =================

KITS['prob-stats'] = [
    S('compare',
      {'lt': 'Mean', 'li': ['Pulled by every outlier', 'Right for symmetric data', 'Minimizes squared error'],
       'rt': 'Median', 'ri': ['Ignores extreme tails', 'Right for skewed data', 'Minimizes absolute error']},
      'The mean listens to every data point including outliers; the median listens only to the middle. '
      'For skewed data such as salaries or latencies, the median describes the typical case honestly.',
      'Comparison diagram: Mean vs Median trade-offs', ['describing', 'concepts']),
    S('flow',
      {'steps': [('Prior', 'P(H) base rate'), ('Likelihood', 'P(E|H) evidence'), ('Posterior', 'P(H|E) updated'), ('Decide', 'act on odds')]},
      "Bayes' theorem updates a prior belief with observed evidence to produce a posterior. "
      'Ignoring the base rate is why a 99%-accurate test can still be wrong most of the time on a rare condition.',
      'Flow diagram of the Bayesian update: prior, likelihood, posterior, decision', ['bayes', 'conditional']),
    S('table',
      {'name': 'binomial(n, p)', 'cols': [('n', 'INTEGER', 'trials'), ('p', 'FLOAT', '0..1'),
                                          ('P(X=k)', 'FORMULA', 'C(n,k) p^k (1-p)^(n-k)'),
                                          ('E[X]', 'FLOAT', 'n·p'), ('Var', 'FLOAT', 'n·p·(1-p)')]},
      'The binomial distribution models k successes in n independent trials with success probability p. '
      'Its expected value n·p is the workhorse for capacity planning and A/B-test sizing.',
      'Table of binomial distribution parameters and formulas', ['binomial', 'expectation']),
    S('concept',
      {'title': 'p99, not the mean', 'lines': ['Mean latency hides the tail', 'p50 = typical user experience',
                                               'p99 = worst 1% experience', 'SLOs are written in percentiles'],
       'accent': ORANGE},
      'Averages hide the users who suffer most: a 50 ms mean can conceal a 5 s tail. '
      'Percentiles like p99 pin the tail down, which is why SLOs are always stated as "p99 < X ms".',
      'Concept box explaining percentiles and SLO math', ['percentile', 'slo']),
]

KITS['linalg'] = [
    S('concept',
      {'title': 'Dot product = alignment', 'lines': ['a·b = Σ aᵢbᵢ', 'a·b = |a||b| cos θ',
                                                     'cos θ = similarity score', 'θ = 0° → identical direction'],
       'accent': ACCENT},
      'The dot product measures how much two vectors point the same way. '
      'Dividing by the lengths gives cosine similarity — the score behind search, recommendations, and embeddings.',
      'Concept box: dot product and cosine similarity', ['dot product', 'vectors']),
    S('table',
      {'name': 'matrix multiply C = AB', 'cols': [('shape', 'TEXT', 'A: m×n, B: n×p → C: m×p'),
                                                  ('C[i,j]', 'FORMULA', 'Σₖ A[i,k]·B[k,j]'),
                                                  ('cost', 'BIG-O', 'O(m·n·p)'),
                                                  ('AB vs BA', 'FACT', 'not equal, usually')]},
      'Matrix multiplication composes linear maps: each entry of C is a dot product of a row of A with a column of B. '
      'Order matters — AB ≠ BA in general — because applying rotation then scaling differs from scaling then rotation.',
      'Table of matrix multiplication rules', ['matrix', 'multiplication']),
    S('concept',
      {'title': 'Eigenvalues of a 2×2', 'lines': ['Solve det(A − λI) = 0', 'λ from: λ² − tr(A)λ + det(A) = 0',
                                                   'tr(A) = λ₁ + λ₂', 'det(A) = λ₁ · λ₂'],
       'accent': PURPLE},
      'Eigenvalues are the stretch factors along the directions a matrix leaves unchanged. '
      'For a 2×2 they fall out of one quadratic whose coefficients are the trace and determinant — a built-in checksum.',
      'Concept box: eigenvalues via trace and determinant', ['eigenvalue', 'determinant']),
    S('flow',
      {'steps': [('Residuals', 'y − Xβ error'), ('Square them', 'Σ residual²'), ('Minimize', 'normal equations'), ('β̂', 'best-fit line')]},
      'Least squares finds the line (or hyperplane) minimizing the sum of squared residuals. '
      'Squaring penalizes large misses hardest, which is also why a single outlier can drag the whole fit.',
      'Flow diagram of the least-squares fitting procedure', ['least squares', 'solving']),
]

KITS['discrete'] = [
    S('concept',
      {'title': 'Inclusion–exclusion', 'lines': ['|A ∪ B| = |A| + |B| − |A ∩ B|', 'Add both, subtract the overlap',
                                                 '3 sets: add back triple overlap', 'Counts each element exactly once'],
       'accent': ACCENT},
      'Inclusion–exclusion corrects double-counting: adding two sets counts their intersection twice, so subtract it once. '
      'It is the reason "or" probabilities are not simply additive.',
      'Concept box: inclusion-exclusion principle', ['inclusion', 'sets']),
    S('compare',
      {'lt': 'Permutations', 'li': ['Order matters', 'P(n,k) = n!/(n−k)!', 'Passwords, rankings'],
       'rt': 'Combinations', 'ri': ['Order irrelevant', 'C(n,k) = n!/(k!(n−k)!)', 'Committees, samples']},
      'Permutations count arrangements where order matters; combinations count selections where it does not. '
      'Choosing the wrong one is the single most common counting error — ask "would swapping change the outcome?"',
      'Comparison: permutations vs combinations', ['permutation', 'combination', 'counting']),
    S('concept',
      {'title': 'Pigeonhole principle', 'lines': ['n+1 items, n boxes → one box holds ≥ 2', 'No counting needed — pure logic',
                                                   'Powers hashing collision arguments', 'Birthdays, caches, hash tables'],
       'accent': ORANGE},
      'With more items than containers, some container must hold two. '
      'This one-line argument proves hash collisions are unavoidable and underlies the birthday bound on hash sizes.',
      'Concept box: the pigeonhole principle', ['pigeonhole']),
    S('flow',
      {'steps': [('Base case', 'P(0) holds'), ('Inductive step', 'P(k) → P(k+1)'), ('Recurrence', 'T(n) = 2T(n/2)+n'), ('Closed form', 'T(n) = n log n')]},
      'Induction proves a statement for all n by anchoring a base case and chaining each step to the next. '
      'Unfolding a divide-and-conquer recurrence the same way turns T(n) = 2T(n/2) + n into the familiar n log n.',
      'Flow: induction proof structure applied to recurrences', ['induction', 'recurrence']),
]

KITS['logic'] = [
    S('table',
      {'name': 'truth table: ∧ ∨ ¬ →', 'cols': [('p q', 'INPUTS', 'T T / T F / F T / F F'),
                                                ('p ∧ q', 'AND', 'T F F F'), ('p ∨ q', 'OR', 'T T T F'),
                                                ('p → q', 'IMPLIES', 'T F T T'), ('¬p', 'NOT', 'F F T T')]},
      'Truth tables enumerate all 2ⁿ input rows, which is why they settle any equivalence by brute force. '
      'Note the implication row: p → q is only false when a true premise leads to a false conclusion.',
      'Table of truth values for AND, OR, NOT, and implication', ['truth', 'proposition']),
    S('concept',
      {'title': "De Morgan's laws", 'lines': ['¬(p ∧ q) ≡ ¬p ∨ ¬q', '¬(p ∨ q) ≡ ¬p ∧ ¬q',
                                               'Negation flips AND ↔ OR', 'Check: brute-force all 4 rows'],
       'accent': ACCENT},
      "De Morgan's laws push a negation through a compound statement by flipping the connective. "
      'They are the workhorse for simplifying conditions like "not (admin and active)" into "not admin or not active".',
      'Concept box: De Morgan laws', ['morgan', 'truth']),
    S('compare',
      {'lt': 'Implication p → q', 'li': ['"if p then q"', 'Contrapositive ≡ : ¬q → ¬p', 'Converse ≢ : q → p'],
       'rt': 'Common trap', 'ri': ['"q therefore p" is affirming the consequent', 'Converse is NOT equivalent', 'Test with truth tables']},
      'An implication is equivalent to its contrapositive but NOT to its converse. '
      '"If the server is down, the site is unreachable" does not mean an unreachable site implies the server is down.',
      'Comparison: implication vs its converse and contrapositive', ['implication', 'contrapositive']),
    S('flow',
      {'steps': [('∀x P(x)', 'for all'), ('Instantiate', 'pick arbitrary c'), ('Prove P(c)', 'no special facts'), ('Generalize', '∀x P(x) QED')]},
      'Predicate logic extends propositions with quantifiers over a domain. '
      'To prove a universal claim, prove it for an arbitrary element using nothing special about it — then it holds for all.',
      'Flow: proving a universally quantified statement', ['predicate', 'quantifier']),
]

KITS['binmath'] = [
    S('table',
      {'name': 'positional systems', 'cols': [('binary', 'BASE 2', '… 8 4 2 1'), ('octal', 'BASE 8', 'groups of 3 bits'),
                                              ('decimal', 'BASE 10', 'human I/O'), ('hex', 'BASE 16', 'groups of 4 bits'),
                                              ('0xFF', 'EXAMPLE', '= 255 = 1111 1111')]},
      'Positional systems all work the same way: each digit is multiplied by the base raised to its position. '
      'Hex is simply a compact way to write binary — every hex digit is exactly one nibble.',
      'Table comparing binary, octal, decimal, and hexadecimal', ['positional', 'number']),
    S('concept',
      {'title': "Two's complement", 'lines': ['Negative x → invert bits of x, add 1', 'Range (8-bit): −128 … +127',
                                               'One zero: +0 only', 'Overflow wraps: 127 + 1 = −128'],
       'accent': ORANGE},
      "Two's complement encodes negatives so that addition hardware works unchanged for signed values. "
      'The price is asymmetric range and silent wraparound — the root of countless integer-overflow bugs.',
      'Concept box: two complement encoding and wraparound', ['complement', 'signed']),
    S('table',
      {'name': 'bitwise ops (x=0b1100, y=0b1010)', 'cols': [('x & y', 'AND mask', '0b1000 = 8'),
                                                             ('x | y', 'OR set', '0b1110 = 14'),
                                                             ('x ^ y', 'XOR flip', '0b0110 = 6'),
                                                             ('x << 2', 'SHIFT', '0b110000 = 48')]},
      'Bitwise operators work on each bit position independently, making them ideal for flags and masks. '
      'AND clears bits, OR sets them, XOR toggles them, and a left shift by n multiplies by 2ⁿ.',
      'Table of bitwise AND, OR, XOR, and shift with examples', ['bitwise', 'operations']),
    S('concept',
      {'title': 'Subnet math: /24', 'lines': ['32 bits: network | host', '/24 → 8 host bits → 254 usable',
                                               'Network = AND(ip, mask)', 'Broadcast = network OR ~mask'],
       'accent': GREEN},
      'A /24 reserves 8 bits for hosts: 2⁸ − 2 = 254 usable addresses after subtracting network and broadcast. '
      'AND-ing the IP with the mask always recovers the network address — the one computation subnetting is built on.',
      'Concept box: subnet mask arithmetic', ['subnet', 'network']),
]

KITS['numtheory'] = [
    S('flow',
      {'steps': [('a, b', 'inputs'), ('r = a mod b', 'remainder'), ('a ← b, b ← r', 'shrink'), ('b = 0 → gcd', 'answer')]},
      'The Euclidean algorithm replaces the pair (a, b) with (b, a mod b) until the remainder is zero. '
      'Each step strictly shrinks the numbers, so it terminates — and the last nonzero remainder is the GCD.',
      'Flow diagram of the Euclidean algorithm', ['euclidean', 'gcd', 'divisibility']),
    S('concept',
      {'title': 'Modular arithmetic', 'lines': ['a ≡ b (mod n) ⟺ n | (a−b)', '(a+b) mod n, (a·b) mod n stay in range',
                                                 'Clock arithmetic: 10 + 5 ≡ 3 (mod 12)', 'Powers cycle: Fermat, Euler'],
       'accent': ACCENT},
      'Modular arithmetic wraps numbers around a modulus like hours on a clock. '
      'Addition and multiplication stay inside the ring, which is exactly what keeps cryptographic computations bounded.',
      'Concept box: congruence and modular operations', ['modular', 'arithmetic']),
    S('concept',
      {'title': 'Modular inverses', 'lines': ['a⁻¹ exists ⟺ gcd(a, n) = 1', 'Found by extended Euclid',
                                               'a · a⁻¹ ≡ 1 (mod n)', 'Division mod n = multiply by inverse'],
       'accent': PURPLE},
      'Division does not exist modulo n — but when a and n are coprime, a has an inverse that behaves like one. '
      'The extended Euclidean algorithm computes it, and RSA decryption is literally "multiply by the inverse exponent".',
      'Concept box: modular inverses via extended Euclid', ['inverse', 'totient']),
    S('flow',
      {'steps': [('Pick p, q', 'two primes'), ('n = pq, φ(n)', 'public modulus'), ('e·d ≡ 1 mod φ', 'key pair'), ('c = m^e, m = c^d', 'encrypt/decrypt')]},
      'Toy RSA: multiply two primes for the modulus, pick e coprime to φ(n), and solve for d as its inverse. '
      'Encryption cubes (or e-powers) the message; only the holder of d can undo it — factoring n is the hard problem guarding it.',
      'Flow diagram of toy RSA key generation and use', ['rsa']),
]

KITS['quantreason'] = [
    S('concept',
      {'title': 'Expected value decides', 'lines': ['EV = Σ pᵢ · xᵢ', 'Positive EV → take the bet, repeated',
                                                     'Salary: EV of offer = base + p(bonus)·bonus', 'Never decide on the best case alone'],
       'accent': GREEN},
      'Expected value weights every outcome by its probability, turning "maybe" into a number. '
      'For career bets — offers, freelance gigs, bootcamps — compare EVs, not headlines.',
      'Concept box: expected value for career decisions', ['expected value', 'decision']),
    S('table',
      {'name': 'total compensation', 'cols': [('base', '$/YR', 'guaranteed'), ('bonus', '% of base', 'p(payout) < 1'),
                                              ('equity', 'RSUs', 'vesting cliff risk'), ('benefits', '$/YR', 'health, 401k match'),
                                              ('total EV', 'FORMULA', 'base + E[bonus] + E[equity] + benefits')]},
      'Comparing offers on base salary alone misprices risk: bonuses are probabilistic and equity vests over cliffs. '
      'Reduce each component to expected annual value before comparing.',
      'Table: decomposing total compensation into expected value', ['compensation', 'total']),
    S('compare',
      {'lt': 'Mean salary', 'li': ['Dragged up by executives', 'What "average pay" usually quotes', 'Misleads negotiations'],
       'rt': 'Median salary', 'ri': ['The 50th-percentile earner', 'Typical offer benchmark', 'Negotiate against this']},
      'Salary data is right-skewed: a few very high earners pull the mean above what most people make. '
      'Benchmark yourself against the median and the 25th/75th percentiles, never the mean.',
      'Comparison: mean vs median in salary data', ['mean', 'median', 'salary']),
    S('concept',
      {'title': 'Break-even analysis', 'lines': ['Break-even: revenue = fixed + variable costs', 'Units = fixed ÷ (price − unit cost)',
                                                  'Bootcamp ROI: cost ÷ monthly raise = months', 'If payback > 24 mo, think hard'],
       'accent': ORANGE},
      'Break-even analysis finds the point where an investment pays for itself. '
      'Apply it to bootcamps, certifications, and relocations: divide the cost by the monthly gain to get the payback horizon.',
      'Concept box: break-even math for career investments', ['break-even', 'innumeracy']),
]

# ================= IL-07 KITS =================

KITS['il07-mongodb'] = [
    S('compare',
      {'lt': 'Embed', 'li': ['One read gets everything', 'Best for 1:few, bounded', '16 MB document limit'],
       'rt': 'Reference', 'ri': ['Join via $lookup', 'Best for 1:many, unbounded', 'Avoids giant documents'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'Embed when the query pattern reads the whole aggregate together; reference when the related set is unbounded or shared. '
      'The decision is driven by reads, not by how the data "looks" conceptually.',
      'Animated comparison: embedding vs referencing documents in MongoDB', ['embed', 'reference', 'concepts']),
    S('flow',
      {'steps': [('$match', 'filter early'), ('$group', 'aggregate'), ('$project', 'reshape'), ('$lookup', 'join'), ('$out', 'persist')]},
      'Aggregation pipelines are staged transformations: filter first to shrink the working set, then group, reshape, join, and persist. '
      'Putting $match first is the single highest-leverage optimization because every later stage does less work.',
      'Animated flow of a MongoDB aggregation pipeline', ['aggregation', 'pipeline', 'hands-on']),
    S('table',
      {'name': 'index strategy', 'cols': [('single field', 'USE', 'equality on one field'),
                                          ('compound', 'USE', 'filter + sort patterns'), ('multikey', 'USE', 'array fields'),
                                          ('text', 'USE', 'full-text search'), ('_id', 'FREE', 'always indexed')]},
      'Index the query pattern, not the schema: each index should serve a real filter or sort the application performs. '
      'Compound indexes follow the ESR rule — equality, then sort, then range — and unused indexes only tax writes.',
      'Table of MongoDB index types and when to use them', ['index', 'query plan', 'hands-on']),
    S('concept',
      {'title': 'Transactions in PyMongo', 'lines': ['with client.start_session() as s:', 'with s.start_transaction():',
                                                      'All ops share the session', 'Abort on any failure → atomic'],
       'accent': PURPLE},
      'Multi-document transactions wrap related writes in a session so they commit or abort together. '
      'Use them for the few operations that truly need atomicity — most document designs avoid them by embedding.',
      'Concept box: ACID transactions with PyMongo', ['transaction', 'pymongo', 'pitfalls']),
]

KITS['il07-data-schools'] = [
    S('layers',
      {'layers': [('Serving: BI / ML / APIs', 'clean, modeled, governed — gold'),
                  ('Transform: dbt / Spark', 'cleanse, conform, aggregate — silver'),
                  ('Ingest: raw landing', 'immutable, append-only — bronze')]},
      'The medallion architecture refines data through bronze (raw), silver (cleaned), and gold (modeled) layers. '
      'Each layer is reproducible from the one below, so a bug in gold never destroys the raw evidence.',
      'Animated layered diagram of the medallion lakehouse architecture', ['medallion', 'lakehouse', 'concepts']),
    S('compare',
      {'lt': 'Batch', 'li': ['Hourly/daily windows', 'Complete, re-runnable', 'Lower cost per byte'],
       'rt': 'Streaming', 'ri': ['Sub-second latency', 'Exactly-once is hard', 'Higher operational cost'],
       'left_accent': ACCENT, 'right_accent': CYAN},
      'Batch optimizes for completeness and cost; streaming optimizes for freshness at the price of exactly-once complexity. '
      'Choose by the decision latency the business actually needs — most "real-time" requests are really "hourly".',
      'Animated comparison of batch vs streaming processing', ['batch', 'streaming', 'concepts']),
    S('flow',
      {'steps': [('Partition', 'split by key'), ('Shuffle', 'network move'), ('Aggregate', 'per partition'), ('Coalesce', 'final result')]},
      'Distributed engines partition data by key, shuffle rows across the network to co-locate them, then aggregate locally. '
      'The shuffle is the expensive step — skew in the partition key turns one straggler into the whole job\'s latency.',
      'Animated flow of distributed partitioning and shuffle', ['partition', 'shuffle', 'distributed']),
    S('concept',
      {'title': 'Reading a query plan', 'lines': ['Seq Scan → full table read', 'Index Scan → seeks via index',
                                                   'Nested Loop → small × large join', 'Cost = planner estimate, not ms'],
       'accent': ORANGE},
      'EXPLAIN shows the planner\'s chosen operators: sequential scans, index seeks, and join strategies with estimated costs. '
      'Costs are relative units for comparing plans, not milliseconds — compare plans to each other, not to a clock.',
      'Concept box: how to read a database query plan', ['query plan', 'index', 'hands-on']),
]

KITS['il07-ai-ml'] = [
    S('compare',
      {'lt': 'High bias (underfit)', 'li': ['Train AND validation error high', 'Model too simple', 'Fix: more capacity/features'],
       'rt': 'High variance (overfit)', 'ri': ['Train low, validation high', 'Model memorizes noise', 'Fix: regularization, more data'],
       'left_accent': ORANGE, 'right_accent': RED},
      'Bias/variance diagnosis starts from the train–validation gap: both bad means underfit, train-good/val-bad means overfit. '
      'The worked example\'s 2% train / 25% validation error is textbook high variance — regularize or add data.',
      'Animated bias-variance diagnosis comparison', ['bias', 'variance', 'worked example']),
    S('flow',
      {'steps': [('Forward pass', 'compute ŷ'), ('Loss', 'compare to y'), ('Backward pass', 'chain rule ∂L/∂w'), ('Update', 'w − η∇w')]},
      'Backpropagation applies the chain rule layer by layer to get every weight\'s contribution to the error. '
      'Gradient descent then steps each weight against its gradient — the entire deep-learning training loop in four stages.',
      'Animated flow of forward pass, loss, backprop, and weight update', ['backprop', 'concepts']),
    S('layers',
      {'layers': [('Output: task head', 'classification / generation logits'),
                  ('Stacked transformer blocks', 'attention + MLP, repeated N×'),
                  ('Embeddings + positions', 'tokens → vectors + order')]},
      'A transformer stacks identical blocks of self-attention and feed-forward layers on top of token embeddings. '
      'Attention lets every position draw on every other position, which is why long-range dependencies stopped being a wall.',
      'Animated layered diagram of transformer architecture', ['transformer', 'concepts']),
    S('flow',
      {'steps': [('State s', 'observe'), ('Action a', 'π(a|s) policy'), ('Reward r', 'environment'), ('Update π', 'policy gradient')]},
      'Reinforcement learning frames control as a Markov decision process: the agent observes state, acts by policy, and receives reward. '
      'Policy-gradient methods nudge the policy toward actions that historically returned more reward.',
      'Animated flow of the reinforcement learning loop', ['reinforcement', 'mdp', 'concepts']),
]

KITS['il07-neuroai'] = [
    S('flow',
      {'steps': [('Input current', 'I(t) spikes in'), ('Integrate', 'membrane V rises'), ('Threshold', 'V ≥ Vth?'), ('Fire + reset', 'spike out, V ← Vrest')]},
      'The leaky integrate-and-fire neuron accumulates incoming current on its membrane potential until it crosses threshold, fires, and resets. '
      'The leak term makes timing matter — coincident inputs sum, scattered ones decay away.',
      'Animated flow of leaky integrate-and-fire neuron dynamics', ['lif', 'neuron', 'concepts']),
    S('concept',
      {'title': 'STDP: timing is plasticity', 'lines': ['Pre before post → strengthen (LTP)', 'Post before pre → weaken (LTD)',
                                                        'Δw falls off with |Δt|', 'Hebb, refined: causality matters'],
       'accent': GREEN},
      'Spike-timing-dependent plasticity strengthens a synapse when the presynaptic spike predicts the postsynaptic one, and weakens it otherwise. '
      'It is Hebb\'s "fire together, wire together" with causality: order decides the sign of the change.',
      'Concept box: STDP learning rule', ['stdp', 'hebbian', 'worked example']),
    S('compare',
      {'lt': 'Artificial neural nets', 'li': ['Continuous activations', 'Dense matrix multiplies', 'GPU-friendly, power-hungry'],
       'rt': 'Spiking neural nets', 'ri': ['Discrete spike events', 'Sparse, event-driven', 'Neuromorphic, ultra-low power'],
       'left_accent': ACCENT, 'right_accent': PURPLE},
      'ANNs communicate with continuous values every timestep; SNNs communicate with sparse spike events only when something happens. '
      'The honest disanalogy: backprop-through-spikes is still awkward, which is why SNNs lag on benchmarks despite the efficiency story.',
      'Animated comparison of ANNs and spiking neural networks', ['spiking', 'neuromorphic', 'honesty']),
    S('layers',
      {'layers': [('Application', 'event vision, always-on sensing'),
                  ('SNN model', 'sparse spike computation'),
                  ('Neuromorphic chip', 'e.g. Loihi — cores = neurons'),
                  ('Physics', 'memristors, analog dynamics')]},
      'Neuromorphic hardware maps neurons to physical cores and synapses to memory, so computation happens where the data lives. '
      'No von Neumann round-trips means idle power near zero — ideal for always-on edge sensing.',
      'Animated layered diagram of the neuromorphic computing stack', ['neuromorphic', 'concepts']),
]

KITS['il07-openweight'] = [
    S('compare',
      {'lt': 'Open-weight', 'li': ['Weights published', 'Run/modify locally', 'License may restrict use'],
       'rt': 'Open-source (OSI)', 'ri': ['Full OSI freedoms', 'Weights + training code', 'No field-of-use limits'],
       'left_accent': GREEN, 'right_accent': ACCENT},
      '"Open-weight" means the parameters are downloadable — it says nothing about the license. '
      'Only OSI-approved licenses grant true open-source freedoms; many "open" models ban commercial use or redistribution.',
      'Animated comparison of open-weight vs open-source licensing', ['license', 'worked example', 'concepts']),
    S('layers',
      {'layers': [('Q8_0: near-lossless', '~1 byte/param, server grade'),
                  ('Q4_K_M: the sweet spot', '~0.5 byte/param, small quality cost'),
                  ('Q2_K: extreme', '~0.3 byte/param, visible degradation'),
                  ('Full FP16: reference', '2 bytes/param, baseline quality')]},
      'Quantization shrinks weights from 16-bit floats down a ladder of ever-coarser formats. '
      'Q4_K_M is the usual sweet spot — roughly 4× smaller than FP16 with quality loss most users never notice.',
      'Animated layered diagram of the quantization quality ladder', ['quantization', 'gguf', 'concepts']),
    S('compare',
      {'lt': 'llama.cpp / Ollama', 'li': ['CPU-friendly, single machine', 'Simplest local serving', 'Lower throughput'],
       'rt': 'vLLM', 'ri': ['GPU server, high throughput', 'PagedAttention batching', 'Production inference'],
       'left_accent': CYAN, 'right_accent': ACCENT},
      'Pick the server by the job: llama.cpp/Ollama for a laptop or single workstation, vLLM when a GPU server must serve many concurrent requests. '
      'vLLM\'s PagedAttention is the throughput trick — it batches requests the way an OS pages memory.',
      'Animated comparison of local model serving stacks', ['ollama', 'vllm', 'serving', 'hands-on']),
    S('table',
      {'name': 'honest benchmark', 'cols': [('tokens/sec', 'METRIC', 'throughput at your batch size'),
                                            ('TTFT', 'METRIC', 'time to first token'), ('quality', 'METRIC', 'task evals, not vibes'),
                                            ('$/1k tokens', 'METRIC', 'hardware amortized')]},
      'Benchmark on your hardware, your prompts, your batch size: tokens/sec, time-to-first-token, task-graded quality, and amortized cost. '
      'Vendor-published numbers are measured under ideal conditions and rarely transfer.',
      'Table of the four honest LLM benchmark dimensions', ['benchmark', 'honesty', 'pitfalls']),
]

KITS['il07-agents'] = [
    S('flow',
      {'steps': [('Reason', 'thought'), ('Act', 'tool call'), ('Observe', 'tool result'), ('Repeat', 'until done')]},
      'The ReAct loop interleaves reasoning traces with tool actions: think, act, observe the result, repeat. '
      'Writing it by hand once teaches the failure mode no framework hides — an agent that loops forever on a failing tool.',
      'Animated flow of the ReAct agent loop', ['react', 'concepts']),
    S('layers',
      {'layers': [('Application', 'support bot, research agent'),
                  ('LangGraph graph', 'nodes, edges, conditional routing'),
                  ('State + checkpointer', 'durable, resumable, inspectable'),
                  ('Model + tools', 'LLM calls and tool executors')]},
      'LangGraph models agents as graphs whose nodes share a checkpointed state object. '
      'Durable state is the point: a crashed or paused run resumes exactly where it stopped instead of restarting.',
      'Animated layered diagram of the LangGraph architecture', ['langgraph', 'concepts']),
    S('flow',
      {'steps': [('Host', 'Claude, IDE'), ('MCP client', 'protocol speaks'), ('MCP server', 'exposes tools'), ('Data source', 'files, DBs, APIs')]},
      'The Model Context Protocol standardizes how a host app discovers and calls external tools: servers expose capabilities, clients consume them. '
      'One protocol replaces N bespoke integrations — the "USB-C for AI tools" framing is nearly literal.',
      'Animated flow of MCP host-client-server architecture', ['mcp', 'concepts']),
    S('concept',
      {'title': 'Evaluating agents', 'lines': ['Rubrics > vibes: grade each step', 'Trajectory: the full action trace',
                                                'Success rate + cost per task', 'Red-team the tool loop deliberately'],
       'accent': ORANGE},
      'Grade the trajectory, not just the final answer: did the agent take sensible steps at reasonable cost? '
      'Rubric-scored trajectories plus adversarial tool-loop tests catch the infinite-retry and prompt-injection failures.',
      'Concept box: agent evaluation with rubrics and trajectories', ['evaluate', 'rubric', 'pitfalls']),
]

KITS['il07-frontier'] = [
    S('concept',
      {'title': 'Scaled dot-product attention', 'lines': ['Attention(Q,K,V) = softmax(QKᵀ/√dₖ)V', 'QKᵀ grows with dimension dₖ',
                                                          '÷√dₖ keeps softmax out of saturation', 'Without it: gradients vanish'],
       'accent': ACCENT},
      'Attention scores grow with the key dimension, pushing softmax into flat saturated regions where gradients die. '
      'Dividing by √dₖ is the one-line fix that keeps the distribution soft and the gradients alive.',
      'Concept box: why attention is scaled by root-d-k', ['attention', 'softmax', 'worked example']),
    S('compare',
      {'lt': 'RLHF', 'li': ['Train reward model on preferences', 'PPO optimizes against it', 'Complex, reward hacking risk'],
       'rt': 'DPO', 'ri': ['Direct preference loss, no RM', 'Simpler, more stable', 'Weaker on hard exploration'],
       'left_accent': PURPLE, 'right_accent': GREEN},
      'RLHF learns a reward model from human preferences then optimizes it with PPO; DPO skips the middleman with a direct preference loss. '
      'DPO is simpler and stabler, RLHF stays stronger where exploration matters — pick by the problem, not the hype.',
      'Animated comparison of RLHF vs DPO alignment recipes', ['rlhf', 'dpo', 'concepts']),
    S('concept',
      {'title': 'Scaling laws — and limits', 'lines': ['Loss falls as a power law in compute/data/params', 'Chinchilla: balance params and tokens',
                                                        'Returns diminish; data quality binds', 'Inference cost scales with use'],
       'accent': ORANGE},
      'Bigger models on more data reliably lower loss along a power law — until data quality, not quantity, becomes the binding constraint. '
      'Chinchilla showed most models were undertrained: match parameters to tokens instead of just scaling parameters.',
      'Concept box: neural scaling laws and their limits', ['scaling', 'concepts']),
    S('flow',
      {'steps': [('Specification', 'what we asked'), ('Optimization', 'what it learned'), ('Generalization', 'new situations'), ('Misalignment', 'reward hacking')]},
      'The alignment problem: an optimizer pursues the specified reward, not the intended goal. '
      'Specification gaming — finding loopholes in the reward — is the default outcome, not an edge case, as capability rises.',
      'Animated flow of how misalignment emerges', ['alignment', 'concepts']),
]

KITS['il07-aws-data'] = [
    S('flow',
      {'steps': [('Kinesis/MSK', 'stream ingest'), ('DMS', 'CDC from DBs'), ('S3 landing', 'raw, immutable'), ('Glue/EMR', 'transform')]},
      'Choose ingest by pattern: Kinesis or MSK for event streams, DMS change-data-capture for database replication. '
      'Land everything raw and immutable in S3 first — reprocessing from raw is the recovery strategy for every downstream bug.',
      'Animated flow of AWS data ingestion patterns', ['kinesis', 'ingest', 'worked example']),
    S('layers',
      {'layers': [('Consumption: Athena / Redshift', 'query the curated zone'),
                  ('Curated: partitioned Parquet', 'clean, typed, partitioned'),
                  ('Raw: S3 landing zone', 'immutable source of truth'),
                  ('Sources: apps, DBs, streams', 'producers')]},
      'A lakehouse layers S3 storage by refinement: raw landing, curated Parquet, then query engines on top. '
      'Partition by the columns you filter on — date, region — because partition pruning is what makes S3 scans cheap.',
      'Animated layered diagram of the S3 lakehouse layout', ['lakehouse', 's3', 'concepts']),
    S('compare',
      {'lt': 'Glue (serverless Spark)', 'li': ['No clusters to manage', 'Pay per DPU-second', 'Best for ETL jobs'],
       'rt': 'EMR (managed clusters)', 'ri': ['Full Spark/Hadoop control', 'Long-running / iterative', 'Tune instance fleets'],
       'left_accent': ACCENT, 'right_accent': ORANGE},
      'Glue wins for managed serverless ETL; EMR wins when you need cluster-level control for iterative or long-running Spark. '
      'Both read and write the same S3 lakehouse — the choice is operational, not architectural.',
      'Animated comparison of Glue vs EMR for transformation', ['glue', 'emr', 'concepts']),
    S('concept',
      {'title': 'Secure the pipeline', 'lines': ['Lake Formation: table/column grants', 'KMS: encrypt at rest, per-bucket keys',
                                                  'IAM: least-privilege job roles', 'CloudTrail + CloudWatch: audit everything'],
       'accent': RED},
      'Data pipelines are high-value targets: they touch every record. '
      'Layer Lake Formation fine-grained grants over KMS encryption and least-privilege IAM roles, and audit with CloudTrail.',
      'Concept box: securing AWS data pipelines', ['lake formation', 'security', 'pitfalls']),
]

KITS['il07-aws-ml'] = [
    S('flow',
      {'steps': [('Feature Store', 'curated features'), ('Ground Truth', 'labeled data'), ('Training job', 'SageMaker'), ('Registry', 'versioned model')]},
      'SageMaker ML starts with data prep — Feature Store for reusable features, Ground Truth for human labeling — then training jobs and a model registry. '
      'The registry is the contract between training and deployment: versioned, approved, auditable.',
      'Animated flow of the SageMaker training pipeline', ['sagemaker', 'feature store', 'concepts']),
    S('compare',
      {'lt': 'Real-time endpoint', 'li': ['ms latency, always on', 'Pay per instance-hour', 'Fraud, recommendations'],
       'rt': 'Batch transform', 'ri': ['No endpoint to manage', 'Pay per job', 'Nightly scoring, ETL enrichment'],
       'left_accent': CYAN, 'right_accent': ACCENT},
      'Real-time endpoints serve millisecond predictions at always-on cost; batch transform scores bulk data with no endpoint to babysit. '
      'Match the pattern to the decision latency — most scoring jobs are batch jobs wearing a real-time costume.',
      'Animated comparison of SageMaker deployment patterns', ['endpoint', 'batch', 'deploy', 'concepts']),
    S('layers',
      {'layers': [('Monitor: Model Monitor', 'drift, bias, quality alarms'),
                  ('Deploy: endpoints / pipelines', 'CI/CD promotion gates'),
                  ('Train: experiments, tuning', 'automatic model tuning'),
                  ('Data: versioned datasets', 'lineage from raw to features')]},
      'MLOps closes the loop: versioned data feeds tuned training, promotion gates guard deployment, and Model Monitor watches for drift. '
      'Drift alarms — not calendars — should trigger retraining.',
      'Animated layered diagram of the SageMaker MLOps loop', ['mlops', 'drift', 'concepts']),
    S('concept',
      {'title': 'Training/serving skew', 'lines': ['Features computed differently in prod', 'Label leakage in training only',
                                                    'Monitor: compare feature distributions', 'Fix: one feature pipeline, both paths'],
       'accent': RED},
      'Training/serving skew means the model sees different feature distributions in production than it trained on. '
      'The fix is architectural: a single feature pipeline (Feature Store) serving both training and inference.',
      'Concept box: diagnosing and fixing training-serving skew', ['skew', 'worked example', 'pitfalls']),
]

# ================= IL-08 KITS =================

KITS['il08-mit'] = [
    S('compare',
      {'lt': 'Induction', 'li': ['Base + step chain', 'Best for: closed forms, recurrences', 'Example: Σ odds = n²'],
       'rt': 'Contradiction / invariant', 'ri': ['Assume ¬P, derive absurdity', 'Best for: impossibility, loop correctness'],
       'left_accent': ACCENT, 'right_accent': PURPLE},
      'Pick the proof tool by the claim\'s shape: induction for statements indexed by n, contradiction for impossibility claims, '
      'invariants for "this loop maintains X". The worked example\'s Σ-of-odds identity is induction\'s home turf.',
      'Animated comparison of proof methods', ['proof', 'induction', 'worked example']),
    S('concept',
      {'title': 'Amortized analysis', 'lines': ['Worst case per op can mislead', 'Average over a sequence of ops',
                                                'Dynamic array push: O(1) amortized', 'Banker/physicist: pay it forward'],
       'accent': GREEN},
      'Amortized analysis averages cost over a sequence: a dynamic array\'s occasional O(n) resize is "paid for" by the many O(1) pushes before it. '
      'Per-operation worst case would call push O(n) — true once, misleading always.',
      'Concept box: amortized analysis', ['amortized', 'concepts']),
    S('layers',
      {'layers': [('Software: algorithms, languages', 'what you write'),
                  ('ISA: the contract', 'instructions, registers, memory model'),
                  ('Microarchitecture', 'pipelines, caches, branch prediction'),
                  ('Physics: transistors', 'what actually switches')]},
      'The ISA is the hardware/software contract: everything above it is portable, everything below is implementation. '
      'Caches and pipelines live below the contract — invisible until performance forces you to look.',
      'Animated layered diagram of the hardware/software stack', ['isa', 'cache', 'concepts']),
    S('flow',
      {'steps': [('Problem in NP', 'verify fast'), ('Pick known NPC', 'e.g. 3-SAT'), ('Poly reduction', 'A ≤p B'), ('B is NP-complete', 'QED')]},
      'To prove NP-completeness, reduce a known NP-complete problem to yours in polynomial time. '
      'The reduction\'s direction is the classic trap: known-hard → your problem shows your problem is at least as hard.',
      'Animated flow of an NP-completeness reduction proof', ['np-complete', 'reduction', 'concepts']),
]

KITS['il08-cmu'] = [
    S('concept',
      {'title': 'malloc: the heap contract', 'lines': ['malloc(n): ≥ n bytes, aligned', 'free(p): exactly what malloc returned',
                                                        'Use-after-free: dangling pointer', 'Double free: heap corruption'],
       'accent': ORANGE},
      'malloc and free form a strict contract: free exactly the pointer malloc returned, exactly once. '
      'Violations — use-after-free, double-free — corrupt the heap silently and surface far from the bug.',
      'Concept box: the malloc/free contract', ['malloc', 'concepts']),
    S('flow',
      {'steps': [('Virtual address', 'program view'), ('TLB lookup', 'cached translation'), ('Page table walk', 'on miss'), ('Physical frame', 'DRAM')]},
      'Virtual memory translates every address through page tables, with the TLB caching hot translations. '
      'A TLB miss triggers a page-table walk — the hidden tax behind "random access is slow".',
      'Animated flow of virtual address translation', ['vm', 'tlb', 'concepts']),
    S('compare',
      {'lt': 'Contracts & invariants', 'li': ['Pre/postconditions on functions', 'Loop invariants for correctness', 'Prove code right'],
       'rt': 'Testing only', 'ri': ['Samples the input space', 'Finds bugs, proves nothing', 'Complement, not substitute'],
       'left_accent': GREEN, 'right_accent': ORANGE},
      'Contracts state what code promises; invariants state what loops preserve — together they make correctness arguable. '
      'Testing samples behavior; contracts specify it. CMU\'s spine teaches both because each catches what the other misses.',
      'Animated comparison: contracts vs testing for correctness', ['contracts', 'invariants', 'concepts']),
    S('concept',
      {'title': 'Work vs span', 'lines': ['Work T₁: total operations', 'Span T∞: longest dependency chain',
                                           'Parallelism = T₁ / T∞', 'Brent: Tp ≤ T₁/p + T∞'],
       'accent': CYAN},
      'Work is the total operation count; span is the critical path no parallelization can shorten. '
      'Their ratio bounds achievable speedup — the worked example\'s parallel sum has Θ(n) work but Θ(log n) span.',
      'Concept box: work-span analysis of parallel algorithms', ['work', 'span', 'worked example']),
]

KITS['il08-stanford'] = [
    S('flow',
      {'steps': [('Base case', 'smallest input'), ('Recursive call', 'smaller subproblem'), ('Combine', 'build answer'), ('Trust the recursion', 'leap of faith')]},
      'Recursive thinking: solve the smallest case directly, then assume the recursive call solves the smaller one and focus only on combining. '
      'The "leap of faith" — trusting the recursion — is the skill; tracing every call is the trap.',
      'Animated flow of recursive problem decomposition', ['recursion', 'concepts']),
    S('concept',
      {'title': 'Randomized quicksort', 'lines': ['Random pivot → no adversarial input', 'Expected: Θ(n log n)',
                                                   'Worst case still Θ(n²), unlikely', 'Randomness defeats the adversary'],
       'accent': GREEN},
      'Choosing the pivot at random removes the adversary: no input order can force worst-case behavior every time. '
      'Expected Θ(n log n) with a worst case that requires spectacularly bad luck — randomness as an engineering tool.',
      'Concept box: randomized quicksort analysis', ['quicksort', 'worked example', 'concepts']),
    S('layers',
      {'layers': [('C program', 'your code'),
                  ('Assembly', 'what the compiler emitted'),
                  ('Machine code', 'bytes the CPU fetches'),
                  ('Bits: registers, flags', 'the actual machine state')]},
      'CS107\'s descent — C to assembly to bits — teaches that every abstraction leaks under pressure. '
      'Reading the compiler\'s assembly output turns "the optimizer did something" into something you can verify.',
      'Animated layered diagram from C down to bits', ['assembly', 'bits', 'concepts']),
    S('flow',
      {'steps': [('Model as graph', 'vertices, edges'), ('Random process', 'Markov / random walk'), ('Analyze', 'expectation, concentration'), ('Bound it', 'Chernoff, union bound')]},
      'Stanford\'s 103/109 spine turns fuzzy problems into graphs plus probability, then bounds the answer with concentration inequalities. '
      'Model first, randomize deliberately, then prove the bound — the three-move sequence behind most randomized analysis.',
      'Animated flow of graph-plus-probability analysis', ['graphs', 'probability', 'concepts']),
]

# ================= IL-09 KITS =================

KITS['il09-core'] = [
    S('table',
      {'name': 'A+ Core 1 domains (220-1201)', 'cols': [('Mobile Devices', '15%', 'laptops, phones'),
                                                        ('Networking', '20%', 'TCP/IP, Wi-Fi, SOHO'),
                                                        ('Hardware', '25%', 'heaviest domain'),
                                                        ('Virtualization/Cloud', '11%', 'concepts'),
                                                        ('Troubleshooting', '29%', 'methodology applied')]},
      'Study by weight: troubleshooting and hardware dominate Core 1, so drill the six-step methodology against hardware scenarios first. '
      'Domain weights tell you where each study hour pays most.',
      'Table of A+ Core 1 exam domain weights', ['a+', 'domains', 'worked example']),
    S('flow',
      {'steps': [('Identify', 'gather info'), ('Theory', 'probable cause'), ('Test', 'verify theory'), ('Plan + fix', 'act'), ('Verify', 'full function'), ('Document', 'lessons learned')]},
      'CompTIA\'s six-step troubleshooting methodology is the PBQ grading rubric in disguise. '
      'Every performance-based question rewards the same sequence: never skip establishing a theory before acting.',
      'Animated flow of the six-step troubleshooting methodology', ['troubleshooting', 'hands-on']),
    S('concept',
      {'title': 'Subnet fluency: /24 in your head', 'lines': ['/24 → mask 255.255.255.0', 'Hosts: 2⁸ − 2 = 254',
                                                               'Network: IP with last octet 0', 'VLSM: carve with /25, /26…'],
       'accent': GREEN},
      'Exam subnetting is /24 arithmetic at speed plus VLSM carving on paper. '
      'Memorize the 2ⁿ − 2 table through /30 and practice until the host count is reflex, not computation.',
      'Concept box: subnetting fluency for Network+', ['subnetting', 'hands-on']),
    S('layers',
      {'layers': [('Security+ : architecture & operations', 'heaviest: threats, architecture, ops'),
                  ('Network+ : infrastructure', 'the pipes and protocols'),
                  ('A+ : endpoints & support', 'the devices and users')]},
      'The core stack layers: A+ proves you can fix endpoints, Network+ proves you understand the pipes, Security+ proves you can defend both. '
      'Each assumes the one below — Security+ scenarios punish shaky networking fundamentals.',
      'Animated layered diagram of the CompTIA core stack', ['security+', 'network+', 'concepts']),
]

KITS['il09-security'] = [
    S('flow',
      {'steps': [('Scope', 'rules of engagement'), ('Recon', 'passive → active'), ('Exploit', 'gaining access'), ('Report', 'findings + remediation')]},
      'A PenTest+ engagement runs scope → recon → exploitation → reporting, with written authorization gating every active step. '
      'The report is the deliverable that matters: findings ranked by risk with concrete remediation.',
      'Animated flow of a penetration test engagement', ['pentest', 'concepts']),
    S('concept',
      {'title': 'CVSS: score the finding, not the fear', 'lines': ['Base: exploitability + impact', 'Temporal: exploit code maturity',
                                                                    'Environmental: your exposure', 'Lab VM ≠ internet-facing: score differs'],
       'accent': ORANGE},
      'CVSS separates the vulnerability\'s intrinsic severity (base) from your exposure to it (environmental). '
      'The worked example\'s trap: a critical on an isolated lab VM outranks nothing — environmental score decides priority.',
      'Concept box: CVSS scoring done right', ['cvss', 'worked example', 'pitfalls']),
    S('layers',
      {'layers': [('SecurityX: architecture & GRC', 'design under constraints'),
                  ('PenTest+: offensive validation', 'prove the holes'),
                  ('CySA+: defensive operations', 'detect and respond'),
                  ('Security+: foundations', 'the vocabulary')]},
      'The security track climbs from vocabulary (Security+) through defense (CySA+) and offense (PenTest+) to architecture (SecurityX). '
      'Earn the stackables in order — CSAP then CNVP — because each exam assumes the previous tier\'s fluency.',
      'Animated layered diagram of the CompTIA security track', ['cysa', 'pentest', 'securityx', 'concepts']),
    S('flow',
      {'steps': [('Triage alert', 'SIEM queue'), ('Enrich', 'threat intel, logs'), ('Contain', 'isolate host'), ('Eradicate + recover', 'close out')]},
      'CySA+ lives in the SOC workflow: triage the alert, enrich with intel and logs, contain the host, then eradicate and recover. '
      'Speed matters at triage; thoroughness matters at eradication — know which phase you\'re in.',
      'Animated flow of SOC incident response', ['soc', 'incident', 'concepts']),
]

KITS['il09-data-cloud'] = [
    S('compare',
      {'lt': 'IaaS', 'li': ['You manage OS → app', 'Example: EC2 VMs', 'Most control, most work'],
       'rt': 'PaaS / SaaS', 'ri': ['Provider manages platform/app', 'Example: RDS / Gmail', 'Least control, least work'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'The cloud shared-responsibility line slides with the service model — under IaaS you patch the guest OS; under SaaS you don\'t. '
      'The worked example\'s answer follows the line: whoever owns the layer owns the patching.',
      'Animated shared-responsibility comparison across service models', ['iaas', 'paas', 'saas', 'worked example']),
    S('flow',
      {'steps': [('Concepts', 'terminology'), ('Acquire', 'ingest sources'), ('Store', 'model + persist'), ('Analyze', 'query, BI'), ('Govern', 'quality, lineage')]},
      'The Data+/DataSys+ lifecycle runs concepts → acquisition → storage → analysis → governance. '
      'Exam questions love the handoffs: garbage acquisition poisons analysis no matter how good the modeling.',
      'Animated flow of the data lifecycle', ['data lifecycle', 'concepts']),
    S('concept',
      {'title': 'Linux+ fluency checklist', 'lines': ['systemd: services, targets, journals', 'Users/groups/permissions: the triad',
                                                      'Storage: LVM, mounting, fstab', 'Security: firewalld, SELinux basics'],
       'accent': CYAN},
      'Linux+ tests system management as practiced: systemd for services, the user/group/permission triad for access, LVM for storage. '
      'Drill the commands until the flags are muscle memory — the exam punishes hesitation, not ignorance.',
      'Concept box: Linux+ system-management fluency', ['linux+', 'hands-on']),
    S('table',
      {'name': 'Server+ DR math', 'cols': [('RTO', 'TARGET', 'how fast to restore'), ('RPO', 'TARGET', 'how much data to lose'),
                                            ('backup window', 'CONSTRAINT', 'fits in off-hours'), ('3-2-1 rule', 'STRATEGY', '3 copies, 2 media, 1 offsite')]},
      'Disaster recovery is two numbers: RTO (how fast) and RPO (how much loss). '
      'Every backup strategy — including the 3-2-1 rule — is judged by whether it meets those two targets within the backup window.',
      'Table of disaster-recovery objectives and strategy', ['rto', 'rpo', 'server+', 'concepts']),
]

KITS['il09-vendor-ai'] = [
    S('layers',
      {'layers': [('Azure AI Engineer Associate', 'build AI apps & agents on Azure'),
                  ('Azure AI Fundamentals (AI-900)', 'concepts, services, responsible AI'),
                  ('Vendor-neutral base', 'CompTIA, cloud fundamentals')]},
      'The Azure AI path climbs from AI-900 fundamentals to the AI Engineer Associate\'s applied agent-building. '
      'Fundamentals first: the associate exam assumes you already speak the service catalog fluently.',
      'Animated layered diagram of the Azure AI certification path', ['azure', 'ai-900', 'concepts']),
    S('flow',
      {'steps': [('AI Practitioner', 'concepts + use cases'), ('ML Engineer Associate', 'SageMaker, pipelines'), ('Specialty (retired track)', 'legacy depth')]},
      'AWS\'s AI path runs from the Practitioner\'s conceptual fluency to the ML Engineer Associate\'s hands-on SageMaker depth. '
      'The associate is the hiring signal; the practitioner is the on-ramp.',
      'Animated flow of the AWS AI certification path', ['aws', 'sagemaker', 'concepts']),
    S('compare',
      {'lt': 'Proctored exam', 'li': ['Identity-verified, timed', 'Strongest hiring signal', 'Example: AI-900, Associate'],
       'rt': 'Badge / course complete', 'ri': ['Self-paced, unverified', 'Weakest signal alone', 'Good as preparation'],
       'left_accent': GREEN, 'right_accent': ORANGE},
      'Tier credentials by verification: proctored exams carry the hiring signal, badges carry preparation value. '
      'The worked example\'s answer is the proctored associate-level exam — verified skill beats completed videos.',
      'Animated comparison of credential tiers', ['credentials', 'worked example', 'pitfalls']),
    S('concept',
      {'title': 'Cover the field', 'lines': ['Google Cloud: Vertex AI, ML Engineer cert', 'NVIDIA: DLI workshops + certs',
                                              'Databricks: Lakehouse AI workloads', 'Map each to a job family'],
       'accent': PURPLE},
      'Beyond the big two: Google Cloud\'s Vertex AI path, NVIDIA\'s DLI technical depth, and Databricks\' lakehouse AI. '
      'Collect at most one per ecosystem — breadth signals tourism, depth signals employability.',
      'Concept box: Google, NVIDIA, and Databricks AI credentials', ['gcp', 'nvidia', 'databricks', 'concepts']),
]

KITS['il09-oracle'] = [
    S('concept',
      {'title': 'Java SE 21 exam core', 'lines': ['Streams: lazy, terminal ops trigger', 'Lambdas: functional interfaces',
                                                  'Modules: JPMS requires/exports', 'Concurrency: virtual threads (21)'],
       'accent': ACCENT},
      'The Java SE 21 exam centers on streams, lambdas, modules, and concurrency. '
      'The worked example\'s trap: intermediate stream ops are lazy — nothing executes until a terminal operation runs.',
      'Concept box: Java SE 21 exam topics', ['java', 'streams', 'worked example']),
    S('flow',
      {'steps': [('FROM + JOINs', 'shape rows'), ('WHERE', 'filter'), ('GROUP BY', 'aggregate'), ('HAVING + ORDER', 'refine, sort')]},
      'Oracle SQL fluency is the logical query order: FROM/JOIN shapes the rows, WHERE filters, GROUP BY aggregates, HAVING refines groups. '
      'Write in execution order mentally even though SELECT comes first syntactically.',
      'Animated flow of SQL logical query processing', ['sql', 'joins', 'concepts']),
    S('layers',
      {'layers': [('Professional: OCI Architect / Developer', 'design & build at depth'),
                  ('Associate: OCI Architect Associate', 'core services competence'),
                  ('Foundations Associate', 'concepts + console fluency')]},
      'OCI\'s year-versioned program stacks Foundations → Associate → Professional. '
      'Each tier assumes the console and service vocabulary of the one below — skipping tiers shows on exam day.',
      'Animated layered diagram of OCI certification tiers', ['oci', 'concepts']),
    S('concept',
      {'title': 'Oracle exam mechanics', 'lines': ['~50–60 questions, ~90 minutes', 'Partial credit on multi-select',
                                                    'No going back on some formats', 'Pace: ~90 seconds per question'],
       'accent': ORANGE},
      'Oracle exams reward pacing discipline: roughly 90 seconds per question with partial credit on multi-select. '
      'Flag-and-move beats perfectionism — an unanswered question scores zero with certainty.',
      'Concept box: Oracle exam timing and mechanics', ['exam', 'pitfalls']),
]

KITS['il09-blockchain'] = [
    S('layers',
      {'layers': [('Application / chaincode', 'smart contracts'),
                  ('Peers: endorse + commit', 'execute and validate'),
                  ('Orderers: sequence', 'total order of transactions'),
                  ('Channels: private subnets', 'data isolation')]},
      'Fabric separates execution (peers endorse chaincode), ordering (orderers sequence), and validation (peers commit). '
      'Channels then partition the ledger so competitors share infrastructure without sharing data.',
      'Animated layered diagram of Hyperledger Fabric architecture', ['fabric', 'peers', 'concepts']),
    S('flow',
      {'steps': [('Client proposes', 'to endorsers'), ('Endorsement', 'peers simulate'), ('Ordering', 'orderers sequence'), ('Commit', 'peers validate + write')]},
      'A Fabric transaction flows propose → endorse → order → commit, with endorsement policy deciding whose signatures suffice. '
      'The worked example\'s answer: orderers sequence transactions — they never execute chaincode.',
      'Animated flow of a Fabric transaction lifecycle', ['fabric', 'orderers', 'worked example']),
    S('compare',
      {'lt': 'Fabric (permissioned)', 'li': ['Known identities, channels', 'Pluggable consensus (Raft)', 'Enterprise privacy'],
       'rt': 'Besu (Ethereum-aligned)', 'ri': ['EVM smart contracts', 'QBFT/IBFT consensus options', 'Public or private nets'],
       'left_accent': ACCENT, 'right_accent': PURPLE},
      'Fabric is the permissioned enterprise ledger with channels; Besu is the Ethereum-compatible client for private or public networks. '
      'HFCP tests Fabric\'s architecture; BCP tests Besu\'s networking, permissioning, and consensus options.',
      'Animated comparison of Fabric vs Besu', ['besu', 'fabric', 'concepts']),
    S('concept',
      {'title': 'Exam logistics', 'lines': ['90 minutes, online proctored', 'HFCP: Fabric internals depth',
                                             'BCP: Besu ops depth', 'Retired perf exams ≠ live exams'],
       'accent': ORANGE},
      'Both live exams run 90 minutes online-proctored; know which one you\'re sitting — HFCP is Fabric architecture, BCP is Besu operations. '
      'Don\'t study retired performance-based exams; the live formats test conceptual and operational depth.',
      'Concept box: HFCP/BCP exam logistics', ['exam', 'pitfalls']),
]

KITS['il09-cpp-python'] = [
    S('layers',
      {'layers': [('CPP: Professional', 'template/STL depth'),
                  ('CPA: Associate', 'OOP, memory, exceptions'),
                  ('CPE: Entry', 'syntax, control flow, functions')]},
      'The C++ ladder climbs CPE → CPA → CPP: syntax first, then OOP and manual memory, then template and STL depth. '
      'Each rung\'s exam assumes the previous rung\'s fluency — there are no shortcuts around pointers.',
      'Animated layered diagram of the C++ certification ladder', ['c++', 'concepts']),
    S('layers',
      {'layers': [('PCPP: Professional', 'OOP depth, stdlib mastery'),
                  ('PCAP: Associate', 'modules, exceptions, OOP basics'),
                  ('PCEP: Entry', 'syntax, data types, flow control')]},
      'The Python ladder mirrors it: PCEP → PCAP → PCPP, from syntax through modules and exceptions to professional OOP and stdlib depth. '
      'OpenEDG\'s free aligned courses are the primary study backbone for every rung.',
      'Animated layered diagram of the Python certification ladder', ['python', 'concepts']),
    S('concept',
      {'title': 'The mutable-default trap', 'lines': ['def f(x=[]): — ONE list object', 'Created at def time, not call time',
                                                       'Appends persist across calls', 'Fix: def f(x=None): x = x or []'],
       'accent': RED},
      'The worked example\'s classic: a mutable default argument is created once at function definition and shared across calls. '
      'Exam tracing questions love it — always use None as the default and build the container inside.',
      'Concept box: Python mutable default arguments', ['worked example', 'pitfalls', 'python']),
    S('flow',
      {'steps': [('Read the code', 'slowly'), ('Track state', 'variables on paper'), ('Spot the idiom', 'defaults, closures, scoping'), ('Predict output', 'then verify')]},
      'Exam precision is a tracing discipline: read slowly, track variable state on paper, name the idiom under test, then predict. '
      'Most "tricky" questions test exactly one idiom — identify it and the answer is mechanical.',
      'Animated flow of code-tracing exam technique', ['tracing', 'hands-on', 'pitfalls']),
]

# ================= IL-10 KITS =================

KITS['il10-fde'] = [
    S('flow',
      {'steps': [('Embed', 'sit with users'), ('Discover', 'real workflow pain'), ('Prototype', 'working demo fast'), ('Land', 'production value')]},
      'Forward-deployed engineering embeds with the customer, discovers the real workflow pain, and prototypes against it in days. '
      'The worked example\'s first move is never the dashboard — it\'s watching how the customer works today.',
      'Animated flow of the forward-deployed engagement loop', ['fde', 'worked example', 'concepts']),
    S('compare',
      {'lt': 'Product engineer', 'li': ['Builds for many users', 'Roadmap-driven', 'Scales through software'],
       'rt': 'Forward-deployed engineer', 'ri': ['Builds with one customer', 'Problem-driven', 'Scales through playbooks'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'Product engineers build for the many via roadmaps; FDEs build with the one via embedded problem-solving. '
      'The FDE scales through playbooks and reusable components extracted from each deployment.',
      'Animated comparison: product vs forward-deployed engineering', ['fde', 'concepts']),
    S('concept',
      {'title': 'Discovery before dashboards', 'lines': ['Shadow the workflow end to end', 'Find the decision the data serves',
                                                         'Prototype the smallest useful thing', 'Earn the right to productionize'],
       'accent': CYAN},
      'Customers ask for dashboards when they need decisions. Shadow the workflow, find the decision, prototype the smallest thing that informs it. '
      'A demo that changes one meeting beats a platform nobody opens.',
      'Concept box: customer discovery discipline', ['discovery', 'hands-on', 'pitfalls']),
    S('layers',
      {'layers': [('Trust: reference customer', 'expansion and advocacy'),
                  ('Value: production outcome', 'metrics moved'),
                  ('Prototype: working demo', 'built in days'),
                  ('Access: embedded seat', 'sitting with users')]},
      'FDE engagements stack: embedded access enables fast prototypes, prototypes earn production trust, trust compounds into reference accounts. '
      'Skip a layer — prototype without access — and the demo solves the wrong problem.',
      'Animated layered diagram of FDE engagement stages', ['fde', 'concepts']),
]

KITS['il10-humanmetrics'] = [
    S('table',
      {'name': 'the four dichotomies', 'cols': [('E / I', 'ENERGY', 'outer vs inner world'), ('S / N', 'INFO', 'facts vs patterns'),
                                                 ('T / F', 'DECISIONS', 'logic vs values'), ('J / P', 'LIFESTYLE', 'planned vs flexible')]},
      'Humanmetrics sorts preferences along four dichotomies — energy, information, decisions, lifestyle. '
      'Each is a preference, not a skill: an INTP can sell, but sustained prospecting drains the preference battery.',
      'Table of the four MBTI dichotomies', ['mbti', 'typology', 'concepts']),
    S('concept',
      {'title': 'INTP × sales engineering', 'lines': ['Strength: deep technical credibility', 'Drain: relentless outbound prospecting',
                                                       'Fit: solutions architect > pure sales', 'Mitigation: inbound/demo-led motion'],
       'accent': PURPLE},
      'The worked example\'s verdict: INTP maps well to solutions architecture — technical depth with the customer — and poorly to pure outbound sales. '
      'Typology doesn\'t forbid the role; it prices the energy cost honestly.',
      'Concept box: INTP career-fit analysis', ['intp', 'worked example', 'concepts']),
    S('compare',
      {'lt': 'What typology gives', 'li': ['Energy-cost map of work', 'Communication preferences', 'Team role tendencies'],
       'rt': 'What it does NOT give', 'ri': ['Ability or ceiling', 'Hiring verdicts', 'Scientific prediction'],
       'left_accent': GREEN, 'right_accent': RED},
      'Use typology as an energy-cost map for self-knowledge, never as a hiring filter or ability ceiling. '
      'The honesty note\'s warning: test-retest reliability is modest — treat results as hypotheses about yourself.',
      'Animated comparison: proper vs improper uses of typology', ['honesty', 'pitfalls', 'concepts']),
    S('flow',
      {'steps': [('Assess', 'honest answers'), ('Reflect', 'resonance check'), ('Experiment', 'try the role shape'), ('Adjust', 'update the map')]},
      'Self-knowledge is iterative: take the assessment honestly, check which results resonate, experiment with the implied role shape, adjust. '
      'One assessment is a snapshot; the loop is the instrument.',
      'Animated flow of the self-knowledge loop', ['hands-on', 'concepts']),
]

KITS['il10-entrepreneur'] = [
    S('compare',
      {'lt': 'Fun, no payer', 'li': ['Users love it, nobody pays', 'Monetization "later"', 'Classic indie trap'],
       'rt': 'Boring, with budget', 'ri': ['Unsexy problem, real budget', 'Customer-funded from day one', 'Babson pick'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'The worked example\'s rule: pick the boring idea with a budget over the fun idea with no payer. '
      'Customer-funded beats investor-funded for first-time founders — revenue is the cheapest validation.',
      'Animated comparison of idea selection', ['worked example', 'ideas', 'concepts']),
    S('flow',
      {'steps': [('Problem interview', '20 conversations'), ('Concierge MVP', 'manual behind the curtain'), ('Paid pilot', 'money changes hands'), ('Scale', 'automate what worked')]},
      'The Babson-informed track: interview twenty prospects, deliver a concierge MVP manually, convert to paid pilots, then automate. '
      'Money changing hands is the only validation that counts — everything before is rehearsal.',
      'Animated flow of the lean startup validation sequence', ['mvp', 'validation', 'hands-on']),
    S('table',
      {'name': 'unit economics', 'cols': [('CAC', 'COST', 'to acquire one customer'), ('LTV', 'VALUE', 'lifetime gross profit'),
                                          ('payback', 'RATIO', 'CAC ÷ monthly margin'), ('rule', 'GATE', 'LTV ≥ 3× CAC')]},
      'Unit economics decides whether the business can ever work: lifetime value must clear acquisition cost by ~3×. '
      'Estimate both before building — a great product with broken unit economics is a hobby with servers.',
      'Table of unit-economics fundamentals', ['unit economics', 'worked estimation']),
    S('concept',
      {'title': 'Founder-market fit', 'lines': ['10-year problem: will you persist?', 'Unfair advantage: why you win',
                                                 'Boring markets: less competition', 'Niche down, then expand'],
       'accent': CYAN},
      'Pick a problem you\'ll still care about in year seven with an advantage competitors can\'t copy-paste. '
      'Boring markets with real budgets beat exciting markets with forty funded competitors.',
      'Concept box: founder-market fit', ['founder', 'pitfalls', 'concepts']),
]

KITS['il10-quantfin'] = [
    S('layers',
      {'layers': [('Quant researcher / PM', 'own strategies, own P&L'),
                  ('Quant developer', 'low-latency systems, research infra'),
                  ('Quant analyst', 'models, backtests, risk'),
                  ('Foundations', 'probability, linear algebra, coding')]},
      'The quant ladder runs foundations → analyst → developer → researcher/PM, with P&L ownership at the top. '
      'Each rung compounds the same three bases: probability, linear algebra, and fast code.',
      'Animated layered diagram of the quantitative finance ladder', ['quant', 'concepts']),
    S('flow',
      {'steps': [('Probability', 'core interview filter'), ('Mental math', 'speed + accuracy'), ('Brainteasers', 'structured thinking'), ('Coding', 'implement under time')]},
      'Quant interviews filter on probability first — the worked example\'s answer — then mental math, structured brainteasers, and timed coding. '
      'Probability fluency is the gate: fail it and nothing else gets evaluated.',
      'Animated flow of quant interview preparation', ['interview', 'worked example', 'hands-on']),
    S('concept',
      {'title': 'Estimation the quant way', 'lines': ['Fermi: decompose ruthlessly', 'Order of magnitude > precision',
                                                       'State assumptions out loud', 'Sanity-check against knowns'],
       'accent': GREEN},
      'Quant estimation is Fermi decomposition narrated aloud: break the unknown into known-ish pieces, multiply, sanity-check. '
      'Interviewers grade the structure of your assumptions, not the final digit.',
      'Concept box: Fermi estimation technique', ['worked estimation', 'fermi', 'concepts']),
    S('compare',
      {'lt': 'Sell-side', 'li': ['Market making, structuring', 'Client flow, steadier', 'Larger teams'],
       'rt': 'Buy-side', 'ri': ['Hedge funds, prop trading', 'P&L pressure, higher upside', 'Smaller, sharper teams'],
       'left_accent': ACCENT, 'right_accent': PURPLE},
      'Sell-side quants serve client flow at banks; buy-side quants chase P&L at funds and prop shops. '
      'The buy-side pays more and fires faster — match the risk profile to your temperament honestly.',
      'Animated comparison of sell-side vs buy-side quant paths', ['career', 'honesty', 'concepts']),
]

# ================= IL-11 KITS =================

KITS['il11-perimeter'] = [
    S('compare',
      {'lt': 'Castle-and-moat', 'li': ['Trust = inside the network', 'VPN extends the moat', 'Breach inside = game over'],
       'rt': 'Zero trust', 'ri': ['Trust = verified per request', 'Identity is the perimeter', 'Breach contained by design'],
       'left_accent': RED, 'right_accent': GREEN},
      'The perimeter model trusts everything inside the network; zero trust verifies every request regardless of origin. '
      'Assume-breach means designing so that one compromised host cannot become a domain-wide incident.',
      'Animated comparison of perimeter vs zero-trust models', ['perimeter', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('Phish one user', 'initial access'), ('Move laterally', 'flat network'), ('Escalate', 'weak segmentation'), ('Exfiltrate', 'no egress checks')]},
      'The classic perimeter kill chain: one phished credential becomes lateral movement across a flat network. '
      'Each stage succeeds because the interior was trusted — micro-segmentation exists to break exactly this chain.',
      'Animated flow of the perimeter-era attack path', ['lateral movement', 'concepts']),
    S('concept',
      {'title': 'Assume breach', 'lines': ['Design as if already compromised', 'Limit blast radius: segment everything',
                                            'Verify continuously, not once', 'Defenders should hunt, not just block'],
       'accent': ORANGE},
      'Assume-breach flips the defender\'s job from keeping attackers out to limiting what they can do inside. '
      'The worked example\'s answer: defenders should hunt for intruders already present, not merely guard the gate.',
      'Concept box: the assume-breach mindset', ['assume breach', 'worked example', 'concepts']),
    S('table',
      {'name': 'why the perimeter fell', 'cols': [('cloud', 'SHIFT', 'assets outside the moat'), ('mobile', 'SHIFT', 'users outside the moat'),
                                                   ('SaaS', 'SHIFT', 'data outside the moat'), ('VPN', 'WEAKNESS', 'extends trust too far')]},
      'Cloud, mobile, and SaaS moved the assets outside the castle walls while VPNs kept extending implicit trust outward. '
      'The perimeter didn\'t fail from one bug — the network stopped being the boundary of anything.',
      'Table of forces that dissolved the network perimeter', ['cloud', 'vpn', 'concepts']),
]

KITS['il11-nist'] = [
    S('layers',
      {'layers': [('7. Dynamic policy', 'enterprise-collected intelligence drives access'),
                  ('5–6. Least privilege + continuous monitoring', 'right-size, watch everything'),
                  ('3–4. Per-session grant, policy-driven', 'no standing access'),
                  ('1–2. All sources are resources; all comms secured', 'never trust, always verify')]},
      'NIST SP 800-207\'s seven tenets stack from "everything is a resource" up to dynamic, intelligence-driven policy. '
      'The worked example asks the count — seven — but the exam tests the logic: access is per-session, least-privilege, and continuously evaluated.',
      'Animated layered diagram of the seven NIST zero-trust tenets', ['nist', 'tenets', 'worked example']),
    S('flow',
      {'steps': [('Subject requests', 'user/device/app'), ('PEP intercepts', 'policy enforcement point'), ('PDP decides', 'policy engine + trust algo'), ('Grant/deny', 'per-session')]},
      'Every access request passes a Policy Enforcement Point that asks the Policy Decision Point — engine plus trust algorithm — for a verdict. '
      'The grant is per-session: reconnect and you\'re evaluated again.',
      'Animated flow of the PEP/PDP access decision', ['pep', 'pdp', 'concepts']),
    S('concept',
      {'title': 'Never trust, always verify', 'lines': ['Verify identity every request', 'Verify device health every request',
                                                         'Verify context: location, risk', 'Trust expires; re-verify'],
       'accent': GREEN},
      'The tenet in one line: no implicit trust from network location, past authentication, or asset ownership. '
      'Each request re-proves identity, device health, and context before access is granted.',
      'Concept box: never trust, always verify', ['verify', 'concepts']),
    S('compare',
      {'lt': 'Data-centric (NIST)', 'li': ['Protect the resource itself', 'Classification drives policy', 'Works anywhere the data goes'],
       'rt': 'Network-centric (legacy)', 'ri': ['Protect the pipe/segment', 'VLANs and firewalls', 'Breaks when data moves'],
       'left_accent': GREEN, 'right_accent': RED},
      'NIST is data-centric: policy travels with the resource, not the network segment. '
      'When data lives in SaaS and on phones, protecting the pipe protects nothing — protect the data.',
      'Animated comparison of data-centric vs network-centric security', ['data-centric', 'concepts']),
]

KITS['il11-cisa'] = [
    S('layers',
      {'layers': [('Governance', 'policy, risk, compliance across all'),
                  ('Devices / Networks / Applications', 'the enforcement surfaces'),
                  ('Identity', 'the primary control plane'),
                  ('Data', 'the asset everything protects')]},
      'CISA\'s five pillars — identity, devices, networks, applications, data — wrapped in governance. '
      'Identity sits at the center because every pillar\'s decision starts with "who and what is asking".',
      'Animated layered diagram of the five CISA zero-trust pillars', ['cisa', 'pillars', 'worked example']),
    S('flow',
      {'steps': [('Traditional', 'manual, perimeter'), ('Initial', 'some automation'), ('Advanced', 'broad automation'), ('Optimal', 'fully dynamic')]},
      'Each pillar matures through Traditional → Initial → Advanced → Optimal. '
      'Maturity is per-pillar: an "optimal" identity program beside a "traditional" network is the normal enterprise reality.',
      'Animated flow of CISA maturity stages', ['maturity', 'concepts']),
    S('compare',
      {'lt': 'Traditional identity', 'li': ['Passwords, static groups', 'VPN = trusted', 'Annual access reviews'],
       'rt': 'Optimal identity', 'ri': ['Phishing-resistant MFA', 'Continuous risk evaluation', 'Just-in-time, auto-revoked'],
       'left_accent': RED, 'right_accent': GREEN},
      'The identity pillar\'s journey: from passwords and static groups to phishing-resistant MFA with continuous, risk-driven evaluation. '
      'Access becomes just-in-time and self-revoking instead of standing and forgotten.',
      'Animated comparison of traditional vs optimal identity maturity', ['identity', 'mfa', 'concepts']),
    S('concept',
      {'title': 'Using the model', 'lines': ['Score each pillar separately', 'Fund the lowest pillar first',
                                              'Re-score quarterly', 'Optimal is a direction, not a destination'],
       'accent': CYAN},
      'Run the model as a gap analysis: score all five pillars, invest in the weakest, re-score quarterly. '
      'Nobody reaches "optimal" everywhere — the model is a compass for security spending, not a finish line.',
      'Concept box: applying the CISA maturity model', ['hands-on', 'pitfalls', 'concepts']),
]

KITS['il11-defaultdeny'] = [
    S('compare',
      {'lt': 'Default-allow', 'li': ['Everything runs unless blocked', 'Blocklists chase malware', 'New threat = unprotected'],
       'rt': 'Default-deny', 'ri': ['Nothing runs unless approved', 'Allowlists define good', 'New threat = blocked by default'],
       'left_accent': RED, 'right_accent': GREEN},
      'Default-deny inverts the security question from "is this known-bad?" to "is this known-good?" '
      'The worked example\'s definition: nothing executes unless explicitly authorized — unknown software fails closed.',
      'Animated comparison of default-allow vs default-deny', ['default deny', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('Execution attempt', 'process launches'), ('Policy check', 'hash/signer/path rule'), ('Allow?', 'explicit rule match'), ('Block + alert', 'default verdict')]},
      'Every execution attempt hits the policy engine: hash, publisher, or path rule must explicitly allow it. '
      'No matching rule means block-and-alert — the default verdict that makes zero-days fail closed.',
      'Animated flow of default-deny enforcement', ['allowlist', 'enforcement', 'concepts']),
    S('layers',
      {'layers': [('Monitoring: blocks + attempts', 'tune, detect bypass tries'),
                  ('Enforcement: block unlisted', 'production default-deny'),
                  ('Learning: audit mode', 'build the allowlist from reality'),
                  ('Inventory: what runs here', 'baseline first')]},
      'Roll out in layers: inventory what runs, learn in audit mode, enforce, then monitor blocks as detection signal. '
      'Skipping learning mode is the classic failure — enforcement without a complete allowlist is a self-inflicted outage.',
      'Animated layered diagram of default-deny rollout', ['rollout', 'pitfalls', 'hands-on']),
    S('concept',
      {'title': 'Fail closed', 'lines': ['Unknown binary → blocked', 'Policy service down → block, not allow',
                                          'Bypass attempt → alert SOC', 'Usability cost is real: plan for it'],
       'accent': ORANGE},
      'Fail-closed means every ambiguity resolves to "block": unknown binaries, unreachable policy services, tamper attempts. '
      'The usability cost is real — budget exception workflows or users will route around the control.',
      'Concept box: fail-closed design', ['fail closed', 'pitfalls', 'concepts']),
]

KITS['il11-osi'] = [
    S('layers',
      {'layers': [('7 Application — phishing, malicious docs', '6 Presentation — TLS abuse, encoding tricks'),
                  ('5 Session — hijacking, 4 Transport — SYN floods', '3 Network — spoofing, 2 Data link — ARP poison'),
                  ('1 Physical — tapping, rogue devices', 'every layer is an attack surface')]},
      'The worked example\'s numbers — 7 OSI layers, 4 TCP/IP — matter because each layer is a distinct attack surface. '
      'Defenses must stack per layer: no single control covers ARP poisoning and phishing at once.',
      'Animated layered diagram of OSI layers under attack', ['osi', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('SYN', 'client → server'), ('SYN-ACK', 'server → client'), ('ACK', 'client → server'), ('Established', 'data flows')]},
      'The TCP three-way handshake synchronizes sequence numbers before data flows — and SYN floods abuse it by never completing the third step. '
      'SYN cookies let servers survive the flood without tracking half-open connections.',
      'Animated flow of the TCP three-way handshake', ['tcp', 'handshake', 'concepts']),
    S('table',
      {'name': 'attacks by layer', 'cols': [('L7', 'ATTACK', 'phishing, SQLi, XSS'), ('L4', 'ATTACK', 'SYN flood, RST injection'),
                                             ('L3', 'ATTACK', 'IP spoofing, ICMP abuse'), ('L2', 'ATTACK', 'ARP spoofing, VLAN hopping')]},
      'Map the attack to the layer to pick the control: ARP spoofing needs dynamic ARP inspection, SYN floods need cookies, phishing needs user + email controls. '
      'Layer confusion is why "the firewall" never fixed anything above L4.',
      'Table of network attacks mapped to OSI layers', ['attacks', 'layers', 'concepts']),
    S('concept',
      {'title': 'Encapsulation', 'lines': ['Each layer wraps the one above', 'Headers = layer N\'s metadata',
                                             'Wireshark reads inside-out', 'Encrypt at the right layer'],
       'accent': CYAN},
      'Encapsulation wraps each layer\'s payload with the next layer\'s header — which is why Wireshark peels packets inside-out. '
      'Encryption must sit at the right layer: TLS protects L7 payload without hiding L3 routing.',
      'Concept box: encapsulation and where encryption sits', ['encapsulation', 'hands-on', 'concepts']),
]

KITS['il11-hashing'] = [
    S('concept',
      {'title': 'What makes a hash cryptographic', 'lines': ['Preimage resistant: can\'t reverse', 'Collision resistant: can\'t find twins',
                                                              'Avalanche: 1-bit flip → 50% change', 'Fast to compute, slow to break'],
       'accent': GREEN},
      'A cryptographic hash is a one-way fingerprint: easy to compute, infeasible to reverse or collide. '
      'The avalanche effect means tampering anywhere scrambles the digest completely — the property integrity checking relies on.',
      'Concept box: cryptographic hash properties', ['hash', 'integrity', 'concepts']),
    S('compare',
      {'lt': 'Legacy: MD5 / SHA-1', 'li': ['Collisions demonstrated', 'Fast = brute-force friendly', 'Never for integrity now'],
       'rt': 'Current: SHA-2 / SHA-3', 'ri': ['No practical collisions', 'SHA-256/512 standard', 'The worked example\'s answer'],
       'left_accent': RED, 'right_accent': GREEN},
      'MD5 and SHA-1 have demonstrated collisions — they are broken for integrity. '
      'Current practice is the SHA-2 family (SHA-256/512); the exam expects you to name it, not the legacy algorithms.',
      'Animated comparison of hash families', ['sha-256', 'md5', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('Compute digest', 'at the source'), ('Transmit', 'file + hash'), ('Recompute', 'at destination'), ('Compare', 'match = intact')]},
      'Integrity checking: hash the file at the source, transmit both, recompute at the destination, compare digests. '
      'A match proves the bits are unchanged; a mismatch proves tampering or corruption — with no way to know which.',
      'Animated flow of hash-based integrity verification', ['integrity', 'concepts']),
    S('concept',
      {'title': 'Salts defeat rainbow tables', 'lines': ['Rainbow table: precomputed hash → password', 'Salt: unique random per password',
                                                          'Same password → different hashes', 'bcrypt/Argon2: slow by design'],
       'accent': ORANGE},
      'Rainbow tables precompute hashes for common passwords — salting makes every entry unique and the tables worthless. '
      'For password storage use slow, salted KDFs (bcrypt, Argon2), never raw SHA-256.',
      'Concept box: salting and password hashing', ['salt', 'rainbow table', 'pitfalls', 'concepts']),
]

KITS['il11-encrypt'] = [
    S('compare',
      {'lt': 'Symmetric (AES)', 'li': ['One shared key', 'Fast: bulk data', 'Key distribution problem'],
       'rt': 'Asymmetric (RSA/ECC)', 'ri': ['Public + private keypair', 'Slow: key exchange, signatures', 'Solves distribution'],
       'left_accent': ACCENT, 'right_accent': PURPLE},
      'The worked example\'s fill-in: symmetric uses one shared key, asymmetric uses a keypair. '
      'Practice combines them — asymmetric exchanges a session key, symmetric encrypts the bulk data.',
      'Animated comparison of symmetric vs asymmetric encryption', ['symmetric', 'asymmetric', 'worked example']),
    S('flow',
      {'steps': [('ClientHello', 'ciphers offered'), ('Certificate', 'server proves identity'), ('Key exchange', 'session key agreed'), ('Encrypted session', 'AES-GCM bulk')]},
      'TLS handshakes authenticate the server via certificate, agree a session key asymmetrically, then switch to fast symmetric encryption. '
      'The certificate check is the whole trust anchor — skip validation and the encryption protects a session with an attacker.',
      'Animated flow of the TLS handshake', ['tls', 'handshake', 'concepts']),
    S('concept',
      {'title': 'Key management is the system', 'lines': ['Keys in code/config = compromised', 'KMS/HSM: keys never leave',
                                                          'Rotate on schedule + on suspicion', 'Lost key = lost data: back up'],
       'accent': RED},
      'Encryption without key management is decoration: keys in source code or chat logs are already compromised. '
      'Use a KMS/HSM so keys never leave hardware, rotate routinely, and back up keys — losing the key loses the data.',
      'Concept box: encryption key management', ['kms', 'keys', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'cipher selection', 'cols': [('AES-256-GCM', 'USE', 'bulk data, authenticated'), ('ChaCha20-Poly1305', 'USE', 'mobile/no AES-NI'),
                                             ('RSA-2048+', 'USE', 'key exchange, signatures'), ('ECC P-256', 'USE', 'same, smaller keys'),
                                             ('DES / RC4', 'NEVER', 'broken, exam distractor')]},
      'Choose authenticated modes (GCM, Poly1305) so tampering is detected, not just scrambled. '
      'DES and RC4 appear on exams only as "which is broken" distractors — never select them.',
      'Table of cipher selection guidance', ['aes', 'cipher', 'pitfalls', 'concepts']),
]

KITS['il11-adstruct'] = [
    S('layers',
      {'layers': [('Forest: the security boundary', 'schema + config shared; compromise = total'),
                  ('Domain: authentication boundary', 'users, computers, GPOs live here'),
                  ('OU: delegation + GPO scope', 'organize and manage'),
                  ('Objects: users, groups, computers', 'the leaves')]},
      'The forest is the security boundary — compromise the forest and every domain falls; domains are authentication boundaries within it. '
      'The worked example\'s answer is the forest: design trust and tiering around that fact.',
      'Animated layered diagram of Active Directory structure', ['forest', 'domain', 'worked example', 'concepts']),
    S('concept',
      {'title': 'Trusts: direction matters', 'lines': ['One-way: A trusts B, not reverse', 'Transitive: trust flows through',
                                                        'Forest trust: selective auth recommended', 'Trust = attack path: audit it'],
       'accent': ORANGE},
      'A trust lets one domain accept another\'s authentication — and every trust is a potential attack path. '
      'Use selective authentication on forest trusts so only approved principals cross, and audit trusts like firewall rules.',
      'Concept box: AD trust relationships', ['trust', 'concepts']),
    S('table',
      {'name': 'FSMO roles', 'cols': [('Schema Master', 'FOREST', 'schema changes'), ('Domain Naming', 'FOREST', 'domain add/remove'),
                                       ('PDC Emulator', 'DOMAIN', 'auth, time, password'), ('RID Master', 'DOMAIN', 'SID allocation'),
                                       ('Infrastructure', 'DOMAIN', 'cross-domain refs')]},
      'Five FSMO roles hold single-master operations per forest or domain — the PDC Emulator being the most operationally critical. '
      'Know which are forest-wide vs per-domain; seizing roles is recovery, transferring them is maintenance.',
      'Table of FSMO roles', ['fsmo', 'concepts']),
    S('flow',
      {'steps': [('OU design', 'by admin need'), ('Delegate', 'least privilege'), ('Link GPO', 'at the OU'), ('Enforce', 'no overrides below')]},
      'Design OUs around delegation and GPO scoping, not the org chart — org charts change, admin boundaries shouldn\'t. '
      'Link GPOs at the OU, delegate only the rights each team needs, and enforce where policy must not be overridden.',
      'Animated flow of OU and GPO design', ['ou', 'gpo', 'hands-on', 'concepts']),
]

KITS['il11-adattacks'] = [
    S('flow',
      {'steps': [('Find SPN account', 'weak password'), ('Request TGS', 'any domain user can'), ('Crack offline', 'no lockout risk'), ('Use the ticket', 'service access')]},
      'Kerberoasting: any domain user can request service tickets, then crack them offline at leisure with no lockout risk. '
      'The fix is structural — long random SPN passwords or Group Managed Service Accounts.',
      'Animated flow of a Kerberoasting attack', ['kerberoasting', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('Steal NTLM hash', 'mimikatz, LSASS'), ('Pass the hash', 'no cracking needed'), ('Authenticate', 'as the victim'), ('Move laterally', 'repeat')]},
      'Pass-the-hash skips cracking entirely: the NTLM hash itself authenticates. '
      'Credential Guard and tiered admin workstations exist because hashes are stealable wherever an admin logs on.',
      'Animated flow of pass-the-hash', ['pass-the-hash', 'concepts']),
    S('layers',
      {'layers': [('Golden ticket: forge TGTs', 'krbtgt hash = domain forever'),
                  ('Silver ticket: forge TGS', 'service account hash = service'),
                  ('DCSync: replicate hashes', 'mimikatz, pulls all secrets'),
                  ('Initial: phish / spray', 'the foothold')]},
      'AD attacks escalate in layers: initial foothold, hash theft, ticket forgery, and at the peak the golden ticket — forged with the krbtgt hash. '
      'A golden ticket means rebuilding the forest; krbtgt must be rotated twice to kill it.',
      'Animated layered diagram of AD attack escalation', ['golden ticket', 'dcsync', 'concepts']),
    S('concept',
      {'title': 'Why AD falls', 'lines': ['Flat networks: lateral movement free', 'Standing DA rights: always available',
                                           'Weak SPN passwords: roastable', 'No tiering: workstation = domain'],
       'accent': RED},
      'AD doesn\'t fall from one vulnerability — it falls from architecture: flat networks, standing domain-admin rights, roastable service accounts. '
      'Each hardening control in the next module maps to one of these structural failures.',
      'Concept box: structural reasons AD gets compromised', ['pitfalls', 'concepts']),
]

KITS['il11-adharden'] = [
    S('layers',
      {'layers': [('Tier 0: domain controllers, identity', 'most privileged, most guarded'),
                  ('Tier 1: servers, apps', 'server admins only'),
                  ('Tier 2: workstations', 'helpdesk, user admins'),
                  ('PAW: privileged access workstations', 'admins never touch user machines')]},
      'The tier model stops credential theft by never letting high-privilege credentials touch low-trust machines. '
      'The worked example\'s scenario — helpdesk logging onto user workstations with domain creds — violates tiering directly.',
      'Animated layered diagram of the AD tier model', ['tier model', 'worked example', 'concepts']),
    S('concept',
      {'title': 'Credential Guard + LAPS', 'lines': ['Credential Guard: isolates LSASS secrets', 'VBS: hashes never in readable memory',
                                                      'LAPS: unique local admin per machine', 'Together: theft gets crumbs'],
       'accent': GREEN},
      'Credential Guard uses virtualization-based security to isolate LSASS so stolen memory yields nothing; LAPS gives every machine a unique rotating local admin password. '
      'Together they make a compromised workstation a dead end instead of a stepping stone.',
      'Concept box: Credential Guard and LAPS', ['credential guard', 'laps', 'concepts']),
    S('flow',
      {'steps': [('Inventory priv', 'who has DA?'), ('Remove standing', 'JIT via PIM'), ('Tier workstations', 'PAWs for admins'), ('Monitor', 'alert on anomalies')]},
      'Hardening sequence: inventory privileged access, eliminate standing rights via just-in-time elevation, tier the workstations, then monitor. '
      'Doing it in this order avoids breaking operations — monitoring a messy estate just generates noise.',
      'Animated flow of the AD hardening sequence', ['hardening', 'hands-on', 'concepts']),
    S('table',
      {'name': 'hardening checklist', 'cols': [('krbtgt', 'ROTATE 2×', 'kills golden tickets'), ('SPN passwords', '30+ RANDOM', 'or gMSA'),
                                                ('legacy protocols', 'DISABLE', 'LLMNR, NBT-NS, SMBv1'), ('admin count', 'MINIMIZE', 'no standing DA')]},
      'The non-negotiable checklist: double-rotate krbtgt, randomize or gMSA-ify service accounts, kill legacy protocols, minimize domain admins. '
      'Each item closes one of the attack paths from the previous module.',
      'Table of AD hardening checklist items', ['checklist', 'pitfalls', 'hands-on']),
]

KITS['il11-allowlist'] = [
    S('flow',
      {'steps': [('Inventory', 'what actually runs'), ('Learning mode', 'audit, don\'t block'), ('Tune rules', 'publishers, hashes'), ('Enforce', 'block the rest')]},
      'The worked example\'s answer: learning (audit) mode comes before enforcement because the allowlist must reflect reality first. '
      'Enforcing from a guessed policy blocks legitimate software and trains users to demand bypasses.',
      'Animated flow of allowlist deployment phases', ['learning mode', 'worked example', 'hands-on']),
    S('compare',
      {'lt': 'Allowlist', 'li': ['Permits known-good only', 'Fails closed on novelty', 'High setup, strong control'],
       'rt': 'Blocklist (AV)', 'ri': ['Blocks known-bad only', 'Fails open on novelty', 'Low setup, chasing threats'],
       'left_accent': GREEN, 'right_accent': ORANGE},
      'Allowlists define good and block everything else; blocklists define bad and permit everything else. '
      'Against novel malware the allowlist fails closed while the blocklist fails open — the fundamental asymmetry.',
      'Animated comparison of allowlisting vs blocklisting', ['allowlist', 'blocklist', 'concepts']),
    S('concept',
      {'title': 'Rule types, strongest first', 'lines': ['Hash: exact binary, brittle to updates', 'Publisher cert: survives updates',
                                                         'Path: weakest, spoofable', 'Layer them: publisher + path'],
       'accent': CYAN},
      'Hash rules are precise but break on every update; publisher-certificate rules survive updates; path rules are easily spoofed. '
      'Layer publisher rules with path constraints for the practical balance of security and maintainability.',
      'Concept box: allowlist rule types', ['rules', 'hands-on', 'concepts']),
    S('table',
      {'name': 'ThreatLocker-style rollout', 'cols': [('pilot group', 'PHASE 1', 'IT first, tune fast'), ('learning', '2–4 WEEKS', 'capture real usage'),
                                                       ('enforce depts', 'PHASE 2', 'one department at a time'), ('monitor', 'ONGOING', 'blocks = signal')]},
      'Roll out in waves: pilot with IT, learn for weeks, enforce department by department, and treat blocked executions as detection signal. '
      'Big-bang enforcement is how allowlisting projects die in week one.',
      'Table of phased allowlist rollout', ['rollout', 'pitfalls', 'hands-on']),
]

KITS['il11-ringfence'] = [
    S('concept',
      {'title': 'Ringfencing: contain the app', 'lines': ['App runs, but boxed in', 'Controls: files, network, registry, processes',
                                                           'Exploit succeeds → nowhere to go', 'The worked example\'s answer: limits lateral reach'],
       'accent': GREEN},
      'Ringfencing wraps an application in a policy boundary: it may run, but its access to files, network, registry, and child processes is fenced. '
      'An exploited app finds itself in a cage — the payload executes with nowhere to spread.',
      'Concept box: application ringfencing', ['ringfence', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('App launches', 'normal start'), ('Policy applies', 'fence rules'), ('App requests', 'file, net, proc'), ('Allowed/denied', 'per rule')]},
      'At launch the fence policy attaches; every resource request the app makes is checked against it. '
      'Legitimate workflows pass untouched while exfiltration, lateral tools, and persistence mechanisms hit the fence.',
      'Animated flow of ringfence policy enforcement', ['policy', 'concepts']),
    S('compare',
      {'lt': 'Ringfence the app', 'li': ['Compromised app contained', 'No rewrite needed', 'Policy per application'],
       'rt': 'Trust the app', 'ri': ['Exploit = full user context', 'Patching is the only control', 'One 0-day from incident'],
       'left_accent': GREEN, 'right_accent': RED},
      'Trusting the application means one exploited vulnerability inherits the user\'s full context; fencing it means the exploit lands in a cage. '
      'Ringfencing is defense-in-depth for the applications you can\'t rewrite and can\'t stop using.',
      'Animated comparison of fenced vs trusted applications', ['defense in depth', 'concepts']),
    S('table',
      {'name': 'fence policies', 'cols': [('internet access', 'DENY', 'browsers excepted'), ('child processes', 'DENY', 'blocks LOLBins'),
                                           ('sensitive folders', 'DENY', 'finance, HR shares'), ('registry writes', 'DENY', 'persistence paths')]},
      'Typical fences: no internet for Office apps, no child processes (kills living-off-the-land binaries), no sensitive shares, no persistence paths. '
      'Start from these templates and carve exceptions from observed need, not requests.',
      'Table of common ringfence policy templates', ['policy', 'lolbins', 'hands-on']),
]

KITS['il11-storage'] = [
    S('flow',
      {'steps': [('Ransomware runs', 'as the user'), ('Requests elevation', 'UAC prompt'), ('Denied by policy', 'no admin rights'), ('Contained', 'user files only')]},
      'The worked example\'s scenario: ransomware executing as the dispatcher is stopped from system-wide damage when elevation is denied by policy. '
      'Least privilege turns a domain-wide incident into a single-user recovery.',
      'Animated flow of elevation control containing ransomware', ['ransomware', 'worked example', 'concepts']),
    S('layers',
      {'layers': [('Deny: block elevation paths', 'policy-enforced'),
                  ('Prompt: UAC consent', 'user must approve'),
                  ('Standard user: daily work', 'no admin token'),
                  ('Separate admin account', 'elevation only')]},
      'Layer elevation control: users work as standard accounts, UAC prompts on elevation attempts, policy denies what shouldn\'t elevate, and admin work uses separate accounts. '
      'Daily-driving an admin account collapses all four layers into one.',
      'Animated layered diagram of elevation control', ['uac', 'least privilege', 'concepts']),
    S('compare',
      {'lt': 'Removable storage open', 'li': ['USB exfiltration trivial', 'Malware ingress vector', 'No audit trail'],
       'rt': 'Storage control', 'ri': ['Allowlisted devices only', 'Encryption enforced', 'Every mount logged'],
       'left_accent': RED, 'right_accent': GREEN},
      'Uncontrolled USB is both an exfiltration channel and a malware ingress — Stuxnet arrived on removable media. '
      'Storage control allowlists devices, enforces encryption, and logs every mount.',
      'Animated comparison of uncontrolled vs controlled removable storage', ['usb', 'exfiltration', 'concepts']),
    S('concept',
      {'title': 'Protect the shares', 'lines': ['Ransomware encrypts mapped drives', 'Least-privilege share ACLs',
                                                 'Offline/air-gapped backups', 'Test restores, not just backups'],
       'accent': ORANGE},
      'Ransomware follows mapped drives and reachable shares, so share ACLs are containment and offline backups are recovery. '
      'A backup you\'ve never restored is a hope, not a control — test restores on schedule.',
      'Concept box: protecting file shares and backups', ['shares', 'backup', 'pitfalls', 'concepts']),
]

KITS['il11-social'] = [
    S('flow',
      {'steps': [('Recon', 'OSINT on target'), ('Lure', 'crafted message'), ('Hook', 'click / scan / call'), ('Exploit', 'creds / malware')]},
      'Social engineering runs recon → lure → hook → exploit: research the target, craft a believable pretext, trigger the action, harvest the result. '
      'Quishing — the worked example\'s answer — is the same playbook delivered via QR code.',
      'Animated flow of the social-engineering kill chain', ['phishing', 'quishing', 'worked example']),
    S('compare',
      {'lt': 'Phishing (email)', 'li': ['Malicious link/attachment', 'Spoofed sender', 'Filterable at gateway'],
       'rt': 'Quishing / vishing / smishing', 'ri': ['QR code / voice / SMS', 'Bypasses link scanners', 'Harder to filter'],
       'left_accent': ORANGE, 'right_accent': RED},
      'Quishing hides the malicious URL inside a QR code the user scans with a phone — off the corporate email gateway entirely. '
      'Vishing and smishing similarly move to voice and SMS where link-scanning controls don\'t reach.',
      'Animated comparison of phishing channel variants', ['quishing', 'vishing', 'smishing', 'concepts']),
    S('concept',
      {'title': 'Red flags checklist', 'lines': ['Urgency: "act now or else"', 'Authority: spoofed exec / IT',
                                                  'Unexpected QR or attachment', 'Verify via a second channel'],
       'accent': GREEN},
      'Every lure leans on urgency plus authority — "act now" from "the CEO". '
      'The defense is procedural, not cleverness: verify out-of-band via a known-good channel before acting.',
      'Concept box: phishing red flags and verification', ['red flags', 'hands-on', 'concepts']),
    S('layers',
      {'layers': [('User reporting culture', 'one-click phish button'),
                  ('Simulated phishing', 'train the reflex'),
                  ('Email auth: SPF/DKIM/DMARC', 'kill spoofing'),
                  ('Gateway filtering', 'block known-bad')]},
      'Defense layers against social engineering: filter at the gateway, authenticate senders, train with simulations, and make reporting frictionless. '
      'A reported phish the SOC never sees is a training failure, not a user failure.',
      'Animated layered diagram of anti-phishing defenses', ['defense', 'dmarc', 'concepts']),
]

KITS['il11-webattacks'] = [
    S('flow',
      {'steps': [('Input field', 'user text'), ('Concatenation', "query + user text"), ('Query runs', 'as code'), ('Database owned', 'exfil / drop')]},
      'The worked example\'s dispatch portal builds SQL by concatenating user input — attacker text becomes query syntax. '
      'Parameterized queries end it permanently: input stays data, never code.',
      'Animated flow of a SQL injection attack', ['sql injection', 'worked example', 'concepts']),
    S('compare',
      {'lt': 'Stored XSS', 'li': ['Payload saved server-side', 'Hits every viewer', 'Highest impact'],
       'rt': 'Reflected XSS', 'ri': ['Payload in the request', 'Needs a crafted link', 'Lower impact, common'],
       'left_accent': RED, 'right_accent': ORANGE},
      'Stored XSS persists on the server and strikes every visitor; reflected XSS rides a single malicious link. '
      'Both die the same way: output-encode by context and validate input on the server.',
      'Animated comparison of XSS variants', ['xss', 'concepts']),
    S('table',
      {'name': 'OWASP Top 10 (essentials)', 'cols': [('A01 Broken Access', 'RISK', 'IDOR, missing checks'), ('A02 Crypto Failures', 'RISK', 'weak hashes, plaintext'),
                                                      ('A03 Injection', 'RISK', 'SQLi, XSS, SSTI'), ('A07 Auth Failures', 'RISK', 'credential stuffing')]},
      'The OWASP Top 10 ranks web risks by real-world prevalence: broken access control leads, injection follows, crypto and auth failures round out the exam favorites. '
      'Map each finding to its category before writing the report.',
      'Table of essential OWASP Top 10 categories', ['owasp', 'concepts']),
    S('concept',
      {'title': 'Mitigation stack', 'lines': ['Parameterized queries: always', 'Output encoding: per context',
                                               'WAF: defense in depth, not the fix', 'Patch + pentest on cadence'],
       'accent': GREEN},
      'Fix injection in code — parameterized queries and contextual output encoding — and treat the WAF as defense-in-depth, not the cure. '
      'Scheduled pentests verify the fixes hold; the WAF buys time, not safety.',
      'Concept box: web-attack mitigations', ['waf', 'mitigation', 'pitfalls', 'concepts']),
]

KITS['il11-bluedetect'] = [
    S('flow',
      {'steps': [('Telemetry', 'EDR, logs, NetFlow'), ('Detect', 'rules + behavior'), ('Triage', 'analyst verdict'), ('Respond', 'contain, eradicate')]},
      'Detection pipelines turn telemetry into verdicts: EDR and logs feed detections, analysts triage, responders contain. '
      'The worked example\'s winword → powershell → external connection chain is exactly what behavioral EDR exists to catch.',
      'Animated flow of the detection-and-response pipeline', ['edr', 'worked example', 'concepts']),
    S('concept',
      {'title': 'Reading the alert chain', 'lines': ['Parent → child process tree', 'winword → powershell = classic macro',
                                                      'External connection = C2 suspect', 'Isolate first, investigate second'],
       'accent': RED},
      'Read alerts as process trees: a document spawning a shell that reaches the internet is the macro-malware signature. '
      'Isolate the host before deep investigation — containment delayed is containment denied.',
      'Concept box: interpreting an EDR alert chain', ['alert', 'hands-on', 'concepts']),
    S('layers',
      {'layers': [('Lessons learned', 'improve the controls'),
                  ('Eradication + recovery', 'remove persistence, restore'),
                  ('Containment', 'isolate hosts, block IOCs'),
                  ('Preparation + detection', 'playbooks, telemetry')]},
      'Incident response runs preparation → detection → containment → eradication → lessons-learned, with each phase gated on the last. '
      'Skipping to eradication before containment just re-infects the rebuilt host.',
      'Animated layered diagram of incident-response phases', ['incident response', 'concepts']),
    S('table',
      {'name': 'MITRE ATT&CK mapping', 'cols': [('Initial Access', 'TACTIC', 'phishing T1566'), ('Execution', 'TACTIC', 'powershell T1059'),
                                                 ('Persistence', 'TACTIC', 'registry run keys'), ('Exfiltration', 'TACTIC', 'C2 channel T1041')]},
      'Map every alert to ATT&CK tactics and techniques to see the campaign, not just the event. '
      'The alert chain above spans four tactics — that breadth is what makes it an incident, not noise.',
      'Table mapping the alert chain to MITRE ATT&CK', ['mitre', 'att&ck', 'concepts']),
]

KITS['il11-heroreview'] = [
    S('layers',
      {'layers': [('Entra ID: identity plane', 'CA, PIM, lifecycle'),
                  ('Endpoints: allowlist + ringfence', 'default-deny execution'),
                  ('AD: tiered, hardened', 'no standing privilege'),
                  ('Crypto/network: hashes, TLS, segmentation', 'the foundations')]},
      'Full-spectrum review stacks the course bottom-up: crypto and network foundations, hardened AD, default-deny endpoints, governed identity. '
      'Every layer assumes the ones below — the review drill walks the stack in dependency order.',
      'Animated layered diagram of the full zero-trust spectrum', ['review', 'concepts']),
    S('flow',
      {'steps': [('Tenets drill', 'recite the seven'), ('Scenario drill', 'apply to Harborview'), ('Hands-on drill', 'KQL + PowerShell'), ('Exam drill', 'timed questions')]},
      'The review rotation cycles tenets → scenarios → hands-on → timed exam questions. '
      'The worked example\'s advice for blanking on tenets: reconstruct from the stack — each layer implies its tenets.',
      'Animated flow of the hero review drill rotation', ['drill', 'worked example', 'hands-on']),
    S('concept',
      {'title': 'Harborview: the running case', 'lines': ['Dispatch company, warehouses, drivers', 'Every module applied to one estate',
                                                          'Scenarios reuse its constraints', 'Think in its hallways on exam day'],
       'accent': CYAN},
      'Harborview — the dispatch company with warehouses and drivers — is the course\'s running case study. '
      'On scenario questions, reason inside its hallways: WAN drops, shared workstations, seasonal contractors.',
      'Concept box: the Harborview case study', ['harborview', 'scenarios', 'concepts']),
    S('table',
      {'name': 'weak-area triage', 'cols': [('tenets', 'DRILL', 'recite + apply'), ('KQL', 'DRILL', 'write 10 queries'),
                                             ('scenarios', 'DRILL', 'Harborview replays'), ('exam sim', 'DRILL', 'timed, review misses')]},
      'Triage weak areas with targeted drills: recite tenets cold, write KQL until fluent, replay Harborview scenarios, then timed exam sims. '
      'Review every miss back to the concept — pattern-matching questions without concepts fails on variants.',
      'Table of review drills by weak area', ['drill', 'pitfalls', 'hands-on']),
]

KITS['il11-heroscen'] = [
    S('flow',
      {'steps': [('Phase 0: visibility', 'inventory, logs'), ('Phase 1: endpoints', 'allowlist + EDR'), ('Phase 2: identity', 'MFA, CA, PIM'), ('Phase 3: network', 'segment, monitor')]},
      'The capstone rollout sequences visibility → endpoints → identity → network. '
      'The worked example endorses endpoint allowlisting in Phase 1: execution control contains breaches while identity work proceeds.',
      'Animated flow of the zero-trust rollout phases', ['rollout', 'worked example', 'concepts']),
    S('concept',
      {'title': 'Scenario method', 'lines': ['Read for constraints first', 'Map to pillars + tenets',
                                              'Eliminate distractor answers', 'Harborview logic over memorization'],
       'accent': GREEN},
      'Attack scenario questions with a method: extract the constraints, map them to pillars and tenets, eliminate answers that violate either. '
      'Harborview-logic beats memorization — the scenarios reward reasoning, not recall.',
      'Concept box: scenario-question method', ['scenarios', 'exam', 'hands-on']),
    S('compare',
      {'lt': 'Technical answer', 'li': ['Names the control', 'Correct but shallow', 'Misses the business fit'],
       'rt': 'Architect answer', 'ri': ['Names control + sequence', 'Phased, risk-ordered', 'Fits Harborview constraints'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Capstone answers are graded like architects think: the right control in the right phase for the right risk. '
      'A technically correct control in the wrong phase is a wrong answer at this level.',
      'Animated comparison of technician vs architect answers', ['scenarios', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'capstone scenario toolkit', 'cols': [('assume breach', 'LENS', 'limit blast radius'), ('least privilege', 'LENS', 'right-size every grant'),
                                                      ('verify explicitly', 'LENS', 'per-request checks'), ('phased rollout', 'LENS', 'visibility first')]},
      'Keep four lenses on every scenario: assume breach, least privilege, explicit verification, phased rollout. '
      'Any proposed plan that violates one of them is eliminable before you even check the details.',
      'Table of the capstone scenario toolkit', ['toolkit', 'scenarios', 'concepts']),
]

KITS['il11-lifecycle'] = [
    S('flow',
      {'steps': [('Joiner', 'provision day one'), ('Mover', 'update on transfer'), ('Leaver', 'deprovision fast'), ('Access package', 'right-sized grant')]},
      'Identity lifecycle is joiner-mover-leaver: provision before day one, adjust on transfer, revoke on exit — the worked example\'s Friday-5 PM contractor case. '
      'Access packages bundle the right resources so leaver-processing is one revocation, not a scavenger hunt.',
      'Animated flow of the identity lifecycle', ['lifecycle', 'worked example', 'concepts']),
    S('concept',
      {'title': 'Leavers are the risk', 'lines': ['Orphaned accounts = attack surface', 'Automate: HR event → disable',
                                                   'Review: quarterly access recert', 'Contractors: time-boxed by default'],
       'accent': RED},
      'Every breach report features an account that should have been disabled months ago. '
      'Drive deprovisioning from the HR system event, time-box contractor access by default, and recertify quarterly.',
      'Concept box: leaver risk and deprovisioning', ['leaver', 'pitfalls', 'concepts']),
    S('layers',
      {'layers': [('Access reviews', 'recertify what exists'),
                  ('Access packages', 'requestable bundles'),
                  ('Dynamic groups', 'rule-driven membership'),
                  ('HR-driven provisioning', 'source of truth')]},
      'Stack lifecycle automation: HR as the source of truth, dynamic groups for rule-driven membership, access packages for requests, reviews for recertification. '
      'Manual account management at scale is how orphans are born.',
      'Animated layered diagram of lifecycle automation', ['provisioning', 'hands-on', 'concepts']),
    S('table',
      {'name': 'lifecycle events', 'cols': [('hire', 'TRIGGER', 'pre-day-one provisioning'), ('transfer', 'TRIGGER', 'add new, remove old'),
                                             ('leave', 'TRIGGER', 'disable within hours'), ('contract end', 'TRIGGER', 'auto-expire access')]},
      'Wire every HR event to an identity action with a deadline — especially transfers, where old access lingers while new access arrives. '
      'The transfer case is the quiet privilege-accumulation machine.',
      'Table of HR-driven lifecycle triggers', ['jml', 'pitfalls', 'concepts']),
]

KITS['il11-ca'] = [
    S('flow',
      {'steps': [('Signals', 'user, device, location, risk'), ('Conditions', 'policy filters'), ('Grant controls', 'MFA, compliant, terms'), ('Decision', 'allow / deny / challenge')]},
      'Conditional Access combines signals — the worked example\'s fill-in — into conditions, then applies grant controls for a decision. '
      'Every policy is an if-then: IF these conditions on these signals, THEN require these controls.',
      'Animated flow of a Conditional Access policy evaluation', ['conditional access', 'worked example', 'concepts']),
    S('concept',
      {'title': 'Policy anatomy', 'lines': ['Assignments: who/what/where', 'Conditions: device, risk, app, location',
                                             'Grant: require MFA / compliant / hybrid-joined', 'Session: sign-in frequency, persistence'],
       'accent': ACCENT},
      'A CA policy has four parts: assignments (scope), conditions (context filters), grant controls (what\'s required), and session controls (how long it lasts). '
      'Read policies in that order and misconfigurations surface immediately.',
      'Concept box: Conditional Access policy anatomy', ['policy', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Allow legacy auth', 'li': ['Basic auth, no MFA', 'Password spray target', 'Common breach vector'],
       'rt': 'Block legacy auth', 'ri': ['Modern auth only', 'MFA enforceable', 'First CA policy to write'],
       'left_accent': RED, 'right_accent': GREEN},
      'Legacy authentication bypasses MFA entirely — blocking it is the highest-value first Conditional Access policy. '
      'Report-only mode first to find the stragglers, then enforce.',
      'Animated comparison of legacy-auth handling', ['legacy auth', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'starter CA policies', 'cols': [('block legacy auth', 'PRIORITY 1', 'kill MFA bypass'), ('require MFA', 'PRIORITY 1', 'all users, all apps'),
                                                ('risk-based', 'PRIORITY 2', 'medium+ sign-in risk'), ('compliant device', 'PRIORITY 2', 'admin portals')]},
      'Deploy CA in priority order: block legacy auth and require MFA first, then risk-based and device-compliance policies. '
      'Test each in report-only mode — an untested CA policy is a self-inflicted lockout waiting to happen.',
      'Table of starter Conditional Access policies', ['hands-on', 'pitfalls', 'concepts']),
]

KITS['il11-auth'] = [
    S('compare',
      {'lt': 'SMS / voice MFA', 'li': ['Phishable via SIM-swap', 'SS7 interception risk', 'The worked example\'s attack'],
       'rt': 'Phishing-resistant', 'ri': ['FIDO2 / Windows Hello', 'Cryptographic binding', 'No shared secret to steal'],
       'left_accent': RED, 'right_accent': GREEN},
      'The worked example\'s phished admin lost SMS codes to a relay — SMS MFA is phishable by design. '
      'FIDO2 and Windows Hello bind authentication cryptographically to the device; there\'s no code for the attacker to relay.',
      'Animated comparison of MFA methods', ['mfa', 'fido2', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('Register', 'device-bound key'), ('Challenge', 'relying party'), ('Sign', 'private key, local'), ('Verify', 'public key check')]},
      'Passwordless with FIDO2: register once to create a device-bound keypair, then each sign-in is a cryptographic challenge-response. '
      'The private key never leaves the device — phishing the user yields nothing reusable.',
      'Animated flow of FIDO2 passwordless authentication', ['fido2', 'passwordless', 'concepts']),
    S('layers',
      {'layers': [('Phishing-resistant: FIDO2, Hello', 'target state'),
                  ('App-based TOTP / push', 'better than SMS, still phishable'),
                  ('SMS / voice', 'legacy, SIM-swappable'),
                  ('Password only', 'single factor: never')]},
      'Climb the authentication ladder: password-only is never acceptable, SMS is legacy, app-based is transitional, phishing-resistant is the target. '
      'Move admins first — they\'re the highest-value phishing targets.',
      'Animated layered diagram of authentication strength', ['ladder', 'hands-on', 'concepts']),
    S('concept',
      {'title': 'Authorization ≠ authentication', 'lines': ['Authentication: who are you?', 'Authorization: what may you do?',
                                                             'MFA proves identity, not permission', 'RBAC + PIM govern the second'],
       'accent': ORANGE},
      'Authentication proves who you are; authorization decides what you may do — and MFA only answers the first question. '
      'Pair strong auth with RBAC least-privilege and PIM just-in-time elevation for the complete picture.',
      'Concept box: authentication vs authorization', ['rbac', 'pitfalls', 'concepts']),
]

KITS['il11-hybrid'] = [
    S('flow',
      {'steps': [('On-prem AD', 'source of truth'), ('Entra Connect Sync', 'replication engine'), ('Entra ID', 'cloud directory'), ('SSO', 'seamless sign-in')]},
      'Hybrid identity syncs on-prem AD to Entra ID via Entra Connect Sync, giving one identity for both worlds. '
      'The worked example\'s WAN-drop warehouses need authentication that survives outages — design sync and fallback accordingly.',
      'Animated flow of hybrid identity synchronization', ['hybrid', 'sync', 'worked example']),
    S('compare',
      {'lt': 'PHS (hash sync)', 'li': ['Hash of hash in cloud', 'Cloud auth, survives WAN cut', 'Simplest, recommended default'],
       'rt': 'PTA / Federation', 'ri': ['Auth happens on-prem', 'Needs on-prem availability', 'Complex, specific needs only'],
       'left_accent': GREEN, 'right_accent': ORANGE},
      'Password hash sync lets Entra ID authenticate directly — users keep signing in during a WAN outage. '
      'Pass-through and federation keep auth on-prem, which fails exactly when the WAN does; choose them only for specific requirements.',
      'Animated comparison of hybrid auth methods', ['phs', 'pta', 'federation', 'concepts']),
    S('concept',
      {'title': 'Writeback + Seamless SSO', 'lines': ['Password writeback: cloud → on-prem', 'Needs PHS or PTA (not federated)',
                                                      'Seamless SSO: Kerberos for domain PCs', 'Together: one password everywhere'],
       'accent': CYAN},
      'Password writeback lets cloud password changes flow back on-prem — but only with hash sync or pass-through, not federation. '
      'Add seamless SSO via Kerberos and domain-joined PCs sign in without prompts.',
      'Concept box: writeback and seamless SSO', ['writeback', 'sso', 'concepts']),
    S('table',
      {'name': 'hybrid failure modes', 'cols': [('sync stopped', 'SYMPTOM', 'stale cloud passwords'), ('WAN cut', 'SYMPTOM', 'PTA/federation dead'),
                                                 ('staging mode', 'FIX', 'test sync safely'), ('health monitoring', 'FIX', 'Entra Connect Health')]},
      'Monitor sync health actively: a stopped sync silently strands cloud passwords, and WAN cuts kill on-prem-dependent auth. '
      'Use staging mode to validate sync changes before they touch production.',
      'Table of hybrid identity failure modes', ['troubleshoot', 'pitfalls', 'hands-on']),
]

KITS['il11-govern'] = [
    S('flow',
      {'steps': [('Request', 'justify need'), ('Approve', 'owner decides'), ('Activate', 'time-boxed'), ('Expire', 'auto-revoked')]},
      'Privileged Identity Management makes admin rights just-in-time: request with justification, get approval, activate time-boxed — the worked example\'s 4-hour migration window — then auto-revoke. '
      'No standing Global Admin, ever.',
      'Animated flow of PIM just-in-time elevation', ['pim', 'worked example', 'concepts']),
    S('concept',
      {'title': 'Access reviews', 'lines': ['Recertify: still need it?', 'Owners attest, not IT', 'Auto-remove on deny/timeout',
                                             'Guest accounts: review quarterly'],
       'accent': ORANGE},
      'Access reviews force periodic re-justification: owners attest their people still need the access, denials auto-remove. '
      'Guest and contractor access decays fastest — review it most often.',
      'Concept box: access reviews', ['access reviews', 'concepts']),
    S('layers',
      {'layers': [('Audit: who had what, when', 'forensics + compliance'),
                  ('Review: recertify periodically', 'decay control'),
                  ('Elevate: PIM just-in-time', 'no standing privilege'),
                  ('Assign: RBAC least-privilege', 'right-sized baseline')]},
      'Governance stacks: least-privilege RBAC as the baseline, PIM for just-in-time elevation, reviews to fight decay, audit for forensics. '
      'Each layer assumes the one below — reviews can\'t fix standing Global Admin.',
      'Animated layered diagram of identity governance', ['governance', 'rbac', 'concepts']),
    S('table',
      {'name': 'admin role hygiene', 'cols': [('Global Admin', 'LIMIT', '≤ 5, break-glass only'), ('Privileged Auth Admin', 'SCOPE', 'auth policy only'),
                                               ('Helpdesk', 'SCOPE', 'password reset, no roles'), ('break-glass', 'PROTECT', 'FIDO2, monitored, offline creds')]},
      'Keep Global Admins to a handful of break-glass accounts on FIDO2 with monitored use. '
      'Scope every other role to its job — helpdesk resets passwords, it doesn\'t assign roles.',
      'Table of admin-role hygiene rules', ['roles', 'pitfalls', 'hands-on']),
]

KITS['il11-trouble'] = [
    S('flow',
      {'steps': [('SigninLogs', 'start here'), ('where ResultType != 0', 'failures only'), ('summarize', 'count by user/app'), ('join AuditLogs', 'correlate change')]},
      'The worked example\'s KQL: SigninLogs filtered to nonzero ResultType returns failed sign-ins. '
      'Summarize by user and app to spot spray patterns, then join AuditLogs to correlate with config changes.',
      'Animated flow of KQL sign-in troubleshooting', ['kql', 'worked example', 'hands-on']),
    S('concept',
      {'title': 'KQL operator toolkit', 'lines': ['where: filter rows', 'summarize … by: aggregate',
                                                   'join: correlate tables', 'project: shape output'],
       'accent': CYAN},
      'Four operators carry most troubleshooting: where filters, summarize aggregates, join correlates, project shapes. '
      'Chain them in that order and most identity mysteries resolve in one query.',
      'Concept box: essential KQL operators', ['kql', 'hands-on', 'concepts']),
    S('table',
      {'name': 'PowerShell identity cmdlets', 'cols': [('Get-MgUser', 'READ', 'user objects'), ('Get-MgAuditLogSignIn', 'READ', 'sign-in events'),
                                                        ('Get-EntraBeta*', 'READ', 'conditional access'), ('Connect-MgGraph', 'AUTH', 'delegated/app scopes')]},
      'The Microsoft Graph PowerShell SDK replaces the retired MSOnline module: Connect-MgGraph first with least-privilege scopes, then query users, sign-ins, and CA policy. '
      'Script the checks you run twice — troubleshooting runbooks beat memory.',
      'Table of identity troubleshooting PowerShell cmdlets', ['powershell', 'graph', 'hands-on']),
    S('compare',
      {'lt': 'Portal clicking', 'li': ['Fine for one-offs', 'Slow, unrepeatable', 'No audit of the check'],
       'rt': 'KQL + PowerShell', 'ri': ['Fast at scale', 'Saved, repeatable queries', 'Runbook-ready'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'The portal is fine for one-offs; KQL and PowerShell win at scale — repeatable, shareable, and fast across thousands of events. '
      'Every repeated portal investigation should become a saved query.',
      'Animated comparison of portal vs code troubleshooting', ['runbook', 'hands-on', 'concepts']),
]

KITS['il11-examprep'] = [
    S('table',
      {'name': 'SC-300 domains', 'cols': [('Identity lifecycle', '15–20%', 'provision, manage'), ('Zero Trust + CA', '15–20%', 'policies, signals'),
                                           ('Auth + access', '20–25%', 'MFA, passwordless, RBAC'), ('Governance', '20–25%', 'PIM, reviews, audit')]},
      'SC-300 weights identity lifecycle, Conditional Access, authentication/access, and governance roughly evenly — there\'s no domain to skip. '
      'The worked example\'s partner-access scenario is pure B2B + CA + governance synthesis.',
      'Table of SC-300 exam domain weights', ['sc-300', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('Read scenario', 'constraints first'), ('Identify domain', 'which SC-300 area'), ('Eliminate', 'kill distractors'), ('Pick + move', 'don\'t stall')]},
      'Scenario questions reward method: extract constraints, name the domain, eliminate answers violating least-privilege or zero-trust, pick and move. '
      'Two minutes per question max — flag the essay-like ones and return.',
      'Animated flow of SC-300 scenario technique', ['exam', 'scenarios', 'hands-on']),
    S('concept',
      {'title': 'B2B partner access', 'lines': ['Invite as guest (B2B)', 'CA policies apply to guests too',
                                                 'Access packages for partners', 'Review guest access quarterly'],
       'accent': PURPLE},
      'Partner access is B2B guests governed like everyone else: invite, scope with access packages, enforce Conditional Access, review quarterly. '
      'The exam loves this scenario because it synthesizes lifecycle, CA, and governance in one question.',
      'Concept box: B2B partner-access design', ['b2b', 'worked example', 'concepts']),
    S('compare',
      {'lt': 'Memorize features', 'li': ['Fades in weeks', 'Fails on novel scenarios', 'Portal-click knowledge'],
       'rt': 'Learn the model', 'ri': ['Pillars + tenets transfer', 'Reasons through scenarios', 'Lasts past exam day'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Don\'t memorize portal blades — learn the identity model (lifecycle, CA signals, governance) and reason from it. '
      'Scenario variants defeat memorizers and reward model-thinkers; the model also survives past exam day.',
      'Animated comparison of exam-prep strategies', ['pitfalls', 'concepts']),
]

# ================= IL-12 KITS =================

KITS['py-syntax'] = [
    S('table',
      {'name': 'core types', 'cols': [('int / float', 'NUMERIC', 'arbitrary-precision ints'), ('str / bytes', 'TEXT', 'immutable sequences'),
                                      ('list / tuple', 'SEQUENCE', 'mutable vs immutable'), ('dict / set', 'MAPPING', 'hash-keyed')]},
      'Python\'s core types split along mutability: lists and dicts change in place, tuples and strings don\'t. '
      'That one distinction explains half of beginner bugs — including functions that mysteriously "remember" calls.',
      'Table of Python core data types', ['types', 'concepts']),
    S('flow',
      {'steps': [('for / while', 'iterate'), ('if / elif', 'branch'), ('try / except', 'handle'), ('with', 'manage resources')]},
      'Control flow in Python reads like pseudocode: loops iterate, branches decide, try/except contains failure, with manages resources. '
      'Prefer with-blocks over manual close() — cleanup that depends on remembering is cleanup that won\'t happen.',
      'Animated flow of Python control-flow constructs', ['control flow', 'concepts']),
    S('concept',
      {'title': 'Functions: the contract', 'lines': ['def name(args): → return', 'Defaults evaluated ONCE at def',
                                                     '*args / **kwargs: flexible calls', 'Docstring = the contract'],
       'accent': ACCENT},
      'A function is a contract: signature in, value out, docstring describing the promise. '
      'Remember defaults are evaluated once at definition — the mutable-default trap from the certification module lives here too.',
      'Concept box: Python functions', ['functions', 'pitfalls', 'concepts']),
    S('concept',
      {'title': 'Comprehensions', 'lines': ['[f(x) for x in xs if p(x)]', 'One line: map + filter',
                                             'Generator: (f(x) for x in xs)', 'Readability first: 2 clauses max'],
       'accent': GREEN},
      'Comprehensions compress map-and-filter into one readable line; generator expressions do it lazily for big data. '
      'Keep them to two clauses — beyond that, a plain loop is clearer and clarity wins.',
      'Concept box: comprehensions and generators', ['comprehension', 'hands-on', 'concepts']),
]

KITS['py-oop'] = [
    S('concept',
      {'title': 'The four pillars', 'lines': ['Encapsulation: bundle data + behavior', 'Abstraction: hide complexity',
                                               'Inheritance: specialize, don\'t copy', 'Polymorphism: one interface, many forms'],
       'accent': ACCENT},
      'OOP\'s four pillars organize code around things that change together: encapsulate state with its behavior, inherit to specialize, polymorph to generalize. '
      'Composition usually beats inheritance — "has a" is more flexible than "is a".',
      'Concept box: OOP pillars', ['oop', 'concepts']),
    S('flow',
      {'steps': [('import pkg', 'load module'), ('from x import y', 'bind name'), ('sys.path search', 'find the file'), ('__init__.py', 'package marker')]},
      'Python\'s import system searches sys.path for the module file and binds names into your namespace. '
      'Packages are directories with __init__.py; virtual environments keep each project\'s packages isolated.',
      'Animated flow of the Python import system', ['import', 'modules', 'concepts']),
    S('layers',
      {'layers': [('Your code', 'imports resolved here'),
                  ('venv: isolated site-packages', 'per-project dependencies'),
                  ('Python interpreter', 'the runtime'),
                  ('OS', 'system python — don\'t touch')]},
      'Virtual environments isolate each project\'s dependencies from the system Python. '
      'One venv per project is the rule — "it works on my machine" usually means "it works in my forgotten global environment".',
      'Animated layered diagram of virtual environments', ['venv', 'hands-on', 'pitfalls']),
    S('compare',
      {'lt': 'Class (OOP)', 'li': ['State + behavior bundled', 'Good for: entities, services', 'Overhead for simple data'],
       'rt': 'Dataclass / function', 'ri': ['Plain data containers', 'Good for: records, configs', 'Simpler, testable'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'Reach for classes when behavior belongs with state; reach for dataclasses or plain functions for simple records. '
      'AI-engineering codebases stay maintainable when data stays dumb and logic stays explicit.',
      'Animated comparison of classes vs dataclasses/functions', ['dataclass', 'honesty', 'concepts']),
]

KITS['py-concurrency'] = [
    S('concept',
      {'title': 'The GIL', 'lines': ['One bytecode thread at a time', 'Blocks CPU-bound threading',
                                      'I/O-bound threads still win', 'CPU-bound → multiprocessing'],
       'accent': ORANGE},
      'The worked example\'s answer: the GIL blocks true parallel execution of Python bytecode threads. '
      'Threads still help I/O-bound work (the GIL releases during I/O); CPU-bound work needs multiprocessing or native extensions.',
      'Concept box: the Python GIL', ['gil', 'worked example', 'concepts']),
    S('compare',
      {'lt': 'threading', 'li': ['Shared memory, GIL-limited', 'Best for: I/O-bound', 'Race conditions lurk'],
       'rt': 'asyncio', 'ri': ['Single thread, cooperatively', 'Best for: many connections', 'No races, must not block'],
       'left_accent': ORANGE, 'right_accent': CYAN},
      'Threading suits I/O-bound work with blocking libraries; asyncio suits thousands of concurrent connections in one thread. '
      'Asyncio\'s rule: never block the event loop — one slow sync call stalls everything.',
      'Animated comparison of threading vs asyncio', ['threading', 'asyncio', 'concepts']),
    S('flow',
      {'steps': [('Task created', 'coroutine'), ('await I/O', 'yield control'), ('Event loop', 'runs others'), ('Resume', 'I/O done')]},
      'Asyncio runs coroutines on one thread: await on I/O yields control to the event loop, which runs other tasks until the I/O completes. '
      'Concurrency without threads — and without their race conditions.',
      'Animated flow of the asyncio event loop', ['asyncio', 'event loop', 'concepts']),
    S('concept',
      {'title': 'multiprocessing', 'lines': ['Separate processes, separate GILs', 'True CPU parallelism',
                                              'IPC cost: pickling overhead', 'Pool: map work across cores'],
       'accent': GREEN},
      'Multiprocessing sidesteps the GIL with separate processes, each with its own interpreter. '
      'Pay the pickling cost for inter-process communication gladly when the work is CPU-bound — that\'s what cores are for.',
      'Concept box: multiprocessing for CPU-bound work', ['multiprocessing', 'hands-on', 'concepts']),
]

KITS['py-genai'] = [
    S('flow',
      {'steps': [('Prompt', 'spec + context'), ('Generate', 'model drafts'), ('Review', 'you verify'), ('Test', 'run it')]},
      'GenAI-assisted coding is a loop: specify precisely, let the model draft, review every line, run the tests. '
      'The model writes; you own correctness — generated code you can\'t explain is a liability.',
      'Animated flow of the GenAI coding workflow', ['workflow', 'concepts']),
    S('concept',
      {'title': 'Prompting for code', 'lines': ['Specify: inputs, outputs, edge cases', 'Show: one example of the pattern',
                                                 'Constrain: "no new dependencies"', 'Iterate: small diffs, not rewrites'],
       'accent': CYAN},
      'Good code prompts specify the contract (inputs, outputs, edge cases), show one example, and constrain the solution space. '
      'Ask for small diffs against existing code — full rewrites discard context the model can\'t see.',
      'Concept box: prompting effectively for code', ['prompting', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Trust the output', 'li': ['Paste and ship', 'Bugs you didn\'t write', 'Security holes inherited'],
       'rt': 'Verify the output', 'ri': ['Read every line', 'Run tests + linters', 'You sign the diff'],
       'left_accent': RED, 'right_accent': GREEN},
      'The honesty note\'s core warning: generated code is a draft, not a deliverable. '
      'Read it, test it, lint it — your name is on the commit, not the model\'s.',
      'Animated comparison of trusting vs verifying AI code', ['honesty', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'review checklist', 'cols': [('correctness', 'CHECK', 'edge cases handled?'), ('security', 'CHECK', 'injection, secrets?'),
                                             ('style', 'CHECK', 'matches repo conventions?'), ('tests', 'CHECK', 'new code covered?')]},
      'Review generated code against a checklist: correctness on edge cases, security (no injected secrets or SQL strings), repo style, and test coverage. '
      'Checklist review is faster than freeform and catches the model\'s characteristic failure modes.',
      'Table of the AI-code review checklist', ['review', 'pitfalls', 'hands-on']),
]

KITS['numpy'] = [
    S('concept',
      {'title': 'The ndarray', 'lines': ['Homogeneous, fixed-type grid', 'Shape: (rows, cols, …)', 'Strides: how to walk memory',
                                          'Views vs copies: know which you have'],
       'accent': ACCENT},
      'NumPy\'s ndarray is a homogeneous, strided view over a memory buffer — shape says the dimensions, strides say the layout. '
      'Slicing returns views (shared memory); fancy indexing returns copies. Know which you hold before mutating.',
      'Concept box: NumPy array anatomy', ['ndarray', 'concepts']),
    S('concept',
      {'title': 'Broadcasting', 'lines': ['Shapes align right-to-left', 'Size-1 dims stretch to match',
                                           '(3,1) + (4,) → (3,4)', 'The worked example\'s answer: vectorized ops'],
       'accent': GREEN},
      'Broadcasting stretches size-1 dimensions so differently-shaped arrays combine without explicit loops or copies. '
      'It\'s the mechanism behind "NumPy lets you add a vector to every row" — the worked example\'s vectorization answer.',
      'Concept box: NumPy broadcasting rules', ['broadcasting', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('Python loop', 'slow, per-element'), ('Vectorize', 'one ufunc call'), ('C loop inside', 'fast'), ('100× faster', 'typical win')]},
      'Vectorization replaces Python-level loops with single ufunc calls that loop in C. '
      'The typical 100× speedup isn\'t cleverness — it\'s removing per-element interpreter overhead.',
      'Animated flow of vectorization', ['vectorization', 'hands-on', 'concepts']),
    S('table',
      {'name': 'indexing', 'cols': [('basic slice', 'VIEW', 'a[1:3] — shared memory'), ('boolean mask', 'COPY', 'a[a > 0] — new array'),
                                     ('fancy index', 'COPY', 'a[[2,0]] — new array'), ('np.where', 'COPY', 'conditional select')]},
      'Basic slices are views into the same memory; boolean masks and fancy indexing return copies. '
      'Mutating a view mutates the original — the source of "my array changed itself" bugs.',
      'Table of NumPy indexing semantics', ['indexing', 'views', 'pitfalls']),
]

KITS['pandas'] = [
    S('flow',
      {'steps': [('Load', 'read_csv/parquet'), ('Clean', 'dtypes, nulls, dupes'), ('Transform', 'groupby, merge'), ('Validate', 'assert invariants')]},
      'Wrangling runs load → clean → transform → validate, with validation as a real stage, not an afterthought. '
      'Assert row counts, key uniqueness, and null rates after every transform — silent corruption is the default failure.',
      'Animated flow of the pandas wrangling pipeline', ['wrangling', 'hands-on', 'concepts']),
    S('concept',
      {'title': 'groupby: split-apply-combine', 'lines': ['Split: partition by key', 'Apply: aggregate per group',
                                                           'Combine: reassemble result', 'Think SQL GROUP BY'],
       'accent': ACCENT},
      'groupby splits rows by key, applies an aggregation per group, and combines the results — pandas\' answer to SQL GROUP BY. '
      'If you can say it in GROUP BY, you can say it in groupby; reach for transform() when the result must align back to rows.',
      'Concept box: the split-apply-combine pattern', ['groupby', 'concepts']),
    S('table',
      {'name': 'merge types', 'cols': [('inner', 'JOIN', 'keys in both'), ('left', 'JOIN', 'all left rows'),
                                        ('outer', 'JOIN', 'all rows, NaN gaps'), ('validate', 'CHECK', '"1:1"/"m:1" asserts')]},
      'Merges are joins: inner keeps matches, left keeps all left rows, outer keeps everything with NaN gaps. '
      'Always pass validate= — asserting "m:1" catches the duplicate-key explosion before it silently multiplies your rows.',
      'Table of pandas merge types', ['merge', 'join', 'pitfalls']),
    S('concept',
      {'title': 'Dtype discipline', 'lines': ['Objects are slow: cast to category', 'Downcast numerics: int64 → int32',
                                               'Parse dates at load: parse_dates', 'Memory: 10× savings are normal'],
       'accent': ORANGE},
      'Object dtype is pandas\' slow lane: cast low-cardinality strings to category, downcast numerics, parse dates at load. '
      'Dtype discipline routinely cuts memory 10× — the difference between fitting in RAM and not.',
      'Concept box: pandas dtype discipline', ['dtypes', 'memory', 'pitfalls', 'hands-on']),
]

KITS['viz'] = [
    S('concept',
      {'title': 'Choose the chart by question', 'lines': ['Distribution → histogram / KDE', 'Trend → line (time on x)',
                                                           'Comparison → bar (zero baseline)', 'Relation → scatter'],
       'accent': ACCENT},
      'Chart choice follows the question: distributions get histograms, trends get lines, comparisons get bars with zero baselines, relationships get scatters. '
      'A pie chart is almost never the answer — humans compare angles poorly.',
      'Concept box: chart selection guide', ['charts', 'concepts']),
    S('concept',
      {'title': 'Matplotlib anatomy', 'lines': ['Figure: the whole canvas', 'Axes: one plot region',
                                                 'Axis: ticks, labels, scale', 'Compose: fig, ax = plt.subplots()'],
       'accent': CYAN},
      'Matplotlib composes figures containing axes containing plotted artists — the object model behind every plot. '
      'Work with the (fig, ax) objects directly; pyplot\'s implicit state is fine for exploration and a trap in functions.',
      'Concept box: matplotlib object model', ['matplotlib', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Honest viz', 'li': ['Zero baselines on bars', 'Same scale across panels', 'Show the uncertainty'],
       'rt': 'Dishonest viz', 'ri': ['Truncated axes exaggerate', 'Dual axes mislead', 'Cherry-picked ranges'],
       'left_accent': GREEN, 'right_accent': RED},
      'Honest visualization is an ethical practice: zero baselines, consistent scales, visible uncertainty. '
      'Truncated axes and dual axes don\'t lie technically — they mislead reliably, which is worse.',
      'Animated comparison of honest vs misleading visualization', ['honesty', 'pitfalls', 'concepts']),
    S('flow',
      {'steps': [('Question', 'what decision?'), ('Data', 'right granularity'), ('Encode', 'chart type'), ('Annotate', 'the takeaway')]},
      'Build visualizations decision-first: name the decision, get data at the right granularity, encode it in the right chart, annotate the takeaway. '
      'A plot without an annotated takeaway is decoration awaiting interpretation.',
      'Animated flow of decision-driven visualization', ['hands-on', 'concepts']),
]

KITS['stats-ml'] = [
    S('flow',
      {'steps': [('Hypothesis', 'H₀: no effect'), ('Test statistic', 'from the data'), ('p-value', 'P(data | H₀)'), ('Decide', 'reject or not')]},
      'Hypothesis testing asks "how surprising is this data if nothing is happening?" — the p-value is P(data | H₀), not P(H₀ | data). '
      'Confusing the two is the base-rate fallacy wearing a lab coat.',
      'Animated flow of hypothesis testing', ['hypothesis', 'p-value', 'concepts']),
    S('concept',
      {'title': 'The CLT promise', 'lines': ['Means of samples → normal', 'Holds for n ≳ 30, any shape',
                                              'SE = σ/√n: more data, tighter', 'Powers confidence intervals'],
       'accent': GREEN},
      'The Central Limit Theorem: sample means converge to normal as n grows, whatever the underlying distribution. '
      'Standard error shrinks with √n — quadrupling data only halves uncertainty, the iron law of measurement.',
      'Concept box: the Central Limit Theorem', ['clt', 'concepts']),
    S('compare',
      {'lt': 'A/B test done right', 'li': ['Randomized assignment', 'Pre-registered metric', 'Sufficient power'],
       'rt': 'A/B test done wrong', 'ri': ['Peeking stops early', 'Metric shopping', 'Underpowered noise'],
       'left_accent': GREEN, 'right_accent': RED},
      'Valid A/B tests randomize, pre-register one primary metric, and run to the planned sample size. '
      'Peeking and stopping early inflates false positives — the p-value assumes you looked once.',
      'Animated comparison of valid vs invalid A/B testing', ['ab test', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'distributions to know', 'cols': [('normal', 'USE', 'measurement error'), ('binomial', 'USE', 'success counts'),
                                                  ('poisson', 'USE', 'event rates'), ('exponential', 'USE', 'waiting times')]},
      'Four distributions cover most ML statistics: normal for measurement error, binomial for counts, Poisson for rates, exponential for waiting times. '
      'Match the data-generating process to the distribution before reaching for a test.',
      'Table of essential probability distributions', ['distributions', 'concepts']),
]

KITS['model-workflow'] = [
    S('flow',
      {'steps': [('Frame', 'metric + baseline'), ('Data', 'collect, label'), ('Train', 'iterate fast'), ('Evaluate', 'held-out'), ('Deploy', 'monitor')]},
      'The model-development workflow runs frame → data → train → evaluate → deploy as a loop, not a line. '
      'Framing picks the metric and a dumb baseline first — a model that can\'t beat the baseline isn\'t a model, it\'s a hobby.',
      'Animated flow of the model-development workflow', ['workflow', 'concepts']),
    S('concept',
      {'title': 'Leakage: the silent killer', 'lines': ['Future info in training features', 'Preprocessing fit on all data',
                                                         'Duplicate rows across splits', 'Fix: split FIRST, then transform'],
       'accent': RED},
      'The worked example\'s answer: leakage is future or test information contaminating training. '
      'Split first, fit preprocessing on train only, deduplicate across splits — validation scores that seem too good are lying.',
      'Concept box: data leakage prevention', ['leakage', 'worked example', 'pitfalls']),
    S('compare',
      {'lt': 'Train / Val / Test', 'li': ['Train: fit parameters', 'Val: tune + select', 'Test: final, touch once'],
       'rt': 'One split reused', 'ri': ['Tune on test = leakage', 'Scores inflate silently', 'Deployment surprises'],
       'left_accent': GREEN, 'right_accent': RED},
      'Three splits, three jobs: train fits, validation selects, test judges once at the end. '
      'Tuning against the test set is leakage with extra steps — the reported score stops meaning anything.',
      'Animated comparison of proper vs improper data splitting', ['splits', 'pitfalls', 'concepts']),
    S('flow',
      {'steps': [('Error analysis', 'where does it fail?'), ('Hypothesis', 'why?'), ('Fix data/model', 'targeted change'), ('Re-evaluate', 'did it help?')]},
      'Iteration is error analysis, not hyperparameter roulette: find where the model fails, hypothesize why, make one targeted change, re-evaluate. '
      'Most gains come from data fixes aimed at the worst error slice.',
      'Animated flow of the model iteration loop', ['iteration', 'error analysis', 'hands-on']),
]

KITS['sql-ai'] = [
    S('concept',
      {'title': 'Window functions', 'lines': ['OVER (PARTITION BY … ORDER BY …)', 'ROW_NUMBER: dedupe, top-N per group',
                                               'LAG/LEAD: compare to neighbors', 'Running totals without GROUP BY'],
       'accent': ACCENT},
      'Window functions compute across rows related to the current row without collapsing them — rankings, running totals, period-over-period deltas. '
      'They\'re the analytical SQL workhorse for feature engineering over event data.',
      'Concept box: SQL window functions', ['window', 'concepts']),
    S('flow',
      {'steps': [('CTE: stage', 'WITH clean AS (…)'), ('Aggregate', 'per entity'), ('Window', 'rank / lag'), ('Select', 'final features')]},
      'Build analytical queries as CTE pipelines: stage and clean, aggregate per entity, apply window functions, select the feature set. '
      'CTEs read top-to-bottom like the pipeline they are — nested subqueries don\'t.',
      'Animated flow of a CTE-based analytical query', ['cte', 'hands-on', 'concepts']),
    S('table',
      {'name': 'dataset validation queries', 'cols': [('row counts', 'CHECK', 'per partition, per day'), ('null rates', 'CHECK', 'per column vs baseline'),
                                                       ('key uniqueness', 'CHECK', 'PK dupes = 0'), ('distribution', 'CHECK', 'mean/std vs last week')]},
      'Validate datasets with SQL before training: row counts per partition, null rates per column, key uniqueness, distribution drift vs baseline. '
      'A training run on silently corrupted data is compute burned for nothing.',
      'Table of SQL dataset-validation checks', ['validation', 'data quality', 'hands-on']),
    S('compare',
      {'lt': 'Transactional SQL', 'li': ['OLTP: point lookups', 'Normalized, fast writes', 'Indexes on keys'],
       'rt': 'Analytical SQL', 'ri': ['OLAP: scans + aggregations', 'Denormalized, fast reads', 'Columnar storage'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'AI engineers live in analytical SQL: full scans, big aggregations, columnar storage — the opposite of transactional point lookups. '
      'Write for the engine you\'re on: partition pruning and column selection matter more than clever joins.',
      'Animated comparison of OLTP vs OLAP SQL', ['oltp', 'olap', 'concepts']),
]

KITS['supervised'] = [
    S('compare',
      {'lt': 'Classification', 'li': ['Predicts categories', 'Metrics: precision/recall', 'Example: spam, churn'],
       'rt': 'Regression', 'ri': ['Predicts numbers', 'Metrics: MAE/RMSE', 'Example: price, demand'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'Supervised learning splits by target type: categories get classification with precision/recall, numbers get regression with MAE/RMSE. '
      'Picking the wrong family — regressing on labels — is a framing error no tuning fixes.',
      'Animated comparison of classification vs regression', ['classification', 'regression', 'concepts']),
    S('concept',
      {'title': 'Overfitting, diagnosed', 'lines': ['Train 99%, val 70% = memorize', 'Gap = variance, not bad luck',
                                                     'Cures: more data, regularization', 'Simpler model often wins'],
       'accent': RED},
      'The worked example\'s verdict: 99% train vs 70% validation accuracy is overfitting — the model memorized training noise. '
      'More data, regularization, or a simpler model closes the gap; more training epochs widens it.',
      'Concept box: diagnosing overfitting', ['overfitting', 'worked example', 'pitfalls']),
    S('flow',
      {'steps': [('Baseline', 'dumb but honest'), ('Simple model', 'logistic/linear'), ('Validate', 'honest metric'), ('Complexify', 'only if justified')]},
      'Start with a dumb baseline, then the simplest model that could work — complexity must earn its place against validation scores. '
      'Most production wins come from better data fed to simple models, not from exotic architectures.',
      'Animated flow of model-complexity discipline', ['baseline', 'honesty', 'hands-on']),
    S('table',
      {'name': 'model families', 'cols': [('linear/logistic', 'USE', 'baseline, interpretable'), ('trees/forests', 'USE', 'tabular default'),
                                           ('gradient boosting', 'USE', 'tabular SOTA'), ('small nets', 'USE', 'unstructured data')]},
      'Default model families by data type: linear for baselines, trees and gradient boosting for tabular, neural nets for unstructured. '
      'Tabular data belongs to boosting until proven otherwise — deep learning rarely wins there.',
      'Table of supervised model families', ['models', 'concepts']),
]

KITS['unsupervised'] = [
    S('compare',
      {'lt': 'K-means', 'li': ['Spherical clusters, k chosen', 'Fast, scalable', 'Fails on odd shapes'],
       'rt': 'DBSCAN / hierarchical', 'ri': ['Arbitrary shapes, finds k', 'Handles noise explicitly', 'Slower, parameter-sensitive'],
       'left_accent': ACCENT, 'right_accent': PURPLE},
      'K-means assumes spherical clusters and a known k; DBSCAN finds arbitrary shapes and labels noise but needs density tuning. '
      'No ground truth means no accuracy score — validate clusters by stability and business sense.',
      'Animated comparison of clustering algorithms', ['clustering', 'kmeans', 'concepts']),
    S('flow',
      {'steps': [('Scale features', 'required'), ('Pick k', 'elbow / silhouette'), ('Fit', 'assign centroids'), ('Validate', 'stability check')]},
      'K-means demands scaled features — unscaled, the largest-magnitude feature decides everything. '
      'Choose k by elbow or silhouette, then validate by stability across seeds: unstable clusters aren\'t findings.',
      'Animated flow of a K-means workflow', ['kmeans', 'hands-on', 'pitfalls']),
    S('concept',
      {'title': 'PCA: variance, compressed', 'lines': ['Find directions of max variance', 'Project onto top-k components',
                                                        'Explained variance: how much kept', 'Decorrelates features'],
       'accent': CYAN},
      'PCA rotates data onto its directions of maximum variance and keeps the top few — compression that preserves signal. '
      'Check explained variance: if 2 components keep 95%, the data was effectively 2-dimensional all along.',
      'Concept box: principal component analysis', ['pca', 'concepts']),
    S('table',
      {'name': 'unsupervised tasks', 'cols': [('clustering', 'TASK', 'segment customers'), ('dimensionality', 'TASK', 'PCA, t-SNE/UMAP'),
                                               ('anomaly detection', 'TASK', 'isolation forest'), ('association', 'TASK', 'market basket')]},
      'Unsupervised learning discovers structure without labels: segments, compressions, anomalies, associations. '
      'Every result needs external validation — an interesting cluster is a hypothesis, not a conclusion.',
      'Table of unsupervised learning tasks', ['tasks', 'honesty', 'concepts']),
]

KITS['rl-intro'] = [
    S('flow',
      {'steps': [('State', 'agent observes'), ('Action', 'policy decides'), ('Reward', 'environment returns'), ('Next state', 'loop continues')]},
      'Reinforcement learning is the agent-environment loop: observe state, act by policy, receive reward, repeat. '
      'The worked example\'s QLoRA question is a distractor here — RL fundamentals are MDPs, policies, and value functions, not fine-tuning acronyms.',
      'Animated flow of the reinforcement learning loop', ['mdp', 'worked example', 'concepts']),
    S('concept',
      {'title': 'Explore vs exploit', 'lines': ['Exploit: best-known action', 'Explore: try uncertain actions',
                                                 'ε-greedy: random with prob ε', 'Decay ε as knowledge grows'],
       'accent': ORANGE},
      'Agents must balance exploiting known-good actions against exploring uncertain ones — pure exploitation never discovers better policies. '
      'ε-greedy is the starter strategy: act randomly with probability ε, greedily otherwise, decaying ε over time.',
      'Concept box: the exploration-exploitation tradeoff', ['exploration', 'concepts']),
    S('compare',
      {'lt': 'Value-based (Q-learning)', 'li': ['Learn Q(s,a) values', 'Act: argmax Q', 'Discrete actions shine'],
       'rt': 'Policy-based', 'ri': ['Learn π(a|s) directly', 'Gradient ascent on reward', 'Continuous actions shine'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'Value-based methods learn action values and act greedily; policy-based methods learn the policy directly via gradient ascent. '
      'Discrete action spaces favor Q-learning; continuous control favors policy gradients.',
      'Animated comparison of value-based vs policy-based RL', ['q-learning', 'policy gradient', 'concepts']),
    S('table',
      {'name': 'MDP elements', 'cols': [('states S', 'SET', 'what agent observes'), ('actions A', 'SET', 'what agent can do'),
                                         ('rewards R', 'SIGNAL', 'the objective, scalar'), ('γ discount', '0..1', 'present vs future')]},
      'A Markov decision process formalizes RL: states, actions, transition dynamics, rewards, and a discount factor. '
      'Reward design is the whole game — the agent optimizes exactly what you reward, including the loopholes.',
      'Table of Markov decision process elements', ['mdp', 'reward', 'pitfalls']),
]

KITS['validation'] = [
    S('concept',
      {'title': 'K-fold cross-validation', 'lines': ['Split data into k folds', 'Train on k−1, validate on 1',
                                                      'Rotate; average the scores', 'Stratify for classification'],
       'accent': ACCENT},
      'K-fold cross-validation rotates the validation fold k times and averages — every point is validated exactly once. '
      'Stratify folds for classification so each fold mirrors the class balance; unstratified folds lie on imbalanced data.',
      'Concept box: k-fold cross-validation', ['cross-validation', 'concepts']),
    S('compare',
      {'lt': 'Grid search', 'li': ['Exhaustive over the grid', 'Exponential in dimensions', 'Wastes budget on dead zones'],
       'rt': 'Random / Bayesian', 'ri': ['Samples the space', 'Scales to many params', 'Bayesian: learns from trials'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Grid search explodes combinatorially; random search samples the space more efficiently, and Bayesian optimization learns from each trial. '
      'Spend the tuning budget where it matters — learning rate and regularization first, architecture last.',
      'Animated comparison of hyperparameter search strategies', ['grid search', 'bayesian', 'concepts']),
    S('flow',
      {'steps': [('Train loss ↓', 'learning'), ('Val loss ↓', 'generalizing'), ('Val loss ↑', 'STOP HERE'), ('Overfit zone', 'memorizing')]},
      'Early stopping watches validation loss and halts when it starts rising — the cheapest regularization available. '
      'It costs nothing to implement and saves every wasted epoch after the model starts memorizing.',
      'Animated flow of early stopping', ['early stopping', 'hands-on', 'concepts']),
    S('concept',
      {'title': 'Bias–variance, operationalized', 'lines': ['Both errors high → underfit: add capacity', 'Gap large → overfit: regularize',
                                                             'Tune on validation, never test', 'Learning curves diagnose'],
       'accent': PURPLE},
      'Learning curves operationalize bias/variance: plot train and validation error against data size. '
      'Converged-and-high means bias (more capacity); gapped means variance (more data or regularization).',
      'Concept box: learning curves for diagnosis', ['learning curves', 'hands-on', 'concepts']),
]

KITS['feature-eng'] = [
    S('table',
      {'name': 'encoding categoricals', 'cols': [('one-hot', 'USE', 'low cardinality'), ('ordinal', 'USE', 'true order exists'),
                                                  ('target encoding', 'USE', 'high cardinality, CV-folded'), ('hashing', 'USE', 'huge cardinality')]},
      'Encode categoricals by cardinality: one-hot for few levels, target encoding (computed within CV folds) for many. '
      'Target encoding outside cross-validation is leakage — the encoding learns the target it\'s supposed to predict.',
      'Table of categorical encoding strategies', ['encoding', 'pitfalls', 'concepts']),
    S('compare',
      {'lt': 'Standardization', 'li': ['Zero mean, unit variance', 'For: regularized/NN models', 'Sensitive to outliers'],
       'rt': 'Normalization / robust', 'ri': ['Min-max or IQR scaling', 'For: distance models', 'Robust: median/IQR vs outliers'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'Scale features for distance- and gradient-based models: standardization for regularized/NN models, robust scaling when outliers lurk. '
      'Tree models don\'t care — skip scaling there and spend the effort on encodings.',
      'Animated comparison of feature scaling methods', ['scaling', 'concepts']),
    S('concept',
      {'title': 'The leakage traps', 'lines': ['Fit scaler on train only', 'No future timestamps as features',
                                                'No target-derived features', 'The worked example\'s answer, again'],
       'accent': RED},
      'Feature engineering\'s cardinal sin is leakage: scalers fit on all data, future information, target-derived features. '
      'The worked example keeps asking because leakage keeps happening — audit every feature\'s availability at prediction time.',
      'Concept box: feature-engineering leakage traps', ['leakage', 'worked example', 'pitfalls']),
    S('flow',
      {'steps': [('Generate', 'domain + automated'), ('Select', 'importance, correlation'), ('Validate', 'CV with pipeline'), ('Serve', 'same code path')]},
      'Engineer features inside a pipeline that runs identically in training and serving — the training/serving skew fix from the AWS module. '
      'Generate broadly, select ruthlessly, and never hand-compute in production what a pipeline computed in training.',
      'Animated flow of the feature-engineering lifecycle', ['pipeline', 'skew', 'hands-on']),
]

KITS['eval-metrics'] = [
    S('table',
      {'name': 'confusion matrix', 'cols': [('TP', 'CELL', 'predicted +, actually +'), ('FP', 'CELL', 'predicted +, actually −'),
                                             ('FN', 'CELL', 'predicted −, actually +'), ('TN', 'CELL', 'predicted −, actually −')]},
      'Every classification metric is arithmetic on these four cells: precision = TP/(TP+FP), recall = TP/(TP+FN). '
      'Memorize the matrix and the metrics become derivations, not incantations.',
      'Table of the confusion matrix', ['confusion matrix', 'concepts']),
    S('compare',
      {'lt': 'Precision', 'li': ['Of predicted +, how many right', 'Matters when FP is costly', 'Example: spam filter'],
       'rt': 'Recall', 'ri': ['Of actual +, how many found', 'Matters when FN is costly', 'Example: cancer screen'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'The worked example\'s tradeoff: precision punishes false alarms, recall punishes misses — and you can\'t maximize both. '
      'Choose by cost: false spam-foldering vs missed tumors have very different prices.',
      'Animated comparison of precision vs recall', ['precision', 'recall', 'worked example']),
    S('concept',
      {'title': 'ROC-AUC, honestly', 'lines': ['TPR vs FPR across thresholds', 'AUC = P(rank + above −)',
                                                'Inflated on imbalanced data', 'Prefer PR-AUC when positives are rare'],
       'accent': ORANGE},
      'ROC-AUC measures ranking quality across thresholds, but on imbalanced data it flatters — true negatives dominate. '
      'When positives are rare, PR-AUC tells the honest story.',
      'Concept box: ROC-AUC and its limits', ['roc', 'auc', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'regression metrics', 'cols': [('MAE', 'METRIC', 'median-like, robust'), ('RMSE', 'METRIC', 'punishes big errors'),
                                               ('R²', 'METRIC', 'variance explained'), ('MAPE', 'METRIC', 'percentage, careful near 0')]},
      'Regression metrics differ in what they punish: MAE is robust, RMSE amplifies large errors, R² reports explained variance. '
      'Match the metric to the business cost of being wrong — the choice is a business decision.',
      'Table of regression evaluation metrics', ['mae', 'rmse', 'concepts']),
]

KITS['neural'] = [
    S('flow',
      {'steps': [('Inputs x', 'features'), ('Weighted sum', 'w·x + b'), ('Activation', 'nonlinearity'), ('Output ŷ', 'prediction')]},
      'A perceptron computes a weighted sum, adds bias, and passes it through a nonlinearity — without the activation it\'s just linear regression. '
      'Stacking these units in layers is what earns the name "deep".',
      'Animated flow through a single perceptron', ['perceptron', 'concepts']),
    S('table',
      {'name': 'activations', 'cols': [('sigmoid', 'USE', 'outputs, saturates'), ('tanh', 'USE', 'zero-centered, saturates'),
                                        ('ReLU', 'USE', 'hidden default'), ('softmax', 'USE', 'multi-class outputs')]},
      'Activations inject nonlinearity: ReLU is the hidden-layer default (cheap, non-saturating for positive inputs), softmax turns logits into probabilities. '
      'Saturating activations in deep stacks cause vanishing gradients — the historical reason ReLU won.',
      'Table of activation functions', ['relu', 'softmax', 'concepts']),
    S('layers',
      {'layers': [('Output layer', 'task predictions'),
                  ('Hidden layers', 'learned representations'),
                  ('Input layer', 'raw features')]},
      'A multilayer perceptron stacks input → hidden → output layers, each transforming the representation. '
      'Depth lets later layers compose features from earlier ones — edges into shapes into objects, in the vision analogy.',
      'Animated layered diagram of an MLP', ['mlp', 'layers', 'concepts']),
    S('flow',
      {'steps': [('Forward', 'compute ŷ'), ('Loss', 'L(y, ŷ)'), ('Backward', 'gradients'), ('Step', 'update w')]},
      'The training loop in four moves: forward pass predicts, loss scores, backward pass assigns blame via the chain rule, optimizer steps the weights. '
      'Repeat for epochs — everything else in deep learning is elaboration on this loop.',
      'Animated flow of the neural training loop', ['training loop', 'concepts']),
]

KITS['backprop'] = [
    S('flow',
      {'steps': [('∂L/∂ŷ', 'loss gradient'), ('Chain rule', 'layer by layer'), ('∂L/∂w', 'every weight'), ('w − η∇', 'gradient step')]},
      'Backpropagation is the chain rule applied mechanically from output to input, computing every weight\'s influence on the loss. '
      'Automatic differentiation does the bookkeeping — your job is the architecture and the hyperparameters.',
      'Animated flow of backpropagation', ['backprop', 'chain rule', 'concepts']),
    S('compare',
      {'lt': 'SGD (+momentum)', 'li': ['One lr for all params', 'Needs tuned schedule', 'Generalizes well'],
       'rt': 'Adam / AdamW', 'ri': ['Per-param adaptive lr', 'Works out of the box', 'Slight generalization cost'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'SGD with momentum generalizes slightly better but demands learning-rate schedules; Adam adapts per-parameter and just works. '
      'AdamW fixes Adam\'s weight-decay bug — use AdamW as the default and tune the learning rate first.',
      'Animated comparison of SGD vs Adam optimizers', ['sgd', 'adam', 'concepts']),
    S('concept',
      {'title': 'Learning rate', 'lines': ['Too high: diverges, loss explodes', 'Too low: crawls, stuck in minima',
                                            'Schedule: warmup then decay', 'Tune it before anything else'],
       'accent': RED},
      'The learning rate is the highest-leverage hyperparameter: too high diverges, too low crawls. '
      'Warm up from small, decay on plateau — and tune this before touching architecture.',
      'Concept box: learning-rate selection', ['learning rate', 'pitfalls', 'hands-on']),
    S('concept',
      {'title': 'Vanishing / exploding gradients', 'lines': ['Deep stacks multiply gradients', 'Saturating activations → vanish',
                                                              'Fixes: ReLU, residuals, norm layers', 'Clip when exploding'],
       'accent': PURPLE},
      'Gradients multiply across layers: saturating activations shrink them to zero (vanishing), poor init blows them up (exploding). '
      'ReLU, residual connections, and normalization are the structural fixes — gradient clipping is the emergency brake.',
      'Concept box: vanishing and exploding gradients', ['gradients', 'concepts']),
]

KITS['cnn'] = [
    S('concept',
      {'title': 'Convolution', 'lines': ['Small kernel slides over input', 'Dot product at each position',
                                          'Detects local patterns: edges', 'Weight sharing: same kernel everywhere'],
       'accent': ACCENT},
      'Convolution slides a small learned kernel across the input, computing dot products that detect local patterns like edges. '
      'Weight sharing — one kernel everywhere — gives translation equivariance and slashes parameters vs dense layers.',
      'Concept box: the convolution operation', ['convolution', 'concepts']),
    S('flow',
      {'steps': [('Conv', 'feature maps'), ('ReLU', 'nonlinearity'), ('Pool', 'downsample'), ('Repeat', 'hierarchy')]},
      'CNNs stack conv → activation → pooling: early layers learn edges, deeper layers compose them into textures, parts, objects. '
      'Pooling downsamples for translation invariance and compute savings.',
      'Animated flow of a CNN feature hierarchy', ['cnn', 'pooling', 'concepts']),
    S('concept',
      {'title': 'Receptive field', 'lines': ['Input region affecting one unit', 'Grows with depth + stride',
                                              'Deep units "see" the whole image', 'Design: field ≥ object size'],
       'accent': CYAN},
      'A unit\'s receptive field is the input region influencing it — growing with depth, kernel size, and stride. '
      'If the field is smaller than the objects you classify, the network literally can\'t see them whole.',
      'Concept box: receptive fields', ['receptive field', 'hands-on', 'concepts']),
    S('table',
      {'name': 'classic architectures', 'cols': [('LeNet/AlexNet', 'ERA', 'proof of concept'), ('VGG', 'ERA', 'deep stacks of 3×3'),
                                                  ('ResNet', 'ERA', 'skip connections win'), ('EfficientNet', 'ERA', 'compound scaling')]},
      'CNN history in four stops: AlexNet proved depth works, VGG standardized 3×3 stacks, ResNet\'s skip connections unlocked 100+ layers, EfficientNet scaled systematically. '
      'Transfer-learn from these before training from scratch — pretrained features beat random init on small data.',
      'Table of landmark CNN architectures', ['resnet', 'transfer learning', 'concepts']),
]

KITS['seq-models'] = [
    S('flow',
      {'steps': [('x₁', 'first token'), ('h₁ → h₂ → h₃', 'hidden state carries'), ('x₂, x₃', 'sequence in'), ('y', 'output at end')]},
      'RNNs process sequences step by step, carrying a hidden state forward — the network\'s memory of what came before. '
      'That sequential dependence is also the curse: no parallelization across time steps.',
      'Animated flow of RNN sequential processing', ['rnn', 'concepts']),
    S('concept',
      {'title': 'LSTM gates', 'lines': ['Forget: what to drop', 'Input: what to store', 'Output: what to emit',
                                         'Cell state: the conveyor belt'],
       'accent': GREEN},
      'LSTMs add a cell-state conveyor belt guarded by forget, input, and output gates — learned decisions about what to remember. '
      'Gates tame the vanishing gradient enough for hundred-step dependencies, the pre-transformer state of the art.',
      'Concept box: LSTM gating mechanism', ['lstm', 'concepts']),
    S('compare',
      {'lt': 'RNNs / LSTMs', 'li': ['Sequential: slow training', 'Fixed-size memory bottleneck', 'Struggle past ~100 steps'],
       'rt': 'Attention (next module)', 'ri': ['Parallel: fast training', 'Direct long-range links', 'Scales to thousands of steps'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'RNNs bottleneck memory through one hidden vector and train sequentially; attention connects every position directly and trains in parallel. '
      'That parallelization is why attention replaced recurrence — the doorstep this module stands on.',
      'Animated comparison of recurrence vs attention', ['attention', 'concepts']),
    S('flow',
      {'steps': [('Embed tokens', 'vectors'), ('Encode sequence', 'RNN/LSTM'), ('Context vector', 'bottleneck'), ('Decode', 'generate output')]},
      'The classic seq2seq pattern: encode the input sequence into a context vector, decode it into the output sequence. '
      'Attention was born as the fix for the context-vector bottleneck — letting the decoder look back at all encoder states.',
      'Animated flow of sequence-to-sequence modeling', ['seq2seq', 'concepts']),
]

KITS['regularization'] = [
    S('compare',
      {'lt': 'L1 (lasso)', 'li': ['Penalty: Σ|w|', 'Drives weights to zero', 'Feature selection built in'],
       'rt': 'L2 (ridge)', 'ri': ['Penalty: Σw²', 'Shrinks weights smoothly', 'Keeps all features small'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'L1\'s absolute penalty zeroes out weights (automatic feature selection); L2\'s squared penalty shrinks everything smoothly. '
      'Use L1 when you suspect few features matter, L2 as the safe default.',
      'Animated comparison of L1 vs L2 regularization', ['l1', 'l2', 'concepts']),
    S('concept',
      {'title': 'Dropout', 'lines': ['Randomly zero activations in training', 'Rate ~0.2–0.5 typical',
                                      'Prevents co-adaptation', 'Off at inference (scale!)'],
       'accent': PURPLE},
      'Dropout randomly zeroes activations during training so no neuron can rely on specific partners — an ensemble of subnetworks for free. '
      'It\'s off at inference (with appropriate scaling): the worked example\'s train/eval behavior difference explained.',
      'Concept box: dropout regularization', ['dropout', 'concepts']),
    S('flow',
      {'steps': [('Augment data', 'rotate, crop, noise'), ('More effective data', 'for free'), ('Less memorization', 'variance ↓'), ('Better generalization', 'the goal')]},
      'Data augmentation manufactures training variety — crops, flips, noise — that the model can\'t memorize its way through. '
      'It\'s often the highest-ROI regularization: more effective data without more labeling.',
      'Animated flow of data augmentation', ['augmentation', 'hands-on', 'concepts']),
    S('table',
      {'name': 'hyperparameter priority', 'cols': [('learning rate', 'FIRST', 'dominates everything'), ('regularization λ', 'SECOND', 'controls variance'),
                                                    ('architecture', 'THIRD', 'after the above'), ('optimizer bells', 'LAST', 'marginal gains')]},
      'Tune in priority order: learning rate first, regularization strength second, architecture third, optimizer trivia last. '
      'Most "architecture breakthroughs" in notebooks are actually learning-rate fixes.',
      'Table of hyperparameter tuning priority', ['tuning', 'pitfalls', 'hands-on']),
]

KITS['pytorch'] = [
    S('flow',
      {'steps': [('DataLoader', 'batches'), ('model(x)', 'forward'), ('loss.backward()', 'gradients'), ('optimizer.step()', 'update')]},
      'The PyTorch training loop: DataLoader yields batches, forward pass predicts, backward() fills .grad, optimizer.step() updates. '
      'Zero the grads each iteration — forgetting zero_grad() accumulates gradients across batches silently.',
      'Animated flow of the PyTorch training loop', ['pytorch', 'training loop', 'hands-on']),
    S('concept',
      {'title': 'Autograd', 'lines': ['Tracks ops on requires_grad tensors', 'Builds the graph dynamically',
                                       'backward(): chain rule, automatic', 'no_grad(): inference, no tracking'],
       'accent': GREEN},
      'Autograd records operations on tensors requiring gradients and differentiates the dynamic graph on demand. '
      'Wrap inference in torch.no_grad() — tracking gradients you\'ll never use wastes memory and time.',
      'Concept box: PyTorch autograd', ['autograd', 'concepts']),
    S('table',
      {'name': 'tensor ops', 'cols': [('view/reshape', 'SHAPE', 'no copy when possible'), ('permute', 'SHAPE', 'reorder dims'),
                                       ('matmul/@', 'MATH', 'batched matrix multiply'), ('device', 'MOVE', '.to("cuda")')]},
      'Core tensor ops: reshape views without copying, permute reorders dimensions, @ does batched matmul, .to() moves to GPU. '
      'Keep data on the GPU across the batch — host-device transfers are the silent throughput killer.',
      'Table of essential PyTorch tensor operations', ['tensors', 'hands-on', 'pitfalls']),
    S('flow',
      {'steps': [('Dataset', 'your data'), ('DataLoader', 'batch + shuffle'), ('num_workers>0', 'parallel load'), ('pin_memory', 'fast GPU transfer')]},
      'DataLoader pipelines keep the GPU fed: parallel workers load and preprocess while the GPU trains. '
      'A starved GPU shows as low utilization with high CPU — fix the pipeline, not the model.',
      'Animated flow of the PyTorch data pipeline', ['dataloader', 'hands-on', 'pitfalls']),
]

KITS['transformers'] = [
    S('concept',
      {'title': 'Scaled dot-product attention', 'lines': ['Q: what I\'m looking for', 'K: what I offer',
                                                           'V: what I contribute', 'softmax(QKᵀ/√d)V: weighted mix'],
       'accent': ACCENT},
      'Attention in QKV terms: each position queries (Q) all positions\' keys (K) for relevance, then takes a weighted mix of values (V). '
      'The √d scaling from the frontier module keeps softmax gradients alive.',
      'Concept box: query-key-value attention', ['attention', 'qkv', 'concepts']),
    S('concept',
      {'title': 'Multi-head attention', 'lines': ['h parallel attention heads', 'Each learns different relations',
                                                   'Concat + project back', 'Syntax, coreference, position…'],
       'accent': PURPLE},
      'Multi-head attention runs several attention operations in parallel subspaces and concatenates the results. '
      'Different heads specialize — one tracks syntax, another coreference — giving the model multiple relational views at once.',
      'Concept box: multi-head attention', ['multi-head', 'concepts']),
    S('layers',
      {'layers': [('Output head', 'task predictions'),
                  ('N × (attention + MLP)', 'the repeated block'),
                  ('Embeddings + positional encoding', 'tokens + order')]},
      'The transformer stacks N identical blocks of multi-head attention plus feed-forward MLP on token embeddings. '
      'Positional encodings inject order — without them, attention is permutation-invariant and "dog bites man" equals "man bites dog".',
      'Animated layered diagram of the transformer block stack', ['transformer', 'positional', 'concepts']),
    S('compare',
      {'lt': 'Self-attention', 'li': ['Every position ↔ every position', 'O(n²) memory in length', 'The parallelization win'],
       'rt': 'Recurrence (old)', 'ri': ['Step-by-step state', 'O(n) memory, O(n) time serial', 'The bottleneck removed'],
       'left_accent': GREEN, 'right_accent': ORANGE},
      'Self-attention\'s O(n²) memory cost buys O(1) sequential steps — fully parallel training. '
      'That tradeoff is the entire reason transformers scaled: throw parallel hardware at the quadratic cost.',
      'Animated comparison of attention vs recurrence complexity', ['complexity', 'concepts']),
]

KITS['gpt-bert'] = [
    S('compare',
      {'lt': 'GPT (decoder)', 'li': ['Causal: sees only the past', 'Objective: predict next token', 'Generates text naturally'],
       'rt': 'BERT (encoder)', 'ri': ['Bidirectional: sees all', 'Objective: fill masked tokens', 'Understands, doesn\'t generate'],
       'left_accent': GREEN, 'right_accent': ACCENT},
      'The worked example\'s answer: GPT\'s causal decoder suits generation (predict the next token); BERT\'s bidirectional encoder suits understanding (classify, extract). '
      'Architecture follows objective — pick the family by the task.',
      'Animated comparison of GPT vs BERT', ['gpt', 'bert', 'worked example', 'concepts']),
    S('concept',
      {'title': 'Causal masking', 'lines': ['Upper triangle masked to −∞', 'Position i sees only ≤ i',
                                             'Enables parallel training', 'Inference: cache KVs, decode step by step'],
       'accent': ORANGE},
      'Causal masking hides future positions so training can process all tokens in parallel while preserving autoregressive order. '
      'At inference, KV-caching avoids recomputing past keys and values — the latency optimization behind fast generation.',
      'Concept box: causal masking and KV caching', ['masking', 'kv-cache', 'concepts']),
    S('concept',
      {'title': 'Masked language modeling', 'lines': ['Mask 15% of tokens', 'Predict them from both sides',
                                                       'Deep bidirectional context', 'Great for classification/NER'],
       'accent': CYAN},
      'BERT masks random tokens and predicts them using both directions of context — deep bidirectional understanding. '
      'That bidirectionality is why encoders dominate classification, NER, and retrieval while decoders dominate generation.',
      'Concept box: BERT masked language modeling', ['bert', 'mlm', 'concepts']),
    S('table',
      {'name': 'family → task', 'cols': [('generation', 'PICK', 'GPT-style decoder'), ('classification', 'PICK', 'BERT-style encoder'),
                                          ('embeddings', 'PICK', 'encoder or dedicated'), ('chat/agent', 'PICK', 'instruction-tuned decoder')]},
      'Match the family to the task: decoders generate, encoders understand, instruction-tuned decoders chat. '
      'Using a 70B chat model for classification is paying generation prices for an encoder\'s job.',
      'Table mapping task types to model families', ['task', 'pitfalls', 'concepts']),
]

KITS['gan-vae'] = [
    S('flow',
      {'steps': [('Generator', 'fake samples'), ('Discriminator', 'real vs fake?'), ('Adversarial loss', 'compete'), ('Equilibrium', 'fakes fool D')]},
      'GANs pit a generator against a discriminator: G crafts fakes, D judges them, and the competition drives both upward. '
      'Training is a game seeking equilibrium — which is why it\'s notoriously unstable compared to likelihood-based models.',
      'Animated flow of GAN adversarial training', ['gan', 'concepts']),
    S('concept',
      {'title': 'VAE: latent structure', 'lines': ['Encoder → latent distribution', 'Sample z, decode to output',
                                                    'KL term: keep latent sane', 'Smooth latent space: interpolate'],
       'accent': PURPLE},
      'Variational autoencoders compress inputs into a regularized latent distribution you can sample and interpolate. '
      'The KL term keeps the latent space smooth — nearby points decode to similar outputs, enabling meaningful morphing.',
      'Concept box: VAE latent space', ['vae', 'latent', 'concepts']),
    S('compare',
      {'lt': 'GANs', 'li': ['Sharpest samples', 'Unstable training', 'Mode collapse risk'],
       'rt': 'VAEs / Diffusion', 'ri': ['Stable likelihood training', 'Blurrier (VAE) / slow (diffusion)', 'Better coverage'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'GANs win sample sharpness but suffer mode collapse — generating limited variety; VAEs and diffusion train stably with better mode coverage. '
      'Diffusion largely displaced GANs for image generation by combining sharpness with stability.',
      'Animated comparison of generative model families', ['mode collapse', 'honesty', 'concepts']),
    S('concept',
      {'title': 'Mode collapse', 'lines': ['Generator finds one fooling sample', 'Outputs lose diversity',
                                            'Discriminator can\'t punish variety', 'Watch: sample diversity metrics'],
       'accent': RED},
      'Mode collapse: the generator discovers a few samples that fool the discriminator and stops exploring. '
      'Outputs look great individually but lack diversity — monitor sample-diversity metrics, not just sample quality.',
      'Concept box: GAN mode collapse', ['mode collapse', 'pitfalls', 'concepts']),
]

KITS['diffusion'] = [
    S('flow',
      {'steps': [('Clean image', 'x₀'), ('Add noise', 't steps forward'), ('Pure noise', 'x_T'), ('Denoise', 'learned reverse')]},
      'Diffusion models learn by reversing a fixed noising process: gradually add Gaussian noise until the image is pure static, then train a network to denoise step by step. '
      'Generation runs the learned reverse process from noise to image.',
      'Animated flow of the diffusion forward/reverse process', ['diffusion', 'concepts']),
    S('concept',
      {'title': 'The noise schedule', 'lines': ['βₜ: how much noise per step', 'Too fast: unlearnable jumps',
                                                 'Too slow: wasted steps', 'Cosine schedule: the modern default'],
       'accent': CYAN},
      'The noise schedule controls how fast signal becomes noise across timesteps — too aggressive and denoising steps are unlearnable, too gentle and steps are wasted. '
      'Cosine schedules spend more steps at informative noise levels.',
      'Concept box: diffusion noise schedules', ['noise schedule', 'hands-on', 'concepts']),
    S('concept',
      {'title': 'UNet: the denoiser', 'lines': ['Encoder: downsample, capture context', 'Bottleneck: global structure',
                                                 'Decoder: upsample, skip connections', 'Predicts the noise, not the image'],
       'accent': ACCENT},
      'The denoising network is typically a UNet: downsampling encoder, bottleneck, upsampling decoder with skip connections preserving detail. '
      'It predicts the noise to remove at each step — predicting noise turns out more stable than predicting pixels.',
      'Concept box: the UNet denoiser', ['unet', 'concepts']),
    S('flow',
      {'steps': [('Text prompt', 'conditioning'), ('Noise', 'random start'), ('Guided denoise', 'classifier-free guidance'), ('Image/video', 'sample')]},
      'Text conditioning steers denoising via cross-attention on prompt embeddings; classifier-free guidance trades diversity for prompt adherence. '
      'Video adds temporal attention across frames — same idea, one more dimension.',
      'Animated flow of text-conditioned generation', ['conditioning', 'guidance', 'concepts']),
]

KITS['prompt-eng'] = [
    S('concept',
      {'title': 'Prompt anatomy', 'lines': ['Role: who the model plays', 'Task: what to do, precisely',
                                             'Context: the facts it needs', 'Format: how to shape output'],
       'accent': ACCENT},
      'Effective prompts have four parts: role (perspective), task (precise instruction), context (the facts), format (output shape). '
      'Most "prompt failures" are missing context or vague tasks — the model can\'t use what you didn\'t provide.',
      'Concept box: prompt anatomy', ['prompt', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Zero-shot', 'li': ['Instruction only', 'Fast, cheap', 'Fails on novel formats'],
       'rt': 'Few-shot', 'ri': ['Instruction + examples', 'Shows the pattern', 'Costs tokens per example'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Few-shot prompting demonstrates the pattern with examples instead of describing it — dramatically more reliable for formats and edge cases. '
      'Pay the token cost for examples on anything the model must get exactly right.',
      'Animated comparison of zero-shot vs few-shot prompting', ['few-shot', 'concepts']),
    S('concept',
      {'title': 'Chain-of-thought', 'lines': ['"Think step by step"', 'Decomposes the reasoning',
                                               'Errors become inspectable', 'Verify the steps, not just the answer'],
       'accent': PURPLE},
      'Chain-of-thought prompting asks the model to reason stepwise before answering — improving accuracy on multi-step problems and making errors inspectable. '
      'Verify the steps: fluent reasoning can still conclude wrongly.',
      'Concept box: chain-of-thought prompting', ['chain-of-thought', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'system prompt levers', 'cols': [('role + audience', 'LEVER', 'calibrates tone/depth'), ('constraints', 'LEVER', '"no new deps"'),
                                                 ('output schema', 'LEVER', 'JSON shape specified'), ('refusal policy', 'LEVER', 'what to decline')]},
      'System prompts set the persistent contract: role and audience calibrate depth, constraints bound behavior, schemas fix output shape. '
      'Put invariants in the system prompt and variables in the user message — separation the model actually respects.',
      'Table of system-prompt design levers', ['system prompt', 'hands-on', 'concepts']),
]

KITS['rag'] = [
    S('flow',
      {'steps': [('Query', 'user asks'), ('Retrieve', 'top-k chunks'), ('Augment', 'context + query'), ('Generate', 'grounded answer')]},
      'RAG grounds generation in retrieved documents: embed the query, fetch top-k chunks, stuff them into context, generate with citations. '
      'The worked example\'s rule: choose RAG when knowledge changes fast or must be cited — fine-tuning bakes in stale facts.',
      'Animated flow of the RAG pipeline', ['rag', 'worked example', 'concepts']),
    S('compare',
      {'lt': 'RAG', 'li': ['Knowledge in documents', 'Update: re-index', 'Cites sources'],
       'rt': 'Fine-tuning', 'ri': ['Knowledge in weights', 'Update: retrain', 'Behavior/style change'],
       'left_accent': GREEN, 'right_accent': ACCENT},
      'RAG for changing knowledge and citations; fine-tuning for behavior, style, and domain format. '
      'They compose — fine-tune the behavior, RAG the facts — but don\'t fine-tune what a document index can answer.',
      'Animated comparison of RAG vs fine-tuning', ['rag', 'fine-tune', 'concepts']),
    S('concept',
      {'title': 'Chunking', 'lines': ['~200–500 tokens typical', 'Overlap 10–20%: don\'t split ideas',
                                       'Respect structure: sections, not chars', 'Bad chunks = bad retrieval'],
       'accent': ORANGE},
      'Chunking decides what retrieval can find: respect document structure, overlap boundaries so ideas aren\'t split, size for the embedding model\'s sweet spot. '
      'Most "RAG doesn\'t work" complaints are chunking complaints.',
      'Concept box: document chunking strategy', ['chunking', 'pitfalls', 'hands-on']),
    S('table',
      {'name': 'RAG evaluation', 'cols': [('retrieval hit@k', 'METRIC', 'is the answer in context?'), ('faithfulness', 'METRIC', 'claims ← sources?'),
                                           ('answer relevance', 'METRIC', 'answers the question?'), ('latency/cost', 'METRIC', 'per query budget')]},
      'Evaluate RAG as two systems: retrieval (is the answer in the context?) and generation (are claims faithful to sources?). '
      'Faithfulness — every claim traceable to a chunk — is the metric that matters for trust.',
      'Table of RAG evaluation metrics', ['evaluation', 'faithfulness', 'concepts']),
]

KITS['vecdb'] = [
    S('flow',
      {'steps': [('Embed query', 'vector'), ('ANN search', 'approximate neighbors'), ('Filter', 'metadata constraints'), ('Rerank', 'precise top-k')]},
      'Vector search: embed the query, run approximate nearest-neighbor search over the index, apply metadata filters, rerank the candidates precisely. '
      'The worked example\'s precision/recall framing applies — ANN trades a little recall for massive speed.',
      'Animated flow of vector search', ['vector search', 'ann', 'worked example']),
    S('concept',
      {'title': 'HNSW: navigable graphs', 'lines': ['Layered proximity graph', 'Greedy walk from top layer',
                                                     'Logarithmic search hops', 'The default ANN index'],
       'accent': ACCENT},
      'HNSW builds layered graphs where greedy walks descend from coarse to fine layers — logarithmic hops to near neighbors. '
      'It\'s the default ANN index for good reason: excellent recall/latency tradeoff with modest build cost.',
      'Concept box: HNSW indexing', ['hnsw', 'concepts']),
    S('compare',
      {'lt': 'Flat / brute force', 'li': ['Exact recall', 'O(n) per query', 'Small collections only'],
       'rt': 'HNSW / IVF', 'ri': ['~99% recall typical', 'Sub-linear queries', 'Production scale'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Brute-force search is exact but linear per query — fine for thousands of vectors, hopeless for millions. '
      'HNSW/IVF trade a point or two of recall for orders of magnitude in speed; tune ef_search for your recall target.',
      'Animated comparison of exact vs approximate vector search', ['ann', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'index choices', 'cols': [('HNSW', 'USE', 'general default'), ('IVF-PQ', 'USE', 'memory-constrained billion-scale'),
                                          ('metadata filter', 'USE', 'pre/post-filter by attrs'), ('hybrid', 'USE', 'dense + BM25')]},
      'Choose the index by scale: HNSW as the default, IVF-PQ when billions of vectors must fit in RAM, hybrid dense+sparse when keywords matter. '
      'Metadata filtering (tenant, date) belongs in the query, not in separate indexes per tenant.',
      'Table of vector index selection', ['index', 'hands-on', 'concepts']),
]

KITS['adv-retrieval'] = [
    S('concept',
      {'title': 'GraphRAG', 'lines': ['Extract entities + relations', 'Build a knowledge graph',
                                       'Retrieve subgraphs, not chunks', 'Multi-hop questions answered'],
       'accent': PURPLE},
      'GraphRAG extracts entities and relationships into a knowledge graph, then retrieves connected subgraphs instead of isolated chunks. '
      'Multi-hop questions — "which supplier\'s delay caused the outage?" — need the graph\'s connections, not chunk similarity.',
      'Concept box: GraphRAG', ['graphrag', 'concepts']),
    S('flow',
      {'steps': [('Decompose', 'sub-questions'), ('Retrieve each', 'targeted'), ('Judge gaps', 'what\'s missing?'), ('Iterate', 'until sufficient')]},
      'Agentic retrieval decomposes hard questions into sub-questions, retrieves for each, judges what\'s still missing, and iterates. '
      'The retriever becomes a reasoning loop instead of a single lookup — slower, far more capable.',
      'Animated flow of agentic retrieval', ['agentic', 'concepts']),
    S('compare',
      {'lt': 'Single-shot retrieval', 'li': ['One query, one fetch', 'Fast, cheap', 'Fails on complex questions'],
       'rt': 'Agentic retrieval', 'ri': ['Reason + multi-fetch', 'Slower, costlier', 'Handles multi-hop'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Single-shot retrieval answers lookup questions; agentic retrieval answers research questions. '
      'Route by complexity — agentic loops on simple queries waste latency and money for no gain.',
      'Animated comparison of retrieval strategies', ['pitfalls', 'hands-on', 'concepts']),
    S('table',
      {'name': 'retrieval upgrades', 'cols': [('reranking', 'ADD', 'cross-encoder on top-k'), ('HyDE', 'ADD', 'hypothetical doc embedding'),
                                               ('query rewrite', 'ADD', 'LLM expands the query'), ('hybrid', 'ADD', 'dense + BM25 fusion')]},
      'Upgrade retrieval incrementally: hybrid dense+sparse first, then reranking, then query rewriting. '
      'Measure hit@k after each addition — upgrades that don\'t move the metric are complexity without value.',
      'Table of advanced retrieval techniques', ['rerank', 'hyde', 'hands-on']),
]

KITS['finetune'] = [
    S('concept',
      {'title': 'LoRA', 'lines': ['Freeze base weights W', 'Learn low-rank ΔW = BA',
                                   'Rank r ≪ d: tiny update', 'Swap adapters per task'],
       'accent': ACCENT},
      'LoRA freezes the base model and learns a low-rank update ΔW = BA — a tiny fraction of parameters. '
      'Adapters swap per task on one shared base, making multi-tenant fine-tuning storage-feasible.',
      'Concept box: LoRA parameter-efficient fine-tuning', ['lora', 'concepts']),
    S('concept',
      {'title': 'QLoRA adds quantization', 'lines': ['Base model in 4-bit (NF4)', 'LoRA adapters in 16-bit',
                                                      'The worked example\'s answer', 'Fine-tune 65B on one GPU'],
       'accent': GREEN},
      'The worked example\'s answer: QLoRA adds 4-bit quantization of the frozen base on top of LoRA — adapters stay precise while the base shrinks. '
      'That combination fits 65B-class fine-tuning on a single GPU.',
      'Concept box: QLoRA', ['qlora', 'worked example', 'concepts']),
    S('compare',
      {'lt': 'Full fine-tuning', 'li': ['All weights update', 'Needs serious GPU RAM', 'Catastrophic forgetting risk'],
       'rt': 'PEFT (LoRA/QLoRA)', 'ri': ['<1% params update', 'Consumer-GPU feasible', 'Base knowledge preserved'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Full fine-tuning updates everything at full GPU cost and risks forgetting; PEFT updates a low-rank adapter cheaply while the base stays intact. '
      'Default to PEFT — full fine-tuning is for when adapters demonstrably underperform.',
      'Animated comparison of full vs parameter-efficient fine-tuning', ['peft', 'pitfalls', 'concepts']),
    S('flow',
      {'steps': [('Curate data', 'quality > quantity'), ('Format', 'instruction pairs'), ('Train adapter', 'LoRA/QLoRA'), ('Evaluate', 'vs base + RAG')]},
      'Fine-tuning data curation beats volume: a few thousand excellent instruction pairs outperform a million noisy ones. '
      'Evaluate against the base model and against RAG — fine-tune only what retrieval can\'t answer.',
      'Animated flow of the fine-tuning workflow', ['data', 'evaluation', 'hands-on']),
]

KITS['multimodal'] = [
    S('concept',
      {'title': 'CLIP: contrastive alignment', 'lines': ['Image encoder + text encoder', 'Contrastive: match pairs, repel others',
                                                         'Shared embedding space', 'Zero-shot classification via text'],
       'accent': ACCENT},
      'CLIP trains image and text encoders contrastively so matching pairs align in a shared space. '
      'That alignment enables zero-shot classification — describe the classes in text, no training images needed.',
      'Concept box: CLIP contrastive learning', ['clip', 'concepts']),
    S('compare',
      {'lt': 'Early fusion', 'li': ['Concatenate raw inputs', 'One model sees all', 'Simple, modality imbalance'],
       'rt': 'Late / cross-attention fusion', 'ri': ['Encode separately, fuse deep', 'Attention bridges modalities', 'Standard for VLMs'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Early fusion concatenates raw modalities; late fusion encodes each separately and joins them with cross-attention. '
      'Modern vision-language models use late fusion — modalities keep their specialized encoders.',
      'Animated comparison of multimodal fusion strategies', ['fusion', 'concepts']),
    S('flow',
      {'steps': [('Image', 'ViT patches'), ('Text', 'token embeddings'), ('Cross-attention', 'align + fuse'), ('Answer', 'grounded output')]},
      'A vision-language model patches the image through a ViT, embeds the text, fuses via cross-attention, and generates grounded in both. '
      'The image tokens join the same sequence the language model reasons over.',
      'Animated flow through a vision-language model', ['vlm', 'concepts']),
    S('table',
      {'name': 'modality encoders', 'cols': [('vision', 'ENCODER', 'ViT / CLIP-ViT'), ('audio', 'ENCODER', 'Whisper encoder'),
                                              ('video', 'ENCODER', 'frame + temporal'), ('fusion', 'POINT', 'cross-attention layers')]},
      'Each modality gets its specialist encoder — ViT for images, Whisper for audio — fused through cross-attention into the language backbone. '
      'Don\'t train encoders from scratch when aligned pretrained ones exist.',
      'Table of multimodal encoder choices', ['encoders', 'hands-on', 'concepts']),
]

KITS['vision-speech'] = [
    S('compare',
      {'lt': 'Classification', 'li': ['One label per image', 'Softmax over classes', 'Simplest vision task'],
       'rt': 'Detection / segmentation', 'ri': ['Boxes or masks per object', 'Localize + classify', 'Autonomous driving, medical'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'Classification names the image; detection draws boxes around objects; segmentation labels every pixel. '
      'Each step up buys spatial precision at the cost of annotation effort — label budgets decide the task.',
      'Animated comparison of vision task types', ['detection', 'segmentation', 'concepts']),
    S('flow',
      {'steps': [('Audio', 'waveform'), ('Features', 'mel spectrogram'), ('Encoder', 'Whisper'), ('Transcript', 'text out')]},
      'Modern ASR: convert audio to mel spectrograms, encode with a transformer like Whisper, decode to text. '
      'Pretrained multilingual ASR beats custom pipelines for nearly every application — fine-tune on your accent domain instead.',
      'Animated flow of automatic speech recognition', ['asr', 'whisper', 'concepts']),
    S('concept',
      {'title': 'Vision transformers', 'lines': ['Image → 16×16 patches', 'Patches = tokens',
                                                  'Self-attention over patches', 'Scales better than CNNs at size'],
       'accent': PURPLE},
      'Vision transformers slice images into patches, treat them as tokens, and apply the same attention machinery as language. '
      'At large data scale they surpass CNNs — the architecture converged across modalities.',
      'Concept box: vision transformers', ['vit', 'concepts']),
    S('table',
      {'name': 'applied stack', 'cols': [('detection', 'MODEL', 'YOLO / DETR'), ('ocr', 'MODEL', 'TrOCR / cloud APIs'),
                                          ('speech→text', 'MODEL', 'Whisper'), ('text→speech', 'MODEL', 'neural TTS')]},
      'The applied stack is pretrained components composed: YOLO/DETR for detection, Whisper for transcription, neural TTS for speech. '
      'Compose before training — custom vision/speech models are a last resort, not a starting point.',
      'Table of applied vision and speech models', ['yolo', 'tts', 'hands-on']),
]

KITS['alignment'] = [
    S('flow',
      {'steps': [('SFT', 'instruction tune'), ('Preferences', 'human rankings'), ('Reward model', 'learn preferences'), ('PPO', 'optimize policy')]},
      'RLHF pipelines: supervised fine-tune on instructions, collect human preference rankings, train a reward model on them, optimize the policy with PPO. '
      'Each stage can fail independently — reward hacking usually means the reward model learned a loophole.',
      'Animated flow of the RLHF pipeline', ['rlhf', 'ppo', 'concepts']),
    S('concept',
      {'title': 'DPO: skip the reward model', 'lines': ['Direct preference loss', 'No PPO, no reward model',
                                                        'Simpler and more stable', 'From the fine-tuning module'],
       'accent': GREEN},
      'DPO optimizes the policy directly on preference pairs with a classification-style loss — no reward model, no PPO. '
      'It\'s the pragmatic default for preference alignment; reserve full RLHF for when exploration genuinely matters.',
      'Concept box: direct preference optimization', ['dpo', 'concepts']),
    S('compare',
      {'lt': 'Reward hacking', 'li': ['High reward, wrong behavior', 'Spec gaming the RM', 'Goodhart\'s law live'],
       'rt': 'Genuine alignment', 'ri': ['Reward tracks intent', 'Evaluate on held-out tasks', 'Red-team the policy'],
       'left_accent': RED, 'right_accent': GREEN},
      'Reward hacking is Goodhart\'s law in action: the policy maximizes the proxy while violating the intent. '
      'Evaluate on held-out tasks the reward model never saw, and red-team for the hacks before users find them.',
      'Animated comparison of reward hacking vs genuine alignment', ['reward hacking', 'pitfalls', 'concepts']),
    S('flow',
      {'steps': [('Base model', 'pretrained'), ('Reasoning training', 'RL on verifiable tasks'), ('Long CoT', 'test-time compute'), ('o1-style', 'think longer')]},
      'Reasoning models shift compute to test time: RL on verifiable tasks (math, code) teaches long chain-of-thought. '
      'The paradigm move — performance scales with thinking time, not just parameters.',
      'Animated flow of reasoning-model training', ['reasoning', 'test-time', 'concepts']),
]

KITS['text-prep'] = [
    S('flow',
      {'steps': [('Raw text', 'as collected'), ('Clean', 'strip HTML, normalize'), ('Normalize', 'case, unicode'), ('Filter', 'language, quality')]},
      'Preprocessing pipelines clean (strip markup), normalize (case, unicode forms), and filter (language, quality) before any modeling. '
      'Garbage in isn\'t a metaphor — encoding mojibake in training data becomes mojibake in outputs.',
      'Animated flow of the text-cleaning pipeline', ['cleaning', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Stemming', 'li': ['Crude suffix chopping', 'Fast: "running" → "run"', 'Errors: "university" → "univers"'],
       'rt': 'Lemmatization', 'ri': ['Dictionary-aware base form', 'Slower, accurate', '"better" → "good"'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Stemming chops suffixes fast and crudely; lemmatization consults morphology for the true base form. '
      'For modern embeddings both matter less — subword tokenization handles morphology — but classic pipelines still choose deliberately.',
      'Animated comparison of stemming vs lemmatization', ['stemming', 'lemmatization', 'concepts']),
    S('concept',
      {'title': 'Stopwords: handle with care', 'lines': ['"the", "is", "at" — frequent, low signal', 'Removing helps classic IR',
                                                          'Hurts: "to be or not to be"', 'Embeddings: usually keep'],
       'accent': ORANGE},
      'Stopword removal helps classic bag-of-words models focus on content words but destroys phrases like "to be or not to be". '
      'Neural models with subword tokenization generally keep stopwords — context needs them.',
      'Concept box: stopword trade-offs', ['stopwords', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'normalization decisions', 'cols': [('lowercasing', 'CHOICE', 'usually yes, careful with NER'), ('unicode NFKC', 'CHOICE', 'yes: café = café'),
                                                    ('punctuation', 'CHOICE', 'task-dependent'), ('contractions', 'CHOICE', 'expand for classic models')]},
      'Normalization is a set of task-dependent choices: lowercase usually, unicode-normalize always, punctuation and contractions by task. '
      'Document every choice — preprocessing mismatches between train and serve are silent killers.',
      'Table of text-normalization decisions', ['normalization', 'pitfalls', 'hands-on']),
]

KITS['tokenization'] = [
    S('concept',
      {'title': 'BPE: learn the merges', 'lines': ['Start: characters', 'Merge most frequent pair',
                                                    'Repeat to vocab size', 'Frequent words = one token'],
       'accent': ACCENT},
      'Byte-pair encoding starts from characters and repeatedly merges the most frequent adjacent pair until the vocabulary fills. '
      'Frequent words become single tokens; rare words decompose into pieces — no out-of-vocabulary ever.',
      'Concept box: byte-pair encoding', ['bpe', 'concepts']),
    S('compare',
      {'lt': 'Word tokens', 'li': ['Huge vocab, OOV problem', 'Clean linguistic units', 'Fails on typos, new words'],
       'rt': 'Subword tokens', 'ri': ['Fixed vocab, no OOV', '"unhappiness" → un+happi+ness', 'The modern standard'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Word tokenization breaks on anything unseen; subword tokenization decomposes unknowns into known pieces. '
      'Subwords won because open-vocabulary generation can\'t afford an <UNK> token.',
      'Animated comparison of word vs subword tokenization', ['subword', 'oov', 'concepts']),
    S('table',
      {'name': 'embedding matrix', 'cols': [('rows', 'DIM', 'vocab_size, e.g. 50k'), ('cols', 'DIM', 'd_model, e.g. 4096'),
                                             ('lookup', 'OP', 'token id → row vector'), ('trained', 'FACT', 'with the model')]},
      'The embedding matrix maps each token id to a dense vector — vocab_size rows, d_model columns, learned with the model. '
      'It\'s a lookup table, not a computation: token 42 always fetches row 42.',
      'Table of the token-embedding matrix', ['embeddings', 'concepts']),
    S('concept',
      {'title': 'Token ≠ word', 'lines': ['"tokenization" ≈ 3–4 tokens', 'Cost math: per 1k tokens',
                                           'Context limits count tokens', 'Multilingual: fertility varies'],
       'accent': ORANGE},
      'Budgets and context windows count tokens, not words — English averages ~0.75 words per token, other languages differ. '
      'Estimate costs and fit in tokens; "words" is a user-interface fiction.',
      'Concept box: tokens vs words for budgeting', ['tokens', 'cost', 'pitfalls']),
]

KITS['nltk'] = [
    S('flow',
      {'steps': [('Tokenize', 'sent_tokenize'), ('Tag', 'POS tags'), ('Chunk', 'NP/VP phrases'), ('Classify', 'Naive Bayes')]},
      'The classic NLTK pipeline: sentence-tokenize, POS-tag, chunk phrases, then classify with something like Naive Bayes. '
      'Every stage is inspectable — the pedagogical value modern end-to-end models hide.',
      'Animated flow of the classic NLTK pipeline', ['nltk', 'pipeline', 'concepts']),
    S('table',
      {'name': 'POS tags (Penn)', 'cols': [('NN / NNS', 'NOUN', 'singular / plural'), ('VB*', 'VERB', 'base, past, gerund…'),
                                            ('JJ', 'ADJECTIVE', 'modifiers'), ('RB', 'ADVERB', '"quickly"')]},
      'Part-of-speech tags label each token\'s grammatical role — the feature set behind classic chunking and information extraction. '
      'Read a tagged sentence once and the "grammar as features" idea clicks permanently.',
      'Table of Penn Treebank POS tags', ['pos', 'concepts']),
    S('concept',
      {'title': 'Naive Bayes for text', 'lines': ['P(class|words) ∝ P(class)·Π P(word|class)', '"Naive": words independent',
                                                   'Works shockingly well for spam', 'Baseline every classifier beats'],
       'accent': GREEN},
      'Naive Bayes multiplies per-word likelihoods under a bold independence assumption — and still classifies spam brilliantly. '
      'It\'s the baseline every fancier classifier must beat to justify its complexity.',
      'Concept box: Naive Bayes text classification', ['naive bayes', 'concepts']),
    S('compare',
      {'lt': 'Classic NLP (NLTK)', 'li': ['Interpretable stages', 'Small data friendly', 'Feature engineering heavy'],
       'rt': 'Neural NLP', 'ri': ['End-to-end learning', 'Data hungry', 'Embeddings do the work'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'Classic NLP teaches the linguistic concepts — tokenization, tagging, parsing — that neural models internalize opaquely. '
      'Learn the concepts here; apply them with transformers in production.',
      'Animated comparison of classic vs neural NLP', ['honesty', 'concepts']),
]

KITS['seq-nlp'] = [
    S('flow',
      {'steps': [('Input text', 'tokens'), ('Embed', 'vectors'), ('Encode', 'RNN/Transformer'), ('Decode', 'generate / classify')]},
      'Sequence models for language: embed tokens, encode the sequence, decode to the task — translation, summarization, classification. '
      'The encoder-decoder pattern predates transformers and still describes them.',
      'Animated flow of neural sequence modeling for language', ['seq2seq', 'concepts']),
    S('concept',
      {'title': 'Language modeling objective', 'lines': ['P(w₁…wₙ) = Π P(wᵢ|w<ᵢ)', 'Next-token prediction',
                                                          'Perplexity: exp(avg NLL)', 'Lower = better model of text'],
       'accent': ACCENT},
      'Language modeling factorizes text probability into next-token predictions; perplexity (exponentiated average negative log-likelihood) scores the model. '
      'Every LLM capability traces back to this one objective scaled up.',
      'Concept box: the language-modeling objective', ['perplexity', 'concepts']),
    S('compare',
      {'lt': 'Greedy decoding', 'li': ['Argmax each step', 'Fast, deterministic', 'Repetitive, myopic'],
       'rt': 'Sampling (top-k/p)', 'ri': ['Sample from distribution', 'Diverse, creative', 'Temperature controls risk'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Greedy decoding takes the argmax every step — fast but repetitive; sampling (top-k/top-p) draws from the distribution for diversity. '
      'Temperature sharpens or flattens the distribution: low for facts, higher for creativity.',
      'Animated comparison of text-decoding strategies', ['decoding', 'temperature', 'hands-on']),
    S('table',
      {'name': 'generation controls', 'cols': [('temperature', 'KNOB', 'randomness 0–2'), ('top-p', 'KNOB', 'nucleus cutoff'),
                                                ('max tokens', 'KNOB', 'budget + stop'), ('stop sequences', 'KNOB', 'format control')]},
      'Control generation with four knobs: temperature for randomness, top-p for nucleus cutoff, max tokens for budget, stop sequences for format. '
      'Deterministic tasks want temperature 0 — creativity is a bug in extraction pipelines.',
      'Table of text-generation controls', ['sampling', 'pitfalls', 'hands-on']),
]

KITS['hf'] = [
    S('flow',
      {'steps': [('pipeline()', 'one-line task'), ('model + tokenizer', 'explicit control'), ('Trainer', 'fine-tune loop'), ('push_to_hub', 'share')]},
      'Hugging Face\'s ladder: pipeline() for instant inference, explicit model+tokenizer for control, Trainer for fine-tuning, push_to_hub to share. '
      'Climb only as far as the task needs — pipeline() covers most demos.',
      'Animated flow of the Hugging Face workflow', ['huggingface', 'pipeline', 'hands-on']),
    S('concept',
      {'title': 'The Hub', 'lines': ['Models: versioned, carded', 'Datasets: versioned, scripted',
                                      'Spaces: hosted demos', 'Model cards: read before use'],
       'accent': ACCENT},
      'The Hub hosts versioned models, datasets, and Spaces demos — but quality varies wildly. '
      'Read the model card (training data, evals, license) before building on anything; downloads count isn\'t due diligence.',
      'Concept box: the Hugging Face Hub', ['hub', 'model card', 'pitfalls']),
    S('table',
      {'name': 'pipeline tasks', 'cols': [('sentiment-analysis', 'TASK', 'classifier'), ('summarization', 'TASK', 'seq2seq'),
                                           ('question-answering', 'TASK', 'extractive'), ('text-generation', 'TASK', 'causal LM')]},
      'pipeline() names the task and handles tokenization, inference, and decoding — the fastest path from idea to working demo. '
      'Specify the model explicitly in production; defaults change.',
      'Table of Hugging Face pipeline tasks', ['pipeline', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'pipeline() default', 'li': ['Fastest to demo', 'Hidden model choice', 'Fine for prototypes'],
       'rt': 'Explicit model + Trainer', 'ri': ['You choose the checkpoint', 'Reproducible, tunable', 'Production path'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Prototypes can ride pipeline() defaults; production pins explicit checkpoints and trains with the Trainer API. '
      'Implicit model selection is tech debt — someone\'s default update becomes your behavior change.',
      'Animated comparison of HF usage patterns', ['pitfalls', 'honesty', 'hands-on']),
]

KITS['agent-arch'] = [
    S('flow',
      {'steps': [('Goal', 'user intent'), ('Plan', 'decompose'), ('Act', 'tools'), ('Reflect', 'check progress')]},
      'Agent architectures loop goal → plan → act → reflect: decompose the objective, execute tools, check progress, replan. '
      'Reflection is what separates agents from scripts — the loop notices when the plan isn\'t working.',
      'Animated flow of the agent architecture loop', ['agents', 'concepts']),
    S('concept',
      {'title': 'ReAct, precisely', 'lines': ['Thought: reason about state', 'Action: call a tool',
                                               'Observation: read the result', 'From the IL-07 agents module'],
       'accent': ACCENT},
      'ReAct interleaves thoughts, actions, and observations in the prompt itself — no special architecture, just a disciplined format. '
      'It remains the baseline every fancier agent pattern must beat.',
      'Concept box: the ReAct pattern', ['react', 'concepts']),
    S('compare',
      {'lt': 'Single agent', 'li': ['One loop, one context', 'Simple, debuggable', 'Context limits bind'],
       'rt': 'Multi-agent', 'ri': ['Specialists coordinate', 'Scales complexity', 'Coordination overhead'],
       'left_accent': GREEN, 'right_accent': ORANGE},
      'Single agents are debuggable and sufficient for most tasks; multi-agent systems parallelize specialized roles at coordination cost. '
      'Default to one agent — add a second only when the context or skill split demands it.',
      'Animated comparison of single vs multi-agent systems', ['multi-agent', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'memory types', 'cols': [('working', 'SCOPE', 'current context'), ('episodic', 'SCOPE', 'past trajectories'),
                                         ('semantic', 'SCOPE', 'facts in a store'), ('procedural', 'SCOPE', 'skills, prompts')]},
      'Agent memory splits four ways: working (current context), episodic (past runs), semantic (fact stores), procedural (skills and prompts). '
      'Most "agent memory" products are just semantic stores — know which type your problem needs.',
      'Table of agent memory types', ['memory', 'concepts']),
]

KITS['tool-use'] = [
    S('flow',
      {'steps': [('Describe tools', 'JSON schema'), ('Model chooses', 'function call'), ('Execute', 'your code runs'), ('Return result', 'model continues')]},
      'Function calling: describe tools as JSON schemas, the model emits a structured call, your code executes, results return to context. '
      'The model never touches the tool — it only requests; your executor is the trust boundary.',
      'Animated flow of tool use / function calling', ['function calling', 'concepts']),
    S('concept',
      {'title': 'Tool schema design', 'lines': ['Name: verb_phrase, clear', 'Descriptions: the model reads them',
                                                 'Parameters: typed, required marked', 'Few tools, well-described'],
       'accent': ACCENT},
      'The model only knows what the schema says: clear names, precise descriptions, typed parameters. '
      'A dozen vague tools lose to four well-described ones — schema quality is tool-use quality.',
      'Concept box: tool schema design', ['schema', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'JSON mode', 'li': ['Structured output only', 'No execution', 'Parsing/extraction tasks'],
       'rt': 'Function calling', 'ri': ['Output + execution', 'Side effects possible', 'Agentic tasks'],
       'left_accent': CYAN, 'right_accent': GREEN},
      'JSON mode constrains output shape without executing anything; function calling executes tools with side effects. '
      'Use JSON mode for extraction, function calling when the model must act on the world.',
      'Animated comparison of JSON mode vs function calling', ['json mode', 'concepts']),
    S('table',
      {'name': 'tool error handling', 'cols': [('validate args', 'GUARD', 'schema-check before exec'), ('timeout', 'GUARD', 'kill hung tools'),
                                                ('retry policy', 'GUARD', 'bounded, backoff'), ('error → model', 'LOOP', 'let it recover')]},
      'Tools fail: validate arguments before execution, timeout hung calls, retry with bounds, and return errors to the model so it can recover. '
      'The worked example\'s infinite tool loop is prevented here — bounded retries plus a step budget.',
      'Table of tool error-handling guards', ['errors', 'pitfalls', 'worked example']),
]

KITS['mcp'] = [
    S('layers',
      {'layers': [('Host: Claude / IDE', 'the application'),
                  ('MCP client', 'one per server connection'),
                  ('MCP server', 'exposes tools/resources/prompts'),
                  ('Data: files, DBs, APIs', 'the underlying systems')]},
      'MCP\'s three actors: hosts (the app), clients (protocol connections), servers (capability providers). '
      'The worked example\'s answer — in MCP, the client calls the server\'s tools; servers never call out.',
      'Animated layered diagram of MCP architecture', ['mcp', 'worked example', 'concepts']),
    S('concept',
      {'title': 'Three primitives', 'lines': ['Tools: model-invoked actions', 'Resources: app-loaded context',
                                               'Prompts: reusable templates', 'Servers choose what to expose'],
       'accent': ACCENT},
      'MCP servers expose three primitives: tools the model can call, resources the app can load as context, prompts as reusable templates. '
      'Design servers around the smallest useful capability set — every exposed tool is attack surface.',
      'Concept box: MCP primitives', ['tools', 'resources', 'concepts']),
    S('flow',
      {'steps': [('Discovery', 'list tools'), ('User approves', 'consent'), ('Model calls', 'via client'), ('Server executes', 'bounded scope')]},
      'The MCP interaction: client discovers server capabilities, the user approves tool use, the model calls through the client, the server executes in its scope. '
      'User consent gates the loop — unattended tool execution is a policy decision, not a default.',
      'Animated flow of an MCP tool-call session', ['consent', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Bespoke integrations', 'li': ['N integrations × M apps', 'Each breaks differently', 'Maintenance nightmare'],
       'rt': 'MCP standard', 'ri': ['Write server once', 'Works in every host', 'Ecosystem compounds'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Without MCP every app integrates every tool separately (N×M); with MCP each tool gets one server that every host consumes. '
      'The standard compounds: each new server multiplies the capability of every host.',
      'Animated comparison of bespoke vs MCP integrations', ['interoperability', 'concepts']),
]

KITS['langchain'] = [
    S('concept',
      {'title': 'LCEL: pipe your chain', 'lines': ['prompt | model | parser', 'Composable runnables',
                                                    'Streaming + async built in', 'Chains as code, not config'],
       'accent': ACCENT},
      'LangChain Expression Language composes runnables with pipes: prompt | model | output_parser. '
      'Composition as code beats visual builders for version control, testing, and debugging.',
      'Concept box: LCEL composition', ['lcel', 'hands-on', 'concepts']),
    S('flow',
      {'steps': [('User msg', 'input'), ('Agent A', 'specialist 1'), ('Handoff', 'structured'), ('Agent B', 'specialist 2')]},
      'AutoGen orchestrates conversable agents that hand off to each other with structured messages. '
      'Multi-agent shines for genuinely separable roles — coder plus reviewer — not for tasks one prompt could do.',
      'Animated flow of AutoGen multi-agent handoff', ['autogen', 'multi-agent', 'concepts']),
    S('compare',
      {'lt': 'LangChain', 'li': ['Chains + agents + RAG', 'Biggest ecosystem', 'Abstraction churn historically'],
       'rt': 'AutoGen', 'ri': ['Multi-agent conversations', 'Research-born patterns', 'Newer, narrower'],
       'left_accent': ACCENT, 'right_accent': PURPLE},
      'LangChain is the broad ecosystem (chains, RAG, agents); AutoGen specializes in multi-agent conversation patterns. '
      'Evaluate both against hand-rolled baselines — frameworks must earn their abstraction tax.',
      'Animated comparison of LangChain vs AutoGen', ['frameworks', 'honesty', 'concepts']),
    S('concept',
      {'title': 'Memory in LangChain', 'lines': ['Buffer: raw history', 'Summary: compressed history',
                                                  'Vector store: semantic recall', 'Match memory to task length'],
       'accent': CYAN},
      'LangChain memory strategies: buffer for short chats, summarization for long ones, vector stores for semantic recall across sessions. '
      'Unbounded buffers are how agents quietly burn context windows.',
      'Concept box: LangChain memory strategies', ['memory', 'pitfalls', 'concepts']),
]

KITS['context-eng'] = [
    S('concept',
      {'title': 'The context budget', 'lines': ['System + tools + history + task', 'Everything competes for tokens',
                                                 'Longer ≠ better: lost in the middle', 'Budget it like money'],
       'accent': ORANGE},
      'Context engineering treats the window as a budget: system prompt, tool schemas, history, and task compete for tokens. '
      '"Lost in the middle" means position matters — put the critical facts where attention finds them.',
      'Concept box: context-window budgeting', ['context', 'pitfalls', 'concepts']),
    S('flow',
      {'steps': [('Full', 'working fine'), ('80% full', 'summarize history'), ('Compact', 'keep decisions'), ('Continue', 'no quality cliff')]},
      'Compaction: when the window fills, summarize history into decisions and open threads, then continue. '
      'Compact before quality degrades — the summary is a bridge, not an archive.',
      'Animated flow of context compaction', ['compaction', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Long context', 'li': ['Stuff everything in', 'Simple, no infra', 'Attention dilutes, costs soar'],
       'rt': 'RAG + clearing', 'ri': ['Retrieve what\'s needed', 'Precise, cheaper', 'Needs retrieval infra'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Long context is simplest but attention dilutes and costs scale; RAG retrieves precisely but needs infrastructure. '
      'Hybrid wins: RAG for facts, long context for the working set — and clear aggressively.',
      'Animated comparison of long-context vs RAG strategies', ['rag', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'clearing triggers', 'cols': [('task done', 'TRIGGER', 'archive, start fresh'), ('topic shift', 'TRIGGER', 'summarize, pivot'),
                                              ('80% full', 'TRIGGER', 'compact now'), ('stale tools', 'TRIGGER', 'drop unused schemas')]},
      'Clear deliberately: completed tasks archive out, topic shifts summarize-and-pivot, 80%-full triggers compaction, stale tool schemas get dropped. '
      'A clean window is a capable agent.',
      'Table of context-clearing triggers', ['clearing', 'hands-on', 'concepts']),
]

KITS['copilot-studio'] = [
    S('flow',
      {'steps': [('Describe', 'natural language'), ('Topics', 'conversation paths'), ('Actions', 'connectors, flows'), ('Publish', 'Teams, web')]},
      'Copilot Studio builds agents low-code: describe the agent, design topics (conversation paths), attach actions via connectors, publish to channels. '
      'The speed win is real for standard enterprise workflows — custom logic still wants pro-code.',
      'Animated flow of building a Copilot Studio agent', ['copilot studio', 'low-code', 'hands-on']),
    S('concept',
      {'title': 'Topics', 'lines': ['Trigger phrases route here', 'Nodes: ask, act, branch',
                                      'Fallback: graceful handoff', 'Test in the pane constantly'],
       'accent': ACCENT},
      'Topics are conversation paths triggered by phrases, built from ask/act/branch nodes. '
      'Design the fallback first — every agent meets input it doesn\'t understand, and graceful handoff beats confident hallucination.',
      'Concept box: Copilot Studio topics', ['topics', 'pitfalls', 'concepts']),
    S('compare',
      {'lt': 'Copilot Studio', 'li': ['Low-code, fast', 'Governed, audited', 'Bounded customization'],
       'rt': 'Pro-code (Foundry)', 'ri': ['Full control', 'Any model, any code', 'You own the ops'],
       'left_accent': GREEN, 'right_accent': ACCENT},
      'Copilot Studio trades customization for speed and governance; AI Foundry trades speed for full control. '
      'Standard HR/IT workflows go low-code; differentiated product experiences go pro-code.',
      'Animated comparison of low-code vs pro-code agents', ['foundry', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'actions catalog', 'cols': [('connectors', 'TYPE', 'M365, Salesforce…'), ('Power Automate', 'TYPE', 'flows as actions'),
                                            ('REST', 'TYPE', 'custom APIs'), ('AI Builder', 'TYPE', 'doc processing')]},
      'Actions connect agents to the enterprise: stock connectors, Power Automate flows, custom REST APIs, AI Builder for documents. '
      'The agent is only as useful as its actions — wire the systems before polishing the conversation.',
      'Table of Copilot Studio action types', ['actions', 'connectors', 'hands-on']),
]

KITS['ai-foundry'] = [
    S('flow',
      {'steps': [('Project', 'organize work'), ('Models', 'deploy/select'), ('Agents', 'code + tools'), ('Evaluate', 'measure')]},
      'AI Foundry organizes pro-code agent work: projects contain model deployments, agent code with tools, and built-in evaluation. '
      'It\'s the Azure-native path from prototype to production agent.',
      'Animated flow of the AI Foundry project structure', ['foundry', 'hands-on', 'concepts']),
    S('concept',
      {'title': 'Model catalog + deployments', 'lines': ['Curated models, versioned', 'Serverless or provisioned',
                                                          'Content filters configurable', 'Benchmark before committing'],
       'accent': ACCENT},
      'The model catalog offers curated, versioned models with serverless (pay-per-token) or provisioned (reserved throughput) deployment. '
      'Benchmark candidates on your eval set before committing — catalog descriptions aren\'t benchmarks.',
      'Concept box: Foundry model deployments', ['deployment', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'evaluation built-ins', 'cols': [('quality', 'METRIC', 'groundedness, relevance'), ('risk/safety', 'METRIC', 'harm categories'),
                                                  ('custom', 'METRIC', 'your rubric, LLM-judged'), ('red-team', 'METRIC', 'adversarial sims')]},
      'Foundry bakes in evaluation: quality metrics (groundedness, relevance), safety scans, custom LLM-judged rubrics, and red-teaming simulations. '
      'Ship the eval harness with the agent — evaluation is a feature, not a phase.',
      'Table of AI Foundry evaluation capabilities', ['evaluation', 'red-team', 'concepts']),
    S('compare',
      {'lt': 'Serverless deployment', 'li': ['Pay per token', 'Scales to zero', 'Rate limits bind'],
       'rt': 'Provisioned throughput', 'ri': ['Reserved capacity', 'Predictable latency', 'Pay for idle too'],
       'left_accent': CYAN, 'right_accent': GREEN},
      'Serverless suits spiky workloads with pay-per-token; provisioned throughput suits steady production with latency SLOs. '
      'Start serverless, move to provisioned when the monthly bill crosses the reservation price.',
      'Animated comparison of Foundry deployment options', ['serverless', 'ptu', 'hands-on']),
]

KITS['azure-services'] = [
    S('table',
      {'name': 'Azure AI services map', 'cols': [('Vision', 'SERVICE', 'image analysis, OCR'), ('Language', 'SERVICE', 'NER, summarization'),
                                                  ('Speech', 'SERVICE', 'STT, TTS'), ('Document Intelligence', 'SERVICE', 'forms, layout')]},
      'Azure AI Services package pretrained capabilities as APIs: vision, language, speech, document intelligence. '
      'Reach for the API before training — pretrained services beat custom models on commodity tasks at commodity cost.',
      'Table of Azure AI services', ['cognitive services', 'concepts']),
    S('concept',
      {'title': 'Azure OpenAI Service', 'lines': ['GPT models on Azure', 'Your data stays in your boundary',
                                                    'Content filtering included', 'Private networking available'],
       'accent': ACCENT},
      'Azure OpenAI Service runs OpenAI models inside Azure\'s compliance boundary with enterprise controls — private networking, managed identity, content filters. '
      'Same models, enterprise wrapper: the reason regulated industries can use them.',
      'Concept box: Azure OpenAI Service', ['azure openai', 'concepts']),
    S('flow',
      {'steps': [('Need', 'what capability?'), ('API or custom?', 'commodity?'), ('Provision', 'keys / managed id'), ('Monitor', 'usage, quality')]},
      'Service selection: name the capability, check if a pretrained API covers it, provision with managed identity (not keys in code), monitor usage and quality. '
      'Custom models are the exception — prove the API insufficient first.',
      'Animated flow of Azure AI service selection', ['selection', 'honesty', 'hands-on']),
    S('compare',
      {'lt': 'Keys', 'li': ['Simple, leakable', 'Manual rotation', 'Never in code'],
       'rt': 'Managed identity', 'ri': ['Azure-managed credential', 'Auto-rotated', 'The production answer'],
       'left_accent': RED, 'right_accent': GREEN},
      'Authenticate services with managed identity, not keys — Azure rotates the credential and nothing leaks from your repo. '
      'Keys in code are the finding in every cloud pentest report.',
      'Animated comparison of auth methods for AI services', ['managed identity', 'pitfalls', 'concepts']),
]

KITS['ml-azure'] = [
    S('flow',
      {'steps': [('Data', 'datastores'), ('Train', 'jobs / AutoML'), ('Register', 'model registry'), ('Deploy', 'endpoints')]},
      'Azure ML\'s loop: datastores feed training jobs (or AutoML), models register with lineage, endpoints serve. '
      'The registry with full lineage — data, code, params — is what makes experiments reproducible.',
      'Animated flow of the Azure ML lifecycle', ['azure ml', 'concepts']),
    S('concept',
      {'title': 'AutoML', 'lines': ['Searches algorithms + params', 'Great baseline, fast', 'You still engineer features',
                                     'Explainability built in'],
       'accent': GREEN},
      'AutoML searches algorithms and hyperparameters to produce a strong baseline in hours. '
      'It doesn\'t replace feature engineering or problem framing — it replaces the tuning grid you were going to run anyway.',
      'Concept box: Azure AutoML', ['automl', 'honesty', 'concepts']),
    S('compare',
      {'lt': 'Designer (drag-drop)', 'li': ['Visual pipelines', 'Low-code friendly', 'Limited flexibility'],
       'rt': 'SDK / CLI (code)', 'ri': ['Full control', 'Version-controlled', 'The production path'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'The designer demos well; the SDK/CLI versions, tests, and deploys. '
      'Prototypes may start visual, but production pipelines live in code — diffable, reviewable, repeatable.',
      'Animated comparison of Azure ML interfaces', ['designer', 'sdk', 'pitfalls']),
    S('table',
      {'name': 'MLOps on Azure', 'cols': [('pipelines', 'CAPABILITY', 'scheduled retraining'), ('model registry', 'CAPABILITY', 'versioned, staged'),
                                           ('data drift', 'CAPABILITY', 'monitor inputs'), ('responsible AI', 'CAPABILITY', 'fairness dashboard')]},
      'Azure MLOps closes the loop: scheduled pipelines retrain, the registry stages promotions, drift monitors watch inputs, the RAI dashboard tracks fairness. '
      'Wire drift alerts to retraining triggers — calendars don\'t detect data change.',
      'Table of Azure MLOps capabilities', ['mlops', 'drift', 'concepts']),
]

KITS['resp-ai'] = [
    S('table',
      {'name': 'Microsoft RAI principles', 'cols': [('fairness', 'PRINCIPLE', 'no unjustified bias'), ('reliability', 'PRINCIPLE', 'safe under use'),
                                                     ('privacy', 'PRINCIPLE', 'data minimization'), ('transparency', 'PRINCIPLE', 'explainable decisions'),
                                                     ('accountability', 'PRINCIPLE', 'human oversight'), ('inclusiveness', 'PRINCIPLE', 'accessible design')]},
      'Microsoft\'s six responsible-AI principles — fairness, reliability, privacy, transparency, accountability, inclusiveness — structure the AI-900 exam and real reviews alike. '
      'Map each system decision to a principle; unmappable decisions are the risks.',
      'Table of responsible AI principles', ['responsible ai', 'concepts']),
    S('flow',
      {'steps': [('Identify harms', 'who could be hurt?'), ('Measure', 'disaggregated evals'), ('Mitigate', 'fix or constrain'), ('Operate', 'monitor live')]},
      'The RAI lifecycle: identify potential harms up front, measure with disaggregated evaluations, mitigate before shipping, monitor in operation. '
      'Fairness measured only in aggregate hides the subgroup it harms — disaggregate or don\'t claim fairness.',
      'Animated flow of the responsible-AI process', ['fairness', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Aggregate metrics', 'li': ['One number for all', 'Hides subgroup harm', 'The easy, wrong way'],
       'rt': 'Disaggregated evals', 'ri': ['Per-group performance', 'Surfaces disparities', 'The honest way'],
       'left_accent': RED, 'right_accent': GREEN},
      'Aggregate accuracy can be 95% while a subgroup sits at 60% — disaggregated evaluation is the only honest fairness check. '
      'Slice by the attributes that matter for your deployment, and set per-slice floors.',
      'Animated comparison of aggregate vs disaggregated evaluation', ['fairness', 'honesty', 'concepts']),
    S('concept',
      {'title': 'Human oversight patterns', 'lines': ['Human-in-the-loop: approves each', 'Human-on-the-loop: monitors, intervenes',
                                                       'Human-out: full automation', 'Match pattern to stakes'],
       'accent': ORANGE},
      'Match oversight to stakes: in-the-loop for consequential decisions, on-the-loop for monitored automation, out-of-the-loop only where errors are cheap. '
      'Oversight theater — a human rubber-stamping — is worse than honest automation.',
      'Concept box: human oversight patterns', ['oversight', 'pitfalls', 'concepts']),
]

KITS['cost-gov'] = [
    S('concept',
      {'title': 'Token economics', 'lines': ['Input + output tokens billed', 'Output costs more than input', 'Long context = long bills',
                                             'Cache hits: the discount lever'],
       'accent': ORANGE},
      'LLM bills count input and output tokens separately — outputs priced higher — so verbose agents on long contexts compound fast. '
      'Prompt caching and concise outputs are the first cost levers, before any architecture change.',
      'Concept box: LLM token economics', ['cost', 'tokens', 'concepts']),
    S('flow',
      {'steps': [('Tag resources', 'cost attribution'), ('Budgets + alerts', 'early warning'), ('Review usage', 'weekly'), ('Optimize', 'rightsizing')]},
      'Cloud cost governance: tag everything for attribution, set budgets with alerts, review weekly, optimize continuously. '
      'Untagged spend is ungovernable spend — attribution precedes optimization.',
      'Animated flow of cost governance', ['finops', 'hands-on', 'concepts']),
    S('table',
      {'name': 'compliance mapping', 'cols': [('data residency', 'CONTROL', 'region pinning'), ('audit logging', 'CONTROL', 'who asked what'),
                                               ('content filters', 'CONTROL', 'harm categories'), ('access reviews', 'CONTROL', 'quarterly')]},
      'Compliance for AI systems maps to concrete controls: region-pinned data residency, full audit logging of prompts and outputs, content filtering, quarterly access reviews. '
      'Regulators ask for evidence — the controls are the evidence.',
      'Table of AI compliance controls', ['compliance', 'concepts']),
    S('compare',
      {'lt': 'No guardrails', 'li': ['Cheapest today', 'Surprise bills', 'Audit findings later'],
       'rt': 'Governed spend', 'ri': ['Budgets + quotas', 'Predictable cost', 'Audit-ready'],
       'left_accent': RED, 'right_accent': GREEN},
      'Ungoverned AI spend feels fast until the surprise bill or the audit finding. '
      'Quotas per team, budgets with alerts, and tracked unit economics keep AI affordable and defensible.',
      'Animated comparison of governed vs ungoverned AI spend', ['governance', 'pitfalls', 'concepts']),
]

KITS['mlops-frame'] = [
    S('flow',
      {'steps': [('Requirements', 'metric + constraints'), ('Architecture', 'components'), ('Data contracts', 'schemas, SLAs'), ('Build', 'iterate')]},
      'ML systems design starts with requirements — the metric, latency/cost constraints, failure modes — then architecture, then data contracts. '
      'Data contracts (schemas, freshness SLAs) are the API boundaries of ML systems; undefined contracts are where pipelines rot.',
      'Animated flow of ML systems design', ['systems design', 'concepts']),
    S('layers',
      {'layers': [('Serving + monitoring', 'predictions, drift alarms'),
                  ('Training + registry', 'experiments, versions'),
                  ('Feature platform', 'shared, consistent features'),
                  ('Data platform', 'raw → curated, governed')]},
      'Production ML stacks in four layers: data platform, feature platform, training/registry, serving/monitoring. '
      'The feature platform is the hinge — one definition of each feature for training and serving alike.',
      'Animated layered diagram of the ML platform stack', ['platform', 'concepts']),
    S('concept',
      {'title': 'Requirements before models', 'lines': ['Metric: what does "good" mean?', 'Latency: p99 budget?',
                                                          'Cost: $ per 1k predictions?', 'Failure: what breaks if wrong?'],
       'accent': CYAN},
      'Every ML system design interview starts here: define good (metric), fast enough (latency), cheap enough (cost), and the failure modes. '
      'Models chosen before requirements are solutions shopping for problems.',
      'Concept box: ML requirements gathering', ['requirements', 'hands-on', 'concepts']),
    S('table',
      {'name': 'design trade-offs', 'cols': [('accuracy', 'AXIS', 'vs latency'), ('complexity', 'AXIS', 'vs maintainability'),
                                              ('freshness', 'AXIS', 'vs cost'), ('coverage', 'AXIS', 'vs precision')]},
      'ML design is trade-off management: accuracy vs latency, complexity vs maintainability, freshness vs cost. '
      'Name the trade-off explicitly in design docs — implicit trade-offs become incidents.',
      'Table of ML systems design trade-offs', ['trade-offs', 'honesty', 'concepts']),
]

KITS['serving'] = [
    S('compare',
      {'lt': 'Real-time endpoint', 'li': ['ms latency', 'Always-on cost', 'Fraud, recommendations'],
       'rt': 'Batch inference', 'ri': ['Scheduled scoring', 'No endpoint to run', 'Nightly jobs, backfills'],
       'left_accent': CYAN, 'right_accent': ACCENT},
      'Real-time endpoints serve millisecond predictions at always-on cost; batch inference scores on schedule with no endpoint to babysit. '
      'Match the pattern to decision latency — the SageMaker module\'s lesson applies everywhere.',
      'Animated comparison of serving patterns', ['serving', 'batch', 'concepts']),
    S('flow',
      {'steps': [('Canary 5%', 'new version'), ('Compare metrics', 'guardrails'), ('Ramp 50%', 'watch'), ('Full rollout', 'or rollback')]},
      'Deploy models like software: canary a small slice, compare guardrail metrics against the champion, ramp gradually, roll back on regression. '
      'Offline metrics don\'t catch production surprises — the canary does.',
      'Animated flow of canary model deployment', ['canary', 'deployment', 'hands-on']),
    S('concept',
      {'title': 'Scaling inference', 'lines': ['Horizontal: more replicas', 'Autoscale on queue/latency',
                                                'GPU sharing: multi-model', 'Cold starts: keep warm pools'],
       'accent': GREEN},
      'Scale inference horizontally with autoscaling on queue depth or latency — not CPU. '
      'Multi-model serving shares GPUs across models; warm pools hide cold-start latency from users.',
      'Concept box: inference scaling', ['scaling', 'hands-on', 'concepts']),
    S('table',
      {'name': 'deployment patterns', 'cols': [('blue/green', 'PATTERN', 'instant cutover'), ('canary', 'PATTERN', 'gradual, measured'),
                                                ('shadow', 'PATTERN', 'score, don\'t serve'), ('champion/challenger', 'PATTERN', 'A/B in prod')]},
      'Four deployment patterns: blue/green for instant cutover, canary for measured ramps, shadow for risk-free validation, champion/challenger for live A/B. '
      'Shadow mode is underused — free production validation with zero user impact.',
      'Table of model deployment patterns', ['patterns', 'hands-on', 'concepts']),
]

KITS['monitoring'] = [
    S('compare',
      {'lt': 'Data drift', 'li': ['P(X) changed', 'Inputs look different', 'Example: new camera model'],
       'rt': 'Concept drift', 'ri': ['P(y|X) changed', 'Same inputs, new meaning', 'Example: fraud tactics evolve'],
       'left_accent': ORANGE, 'right_accent': RED},
      'The worked example\'s answer: identical-looking inputs with collapsing accuracy means concept drift — the relationship changed, not the data. '
      'Data drift is detectable statistically; concept drift needs labeled feedback to confirm.',
      'Animated comparison of data drift vs concept drift', ['drift', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('Log predictions', 'inputs + outputs'), ('Compute drift', 'PSI, KS tests'), ('Alert', 'threshold breach'), ('Retrain?', 'decide with labels')]},
      'Monitoring pipelines log predictions with inputs, compute drift statistics (PSI, KS), alert on breaches, and trigger retraining decisions. '
      'Log everything at serving time — you can\'t analyze what you didn\'t store.',
      'Animated flow of the drift-monitoring pipeline', ['monitoring', 'hands-on', 'concepts']),
    S('concept',
      {'title': 'What to monitor', 'lines': ['Inputs: drift, nulls, ranges', 'Predictions: distribution shifts',
                                              'Business: conversion, loss $', 'System: latency, errors'],
       'accent': CYAN},
      'Monitor four layers: input data quality, prediction distributions, business outcomes, and system health. '
      'Business-metric monitoring catches the failures statistics miss — a model can be "accurate" and still lose money.',
      'Concept box: the four monitoring layers', ['monitoring', 'concepts']),
    S('table',
      {'name': 'retraining triggers', 'cols': [('drift alert', 'TRIGGER', 'statistical breach'), ('performance drop', 'TRIGGER', 'labeled eval decay'),
                                                ('calendar', 'TRIGGER', 'weak, but simple'), ('new data', 'TRIGGER', 'labeled batches arrive')]},
      'Retrain on triggers, not calendars: drift alerts, measured performance decay, or fresh labeled data. '
      'Calendar retraining wastes compute when nothing changed and reacts too slowly when something did.',
      'Table of model-retraining triggers', ['retraining', 'pitfalls', 'hands-on']),
]

KITS['agentops'] = [
    S('concept',
      {'title': 'Trace anatomy', 'lines': ['Trace: one full agent run', 'Spans: LLM call, tool call, …',
                                            'Attributes: tokens, latency, cost', 'The unit of debugging'],
       'accent': ACCENT},
      'AgentOps traces decompose each run into spans — LLM calls, tool executions, retrievals — with tokens, latency, and cost attached. '
      'The trace is the unit of debugging: "the agent failed" becomes "span 7\'s tool returned X".',
      'Concept box: agent trace anatomy', ['tracing', 'concepts']),
    S('flow',
      {'steps': [('Instrument', 'wrap calls'), ('Collect', 'trace backend'), ('Inspect', 'find the bad span'), ('Fix', 'prompt/tool/data')]},
      'Instrument every LLM and tool call, collect traces centrally, inspect failures span-by-span, fix the actual cause (prompt, tool, or data). '
      'Uninstrumented agents fail mysteriously; traced agents fail specifically.',
      'Animated flow of agent debugging with traces', ['debugging', 'hands-on', 'concepts']),
    S('table',
      {'name': 'what to log per span', 'cols': [('inputs/outputs', 'FIELD', 'the actual text'), ('tokens', 'FIELD', 'cost math'),
                                                  ('latency', 'FIELD', 'bottleneck hunt'), ('tool args', 'FIELD', 'repro the call')]},
      'Log inputs, outputs, tokens, latency, and tool arguments per span — the five fields that answer "what happened and what did it cost". '
      'Redact secrets at collection; traces with credentials are incidents waiting to happen.',
      'Table of span logging fields', ['logging', 'pitfalls', 'hands-on']),
    S('compare',
      {'lt': 'Metrics only', 'li': ['Success rate, latency p99', 'Sees the what', 'Blind to the why'],
       'rt': 'Traces + evals', 'ri': ['Full execution detail', 'Sees the why', 'Debuggable, improvable'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Metrics tell you the agent got worse; traces tell you which span broke and why. '
      'Pair tracing with trajectory evals and every regression becomes a debuggable, fixable event.',
      'Animated comparison of metrics-only vs trace-based observability', ['observability', 'concepts']),
]

KITS['cost-latency'] = [
    S('concept',
      {'title': 'The latency budget', 'lines': ['Total = Σ (model + tools + network)', 'Tools usually dominate',
                                                 'Parallelize independent calls', 'Stream tokens: perceived speed'],
       'accent': ORANGE},
      'Budget agent latency end-to-end: model calls plus tool calls plus network, with tools usually dominating. '
      'Parallelize independent calls and stream tokens — perceived latency matters as much as actual.',
      'Concept box: agent latency budgeting', ['latency', 'hands-on', 'concepts']),
    S('flow',
      {'steps': [('Exact cache', 'repeat queries'), ('Semantic cache', 'similar queries'), ('Model router', 'small vs large'), ('Fall back', 'escalate on low confidence')]},
      'Cut costs in layers: exact-match caching for repeats, semantic caching for near-dupes, model routing (small model first, escalate on low confidence). '
      'Routing alone often halves bills — most queries don\'t need the flagship.',
      'Animated flow of LLM cost-optimization layers', ['caching', 'routing', 'hands-on']),
    S('table',
      {'name': 'cost levers', 'cols': [('smaller model', 'LEVER', 'first-line attempt'), ('shorter context', 'LEVER', 'clear aggressively'),
                                        ('fewer tool rounds', 'LEVER', 'step budget'), ('batching', 'LEVER', 'amortize overhead')]},
      'Four cost levers before architecture changes: smaller models, shorter contexts, bounded tool rounds, request batching. '
      'Measure $/successful-task — the unit economics of the agent, not $/token in isolation.',
      'Table of LLM cost-optimization levers', ['cost', 'pitfalls', 'hands-on']),
    S('compare',
      {'lt': 'Optimize tokens', 'li': ['$ per token minimized', 'May hurt task success', 'Local optimum'],
       'rt': 'Optimize $/task', 'ri': ['Cost per completed task', 'Success rate included', 'The business metric'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'A cheaper model that fails twice as often costs more per completed task. '
      'Optimize dollars per successful task — the business metric — not dollars per token.',
      'Animated comparison of token-cost vs task-cost optimization', ['unit economics', 'honesty', 'concepts']),
]

KITS['red-team'] = [
    S('flow',
      {'steps': [('Scope', 'what\'s in bounds'), ('Attack', 'prompt/tools/jailbreaks'), ('Document', 'repro steps'), ('Fix + retest', 'close the loop')]},
      'Red-teaming runs scoped adversarial testing: define what\'s in bounds, attack prompts/tools/jailbreaks, document reproductions, fix and retest. '
      'Undocumented findings don\'t exist — the report is the deliverable.',
      'Animated flow of AI red-teaming', ['red-team', 'hands-on', 'concepts']),
    S('table',
      {'name': 'attack categories', 'cols': [('jailbreaks', 'CLASS', 'policy bypass prompts'), ('prompt injection', 'CLASS', 'untrusted content as instructions'),
                                              ('data exfiltration', 'CLASS', 'tool-mediated leaks'), ('tool abuse', 'CLASS', 'excessive agency')]},
      'Four attack classes: jailbreaks bypass policy, prompt injection turns untrusted content into instructions, tools exfiltrate data, excess agency gets abused. '
      'Test all four — attackers won\'t limit themselves to your favorite.',
      'Table of AI attack categories', ['jailbreak', 'injection', 'concepts']),
    S('concept',
      {'title': 'The eval harness', 'lines': ['Adversarial prompt suite', 'Automated + human judging',
                                               'Regression: run on every release', 'Track pass rate over time'],
       'accent': RED},
      'The evaluation harness runs the adversarial suite on every release with automated plus human judging. '
      'Track pass rates over time — security that isn\'t regression-tested decays with each model update.',
      'Concept box: the red-team evaluation harness', ['harness', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'One-off pentest', 'li': ['Point-in-time', 'Findings age fast', 'Compliance checkbox'],
       'rt': 'Continuous red-teaming', 'ri': ['Every release tested', 'Findings stay fresh', 'Security practice'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'One-off tests age the moment the model updates; continuous red-teaming on every release keeps findings fresh. '
      'AI systems change with prompts, tools, and model versions — test at the pace of change.',
      'Animated comparison of one-off vs continuous red-teaming', ['continuous', 'pitfalls', 'concepts']),
]

KITS['traj-eval'] = [
    S('concept',
      {'title': 'Trajectory anatomy', 'lines': ['Steps: thought → action → observation', 'The full action trace',
                                                 'Grade steps, not just outcomes', 'Right answer, wrong path = risk'],
       'accent': ACCENT},
      'A trajectory is the agent\'s full action trace — every thought, tool call, and observation. '
      'Grade the steps, not just the outcome: a right answer via a reckless path is a incident rehearsal.',
      'Concept box: agent trajectory anatomy', ['trajectory', 'concepts']),
    S('table',
      {'name': 'rubric dimensions', 'cols': [('task success', 'DIM', 'goal achieved?'), ('efficiency', 'DIM', 'steps + tokens used'),
                                              ('safety', 'DIM', 'policy violations?'), ('tool correctness', 'DIM', 'right tools, right args')]},
      'Rubric-scored trajectories beat vibes: task success, efficiency (steps and tokens), safety, and tool correctness as separate dimensions. '
      'LLM judges apply the rubric at scale; humans calibrate the judges.',
      'Table of trajectory-evaluation rubric dimensions', ['rubric', 'hands-on', 'concepts']),
    S('flow',
      {'steps': [('Collect traces', 'production sample'), ('Judge', 'rubric, LLM + human'), ('Find failures', 'cluster modes'), ('Fix top mode', 'iterate')]},
      'Trajectory eval loops: sample production traces, judge against the rubric, cluster failure modes, fix the biggest cluster. '
      'One failure mode fixed per cycle compounds — eval-driven agent development.',
      'Animated flow of trajectory-evaluation iteration', ['iteration', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Final-answer grading', 'li': ['Cheap, simple', 'Misses dangerous paths', 'Gaming-prone'],
       'rt': 'Trajectory grading', 'ri': ['Grades the whole path', 'Catches unsafe steps', 'The production standard'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Final-answer grading misses the agent that got lucky or cheated; trajectory grading catches unsafe intermediate steps. '
      'Production agents get trajectory evals — the path is the product.',
      'Animated comparison of grading approaches', ['honesty', 'pitfalls', 'concepts']),
]

KITS['pipelines'] = [
    S('flow',
      {'steps': [('Commit', 'code + data refs'), ('Test', 'unit + data tests'), ('Train', 'reproducible job'), ('Promote', 'registry gates')]},
      'ML CI/CD: commits trigger code tests plus data tests, training runs reproducibly, registry gates promote. '
      'Data tests (schema, distribution checks) are the ML-specific addition — code tests alone miss data breakage.',
      'Animated flow of the ML CI/CD pipeline', ['cicd', 'hands-on', 'concepts']),
    S('concept',
      {'title': 'Point-in-time correctness', 'lines': ['Features as of prediction time', 'No future leakage in training',
                                                        'The worked example\'s answer', 'Feature store enforces it'],
       'accent': RED},
      'The worked example\'s answer: point-in-time correctness means training features reflect only data available at prediction time. '
      'Joins against current dimension tables leak the future — the feature store\'s time-travel queries exist to prevent exactly this.',
      'Concept box: point-in-time correctness', ['point-in-time', 'worked example', 'pitfalls']),
    S('table',
      {'name': 'pipeline stages', 'cols': [('ingest', 'STAGE', 'validate on entry'), ('transform', 'STAGE', 'tested transforms'),
                                             ('train', 'STAGE', 'tracked experiments'), ('deploy', 'STAGE', 'gated promotion')]},
      'Pipeline stages with their tests: validate data on entry, test transforms, track experiments, gate promotions. '
      'A stage without tests is a stage where failures are discovered in production.',
      'Table of ML pipeline stages and tests', ['stages', 'testing', 'concepts']),
    S('compare',
      {'lt': 'Notebook runs', 'li': ['Manual, unrepeatable', 'Works on my machine', 'No lineage'],
       'rt': 'Pipelined runs', 'ri': ['Scheduled, versioned', 'Reproducible anywhere', 'Full lineage'],
       'left_accent': RED, 'right_accent': GREEN},
      'Notebooks explore; pipelines produce. '
      'Promote notebook logic into versioned, scheduled, lineage-tracked pipelines before anything touches production data.',
      'Animated comparison of notebooks vs production pipelines', ['notebooks', 'honesty', 'pitfalls']),
]

KITS['exp-tracking'] = [
    S('concept',
      {'title': 'Log everything', 'lines': ['Params: every hyperparameter', 'Metrics: per epoch', 'Artifacts: code + data version',
                                             'Environment: image, seed'],
       'accent': ACCENT},
      'Experiment tracking logs params, metrics, artifacts, and environment for every run — the four things needed to reproduce a result. '
      'An untracked experiment is an anecdote; a tracked one is evidence.',
      'Concept box: experiment-tracking essentials', ['mlflow', 'concepts']),
    S('flow',
      {'steps': [('Experiment', 'many runs'), ('Compare', 'leaderboard'), ('Register', 'best → registry'), ('Stage', 'staging → prod')]},
      'The registry workflow: experiments produce runs, the leaderboard surfaces the best, registration versions it, staging gates promote to production. '
      'Stages (staging/production/archived) are the deployment contract.',
      'Animated flow of the model-registry lifecycle', ['registry', 'hands-on', 'concepts']),
    S('table',
      {'name': 'lineage', 'cols': [('data', 'TRACK', 'dataset version/hash'), ('code', 'TRACK', 'git commit'), ('params', 'TRACK', 'full config'),
                                    ('model', 'TRACK', 'artifact + metrics')]},
      'Lineage connects data version → code commit → params → model artifact, so any production model is fully auditable. '
      '"Which data trained this model?" must be answerable in seconds, not sprints.',
      'Table of ML lineage components', ['lineage', 'reproducibility', 'concepts']),
    S('compare',
      {'lt': 'Spreadsheet tracking', 'li': ['Manual, drifts', 'No artifact links', 'Dies at 20 runs'],
       'rt': 'MLflow / Weights & Biases', 'ri': ['Automatic logging', 'Artifacts attached', 'Scales to thousands'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Spreadsheets die around run twenty; MLflow or W&B log automatically with artifacts attached and scale to thousands of runs. '
      'Adopt tracking on run one — retrofitting lineage onto old experiments is archaeology.',
      'Animated comparison of experiment-tracking approaches', ['mlflow', 'pitfalls', 'hands-on']),
]

KITS['feature-store'] = [
    S('compare',
      {'lt': 'Offline store', 'li': ['Batch features', 'Training + backfills', 'Latency-tolerant'],
       'rt': 'Online store', 'ri': ['Low-latency serving', 'Real-time inference', 'Freshness SLAs'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'Feature stores split serving paths: the offline store feeds training and backfills; the online store serves millisecond inference. '
      'Both derive from the same definitions — that\'s the consistency guarantee.',
      'Animated comparison of offline vs online feature stores', ['offline', 'online', 'concepts']),
    S('flow',
      {'steps': [('Define', 'feature logic once'), ('Materialize', 'offline + online'), ('Serve', 'same values both'), ('Monitor', 'freshness, drift')]},
      'Define each feature once, materialize to both stores, serve identical values to training and inference. '
      'One definition kills training/serving skew at the source — the architectural fix from the AWS module.',
      'Animated flow of feature-store materialization', ['materialize', 'skew', 'concepts']),
    S('concept',
      {'title': 'Time travel', 'lines': ['Query features "as of" timestamp', 'Reconstructs training-time values',
                                          'Kills point-in-time leakage', 'The store\'s killer feature'],
       'accent': PURPLE},
      'Time-travel queries reconstruct feature values as of any past timestamp — exactly what point-in-time-correct training sets need. '
      'Without it, teams hand-roll as-of joins and inevitably leak the future.',
      'Concept box: feature-store time travel', ['time travel', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'feature hygiene', 'cols': [('naming', 'RULE', 'domain__feature convention'), ('ownership', 'RULE', 'every feature owned'),
                                            ('freshness SLA', 'RULE', 'documented per feature'), ('deprecation', 'RULE', 'announced, versioned')]},
      'Feature hygiene: consistent naming, clear ownership, documented freshness SLAs, versioned deprecation. '
      'A feature store without governance becomes a feature swamp — discoverable but untrustworthy.',
      'Table of feature-store hygiene rules', ['governance', 'pitfalls', 'hands-on']),
]

KITS['data-centric'] = [
    S('layers',
      {'layers': [('Model iteration', 'architecture, hyperparameters'),
                  ('Data iteration', 'labels, slices, augmentation'),
                  ('Data quality', 'correctness, consistency'),
                  ('Data collection', 'coverage of the problem')]},
      'Data-centric AI inverts the priority stack: fix the data before the model. '
      'Most production accuracy gains come from the bottom three layers — collection, quality, targeted iteration — not architecture.',
      'Animated layered diagram of the data-centric priority stack', ['data-centric', 'concepts']),
    S('flow',
      {'steps': [('Error analysis', 'worst slice'), ('Fix data', 'relabel, augment'), ('Retrain', 'same model'), ('Measure', 'slice improved?')]},
      'The data-centric loop: error analysis finds the worst slice, targeted data fixes address it, retrain the same model, measure the slice. '
      'Label errors in the worst slice often beat any architecture change.',
      'Animated flow of data-centric iteration', ['error analysis', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Model-centric', 'li': ['Fix the architecture', 'Diminishing returns', 'Data assumed fixed'],
       'rt': 'Data-centric', 'ri': ['Fix the data', 'Compounding returns', 'Model held constant'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Model-centric iteration tunes architectures against fixed data with diminishing returns; data-centric iteration improves the data the model learns from. '
      'Hold the model constant while fixing data — otherwise you can\'t attribute the gain.',
      'Animated comparison of model-centric vs data-centric AI', ['honesty', 'concepts']),
    S('table',
      {'name': 'data quality dimensions', 'cols': [('correctness', 'DIM', 'labels right?'), ('coverage', 'DIM', 'slices represented?'),
                                                    ('consistency', 'DIM', 'same rule everywhere?'), ('freshness', 'DIM', 'still true?')]},
      'Audit training data on four dimensions: correctness of labels, coverage of slices, consistency of rules, freshness of facts. '
      'Systematic label errors teach the model the wrong task confidently.',
      'Table of training-data quality dimensions', ['quality', 'pitfalls', 'hands-on']),
]

KITS['edge-ai'] = [
    S('concept',
      {'title': 'The edge constraints', 'lines': ['Memory: MBs, not GBs', 'Compute: no datacenter GPU',
                                                   'Power: battery budgets', 'Latency: offline, instant'],
       'accent': ORANGE},
      'Edge AI lives under four constraints: megabytes of memory, modest compute, battery power, and offline-first latency. '
      'Every technique in this module trades accuracy for fitting inside those walls.',
      'Concept box: edge deployment constraints', ['edge', 'concepts']),
    S('flow',
      {'steps': [('Full model', 'FP32 baseline'), ('Quantize', 'INT8/INT4'), ('Prune', 'drop dead weights'), ('Distill?', 'small mimics large')]},
      'The compression pipeline: quantize to INT8/INT4, prune dead weights, optionally distill into a smaller student. '
      'Each step trades a little accuracy for a lot of size — measure the trade on your task, not a benchmark.',
      'Animated flow of model compression for edge', ['quantization', 'pruning', 'distillation']),
    S('compare',
      {'lt': 'Cloud inference', 'li': ['Big models, easy updates', 'Network latency + cost', 'Data leaves device'],
       'rt': 'On-device', 'ri': ['Private, instant, offline', 'Update logistics harder', 'Model must fit'],
       'left_accent': ACCENT, 'right_accent': GREEN},
      'Cloud inference runs big models with update ease but pays latency, cost, and privacy; on-device is private, instant, and offline but must fit the hardware. '
      'Privacy-sensitive and latency-critical workloads justify the compression effort.',
      'Animated comparison of cloud vs on-device inference', ['privacy', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'deployment targets', 'cols': [('mobile', 'TARGET', 'Core ML, TFLite'), ('browser', 'TARGET', 'ONNX, WebGPU'),
                                               ('microcontroller', 'TARGET', 'TinyML, KBs'), ('edge server', 'TARGET', 'TensorRT')]},
      'Match the runtime to the target: Core ML/TFLite for phones, ONNX/WebGPU for browsers, TinyML for microcontrollers, TensorRT for edge servers. '
      'Convert and benchmark on the actual device — emulator numbers lie.',
      'Table of edge deployment targets', ['tflite', 'onnx', 'hands-on']),
]

KITS['cap-framing'] = [
    S('concept',
      {'title': 'The framing canvas', 'lines': ['Problem: whose pain, how often?', 'Decision: what changes with output?',
                                                 'Metric: how is good measured?', 'Baseline: what must we beat?'],
       'accent': ACCENT},
      'Frame the capstone before building: whose pain and how often, which decision the output changes, how "good" is measured, what baseline must be beaten. '
      'A project that can\'t fill this canvas isn\'t ready to build.',
      'Concept box: the problem-framing canvas', ['framing', 'hands-on', 'concepts']),
    S('flow',
      {'steps': [('Pain', 'real user need'), ('Data?', 'exists or collectable'), ('Feasible', '2-week slices'), ('Valuable', 'metric moves')]},
      'Scope the capstone through four gates: real pain, obtainable data, feasible in slices, valuable by metric. '
      'Kill ideas at the gate that fails — the cheapest failure is the one before building.',
      'Animated flow of capstone scoping gates', ['scoping', 'pitfalls', 'concepts']),
    S('compare',
      {'lt': 'Tech-first project', 'li': ['"Use transformers!"', 'Solution seeks problem', 'Demo impresses, nobody needs'],
       'rt': 'Problem-first project', 'ri': ['Pain → simplest solution', 'Boring tech that works', 'Portfolio with users'],
       'left_accent': RED, 'right_accent': GREEN},
      'Tech-first capstones demo impressively and get used never; problem-first capstones ship boring tech that solves real pain. '
      'Hiring managers remember the project with users, not the one with the fanciest architecture.',
      'Animated comparison of capstone approaches', ['honesty', 'portfolio', 'pitfalls']),
    S('table',
      {'name': 'success criteria', 'cols': [('metric', 'DEFINE', 'target number'), ('baseline', 'DEFINE', 'beat this'),
                                             ('scope', 'DEFINE', 'explicitly out'), ('demo', 'DEFINE', 'the 5-min story')]},
      'Write success criteria before building: the metric target, the baseline to beat, explicit out-of-scope, the five-minute demo story. '
      'Criteria written after building are rationalizations, not goals.',
      'Table of capstone success criteria', ['criteria', 'hands-on', 'concepts']),
]

KITS['cap-build'] = [
    S('flow',
      {'steps': [('Slice 1', 'end-to-end thin'), ('Slice 2', 'harden core'), ('Slice 3', 'differentiate'), ('Polish', 'demo-ready')]},
      'Build in vertical slices: a thin end-to-end first, then harden the core, then differentiate, then polish. '
      'A working thin slice at week one beats a perfect component at week four — integration risk dies early.',
      'Animated flow of vertical-slice building', ['slices', 'hands-on', 'concepts']),
    S('concept',
      {'title': 'Integration points', 'lines': ['Data → features → model → app', 'Contract each boundary',
                                                 'Test boundaries first', 'Mocks unblock parallel work'],
       'accent': CYAN},
      'Capstone integration fails at boundaries: define contracts between data, features, model, and app; test boundaries first; use mocks to unblock parallel work. '
      'The demo dies at the seam nobody tested.',
      'Concept box: capstone integration strategy', ['integration', 'pitfalls', 'hands-on']),
    S('table',
      {'name': 'build milestones', 'cols': [('week 1', 'MILESTONE', 'thin slice works'), ('week 2', 'MILESTONE', 'core hardened'),
                                             ('week 3', 'MILESTONE', 'evals + polish'), ('week 4', 'MILESTONE', 'deployed demo')]},
      'Milestone the build weekly: thin slice, hardened core, evals and polish, deployed demo. '
      'A milestone without a demo-able artifact is a status report, not progress.',
      'Table of capstone build milestones', ['milestones', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Big-bang build', 'li': ['Integrate at the end', 'Risk compounds silently', 'Demo-day surprises'],
       'rt': 'Slice-by-slice', 'ri': ['Always demoable', 'Risk retired early', 'Boring, reliable'],
       'left_accent': RED, 'right_accent': GREEN},
      'Big-bang builds compound integration risk until demo day; vertical slices keep the project always demoable. '
      'Boring and reliable ships; ambitious and integrated-late doesn\'t.',
      'Animated comparison of build strategies', ['pitfalls', 'honesty', 'concepts']),
]

KITS['cap-eval'] = [
    S('flow',
      {'steps': [('Eval set', 'held-out, labeled'), ('Metrics', 'task-appropriate'), ('Slices', 'worst-case first'), ('Adversarial', 'break it')]},
      'Capstone evaluation: a held-out labeled set, task-appropriate metrics, slice analysis worst-first, and adversarial probing. '
      'The aggregate score is the headline; the worst slice is the truth.',
      'Animated flow of capstone evaluation', ['evaluation', 'hands-on', 'concepts']),
    S('concept',
      {'title': 'Robustness tests', 'lines': ['Noise: typos, ASR errors', 'Distribution shift: new sources',
                                               'Adversarial: crafted inputs', 'Ablation: which part matters?'],
       'accent': RED},
      'Robustness testing goes beyond the eval set: noise tolerance, distribution shift, adversarial inputs, and ablations showing which component matters. '
      'A model that only works on clean eval data works nowhere.',
      'Concept box: robustness testing', ['robustness', 'ablation', 'concepts']),
    S('table',
      {'name': 'eval report card', 'cols': [('overall', 'SCORE', 'headline metric'), ('worst slice', 'SCORE', 'the honest number'),
                                             ('latency', 'SCORE', 'p99 in ms'), ('cost', 'SCORE', '$/1k tasks')]},
      'Report four numbers: overall score, worst-slice score, p99 latency, cost per task. '
      'A portfolio piece with all four signals production thinking; one with only accuracy signals a notebook.',
      'Table of the capstone eval report card', ['report', 'honesty', 'hands-on']),
    S('compare',
      {'lt': 'Vibes evaluation', 'li': ['"Looks good"', 'Cherry-picked examples', 'Collapses on questions'],
       'rt': 'Rigorous evaluation', 'ri': ['Held-out + slices', 'Adversarial tested', 'Survives interrogation'],
       'left_accent': RED, 'right_accent': GREEN},
      'Vibes evaluation — a few cherry-picked examples — collapses the moment anyone asks a hard question. '
      'Rigorous evals with slices and adversarial tests survive interrogation, including in interviews.',
      'Animated comparison of evaluation rigor', ['honesty', 'interview', 'pitfalls']),
]

KITS['cap-deploy'] = [
    S('flow',
      {'steps': [('Package', 'container + deps'), ('Serve', 'endpoint or batch'), ('Monitor', 'drift + errors'), ('Iterate', 'MLOps lite loop')]},
      'MLOps-lite deployment: containerize with pinned deps, serve via endpoint or batch, monitor drift and errors, iterate. '
      'The worked example\'s collapse-with-identical-inputs scenario is what monitoring exists to catch.',
      'Animated flow of capstone deployment', ['deploy', 'worked example', 'hands-on']),
    S('concept',
      {'title': 'Deploy checklist', 'lines': ['Pinned dependencies, reproducible', 'Health + readiness probes',
                                               'Rollback plan tested', 'Secrets in vault, not code'],
       'accent': GREEN},
      'The deployment checklist: reproducible builds, health probes, a tested rollback plan, secrets in a vault. '
      'Check the rollback before you need it — untested rollbacks are hopes.',
      'Concept box: deployment checklist', ['checklist', 'pitfalls', 'hands-on']),
    S('table',
      {'name': 'MLOps-lite stack', 'cols': [('serving', 'PIECE', 'FastAPI / BentoML'), ('tracking', 'PIECE', 'MLflow'),
                                             ('monitoring', 'PIECE', 'Evidently / custom'), ('CI', 'PIECE', 'GitHub Actions')]},
      'MLOps-lite needs four pieces: a serving layer, experiment tracking, drift monitoring, and CI. '
      'Boring, standard tools beat bespoke platforms for capstone scale — save innovation for the model.',
      'Table of the MLOps-lite stack', ['stack', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Demo on laptop', 'li': ['Works in the room', 'Dies after demo', 'No one can reproduce'],
       'rt': 'Deployed demo', 'ri': ['Public URL, live', 'Monitored, maintained', 'Portfolio-grade'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'A laptop demo impresses a room; a deployed demo with a public URL impresses hiring managers asynchronously. '
      'Deploy it, monitor it, link it — that\'s the portfolio bar.',
      'Animated comparison of demo quality', ['portfolio', 'honesty', 'concepts']),
]

KITS['cap-rai'] = [
    S('flow',
      {'steps': [('Identify harms', 'who could be hurt?'), ('Assess', 'likelihood × severity'), ('Mitigate', 'constrain or gate'), ('Document', 'model card')]},
      'The RAI review: identify who could be harmed, assess likelihood × severity, mitigate with constraints or human gates, document in a model card. '
      'Do it before launch — retrofitted safety is theater.',
      'Animated flow of the responsible-AI review', ['rai', 'hands-on', 'concepts']),
    S('concept',
      {'title': 'Risk tiers', 'lines': ['Unacceptable: don\'t build', 'High: human gates required',
                                         'Limited: transparency duties', 'Minimal: document and ship'],
       'accent': ORANGE},
      'Tier the risks: unacceptable uses don\'t get built, high-risk gets human gates, limited-risk gets transparency, minimal-risk gets documented. '
      'The EU AI Act\'s framing is a useful mental model even where it doesn\'t apply.',
      'Concept box: AI risk tiers', ['risk', 'concepts']),
    S('table',
      {'name': 'model card sections', 'cols': [('intended use', 'SECTION', 'who, for what'), ('limitations', 'SECTION', 'known failure modes'),
                                                ('evals', 'SECTION', 'disaggregated scores'), ('ethical notes', 'SECTION', 'risks + mitigations')]},
      'The model card documents intended use, limitations, disaggregated evals, and ethical considerations. '
      'Write it honestly — the limitations section is where reviewers learn to trust you.',
      'Table of model-card sections', ['model card', 'honesty', 'hands-on']),
    S('compare',
      {'lt': 'Ship and hope', 'li': ['No review', 'Surprises in production', 'Trust erodes'],
       'rt': 'Reviewed and gated', 'ri': ['RAI review passed', 'Monitored risks', 'Trust compounds'],
       'left_accent': RED, 'right_accent': GREEN},
      'Shipping without review borrows against trust; reviewed and gated systems compound it. '
      'The RAI review is a portfolio differentiator — most candidates never do one.',
      'Animated comparison of shipping discipline', ['trust', 'portfolio', 'pitfalls']),
]

KITS['cap-portfolio'] = [
    S('concept',
      {'title': 'Portfolio piece anatomy', 'lines': ['Problem: one-paragraph story', 'Demo: live link, 30 seconds in',
                                                      'Code: readable, documented', 'Write-up: decisions + trade-offs'],
       'accent': ACCENT},
      'A portfolio piece has four parts: a one-paragraph problem story, a live demo reachable in 30 seconds, readable documented code, and a write-up of decisions and trade-offs. '
      'Reviewers skim — the story and demo carry the piece.',
      'Concept box: portfolio-piece anatomy', ['portfolio', 'hands-on', 'concepts']),
    S('flow',
      {'steps': [('Hook', 'the problem, 10s'), ('Demo', 'it working, 60s'), ('Depth', 'one hard decision'), ('Close', 'what\'s next')]},
      'The five-minute demo arc: hook with the problem, show it working, explain one hard decision in depth, close with what\'s next. '
      'One deep decision beats ten shallow features — depth signals seniority.',
      'Animated flow of the demo narrative', ['demo', 'storytelling', 'hands-on']),
    S('table',
      {'name': 'README that gets read', 'cols': [('top', 'SECTION', 'demo link + screenshot'), ('middle', 'SECTION', 'how to run in 3 steps'),
                                                  ('depth', 'SECTION', 'architecture + trade-offs'), ('bottom', 'SECTION', 'results + next steps')]},
      'READMEs get skimmed top-down: demo link and screenshot first, three-step run instructions, architecture and trade-offs, results and next steps. '
      'If the demo link isn\'t above the fold, most readers never find it.',
      'Table of README structure', ['readme', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Tutorial clone', 'li': ['Follows the guide', 'No decisions made', 'Everyone has it'],
       'rt': 'Differentiated build', 'ri': ['Your problem, your data', 'Trade-offs defended', 'Memorable'],
       'left_accent': ORANGE, 'right_accent': GREEN},
      'Tutorial clones signal you can follow instructions; differentiated builds on your own problem with defended trade-offs signal you can engineer. '
      'Start from a tutorial if you must — then diverge deliberately.',
      'Animated comparison of portfolio project types', ['differentiation', 'honesty', 'pitfalls']),
]

KITS['autonomy'] = [
    S('concept',
      {'title': 'Time horizons', 'lines': ['P50 horizon: task length at 50% success', 'Doubles roughly yearly (as of P50)',
                                            '3-hour unsupervised subtask: check P50', 'Beyond horizon: supervise closely'],
       'accent': ORANGE},
      'The worked example\'s rule: an agent\'s time horizon (P50) is the task length it completes half the time — roughly doubling yearly. '
      'A 3-hour unsupervised subtask is safe only if the as-of P50 covers it; beyond the horizon, supervise closely.',
      'Concept box: agent time horizons', ['time horizon', 'worked example', 'concepts']),
    S('flow',
      {'steps': [('Estimate', 'task length'), ('Check P50', 'as-of horizon'), ('Within?', 'autonomous OK'), ('Beyond?', 'checkpoint it')]},
      'The autonomy decision: estimate the subtask length, check the as-of P50 horizon, run autonomously within it, checkpoint beyond it. '
      'Horizons are empirical — measure on your tasks, don\'t assume.',
      'Animated flow of the autonomy-ceiling decision', ['horizon', 'hands-on', 'concepts']),
    S('compare',
      {'lt': 'Unsupervised long tasks', 'li': ['Drift compounds silently', 'Failure discovered late', 'Expensive recovery'],
       'rt': 'Checkpointed autonomy', 'ri': ['Verify at intervals', 'Catch drift early', 'Cheap correction'],
       'left_accent': RED, 'right_accent': GREEN},
      'Long unsupervised runs let errors compound silently until recovery is expensive; checkpointed autonomy verifies at intervals. '
      'Checkpoints are the autonomy ceiling made operational.',
      'Animated comparison of autonomy strategies', ['checkpoints', 'pitfalls', 'concepts']),
    S('table',
      {'name': 'deployment gates', 'cols': [('read-only', 'GATE', 'low risk, wide autonomy'), ('side effects', 'GATE', 'approve or bound'),
                                             ('irreversible', 'GATE', 'human confirms'), ('scale', 'GATE', 'rate-limit + monitor')]},
      'Gate autonomy by blast radius: read-only gets wide latitude, side effects get bounds or approval, irreversible actions get human confirmation. '
      'Autonomy ceilings aren\'t about trust — they\'re about the cost of being wrong.',
      'Table of agent deployment gates', ['gates', 'safety', 'hands-on']),
]

# ================= ROUTING: module id -> kit key =================
ROUTES = {
 # IL-07
 'il-07-data-engineering-analytics-ai-math-stats': 'prob-stats',
 'il-07-data-engineering-analytics-ai-math-linalg': 'linalg',
 'il07-mongodb': 'il07-mongodb',
 'il07-data-schools': 'il07-data-schools',
 'il07-ai-ml': 'il07-ai-ml',
 'il07-neuroai': 'il07-neuroai',
 'il07-openweight': 'il07-openweight',
 'il07-agents': 'il07-agents',
 'il07-frontier': 'il07-frontier',
 'il07-aws-data': 'il07-aws-data',
 'il07-aws-ml': 'il07-aws-ml',
 # IL-08
 'il-08-algorithms-compilers-distributed-formal-math-discrete': 'discrete',
 'il-08-algorithms-compilers-distributed-formal-math-logic': 'logic',
 'il08-mit-63': 'il08-mit',
 'il08-cmu-cs': 'il08-cmu',
 'il08-stanford-cs': 'il08-stanford',
 # IL-09
 'il-09-adaptive-certification-command-math-binmath': 'binmath',
 'il-09-adaptive-certification-command-math-logic': 'logic',
 'il09-comptia-core': 'il09-core',
 'il09-comptia-security': 'il09-security',
 'il09-comptia-data-cloud': 'il09-data-cloud',
 'il09-vendor-ai': 'il09-vendor-ai',
 'il09-oracle': 'il09-oracle',
 'il09-lf-blockchain': 'il09-blockchain',
 'il09-cpp-python': 'il09-cpp-python',
 # IL-10
 'il-10-portfolio-career-professional-practice-math-quantreason': 'quantreason',
 'il10-fde-career': 'il10-fde',
 'il10-humanmetrics': 'il10-humanmetrics',
 'il10-entrepreneurship': 'il10-entrepreneur',
 'il10-quant-finance': 'il10-quantfin',
 # IL-11
 'il-11-zero-trust-endpoint-defense-math-numtheory': 'numtheory',
 'il-11-zero-trust-endpoint-defense-math-logic': 'logic',
 'il11-zero-trust-foundations--zt-perimeter-fall': 'il11-perimeter',
 'il11-zero-trust-foundations--zt-nist-tenets': 'il11-nist',
 'il11-zero-trust-foundations--zt-cisa-maturity': 'il11-cisa',
 'il11-zero-trust-foundations--zt-default-deny': 'il11-defaultdeny',
 'il11-network-crypto-foundations--zt-osi-tcpip': 'il11-osi',
 'il11-network-crypto-foundations--zt-hashing': 'il11-hashing',
 'il11-network-crypto-foundations--zt-encryption': 'il11-encrypt',
 'il11-active-directory-defense--zt-ad-structure': 'il11-adstruct',
 'il11-active-directory-defense--zt-ad-attacks': 'il11-adattacks',
 'il11-active-directory-defense--zt-ad-harden': 'il11-adharden',
 'il11-allowlisting-ringfencing--zt-allowlist': 'il11-allowlist',
 'il11-allowlisting-ringfencing--zt-ringfence': 'il11-ringfence',
 'il11-allowlisting-ringfencing--zt-storage-elevation': 'il11-storage',
 'il11-red-blue-operations--zt-social-engineering': 'il11-social',
 'il11-red-blue-operations--zt-web-attacks': 'il11-webattacks',
 'il11-red-blue-operations--zt-blue-detect': 'il11-bluedetect',
 'il11-cyber-hero-prep--zt-hero-review': 'il11-heroreview',
 'il11-cyber-hero-prep--zt-hero-scenarios': 'il11-heroscen',
 'il11-entra-identity--sc300-lifecycle': 'il11-lifecycle',
 'il11-entra-identity--sc300-zerotrust-ca': 'il11-ca',
 'il11-entra-identity--sc300-auth': 'il11-auth',
 'il11-entra-identity--sc300-hybrid': 'il11-hybrid',
 'il11-entra-identity--sc300-governance': 'il11-govern',
 'il11-entra-identity--sc300-troubleshoot': 'il11-trouble',
 'il11-entra-identity--sc300-exam-prep': 'il11-examprep',
 # IL-12
 'il-12-ai-engineering-math-linalg': 'linalg',
 'il-12-ai-engineering-math-stats': 'prob-stats',
 'il-12-ai-engineering-math-discrete': 'discrete',
 'aieng-python-foundations--py-syntax-core': 'py-syntax',
 'aieng-python-foundations--py-oop-modular': 'py-oop',
 'aieng-python-foundations--py-concurrency': 'py-concurrency',
 'aieng-python-foundations--py-genai-workflow': 'py-genai',
 'aieng-data-science--numpy-foundations': 'numpy',
 'aieng-data-science--pandas-wrangling': 'pandas',
 'aieng-data-science--viz-matplotlib-seaborn': 'viz',
 'aieng-data-science--statistics-for-ml': 'stats-ml',
 'aieng-data-science--model-dev-workflow': 'model-workflow',
 'aieng-data-science--sql-for-ai-engineers': 'sql-ai',
 'aieng-machine-learning--supervised-learning': 'supervised',
 'aieng-machine-learning--unsupervised-learning': 'unsupervised',
 'aieng-machine-learning--reinforcement-intro': 'rl-intro',
 'aieng-machine-learning--validation-tuning': 'validation',
 'aieng-machine-learning--feature-engineering': 'feature-eng',
 'aieng-machine-learning--evaluation-metrics': 'eval-metrics',
 'aieng-deep-learning--neural-foundations': 'neural',
 'aieng-deep-learning--backprop-optimization': 'backprop',
 'aieng-deep-learning--cnns': 'cnn',
 'aieng-deep-learning--sequence-models': 'seq-models',
 'aieng-deep-learning--regularization-tuning': 'regularization',
 'aieng-deep-learning--pytorch-workflows': 'pytorch',
 'aieng-generative-ai--transformers-attention': 'transformers',
 'aieng-generative-ai--gpt-vs-bert': 'gpt-bert',
 'aieng-generative-ai--gans-vaes': 'gan-vae',
 'aieng-generative-ai--diffusion-generation': 'diffusion',
 'aieng-generative-ai--prompt-engineering': 'prompt-eng',
 'aieng-generative-ai--llm-apis-rag': 'rag',
 'aieng-generative-ai--vecdb-depth': 'vecdb',
 'aieng-generative-ai--advanced-retrieval': 'adv-retrieval',
 'aieng-generative-ai--genai-finetuning': 'finetune',
 'aieng-generative-ai--multimodal-foundation-models': 'multimodal',
 'aieng-generative-ai--vision-speech-apps': 'vision-speech',
 'aieng-generative-ai--llm-alignment-rlhf-dpo': 'alignment',
 'aieng-nlp--text-preprocessing': 'text-prep',
 'aieng-nlp--tokenization-embeddings': 'tokenization',
 'aieng-nlp--nltk-classics': 'nltk',
 'aieng-nlp--sequence-models-nlp': 'seq-nlp',
 'aieng-nlp--hf-pipelines': 'hf',
 'aieng-agentic-ai--agent-architectures': 'agent-arch',
 'aieng-agentic-ai--tool-use': 'tool-use',
 'aieng-agentic-ai--mcp-protocol': 'mcp',
 'aieng-agentic-ai--langchain-autogen': 'langchain',
 'aieng-agentic-ai--context-engineering': 'context-eng',
 'aieng-agentic-ai--copilot-studio': 'copilot-studio',
 'aieng-agentic-ai--azure-ai-foundry': 'ai-foundry',
 'aieng-azure-ai-900--azure-ai-services': 'azure-services',
 'aieng-azure-ai-900--ml-concepts-azure': 'ml-azure',
 'aieng-azure-ai-900--responsible-ai': 'resp-ai',
 'aieng-azure-ai-900--cost-governance': 'cost-gov',
 'aieng-production--prod-mlops-framing': 'mlops-frame',
 'aieng-production--prod-serving': 'serving',
 'aieng-production--prod-monitoring': 'monitoring',
 'aieng-production--agentops-observability': 'agentops',
 'aieng-production--prod-cost-latency': 'cost-latency',
 'aieng-production--prod-red-team': 'red-team',
 'aieng-production--trajectory-eval-agents': 'traj-eval',
 'aieng-production--prod-pipelines': 'pipelines',
 'aieng-production--experiment-tracking-registry': 'exp-tracking',
 'aieng-production--feature-stores': 'feature-store',
 'aieng-production--data-centric-ai': 'data-centric',
 'aieng-production--edge-ondevice-ai': 'edge-ai',
 'aieng-capstone--capstone-framing': 'cap-framing',
 'aieng-capstone--capstone-build': 'cap-build',
 'aieng-capstone--capstone-eval': 'cap-eval',
 'aieng-capstone--capstone-deploy': 'cap-deploy',
 'aieng-capstone--capstone-rai': 'cap-rai',
 'aieng-capstone--capstone-portfolio': 'cap-portfolio',
 'aieng-agentic-ai--agent-autonomy-ceilings': 'autonomy',
}
