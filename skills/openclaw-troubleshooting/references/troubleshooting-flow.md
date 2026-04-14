# Troubleshooting Decision Tree

## Start here
```bash
openclaw status
tail -50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

## Symptom → Skill mapping

| Symptom | Skill to load |
|---------|--------------|
| Config errors, validation | `openclaw-config` |
| Memory not working, embeddings | `openclaw-memory` |
| Multi-agent routing broken | `openclaw-agents` |
| Discord/Telegram/WhatsApp issues | `openclaw-channels` |
| "How does X work?" | `openclaw-concepts` |
| Something broken, need fix | `openclaw-troubleshooting` |
| Plugin not loading, slot conflict | `openclaw-plugins` |
| Tool behavior questions | `openclaw-tools` |
| CLI command syntax | `openclaw-cli` |
| Model provider errors | `openclaw-providers` |

## Issue-specific flows

### Bot not responding (Discord)
1. Check `channels.discord.token` is valid
2. Check `dmPolicy` — if `pairing`, approve pairing request
3. Check `allowFrom` contains your Discord ID
4. Enable Message Content Intent in Discord Developer Portal
5. Check `guilds` config if in guild
6. See `openclaw-channels/references/discord.md`

### Memory search fails
1. Run `openclaw memory status`
2. If no provider, set one explicitly or add API key
3. Run `openclaw memory index --force`
4. Check `memorySearch.remote.baseUrl` is valid
5. Valid providers: local, openai, gemini, voyage, mistral, bedrock
6. See `openclaw-memory/references/memory-config.md`

### Gateway won't start
1. `ps aux | grep openclaw-gateway` — already running?
2. Check `/tmp/openclaw.lock`
3. `python3 -m json.tool /data/.openclaw/openclaw.json` — valid JSON?
4. Check logs for specific error
5. See `openclaw-troubleshooting`

### Plugin disabled (memory slot)
1. Check `plugins.slots.memory` is set to the plugin you want
2. For Honcho: `plugins.slots.memory = "openclaw-honcho"`
3. Restart gateway
4. See `openclaw-plugins/references/plugin-slots.md`

### Wrong agent responding
1. Check `bindings[]` order — first match wins
2. For DM routing: `session.dmScope` collapses DMs if set to `"main"`
3. Peer binding always wins over channel binding
4. See `openclaw-agents/references/multi-agent.md`

### Config changes not taking effect
1. Some changes require gateway restart
2. Changes needing restart: `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*`
3. Dynamic (no restart): `tools.web.search.apiKey`, `agents.defaults.memorySearch.remote`
4. Restart with `openclaw gateway restart` (confirm first!)

### Session context lost
1. Check session grouping: `session.scope` and `session.dmScope`
2. `dmScope: "main"` collapses all DMs to one session
3. Check compaction: `agents.defaults.compaction`
4. Check `memoryFlush` is enabled
5. See `openclaw-concepts/references/session.md`

### Tools not working
1. Check `tools.profile` and `tools.allow`/`tools.deny`
2. Per-agent tools: `agents.list[].tools`
3. Elevated exec: `tools.elevated.enabled` + `tools.elevated.allowFrom`
4. See `openclaw-tools/references/skills.md`

### Cron job not firing
1. Check cron status: `openclaw cron status`
2. Check job `enabled: true`
3. Check `schedule` is valid cron expression
4. Check `sessionTarget` matches payload kind
5. See `openclaw-concepts/references/cron-jobs.md`

## Error code reference

| Error pattern | Likely cause |
|--------------|-------------|
| "plugin disabled (memory slot set to X)" | Slot occupied by another plugin |
| "Port already in use" | Gateway already running |
| "embedding provider not found" | Invalid `memorySearch.provider` |
| "404" on memory search | `memorySearch.remote.baseUrl` wrong |
| "Pairing required" | `dmPolicy: "pairing"` and not approved |
| "Channel not allowed" | Group not in `allowFrom`/`groupAllowFrom` |
| "session not found" | Session expired or wrong session key |
| "Unauthorized" | Wrong bot token or API key |
