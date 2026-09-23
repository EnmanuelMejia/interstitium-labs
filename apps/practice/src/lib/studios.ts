import type { Block, QuizQ } from "@/lib/course";

export type Sim =
  | { kind: "threshold" }
  | { kind: "fringe"; items: { prompt: string; choices: string[]; answer: number; path: string }[] }
  | { kind: "budget" }
  | { kind: "fault"; system: string; stages: { id: string; name: string; symptom: string; fix: string }[] }
  | { kind: "triage"; title: string; cases: { log: string; choices: { label: string; right?: boolean; why: string }[] }[] }
  | { kind: "sequence"; title: string; intro: string; steps: { id: string; label: string }[]; order: string[] }
  | { kind: "classify"; title: string; intro: string; buckets: { id: string; label: string }[]; cards: { id: string; text: string; bucket: string }[] }
  | { kind: "bits"; need: string; mode: string }
  | { kind: "units" }
  | { kind: "beacon" }
  | { kind: "gpu" }
  | { kind: "reduce"; start: string; goal: string; rules: { id: string; label: string; from: string; to: string }[] };

export type Studio = {
  slug: string;
  kicker: string;
  reading: Block[];
  quiz: QuizQ[];
  sim: Sim;
};

const p = (text: string): Block => ({ kind: "p", text });
const h = (text: string): Block => ({ kind: "h", text });
const ul = (items: string[]): Block => ({ kind: "ul", items });
const note = (title: string, text: string): Block => ({ kind: "note", title, text });

