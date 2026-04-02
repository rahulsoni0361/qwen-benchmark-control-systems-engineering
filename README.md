# 🧠 Agentic AI Engineering Team — Control Systems Intelligence Framework

> *"We didn't just ask an AI to help us. We built a team of AI engineers that think, debate, and derive."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Backend-Ollama-black.svg)](https://ollama.ai/)
[![Model: Qwen 2.5 14B](https://img.shields.io/badge/Model-Qwen%202.5%2014B-orange.svg)](https://huggingface.co/Qwen)
[![Hardware: RTX 3090](https://img.shields.io/badge/GPU-RTX%203090-76b900.svg)](https://www.nvidia.com/)

---

## 🎯 Project Overview

This repository represents a **first-of-its-kind** multi-agent AI architecture purpose-built for **precision control systems engineering**. Specifically designed for N20 brushed DC gearmotor systems, this framework goes far beyond a simple chatbot or boilerplate prompt template.

We engineered an **AI organization** — a full team of highly specialized, persona-driven, memory-aware agents — each with their own domain expertise, cognitive style, and conflicting perspectives. Together, they simulate a high-stakes engineering review board that debates, derives, and diagnoses real control system problems.

**This is not prompt engineering. This is cognitive system architecture.**

---

## 🏗️ The Core Problem We Solved

Modern AI assistants fail engineers in a very specific, dangerous way: they are **confidently wrong on quantitative problems**. They will generate a plausible-sounding PID derivation with the wrong gains and present it without hesitation.

The standard "single chatbot" model cannot:
- Maintain engineering domain awareness across dozens of interactions
- Argue with itself from multiple expert perspectives
- Remember the context of a project's physical constraints session-to-session
- Distinguish between a linear stability failure and a nonlinear limit cycle

We solved all of this. Here's how.

---

## 🧬 System Architecture

### The Philosophy: Cognitive Diversity as a Safety Net

The fundamental design principle is **constructive conflict**. Placing a pure mathematician (Hannah) alongside a mechanical pragmatist (Marco) means that an elegant control law gets immediately stress-tested against physical reality — friction, backlash, inertia — before it ever reaches hardware.

Each agent is a **specialized cognitive engine**, not a personality mask over a generic model.

```
┌─────────────────────────────────────────────────────────────┐
│                    OLLAMA SERVER (RTX 3090)                 │
│                       qwen-64k model                        │
│                    64,000 token context                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────▼───────────┐
          │  AGENT ORCHESTRATOR   │
          │  (Python Controller)  │
          │  - Shared Memory Mode │
          │  - Persistent Logging │
          │  - Conversation RAG   │
          └─────────┬─────────────┘
                    │
    ┌───────────────┼───────────────────┐
    │               │                   │
┌───▼───┐      ┌───▼───┐          ┌────▼──┐
│HANNAH │      │SOPHIE │  • • •   │WALTER │
│Control│      │Firmware│         │RF/EMI │
└───────┘      └───────┘          └───────┘
```

### Memory Architecture

The system implements **three layers of memory**:

| Layer | Mechanism | Scope |
|:---|:---|:---|
| **In-Context Memory** | 64k token window per call | Single conversation turn |
| **Shared Team Memory** | Shared history list in orchestrator | Full session across all agents |
| **Persistent RAG Log** | Daily `.txt` log files | Cross-session, indefinite |

Every interaction is automatically persisted to `logs/chat_log_YYYY-MM-DD.txt`, building a **local knowledge corpus** that can later be indexed for Retrieval-Augmented Generation (RAG), enabling the agents to reference engineering decisions made weeks or months ago.

---

## 👥 The Engineering Team (Agent Roster)

Each agent is defined by a structured **JSON persona file** containing: role, identity, cognitive style, system prompt, reasoning levels, logical abilities, conditional behaviors (IF...THEN logic), and cross-agent interaction rules.

| Agent | Role | Domain Specialty | Cognitive Style |
|:---|:---|:---|:---|
| 🇩🇪 **Hannah** | Chief Control Engineer | PID/Loop Shaping, Pole-Zero, Stability | Mathematical. Derives everything. Zero tolerance for guessing. |
| 🇬🇧 **Sophie** | Embedded Systems Lead | PWM, ADC, ISR Timing, Firmware | Clock-obsessed. If sampling rate isn't mentioned, she demands it. |
| 🇮🇹 **Elena** | Systems Debugger | Cross-domain root cause analysis | "It always starts with an assumption somewhere." |
| 🇩🇪 **Walter** | RF / EMI Engineer | Signal integrity, switching noise, grounding | Paranoid about interference. Modeled after a Heisenberg-style methodologist. |
| 🇫🇷 **Clara** | Thermal & Power Engineer | Thermal runaway, efficiency, power budgets | "The motor doesn't care about your elegant math when it's at 80°C." |
| 🇧🇷 **Lucas** | Sensor & Measurement Lead | Encoder jitter, signal filtering, ADC noise | "If you can't measure it precisely, you can't control it." |
| 🇦🇷 **Marco** | Mechanical Systems Engineer | Backlash, friction, reflected inertia, gear physics | Physical realist who challenges every ideal-world assumption. |
| 🇦🇹 **Adrian** | Power Electronics Engineer | MOSFET drivers, H-bridges, dead-time, shoot-through | "The math dies at the gate driver." |
| 🇺🇸 **George** | Tech Lead / Integrator | System integration, architecture direction | Synthesizes team conflict into engineering decisions. |
| 🇺🇸 **Tom** | Junior Engineer / Devil's Advocate | "Why?" questions, first principles | Surfaces hidden assumptions by asking what experts take for granted. |

---

## 🔬 Benchmark Methodology

We designed a **15-question domain-specific validation suite** to assess whether a 14B parameter LLM can perform reliable quantitative engineering work.

### Question Categories

| Category | No. of Questions | Examples |
|:---|:---|:---|
| Transfer Function Analysis | 2 | DC gain derivation, pole extraction |
| PI Controller Design | 2 | Pole-zero cancellation, Kp/Ki derivation |
| Stability (Routh-Hurwitz) | 2 | Characteristic equation stability, phase margin |
| Time-Domain Specs | 2 | Percent overshoot, settling time |
| Nonlinear Phenomena | 2 | Limit cycle prediction, backlash reflection |
| Discrete-Time Control | 2 | Nyquist barrier, Tustin transform selection |
| N20 Motor Physics | 2 | Winding resistance, reflected inertia |
| Conceptual / Risk | 1 | Why pole-zero cancellation fails in practice |

### Grading System

A **regex-based automated grading engine** was built to fairly assess responses despite LaTeX formatting variations (e.g., `K_p = 13.33` vs `Kp=13.33` vs `\(K_p = 13.33\)`). This overcome the naive string-matching failures that previous iterations reported a misleadingly low score.

### Prompt Hardening Protocol

We applied **4 successive iterations** of persona engineering to maximize model performance:

| Version | Strategy | Score |
|:---|:---|:---|
| **V1 Baseline** | Generic engineer persona | ~40% (raw keyword) |
| **V2 Authority Tone** | Strict authoritative voice, mandatory terminology | ~42% |
| **V3 Knowledge Injection** | Specific techniques hard-coded (limit cycles, pole-zero) | ~52% |
| **V4 Worked Examples** | Full derivation examples embedded in prompt | ~65% |
| **V5 Regex Grading + Final** | Accurate grading + DC gain & backlash knowledge injected | **66.7%** |

### Key Finding

> Qwen 2.5 14B demonstrates **elite conceptual reasoning** (87% on terminology, domain understanding, and strategic recommendations) but **systematic arithmetic failures** on multi-step quantitative derivation. This represents a hard ceiling for 14B parameter models on precision engineering tasks — a ceiling that **prompt engineering cannot overcome**.

---

## 📁 Repository Structure

```
├── agents/                          # Persona configuration files
│   ├── hannah.json                  # Chief Control Engineer (Math-first)
│   ├── sophie.json                  # Embedded Systems (Timing-first)
│   ├── elena.json                   # Debugger (Root-cause-first)
│   ├── walter.json                  # RF/EMI (Signal-integrity-first)
│   ├── clara.json                   # Thermal (Power-budget-first)
│   ├── lucas.json                   # Sensors (Measurement-first)
│   ├── marco.json                   # Mechanical (Physics-first)
│   ├── adrian.json                  # Power Electronics (Gate driver-first)
│   ├── george.json                  # Tech Lead (Integration-first)
│   └── tom.json                     # Junior / Devil's Advocate
│
├── logs/                            # Auto-generated persistent RAG corpus
│   └── chat_log_YYYY-MM-DD.txt      # Daily conversation logs
│
├── ollama_agent_orchestrator.py     # 🔑 Main interactive team interface
├── hannah_full_validation.py        # 🧪 15-question benchmark suite
├── hannah_benchmark.py              # Quick 3-question benchmark
├── parallel_agents.py               # Async parallel team brainstorm
├── agent_test_harness.py            # Extended stress testing
│
├── hannah_full_validation.md        # 📊 Full validation results report
├── hannah_benchmark_results.md      # Benchmark output
├── agent_system_prompt.md           # Global team system documentation
├── server.txt                       # Ollama server configuration
└── README.md                        # This file
```

---

## ⚙️ Technical Stack

| Component | Technology | Reason |
|:---|:---|:---|
| **LLM Backend** | Ollama | Local, private, no API costs |
| **Model** | Qwen 2.5 14B (custom `qwen-64k`) | Best quality/VRAM balance for RTX 3090 |
| **Context Window** | 65,536 tokens (64k) | Enough for full project history + all personas |
| **Transport** | HTTP (built-in `http.client`) | Zero external Python dependencies |
| **Memory** | Python list (session) + `.txt` files (persistent) | RAG-ready corpus |
| **Persona Format** | JSON with embedded system prompts | Portable, version-controlled, human-readable |
| **Grading** | Python `re` module (regex) | Accounts for LaTeX and formatting variance |

---

## 🚀 Quick Start

### Prerequisites

1. A Linux/Mac machine with Ollama installed.
2. An RTX 3090 (or any GPU with 16GB+ VRAM).
3. Python 3.11+ on your Windows/Mac control machine.

### Server Setup (Linux machine with GPU)

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull and configure Qwen with 64k context
ollama pull qwen2.5:14b
ollama show qwen2.5:14b --modelfile > Modelfile
echo "PARAMETER num_ctx 65536" >> Modelfile
ollama create qwen-64k -f Modelfile

# 3. Serve on your network
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

### Client Setup (Your Windows machine)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/agentic-engineering-team.git
cd agentic-engineering-team

# Update the server IP in the config
# Edit OLLAMA_IP in all .py files to point to your server

# Run the interactive team
python ollama_agent_orchestrator.py

# Run the full benchmark
python hannah_full_validation.py
```

### Usage — Agent Commands

```
Rahul -> HANNAH: Your PI design has an overshoot problem. G(s) = 2 / (0.3s + 1). Desired tau_cl = 0.02s.
# Switch agents mid-conversation
/switch marco
Rahul -> MARCO: What's the reflected inertia with a 150:1 gearbox and J_L = 0.001?
# Exit
exit
```

---

## 🧠 What Makes This Different

### 1. Persona-Locked System Prompts
Each agent's `system_prompt` is not just a description — it is a **behavioral contract** with explicit `MANDATORY` knowledge bases, `CONDITIONAL LOGIC` (IF/THEN operators), and prohibited behaviors. This is closer to a cognitive architecture than a persona. 

### 2. Cross-Agent Conflict Resolution
In Shared Memory mode, when Hannah proposes a gain of `Kp = 190`, Marco's next response will **already know** Hannah's proposal and can challenge it from a mechanical standpoint. This creates emergent engineering debates without any explicit "debate" prompting.

### 3. Persistent Engineering Memory
Every session is automatically logged. The `logs/` folder becomes your project's **engineering brain** — a growing corpus of all decisions, derivations, and debates that future RAG systems can query.

### 4. Honest Benchmarking
We didn't stop when the model looked "good." We built a 15-question validation suite with known correct answers and automated regex-based grading. We published the real number: **66.7%**. This project includes the infrastructure to reproduce these results and test any future model.

---

## 📊 Benchmark Results Summary

| Domain | Questions | Pass Rate |
|:---|:---|:---|
| Transfer Functions | 2 | 50% |
| PI Controller Design | 2 | **100%** ✅ |
| Routh-Hurwitz Stability | 2 | **100%** ✅ |
| Time-Domain Specs | 2 | 50% |
| Nonlinear Dynamics | 2 | **100%** ✅ |
| Discrete-Time | 2 | **100%** ✅ |
| N20 Motor Physics | 2 | 0% ❌ |
| Conceptual Reasoning | 1 | 0% ❌ |
| **TOTAL** | **15** | **66.7%** |

### Verdict: The Arithmetic Wall

A 14B model is a world-class engineering **co-thinker**. It is not a reliable engineering **co-calculator**. For production control system work, all numerical outputs must be independently verified.

---

## 🗺️ Roadmap

- [ ] **RAG Integration** — Index the `logs/` corpus with ChromaDB for cross-session memory
- [ ] **Live Telemetry** — Connect agents to real-time N20 motor encoder data via serial/USB
- [ ] **Larger Model Testing** — Run the same benchmark on 27B, 32B, and 70B models
- [ ] **Agent Debate Mode** — Formal structured argumentation between agents
- [ ] **Web UI** — Flask/FastAPI dashboard for non-terminal access
- [ ] **Automated Report Generation** — PDF engineering reports from session logs

---

## 🤝 Contributing

Pull requests are welcome. If you're an engineer who wants to:
- Add a new agent persona (e.g., Simulation, Acoustics, Materials)
- Improve the benchmark question suite
- Implement RAG on the log corpus
- Add support for different Ollama models

Open an issue or submit a PR.

---

## 📜 License

MIT License. Use it, fork it, build on it. Just give credit where it's due.

---

## ⭐ Acknowledgment

Built by an engineer who got frustrated with AI that sounds smart but calculates wrong. This project exists because **engineering deserves better than hallucinated helpfulness**.

If this project helps you, star it. If it inspires you to go further, fork it. If you find something wrong, raise an issue — because that's what engineers do.

---

*"The poles don't care about your prompt. But the right prompt will force the model to care about the poles."*
