---
summary: "Voice wake and push-to-talk modes plus routing details in the mac app"
read_when:
  - Working on voice wake or PTT pathways
title: "Voice wake (macOS)"
---

# Voice Wake & Push-to-Talk

## Requirements

Voice Wake and push-to-talk require macOS 26 or newer. On older macOS
versions, the controls are hidden from the Voice settings page, which
shows the macOS 26 requirement.

## Voice wake

Wake word: "hey openclaw" (configurable in Settings → Voice).

When detected:

1. The wake word detector fires `triggerVoiceEars(ttl: nil)`.
2. Ears scale up to 1.9× with circular ear holes (visual feedback).
3. The overlay slides in to capture the utterance.
4. On silence (1.5s of no speech), the utterance is sent.
5. Ears drop back via `stopVoiceEars()` after 1s of post-send silence.

The wake word detector runs in-process (not via the Speech framework
alone — there's a low-latency custom detector on top). The custom
detector's model is bundled in the app.

## Push-to-talk (PTT)

Default hotkey: Right Option (configurable).

Behavior:

- Hotkey down → start listening
- Hotkey held → keep listening, show holding indicator
- Hotkey up → send immediately (no silence wait)

If voice wake fires while PTT is held, the wake-word is ignored (PTT
takes priority).

## What gets sent

The trimmed utterance (no fillers, no leading/trailing whitespace) is
sent as a regular user message to the active session. The agent has no
way to distinguish voice from typed input unless it inspects metadata.

## Overlap with text input

If the user is typing in the chat box when voice fires:

- The current text is preserved.
- The new voice message is sent as a separate message.
- The chat box focus is not stolen.

If the user starts typing mid-voice-utterance:

- The overlay stays up; the typed text goes into the chat box.
- Voice and typed text are sent separately on the next send trigger.

## Privacy

- Voice wake audio is processed in-process; nothing is sent to a cloud
  endpoint for wake-word detection.
- The utterance itself is sent to the agent like any other message —
  subject to the same privacy model.
- Wake word model and STT model are local; nothing leaves the device
  except the final transcript.

## Common issues

- **Wake word doesn't fire** — check the mic permission, the wake word
  model isn't corrupted (reinstall if needed), and the macOS Speech
  Recognition permission is granted.
- **High CPU when idle** — the wake word detector should idle near 0%.
  Check the audio buffer callback rate.
- **PTT double-sends** — likely a hotkey-up event firing twice. Check
  the event filter.
- **Overlay appears but no audio captured** — check the mic permission
  and verify the input device is the expected one in
  Settings → Voice → Input device.

## Settings exposed

- Wake word: on/off, word/phrase
- Wake sensitivity: low / medium / high (default medium)
- PTT hotkey: key combo
- STT model: bundled / cloud
- TTS voice: provider + voice name
- Overlay position: docked / floating / hidden

Changes apply immediately; no app restart needed.

## Example

```bash
# macOS / iOS / Android: launch + connect to a paired node
openclaw nodes status
openclaw nodes invoke camera_snap --facing front --quality 0.8
```
