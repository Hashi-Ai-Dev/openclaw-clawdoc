# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| current | ✅ Security updates |

## Reporting a Vulnerability

If you discover a security vulnerability in ClawDoc:

1. **Do NOT** open a public GitHub issue
2. Email the maintainer directly via Discord or the OpenClaw community
3. Include a description of the vulnerability and steps to reproduce
4. Allow 48 hours for initial response

## Security Best Practices for ClawDoc Users

When deploying ClawDoc:

- **Never commit credentials** to the `skills/` directory — use SecretRefs (`secret:name` pattern) instead of plaintext API keys
- **Review `plugins.allow`** before installing third-party plugins — only allow plugins from trusted sources
- **Run `openclaw gateway` with a token** in production, not in open/unauthenticated mode
- **Use `~/.openclaw/openclaw.json`** for config, not `/data/.openclaw/` — the latter is a local system path

## Config Security Notes

ClawDoc documents OpenClaw's configuration schema. When configuring channels (Discord, Telegram, etc.):

- Use bot tokens, not personal account credentials
- Store sensitive config values as SecretRefs where supported
- Never commit example configs with real tokens — all example files in this repo use placeholder values

## Scope

This security policy covers the ClawDoc knowledge base agent and its documentation. The underlying OpenClaw project has its own security policy at [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw).
