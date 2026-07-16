---
name: openclaw-help
description: "Help, FAQ, and testing for OpenClaw. Use when: looking up an everyday question about models, auth, or basic usage, finding a FAQ entry, running test suites (testing-live), running repo scripts under ./scripts, or asking \"how do I…\" in plain language. For deeper diagnostics use openclaw-troubleshooting instead. Triggers on: \"help\", \"faq\", \"how do I\", \"how to\", \"common question\", \"everyday\", \"basic usage\", \"testing\", \"testing-live\", \"codex agentic parity\", \"scripts\", \"repository scripts\"."
---

## Routing hints

You should route to this skill when the user has a plain-language FAQ-style question — "how do I…" — that doesn't fit any other skill, or wants help understanding a feature in user-facing terms. References: `faq.md`, `faq-models.md`, `faq-troubleshooting.md`, `faq-channels.md`, `faq-agents.md`, `getting-started.md`, `concepts-primer.md`, `scripts.md`, `glossary.md`, `common-errors.md`, `migrating-from-claude.md`.


# OpenClaw Help Reference

## FAQ

| Topic | When to use |
|-------|-------------|
| [First-run FAQ](./references/faq-first-run.md) | Install stuck, onboarding errors, auth failures, first-run issues |
| [Models FAQ](./references/faq-models.md) | Model selection, auth profiles, failover, provider switching |
| [Testing](./references/testing.md) | Writing and running tests for OpenClaw agents |
| [Testing live](./references/testing-live.md) | Testing in production/live environments |

## Common first-run issues

**`openclaw doctor` is your first stop** for any issue:
```bash
openclaw doctor --non-interactive
openclaw status
openclaw logs --follow
```

**Install stuck?** → [First-run FAQ](./references/faq-first-run.md)

**Model auth failing?** → [Models FAQ](./references/faq-models.md)

**Channel not connecting?** → `openclaw channels status` + [channel troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)

## Testing

| Type | Tool |
|------|------|
| Unit/integration tests | `openclaw test` — see [Testing](./references/testing.md) |
| Live environment testing | [Testing live](./references/testing-live.md) |
| Channel diagnostics | `openclaw channels diagnose` |

## Debug checklist

1. `openclaw doctor --non-interactive` — catches 80% of common issues
2. `openclaw status` — gateway + agent health
3. `openclaw logs --follow` — real-time gateway logs
4. `openclaw gateway status` — is the gateway process running?
5. `openclaw config get` — verify active config matches expectations

## References

- `references/faq-first-run.md` — first-run and install issues
- `references/faq-models.md` — model selection, auth, failover
- `references/testing.md` — writing tests
- `references/testing-live.md` — live environment testing
