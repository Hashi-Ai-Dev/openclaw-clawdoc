# Examples

Ready-to-use config snippets. Apply with `openclaw config merge examples/NAME.json`, then restart the gateway.

## Quick picker

**I just installed OpenClaw and want to verify it works**
→ `install-verify.json`

**I want Discord on a single server, no frills**
→ `discord-single.json`

**I want a full-featured Discord setup with threads and exec approvals**
→ `discord-full.json`

**I want Discord and Telegram running together**
→ `discord-telegram.json`

**I want my agent to speak with voice on Discord/Telegram/WhatsApp**
→ `tts-minimax.json`

**I want my agent to remember context across conversations (builtin memory)**
→ `memory-builtin.json`

**I want semantic search over my own notes and files (QMD)**
→ `memory-qmd.json`

**I want full memory with external search (Honcho/PostgreSQL)**
→ `memory-honcho.json`

**I want different agents for different Discord channels**
→ `multi-agent-discord.json`

**I want to lock down an agent so it can't run dangerous tools**
→ `per-agent-sandbox.json`

---

## Applying an example

```bash
# Review first
cat examples/NAME.json

# Apply to your config
openclaw config merge examples/NAME.json

# Restart to pick up changes
openclaw gateway restart

# Verify it applied
openclaw config get
```

## Beginner path

For your first OpenClaw setup:

```
1. install-verify.json     → confirm install works
2. discord-single.json      → add Discord channel
3. memory-builtin.json     → enable conversation memory
```

That's a working bot in 3 steps.

## All files

| File | What it does |
|------|-------------|
| `install-verify.json` | Minimal model config to verify install |
| `discord-single.json` | Single-server Discord, simple setup |
| `discord-full.json` | Multi-server Discord, exec approvals, threads |
| `discord-telegram.json` | Discord + Telegram side-by-side |
| `tts-minimax.json` | MiniMax voice output (TTS) |
| `memory-builtin.json` | Builtin memory with semantic search |
| `memory-qmd.json` | QMD memory over local files |
| `memory-honcho.json` | Honcho/PostgreSQL memory backend |
| `multi-agent-discord.json` | Route tasks to different agents via Discord |
| `per-agent-sandbox.json` | Sandboxed agent profiles |
| `webhook-basic.json` | Receive webhook events from external services |
