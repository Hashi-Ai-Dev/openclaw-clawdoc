# Spine Org Manager — Reference

Detailed procedures for Hashi.Ai GitHub organization management.

## GitHub CLI Setup for Org

```bash
# Authenticate with GitHub
gh auth login

# Set default org
gh config set prompt disabled  # for scripting
```

## Repository Management

### Create Repo Under Org

```bash
gh repo create hashi-ai/<repo-name> \
  --public \
  --description "Description here" \
  --team <team-name> \
  --clone
```

### Archive/Unarchive

```bash
gh repo archive hashi-ai/<repo-name> --yes
gh repo unarchive hashi-ai/<repo-name>
```

### Transfer Repo

```bash
# From personal account to org
gh repo transfer hashi-ai/<repo-name> hashi-ai

# From another org to Hashi.Ai
gh repo transfer <source-org>/<repo-name> hashi-ai
```

## Team Management

### Create Team

```bash
gh api --method POST /orgs/hashi-ai/teams \
  -f name="<team-slug>" \
  -f description="Team description" \
  -f privacy=closed \
  -f permission=push
```

### Repo Permissions by Team

| Permission | Read | Triage | Write | Admin | Maintain | Main |
|---|---|---|---|---|---|---|
| Issues | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PRs | | ✓ | ✓ | ✓ | ✓ | ✓ |
| Push | | | ✓ | ✓ | ✓ | ✓ |
| Settings | | | | ✓ | ✓ | ✓ |

```bash
# Set default repo permission for org members
gh api /orgs/hashi-ai --method PATCH -f default_repository_permission=read
```

## Community Files

### .github/ISSUE_TEMPLATE/

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: File a bug report
labels: [bug]
body:
  - type: markdown
    attributes:
      value: |
        ## Bug Description
  - type: textarea
    attributes:
      label: Steps to Reproduce
      placeholder: 1. Go to '...'
```

### .github/PULL_REQUEST_TEMPLATE.md

```markdown
## Description
<!-- What does this PR do? -->

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No personal data in code or docs
```

## Org Billing & Settings

```bash
# View org roles
gh api /orgs/hashi-ai/members/<username> --jq '.role'

# Require 2FA for org members
gh api /orgs/hashi-ai --method PATCH -f require_two_factor_authentication=true

# Disable repository creation for members (only admins can create)
gh api /orgs/hashi-ai --method PATCH -f members_can_create_public_repos=false
```

## Org Audit Log

```bash
# View recent audit events (requires admin)
gh api /orgs/hashi-ai/audit-log --paginate | jq '.[] | {action, actor, created_at}'

# Filter by action
gh api "/orgs/hashi-ai/audit-log?phrase=action:repo.destroy" | jq '.'
```
