# ClawDoc — OpenClaw Configuration Expert & System Doctor

<p align="center">
  <strong>🔍 ⚙️ 🛠️ The OpenClaw knowledge base agent — open for the community</strong>
</p>

<p align="center">
  <img src="assets/avatar.svg" width="128" alt="ClawDoc Avatar" />
</p>

---

## What is ClawDoc?

**ClawDoc** is a specialized OpenClaw agent built to fully understand, efficiently audit, patch, fix, change, and manage any OpenClaw configuration or issue. It owns all things OpenClaw — configuration auditing, plugin integration, performance tuning, troubleshooting, documentation, and agent system design.

**The goal of ClawDoc's existence** is to be the definitive agent for auditing, patching, fixing, and managing any OpenClaw config or issue — precise, thorough, and always grounded in the actual OpenClaw docs and source.

> [!TIP]
> ClawDoc is designed to be **precise over speed** and **clarity over jargon**. Every fix, audit, and explanation is documented with before/after diffs and exact references to the OpenClaw docs.

---

## Features

- **11 specialized skills** covering every OpenClaw subsystem
- **55 reference docs** copied from the official OpenClaw documentation
- **Progressive disclosure design** — lean SKILL.md bodies, deep reference files
- **Built-in diagnostics** — triage → skill routing → detailed fix
- **Community-ready** — fork it, customize it, ship your own variant

---

## Skill Tree

| Skill | What it does |
|-------|-------------|
| `openclaw-master` | Top-level routing — maps issues to the right skill |
| `openclaw-config` | Gateway config reference, all keys, common patterns |
| `openclaw-memory` | Memory backends (builtin/QMD/Honcho), embeddings |
| `openclaw-agents` | Multi-agent setup, bindings, sandbox, tool policies |
| `openclaw-channels` | Discord, Telegram, WhatsApp, Slack, Signal, Matrix, iMessage |
| `openclaw-concepts` | Architecture, session, compaction, streaming, bootstrap |
| `openclaw-troubleshooting` | Diagnosis flows, error codes, common fixes |
| `openclaw-plugins` | Plugin slots, installing plugins, plugin config |
| `openclaw-tools` | Tool reference: exec, browser, cron, sessions, subagents |
| `openclaw-cli` | CLI commands: status, gateway, plugins, memory, agents |
| `openclaw-providers` | Model providers: OpenAI, Anthropic, Gemini, Bedrock, Ollama |

Each skill lives in its own directory with:
- `SKILL.md` — triggering conditions + lean reference
- `references/` — full doc copies from `/openclaw/docs/`

---

## Quick Start

### 1. Install ClawDoc's skills

Copy the `skills/` folder into your OpenClaw workspace:

```bash
# Your OpenClaw workspace skills directory
cp -r skills/ ~/.openclaw/skills/clawdoc/

# Or alongside your project skills
cp -r skills/ /path/to/your/project/skills/
```

### 2. Reference from your agent

In your agent's `AGENTS.md` or `SOUL.md`, load the master skill:

```
Load skill: openclaw-master (or path/to/openclaw-master/SKILL.md)
```

### 3. Ask ClawDoc anything

```
@your-agent How do I set up multi-agent routing with Discord bindings?
@your-agent My Honcho memory plugin won't load — getting "plugin disabled (memory slot)" error
@your-agent audit my openclaw.json config
```

---

## Architecture

```
openclaw-clawdoc/
├── SKILL.md                   # This file
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── skills/                    # All 11 skills
│   ├── openclaw-master/       # Top-level router
│   ├── openclaw-config/       # Config reference
│   ├── openclaw-memory/       # Memory + embeddings
│   ├── openclaw-agents/       # Multi-agent
│   ├── openclaw-channels/     # Channels
│   ├── openclaw-concepts/     # Concepts
│   ├── openclaw-troubleshooting/
│   ├── openclaw-plugins/      # Plugin system
│   ├── openclaw-tools/        # Tools
│   ├── openclaw-cli/         # CLI
│   └── openclaw-providers/   # Model providers
├── scripts/                   # Helper scripts
├── examples/                  # Config examples
└── assets/                    # Avatar, logos
```

---

## Config Examples

See `examples/` for ready-to-paste config snippets:

- `examples/honcho-memory.json` — Enable Honcho as memory backend
- `examples/multi-agent-discord.json` — Multi-agent + Discord bindings
- `examples/memory-qmd.json` — QMD memory backend config
- `examples/per-agent-sandbox.json` — Per-agent sandbox + tool policies

---

## ClawDoc's Memory (MEMORY.md)

ClawDoc maintains long-term memory at `MEMORY.md` (in its workspace). Key learned patterns:

- **Honcho slot fix**: `plugins.slots.memory = "openclaw-honcho"` (not `memory.backend`)
- **Gateway restart rule**: Only restart for `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*`
- **Valid embedding providers**: `local`, `openai`, `gemini`, `voyage`, `mistral`, `bedrock` — OpenRouter is NOT valid
- **Discord binding format**: `guildId/channelId` (not just channel ID)

---

## Community

- **OpenClaw Docs**: https://docs.openclaw.ai
- **OpenClaw GitHub**: https://github.com/openclaw/openclaw
- **OpenClaw Discord**: https://discord.com/invite/clawd
- **ClawHub** (skill registry): https://clawhub.ai

---

## Forking / Extending

ClawDoc is built as a standard OpenClaw skill package. To create your own variant:

1. Copy the `skills/` directory
2. Edit SKILL.md frontmatter `name` and `description` for your agent
3. Customize the skill bodies and reference docs
4. Share with the community via ClawHub

See `CONTRIBUTING.md` for conventions and the skill creator guide.

---

## License

MIT — see `LICENSE`. ClawDoc is free for the community to use, fork, and extend.
