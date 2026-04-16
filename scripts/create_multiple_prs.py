#!/usr/bin/env python3
"""
Create multiple pull requests for manual bulk contribution runs.

Usage:
    python scripts/create_multiple_prs.py [count]

Default:
    Uses BULK_COUNT if set, otherwise 20 pull request attempts
"""

import os
import sys
import requests
from datetime import datetime


def get_github_token():
    """Get GitHub token from environment."""
    token = os.environ.get('GH_TOKEN3') or os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if token and not os.environ.get('GH_TOKEN3'):
        print("⚠️ Warning: Using fallback GitHub token. Set GH_TOKEN3 to a personal access token so contributions count on your GitHub profile.")
    if not token:
        print("❌ Error: No GitHub token found.")
        sys.exit(1)
    return token


def get_repo_info():
    """Get repository info."""
    repo = os.environ.get('GITHUB_REPOSITORY', 'ramincsy/Auto')
    owner, repo_name = repo.split('/', 1)
    return owner, repo_name


def get_bulk_count():
    """Return the requested PR count."""
    raw_value = sys.argv[1] if len(sys.argv) > 1 else os.getenv("BULK_COUNT", "20")
    try:
        count = int(raw_value)
    except ValueError:
        count = 20

    return max(1, min(count, 100))


def get_date_string():
    """Get current date.

    Includes hour/minute/second if available for unique branch and file names.
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


def create_pr_for_contribution(owner, repo, token, date_str, index):
    """
    Create a PR for a specific contribution.
    
    Args:
        owner: Repository owner
        repo: Repository name
        token: GitHub token
        date_str: Date string (YYYY-MM-DD)
        index: Contribution index (0-4)
        
    Returns:
        PR number if successful, None otherwise
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Create unique branch name for each contribution
    branch_name = f"contribution-{date_str}-{index}"
    
    # Build expected contribution file path for the PR description
    date_parts = date_str.split('-')
    hour = date_parts[3] if len(date_parts) > 3 else None
    minute = date_parts[4] if len(date_parts) > 4 else None
    second = date_parts[5] if len(date_parts) > 5 else None
    contribution_file = f"{date_parts[2]}-contribution-{index}.md"
    if hour:
        contribution_file = f"{date_parts[2]}-{hour}"
        if minute:
            contribution_file += f"-{minute}"
        if second:
            contribution_file += f"-{second}"
        contribution_file += f"-contribution-{index}.md"

    # PR details
    title = f"Contribution #{index} - {date_str}"
    body = f"""# Contribution #{index} - {date_str}

## Summary
- Add one generated contribution file
- File: updates/{date_parts[0]}/{date_parts[1]}/{contribution_file}

## Context
This PR was created by the manual bulk contribution helper.
Review the generated content before merging.

## Activity Details
- Contribution Index: {index}
- Date: {date_str}
- Type: Generated contribution

---
*Created by the manual bulk contribution helper*
"""
    
    data = {
        "title": title,
        "head": branch_name,
        "base": "main",
        "body": body,
        "draft": False
    }
    
    try:
        # Check if branch exists first
        branch_url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch_name}"
        branch_response = requests.get(branch_url, headers=headers, timeout=10)
        
        if branch_response.status_code != 200:
            print(f"  ⏭️  Branch '{branch_name}' does not exist (skipped)")
            return None
        
        # Create PR
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 201:
            pr_data = response.json()
            pr_number = pr_data['number']
            print(f"  ✅ Created PR #{pr_number} for contribution #{index}")
            return pr_number
        elif response.status_code == 422:
            # PR likely already exists
            print(f"  ⏭️  PR already exists for contribution #{index}")
            return None
        else:
            print(f"  ❌ Error creating PR: {response.status_code}")
            print(f"     {response.text[:100]}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return None


def main():
    """Main function."""
    token = get_github_token()
    owner, repo = get_repo_info()
    date_str = get_date_string()
    count = get_bulk_count()
    
    print(f"Creating {count} PR attempt(s) for {date_str}...")
    
    created_prs = []
    for i in range(count):
        pr_num = create_pr_for_contribution(owner, repo, token, date_str, i)
        if pr_num:
            created_prs.append(pr_num)
    
    if created_prs:
        print(f"\n✨ Created {len(created_prs)} PRs: {created_prs}")
    else:
        print("\n⚠️  No PRs were created (branches may not exist yet)")


if __name__ == "__main__":
    main()
    sys.exit(0)  # Always exit successfully
