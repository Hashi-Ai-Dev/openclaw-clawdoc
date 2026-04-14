# Plugin Configuration

## plugins entries

Enable and configure individual plugins under `plugins.entries`:

```json
{
  "plugins": {
    "entries": {
      "plugin-id": {
        "enabled": true,
        "config": {
          // plugin-specific config
        }
      }
    }
  }
}
```

- `enabled: true` — plugin can load
- `config` — passed to the plugin at startup (schema defined in the plugin's `openclaw.plugin.json`)

## plugins allow

Explicit allowlist of plugin IDs that may load. If omitted, any discovered non-bundled plugin may auto-load.

```json
"plugins": {
  "allow": ["@openclaw/voice-call", "openclaw-honcho"]
}
```

Bundled plugins (`discord`, `minimax`, `browser`, `active-memory`, `brave`, `diffs`, `llm-task`, `lobster`, `memory-core`) are always allowed regardless of this list.

## plugins deny

Blocklist of plugin IDs — these will never load even if in `allow` or auto-discovered.

```json
"plugins": {
  "deny": ["some-bad-plugin"]
}
```

## plugin config validation

OpenClaw validates plugin config against each plugin's `openclaw.plugin.json` schema **before** loading the plugin code. Invalid config blocks the plugin and logs a validation error.

## Configuring a Plugin

General pattern:

```json
{
  "plugins": {
    "entries": {
      "PLUGIN_ID": {
        "enabled": true,
        "config": {
          // key: value pairs as defined by the plugin's manifest schema
        }
      }
    }
  }
}
```

### Examples

**Honcho (self-hosted):**
```json
{
  "plugins": {
    "slots": { "memory": "openclaw-honcho" },
    "entries": {
      "openclaw-honcho": {
        "enabled": true,
        "config": {
          "workspaceId": "my-workspace",
          "baseUrl": "http://127.0.0.1:8000"
        }
      }
    }
  }
}
```

**Voice Call (Twilio):**
```json
{
  "plugins": {
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": {
          "provider": "twilio",
          "accountSid": "AC...",
          "authToken": "secret"
        }
      }
    }
  }
}
```

## Inspecting Plugins

```bash
openclaw plugins list
openclaw plugins inspect <plugin-id>
```

## Restart Requirements

Plugin config changes generally require a gateway restart:
- `plugins.entries.*.enabled` changes → restart required
- Plugin `config` changes → restart required (unless the plugin supports hot-reload)

**Dynamic (no restart):**
- Adding/removing from `plugins.allow` or `plugins.deny`

## SecretRef in Plugin Config

Credentials in plugin config should use SecretRefs to avoid plaintext storage:

```json
{
  "plugins": {
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": {
          "authTokenRef": "secret:voice-call-auth"
        }
      }
    }
  }
}
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `plugin disabled (memory slot set to X)` | Another plugin already owns the memory slot | Set `plugins.slots.memory` to the desired plugin ID |
| `config validation failed for plugin X` | Config doesn't match plugin's manifest schema | Check the plugin's `openclaw.plugin.json` schema |
| `plugin not found: X` | Plugin ID not in `plugins.entries` or not auto-discovered | Add to `plugins.entries` or install the plugin |
| `plugin X is not allowed` | Plugin in `plugins.deny` or not in `plugins.allow` | Remove from deny or add to allow list |
