---
name: openclaw-logging
description: OpenClaw logging configuration. Use when configuring log levels, log rotation, log destinations, log format, or debugging OpenClaw log output. Triggers on: "logging", "log level", "log rotation", "log format", "logs", "debug", "output", "logger", "syslog", "file logging".
---

# OpenClaw Logging

## Log location

```
/tmp/openclaw/openclaw-YYYY-MM-DD.log
```

## Log levels

Set via `logging.level` in config:

```json
{ "logging": { "level": "info" } }
```

Levels: `debug`, `info`, `warn`, `error`, `fatal`

## Log rotation

Logs rotate daily. Use `openclaw logs` to tail:

```bash
openclaw logs --follow
openclaw logs --lines 100
```

## Debug mode

Enable verbose logging:

```json
{ "logging": { "level": "debug" } }
```

## References

- `references/logging.md` — full logging configuration, log management commands