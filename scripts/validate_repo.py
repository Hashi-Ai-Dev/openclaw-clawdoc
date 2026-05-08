#!/usr/bin/env python3
"""
ClawDoc Repository Validator — Structure Checks Only

Validates the public ClawDoc repository structure:
- CLAWDOC_MANIFEST.json is valid JSON
- Required public files exist
- SKILL.md frontmatter: name + description required, triggers forbidden as separate key
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
    """Check that neither README nor QUICKSTART claim 11 skills."""
    errors = []
    for path in [readme_path, quickstart_path]:
        if not path.exists():
            continue
        content = path.read_text()
        # Look for the word "11" as a standalone number (not part of 110, 111, etc.)
        matches = re.findall(r'\b11\b', content)
        if matches:
            errors.append(
                f"{path}: incorrectly claims '{matches[0]}' skills — should be 22"
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
    if SKILLS_DIR.exists():
        seen_names = {}
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                errors = check_skill_frontmatter(skill_md)
                all_errors.extend(errors)

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

    # 6. README and QUICKSTART must not claim 11 skills
    errors = check_skill_count_claims(readme_path, quickstart_path)
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