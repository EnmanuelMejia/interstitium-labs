# Content retrofit: IL-13 Frontend track (modules 15-21 of 56)

M = {
"frontend-interview-prep--js-ts-depth": {
"summary": ("Welcome to JavaScript and TypeScript Depth — the opening module of the Frontend Engineering Interview Prep path. I'm your instructor, and this is the "
"language half of every frontend loop: closures, the event loop, and async — plus the TypeScript depth that signals seniority. We cover closures, scope, and the "
"module pattern; prototypes, classes, and this; microtasks versus macrotasks; promises, async/await, and their error paths; and TypeScript narrowing, generics, and "
"utility types. By the end, the ten interview questions that never die will be guaranteed points."),
"concepts": [
("Closure", "A function capturing its enclosing scope's variables — the variables live as long as the closure does; the module pattern, private state, and the classic captured-loop-variable bug."),
("Scope", "Where bindings are visible: function, block (let/const), and module scope — the map you read before reasoning about any variable."),
("this", "Set by the call site — method call, plain call, new, or arrow functions inheriting lexically; prototypes are the delegation chain classes sit on top of."),
("Event loop", "The runtime's scheduling loop: run a macrotask, drain the microtask queue fully, render — the model behind every async interview question."),
("Microtasks vs macrotasks", "Microtasks (promises, queueMicrotask) drain completely after each macrotask (setTimeout, I/O, rendering) — so promise callbacks run before setTimeout(0), and a microtask loop can starve rendering."),
("Promise error paths", "Unhandled rejections, try/catch around await, Promise.all failing fast versus allSettled for independent work — the senior signal is 'here's how this fails and how the caller learns about it.'"),
("Narrowing", "typeof/instanceof checks and discriminated unions that shrink a type — with exhaustiveness checking via never proving every variant is handled."),
("Generics with constraints", "Type parameters bounded by constraints — reusable functions and components that stay type-safe across shapes."),
("Utility types", "Partial, Pick, Omit, Record — the standard transformations for deriving types instead of rewriting them."),
("Module pattern", "Closures used to expose a public API over private state — the pre-class encapsulation idiom that still explains how privacy works."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write the closure bug and its fix from memory: the loop-variable capture, then the let-scoped version — explain both aloud in under a minute.",
"Trace an event-loop ordering exercise by hand: interleaved promises, setTimeout(0), and queueMicrotask — predict the order, then run it to verify.",
"Convert a callback-based function to async/await with proper error paths: try/catch, an allSettled for independent calls, and no unhandled rejections.",
"Write a discriminated union with exhaustive narrowing: switch on the discriminant, put never in the default, and let the compiler prove completeness.",
"Drill the ten perennial questions aloud — two minutes each, layered: the 30-second answer, the mechanism, the classic bug — until none of them cost you composure.",
],
"project": ("Language-depth portfolio. Write a ten-question self-interview: for each perennial question (closures, this, event loop, promises, narrowing, generics, "
"and four more from the module), record a two-minute spoken answer following the layered shape — answer, mechanism, classic bug. Transcribe the two weakest and "
"rewrite them until they're clean. Deliverable: ten recordings plus two rewritten transcripts — guaranteed points, banked."),
"honesty": ("Honest scope: language trivia is the floor of frontend interviews, not the ceiling — fluency here buys composure for the novel problems, and this course "
"confers no certificate. Interviewers use these questions to calibrate; the offer comes from what you build with the language."),
},
"frontend-interview-prep--react-model": {
"summary": ("Welcome to Component Models and React Internals — module 2 of the Frontend path. I'm your instructor, and we study React as a runtime, not an API list: "
"reconciliation, hook closures, and render discipline — the internals senior loops actually probe. We cover components as functions of state, hooks (rules, closures, "
"stale state), reconciliation and keys, memoization (memo, useMemo, useCallback), state management tradeoffs, and the server-components mental model. By the end, you "
"will answer 'why did this re-render?' with a mechanism, not a guess."),
"concepts": [
("UI = f(state)", "Components as pure rendering functions of state: same state, same output — why unidirectional data flow works and why components are easy to test."),
("Hook closures", "Effects and callbacks capture the render's values — stale state is a closure problem; the fix is reading the capture, not fighting the linter."),
("Reconciliation", "React's diff of old and new trees, matched by key — stable keys let it move and reuse DOM nodes; index keys on reorderable lists cause wrong state reuse."),
("Keys as identity", "Keys are identity, not decoration: identity must follow the item, not its position."),
("memo", "Skips re-rendering a component when props are shallow-equal — for expensive subtrees, measured first, not everywhere."),
("useMemo / useCallback", "useMemo caches an expensive computation; useCallback stabilizes a function identity so memoized children don't re-render — memoize by measurement."),
("State management ladder", "Lift state to the lowest common parent → context for truly global low-churn data → external stores for complex shared state with selective subscriptions."),
("Context's re-render cost", "No selectors: one context value change re-renders all consumers — why context is a poor state manager for high-churn state."),
("Server components", "Components that render on the server and never hydrate — non-interactive UI ships less client JavaScript."),
("Render discipline", "The habit of asking 'what re-rendered and why' before optimizing — profile, then memoize the measured hotspot."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Build a tiny app with a stale-closure bug in an effect; diagnose it by naming the captured render's values, then fix it — explain the mechanism aloud.",
"Render a reorderable list with index keys, observe the wrong-state-reuse bug, switch to stable keys, and state the reconciliation rule that changed the behavior.",
"Profile a slow subtree, add memo/useMemo/useCallback at the measured hotspot only, and re-profile — write the before/after numbers.",
"Move shared state through the ladder for one feature: lifted state, then context, then an external store — state at each step what broke or got awkward.",
"Answer 'why did this re-render?' for three scenarios (parent re-render, context change, new function identity) — mechanism first, fix second.",
],
"project": ("Internals deep-dive write-up. Pick one real performance bug (or plant one): a list that re-renders wrongly, a context that re-renders everything, a stale "
"effect. Document the symptom, the mechanism (reconciliation, keys, closures), the fix, and the measured before/after. Write it as the answer you'd give a senior "
"interviewer probing internals. Deliverable: the write-up — proof you reason about the runtime, not the API list."),
"honesty": ("Honest scope: React internals change across versions — the mental models here are durable, but API details drift, and this course confers no certificate. "
"Verify against the current docs before an interview; interviewers reward current knowledge over memorized snapshots."),
},
"frontend-interview-prep--browser-render": {
"summary": ("Welcome to Browser Rendering and Performance — module 3 of the Frontend path. I'm your instructor, and here performance is interview currency: the "
"rendering pipeline, the vitals that measure it, and the optimizations that move them — all demonstrable in DevTools. We cover the critical rendering path, reflow "
"versus repaint versus compositing, Core Web Vitals (LCP, INP, CLS), profiling with the DevTools Performance panel, code splitting, and caching/CDN/resource hints. "
"By the end, your first move in any perf question will be 'profile first' — and you'll mean it."),
"concepts": [
("Critical rendering path", "Parse HTML → DOM, parse CSS → CSSOM, render tree, layout, paint, composite — sync scripts and render-blocking CSS delay first paint."),
("Reflow", "Layout: geometry changes — expensive, cascades to descendants; the cost to avoid in animations."),
("Repaint", "Visual changes without geometry — cheaper than reflow, still per-frame budget to watch."),
("Compositing", "GPU layer moves (transform/opacity) — the cheapest visual change; the animation discipline is 'transform and opacity only.'"),
("LCP", "Largest Contentful Paint: loading — when the main content appears; lower is better."),
("INP", "Interaction to Next Paint: responsiveness — worst-case input latency; lower is better."),
("CLS", "Cumulative Layout Shift: visual stability — unexpected movement; lower is better."),
("Flame-chart reading", "Record an interaction, read the long tasks, layout/paint blocks, and JS stacks — the bottleneck decides the fix, not intuition."),
("Code splitting", "Ship only what the route needs: route-level splits plus lazy loading cut initial JS — and parse/compile time is the real mobile bottleneck."),
("Resource hints", "preload (high-priority, current page) vs prefetch (low-priority, likely next navigation) — intent and priority, declared up front."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Open DevTools Performance on a slow page you know: record an interaction, identify the longest task, and name the category (scripting, rendering, network) before proposing any fix.",
"Fix one layout-thrash pattern: batch DOM reads and writes, or move an animation to transform/opacity — re-measure and write the before/after.",
"Audit a page's vitals: find LCP, INP, CLS, name the likely cause of the worst one, and propose the single highest-leverage fix.",
"Add route-level code splitting to a toy app: measure initial JS before and after with the coverage panel — state the parse/compile saving.",
"Write the perf-investigation script you'd narrate in an interview: profile → bottleneck → fix → re-measure — and rehearse it on one real page.",
],
"project": ("Performance case study. Take a slow page (a demo app or a public page you can analyze): profile it, identify the bottleneck with flame-chart evidence, apply "
"one fix (code split, animation discipline, resource hints, or caching), and re-measure. Write it as a case study: baseline vitals, diagnosis, fix, after-numbers. "
"Deliverable: the case study — the artifact that turns 'I know performance' into 'here's the proof.'"),
"honesty": ("Honest scope: performance numbers are device- and network-specific — a fix that wins on a flagship phone may not move a budget device, and this course "
"confers no certificate. Interviewers score the method (profile, fix, re-measure); absolute numbers are context, not truth."),
},
"frontend-interview-prep--css-systems": {
"summary": ("Welcome to CSS Layout Systems — module 4 of the Frontend path. I'm your instructor, and this is CSS as engineering: layout systems, architecture at "
"scale, and accessibility — the craft half that separates frontend engineers from JS generalists. We cover the box model, specificity, and the cascade; flexbox and "
"grid; responsive design and container queries; CSS architecture (BEM, modules, utilities); animation discipline; and accessibility. By the end, you will choose "
"layout systems with reasons and keep specificity flat by process."),
"concepts": [
("Box model", "Content + padding + border + margin — with box-sizing: border-box making widths sane; the first thing to verify when layout looks wrong."),
("Specificity", "Inline > ID > class > element, ties broken by source order — kept flat (BEM/utilities) so overrides stay predictable."),
("Flexbox", "One-dimensional layout: a row or column of items with content-driven sizing — the tool for components."),
("Grid", "Two-dimensional layout: rows AND columns with explicit placement — the tool for page-level structure; most real UIs compose both."),
("Container queries", "Components responding to their container's size — reusable in any layout; viewport queries adapt pages, container queries adapt components."),
("BEM", "block__element--modifier: one class of specificity per selector — specificity wars prevented by naming discipline."),
("Transform/opacity discipline", "Animate only transform and opacity (GPU-composited); animating width/left/top triggers reflow — jank."),
("Semantic HTML", "Buttons as <button>, real inputs with labels — keyboard support, focus, and screen-reader semantics for free; divs need all of it rebuilt."),
("Focus and contrast", "Visible focus states and sufficient color contrast — the accessibility checks interviewers actually run."),
("Architecture at scale", "One system (BEM, modules, or utilities), enforced — 'specificity wars are a process failure, not a CSS failure.'"),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Build the same card layout three ways (flexbox, grid, floats-free) and state the choosing rule for each — then pick the right one and justify it aloud.",
"Convert a media-query page section to container queries: place the same card in a sidebar and a full-width region and verify it adapts to its container.",
"Refactor a specificity-war stylesheet to flat BEM: cap every selector at one class, remove the !important overrides, and verify the visuals are unchanged.",
"Fix one janky animation by moving it to transform/opacity; record the frame rate before and after — state the reflow you eliminated.",
"Audit a form for accessibility: keyboard-only completion, visible focus, labels on every input, contrast check — fix what fails and log the checklist.",
],
"project": ("Layout-system showcase. Build a small responsive page (a dashboard or gallery) demonstrating: grid for page structure, flexbox for components, container "
"queries for a reusable card, flat-specificity architecture throughout, transform/opacity animations, and a passing accessibility self-audit. Document the choosing "
"rule at each decision. Deliverable: the page plus the decision log — craft you can point at."),
"honesty": ("Honest scope: CSS 'best practices' are team- and codebase-shaped — BEM versus modules versus utilities is a process decision, and this course confers no "
"certificate. The interview tests reasoning about systems; production tests whether the team actually enforces the one it picked."),
},
"frontend-interview-prep--frontend-systems": {
"summary": ("Welcome to Frontend System Design — module 5 of the Frontend path. I'm your instructor, and this is system design through the browser's lens: the "
"classic frontend design questions, practiced with component trees, data flow, and tradeoff narration. We cover designing a news feed, typeahead/autocomplete, and "
"a photo gallery at scale; client-side caching and state sync; real-time options (polling, SSE, WebSockets); and the frontend design-round walkthrough. By the end, "
"you will design the client as a system, not a page."),
"concepts": [
("News-feed fan-out", "Push for normal users, pull for celebrities — the famous hybrid; ranking separated from delivery, hot feeds cached, paginated."),
("Typeahead design", "Debounced input (~200–300ms), prefix index (trie or indexed prefix column), popularity/recency ranking, aggressive caching of hot prefixes — plus canceling stale in-flight requests client-side."),
("Photo pipeline", "Upload → object storage → async thumbnails (multiple sizes) → CDN → lazy loading + responsive images (srcset): 'bytes are the budget.'"),
("Client cache (SWR-style)", "Normalized server data with stale-while-revalidate: instant render from cache, fresh data moments later — invalidation tied to mutations."),
("Optimistic updates", "Apply the mutation to UI immediately, roll back on server rejection — the UX bet with the hedge built in."),
("Polling vs SSE vs WebSockets", "Polling: simple, wasteful. SSE: server→client stream with auto-reconnect — feeds and notifications. WebSockets: full duplex — chat, games, collaboration. Weakest tool that satisfies direction and frequency."),
("State sync", "Server as truth, client cache as a performance layer allowed to be briefly wrong, never permanently wrong."),
("Frontend walkthrough", "Requirements → component tree and data flow → API → caching/sync → rendering perf → real-time — the client-side shape of the standard walkthrough."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Whiteboard the news feed in 45 minutes: requirements, API, data model, fan-out decision with the celebrity math, caching, pagination — narrate tradeoffs throughout.",
"Design typeahead end to end: debounce timing, prefix index choice, ranking inputs, cache layers, and the stale-request cancellation on the client.",
"Design the photo gallery: upload flow, thumbnail sizes, CDN placement, lazy loading and srcset strategy — with the byte budget stated.",
"Choose the real-time mechanism for three features (notifications, chat, live dashboard): name direction and frequency, pick the weakest sufficient tool, state the rejected options.",
"Draw one client architecture (state, cache/sync, rendering, real-time) and present it in 10 minutes — the frontend design-round compressed rep.",
],
"project": ("Frontend design portfolio. Write two one-page design docs — the news feed and one more (typeahead or photo gallery) — each with requirements, component tree "
"and data flow, API, caching/sync strategy, rendering-perf plan, and real-time choice. Record a 20-minute walkthrough of one. Deliverable: two docs plus the recording — "
"the client-side design evidence."),
"honesty": ("Honest scope: frontend design rounds are the least standardized interviews in the loop — expectations swing widely by company, and this course confers no "
"certificate. The walkthrough is a communication skill; the 'right' architecture always depends on the product's actual constraints."),
},
"frontend-interview-prep--frontend-machine-coding": {
"summary": ("Welcome to the Machine Coding Build — module 6 of the Frontend path. I'm your instructor, and this is machine coding as a sport: three builds under a "
"timer with tests and accessible markup — the round that decides most frontend offers. We build a typeahead from scratch, a carousel with accessibility, and a Kanban "
"with drag and drop; we practice clean component APIs under time and testing the build with Testing Library. By the end, the 90-minute cadence will be muscle memory."),
"concepts": [
("90-minute cadence", "10 clarify + plan the component API, 60 build working-first, 20 edge cases + tests — clean props interfaces over pixel perfection."),
("Working-first", "Happy path functional before polish and edge cases — a demoable build beats a perfect fragment; interviewers score working builds with clean APIs."),
("Component API design", "Props as the contract: minimal, typed, intention-revealing — the design judgment interviewers read in your code."),
("Typeahead build", "Debounced input, cancellable requests, keyboard navigation, ranked suggestions — the canonical machine-coding problem."),
("Accessible carousel", "Semantic structure, keyboard controls, visible focus, announced slide changes — accessibility as a correctness requirement."),
("Kanban drag-and-drop", "Data model first (columns → cards, normalized), drag via HTML5 or pointer events, optimistic updates, keyboard-accessible fallback."),
("Testing Library philosophy", "Test user-visible behavior (roles, text), not implementation details — role-based queries align tests with the accessible experience."),
("Edge cases under time", "Empty states, errors, loading — the 20-minute block that separates a demo from a build."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Build the typeahead in 90 minutes on a timer: 10 plan the component API, 60 working-first, 20 edge cases + tests — then score yourself on API cleanliness.",
"Build the accessible carousel in 90 minutes: keyboard operable, focus visible, slide changes announced — test it keyboard-only at the end.",
"Build the Kanban in 90 minutes: normalized data model first, drag-and-drop second, keyboard fallback third — narrate the API choices as you go.",
"Write Testing Library tests for one build: happy path plus two edge cases, role-based queries only — verify the tests break when accessibility breaks.",
"Review all three builds against the rubric: working-first? clean APIs? tests? accessibility? — log the pattern in your misses.",
],
"project": ("Machine-coding portfolio. The three timed builds — typeahead, carousel, Kanban — each with tests and an accessibility self-check, plus a one-page build "
"narrative per build (decisions, rejected alternatives, what you'd do with more time). Deliverable: three builds, tests, and narratives — the round that decides offers, rehearsed."),
"honesty": ("Honest scope: machine-coding rounds vary wildly — some companies grade polish, others grade API design, and this course confers no certificate. Timed builds "
"train the cadence; the real round still depends on the prompt and the grader. What transfers is the working-first discipline."),
},
"frontend-interview-prep--frontend-mock": {
"summary": ("Welcome to the Frontend Mock Circuit — the final module of the Frontend path. I'm your instructor, and these are frontend-flavored mocks across all three "
"round types — timed JS deep-dives, machine coding on camera, frontend system-design rounds — plus the behavioral ledger, debriefed into a punch list. By the end, "
"the onsite will feel like repetition, not discovery."),
"concepts": [
("Layered deep-dive answers", "The 30-second correct answer, then the mechanism, then the edge case — 'the classic bug here is…' before they ask."),
("Machine-coding on camera", "The 90-minute cadence under observation: narrate the API plan, build working-first, test — composure as a scored skill."),
("Frontend design round", "Same walkthrough, client-side components: state architecture, caching/sync, rendering performance, real-time updates."),
("Behavioral ledger", "Story bank, stories-told-where, feedback, stumping questions — every behavioral touchpoint fresh and improving."),
("Debrief and triage", "Within the hour: what leaked, what held, biggest leak by frequency × weight, the 48-hour redrill — the mock is the test, the debrief is the studying."),
("Taper plan", "No new material, redrill from the debrief log, timed mocks, rest — the final two weeks."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Run a timed JS deep-dive mock (30 min): layered answers, 'the question behind the question' — log where you rambled versus where you landed.",
"Run a machine-coding mock on camera (90 min): narrate the component API plan, build working-first, test — review the recording for silent stretches.",
"Run a frontend system-design mock (45 min): client architecture with state, caching/sync, rendering, real-time — end with tradeoffs.",
"Run one behavioral round from your ledger: two-minute STAR answers, no repeated stories — log the follow-ups that stumped you.",
"Debrief all four within the hour: template, ranked leaks, 48-hour redrills, updated ledger — then write the taper plan.",
],
"project": ("Frontend mock portfolio. The four-mock circuit over two weeks — JS deep dive, machine coding on camera, frontend system design, behavioral — each debriefed "
"(leaks, holds, biggest leak, redrill plan) with the ledger updated. Close with the taper schedule for your real loop. Deliverable: four debriefs, the ledger, the taper — "
"the onsite as repetition."),
"honesty": ("Honest scope: mocks can't reproduce the real loop's stakes or its interviewers — and this course confers no certificate. What the circuit removes is surprise: "
"the format, the timing, and your own leak patterns, all discovered while fixes are still cheap."),
},
}
