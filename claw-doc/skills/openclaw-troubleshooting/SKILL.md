---
name: openclaw-troubleshooting
description: OpenClaw troubleshooting and fixes. Use when diagnosing gateway crashes, config errors that other skills can't resolve, plugin conflicts after config checks pass, ACP agent failures, pairing/device pairing, hook not firing, lock file issues, secret resolution failures, or queue/backpressure problems. Triggers on: "gateway crash", "config error", "crash", "debug", "troubleshoot", "pairing", "device pairing", "hook failure", "lock file", "queue", "backpressure", "secret not resolving", "plugin conflict", "openclaw doctor", "gateway locked", " ACP agent won't start", "channel silent", "hook not firing".
---

# OpenClaw Troubleshooting

## ⚠️ Never Do These

- **Never `rm /tmp/openclaw.lock` while the gateway process is still running.** Check `ps aux | grep openclaw-gateway` first — a stale lock file is only safe to delete if the process is confirmed dead.
- **Never restart the gateway without checking the session queue.** Run `openclaw status` and `openclaw doctor` first — a restart mid-queue drops pending messages.
- **Never confuse `openclaw pairing` with `openclaw devices`.** `openclaw pairing` is for channel pairing (Discord DMs, WhatsApp, etc.). `openclaw devices` is for node/device pairing. Using the wrong command will not resolve your issue.
- **Never leave `plugins.slots.memory` at default when using Honcho** — if Honcho is your memory backend, you MUST set `plugins.slots.memory = "openclaw-honcho"`. Leaving it at default (`memory-core`) causes Honcho to fail silently.
- **Never assume a config change took effect without a restart.** Keys that require restart: `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*`. Keys that are dynamic (no restart): `tools.web.search.apiKey`, `agents.defaults.memorySearch.remote`.

## Quick diagnostics

```bash
openclaw status                        # gateway health
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log   # recent logs
ps aux | grep openclaw-gateway | grep -v grep            # is it running?
python3 -m json.tool ~/.openclaw/openclaw.json > /dev/null && echo "valid"  # config valid
curl -s http://127.0.0.1:18789/ -o /dev/null -w "%{http_code}"  # HTTP health
openclaw doctor                        # diagnose + auto-fix
openclaw doctor --fix
```

## Decision tree (action-first order)

**Step 1 — Is the gateway running?**
```bash
ps aux | grep openclaw-gateway | grep -v grep
curl -s http://127.0.0.1:18789/ -o /dev/null -w "%{http_code}"
```
- If not running and won't start → check lock file (see Lock file stale below)
- If running but unresponsive → check logs

**Step 2 — Is it a plugin issue?**
```bash
openclaw plugins list
```
- Missing from list → check `plugins.allow`
- Listed but disabled → check `plugins.entries[<id>].enabled`
- Config validation error → check `openclaw.plugin.json` manifest

**Step 3 — Is it a memory/search issue?**
```bash
openclaw memory status
openclaw memory index --force   # rebuild index if stale
```

**Step 4 — Is it a channel issue?**
```bash
openclaw channels status --probe
openclaw doctor
```

**Step 5 — Is it an ACP agent issue?**
```bash
/acp doctor
/acp status
```

**Step 6 — Is it a hook issue?**
```bash
openclaw hooks list
openclaw hooks info HOOK_NAME
```

**Step 7 — Is it an auth/credential issue?**
Search logs for `auth`, `credential`, or `429`.

---

## Common issues by category

### Installation

**`openclaw: command not found` after install**
OpenClaw installs to non-standard npm paths. Find the binary first:
```bash
find ~ -name openclaw -type f 2>/dev/null
```
Then add to PATH:
```bash
export PATH="/FULL/PATH/FOUND/bin:$PATH"
echo 'export PATH="/FULL/PATH/FOUND/bin:$PATH"' >> ~/.bashrc
```

**Installer wizard crashes (TypeError: Cannot read properties of undefined)**
Clicking "Skip for now" on the channel selection step causes a crash. Workarounds:
1. Select any channel (even unused) instead of skipping
2. Or skip the wizard entirely:
```bash
OPENCLAW_NO_ONBOARD=1 curl -fsSL https://openclaw.ai/install.sh | bash
```
Then configure manually with `openclaw config set ...`

**After wizardless install, configure model + channel:**
```bash
openclaw config set agents.defaults.model.primary "google/gemini-2.5-flash"
openclaw config set auth.profiles.google.provider "google"
openclaw config set channels.discord.token "YOUR_BOT_TOKEN"
openclaw config set channels.discord.enabled true
openclaw gateway start
```

### Gateway startup

**"Port already in use"**
- Gateway is already running. Don't restart. Verify:
```bash
ps aux | grep openclaw-gateway
```

