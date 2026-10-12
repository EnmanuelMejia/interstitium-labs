# Content retrofit: IL-13 SWE Interview Foundations track (modules 1-7 of 56)
# Each entry: summary (instructor voice), concepts [(term, def)], proc_title,
# procedure [steps], project (brief body), honesty.

COURSE = "IL-13 Software Engineering Interview Prep"

M = {
"swe-interview-foundations--dsa-big-o": {
"summary": ("Welcome to Complexity Analysis — the first module of the DSA & System Design Core, the shared spine of IL-13. "
"I'm your instructor, and in this module we build the vocabulary of every technical interview: reading a solution's cost at a glance and saying it out loud without hand-waving. "
"We cover Big-O, Big-Theta, and Big-Omega; time versus space as the two axes; amortized analysis through dynamic arrays; best, average, and worst-case reasoning; and where log n and n log n come from. "
"By the end, you will state a complexity bound, the case it describes, and the dominant operation driving it — while pointing at your own code."),
"concepts": [
("Big-O", "An upper bound on growth: f(n) is O(g(n)) if f grows no faster than a constant multiple of g for large n — the worst-case language interviews expect by default."),
("Big-Theta", "A tight bound: f(n) is Theta(g(n)) when it is both O(g(n)) and Omega(g(n)) — the growth rate pinned from both sides."),
("Big-Omega", "A lower bound on growth: f(n) is Omega(g(n)) if f grows at least as fast as a constant multiple of g — how you describe best cases and optimality."),
("Time complexity", "How the number of primitive operations scales with input size n — the axis interviewers ask about first."),
("Space complexity", "How auxiliary memory scales with n — the second axis; the tradeoff partner of time in nearly every optimization discussion."),
("Amortized analysis", "Averaging a costly operation's price over a whole sequence: a dynamic array's occasional O(n) resize spreads to O(1) per append across n appends."),
("Best / average / worst case", "Three lenses on one algorithm: quicksort is O(n log n) average but O(n²) worst case on sorted input with a naive pivot — the input distribution decides which you pay."),
("Log n from halving", "Each step discards a constant fraction of the problem — binary search halves n times, so the step count is log₂ n."),
("n log n from divide-and-conquer", "Divide into halves, do linear work per level: log n levels × n work per level — mergesort's shape, and the price of comparison-based sorting."),
("Dominant operation", "The operation whose count drives the bound — saying it out loud ('the nested scan of the inner loop') is what makes a complexity answer gradable."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Pick any two solutions you have written recently and, for each, state the time and space bound aloud in one sentence — bound, case, dominant operation.",
"Re-derive log n and n log n from scratch on paper: halving for binary search, levels-times-work for mergesort, until the derivation takes under sixty seconds.",
"Take one O(n²) solution you know (e.g. a nested-loop pair search) and write the hash-map version beside it; state both complexities and the space cost of the improvement.",
"Write the dynamic-array amortized argument in your own words: total cost of n appends with doubling, divided by n — then say it aloud as you would to an interviewer.",
"Run a timed drill: read an unseen problem statement and within two minutes name the pattern, the expected complexity, and the case (best/average/worst) you are quoting.",
],
"project": ("Complexity teardown of your own code. Pick three programs or solutions you have written — one you are proud of, one you suspect is slow, "
"and one from a practice set. For each, write a one-page brief: the algorithm in two sentences, the time bound with the dominant operation named, the space bound, "
"and the best/average/worst-case split where it applies. Then propose one concrete optimization for the slowest of the three and re-state its new bounds. "
"Deliverable: three briefs plus the optimization — the exact artifacts you will narrate in a coding round."),
"honesty": ("Honest scope: complexity fluency gets you past coding rounds, but it confers no credential — this course awards no certificate and no employer "
"recognizes it as one. Interview rubrics differ by company and even by interviewer; the numbers here are practice for a human conversation, not a guarantee of an offer."),
},
"swe-interview-foundations--dsa-patterns": {
"summary": ("Welcome to Arrays, Strings, and Hashing Patterns — module 2 of the DSA & System Design Core. I'm your instructor, and this is the highest-yield "
"module in the path: the handful of patterns behind the majority of array and string questions, trained until recognition is instant. We cover two pointers "
"(same-direction and opposite-ends), fixed and variable sliding windows, hash maps for O(1) lookups, prefix sums and difference arrays, and monotonic stacks "
"and queues. By the end, you will map a novel problem to a known pattern and name its complexity within two minutes."),
"concepts": [
("Two pointers (opposite ends)", "Pointers starting at both ends of ordered data and converging — sorted two-sum, container-with-most-water — O(n) time, O(1) space."),
("Two pointers (same direction)", "Fast/slow pointers moving through one pass — cycle detection, in-place dedup — O(n) time, O(1) space."),
("Sliding window", "A window over contiguous subarrays/substrings that expands on the right and shrinks on the left while a constraint is violated — each element enters and leaves once, hence O(n)."),
("Hash map unlock", "Trading space for time: O(1) average lookups turn O(n²) pair-searches into O(n) single passes — two-sum, frequency counts, seen-sets."),
("Prefix sums", "pre[i] = sum of arr[0..i] after O(n) preprocessing, giving O(1) range sums: sum(i..j) = pre[j] − pre[i−1]."),
("Difference arrays", "Range-update companion to prefix sums: mark +v at l and −v at r+1, then one prefix pass applies all range updates in O(n + q)."),
("Monotonic stack", "A stack kept in increasing (or decreasing) order; each element is pushed and popped at most once — O(n) for next-greater-element and histogram problems that look O(n²)."),
("Monotonic queue", "A deque maintaining candidates in order for sliding-window maximum/minimum — O(n) windowed extremes without rescanning."),
("Pattern recognition", "The interview skill this module trains: mapping an unseen problem to a known pattern under time pressure, then executing the template cleanly."),
("Fixed vs variable windows", "Fixed: the window size is given (max sum of k). Variable: the size adapts to a constraint (longest substring without repeats) — shrink the left edge while violated."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"For each of the five core patterns, write the 10-line template from memory (window loop, two-pointer loop, prefix build, hash-map single pass, monotonic stack) until it is mechanical.",
"Take one unseen array problem and run the recognition drill: read the prompt, name the pattern aloud in under two minutes, state the expected complexity, then code it.",
"Solve two-sum three ways — brute force O(n²), sorted two-pointer O(n log n), hash map O(n) — and narrate the space-for-time tradeoff for each, as if an interviewer asked 'can you do better?'",
"Build a prefix-sum array by hand on a 6-element array, then answer three range-sum queries from it without rescanning — verify each against a brute-force sum.",
"Do a timed set: five problems, 20 minutes each, pattern-first. Log every miss as 'pattern seen late' or 'template fumbled' — that log is your next drill list.",
],
"project": ("Pattern atlas. Build a one-page reference you will actually use: for each pattern (two pointers, sliding window, hash map, prefix sums, monotonic stack/queue), "
"write the recognition trigger ('sorted + pairs' → opposite-ends two pointers), the template in your language, the complexity, and one canonical problem it solves. "
"Then validate the atlas: solve one unseen problem per pattern using only your atlas, timed at 20 minutes each. Deliverable: the atlas plus five solved write-ups naming where the atlas helped and where it didn't."),
"honesty": ("Honest scope: patterns are recognition tools, not a guarantee — interviewers write problems designed to resist template-matching, and this course confers no "
"certificate. Fluency here buys composure for the novel problems; it does not replace the thinking the novel problems require."),
},
"swe-interview-foundations--dsa-trees-graphs": {
"summary": ("Welcome to Trees, Graphs, and Recursion — module 3 of the DSA & System Design Core. I'm your instructor, and here we take the mystique out of "
"non-linear structures: recursion with explicit base cases and call-stack costs, tree traversals, the BST invariant, heaps and priority queues, and graph "
"representations with the BFS/DFS decision reflex every interview expects. By the end, you will write clean recursive solutions, choose adjacency lists by "
"default, and justify heap versus sort in one sentence."),
"concepts": [
("Recursion contract", "Base case first, then the recursive step's promise: 'assume it works for n−1, here is how I build n' — plus the call-stack cost: depth × frame size."),
("Pre-order traversal", "Visit node, then children — natural for copying trees and prefix expressions."),
("In-order traversal", "Left, node, right — yields sorted order on a BST; the traversal that proves the invariant."),
("Post-order traversal", "Children before the node — natural for deletion and bottom-up computations like subtree heights."),
("BST invariant", "Left subtree < node < right subtree at every node — buys O(log n) search/insert/delete when balanced; degenerate insertion order gives O(n) without balancing."),
("Heap", "A complete binary tree with the heap property: min or max at the root, push/pop in O(log n), peek in O(1) — for repeated access to the extreme, not full order."),
("Adjacency list", "The default interview graph representation: O(V+E) memory with fast neighbor iteration — the right choice for sparse graphs, which interview graphs are."),
("BFS", "Level-order exploration with a queue — shortest path in unweighted graphs, because the first visit to a node is via the fewest edges."),
("DFS", "Depth-first exploration with a stack or recursion — cycle detection, topological sort, connected components; watch the recursion depth."),
("Priority queue", "The abstract interface heaps implement: repeated min/max extraction — top-k, merge-k-sorted, streaming medians."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write in-order, pre-order, and post-order traversals from memory on a 7-node tree drawn on paper, then verify each against a hand simulation.",
"Implement a BST insert and search; then insert the sorted keys 1..n and observe the degeneration to O(n) — state aloud why balancing matters.",
"Solve one BFS problem (shortest path) and one DFS problem (cycle or component count) back to back, stating the representation choice ('adjacency list, sparse graph') before coding.",
"Implement top-k with a min-heap of size k and narrate the justification: 'I need repeated access to the extreme, not a full sort.'",
"Run the recursion drill: for any recursive solution, write the base case, the contract sentence, and the stack-depth bound before writing a single line of code.",
],
"project": ("Traversal and graph toolkit. Build a small library in your language: iterative and recursive traversals, BST insert/search with an invariant checker, "
"a binary heap with push/pop, and BFS/DFS over adjacency lists. For each, include a one-paragraph docstring stating when to use it and its complexity. "
"Then apply it: solve two tree problems and two graph problems using only your toolkit, and write a debrief on where the toolkit's shape helped or hindered. "
"Deliverable: the toolkit plus four solved write-ups."),
"honesty": ("Honest scope: traversal fluency and the BFS/DFS reflex are table stakes, not a differentiator — interviewers score the reasoning around the code, "
"and this course confers no certificate. The toolkit is practice equipment; the graded artifact is how you think aloud while using it."),
},
"swe-interview-foundations--dsa-dynamic": {
"summary": ("Welcome to Dynamic Programming — module 4 of the DSA & System Design Core. I'm your instructor, and this is the module most candidates skip and "
"most offers require. We demystify DP into a repeatable method: recurrence first, then memoization versus tabulation, the 1D ladder (climbing stairs, house "
"robber), knapsack and subset patterns, and DP on strings (LCS, edit distance). By the end, you will define the state, write the recurrence, and name the "
"overlapping subproblems before you write code — because interviewers score the recurrence, and the code is transcription."),
"concepts": [
("Overlapping subproblems", "The property that makes DP valid: the same subproblems recur, so caching their results beats recomputation — the precondition you must name before memoizing."),
("Optimal substructure", "The optimal solution is built from optimal solutions to subproblems — the property that makes a recurrence correct."),
("Recurrence", "The decision equation — dp[i] = max(skip, take) — written in words before code; the single most-scored line of a DP answer."),
("Memoization", "Top-down DP: recursion plus a cache — natural to write, pays recursion overhead and risks stack depth."),
("Tabulation", "Bottom-up DP: iterate the table directly — no stack risk, often better constants; the same complexity as memoization, different direction."),
("State design", "Choosing what the state captures: exactly the information future decisions need — too little and the recurrence can't decide, too much and the table explodes."),
("1D DP ladder", "The progression: climbing stairs (dp[i] = dp[i−1] + dp[i−2]) → house robber (add skip-or-take) → harder 1D problems — every 1D DP is a variation on the ladder."),
("0/1 knapsack", "'Choose a subset under a capacity to maximize value': dp[i][w] = max(skip, take) — the skeleton behind partition, coin change, and target-sum."),
("LCS / edit distance", "The 2D prefixes-table skeleton: dp[i][j] from dp[i−1][j], dp[i][j−1], dp[i−1][j−1]; match extends the diagonal, mismatch takes the best neighbor."),
("State compression", "Keeping only the rows or values the recurrence actually reads — the follow-up optimization after the table version works."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"For any DP problem, write the recurrence in English first ('dp[i] = best value considering the first i items'), then the state definition, then code — never code first.",
"Climb the 1D ladder in order: climbing stairs, then house robber, then one harder 1D variant — stating each recurrence aloud before coding.",
"Solve one knapsack-family problem by naming the disguise aloud: 'this is 0/1 knapsack on capacity W' — then write dp[i][w] = max(skip, take).",
"Solve one string DP with the prefixes table: define dp[i][j] on the two prefixes, fill a small table by hand for 3×3 inputs, then code it.",
"Redo one problem both ways — memoized top-down and tabulated bottom-up — and state the tradeoff: recursion overhead versus iteration, same asymptotic cost.",
],
"project": ("DP playbook. Write a five-page playbook: the recurrence-first method, the 1D ladder with worked recurrences, the knapsack recognition checklist, "
"the prefixes-table skeleton for string DP, and the state-design questions you ask yourself ('what must the state remember?'). Validate it: solve six unseen "
"DP problems using only the playbook, logging where the recurrence came easily and where state design stalled you. Deliverable: the playbook plus six solved "
"write-ups with the stall log."),
"honesty": ("Honest scope: DP is the most grind-gated topic in the core — recognition comes from reps, and no module confers a certificate. The playbook compresses "
"the method, not the practice; interviewers will still hand you problems you have never seen, which is the point of the method."),
},
"swe-interview-foundations--sysdesign-core": {
"summary": ("Welcome to System Design Fundamentals — module 5 of the DSA & System Design Core. I'm your instructor, and this module treats the system-design "
"interview as a skill, not a memorization exercise: scoping with functional and non-functional requirements, back-of-envelope estimation, load balancers, caches, "
"and CDNs, the honest SQL-versus-NoSQL choice, and CAP theorem discussed as a real tradeoff rather than a recited textbook. By the end, you will walk the "
"standard interview walkthrough — requirements, estimation, API, data, scaling, failure modes, tradeoffs — with estimation math you can defend."),
"concepts": [
("Functional requirements", "What the system does — the features and behaviors; stated first, before any box is drawn."),
("Non-functional requirements", "How the system behaves — scale, latency, availability, consistency; the constraints that shape the architecture."),
("Back-of-envelope estimation", "Order-of-magnitude math with stated assumptions: users → QPS → storage → bandwidth, rounded aggressively to drive design decisions."),
("Load balancer", "Spreads traffic across healthy servers — placed first along the request path; health checks decide 'healthy'."),
("Cache", "Serves hot data without hitting the origin — Redis/Memcached; the invalidation story is the real design work."),
("CDN", "Pushes static content to edge locations near users — latency for cacheable bytes, offload for the origin."),
("CAP theorem", "Under a network partition, choose consistency or availability — partitions are a fact; CP or AP is the decision, argued from the product's needs."),
("Consistency models", "The spectrum from strong to eventual: who sees what, when — 'the feed can be eventually consistent, but payments cannot.'"),
("Access patterns", "How data is read and written — the honest deciding factor in SQL versus NoSQL, not hype or habit."),
("Bottleneck-first design", "Designing toward the constraint the estimation reveals: shard the hot key, cache the hot read, CDN the static bytes."),
],
"proc_title": "Worked estimation",
"procedure": [
"Work the canonical estimation: 100M daily users × 10 requests each = 10⁹ requests/day ÷ 86,400 ≈ 12k average QPS — write every step, state the rounding, name the peak multiplier assumption.",
"Estimate storage for a photo-sharing sketch: 10M uploads/day × 2 MB average = 20 TB/day; × 365 × retention years — then decide what the number forces (object storage, CDN, thumbnails).",
"Estimate bandwidth for a video feed: concurrent viewers × bitrate — convert to Gbps and state what breaks first (origin egress, cache hit ratio).",
"Take any estimation above and change one assumption (DAU doubles, retention triples); recompute and name which design decision flips.",
"Practice the estimation monologue: 5 minutes, assumptions stated aloud, driving toward one decision ('so we shard by user id') — the interview shape of this skill.",
],
"project": ("Design-brief portfolio piece. Pick one familiar product (a URL shortener, a pastebin, a notification feed) and write a two-page design brief: "
"functional and non-functional requirements, back-of-envelope estimation with every assumption stated, the architecture sketch (LB → app → cache → DB, CDN at the edge), "
"the SQL-versus-NoSQL decision argued from access patterns, the CAP choice argued from the product, and three failure modes with mitigations. Deliverable: the brief — "
"the artifact you will adapt live in the design round."),
"honesty": ("Honest scope: system-design rounds are the most subjective interviews in the loop — there is no single correct architecture, and this course confers no "
"certificate. Estimation is order-of-magnitude judgment, not precision; interviewers score the reasoning chain and the tradeoffs, not the arithmetic."),
},
"swe-interview-foundations--sysdesign-build": {
"summary": ("Welcome to the Guided System Design Build — module 6 of the DSA & System Design Core. I'm your instructor, and here we convert design knowledge "
"into interview performance: three full design reps — a URL shortener, a rate limiter, and a notification service — each with docs and a timer, plus the one-page "
"design doc and the 45-minute presentation cadence. By the end, you will have presented a design on camera with timeboxes you actually kept, and a doc an "
"interviewer could build from."),
"concepts": [
("URL shortener design", "The canonical rep: requirements, API (POST /shorten, GET /{id} → 301), ID generation (counter vs hash, base62), key-value storage, cache hot URLs, shard by hash."),
("Rate limiter design", "Token bucket for bursts versus leaky bucket for smoothing; distributed state in Redis with Lua for atomicity; 429 + RateLimit-* headers communicating limits."),
("Notification service design", "Channels (push/email/SMS), fan-out estimation, queue-based workers per channel with retries and dead-letter queues, templates, provider rate limits, idempotency."),
("One-page design doc", "Requirements, architecture sketch, API and data model, scaling math, failure modes, open tradeoffs — one page forces decisions."),
("45-minute cadence", "5 requirements, 5 estimation, 10 API/data, 15 deep-dive on the hard part, 10 tradeoffs and failures — the timebox that proves you can drive."),
("Review rubric", "Fixed axes for judging designs — comparable, complete feedback that prevents reviews from fixating on one pet concern."),
("ID generation tradeoffs", "Counter (needs coordination, e.g. ZooKeeper-style ranges) versus hash (collision handling) — the classic 'hard part' deep-dive of the shortener."),
("Fan-out math", "Followers × messages: the estimation that decides push versus pull and queue depth for the notification service."),
],
"proc_title": "Worked estimation",
"procedure": [
"Design the URL shortener on paper: requirements, 100M URLs/month estimation (writes/sec, storage for 5 years at ~500 bytes/record), then the full walkthrough — time it at 45 minutes.",
"Work the shortener's ID math: 7 base62 characters = 62⁷ ≈ 3.5 trillion IDs — state how long that lasts at your write rate and what happens at exhaustion.",
"Design the rate limiter: 10k requests/sec per API key, burst allowance 2× — size the Redis state, choose token bucket, and write the Lua atomicity argument.",
"Design the notification service: 1M notifications/day across three channels — fan-out math, worker count from per-worker throughput, queue depth for a 10× spike.",
"Record yourself presenting one design in 45 minutes; watch it back with the rubric and log every timebox you broke and every tradeoff you failed to name.",
],
"project": ("Three documented designs. Produce the full artifacts: one-page design docs for the URL shortener, the rate limiter, and the notification service — each with "
"requirements, estimation, architecture, API/data model, scaling math, failure modes, and open tradeoffs — plus a 45-minute recorded walkthrough of one of them. "
"Peer-review (or self-review with the rubric) all three. Deliverable: three design docs and one recording with the rubric scores — your design-round portfolio."),
"honesty": ("Honest scope: three guided designs do not make you a distributed-systems engineer — they make you practiced at the interview's design genre, which is a "
"different and narrower skill, and this course confers no certificate. Real systems have constraints (org, cost, legacy) the interview hand-waves; name that gap when you feel it."),
},
"swe-interview-foundations--swe-mock-circuit": {
"summary": ("Welcome to the Mock Interview Circuit — the final module of the DSA & System Design Core. I'm your instructor, and this module treats the interview "
"as a performance discipline: timed coding rounds with a stranger, system-design rounds on camera, the STAR behavioral ledger, the debrief template that names "
"what leaked and what held, weak-spot triage after every mock, and the final two-week taper plan. By the end, the real loop will be the second time you have done "
"it — not the first."),
"concepts": [
("Timed coding bar", "The 30-minute shape: 5 clarify + plan, 20 code, 5 test — brute force stated first buys time and shows honesty; a working brute force beats a half-written optimal."),
("Design round walkthrough", "Requirements → estimation → API → data model → happy path → scaling → failure modes → tradeoffs — with the interviewer as collaborator, not examiner."),
("STAR", "Situation (2 sentences), Task (your responsibility), Action (what YOU did — the bulk), Result (measurable outcome + lesson) — a complete evidence unit per story."),
("Behavioral ledger", "Your running record: story bank, which stories you told where, feedback received, questions that stumped you — no repeated stories, every round becomes training data."),
("Debrief template", "Within an hour of a mock: what leaked, what held, the single biggest leak, and the 48-hour redrill plan — mocks without debriefs are stage-fright practice."),
("Weak-spot triage", "Rank leaks by frequency × interview weight — fix what costs the most points most often; expected-value studying."),
("Taper plan", "Final two weeks: no new material, redrill weak patterns from the debrief log, full timed mocks, sleep fixed, story bank rehearsed aloud."),
("Thinking aloud", "Verbalized reasoning is scorable reasoning — narrating complexity, tradeoffs, and the plan as you code turns silent work into graded evidence."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Book or simulate one timed coding mock (30 minutes, stranger or recording): run the 5/20/5 budget aloud, state complexity before optimizing, test at the end.",
"Run one system-design mock on camera (45 minutes): drive the walkthrough, treat the interviewer as collaborator, end with three tradeoffs you would revisit.",
"Write your STAR ledger: five stories in full STAR form, each with the measurable result and the lesson — rehearse two aloud until they fit in two minutes.",
"Within one hour of each mock, fill the debrief template: what leaked, what held, the single biggest leak ranked by frequency × weight, the 48-hour redrill.",
"Execute the taper in miniature: one week of no-new-material redrills from your debrief log, then a full timed mock — measure the leak count before and after.",
],
"project": ("Mock circuit portfolio. Run a four-mock circuit over two weeks: two coding rounds, one system-design round, one behavioral round — each with a partner or on camera. "
"For each, produce the debrief (leaks, holds, biggest leak, redrill plan) and the updated STAR ledger. Close the circuit with the taper plan written for your real loop dates. "
"Deliverable: four debriefs, the ledger, and the taper schedule — the paper trail that proves the loop is your second time, not your first."),
"honesty": ("Honest scope: mocks are the closest simulation available, not the real thing — real interviewers, nerves, and stakes differ, and this course confers no certificate. "
"A taper improves performance; it does not guarantee an offer. What the circuit honestly buys is the removal of surprise — which is most of what sinks first attempts."),
},
}
