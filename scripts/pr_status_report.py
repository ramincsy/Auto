#!/usr/bin/env python3
"""
PR Merge System Status Report

Shows current health and status of the auto-merge system.
Helps identify issues and provides actionable recommendations.

Usage:
    python scripts/pr_status_report.py
"""

import os
import sys
import requests
from typing import Dict, List
from datetime import datetime, timedelta


def get_github_token() -> str:
    """Get GitHub token from environment variables."""
    token = os.environ.get('GH_TOKEN3') or os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not token:
        print("❌ Error: No GitHub token found.")
        print("Please set GH_TOKEN3, GITHUB_TOKEN, or GH_TOKEN environment variable.")
        sys.exit(1)
    return token


def get_headers(token: str) -> Dict[str, str]:
    """Get headers for GitHub API requests."""
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }


def get_open_prs(owner: str, repo: str, token: str) -> List[Dict]:
    """Fetch all open pull requests."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = get_headers(token)
    params = {"state": "open", "per_page": 100}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass

    return []


def get_repo_info(owner: str, repo: str, token: str) -> Dict:
    """Get repository information."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = get_headers(token)

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return {
                'name': data.get('name'),
                'owner': data.get('owner', {}).get('login'),
                'stars': data.get('stargazers_count'),
                'default_branch': data.get('default_branch'),
                'url': data.get('html_url'),
            }
    except requests.exceptions.RequestException:
        pass

    return {}


def get_closed_prs_last_day(owner: str, repo: str, token: str) -> int:
    """Get count of PRs closed in last 24 hours."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = get_headers(token)
    
    since = (datetime.utcnow() - timedelta(days=1)).isoformat() + 'Z'
    params = {"state": "closed", "per_page": 100, "since": since}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            return len(response.json())
    except requests.exceptions.RequestException:
        pass

    return 0


def get_pr_details(owner: str, repo: str, pr_number: int, token: str) -> Dict:
    """Get detailed PR information."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = get_headers(token)

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            created = datetime.fromisoformat(data.get('created_at', '').replace('Z', '+00:00'))
            age_days = (datetime.now(created.tzinfo) - created).days
            
            return {
                'number': data.get('number'),
                'title': data.get('title'),
                'created_at': data.get('created_at'),
                'age_days': age_days,
                'mergeable': data.get('mergeable'),
                'mergeable_state': data.get('mergeable_state'),
                'draft': data.get('draft'),
                'url': data.get('html_url'),
            }
    except requests.exceptions.RequestException:
        pass

    return {}


def analyze_system_health(owner: str, repo: str, token: str) -> Dict:
    """Analyze overall health of the merge system."""
    prs = get_open_prs(owner, repo, token)
    
    daily_prs = [pr for pr in prs if 'Daily Update' in pr['title'] or 'daily-contribution' in pr['title']]
    
    if not daily_prs:
        return {
            'status': 'OK',
            'message': 'No daily contribution PRs found',
            'details': {}
        }
    
    # Analyze states
    clean = 0
    dirty = 0
    unknown = 0
    draft = 0
    
    oldest_dirty = None
    dirty_count_24h = 0
    
    for pr in daily_prs:
        details = get_pr_details(owner, repo, pr['number'], token)
        
        if details.get('draft'):
            draft += 1
            continue
        
        state = details.get('mergeable_state', 'unknown')
        
        if state == 'clean':
            clean += 1
        elif state == 'dirty':
            dirty += 1
            age = details.get('age_days', 0)
            
            if oldest_dirty is None or age > oldest_dirty['age_days']:
                oldest_dirty = {
                    'number': details.get('number'),
                    'age_days': age,
                    'title': details.get('title')
                }
            
            if age <= 1:
                dirty_count_24h += 1
        else:
            unknown += 1
    
    # Determine health
    if dirty == 0:
        status = "EXCELLENT"
        message = "All PRs are clean and ready to merge!"
    elif dirty <= len(daily_prs) * 0.2:  # <= 20% dirty
        status = "GOOD"
        message = f"Most PRs are clean. Only {dirty} have conflicts."
    elif dirty <= len(daily_prs) * 0.5:  # <= 50% dirty
        status = "WARNING"
        message = f"{dirty} out of {len(daily_prs)} PRs have conflicts."
    else:
        status = "CRITICAL"
        message = f"Most PRs are conflicted ({dirty}/{len(daily_prs)})!"
    
    return {
        'status': status,
        'message': message,
        'total_daily_prs': len(daily_prs),
        'clean': clean,
        'dirty': dirty,
        'unknown': unknown,
        'draft': draft,
        'dirty_24h': dirty_count_24h,
        'oldest_dirty': oldest_dirty,
        'closed_last_24h': get_closed_prs_last_day(owner, repo, token),
    }


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_section(title: str):
    """Print a formatted section."""
    print(f"\n{title}")
    print("-" * 80)


