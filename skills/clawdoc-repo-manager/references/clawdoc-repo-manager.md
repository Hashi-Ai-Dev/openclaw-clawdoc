# Spine Repo Manager — Reference

Detailed procedures for GitHub repository maintenance.

## Stale Branch Cleanup (Detailed)

### Step 1: Identify Stale Branches

```bash
# Local branches inactive > 30 days
git for-each-ref --format='%(committerdate:relative) %(refname:short)' refs/heads/ \
  | awk '/months ago|years ago|[0-9]+ weeks ago/ {print $0}' | head -20

# Remote branches gone from default but still listed
git remote prune origin --dry-run
```

### Step 2: Confirm Before Deletion

```bash
# Check if branch is merged (safe to delete)
git branch -r --merged origin/main | grep <branch-name>

# Check if branch has unmerged commits
git log origin/<branch-name> ^origin/main --oneline
```

### Step 3: Deletion

```bash
# Local
git branch -D <stale-branch>

# Remote
git push origin --delete <stale-branch>
```

## Release Workflow

```bash
# 1. Update version in package.json/similar
# 2. Create changelog
git log --oneline main..HEAD > CHANGELOG.md

# 3. Tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z" <commit-sha>

# 4. Push with tags
git push origin main --tags

# 5. Create GitHub release
gh release create vX.Y.Z \
  --title "Release vX.Y.Z" \
  --notes "$(cat CHANGELOG.md)"
```

## Force-Push Decision Tree

```
Is it a protected branch (main/master/develop)?
  YES → STOP. Do not force-push. Use revert instead.
  NO  → Is it your feature branch with no collaborators?
    YES → Safe to force-push with --force-with-lease
    NO  → Coordinate with all branch collaborators first.
```

## CI/CD Integration

```bash
# Check if branch passes CI before merging
gh pr check-status --repo <owner>/<repo>

# Require status checks before merge
gh api repos/{owner}/{repo}/branches/main/protection/required_status_checks \
  -X PUT -f strict=true -f contexts[]=<check-name>
```
