---
summary: "macOS Skills settings UI and gateway-backed status"
read_when:
  - Updating the macOS Skills settings UI
  - Changing skills gating or install behavior
title: "Skills (macOS)"
---

The macOS app surfaces OpenClaw skills via the gateway; it does not parse
skills locally.

## Data source

- `skills.status` (gateway) returns all skills plus eligibility and
  missing requirements (including allowlist blocks for bundled skills).
- Requirements are derived from `metadata.openclaw.requires` in each
  `SKILL.md`.
- The app reads the bundled skills index from the gateway, not from
  its own bundle.

## What's shown

For each skill, the app shows:

- Skill name + description (first sentence of `description:`)
- Eligibility (✓ eligible, ⚠ missing requirements, ✗ blocked)
- Per-requirement line if any are missing (e.g. "needs `openclaw-prose`
  plugin")
- A toggle to enable/disable the skill for the current agent

## Gating

Some skills are gated by:

- **Plugin presence** — e.g. `openclaw-prose` requires the `open-prose`
  plugin.
- **Bundled-skill allowlist** — certain bundled skills require an
  explicit allowlist entry.
- **Tool permissions** — some skills need specific tools enabled.

If a requirement is missing, the toggle is disabled and the requirement
is shown. Clicking the requirement line opens the relevant setup page
(e.g. plugin install flow).

## Install from ClawHub

The Skills settings page has a "Browse ClawHub" button that opens
https://clawhub.ai in the user's default browser. Install from there;
the app refreshes `skills.status` on next gateway call.

## Local skill files

If the user has custom skills in `~/.openclaw/skills/` or in
`OPENCLAW_SKILLS_DIR`, they appear in the list with a "user" badge.
These are not editable from the app — use `clawhub publish` or edit the
files directly.

## What the app does NOT do

- Parse `SKILL.md` files locally (the gateway does this).
- Cache skill state across gateway restarts.
- Run skills — that's the gateway's job.

The app is a **view + toggle** for skill status reported by the
gateway.

## Common UX flows

### Enable a skill that's blocked

1. User sees "blocked: needs `openclaw-prose` plugin" next to a skill.
2. User clicks the requirement line.
3. App opens the plugin install page in the browser (or the plugin
   installer if one is bundled).
4. User installs the plugin and restarts the gateway.
5. App refreshes `skills.status` — skill is now eligible, toggle is
   enabled.

### Disable a skill for one agent

1. User opens the agent picker in the Skills settings.
2. App shows the per-agent skill state (read from `agents.<id>.skills`).
3. User toggles the skill off for that agent.
4. App calls `agents.update` to persist the change.
5. Next agent invocation for that agent omits the disabled skill.

### Bulk enable all eligible skills

1. User clicks "Enable all eligible" at the top of the Skills page.
2. App iterates `skills.status`, enables each eligible skill that isn't
   already enabled.
3. One confirmation prompt before bulk apply.
4. App calls `agents.update` with the merged skill list.