# MEMORY.md — ClawDoc Long-term

*Updated 2026-04-17.*

## Knowledge Base (Skills)

ClawDoc has a full self-contained knowledge base built from OpenClaw source docs:

```
skills/
├── openclaw-master/           # Top-level routing skill
├── openclaw-config/          # Gateway config, secrets, retry, auth, failover
├── openclaw-memory/          # Memory backends + embeddings + active memory
├── openclaw-agents/          # Multi-agent + bindings + sandbox + tool policies
├── openclaw-channels/        # All channel configs + routing + pairing
├── openclaw-concepts/        # Architecture, session, compaction, streaming, queue, SOUL.md
├── openclaw-troubleshooting/  # Diagnosis, errors, ACP, hooks, channel failures
├── openclaw-plugins/         # Plugin slots + plugin config + context engine
├── openclaw-tools/           # Tool reference: exec, browser, ACP, Lobster, Diff viewer
├── openclaw-cli/             # CLI commands: hooks, pairing, cron, ACP, MCP
└── openclaw-providers/       # 43+ model providers + auth profiles + failover
```

Each skill has a `references/` directory with full doc copies from `/openclaw/docs/`.

**Total: 90 files across 11 skills.**

## Open-Source Package

**Official repo:** https://github.com/Hashi-Ai-Dev/openclaw-clawdoc

ClawDoc is open-sourced for the community. Package at `openclaw-clawdoc/` with full skill tree + 44 reference docs from OpenClaw source.

## OpenClaw Architecture (Verified)

### Plugin Slot System
Plugins declare a `kind` field. Some kinds map to exclusive slots:
- `memory` slot → one plugin owns it (default: `memory-core`)
- Slot assignment: `plugins.slots.memory = "plugin-id"`
- Default slot bindings: `memory` → `"memory-core"`, `contextEngine` → `"legacy"`

### Honcho Plugin Integration (SOLVED)
- Plugin ID: `openclaw-honcho`
- Kind: `memory`
- Fix: set `plugins.slots.memory = "openclaw-honcho"`
- Self-hosted: no API key needed for localhost
- Config fields: `workspaceId`, `baseUrl`, `apiKey` (optional for self-hosted), `timeoutMs`

### Gateway Restart Protocol
- **Require restart:** `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*`
- **Dynamic (no restart):** `tools.web.search.apiKey`, `agents.defaults.memorySearch.remote`
- NEVER restart without explicit permission from Hashi
- Lock file: `/tmp/openclaw.lock`

### Config Validation
- Always validate JSON: `python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null && echo "valid"`
- Check logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

## Key Concepts Added

### Streaming + Chunking
Two layers: **block streaming** (emit completed blocks as assistant writes) and **preview streaming** (update a temp message on Telegram/Discord/Slack).
- `blockStreamingDefault: "on"|"off"` — channel default
- `blockStreamingBreak: "text_end"|"message_end"` — chunk flush boundary
- `blockStreamingCoalesce: {minChars?, maxChars?, idleMs?}` — merge blocks before send
- Discord `maxLinesPerMessage` (default 17) prevents UI clipping

### Queue Modes (message handling)
| Mode | Behavior |
|------|----------|
| `collect` (default) | Coalesce all queued messages into single followup turn |
| `steer` | Inject immediately into current run, cancel pending tools |
| `followup` | Enqueue for next turn after current run ends |
| `steer-backlog` | Steer now AND preserve for followup |

### Model Failover
Two-stage: (1) auth profile rotation within provider → (2) model fallback to next in `fallbacks[]`. Only persists fallback-owned fields to avoid overwriting manual `/model` changes.

### SOUL.md Personality
`SOUL.md` is the high-priority personality layer. Short + sharp beats long + vague. Use the Molty prompt to rewrite with actual voice.

### Active Memory (optional plugin)
Blocking sub-agent that runs before the main reply for eligible sessions, proactively surfacing relevant memory. Enable via `plugins.entries.active-memory`.

### Task Flow
Managed multi-step flow orchestration above background tasks. Managed mode owns lifecycle end-to-end; mirrored mode observes external tasks. Cancel is sticky across restarts.

## Schema Reference

### memory.backend
Allowed: `"builtin"`, `"qmd"` — `"honcho"` is NOT valid here. Honcho is a plugin that owns the `memory` slot via `plugins.slots.memory = "openclaw-honcho"`.

### plugins.allow
Bundled plugins: `discord`, `minimax`, `browser`, `active-memory`, `brave`, `diffs`, `llm-task`, `lobster`, `memory-core`

## Common Issues & Fixes

1. **"plugin disabled (memory slot set to X)"**
   → Set `plugins.slots.memory = "openclaw-honcho"` → restart gateway

