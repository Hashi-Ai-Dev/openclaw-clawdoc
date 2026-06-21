---
summary: "Setup guide for developers working on the OpenClaw macOS app"
read_when:
  - Setting up the macOS development environment
title: "macOS dev setup"
---

# macOS developer setup

Build and run the OpenClaw macOS application from source.

## Prerequisites

Before building the app, ensure you have the following installed:

- **Xcode 15 or newer** with macOS 14+ SDK
- **Node.js 20 or newer** — for the local Gateway
- **Swift 5.9+** (ships with Xcode)
- **`openclaw` CLI** — for end-to-end testing against a running Gateway
- **Tailscale** (optional) — for testing tailnet features

Clone the repo:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw/apps/macos
```

## Build

```bash
./scripts/package-mac-app.sh
```

This:

1. Builds the app target (`OpenClaw.app`)
2. Sets the debug bundle ID `ai.openclaw.mac.debug`
3. Signs the binary with your local signing identity (or ad-hoc if none)
4. Writes the .app to `dist/`

## Run from Xcode

Open `apps/macos/OpenClaw.xcodeproj`. The default scheme builds and runs
the app. Set `OPENCLAW_GATEWAY_URL` in the scheme to point at a local
Gateway (default `ws://127.0.0.1:18789`).

## Run a local Gateway

In another terminal:

```bash
cd openclaw
pnpm install
pnpm gateway:dev
```

Verify:

```bash
openclaw status --json | jq .gateway.uptime
```

## Connect the app to your dev Gateway

By default the app looks for a Gateway on `127.0.0.1:18789`. To use a
different port:

1. Edit `~/.openclaw/openclaw.json` and set `gateway.bind` to your port.
2. Restart the dev Gateway.
3. In the app, open Settings → Gateway and update the URL.

For HTTPS Gateway (with self-signed cert):

1. Set `gateway.tls.enabled: true` and `gateway.tls.cert` / `.key` paths
   in your config.
2. Add the cert to macOS Keychain (otherwise the app refuses it).

## Debugging

- View app logs: Console.app → search for `ai.openclaw`
- View Gateway logs: `~/.openclaw/logs/gateway.log`
- Set `OPENCLAW_DEBUG=1` in the app's environment to enable verbose
  logging
- Use the macOS Activity Monitor to inspect CPU/memory for both the app
  and the dev Gateway

## Permissions during dev

macOS TCC prompts the first time the app tries to use:

- **Notifications** — needed for notification delivery
- **Accessibility** — needed for window focus / paste simulation
- **Screen Recording** — needed for canvas snapshot, screen recording
- **Microphone** — needed for voice wake, push-to-talk
- **Speech Recognition** — needed for STT
- **Automation / AppleScript** — needed for `system.run` automation

If a permission prompt doesn't appear, check
`System Settings → Privacy & Security`. Reset the app's permissions with:

```bash
tccutil reset All ai.openclaw.mac.debug
```

## Common issues

- **"App is damaged"** — the ad-hoc signature is rejected. Run
  `xattr -dr com.apple.quarantine /path/to/OpenClaw.app` after first
  launch.
- **WebSocket connect fails** — check the Gateway is bound to the URL the
  app is using.
- **A2UI panel blank** — verify the Gateway serves
  `/__openclaw__/a2ui/` (open it in a browser first).
- **Voice wake unresponsive** — confirm the Microphone and Speech
  Recognition permissions are granted.