---
name: openclaw-providers
description: OpenClaw model providers. Use when configuring LLM providers (50+ providers: OpenAI, Anthropic, Gemini, Bedrock, Ollama, DeepSeek, Groq, Together, Cerebras, xAI, and more), API keys, OAuth, auth profiles, model failover, API key rotation, billing disable backoff, and usage tracking. Triggers on: "provider", "model", "API key", "OAuth", "Anthropic", "OpenAI", "Gemini", "Bedrock", "Ollama", "failover", "auth profile", "billing disable", "key rotation".
---

# OpenClaw Model Providers

50+ providers. Pick a provider, authenticate, set `agents.defaults.model.primary`.

## Quick setup

```bash
openclaw onboard          # Interactive auth
openclaw models status    # Check auth status
```

```json5
agents: {
  defaults: {
    model: { primary: "anthropic/claude-sonnet-4-7", fallbacks: ["openai/gpt-4o-mini"] }
  }
}
```

## Top providers

| Provider | Auth | Auto-detect |
|----------|------|-------------|
| Anthropic | API key / OAuth | ✅ |
| OpenAI | API key / OAuth | ✅ |
| Google Gemini | API key / OAuth | ✅ |
| Amazon Bedrock | AWS SDK | ✅ |
| Ollama | Local (no key) | ❌ |
| DeepSeek | API key | ✅ |
| Groq | API key | ✅ |
| OpenRouter | API key | ✅ |
| Mistral | API key | ✅ |
| Cerebras | API key | ✅ |
| xAI | API key | ✅ |
| LM Studio | Local | ❌ |
| vLLM / SGLang | API key | ❌ |

See `references/providers/index.md` for full 50+ provider list.

## Model failover (two-stage)

**Stage 1:** Auth profile rotation within provider (rate-limit only)
**Stage 2:** Model fallback to next in `fallbacks[]`:
```json5
{ primary: "anthropic/claude-opus-4-0", fallbacks: [{ provider: "openai", model: "gpt-4o" }] }
```
Fallbacks only persist fallback-owned fields — does NOT override manual `/model`.

## API key rotation

```bash
OPENAI_API_KEYS="sk-1,sk-2,sk-3"   # comma/semicolon list
```
Triggers on 429 or text-matched rate-limit errors. Non-429 errors fail immediately.

## Auth profiles (precedence: explicit > configured > round-robin)

```json5
auth: {
  order: { openai: ["openai:default", "openai:work@corp.com"] },
  profiles: {
    "openai:default": { type: "api_key", provider: "openai", key: "sk-..." }
  }
}
```

## Billing disable backoff

On billing errors: `5h → 10h → 20h → 24h cap`. Resets after 24h no-failure.

## `/fast` toggle

| Provider | Effect |
|----------|--------|
| Anthropic | `service_tier: "economy"` |
| OpenAI | `service_tier: "priority"` |
| xAI / MiniMax | Model rewrite to -fast variant |

## Usage tracking

Direct from provider API (not estimates). Supported: **Anthropic OAuth**, **GitHub Copilot OAuth**, **Gemini CLI OAuth**, **OpenAI Codex OAuth**, **MiniMax**.

## References

- `references/providers/index.md` — full 50+ provider list
- `references/model-failover.md` — failover + billing backoff
- `references/anthropic.md`, `references/google.md`, `references/openai.md`
- `references/bedrock.md`, `references/ollama.md`, `references/openrouter.md`
- `references/cerebras.md` — Cerebras setup
