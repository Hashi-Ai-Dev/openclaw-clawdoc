# Install ClawDoc Skills Only

Add ClawDoc's skill tree to an existing OpenClaw agent without creating a new agent or changing your current setup. Use this when you want ClawDoc's OpenClaw expertise in your existing agent, with your existing identity intact.

---

## Which mode is this?

**Mode 2 — Skills Only** copies ClawDoc's public skills into your current agent's workspace. No new agent is created, no new workspace, no routing changes. Your host agent keeps its name, identity, and memory.

For a dedicated standalone agent with its own identity, see [AGENT_INSTALL.md](./AGENT_INSTALL.md) (Mode 1 — Persistent Agent).

---

## Prerequisites

- An existing OpenClaw agent with a configured model
- `git` available in your terminal

---

## Step 1 — Clone the ClawDoc Repo

```bash
git clone https://github.com/Hashi-Ai-Dev/openclaw-clawdoc.git /tmp/openclaw-clawdoc

# Stable install (recommended for production):
cd /tmp/openclaw-clawdoc && git checkout v1.6.1 && cd ..

# Bleeding-edge (may include unreleased changes — use at your own risk):
# cd /tmp/openclaw-clawdoc && git checkout master
```

---

## Step 2 — Install Skills into Your Agent

First, identify your agent's workspace path:

```bash
openclaw agents list
```

Look for your agent's `Workspace:` path (e.g. `/home/user/.openclaw/agents/main`).

Then copy the skills:

```bash
# Replace with your actual agent workspace path
cp -r /tmp/openclaw-clawdoc/skills/* /home/user/.openclaw/agents/main/skills/
```

---

## Step 3 — Verify

```bash
openclaw skills list
openclaw skills check
```

You should see `openclaw-master`, `openclaw-config`, `openclaw-memory`, `openclaw-troubleshooting`, and the other ClawDoc skills in the list.

Restart the gateway to pick up the new skills:
```bash
openclaw gateway restart
```

---

## Step 4 — Smoke Test

```bash
openclaw doctor --non-interactive
```

Send a test message to your agent:

```
How do I enable memory search with embeddings?
```

ClawDoc should route to the right skill and answer with grounded references to the OpenClaw docs.

---

## What You Get with Mode 2

| | Mode 1 — Persistent Agent | Mode 2 — Skills Only |
|---|---|---|
| New agent created | ✅ | ❌ |
| Separate workspace | ✅ | ❌ |
| Dedicated ClawDoc identity | ✅ | ❌ |
| Your existing agent keeps control | — | ✅ |
| Skills available immediately | ✅ | ✅ |
| Requires gateway restart | Yes | Yes |

---

## Updating ClawDoc Skills

```bash
cd /tmp/openclaw-clawdoc && git pull
cp -r /tmp/openclaw-clawdoc/skills/* /home/user/.openclaw/agents/main/skills/
openclaw gateway restart
openclaw skills check
```

---

## Uninstalling Mode 2

Remove the copied skills from your agent's workspace:

```bash
# List the skills that came from ClawDoc
ls /home/user/.openclaw/agents/main/skills/

# Remove them (adjust names as needed)
rm -rf /home/user/.openclaw/agents/main/skills/openclaw-master
rm -rf /home/user/.openclaw/agents/main/skills/openclaw-config
# ... (remove other openclaw-* skills)

# Restart the gateway
openclaw gateway restart
```

> Note: This only removes the ClawDoc skills. Your agent and its configuration are unchanged.

---

## Troubleshooting

**Skills not showing up?**
```bash
openclaw skills list
openclaw skills check --json
```

**Gateway not restarting?**
```bash
openclaw gateway status
```

**Want to switch to Mode 1 later?**
See [AGENT_INSTALL.md](./AGENT_INSTALL.md) — Mode 1 and Mode 2 are independent. You can run both simultaneously with different agents.