# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| current | ✅ Security updates |

## Reporting a Vulnerability

If you discover a security vulnerability in ClawDoc:

1. **Do NOT** open a public GitHub issue. Public disclosure before a fix is available puts users at risk.
2. **Preferred channels (in order):**
   1. **GitHub Security Advisories** on this repo — `https://github.com/Hashi-Ai-Dev/openclaw-clawdoc/security/advisories/new`. This gives you a private thread, a CVE request flow, and an audit trail.
   2. **Email:** `security@openclaw.ai` (routed to the OpenClaw maintainers; ClawDoc shares this channel since it is part of the OpenClaw distribution).
3. **What to include:** affected component, version, commit SHA if known; reproduction steps or proof-of-concept; the actual impact and which trust boundary is crossed; your contact info if you want a follow-up.
4. **Expected response:** an acknowledgement within 72 hours. Triage and a fix or mitigation timeline within 7 days for valid reports. We coordinate disclosure with you on a fix timeline.
5. Discord and the OpenClaw community are **not** appropriate primary channels for security reports — messages there are public, ephemeral, and may not reach the right maintainer quickly. Use them only as a last resort and ask for a private follow-up channel.

## Security Best Practices for ClawDoc Users

When deploying ClawDoc:

- **Never commit credentials** to the `skills/` directory — use SecretRefs (`secret:name` pattern) instead of plaintext API keys
- **Review `plugins.allow`** before installing third-party plugins — only allow plugins from trusted sources
- **Run `openclaw gateway` with a token** in production, not in open/unauthenticated mode
- **Use `~/.openclaw/openclaw.json`** for config, not `/data/.openclaw/` — the latter is a local system path

## Third-Party Plugin Policy

ClawDoc documentation may describe OpenClaw's plugin architecture and mechanisms. However:

- Do not recommend specific third-party plugins unless they are officially maintained by OpenClaw or explicitly audited and allowlisted by this repo.
- Do not include install commands for plugins that run eval-based installers or fetch code from untrusted URLs.
- Link to the official plugin registry at https://docs.openclaw.ai/plugins/ instead of recommending specific third-party tools.

When in doubt, leave it out. Operator security decisions are outside the scope of this documentation repo.

## Config Security Notes

ClawDoc documents OpenClaw's configuration schema. When configuring channels (Discord, Telegram, etc.):

- Use bot tokens, not personal account credentials
- Store sensitive config values as SecretRefs where supported
- Never commit example configs with real tokens — all example files in this repo use placeholder values

## Scope

This security policy covers the ClawDoc knowledge base agent and its documentation. The underlying OpenClaw project has its own security policy at [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw).
