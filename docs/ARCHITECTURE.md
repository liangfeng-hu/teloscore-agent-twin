# Architecture

## Core thesis

TelosCore Agent Twin is built around one claim:

**historical memory changes current action selection**

Instead of using memory as passive retrieval only, the system converts memory hits into energy bias over

\[
U_t = (U_{\mathrm{unc}}, U_{\mathrm{con}}, U_{\mathrm{ent}}, U_{\mathrm{tel}})
\]

Then action is selected from the updated state.

## Main layers

### 1. core/
Computes energy, applies memory bias, and decides the next action.

### 2. memory/
Stores and retrieves event memories through EverMemOS, with a local JSONL fallback.

### 3. modes/
Exposes the same core through two outward behaviors:

- Agent OS
- Life OS / Personal Digital Twin

### 4. agent/
Runs a lightweight multi-step state machine for horizon demos.

## Why two modes share one core

Agent failure and personal inner conflict are both treated as structured deviations:

- task deviation -> higher conflict / uncertainty
- life hesitation -> higher conflict / telos distance

That is why one energy controller can support both.

## Current scope

This repository focuses on Track 1 only:

- long-horizon agent behavior
- personal digital twin mode
- memory-aware action selection

It intentionally does not include browser extension or cross-platform prompt injection.