2. **"Port already in use" on gateway start**
   → Gateway already running — don't restart
   → Check: `ps aux | grep openclaw-gateway`

3. **Embedding 404 errors**
   → Valid providers: `local`, `openai`, `gemini`, `voyage`, `mistral`, `bedrock`
   → OpenRouter is NOT a valid embedding provider

4. **Discord channel binding not working**
   → Format: `guildId/channelId`, e.g. `"1483508270344966247/1493571227963363481"`

5. **ACP agent not spawning**
   → `/acp doctor` to check readiness
   → `/acp spawn codex --bind here` to fetch adapter and spawn

6. **Hook not firing**
   → `openclaw hooks list` → `openclaw hooks info HOOK_NAME` → `openclaw hooks enable HOOK_NAME`

7. **Pairing code expired**
   → Codes expire after 1 hour, max 3 pending per channel
   → `openclaw pairing list telegram` → `openclaw pairing approve telegram <CODE>`

## Learned Fixes

- Honcho + memory-core slot conflict: `plugins.slots.memory` override (NOT `memory.backend`)
- Self-hosted Honcho: no API key needed, just `baseUrl: "http://127.0.0.1:8000"`
- `allow` list in plugins must contain exact plugin ID, not CLI command name
- Config changes for `agents.defaults.*` require gateway restart
- `dmScope: "main"` collapses all DMs to one session key

## OpenClaw Install Troubleshooting (Verified 2026-04-16)

### Binary not found after install
OpenClaw installs to non-standard npm paths. NEVER guess a PATH — always verify with:
```bash
find ~ -name openclaw -type f 2>/dev/null
```
Common locations: `~/.hermes/node/bin/`, `~/.local/bin/`, `/usr/local/bin/`

### Wizard crashes on channel selection (TypeError: Cannot read properties of undefined)
The installer has a bug when clicking "Skip for now" on the channel step. Workarounds:
1. Select a channel (even if unused) instead of skipping
2. Use `OPENCLAW_NO_ONBOARD=1` to skip the entire wizard:
   ```bash
   OPENCLAW_NO_ONBOARD=1 curl -fsSL https://openclaw.ai/install.sh | bash
   ```
   Then configure manually with `openclaw config set ...`

### Recommended model setup for new installs
```bash
openclaw config set agents.defaults.model.primary "google/gemini-2.5-flash"
openclaw config set auth.profiles.google.provider "google"
# Then configure channel (discord example):
openclaw config set channels.discord.token "YOUR_BOT_TOKEN"
openclaw config set channels.discord.enabled true
```

## Memory + Multimodal Fix (Verified 2026-04-16)

### `agents.*.memorySearch.multimodal` warning
If gateway logs show: `qmd memory startup initialization failed: Error: agents.*.memorySearch.multimodal requires a provider adapter`
- Cause: `multimodal.enabled: true` but no installed provider supports image inputs for search
- Fix (dynamic, no restart):
  ```bash
  openclaw config set agents.defaults.memorySearch.multimodal.enabled false
  ```

### Current memory stack (verified working)
- Backend: `qmd` (schema-valid, handles embedding storage)
- Plugin slot: `openclaw-honcho` (handles search + retrieval)
- Correct config:
  ```json
  {
    "memory": { "backend": "qmd", "citations": "auto" },
    "plugins": {
      "slots": { "memory": "openclaw-honcho" },
      "entries": { "openclaw-honcho": { "config": { "workspaceId": "your-workspace", "baseUrl": "http://127.0.0.1:8000" } } }
    }
  }
  ```

## Session Crash Analysis (2026-04-16)

### Root cause: stuck sessions blocking gateway restart
- Load average of 21 was I/O wait (processes blocked on network), not CPU
- Two stuck sessions (`claw-doc`, `main`) held locks, preventing clean restart
- Honcho connection failures (`fetch failed`) cascaded during crash period
- Stuck session indicator: `stuck session: sessionId=X state=processing age=Ns`

### Recovery steps
1. Clear session locks: `rm -f /data/.openclaw/agents/*/sessions/*.lock`
2. Signal gateway: `openclaw gateway restart` (or SIGUSR1 for hot reload)
3. Verify Honcho is running: `curl -s http://127.0.0.1:8000/health`
4. Check logs for reconnection: `tail -20 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log`

## Source Docs

- Open-source repo: https://github.com/Hashi-Ai-Dev/openclaw-clawdoc (official)
- Local docs: `/openclaw/docs/`
- GitHub: general docs + `/docs/reference`
- Docs site: `docs.openclaw.ai`
- ClawHub (skill registry): `clawhub.ai`
