#!/usr/bin/env python3
"""
Review and Merge Pull Requests for GitHub Achievements

This script helps review daily contribution PRs and provides recommendations
for merging them to achieve GitHub achievements.

Usage:
    python scripts/review_and_merge_prs.py [--auto-merge]

Environment Variables:
    GITHUB_TOKEN or GH_TOKEN: GitHub personal access token with 'repo' scope

Features:
    - Lists all daily contribution PRs
    - Checks PR quality (files changed, conflicts, etc.)
    - Provides merge recommendations
    - Optionally auto-merges PRs (with --auto-merge flag)
    - Tracks progress towards GitHub achievements
"""

import os
import sys
import requests
from typing import List, Dict, Optional


def get_github_token() -> str:
    """Get GitHub token from environment variables."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("❌ Error: No GitHub token found.")
        print("Please set GITHUB_TOKEN or GH_TOKEN environment variable.")
        print("\nExample:")
        print("  export GITHUB_TOKEN='your_token_here'")
        print("  python scripts/review_and_merge_prs.py")
        sys.exit(1)
    return token


def get_open_prs(owner: str, repo: str, token: str) -> List[Dict]:
    """Fetch all open pull requests."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    params = {"state": "open", "per_page": 100}

    all_prs = []
    page = 1

    while True:
        params["page"] = page

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error fetching PRs: {e}")
            sys.exit(1)

        if response.status_code != 200:
            print(f"❌ Error fetching PRs: {response.status_code}")
            try:
                print(response.json())
            except ValueError:
                print(response.text)
            sys.exit(1)

        prs = response.json()
        if not prs:
            break

        all_prs.extend(prs)
        page += 1

        if len(prs) < 100:
            break

    return all_prs


def get_pr_files(owner: str, repo: str, pr_number: int, token: str) -> List[Dict]:
    """Get files changed in a PR."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass

    return []


def check_pr_mergeable(
    owner: str, repo: str, pr_number: int, token: str
) -> Optional[bool]:
    """Check if PR is mergeable (no conflicts)."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get("mergeable")
    except requests.exceptions.RequestException:
        pass

    return None


