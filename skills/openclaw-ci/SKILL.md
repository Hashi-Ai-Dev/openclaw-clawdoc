---
name: openclaw-ci
description: OpenClaw CI/CD integration. Use when setting up webhook automation, GitHub Actions integration, automated testing, CI pipelines, or continuous deployment for OpenClaw. Triggers on: "CI", "CD", "webhook", "GitHub Actions", "automation", "pipeline", "deploy", "CI/CD", "automation", "integration".
---

# OpenClaw CI/CD

## Webhook automation

OpenClaw can receive and process webhook events from external services (GitHub, GitLab, Bitbucket, custom).

```json
{
  "channels": {
    "discord": { "token": "BOT" }
  },
  "hooks": {
    "my-hook": {
      "trigger": "webhook",
      "url": "/webhook/github",
      "events": ["push", "pull_request"]
    }
  }
}
```

## GitHub Actions

Use the OpenClaw CLI in CI to run config validation, health checks, or deployment:

```yaml
- name: Validate OpenClaw config
  run: |
    openclaw config show | python3 -m json.tool > /dev/null && echo "valid"
```

## References

- `references/ci.md` — CI setup, webhook triggers, automation patterns