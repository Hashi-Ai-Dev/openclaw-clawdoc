#!/usr/bin/env python3
"""
ClawDoc Safety Scanner — Recursive Forbidden Content Scan

Scans the public ClawDoc repository for:
- Forbidden private runtime files/directories
- Forbidden private clawdoc-* skills (except allowed exceptions)
- Real-looking secrets/tokens in non-example files
- Prompt-injection / permission-expansion patterns in privileged Markdown surfaces

Uses PATH-AWARE blocklist with explicit allowlist overrides.
Only scans files outside the examples/ directory for secrets.
Privilege injection scanning covers skills/ and key docs only (not SECURITY.md / CONTRIBUTING.md).

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
# Note: ALLOWED_PATHS bypasses only private-file/path blocklist checks.
# Secret/token scanning still runs on allowed-path files.
# ---------------------------------------------------------------------------
ALLOWED_PATHS = {
    # Approved public agent template files
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
    # root-level SOUL.md allowed only if it is the public ClawDoc persona
    "SOUL.md",
}

# ---------------------------------------------------------------------------
# SECRET DETECTION PATTERNS
# ---------------------------------------------------------------------------
SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{36}"),             # GitHub PAT
    re.compile(r"github_pat_[A-Za-z0-9_]{22,}"),    # GitHub fine-grained PAT
    re.compile(r"gho_[A-Za-z0-9]{36}"),             # GitHub OAuth
    re.compile(r"ghu_[A-Za-z0-9]{36}"),             # GitHub user token
    re.compile(r"glpat-[A-Za-z0-9\-]{20,}"),        # GitLab PAT
    re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}"),   # Slack tokens
    re.compile(r"sk-[A-Za-z0-9]{48,}"),             # OpenAI API key
    re.compile(r"sk-ant-[A-Za-z0-9\-]{50,}"),       # Anthropic key
    re.compile(r"sk-or-v1-[A-Za-z0-9\-]{40,}"),     # OpenRouter key
    re.compile(r"sk-cp-[A-Za-z0-9\-]{40,}"),        # MiniMax API key
    re.compile(r"AIza[A-Za-z0-9\-]{35,}"),          # Google API key
    re.compile(r"ya29\.[A-Za-z0-9\-]{100,}"),       # Google OAuth
    re.compile(r"BQ[A-Za-z0-9\-]{50,}"),            # Google OAuth
    # Provider env assignment patterns: TOKEN=VALUE where VALUE looks like a real key
    re.compile(r"(?i)(openai_api_key|anthropic_api_key|openrouter_api_key|minimax_api_key|discord_bot_token|github_token)\s*=\s*['\"]?[A-Za-z0-9_\-]{20,}['\"]?"),
]

# Patterns that indicate a deliberate placeholder/example (not a real secret)
PLACEHOLDER_PATTERNS = [
    re.compile(r"your-[a-z]+-id", re.IGNORECASE),        # your-workspace-id, your-api-key
    re.compile(r"your-[a-z]+-host", re.IGNORECASE),     # your-honcho-host.com
    re.compile(r"<[^>]+>"),                               # <YOUR_TOKEN>
    re.compile(r"'.*?'|\".*?\""),                       # 'placeholder', "placeholder"
    re.compile(r"xxx+|XXXX+"),                            # xxx, XXXX
    re.compile(r"OPENCLAW_[A-Z_]{30,}"),                # OpenClaw env var names (e.g. OPENCLAW_BUNDLED_CHANNEL_UPDATE_DOCKER_RUN_TIMEOUT) — not secrets
]

# ---------------------------------------------------------------------------
# PRIVILEGED MARKDOWN — INJECTION / PERMISSION-EXPANSION PATTERNS
# ---------------------------------------------------------------------------
# Scanned only in privileged Markdown surfaces listed in PRIVILEGED_PATH_PREFIXES.
# SECURITY.md and CONTRIBUTING.md are excluded to avoid false positives
# (they name these threats as warnings, not instructions).
# ---------------------------------------------------------------------------
PRIVILEGED_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+(instructions?|rules?|constraints?)", re.IGNORECASE),
    re.compile(r"(disregard|forget)\s+(your\s+)?(instructions?|rules?|constraints?)", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+(a|an)\s+\w+\s+with\s+(elevated|expanded|admin|root)", re.IGNORECASE),
    re.compile(r"grant\s+(yourself|your)\s+(full\s+)?(admin|elevated|root)\s+permission", re.IGNORECASE),
    re.compile(r"you\s+have\s+permission\s+to\s+(escalate|elevate|bypass)", re.IGNORECASE),
    re.compile(r"(elevate|escalate)\s+(your|their)\s+(privileges?|permissions?|access)", re.IGNORECASE),
    re.compile(r"--\s*superuser|--sudo", re.IGNORECASE),
    re.compile(r"new\s+permissions?\s*:\s*\[.*(?:admin|root|elevated|system).*\]", re.IGNORECASE),
    re.compile(r"(write|overwrite|delete)[_-]?(to[_-])?file", re.IGNORECASE),
    re.compile(r"modify[_-]?(your\s+)?(system|prompt|instructions|AGENTS|SOUL)", re.IGNORECASE),
    re.compile(r"<system>|<human>|<system_message>", re.IGNORECASE),
]

# Paths that are privileged Markdown surfaces — scanned for injection patterns.
# SECURITY.md and CONTRIBUTING.md are intentionally excluded (they discuss threats as warnings).
PRIVILEGED_PATH_PREFIXES = {
    "skills/",
    "SOUL.md",
    "AGENTS.md",
    "agent-template/",
    "AGENT_INSTALL.md",
    "SKILLS_INSTALL.md",
    "TROUBLESHOOTING.md",
    "README.md",
    "QUICKSTART.md",
}

# ---------------------------------------------------------------------------
# SCAN LOGIC
# ---------------------------------------------------------------------------

def is_allowed_path(rel_path: Path) -> bool:
    """Return True if this path is on the allowlist."""
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
            continue

        rel = entry.relative_to(repo_root)
        normalized = str(rel).replace("\\", "/")

        if ".git" in rel.parts:
            continue

        if is_allowed_path(rel):
            continue

        name = entry.name

        if name in FORBIDDEN_FILENAMES:
            if is_private_dir(rel):
                violations.append(f"forbidden private file found: {rel}")
            elif name in {"USER.md", "IDENTITY.md", "TOOLS.md", "SOUL.md", "AGENTS.md"}:
                pass  # allowed at root (checked above via is_allowed_path)
            else:
                violations.append(f"forbidden file found: {rel}")

        if entry.parent.name in FORBIDDEN_DIRNAMES or name in FORBIDDEN_DIRNAMES:
            if name in FORBIDDEN_DIRNAMES and not is_allowed_path(rel):
                violations.append(f"forbidden directory found: {rel}")

        if "clawdoc-" in name and len(rel.parts) >= 2 and rel.parts[0] == "skills":
            skill_slug = rel.parts[1]
            if skill_slug in FORBIDDEN_CLAWDOC_SKILLS:
                violations.append(f"forbidden private clawdoc-* skill found: skills/{skill_slug}/")

    return violations


def scan_file_for_secrets(path: Path) -> list[str]:
    """Scan a single file for secret patterns.

    Skips examples/ (they contain placeholder config snippets).
    Skips files that contain only placeholder patterns (not real secrets).
    ALLOWED_PATHS does NOT exempt files from secret scanning.
    """
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
        real_matches = []
        for match in matches:
            # Skip if the match is a known placeholder
            if any(ph.match(match) for ph in PLACEHOLDER_PATTERNS):
                continue
            real_matches.append(match)
        if real_matches:
            violations.append(f"{path}: secret/token pattern detected (redacted)")

    return violations


def check_privileged_markdown(path: Path) -> list[str]:
    """Scan privileged Markdown files for prompt-injection / permission-expansion patterns."""
    violations = []
    try:
        content = path.read_text(errors="ignore")
    except Exception:
        return []

    for pattern in PRIVILEGED_PATTERNS:
        if pattern.search(content):
            violations.append(f"{path}: privileged-content injection pattern detected")
    return violations


def main():
    violations = []

    # Check blocklist (recursive, path-aware)
    blocklist_errors = check_blocklist(REPO_ROOT)
    violations.extend(blocklist_errors)

    # Scan all non-exempt files for secrets
    # NOTE: ALLOWED_PATHS bypasses only blocklist checks, not secret scanning.
    # Only examples/ directory is exempt from secret scanning.
    for path in REPO_ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if "examples" in path.parts:
            continue
        if path.is_dir():
            continue

        secret_errors = scan_file_for_secrets(path)
        violations.extend(secret_errors)

    # Check privileged Markdown files for injection/permission-expansion patterns
    for path in REPO_ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(REPO_ROOT)
        normalized = str(rel).replace("\\", "/")
        if any(normalized.startswith(p) for p in PRIVILEGED_PATH_PREFIXES):
            violations.extend(check_privileged_markdown(path))

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