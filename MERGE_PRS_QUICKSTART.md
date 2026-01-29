# 🚀 Quick Guide: Review & Merge Pull Requests for GitHub Achievements

## 🎯 Goal
Merge your daily contribution PRs efficiently to earn GitHub achievements!

## ⚡ Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
cd Auto
pip install -r requirements.txt
```

### Step 2: Set GitHub Token
```bash
export GITHUB_TOKEN='your_token_here'
```

Get your token: [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
- Select scope: `repo` (full control)

### Step 3: Review & Merge
```bash
# Option A: Review only (no merging)
python scripts/review_and_merge_prs.py

# Option B: Auto-merge ready PRs
python scripts/review_and_merge_prs.py --auto-merge
```

## 🎯 GitHub Achievements You'll Earn

| Achievement | Requirement | How to Get It |
|------------|-------------|---------------|
| 🦈 Pull Shark | Merge 4+ PRs | ✅ Merge 4+ PRs (automatic) |
| ⚡ Quickdraw | Merge within 30 min | Merge new PRs quickly |
| 🎉 YOLO | Merge without review | Merge daily PRs (they don't need review) |
| 🎓 Open Sourcerer | Active for 2+ months | ⏳ Wait until mid-Feb 2026 |
| ⭐ Starstruck | 25+ stars | Share repo with friends |
| 🧠 Galaxy Brain | 4+ approved reviews | Ask friends to review/approve |
| 👯 Pair Extraordinaire | Co-authored commits | Add co-authors to commits |

## 📊 What the Script Does

### Review Mode (no merging):
```bash
python scripts/review_and_merge_prs.py
```

**Output:**
- ✅ Lists all open PRs
- ✅ Shows which are ready to merge
- ⚠️ Shows which have conflicts
- 📊 Shows file changes
- 💡 Provides recommendations

### Auto-Merge Mode:
```bash
python scripts/review_and_merge_prs.py --auto-merge
```

**What it does:**
1. Analyzes all open PRs
2. Identifies ready-to-merge PRs
3. Asks for confirmation
4. Merges all ready PRs
5. Shows achievement progress

## 💡 Best Strategy for Maximum Achievements

### Day 1: Merge Existing PRs
```bash
python scripts/review_and_merge_prs.py --auto-merge
```
**Result:** 🦈 Pull Shark + 🎉 YOLO unlocked!

### Daily: Quick Merge New PRs
When a new daily PR is created:
```bash
# Within 5-10 minutes:
python scripts/review_and_merge_prs.py --auto-merge
```
**Result:** ⚡ Quickdraw unlocked!

### Week 1-2: Get Reviews
- Ask 4 friends to review and approve different PRs
- **Result:** 🧠 Galaxy Brain unlocked!

### Week 2-3: Co-Author Commits
- Add friends as co-authors in commits:
```bash
git commit -m "feat: update content

Co-authored-by: Friend Name <friend@email.com>"
```
**Result:** 👯 Pair Extraordinaire unlocked!

### Month 2: Wait
- Keep making daily contributions
- **Result:** 🎓 Open Sourcerer unlocked!

## 🔍 Example Output

```
🔍 Fetching GitHub token...
📋 Fetching open pull requests for ramincsy/Auto...

🔍 Analyzing 30 pull request(s)...
  Analyzing PR #3423... ✅
  Analyzing PR #3422... ✅
  ...

================================================================================
📊 PULL REQUEST ANALYSIS
================================================================================

✅ Ready to Merge: 28
⚠️  Has Conflicts: 0
🔄 Still Checking: 0
👀 Review Manually: 2

✅ READY TO MERGE:
--------------------------------------------------------------------------------
  #3423: Daily Update daily-contribution-2026-01-22
    Files: updates/2026/01/22.md, README.md
    Created: 2026-01-22
  ...

💡 To automatically merge ready PRs, run:
   python scripts/review_and_merge_prs.py --auto-merge
```

## ⚠️ Important Notes

1. **Conflicts:** If a PR has conflicts, resolve manually
2. **Rate Limits:** If you hit API rate limits, wait a few minutes
3. **Manual Review:** Non-daily PRs should be reviewed manually
4. **Token Security:** Never commit your token to the repository

## 🆚 Script Comparison

| Feature | close_all_prs.py | review_and_merge_prs.py |
|---------|------------------|-------------------------|
| List PRs | ✅ | ✅ |
| Close PRs | ✅ | ❌ |
| Merge PRs | ❌ | ✅ |
| Analyze PRs | ❌ | ✅ |
| Check conflicts | ❌ | ✅ |
| Show files | ❌ | ✅ |
| Recommendations | ❌ | ✅ |
| Track achievements | ❌ | ✅ |

**Use `close_all_prs.py`:** When you want to close PRs without merging
**Use `review_and_merge_prs.py`:** When you want to merge PRs properly

## 🐛 Troubleshooting

### "No GitHub token found"
```bash
# Check if token is set:
echo $GITHUB_TOKEN

# Set it:
export GITHUB_TOKEN='your_token_here'
```

### "Error 401: Unauthorized"
- Your token is invalid or expired
- Create a new token

### "Error 403: Forbidden"
- Your token doesn't have `repo` scope
- Create a new token with proper permissions

### "Merge failed"
- PR might have conflicts
- Branch might be deleted
- Review manually on GitHub

## 📚 Full Documentation

- **Persian Guide:** [MERGE_PRS_GUIDE.md](./MERGE_PRS_GUIDE.md)
- **Close PRs Guide:** [CLOSE_PRS_GUIDE.md](./CLOSE_PRS_GUIDE.md)
- **Achievements Guide:** [ACHIEVEMENTS.md](./ACHIEVEMENTS.md)
- **How to Invite Friends:** [HOW_TO_INVITE_FRIENDS.md](./HOW_TO_INVITE_FRIENDS.md)

## 🎯 Summary

1. **Now:** Merge ready PRs → Get Pull Shark + YOLO
2. **Daily:** Merge new PRs quickly → Get Quickdraw
3. **Weekly:** Get friend reviews → Get Galaxy Brain
4. **Monthly:** Keep contributing → Get Open Sourcerer

Happy merging! 🚀
