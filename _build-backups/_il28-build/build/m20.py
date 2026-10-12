module = {
  "id": "IL28-M20",
  "code": "IL-28",
  "title": "Concurrency, the GIL & Health-Probe-Friendly Services",
  "summary": "Understand threads, processes, and async in Python, what the GIL really limits, and why single-threaded services fail Kubernetes readiness probes under load — then design probe-friendly services with separate /healthz endpoints and timeouts everywhere.",
  "objectives": [
    "Compare threads, processes, and async I/O and choose the right model for a workload.",
    "Explain the GIL's effect on CPU-bound versus I/O-bound Python code.",
    "Diagnose why a single-threaded Python service fails readiness probes under load.",
    "Design separate liveness and readiness endpoints with correct semantics.",
    "Apply timeouts and non-blocking patterns so slow dependencies cannot cascade."
  ],
  "notes": [
    {
      "title": "Threads, processes, async: three kinds of concurrency",
      "body": """Concurrency means making progress on multiple things at once, and Python offers three models. Threads share one memory space — cheap to start, but shared state needs locks and a crash in one thread can take the process. Processes (multiprocessing) each get their own memory and their own GIL — true parallelism for CPU-bound work, at the cost of heavier startup and inter-process communication. Async (asyncio) runs many tasks on a single thread, switching at await points — extremely efficient for I/O-bound work (thousands of connections), but one blocking call with no await freezes everything. Worked example — I/O-bound fetching with threads:

import threading, time

def fetch(n):
    time.sleep(1)  # stands in for network I/O
    print(f\"done {n}\")

threads = [threading.Thread(target=fetch, args=(i,)) for i in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(\"all done\")

Solution: prints \"done 0\" through \"done 3\" in some order after about one second total, then \"all done\" — the four sleeps overlap because threads release the GIL during I/O. The same work sequentially would take four seconds. Rule of thumb: threads or async for I/O-bound (API calls, DB queries), processes for CPU-bound (number crunching, image work), async when you need massive connection counts with low overhead. Picking wrong is a panel-visible defect: threads for CPU-bound hashing gain nothing under the GIL."""
    },
    {
      "title": "The GIL: what it actually limits",
      "body": """CPython's Global Interpreter Lock allows only one thread to execute Python bytecode at a time. This is the single most misunderstood fact in Python interviews, so be precise: the GIL limits CPU-bound threading, not I/O-bound threading. During I/O — network reads, disk waits, time.sleep — a thread releases the GIL, so other threads run. During pure Python computation, they take turns and you gain no speedup (and may lose a little to switching overhead). Worked example — two workloads, two outcomes. Workload A: four threads each downloading a file. Result: roughly 4x faster than sequential, because the threads spend their time waiting on the network with the GIL released. Workload B: four threads each hashing data in a tight Python loop. Result: no faster than sequential — the GIL serializes the bytecode execution. The fixes for B are multiprocessing (each process has its own GIL and its own core) or pushing the hot loop into C (numpy, hashlib releases the GIL internally). For DevOps services — which are overwhelmingly I/O-bound, waiting on APIs, databases, and queues — threads and async are usually the right answer, and \"the GIL makes Python slow\" is not a valid objection to them. Know the boundary cold: GIL bites CPU-bound threads; it does not bite I/O-bound ones."""
    },
    {
      "title": "Panel question: why single-threaded Python fails readiness probes under load",
      "body": """This is a real panel question: a single-threaded Python service passes health checks at low traffic, then starts failing readiness probes under load — while the equivalent Java service survives. Here is the mechanism. A single-threaded server handles one request at a time. Each request does slow work — a database query, a downstream API call — taking, say, 800ms. At low traffic that is fine. Under load, requests queue behind the one being served. The readiness probe is just another HTTP request to /healthz, and it joins the same queue. If the probe cannot get a response within its timeout, the kubelet marks the pod unready and pulls it out of the service — even though the app is technically alive and working through its queue. Traffic shifts to the remaining pods, which now take more load, queue longer, and fail their probes too: a cascading failure from a healthy-but-slow service. The Java comparison: a typical Java server uses a thread pool or non-blocking I/O, so the probe request gets a thread immediately even while others are busy. The Python fix is the same idea — serve probes concurrently with work (threads, async, or a separate probe server), keep the probe endpoint trivially cheap, and set aggressive timeouts on downstream calls so no single request can hold the server for seconds."""
    },
    {
      "title": "Separate /healthz endpoints: liveness vs readiness vs startup",
      "body": """Kubernetes has three probes with three different consequences, and mixing them up causes real outages. Liveness: \"is this container dead?\" If the liveness probe fails, the kubelet RESTARTS the container. Readiness: \"should this pod receive traffic?\" If it fails, the pod is removed from service endpoints but NOT restarted. Startup: for slow-starting containers, it gates the other two so a long warmup does not trigger restarts. Worked example — a Python API with correct probe design:

@app.get(\"/healthz\")   # liveness: trivially cheap
def healthz():
    return {\"status\": \"ok\"}

@app.get(\"/ready\")     # readiness: checks real dependencies
def ready():
    if not db.ping(timeout=2):
        raise HTTPException(503, \"db unreachable\")
    return {\"status\": \"ready\"}

The liveness endpoint does no I/O at all — it answers even when the database is down, because a dead database is not a dead container and restarting would not help. The readiness endpoint checks the database with a short timeout, so traffic stops flowing to a pod that cannot serve. The classic defect is one /health endpoint doing deep dependency checks wired as the liveness probe: a database blip then restarts every pod instead of just pausing traffic. Panel rule: liveness = cheap and restart-worthy; readiness = dependency-aware and traffic-gating; startup = warmup grace period."""
    },
    {
      "title": "Timeouts everywhere: stop slow dependencies from cascading",
      "body": """Every network call your service makes needs a timeout, or one slow dependency becomes your outage. The failure mode: your API calls a downstream service with no timeout; the downstream hangs; your request handlers pile up waiting; memory and threads exhaust; readiness probes time out; the kubelet pulls the pod. One hung dependency, full cascade. Worked example — the timeout discipline in a readiness check:

def db_reachable():
    try:
        return db.ping(timeout=2)   # 2s, not 30s, not forever
    except TimeoutError:
        return False

Three timeout layers professionals set. One: client timeouts on every outbound call (requests timeout=, DB connect_timeout) — short for probes, generous for batch jobs. Two: server timeouts — how long your framework waits before abandoning a request handler, so one bad request cannot hold a worker forever. Three: probe timeouts in the pod spec (timeoutSeconds) shorter than the period, so a stuck probe fails fast instead of overlapping. Also set connection-pool limits: unlimited outbound connections under load become a self-inflicted DDoS on your own database. The panel-ready summary: \"timeouts convert hangs into errors, and errors are retryable, alertable, and survivable — hangs are none of those.\" When reviewing any service, ask \"where is the timeout?\" on every network call; a missing one is a finding."""
    },
    {
      "title": "Async patterns: non-blocking services without thread pools",
      "body": """asyncio lets one thread juggle thousands of connections by suspending tasks at await points instead of blocking. The mental model: async def functions return coroutines; await yields control while waiting; the event loop resumes whichever task is ready. Worked example — concurrent health checks with asyncio.gather:

import asyncio

async def check(name):
    await asyncio.sleep(1)  # stands in for an I/O wait
    return f\"{name} ok\"

async def main():
    results = await asyncio.gather(check(\"db\"), check(\"cache\"))
    print(results)

asyncio.run(main())

Solution: prints ['db ok', 'cache ok'] after about one second — both sleeps overlap on the single thread, and gather preserves result order. Two rules that prevent the classic async defects. One: never call blocking code (time.sleep, requests.get, heavy computation) inside async functions without await — it freezes the entire event loop, and every connection stalls; offload blocking calls with asyncio.to_thread or loop.run_in_executor. Two: async only helps I/O-bound work; CPU-bound coroutines still serialize on the one thread. For probe-friendly services, the async payoff is direct: the /healthz handler is a tiny coroutine that answers between awaits of the slow work, so probes stay fast under load without managing a thread pool. That is the modern answer to the panel's single-threaded-Python question."""
    }
  ],
  "cards": [
    {"front": "Threads vs processes vs async — when is each the right choice?", "back": "Threads: I/O-bound work, shared memory, cheap. Processes: CPU-bound work needing true parallelism (own GIL each). Async: massive I/O connection counts on one thread, switching at await points."},
    {"front": "What does the GIL limit, precisely?", "back": "Only one thread executes Python bytecode at a time in CPython — so CPU-bound threads gain no speedup, while I/O-bound threads still win because the GIL is released during I/O waits."},
    {"front": "Why does a single-threaded Python service fail readiness probes under load?", "back": "One request at a time means probe requests queue behind slow work; when /healthz cannot answer within its timeout, the kubelet marks the pod unready — cascading as traffic shifts to fewer pods."},
    {"front": "Liveness vs readiness probe: what happens when each fails?", "back": "Liveness failure restarts the container; readiness failure only removes the pod from service traffic without restarting."},
    {"front": "What should a liveness endpoint do, and what should it NOT do?", "back": "Do: answer trivially with no I/O. Do NOT: deep-check dependencies — a dead database is not a dead container, and restarting on a DB blip turns a pause into an outage."},
    {"front": "What is a startup probe for?", "back": "It gates liveness/readiness for slow-starting containers so a long warmup does not trigger restarts or premature traffic."},
    {"front": "Name three timeout layers a production service needs.", "back": "Client timeouts on every outbound call; server timeouts bounding request handlers; probe timeoutSeconds shorter than the probe period — plus connection-pool limits."},
    {"front": "Why do timeouts matter more than retries?", "back": "Timeouts convert hangs into errors; errors are retryable, alertable, and survivable, while hangs silently consume workers until the service collapses."},
    {"front": "What freezes an asyncio event loop, and how do you avoid it?", "back": "Blocking calls (time.sleep, requests.get, CPU work) with no await freeze every connection; offload them with asyncio.to_thread or run_in_executor."},
    {"front": "Does asyncio help CPU-bound work?", "back": "No — coroutines still share one thread, so CPU-bound work serializes; use multiprocessing for CPU-bound parallelism."},
    {"front": "In the gather example, why do two 1-second sleeps finish in ~1 second total?", "back": "await suspends each coroutine during its sleep so both waits overlap on the single thread; gather preserves result order."},
    {"front": "A pod is running but gets restarted repeatedly. Which probe is the suspect, and what do you check?", "back": "The liveness probe — check whether it does expensive dependency checks (it should be trivially cheap) and whether timeoutSeconds/periodSeconds fit the app's real response time."}
  ],
  "quiz": [
    {"q": "Four threads each download a file (I/O-bound) under CPython. Expected speedup vs sequential?", "choices": ["No speedup — the GIL serializes everything", "Roughly 4x faster, since the GIL is released during I/O waits", "Exactly 4x faster guaranteed", "Slower, because threads cannot do I/O"], "answer": 1, "explain": "Threads release the GIL while waiting on I/O, so I/O-bound threaded work overlaps and speeds up; the GIL only serializes CPU-bound bytecode."},
    {"q": "Four threads each hash data in a tight Python loop. Expected result?", "choices": ["Roughly 4x faster", "No speedup — the GIL serializes the bytecode", "It raises a GIL error", "Only 2 threads run"], "answer": 1, "explain": "CPU-bound Python threads take turns on the GIL; use multiprocessing (own GIL per process) for CPU-bound parallelism."},
    {"q": "Panel: single-threaded Python service fails readiness probes under load but Java survives. Root cause?", "choices": ["Python is slower than Java", "Probe requests queue behind slow requests on the single thread and time out; Java's thread pool/NIO serves probes concurrently", "Kubernetes probes do not support Python", "The GIL blocks all network I/O"], "answer": 1, "explain": "One-at-a-time serving means /healthz waits in the same queue as work requests; concurrent serving (threads/async) lets probes answer immediately."},
    {"q": "The liveness probe fails. What does the kubelet do?", "choices": ["Removes the pod from service endpoints only", "Restarts the container", "Deletes the deployment", "Scales up replicas"], "answer": 1, "explain": "Liveness = 'is it dead?' → restart. Readiness = 'should it get traffic?' → remove from endpoints without restarting."},
    {"q": "Your liveness endpoint pings the database with a 30s timeout. What is wrong?", "choices": ["Nothing — thorough checks are good", "A DB blip will restart every pod instead of just pausing traffic; liveness must be trivially cheap", "30s is too short", "Liveness probes cannot use HTTP"], "answer": 1, "explain": "Deep dependency checks belong in readiness. Wiring them as liveness turns a downstream blip into mass restarts."},
    {"q": "An outbound API call has no timeout and the downstream hangs. What follows?", "choices": ["The call retries automatically", "Handlers pile up waiting, workers exhaust, probes time out — a cascading failure", "Only that one request is slow", "The GIL prevents the hang"], "answer": 1, "explain": "One hung dependency without a timeout consumes workers until readiness fails and traffic cascades onto fewer pods."},
    {"q": "Inside an async handler you call requests.get() (blocking). What happens?", "choices": ["It runs concurrently like everything else", "It freezes the entire event loop — all connections stall until it returns", "It raises an async error immediately", "It is automatically offloaded"], "answer": 1, "explain": "Blocking calls with no await hold the single thread; offload with asyncio.to_thread or run_in_executor."},
    {"q": "What does await asyncio.gather(check('db'), check('cache')) guarantee about results?", "choices": ["Results arrive in completion order", "Both checks overlap in time and results come back in the gather() argument order", "Exceptions are swallowed", "Only the first check runs"], "answer": 1, "explain": "gather runs the coroutines concurrently and returns results ordered by the argument list."},
    {"q": "Which fix addresses 'service knocked over under load, failing health checks'?", "choices": ["Increase the liveness failureThreshold to 100", "Serve probes concurrently (threads/async), keep /healthz trivially cheap, and set aggressive downstream timeouts", "Delete the readiness probe", "Run a single thread to reduce contention"], "answer": 1, "explain": "Concurrent probe serving plus cheap health endpoints plus timeouts is the cloud-native answer; masking the probe only hides the collapse."}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL28-M28"],
  "drills": [
    {
      "id": "il28-m20-gil-probes",
      "title": "GIL and probe-failure drill",
      "items": [
        {"prompt": "Is the GIL a problem for a thread pool making 50 concurrent API calls? Why?", "answer": "No — the threads spend their time waiting on I/O with the GIL released, so they overlap and speed up.", "explain": "GIL bites CPU-bound threads, not I/O-bound ones."},
        {"prompt": "Is the GIL a problem for threads computing checksums in pure Python? What is the fix?", "answer": "Yes — bytecode execution serializes with no speedup. Fix: multiprocessing (own GIL per process) or push the loop into C.", "explain": "CPU-bound parallelism needs processes, not threads."},
        {"prompt": "Panel: 'Your single-threaded Python API fails readiness under load. Walk me through it.'", "answer": "One request at a time; slow requests queue; the /healthz probe joins the queue and times out; kubelet marks unready; traffic shifts to fewer pods and they cascade too.", "explain": "The full causal chain: queueing → probe timeout → unready → cascade."},
        {"prompt": "Why does the equivalent Java service typically survive the same load?", "answer": "Thread pools or non-blocking I/O serve the probe request concurrently with slow work, so /healthz answers immediately.", "explain": "Concurrent probe serving is the difference, not language speed."},
        {"prompt": "Give three concrete fixes for the Python service.", "answer": "Serve with threads/async so probes answer concurrently; make /healthz trivially cheap with no dependency I/O; set aggressive timeouts on downstream calls.", "explain": "Concurrency + cheap probes + timeouts — the complete answer."},
        {"prompt": "A pod restarts in a loop during a database outage. Which probe is misconfigured and how?", "answer": "Liveness is doing deep dependency checks; move them to readiness so the outage pauses traffic instead of restarting pods.", "explain": "Liveness must be cheap; dependency checks are readiness semantics."},
        {"prompt": "When is a startup probe the right tool?", "answer": "For slow-starting containers, to delay liveness/readiness evaluation during warmup so they do not fire prematurely.", "explain": "Startup gates the other probes during initialization."}
      ]
    },
    {
      "id": "il28-m20-async-timeouts",
      "title": "Async and timeout drill",
      "items": [
        {"prompt": "Predict the output and timing: asyncio.gather(check('db'), check('cache')) where each awaits asyncio.sleep(1).", "answer": "Prints ['db ok', 'cache ok'] after ~1 second — the sleeps overlap and gather preserves argument order.", "explain": "Concurrent waits on one thread; ordered results."},
        {"prompt": "You need 2,000 concurrent outbound connections. Threads or async — and why?", "answer": "Async — thousands of threads carry heavy memory/scheduling overhead; async tasks are cheap coroutines on one thread.", "explain": "Connection-count scale favors async's low per-task cost."},
        {"prompt": "Name the defect: async def handler(): data = requests.get(url); return data.json()", "answer": "Blocking requests.get with no await freezes the event loop; use an async client or asyncio.to_thread.", "explain": "The classic async defect — one blocking call stalls all connections."},
        {"prompt": "Does converting CPU-bound work to async speed it up?", "answer": "No — coroutines share one thread and CPU work does not await; use multiprocessing.", "explain": "Async helps I/O-bound concurrency only."},
        {"prompt": "List the three timeout layers for a production service.", "answer": "Client timeouts on every outbound call; server timeouts bounding handlers; probe timeoutSeconds shorter than the period — plus pool limits.", "explain": "Defense in depth against hangs at every layer."},
        {"prompt": "Your readiness check pings the DB. What timeout and failure behavior?", "answer": "Short timeout (e.g. 2s); on timeout return not-ready (503) so traffic pauses instead of queueing.", "explain": "Fast failure at the probe keeps the failure local."},
        {"prompt": "Summarize in one sentence why timeouts beat retries as the first defense.", "answer": "Timeouts convert hangs into errors, and errors are retryable, alertable, and survivable — hangs are none of those.", "explain": "The panel-ready one-liner."}
      ]
    }
  ],
  "handsOnLab": {
    "id": "il28-m20-lab",
    "title": "Prove the probe failure, then fix it",
    "brief": "You will run a single-threaded Python HTTP server, reproduce the queued-probe failure under load with curl, then switch to a threaded server and show /healthz staying fast — the panel scenario, demonstrated live.",
    "steps": [
      "Create the lab dir: mkdir probe-lab && cd probe-lab.",
      "Write server_single.py: http.server BaseHTTPRequestHandler with do_GET — '/healthz' returns 200 immediately, '/work' does time.sleep(5) then returns 200; serve with HTTPServer (single-threaded).",
      "Start it: python3 server_single.py & then curl -s -o /dev/null -w '%{time_total}\\n' http://localhost:8000/healthz to record the fast baseline.",
      "Reproduce the failure: launch curl http://localhost:8000/work in the background, then immediately time another curl to /healthz — observe it blocks ~5s behind the work request.",
      "Write server_threaded.py: identical handlers, but serve with http.server.ThreadingHTTPServer.",
      "Restart on the threaded server and repeat step 4 — confirm /healthz answers in milliseconds while /work runs.",
      "Add a '/ready' endpoint that returns 503 until a module-level READY flag flips true 10 seconds after startup (simulate warmup); curl it before and after the flip.",
      "Load test: run a loop of 6 sequential 'curl /work' calls against each server version, timing the wall-clock total to feel queueing versus concurrency.",
      "Client timeout: run curl --max-time 2 http://localhost:8000/work and observe the client giving up — the timeout converting a hang into an error.",
      "Write findings.md: the queued-probe mechanism, which probe Kubernetes would fail, and your three fixes (concurrent serving, cheap /healthz, timeouts)."
    ],
    "deliverable": "server_single.py, server_threaded.py, timing notes from the curl experiments, and findings.md with the mechanism and fixes.",
    "checkpoint": "Single-threaded /healthz demonstrably blocks behind /work (~5s); threaded /healthz answers in milliseconds during /work; findings.md names the readiness-probe cascade and all three fixes."
  },
  "mockTask": {
    "id": "il28-m20-mock",
    "type": "choice",
    "q": "Panel: 'Your Python API passes health checks at low traffic but fails readiness probes under load. The Java service next to it is fine. Diagnose it.'",
    "choices": ["Python is too slow — rewrite in Java", "The single-threaded server queues probe requests behind slow work until they time out; fix with concurrent serving, a trivially cheap /healthz, and downstream timeouts", "Increase the readiness failureThreshold until it passes", "Delete the readiness probe so Kubernetes stops checking"],
    "answer": 1,
    "explain": "Queueing behind slow requests is the mechanism; Java survives via concurrent request handling. The fix is concurrent probe serving plus cheap health endpoints plus timeouts — not masking the probe or rewriting the service."
  },
  "crossLinks": [],
  "videos": [
    {"title": "Python Threading Tutorial: Run Code Concurrently", "url": "https://www.youtube.com/watch?v=IEEhzQoKtQU", "source": "Corey Schafer (YouTube)", "durationMin": 30, "order": 1, "watchBefore": "notes", "blurb": "Practical threading tutorial — threads, locks, and thread pools — the concurrency model behind the probe experiments in this module."}
  ],
  "estimatedMinutes": 0
}
