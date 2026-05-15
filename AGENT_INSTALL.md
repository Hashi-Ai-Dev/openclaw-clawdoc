# Install ClawDoc as a Persistent Agent

Create a dedicated, persistent ClawDoc agent with its own workspace and identity. Use this when you want a standalone OpenClaw system doctor that runs continuously and can be addressed directly.

---

## Which mode is this?

**Mode 1 — Persistent Agent** creates a new named OpenClaw agent (`claw-doc` or a name you choose) with its own workspace directory, routing bindings, and ClawDoc skill stack. The agent is fully independent of your existing setup.

For a lighter alternative where no new agent is created, see [SKILLS_INSTALL.md](./SKILLS_INSTALL.md) (Mode 2 — Skills Only).

---

## Prerequisites

- OpenClaw installed (`curl -fsSL https://openclaw.ai/install.sh | bash`)
- A model provider already configured in your gateway (run `openclaw doctor --non-interactive` to verify)

---

## Step 1 — Create the ClawDoc Agent

```bash
# Replace /home/user/.openclaw/agents/claw-doc with your preferred path
openclaw agents add claw-doc \
  --workspace /home/user/.openclaw/agents/claw-doc \
  --non-interactive
```

Verify the agent was created:
```bash
openclaw agents list
```

You should see `claw-doc` in the list with `Routing: default (no explicit rules)`.

---

## Step 2 — Install ClawDoc Skills for the Agent

```bash
# Clone the ClawDoc repo
git clone https://github.com/Hashi-Ai-Dev/openclaw-clawdoc.git /tmp/openclaw-clawdoc

# Stable install (recommended for production):
cd /tmp/openclaw-clawdoc && git checkout v1.6.1 && cd ..

# Bleeding-edge (may include unreleased changes — use at your own risk):
# cd /tmp/openclaw-clawdoc && git checkout master

# Copy skills into the agent's workspace
cp -r /tmp/openclaw-clawdoc/skills/* /home/user/.openclaw/agents/claw-doc/skills/
```

**Set the agent persona** — copy root `SOUL.md` as the agent's persona file:

```bash
cp /tmp/openclaw-clawdoc/SOUL.md /home/user/.openclaw/agents/claw-doc/SOUL.md
```

Verify skills are visible to the agent:

```bash
openclaw skills list --agent claw-doc
openclaw skills check --agent claw-doc
```

---

## Step 3 — Configure Channel Bindings (Optional)

Route a channel to the ClawDoc agent so it can receive messages:

```bash
# Example: route Discord traffic to ClawDoc
openclaw agents bind --agent claw-doc --bind discord

# For a specific Discord account/instance:
openclaw agents bind --agent claw-doc --bind discord:your-account-id

# Route Telegram too:
openclaw agents bind --agent claw-doc --bind telegram
```

Verify bindings:
```bash
openclaw agents bindings --agent claw-doc
```

---

## Step 4 — Set the ClawDoc Identity

```bash
openclaw agents set-identity --agent claw-doc --name "ClawDoc" --emoji "🦞"
```

This sets the agent's display name and emoji in the gateway.

---

## Step 5 — Smoke Test

```bash
openclaw doctor --non-interactive
```

Then send a test message to the bound channel:

```
@ClawDoc How do I configure memory with Honcho?
```

ClawDoc should route to `openclaw-memory`, read the reference docs, and return a precise grounded answer.

---

## Updating ClawDoc

**Stable release update:**

```bash
cd /tmp/openclaw-clawdoc && git fetch --tags
git checkout v1.6.1
cp -r /tmp/openclaw-clawdoc/skills/* /home/user/.openclaw/agents/claw-doc/skills/
cp /tmp/openclaw-clawdoc/SOUL.md /home/user/.openclaw/agents/claw-doc/SOUL.md
openclaw skills check --agent claw-doc
```

**Bleeding-edge update:**

```bash
cd /tmp/openclaw-clawdoc && git checkout master && git pull
cp -r /tmp/openclaw-clawdoc/skills/* /home/user/.openclaw/agents/claw-doc/skills/
cp /tmp/openclaw-clawdoc/SOUL.md /home/user/.openclaw/agents/claw-doc/SOUL.md
openclaw skills check --agent claw-doc
```

---

## Uninstalling Mode 1

```bash
# Remove the agent and its workspace
openclaw agents delete claw-doc --force

# Optionally remove the cloned repo
rm -rf /tmp/openclaw-clawdoc
```

---

## Troubleshooting

**Skills not visible to the agent?**
```bash
openclaw skills list --agent claw-doc
openclaw skills check --agent claw-doc --json
```

**Agent not receiving messages?**
- Check `openclaw agents bindings --agent claw-doc` matches your channel config
- Verify the gateway has the channel enabled: `openclaw channels status`

**Need to start over?**
```bash
openclaw agents delete claw-doc --force
# Then re-run from Step 1
```