export type Domain =
  | "math"
  | "language"
  | "systems"
  | "security"
  | "physics"
  | "chain"
  | "humanities";

export type KNode = {
  id: string;
  domain: Domain;
  title: string;
  prereqs: string[];
  /** Asked before any explanation. */
  ask: string;
  /** A second question. Not the answer. */
  nudge: string;
  choices: string[];
  answer: number;
  why: string;
  path?: string;
};

export const domains: { id: Domain; label: string }[] = [
  { id: "math", label: "Math" },
  { id: "language", label: "Languages" },
  { id: "systems", label: "Systems" },
  { id: "security", label: "Security" },
  { id: "physics", label: "Physics" },
  { id: "chain", label: "Chain" },
  { id: "humanities", label: "Humanities" },
];

export const knowledge: KNode[] = [
  {
    id: "math-rate",
    domain: "math",
    title: "Rates back into counts",
    prereqs: [],
    ask: "A service does 100 requests a second at a 0.1% error budget, for 30 days. What kind of number is the budget?",
    nudge: "What do you multiply, and which factor did you almost drop?",
    choices: ["A percentage you feel", "An integer count of failed requests", "The p99 latency", "The number of deploys"],
    answer: 1,
    why: "0.1% of the requests in the window is a count. The action changes when that count is three versus hundreds of thousands.",
    path: "aleks-ops-math",
  },
  {
    id: "math-tail",
    domain: "math",
    title: "The tail, not the mean",
    prereqs: ["math-rate"],
    ask: "Eight latencies: 10, 12, 11, 40, 13, 11, 90, 12. Which summary is the tired user?",
    nudge: "If you sort them, where does the far end sit?",
    choices: ["The mean, about 25", "The minimum", "A high percentile, the 90 sitting at the end", "The deploy count"],
    answer: 2,
    why: "The mean hides 90. p99-style talk is about the tail you would actually page on.",
    path: "aleks-ops-math",
  },
  {
    id: "py-indent",
    domain: "language",
    title: "Python blocks",
    prereqs: [],
    ask: "A function body in Python is grouped by what?",
    nudge: "What happens if the next line does not line up with the block you think you opened?",
    choices: ["Braces", "Indentation", "A trailing semicolon", "The word end"],
    answer: 1,
    why: "The suite is the indent. A mis-aligned line is a different block, not a style nit.",
  },
  {
    id: "py-default",
    domain: "language",
    title: "Mutable defaults",
    prereqs: ["py-indent"],
    ask: "def push(item, bag=[]): bag.append(item); return bag. What is true on the second call?",
    nudge: "When is that list object created — each call, or once?",
    choices: ["bag is always empty", "The same list survives from the first call", "Python copies the list", "append returns a new list"],
    answer: 1,
    why: "Default values are bound at definition. A mutable default is shared state. Use None and create the list inside.",
  },
  {
    id: "js-eq",
    domain: "language",
    title: "JavaScript equality",
    prereqs: [],
    ask: "What does 0 == '0' do, and what does 0 === '0' do?",
    nudge: "Which operator is allowed to coerce?",
    choices: ["Both true", "Both false", "Loose is true, strict is false", "Loose is false, strict is true"],
    answer: 2,
    why: "== coerces. === does not. In a security check, coercion is how a string slips past a number test.",
  },
  {
    id: "js-const",
    domain: "language",
    title: "const is a binding",
    prereqs: ["js-eq"],
    ask: "const box = { n: 1 }; box.n = 2; does this throw?",
    nudge: "What did const freeze — the binding, or the object?",
    choices: ["Yes, const freezes the object", "No, the binding is fixed and the object is not", "Only in strict mode", "Only if n was a string"],
    answer: 1,
    why: "const stops reassignment of the name. It does not deep-freeze. Object.freeze is a different tool, and still shallow.",
  },
  {
    id: "java-eq",
    domain: "language",
    title: "Java identity",
    prereqs: [],
    ask: "Two String objects built with new String(\"ok\") compared with ==. What are you comparing?",
    nudge: "Where would you look if you wanted the characters, not the references?",
    choices: ["The characters", "The references", "The hash of the class", "The length only"],
    answer: 1,
    why: "== on objects is identity. .equals is the value comparison you usually meant. Interning can make this look fine until it is not.",
  },
  {
    id: "c-decay",
    domain: "language",
    title: "C arrays decay",
    prereqs: [],
    ask: "You pass an int a[8] into void f(int *p). What did the callee receive?",
    nudge: "Can the callee recover 8 from the pointer alone?",
    choices: ["The array and its length", "A pointer to the first element, length lost", "A copy of eight ints", "A slice object"],
    answer: 1,
    why: "The length has to travel separately. Forgetting it is how loops walk off the end.",
  },
  {
    id: "cpp-raii",
    domain: "language",
    title: "C++ scope owns the resource",
    prereqs: ["c-decay"],
    ask: "A lock guard is constructed at the start of a block. When is the mutex released?",
    nudge: "Who calls the destructor, and on which exit?",
    choices: ["When you remember to unlock", "When the guard's scope ends, including by return", "Only if no exception is thrown", "At process exit"],
    answer: 1,
    why: "RAII ties the release to the destructor. Early returns and exceptions still unwind the scope.",
  },
  {
    id: "perl-sigil",
    domain: "language",
    title: "Perl sigils",
    prereqs: [],
    ask: "You have @items. Which expression is one element?",
    nudge: "The sigil follows what you are taking, not only what you stored.",
    choices: ["@items[0]", "$items[0]", "%items[0]", "&items[0]"],
    answer: 1,
    why: "$items[0] is the scalar element. The @ names the whole array. Context bugs start when the sigil and the context disagree.",
  },
  {
    id: "ps-eq",
    domain: "language",
    title: "PowerShell comparison",
    prereqs: [],
    ask: "How do you test equality in PowerShell?",
    nudge: "What language's operator did you almost type?",
    choices: ["==", "-eq", ".equals()", "eq?"],
    answer: 1,
    why: "-eq is the operator. == is not. The pipeline also binds differently than a C-like if.",
  },
  {
    id: "bash-mode",
    domain: "language",
    title: "A mode is three triples",
    prereqs: [],
    ask: "chmod 640 on a log file. Who can write?",
    nudge: "Read the octal as owner, group, other.",
    choices: ["Everyone", "Owner only", "Owner and group", "Group only"],
    answer: 1,
    why: "6 is rw for the owner, 4 is r for the group, 0 is nothing for others. The desk shell will make you set this without a real host.",
  },
  {
    id: "sql-null",
    domain: "language",
    title: "NULL is not a value",
    prereqs: [],
    ask: "In SQL, what is NULL = NULL?",
    nudge: "If it were false, how would you write the test instead?",
    choices: ["TRUE", "FALSE", "UNKNOWN", "0"],
    answer: 2,
    why: "Comparisons with NULL yield unknown. Use IS NULL. Filtering with = NULL drops the rows you came to inspect.",
  },
  {
    id: "sys-probe",
    domain: "systems",
    title: "Liveness is not readiness",
    prereqs: [],
    ask: "A probe that fails when a dependency blips, and restarts the process. Which probe was misused?",
    nudge: "Which one is allowed to remove you from the Service without killing you?",
    choices: ["Readiness", "Liveness", "Startup, always", "The Service port"],
    answer: 1,
    why: "Liveness restarts. Readiness withdraws. Restarting on a dependency blip makes the blip worse.",
    path: "kubernetes-sre",
  },
  {
    id: "sys-plan",
    domain: "systems",
    title: "A plan is a diff with consequences",
    prereqs: ["sys-probe"],
    ask: "Terraform shows destroy on a database. What do you do before apply?",
    nudge: "Is a green apply the same thing as a read plan?",
    choices: ["Apply, then read", "Stop and name the destroy", "Refresh state twice", "Ignore destroys on stateful resources"],
    answer: 1,
    why: "A destroy on state is a stop. Two applies without a lock are how state corrupts.",
    path: "iac-terraform-gitops",
  },
  {
    id: "sec-page",
    domain: "security",
    title: "A score is not an action",
    prereqs: [],
    ask: "A model scores a host at 0.97. What is the score allowed to do by itself?",
    nudge: "Who is still in the loop if the definition update is buggy?",
    choices: ["Isolate the host", "Open a case a human can reject", "Page the CEO", "Rotate every key"],
    answer: 1,
    why: "Detection latency of a few minutes is cheaper than isolating the process operators use to see the line.",
    path: "ai-aided-cybersecurity",
  },
  {
    id: "sec-chain",
    domain: "security",
    title: "Provenance is not intent",
    prereqs: ["sec-page"],
    ask: "An npm release has valid build provenance, and the payload runs during normal use, not in a postinstall. What did provenance prove?",
    nudge: "Which question did the signature not answer?",
    choices: ["The source was reviewed", "A specific builder produced the artifact", "The package is safe to import", "Downloads imply review"],
    answer: 1,
    why: "Provenance binds the artifact to a builder. It does not prove the source that entered the builder was trustworthy. Lifecycle-script blocks miss runtime payloads.",
    path: "devsecops-mastery",
  },
  {
    id: "phys-dim",
    domain: "physics",
    title: "Units have to match",
    prereqs: ["math-rate"],
    ask: "You add 10 meters to 3 seconds. What do you have?",
    nudge: "What would have to be true of the dimensions before addition is defined?",
    choices: ["13", "A speed", "Not a physical quantity", "An acceleration"],
    answer: 2,
    why: "Addition requires the same dimension. A bug in a unit is a bug in the model, not a rounding error.",
  },
  {
    id: "phys-g",
    domain: "physics",
    title: "Acceleration is not velocity",
    prereqs: ["phys-dim"],
    ask: "A constant acceleration of 2 m/s² for 3 seconds, from rest. What is the velocity?",
    nudge: "Which quantity grows with time, and which one stays put?",
    choices: ["2 m/s", "6 m/s", "5 m/s", "2 m"],
    answer: 1,
    why: "From rest, v = at = 6 m/s. The displacement would be ½at², which is a different question. Do not mix them.",
  },
  {
    id: "cs-log",
    domain: "systems",
    title: "Binary search is logarithmic",
    prereqs: [],
    ask: "A sorted table of a million rows. About how many comparisons does a binary search need?",
    nudge: "What happens to the search space each step?",
    choices: ["About a million", "About twenty", "Exactly two", "It depends on the hash"],
    answer: 1,
    why: "log2(10^6) is a little under 20. Linear search is the million. Hashing is a different structure.",
  },
  {
    id: "pqc-kem",
    domain: "security",
    title: "Key establishment is not a signature",
    prereqs: ["sec-page"],
    ask: "NIST's post-quantum key-establishment standard (FIPS 203) is known as what?",
    nudge: "Which job is 'agree on a secret', and which job is 'sign a message'?",
    choices: ["ML-DSA, for signatures", "ML-KEM", "AES-256 used as a signature", "A larger RSA modulus"],
    answer: 1,
    why: "ML-KEM (Kyber) establishes keys. ML-DSA (Dilithium, FIPS 204) signs. A token thread that says 'quantum-proof chain' has not named either.",
  },
  {
    id: "chain-check",
    domain: "chain",
    title: "A node rechecks",
    prereqs: ["pqc-kem"],
    ask: "A block arrives with a high fee. What makes a full node accept it?",
    nudge: "What would a node recompute even if a miner already did?",
    choices: ["The fee alone", "Signatures, rules, and the resulting state", "The miner's brand", "How many followers the poster has"],
    answer: 1,
    why: "Full nodes re-execute and check the rules. Reputation and fees are not validity. This is engineering, not a trade.",
  },
  {
    id: "dee-rule",
    domain: "humanities",
    title: "A symbol means its rule",
    prereqs: [],
    ask: "John Dee's Monas is useful here as what?",
    nudge: "If the picture and the written rule disagree, which one does an interpreter follow?",
    choices: ["A source of hidden power", "A historical composed sign whose meaning is the rule you write down", "A programming language from 1564", "A key to other people's systems"],
    answer: 1,
    why: "Dee (Monas Hieroglyphica, 1564) is history. An interpreter matches and rewrites. The drawing does not outrank the rule. Nothing here is a secret transmission.",
    path: "enochian-programming",
  },
  {
    id: "dee-stop",
    domain: "humanities",
    title: "Say why it stops",
    prereqs: ["dee-rule"],
    ask: "A rewrite system has no stop condition. What have you built?",
    nudge: "What do you check before you apply a rule a second time?",
    choices: ["A complete philosophy", "A loop", "A proof", "A faster machine"],
    answer: 1,
    why: "Match, rewrite, stop. If you cannot say why it stops, it will not. The nested solid on that path is a stage for the lecture, not a claim about physics.",
    path: "enochian-programming",
  },
];

export function passedSet(quizzes: Record<string, { passed: boolean } | undefined>) {
  const ids = new Set<string>();
  for (const node of knowledge) {
    if (quizzes[`ks:${node.id}`]?.passed) ids.add(node.id);
  }
  return ids;
}

export function fringeOf(passed: Set<string>, domain?: Domain) {
  const list = domain ? knowledge.filter((n) => n.domain === domain) : knowledge;
  const ready = list.filter((n) => !passed.has(n.id) && n.prereqs.every((p) => passed.has(p)));
  const blocked = list.filter((n) => !passed.has(n.id) && n.prereqs.some((p) => !passed.has(p)));
  const done = list.filter((n) => passed.has(n.id));
  return { ready, blocked, done };
}
