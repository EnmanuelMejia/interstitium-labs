#!/usr/bin/env python3
"""Retrofit IL-07 modules to the Multicloud (IL-19) course template shape.
Reads docs/university/data/courses/il-07-data-engineering-analytics-ai.json,
restructures every module (weight, instructor-voice summary, 4 titled note
sections), fixes stray quiz keys, converts 'code' mockTasks to 'choice',
validates, and writes atomically. Touches nothing else.
"""
import json, os, re, sys

REPO = os.path.expanduser("~/workspace/apex-audit")
PATH = os.path.join(REPO, "docs/university/data/courses/il-07-data-engineering-analytics-ai.json")

with open(PATH, encoding="utf-8") as f:
    course = json.load(f)

# ---------------------------------------------------------------- summaries
SUMMARIES = {
 "il07-mongodb": ("Welcome to Module 1 of IL-07 \u2014 Document Databases: MongoDB. I'm your instructor "
  "for this module, and together we're going to make the document database your home turf: Atlas foundations "
  "(clusters, Data Explorer, drivers), the document model (flexible schema, schema validation), the aggregation "
  "framework ($match/$group/$project/$lookup), data modeling (embedding vs referencing, indexing for query patterns), "
  "and MongoDB for Python developers (PyMongo, ODM patterns, transactions). By the end, you'll model documents from "
  "query patterns, read explain plans like a story, and ship a working PyMongo application that uses transactions "
  "only where correctness demands them."),
 "il07-data-schools": ("Welcome to Module 2 of IL-07 \u2014 The Data-School Spine. I'm your instructor for this "
  "module, and this is the course's backbone: four tracks in one. The analyst track (SQL fluency, honest "
  "visualization, statistics, portfolio), the data engineering track (pipelines, orchestration, warehousing, batch "
  "and streaming, quality and governance), the databases-deep track (relational internals, indexing, query planning, "
  "transactions and isolation), and the big-data systems track (distributed processing, the Hadoop/Spark lineage, "
  "mining massive datasets) \u2014 closed out with MIT and Stanford credential maps so you know exactly how to "
  "certify what you've learned."),
 "il07-ai-ml": ("Welcome to Module 3 of IL-07 \u2014 Machine Learning and LLM Engineering. I'm your instructor for "
  "this module, and we're walking the Stanford arc end to end: ML foundations (supervised learning, kernels/SVMs, "
  "Bayesian methods, learning theory \u2014 bias/variance, VC dimension), deep learning (backprop from scratch in "
  "NumPy, CNNs, PyTorch fluency), NLP\u2192LLMs (transformers, instruction tuning/RLHF, tokenization and decoding), "
  "vision, reinforcement learning (MDPs, policy gradients, the RLHF connection), MLOps (maturity levels, experiment "
  "tracking, deployment/monitoring, versioning), and LLM engineering (RAG architectures and beyond). Math "
  "prerequisites (IL-02) gate the deep end \u2014 the platform checks before you dive."),
 "il07-neuroai": ("Welcome to Module 4 of IL-07 \u2014 NeuroAI: Brain Principles in Computing. I'm your instructor "
  "for this module, and we're computing from the brain outward: computational neuroscience fundamentals (neural "
  "coding \u2014 rate vs spike; leaky integrate-and-fire and Hodgkin-Huxley; Hebbian learning and STDP), neural "
  "modeling and simulation (NEURON compartmental models, Brian2 spiking networks, STDP in code), and NeuroAI proper "
  "\u2014 transformer attention vs biological attention (the honest analogy), predictive coding and the Bayesian "
  "brain, spiking neural networks and neuromorphic hardware. Where the science is unsettled, we'll say so: rate vs "
  "timing is still debated, and you'll learn to hold both views."),
 "il07-openweight": ("Welcome to Module 5 of IL-07 \u2014 Open-Weight Models & Self-Hosting. I'm your instructor "
  "for this module, and you're going to run models on your own hardware: license literacy (open-source vs "
  "open-weight \u2014 adjacent, not identical; Apache 2.0/MIT grants; custom licenses \u2014 always read the card), "
  "the model families (Llama, Mistral, Qwen, DeepSeek, Gemma, Phi \u2014 release by release, license by license), "
  "quantization (GGUF, GPTQ/AWQ, the quality ladder), and serving (Ollama, llama.cpp, vLLM) with honest benchmarks. "
  "The golden rule of this module: the license card for THIS checkpoint is the source of truth."),
 "il07-agents": ("Welcome to Module 6 of IL-07 \u2014 Agent Harnesses & Frameworks. I'm your instructor for this "
  "module, and we're building agents from the loop outward: the agent loop framework-free (perceive\u2013act, tool "
  "calling as the primitive, the ReAct pattern by hand), then the harnesses \u2014 LangChain (agent-first API, "
  "middleware, integrations), LangGraph (stateful graphs, durable execution, checkpoints), LlamaIndex (data-first "
  "agents, Workflows), CrewAI (crews and flows), the Microsoft landscape (Semantic Kernel, Agent Framework, "
  "AutoGen) \u2014 plus DSPy, MCP, evaluation, and the failure-mode field guide. Build the loop by hand first; "
  "every framework becomes transparent."),
 "il07-frontier": ("Welcome to Module 7 of IL-07 \u2014 Frontier AI Topics. I'm your instructor for this module, "
  "and here every claim is anchored to its paper: attention in depth (scaled dot-product, multi-head specialization, "
  "causal masking), preference optimization (RLHF, DPO and beyond \u2014 the InstructGPT three-stage recipe), "
  "scaling laws, evaluation science, interpretability (probing, circuits), and alignment (the problem statements, "
  "not the solutions). This module is the stable core \u2014 the IL-23 frontier module tracks what's new, so "
  "cross-check it for the latest. The field moves fast: anchor to papers, re-verify claims quarterly."),
 "il07-aws-data": ("Welcome to Module 8 of IL-07 \u2014 AWS Data Engineering. I'm your instructor for this module, "
  "and we're walking the AWS Certified Data Engineer Associate domains with a build in every one: ingestion "
  "(Kinesis, MSK, DMS, Transfer Family), transformation (Glue, EMR, Lambda, Step Functions), storage (S3 data "
  "lakes, Redshift, DynamoDB, RDS/Aurora patterns), and operations/security (Lake Formation, IAM, encryption, "
  "monitoring, cost). The exam is scenario-heavy \u2014 every question is a pipeline decision \u2014 so we train on "
  "decisions, not definitions. Exam codes change: confirm on the vendor's site before booking."),
 "il07-aws-ml": ("Welcome to Module 9 of IL-07 \u2014 AWS ML Engineering. I'm your instructor for this module, and "
  "we're walking the AWS Certified Machine Learning Specialty domains: data engineering for ML (feature stores, "
  "Glue/EMR prep, labeling with Ground Truth), modeling (SageMaker training, built-in algorithms, hyperparameter "
  "tuning), deployment (endpoints, batch transform, multi-model, edge), and MLOps (Pipelines, Model Registry, "
  "Monitor, Bedrock for generative AI) \u2014 plus exam prep. The exam's favorite trap is training where inference "
  "suffices; we learn to reach for a pretrained model or Bedrock first."),
}
