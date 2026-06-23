# ClawDoc — Standalone Agent

**Version:** v1.7.3
**Tracked OpenClaw:** 2026.6.9  
**Template:** agent-template/README.md

---

This directory contains the workspace for a standalone ClawDoc agent.

## What is this?

This agent is running ClawDoc — a dedicated OpenClaw system doctor that knows the entire OpenClaw system inside and out.

## Skills

ClawDoc ships with 24 skills covering:

- **Config** — Gateway config keys, secrets, retry, failover, model routing
- **Memory** — builtin, QMD, Honcho, embeddings, active memory, dreaming
- **Agents** — Multi-agent setup, bindings, sandbox, tool policies
- **Channels** — Discord, Telegram, WhatsApp, Slack, Signal, and 36+ more (41 total)
- **Troubleshooting** — Diagnosis flows, error codes, common fixes
- **Automation** — Cron, hooks, tasks, Task Flow
- **CLI** — Every `openclaw` command with examples
- **Providers** — 50+ model providers: OpenAI, Anthropic, Gemini, Bedrock...
- **Install** — Docker, Railway, Fly, VPS, Raspberry Pi, macOS...

## Updating

To update ClawDoc to the latest release:

```bash
cd /path/to/clawdoc/repo && git pull
cp -r skills/* /home/user/.openclaw/agents/claw-doc/skills/
openclaw skills check --agent claw-doc
```

## Documentation

- [ClawDoc Public Repo](https://github.com/Hashi-Ai-Dev/openclaw-clawdoc)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw Discord](https://discord.com/invite/clawd)