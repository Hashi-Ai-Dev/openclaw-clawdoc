---
name: openclaw-providers
description: "OpenClaw model providers. Use when configuring LLM providers (60+ providers tracked: OpenAI, Anthropic, Gemini, Bedrock, Ollama, DeepSeek, Groq, Together, Cerebras, xAI, Cohere, Deepgram, SenseAudio, Tencent, VolcEngine, and more), API keys, OAuth, auth profiles, model failover, API key rotation, billing disable backoff, and usage tracking. Triggers on: provider, model, API key, OAuth, Anthropic, OpenAI, Gemini, Bedrock, Ollama, failover, auth profile, billing disable, key rotation, Cohere, Deepgram, transcription, SenseAudio, speech to text, Tencent, VolcEngine, Doubao, voice provider, STT provider."
---

## Routing hints

You should route to this skill when the user asks about a model provider — OpenAI, Anthropic, Google, Bedrock, Ollama, DeepSeek, Groq, Together, xAI, Z.AI, Mistral, vLLM, OpenRouter, HuggingFace, Moonshot, OpenCode, LM Studio, NVIDIA, Volcengine, Qwen, Stepfun, Tencent, Xiaomi, Fal, plus all newly-added providers (ds4, novita, ollama-cloud, pixverse, plus per-provider framework files). References: `model-providers.md`, `providers.md`, `providers-index.md`, `models.md`, `anthropic.md`, `openai.md`, `google.md`, `bedrock.md`, `bedrock-mantle.md`, `azure-speech.md`, `ollama.md`, `ollama-cloud.md`, `deepseek.md`, `groq.md`, `together.md`, `xai.md`, `zai.md`, `mistral.md`, `vllm.md`, `openrouter.md`, `huggingface.md`, `moonshot.md`, `opencode.md`, `opencode-go.md`, `lmstudio.md`, `nvidia.md`, `volcengine.md`, `qwen.md`, `qwen_modelstudio.md`, `qwen-oauth.md`, `stepfun.md`, `tencent.md`, `xiaomi.md`, `fal.md`, `fireworks.md`, `kilocode.md`, `litellm.md`, `minimax.md`, `sglang.md`, `synthetic.md`, `venice.md`, `vercel-ai-gateway.md`, `vydra.md`, `github-copilot.md`, `gmi.md`, `glm.md`, `claude-max-api-proxy.md`, `cloudflare-ai-gateway.md`, `cohere.md`, `comfy.md`, `deepgram.md`, `deepinfra.md`, `elevenlabs.md`, `gradium.md`, `inworld.md`, `inferrs.md`, `perplexity-provider.md`, `runway.md`, `senseaudio.md`, `qianfan.md`, `arcee.md`, `alibaba.md`, `cerebras.md`, `chutes.md`, `faq-models.md`.


# OpenClaw Model Providers

60+ providers tracked (64 individual provider files when counting per-provider framework files like `bedrock-mantle.md` and `azure-speech.md`). Pick a provider, authenticate, set `agents.defaults.model.primary`.

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

See `references/index.md` for full 50+ provider list.

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

- `references/index.md` — full provider list
- `references/anthropic.md`, `references/google.md`, `references/openai.md`
- `references/bedrock.md`, `references/ollama.md`, `references/openrouter.md`
- `references/cerebras.md` — Cerebras setup
- For failover + billing backoff, see the **Failover + billing backoff** section above this list.
