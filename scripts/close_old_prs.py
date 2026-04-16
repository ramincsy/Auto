#!/usr/bin/env python3
"""
Close old contribution PRs that cannot be merged due to missing branches.

Usage:
    python scripts/close_old_prs.py [--dry-run]

This script closes old contribution PRs where the branch has been deleted.
Use --dry-run to see what would be closed without actually closing.
"""

import os
import sys
import requests
from datetime import datetime, timedelta, timezone


def get_github_token():
    """Get GitHub token from environment."""
    token = os.environ.get('GH_TOKEN3') or os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not token:
        print("❌ Error: No GitHub token found.")
        sys.exit(1)
    return token


def get_repo_info():
    """Get repository info."""
    repo = os.environ.get('GITHUB_REPOSITORY', 'ramincsy/Auto')
    owner, repo_name = repo.split('/', 1)
    return owner, repo_name


def get_old_contribution_prs(owner, repo, token, days_old=7):
    """Get contribution PRs older than specified days."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    params = {
        "state": "open",
        "per_page": 100
    }

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code != 200:
            print(f"❌ Error fetching PRs: {response.status_code}")
            return []

        all_prs = response.json()
        old_prs = []

        for pr in all_prs:
            created_at_str = pr['created_at'].replace('Z', '+00:00')
            created_at = datetime.fromisoformat(created_at_str)
            if created_at < cutoff_date:
                title = pr.get('title', '')
                if 'Daily Update' in title or 'Contribution #' in title:
                    old_prs.append(pr)

        return old_prs
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def close_pr(owner, repo, token, pr_number, pr_title, dry_run=False):
    """Close a PR."""
    if dry_run:
        print(f"    [DRY RUN] Would close PR #{pr_number}: {pr_title}")
        return True

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "state": "closed"
    }

    try:
        response = requests.patch(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            print(f"    ✅ Closed PR #{pr_number}: {pr_title}")
            return True
        else:
            print(f"    ❌ Error closing PR #{pr_number} (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"    ❌ Error: {str(e)}")
        return False


def main():
    """Main function."""
    dry_run = "--dry-run" in sys.argv

    print("🗂️  Closing old contribution PRs...\n")

    if dry_run:
        print("🔍 DRY RUN MODE - No PRs will be closed\n")

    token = get_github_token()
    owner, repo = get_repo_info()

    # Get old PRs (older than 7 days)
    old_prs = get_old_contribution_prs(owner, repo, token, days_old=7)

    if not old_prs:
        print("✅ No old contribution PRs found to close.")
        return 0

    print(f"Found {len(old_prs)} old contribution PR(s) to close:\n")

    closed_count = 0

    # Close each PR
    for pr in old_prs:
        pr_number = pr['number']
        pr_title = pr['title']
        created_at = pr['created_at']

        print(f"  Processing PR #{pr_number}: {pr_title} (created: {created_at})")

        if close_pr(owner, repo, token, pr_number, pr_title, dry_run=dry_run):
            closed_count += 1

    if not dry_run:
        if closed_count > 0:
            print(f"\n✨ Successfully closed {closed_count} PR(s)!")
        else:
            print(f"\n⚠️  No PRs were successfully closed")
    else:
        print(f"\n🔍 Would have closed {closed_count} PR(s)")

    return closed_count


if __name__ == "__main__":
    closed = main()
    sys.exit(0)