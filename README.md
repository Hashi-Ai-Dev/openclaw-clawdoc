# ClawDoc — OpenClaw Configuration Expert & System Doctor

[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.4.25-blue?style=flat-square)](https://github.com/openclaw/openclaw) · ![Reference Docs](https://img.shields.io/badge/Reference_Docs-440-green?style=flat-square) · ![Skills](https://img.shields.io/badge/Skills-21-orange?style=flat-square)

<p align="center">
  <img src="assets/clawdoc-banner.jpg" alt="ClawDoc Banner" />
</p>

<p align="center">
  <strong>🔍 ⚙️ 🛠️ The OpenClaw knowledge base agent — open for the community</strong>
</p>

---

## What is ClawDoc?

**ClawDoc** is a specialized OpenClaw agent built to fully understand, audit, patch, fix, and manage any OpenClaw configuration or issue. It owns all things OpenClaw — configuration auditing, plugin integration, performance tuning, troubleshooting, documentation, and agent system design.

**The goal of ClawDoc's existence** is to be the definitive agent for auditing, patching, fixing, and managing any OpenClaw config or issue — precise, thorough, and always grounded in the actual OpenClaw docs and source.

> [!NOTE]
> **ClawDoc is an independent community project.** It is not affiliated with or endorsed by OpenClaw. It is a knowledge-base agent built from the public OpenClaw documentation to help operators troubleshoot and configure OpenClaw.

> [!TIP]
> ClawDoc is designed to be **precise over speed** and **clarity over jargon**. Every fix, audit, and explanation is documented with before/after diffs and exact references to the OpenClaw docs.

> [!NOTE]
> **New here?** Start with [QUICKSTART.md](./QUICKSTART.md) — get running in 10 minutes.

---

## Features

- **21 specialized skills** covering every OpenClaw subsystem
- **440 reference docs** copied from the official OpenClaw documentation
- **13 ready-to-use config examples** — TTS, memory, multi-channel, sandboxing, webhooks
- **467 total files** — complete knowledge base ready to run
- **Progressive disclosure design** — lean SKILL.md bodies, deep reference files
- **Built-in diagnostics** — triage → skill routing → detailed fix
- **Community-ready** — MIT licensed, fork it, customize it, ship your own variant

---

## Skill Tree

| Skill | What it does |
|-------|-------------|
| `openclaw-master` | Top-level routing — maps issues to the right skill |
| `openclaw-config` | Gateway config reference, all keys, common patterns |
| `openclaw-memory` | Memory backends (builtin/QMD/Honcho), embeddings, citations |
| `openclaw-agents` | Multi-agent setup, bindings, sandbox, tool policies |
| `openclaw-channels` | All 31 channel types: Discord, Telegram, WhatsApp, Slack, Signal, Matrix, iMessage, IRC, Feishu, LINE, GoogleChat, Mattermost, Microsoft Teams, Nextcloud Talk, Nostr, QQ Bot, Synology Chat, Twitch, Tlon, Zalo, Voice Call |
| `openclaw-concepts` | Architecture, session, compaction, streaming, bootstrap |
| `openclaw-troubleshooting` | Diagnosis flows, error codes, common fixes |
| `openclaw-plugins` | Plugin slots, SDK, hook system, installing plugins |
| `openclaw-tools` | Tool reference: exec, browser, cron, sessions, subagents, gateway |
| `openclaw-cli` | CLI commands: status, gateway, plugins, memory, agents |
| `openclaw-providers` | All 50 model providers: OpenAI, Anthropic, Gemini, Bedrock, Ollama, Groq, DeepSeek, Mistral, and 42 more |
| `openclaw-automation` | Cron, hooks, tasks, Task Flow, standing orders |
| `openclaw-install` | Install guides: Docker, Railway, Fly, Raspberry Pi, DigitalOcean, Hostinger |
| `openclaw-start` | First-run wizard, onboarding flow, getting started |
| `openclaw-help` | FAQ, help commands, usage patterns |
| `openclaw-nodes` | Mobile/desktop node pairing, routing, device management |
| `openclaw-platforms` | Platform-specific setup notes |
| `openclaw-logging` | Logging configuration, log management |
| `openclaw-ci` | CI/CD integration, webhook automation |
| `openclaw-web` | Web UI, dashboard, TUI, webchat |

Each skill lives in its own directory:

```
skill-name/
├── SKILL.md           # Required — trigger conditions + reference summary
└── references/        # Deep-dive docs from OpenClaw source
    ├── deep-topic.md
    └── config-ref.md
```

---

## Quick Start

> ⚡ **10-minute setup:** follow [QUICKSTART.md](./QUICKSTART.md) for the essential install → model → channel → verify path.

### Install ClawDoc

Give your OpenClaw agent the repo URL and let it do the rest:

> **"Install ClawDoc from `https://github.com/Hashi-Ai-Dev/openclaw-clawdoc`"**

Your agent reads the repo, picks up all 21 skills, and ClawDoc is live. That's it.

Or do it manually:

```bash
# Clone into your OpenClaw skills directory
git clone https://github.com/Hashi-Ai-Dev/openclaw-clawdoc.git ~/.openclaw/skills/openclaw

# Or copy individual skill directories you need
cp -r skills/openclaw-master/ ~/.openclaw/skills/
cp -r skills/openclaw-config/ ~/.openclaw/skills/
# ... etc
```

### Use ClawDoc

```
@your-agent [your OpenClaw config question]
```

ClawDoc will route to the right skill, read the relevant reference docs, and give you a precise answer grounded in the actual OpenClaw schema.

---

## Repository Structure

```
openclaw-clawdoc/
├── README.md              # This file
├── LICENSE               # MIT
├── CONTRIBUTING.md       # How to contribute
├── QUICKSTART.md         # Start here — 10 min to running
├── TROUBLESHOOTING.md    # Quick triage front door
├── AUDIT.md              # Config audit report template
├── SECURITY.md           # Security policy
├── assets/
│   ├── avatar.svg
│   └── clawdoc-banner.jpg
├── examples/             # 13 ready-to-use config examples
│   ├── README.md         # Guide to picking the right example
│   ├── discord-single.json
│   ├── discord-full.json
│   ├── discord-telegram.json
│   ├── tts-minimax.json
│   ├── memory-builtin.json
│   ├── memory-honcho.json
│   ├── memory-qmd.json
│   ├── multi-agent-discord.json
│   ├── per-agent-sandbox.json
│   ├── webhook-basic.json
│   └── install-verify.json
└── skills/              # 21 skills total
    ├── openclaw-master/
    ├── openclaw-config/
    ├── openclaw-memory/
    ├── openclaw-agents/
    ├── openclaw-channels/
    ├── openclaw-concepts/
    ├── openclaw-troubleshooting/
    ├── openclaw-plugins/
    ├── openclaw-tools/
    ├── openclaw-cli/
    ├── openclaw-providers/
    ├── openclaw-automation/
    ├── openclaw-install/
    ├── openclaw-start/
    ├── openclaw-help/
    ├── openclaw-nodes/
    ├── openclaw-platforms/
    ├── openclaw-logging/
    ├── openclaw-ci/
    └── openclaw-web/
```

---

## Community

- **Docs:** https://docs.openclaw.ai
- **Discord:** https://discord.com/invite/clawd
- **ClawHub:** https://clawhub.ai (find new skills)
- **Source:** https://github.com/openclaw/openclaw

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for conventions, style guide, and how to add new skills or reference docs.

---

## Philosophy

- **Precision over speed** — Config work requires exactness. Quote the schema, cite the docs, show the exact patch.
- **No hand-waving** — If I'm not sure, I say so and investigate rather than guess.
- **Show your work** — When auditing or fixing, show the before/after diff so it's learnable.
- **Community-minded** — This agent is open-sourced. Design for clarity and generalizability.
