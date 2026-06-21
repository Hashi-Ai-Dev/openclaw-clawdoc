---
summary: "Twilio SMS channel setup, access controls, and webhook configuration"
read_when:
  - You want to connect OpenClaw to SMS through Twilio
  - You need SMS webhook or allowlist setup
title: "SMS"
---

OpenClaw can receive and send SMS through a Twilio phone number or Messaging Service. The Gateway registers an inbound webhook route, validates Twilio request signatures by default, and sends replies back through Twilio's Messages API.

## Before you begin

You need:
- A Twilio account with an SMS-capable phone number, or a Twilio Messaging Service.
- The Twilio Account SID and Auth Token.
- A public HTTPS URL that reaches your OpenClaw Gateway.
- A sender policy choice: `pairing` for private use, `allowlist` for preapproved phone numbers, or `open` only for intentionally public SMS access.

Use one Twilio number for both SMS and Voice Call if the number has both capabilities. Configure the SMS webhook and Voice webhook separately in Twilio; this page only covers the SMS webhook.

## Quick setup

1. In Twilio, open **Phone Numbers > Manage > Active numbers** and choose an SMS-capable number. Save:
   - Account SID (e.g., `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
   - Auth Token
   - Sender phone number (e.g., `+15551234567`)

   If you use a Messaging Service instead of a fixed sender number, save the Messaging Service SID (e.g., `MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`).

2. Configure the SMS channel in `~/.openclaw/openclaw.json`:
   ```json5
   {
     channels: {
       sms: {
         enabled: true,
         accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
         authToken: "twilio-auth-token",
         fromNumber: "+15551234567",
         publicWebhookUrl: "https://your-gateway.example.com/webhooks/sms",
         dmPolicy: "pairing",
         allowFrom: ["+15555550100"]
       }
     }
   }
   ```

3. In the Twilio console, set the **A message comes in** webhook for your number to:
   `POST https://your-gateway.example.com/webhooks/sms`
   Twilio will sign each request; the Gateway validates the signature by default.

4. Restart the Gateway (`openclaw gateway restart`) and verify with `openclaw channels status | grep sms`.

## DM policies

| Policy | Behavior |
|--------|----------|
| `pairing` (default) | Code → owner approves via `openclaw pairing approve sms <code>` |
| `allowlist` | Only `allowFrom` list can DM the bot |
| `open` | Any phone number can DM (`allowFrom: ["*"]`) — only for intentionally public SMS |
| `disabled` | Ignore all inbound SMS |

For private/personal use, `pairing` is the safest default.

## Messaging Service setup

If you have a Twilio Messaging Service (multi-number, sending pools):

```json5
{
  channels: {
    sms: {
      enabled: true,
      accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      authToken: "twilio-auth-token",
      messagingServiceSid: "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      dmPolicy: "allowlist",
      allowFrom: ["+15555550100", "+15555550101"]
    }
  }
}
```

When `messagingServiceSid` is set, `fromNumber` is optional — Twilio picks a sender from the pool.

## Webhook signature verification

The Gateway validates Twilio request signatures (`X-Twilio-Signature`) by default. If your webhook URL changes (e.g., behind a proxy), make sure Twilio's outbound POST matches the configured `publicWebhookUrl`. Mismatched URLs cause signature failures and inbound SMS will be rejected.

For local development, use a tunneling service (ngrok, Cloudflare Tunnel) and update `publicWebhookUrl` accordingly.

## Troubleshooting

- **No inbound events** — verify the Twilio webhook URL matches `publicWebhookUrl`; check `openclaw doctor` for signature failures.
- **Sender blocked** — `openclaw pairing list sms` shows pending pairing codes; approve or update `allowFrom`.
- **"Twilio 401 Unauthorized" in logs** — `accountSid` or `authToken` is wrong. Re-issue the auth token from the Twilio console.
- **SMS sent but no delivery confirmation** — Twilio status callbacks are sent to the same webhook route; check `openclaw channels status` for delivery state.

## See also

- [Pairing](/channels/pairing)
- [Channel troubleshooting](/channels/troubleshooting)
- [Voice Call](/plugins/voice-call) — Twilio voice via the same number