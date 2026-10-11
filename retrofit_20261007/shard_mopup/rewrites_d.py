# Shard D instructor-voice rewrites (no prefix bug; same rewrite treatment).
# Key: (path_id, module_id) -> new il_provides blurb.
RW_D = {
# ---------- il06-azure-soc ----------
("il06-azure-soc", "sc200-soc-env"):
"I'm your instructor for this module. In this module I hand you a SOC lab: connect data sources, write analytics rules, and map every alert to ATT&CK — the environment you'd actually work in. By the end you'll run the security operations environment across the Defender XDR unified portal and Sentinel — workspaces, data connectors, ingestion, and automation playbooks — the exam's largest domain, at 40–45% weight.",
("il06-azure-soc", "sc200-ir"):
"I'm your instructor for this module. In this module I run an IR lab: a simulated compromise, the investigation timeline you build, and the containment actions you take. By the end you'll investigate incidents across Defender XDR and Endpoint, M365 and Purview, enrich with Microsoft Graph, and use Security Copilot as an assistant — not a crutch.",
("il06-azure-soc", "sc200-hunt"):
"I'm your instructor for this module. In this module I run hunting drills: given a hypothesis and a dataset, you write the KQL that proves or kills it. By the end you'll hunt deeply in KQL — hypotheses first, queries second — and repeat your hunts in notebooks so they survive contact with the next incident.",
("il06-azure-soc", "sc200-live-hunt"):
"I'm your instructor for this module. In this module I set the live-hunt capstone: a multi-stage attack scenario, no new tools — synthesis only. By the end you'll have run the full hunt: detect the intrusion, scope it, contain it, and write the incident report a CISO would read.",
("il06-azure-soc", "sc200-exam-prep"):
"I'm your instructor for this module. In this module I run KQL-reading drills — read the query first — and triage scenarios, with readiness tracked per the three exam domains. By the end you'll navigate the portal fluently, prioritize incident triage the way the exam rewards, and walk into booking and exam-day logistics with nothing left to chance.",
# ---------- il11-entra-identity ----------
("il11-entra-identity", "sc300-lifecycle"):
"I'm your instructor for this module. In this module I hand you a lifecycle lab: joiner-mover-leaver automation with access packages — the audit trail writes itself. By the end you'll treat the identity lifecycle as a security boundary: users, groups, devices, applications, and resources, with HR-driven and API-driven provisioning and B2B collaboration done right.",
("il11-entra-identity", "sc300-zerotrust-ca"):
"I'm your instructor for this module. In this module I set a CA lab: build the policy set for a real org, then attack it from a non-compliant device and watch it hold. By the end you'll apply the Zero Trust principles through Conditional Access — signals and controls, named locations, device compliance, risk — and you'll know exactly what breaks when CA is misconfigured.",
("il11-entra-identity", "sc300-auth"):
"I'm your instructor for this module. In this module I run an auth lab: register an app, configure OIDC, and trace the token flow — protocols demystified by doing. By the end you'll compare MFA methods and phishing-resistant auth, deploy passwordless with FIDO2, Windows Hello, and Authenticator, and read the OAuth2/OIDC/SAML protocols underneath.",
("il11-entra-identity", "sc300-hybrid"):
"I'm your instructor for this module. In this module I build the bridge: the on-prem AD from il11-active-directory-defense, extended to Entra. By the end you'll choose between Entra Connect Sync and Cloud Sync, compare pass-through, hash sync, and federation, and run seamless SSO and writeback across the hybrid boundary.",
("il11-entra-identity", "sc300-governance"):
"I'm your instructor for this module. In this module I run a governance lab: run an access review that actually revokes, and activate a PIM role with justification. By the end you'll practice identity governance as continuous hygiene — access reviews, entitlement management, Privileged Identity Management, terms of use, and identity protection.",
("il11-entra-identity", "sc300-troubleshoot"):
"I'm your instructor for this module. In this module I run troubleshooting drills: broken sign-ins with real logs — you diagnose from evidence, not guesses. By the end you'll read sign-in log failures, drive identity operations with PowerShell and Graph, query Entra sign-in data in KQL, and follow a troubleshooting methodology that holds under pressure.",
("il11-entra-identity", "sc300-exam-prep"):
"I'm your instructor for this module. In this module I run policy-reading and scenario drills — readiness across the SC-300 topics, with the identity lifecycle cue trained into every scenario question. By the end you'll read Conditional Access policies fluently, work both PowerShell and the portal, and handle booking and exam-day logistics like a formality.",
# ---------- il07-aws-data ----------
("il07-aws-data", "dea-ingest"):
"I'm your instructor for this module. In this module I hand you a pipeline lab: the same dataset ingested batch and streaming — compare latency, cost, and complexity honestly. By the end you'll make the batch-versus-streaming decision the real way, working Kinesis streams, Firehose, and analytics alongside Glue crawlers, jobs, and DataBrew — the exam's largest domain at 34%.",
("il07-aws-data", "dea-stores"):
"I'm your instructor for this module. In this module I run a storage lab: partition a dataset three ways and measure what each costs to query. By the end you'll lay out S3 as the lake — layout, partitioning, formats — tune Redshift distribution and sort keys, and place operational data in DynamoDB and RDS where each belongs.",
("il07-aws-data", "dea-ops"):
"I'm your instructor for this module. In this module I run an ops lab: break a pipeline's schema on purpose and watch the contract tests catch it. By the end you'll orchestrate with Step Functions, MWAA, and EventBridge, monitor pipelines and alert on what matters, and evolve schemas without breaking consumers.",
("il07-aws-data", "dea-security"):
"I'm your instructor for this module. In this module I run a governance lab: column-level access in Lake Formation — prove the analyst can't see the PII. By the end you'll enforce fine-grained access, encrypt with KMS across the pipeline, and handle PII with real data classification.",
("il07-aws-data", "dea-lineage"):
"I'm your instructor for this module. In this module I set the audit: pick one dashboard number and trace it to the source record, documenting every transform. By the end you'll own end-to-end lineage from source to dashboard, gate on data-quality checks, and trace one record's journey — no new services, synthesis only.",
("il07-aws-data", "dea-exam-prep"):
"I'm your instructor for this module. In this module I run workload-cue drills: every question starts from the data's shape and velocity. By the end you'll select services from the workload cue, drill deepest into the 34% ingestion domain, and walk into booking and exam-day logistics with hands-on console familiarity behind you.",
# ---------- il07-aws-ml ----------
("il07-aws-ml", "mla-foundations"):
"I'm your instructor for this module. In this module I run a foundations lab: classify ten workloads as ML versus GenAI versus rules — precision with the vocabulary first. By the end you'll own the AI/ML/GenAI vocabulary precisely, survey the AWS AI managed services, and understand responsible AI as the exam's ethics layer — the foundation before associate depth.",
("il07-aws-ml", "mla-framing"):
"I'm your instructor for this module. In this module I run a framing workshop: three business problems translated to ML formulations, with the metric chosen first. By the end you'll translate business problems into ML problems, choose the problem type — classification, regression, forecasting — define success metrics before modeling, and avoid the framing mistakes that waste months.",
("il07-aws-ml", "mla-data"):
"I'm your instructor for this module. In this module I run a data lab: build a feature pipeline, then find the leakage planted in it — the skill that matters. By the end you'll engineer and select features, split training, validation, and test sets correctly, work Data Wrangler and Feature Store, and treat leakage as the silent killer it is.",
("il07-aws-ml", "mla-model"):
"I'm your instructor for this module. In this module I run a modeling lab: tune a model with a budget — every experiment logged, every dollar accounted. By the end you'll run SageMaker training jobs and algorithms, tune hyperparameters the disciplined way, reach for Bedrock on foundation-model tasks, and keep experiment tracking that survives audit.",
("il07-aws-ml", "mla-deploy"):
"I'm your instructor for this module. In this module I run a deployment lab: ship an endpoint, detect drift with Model Monitor, and roll back — the full loop. By the end you'll choose between real-time, batch, and serverless SageMaker endpoints, run CI/CD for ML with the pipeline differences understood, and roll back when the model degrades.",
("il07-aws-ml", "mla-cost"):
"I'm your instructor for this module. In this module I run a cost lab: serve 1M inferences three ways and price each — the cheapest correct answer wins. By the end you'll price the inference path end to end, select instances for serving, understand the batch-versus-real-time cost cliff, and treat the bill as a design constraint.",
("il07-aws-ml", "mla-exam-prep"):
"I'm your instructor for this module. In this module I run two-tier prep: foundations exam first, then associate depth. By the end you'll read the SageMaker service cue in scenario questions, study MLA-C02 — not the retired MLA-C01, retired 2026-09-28 — and confirm domain weights against the live exam guide at study time, not memorize them here.",
}
