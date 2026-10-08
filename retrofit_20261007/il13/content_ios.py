# Content retrofit: IL-13 iOS track (modules 29-35 of 56)

M = {
"ios-interview-prep--swift-core": {
"summary": ("Welcome to Swift Language Core — the opening module of the iOS Engineering Interview Prep path. I'm your instructor, and this is Swift at interview "
"depth: optionals without force-unwraps, value/reference discipline, and protocols — the language questions iOS loops open with. We cover optionals (binding, "
"chaining, coalescing), value versus reference semantics, protocols and protocol extensions, generics and associated types, and closures with capture lists. By the "
"end, you will write Swift that reads like you mean it."),
"concepts": [
("Optionals", "The type-level answer to null: binding (if let/guard let) over force-unwrapping, chaining for deep access, nil-coalescing for defaults — '!!' as a justified-only smell."),
("Optional map/flatMap", "Transforms over optionals without pyramid nesting — the functional spelling of 'if-let then transform.'"),
("Value semantics", "Structs/enums copied on assignment — no shared-state bugs; the Swift default, chosen deliberately."),
("Reference semantics", "Classes with shared identity — for view controllers, shared services, and anywhere identity or inheritance is required."),
("Protocols", "Capabilities as contracts — the unit of abstraction Swift leans on hardest."),
("Protocol extensions", "Default implementations shared across conforming types — mixins without a base class: 'composition of protocols over class inheritance.'"),
("Generics and associated types", "Constrained generic code over protocol requirements — the machinery behind Swift's standard library and your own reusable components."),
("Closures and capture lists", "Captured variables with explicit ownership: capture lists ([weak self]) breaking retain cycles — the memory-management interview core."),
("Error handling", "throws and Result: typed, explicit failure — try! justified only with a proof the call cannot fail, never with hope."),
("Retain cycles", "Strong reference loops (delegate patterns, closures capturing self) — broken with weak/unowned; the leak interviewers always probe."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Rewrite five force-unwraps from a sample file using binding, chaining, and coalescing — state aloud for each why the unwrap was unjustified.",
"Model one feature twice: as a struct and as a class — write the test that shows the value/reference difference, then state the choosing rule.",
"Design a small protocol hierarchy with protocol extensions for shared behavior: two conforming types, one extension, zero base classes.",
"Write a generic function with an associated-type constraint (a simple container or pipeline) — state the constraint's job in one sentence.",
"Fix a retain cycle in a closure-heavy sample: add the capture list, explain the cycle that existed, and verify the deinit fires.",
],
"project": ("Swift core portfolio. A playground or package demonstrating: optional-heavy API handling without force-unwraps, a struct-vs-class decision with the test proving "
"the semantics, a protocol-oriented mini-design, one generic abstraction, and a retain-cycle fix with the before/after. Each with a one-paragraph interview-style explanation. "
"Deliverable: the package plus explanations — language depth you can walk through."),
"honesty": ("Honest scope: language depth is the opening of the iOS loop, not the loop — frameworks, concurrency, and architecture decide the rest, and this course confers "
"no certificate. Swift also evolves yearly; verify details against the current language guide before interviewing."),
},
"ios-interview-prep--ui-frameworks": {
"summary": ("Welcome to UIKit and SwiftUI — module 2 of the iOS path. I'm your instructor, and we take both UI worlds honestly: UIKit's imperative lifecycle and "
"SwiftUI's declarative state — plus the judgment to discuss either in an interview. We cover view controllers and their lifecycle, Auto Layout, SwiftUI's state trio "
"and layout algorithm, UIKit–SwiftUI interop, and which framework fits which question. By the end, 'which framework?' will be a reasoned answer, not a religion."),
"concepts": [
("View controller lifecycle", "loadView → viewDidLoad (one-time setup) → viewWill/DidAppear (per-appearance work) → viewWill/DidDisappear → deinit — the traps: per-appearance work in viewDidLoad, leaked observers."),
("Auto Layout", "Constraints as linear equations the solver satisfies; intrinsic content size vs explicit constraints; ambiguity and conflicts read from the logs — 'I think in constraints, not frames.'"),
("@State", "View-local value state — owned by the view, the simplest state."),
("@Binding", "A two-way lens on someone else's state: the child reads and writes without owning — parent owns, child edits through the lens."),
("@ObservedObject / @StateObject", "External reference-type models — StateObject owns the lifetime, ObservedObject borrows it."),
("SwiftUI layout algorithm", "Three steps, parent-driven: the parent proposes a size, the child chooses, the parent places — one pass, no solver; GeometryReader for the rest."),
("UIViewRepresentable", "Wrapping a UIView to live inside SwiftUI — the bridge for the imperative world."),
("UIHostingController", "Embedding SwiftUI inside UIKit — interop as a migration strategy: wrap the legacy, write new code declaratively."),
("State flows down, events flow up", "The unidirectional rule of SwiftUI data flow — ownership explicit at every level."),
("Per-screen pragmatism", "Choosing per screen, not per religion — each framework has real gaps; interop exists so teams can mix."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Trace a view controller's lifecycle for a push/pop/push sequence on paper: name what runs when, and place one per-appearance task correctly (not in viewDidLoad).",
"Build one screen twice: UIKit with constraints and SwiftUI with state — then write the honest comparison (what was easier, what fought you) for each.",
"Diagnose an Auto Layout conflict from a console log: find the conflicting constraints, name the ambiguity, fix it — state the reading method aloud.",
"Explain the SwiftUI layout algorithm for one custom layout: who proposes, who chooses, who places — then implement it and verify against the prediction.",
"Bridge one UIKit component into SwiftUI (representable) and one SwiftUI view into UIKit (hosting controller) — state the ownership/lifecycle rule at each boundary.",
],
"project": ("Two-worlds showcase. One feature built twice — UIKit and SwiftUI — with a shared view model where sensible, plus one interop bridge in each direction. Document: "
"the lifecycle-correct UIKit version, the state-correct SwiftUI version, and the per-screen framework choice argued. Deliverable: the project plus the comparison write-up — "
"both worlds, honestly held."),
"honesty": ("Honest scope: the UIKit/SwiftUI balance shifts every year — teams are mid-migration everywhere, and this course confers no certificate. Interviewers want the "
"judgment to discuss both; claiming one world is 'done' reads as out of touch."),
},
"ios-interview-prep--ios-concurrency": {
"summary": ("Welcome to Concurrency on iOS — module 3 of the iOS path. I'm your instructor, and this is concurrency the iOS way: from GCD to Swift's structured "
"concurrency and actors — plus the main-thread rule interviewers always check. We cover GCD (queues, QoS, dispatch groups), OperationQueues, async/await and structured "
"concurrency, actors and data-race safety, and main-thread discipline for UI. By the end, the compiler will be your concurrency reviewer — and you'll be able to prove it."),
"concepts": [
("GCD queues", "Serial vs concurrent queues; async vs sync dispatch — the iron rule: UI on main, work off main; the deadlock demo: sync onto the current serial queue."),
("QoS classes", "User-interactive down to background — priority as a scheduling hint the system actually honors."),
("Dispatch groups", "Fan-in: enter/leave across parallel work, notify on completion — the pre-async/await coordination primitive."),
("OperationQueue", "Higher-level: dependencies between operations, cancellation, priorities, max concurrency — 'dependencies and cancellation buy the abstraction; otherwise GCD.'"),
("Structured concurrency", "async/await with task hierarchies where children can't outlive parents — lifetimes provable, no detached callbacks leaking."),
("@MainActor", "Compiler-enforced main-thread execution for UI-bound code — UI-touching code can't accidentally run elsewhere."),
("Actors", "Isolated mutable state with serialized, compiler-checked access — data races caught at build time: 'actors make the compiler my concurrency reviewer.'"),
("Main-thread discipline", "UIKit/SwiftUI are not thread-safe: compute off main, hop back for every UI touch — undefined behavior otherwise."),
("Cooperative cancellation", "Tasks check for cancellation at suspension points — structured concurrency makes the propagation automatic."),
("Data-race safety", "The compile-time guarantee: shared mutable state without synchronization can't compile under strict concurrency."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write the GCD deadlock demo (sync onto the current serial queue), run it, then fix it — explain the mechanism aloud in under a minute.",
"Convert a dispatch-group fan-in to structured concurrency: task group with the same coordination, then state what the structure guarantees that the group didn't.",
"Isolate shared mutable state in an actor: show the data race the compiler now rejects, and the serialized access it enforces.",
"Audit a sample for main-thread violations: mark every UI touch, route them through @MainActor, and state the rule each fix enforces.",
"Build one screen's data load with async/await end to end: fetch off main, hop to main for UI, cancellation on disappear — the disciplined shape, complete.",
],
"project": ("Concurrency portfolio. A small app feature demonstrating: GCD done right (queues, QoS, groups), the structured-concurrency rewrite, an actor guarding shared state, "
"and @MainActor-enforced UI updates — each with a before/after showing the hazard removed. Document the interview-style explanation per piece. Deliverable: the feature plus "
"explanations — concurrency you can prove."),
"honesty": ("Honest scope: Swift concurrency is still evolving — strict checking modes and best practices shift yearly, and this course confers no certificate. State which "
"language mode your answers assume; interviewers respect the precision."),
},
"ios-interview-prep--ios-persistence": {
"summary": ("Welcome to Persistence on iOS — module 4 of the iOS path. I'm your instructor, and this is the persistence ladder from UserDefaults to Core Data to "
"Keychain: what each is for, and the selection reasoning design rounds expect. We cover UserDefaults (and what doesn't belong there), Codable and file storage, the "
"Core Data stack, SwiftData at a glance, and the Keychain for secrets. By the end, you will choose the store from the access pattern — then justify the tradeoff."),
"concepts": [
("UserDefaults", "A preferences plist for small user settings — not secrets, not large data, not anything needing queries or migrations."),
("Codable", "Compiler-synthesized serialization for JSON/plist — custom keys and strategies for real-world APIs; the format layer."),
("App sandbox", "Documents vs caches vs tmp: the right directory per data lifetime, with the right file protection."),
("Core Data stack", "Persistent container → contexts (main for UI, background for work) → store coordinator → SQLite — faults as lazy loading; one context per queue."),
("Faults", "Lazily-loaded placeholders — data materializes on first access; memory-efficient by design."),
("Merge policies", "The conflict answer: what happens when background and main contexts disagree — named, not hoped."),
("SwiftData", "The modern API: @Model macro-driven, #Predicate queries, @Query in SwiftUI — backed by Core Data's storage; Core Data knowledge explains what's underneath."),
("@Query", "Live-updating fetch results bound to the view — declarative data that stays in sync automatically."),
("Keychain", "Encrypted, access-controlled secret storage (kSecAttrAccessible) surviving reinstall — 'if it's a secret, it's in the Keychain.'"),
("Access-pattern-first choice", "Queries, relationships, and size decide the store — not habit."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Audit a sample app's storage: move every misplaced item (a token in UserDefaults, a queryable list in a plist) to its correct store — state the rule each move enforces.",
"Build the Codable layer for one API: custom keys, one custom strategy, file persistence in the right sandbox directory with protection set.",
"Stand up the Core Data stack for one entity: background import, main-context UI, a merge policy — then trigger a conflict and watch the policy decide.",
"Rebuild the same feature in SwiftData (@Model, #Predicate, @Query) and write the honest comparison: what the modern API hides, what Core Data knowledge still explains.",
"Store one secret correctly: Keychain with an explicit accessibility attribute — then state what UserDefaults would have exposed.",
],
"project": ("Persistence-ladder showcase. One app using every rung correctly: UserDefaults for preferences, Codable files for documents, SwiftData/Core Data for queryable "
"data with a background import, Keychain for the token — each choice documented with the access-pattern argument. Deliverable: the app plus the choice log — the ladder, climbed deliberately."),
"honesty": ("Honest scope: persistence advice is Apple-ecosystem-shaped — the APIs and best practices move with the platform, and this course confers no certificate. "
"State the iOS version your answers assume; storage choices also answer to sync, backup, and privacy requirements interviews skip."),
},
"ios-interview-prep--ios-arch": {
"summary": ("Welcome to App Architecture Patterns — module 5 of the iOS path. I'm your instructor, and this is architecture as an interview topic: MVVM versus "
"coordinators versus unidirectional flows, dependency injection, and testability — argued with tradeoffs, not slogans. We cover MVC/MVVM and where they break, "
"coordinators and navigation, DI on iOS, unidirectional data flow, and testing layers. By the end, every architecture you name will be a bet with stated odds."),
"concepts": [
("Massive View Controller", "UIKit MVC's decay mode: the view controller absorbs networking, logic, and navigation — the problem MVVM and coordinators solve."),
("MVVM", "State and logic extracted into testable view models; the view as a binding layer — testability as the payoff."),
("Coordinators", "Navigation owned outside view controllers — screens stop knowing about each other; flows become testable objects."),
("Dependency injection", "Classes declare needs, something else supplies them — constructor injection, testable with fakes, no manual singletons."),
("Unidirectional data flow", "State down, events up: one source of truth, one traceable path — 'one direction, one truth, no mysteries.'"),
("Test pyramid (mobile)", "Unit: view models and logic with fakes — fast, many. UI (XCUITest): critical journeys — slow, few. Snapshot: visual regressions on components."),
("Seams", "The interfaces between layers — where testability and changeability live; 'I design the seams first — the code follows the seams.'"),
("Conditional choices", "'I chose X because [conditions]; I'd switch to Y if [change]' — the sentence that proves judgment over dogma."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Refactor one Massive View Controller into MVVM + coordinator: extract the view model, move navigation to the coordinator — state what each move bought.",
"Add DI to the refactored feature: constructor injection with fakes in tests — show the test that was impossible before.",
"Trace one user action through unidirectional flow: event up, state down — then break it deliberately (two-way binding) and observe the debugging cost.",
"Write the three test layers for one feature: unit tests on the view model, one UI test on the critical journey, one snapshot — state what each layer proves.",
"Argue one architecture choice aloud in two minutes: forces, options with costs, choice, and the condition that would change it — the bet with stated odds.",
],
"project": ("Architecture brief. For a two-screen feature: the pattern choice (MVVM + coordinators + repository, or your argued alternative) with the forces analysis, the DI "
"map, the unidirectional flow diagram, and the test plan across the three layers. Include the conditional: what would change your choice. Deliverable: the brief — "
"architecture argued, not asserted."),
"honesty": ("Honest scope: architecture taste is team- and app-shaped — the 'right' pattern depends on size, longevity, and who's maintaining it, and this course confers "
"no certificate. Interviewers reward the tradeoff argument; the codebase you inherit will have opinions of its own."),
},
"ios-interview-prep--ios-guided-build": {
"summary": ("Welcome to the Guided iOS App Build — module 6 of the iOS path. I'm your instructor, and this is a complete small app — networking, persistence, tests — "
"built to be walked through in an interview as proof of platform fluency. We build a list-detail app with cache: the spec, a networking layer with async/await, "
"SwiftUI views with view models, persistence with SwiftData, and unit tests for the view models. By the end, you will have the build narrative, not just the build."),
"concepts": [
("List-detail spec", "The canonical interview app: list, detail, cache — every layer exercised, nothing extraneous."),
("Networking layer", "Typed endpoints, async suspension, centralized error mapping, auth via interceptors, lifecycle-tied cancellation — 'the UI never sees HTTP.'"),
("Repository", "Network + local cache behind one data API — 'the only class that knows where data lives.'"),
("View models", "State holders the UI observes — testable without the UI; the seam the unit tests target."),
("SwiftData persistence", "@Model, #Predicate, @Query — the cache layer with live-updating UI binding."),
("Build narrative", "Problem → constraints → key decisions (with rejected alternatives) → result → 'what I'd do with more time' — the delivery vehicle for the proof."),
("Senior answer structure", "Definition, mechanism, fit-and-tradeoff — then stop and invite the follow-up; structure separating senior answers from recitation."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write the spec in one page: screens, data, cache policy, the explicit non-goals — sign it off before coding.",
"Build the networking layer first: typed endpoints, error mapping, cancellation — test it in isolation before any UI exists.",
"Add the repository: network + SwiftData cache, single source of truth — write the test proving the cache policy.",
"Build the SwiftUI views on view models: state down, events up — keep every decision in the view model, testable.",
"Write the unit tests for the view models, then rehearse the build narrative aloud: decisions first, the probe-fodder you chose to lead with.",
],
"project": ("The guided build, complete. The list-detail app with cache: networking layer, repository, SwiftUI + view models, SwiftData persistence, view-model unit tests — "
"plus the one-page spec and the build narrative (decisions, rejected alternatives, 'what I'd do with more time'). Deliverable: the app, the tests, the narrative — "
"platform fluency you can walk through."),
"honesty": ("Honest scope: a guided build proves you can execute a known shape well — real apps add product ambiguity, legacy, and scale this build doesn't simulate, "
"and this course confers no certificate. Present it as craft evidence, sized honestly."),
},
"ios-interview-prep--ios-mock": {
"summary": ("Welcome to the iOS Mock Circuit — the final module of the iOS path. I'm your instructor, and these are iOS-flavored mocks across language, UI, and "
"architecture rounds: timed Swift deep-dives, UIKit/SwiftUI whiteboard rounds, app-architecture design — plus the behavioral ledger — debriefed into targeted reps "
"before the real loop. By the end, your leaks will be found while fixes are cheap."),
"concepts": [
("Timed Swift deep-dives", "Layered answers: 30-second correct, mechanism, edge case — 'the classic bug here is…' before they ask."),
("Framework whiteboard rounds", "Narrate the architecture as you draw: components, lifecycles, data flow — then zoom into the probed area."),
("App-architecture design", "Requirements → layers → patterns → concurrency and persistence choices → testing story — 'I design the seams first.'"),
("Behavioral ledger", "Story bank, stories-told-where, feedback, stumping questions — every round fresh."),
("Debrief and triage", "Within the hour: leaks, holds, biggest leak by frequency × weight, 48-hour redrill."),
("Taper plan", "No new material, redrill from the log, timed mocks, rest."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Run a timed Swift deep-dive mock (30 min): layered answers on optionals, value/reference, concurrency — log the ramble points.",
"Run a UIKit/SwiftUI whiteboard mock: draw-then-zoom on lifecycles and state flow — review for silent stretches.",
"Run an app-architecture design mock (45 min): seams-first design with the testing story — end with tradeoffs.",
"Run one behavioral round from the ledger: two-minute STAR answers, no repeats.",
"Debrief all four within the hour: template, ranked leaks, 48-hour redrills, ledger update — then the taper.",
],
"project": ("iOS mock portfolio. The four-mock circuit over two weeks — Swift deep dive, framework whiteboard, app-architecture design, behavioral — each debriefed "
"with the template and the ledger updated. Close with the taper schedule. Deliverable: four debriefs, the ledger, the taper — the real loop as repetition."),
"honesty": ("Honest scope: mocks simulate format, not stakes — and this course confers no certificate. iOS loops also vary by team (UIKit-heavy vs SwiftUI-forward); "
"the circuit trains the format, and your research on the specific team covers the rest."),
},
}
