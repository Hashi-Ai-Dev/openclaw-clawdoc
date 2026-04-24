---
name: openclaw-sync
description: Complete OpenClaw release sync pipeline. Use when Hashi says a new OpenClaw version dropped, or when checking for OpenClaw updates to sync into ClawDoc. This skill handles the entire end-to-end pipeline: detect version, diff docs, update local skills, sync clawdoc-live, bump version, commit with git discipline, tag, push, and report. Triggers on: "new openclaw version", "sync openclaw", "sync clawdoc", "update clawdoc", "review OpenClaw release", "OpenClaw version dropped".
---

# OpenClaw Sync Pipeline

Handles the complete sync of a new OpenClaw release into ClawDoc — end to end, fully autonomous.

## Pipeline Overview

```
1. Detect     → current synced version vs latest OpenClaw release
2. Compare    → diff docs/changelogs, identify what changed
3. Plan       → map changed areas → which skills/docs need updating
4. Update     → sync updated reference files into local skills
5. Sync       → push updates to clawdoc-live repo
6. Release    → bump version, commit, tag, GitHub release
7. Report     → give Hashi a summary with release link
```

## Step-by-Step

### 1. Detect Version

```bash
# Get latest OpenClaw release version
curl -s https://api.github.com/repos/openclaw/openclaw/releases/latest | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['tag_name'].lstrip('v'))"

# Read last synced version from clawdoc-live
cat /data/workspace/clawdoc-live/.openclaw-version
```

If same → report "already current" and stop.
If newer → proceed.

### 2. Compare Docs

```bash
# Clone OpenClaw at both versions
SYNCED=$(cat /data/workspace/clawdoc-live/.openclaw-version)
CURRENT="<new version>"

git clone --depth 1 --branch "v$SYNCED" https://github.com/openclaw/openclaw.git /tmp/oc-prev
git clone --depth 1 --branch "v$CURRENT" https://github.com/openclaw/openclaw.git /tmp/oc-new

# Diff the docs/
diff -rq /tmp/oc-prev/docs /tmp/oc-new/docs | grep "differ" | awk '{print $2}' | sed 's|/tmp/oc-prev/docs/||'
```

Key areas to check (in priority order):
- `docs/tools/` → `skills/openclaw-tools/references/`
- `docs/cli/` → `skills/openclaw-cli/references/`
- `docs/providers/` → `skills/openclaw-providers/references/`
- `docs/channels/` → `skills/openclaw-channels/references/`
- `docs/concepts/` → `skills/openclaw-concepts/references/`
- `docs/automation/` → relevant references
- `docs/gateway/` → `skills/openclaw-config/references/`
- `docs/plugins/` → `skills/openclaw-plugins/references/`

### 3. Update Local Reference Files

For each changed doc:
1. Fetch the new version from GitHub:
   ```bash
   curl -s "https://raw.githubusercontent.com/openclaw/openclaw/v{VERSION}/docs/{path}" \
     -o "/data/workspace/claw-doc/skills/{skill}/references/{file}"
   ```
2. Apply any edits needed (e.g., `gpt-image-2` default, `k2.6` default, etc.)
3. Report what was updated

**High-priority updates to always check:**
- `docs/tools/image-generation.md` → default model, 2K/4K hints
- `docs/cli/cron.md` or `docs/automation/cron-jobs.md` → jobs-state split, retry logic
- `docs/providers/moonshot.md` → default model bump (k2.6 was k2.5)

### 4. Update README

After updating reference files, update clawdoc-live/README.md:
- Version badge: `https://img.shields.io/badge/OpenClaw-{VERSION}-blue?style=flat-square`
- Reference doc count: `find skills -name "*.md" | wc -l`
- Example count if examples changed

### 5. Sync to clawdoc-live

```bash
cd /data/workspace/clawdoc-live

# Stage updated files
git add skills/ README.md

# Commit
git commit -m "Sync OpenClaw {VERSION}

- Updated {list of changed files}
- Bumped version badge to {VERSION}
- Updated ref count to {N}"

# Push
git push origin master
```

### 6. Release (Git Discipline)

```bash
cd /data/workspace/clawdoc-live

# Update version tracking
echo "{VERSION}" > .openclaw-version
git add .openclaw-version
git commit -m "Track OpenClaw {VERSION}"

# Tag (semver bump from last tag)
LAST_TAG=$(git describe --tags --abbrev=0)
# bump patch: v1.2.0 → v1.2.1
NEW_TAG="v1.x.x"  # determine from current version

git tag -a v{NEW} -m "OpenClaw {VERSION} synced"
git push origin v{NEW}
git push origin master
```

### 7. Report

Give Hashi:
- What changed (summary of updated files)
- Release link: `https://github.com/Hashi-Ai-Dev/openclaw-clawdoc/releases/tag/v{NEW}`
- Compare link: `https://github.com/Hashi-Ai-Dev/openclaw-clawdoc/compare/v{OLD}...v{NEW}`

## Key Paths

| Item | Path |
|------|------|
| ClawDoc local skills | `/data/workspace/claw-doc/skills/` |
| ClawDoc live repo | `/data/workspace/clawdoc-live/` |
| Version tracking | `/data/workspace/clawdoc-live/.openclaw-version` |
| Skills index | `/data/workspace/clawdoc-live/skills/` |
| Examples | `/data/workspace/clawdoc-live/examples/` |

## Reference

See `references/openclaw-release-process.md` for detailed version-comparison logic and file-mapping rules.