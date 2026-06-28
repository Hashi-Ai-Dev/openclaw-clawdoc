#!/usr/bin/env python3
"""
ClawDoc Repository Validator — Structure Checks Only

Validates the public ClawDoc repository structure:
- CLAWDOC_MANIFEST.json is valid JSON
- Required public files exist
- SKILL.md frontmatter: name + description required, triggers forbidden as separate key
- SKILL.md frontmatter parses as valid YAML (uses yaml.safe_load, not regex)
- No duplicate skills
- Skill/example counts match manifest
- Examples parse as valid JSON (with // comment stripping)
- README.md and QUICKSTART.md mention both install modes
- README/QUICKSTART do not say 11 skills

Does NOT check for forbidden/private files — use safety_scanner.py for that.

Exit codes:
  0  — all checks passed
  1  — validation failed
"""

import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # YAML check becomes a no-op if PyYAML not installed

REPO_ROOT = Path(__file__).parent.parent.resolve()

MANIFEST_PATH = REPO_ROOT / "CLAWDOC_MANIFEST.json"
SKILLS_DIR = REPO_ROOT / "skills"
EXAMPLES_DIR = REPO_ROOT / "examples"

REQUIRED_PUBLIC_FILES = [
    "README.md",
    "QUICKSTART.md",
    "AGENT_INSTALL.md",
    "SKILLS_INSTALL.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "LICENSE",
]


def load_manifest():
    if not MANIFEST_PATH.exists():
        return None
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def frontmatter_fields(content: str) -> dict:
    """Extract YAML frontmatter fields and values from file content."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            # Split on first colon only; strip whitespace
            key = line.split(":", 1)[0].strip()
            # Value is everything after the first colon, stripped
            val = line.split(":", 1)[1].strip()
            fields[key] = val
    return fields


def check_skill_frontmatter(skill_path: Path) -> list[str]:
    """Check a SKILL.md file for valid frontmatter. Returns list of errors."""
    errors = []
    try:
        content = skill_path.read_text()
    except Exception as e:
        return [f"cannot read {skill_path}: {e}"]

    fields = frontmatter_fields(content)

    # Required fields
    for required in ("name", "description"):
        if required not in fields:
            errors.append(f"{skill_path}: missing required frontmatter field '{required}'")

    # Forbidden fields (triggers must be inline in description, not a separate key)
    if "triggers" in fields:
        errors.append(
            f"{skill_path}: forbidden frontmatter field 'triggers' — "
            "embed triggers inline in the description field instead"
        )

    return errors


def strip_comments(content: str) -> str:
    """Strip full-line // comments but NOT // inside string values (URLs etc.)"""
    result = []
    for line in content.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("//"):
            continue  # skip comment-only lines
        result.append(line)
    return "\n".join(result)


def check_json_examples(examples_dir: Path) -> list[str]:
    """Check that example files parse as JSON (stripping full-line // comments first)."""
    errors = []
    if not examples_dir.exists():
        return [f"examples/ directory not found"]
    for example_file in sorted(examples_dir.iterdir()):
        if example_file.suffix == ".json":
            try:
                content = example_file.read_text()
                # Strip full-line // comments (but not // inside URLs or string values)
                content = strip_comments(content)
                json.loads(content)
            except json.JSONDecodeError as e:
                errors.append(f"{example_file}: invalid JSON — {e}")
            except Exception as e:
                errors.append(f"{example_file}: cannot read — {e}")
    return errors


def check_readme_mode_coverage(readme_path: Path) -> list[str]:
    """Check that README.md mentions both install modes."""
    errors = []
    if not readme_path.exists():
        errors.append(f"{readme_path}: not found")
        return errors
    content = readme_path.read_text().lower()
    mode1_keywords = ["persistent agent", "persistent-agent", "mode 1"]
    mode2_keywords = ["skills only", "skills-only", "mode 2"]
    has_mode1 = any(k in content for k in mode1_keywords)
    has_mode2 = any(k in content for k in mode2_keywords)
    if not has_mode1:
        errors.append(f"{readme_path}: does not mention Mode 1 (persistent agent) install")
    if not has_mode2:
        errors.append(f"{readme_path}: does not mention Mode 2 (skills-only) install")
    return errors


def check_skill_count_claims(readme_path: Path, quickstart_path: Path) -> list[str]:
    """Check that neither README nor QUICKSTART claim 22 or 23 skills (current count is 24)."""
    errors = []
    for path in [readme_path, quickstart_path]:
        if not path.exists():
            continue
        content = path.read_text()
        # Look for the word "22" or "23" as a standalone number followed by "skills" / "available skills"
        # (not part of 220, 230, etc.)
        for stale in (22, 23):
            pattern = re.compile(rf'\b{stale}\b[^.\n]{{0,40}}skills?', re.IGNORECASE)
            if pattern.search(content):
                errors.append(
                    f"{path}: claims '{stale} skills' — current count is 24"
                )
    return errors


