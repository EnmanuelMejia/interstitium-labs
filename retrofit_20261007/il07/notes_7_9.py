# Module notes data, part 3: modules 7-9 (frontier, aws-data, aws-ml)

NOTES = {}

NOTES["il07-frontier"] = [
("Concepts",
"- **Scaled dot-product attention** \u2014 Attention(Q,K,V) = softmax(QK\u1d40/\u221ad_k)V.\n"
"- **\u221ad_k scaling** \u2014 the whole trick's bodyguard: without it, dot products grow with dimension, softmax saturates, gradients die \u2014 variance control for the softmax.\n"
"- **Multi-head attention** \u2014 different heads learn different relations (positional, syntactic, rare-word): specialization emerges.\n"
"- **Head visualization** \u2014 some heads are interpretable, most aren't: honesty about interpretability.\n"
"- **Causal masking** \u2014 the future is kept out of the past: the triangular mask that makes autoregression honest.\n"
"- **RLHF** \u2014 the InstructGPT three-stage recipe: SFT (imitate demonstrations) \u2192 reward model (learn preferences from comparisons) \u2192 PPO with KL penalty (optimize without drifting).\n"
"- **KL penalty** \u2014 the leash: optimize reward without forgetting the SFT policy.\n"
"- **DPO and beyond** \u2014 direct preference optimization skips the reward model: simpler, with its own trade-offs (offline, no exploration).\n"
"- **DPO vs PPO** \u2014 simplicity vs online exploration: pick by your data regime.\n"
"- **Scaling laws** \u2014 loss follows power laws in compute, data, and params: predictable, until they're not (the limits: data walls, inference economics).\n"
"- **Scaling-law gap** \u2014 scaling laws predict pretraining loss, not downstream usefulness: the gap matters.\n"
"- **Benchmarks vs evals** \u2014 benchmarks rank; evals measure what YOU care about.\n"
"- **Contamination** \u2014 train-on-test invalidates the measurement: check contamination before trusting any benchmark number.\n"
"- **LLM-as-judge** \u2014 with rubrics and human calibration.\n"
"- **Probing** \u2014 what's linearly decodable from a representation.\n"
"- **Circuits** \u2014 reverse-engineering small computations: the honest state is promising, partial.\n"
"- **Specification gaming** \u2014 Goodharting the reward: the classic boat-racing loop \u2014 optimizing the metric instead of the goal.\n"
"- **Deceptive alignment** \u2014 a debated hypothesis: state it as such, not as established fact.\n"
"- **Corrigibility** \u2014 the system permits oversight and correction: the alignment prerequisite everything else assumes.\n"
"- **Alignment** \u2014 the problem statements, distinguished from claimed solutions: state the problem precisely before evaluating any proposed solution."),
("Worked estimation",
"Attention is arithmetic before it's intuition. Work these by hand \u2014 show your steps.\n"
"1. **Attention memory.** For sequence length n=4096 with d=64 per head, the QK\u1d40 matrix holds n\u00b2 = 16.7M entries \u2192 at fp16 that's ~33.5 MB per head per layer. Multiply by heads \u00d7 layers for the layer's attention memory; write the product out.\n"
"2. **The KV-cache tax.** 2 (K and V) \u00d7 n \u00d7 d_model \u00d7 layers \u00d7 bytes: for a 32-layer, d_model=4096 model at n=8192 in fp16 \u2192 2 \u00d7 8192 \u00d7 4096 \u00d7 32 \u00d7 2 bytes \u2248 4.3 GB. That's the long-context tax \u2014 derive it yourself.\n"
"3. **Scaling arithmetic.** Loss follows power laws in compute: doubling compute buys a predictable (small) loss reduction. From the published exponents, estimate how many doublings a 0.1 loss drop requires \u2014 and note what that costs in dollars.\n"
"4. **The usefulness gap.** Translate a 5% pretraining-loss improvement into an eval delta on YOUR task: the mapping isn't in the scaling law \u2014 you must measure it. State the experiment you'd run.\n"
"5. **Contamination arithmetic.** If 10% of a benchmark leaked into training, bound how much of the reported score could be memorization vs generalization \u2014 then state why you'd still distrust the number even at the favorable bound."),
("Project brief",
"Read one paper properly \u2014 Attention Is All You Need (or BERT/GPT): one paragraph each on the problem, the insight, and the ablations. Then reproduce one estimation from the Worked estimation section and verify the order of magnitude against a real model config you look up. Deliverable: the three-paragraph paper brief plus your estimation write-up."),
("Honesty note",
"Original practice material \u2014 labs, questions, and scenarios are authored for this course. Every claim here is anchored to its paper: check the arXiv link in Source links and read the primary source before quoting. Deceptive alignment is a debated hypothesis \u2014 stated as such; don't present it as established fact. As-of dating: scaling-law exponents, model details, and the frontier itself move fast \u2014 re-verify quarterly, and cross-check the IL-23 frontier module for what's new. Self-check before moving on: derive why \u221ad_k matters; state the RLHF three stages; distinguish a problem statement from a solution in alignment."),
]

