# Contributing to ClawDoc

Thank you for your interest in contributing! ClawDoc is designed to be forked, extended, and customized by the community.

## Ways to Contribute

### 🐛 Report Issues
Found a bug or inaccuracy? Open an issue with:
- The exact error message
- Your OpenClaw version
- Config snippet (redact secrets)
- Steps to reproduce

### 📝 Improve Documentation
- Fix inaccuracies in SKILL.md bodies
- Add missing reference docs
- Improve clarity or examples
- Add transllations

### 🌳 Extend Skills
- Add new skills for uncovered areas
- Expand reference docs with missing content
- Add new diagnostic flows to troubleshooting

### 🎯 Create Variants
- Fork ClawDoc for your own use case
- Publish your variant on ClawHub
- Share your fork on Discord

---

## Skill Conventions

### Naming
- Lowercase letters, digits, and hyphens only
- Under 64 characters
- Example: `openclaw-config`, `openclaw-memory`

### SKILL.md Structure
```markdown
---
name: skill-name
description: Trigger conditions. Use when [exact use case]. Triggers on: [keywords].
---

# Skill Name

## Section 1
Content...

## Section 2
More content...

## References
- `references/FILE.md` — topic details
```

### Frontmatter Rules
- `name`: Unique skill identifier
- `description`: Primary triggering mechanism — what it does + when to use + keywords
- No other fields in frontmatter

### Progressive Disclosure
- SKILL.md body: keep under 500 lines
- Deep content → `references/` directory
- One level of references only (no deeply nested docs)

### File Organization
```
skill-name/
├── SKILL.md           # Required
└── references/        # Optional
    ├── deep-topic.md
    └── config-ref.md
```

---

## Adding New Skills

### Step 1: Plan the skill
- What does this skill do?
- What are the exact trigger conditions?
- What scripts/references/assets are needed?

### Step 2: Create the directory
```bash
mkdir -p skills/my-new-skill/references
```

### Step 3: Write SKILL.md
Follow the frontmatter and progressive disclosure rules above.

### Step 4: Add bundled resources
Add scripts, references, or assets as needed.

### Step 5: Test
Ask ClawDoc to use the new skill and verify it routes correctly.

---

## Publishing

1. Package your skill: `scripts/package_skill.py skills/my-new-skill/`
2. Share on ClawHub: https://clawhub.ai
3. Announce on Discord: https://discord.com/invite/clawd

---

## Style Guide

- **Imperative/infinitive form** in instructions
- **Concise** — challenge every paragraph's token cost
- **Code examples** over prose explanations
- **Exact quotes** from docs over paraphrasing
- **Show your work** — before/after diffs when auditing or fixing
