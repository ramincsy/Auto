#!/usr/bin/env python3
"""
Create contribution branches for manual bulk contribution runs.

Usage:
    python scripts/create_contribution_branches.py [count]

Default:
    Uses BULK_COUNT if set, otherwise 20 branch attempts
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd, check=True):
    """Run shell command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=check
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        print(f"❌ Command error: {e}")
        return "", 1


def get_date_string():
    """Get current date.

    Includes hour/minute/second if available for uniqueness.
    """
    year = os.getenv("year")
    month = os.getenv("month")
    day = os.getenv("day")
    hour = os.getenv("hour")
    minute = os.getenv("minute")
    second = os.getenv("second")

    if not (year and month and day):
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")

    result = f"{year}-{month}-{day}"
    if hour:
        result += f"-{hour}"
        if minute:
            result += f"-{minute}"
        if second:
            result += f"-{second}"
    return result


def get_bulk_count():
    """Return the requested branch count."""
    raw_value = sys.argv[1] if len(sys.argv) > 1 else os.getenv("BULK_COUNT", "20")
    try:
        count = int(raw_value)
    except ValueError:
        count = 20

    return max(1, min(count, 100))


def is_ci_environment():
    """Return whether the script is running in CI."""
    return os.getenv("CI", "").strip().lower() == "true"


def ensure_safe_local_worktree():
    """Avoid destructive cleanup on a developer machine."""
    if is_ci_environment():
        return True

    output, _ = run_command("git status --porcelain", check=False)
    if output.strip():
        print("Warning: local worktree is not clean.")
        print(
            "Bulk branch creation is blocked locally to avoid deleting unrelated files."
        )
        print("Run this helper in CI, or clean/stash your worktree first.")
        return False

    return True


def configure_git_identity():
    """Configure git identity without changing global developer settings."""
    email = os.getenv("GIT_AUTHOR_EMAIL", "ramincsy2@gmail.com")
    name = os.getenv("GIT_AUTHOR_NAME", "ramincsy")
    run_command(f'git config user.email "{email}"', check=False)
    run_command(f'git config user.name "{name}"', check=False)


def create_contribution_branch(date_str, index):
    """
    Create a branch with a unique contribution commit.

    Args:
        date_str: Date string (YYYY-MM-DD)
        index: Contribution index (0-4)

    Returns:
        Branch name if successful, None otherwise
    """
    branch_name = f"contribution-{date_str}-{index}"

    print(f"  📌 Creating branch: {branch_name}")

    # Fetch latest from origin
    run_command("git fetch origin", check=False)

    # In CI we can reset the ephemeral worktree. Locally we avoid destructive cleanup.
    if is_ci_environment():
        run_command("git checkout main", check=False)
        run_command("git reset --hard origin/main", check=False)
        run_command("git clean -fd", check=False)

    # Create new branch from main
    output, code = run_command(
        f"git checkout -b {branch_name} origin/main", check=False
    )
    if code != 0:
        # Branch might already exist, try to checkout and reset
        output, code = run_command(f"git checkout {branch_name}", check=False)
        if code == 0:
            run_command(f"git reset --hard origin/{branch_name}", check=False)
        else:
            print(f"    ❌ Failed to create/checkout branch")
            return None

    # Create or modify a unique file
    parts = date_str.split("-")
    year, month, day = parts[0], parts[1], parts[2]
    hour = parts[3] if len(parts) > 3 else None
    minute = parts[4] if len(parts) > 4 else None
    second = parts[5] if len(parts) > 5 else None

    filename = f"{day}-contribution-{index}.md"
    if hour:
        filename = f"{day}-{hour}"
        if minute:
            filename += f"-{minute}"
        if second:
            filename += f"-{second}"
        filename += f"-contribution-{index}.md"

    filepath = Path("updates") / year / month / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Only create if doesn't exist
    if not filepath.exists():
        content = f"""# Contribution #{index} - {date_str}

## Topic
Generated contribution #{index}

## Activity
- Index: {index}
- Date: {date_str}
- Type: Generated

## Details
Created by the manual bulk contribution helper.
Review this content before merging.
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        # Stage and commit
        run_command(f'git add "{filepath}"')
        run_command(
            f'git commit -m "Add contribution #{index} - {date_str}"', check=False
        )

        # Push branch
        output, code = run_command(f"git push origin {branch_name} --force-with-lease")
        if code == 0:
            print(f"    ✅ Branch created and pushed")
            return branch_name
        else:
            print(f"    ❌ Failed to push branch: {output}")
            return None
    else:
        print(f"    ⏭️  File already exists (branch skipped)")
        return None


def main():
    """Main function."""
    if not ensure_safe_local_worktree():
        return

    date_str = get_date_string()
    count = get_bulk_count()

    print(f"Creating {count} contribution branch(es) for {date_str}...")
    print()

    configure_git_identity()

    created_branches = []

    for i in range(count):
        branch = create_contribution_branch(date_str, i)
        if branch:
            created_branches.append(branch)

    # Return to main
    if is_ci_environment():
        run_command("git checkout main", check=False)
        run_command("git reset --hard origin/main", check=False)
        run_command("git clean -fd", check=False)

    if created_branches:
        print(f"\n✨ Created {len(created_branches)} contribution branches:")
        for b in created_branches:
            print(f"   - {b}")
    else:
        print("\n⚠️  No new branches were created")


if __name__ == "__main__":
    main()
