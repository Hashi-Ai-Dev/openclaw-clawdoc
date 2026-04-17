# ClawDoc Changelog

All notable changes to ClawDoc are documented here.

## [2026-04-17] — Skills Expansion Release

### New Skills Added

**openclaw-setup** (`skills/openclaw-setup/SKILL.md`)
First-run setup guide covering:
- Binary detection after install (`find ~ -name openclaw`)
- Wizardless install (`OPENCLAW_NO_ONBOARD=1`)
- Model configuration (free tier: Gemini 2.5 Flash, GPT-4o-mini)
- Channel setup (Discord, Telegram, WhatsApp)
- Post-install verification + recovery from broken wizard

**openclaw-diagnose** (`skills/openclaw-diagnose/SKILL.md`)
Comprehensive one-pass diagnostic covering:
- Gateway process + HTTP health
- Config JSON validation
- Plugin loading status
- Memory + Honcho status
- Channel probe status
- Recent ERROR/WARN logs
- Session lock files
- Stuck session detection
- Decision tree mapping results to fixes

### Bugs Fixed

**Wrong Honcho memory slot guidance (Critical)**
- `openclaw-troubleshooting/SKILL.md` and `openclaw-memory/SKILL.md` both said "Never set `plugins.slots.memory` for Honcho" — this is wrong
- Honcho MUST have `plugins.slots.memory = "openclaw-honcho"` to function as the memory backend
- Updated both skills to the verified correct configuration

**Installation TypeError (installer wizard crash)**
- Added to `openclaw-troubleshooting` and `openclaw-setup`: channel selection "Skip for now" crashes the wizard with `TypeError: Cannot read properties of undefined`
- Fix: use `OPENCLAW_NO_ONBOARD=1` flag or select any channel instead of skipping

### MEMORY.md Updates

- Added "OpenClaw Install Troubleshooting (Verified 2026-04-16)"
- Added "Memory + Multimodal Fix (Verified 2026-04-16)"
- Added "Session Crash Analysis (2026-04-16)"
- Fixed `memory.backend` schema note (QMD is valid, `honcho` is NOT valid there — it's a plugin slot via `plugins.slots.memory`)
- Updated date to 2026-04-17

### Verified Config (2026-04-16)

```json
{
  "memory": { "backend": "qmd", "citations": "auto" },
  "plugins": {
    "slots": { "memory": "openclaw-honcho" },
    "entries": {
      "openclaw-honcho": {
        "config": {
          "workspaceId": "your-workspace",
          "baseUrl": "http://127.0.0.1:8000"
        }
      }
    }
  },
  "agents": {
    "defaults": {
      "memorySearch": {
        "multimodal": { "enabled": false }
      }
    }
  }
}
```

---

## Prior Releases

- See commit history at https://github.com/Hashi-Ai-Dev/openclaw-clawdoc
