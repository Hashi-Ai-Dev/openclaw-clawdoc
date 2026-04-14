---
name: openclaw-providers
description: OpenClaw model providers. Use when configuring LLM providers (43+ providers: OpenAI, Anthropic, Gemini, Bedrock, Ollama, DeepSeek, Groq, Together, Cerebras, xAI, and more), API keys, OAuth, auth profiles, model failover, API key rotation, billing disable backoff, and usage tracking. Triggers on: "provider", "model", "API key", "OAuth", "Anthropic", "OpenAI", "Gemini", "Bedrock", "Ollama", "failover", "auth profile", "billing disable", "key rotation".
---

# OpenClaw Model Providers

43+ providers supported. Pick a provider, authenticate, set `agents.defaults.model.primary`.

## Quick setup

```bash
openclaw onboard          # Interactive auth setup
openclaw models status    # Check provider auth status
```

```json5
agents: {
  defaults: {
    model: {
      primary: "anthropic/claude-sonnet-4-7",
      fallbacks: ["openai/gpt-4o-mini"]
    }
  }
}
```

## Complete provider list

| Provider | Plugin | Auth | Auto-detect |
|----------|--------|------|-------------|
| **Anthropic** | `anthropic` | API key / OAuth (Claude CLI) | ✅ |
| **OpenAI** | `openai` | API key / OAuth (Codex) | ✅ |
| **Google Gemini** | `google` | API key / OAuth / gcloud ADC | ✅ |
| **Amazon Bedrock** | `bedrock` | AWS SDK chain | ✅ |
| **Ollama** | `ollama` | Local (no key) | ❌ |
| **DeepSeek** | `deepseek` | API key | ✅ |
| **Groq** | `groq` | API key | ✅ |
| **Together AI** | `together` | API key | ✅ |
| **OpenRouter** | `openrouter` | API key | ✅ |
| **Mistral** | `mistral` | API key | ✅ |
| **Fireworks** | `fireworks` | API key | ✅ |
| **vLLM** | `vllm` | API key | ❌ |
| **SGLang** | `sglang` | API key | ❌ |
| **LM Studio** | `lmstudio` | Local | ❌ |
| **Hugging Face** | `huggingface` | API key | ✅ |
| **Perplexity** | `perplexity` | API key | ✅ |
| **GitHub Copilot** | `github-copilot` | OAuth | ✅ |
| **MiniMax** | `minimax` | API key | ✅ |
| **MiniMax Portal** | `minimax` | OAuth | ✅ |
| **xAI** | `xai` | API key | ✅ |
| **Qwen** | `qwen` | API key | ✅ |
| **Moonshot (Kimi)** | `moonshot` | API key | ✅ |
| **Kimi Coding** | `moonshot` | API key | ✅ |
| **Volcengine** | `volcengine` | API key | ✅ |
| **NVIDIA** | `nvidia` | API key | ✅ |
| **Venice** | `venice` | API key | ✅ |
| **Cloudflare AI** | `cloudflare-ai-gateway` | API key | ✅ |
| **Vercel AI Gateway** | `vercel-ai-gateway` | API key | ✅ |
| **LiteLLM** | `litellm` | API key | ✅ |
| **Xiaomi** | `xiaomi` | API key | ✅ |
| **StepFun** | `stepfun` | API key | ✅ |
| **Arcee AI** | `arcee` | API key | ✅ |
| **Kilocode** | `kilocode` | API key | ✅ |
| **Chutes** | `chutes` | API key | ✅ |
| **fal** | `fal` | API key | ✅ |
| **Runway** | `runway` | API key | ✅ |
| **ComfyUI** | `comfyui` | API key | ✅ |
| **Qianfan** | `qianfan` | API key | ✅ |
| **Alibaba** | `alibaba` | API key | ✅ |
| **Synthetic** | `synthetic` | API key | ✅ |
| **Vydra** | `vydra` | API key | ✅ |
| **GLM** | `glm` | API key | ✅ |
| **Cerebras** | `cerebras` | API key | ✅ |
| **BytePlus** | `byteplus` | API key | ✅ |
| **OpenCode (Zen)** | `opencode` | API key | ✅ |
| **OpenCode Go** | `opencode-go` | API key | ✅ |
| **inferrs** | `inferrs` | Local | ❌ |
| **Deepgram** | `deepgram` (transcription) | API key | ✅ |
| **Z.AI** | `zai` | API key | ✅ |

Auto-detect: OpenClaw auto-discovers OpenAI, Gemini, Voyage, Mistral, Bedrock keys from env.

---

## API Key Rotation

```bash
# Multiple keys via comma/semicolon list
OPENAI_API_KEYS="sk-1,s k-2,s k-3"
# Or numbered
OPENAI_API_KEY_1=...; OPENAI_API_KEY_2=...
# Live override (takes priority over all)
OPENCLAW_LIVE_OPENAI_KEY=sk-live
```

