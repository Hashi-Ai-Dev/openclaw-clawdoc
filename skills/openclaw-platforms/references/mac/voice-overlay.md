---
summary: "Voice overlay lifecycle when wake-word and push-to-talk overlap"
read_when:
  - Adjusting voice overlay behavior
title: "Voice overlay"
---

# Voice Overlay Lifecycle (macOS)

Audience: macOS app contributors. Goal: keep the voice overlay
predictable when wake-word and push-to-talk overlap.

## Current intent

- If the overlay is already visible from wake-word and the user
  presses the hotkey, the hotkey session _adopts_ the existing text
  instead of resetting it. The overlay stays up while the hotkey is
  held. When the user releases: send if there is trimmed text,
  otherwise dismiss.
- Wake-word alone still auto-sends on silence; push-to-talk sends
  immediately on release.

## States

```
[hidden] --wake word--> [listening]
[listening] --silence 1.5s--> [sending] --complete--> [hidden]
[listening] --push hotkey down--> [listening + holding]
[listening + holding] --hotkey release--> [sending] --complete--> [hidden]
[sending] --error--> [error] --dismiss--> [hidden]
[error] --retry--> [listening]
```

## Animations

- Show: 150 ms fade-in
- Dismiss: 200 ms fade-out (slower than show to feel "intentional")
- Send: subtle pulse on the send button (3 frames at 30 fps)
- Error: red shake (200 ms total)

Respect the `Reduce motion` accessibility preference — animations drop to
0 ms and the overlay appears/disappears instantly.

## Cancellation

- Esc while listening → dismiss without sending
- Esc while holding → release hotkey, dismiss
- Esc while sending → wait for the send to complete, then dismiss
- Wake word "stop" or "cancel" → same as Esc while listening

## Transcript handling

- The overlay holds the transcript as the user speaks.
- "Adopt" behavior (wake-word + hotkey overlap): keep the existing
  transcript; do not reset.
- Trimming: leading/trailing whitespace and recognized fillers
  ("um", "uh") are trimmed at send time, not at capture time.
- The agent sees the trimmed version; the user sees what they said.

## Push-to-talk voice selection

- The hotkey itself does NOT pick a model — it just toggles
  listening.
- The model is set in Settings → Voice → STT model.
- The TTS voice (for agent replies) is set in Settings → Voice →
  TTS voice.

## Failure modes

- **Mic permission revoked mid-session** — overlay shows error, dismisses
  after 3s. App shows the privacy pane prompt.
- **Speech recognition fails** — overlay shows "couldn't hear that"
  for 2s, returns to listening.
- **Send fails (gateway unreachable)** — overlay shows "retrying" for
  up to 30s; on permanent failure, the transcript is held in a
  pending-send buffer (visible in Settings → Voice → History).

## What this doc is NOT

- Not a guide for end users. See the macOS user guide for "how to use
  voice."
- Not a protocol spec. The voice pipeline is internal to the app.
- Not a tuning guide. Most parameters are exposed in
  Settings → Advanced → Voice internals; tune there, not by editing
  this doc.