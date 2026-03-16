# Demo Script

## Goal

Record a 3–5 minute video that shows:

1. what the project is
2. how memory is used
3. how memory changes action
4. how the same core supports Agent OS and Life OS

## Suggested flow

### Part 1 — Intro (20–30s)
“Hi, this is TelosCore Agent Twin, a memory-aware long-horizon agent with a built-in Personal Digital Twin mode.”

### Part 2 — Repo overview (20–30s)
Show the repository structure:
- core
- memory
- modes
- api
- demo
- eval

### Part 3 — Agent OS demo (60–90s)
Run:

```bash
python demo/run_agent_demo.py

Explain:

historical conflict memories are retrieved

memory bias raises U_con

action shifts toward patch / clarify / replan instead of naive response

Part 4 — Life OS demo (60–90s)

Run:
Explain:

historical conflict memories are retrieved

memory bias raises U_con

action shifts toward patch / clarify / replan instead of naive response

Part 4 — Life OS demo (60–90s)

Run:

Explain:

same brain

different outward behavior

life conflict becomes reflective planning instead of blind execution

Part 5 — Eval script (30–45s)

Run:
python eval/memory_action_shift.py

Explain:

baseline vs seeded memory

seeded user gets stronger conflict memory bias

memory changes action

Part 6 — Closing (15–20s)

“One core, two modes. Memory does not just store the past — it reshapes the next action.”
