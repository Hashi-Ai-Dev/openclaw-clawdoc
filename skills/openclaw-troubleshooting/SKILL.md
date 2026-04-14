---
name: openclaw-troubleshooting
description: OpenClaw troubleshooting and fixes. Use when diagnosing memory issues, channel problems, gateway crashes, config errors, plugin conflicts, ACP agents, or pairing issues. Triggers on: "broken", "not working", "error", "crash", "debug", "fix", "issue", "problem", "troubleshoot", "pairing", "ACP", "hook".
---

# OpenClaw Troubleshooting

## Quick diagnostics

```bash
# Gateway status
openclaw status

# Gateway logs
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# Check if gateway running
ps aux | grep openclaw-gateway | grep -v grep

# Validate config JSON
python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null && echo "valid"

# Health check
curl -s http://127.0.0.1:18789/ -o /dev/null -w "%{http_code}"
```

## Common issues + fixes

### "plugin disabled (memory slot set to X)"
**Cause:** Memory slot occupied by another plugin
**Fix:**
```json5
plugins: { slots: { memory: "openclaw-honcho" } }
```
Then restart gateway.

### "Port already in use" on gateway start
**Cause:** Gateway already running
**Fix:** Don't restart — gateway is already up. Check with:
```bash
ps aux | grep openclaw-gateway
```

### Embedding 404 errors
**Cause:** `memorySearch.remote.baseUrl` wrong or invalid provider
**Fix:** Valid providers: `local`, `openai`, `gemini`, `voyage`, `mistral`, `bedrock`
OpenRouter is NOT a valid embedding provider.

### Discord channel binding not working
**Cause:** Missing `guildId` or wrong format
**Fix:** Format must be `guildId/channelId`, e.g. `"1483508270344966247/1493571227963363481"`

### Config changes not taking effect
**Cause:** Gateway needs restart for certain changes
**Changes requiring restart:** `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*`
**Dynamic (no restart):** `tools.web.search.apiKey`, `agents.defaults.memorySearch.remote`

### Memory search returns stale results
```bash
openclaw memory index --force  # rebuild index
```

### Gateway won't start (lock file stale)
```bash
cat /tmp/openclaw.lock  # check what's there
# If gateway not running, delete lock and retry:
rm /tmp/openclaw.lock
openclaw gateway start
```

### Plugin not loading
```bash
openclaw plugins list  # check plugin status
# Verify plugin ID in allow list:
# plugins.allow: ["plugin-id"]
```

### Session confusion / wrong context
Check session grouping:
```json5
session: { scope: "per-sender", dmScope: "main" }
```
`dmScope: "main"` collapses all DMs to one session key.

### Honcho not responding
```bash
openclaw honcho status  # check connection
# Verify baseUrl points to correct Honcho instance
# For self-hosted: http://127.0.0.1:8000
```

### ACP agent not spawning
**Cause:** Harness adapter not cached or vendor auth missing
**Fix:**
```bash
/acp doctor           # check readiness
/acp spawn codex --bind here  # first spawn fetches adapter
```
ACP uses bundled `acpx` runtime plugin. Fresh installs ship it enabled by default.

### Hook not firing
```bash
openclaw hooks list          # list all hooks
openclaw hooks info HOOK_NAME  # check hook config
openclaw hooks enable HOOK_NAME  # enable if disabled
```
Hooks live in `~/.openclaw/hooks/` and fire on events like `command:new`, `session:compact:before`, `gateway:startup`, `message:received`.

### Pairing code not working / expired
- Codes expire after **1 hour**
- Pending requests capped at **3 per channel**
- Approve with:
```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

### Discord bot appears online but won't respond
1. Check `channels.discord.token` is valid
2. If `dmPolicy: "pairing"`, approve your Discord ID
3. Enable **Message Content Intent** in Discord Developer Portal
4. If `guilds` configured, check `requireMention` setting for the channel
5. Run `openclaw channels status --probe` to verify transport

### Telegram bot online but group stays silent
1. Verify mention requirement and bot privacy mode (disable privacy mode for groups)
2. Check `groups` config for `requireMention: false`
3. For topic routing: Telegram forum topics embed `:topic:<topicId>` in the group key

### WhatsApp random disconnects
```bash
openclaw channels status --probe  # check transport
# Re-login and verify credentials directory is healthy
openclaw channels login --channel whatsapp --account personal
```

### SecretRef unresolved at startup
**Cause:** `secret:` reference in config points to a non-existent or non-resolvable secret
**Fix:** Check `~/.openclaw/credentials/` for the secret file, or use plaintext API key temporarily for diagnosis

### Anthropic 429 rate limit on long context
**Cause:** Model has `context1m: true` but credential isn't eligible for long-context requests
**Fix:**
1. Disable `context1m` for that model
2. Use an eligible Anthropic credential
3. Configure fallback models

## Logs to check

| Situation | Log |
|-----------|-----|
| Gateway crashes | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |
| Plugin issues | Same log, search for plugin name |
| Memory search | Same log, search for `memory` or `embedding` |
| Channel issues | Same log, channel name |
| Auth problems | Same log, search for `auth` or `credential` |
| ACP issues | Same log, search for `acp` or `acpx` |
| Hook issues | Same log, search for `hook` |

## Lock file

`/tmp/openclaw.lock` — if gateway won't start, check if process already running.

## References

- `references/troubleshooting-flow.md` — decision tree for issues
- `references/gateway-troubleshooting.md` — deep gateway runbook
- `references/channel-troubleshooting.md` — per-channel failure signatures
- `references/hooks.md` — hook system reference
