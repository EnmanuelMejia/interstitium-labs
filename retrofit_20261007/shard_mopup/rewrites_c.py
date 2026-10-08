# Shard C instructor-voice rewrites. Key: (path_id, module_id) -> new il_provides blurb.
RW_C = {
# ---------- il09-comptia-core ----------
("il09-comptia-core", "aplus-v15"):
"I'm your instructor for this module. In this module I teach PBQ drills and the troubleshooting methodology from genuine exam-day experience — the platform owner holds A+ CE (earned 4/30/2024, valid through 4/30/2027) and completed a nonprofit tech-training program's A+ training. By the end you'll own Core 1's hardware, networking, and troubleshooting and Core 2's OS, security, and operational procedures — plus honest exam-day logistics.",
("il09-comptia-core", "networkplus-n10009"):
"I'm your instructor for this module. In this module I cross-link you to IL-04's networking path — one networking discipline — because this module is the exam-prep layer over it. By the end you'll be ready across the N10-009 domains: networking concepts, implementation, operations, security, and troubleshooting, with the readiness gate passed.",
("il09-comptia-core", "securityplus-sy0701"):
"I'm your instructor for this module. In this module I build the V7/V8 transition bridge: what changes, what carries over, and a readiness gate that tracks both versions honestly. By the end you'll cover general security concepts, threats and mitigations, and architecture, operations, and program management — ready whichever version you book.",
("il09-comptia-core", "stackable-core"):
"I'm your instructor for this module. In this module I give you the stacking planner: which combinations earn which stackables, and the order that minimizes exam spend. By the end you'll have the infrastructure and cybersecurity pathway mapped — A+ plus Network+ for CIOS, all three for CSIS — as a sequenced plan, not a guess.",
# ---------- il09-comptia-security ----------
("il09-comptia-security", "cysa-cs0004"):
"I'm your instructor for this module. In this module I run SOC-scenario labs mapped to the CySA+ domains — cross-linked to IL-06's defensive path, which is the hands-on home. By the end you'll be ready across security operations, vulnerability management, and incident response — exam prep here, the craft where you practice it.",
("il09-comptia-security", "pentest-pt0003"):
"I'm your instructor for this module. In this module I build the methodology bridge to IL-06's offensive path: this module is the exam-prep layer, the hacking is taught in IL-06. By the end you'll be ready across engagement management, recon and enumeration, attacks and exploits, and post-exploitation — with the methodology to back every answer.",
("il09-comptia-security", "securityx-cas005"):
"I'm your instructor for this module. In this module I run architecture-scenario exercises at the expert level: you design, then you defend the design. By the end you'll reason across GRC, security architecture, security engineering, and security operations — ready for a pass/fail exam that rewards judgment.",
("il09-comptia-security", "stackable-security"):
"I'm your instructor for this module. In this module I give you the multi-year planner: the cybersecurity pathway as a sequenced campaign, not a pile of exams. By the end you'll have the expert stackables — CSAP, CNVP, CNSP, CSAE, CSIE — mapped as a campaign with each credential building on the last.",
# ---------- il09-comptia-data-cloud ----------
("il09-comptia-data-cloud", "cloudplus-cv0004"):
"I'm your instructor for this module. In this module I build the cloud-operations bridge to IL-05: this module preps the exam, IL-05 teaches the craft. By the end you'll be ready across cloud architecture, deployment, operations, security, DevOps fundamentals, and troubleshooting — the Cloud+ map, covered honestly.",
("il09-comptia-data-cloud", "linuxplus-xk0006"):
"I'm your instructor for this module. In this module I cross-link you to IL-04's Linux path — one Linux discipline — with the V7-to-V8 changes called out. By the end you'll be ready across system management, services and user management, security, automation, and troubleshooting at the XK0-006 level.",
("il09-comptia-data-cloud", "serverplus-sk0005"):
"I'm your instructor for this module. In this module I run hardware-lifecycle scenarios and disaster-recovery drills — the physical layer most cloud learners never touch. By the end you'll handle server hardware installation, administration, security, and disaster recovery with the hands-on mindset the exam rewards.",
("il09-comptia-data-cloud", "dataplus-da0002"):
"I'm your instructor for this module. In this module I build the analyst-skills bridge to IL-07: exam prep here, the craft in the data-school spine. By the end you'll be ready across data concepts, acquisition and preparation, analysis, visualization, and governance.",
("il09-comptia-data-cloud", "datasys-ds0001"):
"I'm your instructor for this module. In this module I give you the V1/V2 transition map: what carries over, what's new, and which version to book. By the end you'll know the DS0-001 domains and the V2 changes — including the new Data Integration domain — and you'll book the right version with confidence.",
("il09-comptia-data-cloud", "dataai-dy0001"):
"I'm your instructor for this module. In this module I run the math-readiness audit against IL-02's probability and statistics nodes — because the exam assumes mathematical maturity, and I verify it. By the end you'll be ready across math and statistics, modeling and analysis, machine learning, and operations for this pass/fail exam.",
("il09-comptia-data-cloud", "project-tech-plus"):
"I'm your instructor for this module. In this module I build the true-beginner on-ramp: Tech+ as the first credential for the learner starting from zero, honestly positioned. By the end you'll know the Project+ V5 domains and Tech+'s eleven curriculum topics — and exactly where each fits in your sequence.",
("il09-comptia-data-cloud", "cloudnetx-cnx001"):
"I'm your instructor for this module. In this module I run the expert hybrid-cloud networking scenarios — architecture design exercises at the level the exam demands. By the end you'll reason about network architecture design, network security, and operations and troubleshooting at the expert, pass/fail level.",
# ---------- il09-vendor-ai ----------
("il09-vendor-ai", "anthropic-claude-certs"):
"I'm your instructor for this module. In this module I map preparation to the reported domains with the gate stated plainly: a partner-company email is required, and I say so before you invest. By the end you'll understand the Associate, Developer, and Architect tiers — and what you can and can't pursue from where you stand.",
("il09-vendor-ai", "openai-program-track"):
"I'm your instructor for this module. In this module I maintain the tracked-program page: what exists, what's pilot-only, and the preparation that transfers whenever the program opens. By the end you'll know the AI Foundations pilot and the full credential pilot for what they are — and I never imply a bookable exam that doesn't exist.",
("il09-vendor-ai", "nvidia-databricks"):
"I'm your instructor for this module. In this module I prepare you with the honesty label attached: domains from corroborated sources, never presented as vendor-published fact. By the end you'll be ready for NCA-GENL and the Databricks Generative AI Engineer Associate — with every claim's provenance visible.",
("il09-vendor-ai", "microsoft-azure-ai"):
"I'm your instructor for this module. In this module I run hands-on Azure AI labs mapped to the reported domains — with Microsoft Learn as the cited source of truth for every exam-day fact. By the end you'll be ready for AI-901 and AI-103, and you'll know where the single authoritative source for each fact lives.",
("il09-vendor-ai", "google-cloud-ai"):
"I'm your instructor for this module. In this module I keep the two credentials distinct: the Leader exam is strategic, the PMLE is technical, and preparation differs accordingly. By the end you'll be ready for the Generative AI Leader and the Professional Machine Learning Engineer exams — each on its own terms, with Vertex AI and Model Garden where they belong.",
("il09-vendor-ai", "aws-ai-ml"):
"I'm your instructor for this module. In this module I keep the retirement-aware map: MLA-C01's last day and MLS-C01's retirement are recorded, so you never prepare for a dead exam. By the end you'll be ready for AIF-C01 and MLA-C02 — with Bedrock and the GenAI additions — studying the exams that actually exist.",
# ---------- il09-oracle ----------
("il09-oracle", "java-se21"):
"I'm your instructor for this module. In this module I run the objective-by-objective readiness dashboard with coding drills per topic — cross-linked to IL-03's Java module, which is the learning home. By the end you'll be ready for the 1Z0-830: streams, lambdas, modules, concurrency including virtual threads, I/O, localization, and generics — 50 questions, 120 minutes, 68% to pass.",
("il09-oracle", "oracle-sql"):
"I'm your instructor for this module. In this module I give you the SQL query gym shared with IL-03's databases module — one query discipline, examined through Oracle's lens here. By the end you'll write queries, joins, and subqueries and handle DDL and DML at the 1Z0-071 level — 63 questions, 120 minutes, 63% to pass.",
("il09-oracle", "oci-foundations"):
"I'm your instructor for this module. In this module I run the free-exam fast track: the one Oracle exam with no fee becomes your first cloud credential, honestly positioned. By the end you'll know core services, security, and governance at the 1Z0-1085-26 level — 40 questions, 60 minutes, 65% to pass — and how the year-versioned program works.",
("il09-oracle", "oci-professional"):
"I'm your instructor for this module. In this module I build the professional-track planner with the versioning caveat: 2025-to-2026 transitions tracked, unverified details never asserted. By the end you'll have the Architect Associate and the Developer, DevOps, Networking, and Security Professional tracks mapped — and you'll know exactly which claims I verified and which I didn't.",
# ---------- il09-lf-blockchain ----------
("il09-lf-blockchain", "hfcp-prep"):
"I'm your instructor for this module. In this module I add the performance-lab layer the multiple-choice exam doesn't test: chaincode written, deployed, and debugged — because the coverage guarantee rests on labs here. By the end you'll be ready across Fabric networks, smart contracts, and client apps for the 90-minute proctored HFCP — with real chaincode under your belt.",
("il09-lf-blockchain", "bcp-prep"):
"I'm your instructor for this module. In this module I run Besu network labs: you run nodes, because a multiple-choice exam about networks deserves hands-on networks. By the end you'll be ready across networking, core concepts, permissioning, privacy, and consensus for the 90-minute proctored BCP — valid two years, two attempts included.",
("il09-lf-blockchain", "retired-blockchain"):
"I'm your instructor for this module. In this module I teach the negative curriculum: what the platform deliberately does not teach, so you never prepare for a dead exam. By the end you'll know the retired set — LFS272/LFD272, the CHFA/CHFD/CHSA performance exams, Sawtooth — and you'll steer clear with confidence.",
# ---------- il09-cpp-python ----------
("il09-cpp-python", "cpp-track"):
"I'm your instructor for this module. In this module I build the exam-prep layer over IL-03's C++ modules: the learning lives in IL-03, the certification targeting lives here. By the end you'll be ready from CPE-20-01 entry through CPA-21-02 associate to CPP-22-02 professional — plus the C branch: CLE, CLA, CLP.",
("il09-cpp-python", "python-track"):
"I'm your instructor for this module. In this module I track the delivery-channel caveat: OpenEDG's move off Pearson VUE is watched, and booking guidance is re-verified before it's published. By the end you'll be ready from PCEP entry through PCAP-31-03 associate to PCPP1 and PCPP2 professional — and you'll book through a channel I've actually confirmed.",
# ---------- il10-fde-career ----------
("il10-fde-career", "fde-career-arc"):
"I'm your instructor for this module. In this module I run the career-stage self-assessment: you locate yourself on the arc, and I sequence the platform accordingly. By the end you'll see the full arc — Discover the problem, Model and Prove the technical core, Integrate and Operate inside the customer, Generalize from engagement to product — and know where you stand on it.",
("il10-fde-career", "jobright-outcome-layer"):
"I'm your instructor for this module. In this module I wire the outcome layer itself: your verified skills from every academy flow into the job search as evidence, and outcomes flow back as plan adjustments. By the end you'll have AI-matched applications, tracking against skills earned, and a feedback loop where outcomes refine the plan.",
("il10-fde-career", "interview-systems"):
"I'm your instructor for this module. In this module I run mock interviews with a rubric: system design, coding, and the customer-facing story, each scored separately. By the end you'll handle technical interviews, system design rounds, behavioral interviews with the FDE story, and offer evaluation — practiced, not just read about.",
# ---------- il10-humanmetrics ----------
("il10-humanmetrics", "typology-assessment"):
"I'm your instructor for this module. In this module I give you the interpretation guide: I treat the result as one input among many, never as a verdict, with the instrument's limits stated. By the end you'll understand the Jung typology instrument — the sixteen types as working styles — and exactly what it measures and what it doesn't.",
("il10-humanmetrics", "career-fit-mapping"):
"I'm your instructor for this module. In this module I build the fit map: your type against the university's career paths, as hypotheses to test through the work itself. By the end you'll have type-to-role-family mapping, working-style implications, team composition thinking, and a development plan — all held as working hypotheses, not verdicts.",
# ---------- il10-entrepreneurship ----------
("il10-entrepreneurship", "babson-curriculum-map"):
"I'm your instructor for this module. In this module I run the founder's curriculum audit: which business foundations the technical learner lacks, sequenced as a reading and practice plan. By the end you'll see the Babson structure — majors and minors, entrepreneurship as a discipline, finance, marketing, and operations foundations — mapped against your own gaps.",
("il10-entrepreneurship", "venture-building"):
"I'm your instructor for this module. In this module I give you the venture workbook: original canvases and unit-economics exercises, with Interstitium Labs itself as the worked example. By the end you'll practice problem discovery, the MVP discipline, unit economics, and fundraising literacy — with a real venture's numbers in front of you.",
("il10-entrepreneurship", "academy-sf-study"):
"I'm your instructor for this module. In this module I deliver the competitive study: what a well-funded contemporary academy does right, analyzed without hype and without imitation. By the end you'll understand practitioner-led education, the AI and founder curriculum, and hiring-partner integration — and you'll know what to borrow and what to avoid.",
# ---------- il10-quant-finance ----------
("il10-quant-finance", "undergrad-quant-prep"):
"I'm your instructor for this module. In this module I run the prerequisite audit against IL-02's quant-math path: I verify the mathematics before you apply. By the end you'll have probability and statistics at depth, programming for quant, and the internship map — with the math prerequisite honestly confirmed.",
("il10-quant-finance", "micromasters-finance"):
"I'm your instructor for this module. In this module I give you the preparation map per MicroMasters course, with readiness gates. By the end you'll be ready for the graduate-level finance courses and the proctored comprehensive exam — and I'll remind you plainly: the credential is MITx's, never implying endorsement.",
("il10-quant-finance", "phd-quant-consulting"):
"I'm your instructor for this module. In this module I give you the honest fork analysis: what each branch actually demands, in mathematics and in years — so you choose with eyes open. By the end you'll understand the research-level mathematics, stochastic calculus, and consulting case interviews, and you'll see the career fork clearly: desk quant, researcher, or consultant.",
}
