# Content retrofit: IL-13 Embedded + QA tracks (modules 43-56 of 56)

M = {
"embedded-swe-interview-prep--c-memory": {
"summary": ("Welcome to C and Memory Models — the opening module of the Embedded Software Engineering Interview Prep path. I'm your instructor, and this is C at "
"the metal: memory layout, volatile, and the undefined behaviors embedded interviews use as shibboleths. We cover pointers, arrays, and decay; stack vs heap vs "
"static; volatile and why it matters; alignment, padding, and packing; the undefined-behavior greatest hits; and reading C under time. By the end, you will be "
"able to state your worst-case RAM usage at compile time — and mean it."),
"concepts": [
("Array-pointer decay", "Arrays decay to pointers to their first element in most expressions — sizeof stops working across function boundaries; 'inside the function it's a pointer; always pass the length.'"),
("Stack", "Automatic, fast, tiny — overflow is the classic crash; the first suspect in a HardFault."),
("Heap (embedded)", "Often banned: fragmentation and nondeterminism have no place in RTOS firmware's hot path."),
("Static allocation", "Fixed at link time, deterministic — the embedded default; 'my RAM usage is a number in the map file, not a hope.'"),
("volatile", "The value can change outside program flow (hardware registers, ISR-shared flags): no register caching, no elided reads — required for MMIO and ISR flags, NOT a substitute for atomics or barriers."),
("Alignment and padding", "CPUs want multi-byte types at aligned addresses — the compiler inserts padding; structs have the size the alignment dictates, not the sum of members."),
("Packed structs", "__attribute__((packed)) removes padding for wire/disk formats — at the cost of slower or faulting unaligned access; 'I pack for the protocol, not by default.'"),
("Undefined behavior", "The compiler's license to assume: signed overflow, null dereference, use-after-free, data races — 'works in debug' proves nothing; sanitizers prove the negative."),
("Strict aliasing", "The optimizer's assumption about pointer types — violated casually, punished mysteriously; the UB interviewers probe when they're serious."),
("Reading C fast", "Datasheets, HALs, and legacy drivers are C — you'll read ten times more than you write; reading speed is the bottleneck."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Predict the sizeof and member offsets of three structs by hand (with padding), then verify with a program — state the alignment rule each time.",
"Write the decay demo: pass an array to a function, observe sizeof's answer inside, fix it by passing the length explicitly.",
"Write a polling loop over a fake status register with and without volatile: compile optimized, observe the elided reads — the volatile lesson, earned.",
"Pack a struct for a wire format, then measure the unaligned-access cost on your target (or read the architecture manual's warning) — state when packing is justified.",
"Compile a signed-overflow example at -O2 with and without -fwrapv: observe the optimizer's assumption — then write the UB-free version.",
],
"project": ("Memory-model portfolio. A single C file (host-compiled) demonstrating: the padding/offset predictions with verification, the decay fix, the volatile polling "
"loop, a packed wire-format struct with the justification comment, and one UB example with its safe rewrite — each with the interview-style explanation. Deliverable: "
"the file plus explanations — C at the metal, demonstrated."),
"honesty": ("Honest scope: host-compiled C exercises teach the language model, not the target — real MCUs add errata, toolchains, and debuggers, and this course confers no "
"certificate. State what's host-proven vs target-proven; interviewers respect the distinction."),
},
"embedded-swe-interview-prep--rtos-concepts": {
"summary": ("Welcome to RTOS Concepts — module 2 of the Embedded path. I'm your instructor, and this is real-time thinking: scheduling, determinism, and why there "
"is no malloc in the hot path — the conceptual core of embedded loops. We cover tasks, priorities, and scheduling; preemption and context switches; tickless idle "
"and power; static allocation; and a tour of FreeRTOS primitives with Zephyr at a glance. By the end, you will budget context switches like any other cost."),
"concepts": [
("Priority-based preemptive scheduling", "The highest-priority ready task runs; preemption on events/ticks; deterministic context switches — an RTOS optimizes for deadline guarantees, not throughput."),
("Preemption cost", "Register save/restore, stack switch, cache/TLB disturbance — microseconds that compound at high tick rates; 'context switches are the RTOS's tax.'"),
("Tickless idle", "Program the next wakeup (timer or interrupt) and sleep deeply until then — no periodic wakeups burning power; 'every avoided wakeup is battery life.'"),
("Static allocation", "Fixed-size pools and arrays sized at compile time; object pools for variable lifetimes — bounded worst-case behavior, fragmentation-free."),
("FreeRTOS primitives", "Tasks, queues, semaphores, mutexes — the vocabulary most embedded interviews assume; the small footprint with the huge ecosystem."),
("Zephyr", "The modern RTOS: device-tree-driven, broader protocol/security stack — 'FreeRTOS for the tiny MCU, Zephyr when the product needs the stack.'"),
("Device tree", "Hardware description as data files, not #ifdefs — the same firmware builds for many boards; board differences become data."),
("Determinism", "Bounded worst-case timing — the property that separates real-time from fast; measured in guarantees, not averages."),
("No malloc in the hot path", "Dynamic allocation's nondeterminism (fragmentation, unbounded time) disqualifies it where deadlines live."),
("GPOS vs RTOS", "Time-slicing fairness (throughput) vs priority preemption (deadlines) — the fundamental scheduling fork."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Design a three-task system on paper: priorities, periods, shared resources — then walk a preemption scenario and name the context-switch points.",
"Budget the tick: at 1 kHz with a 2 µs switch cost, compute the tax — then redesign tickless and state the power saving qualitatively.",
"Replace a malloc-based design with object pools: size the pools at compile time, show the worst-case RAM in the (hypothetical) map file.",
"Write the FreeRTOS-primitive choice for five IPC needs (signal, mutual exclusion, resource counting, data handoff, ISR-to-task): name the primitive and the rule per choice.",
"Compare FreeRTOS vs Zephyr for two products (a sensor node, a connected gateway): the footprint/stack tradeoff — verdict with the flip condition.",
],
"project": ("RTOS design brief. For a sensor node: task set with priorities and periods, the scheduling analysis (what preempts what, the switch budget), the IPC map "
"(primitive per need), the static-allocation plan with worst-case RAM, and the tickless-idle power story. Deliverable: the brief — real-time thinking, written down."),
"honesty": ("Honest scope: paper RTOS design is not firmware — real targets add interrupt latencies, errata, and measurement, and this course confers no certificate. "
"The interview tests the conceptual core; the lab proves the rest. State which is which."),
},
"embedded-swe-interview-prep--drivers-peripherals": {
"summary": ("Welcome to Drivers and Peripherals — module 3 of the Embedded path. I'm your instructor, and this is hardware literacy: the peripheral set every embedded "
"interview assumes, DMA, and the datasheet-reading skill that proves you can learn any chip. We cover GPIO, timers, and counters; UART, SPI, I2C (the big three buses); "
"DMA; interrupts versus polling; and clock trees with baud rates. By the end, you will verify clocks before blaming the peripheral."),
"concepts": [
("GPIO", "Digital in/out; modes (push-pull/open-drain); edge-triggered interrupts — the simplest peripheral and the bring-up starting point."),
("Timers", "Counters with prescalers: PWM output, input capture for measurement, periodic interrupts — 'the most underused peripheral.'"),
("UART", "Async point-to-point, no clock line (baud agreement) — simplest debug channel; the bring-up lifeline."),
("SPI", "Fast, full-duplex, 4 wires, one master — displays, flash; speed at the cost of pins."),
("I2C", "2-wire multi-drop with addressing — sensors, EEPROM; wire-count frugality at the cost of speed."),
("DMA", "Peripheral → memory transfers in hardware while the CPU sleeps or computes — configure source/dest/increment, handle transfer-complete, watch cache coherency."),
("Interrupts vs polling", "Interrupts: event-driven, power-efficient, concurrency complexity. Polling: simple, deterministic, wasteful — 'poll when timing is tight and simple; interrupt when events are sparse and power matters.'"),
("Clock trees", "Source (HSE/HSI/PLL) → dividers/multipliers → bus clocks → peripheral clocks — baud rates, timer periods, and power all derive from here."),
("Baud-rate math", "Divisors computed from the peripheral clock — wrong clock tree, wrong divisor, garbage on the UART."),
("Datasheet reading", "Register map and functional description first — registers define what's configurable; everything else is context."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"For one timer, compute the prescaler/period for a 1 kHz PWM from the bus clock: show the clock-tree path and the arithmetic — the baud-rate-math muscle, trained.",
"Choose the bus for three peripherals (a display, a temperature sensor, a debug console): UART/SPI/I2C with the speed/wires/device-count argument per choice.",
"Design a DMA transfer for sensor acquisition: source, destination, increment settings, the transfer-complete ISR, and the cache-coherency check — on paper, completely.",
"Decide interrupts vs polling for three events (a 10 kHz sample clock, a rare button press, a UART RX stream): the timing/power/simplicity argument per event.",
"Read one unfamiliar peripheral's datasheet section (register map + functional description) and write the five-line bring-up sequence — the learn-any-chip drill.",
],
"project": ("Peripheral bring-up portfolio. For one bus peripheral (your choice): the datasheet reading notes, the clock-tree derivation, the init sequence as commented "
"pseudocode or real code, the DMA or interrupt design, and the choosing-rule write-up (why this bus, why this trigger mode). Deliverable: the portfolio — hardware "
"literacy, demonstrated."),
"honesty": ("Honest scope: paper bring-up is not bring-up — real chips have errata, silicon bugs, and scope-measured reality, and this course confers no certificate. "
"The interview tests whether you can read the map; the bench tests whether you can walk the territory."),
},
"embedded-swe-interview-prep--embedded-concurrency": {
"summary": ("Welcome to Concurrency and Interrupts — module 4 of the Embedded path. I'm your instructor, and this is concurrency where the stakes are hardware: ISRs, "
"priority inversion, and the synchronization patterns that keep real-time systems correct. We cover ISR discipline, critical sections, mutexes versus semaphores in an "
"RTOS, priority inversion with inheritance, register-level races, and lock-free ring buffers. By the end, your critical sections will be measured in instructions."),
"concepts": [
("ISR discipline", "Short, no blocking, no heap, minimal work — set a flag or push to a queue; the task does the heavy lifting."),
("Critical sections", "Interrupt masking around shared access — 'measured in instructions, not functions'; the tool for ISR-task sharing."),
("Mutex (RTOS)", "Ownership + priority inheritance — for mutual exclusion; the RTOS knows who holds it."),
("Semaphore (RTOS)", "Counting, no ownership — for signaling and resource pools; 'never use a semaphore where I need ownership semantics.'"),
("Priority inversion", "Low-priority holder + medium-priority preempter = high-priority task waits unboundedly — the classic Mars Pathfinder story."),
("Priority inheritance", "Holder temporarily inherits the blocked high-priority task's level — the inversion fix, built into RTOS mutexes."),
("Register-level races", "Read-modify-write with an ISR between the read and the write — fixed by atomic set/clear registers, critical sections, or lock-free handoff."),
("Lock-free ring buffer", "Single-producer/single-consumer: head owned by consumer, tail by producer — disjoint writes need no mutual exclusion."),
("Interrupt priorities vs RTOS", "Know which priorities the kernel masks — the configuration interviewers probe when they're serious."),
("Deferred interrupt work", "The pattern: ISR signals, task processes — keeping ISRs short and the real work schedulable."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write the ISR rules as a checklist, then audit a sample ISR against it: find the blocking call, the heap use, the overlong work — fix all three.",
"Demonstrate priority inversion on paper: three tasks, one mutex, the unbounded wait — then apply priority inheritance and show the bound restored.",
"Design the sharing for one ISR-task handoff twice: critical-section version and ring-buffer version — state when each wins.",
"Choose mutex vs semaphore for five scenarios: defend each with the ownership rule — 'ownership semantics' as the deciding test.",
"Write the deferred-work pattern for one peripheral: ISR pushes to queue, task drains — with the queue-depth and overflow policy stated.",
],
"project": ("Concurrency-correctness brief. For one subsystem (e.g., sensor acquisition): the ISR design with the discipline checklist, the sharing map (what's shared, "
"the protection per item), the inversion analysis with the inheritance answer, and the deferred-work flow. Deliverable: the brief — real-time correctness, argued."),
"honesty": ("Honest scope: paper concurrency analysis is necessary but not sufficient — real systems need measurement (worst-case execution times, actual latencies), "
"and this course confers no certificate. The interview tests the patterns; the lab proves the bounds."),
},
"embedded-swe-interview-prep--embedded-debug": {
"summary": ("Welcome to Debugging Hardware and Software — module 5 of the Embedded path. I'm your instructor, and this is debugging as a demonstrable skill: from "
"HardFault registers to logic-analyzer traces — plus the war story every embedded behavioral round wants. We cover JTAG/SWD, logic analyzers versus oscilloscopes, "
"printf via semihosting and UART, HardFault diagnosis on Cortex-M, Valgrind for host-side code, and the debugging war story. By the end, you will read a fault like "
"a lab report."),
"concepts": [
("JTAG/SWD", "Halt, step, breakpoints, watchpoints, memory/register inspection — 'printf tells you what happened; the debugger shows you the state when it happened.' SWD is the 2-wire modern standard."),
("Logic analyzer", "Digital protocol decoding: UART/SPI/I2C transactions, timing across channels — 'decodes the conversation.'"),
("Oscilloscope", "Analog reality: signal integrity, noise, voltage levels — 'checks the physics.'"),
("Semihosting", "Debugger-shuttled I/O for early bring-up before UART works — halts the target per call; 'for bring-up, not for the field.'"),
("UART printf", "The field logging channel — cheap, always available, the production debug port."),
("HardFault diagnosis", "Stacked PC/LR plus CFSR/HFSR: the faulting location and cause class (bus fault, usage fault, precise vs imprecise) — diagnosis starts in registers, not guesswork."),
("Valgrind/memcheck", "Host-side memory debugging: leaks, invalid reads/writes, use-after-free — 'I prove memory correctness on the host where the tools are rich.'"),
("War story structure", "Stakes fast, hypotheses tested (not a heroic montage), wrong turns included, lesson + what changed — method and honesty score."),
("Watchpoints", "Break on data access, not just code location — the tool for 'who corrupted this variable.'"),
("Reproduce under the debugger", "The discipline: fault → reproduce → watchpoint → root cause — no guessing, no 'it works now.'"),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Walk a HardFault diagnosis on paper: given stacked registers and CFSR bits, identify the cause class and the faulting instruction — the lab-report reading drill.",
"Compare the debug channels for one bug: what JTAG shows that printf can't, what the analyzer decodes that the scope can't — pick the right tool per symptom.",
"Write the semihosting-vs-UART decision for two phases (bring-up, field): the cost that disqualifies semihosting at real-time rates.",
"Run Valgrind memcheck on a sample C program with a planted leak and overrun: read the report, fix both, re-run clean — the host-side proof habit.",
"Draft your war story: stakes, hypotheses tested, the wrong turns (included), the lesson, what changed afterward — two minutes spoken, honest throughout.",
],
"project": ("Debug portfolio. Three artifacts: a written HardFault diagnosis walkthrough (registers → cause → fix), a tool-choice matrix (symptom → tool → why) for the "
"debug channels, and your two-minute war story recorded — plus the Valgrind-clean report for a sample program. Deliverable: the portfolio — debugging as a demonstrable skill."),
"honesty": ("Honest scope: war stories are judged on honesty — embellishment is detectable and disqualifying, and this course confers no certificate. The wrong turns are "
"part of the story; a debugging history with no dead ends isn't credible."),
},
"embedded-swe-interview-prep--embedded-capstone": {
"summary": ("Welcome to the Embedded Capstone — module 6 of the Embedded path. I'm your instructor, and this is a real firmware build: RTOS tasks, a driver, a power "
"budget — documented and demoed; the artifact that ends 'do you do embedded?' debates. We spec a sensor node with an RTOS, write the driver layer for one bus peripheral, "
"design tasks and IPC, budget power with sleep modes, and build a host-side test harness. By the end, you will demo working hardware with honest numbers."),
"concepts": [
("Sensor-node spec", "Sampling rates and power budget first — the spec drives the architecture, not the reverse."),
("Driver layer", "One bus peripheral, properly abstracted: init, transfer, error handling — the hardware seam."),
("Task design and IPC", "Task per concern (sample, process, transmit) with queue handoff — decoupled timing domains, each meeting its deadline."),
("Power budget", "Milliamps × duty cycle: the math that makes 'low power' a claim with evidence — 'the power budget is the architecture.'"),
("Sleep modes", "Tickless idle and peripheral shutdown between work — every avoided wakeup as battery life."),
("Host-side test harness", "Logic compiled for the host behind hardware interfaces; unit-tested with Valgrind, sanitizers, coverage — 'prove logic on the host, integrate on the target.'"),
("Demo and writeup", "Working hardware plus honest numbers: spec, architecture, power math, test evidence, what you'd change."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write the sensor-node spec: sensors, sampling rates, latency needs, the power budget target — one page, signed off before code.",
"Build the driver layer for one bus peripheral: init, polled transfer, then interrupt/DMA — the hardware seam, tested on host where possible.",
"Design the tasks and IPC: sample/process/transmit with queue handoff, priorities assigned, the inversion check — on paper first.",
"Compute the power budget: active current × duty cycle + sleep current × sleep time — state the battery-life number and the assumption behind each term.",
"Build the host-side harness: hardware behind interfaces, logic unit-tested with sanitizers — then write the demo script and the honest-numbers writeup.",
],
"project": ("The embedded capstone. The sensor node: spec, driver layer, RTOS task design with IPC, power budget with sleep modes, host-side test harness — documented "
"and demoed (hardware or faithful simulation, stated honestly). Deliverable: the firmware, the writeup with power math and test evidence, and the demo — the artifact "
"that ends the debate."),
"honesty": ("Honest scope: a capstone is one system, honestly built — it doesn't prove breadth across targets or production hardening, and this course confers no "
"certificate. State what's simulated vs real hardware; honest numbers beat impressive claims."),
},
"embedded-swe-interview-prep--embedded-mock": {
"summary": ("Welcome to the Embedded Mock Circuit — the final module of the Embedded path. I'm your instructor, and these are embedded-flavored mocks: C under time, "
"RTOS design, live hardware-debugging scenarios — plus the war story — debriefed into the last reps. By the end, your leaks will be found while fixes are cheap."),
"concepts": [
("Timed C deep-dives", "Layered answers: 30-second correct, mechanism, edge case — 'the classic bug here is…' before they ask; UB questions answered with the optimizer's perspective."),
("RTOS whiteboard rounds", "Tasks, priorities, IPC, the inversion question — drawn and defended, not recited."),
("Hardware debugging scenarios", "'The sensor reads garbage' — the hypothesis-driven debug walkthrough, aloud, with the tool choice per step."),
("War story (behavioral)", "Stakes, hypotheses, wrong turns, lesson — method and honesty as the scoring rubric."),
("Debrief and triage", "Within the hour: leaks, holds, biggest leak by frequency × weight, 48-hour redrill."),
("Taper plan", "No new material, redrill from the log, timed mocks, rest."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Run a timed C deep-dive mock (30 min): pointers, volatile, UB — layered answers with the optimizer's perspective.",
"Run an RTOS whiteboard mock: design the task set live, defend the IPC choices, answer the inversion probe.",
"Run a hardware-debugging scenario mock: 'garbage on the UART' — hypothesize aloud (clocks first), pick tools per step, land the root cause.",
"Tell the war story once, recorded: two minutes, stakes-hypotheses-wrong turns-lesson — review for credibility gaps.",
"Debrief all four within the hour: template, ranked leaks, 48-hour redrills — then the taper.",
],
"project": ("Embedded mock portfolio. The four-mock circuit over two weeks — C deep dive, RTOS whiteboard, debugging scenario, war story — each debriefed with the "
"template. Close with the taper schedule. Deliverable: four debriefs and the taper — the last reps, converted."),
"honesty": ("Honest scope: mocks can't reproduce the bench — real debugging has smells, heat, and intermittent faults, and this course confers no certificate. What the "
"circuit trains is the hypothesis-driven narration; the lab provides the rest."),
},
"qa-test-interview-prep--test-strategy": {
"summary": ("Welcome to Test Strategy and the Pyramid — the opening module of the Software Testing & QA Interview Prep path. I'm your instructor, and this is strategy "
"before tools: the pyramid, risk-based planning, and the layering judgment QA interviews probe before any framework question. We cover the test pyramid, what belongs "
"at each layer, test doubles (mocks, stubs, fakes), risk-based planning, shift-left with CI gating, and arguing strategy aloud. By the end, you will allocate test "
"budget where failure hurts most — and say why."),
"concepts": [
("Test pyramid", "Many fast unit tests at the base, fewer integration tests, few e2e at the top — the economics: e2e is slow, flaky, expensive; push coverage down, justify every e2e."),
("Unit layer", "Pure logic and algorithms — provable in milliseconds; where validation logic belongs."),
("Integration layer", "Component interactions: DB, API contracts — what only the seams can prove."),
("E2E layer", "Critical user journeys only — the most expensive proof, spent sparingly."),
("Mocks vs stubs vs fakes", "Dummy: placeholder. Stub: canned responses. Fake: working simplified implementation. Mock: verifies interactions — fakes/stubs for state, mocks sparingly for contracts."),
("Risk-based planning", "Test effort follows failure probability × impact — not uniform coverage; 'strategy is resource allocation under uncertainty, argued out loud.'"),
("Shift-left", "Testing earlier: CI gates, pre-merge checks — defects found when they're cheapest; the cost-of-defect curve flattened."),
("CI gating", "Required checks as mechanical quality gates — no merge without green; enforced, not cultural."),
("Escape rate", "Bugs reaching production — the headline quality metric; 'I optimize for escaped defects, not test count.'"),
("Arguing strategy", "From risk: what breaks × what hurts — then the pyramid allocation with the economics stated."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Draw the pyramid for an app you know: place ten real test cases at their layers — then find the two e2e tests that should be units and move them.",
"Write the risk matrix for one feature: probability × impact per risk — allocate the pyramid from the matrix, not from habit.",
"Classify five test doubles in a sample suite (mock/stub/fake/dummy): find the over-mocked test and rewrite it with a fake — state what the rewrite bought.",
"Design the shift-left gates for one repo: pre-merge checks, required CI checks, the defect-cost argument for each gate.",
"Argue a strategy aloud in three minutes: risks first, pyramid allocation, the economics — the interview shape of this skill.",
],
"project": ("Strategy brief. For a product you choose: the risk matrix, the pyramid allocation with the per-layer test list, the test-double policy, and the shift-left gate "
"design — each argued from risk and economics. Deliverable: the brief — strategy before tools, written down."),
"honesty": ("Honest scope: strategy is argued from risk, and risk estimates are judgments — two good testers can disagree honestly, and this course confers no certificate. "
"The interview tests the reasoning; production tests the estimates. State your assumptions."),
},
"qa-test-interview-prep--automation-frameworks": {
"summary": ("Welcome to Automation Frameworks — module 2 of the QA path. I'm your instructor, and this is the framework landscape at selection depth: WebDriver versus "
"Playwright versus Cypress, POM discipline, and how to justify the choice. We cover Selenium WebDriver's architecture, Playwright's auto-waiting model, the Page Object "
"Model, Cypress's tradeoffs, and Appium basics for mobile. By the end, your framework answers will be criteria-first — engineering, not advocacy."),
"concepts": [
("WebDriver architecture", "Language bindings → WebDriver protocol (HTTP/JSON wire) → browser driver → real browser — cross-browser and cross-language, with explicit waits as the price."),
("Playwright's auto-waiting", "Actions wait for actionability — no sleep/flaky waits; multiple engines, network interception, parallelism built in."),
("Page Object Model", "One class per page encapsulating selectors and actions — 'selectors live in exactly one file per screen.'"),
("Cypress tradeoffs", "In-browser: superb debugging (time travel, real DOM) — but same-origin/tab limits; 'trades browser-architecture limits for the best debugging experience.'"),
("Appium", "WebDriver-protocol mobile automation: one API over iOS (XCUITest) and Android (UiAutomator2) — cross-platform coverage at the cost of speed."),
("Criteria-first selection", "Criteria before candidate tools — 'criteria-first prevents rationalizing a pre-chosen favorite.'"),
("Flakiness sources", "Timing, order-dependence, environment — classified before fixed; 'a flaky test is either fixed or quarantined, never tolerated.'"),
("Explicit vs auto waits", "The framework comparison that matters most in practice: who owns the waiting determines who owns the flakiness."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write the selection criteria for a hypothetical team (browsers, languages, CI, debugging needs) — then score WebDriver, Playwright, and Cypress against them; state the winner and the runner-up's case.",
"Build a three-page POM for a demo app: selectors encapsulated, tests reading as user intent — then change one selector and show the single-file fix.",
"Take one flaky test: classify the flakiness (timing/order/environment), apply the proper wait or isolation fix — state the classification before the fix.",
"Compare an explicit-wait script with an auto-waiting equivalent: run both under load, count the flakes — the empirical comparison.",
"Write the Appium-vs-native decision for one mobile feature: the coverage/speed tradeoff argued — verdict with the flip condition.",
],
"project": ("Framework selection brief. For a team you define: the criteria, the scored comparison (WebDriver/Playwright/Cypress + Appium for mobile), the POM structure sketch, "
"and the flakiness policy (classify → fix-or-quarantine). Deliverable: the brief — selection as engineering."),
"honesty": ("Honest scope: framework advice decays — the landscape moves yearly and team context dominates, and this course confers no certificate. Date your recommendation; "
"'as of 2026' is part of the answer."),
},
"qa-test-interview-prep--api-contract": {
"summary": ("Welcome to API and Contract Testing — module 3 of the QA path. I'm your instructor, and this is APIs as the test surface: contract thinking, schema "
"validation, and consumer-driven contracts — the backend-adjacent depth modern QA roles require. We cover HTTP semantics for testers, status codes and error contracts, "
"schema validation, consumer-driven contracts (Pact-style), and mocking dependencies. By the end, you will test the contract, not just the responses."),
"concepts": [
("HTTP safety/idempotency", "GET safe, PUT idempotent, POST neither — the semantics testers assert, not just the status codes."),
("Status-code classes", "2xx/3xx/4xx/5xx with exact meanings — 429 as the explicit throttle signal ('back off, respect Retry-After')."),
("Error contracts", "Can clients program against the errors? Stable codes, messages, request IDs — the contract's unhappy half."),
("Schema validation", "Shape, types, required fields — the response's promise, mechanically checked."),
("Consumer-driven contracts", "Each consumer's expectations as verifiable pacts — provider changes that break specific consumers, caught before deploy."),
("Mocking dependencies", "Isolating the system under test from unstable or unavailable collaborators — with the fidelity caveat stated."),
("Performance-adjacent API checks", "Response-time budgets per endpoint in CI, payload sizes, N+1 detection — the perf questions QA owns."),
("Reading a load-test report", "Percentiles not averages, error rate vs load steps, saturation signals, the bottleneck's location — 'I read the tail, then find what's saturated.'"),
("Senior answer structure", "Definition, mechanism, fit-and-tradeoff — then stop; structure separating senior answers from recitation."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write the HTTP-semantics checklist for one API: method safety/idempotency per endpoint, the exact status codes asserted, the headers checked — then run it against a real API.",
"Add schema validation to three API tests: shape, types, required fields — break the schema deliberately and watch the test catch it.",
"Write one consumer-driven contract (Pact-style): the consumer's expectations as a pact — then change the provider and watch the pact fail before deploy.",
"Set a response-time budget for two endpoints in CI: the threshold, the percentile measured, the gate that fails the build — the performance-adjacent check, live.",
"Read one load-test report (sample or generated): percentiles per step, error rates, the saturation signal — write the three-line verdict.",
],
"project": ("Contract-testing portfolio. For one API: the HTTP-semantics test suite, schema validation on key endpoints, one consumer-driven pact with the break-it demonstration, "
"and the CI response-time budgets — plus a load-test report reading with the verdict. Deliverable: the suite plus the report reading — the contract, tested."),
"honesty": ("Honest scope: contract tests verify the agreement, not the behavior behind it — a green pact with a broken provider is a false comfort, and this course confers "
"no certificate. State what each test layer proves; no layer proves everything."),
},
"qa-test-interview-prep--perf-testing": {
"summary": ("Welcome to Performance Testing — module 4 of the QA path. I'm your instructor, and this is performance testing literacy: the test types, the percentiles "
"that matter, and scripting a basic load test in k6 — enough to own the topic in QA loops. We cover load, stress, spike, and soak; throughput with p95/p99; k6 scripting "
"basics; JMeter thread groups; and reading a load-test report. By the end, 'performance claims without before/after numbers are stories' will be your line too."),
"concepts": [
("Load test", "Expected traffic: measure latency/throughput under the load you actually expect."),
("Stress test", "Beyond capacity: find the breaking point — where it breaks and how it breaks."),
("Spike test", "Sudden surges: test autoscaling and burst absorption — the thundering-herd rehearsal."),
("Soak test", "Sustained load over hours: find the leaks — memory, connections, the slow degradations."),
("p95/p99", "The tail: 'a 100ms average with a 5s p99 means 1% of users suffer' — SLOs are written on percentiles because experience lives in the tail."),
("Throughput", "Requests per second sustained — with the latency measured alongside; throughput without latency is half the story."),
("k6 scripting", "JS-scripted load tests with thresholds as gates: stages, VUs, assertions — code-reviewed load tests in the pipeline."),
("k6 thresholds", "Pass/fail assertions on metrics — 'the test proves the SLO or it fails.'"),
("JMeter thread groups", "The classic model: threads, ramp-up, loops — GUI-driven, mature, broad protocol support."),
("Report reading", "Percentiles per load step, error rates, saturation signals, bottleneck location — 'read the tail, find what's saturated.'"),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Script a k6 load test for a demo endpoint: stages (ramp, sustain), thresholds on p95 and error rate — run it and read the tail.",
"Run the same endpoint to stress: raise VUs past capacity, find the breaking point — write the 'where and how it breaks' note.",
"Spike it: 10× surge for 60 seconds — observe the autoscaling (or the queueing); write the absorption verdict.",
"Compare k6 vs JMeter for one team scenario: the scripted-vs-GUI tradeoff argued — verdict with the team-context reason.",
"Write the before/after for one optimization: baseline percentiles, the fix, re-measured percentiles — the numbers that prove it.",
],
"project": ("Load-test portfolio. For one endpoint: the k6 script with thresholds, the four test-type runs (load/stress/spike/soak) with reports, the report readings with "
"verdicts, and one before/after optimization with the numbers. Deliverable: the portfolio — performance testing literacy, evidenced."),
"honesty": ("Honest scope: load-test numbers are environment-shaped — test hardware, network, and data realism change everything, and this course confers no certificate. "
"State the environment with the numbers; a percentile without context is a story, not evidence."),
},
"qa-test-interview-prep--test-planning": {
"summary": ("Welcome to Test Planning and Reporting — module 5 of the QA path. I'm your instructor, and this is the craft QA interviews respect most: plans, "
"traceability, defect discipline, and metrics that measure quality — not just activity. We cover test plans that get read, traceability from requirements to cases, "
"defect lifecycle and severity, metrics (escape rate, flakiness), and exploratory testing charters. By the end, you will present conclusions, not queries."),
"concepts": [
("Test plan that gets read", "Scope and risk focus, traceability, entry/exit criteria, environment needs — 'a plan is argued choices, not a form.'"),
("Traceability", "Requirements → cases: every requirement tested, every test justified — the coverage argument that survives audit."),
("Defect lifecycle", "New → triaged → in progress → fixed → verified → closed (reopened on regression) — the discipline of the queue."),
("Severity vs priority", "Severity = impact on users; priority = fix order (business decision) — different axes, conflated at your peril."),
("Escape rate", "Bugs found in production that testing missed — the headline quality metric."),
("Flakiness rate", "Unreliable tests erode trust — measured, quarantined, fixed-or-deleted; never tolerated."),
("Exploratory charters", "Time-boxed missions with a goal, session notes, debriefs — skilled investigation, not random clicking; repeatable and reportable."),
("BLUF reporting", "Bottom line up front: recommendation first, the one chart that proves it, caveats briefly, the decision needed — 'executives decide.'"),
("Entry/exit criteria", "The gates: when testing starts, when it's done — decided in the plan, not in the moment."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write a one-page test plan for a feature you know: scope in/out with reasons, risk focus, entry/exit criteria — then cut every sentence that isn't a decision.",
"Build the traceability matrix for five requirements: requirement → cases → status — find the untested requirement and the unjustified test.",
"Run a defect triage on five sample bugs: assign severity AND priority separately — defend one case where they differ (severe but low priority, or trivial but urgent).",
"Compute escape rate and flakiness rate for a sample suite: write the two numbers, then the action each number demands.",
"Write one exploratory charter (45-minute mission), execute it on a demo app, debrief in writing — the charter → notes → debrief loop, complete.",
],
"project": ("QA craft portfolio. For one release: the one-page test plan, the traceability matrix, the triaged defect log with severity/priority separated, the quality "
"metrics (escape rate, flakiness) with the actions they demand, and one executed exploratory charter with debrief — plus the BLUF stakeholder summary. Deliverable: "
"the portfolio — the craft, evidenced."),
"honesty": ("Honest scope: metrics measure the past — escape rate tells you where quality was, not where it will be, and this course confers no certificate. Report "
"metrics with their limits stated; a metric without caveats is a vanity number."),
},
"qa-test-interview-prep--qa-automation-build": {
"summary": ("Welcome to the Guided Automation Build — module 6 of the QA path. I'm your instructor, and this is a real automation suite: UI, API, CI, reports — "
"built to be demoed; the artifact that converts QA interviews from Q&A into show-and-tell. We scaffold a framework with Playwright, write page objects for a demo "
"app, add API contract tests, wire a CI pipeline with reporting, and practice flaky-test triage. By the end, you will demo the suite, not describe it."),
"concepts": [
("Framework scaffold", "The runnable skeleton: config, fixtures, reporters — the foundation every later test inherits."),
("Page objects", "Selectors in exactly one file per screen; tests reading as user intent ('loginAs(user)') — the maintainability pattern."),
("API contract tests", "Status, schema, error contracts in the same suite — the backend-adjacent depth, automated."),
("CI pipeline", "Triggers, parallel jobs, artifacts, secrets via the platform (never in YAML), branch protection requiring the checks — 'the pipeline is the definition of done.'"),
("Reporting", "The suite's output as evidence: pass/fail, flakiness history, the report stakeholders actually open."),
("Flaky-test triage", "Quarantine first, then classify (timing/order/environment/real bug) — 'fixed or quarantined, never tolerated'; quarantine preserves signal with a dated fix-or-delete decision."),
("Branch protection", "Required checks as mechanical gates — quality enforced, not cultural."),
("Build narrative", "Problem → constraints → decisions → result → 'what I'd do with more time' — the delivery vehicle for the demo."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Scaffold the Playwright framework: config, one fixture, the reporter — run the empty suite green before writing any test.",
"Build page objects for three screens of a demo app: write one test per screen reading as user intent — then change a selector and show the single-file fix.",
"Add API contract tests for two endpoints: status, schema, error contract — the backend-adjacent layer, in the same run.",
"Wire the CI pipeline: push/PR triggers, parallel jobs, artifact upload, the required-check gate — break the build deliberately and watch the gate hold.",
"Plant one flaky test: quarantine it, classify it, fix it properly — document the triage as the interview answer.",
],
"project": ("The automation suite. The complete build: Playwright scaffold, page objects for a demo app, API contract tests, CI pipeline with reporting and branch "
"protection — plus the flaky-test triage log and the build narrative. Deliverable: the suite, the pipeline, the narrative — the demo that converts interviews."),
"honesty": ("Honest scope: a demo suite proves you can build the shape — production suites add the long tail (data, environments, maintenance burden), and this course "
"confers no certificate. Present the suite as what it is: the pattern, executed well, sized honestly."),
},
"qa-test-interview-prep--qa-mock": {
"summary": ("Welcome to the QA Mock Circuit — the final module of the QA path. I'm your instructor, and these are QA-flavored mocks: scenario design, framework "
"grilling, and plan whiteboards — debriefed into the final study plan. By the end, you will whiteboard the reasoning, not just the answer."),
"concepts": [
("Testing-scenario rounds", "Restate the goal, enumerate risks, allocate the pyramid, name tools per layer with reasons — 'I whiteboard the reasoning.'"),
("Framework deep-dives", "Criteria first, then the pick — selection as engineering under follow-up pressure."),
("Test-plan whiteboard", "Scope, risks, traceability, entry/exit — the plan as argued choices, drawn live."),
("Behavioral ledger", "Story bank, stories-told-where, feedback, stumping questions — every round fresh."),
("Debrief and triage", "Within the hour: leaks, holds, biggest leak by frequency × weight, 48-hour redrill."),
("Taper plan", "No new material, redrill from the log, timed mocks, rest."),
("Anchoring", "Restating the scenario's goal first — 'a brilliant plan for the wrong problem' is the classic whiteboard failure."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Run a timed scenario mock: 'test this feature' — goal restated, risks enumerated, pyramid allocated, tools named with reasons — 30 minutes.",
"Run a framework deep-dive mock: defend your framework pick against 'why not X?' — criteria first, every time.",
"Run a test-plan whiteboard mock: draw the plan live — scope, traceability, entry/exit — then defend the cuts.",
"Run one behavioral round from the ledger: two-minute STAR answers, no repeats.",
"Debrief all four within the hour: template, ranked leaks, 48-hour redrills, ledger update — then the taper.",
],
"project": ("QA mock portfolio. The four-mock circuit over two weeks — scenario design, framework deep dive, plan whiteboard, behavioral — each debriefed with the "
"template and the ledger updated. Close with the taper schedule. Deliverable: four debriefs, the ledger, the taper — reasoning, whiteboarded."),
"honesty": ("Honest scope: mocks simulate the format, not the stakes — and this course confers no certificate. QA loops vary by company (automation-heavy vs "
"strategy-heavy); the circuit trains the format, and company research covers the rest."),
},
}
