---
name: clawdoc-org-manager
description: Manage the Hashi.Ai GitHub organization — org settings, team access, funding links, repo visibility, community files. Trigger phrases: "org manager", "GitHub org", "Hashi.Ai org", "team access", "org settings"
---

# Spine Org Manager

Manage the Hashi.Ai GitHub organization settings and repository visibility.

## Org Management (GitHub CLI)

```bash
# View org details
gh org view hashi-ai

# List all repos in org
gh repo list hashi-ai --limit 100

# List org members
gh api orgs/hashi-ai/members --jq '.[].login'

# List teams
gh api orgs/hashi-ai/teams --jq '.[].name'
```

## Team Access Management

```bash
# Add member to team
gh api --method PUT -H "Accept: application/vnd.github.v3+json" \
  /orgs/hashi-ai/teams/<team-slug>/memberships/<username> \
  -f role=member

# List team members
gh api /orgs/hashi-ai/teams/<team-slug>/members --jq '.[].login'

# Add repo to team
gh api --method PUT -H "Accept: application/vnd.github.v3+json" \
  /orgs/hashi-ai/teams/<team-slug>/repos/<owner>/<repo> \
  -f permission=push
```

## Repo Visibility & Settings

```bash
# Transfer repo to org
gh repo transfer <repo-name> hashi-ai

# Set repo visibility
gh repo edit <repo> --visibility public|private|internal

# Enable/disable issues, wiki, projects
gh repo edit <repo> --enable-issues --disable-wiki

# Manage branch protection
gh api repos/{owner}/{repo}/branches/main/protection -X PUT \
  -f required_status_checks=null \
  -f enforce_admins=true \
  -f required_pull_request_reviews=null \
  -f allow_force_pushes=false \
  -f allow_deletions=false
```

## Funding & Community Files

```bash
# Edit FUNDING.yml (create if not exists)
cat > .github/FUNDING.yml << 'EOF'
github: []
patreon: []
open_collective: []
ko_fi: []
tidelift: "npm/package-name"
community_bridge: []
liberapay: []
issuehunt: []
otechie: []
lfms_crowdfunding: []
custom: []
EOF

# Edit CODE_OF_CONDUCT.md
# Edit CONTRIBUTING.md
# Edit SUPPORT.md
```

## Org Settings

```bash
# View org settings (requires admin)
gh api /orgs/hashi-ai --jq '{name, description, blog, twitter_username}'

# Update org description
gh api /orgs/hashi-ai -X PATCH -f description="..." -f blog="https://..."
```

## Reference

See `references/clawdoc-org-manager.md` for detailed API calls, org policy enforcement, and billing settings.
