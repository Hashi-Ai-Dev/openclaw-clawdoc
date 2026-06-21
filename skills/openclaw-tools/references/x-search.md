---
summary: "X search tool — X (Twitter) post search via the Grok provider or standalone"
read_when:
  - You want to search recent X (Twitter) posts from inside an OpenClaw session
  - You need to wire x_search as part of the `group:web` policy
  - You are configuring Grok and want to enable its optional X search
title: "x_search"
---

`x_search` is the X (Twitter) search tool. It lets OpenClaw agents query recent posts by query, hashtag, author, or time range. The tool ships as part of the `grok` provider bundle — when you enable Grok, x_search is available.

| Property         | Value                                            |
| ---------------- | ------------------------------------------------ |
| Tool name        | `x_search`                                       |
| Bundled in       | `grok` provider                                  |
| Auth             | Same as Grok (`XAI_API_KEY`)                     |
| API              | X (Twitter) API via Grok                          |
| Default limit    | 20 results per call                              |
| Max limit        | 100 results per call                             |

## When to use x_search vs web_search

- **`x_search`** — recent public posts on X, time-bounded, public-only. Use for: sentiment on a topic, recent announcements, hashtag trends, author lookups.
- **`web_search`** — general web results (Google/Bing/Brave/Exa/etc.). Use for: documentation, articles, anything not on X.

The two tools are complementary. Most agents enable both via the `group:web` policy.

## Enable

`x_search` requires the Grok provider. Enable Grok, then make sure `x_search` is in your tool allowlist:

```bash
openclaw plugins enable grok
```

```json5
{
  tools: {
    policy: {
      "group:web": {
        enabled: true,
        members: ["web_search", "web_fetch", "x_search"]
      }
    }
  }
}
```

Without `x_search` in the allowlist, the tool is available to the model but blocked at execution time. The agent will see it in the function-call list and get a "permission denied" error.

## Usage

The model invokes `x_search` directly:

```text
x_search(query="OpenClaw", limit=20, time="last_24h")
```

Parameters:

| Parameter | Type | Notes |
|-----------|------|-------|
| `query` | string | Search terms. Supports X advanced search operators (`from:user`, `since:date`, `until:date`, `min_faves:N`, etc.) |
| `limit` | int | 1-100. Default 20. |
| `time` | string | One of: `last_hour`, `last_24h`, `last_7d`, `last_30d`. Default `last_7d`. |
| `lang` | string | ISO 639-1 code (e.g., `en`, `ja`). Optional. |

Example: "what did @openclaw post about Codex in the last week":

```text
x_search(query="from:openclaw Codex", time="last_7d", limit=20)
```

## Output format

The tool returns an array of post objects:

```json
[
  {
    "id": "1234567890",
    "author": "@openclaw",
    "text": "...",
    "created_at": "2026-06-15T12:34:56Z",
    "faves": 42,
    "retweets": 5,
    "url": "https://x.com/openclaw/status/1234567890"
  }
]
```

Post text is truncated at 280 chars in the output; the model can `web_fetch` the full URL for longer threads.

## Limitations

- **Public posts only.** Private/protected accounts are not searchable.
- **No DMs, no bookmarks, no replies-only filter** in the current implementation.
- **Rate limits** apply per `XAI_API_KEY`. Default limits: 100 calls/minute. Check Grok's plan for higher tiers.
- **Cost:** x_search calls are billed like Grok inference. Check your plan.

## See also

- [Grok provider](/providers/grok)
- [Web search policy](/gateway/config-tools)
- [web_search tool](/tools/web-search)