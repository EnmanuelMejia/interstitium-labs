#!/usr/bin/env python3
"""Build IL-30 post-quantum cryptography course JSON (schema v4)."""
import json, os

OUT = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-30-post-quantum-cryptography-quantum-safe.json"

def card(front, back):
    return {"front": front, "back": back}

def quiz(q, choices, answer, explain):
    return {"q": q, "choices": choices, "answer": answer, "explain": explain}

def drill(did, items):
    return {"id": did, "items": [{"prompt": p, "answer": a, "explain": e} for (p, a, e) in items]}

def lab(lid, brief, steps, deliverable, checkpoint):
    return {"id": lid, "brief": brief, "steps": steps, "deliverable": deliverable, "checkpoint": checkpoint}

def mock(q, choices, answer, explain):
    return {"q": q, "choices": choices, "answer": answer, "explain": explain}

def video(title, url, source, blurb, durationMin, order, watchBefore="notes"):
    return {"title": title, "url": url, "source": source, "blurb": blurb,
            "durationMin": durationMin, "order": order, "watchBefore": watchBefore,
            "verifiedUtc": "2026-10-09T00:00:00Z", "httpStatus": 200}

def pdf(title, url, source, blurb, pages=None):
    return {"title": title, "url": url, "source": source, "blurb": blurb,
            "pages": pages, "animated": False,
            "verifiedUtc": "2026-10-09T00:00:00Z", "httpStatus": 200}

def note(title, body):
    return {"title": title, "body": body}

FIPS203 = "https://csrc.nist.gov/pubs/fips/203/final"
FIPS204 = "https://csrc.nist.gov/pubs/fips/204/final"
FIPS205 = "https://csrc.nist.gov/pubs/fips/205/final"
PQCPROJ = "https://csrc.nist.gov/projects/post-quantum-cryptography"
OQSORG = "https://github.com/open-quantum-safe"
OQSPROV = "https://github.com/open-quantum-safe/oqs-provider"
KYBER = "https://pq-crystals.org/kyber"
DILITHIUM = "https://pq-crystals.org/dilithium/"
FALCON = "https://falcon-sign.info/"
SPHINCS = "https://sphincs.org/"
CBOM = "https://cyclonedx.org/capabilities/cbom/"
NCCOE = "https://www.nccoe.nist.gov/crypto-agility-considerations-migrating-post-quantum-cryptographic-algorithms"
KFCIPHER = "https://www.kfcipher.net/pqc-standards-tracker.jsp"
DHSQ = "https://www.dhs.gov/quantum"
TQI = "https://thequantuminsider.com/2026/08/07/post-quantum-cryptography-timelines/"
PQCNSA = "https://postquantum.com/quantum-policy/nsa-cnsa-2-0-pqc/"
AXEL = "https://axelspire.com/business/pqc-timeline-mandates/"
FNDSA = "https://www.digicert.com/blog/quantum-ready-fndsa-nears-draft-approval-from-nist"
FIPS206 = "https://freenode.net/article/nist-locks-fn-dsa-to-fixed-point-math-for-fips-206"
QSDFIPS = "https://quantumsecuritydefence.com/insights/nist-fips-standards/"
AWESOME = "https://github.com/interrato/awesome-post-quantum"

