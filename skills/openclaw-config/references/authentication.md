---
summary: "Model authentication: OAuth, API keys, Claude CLI reuse, and Anthropic setup-token"
read_when:
  - Debugging model auth or OAuth expiry
  - Documenting authentication or credential storage
title: "Authentication"
---

> **Note:** This page is the **model provider** authentication reference (API
> keys, OAuth, Claude CLI reuse, and Anthropic setup-token). For **gateway
> connection** authentication (token, password, trusted-proxy), see
> `gateway.md` and `trusted-proxy-auth.md`.

OpenClaw supports OAuth and API keys for model providers. For always-on
gateway hosts, API keys are usually the most predictable option.
Subscription/OAuth flows are also supported when they match your provider
account model.

For the full OAuth flow and storage layout, see `oauth.md`. For SecretRef-based
auth (`env`/`file`/`exec` providers), see `secrets.md`. For credential
eligibility/reason-code rules used by `models status --probe`, see
`auth-credential-semantics.md`.

## Recommended setup (API key, any provider)

For long-lived gateways, start with an API key:

1. Create an API key in your provider console.
2. Add the provider to your config:

```json5
{
  providers: {
    "your-provider": {
      apiKey: "YOUR_PROVIDER_KEY",
      models: [{ id: "model-id" }],
    },
  },
}
```

3. Verify with `openclaw models status --probe`.

## Anthropic: setup-token and Claude CLI reuse

For Anthropic specifically, you have three options:

1. **API key** (recommended for servers): set `ANTHROPIC_API_KEY` in env or
   use a SecretRef.
2. **Claude CLI reuse**: if you've already logged in with `claude` CLI, set
   `claudeCli: true` in the Anthropic provider block. OpenClaw reuses the
   existing OAuth token.
3. **Setup-token**: for short-lived Claude Max/Pro sessions, use
   `setup-token` mode. The token is short-lived (~1h) and must be rotated
   often.

## OAuth (other providers)

For OAuth-supporting providers (OpenAI, Google, etc.):

1. Run `openclaw auth login --provider <name>`.
2. The browser-based flow walks you through provider-side consent.
3. OpenClaw stores the resulting token in `auth-profiles.json` with a
   default expiry.

To check token status:

```bash
openclaw auth status
openclaw auth status --provider openai --json
```

Tokens near expiry show a clear warning. Re-run `openclaw auth login` to
refresh.

## Credential eligibility

`openclaw models status --probe` reports whether each configured model has a
working credential. Reasons include:

- `ok` — credential present and validated
- `missing` — no credential for this provider
- `expired` — OAuth token past expiry; re-login required
- `quota` — provider reports quota exhausted
- `network` — temporary network/auth error; will retry
- `unsupported` — credential format not supported (e.g. legacy token)

## Storage layout

- API keys: `~/.openclaw/openclaw.json` (or SecretRef)
- OAuth tokens: `~/.openclaw/auth-profiles.json` (0600 permissions)
- Claude CLI reuse: reads from `~/.claude/.credentials.json`

Never check credentials into git. `openclaw secrets audit --check` will catch
plaintext leaks in tracked config files.