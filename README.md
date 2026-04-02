# 🧠 Agentic AI Engineering Team — Control Systems Intelligence Framework

> *"We didn't just ask an AI to help us. We built a team of AI engineers that think, debate, and derive."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Backend-Ollama-black.svg)](https://ollama.ai/)
[![Model: Qwen 2.5 14B](https://img.shields.io/badge/Model-Qwen%202.5%2014B-orange.svg)](https://huggingface.co/Qwen)
[![Hardware: RTX 3090](https://img.shields.io/badge/GPU-RTX%203090-76b900.svg)](https://www.nvidia.com/)

---

## 🎯 Project Overview

This repository represents a **first-of-its-kind** multi-agent AI architecture purpose-built for **precision control systems engineering**. Specifically designed for N20 brushed DC gearmotor systems, this framework goes far beyond a simple chatbot.

We engineered an **AI organization** — a full team of highly specialized, persona-driven agents — each with their own domain expertise and cognitive style. 

**This is not prompt engineering. This is cognitive system architecture.**

---

## 🏗️ The Core Problem

Modern AI assistants are often **confidently wrong on quantitative problems**. They will generate a plausible-sounding PID derivation with the wrong gains.

Our framework uses **constructive conflict** (putting specialists like Hannah and Marco in the same context) to force the AI to challenge its own assumptions before presenting a solution.

---

## 👥 The Engineering Team (Agent Roster)

Each agent is defined by a structured **JSON persona file** with specific behavioral protocols.

| Agent | Role | Domain Specialty |
|:---|:---|:---|
| 🇩🇪 **Hannah** | Chief Control Engineer | PID/Loop Shaping, Pole-Zero, Stability |
| 🇬🇧 **Sophie** | Embedded Systems Lead | PWM, ADC, ISR Timing, Firmware |
| 🇮🇹 **Elena** | Systems Debugger | Root cause analysis |
| 🇩🇪 **Walter** | RF / EMI Engineer | Signal integrity, switching noise |
| 🇫🇷 **Clara** | Thermal & Power Engineer | Thermal runaway, efficiency |
| 🇧🇷 **Lucas** | Sensor & Measurement Lead | Encoder jitter, signal filtering |
| 🇦🇷 **Marco** | Mechanical Systems Engineer | Backlash, gear physics, inertia |
| 🇦🇹 **Adrian** | Power Electronics Engineer | MOSFET drivers, H-bridges |
| 🇺🇸 **George** | Tech Lead / Integrator | Architecture direction |
| 🇺🇸 **Tom** | Junior / Devil's Advocate | First principles challenger |

---

## 🔬 Benchmark Methodology

We designed a **15-question validation suite** to assess model reliability on quantitative engineering work.

| Version | Strategy | Score |
|:---|:---|:---|
| **V1 Baseline** | Generic persona | ~40% |
| **V4 Hardened** | Knowledge injection + Worked examples | **66.7%** |

**Key Finding:** Qwen 2.5 14B demonstrates **elite conceptual reasoning** but hit an **arithmetic ceiling** on multi-step quantitative derivation. This repository is built to push through that ceiling.

---

## 📁 Repository Structure

```
├── agents/                          # Persona configuration files
│   ├── hannah.json                  # Chief Control Engineer
│   ├── sophie.json                  # Embedded Systems
│   └── ... (8 more personas)
│
├── ollama_agent_orchestrator.py     # 🔑 Main interactive team interface
├── hannah_full_validation.py        # 🧪 15-question benchmark suite
├── hannah_benchmark.py              # Quick 3-question benchmark
├── parallel_agents.py               # Async parallel team brainstorm
├── agent_test_harness.py            # Extended stress testing
│
├── agent_system_prompt.md           # Global team documentation
└── README.md                        # This file
```

---

## ⚙️ Technical Stack

- **LLM Backend:** Ollama (Local/Private)
- **Model:** Qwen 2.5 14B (custom `qwen-64k`)
- **Memory:** RAG-ready session logging
- **Transport:** Zero-dependency `http.client`

---

## 🚀 Quick Start

### 1. Server Setup (Linux machine with GPU)
```bash
# Pull and configure Qwen with 64k context
ollama pull qwen2.5:14b
ollama show qwen2.5:14b --modelfile > Modelfile
echo "PARAMETER num_ctx 65536" >> Modelfile
ollama create qwen-64k -f Modelfile
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

### 2. Client Setup (Your machine)
```bash
git clone https://github.com/rahulsoni0361/qwen-benchmark-control-systems-engineering.git
cd qwen-benchmark-control-systems-engineering

# Update the OLLAMA_IP variable in the .py files to your server IP.
python ollama_agent_orchestrator.py
```

---

## 🤝 Contributing

Pull requests are welcome. If you want to add a new specialist agent (e.g., SIMULINK specialist) or improve the benchmark questions, open an issue!

---

## ⭐ Acknowledgment

Built for engineers who demand more than hallucinated helpfulness. If this helps you, star it.

---

*"The poles don't care about your prompt. But the right prompt forces the model to care about the poles."*
