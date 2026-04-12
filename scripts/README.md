# Scripts Overview

## Priority 1: Active Automation

- `auto_merge_prs.py`
- `resolve_conflicts.py`
- `pr_status_report.py`
- `generate_weekly_focus.py`
- `validate_installation.py`

These scripts directly support the active GitHub Actions workflows or operational health checks.

## Priority 2: Manual Daily / Maintenance Tools

- `review_and_merge_prs.py`
- `close_all_prs.py`
- `log_daily.py`
- `merge_daily_updates.py`

These scripts are useful for manual intervention and maintenance, but they are not part of the default scheduled path.
Prefer `auto_merge_prs.py` over `merge_daily_updates.py` for normal merge work.

## Priority 3: Manual Bulk Helpers

- `generate_multiple_contributions.py`
- `create_contribution_branches.py`
- `create_multiple_prs.py`
- `review_contributions.py`

These scripts are intentionally manual-only. They should be used carefully and only when high-volume activity is explicitly desired.
They support `BULK_COUNT` for safer sizing, and `review_contributions.py` defaults to transparent comment reviews unless approval is explicitly requested.

## Removed From Active Workflow Use

- `advanced_code_review.py`
- `create_github_issues.py`

These were part of the older high-volume activity design and were removed during repository cleanup.
