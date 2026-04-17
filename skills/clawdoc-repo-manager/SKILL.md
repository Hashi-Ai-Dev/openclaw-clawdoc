---
name: clawdoc-repo-manager
description: GitHub repository maintenance — branch hygiene, stale branch deletion, commit hygiene, force-push protocols, tag management. Trigger phrases: "repo manager", "clean branches", "delete stale branches", "maintain repo", "OSS maintainer"
---

# Spine Repo Manager

Manage the openclaw-clawdoc GitHub repository with discipline and hygiene.

## Workflow

### 1. Branch Hygiene

```bash
# List all branches sorted by last commit
git branch -v --sort=-committerdate

# Identify merged branches (no longer on remote)
git branch -r --merged main | grep -v 'main\|master\|develop'

# Delete merged local branches safely
git branch -d <branch-name>

# Force-delete unmerged branches (confirmation required)
git branch -D <branch-name>

# Delete remote branches
git push origin --delete <branch-name>
```

### 2. Stale Branch Detection

```bash
# Show branches inactive for >30 days (refs/heads/ only)
git for-each-ref --format='%(committerdate:relative)%(refname)' --sort=committerdate refs/heads/ | head -30

# Remote stale branches (requires GitHub CLI)
gh repo view $(git remote get-url origin | sed 's/.*github.com[/:]//' | sed 's/\.git$//') --json name,url
gh api repos/{owner}/{repo}/branches?protected=false --jq '.[].name'
```

### 3. Force-Push Protocol

> **⚠️ Never force-push to main or protected branches.**

```bash
# Always announce before force-push
git push --force-with-lease origin <branch>

# If remote has new commits you don't have, fetch first
git fetch origin
git push --force-with-lease origin <branch>
```

### 4. Tag Management

```bash
# List tags by date
git tag --sort=-creatordate

# Create annotated tag
git tag -a v<version> -m "Release v<version>: <summary>"

# Push tag to remote
git push origin v<version>

# Push all tags
git push origin --tags

# Delete local tag
git tag -d v<version>

# Delete remote tag
git push origin --delete tag v<version>
```

### 5. Commit Hygiene

```bash
# Amend last commit (before push)
git commit --amend --no-edit

# Interactive rebase for commit history cleanup (last N commits)
git rebase -i HEAD~N

# Squash commits during rebase: replace 'pick' with 'squash' or 's'
# Then fix the commit message

# Check for large files added accidentally
git ls-tree -r HEAD --name-only -s | sort -k1 -n -r | head -20
```

## Reference

See `references/clawdoc-repo-manager.md` for detailed procedures including CI/CD integration and release workflows.
