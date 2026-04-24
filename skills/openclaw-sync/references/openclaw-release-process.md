# OpenClaw Sync — Detailed Process Reference

## Version Detection

**Last synced version:** stored in `/data/workspace/clawdoc-live/.openclaw-version`

**Latest OpenClaw release:** fetch from GitHub API:
```bash
curl -s https://api.github.com/repos/openclaw/openclaw/releases/latest | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(d['tag_name'].lstrip('v'))"
```

**Local OpenClaw install** (fallback):
```bash
openclaw --version
```

## Doc Diff Strategy

Clone both versions and diff:
```bash
SYNCED=$(cat /data/workspace/clawdoc-live/.openclaw-version)
CURRENT="2026.4.22"

git clone --depth 1 --branch "v$SYNCED" https://github.com/openclaw/openclaw.git /tmp/oc-$SYNCED
git clone --depth 1 --branch "v$CURRENT" https://github.com/openclaw/openclaw.git /tmp/oc-$CURRENT

diff -rq /tmp/oc-$SYNCED/docs /tmp/oc-$CURRENT/docs | grep "differ"
```

## File → Skill Mapping

| OpenClaw doc path | ClawDoc skill | Reference dir |
|---|---|---|
| `docs/tools/*.md` | `openclaw-tools` | `skills/openclaw-tools/references/` |
| `docs/cli/*.md` | `openclaw-cli` | `skills/openclaw-cli/references/` |
| `docs/providers/*.md` | `openclaw-providers` | `skills/openclaw-providers/references/` |
| `docs/channels/*.md` | `openclaw-channels` | `skills/openclaw-channels/references/` |
| `docs/concepts/*.md` | `openclaw-concepts` | `skills/openclaw-concepts/references/` |
| `docs/automation/*.md` | `openclaw-tools` | `skills/openclaw-tools/references/automation/` |
| `docs/gateway/*.md` | `openclaw-config` | `skills/openclaw-config/references/` |
| `docs/plugins/*.md` | `openclaw-plugins` | `skills/openclaw-plugins/references/` |

## Known Update Patterns

These updates recur in almost every release — check them first:

### image-generation.md
- Default model (was `gpt-image-1`, now `gpt-image-2`)
- New resolution hints (2K, 4K)
- Provider capability table changes

### cron-jobs.md / cron.md
- `jobs-state.json` split from `jobs.json`
- Retry backoff changes
- Model-switch retry limits
- `NO_REPLY` suppression behavior

### moonshot.md
- Default model bump (k2.5 → k2.6)
- Cost estimates added/updated
- `thinking.keep=all` support on newer models

### providers/index.md + models.md
- New providers added
- New bundled variants

## Fetch Updated Doc from GitHub

```bash
# Template
curl -s "https://raw.githubusercontent.com/openclaw/openclaw/v{VERSION}/docs/{path}" \
  -o "/data/workspace/claw-doc/skills/{skill}/references/{file}"

# Example
curl -s "https://raw.githubusercontent.com/openclaw/openclaw/v2026.4.22/docs/tools/image-generation.md" \
  -o "/data/workspace/claw-doc/skills/openclaw-tools/references/image-generation.md"
```

## README Update Checklist

After syncing reference files:

- [ ] Version badge: `[![OpenClaw](https://img.shields.io/badge/OpenClaw-{VERSION}-blue?style=flat-square)]`
- [ ] Reference doc count: `find skills -name "*.md" | wc -l`
- [ ] Example files listed: confirm actual files match README tree
- [ ] Skills count (should be 11)

## Git Discipline

1. **Always** configure git identity before committing:
   ```bash
   git config user.name "ClawDoc Bot"
   git config user.email "clawdoc@openclaw.ai"
   ```

2. **Commit message format:**
   ```
   Sync OpenClaw {VERSION}

   - Updated {file1}, {file2}
   - Bumped version badge to {VERSION}
   - Ref count: {N} files

   Closes #sync-{VERSION}
   ```

3. **Tag format:** `v{MAJOR}.{MINOR}.{PATCH}` — semver bump from last tag

4. **Push both:** `git push origin {branch} && git push origin {tag}`

## Release Summary Template

```
## ClawDoc v{NEW_TAG} — OpenClaw {VERSION} Sync

**What changed in OpenClaw:**
- {list of significant new features/changes}

**What was updated in ClawDoc:**
- {list of files/skills updated}

**Release:** https://github.com/Hashi-Ai-Dev/openclaw-clawdoc/releases/tag/v{NEW_TAG}
**Compare:** https://github.com/Hashi-Ai-Dev/openclaw-clawdoc/compare/v{OLD_TAG}...v{NEW_TAG}
```

## Pre-Flight Checks

Before pushing:
- [ ] JSON config files are valid: `python3 -m json.tool file.json > /dev/null`
- [ ] No personal data or Hashi-specific content in updated files
- [ ] README counts match actual files
- [ ] `.openclaw-version` updated with new version number
- [ ] SKILL.md trigger conditions still accurate for any new/changed topics