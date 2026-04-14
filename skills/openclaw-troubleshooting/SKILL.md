---
name: openclaw-troubleshooting
description: OpenClaw troubleshooting and fixes. Use when diagnosing memory issues, channel problems, gateway crashes, config errors, plugin conflicts, ACP agents, pairing issues, hook failures, queue problems, or secret resolution. Triggers on: "broken", "not working", "error", "crash", "debug", "fix", "issue", "problem", "troubleshoot", "pairing", "ACP", "hook", "secret", "lock file".
---

# OpenClaw Troubleshooting

## Quick diagnostics

```bash
openclaw status                        # gateway health
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log   # recent logs
ps aux | grep openclaw-gateway | grep -v grep            # is it running?
python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null && echo "valid"  # config valid
curl -s http://127.0.0.1:18789/ -o /dev/null -w "%{http_code}"  # HTTP health
openclaw doctor                        # diagnose + auto-fix
openclaw doctor --fix
```

## Decision tree (which log/section to check)

| Symptom | Check first |
|---------|-------------|
| Gateway won't start | Lock file `/tmp/openclaw.lock` + process check |
| Plugin won't load | `plugins.allow` list + `openclaw plugins list` |
| Memory search stale/wrong | Rebuild index: `openclaw memory index --force` |
| Channel silent/non-responsive | Transport probe + bot token + intent check |
| ACP agent won't spawn | `/acp doctor` then `/acp spawn codex --bind here` |
| Hook not firing | `openclaw hooks list` + `openclaw hooks info HOOK_NAME` |
| Config change no effect | Restart required? Check `memory.backend`, `plugins.entries.*.enabled` |
| Auth/credential error | Search logs for `auth` or `credential` |
| 429 rate limit | Model `context1m` + credential eligibility check |
| SecretRef unresolved | `~/.openclaw/credentials/` + plaintext key test |

---

## Common issues by category

### Gateway startup

**"Port already in use"**
- Gateway is already running. Don't restart. Verify:
```bash
ps aux | grep openclaw-gateway
```

**Lock file stale (gateway won't start)**
```bash
cat /tmp/openclaw.lock
rm /tmp/openclaw.lock   # only if gateway is NOT running
openclaw gateway start
```

**Config JSON invalid**
```bash
python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null
```

### Memory

**"plugin disabled (memory slot set to X)"**
- Memory slot occupied by another plugin
```json5
plugins: { slots: { memory: "openclaw-honcho" } }
```
Then restart gateway.

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

**Node device pairing fails**
- Use `openclaw devices list` to check paired devices
- Approve with `openclaw devices approve <requestId>` (not `openclaw pairing`)
- Node/device pairing uses `openclaw devices`, NOT `openclaw pairing` (which is for channel pairing only)
- Pairing codes expire after 1 hour

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