def main():
    """Main function."""
    owner = os.environ.get('GITHUB_REPOSITORY_OWNER', 'ramincsy')
    repo = os.environ.get('GITHUB_REPOSITORY_NAME', 'Auto')
    
    token = get_github_token()
    
    print_header("🔍 PR AUTO-MERGE SYSTEM STATUS REPORT")
    
    # Repository info
    repo_info = get_repo_info(owner, repo, token)
    print(f"Repository: {owner}/{repo}")
    print(f"URL: {repo_info.get('url', 'N/A')}")
    print(f"Default Branch: {repo_info.get('default_branch', 'main')}")
    print(f"Stars: {repo_info.get('stars', 0)}")
    
    # System health
    health = analyze_system_health(owner, repo, token)
    
    print_section("📊 SYSTEM HEALTH")
    print(f"Status: {health['status']}")
    print(f"Message: {health['message']}")
    
    print_section("📈 PR STATISTICS")
    print(f"Total Daily PRs: {health['total_daily_prs']}")
    print(f"  ✅ Clean (ready): {health['clean']}")
    print(f"  ⚠️  Dirty (conflicts): {health['dirty']}")
    print(f"  🔄 Unknown (checking): {health['unknown']}")
    print(f"  📋 Draft: {health['draft']}")
    print(f"  ✨ Merged (last 24h): {health['closed_last_24h']}")
    
    # Oldest dirty PR
    if health['oldest_dirty']:
        oldest = health['oldest_dirty']
        print_section("⚠️  OLDEST CONFLICTED PR")
        print(f"PR #{oldest['number']}: {oldest['title'][:60]}")
        print(f"Age: {oldest['age_days']} day(s)")
        print(f"🔗 https://github.com/{owner}/{repo}/pull/{oldest['number']}")
    
    # Recommendations
    print_section("💡 RECOMMENDATIONS")
    
    if health['status'] == "EXCELLENT":
        print("✅ System is working perfectly!")
        print("   - All daily PRs are clean")
        print("   - Auto-merge should complete successfully")
    
    elif health['status'] == "GOOD":
        print("✅ System is mostly healthy")
        print(f"   - {health['dirty']} PR(s) have conflicts")
        print("   - Run: python scripts/resolve_conflicts.py --auto-resolve")
        print("   - Then: python scripts/auto_merge_prs.py")
    
    elif health['status'] == "WARNING":
        print("⚠️  System needs attention")
        print(f"   - {health['dirty']} out of {health['total_daily_prs']} PRs have conflicts")
        print("   - Action: Run conflict resolution")
        print("   Command: python scripts/resolve_conflicts.py --auto-resolve")
        if health['dirty_24h'] > 0:
            print(f"   - {health['dirty_24h']} conflict(s) from last 24 hours")
    
    else:  # CRITICAL
        print("🚨 System requires immediate attention!")
        print(f"   - {health['dirty']} out of {health['total_daily_prs']} PRs are conflicted")
        print("   - Run: python scripts/resolve_conflicts.py --force-merge")
        print("   - Then check manual resolution for remaining PRs")
        print("   - See: CONFLICT_RESOLUTION_GUIDE.md")
    
    # Usage guidance
    print_section("📚 QUICK COMMANDS")
    print("Check conflicts:       python scripts/resolve_conflicts.py")
    print("Auto-resolve:          python scripts/resolve_conflicts.py --auto-resolve")
    print("Force merge:           python scripts/resolve_conflicts.py --force-merge")
    print("Auto-merge clean:      python scripts/auto_merge_prs.py")
    print("Full pipeline:         python scripts/resolve_conflicts.py --auto-resolve && python scripts/auto_merge_prs.py")
    
    # Schedule info
    print_section("⏰ AUTOMATED SCHEDULE")
    print("The system runs automatically on:")
    print("  • 01:00 UTC (daily)")
    print("  • 13:00 UTC (daily)")
    print("")
    print("Steps:")
    print("  1. Attempt conflict resolution")
    print("  2. Merge all clean PRs")
    print("  3. Report results to workflow logs")
    
    print_section("📖 FOR MORE INFORMATION")
    print("See: CONFLICT_RESOLUTION_GUIDE.md")
    print("     MERGE_QUICK_REFERENCE.md")
    
    # Footer
    print("\n" + "="*80)
    print(f"  Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
