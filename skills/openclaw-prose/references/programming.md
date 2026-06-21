---
title: "Programming OpenProse"
summary: ".prose file format, syntax, agents, control flow (parallel / sequential), inputs, context binding"
read_when:
  - Writing a new .prose program
  - Looking up the syntax for parallel, session, context, input, agent declarations
---

# Programming OpenProse

A `.prose` file is a markdown document with structured blocks. The format is designed to be readable as plain prose, with control flow that looks like indented lists and fenced blocks.

## File basics

- File extension: `.prose`
- Encoding: UTF-8 text
- Comments: lines starting with `#`
- Strings: double-quoted, with `{name}` interpolation
- Blocks: indented under a `keyword:` header

## Inputs

Declare program inputs at the top of the file. Each `input` line produces a CLI argument on `/prose run`.

```prose
input topic: "What should we research?"
input severity: "SEV3"      # has a default
input region:               # required, no default
```

Callers pass them as `key=value` on the command line. Inside the program, inputs are referenced as `{topic}`, `{severity}`, etc.

## Agents

Define named agents with a model and a system prompt. Agents are referenced later with `session: <name>`.

```prose
agent researcher:
  model: sonnet
  prompt: "You research thoroughly and cite sources."

agent writer:
  model: opus
  prompt: "You write a concise summary."

agent reviewer:
  model: sonnet
  prompt: "You are a strict code reviewer. Flag issues with severity tags."
```

`model` accepts any model identifier accepted by your providers config. `prompt` is the agent's persistent system prompt.

## Control flow

### Sequential

Statements run in order. The result of each is bound to a name with `=`.

```prose
summary = session: researcher
  prompt: "Research {topic}."

draft = session: writer
  prompt: "Draft a short answer from: {summary}."
```

### Parallel

Use `parallel:` to fan out multiple sessions concurrently.

```prose
parallel:
  findings = session: researcher
    prompt: "Research {topic}."
  draft = session: writer
    prompt: "Draft a summary of {topic}."
  risks = session: reviewer
    prompt: "List the risks of {topic}."
```

The next statement waits for all parallel branches to complete.

### Inline session

A bare `session "..."` block runs once and emits its reply as the program's final output.

```prose
session "Merge the findings + draft into a final answer."
context: { findings, draft }
```

`context:` injects the named bindings into the session's prompt as labeled sections.

## Context binding

`context: { a, b, c }` injects the named bindings into the next session as labeled context blocks. The agent sees:

```text
## a
<contents of a>

## b
<contents of b>

## c
<contents of c>
```

This is the primary mechanism for chaining sub-agents.

## Variables and scope

Bindings created by `name = session: ...` are local to the program. They are persisted in the run's `state.md` and can be inspected after a run.

## String interpolation

Anywhere in a string, `{name}` is replaced with the binding's text output. If `name` is undefined, the program fails at compile time.

```prose
session "You researched {topic} and found {findings}."
```

## Full example

```prose
# research.prose
input topic: "What should we research?"

agent researcher:
  model: sonnet
  prompt: "You research thoroughly and cite sources."

agent writer:
  model: opus
  prompt: "You write a concise summary."

parallel:
  findings = session: researcher
    prompt: "Research {topic}."
  draft = session: writer
    prompt: "Summarize {topic}."

session "Merge the findings + draft into a final answer."
context: { findings, draft }
```

## Validation

Run `/prose compile <file.prose>` to catch syntax errors, undefined agents, missing required inputs, and unbound variable references before executing.

## Style guide

- One agent per role. Prefer a small number of focused agents over one large prompt.
- Name agents by role, not by model. `researcher` not `sonnet-researcher`.
- Use `parallel:` aggressively — concurrent sub-agents are the main cost win.
- Keep `prompt:` strings short and action-oriented. Long prompts go in the agent's `prompt:` block.
- Treat `.prose` files like source code: review before running, version-control them, run `/prose compile` in CI.

## Related

- [Runtime mapping](runtime-mapping.md) — how each construct maps to OpenClaw tools
- [Examples](examples.md) — sample programs
- [Slash command](slash-command.md) — running and compiling programs