NOTES["il07-aws-data"] = [
("Concepts",
"- **Kinesis Data Streams** \u2014 real-time ingestion: a retained log with replay and multiple consumers.\n"
"- **Kinesis Firehose** \u2014 delivery-to-S3 with no consumer management: Firehose delivers, Streams keeps.\n"
"- **MSK** \u2014 managed Kafka: when you need Kafka semantics (Kafka protocol, replay, many consumers).\n"
"- **DMS** \u2014 database migration and replication, including CDC.\n"
"- **CDC** \u2014 change data capture: the operational database becomes a stream \u2014 the modern ingestion pattern.\n"
"- **Transfer Family** \u2014 SFTP into S3.\n"
"- **Glue** \u2014 serverless Spark plus the Data Catalog and crawlers.\n"
"- **EMR** \u2014 managed Hadoop/Spark at scale.\n"
"- **Lambda** \u2014 event-driven micro-batch transformation.\n"
"- **Step Functions** \u2014 orchestration of the pipeline's steps.\n"
"- **S3 data lakes** \u2014 raw \u2192 curated \u2192 serving zones.\n"
"- **Parquet** \u2014 the columnar analytics format: 10x less scanned = 10x cheaper and faster \u2014 format discipline pays.\n"
"- **Partitioning** \u2014 partition by query pattern (date/id): partition pruning is the performance story.\n"
"- **Lifecycle to Glacier** \u2014 age data down the storage tiers.\n"
"- **Redshift** \u2014 the columnar warehouse.\n"
"- **Distribution styles** \u2014 KEY / ALL / EVEN: how rows spread across nodes.\n"
"- **Distkey** \u2014 co-locates joins on the join key: the join stays local, no network shuffle.\n"
"- **Sortkey** \u2014 prunes scans via zone maps.\n"
"- **DynamoDB single-table design** \u2014 the access-pattern-first methodology: design for access patterns FIRST (GSIs for the alternates), never entity-first.\n"
"- **RDS/Aurora** \u2014 the relational tier.\n"
"- **Lake Formation** \u2014 centralized permissions on the lake.\n"
"- **LF-tags** \u2014 attribute-based lake permissions: scale without policy explosion.\n"
"- **Encryption** \u2014 SSE-S3/SSE-KMS at rest, TLS in transit.\n"
"- **Monitoring** \u2014 CloudWatch; Glue job bookmarks and metrics.\n"
"- **Job bookmarks** \u2014 exactly-once-ish processing without reprocessing everything.\n"
"- **Cost controls** \u2014 S3 Intelligent-Tiering, Redshift pause/resume, right-sized Glue DPUs.\n"
"- **Exam strategy** \u2014 scenario-heavy: every question is a pipeline decision; domain weights guide study; the exam loves 'least operational overhead' \u2014 managed beats self-managed when requirements allow."),
("Hands-on procedure",
"Build one pipeline per domain \u2014 this sequence is the module's lab spine.\n"
"1. **Land the stream.** Send a clickstream to S3 via Firehose; then write a Data Streams consumer for the same feed \u2014 note exactly what Firehose spares you (no consumer code, no shard management).\n"
"2. **CDC it.** Replicate an operational table with DMS CDC into S3; verify the change feed lands and orders correctly.\n"
"3. **Transform.** Write a Glue job (Spark) over the raw zone: partition by date, write Parquet to the curated zone; confirm the scan reduction.\n"
"4. **Warehouse.** Load Redshift with distkey on the join key and sortkey on the filter column; run EXPLAIN on a join and confirm co-location.\n"
"5. **Serve key-value.** Model a DynamoDB single table for the access patterns first; add a GSI for the alternate pattern.\n"
"6. **Secure.** Apply Lake Formation LF-tags for two analyst groups; verify least-privilege with a denied query.\n"
"7. **Operate.** Turn on Glue job bookmarks; rerun the job and confirm only new data processed \u2014 exactly-once-ish, observed."),
("Project brief",
"One pipeline per domain, end to end: stream ingestion (your choice of Kinesis/MSK/DMS, with a written justification), Glue/EMR transformation with partitioning discipline, lakehouse storage (raw \u2192 curated \u2192 serving, Parquet), Redshift or DynamoDB serving per access pattern, Lake Formation security, and a cost note (Intelligent-Tiering, pause/resume, DPU sizing). Deliverable: the running pipeline plus an architecture doc that answers 'why this service' for every choice."),
("Honesty note",
"Original practice material \u2014 labs, questions, and scenarios are authored for this course, never recalled from any exam. The exam reads scenario-heavy in this write-up's judgment \u2014 your experience may vary. Exam codes and domain weights change: confirm on aws.amazon.com before booking (see Source links). Cost figures are directional; the Pricing Calculator is the source of truth. Self-check before moving on: Firehose vs Streams in one sentence; the DynamoDB design order; what job bookmarks buy you."),
]

