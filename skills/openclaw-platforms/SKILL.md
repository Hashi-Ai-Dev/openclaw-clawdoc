---
name: openclaw-platforms
description: "OpenClaw on different platforms and operating systems. Use when: running OpenClaw on Android, iOS, macOS, Windows, Linux, Raspberry Pi, Oracle Cloud, or DigitalOcean. Triggers on: \"android\", \"ios\", \"macos\", \"windows\", \"linux\", \"raspberry pi\", \"oracle\", \"digitalocean\", \"platform\", \"mac menu bar\", \"menu bar\", \"voice overlay\"."
---

# OpenClaw Platforms Reference

## Platform guides

| Platform | What it covers |
|----------|---------------|
| [Android](./references/android.md) | Android node app (companion device) |
| [iOS](./references/ios.md) | iOS app and node pairing |
| [macOS](./references/macos.md) | Menu bar app, voice overlay, canvas |
| [Windows](./references/windows.md) | Windows native + WSL2 |
| [Linux](./references/dev-setup.md) | Linux server, systemd, headless |
| [Raspberry Pi](./references/raspberry-pi.md) | Pi-specific setup |
| [Oracle Cloud](./references/oracle.md) | Oracle Cloud deployment |
| [DigitalOcean](./references/digitalocean.md) | DigitalOcean App Platform |

## Platform matrix

| Platform | Gateway host | Node capable | Native app |
|----------|-------------|--------------|------------|
| macOS | ✅ | ✅ | ✅ menu bar |
| Linux | ✅ | ❌ | ❌ |
| Windows (WSL2) | ✅ | ❌ | ❌ |
| Android | ❌ | ✅ | ✅ (companion) |
| iOS | ❌ | ✅ | planned |
| Raspberry Pi | ✅ | ✅ | ❌ |

## macOS menu bar

The macOS app runs as a menu bar agent. See:
- `references/macos.md` — macOS overview
- `references/mac/` — macOS-specific sub-pages (bundled-gateway, canvas, child-process, dev-setup, health, icon, logging, menu-bar, peekaboo, permissions, signing, skills, voice-overlay, voicewake, webchat, xpc)

## Linux server

Best for gateway hosting. Use systemd for daemon management:
```bash
systemctl --user enable openclaw
systemctl --user start openclaw
```

## References

- `references/android.md` — Android node app setup
- `references/ios.md` — iOS app and node pairing
- `references/macos.md` — macOS overview
- `references/mac/` — macOS-specific sub-pages
- `references/windows.md` — Windows + WSL2
- `references/dev-setup.md` — Linux server dev setup
- `references/raspberry-pi.md` — Pi-specific setup
- `references/oracle.md` — Oracle Cloud deployment
- `references/digitalocean.md` — DigitalOcean App Platform
