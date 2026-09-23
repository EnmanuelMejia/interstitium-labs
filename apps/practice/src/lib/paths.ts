export type SceneId = "cluster" | "pipeline" | "lattice" | "packets" | "cloud" | "monas" | "detector" | "nodes";

export type PathCourse = {
  slug: string;
  title: string;
  outcome: string;
  scene: SceneId;
  live: string;
  phases: { name: string; text: string }[];
  deep?: "cyber";
};

export const paths: PathCourse[] = [
  {
    slug: "ai-aided-cybersecurity",
    title: "AI-aided cybersecurity",
    outcome: "Train a detector you can defend to a SOC lead: clean data, a threshold, and a known false-positive cost.",
    scene: "detector",
    live: "Hostile points pull away from the mass as the score rises.",
    deep: "cyber",
    phases: [
      { name: "Control", text: "Fit iris before any security table. If petal length cannot separate setosa, the pipeline is not ready for entropy and API counts." },
      { name: "Hostile tables", text: "Synthetic endpoint rows stand in for a malware corpus. Outliers are a hypothesis. Families are a shallower tree you can read aloud." },
      { name: "Authority", text: "Evasion nudges a linear score. The capstone is not a higher accuracy — it is a threshold you would page on a Tuesday." },
    ],
  },
  {
    slug: "adaptive-foundations",
    title: "Adaptive foundations",
    outcome: "Place yourself before a path: what you can already do, and which fringe to repair first.",
    scene: "lattice",
    live: "Cells loosen as placement stress rises. The gaps are the work.",
    phases: [
      { name: "Place", text: "A gate is a small set of tasks, not a personality quiz. Miss the shell, and Linux comes before Kubernetes." },
      { name: "Fringe", text: "The fringe is the skill just outside your reliable set. Study that, not the whole catalog." },
      { name: "Evidence", text: "Write down what the gate measured. Later paths cite it instead of restarting you at zero." },
    ],
  },
  {
    slug: "aleks-ops-math",
    title: "Ops math",
    outcome: "Use the arithmetic operators actually need: rates, percentiles, error budgets, and log scales.",
    scene: "lattice",
    live: "Spacing between cells is a percentile, not a vibe.",
    phases: [
      { name: "Rates", text: "Requests per second and errors per second are ratios. A 0.1% error rate on a huge service is still a large integer." },
      { name: "Percentiles", text: "The mean hides the tail. p99 is the latency your angry user feels. Draw both." },
      { name: "Budgets", text: "An error budget is a count you are allowed to spend. When it is gone, the change window closes." },
    ],
  },
  {
    slug: "devops-zero-to-hire",
    title: "DevOps zero to hire",
    outcome: "Ship a small service through git, CI, and a cluster, and explain the failure when the pipeline goes red.",
    scene: "pipeline",
    live: "The packet speeds up with load and stalls on a red gate.",
    phases: [
      { name: "Git as the record", text: "The branch is the proposal. Main is what production is allowed to run. A commit message says why." },
      { name: "CI", text: "Test, lint, and a build that fails closed. A green check you cannot reproduce locally is not green." },
      { name: "Proof", text: "Weekend SuperLab: break one stage on purpose and write the evidence of the repair." },
    ],
  },
  {
    slug: "k8s-cka-exceed",
    title: "Kubernetes CKA exceed",
    outcome: "Recover a broken control plane task under time, and say which object you changed.",
    scene: "cluster",
    live: "One pod leaves Ready as pressure climbs, then the scheduler places it again.",
    phases: [
      { name: "Objects", text: "Pod, Deployment, Service, Ingress, ConfigMap, Secret. Know which one holds the desired count." },
      { name: "Debug", text: "Describe, logs, events, then exec. Guessing at YAML before events is how time dies." },
      { name: "Exceed", text: "The exam is the floor. The exceed bar is explaining the scheduling decision, not only making the pod green." },
    ],
  },
  {
    slug: "kubernetes-sre",
    title: "Kubernetes SRE",
    outcome: "Hold an error budget on a service that runs as a Deployment, with probes that mean something.",
    scene: "cluster",
    live: "Replicas shed when the budget is spent.",
    phases: [
      { name: "Probes", text: "Liveness restarts. Readiness removes from the Service. Mixing them up causes a restart loop or a black hole." },
      { name: "Requests", text: "Set requests from measurement. Limits without requests make the scheduler lie." },
      { name: "Budget", text: "Page on burn rate, not on a single 500. A deploy that spends the week’s budget rolls back." },
    ],
  },
  {
    slug: "devsecops-mastery",
    title: "DevSecOps mastery",
    outcome: "Put a control in the pipeline that fails the build, and one in the cluster that fails the deploy.",
    scene: "pipeline",
    live: "A tainted artifact stops at the gate instead of reaching the cluster.",
    phases: [
      { name: "Shift left without theater", text: "A scanner that never fails the build is a report. Pick one high rule and make it blocking." },
      { name: "Identity", text: "Workload identity beats long-lived keys in a Secret. The pipeline assumes a role, it does not store one." },
      { name: "Runtime", text: "Admission should reject privileged pods and hostPath unless an exception names an owner." },
    ],
  },
  {
    slug: "secops-blue-team",
    title: "SecOps blue team",
    outcome: "Turn a hypothesis into a detection with a known false-positive story.",
    scene: "packets",
    live: "Regular small flows peel off the busy mass — beacons, not floods.",
    phases: [
      { name: "Hypothesis", text: "Name the technique, the log source, and the decision. No source, no detection." },
      { name: "Signal", text: "Beaconing is regularity plus rarity. Volume is a different page." },
      { name: "Care", text: "A score does not isolate a host. It opens a case a human can reject." },
    ],
  },
  {
    slug: "aws-cloud-ops",
    title: "AWS cloud ops",
    outcome: "Trace a request across VPC, IAM, and a log group, and name the broken permission.",
    scene: "cloud",
    live: "Planes are accounts. Traffic that crosses without a route falls through.",
    phases: [
      { name: "Network", text: "Subnet route, security group, and NACL are three different nos. Check them in that order." },
      { name: "Identity", text: "The deny you cannot see is often a permission boundary or an SCP, not the inline policy you edited." },
      { name: "Observe", text: "If it is not in a log group with a retention you chose, it did not happen for the next shift." },
    ],
  },
  {
    slug: "aws-cloud-practitioner-plus",
    title: "AWS practitioner plus",
    outcome: "Explain the shared responsibility split and price a design before you build it.",
    scene: "cloud",
    live: "The upper plane is the provider. The lower plane is yours.",
    phases: [
      { name: "Split", text: "They run the hypervisor. You run the guest, the data, and the IAM. Memorize which failures are whose." },
      { name: "Price", text: "Data transfer and idle load balancers surprise people. NAT gateways surprise them twice." },
      { name: "Plus", text: "The exam is vocabulary. The plus is a diagram you can defend with a monthly number on it." },
    ],
  },
  {
    slug: "iac-terraform-gitops",
    title: "Terraform and GitOps",
    outcome: "Plan, apply, and reconcile. Know the difference between drift and a desired change.",
    scene: "pipeline",
    live: "A second packet is drift: it should not land unless the plan said so.",
    phases: [
      { name: "Plan", text: "Read the plan. A destroy on a stateful resource is a stop, not a surprise in apply." },
      { name: "State", text: "State is a secret and a lock. Two applies without a lock corrupt it." },
      { name: "Reconcile", text: "GitOps means the cluster follows git. A hotfix on the cluster is drift until it is a commit." },
    ],
  },
  {
    slug: "linux-lf-essentials",
    title: "Linux essentials",
    outcome: "Move through a shell with permissions, processes, and logs — without a GUI.",
    scene: "nodes",
    live: "The process tree sheds a child when you raise the signal.",
    phases: [
      { name: "Permissions", text: "User, group, other. A service account is not root. If the file is 777, you have not finished." },
      { name: "Processes", text: "ps, top, and what the parent is. Kill the parent if the children respawn." },
      { name: "Logs", text: "journalctl for the unit, not a scroll through /var/log until something looks red." },
    ],
  },
  {
    slug: "linux-rhcsa-spine",
    title: "RHCSA spine",
    outcome: "Recover boot, users, and a service unit under a time box.",
    scene: "nodes",
    live: "The root of the tree stays. Leaves fail and you bring one back.",
    phases: [
      { name: "Boot", text: "Know how to reach an emergency target and why you would. Practice it before the clock." },
      { name: "Users", text: "Groups, sudoers as a drop-in file, and a home you meant to create." },
      { name: "Units", text: "Enable versus start. A unit that starts now and dies on reboot was not enabled." },
    ],
  },
  {
    slug: "python-systems",
    title: "Python systems",
    outcome: "Write a small operator script that fails clearly and logs the thing it changed.",
    scene: "nodes",
    live: "Nodes light in the order the script touches them.",
    phases: [
      { name: "Edges", text: "Validate input at the boundary. Trust the objects you already parsed." },
      { name: "Failure", text: "Exit non-zero. Print the object id you failed on. Swallowing the exception is how cron lies." },
      { name: "Side effects", text: "A dry run prints the plan. The real run does only what the dry run printed." },
    ],
  },
  {
    slug: "platform-sre",
    title: "Platform SRE",
    outcome: "Give product teams a paved path: template, policy, and an on-call they can actually use.",
    scene: "cluster",
    live: "A golden path stays lit. A bypassed deploy flickers.",
    phases: [
      { name: "Pave", text: "One template that already has probes, requests, and a dashboard. Deviation is an exception with a name." },
      { name: "Policy", text: "Admission is the paved curb. Documentation nobody reads is not a control." },
      { name: "On-call", text: "Every page links to the runbook step that matches the symptom. Otherwise you trained people to silence alerts." },
    ],
  },
  {
    slug: "data-analyst-to-ml",
    title: "Analyst to ML",
    outcome: "Leave dashboards for a model only when the decision and the label are real.",
    scene: "detector",
    live: "A labeled few pull a boundary through an unlabeled many.",
    phases: [
      { name: "Decision", text: "What will a person do differently if the score is high? If nothing, stay with the chart." },
      { name: "Label", text: "Who labeled it, and were they looking at the future? Leakage looks like brilliance." },
      { name: "Hold-out", text: "Touch the test set once. If you tune on it, it is no longer a test." },
    ],
  },
  {
    slug: "data-science-certs",
    title: "Data science certs",
    outcome: "Map a cert objective to a notebook you can re-run, not a screenshot of a score.",
    scene: "detector",
    live: "Clusters hold still. A bad feature set smears them.",
    phases: [
      { name: "Map", text: "Each exam objective becomes one notebook cell with an assertion, not a highlight in a PDF." },
      { name: "Leak", text: "Fit scalers inside the pipeline, on the training fold only." },
      { name: "Tell", text: "State the metric and the cost of a false positive in one sentence before you chase accuracy." },
    ],
  },
  {
    slug: "nvidia-ai",
    title: "NVIDIA AI",
    outcome: "Know when a GPU changes the wall-clock, and when it only changes the bill.",
    scene: "detector",
    live: "A dense core spins faster as you spend budget. The sparse edge does not.",
    phases: [
      { name: "Fit", text: "Matrix-shaped training is where a GPU pays. A tiny tabular model pays for the driver and nothing else." },
      { name: "Batch", text: "Too small a batch underfills the device. Too large a batch lies about generalization." },
      { name: "Cost", text: "Write the hourly number next to the epoch time. If a CPU finishes the job before lunch, keep the CPU." },
    ],
  },
  {
    slug: "bny-fullstack",
    title: "Full-stack delivery",
    outcome: "Trace one user action from the browser to the data store and back, including the failure.",
    scene: "pipeline",
    live: "The request moves through four stations. Stress drops it at the store.",
    phases: [
      { name: "Contract", text: "The API shape is a contract. Change it with a version, not with a surprise field." },
      { name: "Auth", text: "The browser is not a trust boundary. Check the session on the server that mutates state." },
      { name: "Failure", text: "Show the user a recoverable error. Log the correlation id. Do not show them the stack." },
    ],
  },
  {
    slug: "fde-training",
    title: "Forward deployed",
    outcome: "Sit with an operator, ship a narrow tool, and leave them able to run it without you.",
    scene: "pipeline",
    live: "The last station is theirs. If stress cuts the link, the tool should still explain itself.",
    phases: [
      { name: "Narrow", text: "One workflow, one user, one week. A platform you imagined for them is not the job." },
      { name: "Operate", text: "Write the runbook in their words. If they cannot restart it, you are still on call." },
      { name: "Leave", text: "Access ends. Secrets rotate. The repo they own is the product, not your laptop." },
    ],
  },
  {
    slug: "enochian-programming",
    title: "Hermetica and code",
    outcome: "Read a formal system and implement a small interpreter without mystifying the machine.",
    scene: "monas",
    live: "Nested solids keep their own rates. Stress shears the outer shell, not the core.",
    phases: [
      { name: "Symbol", text: "A symbol means what the rules say, not what the picture suggests. Write the rule before the drawing." },
      { name: "Reduce", text: "An interpreter is a loop: match, rewrite, stop. Define the stop condition or it will not." },
      { name: "Stage", text: "The monas is a stage for the lecture, a nested solid you can orbit. It is not a claim about hidden physics." },
    ],
  },
  {
    slug: "frontier",
    title: "Frontier tracks",
    outcome: "Map an outside signal — a paper, a cert change, a hiring post — onto a path you already run.",
    scene: "lattice",
    live: "New cells appear at the edge and join the lattice only if a path claims them.",
    phases: [
      { name: "Signal", text: "A trending topic is not a curriculum. Ask which existing path it changes." },
      { name: "Map", text: "If it does not change an outcome or a lab, it is a link in the library, not a new path." },
      { name: "Primary", text: "The exceed path stays the spine. Frontier annotates it. It does not replace the thing you can do." },
    ],
  },
  {
    slug: "vendor-map",
    title: "Vendor map",
    outcome: "See which certs and catalogs sit next to a path without pretending you cloned their courses.",
    scene: "cloud",
    live: "Vendor planes stay separate. A bridge is a mapping, not a copy.",
    phases: [
      { name: "Neighbor", text: "KodeKloud, Linux Foundation, Red Hat, AWS, ALEKS — neighbors with different proofs." },
      { name: "Do not copy", text: "Architecture can be studied. Their videos, items, and trademarks are not ours to reuse." },
      { name: "Outcome", text: "Our card still answers what you will be able to do here, on our labs." },
    ],
  },
];

export function pathBySlug(slug: string) {
  return paths.find((p) => p.slug === slug);
}
