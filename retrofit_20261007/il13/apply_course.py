"""STEP 3+4: retrofit IL-13 course file modules to template shape + course-level keys."""
import json, importlib.util, copy

BASE = "/home/hatch/workspace/apex-audit"
CF = BASE + "/docs/university/data/courses/il-13-software-engineering-interview-prep.json"
CDIR = BASE + "/retrofit_20261007/il13"

t = json.load(open(CF))
print("loaded course, modules:", len(t["modules"]))

allc = {}
for f in ["content_swe", "content_backend", "content_frontend", "content_fullstack",
          "content_ios", "content_android", "content_embedded_qa"]:
    spec = importlib.util.spec_from_file_location(f, CDIR + "/" + f + ".py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    allc.update(mod.M)
assert len(allc) == 56, len(allc)

def concepts_body(pairs):
    return "\n".join("- **%s** — %s" % (term, dfn) for term, dfn in pairs)

def proc_body(c):
    intro = {
        "Hands-on procedure": "Work this module the way the interview tests it — hands on, timed, and narrated aloud. Follow the sequence below in order; each step builds the next.",
        "Worked estimation": "Estimation is order-of-magnitude judgment with stated assumptions, narrated aloud. Work each estimation below on paper, stating every assumption before the arithmetic.",
    }[c["proc_title"]]
    steps = "\n".join("%d. %s" % (i + 1, s) for i, s in enumerate(c["procedure"]))
    return intro + "\n\n" + steps

thin_before = []
for m in t["modules"]:
    mid = m["id"]
    c = allc[mid]
    if len(m.get("notes", [])) < 4 or len(m.get("cards", [])) < 5 or len(m.get("quiz", [])) < 4:
        thin_before.append(mid)
    m["summary"] = c["summary"]
    m["notes"] = [
        {"title": "Concepts", "body": concepts_body(c["concepts"])},
        {"title": c["proc_title"], "body": proc_body(c)},
        {"title": "Project brief", "body": c["project"]},
        {"title": "Honesty note", "body": c["honesty"]},
    ]
    # validate module quiz/cards schema (preserved as-is)
    assert len(m["cards"]) >= 5, mid
    for card in m["cards"]:
        assert card.get("front") and card.get("back"), mid
    assert len(m["quiz"]) >= 4, mid
    for q in m["quiz"]:
        assert isinstance(q.get("choices"), list) and len(q["choices"]) == 4, mid
        assert isinstance(q.get("answer"), int) and 0 <= q["answer"] <= 3, mid
        assert q.get("explain"), mid
        assert q.get("q"), mid

print("thin modules retrofitted:", len(thin_before))

# ---------- course-level ----------
# priorities: add missing tracks for consistency with battlePlan
labels = {p["label"] for p in t["priorities"]}
for label, minutes in [("iOS Engineering Interview Prep", 3000),
                       ("Android Engineering Interview Prep", 3000),
                       ("Software Testing & QA Interview Prep", 3000)]:
    if label not in labels:
        t["priorities"].append({"label": label, "minutes": minutes})

# mockTasks: extend to 24 (3 per track), reusing existing module quiz content
existing_ids = {m["id"] for m in t["mockTasks"]}
new_mocks = [
    ("il-13-mock-17", "choice", "@MainActor on a class guarantees:",
     ["Its methods run on the main thread \u2014 safe for UI work",
      "It runs faster", "It never blocks", "It avoids all crashes"], 0,
     "The compiler enforces the hop: UI-touching code can\u2019t accidentally run elsewhere."),
    ("il-13-mock-18", "choice", "StateFlow suits UI state because:",
     ["It is faster than LiveData",
      "It always holds the latest value and replays it to new collectors",
      "It never emits", "It works without coroutines"], 1,
     "New collectors (e.g. after rotation) immediately get current state \u2014 no missed updates."),
    ("il-13-mock-19", "choice", "Priority inheritance fixes inversion by:",
     ["Killing the low-priority task",
      "Temporarily boosting the lock holder to the blocked high-priority task\u2019s level",
      "Disabling preemption", "Raising all priorities"], 1,
     "The holder can\u2019t be preempted by medium-priority tasks anymore, so it releases the lock promptly."),
    ("il-13-mock-20", "choice", "p99 latency of 2s means:",
     ["Average latency is 2s", "99% of requests were faster than 2s \u2014 1% were slower",
      "2% of requests failed", "The server timed out"], 1,
     "Percentiles describe the distribution\u2019s tail: p99 is the near-worst case users feel."),
    ("il-13-mock-21", "choice", "The most robust way to handle duplicate deliveries is:",
     ["Exactly-once infrastructure everywhere",
      "Idempotent consumers, so reprocessing is safe",
      "Never retrying", "Bigger queues"], 1,
     "Duplicates are inevitable in distributed systems; idempotency makes them harmless."),
    ("il-13-mock-22", "choice", "The 0/1 knapsack decision at each item is:",
     ["Take it or skip it, respecting remaining capacity",
      "Always take it", "Take a fraction of it", "Sort by weight first"], 0,
     "The 0/1 constraint forces a binary choice per item: dp[i][w] = max(skip, take)."),
    ("il-13-mock-23", "choice", "useCallback\u2019s purpose is:",
     ["Memoizing expensive computations",
      "Preserving function identity across renders so memoized children don\u2019t re-render",
      "Replacing useMemo", "Avoiding hooks"], 1,
     "A new function identity each render defeats memo on children; useCallback stabilizes it."),
    ("il-13-mock-24", "choice", "PKCE exists to protect:",
     ["Servers with weak passwords",
      "Public clients (mobile/SPA) that can\u2019t keep a secret \u2014 the code exchange is bound to the challenger",
      "JWT signatures", "Database credentials"], 1,
     "Without a client secret, PKCE\u2019s code_verifier/code_challenge pair prevents authorization-code interception."),
]
for mid, typ, q, choices, answer, explain in new_mocks:
    assert mid not in existing_ids, mid
    assert len(choices) == 4 and 0 <= answer <= 3 and explain and q
    t["mockTasks"].append({"id": mid, "type": typ, "q": q, "choices": choices,
                           "answer": answer, "explain": explain})

# cheatSheets: add 4 track survival sheets -> 8 total
t["cheatSheets"].append({
    "title": "Swift & iOS survival sheet",
    "blocks": [
        {"h": "Optionals", "body": "Bind (if let/guard let) over force-unwrapping; chain for deep access; nil-coalesce for defaults.", "code": "guard let user = response.user else { return }\nlet name = user.profile?.name ?? \"Guest\"", "lang": "swift"},
        {"h": "Value vs reference", "body": "Struct by default (value semantics); class when identity or inheritance is required.", "code": "struct Point { var x, y: Double } // copied\nclass Store: ObservableObject { } // shared", "lang": "swift"},
        {"h": "Concurrency rules", "body": "UI on main (@MainActor); work off main; actors for isolated mutable state; children can\u2019t outlive parents.", "code": "@MainActor\nfunc refresh() async {\n    let items = await loader.fetch() // off-main\n    self.items = items               // main\n}", "lang": "swift"},
        {"h": "Persistence ladder", "body": "UserDefaults: preferences. Codable files: documents. Core Data/SwiftData: queryable. Keychain: secrets.", "code": "", "lang": ""},
    ]})
t["cheatSheets"].append({
    "title": "Kotlin & Android survival sheet",
    "blocks": [
        {"h": "Null safety", "body": "?. safe calls, ?: Elvis, let scoping; !! only with proof. Platform types from Java: defend at boundaries.", "code": "val name = user?.profile?.name ?: \"Guest\"\nval len = text?.let { it.length } ?: 0", "lang": "kotlin"},
        {"h": "UI state", "body": "Sealed hierarchies (Loading/Success/Error) with exhaustive when; StateFlow holds latest and replays.", "code": "sealed interface UiState {\n  data object Loading : UiState\n  data class Ready(val items: List<Item>) : UiState\n}", "lang": "kotlin"},
        {"h": "Coroutines", "body": "suspend pauses without blocking; viewModelScope dies with the ViewModel; Dispatchers.Main/IO/Default chosen explicitly.", "code": "viewModelScope.launch {\n  val items = withContext(Dispatchers.IO) { repo.load() }\n  _state.value = UiState.Ready(items)\n}", "lang": "kotlin"},
        {"h": "Persistence ladder", "body": "DataStore: settings. Room: relational (compile-checked DAO). Scoped storage: files. Keystore: secrets.", "code": "", "lang": ""},
    ]})
t["cheatSheets"].append({
    "title": "Embedded C & RTOS survival sheet",
    "blocks": [
        {"h": "volatile", "body": "For MMIO registers and ISR-shared flags: no cached reads, no elided accesses. Not a substitute for atomics.", "code": "#define STATUS (*(volatile uint32_t*)0x40001000)\nwhile ((STATUS & READY) == 0) { /* wait */ }", "lang": "c"},
        {"h": "Memory", "body": "Stack: tiny, fast. Heap: usually banned. Static: the default \u2014 worst-case RAM known at link time.", "code": "static uint8_t pool[POOL_SIZE]; // not malloc", "lang": "c"},
        {"h": "ISR rules", "body": "Short, no blocking, no heap: set a flag or push to a queue; the task does the work.", "code": "", "lang": ""},
        {"h": "Priority inversion", "body": "Low holder + medium preempter = high task waits unboundedly. Fix: priority inheritance (RTOS mutexes).", "code": "", "lang": ""},
    ]})
t["cheatSheets"].append({
    "title": "QA automation survival sheet",
    "blocks": [
        {"h": "Pyramid", "body": "Many fast units, fewer integration, few e2e. Each layer tests what only it can prove.", "code": "", "lang": ""},
        {"h": "Page objects", "body": "One class per page; selectors in exactly one file per screen; tests read as user intent.", "code": "test('login', async ({ page }) => {\n  await loginPage.loginAs(user); // intent, not selectors\n});", "lang": "javascript"},
        {"h": "Flaky triage", "body": "Quarantine first; classify (timing/order/environment/real bug); fixed or quarantined \u2014 never tolerated.", "code": "", "lang": ""},
        {"h": "k6 gate", "body": "Thresholds turn load tests into gates: p95 and error-rate assertions fail the run.", "code": "export const options = {\n  thresholds: { http_req_duration: ['p(95)<500'], http_req_failed: ['rate<0.01'] },\n};", "lang": "javascript"},
    ]})

# answerBank: add 2 -> 9 total
t["answerBank"].append({
    "q": "Walk me through how you debug a tough production bug.",
    "a": "State the stakes fast, then narrate hypotheses tested \u2014 not a heroic montage. Name the tools per step (logs for what happened, traces for where, debugger/watchpoints for state), include the wrong turns honestly, and land the lesson plus what changed afterward. War stories score on method and honesty."})
t["answerBank"].append({
    "q": "Tell me about a time you disagreed with a technical decision.",
    "a": "Use STAR: the situation in two sentences, your responsibility, what YOU did (raised the concern with the tradeoff analysis, proposed the alternative with its costs), and the measurable result plus the lesson. Interviewers score evidence of behavior \u2014 make your decisions explicit, and show you can disagree and commit."})

# honestyNote: interview-appropriate
t["honestyNote"] = ("Preparation only \u2014 this course confers no certificate and is not affiliated with any employer or interview-prep provider. "
                    "Interview rubrics vary by company and interviewer; the mocks and drills here simulate the format, they do not guarantee offers.")

# mockMinutes sanity
assert isinstance(t["mockMinutes"], int), t["mockMinutes"]

# sourceLinks: ensure retrieved dates present
for s in t["sourceLinks"]:
    assert s.get("name") and s.get("url") and s.get("retrieved"), s

with open(CF, "w") as f:
    json.dump(t, f, indent=1, ensure_ascii=False)
    f.write("\n")

t2 = json.load(open(CF))
assert len(t2["modules"]) == 56
for m in t2["modules"]:
    assert [n["title"] for n in m["notes"]] == ["Concepts", m["notes"][1]["title"], "Project brief", "Honesty note"], m["id"]
    assert m["summary"].startswith("Welcome to") and "I'm your instructor" in m["summary"], m["id"]
print("course written + validated")
print("priorities:", len(t2["priorities"]), "mockTasks:", len(t2["mockTasks"]),
      "cheatSheets:", len(t2["cheatSheets"]), "answerBank:", len(t2["answerBank"]))
