# Spine Commit Sanitizer — Reference

Detailed procedures for author identity enforcement and history rewriting.

## git filter-repo (Recommended over filter-branch)

`git filter-branch` is legacy. Use `git filter-repo` for safer history rewriting.

```bash
# Install (one-time)
pip install git-filter-repo

# Rewrite author by name
git filter-repo --mailmap <(echo "ClawDoc <clawdoc@openclaw.ai> <Marcelo>") --force

# Rewrite author by email
git filter-repo --mailmap <(echo "ClawDoc <clawdoc@openclaw.ai> <dejesus.danny12@gmail.com>") --force
```

## Mailmap for Persistent Author Mapping

Create `.mailmap` in repo root:

```
# Correct author mapping
ClawDoc <clawdoc@openclaw.ai> <Marcelo>
ClawDoc <clawdoc@openclaw.ai> <marcelo>
ClawDoc <clawdoc@openclaw.ai> <dejesus.danny12@gmail.com>
ClawDoc <clawdoc@openclaw.ai> <zeusxpr>
```

Then rewrite:

```bash
git filter-repo --mailmap .mailmap --force
```

## Commit Template for Co-Authorship

Create `.github/COMMIT_TEMPLATE`:

```
<title>

<body>

Co-authored-by: ClawDoc <clawdoc@openclaw.ai>
```

Enable globally:

```bash
git config --global commit.template ~/.gitmessage
```

## Per-Repo Enforcement

Add to repo `.git/hooks/commit-msg`:

```bash
#!/usr/bin/env bash
AUTHOR=$(git log -1 --format="%an <%ae>")
ALLOWED="ClawDoc <clawdoc@openclaw.ai>"

if [ "$AUTHOR" != "$ALLOWED" ]; then
    echo "ERROR: Commit author must be: $ALLOWED"
    echo "Got: $AUTHOR"
    exit 1
fi
```

## Complete History Rewrite

```bash
# 1. Clone fresh (never rewrite history on existing clones)
git clone --mirror https://github.com/hashi-ai/clawdoc.git /tmp/clawdoc-mirror

# 2. Rewrite (using mailmap)
cd /tmp/clawdoc-mirror
git filter-repo --mailmap .mailmap --force

# 3. Verify
git log --format="%an <%ae>" | sort -u

# 4. Push (mirror)
git push --mirror https://github.com/hashi-ai/clawdoc.git
```

## Verify Co-Author in Existing Commits

```bash
# Find commits without co-author
git log --format="%H %an <%ae> %s" | \
  awk '!/\(.*\)<clawdoc@openclaw.ai>\)/ {print}'

# Add co-author to existing commits (interactive)
git rebase -i HEAD~N
# Change 'pick' to 'edit' for commits needing fixes
# Then:
git commit --amend --no-edit -m "$(git log -1 --format=%B)

Co-authored-by: ClawDoc <clawdoc@openclaw.ai>"
git rebase --continue
```
