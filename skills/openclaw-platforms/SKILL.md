---
name: openclaw-platforms
description: OpenClaw on different platforms and operating systems. Use when: running OpenClaw on Android, iOS, macOS, Windows, Linux, Raspberry Pi, Oracle Cloud, or DigitalOcean. Triggers on: "android", "ios", "macos", "windows", "linux", "raspberry pi", "oracle", "digitalocean", "platform", "mac menu bar", "menu bar", "voice overlay".
---

# OpenClaw Platforms Reference

## Platform guides

| Platform | What it covers |
|----------|---------------|
| [Android](./references/android.md) | Android node app (companion device) |
| [iOS](./references/index.md) | iOS app and node pairing |
| [macOS](./references/index.md) | Menu bar app, voice overlay, canvas |
| [Windows](./references/index.md) | Windows native + WSL2 |
| [Linux](./references/index.md) | Linux server, systemd, headless |
| [Raspberry Pi](./references/index.md) | Pi-specific setup |
| [Oracle Cloud](./references/index.md) | Oracle Cloud deployment |
| [DigitalOcean](./references/index.md) | DigitalOcean App Platform |

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
- `references/index.md` → macOS section
- Canvas, voice overlay, remote access all covered

## Linux server

Best for gateway hosting. Use systemd for daemon management:
```bash
systemctl --user enable openclaw
systemctl --user start openclaw
```

## References

- `references/index.md` — platform overview + macOS/Linux/Windows/Raspberry Pi/Oracle/DigitalOcean
- `references/android.md` — Android node app setup
- `references/mac/` — macOS-specific docs
