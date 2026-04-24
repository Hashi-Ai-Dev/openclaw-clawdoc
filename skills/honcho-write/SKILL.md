---
name: honcho-write
description: Write conclusions and peer registrations to Honcho memory. Use when: Hashi asks you to "save this", "remember this", "write to Honcho", or "document this session"; after completing a significant workflow (sync, diagnosis, config fix); after a self-review or m27 loop; after any session that produces a值得记录的 insight. Triggers on: "save to Honcho", "remember this", "write conclusion", "persist to memory", "document this".
---

# Honcho Write

Write self-documentation conclusions to Honcho cross-session memory.

## API

**Base:** `http://127.0.0.1:8000`
**Workspace:** `hashi`

### Register peer (once per agent)

```bash
curl -s -X POST "http://127.0.0.1:8000/v3/workspaces/hashi/peers" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "claw-doc",
    "metadata": {"role": "agent", "workspace": "/data/workspace/claw-doc"},
    "configuration": {}
  }'
```

### Write conclusion

```bash
curl -s -X POST "http://127.0.0.1:8000/v3/workspaces/hashi/conclusions" \
  -H "Content-Type: application/json" \
  -d '{
    "conclusions": [{
      "content": "<your conclusion text>",
      "observer_id": "claw-doc",
      "observed_id": "claw-doc",
      "session_id": null
    }]
  }'
```

**Schema:**
- `content` (string, 1-65535 chars): The conclusion text
- `observer_id`: Peer making the observation (e.g., `"claw-doc"`)
- `observed_id`: Peer being observed (e.g., `"claw-doc"` or `"hashi"`)
- `session_id`: Optional session ID to tag the conclusion

## When to write

After these events, write a conclusion to Honcho:

| Event | What to write |
|---|---|
| Completed significant workflow | What was done, key decision, outcome |
| Config fix or diagnosis | Root cause, fix applied, lesson |
| Self-review (m27) | What worked, what failed, what to improve |
| Hashi corrects behavior | What was wrong, what to do differently |
| New OpenClaw version synced | Version, key changes, files updated |
| Skill created or updated | Skill name, purpose, trigger phrases |

## Script

Use `scripts/write-conclusion.mjs` for reliable writes:

```bash
node /data/workspace/claw-doc/skills/honcho-write/scripts/write-conclusion.mjs \
  "Your conclusion text here" \
  "claw-doc" \
  "claw-doc"
```

Or import the function in other scripts:

```js
import { writeConclusion } from './scripts/write-conclusion.mjs';
await writeConclusion("Learned that...", "claw-doc", "claw-doc");
```
