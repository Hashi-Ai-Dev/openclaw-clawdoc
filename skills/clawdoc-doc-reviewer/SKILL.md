---
name: clawdoc-doc-reviewer
description: Review all public-facing repo files for personal references before any commit/PR. Scan for personal names, Discord IDs, workspace paths, and private data. Trigger phrases: "doc reviewer", "review files", "check for leaks", "personal reference scan", "sanitize before commit"
---

# Spine Doc Reviewer

Sanitize files before commit to prevent personal data leakage into the public repository.

## Pre-Commit Scan

Before any `git add`, `git commit`, or opening a PR, run these scans:

### Required Scan Patterns

```bash
# Names and identifiers (case-insensitive grep)
grep -rni "Hashi\|Marcelo\|zeusxpr\|dejesus.danny12\|clawdoc@openclaw\|claw-doc\|clawdoc" --include="*.md" --include="*.json" --include="*.yml" --include="*.yaml" --include="*.txt" .

# Discord IDs
grep -rni "389060154273955840\|discord.*id\|user.*id.*[0-9]\{17,19\}" --include="*.md" --include="*.json" .

# Workspace and memory paths
grep -rni "\/home\/\|/data/workspace/\|~/\|/Users/\|MEMORY.md\|memory/.*\.md\|AGENTS.md\|SOUL.md\|USER.md\|TOOLS.md" --include="*.md" --include="*.json" .

# Private keys and tokens
grep -rni "ghp_\|gho_\|ghu_\|ghs_\|ghr_\|sk-\|OPENAI_API_KEY\|ANTHROPIC_API_KEY" --include="*.md" --include="*.json" --include="*.yml" .

# Email addresses
grep -rni "[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}" --include="*.md" --include="*.txt" .
```

### Workflow

1. **Before any `git add`** — run full scan on staged files
2. **After `git add`** — verify nothing leaked was staged
3. **Before PR** — scan the diff one final time

```bash
# Scan staged changes only (recommended)
git diff --staged | grep -iE "hashi|marcelo|zeusxpr|dejesus|389060154273955840|/home/|/data/workspace|MEMORY.md"

# Quick personal data sweep on all markdown
rg -i "hashi|marcelo|zeusxpr|389060154273955840" --type md
```

### Files to Always Exclude

Ensure these never enter the repo:

- `MEMORY.md`, `AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md` (workspace internals)
- `memory/` directory
- `.env`, `secrets.json`, `credentials.json`
- `node_modules/`
- Any file containing API keys or tokens

## Sanitization Rules

| Pattern | Replace With |
|---|---|
| `Hashi` | Remove or use `[Author]` |
| `Marcelo` | Remove or use `[Contributor]` |
| `zeusxpr` | Remove |
| `dejesus.danny12@gmail.com` | `[REDACTED]` |
| `389060154273955840` | Remove |
| `/data/workspace/` | Remove entirely |
| `~/` paths | Remove entirely |

## Reference

See `references/clawdoc-doc-reviewer.md` for full scan command reference, CI integration, and commit hooks setup.
