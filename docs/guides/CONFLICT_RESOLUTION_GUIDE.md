# Automatic PR Merge System - Conflict Resolution Guide

## Overview

The auto-merge system now has three-tier conflict handling:

1. **Auto-merge**: Merges clean PRs automatically (runs every hour)
2. **Conflict resolution**: Attempts to resolve conflicts by rebasing (runs before auto-merge)
3. **Manual resolution**: Provides instructions for stubborn conflicts

## System Status

### How Conflicts Occur

When the `main` branch is updated after a PR is created, the PR can become "dirty" (conflicted):

- **Mergeable state**: `dirty` = PR has conflicts
- **Mergeable state**: `clean` = PR is ready to merge
- **Mergeable state**: `unknown` = GitHub is still checking

### Automatic Resolution Process

1. **Initial state**: PR is created with `mergeable_state: "dirty"`
2. **Auto-update**: Script calls GitHub API to update branch (rebase with main)
3. **GitHub processes**: Takes 15-30 seconds to compute new merge status
4. **Auto-merge**: If resolved, PR is merged automatically

## Available Commands

### 1. Check for Conflicts (No Changes)

```bash
python scripts/resolve_conflicts.py
```

Shows which PRs have conflicts and their current status.

**Output:**
```
⚠️  PR #42: Daily Update - 2024-04-12
    State: dirty (has conflicts)
    Created: 2024-04-12

✅ PR #41: Daily Update - 2024-04-11
    State: clean (ready to merge)
```

### 2. Automatically Resolve and Merge Conflicts

```bash
python scripts/resolve_conflicts.py --auto-resolve
```

