---
summary: "WeChat channel setup through the external openclaw-weixin plugin"
read_when:
  - You want to connect OpenClaw to WeChat or Weixin
  - You are installing or troubleshooting the openclaw-weixin channel plugin
  - You need to understand how external channel plugins run beside the Gateway
title: "WeChat"
---

OpenClaw connects to WeChat through Tencent's external `@tencent-weixin/openclaw-weixin` channel plugin.

Status: external plugin. Direct chats and media are supported. Group chats are not advertised by the current plugin capability metadata.

## Naming

- **WeChat** is the user-facing name in these docs.
- **Weixin** is the name used by Tencent's package and by the plugin id.
- `openclaw-weixin` is the OpenClaw channel id.
- `@tencent-weixin/openclaw-weixin` is the npm package.

Use `openclaw-weixin` in CLI commands and config paths.

## How it works

The WeChat code does not live in the OpenClaw core repo. OpenClaw provides the generic channel plugin contract, and the external plugin provides the WeChat-specific runtime:

1. `openclaw plugins install @tencent-weixin/openclaw-weixin` installs the plugin.
2. The Gateway discovers the plugin manifest and loads the plugin entrypoint.
3. The plugin registers channel id `openclaw-weixin`.
4. `openclaw channels login --channel openclaw-weixin` starts QR login.
5. The plugin stores account credentials under the OpenClaw state directory.
6. When the Gateway starts, the plugin starts its Weixin monitor for each configured account.
7. Inbound WeChat messages are normalized through the channel contract, routed to the selected OpenClaw agent, and sent back through the plugin outbound path.

That separation matters: OpenClaw core stays channel-agnostic; the WeChat-specific protocol lives in the external plugin.

## Install

```bash
openclaw plugins install @tencent-weixin/openclaw-weixin
openclaw gateway restart
```

Verify the install:

```bash
openclaw plugins list | grep weixin
# Expected: openclaw-weixin ... enabled
openclaw channels status | grep weixin
```

## QR login

The plugin uses WeChat QR-code authentication (Tencent iLink Bot):

```bash
openclaw channels login --channel openclaw-weixin
```

A QR code URL is printed to the terminal. Scan it with the WeChat mobile app within the timeout window (default 60 seconds). On success, the plugin stores the session token and you can restart the Gateway if needed.

To re-login (e.g., session expired):

```bash
openclaw channels logout --channel openclaw-weixin
openclaw channels login --channel openclaw-weixin
```

## Configuration

WeChat is configured under the `openclaw-weixin` channel id:

```json5
{
  channels: {
    "openclaw-weixin": {
      enabled: true,
      dmPolicy: "pairing",
      allowFrom: ["YOUR_WECHAT_USER_ID"],
      accounts: {
        default: {
          displayName: "OpenClaw Bot",
          media: { enabled: true, maxBytes: 10485760 }
        }
      }
    }
  }
}
```

## DM policies

| Policy | Behavior |
|--------|----------|
| `pairing` (default) | Code → owner approves via `openclaw pairing approve openclaw-weixin <code>` |
| `allowlist` | Only `allowFrom` list can DM the bot |
| `open` | Any WeChat user can DM |
| `disabled` | Ignore all inbound messages |

For private use, `pairing` is the default.

## Limitations

- **Direct chats only.** Group chat support is not in the current plugin's capability metadata; do not rely on it.
- **Media support** is direct chats only, with a default 10 MB cap (`media.maxBytes`).
- **Plugin external** — updates to the WeChat protocol come from Tencent via the npm package, not from the OpenClaw core repo. Check `openclaw plugins update @tencent-weixin/openclaw-weixin` periodically.

## Troubleshooting

- **QR code won't scan** — make sure the WeChat mobile app is logged in and on the same network as the Gateway. The QR code expires after 60s; re-run `openclaw channels login --channel openclaw-weixin`.
- **Plugin not loading** — `openclaw plugins list` should show `openclaw-weixin` as enabled. If it's listed but not enabled, run `openclaw plugins enable openclaw-weixin` and restart the Gateway.
- **Inbound messages not arriving** — check `openclaw channels status` and the Gateway logs for plugin errors. The plugin requires outbound HTTPS access to Tencent's iLink servers.

## See also

- [Channels index](/channels/channel-index)
- [Channel troubleshooting](/channels/troubleshooting)
- [Plugin manifest](/plugins/manifest)