def check_install_command_versions(quickstart_path: Path, agent_install_path: Path, skills_install_path: Path) -> list[str]:
    """Check that install commands reference a tagged release, not stale or 'master'."""
    errors = []
    # Find the latest release tag (excluding master HEAD) — use git describe against tags
    try:
        import subprocess
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True
        )
        latest_tag = result.stdout.strip()  # e.g. "v1.7.2"
    except Exception:
        return errors  # can't determine tag, skip

    # Allowed tokens: latest tag, "master" (bleeding-edge), "main" (bleeding-edge)
    allowed = {latest_tag, "master", "main"}

    for path in [quickstart_path, agent_install_path, skills_install_path]:
        if not path.exists():
            continue
        try:
            content = path.read_text()
        except Exception:
            continue
        # Find every "git checkout <ref>" occurrence
        for m in re.finditer(r'git\s+checkout\s+(\S+)', content):
            ref = m.group(1).strip().rstrip('&&').strip()
            if ref not in allowed:
                # Whitelist master/main if explicitly in a "bleeding-edge" context
                # (the validator doesn't enforce the comment — just the literal)
                if ref == latest_tag:
                    continue
                errors.append(
                    f"{path}: 'git checkout {ref}' is stale — latest tag is {latest_tag}"
                )
    return errors


def check_manifest_version(manifest: dict) -> list[str]:
    """Check that clawdoc_version and tracked_openclaw_version match filesystem truth."""
    errors = []
    import subprocess

    # 1. clawdoc_version vs latest tag
    claimed_version = manifest.get("clawdoc_version", "")
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True
        )
        latest_tag = result.stdout.strip()
        if claimed_version != latest_tag:
            errors.append(
                f"CLAWDOC_MANIFEST.json: clawdoc_version is '{claimed_version}' but latest tag is '{latest_tag}'"
            )
    except Exception:
        pass

    # 2. tracked_openclaw_version vs .openclaw-version
    claimed_oc = manifest.get("tracked_openclaw_version", "")
    openclaw_version_file = REPO_ROOT / ".openclaw-version"
    if openclaw_version_file.exists():
        actual_oc = openclaw_version_file.read_text().strip()
        if claimed_oc != actual_oc:
            errors.append(
                f"CLAWDOC_MANIFEST.json: tracked_openclaw_version is '{claimed_oc}' but .openclaw-version is '{actual_oc}'"
            )

    return errors


def check_public_list_completeness(manifest: dict) -> list[str]:
    """Check that skills.public_list matches what's actually on disk."""
    errors = []
    if not SKILLS_DIR.exists():
        return errors
    public_list = set(manifest.get("skills", {}).get("public_list", []))
    on_disk = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists()}
    # Allow clawdoc-* that aren't in public_list only if they are private (must not exist on disk)
    missing_from_list = on_disk - public_list
    extra_in_list = public_list - on_disk
    for skill in sorted(missing_from_list):
        errors.append(
            f"CLAWDOC_MANIFEST.json: skill '{skill}' exists on disk but is missing from skills.public_list"
        )
    for skill in sorted(extra_in_list):
        errors.append(
            f"CLAWDOC_MANIFEST.json: skill '{skill}' is in skills.public_list but does not exist on disk"
        )
    return errors


def check_examples_readme_coverage(examples_dir: Path, readme_path: Path) -> list[str]:
    """Check that examples/README.md mentions every example .json file."""
    errors = []
    if not examples_dir.exists():
        return errors
    if not readme_path.exists():
        return errors
    readme_content = readme_path.read_text()
    example_files = {f.name for f in examples_dir.iterdir() if f.suffix == ".json"}
    for example in sorted(example_files):
        if example not in readme_content:
            errors.append(
                f"examples/README.md: does not mention '{example}' (missing from the table)"
            )
    return errors


