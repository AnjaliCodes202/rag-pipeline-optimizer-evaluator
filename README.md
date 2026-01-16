RAG Pipeline Optimizer & Evaluator

Architecture & System Explanation

1️⃣ What problem this project solves (big picture)

Most RAG projects answer only one question:

“Does RAG work?”

This project answers much harder questions:

Which RAG pipeline works better?

Why does it work better?

How much does it cost?

How fast is it?

What quality–cost–latency tradeoff should I choose?

This turns RAG from a demo system into an engineering decision platform.

2️⃣ High-level system flow (end-to-end)
Documents
 → Ingestion
   → Chunking (pipeline-controlled)
     → Embeddings
       → Retrieval
         → Optional Reranking
           → Generation
             → Evaluation (LLM-as-Judge)
               → Cost & Latency Tracking
                 → Tradeoff Scoring
                   → Pipeline Recommendation


Every arrow is measured, configurable, and explainable.

3️⃣ Core architectural principles (important)
Principle 1: Separation of concerns

Each layer does one job only:

Layer	Responsibility
Ingestion	Read files, extract raw text
Chunking	Split text based on pipeline config
Embeddings	Convert text → vectors
Retrieval	Find relevant chunks
Reranking	Refine relevance (optional)
Generation	Produce final answer
Evaluation	Judge answer quality
Experiment Runner	Orchestrate execution
Comparator	Compare pipelines
Recommendation	Explain best choice

No layer “knows too much”.

Principle 2: Pipeline as configuration, not code

Pipelines are data, not logic.

A pipeline controls:

chunking strategy

chunk size & overlap

embedding model

reranker ON/OFF

top-k

generation model

This enables:

fast experimentation

fair comparison

reproducibility

Principle 3: Everything is measurable

Each pipeline produces:

Answer

Retrieved chunks (traceability)

Evaluation scores

Cost metrics

Latency metrics

Tradeoff score

Nothing is a black box.

4️⃣ Backend folder architecture (explained simply)
core/ — the RAG brain
File	What it does
chunking.py	Multiple chunking strategies + pipeline-based selection
embeddings.py	Embedding abstraction (provider-agnostic)
retrieval.py	Vector similarity search
reranking.py	Optional cross-encoder reranking
generation.py	Prompt building + answer generation
judge.py	LLM-as-judge evaluation
core/experiment_runner/ — orchestration layer
File	Role
executor.py	Executes one pipeline end-to-end
tracker.py	Structures experiment output
comparator.py	Multi-pipeline comparison + scoring + recommendation

This is the heart of the system.

services/ — cross-cutting utilities
File	Role
cost_tracker.py	Token & cost estimation
document_service.py	Document metadata storage
pipeline_service.py	Pipeline persistence
evaluation_service.py	Evaluation coordination
utils/observability/
File	Role
metrics.py	Latency tracking via context managers
5️⃣ How one query actually runs (step-by-step)

For one query + one pipeline:

Raw document text is chunked based on pipeline config

Chunks are embedded

Query is embedded

Top-k chunks retrieved via cosine similarity

(Optional) reranking refines relevance

Context is assembled

Generator produces answer

Judge evaluates answer quality

Cost and latency are measured

Experiment result is produced

This happens identically for every pipeline → fair comparison.

6️⃣ Evaluation logic (why it’s strong)

Evaluation is not vibes-based.

Each answer is scored on:

Relevance → does it answer the question?

Faithfulness → is it grounded in retrieved context?

Completeness → does it fully answer?

This enables:

hallucination detection

coverage analysis

pipeline comparison on quality, not opinion

7️⃣ Tradeoff score (key innovation)

Instead of “best answer wins”, you compute:

Tradeoff Score = Quality / (Cost × Latency)


This reflects real-world constraints:

Slightly worse answer may be preferred if:

10× cheaper

5× faster

This is senior-level system thinking.

