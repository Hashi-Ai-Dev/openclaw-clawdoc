# OpenClaw Master Skill — Overview

This is the top-level entry point for ClawDoc, the OpenClaw configuration expert.

## Skill Architecture

ClawDoc is organized into specialized skills that route based on the task at hand:

| Skill | Domain |
|-------|--------|
| `openclaw-config` | Gateway config, secrets, auth, retry, failover, remote gateways |
| `openclaw-memory` | Memory backends, Honcho, embeddings, active memory, dreaming |
| `openclaw-agents` | Multi-agent, bindings, sandbox, session management |
| `openclaw-channels` | All channel configs (Discord, Telegram, Slack, WhatsApp, etc.) |
| `openclaw-concepts` | Architecture, streaming, queue modes, model failover |
| `openclaw-troubleshooting` | Diagnosis, errors, hooks, ACP, channel failures |
| `openclaw-plugins` | Plugin slots, plugin config, context engine |
| `openclaw-tools` | Tool reference: exec, browser, ACP, lobster, diffs, web |
| `openclaw-cli` | CLI commands: hooks, pairing, cron, ACP, MCP |
| `openclaw-providers` | 43+ model providers, auth profiles, failover |

## How ClawDoc Works

1. **Session startup**: Read `SOUL.md` → `USER.md` → check memory → execute → report
2. **On-demand only**: Wait for Hashi or main agent to call, then execute and report
3. **Anti-hallucination**: Verify against OpenClaw docs or source before claiming a config value
4. **Gateway restart protocol**: NEVER restart without explicit permission

## Key Files

- Config: `/data/.openclaw/openclaw.json`
- Logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- Gateway status: `openclaw status`
- Docs: `/openclaw/docs/`
- Open-source repo: https://github.com/Hashi-Ai-Dev/openclaw-clawdoc

## Source Docs

All reference docs are copied from `/openclaw/docs/` in the OpenClaw source tree.
Run `openclaw skills check` to audit available skills.
