# Honcho Crash Analysis — 2026-04-16

## Timeline (from Railway logs)

### Container Restart Sequence
1. **~20:13 UTC** — System sends SIGTERM to gateway (graceful shutdown)
2. **~20:13 UTC** — `[gateway] signal SIGTERM received; shutting down`
3. **~20:38 UTC** — Gateway restarts after ~25 minutes downtime

### Resource Spikes (from Usage graphs)
- **CPU:** Normal ~0.0 vCPU → spike to **4.6 vCPU** at Apr 16 ~7:46 AM
- **RAM:** Normal ~4 GB → spike to **20.63 GB** at Apr 16 ~7:46 AM
- **Network egress:** cumulative ~20GB (significant outbound traffic)
- **Volume:** stepped increase to ~7GB

### Error at shutdown
```
[media-understanding] image: failed (0/1) reason=Model does not support images
```

## Root Causes

### 1. PostgreSQL Not Auto-Started After Container Restart
**Severity: CRITICAL**
- When container restarts, PostgreSQL doesn't auto-start
- Honcho deriver crashes with `connection refused` on port 5432
- Uvicorn API server DOES start (port 8000 bound), but backend is broken
- Everything appears "running" but queue isn't processing

**Fix:** PostgreSQL must be restarted manually OR via startup script:
```bash
pg_ctlcluster 15 main start
```

### 2. Image Analysis Failure — Multimodal Disabled
**Severity: HIGH**
- `memorySearch.multimodal.enabled = false` in agent defaults
- When image tool was invoked, it tried to use minimax model (non-multimodal)
- Error: `Model does not support images`
- This broke image understanding in conversations

**Fix:** Enable multimodal in agents config:
```json
"memorySearch": {
  "multimodal": {
    "enabled": true
  }
}
```

### 3. Honcho API Started Before PostgreSQL
**Severity: HIGH**
- Uvicorn bound to port 8000 first (startup race condition)
- PostgreSQL wasn't ready, so `/health` returned ok but DB ops failed
- Queue got stuck, new items accumulated, load increased

### 4. Honcho Queue Backlog (from earlier Groq failure)
**Severity: MEDIUM**
- Groq API key was invalid (401) since ~Apr 14
- Queue backed up to ~1800 pending items
- When OpenRouter fix was applied, sudden surge of processing
- Combined with PostgreSQL not ready = chaos

## What Needs Fixing

1. **[x] Startup Script** — Created at `/data/workspace/tools/honcho-startup.sh` ✅
   - Auto-starts PostgreSQL, waits for it, then starts Honcho API + Deriver
   - Run after every container restart

2. **[x] Enable Multimodal** — Fixed in openclaw.json ✅
   - Set `memorySearch.multimodal.enabled = true`

3. **[ ] Railway Health Check Tuning** — Prevent premature restarts
   - Gateway needs to respond to health checks under heavy load
   - Consider adding a lightweight health endpoint that skips heavy ops

4. **[ ] CodeGod Subagent Concurrency Limit**
   - 142 CodeGod sessions were created during sprint
   - Multiple ONNX model builds + embedding generation ran simultaneously
   - This caused the 10+ vCPU spike and memory to climb to 20GB
   - Consider capping max concurrent subagents during heavy workloads

5. **[ ] Clean up unused Groq keys** — `LLM_GROQ_API_KEY` and `GROQ_API_KEY` still in .env but not used
   - No functional impact but should be removed for hygiene

## Root Cause Summary

| Event | Cause | Severity |
|---|---|---|
| Container restart | Railway health check failed under heavy load (CodeGod sprint + Honcho backlog) | Root cause |
| Resource spike (10+ vCPU, 20GB RAM) | CodeGod running 10+ subagents with ONNX builds + embeddings simultaneously | Contributing cause |
| Image analysis failure | `multimodal.enabled = false` in agent defaults | Secondary cause |
| Honcho down after restart | PostgreSQL didn't auto-start; deriver crashed on DB connection | Direct cause |
| Groq key unused | Switched to OpenRouter; Groq keys left in .env unused | No impact |