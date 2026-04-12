#!/usr/bin/env python3
"""
Resolve conflicts in daily contribution PRs.
"""

import os
import sys
import time
from datetime import datetime, timezone
from typing import Dict, List

import requests


def get_github_token() -> str:
    token = os.environ.get("GH_TOKEN3") or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("Error: No GitHub token found.")
        sys.exit(1)
    return token


def get_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }


def get_open_prs(owner: str, repo: str, token: str) -> List[Dict]:
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls",
        headers=get_headers(token),
        params={"state": "open", "per_page": 100},
        timeout=30,
    )
    if response.status_code != 200:
        print(f"Error fetching PRs: {response.status_code}")
        sys.exit(1)
    return response.json()


def is_daily_pr(pr: Dict) -> bool:
    title = pr.get("title", "")
    return "Daily Update" in title or "daily-contribution" in title


def pr_sort_key(pr: Dict) -> datetime:
    created_at = pr.get("created_at")
    if not created_at:
        return datetime.max.replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(created_at.replace("Z", "+00:00"))


def get_pr_details(owner: str, repo: str, pr_number: int, token: str) -> Dict:
    try:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}",
            headers=get_headers(token),
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    return {}


def update_pr_branch(owner: str, repo: str, pr_number: int, token: str) -> bool:
    headers = get_headers(token)
    headers["Accept"] = "application/vnd.github.z3950-preview+json"
    try:
        response = requests.post(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/update-branch",
            headers=headers,
            timeout=30,
        )
    except requests.exceptions.RequestException as exc:
        print(f"  Error updating branch: {exc}")
        return False

    if response.status_code in {200, 202}:
        print(f"  Update request sent (status: {response.status_code})")
        return True

    print(f"  Update failed: {response.status_code}")
    return False


def merge_pr(owner: str, repo: str, pr_number: int, token: str, merge_method: str = "squash") -> bool:
    try:
        response = requests.put(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge",
            headers=get_headers(token),
            json={"merge_method": merge_method},
            timeout=30,
        )
    except requests.exceptions.RequestException as exc:
        print(f"    Error merging PR #{pr_number}: {exc}")
        return False

    if response.status_code == 200:
        return True

    print(f"    Merge failed: {response.status_code}")
    return False


def analyze_conflicts(owner: str, repo: str, token: str) -> Dict:
    print("Analyzing pull requests for conflicts...\n")

    prs = get_open_prs(owner, repo, token)
    daily_prs = sorted((pr for pr in prs if is_daily_pr(pr)), key=pr_sort_key)

    if not daily_prs:
        print("No daily contribution PRs found.")
        return {"conflicted": [], "ready": [], "checking": [], "total": 0}

    conflicted: List[Dict] = []
    ready: List[Dict] = []
    checking: List[Dict] = []

    for pr in daily_prs:
        details = get_pr_details(owner, repo, pr["number"], token)
        mergeable = details.get("mergeable")
        mergeable_state = details.get("mergeable_state", "unknown")

        pr_info = {
            "number": pr["number"],
            "title": pr["title"],
            "created_at": pr["created_at"],
            "mergeable": mergeable,
            "mergeable_state": mergeable_state,
            "head_ref": details.get("head", {}).get("ref", "unknown"),
        }

        if mergeable_state in {"dirty", "behind"}:
            conflicted.append(pr_info)
            print(f"PR #{pr['number']}: {pr['title'][:50]}...")
            print(f"  State: {mergeable_state}")
            print(f"  Created: {pr['created_at'][:10]}")
            print()
        elif mergeable is True and mergeable_state == "clean":
            ready.append(pr_info)
            print(f"PR #{pr['number']}: {pr['title'][:50]}...")
            print("  State: clean")
            print()
        else:
            checking.append(pr_info)
            print(f"PR #{pr['number']}: {pr['title'][:50]}...")
            print(f"  State: {mergeable_state}")
            print()

    print("\nSummary:")
    print(f"  Needs update/conflict work: {len(conflicted)}")
    print(f"  Ready to merge: {len(ready)}")
    print(f"  Still checking: {len(checking)}")

    return {
        "conflicted": conflicted,
        "ready": ready,
        "checking": checking,
        "total": len(daily_prs),
    }


def auto_resolve_conflicts(owner: str, repo: str, conflicted_prs: List[Dict], token: str, force_merge: bool = False) -> Dict:
    print("\nAttempting to resolve conflicts...\n")

    resolved = 0
    merged = 0
    failed = 0

    for pr in conflicted_prs:
        pr_number = pr["number"]
        print(f"Processing PR #{pr_number}: {pr['title'][:50]}...")
        print("  Updating branch from main...")

        if update_pr_branch(owner, repo, pr_number, token):
            print("  Waiting for GitHub to process the update...")
            time.sleep(20)
            details = get_pr_details(owner, repo, pr_number, token)
            mergeable = details.get("mergeable")
            mergeable_state = details.get("mergeable_state", "unknown")
            print(f"  New state: {mergeable_state}")

            if mergeable is True or mergeable_state == "clean":
                resolved += 1
                print("  Branch is mergeable now. Merging...")
                if merge_pr(owner, repo, pr_number, token, merge_method="merge"):
                    merged += 1
                    print(f"  Successfully merged PR #{pr_number}")
                else:
                    failed += 1
            elif force_merge:
                print("  Still not clean. Trying squash merge...")
                if merge_pr(owner, repo, pr_number, token, merge_method="squash"):
                    merged += 1
                    print(f"  Successfully squash-merged PR #{pr_number}")
                else:
                    failed += 1
            else:
                failed += 1
        else:
            failed += 1

        print()

    return {"resolved": resolved, "merged": merged, "failed": failed}


def print_manual_resolution_guide(conflicted_prs: List[Dict], owner: str, repo: str) -> None:
    if not conflicted_prs:
        return

    print("\nManual conflict resolution guide:\n")
    for pr in conflicted_prs:
        head_ref = pr.get("head_ref", "unknown")
        print(f"PR #{pr['number']} ({head_ref})")
        print("  git fetch origin")
        print(f"  git checkout {head_ref}")
        print("  git rebase origin/main")
        print("  git add .")
        print("  git rebase --continue")
        print(f"  git push -f origin {head_ref}")
        print()

    print(f"View PRs: https://github.com/{owner}/{repo}/pulls")


def main() -> None:
    auto_resolve = "--auto-resolve" in sys.argv
    force_merge = "--force-merge" in sys.argv

    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "ramincsy")
    repo = os.environ.get("GITHUB_REPOSITORY_NAME", "Auto")
    token = get_github_token()

    analysis = analyze_conflicts(owner, repo, token)

    if not analysis["conflicted"]:
        print("\nNo conflicted PRs found.")
        if analysis["ready"]:
            print(f"There are {len(analysis['ready'])} ready-to-merge PRs.")
        return

    if auto_resolve or force_merge:
        results = auto_resolve_conflicts(
            owner,
            repo,
            analysis["conflicted"],
            token,
            force_merge=force_merge,
        )
        print("\nResolution results:")
        print(f"  Resolved and merged: {results['merged']}")
        print(f"  Failed: {results['failed']}")
        print(f"  Total: {len(analysis['conflicted'])}")

        if results["failed"] > 0:
            print_manual_resolution_guide(analysis["conflicted"], owner, repo)
    else:
        print("\nRun with --auto-resolve to update stale PR branches.")
        print("Run with --force-merge to allow squash merge fallback.")


if __name__ == "__main__":
    main()