**Rotation triggers on rate-limit responses only:**
- HTTP 429
- Error messages: `rate_limit`, `quota`, `resource exhausted`, `Too many concurrent requests`, `ThrottlingException`, `concurrency limit reached`, `workers_ai ... quota limit exceeded`

**Non-rate-limit errors → fail immediately, no rotation.**

---

## Auth Profile Precedence

Profile selection order (most specific first):
1. Explicit `auth.order[provider]` in config
2. Configured `auth.profiles` entries
3. Round-robin: OAuth > API key, ordered by `usageStats.lastUsed`

**Profile ID format:** `provider:default` (no email) or `provider:<email>` (OAuth).

```json5
auth: {
  order: { openai: ["openai:default", "openai:work@corp.com"] },
  profiles: {
    "openai:default": { type: "api_key", provider: "openai", key: "sk-..." },
    "openai:work@corp.com": { type: "oauth", provider: "openai-codex", access: "...", refresh: "..." }
  }
}
```

User-pinned profiles via `/model ...@<profileId>` lock to that profile. Auto-pinned profiles can rotate on rate limits.

---

## Model Failover

Two-stage fallback:

**Stage 1 — Auth profile rotation within provider**
- Only triggers on rate-limit responses
- Respects `auth.cooldowns.billingBackoffHours` per profile

**Stage 2 — Model fallback to next in `fallbacks[]`**
```json5
agents: {
  defaults: {
    model: {
      primary: "anthropic/claude-opus-4-0",
      fallbacks: [
        { provider: "openai", model: "gpt-4o" },
        { provider: "google", model: "gemini-2.5-pro" }
      ]
    }
  }
}
```

Only persists fallback-owned fields (`providerOverride`, `modelOverride`, `authProfileOverride`) — does NOT overwrite manual `/model` changes.

**Persisted fallback fields:** `providerOverride`, `modelOverride`, `authProfileOverride`, `authProfileOverrideSource`, `authProfileOverrideCompactionCount`

---

## Billing Disable Backoff

When a provider returns a billing error (5xx on usage endpoint, or text-matched `insufficient_usage`):

```
5h → 10h → 20h → 24h (cap) → 24h no-failure → reset
```

- Doubles on each repeated failure
- Resets after 24h with no failures
- Text-matched even on non-402 responses

**Rate-limit cooldowns:** Exponential backoff per profile: 1m → 5m → 25m → 1h cap.

---

## `/fast` Toggle by Provider

| Provider | Effect |
|----------|--------|
| Anthropic | `service_tier: "economy"` on request |
| OpenAI | `service_tier: "priority"` on request |
| xAI | `grok-3/4` → `grok-3/4-fast` model rewrite |
| MiniMax | `MiniMax-M2.7` → `MiniMax-M2.7-highspeed` rewrite |
| Others | Provider-specific handling |

---

## models.mode — merge vs replace

Controls how `models.providers` entries combine with built-in `models.json`:

```json5
models: {
  mode: "merge",   // deep-merge: add/override fields
  mode: "replace"  // full replacement of built-in model entries
}
```

---

## Provider-Owned Hooks (advanced)

Providers can implement hooks that influence failover behavior:

| Hook | Purpose |
|------|---------|
| `matchesContextOverflowError` | Provider-specific context overflow detection |
| `classifyFailoverReason` | Categorize errors as rate-limit vs. billing vs. auth |
| `buildMissingAuthMessage` | Custom recovery hints for missing auth |
| `isCacheTtlEligible` | Whether provider supports cached responses |
| `suppressBuiltInModel` | Hide built-in model from catalog |
| `augmentModelCatalog` | Add/filter models at runtime |
| `isBinaryThinking` | Whether model uses binary thinking tokens |
| `supportsXHighThinking` | Whether x-high thinking is supported |
| `prepareRuntimeAuth` | Transform credential → runtime token |
| `resolveUsageAuth` | Which auth to use for usage API calls |

---

## Usage Tracking

Usage pulled directly from provider APIs (not estimates). Shows in `/status`, `/usage`, `openclaw status --usage`.

Live usage supported: **Anthropic (OAuth)**, **GitHub Copilot (OAuth)**, **Gemini CLI (OAuth)**, **OpenAI Codex (OAuth)**, **MiniMax (API key or OAuth)**.

---

## Image / Music / Video / Transcription

| Tool | Providers |
|------|-----------|
| `image_generate` | FLUX.1, DALL-E, Imagen, etc. |
| `music_generate` | Lyria, Suno, etc. |
| `video_generate` | Wan, Mochi, etc. |
| `transcription` | Deepgram |

---

## References

Load these for detailed topics:
- `references/providers.md` — full provider directory
- `references/model-providers.md` — model providers concept doc
- `references/model-failover.md` — model failover + billing disable
- `references/retry.md` — retry policy per provider
- `references/anthropic.md`, `references/google.md`, `references/openai.md` — setup guides
- `references/bedrock.md`, `references/ollama.md`, `references/openrouter.md`
- `references/deepgram.md` — transcription
- `references/inferrs.md` — local models
