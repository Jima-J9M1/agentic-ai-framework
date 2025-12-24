# 🧠 Agentic AI Framework (FastAPI-based)

A production-oriented **agentic AI framework** built with **FastAPI**, supporting:
- Tool-using agents
- Session-aware vector memory
- Memory summarization with TTL
- Multi-agent debate & critic loops
- Deterministic + LLM-based evaluation
- Hallucination scoring & guardrails

This project is designed to work **without premium LLM APIs**, using open-source or local models.

---

## 🚀 Features

### ✅ Core Agent Capabilities
- Planner → Worker → Critic orchestration
- Tool execution with validation
- Structured JSON IO contracts

### 🧠 Memory System
- Vector-based semantic memory
- Session-aware isolation
- Automatic memory summarization
- TTL-based memory expiration

### 🤝 Multi-Agent Debate
- Planner generates solution
- Critic agent challenges reasoning
- Debate loop improves correctness

### 🛡️ Safety & Evaluation
- Deterministic rule-based evaluation
- LLM-based evaluator
- Hallucination scoring
- Intent alignment scoring
- Plan validity checks

### 🏗️ Production Ready
- FastAPI backend
- Modular architecture
- Extensible evaluation framework
- Logging-friendly design

---

## 📁 Project Structure

```text
app/
├── main.py
├── agents/
│   ├── planner.py
│   ├── worker.py
│   ├── critic.py
│   └── orchestrator.py
├── memory/
│   ├── vector_store.py
│   ├── session_memory.py
│   └── summarizer.py
├── evaluation/
│   ├── schemas.py
│   ├── deterministic.py
│   └── llm_evaluator.py
├── tools/
│   └── math_tool.py
├── llm/
│   └── client.py
└── logger.py
````

---

## 🧩 System Flow (Simplified)

1. User sends task
2. Planner agent creates a plan
3. Critic agent reviews the plan
4. Worker executes approved steps
5. Memory is stored & summarized
6. Evaluation scores output quality
7. Unsafe or low-quality outputs can be blocked

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **LLMs:** Local / open-source (Ollama, llama.cpp, etc.)
* **Memory:** Vector embeddings (FAISS / in-memory)
* **Evaluation:** Rule-based + LLM-based
* **Language:** Python 3.10+

---

## 📌 Why This Project Exists

Most agent demos:

* Ignore hallucinations
* Don’t evaluate outputs
* Break in production

This framework focuses on **correctness, safety, and observability**, not just generation.

---

# High-Level System Design (HLD)

## 🎯 Goal

Build a **safe, observable, and extensible agent system** capable of:
- Reasoning
- Tool usage
- Memory retention
- Self-evaluation

---

## 🧠 High-Level Architecture

```

┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────┐
│  FastAPI    │
│  Gateway    │
└──────┬──────┘
       │
┌──────▼──────────┐
│ Agent Orchestr. │
│ (Control Plane) │
└───── ┬──────────┘
       │
 ┌─────▼─────┐
 │ Planner   │
 └─────┬─────┘
       │
 ┌─────▼─────┐
 │ Critic    │
 └─────┬─────┘
       │
 ┌─────▼─────┐
 │ Worker    │
 └─────┬─────┘
       │
 ┌─────▼─────────────┐
 │ Tools / Functions │
 └───────────────────┘

```

---

## 🧠 Memory Subsystem (HLD)

```

User Input
↓
Vector Embedding
↓
Session Memory Store
↓
TTL Enforcement
↓
Summarization

````

---

## 🛡️ Evaluation Layer (HLD)

Two parallel evaluators:

- **Deterministic Evaluator**
  - Schema checks
  - Tool usage validation
  - Logical constraints

- **LLM-Based Evaluator**
  - Hallucination detection
  - Intent alignment
  - Reasoning quality

---

## 🧩 Key Design Principles

- Separation of concerns
- Model-agnostic LLM layer
- Memory isolation per session
- Evaluation as a first-class citizen

---

# 3️⃣ Low-Level System Design (LLD)

## 🧱 Agent Orchestrator

**Responsibilities**
- Controls agent flow
- Handles debate loops
- Integrates evaluation

```text
Input → Planner → Critic → Worker → Evaluation
````

---

## 🧠 Planner Agent

* Converts user input → structured plan
* Outputs JSON steps
* No tool execution

---

## 🔍 Critic Agent

* Reviews planner output
* Detects logical flaws
* Can request replanning

---

## ⚙️ Worker Agent

* Executes validated steps
* Calls tools
* Stores results in memory

---

## 🧠 Memory System (LLD)

### Vector Store

* Embeddings indexed per session
* Similarity search for recall

### Session Memory Manager

* One memory store per session
* Prevents cross-user leakage

### Summarizer

* Compresses old memory
* Preserves semantic meaning
* Enforced via TTL

**Why TTL + Summarization?**

* Prevents context explosion
* Reduces hallucinations
* Improves retrieval quality

---

## 🛡️ Evaluation System (LLD)

### Deterministic Evaluator

* Output schema validation
* Tool correctness
* Binary failure detection

### LLM-Based Evaluator

* Scores:

  * Intent alignment
  * Hallucination risk
  * Reasoning quality
* Produces structured JSON scores

---

## 🔐 Safety Guarantees

* Invalid plans are rejected
* Hallucinated outputs are scored
* Low-confidence outputs can be blocked
* Memory does not leak across sessions

---

## 📈 Extensibility Points

* Plug new tools
* Swap LLM backends
* Add new evaluators
* Add routing / A–B later

---

## ✅ Production Readiness Checklist

* [x] Guardrails
* [x] Evaluation
* [x] Memory management
* [x] Multi-agent debate
* [x] API boundary
* [ ] Monitoring dashboard (optional)
* [ ] Load testing (optional)

---

## 🧠 Final Note (Very Important)

This project is **not a demo agent**.
It is a **foundation for real agentic systems**.

---