export const studios: Studio[] = [
  {
    slug: "ai-aided-cybersecurity",
    kicker: "Domain 01 · nine weeks",
    reading: [
      h("A score is not an action"),
      p("This domain is an original practice built from a public nine-week outline: a control dataset, hostile tables, unsupervised anomaly scores, a text intent, an evasion nudge, and a capstone you would actually page on. Lectures, slides, and guest talks from that course are not reproduced here, and nothing here is affiliated with that school or with Microsoft."),
      p("The work is the connective layer between a model and a security decision. You fit something small, you look at the errors by hand, and you pick a threshold whose false-positive cost you can say out loud. Synthetic telemetry only. No malware binaries."),
      ul([
        "Control set first. If petal length cannot separate the easy class, the pipeline is not ready for entropy.",
        "Cleaning is part of the model: nulls, duplicate ids, and impossible entropy change the score.",
        "Evasion against a linear weight is a chart, not a weapon. Defenses are clipping and refitting.",
        "Authority stays with a person. A high score opens a case. It does not isolate a host.",
      ]),
      note("Public anchors", "scikit-learn, NIST AI 100-2 on adversarial ML, MITRE ATT&CK and ATLAS, OWASP Machine Learning Security Top 10, and FIRST EPSS. Those are the readings. This bench is the practice."),
    ],
    quiz: [
      {
        q: "What has to be true before you trust a malware-table score?",
        choices: [
          "The control set already separates an easy class",
          "Accuracy on the training rows is above 99%",
          "The model file is larger than the dataset",
          "A vendor dashboard shows a green tile",
        ],
        answer: 0,
        why: "A pipeline that cannot separate iris will not become honest because the column names sound like security.",
      },
      {
        q: "A detector flags a historian process on a plant network. What is the right authority?",
        choices: [
          "Isolate immediately. The score is the decision.",
          "Open a case. Isolation of a control-network process needs a named human.",
          "Retrain until the score drops, then ignore it.",
          "Delete the process so the metric recovers.",
        ],
        answer: 1,
        why: "The failure mode is not a bad weight. It is an automated action on something operators need in order to see the line.",
      },
    ],
    sim: { kind: "threshold" },
  },
  {
    slug: "adaptive-foundations",
    kicker: "Placement · fringe, not a personality quiz",
    reading: [
      h("Study the fringe"),
      p("A knowledge-space gate is a small set of tasks. What you miss, and only what sits just outside what you can already do, is the next assignment. Restarting a catalog at zero because one shell question failed is how people quit."),
      p("The fringe is not a vibe and not a percentile of 'aptitude'. It is the skill whose prerequisites you hold and whose problems you still miss. Later paths should cite that evidence instead of seating you in week one again."),
      ul([
        "Miss the shell, and Linux comes before Kubernetes.",
        "Miss a rate or a percentile, and ops math comes before an SLO conversation.",
        "A perfect score is not the point. A named gap is.",
      ]),
      note("Adaptive rule", "If you miss one probe, the studio names a path. If you miss none, raise the load and take the harder wording. Busywork on skills you already hold is a bug."),
    ],
    quiz: [
      {
        q: "You miss chmod and pass every Kubernetes vocabulary item. What do you study next?",
        choices: ["The CKA time-box", "Linux permissions, then come back", "A cloud cost course", "Nothing. Vocabulary outranks the miss"],
        answer: 1,
        why: "The fringe is the broken prerequisite, not the most impressive noun you recognized.",
      },
      {
        q: "What should a later path inherit from this gate?",
        choices: ["Your job title", "The tasks you missed and the ones you held", "A single percentage", "A recommended video playlist"],
        answer: 1,
        why: "Evidence is the item-level result. A percentage hides which fringe to repair.",
      },
    ],
    sim: {
      kind: "fringe",
      items: [
        {
          prompt: "A file is mode 644. The service account is not the owner and not in the group. Can it write the file?",
          choices: ["Yes, because it is a service", "No. Others have read only", "Yes, if it is a container", "Only on Sundays"],
          answer: 1,
          path: "linux-lf-essentials",
        },
        {
          prompt: "A service does 200 requests/s. The SLO allows 0.1% errors. About how many errors per second is that budget?",
          choices: ["0.2", "2", "20", "200"],
          answer: 0,
          path: "aleks-ops-math",
        },
        {
          prompt: "Readiness fails. Liveness passes. What should the Service do?",
          choices: ["Restart the container", "Drop the pod from the endpoints", "Delete the Deployment", "Scale to zero nodes"],
          answer: 1,
          path: "kubernetes-sre",
        },
        {
          prompt: "A pipeline scanner reports 40 findings and the build stays green. What do you have?",
          choices: ["A blocking control", "A report, not a control", "Admission", "Least privilege"],
          answer: 1,
          path: "devsecops-mastery",
        },
      ],
    },
  },
  {
    slug: "aleks-ops-math",
    kicker: "Rates, percentiles, budgets",
    reading: [
      h("The integer under the percentage"),
      p("Operators drown in rates that were never turned back into counts. A 0.1% error budget on a busy service is a large integer. A 0.1% error budget on a quiet internal tool might be three failures a month. The percentage is the same sentence. The action is not."),
      p("The mean hides the tail. p99 is the latency a tired user feels. Draw the mean and the tail on the same axis before you argue about a timeout. An error budget is a count you are allowed to spend. When it is gone, the change window closes, even if the dashboard is mostly green."),
      ul([
        "Errors allowed = rate × seconds × window × (1 − SLO).",
        "Burn is how fast you are spending that count, not how red the chart looks.",
        "Log scales are for quantities that span orders of magnitude. They are not a style choice.",
      ]),
      note("Check your arithmetic", "Round to the nearest request. If you are off by a thousand, you dropped a factor of the window, not a rounding error."),
    ],
    quiz: [
      {
        q: "Why is p99 a better page than the mean for a user-facing timeout?",
        choices: ["It is always higher, so it looks serious", "The mean can hide the tail the user actually waits on", "Percentiles do not need a sample", "The mean includes errors and p99 does not"],
        answer: 1,
        why: "A few slow requests move p99 and barely move the mean. The user on that request does not experience the mean.",
      },
      {
        q: "The weekly error budget is spent by Tuesday. What closes?",
        choices: ["The SLO document", "The change window, until the budget recovers", "Only the dashboard theme", "Hiring"],
        answer: 1,
        why: "A budget you do not enforce is a slogan. The action is to stop spending it.",
      },
    ],
    sim: { kind: "budget" },
  },
  {
    slug: "devops-zero-to-hire",
    kicker: "Git, CI, a cluster, a red gate",
    reading: [
      h("Green you cannot reproduce is not green"),
      p("The branch is the proposal. Main is what production is allowed to run. A commit message says why, because the diff already says what. CI fails closed: test, lint, and a build. A green check that only exists inside a vendor UI you cannot re-run is a rumor."),
      p("The interview version of this path is not a tool list. It is a failure you caused on purpose and the evidence of the repair: which stage went red, what you changed, and how you know it will fail the same way next time if someone repeats the mistake."),
      ul([
        "Read the failing step before you rerun the job.",
        "Cache misses and missing secrets look similar until you read the log line.",
        "A cluster is not required to explain CI. Do not skip ahead to hide a red test.",
      ]),
      note("Proof", "Break one stage, name it, and apply the fix that belongs to that stage. The packet in the stage stalls on the broken gate."),
    ],
    quiz: [
      {
        q: "A job is green on the vendor and red on your laptop. What is it?",
        choices: ["Green enough to merge", "Not green. You cannot reproduce it", "A flaky network, ignore it", "Proof the laptop is wrong"],
        answer: 1,
        why: "If you cannot re-run the check, you cannot trust the check.",
      },
      {
        q: "What does main mean in this path?",
        choices: ["The branch with the most commits", "What production is allowed to run", "A personal draft", "The branch CI ignores"],
        answer: 1,
        why: "Main is an authority boundary, not a popularity contest.",
      },
    ],
    sim: {
      kind: "fault",
      system: "Delivery pipeline",
      stages: [
        { id: "git", name: "Git", symptom: "The commit message is empty, but the diff is the one you reviewed.", fix: "Rewrite the message. Do not bypass the hook." },
        { id: "test", name: "Test", symptom: "CI is red on a unit test that also fails locally in 2 seconds.", fix: "Fix the assertion. Do not rerun until the log changes." },
        { id: "build", name: "Image build", symptom: "The Dockerfile copies a secret into a layer. The tests passed.", fix: "Remove the secret from the build context and rotate it." },
        { id: "deploy", name: "Deploy", symptom: "The new image never rolls. The previous revision is still Ready.", fix: "Read the rollout status before you push another tag." },
      ],
    },
  },
  {
    slug: "k8s-cka-exceed",
    kicker: "Objects, events, then YAML",
    reading: [
      h("Events before guesses"),
      p("Pod, Deployment, Service, Ingress, ConfigMap, Secret. You should be able to say which object holds the desired count, which one holds the selector, and which one is just a bag of configuration. Mixing those up is how a time-box dies."),
      p("The order is describe, logs, events, then exec. Editing YAML because the pod 'looks wrong' spends the clock on a hypothesis you have not checked. The exceed bar is not a green pod. It is being able to say why the scheduler placed it, or why it refused."),
      ul([
        "CrashLoopBackOff: previous logs, then the probe, then the command.",
        "Pending: events will usually name the resource or the taint.",
        "Endpoints empty: selector, not the Service port you keep retyping.",
      ]),
      note("Time box", "At higher load the log is shorter. You still do not get to edit a random object."),
    ],
    quiz: [
      {
        q: "A Service has no endpoints. What do you check first?",
        choices: ["The cloud bill", "Whether any pod labels match the selector", "The Ingress certificate", "The node image"],
        answer: 1,
        why: "Endpoints are a label match. The port number is the second question.",
      },
      {
        q: "Which object owns the desired replica count?",
        choices: ["ConfigMap", "Secret", "Deployment (or another controller)", "Service"],
        answer: 2,
        why: "The Service routes. The controller holds the count. A ConfigMap holds configuration.",
      },
    ],
    sim: {
      kind: "triage",
      title: "Control-plane scraps",
      cases: [
        {
          log: "Pod web-0  Pending. Events: 0/3 nodes available: 3 Insufficient cpu.",
          choices: [
            { label: "Lower the CPU request or free a node", right: true, why: "The scheduler already named the resource." },
            { label: "Delete the Service", why: "The Service is not why the pod is Pending." },
            { label: "Turn off the liveness probe", why: "It has not started. Probes are not the event." },
          ],
        },
        {
          log: "Pod api-1  CrashLoopBackOff. Last log: connection refused 127.0.0.1:5432. Liveness hits /health on port 8080.",
          choices: [
            { label: "Point the app at the database Service, not localhost", right: true, why: "The process is crashing before the probe matters." },
            { label: "Delete kube-system", why: "That is not a repair." },
            { label: "Scale the Deployment to zero and call it fixed", why: "Absence is not a passing probe." },
          ],
        },
        {
          log: "Service payments has Endpoints: <none>. Pods are Running with label app=pay. Selector is app=payments.",
          choices: [
            { label: "Fix the selector so it matches the pod label", right: true, why: "Endpoints are a label join." },
            { label: "Add more replicas", why: "More pods with the wrong label still will not join." },
            { label: "Change the container port only", why: "The port is not why the endpoint list is empty." },
          ],
        },
      ],
    },
  },
  {
    slug: "kubernetes-sre",
    kicker: "Probes, requests, burn",
    reading: [
      h("Liveness restarts. Readiness removes."),
      p("A liveness probe that checks a dependency will restart your process whenever the dependency blips, and the restart makes the blip worse. Readiness is how you leave the Service. Mixing them up is either a restart loop or a black hole that still looks Running."),
      p("Set requests from measurement. Limits without requests let the scheduler lie about what fits. Page on burn rate, not on a single 500. A deploy that spends the week's budget rolls back, even if the error rate 'came back down'."),
      ul([
        "Startup probes exist so a slow boot is not a crash loop.",
        "An error budget is shared with the change process, not owned by the dashboard.",
        "HPA on CPU you never requested will not do what you think.",
      ]),
      note("Authority", "The replica count is a consequence of the budget and the probes, not a mood."),
    ],
    quiz: [
      {
        q: "Liveness checks a remote database and the database blips. What happens?",
        choices: ["The pod leaves the Service until the database returns", "The container restarts, often in a loop", "Nothing. Liveness is advisory", "The Deployment is deleted"],
        answer: 1,
        why: "Liveness failure kills the container. Readiness is the one that should fail closed on a dependency.",
      },
      {
        q: "What should a page follow?",
        choices: ["Any single 500", "Burn rate against the budget", "CPU over 10%", "A green pipeline"],
        answer: 1,
        why: "One error is not a page. Spending the budget too fast is.",
      },
    ],
    sim: {
      kind: "triage",
      title: "Probe and budget",
      cases: [
        {
          log: "Restarts: 14. Liveness: GET /health, which calls the payments dependency. Readiness: the same URL.",
          choices: [
            { label: "Liveness should be process-local. Readiness may check the dependency.", right: true, why: "Restarting does not bring the dependency back." },
            { label: "Remove both probes", why: "Then a dead process stays in the Service." },
            { label: "Set replicas to 1", why: "Fewer copies of a restart loop is still a restart loop." },
          ],
        },
        {
          log: "SLO 99.9% over 30 days. You have spent 80% of the budget in 2 days. A feature deploy is queued.",
          choices: [
            { label: "Stop the deploy. The burn rate says the budget will not last the window.", right: true, why: "The budget is a change brake." },
            { label: "Ship it. The SLO percentage still looks high today.", why: "Today's percentage hides the burn." },
            { label: "Raise the SLO number in the doc so the budget returns", why: "Editing the slogan is not reliability." },
          ],
        },
        {
          log: "HPA targets CPU 70%. Pod spec has limits and no requests. Scheduler status is tight.",
          choices: [
            { label: "Set requests from a measurement, then keep the HPA target", right: true, why: "Utilization is relative to the request." },
            { label: "Delete the HPA", why: "The missing request is the bug, not the idea of scaling." },
            { label: "Set the limit to 1 millicore", why: "That throttles the process. It does not define the request." },
          ],
        },
      ],
    },
  },
  {
    slug: "devsecops-mastery",
    kicker: "One control that can fail",
    reading: [
      h("A scanner that never fails the build is a report"),
      p("Shift-left theater is a PDF in the pull request. A control is a rule that can reject the change. Pick one high-signal rule and make it blocking before you add twenty that everyone waives."),
      p("Workload identity beats a long-lived key in a Secret. The pipeline assumes a role for the few minutes it needs. Admission should reject privileged pods and hostPath unless an exception names an owner and an expiry."),
      ul([
        "Blocking in CI for the artifact. Blocking at admission for the runtime shape.",
        "Exceptions are objects with names, not a comment that says 'temporary'.",
        "Identity is not a scanner finding. It is how the job authenticates.",
      ]),
      note("Sort the controls", "Some of these are real gates. Some are souvenirs. The simulation asks you which is which."),
    ],
    quiz: [
      {
        q: "Forty findings, build still green. What failed?",
        choices: ["The developers", "The control. It cannot reject anything", "The cluster", "The ticket tracker"],
        answer: 1,
        why: "If the build cannot go red, you published a report.",
      },
      {
        q: "Where should a cloud key for deploy live?",
        choices: ["In a Kubernetes Secret committed to git", "Nowhere long-lived. The job assumes a role", "In the Dockerfile ENV", "In the Slack canvas"],
        answer: 1,
        why: "A key in a file outlives the job and leaks with the repo.",
      },
    ],
    sim: {
      kind: "classify",
      title: "Control or souvenir",
      intro: "Sort each practice. A control can fail a change. A souvenir cannot.",
      buckets: [
        { id: "control", label: "Control" },
        { id: "souvenir", label: "Souvenir" },
      ],
      cards: [
        { id: "c1", text: "CI fails the job when a critical dependency advisory matches a direct import", bucket: "control" },
        { id: "c2", text: "A weekly PDF of container findings, mailed to a list nobody owns", bucket: "souvenir" },
        { id: "c3", text: "Admission rejects hostPath unless an exception names an owner and an expiry", bucket: "control" },
        { id: "c4", text: "A wiki page titled 'we should not be root'", bucket: "souvenir" },
        { id: "c5", text: "The deploy job assumes a role that expires in minutes", bucket: "control" },
        { id: "c6", text: "A badge that says 'scanned' and links to an empty project", bucket: "souvenir" },
      ],
    },
  },
  {
    slug: "secops-blue-team",
    kicker: "Hypothesis, then a page you can reject",
    reading: [
      h("No source, no detection"),
      p("A detection starts as a hypothesis: the technique, the log source, and the decision a human will make. Beaconing is regularity plus rarity. A flood is a different page. Volume and interval answer different questions, and combining them into one 'suspicious' word is how queues fill with junk."),
      p("A score does not isolate a host. It opens a case a human can reject. Write the false-positive story before you celebrate recall. If you cannot name a benign pattern that will also match, you do not know the detection yet."),
      ul([
        "Name the log source in the first sentence.",
        "Separate beaconing (steady gaps) from spikes (volume).",
        "Record the false-positive you are willing to accept.",
      ]),
      note("This bench", "You tune a gap rule against synthetic hosts. It is not a SIEM, and it does not contain anyone's traffic."),
    ],
    quiz: [
      {
        q: "What makes a beacon different from a scan?",
        choices: ["Beacons are always encrypted", "Beacons are regular and rare. Scans are loud and short", "Beacons only happen on UDP", "There is no difference"],
        answer: 1,
        why: "Interval structure is the signal. Volume is a different hypothesis.",
      },
      {
        q: "When is a detection allowed to isolate a host by itself?",
        choices: ["Whenever recall is high", "It is not. A person accepts the case", "If the vendor says so", "On Fridays"],
        answer: 1,
        why: "Authority stays with the analyst. The model proposes.",
      },
    ],
    sim: { kind: "beacon" },
  },
  {
    slug: "aws-cloud-ops",
    kicker: "Route, security group, NACL, then identity",
    reading: [
      h("Three different nos"),
      p("A packet can die in the subnet route table, in the security group, or in the network ACL, and those are not the same object. Check them in that order: is there a route, is the group allowing the flow, did a stateless ACL forget the return. Then, and only then, suspect the application."),
      p("The deny you cannot see is often a permission boundary, a session policy, or an organization policy, not the inline policy you just edited. If it is not in a log group with a retention you chose, the next shift will treat it as if it did not happen."),
      ul([
        "Security groups are stateful. NACLs are not.",
        "An SCP can deny what an identity policy allows.",
        "Write the log group name in the runbook, not 'check CloudWatch'.",
      ]),
      note("Order", "The simulation starts the checks in the wrong order on purpose. Put them back."),
    ],
    quiz: [
      {
        q: "Security group allows the port. The flow still dies, and the return is missing. What is a likely cause?",
        choices: ["A stateless NACL that allows the request and not the reply", "The AZ ran out of letters", "The IAM user has no MFA", "The bill is unpaid"],
        answer: 0,
        why: "Groups remember the connection. NACLs do not. The return rule is a separate line.",
      },
      {
        q: "You edited the identity policy and the deny remains. What else can deny?",
        choices: ["Only the policy you edited", "A boundary, a session policy, or an SCP", "The security group", "The route table"],
        answer: 1,
        why: "Allow in one document does not beat an explicit deny higher up.",
      },
    ],
    sim: {
      kind: "sequence",
      title: "Where the request died",
      intro: "A private instance cannot reach the internet, then a second call is AccessDenied. Order the checks.",
      steps: [
        { id: "iam", label: "Read the identity, then the boundary and the SCP" },
        { id: "nacl", label: "Check the NACL, including the return" },
        { id: "sg", label: "Check the security group egress and ingress" },
        { id: "route", label: "Check the subnet route (and the NAT, if private)" },
      ],
      order: ["route", "sg", "nacl", "iam"],
    },
  },
  {
    slug: "aws-cloud-practitioner-plus",
    kicker: "Shared responsibility, then a monthly number",
    reading: [
      h("They run the hypervisor. You run the guest."),
      p("The exam is vocabulary. The plus is a diagram you can defend with a monthly number on it. Shared responsibility is not a slogan: the provider runs the facilities and the hypervisor. You run the guest operating system, the data, the identity, and the network rules you wrote."),
      p("Data transfer and idle load balancers surprise people. NAT gateways surprise them twice, because the charge is hours plus gigabytes and it does not look like a server. Price the design before you build it, including the path the bytes actually take."),
      ul([
        "If you can ssh to it, patching it is yours.",
        "If you stored the object, the ACL and the encryption choice are yours.",
        "A free-tier story is not an architecture.",
      ]),
      note("Sort the plane", "Upper plane is the provider. Lower plane is yours. The simulation does not accept 'it depends' as a bucket."),
    ],
    quiz: [
      {
        q: "Who patches the guest OS on a virtual machine you launched?",
        choices: ["The provider, always", "You", "Whoever pays the bill, automatically", "The hypervisor"],
        answer: 1,
        why: "The hypervisor is theirs. The guest is yours.",
      },
      {
        q: "Which charge do people forget on a private subnet that pulls packages?",
        choices: ["The IAM user", "NAT gateway hours and data processing", "The route table object", "A certificate name"],
        answer: 1,
        why: "NAT is not free just because you cannot see a server named NAT in your mental diagram.",
      },
    ],
    sim: {
      kind: "classify",
      title: "Whose failure is this?",
      intro: "Put each failure on the plane that owns it.",
      buckets: [
        { id: "theirs", label: "Provider" },
        { id: "yours", label: "Yours" },
      ],
      cards: [
        { id: "a", text: "The physical host loses power in a single facility", bucket: "theirs" },
        { id: "b", text: "The guest OS has an unpatched package you installed", bucket: "yours" },
        { id: "c", text: "An object store ACL is public because you set it that way", bucket: "yours" },
        { id: "d", text: "The hypervisor itself is compromised", bucket: "theirs" },
        { id: "e", text: "A security group allows 0.0.0.0/0 on the admin port", bucket: "yours" },
        { id: "f", text: "A region-wide control-plane outage", bucket: "theirs" },
      ],
    },
  },
  {
    slug: "iac-terraform-gitops",
    kicker: "Plan, apply, drift",
    reading: [
      h("Read the destroy before you apply it"),
      p("A plan is a diff with consequences. A destroy on a stateful resource is a stop, not a surprise you notice in the apply log. Two applies without a lock corrupt state. State is a secret: it often holds attributes you would not put in git."),
      p("GitOps means the cluster follows git. A hotfix typed into the cluster is drift until it is a commit. Drift is not automatically bad — sometimes production was right — but it is unnamed until you classify it as a desired change or as something to revert."),
      ul([
        "Lock the state. One writer.",
        "Plan in the pull request. Apply from the branch you merged.",
        "A live edit is a proposal until git says so.",
      ]),
      note("Classify", "Each diff is either desired (put it in git) or drift (revert it to git). Do not call both 'a change'."),
    ],
    quiz: [
      {
        q: "Two engineers apply at once and state tears. What was missing?",
        choices: ["A prettier theme", "A lock", "More variables", "A larger instance"],
        answer: 1,
        why: "State has one writer. The lock is that rule.",
      },
      {
        q: "Someone kubectl-edited a replica count that git does not have. What is it?",
        choices: ["The new desired state, automatically", "Drift, until a commit says otherwise", "A provider outage", "A plan that already applied"],
        answer: 1,
        why: "GitOps: git is the desired state. The cluster catching up is the job.",
      },
    ],
    sim: {
      kind: "classify",
      title: "Desired or drift",
      intro: "Git is the source of truth. Sort the live differences.",
      buckets: [
        { id: "desired", label: "Make git match it" },
        { id: "drift", label: "Revert to git" },
      ],
      cards: [
        { id: "d1", text: "A replica bump done in the incident channel, never reviewed, 'just for tonight' three weeks ago", bucket: "drift" },
        { id: "d2", text: "A merged pull request adds a tag the cluster has not synced yet", bucket: "desired" },
        { id: "d3", text: "An operator opened port 22 on a security group from the console during a demo", bucket: "drift" },
        { id: "d4", text: "The plan in the open pull request adds a log retention you already agreed", bucket: "desired" },
      ],
    },
  },
  {
    slug: "linux-lf-essentials",
    kicker: "Permissions, processes, logs",
    reading: [
      h("User, group, other"),
      p("A service account is not root. If the file is 777, you have not finished. Read, write, and execute are three bits, and the execute bit on a directory means something different than it does on a file: it is the right to traverse."),
      p("ps and the parent process tell you what will respawn. Killing children of a supervisor is a hobby. journalctl for the unit beats scrolling /var/log until a line looks red. Know which log is the unit's log before the incident, not during it."),
      ul([
        "644 is rw-r--r--. 755 is rwxr-xr-x. 640 keeps others out.",
        "The directory's execute bit is traversal, not 'run this folder'.",
        "Kill the parent if the children come back.",
      ]),
      note("Set the mode", "The studio asks for one mode. Build it from bits, not from memory of a lucky chmod."),
    ],
    quiz: [
      {
        q: "Mode 777 on a config file means what?",
        choices: ["It is finished and portable", "Everyone can read and write it. You are not done", "Only root can read it", "It is immutable"],
        answer: 1,
        why: "World-writable configuration is an unfinished permission.",
      },
      {
        q: "Children of a service keep returning after you kill them. What do you look at?",
        choices: ["The parent supervisor", "The file's color in ls", "The hostname", "The inode of /tmp"],
        answer: 0,
        why: "A supervisor's job is to respawn. Kill or stop the parent.",
      },
    ],
    sim: { kind: "bits", need: "The service user must read and write the log. The group may read. Others get nothing.", mode: "640" },
  },
  {
    slug: "linux-rhcsa-spine",
    kicker: "Boot, users, units",
    reading: [
      h("Enable is not start"),
      p("A unit that starts now and dies on reboot was not enabled. systemctl start affects this boot. enable wires the next ones. Practice the difference before a clock is running, because the exam will not explain it to you."),
      p("Boot recovery is a procedure you have done, not a paragraph you have read. Know how to reach an emergency target and why you would. Users, groups, and a sudoers drop-in are ordinary work: a home directory you meant to create, a group the service is actually in."),
      ul([
        "start: now. enable: across reboot. Both, if you want both.",
        "A drop-in file beats editing the vendor unit.",
        "Emergency and rescue are different targets. Know which one still mounts what you need.",
      ]),
      note("Pick the verb", "Each scrap needs one action. The wrong verb is how a host comes back unprotected, or not at all."),
    ],
    quiz: [
      {
        q: "You started a unit and rebooted. It is dead. What did you skip?",
        choices: ["enable", "A new hostname", "chmod 777", "A second start"],
        answer: 0,
        why: "start does not install the boot symlink. enable does.",
      },
      {
        q: "Where should a local override of a vendor unit live?",
        choices: ["Inside the vendor file, so it is one place", "A drop-in", "In /tmp", "In the user's bashrc"],
        answer: 1,
        why: "Package updates replace the vendor unit. A drop-in survives.",
      },
    ],
    sim: { kind: "units" },
  },
  {
    slug: "python-systems",
    kicker: "Fail clearly, log the change",
    reading: [
      h("A dry run prints the plan"),
      p("Validate input at the boundary. Trust the objects you already parsed. Exit non-zero. Print the object id you failed on. An exception swallowed so cron can stay green is how a job lies for a month."),
      p("The real run does only what the dry run printed. If the apply does a second, quieter mutation, you do not have a dry run. You have a demo. Log the thing you changed, in a line a later operator can grep."),
      ul([
        "Boundary checks on the way in. No defensive copies of framework guarantees.",
        "Non-zero exit is the API cron actually reads.",
        "Side effects are listed, then performed. Not the other way around.",
      ]),
      note("Mark the run", "Some steps belong in the dry run, some only in the apply, and one of them should never run. Sort them."),
    ],
    quiz: [
      {
        q: "A script catches every exception and prints 'ok'. Cron is green. What is true?",
        choices: ["The job succeeded", "You do not know. The exit status lied", "Python forbids this", "The log is the exit code"],
        answer: 1,
        why: "Cron believes the exit code. A swallowed error is a false success.",
      },
      {
        q: "What may the apply do?",
        choices: ["Anything faster than the dry run", "Only what the dry run listed", "The opposite of the dry run, as a surprise", "Write a new plan and execute it quietly"],
        answer: 1,
        why: "If apply can invent work, the dry run was not a plan.",
      },
    ],
    sim: {
      kind: "classify",
      title: "Dry run, apply, or never",
      intro: "A script is about to touch three hosts. Sort the steps.",
      buckets: [
        { id: "dry", label: "Dry run" },
        { id: "apply", label: "Apply only" },
        { id: "never", label: "Do not ship" },
      ],
      cards: [
        { id: "s1", text: "Print the host id and the file it would change", bucket: "dry" },
        { id: "s2", text: "Write the file and log the host id", bucket: "apply" },
        { id: "s3", text: "Catch all exceptions and exit 0", bucket: "never" },
        { id: "s4", text: "Refuse a host id that is empty, before any write", bucket: "dry" },
      ],
    },
  },
  {
    slug: "platform-sre",
    kicker: "A path product teams can stay on",
    reading: [
      h("Deviation is an exception with a name"),
      p("One template that already has probes, requests, a dashboard, and a runbook link. That is the paved path. A team that copies a gist from 2019 is not 'moving faster'. They are building a second platform you will page for."),
      p("Admission is the curb. A wiki is not. Every page links to the runbook step that matches the symptom. Otherwise you trained people to silence alerts, and the template was decoration."),
      ul([
        "Golden path: probes, requests, identity, a dashboard, an owner.",
        "Exceptions expire.",
        "If the page does not name the next command, it is not a page. It is a mood.",
      ]),
      note("Stay on the path", "The simulation is a deploy request. Some of it belongs on the golden path. One line is a bypass."),
    ],
    quiz: [
      {
        q: "What makes admission different from a standards document?",
        choices: ["It is longer", "It can reject the deploy", "It is written by a vendor", "It uses more nouns"],
        answer: 1,
        why: "A curb is a control. A document is a hope.",
      },
      {
        q: "A page fires with no runbook step. What did you train?",
        choices: ["Faster responders", "People who silence the page", "Better SLOs by themselves", "Fewer deploys, automatically"],
        answer: 1,
        why: "Without a next action, the only available action is to make the noise stop.",
      },
    ],
    sim: {
      kind: "fault",
      system: "Golden path",
      stages: [
        { id: "template", name: "Template", symptom: "The service YAML has no requests and no probes. It was pasted from a gist.", fix: "Start from the paved template. Do not fork a gist." },
        { id: "policy", name: "Admission", symptom: "The pod sets privileged: true with a comment that says 'temp'.", fix: "Reject it. An exception needs an owner and an expiry." },
        { id: "page", name: "Page", symptom: "The alert links to the team homepage, not a step.", fix: "Point the alert at the runbook step that matches the symptom." },
        { id: "oncall", name: "On-call", symptom: "The dashboard exists, but the deploy bypassed it and shipped from a laptop.", fix: "Ship through the pipeline. A laptop deploy is drift." },
      ],
    },
  },
  {
    slug: "data-analyst-to-ml",
    kicker: "A decision and a label, or stay with the chart",
    reading: [
      h("If nobody acts, do not model"),
      p("What will a person do differently if the score is high? If the answer is 'nothing, but the chart will be fancier', stay with the chart. A model is a decision compressor. It is not a promotion."),
      p("Who labeled the rows, and were they looking at the future? Leakage looks like brilliance: a feature that contains the thing you are predicting, or a scaler fit on the whole table before the split. Touch the test set once. If you tune on it, it is no longer a test."),
      ul([
        "Name the action the score changes.",
        "Fit transforms on the training fold only.",
        "A feature available only after the outcome is not a feature. It is the answer.",
      ]),
      note("Leak or legitimate", "Sort the columns. One of them is the label wearing a hat."),
    ],
    quiz: [
      {
        q: "The score will not change any action. What should you ship?",
        choices: ["The model, for practice", "The chart", "A deeper network", "A second score"],
        answer: 1,
        why: "No decision, no model. The chart is the product.",
      },
      {
        q: "You tune thresholds on the test set until it looks good. What is the test set now?",
        choices: ["Still a test", "A second training set", "A larger sample, so it is finer", "Unbiased by definition"],
        answer: 1,
        why: "Every look you act on is training. The hold-out is spent.",
      },
    ],
    sim: {
      kind: "classify",
      title: "Column hygiene",
      intro: "You are predicting whether a ticket escalates. Sort the columns.",
      buckets: [
        { id: "ok", label: "Legitimate feature" },
        { id: "leak", label: "Leak or not a feature" },
      ],
      cards: [
        { id: "f1", text: "Hour of day the ticket was opened", bucket: "ok" },
        { id: "f2", text: "Whether an escalation comment was posted tomorrow", bucket: "leak" },
        { id: "f3", text: "Length of the first message", bucket: "ok" },
        { id: "f4", text: "The word 'escalated' copied from the label into a hidden field", bucket: "leak" },
        { id: "f5", text: "Queue name at the moment of arrival", bucket: "ok" },
      ],
    },
  },
  {
    slug: "data-science-certs",
    kicker: "An objective becomes a cell you can re-run",
    reading: [
      h("A screenshot of a score is not evidence"),
      p("Map each exam objective to one notebook cell with an assertion. Highlighting a PDF is not practice. The cell should fail if the metric, the split, or the leakage control is wrong, and it should fail on someone else's machine the same way."),
      p("Fit scalers inside the pipeline, on the training fold only. State the metric and the cost of a false positive in one sentence before you chase accuracy. Accuracy on a rare event is how a constant 'benign' classifier looks employable."),
      ul([
        "One objective, one re-runnable assertion.",
        "The metric matches the decision cost.",
        "No fit() on the full frame before the split.",
      ]),
      note("Pick the metric", "The simulation gives you a rare malicious class. Accuracy is a trap."),
    ],
    quiz: [
      {
        q: "A class is 1% positive. A model predicts all negative and scores 99% accuracy. What is it?",
        choices: ["Ready for the exam", "A constant classifier wearing accuracy as a costume", "Proof the data is clean", "A calibrated probability"],
        answer: 1,
        why: "Accuracy hides the class you care about. Ask for recall and precision, or a cost.",
      },
      {
        q: "Where does a scaler get fit?",
        choices: ["On all rows, so the numbers match", "On the training fold only, inside the pipeline", "On the test set, so production matches", "After you peek at the labels"],
        answer: 1,
        why: "Fitting on the full frame leaks the test distribution into the transform.",
      },
    ],
    sim: {
      kind: "triage",
      title: "Which number do you report?",
      cases: [
        {
          log: "2,000 rows. 40 malicious. Model A: accuracy 0.98, recall 0.00. Model B: accuracy 0.90, recall 0.80, precision 0.45.",
          choices: [
            { label: "Report B, and say what a false positive costs", right: true, why: "A found nothing. B has a cost you can discuss." },
            { label: "Report A. 0.98 is higher", why: "A is the majority-class costume." },
            { label: "Average the two accuracies", why: "That number does not correspond to a decision." },
          ],
        },
        {
          log: "You standardized using the mean of the entire CSV, then split 70/30, then quoted the test accuracy.",
          choices: [
            { label: "Refit the scaler on the training fold and recompute", right: true, why: "The test rows already influenced the transform." },
            { label: "Keep it. Standardization is harmless", why: "The fit is the leak, not the arithmetic." },
            { label: "Standardize the test set to zero mean on its own and keep the score", why: "A separate test scaler is a different leak, not a repair." },
          ],
        },
      ],
    },
  },
  {
    slug: "nvidia-ai",
    kicker: "Wall-clock versus the bill",
    reading: [
      h("A GPU is a shape, not a blessing"),
      p("Matrix-shaped training is where a device pays you back. A tiny tabular model pays for the driver, the data transfer, and a larger invoice, and finishes after the CPU would have finished anyway. Write the hourly number next to the epoch time before you ask for the bigger box."),
      p("Too small a batch underfills the device. Too large a batch lies about generalization and about memory. If a CPU finishes the job before lunch, keep the CPU. The interesting question is the deadline, not the logo on the chip."),
      ul([
        "Tabular, tiny: CPU.",
        "A real training loop that is wide and repeated: GPU, if the deadline cares.",
        "Always write hours × price, not 'it felt faster'.",
      ]),
      note("Pick the device", "Two jobs. One deadline each. The cheap answer and the fast answer are not always the same, and sometimes they are."),
    ],
    quiz: [
      {
        q: "A gradient-boosted model on 8,000 rows finishes on a laptop in four minutes. What does a GPU change?",
        choices: ["The science", "Mostly the bill", "The features", "The train/test split"],
        answer: 1,
        why: "The wall-clock is already short. You would be renting a device to watch it idle.",
      },
      {
        q: "A batch of 2 on a large model. What is wrong?",
        choices: ["Nothing. Small batches are always more honest", "The device is underfilled, so you pay for idle silicon", "The GPU will refuse to start", "The loss becomes the learning rate"],
        answer: 1,
        why: "Honesty about generalization does not require starving the hardware. It requires a batch you chose on purpose.",
      },
    ],
    sim: { kind: "gpu" },
  },
  {
    slug: "bny-fullstack",
    kicker: "One action, traced through the failure",
    reading: [
      h("The browser is not a trust boundary"),
      p("Trace one user action from the control they clicked to the data store and back, including the failure. The API shape is a contract. Change it with a version, not with a surprise field that old clients treat as success."),
      p("Check the session on the server that mutates state. Showing the user a stack trace is not honesty. Showing them a recoverable error and logging a correlation id is. The store is where a retry becomes a double charge if you did not think about identity of the request."),
      ul([
        "Contract, then handler, then auth, then the write.",
        "The failure you demo is part of the feature.",
        "A correlation id is how the next person finds your log line.",
      ]),
      note("Order the trace", "The request in the stage drops at the first broken station. Put the stations in the order a careful handler uses."),
    ],
    quiz: [
      {
        q: "The UI hides the delete button. Is the record safe?",
        choices: ["Yes. Hidden is the same as unauthorized", "No. The server that writes must check the session", "Yes, if the button is off-screen", "Only on mobile"],
        answer: 1,
        why: "Anyone can call the API the button would have called.",
      },
      {
        q: "You need to change a response field clients already parse. What do you do?",
        choices: ["Rename it tonight", "Version the contract", "Add it twice under both names and document neither", "Compress the JSON so the diff is smaller"],
        answer: 1,
        why: "A surprise field is a broken client. Version the change.",
      },
    ],
    sim: {
      kind: "sequence",
      title: "One user action",
      intro: "They clicked Pay. Order the stations. Auth is not the browser's job.",
      steps: [
        { id: "store", label: "Write the charge once, keyed by an idempotency id" },
        { id: "auth", label: "Check the session on the server" },
        { id: "ui", label: "Browser sends the action" },
        { id: "contract", label: "Validate the body against the contract" },
      ],
      order: ["ui", "contract", "auth", "store"],
    },
  },
  {
    slug: "fde-training",
    kicker: "Narrow, operable, then leave",
    reading: [
      h("The repo they own is the product"),
      p("One workflow, one user, one week. A platform you imagined for them is not the job. Sit with the operator long enough to name the step they actually repeat, and ship a tool that does that step. Ambition is how forward-deployed work becomes a second job they did not ask for."),
      p("Write the runbook in their words. If they cannot restart it, you are still on call. When you leave, access ends and secrets rotate. Your laptop is not the production environment, even if it has the only working copy of the script."),
      ul([
        "Narrow the workflow before you name the stack.",
        "They can restart it without you, or you are not done.",
        "Rotate what you touched. Take your access with you.",
      ]),
      note("What you leave", "Sort the artifacts. One of them must not remain on your account."),
    ],
    quiz: [
      {
        q: "They asked for a weekly export. You designed a platform. What did you skip?",
        choices: ["The logo", "The narrow workflow", "A microservice mesh", "A second cluster"],
        answer: 1,
        why: "The job was the export. The platform was your idea.",
      },
      {
        q: "You fly home tomorrow. What has to already be true?",
        choices: ["They have your personal SSH key", "They can restart it, and your access is ready to end", "The script only runs on your laptop", "The secrets stay in your password manager only"],
        answer: 1,
        why: "Leaving means they operate it and you no longer can.",
      },
    ],
    sim: {
      kind: "classify",
      title: "Leave-behind",
      intro: "Last day on site. Sort what happens to each artifact.",
      buckets: [
        { id: "theirs", label: "Theirs, in the runbook" },
        { id: "rotate", label: "Rotate or revoke" },
        { id: "drop", label: "Do not leave it" },
      ],
      cards: [
        { id: "a1", text: "The export script in a repo they own", bucket: "theirs" },
        { id: "a2", text: "A personal access token you used from your laptop", bucket: "rotate" },
        { id: "a3", text: "A paragraph in their words: how to rerun yesterday's job", bucket: "theirs" },
        { id: "a4", text: "The only copy of the working script, on your laptop", bucket: "drop" },
      ],
    },
  },
  {
    slug: "enochian-programming",
    kicker: "A rule, a rewrite, a stop",
    reading: [
      h("The symbol means what the rule says"),
      p("A formal system is not a mood and not a picture. Write the rewrite rule before you draw anything. An interpreter is a loop: match, rewrite, stop. If you cannot say why it stops, it will not stop, and the drawing will not save you."),
      p("The nested solid on this path is a stage for that lecture. It is a thing you can orbit so the structure has a body. It is not a claim about hidden physics, and it is not an invitation to mystify a machine that is only doing the rules you wrote."),
      ul([
        "Match, then rewrite. No match means the rule does not fire.",
        "Define the stop token before you start.",
        "The picture follows the rule. It does not replace it.",
      ]),
      note("Reduce", "Apply the rules until you reach the stop token. A rule that does not match does nothing. That is information, not a bug."),
    ],
    quiz: [
      {
        q: "A rule's left side is not in the current string. What happens?",
        choices: ["The interpreter invents a match", "The rule does not fire", "The program crashes by definition", "The stop token appears"],
        answer: 1,
        why: "No match, no rewrite. That is the loop.",
      },
      {
        q: "What is the monas on this path?",
        choices: ["A physical claim", "A stage: a nested solid for the lecture", "A hidden instruction set", "A required dependency"],
        answer: 1,
        why: "It is a picture of structure, after the rules. It is not the rules.",
      },
    ],
    sim: {
      kind: "reduce",
      start: "△",
      goal: "·",
      rules: [
        { id: "r1", label: "△ → □○", from: "△", to: "□○" },
        { id: "r2", label: "□ → ○", from: "□", to: "○" },
        { id: "r3", label: "○○ → ·", from: "○○", to: "·" },
      ],
    },
  },
  {
    slug: "frontier",
    kicker: "A signal joins a path, or it is a link",
    reading: [
      h("Trending is not a curriculum"),
      p("An outside signal — a paper, a cert-blueprint change, a hiring post — is a candidate annotation. Ask which existing path it changes. If it does not change an outcome or a lab, it belongs in the library as a link, not as a new path with a new name and no proof."),
      p("The exceed path stays the spine. Frontier annotates it. Replacing a thing you can already do with a feed of new nouns is how a school becomes a timeline. Primary work remains the lab you can re-run."),
      ul([
        "Does an outcome sentence change?",
        "Does a lab change?",
        "If both are no, it is a link.",
      ]),
      note("Sort the signals", "Some of these earn a change to a path you already run. Some are reading. Do not promote reading to a path to feel current."),
    ],
    quiz: [
      {
        q: "A new paper does not change any lab or outcome. Where does it go?",
        choices: ["A new path, so the catalog looks alive", "The library, as a link", "The top of every course", "A cert claim"],
        answer: 1,
        why: "No change to what you can do, no new path.",
      },
      {
        q: "What stays primary when a frontier note arrives?",
        choices: ["The note", "The path you can already practice", "Whichever has more traffic", "The vendor homepage"],
        answer: 1,
        why: "Frontier annotates. It does not replace the spine.",
      },
    ],
    sim: {
      kind: "classify",
      title: "Path, or link",
      intro: "You already run these paths. Sort the incoming signal.",
      buckets: [
        { id: "path", label: "Changes a path you run" },
        { id: "link", label: "Library link only" },
      ],
      cards: [
        { id: "n1", text: "A cert blueprint drops a Kubernetes task your CKA path still teaches as current", bucket: "path" },
        { id: "n2", text: "A blog post with a new product name and no change to any lab", bucket: "link" },
        { id: "n3", text: "A hiring screen now asks candidates to explain an error budget, and your SRE path never does", bucket: "path" },
        { id: "n4", text: "A conference talk you enjoyed", bucket: "link" },
      ],
    },
  },
  {
    slug: "vendor-map",
    kicker: "Neighbors, not copies",
    reading: [
      h("A bridge is a mapping"),
      p("KodeKloud, the Linux Foundation, Red Hat, AWS Skill Builder, ALEKS — neighbors with different proofs. You can study how a path is shaped. You cannot reuse their items, videos, or trademarks and call it a course."),
      p("Our card still has to answer what you will be able to do here, on our labs. A vendor logo is not an outcome. If the only content of a path is 'go take theirs', it is a link in this map, not a path of ours."),
      ul([
        "Name the neighbor. Do not impersonate them.",
        "Map an outcome of theirs onto a lab of ours, or admit we do not have it.",
        "Architecture can be studied. Exam items cannot be copied.",
      ]),
      note("Map or refuse", "Each card is either a fair mapping onto our work, or a copy we will not ship."),
    ],
    quiz: [
      {
        q: "What are you allowed to take from a neighbor catalog?",
        choices: ["Their videos and item bank", "The shape of a path, rewritten as our labs", "Their trademarks as our name", "A claim that passing ours is passing theirs"],
        answer: 1,
        why: "Architecture is study. Their expression and their exam are not ours.",
      },
      {
        q: "A path card with no lab of ours, only a vendor URL. What is it?",
        choices: ["A path", "A link on the vendor map", "A cert we grant", "A SuperLab"],
        answer: 1,
        why: "If we do not change what you can do here, we do not get to call it our path.",
      },
    ],
    sim: {
      kind: "classify",
      title: "Map or refuse",
      intro: "Decide what this school is allowed to ship.",
      buckets: [
        { id: "map", label: "Fair map" },
        { id: "refuse", label: "Do not ship" },
      ],
      cards: [
        { id: "v1", text: "Our probe lab, with a note that the Linux Foundation exam covers a neighboring skill", bucket: "map" },
        { id: "v2", text: "A pasted page of someone else's practice questions", bucket: "refuse" },
        { id: "v3", text: "A diagram of their public path phases, rewritten as our outcomes", bucket: "map" },
        { id: "v4", text: "Their logo in our header so it looks official", bucket: "refuse" },
      ],
    },
  },
];

export function studioBySlug(slug: string) {
  return studios.find((s) => s.slug === slug);
}