def merge_pr(
    owner: str, repo: str, pr_number: int, token: str, merge_method: str = "merge"
) -> tuple[bool, str]:
    """Merge a pull request. Returns (success, message)."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"merge_method": merge_method}  # "merge", "squash", or "rebase"

    try:
        response = requests.put(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return True, "Success"
        else:
            error_msg = (
                response.json().get("message", "Unknown error")
                if response.text
                else "Unknown error"
            )
            return False, f"Error {response.status_code}: {error_msg}"
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"


def analyze_pr(pr: Dict, owner: str, repo: str, token: str) -> Dict:
    """Analyze a PR and provide recommendations."""
    pr_number = pr["number"]

    # Get files changed
    files = get_pr_files(owner, repo, pr_number, token)

    # Check if mergeable
    mergeable = check_pr_mergeable(owner, repo, pr_number, token)

    # Analyze PR
    analysis = {
        "number": pr_number,
        "title": pr["title"],
        "created_at": pr["created_at"],
        "user": pr["user"]["login"],
        "files_count": len(files),
        "files": [f["filename"] for f in files],
        "mergeable": mergeable,
        "is_daily_update": "Daily Update" in pr["title"]
        or "daily-contribution" in pr["title"],
        "recommendation": "unknown",
    }

    # Provide recommendation
    if analysis["is_daily_update"]:
        if mergeable is True:
            analysis["recommendation"] = "ready_to_merge"
        elif mergeable is False:
            analysis["recommendation"] = "has_conflicts"
        else:
            # mergeable is None - GitHub is still computing merge status
            analysis["recommendation"] = "checking"
    else:
        analysis["recommendation"] = "review_manually"

    return analysis


def display_pr_analysis(analyses: List[Dict]) -> None:
    """Display PR analysis in a user-friendly format."""
    print("\n" + "=" * 80)
    print("📊 PULL REQUEST ANALYSIS")
    print("=" * 80 + "\n")

    # Group by recommendation
    ready_to_merge = [a for a in analyses if a["recommendation"] == "ready_to_merge"]
    has_conflicts = [a for a in analyses if a["recommendation"] == "has_conflicts"]
    checking = [a for a in analyses if a["recommendation"] == "checking"]
    review_manually = [a for a in analyses if a["recommendation"] == "review_manually"]

    print(f"✅ Ready to Merge: {len(ready_to_merge)}")
    print(f"⚠️  Has Conflicts: {len(has_conflicts)}")
    print(f"🔄 Still Checking: {len(checking)}")
    print(f"👀 Review Manually: {len(review_manually)}")
    print()

    if ready_to_merge:
        print("\n✅ READY TO MERGE:")
        print("-" * 80)
        for pr in ready_to_merge:
            print(f"  #{pr['number']}: {pr['title']}")
            print(
                f"    Files: {', '.join(pr['files'][:3])}{'...' if len(pr['files']) > 3 else ''}"
            )
            print(f"    Created: {pr['created_at'][:10]}")
            print()

    if has_conflicts:
        print("\n⚠️  HAS CONFLICTS:")
        print("-" * 80)
        for pr in has_conflicts:
            print(f"  #{pr['number']}: {pr['title']}")
            print("    Action needed: Resolve conflicts manually")
            print()

    if review_manually:
        print("\n👀 REVIEW MANUALLY:")
        print("-" * 80)
        for pr in review_manually:
            print(f"  #{pr['number']}: {pr['title']}")
            print("    Note: Not a daily update PR")
            print()


def show_achievement_progress(merged_count: int) -> None:
    """Show progress towards GitHub achievements."""
    print("\n" + "=" * 80)
    print("🎯 GITHUB ACHIEVEMENTS PROGRESS")
    print("=" * 80 + "\n")

    achievements = [
        {
            "name": "Pull Shark",
            "emoji": "🦈",
            "requirement": "Merge 4+ PRs",
            "progress": min(merged_count, 4),
            "total": 4,
            "achieved": merged_count >= 4,
        },
        {
            "name": "Quickdraw",
            "emoji": "⚡",
            "requirement": "Merge PR within 30 minutes",
            "note": "Merge a PR quickly after creation",
            "achieved": None,
        },
        {
            "name": "YOLO",
            "emoji": "🎉",
            "requirement": "Merge without review",
            "note": "Merge a PR without requesting review",
            "achieved": None,
        },
    ]

    for achievement in achievements:
        status = "✅ " if achievement.get("achieved") else "⏳ "
        print(f"{status}{achievement['emoji']} {achievement['name']}")
        print(f"   Requirement: {achievement['requirement']}")
        if "progress" in achievement:
            progress_bar = "█" * achievement["progress"] + "░" * (
                achievement["total"] - achievement["progress"]
            )
            print(
                f"   Progress: [{progress_bar}] {achievement['progress']}/{achievement['total']}"
            )
        if "note" in achievement:
            print(f"   Note: {achievement['note']}")
        print()


def main():
    """Main function."""
    # Parse arguments
    auto_merge = "--auto-merge" in sys.argv

    # Repository information - can be overridden with env vars
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "ramincsy")
    repo = os.environ.get("GITHUB_REPOSITORY_NAME", "Auto")

    print("🔍 Fetching GitHub token...")
    token = get_github_token()

    print(f"📋 Fetching open pull requests for {owner}/{repo}...")
    open_prs = get_open_prs(owner, repo, token)

    if not open_prs:
        print("✅ No open pull requests found.")
        return

    print(f"\n🔍 Analyzing {len(open_prs)} pull request(s)...")

    # Analyze each PR
    analyses = []
    for pr in open_prs:
        print(f"  Analyzing PR #{pr['number']}...", end=" ")
        analysis = analyze_pr(pr, owner, repo, token)
        analyses.append(analysis)
        print("✅")

    # Display analysis
    display_pr_analysis(analyses)

    # Auto-merge if requested
    if auto_merge:
        ready_to_merge = [
            a for a in analyses if a["recommendation"] == "ready_to_merge"
        ]

        if not ready_to_merge:
            print("\n⚠️  No PRs ready to merge.")
            return

        print(f"\n⚠️  WARNING: This will merge {len(ready_to_merge)} pull request(s)!")
        print("Are you sure you want to continue? (yes/no): ", end="")

        confirmation = input().strip().lower()
        if confirmation != "yes":
            print("❌ Operation cancelled.")
            return

        print("\n🔄 Merging pull requests...")
        merged_count = 0
        failed_count = 0

        for pr in ready_to_merge:
            pr_number = pr["number"]
            print(f"  Merging PR #{pr_number}...", end=" ")

            success, message = merge_pr(owner, repo, pr_number, token)
            if success:
                print("✅")
                merged_count += 1
            else:
                print(f"❌ ({message})")
                failed_count += 1

        print("\n📊 Merge Summary:")
        print(f"  ✅ Merged: {merged_count}")
        print(f"  ❌ Failed: {failed_count}")
        print(f"  📋 Total: {len(ready_to_merge)}")

        if failed_count == 0:
            print("\n✨ All pull requests merged successfully!")
        else:
            print(f"\n⚠️  {failed_count} pull request(s) failed to merge.")

        # Show achievement progress
        show_achievement_progress(merged_count)
    else:
        print("\n💡 To automatically merge ready PRs, run:")
        print("   python scripts/review_and_merge_prs.py --auto-merge")
        print()
        print("💡 Or merge them manually via GitHub UI:")
        print(f"   https://github.com/{owner}/{repo}/pulls")


if __name__ == "__main__":
    main()
