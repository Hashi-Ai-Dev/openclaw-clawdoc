# ClawDoc Troubleshooting

Quick triage for the most common OpenClaw issues. Start here before diving into detailed runbooks.

## 60-second health check

Run this exact ladder in order:

```bash
openclaw status
openclaw gateway status
openclaw doctor --non-interactive
openclaw logs --follow
```

**All healthy if:**
- `openclaw status` → shows configured channels, no auth errors
- `openclaw gateway status` → `Runtime: running`, `Connectivity probe: ok`
- `openclaw doctor` → no blocking errors

---

## Top 10 issues

### 1. Gateway won't start — "port already in use"

```bash
openclaw gateway status
# If already running: just connect to it, don't restart
```

The gateway is already running. OpenClaw runs as a daemon — starting it again tries to bind the same port. Connect to the existing instance instead.

---

### 2. Gateway won't start — "invalid config"

```bash
openclaw doctor --non-interactive
# Fixes most config errors automatically
```

Run `doctor` first — it catches and repairs the most common config issues. If it can't fix it, the output tells you exactly which field is wrong.

---

### 3. Discord bot not responding

```bash
openclaw channels status --probe
# Verify Discord token is valid and bot has permissions
```

1. Check `channels.discord.token` is set: `openclaw config get channels.discord.token`
2. Verify the bot is in your server and has "Message Content Intent" enabled in Discord Developer Portal
3. For DMs: use `openclaw pairing approve discord <CODE>` after a user initiates pairing

---

### 4. Model authentication failing

```bash
openclaw models status
```

Shows which providers are authenticated and which model calls are succeeding or failing. Most auth failures are:
- Wrong API key format (check for extra spaces, quotes)
- Provider account not activated
- Insufficient credits on the provider account

---

### 5. TTS not working / auto-playing audio

**Enable TTS:**
```bash
openclaw config merge examples/tts-minimax.json
openclaw gateway restart
```

**Disable TTS (if it keeps auto-firing):**
```bash
openclaw config set messages.tts.enabled false
openclaw gateway restart
```

---

### 6. Memory search returning nothing

1. Verify memory is enabled: `openclaw config get memory`
2. For builtin memory: check `memory.backend: "builtin"` — no external services needed
3. For QMD: verify the paths section points to actual files
4. For Honcho: verify the Honcho server is running at the configured baseUrl

---

### 7. Cron jobs not firing

```bash
openclaw cron list
openclaw cron runs --id <job-id>
```

1. `cron list` shows all jobs with next run time
2. `cron runs` shows execution history and any errors
3. Jobs persist across gateway restarts (stored in `~/.openclaw/cron/jobs.json`)
4. Isolated cron runs use a separate session — check if that session is blocked or errored

---

### 8. Plugin won't install

```bash
openclaw plugins install <package-name>
openclaw doctor --non-interactive
```

Common fixes:
- Run `openclaw doctor` first — it repairs most plugin config issues
- If install fails with "missing openclaw.extensions": the plugin is using an old format — open an issue on the plugin's repo
- Verify `plugins.allow` includes the plugin ID

---

### 9. Gateway restart not picking up config changes

Some config changes require a full restart (`openclaw gateway restart`), others are hot-reloaded dynamically. If a config change seems stuck:

```bash
openclaw gateway restart
```

Changes to `memory.backend`, `plugins.slots.*`, and `agents.defaults.*` always require a full restart.

---

### 10. "All models failed" / model failover

```bash
openclaw config get agents.defaults.model.primary
openclaw models status
```

1. Verify your primary model is set: `agents.defaults.model.primary`
2. Check `models.status` — shows which providers are reachable
3. Configure fallback providers in `agents.defaults.model.fallbacks`

---

## Deep runbooks

For deeper diagnosis, ClawDoc routes to these skills:

| Issue | Skill |
|-------|-------|
| Config errors, gateway won't start | `openclaw-troubleshooting` → gateway-troubleshooting |
| Channel connection issues | `openclaw-troubleshooting` → channel-troubleshooting |
| Plugin install failures | `openclaw-plugins` |
| Memory not working | `openclaw-memory` |
| Cron/hooks not firing | `openclaw-automation` |
| Need full diagnostic run | `openclaw doctor --fix` or `openclaw doctor --non-interactive` |

## Getting help

1. Run `openclaw doctor --non-interactive` — fixes 80% of common issues
2. Run `openclaw logs --follow` and look for repeating error patterns
3. Share `openclaw status --all` output when asking for help — it's designed to be shareable

For the full official troubleshooting guide: [docs.openclaw.ai/help/troubleshooting](https://docs.openclaw.ai/help/troubleshooting)
