module = {
  "id": "IL28-M22",
  "code": "IL-28",
  "title": "Docker: Images, Layers & the Dockerfile",
  "summary": "Learn what container images really are — stacked read-only layers plus a thin writable top — and write Dockerfiles with correct FROM, RUN, COPY, CMD, and ENTRYPOINT instructions ordered for maximum layer-cache reuse.",
  "objectives": [
    "Distinguish images (immutable templates) from containers (running instances).",
    "Explain what RUN does: each invocation creates a new image layer.",
    "Write a Dockerfile using FROM, WORKDIR, COPY, ADD, EXPOSE, CMD, and ENTRYPOINT correctly.",
    "Choose between CMD and ENTRYPOINT, and between exec form and shell form.",
    "Order Dockerfile instructions to maximize layer-cache hits and speed up rebuilds."
  ],
  "notes": [
    {
      "title": "Image vs container: template vs running instance",
      "body": """An image is an immutable template: a stack of read-only filesystem layers plus metadata (which command to run, which ports to expose, which environment variables to set). A container is a running instance of an image — the same layers plus a thin writable layer on top and an isolated process namespace. The analogy panels accept: the image is the class, the container is the object. Worked example:

$ docker images
REPOSITORY   TAG     IMAGE ID       SIZE
healthcheck  v1      a91c3e27f104   148MB
$ docker run -d --name hc1 healthcheck:v1
$ docker run -d --name hc2 healthcheck:v1

Both containers share the identical read-only image layers on disk — starting hc2 costs almost nothing extra because only its thin writable layer is new. Delete a container and its writable layer vanishes; the image is untouched. This is why images are the unit of distribution (pushed to registries, scanned for vulnerabilities, promoted through environments) while containers are the unit of execution (started, stopped, replaced). A direct consequence: never store data you need to keep inside a container's writable layer — it dies with the container. Persistent data belongs in volumes (M24). And \"it works on my machine\" dies here too: the image carries the OS libraries, the language runtime, and the pinned dependencies, so the artifact that passed CI is byte-identical to the one running in production."""
    },
    {
      "title": "FROM and WORKDIR: the foundation of every Dockerfile",
      "body": """FROM sets the base image — the starting layer stack your image builds on — and every Dockerfile begins with it. Choose the base deliberately: python:3.12-slim for Python apps (small, Debian-based), or a fuller variant only if you need compilation toolchains. Pin the tag (python:3.12-slim, not python:latest) for the same reproducibility reason you pin pip packages: latest floats, and a rebuild next month may pull a different base. WORKDIR sets the working directory for all following instructions — and creates it if missing. Worked example:

FROM python:3.12-slim
WORKDIR /app

Every subsequent RUN, COPY, and CMD now executes relative to /app, and the directory exists in the image. Without WORKDIR, files scatter across / and COPY destinations become ambiguous — a common beginner defect. Two professional rules: prefer official images (the library/ namespace on Docker Hub) because they are maintained, scanned, and documented; and treat the base image as a dependency to be updated deliberately — schedule base-image refreshes, test, and re-pin, rather than letting a floating tag change your runtime underneath you. The base you choose determines your image's OS libraries, security patch level, and starting size, so it is an architecture decision, not a formality."""
    },
    {
      "title": "What RUN really does: one instruction, one layer",
      "body": """This is the panel question, so learn it precisely: each RUN instruction executes a command in a temporary container based on the previous layer, then commits the resulting filesystem diff as a brand-new read-only layer. The Dockerfile is a recipe for stacking layers. Worked example:

FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir requests==2.32.3
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

Then inspect:

$ docker build -t demo:v1 .
$ docker history demo:v1

The history output shows one row per layer: the base image's layers, then a layer for the pip install, then a layer for the apt-get line — each with its size. Solution insight: docker history is the proof — count the rows and they match your RUN count (plus base). Two consequences follow. First, layers are immutable and content-addressed: identical instruction + identical parent layer = identical layer, which is what makes the build cache work. Second, everything a RUN downloads or creates lives in its layer forever (the whiteout lesson in M23) — which is why the apt-get example chains update, install, and cleanup in a SINGLE RUN: split across three RUNs, the package lists would persist in an intermediate layer even after the rm. Combine related operations in one RUN, joined with && so a failure aborts the whole step."""
    },
    {
      "title": "COPY vs ADD: prefer the obvious one",
      "body": """COPY and ADD both place files into the image, but they differ in exactly two ways — and the guidance is simple: use COPY unless you specifically need ADD's extras. COPY takes files from the build context (the directory you build from) and places them at the destination: COPY requirements.txt . copies one file; COPY . . copies the whole context. ADD does the same plus two magic behaviors: it auto-extracts local tar archives, and it can fetch remote URLs. Worked example of the preferred pattern:

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

This two-step COPY is deliberate layer-cache strategy (next note): dependencies install in their own layer, so editing app code later does not re-run pip. The ADD trap: ADD https://example.com/tool.tar.gz /tmp/ fetches at build time with no checksum verification and no cache invalidation control — the layer cache cannot know the remote changed, so rebuilds silently reuse stale bytes. Professionals fetch remote artifacts with RUN curl plus a checksum check instead, keeping every input explicit and verifiable. Rule: COPY for files, RUN curl for downloads, ADD almost never. One more sharp edge: COPY follows .dockerignore (M23) — without it, your .git directory and local virtualenv ride into the image, bloating it and possibly leaking secrets."""
    },
    {
      "title": "CMD vs ENTRYPOINT: defaults vs the fixed command",
      "body": """CMD and ENTRYPOINT together define what runs when the container starts, and panels probe the difference relentlessly. ENTRYPOINT is the fixed executable — it always runs. CMD provides the default arguments — appended to the entrypoint, and overridden by arguments on docker run. Worked example:

ENTRYPOINT [\"python\", \"app.py\"]
CMD [\"--port\", \"8080\"]

docker run myimage runs python app.py --port 8080; docker run myimage --port 9090 runs python app.py --port 9090 — the CMD defaults were replaced. If you instead wrote only CMD [\"python\", \"app.py\", \"--port\", \"8080\"], then docker run myimage /bin/sh would drop your app entirely and run a shell — CMD is fully replaceable, ENTRYPOINT is not. The second axis is form: the exec form [\"python\", \"app.py\"] runs the binary directly as PID 1, while the shell form CMD python app.py wraps it as /bin/sh -c \"python app.py\". The shell wrapper breaks signal handling — docker stop sends SIGTERM to the shell, not your app, so graceful shutdown fails and stops hang until the kill timeout. Professional default: exec-form ENTRYPOINT for the fixed command, exec-form CMD for overridable defaults, shell form never in production images. Verify with docker inspect: Entrypoint and Cmd are separate fields in the image config."""
    },
    {
      "title": "EXPOSE and layer-cache ordering: fast rebuilds by design",
      "body": """EXPOSE documents which port the container listens on (EXPOSE 8080) — it is metadata, not a firewall rule: the port is only reachable from outside via docker run -p. Its real value is documentation and tooling: orchestrators and docker run -P read it. The performance topic is layer-cache ordering. Docker caches each layer and reuses it when the instruction and its inputs are unchanged; the first changed instruction invalidates that layer and every layer after it. Worked example — the wrong order:

COPY . .
RUN pip install -r requirements.txt

Every code edit changes the COPY layer, invalidating the pip layer below it — a full dependency reinstall on each build. The right order:

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

requirements.txt changes rarely, so the expensive pip layer stays cached across dozens of code edits; only the final cheap COPY re-runs. Solution check: build twice with no changes and watch docker build report \"CACHED\" for every step; then touch app.py, rebuild, and confirm only the last COPY re-ran. Generalize the principle: order instructions from least-frequently-changed to most-frequently-changed — base image, system packages, language dependencies, then application code. A Dockerfile ordered this way turns a 4-minute rebuild into a 10-second one, which compounds across every CI run, every developer, every day."""
    }
  ],
  "cards": [
    {"front": "What is the difference between an image and a container?", "back": "An image is the immutable template (read-only layers + metadata); a container is a running instance — the image layers plus a thin writable layer and an isolated process."},
    {"front": "Panel: what does RUN do in a Dockerfile?", "back": "Each RUN executes in a temp container from the previous layer and commits the filesystem diff as a new read-only layer — one RUN, one layer."},
    {"front": "How do you prove how many layers an image has?", "back": "docker history <image> — one row per layer, matching your RUN/COPY/FROM count plus base layers."},
    {"front": "Why chain apt-get update, install, and cleanup in a single RUN?", "back": "Layers are immutable — split across RUNs, the package lists persist in an intermediate layer even after a later rm; one RUN keeps them out of the final image."},
    {"front": "COPY vs ADD — which do you prefer and why?", "back": "COPY for files. ADD's extras (auto-extract, remote URLs) hide behavior; fetch remotes with RUN curl + checksum instead."},
    {"front": "What is the difference between CMD and ENTRYPOINT?", "back": "ENTRYPOINT is the fixed executable that always runs; CMD supplies default arguments appended to it, fully overridden by docker run arguments."},
    {"front": "Exec form vs shell form — which for production, and why?", "back": "Exec form ([\"python\",\"app.py\"]) — it runs the binary directly as PID 1. Shell form wraps in /bin/sh -c, breaking signal handling so docker stop hangs."},
    {"front": "Does EXPOSE publish a port to the host?", "back": "No — it is documentation/metadata. Reachability needs docker run -p (or -P, which uses EXPOSE)."},
    {"front": "What invalidates the Docker build cache?", "back": "The first instruction whose inputs changed invalidates its layer and every layer after it — hence order least-changed first."},
    {"front": "Why COPY requirements.txt before COPY . . ?", "back": "Dependencies change rarely, so the expensive pip-install layer stays cached across code edits; only the final cheap COPY re-runs."},
    {"front": "Should you use python:latest as a base? Why not?", "back": "No — latest floats, so rebuilds may pull a different runtime. Pin the tag (python:3.12-slim) like any other dependency."},
    {"front": "Where does data a container must keep belong?", "back": "In a volume, not the container's writable layer — the writable layer dies with the container."}
  ],
  "quiz": [
    {"q": "Two containers run from the same image. What do they share on disk?", "choices": ["Nothing — each gets a full copy", "The read-only image layers; each has only its own thin writable layer", "The writable layer too", "Only the metadata"], "answer": 1, "explain": "Image layers are shared read-only; starting a second container costs only its thin writable layer."},
    {"q": "Panel: what does RUN do in a Dockerfile?", "choices": ["It runs a command when the container starts", "Each RUN executes against the previous layer and commits the diff as a new read-only layer", "It downloads the base image", "It sets an environment variable"], "answer": 1, "explain": "One RUN = one new immutable layer stacked on the previous one; docker history proves it."},
    {"q": "A Dockerfile has three RUN instructions. How many layers do they add?", "choices": ["One — they merge", "Three — one per RUN", "Zero — RUN does not create layers", "It depends on caching"], "answer": 1, "explain": "Each RUN commits its own layer regardless of caching; caching only decides whether the layer is rebuilt or reused."},
    {"q": "Why is 'RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*' one RUN instead of three?", "choices": ["It runs faster", "Split across RUNs, the package lists would persist in an intermediate layer despite the later rm", "apt-get requires it", "Fewer lines look cleaner"], "answer": 1, "explain": "Layers are immutable — a later rm cannot shrink an earlier layer, so cleanup must happen in the same RUN that created the files."},
    {"q": "When should you use ADD instead of COPY?", "choices": ["Always — ADD is newer", "Almost never; COPY for files, RUN curl + checksum for remote artifacts", "ADD is faster for large files", "When copying from Windows"], "answer": 1, "explain": "ADD's magic (auto-extract, remote fetch without verification) hides behavior; explicit COPY/curl is reviewable."},
    {"q": "ENTRYPOINT [\"python\",\"app.py\"] and CMD [\"--port\",\"8080\"]. What does 'docker run img --port 9090' execute?", "choices": ["python app.py --port 8080", "python app.py --port 9090", "--port 9090", "It errors — CMD cannot be overridden"], "answer": 1, "explain": "Run arguments replace CMD defaults and are appended to the fixed ENTRYPOINT."},
    {"q": "Why is shell-form CMD a problem for docker stop?", "choices": ["It is slower to start", "SIGTERM goes to the /bin/sh wrapper, not your app, so graceful shutdown fails", "Shell form is deprecated", "It uses more memory"], "answer": 1, "explain": "The shell wrapper becomes PID 1 and does not forward signals; exec form runs your binary as PID 1 directly."},
    {"q": "COPY . . comes before RUN pip install. Every code edit triggers a full pip reinstall. Fix?", "choices": ["Combine them into one RUN", "COPY requirements.txt and RUN pip install first, then COPY . . last", "Remove the COPY", "Use ADD instead"], "answer": 1, "explain": "Order least-changed first: the rarely-changing dependency layer stays cached while code edits only re-run the final COPY."},
    {"q": "Does EXPOSE 8080 make the port reachable from the host?", "choices": ["Yes, automatically", "No — it is metadata; use docker run -p to publish", "Only with --network host", "Only on Linux"], "answer": 1, "explain": "EXPOSE documents intent; publishing is a separate runtime flag."}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL28-M23"],
  "drills": [
    {
      "id": "il28-m22-dockerfile",
      "title": "Dockerfile authoring drill",
      "items": [
        {"prompt": "Write the first two lines of a Dockerfile for a Python app pinned to 3.12-slim with workdir /app.", "answer": "FROM python:3.12-slim\nWORKDIR /app", "explain": "Pinned base for reproducibility; WORKDIR creates and sets the working directory for all following instructions."},
        {"prompt": "Order these for cache efficiency: COPY . ., RUN pip install -r requirements.txt, COPY requirements.txt .", "answer": "COPY requirements.txt . → RUN pip install -r requirements.txt → COPY . .", "explain": "Least-changed first: dependency layer stays cached across code edits."},
        {"prompt": "Install curl in the image without leaving apt lists behind. Write the RUN.", "answer": "RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*", "explain": "Single RUN so cleanup lands in the same layer as the lists; && aborts on failure."},
        {"prompt": "Set a fixed executable python app.py with overridable default arg --port 8080, exec form.", "answer": "ENTRYPOINT [\"python\", \"app.py\"]\nCMD [\"--port\", \"8080\"]", "explain": "ENTRYPOINT is fixed; CMD defaults are appended and replaceable at docker run."},
        {"prompt": "How do you prove an image's layer count and sizes?", "answer": "docker history <image> — one row per layer with sizes.", "explain": "History exposes the layer stack the Dockerfile recipe produced."},
        {"prompt": "A build copies the local .venv into the image. What is wrong and what is the fix?", "answer": "Bloat and possible secret leakage; fix with .dockerignore excluding .venv (and .git).", "explain": "Build context hygiene — covered fully in M23."},
        {"prompt": "docker run myimg /bin/bash starts a shell instead of the app. Which instruction did the author use, and what is the alternative?", "answer": "They used CMD (fully replaceable); ENTRYPOINT would have kept the app as the fixed executable.", "explain": "CMD vs ENTRYPOINT semantics in one symptom."}
      ]
    },
    {
      "id": "il28-m22-image-container",
      "title": "Image vs container drill",
      "items": [
        {"prompt": "Define image and container in one sentence each.", "answer": "Image: immutable template of read-only layers plus metadata. Container: a running instance — those layers plus a thin writable layer and an isolated process.", "explain": "Template versus instance; the class/object analogy."},
        {"prompt": "You docker exec into a container, create /tmp/data.txt, then remove the container. Where is the file?", "answer": "Gone — it lived in the container's writable layer, which dies with the container.", "explain": "Writable layers are ephemeral; volumes persist."},
        {"prompt": "Which is the unit of distribution and which the unit of execution?", "answer": "Image: distribution (registries, scanning, promotion). Container: execution (start, stop, replace).", "explain": "You ship images; you run containers."},
        {"prompt": "Why does 'works on my machine' die with images?", "answer": "The image carries OS libs, runtime, and pinned deps — CI-tested bytes are identical to production bytes.", "explain": "The environment ships with the artifact."},
        {"prompt": "docker images shows healthcheck v1 at 148MB. You start 5 containers. Roughly how much extra disk?", "answer": "Almost nothing beyond 148MB — the image layers are shared; only five thin writable layers are added.", "explain": "Layer sharing makes containers cheap to start."},
        {"prompt": "Name two reasons to prefer official base images.", "answer": "They are maintained/scanned/documented, and their tags are trustworthy for pinning.", "explain": "Supply-chain hygiene starts at FROM."},
        {"prompt": "How should base-image updates be handled?", "answer": "Deliberately: schedule refreshes, test, re-pin — never let a floating tag change the runtime silently.", "explain": "The base is a dependency with the same discipline as pip pins."}
      ]
    }
  ],
  "handsOnLab": {
    "id": "il28-m22-lab",
    "title": "Dockerfile, layers, and cache",
    "brief": "You will containerize the M19 health-check script, inspect its layers with docker history, prove the cache works by rebuilding, then break the cache order deliberately and measure the cost.",
    "steps": [
      "Set up: mkdir docker-lab && cd docker-lab; copy your healthcheck.py and requirements.txt from the M19 lab (or recreate minimal versions).",
      "Write the Dockerfile: FROM python:3.12-slim, WORKDIR /app, COPY requirements.txt ., RUN pip install --no-cache-dir -r requirements.txt, COPY . ., EXPOSE 8080, exec-form CMD.",
      "Build: docker build -t healthcheck:v1 . — read the output and note each step.",
      "Inspect layers: run docker history healthcheck:v1 and map each row to a Dockerfile instruction.",
      "Run it: docker run --rm healthcheck:v1 https://httpbin.org/status/200 — confirm OK output; then docker inspect healthcheck:v1 and find the Cmd/Entrypoint fields.",
      "Prove the cache: run docker build -t healthcheck:v1 . again with no changes — confirm every step reports CACHED.",
      "Touch only the code: append a comment to healthcheck.py, rebuild, and confirm only the final COPY step re-ran.",
      "Break the order: temporarily rewrite the Dockerfile with COPY . . before RUN pip install, rebuild twice (once to populate, once after touching healthcheck.py), and observe pip reinstalling — then restore the good order.",
      "Shell-form demo: build a variant with shell-form CMD, run docker stop against a sleeping variant, and note the delayed stop versus exec form.",
      "Write layers.md: your docker history mapping, the cache experiment results, and the one-sentence RUN/layer rule."
    ],
    "deliverable": "Dockerfile (good order), healthcheck.py, requirements.txt, layers.md with the history mapping and cache experiment notes.",
    "checkpoint": "docker history rows map 1:1 to instructions; no-change rebuild is fully CACHED; code-touch rebuild re-runs only the last COPY; layers.md states the one-RUN-one-layer rule."
  },
  "mockTask": {
    "id": "il28-m22-mock",
    "type": "choice",
    "q": "Panel: 'Your Dockerfile copies the whole repo, then pip-installs, and every tiny code change triggers a 3-minute rebuild. Diagnose and fix.'",
    "choices": ["Add more RUN layers to parallelize", "Reorder: COPY requirements.txt + RUN pip install first (cached), COPY . . last — so code edits only re-run the final cheap layer", "Switch to ADD for faster copies", "Use python:latest to speed up pulls"],
    "answer": 1,
    "explain": "Cache invalidation flows downward: the early COPY . . invalidated the pip layer on every edit. Least-changed-first ordering keeps the expensive dependency layer cached."
  },
  "crossLinks": [],
  "videos": [
    {"title": "Docker Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo", "source": "freeCodeCamp.org (YouTube)", "durationMin": 123, "order": 1, "watchBefore": "notes", "blurb": "Hands-on Docker course covering images, containers, and Dockerfiles — the practical companion to this module's layer model."}
  ],
  "estimatedMinutes": 0
}
