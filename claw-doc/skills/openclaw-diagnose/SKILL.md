---
name: openclaw-diagnose
description: Run comprehensive OpenClaw diagnostics in one pass — gateway, plugins, memory, channels, auth, stuck sessions, and logs. Use when the gateway is unresponsive, behaving oddly, or when doing a full system health check. Triggers on: "diagnose", "full check", "health check", "system status", "debug openclaw", "openclaw doctor", "is openclaw running", "gateway down", "check everything".
---

# OpenClaw Diagnose

Run this script to get a full system health report in one pass:

```bash
echo "=== Gateway ==="
ps aux | grep openclaw-gateway | grep -v grep
curl -s http://127.0.0.1:18789/ -o /dev/null -w "%{http_code}" 2>/dev/null

echo "=== Config Valid ==="
python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null && echo "valid" || echo "INVALID"

echo "=== Plugins ==="
openclaw plugins list 2>/dev/null || echo "plugin list failed"

echo "=== Memory ==="
openclaw memory status 2>/dev/null || echo "memory status failed"

echo "=== Honcho ==="
curl -s http://127.0.0.1:8000/health 2>/dev/null

echo "=== Channels ==="
openclaw channels status 2>/dev/null || echo "channel status failed"

echo "=== Recent Errors ==="
tail -30 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line)
        t = d.get('time','')[:19]
        msg = str(d.get('1',''))
        lv = d.get('_meta',{}).get('logLevelName','')
        if lv in ('ERROR','WARN') or 'failed' in msg.lower():
            print(f'{t} [{lv}] {msg[:120]}')
    except: pass
"

echo "=== Session Locks ==="
find /data/.openclaw/agents -name "*.lock" 2>/dev/null | head -5

echo "=== Stuck Sessions ==="
grep -i "stuck session" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | tail -5
```

## Decision tree based on results

| Check | Failure | Fix |
|---|---|---|
| Gateway process missing | Gateway not running | `openclaw gateway start` |
| HTTP 000 | Gateway down or port blocked | Check `ps aux` and logs |
| Config invalid | JSON malformed | `python3 -m json.tool` to find error |
| Plugin missing | Not in `plugins.allow` | Add to allow list |
| Memory slot error | `plugins.slots.memory` wrong | See memory skill |
| Honcho 000 | Honcho server down | Start Honcho server |
| Channel probe failed | Token missing or wrong | `openclaw config set channels.X.token` |
| Session locks found | Stuck sessions block restart | `find ... -name "*.lock" -delete` then restart |
| Stuck session in logs | Long-running turn blocked | Let it finish or `openclaw sessions kill <id>` |

## Quick triage order

1. **Gateway up?** → `ps aux | grep openclaw-gateway`
2. **HTTP 200?** → `curl -s http://127.0.0.1:18789/`
3. **Config valid?** → `python3 -m json.tool ~/.openclaw/openclaw.json`
4. **Plugins loaded?** → `openclaw plugins list`
5. **Memory working?** → `openclaw memory status`
6. **Logs clean?** → `tail -50` for ERROR/WARN
