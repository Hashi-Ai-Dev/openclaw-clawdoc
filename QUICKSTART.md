# ClawDoc Quickstart

Get ClawDoc running in under 10 minutes. Choose your install mode first.

---

## Choose Your Mode

| | Mode 1 — Persistent Agent | Mode 2 — Skills Only |
|---|---|---|
| **Creates a new agent?** | ✅ Yes | ❌ No |
| **Best for** | Dedicated system doctor, ongoing maintenance | Quick OpenClaw help, existing agent |
| **Your agent keeps its identity?** | ❌ No (ClawDoc has its own) | ✅ Yes |
| **Guide** | [AGENT_INSTALL.md](./AGENT_INSTALL.md) | [SKILLS_INSTALL.md](./SKILLS_INSTALL.md) |

Not sure? **Start with Mode 2** — it's the lightest path.

---

## Prerequisites (Both Modes)

- OpenClaw installed (`curl -fsSL https://openclaw.ai/install.sh | bash`)
- A model provider account (MiniMax, OpenAI, or any [supported provider](./skills/openclaw-providers/))
- `git` available in your terminal

---

## Mode 1 — Persistent Agent

Full guide: [AGENT_INSTALL.md](./AGENT_INSTALL.md)

Summary:

```bash
# 1. Create dedicated ClawDoc agent
openclaw agents add claw-doc \
  --workspace /home/user/.openclaw/agents/claw-doc \
  --non-interactive

# 2. Install skills
git clone https://github.com/Hashi-Ai-Dev/openclaw-clawdoc.git /tmp/openclaw-clawdoc
cd /tmp/openclaw-clawdoc && git checkout v1.6.0 && cd ..
cp -r /tmp/openclaw-clawdoc/skills/* /home/user/.openclaw/agents/claw-doc/skills/
cp /tmp/openclaw-clawdoc/SOUL.md /home/user/.openclaw/agents/claw-doc/SOUL.md

# 3. Verify
openclaw skills list --agent claw-doc
openclaw skills check --agent claw-doc

# 4. Restart and test
openclaw gateway restart
openclaw doctor --non-interactive
```

---

## Mode 2 — Skills Only

Full guide: [SKILLS_INSTALL.md](./SKILLS_INSTALL.md)

Summary:

```bash
# 1. Clone
git clone https://github.com/Hashi-Ai-Dev/openclaw-clawdoc.git /tmp/openclaw-clawdoc
cd /tmp/openclaw-clawdoc && git checkout v1.6.0 && cd ..

# 2. Find your agent's workspace path
openclaw agents list
# Note the Workspace: path for your agent (e.g. /home/user/.openclaw/agents/main)

# 3. Copy skills into your agent's workspace
cp -r /tmp/openclaw-clawdoc/skills/* /home/user/.openclaw/agents/main/skills/

# 4. Restart and verify
openclaw gateway restart
openclaw skills list
openclaw skills check
openclaw doctor --non-interactive
```

---

## What to Try First

Once installed (either mode), ask ClawDoc your first question:

```
@your-agent How do I configure memory search with embeddings?
```

ClawDoc routes to the right skill, reads the reference docs, and gives you a precise grounded answer.

---

## Common First Tasks

| Task | Example |
|------|---------|
| Configure TTS | `examples/tts-minimax.json` |
| Set up Honcho memory | `examples/memory-honcho.json` |
| Add a second channel | `examples/discord-telegram.json` |
| Lock down an agent | `examples/per-agent-sandbox.json` |

---

## Next Steps

- Browse [`skills/`](./skills/) to see all 22 available skills
- Check [`examples/`](./examples/) for ready-to-use config snippets
- Read [AGENT_INSTALL.md](./AGENT_INSTALL.md) if you want a dedicated ClawDoc agent (Mode 1)
- Read [SKILLS_INSTALL.md](./SKILLS_INSTALL.md) for the skills-only install (Mode 2)
- Read [CONTRIBUTING.md](./CONTRIBUTING.md) if you want to extend or fork ClawDoc