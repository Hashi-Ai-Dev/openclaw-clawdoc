---
summary: "OpenClaw logging: rolling diagnostics file log + unified log privacy flags"
read_when:
  - Capturing macOS logs or investigating private data logging
  - Debugging voice wake/session lifecycle issues
title: "macOS logging"
---

# Logging (macOS)

## Rolling diagnostics file log (Debug pane)

OpenClaw routes macOS app logs through swift-log (unified logging by
default) and can write a local, rotating file log to disk when you need a
durable capture.

- Verbosity: **Debug pane → Logs → App logging → Verbosity**
- File location: `~/Library/Application Support/OpenClaw/logs/app.log`
- Rotation: 10 MB per file, 5 files retained (50 MB max)

The file log includes everything the unified log emits, plus app-private
fields the unified log redacts. Useful when you need to inspect a bug
that involves private data the OS would normally hide from log queries.

## Unified log privacy

OpenClaw marks every unified log entry with one of:

- `.public` — safe for sysdiagnose and shared bug reports
- `.private` — includes user content (message bodies, voice transcripts,
  session contents)
- `.private(maskOnDisk)` — like private, but masked if exported via
  sysdiagnose

Voice wake and message bodies are always `.private`. If you file a bug,
include only `.public` excerpts unless specifically asked.

## Capturing a sysdiagnose

```bash
sudo sysdiagnose -b ~/Desktop
```

OpenClaw contributes to the unified log slice. Filter for `ai.openclaw`
in Console.app to see only our entries.

## Tail the file log

```bash
tail -F ~/Library/Application\ Support/OpenClaw/logs/app.log
```

For real-time filtered output:

```bash
tail -F ~/Library/Application\ Support/OpenClaw/logs/app.log \
  | grep -E "voice.wake|session.lifecycle"
```

## Privacy flags in code

When adding new log entries:

```swift
// Public — safe to share
Logger.app.info("gateway connected")

// Private — never share without user consent
Logger.app.private("user said: \(transcript, privacy: .private)")

// Sensitive — mask on disk export
Logger.app.private("auth profile: \(profileId, privacy: .private(maskOnDisk))")
```

`Logger.app` is the shared logger. Category and subsystem are pre-set.

## What we never log

- Plaintext credentials (API keys, OAuth tokens)
- Voice wake raw audio (only transcript is logged, marked `.private`)
- Screen recording frames (only metadata is logged)

## If logs are missing

1. Check `~/Library/Application Support/OpenClaw/logs/` exists.
2. Open Debug pane → Logs → enable "Verbose app logging".
3. Restart the app to force a fresh log handle.
4. Check Console.app → System Reports → `ai.openclaw` for OS-level
   redactions (some entries are redacted by macOS regardless of our
   flag).