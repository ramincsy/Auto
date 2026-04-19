#!/usr/bin/env python3
"""
Add transparent automated reviews to generated contribution PRs.

Usage:
    python scripts/review_contributions.py [--approve]

By default this script leaves a comment-style review.
Use --approve only when you explicitly want an approval review event.
"""

import os
import sys
import requests
from datetime import datetime


def get_github_token():
    """Get GitHub token from environment."""
    token = (
        os.environ.get("GH_TOKEN3")
        or os.environ.get("GITHUB_TOKEN")
        or os.environ.get("GH_TOKEN")
    )
    if token and not os.environ.get("GH_TOKEN3"):
        print(
            "⚠️ Warning: Using fallback GitHub token. Set GH_TOKEN3 to a personal access token so reviews and PR creation count on your GitHub profile."
        )
    if not token:
        print("❌ Error: No GitHub token found.")
        sys.exit(1)
    return token


def get_repo_info():
    """Get repository info."""
    repo = os.environ.get("GITHUB_REPOSITORY", "ramincsy/Auto")
    owner, repo_name = repo.split("/", 1)
    return owner, repo_name


def should_approve():
    """Return whether the review should be submitted as an approval."""
    if "--approve" in sys.argv:
        return True

    value = os.environ.get("AUTO_APPROVE_CONTRIBUTIONS", "false").strip().lower()
    return value in {"1", "true", "yes"}


def get_date_string():
    """Get current date.

    Uses hour/minute/second if available so same-day review runs match branch/PR naming.
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


def get_contribution_prs(owner, repo, token, date_str):
    """Get all contribution PRs for today."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    params = {"state": "open", "per_page": 100}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code != 200:
            print(f"❌ Error fetching PRs: {response.status_code}")
            return []

        all_prs = response.json()

        # Filter for contribution PRs from today
        contribution_prs = []
        for pr in all_prs:
            title = pr.get("title", "")
            if "Contribution #" in title and date_str in title:
                contribution_prs.append(pr)

        return contribution_prs
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def submit_review(owner, repo, token, pr_number, approve=False):
    """Submit a transparent automated review."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    event = "APPROVE" if approve else "COMMENT"
    data = {
        "event": event,
        "body": """Automated maintenance review.

---
This review was created by the repository's bulk contribution helper.
It confirms that the PR matches the generated contribution workflow pattern.
It does not replace a human review of correctness, safety, or content quality.
""",
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            action = "approved" if approve else "reviewed"
            print(f"    ✅ PR #{pr_number} {action} with an automated note")
            return True
        elif response.status_code == 422:
            print(f"    ⏭️  PR #{pr_number} review already exists or is not allowed")
            return False
        else:
            print(f"    ❌ Error submitting review (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"    ❌ Error: {str(e)}")
        return False


def main():
    """Main function."""
    token = get_github_token()
    owner, repo = get_repo_info()
    date_str = get_date_string()
    approve = should_approve()

    mode = "approval" if approve else "comment"
    print(f"Reviewing contribution PRs for {date_str} using {mode} mode...\n")

    # Get contribution PRs
    prs = get_contribution_prs(owner, repo, token, date_str)

    if not prs:
        print(f"⚠️  No contribution PRs found for {date_str}")
        return 0

    print(f"Found {len(prs)} contribution PR(s) to review:\n")

    reviewed_count = 0

    # Review and approve each PR
    for pr in prs:
        pr_number = pr["number"]
        pr_title = pr["title"]
        print(f"  Reviewing PR #{pr_number}: {pr_title}")

        if submit_review(owner, repo, token, pr_number, approve=approve):
            reviewed_count += 1

    if reviewed_count > 0:
        print(f"\n✨ Successfully reviewed and approved {reviewed_count} PR(s)!")
    else:
        print("\n⚠️  No PRs were successfully reviewed")

    return reviewed_count


if __name__ == "__main__":
    reviewed = main()
    sys.exit(0)  # Always exit successfully
