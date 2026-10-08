# Module notes data, part 1: modules 1-3 (mongodb, data-schools, ai-ml)
# Each entry: (title, body). Section 2 title is "Hands-on procedure" or "Worked estimation".

NOTES = {}

NOTES["il07-mongodb"] = [
("Concepts",
"- **Documents, collections, databases** \u2014 JSON-like BSON documents grouped into collections, collections into databases.\n"
"- **Flexible schema** \u2014 fields vary per document; the schema lives in the application, enforced optionally by schema validation rules.\n"
"- **Schema validation** \u2014 JSON Schema rules on the collection: flexibility with guardrails.\n"
"- **ObjectId** \u2014 time-ordered and unique; sortable by creation, no coordination needed.\n"
"- **Value types** \u2014 dates as dates (not strings \u2014 queryability depends on it); arrays and subdocuments as first-class citizens.\n"
"- **Aggregation framework** \u2014 pipelines of stages: $match (filter early), $group (accumulate), $project (shape), $lookup (the join), $unwind (arrays).\n"
"- **Accumulators and expressions** \u2014 $sum, $avg, $push, plus date and string operators.\n"
"- **Embedding** \u2014 nested related data in one document: one read gets everything; for contained, bounded relationships.\n"
"- **Referencing** \u2014 store _ids and join with $lookup: for unbounded, many-to-many, or shared entities.\n"
"- **Modeling mantra** \u2014 model for your queries, not your entities.\n"
"- **ESR** \u2014 Equality, Sort, Range: compound index field order \u2014 equality fields first, then sort, then range.\n"
"- **explain('executionStats')** \u2014 the query plan: IXSCAN good, COLLSCAN means add an index for the query pattern; read winning vs rejected plans.\n"
"- **PyMongo** \u2014 the Python driver: CRUD, cursors, bulk writes.\n"
"- **ODM patterns** \u2014 MongoEngine/Beanie at concept level: when the object mapping helps vs hurts.\n"
"- **Transactions** \u2014 multi-document ACID since 4.0: design to avoid them (embed!), use them where correctness demands.\n"
"- **Bulk writes** \u2014 for ingestion; never one-insert-per-loop at scale.\n"
"- **Atlas** \u2014 the managed path: free tier for learning, Data Explorer for visual querying.\n"
"- **16MB document limit** \u2014 the hard cap that forces referencing for unbounded growth."),
("Hands-on procedure",
"Work through this sequence exactly \u2014 it's the module's lab spine, and it mirrors the quiz logic.\n"
"1. **Provision the cluster.** Spin up an Atlas free-tier cluster (or start mongod locally) and connect with your driver.\n"
"2. **Load a sample.** Insert an e-commerce dataset: orders with line items, customers, products.\n"
"3. **Pipeline.** Write an aggregation pipeline that filters early ($match), accumulates ($group), and shapes ($project) \u2014 revenue by category.\n"
"4. **Join.** Add a $lookup joining orders to customers; observe what the join costs vs an embedded design.\n"
"5. **Index and verify.** Create a compound index following ESR for your pipeline's $match and sort; run explain('executionStats') and confirm IXSCAN, not COLLSCAN.\n"
"6. **Bulk ingest.** Bulk-insert 100k documents with bulk_write; time it against one-insert-per-loop and record the ratio.\n"
"7. **Transact, then remodel.** Implement a multi-document transfer with a transaction; then remodel to embed and show the transaction disappearing \u2014 the design lesson in one exercise."),
("Project brief",
"Your capstone has two workstreams. (1) **The modeling capstone:** given a set of query patterns for a marketplace (product catalog, orders, reviews, sellers), produce a full schema \u2014 which relationships embed, which reference, which indexes (ESR-ordered) \u2014 and defend each choice in writing. (2) **The application capstone:** build a working PyMongo app against that schema with bulk ingestion, an aggregation analytics endpoint, and transactions only where correctness demands them. Deliverable: the schema document, the repo, and a short write-up of what the explain plans taught you."),
("Honesty note",
"Every lab, question, and scenario in this module is original practice material authored for this course \u2014 never recalled from any certification exam. Performance guidance (filter early, ESR order, bulk over loops) is directional: measure on your own data and hardware before quoting it. MongoDB features and the Atlas free tier change over time \u2014 verify against the current docs (see Source links) as of your study date. Self-check before moving on: state the embed-vs-reference rule in one sentence; read an explain plan and name the winning plan; defend your capstone's index choices with ESR."),
]

