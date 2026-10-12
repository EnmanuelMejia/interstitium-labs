module = {
  "id": "IL28-M18",
  "code": "IL-28",
  "title": "Python Fundamentals: Script-Reading Mastery",
  "summary": "Build rock-solid Python reading fluency — types, control flow, functions, comprehensions, and file I/O — through original predict-the-output drills in the spirit of the panel's script-reading exercise, so you can trace any automation script cold.",
  "objectives": [
    "Predict the exact console output of short Python scripts covering loops, conditions, and data structures.",
    "Distinguish mutable from immutable types and explain aliasing bugs.",
    "Write and read list, dict, and set comprehensions with filters.",
    "Use functions with default, *args, and **kwargs parameters correctly.",
    "Read and parse text files safely with context managers and string methods."
  ],
  "notes": [
    {
      "title": "Dynamic typing and the mutable/immutable divide",
      "body": """Python variables are names bound to objects, not typed boxes — the same name can point at an int, then a string, then a list. What matters for bugs is whether the object itself can change in place. Immutable types (int, float, str, tuple) never change: operations on them create new objects. Mutable types (list, dict, set) can be modified through any name pointing at them, which is the classic aliasing trap. Worked example:

a = [1, 2, 3]
b = a
b.append(4)
print(a)

Solution: this prints [1, 2, 3, 4] — not [1, 2, 3]. The assignment b = a copies the reference, not the list, so both names point at the same object and the append is visible through a. The fix is an explicit copy: b = a.copy() or b = list(a). Contrast with strings:

s = "web"
t = s
t = t + "1"
print(s)

Solution: prints \"web\" — concatenation built a new string object and rebound only t. In DevOps scripts this divide bites when a function mutates a list or dict passed in by the caller: the caller's data changes silently. Default to copying inputs you intend to transform, and treat any shared mutable structure as suspect until proven otherwise."""
    },
    {
      "title": "Control flow: loops, break, continue, and the loop-else",
      "body": """Python's for loop iterates over any iterable, while while loops on a condition — but the panel-relevant subtleties are break, continue, and the rarely taught else clause on loops. break exits the loop immediately; continue skips to the next iteration; the else block after a loop runs only if the loop finished without hitting break. Worked example — scanning hosts for the first failure:

hosts = [\"web1\", \"web2\", \"web3\"]
status = {\"web1\": \"up\", \"web2\": \"down\", \"web3\": \"up\"}
for h in hosts:
    if status[h] == \"down\":
        print(\"first failure:\", h)
        break
else:
    print(\"all healthy\")

Solution: prints \"first failure: web2\" and the else never runs, because break fired. If every host were \"up\", the loop would complete and print \"all healthy\". Worked example two — continue filters without nesting:

for code in [200, 500, 200, 503]:
    if code == 200:
        continue
    print(\"alert on\", code)

Solution: prints \"alert on 500\" then \"alert on 503\" — the 200s are skipped before the print. Read continue as \"skip the rest of this round\" and break as \"stop looping entirely,\" and always check whether a loop has an else before predicting output — panels love hiding the else in plain sight."""
    },
    {
      "title": "Functions: parameters, defaults, *args, **kwargs",
      "body": """A Python function signature can mix positional parameters, defaults, *args (extra positionals collected into a tuple), and **kwargs (extra keywords collected into a dict). The caller's arguments bind left to right, and anything unmatched spills into *args/**kwargs. Worked example:

def deploy(service, env=\"staging\", *flags, **opts):
    print(service, env, flags, opts)

deploy(\"api\", \"prod\", \"--force\", \"--dry-run\", timeout=30)

Solution: prints \"api prod ('--force', '--dry-run') {'timeout': 30}\". The walkthrough: service binds \"api\", env binds \"prod\" (overriding the default), the two leftover positional strings collect into flags as a tuple, and timeout=30 collects into opts as a dict. Two rules panels probe. First, defaults are evaluated once at function definition time — a mutable default like def f(x=[]) shares one list across all calls, so the idiom is def f(x=None): followed by x = x or []. Second, return ends the function immediately and a bare return (or falling off the end) yields None — code after a return never runs, which is a favorite predict-output trap. When reading a call, always map each argument to its parameter before tracing the body; most script-reading errors come from misbinding, not from misunderstanding the loop."""
    },
    {
      "title": "Comprehensions: dense, readable data transformation",
      "body": """Comprehensions build lists, dicts, and sets in a single expression: [expression for item in iterable if condition]. They are the idiomatic way DevOps scripts filter inventories, parse ports, and reshape API responses. Worked example — filter an inventory to production web hosts:

hosts = [
    {\"name\": \"web1\", \"env\": \"prod\"},
    {\"name\": \"web2\", \"env\": \"staging\"},
    {\"name\": \"db1\",  \"env\": \"prod\"},
]
prod_webs = [h[\"name\"] for h in hosts if h[\"env\"] == \"prod\" and h[\"name\"].startswith(\"web\")]
print(prod_webs)

Solution: prints ['web1']. Walkthrough: web1 passes both tests (prod and name starts with \"web\"); web2 fails the env test; db1 fails the name test. Worked example two — a dict comprehension counting by key:

codes = [200, 500, 200, 503, 500, 200]
counts = {c: codes.count(c) for c in set(codes)}
print(counts)

Solution: prints {200: 3, 500: 2, 503: 1} in some order (set iteration order is not guaranteed — never assert an order for set-derived output). Read a comprehension inside-out: the for clause first, then the if filter, then the output expression. If a comprehension gets too clever to read at a glance, panels consider rewriting it as a plain loop a sign of maturity, not weakness."""
    },
    {
      "title": "File I/O: context managers and line parsing",
      "body": """Real DevOps Python reads logs, inventories, and config files — always with the with statement, which closes the file even if an exception fires. Worked example — parse a simple status file where each line is \"hostname,status\":

with open(\"hosts.txt\") as f:
    down = []
    for line in f:
        name, state = line.strip().split(\",\")
        if state == \"down\":
            down.append(name)
print(down)

Given hosts.txt containing \"web1,up\\nweb2,down\\nweb3,up\\n\", the solution prints ['web2']. Walkthrough: strip() removes the trailing newline (without it, the last field would be \"down\\n\" and the comparison would fail — the single most common file-parsing bug), split(\",\") unpacks into two names, and only web2 matches. Three professional habits: iterate the file object directly (never readlines() on a log that might be gigabytes), always strip() before splitting or comparing, and wrap parsing in try/except ValueError when the input is untrusted — a malformed line should be logged and skipped, not crash a 3 a.m. remediation script. For writing, the same with pattern applies: with open(\"out.txt\", \"w\") as f: — and remember \"w\" truncates, so double-check the path before running."""
    },
    {
      "title": "Strings, f-strings, and the gotchas panels love",
      "body": """String handling is where script-reading exercises separate fluent readers from guessers. F-strings embed expressions: f\"{name}-{i:02d}\" formats i as two digits with a leading zero. str.split(), strip(), startswith(), and join() do most parsing work. Worked example:

parts = \"prod,us-east,api\".split(\",\")
print(\"-\".join(parts))
print(parts[1].upper())

Solution: prints \"prod-us-east-api\" then \"US-EAST\". Walkthrough: split(\",\") gives ['prod', 'us-east', 'api'], join glues them with dashes, and upper() returns a new string (strings are immutable — upper() never changes parts in place). Now the famous gotcha, which panels ask about directly:

def add_host(host, inventory=[]):
    inventory.append(host)
    return inventory

print(add_host(\"web1\"))
print(add_host(\"web2\"))

Solution: prints ['web1'] then ['web1', 'web2'] — the default list is created once at definition time and shared across calls. The fix: def add_host(host, inventory=None): then inventory = inventory if inventory is not None else []. When tracing any script, flag every mutable default, every in-place mutation of a shared object, and every string method (which always returns new) — those three checks catch the majority of predict-output traps."""
    }
  ],
  "cards": [
    {"front": "Why does b = a; b.append(4) also change a when a is a list?", "back": "Assignment copies the reference, not the object — both names point at the same mutable list. Use a.copy() or list(a) for an independent copy."},
    {"front": "When does the else clause of a for loop execute?", "back": "Only if the loop completes without hitting break. If break fires, the else is skipped."},
    {"front": "In def f(a, b='x', *args, **kwargs), where do extra positional and keyword arguments go?", "back": "Extra positionals collect into args as a tuple; extra keywords collect into kwargs as a dict."},
    {"front": "What is wrong with def add(host, inventory=[]) ?", "back": "The default list is created once at definition time and shared across calls — appends accumulate. Use inventory=None and create the list inside."},
    {"front": "What does [h['name'] for h in hosts if h['env'] == 'prod'] do?", "back": "Builds a list of host names filtered to production — a list comprehension: for-clause, if-filter, output expression."},
    {"front": "Why must you strip() lines when parsing a text file?", "back": "Lines end with '\\n'; without strip(), the last field compares as 'down\\n' instead of 'down' and matches fail."},
    {"front": "What does the with statement guarantee for file I/O?", "back": "The file is closed automatically even if an exception is raised inside the block."},
    {"front": "What does f\"{i:02d}\" produce for i = 7?", "back": "'07' — formats the integer as two digits with a leading zero."},
    {"front": "Do string methods like upper() modify the string in place?", "back": "No — strings are immutable; upper() returns a new string and the original is unchanged."},
    {"front": "What is the difference between break and continue?", "back": "break exits the loop entirely; continue skips the rest of the current iteration and moves to the next one."},
    {"front": "In {'a': 1}, what does d.get('b', 0) return and why use it?", "back": "Returns 0 — get() with a default avoids KeyError on missing keys, unlike d['b']."},
    {"front": "What does 'w' mode do in open('out.txt', 'w')?", "back": "Opens for writing and truncates the file — existing content is destroyed, so verify the path first."}
  ],
  "quiz": [
    {"q": "What does this print? for i in range(3):\n    if i == 5:\n        break\nelse:\n    print('done')", "choices": ["Nothing — the loop never breaks so else is skipped", "done", "0 1 2", "An infinite loop"], "answer": 1, "explain": "i never equals 5, so the loop completes without break and the else clause runs, printing 'done'."},
    {"q": "What is the output? a = [1, 2]; b = a; b = b + [3]; print(a)", "choices": ["[1, 2, 3]", "[1, 2]", "[[1, 2], 3]", "TypeError"], "answer": 1, "explain": "b + [3] builds a NEW list and rebinds b; a still points at the original [1, 2]. Only in-place methods like append would affect a."},
    {"q": "What prints? print([p for p in [80, 443, 22] if p != 22])", "choices": ["[80, 443, 22]", "[80, 443]", "[22]", "[]"], "answer": 1, "explain": "The comprehension keeps every port except 22, producing [80, 443]."},
    {"q": "def g(svc, env='staging', **opts): print(env, opts)\nWhat does g('api', 'prod', timeout=30) print?", "choices": ["staging {'timeout': 30}", "prod {'timeout': 30}", "prod {}", "TypeError: too many arguments"], "answer": 1, "explain": "'prod' overrides the default env positionally, and timeout=30 collects into opts as a dict."},
    {"q": "A script reads lines 'web2,down\\n' and compares fields to 'down' without strip(). What happens?", "choices": ["It matches correctly", "The comparison fails because the field is 'down\\n'", "split(',') raises ValueError", "The file cannot be opened"], "answer": 1, "explain": "The trailing newline stays on the last field, so 'down\\n' != 'down' — the classic file-parsing bug."},
    {"q": "What is the result of {'x': 1}['y'] versus {'x': 1}.get('y', 0)?", "choices": ["Both return 0", "Both raise KeyError", "First raises KeyError, second returns 0", "First returns None, second returns 0"], "answer": 2, "explain": "Direct indexing raises KeyError on a missing key; get() with a default returns the default instead."},
    {"q": "What does this print? for c in [200, 200, 500]:\n    if c == 200: continue\n    print(c)", "choices": ["200 200 500", "500", "200 200", "Nothing"], "answer": 1, "explain": "continue skips the 200 iterations before the print; only 500 reaches print."},
    {"q": "x = 'a,b,c'; what are x.split(',') and '-'.join(x.split(','))?", "choices": ["['a,b,c'] and 'a,b,c'", "['a', 'b', 'c'] and 'a-b-c'", "('a', 'b', 'c') and 'a-b-c'", "['a', 'b', 'c'] and 'a,b,c'"], "answer": 1, "explain": "split(',') gives the list ['a','b','c']; join glues them with dashes into 'a-b-c'."},
    {"q": "How many lines does this print, and what? name='db'\nfor i in range(1, 3): print(f'{name}-{i:02d}')", "choices": ["1 line: db-1", "2 lines: db-01 and db-02", "2 lines: db-1 and db-2", "3 lines: db-01, db-02, db-03"], "answer": 1, "explain": "range(1, 3) yields 1 and 2 (two iterations), and :02d zero-pads each to two digits."}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL28-M19"],
  "drills": [
    {
      "id": "il28-m18-predict-output",
      "title": "Predict the output — original script-reading drills",
      "items": [
        {"prompt": "Predict the exact output:\nevents = [('deploy','prod'),('deploy','staging'),('rollback','prod'),('deploy','prod'),('test','staging'),('deploy','dev')]\ncount = 0\nfor action, env in events:\n    if action == 'deploy' and env != 'dev':\n        count += 1\nprint('deploys:', count)", "answer": "deploys: 3", "explain": "Tuple unpacking binds action/env each round. deploy+prod (twice) and deploy+staging increment; rollback, test, and deploy+dev (env == 'dev' excluded) do not. One print at the end."},
        {"prompt": "Predict the exact output:\nlogs = ['ERROR disk full','INFO ok','ERROR timeout','INFO ok','WARN slow']\nerrors = {}\nfor line in logs:\n    level = line.split()[0]\n    errors[level] = errors.get(level, 0) + 1\nprint(errors)", "answer": "{'ERROR': 2, 'INFO': 2, 'WARN': 1}", "explain": "split()[0] takes the level word; get(level, 0) counts safely. Insertion order is ERROR, INFO, WARN with counts 2, 2, 1."},
        {"prompt": "Predict the exact output:\nports = [80, 443, 8080, 22, 3306]\nopen_ports = [p for p in ports if p not in (22, 3306)]\nprint(open_ports)\nprint(len(open_ports))", "answer": "[80, 443, 8080]\n3", "explain": "The comprehension filters out 22 and 3306, keeping three ports; len of the resulting list is 3. Two print calls, two lines."},
        {"prompt": "Predict the exact output:\ndef add_host(host, inventory=[]):\n    inventory.append(host)\n    return inventory\nprint(add_host('web1'))\nprint(add_host('web2'))", "answer": "['web1']\n['web1', 'web2']", "explain": "The mutable default list is created once at def time and shared: the first call appends web1, the second appends web2 to the same list."},
        {"prompt": "Predict the exact output:\nfor i in range(3):\n    if i == 5:\n        break\nelse:\n    print('done')", "answer": "done", "explain": "i takes 0, 1, 2 — never 5 — so no break fires, the loop completes, and the else clause prints 'done'."},
        {"prompt": "Predict the exact output:\nname = 'api'\nfor i in range(1, 4):\n    print(f'{name}-{i:02d}')", "answer": "api-01\napi-02\napi-03", "explain": "range(1, 4) yields 1, 2, 3; :02d zero-pads each to two digits, producing three lines."},
        {"prompt": "Predict the exact output:\ndata = 'web1,up\\nweb2,down\\nweb3,up\\n'\ndown = [line.split(',')[0] for line in data.strip().split('\\n') if line.split(',')[1] == 'down']\nprint(down)", "answer": "['web2']", "explain": "strip() removes the trailing newline, split('\\n') gives three lines; only web2's second field equals 'down', so the comprehension keeps just 'web2'."}
      ]
    },
    {
      "id": "il28-m18-concepts",
      "title": "Core concepts drill",
      "items": [
        {"prompt": "Is a tuple mutable or immutable? What does that imply for using one as a dict key?", "answer": "Immutable — and because immutable, tuples are hashable and can be dict keys (unlike lists).", "explain": "Immutability enables hashing; mutability forbids it."},
        {"prompt": "What does the * in *args do at call time versus at definition time?", "answer": "At definition it collects extra positionals into a tuple; at a call site, * unpacks an iterable into separate positional arguments.", "explain": "Definition collects, call-site unpacks — the two directions of *."},
        {"prompt": "Why is iterating a file object directly better than readlines() for logs?", "answer": "Iteration streams line by line with constant memory; readlines() loads the entire file, which can exhaust memory on gigabyte logs.", "explain": "Streaming versus whole-file load."},
        {"prompt": "What is the difference between == and is?", "answer": "== compares values for equality; is checks whether two names reference the identical object.", "explain": "Use == for values; is is for identity (e.g. comparing with None)."},
        {"prompt": "Rewrite as a comprehension: result = []; for x in range(10): if x % 2 == 0: result.append(x * 2)", "answer": "result = [x * 2 for x in range(10) if x % 2 == 0]", "explain": "Output expression first, then the for clause, then the if filter."},
        {"prompt": "A function ends without a return statement. What does calling it produce?", "answer": "None — falling off the end of a function returns None implicitly.", "explain": "Every Python call returns something; without return it is None."},
        {"prompt": "When should you prefer a plain loop over a clever comprehension?", "answer": "When the comprehension is hard to read at a glance, has side effects, or needs complex error handling — readability wins.", "explain": "Panels reward the judgment to choose clarity over density."}
      ]
    }
  ],
  "handsOnLab": {
    "id": "il28-m18-lab",
    "title": "Log parser: from reading to writing scripts",
    "brief": "You will write a small Python log-analysis script that parses a generated access log, counts status codes, finds the slowest endpoint, and prints a summary — then verify your output predictions by running it.",
    "steps": [
      "Create the lab directory and file: mkdir py-reading-lab && cd py-reading-lab, then create parse_logs.py (empty for now).",
      "Generate a sample log: write gen.py that writes 200 lines of 'METHOD /path STATUS MS' (e.g. 'GET /api/users 200 42') with random choices from a fixed seed (random.seed(7)) so output is reproducible, then run python3 gen.py to produce access.log.",
      "In parse_logs.py, open access.log with a with statement and iterate line by line — do not use readlines().",
      "Parse each line with strip().split() into method, path, status, ms; convert status and ms to int inside a try/except ValueError that skips malformed lines with a counter.",
      "Count requests per status code in a dict using d.get(code, 0) + 1.",
      "Track the slowest request: keep (ms, method, path) of the maximum seen so far.",
      "Collect error paths: build a list of paths whose status >= 500 using a comprehension over your parsed records.",
      "Print a summary: total lines, skipped lines, per-status counts sorted by code, slowest request, and number of error paths.",
      "Before running, write your predicted summary numbers in predictions.txt by reasoning about the seeded generator (or compute them independently).",
      "Run python3 parse_logs.py, diff actual versus predictions.txt, and fix any mismatch by re-tracing — not by editing the script to match."
    ],
    "deliverable": "parse_logs.py, gen.py, access.log, predictions.txt, and a short notes file explaining any prediction mismatches and what tracing error caused them.",
    "checkpoint": "The script runs with no exceptions on the seeded log; per-status counts sum to (200 - skipped); predictions.txt matches actual output or every mismatch is explained in the notes file."
  },
  "mockTask": {
    "id": "il28-m18-mock",
    "type": "choice",
    "q": "Panel shows a script with def register(host, seen=[]) that appends each host and returns seen, called three times. They ask: 'What does the third call return, and is this code production-safe?'",
    "choices": ["Only the third host — each call gets a fresh list; it is safe", "All three hosts accumulated — the default list is shared; it is a bug, use None default", "An empty list — defaults are re-evaluated per call", "It raises TypeError on the second call"],
    "answer": 1,
    "explain": "Mutable defaults are created once at def time and shared, so hosts accumulate across calls — the classic gotcha. The fix is def register(host, seen=None) with seen = seen if seen is not None else [] inside."
  },
  "crossLinks": [],
  "videos": [
    {"title": "Learn Python – Full Course for Beginners", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw", "source": "freeCodeCamp.org (YouTube)", "durationMin": 277, "order": 1, "watchBefore": "notes", "blurb": "Comprehensive Python course from variables through file I/O — watch the sections matching each note, then test yourself with the predict-output drills."}
  ],
  "estimatedMinutes": 0
}