Attempts to resolve all conflicted PRs by:
1. Updating branch from main (GitHub's rebase)
2. Waiting 20 seconds for processing
3. Checking if conflicts are resolved
4. Merging if clean

**Recommended for**: Daily use in workflow or cron jobs

### 3. Force Merge Conflicted PRs

```bash
python scripts/resolve_conflicts.py --force-merge
```

Force merges PRs that still have conflicts using squash merge.

**⚠️ Warning**: Only use if:
- You've manually verified the PR content is correct
- Conflicts are minor (e.g., update dates)
- The PR contains only daily contribution files

### 4. Run Full Auto-Merge

```bash
python scripts/auto_merge_prs.py
```

Merges all clean PRs automatically (without conflict resolution).

### 5. Run Complete Workflow

```bash
python scripts/resolve_conflicts.py --auto-resolve && \
python scripts/auto_merge_prs.py
```

Or use GitHub Actions (runs automatically on schedule):
- Every day at 01:00 UTC (after morning contribution)
- Every day at 13:00 UTC (after afternoon contribution)

## Manual Conflict Resolution

If automatic resolution fails, follow these steps:

### For a Single PR

```bash
# Get the latest from remote
git fetch origin

# Switch to the PR branch
git checkout your-branch-name

# Rebase with main
git rebase origin/main

# Fix conflicts in your editor
# Files will be marked with <<<<<<, ======, >>>>>>

# Mark conflicts as resolved
git add .

# Complete the rebase
git rebase --continue

# Push the changes
git push -f origin your-branch-name
```

After pushing, GitHub will automatically process the update and the PR should merge.

### For Multiple PRs

```bash
# List all open daily PRs
gh pr list --state open --search "Daily Update" --json number,title,headRefName

# For each conflicted PR:
# 1. Check out the branch
# 2. Rebase from main
# 3. Resolve conflicts
# 4. Push with force
```

## Workflow Architecture

### Scheduled Auto-Merge

**File**: `.github/workflows/auto-merge.yml`

```
Triggers:
  ├── Cron: 01:00 UTC daily
  └── Cron: 13:00 UTC daily

Steps:
  1. Resolve Conflicts (--auto-resolve)
     └─ Attempts to fix dirty PRs
  
  2. Auto-Merge (auto_merge_prs.py)
     └─ Merges all clean PRs
  
  3. Report Results
     └─ Logs summary of actions
```

### Script Hierarchy

```
auto_merge_prs.py (Main)
  ├─ Fetches all open daily PRs
  ├─ Checks each PR's mergeable state
  ├─ Attempts to update dirty PRs
  └─ Merges clean PRs

resolve_conflicts.py (Helper)
  ├─ Analyzes PR conflicts
  ├─ Updates branches from main
  ├─ Force merges if requested
  └─ Provides manual instructions
```

## Handling Different Mergeable States

| State | Meaning | Action |
|-------|---------|--------|
| `clean` | No conflicts | Merge immediately |
| `dirty` | Has conflicts | Update branch or manual fix |
| `unknown` | Still checking | Wait and retry |
| `blocked` | CI failed | Fix and push, or wait for retry |
| `behind` | Behind main | Update branch |

## Troubleshooting

### PR Still Shows "dirty" After Auto-Update

**Cause**: Merge conflicts can't be automatically resolved
**Solution**: Run manual resolution or force merge

```bash
# Manual: Follow manual steps above
git checkout branch-name
git rebase origin/main
# ... fix conflicts ...
git push -f origin branch-name

# Or force merge:
python scripts/resolve_conflicts.py --force-merge
```

### "Cannot automatically merge" Error

**Cause**: GitHub can't rebase the branches (complex conflicts)
**Solution**: Manually resolve or update branch first

```bash
# Pull latest main
git fetch origin
git checkout main
git pull origin main

# Now rebase your feature branch
git checkout your-branch
git rebase main
# Fix conflicts...
```

### Workflow Timeout

**Cause**: Too many PRs or network issues
**Solution**: Run script locally or split into batches

```bash
# Run with smaller batch
python scripts/auto_merge_prs.py

# Check specific PR
python scripts/resolve_conflicts.py | grep "PR #NUMBER"
```

## Best Practices

### For Developers

1. **Keep PRs small**: Easier to merge without conflicts
2. **Update regularly**: If PR sits > 1 day, update branch manually
3. **Communicate**: If PR needs special handling, add notes

### For Maintenance

1. **Run conflict resolution first**: Always attempt auto-resolve before merge
2. **Monitor workflow logs**: Check GitHub Actions results
3. **Manual intervention**: Only when auto-resolution truly fails
4. **Force merge sparingly**: Only for simple, auto-generated PRs

### For GitHub Actions

1. **Runs twice daily**: 01:00 and 13:00 UTC
2. **Continues on error**: Won't stop if conflict resolution fails
3. **Full logs**: Check Actions tab for detailed output
4. **Can trigger manually**: Use "Run workflow" for urgent cases

## Configuration

### Environment Variables

Required in GitHub Actions or local environment:

```bash
export GITHUB_TOKEN="your_personal_access_token"
# OR
export GH_TOKEN="your_personal_access_token"
```

### Repository Requirements

- **Branch protection**: Not required (but recommended for other branches)
- **Auto-merge setting**: Not required (we do it via API)
- **Permissions**: Token needs `repo` scope

### Customization

Edit script variables:

```python
# In auto_merge_prs.py
OWNER = "ramincsy"
REPO = "Auto"

# Filter by PR title
if 'Daily Update' in pr['title'] or 'daily-contribution' in pr['title']

# Change merge method
merge_method="merge"  # or "squash" or "rebase"
```

## Monitoring

### Check Recent PR Status

```bash
# Using GitHub CLI
gh pr list --state all --json number,title,state,mergeable

# Using script
python scripts/resolve_conflicts.py
```

### View Workflow Results

1. Go to repository
2. Click "Actions" tab
3. Find "Auto Merge Daily PRs" workflow
4. Click latest run for details

### Track Merged PRs

Check repository insights or recently closed PRs:
```bash
gh pr list --state closed --limit 20
```

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Check conflicts | 2-3 sec | Per PR |
| Update branch | 5-10 sec | Async operation |
| GitHub processing | 15-30 sec | Varies with complexity |
| Merge PR | 2-3 sec | Per PR |
| Full workflow | 2-5 min | For 10+ PRs |

## Summary

This system provides **fully automated** PR merging with intelligent conflict handling:

✅ **Auto-detects** dirty PRs  
✅ **Auto-resolves** conflicts via rebase  
✅ **Auto-merges** clean PRs  
✅ **Auto-reports** results  
✅ **Provides guidance** for manual fixes  

All with **zero manual intervention** during normal operation.

---

**Last Updated**: April 12, 2026  
**Maintainer**: GitHub Copilot
