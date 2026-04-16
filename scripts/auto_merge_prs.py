#!/usr/bin/env python3
"""
Auto-merge daily pull requests in a conflict-aware order.
"""

import os
import sys
import time
from datetime import datetime, timezone
from typing import Dict, List

import requests


def get_github_token() -> str:
    token = os.environ.get("GH_TOKEN3") or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and not os.environ.get("GH_TOKEN3"):
        print("⚠️ Warning: Using fallback GitHub token. Set GH_TOKEN3 to a personal access token for deterministic workflow behavior.")
    if not token:
        print("Error: No GitHub token found.")
        sys.exit(1)
    return token


def get_repo_info() -> tuple[str, str]:
    repo = os.environ.get("GITHUB_REPOSITORY", "ramincsy/Auto")
    if "/" not in repo:
        print("Error: Invalid GITHUB_REPOSITORY format.")
        sys.exit(1)
    return tuple(repo.split("/", 1))


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
    return any(marker in title for marker in ["Daily Update", "daily-contribution", "Contribution #", "Contribution "])


def pr_sort_key(pr: Dict) -> datetime:
    created_at = pr.get("created_at")
    if not created_at:
        return datetime.max.replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(created_at.replace("Z", "+00:00"))


def check_pr_details(owner: str, repo: str, pr_number: int, token: str) -> Dict:
    try:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}",
            headers=get_headers(token),
            timeout=30,
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "mergeable": data.get("mergeable"),
                "mergeable_state": data.get("mergeable_state"),
                "draft": data.get("draft", False),
            }
    except requests.exceptions.RequestException as exc:
        print(f"Network error checking PR #{pr_number}: {exc}")
    return {"mergeable": False, "mergeable_state": "unknown", "draft": False}


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
        print(f"    Network error updating branch: {exc}")
        return False

    if response.status_code in {200, 202}:
        return True

    print(f"    update-branch failed: {response.status_code}")
    return False


def merge_pr(owner: str, repo: str, pr_number: int, token: str) -> bool:
    try:
        response = requests.put(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge",
            headers=get_headers(token),
            json={"merge_method": "merge"},
            timeout=30,
        )
    except requests.exceptions.RequestException as exc:
        print(f"    Network error merging PR #{pr_number}: {exc}")
        return False

    if response.status_code == 200:
        return True

    print(f"    merge failed: {response.status_code}")
    return False


def wait_for_mergeable(owner: str, repo: str, pr_number: int, token: str, retries: int = 4, delay: int = 5) -> Dict:
    details = check_pr_details(owner, repo, pr_number, token)
    attempts = 0
    while attempts < retries and details["mergeable"] is None:
        attempts += 1
        print(f"  Waiting for PR #{pr_number} mergeability ({attempts}/{retries})...")
        time.sleep(delay)
        details = check_pr_details(owner, repo, pr_number, token)
    return details


def wait_after_update(owner: str, repo: str, pr_number: int, token: str) -> Dict:
    details = {"mergeable": False, "mergeable_state": "unknown", "draft": False}
    for attempt in range(1, 5):
        print(f"  Rechecking PR #{pr_number} after branch update ({attempt}/4)...")
        time.sleep(10)
        details = wait_for_mergeable(owner, repo, pr_number, token, retries=2, delay=3)
        if details.get("mergeable") is True or details.get("mergeable_state") == "clean":
            break
    return details


def main() -> None:
    print("Starting auto-merge process...")

    token = get_github_token()
    owner, repo = get_repo_info()
    open_prs = get_open_prs(owner, repo, token)
    daily_prs = sorted((pr for pr in open_prs if is_daily_pr(pr)), key=pr_sort_key)

    if not daily_prs:
        print("No daily contribution PRs to merge.")
        return

    print(f"Found {len(daily_prs)} daily contribution PR(s).")

    merged_count = 0
    failed_count = 0
    conflict_count = 0

    for pr in daily_prs:
        pr_number = pr["number"]
        print(f"Checking PR #{pr_number}: {pr['title']}")

        details = wait_for_mergeable(owner, repo, pr_number, token)
        if details.get("draft"):
            print(f"  PR #{pr_number} is a draft. Skipping.")
            continue

        mergeable = details.get("mergeable")
        mergeable_state = details.get("mergeable_state")

        if mergeable_state in {"dirty", "behind"} or mergeable is False:
            print(f"  PR #{pr_number} needs branch update (state: {mergeable_state})")
            if update_pr_branch(owner, repo, pr_number, token):
                details = wait_after_update(owner, repo, pr_number, token)
                mergeable = details.get("mergeable")
                mergeable_state = details.get("mergeable_state")
            else:
                failed_count += 1
                if mergeable_state == "dirty":
                    conflict_count += 1
                continue

        if mergeable is None:
            print(f"  PR #{pr_number} is still being computed.")
            failed_count += 1
            continue

        if not mergeable:
            print(f"  PR #{pr_number} is not mergeable after retry (state: {mergeable_state})")
            failed_count += 1
            if mergeable_state == "dirty":
                conflict_count += 1
            continue

        print(f"  Merging PR #{pr_number}...")
        if merge_pr(owner, repo, pr_number, token):
            print(f"  Successfully merged PR #{pr_number}")
            merged_count += 1
        else:
            print(f"  Failed to merge PR #{pr_number}")
            failed_count += 1

    print("\nAuto-merge Summary:")
    print(f"  Merged: {merged_count}")
    print(f"  Conflicts remaining: {conflict_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total: {len(daily_prs)}")


if __name__ == "__main__":
    main()
