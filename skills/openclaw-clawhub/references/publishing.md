---
summary: "How ClawHub publishing works for skills, plugins, owners, scopes, releases, and review"
read_when:
  - Publishing a skill or plugin
  - Debugging owner or package scope errors
  - Adding publish UI, CLI, or backend behavior
title: "Publishing on ClawHub"
---

ClawHub publishing is owner-scoped: every publish targets a publisher, and
the server decides whether the signed-in user is allowed to publish there.

## Owners

An owner is a ClawHub publisher handle, such as `@alice` or `@openclaw`.
Personal owners are created for users. Org owners can have multiple members.

When you publish, you either use your personal owner or choose an org owner
where you have publisher access.

```bash
# See your owners
clawhub owners list

# Create a new personal owner (first-time setup)
clawhub owners create --name @your-handle
```

## Skills

Skills are published from a skill folder. The public page is:

```
https://clawhub.ai/<owner>/<slug>
```

Example:

```
https://clawhub.ai/@alice/calendar
```

A skill package needs:

- A `SKILL.md` with valid frontmatter (`name`, `description`)
- Any reference docs the skill needs
- A `clawhub.json` manifest (auto-generated on first publish)

```bash
cd my-skill/
clawhub publish
```

## Plugins

Plugins are published the same way but from a plugin folder with a
`plugin.json` manifest instead of `SKILL.md`.

```bash
cd my-plugin/
clawhub publish
```

## Versions and semver

ClawHub follows semver strictly:

- **Patch** (`0.0.x`) — bug fixes, no breaking changes
- **Minor** (`0.x.0`) — new features, backward-compatible
- **Major** (`x.0.0`) — breaking changes

You cannot re-publish the same version. To fix a publish, publish a new
patch version.

## Reviews

Every new owner and every new package goes through review:

- **Owner review** — verify the publisher's identity
- **Package review** — verify the package matches its declared capabilities,
  doesn't ship known malware patterns, and meets ClawHub's content
  guidelines

Reviews are run by ClawHub moderators. Standard review time is 24-48 hours.
Expedited review is available for verified org owners.

## Scopes

Packages have a **scope** that describes what they can do:

- `read-files` — package reads files in the workspace
- `write` — package writes files
- `exec` — package runs shell commands
- `network` — package makes outbound network calls
- `credentials` — package reads credentials/secrets
- `browser` — package controls a browser session
- `tools` — package adds new tools to the agent

The manifest's declared scopes are shown on the package page. Users install
at their own risk; high-impact scopes (exec, credentials, browser) display
a confirmation prompt.

## Transfer

Transfer ownership of a package to another owner:

```bash
clawhub transfer <slug> --to @new-owner
```

The current owner and the new owner must both approve. Transfers are
recorded in the package's audit log.

## Yanking

If you publish a version with a critical bug, you can yank it:

```bash
clawhub yank <slug> --version 1.2.0 --reason "critical security issue"
```

Yanked versions cannot be installed by new users. Existing installations
keep running until they update.

## See also

- `cli.md` — full CLI reference.
- `openclaw-tools/references/skill-workshop.md` — review proposals before
  publishing.
- `openclaw-plugins/references/plugin-inventory.md` — bundled plugins
  (separate from ClawHub-published plugins).