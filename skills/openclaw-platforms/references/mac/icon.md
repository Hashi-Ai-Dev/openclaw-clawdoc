---
summary: "Menu bar icon states and animations for OpenClaw on macOS"
read_when:
  - Changing menu bar icon behavior
title: "Menu bar icon"
---

# Menu Bar Icon States

- **Idle:** Normal icon animation (blink, occasional wiggle).
- **Paused:** Status item uses `appearsDisabled`; no motion.
- **Voice trigger (big ears):** Voice wake detector calls
  `AppState.triggerVoiceEars(ttl: nil)` when the wake word is heard,
  keeping `earBoostActive=true` while the utterance is captured. Ears
  scale up (1.9x), get circular ear holes for readability, then drop via
  `stopVoiceEars()` after 1s of silence. Only fired from the in-app voice
  pipeline.
- **Working (agent running):** `AppState.isWorking=true` drives a
  "tail/leg scurry" micro-motion: faster leg wiggle and slight offset
  while work is in-flight. Currently toggled around WebChat agent runs;
  add the same toggle around other long tasks when you wire them.

## Color states

The icon's accent color reflects channel health (see `health.md`):

- Green dot — channel healthy
- Yellow dot — channel stale
- Red dot — channel error
- Gray dot — health unknown

## Animation budget

Menu bar animations are CPU-visible. Keep them subtle:

- Idle blink: max 1 frame per 4s
- Working scurry: max 30 fps
- Voice ears: max 60 fps during utterance, drop immediately after

Disable animations entirely in System Settings → Accessibility → Display
→ Reduce motion. The app respects this preference.

## Click behavior

- **Left click** — open the menu (status + actions)
- **Right click** — same menu, plus "Quit OpenClaw"
- **Cmd + click** — open the Control UI in a browser

## Customization

The icon does not currently support per-user themes. If you want to skin
it, fork the app and replace `Assets.xcassets/MenuBarIcon.imageset/`.

## Performance notes

The icon redraws are coalesced by AppKit. If you observe high CPU usage
in Activity Monitor, check:

- The blink timer isn't being recreated on every state change
- The animation timer isn't running when the menu is closed
- Voice ear animations drop to 0 fps when the menu is hidden

Common bug: forgetting to invalidate the timer when leaving the "working"
state. Symptoms: 5-10% CPU when idle.