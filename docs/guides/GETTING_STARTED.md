# Getting Started with Auto-Merge System

## 🚀 Quick Start (5 Minutes)

### Step 1: Check System Status
```bash
python scripts/pr_status_report.py
```

This shows:
- How many PRs are ready to merge
- How many have conflicts
- What action to take

### Step 2: Resolve Conflicts (if any)
```bash
python scripts/resolve_conflicts.py --auto-resolve
```

This automatically fixes conflicted PRs by updating their branches.

### Step 3: Merge Clean PRs
```bash
python scripts/auto_merge_prs.py
```

This merges all ready-to-go PRs.

---

## ✨ That's It!

The system now automatically:
- ✅ Runs twice daily (1 AM and 1 PM UTC)
- ✅ Resolves conflicts automatically
- ✅ Merges all eligible PRs
- ✅ Reports results

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [MERGE_QUICK_REFERENCE.md](MERGE_QUICK_REFERENCE.md) | 1-page quick commands |
| [CONFLICT_RESOLUTION_GUIDE.md](CONFLICT_RESOLUTION_GUIDE.md) | Complete guide & troubleshooting |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Technical details |

---

## 🔧 Useful Commands

### See what's happening
```bash
python scripts/pr_status_report.py
```

### Fix conflicts only
```bash
python scripts/resolve_conflicts.py --auto-resolve
```

### Merge ready PRs only
```bash
python scripts/auto_merge_prs.py
```

### Do everything
```bash
python scripts/resolve_conflicts.py --auto-resolve && python scripts/auto_merge_prs.py
```

### Force merge everything (last resort)
```bash
python scripts/resolve_conflicts.py --force-merge
```

---

## ⚙️ Setup (One-Time)

### 1. Set GitHub Token
```bash
export GITHUB_TOKEN="your_personal_access_token"
```

Or in GitHub Actions (already configured):
- Uses `${{ secrets.GITHUB_TOKEN }}`

### 2. Verify Installation
```bash
# Check Python version
python --version  # Should be 3.7+

# Check requests library
pip install requests
```

### 3. Test It
```bash
python scripts/pr_status_report.py
```

---

## 🎯 What Happens Automatically

Every day at:
- **01:00 UTC** (1 AM)
- **13:00 UTC** (1 PM)

The system:
1. 🔧 Attempts to resolve any conflicts
2. 🔄 Merges all clean PRs
3. 📊 Logs the results

You'll see the results in:
- GitHub Actions workflow logs
- PR status on GitHub

---

## ❓ FAQ

**Q: Do I need to do anything?**  
A: No! The system runs automatically. Just set the GITHUB_TOKEN once.

**Q: What if a PR has conflicts?**  
A: The system automatically tries to fix it. If it can't, run `resolve_conflicts.py --auto-resolve`.

**Q: Can I merge manually?**  
A: Yes, but you don't need to. The system does it automatically.

**Q: How do I know it's working?**  
A: Check `python scripts/pr_status_report.py` or view GitHub Actions.

**Q: What if something breaks?**  
A: See CONFLICT_RESOLUTION_GUIDE.md for troubleshooting.

---

## 🚀 Next Steps

1. ✅ You're all set!
2. 📅 The system runs automatically
3. 📊 Monitor with `pr_status_report.py`
4. 🔖 Check documentation if needed

---

## 📞 Need Help?

1. **Quick answer**: See MERGE_QUICK_REFERENCE.md
2. **Detailed help**: See CONFLICT_RESOLUTION_GUIDE.md
3. **Technical details**: See IMPLEMENTATION_SUMMARY.md
4. **Check system health**: `python scripts/pr_status_report.py`

---

**Your auto-merge system is ready to use!** 🎉
