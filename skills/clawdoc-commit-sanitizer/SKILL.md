---
name: clawdoc-commit-sanitizer
description: Ensure all commits use the correct author identity (ClawDoc <clawdoc@openclaw.ai>), scan messages for personal info, enforce co-authorship, rewrite history when needed. Trigger phrases: "commit sanitizer", "author identity", "rewrite git history", "co-authored-by", "fix commit author"
---

# Spine Commit Sanitizer

Enforce correct commit authorship and prevent personal data in commit messages.

## Author Identity

### Set Commit Author (per-repo)

```bash
git config user.name "ClawDoc"
git config user.email "clawdoc@openclaw.ai"
```

### Verify Author

```bash
git log --format="%an <%ae>" | sort -u
# Should only show: ClawDoc <clawdoc@openclaw.ai>
```

### Amend Existing Commits

```bash
# Fix last commit's author
git commit --amend --author="ClawDoc <clawdoc@openclaw.ai>" --no-edit

# Re-base and fix all commits on a branch
git rebase -i HEAD~N --exec 'git commit --amend --author="ClawDoc <clawdoc@openclaw.ai>" --no-edit'
```

## Co-Authorship

```bash
# Add co-author to a commit
git commit -m "Fix something

Co-authored-by: Name <email@example.com>"
```

For all commits to include co-authorship with the owner:

```bash
git config commit.template .github/COMMIT_TEMPLATE
```

## Rewrite History (git filter-branch)

> **⚠️ Never rewrite history on main or protected branches.**

### Rewrite All Commits to New Author

```bash
git filter-branch --env-filter '
OLD_NAME="Marcelo"
NEW_NAME="ClawDoc"
NEW_EMAIL="clawdoc@openclaw.ai"

if [ "$GIT_COMMITTER_NAME" = "$OLD_NAME" ]; then
    export GIT_COMMITTER_NAME="$NEW_NAME"
    export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
fi
if [ "$GIT_AUTHOR_NAME" = "$OLD_NAME" ]; then
    export GIT_AUTHOR_NAME="$NEW_NAME"
    export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```

### Rewrite by Email

```bash
git filter-branch --env-filter '
if [ "$GIT_AUTHOR_EMAIL" = "dejesus.danny12@gmail.com" ]; then
    export GIT_AUTHOR_NAME="ClawDoc"
    export GIT_AUTHOR_EMAIL="clawdoc@openclaw.ai"
fi
if [ "$GIT_COMMITTER_EMAIL" = "dejesus.danny12@gmail.com" ]; then
    export GIT_COMMITTER_NAME="ClawDoc"
    export GIT_COMMITTER_EMAIL="clawdoc@openclaw.ai"
fi
' -- --all
```

### Remove Personal Data from History

```bash
git filter-branch --index-filter '
git rm --cached --ignore-unmatch filename-with-secrets
git rm --cached --ignore-unmatch .env
' --tag-name-filter cat -- --all
```

### After filter-branch

```bash
# Verify changes
git log --format="%an <%ae>" | sort -u

# Push rewritten history (force)
git push origin --force --all
git push origin --force --tags
```

## Commit Message Scan

Before any commit, scan for personal info:

```bash
# Scan staged diff for personal data
git diff --staged | grep -iE "hashi|marcelo|zeusxpr|dejesus|389060154273955840|/home/|/data/workspace|MEMORY"

# If found, amend and clean
git commit --amend --no-edit
```

## Reference

See `references/clawdoc-commit-sanitizer.md` for git filter-repo alternatives, GitHub CoPilot setup, and identity enforcement via commit template.
