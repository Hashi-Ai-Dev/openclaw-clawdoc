# OpenClaw Diagnostic Flowchart

## Symptom → Root Cause → Fix mapping for the most common OpenClaw failures.

---

## Gateway Won't Start

```
Gateway won't start
├─ "Port already in use" / EADDRINUSE
│   └─ Another process has port 18789
│       ├─ Check: ps aux | grep openclaw-gateway
│       └─ Fix: Kill old process OR change port via gateway.port in config
├─ "Config validation failed"
│   ├─ Check: python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null && echo "valid"
│   └─ Fix: Review the JSON error, check for trailing commas / bad types
├─ Lock file stuck
│   ├─ Check: cat /tmp/openclaw.lock
│   └─ Fix: rm /tmp/openclaw.lock (only if gateway is NOT running)
└─ "plugin disabled (memory slot set to X)"
    └─ Fix: Set plugins.slots.memory = "openclaw-honcho" (or plugin ID), restart gateway
```

---

## Agent Not Responding / Silent

```
Agent silent on channel
├─ Gateway down?
│   ├─ Check: ps aux | grep openclaw-gateway | grep -v grep
│   └─ Fix: openclaw gateway start
├─ Channel disconnected?
│   ├─ Check: openclaw channels status
│   └─ Fix: openclaw channels enable <channel>
├─ Bot not in guild / DM policy blocking?
│   ├─ Check: channel's DM policy (pairing/allowlist/open)
│   └─ Fix: set channel DM policy or approve pairing
├─ Context window full?
│   ├─ Check: /context list (shows context fill %)
│   └─ Fix: /compact to compress history
└─ Model API down / auth failing?
    ├─ Check: openclaw logs | grep -i "auth\|401\|403\|rate"
    └─ Fix: Check API keys, auth profiles, model fallback config
```

---

## Plugin Won't Load

```
Plugin appears disabled
├─ "plugin disabled (memory slot)"
│   └─ Another plugin owns the slot. Set plugins.slots.memory explicitly
├─ Not in plugins.allow list?
│   └─ Add plugin ID to plugins.allow array
├─ Missing dependency?
│   ├─ Check: openclaw logs | grep "plugin\|import\|require"
│   └─ Fix: Install missing npm deps, restart gateway
├─ Manifest invalid?
│   ├─ Check: openclaw plugins list | grep <plugin>
│   └─ Fix: Validate openclaw.plugin.json schema
└─ Kind slot conflict?
    └─ Check: openclaw status | grep slots
```

---

## Memory / Embedding Not Working

```
Embedding search returns nothing / 404 errors
├─ Wrong embedding provider?
│   └─ Valid: local, openai, gemini, voyage, mistral, bedrock
│   └─ Invalid: openrouter (NOT a valid embedding provider)
├─ memorySearch.remote.baseUrl wrong?
│   ├─ For Honcho: baseUrl = http://127.0.0.1:8000
│   └─ Check: curl -s http://127.0.0.1:8000/health
└─ Honcho plugin not enabled?
    ├─ Check: openclaw status | grep honcho
    └─ Fix: plugins.entries.openclaw-honcho.enabled = true, restart gateway

"memory slot set to memory-core but plugin is openclaw-honcho" error
    └─ Fix: Set plugins.slots.memory = "openclaw-honcho"
```

---

## Hook Not Firing

```
Hook configured but not triggering
├─ Hook disabled?
│   └─ Check: openclaw hooks list
│   └─ Fix: openclaw hooks enable <hook-name>
├─ Wrong trigger event?
│   ├─ Check: openclaw hooks info <hook-name> — shows trigger conditions
│   └─ Fix: Update trigger event spec in config
├─ Hook script errored?
│   ├─ Check: openclaw logs | grep "hook\|error" | tail -50
│   └─ Fix: Debug the hook script
└─ Channel not permitted?
    └─ Hook only fires on permitted channels. Check channel allowlist in hook config.
```

---

## Exec Tool Problems

```
exec tool times out / no output
├─ Approval required?
│   ├─ Check: tools.elevated.enabled and execApprovals config
│   └─ Fix: Run /approve or set allowOncie for one-time
├─ Sandbox blocking?
│   ├─ Check: agents.defaults.sandbox or per-agent sandbox config
│   └─ Fix: Disable sandbox OR add required fs paths to sandbox allowlist
└─ Command not found?
    └─ Check: which <command> in the gateway environment

Elevated exec not working
├─ tools.elevated.enabled = false (default)?
│   └─ Fix: Set tools.elevated.enabled = true in config
└─ Still failing?
    └─ Check: execApprovals for the channel (Discord/Slack/Matrix need execApprovals config)
```

---

## ACP Agent Not Spawning

```
ACP agent won't start / "not ready" errors
├─ /acp doctor — run this first
│   └─ Check output for missing adapter or config issues
├─ Adapter not fetched?
│   └─ /acp spawn codex --bind here (fetches adapter + spawns)
└─ Runtime not available?
    └─ Check: openclaw status | grep acp
```

---

## Quick Diagnostic Commands

```bash
# Full system check
openclaw status

# Gateway health
curl -s http://127.0.0.1:18789/health

# Plugin status
openclaw plugins list

# Channel status
openclaw channels status

# Recent errors
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i error

# Config validation
python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null && echo "VALID"

# Memory provider
openclaw memory status

# Active hooks
openclaw hooks list
```

---

## Context Window Full

```
/context list          # Shows what's consuming context
/compact              # Compress older history into summary
/clear                # Clear current session context

# If context is stuck:
# → Check /context detail for large files injected
# → Remove or truncate large workspace files
# → Use /compact to reduce history
```
