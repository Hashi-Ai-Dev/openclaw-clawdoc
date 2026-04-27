---
name: openclaw-nodes
description: Pairing and using companion nodes (iOS, Android, macOS) with OpenClaw. Use when: pairing a phone or tablet as a node, using camera or canvas from an agent, VoiceWake, talk, audio input, location from a node, device notifications, screen sharing. Triggers on: "node", "pairing", "voicewake", "camera", "canvas", "audio", "talk", "location", "notifications", "screen", "android", "ios", "paired device".
---

# OpenClaw Nodes Reference

## What nodes do

A **node** is a companion device (iOS, Android, macOS) paired to your OpenClaw gateway. It exposes capabilities to agents:

| Capability | What it does |
|------------|-------------|
| `canvas.*` | Render and control a canvas |
| `camera.*` | Take photos, record video |
| `screen.*` | Screen recording, screenshots |
| `device.*` | Device info, permissions |
| `notifications.*` | Send/receive push notifications |
| `system.*` | System commands |
| `location.*` | GPS location |
| `talk.*` | VoiceWake — voice-activated agent |

## Pairing a node

```bash
# On the node: run the OpenClaw app and note the pairing code
# On the gateway machine:
openclaw devices list
openclaw devices approve <requestId>

# Or via CLI on the node host:
openclaw node run
```

## VoiceWake

VoiceWake lets a node wake OpenClaw with your voice without pressing anything. See:
- `references/talk.md` — VoiceWake setup and commands

## Node commands

```bash
openclaw nodes status
openclaw nodes describe --node <idOrName>
openclaw devices list
openclaw devices approve <requestId>
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Node won't pair | `openclaw doctor --non-interactive` + check firewall |
| VoiceWake not responding | Verify mic permissions on node device |
| Camera not working | Check camera permissions per platform |

## References

- `references/index.md` — nodes overview, pairing, protocol
- `references/voicewake.md` — VoiceWake setup and commands
- `references/audio.md` — audio input/output on nodes
- `references/talk.md` — talk commands
- `references/camera.md` — camera and video
- `references/media-understanding.md` — image/video understanding on nodes
