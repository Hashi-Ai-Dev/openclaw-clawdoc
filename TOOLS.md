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

# Edit with python (safe — Path.home() expands ~)
python3 << 'EOF'
from pathlib import Path
import json
cfg = Path.home() / ".openclaw" / "openclaw.json"
with cfg.open() as f:
    d = json.load(f)
# make changes
with cfg.open("w") as f:
    json.dump(d, f, indent=2)
EOF
```

## Gateway Management
```bash
# Start gateway
openclaw gateway start

# Stop gateway — prefer the CLI; pkill is a last resort
openclaw gateway stop          # graceful: SIGTERM, lets in-flight requests finish
# If the gateway is wedged and `openclaw gateway stop` doesn't return within ~30s:
#   pkill -TERM -f openclaw-gateway     # send SIGTERM to the gateway process group
#   # Only escalate to SIGKILL if SIGTERM is ignored for another 30s:
#   pkill -KILL -f openclaw-gateway
# Confirm with the operator before stopping or killing a running gateway; stopping
# interrupts any in-flight requests and disconnects connected channels.

# Restart gateway (requires permission!)
# Ask first!
```

## OpenClaw Docs

The OpenClaw documentation source lives in your local OpenClaw checkout. The most common locations are:

- **Local checkout:** clone OpenClaw from `https://github.com/openclaw/openclaw` and read the `docs/` directory in that clone.
- **Published docs:** `https://docs.openclaw.ai/` — the same content as the local `docs/` directory.

If your install puts the docs somewhere else (Docker bind mount, package manager path, etc.), adjust accordingly. The path on this machine is not a portable contract.

## Key File Paths
- Config: `~/.openclaw/openclaw.json`
- Extensions: `~/.openclaw/extensions/`
- Logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- Lock: `/tmp/openclaw.lock`
