---
name: auto-orchestrator
description: Orchestrate multi-step research and development workflows automatically. Use when the user asks for complex tasks that require research, planning, coding, and validation in sequence — such as building a new project from scratch, doing a literature review with implementation, or developing an end-to-end feature across multiple files.
---

# Auto-Orchestrator

Use this skill for complex, multi-step requests that blend research, planning, implementation, and validation.

## Workflow

1. **Research**
   - If the topic is new or rapidly evolving, use `exa` web search to gather recent information.
   - Save key findings in the conversation context.

2. **Planning**
   - For non-trivial tasks with multiple milestones or dependencies, use `EnterPlanMode`.
   - If `taskmaster` is available, initialize a task plan and track progress.
   - Present the plan to the user for approval before heavy implementation.

3. **Implementation**
   - Write code with `filesystem` tools.
   - Prototype and validate with `jupyter` when dealing with data, algorithms, or models.
   - Follow the project's existing style and conventions.

4. **Validation**
   - Run code, check outputs, fix errors iteratively.
   - If tests exist, run them and ensure they pass.

5. **Error handling**
   - Log issues briefly.
   - Continue with the next actionable step rather than stopping completely.
