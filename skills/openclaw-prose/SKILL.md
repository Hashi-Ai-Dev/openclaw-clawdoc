---
name: openclaw-prose
description: "OpenProse workflow language for OpenClaw. Use when running the /prose slash command or the open-prose plugin. Canonical docs: docs.openclaw.ai/prose. Triggers on: prose, openprose, /prose, .prose files, prose workflow, multi-agent workflow, parallel agents, agent orchestration."
---

# OpenClaw Prose (OpenProse)

OpenProse is a portable, markdown-first workflow format for orchestrating AI sessions. In OpenClaw it ships as a plugin (`open-prose`) that installs a skill pack and a `/prose` slash command. Programs live in `.prose` files and can spawn multiple sub-agents with explicit control flow.

## Quick start

```bash
# Enable the plugin (bundled, disabled by default) and restart the gateway
openclaw plugins enable open-prose
openclaw gateway restart

# Run a program
/prose run ./research.prose
```

## See upstream

The canonical OpenProse documentation lives in upstream OpenClaw:

- [OpenProse overview](https://docs.openclaw.ai/prose) — `openclaw/docs/prose.md`
- [Open Prose plugin reference](https://docs.openclaw.ai/plugins/reference/open-prose) — `openclaw/docs/plugins/reference/open-prose.md`

This skill is a thin pointer. The bundled reference docs that previously lived at `references/` (install, slash-command, programming, runtime-mapping, state, examples) were dropped in v1.7.10 because their content was not verifiable against the upstream source — the canonical material is in the upstream docs linked above. If you need content that is not yet covered upstream, see the upstream source files directly or open an issue against the ClawDoc repo.