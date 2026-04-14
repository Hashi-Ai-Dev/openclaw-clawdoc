# TOOLS.md — ClawDoc Diagnostics

## OpenClaw Diagnostics
```bash
# Check gateway status
openclaw status

# Check gateway logs
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# Check if gateway is running
ps aux | grep openclaw-gateway | grep -v grep

# Validate config JSON
python3 -m json.tool ~/.openclaw/openclaw.json > /dev/null && echo "valid"

# Check gateway health
curl -s http://127.0.0.1:18789/ -o /dev/null -w "%{http_code}"
```

## Config Editing
```bash
# Read current config
cat ~/.openclaw/openclaw.json

# Edit with python (safe)
python3 << 'EOF'
import json
with open('~/.openclaw/openclaw.json') as f:
    d = json.load(f)
# make changes
with open('~/.openclaw/openclaw.json', 'w') as f:
    json.dump(d, f, indent=2)
EOF
```

## Gateway Management
```bash
# Start gateway
openclaw gateway start

# Stop gateway
pkill -f openclaw-gateway

# Restart gateway (requires permission!)
# Ask first!
```

## OpenClaw Docs
- Docs: `/openclaw/docs/`
- Reference: `/openclaw/docs/reference/`
- Config schema: `/openclaw/docs/reference/config.md`
- Plugin API: `/openclaw/docs/plugins/`

## Key File Paths
- Config: `~/.openclaw/openclaw.json`
- Extensions: `~/.openclaw/extensions/`
- Logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- Lock: `/tmp/openclaw.lock`
