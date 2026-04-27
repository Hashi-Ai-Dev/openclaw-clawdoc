---
name: openclaw-troubleshooting
description: OpenClaw troubleshooting and fixes. Use when diagnosing gateway crashes, config errors, plugin conflicts, ACP agent failures, pairing/device pairing, hook not firing, lock file issues, secret resolution failures, or queue/backpressure problems. Triggers on: "gateway crash", "config error", "crash", "debug", "troubleshoot", "pairing", "device pairing", "hook failure", "lock file", "queue", "backpressure", "secret not resolving", "plugin conflict", "openclaw doctor", "gateway locked", "ACP agent won't start", "channel silent".
---

# OpenClaw Troubleshooting

## ⚠️ Critical rules

- **Never `rm /tmp/openclaw.lock` while gateway process is running** — check `ps aux | grep openclaw-gateway` first
- **Never restart gateway without checking session queue** — pending messages get dropped
- **Never confuse `openclaw pairing` (channels) with `openclaw devices` (nodes)**
- **Config changes requiring restart:** `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*` — other keys are hot-reloaded
- **Honcho + memory slot:** must set `plugins.slots.memory = "openclaw-honcho"` — default `memory-core` causes silent failure

## Quick diagnostics

```bash
openclaw doctor --non-interactive    # diagnose + auto-fix most issues
openclaw status                        # gateway health
ps aux | grep openclaw-gateway | grep -v grep   # is it running?
tail -50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log   # recent logs
python3 -m json.tool ~/.openclaw/openclaw.json > /dev/null && echo "valid"
```

## Common issues

| Symptom | Fix |
|---------|-----|
| Gateway won't start | Check lock file: `ps aux \| grep openclaw-gateway` |
| Config errors | Run `openclaw doctor --non-interactive` |
| Plugin not loading | Check `plugins.allow` includes plugin ID |
| Channel silent | Check `channels.<name>.token` set, bot has permissions |
| Memory search returns nothing | Verify backend is set: `openclaw config get memory` |
| Cron not firing | `openclaw cron list` — check next run time |
| Hook not firing | `openclaw hooks list` → `openclaw hooks enable <name>` |

## Lock file stale — safe cleanup

```bash
# Only if process is confirmed dead:
ps aux | grep openclaw-gateway | grep -v grep
# If empty → safe to remove lock:
rm /tmp/openclaw.lock
```

## References

- `references/diagnostic-flowchart.md` — decision tree flowchart
- `references/troubleshooting-flow.md` — step-by-step triage
- `references/gateway-troubleshooting.md` — gateway crash/debug
- `references/channel-troubleshooting.md` — channel-specific issues
- `references/hooks.md` — hook not firing fixes