NOTES["il07-data-schools"] = [
("Concepts",
"- **SQL fluency** \u2014 joins, windows, CTEs: the analyst's core.\n"
"- **Honest visualization** \u2014 the right encoding for the message; charts that don't lie.\n"
"- **Statistics for analysts** \u2014 distributions, confidence, A/B basics.\n"
"- **Portfolio** \u2014 analyses that tell stories; certificates prove coursework, the portfolio proves ability \u2014 do both.\n"
"- **Pipelines and orchestration** \u2014 DAGs, retries, backfills, idempotency; the DAG is the contract, retries and backfills are the reliability story.\n"
"- **Dimensional modeling** \u2014 facts and dimensions, star schemas, slowly changing dimensions.\n"
"- **SCD Type 1** \u2014 overwrite the dimension attribute; history is lost.\n"
"- **SCD Type 2** \u2014 version the dimension row on change (new row, same natural key): history is a business requirement.\n"
"- **Batch and streaming** \u2014 exactly-once semantics, watermarks, late data.\n"
"- **Exactly-once** \u2014 the three-part recipe: idempotent sinks + transactional writes + replayable sources.\n"
"- **Idempotency** \u2014 reruns converge: merge/upsert keys make backfills safe instead of duplicating rows.\n"
"- **Data quality and governance** \u2014 tests on data: freshness, volume, schema, distribution checks; quality tests run IN the pipeline (great expectations or dbt tests, not hope).\n"
"- **Relational internals** \u2014 pages, B-trees, the cost-based query planner (statistics drive plans).\n"
"- **EXPLAIN** \u2014 read it like a story: scan types, join algorithms, row estimates vs actuals.\n"
"- **ANALYZE** \u2014 the fix for mystery slowdowns when statistics go stale and the planner lies.\n"
"- **Isolation levels** \u2014 read committed \u2192 repeatable read \u2192 serializable; each level trades anomalies for concurrency.\n"
"- **Anomalies** \u2014 dirty reads, non-repeatable reads, phantom reads; know which anomaly each level permits.\n"
"- **MVCC** \u2014 multi-version concurrency control: readers see snapshots and don't block writers (Postgres, MySQL-InnoDB).\n"
"- **Distributed processing** \u2014 partition \u2192 shuffle \u2192 compute; shuffle is the expensive operation.\n"
"- **Shuffle** \u2014 all-to-all network transfer plus sort; avoid it by partitioning on the join key.\n"
"- **Hadoop/Spark lineage** \u2014 MapReduce \u2192 RDDs \u2192 DataFrames \u2192 Spark SQL.\n"
"- **Sketching** \u2014 trade exactness for memory: HyperLogLog (probabilistic distinct-count in KBs), Bloom filters.\n"
"- **HyperLogLog** \u2014 counts distincts in kilobytes of memory with small error \u2014 sketching for massive data.\n"
"- **Credential maps** \u2014 MIT xPRO Data Engineering / Advanced Analytics and MicroMasters SDS; Stanford's Data Mining, Mining Massive Data Sets, and Databases graduate certificates \u2014 preparation mapping for each."),
("Worked estimation",
"Data engineering is estimation before it's code. Work these by hand \u2014 show your arithmetic.\n"
"1. **Volume.** 10 billion events/day at 500 bytes each \u2192 ~5 TB/day raw; 90-day retention \u2192 ~450 TB before replication. Write the multiplication out.\n"
"2. **The shuffle join.** Joining 2 TB of fact to 500 GB of dimension with a shuffle join moves ~2.5 TB across the network; at ~10 Gbps effective throughput that's roughly 35 minutes of transfer alone. Show the division.\n"
"3. **The fix.** Co-partition both sides by the join key: the shuffle drops to ~0 and the join becomes a local merge per partition. Restate the transfer time.\n"
"4. **The sketch.** Exact distinct-count needs a hash set of up to N entries; HyperLogLog needs ~1.5 KB for ~2% standard error on 10B users. Compute the memory ratio and state when the error is acceptable.\n"
"5. **Quality-test placement.** Running freshness/volume/schema/distribution checks inside the pipeline costs about one extra scan \u2014 roughly the pipeline's cheapest stage; catching a bad load downstream costs reprocessing the whole day. Put numbers on both.\n"
"6. **Backfill idempotency.** Without merge keys, every rerun multiplies rows (reruns \u00d7 rows); with idempotent merge keys, reruns converge to zero duplicates. Quantify the duplicate-row count for three reruns of a 1B-row load."),
("Project brief",
"Your milestone: one end-to-end pipeline. Ingest a public dataset (or the module starter), orchestrate it as a DAG with retries and backfills, model it as a star schema with one SCD Type 2 dimension, load it with idempotent merge keys, and gate it with in-pipeline quality tests (freshness, volume, schema, distribution). Then write the analyst deliverable: one honest visualization and a portfolio-style analysis that tells a story. Deliverable: the pipeline repo plus the analysis write-up."),
("Honesty note",
"All practice material here is original \u2014 labs, questions, and scenarios are authored for this course, never recalled from any exam. Sketch error bounds (~2%) are typical, not guaranteed; they depend on the data. The credential maps are preparation mappings only: Interstitium Labs confers no certificate and is not affiliated with MIT or Stanford \u2014 confirm current program availability and exam codes on the schools' own sites. Self-check before moving on: state exactly-once's three parts; name which anomaly each isolation level permits; explain shuffle avoidance in one sentence."),
]

