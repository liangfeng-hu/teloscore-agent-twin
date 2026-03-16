# TelosCore Agent Twin

**Memory Genesis Competition 2026 | Track 1: Agent + Memory**

A memory-aware long-horizon agent with built-in Personal Digital Twin mode, powered by EverMemOS.

> **Memory does not just store the past. It reshapes the next action.**

## 1. What this project is

TelosCore Agent Twin is a local-first competition project built on top of **EverMemOS** and a **cognitive energy controller**.

Instead of treating memory as passive retrieval, this project uses a cognitive energy vector

\[
U_t = (U_{\mathrm{unc}}, U_{\mathrm{con}}, U_{\mathrm{ent}}, U_{\mathrm{tel}})
\]

to let retrieved memory actively change the next decision.

The same core supports **two modes**:

- **Agent OS** — a long-horizon autonomous agent for multi-step task execution
- **Life OS** — a Personal Digital Twin mode for goals, habits, conflicts, and self-reflection

This is **one core with two outward behaviors**, not two separate products.

## 2. Why it matters

Most AI systems can retrieve context, but they do not let memory *govern* action selection.

TelosCore Agent Twin is designed to demonstrate a stronger loop:

1. store meaningful events into long-term memory
2. retrieve memory relevant to the current state
3. convert retrieved memory into energy bias
4. shift the next action accordingly

In other words, memory is not an archive here.
It is part of the decision policy.

## 3. How EverMemOS powers this project

EverMemOS is used as the persistent memory substrate.

This project uses EverMemOS for:

- storing state and event memories across sessions
- writing structured events such as conflict, clarify, and goal updates
- retrieving relevant historical memories for the current turn
- feeding retrieval results back into the energy controller

The resulting behavior is **memory-aware**, not purely reactive.

## 4. Core idea

At the center of this repo is a simple claim:

> **historical memory changes current action selection**

The energy controller loads memory bias into the current state, then selects the next action using a policy over the updated energy vector.

Typical behavior examples:

- past conflict retrieved → \(U_{\mathrm{con}}\) rises → next action shifts toward **Patch**
- high uncertainty retrieved → \(U_{\mathrm{unc}}\) rises → next action shifts toward **Clarify**
- goal-aligned memory retrieved → \(U_{\mathrm{tel}}\) drops → next action continues toward execution

## 5. Repo structure

```text
core/      cognitive energy computation + action policy
memory/    EverMemOS client + retrieval + memory bias loading
agent/     long-horizon workflow graph and execution loop
modes/     Agent OS mode and Life OS mode
api/       FastAPI entrypoint

6. Quick start
Step 1: start EverMemOS
git clone https://github.com/EverMind-AI/EverMemOS.git
cd EverMemOS
docker compose up -d

By default, this project expects EverMemOS at:
http://localhost:1995

Step 2: clone this repository
git clone https://github.com/<YOUR_GITHUB_USERNAME>/teloscore-agent-twin.git
cd teloscore-agent-twin
pip install -r requirements.txt

Step 3: configure environment

Create a local .env from .env.example:
cp .env.example .env

Example values:
EVERMEMOS_BASE_URL=http://localhost:1995
APP_HOST=0.0.0.0
APP_PORT=8000
DEFAULT_MODE=agent_os

Step 4: start the API
uvicorn api.app:app --reload --port 8000

7. Run the demos
Agent OS demo
python demo/run_agent_demo.py

Life OS demo
python demo/run_lifeos_demo.py

8. API usage
POST /run

Example request body:
{
  "mode": "agent_os",
  "input": "Plan the next step for a startup project that failed pricing last week."
}

or
{
  "mode": "life_os",
  "input": "I keep delaying an important personal goal and feel conflict about it."
}

9. Evaluation focus

See:
python eval/memory_action_shift.py

This script compares baseline behavior vs memory-biased behavior.

10. What this repo is not

This repository is intentionally focused on Track 1.

It does not include:

browser extension injection

cross-platform prompt middleware

plugin SDK packaging

11. Video demo

Add your 3–5 minute video link here:

Demo Video: <YOUR_VIDEO_URL>

12. Origin and continuity

This repo is a cleaner, competition-focused continuation of the earlier TelosCore Full-Memory Build prototype.

13. License

MIT License

14. Contact

Author: Liangfeng Hu
Project direction: memory-aware cognition, long-horizon agents, personal digital twin systems
demo/      runnable demos for both modes
eval/      reproducible evaluation scripts
tests/     basic tests
