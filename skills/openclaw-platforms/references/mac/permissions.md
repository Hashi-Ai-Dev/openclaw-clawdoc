---
summary: "macOS permission persistence (TCC) and signing requirements"
read_when:
  - Debugging missing or stuck macOS permission prompts
  - Deciding whether to grant Accessibility to node or a CLI runtime
  - Packaging or signing the macOS app
  - Changing bundle IDs or app install paths
title: "macOS permissions"
---

macOS permission grants are fragile. TCC associates a permission grant
with the app's code signature, bundle identifier, and on-disk path. If
any of those change, macOS treats the app as new and may drop or hide
prompts.

## Requirements for stable permissions

For permissions to survive app updates and restarts:

1. **Stable bundle ID** — must not change between builds. Use
   `BUNDLE_ID=...` to set explicitly when packaging.
2. **Stable code signature** — ad-hoc signatures change every build;
   use a real Developer ID identity for releases. For dev, use a
   consistent ad-hoc identity (`-` is fine but stable across rebuilds).
3. **Stable install path** — don't move the .app between
   `/Applications` and `~/Applications`. Pick one.
4. **Same identity per build** — don't let codesign pick a different
   identity each time. Pin it in the build script.

The default debug bundle ID is `ai.openclaw.mac.debug`. For ad-hoc dev
builds, the signature identity is the developer's local key. Both are
recorded by macOS as the granting identity.

## Permission checklist

When adding a new feature that needs a TCC permission:

- [ ] Add the usage description to `Info.plist`
- [ ] Request the permission lazily (only when the feature is used)
- [ ] Handle the deny case gracefully (the app must work without it)
- [ ] Document the permission in the relevant ref doc

## Common permissions used

| Permission | Info.plist key | Used by |
|------------|----------------|---------|
| Notifications | `NSUserNotificationUsageDescription` | Channel message notifications |
| Microphone | `NSMicrophoneUsageDescription` | Voice wake, push-to-talk |
| Speech Recognition | `NSSpeechRecognitionUsageDescription` | Voice wake STT |
| Accessibility | (no Info.plist key — granted via Privacy pane) | Window focus, PeekabooBridge, paste |
| Screen Recording | (no Info.plist key — granted via Privacy pane) | Screen snapshot, screen record |
| Automation / AppleScript | (no Info.plist key — granted per-app) | `system.run` automation |
| Contacts | `NSContactsUsageDescription` | Contact picker for DM allowlist |
| Calendars | `NSCalendarsUsageDescription` | Calendar tool (if used) |

## Resetting permissions

To reset all TCC grants for the debug app:

```bash
tccutil reset All ai.openclaw.mac.debug
```

The next launch will prompt for each permission again. Use this when
debugging permission-state bugs.

## Granting Accessibility

1. Open System Settings → Privacy & Security → Accessibility.
2. Unlock with Touch ID / password.
3. Click + and select OpenClaw.app (or the .app under test).
4. Restart the app.

If the toggle is already on but the app reports no permission, the
signature has likely changed. Re-add the app or reset via `tccutil`.

## Granting Screen Recording

1. System Settings → Privacy & Security → Screen & System Audio Recording.
2. Add OpenClaw.app.
3. Restart the app.

Screen Recording is required for `screen.snapshot` and `screen.record`.
Without it, both tools return `permission_denied`.

## When the prompt doesn't appear

macOS hides TCC prompts when:

- The app is not running.
- The app launched but immediately exited.
- The signature changed since the last grant.
- The app was launched from a path that TCC doesn't trust (e.g. mounted
  DMG that wasn't ejected).

Fix:

```bash
# Move out of /Volumes
cp -R "/Volumes/OpenClaw/OpenClaw.app" /Applications/

# Reset TCC for the app
tccutil reset All ai.openclaw.mac.debug

# Re-launch
open /Applications/OpenClaw.app
```

## Accessibility for node, not just the app

If you want a CLI tool (not the app) to drive the UI, you have two
options:

1. **Use PeekabooBridge** — the app hosts the bridge; the CLI talks to
   it. Inherits the app's TCC permissions.
2. **Grant Accessibility to the CLI binary directly** — each CLI
   (e.g. `peekaboo`) needs its own grant. More fragile, harder to keep
   in sync.

The first option is preferred for stability.