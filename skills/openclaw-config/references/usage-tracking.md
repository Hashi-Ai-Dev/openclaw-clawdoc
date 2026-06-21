---
summary: "Usage tracking surfaces and credential requirements"
read_when:
  - You are wiring provider usage/quota surfaces
  - You need to explain usage tracking behavior or auth requirements
title: "Usage Tracking"
---

# Usage tracking

## What it is

- Pulls provider usage/quota directly from their usage endpoints.
- No estimated costs; only provider-reported quota windows or account-state
  summaries.
- Human-readable quota-window status output is normalized to `X% left`, even
  when an upstream API reports consumed quota, remaining quota, or only raw
  counts. Providers without resettable quota windows can show provider summary
  text instead, such as a balance.
- Session-level `/status` and `session_status` can fall back to the latest
  transcript usage entry when the live session snapshot is sparse. That
  fallback fills missing token/cache counters, can recover the active runtime
  model label, and prefers the larger prompt-oriented total when session
  metadata is missing or smaller. Existing nonzero live values still win.

## Where it shows up

- `/status` in chats: emoji‑rich status card with session tokens + estimated cost (API key only). Provider usage shows for the **current model provider** when available as a normalized `X% left` window.
- `/usage off|tokens|full` in chats: per-response usage footer (OAuth shows tokens only).
- `/usage cost` in chats: local cost summary aggregated from OpenClaw session logs.
- CLI: `openclaw status --usage` prints a full per-provider breakdown.
- CLI: `openclaw channels list` prints the same usage snapshot alongside provider config (use `--no-usage` to skip).
- macOS menu bar: "Usage" section under Context (only if available).

## Custom `/usage full` footer

`/usage full` shows a built-in compact footer with model, reasoning, fast/slow,
context window, turn tokens, cache, and cost when those fields are available. No
template file is required.

`messages.usageTemplate` is only for advanced custom layouts. The value is a
JSON file path (supports `~`) or an inline object, and it replaces the built-in
footer when valid:

```json
{
  "messages": {
    "usageTemplate": "~/.openclaw/usage-footer.json"
  }
}
```

Missing or empty templates fall back to the built-in footer quietly. Unreadable
or invalid configured templates also fall back to the built-in footer and emit an
operator warning.

Start custom templates from the built-in shape, then edit the parts you want
to change:

```json
{
  "messages": {
    "usageTemplate": {
      "model": "{{model}}",
      "reasoning": "{{reasoningEffort}}",
      "speed": "{{speedLabel}}",
      "context": "{{contextSummary}}",
      "turnTokens": "{{turnTokensSummary}}",
      "cache": "{{cacheSummary}}",
      "cost": "{{costSummary}}"
    }
  }
}
```

Available placeholders:

- `model`: resolved model id (after alias / fallback resolution).
- `reasoningEffort`: reasoning tier label (`low` / `medium` / `high` / `xhigh`),
  when the active model reports one.
- `speedLabel`: `fast` or `slow` based on the active profile mapping.
- `contextSummary`: filled/window summary for the active session.
- `turnTokensSummary`: per-turn token totals for the most recent assistant
  message.
- `cacheSummary`: cache read/write totals when the model reports them.
- `costSummary`: cost line (`$0.0123`, API-key sessions only).

Templates are rendered through the same redaction pipeline as built-in usage
output. Keep them small; large templates are clipped to a single footer line.

## Providers + credentials

- **Anthropic (Claude)**: OAuth tokens in auth profiles.
- **GitHub Copilot**: OAuth tokens in auth profiles.
- **Gemini CLI**: OAuth tokens in auth profiles.
  - JSON usage falls back to `stats`; `stats.cached` is normalized into
    `cacheRead`.
- **OpenAI Codex**: OAuth tokens in auth profiles (accountId used when present).
- **MiniMax**: API key or MiniMax OAuth auth profile. OpenClaw treats
  `minimax`, `minimax-cn`, and `minimax-portal` as the same MiniMax quota
  surface, prefers stored MiniMax OAuth when present, and otherwise falls back
  to `MINIMAX_CODE_PLAN_KEY`, `MINIMAX_CODING_API_KEY`, or `MINIMAX_API_KEY`.
  MiniMax's raw `usage_percent` / `usagePercent` fields mean **remaining**
  quota, so OpenClaw inverts them before display; count-based fields win when
  present.
  - Coding-plan window labels come from provider hours/minutes fields when
    present, then fall back to the `start_time` / `end_time` span.
  - If the coding-plan endpoint returns `model_remains`, OpenClaw prefers the
    chat-model entry, derives the window label from timestamps when explicit
    `window_hours` / `window_minutes` fields are absent, and includes the model
    name in the plan label.
- **Xiaomi MiMo**: API key via env/config/auth store (`XIAOMI_API_KEY`).
- **z.ai**: API key via env/config/auth store.

Usage is hidden when no usable provider usage auth can be resolved. Providers
can supply plugin-specific usage auth logic; otherwise OpenClaw falls back to
matching OAuth/API-key credentials from auth profiles, environment variables,
or config.