# =====================================================================
# M00 — Prereq math
# =====================================================================
M00 = {
 "id": "IL30-M00", "code": "IL-30",
 "title": "Prereq Math: Lattices, Modular Arithmetic & Error Distributions",
 "summary": "The mathematical spine of post-quantum cryptography: lattices and the shortest/closest vector problems, modular arithmetic and polynomial rings, and the discrete Gaussian error distributions that make Learning With Errors hard. Draws on IL-02 and IL-06 number-theory modules; every later ML-KEM/ML-DSA module assumes it.",
 "objectives": [
  "Define a lattice and state the SVP and CVP hard problems precisely",
  "Do arithmetic in Z_q and in the polynomial ring R_q = Z_q[x]/(x^256+1)",
  "Explain discrete Gaussian error distributions and why small errors are the secret sauce",
  "State the LWE problem and the Module-LWE generalization",
  "Recognize the worst-case to average-case reduction story: breaking random LWE breaks ALL lattice instances"
 ],
 "estimatedMinutes": 720, "weight": 1.0,
 "prerequisiteFor": ["IL30-M01","IL30-M03","IL30-M04","IL30-M05","IL30-M06","IL30-M11"],
 "crossLinks": [
  {"course": "IL-02", "module": "il-02-mathematical-maturity-engine-math-logic", "note": "logic and proof spine under the hardness arguments"},
  {"course": "IL-06", "module": "il-06-cybersecurity-secure-engineering-math-numtheory", "note": "number theory and modular arithmetic foundation"},
  {"course": "IL-11", "module": "il11-network-crypto-foundations--zt-encryption", "note": "classical encryption context that PQC replaces"},
  {"course": "IL-23", "module": "m23-quantum", "note": "the quantum computing basics behind the threat model"}
 ],
 "cards": [
  card("What is a lattice (in cryptography)?", "A discrete additive subgroup of R^n: all integer linear combinations of n linearly independent basis vectors. Think 'all points on an infinite regular grid' — and two very different bases can describe the same grid."),
  card("SVP and CVP: state both hard problems.", "SVP (Shortest Vector Problem): given a basis of a lattice, find the shortest non-zero lattice vector. CVP (Closest Vector Problem): given a lattice and a target point, find the lattice vector closest to it. Approximate versions (GapSVP_gamma) are NP-hard."),
  card("Why do two bases for the same lattice matter for crypto?", "A 'good' basis (short, nearly orthogonal vectors) makes SVP/CVP easy; a 'bad' basis (long, skewed vectors) hides the structure. Crypto publishes the bad basis as the public key and keeps the good basis (or trapdoor) as the secret."),
  card("What is Z_q?", "The ring of integers modulo q: {0, 1, ..., q-1} with addition and multiplication reduced mod q. ML-KEM uses q = 3329; ML-DSA uses q = 8380417. Mod-q reduction keeps every value in a fixed small range."),
  card("What is the ring R_q = Z_q[x]/(x^256 + 1) used in ML-KEM?", "Polynomials of degree < 256 with coefficients in Z_q, multiplied then reduced modulo x^256+1 (the reduction rule: x^256 = -1). One ring element packs 256 coefficients — this is where Kyber's efficiency comes from."),
  card("What is a discrete Gaussian error distribution?", "A probability distribution over the integers shaped like a bell curve (parameter sigma), outputting small values with high probability. LWE adds small Gaussian noise e to a linear equation so the secret can't be solved for directly."),
  card("State the LWE problem (informal).", "Given many samples (a_i, b_i = <a_i, s> + e_i mod q) with random a_i and small errors e_i, recover the secret vector s. Without the error it's linear algebra; with small errors it is believed hard even for quantum computers."),
  card("What does 'worst-case to average-case reduction' buy us?", "Regev's reduction: if you can solve RANDOM LWE instances efficiently, you can solve the WORST-CASE lattice problem (GapSVP). So the crypto is as hard as the hardest lattice instance — the strongest security foundation in practical crypto."),
  card("Module-LWE vs plain LWE: what changes?", "Plain LWE works over vectors in Z_q^n. Module-LWE works over vectors of ring elements in R_q^k — algebraic structure for efficiency. Module rank k tunes the security/efficiency tradeoff: ML-KEM uses k = 2, 3, 4 for the 512/768/1024 sets."),
  card("Why do lattice schemes get called 'post-quantum' rather than 'quantum-proof'?", "No efficient quantum algorithm is known for approximate lattice problems (the best quantum speedups are modest, unlike Shor's exponential break of factoring). 'Post-quantum' = no known quantum attack; 'proof' would be a claim no one honest makes.")
 ],
 "quiz": [
  quiz("A lattice basis is published as the public key. Why must it be a 'bad' basis?",
       ["Bad bases are shorter and easier to transmit", "A good (short, orthogonal) basis would let anyone solve SVP/CVP and recover the secret", "The key-generation algorithm cannot produce good bases", "Bad bases are required by the FIPS for interoperability"],
       1, "The whole trapdoor idea: public = bad basis (hides structure), secret = good basis/trapdoor (solves the hard problem). Publish the good one and there is no security."),
  quiz("In ML-KEM's ring R_q = Z_q[x]/(x^256+1) with q = 3329, what does multiplying two ring elements give?",
       ["A polynomial of degree up to 510 with integer coefficients", "A polynomial of degree < 256 with coefficients reduced mod 3329", "A 256-bit integer", "A vector in Z_3329^512"],
       1, "Reduction modulo x^256+1 (x^256 = -1) folds higher-degree terms back down, so the product stays a degree-<256 polynomial with coefficients mod 3329."),
  quiz("Why is the error e in LWE samples essential to security?",
       ["It pads the message to a fixed block size", "Without noise, b = <a,s> is a linear system solvable by Gaussian elimination — the small error makes that impossible", "It provides the random seed for key generation", "It encrypts the modulus q"],
       1, "Strip the error and LWE is undergraduate linear algebra. Small-but-present noise is exactly what pushes the problem from easy to (believed) quantum-hard."),
  quiz("Regev's worst-case to average-case reduction means:",
       ["Average lattice instances are harder than worst-case ones", "Breaking random LWE instances would imply breaking the hardest lattice instances — the security claim is maximally strong", "Worst-case keys are weaker and must be rejected", "LWE security reduces to the average case of RSA"],
       1, "This is the celebrated foundation of lattice crypto: random-instance hardness inherits worst-case hardness. RSA/factoring has no comparable reduction."),
  quiz("Module-LWE with rank k=3 in ML-KEM-768 roughly means:",
       ["Three independent AES keys are combined", "The scheme works with vectors of 3 ring elements — larger k buys more security at more cost", "The security level is 3 bits", "Three moduli are used in parallel"],
       1, "Rank k scales the lattice dimension (k*256): ML-KEM-512/768/1024 use k=2/3/4. Bigger k = harder lattice = bigger keys and ciphertexts.")
 ],
 "drills": [
  drill("il30-m00-drill1", [
   ("Define a lattice in one sentence.", "All integer linear combinations of n independent basis vectors — a regular infinite grid in n dimensions.", "Basis first, then the set it generates."),
   ("SVP vs CVP: which asks for the nearest vector to a target?", "CVP (Closest Vector Problem); SVP asks for the shortest non-zero lattice vector.", "Target point present = CVP."),
   ("State the modulus q used by ML-KEM and by ML-DSA.", "ML-KEM: q = 3329. ML-DSA: q = 8380417.", "These are FIPS-fixed constants, not choices.")
  ]),
  drill("il30-m00-drill2", [
   ("Write the LWE sample equation.", "b = <a, s> + e (mod q), with random a, secret s, small error e.", "The +e is the entire security story."),
   ("Why does plain linear algebra fail on LWE samples?", "The small unknown error e on each sample breaks exact elimination — you cannot solve for s exactly.", "Approximate equations are not solvable by elimination."),
   ("What security property does the worst-case/average-case reduction give?", "Random-instance hardness is as strong as worst-case lattice hardness.", "Maximal foundation strength in practical crypto.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m00-lab",
  "You will implement arithmetic in Z_q and in the toy ring Z_17[x]/(x^4+1) in Python, generate LWE-style samples (a, b = a*s + e mod q) for a tiny modulus, and run a brute-force secret-recovery attack that succeeds at toy sizes but visibly explodes as the dimension grows — making the hardness claim concrete.",
  [
   "Implement mod_q add/mul and polynomial multiplication with reduction mod x^4+1 over Z_17 in a single Python file.",
   "Generate 200 LWE samples with secret s (dimension 4), errors drawn from {-1, 0, 1}; verify b = a·s + e mod 17.",
   "Write a brute-force loop over all 17^4 possible secrets; time it, then extrapolate the runtime to dimension 256 — record the number.",
   "Plot the error distribution histogram and confirm >90% of errors are in {-1,0,1}; note how error size controls sample 'noisiness'."
  ],
  "A Python file plus a short writeup: working ring arithmetic, a timed brute-force attack with the dimension-256 extrapolation, and the error histogram.",
  "Ring arithmetic passes self-tests; brute force recovers the toy secret; the extrapolation shows infeasibility at real dimensions; error histogram is concentrated near zero."
 ),
 "mockTask": mock(
  "A vendor claims their 'quantum-proof lattice cipher' uses plain LWE with NO error term for speed. What is the correct engineering response?",
  ["Approve it — lattice is lattice", "Reject it: without the error term the scheme is plain linear algebra and the secret recovers by Gaussian elimination", "Approve with smaller keys", "Ask for a bigger modulus"],
  1,
  "b = <a,s> with no noise is a linear system — seconds to solve. The small error is load-bearing; removing it removes the security. This is exactly the kind of claim the math module trains you to kill on sight."),
 "videos": [
  video("NIST FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard", FIPS203, "NIST CSRC", "The published standard for ML-KEM: read the parameter sets and the encapsulation interface straight from the source.", 45, 1),
  video("NIST Post-Quantum Cryptography project page", PQCPROJ, "NIST CSRC", "The project's home: competition history, selected algorithms, drafts, and the standardization timeline.", 20, 2)
 ],
 "pdfs": [
  pdf("NIST FIPS 203 (ML-KEM) — official publication", FIPS203, "NIST CSRC", "The final standard: algorithms, parameter sets ML-KEM-512/768/1024, KATs. Retrieved 2026-10-09."),
  pdf("PQC standards tracker — FIPS 203/204/205/206 and HQC status", KFCIPHER, "KFCipher", "Status board for the whole NIST PQC portfolio: final, draft, selected, and candidate algorithms with timelines. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("Why lattices survive quantum computers", "Shor's algorithm exploits the hidden-subgroup structure of factoring and discrete logs — periodic structure a quantum computer can find with the quantum Fourier transform. Approximate lattice problems (GapSVP, SIVP, LWE) have no known periodic structure to exploit: the best quantum algorithms give at most modest (subexponential, often polynomial-factor) speedups, not the exponential collapse Shor delivers. That asymmetry — exponential break for RSA/ECC, no known break for lattices — is the entire bet behind the NIST selections. 'Believed hard' is doing real work here: it is a belief backed by 25+ years of failed cryptanalysis, plus the worst-case/average-case reduction that RSA never had."),
  note("The ring R_q = Z_q[x]/(x^256+1), concretely", "Take polynomials with coefficients mod q and degree under 256. Multiply normally, then wherever you see x^256, replace it with -1 (so x^257 becomes -x, x^258 becomes -x^2, and so on) and reduce every coefficient mod q. Example over a toy ring: (2x + 3)(x^3 + 1) in Z_5[x]/(x^4+1) = 2x^4 + 3x^3 + 2x + 3 → 2x^4 becomes 2·(-1) = -2 → result 3x^3 + 2x + 1 (mod 5). Kyber's real ring uses n=256, q=3329 — and crucially x^256+1 splits nicely for the Number Theoretic Transform, which makes multiplication fast. The NTT is why Kyber/Dilithium are practical at TLS speeds."),
  note("Discrete Gaussians and why 'small' matters", "An LWE error is drawn from a distribution concentrated near zero (parameter sigma ≈ 2-3 for Kyber's binomial approximation of a Gaussian). Small errors mean: (1) decryption works — the receiver rounds away the noise; (2) the attacker cannot — recovering s from noisy equations is the hard problem. If errors were large, decryption would fail; if zero, it's linear algebra. Parameter design is the art of parking the error exactly in the band where honest parties succeed and attackers fail — and the FIPS parameter sets are the settled, reviewed choices. Never re-tune them.")
 ]
}

# =====================================================================
# M01 — Quantum threat model
# =====================================================================
M01 = {
 "id": "IL30-M01", "code": "IL-30",
 "title": "The Quantum Threat Model: Shor, Grover & Harvest-Now-Decrypt-Later",
 "summary": "Exactly what a cryptographically relevant quantum computer breaks, what it merely weakens, and why the migration deadline is driven by data lifetime — not by the day the machine arrives. Mosca's inequality made operational.",
 "objectives": [
  "State precisely which primitives Shor's algorithm breaks: RSA, finite-field DH, ECDSA, ECDH, DSA",
  "Quantify Grover's effect: AES-128 drops to ~64-bit effective strength; AES-256 stays viable",
  "Explain harvest-now-decrypt-later and why it moves the deadline earlier",
  "Apply Mosca's inequality (x + y > z) to decide migration urgency for a data class",
  "Debunk the 'we'll wait for Q-day' fallacy with the shelf-life argument"
 ],
 "estimatedMinutes": 600, "weight": 1.0,
 "prerequisiteFor": ["IL30-M02","IL30-M07","IL30-M08","IL30-M13"],
 "crossLinks": [
  {"course": "IL-23", "module": "m23-quantum", "note": "qubit/superposition/entanglement physics behind Shor and Grover"},
  {"course": "IL-11", "module": "il11-network-crypto-foundations--zt-encryption", "note": "the classical encryption being threatened"},
  {"course": "IL-06", "module": "il-06-cybersecurity-secure-engineering-math-numtheory", "note": "factoring/discrete-log math that Shor destroys"}
 ],
 "cards": [
  card("Which classical primitives does Shor's algorithm break?", "Integer factorization (RSA) and the discrete logarithm problem — finite-field DH/DSA and elliptic-curve ECDSA/ECDH/EdDSA. All public-key crypto in wide use except hash-based and lattice schemes."),
  card("What does Shor's algorithm do, in one line?", "Finds the period of a modular-exponentiation function in polynomial time via the quantum Fourier transform — and period-finding reduces both factoring and discrete logs."),
  card("What is Grover's algorithm's effect on symmetric crypto?", "Quadratic speedup of brute-force search: an n-bit key offers ~n/2 bits of security against Grover. AES-128 → ~64 bits (inadequate); AES-256 → ~128 bits (fine). Double key lengths, don't panic."),
  card("Grover vs hash functions?", "Grover halves preimage resistance (SHA-256 → ~128-bit preimage). Collision resistance falls to ~n/3 via the Brassard-Høyer-Tapp quantum collision algorithm — SHA-384/SHA-512 are the CNSA 2.0 answers."),
  card("What is harvest-now-decrypt-later (HNDL)?", "Adversaries record encrypted traffic today and decrypt it once a cryptographically relevant quantum computer exists. Data with long secrecy lifetimes is ALREADY at risk."),
  card("State Mosca's inequality and its terms.", "x + y > z means act now: x = years your data must stay secret (shelf life), y = years to migrate to PQC, z = years until a quantum break. If secrecy + migration time exceeds time-to-break, you are already late."),
  card("Why doesn't 'no quantum computer exists yet' justify waiting?", "Two reasons: HNDL (captured traffic is a ticking asset) and migration lead time (large orgs need 5-10 years; protocols, firmware, and hardware turn over slowly). The deadline is x + y, not z."),
  card("Which systems are HIGHEST priority for PQC migration?", "Long-lived secrets in transit or at rest under RSA/ECC: state secrets, health records, firmware signing keys, root CAs, VPN tunnels carrying sensitive data, anything with >10-year confidentiality needs."),
  card("Does Shor break AES?", "No. Shor attacks the algebraic structure of factoring/discrete-log. Symmetric ciphers and hashes have no such structure; Grover is the relevant (and far weaker) quantum threat there.")
 ],
 "quiz": [
  quiz("A hospital encrypts patient archives with RSA-2048 key transport. The data must stay confidential 25 years. Why is this a PQC priority NOW?",
       ["RSA-2048 is already classically broken", "Harvest-now-decrypt-later: captured ciphertexts can be stored and decrypted by a future quantum computer, and 25-year secrecy far exceeds any migration schedule", "AES is also broken by Shor", "Hospitals are legally required to use ML-KEM today"],
       1, "HNDL plus long shelf life is the textbook trigger. The migration deadline precedes the quantum computer by the data's secrecy lifetime."),
  quiz("Grover's algorithm against AES-256 leaves approximately what effective security?",
       ["256 bits — Grover doesn't affect AES", "~128 bits — the quadratic speedup halves the exponent, which remains acceptable", "~64 bits — AES-256 must be abandoned", "~192 bits"],
       1, "Quadratic speedup: 2^256 search becomes ~2^128 operations. 128-bit quantum security is the CNSA 2.0 bar — AES-256 clears it; AES-128 at ~64 bits does not."),
  quiz("Mosca's inequality x + y > z: an org needs 15-year secrecy (x), 8-year migration (y), and estimates 20 years to a quantum break (z). Verdict?",
       ["Safe — 20 > 8", "Act now — 15 + 8 = 23 > 20, already late by the inequality", "Wait 5 years then decide", "Only migrate the 15-year data"],
       1, "23 > 20: the inequality fires. Even with a 20-year z estimate, the sum of secrecy and migration time already exceeds it."),
  quiz("Which of these is NOT broken by Shor's algorithm?",
       ["RSA-3072", "ECDSA P-256", "Finite-field Diffie-Hellman", "SHA-256 preimage resistance"],
       3, "Shor targets factoring and discrete logs. Hash preimage is Grover's domain (quadratic, not exponential) — SHA-256 keeps ~128-bit quantum preimage resistance."),
  quiz("The Brassard-Høyer-Tapp result matters for migration because:",
       ["It breaks lattice cryptography", "Quantum collision-finding runs in ~2^(n/3), so collision resistance needs bigger hashes — one reason CNSA 2.0 specifies SHA-384/512", "It makes Shor's algorithm obsolete", "It proves AES-128 is quantum-safe"],
       1, "BHT gives cube-root collision attacks: SHA-256's 128-bit classical collision resistance drops to ~85-bit quantum. CNSA 2.0's SHA-384/512 requirement follows directly.")
 ],
 "drills": [
  drill("il30-m01-drill1", [
   ("Name the three families Shor breaks.", "RSA (factoring), finite-field DH/DSA (discrete log), elliptic-curve ECDSA/ECDH/EdDSA (elliptic-curve discrete log).", "Factoring + two flavors of discrete log."),
   ("Grover's speedup in one phrase?", "Quadratic: n-bit key → ~n/2-bit quantum security.", "Square root of the search space."),
   ("Define HNDL in one sentence.", "Record encrypted traffic now; decrypt later with a quantum computer.", "The deadline-mover.")
  ]),
  drill("il30-m01-drill2", [
   ("Mosca: x=10, y=7, z=25. Migrate now?", "No: 10+7=17 < 25 — margin exists, but start planning; estimates of z are the weak input.", "Compute x+y vs z."),
   ("Mosca: x=30 (state secret), y=10, z=25. Verdict?", "Act now: 40 > 25 — badly late already.", "Long secrecy dominates."),
   ("Which data class migrates first: 2-year marketing emails or 20-year firmware signing keys?", "Firmware signing keys: long trust lifetime plus code-signing is a signature (not just confidentiality) problem.", "Lifetime × blast radius.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m01-lab",
  "You will build a Mosca-inequality worksheet for a fictional company: classify 12 data assets by secrecy lifetime (x) and crypto in use, estimate migration time (y) per asset class, and compute which assets are already past the migrate-now line under three z scenarios (optimistic 25y, central 15y, pessimistic 10y). Deliverable is a prioritized migration queue with the math shown.",
  [
   "List 12 assets (TLS private keys, DB backups, firmware signing key, VPN PSKs, code-signing cert, archived PII, etc.) with current algorithm and secrecy lifetime x.",
   "Assign each a migration time y (protocol change = 2y, firmware fleet = 6y, PKI root rotation = 4y — justify each).",
   "Compute x+y vs z for z in {10, 15, 25}; flag every asset where x+y > z under the central scenario.",
   "Write the one-page executive summary: top-5 queue, and the sentence that kills the 'wait for Q-day' objection."
  ],
  "mosca-worksheet.md: the asset table with x/y/z math, the prioritized queue, and the executive summary.",
  "Every asset has x, y, and three z-comparisons; the queue order follows the math; the summary states the HNDL argument in one paragraph."
 ),
 "mockTask": mock(
  "Your CISO says: 'No quantum computer can break RSA today, so PQC migration can wait until one is announced.' Using HNDL and Mosca's inequality, what is the flaw?",
  ["There is no flaw — the CISO is right", "Two flaws: (1) HNDL means adversaries are already collecting today's RSA-encrypted traffic for future decryption; (2) Mosca's x+y>z shows migration must START years before the break, not after the announcement", "The flaw is that RSA is already classically broken", "The flaw is only about signatures, not encryption"],
  1,
  "The announcement-day framing ignores both the adversary's head start (recorded ciphertext) and your own lead time (multi-year migration). The deadline is x+y, never z."),
 "videos": [
  video("NIST PQC project — why the migration starts before the quantum computer", PQCPROJ, "NIST CSRC", "The official framing: standards now, because HNDL and migration lead times move the deadline earlier.", 20, 1),
  video("DHS post-quantum cryptography roadmap", DHSQ, "DHS", "The federal roadmap view: inventory, prioritize, migrate — the operational translation of Mosca's inequality.", 25, 2)
 ],
 "pdfs": [
  pdf("NIST PQC project page — standards and timeline", PQCPROJ, "NIST CSRC", "Competition history, final standards, drafts. Retrieved 2026-10-09."),
  pdf("PQC migration timelines 2026–2035 (mandates mapped)", TQI, "The Quantum Insider", "CNSA 2.0, NSM-10, IR 8547, and EU timelines in one map. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("Shor, precisely", "Shor's algorithm (1994) solves integer factorization and discrete logarithms in polynomial time on a quantum computer: O((log N)^3) gate operations. The mechanism: reduce factoring to period-finding (find r with a^r ≡ 1 mod N), then use the quantum Fourier transform to extract the period exponentially faster than any known classical method. RSA-2048 falls to ~4000 logical qubits running ~10^8-10^9 gates — a machine that does not exist yet, but the algorithm is 30 years old and its resource estimates only shrink. Every cryptosystem whose security reduces to factoring or discrete logs — RSA, DH, DSA, ECDSA, ECDH, EdDSA — is in the blast radius. Nothing about bigger RSA keys helps: Shor is polynomial, so doubling key size barely moves the attack cost."),
  note("Grover, precisely, and the 'just double it' rule", "Grover's algorithm (1996) searches an unsorted space of N items in O(√N) quantum queries — a quadratic speedup over classical brute force, and provably optimal for unstructured search. Consequence: symmetric key strength halves in bits (AES-128 → 64-bit quantum security: broken; AES-256 → 128-bit: fine). Hash preimage resistance halves the same way; collision resistance falls further, to ~n/3 via Brassard–Høyer–Tapp. The engineering rule is boring and correct: AES-256, SHA-384/512 — which is exactly what CNSA 2.0 mandates. No new primitives needed on the symmetric side, just parameter discipline."),
  note("Mosca's inequality as a planning tool", "x + y > z ⇒ migrate now. x: how long data must stay secret. y: how long migration takes YOUR org (discovery, testing, rollout, fleet turnover). z: years until a cryptographically relevant quantum computer. The inequality's power is that it converts an unknowable (z) into a decision rule: pick your z estimate, and the assets whose x+y exceeds it are already late. Note the asymmetry: underestimating z is catastrophic (silent HNDL exposure), overestimating it just means you migrated early — and early migration buys crypto-agility anyway. Run it per data class, not per company: the 25-year firmware key and the 2-year session token live in different universes.")
 ]
}

# =====================================================================
# M02 — NIST PQC competition history
# =====================================================================
M02 = {
 "id": "IL30-M02", "code": "IL-30",
 "title": "NIST PQC Competition: From the 2016 Call to Final Standards",
 "summary": "The decade-long standardization marathon: the 2016 call, 82 submissions, three rounds of cryptanalysis, the 2022 selections, the SIKE break that proved the process works, and the August 13, 2024 finals. Plus the live pipeline: FIPS 206, HQC, and the additional-signatures round.",
 "objectives": [
  "Narrate the competition timeline: 2016 call → 69 first-round candidates → rounds 2/3 → 2022 selection → 2024 finals",
  "Explain why the SIKE break (2022) validates rather than undermines the process",
  "State the current status of every algorithm: final, in-standardization, or candidate",
  "Distinguish FIPS 203/204/205 by role: KEM, primary signatures, conservative backup",
  "Track the live pipeline: FN-DSA/FIPS 206 draft, HQC selection, additional signature round"
 ],
 "estimatedMinutes": 540, "weight": 0.9,
 "prerequisiteFor": ["IL30-M03","IL30-M04","IL30-M05","IL30-M06","IL30-M13"],
 "crossLinks": [
  {"course": "IL-29", "module": "IL29-M33", "note": "Security+ cert-track module — crypto domain context"},
  {"course": "IL-23", "module": "m23-quantum", "note": "quantum basics behind why the competition existed"}
 ],
 "cards": [
  card("When did NIST start PQC standardization, and how many submissions arrived?", "Call for proposals December 2016; 82 submissions, 69 accepted as first-round candidates in 2017."),
  card("Which four algorithms did NIST select in July 2022?", "CRYSTALS-Kyber (KEM), CRYSTALS-Dilithium, Falcon, and SPHINCS+ (signatures). Kyber/Dilithium/SPHINCS+ became FIPS 203/204/205; Falcon became FN-DSA/FIPS 206 (in draft)."),
  card("What happened to SIKE, and why is that GOOD news?", "SIKE (isogeny-based) was broken classically in 2022 by Castryck-Decru using a 1990s-era theorem — before standardization. The multi-year public cryptanalysis did exactly its job: weak candidates die in the open, not in your products."),
  card("What are the three FINAL FIPS and their dates?", "FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) — all published August 13, 2024."),
  card("Why did NIST standardize BOTH lattice signatures (ML-DSA) and hash-based signatures (SLH-DSA)?", "Assumption diversity: ML-DSA is fast and the general default; SLH-DSA rests only on hash-function security — a conservative backup if lattice assumptions ever weaken."),
  card("What is HQC's status?", "Selected March 2025 as the backup KEM for standardization (code-based, Hamming Quasi-Cyclic); draft standard expected, final ~2026-2027. Not yet a FIPS — do not cite it as one."),
  card("What is FN-DSA / FIPS 206's status?", "Falcon-based signature standard: draft FIPS 206 submitted August 2025 as Initial Public Draft; final expected late 2026/early 2027. Fixed-point arithmetic mandated in the draft. Compact signatures for constrained/firmware use."),
  card("What is the additional-signatures round?", "NIST's ongoing second track for more signature diversity (call 2023, round-2 candidates under evaluation through 2026 — e.g., the HAWK withdrawal shows live cryptanalysis). Nothing there is deployable yet."),
  card("Why 'teach to the standard, not the candidate'?", "Candidates change status (SIKE died, HAWK withdrew, Falcon's spec moved to fixed-point). Final FIPS are the stable engineering target; everything else is tracked, not built on.")
 ],
 "quiz": [
  quiz("The SIKE break is best described as:",
       ["Proof that post-quantum cryptography is impossible", "The standardization process working as designed: years of public cryptanalysis killed a weak candidate before it shipped in standards", "A quantum computer breaking its first cipher", "A reason to distrust all NIST selections"],
       1, "SIKE was broken by classical math, in the open, pre-standardization. That is the filter functioning — contrast with a break discovered after deployment."),
  quiz("Which statement about the August 2024 finals is accurate?",
       ["FIPS 203/204/205/206 all published together", "FIPS 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA) published August 13, 2024; FIPS 206 (FN-DSA) remained in draft", "Only FIPS 203 was finalized", "The finals were delayed to 2025"],
       1, "Three finals in August 2024. FIPS 206's IPD came about a year later (Aug 2025 submission); final expected late 2026/early 2027."),
  quiz("An architect proposes deploying HQC in production today citing 'NIST selection.' What is wrong?",
       ["Nothing — selection equals standardization", "HQC was selected (March 2025) but is not a final FIPS; deploying pre-standard algorithms risks spec churn and no FIPS validation path", "HQC is a signature scheme, not a KEM", "HQC was rejected"],
       1, "Selected ≠ standardized. The draft is still being written; parameters, OIDs, and KATs can move. Track it; build on FIPS 203/204/205."),
  quiz("Why two lattice-based standards (ML-KEM for encryption, ML-DSA for signatures) instead of one scheme for both?",
       ["Marketing", "KEMs and signatures have different security properties and use patterns; ML-KEM (Kyber) is optimized for key establishment, ML-DSA (Dilithium) for signing — each is the best-of-breed in its role", "NIST was required by law to pick two", "They are actually the same algorithm"],
       1, "Different jobs, different optima. Kyber's FO-transform KEM and Dilithium's Fiat–Shamir signatures are each the reviewed leader for their function."),
  quiz("The additional-signatures track exists because:",
       ["ML-DSA was found broken", "NIST wants more signature diversity beyond lattices — different hard problems (codes, isogenies, multivariate, symmetric-based) as insurance", "The 2022 selections were all hash-based", "Vendors demanded more options"],
       1, "Defense in depth at the assumption level: if one mathematical family ever weakens, the portfolio survives. The track is insurance, evaluated slowly and publicly.")
 ],
 "drills": [
  drill("il30-m02-drill1", [
   ("2016 → 2022 → 2024: name the three milestones.", "2016: call for proposals. 2022: four selections (Kyber, Dilithium, Falcon, SPHINCS+). 2024: FIPS 203/204/205 published.", "Call, select, publish."),
   ("SIKE: broken by what, and when in the process?", "Classically broken (Castryck-Decru, 2022) — during evaluation, before standardization.", "Pre-standard kill = process working."),
   ("Map: 203/204/205 → algorithm → role.", "203 ML-KEM (key establishment), 204 ML-DSA (primary signatures), 205 SLH-DSA (conservative hash-based backup).", "KEM, sig, backup-sig.")
  ]),
  drill("il30-m02-drill2", [
   ("Status check: FN-DSA.", "FIPS 206 in draft (IPD submitted Aug 2025); final expected late 2026/early 2027. Not final.", "Draft, not final."),
   ("Status check: HQC.", "Selected March 2025 for KEM standardization; draft in progress. Not final.", "Selected, not standardized."),
   ("One-sentence rule for what to build on today?", "Build on final FIPS 203/204/205; track everything else.", "Finals are the target.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m02-lab",
  "You will build a standards-status tracker: a one-page document (or spreadsheet) listing every NIST PQC algorithm (ML-KEM, ML-DSA, SLH-DSA, FN-DSA, HQC, and the additional-signature round-2 candidates), each with current status, FIPS number if any, role, and a 'safe to build on?' verdict with the date you checked. You will re-verify each status against a primary source.",
  [
   "Create the tracker table with columns: algorithm, type, FIPS #, status, role, build-verdict, source URL, checked date.",
   "Verify FIPS 203/204/205 publication facts against the NIST CSRC publication pages.",
   "Verify FN-DSA and HQC status against current NIST announcements (note the fixed-point change for FIPS 206).",
   "Write the verdict column honestly: 'final — build', 'draft — experiment only', 'candidate — track only'.",
   "Set a calendar reminder: re-verify quarterly; standards move."
  ],
  "standards-tracker.md: the verified table with primary-source URLs and the quarterly re-check reminder.",
  "Every row cites a primary source with a check date; no 'selected' algorithm is labeled 'final'; the re-check reminder is set."
 ),
 "mockTask": mock(
  "A vendor slide deck claims 'NIST-approved FIPS 206 FN-DSA signatures' as a shipping feature in Q4 2026. Your assessment?",
  ["Accurate — approve the claim", "Inaccurate: FIPS 206 was in Initial Public Draft as of late 2025 with final expected late 2026/early 2027; calling a draft 'approved' misrepresents its status — require the vendor to correct it", "Accurate if they use the IPD text", "Irrelevant — signatures don't need standards"],
  1,
  "Draft ≠ approved. The compliance note from the standards trackers is explicit: do not cite HQC or FN-DSA as 'NIST-approved' without noting draft/selected status."),
 "videos": [
  video("NIST PQC standards: FIPS 203/204/205 — what the three standards cover and what they don't", QSDFIPS, "Quantum Security Defence", "The three finals plus the pipeline (FIPS 206, HQC): what each standard covers and the hybrid/transition documents around them.", 30, 1),
  video("PQC standards tracker — portfolio status board", KFCIPHER, "KFCipher", "Every algorithm's current status (final/draft/selected/candidate) with primary NIST links — the compliance-safe reference.", 15, 2)
 ],
 "pdfs": [
  pdf("NIST FIPS 203/204/205 — official publication pages", FIPS203, "NIST CSRC", "Start here; 204 and 205 at /pubs/fips/204/final and /pubs/fips/205/final. Retrieved 2026-10-09."),
  pdf("FN-DSA nears draft approval — FIPS 206 timeline", FNDSA, "DigiCert", "Draft submitted Aug 28, 2025; IPD review ~1 year; final expected late 2026/early 2027. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("The competition, beat by beat", "December 2016: NIST calls for quantum-resistant public-key proposals. Late 2017: 69 first-round candidates (encryption/KEM and signatures). 2019: 26 advance to round 2. 2020: 7 finalists + 8 alternates to round 3 — the alternates kept alive deliberately as insurance. July 2022: NIST selects Kyber (KEM) plus Dilithium, Falcon, SPHINCS+ (signatures); four round-4 KEM candidates (BIKE, Classic McEliece, HQC, SIKE) continue. August 2022: SIKE falls to classical cryptanalysis — the filter working in public. August 2023: draft standards published for comment. August 13, 2024: FIPS 203/204/205 final. March 2025: HQC selected for KEM standardization. August 2025: FIPS 206 (FN-DSA) draft submitted. The pattern to internalize: NIST standardizes slowly, publicly, and kills candidates in the open — that slowness is the security feature."),
  note("Why the process deserves your trust (and its limits)", "Three properties make the NIST process the best available basis for engineering decisions: (1) adversarial review at scale — thousands of cryptanalyst-years across three rounds, with real kills (SIKE, Rainbow in round 3); (2) diversity of assumptions — lattices, hashes, codes, and a second signature track, so no single mathematical break sinks the portfolio; (3) conservative parameter choices — NIST picked security margins, not speed records. The limits are honest too: 'no known attack' is not 'no attack', implementations (not math) are where real systems usually fail, and the standards are young — which is exactly why hybrids and crypto-agility are part of the migration doctrine, not optional extras."),
  note("Reading a status correctly: candidate vs selected vs draft vs final", "Candidate: under evaluation, may die (most do). Selected: NIST intends to standardize; the spec is still being written and CAN change (Falcon's move to fixed-point arithmetic in FIPS 206 is the live example). Draft (IPD): public text under comment; close to final but OIDs, KATs, and details can move. Final FIPS: the stable target — validated implementations, procurement language, and compliance regimes can reference it. The expensive deployment errors come from treating 'selected' as 'final'. Your tracker (the lab) exists to make that mistake structurally impossible.")
 ]
}

# =====================================================================
# M03 — ML-KEM (Kyber)
# =====================================================================
M03 = {
 "id": "IL30-M03", "code": "IL-30",
 "title": "ML-KEM (Kyber): Module-Lattice Key Encapsulation in Depth",
 "summary": "FIPS 203 end to end: the K-PKE encryption core, the Fujisaki–Okamoto transform to CCA security, parameter sets ML-KEM-512/768/1024 with exact key and ciphertext sizes, the encapsulation protocol, decapsulation failure behavior, and the misuse cases that void the security story.",
 "objectives": [
  "Describe the ML-KEM protocol: KeyGen, Encaps, Decaps and what each party holds",
  "Explain the K-PKE core and the Fujisaki–Okamoto transform (implicit rejection)",
  "State exact sizes: public keys 800/1184/1568 B, ciphertexts 768/1088/1568 B for 512/768/1024",
  "Map parameter sets to NIST security levels 1/3/5 and choose correctly",
  "Identify misuse: non-ephemeral key reuse patterns, keygen randomness failures, and timing side channels"
 ],
 "estimatedMinutes": 660, "weight": 1.0,
 "prerequisiteFor": ["IL30-M07","IL30-M09","IL30-M11","IL30-M12"],
 "crossLinks": [
  {"course": "IL-11", "module": "il11-network-crypto-foundations--zt-encryption", "note": "classical key exchange that ML-KEM replaces"},
  {"course": "IL-06", "module": "il-06-cybersecurity-secure-engineering-math-numtheory", "note": "modular arithmetic behind the ring operations"}
 ],
 "cards": [
  card("What is a KEM (key encapsulation mechanism)?", "A three-algorithm primitive: KeyGen → (pk, sk); Encaps(pk) → (ciphertext, shared secret); Decaps(sk, ciphertext) → shared secret. Unlike Diffie-Hellman there is no interactive exchange — one party encapsulates to the other's public key."),
  card("ML-KEM parameter sets and NIST levels?", "ML-KEM-512 (level 1 ≈ AES-128), ML-KEM-768 (level 3 ≈ AES-192), ML-KEM-1024 (level 5 ≈ AES-256). ML-KEM-768 is the recommended default."),
  card("Exact ML-KEM sizes (public key / ciphertext)?", "512: pk 800 B, ct 768 B. 768: pk 1184 B, ct 1088 B. 1024: pk 1568 B, ct 1568 B. Secret keys: 1632/2400/3168 B. These sizes drive every protocol-integration decision (TLS, X.509)."),
  card("What hard problem underlies ML-KEM?", "Module Learning With Errors (Module-LWE) over R_q with q=3329, n=256, rank k=2/3/4. Security reduces to worst-case lattice problems via Regev-style reductions."),
  card("What does the Fujisaki–Okamoto transform add?", "It upgrades the IND-CPA K-PKE core to IND-CCA2 security: decapsulation re-encrypts and compares — invalid ciphertexts are implicitly rejected (a pseudorandom key is returned instead of failing loudly, defeating chosen-ciphertext oracles)."),
  card("What is 'implicit rejection' and why does it matter?", "On invalid ciphertext, Decaps returns a deterministic pseudorandom value derived from a secret seed instead of an error. Attackers learn nothing from submitting malformed ciphertexts — no decryption-failure oracle."),
  card("Why must ML-KEM keypairs be generated with fresh randomness — and what breaks if not?", "The FO transform's CCA proof assumes honest keygen; weak RNG produces guessable secrets. Worse: some KEM misuse patterns (reusing ephemeral randomness across encapsulations) leak the secret. Use the OS CSPRNG, never a userspace PRNG."),
  card("ML-KEM-512 vs 1024: when is 512 acceptable?", "Level 1 (≈AES-128 quantum ~64-bit... careful: level 1 means comparable to AES-128 CLASSICAL attack cost). Use 512 only where constraints demand it and policy allows; 768 is the default; 1024 where CNSA 2.0 / long-lived secrecy demands level 5."),
  card("What is the decapsulation failure probability, and why is it a security parameter?", "ML-KEM's failure rate is ~2^-139 to 2^-164 depending on set — negligible by design. Non-negligible failure rates enable failure-boosting attacks; the FIPS sets keep failures cryptographically irrelevant."),
  card("Why can't you just drop ML-KEM into RSA's slot in a protocol?", "Sizes differ by 10-50x (RSA-2048 pk: 256 B vs ML-KEM-768 pk: 1184 B), KEM ≠ key transport semantics, and hybrid negotiation needs protocol changes. Integration is a protocol-engineering task (see M07/M09).")
 ],
 "quiz": [
  quiz("ML-KEM-768: public key and ciphertext sizes?",
       ["800 B / 768 B", "1184 B / 1088 B", "1568 B / 1568 B", "256 B / 256 B"],
       1, "768 set: pk 1184 bytes, ciphertext 1088 bytes. (512: 800/768; 1024: 1568/1568.) These exact numbers are the FIPS-fixed integration constants."),
  quiz("The Fujisaki–Okamoto transform in ML-KEM provides:",
       ["Faster key generation", "IND-CCA2 security from an IND-CPA core, via re-encryption check and implicit rejection of invalid ciphertexts", "Smaller public keys", "Quantum key distribution"],
       1, "FO is the CCA upgrade: decaps re-encrypts the recovered message and compares ciphertexts; mismatches yield a pseudorandom key, not an error — killing chosen-ciphertext oracles."),
  quiz("Implicit rejection means a decapsulation of a malformed ciphertext:",
       ["Returns an error code the caller must handle", "Returns a pseudorandom shared secret derived from a secret seed — indistinguishable from a valid decapsulation to the attacker", "Panics", "Retries with a different secret key"],
       1, "No error oracle: the attacker cannot tell valid from invalid decapsulations by observing outputs. Error-returning decaps would enable adaptive attacks."),
  quiz("An engineer proposes ML-KEM-512 for a root CA with 20-year lifetime because 'keys are smaller.' Your response?",
       ["Approve — size is what matters", "Reject: level-1 security with a 20-year horizon violates the Mosca calculation; a root CA wants ML-KEM-1024 (level 5) or at minimum 768 — key size is not the deciding metric, secrecy lifetime is", "Approve with hybrid mode", "Use RSA-4096 instead"],
       1, "Root CAs are the longest-lived keys in the system. Level 1 for 20-year trust is a category error; the size saving (~384 B) is meaningless against the risk."),
  quiz("Which is a genuine ML-KEM misuse risk?",
       ["Using ML-KEM-768 as the default", "Feeding decapsulation output directly as an AES key without a KDF", "Generating keys with the OS CSPRNG", "Using implicit rejection"],
       1, "KEM shared secrets must go through a KDF (HKDF/SHAKE) before use as symmetric keys — raw shared secrets lack uniform distribution guarantees and domain separation. The other options are all correct practice.")
 ],
 "drills": [
  drill("il30-m03-drill1", [
   ("KEM triple: name the three algorithms and their inputs/outputs.", "KeyGen() → (pk, sk); Encaps(pk) → (ct, K); Decaps(sk, ct) → K.", "Generate, encapsulate, decapsulate."),
   ("ML-KEM-768 sizes: pk? ct?", "pk 1184 B, ct 1088 B.", "FIPS-fixed constants."),
   ("Hard problem + ring?", "Module-LWE over R_q, q=3329, n=256, k=2/3/4.", "Module rank scales the set.")
  ]),
  drill("il30-m03-drill2", [
   ("What does FO transform buy?", "IND-CCA2 from IND-CPA via re-encrypt-and-compare.", "The CCA upgrade."),
   ("Implicit rejection: what does the attacker observe on bad ct?", "A pseudorandom key — no error signal.", "No oracle."),
   ("Failure probability magnitude?", "~2^-139 or better — cryptographically negligible by design.", "Failures must be irrelevant.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m03-lab",
  "You will implement a toy KEM inspired by ML-KEM's structure (NOT real ML-KEM): a tiny Module-LWE K-PKE over Z_17 with k=2, then wrap it with a simplified FO-style re-encryption check, and demonstrate (1) correct encaps/decaps round-trip, (2) implicit rejection on tampered ciphertext, (3) what breaks when you skip the re-encryption check (a malleability demo).",
  [
   "Implement toy KeyGen/Encaps/Decaps over Z_17[x]/(x^4+1), k=2, binomial noise {-1,0,1} (reuse M00 ring code).",
   "Add the FO-style wrapper: encaps derives (K, randomness) via a hash of (message, pk); decaps re-encrypts and compares.",
   "Tamper with one ciphertext byte; show decaps returns a pseudorandom key, not an error and not the real K.",
   "Remove the re-encryption check; craft a malleability attack that distinguishes decaps outputs — write up why the check is load-bearing."
  ],
  "toy_kem.py plus a writeup: round-trip proof, tamper demo output, and the malleability writeup with the check removed.",
  "Round-trip recovers K; tampered ct yields unrelated pseudorandom K; without the check, the malleability attack visibly succeeds."
 ),
 "mockTask": mock(
  "During a TLS 1.3 integration review you see: server's ML-KEM keypair is generated once at install and reused for all handshakes; decapsulation errors are logged with full ciphertexts. Two findings?",
  ["No findings — this is standard", "(1) Long-term KEM key reuse across handshakes needs explicit analysis — ML-KEM is designed for this in some modes but the deployment must follow the FIPS/usage guidance on key lifetimes; (2) logging full failing ciphertexts builds a decryption-failure oracle dataset — strip ciphertext material from logs", "(1) fine (2) fine", "Only finding: use bigger keys"],
  1,
  "KEM key lifecycle is a policy decision with real constraints, and failure oracles are the classic CCA attack surface — implicit rejection exists precisely to deny attackers this signal; logging it re-opens the door."),
 "videos": [
  video("FIPS 203 (ML-KEM) — the standard text", FIPS203, "NIST CSRC", "Parameter sets, algorithms, and KATs from the source. Read the Encaps/Decaps pseudocode here.", 45, 1),
  video("CRYSTALS-Kyber — the submission behind ML-KEM", KYBER, "pq-crystals.org", "The Kyber team's site: specs, software, and the design rationale NIST standardized.", 20, 2)
 ],
 "pdfs": [
  pdf("NIST FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard", FIPS203, "NIST CSRC", "The final standard. Retrieved 2026-10-09."),
  pdf("Open Quantum Safe — liboqs and oqs-provider", OQSPROV, "Open Quantum Safe", "Production-path PQC: liboqs plus the OpenSSL 3 provider for real integrations. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("The protocol, precisely", "KeyGen: sample secret s and error e, compute t = A·s + e (A public or derived from a seed); pk = (seed_A, t), sk = s. Encaps(pk): sample message m and randomness; encrypt m under pk with fresh noise → ciphertext c; derive shared secret K = KDF(m, c) (simplified — the FIPS uses SHAKE-based derivation with domain separation). Decaps(sk, c): decrypt to m'; re-encrypt m' with the same randomness derivation; if the re-encryption equals c, return K = KDF(m', c), else return K' = PRF(secret_seed, c) — implicit rejection. The re-encryption check is the FO transform: it binds the ciphertext to honestly-generated randomness, which is what upgrades CPA to CCA security."),
  note("Parameter sets and what they cost", "ML-KEM-512: k=2, pk 800 B, ct 768 B, sk 1632 B, level 1. ML-KEM-768: k=3, pk 1184 B, ct 1088 B, sk 2400 B, level 3 — the default. ML-KEM-1024: k=4, pk 1568 B, ct 1568 B, sk 3168 B, level 5. Compare RSA-2048: pk 256 B. The 4-6x size growth is the central integration fact: TLS ClientHello/KeyShare, X.509 certificates, and DNS/DANE all have size budgets that ML-KEM strains. Every migration playbook (M09/M10) is downstream of these four numbers. Performance, by contrast, is a non-issue: ML-KEM keygen/encaps/decaps run in microseconds-to-milliseconds — faster than RSA-2048 private ops on most platforms."),
  note("Misuse cases that void the warranty", "(1) Randomness: keygen and encaps randomness must come from a CSPRNG; the FO security proof assumes it. (2) Key lifetimes: follow usage guidance — KEM keys are not immortal; rotation policy belongs in your migration plan. (3) Side channels: lattice ops are timing-attack targets (KyberSlash, 2023, showed non-constant-time reference decapsulation leaking secrets); deploy constant-time implementations and validate. (4) No raw K: always KDF the shared secret with context binding before use. (5) Don't 'optimize' the FO check away — the malleability lab (above) shows what happens. The math is proven; the implementation is where systems die.")
 ]
}

# =====================================================================
# M04 — ML-DSA (Dilithium)
# =====================================================================
M04 = {
 "id": "IL30-M04", "code": "IL-30",
 "title": "ML-DSA (Dilithium): Module-Lattice Signatures in Depth",
 "summary": "FIPS 204 end to end: Fiat–Shamir with aborts, the signing loop and rejection sampling, parameter sets ML-DSA-44/65/87 with exact signature sizes, verification, deterministic vs hedged signing, and why ML-DSA is the default signature for the migration.",
 "objectives": [
  "Explain Fiat–Shamir with aborts: commit, challenge, respond, reject-and-retry",
  "State exact signature sizes: 2420/3309/4627 B for 44/65/87 and public keys 1312/1952/2592 B",
  "Map parameter sets to NIST levels 2/3/5 and choose the right default (65)",
  "Describe deterministic signing and when hedged randomness matters",
  "Verify a signature by hand-tracing the verification equation"
 ],
 "estimatedMinutes": 660, "weight": 1.0,
 "prerequisiteFor": ["IL30-M05","IL30-M10","IL30-M12"],
 "crossLinks": [
  {"course": "IL-11", "module": "il11-network-crypto-foundations--zt-hashing", "note": "hash functions inside the Fiat–Shamir transform"},
  {"course": "IL-29", "module": "IL29-M33", "note": "Security+ crypto domain — signature concepts"}
 ],
 "cards": [
  card("What is the Fiat–Shamir transform (one line)?", "Turns an interactive identification protocol (commit → challenge → respond) into a non-interactive signature by deriving the challenge as a hash of the commitment and message."),
  card("Why 'with aborts' in Dilithium?", "The response z = y + c·s1 must hide the secret s1: if z leaks information (coefficients too large), the signer aborts and retries with fresh y. Rejection sampling keeps the signature distribution independent of the secret."),
  card("ML-DSA parameter sets → levels → sizes?", "ML-DSA-44: level 2, pk 1312 B, sig 2420 B. ML-DSA-65: level 3, pk 1952 B, sig 3309 B (default). ML-DSA-87: level 5, pk 2592 B, sig 4627 B."),
  card("What hard problems underlie ML-DSA?", "Module-LWE plus the SelfTargetMSIS problem (a variant of Module-SIS): forging requires finding short vectors satisfying a hash-targeted equation. Both are lattice problems with worst-case connections."),
  card("Deterministic vs randomized (hedged) signing?", "FIPS 204 specifies deterministic signing: randomness derived from (sk seed, message) — no RNG needed at sign time, no catastrophic failure if the RNG is weak. Hedged/randomized variants add fresh randomness for side-channel robustness; both verify identically."),
  card("What does verification check, conceptually?", "Recompute the challenge hash from the signature's commitment hint and the message, then check the response equation A·z − c·t ≈ w with tight coefficient bounds — and that no bound was violated (the verifier enforces the aborts the signer promised)."),
  card("Why is ML-DSA the default migration signature?", "Fast (sign/verify in microseconds), moderate sizes, strong reviewed security, FIPS-final since Aug 2024. SLH-DSA is the conservative backup; FN-DSA the compact future — ML-DSA is the workhorse."),
  card("Context strings / domain separation in ML-DSA?", "FIPS 204 signs (message, context): the optional context string domain-separates signature uses (e.g., 'firmware-v2' vs 'tls-cert'). Always set it — cross-protocol signature confusion is a real attack class."),
  card("The #1 implementation pitfall in lattice signatures?", "Side channels in signing: the abort loop's timing and the secret-dependent sampling must be constant-time. Rejection sampling is the classic leak point — use validated implementations."),
  card("ML-DSA vs ECDSA size comparison?", "ECDSA P-256: 64-byte signatures, 32-byte keys. ML-DSA-65: 3309-byte signatures, 1952-byte public keys — ~50x growth. Certificate chains and code-signing blobs must be re-budgeted (M10).")
 ],
 "quiz": [
  quiz("In Fiat–Shamir with aborts, the signer retries when:",
       ["The message is too long", "The candidate response z would leak secret information (coefficients out of bounds) — rejection sampling restarts with fresh masking randomness", "The verifier is offline", "The hash function is slow"],
       1, "Aborts are the security mechanism: z must be distributed independently of the secret. Out-of-bounds z → discard, retry. Expected retries are small (~4-7) and constant-time implementations must not leak the retry count."),
  quiz("ML-DSA-65 signature and public key sizes?",
       ["2420 B / 1312 B", "3309 B / 1952 B", "4627 B / 2592 B", "64 B / 32 B"],
       1, "65 set: sig 3309 bytes, pk 1952 bytes. (44: 2420/1312; 87: 4627/2592.)"),
  quiz("FIPS 204 deterministic signing means:",
       ["The same message always produces the same signature — randomness is derived deterministically from the secret seed and message, so signing needs no RNG", "Signatures are deterministic across different keys", "Verification is deterministic (it always is)", "The scheme has no randomness anywhere"],
       0, "Deterministic nonces kill the catastrophic RNG-failure class that broke ECDSA/DSA (Sony PS3, Android). Keygen still needs a CSPRNG; signing does not."),
  quiz("A verifier must check, in addition to the equation:",
       ["The signer's identity document", "That all signature coefficients satisfy the FIPS bounds — the verifier enforces the abort conditions the signer claims", "The timestamp", "The certificate chain (always)"],
       1, "Bounds checking is part of verification: a signature that violates the coefficient bounds is invalid, period. Skipping bound checks has broken real implementations."),
  quiz("Why specify a context string when signing firmware with ML-DSA?",
       ["It compresses the signature", "Domain separation: a signature valid for context 'firmware-v2' cannot be transplanted into context 'tls-cert' — defeats cross-protocol confusion attacks", "It is required for the math to work", "It replaces the public key"],
       1, "Same key, different jobs: without domain separation, a signature from one protocol can be replayed as valid in another. Context strings are cheap insurance.")
 ],
 "drills": [
  drill("il30-m04-drill1", [
   ("Fiat–Shamir in 4 words?", "Commit, challenge (hash), respond.", "Interactive → non-interactive via hash."),
   ("Why abort?", "Keep z independent of the secret — reject leaky responses.", "Rejection sampling protects s1."),
   ("ML-DSA-65 sizes?", "pk 1952 B, sig 3309 B.", "The default set.")
  ]),
  drill("il30-m04-drill2", [
   ("Deterministic signing: what does it remove?", "Sign-time RNG dependence — nonces derive from (seed, message).", "No RNG at sign time."),
   ("Verifier's extra job beyond the equation?", "Enforce coefficient bounds.", "Bounds are part of validity."),
   ("Hard problems?", "Module-LWE + SelfTargetMSIS (Module-SIS variant).", "Two lattice legs.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m04-lab",
  "You will implement a toy Fiat–Shamir-with-aborts signature over a tiny ring (NOT real Dilithium): commit/challenge/response with rejection sampling, then verify. You will measure abort rates, demonstrate a leaky variant (no aborts) whose responses reveal the secret statistically, and verify signatures with bound checks.",
  [
   "Implement toy keygen/sign/verify over Z_17[x]/(x^4+1) with challenge = hash(commitment || message) mod small range.",
   "Implement rejection sampling: resample masking vector when response coefficients exceed bound B; measure average retries.",
   "Build the leaky variant (no aborts); collect 500 signatures and show the secret's statistical recovery — write up the leak.",
   "Implement verification WITH bound checks; feed it an out-of-bounds forgery and confirm rejection."
  ],
  "toy_dsa.py plus writeup: abort-rate measurement, the leak demo results, and the bound-check rejection proof.",
  "Valid signatures verify; leaky variant demonstrably leaks the secret; out-of-bounds forgeries are rejected by bound checks."
 ),
 "mockTask": mock(
  "Code review: a team's ML-DSA integration skips coefficient bound checks in verification 'for speed' and reuses one context string ('app') for firmware, TLS certs, and tokens. Findings?",
  ["No issues — verification is just the equation", "Two critical findings: (1) bound checks are part of FIPS validity — skipping them accepts malformed signatures and has broken real implementations; (2) one context for three protocols invites cross-protocol replay — separate contexts per use", "Only the context issue matters", "Only the bounds issue matters"],
  1,
  "Both are spec-level requirements, not style: bounds are validity, contexts are domain separation. 'For speed' is never an acceptable reason to drop validity checks."),
 "videos": [
  video("FIPS 204 (ML-DSA) — the standard text", FIPS204, "NIST CSRC", "Parameter sets, signing/verification pseudocode, KATs. Trace the abort loop here.", 45, 1),
  video("CRYSTALS-Dilithium — the submission behind ML-DSA", DILITHIUM, "pq-crystals.org", "Design rationale, security estimates, and reference software from the Dilithium team.", 20, 2)
 ],
 "pdfs": [
  pdf("NIST FIPS 204 — Module-Lattice-Based Digital Signature Standard", FIPS204, "NIST CSRC", "The final standard. Retrieved 2026-10-09."),
  pdf("FIPS 206 (FN-DSA) fixed-point draft change — why specs move", FIPS206, "freenode", "Live example of a standard in motion: fixed-point arithmetic mandated for Falcon's FIPS. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("Fiat–Shamir with aborts, step by step", "Key: A random matrix, secret (s1, s2) small, public t = A·s1 + s2. Sign(m): sample masking y (large-ish); w = A·y; challenge c = H(w_highbits || m) (small, sparse); z = y + c·s1; ABORT CHECK: if z's coefficients are too large (would leak s1) or the hint would be wrong, restart with fresh y. Output (z, hint, c-derived w1). Verify: recompute w1' from (A, z, hint, t), check c == H(w1' || m) and all bounds. The abort loop runs ~4-7 iterations on average; the security proof shows the accepted z distribution is independent of the secret — that independence is the entire game, and it is why the timing of the loop must not leak."),
  note("Sizes, levels, and the default", "ML-DSA-44: level 2, pk 1312 B, sig 2420 B — constrained use. ML-DSA-65: level 3, pk 1952 B, sig 3309 B — the default; matches CNSA 2.0-era expectations for general use. ML-DSA-87: level 5, pk 2592 B, sig 4627 B — long-lived/high-value keys. The naming: first digit ≈ matrix rows k, second ≈ columns l (44: k=4,l=4; 65: k=6,l=5; 87: k=8,l=7). Bigger matrices = harder lattice = bigger everything. Performance is excellent across all three (tens of microseconds); size is the dimension you plan around — X.509 chains carrying 3 KB signatures need new path-length and MTU thinking (M09/M10)."),
  note("Deterministic signing and hedged variants", "FIPS 204 signs deterministically: the per-message randomness derives from a secret seed and the message (via SHAKE). Consequence: no RNG at sign time, and the entire 'broken/duplicate nonce' catastrophe class (Sony PS3 ECDSA, 2010) cannot occur. The tradeoff cryptographers debate: deterministic signing is fragile against fault-injection and some side channels (same input → same execution trace), which is why hedged variants mix fresh randomness in. Both verify identically — the verifier never knows which you used. Engineering rule: use validated implementations, keep firmware patched, and treat signing devices as side-channel-sensitive hardware regardless of mode.")
 ]
}

# =====================================================================
# M05 — SLH-DSA (SPHINCS+)
# =====================================================================
M05 = {
 "id": "IL30-M05", "code": "IL-30",
 "title": "SLH-DSA (SPHINCS+): Stateless Hash-Based Signatures",
 "summary": "FIPS 205 end to end: why hash-based signatures are the conservative choice, the hypertree + FORS construction, all 12 parameter sets (SHA2/SHAKE × 128/192/256 × small/fast), size/performance tradeoffs, and when to choose SLH-DSA over ML-DSA.",
 "objectives": [
  "Explain why hash-based signatures need no number-theoretic assumptions",
  "Describe the hypertree + XMSS + WOTS+ + FORS construction at block level",
  "Navigate the 12 parameter sets and pick small vs fast correctly",
  "State the size/performance costs: 7.8–49 KB signatures, slow signing",
  "Decide SLH-DSA vs ML-DSA for firmware, root CA, and general use"
 ],
 "estimatedMinutes": 600, "weight": 0.9,
 "prerequisiteFor": ["IL30-M10","IL30-M14"],
 "crossLinks": [
  {"course": "IL-11", "module": "il11-network-crypto-foundations--zt-hashing", "note": "hash primitives the whole scheme rests on"},
  {"course": "IL-29", "module": "IL29-M33", "note": "Security+ crypto domain context"}
 ],
 "cards": [
  card("What assumption does SLH-DSA's security rest on?", "Only the security of the underlying hash function (second-preimage/collision resistance, PRF properties) — no lattices, no number theory. If SHA-256/SHAKE hold, SLH-DSA holds."),
  card("One-time signatures → many-time: how?", "WOTS+ signs once per keypair (each private element usable once). XMSS builds a Merkle tree over many WOTS+ keys: the root is the public key, the authentication path proves membership. The hypertree stacks XMSS trees: a signature signs with a WOTS+ leaf and includes d authentication paths."),
  card("What is FORS and what does it sign?", "FORS (Forest of Random Subsets): a few-time signature at the hypertree's leaves that signs the message digest. 'Few-time' = secure as long as the same FORS key signs only a handful of messages — the hypertree guarantees fresh FORS keys per signature."),
  card("Why 'stateless' matters (vs XMSS/LMS in SP 800-208)?", "Stateful schemes (XMSS, LMS) MUST NEVER reuse a one-time key — a state-rollback (VM clone, backup restore) breaks them catastrophically. SLH-DSA derives one-time keys pseudorandomly per signature: no state to manage, no catastrophic reuse."),
  card("The 12 parameter sets: what are the three axes?", "Hash function (SHA2 vs SHAKE), security level (128/192/256-bit, matching NIST levels 1/3/5), and size/speed tradeoff (s = small signatures, f = fast signing). 2 × 3 × 2 = 12."),
  card("SLH-DSA sizes: public key? signatures?", "Public keys tiny: 32/48/64 B. Signatures large: ~7.8 KB (128s) to ~49 KB (256f). Private keys 64/96/128 B. The asymmetry (tiny pk, huge sig) shapes every use case."),
  card("Signing performance: the honest numbers?", "SLH-DSA signing is SLOW: milliseconds to tens of milliseconds (128f) up to seconds-scale for the 's' variants on constrained hardware — vs microseconds for ML-DSA. Verification is fast (sub-millisecond). Sign rarely, verify often."),
  card("When do you choose SLH-DSA over ML-DSA?", "Long-lived roots and firmware signing where (1) assumption diversity matters, (2) signing is infrequent, (3) tiny public keys help (embedded verifiers), and (4) you can tolerate KB-scale signatures. General-purpose: ML-DSA."),
  card("Small ('s') vs fast ('f'): the rule?", "'f': bigger signatures, much faster signing — online signers. 's': smaller signatures, slower signing — bandwidth-constrained distribution (firmware images signed rarely, verified by millions)."),
  card("Does Grover threaten SLH-DSA's hash assumption?", "Only in the generic way: use the 192/256-bit parameter sets for long-lived use (matching CNSA 2.0's SHA-384/512 posture). The 128-bit sets remain fine for short-lived signatures — same logic as AES-128 vs 256.")
 ],
 "quiz": [
  quiz("The catastrophic failure mode of STATEFUL hash-based signatures (XMSS/LMS) is:",
       ["Slow signing", "One-time key reuse after state rollback (VM clone, backup restore) — a reused WOTS+ key leaks enough to forge", "Large public keys", "Quantum attack on Merkle trees"],
       1, "State management is the entire risk: sign twice with one WOTS+ key and the scheme breaks. SLH-DSA's stateless design exists precisely to delete this failure class."),
  quiz("SLH-DSA-128s: public key and signature size, roughly?",
       ["32 B pk, ~7.8 KB sig", "1952 B pk, 3309 B sig", "64 B pk, 64 B sig", "800 B pk, 768 B sig"],
       0, "Tiny public key (32 B), ~7.8 KB signature. Contrast ML-DSA-65: 1952 B pk / 3309 B sig — SLH-DSA wins on pk size, loses on signature size."),
  quiz("FORS sits where in the construction, and signs what?",
       ["At the root; signs the public key", "At the hypertree leaves; signs the message digest with a few-time signature", "In the middle; signs the WOTS+ keys", "It replaces the Merkle tree"],
       1, "Message → FORS (few-time) → WOTS+ leaf → XMSS tree → hypertree layers → root pk. Each layer authenticates the one below."),
  quiz("You need signatures for a firmware update system: images signed quarterly, verified by 10M constrained devices, keys must last 15 years. Best fit?",
       ["ML-DSA-44", "SLH-DSA-128s or 192s: infrequent signing tolerates slow sign times, 's' minimizes per-image signature overhead, hash-only assumptions suit 15-year trust, tiny pks help constrained verifiers", "RSA-2048", "Ed25519"],
       1, "This is SLH-DSA's home turf: sign rarely (quarterly), verify everywhere, long-lived trust, conservative assumptions. The 's' variant optimizes the distributed artifact."),
  quiz("Why does FIPS 205 exist alongside FIPS 204 (both signatures)?",
       ["Redundancy for marketing", "Assumption diversity: if lattice problems ever weaken, a hash-based standard survives — NIST explicitly wanted a non-lattice backup", "SLH-DSA is faster", "FIPS 204 was found broken"],
       1, "Portfolio theory at the standards level. ML-DSA is the workhorse; SLH-DSA is the insurance policy whose security reduces to hash functions alone.")
 ],
 "drills": [
  drill("il30-m05-drill1", [
   ("Security assumption of SLH-DSA?", "Hash-function security only — no lattices, no number theory.", "Hashes all the way down."),
   ("WOTS+ → XMSS → hypertree: what does each layer add?", "WOTS+: one-time signing. XMSS: Merkle tree over many WOTS+ keys (many-time, stateful). Hypertree: layers of XMSS for scale.", "One-time → tree → tree-of-trees."),
   ("FORS role?", "Few-time signature at the leaves signing the message digest.", "Leaf-level message signing.")
  ]),
  drill("il30-m05-drill2", [
   ("12 parameter sets: name the 3 axes.", "Hash (SHA2/SHAKE) × level (128/192/256) × tradeoff (small/fast).", "2×3×2=12."),
   ("'s' vs 'f': when each?", "'f': fast signing, bigger sigs (online). 's': small sigs, slow signing (firmware distribution).", "Signing frequency decides."),
   ("Stateless advantage in one line?", "No one-time-key state to roll back — VM clones can't cause catastrophic reuse.", "Deletes the state risk.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m05-lab",
  "You will implement a miniature hash-based signature (Lamport one-time + 2-level Merkle tree, NOT real SPHINCS+) in Python: keygen over 8 messages, signing with authentication paths, verification, and a demo of the stateful-reuse catastrophe (sign two messages with one Lamport key, then forge). Then you will benchmark real SLH-DSA via liboqs if available and record sign/verify timings.",
  [
   "Implement Lamport OTS (256 keypairs of 256-bit secrets) and a height-3 Merkle tree; sign 8 distinct messages with correct auth paths.",
   "Implement verification; confirm all 8 verify and a tampered message fails.",
   "Reuse one Lamport key for two messages; demonstrate the forgery this enables — write up why state matters.",
   "If liboqs is installed, time SLH-DSA-128s vs 128f sign/verify; otherwise document expected orders of magnitude from the FIPS."
  ],
  "toy_hashsig.py, the reuse-forgery writeup, and timing notes for real SLH-DSA parameter sets.",
  "All 8 toy signatures verify; the reuse forgery is demonstrated and explained; SLH-DSA timings (or documented estimates) distinguish s vs f."
 ),
 "mockTask": mock(
  "A team proposes SLH-DSA-256f for high-frequency API token signing (10k signatures/second). Assessment?",
  ["Good — strongest parameters", "Wrong tool: SLH-DSA signing throughput is orders of magnitude below 10k/s and signatures are KB-scale — ML-DSA-65 is the correct high-frequency choice; reserve SLH-DSA for infrequent, long-lived signing", "Good with hardware acceleration", "Use 128s instead"],
  1,
  "Parameter strength ≠ fitness. SLH-DSA's costs (slow signing, huge signatures) make it wrong for high-frequency use no matter the security level — this is the M05 decision framework applied."),
 "videos": [
  video("FIPS 205 (SLH-DSA) — the standard text", FIPS205, "NIST CSRC", "The 12 parameter sets, signing/verification, and the hypertree spec from the source.", 45, 1),
  video("SPHINCS+ — the submission behind SLH-DSA", SPHINCS, "sphincs.org", "Design, parameters, and software from the SPHINCS+ team.", 20, 2)
 ],
 "pdfs": [
  pdf("NIST FIPS 205 — Stateless Hash-Based Digital Signature Standard", FIPS205, "NIST CSRC", "The final standard. Retrieved 2026-10-09."),
  pdf("NIST SP 800-208 — stateful hash-based signatures (XMSS/LMS)", AWESOME, "awesome-post-quantum (NIST link)", "The stateful counterpart: when XMSS/LMS fit and their state-management rules. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("The construction, block by block", "Bottom: FORS signs the message digest — a few-time signature secure because each FORS key is used (essentially) once. FORS public key → signed by a WOTS+ one-time key at a hypertree leaf. WOTS+ keys are aggregated by XMSS Merkle trees; XMSS roots are signed by the WOTS+ keys of the XMSS layer above; d layers up, the top root is the SLH-DSA public key (32-64 bytes). A signature = FORS signature + d × (WOTS+ signature + XMSS auth path). Verification walks the chain upward recomputing hashes. Total hash calls per signature: tens of thousands — that is the entire performance story, and why 'f' variants use taller/faster tree shapes."),
  note("The 12 sets, decoded", "Naming: SLH-DSA-{SHA2|SHAKE}-{128s|128f|192s|192f|256s|256f}. 128/192/256 = security bits (NIST levels 1/3/5). s/f = small/fast. SHA2 vs SHAKE: SHAKE variants are faster in software and the conservative choice where SHA-3 is acceptable; SHA2 variants exist for FIPS-140-style SHA-2-only environments. Sizes: pk 32/48/64 B; sig from 7,856 B (128s) to 49,216 B (256f). Signing: 128f ≈ ms-scale, 128s ≈ 10-100ms, 256s can exceed a second on slow CPUs. Rule of thumb: online signers → f; distributed artifacts signed rarely → s; 15-year trust → 192/256."),
  note("SLH-DSA vs ML-DSA: the decision table", "Choose ML-DSA when: high signature volume, latency-sensitive signing, moderate sizes acceptable, general-purpose (TLS certs, tokens, most code signing). Choose SLH-DSA when: signing is rare (firmware, roots), verifiers are constrained (tiny pk), trust must span decades, or policy demands non-lattice assumptions. Choose FN-DSA (when final) when: signature size is the binding constraint (embedded, some firmware). The three standards are a portfolio, not a ranking — M14's capstone makes you allocate them across a real architecture.")
 ]
}

# =====================================================================
# M06 — FN-DSA, HQC, pipeline
# =====================================================================
M06 = {
 "id": "IL30-M06", "code": "IL-30",
 "title": "FN-DSA (Falcon), HQC & the Standards Pipeline",
 "summary": "The algorithms still in the pipeline: FN-DSA (Falcon) heading for FIPS 206 with its fixed-point rewrite, HQC selected as the backup KEM, the additional-signatures round-2 candidates, and how to track — not build on — moving standards.",
 "objectives": [
  "Explain Falcon's NTRU-lattice design and why its signatures are the smallest",
  "State FIPS 206's status, timeline, and the fixed-point arithmetic change",
  "Explain HQC's code-based design and its backup-KEM role",
  "Track the additional-signatures round without deploying candidates",
  "Apply the 'track, don't build' rule to draft-status algorithms"
 ],
 "estimatedMinutes": 540, "weight": 0.8,
 "prerequisiteFor": ["IL30-M13","IL30-M14"],
 "crossLinks": [
  {"course": "IL-29", "module": "IL29-M33", "note": "Security+ crypto domain context"},
  {"course": "IL-23", "module": "m23-quantum", "note": "quantum basics"}
 ],
 "cards": [
  card("What mathematical problem underlies Falcon/FN-DSA?", "NTRU lattices: short vectors in NTRU-style lattices, with signatures produced by Gaussian sampling over the lattice (GPV framework) using an NTRU trapdoor."),
  card("Why are Falcon signatures so small?", "Falcon-512: ~666-byte signatures, 897-byte public keys; Falcon-1024: ~1280-byte sigs. The Gaussian sampler produces compact signatures — the smallest of any NIST-selected scheme — at the cost of implementation complexity."),
  card("What is FIPS 206's status and expected timeline?", "Initial Public Draft submitted August 2025; public review ~1 year; final expected late 2026/early 2027. Track the IPD — do not ship against it."),
  card("What changed between Falcon-as-submitted and FN-DSA?", "NIST is mandating fixed-point arithmetic (32.32 for keygen, 64.64 for signing) and a single KAT-matchable signing procedure — floating-point will NOT be allowed in the FIPS. Implementations must match Known Answer Tests exactly."),
  card("Why did floating-point become a problem?", "Falcon's Gaussian sampler historically used floating point; tiny platform-to-platform FP differences break determinism and KAT-matching, and FP pipelines are side-channel-sensitive. Fixed-point makes behavior exact and testable."),
  card("What is HQC and why was it selected?", "Hamming Quasi-Cyclic: a code-based KEM (security from quasi-cyclic codes / syndrome decoding). Selected March 2025 as the backup KEM — a non-lattice alternative if Module-LWE ever weakens. Draft standard in progress."),
  card("HQC's practical profile vs ML-KEM?", "Larger public keys/ciphertexts than ML-KEM, slower — the price of code-based diversity. It's insurance, not a performance play."),
  card("What is the additional-signatures round tracking?", "NIST's second signature track (round-2 candidates under evaluation through 2026): code-, multivariate-, isogeny-, MPC-in-the-head-based schemes. The HAWK withdrawal (2026) shows live cryptanalysis doing its job."),
  card("The 'track, don't build' rule, stated?", "Draft/selected/candidate algorithms: follow their status, experiment in labs, never ship production crypto against them, never cite them as 'NIST-approved' without the status qualifier."),
  card("When WILL FN-DSA be the right choice?", "After FIPS 206 finalizes: firmware/embedded signing where signature size is the binding constraint and ML-DSA's 3.3 KB signatures don't fit.")
 ],
 "quiz": [
  quiz("The FIPS 206 draft's fixed-point mandate exists because:",
       ["Fixed-point is faster on all CPUs", "Floating-point non-determinism across platforms breaks KAT-matching and exact behavior; fixed-point makes signing precisely specified and testable", "NIST dislikes floating point generally", "It shrinks signatures"],
       1, "Conformance needs bit-exact behavior: FP rounding varies by platform/library, which breaks Known Answer Tests and complicates validation. Fixed-point (32.32/64.64) is exact."),
  quiz("A vendor ships 'FIPS 206 FN-DSA' in production citing the IPD. The problem?",
       ["None — IPDs are final", "The IPD is a draft under public comment; parameters, OIDs, and KATs can still change, and no FIPS validation path exists for drafts — production deployment is premature", "FN-DSA is hash-based", "IPDs are only for signatures"],
       1, "Draft ≠ standard. Ship against FIPS 203/204/205; experiment with the IPD in labs only."),
  quiz("HQC's role in the portfolio is:",
       ["Primary KEM replacing ML-KEM", "Backup KEM: code-based diversity in case lattice assumptions weaken — larger and slower than ML-KEM by design tradeoff", "A signature scheme", "Deprecated"],
       1, "Insurance, not replacement. NIST selected HQC precisely so the KEM portfolio doesn't rest on lattices alone."),
  quiz("Falcon's signature-size advantage comes with which cost?",
       ["Larger public keys than ML-DSA", "Complex Gaussian sampling over NTRU lattices — historically floating-point, side-channel-sensitive, hard to implement in constant time", "No security proof", "It is stateful"],
       1, "Compactness is bought with sampler complexity. The FIPS 206 fixed-point rewrite is NIST paying down exactly this implementation risk."),
  quiz("The HAWK withdrawal (2026) demonstrates:",
       ["PQC is failing", "The evaluation process working: weakness found during public review, candidate withdrawn before standardization — the same filter that killed SIKE", "Lattice crypto is broken", "NIST moving too slowly"],
       1, "Candidates are supposed to die in evaluation. A withdrawal with no deployed systems affected is the process succeeding — and a warning against building on unevaluated candidates.")
 ],
 "drills": [
  drill("il30-m06-drill1", [
   ("Falcon math base?", "NTRU lattices + GPV Gaussian sampling.", "NTRU trapdoor signatures."),
   ("FIPS 206 status + timeline?", "IPD submitted Aug 2025; final expected late 2026/early 2027.", "Draft, not final."),
   ("The fixed-point change, in one line?", "FIPS mandates exact fixed-point arithmetic; floating-point not allowed.", "Exactness for KATs.")
  ]),
  drill("il30-m06-drill2", [
   ("HQC: what is it, what role?", "Code-based (Hamming Quasi-Cyclic) KEM; backup KEM for assumption diversity.", "Non-lattice insurance."),
   ("HQC vs ML-KEM practically?", "Bigger keys/ciphertexts, slower — diversity costs performance.", "Insurance costs speed."),
   ("Additional-signatures round: deployable?", "No — candidates under evaluation; track only.", "Never ship candidates.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m06-lab",
  "You will extend your standards tracker from M02 into a pipeline watch brief: for FN-DSA, HQC, and three additional-signature round-2 candidates, record the latest primary-source status, the open technical questions (e.g., FIPS 206 fixed-point details), and a 'what would change our build decision' trigger list. You will also draft the one-paragraph policy your org will use for draft-standard algorithms.",
  [
   "For FN-DSA: record IPD status, the fixed-point mandate specifics, and what 'final' would unlock for your architecture.",
   "For HQC: record selection status, draft progress, and the backup-KEM deployment conditions you'd require.",
   "Pick three additional-signature candidates; record their basis (code/multivariate/isogeny/MPC) and status — one paragraph each.",
   "Write the org policy paragraph: under what conditions may a draft/candidate algorithm touch production? (Answer: essentially never, with named exceptions.)",
   "Define trigger events that would change a verdict (e.g., 'FIPS 206 final published' → re-evaluate firmware signing)."
  ],
  "pipeline-watch.md: per-algorithm status with primary sources, the draft-algorithm policy paragraph, and the trigger list.",
  "Every status cites a primary source with date; the policy paragraph is unambiguous; triggers are concrete events, not vibes."
 ),
 "mockTask": mock(
  "Your firmware team wants Falcon signatures NOW (they fit the bootloader budget; ML-DSA doesn't) and proposes shipping the IPD implementation. Decide.",
  ["Approve — size wins", "Deny production use: FIPS 206 is draft; the fixed-point spec is still settling and no validation path exists. Approve a lab pilot against the IPD plus a re-evaluation trigger at 'FIPS 206 final', and have them prototype ML-DSA/SLH-DSA size mitigations (signature segmentation, external sig stores) in parallel", "Approve with ML-DSA fallback", "Tell them to use RSA"],
  1,
  "The constraint is real but draft crypto in a bootloader is how you get unpatchable mistakes. Pilot now, decide at final — with parallel work on making the standardized options fit."),
 "videos": [
  video("FN-DSA nears draft approval — FIPS 206 timeline and industry posture", FNDSA, "DigiCert", "Draft submitted Aug 2025, ~1-year review, final expected late 2026/early 2027; why vendors wait for final.", 15, 1),
  video("NIST locks FN-DSA to fixed-point math for FIPS 206", FIPS206, "freenode", "The spec-in-motion story: single KAT-matchable signing procedure, 32.32/64.64 fixed-point, floating-point out.", 10, 2)
 ],
 "pdfs": [
  pdf("Falcon — the submission behind FN-DSA", FALCON, "falcon-sign.info", "Specs, rationale, and reference software from the Falcon team. Retrieved 2026-10-09."),
  pdf("PQC standards tracker — FN-DSA/HQC/additional-signature status", KFCIPHER, "KFCipher", "Live status board for the pipeline algorithms. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("Falcon's design and its price", "Falcon = GPV-framework signatures over NTRU lattices: keygen builds an NTRU lattice with a short trapdoor basis; signing uses the trapdoor to sample a lattice vector close to a hashed target (Gaussian sampling); verification checks shortness and the hash equation. The sampler is the crown jewel and the risk: it needs high-precision Gaussian sampling over the lattice, historically done in floating point — fast on desktops, treacherous for determinism and side channels. NIST's FIPS 206 answer: mandate fixed-point (32.32 keygen, 64.64 signing), specify ONE signing procedure that KATs can pin down, and allow future variants only via separate Special Publications with their own KATs. Result: Falcon-512 signatures ~666 B — roughly 5x smaller than ML-DSA-65 — for firmware and embedded use, once final."),
  note("HQC: the backup KEM", "HQC (Hamming Quasi-Cyclic) bases security on quasi-cyclic codes — syndrome decoding, a problem cryptanalyzed since McEliece (1978). As the selected backup KEM it gives the portfolio a non-lattice key-establishment option: if Module-LWE ever weakens, migration has somewhere to go. Costs are real: public keys and ciphertexts substantially larger than ML-KEM's, slower operations. NIST's selection (March 2025) is about the portfolio, not about beating Kyber on merit — and the draft standard is still being written, so the only correct production posture is 'track'."),
  note("How to watch a pipeline without betting on it", "Three disciplines: (1) Status literacy — candidate/selected/draft/final are different planets; your tracker (M02 lab) is the instrument. (2) Trigger-based decisions — pre-write the events that change a verdict ('FIPS 206 final' → evaluate Falcon for bootloader; 'HQC draft' → lab-test interop), so you're reacting to publications, not hype. (3) Lab-only contact — IPDs and candidates run in isolated experiments with no production data, no production keys, and a written sunset date. Standards move; your architecture shouldn't move with rumors.")
 ]
}

# =====================================================================
# M07 — Hybrid key exchange
# =====================================================================
M07 = {
 "id": "IL30-M07", "code": "IL-30",
 "title": "Hybrid Key Exchange: X25519 + ML-KEM in TLS 1.3",
 "summary": "The transition workhorse: why hybrids exist, the hybrid security property (safe if EITHER component holds), how X25519MLKEM768 works in TLS 1.3, combiner design, and where hybrids are (and aren't) appropriate.",
 "objectives": [
  "State the hybrid security property precisely and why it de-risks migration",
  "Describe the X25519MLKEM768 TLS 1.3 handshake: key shares, concatenation, KDF",
  "Explain combiner/KDF design: why simple concatenation needs a proper KDF",
  "Distinguish hybrid key exchange from hybrid signatures/certs",
  "Decide hybrid vs pure-PQC per deployment phase"
 ],
 "estimatedMinutes": 600, "weight": 1.0,
 "prerequisiteFor": ["IL30-M09","IL30-M12","IL30-M14"],
 "crossLinks": [
  {"course": "IL-11", "module": "il11-network-crypto-foundations--zt-encryption", "note": "TLS/classical key exchange context"},
  {"course": "IL-29", "module": "IL29-M33", "note": "Security+ crypto domain — key exchange concepts"}
 ],
 "cards": [
  card("What is a hybrid key exchange?", "A key exchange combining a classical algorithm (X25519) with a PQC KEM (ML-KEM-768): both run, both shared secrets feed a KDF, and the session key is safe if EITHER component is unbroken."),
  card("State the hybrid security property.", "The combined exchange is secure as long as at least one component is secure: classical breaks (quantum) → ML-KEM carries it; ML-KEM breaks (cryptanalysis) → X25519 carries it. Defense in depth across assumptions."),
  card("Why hybrids instead of jumping straight to pure PQC?", "Three reasons: (1) hedge against young-standard cryptanalysis — ML-KEM is new, X25519 is battle-tested; (2) FIPS/validation continuity during transition; (3) downgrade-safety while peers upgrade at different speeds."),
  card("How does X25519MLKEM768 work in TLS 1.3?", "Client offers the hybrid named group: KeyShare carries X25519 ephemeral public key CONCATENATED with ML-KEM-768 public key (client) / ciphertext (server). Both shared secrets feed TLS 1.3's HKDF key schedule — one handshake, two algorithms."),
  card("Why must the two shared secrets go through a KDF, not just concatenation?", "Raw concatenation can leak structure and enables cross-protocol confusion; a proper KDF (HKDF with context/labels) gives domain separation and uniform keys. The combiner is load-bearing — NIST IR 8547 and the IETF hybrid drafts specify it."),
  card("What did Chrome's CECPQ2 experiment prove?", "That hybrid X25519+Kyber could ship to billions of TLS connections (2023-2024) without breaking the web: negotiation, middlebox tolerance, and performance were all validated at scale — the deployment template for the standardized X25519MLKEM768."),
  card("Hybrid signatures: same idea, different shape?", "Conceptually yes (sign with both, verify both — or dual certificates), but operationally heavier: certificate chains double in size and validators must understand both. Key-exchange hybrids are the easy win; signature hybrids are adopted more selectively."),
  card("When is pure PQC (no hybrid) the right call?", "Late migration phases and CNSA 2.0's end state: once the PQC component is trusted and validated, hybrids' extra bytes and complexity stop paying. CNSA 2.0's 2031+ posture moves toward PQC-exclusive use."),
  card("What's the main operational cost of hybrids?", "Size: X25519MLKEM768 KeyShare is ~1.2 KB+ vs 32 B for X25519 — ClientHello growth, fragmentation risk, and middlebox intolerance must be tested (M09/M12)."),
  card("Downgrade protection in hybrid negotiation?", "TLS 1.3 negotiates the named group; a network attacker can't silently strip the PQ component without breaking the handshake transcript (Finished MAC covers negotiation). Test that your deployment refuses silent fallback to classical-only.")
 ],
 "quiz": [
  quiz("The hybrid security property means:",
       ["Both algorithms must be broken to break the exchange", "The exchange is secure if at least one component remains secure — a break in either alone does not compromise the session", "Hybrids are twice as fast", "Classical and PQC keys must be the same size"],
       1, "OR-security, not AND: each component independently protects the session. This is what lets you deploy a young standard (ML-KEM) backed by a mature one (X25519)."),
  quiz("In X25519MLKEM768, the TLS 1.3 KeyShare contains:",
       ["Only the ML-KEM public key", "The X25519 ephemeral key and the ML-KEM key material concatenated, with both shared secrets combined via the TLS key schedule KDF", "Two separate handshakes", "A certificate"],
       1, "One group, one KeyShare, concatenated material, KDF-combined secrets. The transcript hash binds the negotiation against downgrade."),
  quiz("Why did large-scale hybrid deployment start with key exchange rather than signatures?",
       ["Signatures don't need quantum resistance", "Key-exchange hybrids are operationally lighter: no certificate-chain doubling, no dual validation paths — one handshake change vs PKI-wide changes", "ML-DSA wasn't ready", "Hybrids don't work for signatures"],
       1, "KEX hybrids touch the handshake; signature hybrids touch the PKI. The industry sequenced the easy win first — a pattern your migration plan should copy."),
  quiz("A middlebox drops ClientHellos larger than 1500 bytes. Your hybrid deployment must:",
       ["Disable PQC", "Test and handle fragmentation/intolerance: TLS record fragmentation, middlebox behavior testing, and fallback policies that never silently downgrade security", "Use smaller keys", "Switch to RSA"],
       1, "Size is the operational tax of PQC. The M09/M12 labs make you measure and mitigate this rather than discovering it in production."),
  quiz("An attacker records a hybrid X25519+ML-KEM handshake today. In 2040 a quantum computer breaks X25519. The session is:",
       ["Broken — X25519 fell", "Safe — ML-KEM still protects the session key (HNDL defeated for this session), assuming ML-KEM holds", "Broken — hybrids don't help HNDL", "Safe only if re-handshaked"],
       1, "This is the point of hybrids against HNDL: the recorded session needs BOTH components broken. Quantum breaks the classical half; the PQ half still stands.")
 ],
 "drills": [
  drill("il30-m07-drill1", [
   ("Hybrid security property, one sentence?", "Secure if EITHER component holds.", "OR-security."),
   ("X25519MLKEM768 KeyShare contents?", "X25519 ephemeral + ML-KEM material concatenated.", "One share, two algorithms."),
   ("Why KDF the two secrets?", "Domain separation + uniformity; raw concat leaks structure.", "Combiner is load-bearing.")
  ]),
  drill("il30-m07-drill2", [
   ("Why hybrids before pure PQC?", "Hedge young-standard risk + validation continuity + mixed-peer interop.", "De-risk the transition."),
   ("Key-exchange vs signature hybrids: which is easier?", "Key exchange — no PKI/chain doubling.", "Handshake vs PKI."),
   ("End state per CNSA 2.0?", "PQC-exclusive use by the 2030s — hybrids are the bridge, not the destination.", "Bridge, not destination.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m07-lab",
  "You will diagram and simulate a hybrid handshake: compute the byte sizes of each KeyShare component, trace both shared secrets through an HKDF-based combiner (using Python's hashlib/hmac), and demonstrate the security property by 'breaking' one component (revealing its secret) and showing the final session key remains unknown. You will also write the downgrade-resistance argument from the TLS transcript.",
  [
   "Compute exact KeyShare sizes: X25519 (32 B) + ML-KEM-768 pk (1184 B) client-side; X25519 (32 B) + ct (1088 B) server-side.",
   "Implement the combiner: session_key = HKDF(x25519_secret || mlkem_secret, info='hybrid-tls13-test') with hashlib.",
   "Simulate the break: reveal x25519_secret to the 'attacker'; show session_key is still uncomputable without mlkem_secret (and vice versa).",
   "Write the downgrade argument: which TLS 1.3 transcript elements prevent silent stripping of the PQ component?"
  ],
  "hybrid_sim.py plus a writeup: size table, combiner code, the break-simulation output, and the downgrade-resistance argument.",
  "Sizes match FIPS constants; both break-simulations leave the session key unknown; the transcript argument names Finished/transcript-hash binding."
 ),
 "mockTask": mock(
  "A vendor proposes 'hybrid' TLS where the client does X25519, and IF the server supports it, a second separate handshake does ML-KEM, concatenating the two session keys with no KDF. Findings?",
  ["Acceptable hybrid", "Two findings: (1) two handshakes doubles round trips and the negotiation isn't transcript-bound together — downgrade/strip attacks; (2) raw concatenation without a KDF is a broken combiner — use the standardized single-handshake X25519MLKEM768 with HKDF combination", "Only the KDF issue matters", "Only the handshake issue matters"],
  1,
  "'Hybrid' is not a vibe: the security property comes from the standardized construction (single transcript, KDF combiner). Ad-hoc hybrids routinely void the property they claim."),
 "videos": [
  video("NIST IR 8547 — transition to PQC standards (initial public draft)", PQCPROJ, "NIST CSRC", "The transition framework: deprecation timelines and migration approaches from NIST.", 30, 1),
  video("Open Quantum Safe — protocol integrations (TLS, SSH)", OQSORG, "Open Quantum Safe", "Where hybrid integrations live: oqs-provider, OQS-OpenSSL, OQS-OpenSSH.", 20, 2)
 ],
 "pdfs": [
  pdf("NCCoE SP 1800-38 — crypto-agility and PQC migration practice guide", NCCOE, "NIST NCCoE", "Migration practice: discovery, agility, phased deployment. Retrieved 2026-10-09."),
  pdf("PQC migration skill — FIPS/hybrid/CBOM reference table", "https://github.com/sayandey322/anthropic-cybersecurity-skills/blob/HEAD/skills/migrating-to-post-quantum-cryptography/SKILL.md", "anthropic-cybersecurity-skills", "Algorithm map: classical → PQC replacements, hybrid groups, tooling. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("The combiner, precisely", "Given classical secret S_c and PQ secret S_pq, the hybrid session key is K = KDF(S_c || S_pq, context). The KDF (HKDF-SHA256/384 in TLS 1.3's schedule) does three jobs: (1) extracts uniform randomness from two non-uniform inputs; (2) domain-separates via labels/context so the same inputs can't be replayed across protocols; (3) ensures that knowledge of one input gives zero information about K without the other (given KDF security). Naive XOR or raw concatenation fails (2) and can fail (3) under cross-protocol attacks. In TLS 1.3 the hybrid group is a named group like any other — the key schedule doesn't care that two algorithms contributed; it just sees a longer shared secret. That design elegance is why deployment was feasible at Chrome scale."),
  note("What CECPQ2 taught the industry", "Google's CECPQ2 (2023-2024) shipped hybrid X25519+Kyber768 to Chrome stable: lessons that became the deployment playbook — (1) middleboxes: oversized ClientHellos triggered intolerance in a measurable fraction of networks; fragmentation and retry logic had to be hardened; (2) negotiation: signaling the hybrid group and falling back cleanly when peers lack support; (3) performance: the added ~1 KB and extra KEM ops were negligible client-side; (4) telemetry first: measuring handshake success rates by group before enforcing. Every enterprise hybrid rollout replays these four lessons — M12's lab makes you replay them hands-on."),
  note("Hybrid signatures and certificates: the harder sibling", "Two approaches: dual signatures (sign with both algorithms, verify both — doubles signature bytes) and composite/hybrid certificates (one cert carrying both keys). Costs: certificate chains balloon (a 3-cert chain with ML-DSA-65 adds ~15 KB), validators need dual algorithm support, and revocation/rotation doubles. Industry posture: key-exchange hybrids now (big HNDL win, low cost), signature hybrids selectively (code signing, roots) while pure-PQC signature migration is planned. Your M10 playbook must cost both paths before recommending one.")
 ]
}

# =====================================================================
# M08 — Migration planning
# =====================================================================
M08 = {
 "id": "IL30-M08", "code": "IL-30",
 "title": "Migration Planning: Inventory, Prioritization & Hybrid Deployment",
 "summary": "The management core of PQC migration: cryptographic discovery and CBOM, inventory methods that actually work, prioritization by exposure × data lifetime × blast radius, phased hybrid-first deployment, and crypto-agility as the architectural requirement.",
 "objectives": [
  "Run cryptographic discovery: network, code, and config inventory methods",
  "Build and maintain a CBOM (Cryptography Bill of Materials)",
  "Prioritize with exposure × lifetime × blast radius scoring",
  "Phase a hybrid-first deployment: pilot → high-value → broad → pure-PQC",
  "Specify crypto-agility requirements for procurement and architecture"
 ],
 "estimatedMinutes": 660, "weight": 1.0,
 "prerequisiteFor": ["IL30-M09","IL30-M10","IL30-M13","IL30-M14"],
 "crossLinks": [
  {"course": "IL-29", "module": "IL29-M33", "note": "Security+ / cert-track crypto domain"},
  {"course": "IL-11", "module": "il11-network-crypto-foundations--zt-encryption", "note": "protocol inventory targets"}
 ],
 "cards": [
  card("What is cryptographic discovery?", "Finding every place cryptography is used: TLS endpoints, certificates, code (libraries/APIs), configs, firmware, VPNs, tokens, HSMs, backups. You cannot migrate what you haven't inventoried — and nobody's inventory is complete on the first pass."),
  card("Three discovery methods?", "Network scanning (TLS handshakes, cert transparency logs), code/dependency analysis (crypto API calls, library versions), config & asset review (PKI inventories, HSM partitions, IaC). Use all three — each misses what the others catch."),
  card("What is a CBOM?", "Cryptography Bill of Materials: a machine-readable inventory (CycloneDX CBOM standard) of algorithms, key lengths, protocols, and certificates per asset — the SBOM's crypto sibling. It makes 'where do we still use RSA-2048?' a query, not a project."),
  card("Prioritization formula?", "Risk ≈ exposure (internet-facing? HNDL-collectible?) × data lifetime (Mosca's x) × blast radius (root CA vs leaf). Sort descending; migrate the top decile first."),
  card("The four migration phases?", "1) Pilot: hybrid KEX on internal/low-risk services, measure. 2) High-value: HNDL-exposed and long-lived secrets go hybrid. 3) Broad: fleet-wide hybrid rollout with interop testing. 4) Pure-PQC: retire classical where policy allows (2030s)."),
  card("Why hybrid-FIRST rather than pure-PQC-first?", "Hybrids preserve interop with unmigrated peers, hedge young-standard risk, and keep FIPS-validated classical components in the loop during transition. Pure-PQC is the end state, not the starting move."),
  card("What is crypto-agility, concretely?", "The architectural property that algorithms are configurable, not hardcoded: algorithm negotiation, pluggable providers (e.g., OpenSSL providers), parameterized key handling, and upgrade paths that don't require rewrites. Procurement must REQUIRE it."),
  card("Biggest inventory pitfall?", "Shadow crypto: embedded devices, third-party SaaS, vendor appliances, and legacy code nobody owns. The first inventory finds ~70%; plan re-scans quarterly."),
  card("How do you handle vendors who 'don't support PQC yet'?", "Contract language with dated commitments, hybrid interop modes that keep you safe while they catch up, and escalation triggers tied to CNSA 2.0 procurement dates (Jan 2027 for NSS)."),
  card("What does 'done' look like for phase 2?", "All HNDL-exposed paths and >10-year-lifetime keys on hybrid-or-better, CBOM queryable and current, and a dated plan for phases 3-4 with owners. 'Done' is a CBOM query returning zero classical-only on priority assets.")
 ],
 "quiz": [
  quiz("Your CBOM query shows RSA-2048 in: (A) public marketing site TLS, (B) firmware signing pipeline, (C) internal dev Jenkins. Migration order?",
       ["A, B, C", "B, A, C", "C, B, A", "All at once"],
       1, "Blast radius × lifetime: firmware signing (B) is long-lived trust with massive blast radius; public TLS (A) is HNDL-exposed; internal dev (C) is lowest. B, A, C."),
  quiz("Crypto-agility in procurement means requiring:",
       ["The cheapest HSM", "Algorithm negotiation, pluggable crypto providers, parameterized key handling, and vendor commitments to PQC support on dated timelines — so the next algorithm change doesn't require re-architecture", "Only NIST-approved algorithms", "On-premise key storage"],
       1, "Agility is the meta-requirement: HAWK/SIKE taught us algorithms change status. Buy the ability to change, not just today's algorithm list."),
  quiz("A business unit says 'we have no crypto inventory and no staff for one.' Your minimum viable answer?",
       ["Skip them", "Start with automated discovery: TLS scanners + certificate-transparency logs + dependency scans produce a first CBOM draft in days; assign ownership per finding; iterate quarterly", "Hire consultants immediately", "Migrate everything blindly"],
       1, "Discovery is automatable to ~70% on the first pass. The perfect inventory is the enemy of the started migration — scan, assign, iterate."),
  quiz("Why is phase 1 (pilot) deliberately low-risk internal services?",
       ["PQC doesn't work on public services", "To measure real-world behavior — handshake sizes, middlebox tolerance, performance, interop — with blast radius contained, before touching HNDL-exposed or revenue paths", "Compliance requires it", "Vendors demand it"],
       1, "CECPQ2's lessons (middlebox intolerance, ClientHello sizes) were learned by measuring. Your pilot is your measurement phase — with rollback ready."),
  quiz("The quarterly CBOM re-scan exists because:",
       ["Auditors like paper", "Shadow crypto: new deployments, vendor updates, and code changes reintroduce classical-only crypto continuously — the inventory decays without re-scanning", "Algorithms change quarterly", "Certificates expire quarterly"],
       1, "Inventory is a process, not a project. Crypto posture decays as systems change; the CBOM must be a living query, not a one-time spreadsheet.")
 ],
 "drills": [
  drill("il30-m08-drill1", [
   ("Three discovery methods?", "Network scanning, code/dependency analysis, config & asset review.", "Scan, code, config."),
   ("CBOM in one line?", "Machine-readable crypto inventory (CycloneDX) — 'where is RSA-2048?' as a query.", "Crypto SBOM."),
   ("Prioritization inputs?", "Exposure × data lifetime × blast radius.", "Three-factor sort.")
  ]),
  drill("il30-m08-drill2", [
   ("Four phases?", "Pilot → high-value → broad → pure-PQC.", "Measure, protect, scale, finish."),
   ("Why hybrid-first?", "Interop + young-standard hedge + validation continuity.", "Bridge strategy."),
   ("Crypto-agility, concretely?", "Algorithms configurable/negotiable/pluggable — no hardcoded crypto.", "Buy the ability to change.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m08-lab",
  "You will run real discovery against a lab target: scan a test host's TLS endpoints (ciphersuites, cert chains, key types), extract crypto usage from a sample codebase (grep for crypto APIs), and assemble the findings into a minimal CycloneDX CBOM JSON. Then you will score and prioritize the findings with the exposure × lifetime × blast radius formula and write the phase plan.",
  [
   "TLS-scan a lab host (testssl.sh or openssl s_client): record protocol versions, key exchange, cert key types/sizes.",
   "Grep a sample repo for crypto calls (RSA/ECDH/AES/MD5 etc.); record library names and versions.",
   "Author a minimal CycloneDX CBOM JSON with the findings (components + crypto properties).",
   "Score each finding (1-5 on exposure, lifetime, blast radius); sort; write the 4-phase plan with owners and dates."
  ],
  "discovery-report.md + cbom.json + phased-plan.md: scan results, the CBOM, prioritized queue, and the dated phase plan.",
  "CBOM validates as JSON and answers 'where is RSA-2048?'; every finding is scored; the phase plan has owners and dates."
 ),
 "mockTask": mock(
  "Leadership wants '100% PQC by end of year' for a 5,000-system estate with no inventory. Your professional response?",
  ["Commit and start swapping algorithms", "Refuse the date, propose the real sequence: 60-90 day discovery + CBOM, prioritized phases starting with HNDL-exposed/long-lived assets, hybrid-first pilots with measurements, dated milestones per phase — and show the Mosca math for why the top decile can't wait but the long tail needs the full program", "Quit", "Outsource it all"],
  1,
  "Unrealistic mandates produce fake compliance. The operator's job: replace the fantasy date with an honest program — discovery first, priorities by risk math, measurable phases."),
 "videos": [
  video("NCCoE SP 1800-38 — migration to PQC practice guide", NCCOE, "NIST NCCoE", "Discovery, crypto-agility, phased migration — the practice companion to the standards.", 40, 1),
  video("CycloneDX CBOM specification", CBOM, "CycloneDX", "The Cryptography Bill of Materials standard your inventory should emit.", 15, 2)
 ],
 "pdfs": [
  pdf("NCCoE — crypto-agility considerations for migrating to PQC", NCCOE, "NIST NCCoE", "The migration practice guide. Retrieved 2026-10-09."),
  pdf("PQC timelines and mandates 2026–2035", TQI, "The Quantum Insider", "The deadline landscape your phases must satisfy. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("Discovery that works", "No single method suffices. Network: scan TLS endpoints (testssl.sh, censys-style data), pull Certificate Transparency logs for your domains, inventory VPN concentrators and their algorithms. Code: grep/AST-scan for crypto APIs (Cipher.getInstance, EVP_*, cryptography.hazmat), pin library versions, check SBOMs for OpenSSL/BoringSSL versions (PQC support landed natively in OpenSSL 3.5; earlier needs oqs-provider). Config/asset: PKI inventories (every CA, every template), HSM partitions and their mechanism lists, IaC/Terraform for TLS settings, MDM for device certs, firmware BOMs. Then the human layer: ask every team 'where do you sign or encrypt?' — the answers will surprise you. Expect the first pass to find ~70%; schedule the second pass before phase 2."),
  note("Scoring and phasing, honestly", "Score 1-5 on: exposure (internet-facing/HNDL-collectible = 5), data lifetime (Mosca's x: >15y = 5), blast radius (root CA/signing infra = 5). Multiply. Top decile → phase 2 immediately. Middle → phase 3. Bottom → phase 4 or accept-and-document. Phase 1 (pilot, 1-3 months): internal services, hybrid KEX, measure everything, practice rollback. Phase 2 (high-value, 3-9 months): HNDL paths + long-lived keys → hybrid. Phase 3 (broad, 9-24 months): fleet rollout, vendor coordination, interop matrices. Phase 4 (pure-PQC, 2030s): retire classical per CNSA 2.0/IR 8547 timelines. Each phase has an exit criterion written BEFORE it starts — otherwise phases never end."),
  note("Crypto-agility as procurement language", "Write it into contracts: 'Supplier shall support algorithm negotiation and pluggable cryptographic providers; shall deliver PQC support for [TLS/signing/HSM] by [date]; shall disclose all cryptographic algorithms and key lengths in CycloneDX CBOM format on delivery and per release.' Tie dates to CNSA 2.0 (Jan 2027 new-acquisition gate for NSS-adjacent; 2030 exclusive-use milestones). Require a written PQC roadmap from every crypto-touching vendor NOW — the vendors without one are your phase-3 risk register. Agility also means internal architecture: no hardcoded algorithm names in application code, centralize crypto in vetted libraries/providers, and keep the KDF/protocol versioning that makes the next transition boring.")
 ]
}

# =====================================================================
# M09 — TLS & network protocol migration playbook
# =====================================================================
M09 = {
 "id": "IL30-M09", "code": "IL-30",
 "title": "Playbook: TLS 1.3 & Network Protocol Migration",
 "summary": "The TLS 1.3 migration runbook: enabling X25519MLKEM768, certificate chains with ML-DSA, size/fragmentation/middlebox handling, interop testing matrices, rollback plans, and the EO 14144 January 2030 TLS 1.3 deadline.",
 "objectives": [
  "Enable hybrid key exchange (X25519MLKEM768) on a TLS 1.3 stack step by step",
  "Plan certificate migration: classical → dual → PQC chains with size budgets",
  "Handle the size tax: fragmentation, record sizing, middlebox intolerance",
  "Build an interop test matrix across clients, libraries, and middleboxes",
  "Write a rollback plan that never silently downgrades security"
 ],
 "estimatedMinutes": 600, "weight": 1.0,
 "prerequisiteFor": ["IL30-M12","IL30-M14"],
 "crossLinks": [
  {"course": "IL-11", "module": "il11-network-crypto-foundations--zt-encryption", "note": "TLS fundamentals this playbook upgrades"},
  {"course": "IL-06", "module": "il-06-cybersecurity-secure-engineering-math-numtheory", "note": "handshake math background"}
 ],
 "cards": [
  card("TLS 1.3 migration step 1?", "Get to TLS 1.3 everywhere first (EO 14144: required across federal systems by Jan 2, 2030). PQC hybrids are a TLS 1.3 feature — 1.2 backports are pain; 1.3 is the floor."),
  card("Enabling X25519MLKEM768: what changes?", "Advertise the hybrid named group in supported_groups; ensure the stack supports it (OpenSSL 3.5+ native, or oqs-provider on 3.0-3.4); size buffers for ~1.2 KB KeyShares; test negotiation and fallback."),
  card("Certificate migration path?", "Classical → dual/hybrid certificates (both keys, both signatures) → PQC-only. Dual certs keep old validators working while new ones get PQ authentication. Budget chain sizes: ML-DSA-65 adds ~3.3 KB per signature."),
  card("The size tax, quantified?", "ClientHello with hybrid KeyShare: +1.2 KB. Cert chain with 2× ML-DSA-65: +10-15 KB. Consequences: TCP fragmentation, TLS record fragmentation, handshake retransmits on lossy links — measure, don't assume."),
  card("Middlebox intolerance: what and how to test?", "Some middleboxes/firewalls drop or mangle oversized ClientHellos or unknown groups. Test through YOUR actual path: canary with telemetry on handshake success/failure by negotiated group, with automatic fallback that logs (never silent)."),
  card("Interop matrix: what axes?", "Clients (browsers, mobile, IoT) × libraries (OpenSSL/BoringSSL/rustls/wolfSSL versions) × middleboxes (your firewalls/proxies) × server configs. Every cell: handshake succeeds, negotiates hybrid, no silent downgrade."),
  card("Rollback plan that is safe?", "Rollback = return to classical-only config via the same deployment pipeline, with alerts (not silent), a written trigger (e.g., >1% handshake failure), and a forward-fix timeline. Never 'temporarily' disable without expiry."),
  card("Why not migrate certificates before key exchange?", "HNDL: key exchange protects recorded traffic retroactively; certificates authenticate the present. KEX first kills the HNDL backlog; cert migration follows on its own (slower, PKI-heavy) schedule."),
  card("Session resumption and 0-RTT with hybrids?", "Resumption derives from the initial handshake's secrets — hybrid-derived resumption keys inherit the hybrid property. 0-RTT's replay risks are unchanged by PQC; keep existing 0-RTT policies."),
  card("What breaks if you skip the pilot?", "You discover middlebox intolerance, oversized-handshake failures, and client incompatibilities in production — on revenue paths. The pilot (M08 phase 1) exists to convert these from incidents into measurements.")
 ],
 "quiz": [
  quiz("First step of the TLS migration playbook?",
       ["Deploy ML-DSA certificates", "Reach TLS 1.3 everywhere — hybrids are a 1.3 feature and EO 14144 mandates 1.3 by Jan 2030", "Disable TLS 1.2 immediately", "Buy new HSMs"],
       1, "Foundation first: 1.3 everywhere, then hybrid KEX, then certificates. Skipping to certs leaves HNDL exposure and 1.2 legacy behind."),
  quiz("A canary shows 2% handshake failures after enabling X25519MLKEM768, concentrated on one legacy proxy fleet. Correct action?",
       ["Disable PQC globally", "Follow the rollback plan for the affected path: revert the proxy fleet's config via pipeline with alerts, keep hybrid on healthy paths, engage the vendor with a dated PQC-support requirement, and re-canary after the fix", "Ignore — 2% is fine", "Switch to pure PQC"],
       1, "Surgical rollback, not global retreat: the plan isolates the intolerant path, keeps the win elsewhere, and converts the incident into a vendor commitment."),
  quiz("Certificate chain sizing with ML-DSA-65: a 3-cert chain grows by approximately?",
       ["100 bytes", "~10-15 KB (each signature ~3.3 KB plus larger public keys)", "1 MB", "It shrinks"],
       1, "3309-byte signatures × 3 plus 1952-byte public keys: the chain roughly quintuples. Path MTU, OCSP, and stapling all need re-examination."),
  quiz("Why does key-exchange migration precede certificate migration?",
       ["Certificates are unimportant", "HNDL: KEX migration retroactively protects recorded traffic; certificates only authenticate new connections — the HNDL backlog is the urgent risk", "KEX is easier to spell", "CAs forbid it"],
       1, "Sequencing by risk: recorded handshakes are being stockpiled NOW. Cert migration is PKI-heavy and slower — schedule it second, deliberately."),
  quiz("Your rollback trigger fires. What must the rollback NOT do?",
       ["Alert the team", "Silently downgrade to classical-only with no alert, no expiry, and no forward-fix date — that converts a temporary mitigation into permanent, invisible exposure", "Use the deployment pipeline", "Log the event"],
       1, "Silent permanent downgrade is the failure mode. Rollbacks are loud, dated, and forward-fixed — otherwise 'temporary' becomes forever.")
 ],
 "drills": [
  drill("il30-m09-drill1", [
   ("Migration order: 1.3, KEX, certs — why this sequence?", "1.3 is the platform; KEX kills HNDL; certs are PKI-heavy and follow.", "Platform, traffic, identity."),
   ("Hybrid KeyShare size cost?", "~+1.2 KB in ClientHello.", "The size tax."),
   ("EO 14144 TLS deadline?", "TLS 1.3 (or successor) across federal systems by Jan 2, 2030.", "2030 floor.")
  ]),
  drill("il30-m09-drill2", [
   ("Interop matrix axes?", "Clients × libraries × middleboxes × server configs.", "Four axes, every cell tested."),
   ("Middlebox intolerance test?", "Canary with per-group handshake telemetry through the real path.", "Measure, don't assume."),
   ("Safe rollback properties?", "Pipeline-driven, alerting, trigger-defined, expiry-dated, forward-fix planned.", "Loud, dated, temporary.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m09-lab",
  "You will stand up two TLS 1.3 endpoints (OQS-OpenSSL or OpenSSL 3.5+ with PQC) and: negotiate X25519MLKEM768, capture the handshake and measure ClientHello/KeyShare/certificate sizes, test a simulated intolerant middlebox (MTU clamp), and execute a rollback drill. All in a local lab — no production systems.",
  [
   "Build or install a PQC-capable OpenSSL (3.5+ native or oqs-provider); generate a test CA and server cert.",
   "Configure the server to prefer X25519MLKEM768; connect with s_client; confirm negotiated group in the session output.",
   "Capture with Wireshark/tshark: record ClientHello size, KeyShare size, full handshake bytes; compare against classical-only.",
   "Simulate intolerance: clamp MTU / use a dropping proxy; observe failure mode; document the telemetry you'd alert on.",
   "Execute the rollback drill: revert to classical-only via config change, verify, then re-enable — timed, with a written trigger."
  ],
  "tls-lab-report.md: negotiated-group proof, size measurements (classical vs hybrid), intolerance observations, and the timed rollback drill log.",
  "Hybrid group negotiates; sizes are measured and compared; the intolerance failure mode is documented; rollback completes via pipeline-like steps under the written trigger."
 ),
 "mockTask": mock(
  "A CDN vendor says 'we support PQC' but their handshake negotiates classical-only with your hybrid-preferring clients and offers no telemetry on why. Assessment and ask?",
  ["Accept — support is support", "Not acceptable: require (1) named-group support list in writing, (2) per-group handshake telemetry, (3) a dated roadmap to hybrid-by-default, (4) contract language tying to your 2027/2030 milestones — 'supports PQC' without negotiation proof is marketing", "Switch CDNs immediately", "Disable hybrid on your side"],
  1,
  "Verify, don't trust: negotiation proof plus telemetry plus dated commitments. Vague PQC claims are the vendor-risk register's favorite entry."),
 "videos": [
  video("OQS-OpenSSL / oqs-provider — PQC in TLS", OQSPROV, "Open Quantum Safe", "The integration path: provider-based PQC for OpenSSL 3.x and the demo topologies.", 20, 1),
  video("NIST IR 8547 transition guidance — deprecation timelines", PQCPROJ, "NIST CSRC", "Which algorithms deprecate when: the planning baseline for protocol sequencing.", 30, 2)
 ],
 "pdfs": [
  pdf("NCCoE SP 1800-38 — migration practice guide (protocol chapters)", NCCOE, "NIST NCCoE", "Phased protocol migration in practice. Retrieved 2026-10-09."),
  pdf("CNSA 2.0 timeline and enforcement (V2.1 FAQ analysis)", "https://postquantum.com/security-pqc/nsa-cnsa-2-0-faq-v2-1-update/", "postquantum.com", "Procurement gate Jan 2027, phase-outs 2030/2031, category timelines. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("The runbook, in order", "1) TLS 1.3 everywhere (measure current 1.2/1.3 split; EO 14144 says Jan 2030 — beat it). 2) Library readiness: OpenSSL 3.5+ (native ML-KEM/ML-DSA/SLH-DSA + hybrid groups) or oqs-provider on 3.0–3.4; BoringSSL/rustls/wolfSSL per their PQC support matrices. 3) Lab: negotiate X25519MLKEM768, measure sizes, test your actual middlebox path. 4) Canary: 1% of traffic with per-group telemetry and a written rollback trigger. 5) Expand: high-value/HNDL paths first (M08 scoring). 6) Certificates: dual/hybrid certs where validators need them, then PQC chains — budgeted for size. 7) Harden: disable classical-only fallback where policy allows; alert on any negotiated-classical event on priority paths. 8) Document: the interop matrix becomes a living artifact, re-run per release."),
  note("Size engineering", "Budget per connection: ClientHello +~1.2 KB (hybrid KeyShare), ServerHello/KeyShare +~1.1 KB, certificate chain +10-15 KB (ML-DSA-65 ×3). Mitigations: TLS record fragmentation (negotiate sensibly), certificate compression (RFC 8879) — big win for PQC chains, session resumption to amortize full handshakes, and MTU/path validation in the pilot. On lossy or constrained links, measure handshake completion rates explicitly — PQC's handshake is heavier and loss amplifies that. None of this is exotic; it's the same discipline as the ECDSA→RSA-size transitions, with bigger numbers."),
  note("The downgrade-safety contract", "Every stage of the migration must answer: 'what does an attacker on the path get by interfering with negotiation?' TLS 1.3's transcript binding means stripping the PQ group breaks the Finished MAC — the handshake fails closed, not open. Your deployment must preserve that property: no 'compatibility mode' that silently accepts classical-only when hybrid was policy, no middlebox 'optimizations' that strip unknown groups, and alerts on every classical-negotiated handshake on migrated paths. Test the attack, not just the feature: run the stripping proxy in the lab and confirm the failure is loud.")
 ]
}

# =====================================================================
# M10 — SSH, VPN, code-signing playbook
# =====================================================================
M10 = {
 "id": "IL30-M10", "code": "IL-30",
 "title": "Playbook: SSH, VPN & Code-Signing Migration",
 "summary": "Beyond TLS: hybrid key exchange in OpenSSH (sntrup761x25519 and the ML-KEM successors), IPsec/WireGuard VPN migration, and the code-signing pipeline — ML-DSA vs SLH-DSA vs (future) FN-DSA, with size budgets and verification-at-scale thinking.",
 "objectives": [
  "Enable PQC/hybrid key exchange in OpenSSH and verify negotiation",
  "Plan IPsec VPN migration: IKEv2 with ML-KEM hybrids, CNSA 2.0 2030 networking deadline",
  "Design a code-signing migration: algorithm choice, key ceremony, size budgets",
  "Handle verification at scale: millions of verifiers, constrained devices",
  "Sequence SSH/VPN/signing against the TLS work without resource collisions"
 ],
 "estimatedMinutes": 600, "weight": 0.9,
 "prerequisiteFor": ["IL30-M14"],
 "crossLinks": [
  {"course": "IL-11", "module": "il11-network-crypto-foundations--zt-hashing", "note": "hashing/integrity for code signing"},
  {"course": "IL-04", "module": "il04-networking", "note": "networking core context (IL-04 Networking Core: Network+)"}
 ],
 "cards": [
  card("What PQC does OpenSSH already ship?", "OpenSSH 9.0+ (2022) defaults to sntrup761x25519-sha512 — a hybrid of Streamlined NTRU Prime and X25519 — for key exchange. The ML-KEM-based successors (mlkem768x25519) are the standards-aligned future; track your distro's support."),
  card("Why did OpenSSH move BEFORE the NIST finals?", "SSH key exchange is the HNDL front line for admin access, and sntrup761 was a conservative, well-reviewed hybrid — OpenSSH chose to protect sessions early rather than wait. Lesson: HNDL urgency can justify pre-standard hybrids with conservative choices."),
  card("Enabling/verifying in practice?", "Check 'kex' in ssh -Q / sshd -T; the client/server negotiate the strongest mutual method. Verify with ssh -vvv (look for the kex algorithm line) — then pin it in sshd_config/ssh_config where policy requires."),
  card("IPsec/IKEv2 migration shape?", "IKEv2 negotiates key exchange methods; ML-KEM hybrid KEX drafts exist for IKEv2. CNSA 2.0: traditional networking equipment (VPNs, routers) must support-and-prefer PQC by 2026, exclusively use by 2030. Vendor firmware is the long pole — start vendor conversations now."),
  card("WireGuard's PQC posture?", "WireGuard's handshake is Noise-based with fixed X25519; PQC variants are research/prototype stage. For VPN PQC today: IPsec with PQC KEX, or hybrid TLS-based VPNs — not WireGuard mainline."),
  card("Code-signing algorithm choice?", "ML-DSA-65: the default (fast signing, moderate size). SLH-DSA-s: infrequent signing, tiny verifier keys, conservative assumptions (firmware). FN-DSA: when final and size-constrained (bootloaders). Match the signer/verifier economics, not just security level."),
  card("The code-signing migration checklist?", "New PQC signing keys (ceremony!), dual-sign during transition (classical + PQC signatures on artifacts), verifier updates BEFORE enforcing PQC-only verification, timestamping continuity, and HSM/firmware support verification."),
  card("Why 'verifiers before enforcement'?", "A PQC-only signature that old verifiers reject = bricked fleet. Ship verifier support (OS updates, bootloader updates) first, dual-sign during the overlap, enforce PQC-only after telemetry shows verifier coverage."),
  card("Key ceremony for the new signing keys?", "Fresh entropy, audited ceremony, HSM-backed, split knowledge/dual control, recorded — the PQC migration is the moment to fix every shortcut in the old ceremony too. ML-DSA keys are bigger; confirm HSM slot/mechanism support first."),
  card("Size budgets for signed artifacts?", "ML-DSA-65 adds ~3.3 KB per signature; dual-signing doubles that; SLH-DSA-128s adds ~7.8 KB. Bootloaders, OTA partitions, and package formats (RPM/Deb/MSI) all have size assumptions to re-validate.")
 ],
 "quiz": [
  quiz("OpenSSH's default PQC-hybrid key exchange (9.0+) is:",
       ["mlkem768x25519-sha512", "sntrup761x25519-sha512 — Streamlined NTRU Prime × X25519, shipped before the NIST finals as HNDL protection", "rsa2048-sha256", "ecdh-nistp256"],
       1, "OpenSSH moved early on HNDL grounds with a conservative hybrid. ML-KEM-based method names are the standards-aligned successors — know both, and what your fleet negotiates."),
  quiz("The #1 rule of code-signing migration sequencing?",
       ["Sign with PQC immediately", "Update verifiers BEFORE enforcing PQC-only verification — enforcement before verifier coverage bricks the fleet", "Rotate keys monthly", "Dual-sign forever"],
       1, "Verifier coverage is the gating metric. Dual-sign during overlap; enforce only when telemetry proves the fleet can verify."),
  quiz("CNSA 2.0 for traditional networking equipment (VPNs, routers):",
       ["No requirements", "Support and prefer PQC by 2026, exclusively use by 2030", "2035", "Only for new purchases after 2033"],
       1, "2026 support-and-prefer / 2030 exclusive-use. Vendor firmware cycles are long — this deadline is why vendor conversations start in phase 1."),
  quiz("Your HSM doesn't support ML-DSA. Options, in order?",
       ["Abandon PQC", "Check vendor roadmap/firmware updates for PQC mechanisms; evaluate partitioned approaches (signing service in front of HSM); include PQC mechanism support as a hard requirement in the next HSM procurement; never extract keys to work around the HSM", "Export the keys to software", "Use smaller keys"],
       1, "HSM mechanism support is a real gating item — which is why the inventory (M08) includes HSM partitions. Workarounds that extract keys defeat the HSM's purpose."),
  quiz("Dual-signing during transition means:",
       ["Signing twice with the same key", "Artifacts carry both a classical and a PQC signature; old verifiers check the classical one, new verifiers check both — coverage without breakage", "Two engineers sign", "Signing the signature"],
       1, "The bridge: no verifier left behind, PQC protection building. Sunset the classical signature on the dated plan, not by accident.")
 ],
 "drills": [
  drill("il30-m10-drill1", [
   ("OpenSSH default PQC kex?", "sntrup761x25519-sha512 (9.0+); ML-KEM successors incoming.", "Early hybrid, conservative choice."),
   ("Verify negotiated kex?", "ssh -vvv shows the kex line; sshd -T / ssh -Q list support.", "Check, don't assume."),
   ("IKEv2 PQC path?", "ML-KEM hybrid KEX drafts; vendor firmware is the long pole.", "Standards + vendors.")
  ]),
  drill("il30-m10-drill2", [
   ("Code-signing algorithm default?", "ML-DSA-65; SLH-DSA-s for rare/long-lived; FN-DSA when final + size-bound.", "Match economics, not just level."),
   ("Sequencing rule?", "Verifiers first, dual-sign overlap, enforce last.", "Coverage gates enforcement."),
   ("CNSA 2.0 networking deadline?", "Support+prefer by 2026, exclusive by 2030.", "Vendor clock is ticking.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m10-lab",
  "You will: verify PQC key exchange negotiation on a local OpenSSH setup, benchmark and compare key/signature sizes for a code-signing decision (ML-DSA-65 vs SLH-DSA-128s via liboqs if available), and write the verifier-coverage plan for a fictional 50k-device fleet including the dual-signing window and enforcement trigger.",
  [
   "On a lab VM: check supported kex (ssh -Q kex), connect with -vvv, and record the negotiated key exchange.",
   "Pin the PQC-hybrid kex in ssh_config/sshd_config on the lab hosts; reconnect and confirm.",
   "Size exercise: tabulate artifact-size impact of ML-DSA-65 vs SLH-DSA-128s vs dual classical+PQC for a 10 MB firmware image.",
   "Write the fleet plan: verifier update waves, dual-signing window dates, telemetry proving coverage, and the enforcement trigger with rollback."
  ],
  "ssh-lab.md + signing-decision.md + fleet-plan.md: negotiation proof, size table, and the dated verifier-coverage plan.",
  "Negotiated kex is recorded and pinned; size table uses FIPS constants; the fleet plan's enforcement trigger is telemetry-based with rollback."
 ),
 "mockTask": mock(
  "The release team wants to 'just switch' code signing to ML-DSA next sprint. Fleet: 50k devices, mixed firmware ages, no verifier telemetry. Your call?",
  ["Approve — PQC urgency", "Block the switch; require: verifier capability inventory first, dual-signing implementation, staged verifier updates with telemetry, and only then a dated enforcement milestone. 'Just switch' bricks every device whose verifier predates PQC support.", "Approve for new devices only", "Delay a year"],
  1,
  "Code signing is the one migration where the failure mode is unbootable hardware. Verifier coverage is the gating metric — everything else follows it."),
 "videos": [
  video("Open Quantum Safe — OpenSSH integration", OQSORG, "Open Quantum Safe", "OQS-OpenSSH: prototype PQC key exchange and authentication in SSH.", 15, 1),
  video("CNSA 2.0 timeline and enforcement (V2.1 FAQ)", "https://postquantum.com/security-pqc/nsa-cnsa-2-0-faq-v2-1-update/", "postquantum.com", "Networking-equipment deadlines and the procurement gate mechanics.", 20, 2)
 ],
 "pdfs": [
  pdf("NIST FIPS 204 (ML-DSA) — code-signing default", FIPS204, "NIST CSRC", "The signature standard behind the signing playbook. Retrieved 2026-10-09."),
  pdf("NIST FIPS 205 (SLH-DSA) — firmware-signing conservative option", FIPS205, "NIST CSRC", "When hash-based fits the signing economics. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("SSH: the early mover", "OpenSSH 9.0 (April 2022) made sntrup761x25519-sha512 the default key exchange — a hybrid of the Streamlined NTRU Prime KEM and X25519, chosen conservatively years before the NIST finals because SSH sessions are prime HNDL targets (admin credentials, tunneled data). The lesson for your program: where HNDL risk is high and the hybrid is conservative, waiting for the final FIPS is the wrong call — but you must then track the standards-aligned successor (ML-KEM-based kex) and plan the second hop. Inventory your fleet's OpenSSH versions NOW: anything pre-9.0 negotiates classical-only, and embedded/old-LTS SSH is the long tail that breaks 'we're done' claims."),
  note("VPNs: the vendor problem", "IPsec/IKEv2 has PQC key-exchange drafts and CNSA 2.0 gives networking equipment the 2026/2030 support/exclusive-use deadlines — but the equipment runs vendor firmware, and firmware cycles are 12-36 months. Your playbook: (1) inventory every VPN concentrator, router, and firewall with its firmware and crypto capabilities; (2) get written PQC roadmaps from each vendor with dates; (3) where vendors lag, plan overlay/migration paths (TLS-based VPN, or hybrid tunnels) rather than waiting; (4) test PQC KEX interop between vendors early — multi-vendor IKEv2 PQC is where interop goes to die. WireGuard: no PQC in mainline; don't plan around future WireGuard PQC — plan around IPsec/TLS-based options that exist."),
  note("Code signing: the ceremony is the product", "New PQC signing keys deserve a real key ceremony: fresh entropy (audited), HSM-backed with confirmed ML-DSA/SLH-DSA mechanism support, split knowledge and dual control, witnessed and recorded. Then the sequencing: (1) ship verifier support (OS/bootloader/package-manager updates) and MEASURE coverage via telemetry; (2) dual-sign artifacts (classical + PQC) through the overlap window; (3) enforce PQC verification only when coverage telemetry clears your threshold, with rollback ready. Size the artifacts: ML-DSA-65 +3.3 KB/sig, SLH-DSA-128s +7.8 KB — re-validate bootloader partition budgets, OTA diff sizes, and package-format limits. Timestamping: ensure your TSA chain migrates too, or long-term signature validation breaks at the timestamp, not the signature.")
 ]
}

# =====================================================================
# M11 — Toy lattice schemes lab
# =====================================================================
M11 = {
 "id": "IL30-M11", "code": "IL-30",
 "title": "Lab: Toy Lattice Schemes in Python",
 "summary": "Build intuition by building: a Regev-style LWE cryptosystem, a Module-LWE toy KEM, and a Babai-style CVP decoder — all at toy sizes where attacks still work, so you feel exactly where the hardness comes from.",
 "objectives": [
  "Implement Regev LWE encryption/decryption at toy parameters",
  "Build a Module-LWE toy KEM and measure its failure rate",
  "Implement Babai's nearest-plane CVP decoder and watch it fail on bad bases",
  "Run lattice-reduction (LLL) at toy sizes to see the attack work",
  "State precisely which toy simplifications must NEVER ship"
 ],
 "estimatedMinutes": 720, "weight": 1.0,
 "prerequisiteFor": ["IL30-M12","IL30-M14"],
 "crossLinks": [
  {"course": "IL-02", "module": "il-02-mathematical-maturity-engine-math-logic", "note": "proof spine behind the reductions"},
  {"course": "IL-06", "module": "il-06-cybersecurity-secure-engineering-math-numtheory", "note": "modular arithmetic toolkit"}
 ],
 "cards": [
  card("Regev LWE encryption, toy version?", "pk: (A, b = A·s + e). Encrypt bit m: pick random subset (or random r), send (u = r^T·A, v = r^T·b + m·⌊q/2⌉). Decrypt: v − u·s ≈ m·⌊q/2⌉ + noise; round to recover m. Noise must stay < q/4."),
  card("Why does decryption work?", "v − ⟨u, s⟩ = m·⌊q/2⌉ + (small noise). If the noise magnitude stays below q/4, rounding recovers m exactly. Parameter design = keeping noise in that band."),
  card("Babai's nearest plane: what does it do?", "Given a lattice basis and a target, it rounds coordinates in the Gram–Schmidt basis — a polynomial-time APPROXIMATE CVP solver. On good bases it's near-exact; on bad (crypto) bases the approximation is uselessly loose."),
  card("What does LLL do, and why do we run it in the lab?", "LLL lattice reduction converts a bad basis into a somewhat-better one in polynomial time. At toy dimensions it breaks toy schemes — demonstrating that 'hard' is parameter-dependent and reductions have concrete thresholds."),
  card("Toy vs real: name three simplifications that must never ship.", "(1) Tiny moduli/dimensions (brute-forceable). (2) No side-channel protection (Python ints leak timing). (3) No FO transform / no KATs / no domain separation. Toys teach; FIPS implementations ship."),
  card("How do you MEASURE a toy KEM's failure rate?", "Run N encaps/decaps trials, count mismatches: failure_rate ≈ failures/N. Real ML-KEM targets ~2^-139 — your toy will show percents, which is the point: parameters control the rate."),
  card("What happens when you grow the error past q/4 in the toy?", "Decryption failures appear, then dominate — the correctness cliff. This is why FIPS parameters are fixed: the error band is engineered, not chosen."),
  card("Why implement the attack (LLL/brute force) yourself?", "To calibrate 'hard': watching your toy fall at dimension 20 while ML-KEM uses dimension 768·(k) makes the security margin visceral, not abstract."),
  card("Module vs plain LWE in your toy: what's the visible difference?", "Module-LWE packs the dimension into ring elements (k=2 over R_q vs n=512 over Z_q): same security dimension, far less code and key material — you feel the ring's efficiency directly."),
  card("Lab safety rule?", "Toy code is labeled TOY in every file header, never imported by anything real, and the writeup lists the five reasons it must never ship. Confusion between teaching code and production code is a career-ending bug class.")
 ],
 "quiz": [
  quiz("In Regev encryption, decryption recovers m because:",
       ["The modulus is prime", "v − ⟨u,s⟩ = m·⌊q/2⌉ + small noise, and rounding removes noise below q/4", "The attacker can't do linear algebra", "Gaussian elimination is slow"],
       1, "Correctness is a noise budget: everything works iff accumulated noise stays under q/4. Parameter selection IS noise-budget engineering."),
  quiz("Babai's nearest-plane decoder on a cryptographic (bad) basis:",
       ["Recovers the secret", "Runs fast but returns a uselessly loose approximation — which is exactly why the bad basis is safe to publish", "Is exponential-time", "Requires a quantum computer"],
       1, "Approximation quality depends on basis quality: good basis → near-exact; bad basis → garbage. The trapdoor is the good basis you never publish."),
  quiz("Your toy KEM shows 3% decryption failures. This tells you:",
       ["The scheme is broken", "Parameters are wrong for correctness: noise exceeds the q/4 budget too often — real deployments need failure rates ~2^-139, which is why FIPS parameters are fixed and validated", "LWE is insecure", "Increase the message size"],
       1, "Correctness failures are a parameter bug, and at scale they're also a security issue (failure-boosting attacks). The lab makes the cliff visible."),
  quiz("Running LLL against your toy at dimension 24 succeeds. Correct conclusion?",
       ["LWE is broken, tell NIST", "Hardness is parameter-dependent: toy dimensions fall to polynomial attacks; real parameters (dimension 512-1024+) are far beyond LLL/BKZ reach — which is why parameters are standardized, not improvised", "LLL breaks ML-KEM", "Increase q"],
       1, "The lab's whole point: feel the threshold. Toy falls, real stands — and the distance between them is quantified by decades of lattice cryptanalysis."),
  quiz("Which is an acceptable use of your toy implementation?",
       ["Shipping it in an internal tool ('it's just internal')", "Teaching and intuition only — labeled TOY, never imported by real code, with the writeup's never-ship list", "Using it where performance doesn't matter", "Publishing as a library"],
       1, "'Just internal' is how toy crypto reaches production. The lab's safety rule is absolute: teaching code never ships, no exceptions, no matter the deployment.")
 ],
 "drills": [
  drill("il30-m11-drill1", [
   ("Regev decrypt equation?", "m' = round((v − ⟨u,s⟩) / ⌊q/2⌉); works iff noise < q/4.", "Noise budget."),
   ("Babai: good basis vs bad basis?", "Good: near-exact. Bad: useless approximation.", "Basis quality = trapdoor."),
   ("LLL in one line?", "Polynomial-time basis improvement; breaks toys, not real params.", "Feel the threshold.")
  ]),
  drill("il30-m11-drill2", [
   ("Measure toy failure rate how?", "N trials, count mismatches.", "Empirical rate."),
   ("Three never-ship simplifications?", "Tiny params, no side-channel care, no FO/KATs/domain separation.", "Toys teach; FIPS ships."),
   ("Module-LWE visible win?", "Dimension packed into ring elements: less code, less key material.", "Rings are efficient.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m11-lab",
  "The capstone lab of the math spine: implement Regev LWE encryption, a Module-LWE toy KEM with measured failure rate, Babai's nearest-plane decoder, and an LLL/break demo at toy sizes. Every file labeled TOY. Deliverable includes the never-ship list.",
  [
   "Implement Regev encrypt/decrypt over Z_q (q=97, n=16); verify round-trip for random bits; measure failure rate over 1000 trials.",
   "Extend to Module-LWE toy KEM (k=2 over Z_17[x]/(x^4+1)); measure failure rate; push error size past the cliff and record it.",
   "Implement Babai nearest-plane; decode with a good basis (succeeds) vs a bad basis (fails) — same lattice, both bases.",
   "Brute-force/LLL the toy secret at small dimension; time it; extrapolate to ML-KEM-768 dimensions and write the margin.",
   "Write the never-ship list: five concrete reasons this code must never leave the lab."
  ],
  "toy_lattice/ (TOY-labeled): regev.py, module_kem.py, babai.py, attack_demo.py, plus NEVER_SHIP.md and the failure-rate/margin writeup.",
  "Round-trips succeed; failure cliff demonstrated and measured; good/bad basis decoder contrast shown; attack works at toy size with quantified margin to real; NEVER_SHIP.md complete."
 ),
 "mockTask": mock(
  "A junior engineer, inspired by this module, proposes 'our own lattice KEM with custom parameters for our IoT fleet' to save key size. Your response?",
  ["Encourage innovation", "Hard no: custom parameters void the FIPS security analysis, KATs, and validation path; the size savings are dwarfed by the risk of a broken-by-design scheme. Use standardized ML-KEM (possibly 512) or document why PQC can't fit and what compensating controls apply.", "Approve with a security review", "Approve for IoT only"],
  1,
  "This is the module's punchline: the labs teach you enough to understand the standards and exactly enough to know never to freelance them. Custom crypto parameters are a unilateral disarmament."),
 "videos": [
  video("NIST FIPS 203 — parameter choices and rationale", FIPS203, "NIST CSRC", "Why the parameters are what they are: the fixed, reviewed choices your toys approximate.", 45, 1),
  video("CRYSTALS-Kyber design documentation", KYBER, "pq-crystals.org", "The design story behind the parameters: noise budgets, NTT, and security estimates.", 20, 2)
 ],
 "pdfs": [
  pdf("NIST FIPS 203 — the real parameter sets", FIPS203, "NIST CSRC", "Compare your toy's cliff against the engineered FIPS band. Retrieved 2026-10-09."),
  pdf("PQC standards tracker", KFCIPHER, "KFCipher", "Status board. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("Regev's cryptosystem, concretely (toy)", "Parameters: q=97, n=16, error in {−1,0,1}. KeyGen: A ← random n×n over Z_q, s ← small secret, e ← small errors, b = A·s + e. pk=(A,b), sk=s. Encrypt bit m: random binary r; u = rᵀA; v = rᵀb + m·⌊97/2⌉ = rᵀb + 48m. Decrypt: d = v − ⟨u,s⟩ = 48m + rᵀe (small noise); if d closer to 0 → m=0, closer to 48 → m=1. The noise rᵀe grows with n — at n=16 it's tiny; scale n up and you must scale q or shrink errors. That three-way tension (n, q, error) IS lattice parameter design, and the FIPS sets are its settled resolution."),
  note("Babai and the good-basis/bad-basis chasm", "Babai's nearest plane: Gram–Schmidt the basis, then round the target's coordinates from the last vector backward — each rounding picks the nearest hyperplane. With a good basis (short, near-orthogonal), the rounded point is genuinely close to the target: CVP approximately solved. With a bad basis (long, skewed — exactly what a public key is), each rounding step compounds error and the output is nowhere near the target. Same lattice, two bases, two universes. Run both in the lab: the contrast is the most convincing five minutes in lattice cryptography."),
  note("Why the lab attacks its own toys", "Three attacks, three lessons: (1) brute force at tiny qⁿ — calibrates exponential scaling; (2) LLL/BKZ lattice reduction — shows 'hard' has a concrete dimensional threshold and that reduction quality degrades predictably with dimension (root-Hermite-factor thinking, intuitively); (3) the error-cliff experiment — correctness is engineered, not assumed. None of these touch real ML-KEM parameters, and that's the lesson: the margin between 'my laptop breaks it' and 'nobody breaks it' is quantified, published, and standardized. Your job is to operate inside the standardized margin, never to redraw it.")
 ]
}

# =====================================================================
# M12 — Hybrid TLS lab with liboqs
# =====================================================================
M12 = {
 "id": "IL30-M12", "code": "IL-30",
 "title": "Lab: Hybrid TLS with liboqs — Build, Handshake, Capture",
 "summary": "The integration lab: build liboqs, drive KEMs and signatures through its API, stand up OQS-OpenSSL with X25519MLKEM768, capture real hybrid handshakes, and measure everything M09's playbook needs.",
 "objectives": [
  "Build liboqs and run its KEM/signature API (keygen, encaps, sign, verify)",
  "Stand up a hybrid TLS 1.3 handshake with X25519MLKEM768",
  "Capture and dissect the handshake: sizes, groups, negotiation",
  "Benchmark ML-KEM/ML-DSA/SLH-DSA operations and tabulate the results",
  "Document the exact build versions for reproducibility"
 ],
 "estimatedMinutes": 660, "weight": 1.0,
 "prerequisiteFor": ["IL30-M14"],
 "crossLinks": [
  {"course": "IL-04", "module": "il04-linux", "note": "Linux lab context (IL-04 Linux Foundations)"},
  {"course": "IL-11", "module": "il11-network-crypto-foundations--zt-encryption", "note": "TLS fundamentals"}
 ],
 "cards": [
  card("What is liboqs?", "The Open Quantum Safe project's C library: implementations of PQC KEMs and signatures (including the FIPS standards) behind a common API, plus test harnesses and benchmarks — the lab and prototyping standard for PQC."),
  card("liboqs API shape (KEM)?", "OQS_KEM_new(alg) → keypair() → encaps() → decaps(); OQS_KEM_alg_is_enabled(). Same pattern for SIG: keypair/sign/verify. One API, every algorithm — which is why it's the integration lab tool."),
  card("oqs-provider: what does it do?", "An OpenSSL 3 provider plugging PQC KEMs/signatures and hybrid groups into OpenSSL — so existing OpenSSL-based apps get PQC without code changes. (OpenSSL 3.5+ has native support; oqs-provider covers 3.0–3.4.)"),
  card("What will you capture in the handshake?", "Negotiated group (X25519MLKEM768), ClientHello/KeyShare sizes, certificate algorithms and sizes, handshake transcript bytes, timing — the evidence M09's playbook decisions rest on."),
  card("Benchmark discipline?", "Same machine, same build flags, N iterations, report ops/sec AND per-op ms for keygen/encaps/decaps/sign/verify across ML-KEM-512/768/1024, ML-DSA-44/65/87, SLH-DSA-128s/128f. Versions recorded."),
  card("Why does the lab pin exact versions?", "PQC implementations move fast (oqs-provider, OpenSSL 3.5): results without versions are unrepeatable. Reproducibility is part of the deliverable."),
  card("Biggest build gotcha?", "Provider path config (OPENSSL_MODULES / provider config files) — the #1 'it built but doesn't negotiate' cause. The lab makes you verify negotiation explicitly, not assume it."),
  card("What does 'KEM' vs 'SIG' provider config look like?", "openssl.cnf provider sections activating oqsprovider; then groups = X25519MLKEM768 in the SSL config. Verify with openssl list -providers and a test handshake."),
  card("How do you prove the hybrid property in the lab?", "Capture shows both components' material in KeyShare; config shows both algorithms required; break-simulation (M07) shows either secret alone is insufficient. Evidence, not claims."),
  card("Lab-to-production gap: what doesn't transfer?", "Lab certs (no trust), lab keys (no ceremony), performance on lab VMs (not capacity planning), and security properties of the lab build (not FIPS-validated). The lab teaches mechanics; production needs the validated path.")
 ],
 "quiz": [
  quiz("After configuring oqs-provider, the handshake still negotiates X25519. First check?",
       ["Rebuild everything", "Verify the provider actually loaded (openssl list -providers), the config file is being read (OPENSSL_CONF), and the group is in the offered groups list — provider-path/config issues are the #1 cause", "Blame the network", "Disable TLS 1.3"],
       1, "Configuration, not compilation: provider loading and group offering are the two silent failure points. Verify each explicitly."),
  quiz("Your benchmark shows ML-DSA-87 signing at 0.05 ms and SLH-DSA-128s at 25 ms. Correct reading?",
       ["SLH-DSA is broken", "Expected: lattice signing is microseconds; hash-based signing is milliseconds — the 500x gap is the construction (tens of thousands of hashes), not a bug. This is why algorithm choice follows signing frequency.", "The benchmark is wrong", "Use 128f instead"],
       1, "The gap is structural. Benchmarks calibrate decisions: high-frequency signing → ML-DSA; rare signing → SLH-DSA viable."),
  quiz("Why record exact build versions in the lab report?",
       ["Pedantry", "PQC stacks evolve rapidly; without versions (liboqs, oqs-provider, OpenSSL) results aren't reproducible and can't be compared to future runs or vendor claims", "Auditors require it", "It speeds up the build"],
       1, "Reproducibility is the deliverable's backbone — especially in a field where the software moves quarterly."),
  quiz("Wireshark shows the ServerHello selected X25519MLKEM768 but your client log says handshake failed after. Likely?",
       ["The group is unsupported", "Size/path issue downstream: check certificate chain handling, middlebox interference, or client-side buffer limits for the larger messages — negotiation succeeded, something after it didn't", "PQC is broken", "Wrong port"],
       1, "Negotiation succeeding then failing points past the group choice: certs, sizes, middleboxes. The capture tells you where — read it."),
  quiz("The lab uses self-signed certs. What must the report state?",
       ["Nothing", "Explicitly: lab PKI carries no trust — production needs real CA issuance, ceremony, and validation. Mechanics transfer; trust doesn't.", "Self-signed is fine for production", "Certs don't matter"],
       1, "Lab-to-production gaps get written down, not assumed away. Trust infrastructure is a separate workstream (M10).")
 ],
 "drills": [
  drill("il30-m12-drill1", [
   ("liboqs KEM API calls?", "OQS_KEM_new → keypair → encaps → decaps.", "One API, every KEM."),
   ("oqs-provider role?", "Plugs PQC into OpenSSL 3.0–3.4 without app rewrites.", "Provider = integration path."),
   ("#1 build gotcha?", "Provider path/config — verify negotiation explicitly.", "Config, not compile.")
  ]),
  drill("il30-m12-drill2", [
   ("Capture targets?", "Group, sizes, cert algs, transcript bytes, timing.", "Evidence for M09."),
   ("Benchmark axes?", "Algs × ops, ops/sec + ms/op, versions recorded.", "Disciplined numbers."),
   ("What doesn't transfer to prod?", "Lab PKI trust, lab keys, VM perf, non-validated security.", "Mechanics ≠ production.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m12-lab",
  "Full integration lab: build liboqs, exercise its API directly, stand up OQS-OpenSSL (or OpenSSL 3.5+) with X25519MLKEM768, capture real hybrid handshakes, benchmark the algorithm suite, and produce the evidence pack M09's playbook consumes.",
  [
   "Build liboqs from source (pinned version); run kat_kem / kat_sig for ML-KEM-768 and ML-DSA-65; record pass/fail.",
   "Write a C or Python(ctypes) program driving OQS_KEM ML-KEM-768: keypair → encaps → decaps → shared-secret match; time 1000 iterations.",
   "Set up oqs-provider (or native 3.5+): configure provider + X25519MLKEM768 group; generate test CA/server cert (ML-DSA or classical for this lab).",
   "Perform the handshake (s_server/s_client); capture with tshark; extract: negotiated group, ClientHello bytes, KeyShare bytes, cert sizes.",
   "Benchmark: full suite (ML-KEM ×3, ML-DSA ×3, SLH-DSA 128s/128f) — ops/sec and ms/op table with versions.",
   "Write the evidence pack: versions, KAT results, capture analysis, benchmark table, and the lab-to-production gap statement."
  ],
  "Evidence pack: build log with versions, KAT output, API timing program + results, handshake captures with size analysis, benchmark table, gap statement.",
  "KATs pass; API round-trip matches; handshake negotiates X25519MLKEM768 with captured proof; benchmark table complete with versions; gap statement written."
 ),
 "mockTask": mock(
  "A vendor demo shows a 'PQC handshake' but won't share captures, versions, or which group was negotiated. Your evaluation?",
  ["Accept the demo", "Reject as evidence: require the capture (negotiated group proof), exact software versions, and KAT/benchmark methodology — a PQC claim without artifacts is marketing. Offer the lab's evidence-pack template as the acceptance bar.", "Ask for a discount", "Test it yourself silently"],
  1,
  "The lab exists to make you artifact-driven: no capture, no versions, no claim. Set the acceptance bar at evidence, every time."),
 "videos": [
  video("Open Quantum Safe — project and integrations", OQSORG, "Open Quantum Safe", "liboqs, oqs-provider, OQS-OpenSSL/SSH: the full integration surface.", 20, 1),
  video("oqs-provider — PQC for OpenSSL 3", OQSPROV, "Open Quantum Safe", "Provider mechanics: config, groups, and the demo apps.", 15, 2)
 ],
 "pdfs": [
  pdf("liboqs assessment — project overview and algorithm inventory", "https://github.com/tylerdrakemusic/quantum/blob/HEAD/research/quantum-cryptography/liboqs-assessment.md", "OQS community research", "liboqs scope, supported algorithms, integration points. Retrieved 2026-10-09."),
  pdf("NIST FIPS 203 — KATs and API behavior reference", FIPS203, "NIST CSRC", "What 'correct' looks like: known-answer tests for the lab. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("Build order that works", "1) Dependencies: cmake, gcc, OpenSSL headers. 2) liboqs: clone at a PINNED tag, cmake -DOQS_BUILD_ONLY_LIB=OFF if you want the KAT tools, build, run tests (ctest) — failures here stop everything downstream. 3) KATs: ./tests/kat_kem ML-KEM-768, ./tests/kat_sig ML-DSA-65 — passing KATs are your 'the math is right' proof. 4) oqs-provider (if OpenSSL < 3.5): build against your OpenSSL, install to the modules dir, write openssl.cnf activating it. 5) Verify: openssl list -providers shows oqsprovider; openssl list -kem-algorithms | grep ML-KEM. 6) Only then: certs, server, handshake. Skipping verification at each step is how you spend a day debugging step 6 for a step-2 problem."),
  note("Reading the capture", "Filter: tls.handshake. What to extract: ClientHello → supported_groups (find the hybrid group ID), key_share → key_exchange length (expect ~1184+32 client-side for X25519MLKEM768); ServerHello → selected group + key_share (~1088+32); Certificate → signature algorithms and total chain bytes; timing: handshake duration vs classical baseline. Save the pcap with the report — 'the capture shows' beats 'I believe' in every review. Compare against your M07 size predictions: theory and measurement should agree within bytes."),
  note("Benchmarks that mean something", "Method: pinned versions, CPU model recorded, frequency scaling noted (or disabled), N≥1000 iterations, report median ms/op and ops/sec, separate keygen/encaps/decaps/sign/verify. Expect: ML-KEM ops in the 0.01-0.1 ms band; ML-DSA sign/verify similar; SLH-DSA-128f sign ~1-10 ms, 128s ~10-100 ms, verify sub-ms. Use the table to justify algorithm choices in M14's capstone: 'we chose ML-DSA-65 for the token service because signing happens 40k/s and SLH-DSA cannot' — with YOUR numbers attached. Numbers without versions and methodology are anecdotes.")
 ]
}

# =====================================================================
# M13 — Policy & compliance
# =====================================================================
M13 = {
 "id": "IL30-M13", "code": "IL-30",
 "title": "Policy & Compliance: CNSA 2.0, NSM-10, IR 8547 Timelines",
 "summary": "The mandate landscape: CNSA 2.0's category timelines and procurement gate, NSM-10's 2035 horizon, NIST IR 8547's deprecation schedule, EO 14144, and how federal mandates become your organization's dated obligations — without inventing a certification that doesn't exist.",
 "objectives": [
  "Recite the CNSA 2.0 timeline: 2025 prefer, 2027 procurement gate, 2030/2031/2033 milestones",
  "Explain NSM-10's requirements: inventory, prioritization, 2035 risk-mitigation horizon",
  "Use NIST IR 8547's deprecation schedule (RSA-2048/ECC-256 deprecated 2030, disallowed after 2035)",
  "Translate mandates into organizational obligations with owners and dates",
  "State honestly: no PQC certification exists; compliance means standards alignment"
 ],
 "estimatedMinutes": 540, "weight": 0.9,
 "prerequisiteFor": ["IL30-M14","IL30-M15"],
 "crossLinks": [
  {"course": "IL-29", "module": "IL29-M33", "note": "Security+ governance domain context"},
  {"course": "IL-11", "module": "il11-zero-trust-foundations--zt-nist-tenets", "note": "NIST framework context"}
 ],
 "cards": [
  card("What is CNSA 2.0?", "NSA's Commercial National Security Algorithm Suite 2.0 (2022): the quantum-resistant algorithm suite for National Security Systems — ML-KEM, ML-DSA, AES-256, SHA-384/512 — with a dated transition timeline. Guidance with procurement teeth."),
  card("CNSA 2.0 headline dates?", "2025: support-and-prefer for software/firmware signing, web/cloud. Jan 1, 2027: new NSS acquisitions must be CNSA 2.0-compliant (procurement gate). 2030: exclusive use for software/firmware signing + networking equipment phase-out. End of 2031: full enforcement across NSS. 2033: niche/legacy done."),
  card("What is NSM-10?", "National Security Memorandum 10 (May 2022): directs US agencies to inventory quantum-vulnerable systems, prioritize, and mitigate most quantum risk by 2035. The top-level 'why' behind federal PQC programs."),
  card("What is NIST IR 8547?", "NIST's transition-to-PQC-standards framework (initial public draft Nov 2024): deprecation schedule and migration approaches — RSA-2048 and ECC-256 deprecated by 2030, disallowed after 2035. The planning baseline."),
  card("EO 14144 (Jan 2025) PQC-relevant requirement?", "TLS 1.3 (or successor) across all federal systems by January 2, 2030 — plus PQC built into federal procurement rules."),
  card("OMB M-23-02's PQC component?", "Directed federal agencies to inventory quantum-vulnerable systems (implementing the Quantum Cybersecurity Preparedness Act's inventory mandate), prioritized by high-value assets, with annual reporting through 2035."),
  card("How do these become YOUR dates?", "Map each mandate to your asset classes: NSS-adjacent → CNSA 2.0 dates directly; federal contractors → procurement clauses flow down; everyone else → use the federal timeline as the industry-baseline plan (insurers, auditors, and customers will)."),
  card("The 2027 procurement gate, practically?", "From Jan 1, 2027, new NSS acquisitions must support CNSA 2.0 algorithms by default. For vendors: PQC support must be IN the product by then. For buyers: write it into RFPs now — 2027 products are being built today."),
  card("What does 'support and prefer by 2025' mean for software signing?", "Vendors should support CNSA 2.0 algorithms and prefer them where possible by end of 2025 — no mandatory enforcement before then, but the direction is set. Laggards get no extension on the 2030 exclusive-use date."),
  card("Compliance vs certification: the honest statement?", "No PQC certification exists. 'Compliance' today means: aligned to final FIPS, following the transition timelines, with inventory + plan + evidence. Anyone selling a 'PQC certificate' is selling something NIST doesn't issue.")
 ],
 "quiz": [
  quiz("The CNSA 2.0 date that turns guidance into procurement requirement is:",
       ["End of 2025", "January 1, 2027 — new NSS acquisitions must be CNSA 2.0-compliant by default", "2030", "2035"],
       1, "The 2027 gate is the teeth: it converts the timeline from advice into buying rules. Products shipping in 2027 are specified now."),
  quiz("NIST IR 8547 says RSA-2048 and ECC-256 will be:",
       ["Banned immediately", "Deprecated by 2030 and disallowed after 2035", "Fine indefinitely", "Replaced by RSA-4096"],
       1, "The deprecation schedule is the planning baseline: deprecated 2030 (migrate off), disallowed after 2035 (no new use). Your phase plan (M08) must clear these bars."),
  quiz("A vendor claims 'CNSA 2.0 certified' status for their product. You should:",
       ["Accept it", "Ask what they mean: CNSA 2.0 is a suite + timeline, not a certification program — require specifics (which algorithms, which validations, e.g., FIPS 140 with PQC, against which timeline milestone)", "Reject the vendor", "Report them"],
       1, "Precision matters: there is no 'CNSA 2.0 certification.' Demand the underlying facts — algorithms, validations, dates — not the label."),
  quiz("NSM-10's ultimate horizon and its mechanism?",
       ["2027, procurement", "2035: mitigate most quantum risk — via agency inventories, prioritization, and annual progress", "2030, enforcement", "No horizon"],
       1, "NSM-10 is the strategy; CNSA 2.0/IR 8547 are the tactics. 2035 is the 'most risk mitigated' horizon — your long-range plan should land there or earlier."),
  quiz("Your org isn't federal and handles no NSS data. Why track CNSA 2.0 at all?",
       ["No reason", "It sets the industry baseline: auditors, insurers, enterprise customers, and vendors all coordinate on it — and the threat (HNDL) doesn't check your sector", "It's legally required anyway", "Only for marketing"],
       1, "Mandates propagate: through supply chains, customer requirements, insurance questionnaires, and vendor roadmaps. The federal timeline is the Schelling point for everyone.")
 ],
 "drills": [
  drill("il30-m13-drill1", [
   ("CNSA 2.0: 2027 = ?", "Procurement gate: new NSS acquisitions CNSA 2.0-compliant.", "Guidance → buying rules."),
   ("2030/2031/2033?", "2030: signing + networking exclusive/phase-out. 2031: full enforcement. 2033: niche/legacy done.", "Escalating milestones."),
   ("NSM-10 horizon?", "2035: most quantum risk mitigated.", "The strategy's end date.")
  ]),
  drill("il30-m13-drill2", [
   ("IR 8547 deprecation line?", "RSA-2048/ECC-256 deprecated 2030, disallowed after 2035.", "Planning baseline."),
   ("EO 14144 TLS date?", "TLS 1.3+ across federal systems by Jan 2, 2030.", "2030 floor."),
   ("Honest compliance statement?", "Aligned to final FIPS + timelines + inventory/plan/evidence. No PQC cert exists.", "Evidence, not labels.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m13-lab",
  "You will build a mandate-to-obligation map for a fictional org: take the CNSA 2.0 / NSM-10 / IR 8547 / EO 14144 requirements, determine which apply (directly or by propagation) to each business unit, and produce dated obligations with owners. You will also draft the RFP clause requiring PQC support.",
  [
   "List the mandates with their dates and scope (table).",
   "For each of 6 fictional business units (federal-adjacent SaaS, commercial IoT, internal IT, etc.), mark applicable/propagated/not-applicable with reasoning.",
   "Write dated obligations: e.g., 'IoT firmware: vendor PQC roadmap by Q2 2027; signing migration complete 2029' — with owners.",
   "Draft the RFP clause: PQC algorithm support, CBOM disclosure, dated commitments, tied to the 2027 gate.",
   "Write the 'no such certification' paragraph for leadership: what compliance evidence looks like without a cert."
  ],
  "mandate-map.md + rfp-clause.md: the applicability table, dated obligations with owners, the RFP clause, and the compliance-evidence paragraph.",
  "Every obligation has a date and an owner; the RFP clause names algorithms, CBOM, and dates; the compliance paragraph is honest about no-certification."
 ),
 "mockTask": mock(
  "Leadership asks: 'Which PQC certification should our team get to prove compliance?' Your answer?",
  ["Recommend a vendor's 'PQC certified' course", "Honest answer: none exists — NIST issues standards, not certifications. Proof of compliance = alignment evidence: CBOM currency, FIPS-aligned deployments, milestone completion against the CNSA 2.0/IR 8547 timelines, validated implementations. Propose building that evidence pack instead of buying a badge.", "Recommend Security+", "Say compliance is impossible"],
  1,
  "The module's core honesty point: in a field with no certification, evidence replaces badges. Selling a badge-shaped solution would be malpractice."),
 "videos": [
  video("CNSA 2.0 timeline and V2.1 FAQ enforcement mechanics", "https://postquantum.com/security-pqc/nsa-cnsa-2-0-faq-v2-1-update/", "postquantum.com", "Procurement gate, phase-outs, category timelines — the enforcement teeth.", 20, 1),
  video("PQC timelines 2026–2035: mandates mapped", TQI, "The Quantum Insider", "NSM-10, CNSA 2.0, IR 8547, EU framework on one timeline.", 25, 2)
 ],
 "pdfs": [
  pdf("Federal PQC mandates and phased timeline", AXEL, "AxelSpire", "NSM-10, OMB M-23-02, EO 14144, QCPA mapped to 2025/2027/2030/2035 milestones. Retrieved 2026-10-09."),
  pdf("NCCoE migration practice guide", NCCOE, "NIST NCCoE", "Practice companion to the mandates. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("The mandate stack, bottom to top", "NSM-10 (May 2022): strategy — inventory, prioritize, mitigate most risk by 2035. Quantum Cybersecurity Preparedness Act (Dec 2022): law — OMB guidance, agency inventories of quantum-vulnerable systems. OMB M-23-02: implementation — inventory requirements, high-value-asset prioritization, annual reporting. CNSA 2.0 (2022, V2.1 FAQ): the technical suite + dated timeline for NSS — 2025 prefer, 2027 procurement gate, 2030/2031/2033 milestones. NIST IR 8547 (draft 2024): transition framework — deprecation schedule (RSA-2048/ECC-256 deprecated 2030, disallowed after 2035). EO 14144 (Jan 2025): TLS 1.3 by Jan 2030 + PQC in procurement. Read them as a stack: strategy → law → implementation → technical timeline → transition schedule → procurement enforcement. Your mandate map (lab) hangs obligations on each layer."),
  note("Propagation: how federal dates become your dates", "Direct: you sell to NSS/federal → the dates are contractual. Flow-down: you're a subcontractor → primes flow the clauses to you. Market: your enterprise customers' questionnaires (and cyber-insurance applications) increasingly ask for PQC plans referencing these timelines. Vendor: your suppliers' roadmaps are built around the 2027 gate — their dates become your dependency dates. Even with zero federal touch, the rational plan mirrors the federal timeline: it's the industry's coordination point, the auditors' reference, and — via HNDL — the threat doesn't care about your sector. 'Not applicable' is a conclusion you document with reasoning, not a default."),
  note("Evidence in place of certification", "With no PQC certification in existence, compliance evidence is: (1) current CBOM with algorithm inventory and trend lines; (2) deployment records showing FIPS-final algorithms (203/204/205) with validated implementations; (3) milestone completion against the mapped timelines, signed by owners; (4) vendor PQC roadmaps and contract clauses; (5) test artifacts (interop matrices, KAT results, canary telemetry). Package it as the quarterly quantum-readiness report — one page for leadership (milestones, risks, dates), appendices for auditors. When a certification eventually exists, this evidence pack becomes the application. Until then, it IS the compliance posture.")
 ]
}

# =====================================================================
# M14 — Capstone
# =====================================================================
M14 = {
 "id": "IL30-M14", "code": "IL-30",
 "title": "Capstone: Enterprise Quantum-Readiness Migration Plan",
 "summary": "The full program assembled: for a fictional 8,000-person company you will produce the complete quantum-readiness migration plan — inventory, Mosca prioritization, algorithm allocations, protocol playbooks, vendor strategy, timeline to 2035, budget narrative, and the board-level one-pager.",
 "objectives": [
  "Synthesize every module into one coherent migration program",
  "Allocate ML-KEM/ML-DSA/SLH-DSA across a real architecture with reasons",
  "Write protocol playbooks sequenced without resource collisions",
  "Produce the board one-pager: risk, dates, costs, asks",
  "Defend the plan against adversarial review (red-team questions)"
 ],
 "estimatedMinutes": 780, "weight": 1.2,
 "prerequisiteFor": ["IL30-M15"],
 "crossLinks": [
  {"course": "IL-29", "module": "IL29-M33", "note": "cert-track governance context"},
  {"course": "IL-11", "module": "il11-zero-trust-foundations--zt-nist-tenets", "note": "framework context"}
 ],
 "cards": [
  card("Capstone inputs?", "M00 math, M01 threat model, M02 standards, M03-M06 algorithms, M07 hybrids, M08 planning, M09/M10 playbooks, M11/M12 lab evidence, M13 mandates. The capstone is the integration exam."),
  card("Algorithm allocation example?", "TLS KEX: X25519MLKEM768 hybrid → pure ML-KEM-768 (2032). Web PKI: ML-DSA-65 chains. Firmware signing: SLH-DSA-192s (rare signing, tiny verifiers, 15y trust). Bootloader (size-bound): FN-DSA at FIPS-206-final, ML-DSA interim. Tokens: ML-DSA-65 (high frequency)."),
  card("What makes an allocation defensible?", "Each choice cites: the decision framework (M05/M10), measured numbers (M12), mandate dates (M13), and the fallback if the algorithm's status changes (crypto-agility, M08). No vibes."),
  card("Sequencing rule?", "TLS 1.3 → hybrid KEX → SSH → VPN → certs → code signing, with the HNDL/high-value assets first and no two fleet-wide changes colliding in one quarter. The Gantt chart is a deliverable."),
  card("Board one-pager contents?", "Risk in one paragraph (HNDL + Mosca), the dated milestones, the budget (ranges, honest), the asks (headcount, vendor escalations, decisions needed), and what happens if deferred. One page — the appendix holds the rest."),
  card("Red-team questions to survive?", "'What if ML-KEM breaks in 2028?' (hybrids + agility + HQC watch). 'Vendor X misses 2027?' (escalation triggers, overlay options). 'Budget cut 40%?' (priority order is the cut order — top decile is untouchable)."),
  card("Budget narrative honesty?", "Ranges, not false precision: discovery tooling, HSM upgrades, vendor uplifts, engineering time, audit. State what's excluded. A fake-precise budget is a lie that compounds."),
  card("What does 'done' mean in 2035?", "CBOM shows zero quantum-vulnerable-only crypto on in-scope assets; classical retired per IR 8547; pure-PQC where policy requires; crypto-agility demonstrated by at least one algorithm rotation exercise."),
  card("The rotation exercise: why?", "Crypto-agility must be PROVEN, not claimed: rotate one algorithm (or parameter set) fleet-wide in the lab/ staging and document it. The next SIKE/HAWK event is when, not if."),
  card("Handoff: who owns this after the course?", "Named roles: crypto inventory owner, PKI owner, vendor-management owner, timeline owner. A plan without owners is a document; with owners it's a program.")
 ],
 "quiz": [
  quiz("The capstone's algorithm allocation must be defensible. 'Defensible' means:",
       ["It uses the newest algorithms", "Each choice cites the decision framework, measured lab numbers, mandate dates, and a fallback plan — a reviewer can trace every decision to evidence", "It's the cheapest", "It matches what competitors do"],
       1, "Traceability is the grading criterion: framework → numbers → dates → fallback. Untraceable choices fail review no matter how fashionable."),
  quiz("Red-team: 'ML-KEM suffers a major cryptanalytic break in 2028.' Your plan's answer?",
       ["Panic", "Hybrids carry the sessions (X25519 still stands), crypto-agility enables the rotation, HQC is the tracked backup KEM, and the plan's trigger list already named this event — execute the contingency, don't improvise it", "Deny it happened", "Wait for NIST"],
       1, "This is why the plan has hybrids, agility, a pipeline watch, and pre-written triggers: the break is a scenario you rehearsed, not a surprise you improvise."),
  quiz("Two fleet-wide changes are scheduled for the same quarter (VPN migration + cert rotation). Problem?",
       ["No problem — efficiency", "Resource collision: change windows, rollback capacity, and incident response bandwidth are finite — sequence them, don't stack them. The Gantt chart must show no overlapping fleet-wide changes.", "It saves money", "Certs are easy"],
       1, "Operational reality: every fleet-wide change consumes the same on-call, rollback, and comms capacity. Stacking them is how migrations cause the outages they were meant to prevent."),
  quiz("The board asks 'what if we defer two years?' The honest answer includes:",
       ["Nothing changes", "The Mosca math for your top assets (which are already past x+y>z), the HNDL accumulation (two more years of collectible traffic), vendor-date slippage risk, and the compressed timeline's cost premium — quantified, not hand-waved", "It's fine", "Quantum computers won't exist"],
       1, "Deferral has a price: compute it. HNDL stockpiles, deadlines don't move, and compressed migrations cost more. The board decides; you quantify."),
  quiz("Why does the capstone require a named owner per workstream?",
       ["Bureaucracy", "Plans without owners don't execute: inventory, PKI, vendors, and timeline each need a human accountable for the dates — otherwise the plan is a document, not a program", "For the org chart", "Auditors like names"],
       1, "Accountability is the difference between a plan and a program. Every date in the Gantt needs a name next to it.")
 ],
 "drills": [
  drill("il30-m14-drill1", [
   ("Allocation example: firmware signing?", "SLH-DSA-192s: rare signing, tiny verifiers, 15-year trust.", "Economics + lifetime."),
   ("Allocation: high-frequency tokens?", "ML-DSA-65: microseconds, moderate size.", "Frequency decides."),
   ("Sequencing order?", "TLS 1.3 → hybrid KEX → SSH → VPN → certs → code signing.", "Platform, traffic, identity.")
  ]),
  drill("il30-m14-drill2", [
   ("Board one-pager: 5 elements?", "Risk, milestones, budget, asks, cost-of-deferral.", "One page, five answers."),
   ("Red-team ML-KEM break: response?", "Hybrids hold, agility rotates, HQC tracked, triggers fire.", "Rehearsed, not improvised."),
   ("2035 'done' definition?", "Zero vulnerable-only crypto in scope; classical retired; agility proven by rotation exercise.", "Measurable end state.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m14-lab",
  "Write the complete quantum-readiness migration plan for the fictional company (brief provided: 8,000 staff, SaaS + IoT fleet, federal-adjacent contracts): inventory approach, Mosca prioritization, algorithm allocation with justifications, sequenced protocol playbooks, vendor strategy, Gantt to 2035, budget narrative, board one-pager, and red-team Q&A. This is the course's comprehensive artifact.",
  [
   "Draft the asset inventory approach and a sample CBOM for 15 representative assets.",
   "Score and prioritize with Mosca + exposure × lifetime × blast radius; produce the queue.",
   "Allocate algorithms per asset class with cited justifications (framework + lab numbers + dates + fallback).",
   "Sequence the playbooks into a Gantt to 2035 with no resource collisions and named owners.",
   "Write the vendor strategy: roadmaps required, escalation triggers, 2027-gate clauses.",
   "Write the budget narrative (ranges, exclusions) and the board one-pager.",
   "Red-team your own plan with 10 adversarial questions; answer each in writing."
  ],
  "quantum-readiness-plan/: the full plan — inventory, prioritization, allocations, Gantt, vendor strategy, budget, board one-pager, red-team Q&A.",
  "Every allocation is traceable to evidence; the Gantt has owners and no collisions; the one-pager fits one page; all 10 red-team questions are answered honestly."
 ),
 "mockTask": mock(
  "Your plan is done. The CTO's first question: 'Convince me in 60 seconds.' Your answer?",
  ["Read the whole plan aloud", "'Adversaries are recording our encrypted traffic today (HNDL). Our longest-lived secrets expire after any plausible quantum timeline (Mosca). The plan migrates the top-risk assets to hybrid PQC in 18 months for [budget range], hits every federal date that touches our contracts, and the alternative — deferral — costs [deferral math] while the recorded traffic keeps accumulating. The one-pager has the dates; I need your decision on [the asks].'", "Say 'trust me'", "Show the math module"],
  1,
  "Sixty seconds: threat, math, plan, cost, ask. Everything else is appendix. Executives decide on the one-pager; the plan exists so the one-pager is true."),
 "videos": [
  video("NCCoE migration practice guide — putting it together", NCCOE, "NIST NCCoE", "The practice framework your capstone instantiates.", 40, 1),
  video("PQC timelines 2026–2035", TQI, "The Quantum Insider", "The deadline landscape the Gantt must satisfy.", 25, 2)
 ],
 "pdfs": [
  pdf("NIST PQC project — standards reference", PQCPROJ, "NIST CSRC", "The source of truth for allocations. Retrieved 2026-10-09."),
  pdf("CycloneDX CBOM — inventory format", CBOM, "CycloneDX", "The inventory artifact format. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("How the plan is graded", "Five criteria: (1) Traceability — every algorithm and date traces to a framework, a number, or a mandate. (2) Sequencing — no resource collisions, HNDL-first ordering, realistic phase durations. (3) Honesty — budget ranges not false precision, risks named, deferral cost computed. (4) Operability — owners on every workstream, rollback plans, telemetry-defined triggers. (5) Red-team survival — the 10 adversarial questions answered without hand-waving. A plan that is technically brilliant but unowned fails; a plan that is modest but executable passes. Grade yourself the way an auditor will: evidence, dates, names."),
  note("The fictional company brief", "Meridian Field Systems: 8,000 staff, SaaS platform (TLS-heavy, enterprise customers asking PQC questions), IoT fleet of 200k devices (firmware signed quarterly, 15-year device life, constrained bootloaders), federal-adjacent contracts (CNSA 2.0 dates apply by flow-down), on-prem PKI with an aging root CA, 40-person platform team, no crypto inventory. Your plan must handle: the SaaS HNDL exposure, the IoT signing economics (this is where SLH-DSA/FN-DSA earn their keep), the root CA rotation, and the vendor firmware long pole — all inside one Gantt, one budget, one page for the board."),
  note("After the capstone: keeping it alive", "The plan is a living program: quarterly CBOM re-scans, milestone reviews against the Gantt, pipeline-watch updates (FIPS 206 final? HQC draft?), annual Mosca re-computation with fresh z estimates, and the crypto-agility rotation exercise. Assign the 'quantum-readiness owner' as a standing role, not a project — the threat evolves (new algorithms, new breaks, new mandates) and the program must evolve with it. Noah (see noahTutoring) continues as the currency layer: as standards move past the 2026-10-09 baseline, the tutoring layer surfaces what changed and what it means for YOUR plan.")
 ]
}

# =====================================================================
# M15 — Readiness gate
# =====================================================================
M15 = {
 "id": "IL30-M15", "code": "IL-30",
 "title": "Standards-Alignment Readiness Gate",
 "summary": "The exit gate: prove standards literacy (FIPS 203/204/205 cold), defend algorithm choices, demonstrate lab evidence, and state the honesty boundaries — no certificate is conferred; readiness means you can operate the migration, not that you hold a credential.",
 "objectives": [
  "Recite FIPS 203/204/205 parameter sets, sizes, and roles from memory",
  "Defend three algorithm allocations against adversarial questioning",
  "Present lab evidence: captures, benchmarks, KATs",
  "State the honesty boundaries: what you know, what's draft, what's unknown",
  "Produce the personal quantum-readiness action list for your own org"
 ],
 "estimatedMinutes": 420, "weight": 0.8,
 "prerequisiteFor": [],
 "crossLinks": [
  {"course": "IL-29", "module": "IL29-M33", "note": "cert-gate pattern reference"},
  {"course": "IL-23", "module": "m23-quantum", "note": "quantum basics"}
 ],
 "cards": [
  card("Gate rule?", "Clear every check twice, on different days — same discipline as the cert gates. Readiness is demonstrated, not claimed."),
  card("FIPS 203 cold: parameter sets + sizes?", "ML-KEM-512/768/1024; pk 800/1184/1568 B; ct 768/1088/1568 B; levels 1/3/5; default 768."),
  card("FIPS 204 cold?", "ML-DSA-44/65/87; sig 2420/3309/4627 B; pk 1312/1952/2592 B; levels 2/3/5; default 65."),
  card("FIPS 205 cold?", "SLH-DSA: 12 sets (SHA2/SHAKE × 128/192/256 × s/f); pk 32/48/64 B; sig 7.8–49 KB; hash-only assumptions."),
  card("Pipeline status cold?", "FN-DSA: FIPS 206 draft (IPD Aug 2025), final expected late 2026/early 2027. HQC: selected Mar 2025, draft in progress. Additional signatures: round 2, track only."),
  card("Mandate dates cold?", "CNSA 2.0: 2027 procurement gate, 2030 signing/networking exclusive, 2031 full enforcement, 2033 niche done. IR 8547: RSA-2048/ECC-256 deprecated 2030, disallowed after 2035. EO 14144: TLS 1.3 by Jan 2030. NSM-10: 2035 horizon."),
  card("The honesty statement you must be able to give?", "'I am aligned to FIPS 203/204/205 as published [date]; FN-DSA and HQC are not final and I track them; no PQC certification exists and I claim none; my recommendations cite evidence, and where evidence ends I say so.'"),
  card("Lab evidence required?", "Handshake capture with hybrid group proof, benchmark table with versions, KAT passes, toy-attack margin writeup — artifacts, not assertions."),
  card("What does passing confer?", "Readiness to operate a migration program — not a certificate, not a credential, not an affiliation. Say exactly that."),
  card("Personal action list?", "Three dated actions for YOUR org: e.g., 'run TLS discovery scan by [date]', 'get vendor PQC roadmaps by [date]', 'draft CBOM by [date]'. The course ends when your org's program starts.")
 ],
 "quiz": [
  quiz("ML-KEM-768 public key size?",
       ["800 B", "1184 B", "1568 B", "256 B"],
       1, "1184 bytes. Cold recall — no notes at the gate."),
  quiz("SLH-DSA-128s signature size, approximately?",
       ["64 B", "~7.8 KB", "3309 B", "256 B"],
       1, "~7,856 bytes. The 's' (small) variant at the 128-bit level."),
  quiz("CNSA 2.0 procurement gate date?",
       ["Jan 1, 2027", "2030", "2025", "2035"],
       0, "January 1, 2027: new NSS acquisitions CNSA 2.0-compliant by default."),
  quiz("A colleague says they are 'PQC certified' after this course. Correction?",
       ["Congratulate them", "No PQC certification exists; the course confers readiness to operate a migration, aligned to published FIPS — claiming a credential would be dishonest and this course teaches you to say so", "Ask which vendor", "It's fine informally"],
       1, "The honesty boundary is itself a gate item: misrepresenting credentials destroys the trust the whole program runs on."),
  quiz("FIPS 206 status as of the course baseline (2026-10-09)?",
       ["Final", "Draft — IPD submitted August 2025, final expected late 2026/early 2027", "Abandoned", "Not started"],
       1, "Draft, tracked, not built on. The baseline date matters: re-verify before citing.")
 ],
 "drills": [
  drill("il30-m15-drill1", [
   ("FIPS 203 sizes cold?", "pk 800/1184/1568; ct 768/1088/1568.", "512/768/1024."),
   ("FIPS 204 sizes cold?", "sig 2420/3309/4627; pk 1312/1952/2592.", "44/65/87."),
   ("FIPS 205 shape cold?", "12 sets; pk 32-64 B; sig 7.8-49 KB.", "Hash-only backup.")
  ]),
  drill("il30-m15-drill2", [
   ("Gate rule?", "Clear every check twice, different days.", "Demonstrated, not claimed."),
   ("Passing confers?", "Readiness to operate — no certificate, no credential.", "Honesty boundary."),
   ("Course ends when?", "Your org's program starts: three dated personal actions.", "Action, not just knowledge.")
  ])
 ],
 "handsOnLab": lab(
  "il30-m15-lab",
  "The gate itself: (1) closed-book standards recitation (parameter sets, sizes, dates) recorded twice on different days; (2) adversarial defense of three capstone allocations (15 min each, recorded or written); (3) lab evidence pack review against the checklist; (4) the honesty statement written and spoken; (5) your personal three-action list with dates.",
  [
   "Closed-book: write FIPS 203/204/205 sets+sizes+roles and the mandate dates from memory. Repeat on a second day.",
   "Defend three allocations from your capstone against the red-team questions — in writing, with evidence citations.",
   "Assemble the evidence pack: capture, benchmarks, KATs, toy-attack margin — check each against the rubric.",
   "Write and speak the honesty statement (card 7) — word-perfect on the boundaries.",
   "Write your three dated personal actions; schedule the first."
  ],
  "gate-dossier/: recitation sheets (×2 days), defense writeups, evidence pack, honesty statement, personal action list.",
  "Both recitations pass; defenses cite evidence; evidence pack complete; honesty statement exact; actions dated and the first scheduled."
 ),
 "mockTask": mock(
  "Final gate scenario: a hiring manager asks 'Are you PQC certified?' after seeing IL-30 on your resume. The answer that passes the gate?",
  ["'Yes, IL-30 certified me.'", "'No — and be wary of anyone who says yes: no PQC certification exists. IL-30 made me standards-literate on FIPS 203/204/205, able to run the migration playbooks, and honest about the boundaries — here's my capstone plan and lab evidence.'", "'Sort of.'", "Deflect"],
  1,
  "The gate's deepest check: honesty under incentive pressure. The correct answer converts the question into evidence — and flags credential fraud as the disqualifier it is."),
 "videos": [
  video("NIST PQC project — verify the current baseline", PQCPROJ, "NIST CSRC", "Re-verify every baseline fact before you cite it elsewhere. Standards move; your citations must carry dates.", 20, 1)
 ],
 "pdfs": [
  pdf("PQC standards tracker — re-verify before citing", KFCIPHER, "KFCipher", "The re-verification habit, as a bookmark. Retrieved 2026-10-09."),
  pdf("NIST FIPS 203/204/205 publication pages", FIPS203, "NIST CSRC", "The primary sources. Retrieved 2026-10-09.")
 ],
 "notes": [
  note("The gate rubric", "Five checks, each cleared twice on different days: (1) Cold recitation: FIPS 203/204/205 parameter sets, sizes, roles; pipeline statuses; mandate dates. Bar: 90%+ accuracy, no notes. (2) Allocation defense: three capstone choices defended against adversarial questions with evidence citations. Bar: every claim traces to framework/numbers/dates. (3) Evidence pack: capture, benchmarks with versions, KATs, toy-attack margin. Bar: artifacts complete and honest about gaps. (4) Honesty statement: word-perfect on no-certification, draft-status, and baseline-date boundaries. Bar: exact. (5) Personal actions: three dated, first scheduled. Bar: dates in the calendar. Two consecutive clears per check — the same discipline as every cert gate on this platform."),
  note("What 'ready' means here", "Ready = you can walk into an org with no PQC program and stand up the discovery → prioritization → pilot → rollout sequence without inventing facts, without freelancing crypto, and without misrepresenting credentials. It does NOT mean: certified (no such thing), a cryptographer (you operate standards; you don't design schemes), or finished (FIPS 206/HQC/the second signature round will move the baseline — the pipeline-watch habit from M06/M13 is part of readiness). The most important gate item is the honesty statement: in a field this new, the person who says 'I don't know, here's how I'd find out' is the one you want running the program."),
  note("Keeping current after the gate", "Baseline: 2026-10-09. Re-verify quarterly: FIPS 206 status, HQC draft, IR 8547 updates, CNSA 2.0 revisions. Triggers that change your plan: any FIPS finalization, any deprecation-date change, any major cryptanalytic result against a deployed algorithm. Noah (noahTutoring) is the course's currency layer — it tracks these publications against your baseline and briefs you on what changed and what it means for your plan. The gate dossier gets a dated addendum each quarter; a readiness claim without a current date is stale.")
 ]
}

# =====================================================================
# Noah AI integration — per-module tutor wiring + top-level section
# =====================================================================
NOAH_TUTOR = {
 "IL30-M00": ("mathematician", "Before we touch code: state the LWE equation from memory, then tell me — in your own words — why the error term is load-bearing. I'll push back Socratically until the hardness story is airtight."),
 "IL30-M01": ("philosopher", "A CISO tells you 'we'll migrate when the quantum computer is announced.' Using HNDL and Mosca's inequality, dismantle that position — I'll play the skeptical executive and make you earn every claim."),
 "IL30-M02": ("philosopher", "SIKE died in public before standardization. Was that a failure of post-quantum cryptography or its finest hour? Defend your answer — then we'll extract the general rule for trusting standards processes."),
 "IL30-M03": ("mathematician", "Walk me through ML-KEM decapsulation step by step: where exactly does the Fujisaki–Okamoto re-encryption check happen, and what attack becomes possible if you remove it? I'll probe each step."),
 "IL30-M04": ("mathematician", "Explain Fiat–Shamir with aborts as if I'm a smart engineer who distrusts magic: why does the signer retry, what does 'independent of the secret' mean operationally, and where would a timing leak hide?"),
 "IL30-M05": ("mathematician", "You have to choose between ML-DSA-65 and SLH-DSA-128s for a firmware signing pipeline. Argue both sides — I'll challenge your assumptions about signing frequency, verifier constraints, and trust lifetime."),
 "IL30-M06": ("mathematician", "FIPS 206 mandates fixed-point arithmetic and bans floating point. Explain to me why a standards body cares about floating-point determinism — then tell me what you'd do about a vendor shipping the IPD in production."),
 "IL30-M07": ("operator", "Design the hybrid handshake rollout for one production service: group selection, KDF combiner, downgrade-safety argument, and the canary metrics. I'll red-team your design for silent-downgrade holes."),
 "IL30-M08": ("philosopher", "You have 5,000 systems, no inventory, and leadership wants '100% PQC by year-end.' Build the honest counter-proposal with me — discovery, scoring, phases — and rehearse delivering it to an impatient executive."),
 "IL30-M09": ("operator", "Walk the TLS runbook: your canary shows 2% handshake failures on a legacy proxy fleet after enabling X25519MLKEM768. Talk me through the diagnosis, the surgical rollback, and the vendor conversation — step by step."),
 "IL30-M10": ("operator", "The release team wants to 'just switch' code signing to ML-DSA next sprint for a 50k-device fleet with no verifier telemetry. Stop them — construct the verifier-first sequencing argument and the dual-signing plan."),
 "IL30-M11": ("engineer", "Your toy KEM decrypts correctly 97% of the time. Is that good or broken? Let's trace the noise budget together until you can predict the failure rate from the parameters — then we'll push past the cliff on purpose."),
 "IL30-M12": ("engineer", "The handshake negotiates X25519 instead of the hybrid group. Debug with me: provider loaded? config read? group offered? I'll make you check each layer and prove the fix with a fresh capture."),
 "IL30-M13": ("philosopher", "Leadership asks which PQC certification the team should get. There's no such thing — so what IS the compliance evidence? Let's build the honest answer and the quarterly readiness report outline together."),
 "IL30-M14": ("examiner", "Defend your capstone: pick your hardest allocation decision and I'll attack it — the framework, the numbers, the fallback. If your reasoning survives me, it survives the architecture review."),
 "IL30-M15": ("examiner", "Gate time. Closed-book: FIPS 203/204/205 sizes, pipeline statuses, mandate dates. I'll drill you twice — and then I'll ask the hardest question: what do you do when you don't know?"),
}

NOAH_VOICES = {
 "mathematician": "noah-voice-mathematician",
 "engineer": "noah-voice-engineer",
 "philosopher": "noah-voice-philosopher",
 "operator": "noah-voice-operator",
 "examiner": "noah-voice-examiner",
}

MODULES = [M00, M01, M02, M03, M04, M05, M06, M07, M08, M09, M10, M11, M12, M13, M14, M15]
for m in MODULES:
    persona, prompt = NOAH_TUTOR[m["id"]]
    m["noahTutor"] = {
        "persona": persona,
        "voice": NOAH_VOICES[persona],
        "starterPrompt": prompt,
        "mode": "Socratic tutoring grounded in this module's content — questions before answers, hypothesis-driven",
    }

NOAH_TUTORING = {
 "concept": "Noah AI is the core learning-experience driver for IL-30 — not a bolt-on. Every module opens with a Noah-guided Socratic session, every lab has Noah as a debugging partner, and every gate is rehearsed against Noah's Examiner before the real attempt.",
 "vision": "Built to our vision — Noah-driven personalized tutoring over bleeding-edge content — not modeled on competitors. The tutor adapts to the learner; the content stays at the standards frontier.",
 "personas": [
  {"id": "mathematician", "name": "The Mathematician", "voice": "noah-voice-mathematician",
   "role": "Proofs, hardness arguments, and algorithm internals",
   "style": "Precise, Socratic, allergic to hand-waving. Demands definitions before conclusions.",
   "modules": ["IL30-M00", "IL30-M03", "IL30-M04", "IL30-M05", "IL30-M06"]},
  {"id": "engineer", "name": "The Engineer", "voice": "noah-voice-engineer",
   "role": "Labs, debugging, measurement, and build discipline",
   "style": "Direct, terminal-flavored. Pairs on code, insists on captures and versions, never accepts 'it works' without evidence.",
   "modules": ["IL30-M00", "IL30-M11", "IL30-M12"]},
  {"id": "philosopher", "name": "The Philosopher", "voice": "noah-voice-philosopher",
   "role": "Strategy, threat modeling, policy, and first-principles reasoning",
   "style": "Plays the skeptical executive. Forces the 'why now, why this, what if wrong' discipline behind every migration decision.",
   "modules": ["IL30-M01", "IL30-M02", "IL30-M08", "IL30-M13"]},
  {"id": "operator", "name": "The Operator", "voice": "noah-voice-operator",
   "role": "Runbooks, playbooks, incidents, and rollout sequencing",
   "style": "Checklist-driven, rollback-aware. Red-teams every plan for silent-downgrade holes and resource collisions.",
   "modules": ["IL30-M07", "IL30-M09", "IL30-M10"]},
  {"id": "examiner", "name": "The Examiner", "voice": "noah-voice-examiner",
   "role": "Drills, readiness gates, and adversarial defense",
   "style": "Closed-book, twice-on-different-days. Attacks allocations until only evidence remains.",
   "modules": ["IL30-M14", "IL30-M15"]}
 ],
 "voices": {
  "count": 5,
  "description": "Five natural voices, one per persona, selectable by the learner. Voice follows persona: switch to the Engineer and the voice shifts with the role — the tutoring feels like a team, not a chatbot.",
  "mapping": "1:1 persona-to-voice; learner can pin a preferred voice across personas."
 },
 "adaptiveLearning": {
  "method": "SM-2 spaced repetition",
  "description": "Every flashcard, quiz miss, and drill item feeds an SM-2 scheduler per learner: intervals grow on recall, collapse on misses. Noah resurfaces the FIPS constants (key sizes, dates, parameter sets) exactly when forgetting curves predict decay — cold recall at the gate is trained, not hoped for.",
  "signals": ["quiz scores", "drill misses", "card review latency", "lab checkpoint outcomes"]
 },
 "courseAwareTutoring": {
  "description": "Noah tutors FROM this course's content: module notes, cards, labs, and the capstone are its grounding corpus. It answers with citations to module sections, refuses to freelance cryptography beyond the standards, and escalates to primary sources (the FIPS PDFs) when the learner's question exceeds the course baseline.",
  "rules": [
   "Questions before answers — the learner states a hypothesis first",
   "Every factual claim traceable to a module note or a linked primary source",
   "Never invents parameters, dates, or statuses — says 'I don't know, here's how we'd verify' instead",
   "Lab debugging pairs on the learner's code and captures, never rewrites the lab for them"
  ]
 },
 "currencyMechanism": {
  "baseline": "2026-10-09",
  "description": "PQC is bleeding-edge by definition: standards move after the course ships. Noah tracks the live pipeline against the course baseline and briefs the learner on deltas.",
  "tracked": [
   "FIPS 206 (FN-DSA): draft → final",
   "HQC: selection → draft → final",
   "NIST IR 8547: draft → final, deprecation-date changes",
   "CNSA 2.0: revisions and V2.x FAQ updates",
   "Additional-signature round: candidate status changes and withdrawals",
   "Major cryptanalytic results against deployed algorithms"
  ],
  "behavior": "When a tracked item changes status, Noah surfaces a dated delta brief: what changed, which modules it touches, and whether the learner's capstone plan needs revision. Baseline facts in the course always carry their as-of date; Noah never silently rewrites them."
 },
 "tutorModes": [
  {"mode": "socratic-session", "description": "Module-opening dialogue from the per-module starter prompt — hypothesis-driven, questions first."},
  {"mode": "lab-pair", "description": "Engineer persona pairs on labs: debugging, measurement review, evidence-pack critique."},
  {"mode": "red-team", "description": "Operator/Examiner attack the learner's designs and allocations until only evidence remains."},
  {"mode": "gate-rehearsal", "description": "Examiner runs the readiness gate twice on different days before the real attempt."},
  {"mode": "delta-brief", "description": "Currency mechanism: dated briefs when tracked standards move past the baseline."}
 ],
 "integrationRules": [
  "Noah is the default first step of every module — the starter prompt opens the module, not an afterthought link.",
  "Persona follows the module's cognitive demand (see mapping); the learner may override.",
  "SM-2 scheduling is per-learner and persistent across sessions.",
  "Noah never replaces the labs: it tutors the thinking, the learner does the building.",
  "All Noah factual claims about standards carry the 2026-10-09 baseline date or a newer verified delta."
 ]
}

# =====================================================================
# Top-level assembly
# =====================================================================
TOTAL_MIN = sum(m["estimatedMinutes"] for m in MODULES)
HOURS = round(TOTAL_MIN / 60)

OBJECTIVES = [
 "Explain precisely which classical primitives fall to which quantum algorithm: Shor breaks RSA/DH/ECDSA/ECDH, Grover halves symmetric key strength, and why harvest-now-decrypt-later forces action before any quantum computer exists.",
 "Work the lattice mathematics behind Module-LWE/Module-SIS: lattices, shortest/closest vector problems, modular arithmetic, and error distributions — far enough to read the algorithm specs.",
 "Trace the NIST PQC competition from the 2016 call to the August 2024 finals and know exactly where every algorithm stands: final (FIPS 203/204/205), in standardization (HQC, FN-DSA), or still under evaluation.",
 "Deploy ML-KEM (Kyber) correctly: parameter sets ML-KEM-512/768/1024, key/ciphertext sizes, the encapsulation protocol, and why misusing an ephemeral keypair breaks its security story.",
 "Deploy ML-DSA (Dilithium) and SLH-DSA (SPHINCS+): parameter sets, signature sizes, Fiat–Shamir with aborts, hypertree-plus-FORS construction, and the size/performance tradeoffs that decide which signature to use where.",
 "Design hybrid key exchange (X25519 + ML-KEM in TLS 1.3) and state the hybrid security property: the exchange is safe if EITHER component holds.",
 "Build a crypto inventory and migration plan: discovery methods, CBOM practice, prioritization by exposure and data lifetime, and hybrid-first deployment strategy.",
 "Execute protocol migration playbooks for TLS 1.3, SSH, IPsec VPN, and code signing — including the failure modes, rollback plans, and testing each step requires.",
 "Run the toolchain: implement a toy lattice KEM in Python, drive liboqs, and stand up a hybrid TLS handshake with OQS-enabled software.",
 "Read the policy landscape: CNSA 2.0 enforcement timeline, NSM-10, NIST IR 8547 transition guidance, and how federal mandates become organizational deadlines — without claiming any certification that does not exist.",
]

HONESTY = ("This is an independent preparation and practice course aligned to publicly published standards "
 "(NIST FIPS 203/204/205, August 2024). It is not affiliated with, endorsed by, or sponsored by NIST, the NSA, "
 "the U.S. Department of Commerce, or any vendor; it confers no certificate and grants no credentials. "
 "Standards facts (publication dates, parameter sets, key and signature sizes, security levels) reflect the published "
 "FIPS documents as of October 2026 — always verify against the current standards text. No post-quantum cryptography "
 "certification exists; this course teaches TO the standards, not FOR any credential. Noah AI tutoring is grounded in "
 "this course's content with a 2026-10-09 baseline and surfaces dated delta briefs as standards evolve.")

course = {
 "code": "IL-30",
 "courseId": "il-30-post-quantum-cryptography-quantum-safe",
 "title": "IL-30 · Post-Quantum Cryptography & Quantum-Safe Engineering",
 "tagline": "Quantum-safe cryptography at engineering depth — NIST's PQC standards, lattice and hash-based math, hybrid TLS, and a real migration playbook.",
 "blurb": ("IL-30 is the quantum-safe engineering course built on NIST's finalized post-quantum cryptography standards: "
  "FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), and FIPS 205 (SLH-DSA), published August 2024. You will learn the quantum threat model "
  "(Shor vs RSA/ECC, Grover vs symmetric, harvest-now-decrypt-later), the lattice math that carries modern cryptography "
  "(LWE, Module-LWE, NTRU-style problems), each standardized algorithm at implementation depth — key sizes, parameter sets, "
  "failure modes — hybrid key exchange in TLS 1.3, and the full migration discipline: crypto inventory, prioritization, "
  "protocol playbooks (TLS, SSH, VPN, code signing), and CNSA 2.0/NSM-10 compliance timelines. Hands-on labs take you from a toy "
  "lattice cipher in Python through liboqs to a hybrid TLS handshake you capture and inspect. Noah AI is the core learning driver: "
  "five tutor personas with five natural voices, SM-2 adaptive scheduling, and course-aware Socratic tutoring that keeps your "
  "knowledge current as the standards evolve past the 2026-10-09 baseline. No vendor certificate exists for PQC yet — the course "
  "aligns to the published NIST FIPS as independent study, not certification prep."),
 "hours": HOURS,
 "mockMinutes": 90,
 "schemaVersion": "4",
 "updatedAt": "2026-10-09",
 "honestyNote": HONESTY,
 "objectives": OBJECTIVES,
 "arc": ("IL-30 takes you from mathematical foundations to a running migration program: first the lattice math spine (M00) and the "
  "quantum threat model that makes migration urgent (M01), then the standards themselves — the competition history (M02), ML-KEM (M03), "
  "ML-DSA (M04), SLH-DSA (M05), and the live pipeline of FN-DSA/HQC (M06). With the algorithms understood, you learn the transition "
  "mechanics: hybrid key exchange (M07), migration planning with crypto inventory and CBOM (M08), and the protocol playbooks for TLS (M09) "
  "and SSH/VPN/code-signing (M10). Two intensive labs make it concrete — toy lattice schemes in Python (M11) and a real hybrid TLS "
  "handshake with liboqs (M12) — before policy and compliance timelines (M13), the enterprise capstone plan (M14), and the "
  "standards-alignment readiness gate (M15). Noah AI tutors every step: the Mathematician for the math, the Engineer for the labs, "
  "the Philosopher for strategy, the Operator for the playbooks, and the Examiner for the gate — with SM-2 scheduling keeping the "
  "FIPS constants in cold recall and delta briefs keeping you current as standards evolve."),
 "priorities": [
  {"label": "Prereq math & foundations", "minutes": 1860},
  {"label": "Algorithm depth (ML-KEM/ML-DSA/SLH-DSA/pipeline)", "minutes": 2460},
  {"label": "Hybrid exchange & migration planning", "minutes": 1260},
  {"label": "Protocol playbooks (TLS, SSH, VPN, code signing)", "minutes": 1200},
  {"label": "Hands-on labs (toy lattices, hybrid TLS)", "minutes": 1380},
  {"label": "Policy, capstone & readiness gate", "minutes": 1740},
 ],
 "battlePlan": [
  {"id": "sprint-math", "title": "Math Spine Sprint", "minutes": 720,
   "detail": "M00: lattices, modular arithmetic, polynomial rings, error distributions, LWE — the foundation every algorithm module assumes."},
  {"id": "sprint-threat-history", "title": "Threat Model & Standards Sprint", "minutes": 1140,
   "detail": "M01-M02: Shor/Grover/HNDL/Mosca, then the NIST competition 2016→2024 and the live pipeline."},
  {"id": "sprint-algorithms", "title": "Algorithm Depth Sprint", "minutes": 2460,
   "detail": "M03-M06: ML-KEM, ML-DSA, SLH-DSA at implementation depth, plus FN-DSA/HQC pipeline tracking."},
  {"id": "sprint-migration", "title": "Hybrid & Migration Sprint", "minutes": 1260,
   "detail": "M07-M08: hybrid key exchange design, then crypto inventory, CBOM, prioritization, phased deployment."},
  {"id": "sprint-playbooks", "title": "Protocol Playbook Sprint", "minutes": 1200,
   "detail": "M09-M10: TLS 1.3 migration runbook; SSH, VPN, and code-signing playbooks with rollback plans."},
  {"id": "sprint-labs", "title": "Hands-On Lab Sprint", "minutes": 1380,
   "detail": "M11-M12: toy lattice schemes in Python, then liboqs + real hybrid TLS handshakes with captures."},
  {"id": "sprint-finish", "title": "Policy, Capstone & Gate Sprint", "minutes": 1740,
   "detail": "M13-M15: CNSA 2.0/NSM-10/IR 8547 timelines, the enterprise migration-plan capstone, and the readiness gate."},
 ],
 "modules": MODULES,
 "noahTutoring": NOAH_TUTORING,
 "crosswalk": [
  {"cert": "NIST FIPS 203/204/205 standards alignment (independent study — not a certification)",
   "modules": ["IL30-M02","IL30-M03","IL30-M04","IL30-M05","IL30-M15"],
   "note": "Aligned to the published standards text (August 2024). Teaches TO the standards, not FOR any credential — no PQC certification exists."},
  {"cert": "CompTIA Security+ SY0-701 — crypto domain (adjacent, independent preparation)",
   "modules": ["IL30-M01","IL30-M03","IL30-M04","IL30-M07","IL30-M09"],
   "note": "Independent preparation aligned to published SY0-701 objectives. IL-30 supports the cryptography domain; it is not a Security+ course."},
  {"cert": "CompTIA CySA+ CS0-003 — threat/vuln management (adjacent, independent preparation)",
   "modules": ["IL30-M01","IL30-M08","IL30-M13"],
   "note": "Adjacent domain support only: threat modeling, vulnerability management, and compliance timelines."},
  {"cert": "ISC2 CISSP — crypto & security architecture domains (adjacent, independent preparation)",
   "modules": ["IL30-M02","IL30-M07","IL30-M08","IL30-M13"],
   "note": "Independent preparation aligned to published 2024 CISSP domains. Adjacent support for cryptography and security architecture."},
 ],
 "certGates": [
  {"id": "gate-pqc-standards", "cert": "NIST FIPS 203/204/205 standards alignment (independent study — not a certification)",
   "trackModule": "IL30-M15",
   "framing": "Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate.",
   "format": "Closed-book recitation + allocation defense + evidence pack review, cleared twice on different days",
   "minutes": 120, "questionCount": 40,
   "readinessRule": "Score 90%+ on cold recitation (parameter sets, sizes, dates) and defend three capstone allocations with evidence, twice on different days.",
   "modules": ["IL30-M02","IL30-M03","IL30-M04","IL30-M05","IL30-M06","IL30-M13","IL30-M15"]},
  {"id": "gate-security-plus-crypto", "cert": "CompTIA Security+ SY0-701 — cryptography domain practice (adjacent)",
   "trackModule": "IL30-M09",
   "framing": "Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate.",
   "format": "Up to 90 questions, 90 minutes, passing score 750/900 (per published SY0-701 objectives; verify current objectives before booking)",
   "minutes": 90, "questionCount": 90,
   "readinessRule": "Score 83%+ (750/900 equivalent) on two consecutive timed practice gates before booking the real exam.",
   "modules": ["IL30-M01","IL30-M03","IL30-M04","IL30-M07","IL30-M09"]},
  {"id": "gate-cysa-plus-adjacent", "cert": "CompTIA CySA+ CS0-003 — threat management practice (adjacent)",
   "trackModule": "IL30-M08",
   "framing": "Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate.",
   "format": "85 questions, 165 minutes, passing score 750/900 (per published CS0-003 objectives; verify current objectives before booking)",
   "minutes": 165, "questionCount": 85,
   "readinessRule": "Score 83%+ on two consecutive timed practice gates before booking the real exam.",
   "modules": ["IL30-M01","IL30-M08","IL30-M13"]},
 ],
 "readinessDashboard": {
  "title": "IL-30 Standards-Alignment Readiness Dashboard",
  "framing": "Independent preparation. Not affiliated with, endorsed by, or sponsored by any vendor or institution; confers no certificate.",
  "concept": "Each track has a practice gate. You are ready when you clear the gate threshold twice in a row, on different days.",
  "formula": "readiness = (gate1 >= threshold) AND (gate2 >= threshold), gates on separate days",
  "thresholds": "Per-gate thresholds are listed on each certGate.",
  "statusLabels": ["not started", "in progress", "gate 1 cleared", "ready"],
  "rule": "Two consecutive clears on different days before claiming readiness.",
  "order": ["gate-pqc-standards", "gate-security-plus-crypto", "gate-cysa-plus-adjacent"],
 },
 "scriptLabs": [
  {"id": "lab-script-lwe", "title": "LWE Toy Cryptosystem Script",
   "brief": "Write a Python script implementing Regev-style LWE encryption at toy parameters with a measured failure rate and a brute-force attack timer — the M00/M11 starter.",
   "starter": "# TOY ONLY — never ship\n# TODO 1: mod-q arithmetic\n# TODO 2: keygen (A, b = A s + e)\n# TODO 3: encrypt/decrypt bit\n# TODO 4: failure-rate measurement over N trials\n# TODO 5: brute-force timer + extrapolation"},
  {"id": "lab-script-hybrid", "title": "Hybrid Combiner Simulator",
   "brief": "Simulate the X25519+ML-KEM hybrid combiner with HKDF: prove the OR-security property by revealing one component secret and showing the session key stays unknown — the M07 lab starter.",
   "starter": "# TODO 1: fake component secrets (random bytes)\n# TODO 2: HKDF combiner (hashlib)\n# TODO 3: break-simulation: reveal one secret, show K unknown\n# TODO 4: size table for KeyShare components"},
  {"id": "lab-script-cbom", "title": "Minimal CBOM Generator",
   "brief": "Generate a minimal CycloneDX CBOM JSON from TLS-scan and code-grep findings — the M08 discovery lab starter.",
   "starter": "# TODO 1: parse scan findings into components\n# TODO 2: emit CycloneDX CBOM JSON with crypto properties\n# TODO 3: query function: 'where is RSA-2048?'"},
 ],
 "drills": [
  {"id": "drill-il30-cold1", "title": "Cold recitation: FIPS sizes",
   "prompt": "ML-KEM-768 pk/ct, ML-DSA-65 pk/sig, SLH-DSA-128s pk/sig — from memory.",
   "choices": ["1184/1088, 1952/3309, 32B/~7.8KB", "800/768, 1312/2420, 64B/~49KB", "1568/1568, 2592/4627, 32B/~7.8KB", "1184/1088, 1952/3309, 48B/~17KB"],
   "answer": 0,
   "explain": "768: pk 1184 B, ct 1088 B. ML-DSA-65: pk 1952 B, sig 3309 B. SLH-DSA-128s: pk 32 B, sig ~7,856 B."},
  {"id": "drill-il30-cold2", "title": "Mandate dates",
   "prompt": "CNSA 2.0 procurement gate, IR 8547 RSA-2048 deprecation, EO 14144 TLS 1.3 date, NSM-10 horizon.",
   "choices": ["Jan 2027, deprecated 2030, Jan 2030, 2035", "2025, deprecated 2028, 2028, 2030", "2030, deprecated 2035, 2032, 2040", "Jan 2027, deprecated 2025, Jan 2030, 2035"],
   "answer": 0,
   "explain": "2027 gate; 2030 deprecation (disallowed after 2035); TLS 1.3 by Jan 2, 2030; NSM-10 horizon 2035."},
  {"id": "drill-il30-status", "title": "Pipeline status check",
   "prompt": "Status of FN-DSA and HQC as of the 2026-10-09 baseline?",
   "choices": ["Both final FIPS", "FN-DSA: FIPS 206 draft (IPD Aug 2025); HQC: selected Mar 2025, draft in progress — neither final", "Both abandoned", "FN-DSA final, HQC candidate"],
   "answer": 1,
   "explain": "Draft/selected, not final. Track, don't build — and re-verify, since the baseline moves."},
 ],
 "scenarios": [
  {"id": "scenario-hndl-board", "title": "The Board Asks About Harvest-Now-Decrypt-Later",
   "context": "Q4 board meeting. A director asks whether PQC spending can wait 'until the quantum computer exists.' You have five minutes and the Mosca worksheet.",
   "steps": [
    {"prompt": "Your opening sentence?", "options": [{"text": "Adversaries are recording our encrypted traffic today; waiting means the backlog grows while our migration clock shrinks.", "correct": True}, {"text": "Quantum computers are decades away, so yes, we can wait.", "correct": False}, {"text": "NIST hasn't finished, so there's nothing to do.", "correct": False}]},
    {"prompt": "The one number you put on the slide?", "options": [{"text": "x + y vs z for the top-5 data classes — which are already past the line.", "correct": True}, {"text": "The price of a quantum computer.", "correct": False}, {"text": "Total CVE count.", "correct": False}]},
    {"prompt": "Your ask?", "options": [{"text": "Fund discovery + the top-decile hybrid migration with dated milestones.", "correct": True}, {"text": "A bigger firewall.", "correct": False}, {"text": "Wait for a certification to exist.", "correct": False}]},
   ]},
  {"id": "scenario-vendor-pqc-claim", "title": "Vendor Claims 'PQC Ready'",
   "context": "A critical vendor's one-pager says 'PQC ready' with no details. Your renewal decision depends on it.",
   "steps": [
    {"prompt": "First response?", "options": [{"text": "Require specifics: named algorithms, FIPS references, validation status, deployment evidence.", "correct": True}, {"text": "Accept the claim.", "correct": False}, {"text": "Ask for a discount instead.", "correct": False}]},
    {"prompt": "The contract clause must include?", "options": [{"text": "Dated PQC support commitments, CBOM disclosure, and algorithm-negotiation requirements.", "correct": True}, {"text": "A marketing quote.", "correct": False}, {"text": "Nothing — trust them.", "correct": False}]},
   ]},
 ],
 "trainers": [],
 "terminalSims": [
  {"id": "term-openssl-pqc", "title": "OpenSSL PQC handshake drill",
   "brief": "Simulated terminal: list PQC providers, configure the hybrid group, run s_server/s_client, and read the negotiated group from the session output.",
   "steps": ["openssl list -providers", "openssl list -kem-algorithms | grep -i ml-kem", "openssl s_server -groups X25519MLKEM768 ...", "openssl s_client -connect ... -groups X25519MLKEM768", "Read 'Negotiated group' from the output"]},
  {"id": "term-liboqs-kat", "title": "liboqs KAT verification drill",
   "brief": "Simulated terminal: build liboqs at a pinned version and run the known-answer tests for ML-KEM-768 and ML-DSA-65.",
   "steps": ["git checkout <pinned-tag>", "cmake -B build && cmake --build build", "./build/tests/kat_kem ML-KEM-768", "./build/tests/kat_sig ML-DSA-65", "Confirm: all KATs pass"]},
 ],
 "mockTasks": [],
 "cheatSheets": [
  {"id": "IL30-CH-SIZES", "title": "FIPS sizes — cold-recall sheet", "moduleId": "IL30-M15",
   "blocks": [{"h": "ML-KEM (FIPS 203)", "body": "- 512: pk 800 B, ct 768 B, sk 1632 B (level 1)\n- 768: pk 1184 B, ct 1088 B, sk 2400 B (level 3, default)\n- 1024: pk 1568 B, ct 1568 B, sk 3168 B (level 5)"}, {"h": "ML-DSA (FIPS 204)", "body": "- 44: pk 1312 B, sig 2420 B (level 2)\n- 65: pk 1952 B, sig 3309 B (level 3, default)\n- 87: pk 2592 B, sig 4627 B (level 5)"}, {"h": "SLH-DSA (FIPS 205)", "body": "- pk 32/48/64 B; sig 7.8–49 KB; 12 sets: SHA2/SHAKE × 128/192/256 × s/f"}]},
  {"id": "IL30-CH-THREAT", "title": "Quantum threat model — one page", "moduleId": "IL30-M01",
   "blocks": [{"h": "Reference", "body": "- Shor: breaks RSA, DH/DSA, ECDSA/ECDH/EdDSA (factoring + discrete log, polynomial time)\n- Grover: quadratic — AES-128 → ~64-bit (dead), AES-256 → ~128-bit (fine)\n- BHT: collisions ~n/3 — SHA-384/512 per CNSA 2.0\n- HNDL: record now, decrypt later — the deadline mover\n- Mosca: x + y > z ⇒ migrate now (secrecy + migration time vs time-to-break)"}]},
  {"id": "IL30-CH-TIMELINE", "title": "Mandate timeline — one page", "moduleId": "IL30-M13",
   "blocks": [{"h": "Dates", "body": "- 2025: CNSA 2.0 support-and-prefer (signing, web/cloud)\n- Jan 1, 2027: CNSA 2.0 procurement gate (new NSS acquisitions)\n- Jan 2, 2030: EO 14144 — TLS 1.3+ across federal systems\n- 2030: CNSA 2.0 exclusive use (signing, networking); IR 8547 deprecates RSA-2048/ECC-256\n- End 2031: CNSA 2.0 full enforcement\n- 2033: niche/legacy done\n- 2035: NSM-10 horizon; IR 8547 disallows RSA-2048/ECC-256"}]},
  {"id": "IL30-CH-HYBRID", "title": "Hybrid key exchange — one page", "moduleId": "IL30-M07",
   "blocks": [{"h": "Reference", "body": "- Property: secure if EITHER component holds (OR-security)\n- TLS 1.3: X25519MLKEM768 — concatenated KeyShare, HKDF-combined secrets\n- Combiner: KDF with domain separation, never raw concat\n- Order: KEX hybrids first (HNDL win, low cost); signature hybrids selectively\n- End state: pure PQC per CNSA 2.0 2030s posture — hybrids are the bridge"}]},
  {"id": "IL30-CH-PIPELINE", "title": "Pipeline status — one page", "moduleId": "IL30-M06",
   "blocks": [{"h": "As of 2026-10-09", "body": "- FINAL: FIPS 203/204/205 (Aug 13, 2024) — build here\n- DRAFT: FIPS 206 FN-DSA (IPD Aug 2025; final ~late 2026/early 2027) — lab only\n- SELECTED: HQC (Mar 2025; draft in progress) — track only\n- CANDIDATE: additional-signatures round 2 — track only\n- Rule: never cite draft/selected as 'NIST-approved' without the qualifier"}]},
  {"id": "IL30-CH-MIGRATION", "title": "Migration phases — one page", "moduleId": "IL30-M08",
   "blocks": [{"h": "Reference", "body": "- Discover: network scan + code analysis + config review → CBOM (CycloneDX)\n- Prioritize: exposure × lifetime × blast radius; Mosca per data class\n- Phase 1: pilot (measure, rollback-ready) → 2: high-value/HNDL → 3: broad → 4: pure-PQC\n- Crypto-agility in procurement: negotiation, pluggable providers, dated PQC commitments\n- Evidence over badges: no PQC certification exists"}]},
 ],
 "answerBank": {
  "note": "Every drill item and quiz question carries its answer and explanation inline; this bank indexes them by module for review.",
  "modules": ["IL30-M00","IL30-M01","IL30-M02","IL30-M03","IL30-M04","IL30-M05","IL30-M06","IL30-M07","IL30-M08","IL30-M09","IL30-M10","IL30-M11","IL30-M12","IL30-M13","IL30-M14","IL30-M15"],
 },
 "sourceLinks": [
  {"url": FIPS203, "name": "NIST FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard", "retrieved": "2026-10-09"},
  {"url": FIPS204, "name": "NIST FIPS 204 — Module-Lattice-Based Digital Signature Standard", "retrieved": "2026-10-09"},
  {"url": FIPS205, "name": "NIST FIPS 205 — Stateless Hash-Based Digital Signature Standard", "retrieved": "2026-10-09"},
  {"url": PQCPROJ, "name": "NIST Post-Quantum Cryptography project page", "retrieved": "2026-10-09"},
  {"url": OQSORG, "name": "Open Quantum Safe (GitHub organization)", "retrieved": "2026-10-09"},
  {"url": OQSPROV, "name": "OQS oqs-provider — PQC for OpenSSL 3", "retrieved": "2026-10-09"},
  {"url": KFCIPHER, "name": "PQC standards tracker — FIPS 203/204/205/206 and HQC status", "retrieved": "2026-10-09"},
  {"url": QSDFIPS, "name": "NIST FIPS 203, 204 and 205: PQC Standards — coverage and gaps", "retrieved": "2026-10-09"},
  {"url": FNDSA, "name": "DigiCert — Quantum-ready FN-DSA (FIPS 206) nears draft approval", "retrieved": "2026-10-09"},
  {"url": FIPS206, "name": "NIST locks FN-DSA to fixed-point math for FIPS 206", "retrieved": "2026-10-09"},
  {"url": "https://postquantum.com/security-pqc/nsa-cnsa-2-0-faq-v2-1-update/", "name": "NSA updates CNSA 2.0 after NIST finalizes PQC standards (V2.1 FAQ timeline)", "retrieved": "2026-10-09"},
  {"url": PQCNSA, "name": "NSA unveils CNSA 2.0 post-quantum algorithm suite", "retrieved": "2026-10-09"},
  {"url": AXEL, "name": "CNSA 2.0 & NIST PQC deadlines 2026–2035", "retrieved": "2026-10-09"},
  {"url": TQI, "name": "Post-quantum cryptography timelines: when will organizations migrate?", "retrieved": "2026-10-09"},
  {"url": NCCOE, "name": "NIST NCCoE — crypto-agility considerations for migrating to PQC algorithms", "retrieved": "2026-10-09"},
  {"url": DHSQ, "name": "DHS post-quantum cryptography roadmap", "retrieved": "2026-10-09"},
  {"url": CBOM, "name": "CycloneDX Cryptography Bill of Materials (CBOM)", "retrieved": "2026-10-09"},
  {"url": AWESOME, "name": "awesome-post-quantum — curated PQC resource list", "retrieved": "2026-10-09"},
 ],
 "toolLabs": [],
 "multicloudLabs": [],
 "sampleDatasets": [],
 "installSteps": [],
 "installLabs": [],
 "installPrereqOrder": [],
 "employerMappings": [],
 "jdMatrix": [],
 "sqlPlaygrounds": [],
 "pythonExercises": [
  {"id": "py-il30-ring", "title": "Ring arithmetic in Z_q[x]/(x^n+1)",
   "brief": "Implement polynomial multiplication with modular reduction — the M00 lab starter as a graded exercise.",
   "starter": "# TODO: poly_mul(a, b, q, n) with x^n = -1 reduction"},
  {"id": "py-il30-lwe", "title": "Toy LWE encrypt/decrypt",
   "brief": "Regev-style encryption at toy parameters with failure-rate measurement — the M11 exercise.",
   "starter": "# TOY ONLY\n# TODO: keygen, encrypt, decrypt, failure-rate loop"},
  {"id": "py-il30-hybrid", "title": "Hybrid KDF combiner",
   "brief": "HKDF-combine two component secrets and prove OR-security by simulation — the M07 exercise.",
   "starter": "# TODO: HKDF combiner + break-simulation"},
 ],
 "daxPlaygrounds": [],
 "branchingScenarios": [
  {"id": "bs-il30-rollback", "title": "Canary Failure: Roll Back or Push Through?",
   "context": "Hybrid TLS canary at 5%: handshake failures spike on one ASN. The release train leaves in 4 hours.",
   "branches": [
    {"choice": "Roll back the affected ASN via pipeline, keep hybrid elsewhere, alert loudly", "outcome": "Correct: surgical, loud, dated — the failure becomes a vendor ticket with telemetry."},
    {"choice": "Disable PQC globally and ship classical", "outcome": "Wrong: global retreat from a local problem; silent downgrade risk if the revert isn't tracked."},
    {"choice": "Push through — 5% failure is acceptable", "outcome": "Wrong: 5% of production handshakes failing is an outage wearing a feature flag."},
   ]},
  {"id": "bs-il30-signing", "title": "Firmware Signing: Ship Falcon Now?",
   "context": "Bootloader budget fits Falcon (~666 B) but not ML-DSA (~3.3 KB). FIPS 206 is in draft. Release is Q1.",
   "branches": [
    {"choice": "Lab-pilot the IPD, re-evaluate at FIPS 206 final; parallel-track ML-DSA size mitigations", "outcome": "Correct: constraint respected, draft not shipped, decision trigger dated."},
    {"choice": "Ship the IPD implementation now", "outcome": "Wrong: draft crypto in an unpatchable bootloader — spec churn becomes bricked devices."},
    {"choice": "Stay on ECDSA indefinitely", "outcome": "Wrong: HNDL doesn't apply to signatures, but 15-year firmware trust with quantum-vulnerable signatures fails the Mosca test."},
   ]},
 ],
 "clickSims": [
  {"id": "cs-il30-handshake", "title": "Dissect a hybrid TLS handshake",
   "brief": "Click-through packet anatomy: ClientHello → supported_groups → KeyShare lengths → ServerHello selection → certificate chain bytes. Identify the hybrid group and compute the size tax.",
   "steps": ["Open the capture", "Find supported_groups", "Measure KeyShare", "Confirm server selection", "Total the size tax"]},
  {"id": "cs-il30-cbom", "title": "Query a CBOM",
   "brief": "Click-through CBOM explorer: run 'where is RSA-2048?', drill into an asset's crypto properties, and flag the top-3 migration priorities.",
   "steps": ["Load the CBOM", "Query RSA-2048", "Open asset detail", "Score the findings", "Export the priority queue"]},
 ],
 "interactivityAudit": {
  "terminalSims": 2, "branchingScenarios": 2, "clickSims": 2, "toolLabs": 0,
  "installLabs": 0, "multicloudLabs": 0, "trainers": 0, "scriptLabs": 3,
  "cheatSheets": 6, "totalInteractive": 15,
  "rule": "Every module ships notes, flashcards, quiz, drills, a hands-on lab, a mock task, and a Noah tutor prompt; interactivity is counted, not claimed.",
 },
 "studyGuide": {
  "title": "Study guide: how to work IL-30 in 10 weeks",
  "totalHours": HOURS,
  "totalMinutes": TOTAL_MIN,
  "note": "Noah AI paces the plan: SM-2 schedules your reviews, the Examiner rehearses each gate, and delta briefs keep the plan current.",
  "pacing": [
   "Weeks 1-2 — Foundations: M00 (math spine) + M01 (threat model) + M02 (standards history). Open every module with its Noah starter prompt; the Mathematician and Philosopher carry these weeks.",
   "Weeks 3-4 — Algorithm depth: M03 (ML-KEM) + M04 (ML-DSA). Implement the toy schemes (M11 first half) in parallel — theory and code reinforce each other.",
   "Weeks 5-6 — Signatures & pipeline: M05 (SLH-DSA) + M06 (FN-DSA/HQC). Build the standards tracker and pipeline watch; these are living documents.",
   "Week 7 — Transition mechanics: M07 (hybrids) + M08 (migration planning). Run the hybrid combiner simulation; draft the CBOM.",
   "Week 8 — Playbooks: M09 (TLS) + M10 (SSH/VPN/code signing). Finish the M12 hybrid-TLS lab; every playbook gets a rollback plan.",
   "Week 9 — Policy & integration: M13 (mandates) + M11/M12 lab completion. Evidence pack assembled: captures, benchmarks, KATs.",
   "Week 10 — Capstone & gate: M14 (migration plan) + M15 (readiness gate, cleared twice). The course ends when your org's program starts.",
  ],
 },
 "timeFormula": "estimatedMinutes per module = instruction + videos + drills + hands-on lab, set per module by the author; course total = sum of module estimates. Declared hours are the honest rounded sum.",
 "glossary": [
  {"term": "Post-quantum cryptography (PQC)", "definition": "Cryptography believed secure against quantum computers — almost entirely classical algorithms running on classical hardware."},
  {"term": "ML-KEM", "definition": "Module-Lattice Key-Encapsulation Mechanism; FIPS 203; from CRYSTALS-Kyber. The primary PQC key-establishment standard."},
  {"term": "ML-DSA", "definition": "Module-Lattice Digital Signature Algorithm; FIPS 204; from CRYSTALS-Dilithium. The primary PQC signature standard."},
  {"term": "SLH-DSA", "definition": "Stateless Hash-Based Digital Signature Algorithm; FIPS 205; from SPHINCS+. Conservative hash-only backup signature."},
  {"term": "FN-DSA", "definition": "Falcon-based signature slated for FIPS 206 (draft); compact NTRU-lattice signatures. Not final — track, don't build."},
  {"term": "HQC", "definition": "Hamming Quasi-Cyclic code-based KEM; selected March 2025 as backup KEM. Not final — track, don't build."},
  {"term": "Shor's algorithm", "definition": "Quantum algorithm breaking factoring and discrete logs in polynomial time — kills RSA, DH, ECDSA, ECDH."},
  {"term": "Grover's algorithm", "definition": "Quantum search with quadratic speedup — halves symmetric key strength in bits."},
  {"term": "Harvest-now-decrypt-later (HNDL)", "definition": "Recording encrypted traffic today for quantum decryption later — moves the migration deadline earlier."},
  {"term": "Mosca's inequality", "definition": "x + y > z ⇒ migrate now: secrecy lifetime + migration time vs time-to-quantum-break."},
  {"term": "Lattice", "definition": "Discrete additive subgroup of R^n — integer combinations of basis vectors; the geometric home of PQC hardness."},
  {"term": "SVP / CVP", "definition": "Shortest Vector Problem / Closest Vector Problem — the lattice hard problems underpinning security."},
  {"term": "LWE", "definition": "Learning With Errors: recover s from noisy linear samples (a, <a,s>+e). Believed quantum-hard."},
  {"term": "Module-LWE", "definition": "LWE over module rank-k vectors of ring elements — the efficient structured variant behind ML-KEM/ML-DSA."},
  {"term": "R_q", "definition": "The polynomial ring Z_q[x]/(x^256+1) used by ML-KEM/ML-DSA — 256 coefficients mod q with x^256 = -1."},
  {"term": "KEM", "definition": "Key Encapsulation Mechanism: KeyGen/Encaps/Decaps — one-pass key establishment without interaction."},
  {"term": "Fujisaki–Okamoto transform", "definition": "Upgrades IND-CPA encryption to IND-CCA2 KEM via re-encryption check + implicit rejection."},
  {"term": "Implicit rejection", "definition": "Invalid ciphertexts decapsulate to pseudorandom keys, not errors — denies chosen-ciphertext oracles."},
  {"term": "Fiat–Shamir with aborts", "definition": "Dilithium signing: hash-derived challenge, rejection sampling to keep responses secret-independent."},
  {"term": "FORS", "definition": "Forest of Random Subsets — few-time signature at SLH-DSA's hypertree leaves signing the message digest."},
  {"term": "Hypertree", "definition": "Layered XMSS Merkle trees in SLH-DSA — scales hash-based signatures to many messages, statelessly."},
  {"term": "WOTS+", "definition": "Winternitz one-time signature — the one-shot signing primitive inside hash-based schemes."},
  {"term": "Hybrid key exchange", "definition": "Classical + PQC KEM combined; secure if EITHER holds. The transition workhorse (X25519MLKEM768)."},
  {"term": "X25519MLKEM768", "definition": "Standardized hybrid TLS 1.3 group: X25519 + ML-KEM-768 with KDF-combined secrets."},
  {"term": "CBOM", "definition": "Cryptography Bill of Materials (CycloneDX) — machine-readable crypto inventory per asset."},
  {"term": "Crypto-agility", "definition": "Architecture where algorithms are negotiable/pluggable, not hardcoded — the ability to rotate on demand."},
  {"term": "CNSA 2.0", "definition": "NSA's quantum-resistant suite + timeline for National Security Systems (2022; procurement gate Jan 2027)."},
  {"term": "NSM-10", "definition": "National Security Memorandum 10 (May 2022) — inventory, prioritize, mitigate most quantum risk by 2035."},
  {"term": "NIST IR 8547", "definition": "Transition-to-PQC framework (draft 2024): RSA-2048/ECC-256 deprecated 2030, disallowed after 2035."},
  {"term": "KAT", "definition": "Known Answer Test — fixed test vectors proving an implementation matches the standard exactly."},
  {"term": "liboqs", "definition": "Open Quantum Safe C library — PQC KEMs/signatures behind a common API; the lab standard."},
  {"term": "oqs-provider", "definition": "OpenSSL 3 provider adding PQC algorithms and hybrid groups to OpenSSL-based apps."},
  {"term": "SM-2", "definition": "Spaced-repetition scheduling algorithm Noah uses to time flashcard/quiz reviews per learner."},
 ],
 "faq": [
  {"q": "Is there a PQC certification I can earn with IL-30?", "a": "No — and be wary of anyone selling one. No post-quantum cryptography certification exists as of October 2026. IL-30 aligns you to the published NIST FIPS 203/204/205 as independent study and builds an evidence pack (captures, benchmarks, migration plan) that demonstrates readiness. The readiness gate measures that, not a badge."},
  {"q": "Why learn PQC now if quantum computers can't break RSA yet?", "a": "Harvest-now-decrypt-later: adversaries record today's encrypted traffic for future decryption. Combined with multi-year migration lead times (Mosca's inequality), the deadline for long-lived data has already passed. M01 makes this quantitative."},
  {"q": "Should we deploy HQC or FN-DSA today?", "a": "No. HQC is selected-but-not-standardized; FN-DSA/FIPS 206 is in draft. Build production on final FIPS 203/204/205, experiment with drafts in labs, and track the pipeline with dated triggers. M06 is the full discipline."},
  {"q": "Hybrid or pure PQC?", "a": "Hybrid first, pure later. Hybrids (X25519+ML-KEM) hedge young-standard risk and preserve interop during transition; CNSA 2.0's end state moves toward PQC-exclusive use in the 2030s. M07 covers the design; M08 the phasing."},
  {"q": "How does Noah keep the content current?", "a": "Noah tracks the standards pipeline against the 2026-10-09 course baseline (FIPS 206, HQC, IR 8547, CNSA 2.0 revisions, new cryptanalysis) and surfaces dated delta briefs: what changed, which modules it touches, whether your capstone plan needs revision. See noahTutoring.currencyMechanism."},
  {"q": "Do I need the math module (M00)?", "a": "Yes — it's load-bearing. You can't read the FIPS pseudocode, evaluate parameter choices, or spot snake-oil vendor claims without lattices, modular arithmetic, and error distributions. It draws on IL-02/IL-06 and is the prerequisite for M03–M06 and M11."},
  {"q": "How is IL-30 different from IL-06/IL-11's crypto content?", "a": "IL-06 and IL-11 teach classical cryptography and zero-trust architecture. IL-30 is the post-quantum sequel: the quantum threat model, the NIST PQC standards at implementation depth, and the migration program. Cross-links connect them; IL-30 assumes their foundations."},
  {"q": "What hardware/software do the labs need?", "a": "A Linux VM or container: Python 3, a C toolchain, cmake, OpenSSL, Wireshark/tshark. liboqs and oqs-provider build from source at pinned versions. No quantum computer required — that, happily, is the point."},
 ],
 "tips": [
  "Follow the guided path in order — M00's math is load-bearing for M03–M06, and the migration modules assume the algorithm depth. The sequence is the curriculum.",
  "Open every module with its Noah starter prompt: state a hypothesis first, let the persona push back Socratically, then read the notes. Tutoring before content beats content before tutoring.",
  "Cold-recall the FIPS constants (sizes, parameter sets, dates) via Noah's SM-2 scheduling — the readiness gate is closed-book and the numbers must be automatic.",
  "Do each hands-on lab twice — once following the steps, once from memory with the evidence pack as the deliverable. Artifacts, not assertions.",
  "Re-verify every pipeline status quarterly against primary sources. Standards move; your citations must carry dates. Noah's delta briefs help, but the habit is yours.",
  "When a vendor says 'PQC ready,' ask for the capture, the versions, and the named algorithms. This course trained you to accept evidence, not claims — practice it everywhere.",
 ],
 "legends": {
  "✓ Complete": "Module finished — marked complete by you, or auto-marked when you scrolled the whole module.",
  "✓ Mastered": "Module finished AND its quiz mastery gate passed (score of 70% or higher).",
  "✓ Tested out": "Placed out via the diagnostic — counts as passed without completing the module.",
  "● You are here": "Your current position in the guided sequence.",
  "→ Up next": "The next module in the sequence — unlocks when the current lesson is passed.",
  "🔒 Locked": "Complete the previous lesson to unlock this module.",
  "🤖 Noah": "Noah AI — your Socratic tutor. Each module opens with a persona-matched starter prompt; five personas, five voices, SM-2 scheduled. Ask with a hypothesis; it guides with questions before answers, grounded in this course's content with a 2026-10-09 baseline.",
 },
 "topicTheme": "mr-robot",
 "topic": "cybersecurity",
}

# mockTasks: one per module, derived from module mockTask
for m in MODULES:
    mt = dict(m["mockTask"])
    mt["id"] = m["id"] + "-MOCK"
    mt["type"] = "choice"
    mt["moduleId"] = m["id"]
    course["mockTasks"].append(mt)

with open(OUT, "w") as f:
    json.dump(course, f, indent=1, ensure_ascii=False)
    f.write("\n")

# validate
with open(OUT) as f:
    d = json.load(f)
print("modules:", len(d["modules"]), "| hours:", d["hours"], "| sum/60:", TOTAL_MIN/60)
print("schemaVersion:", d["schemaVersion"], "| updatedAt:", d["updatedAt"])
print("noahTutoring personas:", len(d["noahTutoring"]["personas"]))
print("mockTasks:", len(d["mockTasks"]), "| cheatSheets:", len(d["cheatSheets"]))
req = ["id","code","title","summary","objectives","estimatedMinutes","weight","prerequisiteFor","crossLinks","cards","quiz","drills","handsOnLab","mockTask","videos","pdfs","notes","noahTutor"]
bad = [m["id"] for m in d["modules"] if any(k not in m for k in req)]
print("modules missing keys:", bad)
topreq = ["code","courseId","title","tagline","blurb","hours","mockMinutes","schemaVersion","updatedAt","honestyNote","objectives","arc","priorities","battlePlan","modules","noahTutoring","crosswalk","certGates","readinessDashboard","scriptLabs","drills","scenarios","trainers","terminalSims","mockTasks","cheatSheets","answerBank","sourceLinks","toolLabs","multicloudLabs","sampleDatasets","installSteps","installLabs","installPrereqOrder","employerMappings","jdMatrix","sqlPlaygrounds","pythonExercises","daxPlaygrounds","branchingScenarios","clickSims","interactivityAudit","studyGuide","timeFormula","glossary","faq","tips","legends","topicTheme","topic"]
missing = [k for k in topreq if k not in d]
print("top-level missing:", missing)
