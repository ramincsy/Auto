#!/usr/bin/env python3
"""
Close all open pull requests in the configured repository.
"""

import os
import sys

import requests


def get_github_token():
    """Get GitHub token from environment variables."""
    token = os.environ.get("GH_TOKEN3") or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("Error: No GitHub token found.")
        print("Please set GH_TOKEN3, GITHUB_TOKEN, or GH_TOKEN environment variable.")
        print("\nExample:")
        print("  export GH_TOKEN3='your_token_here'")
        print("  python scripts/close_all_prs.py")
        sys.exit(1)
    return token


def get_open_prs(owner, repo, token):
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
        except requests.exceptions.RequestException as exc:
            print(f"Network error fetching PRs: {exc}")
            sys.exit(1)

        if response.status_code != 200:
            print(f"Error fetching PRs: {response.status_code}")
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


def close_pr(owner, repo, pr_number, token):
    """Close a specific pull request."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"state": "closed"}

    try:
        response = requests.patch(url, headers=headers, json=data, timeout=30)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def main():
    """Main function to close all open pull requests."""
    repository = os.environ.get("GITHUB_REPOSITORY", "ramincsy/Auto")
    owner, repo = repository.split("/", 1)

    token = get_github_token()
    open_prs = get_open_prs(owner, repo, token)

    if not open_prs:
        print("No open pull requests found.")
        return

    print(f"Found {len(open_prs)} open pull request(s) in {owner}/{repo}:")
    for pr in open_prs:
        print(f"  - PR #{pr['number']}: {pr['title']}")

    print("\nWARNING: This will close ALL open pull requests.")
    print("Are you sure you want to continue? (yes/no): ", end="")
    confirmation = input().strip().lower()
    if confirmation != "yes":
        print("Operation cancelled.")
        sys.exit(0)

    closed_count = 0
    failed_count = 0
    for pr in open_prs:
        pr_number = pr["number"]
        print(f"Closing PR #{pr_number}...", end=" ")
        if close_pr(owner, repo, pr_number, token):
            print("OK")
            closed_count += 1
        else:
            print("FAILED")
            failed_count += 1

    print("\nSummary:")
    print(f"  Closed: {closed_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total: {len(open_prs)}")


if __name__ == "__main__":
    main()
