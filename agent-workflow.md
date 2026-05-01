# Agent Workflow: Credit Card Fraud Detection

This project follows the strict anti-slop agent workflow. Any AI agent (or human) contributing to this repository must adhere to the RPI protocol, obey the quality gates, and maintain context discipline.

## 1. RPI Protocol

All multi-file or complex features must be implemented in three distinct phases, using separate context windows (separate agent sessions) to stay in the "smart zone".

- **Research Phase**: Read-only exploration. The agent explores the codebase, finds relevant files, and understands patterns. **No code modification allowed.** Output must be a summary document.
- **Plan Phase**: Design-only. A fresh agent reads the research summary and designs the implementation step-by-step. Output must be a plan document containing exact file paths and snippets.
- **Implement Phase**: Execute-only. A fresh agent follows the plan. No improvisation. If unexpected issues arise, the agent must stop and return to the planning phase.

## 2. Quality Gates

We enforce a strict "Pit of Success". It is impossible to commit slop.

- **Testing**: `pytest --strict-markers -x`. We target 100% passing tests. No known failures, no skipping.
- **Linting**: `ruff`. Configured in `pyproject.toml`. We enforce strict rules including `E, F, I, N, UP, B, A, SIM, TCH` and zero warnings.
- **Type Checking**: `mypy`. Configured in `pyproject.toml`. All public function signatures must have type annotations (`disallow_untyped_defs = true`).
- **Pre-commit**: Configured in `.pre-commit-config.yaml`. All gates run locally before every commit.

## 3. Agent Isolation

To prevent race conditions and cross-agent context contamination:

- **Branching strategy**: Feature branch workflows (e.g., `feature/agent-x-auth`).
- **Worktree usage**: Multi-agent sessions must use isolated `git worktree` directories.
  - Setup: `git worktree add ../agent-feature-x -b feature-x`
- **Hard blocks**: 
  - Never `git push --force`.
  - Never bypass pre-commit hooks (`--no-verify`).
  - Implement agents cannot push directly to `main`.
- **Traceability**: Commit messages must prefix the agent or phase, e.g., `[Agent:Implement] Add robust scaler`.

## 4. Anti-Slop Checklist

Before declaring a task "done", verify:
- [ ] All tests passing locally (100%, no skips)
- [ ] Strict linting enabled (zero warnings)
- [ ] Type checking passing
- [ ] Pre-commit hooks executed successfully
- [ ] No force pushes allowed
- [ ] Plans were reviewed by a human *before* implementation
- [ ] Research docs explicitly reference exact file paths

> If an agent produces bad code, do not try to prompt it to fix it. Diagnose the root cause (bad prompt, missing context), fix the cause, and run a fresh agent. Patching slop creates a debt spiral!
