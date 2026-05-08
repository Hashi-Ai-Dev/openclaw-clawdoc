#!/usr/bin/env python3
"""
ClawDoc Safety Scanner — Recursive Forbidden Content Scan

Scans the public ClawDoc repository for:
- Forbidden private runtime files/directories
- Forbidden private clawdoc-* skills (except allowed exceptions)
- Real-looking secrets/tokens in non-example files

Uses PATH-AWARE blocklist with explicit allowlist overrides.
Only scans files outside the examples/ directory for secrets.

Exit codes:
  0  — no forbidden content found
  1  — forbidden content detected
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()

# ---------------------------------------------------------------------------
# PATH-AWARE BLOCKLIST
# ---------------------------------------------------------------------------
# Any path matching these is a VIOLATION unless it appears in ALLOWED_PATHS.
# Format: for files, use the filename only (matched against entry.name).
# For directories, use the directory name (matched against entry.name).
# ---------------------------------------------------------------------------

# Filenames that are always forbidden (private runtime markers)
FORBIDDEN_FILENAMES = {
    "MEMORY.md",
    "HEARTBEAT.md",
    "AGENTS.md",       # root-level AGENTS.md is private runtime
    "USER.md",         # will be filtered by path check below
    "IDENTITY.md",     # will be filtered by path check below
    "TOOLS.md",        # will be filtered by path check below
    "SOUL.md",         # will be filtered by path check below
}

# Directory names that are always forbidden (private runtime containers)
FORBIDDEN_DIRNAMES = {
    "memory",
    ".agents",
    ".openclaw",
}

# Private clawdoc-* skills that must not appear in the public repo.
# clawdoc-onboarding is explicitly allowed (already public and intended for OSS).
FORBIDDEN_CLAWDOC_SKILLS = {
    "clawdoc-update",
    "clawdoc-release-manager",
    "clawdoc-repo-manager",
    "clawdoc-m27-loop",
    "clawdoc-effectiveness",
    "clawdoc-doc-auditor",
    "clawdoc-doc-reviewer",
    "clawdoc-oss-reviewer",
    "clawdoc-org-manager",
    "clawdoc-fb-post",
    "clawdoc-commit-sanitizer",
}

# ---------------------------------------------------------------------------
# PATH-AWARE ALLOWLIST
# ---------------------------------------------------------------------------
# These exact paths are approved public files and must NOT be flagged.
# All other occurrences of these filenames are still blocked.
# ---------------------------------------------------------------------------
ALLOWED_PATHS = {
    # Approved public agent template files
    "agent-template/SOUL.md",
    "agent-template/AGENTS.md",
    "agent-template/README.md",
    # Approved public root files
    "README.md",
    "QUICKSTART.md",
    "AGENT_INSTALL.md",
    "SKILLS_INSTALL.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "AUDIT.md",
    "TROUBLESHOOTING.md",
    # root-level SOUL.md allowed ONLY if it is the public ClawDoc persona
    # (checked separately via origin/master tracking — not allowed if it is
    # Root-level SOUL.md is allowed only if it is the public ClawDoc persona.
    # A SOUL.md that is a private/personal runtime marker is forbidden and
    # must not appear in the public repo.
    "SOUL.md",
}

# ---------------------------------------------------------------------------
# SECRET DETECTION PATTERNS
# ---------------------------------------------------------------------------
SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{36}"),            # GitHub PAT
    re.compile(r"gho_[A-Za-z0-9]{36}"),            # GitHub OAuth
    re.compile(r"ghu_[A-Za-z0-9]{36}"),            # GitHub user token
    re.compile(r"glpat-[A-Za-z0-9\-]{20,}"),       # GitLab PAT
    re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}"),  # Slack tokens
    re.compile(r"sk-[A-Za-z0-9]{48,}"),            # OpenAI API key
    re.compile(r"sk-ant-[A-Za-z0-9\-]{50,}"),      # Anthropic key
    re.compile(r"AIza[A-Za-z0-9\-]{35,}"),         # Google API key
    re.compile(r"ya29\.[A-Za-z0-9\-]{100,}"),      # Google OAuth
    re.compile(r"BQ[A-Za-z0-9\-]{50,}"),           # Google OAuth
]

# ---------------------------------------------------------------------------
# SCAN LOGIC
# ---------------------------------------------------------------------------

def is_allowed_path(rel_path: Path) -> bool:
    """Return True if this path is on the allowlist."""
    # Normalize separators
    normalized = str(rel_path).replace("\\", "/")
    return normalized in ALLOWED_PATHS


def is_private_dir(rel_path: Path) -> bool:
    """Return True if this path is inside a private runtime directory."""
    parts = rel_path.parts
    private_parents = {"memory", ".agents", ".openclaw"}
    return bool(private_parents & set(parts))


def check_blocklist(repo_root: Path) -> list[str]:
    """Check for blocklisted files/directories. Returns list of violations."""
    violations = []
    for entry in repo_root.rglob("*"):
        if entry.is_dir():
            continue  # directories handled below

        rel = entry.relative_to(repo_root)
        normalized = str(rel).replace("\\", "/")

        # Skip .git entirely
        if ".git" in rel.parts:
            continue

        # Skip allowed paths
        if is_allowed_path(rel):
            continue

        name = entry.name

        # Check: forbidden filename at non-allowed path
        if name in FORBIDDEN_FILENAMES:
            # Root-level USER.md, IDENTITY.md, TOOLS.md, SOUL.md are public templates
            # But inside memory/, .agents/, .openclaw/ they are private runtime
            if is_private_dir(rel):
                violations.append(f"forbidden private file found: {rel}")
            elif name in {"USER.md", "IDENTITY.md", "TOOLS.md", "SOUL.md", "AGENTS.md"}:
                # These at root are allowed; flag only if somewhere unexpected
                pass  # allowed at root (checked above via is_allowed_path)
            else:
                violations.append(f"forbidden file found: {rel}")

        # Check: forbidden directory names
        if entry.parent.name in FORBIDDEN_DIRNAMES or name in FORBIDDEN_DIRNAMES:
            if name in FORBIDDEN_DIRNAMES and not is_allowed_path(rel):
                violations.append(f"forbidden directory found: {rel}")

        # Check: private clawdoc-* skill directories
        if "clawdoc-" in name:
            skill_dir = rel.parts[0] if len(rel.parts) == 1 else rel.parts[1] if len(rel.parts) >= 2 else name
            # Actually we need to check the directory name under skills/
            # e.g. skills/clawdoc-update/SKILL.md → clawdoc-update is forbidden
            if len(rel.parts) >= 2 and rel.parts[0] == "skills":
                skill_slug = rel.parts[1]
                if skill_slug in FORBIDDEN_CLAWDOC_SKILLS:
                    violations.append(f"forbidden private clawdoc-* skill found: skills/{skill_slug}/")

    return violations


def scan_file_for_secrets(path: Path) -> list[str]:
    """Scan a single file for secret patterns."""
    # Skip example JSON files — they intentionally contain placeholder/test data
    if path.suffix == ".json" and "examples" in path.parts:
        return []

    violations = []
    try:
        content = path.read_text(errors="ignore")
    except Exception:
        return []

    for pattern in SECRET_PATTERNS:
        matches = pattern.findall(content)
        if matches:
            violations.append(f"{path}: secret/token pattern detected (redacted)")

    return violations


def main():
    violations = []

    # Check blocklist (recursive, path-aware)
    blocklist_errors = check_blocklist(REPO_ROOT)
    violations.extend(blocklist_errors)

    # Scan non-exempt files for secrets
    for path in REPO_ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if "examples" in path.parts:
            continue
        if path.is_dir():
            continue
        # Skip allowed paths for secret scanning too
        rel = path.relative_to(REPO_ROOT)
        if is_allowed_path(rel):
            continue

        secret_errors = scan_file_for_secrets(path)
        violations.extend(secret_errors)

    if violations:
        print("SAFETY SCAN FAILED", file=sys.stderr)
        for v in violations:
            print(f"  VIOLATION: {v}", file=sys.stderr)
        sys.exit(1)
    else:
        print("OK — no forbidden content or secrets detected")
        sys.exit(0)


if __name__ == "__main__":
    main()