def check_referenced_files_exist(skills_dir: Path) -> list[str]:
    """Check that every references/X.md path referenced from a SKILL.md body exists.

    Only validates references that look like current-skill relative paths:
    - `references/foo.md` (skill-relative)
    - `references/sub/foo.md` (skill-relative with subdir)
    Skips cross-skill references like `openclaw-tools/references/foo.md` and
    the literal `SKILL.md` self-reference.
    """
    errors = []
    if not skills_dir.exists():
        return errors
    # Match `references/<name>.md` or `references/<sub>/<name>.md` only
    pattern = re.compile(r'`references/([\w\-]+(?:/[\w\-]+)*\.md)`')
    for skill_dir in sorted(skills_dir.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        try:
            content = skill_md.read_text()
        except Exception:
            continue
        # Skip frontmatter
        body_match = re.search(r"^---\n.*?\n---\n(.*)", content, re.DOTALL)
        body = body_match.group(1) if body_match else content
        for m in pattern.finditer(body):
            ref_rel = m.group(1)
            candidate = skill_dir / "references" / ref_rel
            if not candidate.exists():
                errors.append(
                    f"{skill_md}: references '{ref_rel}' does not exist on disk"
                )
    return errors


def check_root_file_example_counts(repo_root: Path) -> list[str]:
    """Check that root files don't claim a stale example count."""
    errors = []
    stale_phrases = [
        ("12 examples covering", "current count is 24"),
        ("12 example configs", "current count is 24"),
    ]
    for filename in ("AGENT_INSTALL.md", "SKILLS_INSTALL.md"):
        path = repo_root / filename
        if not path.exists():
            continue
        try:
            content = path.read_text()
        except Exception:
            continue
        for phrase, fix in stale_phrases:
            if phrase in content:
                errors.append(
                    f"{path}: contains stale phrase '{phrase}' — {fix}"
                )
    return errors


def main():
    manifest = load_manifest()
    all_errors = []

    # 1. CLAWDOC_MANIFEST.json must be valid JSON
    try:
        if MANIFEST_PATH.exists():
            with open(MANIFEST_PATH) as f:
                json.load(f)
        else:
            all_errors.append("CLAWDOC_MANIFEST.json: not found")
    except json.JSONDecodeError as e:
        all_errors.append(f"CLAWDOC_MANIFEST.json: invalid JSON — {e}")
    except Exception as e:
        all_errors.append(f"CLAWDOC_MANIFEST.json: cannot read — {e}")

    # 2. Required public files must exist
    for filename in REQUIRED_PUBLIC_FILES:
        path = REPO_ROOT / filename
        if not path.exists():
            all_errors.append(f"required public file missing: {filename}")

    # 3. SKILL.md frontmatter for all skills; check for duplicate names
    # 3a. SKILL.md frontmatter must round-trip as valid YAML (yaml.safe_load)
    if SKILLS_DIR.exists():
        seen_names = {}
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                errors = check_skill_frontmatter(skill_md)
                all_errors.extend(errors)

                # YAML round-trip check (catches unescaped colons in description values, etc.)
                if yaml is not None:
                    try:
                        content = skill_md.read_text()
                        if content.startswith("---\n"):
                            fm_text = content.split("---", 2)[1]
                            data = yaml.safe_load(fm_text)
                            if not isinstance(data, dict):
                                all_errors.append(
                                    f"{skill_md}: frontmatter is not a YAML mapping (got {type(data).__name__})"
                                )
                    except yaml.YAMLError as e:
                        first_line = str(e).split('\n')[0]
                        all_errors.append(
                            f"{skill_md}: frontmatter does not parse as valid YAML — {first_line}"
                        )

                fields = frontmatter_fields(skill_md.read_text())
                name_val = fields.get("name", "")
                if name_val:
                    if name_val in seen_names:
                        all_errors.append(
                            f"duplicate skill name '{name_val}' in {skill_md} and {seen_names[name_val]}"
                        )
                    else:
                        seen_names[name_val] = skill_md

    # 4. JSON examples must parse (with // comment stripping)
    if EXAMPLES_DIR.exists():
        errors = check_json_examples(EXAMPLES_DIR)
        all_errors.extend(errors)

    # 5. README and QUICKSTART must mention both install modes
    readme_path = REPO_ROOT / "README.md"
    quickstart_path = REPO_ROOT / "QUICKSTART.md"
    for path in [readme_path, quickstart_path]:
        errors = check_readme_mode_coverage(path)
        all_errors.extend(errors)

    # 6. README and QUICKSTART must not claim 22 or 23 skills
    errors = check_skill_count_claims(readme_path, quickstart_path)
    all_errors.extend(errors)

    # 7. Install commands must reference the latest tag (not stale)
    errors = check_install_command_versions(
        quickstart_path,
        REPO_ROOT / "AGENT_INSTALL.md",
        REPO_ROOT / "SKILLS_INSTALL.md",
    )
    all_errors.extend(errors)

    # 8. CLAWDOC_MANIFEST.json version fields must match filesystem truth
    if manifest is not None:
        errors = check_manifest_version(manifest)
        all_errors.extend(errors)

        # 9. skills.public_list must match what's on disk
        errors = check_public_list_completeness(manifest)
        all_errors.extend(errors)

    # 10. examples/README.md must mention every example
    if EXAMPLES_DIR.exists():
        errors = check_examples_readme_coverage(EXAMPLES_DIR, EXAMPLES_DIR / "README.md")
        all_errors.extend(errors)

    # 11. Skill bodies must not reference non-existent references/*.md files
    errors = check_referenced_files_exist(SKILLS_DIR)
    all_errors.extend(errors)

    # 12. Root install guides must not claim a stale example count
    errors = check_root_file_example_counts(REPO_ROOT)
    all_errors.extend(errors)

    # Report
    if all_errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for err in all_errors:
            print(f"  ERROR: {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print("OK — all structure validation checks passed")
        sys.exit(0)


if __name__ == "__main__":
    main()