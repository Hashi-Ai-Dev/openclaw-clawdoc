---
summary: "Secrets management: SecretRef contract, runtime snapshot, and safe one-way scrubbing"
read_when:
  - Configuring SecretRefs for provider credentials and auth-profiles.json refs
  - Operating secrets reload, audit, configure, and apply safely in production
  - Understanding startup fail-fast, inactive-surface filtering, and last-known-good behavior
title: "Secrets management"
---

OpenClaw supports additive SecretRefs so supported credentials do not need to
be stored as plaintext in configuration.

> **Note:** Plaintext still works. SecretRefs are opt-in per credential.

> **Warning:** Plaintext credentials remain agent-readable if they are stored
> in files the agent can inspect, including `openclaw.json`,
> `auth-profiles.json`, `.env`, or generated `agents/*/agent/models.json`
> files. SecretRefs reduce that local blast radius only after every supported
> credential has been migrated and `openclaw secrets audit --check` reports
> no plaintext secret residue.

## Goals and runtime model

Secrets are resolved into an in-memory runtime snapshot.

- **Resolution is eager during activation**, not lazy on request paths.
- **Startup fails fast** when an effectively active SecretRef cannot be
  resolved.
- **Inactive-surface filtering** keeps unused credentials out of the snapshot.
- **Last-known-good behavior** keeps the previous snapshot when reload fails,
  so a single bad secret does not disable the gateway.

## SecretRef providers

Three providers are supported:

| Provider | Source | Example |
|----------|--------|---------|
| `env`    | Environment variable | `env://OPENAI_API_KEY` |
| `file`   | Path to a file (read once) | `file:///run/secrets/openai.key` |
| `exec`   | Run a command, capture stdout | `exec://vault read -field=key openai/api` |

Each credential field accepts an object form for SecretRefs:

```json5
{
  providers: {
    openai: {
      apiKey: { ref: { provider: "env", name: "OPENAI_API_KEY" } },
    },
  },
}
```

## Common commands

```bash
# Audit current config for plaintext credentials
openclaw secrets audit
openclaw secrets audit --check    # strict: exit non-zero if plaintext found

# Show the resolved runtime snapshot (one-way scrubbed)
openclaw secrets show

# Reload the snapshot after rotating credentials
openclaw secrets reload

# Configure a new SecretRef for an existing credential
openclaw secrets configure --provider openai --field apiKey

# Apply pending SecretRef changes (one-shot)
openclaw secrets apply
```

## Scrubbing

`openclaw secrets show` is a **one-way scrubbed** view. The following fields
are replaced with `***`:

- `apiKey`, `token`, `password`, `secret`, `key` (case-insensitive substring
  match)
- Any field whose name contains `credential`

The scrubber preserves the shape of the snapshot (so you can verify the
structure loaded correctly) without exposing the values.

## Production operating notes

- **Always run `openclaw secrets audit --check` in CI** before merging
  config changes. A non-zero exit means plaintext credentials are present
  and should be migrated.
- **Reload is non-destructive** — a failed reload keeps the previous
  snapshot and emits a clear log line. Don't panic on a partial failure.
- **`apply` is destructive** — it commits pending SecretRef changes. There
  is no automatic rollback on `apply` failure; use `secrets show` to verify
  the new snapshot loaded before relying on it.
- **`auth-profiles.json` can also hold SecretRefs.** Use the same
  `secrets audit` flow for those files.

## Migration path

For each plaintext credential in your config:

1. Move the value to your secret backend (env var, file, exec).
2. Update the config to use `{ ref: { provider, name } }`.
3. Run `openclaw secrets reload`.
4. Verify with `openclaw secrets show`.
5. Repeat `openclaw secrets audit --check` until it exits zero.