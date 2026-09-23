export type RoadCheck = { q: string; choices: string[]; answer: number; why: string };
export type RoadModule = { name: string; units: string[]; check: RoadCheck };
export type Road = {
  id: string;
  vendor: string;
  title: string;
  catalog: { label: string; href: string };
  note: string;
  modules: RoadModule[];
};

const check = (q: string, choices: string[], why: string): RoadCheck => ({ q, choices, answer: 0, why });

export const roads: Road[] = [
  {
    id: "microsoft",
    vendor: "Microsoft",
    title: "Microsoft credentials",
    catalog: { label: "Microsoft Learn credentials", href: "https://learn.microsoft.com/credentials/" },
    note: "Learn’s shape: a path, then modules, then a unit, then a check. The checks here are ours. Their exams stay on their site.",
    modules: [
      { name: "Role", units: ["Pick one role: administrator, developer, or data. A credential is for that role, not for the whole cloud.", "Read the skills measured page before any video."], check: check("A Microsoft credential is scoped to", ["a role and a skills-measured list", "every Azure service", "a calendar month", "an IDE license"], "The skills list is the contract. The rest is marketing.") },
      { name: "Module", units: ["A module is a cluster of units with one outcome.", "Finish the unit before the knowledge check. The check is not the unit."], check: check("In this flow, a knowledge check comes", ["after the unit, and does not replace the manual", "instead of the documentation", "on a due date", "only if you pay"], "The check tells you whether the unit landed.") },
      { name: "Azure data", units: ["Azure SQL is a managed database. You still own the schema, the identity, and the backup test.", "The product name on the exam and the product you deployed must be the same one."], check: check("Who owns the schema on Azure SQL?", ["You do", "The hypervisor", "The IDE", "The certification voucher"], "Managed does not mean they designed your tables.") },
    ],
  },
  {
    id: "aws",
    vendor: "AWS",
    title: "AWS certification",
    catalog: { label: "AWS Certification", href: "https://aws.amazon.com/certification/" },
    note: "Foundational, associate, professional. The exam is theirs. The order of work is: network, identity, then the log.",
    modules: [
      { name: "Foundational", units: ["Shared responsibility: they run the hypervisor, you run the guest, the data, and IAM.", "Price the design before you build it. Data transfer is a line item."], check: check("Under the shared-responsibility split, IAM is", ["yours", "the hypervisor’s", "optional at associate level", "a property of the region"], "Identity is on your side of the line.") },
      { name: "Associate", units: ["A deny you cannot see is often a boundary or an organization policy, not the inline policy you just edited.", "A security group, a route table, and a network ACL are three different nos."], check: check("The first network no to check is", ["the route, then the security group, then the ACL", "the ACL only", "the IDE theme", "the exam voucher"], "Order keeps you from editing the wrong no.") },
      { name: "Professional", units: ["A professional design names the failure and the monthly number.", "Multi-account is a boundary, not a folder."], check: check("A design you cannot price is", ["not finished", "professional by default", "cheaper", "out of scope for IAM"], "The number is part of the architecture.") },
    ],
  },
  {
    id: "google",
    vendor: "Google Cloud",
    title: "Google Cloud certification",
    catalog: { label: "Google Cloud certification", href: "https://cloud.google.com/learn/certification" },
    note: "Same shape as the others: role, then the skills outline on their site, then our check.",
    modules: [
      { name: "Project", units: ["A project is the boundary for identity and billing. A folder is not a security control by itself.", "Enable the API you mean to call. A client library does not enable it."], check: check("A Google Cloud project primarily bounds", ["identity and billing", "the Vim mode", "a single SQL row", "the JDK vendor"], "Resources live in a project. The bill does too.") },
      { name: "IAM", units: ["A role is a bag of permissions. Bind it to a principal on a resource.", "Basic roles are broad. A predefined or custom role is the one you can explain."], check: check("Binding a role means", ["a principal gets that role on a resource", "the role is deleted", "the project is public", "billing stops"], "The binding is the grant.") },
      { name: "Data", units: ["BigQuery and Cloud SQL are different engines. Do not study one and sit the exam for the other.", "A dataset’s location is a decision, not a default you notice later."], check: check("Cloud SQL and BigQuery are", ["different engines", "two names for the same service", "both a JVM", "IDEs"], "The manual you need is the one for the engine you run.") },
    ],
  },
  {
    id: "oracle-db",
    vendor: "Oracle",
    title: "Oracle Database",
    catalog: { label: "Oracle Database training", href: "https://education.oracle.com/oracle-database" },
    note: "Associate toward architect is their ladder. We do not store their items. SQL practice is the bench.",
    modules: [
      { name: "SQL", units: ["Say the grain of the row before you write the join.", "WHERE filters rows. HAVING filters groups. Mixing them up changes the answer."], check: check("HAVING applies to", ["groups", "individual rows before grouping", "the JDK", "the editor theme"], "GROUP BY first, HAVING second.") },
      { name: "Administration", units: ["A backup you have not restored is a hope.", "Users, roles, and privileges are three objects."], check: check("A backup counts when", ["you have restored it", "the job exited zero once", "it is on the same disk only", "the exam is booked"], "Restore is the test.") },
      { name: "Architecture", units: ["Instance and database are not synonyms.", "An architect names the recovery point, not only the product."], check: check("Recovery point objective is", ["how much data you can afford to lose", "the IDE you bought", "a certification level", "the number of indexes"], "RPO is a business number implemented by a technical one.") },
    ],
  },
  {
    id: "vertica",
    vendor: "Vertica",
    title: "Vertica",
    catalog: { label: "Vertica learning paths", href: "https://www.opentext.com/learning-services/learning-paths-vertica" },
    note: "OpenText runs the Vertica exams now, including the analyst exam on projection design. Their items are not here.",
    modules: [
      { name: "Essentials", units: ["Vertica stores columns, and a projection is the physical design, not a SELECT alias.", "Load, query, and user administration are the essentials course. Take their outline, not a rumor."], check: check("A Vertica projection is", ["a physical design for how data sits on disk", "only a SELECT alias", "a JVM flag", "an editor plugin"], "Projections are why the query is fast or not.") },
      { name: "Plans", units: ["Read the plan before you add a projection.", "The designer can propose a design. You still have to read it."], check: check("Before a new projection, read", ["the query plan", "a meme", "the Vim cheatsheet", "the voucher"], "The plan says which projection the query used.") },
      { name: "Analyst", units: ["The analyst exam is about reading and writing projection designs for specific queries.", "That exam is theirs, timed, and paid. This module is the vocabulary."], check: check("The Vertica analyst exam is offered by", ["OpenText, not by this page", "the bench editor", "CompTIA", "HashiCorp"], "We link the catalog. We do not give the exam.") },
    ],
  },
  {
    id: "wolfram",
    vendor: "Wolfram",
    title: "Mathematica",
    catalog: { label: "Wolfram certifications", href: "https://www.wolfram.com/wolfram-u/certifications/" },
    note: "Level 1 is their proficiency exam in Mathematica and the Wolfram Language. The reference is the function page.",
    modules: [
      { name: "Language", units: ["Every built-in has a reference page. The examples on that page are the lesson.", "A notebook is not a substitute for naming the function you used."], check: check("The authority for a Wolfram function is", ["its reference page", "a forum reply with no version", "the editor font", "a certification voucher alone"], "The reference names the arguments.") },
      { name: "Level 1", units: ["Level 1 covers fundamental and further Mathematica use. Wolfram sets the passing mark.", "Do not confuse an attendance certificate with Level 1."], check: check("An attendance certificate means", ["you were present, not that you passed Level 1", "you are an architect", "the kernel is yours to redistribute", "you finished every certification"], "Wolfram publishes the levels separately.") },
      { name: "Level 2", units: ["Level 2 is a further credential on their site. Read its outline there.", "Computation you cannot replay is not a result."], check: check("A result in Mathematica is done when", ["someone else can replay the notebook", "the plot looks finished", "the exam timer starts", "the font is large"], "Replay is the standard.") },
    ],
  },
  {
    id: "security",
    vendor: "Security",
    title: "Cybersecurity credentials",
    catalog: { label: "CompTIA certifications", href: "https://www.comptia.org/certifications" },
    note: "CompTIA is the broad ladder. The work in this app is the detection spine. Vendor items are not stored.",
    modules: [
      { name: "CompTIA", units: ["A+ , Network+, Security+, then the specialty you can defend. Their site has the current codes.", "A cert is a vocabulary check. A detection still needs a log source."], check: check("Security+ does not replace", ["a log source and a hypothesis", "the need to read", "a manual", "a baseline"], "The credential names the topics. The detection names the log.") },
      { name: "Operations", units: ["Blue team work is a hypothesis, a source, and a false-positive story.", "A score does not isolate a host."], check: check("A detection without a log source is", ["not a detection", "a SIEM", "a certification", "an IDE"], "No source, no page.") },
      { name: "Spine", units: ["The nine-part sequence in this app is self-paced and has no exam bank.", "The capstone is a threshold you would page on."], check: check("The capstone is cleared by", ["a threshold you can defend", "a purchased dump", "a due date", "an editor theme"], "The bench records the pass.") },
    ],
  },
  {
    id: "linux",
    vendor: "Linux",
    title: "Linux Foundation and Red Hat",
    catalog: { label: "Linux Foundation certification", href: "https://training.linuxfoundation.org/certification/" },
    note: "LFCS and the RHCSA are different exams on different systems. Read the one you are sitting.",
    modules: [
      { name: "Essentials", units: ["Permissions, processes, and the journal. 777 is not a finish.", "The manual for a command is the man page, then the info page if the command says so."], check: check("The first manual for a Unix command is", ["the man page", "a video with no version", "the IDE tooltip only", "a meme"], "man is the contract for that binary.") },
      { name: "Linux Foundation", units: ["Their certification catalog lists the current performance-based exams.", "A performance exam means you do the task, you do not only recognize it."], check: check("A performance-based Linux exam asks you to", ["do the task on a system", "recognize a screenshot only", "name an IDE", "pay and skip the lab"], "The system is the test.") },
      { name: "Red Hat", units: ["RHCSA is sat on Red Hat’s systems. Enable and start are different.", "The spine in this app is boot, users, and units."], check: check("systemctl enable differs from start because", ["enable survives reboot", "start edits the unit file", "enable reboots immediately", "they are aliases"], "Enable is the next boot. Start is now.") },
    ],
  },
  {
    id: "hashicorp",
    vendor: "HashiCorp",
    title: "Terraform and HashiCorp",
    catalog: { label: "HashiCorp certifications", href: "https://developer.hashicorp.com/certifications" },
    note: "Terraform is one product in their catalog. Vault, Consul, and the others have their own docs. Do not collapse them.",
    modules: [
      { name: "Plan", units: ["Read the plan. A destroy on a stateful resource is a stop.", "State is a secret and a lock."], check: check("Two applies without a lock can", ["corrupt state", "speed the plan", "replace the provider docs", "set a deadline"], "The lock is why the plan stays true.") },
      { name: "Terraform", units: ["The provider manual is the resource schema. The tutorial is not the schema.", "Drift is a change the plan did not ask for."], check: check("Drift means", ["the live system left the plan", "the exam expired", "the IDE crashed", "state is public"], "Git, or the plan, is the desired state.") },
      { name: "Other products", units: ["Vault is secrets. Consul is service discovery. They are not Terraform with a different logo.", "Open the product manual for the binary you are running."], check: check("Vault’s manual is the authority when you are", ["running Vault", "writing a Terraform resource for a VPC only", "editing Vim", "sitting a CompTIA exam"], "Match the manual to the binary.") },
    ],
  },
  {
    id: "kubernetes",
    vendor: "CNCF",
    title: "Kubernetes",
    catalog: { label: "CNCF certifications", href: "https://www.cncf.io/training/certification/" },
    note: "CKA is the administration exam. CKAD and CKS are different exams. The objects are the same language.",
    modules: [
      { name: "Objects", units: ["Pod, Deployment, Service, Ingress, ConfigMap, Secret. Know which one holds the desired count.", "A Secret in a manifest you committed is a leak."], check: check("The desired replica count lives on the", ["Deployment", "Service", "ConfigMap", "editor"], "The Service only selects pods.") },
      { name: "Debug", units: ["Describe, logs, events, then exec.", "Guessing at YAML before events wastes the clock you set yourself."], check: check("The first debugging command after a pod is not Ready is", ["describe, and read events", "delete the namespace", "change the editor", "scale to zero and go home"], "Events usually name the failure.") },
      { name: "Exams", units: ["CKA, CKAD, and CKS have different outlines on the CNCF page.", "The exceed bar here is explaining the scheduling decision."], check: check("CKS is", ["the security specialist exam, not the admin exam", "an alias of CKA", "a HashiCorp exam", "a SQL exam"], "Read the outline for the letters you are sitting.") },
    ],
  },
  {
    id: "ai",
    vendor: "Research",
    title: "Models, diffusion, and retrieval",
    catalog: { label: "Attention is all you need", href: "https://arxiv.org/abs/1706.03762" },
    note: "These are papers and docs, not a certification. No deadline, and no claim that a vendor exam covers them.",
    modules: [
      { name: "Transformers", units: ["The 2017 attention paper is the citation for the architecture, not a blog summary.", "Self-attention mixes tokens. It does not by itself give you a database."], check: check("The transformer citation we use is", ["Vaswani and coauthors, 2017", "a certification blueprint", "the Vim manual", "a price chart"], "The paper is the source.") },
      { name: "Diffusion", units: ["Denoising diffusion learns to reverse a noise process. Ho, Jain, and Abbeel, 2020, is the citation.", "A sampler step is not a training step. Know which one you are running."], check: check("A diffusion model is trained to", ["reverse a noise process", "store a SQL table", "replace IAM", "sign a ledger transaction"], "The paper’s abstract is enough to refuse a wrong slogan.") },
      { name: "RAG", units: ["Retrieval-augmented generation fetches passages and then conditions the generator. Lewis and coauthors, 2020.", "If the passage is wrong, the fluent answer is still wrong. Cite the passage or do not claim it."], check: check("RAG fails open when", ["the retrieved passage is irrelevant and the model answers anyway", "the index is cited", "you refuse without a source", "the manual is open"], "Retrieval is only useful if the reader can see it.") },
    ],
  },
  {
    id: "chain",
    vendor: "Ledgers",
    title: "Bitcoin, Ethereum, and the XRP Ledger",
    catalog: { label: "XRPL docs", href: "https://xrpl.org/docs.html" },
    note: "Protocol development. Not price talk, not a trading desk, and not an exploit lab.",
    modules: [
      { name: "Bitcoin", units: ["Read the paper. A transaction spends previous outputs under a locking script.", "The client manual for the node you run is the second book."], check: check("A Bitcoin transaction spends", ["previous outputs", "an account balance stored like a bank row", "an IDE buffer", "a Kubernetes secret"], "The UTXO set is the state.") },
      { name: "Ethereum", units: ["Accounts, transactions, and the EVM are documented on ethereum.org.", "A contract you cannot verify on a block explorer build is a blob."], check: check("The authority for Ethereum application development here is", ["ethereum.org/developers", "a price feed", "the RHCSA outline", "a meme"], "The docs name the transaction fields.") },
      { name: "XRPL", units: ["The XRP Ledger docs describe accounts, transactions, and the consensus protocol.", "A library is not the ledger. Read the transaction type you are submitting."], check: check("Before submitting an XRPL transaction, read", ["that transaction type’s doc", "a candlestick chart", "the Vim tutorial", "a certification dump"], "The field you omit is the bug.") },
    ],
  },
];

export const roadVendors = ["All", ...new Set(roads.map((road) => road.vendor))];