NOTES["il07-aws-ml"] = [
("Concepts",
"- **Feature Store** \u2014 online/offline consistency: one feature definition for training and serving \u2014 the train/serve skew killer.\n"
"- **Train/serve skew** \u2014 features computed differently in training vs serving: the silent model killer.\n"
"- **Ground Truth** \u2014 human labeling workflows with active learning.\n"
"- **Active learning** \u2014 escalate uncertainty to humans: label where labels matter; start with weak supervision/pretrained, escalate to humans for the hard cases.\n"
"- **Glue/EMR prep at scale** \u2014 the data-engineering tier feeding ML training.\n"
"- **SageMaker training** \u2014 managed training jobs.\n"
"- **Built-in algorithms** \u2014 XGBoost, BlazingText, DeepAR: built-ins win on undifferentiated problems \u2014 custom for the novel.\n"
"- **Automatic model tuning** \u2014 Bayesian hyperparameter optimization.\n"
"- **Real-time endpoints** \u2014 autoscaling variants for online inference.\n"
"- **Batch transform** \u2014 offline inference at scale.\n"
"- **Multi-model endpoints** \u2014 many low-traffic models on one fleet: shared economics.\n"
"- **Inference pipelines** \u2014 pre/post-processing chains around the model.\n"
"- **Shadow deployments** \u2014 the new model scores live traffic without serving: safe validation before promotion.\n"
"- **SageMaker Pipelines** \u2014 CI/CD for ML.\n"
"- **Model Registry** \u2014 versioned, approved models.\n"
"- **Model Monitor** \u2014 data drift and quality-decay alerts in production: the ML smoke detector.\n"
"- **Lineage tracking** \u2014 which data and code produced which model.\n"
"- **Data versioning** \u2014 the dataset is part of the model artifact: version it.\n"
"- **Bedrock** \u2014 foundation models as API.\n"
"- **Bedrock Guardrails** \u2014 the safety layer on Bedrock generation.\n"
"- **Bedrock Knowledge Bases** \u2014 managed RAG: connect data sources, get retrieval-augmented generation via API \u2014 least overhead for GenAI Q&A.\n"
"- **Bedrock Agents** \u2014 agentic workflows on the Bedrock substrate.\n"
"- **Bedrock vs SageMaker** \u2014 API convenience vs training control: pick by differentiation.\n"
"- **Exam strategy** \u2014 the specialty is scenario-dense: data prep \u2192 modeling \u2192 deployment \u2192 operations, with cost and 'least overhead' as tiebreakers.\n"
"- **The exam's favorite trap** \u2014 training where inference suffices: use a pretrained model or Bedrock first."),
("Hands-on procedure",
"1. **Kill the skew.** Define features in Feature Store (offline + online groups); demonstrate the same definition serving training and inference.\n"
"2. **Label smart.** Run a Ground Truth-style workflow on a small dataset: weak labels first, humans on the uncertain cases via active learning.\n"
"3. **Train managed.** Train with a SageMaker built-in (XGBoost); run automatic model tuning over three hyperparameters and record the winner.\n"
"4. **Register and deploy.** Register the best model in Model Registry; approve it; deploy to a real-time endpoint with autoscaling.\n"
"5. **Shadow the challenger.** Add a shadow variant with the challenger model; compare live scores without serving it \u2014 evidence before promotion.\n"
"6. **Watch it decay.** Enable Model Monitor; feed shifted data; confirm the drift alert fires \u2014 the smoke detector works."),
("Project brief",
"The MLOps capstone: a full SageMaker pipeline \u2014 Feature Store features, a versioned dataset, a tuned training job, a registered model, shadow-validated deployment, and Model Monitor watching production. Plus the Bedrock alternative: implement the same use case's GenAI slice with Knowledge Bases and write the 'Bedrock vs SageMaker' decision memo. Deliverable: the pipeline plus the decision memo."),
("Honesty note",
"Original practice material \u2014 labs, questions, and scenarios are authored for this course, never recalled from any exam. The specialty exam reads scenario-dense in this write-up's judgment. Exam codes change: confirm on aws.amazon.com before booking (see Source links). Bedrock model availability varies by region and changes frequently \u2014 verify in the console as of your study date. Self-check before moving on: the train/serve skew fix; when built-in beats custom; what Model Monitor watches."),
]
