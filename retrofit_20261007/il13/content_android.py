# Content retrofit: IL-13 Android track (modules 36-42 of 56)

M = {
"android-interview-prep--kotlin-core": {
"summary": ("Welcome to Kotlin Language Core — the opening module of the Android Engineering Interview Prep path. I'm your instructor, and this is Kotlin at "
"interview depth: null safety without the double-bang, sealed hierarchies, and the coroutine mental model — the language half of every Android loop. We cover "
"null safety (?., ?:, and the justified-only !!), data/sealed classes and objects, the coroutines mental model, extension and scope functions, delegation (by lazy, "
"observable), and Java interop costs. By the end, you will write Kotlin that defends itself at the boundaries."),
"concepts": [
("Null safety", "Nullable types (?), safe calls (?.), Elvis (?:) for defaults — with !! as a justified-only escape hatch and platform types from Java interop still able to hand you null."),
("Data classes", "Value holders with generated equals/hashCode/copy — UI state, DTOs; the boring-correct choice for data."),
("Sealed classes/interfaces", "Closed hierarchies for states and results (Loading/Success/Error) with exhaustive when — UI state modeled safely."),
("Coroutines mental model", "'Sequential code, asynchronous execution': suspend functions pause without blocking threads; structured concurrency ties child lifetimes to scopes; dispatchers choose the pool (Main/IO/Default)."),
("Extension functions", "Behavior added without inheritance — nullable receivers included; the API-shaping tool."),
("Scope functions", "let (transform nullable), apply (configure), run/with (compute on receiver), also (side effects) — picked by what they return and what 'it' is."),
("by lazy", "Thread-safe lazy init — expensive immutable values created once on first access; preferred over lateinit var when the value is a val."),
("Delegation (by)", "Class delegation as composition without boilerplate — the ceremony remover for common patterns."),
("Platform types", "Java interop's nullability blind spot: annotate and defend at the boundaries — the compiler can't see what Java didn't declare."),
("Suspend vs blocking", "Suspension frees the thread for other coroutines; blocking pins it — the distinction the whole concurrency model rests on."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Rewrite five !! usages with safe calls, Elvis, and let-scoping — justify the one you keep (if any) with the proof it can't fail.",
"Model one screen's UI state as a sealed hierarchy (Loading/Success/Error): write the exhaustive when, then add a state and watch the compiler demand handling.",
"Convert a callback-based repository call to suspend functions: sequential-looking code, dispatcher made explicit — state what changed about threading.",
"Pick the scope function for five snippets (transform, configure, compute, side-effect, nullable chain) — state the return-and-receiver rule each time.",
"Draw the Java-interop boundary for one module: mark every platform type, add the nullability annotations, and write the defensive check at the seam.",
],
"project": ("Kotlin core portfolio. A small module demonstrating: null-safe API handling with the boundary defenses marked, a sealed UI-state hierarchy with exhaustive "
"handling, a suspend-based data call, scope functions chosen by the rule, and one by-lazy expensive init with the lateinit comparison. Each with the interview-style "
"explanation. Deliverable: the module plus explanations — language depth, defended."),
"honesty": ("Honest scope: Kotlin evolves — coroutines and language features gain new idioms yearly, and this course confers no certificate. State the version your answers "
"assume; interviewers respect current knowledge over memorized snapshots."),
},
"android-interview-prep--android-framework": {
"summary": ("Welcome to The Android Framework — module 2 of the Android path. I'm your instructor, and this is the framework without folklore: lifecycles, the back "
"stack, and background work — the platform facts Android interviews assume cold. We cover activities, fragments, and lifecycles; intents and the task back stack; views, "
"ViewGroups, and measurement; services, broadcast receivers, and WorkManager; and the permissions model. By the end, the lifecycle will be a contract you code against."),
"concepts": [
("Lifecycle as contract", "Init in onCreate, symmetric cleanup in onDestroy — code against the callbacks, not around them; ViewModels survive what activities don't."),
("Configuration changes", "Destroy-and-recreate on rotation — the reason state lives in ViewModels, not activities."),
("Intents", "The messaging primitive: explicit (targeted at a component) vs implicit (resolved by the system via intent filters) — deep links are intents from outside."),
("Task back stack", "The ordered activities behind the back button — shaped by launch modes and intent flags; the navigation model interviews assume."),
("Measure/layout passes", "Measure negotiates size (MeasureSpec: EXACTLY/AT_MOST/UNSPECIFIED), layout assigns position — custom views implement onMeasure/onLayout."),
("Foreground service", "User-visible long work (playback) — the only long-running background shape the user consents to."),
("WorkManager", "Deferrable guaranteed work (sync, uploads): battery-aware, survives restarts, respects Doze — the modern default for background work."),
("Broadcast receivers", "System-event hooks — for reacting to the outside world, not for doing the work itself."),
("Permissions model", "Install-time vs runtime, groups, one-time and while-in-use grants — 'permissions are a trust negotiation, not a manifest entry.'"),
("In-context permission requests", "Ask when the feature needs it, with a rationale, handle denial gracefully — the UX rule that decides grant rates."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Trace an activity through rotation, back-press, and process death on paper: name every callback and what state survives each — then verify with logging.",
"Route three navigations (in-app, deep link, share intent): explicit vs implicit, the intent flags shaping the back stack — state the resolution rule each time.",
"Implement a custom view's onMeasure/onLayout for a simple layout: predict the MeasureSpec modes, verify with logging, fix the AT_MOST wrap_content case.",
"Schedule one deferrable job three ways (raw service, receiver, WorkManager): write the honest comparison — then keep the WorkManager version and state why.",
"Implement one runtime-permission flow in context with rationale and graceful denial — the trust-negotiation shape, complete.",
],
"project": ("Framework fluency portfolio. A sample app exercising: lifecycle-correct state (survives rotation), deep-link routing, a custom view with correct measurement, "
"WorkManager-scheduled sync, and an in-context permission flow — each with the one-paragraph 'platform fact' it demonstrates. Deliverable: the app plus the fact log — "
"the framework, without folklore."),
"honesty": ("Honest scope: the framework is a moving target — APIs deprecate, recommendations shift (Compose, anyone), and this course confers no certificate. Learn the "
"current guidance alongside these fundamentals; interviewers test both the facts and your awareness that they change."),
},
"android-interview-prep--android-concurrency": {
"summary": ("Welcome to Coroutines and Concurrency — module 3 of the Android path. I'm your instructor, and this is concurrency the modern Android way: structured "
"coroutines, Flows, and lifecycle-aware scopes — plus RxJava literacy for the legacy code you will inherit. We cover suspend functions and dispatchers, structured "
"concurrency and scopes, cold/hot Flows with StateFlow and SharedFlow, viewModelScope, and cancellation with exception handling. By the end, lifecycle bugs will be "
"impossible by construction — and you'll be able to prove it."),
"concepts": [
("Suspend functions", "Sequential-looking async that pauses without blocking threads — the unit of coroutine work."),
("Dispatchers", "Main (UI), IO (blocking I/O), Default (CPU work) — the pool choice made explicit per call."),
("Structured concurrency", "Child lifetimes tied to scopes: cancellation and completion propagate through the structure — no detached work leaking."),
("coroutineScope vs supervisorScope", "coroutineScope: a child's failure cancels siblings. supervisorScope: failures isolated — 'failure policy is a design choice, stated up front.'"),
("Cold flows", "Start work per collector — the stream that doesn't exist until observed."),
("StateFlow", "Hot, holds the latest value, replays to new collectors — UI state; rotation-safe by construction."),
("SharedFlow", "Hot, configurable replay/buffer — one-shot events (with the caveat that events are often better modeled as state)."),
("viewModelScope", "A CoroutineScope tied to the ViewModel lifecycle — cancelled automatically on clearance; no leaked coroutines on rotation."),
("Cooperative cancellation", "Checkpoints at suspension points — cancellation propagates through structured scopes automatically."),
("RxJava literacy", "Disposables as the Jobs/scopes equivalent — the legacy vocabulary for the codebases you'll inherit."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Convert a callback chain to suspend functions with explicit dispatchers: state the thread each part runs on before and after.",
"Build a task hierarchy with coroutineScope, fail one child, observe the sibling cancellation — then switch to supervisorScope and observe the isolation.",
"Model one screen's state in StateFlow and its one-shot events in SharedFlow: rotate the device and verify the state replay; state the events-as-state caveat.",
"Launch work in viewModelScope, rotate, and verify cancellation — then write the sentence: 'structured concurrency makes this leak impossible by construction.'",
"Translate one RxJava chain (map/filter/dispose) to coroutines/Flow: name the Disposable→Job mapping at each step — the literacy drill for legacy code.",
],
"project": ("Concurrency portfolio. A feature demonstrating: suspend-based data loading with explicit dispatchers, a StateFlow UI state with SharedFlow events, "
"viewModelScope lifecycle safety (with the rotation test), and one RxJava-to-coroutines translation with the mapping documented. Deliverable: the feature plus "
"explanations — modern concurrency, proven."),
"honesty": ("Honest scope: coroutines are the current idiom, not the eternal one — RxJava still runs production code you'll inherit, and this course confers no "
"certificate. Literacy in both is the honest position; fluency in the modern one is the interview position."),
},
"android-interview-prep--android-persistence": {
"summary": ("Welcome to Persistence on Android — module 4 of the Android path. I'm your instructor, and this is the Android persistence ladder: DataStore, Room, "
"scoped storage, and encrypted prefs — selected with reasons, not habit. We cover SharedPreferences versus DataStore, Room (entities, DAOs, migrations), SQLite "
"under Room, files and scoped storage, and encrypted storage for secrets. By the end, 'why this store?' will be your reflex."),
"concepts": [
("SharedPreferences", "Synchronous-ish XML, no type safety, main-thread reads risk ANRs — legacy you migrate, not code you write."),
("DataStore", "Preferences/Proto: coroutine/Flow-based, async, transactional, typed schemas — the modern preferences store."),
("Room", "SQLite with compile-time safety: @Entity tables, @Dao interfaces with build-time query checking, migrations — 'Room doesn't replace SQLite, it civilizes it.'"),
("DAO", "The data-access seam: queries declared as interface methods, validated at compile time — bad queries fail the build."),
("Migrations", "Schema changes as versioned steps — never destructive in production; the upgrade path is part of the design."),
("SQLite under Room", "The same relational engine underneath — migrations, complex queries, and debugging all bottom out at SQL."),
("Scoped storage", "App-specific directories need no permissions; shared media via MediaStore — no more broad external-storage access."),
("Encrypted storage", "EncryptedSharedPreferences/DataStore backed by the Android Keystore — secrets never in plaintext."),
("Android Keystore", "Hardware-backed key storage — keys that never leave secure hardware can't be extracted from a stolen file."),
("Access-pattern-first choice", "Preferences → DataStore; relational → Room; documents → files; secrets → Keystore; blobs → files with DB metadata."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Migrate a SharedPreferences usage to DataStore: convert the reads to Flows, handle the async, and state what the migration bought.",
"Build a Room database for two entities with a relation: write the DAO, trigger a compile-time query error deliberately, fix it — the safety, demonstrated.",
"Write a migration for adding a column: version bump, the migration object, the test — then state the 'never destructive in prod' rule it enforces.",
"Store three data kinds correctly (a setting, a relational dataset, a secret): DataStore, Room, encrypted prefs — state the access-pattern rule per choice.",
"Write one raw SQL query Room can't express cleanly, run it through the DAO, and explain when you drop below the abstraction.",
],
"project": ("Persistence-ladder showcase. One app using every rung correctly: DataStore for settings, Room for relational data with a tested migration, scoped storage "
"for files, Keystore-backed encrypted storage for the token — each choice documented with the access-pattern argument. Deliverable: the app plus the choice log — "
"the ladder, climbed deliberately."),
"honesty": ("Honest scope: persistence guidance is platform-shaped and version-sensitive — DataStore vs SharedPreferences is a migration story, not a debate, and this "
"course confers no certificate. State the API levels your answers assume."),
},
"android-interview-prep--android-arch": {
"summary": ("Welcome to App Architecture — module 5 of the Android path. I'm your instructor, and this is architecture the Google-recommended way: layers, DI, and "
"offline-first — discussed as tradeoffs so the design round sounds senior. We cover MVVM with ViewModel and Flow, the repository pattern, Hilt DI, single-activity "
"with Navigation, offline-first design, and testing layers. By the end, you will design the seams first — because the code follows the seams."),
"concepts": [
("MVVM on Android", "UI observes ViewModel StateFlow; ViewModel calls the repository; unidirectional data flow — events up, state down."),
("Repository pattern", "'The only class that knows where data lives': mediating network and Room, the seam the tests target."),
("Hilt", "Constructor injection with generated components: testable (swap fakes), lifecycle-aware scoping — 'the class declares needs, Hilt supplies them.'"),
("Single-activity + Navigation", "One Activity, many destinations: shared ViewModel scoping, consistent back-stack, deep-link routing in one graph — 'the Activity is the stage; destinations are the scenes.'"),
("Navigation graph", "Declarative destinations, arguments, and back-stack behavior in one place — navigation as data."),
("Offline-first", "Local database as source of truth; UI reads local, writes queue for sync; conflict-resolution policy stated — 'what happens when the sync conflicts?'"),
("Sync strategy", "WorkManager for deferred sync; the repository mediating network ↔ cache; UI states for stale/offline."),
("Testing layers", "Unit (JUnit + fakes, fast) → Espresso (critical journeys, slow, few) → screenshot (visual regressions) — 'logic in units, devices for what only devices prove.'"),
("Seams-first design", "Architecture as the shape of the boundaries — implementations follow; seams are where testability lives."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Structure one feature as UI → ViewModel (StateFlow) → Repository → (network + Room): draw the seams, then implement — state what each layer owns.",
"Add Hilt: constructor-inject the repository, scope it, swap a fake in tests — show the test that DI made possible.",
"Convert the feature to offline-first: Room as source of truth, WorkManager sync, conflict policy written down — then test airplane-mode behavior.",
"Define the Navigation graph for three destinations with arguments and deep links: verify the back stack behaves — state the graph's job in one sentence.",
"Write the testing pyramid for the feature: view-model units with fakes, one Espresso journey, the screenshot case — state what each layer proves.",
],
"project": ("Architecture brief + build. The offline-first feature, complete: layered MVVM with Hilt, repository mediating network and Room, Navigation graph, sync with "
"conflict policy, and the three-layer test plan — plus the one-page architecture brief (pattern choice, forces, the conditional that would change it). Deliverable: "
"the feature and the brief — seams designed first."),
"honesty": ("Honest scope: 'Google-recommended' is a snapshot — recommendations evolve (and teams deviate), and this course confers no certificate. State the guidance "
"version you follow; interviewers reward awareness of the drift, not recitation of a snapshot."),
},
"android-interview-prep--android-guided-build": {
"summary": ("Welcome to the Guided Android App Build — module 6 of the Android path. I'm your instructor, and this is a complete offline-first app — network, Room, "
"Compose — built to be walked through as the centerpiece of the Android loop. We build a list-detail app with offline cache: the spec, networking with Retrofit and "
"coroutines, a Room-backed repository, Compose UI with ViewModels, and unit tests for the repository. By the end, the build narrative will be as rehearsed as the build."),
"concepts": [
("List-detail with offline cache", "The canonical Android interview app: every layer exercised — network, cache, UI — with offline as the design constraint."),
("Retrofit + coroutines", "Typed endpoints as suspend functions: declarative HTTP with structured concurrency — the networking layer interviews expect."),
("Room-backed repository", "Network ↔ Room mediation behind one data API — fakes for network/DB in tests; 'state-based testing with fakes is robust.'"),
("Compose + ViewModel", "'Compose is the renderer, the ViewModel is the state machine, the repository is the seam' — each tested at its own layer."),
("Repository tests with fakes", "Working in-memory fakes testing state transitions — not interaction-counting mocks; robust over brittle."),
("Build narrative", "Problem → constraints → key decisions (with rejected alternatives) → result → 'what I'd do with more time.'"),
("Senior answer structure", "Definition, mechanism, fit-and-tradeoff — then stop; structure separating senior answers from recitation."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write the spec: list-detail with offline cache — screens, cache policy, the explicit non-goals — sign it off before coding.",
"Build the Retrofit layer: typed endpoints as suspend functions, error mapping, auth interceptor — test it faked before any UI.",
"Add the Room-backed repository: network ↔ cache mediation, the offline policy — unit-test it with fakes for both sources.",
"Build the Compose UI on ViewModels: StateFlow down, events up — keep decisions in the ViewModel.",
"Write the repository unit tests, then rehearse the narrative: decisions first, rejected alternatives named, 'what I'd do with more time' last.",
],
"project": ("The guided build, complete. The offline-first list-detail app: Retrofit networking, Room-backed repository with unit tests, Compose UI with ViewModels — "
"plus the spec and the build narrative. Deliverable: the app, the tests, the narrative — the centerpiece of the Android loop, walkable."),
"honesty": ("Honest scope: a guided build proves execution of a known shape — real apps add product ambiguity, legacy code, and scale, and this course confers no "
"certificate. Present it as craft evidence: the layers, the tests, the decisions — sized honestly."),
},
"android-interview-prep--android-mock": {
"summary": ("Welcome to the Android Mock Circuit — the final module of the Android path. I'm your instructor, and these are Android-flavored mocks across language, "
"framework, and architecture: timed Kotlin deep-dives, framework whiteboard rounds, app-architecture design — plus the behavioral ledger — debriefed into the final "
"reps. By the end, the loop will be repetition, not discovery."),
"concepts": [
("Timed Kotlin deep-dives", "Layered answers: 30-second correct, mechanism, edge case — 'the classic bug here is…' before they ask."),
("Framework whiteboard rounds", "'I draw the system first so we both know where the deep dive lives' — lifecycles, back stack, measurement, narrated."),
("App-architecture design", "Seams-first: layers, DI, offline-first, testing story — the design-round shape for mobile."),
("Behavioral ledger", "Story bank, stories-told-where, feedback, stumping questions — every round fresh."),
("Debrief and triage", "Within the hour: leaks, holds, biggest leak by frequency × weight, 48-hour redrill."),
("Taper plan", "No new material, redrill from the log, timed mocks, rest."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Run a timed Kotlin deep-dive mock (30 min): null safety, coroutines, scope functions — layered answers, log the rambles.",
"Run a framework whiteboard mock: lifecycles, intents, WorkManager — draw first, then zoom.",
"Run an app-architecture design mock (45 min): offline-first with the conflict policy — end with tradeoffs.",
"Run one behavioral round from the ledger: two-minute STAR answers, no repeats.",
"Debrief all four within the hour: template, ranked leaks, 48-hour redrills, ledger update — then the taper.",
],
"project": ("Android mock portfolio. The four-mock circuit over two weeks — Kotlin deep dive, framework whiteboard, app-architecture design, behavioral — each debriefed "
"with the template and the ledger updated. Close with the taper schedule. Deliverable: four debriefs, the ledger, the taper — repetition, not discovery."),
"honesty": ("Honest scope: mocks simulate format, not stakes — and this course confers no certificate. Android loops vary by team (framework vs Compose depth); the "
"circuit trains the format, and team research covers the rest."),
},
}
