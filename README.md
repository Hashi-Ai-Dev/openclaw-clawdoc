# ClawDoc — OpenClaw Configuration Expert & System Doctor

<p align="center">
  <strong>🔍 ⚙️ 🛠️ The OpenClaw knowledge base agent — open for the community</strong>
</p>

<p align="center">
  <img src="assets/avatar.svg" width="128" alt="ClawDoc Avatar" />
</p>

---

## What is ClawDoc?

**ClawDoc** is a specialized OpenClaw agent built to fully understand, audit, patch, fix, and manage any OpenClaw configuration or issue. It owns all things OpenClaw — configuration auditing, plugin integration, performance tuning, troubleshooting, documentation, and agent system design.

**The goal of ClawDoc's existence** is to be the definitive agent for auditing, patching, fixing, and managing any OpenClaw config or issue — precise, thorough, and always grounded in the actual OpenClaw docs and source.

> [!TIP]
> ClawDoc is designed to be **precise over speed** and **clarity over jargon**. Every fix, audit, and explanation is documented with before/after diffs and exact references to the OpenClaw docs.

---

## Features

- **11 specialized skills** covering every OpenClaw subsystem
- **297 reference docs** copied from the official OpenClaw documentation
- **315 total files** — complete knowledge base ready to run
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

### Run ClawDoc
```bash
# Point OpenClaw at this directory as the skills root
openclaw skills add /path/to/clawdoc/skills

# Or copy skills into your OpenClaw workspace
cp -r skills/* ~/.openclaw/skills/
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
├── README.md          # This file
├── LICENSE            # MIT
├── CONTRIBUTING.md    # How to contribute
├── AUDIT.md           # Config audit report template
├── assets/
│   └── avatar.svg    # ClawDoc avatar
├── examples/
│   ├── discord-full.json
│   ├── honcho-memory.json
│   ├── multi-agent-discord.json
│   └── per-agent-sandbox.json
└── skills/
    ├── openclaw-master/
    ├── openclaw-config/
    ├── openclaw-memory/
    └── ... (11 skills total)
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
