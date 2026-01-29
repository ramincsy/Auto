#!/usr/bin/env python3
"""
Close All Open Pull Requests

This script closes all open pull requests in the repository.
Requires a GitHub token with appropriate permissions.

Usage:
    python scripts/close_all_prs.py

Environment Variables:
    GITHUB_TOKEN or GH_TOKEN2: GitHub personal access token with 'repo' scope
"""

import os
import sys
import requests


def get_github_token():
    """Get GitHub token from environment variables."""
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN2')
    if not token:
        print("❌ Error: No GitHub token found.")
        print("Please set GITHUB_TOKEN or GH_TOKEN2 environment variable.")
        print("\nExample:")
        print("  export GITHUB_TOKEN='your_token_here'")
        print("  python scripts/close_all_prs.py")
        sys.exit(1)
    return token


def get_open_prs(owner, repo, token):
    """Fetch all open pull requests."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "state": "open",
        "per_page": 100
    }
    
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
        
        # GitHub API pagination limit
        if len(prs) < 100:
            break
    
    return all_prs


def close_pr(owner, repo, pr_number, token):
    """Close a specific pull request."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "state": "closed"
    }
    
    try:
        response = requests.patch(url, headers=headers, json=data, timeout=30)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def main():
    """Main function to close all open pull requests."""
    # Repository information
    owner = "ramincsy"
    repo = "Auto"
    
    print("🔍 Fetching GitHub token...")
    token = get_github_token()
    
    print(f"📋 Fetching open pull requests for {owner}/{repo}...")
    open_prs = get_open_prs(owner, repo, token)
    
    if not open_prs:
        print("✅ No open pull requests found.")
        return
    
    print(f"\n📊 Found {len(open_prs)} open pull request(s):")
    for pr in open_prs:
        print(f"  - PR #{pr['number']}: {pr['title']}")
    
    print("\n⚠️  WARNING: This will close ALL open pull requests!")
    print("Are you sure you want to continue? (yes/no): ", end="")
    
    confirmation = input().strip().lower()
    if confirmation != "yes":
        print("❌ Operation cancelled.")
        sys.exit(0)
    
    print("\n🔄 Closing pull requests...")
    closed_count = 0
    failed_count = 0
    
    for pr in open_prs:
        pr_number = pr['number']
        print(f"  Closing PR #{pr_number}...", end=" ")
        
        if close_pr(owner, repo, pr_number, token):
            print("✅")
            closed_count += 1
        else:
            print("❌")
            failed_count += 1
    
    print(f"\n📊 Summary:")
    print(f"  ✅ Closed: {closed_count}")
    print(f"  ❌ Failed: {failed_count}")
    print(f"  📋 Total: {len(open_prs)}")
    
    if failed_count == 0:
        print("\n✨ All pull requests closed successfully!")
    else:
        print(f"\n⚠️  {failed_count} pull request(s) failed to close.")


if __name__ == "__main__":
    main()
