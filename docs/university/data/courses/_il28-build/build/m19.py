module = {
  "id": "IL28-M19",
  "code": "IL-28",
  "title": "Python for DevOps: APIs, Subprocess & Dependency Pinning",
  "summary": "Turn Python into an operations tool: call REST APIs safely with requests, drive system commands with subprocess, build argparse CLIs, and pin dependencies reproducibly — the scripting backbone of every DevOps workflow.",
  "objectives": [
    "Make HTTP API calls with requests using timeouts and explicit status-code handling.",
    "Run and capture system commands with subprocess.run without shell-injection risk.",
    "Parse JSON and YAML configuration into Python data structures.",
    "Build a command-line tool with argparse, exit codes, and helpful --help output.",
    "Create virtualenvs and write pinned requirements files that make builds reproducible."
  ],
  "notes": [
    {
      "title": "requests: the timeout is not optional",
      "body": """Almost every DevOps script talks to an HTTP API — cloud providers, monitoring, artifact registries. The requests library makes it pleasant, but there is one rule professionals never break: always pass a timeout. Without it, a hung server hangs your script forever, and at 3 a.m. that means a remediation job that never finishes. Worked example:

import requests

resp = requests.get(\"https://httpbin.org/get\", timeout=10)
print(resp.status_code)
print(resp.json()[\"url\"])

Solution: prints 200, then \"https://httpbin.org/get\". Walkthrough: requests.get returns a Response; .status_code is the integer code; .json() parses the body. The timeout=10 means \"give up after 10 seconds\" — pass a tuple like timeout=(5, 30) to separate connect and read timeouts when you need finer control. Two more habits: check resp.ok or call resp.raise_for_status() instead of assuming 200, because APIs return 201, 204, 429, and 503 in normal operation; and never put secrets in URLs — use the headers={\"Authorization\": f\"Bearer {token}\"} pattern with the token from an environment variable. A script that calls an API without a timeout and without status handling is the single most common defect in take-home automation exercises."""
    },
    {
      "title": "POSTing JSON and handling API errors",
      "body": """Reading is half the job; the other half is creating and updating resources — opening tickets, triggering pipelines, registering webhooks. requests.post with the json= parameter serializes your dict and sets the Content-Type header automatically. Worked example:

import requests

payload = {\"service\": \"api\", \"env\": \"prod\", \"replicas\": 3}
resp = requests.post(\"https://httpbin.org/post\", json=payload, timeout=10)
resp.raise_for_status()
echoed = resp.json()[\"json\"]
print(echoed[\"replicas\"])

Solution: prints 3. Walkthrough: json=payload sends the dict as a JSON body; raise_for_status() throws an HTTPError on 4xx/5xx so failures cannot slip by silently; httpbin echoes the JSON back under the \"json\" key, so echoed[\"replicas\"] is 3. The panel-relevant pattern is what surrounds the call:

try:
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
except requests.Timeout:
    print(\"API timed out — will retry\")
except requests.HTTPError as e:
    print(\"API error:\", e)

Catch Timeout separately from HTTPError because the remediation differs: timeouts merit a retry with backoff, while a 400 means your payload is wrong and retrying is pointless. Always log the status code and a correlation ID — \"it failed\" is not a debuggable incident report."""
    },
    {
      "title": "subprocess: running system commands safely",
      "body": """When Python must drive the system — kubectl, docker, systemctl, git — subprocess.run is the modern interface. The critical choice is shell=False (the default) with the command as a list: each list element is one argument, so a hostile filename can never become a second command. Worked example:

import subprocess

result = subprocess.run(
    [\"kubectl\", \"get\", \"pods\", \"-n\", \"prod\", \"-o\", \"json\"],
    capture_output=True, text=True, timeout=30, check=False,
)
print(\"rc:\", result.returncode)
print(\"bytes:\", len(result.stdout))

Solution: prints the real return code (0 on a healthy cluster) and the byte length of the JSON output. Walkthrough: capture_output=True grabs stdout/stderr instead of inheriting the terminal; text=True decodes to str; timeout=30 bounds the call; check=False (default) means a nonzero exit does NOT raise — you inspect result.returncode yourself. Use check=True only when any failure should abort the script. Never do subprocess.run(f\"kubectl get {user_input}\", shell=True) — with shell=True the string is parsed by a shell and user_input containing \"; rm -rf\" executes. If you truly need shell features (pipes), keep shell=True but never interpolate untrusted data, or better, chain two subprocess.run calls with pipes in Python. Prefer passing lists, always set a timeout, and log result.stderr on failure."""
    },
    {
      "title": "Parsing JSON and YAML configuration",
      "body": """DevOps scripts constantly read config: JSON from APIs and files, YAML from Kubernetes manifests and pipeline definitions. Python's json module is stdlib; YAML needs the third-party pyyaml package (import yaml). Worked example — read a JSON service catalog and a YAML deploy config:

import json

catalog = json.loads('{\"services\": [{\"name\": \"api\", \"port\": 8080}]}')
print(catalog[\"services\"][0][\"port\"])

Solution: prints 8080 — json.loads turns the JSON string into nested dicts/lists. For YAML:

import yaml

with open(\"deploy.yaml\") as f:
    config = yaml.safe_load(f)
print(config[\"replicas\"])

Given deploy.yaml containing \"replicas: 3\\nimage: api:v2\\n\", this prints 3. Always use yaml.safe_load, never yaml.load — the unsafe loader can construct arbitrary Python objects from hostile YAML, a real deserialization risk. Two reading habits: validate the shape after parsing (config.get(\"replicas\") with a sensible default beats a KeyError at 3 a.m.), and when writing JSON for machines use json.dump(obj, f, indent=2, sort_keys=True) so diffs are stable and reviewable. Panels often ask you to extract one value from a nested API response by hand — practice navigating dict-in-list-in-dict without running the code."""
    },
    {
      "title": "argparse: CLIs people can actually use",
      "body": """An automation script nobody can invoke correctly is shelfware. argparse turns a script into a real CLI with --help, types, defaults, and required flags. Worked example — the skeleton of the health-check tool you will build in the lab:

import argparse

parser = argparse.ArgumentParser(description=\"Check an HTTP endpoint and exit nonzero on failure.\")
parser.add_argument(\"url\", help=\"Endpoint to check, e.g. https://api.example.com/healthz\")
parser.add_argument(\"--timeout\", type=int, default=10, help=\"Seconds before giving up (default: 10)\")
parser.add_argument(\"--expect\", type=int, default=200, help=\"Expected HTTP status (default: 200)\")
args = parser.parse_args()
print(args.url, args.timeout, args.expect)

Run as python3 healthcheck.py https://example.com --timeout 5 and it prints \"https://example.com 5 200\". Walkthrough: the positional url is required (argparse errors out with usage text if missing); --timeout and --expect are optional with typed, defaulted values — type=int converts and validates, rejecting \"--timeout abc\" with a clear error. Three professional touches: a description string (it becomes the --help header), explicit defaults shown in help text, and exiting with distinct codes (0 healthy, 1 unhealthy, 2 usage/config error) so CI pipelines and cron can branch on the result. Never parse sys.argv by hand — argparse is stdlib, tested, and expected."""
    },
    {
      "title": "Virtualenvs and pinning: reproducible automation",
      "body": """A script that works on your laptop and breaks in CI is usually a dependency problem: different package versions. The fix has two parts. First, isolate with a virtualenv so the script's packages never fight the system Python: python3 -m venv .venv && source .venv/bin/activate && pip install requests. Second, pin every dependency with == in requirements.txt — the exact lesson from the M17 MR review. Worked example:

$ pip freeze > requirements.txt
$ cat requirements.txt
requests==2.32.3

That file, committed to the repo, means every install — laptop, CI, container — resolves the identical tree. Unpinned requirements (a bare requests line) resolve to whatever is newest on install day, so the code you tested is not the code you deploy. The hashes concept goes one step further: pip install --require-hashes verifies each downloaded wheel against a recorded SHA256, defeating a compromised mirror serving a trojaned package — generate them with pip hash on the downloaded files or pip-compile. Practical rules: pin runtime deps in requirements.txt, keep test tooling in requirements-test.txt, never commit the .venv directory itself, and regenerate pins deliberately (upgrade, test, re-pin) rather than letting them drift. A panel asked to review a requirements.txt expects exactly this verdict-first reasoning."""
    }
  ],
  "cards": [
    {"front": "What is the one requests rule you must never break?", "back": "Always pass a timeout — without it a hung server hangs your script forever."},
    {"front": "What does resp.raise_for_status() do?", "back": "Raises an HTTPError on 4xx/5xx responses so API failures cannot pass silently; call it (or check status) instead of assuming 200."},
    {"front": "Why catch requests.Timeout separately from requests.HTTPError?", "back": "Timeouts merit a retry with backoff; a 400 means your payload is wrong and retrying is pointless — different failures need different remediation."},
    {"front": "Why is subprocess.run(['kubectl','get','pods']) safer than subprocess.run('kubectl get ' + user_input, shell=True)?", "back": "With a list and shell=False each element is one argument, so hostile input cannot become a second command; shell=True lets injected input like '; rm -rf' execute."},
    {"front": "In subprocess.run, what do capture_output, text, timeout, and check do?", "back": "capture_output grabs stdout/stderr; text decodes to str; timeout bounds the call; check=True raises on nonzero exit (default False — inspect returncode yourself)."},
    {"front": "Why yaml.safe_load instead of yaml.load?", "back": "The unsafe loader can construct arbitrary Python objects from hostile YAML — a deserialization risk. safe_load restricts to basic types."},
    {"front": "What does argparse give you that hand-parsing sys.argv does not?", "back": "--help text, typed/validated options, defaults, required flags, and clear usage errors — all from the stdlib."},
    {"front": "What exit-code convention should a health-check CLI use?", "back": "0 = healthy, 1 = unhealthy, 2 = usage/config error — so CI and cron can branch on the result."},
    {"front": "Why pin dependencies with == in requirements.txt?", "back": "Unpinned installs resolve to whatever is newest on install day, so the tested artifact differs from the deployed one; pins make every install identical."},
    {"front": "What does pip install --require-hashes add beyond == pins?", "back": "It verifies each downloaded wheel against a recorded SHA256, defeating a compromised mirror serving a trojaned package."},
    {"front": "Should the .venv directory be committed to git?", "back": "No — commit requirements.txt (the recipe), never the environment itself."},
    {"front": "Where does pytest belong: requirements.txt or requirements-test.txt?", "back": "requirements-test.txt — test tooling does not belong in the production install (leaner images, smaller attack surface)."}
  ],
  "quiz": [
    {"q": "A script calls requests.get(url) with no timeout. What is the operational risk?", "choices": ["The response is always cached", "A hung server hangs the script indefinitely", "It uses too much memory", "DNS lookups are skipped"], "answer": 1, "explain": "Without a timeout there is no bound on how long the call can block — a hung server means a hung automation job."},
    {"q": "What does timeout=(5, 30) mean in requests?", "choices": ["Retry 5 times over 30 seconds", "5 seconds connect timeout, 30 seconds read timeout", "30 seconds connect timeout, 5 seconds read timeout", "Cache the response for 5-30 seconds"], "answer": 1, "explain": "The tuple form separates the connect timeout from the read timeout for finer control."},
    {"q": "Which subprocess call is safe against shell injection with untrusted filename input?", "choices": ["subprocess.run('ls ' + filename, shell=True)", "subprocess.run(['ls', filename])", "subprocess.run(f'ls {filename}', shell=True)", "os.system('ls ' + filename)"], "answer": 1, "explain": "A list with shell=False passes filename as a single argument; every shell=True option lets injected metacharacters execute."},
    {"q": "subprocess.run(['kubectl','get','pods'], capture_output=True, text=True) — what do the flags do?", "choices": ["They stream output live to the terminal", "They capture stdout/stderr and decode to str instead of bytes", "They suppress all output", "They run the command as text, not binary"], "answer": 1, "explain": "capture_output grabs the streams; text=True decodes bytes to str so you can parse directly."},
    {"q": "Why must you use yaml.safe_load on untrusted YAML?", "choices": ["It is faster", "The unsafe loader can construct arbitrary Python objects — a deserialization attack", "safe_load supports more YAML features", "Untrusted YAML cannot be parsed otherwise"], "answer": 1, "explain": "yaml.load can instantiate arbitrary objects from hostile input; safe_load restricts parsing to basic types."},
    {"q": "In argparse, what does parser.add_argument('--timeout', type=int, default=10) provide?", "choices": ["A required positional argument", "An optional flag, converted to int, defaulting to 10, rejected with a clear error if not numeric", "A boolean toggle", "An environment variable reader"], "answer": 1, "explain": "type=int validates and converts; default supplies the fallback; invalid input produces a clean usage error."},
    {"q": "A requirements.txt lists bare 'requests' with no version. What breaks?", "choices": ["Nothing — pip pins automatically", "Reproducibility: installs on different days may resolve different versions", "The package cannot be found", "Virtualenvs stop working"], "answer": 1, "explain": "Unpinned requirements float with the newest release, so tested code and deployed code can differ."},
    {"q": "What is the purpose of pip freeze > requirements.txt?", "choices": ["To delete unused packages", "To record the exact installed versions so others can reproduce the environment", "To upgrade all packages", "To verify package hashes"], "answer": 1, "explain": "freeze snapshots the working set's exact versions into the pin file you commit."},
    {"q": "An API returns 429. Your script called raise_for_status() inside try/except HTTPError. What should the handler do?", "choices": ["Retry immediately in a tight loop", "Back off and retry, honoring any Retry-After guidance — 429 means rate-limited", "Treat it as success", "Delete the payload and resend"], "answer": 1, "explain": "429 signals rate limiting; the correct remediation is backoff-and-retry, not hammering the API."}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL28-M20"],
  "drills": [
    {
      "id": "il28-m19-api-subprocess",
      "title": "APIs and subprocess drill",
      "items": [
        {"prompt": "Write the requests call to GET https://api.example.com/healthz with a 10-second timeout, raising on HTTP errors.", "answer": "resp = requests.get('https://api.example.com/healthz', timeout=10); resp.raise_for_status()", "explain": "Timeout bounds the call; raise_for_status converts 4xx/5xx into exceptions instead of silent failures."},
        {"prompt": "How do you POST the dict {'replicas': 3} as JSON and read back the echoed value?", "answer": "resp = requests.post(url, json={'replicas': 3}, timeout=10); resp.raise_for_status(); value = resp.json()['replicas']", "explain": "json= serializes and sets Content-Type; .json() parses the response body back into Python."},
        {"prompt": "Where should an API token live, and how does it reach the request?", "answer": "In an environment variable (never hardcoded or in URLs); passed via headers={'Authorization': f'Bearer {token}'}.", "explain": "Env vars keep secrets out of code and URLs keep them out of logs."},
        {"prompt": "Run 'kubectl get pods -n prod -o json' from Python, capturing output as text with a 30s timeout. Write the call.", "answer": "subprocess.run(['kubectl','get','pods','-n','prod','-o','json'], capture_output=True, text=True, timeout=30)", "explain": "List form with shell=False (no injection), capture_output+text for parseable str, timeout to bound the call."},
        {"prompt": "The command above returns exit code 1. How do you detect it, and when would check=True be appropriate?", "answer": "Inspect result.returncode (check defaults False); use check=True when any failure should abort the script via CalledProcessError.", "explain": "Default gives you control to branch on the code; check=True is the fail-fast option."},
        {"prompt": "Parse the JSON string '{\"port\": 8080}' and print the port. Write the code.", "answer": "import json; print(json.loads('{\"port\": 8080}')['port'])", "explain": "json.loads converts the JSON string to a dict; index the key."},
        {"prompt": "A script reads deploy.yaml from an untrusted source. Which loader and why?", "answer": "yaml.safe_load — the default yaml.load can construct arbitrary Python objects, a deserialization risk on hostile input.", "explain": "safe_load restricts to basic types."}
      ]
    },
    {
      "id": "il28-m19-cli-pinning",
      "title": "CLI design and pinning drill",
      "items": [
        {"prompt": "Define an argparse positional 'url' and optional '--timeout' (int, default 10). Write the snippet.", "answer": "p = argparse.ArgumentParser(description='...'); p.add_argument('url'); p.add_argument('--timeout', type=int, default=10); args = p.parse_args()", "explain": "Positional is required by default; the option is typed, defaulted, and self-documenting in --help."},
        {"prompt": "Your CLI is used by CI. Which exit codes do you use for healthy, unhealthy, and bad usage?", "answer": "0 healthy, 1 unhealthy, 2 usage/config error.", "explain": "Distinct codes let pipelines and cron branch on the outcome."},
        {"prompt": "Create and activate a virtualenv, then install requests into it. Give the commands.", "answer": "python3 -m venv .venv && source .venv/bin/activate && pip install requests", "explain": "Isolates the script's packages from the system Python."},
        {"prompt": "Generate a pinned requirements file from the active venv. Give the command and explain what it records.", "answer": "pip freeze > requirements.txt — records exact installed versions so every environment installs identically.", "explain": "The pin file is the reproducibility contract you commit."},
        {"prompt": "An MR adds requirements.txt with 'requests' unpinned. Verdict and fix?", "answer": "Request changes: pin as requests==<verified-version> so builds are reproducible.", "explain": "The M17 review rule applied: verdict first, then the fix."},
        {"prompt": "What does --require-hashes protect against that == pins do not?", "answer": "A compromised mirror serving a trojaned wheel with the right version number — hashes verify the actual bytes.", "explain": "Pins name the version; hashes verify the content."},
        {"prompt": "Should pytest go in requirements.txt for a production container image? Why?", "answer": "No — test tooling belongs in requirements-test.txt; shipping it bloats the image and widens the attack surface.", "explain": "Separation of runtime and test dependency sets."}
      ]
    }
  ],
  "handsOnLab": {
    "id": "il28-m19-lab",
    "title": "Build a CLI health-check tool",
    "brief": "You will build healthcheck.py — an argparse CLI that GETs a URL with a timeout, compares the status to an expected code, exits 0/1/2 appropriately, and ships with a pinned requirements.txt generated from a virtualenv.",
    "steps": [
      "Set up: mkdir healthcheck-lab && cd healthcheck-lab && python3 -m venv .venv && source .venv/bin/activate && pip install requests.",
      "Write healthcheck.py with argparse: positional 'url', --timeout (int, default 10), --expect (int, default 200), and a --retries (int, default 0) flag.",
      "Implement the check: requests.get(url, timeout=timeout) inside try/except — catch requests.Timeout separately from requests.RequestException.",
      "On timeout: print a clear message, honor --retries with a short sleep backoff, then exit 1 if still failing.",
      "On response: compare resp.status_code to --expect; print 'OK <code>' and exit 0 on match, 'FAIL: got <code>, expected <exp>' and exit 1 otherwise.",
      "On request exception (DNS, connection refused): print the error class and message, exit 1.",
      "Validate argparse: run with no args (expect exit 2 + usage), --help (readable help), and --timeout abc (clean type error).",
      "Test live: run against https://httpbin.org/status/200 (expect OK/0), https://httpbin.org/status/503 with --expect 200 (expect FAIL/1), and https://httpbin.org/delay/5 with --timeout 2 (expect timeout path).",
      "Pin it: run pip freeze > requirements.txt, confirm requests is pinned with ==, and add a requirements-test.txt placeholder note.",
      "Write README.md with three example invocations and the exit-code contract (0/1/2)."
    ],
    "deliverable": "healthcheck.py, requirements.txt (pinned), requirements-test.txt, README.md with usage examples and the exit-code contract.",
    "checkpoint": "No-arg run exits 2; httpbin 200-check exits 0 printing OK; 503-check exits 1 printing FAIL; delay/timeout path prints a timeout message and exits 1; requirements.txt contains requests==<version>."
  },
  "mockTask": {
    "id": "il28-m19-mock",
    "type": "choice",
    "q": "Panel: 'Your Python remediation script calls an internal API and shells out to kubectl. Two review findings — what are they?'",
    "choices": ["Use os.system instead of subprocess, and hardcode the API token for speed", "Add a timeout to the API call and use subprocess.run with a list (shell=False) instead of shell=True with string interpolation", "Remove all error handling to keep it short, and skip the virtualenv", "Call the API without checking status codes, and parse YAML with yaml.load"],
    "answer": 1,
    "explain": "Timeouts bound API calls so hung servers cannot hang automation; list-form subprocess with shell=False eliminates shell injection. The other options each introduce a defect: hardcoded secrets, missing error handling, and unsafe YAML loading."
  },
  "crossLinks": [],
  "videos": [
    {"title": "Python Requests Tutorial: Request Models", "url": "https://www.youtube.com/watch?v=tb8gH9ZhlG0", "source": "Corey Schafer (YouTube)", "durationMin": 25, "order": 1, "watchBefore": "notes", "blurb": "Clear walkthrough of the requests library — GET/POST, responses, and error handling — the API foundation this module builds on."}
  ],
  "estimatedMinutes": 0
}
