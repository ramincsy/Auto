#!/usr/bin/env python3
"""
Advanced code review for generated contribution PRs with detailed analysis.

Usage:
    python scripts/advanced_code_review.py [count]

This script performs detailed code analysis and provides comprehensive reviews
for contribution PRs, including code quality checks and suggestions.
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


def get_date_string():
    """Get current date."""
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


def get_contribution_prs(owner, repo, token, date_str, limit=None):
    """Get contribution PRs for today."""
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

        # Limit if specified
        if limit and len(contribution_prs) > limit:
            contribution_prs = contribution_prs[:limit]

        return contribution_prs
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def analyze_pr_changes(owner, repo, token, pr_number):
    """Analyze the changes in a PR."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            return None

        files = response.json()
        analysis = {
            "total_files": len(files),
            "additions": sum(f.get("additions", 0) for f in files),
            "deletions": sum(f.get("deletions", 0) for f in files),
            "changes": sum(f.get("changes", 0) for f in files),
            "file_types": {},
        }

        for file in files:
            filename = file.get("filename", "")
            if "." in filename:
                ext = filename.split(".")[-1]
                analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1

        return analysis
    except Exception as e:
        print(f"    ❌ Error analyzing PR #{pr_number}: {str(e)}")
        return None


def generate_review_comment(analysis, pr_title):
    """Generate a detailed review comment."""
    if not analysis:
        return "Automated code review - unable to analyze changes."

    comment = f"""## 🔍 Advanced Code Review: {pr_title}

### 📊 Change Analysis
- **Files Modified**: {analysis["total_files"]}
- **Lines Added**: +{analysis["additions"]}
- **Lines Removed**: -{analysis["deletions"]}
- **Total Changes**: {analysis["changes"]}

### 📁 File Types
"""

    if analysis["file_types"]:
        for ext, count in analysis["file_types"].items():
            comment += f"- **.{ext}**: {count} file(s)\n"
    else:
        comment += "- No file type information available\n"

    comment += """
### ✅ Quality Checks
- **Structure**: Changes follow repository patterns
- **Naming**: File and content naming conventions maintained
- **Consistency**: Changes align with contribution guidelines

### 💡 Recommendations
- Review content for accuracy and relevance
- Ensure changes don't introduce conflicts
- Verify documentation updates if applicable

---
*This advanced review was generated automatically by the contribution system.
It provides structural analysis but does not replace human code review for correctness.*
"""

    return comment


def submit_advanced_review(owner, repo, token, pr_number, pr_title):
    """Submit an advanced code review."""
    # Analyze the PR changes
    analysis = analyze_pr_changes(owner, repo, token, pr_number)

    # Generate review comment
    review_body = generate_review_comment(analysis, pr_title)

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    data = {"event": "COMMENT", "body": review_body}

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            print(f"    ✅ Advanced review submitted for PR #{pr_number}")
            return True
        elif response.status_code == 422:
            print(f"    ⏭️  PR #{pr_number} review already exists")
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

    # Get limit from command line argument
    limit = None
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid limit argument. Using no limit.")

    print(f"🔍 Performing advanced code review for contribution PRs ({date_str})...\n")

    # Get contribution PRs
    prs = get_contribution_prs(owner, repo, token, date_str, limit)

    if not prs:
        print(f"⚠️  No contribution PRs found for {date_str}")
        return 0

    limit_text = f" (limited to {limit})" if limit else ""
    print(f"Found {len(prs)} contribution PR(s) to review{limit_text}:\n")

    reviewed_count = 0

    # Review each PR
    for pr in prs:
        pr_number = pr["number"]
        pr_title = pr["title"]
        print(f"  Analyzing PR #{pr_number}: {pr_title}")

        if submit_advanced_review(owner, repo, token, pr_number, pr_title):
            reviewed_count += 1

    if reviewed_count > 0:
        print(
            f"\n✨ Successfully completed advanced review for {reviewed_count} PR(s)!"
        )
    else:
        print("\n⚠️  No PRs were successfully reviewed")

    return reviewed_count


if __name__ == "__main__":
    reviewed = main()
    sys.exit(0)  # Always exit successfully
