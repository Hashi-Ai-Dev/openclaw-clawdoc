---
title: "OpenProse examples"
summary: "Sample .prose programs: parallel research, code review pipeline, incident triage"
read_when:
  - Looking for a starting template
  - Studying common OpenProse patterns
---

# Examples

Three sample programs, each illustrating a different OpenProse pattern. Save any of them as `name.prose` and run with `/prose run name.prose [args]`.

## 1. Parallel research and synthesis

Fan out to multiple sub-agents in parallel, then merge.

```prose
# research.prose
# Run: /prose run research.prose topic="agent orchestration"

input topic: "What should we research?"

agent researcher:
  model: sonnet
  prompt: "You research thoroughly and cite sources."

agent writer:
  model: opus
  prompt: "You write a concise summary."

agent critic:
  model: sonnet
  prompt: "You are a skeptic. Find weaknesses and missing perspectives."

parallel:
  findings = session: researcher
    prompt: "Research {topic}. Cite at least three sources."

  draft = session: writer
    prompt: "Write a 200-word summary of {topic}."

  risks = session: critic
    prompt: "List the top three risks or counter-arguments for {topic}."

session "Merge the research, draft, and critique into a balanced final answer."
context: { findings, draft, risks }
```

**What this demonstrates:** `input` declaration, three named agents with different models, `parallel:` block, `context:` binding for the final merge.

## 2. Code review pipeline

Sequential pipeline with role separation. The reviewer reads, the applier writes.

```prose
# code-review.prose
# Run: /prose run code-review.prose repo=./service branch=main

input repo: "Path to the repository"
input branch: "main"

agent reader:
  model: sonnet
  prompt: "You read code carefully and report findings precisely."
  tools: ["read"]                  # read-only

agent reviewer:
  model: opus
  prompt: |
    You are a strict code reviewer. For each file, list issues with
    severity tags: [BLOCKER], [MAJOR], [MINOR], [NIT]. Be specific
    about line numbers and what to change.
  tools: ["read"]

agent applier:
  model: sonnet
  prompt: "You apply review feedback with minimal, targeted diffs."
  tools: ["read", "edit"]          # read + edit, no shell

diff = session: reader
  prompt: "List the files changed in {repo} on branch {branch}."

review = session: reviewer
  prompt: |
    Review the changes to {repo} on branch {branch}.
    Changed files: {diff}
  context: { diff }

fixes = session: applier
  prompt: |
    Apply the [BLOCKER] and [MAJOR] items from this review.
    Repo: {repo}, branch: {branch}.
    Review: {review}
  context: { review }

session "Summarize the review and the fixes that were applied."
context: { diff, review, fixes }
```

**What this demonstrates:** sequential `session:` chain, agent-level `tools:` allowlist override (read-only reviewer, no-shell applier), `context:` propagation across stages.

## 3. Incident triage

Short, action-oriented workflow that fans out to gather signals, then writes a triage note.

```prose
# incident-triage.prose
# Run: /prose run incident-triage.prose severity=SEV2 service=api

input severity: "SEV3"
input service: "the affected service"

agent oncall:
  model: sonnet
  prompt: |
    You are an on-call engineer. Read logs and metrics carefully.
    Report signal: error rate, p99 latency, recent deploys.

agent historian:
  model: sonnet
  prompt: |
    You remember past incidents. Search memory for similar
    symptoms in {service} and report the most likely root cause.

agent sre:
  model: opus
  prompt: |
    You write a clear, calm incident triage note. One-paragraph
    summary, then bullet points for: signals, hypotheses, next steps.

parallel:
  signals = session: oncall
    prompt: "Report current signals for {service} at {severity}."

  history = session: historian
    prompt: "Find past incidents with similar signals in {service}."

note = session: sre
  prompt: |
    Write the incident triage note for {service} at {severity}.
  context: { signals, history }

session "Post the triage note to the incident channel."
context: { note }
```

**What this demonstrates:** realistic incident-response shape — fan-out for signals, fan-in to a single synthesis, prompt for the final handoff step.

## Running the examples

```bash
# Save any of the above as research.prose, code-review.prose, incident-triage.prose
# Then:

/prose run research.prose topic="memory architectures for AI agents"
/prose run code-review.prose repo=./service branch=feature/foo
/prose run incident-triage.prose severity=SEV1 service=api-gateway
```

Compile first to catch syntax errors before running:

```bash
/prose compile research.prose
```

## Adapting these templates

- **Swap the agents.** Replace the `agent` block definitions with ones that match your domain.
- **Add inputs.** Declare more `input` lines for variables the program needs.
- **Add stages.** Sequential statements are just `name = session: ...` blocks. Add as many as you need.
- **Constrain tools.** Add a `tools:` list to an `agent` block to enforce least-privilege on a sub-agent.

## Related

- [Programming guide](programming.md) — full syntax
- [Runtime mapping](runtime-mapping.md) — tool allowlist requirements
- [Slash command](slash-command.md) — running and compiling