**Lock file stale (gateway won't start)**
```bash
cat /tmp/openclaw.lock
ps aux | grep openclaw-gateway | grep -v grep   # must return EMPTY before proceeding
# Only run the next line if the process is truly dead:
rm /tmp/openclaw.lock
openclaw gateway start
```

**Never delete the lock file while the gateway process is alive.** The lock file prevents two gateway instances from starting. If you delete it with the process still running, you'll create a race condition on next start.

**Config JSON invalid**
```bash
python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null
```

### Memory

**"plugin disabled (memory slot set to X)"**
- Memory slot misconfiguration. Check what is in `plugins.slots.memory`.
- If using Honcho: **set `plugins.slots.memory = "openclaw-honcho"`** and restart gateway. This is required for Honcho to own the memory slot.
- If switching to builtin/QMD: set `plugins.slots.memory = "memory-core"` and restart gateway.

**Embedding 404**
- `memorySearch.remote.baseUrl` wrong OR invalid provider
- Valid providers: `local`, `openai`, `gemini`, `voyage`, `mistral`, `bedrock`
- OpenRouter is NOT a valid embedding provider

**Memory search stale results**
```bash
openclaw memory index --force   # rebuild index
openclaw memory status          # check provider health
```

**Honcho not responding**
```bash
openclaw honcho status
# Verify baseUrl = http://127.0.0.1:8000 for self-hosted
```

### Plugins

**Plugin not loading**
```bash
openclaw plugins list
# Missing from list → check plugins.allow:
plugins: { allow: ["plugin-id", "@scope/plugin-name"] }
# Bundled plugins are always allowed:
# discord, minimax, browser, active-memory, brave, diffs, llm-task, lobster, memory-core
```

**Config change not taking effect**
Requires gateway restart: `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*`
Dynamic (no restart): `tools.web.search.apiKey`, `agents.defaults.memorySearch.remote`

### Channels

**Discord bot online but won't respond**
1. Token valid? `channels.discord.token`
2. `dmPolicy: "pairing"` → approve your Discord ID via pairing flow
3. **Message Content Intent** must be enabled in Discord Developer Portal
4. `guilds` configured → check `requireMention` for the channel
5. Verify transport:
```bash
openclaw channels status --probe
```

**Discord binding format wrong**
- Format: `guildId/channelId` e.g. `"1483508270344966247/1493571227963363481"`

**Telegram group silent**
1. Disable privacy mode for groups (bot privacy mode = can't read group messages)
2. Check `groups` config for `requireMention: false`
3. Forum topics: Telegram embeds `:topic:<topicId>` in the group key

**WhatsApp random disconnects**
```bash
openclaw channels status --probe
openclaw channels login --channel whatsapp --account personal  # re-login
```

**Pairing code expired/not working**
- Codes expire after **1 hour**
- Max **3 pending** pairing requests per channel
```bash
openclaw pairing list <channel>
openclaw pairing approve <channel> <CODE>
```

### Auth + secrets

**SecretRef unresolved at startup**
- `secret:` reference points to non-existent credential
- Check `~/.openclaw/credentials/` for the secret file
- Test with plaintext key temporarily to isolate the issue

**Anthropic 429 on long context**
- Model has `context1m: true` but credential isn't eligible
- Fix: disable `context1m`, use eligible credential, or add fallback models

### Hooks

**Hook not firing**
```bash
openclaw hooks list
openclaw hooks info HOOK_NAME     # check if enabled
openclaw hooks enable HOOK_NAME   # enable if disabled
```
Hook events: `command:new`, `command:reset`, `command:stop`, `session:compact:before/after`, `agent:bootstrap`, `gateway:startup`, `message:received`, `message:preprocessed`, `message:sent`, `session:patch`

**Hook writing error** — hooks are directories with `script.sh` + `hook.json`:
```
~/.openclaw/hooks/<hook-name>/
  hook.json   # { "event": "...", "filter": {...} }
  script.sh   # executable script
```

### ACP agents

**ACP agent not spawning**
```bash
/acp doctor                   # check readiness
/acp spawn codex --bind here  # first spawn fetches adapter
```
- ACP uses bundled `acpx` runtime plugin (enabled by default on fresh installs)
- Harness adapter cached on first spawn

**ACP agent hanging or unresponsive**
```bash
/acp cancel       # stop current turn
/acp close        # close session + remove bindings
/acp status       # check runtime state
```

### Session + queue

**Session confusion / wrong context**
```json5
session: { scope: "per-sender", dmScope: "main" }
```
- `dmScope: "main"` collapses all DMs to one session key
- `scope: "per-sender"` isolates each sender

**Queue not draining / messages stacked up**
- Check `messages.queue.mode`: `collect` (default) coalesces all queued into one followup
- `steer` injects immediately; `followup` enqueues after current run
- `maxConcurrent` may be capping parallelism:
```json5
agents: { defaults: { maxConcurrent: 4 } }
```

**Message debounce batching unexpectedly**
- `debounceMs` batches rapid consecutive messages from same sender
- Check `messages.queue.debounceMs` config

### ACP + pairing

**Pairing code expired**
- 1-hour expiry, 3 pending max per channel

**Node device pairing fails — this is the #1 confusion point**
```bash
# Check paired devices:
openclaw devices list

# Approve a device pairing request:
openclaw devices approve <requestId>
# ^^^ NOT "openclaw pairing approve" — that command is for channel pairing
```

**Rule of thumb:**
- `openclaw pairing *` → channel pairing (Discord DMs, WhatsApp, Telegram — linking your account to the bot)
- `openclaw devices *` → node/device pairing (linking a client node to the gateway)

If your issue is "my phone/desktop client won't connect to the gateway", you need `openclaw devices`, not `openclaw pairing`. Pairing codes expire after 1 hour and max 3 are pending per channel.

---

## Log file guide

| Situation | Search term |
|----------|-------------|
| Gateway crashes | (check full log) |
| Plugin issues | plugin name |
| Memory/embedding | `memory` or `embedding` |
| Channel problems | channel name |
| Auth/credential | `auth` or `credential` |
| ACP issues | `acp` or `acpx` |
| Hook problems | `hook` |
| Rate limits | `429` or `rate_limit` |
| Session routing | `session` or `routing` |

---

## References

- `references/troubleshooting-flow.md` — visual decision tree (98 lines)
- `references/gateway-troubleshooting.md` — deep gateway runbook (506 lines)
- `references/channel-troubleshooting.md` — per-channel failure signatures (133 lines)
- `references/hooks.md` — hook writing guide, events, structure (319 lines)
- `references/automation-troubleshooting.md` — cron/webhook/CRP issues (8 lines)
