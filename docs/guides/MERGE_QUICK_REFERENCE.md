# Quick Reference: PR Auto-Merge System

## 🚀 One-Line Solutions

### Check for Conflicts
```bash
python scripts/resolve_conflicts.py
```

### Fix All Conflicts Automatically
```bash
python scripts/resolve_conflicts.py --auto-resolve
```

### Force Merge Stuck Conflicts
```bash
python scripts/resolve_conflicts.py --force-merge
```

### Auto-Merge Clean PRs
```bash
python scripts/auto_merge_prs.py
```

### Do Everything (Recommended)
```bash
python scripts/resolve_conflicts.py --auto-resolve && python scripts/auto_merge_prs.py
```

---

## 📊 Understanding PR States

| State | Symbol | Meaning | Action |
|-------|--------|---------|--------|
| clean | ✅ | Ready to merge | Merge immediately |
| dirty | ⚠️ | Has conflicts | Update branch → merge |
| unknown | 🔄 | Still checking | Wait 30 sec, retry |

---

## 🔧 Manual Fix (Last Resort)

```bash
# Get the problematic branch
git fetch origin
git checkout branch-name

# Rebase with main to find conflicts
git rebase origin/main

# Fix conflicts in your editor (look for <<<<<<, ======, >>>>>>)

# Complete the fix
git add .
git rebase --continue
git push -f origin branch-name

# GitHub will auto-merge when clean ✅
```

---

## ⏰ Automatic Schedule

**GitHub Actions runs every day at:**
- 01:00 UTC (1 AM)
- 13:00 UTC (1 PM)

**Automatically:**
1. ✅ Attempts conflict resolution
2. ✅ Merges all clean PRs
3. ✅ Reports results

---

## 🎯 Success Metrics

After running the auto-merge system:

- **All new daily PRs merged**: ✅
- **Old PRs with conflicts resolved**: ✅
- **Manual intervention needed**: ❌ (rare)

---

## 📍 Key Files

| File | Purpose |
|------|---------|
| `scripts/auto_merge_prs.py` | Main merge script |
| `scripts/resolve_conflicts.py` | Conflict resolver |
| `.github/workflows/auto-merge.yml` | GitHub Actions workflow |
| `CONFLICT_RESOLUTION_GUIDE.md` | Full documentation |

---

## 💡 Common Tasks

### See all open PRs
```bash
python scripts/resolve_conflicts.py
```

### Merge one specific PR
```bash
gh pr merge 42 --squash
```

### List open daily PRs
```bash
gh pr list --state open --search "Daily Update"
```

### Check PR merge status
```bash
gh pr view 42 --json mergeable,mergeable_state
```

---

## ⚡ Emergency: Manually Merge All

```bash
# For each conflicted PR:
gh pr merge <PR_NUMBER> --squash --admin

# Example:
gh pr merge 42 --squash --admin
gh pr merge 43 --squash --admin
```

---

**Need help?** See `CONFLICT_RESOLUTION_GUIDE.md` for detailed documentation.