NOTES["il07-ai-ml"] = [
("Concepts",
"- **Supervised learning** \u2014 regression/classification: learn a mapping from labeled examples via a loss function.\n"
"- **Loss functions and regularization** \u2014 what the model minimizes, and the penalty that keeps it honest.\n"
"- **Regularization menu** \u2014 L1/L2, dropout, early stopping, augmentation: know when each applies.\n"
"- **Kernels and SVMs** \u2014 the kernel trick: implicit high-dimensional features via the kernel function, no explicit mapping computed.\n"
"- **Bayesian methods** \u2014 priors, MAP, the probabilistic view of learning.\n"
"- **Bias/variance decomposition** \u2014 high bias \u2192 underfit (more capacity/features); high variance \u2192 overfit (more data/regularization).\n"
"- **VC dimension** \u2014 capacity vs data: the learning-theory measure of model expressiveness.\n"
"- **Backprop** \u2014 the chain rule through the network; implement it once from scratch in NumPy \u2014 the rite of passage that makes frameworks transparent.\n"
"- **CNNs** \u2014 convolutional architectures; train one on CIFAR-10 as the canonical exercise.\n"
"- **PyTorch fluency** \u2014 tensors, autograd, DataLoaders.\n"
"- **Classical NLP** \u2014 n-grams, embeddings: word2vec.\n"
"- **Transformers** \u2014 attention plus positional encoding; the architecture behind modern LLMs.\n"
"- **Instruction tuning and RLHF** \u2014 SFT \u2192 reward model \u2192 PPO: the alignment training recipe.\n"
"- **Tokenization (BPE)** \u2014 byte-pair encoding: subword units \u2014 frequent words whole, rare words split.\n"
"- **Decoding** \u2014 greedy, beam search, temperature/top-p sampling.\n"
"- **Temperature** \u2014 low = deterministic, high = creative: decoding is a policy choice.\n"
"- **Transfer learning** \u2014 pretrain on big data, fine-tune on yours: the 90% solution (fine-tune the head is the practical default).\n"
"- **Vision (CS231N arc)** \u2014 CNN architectures (the zoo: ResNet's skip connections), detection/segmentation, vision transformers.\n"
"- **MDPs** \u2014 Markov decision processes: states, actions, rewards, discount.\n"
"- **Dynamic programming** \u2014 the tabular RL foundation.\n"
"- **Policy gradients (REINFORCE)** \u2014 optimize the policy directly (on-policy).\n"
"- **Value methods (Q-learning)** \u2014 learn Q, then act (off-policy).\n"
"- **RLHF connection** \u2014 human preferences as the reward; the reward model IS the product \u2014 alignment quality lives there.\n"
"- **MLOps maturity levels** \u2014 level 0 manual, level 1 ML pipeline, level 2 automated retraining (CI/CD for ML).\n"
"- **Experiment tracking** \u2014 params, metrics, artifacts: reproducibility.\n"
"- **Deployment** \u2014 batch vs online, shadow/canary.\n"
"- **Monitoring** \u2014 data drift, performance decay: input distribution shifts silently kill models \u2014 the MLOps ongoing tax.\n"
"- **Data and model versioning** \u2014 DVC/registry: the model is a build artifact; version the dataset too.\n"
"- **RAG** \u2014 retrieve \u2192 augment \u2192 generate: grounding generation in retrieved context.\n"
"- **RAG failure hierarchy** \u2014 RAG fails at retrieval first: chunking + embeddings + reranking beat bigger models.\n"
"- **LLM evaluation** \u2014 faithfulness (grounded?), relevance (answers the question?), groundedness; LLM-as-judge with rubrics; evaluate with rubrics, not vibes.\n"
"- **Fine-tuning shapes** \u2014 full vs LoRA.\n"
"- **Guardrails** \u2014 the safety layer around generation."),
("Hands-on procedure",
"1. **Induce the failure modes.** Train a small classifier three ways: a tiny model (high bias \u2014 underfit), a deep model on little data (high variance \u2014 overfit), and a right-sized baseline. Record train vs validation error for each and diagnose from the gap.\n"
"2. **Backprop by hand.** Implement the forward and backward pass through a 2-layer net in NumPy; gradient-check against numerical gradients until they agree to 1e-7.\n"
"3. **Train the CNN.** Build a CNN on CIFAR-10 in PyTorch with DataLoaders; apply the regularization menu one item at a time and record which moves validation accuracy.\n"
"4. **Feel the temperature.** Tokenize with BPE; decode the same prompt at temperature 0.1, 0.7, and 1.5 \u2014 record how determinism gives way to diversity.\n"
"5. **Build RAG, then fix retrieval.** Build a small RAG pipeline (chunk \u2192 embed \u2192 retrieve \u2192 generate); then add reranking and a faithfulness rubric \u2014 measure which change helped most and write it down.\n"
"6. **Simulate drift.** Evaluate a trained model on a shifted input distribution; set a monitoring threshold that would have paged you before the decay mattered."),
("Project brief",
"Build and evaluate a RAG system on a real corpus (the course docs make a good first target). Choose a chunking strategy, embeddings, and reranking; then write the evaluation: faithfulness and relevance rubrics scored with an LLM judge that you calibrate against your own human labels. Deliverable: the running system plus an eval report that names the #1 failure mode you found and how you fixed it."),
("Honesty note",
"Original practice material only \u2014 labs, questions, and scenarios are authored for this course, never recalled from any exam. Reported numbers (accuracy, tokens/sec) are yours to reproduce: report your hardware and seed alongside any claim. The math prerequisites gate the deep end per the course arc (IL-02) \u2014 don't skip them. Self-check before moving on: diagnose a train/validation gap; explain the RLHF three stages; state the RAG failure hierarchy in order."),
]
