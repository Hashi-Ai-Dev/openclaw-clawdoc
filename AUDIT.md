# ClawDoc Package — Config Audit Report

*Use this template when ClawDoc audits an OpenClaw config. Fill in your own values.*

## Audit Scope
- Config file audited: `~/.openclaw/openclaw.json` (or your config path)
- Date: YYYY-MM-DD
- OpenClaw version: (run `openclaw --version`)

## Findings

| Issue | Severity | Fix |
|-------|----------|-----|
| (your finding here) | high/medium/low | (your fix here) |

## Config Summary

*(run `openclaw config show` or paste the relevant sections)*

```json
{
  "agents": { ... },
  "channels": { ... },
  "memory": { ... },
  "plugins": { ... }
}
```

## Actions Taken

- [ ] Config validated (`python3 -m json.tool ~/.openclaw/openclaw.json`)
- [ ] Issues identified
- [ ] Fixes applied
- [ ] Gateway restarted (if required)

## Notes

(What you learned, what to watch for, edge cases discovered)
