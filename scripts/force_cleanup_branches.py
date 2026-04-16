#!/usr/bin/env python3
"""
Force delete all contribution branches.

Usage:
    python scripts/force_cleanup_branches.py [--dry-run]

This script force deletes all remote contribution branches.
Use --dry-run to see what would be deleted without actually deleting.
"""

import os
import sys
import subprocess


def run_git_command(command):
    """Run a git command and return output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)


def get_contribution_branches():
    """Get list of all contribution branches."""
    success, stdout, stderr = run_git_command('git branch -r')

    if not success:
        print(f"❌ Error getting branches: {stderr}")
        return []

    branches = []
    for line in stdout.split('\n'):
        line = line.strip()
        if 'origin/' in line and ('contribution-' in line or 'daily-contribution-' in line):
            branch_name = line.replace('origin/', '')
            branches.append(branch_name)

    return branches


def delete_remote_branch(branch_name, dry_run=False):
    """Delete a remote branch."""
    if dry_run:
        print(f"    [DRY RUN] Would delete branch: {branch_name}")
        return True

    success, stdout, stderr = run_git_command(f'git push origin --delete {branch_name}')

    if success:
        print(f"    ✅ Deleted branch: {branch_name}")
        return True
    else:
        print(f"    ❌ Failed to delete branch {branch_name}: {stderr}")
        return False


def main():
    """Main function."""
    dry_run = "--dry-run" in sys.argv

    print("🧹 Force cleaning up all contribution branches...\n")

    if dry_run:
        print("🔍 DRY RUN MODE - No branches will be deleted\n")

    # Get all contribution branches
    branches = get_contribution_branches()

    if not branches:
        print("✅ No contribution branches found to clean up.")
        return 0

    print(f"Found {len(branches)} contribution branch(es) to clean up:\n")

    deleted_count = 0

    # Delete each branch
    for branch in branches:
        if delete_remote_branch(branch, dry_run=dry_run):
            deleted_count += 1

    if not dry_run:
        if deleted_count > 0:
            print(f"\n✨ Successfully cleaned up {deleted_count} branch(es)!")
        else:
            print(f"\n⚠️  No branches were successfully deleted")
    else:
        print(f"\n🔍 Would have cleaned up {deleted_count} branch(es)")

    return deleted_count


if __name__ == "__main__":
    cleaned = main()
    sys.exit(0)