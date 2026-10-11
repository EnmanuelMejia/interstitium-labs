module = {
  "id": "IL28-M23",
  "code": "IL-28",
  "title": "Multi-Stage Builds & Image Optimization",
  "summary": "Shrink images dramatically with multi-stage builds, minimal bases, and .dockerignore — and master the panel's favorite Docker questions: the whiteout lesson, the 'echo hello' trap, and measuring what each layer costs.",
  "objectives": [
    "Write multi-stage Dockerfiles that keep build tooling out of the runtime image.",
    "Choose minimal base images and justify the trade-offs.",
    "Use .dockerignore to control the build context and keep secrets out of images.",
    "Explain the whiteout lesson: deleting files in a later layer does not shrink the image.",
    "Measure image and layer sizes with docker images, docker history, and docker system df."
  ],
  "notes": [
    {
      "title": "Multi-stage builds: ship the artifact, not the toolchain",
      "body": """A multi-stage Dockerfile uses multiple FROM instructions: early stages build the artifact with the full toolchain, and the final stage copies only the artifact into a lean runtime image. Everything left behind in earlier stages never ships. Worked example — the Go port-checker from M21:

# Build stage: full toolchain
FROM golang:1.23 AS builder
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /portcheck .

# Runtime stage: only the binary
FROM scratch
COPY --from=builder /portcheck /portcheck
ENTRYPOINT [\"/portcheck\"]

Solution walkthrough: the builder stage (hundreds of MB: compiler, module cache) compiles a static binary; the final stage starts FROM scratch — literally empty — and copies in just /portcheck. The published image is a few MB: no Go toolchain, no source, no module cache. COPY --from=builder is the bridge between stages, and naming stages with AS makes the intent readable. The same pattern serves compiled languages and frontend builds alike (node:slim builds the bundle, nginx:alpine serves it). Panel framing: \"multi-stage separates build-time dependencies from runtime dependencies at the image layer.\" Without it, teams ship compilers and caches to production — larger attack surface, slower pulls, slower deploys. Verify the win with docker images: compare the builder-stage size against the final."""
    },
    {
      "title": "Minimal bases: scratch, distroless, alpine, slim",
      "body": """The base image sets your floor for size and attack surface, and the options form a spectrum. scratch is empty — nothing but what you copy in; ideal for static binaries, but there is no shell for debugging. Distroless images add just a runtime (language libs, CA certs) with no shell or package manager — a strong default for dynamic languages. Alpine is a tiny full Linux (~5MB) with a shell and apk — great for debugging, though its musl libc occasionally surprises glibc-linked binaries. Slim variants (python:3.12-slim) drop the compiler toolchain but keep a familiar Debian userland. Worked example of the decision:

# Needs a shell for debugging and apk for packages:
FROM python:3.12-alpine
# Static Go binary, no shell needed:
FROM scratch

There is no universally right answer — only trade-offs to defend. Smaller base means faster pulls (matters enormously at scale: a 1GB image pulled by 500 nodes is 500GB of transfer), fewer packages to patch, and fewer CVEs for scanners to flag. But an image you cannot debug at 3 a.m. has its own cost, which is why many teams standardize on slim/distroless for production and keep a debug variant with a shell. The panel expects you to name the spectrum and argue a choice for a given workload, not to recite a favorite."""
    },
    {
      "title": ".dockerignore: control the build context",
      "body": """docker build sends the entire build context directory to the daemon before the first instruction runs — including your .git history, local virtualenvs, .env files with secrets, and editor swap files. .dockerignore filters that context, exactly like .gitignore filters commits. Worked example for a Python project:

.git
.venv
__pycache__
*.pyc
.env
*.log
Dockerfile

Solution walkthrough: .git alone can be hundreds of MB — excluding it slashes context transfer time on every build; .venv and __pycache__ are local artifacts that must never ship; .env exclusion is a security control, because anything COPY . . would otherwise bake secrets into a layer (and layers are forever — a secret in any layer is in the image permanently, retrievable with docker save). Two verifications: run docker build and watch the \"transferring context\" size drop, and audit with a temporary RUN find / -name \"*.env\" in a test build. Professional rule: every repo with a Dockerfile gets a .dockerignore from day one, reviewed like code — because the build context is an input to your supply chain, and unfiltered inputs are how secrets leak into registries."""
    },
    {
      "title": "The whiteout lesson: later deletes do not shrink earlier layers",
      "body": """This is the panel's favorite Docker trap, so learn the mechanism: layers are immutable, and deleting a file in a later layer only adds a whiteout marker that hides the file in the merged view — the bytes remain in the earlier layer, and the image stays the same size. Worked example — the wrong way:

FROM python:3.12-slim
WORKDIR /app
RUN dd if=/dev/zero of=/tmp/blob bs=1M count=100
RUN rm /tmp/blob

Build it and run docker images: the image is ~100MB larger than the base, even though /tmp/blob no longer exists in the running container. The rm layer contains only a whiteout file saying \"/tmp/blob is deleted\"; the 100MB of zeros sit untouched in the previous layer. Now the right way — one RUN:

RUN dd if=/dev/zero of=/tmp/blob bs=1M count=100 && rm /tmp/blob

The file is created and deleted inside the same layer commit, so it never persists — image size unchanged. This is exactly why the M22 apt-get pattern chains update, install, and cleanup with && in one RUN. The panel question \"does removing files in a later layer reduce image size?\" expects: no — whiteout hides but does not delete; only same-layer cleanup (or multi-stage, or squashing) actually shrinks the image. Verify any claim with docker history: the layer sizes do not lie."""
    },
    {
      "title": "The 'echo hello' trap: replacing cleanup grows the image",
      "body": """A panel variant of the whiteout lesson: take a Dockerfile whose RUN does install-then-cleanup, replace the cleanup step with RUN echo hello, and ask what happens to the image size. Worked example:

# Original
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Modified: cleanup replaced
RUN apt-get update && apt-get install -y curl
RUN echo hello

Solution: the image grows by the size of /var/lib/apt/lists/* (tens of MB). Walkthrough: the first RUN's layer permanently contains the downloaded package lists; the second RUN adds a tiny layer with hello's output and changes nothing about the first. Replacing cleanup with an unrelated command does not remove the files — layers are append-only history. The general principle: every byte written by a RUN lives in that RUN's layer forever, so cleanup must happen in the same RUN that created the mess, joined with && so failures abort before the commit. Related panel follow-up: \"how would you actually shrink it?\" — rewrite as a single RUN with the rm restored, or restructure with multi-stage so the package manager never appears in the final image at all. When optimizing, always measure before and after with docker images; intuition about sizes is unreliable, the numbers are not."""
    },
    {
      "title": "Measuring: docker images, history, and system df",
      "body": """Optimization without measurement is guessing. Three commands form the measurement toolkit. docker images shows repository, tag, and total size per image — your before/after scoreboard. docker history <image> breaks that total into per-layer rows with sizes and the creating command — your profiler, showing exactly which instruction costs what. docker system df reports overall disk usage: images, containers, build cache, and how much is reclaimable. Worked example — the optimization loop:

$ docker build -t api:naive -f Dockerfile.naive .
$ docker build -t api:opt -f Dockerfile.opt .
$ docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}'
api:naive 1.12GB
api:opt 142MB
$ docker history api:naive --format '{{.CreatedBy}} {{.Size}}' | sort -k2 -h | tail -3

Solution walkthrough: the scoreboard proves the 8x win; the history tail names the three most expensive layers (usually a fat base, an uncached pip install, and a COPY of unfiltered context) — each maps to a fix from this module (minimal base, cache-ordered deps, .dockerignore). Workflow discipline: measure the naive build first, change one thing, rebuild, compare. docker system df -v goes deeper per-object when hunting a disk-full builder, and docker builder prune reclaims cache deliberately — never on a shared CI builder without coordination. Panels respect engineers who quote their numbers: \"multi-stage took us from 1.1GB to 142MB\" beats \"we optimized the image.\""""
    }
  ],
  "cards": [
    {"front": "What is a multi-stage Dockerfile, and what problem does it solve?", "back": "Multiple FROM stages: early stages build with the full toolchain, the final stage copies only the artifact in — build tooling never ships to production."},
    {"front": "What does COPY --from=builder /portcheck /portcheck do?", "back": "Copies the built binary from the named builder stage into the final stage's filesystem."},
    {"front": "Order these bases by size/simplicity: scratch, distroless, alpine, slim.", "back": "scratch (empty) < distroless (runtime only, no shell) < alpine (tiny full Linux) < slim (Debian minus toolchain). Smaller = faster pulls, fewer CVEs, harder to debug."},
    {"front": "What does .dockerignore do, and name three things that belong in it.", "back": "Filters the build context sent to the daemon: .git, .venv, .env (secrets must never bake into layers)."},
    {"front": "Panel: does removing a file in a later layer shrink the image?", "back": "No — the delete only adds a whiteout marker hiding the file; the bytes remain in the earlier immutable layer and the size is unchanged."},
    {"front": "How do you actually remove the bytes, then?", "back": "Create and delete in the same RUN (&& chained), or restructure with multi-stage so the files never enter the final image."},
    {"front": "Panel: you replace a RUN's cleanup step with 'RUN echo hello'. What happens to image size?", "back": "It grows — the files the cleanup would have removed persist in the earlier layer; the echo layer changes nothing about them."},
    {"front": "Which three commands measure image/layer/disk usage?", "back": "docker images (per-image totals), docker history (per-layer sizes + creating command), docker system df (overall reclaimable usage)."},
    {"front": "Why is a secret in any image layer a permanent leak?", "back": "Layers are immutable and ship with the image — anyone with the image can extract the layer's bytes (e.g. via docker save)."},
    {"front": "A 1GB image is pulled by 500 nodes. Why does base-image size matter?", "back": "That is ~500GB of transfer plus slower rollouts — minimal bases directly cut pull time, disk, and patch surface at scale."},
    {"front": "What is the optimization loop you should follow?", "back": "Measure the naive build (docker images/history), change one thing, rebuild, compare — quote the numbers."},
    {"front": "When is alpine a risky base choice?", "back": "Its musl libc can surprise glibc-linked binaries — test compatibility; otherwise it is a fine tiny base with a shell."}
  ],
  "quiz": [
    {"q": "What is the core benefit of a multi-stage Dockerfile?", "choices": ["Faster syntax highlighting", "Build tooling stays in early stages; the final image contains only the runtime artifact", "It enables multiple entrypoints", "It removes the need for a base image"], "answer": 1, "explain": "Stages separate build-time from runtime dependencies at the image layer — compilers and caches never ship."},
    {"q": "In a Go multi-stage build, why can the final stage be FROM scratch?", "choices": ["Go binaries are interpreted", "A static Go binary needs no OS userland — just copy the binary in", "scratch includes Go", "It cannot — scratch is invalid"], "answer": 1, "explain": "CGO_ENABLED=0 produces a static binary with no libc dependency, so an empty base suffices."},
    {"q": "Which .dockerignore entry is a security control, and why?", "choices": [".venv — it is large", ".env — otherwise secrets bake into immutable layers permanently", "*.log — logs are noisy", "Dockerfile — it is metadata"], "answer": 1, "explain": "Anything copied into a layer ships forever; .env exclusion keeps secrets out of the image supply chain."},
    {"q": "Panel: RUN downloads a 100MB file, and a later RUN deletes it. Final image size impact?", "choices": ["Unchanged — the delete reclaims it", "+100MB — the whiteout hides the file but the bytes persist in the earlier layer", "+200MB", "The build fails"], "answer": 1, "explain": "Immutable layers: the later rm only adds a whiteout marker; measure with docker history to see the layer still holding 100MB."},
    {"q": "How do you make the 100MB actually disappear?", "choices": ["Run docker prune", "Download and delete in the same RUN, or use multi-stage", "Use ADD instead of RUN", "Delete it at container runtime"], "answer": 1, "explain": "Same-layer cleanup never commits the bytes; multi-stage keeps them out of the final image entirely."},
    {"q": "Panel: replacing '&& rm -rf /var/lib/apt/lists/*' with 'RUN echo hello' — image size?", "choices": ["Shrinks — echo is tiny", "Grows by the apt lists size — the cleanup no longer happens and layers are append-only", "Unchanged", "The build errors"], "answer": 1, "explain": "The package lists persist in their layer; the echo layer cannot remove them."},
    {"q": "docker history shows one 900MB layer from 'COPY . .'. Most likely cause and fix?", "choices": ["Base image is fat — change FROM", "Unfiltered build context (.git, .venv) — add .dockerignore", "Too many RUN instructions", "EXPOSE is wrong"], "answer": 1, "explain": "A giant COPY layer means the context carried junk; .dockerignore is the fix."},
    {"q": "Why might a team standardize on distroless for production but keep a debug variant?", "choices": ["Distroless is faster to build", "Distroless minimizes attack surface; the debug variant keeps a shell for 3 a.m. troubleshooting", "Debug variants are smaller", "Distroless includes more tools"], "answer": 1, "explain": "The trade-off is explicit: minimal surface in prod, debuggability when incidents strike."},
    {"q": "Before/after: 1.12GB → 142MB via multi-stage. What proved the win?", "choices": ["docker ps", "docker images size comparison plus docker history identifying the expensive layers", "The build log timestamps", "docker exec"], "answer": 1, "explain": "images gives the scoreboard; history profiles which layers cost what — measurement, not intuition."}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL28-M24"],
  "drills": [
    {
      "id": "il28-m23-whiteout-panel",
      "title": "Whiteout and optimization — panel drill",
      "items": [
        {"prompt": "Panel: 'Does removing files in a later layer reduce image size?' Give the full answer.", "answer": "No. Layers are immutable; the delete adds only a whiteout marker hiding the file, while the bytes persist in the earlier layer. Prove it with docker history showing the layer size unchanged.", "explain": "Mechanism (whiteout) + proof (history) is the complete panel answer."},
        {"prompt": "Panel: 'You replaced the cleanup step with RUN echo hello. What happens to size?'", "answer": "It grows by whatever the cleanup would have removed — layers are append-only, so the echo layer cannot delete the earlier layer's files.", "explain": "The trap variant: cleanup must happen in the creating RUN."},
        {"prompt": "Write the correct apt-get RUN that leaves no package lists behind.", "answer": "RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*", "explain": "Single RUN, && chaining so failure aborts before commit, cleanup in the same layer."},
        {"prompt": "Why does multi-stage beat even perfect single-stage cleanup for compiled apps?", "answer": "The compiler, source, and caches never enter the final image at all — cleanup can only remove files, multi-stage removes whole toolchains.", "explain": "Qualitative difference, not just tidier layers."},
        {"prompt": "Your final stage is FROM scratch. What must be true of the binary?", "answer": "It must be fully static (e.g. CGO_ENABLED=0 for Go) — scratch has no libc, no shell, nothing.", "explain": "Scratch works only when the artifact has zero runtime dependencies."},
        {"prompt": "Name the measurement commands and what each tells you.", "answer": "docker images: per-image totals (scoreboard). docker history: per-layer sizes and creating command (profiler). docker system df: overall reclaimable disk.", "explain": "Scoreboard, profiler, janitor."},
        {"prompt": "A reviewer says 'just use python:latest, it is always patched.' Your response?", "answer": "Floating tags break reproducibility — rebuilds silently change the runtime. Pin the base tag and schedule deliberate, tested refreshes instead.", "explain": "Same pinning discipline as pip, applied to the base image."}
      ]
    },
    {
      "id": "il28-m23-multistage-ignore",
      "title": "Multi-stage and context drill",
      "items": [
        {"prompt": "Sketch a multi-stage Dockerfile for a Go app: builder and scratch final.", "answer": "FROM golang:1.23 AS builder → WORKDIR, COPY go.mod, RUN go mod download, COPY ., RUN CGO_ENABLED=0 go build -o /app .; then FROM scratch → COPY --from=builder /app /app → ENTRYPOINT [\"/app\"]", "explain": "Toolchain in builder, static binary only in final."},
        {"prompt": "What does AS builder enable?", "answer": "Names the stage so later COPY --from=builder can reference it — readable and explicit.", "explain": "Named stages are the bridge mechanism."},
        {"prompt": "Write a .dockerignore for a Python repo and justify each line.", "answer": ".git (huge history), .venv (local env), __pycache__/*.pyc (build junk), .env (secrets must never layer), *.log, Dockerfile", "explain": "Size, hygiene, and the security control."},
        {"prompt": "How do you verify .dockerignore worked?", "answer": "Watch the 'transferring context' size drop on build, and audit with a test RUN find for excluded names.", "explain": "Measure the context, not just the image."},
        {"prompt": "Frontend pattern: node builds, nginx serves. Sketch the stages.", "answer": "FROM node:slim AS build → COPY, RUN npm ci && npm run build; FROM nginx:alpine → COPY --from=build /app/dist /usr/share/nginx/html", "explain": "Same pattern, different runtimes — toolchain never ships."},
        {"prompt": "When would you NOT use scratch for the final stage?", "answer": "When you need a shell, CA certs, or a language runtime at debug/run time — then distroless/alpine/slim.", "explain": "Scratch is for fully static artifacts; debuggability has value."},
        {"prompt": "docker system df shows 40GB reclaimable on a shared CI builder. What do you do?", "answer": "Coordinate first — docker builder prune affects everyone's cache; never prune a shared builder unilaterally.", "explain": "Cache is shared infrastructure; pruning is a team decision."}
      ]
    }
  ],
  "handsOnLab": {
    "id": "il28-m23-lab",
    "title": "Three builds, one scoreboard",
    "brief": "You will build naive, cleaned-up, and multi-stage variants of the same app, measure each with docker images and docker history, demonstrate the whiteout effect live, and record the numbers.",
    "steps": [
      "Set up: mkdir opt-lab && cd opt-lab; create app.py (a trivial HTTP server or the M19 healthcheck) and requirements.txt with one pinned dep.",
      "Write Dockerfile.naive: FROM python:3.12, separate RUNs for apt update/install (install curl) with no cleanup, COPY . . first then pip install (bad cache order), no .dockerignore.",
      "Build naive: docker build -t opt:naive -f Dockerfile.naive . ; record docker images size for opt:naive.",
      "Write Dockerfile.clean: FROM python:3.12-slim, single chained apt RUN with cleanup, COPY requirements.txt + pip install before COPY . ., plus a .dockerignore excluding .git/__pycache__/*.pyc.",
      "Build clean: docker build -t opt:clean -f Dockerfile.clean . ; record size; compare with naive.",
      "Whiteout demo: add to the naive variant 'RUN dd if=/dev/zero of=/tmp/blob bs=1M count=50' followed by 'RUN rm /tmp/blob'; rebuild and show via docker history that the layer (and image size) still carries ~50MB.",
      "Echo-hello demo: in a copy of the clean Dockerfile, replace the apt cleanup with a separate 'RUN echo hello'; rebuild and record the size increase.",
      "Multi-stage: write Dockerfile.multi for a static Go hello (or reuse portcheck): golang builder → scratch final; build and record the tiny final size.",
      "Profile: run docker history on each tag, identify the single most expensive layer per variant, and map it to its fix.",
      "Write sizes.md: the four image sizes, the whiteout/echo-hello deltas, and the one-paragraph whiteout explanation in your own words."
    ],
    "deliverable": "Dockerfile.naive, Dockerfile.clean, Dockerfile.multi, .dockerignore, and sizes.md with all measurements and the whiteout explanation.",
    "checkpoint": "sizes.md shows clean < naive, multi smallest; whiteout demo proves the rm layer did not shrink the image; echo-hello variant measurably larger than clean."
  },
  "mockTask": {
    "id": "il28-m23-mock",
    "type": "choice",
    "q": "Panel: 'Your production image is 1.1GB for a Go microservice. Walk me through shrinking it.'",
    "choices": ["Add RUN rm -rf on the build tools in the final layer", "Multi-stage: compile in a golang builder stage, copy the static binary into a scratch final stage; verify with docker images/history", "Compress the image with gzip before pushing", "Split the app into more layers"],
    "answer": 1,
    "explain": "Later-layer deletes cannot shrink earlier layers (whiteout); multi-stage keeps the toolchain out of the final image entirely — the only approach that actually removes the bytes. Measurement with docker images/history proves the win."
  },
  "crossLinks": [],
  "videos": [
    {"title": "Docker Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "source": "TechWorld with Nana (YouTube)", "durationMin": 125, "order": 1, "watchBefore": "notes", "blurb": "Comprehensive Docker course including multi-stage builds and best practices — pairs with this module's optimization techniques."}
  ],
  "estimatedMinutes": 0
}
