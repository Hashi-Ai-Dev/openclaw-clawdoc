# Spine Doc Reviewer — Reference

Full scan commands and CI integration for personal data sanitization.

## Comprehensive Scan Commands

```bash
#!/usr/bin/env bash
# pre-commit-sanitize.sh — run before any git commit

echo "=== Personal Reference Scan ==="

# Names
echo "--- Names ---"
rg -i "hashi|marcelo|zeusxpr|dejesus" --type md --type json --type yaml | grep -v "node_modules" || true

# Discord IDs
echo "--- Discord IDs ---"
rg "\d{17,20}" --type md --type json | rg "389060154273955840|discord|user.*id" || true

# Paths
echo "--- Private Paths ---"
rg "/home/|/data/workspace/|MEMORY\.md|AGENTS\.md|SOUL\.md|USER\.md|TOOLS\.md" --type md --type json --type yaml | grep -v "node_modules" || true

# API Keys
echo "--- Secrets ---"
rg "ghp_|gho_|ghu_|ghs_|sk-|OPENAI_API_KEY|ANTHROPIC_API_KEY" --type md --type json --type yaml --type env | grep -v "node_modules" || true

# Emails
echo "--- Emails ---"
rg "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" --type md | rg -v "@openclaw.ai" || true

echo "=== Scan Complete ==="
```

## Pre-Commit Hook Setup

```bash
# Create .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash
set -e

echo "Running personal data scan..."

SCAN_RESULT=$(git diff --staged --name-only | xargs grep -iE "hashi|marcelo|zeusxpr|dejesus|389060154273955840" 2>/dev/null || true)

if [ -n "$SCAN_RESULT" ]; then
    echo "ERROR: Personal data detected in staged files:"
    echo "$SCAN_RESULT"
    echo "Remove personal references before committing."
    exit 1
fi

echo "Scan passed. Proceeding with commit."
EOF

chmod +x .git/hooks/pre-commit
```

## GitHub Actions CI Check

```yaml
# .github/workflows/sanitize-check.yml
name: Sanitize Check
on: [push, pull_request]

jobs:
  sanitize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run sanitize scan
        run: |
          echo "Checking for personal data..."
          FOUND=$(grep -rni "hashi|marcelo|zeusxpr|dejesus" . --include="*.md" --include="*.json" | grep -v node_modules || true)
          if [ -n "$FOUND" ]; then
            echo "ERROR: Personal references found:"
            echo "$FOUND"
            exit 1
          fi
          echo "No personal data found."
```

## Redaction Guide

| Type | Example | Replacement |
|---|---|---|
| Name: Marcelo | `Thank you Marcelo!` | `Thank you!` or `Thank you @contributor` |
| Email | `dejesus.danny12@gmail.com` | `[EMAIL REDACTED]` |
| Discord ID | `389060154273955840` | Remove entirely |
| Workspace path | `/data/workspace/skills/` | Remove entirely |
| GitHub handle | `zeusxpr` | `openclaw` or org name |
