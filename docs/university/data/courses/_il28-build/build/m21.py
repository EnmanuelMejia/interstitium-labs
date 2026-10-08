module = {
  "id": "IL28-M21",
  "code": "IL-28",
  "title": "Go Essentials for Tooling",
  "summary": "Learn enough Go to build real operations tools: syntax, error handling, modules, and cross-compilation — and understand why so much cloud-native tooling (Docker, Kubernetes, Terraform) ships as single Go binaries.",
  "objectives": [
    "Explain why Go fits operations tooling: single static binaries, fast startup, strong stdlib.",
    "Write basic Go programs using packages, functions, slices, and maps.",
    "Handle errors the Go way with explicit multiple return values.",
    "Initialize a module and build a binary with the go toolchain.",
    "Cross-compile one codebase for Linux, Windows, and macOS targets."
  ],
  "notes": [
    {
      "title": "Why Go owns the ops-tooling niche",
      "body": """A remarkable share of cloud-native tooling — Docker, Kubernetes, Terraform, Prometheus — is written in Go, and the reasons are practical, not fashionable. First, Go compiles to a single statically linked binary: you ship one file with no runtime to install, no virtualenv to activate, no dependency tree to resolve on the target machine. Second, startup is instant — a Go CLI answers in milliseconds, while a JVM or Python-based tool pays interpreter or VM warmup on every invocation, which matters when the tool runs inside tight automation loops. Third, the standard library covers the ops basics out of the box: HTTP clients and servers, JSON, flags, templating, and cryptography, so small tools need zero third-party packages. Fourth, cross-compilation is a one-line environment change (next notes), so one codebase ships for every platform your fleet runs. Worked example of the payoff — the entire release process for the port-checker you will build in the lab is:

$ go build -o portcheck .

One command, one binary, runs anywhere. The trade-off to name honestly: Go is more verbose than Python for quick scripts, and its type system demands more upfront design. For a 20-line glue script, Python wins; for a tool you will distribute, run a million times, and maintain for years, Go's binary is the professional choice."""
    },
    {
      "title": "First Go program: packages, funcs, and types",
      "body": """Every Go program starts with package main and func main — the entry point the toolchain looks for. Variables declared with := get their type inferred; the fmt package handles formatted I/O. Worked example:

package main

import \"fmt\"

func main() {
    name := \"api\"
    port := 8080
    healthy := true
    fmt.Printf(\"%s listening on %d (healthy=%t)\\n\", name, port, healthy)
}

Solution: prints \"api listening on 8080 (healthy=true)\". Walkthrough: := declares and infers (string, int, bool); Printf verbs %s/%d/%t format each type; \\n is the newline. Key type facts: Go is statically typed — name cannot later hold an int, and the compiler rejects it. Integers have explicit sizes (int, int64); strings are immutable UTF-8 byte sequences; bool is a real type, not an int alias. Unused variables and imports are compile errors, not warnings — the compiler enforces hygiene. Run it without building via go run main.go. Two habits from day one: gofmt your code (go fmt ./...) so formatting debates never happen, and read compiler errors literally — Go's errors point at the exact line and are unusually actionable compared to template-heavy languages."""
    },
    {
      "title": "Slices, maps, and control flow",
      "body": """Go's workhorse data structures are slices (dynamic arrays) and maps (hash tables), with deliberately small control-flow syntax: for is the only loop, if requires no parentheses, switch is clean. Worked example:

package main

import \"fmt\"

func main() {
    hosts := []string{\"web1\", \"web2\", \"web3\"}
    status := map[string]string{\"web1\": \"up\", \"web2\": \"down\"}
    fmt.Println(len(hosts))
    fmt.Println(status[\"web2\"])
    for i, h := range hosts {
        fmt.Printf(\"%d: %s\\n\", i, h)
    }
}

Solution: prints 3, then \"down\", then \"0: web1\", \"1: web2\", \"2: web3\". Walkthrough: []string{\"web1\", ...} is a slice literal; map[string]string maps strings to strings; len works on slices; range yields index and value. Three sharp edges: indexing a missing map key returns the zero value (\"\" here) with no error — use the two-value form v, ok := status[\"web9\"] to detect absence; slices share backing arrays, so appending may or may not reallocate (copy when sharing matters); and range over a map visits keys in random order — never depend on map iteration order in output. For conditionals, if err != nil is the heartbeat of Go code (next note), and switch needs no break statements."""
    },
    {
      "title": "Error handling: explicit, not exceptional",
      "body": """Go has no exceptions. Functions return errors as ordinary values — usually the last return value — and callers check them explicitly. This makes failure handling visible in the code instead of hidden in stack unwinding, which is exactly what you want in automation that must degrade gracefully. Worked example:

package main

import (
    \"fmt\"
    \"strconv\"
)

func parsePort(s string) (int, error) {
    return strconv.Atoi(s)
}

func main() {
    port, err := parsePort(\"8080\")
    if err != nil {
        fmt.Println(\"bad port:\", err)
        return
    }
    fmt.Println(\"port:\", port)
}

Solution: prints \"port: 8080\". Walkthrough: parsePort returns (int, error); the caller binds both and branches on err != nil before touching port. The idiom if err != nil { ... } appears after nearly every fallible call — reading Go means scanning those branches to learn every failure mode the author considered. Conventions: error is the last return value; functions that cannot fail do not return one; sentinel errors and fmt.Errorf(\"dial %s: %w\", addr, err) with %w wrap context around root causes while preserving unwrapping. For CLIs, a fatal error usually means print to stderr and os.Exit(1) — nonzero exit codes are how automation detects your tool's failure, the same contract as the Python CLI in M19."""
    },
    {
      "title": "Modules and the build: go mod init to go build",
      "body": """Go modules are the dependency and build story: a go.mod file names your module and pins every dependency's version, giving reproducible builds like a requirements.txt with teeth. Worked example — from zero to binary:

$ mkdir portcheck && cd portcheck
$ go mod init example.com/portcheck
go: creating new go.mod: module example.com/portcheck
$ go run .
$ go build -o portcheck .
$ ./portcheck --help

Walkthrough: go mod init creates go.mod (module path plus go version); go run compiles to a temp binary and executes it — the fast edit loop; go build -o portcheck . produces the real distributable binary in the current directory. Dependencies enter via go get (e.g. go get github.com/spf13/cobra) and land pinned in go.mod with hashes in go.sum — commit both files, exactly like committing a pinned requirements.txt. go vet ./... runs the built-in static analyzer (catches Printf verb mismatches and suspicious constructs) and belongs in every CI pipeline; gofmt -l . lists unformatted files. No Makefile is needed for small tools — the toolchain is the build system. The mental model: go.mod is the contract, go.sum is the integrity proof, and the single binary is the artifact you ship to every machine in the fleet."""
    },
    {
      "title": "Cross-compilation and a real CLI: the port checker",
      "body": """Cross-compilation is Go's superpower for ops: set GOOS and GOARCH and the same source builds for another platform — no container, no VM, no cross toolchain to install. Worked example:

$ GOOS=linux GOARCH=amd64 go build -o portcheck-linux .
$ GOOS=windows GOARCH=amd64 go build -o portcheck.exe .
$ GOOS=darwin GOARCH=arm64 go build -o portcheck-mac .
$ file portcheck-linux
portcheck-linux: ELF 64-bit LSB executable, x86-64, statically linked

One codebase, three fleet-ready binaries. And here is the CLI itself, using only the stdlib flag package — the tool you will build in the lab:

package main

import (
    \"flag\"
    \"fmt\"
    \"net\"
    \"os\"
    \"time\"
)

func main() {
    host := flag.String(\"host\", \"localhost\", \"host to check\")
    port := flag.Int(\"port\", 80, \"port to check\")
    timeout := flag.Duration(\"timeout\", 5*time.Second, \"dial timeout\")
    flag.Parse()

    addr := fmt.Sprintf(\"%s:%d\", *host, *port)
    conn, err := net.DialTimeout(\"tcp\", addr, *timeout)
    if err != nil {
        fmt.Println(\"CLOSED:\", err)
        os.Exit(1)
    }
    conn.Close()
    fmt.Println(\"OPEN:\", addr)
}

Run ./portcheck -host db.internal -port 5432 -timeout 3s. Flags are pointers (*host dereferences); DialTimeout bounds the dial so a dead host fails in 3 seconds, not 2 minutes; exit 1 on closed keeps the CI contract. This is production-shaped Go: stdlib only, explicit errors, timeouts everywhere."""
    }
  ],
  "cards": [
    {"front": "Why is Go popular for operations tooling?", "back": "Single statically linked binary (nothing to install), instant startup, strong stdlib (HTTP, JSON, flags), and trivial cross-compilation."},
    {"front": "What do 'package main' and 'func main' signify?", "back": "They mark the program's entry point — the toolchain builds an executable starting at func main in package main."},
    {"front": "What does := do, and what is Go's stance on unused variables?", "back": ":= declares a variable with inferred type; unused variables or imports are compile errors, not warnings."},
    {"front": "How do you detect a missing key in a Go map?", "back": "Use the two-value form: v, ok := m[key] — ok is false when absent. Single-value indexing returns the zero value silently."},
    {"front": "How does Go signal errors, and what is the calling convention?", "back": "No exceptions — functions return error as (usually) the last value; callers check if err != nil before using the result."},
    {"front": "What does fmt.Errorf(\"dial %s: %w\", addr, err) accomplish?", "back": "Wraps the root error with context while %w preserves unwrapping, so callers can still inspect the original cause."},
    {"front": "What are go.mod and go.sum, and should you commit them?", "back": "go.mod names the module and pins dependency versions; go.sum holds integrity hashes — commit both for reproducible builds."},
    {"front": "What is the difference between go run and go build?", "back": "go run compiles to a temp binary and executes it (fast edit loop); go build produces the distributable binary file."},
    {"front": "Give the commands to cross-compile for Windows amd64 and macOS arm64.", "back": "GOOS=windows GOARCH=amd64 go build -o app.exe . and GOOS=darwin GOARCH=arm64 go build -o app-mac ."},
    {"front": "In the flag package, why do you write *host instead of host?", "back": "flag.String returns a *string pointer; you dereference it to get the value."},
    {"front": "Why does the port checker use net.DialTimeout instead of net.Dial?", "back": "DialTimeout bounds the dial so a dead host fails fast (e.g. 3s) instead of hanging for minutes — the timeouts-everywhere rule."},
    {"front": "What CI checks belong on every Go repo?", "back": "gofmt for formatting, go vet ./... for static analysis, and building (plus tests) on every change."}
  ],
  "quiz": [
    {"q": "What is the primary distribution advantage of a Go tool over a Python script?", "choices": ["Go is faster to write", "Go compiles to a single static binary with no runtime to install on targets", "Go has more libraries", "Go does not need a compiler"], "answer": 1, "explain": "One static binary ships and runs anywhere — no interpreter, virtualenv, or dependency install on the target machine."},
    {"q": "What does this print? name := \"api\"; port := 8080; fmt.Printf(\"%s:%d\", name, port)", "choices": ["api:8080", "api:%d", "A compile error — := needs types", "%s:8080"], "answer": 0, "explain": ":= infers string and int; %s formats the string, %d the integer."},
    {"q": "status := map[string]string{\"a\": \"up\"}; fmt.Println(status[\"b\"]). What prints and why?", "choices": ["A runtime panic", "An empty string — missing keys return the zero value", "nil", "A compile error"], "answer": 1, "explain": "Single-value map indexing on a missing key yields the zero value silently; use v, ok := status[\"b\"] to detect absence."},
    {"q": "A function returns (int, error). What is the idiomatic handling?", "choices": ["Use the int first, check err later", "if err != nil { handle it } before using the int", "Ignore err if the int looks right", "Wrap in try/catch"], "answer": 1, "explain": "Go has no exceptions; you must check err != nil explicitly before trusting the other return value."},
    {"q": "What does GOOS=windows GOARCH=amd64 go build -o app.exe . do?", "choices": ["Builds for the current machine only", "Cross-compiles the package for 64-bit Windows without needing a Windows machine", "Runs the Windows test suite", "Installs the Windows SDK"], "answer": 1, "explain": "GOOS/GOARCH retarget the compiler — one codebase builds for any supported platform from anywhere."},
    {"q": "Why does go vet ./... belong in CI?", "choices": ["It formats code", "It runs static analysis catching bugs like Printf verb mismatches", "It downloads dependencies", "It publishes the module"], "answer": 1, "explain": "go vet is the built-in analyzer that flags suspicious constructs before they ship."},
    {"q": "In flag.Duration(\"timeout\", 5*time.Second, ...), what does the user pass and get?", "choices": ["-timeout 3s gives a 3-second time.Duration", "-timeout must be an integer of nanoseconds", "Durations are not supported by flag", "-timeout 3s gives the string \"3s\""], "answer": 0, "explain": "flag.Duration parses Go duration strings like 3s or 500ms into a time.Duration value."},
    {"q": "Your CLI fails to connect. Which exit behavior keeps the automation contract?", "choices": ["Exit 0 with an error message", "Print to stderr and os.Exit(1) so callers detect failure", "Panic with a stack trace always", "Retry forever"], "answer": 1, "explain": "Nonzero exit codes are how CI/cron detect tool failure — same contract as the M19 Python CLI."},
    {"q": "Should you commit go.sum? Why?", "choices": ["No — it is machine-local", "Yes — it holds integrity hashes proving dependencies are untampered", "Only for libraries, not tools", "It is generated at release time only"], "answer": 1, "explain": "go.sum verifies dependency bytes; committing it makes every build verify integrity."}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL28-M38"],
  "drills": [
    {
      "id": "il28-m21-go-basics",
      "title": "Go syntax drill",
      "items": [
        {"prompt": "Predict the output: fmt.Printf(\"%s listening on %d\\n\", \"api\", 8080)", "answer": "api listening on 8080", "explain": "%s formats the string, %d the integer, \\n ends the line."},
        {"prompt": "Predict the output: hosts := []string{\"a\",\"b\"}; fmt.Println(len(hosts), hosts[1])", "answer": "2 b", "explain": "Slice of two strings; len is 2; index 1 is the second element."},
        {"prompt": "m := map[string]int{}; v, ok := m[\"x\"]; what are v and ok?", "answer": "v is 0, ok is false.", "explain": "Missing key: zero value plus ok=false from the two-value form."},
        {"prompt": "Write the idiom for handling err returned from parsePort(\"abc\").", "answer": "port, err := parsePort(\"abc\"); if err != nil { fmt.Println(\"bad port:\", err); return }", "explain": "Bind both values, branch on err != nil before using port."},
        {"prompt": "What is wrong with: var x int; fmt.Println(y)?", "answer": "y is undeclared (compile error); also x is declared but unused is allowed for package-level... actually unused local x would also error.", "explain": "Go rejects undeclared names and unused local variables at compile time."},
        {"prompt": "Rewrite using range: for i := 0; i < len(hosts); i++ { fmt.Println(hosts[i]) }", "answer": "for _, h := range hosts { fmt.Println(h) }", "explain": "range yields index and value; _ discards the index."},
        {"prompt": "When would you choose Go over Python for an ops tool?", "answer": "When distributing to many machines (single binary), running in tight loops (fast startup), or maintaining long-term (static types, vet).", "explain": "Distribution, startup, and maintainability are Go's ops advantages."}
      ]
    },
    {
      "id": "il28-m21-build-ship",
      "title": "Build and ship drill",
      "items": [
        {"prompt": "Initialize a module, run it, and build a binary. Give the three commands.", "answer": "go mod init example.com/tool; go run .; go build -o tool .", "explain": "init creates go.mod; run is the edit loop; build produces the artifact."},
        {"prompt": "Cross-compile the current package for Linux amd64 and macOS arm64.", "answer": "GOOS=linux GOARCH=amd64 go build -o tool-linux . && GOOS=darwin GOARCH=arm64 go build -o tool-mac .", "explain": "GOOS/GOARCH retarget the build; no extra toolchain needed."},
        {"prompt": "How do you verify the Linux binary is really a Linux binary on your Mac?", "answer": "file tool-linux — reports ELF 64-bit LSB executable, x86-64, statically linked.", "explain": "The file command identifies the binary format."},
        {"prompt": "Define a -port flag defaulting to 80 and parse flags. Write the snippet.", "answer": "port := flag.Int(\"port\", 80, \"port to check\"); flag.Parse(); fmt.Println(*port)", "explain": "flag.Int returns *int; Parse processes os.Args; dereference to use."},
        {"prompt": "Why net.DialTimeout(\"tcp\", addr, 3*time.Second) instead of net.Dial?", "answer": "Bounds the dial — a dead host fails in 3 seconds instead of hanging for minutes.", "explain": "Timeouts everywhere, applied to dials too."},
        {"prompt": "A teammate's Go repo has no go.sum committed. What do you tell them?", "answer": "Commit it — go.sum holds the hashes that prove dependencies are untampered on every build.", "explain": "Integrity verification only works if the hashes are in the repo."},
        {"prompt": "Name two CI checks for a Go repo and what each catches.", "answer": "gofmt -l . (unformatted files) and go vet ./... (static analysis: Printf mismatches, suspicious code).", "explain": "Formatting plus analysis on every change."}
      ]
    }
  ],
  "handsOnLab": {
    "id": "il28-m21-lab",
    "title": "Build and ship a port-checker CLI",
    "brief": "You will write a Go CLI that checks TCP connectivity with a dial timeout, build it, cross-compile it for three platforms, and verify each binary — the full 'write once, ship everywhere' ops workflow.",
    "steps": [
      "Check the toolchain: run go version (install Go from your OS package manager or go.dev if missing).",
      "Scaffold: mkdir portcheck && cd portcheck && go mod init example.com/portcheck.",
      "Write main.go with the flag-based port checker from the notes (-host, -port, -timeout), DialTimeout, OPEN/CLOSED output, and os.Exit(1) on failure.",
      "Format and vet: run gofmt -l . (expect no output) and go vet ./... (expect no findings); fix anything reported.",
      "Fast loop: run go run . -host localhost -port 22 -timeout 2s and confirm OPEN or CLOSED with the right exit code (echo $?).",
      "Build native: go build -o portcheck . then ./portcheck -host example.com -port 443.",
      "Cross-compile: GOOS=linux GOARCH=amd64 go build -o portcheck-linux . ; GOOS=windows GOARCH=amd64 go build -o portcheck.exe . ; GOOS=darwin GOARCH=arm64 go build -o portcheck-mac .",
      "Verify formats: run file portcheck-linux portcheck.exe portcheck-mac and confirm ELF, PE32+, and Mach-O respectively.",
      "Negative test: ./portcheck -host 127.0.0.1 -port 9 -timeout 1s (discard port, almost certainly closed) — confirm CLOSED output and exit code 1.",
      "Write SHIP.md: the three build commands, the file(1) output, and one paragraph on when you would choose Go over Python for an ops tool."
    ],
    "deliverable": "main.go, go.mod, four binaries (native + linux/windows/mac), and SHIP.md with build commands, file output, and the Go-vs-Python judgment.",
    "checkpoint": "gofmt and go vet clean; native binary exits 0 on open port and 1 on closed; file(1) identifies three correct foreign formats; SHIP.md present."
  },
  "mockTask": {
    "id": "il28-m21-mock",
    "type": "choice",
    "q": "Panel: 'We need a small network diagnostic tool deployed to 500 mixed Linux/Windows servers with no Python guaranteed. Python or Go — and how do you ship it?'",
    "choices": ["Python — ship the script and install Python everywhere first", "Go — cross-compile with GOOS/GOARCH into static binaries per platform; one file per OS, no runtime to install", "Python — bundle the interpreter in a zip manually", "Go — but run it through a container on each server"],
    "answer": 1,
    "explain": "Go's single static binaries and one-command cross-compilation directly solve heterogeneous-fleet distribution with no runtime prerequisite; installing Python on 500 servers (or containers everywhere) adds operational burden the Go binary avoids."
  },
  "crossLinks": [],
  "videos": [
    {"title": "Learn Go Programming – Golang Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=YS4e4q9oBaU", "source": "freeCodeCamp.org (YouTube)", "durationMin": 419, "order": 1, "watchBefore": "notes", "blurb": "Full Go course from syntax to concurrency — follow the early sections for this module's fundamentals, then revisit for deeper topics."}
  ],
  "estimatedMinutes": 0
}
