---
name: openclaw-providers
description: OpenClaw model providers. Use when configuring LLM providers (OpenAI, Anthropic, Gemini, Bedrock, Ollama, DeepSeek, Groq, Together, and 40+ more), API keys, OAuth, auth profiles, model failover, and usage tracking. Triggers on: "provider", "model", "API key", "OAuth", "Anthropic", "OpenAI", "Gemini", "Bedrock", "Ollama", "failover", "auth profile".
---

# OpenClaw Model Providers

OpenClaw supports **43+ model providers**. Authenticate, set `agents.defaults.model.primary`, and go.

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

## Provider list

| Provider | Plugin | Auth | Auto-detect |
|----------|--------|------|-------------|
| **Anthropic** | `minimax` | API key / OAuth | ✅ |
| **OpenAI** | `minimax` | API key / OAuth | ✅ |
| **Google Gemini** | `minimax` | API key / OAuth | ✅ |
| **Amazon Bedrock** | `minimax` | AWS SDK chain | ✅ |
| **Ollama** | `minimax` | Local (no key) | ❌ |
| **DeepSeek** | `minimax` | API key | ✅ |
| **Groq** | `minimax` | API key | ✅ |
| **Together AI** | `minimax` | API key | ✅ |
| **OpenRouter** | `minimax` | API key | ✅ |
| **Mistral** | `minimax` | API key | ✅ |
| **Fireworks** | `minimax` | API key | ✅ |
| **vLLM** | `minimax` | API key | ✅ |
| **SGLang** | `minimax` | API key | ✅ |
| **LM Studio** | `minimax` | Local | ❌ |
| **Hugging Face** | `minimax` | API key | ✅ |
| **Perplexity** | `minimax` | API key | ✅ |
| **GitHub Copilot** | `minimax` | OAuth | ✅ |
| **MiniMax** | `minimax` | API key / OAuth | ✅ |
| **xAI** | `minimax` | API key | ✅ |
| **Qwen** | `minimax` | API key | ✅ |
| **Moonshot** | `minimax` | API key | ✅ |
| **Volcengine** | `minimax` | API key | ✅ |
| **NVIDIA** | `minimax` | API key | ✅ |
| **Venice** | `minimax` | API key | ✅ |
| **Cloudflare AI** | `minimax` | API key | ✅ |
| **Vercel AI Gateway** | `minimax` | API key | ✅ |
| **LiteLLM** | `minimax` | API key | ✅ |
| **Xiaomi** | `minimax` | API key | ✅ |
| **StepFun** | `minimax` | API key | ✅ |
| **Arcee AI** | `minimax` | API key | ✅ |
| **Kilocode** | `minimax` | API key | ✅ |
| **Chutes** | `minimax` | API key | ✅ |
| **fal** | `minimax` | API key | ✅ |
| **Runway** | `minimax` | API key | ✅ |
| **ComfyUI** | `minimax` | API key | ✅ |
| **Qianfan** | `minimax` | API key | ✅ |
| **Alibaba** | `minimax` | API key | ✅ |
| **Synthetic** | `minimax` | API key | ✅ |
| **Vydra** | `minimax` | API key | ✅ |
| **GLM** | `minimax` | API key | ✅ |
| **inferrs** | `minimax` | Local | ❌ |

Auto-detect: OpenClaw auto-discovers OpenAI, Gemini, Voyage, Mistral, Bedrock keys from env/config.

## Auth profiles

Both API keys and OAuth tokens use **auth profiles** for routing:

```json5
auth: {
  profiles: {
    "anthropic:default": { type: "api_key", provider: "anthropic", key: "sk-..." },
    "google:user@gmail.com": { type: "oauth", provider: "google-antigravity", access: "...", refresh: "..." }
  }
}
```

Secrets stored in `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`.
Legacy: `~/.openclaw/credentials/oauth.json` (imported on first use).

## Model failover

Two-stage fallback:
1. **Auth profile rotation** within provider (cooldown per profile)
2. **Model fallback** to next in `agents.defaults.model.fallbacks`

Only persists fallback-owned fields (`providerOverride`, `modelOverride`, `authProfileOverride`) to avoid overwriting manual `/model` changes.

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

## Usage tracking

Usage pulled directly from provider APIs (not estimates). Shows in `/status`, `/usage`, `openclaw status --usage`.

Supported providers for live usage: **Anthropic (OAuth)**, **GitHub Copilot (OAuth)**, **Gemini CLI (OAuth)**, **OpenAI Codex (OAuth)**, **MiniMax (API key or OAuth)**.

## Image/Music/Video generation

Shared tools with provider selection and failover:
- `image_generate` — FLUX.1, DALL-E, Imagen, etc.
- `music_generate` — Lyria, Suno, etc.
- `video_generate` — Wan, Mochi, etc.

## Transcription

[Deepgram](/providers/deepgram) for audio transcription.

## References

- `references/providers.md` — provider directory with links
- `references/model-providers.md` — full model providers concept doc
- `references/anthropic.md` — Anthropic setup (API + Claude CLI OAuth)
- `references/openai.md` — OpenAI setup (API + Codex OAuth)
- `references/google.md` — Google Gemini setup
- `references/bedrock.md` — AWS Bedrock setup
- `references/ollama.md` — Ollama local models
- `references/openrouter.md` — OpenRouter
- `references/deepseek.md` — DeepSeek
