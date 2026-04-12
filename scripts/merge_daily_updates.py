#!/usr/bin/env python3
"""
Legacy helper to merge open daily contribution PRs.

Prefer scripts/auto_merge_prs.py for the active merge flow.
"""

import os
import sys
import requests
from typing import List, Dict, Any

# GitHub API base URL
GITHUB_API_BASE = "https://api.github.com"

def get_github_token() -> str:
    """Get GitHub token from environment variable."""
    token = os.getenv("GH_TOKEN3") or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        print("Error: GH_TOKEN3, GITHUB_TOKEN, or GH_TOKEN environment variable not set")
        sys.exit(1)
    return token


def get_repo_info() -> tuple[str, str]:
    """Return repository owner/name from environment or defaults."""
    repo_full_name = os.getenv("GITHUB_REPOSITORY", "ramincsy/Auto")
    owner, repo = repo_full_name.split("/", 1)
    return owner, repo

def get_headers(token: str) -> Dict[str, str]:
    """Get headers for GitHub API requests."""
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

def get_open_prs(owner: str, repo: str, token: str) -> List[Dict[str, Any]]:
    """Get all open pull requests."""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls"
    params = {"state": "open", "per_page": 100}  # Assuming not too many PRs
    response = requests.get(url, headers=get_headers(token), params=params, timeout=30)
    
    if response.status_code != 200:
        print(f"Error fetching PRs: {response.status_code} - {response.text}")
        return []
    
    return response.json()

def is_daily_update_pr(pr: Dict[str, Any]) -> bool:
    """Check if PR title contains 'Daily Update'."""
    return "Daily Update" in pr.get("title", "")

def check_pr_mergeable(owner: str, repo: str, token: str, pr_number: int) -> bool:
    """Check if a PR is mergeable."""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=get_headers(token), timeout=30)
    
    if response.status_code != 200:
        print(f"Error checking PR {pr_number}: {response.status_code} - {response.text}")
        return False
    
    pr_data = response.json()
    return pr_data.get("mergeable", False)

def merge_pr(owner: str, repo: str, token: str, pr_number: int, pr_title: str) -> bool:
    """Merge a pull request."""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}/merge"
    data = {
        "merge_method": "merge"  # or "squash", "rebase"
    }
    response = requests.put(url, headers=get_headers(token), json=data, timeout=30)
    
    if response.status_code == 200:
        print(f"Successfully merged PR #{pr_number}: {pr_title}")
        return True
    else:
        print(f"Failed to merge PR #{pr_number}: {response.status_code} - {response.text}")
        return False

def main():
    """Main function to merge daily update PRs."""
    token = get_github_token()
    owner, repo = get_repo_info()
    
    print("Fetching open pull requests...")
    open_prs = get_open_prs(owner, repo, token)
    
    if not open_prs:
        print("No open pull requests found.")
        return
    
    # Filter daily update PRs
    daily_prs = [pr for pr in open_prs if is_daily_update_pr(pr)]
    
    if not daily_prs:
        print("No daily update PRs found.")
        return
    
    print(f"Found {len(daily_prs)} daily update PR(s).")
    
    merged_count = 0
    failed_count = 0
    
    for pr in daily_prs:
        pr_number = pr["number"]
        pr_title = pr["title"]
        
        print(f"Checking PR #{pr_number}: {pr_title}")
        
        if check_pr_mergeable(owner, repo, token, pr_number):
            if merge_pr(owner, repo, token, pr_number, pr_title):
                merged_count += 1
            else:
                failed_count += 1
        else:
            print(f"PR #{pr_number} is not mergeable.")
            failed_count += 1
    
    print("\nSummary:")
    print(f"Total daily update PRs: {len(daily_prs)}")
    print(f"Successfully merged: {merged_count}")
    print(f"Failed or not mergeable: {failed_count}")

if __name__ == "__main__":
    main()
